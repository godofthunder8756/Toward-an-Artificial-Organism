"""Independent float64 NumPy forward pass and metrics.

No torch. No import of the frozen evaluator. No consciousness claim.
"""

from __future__ import annotations

import math

import numpy as np

from frozen_recurrent_compensation_spec import COMPONENT_NAMES, TAU


def sigmoid(values: np.ndarray) -> np.ndarray:
    out = np.empty(values.shape, dtype=np.float64)
    positive = values >= 0
    out[positive] = 1.0 / (1.0 + np.exp(-values[positive]))
    exp_values = np.exp(values[~positive])
    out[~positive] = exp_values / (1.0 + exp_values)
    return out


def history_bits() -> np.ndarray:
    bits = np.zeros((256, 8), dtype=np.float64)
    for history in range(256):
        for stage in range(8):
            bits[history, stage] = (history >> stage) & 1
    return bits


def _as_grid(values: np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.shape != (256, 3):
        raise ValueError(array.shape)
    return np.transpose(array.reshape(16, 16, 3), (1, 0, 2))


def l_prefix(forecast: np.ndarray, oracle: np.ndarray) -> float:
    """Uniform mean over the 16×16 grid of the squared prefix-centered gap. No /3."""
    forecast_g = _as_grid(forecast)
    oracle_g = _as_grid(oracle)
    deviation = (forecast_g - forecast_g.mean(axis=0, keepdims=True)) - (
        oracle_g - oracle_g.mean(axis=0, keepdims=True)
    )
    return float(np.mean(np.sum(deviation * deviation, axis=-1)))


def pd_q(oracle: np.ndarray) -> float:
    oracle_g = _as_grid(oracle)
    centered = oracle_g - oracle_g.mean(axis=0, keepdims=True)
    return float(np.mean(np.sum(centered * centered, axis=-1)))


def split_excess(predictions: np.ndarray, oracle: np.ndarray, probability: np.ndarray, is_test: np.ndarray) -> dict:
    squared = (predictions - oracle) ** 2
    out = {}
    for name, flag in (("TEST", True), ("TRAIN", False)):
        mask = is_test if flag else np.logical_not(is_test)
        mass = float(probability[mask].sum())
        if not math.isfinite(mass) or mass <= 0.0:
            raise RuntimeError("split mass is not positive")
        weights = np.zeros(probability.shape[0], dtype=np.float64)
        weights[mask] = probability[mask] / mass
        components = (weights[:, None] * squared).sum(axis=0)
        out[name] = {
            "X": float(components[0]),
            "Y": float(components[1]),
            "XOR": float(components[2]),
            "total": float(components.sum()),
        }
    return out


def subset_excess(predictions: np.ndarray, oracle: np.ndarray, probability: np.ndarray, mask: np.ndarray) -> dict:
    mass = float(probability[mask].sum())
    if not math.isfinite(mass) or mass <= 0.0:
        raise RuntimeError("subset mass is not positive")
    weights = np.zeros(probability.shape[0], dtype=np.float64)
    weights[mask] = probability[mask] / mass
    components = (weights[:, None] * (predictions - oracle) ** 2).sum(axis=0)
    return {
        "X": float(components[0]),
        "Y": float(components[1]),
        "XOR": float(components[2]),
        "total": float(components.sum()),
    }


def outputs_valid(predictions: np.ndarray) -> bool:
    return bool(np.isfinite(predictions).all() and np.all(predictions > 0.0) and np.all(predictions < 1.0))


def forward(weights: dict, bits: np.ndarray | None = None) -> np.ndarray:
    """Float64 GRU-8. Gate order is reset, update, new. Readout is tanh then sigmoid."""
    if bits is None:
        bits = history_bits()
    w_ih = weights["w_ih"]
    w_hh = weights["w_hh"]
    b_ih = weights["b_ih"]
    b_hh = weights["b_hh"]
    hidden = w_hh.shape[1]
    state = np.zeros((bits.shape[0], hidden), dtype=np.float64)
    for stage in range(bits.shape[1]):
        packed = np.zeros((bits.shape[0], 9), dtype=np.float64)
        packed[:, 0] = bits[:, stage] * 2.0 - 1.0
        packed[:, stage + 1] = 1.0
        gates_i = packed @ w_ih.T + b_ih
        gates_h = state @ w_hh.T + b_hh
        i_r, i_z, i_n = np.split(gates_i, 3, axis=1)
        h_r, h_z, h_n = np.split(gates_h, 3, axis=1)
        reset = sigmoid(i_r + h_r)
        update = sigmoid(i_z + h_z)
        new = np.tanh(i_n + reset * h_n)
        state = (1.0 - update) * new + update * state
    readout = np.tanh(state @ weights["w1"].T + weights["b1"])
    return sigmoid(readout @ weights["w2"].T + weights["b2"])


def normalized_components(l_prefix_value: float, e_total: float, e_xor: float, pd: float, thr_total: float, thr_xor: float) -> dict:
    if pd <= 0.0 or thr_total <= 0.0 or thr_xor <= 0.0:
        raise RuntimeError("target denominators must be positive")
    return {
        "prefix": l_prefix_value / (TAU * pd),
        "total": e_total / thr_total,
        "xor": e_xor / thr_xor,
    }


def evaluate(weights: dict, oracle: np.ndarray, probability: np.ndarray, is_test: np.ndarray, thr_total: float, thr_xor: float, val_mask: np.ndarray | None = None) -> dict:
    predictions = forward(weights)
    prefix = l_prefix(predictions, oracle)
    pd = pd_q(oracle)
    errors = split_excess(predictions, oracle, probability, is_test)
    components = normalized_components(
        prefix,
        errors["TEST"]["total"],
        errors["TEST"]["XOR"],
        pd,
        thr_total,
        thr_xor,
    )
    result = {
        "predictions": predictions,
        "L_prefix": prefix,
        "PD": pd,
        "E_TEST": errors["TEST"],
        "E_TRAIN": errors["TRAIN"],
        "components": components,
        "T": float(max(components[name] for name in COMPONENT_NAMES)),
        "outputs_valid": outputs_valid(predictions),
        "val": None if val_mask is None else subset_excess(predictions, oracle, probability, val_mask),
    }
    return result
