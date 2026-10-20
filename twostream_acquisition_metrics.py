"""Evaluation, precision curves, and prespecified interventions.

Training is float32. Every number that enters a verdict is computed here in
float64 from the frozen oracle. Chart values are analysis targets only.
"""

from __future__ import annotations

import numpy as np
import torch

from twostream_chart import marginals_covariance
from twostream_constants import A, BX, BY, E, ETA
from twostream_filter import filter_prefix, fraction_transition
from twostream_acquisition_models import eval_copy, parameter_counts
from twostream_acquisition_oracle import parity_fold
from twostream_acquisition_spec import (
    B_GRID,
    CHART_R2_MIN,
    CONSTANT_SPAN,
    COVERAGE_MIN,
    E3_COMPLEMENT_MIN,
    E3_PARTIAL_MAX,
    E3_WRONG_MAX,
    IDENTITY_TOL,
    MIN_DISTINCT,
    NORM_MATCH,
    RANK_RELATIVE,
    RATIO_TIE,
    RIDGE_LAMBDA,
    TAU_DEN,
)

_BITS = None
_MATRIX = None
_PREFIX_CHART = {}


def all_bits() -> np.ndarray:
    global _BITS
    if _BITS is None:
        bits = np.zeros((256, 8), dtype=np.float64)
        for history in range(256):
            for stage in range(8):
                bits[history, stage] = (history >> stage) & 1
        _BITS = bits
    return _BITS


def component_excess(preds: np.ndarray, world) -> dict:
    squared = (preds - world.q) ** 2
    out = {}
    for split, test in (("TRAIN", False), ("TEST", True)):
        weights = world.split_weights(test)
        components = (weights[:, None] * squared).sum(axis=0)
        out[split] = {
            "X": float(components[0]),
            "Y": float(components[1]),
            "XOR": float(components[2]),
            "total": float(components.sum()),
        }
    return out


def afit_holds(errors: dict, world, split: str) -> bool:
    total = errors[split]["total"]
    xor = errors[split]["XOR"]
    if not np.isfinite(total) or not np.isfinite(xor):
        return False
    return bool(
        total <= float(world.afit_threshold[split]["total"])
        and xor <= float(world.afit_threshold[split]["XOR"])
    )


def outputs_valid(preds: np.ndarray) -> bool:
    return bool(np.isfinite(preds).all() and np.all(preds > 0.0) and np.all(preds < 1.0))


@torch.inference_mode()
def rollout(model, bits: np.ndarray):
    bits_t = torch.from_numpy(np.ascontiguousarray(bits, dtype=np.float64))
    batch = bits_t.shape[0]
    parameter = next(model.parameters())
    state = model.initial_state(batch, parameter.dtype, parameter.device)
    states = []
    for stage in range(bits_t.shape[1]):
        state = model.step(state, bits_t[:, stage], stage)
        states.append(state.detach().cpu().numpy().copy())
    predictions = model.readout(state).detach().cpu().numpy().copy()
    return predictions, states


@torch.inference_mode()
def continue_from(model, state_np: np.ndarray, cont_bits: np.ndarray, stage0: int):
    parameter = next(model.parameters())
    if state_np.dtype.kind in "iu":
        state = torch.from_numpy(np.ascontiguousarray(state_np.astype(np.int64)))
    else:
        state = torch.from_numpy(np.ascontiguousarray(state_np.astype(np.float64))).to(parameter.dtype)
    if cont_bits.shape[1] == 0:
        return model.readout(state).detach().cpu().numpy().copy()
    cont = torch.from_numpy(np.ascontiguousarray(cont_bits.astype(np.float64)))
    for offset in range(cont.shape[1]):
        state = model.step(state, cont[:, offset], stage0 + offset)
    return model.readout(state).detach().cpu().numpy().copy()


def continuation_bits(continuations: np.ndarray) -> np.ndarray:
    out = np.zeros((len(continuations), 4), dtype=np.float64)
    for index in range(4):
        out[:, index] = (continuations >> index) & 1
    return out


def predict_only(model, world):
    copied = eval_copy(model)
    predictions, states = rollout(copied, all_bits())
    errors = component_excess(predictions, world)
    return {
        "errors": errors,
        "afit_test": afit_holds(errors, world, "TEST"),
        "afit_train": afit_holds(errors, world, "TRAIN"),
        "outputs_valid": outputs_valid(predictions),
        "predictions": predictions,
        "states": states,
        "model": copied,
    }


def _stage4(states):
    return np.stack([states[3][prefix] for prefix in range(16)], axis=0)


def identity_checks(model, predictions, states) -> dict:
    """Whole-state transplant and restoration. Both are integrity checks."""
    vector = states[0].ndim == 2
    z4 = _stage4(states)
    pairs_a = []
    pairs_b = []
    pairs_u = []
    for recipient in range(16):
        for donor in range(16):
            if recipient == donor:
                continue
            for continuation in range(16):
                pairs_a.append(recipient)
                pairs_b.append(donor)
                pairs_u.append(continuation)
    recipients = np.asarray(pairs_a)
    donors = np.asarray(pairs_b)
    continuations = np.asarray(pairs_u)
    transplanted = continue_from(model, z4[donors], continuation_bits(continuations), 4)
    native_index = donors | (continuations << 4)
    gap = np.max(np.abs(transplanted - predictions[native_index]))
    restoration = 0.0
    bits = all_bits()
    for stage in (5, 6, 7, 8):
        saved = states[stage - 1]
        if stage == 8:
            restored = model.readout(
                _torch_state(model, saved)
            ).detach().cpu().numpy()
        else:
            restored = continue_from(model, saved, bits[:, stage:], stage)
        restoration = max(restoration, float(np.max(np.abs(restored - predictions))))
    return {
        "whole_state_max_abs": float(gap),
        "restoration_max_abs": float(restoration),
        "whole_state_ok": bool(gap <= IDENTITY_TOL),
        "restoration_ok": bool(restoration <= IDENTITY_TOL),
        "ok": bool(gap <= IDENTITY_TOL and restoration <= IDENTITY_TOL),
        "vector_state": vector,
        "n_transplant_trials": int(len(continuations)),
    }


def _torch_state(model, state_np):
    parameter = next(model.parameters())
    if state_np.dtype.kind in "iu":
        return torch.from_numpy(np.ascontiguousarray(state_np.astype(np.int64)))
    return torch.from_numpy(np.ascontiguousarray(state_np.astype(np.float64))).to(parameter.dtype)


def centered_ridge(states: np.ndarray, targets: np.ndarray, lam: float = RIDGE_LAMBDA):
    """Centered least squares with an unpenalized intercept and Frobenius penalty lam."""
    z_mean = states.mean(axis=0)
    y_mean = targets.mean(axis=0)
    centered_z = states - z_mean
    centered_y = targets - y_mean
    hidden = states.shape[1]
    gram = centered_z.T @ centered_z
    gram.flat[:: hidden + 1] += lam
    try:
        weight = np.linalg.solve(gram, centered_z.T @ centered_y)
    except np.linalg.LinAlgError:
        weight = np.linalg.lstsq(gram, centered_z.T @ centered_y, rcond=None)[0]
    intercept = y_mean - z_mean @ weight
    return weight, intercept, z_mean, y_mean


def column_basis(weight: np.ndarray):
    if weight.size == 0:
        return np.zeros((weight.shape[0], 0)), 0, np.zeros(0)
    u_factor, singular, _vt = np.linalg.svd(weight, full_matrices=False)
    if singular.size == 0 or singular[0] == 0:
        return np.zeros((weight.shape[0], 0)), 0, singular
    rank = int(np.sum(singular > RANK_RELATIVE * singular[0]))
    return u_factor[:, :rank], rank, singular


def _project(basis: np.ndarray, delta: np.ndarray) -> np.ndarray:
    if basis.ndim != 2 or basis.shape[1] == 0:
        return np.zeros_like(delta)
    return basis @ (basis.T @ delta)


def _rho(forecast, q_target, q_recipient, xor_only: bool):
    if xor_only:
        numerator = np.sum((forecast[:, 2] - q_target[:, 2]) ** 2)
        denominator = np.sum((forecast[:, 2] - q_recipient[:, 2]) ** 2)
    else:
        numerator = np.sum((forecast - q_target) ** 2)
        denominator = np.sum((forecast - q_recipient) ** 2)
    if denominator <= RATIO_TIE:
        return None
    return float(numerator / denominator)


def _vector_summaries(forecast, native, q_target, q_recipient):
    """Absolute (L1 and squared L2) and normalized errors against Delta-star."""
    delta_star = q_target - q_recipient
    delta_f = forecast - native
    residual = delta_f - delta_star
    squared = np.sum(residual ** 2, axis=1)
    absolute = np.abs(residual)
    summed = absolute.sum(axis=1)
    norm = np.linalg.norm(delta_star, axis=1)
    large = norm >= TAU_DEN
    normalized = np.full_like(absolute, np.nan)
    normalized_sum = np.full(len(norm), np.nan)
    if np.any(large):
        normalized[large] = absolute[large] / norm[large, None]
        normalized_sum[large] = summed[large] / norm[large]
    return {
        "squared_l2_mean": float(np.mean(squared)) if len(squared) else None,
        "absolute_per_query_mean": [float(np.mean(absolute[:, i])) for i in range(3)] if len(squared) else None,
        "absolute_summed_mean": float(np.mean(summed)) if len(squared) else None,
        "normalized_per_query_mean": [
            None if not np.any(large) else float(np.nanmean(normalized[:, i])) for i in range(3)
        ],
        "normalized_summed_mean": None if not np.any(large) else float(np.nanmean(normalized_sum)),
        "n_trials": int(len(squared)),
        "n_below_tau": int(np.sum(~large)) if len(squared) else 0,
        "xor_squared_mean": float(np.mean(residual[:, 2] ** 2)) if len(squared) else None,
    }


def _empty_suite(reason: str) -> dict:
    return {
        "applicable": False,
        "reason": reason,
        "localized": False,
        "coverage_ok": False,
        "rank_ok": False,
        "descriptive_only": True,
    }


def _choose_donor(trial, z4, basis):
    if not trial["xor_separated"] or not trial["candidates"]:
        return None
    target_norm = np.linalg.norm(_project(basis, z4[trial["b"]] - z4[trial["a"]]))
    best = None
    best_gap = None
    for candidate in trial["candidates"]:
        candidate_norm = np.linalg.norm(_project(basis, z4[candidate] - z4[trial["a"]]))
        if target_norm == 0.0:
            if candidate_norm != 0.0:
                continue
        else:
            lower = (1.0 - NORM_MATCH) * target_norm
            upper = (1.0 + NORM_MATCH) * target_norm
            if candidate_norm < lower or candidate_norm > upper:
                continue
        gap = abs(candidate_norm - target_norm)
        if best is None or gap < best_gap or (gap == best_gap and candidate < best):
            best = candidate
            best_gap = gap
    return best


def _coverage(eligible, n_cross: int) -> dict:
    recipients = {0: set(), 1: set()}
    donors = {0: set(), 1: set()}
    for trial in eligible:
        recipients[trial["fold"]].add(trial["a"])
        donors[trial["fold"]].add(trial["b"])
    fraction = (len(eligible) / n_cross) if n_cross else 0.0
    ok = (
        n_cross > 0
        and fraction >= COVERAGE_MIN
        and all(len(recipients[fold]) >= MIN_DISTINCT and len(donors[fold]) >= MIN_DISTINCT for fold in (0, 1))
    )
    return {
        "n_cross_fitted": n_cross,
        "n_eligible": len(eligible),
        "fraction": fraction,
        "recipients": {str(fold): sorted(recipients[fold]) for fold in (0, 1)},
        "donors": {str(fold): sorted(donors[fold]) for fold in (0, 1)},
        "ok": bool(ok),
    }


def _suite_from_trials(model, predictions, z4, world, trials, basis_for_fold, descriptive_only: bool, rank_ok: bool, ranks: dict):
    n_cross = len(trials)
    chosen = []
    n_xor = 0
    n_dropped = 0
    for trial in trials:
        if trial["xor_separated"]:
            n_xor += 1
        donor = _choose_donor(trial, z4, basis_for_fold(trial["fold"]))
        if trial["xor_separated"] and donor is None:
            n_dropped += 1
        if donor is None:
            continue
        chosen.append((trial, donor))
    coverage = _coverage([trial for trial, _donor in chosen], n_cross)
    if not chosen:
        return {
            "applicable": True,
            "descriptive_only": descriptive_only,
            "rank_ok": bool(rank_ok),
            "ranks": ranks,
            "localized": False,
            "coverage_ok": False,
            "coverage": coverage,
            "n_xor_separated": n_xor,
            "n_dropped_no_wrong_donor": n_dropped,
            "ratios": None,
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
    partial = continue_from(model, partial_state, cont, 4)
    complement = continue_from(model, complement_state, cont, 4)
    wrong_forecast = continue_from(model, wrong_state, cont, 4)
    ha = recipients | (continuations << 4)
    hb = intended | (continuations << 4)
    hc = wrong | (continuations << 4)
    native = predictions[ha]
    q_a = world.q[ha]
    q_b = world.q[hb]
    q_c = world.q[hc]
    ratios = {}
    summaries = {}
    for name, forecast, q_target in (
        ("partial", partial, q_b),
        ("complement", complement, q_b),
        ("wrong", wrong_forecast, q_c),
    ):
        ratios[name] = {
            "vector": _rho(forecast, q_target, q_a, False),
            "xor": _rho(forecast, q_target, q_a, True),
        }
        summaries[name] = _vector_summaries(forecast, native, q_target, q_a)
    localized = all(
        ratios[name]["vector"] is not None
        and ratios[name]["xor"] is not None
        and (
            ratios[name]["vector"] <= E3_PARTIAL_MAX
            if name != "complement"
            else ratios[name]["vector"] >= E3_COMPLEMENT_MIN
        )
        and (
            ratios[name]["xor"] <= (E3_WRONG_MAX if name == "wrong" else E3_PARTIAL_MAX)
            if name != "complement"
            else ratios[name]["xor"] >= E3_COMPLEMENT_MIN
        )
        for name in ("partial", "complement", "wrong")
    )
    return {
        "applicable": True,
        "descriptive_only": descriptive_only,
        "rank_ok": bool(rank_ok),
        "ranks": ranks,
        "localized": bool(localized),
        "coverage_ok": bool(coverage["ok"]),
        "coverage": coverage,
        "n_xor_separated": n_xor,
        "n_dropped_no_wrong_donor": n_dropped,
        "ratios": ratios,
        "errors": summaries,
    }


def _cross_fit_bases(z4, charts):
    folds = {
        0: np.array([prefix for prefix in range(16) if parity_fold(prefix) == 0]),
        1: np.array([prefix for prefix in range(16) if parity_fold(prefix) == 1]),
    }
    fits = {}
    for fold, members in folds.items():
        other = folds[1 - fold]
        weight, intercept, z_mean, y_mean = centered_ridge(z4[other], charts[other])
        basis, rank, singular = column_basis(weight)
        fits[fold] = {
            "basis": basis,
            "rank": rank,
            "singular": [float(value) for value in singular],
            "held_out_prefixes": members.tolist(),
            "fit_prefixes": other.tolist(),
        }
    weight, _intercept, _z_mean, _y_mean = centered_ridge(z4, charts)
    basis, rank, singular = column_basis(weight)
    all16 = {"basis": basis, "rank": rank, "singular": [float(value) for value in singular]}
    return fits, all16


def _pca_basis(states, world):
    rows = states[3][np.where(~world.is_test)[0]]
    centered = rows - rows.mean(axis=0)
    _u, _s, vt = np.linalg.svd(centered, full_matrices=False)
    width = min(3, vt.shape[0])
    return vt[:width].T


def _donor_tracking(predictions, world, trials):
    if not trials:
        return {"vector": None, "xor": None, "n": 0}
    hb = np.array([trial["hb"] for trial in trials])
    ha = np.array([trial["ha"] for trial in trials])
    forecast = predictions[hb]
    return {
        "vector": _rho(forecast, world.q[hb], world.q[ha], False),
        "xor": _rho(forecast, world.q[hb], world.q[ha], True),
        "n": int(len(trials)),
    }


def _nearest(model, predictions, z4, world, basis_for_fold):
    recipients = []
    donors = []
    continuations = []
    for recipient in range(16):
        donor = int(world.nearest_posterior[recipient])
        for continuation in range(16):
            recipients.append(recipient)
            donors.append(donor)
            continuations.append(continuation)
    recipients = np.asarray(recipients)
    donors = np.asarray(donors)
    continuations = np.asarray(continuations)
    partial_state = np.zeros((len(recipients), z4.shape[1]), dtype=np.float64)
    for index, recipient in enumerate(recipients):
        donor = donors[index]
        basis = basis_for_fold(parity_fold(int(recipient)))
        partial_state[index] = z4[recipient] + _project(basis, z4[donor] - z4[recipient])
    partial = continue_from(model, partial_state, continuation_bits(continuations), 4)
    ha = recipients | (continuations << 4)
    hn = donors | (continuations << 4)
    native = predictions[ha]
    whole = predictions[hn]
    q_a = world.q[ha]
    q_n = world.q[hn]
    return {
        "donor": world.nearest_posterior.tolist(),
        "tv": [float(value) for value in world.nearest_tv],
        "whole": _vector_summaries(whole, native, q_n, q_a),
        "partial": _vector_summaries(partial, native, q_n, q_a),
    }


def _random_probes(model, z4, predictions, world, eligible, basis_for_fold, seed: int):
    if not eligible:
        return {"n": 0, "direction": None, "subspace": None}
    generator = torch.Generator(device="cpu")
    generator.manual_seed(7000 + seed)
    hidden = z4.shape[1]
    direction_state = np.zeros((len(eligible), hidden), dtype=np.float64)
    subspace_state = np.zeros_like(direction_state)
    continuations = []
    recipients = []
    intended = []
    for index, trial in enumerate(eligible):
        basis = basis_for_fold(trial["fold"])
        scale = np.linalg.norm(_project(basis, z4[trial["b"]] - z4[trial["a"]]))
        direction = torch.randn(hidden, generator=generator).numpy()
        norm = np.linalg.norm(direction)
        if norm > 0 and scale > 0:
            direction = direction / norm * scale
        else:
            direction = np.zeros(hidden)
        raw = torch.randn(hidden, 3, generator=generator).numpy()
        q_factor, _r = np.linalg.qr(raw)
        width = min(3, q_factor.shape[1])
        projected = q_factor[:, :width] @ (q_factor[:, :width].T @ (z4[trial["b"]] - z4[trial["a"]]))
        projected_norm = np.linalg.norm(projected)
        if projected_norm > 0 and scale > 0:
            projected = projected * (scale / projected_norm)
        elif scale == 0:
            projected = np.zeros(hidden)
        direction_state[index] = z4[trial["a"]] + direction
        subspace_state[index] = z4[trial["a"]] + projected
        continuations.append(trial["u"])
        recipients.append(trial["a"])
        intended.append(trial["b"])
    cont = continuation_bits(np.asarray(continuations))
    direction_forecast = continue_from(model, direction_state, cont, 4)
    subspace_forecast = continue_from(model, subspace_state, cont, 4)
    ha = np.asarray(recipients) | (np.asarray(continuations) << 4)
    hb = np.asarray(intended) | (np.asarray(continuations) << 4)
    native = predictions[ha]

    def pack(forecast):
        return {
            "rho_vector_vs_intended": _rho(forecast, world.q[hb], world.q[ha], False),
            "rho_xor_vs_intended": _rho(forecast, world.q[hb], world.q[ha], True),
            "errors": _vector_summaries(forecast, native, world.q[hb], world.q[ha]),
        }

    return {"n": len(eligible), "direction": pack(direction_forecast), "subspace": pack(subspace_forecast)}


def interventions(model, predictions, states, world, seed: int) -> dict:
    if states[0].ndim != 2:
        return _empty_suite("K-TAB state is a discrete history index; vector interventions are not applicable")
    z4 = np.asarray(_stage4(states), dtype=np.float64)
    hidden = z4.shape[1]
    trials = world.oracle_trials()
    tracking = _donor_tracking(predictions, world, trials)
    if hidden < 4:
        basis = np.eye(hidden)
        suite = _suite_from_trials(
            model,
            predictions,
            z4,
            world,
            trials,
            lambda _fold: basis,
            True,
            False,
            {"note": "whole 2-d state; chart subspace not fitted"},
        )
        suite["donor_tracking"] = tracking
        suite["nearest_posterior"] = _nearest(model, predictions, z4, world, lambda _fold: basis)
        eligible = []
        for trial in trials:
            if _choose_donor(trial, z4, basis) is not None:
                eligible.append(trial)
        eligible.sort(key=lambda trial: (trial["a"], trial["b"], trial["u"]))
        suite["random"] = _random_probes(
            model, z4, predictions, world, eligible, lambda _fold: basis, seed
        )
        suite["all16"] = None
        suite["pca"] = None
        suite["note"] = "H<4 uses the whole state; statistics are descriptive only"
        return suite
    charts = world.stage4_chart
    fits, all16 = _cross_fit_bases(z4, charts)
    rank_ok = fits[0]["rank"] >= 3 and fits[1]["rank"] >= 3

    def basis_for_fold(fold):
        return fits[fold]["basis"]

    primary = _suite_from_trials(
        model, predictions, z4, world, trials, basis_for_fold, False, rank_ok,
        {str(fold): fits[fold]["rank"] for fold in (0, 1)},
    )
    primary["singular_values"] = {str(fold): fits[fold]["singular"] for fold in (0, 1)}
    primary["donor_tracking"] = tracking
    primary["nearest_posterior"] = _nearest(model, predictions, z4, world, basis_for_fold)
    # Eligible trials in the same order the suite used, for the random probe.
    eligible = []
    for trial in trials:
        donor = _choose_donor(trial, z4, basis_for_fold(trial["fold"]))
        if donor is not None:
            eligible.append(trial)
    eligible.sort(key=lambda trial: (trial["a"], trial["b"], trial["u"]))
    primary["random"] = _random_probes(model, z4, predictions, world, eligible, basis_for_fold, seed)
    all_basis = all16["basis"]
    primary["all16"] = _suite_from_trials(
        model, predictions, z4, world, trials, lambda _fold: all_basis, True, all16["rank"] >= 3,
        {"all16": all16["rank"]},
    )
    primary["all16"]["note"] = "descriptive fit on all 16 prefixes"
    pca = _pca_basis(states, world)
    primary["pca"] = _suite_from_trials(
        model, predictions, z4, world, trials, lambda _fold: pca, True, pca.shape[1] >= 3,
        {"pca": int(pca.shape[1])},
    )
    primary["pca"]["note"] = "exploratory; failure means not localized by this intervention"
    return primary


def chart_probe(states, world) -> dict:
    if states[0].ndim != 2:
        return {"applicable": False, "reason": "no vector state at stage 8"}
    z8 = np.asarray(states[7], dtype=np.float64)
    train = np.where(~world.is_test)[0]
    test = np.where(world.is_test)[0]
    _weight, _intercept, z_mean, y_mean = centered_ridge(z8[train], world.chart[train])
    weight = _weight
    predicted = (z8[test] - z_mean) @ weight + y_mean
    scores = {}
    names = ("m_x", "m_y", "c")
    accessible = True
    for index, name in enumerate(names):
        target = world.chart[test, index]
        total = np.sum((target - target.mean()) ** 2)
        if total == 0:
            scores[name] = None
            accessible = False
            continue
        residual = np.sum((target - predicted[:, index]) ** 2)
        scores[name] = float(1.0 - residual / total)
        if scores[name] < CHART_R2_MIN:
            accessible = False
    return {"applicable": True, "r2": scores, "accessible": bool(accessible)}


def geometry_correlation(z4_init, z4_final):
    if z4_init.ndim != 2:
        return None

    def distances(z4):
        gap = z4[:, None, :] - z4[None, :, :]
        return np.sqrt(np.sum(gap ** 2, axis=-1))

    index = np.triu_indices(16, 1)
    left = distances(np.asarray(z4_init, dtype=np.float64))[index]
    right = distances(np.asarray(z4_final, dtype=np.float64))[index]
    if np.std(left) == 0 or np.std(right) == 0:
        return None
    return float(np.corrcoef(left, right)[0, 1])


def recurrent_change(model, init_state: dict) -> dict:
    keys = [key for key in init_state if key.startswith("rnn.") or key.startswith("update_")]
    if not keys:
        final = model.state_dict()["logits"].detach().double().reshape(-1)
        initial = init_state["logits"].double().reshape(-1)
        absolute = float(torch.linalg.vector_norm(final - initial))
        return {
            "relative": None,
            "absolute": absolute,
            "note": "K-TAB is initialized at 0, so the relative change is undefined",
        }
    final_state = model.state_dict()
    delta = torch.cat([(final_state[key].detach().double() - init_state[key].double()).reshape(-1) for key in keys])
    base = torch.cat([init_state[key].double().reshape(-1) for key in keys])
    base_norm = float(torch.linalg.vector_norm(base))
    absolute = float(torch.linalg.vector_norm(delta))
    relative = None if base_norm == 0 else absolute / base_norm
    return {"relative": relative, "absolute": absolute, "n_parameters": int(base.numel())}


def round_ties_even(index: np.ndarray, levels: int) -> np.ndarray:
    """Nearest integer, ties to even, then clipped to 0..levels."""
    clipped = np.clip(index, 0.0, levels)
    return np.clip(np.rint(clipped), 0.0, levels)


def quantize_coordinates(values: np.ndarray, lo: np.ndarray, hi: np.ndarray, bits: int):
    """Quantize the last axis. lo and hi already carry float32 endpoints."""
    values = np.asarray(values, dtype=np.float64)
    lo = np.asarray(lo, dtype=np.float64)
    hi = np.asarray(hi, dtype=np.float64)
    span = hi - lo
    constant = span < CONSTANT_SPAN
    outside = (values < lo) | (values > hi)
    clipped = np.minimum(np.maximum(values, lo), hi)
    levels = (1 << bits) - 1
    index = np.zeros_like(clipped)
    active = ~constant
    index[..., active] = (clipped[..., active] - lo[active]) * levels / span[active]
    rounded = round_ties_even(index, levels)
    reconstructed = lo + rounded * (span / levels)
    reconstructed[..., constant] = lo[constant]
    return reconstructed, outside, constant


def state_ranges(states, world):
    ranges = []
    for stage in range(1, 9):
        mask = (1 << stage) - 1
        representatives = []
        for prefix in world.train_prefixes[stage]:
            for history in range(256):
                if (not world.is_test[history]) and (history & mask) == prefix:
                    representatives.append(states[stage - 1][history])
                    break
        stacked = np.stack(representatives, axis=0).astype(np.float64)
        lo = stacked.min(axis=0).astype(np.float32).astype(np.float64)
        hi = stacked.max(axis=0).astype(np.float32).astype(np.float64)
        ranges.append((lo, hi))
    return ranges


@torch.inference_mode()
def rollout_quantized(model, ranges, bits: int):
    bits_np = all_bits()
    bits_t = torch.from_numpy(bits_np)
    parameter = next(model.parameters())
    state = model.initial_state(bits_t.shape[0], parameter.dtype, parameter.device)
    clip_counts = []
    for stage in range(8):
        state = model.step(state, bits_t[:, stage], stage)
        reconstructed, outside, _constant = quantize_coordinates(
            state.detach().cpu().numpy(), ranges[stage][0], ranges[stage][1], bits
        )
        clip_counts.append(int(np.sum(outside)))
        state = torch.from_numpy(np.ascontiguousarray(reconstructed)).to(parameter.dtype)
    predictions = model.readout(state).detach().cpu().numpy().copy()
    return predictions, clip_counts


def precision_report(model, states, world, hidden: int):
    if states[0].ndim != 2:
        return {
            "applicable": False,
            "b_sel": "exact index; logits unquantized",
            "confirmation": "NOT CONFIRMED",
            "note": "K-TAB logits are not quantized",
        }
    ranges = state_ranges(states, world)
    curve = []
    selected = None
    for bits in B_GRID:
        predictions, clips = rollout_quantized(model, ranges, bits)
        valid = outputs_valid(predictions)
        errors = component_excess(predictions, world) if valid else None
        passed = bool(valid and afit_holds(errors, world, "TRAIN"))
        curve.append(
            {
                "b": bits,
                "train_afit": passed,
                "outputs_valid": valid,
                "errors": errors,
                "clip_counts": clips,
            }
        )
        if passed and selected is None:
            selected = bits
    if selected is None:
        return {
            "applicable": True,
            "b_sel": "no qualifying precision in the declared grid",
            "confirmation": "NOT CONFIRMED",
            "curve": curve,
            "ranges_constant": _constant_mask(ranges),
            "charged_state_bits_nominal": None,
            "charged_state_bits_stagewise": None,
            "metadata_bits": 64 * hidden * 8,
        }
    chosen = next(row for row in curve if row["b"] == selected)
    confirmed = "CONFIRMED" if afit_holds(chosen["errors"], world, "TEST") else "NOT CONFIRMED"
    constant = _constant_mask(ranges)
    stagewise = []
    for mask in constant:
        stagewise.append(int((~np.asarray(mask)).sum()) * selected)
    return {
        "applicable": True,
        "b_sel": selected,
        "confirmation": confirmed,
        "curve": curve,
        "ranges_constant": constant,
        "charged_state_bits_nominal": hidden * selected,
        "charged_state_bits_stagewise": stagewise,
        "metadata_bits": 64 * hidden * 8,
    }


def _constant_mask(ranges):
    masks = []
    for lo, hi in ranges:
        masks.append((hi - lo < CONSTANT_SPAN).tolist())
    return masks


def ledger(spec, counts: dict, precision: dict) -> dict:
    if spec.arm == "K-TAB":
        return {
            "persistent_state": "history/index buffer, max 8 bits",
            "state_bits": 8,
            "b_sel": precision.get("b_sel"),
            "stage_information": "subsumed by the index",
            "update_parameters": "0",
            "readout_storage_bits": 768 * 32,
            "quantizer_metadata_bits": 0,
        }
    frozen = spec.freeze_recurrent
    update = (
        "0 trained + %d frozen-random" % counts["recurrent"]
        if frozen
        else counts["recurrent"] * 32
    )
    return {
        "persistent_state": "d=%d" % spec.hidden,
        "state_bits_nominal": precision.get("charged_state_bits_nominal"),
        "state_bits_stagewise": precision.get("charged_state_bits_stagewise"),
        "b_sel": precision.get("b_sel"),
        "confirmation": precision.get("confirmation"),
        "stage_information_bits_per_step": 3,
        "update_parameters": update,
        "readout_storage_bits": counts["readout"] * 32,
        "quantizer_metadata_bits": precision.get("metadata_bits"),
    }


def full_analysis(model, spec, world, init_state, init_eval, train_info) -> dict:
    copied = eval_copy(model)
    predictions, states = rollout(copied, all_bits())
    errors = component_excess(predictions, world)
    valid = outputs_valid(predictions)
    identity = identity_checks(copied, predictions, states)
    integrity = bool(train_info["integrity_training"] and valid and identity["ok"] and init_eval["outputs_valid"])
    precision = precision_report(copied, states, world, spec.hidden)
    counts = parameter_counts(model)
    record = {
        "arm": spec.arm,
        "cell": spec.cell,
        "hidden": spec.hidden,
        "seed": spec.seed,
        "configuration": spec.configuration(),
        "freeze_recurrent": spec.freeze_recurrent,
        "parameter_counts": counts,
        "training": train_info,
        "init": {
            "errors": init_eval["errors"],
            "afit_test": init_eval["afit_test"],
            "afit_train": init_eval["afit_train"],
            "outputs_valid": init_eval["outputs_valid"],
        },
        "final": {
            "errors": errors,
            "afit_test": afit_holds(errors, world, "TEST") if valid else False,
            "afit_train": afit_holds(errors, world, "TRAIN") if valid else False,
            "outputs_valid": valid,
        },
        "change": _change(init_eval["errors"], errors),
        "alearn": (not init_eval["afit_test"]),
        "integrity": integrity,
        "identity": {key: value for key, value in identity.items()},
        "recurrent_change": recurrent_change(model, init_state),
        "geometry_correlation": geometry_correlation(_stage4(init_eval["states"]), _stage4(states)),
        "precision": precision,
        "ledger": ledger(spec, counts, precision),
        "interventions": interventions(copied, predictions, states, world, spec.seed) if valid else _empty_suite("invalid outputs"),
        "chart_probe": chart_probe(states, world) if valid else {"applicable": False, "accessible": False},
        "complete": True,
    }
    return record


def _change(init_errors, final_errors):
    out = {}
    for split in ("TRAIN", "TEST"):
        out[split] = {
            key: final_errors[split][key] - init_errors[split][key]
            for key in ("X", "Y", "XOR", "total")
        }
    return out


def _observe_f(mx, my, c, variable, bit):
    e = float(E)
    eta = float(ETA)
    if variable == "X":
        observed, other = mx, my
    else:
        observed, other = my, mx
    p1 = e + eta * observed
    predictive = p1 if bit == 1 else 1.0 - p1
    if bit == 1:
        observed_2 = (1.0 - e) * observed / predictive
        other_2 = other + eta * c / predictive
    else:
        observed_2 = e * observed / predictive
        other_2 = other - eta * c / predictive
    c_2 = e * (1.0 - e) * c / (predictive * predictive)
    if variable == "X":
        return observed_2, other_2, c_2
    return other_2, observed_2, c_2


def _transit_f(mx, my, c):
    a = float(A)
    bx = float(BX)
    by = float(BY)
    mx_2 = 0.5 + a * bx * (mx - 0.5)
    my_2 = 0.5 + a * by * (my - 0.5)
    created = (1.0 - a * a) * (mx - 0.5) * (my - 0.5)
    c_2 = bx * by * (c + created)
    return mx_2, my_2, c_2


def _repair(mx, my, c):
    mx2 = min(1.0, max(0.0, mx))
    my2 = min(1.0, max(0.0, my))
    lower = max(-mx2 * my2, -(1.0 - mx2) * (1.0 - my2))
    upper = min(mx2 * (1.0 - my2), my2 * (1.0 - mx2))
    c2 = min(upper, max(lower, c))
    changed = (mx2 != mx) or (my2 != my) or (c2 != c)
    return mx2, my2, c2, changed


def _prefix_chart(prefix: int, stage: int) -> np.ndarray:
    global _MATRIX
    if _MATRIX is None:
        _MATRIX = fraction_transition()
    key = (prefix, stage)
    if key not in _PREFIX_CHART:
        belief, _probability = filter_prefix(prefix, stage, _MATRIX)
        mx, my, c = marginals_covariance(belief)
        _PREFIX_CHART[key] = np.array([float(mx), float(my), float(c)], dtype=np.float64)
    return _PREFIX_CHART[key]


def exact_ranges(world):
    ranges = []
    for stage in range(1, 9):
        rows = [_prefix_chart(prefix, stage) for prefix in world.train_prefixes[stage]]
        stacked = np.stack(rows, axis=0)
        lo = stacked.min(axis=0).astype(np.float32).astype(np.float64)
        hi = stacked.max(axis=0).astype(np.float32).astype(np.float64)
        ranges.append((lo, hi))
    return ranges


def quantized_exact_forecasts(ranges, bits: int):
    predictions = np.zeros((256, 3), dtype=np.float64)
    repairs = np.zeros(8, dtype=np.int64)
    clips = np.zeros(8, dtype=np.int64)
    for history in range(256):
        mx, my, c = 0.5, 0.5, 0.0
        for stage in range(8):
            bit = (history >> stage) & 1
            variable = "X" if stage % 2 == 0 else "Y"
            mx, my, c = _observe_f(mx, my, c, variable, bit)
            if stage < 7:
                mx, my, c = _transit_f(mx, my, c)
            reconstructed, outside, _constant = quantize_coordinates(
                np.array([mx, my, c]), ranges[stage][0], ranges[stage][1], bits
            )
            clips[stage] += int(np.sum(outside))
            mx, my, c, changed = _repair(float(reconstructed[0]), float(reconstructed[1]), float(reconstructed[2]))
            repairs[stage] += int(changed)
        qxor = mx + my - 2.0 * (mx * my + c)
        predictions[history] = (mx, my, qxor)
    return predictions, repairs.tolist(), clips.tolist()


def reference_arm_report(world) -> dict:
    """Unquantized K-EXACT, K-PROD*, K-CUR, plus the K-EXACT precision curve."""
    reports = {}
    for name, forecasts in world.reference_forecasts.items():
        errors = component_excess(forecasts, world)
        reports[name] = {
            "errors": errors,
            "afit_test": afit_holds(errors, world, "TEST"),
            "afit_train": afit_holds(errors, world, "TRAIN"),
            "init_equals_final": True,
        }
    ranges = exact_ranges(world)
    curve = []
    selected = None
    for bits in B_GRID:
        forecasts, repairs, clips = quantized_exact_forecasts(ranges, bits)
        valid = bool(np.isfinite(forecasts).all())
        errors = component_excess(forecasts, world) if valid else None
        passed = bool(valid and afit_holds(errors, world, "TRAIN"))
        curve.append(
            {
                "b": bits,
                "train_afit": passed,
                "errors": errors,
                "repairs": repairs,
                "clip_counts": clips,
            }
        )
        if passed and selected is None:
            selected = bits
    if selected is None:
        confirmation = "NOT CONFIRMED"
        b_sel = "no qualifying precision in the declared grid"
    else:
        chosen = next(row for row in curve if row["b"] == selected)
        confirmation = "CONFIRMED" if afit_holds(chosen["errors"], world, "TEST") else "NOT CONFIRMED"
        b_sel = selected
    reports["K-EXACT"]["precision"] = {
        "b_sel": b_sel,
        "confirmation": confirmation,
        "curve": curve,
        "metadata_bits": 64 * 3 * 8,
        "charged_state": "three quantization indices",
    }
    return reports
