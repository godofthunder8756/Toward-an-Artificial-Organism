"""Load the frozen W2 inputs from commit 5d9d8a7 and check their hashes."""

from __future__ import annotations

import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

from ckappa_oracle.io import PackageStop
from ckappa_oracle.pinned import FROZEN_RUNTIME

COMMIT = FROZEN_RUNTIME["input_commit"]
_PATHS = {
    "results.json": (
        f"{COMMIT}:twostream_results_v1/results.json",
        FROZEN_RUNTIME["results_json_sha256"],
    ),
    "RESULTS.md": (
        f"{COMMIT}:twostream_results_v1/RESULTS.md",
        FROZEN_RUNTIME["results_md_sha256"],
    ),
    "TWOSTREAM_PROTOCOL_v1.md": (
        f"{COMMIT}:TWOSTREAM_PROTOCOL_v1.md",
        FROZEN_RUNTIME["protocol_sha256"],
    ),
}


def _git_bytes(root: Path, spec: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(root), "show", spec],
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise PackageStop(
            "PIPELINE INVALID",
            2,
            {"reason": "git show failed", "spec": spec, "stderr": proc.stderr.decode("utf-8", "replace")[:500]},
        )
    return proc.stdout


def _exact(field) -> Fraction:
    return Fraction(field["exact"])


def load_inputs(root: Path) -> dict:
    blobs = {}
    for name, (spec, expected) in _PATHS.items():
        raw = _git_bytes(root, spec)
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected:
            raise PackageStop(
                "PIPELINE INVALID",
                2,
                {"reason": "input sha256 mismatch", "name": name, "found": digest, "expected": expected},
            )
        blobs[name] = raw
    payload = json.loads(blobs["results.json"].decode("utf-8"))
    if payload.get("certificate") != FROZEN_RUNTIME["certificate"]:
        raise PackageStop("PIPELINE INVALID", 2, {"reason": "certificate field mismatch"})
    if payload.get("freeze_commit") != FROZEN_RUNTIME["freeze_commit"]:
        raise PackageStop("PIPELINE INVALID", 2, {"reason": "freeze_commit mismatch"})
    if payload.get("freeze_file_sha256") != FROZEN_RUNTIME["freeze_file_sha256"]:
        raise PackageStop("PIPELINE INVALID", 2, {"reason": "freeze_file_sha256 mismatch"})
    rows = payload.get("per_history")
    if payload.get("history_count") != 256 or not isinstance(rows, list) or len(rows) != 256:
        raise PackageStop("PIPELINE INVALID", 2, {"reason": "history_count is not 256"})
    by_history = {}
    for row in rows:
        history = int(row["history"])
        bits = row["bits"]
        expected_bits = "".join(str((history >> t) & 1) for t in range(8))
        if bits != expected_bits:
            raise PackageStop(
                "PIPELINE INVALID",
                2,
                {"reason": "history bit string mismatch", "history": history},
            )
        by_history[history] = {
            "probability": _exact(row["probability"]),
            "marginal_x": _exact(row["marginal_x"]),
            "marginal_y": _exact(row["marginal_y"]),
            "xor_joint": _exact(row["xor_joint"]),
            "probability_truncation_50": row["probability"]["decimal_truncation_50"],
            "marginal_x_truncation_50": row["marginal_x"]["decimal_truncation_50"],
            "marginal_y_truncation_50": row["marginal_y"]["decimal_truncation_50"],
            "xor_joint_truncation_50": row["xor_joint"]["decimal_truncation_50"],
        }
    if len(by_history) != 256:
        raise PackageStop("PIPELINE INVALID", 2, {"reason": "duplicate history index"})
    return {
        "by_history": by_history,
        "input_shas": {name: expected for name, (_spec, expected) in _PATHS.items()},
    }
