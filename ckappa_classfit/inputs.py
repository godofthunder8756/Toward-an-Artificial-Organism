"""W2 inputs and the committed O7 coefficient vector, through the read gate."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from ckappa_oracle.io import integrity_stop
from ckappa_oracle.pinned import FROZEN_RUNTIME as ORACLE_FROZEN
from ckappa_classfit.gate import git_show, sha256_bytes
from ckappa_classfit.pinned import ARRAY_COMMIT, STAGE_O7_FILE_SHA256

_PATHS = {
    "results.json": (
        f"{ORACLE_FROZEN['input_commit']}:twostream_results_v1/results.json",
        ORACLE_FROZEN["results_json_sha256"],
    ),
    "RESULTS.md": (
        f"{ORACLE_FROZEN['input_commit']}:twostream_results_v1/RESULTS.md",
        ORACLE_FROZEN["results_md_sha256"],
    ),
    "TWOSTREAM_PROTOCOL_v1.md": (
        f"{ORACLE_FROZEN['input_commit']}:TWOSTREAM_PROTOCOL_v1.md",
        ORACLE_FROZEN["protocol_sha256"],
    ),
}


def _exact(field) -> Fraction:
    return Fraction(field["exact"])


def load_world_inputs(root: Path) -> dict:
    blobs = {}
    shas = {}
    for name, (spec, expected) in _PATHS.items():
        raw = git_show(root, spec)
        digest = sha256_bytes(raw)
        if digest != expected:
            integrity_stop("input sha256 mismatch", name=name, found=digest, expected=expected)
        blobs[name] = raw
        shas[name] = digest
    payload = json.loads(blobs["results.json"].decode("utf-8"))
    if payload.get("certificate") != ORACLE_FROZEN["certificate"]:
        integrity_stop("certificate field mismatch")
    if payload.get("freeze_commit") != ORACLE_FROZEN["freeze_commit"]:
        integrity_stop("freeze_commit mismatch")
    if payload.get("freeze_file_sha256") != ORACLE_FROZEN["freeze_file_sha256"]:
        integrity_stop("freeze_file_sha256 mismatch")
    rows = payload.get("per_history")
    if payload.get("history_count") != 256 or not isinstance(rows, list) or len(rows) != 256:
        integrity_stop("history_count is not 256")
    by_history = {}
    for row in rows:
        history = int(row["history"])
        bits = row["bits"]
        expected_bits = "".join(str((history >> t) & 1) for t in range(8))
        if bits != expected_bits:
            integrity_stop("history bit string mismatch", history=history)
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
        integrity_stop("duplicate history index")
    return {"by_history": by_history, "input_shas": shas}


def load_committed_g(root: Path) -> dict:
    spec = f"{ARRAY_COMMIT}:outputs/stage_O7.json"
    raw = git_show(root, spec)
    digest = sha256_bytes(raw)
    if digest != STAGE_O7_FILE_SHA256:
        integrity_stop("stage_O7.json sha256 mismatch", found=digest, expected=STAGE_O7_FILE_SHA256)
    payload = json.loads(raw.decode("utf-8"))
    coef = payload.get("g_coefficients")
    if not isinstance(coef, list) or len(coef) != 6:
        integrity_stop("committed g_coefficients missing")
    return {"g_coefficients": [float(value) for value in coef], "sha256": digest}
