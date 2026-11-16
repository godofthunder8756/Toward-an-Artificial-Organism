"""Track C swap, option T: training length in the base cell. Frozen runner and scorer.

    python run_trackc_length.py --mode final --out trackc_length   # once, after the freeze
    python run_trackc_length.py --mode smoke --out <scratch dir>   # pipeline check
    python run_trackc_length.py --score trackc_length              # re-score saved raw results

A final run that was interrupted is continued by the same command: finished jobs are kept in
<out>/partial and are not run again (every job is deterministic given its seed).

Design, decision rules and disclosures: TRACKC_LENGTH_PROTOCOL.md.
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

from run_trackc_general import ARMS, k_agent, score_cell
from run_trackc_paid import P2_ITERS, PAY, RATE, WEAR, two_sided_sign
from run_trackc_paid2 import ALPHA, MIN_PAIRS, holm, pair_test, wilcoxon_p
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.length import run_seed_t
from trackc_swap.train import TrainConfig

# Frozen (protocol section 2). Seeds are fresh: v1-v8 used 100-808, R 900-917, R2 1000-1027,
# R3 1100-1127, R4 1200-1227, G 1300-1327 and 1400-1427; calibration seeds were 9000-9605.
FINAL_SEEDS = list(range(1500, 1528))
POINTS = (P2_ITERS, 2 * P2_ITERS, 3 * P2_ITERS)      # 3600 (options R-R4), 7200, 10 800 (option G's B2)
SIZES = (128, 4)                                     # downstream: environments, probe episodes (as R-R4 and G)
INTERVAL = 0.95                                      # coverage asked of the interval for a median difference
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py", "trackc_swap/relocate.py",
           "trackc_swap/probe.py", "trackc_swap/causal.py", "trackc_swap/paid.py", "trackc_swap/paid2.py",
           "trackc_swap/general.py", "trackc_swap/length.py", "run_trackc_probe.py", "run_trackc_paid.py",
           "run_trackc_paid2.py", "run_trackc_general.py", "run_trackc_length.py", "test_trackc_swap.py",
           "TRACKC_LENGTH_PROTOCOL.md"]


def configs(mode):
    """(world, phase-1 train config, seeds, measurement points, downstream sizes, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, SIZES, 2
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1),
            [9000, 9001], (20, 40, 60), (16, 1), 2)


def at(seeds, i):
    """The seeds' records as they stood at measurement point i, in the form option G's scorer reads."""
    out = []
    for s in seeds:
        pt = s["points"][i]
        rec = {"seed": s["seed"], "nofate": s["nofate"], "stage1": pt["stage1"], "relocations1": pt["relocations1"],
               "curves1": {k: {n: v[:pt["episodes"]] for n, v in c.items()} for k, c in s["curves"].items()}}
        if "downstream" in pt:
            rec["downstream"] = pt["downstream"]
        out.append(rec)
    return out


def median_interval(d, coverage=INTERVAL):
    """Exact order-statistic interval for the median of d: (low, high, coverage reached); None if
    no pair of order statistics reaches the coverage."""
    d = sorted(x for x in d if x is not None)
    n = len(d)
    for j in range(n // 2, 0, -1):
        cov = 1.0 - 2.0 * sum(comb(n, i) for i in range(j)) / 2.0 ** n
        if cov >= coverage:
            return [d[j - 1], d[n - j], cov]
    return None


def change_test(pairs):
    """T3. pairs: (difference at the first point, difference at the last point) for each seed usable
    at both. Two-sided sign test of the change. Labels NARROWS, WIDENS, NO_CHANGE_DETECTED,
    UNDETERMINED (fewer than MIN_PAIRS pairs)."""
    vals = [(a, b) for a, b in pairs if a is not None and b is not None and a != b]
    n, k = len(vals), sum(b < a for a, b in vals)
    p = two_sided_sign(k, n)
    if n < MIN_PAIRS:
        label = "UNDETERMINED"
    elif p <= ALPHA:
        label = "NARROWS" if k > n - k else "WIDENS"
    else:
        label = "NO_CHANGE_DETECTED"
    return {"n": n, "smaller_at_end": k, "sign_p": p, "wilcoxon_p": wilcoxon_p([b - a for a, b in vals]),
            "first_median": med(a for a, _ in vals), "last_median": med(b for _, b in vals),
            "change_median": med(b - a for a, b in vals), "label": label}


def overall(t1, t2, t3):
    """The run's label from the check at the first point (t1), the primary test at the last point
    (t2) and the change between them (t3). Protocol section 4."""
    labs = (t1["label"], t2["label"], t3["label"])
    if "INVALID" in labs:
        return "INVALID"
    if "UNDETERMINED" in labs[:2]:
        return "UNDETERMINED"
    if labs[0] != "DERIVED_AHEAD":
        return "NOT_REPLICATED"
    narrows = labs[2] == "NARROWS"
    if labs[1] == "DERIVED_AHEAD":
        return "PERSISTS_SMALLER" if narrows else "PERSISTS"
    return "CLOSES" if narrows else "UNRESOLVED"


def score(seeds):
    pts = [p["iters"] for p in seeds[0]["points"]]
    cells = [score_cell(at(seeds, i)) for i in range(len(pts))]
    out = {"n_seeds": len(seeds), "points_at": pts, "points": dict(zip(map(str, pts), cells))}
    first, last = cells[0], cells[-1]
    g0 = (first["G0_regulation"]["label"], last["G0_regulation"]["label"])
    out["T0_regulation"] = {"first": first["G0_regulation"], "last": last["G0_regulation"],
                            "label": "INVALID" if "INVALID" in g0 else "HOLDS" if g0 == ("HOLDS", "HOLDS")
                            else "DOES_NOT_HOLD"}
    reg_all = lambda s, arm: all(c["per_seed"][s["seed"]]["regulator"][arm] for c in cells)
    out["regulators_at_every_point"] = {arm: sum(reg_all(s, arm) for s in seeds) for arm in ARMS}
    if "G1_combined" not in last:
        return out                                           # stage 1 only
    K = lambda s, i, arm: k_agent(s["points"][i]["downstream"][arm])
    def diff(s, i):
        a, b = K(s, i, "DERIVED"), K(s, i, "PAID")
        return None if a is None or b is None else a - b
    out["T1_first"] = t1 = first["G1_combined"]
    out["T2_last"] = t2 = last["G1_combined"]
    both = [s for s in seeds if first["per_seed"][s["seed"]]["usable"] and last["per_seed"][s["seed"]]["usable"]]
    out["usable_at_first_and_last"] = len(both)
    out["T3_change"] = t3 = change_test([(diff(s, 0), diff(s, -1)) for s in both])
    if "INVALID" in (t1["label"], t2["label"]):
        t3["label"] = "INVALID"
    out["overall"] = overall(t1, t2, t3)
    out["holm_T2_T3"] = dict(zip(("T2", "T3"), holm([t2["sign_p"], t3["sign_p"]])))
    sec = {"difference_interval": {}, "K_change": {}, "K_median": {}, "K_below_half": {}, "difference_all_seeds_median": {}}
    for i, p in enumerate(pts):
        c = cells[i]
        sec["difference_interval"][str(p)] = median_interval([diff(s, i) for s in seeds if c["per_seed"][s["seed"]]["usable"]])
        sec["difference_all_seeds_median"][str(p)] = med(diff(s, i) for s in seeds)
        sec["K_median"][str(p)] = {arm: c["descriptive"][arm]["K_median"] for arm in ARMS}
        sec["K_below_half"][str(p)] = {arm: c["descriptive"][arm]["K_below_half"] for arm in ARMS}
    for arm in ("DERIVED", "PAID"):                          # each arm's own K, last point against first
        keep = [s for s in seeds if first["per_seed"][s["seed"]]["regulator"][arm]
                and last["per_seed"][s["seed"]]["regulator"][arm]]
        sec["K_change"][arm] = pair_test([(s["points"][-1]["downstream"][arm], s["points"][0]["downstream"][arm])
                                          for s in keep], k_agent, "LAST", "FIRST")
    sec["change_all_seeds"] = change_test([(diff(s, 0), diff(s, -1)) for s in seeds])
    out["secondary"] = sec
    return out


def report(sc):
    L = ["# Track C swap, option T: training length in the base cell", ""]
    pts = sc["points_at"]
    t0 = sc["T0_regulation"]
    if "overall" in sc:
        h = sc["holm_T2_T3"]
        L += [f"**Overall: {sc['overall']}.** T1 (at {pts[0]}) {sc['T1_first']['label']}; T2 (at {pts[-1]}) "
              f"{sc['T2_last']['label']}; T3 (change) {sc['T3_change']['label']}. Holm-adjusted p: T2 {fmt(h['T2'], 4)}, "
              f"T3 {fmt(h['T3'], 4)}.", ""]
    L += [f"**T0 (derived regulation at the first and last point): {t0['label']}.** Derived regulators "
          f"{t0['first']['derived_regulators']}/{t0['first']['n']} then {t0['last']['derived_regulators']}/{t0['last']['n']} "
          f"(needed {t0['first']['needed']}); yoked {t0['first']['yoked_regulators']} then {t0['last']['yoked_regulators']}. "
          "Regulating at every point: " + ", ".join(f"{k} {v}" for k, v in sc["regulators_at_every_point"].items()) + ".", "",
          "| updates | regulators D / Y / P | usable | in band D / Y / P | K D / Y / P | K below 0.5 D / P | "
          "derived ahead | sign p | Wilcoxon p | median difference | interval | label |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for p in pts:
        c = sc["points"][str(p)]
        reg, arms = c["regulators"], c["arms"]
        row = f"| {p} | " + " / ".join(str(reg[a]) for a in ARMS) + f" | {c['usable']} | " + \
              " / ".join(fmt(arms[a]["in_band_median"]) for a in ARMS) + " | "
        if "G1_combined" in c:
            g, d = c["G1_combined"], c["descriptive"]
            iv = sc["secondary"]["difference_interval"][str(p)]
            row += " / ".join(fmt(d[a]["K_median"]) for a in ARMS) + f" | {d['DERIVED']['K_below_half']} / " \
                   f"{d['PAID']['K_below_half']} | {g['first_ahead']}/{g['n']} | {fmt(g['sign_p'], 4)} | " \
                   f"{fmt(g['wilcoxon_p'], 4)} | {fmt(g['difference_median'])} | " + \
                   ("n/a" if iv is None else f"{fmt(iv[0])} to {fmt(iv[1])}") + f" | {g['label']} |"
        else:
            row += "n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |"
        L.append(row)
    L.append("")
    if "overall" in sc:
        t3, sec = sc["T3_change"], sc["secondary"]
        L += [f"**T3 (change in the within-pair difference, {pts[0]} to {pts[-1]}): {t3['label']}.** Seeds usable at both "
              f"points: {sc['usable_at_first_and_last']}. Smaller at the end in {t3['smaller_at_end']}/{t3['n']} "
              f"(sign p {fmt(t3['sign_p'], 4)}, Wilcoxon p {fmt(t3['wilcoxon_p'], 4)}); median difference "
              f"{fmt(t3['first_median'])} then {fmt(t3['last_median'])}; median change {fmt(t3['change_median'])}.", ""]
        ca = sec["change_all_seeds"]
        L += [f"All seeds, no matching: smaller at the end in {ca['smaller_at_end']}/{ca['n']} (sign p {fmt(ca['sign_p'], 4)}); "
              f"median change {fmt(ca['change_median'])}.", "",
              "| arm (regulating at first and last point) | K higher at the end | sign p | K at the end | K at the first point | "
              "median change | label |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for arm, t in sec["K_change"].items():
            L.append(f"| {arm} | {t['first_ahead']}/{t['n']} | {fmt(t['sign_p'], 4)} | {fmt(t['first_median'])} | "
                     f"{fmt(t['second_median'])} | {fmt(t['difference_median'])} | {t['label']} |")
        L.append("")
        for p in pts:
            c = sc["points"][str(p)]
            s2, fl, sp = c["secondary"], c["secondary"]["flat"], c["learning_speed"]
            L += [f"At {p} updates: K on all seeds derived ahead {s2['K_all_seeds']['first_ahead']}/{s2['K_all_seeds']['n']} "
                  f"(p {fmt(s2['K_all_seeds']['sign_p'], 4)}); pairs within 0.05 {s2['K_tight_pairs']['first_ahead']}/"
                  f"{s2['K_tight_pairs']['n']} (p {fmt(s2['K_tight_pairs']['sign_p'], 4)}); S {s2['S']['first_ahead']}/"
                  f"{s2['S']['n']} ({fmt(s2['S']['first_median'])} against {fmt(s2['S']['second_median'])}); M "
                  f"{s2['M']['first_ahead']}/{s2['M']['n']} ({fmt(s2['M']['first_median'])} against "
                  f"{fmt(s2['M']['second_median'])}); flat derived {fl['derived_flat']}/{fl['derived_n']}, paid "
                  f"{fl['paid_flat']}/{fl['paid_n']}; in-band difference in usable pairs "
                  f"{fmt(s2['in_band_difference_usable_median'])}; K against in-band time, rank correlation derived "
                  f"{fmt(s2['K_vs_in_band_spearman']['DERIVED'], 2)}, paid {fmt(s2['K_vs_in_band_spearman']['PAID'], 2)}; "
                  f"erasure off, regulating derived {c['descriptive']['DERIVED']['regulating_off']}, paid "
                  f"{c['descriptive']['PAID']['regulating_off']}.", ""]
    last = sc["points"][str(pts[-1])]
    sp = last["learning_speed"]
    L += [f"Derived reached sustained regulation sooner than paid in {sp['derived_sooner']}/{sp['n']} "
          f"(p {fmt(sp['sign_p'], 4)}). No-fate task accuracy {fmt(last['nofate_accuracy_median'])} "
          f"(learned: {last['learned']}).", ""]
    return "\n".join(L)


def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(report(score(d["seeds"])))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, points, sizes, stages = configs(args.mode)
    wcd, tcd = asdict(wc), asdict(tc)
    wdir, pdir = os.path.join(args.out, "weights"), os.path.join(args.out, "partial")
    os.makedirs(wdir, exist_ok=True)
    os.makedirs(pdir, exist_ok=True)
    t0 = time.time()
    jobs = [(s, wcd, tcd, RATE, list(points), PAY[1], sizes, stages) for s in seeds]
    ppath = lambda seed: os.path.join(pdir, f"seed{seed}.json")
    recs, todo = [], []
    for job in jobs:                                         # keep what an interrupted run finished
        if os.path.exists(ppath(job[0])):
            recs.append(json.load(open(ppath(job[0]))))
        else:
            todo.append(job)
    done = len(jobs) - len(todo)
    if done:
        print(f"resuming: {done} of {len(jobs)} jobs already finished", flush=True)
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_seed_t, todo), done + 1):
            for name, b in r["weights"].items():
                arm, p = name.split("@")
                torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}_{p}.pt"))
            with open(ppath(r["seed"]) + ".tmp", "w") as fh:
                json.dump(strip(r), fh)
            os.replace(ppath(r["seed"]) + ".tmp", ppath(r["seed"]))
            recs.append(json.load(open(ppath(r["seed"]))))
            print(f"[job {k}/{len(jobs)}] seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE, "pay": PAY[1], "points": list(points),
            "seeds": seeds, "sizes": list(sizes), "seconds": round(sum(r["seconds"] for r in recs), 1),
            "resumed_jobs": done, "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "seeds": recs}, fh)
    sc = score(recs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    for p in sc["points_at"]:
        c = sc["points"][str(p)]
        print(p, "regulators:", c["regulators"], "usable:", c["usable"], c["G0_regulation"]["label"],
              c.get("G1_combined", {}).get("label"))
    print("T0", sc["T0_regulation"]["label"], "T3", sc.get("T3_change", {}).get("label"), "overall", sc.get("overall"))


if __name__ == "__main__":
    main()
