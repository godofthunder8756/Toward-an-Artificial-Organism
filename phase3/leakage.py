"""Phase-III leakage audit (G8): the z-decoder instrument.

A capacity-capped readout (logistic regression) trained to predict z from a
frozen snapshot of a pathway's activations. It is a supplied measuring
instrument — never part of any arm's forward graph, never back-propagated
through arm weights, trained on a disjoint seed family from the one it is
evaluated on (G8 §2.4).

The three reference anchors (G8 §2.2): chance 0.500, memoryless 0.606 (clean),
and the W ceiling 0.812. A pathway is LEAK-grade only if its probe decode
exceeds chance by more than the finite-sample resolution epsilon (G8 §2.5).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import bridge.reproducibility as _rep

from phase3.config import Phase3Config

__all__ = ["LogisticDecoder", "decode_accuracy", "probe_decode", "binomial_se"]


def binomial_se(p: float, n: int) -> float:
    return float(np.sqrt(p * (1.0 - p) / n)) if n else 0.0


class LogisticDecoder(nn.Module):
    """Capacity-capped logistic readout (the G8 §2.1 instrument)."""

    def __init__(self, in_dim: int):
        super().__init__()
        self.fc = nn.Linear(in_dim, 1)
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc(x).squeeze(-1)


def decode_accuracy(features: np.ndarray, z: np.ndarray, in_dim: Optional[int] = None,
                    train_seed: int = 0, steps: int = 500, lr: float = 1e-2,
                    eval_frac: float = 0.5) -> Tuple[float, float]:
    """Train a logistic decoder on a held-out split and report eval accuracy.

    Returns (accuracy, epsilon) with epsilon the binomial SE at the eval size.
    The split is deterministic (first half train, second half eval); in the
    audit the train/eval families are disjoint by seed, not by split.
    """
    n = features.shape[0]
    mid = n // 2
    x_tr = features[:mid]
    z_tr = z[:mid]
    x_ev = features[mid:]
    z_ev = z[mid:]
    if in_dim is None:
        in_dim = features.shape[-1]
    dec = LogisticDecoder(in_dim)
    opt = torch.optim.Adam(dec.parameters(), lr=lr)
    x_tr_t = torch.from_numpy(np.asarray(x_tr, dtype=np.float32))
    z_tr_t = torch.from_numpy(np.asarray(z_tr, dtype=np.float32))
    for _ in range(steps):
        opt.zero_grad()
        loss = F.binary_cross_entropy_with_logits(dec(x_tr_t), z_tr_t)
        loss.backward()
        opt.step()
    with torch.no_grad():
        logits = dec(torch.from_numpy(np.asarray(x_ev, dtype=np.float32)))
        pred = (logits > 0).float()
        acc = float((pred == torch.from_numpy(np.asarray(z_ev, dtype=np.float32))).float().mean())
    return acc, binomial_se(acc, len(z_ev))


def probe_decode(features: np.ndarray, z: np.ndarray, probe_entry: int) -> Tuple[np.ndarray, np.ndarray]:
    """Slice a trajectory's features and labels to the probe window (H-K..H)."""
    f = np.asarray(features)
    probe = f[:, probe_entry:, :] if f.ndim == 3 else f[:, probe_entry:]
    return probe.reshape(probe.shape[0], -1), np.asarray(z)
