"""Run the frozen GRU oracle-accessibility audit.

Invoke only as `python -B` after the implementation manifest is sealed.
The process must be pinned to one CPU, with single-threaded BLAS and a 4 GB
address-space limit. See run_frozen.sh.
"""

from __future__ import annotations

import hashlib
import json
import os
import resource
import sys
import time
import traceback
from collections import defaultdict
from itertools import combinations
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import numpy as np

from audit.gru_v1_3.accounting import TRAINED_ARMS, add_label, empty_counts, quota_status
from audit.gru_v1_3.domain import (
    ACBD_FOLDS,
    FORWARD_ATOL,
    PRIMARY_LAMBDA,
    REPLAY_ATOL,
    VAR_MAX,
    conf_features,
    fq_features,
    load_world,
    state_features,
    val_histories,
)
from audit.gru_v1_3.forward import numpy_forward, torch_batched_forward, torch_step_forward, weights_from_checkpoint
from audit.gru_v1_3.metrics import (
    compare_fields,
    component_excess,
    e1_block,
    excess_brier,
    flat_e_block,
    flat_errors,
    probability_excess,
    recorded_outcome_errors,
    recorded_pr10_block,
    recorded_pr7_errors,
    weighted_correlation,
    weighted_mean_sd,
    weighted_quantiles,
)
from audit.gru_v1_3.replay_map import (
    ERROR_KEYS,
    GRID_GB,
    PR10_E_FIELDS,
    PR7_ERROR_ARMS,
    REPLAY_MAP,
    selection_index,
)
from audit.gru_v1_3.report import render
from audit.gru_v1_3.ridge import (
    combine_labels,
    comparison_label,
    dhat_identity_ok,
    ep_reconstruction_ok,
    eval_model_losses,
    fit_design,
    fit_predict_named,
    inner_lambda,
    pool_loss,
    squared_error,
)

REPO = "/workspace"
ROSTER_PATH = Path("/workspace/review/gru_own_error_audit_roster_v1.json")
SPEC_PATH = Path("/workspace/review/gru_own_error_audit_spec_v1_3.md")
MANIFEST_PATH = Path("/workspace/audit/gru_v1_3/IMPLEMENTATION_MANIFEST.json")
OUT_DIR = Path("/workspace/audit/gru_v1_3/results")
OUTSIDE = Path("/tmp/gru_oracle_audit_outside_repo")
DEVIATION_NOTE = (
    "review/DEVIATION_check_script_predecessors_absent.md: the v1.3 consistency "
    "check cannot be re-executed to 112/112 because predecessor artifacts it hashes "
    "are not in this checkout. That item is stopped. No predecessor file was fabricated."
)


class Clock:
    def __init__(self):
        self.t0 = time.perf_counter()
        self.stage = "S0"
        self.stage_t = self.t0
        self.caps = {"S0": 10 * 60, "P": 15 * 60, "D": 20 * 60, "report": 5 * 60}
        self.total = 50 * 60
        self.hit = False
        self.stages = {}

    def elapsed(self) -> float:
        return time.perf_counter() - self.t0

    def begin(self, name: str) -> None:
        now = time.perf_counter()
        if self.stage is not None:
            self.stages[self.stage] = now - self.stage_t
        self.stage = name
        self.stage_t = now
        print("stage %s at wall %.1fs" % (name, self.elapsed()), flush=True)

    def over(self) -> bool:
        if self.elapsed() > self.total or (time.perf_counter() - self.stage_t) > self.caps[self.stage]:
            self.hit = True
            return True
        return False

    def finish(self) -> None:
        self.stages[self.stage] = time.perf_counter() - self.stage_t


def cpu_seconds() -> float:
    own = resource.getrusage(resource.RUSAGE_SELF)
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    return own.ru_utime + own.ru_stime + children.ru_utime + children.ru_stime


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_show(commit: str, path: str) -> bytes:
    return subprocess_check(["git", "-C", REPO, "show", "%s:%s" % (commit, path)])


def subprocess_check(args):
    import subprocess
    return subprocess.check_output(args)


def json_ready(value):
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, float):
        if not np.isfinite(value):
            return None
        return value
    return value


def load_roster():
    payload = json.loads(ROSTER_PATH.read_text(encoding="utf-8"))
    return payload


def copy_checkpoint(row) -> tuple[bytes, str]:
    OUTSIDE.mkdir(parents=True, exist_ok=True)
    raw = git_show(row["commit"], row["path"])
    dest = OUTSIDE / ("%s.json" % row["id"].replace("/", "_"))
    dest.write_bytes(raw)
    copied = dest.read_bytes()
    return copied, hashlib.sha256(copied).hexdigest()


def max_abs(a, b) -> float:
    return float(np.max(np.abs(a - b)))


def forward_all(weights, bits):
    n_state, n_out = numpy_forward(weights, bits)
    s_state, s_out = torch_step_forward(weights, bits)
    b_state, b_out = torch_batched_forward(weights, bits)
    report = {
        "numpy_vs_step_state": max_abs(n_state, s_state),
        "numpy_vs_step_output": max_abs(n_out, s_out),
        "numpy_vs_forward_state": max_abs(n_state, b_state),
        "numpy_vs_forward_output": max_abs(n_out, b_out),
    }
    finite = all(np.isfinite(a).all() for a in (n_state, n_out, s_state, s_out, b_state, b_out))
    agreed = finite and all(value <= FORWARD_ATOL for value in report.values())
    return s_state, s_out, report, finite, agreed


class Records:
    def __init__(self):
        self.seeds = {}
        self.stage2 = None

    def seed_json(self, pr, seed, commit, path):
        key = (pr, seed)
        if key not in self.seeds:
            self.seeds[key] = json.loads(git_show(commit, path))
        return self.seeds[key]

    def pr10(self, commit):
        if self.stage2 is None:
            payload = json.loads(git_show(commit, REPLAY_MAP["pr10"]["record"]))
            self.stage2 = {(row["seed"], row["arm"]): row for row in payload["runs"]}
        return self.stage2


def replay_checkpoint(row, outputs, world, records: Records):
    """Return (ok, label, mismatches, reasons)."""
    pr, arm, role = row["pr"], row["arm"], row["role"]
    if pr == 7:
        seed_json = records.seed_json(7, row["seed"], row["commit"], "recurrent_core_results_v1/seeds/s%d.json" % row["seed"])
        if arm in PR7_ERROR_ARMS:
            recorded = recorded_pr7_errors(seed_json, PR7_ERROR_ARMS[arm])
            got = flat_errors(component_excess(outputs, world.q, world.probability, world.is_test))
            mismatches = compare_fields(got, recorded, ERROR_KEYS, PR7_ERROR_ARMS[arm] + ".")
            return (not mismatches), "source-metric replay", mismatches, []
        index = selection_index(arm)
        if index is None:
            return False, None, [], ["arm not in frozen PR #7 replay map"]
        grid = seed_json["selection"]["grid"][index]
        reasons = []
        mismatches = []
        if float(grid["g"]) != GRID_GB[index][0] or float(grid["b"]) != GRID_GB[index][1]:
            mismatches.append({
                "field": "selection.grid[%d].{g,b}" % index,
                "value": list(GRID_GB[index]),
                "recorded": [grid["g"], grid["b"]],
                "abs_diff": None,
            })
        histories = world.val_histories
        got = probability_excess(outputs[histories], histories, world.q, world.probability)["total"]
        recorded = float(grid["criterion"])
        if not np.isfinite(got) or not np.isfinite(recorded) or abs(got - recorded) > REPLAY_ATOL:
            mismatches.append({
                "field": "selection.grid[%d].criterion" % index,
                "value": None if not np.isfinite(got) else float(got),
                "recorded": None if not np.isfinite(recorded) else recorded,
                "abs_diff": None if not (np.isfinite(got) and np.isfinite(recorded)) else abs(got - recorded),
            })
        return (not mismatches), "source-metric replay", mismatches, reasons
    if pr in (8, 9):
        spec = REPLAY_MAP["pr%d" % pr]
        if arm in spec["unavailable"]:
            return True, spec["unavailable"][arm], [], []
        seed_json = records.seed_json(pr, row["seed"], row["commit"], spec["record"].format(seed=row["seed"]))
        node = seed_json["evaluation"]["intact_outcomes" if arm == "f_trained" else "f_init_outcomes"]
        recorded = recorded_outcome_errors(node)
        got = flat_errors(component_excess(outputs, world.q, world.probability, world.is_test))
        mismatches = compare_fields(got, recorded, ERROR_KEYS, spec["available"][arm] + ".")
        return (not mismatches), "source-metric replay", mismatches, []
    if pr == 10:
        side = "init" if role == "INIT" else "final"
        run = records.pr10(row["commit"])[(row["seed"], arm)]
        mismatches = []
        numpy_state_unused, numpy_out = numpy_forward(weights_from_checkpoint(json.loads(row["_raw"])), world.bits)
        for block_name, preds in (("E1", outputs), ("E2", numpy_out)):
            got = flat_e_block(e1_block(preds, world))
            recorded = recorded_pr10_block(run[side][block_name])
            mismatches.extend(compare_fields(got, recorded, PR10_E_FIELDS, "%s.%s." % (side, block_name)))
        return (not mismatches), "source-metric replay", mismatches, []
    return False, None, [], ["PR not in frozen replay map"]


def s0_one(row, world, records: Records):
    entry = {
        "id": row["id"],
        "pr": row["pr"],
        "seed": row["seed"],
        "arm": row["arm"],
        "role": row["role"],
        "status": "ok",
        "reasons": [],
        "mismatches": [],
        "replay_label": None,
        "forward": None,
        "R_exc": None,
        "f": None,
        "state": None,
        "e": None,
    }
    try:
        raw, digest = copy_checkpoint(row)
        row = dict(row)
        row["_raw"] = raw
        if digest != row["sha256"]:
            entry["status"] = "fail"
            entry["reasons"].append("sha256 mismatch")
            return entry
        payload = json.loads(raw)
        weights = weights_from_checkpoint(payload)
        state, outputs, forward, finite, agreed = forward_all(weights, world.bits)
        entry["forward"] = forward
        if not finite:
            entry["status"] = "fail"
            entry["reasons"].append("non-finite state or output")
            return entry
        if not agreed:
            entry["status"] = "fail"
            entry["reasons"].append("numpy vs torch max-abs > 1e-10")
            return entry
        ok_ep, worst = ep_reconstruction_ok(outputs, world.q)
        if not ok_ep:
            entry["status"] = "fail"
            entry["reasons"].append("e_P reconstruction tolerance failed (worst excess %s)" % worst)
            return entry
        entry["R_exc"] = excess_brier(outputs, world.q, world.probability)
        if not np.isfinite(entry["R_exc"]):
            entry["status"] = "fail"
            entry["reasons"].append("non-finite R_exc")
            return entry
        ok, label, mismatches, reasons = replay_checkpoint(row, outputs, world, records)
        entry["replay_label"] = label
        entry["mismatches"] = mismatches
        entry["reasons"].extend(reasons)
        if not ok:
            entry["status"] = "fail"
            entry["reasons"].append("source-metric replay mismatch")
            return entry
        entry["f"] = outputs
        entry["state"] = state
        entry["e"] = np.sum((outputs - world.q) ** 2, axis=1)
    except Exception as exc:
        entry["status"] = "fail"
        entry["reasons"].append("%s: %s" % (type(exc).__name__, exc))
        entry["traceback"] = traceback.format_exc()
    return entry


def _finite_numbers(value) -> bool:
    if isinstance(value, dict):
        return all(_finite_numbers(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return all(_finite_numbers(v) for v in value)
    if isinstance(value, str) or value is None:
        return True
    if isinstance(value, (int, np.integer)):
        return True
    if isinstance(value, (float, np.floating)):
        return bool(np.isfinite(value))
    return True


def _public_rows(rows):
    public = []
    for row in rows:
        public.append({
            "fold": row["fold"],
            "loss": row["loss"],
            "numerator": row["numerator"],
            "rank": row["rank"],
            "excluded": row["excluded"],
        })
    return public


def build_comparison(base_rows, full_rows, world, issue_label: bool):
    total = world.total_mass
    var_q = world.Var_w_q
    l_base = pool_loss(base_rows, total, 3)
    l_full = pool_loss(full_rows, total, 3)
    delta = l_base - l_full
    foldwise = []
    for base, full in zip(base_rows, full_rows):
        foldwise.append({
            "fold": base["fold"],
            "L_base": base["loss"],
            "L_full": full["loss"],
            "delta": base["loss"] - full["loss"],
            "rank_base": base["rank"],
            "rank_full": full["rank"],
            "excluded_base": base["excluded"],
            "excluded_full": full["excluded"],
        })
    ac_base = [row for row in base_rows if row["fold"] in ACBD_FOLDS]
    ac_full = [row for row in full_rows if row["fold"] in ACBD_FOLDS]
    ac_l_base = pool_loss(ac_base, total, 1)
    ac_l_full = pool_loss(ac_full, total, 1)
    ac_delta = ac_l_base - ac_l_full
    block = {
        "L_base": l_base,
        "L_full": l_full,
        "delta": delta,
        "r2": delta / var_q,
        "foldwise": foldwise,
        "acbd": {
            "L_base": ac_l_base,
            "L_full": ac_l_full,
            "delta": ac_delta,
            "r2": ac_delta / var_q,
        },
        "label": comparison_label(delta, world.floor) if issue_label else None,
    }
    return block


def feature_sets(entry, world):
    conf, conf_names = conf_features(entry["f"])
    state, state_names = state_features(entry["state"])
    plus, plus_names = world.bin_plus, world.bin_plus_names
    return {
        "C1": (conf, conf_names, np.concatenate([conf, state], axis=1), conf_names + state_names),
        "C2": (
            np.concatenate([conf, plus], axis=1),
            conf_names + plus_names,
            np.concatenate([conf, plus, state], axis=1),
            conf_names + plus_names + state_names,
        ),
    }


def primary_one(entry, world, issue_label: bool):
    sets = feature_sets(entry, world)
    q = world.q
    w = world.probability
    worst = -1.0
    failed = False
    blocks = {}
    for name, (x_base, n_base, x_full, n_full) in sets.items():
        if x_base.shape[1] not in (6, 42) or x_full.shape[1] not in (14, 50):
            raise RuntimeError("feature count %s %s %s" % (name, x_base.shape, x_full.shape))
        base_rows = eval_model_losses(x_base, q, w, world.folds, PRIMARY_LAMBDA, n_base)
        full_rows = eval_model_losses(x_full, q, w, world.folds, PRIMARY_LAMBDA, n_full)
        for rows in (base_rows, full_rows):
            for row in rows:
                if not np.isfinite(row["predictions"]).all() or not np.isfinite(row["loss"]):
                    failed = True
                ok, viol = dhat_identity_ok(entry["f"], q, row["predictions"])
                worst = max(worst, viol)
                if not ok:
                    failed = True
        blocks[name] = build_comparison(base_rows, full_rows, world, issue_label)
        if not _finite_numbers(blocks[name]):
            failed = True
    entry["dhat_worst_excess"] = worst
    entry["C1"] = blocks["C1"]
    entry["C2"] = blocks["C2"]
    if failed:
        entry["status"] = "fail"
        entry["reasons"].append("non-finite primary quantity or signed-deviation identity failure")
        entry["C1"]["label"] = None
        entry["C2"]["label"] = None
        return
    if issue_label:
        entry["decision"] = combine_labels(blocks["C1"]["label"], blocks["C2"]["label"])
    else:
        entry["decision"] = None


def r_exc(entry, world):
    value = excess_brier(entry["f"], world.q, world.probability)
    entry["R_exc"] = value
    if not np.isfinite(value):
        entry["status"] = "fail"
        entry["reasons"].append("non-finite R_exc")


def input_only(world):
    rows = eval_model_losses(
        world.bin_plus, world.q, world.probability, world.folds, PRIMARY_LAMBDA, world.bin_plus_names
    )
    return {
        "status": "done",
        "lambda": PRIMARY_LAMBDA,
        "pooled": pool_loss(rows, world.total_mass, 3),
        "per_fold": {row["fold"]: row["loss"] for row in rows},
        "rank": _public_rows(rows),
        "note": (
            "Target-decoding calculation of B_in+ alone. Not described as outcome-blind "
            "merely because it needs no checkpoint. Not a gate."
        ),
    }


def uniform_one(entry, world):
    sets = feature_sets(entry, world)
    w = np.full(256, 1.0 / 256.0)
    q = world.q
    out = {}
    for name, (x_base, n_base, x_full, n_full) in sets.items():
        base_rows = eval_model_losses(x_base, q, w, world.folds, PRIMARY_LAMBDA, n_base)
        full_rows = eval_model_losses(x_full, q, w, world.folds, PRIMARY_LAMBDA, n_full)
        l_base = pool_loss(base_rows, 1.0, 3)
        l_full = pool_loss(full_rows, 1.0, 3)
        delta = l_base - l_full
        out[name] = {
            "L_base": l_base,
            "L_full": l_full,
            "delta": delta,
            "r2": delta / world.var_q_uniform,
            "r2_denominator": "uniform-weight Var(q)",
            "floor_label": None,
            "foldwise": [
                {"fold": b["fold"], "L_base": b["loss"], "L_full": f["loss"], "delta": b["loss"] - f["loss"]}
                for b, f in zip(base_rows, full_rows)
            ],
        }
    return out


def inner_one(entry, world):
    sets = feature_sets(entry, world)
    q = world.q
    w = world.probability
    out = {}
    for name, (x_base, n_base, x_full, n_full) in sets.items():
        chosen = []
        base_rows = []
        full_rows = []
        for fold in world.folds:
            lam_b, _ = inner_lambda(x_base, q, w, fold["fit"], fold["orbits"], n_base)
            lam_f, _ = inner_lambda(x_full, q, w, fold["fit"], fold["orbits"], n_full)
            pred_b, model_b = fit_predict_named(x_base, q, w, fold["fit"], lam_b, n_base)
            pred_f, model_f = fit_predict_named(x_full, q, w, fold["fit"], lam_f, n_full)
            err_b = squared_error(pred_b, q)
            err_f = squared_error(pred_f, q)
            from audit.gru_v1_3.ridge import weighted_loss
            num_b, loss_b = weighted_loss(err_b, w, fold["eval"])
            num_f, loss_f = weighted_loss(err_f, w, fold["eval"])
            base_rows.append({"fold": fold["name"], "loss": loss_b, "numerator": num_b, "lambda": lam_b,
                              "rank": model_b.rank_info, "excluded": model_b.excluded})
            full_rows.append({"fold": fold["name"], "loss": loss_f, "numerator": num_f, "lambda": lam_f,
                              "rank": model_f.rank_info, "excluded": model_f.excluded})
            chosen.append({"fold": fold["name"], "lambda_base": lam_b, "lambda_full": lam_f})
        block = build_comparison(base_rows, full_rows, world, False)
        block["label"] = None
        block["floor_label"] = None
        block["selected_lambda"] = chosen
        primary = entry[name]
        block["difference_from_fixed_lambda"] = {
            "L_base": block["L_base"] - primary["L_base"],
            "L_full": block["L_full"] - primary["L_full"],
            "delta": block["delta"] - primary["delta"],
            "r2": block["r2"] - primary["r2"],
        }
        out[name] = block
    return out


def heldout_from_designs(designs, x, y, w, folds, total_mass):
    numer = 0.0
    for fold, design in zip(folds, designs):
        pred = design.predict(x, np.asarray(y)[fold["fit"]], PRIMARY_LAMBDA)
        err = squared_error(pred, y)
        weight = w[fold["eval"]]
        numer += float(weight @ err[fold["eval"]])
    return numer / (3.0 * total_mass)


def r2_of(loss, var):
    if var <= VAR_MAX:
        return "UNDEFINED"
    return 1.0 - loss / var


def t_pair(source_p, source_q, loss_pp, loss_qp, loss_qq, loss_pq, var_p, var_q):
    r_pp = r2_of(loss_pp, var_p)
    r_qp = r2_of(loss_qp, var_p)
    r_qq = r2_of(loss_qq, var_q)
    r_pq = r2_of(loss_pq, var_q)
    undefined = var_p <= VAR_MAX or var_q <= VAR_MAX
    if undefined or "UNDEFINED" in (r_pp, r_qp, r_qq, r_pq):
        beta_p = "UNDEFINED" if var_p <= VAR_MAX else (None if "UNDEFINED" in (r_pp, r_qp) else r_pp - r_qp)
        beta_q = "UNDEFINED" if var_q <= VAR_MAX else (None if "UNDEFINED" in (r_qq, r_pq) else r_qq - r_pq)
        if var_p <= VAR_MAX:
            beta_p = "UNDEFINED"
        elif "UNDEFINED" not in (r_pp, r_qp):
            beta_p = r_pp - r_qp
        else:
            beta_p = "UNDEFINED"
        if var_q <= VAR_MAX:
            beta_q = "UNDEFINED"
        elif "UNDEFINED" not in (r_qq, r_pq):
            beta_q = r_qq - r_pq
        else:
            beta_q = "UNDEFINED"
        return {
            "beta_P": beta_p,
            "beta_Q": beta_q,
            "T": "UNDEFINED",
            "R_Sp_ep": r_pp,
            "R_Sq_ep": r_qp,
            "R_Sq_eq": r_qq,
            "R_Sp_eq": r_pq,
            "status": "UNDEFINED",
        }
    beta_p = r_pp - r_qp
    beta_q = r_qq - r_pq
    return {
        "beta_P": beta_p,
        "beta_Q": beta_q,
        "T": beta_p + beta_q,
        "R_Sp_ep": r_pp,
        "R_Sq_ep": r_qp,
        "R_Sq_eq": r_qq,
        "R_Sp_eq": r_pq,
        "status": "ok",
    }


def features_for(entry, kind, q):
    if kind == "STATE":
        return state_features(entry["state"])
    if kind == "CONF":
        return conf_features(entry["f"])
    if kind == "FQ":
        return fq_features(entry["f"], q)
    raise ValueError(kind)


def declare_pairs(trained_rows):
    by_seed = defaultdict(list)
    by_arm = defaultdict(list)
    for row in trained_rows:
        by_seed[(row["pr"], row["seed"])].append(row)
        by_arm[(row["pr"], row["arm"])].append(row)
    pairs = []
    for group in by_seed.values():
        ordered = sorted(group, key=lambda r: r["arm"])
        for left, right in combinations(ordered, 2):
            pairs.append({"roster": "within-seed-cross-arm", "p": left["id"], "q": right["id"]})
    for group in by_arm.values():
        ordered = sorted(group, key=lambda r: r["seed"])
        for left, right in combinations(ordered, 2):
            pairs.append({"roster": "same-arm-cross-seed", "p": left["id"], "q": right["id"]})
    return pairs


def public_entry(entry):
    kept = {
        "id": entry["id"],
        "pr": entry["pr"],
        "seed": entry["seed"],
        "arm": entry["arm"],
        "role": entry["role"],
        "status": entry["status"],
        "reasons": entry.get("reasons", []),
        "mismatches": entry.get("mismatches", []),
        "replay_label": entry.get("replay_label"),
        "forward": entry.get("forward"),
        "R_exc": entry.get("R_exc"),
        "decision": entry.get("decision"),
        "dhat_worst_excess": entry.get("dhat_worst_excess"),
    }
    for name in ("C1", "C2"):
        if name in entry:
            kept[name] = entry[name]
    if entry.get("traceback"):
        kept["traceback"] = entry["traceback"]
    return kept


def mark_seed(entries, status, reason):
    for entry in entries:
        entry["status"] = status
        if reason and reason not in entry["reasons"]:
            entry["reasons"].append(reason)
        entry["decision"] = "UNRESOLVED" if status == "UNRESOLVED" else None
        for name in ("C1", "C2"):
            if name in entry and isinstance(entry[name], dict):
                entry[name]["label"] = None


def run():
    if not sys.dont_write_bytecode:
        raise SystemExit("refusing to run without python -B")
    if not MANIFEST_PATH.is_file():
        raise SystemExit("implementation manifest is missing")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest["replay_map"] != json_ready(REPLAY_MAP):
        raise SystemExit("manifest replay map does not match the frozen code map")
    clock = Clock()
    world = load_world()
    world.val_histories = val_histories()
    roster = load_roster()
    rows = roster["roster"]
    by_seed = defaultdict(list)
    for row in rows:
        by_seed[(row["pr"], row["seed"])].append(row)
    seed_keys = sorted(by_seed)
    records = Records()
    done = {}
    print("S0 seeds %d checkpoints %d" % (len(seed_keys), len(rows)), flush=True)
    for key in seed_keys:
        if clock.over():
            for row in by_seed[key]:
                done[row["id"]] = {
                    "id": row["id"], "pr": row["pr"], "seed": row["seed"], "arm": row["arm"],
                    "role": row["role"], "status": "INCOMPLETE", "reasons": ["S0 cap"],
                    "decision": None, "R_exc": None,
                }
            continue
        entries = []
        aborted = False
        for row in by_seed[key]:
            if clock.over():
                aborted = True
                break
            entries.append(s0_one(row, world, records))
            print("S0 %s %s" % (row["id"], entries[-1]["status"]), flush=True)
        if aborted or len(entries) != len(by_seed[key]):
            for row in by_seed[key]:
                done[row["id"]] = {
                    "id": row["id"], "pr": row["pr"], "seed": row["seed"], "arm": row["arm"],
                    "role": row["role"], "status": "INCOMPLETE", "reasons": ["S0 cap"],
                    "decision": None, "R_exc": None,
                }
            continue
        if any(entry["status"] != "ok" for entry in entries):
            for entry in entries:
                if entry.get("f") is not None:
                    entry["R_exc"] = excess_brier(entry["f"], world.q, world.probability)
            mark_seed(entries, "UNRESOLVED", "integrity unit failed")
            for entry in entries:
                entry["f"] = None
                entry["state"] = None
                entry["e"] = None
        for entry in entries:
            done[entry["id"]] = entry

    clock.begin("P")
    if not clock.over():
        try:
            input_block = input_only(world)
            print("input-only pooled %s" % input_block["pooled"], flush=True)
        except Exception as exc:
            input_block = {"status": "INCOMPLETE", "reason": "%s: %s" % (type(exc).__name__, exc)}
    else:
        input_block = {"status": "INCOMPLETE"}
    for key in seed_keys:
        entries = [done[row["id"]] for row in by_seed[key]]
        if any(entry["status"] != "ok" for entry in entries):
            continue
        if clock.over():
            mark_seed(entries, "INCOMPLETE", "P cap")
            for entry in entries:
                entry["status"] = "INCOMPLETE"
                entry["decision"] = None
            continue
        failed = False
        for entry in entries:
            if clock.over():
                failed = True
                break
            r_exc(entry, world)
            if entry["status"] != "ok":
                failed = True
                break
            primary_one(entry, world, issue_label=(entry["role"] == "TRAINED"))
            if entry["status"] != "ok":
                failed = True
                break
            print("P %s decision=%s" % (entry["id"], entry.get("decision")), flush=True)
        if failed or any(entry["status"] != "ok" for entry in entries):
            if any(entry["status"] == "fail" for entry in entries):
                mark_seed(entries, "UNRESOLVED", "integrity unit failed")
            else:
                for entry in entries:
                    entry["status"] = "INCOMPLETE"
                    entry["decision"] = None
                    entry["reasons"].append("P cap")

    clock.begin("D")
    trained_ok = [entry for entry in done.values() if entry["role"] == "TRAINED" and entry["status"] == "ok" and entry.get("f") is not None]
    inner_rows = []
    uniform_rows = []
    inner_status = "done"
    uniform_status = "done"
    for entry in trained_ok:
        if clock.over():
            inner_status = "INCOMPLETE"
            break
        try:
            inner_rows.append({"id": entry["id"], "pr": entry["pr"], "seed": entry["seed"], "arm": entry["arm"], **inner_one(entry, world)})
        except Exception as exc:
            inner_status = "INCOMPLETE"
            inner_rows.append({"id": entry["id"], "status": "INCOMPLETE", "reason": "%s: %s" % (type(exc).__name__, exc)})
            print("D inner %s FAILED %s" % (entry["id"], exc), flush=True)
            continue
        print("D inner %s" % entry["id"], flush=True)
    for entry in trained_ok:
        if clock.over():
            uniform_status = "INCOMPLETE"
            break
        try:
            uniform_rows.append({"id": entry["id"], "pr": entry["pr"], "seed": entry["seed"], "arm": entry["arm"], **uniform_one(entry, world)})
        except Exception as exc:
            uniform_status = "INCOMPLETE"
            uniform_rows.append({"id": entry["id"], "status": "INCOMPLETE", "reason": "%s: %s" % (type(exc).__name__, exc)})
            print("D uniform %s FAILED %s" % (entry["id"], exc), flush=True)
            continue

    t_status = "done"
    corr_status = "done"
    var_status = "done"
    t_rows = []
    corr_rows = []
    variation_rows = []
    trained_rows = [row for row in rows if row["role"] == "TRAINED"]
    pairs = declare_pairs(trained_rows)
    if len(pairs) != 2035:
        raise RuntimeError("pair roster is %d, expected 2035" % len(pairs))
    by_id = {entry["id"]: entry for entry in done.values()}
    if clock.over() or uniform_status == "INCOMPLETE" and clock.hit:
        t_status = "INCOMPLETE"
    # Compute T only while the descriptive cap allows it. A prior incomplete
    # uniform stage does not by itself skip T if time remains.
    if clock.over():
        t_status = "INCOMPLETE"
        corr_status = "INCOMPLETE"
        var_status = "INCOMPLETE"
    else:
        losses = {}
        variances = {}
        needed = defaultdict(set)
        eligible = []
        for pair in pairs:
            left = by_id[pair["p"]]
            right = by_id[pair["q"]]
            if left["status"] != "ok" or right["status"] != "ok" or left.get("e") is None or right.get("e") is None:
                continue
            eligible.append(pair)
            needed[pair["p"]].update((pair["p"], pair["q"]))
            needed[pair["q"]].update((pair["p"], pair["q"]))
        w = world.probability
        for source_id, targets in needed.items():
            if clock.over():
                t_status = "INCOMPLETE"
                break
            source = by_id[source_id]
            for kind in ("STATE", "CONF", "FQ"):
                x, names = features_for(source, kind, world.q)
                designs = [fit_design(x, w, fold["fit"], names) for fold in world.folds]
                for target_id in targets:
                    y = by_id[target_id]["e"]
                    losses[(source_id, target_id, kind)] = heldout_from_designs(designs, x, y, w, world.folds, world.total_mass)
            print("D T source %s" % source_id, flush=True)
        for entry in trained_ok:
            variances[entry["id"]] = weighted_mean_sd(w, entry["e"])[2]
        for pair in pairs:
                left = by_id[pair["p"]]
                right = by_id[pair["q"]]
                base = {
                    "roster": pair["roster"],
                    "P": pair["p"],
                    "Q": pair["q"],
                    "pr_P": left["pr"],
                    "seed_P": left["seed"],
                    "arm_P": left["arm"],
                    "pr_Q": right["pr"],
                    "seed_Q": right["seed"],
                    "arm_Q": right["arm"],
                }
                if left["status"] != "ok" or right["status"] != "ok":
                    status = "UNRESOLVED" if "UNRESOLVED" in (left["status"], right["status"]) else left["status"]
                    if left["status"] == "INCOMPLETE" or right["status"] == "INCOMPLETE":
                        status = "INCOMPLETE"
                    for kind in ("STATE", "CONF", "FQ"):
                        t_rows.append({**base, "feature": kind, "status": status})
                    continue
                if any((pair["p"], pair["q"], kind) not in losses for kind in ("STATE", "CONF", "FQ")):
                    t_status = "INCOMPLETE"
                    for kind in ("STATE", "CONF", "FQ"):
                        t_rows.append({**base, "feature": kind, "status": "INCOMPLETE"})
                    continue
                var_p = variances[pair["p"]]
                var_q = variances[pair["q"]]
                for kind in ("STATE", "CONF", "FQ"):
                    rec = t_pair(
                        pair["p"], pair["q"],
                        losses[(pair["p"], pair["p"], kind)],
                        losses[(pair["q"], pair["p"], kind)],
                        losses[(pair["q"], pair["q"], kind)],
                        losses[(pair["p"], pair["q"], kind)],
                        var_p, var_q,
                    )
                    rec.update({
                        "loss_Sp_ep": losses[(pair["p"], pair["p"], kind)],
                        "loss_Sq_ep": losses[(pair["q"], pair["p"], kind)],
                        "loss_Sq_eq": losses[(pair["q"], pair["q"], kind)],
                        "loss_Sp_eq": losses[(pair["p"], pair["q"], kind)],
                        "feature": kind,
                    })
                    rec.update(base)
                    t_rows.append(rec)
        if clock.over():
            corr_status = "INCOMPLETE"
            var_status = "INCOMPLETE"
        else:
            for pair in pairs:
                left = by_id[pair["p"]]
                right = by_id[pair["q"]]
                if left["status"] != "ok" or right["status"] != "ok" or left.get("e") is None:
                    status = "INCOMPLETE" if "INCOMPLETE" in (left["status"], right["status"]) else "UNRESOLVED"
                    corr_rows.append({"roster": pair["roster"], "P": pair["p"], "Q": pair["q"], "status": status})
                    continue
                corr_rows.append({
                    "roster": pair["roster"],
                    "P": pair["p"],
                    "Q": pair["q"],
                    "status": "ok",
                    "corr_w": weighted_correlation(w, left["e"], right["e"]),
                })
            for entry in done.values():
                if entry["status"] == "ok" and entry.get("e") is not None:
                    mean, sd, var = weighted_mean_sd(w, entry["e"])
                    variation_rows.append({
                        "id": entry["id"],
                        "status": "ok",
                        "mean": mean,
                        "sd": sd,
                        "var": var,
                        "quantiles": weighted_quantiles(w, entry["e"]),
                        "min": float(np.min(entry["e"])),
                        "max": float(np.max(entry["e"])),
                        "quantile_definition": "smallest value whose cumulative P(h) weight reaches the probability",
                    })
                else:
                    kind = "INCOMPLETE" if entry["status"] == "INCOMPLETE" else "UNRESOLVED"
                    variation_rows.append({"id": entry["id"], "status": kind})
                    if kind == "INCOMPLETE":
                        var_status = "INCOMPLETE"
            if var_status != "INCOMPLETE":
                var_status = "done"

    clock.begin("report")
    units = []
    for pr, arms in TRAINED_ARMS.items():
        seeds = sorted({row["seed"] for row in rows if row["pr"] == pr})
        verified_seeds = 0
        for seed in seeds:
            members = [done[row["id"]] for row in by_seed[(pr, seed)]]
            if members and all(member["status"] == "ok" for member in members):
                verified_seeds += 1
        statement = (
            "UNRESOLVED as a whole"
            if verified_seeds < 8
            else "reported with its (PR, arm) units; a PR-level median is not a claim about every arm"
        )
        for arm in arms:
            counts = empty_counts()
            for seed in seeds:
                entry = done["%s" % next(row["id"] for row in by_seed[(pr, seed)] if row["arm"] == arm and row["role"] == "TRAINED")]
                if entry["status"] == "INCOMPLETE":
                    add_label(counts, "INCOMPLETE")
                elif entry["status"] != "ok":
                    add_label(counts, "UNRESOLVED")
                else:
                    add_label(counts, entry["decision"])
            if sum(counts.values()) != 10:
                raise RuntimeError("counts for PR %s %s are %s" % (pr, arm, counts))
            units.append({"pr": pr, "arm": arm, "counts": counts, "quota": quota_status(**counts)})
        # pr_level stored below
    pr_level = []
    for pr in (7, 8, 9, 10):
        seeds = sorted({row["seed"] for row in rows if row["pr"] == pr})
        verified_seeds = 0
        for seed in seeds:
            members = [done[row["id"]] for row in by_seed[(pr, seed)]]
            if members and all(member["status"] == "ok" for member in members):
                verified_seeds += 1
        pr_level.append({
            "pr": pr,
            "verified_seeds": verified_seeds,
            "statement": "UNRESOLVED as a whole" if verified_seeds < 8 else "not unresolved as a whole",
        })
    seed_medians = []
    for key in seed_keys:
        members = [done[row["id"]] for row in by_seed[key] if row["role"] == "TRAINED"]
        if not members or any(member["status"] != "ok" or "C1" not in member for member in members):
            status = "INCOMPLETE" if any(member["status"] == "INCOMPLETE" for member in members) else "UNRESOLVED"
            seed_medians.append({"pr": key[0], "seed": key[1], "status": status})
            continue
        seed_medians.append({
            "pr": key[0],
            "seed": key[1],
            "status": "descriptive",
            "median_C1": float(np.median([member["C1"]["delta"] for member in members])),
            "median_C2": float(np.median([member["C2"]["delta"] for member in members])),
        })
    dup_notes = []
    for seed in sorted({row["seed"] for row in rows if row["pr"] == 10 and row["role"] == "INIT"}):
        cand = next(row for row in rows if row["pr"] == 10 and row["seed"] == seed and row["role"] == "INIT" and row["arm"] == "CAND")
        other = next(row for row in rows if row["pr"] == 10 and row["seed"] == seed and row["role"] == "INIT" and row["arm"] == "R-FIX-32")
        dup_notes.append({"seed": seed, "identical": cand["sha256"] == other["sha256"]})
    trained_public = [public_entry(done[row["id"]]) for row in rows if row["role"] == "TRAINED"]
    init_public = [public_entry(done[row["id"]]) for row in rows if row["role"] == "INIT"]
    unfinished = []
    if input_block.get("status") == "INCOMPLETE":
        unfinished.append("input-only B_in+ → q")
    if any(entry["status"] == "INCOMPLETE" for entry in done.values()):
        unfinished.append("checkpoints")
    if inner_status == "INCOMPLETE":
        unfinished.append("inner-lambda sensitivity")
    if uniform_status == "INCOMPLETE":
        unfinished.append("uniform-weight sensitivity")
    if t_status == "INCOMPLETE":
        unfinished.append("T")
    if corr_status == "INCOMPLETE":
        unfinished.append("correlations")
    if var_status == "INCOMPLETE":
        unfinished.append("e_P variation")
    clock.finish()
    audit_complete = not clock.hit and not unfinished
    payload = {
        "spec_sha256": sha256_file(SPEC_PATH),
        "roster_sha256": sha256_file(ROSTER_PATH),
        "manifest_sha256": sha256_file(MANIFEST_PATH),
        "bits_sha256": world.bits_sha256,
        "constants": {
            "R_oracle": world.R_oracle,
            "Var_w_q": world.Var_w_q,
            "floor": world.floor,
            "r2_floor": world.r2_floor,
            "var_q_uniform": world.var_q_uniform,
            "primary_lambda": PRIMARY_LAMBDA,
            "var_max": VAR_MAX,
        },
        "input_only": input_block,
        "units": units,
        "pr_level": pr_level,
        "checkpoints": trained_public,
        "init_checkpoints": init_public,
        "init_duplicate_notes": dup_notes,
        "seed_medians": seed_medians,
        "inner_status": inner_status,
        "inner": inner_rows,
        "uniform_status": uniform_status,
        "uniform": uniform_rows,
        "T_status": t_status,
        "T": t_rows,
        "correlation_status": corr_status,
        "correlations": corr_rows,
        "variation_status": var_status,
        "variation": variation_rows,
        "runtime": {
            "wall_seconds": clock.elapsed(),
            "cpu_seconds": cpu_seconds(),
            "stages": clock.stages,
            "cap_reached": clock.hit,
        },
        "audit_complete": audit_complete,
        "unfinished": unfinished,
        "deviations": [DEVIATION_NOTE],
        "n_units": len(units),
        "pair_count": len(pairs),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ready = json_ready(payload)
    (OUT_DIR / "results.json").write_text(json.dumps(ready, indent=1) + "\n", encoding="utf-8")
    (OUT_DIR / "REPORT.md").write_text(render(ready), encoding="utf-8")
    summary = {
        "audit_complete": ready["audit_complete"],
        "wall_seconds": ready["runtime"]["wall_seconds"],
        "cpu_seconds": ready["runtime"]["cpu_seconds"],
        "units": [
            {"pr": u["pr"], "arm": u["arm"], **u["counts"], "quota": u["quota"]}
            for u in ready["units"]
        ],
        "unfinished": ready["unfinished"],
        "input_only_pooled": ready["input_only"].get("pooled"),
        "manifest_sha256": ready["manifest_sha256"],
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print("wrote report complete=%s wall=%.1f cpu=%.1f" % (audit_complete, clock.elapsed(), cpu_seconds()), flush=True)


if __name__ == "__main__":
    run()
