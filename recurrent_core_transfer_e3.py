"""E3-v2 instrument on a model that exposes initial_state, step, and readout.

The frozen PR #5 ratio is computed beside E3-v2 and is not a verdict.
"""

from __future__ import annotations

import math

import numpy as np

from recurrent_core_transfer_spec import (
    ANGLE_MAX_DEG,
    CHART_R2_MIN,
    DECODER_NOT,
    DECODER_OK,
    EPS0,
)
from twostream_acquisition_e3_v2 import (
    UNDEFINED,
    e3_v2_meets,
    e3_v2_ratio,
)
from twostream_acquisition_metrics import (
    _choose_donor,
    _coverage,
    _project,
    _stage4,
    all_bits,
    centered_ridge,
    column_basis,
    continuation_bits,
    continue_from,
    rollout,
)
from twostream_acquisition_oracle import parity_fold
from twostream_acquisition_spec import (
    E3_COMPLEMENT_MIN,
    E3_PARTIAL_MAX,
    E3_WRONG_MAX,
    RATIO_TIE,
)


def principal_angles_deg(left: np.ndarray, right: np.ndarray):
    if left.ndim != 2 or right.ndim != 2 or left.shape[1] == 0 or right.shape[1] == 0:
        return None
    singular = np.linalg.svd(left.T @ right, compute_uv=False)
    singular = np.clip(singular, -1.0, 1.0)
    return [float(np.degrees(np.arccos(value))) for value in singular]


def largest_angle(angles) -> float | None:
    if not angles:
        return None
    return float(max(angles))


def decoder_report(z4: np.ndarray, charts: np.ndarray) -> dict:
    folds = {
        0: np.array([prefix for prefix in range(16) if parity_fold(prefix) == 0]),
        1: np.array([prefix for prefix in range(16) if parity_fold(prefix) == 1]),
    }
    bases = {}
    detail = {}
    for fold, held in folds.items():
        fit = folds[1 - fold]
        weight, intercept, _z_mean, _y_mean = centered_ridge(z4[fit], charts[fit])
        basis, rank, singular = column_basis(weight)
        predicted = z4[held] @ weight + intercept
        r2 = {}
        rmse = {}
        for index, name in enumerate(("m_x", "m_y", "c")):
            target = charts[held, index]
            residual = target - predicted[:, index]
            total = float(np.sum((target - target.mean()) ** 2))
            rmse[name] = float(np.sqrt(np.mean(residual ** 2)))
            if total <= EPS0:
                r2[name] = None
            else:
                r2[name] = float(1.0 - float(np.sum(residual ** 2)) / total)
        bases[fold] = basis
        detail[fold] = {
            "r2": r2,
            "rmse": rmse,
            "singular_values": [float(value) for value in singular],
            "rank": int(rank),
        }
    angles = principal_angles_deg(bases[0], bases[1])
    return {
        "folds": detail,
        "bases": bases,
        "interfold_angles_deg": angles,
        "largest_interfold_angle_deg": largest_angle(angles),
    }


def decoder_label(report: dict) -> str:
    angle = report["largest_interfold_angle_deg"]
    if angle is None or angle > ANGLE_MAX_DEG:
        return DECODER_NOT
    for fold in (0, 1):
        for name in ("m_x", "m_y", "c"):
            value = report["folds"][fold]["r2"][name]
            if value is None or value < CHART_R2_MIN:
                return DECODER_NOT
    return DECODER_OK


def _gap(forecast: np.ndarray, target: np.ndarray, xor_only: bool) -> float:
    if xor_only:
        return float(np.sum((forecast[:, 2] - target[:, 2]) ** 2))
    return float(np.sum((forecast - target) ** 2))


def _pair(numerator: float, denominator: float) -> dict:
    frozen = None if denominator <= RATIO_TIE else float(numerator / denominator)
    try:
        versioned = e3_v2_ratio(numerator, denominator)
    except ValueError:
        versioned = UNDEFINED
    return {
        "numerator": float(numerator),
        "denominator": float(denominator),
        "e3_v2": versioned,
        "frozen_v1": frozen,
    }


def _localized(ratios: dict) -> bool:
    gates = {
        "partial": (E3_PARTIAL_MAX, False),
        "wrong": (E3_WRONG_MAX, False),
        "complement": (E3_COMPLEMENT_MIN, True),
    }
    for name, (threshold, at_least) in gates.items():
        block = ratios.get(name)
        if not block:
            return False
        for kind in ("vector", "xor"):
            if not e3_v2_meets(block[kind]["e3_v2"], threshold, at_least=at_least):
                return False
    return True


def _historical_localized(ratios: dict) -> bool:
    for name in ("partial", "complement", "wrong"):
        for kind in ("vector", "xor"):
            value = ratios[name][kind]["frozen_v1"]
            if value is None:
                return False
            if name == "complement":
                if value < E3_COMPLEMENT_MIN:
                    return False
            elif value > (E3_WRONG_MAX if name == "wrong" else E3_PARTIAL_MAX):
                return False
    return True


def _snapshot_repairs(model):
    if not hasattr(model, "repair_snapshot"):
        return None
    return model.repair_snapshot()


def _continue(model, state, cont, stage0, log, kind):
    before = _snapshot_repairs(model)
    forecast = continue_from(model, state, cont, stage0)
    after = _snapshot_repairs(model)
    if before is not None and after is not None:
        log[kind] = _repair_diff(before, after)
    return forecast


def _repair_diff(before, after) -> dict:
    stage_before, read_before = before
    stage_after, read_after = after
    return {
        "per_stage": [int(stage_after[i] - stage_before[i]) for i in range(8)],
        "readout": int(read_after - read_before),
    }


def run_suite(model, predictions, z4, world, basis_for_fold, rank_ok: bool, ranks: dict) -> dict:
    trials = world.oracle_trials()
    chosen = []
    for trial in trials:
        donor = _choose_donor(trial, z4, basis_for_fold(trial["fold"]))
        if donor is None:
            continue
        chosen.append((trial, donor))
    coverage = _coverage([trial for trial, _donor in chosen], len(trials))
    repairs = {}
    if not chosen:
        return {
            "localized": False,
            "historical_localized": False,
            "coverage_ok": False,
            "coverage": coverage,
            "rank_ok": bool(rank_ok),
            "ranks": ranks,
            "n_chosen": 0,
            "ratios": None,
            "repairs": repairs,
        }
    order = np.argsort([trial["a"] * 256 + trial["b"] * 16 + trial["u"] for trial, _donor in chosen])
    chosen = [chosen[index] for index in order]
    recipients = np.array([trial["a"] for trial, _donor in chosen])
    intended = np.array([trial["b"] for trial, _donor in chosen])
    wrong = np.array([donor for _trial, donor in chosen])
    continuations = np.array([trial["u"] for trial, _donor in chosen])
    cont = continuation_bits(continuations)
    partial_state = np.zeros((len(chosen), z4.shape[1]), dtype=np.float64)
    complement_state = np.zeros_like(partial_state)
    wrong_state = np.zeros_like(partial_state)
    for index, (trial, donor) in enumerate(chosen):
        basis = basis_for_fold(trial["fold"])
        delta_b = z4[trial["b"]] - z4[trial["a"]]
        delta_c = z4[donor] - z4[trial["a"]]
        projected_b = _project(basis, delta_b)
        partial_state[index] = z4[trial["a"]] + projected_b
        complement_state[index] = z4[trial["a"]] + (delta_b - projected_b)
        wrong_state[index] = z4[trial["a"]] + _project(basis, delta_c)
    partial = _continue(model, partial_state, cont, 4, repairs, "partial")
    complement = _continue(model, complement_state, cont, 4, repairs, "complement")
    wrong_forecast = _continue(model, wrong_state, cont, 4, repairs, "wrong")
    ha = recipients | (continuations << 4)
    hb = intended | (continuations << 4)
    hc = wrong | (continuations << 4)
    q_a = world.q[ha]
    q_b = world.q[hb]
    q_c = world.q[hc]
    ratios = {}
    for name, forecast, q_target in (
        ("partial", partial, q_b),
        ("complement", complement, q_b),
        ("wrong", wrong_forecast, q_c),
    ):
        ratios[name] = {
            "vector": _pair(_gap(forecast, q_target, False), _gap(forecast, q_a, False)),
            "xor": _pair(_gap(forecast, q_target, True), _gap(forecast, q_a, True)),
        }
    return {
        "localized": _localized(ratios),
        "historical_localized": _historical_localized(ratios),
        "coverage_ok": bool(coverage["ok"]),
        "coverage_fraction": float(coverage["fraction"]),
        "n_chosen": int(len(chosen)),
        "rank_ok": bool(rank_ok),
        "ranks": ranks,
        "ratios": ratios,
        "repairs": repairs,
        "partial_forecast": partial,
        "wrong_forecast": wrong_forecast,
        "ha": ha,
    }


def zero_effect_gap(suite: dict, intact: np.ndarray) -> float | None:
    """Max abs forecast change of Q-direction transplants versus the intact rollout."""
    if suite["ratios"] is None:
        return None
    gaps = [float(np.max(np.abs(suite["partial_forecast"] - intact[suite["ha"]])))]
    gaps.append(float(np.max(np.abs(suite["wrong_forecast"] - intact[suite["ha"]]))))
    return float(max(gaps))


def instrument(model, world, basis_override=None) -> dict:
    if hasattr(model, "reset_repairs"):
        model.reset_repairs()
    predictions, states = rollout(model, all_bits())
    rollout_repairs = model.repair_snapshot() if hasattr(model, "repair_snapshot") else None
    z4 = np.asarray(_stage4(states), dtype=np.float64)
    decoder = decoder_report(z4, world.stage4_chart)
    if basis_override is None:
        def basis_for_fold(fold):
            return decoder["bases"][fold]

        rank_ok = decoder["folds"][0]["rank"] >= 3 and decoder["folds"][1]["rank"] >= 3
        ranks = {str(fold): decoder["folds"][fold]["rank"] for fold in (0, 1)}
    else:
        def basis_for_fold(_fold):
            return basis_override

        rank_ok = basis_override.shape[1] >= 3
        ranks = {"override": int(basis_override.shape[1])}
    suite = run_suite(model, predictions, z4, world, basis_for_fold, rank_ok, ranks)
    angles_to_q = None
    return {
        "predictions": predictions,
        "z4": z4,
        "decoder": decoder,
        "suite": suite,
        "rollout_repairs": rollout_repairs,
        "angles_to_q": angles_to_q,
        "label": decoder_label(decoder) if basis_override is None else None,
    }


def angles_to_subspace(basis: np.ndarray, subspace: np.ndarray):
    return principal_angles_deg(basis, subspace)


def pack_ratio(value):
    if value is UNDEFINED:
        return "UNDEFINED"
    if value is None:
        return None
    number = float(value)
    if math.isinf(number):
        return "+inf" if number > 0 else "-inf"
    return number


def pack_suite(suite: dict) -> dict:
    ratios = suite["ratios"]
    packed = None
    if ratios is not None:
        packed = {}
        for name, block in ratios.items():
            packed[name] = {}
            for kind, record in block.items():
                packed[name][kind] = {
                    "numerator": record["numerator"],
                    "denominator": record["denominator"],
                    "e3_v2": pack_ratio(record["e3_v2"]),
                    "frozen_v1": pack_ratio(record["frozen_v1"]),
                }
    return {
        "localized": bool(suite["localized"]),
        "historical_localized": bool(suite["historical_localized"]),
        "coverage_ok": bool(suite["coverage_ok"]),
        "coverage_fraction": suite.get("coverage_fraction"),
        "n_chosen": suite["n_chosen"],
        "rank_ok": bool(suite["rank_ok"]),
        "ranks": suite["ranks"],
        "ratios": packed,
        "repairs": suite["repairs"],
    }
