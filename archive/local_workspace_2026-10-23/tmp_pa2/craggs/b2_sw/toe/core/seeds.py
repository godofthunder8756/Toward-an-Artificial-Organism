"""Registered seed management for ToE experiments.

Scientific randomness must be explicit, reproducible and auditable.  This module
resolves a manifest seed specification into an immutable seed plan, verifies
registry hashes where applicable, and emits a canonical per-run seed snapshot.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from validate_manifest import resolve_project_path, sha256_file


class SeedError(RuntimeError):
    """Raised when a seed specification cannot be resolved safely."""


@dataclass(frozen=True)
class SeedRecord:
    seed_id: str
    value: int
    source: str


@dataclass(frozen=True)
class SeedPlan:
    procedure: str
    records: tuple[SeedRecord, ...]
    generator_seed: int | None = None
    registry_file: str | None = None
    registry_sha256: str | None = None

    @property
    def values(self) -> list[int]:
        return [r.value for r in self.records]

    @property
    def digest(self) -> str:
        payload = {
            "procedure": self.procedure,
            "records": [asdict(r) for r in self.records],
            "generator_seed": self.generator_seed,
            "registry_file": self.registry_file,
            "registry_sha256": self.registry_sha256,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def record_for_value(self, value: int) -> SeedRecord:
        for record in self.records:
            if record.value == value:
                return record
        raise SeedError(f"Seed {value} is not registered in this plan")

    def to_dict(self) -> dict[str, Any]:
        return {
            "procedure": self.procedure,
            "records": [asdict(r) for r in self.records],
            "generator_seed": self.generator_seed,
            "registry_file": self.registry_file,
            "registry_sha256": self.registry_sha256,
            "seed_plan_sha256": self.digest,
        }


def _ensure_unique(values: list[int]) -> None:
    if len(values) != len(set(values)):
        raise SeedError("Resolved seed set contains duplicate values")


def _records(values: list[int], source: str) -> tuple[SeedRecord, ...]:
    _ensure_unique(values)
    return tuple(
        SeedRecord(seed_id=f"SEED_{index:04d}", value=int(value), source=source)
        for index, value in enumerate(values, start=1)
    )


def _parse_registry(path: Path) -> list[int]:
    values: list[int] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        try:
            value = int(raw)
        except ValueError as exc:
            raise SeedError(f"Non-integer seed in registry {path}: {raw!r}") from exc
        if value < 0:
            raise SeedError(f"Negative seed in registry {path}: {value}")
        values.append(value)
    if not values:
        raise SeedError(f"Seed registry contains no usable seeds: {path}")
    return values


def resolve_seed_plan(manifest: dict[str, Any], project_root: Path) -> SeedPlan:
    spec = manifest["seeds"]
    procedure = spec["procedure"]

    if procedure == "explicit":
        values = [int(v) for v in spec["values"]]
        return SeedPlan(procedure="explicit", records=_records(values, "manifest"))

    if procedure == "generated":
        if manifest["experiment"]["mode"] != "development":
            raise SeedError("Generated-at-runtime seeds are permitted only in development mode")
        generator_seed = int(spec["generator_seed"])
        rng = random.Random(generator_seed)
        values: list[int] = []
        seen: set[int] = set()
        while len(values) < int(spec["count"]):
            value = rng.randrange(0, 2**31 - 1)
            if value not in seen:
                values.append(value)
                seen.add(value)
        return SeedPlan(
            procedure="generated",
            records=_records(values, "deterministic_generator"),
            generator_seed=generator_seed,
        )

    if procedure == "registry":
        rel = spec["file"]
        path = resolve_project_path(project_root, rel)
        if not path.exists():
            raise SeedError(f"Seed registry does not exist: {rel}")
        actual = sha256_file(path)
        expected = spec["sha256"].lower()
        if actual.lower() != expected:
            raise SeedError(
                f"Seed registry hash mismatch for {rel}: expected {expected}, got {actual}"
            )
        values = _parse_registry(path)
        return SeedPlan(
            procedure="registry",
            records=_records(values, "frozen_registry"),
            registry_file=rel,
            registry_sha256=actual,
        )

    raise SeedError(f"Unsupported seed procedure: {procedure!r}")
