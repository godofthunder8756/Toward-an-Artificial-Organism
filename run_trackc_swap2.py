"""Track C swap v2: 2x2 factorial (start x gain rule). Frozen runner and scorer.

    python run_trackc_swap2.py --mode final --out trackc_swap_v2     # once, after the freeze
    python run_trackc_swap2.py --mode smoke --out <scratch dir>      # pipeline check
    python run_trackc_swap2.py --score trackc_swap_v2                # re-score saved raw results

Design, decision rules and disclosures: TRACKC_SWAP_PROTOCOL_v2.md.
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

from trackc_swap.env import WorldConfig
from trackc_swap.factorial import GAIN_RULES, STARTS, run_pair, run_phase1, state_from_bytes
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(200, 209))          # v1 used 100-108; engineering used 0 and 1
DOSES = [2.0, 4.0]
PRIMARY_DOSE = 4.0
FLOOR_FRAC, MARGIN_FRAC = 0.05, 0.25
PAID_FLOOR = 8.0
LOAD_DROP = 0.15
LEARNED = 0.90
MIN_SEEDS = 8                                # of 9; exact one-sided sign test 10/512
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py",
           "trackc_swap/train.py", "trackc_swap/factorial.py", "run_trackc_swap2.py",
           "test_trackc_swap.py", "TRACKC_SWAP_PROTOCOL_v2.md"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def conditions():
    """(objective, gain_rule, start, dose) for every fate/yoked pair condition."""
    out = []
    for dose in DOSES:
        for g in GAIN_RULES:
            for s in STARTS:
                out.append(("M1", g, s, dose))
    for g in GAIN_RULES:
        for s in STARTS:
            out.append(("M0", g, s, PRIMARY_DOSE))
    return out


def configs(mode):
    if mode == "final":
        return WorldConfig(), TrainConfig(), FINAL_SEEDS
    return WorldConfig(horizon=100), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001]


def med(xs):
    return statistics.median(list(xs))


def score(p1, pairs):
    nf = {(r["objective"], r["seed"]): r["S-NOFATE"] for r in p1}
    paid = [v["eval"]["rho"] for (o, s), v in nf.items() if o == "DRIVE"]
    m1 = {s: v for (o, s), v in nf.items() if o == "M1"}
    rho_paid = med(paid)
    phi, mu = FLOOR_FRAC * rho_paid, MARGIN_FRAC * rho_paid
    out = {"rho_paid_median": rho_paid, "floor_phi": phi, "margin_mu": mu,
           "nofate_m1_accuracy_median": med(v["eval"]["best_response_rate"] for v in m1.values()),
           "nofate_m1_rho_median": med(v["eval"]["rho"] for v in m1.values())}
    out["learned"] = out["nofate_m1_accuracy_median"] >= LEARNED
    out["S4_payment"] = rho_paid >= PAID_FLOOR and out["nofate_m1_rho_median"] <= phi
    out["task_load"] = {}
    for dose in DOSES:
        drop = med(v["eval"]["best_response_rate"] - v["eval_full_noise"][str(dose)]["best_response_rate"]
                   for v in m1.values())
        out["task_load"][str(dose)] = {"drop_median": drop, "loaded": drop >= LOAD_DROP}
    cells = {}
    for r in pairs:
        cells.setdefault((r["objective"], r["gain_rule"], r["start"], r["kappa_f"]), {})[r["seed"]] = r
    res = {}
    for (obj, g, st, dose), byseed in sorted(cells.items()):
        seeds = sorted(byseed)
        f = {s: byseed[s]["S-FATE"]["eval"]["rho"] for s in seeds}
        y = {s: byseed[s]["S-YOKED"]["eval"]["rho"] for s in seeds}
        diff = {s: f[s] - y[s] for s in seeds}
        fe = [byseed[s]["S-FATE"]["eval"] for s in seeds]
        c = {
            "rho_fate": f, "rho_yoked": y,
            "rho_fate_median": med(f.values()), "rho_yoked_median": med(y.values()),
            "diff_median": med(diff.values()),
            "seeds_exceeding_margin": sum(v >= mu for v in diff.values()),
            "acc_fate_median": med(e["best_response_rate"] for e in fe),
            "acc_fate_full_noise_median": med(byseed[s]["S-FATE"]["eval_full_noise"]["best_response_rate"] for s in seeds),
            "acc_fate_zero_noise_median": med(byseed[s]["S-FATE"]["eval_zero_noise"]["best_response_rate"] for s in seeds),
            "acc_yoked_median": med(byseed[s]["S-YOKED"]["eval"]["best_response_rate"] for s in seeds),
            "in_band_fate_median": med(e["in_band"] for e in fe),
            "in_band_yoked_median": med(byseed[s]["S-YOKED"]["eval"]["in_band"] for s in seeds),
            "mean_gain_fate_median": med(e["mean_gain"] for e in fe),
            "eat_rate_low_fate_median": med(e["eat_rate_low"] for e in fe),
            "eat_rate_high_fate_median": med(e["eat_rate_high"] for e in fe),
        }
        if st == "SCAFFOLD":
            on = [byseed[s]["onset"] for s in seeds]
            c["onset_acc_fate_median"] = med(o["S-FATE"]["best_response_rate"] for o in on)
            c["onset_rho_fate_median"] = med(o["S-FATE"]["rho"] for o in on)
            c["onset_mean_gain_fate_median"] = med(o["S-FATE"]["mean_gain"] for o in on)
        c["S1_emergence"] = c["seeds_exceeding_margin"] >= MIN_SEEDS and c["rho_yoked_median"] <= phi
        if obj == "M1":
            loaded = out["task_load"][str(dose)]["loaded"]
            if not loaded:
                label = "NOT_LOADED"
            elif c["S1_emergence"]:
                label = "EMERGED"
            elif c["acc_fate_full_noise_median"] >= 0.90:
                label = "ARMOURED"
            elif c["acc_fate_median"] < 0.75:
                label = "DEGRADED" if st == "SCAFFOLD" else "UNLEARNED"
            else:
                label = "NO_EMERGENCE_OTHER"
            c["label"] = label
        res[f"{obj}|{g}|{st}|{dose}"] = c
    for g in GAIN_RULES:
        for st in STARTS:
            m0 = res.get(f"M0|{g}|{st}|{PRIMARY_DOSE}")
            for dose in DOSES:
                c = res[f"M1|{g}|{st}|{dose}"]
                c["S3_specificity"] = (m0["diff_median"] < mu) if (m0 and dose == PRIMARY_DOSE) else None
                c["H3D_supported"] = bool(out["learned"] and out["S4_payment"] and c["label"] == "EMERGED" and
                                          c["S3_specificity"] is not False)
                c["specificity_tested"] = c["S3_specificity"] is not None
    out["conditions"] = res
    out["any_supported"] = any(c.get("H3D_supported") for c in res.values())
    return out


def report(sc):
    L = ["# Track C swap v2 (2x2: start x gain rule): results", "",
         f"rho = consumed food per 500 steps. Paid regulator rho_paid = {sc['rho_paid_median']:.2f}; "
         f"floor = {sc['floor_phi']:.2f}; margin = {sc['margin_mu']:.2f}. "
         f"No-fate task accuracy {sc['nofate_m1_accuracy_median']:.3f}; no-fate task agent rho "
         f"{sc['nofate_m1_rho_median']:.2f}. Learned: {sc['learned']}. S4: {sc['S4_payment']}.", "",
         "Task load (accuracy lost by no-fate agents under imposed full noise): " +
         "; ".join(f"kappa_f {d}: {v['drop_median']:.3f} ({'loaded' if v['loaded'] else 'not loaded'})"
                   for d, v in sc["task_load"].items()), "",
         f"Any condition supports H3-D: **{sc['any_supported']}**.", "",
         "## Objective M1", "",
         "| gain | start | kappa_f | rho fate | rho yoked | seeds over margin | in band fate / yoked | acc fate | acc fate full noise | mean gain | S3 | label | H3-D |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    C = sc["conditions"]
    for k, c in C.items():
        obj, g, st, dose = k.split("|")
        if obj != "M1":
            continue
        s3 = "untested" if c["S3_specificity"] is None else c["S3_specificity"]
        L.append(f"| {g} | {st} | {dose} | {c['rho_fate_median']:.2f} | {c['rho_yoked_median']:.2f} | "
                 f"{c['seeds_exceeding_margin']}/9 | {c['in_band_fate_median']:.2f} / {c['in_band_yoked_median']:.2f} | "
                 f"{c['acc_fate_median']:.3f} | {c['acc_fate_full_noise_median']:.3f} | {c['mean_gain_fate_median']:.2f} | "
                 f"{s3} | {c['label']} | {c['H3D_supported']} |")
    L += ["", "## Specificity cells (objective M0, kappa_f 4)", "",
          "| gain | start | rho fate | rho yoked | median paired difference | seeds over margin |",
          "| --- | --- | --- | --- | --- | --- |"]
    for k, c in C.items():
        obj, g, st, dose = k.split("|")
        if obj == "M0":
            L.append(f"| {g} | {st} | {c['rho_fate_median']:.2f} | {c['rho_yoked_median']:.2f} | "
                     f"{c['diff_median']:.2f} | {c['seeds_exceeding_margin']}/9 |")
    L += ["", "## Scaffold onset (phase-1 agent with fate switched on, before any phase-2 update)", "",
          "| objective | gain | kappa_f | acc at onset | rho at onset | mean gain at onset |", "| --- | --- | --- | --- | --- | --- |"]
    for k, c in C.items():
        obj, g, st, dose = k.split("|")
        if st == "SCAFFOLD":
            L.append(f"| {obj} | {g} | {dose} | {c['onset_acc_fate_median']:.3f} | {c['onset_rho_fate_median']:.2f} | "
                     f"{c['onset_mean_gain_fate_median']:.2f} |")
    L += ["", "## Per-seed rho (fate / yoked)", "", "| condition | " + " | ".join(str(s) for s in FINAL_SEEDS) + " |",
          "| --- | " + " | ".join("---" for _ in FINAL_SEEDS) + " |"]
    for k, c in C.items():
        L.append(f"| {k} | " + " | ".join(f"{c['rho_fate'].get(s, float('nan')):.2f} / {c['rho_yoked'].get(s, float('nan')):.2f}"
                                          for s in sorted(c["rho_fate"])) + " |")
    return "\n".join(L) + "\n"


def strip(r):
    return {k: v for k, v in r.items() if k != "state"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(json.dumps(score(d["phase1"], d["pairs"]), indent=1, default=str)[:4000])
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds = configs(args.mode)
    wcd, tcd = asdict(wc), asdict(tc)
    t0 = time.time()
    p1_jobs = [(o, s, wcd, tcd, DOSES) for o in ("M1", "M0", "DRIVE") for s in seeds]
    with Pool(os.cpu_count() or 1) as pool:
        p1 = []
        for k, r in enumerate(pool.imap_unordered(run_phase1, p1_jobs), 1):
            p1.append(r)
            print(f"[phase1 {k}/{len(p1_jobs)}] {r['objective']} seed {r['seed']} ({r['seconds']} s, "
                  f"elapsed {time.time() - t0:.0f} s)", flush=True)
        states = {(r["objective"], r["seed"]): r["state"] for r in p1}
        sdir = os.path.join(args.out, "phase1_weights")
        os.makedirs(sdir, exist_ok=True)
        for (o, s), b in states.items():
            if o in ("M1", "M0"):
                torch.save(state_from_bytes(b)["agent"], os.path.join(sdir, f"{o}_seed{s}.pt"))
        pair_jobs = [(o, s, g, st, dose, wcd, tcd, states[(o, s)] if st == "SCAFFOLD" else None)
                     for (o, g, st, dose) in conditions() for s in seeds]
        pairs = []
        for k, r in enumerate(pool.imap_unordered(run_pair, pair_jobs), 1):
            pairs.append(r)
            print(f"[pair {k}/{len(pair_jobs)}] {r['objective']} {r['gain_rule']} {r['start']} kappa_f {r['kappa_f']} "
                  f"seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    p1 = sorted((strip(r) for r in p1), key=lambda r: (r["objective"], r["seed"]))
    pairs.sort(key=lambda r: (r["objective"], r["gain_rule"], r["start"], r["kappa_f"], r["seed"]))
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "seeds": seeds, "doses": DOSES,
            "primary_dose": PRIMARY_DOSE, "seconds": round(time.time() - t0, 1),
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "phase1": p1, "pairs": pairs}, fh)
    sc = score(p1, pairs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print("any supported:", sc["any_supported"])
    for k, c in sc["conditions"].items():
        if k.startswith("M1"):
            print(k, c["label"], c["H3D_supported"])


if __name__ == "__main__":
    main()
