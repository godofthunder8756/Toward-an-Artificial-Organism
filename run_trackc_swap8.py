"""Track C swap v8 (option M): confirmation of v7's r = 0.1 and GRADED r = 0.3 cells. Frozen runner and scorer.

    python run_trackc_swap8.py --mode final --out trackc_swap_v8     # once, after the freeze
    python run_trackc_swap8.py --mode smoke --out <scratch dir>      # pipeline check
    python run_trackc_swap8.py --score trackc_swap_v8                # re-score saved raw results

World, learner and training are v7's (erasure also relocates the agent; trackc_swap/relocate.py, unchanged).
New here: fresh seeds, an M0 control at every M1 cell's gain and rate, and a rate-matched bypass check.
Design, decision rules and disclosures: TRACKC_SWAP_PROTOCOL_v8.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import json
import os
import platform
import sys
import time
from dataclasses import asdict
from multiprocessing import Pool

import torch

from run_trackc_swap7 import acc, cell_stats, med, sha, strip
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.relocate import run_pair_reloc, run_phase1_reloc
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(800, 809))          # fresh; v1-v7 used 100-108 ... 700-708
WEAR = 0.001
RATES = [0.1, 0.3]
P2_ITERS = 3600
CHECKPOINTS = (1200, 2400)                   # descriptive
MARGIN_FRAC = 0.25
PAID_FLOOR = 2.0
LOAD_DROP = 0.15
LEARNED = 0.90
# v8 decision rules (frozen; protocol v8 section 4). Regulator criterion: v6's, via run_trackc_swap7.is_regulator.
EXCESS_MAX = 0.10                            # bypass closed: median (fate - same-seed no-fate) full-erasure acc <= this
NEEDED = 6                                   # of 9 fate regulators per M1 cell
MAX_CONTROL_REGULATORS = 1                   # yoked agents in the cell; M0 fate agents at the same gain and rate
M1_CELLS = [("M1", "SAT", 0.1), ("M1", "GRADED", 0.1), ("M1", "GRADED", 0.3)]
CLAIMS = {"MA": ("M1", "SAT", 0.1), "MB": ("M1", "GRADED", 0.3)}   # GRADED 0.1: labelled, not a claim
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py",
           "trackc_swap/confirm.py", "trackc_swap/relocate.py", "run_trackc_swap7.py", "run_trackc_swap8.py",
           "test_trackc_swap.py", "TRACKC_SWAP_PROTOCOL_v8.md"]


def conditions():
    return M1_CELLS + [("M0", g, r) for (_, g, r) in M1_CELLS]


def ckey(o, g, r):
    return f"{o} {g} {r}"


def configs(mode):
    """(world, train config for phase 1, seeds, phase-2 updates, checkpoints)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, P2_ITERS, CHECKPOINTS
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001],
            30, (10, 20))


def score(p1, pairs):
    nf = {(r["objective"], r["seed"]): r["S-NOFATE"] for r in p1}
    drive = [v for (o, s), v in nf.items() if o == "DRIVE"]
    m1 = {s: v for (o, s), v in nf.items() if o == "M1"}
    rho_paid = med(v["eval"]["rho"] for v in drive)
    mu = MARGIN_FRAC * rho_paid
    out = {"rho_paid_median": rho_paid, "margin_mu": mu,
           "drive_in_band_median": med(v["eval"]["in_band"] for v in drive),
           "nofate_m1_accuracy_median": med(acc(v["eval"]) for v in m1.values()),
           "nofate_m1_rho_median": med(v["eval"]["rho"] for v in m1.values())}
    out["learned"] = out["nofate_m1_accuracy_median"] >= LEARNED
    out["S4_payment"] = rho_paid >= PAID_FLOOR and out["nofate_m1_rho_median"] <= mu
    out["task_load"] = {}
    for rate in RATES:
        drop = med(acc(v["eval"]) - acc(v["eval_full_erasure"][str(rate)]) for v in m1.values())
        out["task_load"][str(rate)] = {"drop_median": drop, "loaded": drop >= LOAD_DROP,
                                       "nofate_full_erasure_median": med(acc(v["eval_full_erasure"][str(rate)])
                                                                         for v in m1.values())}
    cells = {}
    for (o, g, rate) in conditions():
        ps = sorted((r for r in pairs if (r["objective"], r["gain_rule"], r["rate"]) == (o, g, rate)),
                    key=lambda r: r["seed"])
        c = cell_stats(ps, mu)
        if o == "M1":
            for r in ps:
                x = c["per_seed"][r["seed"]]
                x["nofate_full_erasure"] = acc(m1[r["seed"]]["eval_full_erasure"][str(rate)])
                x["bypass_excess"] = x["acc_full_erasure_fate"] - x["nofate_full_erasure"]
            ex = [x["bypass_excess"] for x in c["per_seed"].values()]
            c["bypass_excess_median"] = med(ex)
            c["bypass_excess_max"] = max(ex) if ex else None
            c["seeds_bypass_excess"] = sum(e > EXCESS_MAX for e in ex)
        cells[ckey(o, g, rate)] = c
    base = out["learned"] and out["S4_payment"]
    labels = {}
    for (o, g, rate) in M1_CELLS:
        c, m0 = cells[ckey(o, g, rate)], cells[ckey("M0", g, rate)]
        closed = c["bypass_excess_median"] <= EXCESS_MAX
        spec = m0["regulators_fate"] <= MAX_CONTROL_REGULATORS
        yok = c["regulators_yoked"] <= MAX_CONTROL_REGULATORS
        loaded = out["task_load"][str(rate)]["loaded"]
        enough = c["regulators_fate"] >= NEEDED
        if not (base and loaded):
            lab = "INVALID"
        elif not closed:
            lab = "BYPASS_OPEN"
        elif not (yok and spec):
            lab = "CONTROL_FAILS"
        elif enough:
            lab = "CONFIRMED"
        else:
            lab = "NOT_CONFIRMED"
        labels[ckey(o, g, rate)] = {"label": lab, "closed": closed, "specificity": spec, "yoked_ok": yok,
                                    "loaded": loaded, "regulators": c["regulators_fate"], "needed": NEEDED}
    out["claims"] = {k: labels[ckey(*cell)]["label"] == "CONFIRMED" for k, cell in CLAIMS.items()}
    out["labels"] = labels
    out["cells"] = cells
    return out


def report(sc):
    L = ["# Track C swap v8 (option M: confirmation in the relocation world): results", "",
         "**Claims (each: >= 6/9 fate regulators, bypass closed at the cell's rate, yoked and M0 controls <= 1):**", ""]
    for k, cell in CLAIMS.items():
        L.append(f"- {k} ({ckey(*cell)}): **{'CONFIRMED' if sc['claims'][k] else 'NOT CONFIRMED'}** "
                 f"({sc['labels'][ckey(*cell)]['label']})")
    L += ["", f"Paid regulator rho_paid = {sc['rho_paid_median']:.2f}, in band {sc['drive_in_band_median']:.2f}; "
          f"margin = {sc['margin_mu']:.2f}. No-fate task accuracy {sc['nofate_m1_accuracy_median']:.3f}; "
          f"no-fate task agent rho {sc['nofate_m1_rho_median']:.2f}. Learned: {sc['learned']}. S4: {sc['S4_payment']}. "
          "Task load: " + "; ".join(f"{r}: {v['drop_median']:.3f} ({'loaded' if v['loaded'] else 'not loaded'}; "
                                    f"no-fate full-erasure acc {v['nofate_full_erasure_median']:.3f})"
                                    for r, v in sc["task_load"].items()) + ".", "",
          "## Labels (M1 cells)", "",
          "| cell | label | regulators (needed) | bypass closed (median excess over no-fate; max; seeds > 0.10) | "
          "yoked regulators <= 1 | M0 regulators <= 1 |",
          "| --- | --- | --- | --- | --- | --- |"]
    for k, l in sc["labels"].items():
        c, m0 = sc["cells"][k], sc["cells"]["M0" + k[2:]]
        L.append(f"| {k} | {l['label']} | {l['regulators']}/{c['n']} ({l['needed']}) | {l['closed']} "
                 f"({c['bypass_excess_median']:+.3f}; {c['bypass_excess_max']:+.3f}; {c['seeds_bypass_excess']}) | "
                 f"{l['yoked_ok']} ({c['regulators_yoked']}) | {l['specificity']} ({m0['regulators_fate']}) |")
    L += ["", "## Cells (medians)", "",
          "| cell | regulators fate / yoked | in band fate / yoked | fate more in band | rho fate / yoked | over margin | "
          "acc fate / yoked | acc full erasure fate / yoked | acc erasure off fate | "
          "Spearman(in band, full-erasure acc) |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for k, c in sc["cells"].items():
        L.append(f"| {k} | {c['regulators_fate']} / {c['regulators_yoked']} | {c['in_band_fate_median']:.2f} / "
                 f"{c['in_band_yoked_median']:.2f} | {c['seeds_fate_more_in_band']}/{c['n']} | "
                 f"{c['rho_fate_median']:.2f} / {c['rho_yoked_median']:.2f} | {c['seeds_exceeding_margin']}/{c['n']} | "
                 f"{c['acc_fate_median']:.3f} / {c['acc_yoked_median']:.3f} | "
                 f"{c['acc_full_erasure_fate_median']:.3f} / {c['acc_full_erasure_yoked_median']:.3f} | "
                 f"{c['acc_no_erasure_fate_median']:.3f} | {c['tradeoff_spearman']:.2f} |")
    L += ["", "## Checkpoints (descriptive)", "",
          "| cell | updates | fate regulators | in band fate | fate more in band | acc full erasure fate |",
          "| --- | --- | --- | --- | --- | --- |"]
    for k, c in sc["cells"].items():
        for it, ck in c["checkpoints"].items():
            L.append(f"| {k} | {it} | {ck['regulators_fate']}/{c['n']} | {ck['in_band_fate_median']:.2f} | "
                     f"{ck['seeds_fate_more_in_band']}/{c['n']} | {ck['acc_full_erasure_fate_median']:.3f} |")
        L.append(f"| {k} | final | {c['regulators_fate']}/{c['n']} | {c['in_band_fate_median']:.2f} | "
                 f"{c['seeds_fate_more_in_band']}/{c['n']} | {c['acc_full_erasure_fate_median']:.3f} |")
    for k, c in sc["cells"].items():
        m1 = k.startswith("M1")
        L += ["", f"## Per seed, {k}", "",
              "| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | "
              "acc full erasure fate / yoked |" + (" excess over no-fate |" if m1 else "")
              + " fate regulator | yoked regulator |",
              "| --- | --- | --- | --- | --- | --- |" + (" --- |" if m1 else "") + " --- | --- |"]
        for s, x in sorted(c["per_seed"].items(), key=lambda kv: int(kv[0])):
            L.append(f"| {s} | {x['rho_fate']:.2f} / {x['rho_yoked']:.2f} | {x['in_band_fate']:.2f} / "
                     f"{x['in_band_yoked']:.2f} | {x['eat_low_fate']:.4f} / {x['eat_high_fate']:.4f} | "
                     f"{x['mean_gain_fate']:.2f} | {x['acc_full_erasure_fate']:.3f} / {x['acc_full_erasure_yoked']:.3f} |"
                     + (f" {x['bypass_excess']:+.3f} |" if m1 else "")
                     + f" {x['fate_regulator']} | {x['yoked_regulator']} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(report(score(d["phase1"], d["pairs"])))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, p2_iters, checkpoints = configs(args.mode)
    wcd, tcd = asdict(wc), asdict(tc)
    t0 = time.time()
    p1_jobs = [(o, s, wcd, tcd, RATES) for o in ("M1", "M0", "DRIVE") for s in seeds]
    pdir = os.path.join(args.out, "pair_weights")
    os.makedirs(pdir, exist_ok=True)
    with Pool(os.cpu_count() or 1) as pool:
        p1 = []
        for k, r in enumerate(pool.imap_unordered(run_phase1_reloc, p1_jobs), 1):
            p1.append(r)
            print(f"[phase1 {k}/{len(p1_jobs)}] {r['objective']} seed {r['seed']} ({r['seconds']} s, "
                  f"elapsed {time.time() - t0:.0f} s)", flush=True)
        states = {(r["objective"], r["seed"]): r["state"] for r in p1}
        sdir = os.path.join(args.out, "phase1_weights")
        os.makedirs(sdir, exist_ok=True)
        for (o, s), b in states.items():
            if o in ("M1", "M0"):
                torch.save(state_from_bytes(b)["agent"], os.path.join(sdir, f"{o}_seed{s}.pt"))
        pair_jobs = [(o, s, g, rate, wcd, tcd, states[(o, s)], p2_iters, checkpoints)
                     for (o, g, rate) in conditions() for s in seeds]
        pairs = []
        for k, r in enumerate(pool.imap_unordered(run_pair_reloc, pair_jobs), 1):
            for arm, b in r["weights"].items():
                torch.save(state_from_bytes(b), os.path.join(
                    pdir, f"{r['objective']}_{r['gain_rule']}_r{r['rate']}_seed{r['seed']}_{arm}.pt"))
            pairs.append(strip(r))
            print(f"[pair {k}/{len(pair_jobs)}] {r['objective']} {r['gain_rule']} rate {r['rate']} "
                  f"seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    p1 = sorted((strip(r) for r in p1), key=lambda r: (r["objective"], r["seed"]))
    pairs.sort(key=lambda r: (r["objective"], r["gain_rule"], r["rate"], r["seed"]))
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "p2_iters": p2_iters, "checkpoints": list(checkpoints),
            "seeds": seeds, "rates": RATES, "claims": {k: list(v) for k, v in CLAIMS.items()},
            "relocate_on_erasure": True,
            "seconds": round(time.time() - t0, 1), "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "phase1": p1, "pairs": pairs}, fh)
    sc = score(p1, pairs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print("claims:", sc["claims"])
    for k, l in sc["labels"].items():
        print(k, l["label"])


if __name__ == "__main__":
    main()
