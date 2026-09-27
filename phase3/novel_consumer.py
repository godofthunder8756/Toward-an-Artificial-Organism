"""Phase-III novel-consumer test (G7): frozen-W reuse by S_conf / S_bias.

Freeze the encoder, W's acquisition write, and the three original specialists
after training; leave pi + A running; attach two read-only heads — S_conf
(calibrated posterior, the fourth invariance class) and S_bias (the shifted
asymmetric-cost decision). Both are *fixed functions of W* (their analytic
optima, G7 §2): the reuse is of the frozen content, with zero inference
retraining and zero gradient into the frozen core.

The four measures (G7 §4): sample efficiency (0 retraining samples), frozen-
core completeness (S_conf reaches the Bayes-calibrated ceiling to the
quantization floor), information required (b bits), and interference (old
specialists byte-identical across the Phase-1/Phase-2 boundary).
"""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

from phase3.config import Phase3Config
from phase3.specialists import s_bias, s_conf

__all__ = ["s_conf_log_loss", "s_bias_accuracy", "posterior_entropy_ceiling",
           "novel_consumer_scores"]


def posterior_entropy_ceiling(cfg: Phase3Config, s_h: np.ndarray, z: np.ndarray) -> float:
    """The Bayes-calibrated log loss: E[-log P*(z|x)] over the true posterior
    P*(A) = sigmoid(S_H). This is the ceiling S_conf must reach (G7 §2.1)."""
    p_a = 1.0 / (1.0 + np.exp(-np.asarray(s_h, dtype=np.float64)))
    p_z = np.where(np.asarray(z) == 0, p_a, 1.0 - p_a)
    return float(np.mean(-np.log(np.clip(p_z, 1e-9, 1.0))))


def s_conf_log_loss(w_h: np.ndarray, z: np.ndarray) -> float:
    """S_conf's log loss: E[-log sigma(W_H)] against z (the fourth-class objective)."""
    p = s_conf(np.asarray(w_h, dtype=np.float64))
    p = np.clip(p, 1e-9, 1.0)
    return float(np.mean(-np.log(np.where(np.asarray(z) == 0, p, 1.0 - p))))


def s_bias_accuracy(w_h: np.ndarray, z: np.ndarray, theta_bias: float) -> float:
    """S_bias's decision accuracy under the shifted boundary (G7 §2.2)."""
    zhat = s_bias(np.asarray(w_h, dtype=np.float64), theta_bias)
    return float(np.mean(zhat == np.asarray(z, dtype=np.int64)))


def novel_consumer_scores(cfg: Phase3Config, w: np.ndarray, z: np.ndarray,
                          thr: Dict[str, float]) -> Dict[str, float]:
    """The S_conf / S_bias scores at t = H from the frozen W trajectory.

    ``w`` is the (..., H) quantized W for the shared arms, or (..., H, 3) for
    R1/R5; the new consumer reads the shared slot (or, for R1, piggybacks on
    copy 0 — the disclosed R1-piggyback sub-arm, G7 §5). Scores are read at
    the final step H.
    """
    w = np.asarray(w, dtype=np.float64)
    if w.ndim >= 3 and w.shape[-1] == 3:
        w_h = w[..., -1, 0]                        # piggyback on copy 0
    else:
        w_h = w[..., -1]
    return {
        "s_conf_log_loss": s_conf_log_loss(w_h, z),
        "s_bias_accuracy": s_bias_accuracy(w_h, z, thr["theta_bias"]),
    }
