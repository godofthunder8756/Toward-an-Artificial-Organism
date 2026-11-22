"""Track C P3b: can the global body-grounded self-state become differentiated? (Layer 3 -> Layer 4)
Runner and scorer.

    python run_p3b_diff.py --mode final --out p3b_diff [--max-new 4]   # after the freeze
    python run_p3b_diff.py --mode calib --out <dir> [--max-new 4]     # calibration seeds (blind summary)
    python run_p3b_diff.py --mode smoke --out <scratch dir>           # pipeline check
    python run_p3b_diff.py --score p3b_diff                           # re-score saved raw results
    python run_p3b_diff.py --calib-summary <dir>                      # calibration summary: validity, own-side
                                                                      # referents; no cross-side, C or index

Finished jobs are kept in <out>/partial; --max-new N runs at most N unfinished jobs and stops.

Protocol and decision rules: P3B_DIFF_PROTOCOL.md. Simulated variables only; no operator-stop variable
exists in the world.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # one thread per worker
    os.environ.setdefault(_v, "1")

import argparse
import json
import platform
import sys
import time
from dataclasses import asdict
from math import ceil
from multiprocessing import Pool

import torch

from run_p1_selfeval import VALID_CLEAR_CORRECT, one_sample, regulates
from run_p1c_selfover import DAMAGE_MAX, EXPOSURE_MIN, MATCH_MAX
from run_p3_global import (cell, clear_correct_t, damage_t, diff, discrimination, noise_effect, phase1_usable,
                           retained)
from run_trackc_paid import P2_ITERS, PAY, WEAR
from run_trackc_paid2 import ALPHA, C0_SHARE, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.differentiate import LOOK_KINDS, REG_ITERS_D, WRONG_UNCLEAR_P1, run_seed_x
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.selfcomp import WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from trackc_swap.selfeval import DRAIN_SHIFT
from trackc_swap.selfover import ARMS_O, P_MAX_O, PROBE_GAIN_O, RATE_O, REL_BREAK_EVEN
from trackc_swap.train import TrainConfig
from trackc_swap.workspace import TYPE_P_MIXED, TYPES

ARMS = ARMS_O
FINAL_SEEDS = list(range(2400, 2428))
CALIB_SEEDS = list(range(10100, 10116))
CALIB_ROUND = list(range(10100, 10104))
POINTS = (P2_ITERS // 2, P2_ITERS)                  # 1800, 3600 (primary)
S_MIN = 0.50                                        # DIFFERENTIATED needs median selectivity >= this in PFATE
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/train.py", "trackc_swap/factorial.py",
           "trackc_swap/agent.py", "trackc_swap/selfeval.py", "trackc_swap/selfcomp.py", "trackc_swap/selfover.py",
           "trackc_swap/selfconf.py", "trackc_swap/workspace.py", "trackc_swap/differentiate.py",
           "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py", "run_p1_selfeval.py",
           "run_p1b_selfcomp.py", "run_p1c_selfover.py", "run_p3_global.py", "run_p3b_diff.py",
           "test_p3b_diff.py", "P3B_DIFF_PROTOCOL.md"]


def configs(mode):
    """(world, train config, seeds, points, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, 2
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_ROUND, POINTS, 1
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001], (10, 20), 2


# ---------------------------------------------------------------- measures
def look_effect(pt, arm, typ, kind):
    """Abstention on probed minus unprobed clear trials of a type under look_low ('low') or look_high ('high')."""
    k = f"probe_look_{kind}"
    return diff(cell(pt, k, arm, typ, "clear_drained"), cell(pt, k, arm, typ, "clear_plain"))


def evidence_effect_x(pt, arm, typ):
    k = "probe_look_low"
    return diff(cell(pt, k, arm, typ, "unclear_plain"), cell(pt, k, arm, typ, "clear_plain"))


def retained_x(pt, arm, typ):
    p = pt.get("probe_look_low", {}).get(arm, {}).get("probes", {}).get(typ)
    return None if not p else clear_correct_t(p)


def parts(pt, arm):
    e = {f"{t}_{k}": look_effect(pt, arm, t, k) for t in TYPES for k in ("low", "high")}
    a_half = diff(e["A_low"], e["A_high"])
    b_half = diff(e["B_high"], e["B_low"])
    d = None if a_half is None or b_half is None else a_half + b_half
    den = None if e["A_low"] is None or e["B_high"] is None else e["A_low"] + e["B_high"]
    s = None if d is None or den is None or den <= 0 else d / den
    g = None if e["A_high"] is None or e["B_low"] is None else 0.5 * (e["A_high"] + e["B_low"])
    c = None if e["C_low"] is None or e["C_high"] is None else 0.5 * (e["C_low"] + e["C_high"])
    return e | {"A_half": a_half, "B_half": b_half, "D": d, "S": s, "G": g, "C_mean": c}


def exposure_t(nat, typ):
    return nat["probes"][typ].get("clear_share_below_break_even")


# ---------------------------------------------------------------- tests
def score_point(seeds, i, stages):
    out = {"iters": seeds[0]["points"][i]["iters"]}
    per = {}
    for s in seeds:
        pt = s["points"][i]
        nat = pt["natural"]
        reg = {a: bool(regulates(nat[a])) for a in ARMS}
        x = {"regulator": reg, "in_band": {a: nat[a]["in_band"] for a in ARMS}}
        pa = {a: parts(pt, a) for a in ARMS}
        for key in pa["PFATE"]:
            x[key] = {a: pa[a][key] for a in ARMS}
        for t in TYPES:
            x[f"evidence_{t}"] = {a: evidence_effect_x(pt, a, t) for a in ARMS}
            x[f"retained_{t}"] = {a: retained_x(pt, a, t) for a in ARMS}
            x[f"discrimination_{t}"] = {a: discrimination(nat[a], t) for a in ARMS}
            if stages >= 2:
                x[f"noise_{t}"] = {a: noise_effect(pt, a, t) for a in ARMS}
        per[s["seed"]] = x
    out["per_seed"] = per
    out["regulators"] = {a: sum(x["regulator"][a] for x in per.values()) for a in ARMS}
    need = ceil(C0_SHARE * len(seeds))
    ya = sum((x["evidence_A"]["PYOKED"] or 0) > 0 for x in per.values())
    yb = sum((x["evidence_B"]["PYOKED"] or 0) > 0 for x in per.values())
    ret = {f"{t}_{a}": med(x[f"retained_{t}"][a] for x in per.values()) for t in ("A", "B") for a in ARMS}
    out["P3B_0_gate"] = {"yoked_A_evidence_positive": ya, "yoked_B_evidence_positive": yb, "n": len(per),
                         "needed": need, "retained_median": ret}
    out["P3B_0_gate"]["label"] = ("PASS" if ya >= need and yb >= need and all(v is not None and v >= 0.6 for v in ret.values())
                                  else "FAIL")
    ident = lambda v: v
    P = lambda key, a, b: [(per[s["seed"]][key][a], per[s["seed"]][key][b]) for s in seeds]
    out["P3B_0_referent_A"] = pair_test(P("A_low", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    out["P3B_0_referent_B"] = pair_test(P("B_high", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    m = lambda arm, f: med(f(s["points"][i]["natural"][arm]) for s in seeds)
    out["arms"] = {a: {"in_band": m(a, lambda e: e["in_band"]), "abstain": m(a, lambda e: e["abstain_rate"]),
                       "mean_gain": m(a, lambda e: e["mean_gain"]),
                       "below_break_even_A": m(a, lambda e: exposure_t(e, "A")),
                       "below_break_even_B": m(a, lambda e: exposure_t(e, "B"))} for a in ARMS}
    keys = (["A_low", "A_high", "B_low", "B_high", "C_low", "C_high", "A_half", "B_half", "D", "S", "G", "C_mean"]
            + [f"{k}_{t}" for k in ("evidence", "retained", "discrimination") for t in TYPES]
            + ([f"noise_{t}" for t in TYPES] if stages >= 2 else []))
    for a in ARMS:
        for k in keys:
            out["arms"][a][k] = med(x[k][a] for x in per.values())
    if stages < 2:
        return out
    one = lambda key, arm, hi, lo: one_sample([x[key][arm] for x in per.values()], hi, lo)
    out["P3B_1"] = one("D", "PFATE", "DIFFERENTIATED", "REVERSED")
    out["P3B_2"] = pair_test(P("D", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    out["P3B_A"] = one("A_half", "PFATE", "PRESENT", "REVERSED")
    out["P3B_B"] = one("B_half", "PFATE", "PRESENT", "REVERSED")
    out["selectivity_PFATE"] = med(x["S"]["PFATE"] for x in per.values())
    B = lambda a, b: [(per[s["seed"]]["in_band"][a], per[s["seed"]]["in_band"][b]) for s in seeds]
    out["secondary"] = {
        "G_cross_side_PFATE_vs_PYOKED": pair_test(P("G", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "G_cross_side_PFATE_vs_PNOFATE": pair_test(P("G", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "C_low_PFATE_vs_PYOKED": pair_test(P("C_low", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "C_high_PFATE_vs_PYOKED": pair_test(P("C_high", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "A_low_PFATE_vs_PNOFATE": pair_test(P("A_low", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "B_high_PFATE_vs_PNOFATE": pair_test(P("B_high", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "D_PFATE_vs_PNOFATE": pair_test(P("D", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "A_discrimination_PFATE_vs_PYOKED": pair_test(P("discrimination_A", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "B_discrimination_PFATE_vs_PYOKED": pair_test(P("discrimination_B", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "D_route": {a: one("D", a, "DIFFERENTIATED", "REVERSED") for a in ARMS},
        "look_routes": {k: {a: one(k, a, "PRESENT", "REVERSED") for a in ARMS}
                        for k in ("A_low", "A_high", "B_low", "B_high", "C_low", "C_high")},
        "monitor_route": {t: {a: one(f"noise_{t}", a, "PRESENT", "REVERSED") for a in ARMS} for t in ("A", "B")},
        "regulation_PFATE_vs_PNOFATE": pair_test(B("PFATE", "PNOFATE"), ident, "FATE", "HOST"),
        "regulation_PFATE_vs_PYOKED": pair_test(B("PFATE", "PYOKED"), ident, "FATE", "YOKED")}
    return out


def overall(sc):
    p = sc["points"][str(sc["primary_at"])]
    if not sc["valid"]:
        return "INVALID"
    if (p["P3B_0_gate"]["label"] != "PASS" or p["P3B_0_referent_A"]["label"] != "DERIVED_AHEAD"
            or p["P3B_0_referent_B"]["label"] != "DERIVED_AHEAD"):
        return "UNDETERMINED"
    l1, l2 = p["P3B_1"]["label"], p["P3B_2"]["label"]
    if "UNDETERMINED" in (l1, l2):
        return "UNDETERMINED"
    if l1 == "DIFFERENTIATED":
        full = (l2 == "DERIVED_AHEAD" and p["P3B_A"]["label"] == "PRESENT" and p["P3B_B"]["label"] == "PRESENT"
                and p["selectivity_PFATE"] is not None and p["selectivity_PFATE"] >= S_MIN)
        return "DIFFERENTIATED" if full else "PARTLY_DIFFERENTIATED"
    return "UNDIFFERENTIATED"


def phase1_validity(seeds):
    out = {f"clear_correct_{t}": med(clear_correct_t(s["phase1"]["PLAIN"]["probes"][t]) for s in seeds) for t in TYPES}
    out["damage_A"] = med(damage_t(s["phase1"]["PLAIN"]["probes"]["A"]) for s in seeds)
    out["damage_B"] = med(damage_t(s["phase1"]["PLAIN"]["probes"]["B"]) for s in seeds)
    return out


def score(seeds, stages=2):
    pts = [p["iters"] for p in seeds[0]["points"]]
    use = [s for s in seeds if phase1_usable(s)]
    sc = {"n_seeds": len(seeds), "n_usable": len(use), "excluded_seeds": [s["seed"] for s in seeds if not phase1_usable(s)],
          "points_at": pts, "primary_at": pts[-1], "params": seeds[0]["params"], "phase1": phase1_validity(seeds)}
    if not use:
        sc.update({"valid": False, "valid_memory": False, "valid_damage": False, "valid_exposure": False,
                   "exposure_median": {"A": None, "B": None}, "points": {}})
        if stages >= 2:
            sc.update({"overall": "INVALID", "holm": {k: None for k in ("P3B_1", "P3B_2", "P3B_A", "P3B_B")}, "weak": False})
        return sc
    sc["points"] = {str(p): score_point(use, i, stages) for i, p in enumerate(pts)}
    i_pri = len(pts) - 1
    sc["exposure_median"] = {t: med(exposure_t(s["points"][i_pri]["natural"]["PFATE"], t) for s in use) for t in ("A", "B")}
    v = sc["phase1"]
    sc["valid_memory"] = all(v[f"clear_correct_{t}"] is not None and v[f"clear_correct_{t}"] >= VALID_CLEAR_CORRECT
                             for t in TYPES)
    sc["valid_damage"] = all(v[k] is not None and v[k] <= DAMAGE_MAX for k in ("damage_A", "damage_B"))
    sc["valid_exposure"] = all(x is not None and x >= EXPOSURE_MIN for x in sc["exposure_median"].values())
    sc["valid"] = sc["valid_memory"] and sc["valid_damage"] and sc["valid_exposure"]
    if stages >= 2:
        p = sc["points"][str(sc["primary_at"])]
        sc["overall"] = overall(sc)
        names = ("P3B_1", "P3B_2", "P3B_A", "P3B_B")
        sc["holm"] = dict(zip(names, holm([p[k]["sign_p"] for k in names])))
        need = {"DIFFERENTIATED": names, "PARTLY_DIFFERENTIATED": ("P3B_1",)}
        sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
    return sc


# ---------------------------------------------------------------- report
def _pt(r):
    if "first_ahead" in r:
        return f"{r['first_ahead']}/{r['n']} (p {fmt(r['sign_p'], 4)}; {fmt(r['first_median'])} against {fmt(r['second_median'])}) {r['label']}"
    return f"{r['positive']}/{r['n']} (p {fmt(r['sign_p'], 4)}; median {fmt(r['median'])}) {r['label']}"


def report(sc, stages=2):
    L = ["# Track C P3b: differentiation of the body-grounded self-state (Layer 3 -> Layer 4)", ""]
    if stages >= 2:
        h = sc["holm"]
        L += [f"**Overall: {sc['overall']}**{' (weak)' if sc['weak'] else ''}. Holm-adjusted p: "
              + ", ".join(f"{k} {fmt(h[k], 4)}" for k in ("P3B_1", "P3B_2", "P3B_A", "P3B_B")) + ".", ""]
    v = sc["phase1"]
    em = sc["exposure_median"]
    L += [f"Valid: {sc['valid']} (phase 1 clear correct A / B / C {fmt(v['clear_correct_A'])} / {fmt(v['clear_correct_B'])} / "
          f"{fmt(v['clear_correct_C'])}, needed >= {VALID_CLEAR_CORRECT}; overwrite-probe accuracy A / B {fmt(v['damage_A'])} / "
          f"{fmt(v['damage_B'])}, needed <= {DAMAGE_MAX}; PFATE clear trials below break-even A / B {fmt(em['A'])} / "
          f"{fmt(em['B'])}, needed >= {EXPOSURE_MIN} each). Parameters: {sc['params']['PLAIN']}.", "",
          f"Usable seeds (phase 1 learned every type): {sc['n_usable']} of {sc['n_seeds']}; excluded: "
          f"{sc['excluded_seeds'] or 'none'}. Every test below is on the usable seeds.", ""]
    if not sc["points"]:
        return "\n".join(L + ["No usable seed: nothing is tested."])
    cols = ["in_band", "A_low", "A_high", "B_low", "B_high", "C_low", "C_high", "D", "S", "G", "retained_A", "retained_B",
            "retained_C", "discrimination_A", "discrimination_B"] + (["noise_A", "noise_B"] if stages >= 2 else [])
    L += ["| updates | arm | " + " | ".join(cols) + " |", "| --- | --- | " + " | ".join("---" for _ in cols) + " |"]
    for p in sc["points_at"]:
        P = sc["points"][str(p)]
        for a in ARMS:
            L.append(f"| {p} | {a} | " + " | ".join(fmt(P["arms"][a].get(c)) for c in cols) + " |")
    L.append("")
    for p in sc["points_at"]:
        P = sc["points"][str(p)]
        g = P["P3B_0_gate"]
        L += [f"At {p}: regulators {P['regulators']}; gate {g['label']} (yoked evidence effect positive A "
              f"{g['yoked_A_evidence_positive']}/{g['n']}, B {g['yoked_B_evidence_positive']}/{g['n']}, needed {g['needed']}; "
              f"retained medians { {k: fmt(x) for k, x in g['retained_median'].items()} }, needed >= 0.6).",
              f"- P3B-0 referent A (look_low on A), PFATE against PYOKED: {_pt(P['P3B_0_referent_A'])}",
              f"- P3B-0 referent B (look_high on B), PFATE against PYOKED: {_pt(P['P3B_0_referent_B'])}"]
        if stages >= 2:
            L += [f"- P3B-1 differentiation index D in PFATE: {_pt(P['P3B_1'])}",
                  f"- P3B-2 D, PFATE against PYOKED: {_pt(P['P3B_2'])}",
                  f"- P3B-A A half (A_low - A_high) in PFATE: {_pt(P['P3B_A'])}",
                  f"- P3B-B B half (B_high - B_low) in PFATE: {_pt(P['P3B_B'])}",
                  f"- Selectivity S in PFATE, median: {fmt(P['selectivity_PFATE'])} (needed >= {S_MIN} for DIFFERENTIATED)"]
            for k, r in P["secondary"].items():
                if k in ("D_route",):
                    L.append(f"- {k}: " + "; ".join(f"{a} {_pt(x)}" for a, x in r.items()))
                elif k in ("look_routes", "monitor_route"):
                    for t, rr in r.items():
                        L.append(f"- {k} {t}: " + "; ".join(f"{a} {_pt(x)}" for a, x in rr.items()))
                else:
                    L.append(f"- {k}: {_pt(r)}")
        L.append("")
    return "\n".join(L)


def calib_summary(seeds):
    """Calibration (blind): validity, usability, retention, evidence effects, the own-side referents (A_low, B_high),
    exposure per side, regulation. No cross-side effect, C effect, index or selectivity is computed or printed."""
    L = ["# P3b calibration summary (blind to cross-side, C and differentiation measures)", ""]
    v = phase1_validity(seeds)
    L.append("phase 1: " + ", ".join(f"{k} {fmt(x)}" for k, x in v.items()))
    L.append("usable: " + ", ".join(f"{s['seed']} {phase1_usable(s)}" for s in seeds))
    for i, p in enumerate(seeds[0]["points_at"]):
        L.append(f"## {p}")
        for s in seeds:
            pt = s["points"][i]
            nat = pt["natural"]
            row = [f"seed {s['seed']}"]
            for a in ARMS:
                row.append(f"{a}: band {fmt(nat[a]['in_band'])} A_low {fmt(look_effect(pt, a, 'A', 'low'))} "
                           f"B_high {fmt(look_effect(pt, a, 'B', 'high'))} "
                           f"ret A/B/C {fmt(retained_x(pt, a, 'A'))}/{fmt(retained_x(pt, a, 'B'))}/{fmt(retained_x(pt, a, 'C'))} "
                           f"evid A/B/C {fmt(evidence_effect_x(pt, a, 'A'))}/{fmt(evidence_effect_x(pt, a, 'B'))}/"
                           f"{fmt(evidence_effect_x(pt, a, 'C'))}")
            row.append(f"exposure A/B {fmt(exposure_t(nat['PFATE'], 'A'))}/{fmt(exposure_t(nat['PFATE'], 'B'))}")
            L.append(" | ".join(row))
    for s in seeds:
        p1 = s["phase1"]["PLAIN"]["probes"]
        L.append(f"phase 1 seed {s['seed']} (clear abstain / correct-given-report / unclear abstain): " + "  ".join(
            f"{t} {fmt(p1[t]['clear_plain']['abstain'])}/{fmt(p1[t]['clear_plain']['correct_given_report'])}/"
            f"{fmt(p1[t]['unclear_plain']['abstain'])}" for t in TYPES))
    return "\n".join(L)


def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "calib", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    ap.add_argument("--calib-summary")
    ap.add_argument("--max-new", type=int, default=0, help="run at most this many unfinished jobs, then stop (0: all)")
    args = ap.parse_args()
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        st = d["meta"]["stages"]
        print(report(score(d["seeds"], st), st))
        return
    if args.calib_summary:
        pdir = os.path.join(args.calib_summary, "partial")
        recs = [json.load(open(os.path.join(pdir, f))) for f in sorted(os.listdir(pdir))]
        print(calib_summary(recs))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, points, stages = configs(args.mode)
    wcd, tcd = asdict(wc), asdict(tc)
    wdir, pdir = os.path.join(args.out, "weights"), os.path.join(args.out, "partial")
    os.makedirs(wdir, exist_ok=True)
    os.makedirs(pdir, exist_ok=True)
    reg = REG_ITERS_D if args.mode != "smoke" else 10
    warm = WARM_ITERS_C if args.mode != "smoke" else 5
    jobs = [(s, wcd, tcd, list(points), PAY[1], stages, warm, WARM_WRONG_C, reg) for s in seeds]
    ppath = lambda seed: os.path.join(pdir, f"seed{seed}.json")
    recs, todo = [], []
    for job in jobs:
        if os.path.exists(ppath(job[0])):
            with open(ppath(job[0])) as fh:
                recs.append(json.load(fh))
        else:
            todo.append(job)
    done = len(jobs) - len(todo)
    if done:
        print(f"resuming: {done} of {len(jobs)} jobs already finished", flush=True)
    if args.max_new:
        todo = todo[:args.max_new]
    t0 = time.time()
    if todo:
        with Pool(min(len(todo), os.cpu_count() or 1)) as pool:
            for k, r in enumerate(pool.imap_unordered(run_seed_x, todo), done + 1):
                for name, b in r["weights"].items():
                    arm, p = name.split("@")
                    torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}_{p}.pt"))
                r = json.loads(json.dumps(strip(r), default=float))
                with open(ppath(r["seed"]) + ".tmp", "w") as fh:
                    json.dump(r, fh)
                os.replace(ppath(r["seed"]) + ".tmp", ppath(r["seed"]))
                recs.append(r)
                print(f"[job {k}/{len(jobs)}] seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    if len(recs) < len(jobs):
        print(f"stopped after this batch: {len(recs)} of {len(jobs)} jobs finished", flush=True)
        return
    recs.sort(key=lambda r: r["seed"])
    if args.mode == "calib":
        print(calib_summary(recs))
        return
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE_O, "probe_gain": PROBE_GAIN_O,
            "rel_break_even": REL_BREAK_EVEN, "p_max": P_MAX_O, "probe_shift": DRAIN_SHIFT, "look_kinds": list(LOOK_KINDS),
            "type_p": list(TYPE_P_MIXED), "wrong_ramp": WRONG_RAMP_C, "wrong_unclear_phase1": WRONG_UNCLEAR_P1,
            "reg_iters_phase1": reg, "warm_iters": warm, "warm_wrong": WARM_WRONG_C, "pay": PAY[1], "drive_all_arms": True,
            "points": list(points), "stages": stages, "seeds": seeds,
            "seconds": round(sum(r["seconds"] for r in recs), 1), "resumed_jobs": done,
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "seeds": recs}, fh)
    sc = score(recs, stages)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc, stages))
    print(report(sc, stages))


if __name__ == "__main__":
    main()
