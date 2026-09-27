"""Substrate law for the bridge economy (v3 §3, §6.3): energy, decay, refresh.

Not a neural module — no parameters and no gradient path (N4 §7.3: "energy /
decay: substrate law"). This is the content-blind bookkeeping every arm
receives: energy ``E_t`` (earned by correctly processing the distractor
stream, spent on ``E_proc`` + ``E_pi``, capped by ``B_t``, death at ``E_t <=
death_floor``) and decay age ``d_t`` (time since the cue slot was last
refreshed). All quantities are exposed as explicit tensors so train/test code
can inspect the economy directly.

CPU-only; no CUDA reference.
"""

from __future__ import annotations

from typing import Optional

import torch

from bridge.config import DecayConfig, EnergyConfig

__all__ = ["Substrate"]


class Substrate:
    """Resource economy + decay bookkeeping for one batch of episodes.

    Holds the running ``energy`` (B,), ``age`` (B,) and ``alive`` (B,) state
    for a batch and applies the substrate laws. The cue slot itself lives in
    :class:`bridge.modules.Workspace`; this class owns its age and the energy
    ledger.
    """

    def __init__(self, energy: EnergyConfig, decay: DecayConfig):
        self.energy_cfg = energy
        self.decay_cfg = decay
        self.energy: Optional[torch.Tensor] = None
        self.age: Optional[torch.Tensor] = None
        self.alive: Optional[torch.Tensor] = None

    # -- lifecycle ---------------------------------------------------------- #

    def reset(self, batch_size: int, device: Optional[torch.device] = None) -> None:
        self.energy = torch.full(
            (batch_size,), self.energy_cfg.e0, device=device, dtype=torch.float32
        )
        self.age = torch.zeros(batch_size, device=device, dtype=torch.long)
        self.alive = torch.ones(batch_size, device=device, dtype=torch.bool)

    # -- economy ------------------------------------------------------------ #

    def earn(self, correct: torch.Tensor) -> torch.Tensor:
        """Add ``E_earn`` per correctly processed distractor tick. Returns gain."""
        gain = correct.float() * self.energy_cfg.e_earn
        self.energy = self.energy + gain
        return gain

    def spend(self, action: torch.Tensor) -> torch.Tensor:
        """Spend ``E_proc`` (always) + ``E_pi`` (where refreshed).

        The budget cap ``B_t`` is enforced here: refreshed ticks may not spend
        more than ``budget_b`` total, so a refresh is clamped off when
        ``E_pi + E_proc > B_t`` (or when ``energy < E_pi``). Returns total spend.
        """
        e_proc = self.energy_cfg.e_proc
        e_pi = self.energy_cfg.e_pi
        budget = self.energy_cfg.budget_b

        can_afford = self.energy >= e_pi
        within_budget = (e_pi + e_proc) <= budget
        refresh = (action > 0.5) & can_afford & within_budget

        spend = torch.full_like(self.energy, e_proc) + refresh.float() * e_pi
        self.energy = self.energy - spend
        self.alive = self.alive & (self.energy > self.energy_cfg.death_floor)
        return spend

    def apply_refresh(self, action: torch.Tensor) -> torch.Tensor:
        """Apply the refresh action to the decay age (0 where refreshed).

        Returns the new age (B,).
        """
        self.age = torch.where(
            action > 0.5, torch.zeros_like(self.age), self.age
        )
        return self.age

    def tick_age(self) -> torch.Tensor:
        """Increment decay age for surviving episodes. Returns new age."""
        self.age = self.age + self.alive.long()
        return self.age

    # -- decay law ---------------------------------------------------------- #

    def decay_slot(self, slot: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        """Deterministic countdown decay (v3 §3, N6 §3.2).

        The slot readout is neutral ("no cue") once the decay age reaches
        ``lifetime`` since the last refresh; a paid refresh resets the age and
        thereby restores the readout. The stored value is preserved (it is the
        register); only the readout gates. Returns the readout, detached — this
        is a substrate law, no gradient flows through it.

        ``action`` is accepted for signature compatibility with the refresh
        primitive; the readout is a pure function of the (post-refresh) age,
        since ``apply_refresh`` has already reset it where the action fired.
        """
        intact = self.age < self.decay_cfg.lifetime
        out = slot.detach().clone()
        out[~intact] = 0.0
        return out
