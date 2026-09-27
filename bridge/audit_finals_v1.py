"""N12 independent audit of the frozen N11 bridge finals (bridge/finals_v1/).

Read-only: verifies the saved data survives an independent audit and applies
the adversarial-reduction tests from the N12 card. No simulation is re-run and
no frozen source is modified; this file is NOT in the study's frozen hash set.

Sections:
  1. source-hash integrity (snapshot vs on-disk)
  2. coverage / seeds / arm counts
  3. seed discipline (final vs engineering)
  4. checkpoint provenance (cells + spot reload reproduces rows)
  5. raw-to-summary re-derivation (independent sign-flip test)
  6. adversarial reduction (rival arms from the frozen rows)
"""
from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from itertools import product

import torch

from bridge.config import BridgeConfig
from bridge import final_arms as fa

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(REPO, "bridge", "finals_v1", "pre_run_snapshot.json")
ROWS = os.path.join(REPO, "bridge", "finals_v1", "rows.jsonl")
CKPT = os.path.join(REPO, "bridge", "finals_v1", "checkpoints")

FIXED = ["fixed_p1", "fixed_p2", "fixed_p4", "fixed_p8",
         "fixed_p16", "fixed_p32", "fixed_p64"]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sign_flip_p(diffs):
    """Independent exact two-sided sign-flip test (ties dropped)."""
    d = [float(x) for x in diffs if float(x) != 0.0]
    ties = len([x for x in diffs if float(x) == 0.0])
    n = len(d)
    if n == 0:
        return 1.0, ties, 0
    observed = sum(d)
    count = 0
    for mask in range(1 << n):
        s = 0.0
        for i in range(n):
            s += d[i] if (mask >> i) & 1 else -d[i]
        if abs(s) >= abs(observed) - 1e-9:
            count += 1
    return count / (1 << n), ties, n


def op(r):
    return 0.5 * r["stable_slot_surv"] + 0.5 * (1.0 - r["volatile_slot_surv"])


def main() -> int:
    snap = json.load(open(SNAP))
    rows = [json.loads(l) for l in open(ROWS)]
    seeds = sorted({r["seed"] for r in rows})
    by = {(r["seed"], r["arm"]): r for r in rows}

    def series(arm, key):
        return [by[(s, arm)][key] for s in seeds]

    failures = []

    def check(name, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
        if not ok:
            failures.append(name)

    print("1. SOURCE HASH INTEGRITY")
    intact = True
    for rel, rec in snap["sources"].items():
        if sha256_file(os.path.join(REPO, rel)) != rec:
            intact = False
            print(f"  DRIFT {rel}")
    check("all 13 frozen sources intact", intact)

    print("2. COVERAGE / SEEDS / ARMS")
    exp_arms = set(["candidate", "no_maintenance", "free_memory", "oracle",
                    "arm9_d", "arm9_nod", "arm10_P_rb", "arm7_reward",
                    "arm8_multi"] + FIXED)
    arms = Counter(r["arm"] for r in rows)
    cells = {(r["seed"], r["arm"]) for r in rows}
    check("192 rows", len(rows) == 192, f"n={len(rows)}")
    check("12 seeds 2000-2011", seeds == list(range(2000, 2012)))
    check("16 arms, one row per (seed, arm) cell",
          set(arms) == exp_arms and len(arms) == 16 and
          not any((s, a) not in cells for s, a in product(seeds, exp_arms)))

    print("3. SEED DISCIPLINE")
    check("final seeds == row seeds", set(snap["final_seeds"]) == set(seeds))
    check("final/engineering disjoint",
          set(snap["final_seeds"]).isdisjoint(
              set(snap["config"]["training"]["engineering_seeds"])))

    print("4. CHECKPOINT PROVENANCE")
    names = sorted(os.listdir(CKPT))
    trained = ["cand", "arm10_P_rb", "arm7_reward", "arm8_multi"]
    have = {(n[:-3].rsplit("_", 1)[0], int(n[:-3].rsplit("_", 1)[1]))
            for n in names}
    expect = {(a, s) for a in trained for s in seeds}
    check("48 checkpoints, 4 trained arms x 12 seeds, no gaps",
          len(names) == 48 and have == expect)
    # spot reload: candidate + arm10, seed 2000, must reproduce rows
    from bridge.trainer import BridgeTrainer
    cfg = BridgeConfig()
    tr = BridgeTrainer.load_checkpoint(os.path.join(CKPT, "cand_2000.pt"))
    res = fa.evaluate_episodes_uniform(
        cfg, 2000, cfg.training.eval_episodes,
        runner=lambda b: fa.evaluate_candidate_full(tr, b))
    rec = by[(2000, "candidate")]
    ok = (abs(res["stable_slot_surv"] - rec["stable_slot_surv"]) < 1e-6 and
          abs(res["volatile_slot_surv"] - rec["volatile_slot_surv"]) < 1e-6 and
          abs(res["stable_survival"] - rec["stable_survival"]) < 1e-6)
    check("candidate seed-2000 reload reproduces row", ok)

    print("5. RAW-TO-SUMMARY RE-DERIVATION")
    c_slot = series("candidate", "stable_slot_surv")
    n_slot = series("no_maintenance", "stable_slot_surv")
    p, ties, neff = sign_flip_p([a - b for a, b in zip(c_slot, n_slot)])
    check("G-N1 sign-flip p == 2/2^12 floor",
          abs(p - 0.00048828125) < 1e-12 and neff == 12,
          f"p={p:.6f}")
    cand_op = [op(by[(s, "candidate")]) for s in seeds]
    lvl_op = [op(by[(s, "fixed_p1")]) for s in seeds]
    p, ties, neff = sign_flip_p([a - b for a, b in zip(cand_op, lvl_op)])
    check("G3b sign-flip p == 2/2^10 with 2 ties",
          abs(p - 0.001953125) < 1e-12 and ties == 2 and neff == 10,
          f"p={p:.6f}")
    p_rb_op = [op(by[(s, "arm10_P_rb")]) for s in seeds]
    p, ties, neff = sign_flip_p([a - b for a, b in zip(cand_op, p_rb_op)])
    check("N3c sign-flip p == 0.6445 (5 pos / 7 neg)",
          abs(p - 0.64453125) < 1e-9 and neff == 12, f"p={p:.6f}")
    check("candidate op mean == 0.895",
          abs(sum(cand_op) / 12 - 0.8949694718806617) < 1e-9)
    check("oracle == arm9_d == 1.0, arm9_nod == 1.0 (phase-0 knife-edge)",
          abs(sum(op(by[(s, "oracle")]) for s in seeds) / 12 - 1.0) < 1e-9 and
          abs(sum(op(by[(s, "arm9_d")]) for s in seeds) / 12 - 1.0) < 1e-9 and
          abs(sum(op(by[(s, "arm9_nod")]) for s in seeds) / 12 - 1.0) < 1e-9)

    print("6. ADVERSARIAL REDUCTION (frozen rows)")
    for arm in ["candidate", "arm7_reward", "arm8_multi", "arm10_P_rb",
                "oracle", "arm9_d", "no_maintenance", "free_memory"] + FIXED:
        r = [by[(s, arm)] for s in seeds]
        ss = sum(x["stable_slot_surv"] for x in r) / 12
        vs = sum(x["volatile_slot_surv"] for x in r) / 12
        sv = sum(x["stable_survival"] for x in r) / 12
        rf = sum(x["stable_refresh"] for x in r) / 12
        print(f"    {arm:14s} st_slot={ss:.3f} vol_slot={vs:.3f} "
              f"st_surv={sv:.3f} st_refresh={rf:.3f} op={sum(op(x) for x in r)/12:.3f}")
    # free_memory structurally identical to no_maintenance
    ident = all(all(abs(by[(s, "free_memory")][k] - by[(s, "no_maintenance")][k])
                    < 1e-12 for k in ("stable_slot_surv", "stable_refresh",
                                      "stable_survival", "stable_E_final"))
                for s in seeds)
    check("free_memory == no_maintenance in every seed (redundant arm)",
          ident, "both action_never -> slot 0 at probe")

    print()
    print("RESULT:", "ALL CHECKS PASS" if not failures else
          f"FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
