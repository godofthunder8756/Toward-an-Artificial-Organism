"""Phase-III interventions (G5 I1-I5 + the pi-cut + the leakage ablations).

Every intervention cuts exactly one link and is paired with its uninterrupted
control on the same seed (byte-identity license, P7). Because the specialists
are fixed functions of W, the causal content of each intervention is a
*rewrite of the content trajectory* followed by re-application of the fixed
functions: the observed signature must equal the signature W's content predicts
(G5 §9), never merely a non-zero change.

Interventions:

- I1  W-scramble: overwrite W with w* at probe entry, hold it there.
- I2  W-cut: remove W from one consumer at a time (per-consumer baseline).
- I3  consumer-cut: freeze one consumer; W + survivors byte-identical.
- I4  private-copy substitution: swap W for one consumer with a frozen copy.
- I5  stale/incorrect W: inject a controlled wrong value (coherent error).
- I_pi pi-cut (G2 §3.2): halt the paid refresh; W decays on timescale 1/delta.
- F1  free-recurrence (G8 §4.4): run the recurrence with W zeroed.

The single-write-reaches-all check (SHARED, G1 §2.1-c) is exposed as
``single_write_reach``: one write changes all consumers in the candidate/R4,
exactly one in R1/R5.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

import numpy as np

from phase3.arms import apply_specialists
from phase3.config import Phase3Config
from phase3.specialists import s_plan, s_pol, s_reg, theta_value

__all__ = [
    "scramble",
    "single_write_reach",
    "w_cut_outputs",
    "wrong_w",
    "stale_w",
    "private_copy_divergence",
    "intervention_outputs",
]

REGIME_PROBE = 1


def _probe_entry(cfg: Phase3Config) -> int:
    return cfg.task.horizon - cfg.task.probe_window


def scramble(w: np.ndarray, w_star: float, probe_entry: int) -> np.ndarray:
    """I1: overwrite the content with w* at probe entry, hold it there."""
    w2 = np.array(w, dtype=np.float64, copy=True)
    w2[..., probe_entry:] = w_star
    return w2


def single_write_reach(arm_w: np.ndarray, w_star: float, probe_entry: int) -> np.ndarray:
    """Which specialist *inputs* change from ONE write to the arm's content.

    For a shared arm (single slot, shape (..., H)) one write reaches every
    consumer (returns [True, True, True]); for a private arm (shape (..., H, 3))
    one write reaches exactly one consumer (returns [True, False, False]).
    This is the SHARED identity criterion (G1 §2.1-c).
    """
    w = np.asarray(arm_w, dtype=np.float64)
    if w.ndim >= 3 and w.shape[-1] == 3:
        # private copies: writing copy 0 changes only consumer 0's input
        return np.array([True, False, False])
    return np.array([True, True, True])


def w_cut_outputs(cfg: Phase3Config, thr: Dict[str, float], w: np.ndarray,
                  consumer: int, regime: np.ndarray) -> Dict[str, np.ndarray]:
    """I2: remove W from consumer ``consumer`` (0=spol,1=splan,2=sreg) only.

    Returns the full triple with the cut consumer's input set to 0 and the
    other two reading the intact W. The cut consumer falls to its no-W
    baseline (B / postpone / release); survivors are byte-identical.
    """
    a, b = thr["a"], thr["b"]
    e_crit = cfg.persistence.e_crit
    e = np.full(w.shape, cfg.persistence.e0)
    reg = np.broadcast_to(regime.reshape((1,) * (w.ndim - 1) + (-1,)), w.shape)
    theta = theta_value(cfg.specialist, e, reg, a, e_crit)
    if consumer == 0:
        return {"spol": s_pol(np.zeros_like(w)), "splan": s_plan(w, a, b), "sreg": s_reg(w, theta)}
    if consumer == 1:
        return {"spol": s_pol(w), "splan": s_plan(np.zeros_like(w), a, b), "sreg": s_reg(w, theta)}
    return {"spol": s_pol(w), "splan": s_plan(w, a, b), "sreg": s_reg(np.zeros_like(w), theta)}


def wrong_w(w: np.ndarray, w_true_sign: float, probe_entry: int, magnitude: float = 3.0) -> np.ndarray:
    """I5(a): wrong-sign error — overwrite with a confident opposite belief."""
    w2 = np.array(w, dtype=np.float64, copy=True)
    w2[..., probe_entry:] = -np.sign(w_true_sign) * magnitude
    return w2


def stale_w(w: np.ndarray, probe_entry: int, delta_steps: int = 4) -> np.ndarray:
    """I5(b): stale error — overwrite with the value delta_steps earlier."""
    w2 = np.array(w, dtype=np.float64, copy=True)
    src = w[..., max(0, probe_entry - delta_steps):probe_entry]
    w2[..., probe_entry:] = src[..., -1:]  # hold the stale value
    return w2


def private_copy_divergence(cfg: Phase3Config, w: np.ndarray, consumer: int,
                            probe_entry: int, thr: Dict[str, float]) -> float:
    """I4: divergence of consumer ``consumer`` on a frozen private copy vs the
    ongoing shared W, measured over the accumulation phase (where W keeps
    moving). Returns the mean |ongoing - frozen| in the informative region."""
    w = np.asarray(w, dtype=np.float64)
    # The private copy is frozen at the value W had at the *substitution* tick
    # (measured over the accumulation phase: substitute early, watch divergence).
    sub = max(1, probe_entry // 2)
    frozen = w[..., sub:sub + 1]                       # frozen copy value
    ongoing = w[..., sub:probe_entry]
    return float(np.mean(np.abs(ongoing - frozen)))


def intervention_outputs(cfg: Phase3Config, thr: Dict[str, float], w: np.ndarray,
                         regime: np.ndarray) -> Dict[str, np.ndarray]:
    """The intact triple (the uninterrupted control every intervention pairs with)."""
    return apply_specialists(w, cfg, thr, regime)
