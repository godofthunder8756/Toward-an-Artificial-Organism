"""Track C swap, option R2: replication of derived against paid, with a relocation control.
Frozen runner and scorer.

    python run_trackc_paid2.py --mode final --out trackc_paid2     # once, after the freeze
    python run_trackc_paid2.py --mode calib --out <scratch dir>    # calibration seeds, stage 1 only
    python run_trackc_paid2.py --mode smoke --out <scratch dir>    # pipeline check
    python run_trackc_paid2.py --score trackc_paid2                # re-score saved raw results

Design, decision rules and disclosures: TRACKC_PAID2_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import json
import os
import platform
import sys
import time
from dataclasses import asdict
from math import ceil, comb
from multiprocessing import Pool

import torch

from run_trackc_paid import (BAND_LEAD, BAND_MIN, LEARNED, P2_ITERS, PAY, RATE, SIZES, TIMING_RATIO, WEAR,
                             is_regulator, regulates, two_sided_sign)
from run_trackc_probe import D_WIN_MIN, fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.paid2 import run_seed2
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(1000, 1028))        # fresh; v1-v8 used 100-808, option R 900-917
CALIB_SEEDS = list(range(9200, 9204))        # calibration only, never scored
ARMS = ("DERIVED", "YOKED", "PAID", "PAIDR")
# Decision rules (frozen; protocol section 4). The regulator criterion, cell, payment, training
# length and downstream sizes are option R's, imported unchanged.
C0_SHARE = 2 / 3                             # C0: derived regulators, share of seeds (option R: 12 of 18)
C0_MAX_YOKED = 1                             # C0: yoked regulators
MATCH_MAX = 0.10                             # usable pair: both regulate and in band differs by at most this
MIN_PAIRS = 14                               # fewer pairs: UNDETERMINED
ALPHA = 0.05                                 # two-sided, every test
DECODE_FAIL = -0.10                          # held-out R2(h -> D) below this: the decoder failed, index undefined
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py", "trackc_swap/relocate.py",
           "trackc_swap/probe.py", "trackc_swap/causal.py", "trackc_swap/paid.py", "trackc_swap/paid2.py",
           "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py", "test_trackc_swap.py",
           "TRACKC_PAID2_PROTOCOL.md"]


def configs(mode):
    """(world, phase-1 train config, seeds, phase-2 updates, downstream sizes, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, P2_ITERS, SIZES, 2
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_SEEDS, P2_ITERS, SIZES, 1
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001],
            30, (16, 1, 1), 2)


def anticipation2(d):
    """Option R's anticipation index, undefined when the decoder failed."""
    if d["r2_D_win"] < D_WIN_MIN or d["r2_D_h"] < DECODE_FAIL:
        return None
    return d["r2_D_h"] / d["r2_D_win"]


def combined(d):
    """Combined post-meal suppression K = 1 - (1 - S)(1 - M): how far the readiness to get a
    meal (approach food, then eat it) falls after a meal the agent has not yet sensed."""
    S, M = d["suppression"]["S"], d["approach"]["M"]
    return None if S is None or M is None else 1.0 - (1.0 - S) * (1.0 - M)


def wilcoxon_p(diffs):
    """Exact two-sided Wilcoxon signed-rank p-value (zeros dropped, average ranks for ties)."""
    d = [x for x in diffs if x != 0]
    n = len(d)
    if n == 0:
        return None
    order = sorted(range(n), key=lambda i: abs(d[i]))
    rank2 = [0] * n                                   # twice the rank, so that tied ranks stay integers
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(d[order[j + 1]]) == abs(d[order[i]]):
            j += 1
        for k in range(i, j + 1):
            rank2[order[k]] = i + j + 2
        i = j + 1
    total = sum(rank2)
    w = sum(r for r, x in zip(rank2, d) if x > 0)
    counts = [1] + [0] * total
    for r in rank2:
        for s in range(total, r - 1, -1):
            counts[s] += counts[s - r]
    lo = min(w, total - w)
    return min(1.0, 2 * sum(counts[:lo + 1]) / 2 ** n)


def fisher_two_sided(a, b, c, d):
    """Two-sided Fisher exact p for the table [[a, b], [c, d]]."""
    n, r1, c1 = a + b + c + d, a + b, a + c
    if n == 0:
        return None
    pr = lambda x: comb(c1, x) * comb(n - c1, r1 - x) / comb(n, r1)
    p0 = pr(a)
    return min(1.0, sum(pr(x) for x in range(max(0, r1 - (n - c1)), min(r1, c1) + 1) if pr(x) <= p0 * (1 + 1e-9)))


def holm(ps):
    """Holm-adjusted p-values, in the order given (None entries stay None)."""
    idx = sorted((i for i, p in enumerate(ps) if p is not None), key=lambda i: ps[i])
    out, m, run = [None] * len(ps), len(idx), 0.0
    for rank, i in enumerate(idx):
        run = max(run, min(1.0, (m - rank) * ps[i]))
        out[i] = run
    return out


def pair_test(pairs, f, hi, lo):
    """Two-sided paired sign test of f(first) against f(second). Labels: <hi>_AHEAD, <lo>_AHEAD,
    NO_DIFFERENCE_DETECTED, UNDETERMINED (fewer than MIN_PAIRS pairs with both values)."""
    vals = [(f(a), f(b)) for a, b in pairs]
    vals = [(a, b) for a, b in vals if a is not None and b is not None and a != b]
    n, k = len(vals), sum(a > b for a, b in vals)
    p = two_sided_sign(k, n)
    if n < MIN_PAIRS:
        label = "UNDETERMINED"
    elif p <= ALPHA:
        label = f"{hi}_AHEAD" if k > n - k else f"{lo}_AHEAD"
    else:
        label = "NO_DIFFERENCE_DETECTED"
    return {"n": n, "first_ahead": k, "sign_p": p, "wilcoxon_p": wilcoxon_p([a - b for a, b in vals]),
            "first_median": med(a for a, _ in vals), "second_median": med(b for _, b in vals),
            "difference_median": med(a - b for a, b in vals), "label": label}


def flat_test(first, second, hi, lo):
    """Fisher exact test of the share of flat agents in two groups of downstream records."""
    fa = [d["flat"] for d in first if d["flat"] is not None]
    fb = [d["flat"] for d in second if d["flat"] is not None]
    a, c = sum(fa), sum(fb)
    p = fisher_two_sided(a, len(fa) - a, c, len(fb) - c)
    if min(len(fa), len(fb)) < MIN_PAIRS:
        label = "UNDETERMINED"
    elif p <= ALPHA:
        label = f"{hi}_MORE_FLAT" if a * len(fb) > c * len(fa) else f"{lo}_MORE_FLAT"
    else:
        label = "NO_DIFFERENCE_DETECTED"
    return {"first_flat": a, "first_n": len(fa), "second_flat": c, "second_n": len(fb), "fisher_p": p, "label": label}


def first_sustained(curve, level=BAND_MIN, run=5):
    """Index of the first episode from which in-band time stays at or above `level` for `run` episodes."""
    for i in range(len(curve) - run + 1):
        if min(curve[i:i + run]) >= level:
            return i
    return None


def score(seeds):
    out = {"n_seeds": len(seeds),
           "nofate_accuracy_median": med(s["nofate"]["eval"]["best_response_rate"] for s in seeds)}
    out["learned"] = valid = out["nofate_accuracy_median"] >= LEARNED
    per = {}
    for s in seeds:
        e = s["stage1"]
        reg = {k: is_regulator(e[k], e["YOKED"]) for k in ("DERIVED", "PAID", "PAIDR")}
        reg["YOKED"] = is_regulator(e["YOKED"], e["DERIVED"])
        match = lambda a, b: bool(reg[a] and reg[b] and abs(e[a]["in_band"] - e[b]["in_band"]) <= MATCH_MAX)
        per[s["seed"]] = {"regulator": reg, "in_band": {k: e[k]["in_band"] for k in ARMS},
                          "rho": {k: e[k]["rho"] for k in ARMS},
                          "usable": {"D_P": match("DERIVED", "PAID"), "R_P": match("PAIDR", "PAID"),
                                     "D_R": match("DERIVED", "PAIDR")}}
    out["per_seed"] = per
    out["regulators"] = {k: sum(x["regulator"][k] for x in per.values()) for k in ARMS}
    out["usable"] = {k: sum(x["usable"][k] for x in per.values()) for k in ("D_P", "R_P", "D_R")}
    need = ceil(C0_SHARE * len(seeds))
    out["C0_regulation"] = {
        "derived_regulators": out["regulators"]["DERIVED"], "yoked_regulators": out["regulators"]["YOKED"],
        "n": len(seeds), "needed": need,
        "label": ("INVALID" if not valid else "HOLDS" if (out["regulators"]["DERIVED"] >= need and
                  out["regulators"]["YOKED"] <= C0_MAX_YOKED) else "DOES_NOT_HOLD")}
    out["arms"] = {k: {"in_band_median": med(s["stage1"][k]["in_band"] for s in seeds),
                       "rho_median": med(s["stage1"][k]["rho"] for s in seeds),
                       "accuracy_median": med(s["stage1"][k]["best_response_rate"] for s in seeds),
                       "timing_ratio_median": med(min(999.0, s["stage1"][k]["eat_rate_low"] /
                                                      max(s["stage1"][k]["eat_rate_high"], 1e-9)) for s in seeds),
                       "relocations_median": med(s["relocations1"][k] for s in seeds),
                       "first_sustained_median": med(first_sustained(s["curves1"][k]["in_band"]) for s in seeds)}
                   for k in ARMS}
    if not all("downstream" in s for s in seeds):
        return out                                           # calibration: stage 1 only
    ds = lambda s, k: s["downstream"][k]
    pairs = lambda key, a, b: [(ds(s, a), ds(s, b)) for s in seeds if per[s["seed"]]["usable"][key]]
    dp, rp, dr = pairs("D_P", "DERIVED", "PAID"), pairs("R_P", "PAIDR", "PAID"), pairs("D_R", "DERIVED", "PAIDR")
    # C1 (primary): the anticipation index, derived against paid
    c1 = pair_test(dp, anticipation2, "DERIVED", "PAID")
    c1["label"] = {"DERIVED_AHEAD": "REPLICATED", "PAID_AHEAD": "REVERSED",
                   "NO_DIFFERENCE_DETECTED": "NOT_REPLICATED"}.get(c1["label"], c1["label"])
    out["C1_anticipation"] = c1
    # C2: flat eat readiness, among seeds where both regulate
    both = [s for s in seeds if per[s["seed"]]["regulator"]["DERIVED"] and per[s["seed"]]["regulator"]["PAID"]]
    out["C2_flat"] = flat_test([ds(s, "DERIVED") for s in both], [ds(s, "PAID") for s in both], "DERIVED", "PAID")
    # C3: combined post-meal suppression K, derived against paid
    out["C3_combined"] = pair_test(dp, combined, "DERIVED", "PAID")
    # C4: the relocation control, on K
    r_p, d_r = pair_test(rp, combined, "PAIDR", "PAID"), pair_test(dr, combined, "DERIVED", "PAIDR")
    up, below = r_p["label"] == "PAIDR_AHEAD", d_r["label"] == "DERIVED_AHEAD"
    if "UNDETERMINED" in (r_p["label"], d_r["label"]):
        label = "UNDETERMINED"
    else:
        label = ("PARTIAL" if up and below else "RELOCATION_SUFFICES" if up else
                 "RELOCATION_NOT_SUFFICIENT" if below else "UNDETERMINED")
    reg3 = [s for s in seeds if all(per[s["seed"]]["regulator"][k] for k in ("DERIVED", "PAID", "PAIDR"))]
    out["C4_relocation"] = {
        "paidr_vs_paid": r_p, "derived_vs_paidr": d_r, "label": label,
        "anticipation_paidr_vs_paid": pair_test(rp, anticipation2, "PAIDR", "PAID"),
        "anticipation_derived_vs_paidr": pair_test(dr, anticipation2, "DERIVED", "PAIDR"),
        "flat_paidr_vs_paid": flat_test([ds(s, "PAIDR") for s in reg3], [ds(s, "PAID") for s in reg3], "PAIDR", "PAID"),
        "flat_derived_vs_paidr": flat_test([ds(s, "DERIVED") for s in reg3], [ds(s, "PAIDR") for s in reg3],
                                           "DERIVED", "PAIDR")}
    if not valid:
        for k in ("C1_anticipation", "C2_flat", "C3_combined", "C4_relocation"):
            out[k]["label"] = "INVALID"
    h = holm([c1["sign_p"], out["C2_flat"]["fisher_p"], out["C3_combined"]["sign_p"]])
    out["holm_C1_C2_C3"] = {"C1_anticipation": h[0], "C2_flat": h[1], "C3_combined": h[2]}
    # secondary and descriptive
    all_dp = [(ds(s, "DERIVED"), ds(s, "PAID")) for s in both]
    out["secondary"] = {
        "S_derived_vs_paid": pair_test(dp, lambda d: d["suppression"]["S"], "DERIVED", "PAID"),
        "M_derived_vs_paid": pair_test(dp, lambda d: d["approach"]["M"], "DERIVED", "PAID"),
        "r2_E_h_derived_vs_paid": pair_test(dp, lambda d: d["r2_E_h"], "DERIVED", "PAID"),
        "anticipation_all_both_regulate": pair_test(all_dp, anticipation2, "DERIVED", "PAID"),
        "combined_all_both_regulate": pair_test(all_dp, combined, "DERIVED", "PAID"),
        "decoder_failures": {k: sum(ds(s, k)["r2_D_h"] < DECODE_FAIL for s in seeds) for k in ARMS}}
    desc = {}
    for arm in ARMS:
        d = [ds(s, arm) for s in seeds]
        desc[arm] = {"anticipation_median": med(anticipation2(x) for x in d), "S_median": med(x["suppression"]["S"] for x in d),
                     "M_median": med(x["approach"]["M"] for x in d), "K_median": med(combined(x) for x in d),
                     "r2_E_h_median": med(x["r2_E_h"] for x in d), "flat": sum(bool(x["flat"]) for x in d),
                     "in_band_off_median": med(x["base"]["in_band"] for x in d),
                     "regulating_off": sum(regulates(x["intact"]) for x in d),
                     "regulating_off_shuffled": sum(regulates(x["shuffled"]) for x in d)}
    out["descriptive"] = desc
    return out


def report(sc):
    L = ["# Track C swap option R2: replication of derived against paid, with a relocation control", ""]
    reg, us = sc["regulators"], sc["usable"]
    L += [f"Seeds {sc['n_seeds']}. No-fate task accuracy {fmt(sc['nofate_accuracy_median'])} (learned: {sc['learned']}). "
          f"Regulators: derived {reg['DERIVED']}, paid {reg['PAID']}, paid with own relocation {reg['PAIDR']}, yoked "
          f"{reg['YOKED']}. Usable pairs (both regulate, in band within {MATCH_MAX}): derived/paid **{us['D_P']}**, "
          f"PAIDR/paid {us['R_P']}, derived/PAIDR {us['D_R']}.", "",
          "| arm | in band | rho | eat timing ratio | task accuracy | relocations | first sustained in band (episode) |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for k, a in sc["arms"].items():
        L.append(f"| {k} | {fmt(a['in_band_median'])} | {fmt(a['rho_median'], 2)} | {fmt(a['timing_ratio_median'], 1)} | "
                 f"{fmt(a['accuracy_median'])} | {fmt(a['relocations_median'], 0)} | {fmt(a['first_sustained_median'], 0)} |")
    c0 = sc["C0_regulation"]
    L += ["", f"**C0 (derived regulation, independent optimizers): {c0['label']}.** Derived regulators "
          f"{c0['derived_regulators']}/{c0['n']} (needed {c0['needed']}); yoked regulators {c0['yoked_regulators']} "
          f"(at most {C0_MAX_YOKED})."]
    if "C1_anticipation" not in sc:
        return "\n".join(L + ["", "Calibration: stage 1 only.", ""])
    row = lambda name, c: (f"| {name} | **{c['label']}** | {c['first_ahead']}/{c['n']} | {fmt(c['sign_p'], 4)} | "
                           f"{fmt(c['wilcoxon_p'], 4)} | {fmt(c['first_median'])} | {fmt(c['second_median'])} |")
    head = ["| comparison (first against second) | label | first ahead | sign p | Wilcoxon p | first median | second median |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    c2, c4 = sc["C2_flat"], sc["C4_relocation"]
    frow = lambda name, c: (f"| {name} | **{c['label']}** | {c['first_flat']}/{c['first_n']} | {c['second_flat']}/"
                            f"{c['second_n']} | {fmt(c['fisher_p'], 4)} |")
    L += ["", "## Claims", ""] + head
    L += [row("**C1 (primary)** anticipation index, derived against paid", sc["C1_anticipation"]),
          row("**C3** combined post-meal suppression K, derived against paid", sc["C3_combined"]),
          row("C4a K, PAIDR against paid", c4["paidr_vs_paid"]), row("C4b K, derived against PAIDR", c4["derived_vs_paidr"])]
    L += ["", f"**C4 (relocation control): {c4['label']}.**", "",
          "| flat eat readiness (first against second) | label | first | second | Fisher p |", "| --- | --- | --- | --- | --- |",
          frow("**C2** derived against paid", c2), frow("PAIDR against paid", c4["flat_paidr_vs_paid"]),
          frow("derived against PAIDR", c4["flat_derived_vs_paidr"])]
    hm = sc["holm_C1_C2_C3"]
    L += ["", "Holm-adjusted p over C1, C2, C3: " + ", ".join(f"{k.split('_')[0]} {fmt(v, 4)}" for k, v in hm.items()) + "."]
    sec = sc["secondary"]
    L += ["", "## Secondary (labels are descriptive)", ""] + head
    L += [row("S, derived against paid", sec["S_derived_vs_paid"]), row("M, derived against paid", sec["M_derived_vs_paid"]),
          row("R2(h -> E), derived against paid", sec["r2_E_h_derived_vs_paid"]),
          row("anticipation, all seeds where both regulate", sec["anticipation_all_both_regulate"]),
          row("K, all seeds where both regulate", sec["combined_all_both_regulate"]),
          row("anticipation, PAIDR against paid", c4["anticipation_paidr_vs_paid"]),
          row("anticipation, derived against PAIDR", c4["anticipation_derived_vs_paidr"])]
    L += ["", f"Decoder failures (held-out R2(h -> D) below {DECODE_FAIL}): "
          + ", ".join(f"{k} {v}" for k, v in sec["decoder_failures"].items()) + ".", "",
          "## Descriptive (all seeds, erasure off)", "",
          "| arm | anticipation | S | M | K | R2(h -> E) | flat | in band | regulating intact / shuffled |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for k, d in sc["descriptive"].items():
        L.append(f"| {k} | {fmt(d['anticipation_median'])} | {fmt(d['S_median'])} | {fmt(d['M_median'])} | {fmt(d['K_median'])} | "
                 f"{fmt(d['r2_E_h_median'])} | {d['flat']} | {fmt(d['in_band_off_median'])} | {d['regulating_off']} / "
                 f"{d['regulating_off_shuffled']} |")
    L += ["", "## Per seed (stage 1)", "",
          "| seed | in band derived / paid / PAIDR / yoked | regulator derived / paid / PAIDR | usable D-P / R-P / D-R |",
          "| --- | --- | --- | --- |"]
    yn = lambda b: "y" if b else "n"
    for s, x in sorted(sc["per_seed"].items(), key=lambda kv: int(kv[0])):
        b, r, u = x["in_band"], x["regulator"], x["usable"]
        L.append(f"| {s} | {b['DERIVED']:.2f} / {b['PAID']:.2f} / {b['PAIDR']:.2f} / {b['YOKED']:.2f} | "
                 f"{yn(r['DERIVED'])} / {yn(r['PAID'])} / {yn(r['PAIDR'])} | {yn(u['D_P'])} / {yn(u['R_P'])} / {yn(u['D_R'])} |")
    return "\n".join(L) + "\n"


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
        print(report(score(d["seeds"])))
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
    jobs = [(s, wcd, tcd, RATE, p2_iters, PAY, sizes, stages) for s in seeds]
    recs = []
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_seed2, jobs), 1):
            for arm, b in r["weights"].items():
                torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}.pt"))
            recs.append(strip(r))
            print(f"[seed {k}/{len(jobs)}] {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE, "pay": list(PAY), "p2_iters": p2_iters,
            "sizes": list(sizes), "seeds": seeds, "seconds": round(time.time() - t0, 1),
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "seeds": recs}, fh)
    sc = score(recs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print("regulators:", sc["regulators"], "usable:", sc["usable"])
    for k in ("C0_regulation", "C1_anticipation", "C2_flat", "C3_combined", "C4_relocation"):
        if k in sc:
            print(k, sc[k]["label"])


if __name__ == "__main__":
    main()
