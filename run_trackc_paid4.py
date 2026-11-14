"""Track C swap, option R4: a paid agent with undisturbed memory, and a derived agent that also
receives replayed erasures. Frozen runner and scorer.

    python run_trackc_paid4.py --mode final --out trackc_paid4     # once, after the freeze
    python run_trackc_paid4.py --mode calib --out <scratch dir>    # calibration seeds, stage 1 only
    python run_trackc_paid4.py --mode smoke --out <scratch dir>    # pipeline check
    python run_trackc_paid4.py --score trackc_paid4                # re-score saved raw results

Design, decision rules and disclosures: TRACKC_PAID4_PROTOCOL.md.
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
from trackc_swap.paid4 import run_seed4
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(1200, 1228))        # fresh; v1-v8 used 100-808, R 900-917, R2 1000-1027, R3 1100-1127
CALIB_SEEDS = list(range(9400, 9404))        # calibration only, never scored
ARMS = ("DERIVED", "YOKED", "PAID", "PAID0", "DNOISE")
# pair key: (first arm, second arm). Usable pair: both regulate and in band within MATCH_MAX.
PAIRS = {"D_P": ("DERIVED", "PAID"), "Z_P": ("PAID0", "PAID"), "D_Z": ("DERIVED", "PAID0"),
         "N_P": ("DNOISE", "PAID"), "D_N": ("DERIVED", "DNOISE")}
# Decision rules (frozen; protocol section 4). The regulator criterion, cell, payment, training length,
# downstream sizes, tests and thresholds are those of options R, R2 and R3, imported unchanged.
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py", "trackc_swap/relocate.py",
           "trackc_swap/probe.py", "trackc_swap/causal.py", "trackc_swap/paid.py", "trackc_swap/paid2.py",
           "trackc_swap/paid4.py", "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py",
           "run_trackc_paid4.py", "test_trackc_swap.py", "TRACKC_PAID4_PROTOCOL.md"]


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
    out["F0_regulation"] = {
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
    out["learning_speed"] = {f"{a}_vs_PAID": sooner(seeds, a, "PAID") for a in ("DERIVED", "PAID0", "DNOISE")}
    if not all("downstream" in s for s in seeds):
        return out                                           # calibration: stage 1 only
    ds = lambda s, k: s["downstream"][k]
    pairs = {key: [(ds(s, a), ds(s, b)) for s in seeds if per[s["seed"]]["usable"][key]] for key, (a, b) in PAIRS.items()}
    test = lambda key, f: pair_test(pairs[key], f, *PAIRS[key])
    regs = lambda *arms: [s for s in seeds if all(per[s["seed"]]["regulator"][k] for k in arms)]
    flat = lambda a, b: flat_test([ds(s, a) for s in regs(a, b)], [ds(s, b) for s in regs(a, b)], a, b)
    # F1 (check): the combined index K, derived against paid; R2's C3 and R3's E1 on fresh seeds
    f1 = test("D_P", combined)
    out["F1_combined"] = f1
    read = f1["label"] == "DERIVED_AHEAD"
    # F2 (primary): the paid agent whose memory is never erased
    z_p, d_z = test("Z_P", combined), test("D_Z", combined)
    out["F2_undisturbed"] = {
        "paid0_vs_paid": z_p, "derived_vs_paid0": d_z, "read": read,
        "label": two_by_two(z_p["label"] == "PAID0_AHEAD", d_z["label"] == "DERIVED_AHEAD",
                            "UNDETERMINED" in (z_p["label"], d_z["label"]),
                            ("REPLAY_EXPLAINS", "REPLAY_DOES_NOT_EXPLAIN", "REPLAY_EXPLAINS_PART")),
        "gap_closed": gap_closed(seeds, ds, per, "PAID0"),
        "flat_paid0_vs_paid": flat("PAID0", "PAID"), "flat_derived_vs_paid0": flat("DERIVED", "PAID0"),
        "anticipation_paid0_vs_paid": test("Z_P", anticipation2), "anticipation_derived_vs_paid0": test("D_Z", anticipation2)}
    # F3: the derived agent that also receives the replayed erasures
    n_p, d_n = test("N_P", combined), test("D_N", combined)
    out["F3_added_replay"] = {
        "dnoise_vs_paid": n_p, "derived_vs_dnoise": d_n, "read": read,
        "label": two_by_two(n_p["label"] == "DNOISE_AHEAD", d_n["label"] == "DERIVED_AHEAD",
                            "UNDETERMINED" in (n_p["label"], d_n["label"]),
                            ("REPLAY_HARMLESS", "REPLAY_REMOVES", "REPLAY_REDUCES")),
        "gap_closed": gap_closed(seeds, ds, per, "DNOISE"),
        "flat_dnoise_vs_paid": flat("DNOISE", "PAID"), "flat_derived_vs_dnoise": flat("DERIVED", "DNOISE"),
        "anticipation_dnoise_vs_paid": test("N_P", anticipation2), "anticipation_derived_vs_dnoise": test("D_N", anticipation2)}
    if not valid:
        for k in ("F1_combined", "F2_undisturbed", "F3_added_replay"):
            out[k]["label"] = "INVALID"
    h = holm([z_p["sign_p"], d_z["sign_p"], n_p["sign_p"], d_n["sign_p"]])
    out["holm_F2_F3"] = dict(zip(("paid0_vs_paid", "derived_vs_paid0", "dnoise_vs_paid", "derived_vs_dnoise"), h))
    # secondary and descriptive
    out["secondary"] = {
        "flat_derived_vs_paid": flat("DERIVED", "PAID"),
        "anticipation_derived_vs_paid": test("D_P", anticipation2),
        "S_derived_vs_paid": test("D_P", lambda d: d["suppression"]["S"]),
        "M_derived_vs_paid": test("D_P", lambda d: d["approach"]["M"]),
        "S_paid0_vs_paid": test("Z_P", lambda d: d["suppression"]["S"]),
        "M_paid0_vs_paid": test("Z_P", lambda d: d["approach"]["M"]),
        "S_derived_vs_paid0": test("D_Z", lambda d: d["suppression"]["S"]),
        "M_derived_vs_paid0": test("D_Z", lambda d: d["approach"]["M"]),
        "S_derived_vs_dnoise": test("D_N", lambda d: d["suppression"]["S"]),
        "M_derived_vs_dnoise": test("D_N", lambda d: d["approach"]["M"]),
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
    L = ["# Track C swap option R4: a paid agent with undisturbed memory, and a derived agent with added replayed erasures", ""]
    reg, us = sc["regulators"], sc["usable"]
    L += [f"Seeds {sc['n_seeds']}. No-fate task accuracy {fmt(sc['nofate_accuracy_median'])} (learned: {sc['learned']}). "
          "Regulators: " + ", ".join(f"{k} {reg[k]}" for k in ARMS) + ". "
          f"Usable pairs (both regulate, in band within {MATCH_MAX}): "
          + ", ".join(f"{a}/{b} {us[k]}" for k, (a, b) in PAIRS.items()) + ".", "",
          "| arm | in band | rho | eat timing ratio | task accuracy | relocations | first sustained in band (episode) |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for k, a in sc["arms"].items():
        L.append(f"| {k} | {fmt(a['in_band_median'])} | {fmt(a['rho_median'], 2)} | {fmt(a['timing_ratio_median'], 1)} | "
                 f"{fmt(a['accuracy_median'])} | {fmt(a['relocations_median'], 0)} | {fmt(a['first_sustained_median'], 0)} |")
    f0 = sc["F0_regulation"]
    L += ["", f"**F0 (derived regulation): {f0['label']}.** Derived regulators {f0['derived_regulators']}/{f0['n']} "
          f"(needed {f0['needed']}); yoked regulators {f0['yoked_regulators']} (at most {C0_MAX_YOKED}).", "",
          "Sustained regulation reached sooner than PAID: "
          + "; ".join(f"{k.split('_')[0]} {v['first_sooner']}/{v['n']} (p {fmt(v['sign_p'], 4)})"
                      for k, v in sc["learning_speed"].items()) + "."]
    if "F1_combined" not in sc:
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
    f2, f3, sec = sc["F2_undisturbed"], sc["F3_added_replay"], sc["secondary"]
    L += ["", "## Claims (combined post-meal suppression K)", ""] + head
    L += [row("**F1 (check)** derived against paid", sc["F1_combined"]),
          row("**F2a** PAID0 against paid", f2["paid0_vs_paid"]), row("**F2b** derived against PAID0", f2["derived_vs_paid0"]),
          row("**F3a** DNOISE against paid", f3["dnoise_vs_paid"]), row("**F3b** derived against DNOISE", f3["derived_vs_dnoise"])]
    L += ["", f"**F2 (primary; paid with undisturbed memory): {f2['label']}.** Share of the derived/paid gap in median K "
          f"closed by PAID0: {fmt(f2['gap_closed'], 2)}.", "",
          f"**F3 (derived with added replayed erasures): {f3['label']}.** Share of the gap kept by DNOISE: "
          f"{fmt(f3['gap_closed'], 2)}.", "",
          f"F2 and F3 are read: {f2['read']} (F1 must be DERIVED_AHEAD).", "",
          "Holm-adjusted p over the four tests of F2 and F3: "
          + ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm_F2_F3"].items()) + ".", "",
          "## Secondary (labels are descriptive)", "",
          "| flat eat readiness (first against second) | label | first | second | Fisher p |", "| --- | --- | --- | --- | --- |",
          frow("derived against paid", sec["flat_derived_vs_paid"]), frow("PAID0 against paid", f2["flat_paid0_vs_paid"]),
          frow("derived against PAID0", f2["flat_derived_vs_paid0"]), frow("DNOISE against paid", f3["flat_dnoise_vs_paid"]),
          frow("derived against DNOISE", f3["flat_derived_vs_dnoise"]), ""] + head
    L += [row("anticipation, derived against paid", sec["anticipation_derived_vs_paid"]),
          row("anticipation, PAID0 against paid", f2["anticipation_paid0_vs_paid"]),
          row("anticipation, derived against PAID0", f2["anticipation_derived_vs_paid0"]),
          row("anticipation, DNOISE against paid", f3["anticipation_dnoise_vs_paid"]),
          row("anticipation, derived against DNOISE", f3["anticipation_derived_vs_dnoise"]),
          row("S, derived against paid", sec["S_derived_vs_paid"]), row("M, derived against paid", sec["M_derived_vs_paid"]),
          row("S, PAID0 against paid", sec["S_paid0_vs_paid"]), row("M, PAID0 against paid", sec["M_paid0_vs_paid"]),
          row("S, derived against PAID0", sec["S_derived_vs_paid0"]), row("M, derived against PAID0", sec["M_derived_vs_paid0"]),
          row("S, derived against DNOISE", sec["S_derived_vs_dnoise"]), row("M, derived against DNOISE", sec["M_derived_vs_dnoise"])]
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
    jobs = [(s, wcd, tcd, RATE, p2_iters, PAY, sizes, stages) for s in seeds]
    recs = []
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_seed4, jobs), 1):
            for arm, b in r["weights"].items():
                torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}.pt"))
            recs.append(strip(r))
            print(f"[seed {k}/{len(jobs)}] {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE, "pay": list(PAY),
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
    for k in ("F0_regulation", "F1_combined", "F2_undisturbed", "F3_added_replay"):
        if k in sc:
            print(k, sc[k]["label"])


if __name__ == "__main__":
    main()
