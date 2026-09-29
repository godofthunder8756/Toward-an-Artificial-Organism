"""Pre-engineering source snapshot; never an authorization by itself."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
import torch

from phase3b import execution
from phase3b.resources import grid
from phase3b import PRIMARY


def _canonical(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def create_preflight_snapshot(path: Path) -> str:
    """Create one provisional snapshot with O_EXCL; no run or approval."""
    checks = execution.preflight()
    content: dict[str, Any] = {
        "schema": 1,
        "phase": "preflight_only",
        "source_sha256": checks["source_sha256"],
        "grids": checks["grids"],
        "h3": checks["h3"],
        "r9_clone_inputs": checks["r9_clone_inputs"],
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "meter_complete": execution.RESOURCE_METER_COMPLETE,
        "approved": False,
    }
    raw = _canonical(content)
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def verify_preflight_snapshot(path: Path, expected_sha256: str) -> dict[str, Any]:
    """Reject source/config/runtime drift; neither this nor the digest is consent."""
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("preflight snapshot hash mismatch; STOP")
    document = json.loads(raw)
    if (raw != _canonical(document) or document.get("schema") != 1
            or document.get("phase") != "preflight_only"
            or document.get("approved") is not False
            or document.get("meter_complete") is not execution.RESOURCE_METER_COMPLETE
            or document.get("source_sha256") != execution.source_hashes()
            or document.get("grids") != {family: [list(pair) for pair in grid(family)]
                                         for family in PRIMARY}
            or document.get("h3") != {"policy_triples": 27, "legal_words": 8}
            or document.get("r9_clone_inputs") != 8192
            or document.get("python") != sys.version
            or document.get("torch") != torch.__version__
            or document.get("numpy") != np.__version__):
        raise ValueError("preflight snapshot is stale or not the required design; STOP")
    return document