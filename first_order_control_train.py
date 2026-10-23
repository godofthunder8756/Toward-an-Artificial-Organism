"""Phase B training for fresh GRU-8 seeds 300-309.

The recipe is recurrent_core_transfer_train.train_arm, unchanged: 4000 steps,
batch 256, Adam, cosine 1e-3 to 1e-4, clip 1.0, one thread, deterministic.
Thirty runs are CAND, F-TRAINED and F-INIT. This module does not evaluate
dose curves and does not run an extra rival grid.
"""

from __future__ import annotations

from pathlib import Path

import torch

from first_order_control_spec import BLOCKS, CODE_VERSION, PHASE_B_SEEDS, TARGETS
from graded_reversion_spec import READOUT_32
from recurrent_core_transfer_metrics import evaluate_arm
from recurrent_core_transfer_models import (
    CoreGRU,
    build_initialized,
    checkpoint_sha256,
    copy_recurrent,
    load_checkpoint,
    load_snapshot,
    save_checkpoint,
    snapshot_state,
)
from recurrent_core_transfer_train import train_arm
from twostream_acquisition_metrics import afit_holds


def configure_runtime() -> None:
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def build_inits(seeds=PHASE_B_SEEDS) -> dict:
    """Every initialization is drawn before any training, in seed order."""
    inits = {}
    for seed in seeds:
        inits[int(seed)] = snapshot_state(build_initialized(int(seed), READOUT_32))
    return inits


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


def _arm_integrity(train_info, evaluation, checkpoint_ok: bool, init_outputs_valid: bool = True) -> bool:
    if not train_info["integrity_training"] or not checkpoint_ok or not init_outputs_valid:
        return False
    if evaluation is None:
        return False
    return bool(evaluation["outputs_valid"] and evaluation["identity"]["ok"])


def train_confirmation_seed(seed: int, world, w0: dict, directory: Path) -> dict:
    """Train CAND, F-TRAINED and F-INIT. Does not score FO or ISO curves."""
    directory.mkdir(parents=True, exist_ok=True)
    init_digest, init_ok = _store(directory, "s%d_cand_init.ckpt" % seed, w0)
    cand = CoreGRU(READOUT_32)
    load_snapshot(cand, w0)
    init_eval = evaluate_arm(cand, world)
    cand_info = train_arm(cand, seed, False, False)
    cand_state = snapshot_state(cand)
    cand_digest, cand_ok = _store(directory, "s%d_cand_final.ckpt" % seed, cand_state)
    cand_eval = evaluate_arm(cand, world) if cand_info["integrity_training"] else None
    cand_integrity = _arm_integrity(
        cand_info,
        cand_eval,
        cand_ok and init_ok,
        bool(init_eval["outputs_valid"]),
    )
    init_afit = bool(afit_holds(init_eval["errors"], world, "TEST")) if init_eval is not None else False
    cand_afit = bool(afit_holds(cand_eval["errors"], world, "TEST")) if cand_eval is not None else False
    alearn = not init_afit
    training = {
        "cand": {
            "integrity_training": cand_info["integrity_training"],
            "steps_completed": cand_info["steps_completed"],
            "failure_step": cand_info["failure_step"],
            "checkpoint_sha256": cand_digest,
            "init_checkpoint_sha256": init_digest,
            "checkpoint_ok": bool(cand_ok and init_ok),
            "integrity": cand_integrity,
            "afit_test": cand_afit,
            "init_afit_test": init_afit,
            "alearn": alearn,
            "outputs_valid": None if cand_eval is None else bool(cand_eval["outputs_valid"]),
            "init_outputs_valid": bool(init_eval["outputs_valid"]),
        }
    }
    expected = {"cand_init": init_digest}
    if cand_info["integrity_training"]:
        model = build_initialized(5000 + seed, READOUT_32)
        copy_recurrent(model, cand_state)
        info = train_arm(model, seed, True, False)
        state = snapshot_state(model)
        digest, ok = _store(directory, "s%d_f_trained.ckpt" % seed, state)
        training["f_trained"] = {
            "integrity_training": info["integrity_training"],
            "steps_completed": info["steps_completed"],
            "failure_step": info["failure_step"],
            "checkpoint_sha256": digest,
            "checkpoint_ok": ok,
        }
        if info["integrity_training"] and ok:
            expected["f_trained"] = digest
    else:
        training["f_trained"] = None

    model = build_initialized(5000 + seed, READOUT_32)
    copy_recurrent(model, w0)
    info = train_arm(model, seed, True, False)
    state = snapshot_state(model)
    digest, ok = _store(directory, "s%d_f_init.ckpt" % seed, state)
    training["f_init"] = {
        "integrity_training": info["integrity_training"],
        "steps_completed": info["steps_completed"],
        "failure_step": info["failure_step"],
        "checkpoint_sha256": digest,
        "checkpoint_ok": ok,
    }
    if info["integrity_training"] and ok:
        expected["f_init"] = digest

    ready = "f_trained" in expected and "f_init" in expected and "cand_init" in expected
    return {
        "seed": int(seed),
        "e1_pass": bool(cand_integrity and cand_afit and alearn),
        "training_ready": ready,
        "training": training,
        "expected_hashes": expected if ready else None,
    }


def missing_evaluation(seed: int, reasons: list[str]) -> dict:
    """Curve cells stay missing when training did not produce the three checkpoints."""
    false_map = {target: False for target in TARGETS}
    collapsed = {name: False for name in BLOCKS}
    summary = {}
    for target in TARGETS:
        summary[target] = {
            "collapsed": False,
            "eligible": False,
            "eligibility_reasons": ["invalid"],
            "D_FO": None,
            "D_ISO": None,
            "D": None,
            "M": None,
            "joint": False,
            "auc_rev": None,
            "fo": None,
            "iso": None,
            "conditions": {
                "valid": "fail",
                "eligible": "fail",
                "D_FO": "not_evaluated",
                "D_ISO": "not_evaluated",
                "M": "not_evaluated",
                "joint": "fail",
            },
        }
    return {
        "seed": int(seed),
        "code_version": CODE_VERSION,
        "curves_missing": True,
        "engineering_flags": [],
        "valid": False,
        "invalid_reasons": list(reasons),
        "transfer_pass": False,
        "afit_f_trained": False,
        "B_prefix": None,
        "C_prefix": None,
        "B_prefix_over_PD": None,
        "C_prefix_over_PD": None,
        "L_prefix_f_trained": None,
        "L_prefix_f_init": None,
        "PD_q_star": None,
        "eligible": dict(false_map),
        "eligibility_reasons": {target: ["invalid"] for target in TARGETS},
        "joint": dict(false_map),
        "primary_collapsed": False,
        "block_collapsed": collapsed,
        "summary": summary,
        "targets": None,
        "geometry": None,
        "hashes": None,
    }
