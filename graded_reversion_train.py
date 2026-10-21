"""Phase B training for fresh GRU-8 seeds 200–209.

The recipe is recurrent_core_transfer_train.train_arm, unchanged: 4000 steps,
batch 256, Adam, cosine learning rate, clip 1.0, TEST rejection, one thread.
This module does not run Appendix A. The study runner calls it only after the
approval note, the freeze, and a phase A engineering status with no blocking issue.
"""

from __future__ import annotations

import json
from pathlib import Path

import torch

from graded_reversion_spec import (
    PHASE_B_SEEDS,
    READOUT_32,
    TARGETS,
)
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
from recurrent_core_transfer_metrics import evaluate_arm
from recurrent_core_transfer_train import train_arm
from twostream_acquisition_metrics import afit_holds


def configure_runtime() -> None:
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def build_inits(seeds=PHASE_B_SEEDS) -> dict:
    """Match the PR #7 order: every initialization is drawn before any training."""
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


def train_phase_b_seed(seed: int, world, w0: dict, directory: Path) -> dict:
    """Train CAND, F-TRAINED, and F-INIT for one fresh seed. Does not score curves.

    If CAND training fails there is no W_T, so F-TRAINED is not trained. F-INIT
    still trains from W_0. Missing F-TRAINED cells stay missing.
    """
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
    f_trained_state = None
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
            f_trained_state = state
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
        "f_trained_state_saved": f_trained_state is not None,
    }


def missing_evaluation(seed: int, reasons: list[str]) -> dict:
    """A seed record when the graded curve cannot be computed. Cells stay missing."""
    false_map = {target: False for target in TARGETS}
    reason_map = {target: ["invalid"] for target in TARGETS}
    return {
        "seed": int(seed),
        "code_version": "graded-reversion-v1",
        "curves_missing": True,
        "engineering_flags": [],
        "valid": False,
        "invalid_reasons": list(reasons),
        "checkpoint_ok": False,
        "transfer_pass": False,
        "afit_f_trained": False,
        "B_prefix": None,
        "C_prefix": None,
        "B_prefix_over_PD": None,
        "C_prefix_over_PD": None,
        "L_prefix_f_trained": None,
        "L_prefix_f_trained_over_PD": None,
        "L_prefix_f_init": None,
        "E_TEST_f_trained": None,
        "E_TEST_f_init": None,
        "eligible": false_map,
        "eligibility_reasons": reason_map,
        "joint": dict(false_map),
        "targets": None,
        "PD_q_star": None,
        "forecast_change_max_abs_primary": None,
    }


def refusal_reason(approval_ok: bool, freeze_ok: bool, status) -> str | None:
    """Pure guard used by the runner and by the freeze tests. None means proceed."""
    if not approval_ok:
        return "Phase B training approval note is missing or does not match the required record."
    if not freeze_ok:
        return "Freeze manifest does not match the current code."
    if status is None:
        return "Phase A has not been completed."
    if status.get("code_version") != "graded-reversion-v1":
        return "Phase A engineering status is from a different code version."
    if status.get("blocking_engineering_issue"):
        return (
            "Phase A surfaced an engineering issue that must be versioned and hashed before phase B."
        )
    return None


def approval_text_ok(text: str, protocol_sha256: str) -> bool:
    required = (
        "Aidan Ahern",
        "2026-10-20",
        "10:38 PM ET",
        "Grok Bot chat",
        "Yes, approve it once Astra clears it",
        protocol_sha256,
        "Appendix A",
    )
    return all(piece in text for piece in required)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
