"""Track C swap, generality: derived against paid regulators in two new cells (a 128-unit
learner; a world with two body variables). Frozen runner and scorer.

    python run_trackc_general.py --mode final --out trackc_general   # once, after the freeze
    python run_trackc_general.py --mode calib --out <scratch dir>    # calibration seeds, stage 1 only
    python run_trackc_general.py --mode smoke --out <scratch dir>    # pipeline check
    python run_trackc_general.py --score trackc_general              # re-score saved raw results

A final run that was interrupted is continued by the same command: finished jobs are kept in
<out>/partial and are not run again (every job is deterministic given its seed).

Design, decision rules and disclosures: TRACKC_GENERAL_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import json
import os
import platform
import sys
import time
from dataclasses import asdict
from math import ceil
from multiprocessing import Pool

import torch

from run_trackc_paid import BAND_LEAD, BAND_MIN, LEARNED, P2_ITERS, PAY, RATE, TIMING_RATIO, WEAR, two_sided_sign
from run_trackc_paid2 import (ALPHA, C0_MAX_YOKED, C0_SHARE, MATCH_MAX, MIN_PAIRS, combined, first_sustained,
                              fisher_two_sided, holm, pair_test)
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.general import CELLS, run_seed_g
from trackc_swap.train import TrainConfig

# Cells (frozen; protocol sections 2 and 3). Seeds are fresh: v1-v8 used 100-808, R 900-917,
# R2 1000-1027, R3 1100-1127, R4 1200-1227. Calibration seeds are never scored.
RUN = {"H128": {"final": list(range(1300, 1328)), "calib": list(range(9500, 9504)), "p2_iters": P2_ITERS, "pay": PAY[1]},
       "B2": {"final": list(range(1400, 1428)), "calib": list(range(9600, 9606)), "p2_iters": 3 * P2_ITERS, "pay": PAY[1]}}
ARMS = ("DERIVED", "YOKED", "PAID")
SIZES = (128, 4)                             # downstream: environments, probe episodes (as options R-R4)
TIGHT = 0.05                                 # secondary: pairs matched within this in-band difference
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py", "trackc_swap/relocate.py",
           "trackc_swap/probe.py", "trackc_swap/causal.py", "trackc_swap/paid.py", "trackc_swap/paid2.py",
           "trackc_swap/general.py", "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py",
           "run_trackc_general.py", "test_trackc_swap.py", "TRACKC_GENERAL_PROTOCOL.md"]


def configs(mode):
    """(world, phase-1 train config, {cell: seeds}, {cell: phase-2 updates}, downstream sizes, stages)."""
    if mode in ("final", "calib"):
        return (WorldConfig(wear=WEAR), TrainConfig(), {c: v[mode] for c, v in RUN.items()},
                {c: v["p2_iters"] for c, v in RUN.items()}, SIZES, 2 if mode == "final" else 1)
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1),
            {c: [9000, 9001] for c in RUN}, {c: 30 for c in RUN}, (16, 1), 2)


def timing(e):
    """(eat rate while low, eat rate while high) for every body variable of an evaluation."""
    if "eat_rate_low" in e:
        return [(e["eat_rate_low"], e["eat_rate_high"])]
    return [(e[f"eat_rate_low_{r}"], e[f"eat_rate_high_{r}"]) for r in (0, 1)]


def regulates_g(e):
    """v6's criterion, for every body variable: in band (all variables at once) at least BAND_MIN,
    and each variable's items eaten at TIMING_RATIO times the rate when it is low as when high."""
    return e["in_band"] >= BAND_MIN and all(lo >= TIMING_RATIO * hi for lo, hi in timing(e))


def is_regulator_g(a, b):
    return regulates_g(a) and a["in_band"] - b["in_band"] >= BAND_LEAD


def k_res(d):
    """K = 1 - (1 - S)(1 - M) for each body variable of a downstream record."""
    return [combined(x) for x in d["res"]]


def k_agent(d):
    """The agent's K: the mean over its body variables; undefined if any is."""
    ks = k_res(d)
    return None if any(k is None for k in ks) else sum(ks) / len(ks)


def part(d, key, sub):
    """Mean over body variables of S (key "suppression", sub "S") or M ("approach", "M")."""
    v = [x[key][sub] for x in d["res"]]
    return None if any(x is None for x in v) else sum(v) / len(v)


def is_flat(d):
    """Flat eat readiness on at least one body variable; None if undefined on all."""
    v = [x["flat"] for x in d["res"] if x["flat"] is not None]
    return any(v) if v else None


def cross(d):
    """Mean over variables of K computed from the other variable's meals (B2 only)."""
    if "cross" not in d:
        return None
    v = [combined({"suppression": {"S": c["S"]}, "approach": {"M": c["M"]}}) for c in d["cross"]]
    return None if any(x is None for x in v) else sum(v) / len(v)


def spearman(xs, ys):
    """Rank correlation (average ranks for ties); None with fewer than 4 points."""
    pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pts) < 4:
        return None

    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r, i = [0.0] * len(v), 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0
            i = j + 1
        return r

    rx, ry = ranks([p[0] for p in pts]), ranks([p[1] for p in pts])
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx, syy = sum((a - mx) ** 2 for a in rx), sum((b - my) ** 2 for b in ry)
    return sxy / (sxx * syy) ** 0.5 if sxx > 0 and syy > 0 else None


def score_cell(seeds):
    out = {"n_seeds": len(seeds),
           "nofate_accuracy_median": med(s["nofate"]["eval"]["best_response_rate"] for s in seeds)}
    out["learned"] = valid = out["nofate_accuracy_median"] >= LEARNED
    per = {}
    for s in seeds:
        e = s["stage1"]
        reg = {k: is_regulator_g(e[k], e["YOKED"]) for k in ("DERIVED", "PAID")}
        reg["YOKED"] = is_regulator_g(e["YOKED"], e["DERIVED"])
        gap = abs(e["DERIVED"]["in_band"] - e["PAID"]["in_band"])
        both = reg["DERIVED"] and reg["PAID"]
        per[s["seed"]] = {"regulator": reg, "in_band": {k: e[k]["in_band"] for k in ARMS},
                          "rho": {k: e[k]["rho"] for k in ARMS}, "usable": bool(both and gap <= MATCH_MAX),
                          "tight": bool(both and gap <= TIGHT)}
    out["per_seed"] = per
    out["regulators"] = {k: sum(x["regulator"][k] for x in per.values()) for k in ARMS}
    out["usable"] = sum(x["usable"] for x in per.values())
    need = ceil(C0_SHARE * len(seeds))
    out["G0_regulation"] = {
        "derived_regulators": out["regulators"]["DERIVED"], "yoked_regulators": out["regulators"]["YOKED"],
        "n": len(seeds), "needed": need,
        "label": ("INVALID" if not valid else "HOLDS" if (out["regulators"]["DERIVED"] >= need and
                  out["regulators"]["YOKED"] <= C0_MAX_YOKED) else "DOES_NOT_HOLD")}
    ratio = lambda e: min(min(999.0, lo / max(hi, 1e-9)) for lo, hi in timing(e))
    out["arms"] = {k: {"in_band_median": med(s["stage1"][k]["in_band"] for s in seeds),
                       "in_band_each_median": [med(s["stage1"][k][f"in_band_{r}"] for s in seeds) for r in (0, 1)]
                       if "in_band_0" in seeds[0]["stage1"][k] else None,
                       "rho_median": med(s["stage1"][k]["rho"] for s in seeds),
                       "accuracy_median": med(s["stage1"][k]["best_response_rate"] for s in seeds),
                       "timing_ratio_median": med(ratio(s["stage1"][k]) for s in seeds),
                       "relocations_median": med(s["relocations1"][k] for s in seeds),
                       "first_sustained_median": med(first_sustained(s["curves1"][k]["in_band"]) for s in seeds)}
                   for k in ARMS}
    fs = [(first_sustained(s["curves1"]["DERIVED"]["in_band"]), first_sustained(s["curves1"]["PAID"]["in_band"]))
          for s in seeds]
    fs = [(a, b) for a, b in fs if a is not None and b is not None and a != b]
    out["learning_speed"] = {"n": len(fs), "derived_sooner": sum(a < b for a, b in fs),
                             "sign_p": two_sided_sign(sum(a < b for a, b in fs), len(fs))}
    if not all("downstream" in s for s in seeds):
        return out                                           # calibration: stage 1 only
    ds = lambda s, k: s["downstream"][k]
    sel = lambda flag: [(ds(s, "DERIVED"), ds(s, "PAID")) for s in seeds if flag(per[s["seed"]])]
    usable = sel(lambda x: x["usable"])
    test = lambda pairs, f: pair_test(pairs, f, "DERIVED", "PAID")
    # G1: the combined index K, derived against paid, in usable pairs
    g1 = test(usable, k_agent)
    if not valid:
        g1["label"] = "INVALID"
    out["G1_combined"] = g1
    n_res = len(ds(seeds[0], "DERIVED")["res"])
    both = [s for s in seeds if per[s["seed"]]["regulator"]["DERIVED"] and per[s["seed"]]["regulator"]["PAID"]]
    fa = [is_flat(ds(s, "DERIVED")) for s in both]
    fb = [is_flat(ds(s, "PAID")) for s in both]
    fa, fb = [x for x in fa if x is not None], [x for x in fb if x is not None]
    out["secondary"] = {
        "K_all_seeds": test(sel(lambda x: True), k_agent),
        "K_tight_pairs": test(sel(lambda x: x["tight"]), k_agent),
        "K_each_variable": [test(usable, lambda d, r=r: k_res(d)[r]) for r in range(n_res)],
        "S": test(usable, lambda d: part(d, "suppression", "S")),
        "M": test(usable, lambda d: part(d, "approach", "M")),
        "flat": {"derived_flat": sum(fa), "derived_n": len(fa), "paid_flat": sum(fb), "paid_n": len(fb),
                 "fisher_p": fisher_two_sided(sum(fa), len(fa) - sum(fa), sum(fb), len(fb) - sum(fb))},
        "in_band_difference_usable_median": med(per[s["seed"]]["in_band"]["DERIVED"] - per[s["seed"]]["in_band"]["PAID"]
                                                for s in seeds if per[s["seed"]]["usable"]),
        "K_vs_in_band_spearman": {k: spearman([k_agent(ds(s, k)) for s in seeds],
                                              [s["stage1"][k]["in_band"] for s in seeds]) for k in ("DERIVED", "PAID")},
        "cross_K": test(usable, cross) if n_res == 2 else None}
    desc = {}
    for arm in ARMS:
        d = [ds(s, arm) for s in seeds]
        ks = [k_agent(x) for x in d]
        desc[arm] = {"K_median": med(ks), "K_below_half": sum(k is not None and k < 0.5 for k in ks),
                     "K_each_median": [med(k_res(x)[r] for x in d) for r in range(n_res)],
                     "S_median": med(part(x, "suppression", "S") for x in d),
                     "M_median": med(part(x, "approach", "M") for x in d),
                     "cross_K_median": med(cross(x) for x in d), "flat": sum(bool(is_flat(x)) for x in d),
                     "in_band_off_median": med(x["base"]["in_band"] for x in d),
                     "regulating_off": sum(regulates_g(x["base"]) for x in d)}
    out["descriptive"] = desc
    return out


def overall(cells):
    """Label over the two cells' G1 tests, with Holm-adjusted p-values."""
    if not all("G1_combined" in c for c in cells.values()):
        return None
    lab = {k: c["G1_combined"]["label"] for k, c in cells.items()}
    ahead = [k for k, v in lab.items() if v == "DERIVED_AHEAD"]
    if "INVALID" in lab.values():
        label = "INVALID"
    elif len(ahead) == len(lab):
        label = "HOLDS_IN_BOTH"
    elif ahead:
        label = "HOLDS_IN_" + ahead[0] + "_ONLY"
    elif "UNDETERMINED" in lab.values():
        label = "UNDETERMINED"
    else:
        label = "HOLDS_IN_NEITHER"
    h = holm([c["G1_combined"]["sign_p"] for c in cells.values()])
    return {"label": label, "cells": lab, "holm": dict(zip(cells, h))}


def score(raw_cells):
    cells = {c: score_cell(seeds) for c, seeds in raw_cells.items()}
    return {"cells": cells, "overall": overall(cells)}


def report(sc):
    L = ["# Track C swap, generality: derived against paid regulators in two new cells", ""]
    ov = sc["overall"]
    if ov:
        L += [f"**Overall: {ov['label']}.** " + "; ".join(f"{c} {v}" for c, v in ov["cells"].items()) + ". Holm-adjusted p: "
              + ", ".join(f"{c} {fmt(p, 4)}" for c, p in ov["holm"].items()) + ".", ""]
    row = lambda name, c: (f"| {name} | **{c['label']}** | {c['first_ahead']}/{c['n']} | {fmt(c['sign_p'], 4)} | "
                           f"{fmt(c['wilcoxon_p'], 4)} | {fmt(c['first_median'])} | {fmt(c['second_median'])} | "
                           f"{fmt(c['difference_median'])} |")
    for cell, c in sc["cells"].items():
        spec, reg = CELLS[cell], c["regulators"]
        L += [f"## Cell {cell} ({spec['hidden']} units, {spec['n_res']} body variable{'s' if spec['n_res'] > 1 else ''})", "",
              f"Seeds {c['n_seeds']}. No-fate task accuracy {fmt(c['nofate_accuracy_median'])} (learned: {c['learned']}). "
              "Regulators: " + ", ".join(f"{k} {reg[k]}" for k in ARMS) + f". Usable pairs (both regulate, in band within "
              f"{MATCH_MAX}): {c['usable']}.", "",
              "| arm | in band | in band, each variable | rho | eat timing ratio | task accuracy | relocations | "
              "first sustained in band (episode) |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for k, a in c["arms"].items():
            each = "n/a" if a["in_band_each_median"] is None else " / ".join(fmt(x) for x in a["in_band_each_median"])
            L.append(f"| {k} | {fmt(a['in_band_median'])} | {each} | {fmt(a['rho_median'], 2)} | "
                     f"{fmt(a['timing_ratio_median'], 1)} | {fmt(a['accuracy_median'])} | {fmt(a['relocations_median'], 0)} | "
                     f"{fmt(a['first_sustained_median'], 0)} |")
        g0, sp = c["G0_regulation"], c["learning_speed"]
        L += ["", f"**G0 (derived regulation): {g0['label']}.** Derived regulators {g0['derived_regulators']}/{g0['n']} "
              f"(needed {g0['needed']}); yoked regulators {g0['yoked_regulators']} (at most {C0_MAX_YOKED}).", "",
              f"Derived reached sustained regulation sooner than paid in {sp['derived_sooner']}/{sp['n']} "
              f"(p {fmt(sp['sign_p'], 4)}).", ""]
        yn = lambda b: "y" if b else "n"
        if "G1_combined" in c:
            sec = c["secondary"]
            L += ["| comparison (derived against paid) | label | derived ahead | sign p | Wilcoxon p | derived median | "
                  "paid median | median difference |", "| --- | --- | --- | --- | --- | --- | --- | --- |",
                  row("**G1** K, usable pairs", c["G1_combined"]), row("K, all seeds (no matching)", sec["K_all_seeds"]),
                  row(f"K, pairs within {TIGHT}", sec["K_tight_pairs"])]
            L += [row(f"K, variable {r}", t) for r, t in enumerate(sec["K_each_variable"])] if spec["n_res"] > 1 else []
            L += [row("S", sec["S"]), row("M", sec["M"])]
            L += [row("K from the other variable's meals", sec["cross_K"])] if sec["cross_K"] else []
            fl, sr = sec["flat"], sec["K_vs_in_band_spearman"]
            L += ["", f"Flat eat readiness: derived {fl['derived_flat']}/{fl['derived_n']}, paid {fl['paid_flat']}/"
                  f"{fl['paid_n']} (Fisher p {fmt(fl['fisher_p'], 4)}). In-band difference within usable pairs (median, "
                  f"derived minus paid): {fmt(sec['in_band_difference_usable_median'])}. Rank correlation of K with in-band "
                  f"time: derived {fmt(sr['DERIVED'], 2)}, paid {fmt(sr['PAID'], 2)}.", "",
                  "| arm (all seeds, erasure off) | K | K below 0.5 | K each variable | S | M | K from the other "
                  "variable's meals | flat | in band | regulating |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
            for k, d in c["descriptive"].items():
                L.append(f"| {k} | {fmt(d['K_median'])} | {d['K_below_half']} | "
                         + " / ".join(fmt(x) for x in d["K_each_median"]) + f" | {fmt(d['S_median'])} | {fmt(d['M_median'])} | "
                         f"{fmt(d['cross_K_median'])} | {d['flat']} | {fmt(d['in_band_off_median'])} | {d['regulating_off']} |")
            L.append("")
        L += ["| seed | in band " + " / ".join(ARMS) + " | regulator DERIVED / PAID | usable | within " + str(TIGHT) + " |",
              "| --- | --- | --- | --- | --- |"]
        for s, x in sorted(c["per_seed"].items(), key=lambda kv: int(kv[0])):
            L.append(f"| {s} | " + " / ".join(f"{x['in_band'][a]:.2f}" for a in ARMS) + " | "
                     + " / ".join(yn(x["regulator"][a]) for a in ("DERIVED", "PAID")) + f" | {yn(x['usable'])} | {yn(x['tight'])} |")
        L.append("")
    return "\n".join(L)


def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "calib", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(report(score(d["cells"])))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, p2_iters, sizes, stages = configs(args.mode)
    wcd, tcd = asdict(wc), asdict(tc)
    wdir = os.path.join(args.out, "weights")
    os.makedirs(wdir, exist_ok=True)
    t0 = time.time()
    jobs = [(c, s, wcd, tcd, RATE, p2_iters[c], RUN[c]["pay"], sizes, stages) for c in RUN for s in seeds[c]]
    pdir = os.path.join(args.out, "partial")
    os.makedirs(pdir, exist_ok=True)
    ppath = lambda cell, seed: os.path.join(pdir, f"{cell}_seed{seed}.json")
    recs = {c: [] for c in RUN}
    todo = []
    for job in jobs:                                         # keep what an interrupted run finished
        if os.path.exists(ppath(job[0], job[1])):
            recs[job[0]].append(json.load(open(ppath(job[0], job[1]))))
        else:
            todo.append(job)
    done = len(jobs) - len(todo)
    if done:
        print(f"resuming: {done} of {len(jobs)} jobs already finished", flush=True)
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_seed_g, todo), done + 1):
            for arm, b in r["weights"].items():
                torch.save(state_from_bytes(b), os.path.join(wdir, f"{r['cell']}_seed{r['seed']}_{arm}.pt"))
            with open(ppath(r["cell"], r["seed"]) + ".tmp", "w") as fh:
                json.dump(strip(r), fh)
            os.replace(ppath(r["cell"], r["seed"]) + ".tmp", ppath(r["cell"], r["seed"]))
            recs[r["cell"]].append(json.load(open(ppath(r["cell"], r["seed"]))))
            print(f"[job {k}/{len(jobs)}] {r['cell']} {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)",
                  flush=True)
    for c in recs:
        recs[c].sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE, "cells": {c: CELLS[c] for c in RUN},
            "run": {c: {"p2_iters": p2_iters[c], "pay": RUN[c]["pay"], "seeds": seeds[c]} for c in RUN},
            "sizes": list(sizes), "seconds": round(sum(r["seconds"] for v in recs.values() for r in v), 1),
            "resumed_jobs": done,
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "cells": recs}, fh)
    sc = score(recs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    for c, x in sc["cells"].items():
        print(c, "regulators:", x["regulators"], "usable:", x["usable"], x["G0_regulation"]["label"],
              x.get("G1_combined", {}).get("label"))
    if sc["overall"]:
        print("overall", sc["overall"]["label"])


if __name__ == "__main__":
    main()
