"""Stage S0 checks. A failure returns before any class-fit quantity is computed."""

from __future__ import annotations

import os
import platform
import resource
import sys
from pathlib import Path

from ckappa_oracle.io import PackageStop, integrity_stop
from ckappa_classfit.gate import sha256_file
from ckappa_classfit.outputs_gate import index_refusal, output_dir_state, outputs_refusal
from ckappa_classfit.pinned import (
    ANNEX_V1_SHA256,
    ANNEX_V2_SHA256,
    ANNEX_V3_SHA256,
    ARRAY_COMMIT,
    CONSULT36_SHA256,
    CONSULT37_SHA256,
    CONSULT38_SHA256,
    CONSULT39_SHA256,
    DRAWN_ARRAYS_FILE_SHA256,
    FROZEN_RUNTIME,
    NUMPY,
    ORACLE_IMPORTED_MODULES,
    ORACLE_IMPORTED_SHA256,
    PACKAGE_BUDGET_BYTES,
    PROTOCOL_SHA256,
    PYTHON,
    RESULTS_JSON_SHA256,
    RESULTS_MD_SHA256,
    SCOPE_SHA256,
    STAGE_O7_FILE_SHA256,
)
from ckappa_classfit.schedule import DECLARED_N_O1, SCHEDULED_FLOAT, check_schedule_arithmetic

MANIFEST_NAME = "classfit_manifest.json"
OUTPUT_DIR_NAME = "classfit_outputs"
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


def outputs_directory_state(root: Path) -> str:
    """RL-9 / B-6. lstat. A symlink is not followed."""
    reason = outputs_refusal(root)
    if reason is not None:
        return reason
    return output_dir_state(root)


def check_outputs_directory(root: Path) -> str:
    """RL-5 and RL-9. Absent or empty real directory, and no existing post-run index."""
    state = outputs_directory_state(root)
    index_state = index_refusal(root)
    if state in ("absent", "empty") and index_state is None:
        return state
    integrity_stop(
        "classfit_outputs is not absent or empty",
        state=state,
        post_run_index=index_state,
        path=OUTPUT_DIR_NAME,
    )
    return state


def _status_kib_bytes(text: str | None) -> int | None:
    if text is None:
        return None
    parts = text.split()
    if len(parts) != 2 or parts[1] != "kB":
        return None
    return int(parts[0]) * 1024


def read_address_space() -> dict:
    """VmPeak is the virtual-address high-water mark. RSS fields are context only."""
    status = {}
    try:
        with open("/proc/self/status", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith(("VmPeak:", "VmHWM:", "VmRSS:")):
                    key, rest = line.split(":", 1)
                    status[key] = rest.strip()
    except OSError:
        status = {}
    rss_kb = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    vmpeak = status.get("VmPeak")
    return {
        "VmPeak": vmpeak,
        "VmPeak_source": "/proc/self/status",
        "vmpeak_bytes": _status_kib_bytes(vmpeak),
        "VmHWM": status.get("VmHWM"),
        "VmRSS": status.get("VmRSS"),
        "ru_maxrss_kb": rss_kb,
        "ru_maxrss_bytes": rss_kb * 1024,
        "ru_maxrss_source": "resource.getrusage(RUSAGE_SELF).ru_maxrss; Linux reports KiB",
        "rss_role": "context only; the RLIMIT_AS comparison uses VmPeak",
    }


def address_space_exceeds(vmpeak_bytes: int, budget_bytes: int, cap_bytes: int) -> bool:
    """True when VmPeak + package budget is above RLIMIT_AS. RSS is not an argument."""
    return vmpeak_bytes + budget_bytes > cap_bytes


def check_b0_budget() -> dict:
    """RL-4. Re-measure B0 as VmPeak and stop if VmPeak + package budget exceeds 4e9 B."""
    observed = read_address_space()
    cap = int(FROZEN_RUNTIME["memory_bytes"])
    vmpeak = observed["vmpeak_bytes"]
    if vmpeak is None:
        integrity_stop("VmPeak was not measured", VmPeak=observed.get("VmPeak"))
    total = vmpeak + PACKAGE_BUDGET_BYTES
    observed.update(
        {
            "package_budget_bytes": PACKAGE_BUDGET_BYTES,
            "rlimit_as_bytes": cap,
            "vmpeak_plus_budget_bytes": total,
            "comparison": "VmPeak + package_budget against RLIMIT_AS",
            "within_cap": not address_space_exceeds(vmpeak, PACKAGE_BUDGET_BYTES, cap),
        }
    )
    if address_space_exceeds(vmpeak, PACKAGE_BUDGET_BYTES, cap):
        integrity_stop("B0 VmPeak plus package budget exceeds RLIMIT_AS", **observed)
    return observed


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
    # RL-8. Schedule arithmetic errors are INTEGRITY STOP, and the check runs at S0.
    check_schedule_arithmetic()


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


# RL-9 / M-1. Exact path and sha. Annex v4 is required. There is no fallback.
ANNEX_V4_PATH = "review/ckappa_classfit/ckappa_classfit_implementation_annex_v4.md"
REQUIRED_GOVERNING = {
    "review/ckappa_classfit/astra_consult39_response.txt": CONSULT39_SHA256,
    "review/ckappa_classfit/astra_consult38_response.txt": CONSULT38_SHA256,
    "review/ckappa_classfit/astra_consult37_response.txt": CONSULT37_SHA256,
    "review/ckappa/astra_consult36_response.txt": CONSULT36_SHA256,
    "review/ckappa_classfit/ckappa_classfit_synthetic_scope_record_v1_3.md": SCOPE_SHA256,
    ANNEX_V4_PATH: None,
    "review/ckappa_classfit/ckappa_classfit_implementation_annex_v3.md": ANNEX_V3_SHA256,
    "review/ckappa_classfit/ckappa_classfit_implementation_annex_v2.md": ANNEX_V2_SHA256,
    "review/ckappa_classfit/ckappa_classfit_implementation_annex_v1.md": ANNEX_V1_SHA256,
    "review/ckappa/CKAPPA_SCOPE_GOVERNING_SET_RL.md": "6a5e0f24995a1349664349713e1ee0a550267ac06ab0e4b462b121d931c15c63",
    "review/ckappa/ckappa_oracle_scope_v1_4_N_closure_note.md": "4ad1d217aaab0bd45d2be6fd3e24872a4b22407d0c8abc2fa36a5a1ac7c45c9c",
    "review/ckappa/ckappa_oracle_scope_record_v1_4_N.md": "3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359",
    "review/ckappa/ckappa_oracle_scope_record_v1_3_E36.md": "f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5",
    "review/ckappa/ckappa_oracle_scope_record_v1_2.md": "7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d",
    "review/ckappa/ckappa_oracle_scope_record_v1_1.md": "e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c",
}


def check_application_hash(root: Path, application: dict) -> str:
    """C8.6. Hash application.path and compare it to application.sha256.

    A missing file or a mismatch is INTEGRITY STOP. The draft manifest keeps
    both fields null until the application is filed; this check still runs.
    """
    path = None if not isinstance(application, dict) else application.get("path")
    expected = None if not isinstance(application, dict) else application.get("sha256")
    if not isinstance(path, str) or path == "":
        integrity_stop("standing-approval application path is missing")
    if not isinstance(expected, str) or len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected):
        integrity_stop("standing-approval application sha256 is missing")
    file = root / path
    if file.is_symlink() or not file.is_file():
        integrity_stop("standing-approval application file is missing", path=path)
    digest = sha256_file(file)
    if digest != expected:
        integrity_stop(
            "standing-approval application sha256 mismatch",
            path=path,
            found=digest,
            expected=expected,
        )
    return digest


def check_input_rows(manifest: dict) -> None:
    """M-1. items.inputs must match the pinned input constants."""
    rows = (manifest.get("items") or {}).get("inputs")
    if not isinstance(rows, list):
        integrity_stop("manifest inputs list is missing")
    expected = {
        (ARRAY_COMMIT, "outputs/drawn_arrays.npz"): DRAWN_ARRAYS_FILE_SHA256,
        (ARRAY_COMMIT, "outputs/stage_O7.json"): STAGE_O7_FILE_SHA256,
        (FROZEN_RUNTIME["input_commit"], "twostream_results_v1/results.json"): RESULTS_JSON_SHA256,
        (FROZEN_RUNTIME["input_commit"], "twostream_results_v1/RESULTS.md"): RESULTS_MD_SHA256,
        (FROZEN_RUNTIME["input_commit"], "TWOSTREAM_PROTOCOL_v1.md"): PROTOCOL_SHA256,
    }
    found = {}
    for entry in rows:
        if not isinstance(entry, dict):
            integrity_stop("input entry is incomplete")
        key = (entry.get("commit"), entry.get("path_at_commit"))
        sha = entry.get("sha256")
        if key in expected and sha != expected[key]:
            integrity_stop("input sha256 does not match the pinned constant", path=key[1], found=sha, expected=expected[key])
        if key in expected:
            found[key] = sha
    missing = sorted(path for (_commit, path) in expected if (_commit, path) not in found)
    if missing:
        integrity_stop("pinned inputs are missing from the manifest", missing=missing)


def assert_oracle_modules_loaded() -> None:
    """B-4. No ckappa_oracle module outside the imported set may be loaded."""
    extra = sorted(name for name in sys.modules if name.startswith("ckappa_oracle") and name not in ORACLE_IMPORTED_MODULES)
    if extra:
        integrity_stop("unexpected ckappa_oracle module is loaded", modules=extra)


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
    classfit_found = {f"ckappa_classfit/{path.name}" for path in (root / "ckappa_classfit").glob("*.py")}
    classfit_found.add("run_classfit_package.sh")
    classfit_listed = {path for path in expected if path.startswith("ckappa_classfit/") or path == "run_classfit_package.sh"}
    oracle_listed = {path: sha for path, sha in expected.items() if path.startswith("ckappa_oracle/")}
    other = sorted(set(expected) - classfit_listed - set(oracle_listed))
    if classfit_listed != classfit_found or set(oracle_listed) != set(ORACLE_IMPORTED_SHA256) or other:
        integrity_stop(
            "code file set does not match the manifest",
            missing_classfit=sorted(classfit_found - classfit_listed),
            extra_classfit=sorted(classfit_listed - classfit_found),
            missing_oracle=sorted(set(ORACLE_IMPORTED_SHA256) - set(oracle_listed)),
            extra_oracle=sorted(set(oracle_listed) - set(ORACLE_IMPORTED_SHA256)),
            other=other,
        )
    for relative, pinned_sha in ORACLE_IMPORTED_SHA256.items():
        if oracle_listed[relative] != pinned_sha:
            integrity_stop(
                "inherited oracle module sha does not match the pinned module",
                path=relative,
                manifest_sha=oracle_listed[relative],
                pinned_sha=pinned_sha,
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
    by_path = {}
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
        by_path[relative] = digest
        checked.append({"path": relative, "sha256": digest})
    for relative, pinned_sha in REQUIRED_GOVERNING.items():
        if relative not in by_path:
            integrity_stop("required governing file is missing", path=relative)
        if pinned_sha is not None and by_path[relative] != pinned_sha:
            integrity_stop(
                "required governing sha256 mismatch",
                path=relative,
                found=by_path[relative],
                expected=pinned_sha,
            )
    if ANNEX_V4_PATH not in by_path:
        integrity_stop("annex v4 entry is missing", path=ANNEX_V4_PATH)
    assert_oracle_modules_loaded()
    check_input_rows(manifest)
    return {"implementation": expected, "governing": checked}


def preflight(root: Path) -> tuple[float, dict, dict]:
    outputs_state = check_outputs_directory(root)
    check_threads()
    t0 = check_clock()
    affinity = check_affinity()
    limits = check_memory()
    check_no_gpu()
    observed = check_versions()
    check_schedule_constants()
    manifest = load_manifest(root)
    check_application_hash(root, manifest.get("standing_approval_application") or {})
    hashes = check_sealed_hashes(root, manifest)
    b0 = check_b0_budget()
    observation = {
        "runtime_observed": observed,
        "runtime_observed_source": "platform.python_version and numpy.__version__ at preflight",
        "rlimit_as_observed": {"soft": limits[0], "hard": limits[1]},
        "cpu_affinity_observed": affinity,
        "classfit_outputs_state": outputs_state,
        "b0": b0,
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
