"""Phase-III specialists (G3): three fixed functions of the shared W.

The three consumers and their invariance classes (G3 §4):

- S_pol  (W, x_t)       -> zhat in {A, B}: odd (sign-equivariant), zhat = A iff W > 0.
- S_plan (W, cost)      -> {commit-A, commit-B, postpone}: sign-and-magnitude,
                           commit-A iff W >= +a, commit-B iff W <= -b, else postpone.
- S_reg  (W, E, d, s)   -> {preserve, release}: even (sign-invariant),
                           preserve iff |W| >= theta(E, d, s).

The two novel consumers (G7 §2) reuse the same W after the core is frozen:

- S_conf (W)            -> Phat = sigmoid(W): strict monotone (fourth class).
- S_bias (W)            -> zhat = A iff W > theta_bias: odd about a shifted boundary.

Every specialist is a *fixed function form* (zero parameters) — the analytic
optimum kept as a co-equal rival (G3 §6 gate 3). Only the encoder producing W
is learned. The S_plan SPRT boundaries (a, b) are derived from the cost model
before training (``sprt_boundaries``); S_reg's theta is reactive on (E, d, s)
and bounded above by ``a`` (the G6 §2.3 ordering theta <= a).

All functions accept numpy scalars/arrays; ties use the frozen convention
W <= 0 -> B (G5 §3 rule 4).
"""

from __future__ import annotations

from typing import Tuple

import numpy as np

from phase3.config import P_X_GIVEN_A, P_X_GIVEN_B, TOKEN_LAMBDA, SpecialistConfig, WConfig
from phase3.task import Quantizer

__all__ = [
    "s_pol",
    "s_plan",
    "s_reg",
    "s_conf",
    "s_bias",
    "theta_value",
    "sprt_boundaries",
    "specialist_triple",
]

A, B = 0, 1
COMMIT_A, COMMIT_B, POSTPONE = 0, 1, 2
PRESERVE, RELEASE = 0, 1

# The six on-curve triples of the shared-content manifold (G6 §2.1), in the
# (S_pol, S_plan, S_reg) encoding above, and the two contradiction classes.
MANIFOLD_TRIPLES = {(0, 0, 0), (0, 2, 0), (0, 2, 1), (1, 2, 1), (1, 2, 0), (1, 1, 0)}
SIGN_CONTRADICTIONS = {(0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1)}
MAGNITUDE_CONTRADICTIONS = {(0, 0, 1), (1, 1, 1)}


def s_pol(w: np.ndarray) -> np.ndarray:
    """S_pol: zhat = A iff W > 0 (tie W <= 0 -> B)."""
    return np.where(np.asarray(w) > 0.0, A, B)


def s_plan(w: np.ndarray, a: float, b: float) -> np.ndarray:
    """S_plan: two-sided SPRT threshold (symmetric default a = b)."""
    w = np.asarray(w, dtype=np.float64)
    out = np.full(w.shape, POSTPONE, dtype=np.int64)
    out[w >= a] = COMMIT_A
    out[w <= -b] = COMMIT_B
    return out


def theta_value(cfg: SpecialistConfig, e: np.ndarray, s: np.ndarray, a: float,
                e_crit: float) -> np.ndarray:
    """S_reg threshold theta(E, d, s), reactive and clamped to [theta_lo, a].

    Rises as energy E falls (scarcer budget -> require more confidence before
    paying) and falls in the probe (s == probe, where W is the only carrier).
    Never exceeds the SPRT boundary ``a`` (G6 §2.3 ordering theta <= a).
    ``d`` enters only through the caller's bookkeeping; the default reactive
    form depends on (E, s) directly.
    """
    e = np.asarray(e, dtype=np.float64)
    s = np.asarray(s, dtype=np.int64)
    probe = (s == 1).astype(np.float64)
    theta = (
        cfg.theta_base
        - cfg.theta_probe * probe
        + cfg.theta_energy * np.maximum(0.0, e_crit - e)
    )
    return np.clip(theta, cfg.theta_lo, a)


def s_reg(w: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """S_reg: preserve iff |W| >= theta (even / sign-invariant)."""
    w = np.asarray(w, dtype=np.float64)
    return np.where(np.abs(w) >= np.asarray(theta, dtype=np.float64), PRESERVE, RELEASE)


def s_conf(w: np.ndarray) -> np.ndarray:
    """S_conf: calibrated posterior Phat = sigmoid(W)."""
    return 1.0 / (1.0 + np.exp(-np.asarray(w, dtype=np.float64)))


def s_bias(w: np.ndarray, theta_bias: float) -> np.ndarray:
    """S_bias: zhat = A iff W > theta_bias (asymmetric-cost shifted boundary)."""
    return np.where(np.asarray(w, dtype=np.float64) > theta_bias, A, B)


def specialist_triple(w: np.ndarray, cfg: SpecialistConfig, a: float, b: float,
                      theta: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The (S_pol, S_plan, S_reg) triple for a scalar (or array of) W."""
    return s_pol(w), s_plan(w, a, b), s_reg(w, theta)


def sprt_boundaries(cfg: SpecialistConfig, bits: int, lo: float, hi: float,
                    horizon: int) -> Tuple[float, float]:
    """Derive the finite-horizon SPRT boundaries (a, b) from the cost model.

    Value iteration over the b-bit quantized W lattice. The belief evolves by
    Bayes: S_{t+1} = S_t + lambda(x) with predictive token distribution
    P(x | w) = P(x|A) sigma(w) + P(x|B) (1 - sigma(w)). At each state the
    decision is argmax over {commit-A, commit-B, postpone}; commit-A pays
    r_correct*P(A) - r_wrong*P(B), commit-B the mirror, postpone pays -c_obs
    plus the expected continuation value. ``a`` (``b``) is the smallest
    non-negative (non-positive) lattice value where commit-A (commit-B) is
    optimal at the first step; symmetric costs give a == b.

    This is the "derive before training" discipline of G2 §2 / G3 §2.2.
    """
    q = Quantizer(WConfig(bits=bits, lo=lo, hi=hi))
    levels = q.levels.astype(np.float64)   # (n_levels,)
    n = q.n_levels
    lam = np.asarray(TOKEN_LAMBDA, dtype=np.float64)
    p_a = np.asarray(P_X_GIVEN_A, dtype=np.float64)
    p_b = np.asarray(P_X_GIVEN_B, dtype=np.float64)
    step = (hi - lo) / (n - 1)

    # Value function V[w, r]: belief at lattice level w with r steps remaining.
    V = np.zeros((n, horizon + 1), dtype=np.float64)
    for r in range(1, horizon + 1):
        for w in range(n):
            s = levels[w]
            pa = 1.0 / (1.0 + np.exp(-s))
            pb = 1.0 - pa
            commit_a = cfg.r_correct * pa - cfg.r_wrong * pb
            commit_b = cfg.r_correct * pb - cfg.r_wrong * pa
            px = p_a * pa + p_b * pb            # predictive token distribution
            cont = 0.0
            for tok in range(len(lam)):
                s_next = s + lam[tok]
                w_next = int(np.clip(np.rint((s_next - lo) / step), 0, n - 1))
                cont += px[tok] * V[w_next, r - 1]
            postpone = -cfg.c_obs + cont
            V[w, r] = max(commit_a, commit_b, postpone, cfg.abstain_payoff)

    r0 = horizon
    a = float("inf")
    b = float("inf")
    for w in range(n):
        s = levels[w]
        pa = 1.0 / (1.0 + np.exp(-s))
        pb = 1.0 - pa
        commit_a = cfg.r_correct * pa - cfg.r_wrong * pb
        commit_b = cfg.r_correct * pb - cfg.r_wrong * pa
        px = p_a * pa + p_b * pb
        cont = 0.0
        for tok in range(len(lam)):
            s_next = s + lam[tok]
            w_next = int(np.clip(np.rint((s_next - lo) / step), 0, n - 1))
            cont += px[tok] * V[w_next, r0 - 1]
        postpone = -cfg.c_obs + cont
        best = max(commit_a, commit_b, postpone, cfg.abstain_payoff)
        if s >= 0.0 and best == commit_a and s < a:
            a = float(s)
        if s <= 0.0 and best == commit_b and -s < b:
            b = -float(s)
    if a == float("inf"):
        a = float(levels[-1])
    if b == float("inf"):
        b = float(levels[-1])
    return a, b
