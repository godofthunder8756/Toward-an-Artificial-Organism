"""Live-trace diagnostic exposing the ordinary-code and supplied-rule boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]
BANKS = ("skill", "replay", "repair")


@dataclass(frozen=True)
class Damage:
    shrinkage: Array
    drift: Array
    erase: NDArray[np.bool_]

    def validate(self, shape: tuple[int, ...]) -> None:
        if any(value.shape != shape for value in
               (self.shrinkage, self.drift, self.erase)):
            raise ValueError("Damage must cover the complete bank shape")
        if not np.isfinite(self.shrinkage).all() or not np.isfinite(self.drift).all():
            raise ValueError("Damage coefficients must be finite")
        if np.any(self.shrinkage < 0) or np.any(self.shrinkage > 1):
            raise ValueError("Shrinkage must be in [0, 1]")
        if self.erase.dtype != np.bool_:
            raise ValueError("Erasure mask must be boolean")


class Arm(Enum):
    SELF = "self_every_tick"
    EXTERNAL = "external_every_tick"
    CODE = "ordinary_consensus_code"
    YOKED = "yoked_actions"
    FIXED_THRESHOLD = "fixed_disagreement_threshold"
    IMMORTAL = "immortal_reference"
    NO_REPAIR = "no_repair"


@dataclass(frozen=True)
class Step:
    tick: int
    repair_requested: bool
    repair_applied: bool
    stored_scalars: int


class Substrate:
    """All retained coefficient banks are live; consensus arithmetic is supplied.

    No initial weights, labels, optimizer or target logits are retained here.
    Diagnostic callers may hold independent fixtures, but repair cannot read them.
    This is not a security isolation boundary or a production-closure claim.
    """

    def __init__(self, skill: Array, replay: Array, repair: Array):
        skill = np.asarray(skill, dtype=np.float64)
        replay = np.asarray(replay, dtype=np.float64)
        repair = np.asarray(repair, dtype=np.float64)
        if skill.ndim != 2 or skill.shape[0] != 3 or skill.shape[1] == 0:
            raise ValueError("Skill must have three replicas and at least one cue")
        if replay.shape != skill.shape or repair.shape != (3, 1):
            raise ValueError("Replay must match skill; repair must have shape (3, 1)")
        if not all(np.isfinite(bank).all() for bank in (skill, replay, repair)):
            raise ValueError("Live coefficients must be finite")
        self.banks: dict[str, Array] = {
            "skill": skill.copy(), "replay": replay.copy(), "repair": repair.copy()
        }
        self.tick = 0

    @property
    def stored_scalars(self) -> int:
        return sum(bank.size for bank in self.banks.values())

    def predict(self, cue: int) -> int:
        if isinstance(cue, bool) or not isinstance(cue, (int, np.integer)):
            raise ValueError("Cue must be an integer")
        if not 0 <= cue < self.banks["skill"].shape[1]:
            raise ValueError("Cue is out of range")
        return int(np.median(self.banks["skill"][:, cue]) > 0)

    def disagreement(self) -> float:
        return float(np.max(np.ptp(self.banks["skill"], axis=0)))

    def damage(self, events: Mapping[str, Damage]) -> None:
        if set(events) != set(BANKS):
            raise ValueError("Every persistent bank must receive a damage event")
        for name in BANKS:
            events[name].validate(self.banks[name].shape)
        updated = {
            name: np.where(events[name].erase, 0.0,
                           (1.0 - events[name].shrinkage) * self.banks[name]
                           + events[name].drift)
            for name in BANKS
        }
        if not all(np.isfinite(bank).all() for bank in updated.values()):
            raise ValueError("Damage produced nonfinite live coefficients")
        self.banks = updated

    def consolidate(self) -> bool:
        gain = float(np.clip(np.median(self.banks["repair"]), 0.0, 1.0))
        if gain == 0:
            return False
        cues = np.median(self.banks["replay"], axis=0) > 0
        for name in ("skill", "replay"):
            bank = self.banks[name]
            target = np.median(bank, axis=0)
            bank[:, cues] += gain * (target[cues] - bank[:, cues])
        bank = self.banks["repair"]
        bank += gain * (np.median(bank, axis=0) - bank)
        return True

    def step(
        self,
        events: Mapping[str, Damage],
        arm: Arm,
        *,
        yoked_action: bool | None = None,
        threshold: float = 0.1,
    ) -> Step:
        if not isinstance(arm, Arm):
            raise ValueError("Unknown arm")
        if not np.isfinite(threshold) or threshold < 0:
            raise ValueError("Threshold must be finite and nonnegative")
        if arm is Arm.YOKED:
            if not isinstance(yoked_action, bool):
                raise ValueError("Yoked arm requires an explicit boolean donor action")
        elif yoked_action is not None:
            raise ValueError("Only the yoked arm may receive a donor action")
        if set(events) != set(BANKS):
            raise ValueError("Every persistent bank must receive a damage event")
        for name in BANKS:
            events[name].validate(self.banks[name].shape)
        if arm is not Arm.IMMORTAL:
            self.damage(events)
        requested = (
            yoked_action if arm is Arm.YOKED
            else self.disagreement() > threshold if arm is Arm.FIXED_THRESHOLD
            else arm is not Arm.NO_REPAIR
        )
        applied = self.consolidate() if requested else False
        self.tick += 1
        return Step(self.tick, bool(requested), applied, self.stored_scalars)
