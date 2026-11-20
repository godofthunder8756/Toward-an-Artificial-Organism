"""Track C P3: is the body-grounded self-state globally available? (Layer 0 -> Layer 3). Runner and scorer.

    python run_p3_global.py --mode final --out p3_global [--max-new 4]   # after the freeze
    python run_p3_global.py --mode calib --out <dir> [--max-new 4]      # calibration seeds (blind summary)
    python run_p3_global.py --mode smoke --out <scratch dir>            # pipeline check
    python run_p3_global.py --score p3_global                           # re-score saved raw results
    python run_p3_global.py --calib-summary <dir>                       # calibration summary: validity and the
                                                                        # A referent only; no B or C probe effect

Finished jobs are kept in <out>/partial; --max-new N runs at most N unfinished jobs and stops.

Protocol and decision rules: P3_GLOBAL_PROTOCOL.md. Simulated variables only; no operator-stop variable
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
from run_trackc_paid import P2_ITERS, PAY, WEAR
from run_trackc_paid2 import ALPHA, C0_SHARE, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from trackc_swap.selfeval import DRAIN_SHIFT
from trackc_swap.selfover import ARMS_O, P_MAX_O, PROBE_GAIN_O, RATE_O, REL_BREAK_EVEN
from trackc_swap.train import TrainConfig
from trackc_swap.workspace import RAMP_DOWN_W, REG_ITERS_W, REHEARSE_EVERY_W, WRONG_PEAK_W, TYPE_P_A, TYPE_P_MIXED, TYPES, run_seed_w

ARMS = ARMS_O
FINAL_SEEDS = list(range(2200, 2228))
CALIB_SEEDS = list(range(9980, 9996))
CALIB_ROUND = list(range(9988, 9992))   # round 1: 9980-9983; round 2: 9984-9987 (protocol section 3)
POINTS = (P2_ITERS // 2, P2_ITERS)                  # 1800, 3600 (primary), as P1c and P1d
RETAIN_MIN = 0.60                                   # B must still be answered: clear correct-report rate, every arm
TRANSFER_MIN = 0.20                                 # GLOBAL needs PFATE's B worse effect >= this share of its A effect
PHASE2_TYPES = TYPE_P_A
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/train.py", "trackc_swap/factorial.py",
           "trackc_swap/agent.py", "trackc_swap/selfeval.py", "trackc_swap/selfcomp.py", "trackc_swap/selfover.py",
           "trackc_swap/selfconf.py", "trackc_swap/workspace.py", "run_trackc_probe.py", "run_trackc_paid.py",
           "run_trackc_paid2.py", "run_p1_selfeval.py", "run_p1b_selfcomp.py", "run_p1c_selfover.py",
           "run_p1d_confirm.py", "run_p3_global.py", "test_p3_global.py", "P3_GLOBAL_PROTOCOL.md"]


def configs(mode):
    """(world, train config, seeds, points, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, 2
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_ROUND, POINTS, 1
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001], (10, 20), 2


# ---------------------------------------------------------------- measures
def cell(pt, kind, arm, typ, key, field="abstain"):
    c = pt.get(kind, {}).get(arm, {}).get("probes", {}).get(typ, {}).get(key)
    return None if c is None else c[field]


def diff(a, b):
    return None if a is None or b is None else a - b


def worse_effect(pt, arm, typ):
    """Abstention on worse-probed minus unprobed clear trials of a type (overwrite off)."""
    return diff(cell(pt, "probe_worse", arm, typ, "clear_drained"), cell(pt, "probe_worse", arm, typ, "clear_plain"))


def evidence_effect(pt, arm, typ):
    return diff(cell(pt, "probe_worse", arm, typ, "unclear_plain"), cell(pt, "probe_worse", arm, typ, "clear_plain"))


def clear_correct_t(probes_t):
    """Share of plain clear probes of one type answered correctly."""
    c = probes_t.get("clear_plain")
    if not c or c["abstain"] is None or c["correct_given_report"] is None:
        return None
    return (1 - c["abstain"]) * c["correct_given_report"]


def retained(pt, arm, typ):
    p = pt.get("probe_worse", {}).get(arm, {}).get("probes", {}).get(typ)
    return None if not p else clear_correct_t(p)


def damage_t(probes_t):
    c = probes_t.get("clear_noised")
    return None if not c else c["correct_given_report"]


def noise_effect(pt, arm, typ):
    return diff(cell(pt, "noise", arm, typ, "clear_noised"), cell(pt, "noise", arm, typ, "clear_plain"))


def steer_effect(pt, arm, typ):
    """Steering along A's worse direction, minus a random direction of the same norm, on clear trials of a type."""
    s = pt.get("steer", {}).get(arm)
    if not s or s.get("n") == 0:
        return None
    a, b = s["steer"][typ]["effect"], s["random"][typ]["effect"]
    return None if a is None or b is None else a - b


def discrimination(nat, typ):
    """Natural abstention on clear trials with implied reliability < 0.6 minus on trials with reliability 1."""
    b = nat["probes"][typ]["clear_by_rel"]
    n_lo = sum(b[j]["n"] for j in (2, 3))
    if n_lo == 0 or b[0]["n"] == 0 or b[0]["abstain"] is None:
        return None
    lo = sum(b[j]["abstain"] * b[j]["n"] for j in (2, 3) if b[j]["n"]) / n_lo
    return lo - b[0]["abstain"]


def exposure(nat):
    return nat["probes"]["A"].get("clear_share_below_break_even")


# ---------------------------------------------------------------- tests
def score_point(seeds, i, stages):
    out = {"iters": seeds[0]["points"][i]["iters"]}
    per = {}
    for s in seeds:
        pt = s["points"][i]
        nat = pt["natural"]
        reg = {a: bool(regulates(nat[a])) for a in ARMS}
        both = reg["PFATE"] and reg["PYOKED"]
        x = {"regulator": reg, "in_band": {a: nat[a]["in_band"] for a in ARMS},
             "usable": bool(both and abs(nat["PFATE"]["in_band"] - nat["PYOKED"]["in_band"]) <= MATCH_MAX)}
        for t in TYPES:
            x[f"evidence_{t}"] = {a: evidence_effect(pt, a, t) for a in ARMS}
            x[f"retained_{t}"] = {a: retained(pt, a, t) for a in ARMS}
            x[f"worse_{t}"] = {a: worse_effect(pt, a, t) for a in ARMS}
            x[f"discrimination_{t}"] = {a: discrimination(nat[a], t) for a in ARMS}
            if stages >= 2:
                x[f"noise_{t}"] = {a: noise_effect(pt, a, t) for a in ARMS}
                x[f"steer_{t}"] = {a: steer_effect(pt, a, t) for a in ARMS}
        per[s["seed"]] = x
    out["per_seed"] = per
    out["regulators"] = {a: sum(x["regulator"][a] for x in per.values()) for a in ARMS}
    out["usable"] = sum(x["usable"] for x in per.values())
    need = ceil(C0_SHARE * len(seeds))
    yp = sum((x["evidence_B"]["PYOKED"] or 0) > 0 for x in per.values())
    ret = {a: med(x["retained_B"][a] for x in per.values()) for a in ARMS}
    out["P3_0_gate"] = {"yoked_B_evidence_positive": yp, "n": len(per), "needed": need, "B_retained_median": ret,
                        "retain_min": RETAIN_MIN}
    out["P3_0_gate"]["label"] = ("PASS" if yp >= need and all(v is not None and v >= RETAIN_MIN for v in ret.values())
                                 else "FAIL")
    ident = lambda v: v
    P = lambda key, a, b, flag=lambda x: True: [(per[s["seed"]][key][a], per[s["seed"]][key][b])
                                                for s in seeds if flag(per[s["seed"]])]
    out["P3_0_referent"] = pair_test(P("worse_A", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    m = lambda arm, f: med(f(s["points"][i]["natural"][arm]) for s in seeds)
    out["arms"] = {a: {"in_band": m(a, lambda e: e["in_band"]), "abstain": m(a, lambda e: e["abstain_rate"]),
                       "correct": m(a, lambda e: e["correct_rate"]), "mean_gain": m(a, lambda e: e["mean_gain"]),
                       "below_break_even_A": m(a, exposure)} for a in ARMS}
    keys = ["evidence", "retained", "worse", "discrimination"] + (["noise", "steer"] if stages >= 2 else [])
    for a in ARMS:
        for k in keys:
            for t in TYPES:
                out["arms"][a][f"{k}_{t}"] = med(x[f"{k}_{t}"][a] for x in per.values())
    if stages < 2:
        return out
    out["P3_1"] = pair_test(P("worse_B", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    out["P3_2"] = pair_test(P("worse_B", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    out["P3_3"] = one_sample([x["steer_B"]["PFATE"] for x in per.values()], "CAUSAL", "REVERSED_CAUSAL")
    B = lambda a, b: [(per[s["seed"]]["in_band"][a], per[s["seed"]]["in_band"][b]) for s in seeds]
    out["secondary"] = {
        "C_worse_PFATE_vs_PYOKED": pair_test(P("worse_C", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "C_worse_PFATE_vs_PNOFATE": pair_test(P("worse_C", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "C_steer_PFATE": one_sample([x["steer_C"]["PFATE"] for x in per.values()], "CAUSAL", "REVERSED_CAUSAL"),
        "A_worse_PFATE_vs_PNOFATE": pair_test(P("worse_A", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "A_steer_PFATE": one_sample([x["steer_A"]["PFATE"] for x in per.values()], "CAUSAL", "REVERSED_CAUSAL"),
        "B_worse_usable_pairs": pair_test(P("worse_B", "PFATE", "PYOKED", flag=lambda x: x["usable"]), ident, "DERIVED", "YOKED"),
        "B_discrimination_PFATE_vs_PYOKED": pair_test(P("discrimination_B", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "A_discrimination_PFATE_vs_PYOKED": pair_test(P("discrimination_A", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "B_minus_C_worse_PFATE": one_sample([diff(x["worse_B"]["PFATE"], x["worse_C"]["PFATE"]) for x in per.values()],
                                            "B_AHEAD", "C_AHEAD"),
        "worse_route": {t: {a: one_sample([x[f"worse_{t}"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS}
                        for t in TYPES},
        "steer_route": {t: {a: one_sample([x[f"steer_{t}"][a] for x in per.values()], "CAUSAL", "REVERSED_CAUSAL")
                            for a in ARMS} for t in TYPES},
        "monitor_route": {t: {a: one_sample([x[f"noise_{t}"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS}
                          for t in ("A", "B")},
        "regulation_PFATE_vs_PNOFATE": pair_test(B("PFATE", "PNOFATE"), ident, "FATE", "HOST"),
        "regulation_PFATE_vs_PYOKED": pair_test(B("PFATE", "PYOKED"), ident, "FATE", "YOKED")}
    out["transfer_ratio_PFATE"] = med(None if not x["worse_A"]["PFATE"] or x["worse_B"]["PFATE"] is None
                                      else x["worse_B"]["PFATE"] / x["worse_A"]["PFATE"] for x in per.values())
    return out


def overall(sc):
    p = sc["points"][str(sc["primary_at"])]
    if not sc["valid"]:
        return "INVALID"
    if p["P3_0_gate"]["label"] != "PASS" or p["P3_0_referent"]["label"] != "DERIVED_AHEAD":
        return "UNDETERMINED"
    l1, l2, l3 = p["P3_1"]["label"], p["P3_2"]["label"], p["P3_3"]["label"]
    if "UNDETERMINED" in (l1, l2):
        return "UNDETERMINED"
    if l1 == "DERIVED_AHEAD" and l2 == "DERIVED_AHEAD":
        ratio = p.get("transfer_ratio_PFATE")
        if ratio is None or ratio < TRANSFER_MIN:
            return "TRACE"
        return "GLOBAL_ROUTED" if l3 == "CAUSAL" else "GLOBAL"
    if l1 == "DERIVED_AHEAD":
        return "PARTIAL"
    return "LOCAL"


def gating(sc):
    """Only for GLOBAL / GLOBAL_ROUTED: does the spread reach C, the decision the body cannot affect?"""
    if sc.get("overall") not in ("GLOBAL", "GLOBAL_ROUTED"):
        return "NOT_APPLICABLE"
    c = sc["points"][str(sc["primary_at"])]["secondary"]["C_worse_PFATE_vs_PYOKED"]["label"]
    return "UNGATED" if c == "DERIVED_AHEAD" else "GATED"


def phase1_validity(seeds):
    out = {}
    for t in TYPES:
        out[f"clear_correct_{t}"] = med(clear_correct_t(s["phase1"]["PLAIN"]["probes"][t]) for s in seeds)
    out["damage_A"] = med(damage_t(s["phase1"]["PLAIN"]["probes"]["A"]) for s in seeds)
    out["damage_B"] = med(damage_t(s["phase1"]["PLAIN"]["probes"]["B"]) for s in seeds)
    return out


def score(seeds, stages=2):
    pts = [p["iters"] for p in seeds[0]["points"]]
    sc = {"n_seeds": len(seeds), "points_at": pts, "primary_at": pts[-1], "params": seeds[0]["params"],
          "phase1": phase1_validity(seeds),
          "points": {str(p): score_point(seeds, i, stages) for i, p in enumerate(pts)}}
    i_pri = len(pts) - 1
    sc["exposure_median"] = med(exposure(s["points"][i_pri]["natural"]["PFATE"]) for s in seeds)
    v = sc["phase1"]
    sc["valid_memory"] = all(v[f"clear_correct_{t}"] is not None and v[f"clear_correct_{t}"] >= VALID_CLEAR_CORRECT
                             for t in TYPES)
    sc["valid_damage"] = all(v[k] is not None and v[k] <= DAMAGE_MAX for k in ("damage_A", "damage_B"))
    sc["valid_exposure"] = sc["exposure_median"] is not None and sc["exposure_median"] >= EXPOSURE_MIN
    sc["valid"] = sc["valid_memory"] and sc["valid_damage"] and sc["valid_exposure"]
    if stages >= 2:
        p = sc["points"][str(sc["primary_at"])]
        sc["overall"] = overall(sc)
        names = ("P3_1", "P3_2", "P3_3")
        sc["holm"] = dict(zip(names, holm([p[k]["sign_p"] for k in names])))
        need = {"GLOBAL": ("P3_1", "P3_2"), "GLOBAL_ROUTED": ("P3_1", "P3_2", "P3_3")}
        sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
        sc["gating"] = gating(sc)
    return sc


# ---------------------------------------------------------------- report
def _pt(r):
    if "first_ahead" in r:
        return f"{r['first_ahead']}/{r['n']} (p {fmt(r['sign_p'], 4)}; {fmt(r['first_median'])} against {fmt(r['second_median'])}) {r['label']}"
    return f"{r['positive']}/{r['n']} (p {fmt(r['sign_p'], 4)}; median {fmt(r['median'])}) {r['label']}"


def report(sc, stages=2):
    L = ["# Track C P3: global availability of the body-grounded self-state (Layer 0 -> Layer 3)", ""]
    if stages >= 2:
        h = sc["holm"]
        L += [f"**Overall: {sc['overall']}**{' (weak)' if sc['weak'] else ''}. Gating (C): {sc['gating']}. "
              f"Holm-adjusted p: P3_1 {fmt(h['P3_1'], 4)}, P3_2 {fmt(h['P3_2'], 4)}, P3_3 {fmt(h['P3_3'], 4)}.", ""]
    v = sc["phase1"]
    L += [f"Valid: {sc['valid']} (phase 1 clear correct A / B / C {fmt(v['clear_correct_A'])} / {fmt(v['clear_correct_B'])} / "
          f"{fmt(v['clear_correct_C'])}, needed >= {VALID_CLEAR_CORRECT}; overwrite-probe accuracy A / B {fmt(v['damage_A'])} / "
          f"{fmt(v['damage_B'])}, needed <= {DAMAGE_MAX}; PFATE A clear trials below break-even {fmt(sc['exposure_median'])}, "
          f"needed >= {EXPOSURE_MIN}). Parameters: {sc['params']['PLAIN']}. Phase 2 trial types: A only.", ""]
    cols = ["in_band", "worse_A", "worse_B", "worse_C", "retained_A", "retained_B", "retained_C", "evidence_B",
            "discrimination_A", "discrimination_B"] + (["steer_A", "steer_B", "steer_C", "noise_A", "noise_B"] if stages >= 2 else [])
    L += ["| updates | arm | " + " | ".join(cols) + " |", "| --- | --- | " + " | ".join("---" for _ in cols) + " |"]
    for p in sc["points_at"]:
        P = sc["points"][str(p)]
        for a in ARMS:
            L.append(f"| {p} | {a} | " + " | ".join(fmt(P["arms"][a].get(c)) for c in cols) + " |")
    L.append("")
    for p in sc["points_at"]:
        P = sc["points"][str(p)]
        g = P["P3_0_gate"]
        L += [f"At {p}: usable pairs {P['usable']}; regulators {P['regulators']}; gate {g['label']} (yoked B evidence "
              f"effect positive {g['yoked_B_evidence_positive']}/{g['n']}, needed {g['needed']}; B retained medians "
              f"{ {a: fmt(x) for a, x in g['B_retained_median'].items()} }, needed >= {RETAIN_MIN}).",
              f"- P3-0 referent in A, PFATE against PYOKED: {_pt(P['P3_0_referent'])}"]
        if stages >= 2:
            L += [f"- P3-1 B worse effect, PFATE against PYOKED: {_pt(P['P3_1'])}",
                  f"- P3-2 B worse effect, PFATE against PNOFATE: {_pt(P['P3_2'])}",
                  f"- P3-3 steering along A's worse direction, B trials, PFATE: {_pt(P['P3_3'])}",
                  f"- Transfer ratio in PFATE (B worse effect / A worse effect), median: {fmt(P['transfer_ratio_PFATE'])}"]
            for k, r in P["secondary"].items():
                if k in ("worse_route", "steer_route", "monitor_route"):
                    for t, rr in r.items():
                        L.append(f"- {k} {t}: " + "; ".join(f"{a} {_pt(x)}" for a, x in rr.items()))
                else:
                    L.append(f"- {k}: {_pt(r)}")
        L.append("")
    return "\n".join(L)


def calib_summary(seeds):
    """Calibration (blind): validity, B and C retention and evidence effects on unprobed trials, the A referent,
    regulation. No B or C probe effect is computed or printed."""
    L = ["# P3 calibration summary (blind to B and C probe effects)", ""]
    v = phase1_validity(seeds)
    L.append("phase 1: " + ", ".join(f"{k} {fmt(x)}" for k, x in v.items()))
    for i, p in enumerate(seeds[0]["points_at"]):
        L.append(f"## {p}")
        for s in seeds:
            pt = s["points"][i]
            nat = pt["natural"]
            row = [f"seed {s['seed']}"]
            for a in ARMS:
                row.append(f"{a}: band {fmt(nat[a]['in_band'])} worseA {fmt(worse_effect(pt, a, 'A'))} "
                           f"ret A/B/C {fmt(retained(pt, a, 'A'))}/{fmt(retained(pt, a, 'B'))}/{fmt(retained(pt, a, 'C'))} "
                           f"evid A/B/C {fmt(evidence_effect(pt, a, 'A'))}/{fmt(evidence_effect(pt, a, 'B'))}/{fmt(evidence_effect(pt, a, 'C'))}")
            row.append(f"exposure {fmt(exposure(nat['PFATE']))}")
            L.append(" | ".join(row))
            for a in ARMS:
                pr = pt["probe_worse"][a]["probes"]
                L.append(f"    {a} plain clear abstain / correct-given-report / unclear abstain: " + "  ".join(
                    f"{t} {fmt(pr[t]['clear_plain']['abstain'])}/{fmt(pr[t]['clear_plain']['correct_given_report'])}/"
                    f"{fmt(pr[t]['unclear_plain']['abstain'])}" for t in TYPES))
    for s in seeds:
        p1 = s["phase1"]["PLAIN"]["probes"]
        L.append(f"phase 1 seed {s['seed']}: " + "  ".join(
            f"{t} {fmt(p1[t]['clear_plain']['abstain'])}/{fmt(p1[t]['clear_plain']['correct_given_report'])}/"
            f"{fmt(p1[t]['unclear_plain']['abstain'])}" for t in TYPES))
    return "\n".join(L)


def strip(r):
    r = dict(r)
    r.pop("weights", None)
    return r


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
        recs = []
        for f in sorted(os.listdir(pdir)):
            with open(os.path.join(pdir, f)) as fh:
                recs.append(json.load(fh))
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
    reg = REG_ITERS_W if args.mode != "smoke" else 10
    warm = WARM_ITERS_C if args.mode != "smoke" else 5
    jobs = [(s, wcd, tcd, list(points), PAY[1], stages, warm, WARM_WRONG_C, reg, PHASE2_TYPES, REHEARSE_EVERY_W)
            for s in seeds]
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
            for k, r in enumerate(pool.imap_unordered(run_seed_w, todo), done + 1):
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
    if args.mode == "calib":
        print(calib_summary(sorted(recs, key=lambda r: r["seed"])))
        return
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE_O, "probe_gain": PROBE_GAIN_O,
            "rel_break_even": REL_BREAK_EVEN, "p_max": P_MAX_O, "probe_shift": DRAIN_SHIFT,
            "type_p_phase1_and_eval": list(TYPE_P_MIXED), "type_p_phase2": list(PHASE2_TYPES),
            "rehearse_every": REHEARSE_EVERY_W, "wrong_peak_phase1": WRONG_PEAK_W, "ramp_down_phase1": RAMP_DOWN_W,
            "wrong_ramp": WRONG_RAMP_C, "reg_iters_phase1": reg, "warm_iters": warm, "warm_wrong": WARM_WRONG_C,
            "pay": PAY[1], "drive_all_arms": True, "points": list(points), "stages": stages, "seeds": seeds,
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
