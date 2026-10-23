"""Evaluation of one frozen GRU-8 seed. No training.

The gradient is computed and the transformed paths are hashed before any dose
curve. Phase A also cross-checks reversion curves against the committed PR #8
values. Existing checkpoint files are read and not rewritten.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import torch

from graded_reversion_draws import ZeroDrawError, block_norm_errors, rescale_draws
from graded_reversion_eval import (
    endpoint_gaps,
    load_verified_checkpoint,
    module_from_state,
    weight_hh_f64,
)
from graded_reversion_outcomes import (
    auc,
    divide_by_pd,
    nondecreasing_steps,
    outcome_bundle,
    pd_cd_components,
    saturation_index,
)
from graded_reversion_spec import (
    ALPHAS,
    CONTINUATION_STAGES,
    EPS0,
    IDENTITY_TOL,
    PRIMARY,
    TARGETS,
    target_rows,
)
from first_order_control_construct import construct_fo_paths
from first_order_control_criteria import (
    d_family,
    eligibility_target,
    family_margin_report,
    fo_auc_from_dot,
    joint_pass,
    m_flag,
    materiality_ratio,
)
from first_order_control_draws import fo_raw_draws, grad_raw_draws, iso_raw_draws, sha256_array
from first_order_control_gradient import (
    bit_tensor,
    compute_gradient,
    finite_difference_report,
    oracle_tensor,
)
from first_order_control_spec import (
    BLOCKS,
    CODE_VERSION,
    CROSS_CHECK_ABS,
    N_PATHS,
)
from recurrent_core_transfer_models import MatrixOverride
from recurrent_core_transfer_verdicts import transfer_pass
from twostream_acquisition_metrics import afit_holds, all_bits, continue_from, outputs_valid, rollout


def _json_number(value):
    number = float(value)
    if not np.isfinite(number):
        return None
    return number


def _state_word(flag):
    if flag is None:
        return "not_evaluated"
    return "pass" if flag else "fail"


def _bundle_record(bundle: dict, baseline: dict) -> dict:
    record = {key: _json_number(value) for key, value in bundle.items()}
    record["delta_L_prefix"] = _json_number(bundle["L_prefix"] - baseline["L_prefix"])
    record["delta_L_cont"] = _json_number(bundle["L_cont"] - baseline["L_cont"])
    record["delta_L_prefix_XOR"] = _json_number(bundle["L_prefix_XOR"] - baseline["L_prefix_XOR"])
    record["delta_E_TEST_total"] = _json_number(bundle["E_TEST_total"] - baseline["E_TEST_total"])
    record["delta_E_TEST_XOR"] = _json_number(bundle["E_TEST_XOR"] - baseline["E_TEST_XOR"])
    return record


def _continue(model, h4, block, rows) -> np.ndarray:
    model.override = MatrixOverride(CONTINUATION_STAGES, rows, block)
    try:
        return continue_from(model, h4, all_bits()[:, 4:], 4)
    finally:
        model.override = None


def _series(values):
    if any(value is None for value in values):
        return None
    return [float(value) for value in values]


def _missing_target(displacement_norm, collapsed: bool) -> dict:
    return {
        "curves_missing": True,
        "collapsed": bool(collapsed),
        "delta_norm": displacement_norm,
        "D_FO": None,
        "D_ISO": None,
        "D": None,
        "M": None,
        "joint": False,
        "fo": None,
        "iso": None,
        "auc_rev": None,
        "delta_rev": None,
        "doses": None,
    }


def _dose_curves(model, h4, intact_pred, intact_bundle, trained, delta, fo_paths, iso_paths, world):
    baseline_l = intact_bundle["L_prefix"]
    targets = {}
    invalid = []
    fo_t = torch.from_numpy(np.ascontiguousarray(fo_paths, dtype=np.float64))
    iso_t = torch.from_numpy(np.ascontiguousarray(iso_paths, dtype=np.float64))
    for target in TARGETS:
        rows = target_rows(target)
        outputs_ok = True
        sham_pred = _continue(model, h4, trained[rows[0]:rows[1], :].clone(), rows)
        sham_gap = float(np.max(np.abs(sham_pred - intact_pred)))
        if not (sham_gap <= EPS0):
            invalid.append(target + ":sham")
        doses = []
        alpha0_gap = None
        for alpha in ALPHAS:
            rev_block = (trained + float(alpha) * delta)[rows[0]:rows[1], :]
            rev_pred = _continue(model, h4, rev_block.contiguous(), rows)
            if alpha == 0.0:
                alpha0_gap = float(np.max(np.abs(rev_pred - intact_pred)))
            if not outputs_valid(rev_pred):
                outputs_ok = False
            rev_record = _bundle_record(outcome_bundle(rev_pred, world), intact_bundle)
            fo_records = []
            iso_records = []
            for index in range(N_PATHS):
                fo_block = (trained + float(alpha) * fo_t[index])[rows[0]:rows[1], :]
                iso_block = (trained + float(alpha) * iso_t[index])[rows[0]:rows[1], :]
                fo_pred = _continue(model, h4, fo_block.contiguous(), rows)
                iso_pred = _continue(model, h4, iso_block.contiguous(), rows)
                if not outputs_valid(fo_pred) or not outputs_valid(iso_pred):
                    outputs_ok = False
                fo_records.append(_bundle_record(outcome_bundle(fo_pred, world), intact_bundle))
                iso_records.append(_bundle_record(outcome_bundle(iso_pred, world), intact_bundle))
            doses.append(
                {
                    "alpha": float(alpha),
                    "rev": rev_record,
                    "fo": fo_records,
                    "iso": iso_records,
                }
            )
        restored, _states = rollout(model, all_bits())
        restore_gap = float(np.max(np.abs(restored - intact_pred)))
        if not (restore_gap <= IDENTITY_TOL):
            invalid.append(target + ":restore")
        if alpha0_gap is None or not (alpha0_gap <= EPS0):
            invalid.append(target + ":alpha0")
        if not outputs_ok:
            invalid.append(target + ":outputs")
        rev_deltas = _series([dose["rev"]["delta_L_prefix"] for dose in doses])
        fo_deltas = []
        iso_deltas = []
        finite = rev_deltas is not None
        for index in range(N_PATHS):
            fo_series = _series([dose["fo"][index]["delta_L_prefix"] for dose in doses])
            iso_series = _series([dose["iso"][index]["delta_L_prefix"] for dose in doses])
            if fo_series is None or iso_series is None:
                finite = False
            fo_deltas.append(fo_series)
            iso_deltas.append(iso_series)
        endpoint_pred = doses[-1]["rev"]
        targets[target] = {
            "curves_missing": not finite,
            "sham_gap": sham_gap,
            "restore_gap": restore_gap,
            "alpha0_gap": alpha0_gap,
            "sham_ok": bool(sham_gap <= EPS0),
            "restore_ok": bool(restore_gap <= IDENTITY_TOL),
            "alpha0_ok": bool(alpha0_gap is not None and alpha0_gap <= EPS0),
            "outputs_valid": outputs_ok,
            "delta_rev": rev_deltas,
            "delta_fo": fo_deltas,
            "delta_iso": iso_deltas,
            "forecast_change_max_abs": float(np.max(np.abs(
                _continue(model, h4, (trained + delta)[rows[0]:rows[1], :].contiguous(), rows) - intact_pred
            ))),
            "endpoint_L_prefix": endpoint_pred["L_prefix"],
            "endpoint_delta_L_prefix": endpoint_pred["delta_L_prefix"],
            "endpoint_L_cont": endpoint_pred["L_cont"],
            "endpoint_delta_L_cont": endpoint_pred["delta_L_cont"],
            "endpoint_L_prefix_XOR": endpoint_pred["L_prefix_XOR"],
            "endpoint_delta_L_prefix_XOR": endpoint_pred["delta_L_prefix_XOR"],
            "endpoint_E_TEST_total": endpoint_pred["E_TEST_total"],
            "endpoint_delta_E_TEST_total": endpoint_pred["delta_E_TEST_total"],
            "endpoint_E_TEST_XOR": endpoint_pred["E_TEST_XOR"],
            "endpoint_delta_E_TEST_XOR": endpoint_pred["delta_E_TEST_XOR"],
            "L_cont_auc": None if rev_deltas is None else auc([dose["rev"]["delta_L_cont"] for dose in doses]),
            "L_prefix_XOR_auc": None if rev_deltas is None else auc([dose["rev"]["delta_L_prefix_XOR"] for dose in doses]),
            "doses": doses,
            "finite_curve": finite,
        }
        if not finite:
            invalid.append(target + ":nonfinite curve")
    return targets, invalid


def _cross_check(targets, committed) -> dict:
    gaps = {}
    ok = True
    for target in TARGETS:
        got = targets[target]["delta_rev"]
        expected = committed[target]
        if got is None or len(got) != len(expected):
            gaps[target] = None
            ok = False
            continue
        worst = 0.0
        for left, right in zip(got, expected):
            worst = max(worst, abs(float(left) - float(right)))
        gaps[target] = worst
        if worst > CROSS_CHECK_ABS:
            ok = False
    return {"ok": ok, "max_abs": gaps}


def _summarize_target(target_name, target, valid, transfer, b_prefix, c_prefix, displacement, collapsed, g_dot_delta, iso_dots, pd_value):
    if target.get("curves_missing") or not target.get("finite_curve", False):
        eligible, reasons = eligibility_target(valid, transfer, b_prefix, c_prefix, displacement, collapsed)
        return {
            "collapsed": bool(collapsed),
            "delta_norm": displacement,
            "eligible": eligible,
            "eligibility_reasons": reasons,
            "D_FO": None,
            "D_ISO": None,
            "D": None,
            "M": None,
            "joint": False,
            "auc_rev": None,
            "fo": None,
            "iso": None,
            "conditions": {
                "valid": _state_word(valid),
                "eligible": _state_word(eligible),
                "D_FO": "not_evaluated",
                "D_ISO": "not_evaluated",
                "M": "not_evaluated",
                "joint": "fail",
            },
        }
    rev_deltas = target["delta_rev"]
    auc_rev = auc(rev_deltas)
    auc_fo = [auc(series) for series in target["delta_fo"]]
    auc_iso = [auc(series) for series in target["delta_iso"]]
    eligible, reasons = eligibility_target(valid, transfer, b_prefix, c_prefix, displacement, collapsed)
    # Directional flags are properties of the curves. Joint also needs validity
    # and eligibility, which are applied after these booleans exist.
    directional_fo = d_family(auc_rev, auc_fo)
    directional_iso = d_family(auc_rev, auc_iso)
    material = m_flag(auc_rev, b_prefix)
    passed = joint_pass(valid, eligible, directional_fo, directional_iso, material)
    fo_report = family_margin_report(auc_rev, auc_fo, rev_deltas, target["delta_fo"], b_prefix, pd_value, passed)
    iso_report = family_margin_report(auc_rev, auc_iso, rev_deltas, target["delta_iso"], b_prefix, pd_value, passed)
    tangent = fo_auc_from_dot(g_dot_delta)
    iso_tangents = [
        None if value is None else fo_auc_from_dot(float(value)) for value in iso_dots
    ]
    summary = {
        "collapsed": bool(collapsed),
        "delta_norm": displacement,
        "eligible": eligible,
        "eligibility_reasons": reasons,
        "D_FO": directional_fo,
        "D_ISO": directional_iso,
        "D": bool(directional_fo and directional_iso),
        "M": material,
        "joint": passed,
        "auc_rev": auc_rev,
        "M_over_B_quarter": materiality_ratio(auc_rev, b_prefix),
        "FO_AUC": tangent,
        "residual_rev": float(auc_rev - tangent),
        "residual_name": "residual after subtracting the initial tangent contribution",
        "residual_fo": [float(value - tangent) for value in auc_fo],
        "residual_iso": [
            None if tangent_j is None else float(value - tangent_j)
            for value, tangent_j in zip(auc_iso, iso_tangents)
        ],
        "fo": fo_report,
        "iso": iso_report,
        "saturation": saturation_index(rev_deltas[ALPHAS.index(0.5)], rev_deltas[ALPHAS.index(1.0)]),
        "nondecreasing_steps": nondecreasing_steps(rev_deltas),
        "delta_rev_one_eighth": rev_deltas[ALPHAS.index(0.125)],
        "tangent_one_eighth": float(g_dot_delta) / 8.0,
        "conditions": {
            "valid": _state_word(valid),
            "eligible": _state_word(eligible),
            "D_FO": _state_word(directional_fo),
            "D_ISO": _state_word(directional_iso),
            "M": _state_word(material),
            "joint": _state_word(passed),
        },
    }
    target.update(summary)
    return summary


def evaluate_seed(
    seed: int,
    world,
    checkpoint_dir: Path,
    expected_hashes: dict,
    manifest_seed: dict,
    committed_delta_rev: dict | None = None,
    phase: str = "A",
) -> dict:
    """Full evaluation. Dose curves run only after path hashes are in hand."""
    invalid_reasons = []
    engineering_flags = []
    names = {
        "f_trained": "s%d_f_trained.ckpt" % seed,
        "f_init": "s%d_f_init.ckpt" % seed,
        "cand_init": "s%d_cand_init.ckpt" % seed,
    }
    before = {key: hashlib.sha256((checkpoint_dir / filename).read_bytes()).hexdigest() for key, filename in names.items()}
    states = {}
    file_shas = {}
    for key, filename in names.items():
        state, ok, file_sha = load_verified_checkpoint(checkpoint_dir / filename, expected_hashes[key])
        states[key] = state
        file_shas[key] = file_sha
        if not ok:
            invalid_reasons.append("checkpoint:" + key)
            engineering_flags.append("checkpoint sha mismatch:" + key)
    trained = weight_hh_f64(states["f_trained"])
    init = weight_hh_f64(states["cand_init"])
    w0_match = bool(torch.equal(states["f_init"]["rnn.weight_hh_l0"], states["cand_init"]["rnn.weight_hh_l0"]))
    if not w0_match:
        invalid_reasons.append("W0 mismatch")
    delta = init - trained
    endpoint = endpoint_gaps(trained, init)
    if not endpoint["ok"]:
        invalid_reasons.append("endpoint")
        engineering_flags.append("endpoint path identity failed")

    model = module_from_state(states["f_trained"])
    if not torch.equal(model.rnn.weight_hh_l0, trained):
        raise RuntimeError("float64 W_T does not match the eval model")
    oracle = oracle_tensor(world.q)
    bits = bit_tensor()
    gradient = compute_gradient(model, oracle, bits, trained)
    if not gradient["finite"]:
        invalid_reasons.append("nonfinite gradient")
    if not gradient["byte_identical"]:
        invalid_reasons.append("gradient byte identity")
        engineering_flags.append("two gradient computations were not byte-identical")
    raw_grad = torch.from_numpy(np.ascontiguousarray(grad_raw_draws(seed), dtype=np.float64))
    grad_draw_sha = sha256_array(raw_grad.numpy())
    if grad_draw_sha != manifest_seed["grad_sha256"]:
        invalid_reasons.append("gradient-check draw sha")
        engineering_flags.append("gradient-check draw sha does not match the freeze manifest")
    fd_report = finite_difference_report(model, oracle, bits, trained, gradient["G"], delta, raw_grad)
    if not fd_report["ok"]:
        invalid_reasons.append("finite difference")

    fo_draws = fo_raw_draws(seed)
    fo_draw_sha = sha256_array(fo_draws)
    if fo_draw_sha != manifest_seed["fo_sha256"]:
        invalid_reasons.append("FO draw sha")
        engineering_flags.append("FO base-draw sha does not match the freeze manifest")
    iso_draws = iso_raw_draws(seed)
    iso_draw_sha = sha256_array(iso_draws)
    if iso_draw_sha != manifest_seed["iso_sha256"]:
        invalid_reasons.append("ISO draw sha")
        engineering_flags.append("ISO draw sha does not match the freeze manifest")

    construction = construct_fo_paths(delta, gradient["G"], fo_draws)
    fo_path_sha = None if construction["paths"] is None else sha256_array(construction["paths"])
    if not construction["ok"]:
        invalid_reasons.append("FO construction")
    try:
        scaled, block_info = rescale_draws(iso_draws, delta.numpy())
        iso_error = None
    except ZeroDrawError as exc:
        scaled = np.zeros_like(iso_draws)
        block_info = []
        iso_error = "zero random draw:" + str(exc)
        invalid_reasons.append(iso_error)
    norm_report = block_norm_errors(scaled, delta.numpy())
    if not norm_report["ok"]:
        invalid_reasons.append("ISO block norm")
        engineering_flags.append("ISO block-norm check failed")
    iso_path_sha = sha256_array(scaled)
    g_np = gradient["G"].detach().cpu().numpy()
    iso_dots = (np.ascontiguousarray(scaled, dtype=np.float64).reshape(N_PATHS, -1) @ g_np.reshape(-1)).tolist()
    g_dot_delta = float(torch.sum(gradient["G"] * delta))
    g_norm = float(gradient["norm"])
    delta_norm = float(torch.linalg.vector_norm(delta))
    if not np.isfinite(g_dot_delta) or g_norm == 0.0 or delta_norm == 0.0 or not np.isfinite(g_norm):
        cos = None
    else:
        cos = g_dot_delta / (g_norm * delta_norm)
    if not np.isfinite(g_dot_delta):
        g_dot_delta_out = None
        fo_auc_value = None
    else:
        g_dot_delta_out = g_dot_delta
        fo_auc_value = fo_auc_from_dot(g_dot_delta)
    iso_dots = [
        None if value is None or not np.isfinite(value) else float(value) for value in iso_dots
    ]

    # Transformed-path hashes exist before any dose curve is evaluated.
    path_hashes_ready = True
    pre_curve_block = any(
        reason.startswith("checkpoint:")
        or reason in {
            "W0 mismatch",
            "endpoint",
            "nonfinite gradient",
            "gradient byte identity",
            "gradient-check draw sha",
            "finite difference",
            "FO draw sha",
            "ISO draw sha",
            "FO construction",
            "ISO block norm",
        }
        or reason.startswith("zero random draw:")
        for reason in invalid_reasons
    )
    oracle_scale = pd_cd_components(world.q)
    intact_pred, states_roll = rollout(model, all_bits())
    h4 = states_roll[3]
    f_init = module_from_state(states["f_init"])
    f_init_pred = rollout(f_init, all_bits())[0]
    intact_valid = bool(outputs_valid(intact_pred))
    f_init_valid = bool(outputs_valid(f_init_pred))
    if not intact_valid:
        invalid_reasons.append("outputs intact")
    if not f_init_valid:
        invalid_reasons.append("outputs f_init")
    intact_bundle = outcome_bundle(intact_pred, world)
    f_init_bundle = outcome_bundle(f_init_pred, world)
    b_prefix = float(f_init_bundle["L_prefix"] - intact_bundle["L_prefix"])
    c_prefix = float(oracle_scale["PD"] - intact_bundle["L_prefix"])
    e_trained = float(intact_bundle["E_TEST_total"])
    e_init = float(f_init_bundle["E_TEST_total"])
    afit = bool(afit_holds(
        {
            "TEST": {"total": intact_bundle["E_TEST_total"], "XOR": intact_bundle["E_TEST_XOR"]},
            "TRAIN": {"total": intact_bundle["E_TRAIN_total"], "XOR": intact_bundle["E_TRAIN_XOR"]},
        },
        world,
        "TEST",
    ))
    # Validity is a separate eligibility item, matching the PR #8 reading.
    transfer = bool(transfer_pass(True, afit, e_trained, e_init))
    block_norms = {}
    for name in BLOCKS:
        rows = target_rows(name)
        block_norms[name] = float(torch.linalg.vector_norm(delta[rows[0]:rows[1], :]))

    curves_missing = True
    targets = {}
    if path_hashes_ready and not pre_curve_block:
        targets, curve_invalid = _dose_curves(
            model, h4, intact_pred, intact_bundle, trained, delta, construction["paths"], scaled, world
        )
        invalid_reasons.extend(curve_invalid)
        curves_missing = False
        if committed_delta_rev is not None:
            check = _cross_check(targets, committed_delta_rev)
            if not check["ok"]:
                invalid_reasons.append("REV cross-check")
                engineering_flags.append("REV delta_rev differs from the committed PR #8 curve by more than 1e-15")
        else:
            check = None
    else:
        check = None
        for target in TARGETS:
            norm = delta_norm if target == PRIMARY else block_norms[target]
            collapsed = False
            targets[target] = _missing_target(norm, collapsed)

    after = {key: hashlib.sha256((checkpoint_dir / filename).read_bytes()).hexdigest() for key, filename in names.items()}
    if before != after:
        invalid_reasons.append("checkpoint mutated")
        engineering_flags.append("evaluation rewrote a checkpoint file")

    valid_for_summary = len(invalid_reasons) == 0
    # Collapse is non-evaluability only when the paths were actually built.
    primary_collapsed = bool(construction["ok"] and construction["primary_collapsed"])
    block_collapsed = {
        name: bool(construction["ok"] and construction["blocks"][name]["collapsed"]) for name in BLOCKS
    }
    summaries = {}
    eligible = {}
    eligibility_reasons = {}
    joint = {}
    for target in TARGETS:
        collapsed = primary_collapsed if target == PRIMARY else block_collapsed[target]
        displacement = delta_norm if target == PRIMARY else block_norms[target]
        if curves_missing:
            targets[target]["collapsed"] = collapsed
            summary = _summarize_target(
                target, targets[target], valid_for_summary, transfer, b_prefix, c_prefix, displacement, collapsed,
                g_dot_delta_out if g_dot_delta_out is not None else 0.0, iso_dots, oracle_scale["PD"],
            )
        else:
            targets[target]["collapsed"] = collapsed
            targets[target]["delta_norm"] = displacement
            summary = _summarize_target(
                target, targets[target], valid_for_summary, transfer, b_prefix, c_prefix, displacement, collapsed,
                g_dot_delta_out if g_dot_delta_out is not None else 0.0, iso_dots, oracle_scale["PD"],
            )
        summaries[target] = summary
        eligible[target] = summary["eligible"]
        eligibility_reasons[target] = summary["eligibility_reasons"]
        joint[target] = summary["joint"]

    geometry = {
        "G_dot_delta": g_dot_delta_out,
        "cos_G_delta": cos,
        "G_norm": None if not np.isfinite(g_norm) else g_norm,
        "delta_norm": delta_norm,
        "FO_AUC": fo_auc_value,
        "blocks": construction["blocks"],
        "fixed_blocks": construction["fixed_blocks"] if construction["ok"] else construction["fixed_blocks"],
        "negligible_blocks": construction["negligible_blocks"],
        "R_eff": construction["R_eff"],
        "R_eff_over_delta": construction["R_eff_over_delta"],
        "primary_collapsed": primary_collapsed,
        "primary_near_collapse": construction["primary_near_collapse"],
        "construction_ok": construction["ok"],
        "construction_reasons": construction["reasons"],
        "assembled_norm_ok": construction["assembled_norm_ok"],
        "assembled_fo_ok": construction["assembled_fo_ok"],
        "g_preserved": construction["g_preserved"],
        "iso_dots": [None if value is None else float(value) for value in iso_dots],
        "fd": fd_report,
        "gradient_byte_identical": gradient["byte_identical"],
        "gradient_finite": gradient["finite"],
        "gradient_loss": gradient["loss"],
    }
    return {
        "seed": int(seed),
        "phase": phase,
        "code_version": CODE_VERSION,
        "curves_missing": curves_missing,
        "path_hash_before_curves": path_hashes_ready,
        "engineering_flags": engineering_flags,
        "valid": valid_for_summary,
        "invalid_reasons": invalid_reasons,
        "checkpoint_sha256": {key: expected_hashes[key] for key in expected_hashes},
        "checkpoint_file_sha256": file_shas,
        "checkpoint_unchanged": before == after,
        "w0_matches_f_init_hh": w0_match,
        "endpoint": endpoint,
        "hashes": {
            "checkpoint": {key: expected_hashes[key] for key in expected_hashes},
            "gradient": gradient["sha256"],
            "fo_base_draw": fo_draw_sha,
            "iso_draw": iso_draw_sha,
            "grad_check_draw": grad_draw_sha,
            "fo_transformed": fo_path_sha,
            "iso_transformed": iso_path_sha,
        },
        "draw_sha_matches_manifest": (
            fo_draw_sha == manifest_seed["fo_sha256"] and iso_draw_sha == manifest_seed["iso_sha256"]
        ),
        "block_rescale": {"info": block_info, "norms": norm_report},
        "delta_norm": delta_norm,
        "block_norms": block_norms,
        "G": g_np.tolist(),
        "geometry": geometry,
        "rev_cross_check": check,
        "PD_q_star": oracle_scale["PD"],
        "PD_q_star_X": oracle_scale["PD_X"],
        "PD_q_star_Y": oracle_scale["PD_Y"],
        "PD_q_star_XOR": oracle_scale["PD_XOR"],
        "CD_q_star": oracle_scale["CD"],
        "L_prefix_f_trained": intact_bundle["L_prefix"],
        "L_prefix_f_init": f_init_bundle["L_prefix"],
        "L_prefix_f_trained_over_PD": divide_by_pd(intact_bundle["L_prefix"], oracle_scale["PD"]),
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
        "intact_outcomes": {key: _json_number(value) for key, value in intact_bundle.items()},
        "f_init_outcomes": {key: _json_number(value) for key, value in f_init_bundle.items()},
        "eligible": eligible,
        "eligibility_reasons": eligibility_reasons,
        "joint": joint,
        "primary_collapsed": primary_collapsed,
        "block_collapsed": block_collapsed,
        "summary": summaries,
        "targets": targets,
    }
