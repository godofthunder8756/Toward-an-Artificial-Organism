"""Deterministic Phase III-B episode generator and evaluator-only loss ledger.

Never pass ``Episode.truth`` or ``Episode.losses`` to an arm's forward method.
Randomness is per stream, not coupled to calls made by an arm.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch


PORTS = np.tile(np.arange(4, dtype=np.int64), 2)
FLIP = 0.2
LOSS_UNIT = 150


@dataclass(frozen=True)
class Episode:
    common: torch.Tensor  # (B,8), scheduled readings only
    local: torch.Tensor  # (B,4,3), independently drawn private readings
    truth: torch.Tensor  # (B,4), evaluator only


def generate(seed: int, size: int) -> Episode:
    """Independent fair factors, BSC(1/5) readings, fixed 0..3/0..3 schedule."""
    if size < 1 or seed < 0:
        raise ValueError("size must be positive and seed nonnegative")
    rng = np.random.default_rng(seed)
    truth = rng.integers(0, 2, size=(size, 4), dtype=np.int64)
    common = truth[:, PORTS] ^ (rng.random((size, 8)) < FLIP)
    local = np.empty((size, 4, 3), dtype=np.int64)
    for c in range(4):
        targets = ((c, (c + 1) % 4, (c + 2) % 4))
        local[:, c, :] = truth[:, targets] ^ (rng.random((size, 3)) < FLIP)
    return Episode(torch.from_numpy(common.astype(np.int64)),
                   torch.from_numpy(local), torch.from_numpy(truth))


def targets(truth: torch.Tensor, contexts: int) -> tuple[torch.Tensor, ...]:
    if contexts not in (3, 4) or truth.ndim != 2 or truth.shape[1] != 4:
        raise ValueError("invalid evaluator targets")
    return (torch.stack([truth[:, c] for c in range(contexts)], 1),
            torch.stack([truth[:, (c + 1) % 4] for c in range(contexts)], 1),
            torch.stack([truth[:, (c + 2) % 4] ^ truth[:, (c + 3) % 4]
                         for c in range(contexts)], 1))


def loss_units(actions: tuple[torch.Tensor, ...], truth: torch.Tensor) -> torch.Tensor:
    """(B,C,3) component losses in units of 1/150 of JOINT loss.

    S2 commitments settle at the next tick (including terminal tick 12).
    This ledger is computed after all decisions; it is never returned to a model.
    S3 feedback is likewise withheld until episode end.
    """
    contexts = actions[0].shape[1]
    if any(a.shape != (truth.shape[0], contexts) for a in actions):
        raise ValueError("action/episode shape mismatch")
    s1, s2, s3 = targets(truth, contexts)
    return torch.stack(((actions[0] != s1).long() * 50,
                        torch.where(actions[1] == 2, 9,
                                    (actions[1] != s2).long() * 50),
                        (actions[2] != s3).long() * 50), -1)


def posterior_counts(common: torch.Tensor) -> torch.Tensor:
    """Evaluator-only counter; never expose to trained-arm forward methods."""
    return common[:, :4].long() + common[:, 4:].long()