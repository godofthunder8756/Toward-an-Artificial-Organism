"""Non-trainable constant-action Stage A dummy agent."""

from __future__ import annotations

from typing import Any, Mapping

from .base import BaseAgent


class DummyAgent(BaseAgent):
    def __init__(self, config: Mapping[str, Any]):
        self.architecture_id = str(config["id"])
        self.version = str(config["version"])
        self.policy = str(config.get("policy", "constant_zero"))
        self.trainable = bool(config.get("trainable", False))
        if self.policy != "constant_zero":
            raise ValueError(f"Unsupported dummy policy: {self.policy}")
        if self.trainable:
            raise ValueError("Stage A DummyAgent must be non-trainable")
        self._seed = 0
        self._actions_taken = 0

    def reset(self, seed: int) -> None:
        if not isinstance(seed, int) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self._seed = seed
        self._actions_taken = 0

    def act(self, observation: Any) -> int:
        del observation
        self._actions_taken += 1
        return 0

    def snapshot(self) -> Mapping[str, Any]:
        return {
            "seed": self._seed,
            "actions_taken": self._actions_taken,
            "policy": self.policy,
        }
