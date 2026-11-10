"""Recurrent actor-critic with the Track B D19 fate-noise rule.

D19: block = the recurrent core hidden state (all units); zero-mean isotropic
Gaussian noise with SD sigma_t = kappa_f * g(d_t) * s_core; applied after the
recurrent update and before every readout; the post-noise state is clipped to
the cell's activation range and is the state carried forward.
"""
from __future__ import annotations

import torch
import torch.nn as nn

from .env import N_ACT, OBS_DIM


class Agent(nn.Module):
    def __init__(self, hidden: int = 64, kappa_f: float = 1.0, s_core: float = 0.15):
        super().__init__()
        self.hidden, self.kappa_f, self.s_core = hidden, kappa_f, s_core
        self.enc = nn.Linear(OBS_DIM, hidden)
        self.core = nn.GRUCell(hidden, hidden)
        self.pi = nn.Linear(hidden, N_ACT)
        self.v = nn.Linear(hidden, 1)

    def init_state(self, n: int) -> torch.Tensor:
        return torch.zeros(n, self.hidden)

    def step(self, obs: torch.Tensor, h: torch.Tensor, gain: torch.Tensor, gen: torch.Generator):
        """One step. `gain` in [0,1] per env is g(d_t); returns logits, value, new h."""
        h = self.core(torch.relu(self.enc(obs)), h)
        if gain is not None:
            noise = torch.randn(h.shape, generator=gen) * (self.kappa_f * self.s_core)
            h = torch.clamp(h + gain[:, None] * noise, -1.0, 1.0)
        return self.pi(h), self.v(h).squeeze(-1), h
