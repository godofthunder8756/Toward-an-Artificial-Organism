"""One SVD supplies the rank report and the minimum-norm solution.

B2: a resolved lower-rank design, including sigma_1 = 0, is fitted and scored.
An unresolved ratio in [1e-10, 1e-6], endpoints included, is not scored.
rcond = 1e-10. Singular values with sigma_i <= rcond * sigma_1 are not inverted.
On a resolved design every ratio lies outside the unresolved band, so the
inverted set is the resolved-nonzero singular values.
"""

from __future__ import annotations

import numpy as np

from ckappa_oracle.pinned import fnum

RCOND = fnum("rcond")
BAND_LO = fnum("rank_resolved_zero_below")
BAND_HI = fnum("rank_resolved_above")


def fit_from_svd(design: np.ndarray, target: np.ndarray):
    """Fit design @ X = target from a single SVD.

    design is (m, n). target is (m, k) or (m,).
    Returns (solution or None, report). None means the design is unresolved
    and the cell is not scored.
    """
    matrix = np.asarray(design, dtype=np.float64)
    rhs = np.asarray(target, dtype=np.float64)
    single = rhs.ndim == 1
    if single:
        rhs = rhs[:, None]
    if matrix.ndim != 2 or rhs.ndim != 2 or matrix.shape[0] != rhs.shape[0]:
        raise ValueError("fit_from_svd shape")
    if not np.all(np.isfinite(matrix)) or not np.all(np.isfinite(rhs)):
        raise ValueError("non-finite design")
    u_factor, singular_values, vh_factor = np.linalg.svd(matrix, full_matrices=False)
    report = {
        "sigma": [float(value) for value in singular_values],
        "sigma_1": None,
        "ratios": None,
        "ratios_formed": False,
        "rank": None,
        "unresolved": False,
        "scored": False,
        "n_inverted": 0,
    }
    if singular_values.size == 0 or float(singular_values[0]) == 0.0:
        report["sigma_1"] = 0.0
        report["rank"] = 0
        report["scored"] = True
        solution = np.zeros((matrix.shape[1], rhs.shape[1]), dtype=np.float64)
        return (solution[:, 0] if single else solution), report
    sigma1 = float(singular_values[0])
    ratios = singular_values / sigma1
    report["sigma_1"] = sigma1
    report["ratios"] = [float(value) for value in ratios]
    report["ratios_formed"] = True
    report["rank"] = int(np.sum(ratios > BAND_HI))
    report["unresolved"] = bool(np.any((ratios >= BAND_LO) & (ratios <= BAND_HI)))
    if report["unresolved"]:
        return None, report
    cutoff = RCOND * sigma1
    inverse = np.zeros(singular_values.shape, dtype=np.float64)
    keep = singular_values > cutoff
    inverse[keep] = 1.0 / singular_values[keep]
    solution = vh_factor.T @ (inverse[:, None] * (u_factor.T @ rhs))
    report["n_inverted"] = int(np.sum(keep))
    report["scored"] = True
    return (solution[:, 0] if single else solution), report


def singular_values(matrix: np.ndarray) -> np.ndarray:
    values = np.linalg.svd(np.asarray(matrix, dtype=np.float64), full_matrices=False, compute_uv=False)
    return np.asarray(values, dtype=np.float64)
