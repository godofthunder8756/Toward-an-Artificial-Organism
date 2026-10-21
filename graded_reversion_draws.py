"""Torch random-direction draws for graded reversion.

Draws are the raw float64 torch.randn tensors, before block rescaling.
The freeze manifest records the sha256 of those bytes. Rescaling is separate
and is tested against displacement norms, including a synthetic zero block.
"""

from __future__ import annotations

import hashlib
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import torch

from graded_reversion_spec import (
    DRAW_SEEDS,
    EPS0,
    GATE_ROWS,
    N_RANDOM,
    NORM_REL_TOL,
    draw_generator_seed,
)


class ZeroDrawError(RuntimeError):
    """A nonzero block produced a random matrix of Frobenius norm 0."""


def _prepare_torch() -> None:
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def raw_draws(seed: int) -> np.ndarray:
    """Return shape (32, 24, 8) float64, one torch.randn call per path, in order."""
    _prepare_torch()
    generator = torch.Generator(device="cpu")
    generator.manual_seed(draw_generator_seed(seed))
    chunks = []
    for _index in range(N_RANDOM):
        draw = torch.randn((24, 8), dtype=torch.float64, generator=generator)
        chunks.append(draw.numpy())
    array = np.ascontiguousarray(np.stack(chunks, axis=0), dtype=np.float64)
    if array.shape != (N_RANDOM, 24, 8):
        raise RuntimeError(array.shape)
    return array


def draws_sha256(seed: int) -> str:
    return hashlib.sha256(raw_draws(seed).tobytes()).hexdigest()


def all_draw_sha256s(seeds=DRAW_SEEDS) -> dict:
    return {str(int(seed)): draws_sha256(int(seed)) for seed in seeds}


def concatenated_draw_bytes(seeds=DRAW_SEEDS) -> bytes:
    return b"".join(raw_draws(int(seed)).tobytes() for seed in seeds)


def rescale_draws(draws: np.ndarray, delta: np.ndarray) -> tuple[np.ndarray, list[dict]]:
    """Rescale each gate block to ||delta_k||_F. A block with ||delta_k||_F <= eps0 is zero.

    `draws` has shape (32, 24, 8). `delta` has shape (24, 8).
    """
    if draws.shape != (N_RANDOM, 24, 8):
        raise ValueError(draws.shape)
    if delta.shape != (24, 8):
        raise ValueError(delta.shape)
    source = torch.from_numpy(np.ascontiguousarray(draws, dtype=np.float64))
    displacement = torch.from_numpy(np.ascontiguousarray(delta, dtype=np.float64))
    scaled = torch.zeros_like(source)
    info = []
    for name in ("r", "z", "n"):
        row0, row1 = GATE_ROWS[name]
        block = displacement[row0:row1, :]
        block_norm = torch.linalg.vector_norm(block)
        block_norm_f = float(block_norm)
        if block_norm_f <= EPS0:
            info.append({"block": name, "zero": True, "norm": block_norm_f})
            continue
        random_block = source[:, row0:row1, :]
        random_norm = torch.linalg.vector_norm(random_block, dim=(1, 2))
        if bool(torch.any(random_norm == 0)):
            raise ZeroDrawError(name)
        factor = (block_norm / random_norm).reshape(-1, 1, 1)
        scaled[:, row0:row1, :] = random_block * factor
        info.append({"block": name, "zero": False, "norm": block_norm_f})
    return scaled.numpy(), info


def block_norm_errors(scaled: np.ndarray, delta: np.ndarray) -> dict:
    """Relative Frobenius errors. Zero blocks must be exactly zero."""
    scaled_t = torch.from_numpy(np.ascontiguousarray(scaled, dtype=np.float64))
    delta_t = torch.from_numpy(np.ascontiguousarray(delta, dtype=np.float64))
    per_block = {}
    worst = 0.0
    ok = True
    for name in ("r", "z", "n"):
        row0, row1 = GATE_ROWS[name]
        target = float(torch.linalg.vector_norm(delta_t[row0:row1, :]))
        got = torch.linalg.vector_norm(scaled_t[:, row0:row1, :], dim=(1, 2))
        if target <= EPS0:
            exact = bool(torch.all(scaled_t[:, row0:row1, :] == 0))
            per_block[name] = {"target": target, "max_abs": float(torch.max(torch.abs(got))), "relative": 0.0, "ok": exact}
            ok = ok and exact
            continue
        relative = torch.abs(got - target) / target
        max_relative = float(torch.max(relative))
        block_ok = max_relative <= NORM_REL_TOL
        per_block[name] = {"target": target, "max_relative": max_relative, "ok": block_ok}
        worst = max(worst, max_relative)
        ok = ok and block_ok
    full_target = float(torch.linalg.vector_norm(delta_t))
    full_got = torch.linalg.vector_norm(scaled_t, dim=(1, 2))
    if full_target <= EPS0:
        full_relative = 0.0
        full_ok = bool(torch.all(full_got <= EPS0))
    else:
        full_relative = float(torch.max(torch.abs(full_got - full_target) / full_target))
        full_ok = full_relative <= NORM_REL_TOL
    return {
        "blocks": per_block,
        "full_target": full_target,
        "full_max_relative": full_relative,
        "full_ok": full_ok,
        "worst_relative": worst,
        "ok": bool(ok and full_ok),
    }
