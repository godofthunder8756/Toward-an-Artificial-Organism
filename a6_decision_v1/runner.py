"""One-thread Windows job-object supervisor for the six approved A6 jobs."""

from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

from a6_decision_v1.preservation import ROOT, digest, head, verify, write_once

HERE = Path(__file__).resolve().parent
JOBS = ("f1_positive", "f1_negative", "f2_positive", "f2_negative",
        "f3_bank", "f3_singleton")
LIMITS = {"node_limit": 100000, "solver_timeout_seconds": 900,
          "memory_bytes": 4 * 1024**3, "threads": 1, "cut_limit": 10000,
          "candidate_limit": 8}


class BasicLimits(ctypes.Structure):
    _fields_ = [
        ("process_time", ctypes.c_int64), ("job_time", ctypes.c_int64),
        ("flags", wintypes.DWORD), ("minimum_working_set", ctypes.c_size_t),
        ("maximum_working_set", ctypes.c_size_t), ("active_processes", wintypes.DWORD),
        ("affinity", ctypes.c_size_t), ("priority", wintypes.DWORD),
        ("scheduling", wintypes.DWORD),
    ]


class IoCounters(ctypes.Structure):
    _fields_ = [(name, ctypes.c_uint64) for name in
                ("read_ops", "write_ops", "other_ops", "read_bytes", "write_bytes", "other_bytes")]


class ExtendedLimits(ctypes.Structure):
    _fields_ = [("basic", BasicLimits), ("io", IoCounters),
                ("process_memory", ctypes.c_size_t), ("job_memory", ctypes.c_size_t),
                ("peak_process_memory", ctypes.c_size_t), ("peak_job_memory", ctypes.c_size_t)]


class MemoryJob:
    def __init__(self, limit):
        if os.name != "nt":
            raise RuntimeError("this approved supervisor requires Windows Job Objects")
        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self.kernel.CreateJobObjectW.restype = wintypes.HANDLE
        self.kernel.SetInformationJobObject.argtypes = [
            wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        self.kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        self.kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.kernel.OpenProcess.restype = wintypes.HANDLE
        self.kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self.kernel.QueryInformationJobObject.argtypes = [
            wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
        self.handle = self.kernel.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        info = ExtendedLimits()
        info.basic.flags = 0x2000 | 0x200 | 0x100
        info.process_memory = info.job_memory = limit
        if not self.kernel.SetInformationJobObject(self.handle, 9, ctypes.byref(info), ctypes.sizeof(info)):
            error = ctypes.get_last_error()
            self.close()
            raise ctypes.WinError(error)

    def assign(self, pid):
        process = self.kernel.OpenProcess(0x0101, False, pid)
        if not process:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            if not self.kernel.AssignProcessToJobObject(self.handle, process):
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            self.kernel.CloseHandle(process)

    def peak(self):
        info = ExtendedLimits()
        if not self.kernel.QueryInformationJobObject(
                self.handle, 9, ctypes.byref(info), ctypes.sizeof(info), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return info.peak_job_memory

    def close(self):
        if self.handle:
            if not self.kernel.CloseHandle(self.handle):
                raise ctypes.WinError(ctypes.get_last_error())
            self.handle = None


def freeze():
    baseline = HERE / "baseline_hashes.json"
    preservation = verify(json.loads(baseline.read_text()))
    from a6_decision_v1.verify import verify_lemmas
    write_once(HERE / "lemmas.json", verify_lemmas())
    sources = sorted(HERE.glob("*.py")) + [HERE / "PROTOCOL.md"]
    contract = {
        "schema": 1, "head": head(), "executable": sys.executable,
        "python": platform.python_version(), "platform": platform.platform(),
        "dependencies": {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "torch")},
        "source_sha256": {p.name: digest(p) for p in sources},
        "baseline_sha256": digest(baseline), "preservation": preservation,
        "jobs": list(JOBS), "limits": LIMITS, "training": False,
    }
    write_once(HERE / "contract.json", contract)
    print(json.dumps(contract, indent=2))


def contract():
    document = json.loads((HERE / "contract.json").read_text())
    if document["schema"] != 1 or document["limits"] != LIMITS or document["jobs"] != list(JOBS):
        raise ValueError("approved resource contract changed")
    if document["head"] != head() or document["executable"] != sys.executable:
        raise ValueError("live HEAD/interpreter differs from analytic freeze")
    for name, sha in document["source_sha256"].items():
        if digest(HERE / name) != sha:
            raise ValueError(f"frozen analytic source changed: {name}")
    if digest(HERE / "baseline_hashes.json") != document["baseline_sha256"]:
        raise ValueError("preservation inventory changed")
    for name, version in document["dependencies"].items():
        if importlib.metadata.version(name) != version:
            raise ValueError(f"dependency changed: {name}")
    return document


def worker(name):
    ready = HERE / (name + "_ready.json")
    until = time.monotonic() + 10
    while not ready.exists():
        if time.monotonic() >= until:
            raise TimeoutError("worker never received resource-enforcement handshake")
        time.sleep(0.05)
    handshake = json.loads(ready.read_text())
    if handshake != {"pid": os.getpid(), "memory_job_assigned": True}:
        raise ValueError("invalid supervisor handshake")
    document = contract()
    started = time.monotonic()
    from a6_decision_v1.search import run
    try:
        result = run(name, started, document["limits"])
    except (TimeoutError, MemoryError) as error:
        result = {"job": name, "resource_exhausted": type(error).__name__,
                  "error": str(error), "certified": False, "training": False}
    write_once(HERE / (name + "_worker.json"), result)
    print(json.dumps(result, indent=2))


def run_all():
    document = contract()
    verify(json.loads((HERE / "baseline_hashes.json").read_text()))
    for name in JOBS:
        start = HERE / (name + "_start.json")
        result_path = HERE / (name + "_result.json")
        if start.exists():
            print(f"{name}: already consumed; never restarting", flush=True)
            continue
        memory = MemoryJob(LIMITS["memory_bytes"])
        write_once(start, {"job": name, "contract_sha256": digest(HERE / "contract.json"),
                           "limits": LIMITS, "counts_against_six_jobs": True})
        env = os.environ.copy()
        for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS"):
            env[key] = "1"
        started = time.monotonic()
        process = None
        ready = HERE / (name + "_ready.json")
        try:
            with (HERE / (name + ".log")).open("x", encoding="utf-8") as log:
                process = subprocess.Popen(
                    [sys.executable, "-B", "-m", "a6_decision_v1.runner", "--worker", name],
                    cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
                )
                try:
                    memory.assign(process.pid)
                except OSError:
                    process.terminate()
                    process.wait(timeout=10)
                    raise
                write_once(ready, {"pid": process.pid, "memory_job_assigned": True})
                print(f"Started {name}, PID {process.pid}; all limits enforced", flush=True)
                try:
                    code = process.wait(timeout=LIMITS["solver_timeout_seconds"])
                    state = ("completed" if code == 0 and
                             (HERE / (name + "_worker.json")).is_file() else "worker_error")
                except subprocess.TimeoutExpired:
                    state, code = "watchdog_exhausted", None
                peak = memory.peak()
        finally:
            memory.close()
            if process is not None:
                process.wait(timeout=10)
            if ready.exists():
                ready.unlink()
        result = {"job": name, "pid": process.pid, "state": state, "exit_code": code,
                  "elapsed_seconds": time.monotonic() - started,
                  "peak_job_committed_bytes": peak, "memory_limit_enforced": True,
                  "watchdog_enforced": True, "thread_options": 1,
                  "counts_against_six_jobs": True, "training": False}
        write_once(result_path, result)
        print(json.dumps(result), flush=True)
        if state == "worker_error":
            raise RuntimeError(f"{name} failed; inspect its log before any further discovery")
        worker_path = HERE / (name + "_worker.json")
        if worker_path.exists():
            report = json.loads(worker_path.read_text())
            if report.get("candidate_certification", {}).get("certified_gate_PASS", False):
                print("Candidate PASS requires separate solver-free replay; stopping discovery.")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--freeze", action="store_true")
    action.add_argument("--run", action="store_true")
    action.add_argument("--worker", choices=JOBS)
    args = parser.parse_args()
    if args.freeze:
        freeze()
    elif args.run:
        run_all()
    else:
        worker(args.worker)
