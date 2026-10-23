"""Explicit component allow-list for the ToE experimental programme."""
from __future__ import annotations
from typing import Any, Mapping
from toe.agents import DummyAgent, NoOpAgent, MaintenanceAgent
from toe.environments import DummyEnvironment, GrayScottEnvironment, MaintenanceNetworkEnvironment

class ComponentFactoryError(RuntimeError):
    pass

def make_environment(config: Mapping[str, Any]):
    env_id = config.get("id")
    if env_id == "DUMMY_ENV":
        return DummyEnvironment(config)
    if env_id == "GRAY_SCOTT_2D":
        return GrayScottEnvironment(config)
    if env_id == "MAINTENANCE_NETWORK":
        return MaintenanceNetworkEnvironment(config)
    raise ComponentFactoryError(f"Unregistered environment id: {env_id!r}")

def make_agent(config: Mapping[str, Any]):
    arch_id = config.get("id")
    if arch_id == "DUMMY_AGENT":
        return DummyAgent(config)
    if arch_id == "NOOP_FIELD_DRIVER":
        return NoOpAgent(config)
    if str(config.get("kind", "")) in {"passive", "external", "feedforward", "reciprocal", "brute_force"}:
        return MaintenanceAgent(config)
    raise ComponentFactoryError(f"Unregistered architecture id: {arch_id!r}")
