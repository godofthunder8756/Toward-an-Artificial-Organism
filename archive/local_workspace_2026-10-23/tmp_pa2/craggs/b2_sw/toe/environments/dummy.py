"""Deterministic dummy environment used to verify the Stage A execution pipeline."""

from __future__ import annotations

from typing import Any, Mapping

from .base import BaseEnvironment, EnvironmentOperationError, StepResult


class DummyEnvironment(BaseEnvironment):
    """A tiny deterministic environment with an auditable transition rule.

    State begins at ``initial_state`` and increments by one at every step.
    The agent action is deliberately irrelevant.  The registered dummy
    intervention adds one temporary unit and the registered rescue removes it.
    This environment tests infrastructure only; it carries no ToE claim.
    """

    def __init__(self, config: Mapping[str, Any]):
        self.environment_id = str(config["id"])
        self.version = str(config["version"])
        self.initial_state = int(config.get("initial_state", 0))
        self.transition = str(config.get("transition", "increment"))
        self.steps_per_episode = int(config.get("steps_per_episode", 1))
        if self.transition != "increment":
            raise ValueError(f"Unsupported dummy transition: {self.transition}")
        if self.steps_per_episode <= 0:
            raise ValueError("steps_per_episode must be positive")
        self._state = self.initial_state
        self._step_index = 0
        self._seed = 0
        self._active_dummy_intervention = False

    def reset(self, seed: int) -> int:
        if not isinstance(seed, int) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self._seed = seed
        self._state = self.initial_state
        self._step_index = 0
        self._active_dummy_intervention = False
        return self.observe()

    def observe(self) -> int:
        return self._state

    def step(self, action: Any) -> StepResult:
        del action  # The Stage A dummy policy has no causal role by design.
        if self._step_index >= self.steps_per_episode:
            raise RuntimeError("Episode already terminated")
        self._state += 1
        self._step_index += 1
        terminated = self._step_index >= self.steps_per_episode
        return StepResult(
            observation=self.observe(),
            outcome=self._state,
            terminated=terminated,
            info={"step_index": self._step_index, "seed": self._seed},
        )

    def snapshot(self) -> Mapping[str, Any]:
        return {
            "state": self._state,
            "step_index": self._step_index,
            "seed": self._seed,
            "active_dummy_intervention": self._active_dummy_intervention,
        }

    def intervene(self, intervention_id: str) -> Mapping[str, Any]:
        if intervention_id != "DUMMY_INTERVENTION_01":
            raise EnvironmentOperationError(f"Unknown dummy intervention {intervention_id!r}")
        if self._active_dummy_intervention:
            raise EnvironmentOperationError("Dummy intervention is already active")
        before = self._state
        self._state += 1
        self._active_dummy_intervention = True
        return {"operation": intervention_id, "before": before, "after": self._state}

    def restore(self, rescue_id: str) -> Mapping[str, Any]:
        if rescue_id != "DUMMY_RESCUE_01":
            raise EnvironmentOperationError(f"Unknown dummy rescue {rescue_id!r}")
        if not self._active_dummy_intervention:
            raise EnvironmentOperationError("Dummy rescue requested without active intervention")
        before = self._state
        self._state -= 1
        self._active_dummy_intervention = False
        return {"operation": rescue_id, "before": before, "after": self._state}
