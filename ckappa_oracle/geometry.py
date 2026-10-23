"""Folds, output groups, and the synthetic-chart embedding."""

from __future__ import annotations

import numpy as np

ORBITS = {
    "A": (0, 5, 10, 15),
    "B": (1, 4, 11, 14),
    "C": (2, 7, 8, 13),
    "D": (3, 6, 9, 12),
}

# (name, fit orbits, evaluation orbits), in the v1.1 listed order.
FOLD_SPEC = (
    ("AB->CD", ("A", "B"), ("C", "D")),
    ("CD->AB", ("C", "D"), ("A", "B")),
    ("AC->BD", ("A", "C"), ("B", "D")),
    ("BD->AC", ("B", "D"), ("A", "C")),
    ("AD->BC", ("A", "D"), ("B", "C")),
    ("BC->AD", ("B", "C"), ("A", "D")),
)

GROUP_INDEX = {
    "MARG": (0, 1),
    "XOR": (2,),
    "ALL": (0, 1, 2),
}
GROUPS = ("MARG", "XOR", "ALL")
SECTION5_GROUPS = ("ALL", "MARG")


def prefixes_of(orbits) -> tuple:
    return tuple(sorted(prefix for name in orbits for prefix in ORBITS[name]))


def folds():
    return tuple(
        (name, prefixes_of(fit_orbits), prefixes_of(eval_orbits))
        for name, fit_orbits, eval_orbits in FOLD_SPEC
    )


def squared_error(vector: np.ndarray, group: str) -> float:
    return float(sum(float(vector[index]) ** 2 for index in GROUP_INDEX[group]))


def weighted_mean_and_sd(values: np.ndarray, weights: np.ndarray):
    """P-weighted mean and population standard deviation, one column at a time."""
    weight = np.asarray(weights, dtype=np.float64)
    total = float(weight.sum())
    mean = (weight[:, None] * values).sum(axis=0) / total
    variance = (weight[:, None] * (values - mean) ** 2).sum(axis=0) / total
    sd = np.sqrt(variance)
    return mean, sd


def monomials(mu_x: float, mu_y: float) -> np.ndarray:
    return np.array(
        [1.0, mu_x, mu_y, mu_x * mu_x, mu_x * mu_y, mu_y * mu_y],
        dtype=np.float64,
    )


def g_value(coef: np.ndarray, mu_x: float, mu_y: float) -> float:
    basis = monomials(mu_x, mu_y)
    return float(coef @ basis)


def g_gradient(coef: np.ndarray, mu_x: float, mu_y: float) -> np.ndarray:
    # d/d(mu_x, mu_y) of c0 + c1 x + c2 y + c3 x^2 + c4 x y + c5 y^2
    return np.array(
        [
            coef[1] + 2.0 * coef[3] * mu_x + coef[4] * mu_y,
            coef[2] + coef[4] * mu_x + 2.0 * coef[5] * mu_y,
        ],
        dtype=np.float64,
    )
