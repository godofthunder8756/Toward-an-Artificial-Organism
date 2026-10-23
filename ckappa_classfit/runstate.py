"""Clock, propagation counter, and durable COUNTERS lines for one class-fit run.

Writes only under classfit_outputs/. The oracle outputs/ directory is not used.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import numpy as np

from ckappa_oracle.io import PackageStop, atomic_write_json, atomic_write_text, integrity_stop
from ckappa_oracle.world import phi_float
from ckappa_classfit.accounting import Ledger
from ckappa_classfit.outputs_gate import claim_output_dir
from ckappa_classfit.pinned import FROZEN_RUNTIME, SCHEDULED_FLOAT
from ckappa_classfit.schedule import SVDS

SOFT_DEADLINE = int(FROZEN_RUNTIME["soft_deadline_seconds"])
SAMPLE_N = int(FROZEN_RUNTIME["sample_propagations"])
OUTPUT_DIR = "classfit_outputs"


class Run:
    def __init__(self, root: Path, t0: float):
        self.root = root
        reason = claim_output_dir(root)
        if reason is not None:
            raise PackageStop(
                "INTEGRITY STOP",
                7,
                {"reason": "classfit_outputs refused", "outputs": reason},
            )
        self.outputs = root / OUTPUT_DIR
        self.outputs.mkdir(parents=True, exist_ok=True)
        self.t0 = t0
        self.t0_source = "CKAPPA_CLASSFIT_T0"
        self.log_path = self.outputs / "run.log"
        self.log_handle = open(self.log_path, "w", encoding="utf-8")
        self.float_count = 0
        self.exact_count = 0
        self.svd_count = 0
        self.ledger = Ledger()
        self.stopped = False
        self.sample_n = 0
        self.sample_seconds = 0.0
        self.sample_closed = False
        self.retained = []
        self.projection = None
        self.transition = None
        self.t_o1 = None
        self.n_o1 = None

    def close(self) -> None:
        self.log_handle.flush()
        try:
            os.fsync(self.log_handle.fileno())
        except OSError:
            pass
        self.log_handle.close()

    def elapsed(self) -> float:
        return time.time() - self.t0

    def log(self, message: str) -> None:
        self.log_handle.write(f"{self.elapsed():.6f} {message}\n")
        self.log_handle.flush()

    def checkpoint(self, label: str) -> None:
        payload = {
            "label": label,
            "t_elapsed_s": self.elapsed(),
            "t_elapsed_s_source": "time.time() minus " + self.t0_source,
            "float_propagations": self.float_count,
            "exact_propagations": self.exact_count,
            "svd_count": self.svd_count,
            "accounting": self.ledger.snapshot(),
        }
        line = "COUNTERS " + json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        self.log_handle.write(line)
        self.log_handle.flush()
        os.fsync(self.log_handle.fileno())

    def memory_observation(self) -> dict:
        import resource

        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        vmpeak = None
        try:
            with open("/proc/self/status", encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith("VmPeak:"):
                        vmpeak = line.strip()
                        break
        except OSError:
            vmpeak = None
        return {
            "ru_maxrss_kb": int(rss),
            "ru_maxrss_source": "resource.getrusage(RUSAGE_SELF).ru_maxrss",
            "VmPeak": vmpeak,
            "VmPeak_source": "/proc/self/status",
        }

    def check_deadline(self, stage: str) -> None:
        elapsed = self.elapsed()
        if elapsed >= SOFT_DEADLINE:
            self.stopped = True
            raise PackageStop(
                "CAP RESERVE REACHED",
                4,
                {
                    "stage_not_started": stage,
                    "t_elapsed_s": elapsed,
                    "t_elapsed_s_source": "time.time() minus " + self.t0_source,
                    "soft_deadline_s": SOFT_DEADLINE,
                },
            )

    def note_svd(self) -> None:
        self.svd_count += 1
        if self.svd_count > SVDS:
            integrity_stop(
                "SVD count exceeded the frozen schedule",
                svd_count=self.svd_count,
                scheduled_svd=SVDS,
            )

    def bump_exact(self, n: int = 1) -> None:
        self.exact_count += n
        if self.exact_count > int(FROZEN_RUNTIME["classfit_declared_n_o1"]):
            integrity_stop(
                "exact propagation count exceeded the frozen schedule",
                exact_count=self.exact_count,
            )

    def phi(self, theta: np.ndarray, u: int, bucket: str, key):
        if self.elapsed() >= SOFT_DEADLINE:
            self.stopped = True
            raise PackageStop(
                "CAP RESERVE REACHED",
                4,
                {
                    "during": bucket,
                    "t_elapsed_s": self.elapsed(),
                    "t_elapsed_s_source": "time.time() minus " + self.t0_source,
                    "soft_deadline_s": SOFT_DEADLINE,
                },
            )
        # RL-13 / NB-1. Order is fixed: overrun check, then count, then phi_float.
        # A stop here does not count the call. The count is already recorded
        # if phi_float later raises ValueError. The timing sample stays success-only.
        if self.float_count >= SCHEDULED_FLOAT:
            integrity_stop(
                "float propagation count exceeded the frozen schedule",
                float_count=self.float_count,
                scheduled_float=SCHEDULED_FLOAT,
            )
        self.float_count += 1
        started = time.perf_counter()
        forecast, belief = phi_float(theta, u, self.transition)
        dt = time.perf_counter() - started
        if bucket == "S6" and not self.sample_closed:
            self.sample_n += 1
            self.sample_seconds += dt
            finite = bool(np.all(np.isfinite(forecast)))
            self.retained.append(
                {
                    "i": self.sample_n,
                    "key": list(key) if isinstance(key, tuple) else key,
                    "q": [float(value) for value in forecast] if finite else None,
                }
            )
            if self.sample_n == SAMPLE_N:
                self.sample_closed = True
                self.project()
        return forecast, belief

    def project(self) -> None:
        if self.sample_n != SAMPLE_N:
            raise PackageStop(
                "STEP 0 SAMPLE SHORT",
                6,
                {"sample_n": self.sample_n, "required": SAMPLE_N},
            )
        completed = self.float_count
        n_float = SCHEDULED_FLOAT - completed
        t_rem = (n_float / float(SAMPLE_N)) * self.sample_seconds
        t_elapsed = self.elapsed()
        limit = SOFT_DEADLINE - t_elapsed
        self.projection = {
            "t_sample_s": self.sample_seconds,
            "t_sample_s_source": "sum of perf_counter intervals around the first 1000 stage-S6 Phi calls",
            "sample_n": self.sample_n,
            "T_O1_s": self.t_o1,
            "T_O1_s_source": "perf_counter around stage S1",
            "n_O1": self.n_o1,
            "float_completed": completed,
            "N_float_remaining": n_float,
            "N_float_remaining_definition": "classfit_scheduled_float_propagations minus float continuations already performed",
            "N_exact_remaining": 0,
            "T_rem_s": t_rem,
            "T_elapsed_s": t_elapsed,
            "T_elapsed_s_source": "time.time() minus " + self.t0_source,
            "projection_limit_s": limit,
        }
        if t_rem > limit:
            self.stopped = True
            raise PackageStop("PROJECTION HALT", 3, dict(self.projection))

    def write_json(self, name: str, obj) -> None:
        atomic_write_json(self.outputs / name, obj)

    def write_text(self, name: str, text: str) -> None:
        atomic_write_text(self.outputs / name, text)


def write_stop(root: Path, kind: str, exit_code: int) -> None:
    atomic_write_json(
        root / OUTPUT_DIR / "stop_kind.json",
        {"stop_kind": kind, "exit_code": exit_code},
    )
