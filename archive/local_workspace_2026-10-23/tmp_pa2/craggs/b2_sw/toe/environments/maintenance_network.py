"""Small causal-maintenance environment for Paper III Block I / B2.

The environment implements the discrete-time component dynamics in Paper III:
q_i(t+1) = clip(q_i - d_i - xi_i + m_int_i + m_ext_i, 0, 1).
It intentionally keeps the system small and fully inspectable.
"""
from __future__ import annotations
from typing import Any, Mapping
import numpy as np
from .base import BaseEnvironment, StepResult


class MaintenanceNetworkEnvironment(BaseEnvironment):
    def __init__(self, config: Mapping[str, Any]):
        self.config = dict(config)
        self.environment_id = str(config["id"])
        self.version = str(config["version"])
        self.n = int(config.get("n_components", 3))
        self.horizon = int(config.get("horizon", 400))
        self.theta = np.asarray(config.get("viability_thresholds", [0.35]*self.n), dtype=float)
        self.degradation = np.asarray(config.get("degradation", [0.010]*self.n), dtype=float)
        self.noise_max = float(config.get("noise_max", 0.002))
        self.shock_probability = float(config.get("shock_probability", 0.06))
        self.shock_min = float(config.get("shock_min", 0.05))
        self.shock_max = float(config.get("shock_max", 0.12))
        self.intervention = dict(config.get("intervention", {}))
        self.rescue = dict(config.get("rescue", {}))
        self._rng = None
        self._q = np.ones(self.n, dtype=float)
        self._step = 0
        self._last_disturbance = np.zeros(self.n)
        self._last_m_int = np.zeros(self.n)
        self._last_m_ext = np.zeros(self.n)
        self._ever_failed = False

    def reset(self, seed: int) -> Any:
        self._rng = np.random.default_rng(int(seed))
        self._q = np.asarray(self.config.get("initial_state", [1.0]*self.n), dtype=float).copy()
        self._step = 0
        self._last_disturbance = np.zeros(self.n)
        self._last_m_int = np.zeros(self.n)
        self._last_m_ext = np.zeros(self.n)
        self._ever_failed = not self._is_viable()
        return self.observe()

    def _is_viable(self) -> bool:
        return bool(np.all(self._q >= self.theta))

    def _intervention_active(self) -> bool:
        return bool(self.intervention) and self._step >= int(self.intervention.get("step", self.horizon+1))

    def _rescue_active(self) -> bool:
        return bool(self.rescue) and self._step >= int(self.rescue.get("step", self.horizon+1))

    def observe(self) -> Any:
        disabled = None
        if self._intervention_active() and self.intervention.get("type") == "ablate_node":
            disabled = int(self.intervention["node"])
        external_support_allowed = not (
            self._intervention_active() and self.intervention.get("type") == "withdraw_external_support"
        )
        return {
            "q": self._q.tolist(),
            "step": self._step,
            "viability_thresholds": self.theta.tolist(),
            "disabled_node": disabled,
            "external_support_allowed": external_support_allowed,
        }

    def _sample_disturbance(self) -> np.ndarray:
        assert self._rng is not None
        x = self._rng.uniform(0.0, self.noise_max, size=self.n)
        if self._rng.random() < self.shock_probability:
            target = int(self._rng.integers(0, self.n))
            x[target] += float(self._rng.uniform(self.shock_min, self.shock_max))
        return x

    def step(self, action: Any) -> StepResult:
        action = action or {}
        m_int = np.asarray(action.get("m_int", [0.0]*self.n), dtype=float)
        m_ext = np.asarray(action.get("m_ext", [0.0]*self.n), dtype=float)
        if m_int.shape != (self.n,) or m_ext.shape != (self.n,):
            raise ValueError("maintenance vectors must match component count")
        m_int = np.maximum(m_int, 0.0)
        m_ext = np.maximum(m_ext, 0.0)

        # Registered withdrawal removes external controller support.
        if self._intervention_active() and self.intervention.get("type") == "withdraw_external_support":
            m_ext[:] = 0.0

        # Registered node ablation fixes the component at zero and prevents its own maintenance.
        ablated = None
        if self._intervention_active() and self.intervention.get("type") == "ablate_node":
            ablated = int(self.intervention["node"])
            self._q[ablated] = 0.0
            m_int[ablated] = 0.0
            m_ext[ablated] = 0.0

        # Rescue supplies a specific external replacement function to a target component.
        if self._rescue_active():
            target = int(self.rescue["target"])
            amount = float(self.rescue.get("amount", 0.03))
            m_ext[target] += amount

        disturbance = self._sample_disturbance()
        q_next = np.clip(self._q - self.degradation - disturbance + m_int + m_ext, 0.0, 1.0)
        if ablated is not None:
            q_next[ablated] = 0.0
        self._q = q_next
        self._step += 1
        viable = self._is_viable()
        self._ever_failed = self._ever_failed or (not viable)
        self._last_disturbance = disturbance
        self._last_m_int = m_int
        self._last_m_ext = m_ext
        terminated = self._step >= self.horizon
        snap = self.snapshot()
        return StepResult(observation=self.observe(), outcome={"viable": viable}, terminated=terminated, info=snap)

    def snapshot(self) -> Mapping[str, Any]:
        return {
            "state": float(np.mean(self._q)),
            "q": self._q.tolist(),
            "min_q": float(np.min(self._q)),
            "mean_q": float(np.mean(self._q)),
            "viable": self._is_viable(),
            "ever_failed": self._ever_failed,
            "step": self._step,
            "disturbance": self._last_disturbance.tolist(),
            "m_int": self._last_m_int.tolist(),
            "m_ext": self._last_m_ext.tolist(),
            "maintenance_total": float(np.sum(self._last_m_int) + np.sum(self._last_m_ext)),
        }
