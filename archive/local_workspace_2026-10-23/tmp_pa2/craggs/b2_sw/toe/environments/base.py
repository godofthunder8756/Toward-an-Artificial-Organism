"""Common environment contract for Paper III experiments.

The interface mirrors the minimal operations specified in Paper III:
observe, step, intervene, ablate, corrupt and restore.  Concrete environments
may decline a controlled operation explicitly; silent no-ops are prohibited.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping


class EnvironmentOperationError(RuntimeError):
    """Raised when an environment cannot perform a requested registered operation."""


@dataclass(frozen=True)
class StepResult:
    """Result returned by one environment transition."""

    observation: Any
    outcome: Any
    terminated: bool
    info: Mapping[str, Any]


class BaseEnvironment(ABC):
    """Minimal cross-block environment interface.

    The substantive state space is deliberately unconstrained.  The common
    contract standardises execution and intervention without implying that
    different experimental blocks share one ontology or metric.
    """

    environment_id: str
    version: str

    @abstractmethod
    def reset(self, seed: int) -> Any:
        """Reset the environment and return the initial observation."""

    @abstractmethod
    def observe(self) -> Any:
        """Return the observation currently exposed to the agent."""

    @abstractmethod
    def step(self, action: Any) -> StepResult:
        """Advance the environment by one transition."""

    @abstractmethod
    def snapshot(self) -> Mapping[str, Any]:
        """Return a serialisable state snapshot sufficient for Stage A logging."""


    def raw_state(self) -> Mapping[str, Any] | None:
        """Return optional primary-state arrays for archival storage.

        Stage A environments may return ``None``. Scientific environments whose
        primary state is not fully represented by scalar logs can override this hook.
        """
        return None

    def intervene(self, intervention_id: str) -> Mapping[str, Any]:
        raise EnvironmentOperationError(
            f"{self.environment_id} does not support intervention {intervention_id!r}"
        )

    def ablate(self, ablation_id: str) -> Mapping[str, Any]:
        raise EnvironmentOperationError(
            f"{self.environment_id} does not support ablation {ablation_id!r}"
        )

    def corrupt(self, corruption_id: str) -> Mapping[str, Any]:
        raise EnvironmentOperationError(
            f"{self.environment_id} does not support corruption {corruption_id!r}"
        )

    def restore(self, rescue_id: str) -> Mapping[str, Any]:
        raise EnvironmentOperationError(
            f"{self.environment_id} does not support restore/rescue {rescue_id!r}"
        )
