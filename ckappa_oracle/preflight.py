"""Startup checks. A failure returns before any oracle quantity is computed."""

from __future__ import annotations

import os
import platform
import resource
from pathlib import Path

from ckappa_oracle.io import PackageStop
from ckappa_oracle.pinned import FROZEN_RUNTIME, NUMPY, PYTHON
from ckappa_oracle.schedule import (
    DECLARED_N_O1,
    SCHEDULED_EXACT_REMAINING,
    SCHEDULED_FLOAT,
)


def _fail(reason: str, **detail) -> None:
    payload = {"reason": reason}
    payload.update(detail)
    raise PackageStop("PREFLIGHT FAILED", 5, payload)


def check_threads() -> None:
    for name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        value = os.environ.get(name)
        if value != "1":
            _fail("thread environment", variable=name, value=value)


def check_clock() -> float:
    raw = os.environ.get("CKAPPA_T0")
    if raw is None or raw == "":
        _fail("CKAPPA_T0 is unset")
    try:
        t0 = float(raw)
    except ValueError:
        _fail("CKAPPA_T0 is not a float", value=raw)
    if t0 <= 0.0:
        _fail("CKAPPA_T0 is not positive", value=raw)
    return t0


def check_affinity() -> None:
    affinity = os.sched_getaffinity(0)
    if affinity != {0}:
        _fail("CPU affinity", affinity=sorted(affinity))


def check_memory() -> None:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    expected = int(FROZEN_RUNTIME["memory_bytes"])
    if soft != expected or hard != expected:
        _fail("RLIMIT_AS", soft=soft, hard=hard, expected=expected)


def check_versions() -> None:
    import numpy

    if platform.python_version() != PYTHON:
        _fail("python version", found=platform.python_version(), expected=PYTHON)
    if numpy.__version__ != NUMPY:
        _fail("numpy version", found=numpy.__version__, expected=NUMPY)


def check_schedule_constants() -> None:
    if SCHEDULED_FLOAT != int(FROZEN_RUNTIME["scheduled_float_propagations"]):
        _fail("scheduled float count drifted")
    if DECLARED_N_O1 != int(FROZEN_RUNTIME["declared_n_o1"]):
        _fail("declared n_O1 drifted")
    if SCHEDULED_EXACT_REMAINING != int(FROZEN_RUNTIME["scheduled_exact_remaining"]):
        _fail("scheduled exact remaining drifted")


def load_manifest(root: Path) -> dict:
    path = root / "manifest.json"
    if not path.is_file():
        draft = root / "manifest_DRAFT.json"
        draft_note = "present" if draft.is_file() else "absent"
        _fail("sealed manifest.json is absent", manifest_DRAFT=draft_note)
    import json

    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _fail("manifest.json is not JSON", error=str(exc))
    if manifest.get("sealed") is not True:
        _fail("manifest is not sealed")
    application = manifest.get("standing_approval_application") or {}
    sha = application.get("sha256")
    if not isinstance(sha, str) or len(sha) != 64 or any(ch not in "0123456789abcdef" for ch in sha):
        _fail("standing-approval application sha is not a sha256 hex string")
    if application.get("status") == "PLACEHOLDER_NOT_FILED":
        _fail("standing-approval application is still a placeholder")
    runtime = manifest.get("frozen_runtime")
    if runtime != FROZEN_RUNTIME:
        _fail("manifest frozen_runtime does not match pinned constants")
    return manifest


def preflight(root: Path) -> tuple[float, dict]:
    check_threads()
    t0 = check_clock()
    check_affinity()
    check_memory()
    check_versions()
    check_schedule_constants()
    manifest = load_manifest(root)
    return t0, manifest
