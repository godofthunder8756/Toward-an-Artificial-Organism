"""Exact statistics for the N11 final experiment (stdlib + numpy only).

Implements the frozen statistical plan (``TBRIDGE_STATISTICAL_PLAN_v1.md`` §4-§6):

- exact sign-flip test on paired per-seed differences (ties excluded, N_eff
  reported; p-value support is a discrete subset of {2/2^n, ...}, never 0);
- exact binomial (Clopper-Pearson) 95% CI, computed by numerically inverting
  the exact binomial CDF (no scipy dependency);
- the effect-size reporting quantities (mean/median paired difference, fraction
  of seeds positive with exact binomial CI).
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

__all__ = [
    "sign_flip_test",
    "binomial_ci",
    "paired_effect",
]


def _binom_pmf(k: int, n: int, p: float) -> float:
    return math.comb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))


def _binom_cdf(k: int, n: int, p: float) -> float:
    return sum(_binom_pmf(i, n, p) for i in range(0, k + 1))


def binomial_ci(k: int, n: int, alpha: float = 0.05) -> Tuple[float, float]:
    """Exact Clopper-Pearson 95% CI for k successes in n trials.

    Computed by bisecting the exact binomial CDF; equals the Clopper-Pearson
    interval to numerical tolerance without needing the incomplete beta.
    ``k`` is the number of successes (a float count is accepted and rounded to
    the nearest whole number for the binomial; callers pass integer counts).
    """
    if n == 0:
        return (0.0, 1.0)
    k = int(round(k))
    k = max(0, min(n, k))

    # Lower bound: p where P(X >= k | p) = alpha/2 (increasing in p). k==0 -> 0.
    if k == 0:
        lower = 0.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            p_ge_k = 1.0 - _binom_cdf(k - 1, n, mid)
            if p_ge_k > alpha / 2:
                hi = mid   # p too large -> shrink
            else:
                lo = mid
        lower = (lo + hi) / 2

    # Upper bound: p where P(X <= k | p) = alpha/2 (decreasing in p). k==n -> 1.
    if k == n:
        upper = 1.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            p_le_k = _binom_cdf(k, n, mid)
            if p_le_k < alpha / 2:
                hi = mid   # p too large (P(X<=k) shrinks as p grows) -> shrink
            else:
                lo = mid
        upper = (lo + hi) / 2
    return (lower, upper)


def sign_flip_test(differences: Sequence[float]) -> Dict[str, object]:
    """Exact paired sign-flip test (ties excluded).

    Returns observed mean, n (non-tie), N_eff, the exact two-sided p over all
    2^n sign assignments, and the null mean's sd. ``differences`` are the paired
    per-seed (arm_a - arm_b) values; zero ties are dropped and reported.
    """
    d = [float(x) for x in differences]
    ties = sum(1 for x in d if x == 0.0)
    d = [x for x in d if x != 0.0]
    n = len(d)
    if n == 0:
        return {"observed": 0.0, "n_ties": ties, "N_eff": 0, "p": 1.0,
                "null_sd": 0.0, "diffs": differences}
    observed = sum(d)
    count = 0
    total = 0
    means = []
    for mask in range(1 << n):
        total += 1
        s = 0.0
        for i in range(n):
            s += d[i] if (mask >> i) & 1 else -d[i]
        means.append(s / n)
        if abs(s) >= abs(observed) - 1e-9:
            count += 1
    p = count / total
    mu = sum(means) / len(means)
    var = sum((m - mu) ** 2 for m in means) / len(means)
    return {
        "observed_mean": observed / n,
        "observed_sum": observed,
        "n_ties": ties,
        "N_eff": n,
        "p": p,
        "null_sd": math.sqrt(var),
        "diffs": [float(x) for x in differences],
    }


def paired_effect(a: Sequence[float], b: Sequence[float]) -> Dict[str, object]:
    """Paired effect-size summary: per-seed differences (a - b) and the
    fraction of seeds positive, with exact binomial CI."""
    diffs = [float(x) - float(y) for x, y in zip(a, b)]
    n = len(diffs)
    n_pos = sum(1 for d in diffs if d > 0)
    n_neg = sum(1 for d in diffs if d < 0)
    n_tie = n - n_pos - n_neg
    frac_pos = n_pos / n if n else 0.0
    lo, hi = binomial_ci(n_pos, n)
    mean = sum(diffs) / n if n else 0.0
    sorted_d = sorted(diffs)
    median = sorted_d[n // 2] if n else 0.0
    return {
        "diffs": diffs,
        "mean_diff": mean,
        "median_diff": median,
        "n": n,
        "n_positive": n_pos,
        "n_negative": n_neg,
        "n_tie": n_tie,
        "fraction_positive": frac_pos,
        "ci_95": [lo, hi],
    }
