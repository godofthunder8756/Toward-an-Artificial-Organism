"""Stage S0 checks. A failure returns before any class-fit quantity is computed."""

from __future__ import annotations

import os
import platform
import resource
import sys
from pathlib import Path

from ckappa_oracle.io import PackageStop, integrity_stop
from ckappa_classfit.gate import sha256_file
from ckappa_classfit.pinned import FROZEN_RUNTIME, NUMPY, PYTHON
from ckappa_classfit.schedule import DECLARED_N_O1, SCHEDULED_FLOAT

MANIFEST_NAME = "classfit_manifest.json"
FORBIDDEN_MODULES = ("torch", "cupy", "tensorflow")


def _fail(reason: str, **detail) -> None:
    payload = {"reason": reason}
    payload.update(detail)
    raise PackageStop("PREFLIGHT FAILED", 5, payload)


def check_threads() -> None:
    for name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        if os.environ.get(name) != "1":
            _fail("thread environment", variable=name, value=os.environ.get(name))


def check_clock() -> float:
    raw = os.environ.get("CKAPPA_CLASSFIT_T0")
    if raw is None or raw == "":
        _fail("CKAPPA_CLASSFIT_T0 is unset")
    try:
        t0 = float(raw)
    except ValueError:
        _fail("CKAPPA_CLASSFIT_T0 is not a float", value=raw)
    if t0 <= 0.0:
        _fail("CKAPPA_CLASSFIT_T0 is not positive", value=raw)
    return t0


def check_affinity() -> list:
    affinity = os.sched_getaffinity(0)
    if affinity != {0}:
        _fail("CPU affinity", affinity=sorted(affinity))
    return sorted(affinity)


def check_memory() -> tuple:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    expected = int(FROZEN_RUNTIME["memory_bytes"])
    if soft != expected or hard != expected:
        _fail("RLIMIT_AS", soft=soft, hard=hard, expected=expected)
    return soft, hard


def check_no_gpu() -> None:
    present = [name for name in FORBIDDEN_MODULES if name in sys.modules]
    if present:
        integrity_stop("GPU library is imported", modules=present)


def check_versions() -> dict:
    import numpy

    observed = {"python": platform.python_version(), "numpy": numpy.__version__}
    if observed["python"] != PYTHON or observed["numpy"] != NUMPY:
        integrity_stop(
            "runtime-version mismatch",
            observed=observed,
            pinned={"python": PYTHON, "numpy": NUMPY},
        )
    return observed


def check_schedule_constants() -> None:
    if SCHEDULED_FLOAT != int(FROZEN_RUNTIME["classfit_scheduled_float_propagations"]):
        _fail("scheduled float count drifted")
    if DECLARED_N_O1 != int(FROZEN_RUNTIME["classfit_declared_n_o1"]):
        _fail("declared n_O1 drifted")
    if int(FROZEN_RUNTIME["scheduled_float_propagations"]) == SCHEDULED_FLOAT:
        _fail("inherited oracle schedule was overwritten")


def load_manifest(root: Path) -> dict:
    path = root / MANIFEST_NAME
    if not path.is_file():
        _fail("classfit manifest is absent", path=MANIFEST_NAME)
    import json

    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _fail("classfit manifest is not JSON", error=str(exc))
    if manifest.get("sealed") is not True:
        _fail("manifest field sealed is not true")
    application = manifest.get("standing_approval_application")
    if not isinstance(application, dict):
        _fail("standing-approval application is missing")
    sha = application.get("sha256")
    if not isinstance(sha, str) or len(sha) != 64 or any(ch not in "0123456789abcdef" for ch in sha):
        _fail("standing-approval application sha is not a sha256 hex string")
    if application.get("status") in (None, "PENDING", "PLACEHOLDER_NOT_FILED"):
        _fail("standing-approval application is not filed", status=application.get("status"))
    if manifest.get("frozen_runtime") != FROZEN_RUNTIME:
        _fail("manifest frozen_runtime does not match pinned constants")
    return manifest


def check_sealed_hashes(root: Path, manifest: dict) -> dict:
    item = (manifest.get("items") or {}).get("implementation") or {}
    listed = item.get("implementation_files")
    if not isinstance(listed, list) or not listed:
        integrity_stop("manifest implementation_files is missing")
    expected = {}
    for entry in listed:
        path = entry.get("path")
        sha = entry.get("sha256")
        if not isinstance(path, str) or not isinstance(sha, str):
            integrity_stop("implementation file entry is incomplete")
        expected[path] = sha
    found = {f"ckappa_classfit/{path.name}" for path in (root / "ckappa_classfit").glob("*.py")}
    found.add("run_classfit_package.sh")
    if set(expected) != found:
        integrity_stop(
            "code file set does not match the manifest",
            missing=sorted(found - set(expected)),
            extra=sorted(set(expected) - found),
        )
    for relative, sha in expected.items():
        path = root / relative
        if not path.is_file():
            integrity_stop("code file missing", path=relative)
        digest = sha256_file(path)
        if digest != sha:
            integrity_stop("code file sha256 mismatch", path=relative, found=digest, expected=sha)
    governing = (manifest.get("items") or {}).get("governing") or []
    if not isinstance(governing, list) or not governing:
        integrity_stop("manifest governing list is missing")
    checked = []
    for entry in governing:
        relative = entry.get("path")
        sha = entry.get("sha256")
        if not isinstance(relative, str) or not isinstance(sha, str):
            integrity_stop("governing entry is incomplete")
        path = root / relative
        if not path.is_file():
            integrity_stop("governing file missing", path=relative)
        digest = sha256_file(path)
        if digest != sha:
            integrity_stop("governing file sha256 mismatch", path=relative, found=digest, expected=sha)
        checked.append({"path": relative, "sha256": digest})
    return {"implementation": expected, "governing": checked}


def preflight(root: Path) -> tuple[float, dict, dict]:
    check_threads()
    t0 = check_clock()
    affinity = check_affinity()
    limits = check_memory()
    check_no_gpu()
    observed = check_versions()
    check_schedule_constants()
    manifest = load_manifest(root)
    hashes = check_sealed_hashes(root, manifest)
    observation = {
        "runtime_observed": observed,
        "runtime_observed_source": "platform.python_version and numpy.__version__ at preflight",
        "rlimit_as_observed": {"soft": limits[0], "hard": limits[1]},
        "cpu_affinity_observed": affinity,
        "sealed": manifest.get("sealed"),
        "input_allow_list": sorted(
            [
                f"{FROZEN_RUNTIME['array_commit']}:outputs/drawn_arrays.npz",
                f"{FROZEN_RUNTIME['array_commit']}:outputs/stage_O7.json",
                f"{FROZEN_RUNTIME['input_commit']}:twostream_results_v1/results.json",
                f"{FROZEN_RUNTIME['input_commit']}:twostream_results_v1/RESULTS.md",
                f"{FROZEN_RUNTIME['input_commit']}:TWOSTREAM_PROTOCOL_v1.md",
            ]
        ),
        "hashes": hashes,
    }
    return t0, manifest, observation
