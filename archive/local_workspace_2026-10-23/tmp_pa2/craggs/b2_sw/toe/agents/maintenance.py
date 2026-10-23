"""Transparent maintenance controllers for B2 causal-maintenance experiments."""
from __future__ import annotations
from typing import Any, Mapping
import numpy as np
from .base import BaseAgent


class MaintenanceAgent(BaseAgent):
    def __init__(self, config: Mapping[str, Any]):
        self.config = dict(config)
        self.architecture_id = str(config["id"])
        self.version = str(config["version"])
        self.kind = str(config["kind"])
        self.n = int(config.get("n_components", 3))
        self.budget = float(config.get("maintenance_budget", 0.075))
        self.target = float(config.get("target_state", 0.90))
        self.edges = [tuple(map(int, e)) for e in config.get("edges", [])]
        self.source_self_fraction = float(config.get("source_self_fraction", 0.0))
        self.source_self_node = int(config.get("source_self_node", 0))
        self._seed = 0
        self._actions = 0

    def reset(self, seed: int) -> None:
        self._seed = int(seed)
        self._actions = 0

    def _allocate_direct(self, q: np.ndarray) -> np.ndarray:
        deficit = np.maximum(self.target - q, 0.0)
        s = deficit.sum()
        if s <= 0:
            return np.zeros(self.n)
        return self.budget * deficit / s

    def _allocate_edges(self, q: np.ndarray, disabled_node: int | None) -> np.ndarray:
        scores = []
        for source, target in self.edges:
            if disabled_node is not None and source == disabled_node:
                score = 0.0
            else:
                score = max(self.target - q[target], 0.0) * max(q[source], 0.0)
            scores.append(score)
        total = sum(scores)
        out = np.zeros(self.n)
        if total <= 0:
            return out
        for (source, target), score in zip(self.edges, scores):
            if score > 0:
                out[target] += self.budget * score / total
        return out

    def act(self, observation: Any) -> Any:
        self._actions += 1
        q = np.asarray(observation["q"], dtype=float)
        disabled = observation.get("disabled_node")
        if self.kind == "passive":
            return {"m_int": [0.0]*self.n, "m_ext": [0.0]*self.n}
        if self.kind == "external":
            ext = self._allocate_direct(q) if observation.get("external_support_allowed", True) else np.zeros(self.n)
            return {"m_int": [0.0]*self.n, "m_ext": ext.tolist()}
        if self.kind == "brute_force":
            m = self._allocate_direct(q)
            return {"m_int": m.tolist(), "m_ext": [0.0]*self.n}
        if self.kind in {"feedforward", "reciprocal"}:
            if self.kind == "feedforward" and self.source_self_fraction > 0:
                original_budget = self.budget
                source_budget = original_budget * self.source_self_fraction
                edge_budget = original_budget - source_budget
                m = np.zeros(self.n)
                if disabled is None or self.source_self_node != disabled:
                    source_deficit = max(self.target - q[self.source_self_node], 0.0)
                    if source_deficit > 0:
                        m[self.source_self_node] += min(source_budget, source_deficit)
                self.budget = edge_budget
                try:
                    m += self._allocate_edges(q, disabled)
                finally:
                    self.budget = original_budget
            else:
                m = self._allocate_edges(q, disabled)
            total = float(m.sum())
            if total > self.budget + 1e-12:
                m *= self.budget / total
            return {"m_int": m.tolist(), "m_ext": [0.0]*self.n}
        raise ValueError(f"Unknown maintenance architecture kind: {self.kind}")

    def snapshot(self) -> Mapping[str, Any]:
        return {
            "seed": self._seed,
            "actions_taken": self._actions,
            "kind": self.kind,
            "maintenance_budget": self.budget,
            "edges": [list(e) for e in self.edges],
        }
