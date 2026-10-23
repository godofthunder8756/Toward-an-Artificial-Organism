"""Provenance capture and validation for ToE experiment runs."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from toe import __version__ as software_version
from toe.core.logging import atomic_write_json, canonical_json
from toe.core.seeds import SeedPlan
from validate_manifest import sha256_file


@dataclass(frozen=True)
class ProvenanceIssue:
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def detect_source_commit(project_root: Path, fallback: str | None = None) -> str | None:
    env_value = os.environ.get("TOE_SOURCE_COMMIT")
    if env_value:
        return env_value
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
        value = result.stdout.strip()
        return value or fallback
    except Exception:  # noqa: BLE001
        return fallback


def runtime_metadata() -> dict[str, Any]:
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "executable": os.path.realpath(os.sys.executable),
        "process_id": os.getpid(),
    }


def trajectory_content_sha256(path: Path) -> str:
    """Digest scientific trajectory content while excluding run-instance metadata."""
    h = hashlib.sha256()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            record.pop("run_id", None)
            h.update((canonical_json(record) + "\n").encode("utf-8"))
    return h.hexdigest()


def build_provenance(
    *,
    run_id: str,
    manifest: dict[str, Any],
    manifest_path: Path,
    lock: dict[str, Any] | None,
    project_root: Path,
    seed_plan: SeedPlan,
    architecture_hashes: dict[str, str],
    environment_sha256: str,
    trajectory_file_sha256: str,
    trajectory_content_sha256_value: str,
    trajectory_records: int,
    event_log_sha256: str,
    seed_snapshot_sha256: str,
    started_at_utc: str,
    completed_at_utc: str,
    runtime_seconds: float,
    raw_state_archives: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    fallback_commit = lock.get("source_commit") if lock else None
    source_commit = detect_source_commit(project_root, fallback_commit)
    return {
        "provenance_schema_version": "1.0.0",
        "run_id": run_id,
        "experiment_id": manifest["experiment"]["id"],
        "experiment_version": manifest["experiment"]["version"],
        "execution_mode": manifest["experiment"]["mode"],
        "manifest_path": str(manifest_path.relative_to(project_root)),
        "manifest_sha256": sha256_file(manifest_path),
        "frozen_manifest_sha256": lock.get("manifest_sha256") if lock else None,
        "frozen_at_utc": lock.get("frozen_at_utc") if lock else None,
        "software_version": software_version,
        "source_commit": source_commit,
        "environment": {
            "id": manifest["environment"]["id"],
            "version": manifest["environment"]["version"],
            "sha256": environment_sha256,
        },
        "architectures": [
            {
                "id": arch["id"],
                "version": arch["version"],
                "sha256": architecture_hashes[arch["id"]],
            }
            for arch in manifest["architectures"]
        ],
        "seed_plan": seed_plan.to_dict(),
        "trajectory": {
            "file_sha256": trajectory_file_sha256,
            "content_sha256": trajectory_content_sha256_value,
            "records": trajectory_records,
        },
        "event_log_sha256": event_log_sha256,
        "seed_snapshot_sha256": seed_snapshot_sha256,
        "started_at_utc": started_at_utc,
        "completed_at_utc": completed_at_utc,
        "runtime_seconds": runtime_seconds,
        "runtime_metadata": runtime_metadata(),
        "raw_state_archives": raw_state_archives or [],
    }


def write_file_manifest(run_dir: Path, include: list[Path]) -> Path:
    entries: list[dict[str, Any]] = []
    for path in include:
        entries.append(
            {
                "path": str(path.relative_to(run_dir)),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    output = run_dir / "file_manifest.json"
    atomic_write_json(output, {"files": entries})
    return output


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_run_provenance(
    run_dir: Path,
    *,
    project_root: Path | None = None,
    manifest_path: Path | None = None,
) -> list[ProvenanceIssue]:
    issues: list[ProvenanceIssue] = []
    required = [
        "trajectories.jsonl",
        "events.jsonl",
        "seed_registry.json",
        "provenance.json",
        "run_summary.json",
        "file_manifest.json",
    ]
    for name in required:
        if not (run_dir / name).exists():
            issues.append(ProvenanceIssue("P001", f"Missing required run artefact: {name}"))
    if issues:
        return issues

    provenance = _load_json(run_dir / "provenance.json")
    summary = _load_json(run_dir / "run_summary.json")
    seed_snapshot = _load_json(run_dir / "seed_registry.json")
    file_manifest = _load_json(run_dir / "file_manifest.json")

    run_id = provenance.get("run_id")
    if not run_id or summary.get("run_id") != run_id:
        issues.append(ProvenanceIssue("P002", "run_id missing or inconsistent between provenance and summary"))

    if provenance.get("execution_mode") in {"confirmatory", "replication"} and provenance.get("source_commit") in {None, "", "UNKNOWN"}:
        issues.append(ProvenanceIssue("P003", "source_commit is required for confirmatory/replication runs"))
    if not provenance.get("software_version"):
        issues.append(ProvenanceIssue("P004", "software_version is required"))
    if not provenance.get("runtime_metadata"):
        issues.append(ProvenanceIssue("P005", "runtime_metadata is required"))

    # Validate the run file inventory.
    entries = file_manifest.get("files")
    if not isinstance(entries, list) or not entries:
        issues.append(ProvenanceIssue("P006", "file_manifest contains no files"))
    else:
        for entry in entries:
            rel = entry.get("path")
            if not isinstance(rel, str):
                issues.append(ProvenanceIssue("P006", "file_manifest entry lacks path"))
                continue
            path = run_dir / rel
            if not path.exists():
                issues.append(ProvenanceIssue("P007", f"Archived file missing: {rel}"))
                continue
            actual = sha256_file(path)
            if actual != entry.get("sha256"):
                issues.append(ProvenanceIssue("P008", f"File hash mismatch: {rel}"))

    trajectory_path = run_dir / "trajectories.jsonl"
    trajectory_file_hash = sha256_file(trajectory_path)
    trajectory_content_hash = trajectory_content_sha256(trajectory_path)
    if trajectory_file_hash != provenance.get("trajectory", {}).get("file_sha256"):
        issues.append(ProvenanceIssue("P009", "Trajectory file hash differs from provenance record"))
    if trajectory_content_hash != provenance.get("trajectory", {}).get("content_sha256"):
        issues.append(ProvenanceIssue("P010", "Trajectory content hash differs from provenance record"))
    if trajectory_content_hash != summary.get("trajectory_sha256"):
        issues.append(ProvenanceIssue("P024", "Trajectory content hash differs from run summary"))

    # Validate every trajectory seed and run id against the frozen seed snapshot.
    registered = {
        int(item["value"]): item["seed_id"]
        for item in seed_snapshot.get("records", [])
        if isinstance(item, dict) and "value" in item and "seed_id" in item
    }
    line_count = 0
    with trajectory_path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                issues.append(ProvenanceIssue("P011", f"Invalid JSON trajectory record at line {line_no}"))
                continue
            if record.get("run_id") != run_id:
                issues.append(ProvenanceIssue("P012", f"Trajectory run_id mismatch at line {line_no}"))
            seed = record.get("seed")
            if seed not in registered:
                issues.append(ProvenanceIssue("P013", f"Unregistered seed {seed!r} at line {line_no}"))
            elif record.get("seed_id") != registered[seed]:
                issues.append(ProvenanceIssue("P014", f"seed_id mismatch at line {line_no}"))
    if line_count != provenance.get("trajectory", {}).get("records"):
        issues.append(ProvenanceIssue("P015", "Trajectory record count differs from provenance record"))

    # Validate seed-plan digest linkage.
    if seed_snapshot.get("seed_plan_sha256") != provenance.get("seed_plan", {}).get("seed_plan_sha256"):
        issues.append(ProvenanceIssue("P016", "Seed-plan digest mismatch"))

    if sha256_file(run_dir / "events.jsonl") != provenance.get("event_log_sha256"):
        issues.append(ProvenanceIssue("P018", "Event-log hash differs from provenance record"))
    if sha256_file(run_dir / "seed_registry.json") != provenance.get("seed_snapshot_sha256"):
        issues.append(ProvenanceIssue("P019", "Seed-snapshot hash differs from provenance record"))

    for archive in provenance.get("raw_state_archives", []):
        rel = archive.get("path")
        expected = archive.get("sha256")
        if not isinstance(rel, str):
            issues.append(ProvenanceIssue("P025", "Raw-state archive entry lacks path"))
            continue
        path = run_dir / rel
        if not path.exists():
            issues.append(ProvenanceIssue("P025", f"Raw-state archive missing: {rel}"))
        elif sha256_file(path) != expected:
            issues.append(ProvenanceIssue("P026", f"Raw-state archive hash mismatch: {rel}"))

    # Optional revalidation against project source material.
    if project_root is not None and manifest_path is not None:
        manifest_hash = sha256_file(manifest_path)
        if manifest_hash != provenance.get("manifest_sha256"):
            issues.append(ProvenanceIssue("P017", "Current manifest hash differs from recorded provenance"))
        try:
            from validate_manifest import load_structured
            manifest = load_structured(manifest_path)
            env_path = (project_root / manifest["environment"]["config"]).resolve()
            if sha256_file(env_path) != provenance.get("environment", {}).get("sha256"):
                issues.append(ProvenanceIssue("P020", "Environment configuration hash mismatch"))
            prov_arch = {x.get("id"): x.get("sha256") for x in provenance.get("architectures", [])}
            for arch in manifest.get("architectures", []):
                arch_path = (project_root / arch["config"]).resolve()
                if sha256_file(arch_path) != prov_arch.get(arch["id"]):
                    issues.append(ProvenanceIssue("P021", f"Architecture configuration hash mismatch: {arch['id']}"))
            if manifest["experiment"]["mode"] in {"confirmatory", "replication"}:
                frozen_hash = provenance.get("frozen_manifest_sha256")
                if not frozen_hash or frozen_hash != provenance.get("manifest_sha256"):
                    issues.append(ProvenanceIssue("P022", "Confirmatory frozen manifest hash is missing or inconsistent"))
        except Exception as exc:  # noqa: BLE001
            issues.append(ProvenanceIssue("P023", f"Could not revalidate project configuration: {exc}"))

    return issues


def write_validation_report(run_dir: Path, issues: list[ProvenanceIssue]) -> Path:
    output = run_dir / "provenance_validation.json"
    atomic_write_json(
        output,
        {
            "status": "PASS" if not issues else "FAIL",
            "validated_at_utc": _utc_now(),
            "issues": [{"code": i.code, "message": i.message} for i in issues],
        },
    )
    return output
