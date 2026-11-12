"""Track C swap, option R: derived against paid regulators. Frozen runner and scorer.

    python run_trackc_paid.py --mode final --out trackc_paid       # once, after the freeze
    python run_trackc_paid.py --mode calib --out <scratch dir>     # calibration seeds, stage 1 only
    python run_trackc_paid.py --mode smoke --out <scratch dir>     # pipeline check
    python run_trackc_paid.py --score trackc_paid                  # re-score saved raw results

Design, decision rules and disclosures: TRACKC_PAID_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import json
import os
import platform
import sys
import time
from dataclasses import asdict
from math import comb
from multiprocessing import Pool

import torch

from run_trackc_probe import D_WIN_MIN, RAW_MIN, fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.paid import SHIFTS, run_seed
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(900, 918))          # fresh; v1-v8 used 100-108 ... 800-808
CALIB_SEEDS = list(range(9100, 9104))        # calibration only, never scored
WEAR = 0.001
RATE = 0.3                                   # SAT, r = 0.3: v7's primary cell
PAY = ("gain", 0.04)                         # PAID's homeostatic reward: kind and weight (set after calibration)
P2_ITERS = 3600
W_ITERS = 1200                               # withdrawal stage
SIZES = (128, 2, 4)                          # downstream: environments, probe episodes, causal episodes
LEARNED = 0.90
# v6's regulator criterion, unchanged
BAND_MIN, TIMING_RATIO, BAND_LEAD = 0.60, 2.0, 0.15
# Option R decision rules (frozen; protocol section 4)
MATCH_MAX = 0.10                             # usable seed: both regulate and in band differs by at most this
MIN_USABLE = 10                              # fewer usable seeds: UNDETERMINED
ALPHA = 0.05                                 # two-sided sign test, R1-R3
CUT_DROP = 0.05                              # R4: a cut arm's in band at least this far below its keep arm
CUT_FRAC = 0.70                              # R4: in at least this share of usable seeds
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py", "trackc_swap/relocate.py",
           "trackc_swap/probe.py", "trackc_swap/causal.py", "trackc_swap/paid.py", "run_trackc_probe.py",
           "run_trackc_paid.py", "test_trackc_swap.py", "TRACKC_PAID_PROTOCOL.md"]


def configs(mode):
    """(world, phase-1 train config, seeds, phase-2 updates, withdrawal updates, downstream sizes, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, P2_ITERS, W_ITERS, SIZES, 3
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_SEEDS, P2_ITERS, W_ITERS, SIZES, 1
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001],
            30, 10, (16, 1, 1), 3)


def regulates(e):
    return e["in_band"] >= BAND_MIN and e["eat_rate_low"] >= TIMING_RATIO * e["eat_rate_high"]


def is_regulator(a, b):
    return regulates(a) and a["in_band"] - b["in_band"] >= BAND_LEAD


def two_sided_sign(k, n):
    """Two-sided sign-test p-value for k successes of n (ties already removed)."""
    if n == 0:
        return None
    tail = sum(comb(n, i) for i in range(max(k, n - k), n + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def anticipation(d):
    return d["r2_D_h"] / d["r2_D_win"] if d["r2_D_win"] >= D_WIN_MIN else None


def retention(d):
    return d["r2_E_h"] / d["r2_E_raw"] if d["r2_E_raw"] >= RAW_MIN else None


def robustness(d):
    base = d["base"]["in_band"]
    return sum(s["in_band"] for s in d["shifts"].values()) / (len(d["shifts"]) * base) if base > 0 else None


def compare(pairs, f):
    """Two-sided paired comparison of f(derived) against f(paid) over usable seeds."""
    vals = [(f(d), f(p)) for d, p in pairs]
    vals = [(a, b) for a, b in vals if a is not None and b is not None and a != b]
    n, k = len(vals), sum(a > b for a, b in vals)
    p = two_sided_sign(k, n)
    if n < MIN_USABLE:
        label = "UNDETERMINED"
    elif p <= ALPHA:
        label = "DERIVED_AHEAD" if k > n - k else "PAID_AHEAD"
    else:
        label = "NO_DIFFERENCE_DETECTED"
    return {"n": n, "derived_ahead": k, "sign_p": p, "derived_median": med(a for a, _ in vals),
            "paid_median": med(b for _, b in vals), "difference_median": med(a - b for a, b in vals), "label": label}


def score(seeds):
    out = {"n_seeds": len(seeds),
           "nofate_accuracy_median": med(s["nofate"]["eval"]["best_response_rate"] for s in seeds)}
    out["learned"] = out["nofate_accuracy_median"] >= LEARNED
    per = {}
    for s in seeds:
        D, Y, P = (s["stage1"][k] for k in ("DERIVED", "YOKED", "PAID"))
        d_reg, p_reg = is_regulator(D, Y), is_regulator(P, Y)
        per[s["seed"]] = {"derived_regulator": d_reg, "paid_regulator": p_reg, "yoked_regulator": is_regulator(Y, D),
                          "in_band": {k: s["stage1"][k]["in_band"] for k in ("DERIVED", "YOKED", "PAID")},
                          "rho": {k: s["stage1"][k]["rho"] for k in ("DERIVED", "YOKED", "PAID")},
                          "usable": bool(d_reg and p_reg and abs(D["in_band"] - P["in_band"]) <= MATCH_MAX)}
    out["per_seed"] = per
    out["derived_regulators"] = sum(x["derived_regulator"] for x in per.values())
    out["paid_regulators"] = sum(x["paid_regulator"] for x in per.values())
    out["yoked_regulators"] = sum(x["yoked_regulator"] for x in per.values())
    out["both_regulate"] = sum(x["derived_regulator"] and x["paid_regulator"] for x in per.values())
    usable = [s for s in seeds if per[s["seed"]]["usable"]]
    out["usable"] = len(usable)
    out["arms"] = {k: {"in_band_median": med(s["stage1"][k]["in_band"] for s in seeds),
                       "rho_median": med(s["stage1"][k]["rho"] for s in seeds),
                       "accuracy_median": med(s["stage1"][k]["best_response_rate"] for s in seeds),
                       "mean_gain_median": med(s["stage1"][k]["mean_gain"] for s in seeds)}
                   for k in ("DERIVED", "YOKED", "PAID")}
    if not all("downstream" in s for s in seeds):
        return out                                           # calibration: stage 1 only
    valid = out["learned"]
    pairs = [(s["downstream"]["DERIVED"], s["downstream"]["PAID"]) for s in usable]
    out["R1_anticipation"] = compare(pairs, anticipation)
    out["R2_suppression"] = compare(pairs, lambda d: d["suppression"]["S"])
    out["R3_robustness"] = compare(pairs, robustness)
    # R4: withdrawal
    n = len(usable)
    dd = [s["stage3"]["DCUT"]["in_band"] - s["stage3"]["DKEEP"]["in_band"] for s in usable]
    pp = [s["stage3"]["PCUT"]["in_band"] - s["stage3"]["PKEEP"]["in_band"] for s in usable]
    kd, kp = sum(v <= -CUT_DROP for v in dd), sum(v <= -CUT_DROP for v in pp)
    d_ok = None if n < MIN_USABLE else kd >= CUT_FRAC * n
    p_ok = None if n < MIN_USABLE else kp >= CUT_FRAC * n
    out["R4_withdrawal"] = {
        "n": n, "derived_cut_dropped": kd, "paid_cut_dropped": kp,
        "derived_change_median": med(dd), "paid_change_median": med(pp),
        "in_band_median": {k: med(s["stage3"][k]["in_band"] for s in usable) for k in ("DKEEP", "DCUT", "PKEEP", "PCUT")},
        "regulating": {k: sum(regulates(s["stage3"][k]) for s in usable) for k in ("DKEEP", "DCUT", "PKEEP", "PCUT")},
        "derived_follows_dependence": d_ok, "paid_follows_payment": p_ok,
        "label": ("UNDETERMINED" if d_ok is None else "BOTH_FOLLOW_THEIR_GROUND" if d_ok and p_ok else
                  "ONLY_DERIVED_DROPS" if d_ok else "ONLY_PAID_DROPS" if p_ok else "NEITHER_DROPS")}
    if not valid:
        for k in ("R1_anticipation", "R2_suppression", "R3_robustness", "R4_withdrawal"):
            out[k]["label"] = "INVALID"
    # descriptive, usable seeds
    desc = {}
    for arm in ("DERIVED", "PAID", "YOKED"):
        ds = [s["downstream"][arm] for s in usable]
        desc[arm] = {"retention_median": med(retention(d) for d in ds),
                     "r2_E_h_median": med(d["r2_E_h"] for d in ds),
                     "anticipation_median": med(anticipation(d) for d in ds),
                     "S_median": med(d["suppression"]["S"] for d in ds),
                     "robustness_median": med(robustness(d) for d in ds),
                     "in_band_off_median": med(d["base"]["in_band"] for d in ds),
                     "in_band_shift_median": {k: med(d["shifts"][k]["in_band"] for d in ds) for k in SHIFTS},
                     "regulating_off": sum(regulates(d["intact"]) for d in ds),
                     "regulating_off_shuffled": sum(regulates(d["shuffled"]) for d in ds),
                     "eats_median": med(d["base"]["eats"] for d in ds)}
    out["descriptive"] = desc
    return out


def report(sc):
    L = ["# Track C swap option R: derived against paid regulators", ""]
    L += [f"Seeds {sc['n_seeds']}. No-fate task accuracy {fmt(sc['nofate_accuracy_median'])} (learned: {sc['learned']}). "
          f"Regulators: derived {sc['derived_regulators']}, paid {sc['paid_regulators']}, yoked {sc['yoked_regulators']}; "
          f"both {sc['both_regulate']}; **usable (both regulate, in band within {MATCH_MAX}) {sc['usable']}**.", "",
          "| arm | in band | rho | task accuracy | mean erasure gain |", "| --- | --- | --- | --- | --- |"]
    for k, a in sc["arms"].items():
        L.append(f"| {k} | {fmt(a['in_band_median'])} | {fmt(a['rho_median'], 2)} | {fmt(a['accuracy_median'])} | "
                 f"{fmt(a['mean_gain_median'])} |")
    if "R1_anticipation" not in sc:
        L += ["", "Calibration: stage 1 only."]
    else:
        L += ["", "## Claims (usable seeds, derived against paid)", "",
              "| claim | label | derived ahead | sign p (two-sided) | derived median | paid median |",
              "| --- | --- | --- | --- | --- | --- |"]
        for k, name in (("R1_anticipation", "R1 anticipation in the state"),
                        ("R2_suppression", "R2 post-meal suppression"), ("R3_robustness", "R3 robustness to world shifts")):
            c = sc[k]
            L.append(f"| {name} | **{c['label']}** | {c['derived_ahead']}/{c['n']} | {fmt(c['sign_p'], 4)} | "
                     f"{fmt(c['derived_median'])} | {fmt(c['paid_median'])} |")
        w = sc["R4_withdrawal"]
        L += ["", f"**R4 withdrawal: {w['label']}.** In band at least {CUT_DROP} below the keep arm: derived (dependence "
              f"removed) {w['derived_cut_dropped']}/{w['n']}, median change {fmt(w['derived_change_median'])}; paid "
              f"(payment removed) {w['paid_cut_dropped']}/{w['n']}, median change {fmt(w['paid_change_median'])}.", "",
              "| arm after withdrawal stage | in band (median) | regulating |", "| --- | --- | --- |"]
        for k in ("DKEEP", "DCUT", "PKEEP", "PCUT"):
            L.append(f"| {k} | {fmt(w['in_band_median'][k])} | {w['regulating'][k]}/{w['n']} |")
        L += ["", "## Descriptive (usable seeds, erasure off)", "",
              "| arm | retention | R2(h -> E) | anticipation | S | robustness | in band base | "
              + " | ".join(SHIFTS) + " | regulating intact / shuffled | eats |",
              "| --- | --- | --- | --- | --- | --- | --- |" + " --- |" * len(SHIFTS) + " --- | --- |"]
        for k, d in sc["descriptive"].items():
            L.append(f"| {k} | {fmt(d['retention_median'])} | {fmt(d['r2_E_h_median'])} | {fmt(d['anticipation_median'])} | "
                     f"{fmt(d['S_median'])} | {fmt(d['robustness_median'])} | {fmt(d['in_band_off_median'])} | "
                     + " | ".join(fmt(d["in_band_shift_median"][s]) for s in SHIFTS)
                     + f" | {d['regulating_off']} / {d['regulating_off_shuffled']} | {fmt(d['eats_median'], 0)} |")
    L += ["", "## Per seed (stage 1)", "",
          "| seed | in band derived / paid / yoked | rho derived / paid / yoked | derived reg | paid reg | usable |",
          "| --- | --- | --- | --- | --- | --- |"]
    for s, x in sorted(sc["per_seed"].items(), key=lambda kv: int(kv[0])):
        b, r = x["in_band"], x["rho"]
        L.append(f"| {s} | {b['DERIVED']:.2f} / {b['PAID']:.2f} / {b['YOKED']:.2f} | {r['DERIVED']:.2f} / "
                 f"{r['PAID']:.2f} / {r['YOKED']:.2f} | {x['derived_regulator']} | {x['paid_regulator']} | {x['usable']} |")
    return "\n".join(L) + "\n"


def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "calib", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    ap.add_argument("--pay", type=float, default=PAY[1], help="calibration only; the final run uses PAY")
    ap.add_argument("--pay-kind", default=PAY[0], help="calibration only; the final run uses PAY")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(report(score(d["seeds"])))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, p2_iters, w_iters, sizes, stages = configs(args.mode)
    pay = PAY if args.mode == "final" else (args.pay_kind, args.pay)
    wcd, tcd = asdict(wc), asdict(tc)
    wdir = os.path.join(args.out, "weights")
    os.makedirs(wdir, exist_ok=True)
    t0 = time.time()
    jobs = [(s, wcd, tcd, RATE, p2_iters, w_iters, pay, sizes, stages) for s in seeds]
    recs = []
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_seed, jobs), 1):
            for arm, b in r["weights"].items():
                torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}.pt"))
            recs.append(strip(r))
            print(f"[seed {k}/{len(jobs)}] {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE, "pay": list(pay), "p2_iters": p2_iters,
            "w_iters": w_iters, "sizes": list(sizes), "seeds": seeds, "seconds": round(time.time() - t0, 1),
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "seeds": recs}, fh)
    sc = score(recs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print("regulators derived/paid/usable:", sc["derived_regulators"], sc["paid_regulators"], sc["usable"])
    for k in ("R1_anticipation", "R2_suppression", "R3_robustness", "R4_withdrawal"):
        if k in sc:
            print(k, sc[k]["label"])


if __name__ == "__main__":
    main()
