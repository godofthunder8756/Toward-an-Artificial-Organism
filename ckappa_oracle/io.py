"""Atomic JSON writes and the package stop type."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path


class PackageStop(Exception):
    def __init__(self, kind: str, exit_code: int, detail: dict | None = None):
        super().__init__(kind)
        self.kind = kind
        self.exit_code = exit_code
        self.detail = detail or {}


# M3. Distinct from exits 0–6. The ruling names the stop kind and not this integer.
INTEGRITY_STOP_KIND = "INTEGRITY STOP"
INTEGRITY_STOP_EXIT = 7


def integrity_stop(reason: str, **detail) -> None:
    """Fail-closed check that is not N1. No outcome label is attached here."""
    payload = {"classification": "non-N1", "reason": reason}
    payload.update(detail)
    raise PackageStop(INTEGRITY_STOP_KIND, INTEGRITY_STOP_EXIT, payload)


def _nonfinite_to_null(value: float):
    if not math.isfinite(value):
        return None
    return value


def json_ready(obj):
    """Convert a JSON-ready structure. Non-finite floats are serialized as null."""
    if obj is None or isinstance(obj, (str, int, bool)):
        return obj
    if isinstance(obj, float):
        return _nonfinite_to_null(obj)
    if type(obj).__module__ == "numpy":
        name = type(obj).__name__
        if name == "ndarray":
            return json_ready(obj.tolist())
        if name.startswith("float"):
            return _nonfinite_to_null(float(obj))
        if name.startswith("int"):
            return int(obj)
        if name.startswith("bool"):
            return bool(obj)
    if isinstance(obj, dict):
        return {str(k): json_ready(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_ready(v) for v in obj]
    raise TypeError(type(obj).__name__)


def atomic_write_text(path: Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    dir_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def atomic_write_json(path: Path, obj) -> None:
    text = json.dumps(json_ready(obj), indent=2, sort_keys=True, allow_nan=False) + "\n"
    atomic_write_text(path, text)
