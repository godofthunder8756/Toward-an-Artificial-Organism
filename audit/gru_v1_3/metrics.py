"""Source-study metrics used for replay and for R_exc.

Formulas follow the float64 paths named in the frozen replay map:
component_excess, probability_excess, l_prefix, and the PR #10 normalized components.
"""

from __future__ import annotations

import numpy as np

from audit.gru_v1_3.domain import REPLAY_ATOL, VAR_MAX, population_variance
from audit.gru_v1_3.replay_map import ERROR_KEYS, PR10_E_FIELDS


def history_grid(values: np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    return np.transpose(array.reshape(16, 16, array.shape[-1]), (1, 0, 2))


def component_excess(predictions: np.ndarray, q: np.ndarray, probability: np.ndarray, is_test: np.ndarray) -> dict:
    squared = (predictions - q) ** 2
    out = {}
    for split, flag in (("TRAIN", False), ("TEST", True)):
        mask = is_test if flag else np.logical_not(is_test)
        mass = float(probability[mask].sum())
        weights = np.zeros(probability.shape[0], dtype=np.float64)
        weights[mask] = probability[mask] / mass
        components = (weights[:, None] * squared).sum(axis=0)
        out[split] = {
            "X": float(components[0]),
            "Y": float(components[1]),
            "XOR": float(components[2]),
            "total": float(components.sum()),
        }
    return out


def probability_excess(predictions: np.ndarray, histories: np.ndarray, q: np.ndarray, probability: np.ndarray) -> dict:
    index = np.asarray(histories, dtype=np.int64)
    weights = probability[index]
    weights = weights / weights.sum()
    squared = (predictions - q[index]) ** 2
    components = (weights[:, None] * squared).sum(axis=0)
    return {
        "X": float(components[0]),
        "Y": float(components[1]),
        "XOR": float(components[2]),
        "total": float(components.sum()),
    }


def l_prefix(forecast: np.ndarray, oracle: np.ndarray) -> float:
    forecast_g = history_grid(forecast)
    oracle_g = history_grid(oracle)
    deviation = (forecast_g - forecast_g.mean(axis=0, keepdims=True)) - (
        oracle_g - oracle_g.mean(axis=0, keepdims=True)
    )
    return float(np.mean(np.sum(deviation * deviation, axis=-1)))


def pd_q(oracle: np.ndarray) -> float:
    oracle_g = history_grid(oracle)
    centered = oracle_g - oracle_g.mean(axis=0, keepdims=True)
    return float(np.mean(np.sum(centered * centered, axis=-1)))


def normalized_components(prefix: float, e_total: float, e_xor: float, pd: float, thr_total: float, thr_xor: float) -> dict:
    return {
        "prefix": prefix / (0.25 * pd),
        "total": e_total / thr_total,
        "xor": e_xor / thr_xor,
    }


def e1_block(predictions: np.ndarray, world) -> dict:
    errors = component_excess(predictions, world.q, world.probability, world.is_test)
    prefix = l_prefix(predictions, world.q)
    pd = pd_q(world.q)
    components = normalized_components(
        prefix, errors["TEST"]["total"], errors["TEST"]["XOR"], pd, world.thr_total, world.thr_xor
    )
    return {
        "L_prefix": prefix,
        "PD": pd,
        "E_TEST": errors["TEST"],
        "E_TRAIN": errors["TRAIN"],
        "components": components,
        "T": float(max(components[name] for name in ("prefix", "total", "xor"))),
    }


def excess_brier(outputs: np.ndarray, q: np.ndarray, probability: np.ndarray) -> float:
    per_history = np.sum((outputs - q) ** 2, axis=1)
    return float(probability @ per_history)


def flat_errors(errors: dict) -> dict:
    out = {}
    for split in ("TRAIN", "TEST"):
        for name in ("X", "Y", "XOR", "total"):
            out["%s.%s" % (split, name)] = float(errors[split][name])
    return out


def flat_e_block(block: dict) -> dict:
    out = {
        "L_prefix": float(block["L_prefix"]),
        "PD": float(block["PD"]),
        "T": float(block["T"]),
    }
    for split in ("E_TEST", "E_TRAIN"):
        for name in ("X", "Y", "XOR", "total"):
            out["%s.%s" % (split, name)] = float(block[split][name])
    for name in ("prefix", "total", "xor"):
        out["components.%s" % name] = float(block["components"][name])
    return out


def compare_fields(got: dict, recorded: dict, keys, field_prefix: str) -> list:
    mismatches = []
    for key in keys:
        gv = got[key]
        rv = recorded[key]
        if not np.isfinite(gv) or not np.isfinite(rv) or abs(gv - rv) > REPLAY_ATOL:
            mismatches.append(
                {
                    "field": "%s%s" % (field_prefix, key),
                    "value": None if not np.isfinite(gv) else float(gv),
                    "recorded": None if not np.isfinite(rv) else float(rv),
                    "abs_diff": None if not (np.isfinite(gv) and np.isfinite(rv)) else float(abs(gv - rv)),
                }
            )
    return mismatches


def dig(obj, path: str):
    current = obj
    for part in path.split("."):
        current = current[part]
    return current


def recorded_pr7_errors(seed_json: dict, prefix: str) -> dict:
    node = seed_json
    for part in prefix.split("."):
        node = node[part]
    return {"%s.%s" % (split, name): float(node[split][name]) for split, name in (k.split(".") for k in ERROR_KEYS)}


def recorded_outcome_errors(node: dict) -> dict:
    out = {}
    for split in ("TEST", "TRAIN"):
        for name in ("X", "Y", "XOR", "total"):
            out["%s.%s" % (split, name)] = float(node["E_%s_%s" % (split, name)])
    return out


def recorded_pr10_block(block: dict) -> dict:
    out = {}
    for key in PR10_E_FIELDS:
        out[key] = float(dig(block, key))
    return out


def weighted_mean_sd(w: np.ndarray, values: np.ndarray) -> tuple[float, float, float]:
    var = population_variance(w, values)
    mean = float((w / w.sum()) @ values)
    return mean, float(np.sqrt(var)), var


def weighted_quantiles(w: np.ndarray, values: np.ndarray, probs=(0.25, 0.5, 0.75)) -> dict:
    """Smallest value whose cumulative weight reaches p. Descriptive only."""
    weight = np.asarray(w, dtype=np.float64)
    weight = weight / weight.sum()
    order = np.argsort(values, kind="mergesort")
    cumulative = np.cumsum(weight[order])
    out = {}
    for p in probs:
        index = int(np.searchsorted(cumulative, p, side="left"))
        index = min(index, len(order) - 1)
        out[str(p)] = float(values[order[index]])
    return out


def weighted_correlation(w: np.ndarray, left: np.ndarray, right: np.ndarray):
    weight = np.asarray(w, dtype=np.float64)
    weight = weight / weight.sum()
    vl = population_variance(weight, left)
    vr = population_variance(weight, right)
    if vl <= VAR_MAX or vr <= VAR_MAX:
        return "UNDEFINED"
    ml = float(weight @ left)
    mr = float(weight @ right)
    cov = float(weight @ ((left - ml) * (right - mr)))
    return cov / float(np.sqrt(vl * vr))
