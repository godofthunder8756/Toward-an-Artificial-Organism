"""Track C swap, option K step 1: locate the erasure bypass in v6's saved agents. No training.

    python run_trackc_bypass_diag.py --mode final --out trackc_bypass_diag      # once, after the freeze
    python run_trackc_bypass_diag.py --mode smoke --weights <v6-format dir> --out <scratch dir>
    python run_trackc_bypass_diag.py --score trackc_bypass_diag                  # re-score saved raw results

Plan, decision rules and expectations: TRACKC_BYPASS_DIAG_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import hashlib
import json
import os
import platform
import statistics
import sys
import time
from dataclasses import asdict
from multiprocessing import Pool

import torch

from trackc_swap.bypass import GROUPS, diagnose_agent
from trackc_swap.env import WorldConfig

V6_DIR = "trackc_swap_v6"
SEEDS = list(range(600, 618))
WEAR = 0.001
RATE = 0.3
WINDOW = 3                       # shuffle on the probe step and the two steps before it
N_ENVS = 128
EPISODES = 4
# Decision rules (frozen; protocol section 3)
EXTERNAL = 0.75                  # memoryless accuracy at or above this: the agent stores the bit outside itself
CARRY = 0.5                      # a shuffle that removes at least this share of above-chance accuracy
TESTABLE = 0.75                  # carriage is judged only for agents with accuracy under full erasure >= this
BYPASS_ACC = 0.85                # v6 definition of a bypass agent (full-erasure accuracy above this)
MIN_IDENTIFIED = 9               # of v6's bypass fate agents (11)
ORDER = ["walls", "food", "intero", "view", "all"]   # smallest groups first
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/bypass.py",
           "run_trackc_bypass_diag.py", "TRACKC_BYPASS_DIAG_PROTOCOL.md"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def med(xs):
    xs = list(xs)
    return statistics.median(xs) if xs else None


def carries(cond):
    """Groups whose shuffle removes >= CARRY of the above-chance accuracy in this condition."""
    base = cond["acc"]
    if base < TESTABLE:
        return None
    return {g: (base - cond["shuffled"][g]) >= CARRY * (base - 0.5) for g in GROUPS}


def score(agents, v6_seed_table):
    per = {}
    for a in agents:
        key = f"{a['arm']}_{a['seed']}"
        c = carries(a["full"])
        per[key] = {
            "arm": a["arm"], "seed": a["seed"], "group": a["group"],
            "acc_intact": a["intact"]["acc"], "acc_full": a["full"]["acc"], "acc_memoryless": a["memoryless"]["acc"],
            "external": a["memoryless"]["acc"] >= EXTERNAL,
            "carries_full": c,
            "carries_memoryless": carries(a["memoryless"]),
            "shuffled_full": a["full"]["shuffled"], "shuffled_memoryless": a["memoryless"]["shuffled"],
            "cell_decoder": a["memoryless"]["cell_decoder"],
            "intero_by_target": a["memoryless"]["intero_by_target"],
            "in_band_intact": a["intact"]["in_band"],
        }
    groups = {}
    for gname in ("bypass_fate", "regulator_fate", "other_fate", "yoked", "nofate"):
        rows = [r for r in per.values() if r["group"] == gname]
        if not rows:
            continue
        g = {"n": len(rows), "external": sum(r["external"] for r in rows),
             "acc_full_median": med(r["acc_full"] for r in rows),
             "acc_memoryless_median": med(r["acc_memoryless"] for r in rows),
             "cell_decoder_median": med(r["cell_decoder"] for r in rows),
             "carries_full": {k: sum(bool(r["carries_full"] and r["carries_full"][k]) for r in rows) for k in GROUPS},
             "testable_full": sum(r["carries_full"] is not None for r in rows)}
        groups[gname] = g
    byp = [r for r in per.values() if r["group"] == "bypass_fate"]
    identified = None
    if byp and sum(r["external"] for r in byp) >= MIN_IDENTIFIED:
        for g in ORDER:
            if sum(bool(r["carries_full"] and r["carries_full"][g]) for r in byp) >= MIN_IDENTIFIED:
                identified = g
                break
    verdict = f"IDENTIFIED: {identified}" if identified else "NOT_IDENTIFIED"
    return {"per_agent": per, "groups": groups, "n_bypass_fate": len(byp), "identified": identified,
            "verdict": verdict}


def report(sc):
    L = ["# Track C swap, option K step 1: bypass diagnosis", "", f"**Verdict: {sc['verdict']}**", "",
         f"v6 bypass fate agents: {sc['n_bypass_fate']} (identification needs {MIN_IDENTIFIED}).", "",
         "## Groups", "",
         "| group | n | acc full / memoryless (median) | external store | carries the bit under full erasure: "
         "walls / food / intero / view / all (of testable) | cell decoder |",
         "| --- | --- | --- | --- | --- | --- |"]
    for k, g in sc["groups"].items():
        c = g["carries_full"]
        L.append(f"| {k} | {g['n']} | {g['acc_full_median']:.3f} / {g['acc_memoryless_median']:.3f} | "
                 f"{g['external']}/{g['n']} | {c['walls']} / {c['food']} / {c['intero']} / {c['view']} / {c['all']} "
                 f"(of {g['testable_full']}) | {g['cell_decoder_median']:.3f} |")
    L += ["", "## Per agent", "",
          "| agent | group | acc intact / full / memoryless | full, shuffled: walls / food / intero / view / all | "
          "memoryless, shuffled: walls / food / intero / view / all | cell decoder | intero by target |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for key, r in sorted(sc["per_agent"].items(), key=lambda kv: (kv[1]["arm"], kv[1]["seed"])):
        sf, sm = r["shuffled_full"], r["shuffled_memoryless"]
        L.append(f"| {key} | {r['group']} | {r['acc_intact']:.3f} / {r['acc_full']:.3f} / {r['acc_memoryless']:.3f} | "
                 + " / ".join(f"{sf[g]:.2f}" for g in ORDER) + " | "
                 + " / ".join(f"{sm[g]:.2f}" for g in ORDER) + f" | {r['cell_decoder']:.3f} | "
                 + f"{r['intero_by_target'][0]:.3f} / {r['intero_by_target'][1]:.3f} |")
    return "\n".join(L) + "\n"


def classify(arm, seed, table):
    if arm == "NOFATE":
        return "nofate"
    if arm == "YOKED":
        return "yoked"
    r = table[str(seed)]
    if r["fate_regulator"]:
        return "regulator_fate"
    if r["acc_full_erasure_fate"] > BYPASS_ACC:
        return "bypass_fate"
    return "other_fate"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--weights", default=V6_DIR)
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(report(score(d["agents"], None)))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    table = json.load(open(os.path.join(args.weights, "scores.json")))["scores"]["cells"]["M1"]["per_seed"]
    seeds = SEEDS if args.mode == "final" else sorted(int(s) for s in table)
    wc = WorldConfig(wear=WEAR) if args.mode == "final" else WorldConfig(wear=WEAR, horizon=100)
    n_envs, episodes = (N_ENVS, EPISODES) if args.mode == "final" else (16, 1)
    jobs = []
    for s in seeds:
        for arm in ("FATE", "YOKED", "NOFATE"):
            f = (os.path.join(args.weights, "phase1_weights", f"M1_seed{s}.pt") if arm == "NOFATE"
                 else os.path.join(args.weights, "pair_weights", f"M1_seed{s}_{arm}.pt"))
            sd = torch.load(f, weights_only=False)
            label = {"arm": arm, "seed": s, "group": classify(arm, s, table), "weights": f,
                     "weights_sha256": sha(f)}
            jobs.append((label, sd, s, asdict(wc), n_envs, episodes, RATE, WINDOW))
    t0 = time.time()
    agents = []
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(diagnose_agent, jobs), 1):
            agents.append(r)
            print(f"[{k}/{len(jobs)}] {r['arm']} seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)",
                  flush=True)
    agents.sort(key=lambda r: (r["arm"], r["seed"]))
    meta = {"mode": args.mode, "world": asdict(wc), "rate": RATE, "window": WINDOW, "n_envs": n_envs,
            "episodes": episodes, "seeds": seeds, "seconds": round(time.time() - t0, 1),
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "agents": agents}, fh)
    sc = score(agents, table)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print("verdict:", sc["verdict"])


if __name__ == "__main__":
    main()
