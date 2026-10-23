"""Enumerated reads. No checkpoint or weight file is opened (C1.2, C9.3)."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

from ckappa_oracle.io import integrity_stop
from ckappa_classfit.pinned import ARRAY_COMMIT
from ckappa_oracle.pinned import FROZEN_RUNTIME as ORACLE_FROZEN

INPUT_COMMIT = ORACLE_FROZEN["input_commit"]

ALLOWED_GIT = frozenset(
    {
        f"{ARRAY_COMMIT}:outputs/drawn_arrays.npz",
        f"{ARRAY_COMMIT}:outputs/stage_O7.json",
        f"{ARRAY_COMMIT}:outputs/drawn_array_hashes.json",
        f"{INPUT_COMMIT}:twostream_results_v1/results.json",
        f"{INPUT_COMMIT}:twostream_results_v1/RESULTS.md",
        f"{INPUT_COMMIT}:TWOSTREAM_PROTOCOL_v1.md",
    }
)

# Substrings that identify a checkpoint or weight file. A spec containing one
# of these is refused even if it were added to the allow-list by mistake.
FORBIDDEN_PARTS = (
    "checkpoint",
    "weight",
    ".pt",
    ".pth",
    ".ckpt",
    ".safetensors",
    "state_dict",
    ".bin",
)


def assert_spec_allowed(spec: str) -> None:
    lowered = spec.lower()
    for part in FORBIDDEN_PARTS:
        if part in lowered:
            integrity_stop("refused checkpoint or weight path", spec=spec, part=part)
    if spec not in ALLOWED_GIT:
        integrity_stop("git spec is not in the enumerated input set", spec=spec)


def git_show(root: Path, spec: str) -> bytes:
    assert_spec_allowed(spec)
    proc = subprocess.run(
        ["git", "-C", str(root), "show", spec],
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        integrity_stop(
            "git show failed",
            spec=spec,
            stderr=proc.stderr.decode("utf-8", "replace")[:500],
        )
    return proc.stdout


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()
