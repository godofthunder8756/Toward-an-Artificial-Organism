"""Evaluation of one frozen GRU-8 seed. No training.

Phase A calls this on the saved PR #7 checkpoints. Phase B calls the same
function on checkpoints it has just trained. The dose grid, the 32 directions,
and the loss are the frozen protocol's.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import torch

from graded_reversion_draws import (
    ZeroDrawError,
    block_norm_errors,
    raw_draws,
    rescale_draws,
)
from graded_reversion_outcomes import (
    auc,
    d_passes,
    divide_by_pd,
    eligibility,
    joint_pass,
    m_passes,
    nondecreasing_steps,
    outcome_bundle,
    pd_cd_components,
    random_median,
    rev_rank,
    saturation_index,
)
from graded_reversion_spec import (
    ALPHAS,
    CODE_VERSION,
    CONTINUATION_STAGES,
    EPS0,
    IDENTITY_TOL,
    N_RANDOM,
    PRIMARY,
    PRIMARY_ROWS,
    TARGETS,
    target_rows,
)
from recurrent_core_transfer_models import (
    CoreGRU,
    MatrixOverride,
    checkpoint_sha256,
    eval_copy,
    load_checkpoint,
    load_snapshot,
)
from recurrent_core_transfer_verdicts import transfer_pass
from twostream_acquisition_metrics import afit_holds, all_bits, outputs_valid, rollout


def _finite(value) -> bool:
    try:
        return bool(math.isfinite(float(value)))
    except (TypeError, ValueError):
        return False


def load_verified_checkpoint(path: Path, expected_sha256: str) -> tuple[dict, bool, str]:
    raw = path.read_bytes()
    file_sha = hashlib.sha256(raw).hexdigest()
    state = load_checkpoint(path)
    canon = checkpoint_sha256(state)
    ok = bool(file_sha == expected_sha256 and canon == expected_sha256)
    return state, ok, file_sha


def module_from_state(state: dict) -> CoreGRU:
    model = CoreGRU(32)
    load_snapshot(model, state)
    copied = eval_copy(model)
    return copied


def weight_hh_f64(state: dict) -> torch.Tensor:
    return state["rnn.weight_hh_l0"].detach().to(dtype=torch.float64).contiguous()


def path_matrix(trained: torch.Tensor, displacement: torch.Tensor, alpha: float) -> torch.Tensor:
    """W(alpha) = W_T + alpha * (W_source - W_T), in float64."""
    return trained + float(alpha) * displacement


def endpoint_gaps(trained: torch.Tensor, init: torch.Tensor) -> dict:
    displacement = init - trained
    at_zero = path_matrix(trained, displacement, 0.0)
    at_one = path_matrix(trained, displacement, 1.0)
    zero_exact = bool(torch.equal(at_zero, trained))
    one_gap = float(torch.max(torch.abs(at_one - init)))
    return {
        "w0_exact": zero_exact,
        "w1_max_abs": one_gap,
        "w1_ok": bool(one_gap <= EPS0),
        "ok": bool(zero_exact and one_gap <= EPS0),
    }


def _rollout_block(model, block: torch.Tensor, rows: tuple[int, int]) -> np.ndarray:
    saved_w = model.rnn.weight_hh_l0.detach().clone()
    saved_b = model.rnn.bias_hh_l0.detach().clone()
    model.override = MatrixOverride(CONTINUATION_STAGES, rows, block)
    try:
        predictions, _states = rollout(model, all_bits())
    finally:
        model.override = None
    if not torch.equal(model.rnn.weight_hh_l0, saved_w) or not torch.equal(model.rnn.bias_hh_l0, saved_b):
        raise RuntimeError("MatrixOverride did not restore hidden-to-hidden weights")
    return predictions


def _rollout_intact(model) -> np.ndarray:
    model.override = None
    predictions, _states = rollout(model, all_bits())
    return predictions


def probe_sham_restore(model) -> dict:
    """SHAM substitutes W_T. RESTORE reruns with the override removed."""
    trained = model.rnn.weight_hh_l0.detach().clone()
    intact = _rollout_intact(model)
    sham = _rollout_block(model, trained.clone(), PRIMARY_ROWS)
    _rollout_block(model, torch.zeros_like(trained), PRIMARY_ROWS)
    restored = _rollout_intact(model)
    sham_gap = float(np.max(np.abs(sham - intact)))
    restore_gap = float(np.max(np.abs(restored - intact)))
    return {
        "sham_gap": sham_gap,
        "restore_gap": restore_gap,
        "sham_ok": bool(sham_gap <= EPS0),
        "restore_ok": bool(restore_gap <= IDENTITY_TOL),
        "ok": bool(sham_gap <= EPS0 and restore_gap <= IDENTITY_TOL),
    }


def _json_number(value):
    number = float(value)
    if not math.isfinite(number):
        return None
    return number


def _bundle_json(bundle: dict) -> dict:
    return {key: _json_number(value) for key, value in bundle.items()}


def _dose_record(bundle: dict, baseline_l_prefix: float) -> dict:
    record = _bundle_json(bundle)
    l_prefix = bundle["L_prefix"]
    record["delta_L_prefix"] = _json_number(l_prefix - baseline_l_prefix)
    record["delta_L_cont"] = None
    record["delta_L_prefix_XOR"] = None
    record["delta_E_TEST_total"] = None
    record["delta_E_TEST_XOR"] = None
    return record


def _attach_deltas(record: dict, baseline: dict) -> None:
    record["delta_L_cont"] = _json_number(record["L_cont"] - baseline["L_cont"])
    record["delta_L_prefix_XOR"] = _json_number(record["L_prefix_XOR"] - baseline["L_prefix_XOR"])
    record["delta_E_TEST_total"] = _json_number(record["E_TEST_total"] - baseline["E_TEST_total"])
    record["delta_E_TEST_XOR"] = _json_number(record["E_TEST_XOR"] - baseline["E_TEST_XOR"])


def pr7_expected_hashes(root: Path, seed: int) -> dict:
    payload = json.loads((root / "recurrent_core_results_v1" / "seeds" / ("s%d.json" % seed)).read_text(encoding="utf-8"))
    return {
        "f_trained": payload["f_trained"]["checkpoint_sha256"],
        "f_init": payload["f_init"]["checkpoint_sha256"],
        "cand_init": payload["cand"]["init_checkpoint_sha256"],
    }


def evaluate_seed(
    seed: int,
    world,
    checkpoint_dir: Path,
    expected_hashes: dict,
    draw_sha_expected: str | None = None,
) -> dict:
    """Full §4–§6 evaluation for one seed. Does not train."""
    invalid_reasons = []
    names = {
        "f_trained": "s%d_f_trained.ckpt" % seed,
        "f_init": "s%d_f_init.ckpt" % seed,
        "cand_init": "s%d_cand_init.ckpt" % seed,
    }
    states = {}
    file_shas = {}
    for key, filename in names.items():
        state, ok, file_sha = load_verified_checkpoint(checkpoint_dir / filename, expected_hashes[key])
        states[key] = state
        file_shas[key] = file_sha
        if not ok:
            invalid_reasons.append("checkpoint:" + key)

    trained_hh = weight_hh_f64(states["f_trained"])
    init_hh = weight_hh_f64(states["cand_init"])
    f_init_hh = weight_hh_f64(states["f_init"])
    w0_match = bool(torch.equal(states["f_init"]["rnn.weight_hh_l0"], states["cand_init"]["rnn.weight_hh_l0"]))
    if not w0_match:
        invalid_reasons.append("W0 mismatch")

    delta = init_hh - trained_hh
    endpoint = endpoint_gaps(trained_hh, init_hh)
    if not endpoint["ok"]:
        invalid_reasons.append("endpoint")

    try:
        draws = raw_draws(seed)
        draw_sha = hashlib.sha256(draws.tobytes()).hexdigest()
    except Exception as exc:
        raise RuntimeError("draw sequence failed for seed %d" % seed) from exc
    if draw_sha_expected is not None and draw_sha != draw_sha_expected:
        invalid_reasons.append("draw sha")

    try:
        scaled, block_info = rescale_draws(draws, delta.numpy())
    except ZeroDrawError as exc:
        invalid_reasons.append("zero random draw:" + str(exc))
        scaled = np.zeros_like(draws)
        block_info = []
    norm_report = block_norm_errors(scaled, delta.numpy())
    if not norm_report["ok"]:
        invalid_reasons.append("block norm")

    oracle_scale = pd_cd_components(world.q)
    if oracle_scale["PD"] <= EPS0:
        raise RuntimeError("PD(q_star) is not positive")

    f_trained = module_from_state(states["f_trained"])
    f_init = module_from_state(states["f_init"])
    if not torch.equal(f_trained.rnn.weight_hh_l0, trained_hh):
        raise RuntimeError("float64 promotion of W_T does not match the eval model")

    intact_pred = _rollout_intact(f_trained)
    f_init_pred = _rollout_intact(f_init)
    intact_valid = bool(outputs_valid(intact_pred))
    f_init_valid = bool(outputs_valid(f_init_pred))
    if not intact_valid:
        invalid_reasons.append("outputs intact")
    if not f_init_valid:
        invalid_reasons.append("outputs f_init")

    intact_bundle = outcome_bundle(intact_pred, world)
    f_init_bundle = outcome_bundle(f_init_pred, world)
    baseline_l = intact_bundle["L_prefix"]
    b_prefix = float(f_init_bundle["L_prefix"] - baseline_l)
    c_prefix = float(oracle_scale["PD"] - baseline_l)
    e_trained = float(intact_bundle["E_TEST_total"])
    e_init = float(f_init_bundle["E_TEST_total"])
    afit = bool(afit_holds(
        {"TEST": {"total": intact_bundle["E_TEST_total"], "XOR": intact_bundle["E_TEST_XOR"], "X": intact_bundle["E_TEST_X"], "Y": intact_bundle["E_TEST_Y"]},
         "TRAIN": {"total": intact_bundle["E_TRAIN_total"], "XOR": intact_bundle["E_TRAIN_XOR"], "X": intact_bundle["E_TRAIN_X"], "Y": intact_bundle["E_TRAIN_Y"]}},
        world,
        "TEST",
    ))
    # Validity is a separate eligibility item. The helper's validity argument
    # is therefore true here; see the deviations log.
    transfer = bool(transfer_pass(True, afit, e_trained, e_init))

    block_norms = {}
    for name, rows in (("r", (0, 8)), ("z", (8, 16)), ("n", (16, 24))):
        block_norms[name] = float(torch.linalg.vector_norm(delta[rows[0]:rows[1], :]))
    full_norm = float(torch.linalg.vector_norm(delta))

    targets = {}
    for target in TARGETS:
        rows = target_rows(target)
        displacement_norm = full_norm if target == PRIMARY else block_norms[target]
        target_reasons = []
        sham_pred = _rollout_block(f_trained, trained_hh[rows[0]:rows[1], :].clone(), rows)
        sham_gap = float(np.max(np.abs(sham_pred - intact_pred)))
        if not (sham_gap <= EPS0):
            target_reasons.append("sham")
        doses = []
        outputs_ok = True
        alpha0_gap = None
        for alpha in ALPHAS:
            rev_block = path_matrix(trained_hh, delta, alpha)[rows[0]:rows[1], :]
            rev_pred = _rollout_block(f_trained, rev_block, rows)
            if alpha == 0.0:
                alpha0_gap = float(np.max(np.abs(rev_pred - intact_pred)))
            rev_bundle = outcome_bundle(rev_pred, world)
            rev_record = _dose_record(rev_bundle, baseline_l)
            _attach_deltas(rev_record, intact_bundle)
            if not outputs_valid(rev_pred):
                outputs_ok = False
            random_records = []
            random_deltas = []
            for index in range(N_RANDOM):
                eps = torch.from_numpy(np.ascontiguousarray(scaled[index], dtype=np.float64))
                random_block = path_matrix(trained_hh, eps, alpha)[rows[0]:rows[1], :]
                random_pred = _rollout_block(f_trained, random_block, rows)
                random_bundle = outcome_bundle(random_pred, world)
                random_record = _dose_record(random_bundle, baseline_l)
                _attach_deltas(random_record, intact_bundle)
                random_records.append(random_record)
                random_deltas.append(random_record["delta_L_prefix"])
                if not outputs_valid(random_pred):
                    outputs_ok = False
            rev_delta = rev_record["delta_L_prefix"]
            rank = None
            if rev_delta is not None and all(value is not None for value in random_deltas):
                rank = rev_rank(rev_delta, random_deltas)
            doses.append(
                {
                    "alpha": alpha,
                    "rev": rev_record,
                    "random": random_records,
                    "rev_rank": rank,
                    "random_delta_L_prefix": random_deltas,
                }
            )
        restored = _rollout_intact(f_trained)
        restore_gap = float(np.max(np.abs(restored - intact_pred)))
        if not (restore_gap <= IDENTITY_TOL):
            target_reasons.append("restore")
        if alpha0_gap is None or not (alpha0_gap <= EPS0):
            target_reasons.append("alpha0")
        if not outputs_ok:
            target_reasons.append("outputs")
        if target_reasons:
            invalid_reasons.append(target + ":" + ",".join(target_reasons))

        rev_deltas = [dose["rev"]["delta_L_prefix"] for dose in doses]
        cont_deltas = [dose["rev"]["delta_L_cont"] for dose in doses]
        xor_deltas = [dose["rev"]["delta_L_prefix_XOR"] for dose in doses]
        finite_curve = all(value is not None for value in rev_deltas)
        random_aucs = []
        if finite_curve:
            for index in range(N_RANDOM):
                series = [dose["random"][index]["delta_L_prefix"] for dose in doses]
                if any(value is None for value in series):
                    random_aucs = []
                    finite_curve = False
                    break
                random_aucs.append(auc(series))
        if finite_curve:
            auc_rev = auc(rev_deltas)
            auc_cont = auc(cont_deltas) if all(value is not None for value in cont_deltas) else None
            auc_xor = auc(xor_deltas) if all(value is not None for value in xor_deltas) else None
            directional = d_passes(auc_rev, random_aucs)
            material = m_passes(auc_rev, b_prefix)
            margin = auc_rev - max(random_aucs)
            sat = saturation_index(rev_deltas[ALPHAS.index(0.5)], rev_deltas[ALPHAS.index(1.0)])
            steps = nondecreasing_steps(rev_deltas)
            median = random_median(random_aucs)
            maximum = max(random_aucs)
        else:
            auc_rev = None
            auc_cont = None
            auc_xor = None
            directional = False
            material = False
            margin = None
            sat = None
            steps = None
            median = None
            maximum = None
            invalid_reasons.append(target + ":nonfinite curve")

        targets[target] = {
            "delta_norm": displacement_norm,
            "sham_gap": sham_gap,
            "restore_gap": restore_gap,
            "alpha0_gap": alpha0_gap,
            "sham_ok": bool(sham_gap <= EPS0),
            "restore_ok": bool(restore_gap <= IDENTITY_TOL),
            "alpha0_ok": bool(alpha0_gap is not None and alpha0_gap <= EPS0),
            "outputs_valid": outputs_ok,
            "auc_rev": auc_rev,
            "auc_random": random_aucs,
            "auc_random_max": maximum,
            "auc_random_median": median,
            "D": directional,
            "D_margin": margin,
            "M": material,
            "saturation": sat,
            "nondecreasing_steps": steps,
            "delta_rev": rev_deltas,
            "L_cont_auc": auc_cont,
            "L_prefix_XOR_auc": auc_xor,
            "endpoint_L_prefix": doses[-1]["rev"]["L_prefix"],
            "endpoint_delta_L_prefix": doses[-1]["rev"]["delta_L_prefix"],
            "endpoint_E_TEST_total": doses[-1]["rev"]["E_TEST_total"],
            "endpoint_E_TEST_X": doses[-1]["rev"]["E_TEST_X"],
            "endpoint_E_TEST_Y": doses[-1]["rev"]["E_TEST_Y"],
            "endpoint_E_TEST_XOR": doses[-1]["rev"]["E_TEST_XOR"],
            "endpoint_delta_E_TEST_total": doses[-1]["rev"]["delta_E_TEST_total"],
            "endpoint_delta_E_TEST_XOR": doses[-1]["rev"]["delta_E_TEST_XOR"],
            "endpoint_L_cont": doses[-1]["rev"]["L_cont"],
            "endpoint_delta_L_cont": doses[-1]["rev"]["delta_L_cont"],
            "forecast_change_max_abs": None,
            "doses": doses,
        }

    # Forecast change at alpha = 1 is |predictions difference|, recomputed from
    # the stored endpoint excess only as a descriptive scalar of L and E.
    # The max-abs forecast gap is measured directly below from a dedicated pair
    # already consumed; recompute from the alpha=1 REV block for the primary.
    primary_rows = target_rows(PRIMARY)
    endpoint_block = path_matrix(trained_hh, delta, 1.0)
    endpoint_pred = _rollout_block(f_trained, endpoint_block, primary_rows)
    forecast_change = float(np.max(np.abs(endpoint_pred - intact_pred)))
    targets[PRIMARY]["forecast_change_max_abs"] = forecast_change
    for target in TARGETS:
        if target == PRIMARY:
            continue
        rows = target_rows(target)
        block = path_matrix(trained_hh, delta, 1.0)[rows[0]:rows[1], :]
        pred = _rollout_block(f_trained, block, rows)
        targets[target]["forecast_change_max_abs"] = float(np.max(np.abs(pred - intact_pred)))

    engineering_flags = []
    if not endpoint["w0_exact"]:
        engineering_flags.append("W(0) is not exactly W_T")
    if draw_sha_expected is not None and draw_sha != draw_sha_expected:
        engineering_flags.append("draw sha256 does not match the freeze manifest")

    valid = len(invalid_reasons) == 0
    eligible = {}
    eligibility_reasons = {}
    joint = {}
    for target in TARGETS:
        norm = full_norm if target == PRIMARY else block_norms[target]
        flag, reasons = eligibility(valid, transfer, b_prefix, c_prefix, norm)
        eligible[target] = flag
        eligibility_reasons[target] = reasons
        joint[target] = joint_pass(valid, flag, targets[target]["D"], targets[target]["M"])

    return {
        "seed": int(seed),
        "code_version": CODE_VERSION,
        "curves_missing": False,
        "engineering_flags": engineering_flags,
        "valid": valid,
        "invalid_reasons": invalid_reasons,
        "checkpoint_ok": not any(reason.startswith("checkpoint:") for reason in invalid_reasons),
        "checkpoint_sha256": {key: expected_hashes[key] for key in expected_hashes},
        "checkpoint_file_sha256": file_shas,
        "w0_matches_f_init_hh": w0_match,
        "endpoint": endpoint,
        "draw_sha256": draw_sha,
        "draw_sha_matches_manifest": draw_sha_expected is None or draw_sha == draw_sha_expected,
        "block_rescale": {"info": block_info, "norms": norm_report},
        "delta_norm": full_norm,
        "block_norms": block_norms,
        "PD_q_star": oracle_scale["PD"],
        "PD_q_star_X": oracle_scale["PD_X"],
        "PD_q_star_Y": oracle_scale["PD_Y"],
        "PD_q_star_XOR": oracle_scale["PD_XOR"],
        "CD_q_star": oracle_scale["CD"],
        "L_prefix_f_trained": baseline_l,
        "L_prefix_f_init": f_init_bundle["L_prefix"],
        "L_prefix_f_trained_over_PD": divide_by_pd(baseline_l, oracle_scale["PD"]),
        "B_prefix": b_prefix,
        "C_prefix": c_prefix,
        "B_prefix_over_PD": divide_by_pd(b_prefix, oracle_scale["PD"]),
        "C_prefix_over_PD": divide_by_pd(c_prefix, oracle_scale["PD"]),
        "E_TEST_f_trained": e_trained,
        "E_TEST_f_init": e_init,
        "E_TEST_XOR_f_trained": intact_bundle["E_TEST_XOR"],
        "E_TEST_XOR_f_init": f_init_bundle["E_TEST_XOR"],
        "afit_f_trained": afit,
        "transfer_pass": transfer,
        "outputs_valid_intact": intact_valid,
        "outputs_valid_f_init": f_init_valid,
        "intact_outcomes": _bundle_json(intact_bundle),
        "f_init_outcomes": _bundle_json(f_init_bundle),
        "forecast_change_max_abs_primary": forecast_change,
        "eligible": eligible,
        "eligibility_reasons": eligibility_reasons,
        "joint": joint,
        "targets": targets,
    }

