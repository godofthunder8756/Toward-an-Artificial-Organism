#!/usr/bin/env python3
"""Run one ToE experiment from a validated manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from toe.core.runner import ExperimentRunner, RunnerError


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--schema", type=Path, default=Path("configs/schema/experiment_manifest.schema.json"))
    ap.add_argument("--project-root", type=Path, default=Path("."))
    ap.add_argument("--output-root", type=Path, default=Path("results"))
    ap.add_argument("--experiment-registry", type=Path, default=Path("configs/experiment_registry.yaml"))
    args = ap.parse_args()

    runner = ExperimentRunner(
        project_root=args.project_root,
        schema_path=(args.project_root / args.schema if not args.schema.is_absolute() else args.schema),
        output_root=(args.project_root / args.output_root if not args.output_root.is_absolute() else args.output_root),
        experiment_registry=(args.project_root / args.experiment_registry if not args.experiment_registry.is_absolute() else args.experiment_registry),
    )
    try:
        result = runner.run(args.manifest)
    except RunnerError as exc:
        print(f"FAIL\n{exc}")
        return 2

    print("PASS")
    print(json.dumps({
        "run_id": result.run_id,
        "run_directory": str(result.run_directory),
        "raw_trajectory_path": str(result.raw_trajectory_path),
        "event_log_path": str(result.event_log_path),
        "seed_registry_path": str(result.seed_registry_path),
        "provenance_path": str(result.provenance_path),
        "summary_path": str(result.summary_path),
        "file_manifest_path": str(result.file_manifest_path),
        "validation_report_path": str(result.validation_report_path),
        "trajectory_sha256": result.trajectory_sha256,
        "terminal_state_mean": result.terminal_state_mean,
        "records_written": result.records_written,
        "provenance_valid": result.provenance_valid,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
