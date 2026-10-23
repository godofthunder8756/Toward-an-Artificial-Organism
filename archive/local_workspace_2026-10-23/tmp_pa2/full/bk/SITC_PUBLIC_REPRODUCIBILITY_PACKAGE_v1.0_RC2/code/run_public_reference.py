# SPDX-License-Identifier: MPL-2.0
"""Execute a fresh public reproduction of the SITC reference construction.

This portable wrapper launches six new child processes using the registered
order and token permutations, scores each raw result with the scientific-only
public scorer, and compares normalized projections.  It does not replay the
historical command binding or process-provenance campaign.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import os
import secrets
import subprocess
import sys
import tempfile

from sitc_experiment import execute_registered_run
from sitc_plan import PREREG_SHA256, canonical, preregistration, replication_plan
from sitc_score import score_raw_run, terminal_decision


EXPECTED_PROJECTION_SHA256 = "565cf5f59fdc0d13b2ea538bd3bc8830cd5fff0ad80a51e19328128efe72d7f0"
HERE = Path(__file__).resolve().parent


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ValueError(code)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def worker(index: int, run_nonce: str, raw_path: Path, meta_path: Path) -> None:
    plan = replication_plan()
    require(0 <= index < len(plan), "WORKER_INDEX")
    require(len(run_nonce) == 64
            and all(ch in "0123456789abcdef" for ch in run_nonce),
            "WORKER_RUN_NONCE")
    run = plan[index]
    started = utc_now()
    raw = execute_registered_run(run)
    raw_path.write_bytes(canonical(raw))
    metadata = {
        "schema": "sitc-public-reference-worker/2",
        "registered_run_id": run["registered_run_id"],
        "ordering": run["ordering"],
        "run_nonce": run_nonce,
        "pid": os.getpid(),
        "parent_pid": os.getppid(),
        "python_implementation": sys.implementation.name,
        "python_version": ".".join(str(part) for part in sys.version_info[:3]),
        "started_utc": started,
        "finished_utc": utc_now(),
        "raw_bytes": raw_path.stat().st_size,
        "raw_sha256": file_sha256(raw_path),
    }
    meta_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def parent(output: Path, keep_raw: bool) -> None:
    preregistration()
    plan = replication_plan()
    execution_code_sha256 = {
        name: file_sha256(HERE / name)
        for name in [
            "run_public_reference.py",
            "sitc_core.py",
            "sitc_experiment.py",
            "sitc_plan.py",
            "sitc_score.py",
        ]
    }
    output.mkdir(parents=True, exist_ok=False)
    reports = []
    public_runs = []
    normalized_bytes: bytes | None = None
    parent_pid = os.getpid()
    started = utc_now()

    with tempfile.TemporaryDirectory(prefix="sitc-public-reference-") as temp_name:
        temp = Path(temp_name)
        for index, run in enumerate(plan):
            raw_path = temp / f"raw_{index + 1:03d}.json"
            meta_path = temp / f"meta_{index + 1:03d}.json"
            run_nonce = secrets.token_hex(32)
            command = [
                sys.executable,
                "-B",
                str(Path(__file__).resolve()),
                "--worker-index", str(index),
                "--run-nonce", run_nonce,
                "--raw-path", str(raw_path),
                "--meta-path", str(meta_path),
            ]
            environment = os.environ.copy()
            environment.update({
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONHASHSEED": "0",
                "OMP_NUM_THREADS": "1",
                "OPENBLAS_NUM_THREADS": "1",
                "MKL_NUM_THREADS": "1",
            })
            completed = subprocess.run(
                command,
                cwd=HERE,
                env=environment,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    "REFERENCE_WORKER_FAILED:"
                    + run["registered_run_id"]
                    + ":"
                    + str(completed.returncode)
                    + ":"
                    + completed.stderr[-2000:]
                )
            require(raw_path.is_file() and meta_path.is_file(),
                    "REFERENCE_WORKER_OUTPUT_MISSING:" + run["registered_run_id"])
            raw = json.loads(raw_path.read_text(encoding="ascii"))
            report = score_raw_run(raw, run)
            projection = canonical(report["normalized_projection"])
            projection_hash = hashlib.sha256(projection).hexdigest()
            require(report["status"] == "PASS" and report["scientific_failures"] == [],
                    "REFERENCE_SCORE_FAILED:" + run["registered_run_id"])
            require(projection_hash == EXPECTED_PROJECTION_SHA256,
                    "REFERENCE_PROJECTION_MISMATCH:" + run["registered_run_id"])
            if normalized_bytes is None:
                normalized_bytes = projection
            else:
                require(normalized_bytes == projection,
                        "REFERENCE_CROSS_RUN_MISMATCH:" + run["registered_run_id"])

            metadata = json.loads(meta_path.read_text(encoding="utf-8"))
            require(metadata.get("registered_run_id") == run["registered_run_id"]
                    and metadata.get("ordering") == run["ordering"],
                    "REFERENCE_WORKER_MAPPING:" + run["registered_run_id"])
            require(metadata.get("run_nonce") == run_nonce,
                    "REFERENCE_WORKER_NONCE:" + run["registered_run_id"])
            require(metadata.get("parent_pid") == parent_pid,
                    "REFERENCE_WORKER_PARENT:" + run["registered_run_id"])
            require(metadata.get("raw_sha256") == file_sha256(raw_path)
                    and metadata.get("raw_bytes") == raw_path.stat().st_size,
                    "REFERENCE_WORKER_RAW_BINDING:" + run["registered_run_id"])

            reports.append(report)
            public_runs.append({
                "registered_run_id": run["registered_run_id"],
                "ordering": run["ordering"],
                "run_nonce": run_nonce,
                "worker_pid": metadata["pid"],
                "worker_parent_pid": metadata["parent_pid"],
                "python_implementation": metadata["python_implementation"],
                "python_version": metadata["python_version"],
                "raw_bytes": metadata["raw_bytes"],
                "raw_sha256": metadata["raw_sha256"],
                "scientific_score": report["status"],
                "scientific_failures": report["scientific_failures"],
                "normalized_projection_sha256": projection_hash,
            })
            if keep_raw:
                destination = output / f"PUBLIC_RAW_{index + 1:03d}.json"
                destination.write_bytes(raw_path.read_bytes())
            print(f"{run['registered_run_id']} {run['ordering']} PASS", flush=True)

    status = terminal_decision(reports)
    require(status == "SITC_PASS", "PUBLIC_REFERENCE_TERMINAL_DECISION")
    worker_pids = [item["worker_pid"] for item in public_runs]
    nonces = [item["run_nonce"] for item in public_runs]
    require(len(set(nonces)) == 6, "PUBLIC_REFERENCE_NONCE_REUSE")
    require(len(set(worker_pids)) == 6, "PUBLIC_REFERENCE_WORKER_PID_REUSE")

    summary = {
        "schema": "sitc-public-reference-reproduction/2",
        "status": "PUBLIC_REFERENCE_REPRODUCTION_PASS",
        "execution_mode": "FRESH_PUBLIC_REFERENCE_EXECUTION",
        "preregistration_sha256": PREREG_SHA256,
        "started_utc": started,
        "finished_utc": utc_now(),
        "registered_run_count": 6,
        "execution_code_sha256": execution_code_sha256,
        "order_sequence": [item["ordering"] for item in public_runs],
        "fresh_child_processes": True,
        "unique_run_nonces": True,
        "all_six_scientific_scores_pass": True,
        "all_six_normalized_projections_byte_identical": True,
        "normalized_projection_sha256": EXPECTED_PROJECTION_SHA256,
        "historical_campaign_recreated": False,
        "historical_raw_arrays_loaded": False,
        "historical_absolute_command_binding_replayed": False,
        "historical_process_provenance_replayed": False,
        "runs": public_runs,
    }
    target = output / "PUBLIC_REFERENCE_REPRODUCTION_SUMMARY.json"
    target.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd() / "sitc_public_reference_output",
    )
    parser.add_argument("--keep-raw", action="store_true")
    parser.add_argument("--worker-index", type=int)
    parser.add_argument("--run-nonce")
    parser.add_argument("--raw-path", type=Path)
    parser.add_argument("--meta-path", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.worker_index is not None:
        if args.run_nonce is None or args.raw_path is None or args.meta_path is None:
            raise ValueError("WORKER_ARGUMENTS_REQUIRED")
        worker(args.worker_index, args.run_nonce, args.raw_path, args.meta_path)
    else:
        if args.run_nonce is not None or args.raw_path is not None or args.meta_path is not None:
            raise ValueError("WORKER_ARGUMENTS_WITHOUT_WORKER_INDEX")
        parent(args.output.resolve(), args.keep_raw)


if __name__ == "__main__":
    main()
