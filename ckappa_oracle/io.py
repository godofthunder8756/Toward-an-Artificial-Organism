"""Atomic JSON writes and the package stop type."""

from __future__ import annotations

import json
import os
from pathlib import Path


class PackageStop(Exception):
    def __init__(self, kind: str, exit_code: int, detail: dict | None = None):
        super().__init__(kind)
        self.kind = kind
        self.exit_code = exit_code
        self.detail = detail or {}


def json_ready(obj):
    """Convert a JSON-ready structure, rejecting NaN and non-finite floats."""
    if obj is None or isinstance(obj, (str, int, bool)):
        return obj
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):
            raise ValueError("non-finite float in output")
        return obj
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
