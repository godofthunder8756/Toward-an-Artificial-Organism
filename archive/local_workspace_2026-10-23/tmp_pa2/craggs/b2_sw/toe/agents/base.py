"""Common agent contract for manifest-driven Paper III experiments."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping


class BaseAgent(ABC):
    architecture_id: str
    version: str

    @abstractmethod
    def reset(self, seed: int) -> None:
        """Reset episode-local agent state."""

    @abstractmethod
    def act(self, observation: Any) -> Any:
        """Return an action for the current observation."""

    @abstractmethod
    def snapshot(self) -> Mapping[str, Any]:
        """Return serialisable accessible internal state for logging."""
