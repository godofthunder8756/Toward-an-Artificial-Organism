"""Structured append-only logging for Stage A experiments."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


class JsonlWriter:
    """Append-only JSONL writer with an incremental SHA-256 digest."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = path.open("x", encoding="utf-8")
        self._hash = hashlib.sha256()
        self.count = 0
        self.closed = False

    def write(self, record: dict[str, Any]) -> None:
        if self.closed:
            raise RuntimeError("Cannot write to a closed JsonlWriter")
        line = canonical_json(record) + "\n"
        self._handle.write(line)
        self._hash.update(line.encode("utf-8"))
        self.count += 1

    def close(self) -> None:
        if self.closed:
            return
        self._handle.flush()
        os.fsync(self._handle.fileno())
        self._handle.close()
        self.closed = True

    @property
    def sha256(self) -> str:
        if not self.closed:
            raise RuntimeError("Digest is final only after close()")
        return self._hash.hexdigest()

    def __enter__(self) -> "JsonlWriter":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


class RunEventLogger:
    """Stable event log for execution milestones and failures."""

    def __init__(self, path: Path, run_id: str):
        self.run_id = run_id
        self.writer = JsonlWriter(path)

    def emit(self, event_type: str, **fields: Any) -> None:
        payload = {
            "run_id": self.run_id,
            "event_type": event_type,
            "timestamp_utc": utc_now_iso(),
            **fields,
        }
        self.writer.write(payload)

    def close(self) -> None:
        self.writer.close()

    @property
    def sha256(self) -> str:
        return self.writer.sha256
