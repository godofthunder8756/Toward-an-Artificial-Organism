"""Manifest-driven experiment runner with Stage A4 audit logging.

A valid manifest controls execution.  Confirmatory/replication execution additionally
requires a verified frozen lock.  Every run emits append-only trajectories and events,
a frozen seed snapshot, provenance metadata, a file integrity manifest and an automatic
provenance validation report.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from toe.core.factories import make_agent, make_environment
from toe.core.logging import JsonlWriter, RunEventLogger, atomic_write_json, canonical_json
from toe.core.provenance import (
    build_provenance,
    validate_run_provenance,
    write_file_manifest,
    write_validation_report,
)
from toe.core.seeds import SeedError, SeedPlan, resolve_seed_plan
from validate_manifest import (
    load_structured,
    schema_validate,
    semantic_validate,
    sha256_file,
    verify_frozen,
)


class RunnerError(RuntimeError):
    """Raised when execution would violate the experiment contract."""


@dataclass(frozen=True)
class RunResult:
    run_id: str
    run_directory: Path
    raw_trajectory_path: Path
    event_log_path: Path
    seed_registry_path: Path
    provenance_path: Path
    summary_path: Path
    file_manifest_path: Path
    validation_report_path: Path
    trajectory_sha256: str
    terminal_state_mean: float
    records_written: int
    provenance_valid: bool


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _utc_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")


def _infer_lock_path(manifest_path: Path) -> Path:
    return manifest_path.with_suffix(".lock.json")


def _new_run_id(experiment_id: str, version: str, mode: str) -> str:
    return f"{experiment_id}__v{version}__{mode}__{_utc_compact()}__{uuid.uuid4().hex[:12]}"


class ExperimentRunner:
    def __init__(
        self,
        *,
        project_root: Path,
        schema_path: Path,
        output_root: Path,
        experiment_registry: Path | None = None,
    ):
        self.project_root = project_root.resolve()
        self.schema_path = schema_path.resolve()
        self.output_root = output_root.resolve()
        self.experiment_registry = experiment_registry.resolve() if experiment_registry else None

    def _check_execution_gate(self, manifest: dict[str, Any]) -> None:
        """Enforce optional experiment-registry execution status for confirmatory work."""
        if self.experiment_registry is None or manifest["experiment"]["mode"] not in {"confirmatory", "replication"}:
            return
        if not self.experiment_registry.exists():
            raise RunnerError(f"Experiment registry does not exist: {self.experiment_registry}")
        registry = load_structured(self.experiment_registry)
        entries = registry.get("experiments", []) if isinstance(registry, dict) else []
        eid = manifest["experiment"]["id"]
        ver = manifest["experiment"]["version"]
        match = next((x for x in entries if isinstance(x, dict) and x.get("id") == eid and x.get("version") == ver), None)
        if match is None:
            return
        status = str(match.get("status", ""))
        if status in {"FROZEN_PENDING_PUBLIC_PREREGISTRATION", "FROZEN_PREREGISTRATION_READY_UNRUN"}:
            raise RunnerError(
                f"Execution gate closed for {eid} v{ver}: public preregistration has not yet been recorded"
            )
        allowed = {"CLEARED_FOR_CONFIRMATORY_EXECUTION", "EXECUTED", "REPLICATION_CLEARED"}
        if status and status not in allowed:
            raise RunnerError(f"Execution gate status {status!r} does not permit confirmatory execution")

    def _validate_for_execution(self, manifest_path: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
        manifest_path = manifest_path.resolve()
        manifest = load_structured(manifest_path)
        schema = load_structured(self.schema_path)
        issues = schema_validate(manifest, schema)
        if not issues:
            # An already registered experiment is executable, so V001 is not re-applied here.
            issues.extend(semantic_validate(manifest, manifest_path, self.project_root, None))
        if issues:
            joined = "\n".join(str(x) for x in issues)
            raise RunnerError(f"Manifest validation failed:\n{joined}")

        self._check_execution_gate(manifest)

        lock: dict[str, Any] | None = None
        if manifest["experiment"]["mode"] in {"confirmatory", "replication"}:
            lock_path = _infer_lock_path(manifest_path)
            frozen_issues = verify_frozen(manifest_path, lock_path, self.project_root)
            if frozen_issues:
                joined = "\n".join(str(x) for x in frozen_issues)
                raise RunnerError(f"Frozen-manifest verification failed:\n{joined}")
            lock = load_structured(lock_path)
        return manifest, lock

    def _load_environment_config(self, manifest: dict[str, Any]) -> tuple[dict[str, Any], Path]:
        path = (self.project_root / manifest["environment"]["config"]).resolve()
        config = load_structured(path)
        if config.get("id") != manifest["environment"]["id"]:
            raise RunnerError("Environment config id does not match manifest")
        if str(config.get("version")) != manifest["environment"]["version"]:
            raise RunnerError("Environment config version does not match manifest")
        return config, path

    def _load_architecture_config(self, arch_spec: dict[str, Any]) -> tuple[dict[str, Any], Path]:
        path = (self.project_root / arch_spec["config"]).resolve()
        config = load_structured(path)
        if config.get("id") != arch_spec["id"]:
            raise RunnerError(f"Architecture config id does not match manifest for {arch_spec['id']}")
        if str(config.get("version")) != arch_spec["version"]:
            raise RunnerError(f"Architecture config version does not match manifest for {arch_spec['id']}")
        return config, path

    def run(self, manifest_path: Path) -> RunResult:
        manifest_path = manifest_path.resolve()
        manifest, lock = self._validate_for_execution(manifest_path)
        env_config, env_config_path = self._load_environment_config(manifest)
        try:
            seed_plan: SeedPlan = resolve_seed_plan(manifest, self.project_root)
        except SeedError as exc:
            raise RunnerError(str(exc)) from exc

        arch_configs: list[tuple[dict[str, Any], dict[str, Any], Path]] = []
        for arch_spec in manifest["architectures"]:
            config, path = self._load_architecture_config(arch_spec)
            arch_configs.append((arch_spec, config, path))

        exp_id = manifest["experiment"]["id"]
        exp_ver = manifest["experiment"]["version"]
        mode = manifest["experiment"]["mode"]
        run_id = _new_run_id(exp_id, exp_ver, mode)
        run_dir = self.output_root / "raw" / exp_id / exp_ver / run_id
        run_dir.mkdir(parents=True, exist_ok=False)

        raw_path = run_dir / "trajectories.jsonl"
        events_path = run_dir / "events.jsonl"
        seed_registry_path = run_dir / "seed_registry.json"
        provenance_path = run_dir / "provenance.json"
        summary_path = run_dir / "run_summary.json"

        atomic_write_json(seed_registry_path, seed_plan.to_dict())
        seed_snapshot_sha = sha256_file(seed_registry_path)

        started_wall = _utc_iso()
        started = time.perf_counter()
        terminal_states: list[float] = []
        raw_state_archives: list[dict[str, Any]] = []
        raw_state_paths: list[Path] = []
        archive_raw_state = bool(env_config.get("archive_raw_state", False))
        scientific_trajectory_hash = hashlib.sha256()
        episodes_per_seed = int(manifest["evaluation"]["episodes_per_seed"])

        trajectory_writer = JsonlWriter(raw_path)
        event_logger = RunEventLogger(events_path, run_id)
        event_logger.emit(
            "RUN_START",
            experiment_id=exp_id,
            experiment_version=exp_ver,
            execution_mode=mode,
            manifest_sha256=sha256_file(manifest_path),
            seed_plan_sha256=seed_plan.digest,
        )

        try:
            for arch_spec, arch_config, _arch_path in arch_configs:
                event_logger.emit("ARCHITECTURE_START", architecture_id=arch_spec["id"])
                for seed_record in seed_plan.records:
                    event_logger.emit(
                        "SEED_START",
                        architecture_id=arch_spec["id"],
                        seed_id=seed_record.seed_id,
                        seed=seed_record.value,
                    )
                    for episode in range(episodes_per_seed):
                        environment = make_environment(env_config)
                        agent = make_agent(arch_config)
                        observation = environment.reset(seed_record.value)
                        agent.reset(seed_record.value)
                        step_index = 0
                        field_steps: list[int] = []
                        field_u: list[np.ndarray] = []
                        field_v: list[np.ndarray] = []
                        if archive_raw_state:
                            raw0 = environment.raw_state()
                            if raw0 is not None:
                                field_steps.append(int(raw0["pde_step"]))
                                field_u.append(np.asarray(raw0["u"], dtype=np.float32))
                                field_v.append(np.asarray(raw0["v"], dtype=np.float32))

                        while True:
                            state_before = dict(environment.snapshot())
                            internal_before = dict(agent.snapshot())
                            action = agent.act(observation)
                            result = environment.step(action)
                            record = {
                                "run_id": run_id,
                                "experiment_id": exp_id,
                                "experiment_version": exp_ver,
                                "execution_mode": mode,
                                "environment_id": environment.environment_id,
                                "environment_version": environment.version,
                                "architecture_id": agent.architecture_id,
                                "architecture_version": agent.version,
                                "seed_id": seed_record.seed_id,
                                "seed": seed_record.value,
                                "episode": episode,
                                "step": step_index,
                                "observation_before": observation,
                                "state_before": state_before,
                                "agent_state_before": internal_before,
                                "action": action,
                                "observation_after": result.observation,
                                "outcome": result.outcome,
                                "state_after": dict(environment.snapshot()),
                                "terminated": result.terminated,
                                "info": dict(result.info),
                                "intervention_label": None,
                            }
                            trajectory_writer.write(record)
                            scientific_record = dict(record)
                            scientific_record.pop("run_id", None)
                            scientific_trajectory_hash.update(
                                (canonical_json(scientific_record) + "\n").encode("utf-8")
                            )
                            observation = result.observation
                            step_index += 1
                            if archive_raw_state:
                                raw_state = environment.raw_state()
                                if raw_state is not None:
                                    field_steps.append(int(raw_state["pde_step"]))
                                    field_u.append(np.asarray(raw_state["u"], dtype=np.float32))
                                    field_v.append(np.asarray(raw_state["v"], dtype=np.float32))
                            if result.terminated:
                                terminal_states.append(float(environment.snapshot()["state"]))
                                if archive_raw_state and field_u:
                                    fields_dir = run_dir / "fields"
                                    fields_dir.mkdir(parents=True, exist_ok=True)
                                    field_path = fields_dir / f"{arch_spec['id']}__{seed_record.seed_id}__ep{episode:03d}.npz"
                                    np.savez_compressed(
                                        field_path,
                                        pde_step=np.asarray(field_steps, dtype=np.int32),
                                        u=np.stack(field_u).astype(np.float32),
                                        v=np.stack(field_v).astype(np.float32),
                                    )
                                    raw_state_paths.append(field_path)
                                break
                    event_logger.emit(
                        "SEED_END",
                        architecture_id=arch_spec["id"],
                        seed_id=seed_record.seed_id,
                        seed=seed_record.value,
                    )
                event_logger.emit("ARCHITECTURE_END", architecture_id=arch_spec["id"])
        except Exception as exc:  # noqa: BLE001
            event_logger.emit("RUN_ERROR", error_type=type(exc).__name__, error_message=str(exc))
            trajectory_writer.close()
            event_logger.close()
            raise

        trajectory_writer.close()
        runtime = time.perf_counter() - started
        terminal_mean = sum(terminal_states) / len(terminal_states)
        event_logger.emit(
            "RUN_END",
            records_written=trajectory_writer.count,
            terminal_state_mean=terminal_mean,
            runtime_seconds=runtime,
            raw_state_archives=raw_state_archives,
        )
        event_logger.close()
        completed_wall = _utc_iso()

        scientific_trajectory_sha = scientific_trajectory_hash.hexdigest()

        architecture_hashes = {
            arch_spec["id"]: sha256_file(path)
            for arch_spec, _config, path in arch_configs
        }
        raw_state_archives = [
            {
                "path": str(path.relative_to(run_dir)),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in raw_state_paths
        ]
        provenance = build_provenance(
            run_id=run_id,
            manifest=manifest,
            manifest_path=manifest_path,
            lock=lock,
            project_root=self.project_root,
            seed_plan=seed_plan,
            architecture_hashes=architecture_hashes,
            environment_sha256=sha256_file(env_config_path),
            trajectory_file_sha256=trajectory_writer.sha256,
            trajectory_content_sha256_value=scientific_trajectory_sha,
            trajectory_records=trajectory_writer.count,
            event_log_sha256=event_logger.sha256,
            seed_snapshot_sha256=seed_snapshot_sha,
            started_at_utc=started_wall,
            completed_at_utc=completed_wall,
            runtime_seconds=runtime,
            raw_state_archives=raw_state_archives,
        )
        atomic_write_json(provenance_path, provenance)

        summary = {
            "run_id": run_id,
            "experiment_id": exp_id,
            "experiment_version": exp_ver,
            "execution_mode": mode,
            "registered_seed_count": len(seed_plan.records),
            "seed_plan_sha256": seed_plan.digest,
            "episodes_per_seed": episodes_per_seed,
            "records_written": trajectory_writer.count,
            "terminal_state_mean": terminal_mean,
            "trajectory_sha256": scientific_trajectory_sha,
            "trajectory_file_sha256": trajectory_writer.sha256,
            "runtime_seconds": runtime,
            "provenance_path": "provenance.json",
            "status": "EXECUTION_COMPLETE",
        }
        atomic_write_json(summary_path, summary)

        file_manifest_path = write_file_manifest(
            run_dir,
            [raw_path, events_path, seed_registry_path, provenance_path, summary_path, *raw_state_paths],
        )
        provenance_issues = validate_run_provenance(
            run_dir,
            project_root=self.project_root,
            manifest_path=manifest_path,
        )
        validation_report_path = write_validation_report(run_dir, provenance_issues)
        if provenance_issues:
            joined = "\n".join(str(issue) for issue in provenance_issues)
            raise RunnerError(f"Run completed but provenance validation failed:\n{joined}")

        return RunResult(
            run_id=run_id,
            run_directory=run_dir,
            raw_trajectory_path=raw_path,
            event_log_path=events_path,
            seed_registry_path=seed_registry_path,
            provenance_path=provenance_path,
            summary_path=summary_path,
            file_manifest_path=file_manifest_path,
            validation_report_path=validation_report_path,
            trajectory_sha256=scientific_trajectory_sha,
            terminal_state_mean=terminal_mean,
            records_written=trajectory_writer.count,
            provenance_valid=True,
        )
