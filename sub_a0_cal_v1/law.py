"""Parameterized SUB-A0 fault law.

Identical random-draw order to ``sub_a0_v1.world.FaultStream``. With all
multipliers equal to 1 the produced faults are bitwise identical to A0's.
Multipliers scale shrinkage, drift amplitude and the erase-event probability;
region count, hidden modes, switch rate and erase fraction are unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor

from sub_a0_v1.model import DESTINATIONS, HIDDEN

MODES = (1.0, 4.0, 16.0)
REGIONS = 8
SWITCH_PROBABILITY = 1 / 200
BASE_SHRINK = 0.0002
BASE_DRIFT = 0.002
BASE_ERASE_DENOMINATOR = 2000
ERASE_FRACTION = 0.1


@dataclass(frozen=True)
class Cell:
    shrink: int = 1
    drift: int = 1
    erase: int = 1

    def key(self) -> str:
        return f"s{self.shrink}_d{self.drift}_e{self.erase}"


@dataclass(frozen=True)
class RawFault:
    """One tick of draws shared by every cell with the same erase multiplier."""

    scale: Tensor          # per-destination hidden mode multiplier
    unit_drift: Tensor     # standard normal draws for value drift
    erase: Tensor          # bool mask of erased destinations
    entered_high: Tensor   # bool per region: switched INTO mode 16 this tick
    erase_event: bool      # evaluator-only event metadata


class ParamFaultStream:
    def __init__(self, seed: int, erase: int = 1):
        if erase < 1:
            raise ValueError("Erase multiplier must be >= 1")
        self.erase_probability = erase / BASE_ERASE_DENOMINATOR
        self.gen = torch.Generator().manual_seed(seed)
        self.mode = torch.tensor(MODES)[torch.randint(3, (REGIONS,), generator=self.gen)]
        self.regions = torch.arange(DESTINATIONS) % REGIONS

    def next(self) -> RawFault:
        switches = torch.rand(REGIONS, generator=self.gen) < SWITCH_PROBABILITY
        choices = torch.tensor(MODES)[torch.randint(3, (REGIONS,), generator=self.gen)]
        entered_high = switches & (choices == 16.0) & (self.mode != 16.0)
        self.mode = torch.where(switches, choices, self.mode)
        scale = self.mode[self.regions]
        erase = torch.zeros(DESTINATIONS, dtype=torch.bool)
        event = False
        if torch.rand((), generator=self.gen) < self.erase_probability:
            event = True
            region = torch.randint(REGIONS, (), generator=self.gen)
            erase = (self.regions == region) & (
                torch.rand(DESTINATIONS, generator=self.gen) < ERASE_FRACTION
            )
        unit_drift = torch.randn(DESTINATIONS, generator=self.gen)
        # Hidden-state drift is drawn (and discarded) so the stream stays aligned
        # with the full A0 law used by any later candidate run.
        torch.randn(DESTINATIONS, HIDDEN, generator=self.gen)
        return RawFault(scale, unit_drift, erase, entered_high, event)


def cell_terms(raw: RawFault, cells: list[Cell]) -> tuple[Tensor, Tensor]:
    """Return shrink and drift tensors of shape [len(cells), DESTINATIONS].

    Operation order matches A0 (``0.002 * scale * randn``) for multiplier 1.
    """
    shrink = torch.stack([(BASE_SHRINK * c.shrink) * raw.scale for c in cells])
    drift = torch.stack([(BASE_DRIFT * c.drift) * raw.scale * raw.unit_drift for c in cells])
    return shrink, drift


def apply(values: Tensor, shrink: Tensor, drift: Tensor, erase: Tensor) -> Tensor:
    """Damage values of shape [cells, rows, DESTINATIONS] exactly as A0 ``damage``."""
    return torch.where(erase, 0.0, values * (1 - shrink[:, None, :]) + drift[:, None, :])
