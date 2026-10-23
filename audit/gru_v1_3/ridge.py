"""Closed-form weighted ridge with an unpenalized intercept.

The fit minimizes, on a fit set S with ŵ = w / sum_S w,

    J(b, β) = Σ ŵ ||q - b - Z β||^2 + λ ||β||^2_F

Z is standardized with the fit-set ŵ-weighted mean and population sd.
A column with ŵ-weighted variance <= 1e-24 is excluded (coefficient 0).
Predictions are not clipped. The SVD solution is not truncated.
"""

from __future__ import annotations

import numpy as np

from audit.gru_v1_3.domain import BOUNDARY_GUARD, LAMBDA_GRID, VAR_MAX


def comparison_label(delta: float, floor: float) -> str:
    if delta > floor + BOUNDARY_GUARD:
        return "meets-floor"
    if delta < floor - BOUNDARY_GUARD:
        return "below-floor"
    return "BOUNDARY"


def combine_labels(c1: str, c2: str) -> str:
    """F5: meets only if both meet; below if either is below; otherwise BOUNDARY."""
    if c1 == "below-floor" or c2 == "below-floor":
        return "below-floor"
    if c1 == "meets-floor" and c2 == "meets-floor":
        return "meets-floor"
    return "BOUNDARY"


def _population_var(weight: np.ndarray, values: np.ndarray) -> np.ndarray:
    if values.ndim == 1:
        mu = weight @ values
        return np.array([weight @ (values - mu) ** 2])
    mu = weight @ values
    return weight @ (values - mu) ** 2


class Prepared:
    def __init__(self, keep, mu, sd, b, u, s, vt, names, n_rows, excluded):
        self.keep = keep
        self.mu = mu
        self.sd = sd
        self.b = b
        self.u = u
        self.s = s
        self.vt = vt
        self.names = names
        self.n_rows = n_rows
        self.excluded = excluded
        self.rank_info = rank_report(s, n_rows, int(keep.sum()) if keep is not None else 0)

    def beta(self, lam: float) -> np.ndarray:
        if self.s.size == 0:
            return np.zeros((0, self.b.shape[0]), dtype=np.float64)
        filt = np.zeros_like(self.s)
        positive = self.s > 0
        filt[positive] = self.s[positive] / (self.s[positive] ** 2 + lam)
        # UtY was stored in self.u, shape (r, k)
        return self.vt.T @ (filt[:, None] * self.u)

    def predict(self, x: np.ndarray, lam: float) -> np.ndarray:
        beta = self.beta(lam)
        if beta.shape[0] == 0:
            return np.broadcast_to(self.b, (x.shape[0], self.b.shape[0])).copy()
        z = (x[:, self.keep] - self.mu) / self.sd
        return self.b + z @ beta


def rank_report(s: np.ndarray, n_rows: int, p_kept: int) -> dict:
    if p_kept == 0 or s.size == 0 or not np.isfinite(s).all() or s[0] == 0:
        return {
            "features_after_exclusion": int(p_kept),
            "rank": 0,
            "rank_deficient": True,
            "condition_number": "inf",
            "sigma_max": None if s.size == 0 else float(s[0]),
            "sigma_min": None if s.size == 0 else float(s[-1]),
            "sigma_rank": None,
            "sigma_max_over_sigma_rank": None,
        }
    tol = float(s[0] * max(n_rows, p_kept) * np.finfo(np.float64).eps)
    rank = int(np.sum(s > tol))
    deficient = rank < min(n_rows, p_kept)
    sigma_rank = float(s[rank - 1]) if rank else None
    return {
        "features_after_exclusion": int(p_kept),
        "rank": rank,
        "rank_deficient": bool(deficient),
        "condition_number": "inf" if deficient else float(s[0] / s[-1]),
        "sigma_max": float(s[0]),
        "sigma_min": float(s[-1]),
        "sigma_rank": sigma_rank,
        "sigma_max_over_sigma_rank": None if not sigma_rank else float(s[0] / sigma_rank),
        "FLAG": "RANK-DEFICIENT" if deficient else None,
    }


def prepare(x: np.ndarray, y: np.ndarray, w: np.ndarray, names: list[str] | None = None) -> Prepared:
    weight = np.asarray(w, dtype=np.float64)
    weight = weight / weight.sum()
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    if y.ndim == 1:
        y = y[:, None]
    n_rows, p_cols = x.shape
    if names is None:
        names = ["x%d" % i for i in range(p_cols)]
    mu_x = weight @ x
    var = weight @ (x - mu_x) ** 2
    keep = var > VAR_MAX
    excluded = [names[i] for i in range(p_cols) if not keep[i]]
    b = weight @ y
    if not np.any(keep):
        return Prepared(keep, np.zeros(0), np.zeros(0), b, np.zeros((0, y.shape[1])), np.zeros(0), np.zeros((0, 0)), names, n_rows, excluded)
    sd = np.sqrt(var[keep])
    z = (x[:, keep] - mu_x[keep]) / sd
    sw = np.sqrt(weight)
    design = sw[:, None] * z
    y_centered = y - b
    yw = sw[:, None] * y_centered
    u, s, vt = np.linalg.svd(design, full_matrices=False)
    ut_y = u.T @ yw
    return Prepared(keep, mu_x[keep], sd, b, ut_y, s, vt, names, n_rows, excluded)


class Design:
    """SVD of the standardized design. The target is applied later."""

    def __init__(self, keep, mu, sd, b_weight, sw, u, s, vt, excluded, n_rows, names):
        self.keep = keep
        self.mu = mu
        self.sd = sd
        self.b_weight = b_weight
        self.sw = sw
        self.u = u
        self.s = s
        self.vt = vt
        self.excluded = excluded
        self.names = names
        self.rank_info = rank_report(s, n_rows, int(np.sum(keep)) if np.size(keep) else 0)

    def predict(self, x: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
        y = np.asarray(y, dtype=np.float64)
        if y.ndim == 1:
            y = y[:, None]
        b = self.b_weight @ y
        if self.s.size == 0:
            return np.broadcast_to(b, (x.shape[0], y.shape[1])).copy()
        yw = self.sw[:, None] * (y - b)
        ut_y = self.u.T @ yw
        filt = np.zeros_like(self.s)
        positive = self.s > 0
        filt[positive] = self.s[positive] / (self.s[positive] ** 2 + float(lam))
        beta = self.vt.T @ (filt[:, None] * ut_y)
        z = (x[:, self.keep] - self.mu) / self.sd
        return b + z @ beta


def fit_design(x: np.ndarray, w: np.ndarray, idx: np.ndarray, names: list[str] | None = None) -> Design:
    weight = np.asarray(w, dtype=np.float64)[idx]
    weight = weight / weight.sum()
    x_fit = np.asarray(x, dtype=np.float64)[idx]
    n_rows, p_cols = x_fit.shape
    if names is None:
        names = ["x%d" % i for i in range(p_cols)]
    mu_x = weight @ x_fit
    var = weight @ (x_fit - mu_x) ** 2
    keep = var > VAR_MAX
    excluded = [names[i] for i in range(p_cols) if not keep[i]]
    if not np.any(keep):
        return Design(keep, np.zeros(0), np.zeros(0), weight, np.sqrt(weight), np.zeros((n_rows, 0)), np.zeros(0), np.zeros((0, 0)), excluded, n_rows, names)
    sd = np.sqrt(var[keep])
    z = (x_fit[:, keep] - mu_x[keep]) / sd
    sw = np.sqrt(weight)
    design = sw[:, None] * z
    u, s, vt = np.linalg.svd(design, full_matrices=False)
    return Design(keep, mu_x[keep], sd, weight, sw, u, s, vt, excluded, n_rows, names)


def squared_error(pred: np.ndarray, y: np.ndarray) -> np.ndarray:
    y = np.asarray(y, dtype=np.float64)
    if y.ndim == 1:
        y = y[:, None]
    return np.sum((pred - y) ** 2, axis=1)


def select_lambda(losses: dict) -> float:
    """Largest λ whose inner loss is within 1e-12 relative of the minimum."""
    best = min(losses.values())
    tied = []
    for lam in LAMBDA_GRID:
        loss = losses[lam]
        if best == 0.0:
            ok = loss == 0.0
        else:
            ok = (loss - best) <= 1e-12 * abs(best)
        if ok:
            tied.append(lam)
    if not tied:
        raise RuntimeError("lambda selection found no tied value")
    return max(tied)


def inner_lambda(x, y, w, fit_idx, orbits, names=None) -> tuple[float, dict]:
    """Leave-one-depth-5-orbit-out λ on one outer fit set. One SVD per orbit."""
    prepared = []
    holdouts = []
    for orbit in orbits:
        complement = np.setdiff1d(fit_idx, orbit, assume_unique=False)
        model = prepare(x[complement], y[complement], w[complement], names)
        prepared.append(model)
        holdouts.append(orbit)
    losses = {}
    mass = float(np.asarray(w, dtype=np.float64)[fit_idx].sum())
    for lam in LAMBDA_GRID:
        total = 0.0
        for model, orbit in zip(prepared, holdouts):
            pred = model.predict(x[orbit], lam)
            err = squared_error(pred, y[orbit])
            total += float(np.asarray(w, dtype=np.float64)[orbit] @ err)
        losses[lam] = total / mass
    chosen = select_lambda(losses)
    return chosen, losses


def weighted_loss(err: np.ndarray, w: np.ndarray, idx: np.ndarray) -> tuple[float, float]:
    """Return (sum w*err, sum w*err / sum w) on idx."""
    weight = np.asarray(w, dtype=np.float64)[idx]
    numer = float(weight @ err[idx] if err.shape[0] != len(idx) else weight @ err)
    return numer, numer / float(weight.sum())


def eval_model_losses(x, y, w, folds, lam, names=None):
    """Fit each fold and return per-fold numerators, eval-normalized losses, and rank info."""
    fold_rows = []
    for fold in folds:
        pred, model = fit_predict_named(x, y, w, fold["fit"], lam, names)
        err = squared_error(pred, y)
        numer, normalized = weighted_loss(err, w, fold["eval"])
        fold_rows.append(
            {
                "fold": fold["name"],
                "numerator": numer,
                "loss": normalized,
                "eval_mass": float(np.asarray(w, dtype=np.float64)[fold["eval"]].sum()),
                "predictions": pred,
                "error": err,
                "rank": model.rank_info,
                "excluded": list(model.excluded),
            }
        )
    return fold_rows


def fit_predict_named(x, y, w, idx, lam, names=None):
    model = prepare(x[idx], y[idx], w[idx], names)
    return model.predict(x, lam), model


def pool_loss(fold_rows, total_mass: float, cover: int) -> float:
    return sum(row["numerator"] for row in fold_rows) / (cover * total_mass)


def identity_holds(a: float, b: float) -> bool:
    return abs(a - b) <= 1e-12 + 1e-12 * max(abs(a), abs(b))


def dhat_identity_ok(outputs: np.ndarray, q: np.ndarray, qhat: np.ndarray) -> tuple[bool, float]:
    """Check Σ (dhat - d)^2 = Σ (qhat - q)^2 per history. Return (ok, max violation)."""
    d = outputs - q
    dhat = outputs - qhat
    left = np.sum((dhat - d) ** 2, axis=1)
    right = np.sum((qhat - q) ** 2, axis=1)
    scale = np.maximum(np.abs(left), np.abs(right))
    gap = np.abs(left - right)
    tol = 1e-12 + 1e-12 * scale
    worst = float(np.max(gap - tol))
    return bool(np.all(gap <= tol)), worst


def ep_reconstruction_ok(outputs: np.ndarray, q: np.ndarray) -> tuple[bool, float]:
    direct = np.sum((outputs - q) ** 2, axis=1)
    expanded = np.sum(outputs ** 2 - 2.0 * outputs * q + q ** 2, axis=1)
    scale = np.maximum(np.abs(direct), np.abs(expanded))
    gap = np.abs(direct - expanded)
    tol = 1e-12 + 1e-12 * scale
    worst = float(np.max(gap - tol))
    return bool(np.all(gap <= tol)), worst
