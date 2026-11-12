"""Track C swap, option Q: causal probes of the saved v7 and v8 regulators. Frozen runner and scorer.

    python run_trackc_causal.py --mode final --out trackc_causal     # once, after the freeze
    python run_trackc_causal.py --mode smoke --out <scratch dir>     # pipeline check (smoke-test agents)
    python run_trackc_causal.py --score trackc_causal                # re-score saved raw results

No training. Design, decision rules and disclosures: TRACKC_CAUSAL_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import json
import os
import platform
import sys
import time
from dataclasses import asdict
from multiprocessing import Pool

import torch

from run_trackc_probe import agents, fmt, med, regulates, sha, sign_p
from trackc_swap.causal import BINS, causal_agent
from trackc_swap.env import WorldConfig

WEAR = 0.001
N_ENVS = 128
EPISODES = 4
FULL_GROUPS = ("REG", "NREG")      # fate agents: all four conditions
OFF_GROUPS = ("YREG",)             # yoked partners of regulators: erasure off with the propensity probe only
# Decision rules (frozen; protocol section 4)
FRAC = 0.70                        # share of regulators needed for each claim
MIN_N = 30                         # fewer usable regulators: UNDETERMINED
S_MIN = 0.10                       # Q-a: post-meal suppression of eat propensity at least this
C_MIN = 0.02                       # Q-c: in band under own fate minus under scrambled erasure above this
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/relocate.py", "trackc_swap/causal.py",
           "run_trackc_probe.py", "run_trackc_causal.py", "test_trackc_swap.py", "TRACKC_CAUSAL_PROTOCOL.md"]


def verdict(k, n, frac=FRAC):
    return None if n < MIN_N else k >= frac * n


def score(recs):
    groups = {}
    for r in recs:
        groups.setdefault(r["group"], []).append(r)
    out = {"groups": {}}
    for g, rs in sorted(groups.items()):
        x = {"n": len(rs),
             "S_median": med(r["suppression"]["S"] for r in rs),
             "S_defined": sum(r["suppression"]["S"] is not None for r in rs),
             "S_at_least_min": sum((r["suppression"]["S"] or -9) >= S_MIN for r in rs),
             "in_band_off_median": med(r["off"]["in_band"] for r in rs),
             "psi_zero_median": med(r["zero_state"]["psi_zero"] for r in rs),
             "psi_carried_median": med(r["zero_state"]["psi_carried"] for r in rs),
             "S_by_bin_median": [med(r["suppression"]["per_bin"][i]["S"] for r in rs) for i in range(len(BINS) - 1)],
             "S_by_bin_defined": [sum(r["suppression"]["per_bin"][i]["S"] is not None for r in rs)
                                  for i in range(len(BINS) - 1)]}
        if all("own" in r for r in rs):
            x.update({"in_band_own_median": med(r["own"]["in_band"] for r in rs),
                      "in_band_own_shuffled_median": med(r["own_shuffled"]["in_band"] for r in rs),
                      "in_band_scrambled_median": med(r["scrambled"]["in_band"] for r in rs),
                      "regulating_own": sum(regulates(r["own"]) for r in rs),
                      "regulating_own_shuffled": sum(regulates(r["own_shuffled"]) for r in rs),
                      "regulating_scrambled": sum(regulates(r["scrambled"]) for r in rs),
                      "regulating_off": sum(regulates(r["off"]) for r in rs),
                      "erasures_own_median": med(float(r["own"]["erasures"]) for r in rs),
                      "erasures_scrambled_median": med(float(r["scrambled"]["erasures"]) for r in rs)})
        out["groups"][g] = x
    regs = groups.get("REG", [])
    # Q-a: the memory of a meal suppresses eating before interoception reports it
    s = [r["suppression"]["S"] for r in regs if r["suppression"]["S"] is not None]
    ka = sum(v >= S_MIN for v in s)
    out["Qa"] = {"defined": len(s), "of_regulators": len(regs), "suppressing": ka, "S_median": med(s),
                 "holds": verdict(ka, len(s))}
    # Q-b: under its own fate, regulation is lost when interoception is scrambled
    base = [r for r in regs if regulates(r["own"])]
    kb = sum(not regulates(r["own_shuffled"]) for r in base)
    out["Qb"] = {"regulating_own": len(base), "of_regulators": len(regs), "lost_under_shuffle": kb,
                 "in_band_own_median": med(r["own"]["in_band"] for r in base),
                 "in_band_shuffled_median": med(r["own_shuffled"]["in_band"] for r in base),
                 "holds": verdict(kb, len(base))}
    # Q-c: erasure contingent on the agent's own E supports regulation, against the same erasures scrambled
    c = [r["own"]["in_band"] - r["scrambled"]["in_band"] for r in regs]
    kc = sum(v > C_MIN for v in c)
    out["Qc"] = {"regulators": len(c), "contingent_higher": kc, "difference_median": med(c),
                 "sign_p": sign_p(sum(v > 0 for v in c), len(c)),
                 "in_band_own_median": med(r["own"]["in_band"] for r in regs),
                 "in_band_scrambled_median": med(r["scrambled"]["in_band"] for r in regs),
                 "in_band_off_median": med(r["off"]["in_band"] for r in regs),
                 "holds": verdict(kc, len(c))}
    return out


def report(sc):
    def v(h):
        return "UNDETERMINED" if h is None else ("HOLDS" if h else "DOES NOT HOLD")
    a, b, c = sc["Qa"], sc["Qb"], sc["Qc"]
    L = ["# Track C swap option Q: causal probes of the v7 and v8 regulators", "",
         f"**Q-a (memory of a meal suppresses eating before interoception reports it): {v(a['holds'])}** - "
         f"suppression >= {S_MIN} in {a['suppressing']}/{a['defined']} regulators (median S {fmt(a['S_median'])})", "",
         f"**Q-b (under its own fate, regulation needs interoception): {v(b['holds'])}** - {b['lost_under_shuffle']} of "
         f"{b['regulating_own']} regulators that regulate under their own fate (of {b['of_regulators']}) lose it under "
         f"the shuffle; median in band {fmt(b['in_band_own_median'])} -> {fmt(b['in_band_shuffled_median'])}", "",
         f"**Q-c (erasure contingent on own E supports regulation): {v(c['holds'])}** - in band higher by more than "
         f"{C_MIN} under own fate than under scrambled erasure in {c['contingent_higher']}/{c['regulators']} regulators; "
         f"median in band own {fmt(c['in_band_own_median'])}, scrambled {fmt(c['in_band_scrambled_median'])}, erasure off "
         f"{fmt(c['in_band_off_median'])}; median difference {fmt(c['difference_median'])}", "",
         "## Groups (medians)", "",
         "| group | n | S (defined; >= min) | eat propensity, in-band reading: zeroed / carried state | in band: off / own / "
         "own + shuffled / scrambled | regulating: off / own / own + shuffled / scrambled | erasures own / scrambled |",
         "| --- | --- | --- | --- | --- | --- | --- |"]
    for g, x in sc["groups"].items():
        full = "in_band_own_median" in x
        L.append(f"| {g} | {x['n']} | {fmt(x['S_median'])} ({x['S_defined']}; {x['S_at_least_min']}) | "
                 f"{fmt(x['psi_zero_median'])} / {fmt(x['psi_carried_median'])} | {fmt(x['in_band_off_median'])}"
                 + (f" / {fmt(x['in_band_own_median'])} / {fmt(x['in_band_own_shuffled_median'])} / "
                    f"{fmt(x['in_band_scrambled_median'])} | {x['regulating_off']} / {x['regulating_own']} / "
                    f"{x['regulating_own_shuffled']} / {x['regulating_scrambled']} | "
                    f"{fmt(x['erasures_own_median'], 0)} / {fmt(x['erasures_scrambled_median'], 0)} |"
                    if full else " / - / - / - | - | - |"))
    L += ["", "## Suppression by interoceptive reading (medians; agents with the bin defined)", "",
          "| group | " + " | ".join(f"{lo:.2f}-{hi:.2f}" for lo, hi in zip(BINS[:-1], BINS[1:])) + " |",
          "| --- |" + " --- |" * (len(BINS) - 1)]
    for g, x in sc["groups"].items():
        L.append(f"| {g} | " + " | ".join(f"{fmt(s)} ({n})" for s, n in zip(x["S_by_bin_median"], x["S_by_bin_defined"]))
                 + " |")
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
    ag = [(lab, p, o, s) for lab, p, o, s in agents(args.mode) if lab["group"] in FULL_GROUPS + OFF_GROUPS]
    weights_sha = {p: sha(p) for _, p, _, _ in ag}
    jobs = [(lab, torch.load(p), o, lab["gain"], lab["rate"], s, wcd, n_envs, episodes, lab["group"] in FULL_GROUPS)
            for lab, p, o, s in ag]
    t0 = time.time()
    recs = []
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(causal_agent, jobs), 1):
            recs.append(r)
            if k % 20 == 0 or k == len(jobs):
                print(f"[{k}/{len(jobs)}] elapsed {time.time() - t0:.0f} s", flush=True)
    recs.sort(key=lambda r: r["id"])
    meta = {"mode": args.mode, "world": wcd, "n_envs": n_envs, "episodes": episodes,
            "seconds": round(time.time() - t0, 1), "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}, "weights_sha256": weights_sha}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "agents": recs}, fh)
    sc = score(recs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print({k: sc[k]["holds"] for k in ("Qa", "Qb", "Qc")})


if __name__ == "__main__":
    main()
