"""Track C swap v4 (option E): v3 with gentler maintenance duty (wear 0.001). Frozen runner and scorer.

    python run_trackc_swap4.py --mode final --out trackc_swap_v4     # once, after the freeze
    python run_trackc_swap4.py --mode smoke --out <scratch dir>      # pipeline check
    python run_trackc_swap4.py --score trackc_swap_v4                # re-score saved raw results

Design, decision rules and disclosures: TRACKC_SWAP_PROTOCOL_v4.md.
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
from trackc_swap.erasure import run_pair, run_phase1
from trackc_swap.factorial import GAIN_RULES, state_from_bytes
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(400, 409))          # v1 100-108, v2 200-208, v3 300-308; engineering used 0 and 1
WEAR = 0.001                                 # v1-v3: 0.005
RATES = [0.1, 0.3]                           # erasure probability per step at gain 1
PRIMARY_RATE = 0.3
FLOOR_FRAC, MARGIN_FRAC = 0.05, 0.25
PAID_FLOOR = 2.0                             # half the intake that holds the band at WEAR (about 4.1)
LOAD_DROP = 0.15
LEARNED = 0.90
MIN_SEEDS = 8                                # of 9; exact one-sided sign test 10/512
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py",
           "trackc_swap/train.py", "trackc_swap/factorial.py", "trackc_swap/erasure.py",
           "run_trackc_swap4.py", "test_trackc_swap.py", "TRACKC_SWAP_PROTOCOL_v4.md"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def conditions():
    """(objective, gain_rule, rate) for every scaffolded fate/yoked pair condition."""
    out = [("M1", g, r) for r in RATES for g in GAIN_RULES]
    out += [("M0", g, PRIMARY_RATE) for g in GAIN_RULES]
    return out


def configs(mode):
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001]


def required_intake(wc):
    """Meals per 500 steps that offset expected wear and pulses."""
    return 500 * (wc.wear + wc.pulse_p * wc.pulse_size) / wc.bolus


def med(xs):
    return statistics.median(list(xs))


def acc(e):
    return e["best_response_rate"]


def score(p1, pairs):
    nf = {(r["objective"], r["seed"]): r["S-NOFATE"] for r in p1}
    paid = [v["eval"]["rho"] for (o, s), v in nf.items() if o == "DRIVE"]
    m1 = {s: v for (o, s), v in nf.items() if o == "M1"}
    rho_paid = med(paid)
    phi, mu = FLOOR_FRAC * rho_paid, MARGIN_FRAC * rho_paid
    out = {"rho_paid_median": rho_paid, "floor_phi": phi, "margin_mu": mu,
           "nofate_m1_accuracy_median": med(acc(v["eval"]) for v in m1.values()),
           "nofate_m1_rho_median": med(v["eval"]["rho"] for v in m1.values())}
    out["learned"] = out["nofate_m1_accuracy_median"] >= LEARNED
    out["required_intake"] = required_intake(WorldConfig(wear=WEAR))
    out["S4_payment"] = rho_paid >= PAID_FLOOR and out["nofate_m1_rho_median"] <= mu
    out["task_load"] = {}
    for rate in RATES:
        drop = med(acc(v["eval"]) - acc(v["eval_full_erasure"][str(rate)]) for v in m1.values())
        out["task_load"][str(rate)] = {"drop_median": drop, "loaded": drop >= LOAD_DROP}
    cells = {}
    for r in pairs:
        cells.setdefault((r["objective"], r["gain_rule"], r["rate"]), {})[r["seed"]] = r
    res = {}
    for (obj, g, rate), byseed in sorted(cells.items()):
        seeds = sorted(byseed)
        F = {s: byseed[s]["S-FATE"] for s in seeds}
        Y = {s: byseed[s]["S-YOKED"] for s in seeds}
        f = {s: F[s]["eval"]["rho"] for s in seeds}
        y = {s: Y[s]["eval"]["rho"] for s in seeds}
        diff = {s: f[s] - y[s] for s in seeds}
        band_diff = {s: F[s]["eval"]["in_band"] - Y[s]["eval"]["in_band"] for s in seeds}
        on = {s: byseed[s]["onset"] for s in seeds}
        c = {
            "rho_fate": f, "rho_yoked": y,
            "rho_fate_median": med(f.values()), "rho_yoked_median": med(y.values()),
            "diff_median": med(diff.values()),
            "seeds_exceeding_margin": sum(v >= mu for v in diff.values()),
            "seeds_fate_above_yoked": sum(v > 0 for v in diff.values()),
            "seeds_fate_more_in_band": sum(v > 0 for v in band_diff.values()),
            "in_band_diff_median": med(band_diff.values()),
            "acc_fate_median": med(acc(F[s]["eval"]) for s in seeds),
            "acc_yoked_median": med(acc(Y[s]["eval"]) for s in seeds),
            "acc_fate_full_erasure_median": med(acc(F[s]["eval_full_erasure"]) for s in seeds),
            "acc_fate_no_erasure_median": med(acc(F[s]["eval_no_erasure"]) for s in seeds),
            "acc_yoked_no_erasure_median": med(acc(Y[s]["eval_no_erasure"]) for s in seeds),
            "in_band_fate_median": med(F[s]["eval"]["in_band"] for s in seeds),
            "in_band_yoked_median": med(Y[s]["eval"]["in_band"] for s in seeds),
            "mean_gain_fate_median": med(F[s]["eval"]["mean_gain"] for s in seeds),
            "eat_rate_low_fate_median": med(F[s]["eval"]["eat_rate_low"] for s in seeds),
            "eat_rate_high_fate_median": med(F[s]["eval"]["eat_rate_high"] for s in seeds),
            "onset_acc_fate_median": med(acc(on[s]["S-FATE"]) for s in seeds),
            "onset_rho_fate_median": med(on[s]["S-FATE"]["rho"] for s in seeds),
            "onset_in_band_fate_median": med(on[s]["S-FATE"]["in_band"] for s in seeds),
            "onset_mean_gain_fate_median": med(on[s]["S-FATE"]["mean_gain"] for s in seeds),
        }
        c["S1_emergence"] = c["seeds_exceeding_margin"] >= MIN_SEEDS and c["seeds_fate_more_in_band"] >= MIN_SEEDS
        c["partial"] = c["seeds_fate_above_yoked"] >= MIN_SEEDS and c["seeds_fate_more_in_band"] >= MIN_SEEDS
        if obj == "M1":
            if not out["task_load"][str(rate)]["loaded"]:
                label = "NOT_LOADED"
            elif c["S1_emergence"]:
                label = "EMERGED"
            elif c["acc_fate_full_erasure_median"] >= 0.90:
                label = "ARMOURED"
            elif c["acc_fate_no_erasure_median"] < LEARNED:
                label = "DEGRADED"
            elif c["partial"]:
                label = "PARTIAL"
            else:
                label = "NO_EMERGENCE"
            c["label"] = label
        res[f"{obj}|{g}|{rate}"] = c
    for g in GAIN_RULES:
        m0 = res.get(f"M0|{g}|{PRIMARY_RATE}")
        for rate in RATES:
            c = res[f"M1|{g}|{rate}"]
            c["S3_specificity"] = (m0["diff_median"] < mu) if (m0 and rate == PRIMARY_RATE) else None
            c["H3D_supported"] = bool(out["learned"] and out["S4_payment"] and c["label"] == "EMERGED" and
                                      c["S3_specificity"] is not False)
            c["specificity_tested"] = c["S3_specificity"] is not None
    out["conditions"] = res
    out["any_supported"] = any(c.get("H3D_supported") for c in res.values())
    return out


def report(sc):
    L = ["# Track C swap v4 (option E: erasure fate, scaffolded start, wear 0.001): results", "",
         f"Intake that holds the band: about {sc['required_intake']:.2f} meals per 500 steps.", "",
         f"rho = consumed food per 500 steps. Paid regulator rho_paid = {sc['rho_paid_median']:.2f}; "
         f"floor = {sc['floor_phi']:.2f}; margin = {sc['margin_mu']:.2f}. "
         f"No-fate task accuracy {sc['nofate_m1_accuracy_median']:.3f}; no-fate task agent rho "
         f"{sc['nofate_m1_rho_median']:.2f}. Learned: {sc['learned']}. S4: {sc['S4_payment']}.", "",
         "Task load (accuracy lost by no-fate agents under imposed full erasure): " +
         "; ".join(f"rate {d}: {v['drop_median']:.3f} ({'loaded' if v['loaded'] else 'not loaded'})"
                   for d, v in sc["task_load"].items()), "",
         f"Any condition supports H3-D: **{sc['any_supported']}**.", "",
         "## Objective M1", "",
         "| gain | rate | rho fate | rho yoked | seeds over margin | fate > yoked | fate more in band | in band fate / yoked | "
         "acc fate / yoked | acc fate full erasure | mean gain | S3 | label | H3-D |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    C = sc["conditions"]
    for k, c in C.items():
        obj, g, rate = k.split("|")
        if obj != "M1":
            continue
        s3 = "untested" if c["S3_specificity"] is None else c["S3_specificity"]
        L.append(f"| {g} | {rate} | {c['rho_fate_median']:.2f} | {c['rho_yoked_median']:.2f} | "
                 f"{c['seeds_exceeding_margin']}/9 | {c['seeds_fate_above_yoked']}/9 | {c['seeds_fate_more_in_band']}/9 | "
                 f"{c['in_band_fate_median']:.2f} / {c['in_band_yoked_median']:.2f} | "
                 f"{c['acc_fate_median']:.3f} / {c['acc_yoked_median']:.3f} | {c['acc_fate_full_erasure_median']:.3f} | "
                 f"{c['mean_gain_fate_median']:.2f} | {s3} | {c['label']} | {c['H3D_supported']} |")
    L += ["", f"## Specificity cells (objective M0, rate {PRIMARY_RATE})", "",
          "| gain | rho fate | rho yoked | median paired difference | seeds over margin | fate > yoked | fate more in band |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for k, c in C.items():
        obj, g, rate = k.split("|")
        if obj == "M0":
            L.append(f"| {g} | {c['rho_fate_median']:.2f} | {c['rho_yoked_median']:.2f} | "
                     f"{c['diff_median']:.2f} | {c['seeds_exceeding_margin']}/9 | {c['seeds_fate_above_yoked']}/9 | "
                     f"{c['seeds_fate_more_in_band']}/9 |")
    L += ["", "## Onset (phase-1 agent with fate switched on, before any phase-2 update)", "",
          "| objective | gain | rate | acc | rho | in band | mean gain |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for k, c in C.items():
        obj, g, rate = k.split("|")
        L.append(f"| {obj} | {g} | {rate} | {c['onset_acc_fate_median']:.3f} | {c['onset_rho_fate_median']:.2f} | "
                 f"{c['onset_in_band_fate_median']:.2f} | {c['onset_mean_gain_fate_median']:.2f} |")
    seeds = sorted(next(iter(C.values()))["rho_fate"])
    L += ["", "## Per-seed rho (fate / yoked)", "", "| condition | " + " | ".join(str(s) for s in seeds) + " |",
          "| --- | " + " | ".join("---" for _ in seeds) + " |"]
    for k, c in C.items():
        L.append(f"| {k} | " + " | ".join(f"{c['rho_fate'][s]:.2f} / {c['rho_yoked'][s]:.2f}" for s in seeds) + " |")
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
        print(report(score(d["phase1"], d["pairs"])))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds = configs(args.mode)
    wcd, tcd = asdict(wc), asdict(tc)
    t0 = time.time()
    p1_jobs = [(o, s, wcd, tcd, RATES) for o in ("M1", "M0", "DRIVE") for s in seeds]
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
        pair_jobs = [(o, s, g, rate, wcd, tcd, states[(o, s)]) for (o, g, rate) in conditions() for s in seeds]
        pairs = []
        for k, r in enumerate(pool.imap_unordered(run_pair, pair_jobs), 1):
            pairs.append(r)
            print(f"[pair {k}/{len(pair_jobs)}] {r['objective']} {r['gain_rule']} rate {r['rate']} "
                  f"seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    p1 = sorted((strip(r) for r in p1), key=lambda r: (r["objective"], r["seed"]))
    pairs.sort(key=lambda r: (r["objective"], r["gain_rule"], r["rate"], r["seed"]))
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "seeds": seeds, "rates": RATES,
            "primary_rate": PRIMARY_RATE, "seconds": round(time.time() - t0, 1),
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
