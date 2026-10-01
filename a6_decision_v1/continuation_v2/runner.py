"""Additive resource fix and prospectively proved compact F2 continuation."""

from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from a6_decision_v1.preservation import digest, write_once
from a6_decision_v1.runner import HERE, JOBS, LIMITS, MemoryJob, ROOT, contract

LOCAL = Path(__file__).resolve().parent
REMAINING = JOBS[2:]


def normalize_counts(report):
    diagnostic = report.get("milp_NOT_CERTIFICATE")
    if diagnostic is not None and diagnostic["nodes_reported"] is None:
        diagnostic["raw_internal_aggregate_counter"] = diagnostic["aggregate_nodes"]
        diagnostic["aggregate_nodes"] = None
        diagnostic["node_usage_known"] = False
    elif diagnostic is not None:
        diagnostic["nodes_reported"] = int(diagnostic["nodes_reported"])
        diagnostic["aggregate_nodes"] = int(diagnostic["aggregate_nodes"])
    if report.get("job", "").startswith("f3"):
        if report.get("nodes_reported") is not None:
            report["nodes_reported"] = int(report["nodes_reported"])
        report["aggregate_nodes"] = report.get("nodes_reported")
        report["node_usage_known"] = report.get("nodes_reported") is not None
    return report


def freeze():
    original = contract()
    if not (HERE / "f1_positive_result.json").is_file() or not (HERE / "f1_negative_result.json").is_file():
        raise ValueError("both consumed prefix jobs must have explicit closures")
    sources = sorted(LOCAL.glob("*.py")) + [LOCAL / "RESOURCE_ERRATA.md"]
    document = {
        "schema": 2, "original_contract_sha256": digest(HERE / "contract.json"),
        "remaining_jobs": list(REMAINING), "limits": original["limits"],
        "source_sha256": {p.name: digest(p) for p in sources},
        "no_additional_budget": True, "gate_and_deployed_family_unchanged": True,
        "f2_prospectively_reduced_by_exact_theorem": True,
        "reduction_sha256": digest(ROOT / "A6_GATE_REDUCTION_v1.md"),
        "additional_checker_sha256": {
            name: digest(HERE / name)
            for name in ("analytic_corollaries.py", "independent_replay.py")
        },
        "prefix_jobs_consumed": list(JOBS[:2]),
    }
    path = LOCAL / "contract.json"
    write_once(path, document)
    for name in REMAINING:
        write_once(HERE / (name + "_start.json"), {
            "job": name, "contract_sha256": digest(HERE / "contract.json"),
            "continuation_contract_sha256": digest(path), "limits": LIMITS,
            "counts_against_six_jobs": True, "reservation_not_process_launch": True,
        })
    print("Continuation frozen; four original slots reserved, none added.")


def continuation():
    contract()
    document = json.loads((LOCAL / "contract.json").read_text())
    if document["remaining_jobs"] != list(REMAINING) or document["limits"] != LIMITS:
        raise ValueError("continuation changes the approved budget")
    if document["original_contract_sha256"] != digest(HERE / "contract.json"):
        raise ValueError("original contract changed")
    for name, sha in document["source_sha256"].items():
        if digest(LOCAL / name) != sha:
            raise ValueError(f"frozen continuation source changed: {name}")
    for name, sha in document["additional_checker_sha256"].items():
        if digest(HERE / name) != sha:
            raise ValueError(f"frozen continuation checker changed: {name}")
    if digest(ROOT / "A6_GATE_REDUCTION_v1.md") != document["reduction_sha256"]:
        raise ValueError("prospective gate-reduction proof changed")
    return document


def worker(name):
    ready = HERE / (name + "_ready.json")
    until = time.monotonic() + 10
    while not ready.exists():
        if time.monotonic() >= until:
            raise TimeoutError("no assigned-memory/deadline handshake")
        time.sleep(0.05)
    handshake = json.loads(ready.read_text())
    if handshake["pid"] != os.getpid() or handshake["memory_job_assigned"] is not True:
        raise ValueError("invalid supervisor handshake")
    continuation()
    started = handshake["deadline_monotonic"] - LIMITS["solver_timeout_seconds"]
    if time.monotonic() >= handshake["deadline_monotonic"]:
        raise TimeoutError("whole-process deadline already exhausted")
    if name.startswith("f2"):
        from a6_decision_v1.continuation_v2.compact import run
    else:
        from a6_decision_v1.search import run
    try:
        report = run(name, started, LIMITS)
    except (TimeoutError, MemoryError) as error:
        report = {"job": name, "resource_exhausted": type(error).__name__,
                  "error": str(error), "certified": False, "training": False}
    write_once(HERE / (name + "_worker.json"), normalize_counts(report))
    print(json.dumps(report, indent=2))


def terminate_job(memory):
    memory.kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    if not memory.kernel.TerminateJobObject(memory.handle, 124):
        raise ctypes.WinError(ctypes.get_last_error())


def run_all():
    continuation()
    lock = LOCAL / "supervisor.lock"
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps({"pid": os.getpid(), "contract_sha256": digest(LOCAL / "contract.json")}))
        stream.flush()
        stream.close()
        try:
            for name in REMAINING:
                result_path = HERE / (name + "_result.json")
                launch = LOCAL / (name + "_launch.json")
                if result_path.exists():
                    continue
                if launch.exists():
                    raise RuntimeError(f"unclosed launched job: {name}; never advance or restart")
                memory = MemoryJob(LIMITS["memory_bytes"])
                ready = HERE / (name + "_ready.json")
                process = None
                started = time.monotonic()
                deadline = started + LIMITS["solver_timeout_seconds"]
                write_once(launch, {"job": name, "deadline_monotonic": deadline,
                                    "continuation_contract_sha256": digest(LOCAL / "contract.json")})
                env = os.environ.copy()
                for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                            "NUMEXPR_NUM_THREADS"):
                    env[key] = "1"
                try:
                    with (HERE / (name + ".log")).open("x", encoding="utf-8") as log:
                        process = subprocess.Popen(
                            [sys.executable, "-B", "-m",
                             "a6_decision_v1.continuation_v2.runner", "--worker", name],
                            cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
                        try:
                            memory.assign(process.pid)
                        except OSError:
                            process.terminate()
                            process.wait(timeout=10)
                            raise
                        write_once(ready, {"pid": process.pid, "memory_job_assigned": True,
                                           "deadline_monotonic": deadline})
                        print(f"Started {name}, PID {process.pid}; exclusive supervisor/absolute deadline", flush=True)
                        try:
                            code = process.wait(timeout=max(0.001, deadline - time.monotonic()))
                            state = ("completed" if code == 0 and
                                     (HERE / (name + "_worker.json")).is_file() else "worker_error")
                        except subprocess.TimeoutExpired:
                            terminate_job(memory)
                            process.wait(timeout=10)
                            state, code = "watchdog_exhausted", None
                        worker_elapsed = time.monotonic() - started
                        peak = memory.peak()
                finally:
                    memory.close()
                    if process is not None:
                        process.wait(timeout=10)
                    if ready.exists():
                        ready.unlink()
                write_once(result_path, {
                    "job": name, "pid": process.pid, "state": state, "exit_code": code,
                    "elapsed_seconds": worker_elapsed, "peak_job_committed_bytes": peak,
                    "memory_limit_enforced": True, "watchdog_enforced": True,
                    "absolute_deadline_used": True,
                    "observed_within_cutoff": worker_elapsed <= LIMITS["solver_timeout_seconds"],
                    "exclusive_supervisor": True, "thread_options": 1,
                    "counts_against_six_jobs": True, "training": False,
                    "continuation_contract_sha256": digest(LOCAL / "contract.json"),
                })
                print(f"Closed {name}: {state}, elapsed={worker_elapsed:.3f}", flush=True)
                if state == "worker_error":
                    raise RuntimeError(f"{name} failed; investigate its log before advancing")
        finally:
            lock.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--freeze", action="store_true")
    action.add_argument("--run", action="store_true")
    action.add_argument("--worker", choices=REMAINING)
    args = parser.parse_args()
    if args.freeze:
        freeze()
    elif args.run:
        run_all()
    else:
        worker(args.worker)
