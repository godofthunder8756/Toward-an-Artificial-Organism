"""PCG64 draws. The hash file is rewritten and fsynced at each draw."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import numpy as np

from ckappa_oracle.io import PackageStop, atomic_write_json
from ckappa_oracle.pinned import FROZEN_RUNTIME


def _sha_record(name: str, array: np.ndarray, seed: int, procedure: str, extra: dict | None = None):
    raw = np.ascontiguousarray(array, dtype="<f8")
    if raw.dtype.str != "<f8":
        raise PackageStop("PIPELINE INVALID", 2, {"reason": "drawn array dtype", "name": name})
    digest = hashlib.sha256(raw.tobytes()).hexdigest()
    record = {
        "name": name,
        "seed": seed,
        "shape": [int(value) for value in raw.shape],
        "dtype": "<f8",
        "sha256": digest,
        "procedure": procedure,
    }
    if extra:
        record.update(extra)
    return raw, record


def _generator(seed: int):
    return np.random.Generator(np.random.PCG64(seed))


def _orthonormal(seed: int, columns: int):
    raw = _generator(seed).standard_normal((8, columns))
    q_factor, r_factor = np.linalg.qr(raw, mode="reduced")
    for index in range(r_factor.shape[0]):
        diagonal = r_factor[index, index]
        if diagonal < 0.0:
            q_factor[:, index] *= -1.0
            r_factor[index, :] *= -1.0
        elif not (r_factor[index, index] > 0.0):
            raise PackageStop(
                "PIPELINE INVALID",
                2,
                {"reason": "QR diagonal is not strictly positive", "column": index, "seed": seed},
            )
    procedure = f"standard_normal((8, {columns})); reduced QR; columns signed so diag(R) > 0"
    return _sha_record(f"Q{columns}", q_factor, seed, procedure)[0]


def _unit_directions(seed: int, count: int, dim: int):
    raw = _generator(seed).standard_normal((count, dim))
    norms = np.linalg.norm(raw, axis=1)
    if np.any(norms == 0.0):
        raise PackageStop("PIPELINE INVALID", 2, {"reason": "direction row has norm 0", "seed": seed})
    unit = raw / norms[:, None]
    procedure = f"standard_normal(({count}, {dim})); each row divided by its Euclidean norm"
    return unit


def draw_arrays(root: Path) -> dict:
    """Draw Q, Q2, O6 directions, and O4 directions. Hash file updated at each draw."""
    records = []
    path = root / "outputs" / "drawn_array_hashes.json"

    def commit(array, name, seed, procedure, extra=None):
        stored, record = _sha_record(name, array, seed, procedure, extra)
        records.append(record)
        atomic_write_json(path, {"arrays": records})
        return stored

    q_matrix = commit(
        _orthonormal(int(FROZEN_RUNTIME["seed_Q"]), 3),
        "Q",
        int(FROZEN_RUNTIME["seed_Q"]),
        "standard_normal((8, 3)); reduced QR; columns signed so diag(R) > 0",
    )
    q2_matrix = commit(
        _orthonormal(int(FROZEN_RUNTIME["seed_Q2"]), 2),
        "Q2",
        int(FROZEN_RUNTIME["seed_Q2"]),
        "standard_normal((8, 2)); reduced QR; columns signed so diag(R) > 0",
    )
    o6 = commit(
        _unit_directions(int(FROZEN_RUNTIME["seed_O6_directions"]), 16, 8),
        "O6_directions",
        int(FROZEN_RUNTIME["seed_O6_directions"]),
        "standard_normal((16, 8)); each row divided by its Euclidean norm; signs applied later as +v then -v",
    )
    o4 = commit(
        _unit_directions(int(FROZEN_RUNTIME["seed_O4_directions"]), 64, 3),
        "O4_directions",
        int(FROZEN_RUNTIME["seed_O4_directions"]),
        "standard_normal((64, 3)); each row divided by its Euclidean norm; signs applied later as +v then -v",
    )
    # O7 reuses the O6 draw. The hash entry is written at this assignment, not from a second draw.
    o6_record = next(record for record in records if record["name"] == "O6_directions")
    records.append(
        {
            "name": "O7_directions",
            "seed": o6_record["seed"],
            "shape": list(o6_record["shape"]),
            "dtype": "<f8",
            "sha256": o6_record["sha256"],
            "procedure": "shared with O6_directions; no second draw",
            "shared_with": "O6_directions",
        }
    )
    atomic_write_json(path, {"arrays": records})

    npz_path = root / "outputs" / "drawn_arrays.npz"
    tmp = npz_path.with_name("drawn_arrays.npz.tmp.npz")
    np.savez(
        tmp,
        Q=q_matrix,
        Q2=q2_matrix,
        O6_directions=o6,
        O7_directions=o6,
        O4_directions=o4,
    )
    os.replace(tmp, npz_path)
    fd = os.open(npz_path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    dir_fd = os.open(npz_path.parent, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
    return {
        "Q": q_matrix,
        "Q2": q2_matrix,
        "O6_directions": o6,
        "O4_directions": o4,
        "records": records,
    }
