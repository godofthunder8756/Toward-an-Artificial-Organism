"""Integer primary endpoint, paired rival envelope and exact sign gate."""

from __future__ import annotations

from fractions import Fraction
from math import comb
from statistics import mean, median

import numpy as np

from phase3b import PRIMARY


def sign_p(wins: int, losses: int) -> Fraction:
    n = wins + losses
    if n == 0:
        return Fraction(1)
    return min(Fraction(1), Fraction(2 * sum(comb(n, k) for k in range(min(wins, losses) + 1)), 2 ** n))


def _binomial_tail(k: int, n: int, p: float) -> float:
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def positive_fraction_ci(wins: int, n: int = 16) -> tuple[float, float]:
    """Two-sided 95% Clopper-Pearson interval, not episode-level replication."""
    if n < 1 or not 0 <= wins <= n:
        raise ValueError("invalid binomial counts")
    def inverse(k: int, target: float) -> float:
        lo, hi = 0.0, 1.0
        for _ in range(64):
            mid = (lo + hi) / 2
            if _binomial_tail(k, n, mid) < target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lower = 0.0 if wins == 0 else inverse(wins, 0.025)
    upper = 1.0 if wins == n else inverse(wins + 1, 0.975)
    return lower, upper


def final_gate(per_seed: dict[int, dict[str, np.ndarray]]) -> dict:
    """Arrays must contain all 4096 held-out episode *joint* integer sums.

    Each episode is the sum of component units (S1/S3=50, S2 abstain=9).
    Threshold .02 in joint loss is 3 units per episode. Missing comparators,
    EXTERNAL controls or malformed seeds never silently enter the envelope.
    """
    if set(per_seed) != set(range(1000, 1016)):
        raise ValueError("exactly the 16 declared final training seeds required")
    diffs: dict[int, Fraction] = {}
    for seed, arms in per_seed.items():
        if set(arms) != set(PRIMARY):
            raise ValueError(f"{seed}: missing primary or EXTERNAL included")
        totals = {}
        for name, array in arms.items():
            a = np.asarray(array)
            if a.shape != (4096,) or not np.issubdtype(a.dtype, np.integer) or np.any((a < 0) | (a > 150)):
                raise ValueError(f"{seed}/{name}: invalid raw held-out losses")
            totals[name] = int(a.sum())
        diffs[seed] = Fraction(min(totals[r] for r in PRIMARY[1:]) - totals["candidate"], 150 * 4096)
    threshold = Fraction(1, 50)
    w = sum(d > threshold for d in diffs.values())
    l = sum(d < threshold for d in diffs.values())
    t = 16 - w - l
    p = sign_p(w, l)
    return {"pass": w >= 14 and p <= Fraction(1, 100), "wins": w, "losses": l,
            "ties": t, "n": w + l, "p_exact": str(p), "p_float": float(p),
            "minimum_p": str(Fraction(2, 2 ** (w + l))) if w + l else "1",
            "differences_exact": {str(s): str(v) for s, v in diffs.items()},
            "mean": float(mean(diffs.values())), "median": float(median(diffs.values())),
            "positive_fraction_ci_95": positive_fraction_ci(w)}