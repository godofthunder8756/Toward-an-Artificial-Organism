"""Track C swap, option B: does selective post-meal suppression help? No training. Frozen
runner and scorer.

    python run_trackc_benefit.py --mode final --out trackc_benefit             # once, after the freeze
    python run_trackc_benefit.py --mode smoke --from <G2 smoke dir> --out <dir> # pipeline check
    python run_trackc_benefit.py --score trackc_benefit                         # re-score saved raw results

A final run that was interrupted is continued by the same command: finished jobs are kept in
<out>/partial and are not run again (every job is deterministic).

Design, decision rules and disclosures: TRACKC_BENEFIT_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # one thread per worker (option W's lesson)
    os.environ.setdefault(_v, "1")

import argparse
import hashlib
import json
import platform
import sys
import time
from multiprocessing import Pool

import torch

from run_trackc_general import is_regulator_g, k_agent, spearman
from run_trackc_mechanism import load_source, perm_spearman, stored
from run_trackc_paid2 import ALPHA, MIN_PAIRS, holm, pair_test
from run_trackc_probe import fmt, med, sha
from run_trackc_specific import cross, spec
from trackc_swap.benefit import VARIANTS, run_agent_b

ARMS = ("DERIVED", "YOKED", "PAID")
CLAIMS = ("B1", "B2", "B3")
PRIMARY = "V1"                                       # the variant of the three claims
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/relocate.py", "trackc_swap/causal.py",
           "trackc_swap/paid.py", "trackc_swap/paid2.py", "trackc_swap/general.py", "trackc_swap/specific.py",
           "trackc_swap/mechanism.py", "trackc_swap/benefit.py", "run_trackc_probe.py", "run_trackc_paid.py",
           "run_trackc_paid2.py", "run_trackc_general.py", "run_trackc_length.py", "run_trackc_specific.py",
           "run_trackc_mechanism.py", "run_trackc_benefit.py", "test_trackc_swap.py", "TRACKC_BENEFIT_PROTOCOL.md",
           "trackc_general/raw.json", "trackc_general/scores.json", "trackc_specific/raw.json",
           "trackc_specific/scores.json"]


def datasets(mode, smoke_from=None):
    """The three sets of stored agents: {name: {claim, dir, kind, point}}. B1 is the primary."""
    if mode == "final":
        return {"G2_10800": {"claim": "B1", "dir": "trackc_specific", "kind": "G2", "point": 10800},
                "G2_14400": {"claim": "B2", "dir": "trackc_specific", "kind": "G2", "point": 14400},
                "G_10800": {"claim": "B3", "dir": "trackc_general", "kind": "G", "point": 10800}}
    return {"G2_60": {"claim": "B1", "dir": smoke_from, "kind": "G2", "point": 60},
            "G2_80": {"claim": "B2", "dir": smoke_from, "kind": "G2", "point": 80},
            "G2_40": {"claim": "B3", "dir": smoke_from, "kind": "G2", "point": 40}}


def inband(v):
    return lambda r: None if r is None else r["variants"][v]["base"]["in_band"]


def gain(v, base="V0"):
    """A record's in-band time in variant v minus its in-band time in the base world."""
    return lambda r: None if r is None else inband(v)(r) - inband(base)(r)


def accuracy(v):
    return lambda r: None if r is None else r["variants"][v]["base"]["best_response_rate"]


def down(v, f):
    return lambda r: None if r is None else f(r["variants"][v])


def regulators(recs, v):
    """Agents meeting option G's regulator criterion in variant v (against the seed's yoked agent)."""
    out = {a: 0 for a in ("DERIVED", "PAID")}
    for r in recs.values():
        if all(a in r for a in ARMS):
            y = r["YOKED"]["variants"][v]["base"]
            for a in out:
                out[a] += is_regulator_g(r[a]["variants"][v]["base"], y)
    return out


def score_set(recs, info):
    seeds = sorted(recs)
    pairs = lambda flag: [(recs[s].get("DERIVED"), recs[s].get("PAID")) for s in seeds if flag(info[s])]
    test = lambda prs, f: pair_test(prs, f, "DERIVED", "PAID")
    usable = lambda x: x["usable"]
    us = pairs(usable)
    out = {"n_seeds": len(seeds), "usable": len(us), "claim": test(us, gain(PRIMARY))}
    out["claim"]["label"] = out["claim"]["label"].replace("_AHEAD", "_GAINS")
    out["v0_match"] = {a: sum(_match(recs[s][a]["variants"]["V0"], info[s]["downstream"][a]) for s in seeds if a in recs[s])
                       for a in ARMS}
    var = {}
    for v in VARIANTS:
        t = {"in_band": test(us, inband(v)), "accuracy": test(us, accuracy(v)), "spec": test(us, down(v, spec)),
             "K": test(us, down(v, k_agent)), "cross_K": test(us, down(v, cross)),
             "regulators": regulators(recs, v),
             "medians": {a: {"in_band": med(inband(v)(recs[s].get(a)) for s in seeds),
                             "accuracy": med(accuracy(v)(recs[s].get(a)) for s in seeds),
                             "rho": med(None if a not in recs[s] else recs[s][a]["variants"][v]["base"]["rho"] for s in seeds),
                             "spec": med(down(v, spec)(recs[s].get(a)) for s in seeds),
                             "K": med(down(v, k_agent)(recs[s].get(a)) for s in seeds)} for a in ARMS}}
        if v != "V0":
            t["gain"] = test(us, gain(v))
            t["gain_all_seeds"] = test(pairs(lambda x: True), gain(v))
        var[v] = t
    out["variants"] = var
    dg = [None if recs[s].get("DERIVED") is None else gain(PRIMARY)(recs[s]["DERIVED"]) - gain(PRIMARY)(recs[s]["PAID"])
          for s in seeds if info[s]["usable"]]
    ds = [_minus(spec(info[s]["downstream"]["DERIVED"]), spec(info[s]["downstream"]["PAID"])) for s in seeds if info[s]["usable"]]
    out["link"] = perm_spearman(ds, dg)
    out["link"]["label"] = ("UNDETERMINED" if out["link"]["n"] < MIN_PAIRS else
                            "LINKED" if out["link"]["rho"] is not None and out["link"]["rho"] > 0 and out["link"]["perm_p"] <= ALPHA
                            else "NOT_LINKED")
    out["within_arm_spearman"] = {a: spearman([spec(info[s]["downstream"][a]) for s in seeds],
                                              [gain(PRIMARY)(recs[s].get(a)) for s in seeds]) for a in ("DERIVED", "PAID")}
    return out


def _minus(a, b):
    return None if a is None or b is None else a - b


def _match(new, old):
    """V0 reproduces the stored downstream record (option G's records lack own_clean)."""
    return all(new[k] == old[k] for k in old)


def overall(c):
    l1 = c["B1"]["label"]
    if l1 == "UNDETERMINED":
        return "UNDETERMINED"
    if l1 == "PAID_GAINS":
        return "COST"
    if l1 == "DERIVED_GAINS":
        return "BENEFIT" if "DERIVED_GAINS" in (c["B2"]["label"], c["B3"]["label"]) else "MIXED"
    return "NO_BENEFIT"


def score(raw_sets, infos, ds):
    sets = {n: score_set(raw_sets[n], infos[n]) for n in raw_sets}
    by = {d["claim"]: n for n, d in ds.items()}
    c = {k: sets[by[k]]["claim"] for k in CLAIMS}
    label = overall(c)
    h = dict(zip(CLAIMS, holm([c[k]["sign_p"] for k in CLAIMS])))
    ok = lambda k: c[k]["label"] == "DERIVED_GAINS" and h[k] is not None and h[k] <= ALPHA
    weak = label == "BENEFIT" and not (ok("B1") and (ok("B2") or ok("B3")))
    return {"sets": sets, "claims": by, "B": c, "overall": label, "holm": h, "weak": weak}


def report(sc):
    L = ["# Track C swap, option B: does selective post-meal suppression help?", "",
         f"**Overall: {sc['overall']}{' (weak)' if sc['weak'] else ''}.** " +
         "; ".join(f"{k} ({sc['claims'][k]}) {sc['B'][k]['label']}" for k in CLAIMS) +
         ". Holm-adjusted p: " + ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm"].items()) + ".", "",
         f"Gain is in-band time (both variables) in {PRIMARY} minus in the base world V0, erasure off; the claim tests it "
         "derived against paid over usable pairs.", "",
         "| set | variant | in band D / Y / P | regulators D / P | derived higher in band | gain: derived ahead | sign p | "
         "median gain difference | accuracy D / P | specificity D / P | K D / P |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name, s in sc["sets"].items():
        for v, t in s["variants"].items():
            m, g = t["medians"], t.get("gain")
            L.append(f"| {name} | {v} | " + " / ".join(fmt(m[a]["in_band"]) for a in ARMS) +
                     f" | {t['regulators']['DERIVED']} / {t['regulators']['PAID']} | {t['in_band']['first_ahead']}/{t['in_band']['n']} | " +
                     ("n/a | n/a | n/a" if g is None else f"{g['first_ahead']}/{g['n']} | {fmt(g['sign_p'], 4)} | {fmt(g['difference_median'])}") +
                     f" | {fmt(m['DERIVED']['accuracy'])} / {fmt(m['PAID']['accuracy'])} | {fmt(m['DERIVED']['spec'])} / "
                     f"{fmt(m['PAID']['spec'])} | {fmt(m['DERIVED']['K'])} / {fmt(m['PAID']['K'])} |")
    L.append("")
    for name, s in sc["sets"].items():
        L.append(f"{name}: V0 reproduces the stored records for " + " / ".join(str(s["v0_match"][a]) for a in ARMS) +
                 f" agents; link (specificity difference with gain difference) {s['link']['label']} (rho "
                 f"{fmt(s['link']['rho'], 2)}, p {fmt(s['link']['perm_p'], 4)}, n {s['link']['n']}).")
    return "\n".join(L + [""])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--from", dest="smoke_from")
    ap.add_argument("--out")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        ds = d["meta"]["datasets"]
        infos = {n: stored(x, *load_source(x)) for n, x in ds.items()}
        raw_sets = {n: {int(s): v for s, v in recs.items()} for n, recs in d["sets"].items()}
        print(report(score(raw_sets, infos, ds)))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    ds = datasets(args.mode, args.smoke_from)
    infos, jobs, hashes = {}, [], {}
    for name, d in ds.items():
        raw, sc = load_source(d)
        infos[name] = info = stored(d, raw, sc)
        wcd, rate = raw["meta"]["world"], raw["meta"]["rate"]
        n_envs, episodes = raw["meta"]["sizes"]
        for seed, x in sorted(info.items()):
            for arm in ARMS:
                p = x["weights"][arm]
                with open(p, "rb") as fh:
                    hashes[p] = hashlib.sha256(fh.read()).hexdigest()
                jobs.append(({"set": name, "seed": seed, "arm": arm}, p, seed, rate, wcd, n_envs, episodes))
    pdir = os.path.join(args.out, "partial")
    os.makedirs(pdir, exist_ok=True)
    ppath = lambda lab: os.path.join(pdir, f"{lab['set']}_{lab['seed']}_{lab['arm']}.json")
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
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(_job, todo), done + 1):
            r = json.loads(json.dumps(r, default=float))
            with open(ppath(r) + ".tmp", "w") as fh:
                json.dump(r, fh)
            os.replace(ppath(r) + ".tmp", ppath(r))
            recs.append(r)
            if k % 12 == 0 or k == len(jobs):
                print(f"[job {k}/{len(jobs)}] {r['set']} seed {r['seed']} {r['arm']} ({r['seconds']} s, elapsed "
                      f"{time.time() - t0:.0f} s)", flush=True)
    raw_sets = {name: {} for name in ds}
    for r in recs:
        raw_sets[r["set"]].setdefault(r["seed"], {})[r["arm"]] = r
    meta = {"mode": args.mode, "datasets": ds, "variants": VARIANTS, "n_jobs": len(jobs), "resumed_jobs": done,
            "seconds": round(sum(r["seconds"] for r in recs), 1), "python": platform.python_version(),
            "torch": torch.__version__, "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)},
            "weights_sha256": hashes}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "sets": {n: {str(s): v for s, v in x.items()} for n, x in raw_sets.items()}}, fh)
    sc = score(raw_sets, infos, ds)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    for k in CLAIMS:
        print(k, sc["claims"][k], sc["B"][k]["label"], sc["B"][k]["first_ahead"], "/", sc["B"][k]["n"])
    print("overall", sc["overall"], "weak" if sc["weak"] else "")


def _job(job):
    label, p, seed, rate, wcd, n_envs, episodes = job
    sd = torch.load(p, weights_only=True)
    return run_agent_b((label, sd, seed, rate, wcd, n_envs, episodes))


if __name__ == "__main__":
    main()
