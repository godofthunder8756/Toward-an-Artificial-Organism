"""Load authenticated existing arrays. Never regenerates them (annex A1, E39-10)."""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np

from ckappa_oracle.io import integrity_stop
from ckappa_classfit.gate import git_show, sha256_bytes
from ckappa_classfit.pinned import (
    ARRAY_COMMIT,
    DRAWN_ARRAYS_FILE_SHA256,
    RAW_ARRAY_SHA256,
    USED_ARRAYS,
)
from ckappa_classfit.records import matrix_sha


_SHAPES = {
    "Q": (8, 3),
    "Q2": (8, 2),
    "O6_directions": (16, 8),
    "O4_directions": (64, 3),
    "O7_directions": (16, 8),
}


def load_drawn_arrays(root: Path) -> dict:
    spec = f"{ARRAY_COMMIT}:outputs/drawn_arrays.npz"
    raw = git_show(root, spec)
    file_sha = sha256_bytes(raw)
    if file_sha != DRAWN_ARRAYS_FILE_SHA256:
        integrity_stop("drawn_arrays.npz file sha256 mismatch", found=file_sha, expected=DRAWN_ARRAYS_FILE_SHA256)
    with np.load(io.BytesIO(raw), allow_pickle=False) as archive:
        keys = list(archive.keys())
        loaded = {}
        checked = []
        for name, expected in RAW_ARRAY_SHA256.items():
            if name not in archive:
                integrity_stop("drawn array key missing", name=name)
            array = np.ascontiguousarray(archive[name], dtype="<f8")
            if array.dtype.str != "<f8" or not array.flags.c_contiguous:
                integrity_stop("drawn array dtype or order", name=name)
            if tuple(int(v) for v in array.shape) != _SHAPES[name]:
                integrity_stop("drawn array shape", name=name, shape=list(array.shape))
            digest = matrix_sha(array)
            if digest != expected:
                integrity_stop("drawn array raw-byte sha256 mismatch", name=name, found=digest, expected=expected)
            checked.append(
                {
                    "name": name,
                    "shape": list(array.shape),
                    "dtype": "<f8",
                    "sha256": digest,
                    "used": name in USED_ARRAYS,
                }
            )
            if name in USED_ARRAYS:
                loaded[name] = array
        extra = sorted(set(keys) - set(RAW_ARRAY_SHA256))
        if extra:
            integrity_stop("unexpected drawn array key", keys=extra)
    return {"Q": loaded["Q"], "Q2": loaded["Q2"], "O6_directions": loaded["O6_directions"], "checked": checked, "file_sha256": file_sha}
