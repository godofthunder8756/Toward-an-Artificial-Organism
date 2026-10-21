"""Oracle-referenced prefix-function loss, AUC, and per-seed flags.

The primary loss is the protocol's ASCII definition. There is no division by
three. Negative excesses are retained.
"""

from __future__ import annotations

import math

import numpy as np

from graded_reversion_spec import (
    ALPHAS,
    AUC_WEIGHTS,
    EPS0,
    N_RANDOM,
    UNDEFINED,
)
from recurrent_core_transfer_metrics import variation_stats
from twostream_acquisition_metrics import component_excess


def history_grid(values: np.ndarray) -> np.ndarray:
    """Map h = p + 16u onto an array indexed [prefix, continuation, component]."""
    array = np.asarray(values, dtype=np.float64)
    if array.shape != (256, 3):
        raise ValueError(array.shape)
    # C-order reshape is [continuation, prefix, component] because h = p + 16u.
    return np.transpose(array.reshape(16, 16, 3), (1, 0, 2))


def probability_grid(probability: np.ndarray) -> np.ndarray:
    weights = np.asarray(probability, dtype=np.float64)
    if weights.shape != (256,):
        raise ValueError(weights.shape)
    return np.transpose(weights.reshape(16, 16), (1, 0))


def test_mask_grid(is_test: np.ndarray) -> np.ndarray:
    mask = np.asarray(is_test, dtype=bool)
    if mask.shape != (256,):
        raise ValueError(mask.shape)
    return np.transpose(mask.reshape(16, 16), (1, 0))


def _prefix_deviation(forecast: np.ndarray, oracle: np.ndarray) -> np.ndarray:
    """Deviation of the prefix-centered forecast from the prefix-centered oracle.

    Shape is [prefix, continuation, component]. Means are uniform over prefixes.
    """
    centered_f = forecast - forecast.mean(axis=0, keepdims=True)
    centered_q = oracle - oracle.mean(axis=0, keepdims=True)
    return centered_f - centered_q


def _continuation_deviation(forecast: np.ndarray, oracle: np.ndarray) -> np.ndarray:
    centered_f = forecast - forecast.mean(axis=1, keepdims=True)
    centered_q = oracle - oracle.mean(axis=1, keepdims=True)
    return centered_f - centered_q


def l_prefix(forecast: np.ndarray, oracle: np.ndarray) -> float:
    """Protocol §5 L_prefix. The 1/256 factor is the mean over the 16×16 grid."""
    deviation = _prefix_deviation(history_grid(forecast), history_grid(oracle))
    return float(np.mean(np.sum(deviation * deviation, axis=-1)))


def l_prefix_components(forecast: np.ndarray, oracle: np.ndarray) -> dict:
    deviation = _prefix_deviation(history_grid(forecast), history_grid(oracle))
    components = np.mean(deviation * deviation, axis=(0, 1))
    return {
        "X": float(components[0]),
        "Y": float(components[1]),
        "XOR": float(components[2]),
    }


def l_cont(forecast: np.ndarray, oracle: np.ndarray) -> float:
    deviation = _continuation_deviation(history_grid(forecast), history_grid(oracle))
    return float(np.mean(np.sum(deviation * deviation, axis=-1)))


def l_cont_components(forecast: np.ndarray, oracle: np.ndarray) -> dict:
    deviation = _continuation_deviation(history_grid(forecast), history_grid(oracle))
    components = np.mean(deviation * deviation, axis=(0, 1))
    return {
        "X": float(components[0]),
        "Y": float(components[1]),
        "XOR": float(components[2]),
    }


def _weighted_prefix_loss(forecast: np.ndarray, oracle: np.ndarray, weights: np.ndarray) -> float:
    mass = weights.sum(axis=0)
    if np.any(mass <= 0):
        raise ValueError("a continuation has no weight")
    f_bar = np.sum(weights[:, :, None] * forecast, axis=0) / mass[:, None]
    q_bar = np.sum(weights[:, :, None] * oracle, axis=0) / mass[:, None]
    deviation = (forecast - f_bar[None, :, :]) - (oracle - q_bar[None, :, :])
    squared = np.sum(deviation * deviation, axis=-1)
    return float(np.sum(weights * squared))


def _weighted_continuation_loss(forecast: np.ndarray, oracle: np.ndarray, weights: np.ndarray) -> float:
    mass = weights.sum(axis=1)
    if np.any(mass <= 0):
        raise ValueError("a prefix has no weight")
    f_bar = np.sum(weights[:, :, None] * forecast, axis=1) / mass[:, None]
    q_bar = np.sum(weights[:, :, None] * oracle, axis=1) / mass[:, None]
    deviation = (forecast - f_bar[:, None, :]) - (oracle - q_bar[:, None, :])
    squared = np.sum(deviation * deviation, axis=-1)
    return float(np.sum(weights * squared))


def l_prefix_probability(forecast: np.ndarray, oracle: np.ndarray, probability: np.ndarray) -> float:
    return _weighted_prefix_loss(history_grid(forecast), history_grid(oracle), probability_grid(probability))


def l_cont_probability(forecast: np.ndarray, oracle: np.ndarray, probability: np.ndarray) -> float:
    return _weighted_continuation_loss(
        history_grid(forecast), history_grid(oracle), probability_grid(probability)
    )


def l_prefix_test(forecast: np.ndarray, oracle: np.ndarray, is_test: np.ndarray) -> float:
    forecast_g = history_grid(forecast)
    oracle_g = history_grid(oracle)
    mask = test_mask_grid(is_test)
    f_bar = np.zeros((16, 3), dtype=np.float64)
    q_bar = np.zeros((16, 3), dtype=np.float64)
    for continuation in range(16):
        selected = mask[:, continuation]
        if not np.any(selected):
            raise ValueError("continuation %d has no TEST prefix" % continuation)
        f_bar[continuation] = forecast_g[selected, continuation, :].mean(axis=0)
        q_bar[continuation] = oracle_g[selected, continuation, :].mean(axis=0)
    deviation = (forecast_g - f_bar[None, :, :]) - (oracle_g - q_bar[None, :, :])
    squared = np.sum(deviation * deviation, axis=-1)
    return float(squared[mask].mean())


def l_cont_test(forecast: np.ndarray, oracle: np.ndarray, is_test: np.ndarray) -> float:
    forecast_g = history_grid(forecast)
    oracle_g = history_grid(oracle)
    mask = test_mask_grid(is_test)
    f_bar = np.zeros((16, 3), dtype=np.float64)
    q_bar = np.zeros((16, 3), dtype=np.float64)
    for prefix in range(16):
        selected = mask[prefix, :]
        if not np.any(selected):
            raise ValueError("prefix %d has no TEST continuation" % prefix)
        f_bar[prefix] = forecast_g[prefix, selected, :].mean(axis=0)
        q_bar[prefix] = oracle_g[prefix, selected, :].mean(axis=0)
    deviation = (forecast_g - f_bar[:, None, :]) - (oracle_g - q_bar[:, None, :])
    squared = np.sum(deviation * deviation, axis=-1)
    return float(squared[mask].mean())


def pd_cd_components(oracle: np.ndarray) -> dict:
    grid = history_grid(oracle)
    prefix_mean = grid.mean(axis=0, keepdims=True)
    continuation_mean = grid.mean(axis=1, keepdims=True)
    prefix_components = np.mean((grid - prefix_mean) ** 2, axis=(0, 1))
    continuation_components = np.mean((grid - continuation_mean) ** 2, axis=(0, 1))
    return {
        "PD": float(prefix_components.sum()),
        "PD_X": float(prefix_components[0]),
        "PD_Y": float(prefix_components[1]),
        "PD_XOR": float(prefix_components[2]),
        "CD": float(continuation_components.sum()),
    }


def outcome_bundle(forecast: np.ndarray, world) -> dict:
    oracle = world.q
    components = l_prefix_components(forecast, oracle)
    cont = l_cont_components(forecast, oracle)
    errors = component_excess(forecast, world)
    variation = variation_stats(forecast, world)
    return {
        "L_prefix": l_prefix(forecast, oracle),
        "L_prefix_X": components["X"],
        "L_prefix_Y": components["Y"],
        "L_prefix_XOR": components["XOR"],
        "L_cont": l_cont(forecast, oracle),
        "L_cont_X": cont["X"],
        "L_cont_Y": cont["Y"],
        "L_cont_XOR": cont["XOR"],
        "L_prefix_probability": l_prefix_probability(forecast, oracle, world.probability),
        "L_cont_probability": l_cont_probability(forecast, oracle, world.probability),
        "L_prefix_test": l_prefix_test(forecast, oracle, world.is_test),
        "L_cont_test": l_cont_test(forecast, oracle, world.is_test),
        "PD": float(variation["uniform"]["PD"]),
        "CD": float(variation["uniform"]["CD"]),
        "PD_probability": float(variation["probability"]["PD"]),
        "CD_probability": float(variation["probability"]["CD"]),
        "PD_test": float(variation["test"]["PD"]),
        "CD_test": float(variation["test"]["CD"]),
        "E_TEST_X": float(errors["TEST"]["X"]),
        "E_TEST_Y": float(errors["TEST"]["Y"]),
        "E_TEST_XOR": float(errors["TEST"]["XOR"]),
        "E_TEST_total": float(errors["TEST"]["total"]),
        "E_TRAIN_X": float(errors["TRAIN"]["X"]),
        "E_TRAIN_Y": float(errors["TRAIN"]["Y"]),
        "E_TRAIN_XOR": float(errors["TRAIN"]["XOR"]),
        "E_TRAIN_total": float(errors["TRAIN"]["total"]),
    }


def auc(deltas) -> float:
    """Trapezoidal weights. Zero-dose weight is kept. Nothing is clipped."""
    if len(deltas) != len(AUC_WEIGHTS):
        raise ValueError(len(deltas))
    total = 0.0
    for weight, delta in zip(AUC_WEIGHTS, deltas):
        value = float(delta)
        total += weight * value
    return float(total)


def d_passes(auc_rev: float, random_aucs) -> bool:
    if len(random_aucs) != N_RANDOM:
        return False
    if not math.isfinite(auc_rev):
        return False
    maximum = max(float(value) for value in random_aucs)
    if not math.isfinite(maximum):
        return False
    return bool((auc_rev - maximum) > EPS0)


def m_passes(auc_rev: float, b_prefix: float) -> bool:
    if not math.isfinite(auc_rev) or not math.isfinite(b_prefix):
        return False
    return bool(auc_rev > EPS0 and auc_rev >= (b_prefix / 4.0))


def saturation_index(delta_half: float, delta_one: float):
    if not math.isfinite(delta_half) or not math.isfinite(delta_one):
        return UNDEFINED
    if not (delta_one > EPS0):
        return UNDEFINED
    return float(delta_half / delta_one)


def nondecreasing_steps(deltas) -> int:
    if len(deltas) != len(ALPHAS):
        raise ValueError(len(deltas))
    count = 0
    for earlier, later in zip(deltas, deltas[1:]):
        if float(later) >= float(earlier):
            count += 1
    return count


def rev_rank(rev_delta: float, random_deltas) -> int:
    """1-based rank among 33 paths. A tie keeps the better rank."""
    if len(random_deltas) != N_RANDOM:
        raise ValueError(len(random_deltas))
    better = sum(1 for value in random_deltas if float(value) > float(rev_delta))
    return 1 + better


def random_median(values) -> float:
    ordered = sorted(float(value) for value in values)
    if len(ordered) != N_RANDOM:
        raise ValueError(len(ordered))
    return 0.5 * (ordered[15] + ordered[16])


def divide_by_pd(value: float, pd_value: float):
    if not math.isfinite(value) or not math.isfinite(pd_value) or pd_value <= EPS0:
        return None
    return float(value / pd_value)


def eligibility(
    valid: bool,
    transfer: bool,
    b_prefix: float,
    c_prefix: float,
    displacement: float,
) -> tuple[bool, list[str]]:
    """Eligibility failures are non-passes. They do not by themselves invalidate."""
    reasons = []
    if not valid:
        reasons.append("invalid")
    if not transfer:
        reasons.append("transfer")
    if not math.isfinite(b_prefix) or not (b_prefix > EPS0):
        reasons.append("B_prefix")
    if not math.isfinite(c_prefix) or not (c_prefix > EPS0):
        reasons.append("C_prefix")
    if not math.isfinite(displacement) or not (displacement > EPS0):
        reasons.append("displacement")
    return (len(reasons) == 0), reasons


def joint_pass(valid: bool, eligible: bool, directional: bool, material: bool) -> bool:
    return bool(valid and eligible and directional and material)
