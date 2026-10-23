"""Base Gaussian draws for FO paths, ISO paths, and gradient-check directions.

ISO draws are the PR #8 generator (40000 + 100*s), called through the existing
draw function so the bytes stay identical. FO and gradient-check draws are new
generators. Manifests hash the raw float64 tensors before rescaling or
normalization. Nothing here redraws, rejects, or reorders a sample.
"""

from __future__ import annotations

import hashlib
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import torch

from graded_reversion_draws import raw_draws as iso_raw_draws
from graded_reversion_spec import draw_generator_seed
from first_order_control_spec import (
    MANIFEST_SEEDS,
    N_GRAD_RANDOM,
    N_PATHS,
    fo_generator_seed,
    grad_generator_seed,
)


def _prepare_torch() -> None:
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def _randn_stack(generator_seed: int, count: int) -> np.ndarray:
    _prepare_torch()
    generator = torch.Generator(device="cpu")
    generator.manual_seed(int(generator_seed))
    chunks = []
    for _index in range(count):
        draw = torch.randn((24, 8), dtype=torch.float64, generator=generator)
        chunks.append(draw.numpy())
    array = np.ascontiguousarray(np.stack(chunks, axis=0), dtype=np.float64)
    if array.shape != (count, 24, 8):
        raise RuntimeError(array.shape)
    return array


def fo_raw_draws(seed: int) -> np.ndarray:
    """Shape (32, 24, 8). One torch.randn call per path, in order j = 1..32."""
    return _randn_stack(fo_generator_seed(seed), N_PATHS)


def grad_raw_draws(seed: int) -> np.ndarray:
    """Shape (3, 24, 8). Three torch.randn calls, before unit normalization."""
    return _randn_stack(grad_generator_seed(seed), N_GRAD_RANDOM)


def sha256_array(array: np.ndarray) -> str:
    raw = np.ascontiguousarray(array, dtype=np.float64).tobytes()
    return hashlib.sha256(raw).hexdigest()


def iso_generator_seed(seed: int) -> int:
    return draw_generator_seed(int(seed))


def manifest_for_seed(seed: int) -> dict:
    fo = fo_raw_draws(seed)
    iso = iso_raw_draws(seed)
    grad = grad_raw_draws(seed)
    return {
        "seed": int(seed),
        "fo_generator_seed": fo_generator_seed(seed),
        "iso_generator_seed": iso_generator_seed(seed),
        "grad_generator_seed": grad_generator_seed(seed),
        "fo_sha256": sha256_array(fo),
        "iso_sha256": sha256_array(iso),
        "grad_sha256": sha256_array(grad),
    }


def all_manifests(seeds=MANIFEST_SEEDS) -> dict:
    return {str(int(seed)): manifest_for_seed(int(seed)) for seed in seeds}


def concatenated_manifest_bytes(seeds=MANIFEST_SEEDS) -> bytes:
    parts = []
    for seed in seeds:
        parts.append(np.ascontiguousarray(fo_raw_draws(int(seed)), dtype=np.float64).tobytes())
        parts.append(np.ascontiguousarray(iso_raw_draws(int(seed)), dtype=np.float64).tobytes())
        parts.append(np.ascontiguousarray(grad_raw_draws(int(seed)), dtype=np.float64).tobytes())
    return b"".join(parts)
