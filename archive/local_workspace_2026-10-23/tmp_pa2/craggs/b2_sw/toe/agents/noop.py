"""No-op architecture for autonomous physical-field baselines."""
from __future__ import annotations
from typing import Any, Mapping
from .base import BaseAgent

class NoOpAgent(BaseAgent):
    def __init__(self, config: Mapping[str, Any]):
        self.architecture_id = str(config["id"])
        self.version = str(config["version"])
        self._seed = 0
        self._actions = 0

    def reset(self, seed: int) -> None:
        self._seed = int(seed)
        self._actions = 0

    def act(self, observation: Any) -> None:
        del observation
        self._actions += 1
        return None

    def snapshot(self) -> Mapping[str, Any]:
        return {"seed": self._seed, "actions_taken": self._actions, "policy": "no_op"}
