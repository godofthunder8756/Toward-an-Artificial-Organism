"""Track C objective-swap experiment: frozen runner and scorer.

    python run_trackc_swap.py --mode final --out trackc_swap_v1     # once, after the freeze
    python run_trackc_swap.py --mode smoke --out <scratch dir>      # pipeline check, 10 iterations
    python run_trackc_swap.py --score trackc_swap_v1                # re-score saved raw results

Design, decision rules and disclosures: TRACKC_SWAP_PROTOCOL_v1.md.
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

from trackc_swap.env import WorldConfig
from trackc_swap.train import TrainConfig, run_job

FINAL_SEEDS = list(range(100, 109))          # engineering used seeds 0 and 1 only
PRIMARY_DOSE = 4.0
DOSES = [1.0, 2.0, 4.0]                      # kappa_f; 1.0 is the Track B D19 proposed value
PAIR_OBJECTIVES = {4.0: ["M1", "M2", "M4", "M0"], 2.0: ["M1"], 1.0: ["M1"]}
FLOOR_FRAC, MARGIN_FRAC, EQUIV = 0.05, 0.25, 0.25
PAID_FLOOR = 8.0                             # consumed food per 500 steps
LOAD_DROP = 0.15                             # task-load control: required accuracy drop
LEARNED = 0.90                               # task counted as learned
MIN_SEEDS = 8                                # of 9; exact one-sided sign test 10/512 = 0.0195
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py",
           "trackc_swap/train.py", "run_trackc_swap.py", "test_trackc_swap.py",
           "TRACKC_SWAP_PROTOCOL_v1.md"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def build_jobs(mode):
    wc = WorldConfig() if mode == "final" else WorldConfig(horizon=100)
    base = TrainConfig() if mode == "final" else TrainConfig(iters=10, n_envs=16, eval_episodes=1)
    seeds = FINAL_SEEDS if mode == "final" else [9000, 9001]
    jobs = []
    for dose in sorted(PAIR_OBJECTIVES, reverse=True):
        tc = asdict(base) | {"kappa_f": dose}
        for obj in PAIR_OBJECTIVES[dose]:
            jobs += [("pair", obj, s, asdict(wc), tc, DOSES) for s in seeds]
    for obj in ("M1", "DRIVE"):
        jobs += [("nofate", obj, s, asdict(wc), asdict(base), DOSES) for s in seeds]
    return jobs, wc, base


def med(xs):
    return statistics.median(xs)


def score(raw):
    cells = {}
    for r in raw:
        for arm in ("S-FATE", "S-YOKED", "S-NOFATE"):
            if arm in r:
                dose = r["kappa_f"] if arm != "S-NOFATE" else None
                cells.setdefault((arm, r["objective"], dose), {})[r["seed"]] = r[arm]

    def rho(arm, obj, dose=None):
        c = cells[(arm, obj, dose)]
        return {s: c[s]["eval"]["rho"] for s in sorted(c)}

    def acc(arm, obj, dose=None, key="eval"):
        c = cells[(arm, obj, dose)]
        return {s: c[s][key]["best_response_rate"] for s in sorted(c)}

    out = {}
    paid = rho("S-NOFATE", "DRIVE")
    rho_paid = med(paid.values())
    phi, mu = FLOOR_FRAC * rho_paid, MARGIN_FRAC * rho_paid
    nf_m1 = rho("S-NOFATE", "M1")
    nf_acc = acc("S-NOFATE", "M1")
    out["rho_paid_median"] = rho_paid
    out["floor_phi"], out["margin_mu"] = phi, mu
    out["learned"] = med(nf_acc.values()) >= LEARNED
    out["nofate_m1_accuracy_median"] = med(nf_acc.values())
    out["S4_payment"] = {"rho_paid_median": rho_paid, "rho_nofate_m1_median": med(nf_m1.values()),
                         "holds": rho_paid >= PAID_FLOOR and med(nf_m1.values()) <= phi}
    out["doses"] = {}
    for dose in DOSES:
        d = {}
        c = cells[("S-NOFATE", "M1", None)]
        drops = [c[s]["eval"]["best_response_rate"] - c[s]["eval_full_noise"][str(dose)]["best_response_rate"]
                 for s in sorted(c)]
        d["load_drop_median"] = med(drops)
        d["PC_task_loaded"] = med(drops) >= LOAD_DROP
        f, y = rho("S-FATE", "M1", dose), rho("S-YOKED", "M1", dose)
        diffs = {s: f[s] - y[s] for s in f}
        d["rho_fate_m1"] = f
        d["rho_yoked_m1"] = y
        d["rho_fate_m1_median"], d["rho_yoked_m1_median"] = med(f.values()), med(y.values())
        d["seeds_exceeding_margin"] = sum(v >= mu for v in diffs.values())
        d["S1_emergence"] = d["seeds_exceeding_margin"] >= MIN_SEEDS and med(y.values()) <= phi
        fa = acc("S-FATE", "M1", dose)
        hard = acc("S-FATE", "M1", dose, key="eval_full_noise")
        d["fate_m1_accuracy_median"] = med(fa.values())
        d["fate_m1_accuracy_full_noise_median"] = med(hard.values())
        d["yoked_m1_accuracy_median"] = med(acc("S-YOKED", "M1", dose).values())
        cf = cells[("S-FATE", "M1", dose)]
        d["fate_m1_in_band_median"] = med(cf[s]["eval"]["in_band"] for s in cf)
        d["fate_m1_mean_gain_median"] = med(cf[s]["eval"]["mean_gain"] for s in cf)
        d["fate_m1_eat_rate_low_median"] = med(cf[s]["eval"]["eat_rate_low"] for s in cf)
        d["fate_m1_eat_rate_high_median"] = med(cf[s]["eval"]["eat_rate_high"] for s in cf)
        if not d["PC_task_loaded"]:
            d["label"] = "NOT_LOADED"
        elif d["S1_emergence"]:
            d["label"] = "EMERGED"
        elif d["fate_m1_accuracy_full_noise_median"] >= 0.90:
            d["label"] = "ARMOURED"
        elif d["fate_m1_accuracy_median"] < 0.75:
            d["label"] = "UNLEARNED"
        else:
            d["label"] = "NO_EMERGENCE_OTHER"
        out["doses"][str(dose)] = d
    p = PRIMARY_DOSE
    m1 = med(rho("S-FATE", "M1", p).values())
    s2 = {}
    for obj in ("M2", "M4"):
        v = med(rho("S-FATE", obj, p).values())
        s2[obj] = {"rho_fate_median": v, "rho_yoked_median": med(rho("S-YOKED", obj, p).values()),
                   "within": (abs(v - m1) <= EQUIV * m1) if m1 > phi else None,
                   "accuracy_fate_median": med(acc("S-FATE", obj, p).values())}
    out["S2_convention"] = {"cells": s2, "applicable": m1 > phi,
                            "holds": (m1 > phi) and all(c["within"] for c in s2.values())}
    m0 = med(rho("S-FATE", "M0", p).values())
    out["S3_specificity"] = {"rho_fate_m0_median": m0,
                             "rho_yoked_m0_median": med(rho("S-YOKED", "M0", p).values()),
                             "holds": m0 <= phi}
    prim = out["doses"][str(p)]
    out["H3D_supported_at_primary_dose"] = bool(
        out["learned"] and prim["PC_task_loaded"] and prim["S1_emergence"] and
        out["S2_convention"]["holds"] and out["S3_specificity"]["holds"] and out["S4_payment"]["holds"])
    out["primary_label"] = prim["label"] if out["learned"] else "UNRESOLVED_TASK_NOT_LEARNED"
    return out


def report(sc, raw):
    L = ["# Track C objective-swap experiment: results", "",
         f"Primary dose kappa_f = {PRIMARY_DOSE}. Outcome label: **{sc['primary_label']}**. "
         f"H3-D supported: **{sc['H3D_supported_at_primary_dose']}**.", "",
         f"rho = consumed food per 500 steps. Paid regulator rho_paid = {sc['rho_paid_median']:.2f}; "
         f"floor = {sc['floor_phi']:.2f}; margin = {sc['margin_mu']:.2f}. "
         f"No-fate task accuracy (median) = {sc['nofate_m1_accuracy_median']:.3f}.", "",
         "## By dose (objective M1)", "",
         "| kappa_f | task-load drop | loaded | rho fate | rho yoked | seeds over margin | S1 | acc fate | acc fate, full noise | acc yoked | in band | mean gain | label |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for dose, d in sc["doses"].items():
        L.append(f"| {dose} | {d['load_drop_median']:.3f} | {d['PC_task_loaded']} | {d['rho_fate_m1_median']:.2f} | "
                 f"{d['rho_yoked_m1_median']:.2f} | {d['seeds_exceeding_margin']}/9 | {d['S1_emergence']} | "
                 f"{d['fate_m1_accuracy_median']:.3f} | {d['fate_m1_accuracy_full_noise_median']:.3f} | "
                 f"{d['yoked_m1_accuracy_median']:.3f} | {d['fate_m1_in_band_median']:.2f} | "
                 f"{d['fate_m1_mean_gain_median']:.2f} | {d['label']} |")
    L += ["", "## Predictions at the primary dose", "", "| Prediction | Holds | Detail |", "| --- | --- | --- |"]
    prim = sc["doses"][str(PRIMARY_DOSE)]
    L.append(f"| PC task loaded | {prim['PC_task_loaded']} | drop {prim['load_drop_median']:.3f} (need {LOAD_DROP}) |")
    L.append(f"| S1 emergence | {prim['S1_emergence']} | {prim['seeds_exceeding_margin']}/9 seeds over margin; yoked median {prim['rho_yoked_m1_median']:.2f} |")
    s2 = sc["S2_convention"]
    L.append(f"| S2 convention | {s2['holds'] if s2['applicable'] else 'not applicable'} | " +
             "; ".join(f"{k}: fate {v['rho_fate_median']:.2f}, yoked {v['rho_yoked_median']:.2f}" for k, v in s2["cells"].items()) + " |")
    s3 = sc["S3_specificity"]
    L.append(f"| S3 specificity | {s3['holds']} | fate M0 {s3['rho_fate_m0_median']:.2f}; yoked M0 {s3['rho_yoked_m0_median']:.2f} |")
    s4 = sc["S4_payment"]
    L.append(f"| S4 payment | {s4['holds']} | paid {s4['rho_paid_median']:.2f}; no-fate M1 {s4['rho_nofate_m1_median']:.2f} |")
    L += ["", "## Per-seed rho, objective M1", "", "| kappa_f | seed | fate | yoked |", "| --- | --- | --- | --- |"]
    for dose, d in sc["doses"].items():
        for s in d["rho_fate_m1"]:
            L.append(f"| {dose} | {s} | {d['rho_fate_m1'][s]:.2f} | {d['rho_yoked_m1'][s]:.2f} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        raw = json.load(open(os.path.join(args.score, "raw.json")))["jobs"]
        print(json.dumps(score(raw), indent=1, default=str)[:3000])
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    jobs, wc, tc = build_jobs(args.mode)
    t0 = time.time()
    raw = []
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_job, jobs), 1):
            raw.append(r)
            print(f"[{k}/{len(jobs)}] {r['kind']} {r['objective']} seed {r['seed']} kappa_f {r['kappa_f']} "
                  f"({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    raw.sort(key=lambda r: (r["kind"], r["kappa_f"], r["objective"], r["seed"]))
    meta = {"mode": args.mode, "world": asdict(wc), "train": asdict(tc), "seeds": sorted({j[2] for j in jobs}),
            "doses": DOSES, "primary_dose": PRIMARY_DOSE, "seconds": round(time.time() - t0, 1),
            "python": platform.python_version(),
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "jobs": raw}, fh)
    sc = score(raw)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc, raw))
    print("label:", sc["primary_label"], "| H3-D supported:", sc["H3D_supported_at_primary_dose"])


if __name__ == "__main__":
    main()
