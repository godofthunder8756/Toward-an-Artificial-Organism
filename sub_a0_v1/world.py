from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor

from sub_a0_v1.model import DESTINATIONS, HIDDEN, State


@dataclass(frozen=True)
class Fault:
    shrink: Tensor
    drift: Tensor
    erase: Tensor
    hidden_drift: Tensor


class FaultStream:
    def __init__(self, seed: int):
        self.gen = torch.Generator().manual_seed(seed)
        self.mode = torch.tensor([1.0, 4.0, 16.0])[
            torch.randint(3, (8,), generator=self.gen)
        ]
        self.regions = torch.arange(DESTINATIONS) % 8

    def next(self) -> Fault:
        switches = torch.rand(8, generator=self.gen) < 1 / 200
        choices = torch.tensor([1.0, 4.0, 16.0])[
            torch.randint(3, (8,), generator=self.gen)
        ]
        self.mode = torch.where(switches, choices, self.mode)
        scale = self.mode[self.regions]
        erase = torch.zeros(DESTINATIONS, dtype=torch.bool)
        if torch.rand((), generator=self.gen) < 1 / 2000:
            region = torch.randint(8, (), generator=self.gen)
            erase = (self.regions == region) & (
                torch.rand(DESTINATIONS, generator=self.gen) < 0.1
            )
        return Fault(
            0.0002 * scale,
            0.002 * scale * torch.randn(DESTINATIONS, generator=self.gen),
            erase,
            0.002 * scale[:, None] * torch.randn(DESTINATIONS, HIDDEN, generator=self.gen),
        )


def damage(state: State, fault: Fault) -> State:
    values = torch.where(
        fault.erase, 0.0, state.values * (1 - fault.shrink) + fault.drift
    )
    hidden = torch.where(
        fault.erase[:, None], 0.0,
        state.hidden * (1 - fault.shrink[:, None]) + fault.hidden_drift,
    )
    return State(values, hidden)
