"""Track C swap, option P: probe how the saved v7 and v8 agents represent and use E. Frozen runner and scorer.

    python run_trackc_probe.py --mode final --out trackc_probe     # once, after the freeze
    python run_trackc_probe.py --mode smoke --out <scratch dir>    # pipeline check (smoke-test agents)
    python run_trackc_probe.py --score trackc_probe                # re-score saved raw results

No training. Design, decision rules and disclosures: TRACKC_PROBE_PROTOCOL.md.
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
from math import comb
from multiprocessing import Pool

import torch

from trackc_swap.env import WorldConfig
from trackc_swap.probe import probe_agent

RUNS = {"v7": "trackc_swap_v7", "v8": "trackc_swap_v8"}
WEAR = 0.001
N_ENVS = 128
EPISODES = 2
# Decision rules (frozen; protocol section 4)
PAIR_FRAC = 0.70          # share of regulator/yoked pairs in which the regulator must be ahead (P1, P2)
LOST_FRAC = 0.70          # share of intact-regulating regulators that must lose regulation under the shuffle (P3)
MIN_PAIRS = 30            # fewer usable pairs or regulators: UNDETERMINED
D_WIN_MIN = 0.05          # anticipation index defined only where the window decoder explains >= this much of D
RAW_MIN = 0.20            # retention index defined only where the raw input explains >= this much of E
BAND_MIN, TIMING_RATIO = 0.60, 2.0   # v6's regulator criterion, own-behaviour parts
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/erasure.py", "trackc_swap/probe.py", "run_trackc_probe.py", "test_trackc_swap.py",
           "TRACKC_PROBE_PROTOCOL.md"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def sign_p(k, n):
    """One-sided sign-test p-value, P(X >= k) for X ~ Bin(n, 0.5)."""
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else None


def regulates(b):
    return b["in_band"] >= BAND_MIN and b["eat_rate_low"] >= TIMING_RATIO * b["eat_rate_high"]


def retention(r):
    return r["r2_E_h"] / r["r2_E_raw"] if r["r2_E_raw"] >= RAW_MIN else None


def anticipation(r):
    return r["r2_D_h"] / r["r2_D_win"] if r["r2_D_win"] >= D_WIN_MIN else None


def aid(run, o, g, rate, seed, arm):
    return f"{run} {o} {g} {rate} {seed} {arm}"


def agents(mode):
    """(label, weight path, objective, seed) for every agent to probe."""
    out = []
    if mode == "smoke":
        sd = os.environ["PROBE_SMOKE_DIR"]
        for f in sorted(os.listdir(sd)):
            if f.endswith(".pt"):
                o, g, r, s, arm = f[:-3].split("_")
                lab = {"id": aid("smoke", o, g, r[1:], s[4:], arm), "run": "smoke", "objective": o, "gain": g,
                       "rate": float(r[1:]), "seed": int(s[4:]), "arm": arm, "group": "REG" if arm == "FATE"
                       else "YREG", "partner": aid("smoke", o, g, r[1:], s[4:], "YOKED" if arm == "FATE" else "FATE")}
                out.append((lab, os.path.join(sd, f), o, int(s[4:])))
        return out
    for run, d in RUNS.items():
        sc = json.load(open(os.path.join(d, "scores.json")))["scores"]
        for ck, c in sc["cells"].items():
            o, g, r = ck.split()
            for s, x in c["per_seed"].items():
                reg = x["fate_regulator"]
                for arm in ("FATE", "YOKED"):
                    other = "YOKED" if arm == "FATE" else "FATE"
                    if o == "M0":
                        grp = "M0F" if arm == "FATE" else "M0Y"
                    elif arm == "FATE":
                        grp = "REG" if reg else "NREG"
                    else:
                        grp = "YREG" if reg else "YNREG"
                    lab = {"id": aid(run, o, g, r, s, arm), "run": run, "objective": o, "gain": g, "rate": float(r),
                           "seed": int(s), "arm": arm, "group": grp, "partner": aid(run, o, g, r, s, other),
                           "frozen_in_band": x["in_band_fate"] if arm == "FATE" else x["in_band_yoked"]}
                    out.append((lab, os.path.join(d, "pair_weights", f"{o}_{g}_r{r}_seed{s}_{arm}.pt"), o, int(s)))
        for s in json.load(open(os.path.join(d, "raw.json")))["meta"]["seeds"]:
            lab = {"id": aid(run, "M1", "-", "-", s, "NOFATE"), "run": run, "objective": "M1", "gain": None,
                   "rate": None, "seed": s, "arm": "NOFATE", "group": "NOFATE", "partner": None}
            out.append((lab, os.path.join(d, "phase1_weights", f"M1_seed{s}.pt"), "M1", s))
    return out


def score(recs):
    by = {r["id"]: r for r in recs}
    groups = {}
    for r in recs:
        groups.setdefault(r["group"], []).append(r)
    out = {"groups": {}}
    for g, rs in sorted(groups.items()):
        out["groups"][g] = {
            "n": len(rs),
            **{f"{k}_median": med(r[k] for r in rs) for k in
               ("r2_E_h", "r2_E_raw", "r2_E_win", "gain_E", "r2_D_h", "r2_D_win", "E_sd")},
            "retention_median": med(retention(r) for r in rs),
            "anticipation_median": med(anticipation(r) for r in rs),
            "anticipation_defined": sum(anticipation(r) is not None for r in rs),
            "in_band_intact_median": med(r["intact"]["in_band"] for r in rs),
            "in_band_shuffled_median": med(r["shuffled"]["in_band"] for r in rs),
            "regulating_intact": sum(regulates(r["intact"]) for r in rs),
            "regulating_shuffled": sum(regulates(r["shuffled"]) for r in rs),
            "eats_intact_median": med(r["intact"]["eats"] for r in rs),
        }
    regs = groups.get("REG", [])
    pairs = [(r, by[r["partner"]]) for r in regs if r["partner"] in by]
    # P1: retention of what interoception says about E, regulator ahead of its yoked partner
    ep = [(retention(f), retention(y)) for f, y in pairs]
    ep = [(a, b) for a, b in ep if a is not None and b is not None]
    n1, w1 = len(ep), sum(a > b for a, b in ep)
    p1 = None if n1 < MIN_PAIRS else w1 >= PAIR_FRAC * n1
    # P2: anticipation of the unreported change
    dp = [(anticipation(f), anticipation(y)) for f, y in pairs]
    dp = [(a, b) for a, b in dp if a is not None and b is not None]
    n2, w2 = len(dp), sum(a > b for a, b in dp)
    p2 = None if n2 < MIN_PAIRS else w2 >= PAIR_FRAC * n2
    # P3: regulation needs interoception
    base = [r for r in regs if regulates(r["intact"])]
    n3 = len(base)
    lost = sum(not regulates(r["shuffled"]) for r in base)
    p3 = None if n3 < MIN_PAIRS else lost >= LOST_FRAC * n3
    out["P1"] = {"pairs": n1, "regulator_ahead": w1, "sign_p": sign_p(w1, n1),
                 "regulator_retention_median": med(a for a, _ in ep), "yoked_retention_median": med(b for _, b in ep),
                 "regulator_gain_E_median": med(f["gain_E"] for f, _ in pairs),
                 "yoked_gain_E_median": med(y["gain_E"] for _, y in pairs), "holds": p1}
    out["P2"] = {"pairs": n2, "regulator_ahead": w2, "sign_p": sign_p(w2, n2),
                 "regulator_anticipation_median": med(a for a, _ in dp),
                 "yoked_anticipation_median": med(b for _, b in dp), "holds": p2}
    out["P3"] = {"regulating_intact": n3, "of_regulators": len(regs), "lost_under_shuffle": lost,
                 "in_band_intact_median": med(r["intact"]["in_band"] for r in base),
                 "in_band_shuffled_median": med(r["shuffled"]["in_band"] for r in base), "holds": p3}
    return out


def fmt(x, d=3):
    return "n/a" if x is None else (f"{x:.{d}f}" if isinstance(x, float) else str(x))


def report(sc):
    def verdict(h):
        return "UNDETERMINED" if h is None else ("HOLDS" if h else "DOES NOT HOLD")
    P1, P2, P3 = sc["P1"], sc["P2"], sc["P3"]
    L = ["# Track C swap option P: how regulators represent and use E (probe of v7 and v8 weights)", "",
         f"**P1 (state retains what interoception says about E, regulator ahead of yoked partner): "
         f"{verdict(P1['holds'])}** - ahead in {P1['regulator_ahead']}/{P1['pairs']} pairs (sign p = "
         f"{fmt(P1['sign_p'], 4)}); median retention regulator {fmt(P1['regulator_retention_median'])}, yoked "
         f"{fmt(P1['yoked_retention_median'])} (gain over raw input, descriptive: {fmt(P1['regulator_gain_E_median'])} "
         f"/ {fmt(P1['yoked_gain_E_median'])})", "",
         f"**P2 (anticipates the change interoception has not reported, regulator ahead): {verdict(P2['holds'])}** "
         f"- ahead in {P2['regulator_ahead']}/{P2['pairs']} pairs (sign p = {fmt(P2['sign_p'], 4)}); median "
         f"anticipation regulator {fmt(P2['regulator_anticipation_median'])}, yoked {fmt(P2['yoked_anticipation_median'])}",
         "",
         f"**P3 (regulation needs interoception): {verdict(P3['holds'])}** - {P3['lost_under_shuffle']} of "
         f"{P3['regulating_intact']} regulators that regulate intact (of {P3['of_regulators']}) lose it under the "
         f"shuffle; median in band {fmt(P3['in_band_intact_median'])} -> {fmt(P3['in_band_shuffled_median'])}", "",
         "## Groups (medians)", "",
         "| group | n | R2 E: h / raw / window | retention | gain_E | R2 D: h / window | anticipation (defined) | E sd | "
         "in band intact / shuffled | regulating intact / shuffled | eats per run |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for g, x in sc["groups"].items():
        L.append(f"| {g} | {x['n']} | {fmt(x['r2_E_h_median'])} / {fmt(x['r2_E_raw_median'])} / "
                 f"{fmt(x['r2_E_win_median'])} | {fmt(x['retention_median'])} | {fmt(x['gain_E_median'])} | {fmt(x['r2_D_h_median'])} / "
                 f"{fmt(x['r2_D_win_median'])} | {fmt(x['anticipation_median'])} ({x['anticipation_defined']}) | "
                 f"{fmt(x['E_sd_median'])} | {fmt(x['in_band_intact_median'])} / {fmt(x['in_band_shuffled_median'])} | "
                 f"{x['regulating_intact']} / {x['regulating_shuffled']} | {fmt(x['eats_intact_median'], 0)} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(report(score(d["agents"])))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc = WorldConfig(wear=WEAR) if args.mode == "final" else WorldConfig(horizon=100, wear=WEAR)
    n_envs, episodes = (N_ENVS, EPISODES) if args.mode == "final" else (16, 1)
    wcd = asdict(wc)
    ag = agents(args.mode)
    weights_sha = {p: sha(p) for _, p, _, _ in ag}
    jobs = [(lab, torch.load(p), o, s, wcd, n_envs, episodes) for lab, p, o, s in ag]
    t0 = time.time()
    recs = []
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(probe_agent, jobs), 1):
            recs.append(r)
            if k % 20 == 0 or k == len(jobs):
                print(f"[{k}/{len(jobs)}] elapsed {time.time() - t0:.0f} s", flush=True)
    recs.sort(key=lambda r: r["id"])
    meta = {"mode": args.mode, "world": wcd, "n_envs": n_envs, "episodes": episodes, "runs": RUNS,
            "seconds": round(time.time() - t0, 1), "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}, "weights_sha256": weights_sha}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "agents": recs}, fh)
    sc = score(recs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print({k: sc[k]["holds"] for k in ("P1", "P2", "P3")})


if __name__ == "__main__":
    main()
