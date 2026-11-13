"""Track C swap, option R3: a derived agent that is also paid, and a paid agent with a sparse payment.
Frozen runner and scorer.

    python run_trackc_paid3.py --mode final --out trackc_paid3     # once, after the freeze
    python run_trackc_paid3.py --mode calib --out <scratch dir>    # calibration seeds, stage 1 only
    python run_trackc_paid3.py --mode smoke --out <scratch dir>    # pipeline check
    python run_trackc_paid3.py --score trackc_paid3                # re-score saved raw results

Design, decision rules and disclosures: TRACKC_PAID3_PROTOCOL.md.
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

from run_trackc_paid import LEARNED, P2_ITERS, PAY, RATE, SIZES, WEAR, is_regulator, regulates, two_sided_sign
from run_trackc_paid2 import (ALPHA, C0_MAX_YOKED, C0_SHARE, DECODE_FAIL, MATCH_MAX, MIN_PAIRS, anticipation2, combined,
                              first_sustained, flat_test, holm, pair_test)
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.paid3 import run_seed3
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(1100, 1128))        # fresh; v1-v8 used 100-808, R 900-917, R2 1000-1027
CALIB_SEEDS = list(range(9300, 9304))        # calibration only, never scored
ARMS = ("DERIVED", "YOKED", "PAID", "DPAID", "PAIDS")
LUMP = (RATE, PAY[1] / RATE)                 # sparse payment: (rate, size); expected payment equals PAID's
# pair key: (first arm, second arm). Usable pair: both regulate and in band within MATCH_MAX.
PAIRS = {"D_P": ("DERIVED", "PAID"), "X_P": ("DPAID", "PAID"), "D_X": ("DERIVED", "DPAID"),
         "S_P": ("PAIDS", "PAID"), "D_S": ("DERIVED", "PAIDS")}
# Decision rules (frozen; protocol section 4). The regulator criterion, cell, payment, training length,
# downstream sizes, tests and thresholds are those of options R and R2, imported unchanged.
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py", "trackc_swap/relocate.py",
           "trackc_swap/probe.py", "trackc_swap/causal.py", "trackc_swap/paid.py", "trackc_swap/paid2.py",
           "trackc_swap/paid3.py", "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py",
           "run_trackc_paid3.py", "test_trackc_swap.py", "TRACKC_PAID3_PROTOCOL.md"]


def configs(mode):
    """(world, phase-1 train config, seeds, phase-2 updates, downstream sizes, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, P2_ITERS, SIZES, 2
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_SEEDS, P2_ITERS, SIZES, 1
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001],
            30, (16, 1, 1), 2)


def two_by_two(up, below, undetermined, labels):
    """Label of a control arm X from two tests on K: X above PAID (`up`), DERIVED above X (`below`).
    labels = (up only, below only, both)."""
    if undetermined:
        return "UNDETERMINED"
    return labels[2] if up and below else labels[0] if up else labels[1] if below else "UNDETERMINED"


def gap_closed(seeds, ds, per, arm):
    """Descriptive: where the arm's median K sits between PAID's (0) and DERIVED's (1), over seeds
    where DERIVED, PAID and the arm all regulate."""
    reg = [s for s in seeds if all(per[s["seed"]]["regulator"][k] for k in ("DERIVED", "PAID", arm))]
    k = {a: med(combined(ds(s, a)) for s in reg) for a in ("DERIVED", "PAID", arm)}
    if None in k.values() or k["DERIVED"] == k["PAID"]:
        return None
    return (k[arm] - k["PAID"]) / (k["DERIVED"] - k["PAID"])


def sooner(seeds, a, b):
    """Sign test: arm a reaches sustained regulation in training before arm b."""
    v = [(first_sustained(s["curves1"][a]["in_band"]), first_sustained(s["curves1"][b]["in_band"])) for s in seeds]
    v = [(x, y) for x, y in v if x is not None and y is not None and x != y]
    n, k = len(v), sum(x < y for x, y in v)
    return {"n": n, "first_sooner": k, "sign_p": two_sided_sign(k, n)}


def score(seeds):
    out = {"n_seeds": len(seeds),
           "nofate_accuracy_median": med(s["nofate"]["eval"]["best_response_rate"] for s in seeds)}
    out["learned"] = valid = out["nofate_accuracy_median"] >= LEARNED
    per = {}
    for s in seeds:
        e = s["stage1"]
        reg = {k: is_regulator(e[k], e["YOKED"]) for k in ARMS if k != "YOKED"}
        reg["YOKED"] = is_regulator(e["YOKED"], e["DERIVED"])
        match = lambda a, b: bool(reg[a] and reg[b] and abs(e[a]["in_band"] - e[b]["in_band"]) <= MATCH_MAX)
        per[s["seed"]] = {"regulator": reg, "in_band": {k: e[k]["in_band"] for k in ARMS},
                          "rho": {k: e[k]["rho"] for k in ARMS},
                          "usable": {key: match(a, b) for key, (a, b) in PAIRS.items()}}
    out["per_seed"] = per
    out["regulators"] = {k: sum(x["regulator"][k] for x in per.values()) for k in ARMS}
    out["usable"] = {k: sum(x["usable"][k] for x in per.values()) for k in PAIRS}
    need = ceil(C0_SHARE * len(seeds))
    out["E0_regulation"] = {
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
    out["lumps_median"] = med(s["lumps1"] for s in seeds)
    out["learning_speed"] = {f"{a}_vs_PAID": sooner(seeds, a, "PAID") for a in ("DERIVED", "DPAID", "PAIDS")}
    if not all("downstream" in s for s in seeds):
        return out                                           # calibration: stage 1 only
    ds = lambda s, k: s["downstream"][k]
    pairs = {key: [(ds(s, a), ds(s, b)) for s in seeds if per[s["seed"]]["usable"][key]] for key, (a, b) in PAIRS.items()}
    test = lambda key, f: pair_test(pairs[key], f, *PAIRS[key])
    regs = lambda *arms: [s for s in seeds if all(per[s["seed"]]["regulator"][k] for k in arms)]
    flat = lambda a, b: flat_test([ds(s, a) for s in regs(a, b)], [ds(s, b) for s in regs(a, b)], a, b)
    # E1 (check): the combined index K, derived against paid; R2's C3 on fresh seeds
    e1 = test("D_P", combined)
    out["E1_combined"] = e1
    read = e1["label"] == "DERIVED_AHEAD"
    # E2 (primary): the derived agent that is also paid
    x_p, d_x = test("X_P", combined), test("D_X", combined)
    out["E2_dependence"] = {
        "dpaid_vs_paid": x_p, "derived_vs_dpaid": d_x, "read": read,
        "label": two_by_two(x_p["label"] == "DPAID_AHEAD", d_x["label"] == "DERIVED_AHEAD",
                            "UNDETERMINED" in (x_p["label"], d_x["label"]),
                            ("DEPENDENCE_SUFFICES", "PAYMENT_PREVENTS", "BOTH_CONTRIBUTE")),
        "gap_closed": gap_closed(seeds, ds, per, "DPAID"),
        "flat_dpaid_vs_paid": flat("DPAID", "PAID"), "flat_derived_vs_dpaid": flat("DERIVED", "DPAID"),
        "anticipation_dpaid_vs_paid": test("X_P", anticipation2), "anticipation_derived_vs_dpaid": test("D_X", anticipation2)}
    # E3: the paid agent with a sparse payment
    s_p, d_s = test("S_P", combined), test("D_S", combined)
    out["E3_sparse"] = {
        "paids_vs_paid": s_p, "derived_vs_paids": d_s, "read": read,
        "label": two_by_two(s_p["label"] == "PAIDS_AHEAD", d_s["label"] == "DERIVED_AHEAD",
                            "UNDETERMINED" in (s_p["label"], d_s["label"]),
                            ("SPARSE_SUFFICES", "SPARSE_NOT_SUFFICIENT", "PARTIAL")),
        "gap_closed": gap_closed(seeds, ds, per, "PAIDS"),
        "flat_paids_vs_paid": flat("PAIDS", "PAID"), "flat_derived_vs_paids": flat("DERIVED", "PAIDS"),
        "anticipation_paids_vs_paid": test("S_P", anticipation2), "anticipation_derived_vs_paids": test("D_S", anticipation2)}
    if not valid:
        for k in ("E1_combined", "E2_dependence", "E3_sparse"):
            out[k]["label"] = "INVALID"
    h = holm([x_p["sign_p"], d_x["sign_p"], s_p["sign_p"], d_s["sign_p"]])
    out["holm_E2_E3"] = dict(zip(("dpaid_vs_paid", "derived_vs_dpaid", "paids_vs_paid", "derived_vs_paids"), h))
    # secondary and descriptive
    out["secondary"] = {
        "flat_derived_vs_paid": flat("DERIVED", "PAID"),
        "anticipation_derived_vs_paid": test("D_P", anticipation2),
        "S_derived_vs_paid": test("D_P", lambda d: d["suppression"]["S"]),
        "M_derived_vs_paid": test("D_P", lambda d: d["approach"]["M"]),
        "S_dpaid_vs_paid": test("X_P", lambda d: d["suppression"]["S"]),
        "M_dpaid_vs_paid": test("X_P", lambda d: d["approach"]["M"]),
        "S_paids_vs_paid": test("S_P", lambda d: d["suppression"]["S"]),
        "M_paids_vs_paid": test("S_P", lambda d: d["approach"]["M"]),
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
    L = ["# Track C swap option R3: a derived agent that is also paid, and a sparse payment", ""]
    reg, us = sc["regulators"], sc["usable"]
    L += [f"Seeds {sc['n_seeds']}. No-fate task accuracy {fmt(sc['nofate_accuracy_median'])} (learned: {sc['learned']}). "
          "Regulators: " + ", ".join(f"{k} {reg[k]}" for k in ARMS) + ". "
          f"Usable pairs (both regulate, in band within {MATCH_MAX}): "
          + ", ".join(f"{a}/{b} {us[k]}" for k, (a, b) in PAIRS.items()) + ". "
          f"Sparse penalties charged in training (median): {fmt(sc['lumps_median'], 0)}.", "",
          "| arm | in band | rho | eat timing ratio | task accuracy | relocations | first sustained in band (episode) |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for k, a in sc["arms"].items():
        L.append(f"| {k} | {fmt(a['in_band_median'])} | {fmt(a['rho_median'], 2)} | {fmt(a['timing_ratio_median'], 1)} | "
                 f"{fmt(a['accuracy_median'])} | {fmt(a['relocations_median'], 0)} | {fmt(a['first_sustained_median'], 0)} |")
    e0 = sc["E0_regulation"]
    L += ["", f"**E0 (derived regulation): {e0['label']}.** Derived regulators {e0['derived_regulators']}/{e0['n']} "
          f"(needed {e0['needed']}); yoked regulators {e0['yoked_regulators']} (at most {C0_MAX_YOKED}).", "",
          "Sustained regulation reached sooner than PAID: "
          + "; ".join(f"{k.split('_')[0]} {v['first_sooner']}/{v['n']} (p {fmt(v['sign_p'], 4)})"
                      for k, v in sc["learning_speed"].items()) + "."]
    if "E1_combined" not in sc:
        L += ["", "| seed | in band " + " / ".join(ARMS) + " | regulator " + " / ".join(a for a in ARMS if a != "YOKED") + " |",
              "| --- | --- | --- |"]
        for s, x in sorted(sc["per_seed"].items(), key=lambda kv: int(kv[0])):
            L.append(f"| {s} | " + " / ".join(f"{x['in_band'][a]:.2f}" for a in ARMS) + " | "
                     + " / ".join("y" if x["regulator"][a] else "n" for a in ARMS if a != "YOKED") + " |")
        return "\n".join(L + ["", "Calibration: stage 1 only.", ""])
    row = lambda name, c: (f"| {name} | **{c['label']}** | {c['first_ahead']}/{c['n']} | {fmt(c['sign_p'], 4)} | "
                           f"{fmt(c['wilcoxon_p'], 4)} | {fmt(c['first_median'])} | {fmt(c['second_median'])} |")
    head = ["| comparison (first against second) | label | first ahead | sign p | Wilcoxon p | first median | second median |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    frow = lambda name, c: (f"| {name} | **{c['label']}** | {c['first_flat']}/{c['first_n']} | {c['second_flat']}/"
                            f"{c['second_n']} | {fmt(c['fisher_p'], 4)} |")
    e2, e3, sec = sc["E2_dependence"], sc["E3_sparse"], sc["secondary"]
    L += ["", "## Claims (combined post-meal suppression K)", ""] + head
    L += [row("**E1 (check)** derived against paid", sc["E1_combined"]),
          row("**E2a** DPAID against paid", e2["dpaid_vs_paid"]), row("**E2b** derived against DPAID", e2["derived_vs_dpaid"]),
          row("**E3a** PAIDS against paid", e3["paids_vs_paid"]), row("**E3b** derived against PAIDS", e3["derived_vs_paids"])]
    L += ["", f"**E2 (primary; dependence with payment): {e2['label']}.** Share of the derived/paid gap in median K "
          f"closed by DPAID: {fmt(e2['gap_closed'], 2)}.", "",
          f"**E3 (sparse payment): {e3['label']}.** Share of the gap closed by PAIDS: {fmt(e3['gap_closed'], 2)}.", "",
          f"E2 and E3 are read: {e2['read']} (E1 must be DERIVED_AHEAD).", "",
          "Holm-adjusted p over the four tests of E2 and E3: "
          + ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm_E2_E3"].items()) + ".", "",
          "## Secondary (labels are descriptive)", "",
          "| flat eat readiness (first against second) | label | first | second | Fisher p |", "| --- | --- | --- | --- | --- |",
          frow("derived against paid", sec["flat_derived_vs_paid"]), frow("DPAID against paid", e2["flat_dpaid_vs_paid"]),
          frow("derived against DPAID", e2["flat_derived_vs_dpaid"]), frow("PAIDS against paid", e3["flat_paids_vs_paid"]),
          frow("derived against PAIDS", e3["flat_derived_vs_paids"]), ""] + head
    L += [row("anticipation, derived against paid", sec["anticipation_derived_vs_paid"]),
          row("anticipation, DPAID against paid", e2["anticipation_dpaid_vs_paid"]),
          row("anticipation, derived against DPAID", e2["anticipation_derived_vs_dpaid"]),
          row("anticipation, PAIDS against paid", e3["anticipation_paids_vs_paid"]),
          row("anticipation, derived against PAIDS", e3["anticipation_derived_vs_paids"]),
          row("S, derived against paid", sec["S_derived_vs_paid"]), row("M, derived against paid", sec["M_derived_vs_paid"]),
          row("S, DPAID against paid", sec["S_dpaid_vs_paid"]), row("M, DPAID against paid", sec["M_dpaid_vs_paid"]),
          row("S, PAIDS against paid", sec["S_paids_vs_paid"]), row("M, PAIDS against paid", sec["M_paids_vs_paid"])]
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
          "| seed | in band " + " / ".join(ARMS) + " | regulator " + " / ".join(a for a in ARMS if a != "YOKED")
          + " | usable " + " / ".join(PAIRS) + " |", "| --- | --- | --- | --- |"]
    yn = lambda b: "y" if b else "n"
    for s, x in sorted(sc["per_seed"].items(), key=lambda kv: int(kv[0])):
        L.append(f"| {s} | " + " / ".join(f"{x['in_band'][a]:.2f}" for a in ARMS) + " | "
                 + " / ".join(yn(x["regulator"][a]) for a in ARMS if a != "YOKED") + " | "
                 + " / ".join(yn(x["usable"][k]) for k in PAIRS) + " |")
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
    jobs = [(s, wcd, tcd, RATE, p2_iters, PAY, LUMP, sizes, stages) for s in seeds]
    recs = []
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_seed3, jobs), 1):
            for arm, b in r["weights"].items():
                torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}.pt"))
            recs.append(strip(r))
            print(f"[seed {k}/{len(jobs)}] {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE, "pay": list(PAY), "lump": list(LUMP),
            "p2_iters": p2_iters, "sizes": list(sizes), "seeds": seeds, "seconds": round(time.time() - t0, 1),
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
    for k in ("E0_regulation", "E1_combined", "E2_dependence", "E3_sparse"):
        if k in sc:
            print(k, sc[k]["label"])


if __name__ == "__main__":
    main()
