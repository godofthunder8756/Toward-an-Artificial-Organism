"""Track C P1: does a precarious substrate give self-evaluation a referent? Runner and scorer.

    python run_p1_selfeval.py --mode final --out p1_selfeval     # once, after the freeze
    python run_p1_selfeval.py --mode calib --out <scratch dir>   # calibration seeds, stage 1 only
    python run_p1_selfeval.py --mode smoke --out <scratch dir>   # pipeline check
    python run_p1_selfeval.py --score p1_selfeval                # re-score saved raw results

A final run that was interrupted is continued by the same command: finished jobs are kept in
<out>/partial and are not run again (every job is deterministic given its seed).

Design: P1_SELFEVAL_DESIGN_v1.md; decision rules and disclosures: P1_SELFEVAL_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
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

from run_trackc_paid import BAND_LEAD, BAND_MIN, P2_ITERS, PAY, RATE, TIMING_RATIO, WEAR, two_sided_sign
from run_trackc_paid2 import ALPHA, C0_SHARE, MIN_PAIRS, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.selfeval import run_seed_p1
from trackc_swap.train import TrainConfig

ARMS = ("FATE", "LOSS", "YOKED", "PFATE")
FINAL_SEEDS = list(range(1700, 1728))
CALIB_SEEDS = list(range(9900, 9912))   # round 1: 9900-9903; round 2 (warm-up): 9904-9907; round 3 (tanh task slice): 9908-9911
CALIB_ROUND = list(range(9908, 9912))
POINTS = (P2_ITERS, 2 * P2_ITERS)                   # 3600 (the base length), 7200 (primary)
MATCH_MAX = 0.10
VALID_CLEAR_CORRECT = 0.80                          # phase 1 must have learned the task (protocol section 4)
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/train.py", "trackc_swap/factorial.py",
           "trackc_swap/selfeval.py", "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py",
           "run_p1_selfeval.py", "test_trackc_swap.py", "P1_SELFEVAL_DESIGN_v1.md", "P1_SELFEVAL_PROTOCOL.md"]


def configs(mode):
    """(world, train config, seeds, points, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, 2
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_ROUND, POINTS, 1
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001], (10, 20), 2


def regulates(e):
    return e["in_band"] >= BAND_MIN and e["eat_rate_low"] >= TIMING_RATIO * e["eat_rate_high"]


def is_regulator(a, y):
    return regulates(a) and a["in_band"] - y["in_band"] >= BAND_LEAD


def cell(pt, kind, arm, key):
    """Abstention in a cell of the probe or natural evaluation; None if empty."""
    c = pt[kind][arm]["probes"].get(key)
    return None if c is None else c["abstain"]


def drain_effect(pt, arm, evidence="clear"):
    a, b = cell(pt, "probe", arm, f"{evidence}_drained"), cell(pt, "probe", arm, f"{evidence}_plain")
    return None if a is None or b is None else a - b


def evidence_effect(pt, arm):
    a, b = cell(pt, "probe", arm, "unclear_plain"), cell(pt, "probe", arm, "clear_plain")
    return None if a is None or b is None else a - b


def steer_effect(pt, arm):
    s = pt.get("steer", {}).get(arm)
    if not s or s.get("n") == 0 or s["steer"]["effect"] is None or s["random"]["effect"] is None:
        return None
    return s["steer"]["effect"] - s["random"]["effect"]


def clear_correct(ev):
    """Share of clear-evidence probes answered correctly (corruption off in phase 1, so reporting is right)."""
    c = ev["probes"].get("clear_plain")
    if not c or c["abstain"] is None or c["correct_given_report"] is None:
        return None
    return (1 - c["abstain"]) * c["correct_given_report"]


def one_sample(vals, hi, lo):
    v = [x for x in vals if x is not None and x != 0]
    n, k = len(v), sum(x > 0 for x in v)
    p = two_sided_sign(k, n)
    label = "UNDETERMINED" if n < MIN_PAIRS else (hi if k > n - k else lo) if p <= ALPHA else "NOT_DETECTED"
    return {"n": n, "positive": k, "sign_p": p, "median": med(v), "label": label}


def score_point(seeds, i, stages):
    out = {"iters": seeds[0]["points"][i]["iters"]}
    per = {}
    for s in seeds:
        pt = s["points"][i]
        nat = pt["natural"]
        y = nat["YOKED"]
        reg = {a: is_regulator(nat[a], y) for a in ("FATE", "LOSS", "PFATE")}
        reg["YOKED"] = is_regulator(y, nat["FATE"])
        both = reg["FATE"] and reg["LOSS"]
        per[s["seed"]] = {"regulator": reg, "in_band": {a: nat[a]["in_band"] for a in ARMS},
                          "usable": bool(both and abs(nat["FATE"]["in_band"] - nat["LOSS"]["in_band"]) <= MATCH_MAX),
                          "evidence_effect": {a: evidence_effect(pt, a) for a in ARMS},
                          "drain_effect": {a: drain_effect(pt, a) for a in ARMS} if stages >= 2 else None,
                          "steer_effect": {a: steer_effect(pt, a) for a in ("FATE", "LOSS", "YOKED")} if stages >= 2 else None}
    out["per_seed"] = per
    out["regulators"] = {a: sum(x["regulator"][a] for x in per.values()) for a in ARMS}
    out["usable"] = sum(x["usable"] for x in per.values())
    need = ceil(C0_SHARE * len(seeds))
    out["evidence_route"] = {a: one_sample([x["evidence_effect"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS}
    out["P1_0_gate"] = {"yoked_positive": sum((x["evidence_effect"]["YOKED"] or 0) > 0 for x in per.values()),
                        "n": len(per), "needed": need}
    out["P1_0_gate"]["label"] = "PASS" if out["P1_0_gate"]["yoked_positive"] >= need else "FAIL"
    m = lambda arm, f: med(f(s["points"][i]["natural"][arm]) for s in seeds)
    out["arms"] = {a: {"in_band": m(a, lambda e: e["in_band"]), "abstain": m(a, lambda e: e["abstain_rate"]),
                       "correct": m(a, lambda e: e["correct_rate"]), "wrong": m(a, lambda e: e["wrong_rate"]),
                       "rho": m(a, lambda e: e["rho"]),
                       "evidence_effect": med(x["evidence_effect"][a] for x in per.values())} for a in ARMS}
    if stages < 2:
        return out
    D = lambda s, a: per[s["seed"]]["drain_effect"][a]
    pairs = lambda flag, b: [(D(s, "FATE"), D(s, b)) for s in seeds if flag(per[s["seed"]])]
    ident = lambda x: x
    out["P1_1"] = pair_test(pairs(lambda x: x["usable"], "LOSS"), ident, "DERIVED", "PAID")
    out["P1_2"] = pair_test(pairs(lambda x: True, "YOKED"), ident, "DERIVED", "YOKED")
    out["P1_3"] = one_sample([per[s["seed"]]["steer_effect"]["FATE"] for s in seeds], "CAUSAL", "REVERSED_CAUSAL")
    out["P1_4"] = pair_test(pairs(lambda x: True, "PFATE"), ident, "RTSS", "PLAIN")
    for a in ARMS:
        out["arms"][a]["drain_effect"] = med(per[s["seed"]]["drain_effect"][a] for s in seeds)
        out["arms"][a]["drain_effect_unclear"] = med(drain_effect(s["points"][i], a, "unclear") for s in seeds)
    for a in ("FATE", "LOSS", "YOKED"):
        out["arms"][a]["steer_effect"] = med(per[s["seed"]]["steer_effect"][a] for s in seeds)
    out["secondary"] = {
        "P1_1_all_seeds": pair_test(pairs(lambda x: True, "LOSS"), ident, "DERIVED", "PAID"),
        "drain_route": {a: one_sample([per[s["seed"]]["drain_effect"][a] for s in seeds], "PRESENT", "REVERSED") for a in ARMS},
        "steer_LOSS": one_sample([per[s["seed"]]["steer_effect"]["LOSS"] for s in seeds], "CAUSAL", "REVERSED_CAUSAL"),
        "steer_YOKED": one_sample([per[s["seed"]]["steer_effect"]["YOKED"] for s in seeds], "CAUSAL", "REVERSED_CAUSAL"),
        "natural_by_reliability": {a: [{"bin": j, "abstain": med(s["points"][i]["natural"][a]["probes"]["clear_by_reliability"][j]["abstain"] for s in seeds),
                                        "n": med(s["points"][i]["natural"][a]["probes"]["clear_by_reliability"][j]["n"] for s in seeds)}
                                       for j in range(4)] for a in ARMS}}
    return out


def overall(sc):
    p = sc["points"][str(sc["primary_at"])]
    if not sc["valid"]:
        return "INVALID"
    if p["P1_0_gate"]["label"] != "PASS":
        return "UNDETERMINED"
    l1, l2, l3 = p["P1_1"]["label"], p["P1_2"]["label"], p["P1_3"]["label"]
    if "UNDETERMINED" in (l1, l2):
        return "UNDETERMINED"
    if l1 == "DERIVED_AHEAD" and l2 == "DERIVED_AHEAD":
        return "REFERENT_SUPPORTED_ROUTED" if l3 == "CAUSAL" else "REFERENT_SUPPORTED"
    if l1 == "DERIVED_AHEAD":
        return "MIXED"
    return "NOT_ESTABLISHED"


def score(seeds, stages=2):
    pts = [p["iters"] for p in seeds[0]["points"]]
    sc = {"n_seeds": len(seeds), "points_at": pts, "primary_at": pts[-1],
          "phase1_clear_correct_median": {k: med(clear_correct(s["phase1"][k]) for s in seeds) for k in ("RTSS", "PLAIN")},
          "params": seeds[0]["params"],
          "points": {str(p): score_point(seeds, i, stages) for i, p in enumerate(pts)}}
    sc["valid"] = all(v is not None and v >= VALID_CLEAR_CORRECT for v in sc["phase1_clear_correct_median"].values())
    if stages >= 2:
        p = sc["points"][str(sc["primary_at"])]
        sc["overall"] = overall(sc)
        sc["holm"] = dict(zip(("P1_1", "P1_2", "P1_3"), holm([p["P1_1"]["sign_p"], p["P1_2"]["sign_p"], p["P1_3"]["sign_p"]])))
        need = {"REFERENT_SUPPORTED": ("P1_1", "P1_2"), "REFERENT_SUPPORTED_ROUTED": ("P1_1", "P1_2", "P1_3")}
        sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
    return sc


def report(sc, stages=2):
    L = ["# Track C P1: does a precarious substrate give self-evaluation a referent?", ""]
    if stages >= 2:
        L += [f"**Overall: {sc['overall']}{' (weak)' if sc['weak'] else ''}.** Holm-adjusted p: " +
              ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm"].items()) + ".", ""]
    L += [f"Valid: {sc['valid']} (phase-1 correct-report rate, median: RTSS {fmt(sc['phase1_clear_correct_median']['RTSS'])}, "
          f"plain {fmt(sc['phase1_clear_correct_median']['PLAIN'])}). Parameters: RTSS {sc['params']['RTSS']}, plain {sc['params']['PLAIN']}.", "",
          "| updates | arm | regulators | in band | abstain | correct | wrong | evidence effect | drain effect (clear) | drain effect (unclear) | steer effect |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for p, x in sc["points"].items():
        for a in ARMS:
            ar = x["arms"][a]
            L.append(f"| {p} | {a} | {x['regulators'][a]} | {fmt(ar['in_band'])} | {fmt(ar['abstain'])} | {fmt(ar['correct'])} | "
                     f"{fmt(ar['wrong'])} | {fmt(ar['evidence_effect'])} | {fmt(ar.get('drain_effect'))} | "
                     f"{fmt(ar.get('drain_effect_unclear'))} | {fmt(ar.get('steer_effect'))} |")
    L.append("")
    for p, x in sc["points"].items():
        g = x["P1_0_gate"]
        L.append(f"At {p}: usable pairs {x['usable']}; P1-0 gate {g['label']} (yoked evidence effect positive in "
                 f"{g['yoked_positive']}/{g['n']}, needed {g['needed']}).")
        if stages >= 2:
            tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)}; {fmt(t['first_median'])} against {fmt(t['second_median'])}) {t['label']}"
            L += [f"- P1-1 drain effect, FATE against LOSS, usable pairs: {tt(x['P1_1'])}",
                  f"- P1-2 drain effect, FATE against YOKED: {tt(x['P1_2'])}",
                  f"- P1-3 steering in FATE: {x['P1_3']['positive']}/{x['P1_3']['n']} (p {fmt(x['P1_3']['sign_p'], 4)}) {x['P1_3']['label']}",
                  f"- P1-4 drain effect, RTSS-FATE against PLAIN-FATE: {tt(x['P1_4'])}"]
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
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        st = d["meta"]["stages"]
        print(report(score(d["seeds"], st), st))
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
    jobs = [(s, wcd, tcd, RATE, list(points), PAY[1], stages) for s in seeds]
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
    t0 = time.time()
    with Pool(min(len(todo), os.cpu_count() or 1) or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_seed_p1, todo), done + 1):
            for name, b in r["weights"].items():
                arm, p = name.split("@")
                torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}_{p}.pt"))
            r = json.loads(json.dumps(strip(r), default=float))
            with open(ppath(r["seed"]) + ".tmp", "w") as fh:
                json.dump(r, fh)
            os.replace(ppath(r["seed"]) + ".tmp", ppath(r["seed"]))
            recs.append(r)
            print(f"[job {k}/{len(jobs)}] seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE, "pay": PAY[1], "points": list(points),
            "stages": stages, "seeds": seeds, "seconds": round(sum(r["seconds"] for r in recs), 1), "resumed_jobs": done,
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
