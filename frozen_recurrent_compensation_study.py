"""Two-stage sealed runner for frozen recurrent matrices with learned compensation.

Stage 0 draws inits and episode digests. Stage 1 trains and does not score.
Stage 2 scores only checkpoints whose sha matches the sealed manifests.
No consciousness claim. No appendix is executed.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch

from recurrent_core_transfer_models import (
    CoreGRU,
    checkpoint_sha256,
    load_checkpoint,
    load_snapshot,
    save_checkpoint,
    snapshot_state,
)
from recurrent_core_transfer_spec import BATCH, STEPS, is_val_history
from twostream_acquisition_oracle import World
from twostream_acquisition_spec import cosine_lr

from frozen_recurrent_compensation_labels import (
    arm_counts,
    best_and_median,
    binding_frequencies,
    format_counts_block,
    ledger_lines,
    paired_differences,
    render_report,
    stage1_final_reasons,
    statements_for_arm,
    status_from,
)
from frozen_recurrent_compensation_spec import (
    ARM_HIDDEN,
    ARMS,
    COMPARATOR_UNRESOLVED,
    INVALID,
    CODE_FILES,
    PROTOCOL_FILENAME,
    PROTOCOL_SHA256,
    REPRO_YES,
    RESULTS_DIRNAME,
    SEEDS,
    TAU,
    code_tree_sha256,
    components_agree,
    protocol_sha256,
)
from frozen_recurrent_compensation_train import (
    configure_runtime,
    draw_seed,
    episode_stream_digest,
    run_synthetic_fixture,
    tensor_sha256,
    train_arm_rfix,
    train_cand,
)

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / RESULTS_DIRNAME
STAGE0_MANIFEST = RESULTS / "stage0" / "manifest_stage0.json"
STAGE1_MANIFEST = RESULTS / "stage1" / "manifest_stage1.json"
STAGE1_PROGRESS = RESULTS / "stage1" / "progress.jsonl"
STAGE2_JSON = RESULTS / "stage2" / "results.json"
STAGE2_MD = RESULTS / "stage2" / "RESULTS.md"

SCORE_KEYS = {
    "T",
    "T_repr",
    "L_prefix",
    "C_prefix",
    "G_prefix",
    "components",
    "classification",
    "numeric_class",
    "binding_E1",
    "binding_E2",
    "witness",
    "existence_label",
    "reproducibility_label",
    "acquisition",
    "E_TEST",
    "E_TRAIN",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def to_jsonable(value):
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if not math.isfinite(number):
            return None
        return number
    if value is None or isinstance(value, str):
        return value
    raise TypeError(type(value))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(to_jsonable(payload), indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def assert_no_scores(value, path: str = "") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in SCORE_KEYS:
                raise RuntimeError("stage 1 record contains a score key: %s%s" % (path, key))
            assert_no_scores(item, path + key + ".")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            assert_no_scores(item, "%s[%d]." % (path, index))


def git_output(args: list[str]) -> str:
    proc = subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def assert_committed(relative: str) -> str:
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", relative],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    if status.stdout.strip():
        raise SystemExit("not sealed, dirty: %s\n%s" % (relative, status.stdout))
    listed = subprocess.run(
        ["git", "ls-files", "--error-unmatch", relative],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if listed.returncode != 0:
        raise SystemExit("not committed: %s" % relative)
    return git_output(["git", "log", "-1", "--format=%H", "--", relative])


def assert_code_matches_stage0(stage0: dict) -> None:
    if protocol_sha256() != PROTOCOL_SHA256:
        raise SystemExit("protocol hash changed after the freeze text")
    if code_tree_sha256() != stage0["code_tree_sha256"]:
        raise SystemExit("code changed after the stage 0 seal")
    names = list(stage0["code_files_sha256"])
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", *names],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    if status.stdout.strip():
        raise SystemExit("code files are dirty:\n%s" % status.stdout)


def _empty_checkpoint() -> dict:
    return {
        "evaluated": False,
        "E1": None,
        "E2": None,
        "float32_descriptive": None,
        "components_agree": None,
        "agreement_gaps": None,
        "prediction_max_abs": None,
        "numeric_class": None,
        "binding_E1": None,
        "binding_E2": None,
        "outputs_valid_E1": None,
        "outputs_valid_E2": None,
        "identity_ok": None,
        "identity": None,
        "val_E1": None,
        "val_E2": None,
        "values_agree_T": None,
        "checkpoint_sha256": None,
        "w0_sha256": None,
        "w0_matches_stage0": None,
    }


def run_stage0() -> None:
    if STAGE0_MANIFEST.exists():
        raise SystemExit("stage 0 manifest already exists; refuse to redraw")
    if STEPS != 4000 or BATCH != 256:
        raise SystemExit("PR #7 recipe constants are not 4000 steps and batch 256")
    if abs(cosine_lr(0, STEPS) - 1e-3) > 1e-15 or abs(cosine_lr(STEPS - 1, STEPS) - 1e-4) > 1e-15:
        raise SystemExit("cosine schedule endpoints differ from 1e-3 and 1e-4")
    if protocol_sha256() != PROTOCOL_SHA256:
        raise SystemExit("protocol file hash does not match the reviewed text")
    configure_runtime()
    print("stage0 synthetic fixture", flush=True)
    fixture = run_synthetic_fixture(return_model=False)
    seeds = {}
    init_dir = RESULTS / "stage0" / "checkpoints"
    init_dir.mkdir(parents=True, exist_ok=True)
    for seed in SEEDS:
        print("stage0 draw seed %d" % seed, flush=True)
        states = draw_seed(seed)
        arms = {}
        w0_hashes = []
        for arm in ARMS:
            path = init_dir / ("s%d_%s.json" % (seed, arm))
            sha = save_checkpoint(path, states[arm])
            loaded = load_checkpoint(path)
            if checkpoint_sha256(loaded) != sha:
                raise SystemExit("init round-trip failed for %s %s" % (seed, arm))
            for key, tensor in states[arm].items():
                if not torch.equal(tensor, loaded[key]):
                    raise SystemExit("init tensor mismatch for %s %s %s" % (seed, arm, key))
            w0 = tensor_sha256(states[arm]["rnn.weight_hh_l0"])
            w0_hashes.append(w0)
            arms[arm] = {
                "init_checkpoint_sha256": sha,
                "init_checkpoint_file": path.relative_to(ROOT).as_posix(),
                "w0_sha256": w0,
                "stored_parameters": sum(int(tensor.numel()) for tensor in states[arm].values()),
                "H": ARM_HIDDEN[arm],
            }
        if len(set(w0_hashes)) != 1:
            raise SystemExit("W0 hash differs inside seed %d" % seed)
        print("stage0 digest seed %d" % seed, flush=True)
        digest = episode_stream_digest(seed, STEPS, BATCH)
        seeds[str(seed)] = {
            "episode_digest": digest,
            "episode_generator_seed": 1000 + seed,
            "w0_sha256": w0_hashes[0],
            "pairing_ok": True,
            "arms": arms,
        }
    manifest = {
        "study": "Frozen recurrent matrices with learned compensation",
        "stage": 0,
        "scoring": False,
        "protocol_file": PROTOCOL_FILENAME,
        "protocol_sha256": PROTOCOL_SHA256,
        "code_tree_sha256": code_tree_sha256(),
        "code_files_sha256": {name: sha256_file(ROOT / name) for name in sorted(CODE_FILES)},
        "synthetic_fixture": fixture,
        "seeds": seeds,
        "draw_order": "seeds 400-409; within a seed CAND, R-FIX-32, R-FIX-48",
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
    }
    assert_no_scores(manifest)
    write_json(STAGE0_MANIFEST, manifest)
    print("stage0 wrote %s" % STAGE0_MANIFEST, flush=True)


def _load_stage0() -> dict:
    if not STAGE0_MANIFEST.exists():
        raise SystemExit("stage 0 manifest is missing")
    stage0 = json.loads(STAGE0_MANIFEST.read_text(encoding="utf-8"))
    if stage0.get("protocol_sha256") != PROTOCOL_SHA256:
        raise SystemExit("stage 0 protocol hash mismatch")
    if sha256_file(ROOT / PROTOCOL_FILENAME) != PROTOCOL_SHA256:
        raise SystemExit("protocol file changed")
    return stage0


def _load_progress() -> dict:
    if not STAGE1_PROGRESS.exists():
        return {}
    rows = {}
    for line in STAGE1_PROGRESS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows[(int(row["seed"]), row["arm"])] = row
    return rows


def _append_progress(row: dict) -> None:
    STAGE1_PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    with STAGE1_PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(to_jsonable(row), allow_nan=False) + "\n")
        handle.flush()


def _train_one(seed: int, arm: str, stage0: dict) -> dict:
    spec = stage0["seeds"][str(seed)]["arms"][arm]
    init_path = ROOT / spec["init_checkpoint_file"]
    sealed = load_checkpoint(init_path)
    if checkpoint_sha256(sealed) != spec["init_checkpoint_sha256"]:
        raise SystemExit("sealed init file does not match stage 0 for %s %s" % (seed, arm))
    rebuilt = draw_seed(seed)[arm]
    if checkpoint_sha256(rebuilt) != spec["init_checkpoint_sha256"]:
        raise SystemExit("rebuilt init does not match the sealed init for %s %s" % (seed, arm))
    model = CoreGRU(ARM_HIDDEN[arm])
    load_snapshot(model, sealed)
    started = time.perf_counter()
    if arm == "CAND":
        info = train_cand(model, seed)
    else:
        info = train_arm_rfix(model, seed)
    final_dir = RESULTS / "stage1" / "checkpoints"
    final_dir.mkdir(parents=True, exist_ok=True)
    final_path = final_dir / ("s%d_%s.json" % (seed, arm))
    state = snapshot_state(model)
    sha = save_checkpoint(final_path, state)
    loaded = load_checkpoint(final_path)
    roundtrip = checkpoint_sha256(loaded) == sha
    for key, tensor in state.items():
        if not torch.equal(tensor, loaded[key]):
            roundtrip = False
    w0_stage0 = stage0["seeds"][str(seed)]["w0_sha256"]
    w0_after = tensor_sha256(state["rnn.weight_hh_l0"])
    w0_reload = tensor_sha256(loaded["rnn.weight_hh_l0"])
    digest = info.get("episode_digest")
    expected = stage0["seeds"][str(seed)]["episode_digest"]
    if int(info["batches_hashed"]) == STEPS:
        digest_matches = bool(digest == expected)
    else:
        digest_matches = None
    record = {
        "seed": seed,
        "arm": arm,
        "init_checkpoint_sha256": spec["init_checkpoint_sha256"],
        "final_checkpoint_sha256": sha,
        "final_checkpoint_file": final_path.relative_to(ROOT).as_posix(),
        "integrity_training": bool(info["integrity_training"]),
        "steps_completed": int(info["steps_completed"]),
        "final_loss": info["final_loss"],
        "failure_step": info["failure_step"],
        "episode_digest": digest,
        "batches_hashed": int(info["batches_hashed"]),
        "episode_digest_matches_stage0": digest_matches,
        "checkpoint_round_trip": bool(roundtrip),
        "freezing_checks": info["freezing_checks"],
        "freezing_failure": info["freezing_failure"],
        "w0_sha256_after_training": w0_after,
        "w0_sha256_after_reload": w0_reload,
        "w0_matches_stage0_after_training": bool(w0_after == w0_stage0) if arm != "CAND" else None,
        "w0_matches_stage0_after_reload": bool(w0_reload == w0_stage0) if arm != "CAND" else None,
        "seconds": time.perf_counter() - started,
        "trainer": info["trainer"],
    }
    if arm == "CAND":
        record["w0_matches_stage0_after_training"] = None
        record["w0_matches_stage0_after_reload"] = None
    assert_no_scores(record)
    return record


def run_stage1() -> None:
    if STAGE1_MANIFEST.exists():
        raise SystemExit("stage 1 manifest already exists; refuse to train again")
    stage0 = _load_stage0()
    assert_committed(STAGE0_MANIFEST.relative_to(ROOT).as_posix())
    assert_code_matches_stage0(stage0)
    if STEPS != 4000 or BATCH != 256:
        raise SystemExit("recipe constants changed")
    configure_runtime()
    done = _load_progress()
    ordered = [(seed, arm) for seed in SEEDS for arm in ARMS]
    for seed, arm in ordered:
        if (seed, arm) in done:
            print("stage1 skip finished %d %s" % (seed, arm), flush=True)
            continue
        existing = RESULTS / "stage1" / "checkpoints" / ("s%d_%s.json" % (seed, arm))
        if existing.exists():
            raise SystemExit(
                "checkpoint exists without a progress line for %s %s; refuse to retrain" % (seed, arm)
            )
        print("stage1 seed %d %s starting" % (seed, arm), flush=True)
        record = _train_one(seed, arm, stage0)
        _append_progress(record)
        done[(seed, arm)] = record
        print(
            "stage1 seed %d %s done steps=%s integrity=%s loss=%s"
            % (seed, arm, record["steps_completed"], record["integrity_training"], record["final_loss"]),
            flush=True,
        )
    if len(done) != 30:
        raise SystemExit("stage 1 finished %d runs, not 30" % len(done))
    runs = [done[(seed, arm)] for seed, arm in ordered]
    manifest = {
        "study": "Frozen recurrent matrices with learned compensation",
        "stage": 1,
        "scoring": False,
        "protocol_sha256": PROTOCOL_SHA256,
        "code_tree_sha256": stage0["code_tree_sha256"],
        "stage0_manifest_sha256": sha256_file(STAGE0_MANIFEST),
        "runs": runs,
    }
    assert_no_scores(manifest)
    write_json(STAGE1_MANIFEST, manifest)
    print("stage1 wrote %s" % STAGE1_MANIFEST, flush=True)


def _weights_finite(state: dict) -> bool:
    for tensor in state.values():
        if not torch.isfinite(tensor).all():
            return False
    return True


def _prefix_gap(pd: float, init_block: dict, final_block: dict, which: str):
    if not init_block.get("evaluated") or not final_block.get("evaluated"):
        return None, None
    init_L = init_block[which]["L_prefix"]
    final_L = final_block[which]["L_prefix"]
    return float(pd - final_L), float(init_L - final_L)


def _invalidate_init(record: dict, reason: str) -> None:
    reasons = list(record["init_invalid_reasons"])
    if reason not in reasons:
        reasons.append(reason)
    record["init_invalid_reasons"] = reasons
    record["init_status"] = INVALID


def reconcile_shared_inits(records: list[dict]) -> None:
    index = {(record["seed"], record["arm"]): record for record in records}
    for seed in SEEDS:
        cand = index[(seed, "CAND")]
        other = index[(seed, "R-FIX-32")]
        if cand["init"]["checkpoint_sha256"] != other["init"]["checkpoint_sha256"]:
            _invalidate_init(cand, "pairing")
            _invalidate_init(other, "pairing")
            continue
        if cand["init_status"] != other["init_status"]:
            _invalidate_init(cand, "shared_init_classification_mismatch")
            _invalidate_init(other, "shared_init_classification_mismatch")
            continue
        if cand["init_status"] == INVALID:
            continue
        if not components_agree(cand["init"]["E1"]["components"], other["init"]["E1"]["components"]):
            _invalidate_init(cand, "shared_init_classification_mismatch")
            _invalidate_init(other, "shared_init_classification_mismatch")


def _score_checkpoint(path: Path, expected_sha: str, hidden: int, world, thr_total: float, thr_xor: float, val_mask, stage0_w0: str, check_w0: bool) -> tuple[dict, list[str]]:
    from frozen_recurrent_compensation_eval import evaluate_state, evaluation_reasons

    reasons = []
    block = _empty_checkpoint()
    if not path.exists():
        reasons.append("stage2_sha")
        return block, reasons
    state = load_checkpoint(path)
    actual = checkpoint_sha256(state)
    block["checkpoint_sha256"] = actual
    block["w0_sha256"] = tensor_sha256(state["rnn.weight_hh_l0"])
    if check_w0:
        block["w0_matches_stage0"] = bool(block["w0_sha256"] == stage0_w0)
        if not block["w0_matches_stage0"]:
            reasons.append("freezing_check")
    if actual != expected_sha:
        reasons.append("stage2_sha")
        return block, reasons
    if not _weights_finite(state):
        reasons.append("training_integrity")
        return block, reasons
    evaluated = evaluate_state(state, hidden, world, thr_total, thr_xor, val_mask)
    block.update(evaluated)
    reasons.extend(evaluation_reasons(block))
    return block, reasons


def run_stage2() -> None:
    if not STAGE1_MANIFEST.exists():
        raise SystemExit("stage 1 manifest is missing")
    stage0 = _load_stage0()
    stage1 = json.loads(STAGE1_MANIFEST.read_text(encoding="utf-8"))
    assert_no_scores(stage1)
    if stage1.get("scoring") is not False:
        raise SystemExit("stage 1 manifest is marked as scoring")
    if sha256_file(STAGE0_MANIFEST) != stage1["stage0_manifest_sha256"]:
        raise SystemExit("stage 0 manifest changed after the stage 1 seal")
    assert_code_matches_stage0(stage0)
    stage0_commit = assert_committed(STAGE0_MANIFEST.relative_to(ROOT).as_posix())
    stage1_commit = assert_committed(STAGE1_MANIFEST.relative_to(ROOT).as_posix())
    if stage0_commit == stage1_commit:
        raise SystemExit("stage 0 and stage 1 are not separate commits")
    configure_runtime()
    world = World()
    from graded_reversion_outcomes import pd_cd_components
    from frozen_recurrent_compensation_numpy_eval import pd_q

    pd_e1 = float(pd_cd_components(world.q)["PD"])
    pd_e2 = float(pd_q(world.q))
    thr_total = float(world.afit_threshold["TEST"]["total"])
    thr_xor = float(world.afit_threshold["TEST"]["XOR"])
    val_mask = np.array([is_val_history(history) for history in range(256)], dtype=bool)
    by_run = {(int(row["seed"]), row["arm"]): row for row in stage1["runs"]}
    if len(by_run) != 30:
        raise SystemExit("stage 1 does not contain 30 runs")
    records = []
    for seed in SEEDS:
        for arm in ARMS:
            print("stage2 seed %d %s" % (seed, arm), flush=True)
            stage1_row = by_run[(seed, arm)]
            stage0_arm = stage0["seeds"][str(seed)]["arms"][arm]
            stage0_w0 = stage0["seeds"][str(seed)]["w0_sha256"]
            init_block, init_reasons = _score_checkpoint(
                ROOT / stage0_arm["init_checkpoint_file"],
                stage0_arm["init_checkpoint_sha256"],
                ARM_HIDDEN[arm],
                world,
                thr_total,
                thr_xor,
                val_mask,
                stage0_w0,
                arm != "CAND",
            )
            final_reasons = list(stage1_final_reasons(stage1_row))
            can_eval_final = (
                stage1_row["steps_completed"] == 4000
                and stage1_row["checkpoint_round_trip"]
                and "stage2_sha" not in final_reasons
            )
            final_block = _empty_checkpoint()
            final_block["checkpoint_sha256"] = stage1_row["final_checkpoint_sha256"]
            if can_eval_final:
                final_block, eval_reasons = _score_checkpoint(
                    ROOT / stage1_row["final_checkpoint_file"],
                    stage1_row["final_checkpoint_sha256"],
                    ARM_HIDDEN[arm],
                    world,
                    thr_total,
                    thr_xor,
                    val_mask,
                    stage0_w0,
                    arm != "CAND",
                )
                for reason in eval_reasons:
                    if reason not in final_reasons:
                        final_reasons.append(reason)
            elif stage1_row["steps_completed"] != 4000 and "training_integrity" not in final_reasons and "freezing_check" not in final_reasons:
                final_reasons.append("training_integrity")
            c1, g1 = _prefix_gap(pd_e1, init_block, final_block, "E1")
            c2, g2 = _prefix_gap(pd_e2, init_block, final_block, "E2")
            records.append(
                {
                    "seed": seed,
                    "arm": arm,
                    "init_status": status_from(init_block.get("numeric_class"), init_reasons),
                    "final_status": status_from(final_block.get("numeric_class"), final_reasons),
                    "init_invalid_reasons": init_reasons,
                    "final_invalid_reasons": final_reasons,
                    "final_training_loss": stage1_row["final_loss"],
                    "steps_completed": stage1_row["steps_completed"],
                    "init": init_block,
                    "final": final_block,
                    "C_prefix_E1": c1,
                    "G_prefix_E1": g1,
                    "C_prefix_E2": c2,
                    "G_prefix_E2": g2,
                }
            )
    reconcile_shared_inits(records)
    arms = {}
    for arm in ARMS:
        arm_runs = [record for record in records if record["arm"] == arm]
        counts = arm_counts(arm_runs)
        sentences = statements_for_arm(arm, counts)
        arms[arm] = {
            "counts": counts,
            "statements": sentences,
            "counts_block": format_counts_block(arm, counts),
            "best_median": best_and_median(arm_runs),
            "binding_final": binding_frequencies(arm_runs, "final"),
            "binding_init": binding_frequencies(arm_runs, "init"),
            "ledger": ledger_lines(arm, counts, sentences),
        }
    if arms["CAND"]["counts"]["reproducibility_label"] == REPRO_YES:
        comparator = (
            "R-FIX-vs-CAND comparison: CAND reached TARGET REACHED REPRODUCIBLY. "
            "There is no comparison test between arms."
        )
    else:
        comparator = COMPARATOR_UNRESOLVED
    payload = {
        "study": "Frozen recurrent matrices with learned compensation",
        "stage": 2,
        "protocol_sha256": PROTOCOL_SHA256,
        "code_tree_sha256": stage0["code_tree_sha256"],
        "stage0_commit": stage0_commit,
        "stage1_commit": stage1_commit,
        "reference": {
            "tau": TAU,
            "PD_E1": pd_e1,
            "PD_E2": pd_e2,
            "thr_total": thr_total,
            "thr_xor": thr_xor,
        },
        "comparator": comparator,
        "arms": arms,
        "runs": records,
        "paired": paired_differences(records),
        "deviations_during_stages": "No further deviation was recorded during Stage 1 or Stage 2.",
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
    }
    write_json(STAGE2_JSON, payload)
    STAGE2_MD.write_text(render_report(payload), encoding="utf-8")
    print("stage2 wrote %s" % STAGE2_JSON, flush=True)


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("stage0", "stage1", "stage2"):
        raise SystemExit("usage: python frozen_recurrent_compensation_study.py stage0|stage1|stage2")
    if sys.argv[1] == "stage0":
        run_stage0()
    elif sys.argv[1] == "stage1":
        run_stage1()
    else:
        run_stage2()


if __name__ == "__main__":
    main()
