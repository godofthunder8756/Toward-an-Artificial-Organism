"""G13 final analysis — the full endpoint set + frozen statistical plan.

UN-HASHED analysis layer on top of the frozen finals run
(``phase3_results_finals_v1``, produced untouched by ``run_engineering.py``).
It computes the endpoints the task's report list requires but the frozen
runner's rows do not carry, and applies the frozen statistical plan
(``ACI_PHASE3_PROTOCOL_v1.md`` §10): the exact sign-flip test on paired
per-seed differences, effect sizes with exact binomial CIs, per-gate
alpha = 0.01, floor 2/2^12 = 0.00049. Equivalence / byte-identity gates are
reported per-seed, never as a "p > 0.05 therefore equal" inference.

Training is deterministic (``seed_all``), so this re-train reproduces the
frozen rows exactly; the script cross-checks its frozen-format rows against
``phase3_results_finals_v1/rows.jsonl`` and records any mismatch.

Usage (CPU-only, from repo root):
    CUDA_VISIBLE_DEVICES= OPENBLAS_NUM_THREADS=1 PYTHONPATH=. \\
        .venv-bridge/bin/python -B phase3/analyze_finals.py \\
        --frozen phase3_results_finals_v1 --out phase3_finals_analysis_v1
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

from phase3.config import Phase3Config, parameter_counts
from phase3.runner import ARM_NAMES, build_arm, evaluate_arm
from phase3.arms import compute_thresholds, apply_specialists
from phase3.task import sample_episodes
from phase3.specialists import (
    A, B, COMMIT_A, COMMIT_B, POSTPONE, PRESERVE, RELEASE,
    s_pol, s_plan, s_reg, theta_value,
)
from phase3.interventions import (
    scramble, w_cut_outputs, wrong_w, stale_w, private_copy_divergence,
    single_write_reach,
)
from phase3.leakage import decode_accuracy

FINAL_SEEDS = [100 + i for i in range(12)]
N_EP = 1024
WSTAR_SWEEP = [-3.0, -0.4, 0.0, 0.4, 3.0]
CKPT_KEYS = ["candidate", "r1", "r2", "r3"]  # learned arms only
FROZEN_KEYS = ("probe_acc", "clean_acc", "incoherence_rate", "pi_cut_probe_acc",
               "s_conf_log_loss", "s_bias_accuracy", "s_conf_ceiling")


def predicted_triple(w_star: float, cfg: Phase3Config, thr: dict) -> np.ndarray:
    a, b = thr["a"], thr["b"]
    theta = theta_value(cfg.specialist, np.array([cfg.persistence.e0]),
                        np.array([1]), a, cfg.persistence.e_crit)
    return np.array([s_pol(np.array([w_star]))[0],
                     s_plan(np.array([w_star]), a, b)[0],
                     s_reg(np.array([w_star]), theta)[0]])


def analyze_seed(cfg: Phase3Config, seed: int, ckpt_dir: str) -> dict:
    """Train all arms for one seed and compute every endpoint (frozen-format
    rows for cross-check + the extra set + the interventions + F1 decode)."""
    z, x = sample_episodes(cfg.task, N_EP, seed)
    thr = compute_thresholds(cfg)
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    regime = np.zeros(cfg.task.horizon, dtype=np.int64)
    regime[probe_entry:] = 1

    arms = {name: build_arm(cfg, name, seed) for name in ARM_NAMES}
    for name in CKPT_KEYS:
        from phase3.runner import save_checkpoint
        save_checkpoint(arms[name], os.path.join(ckpt_dir, f"arm_{name}_seed_{seed}.pt"))

    rows = []          # frozen-format rows (cross-check against the frozen run)
    extras = {}
    for name in ARM_NAMES:
        arm = arms[name]
        rows.append(evaluate_arm(cfg, arm, x, z, thr) | {"seed": seed})
        tr = arm.run(x)
        ex = {}
        if arm.has_w:
            w = np.asarray(tr["w"])
            out = apply_specialists(w, cfg, thr, regime)
            spol, splan, sreg = out["spol"], out["splan"], out["sreg"]
            ex["spol_probe_acc"] = float(np.mean(spol[..., -1] == z))
            spf = splan[..., -1]
            committed = spf != POSTPONE
            ex["splan_commit_rate"] = float(np.mean(committed))
            correct = ((spf == COMMIT_A) & (z == A)) | ((spf == COMMIT_B) & (z == B))
            ex["splan_commit_acc"] = (float(np.mean(correct[committed]))
                                      if committed.any() else None)
            ex["sreg_preserve_rate"] = float(np.mean(sreg[..., -1] == PRESERVE))
            refresh = np.asarray(tr["refresh"])
            ex["n_refresh_targets"] = (3 if name == "r1" else
                                       1 if name == "candidate" else 0)
            ex["total_refresh_events"] = float(refresh.sum())
            ex["mean_refresh_per_ep"] = float(refresh.sum() / refresh.shape[0])
            ex["final_energy_mean"] = float(np.asarray(tr["energy"])[..., -1].mean())
        else:
            ex["spol_probe_acc"] = None
            ex["splan_commit_rate"] = None
            ex["splan_commit_acc"] = None
            ex["sreg_preserve_rate"] = None
            ex["n_refresh_targets"] = 0
            ex["total_refresh_events"] = 0.0
            ex["mean_refresh_per_ep"] = 0.0
            ex["final_energy_mean"] = None
        extras[name] = ex

    # ---- interventions (candidate is the load-bearing arm) ---------------- #
    w_cand = np.asarray(arms["candidate"].run(x)["w"])
    intact = apply_specialists(w_cand, cfg, thr, regime)

    i1 = {}
    for w_star in WSTAR_SWEEP:
        o = apply_specialists(scramble(w_cand, w_star, probe_entry), cfg, thr, regime)
        final = np.array([o["spol"][0, -1], o["splan"][0, -1], o["sreg"][0, -1]])
        pred = predicted_triple(w_star, cfg, thr)
        i1[str(w_star)] = {"measured": final.tolist(), "predicted": pred.tolist(),
                           "match": bool(np.array_equal(final, pred))}

    i2 = {}
    for consumer, nm in [(0, "spol"), (1, "splan"), (2, "sreg")]:
        cut = w_cut_outputs(cfg, thr, w_cand, consumer, regime)
        surv = [k for k in ("spol", "splan", "sreg") if k != nm]
        byte_same = all(np.array_equal(cut[k], intact[k]) for k in surv)
        base_ok = {"spol": np.all(cut["spol"] == B),
                   "splan": np.all(cut["splan"] == POSTPONE),
                   "sreg": np.all(cut["sreg"] == RELEASE)}[nm]
        i2[nm] = {"no_w_baseline_ok": bool(base_ok),
                  "survivors_byte_identical": bool(byte_same)}

    i4 = {nm: private_copy_divergence(cfg, w_cand, consumer, probe_entry, thr)
          for consumer, nm in [(0, "spol"), (1, "splan"), (2, "sreg")]}

    w_wrong = wrong_w(w_cand, w_true_sign=+1.0, probe_entry=probe_entry, magnitude=3.0)
    o_wrong = apply_specialists(w_wrong, cfg, thr, regime)
    wrong_triple = np.array([o_wrong["spol"][0, -1], o_wrong["splan"][0, -1],
                             o_wrong["sreg"][0, -1]])
    wrong_pred = predicted_triple(-3.0, cfg, thr)
    w_stale = stale_w(w_cand, probe_entry, delta_steps=4)
    o_stale = apply_specialists(w_stale, cfg, thr, regime)
    stale_triple = np.array([o_stale["spol"][0, -1], o_stale["splan"][0, -1],
                             o_stale["sreg"][0, -1]])
    # frozen stale_w injects w[probe_entry-1] (src[..., -1:]), not -delta_steps
    stale_src = float(np.asarray(w_cand)[0, probe_entry - 1])
    stale_pred = predicted_triple(stale_src, cfg, thr)
    i5 = {
        "wrong_sign": {"triple": wrong_triple.tolist(), "pred": wrong_pred.tolist(),
                       "coherent": bool(np.array_equal(wrong_triple, wrong_pred))},
        "stale": {"triple": stale_triple.tolist(), "pred": stale_pred.tolist(),
                  "coherent": bool(np.array_equal(stale_triple, stale_pred))},
    }

    sw = {
        "candidate": single_write_reach(w_cand, 3.0, probe_entry).tolist(),
        "r1": single_write_reach(np.asarray(arms["r1"].run(x)["w"]), 3.0, probe_entry).tolist(),
        "r5": single_write_reach(np.asarray(arms["r5"].run(x)["w"]), 3.0, probe_entry).tolist(),
    }

    # F1 free-recurrence decode: candidate under pi-cut + zero W
    tr_cut = arms["candidate"].run(x, cut_pi=True, zero_w=True)
    h_probe = tr_cut["h"][:, probe_entry:, :].reshape(len(z), -1)
    f1_decode, f1_eps = decode_accuracy(h_probe, z)

    return {"seed": seed, "rows": rows, "extras": extras,
            "i1": i1, "i2": i2, "i4": i4, "i5": i5, "single_write_reach": sw,
            "f1_decode": f1_decode, "f1_eps": f1_eps}


def crosscheck(ep: dict, frozen_by_seed: dict) -> dict:
    seed = ep["seed"]
    fr = {r["arm"]: r for r in frozen_by_seed.get(seed, [])}
    ok = True
    diffs = []
    for row in ep["rows"]:
        fr_row = fr.get(row["arm"])
        if fr_row is None:
            ok = False
            diffs.append({"arm": row["arm"], "key": "(missing)", "a": None, "b": None})
            continue
        for key in FROZEN_KEYS:
            a_val, b_val = row.get(key), fr_row.get(key)
            if a_val is None and b_val is None:
                continue
            if a_val is None or b_val is None or abs(a_val - b_val) > 1e-9:
                ok = False
                diffs.append({"arm": row["arm"], "key": key, "a": a_val, "b": b_val})
    return {"ok": ok, "diffs": diffs}


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--frozen", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--seeds", type=int, nargs="+", default=FINAL_SEEDS)
    args = p.parse_args(argv)

    cfg = Phase3Config()
    os.makedirs(args.out, exist_ok=True)
    ckpt_dir = os.path.join(args.out, "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)

    with open(os.path.join(args.frozen, "rows.jsonl")) as fh:
        frozen_rows = [json.loads(l) for l in fh if l.strip()]
    frozen_by_seed = {}
    for r in frozen_rows:
        frozen_by_seed.setdefault(r["seed"], []).append(r)

    endpoints = []
    for seed in args.seeds:
        print(f"seed {seed}: training + endpoints", flush=True)
        ep = analyze_seed(cfg, seed, ckpt_dir)
        ep["crosscheck"] = crosscheck(ep, frozen_by_seed)
        if not ep["crosscheck"]["ok"]:
            print(f"  CROSS-CHECK FAIL seed {seed}: {ep['crosscheck']['diffs']}", flush=True)
        endpoints.append(ep)

    with open(os.path.join(args.out, "endpoints.json"), "w") as fh:
        json.dump(endpoints, fh, indent=2, default=_default)

    n_fail = sum(1 for e in endpoints if not e["crosscheck"]["ok"])
    print(f"seeds: {len(endpoints)}, cross-check failures: {n_fail}")
    return 1 if n_fail else 0


def _default(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError(type(o))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
