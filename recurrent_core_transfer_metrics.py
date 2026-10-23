"""TEST excesses, VAL selection risk, forecast variation, and reversion."""

from __future__ import annotations

import math

import numpy as np
import torch

from recurrent_core_transfer_models import MatrixOverride, eval_copy, gate_block
from recurrent_core_transfer_spec import (
    CONTINUATION_STAGES,
    EARLY_STAGES,
    EPS0,
    GATE_INDEX,
    GATE_ROWS,
    GATES,
    IDENTITY_TOL,
    N_RANDOM,
)
from twostream_acquisition_e3_v2 import UNDEFINED
from twostream_acquisition_metrics import (
    all_bits,
    component_excess,
    identity_checks,
    outputs_valid,
    rollout,
)
from twostream_acquisition_spec import is_test_history


def evaluate_arm(model, world) -> dict:
    copied = eval_copy(model)
    predictions, states = rollout(copied, all_bits())
    errors = component_excess(predictions, world)
    return {
        "errors": errors,
        "outputs_valid": outputs_valid(predictions),
        "identity": identity_checks(copied, predictions, states),
        "predictions": predictions,
        "states": states,
        "model": copied,
    }


def val_histories() -> list[int]:
    from recurrent_core_transfer_spec import is_val_history

    return [history for history in range(256) if is_val_history(history)]


def probability_excess(predictions: np.ndarray, histories: list[int], world) -> dict:
    index = np.asarray(histories, dtype=np.int64)
    weights = world.probability[index]
    total = float(weights.sum())
    if total <= 0:
        raise RuntimeError("VAL mass is zero")
    weights = weights / total
    squared = (predictions - world.q[index]) ** 2
    components = (weights[:, None] * squared).sum(axis=0)
    return {
        "X": float(components[0]),
        "Y": float(components[1]),
        "XOR": float(components[2]),
        "total": float(components.sum()),
    }


def predict_histories(model, histories: list[int]) -> np.ndarray:
    copied = eval_copy(model)
    bits = all_bits()[np.asarray(histories, dtype=np.int64)]
    predictions, _states = rollout(copied, bits)
    return predictions


def _grid(predictions: np.ndarray) -> np.ndarray:
    grid = np.zeros((16, 16, 3), dtype=np.float64)
    for prefix in range(16):
        for continuation in range(16):
            grid[prefix, continuation] = predictions[prefix + 16 * continuation]
    return grid


def _uniform_variation(grid: np.ndarray) -> tuple[float, float]:
    mean_u = grid.mean(axis=0)
    mean_p = grid.mean(axis=1)
    prefix_var = np.mean(np.sum((grid - mean_u[None, :, :]) ** 2, axis=-1))
    continuation_var = np.mean(np.sum((grid - mean_p[:, None, :]) ** 2, axis=-1))
    return float(prefix_var), float(continuation_var)


def _probability_variation(grid: np.ndarray, world) -> tuple[float, float]:
    probability = np.zeros((16, 16), dtype=np.float64)
    for prefix in range(16):
        for continuation in range(16):
            probability[prefix, continuation] = world.probability[prefix + 16 * continuation]
    mass_u = probability.sum(axis=0)
    mass_p = probability.sum(axis=1)
    mean_u = np.zeros((16, 3), dtype=np.float64)
    mean_p = np.zeros((16, 3), dtype=np.float64)
    for continuation in range(16):
        mean_u[continuation] = (probability[:, continuation, None] * grid[:, continuation, :]).sum(axis=0) / mass_u[continuation]
    for prefix in range(16):
        mean_p[prefix] = (probability[prefix, :, None] * grid[prefix, :, :]).sum(axis=0) / mass_p[prefix]
    prefix_sq = np.sum((grid - mean_u[None, :, :]) ** 2, axis=-1)
    continuation_sq = np.sum((grid - mean_p[:, None, :]) ** 2, axis=-1)
    return float((probability * prefix_sq).sum()), float((probability * continuation_sq).sum())


def _test_variation(grid: np.ndarray) -> tuple[float, float]:
    mask = np.zeros((16, 16), dtype=bool)
    for prefix in range(16):
        for continuation in range(16):
            mask[prefix, continuation] = is_test_history(prefix + 16 * continuation)
    mean_u = np.zeros((16, 3), dtype=np.float64)
    mean_p = np.zeros((16, 3), dtype=np.float64)
    for continuation in range(16):
        rows = grid[mask[:, continuation], continuation, :]
        mean_u[continuation] = rows.mean(axis=0)
    for prefix in range(16):
        rows = grid[prefix, mask[prefix, :], :]
        mean_p[prefix] = rows.mean(axis=0)
    prefix_sq = np.sum((grid - mean_u[None, :, :]) ** 2, axis=-1)
    continuation_sq = np.sum((grid - mean_p[:, None, :]) ** 2, axis=-1)
    return float(prefix_sq[mask].mean()), float(continuation_sq[mask].mean())


def variation_stats(predictions: np.ndarray, world) -> dict:
    grid = _grid(predictions)
    uniform_pd, uniform_cd = _uniform_variation(grid)
    probability_pd, probability_cd = _probability_variation(grid, world)
    test_pd, test_cd = _test_variation(grid)
    return {
        "uniform": {"PD": uniform_pd, "CD": uniform_cd},
        "probability": {"PD": probability_pd, "CD": probability_cd},
        "test": {"PD": test_pd, "CD": test_cd},
    }


def pdcd_ratio(numerator: float, denominator: float):
    """§5 rule: a denominator ≤ 10⁻¹² makes the ratio undefined. Never +∞."""
    numerator = float(numerator)
    denominator = float(denominator)
    if not math.isfinite(numerator) or not math.isfinite(denominator):
        return UNDEFINED
    if denominator <= EPS0:
        return UNDEFINED
    return numerator / denominator


def _delta(errors, baseline) -> dict:
    out = {}
    for split in ("TEST", "TRAIN"):
        out[split] = {
            key: float(errors[split][key] - baseline[split][key])
            for key in ("X", "Y", "XOR", "total")
        }
    return out


def _rollout_override(model, override) -> np.ndarray:
    model.override = override
    try:
        predictions, _states = rollout(model, all_bits())
    finally:
        model.override = None
    return predictions


def _random_blocks(seed: int, gate: str, delta_norm: float) -> list[torch.Tensor]:
    generator = torch.Generator(device="cpu")
    generator.manual_seed(9000 + 100 * (seed - 100) + 10 * GATE_INDEX[gate])
    blocks = []
    for _draw in range(N_RANDOM):
        epsilon = torch.randn((8, 8), dtype=torch.float64, generator=generator)
        norm = float(torch.linalg.vector_norm(epsilon))
        if delta_norm <= EPS0 or norm == 0.0:
            scaled = torch.zeros((8, 8), dtype=torch.float64)
        else:
            scaled = epsilon * (delta_norm / norm)
        blocks.append(scaled)
    return blocks


def original_readout_excess(model, init_block, rows, world) -> dict:
    """REV_k on CAND's own readout. Descriptive only."""
    predictions = _rollout_override(model, MatrixOverride(CONTINUATION_STAGES, rows, init_block))
    return component_excess(predictions, world)


def hidden_reversion(model, intact: np.ndarray, intact_errors: dict, w0_hh, w0_bias, foreign_hh, seed: int, world) -> dict:
    """Interventions on one frozen F-TRAINED eval model. The readout stays fixed."""
    trained_hh = model.rnn.weight_hh_l0.detach()
    out = {}
    for gate in GATES:
        rows = GATE_ROWS[gate]
        trained_block = gate_block(trained_hh, gate).double()
        init_block = gate_block(w0_hh, gate).double()
        init_bias = w0_bias[rows[0]:rows[1]].detach().double().clone()
        foreign_block = gate_block(foreign_hh, gate).double()
        delta = init_block - trained_block
        delta_norm = float(torch.linalg.vector_norm(delta))
        rev = _rollout_override(
            model, MatrixOverride(CONTINUATION_STAGES, rows, init_block)
        )
        sham = _rollout_override(
            model, MatrixOverride(CONTINUATION_STAGES, rows, trained_block.clone())
        )
        restored = _rollout_override(model, None)
        sham_gap = float(np.max(np.abs(sham - intact)))
        restore_gap = float(np.max(np.abs(restored - intact)))
        random_predictions = []
        random_deltas = []
        for block in _random_blocks(seed, gate, delta_norm):
            preds = _rollout_override(
                model, MatrixOverride(CONTINUATION_STAGES, rows, trained_block + block)
            )
            random_predictions.append(preds)
            random_deltas.append(_delta(component_excess(preds, world), intact_errors))
        descriptive = {
            "temporal": _delta(
                component_excess(
                    _rollout_override(model, MatrixOverride((4, 5), rows, init_block)),
                    world,
                ),
                intact_errors,
            ),
            "early": _delta(
                component_excess(
                    _rollout_override(model, MatrixOverride(EARLY_STAGES, rows, init_block)),
                    world,
                ),
                intact_errors,
            ),
            "bias": _delta(
                component_excess(
                    _rollout_override(
                        model,
                        MatrixOverride(CONTINUATION_STAGES, rows, init_block, init_bias),
                    ),
                    world,
                ),
                intact_errors,
            ),
            "foreign": _delta(
                component_excess(
                    _rollout_override(
                        model, MatrixOverride(CONTINUATION_STAGES, rows, foreign_block)
                    ),
                    world,
                ),
                intact_errors,
            ),
        }
        rev_errors = component_excess(rev, world)
        out[gate] = {
            "delta_norm": delta_norm,
            "zero_displacement": bool(delta_norm <= EPS0),
            "delta_E": _delta(rev_errors, intact_errors),
            "random_delta_E": random_deltas,
            "sham_gap": sham_gap,
            "restore_gap": restore_gap,
            "sham_ok": bool(sham_gap <= EPS0),
            "restore_ok": bool(restore_gap <= IDENTITY_TOL),
            "finite": bool(
                np.isfinite(rev).all()
                and all(np.isfinite(preds).all() for preds in random_predictions)
            ),
            "variation_rev": variation_stats(rev, world),
            "variation_random": [variation_stats(preds, world) for preds in random_predictions],
            "descriptive_delta_E": descriptive,
            "predictions_rev": rev,
        }
    return out
