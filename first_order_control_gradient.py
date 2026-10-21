"""Autograd of primary L_prefix at the trained hidden-to-hidden matrix.

Updates 1-4 use the intact trained matrix. The stage-4 state is detached.
Updates 5-8 share one leaf V. Other parameters are frozen. The forward is the
float64 GRU used by evaluation, called without inference mode.
"""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import torch
from torch.func import functional_call

from first_order_control_draws import sha256_array
from first_order_control_spec import FD_ABS_FLOOR, FD_REL, FD_STEP, N_GRAD_RANDOM
from twostream_acquisition_metrics import all_bits


def _prepare() -> None:
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def l_prefix_torch(forecast: torch.Tensor, oracle: torch.Tensor) -> torch.Tensor:
    """Same 16x16 prefix centering as the NumPy primary loss. No division by three."""
    forecast_g = forecast.reshape(16, 16, 3).permute(1, 0, 2)
    oracle_g = oracle.reshape(16, 16, 3).permute(1, 0, 2)
    deviation = (forecast_g - forecast_g.mean(dim=0, keepdim=True)) - (
        oracle_g - oracle_g.mean(dim=0, keepdim=True)
    )
    return torch.mean(torch.sum(deviation * deviation, dim=-1))


def fd_within_tolerance(fd_value: float, directional: float, g_norm: float) -> bool:
    gap = abs(float(fd_value) - float(directional))
    limit = FD_ABS_FLOOR + FD_REL * float(g_norm)
    return bool(gap <= limit)


def _gru_step(rnn, state, bit, stage_idx: int, weight_hh: torch.Tensor) -> torch.Tensor:
    reading = (bit.to(dtype=state.dtype) * 2.0 - 1.0).unsqueeze(1)
    one = state.new_zeros(bit.shape[0], 8)
    one[:, stage_idx] = 1
    packed = torch.cat([reading, one], dim=1).unsqueeze(1)
    params = {
        "weight_ih_l0": rnn.weight_ih_l0,
        "weight_hh_l0": weight_hh,
        "bias_ih_l0": rnn.bias_ih_l0,
        "bias_hh_l0": rnn.bias_hh_l0,
    }
    _out, hidden = functional_call(rnn, params, (packed, state.unsqueeze(0)))
    return hidden.squeeze(0)


def _readout(model, state) -> torch.Tensor:
    return torch.sigmoid(model.readout_fc2(torch.tanh(model.readout_fc1(state))))


def prefix_loss(model, oracle: torch.Tensor, bits: torch.Tensor, weight_hh, *, detach_h4: bool = True, freeze_parameters: bool = True) -> torch.Tensor:
    """L_prefix at tied or untied late-stage hidden-to-hidden weights.

    A single tensor is reused at stages 4-7. A sequence of four tensors uses
    one leaf per stage. Production calls keep the defaults.
    """
    _prepare()
    if freeze_parameters:
        for parameter in model.parameters():
            parameter.requires_grad_(False)
    if isinstance(weight_hh, (list, tuple)):
        late = list(weight_hh)
    else:
        late = [weight_hh, weight_hh, weight_hh, weight_hh]
    if len(late) != 4:
        raise ValueError(len(late))
    rnn = model.rnn
    state = model.initial_state(bits.shape[0], bits.dtype, bits.device)
    for stage in range(4):
        state = _gru_step(rnn, state, bits[:, stage], stage, rnn.weight_hh_l0)
    if detach_h4:
        state = state.detach()
    for offset, stage in enumerate(range(4, 8)):
        state = _gru_step(rnn, state, bits[:, stage], stage, late[offset])
    return l_prefix_torch(_readout(model, state), oracle)


def oracle_tensor(oracle_np: np.ndarray) -> torch.Tensor:
    return torch.from_numpy(np.ascontiguousarray(oracle_np, dtype=np.float64))


def bit_tensor() -> torch.Tensor:
    return torch.from_numpy(np.ascontiguousarray(all_bits(), dtype=np.float64))


def _one_gradient(model, oracle, bits, trained):
    leaf = trained.detach().clone().requires_grad_(True)
    loss = prefix_loss(model, oracle, bits, leaf)
    loss.backward()
    if leaf.grad is None:
        raise RuntimeError("V received no gradient")
    return loss.detach(), leaf.grad.detach().clone()


def compute_gradient(model, oracle: torch.Tensor, bits: torch.Tensor, trained: torch.Tensor) -> dict:
    """Two independent backward passes. Byte identity is required for validity."""
    _prepare()
    model.zero_grad(set_to_none=True)
    loss_a, grad_a = _one_gradient(model, oracle, bits, trained)
    model.zero_grad(set_to_none=True)
    loss_b, grad_b = _one_gradient(model, oracle, bits, trained)
    identical = bool(torch.equal(grad_a, grad_b) and torch.equal(loss_a, loss_b))
    finite = bool(torch.isfinite(grad_a).all() and torch.isfinite(loss_a))
    array = np.ascontiguousarray(grad_a.cpu().numpy(), dtype=np.float64)
    return {
        "loss": float(loss_a),
        "G": grad_a,
        "byte_identical": identical,
        "finite": finite,
        "norm": float(torch.linalg.vector_norm(grad_a)),
        "sha256": sha256_array(array),
    }


def untied_stage_gradients(model, oracle, bits, trained: torch.Tensor):
    """Four independent leaves, one per late stage, summed by the caller."""
    _prepare()
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    leaves = [trained.detach().clone().requires_grad_(True) for _index in range(4)]
    loss = prefix_loss(model, oracle, bits, leaves, detach_h4=True, freeze_parameters=True)
    loss.backward()
    grads = []
    for leaf in leaves:
        if leaf.grad is None:
            raise RuntimeError("an untied stage received no gradient")
        grads.append(leaf.grad.detach().clone())
    return grads


def unit_direction(matrix: torch.Tensor) -> torch.Tensor | None:
    norm = torch.linalg.vector_norm(matrix)
    if not bool(torch.isfinite(norm)) or float(norm) == 0.0:
        return None
    return matrix / norm


def fd_directions(delta: torch.Tensor, raw_random: torch.Tensor):
    """d/||d|| plus three unit directions. None if a direction cannot be formed."""
    first = unit_direction(delta)
    if first is None:
        return None
    directions = [first]
    names = ["reversion"]
    if tuple(raw_random.shape) != (N_GRAD_RANDOM, 24, 8):
        raise ValueError(raw_random.shape)
    for index in range(N_GRAD_RANDOM):
        direction = unit_direction(raw_random[index])
        if direction is None:
            return None
        directions.append(direction)
        names.append("random_%d" % (index + 1))
    return names, directions


def central_fd(model, oracle, bits, trained: torch.Tensor, direction: torch.Tensor, step: float = FD_STEP) -> float:
    step_t = torch.tensor(float(step), dtype=torch.float64)
    with torch.no_grad():
        plus = prefix_loss(model, oracle, bits, (trained + step_t * direction).detach())
        minus = prefix_loss(model, oracle, bits, (trained - step_t * direction).detach())
    return float((plus - minus) / (2.0 * step_t))


def finite_difference_report(model, oracle, bits, trained, gradient, delta, raw_random) -> dict:
    built = fd_directions(delta, raw_random)
    if built is None:
        return {"ok": False, "reason": "direction", "checks": []}
    names, directions = built
    g_norm = float(torch.linalg.vector_norm(gradient))
    checks = []
    ok = bool(torch.isfinite(gradient).all())
    for name, direction in zip(names, directions):
        fd_value = central_fd(model, oracle, bits, trained, direction)
        directional = float(torch.sum(gradient * direction))
        gap = abs(fd_value - directional)
        passed = fd_within_tolerance(fd_value, directional, g_norm)
        ok = ok and passed and math_finite(fd_value) and math_finite(directional)
        checks.append(
            {
                "name": name,
                "fd": fd_value,
                "directional": directional,
                "gap": gap,
                "limit": FD_ABS_FLOOR + FD_REL * g_norm,
                "ok": passed,
            }
        )
    return {"ok": bool(ok), "reason": None if ok else "fd", "checks": checks, "g_norm": g_norm}


def math_finite(value: float) -> bool:
    return bool(np.isfinite(value))
