"""Clock, propagation counter, and phi cache for one run."""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from ckappa_oracle.io import PackageStop, atomic_write_json, atomic_write_text
from ckappa_oracle.pinned import FROZEN_RUNTIME
from ckappa_oracle.schedule import SCHEDULED_FLOAT
from ckappa_oracle.world import phi_float

SOFT_DEADLINE = int(FROZEN_RUNTIME["soft_deadline_seconds"])
SAMPLE_N = int(FROZEN_RUNTIME["sample_propagations"])


class Run:
    def __init__(self, root: Path, t0: float, log_path: Path):
        self.root = root
        self.outputs = root / "outputs"
        self.outputs.mkdir(parents=True, exist_ok=True)
        self.t0 = t0
        self.log_path = log_path
        self.log_handle = open(log_path, "w", encoding="utf-8")
        self.float_count = 0
        self.exact_count = 0
        self.bucket = {
            "O2": 0,
            "O6": 0,
            "O7": 0,
            "O5": 0,
            "true_baseline": 0,
            "O7_baseline": 0,
        }
        self.cache = {}
        self.transition = None
        self.sample_n = 0
        self.sample_seconds = 0.0
        self.sample_closed = False
        self.retained = []
        self.on_sample = None
        self.t_o1 = None
        self.n_o1 = None
        self.projection = None
        self.stages = {}
        self.completed = []
        self.drawn_records = []

    def close(self) -> None:
        self.log_handle.flush()
        self.log_handle.close()

    def elapsed(self) -> float:
        return time.time() - self.t0

    def log(self, message: str) -> None:
        line = f"{self.elapsed():.6f} {message}\n"
        self.log_handle.write(line)
        self.log_handle.flush()

    def check_deadline(self, stage: str) -> None:
        elapsed = self.elapsed()
        if elapsed >= SOFT_DEADLINE:
            raise PackageStop(
                "CAP RESERVE REACHED",
                4,
                {"stage_not_started": stage, "t_elapsed": elapsed, "soft_deadline_s": SOFT_DEADLINE},
            )

    def bump_exact(self, n: int = 1) -> None:
        self.exact_count += n

    def _note_float(self, bucket: str, dt: float, key, q: np.ndarray) -> None:
        self.float_count += 1
        self.bucket[bucket] = self.bucket.get(bucket, 0) + 1
        if self.float_count > SCHEDULED_FLOAT:
            raise PackageStop(
                "PIPELINE INVALID",
                2,
                {
                    "reason": "float propagation count exceeded the frozen schedule",
                    "float_count": self.float_count,
                    "scheduled_float": SCHEDULED_FLOAT,
                },
            )
        if bucket == "O6" and not self.sample_closed:
            self.sample_n += 1
            self.sample_seconds += dt
            self.retained.append(
                {
                    "i": self.sample_n,
                    "key": list(key) if isinstance(key, tuple) else key,
                    "q": [float(value) for value in q],
                }
            )
            if self.sample_n == SAMPLE_N:
                self.sample_closed = True
                if self.on_sample is not None:
                    self.on_sample()

    def phi(self, theta: np.ndarray, u: int, bucket: str, key):
        started = time.perf_counter()
        q, belief = phi_float(theta, u, self.transition)
        dt = time.perf_counter() - started
        self._note_float(bucket, dt, key, q)
        return q, belief

    def phi_cached(self, key, theta: np.ndarray, u: int, bucket: str):
        found = self.cache.get(key)
        if found is not None:
            return found
        q, belief = self.phi(theta, u, bucket, key)
        self.cache[key] = (q, belief)
        return q, belief

    def project(self) -> None:
        if self.sample_n != SAMPLE_N:
            raise PackageStop(
                "STEP 0 SAMPLE SHORT",
                6,
                {"sample_n": self.sample_n, "required": SAMPLE_N},
            )
        completed = self.float_count
        n_float = SCHEDULED_FLOAT - completed
        # N_exact remaining is 0, so the exact-rate term is omitted.
        t_rem = (n_float / float(SAMPLE_N)) * self.sample_seconds
        t_elapsed = self.elapsed()
        limit = SOFT_DEADLINE - t_elapsed
        self.projection = {
            "t_sample_s": self.sample_seconds,
            "sample_n": self.sample_n,
            "T_O1_s": self.t_o1,
            "n_O1": self.n_o1,
            "float_completed": completed,
            "N_float_remaining": n_float,
            "N_exact_remaining": 0,
            "T_rem_s": t_rem,
            "T_elapsed_s": t_elapsed,
            "projection_limit_s": limit,
            "bucket": dict(self.bucket),
        }
        if t_rem > limit:
            raise PackageStop("PROJECTION HALT", 3, dict(self.projection))

    def write_json(self, relative: str, obj) -> None:
        atomic_write_json(self.root / relative, obj)

    def write_stage(self, stage: str, obj) -> None:
        payload = dict(obj)
        payload["stage"] = stage
        self.stages[stage] = payload
        self.write_json(f"outputs/stage_{stage}.json", payload)
        if stage not in self.completed:
            self.completed.append(stage)
        self.log(f"stage {stage} written")


def write_stop(root: Path, kind: str, exit_code: int) -> None:
    atomic_write_json(
        root / "outputs" / "stop_kind.json",
        {"stop_kind": kind, "exit_code": exit_code},
    )


def write_log_line(path: Path, message: str) -> None:
    atomic_write_text(path, message)
