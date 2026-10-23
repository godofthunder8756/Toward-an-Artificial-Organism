"""Run the frozen recurrent-core transfer study and write its results.

The freeze manifest must already exist. TEST is read only inside this run.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import torch

from recurrent_core_transfer_e3 import decoder_label, decoder_report, pack_ratio
from recurrent_core_transfer_metrics import (
    evaluate_arm,
    hidden_reversion,
    original_readout_excess,
    pdcd_ratio,
    predict_histories,
    probability_excess,
    val_histories,
    variation_stats,
)
from recurrent_core_transfer_models import (
    CoreGRU,
    build_initialized,
    checkpoint_sha256,
    copy_recurrent,
    gate_block,
    load_checkpoint,
    load_snapshot,
    save_checkpoint,
    snapshot_state,
    tune_recurrent,
)
from recurrent_core_transfer_p2 import run_p2
from recurrent_core_transfer_spec import (
    CODE_FILES,
    GATE_ROWS,
    GATES,
    GRID_B,
    GRID_G,
    PROTOCOL_FILENAME,
    PROTOCOL_SHA256,
    READOUT_32,
    READOUT_70,
    SEEDS,
    STEPS,
    foreign_seed,
    is_grid_edge,
    select_configuration,
)
from recurrent_core_transfer_train import train_arm
from recurrent_core_transfer_verdicts import (
    assemble_claim,
    label_advantage,
    label_e1,
    label_rival_afit,
    label_specific,
    label_transfer,
    label_variation,
    ratio_at_most_half,
    ratio_value,
    specific_joint,
    transfer_pass,
    variation_joint,
)
from twostream_acquisition_metrics import _stage4, afit_holds
from twostream_acquisition_oracle import World

ROOT = Path(__file__).resolve().parent
FREEZE_PATH = ROOT / "RECURRENT_CORE_TRANSFER_FREEZE_v1.json"
RESULTS_DIR = ROOT / "recurrent_core_results_v1"


def configure_runtime() -> None:
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_freeze() -> None:
    protocol = sha256_file(ROOT / PROTOCOL_FILENAME)
    if protocol != PROTOCOL_SHA256:
        raise SystemExit("protocol hash does not match the reviewed file")
    code = {name: sha256_file(ROOT / name) for name in CODE_FILES}
    document = {
        "study": "recurrent-core transfer with hidden-to-hidden matrix reversion",
        "status": "FREEZE. No training run and no result file is part of this freeze.",
        "protocol_file": PROTOCOL_FILENAME,
        "protocol_sha256": protocol,
        "code_sha256": code,
        "seeds": list(SEEDS),
        "budget_steps": STEPS,
        "parameter_counts": {"recurrent": 456, "readout_32": 387, "readout_70": 843, "cand_total": 843},
        "approval": "Aidan Ahern approved the neural training for this study on 2026-10-20.",
        "base_branch": "cursor/twostream-acquisition-study-0e12",
    }
    FREEZE_PATH.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print("wrote %s" % FREEZE_PATH.name, flush=True)


def _require_freeze() -> dict:
    if not FREEZE_PATH.exists():
        raise SystemExit("freeze file is missing; refuse to train")
    manifest = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if manifest.get("protocol_sha256") != PROTOCOL_SHA256:
        raise SystemExit("freeze protocol hash does not match")
    for name, digest in manifest["code_sha256"].items():
        actual = sha256_file(ROOT / name)
        if actual != digest:
            raise SystemExit("code changed after freeze: %s" % name)
    return manifest


def _store(directory: Path, name: str, state: dict) -> tuple[str, bool]:
    path = directory / name
    digest = save_checkpoint(path, state)
    loaded = load_checkpoint(path)
    ok = checkpoint_sha256(loaded) == digest
    if ok:
        for key, value in state.items():
            if not torch.equal(value.detach().cpu(), loaded[key]):
                ok = False
                break
    return digest, ok


def _afit(evaluation, world, split: str) -> bool:
    if evaluation is None:
        return False
    return bool(afit_holds(evaluation["errors"], world, split))


def _total(evaluation, split: str):
    if evaluation is None:
        return None
    return float(evaluation["errors"][split]["total"])


def _safe_ratio(numerator, denominator):
    if numerator is None or denominator is None:
        return None
    if not math.isfinite(numerator) or not math.isfinite(denominator):
        return "UNDEFINED"
    return pack_ratio(ratio_value(numerator, denominator))


def _curve_value(value):
    if isinstance(value, float) and not math.isfinite(value):
        return "+inf" if value > 0 else "-inf"
    return value


def _arm_integrity(train_info, evaluation, checkpoint_ok: bool, init_outputs_valid: bool = True) -> bool:
    if not train_info["integrity_training"] or not checkpoint_ok or not init_outputs_valid:
        return False
    if evaluation is None:
        return False
    return bool(evaluation["outputs_valid"] and evaluation["identity"]["ok"])


def _pack_arm(train_info, evaluation, digest: str, checkpoint_ok: bool, integrity: bool, world) -> dict:
    identity = None if evaluation is None else to_jsonable(evaluation["identity"])
    return {
        "training": train_info,
        "errors": None if evaluation is None else evaluation["errors"],
        "afit_test": _afit(evaluation, world, "TEST"),
        "afit_train": _afit(evaluation, world, "TRAIN"),
        "outputs_valid": None if evaluation is None else bool(evaluation["outputs_valid"]),
        "identity": identity,
        "checkpoint_sha256": digest,
        "checkpoint_ok": checkpoint_ok,
        "integrity": integrity,
    }


def _train_frozen(seed, readout_seed, width, recurrent, world, steps, reject_val):
    model = build_initialized(readout_seed, width)
    copy_recurrent(model, recurrent)
    info = train_arm(model, seed, True, reject_val, steps=steps)
    evaluation = evaluate_arm(model, world) if info["integrity_training"] else None
    return model, info, evaluation


def _pack_delta_list(deltas) -> list:
    packed = []
    for item in deltas:
        packed.append({split: dict(item[split]) for split in ("TEST", "TRAIN")})
    return packed


def _pack_variation_pair(numerator: float, denominator: float):
    return pack_ratio(pdcd_ratio(numerator, denominator))


def run_seed(seed: int, world, inits: dict, directory: Path, steps: int = STEPS) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    w0 = inits[seed]
    init_digest, init_ok = _store(directory, "s%d_cand_init.ckpt" % seed, w0)
    cand = CoreGRU(READOUT_32)
    load_snapshot(cand, w0)
    init_eval = evaluate_arm(cand, world)
    cand_info = train_arm(cand, seed, False, False, steps=steps)
    cand_state = snapshot_state(cand)
    cand_digest, cand_ckpt_ok = _store(directory, "s%d_cand_final.ckpt" % seed, cand_state)
    cand_eval = evaluate_arm(cand, world) if cand_info["integrity_training"] else None
    cand_integrity = _arm_integrity(
        cand_info,
        cand_eval,
        cand_ckpt_ok and init_ok,
        bool(init_eval["outputs_valid"]),
    )
    cand_record = _pack_arm(cand_info, cand_eval, cand_digest, cand_ckpt_ok and init_ok, cand_integrity, world)
    cand_record["init_errors"] = init_eval["errors"]
    cand_record["init_afit_test"] = _afit(init_eval, world, "TEST")
    cand_record["init_outputs_valid"] = bool(init_eval["outputs_valid"])
    cand_record["init_checkpoint_sha256"] = init_digest
    cand_record["alearn"] = not cand_record["init_afit_test"]
    print("seed %d CAND integrity=%s E_test=%s" % (seed, cand_integrity, _total(cand_eval, "TEST")), flush=True)

    def frozen_arm(name, readout_seed, width, recurrent, reject_val):
        _model, info, evaluation = _train_frozen(seed, readout_seed, width, recurrent, world, steps, reject_val)
        digest, ckpt_ok = _store(directory, "s%d_%s.ckpt" % (seed, name), snapshot_state(_model))
        integrity = _arm_integrity(info, evaluation, ckpt_ok)
        print("seed %d %s integrity=%s E_test=%s" % (seed, name, integrity, _total(evaluation, "TEST")), flush=True)
        return _pack_arm(info, evaluation, digest, ckpt_ok, integrity, world), evaluation

    ft_record, ft_eval = (None, None)
    if cand_info["integrity_training"]:
        ft_record, ft_eval = frozen_arm("f_trained", 5000 + seed, READOUT_32, cand_state, False)
    fi_record, fi_eval = frozen_arm("f_init", 5000 + seed, READOUT_32, w0, False)

    histories = val_histories()
    grid = []
    for g in GRID_G:
        for b in GRID_B:
            model = build_initialized(6000 + seed, READOUT_70)
            copy_recurrent(model, tune_recurrent(w0, g, b))
            info = train_arm(model, seed, True, True, steps=steps)
            if info["integrity_training"]:
                preds = predict_histories(model, histories)
                criterion = probability_excess(preds, histories, world)["total"]
            else:
                criterion = float("inf")
            digest, ckpt_ok = _store(directory, "s%d_sel_g%s_b%s.ckpt" % (seed, g, b), snapshot_state(model))
            grid.append(
                {
                    "g": g,
                    "b": b,
                    "criterion": criterion,
                    "training_ok": bool(info["integrity_training"]),
                    "checkpoint_sha256": digest,
                    "checkpoint_ok": ckpt_ok,
                }
            )
            print(
                "seed %d sel g=%s b=%s criterion=%s"
                % (seed, g, b, "inf" if not np.isfinite(criterion) else "%.6g" % criterion),
                flush=True,
            )
    selection_ok = any(np.isfinite(row["criterion"]) for row in grid)
    chosen = None
    tie = False
    if selection_ok:
        chosen, tie = select_configuration(grid)
    rt_record, rt_eval = (None, None)
    fu_record, fu_eval = (None, None)
    if chosen is not None:
        tuned = tune_recurrent(w0, chosen["g"], chosen["b"])
        rt_record, rt_eval = frozen_arm("r_tuned843", 6000 + seed, READOUT_70, tuned, False)
        fu_record, fu_eval = frozen_arm("f_tuned32", 5000 + seed, READOUT_32, tuned, False)

    section3_valid = bool(
        cand_integrity
        and ft_record is not None
        and ft_record["integrity"]
        and fi_record["integrity"]
    )
    e_ft = _total(ft_eval, "TEST")
    e_fi = _total(fi_eval, "TEST")
    e_cand = _total(cand_eval, "TEST")
    passed_transfer = bool(
        section3_valid and e_ft is not None and e_fi is not None and transfer_pass(True, ft_record["afit_test"], e_ft, e_fi)
    )
    benefit = None if e_ft is None or e_fi is None else float(e_fi - e_ft)

    reversion = None
    section5_valid = False
    if ft_eval is not None and fi_eval is not None:
        foreign = inits[foreign_seed(seed)]
        raw = hidden_reversion(
            ft_eval["model"],
            ft_eval["predictions"],
            ft_eval["errors"],
            w0["rnn.weight_hh_l0"],
            w0["rnn.bias_hh_l0"],
            foreign["rnn.weight_hh_l0"],
            seed,
            world,
        )
        base_variation = variation_stats(ft_eval["predictions"], world)
        reversion = {}
        sham_all = True
        for gate in GATES:
            block = raw[gate]
            block.pop("predictions_rev", None)
            versions = {}
            for version in ("uniform", "probability", "test"):
                pr_random = [
                    _pack_variation_pair(item[version]["PD"], base_variation[version]["PD"])
                    for item in block["variation_random"]
                ]
                cr_random = [
                    _pack_variation_pair(item[version]["CD"], base_variation[version]["CD"])
                    for item in block["variation_random"]
                ]
                versions[version] = {
                    "PD_base": base_variation[version]["PD"],
                    "CD_base": base_variation[version]["CD"],
                    "PD_rev": block["variation_rev"][version]["PD"],
                    "CD_rev": block["variation_rev"][version]["CD"],
                    "PR": _pack_variation_pair(block["variation_rev"][version]["PD"], base_variation[version]["PD"]),
                    "CR": _pack_variation_pair(block["variation_rev"][version]["CD"], base_variation[version]["CD"]),
                    "PR_random": pr_random,
                    "CR_random": cr_random,
                }
            uniform_pr = pdcd_ratio(block["variation_rev"]["uniform"]["PD"], base_variation["uniform"]["PD"])
            uniform_cr = pdcd_ratio(block["variation_rev"]["uniform"]["CD"], base_variation["uniform"]["CD"])
            uniform_pr_random = [
                pdcd_ratio(item["uniform"]["PD"], base_variation["uniform"]["PD"])
                for item in block["variation_random"]
            ]
            random_totals = [item["TEST"]["total"] for item in block["random_delta_E"]]
            joint = specific_joint(
                passed_transfer,
                -1.0 if benefit is None else benefit,
                block["delta_E"]["TEST"]["total"],
                random_totals,
                block["delta_norm"],
            )
            if cand_eval is not None:
                rows = GATE_ROWS[gate]
                init_block = gate_block(w0["rnn.weight_hh_l0"], gate).double()
                original_errors = original_readout_excess(cand_eval["model"], init_block, rows, world)
            else:
                original_errors = None
            sham_all = sham_all and block["sham_ok"] and block["restore_ok"] and block["finite"]
            reversion[gate] = {
                "delta_norm": block["delta_norm"],
                "zero_displacement": block["zero_displacement"],
                "delta_E": block["delta_E"],
                "random_delta_E_total_TEST": random_totals,
                "random_max_TEST": None if not random_totals else float(max(random_totals)),
                "random_min_TEST": None if not random_totals else float(min(random_totals)),
                "random_delta_E": _pack_delta_list(block["random_delta_E"]),
                "sham_gap": block["sham_gap"],
                "restore_gap": block["restore_gap"],
                "sham_ok": block["sham_ok"],
                "restore_ok": block["restore_ok"],
                "finite": block["finite"],
                "pdcd": versions,
                "variation_pass": bool(
                    variation_joint(True, uniform_pr, uniform_pr_random, uniform_cr)
                ),
                "specific_pass": bool(joint),
                "descriptive_delta_E": block["descriptive_delta_E"],
                "original_readout_errors": original_errors,
                "foreign_seed": foreign_seed(seed),
            }
        section5_valid = bool(section3_valid and sham_all)

    section4_valid = bool(cand_integrity and rt_record is not None and rt_record["integrity"])
    e_rt = _total(rt_eval, "TEST")
    ratio843 = _safe_ratio(e_cand, e_rt)
    ratio843_pass = False
    if section4_valid and e_cand is not None and e_rt is not None:
        if math.isfinite(e_cand) and math.isfinite(e_rt):
            ratio843_pass = ratio_at_most_half(e_cand, e_rt)
    e_fu = _total(fu_eval, "TEST")
    ratio_tuned32 = _safe_ratio(e_ft, e_fu)

    p1 = {}
    for name, evaluation in (("cand", cand_eval), ("f_trained", ft_eval), ("f_init", fi_eval)):
        if evaluation is None:
            p1[name] = None
            continue
        report = decoder_report(np.asarray(_stage4(evaluation["states"]), dtype=np.float64), world.stage4_chart)
        p1[name] = {
            "label": decoder_label(report),
            "largest_interfold_angle_deg": report["largest_interfold_angle_deg"],
            "interfold_angles_deg": report["interfold_angles_deg"],
            "folds": {
                str(fold): {
                    "r2": report["folds"][fold]["r2"],
                    "rmse": report["folds"][fold]["rmse"],
                    "singular_values": report["folds"][fold]["singular_values"],
                    "rank": report["folds"][fold]["rank"],
                }
                for fold in (0, 1)
            },
        }

    record = {
        "seed": seed,
        "foreign_seed": foreign_seed(seed),
        "cand": cand_record,
        "f_trained": ft_record,
        "f_init": fi_record,
        "f_tuned32": fu_record,
        "r_tuned843": rt_record,
        "selection": {
            "ok": selection_ok,
            "grid": [{key: _curve_value(value) for key, value in row.items()} for row in grid],
            "g_star": None if chosen is None else chosen["g"],
            "b_star": None if chosen is None else chosen["b"],
            "tie": tie,
            "edge": None if chosen is None else is_grid_edge(chosen["g"], chosen["b"]),
            "selection_steps": 9 * steps,
        },
        "section3_valid": section3_valid,
        "section4_valid": section4_valid,
        "section5_valid": section5_valid,
        "transfer_pass": passed_transfer,
        "benefit_B": benefit,
        "ratio843": ratio843,
        "ratio843_pass": ratio843_pass,
        "ratio_f_tuned32": ratio_tuned32,
        "readout_gap_TEST": None if e_cand is None or e_ft is None else float(e_cand - e_ft),
        "readout_gap_TRAIN": None
        if cand_eval is None or ft_eval is None
        else float(cand_eval["errors"]["TRAIN"]["total"] - ft_eval["errors"]["TRAIN"]["total"]),
        "reversion": reversion,
        "p1": p1,
        "e1_pass": bool(cand_integrity and cand_record["afit_test"] and cand_record["alearn"]),
    }
    return to_jsonable(record)


def _flags(records, valid_key, pass_key):
    return [(bool(record[valid_key]), bool(record[pass_key])) for record in records]


def summarize(records: list[dict], p2: dict, world) -> dict:
    e1_flags = [bool(record["e1_pass"]) for record in records]
    transfer_flags = _flags(records, "section3_valid", "transfer_pass")
    advantage_flags = _flags(records, "section4_valid", "ratio843_pass")
    rival_flags = [
        (
            bool(record["section4_valid"]),
            bool(record["r_tuned843"]["afit_test"]) if record["r_tuned843"] else False,
        )
        for record in records
    ]
    specific = {}
    variation = {}
    for gate in GATES:
        specific_flags = []
        variation_flags = []
        for record in records:
            block = None if not record["reversion"] else record["reversion"][gate]
            specific_flags.append((bool(record["section5_valid"]), bool(block["specific_pass"]) if block else False))
            variation_flags.append(
                (bool(record["section5_valid"]), bool(block["variation_pass"]) if block else False)
            )
        specific[gate] = {
            "label": label_specific(specific_flags, gate),
            "pass_count": sum(1 for valid, passed in specific_flags if valid and passed),
            "invalid": sum(1 for valid, _passed in specific_flags if not valid),
        }
        variation[gate] = {
            "label": label_variation(specific[gate]["label"], variation_flags, gate),
            "pass_count": sum(1 for valid, passed in variation_flags if valid and passed),
            "invalid": sum(1 for valid, _passed in variation_flags if not valid),
        }
    e1 = label_e1(e1_flags)
    transfer = label_transfer(transfer_flags)
    advantage = label_advantage(advantage_flags)
    rival = label_rival_afit(rival_flags)
    rival_count = sum(1 for valid, passed in rival_flags if valid and passed)
    claim = assemble_claim(
        e1,
        transfer,
        {gate: specific[gate]["label"] for gate in GATES},
        {gate: variation[gate]["label"] for gate in GATES},
        advantage,
        rival,
        rival_count,
    )
    p1_counts = {}
    for name in ("cand", "f_trained", "f_init"):
        p1_counts[name] = sum(
            1
            for record in records
            if record["p1"][name] and record["p1"][name]["label"] == "DECODER PREDICTIVE AND CROSS-FOLD STABLE"
        )
    return {
        "e1": {"label": e1, "count": sum(e1_flags)},
        "transfer": {
            "label": transfer,
            "pass_count": sum(1 for valid, passed in transfer_flags if valid and passed),
            "invalid": sum(1 for valid, _passed in transfer_flags if not valid),
        },
        "f_init_afit": sum(1 for record in records if record["f_init"] and record["f_init"]["afit_test"]),
        "f_tuned32_afit": sum(
            1 for record in records if record["f_tuned32"] and record["f_tuned32"]["afit_test"]
        ),
        "advantage": {
            "label": advantage,
            "pass_count": sum(1 for valid, passed in advantage_flags if valid and passed),
            "invalid": sum(1 for valid, _passed in advantage_flags if not valid),
        },
        "rival_afit": {"label": rival, "count": rival_count, "invalid": sum(1 for valid, _p in rival_flags if not valid)},
        "specific": specific,
        "variation": variation,
        "p1_counts": p1_counts,
        "p2": p2["summary"],
        "oracle_variation": variation_stats(world.q, world),
        "claim": claim,
    }


def render_markdown(records: list[dict], summary: dict) -> str:
    lines = [
        "# Recurrent-core transfer results",
        "",
        "Protocol `%s` sha256 `%s`." % (PROTOCOL_FILENAME, PROTOCOL_SHA256),
        "",
        "## Claim",
        "",
        summary["claim"],
        "",
        "## Labels",
        "",
        "- E1: %s (%d/10)" % (summary["e1"]["label"], summary["e1"]["count"]),
        "- Transfer: %s (%d/10 passes, %d invalid)"
        % (summary["transfer"]["label"], summary["transfer"]["pass_count"], summary["transfer"]["invalid"]),
        "- F-INIT A-FIT on TEST: %d/10" % summary["f_init_afit"],
        "- F-TUNED32 A-FIT on TEST: %d/10" % summary["f_tuned32_afit"],
        "- ratio843: %s (%d/10 passes, %d invalid)"
        % (summary["advantage"]["label"], summary["advantage"]["pass_count"], summary["advantage"]["invalid"]),
        "- R-TUNED843 A-FIT: %s (%d/10, %d invalid)"
        % (summary["rival_afit"]["label"], summary["rival_afit"]["count"], summary["rival_afit"]["invalid"]),
    ]
    for gate in GATES:
        lines.append(
            "- %s (%d/10 passes, %d invalid)"
            % (summary["specific"][gate]["label"], summary["specific"][gate]["pass_count"], summary["specific"][gate]["invalid"])
        )
        lines.append(
            "- variation %s: %s (%d/10)"
            % (gate, summary["variation"][gate]["label"], summary["variation"][gate]["pass_count"])
        )
    lines.append("- P2: %s" % summary["p2"]["label"])
    minus = summary["p2"]["p2_minus"]
    lines.append(
        "- P2− zero-effect: %s (max abs change %s)"
        % (minus["zero_effect_ok"], minus["max_abs_change"])
    )
    for name, count in summary["p1_counts"].items():
        lines.append("- P1 %s DECODER PREDICTIVE AND CROSS-FOLD STABLE: %d/10" % (name, count))
    lines.extend(["", "## Per-seed transfer", "", "| seed | E1 | valid3 | CAND | F-TRAINED | F-INIT | F-TUNED32 | R-TUNED843 | transfer | B | g* | b* | edge |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
    for record in records:
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                record["seed"],
                record["e1_pass"],
                record["section3_valid"],
                _cell(record["cand"]),
                _cell(record["f_trained"]),
                _cell(record["f_init"]),
                _cell(record["f_tuned32"]),
                _cell(record["r_tuned843"]),
                record["transfer_pass"],
                _fmt(record["benefit_B"]),
                record["selection"]["g_star"],
                record["selection"]["b_star"],
                record["selection"]["edge"],
            )
        )
    lines.extend(["", "## VAL curve", ""])
    for record in records:
        cells = ", ".join(
            "g=%s b=%s %s" % (row["g"], row["b"], _fmt(row["criterion"])) for row in record["selection"]["grid"]
        )
        lines.append("- seed %d tie=%s: %s" % (record["seed"], record["selection"]["tie"], cells))
    lines.extend(["", "## Hidden-to-hidden reversion", ""])
    for gate in GATES:
        lines.extend(
            [
                "### %s" % gate,
                "",
                "| seed | delta_norm | dE_X | dE_Y | dE_XOR | dE | max RND | min RND | specific | sham | restore | PR | CR | variation |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for record in records:
            block = None if not record["reversion"] else record["reversion"][gate]
            if block is None:
                lines.append("| %d | missing ||||||||| |" % record["seed"])
                continue
            delta = block["delta_E"]["TEST"]
            lines.append(
                "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                % (
                    record["seed"],
                    _fmt(block["delta_norm"]),
                    _fmt(delta["X"]),
                    _fmt(delta["Y"]),
                    _fmt(delta["XOR"]),
                    _fmt(delta["total"]),
                    _fmt(block["random_max_TEST"]),
                    _fmt(block["random_min_TEST"]),
                    block["specific_pass"],
                    _fmt(block["sham_gap"]),
                    _fmt(block["restore_gap"]),
                    block["pdcd"]["uniform"]["PR"],
                    block["pdcd"]["uniform"]["CR"],
                    block["variation_pass"],
                )
            )
            uniform = block["pdcd"]["uniform"]
            probability = block["pdcd"]["probability"]
            restricted = block["pdcd"]["test"]
            lines.append(
                "Seed %d %s PD/CD uniform %s/%s PR/CR %s/%s; probability %s/%s PR/CR %s/%s; TEST-restricted %s/%s PR/CR %s/%s."
                % (
                    record["seed"],
                    gate,
                    _fmt(uniform["PD_base"]),
                    _fmt(uniform["CD_base"]),
                    uniform["PR"],
                    uniform["CR"],
                    _fmt(probability["PD_rev"]),
                    _fmt(probability["CD_rev"]),
                    probability["PR"],
                    probability["CR"],
                    _fmt(restricted["PD_rev"]),
                    _fmt(restricted["CD_rev"]),
                    restricted["PR"],
                    restricted["CR"],
                )
            )
        lines.append("")
        for record in records:
            block = None if not record["reversion"] else record["reversion"][gate]
            if block is None:
                continue
            draws = ", ".join(_fmt(value) for value in block["random_delta_E_total_TEST"])
            lines.append("Seed %d %s RND ΔE_total TEST (32): %s" % (record["seed"], gate, draws))
        lines.append("")
    lines.extend(["", "## P2", ""])
    for scale, row in summary["p2"]["per_scale"].items():
        lines.append(
            "- s=%s known-Q LOCALIZED %d/%d, fitted LOCALIZED %d/%d, median angle to span(Q) %s"
            % (
                scale,
                row["known_q_localized"],
                row["n"],
                row["fitted_localized"],
                row["n"],
                row["median_largest_angle_to_span_Q_deg"],
            )
        )
    lines.append("")
    lines.append(summary["p2"]["note"])
    lines.append("")
    lines.append("P2− fitted descriptive LOCALIZED %d/%d. Invalid: %s." % (
        summary["p2"]["p2_minus"]["fitted_localized"],
        summary["p2"]["p2_minus"]["n"],
        summary["p2"]["p2_minus"]["invalid"],
    ))
    lines.extend(["", "## Invalid seeds", ""])
    lines.append("- §3 invalid: %s" % _invalid_list(records, "section3_valid"))
    lines.append("- §4 invalid: %s" % _invalid_list(records, "section4_valid"))
    lines.append("- §5 invalid: %s" % _invalid_list(records, "section5_valid"))
    lines.extend(["", "## Ratio and readout notes", ""])
    for record in records:
        lines.append(
            "- seed %d ratio843=%s pass=%s F-TRAINED/F-TUNED32=%s readout gap TEST=%s"
            % (
                record["seed"],
                record["ratio843"],
                record["ratio843_pass"],
                record["ratio_f_tuned32"],
                _fmt(record["readout_gap_TEST"]),
            )
        )
    lines.extend(["", "Oracle uniform PD=%s CD=%s." % (
        _fmt(summary["oracle_variation"]["uniform"]["PD"]),
        _fmt(summary["oracle_variation"]["uniform"]["CD"]),
    )])
    lines.append("")
    lines.append("Deviations: `DEVIATIONS_AND_AMBIGUITIES.md`.")
    lines.append("")
    return "\n".join(lines)


def _cell(arm) -> str:
    if not arm or arm["errors"] is None:
        return "missing"
    return _fmt(arm["errors"]["TEST"]["total"])


def _fmt(value) -> str:
    if value is None:
        return "missing"
    if isinstance(value, str):
        return value
    if isinstance(value, float) and not np.isfinite(value):
        return "+inf" if value > 0 else str(value)
    if isinstance(value, float):
        return "%.6g" % value
    return str(value)


def _invalid_list(records, key) -> str:
    seeds = [str(record["seed"]) for record in records if not record[key]]
    return "none" if not seeds else ", ".join(seeds)


def to_jsonable(value):
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return to_jsonable(value.tolist())
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if not np.isfinite(number):
            return None
        return number
    if isinstance(value, (np.str_,)):
        return str(value)
    return value


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(to_jsonable(payload), indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run_study() -> None:
    _require_freeze()
    configure_runtime()
    world = World()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    checkpoint_dir = RESULTS_DIR / "checkpoints"
    seed_dir = RESULTS_DIR / "seeds"
    seed_dir.mkdir(parents=True, exist_ok=True)
    inits = {}
    for seed in SEEDS:
        model = build_initialized(seed, READOUT_32)
        inits[seed] = snapshot_state(model)
    records = []
    for seed in SEEDS:
        path = seed_dir / ("s%d.json" % seed)
        if path.exists():
            print("resume %s" % path.name, flush=True)
            records.append(json.loads(path.read_text(encoding="utf-8")))
            continue
        record = run_seed(seed, world, inits, checkpoint_dir, STEPS)
        _write_json(path, record)
        records.append(record)
    p2_path = RESULTS_DIR / "p2.json"
    if p2_path.exists():
        p2 = json.loads(p2_path.read_text(encoding="utf-8"))
    else:
        p2 = run_p2(world)
        _write_json(p2_path, p2)
    summary = summarize(records, p2, world)
    payload = {
        "protocol_sha256": PROTOCOL_SHA256,
        "environment": {
            "python": sys.version,
            "torch": torch.__version__,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "summary": summary,
        "seeds": records,
        "p2_summary": p2["summary"],
    }
    _write_json(RESULTS_DIR / "results.json", payload)
    (RESULTS_DIR / "RESULTS.md").write_text(render_markdown(records, summary), encoding="utf-8")
    print(summary["claim"], flush=True)
    print("P2 %s" % summary["p2"]["label"], flush=True)


if __name__ == "__main__":
    run_study()
