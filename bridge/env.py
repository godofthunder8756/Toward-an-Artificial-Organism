"""Bridge environment: the c-independent distractor stream, the one-shot cue,
the announced regime, and the exogenous metabolic-correctness stream.

Every arm in the study must see the *same* underlying environment and, where
appropriate, the *same saved episodes* (v3 §4, N2 §5.3). This module owns the
generation of an episode batch and its round-trip through the ``episodes``
JSONL format, so an evaluation batch can be drawn once, saved, and replayed
identically by every arm.

The environment is fully c-independent outside the one-shot cue: the cue
identity is delivered only at t=0 (as the acquisition write), the distractor
``x_t`` is i.i.d. and independent of ``c`` (N3 §1.3), and the regime ``s`` is
announced at a fixed tick ``announce_m`` (before which the one-hot is the zero
vector, "unannounced"). The metabolic ``correct`` stream is exogenous (the
bridge does not model the metabolic task; it only earns energy from it).

Cue convention: the cue takes values in ``{+1, -1}`` so that the decayed /
neutral slot state (``0.0``, see :mod:`bridge.substrate`) is distinct from
every cue value. The probe readout's two answer classes are indexed ``0``/``1``
for ``+1``/``-1``.

CPU-only; no CUDA reference. All generation goes through the global RNG, which
``seed_all`` pins (see :mod:`bridge.reproducibility`).
"""

from __future__ import annotations

from typing import Dict, List

import torch

from bridge.config import BridgeConfig

__all__ = ["BridgeEnv", "REGIME_STABLE", "REGIME_VOLATILE"]

# Regime class indices (one-hot column order matches ArchConfig.regime_dim).
REGIME_STABLE = 0
REGIME_VOLATILE = 1

_CUE_VALUES = torch.tensor([1.0, -1.0])  # +1 -> class 0, -1 -> class 1


def _one_hot_regime(regime: torch.Tensor, m: int, T: int) -> torch.Tensor:
    """One-hot regime (B, T, 2), zeroed before the announce tick ``m``.

    ``regime`` is (B,) in {0, 1} (stable / volatile); the announcement at tick
    ``m`` means ticks ``t < m`` carry the zero vector ("unannounced").
    """
    B = regime.shape[0]
    one_hot = torch.nn.functional.one_hot(regime, num_classes=2).float()  # (B, 2)
    vec = one_hot.unsqueeze(1).repeat(1, T, 1)  # (B, T, 2)
    announce = torch.arange(T, device=regime.device).unsqueeze(0) >= m
    vec = vec * announce.unsqueeze(-1)
    return vec


class BridgeEnv:
    """Generates and (de)serializes episode batches for the bridge.

    A batch is the tuple ``(x, cue, regime, correct)`` consumed by
    :meth:`bridge.agent.NeuralBridge.forward`, plus the per-episode regime
    class (``regime_class``, for the probe's stable-only reward) and the
    per-tick announced one-hot (``regime_vec``). ``to_records`` /
    ``from_records`` round-trip through the ``episodes`` JSONL format so
    evaluation batches can be saved once and replayed identically by every arm.
    """

    def __init__(self, config: BridgeConfig):
        self.config = config
        self.horizon = config.episode.horizon_t
        self.distractor_dim = config.arch.distractor_dim
        self.w_bits = config.arch.w_bits
        self.regime_dim = config.arch.regime_dim
        self.announce_m = config.decay.announce_m
        self.p_correct = 0.9  # exogenous metabolic correctness (documented default)

    # -- generation --------------------------------------------------------- #

    def sample(self, batch_size: int, *, p_stable: float = 0.5) -> Dict[str, torch.Tensor]:
        """Draw a deterministic (seeded) batch of episodes.

        ``p_stable`` is the fraction of episodes in the stable regime; the
        remainder are volatile. Drawn from the global RNG (pinned by
        ``seed_all``).
        """
        B, T = batch_size, self.horizon
        x = torch.randn(B, T, self.distractor_dim)

        # Cue in {+1, -1} (1 bit); neutral/decayed slot state is 0.0.
        idx = torch.randint(0, 2, (B, self.w_bits))
        cue = _CUE_VALUES[idx]  # (B, w_bits)

        regime = torch.rand(B) < p_stable  # (B,) bool -> True = stable
        regime_class = (~regime).long()  # 0 = stable, 1 = volatile
        regime_vec = _one_hot_regime(regime_class, self.announce_m, T)

        correct = torch.rand(B, T) < self.p_correct  # (B, T) bool

        return {
            "x": x,
            "cue": cue,
            "regime": regime_vec,
            "regime_class": regime_class,
            "correct": correct,
        }

    # -- (de)serialization (reuse the same episodes across arms) ------------ #

    def to_records(self, batch: Dict[str, torch.Tensor]) -> List[List[Dict]]:
        """Flatten a batch into a list of per-episode record dicts (for JSONL)."""
        B = batch["x"].shape[0]
        records: List[List[Dict]] = []
        for b in range(B):
            records.append(
                [
                    {
                        "cue": batch["cue"][b].tolist(),
                        "regime_class": int(batch["regime_class"][b]),
                        "x": batch["x"][b].tolist(),
                        "regime_vec": batch["regime"][b].tolist(),
                        "correct": [int(c) for c in batch["correct"][b].tolist()],
                    }
                ]
            )
        return records

    @classmethod
    def from_records(
        cls, episodes: List[List[Dict]]
    ) -> Dict[str, torch.Tensor]:
        """Reconstruct a batch from saved episode records (the exact inverse of
        :meth:`to_records`)."""
        B = len(episodes)
        rec = episodes[0][0]
        T = len(rec["x"])
        distractor_dim = len(rec["x"][0])

        x = torch.zeros(B, T, distractor_dim)
        cue = torch.zeros(B, len(rec["cue"]))
        regime_class = torch.zeros(B, dtype=torch.long)
        regime = torch.zeros(B, T, 2)
        correct = torch.zeros(B, T, dtype=torch.bool)

        for b, episode in enumerate(episodes):
            r = episode[0]
            x[b] = torch.tensor(r["x"])
            cue[b] = torch.tensor(r["cue"])
            regime_class[b] = int(r["regime_class"])
            regime[b] = torch.tensor(r["regime_vec"])
            correct[b] = torch.tensor(r["correct"], dtype=torch.bool)

        return {
            "x": x,
            "cue": cue,
            "regime": regime,
            "regime_class": regime_class,
            "correct": correct,
        }

