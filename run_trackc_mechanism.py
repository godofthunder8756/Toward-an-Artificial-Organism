"""Track C swap, option W: what the hidden state of stored two-variable agents carries after a
meal. No training. Frozen runner and scorer.

    python run_trackc_mechanism.py --mode final --out trackc_mechanism           # once, after the freeze
    python run_trackc_mechanism.py --mode smoke --from <G2 smoke dir> --out <dir> # pipeline check
    python run_trackc_mechanism.py --score trackc_mechanism                       # re-score saved raw results

A final run that was interrupted is continued by the same command: finished jobs are kept in
<out>/partial and are not run again (every job is deterministic).

Design, decision rules and disclosures: TRACKC_MECHANISM_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time
from multiprocessing import Pool

import numpy as np
import torch

from run_trackc_general import spearman
from run_trackc_paid import two_sided_sign
from run_trackc_paid2 import ALPHA, MIN_PAIRS, holm, pair_test
from run_trackc_probe import fmt, med, sha
from run_trackc_specific import spec
from trackc_swap.mechanism import run_agent_w

ARMS = ("DERIVED", "YOKED", "PAID")
CLAIMS = ("W1", "W2", "W3")                  # the datasets the three tests are made on, in this order
PERMS = 10000                                # permutations for the link test
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/relocate.py", "trackc_swap/causal.py",
           "trackc_swap/paid.py", "trackc_swap/paid2.py", "trackc_swap/general.py", "trackc_swap/specific.py",
           "trackc_swap/mechanism.py", "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py",
           "run_trackc_general.py", "run_trackc_length.py", "run_trackc_specific.py", "run_trackc_mechanism.py",
           "test_trackc_swap.py", "TRACKC_MECHANISM_PROTOCOL.md", "trackc_general/raw.json",
           "trackc_general/scores.json", "trackc_specific/raw.json", "trackc_specific/scores.json"]


def datasets(mode, smoke_from=None):
    """The four sets of stored agents: {name: {claim, dir, kind, point}}. W1 is the primary."""
    if mode == "final":
        return {"G2_10800": {"claim": "W1", "dir": "trackc_specific", "kind": "G2", "point": 10800},
                "G2_14400": {"claim": "W2", "dir": "trackc_specific", "kind": "G2", "point": 14400},
                "G_10800": {"claim": "W3", "dir": "trackc_general", "kind": "G", "point": 10800},
                "G2_7200": {"claim": None, "dir": "trackc_specific", "kind": "G2", "point": 7200}}
    return {"G2_60": {"claim": "W1", "dir": smoke_from, "kind": "G2", "point": 60},
            "G2_80": {"claim": "W2", "dir": smoke_from, "kind": "G2", "point": 80},
            "G2_40": {"claim": "W3", "dir": smoke_from, "kind": "G2", "point": 40}}


def load_source(d):
    """(raw, scores) of the run a dataset comes from."""
    with open(os.path.join(d["dir"], "raw.json")) as fh:
        raw = json.load(fh)
    with open(os.path.join(d["dir"], "scores.json")) as fh:
        sc = json.load(fh)["scores"]
    return raw, sc


def stored(d, raw, sc):
    """For each seed: weights path per arm, the stored behavioural record per arm, regulator and usable flags."""
    out = {}
    if d["kind"] == "G":
        seeds, per = raw["cells"]["B2"], sc["cells"]["B2"]["per_seed"]
        for s in seeds:
            out[s["seed"]] = {"weights": {a: os.path.join(d["dir"], "weights", f"B2_seed{s['seed']}_{a}.pt") for a in ARMS},
                              "downstream": s["downstream"], **{k: per[str(s["seed"])][k] for k in ("usable", "regulator")}}
    else:
        i = raw["meta"]["points"].index(d["point"])
        per = sc["points"][str(d["point"])]["per_seed"]
        for s in raw["seeds"]:
            out[s["seed"]] = {"weights": {a: os.path.join(d["dir"], "weights", f"seed{s['seed']}_{a}_{d['point']}.pt")
                                          for a in ARMS},
                              "downstream": s["points"][i]["downstream"],
                              **{k: per[str(s["seed"])][k] for k in ("usable", "regulator")}}
    return out


def bits(r):
    return None if r is None or r.get("kind") is None else r["kind"]["bits"]


def field(name, sub="bits"):
    return lambda r: None if r is None or r.get(name) is None else r[name][sub]


def carries(vals):
    """Two-sided sign test of a measure against 0 over one arm's agents. CARRIES, NOT_DETECTED, UNDETERMINED."""
    v = [x for x in vals if x is not None and x != 0]
    n, k = len(v), sum(x > 0 for x in v)
    p = two_sided_sign(k, n)
    label = "UNDETERMINED" if n < MIN_PAIRS else "CARRIES" if (p <= ALPHA and k > n - k) else "NOT_DETECTED"
    return {"n": n, "positive": k, "sign_p": p, "median": med(v), "label": label}


def perm_spearman(xs, ys, perms=PERMS, seed=0):
    """Spearman rho and a two-sided permutation p over pairs with both values."""
    pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    rho = spearman([p[0] for p in pts], [p[1] for p in pts])
    if rho is None:
        return {"n": len(pts), "rho": None, "perm_p": None}
    rng = np.random.default_rng(seed)
    x, y = [p[0] for p in pts], [p[1] for p in pts]
    hits = sum(abs(spearman(x, list(rng.permutation(y))) or 0.0) >= abs(rho) - 1e-12 for _ in range(perms))
    return {"n": len(pts), "rho": rho, "perm_p": (hits + 1) / (perms + 1)}


def link(recs, info):
    """W4: rank correlation, over usable pairs, of the within-pair difference in what h carries about the
    kind of meal with the within-pair difference in behavioural specificity."""
    dx, dy = [], []
    for s, r in recs.items():
        if not info[s]["usable"]:
            continue
        a, b = bits(r.get("DERIVED")), bits(r.get("PAID"))
        sa, sb = spec(info[s]["downstream"]["DERIVED"]), spec(info[s]["downstream"]["PAID"])
        dx.append(None if a is None or b is None else a - b)
        dy.append(None if sa is None or sb is None else sa - sb)
    out = perm_spearman(dx, dy)
    out["label"] = ("UNDETERMINED" if out["n"] < MIN_PAIRS else
                    "LINKED" if out["rho"] is not None and out["rho"] > 0 and out["perm_p"] <= ALPHA else "NOT_LINKED")
    return out


def score_set(recs, info):
    """recs: {seed: {arm: record}}; info: stored() of the dataset."""
    seeds = sorted(recs)
    pairs = lambda flag: [(recs[s].get("DERIVED"), recs[s].get("PAID")) for s in seeds if flag(info[s])]
    test = lambda prs, f: pair_test(prs, f, "DERIVED", "PAID")
    usable = lambda x: x["usable"]
    out = {"n_seeds": len(seeds), "usable": sum(info[s]["usable"] for s in seeds),
           "kind": test(pairs(usable), bits)}
    regs = lambda arm: [recs[s].get(arm) for s in seeds if info[s]["regulator"][arm]]
    out["carries"] = {arm: carries([bits(r) for r in regs(arm)]) for arm in ("DERIVED", "PAID")}
    out["link"] = link(recs, info)
    out["trajectory_match"] = {arm: sum(recs[s][arm]["base"] == info[s]["downstream"][arm]["base"] for s in seeds
                                        if arm in recs[s]) for arm in ARMS}
    sec = {"kind_all_seeds": test(pairs(lambda x: True), bits),
           "meal": test(pairs(usable), field("meal")),
           "kind_h_alone_accuracy": test(pairs(usable), field("kind", "acc_h_alone")),
           "kind_baseline_bits": test(pairs(usable), field("kind", "bits_baseline")),
           "kind_lambda": {l: test(pairs(usable), lambda r, l=l: None if r is None else r["kind_lam"][l]) for l in ("10.0", "100.0")},
           "within_arm_spearman": {arm: spearman([bits(recs[s].get(arm)) for s in seeds],
                                                 [spec(info[s]["downstream"][arm]) for s in seeds]) for arm in ("DERIVED", "PAID")},
           "medians": {arm: {"kind_bits": med(bits(recs[s].get(arm)) for s in seeds),
                             "kind_acc_h_alone": med(field("kind", "acc_h_alone")(recs[s].get(arm)) for s in seeds),
                             "kind_acc_baseline": med(field("kind", "acc_baseline")(recs[s].get(arm)) for s in seeds),
                             "kind_acc_both": med(field("kind", "acc_both")(recs[s].get(arm)) for s in seeds),
                             "kind_bits_baseline": med(field("kind", "bits_baseline")(recs[s].get(arm)) for s in seeds),
                             "kind_n": med(field("kind", "n")(recs[s].get(arm)) for s in seeds),
                             "meal_bits": med(field("meal")(recs[s].get(arm)) for s in seeds),
                             "kind_by_step": {str(k): med(None if recs[s].get(arm) is None or recs[s][arm]["kind_by_step"][str(k)] is None
                                                          else recs[s][arm]["kind_by_step"][str(k)]["bits"] for s in seeds)
                                              for k in range(1, 11)}}
                       for arm in ARMS}}
    out["secondary"] = sec
    return out


def overall(w, carry1):
    """The label from W1 to W3 (pair tests) and the carries tests at W1. Protocol section 4."""
    l1 = w["W1"]["label"]
    if l1 == "UNDETERMINED":
        return "UNDETERMINED"
    if l1 == "PAID_AHEAD":
        return "REVERSED"
    if l1 == "DERIVED_AHEAD":
        return "REPRESENTED" if "DERIVED_AHEAD" in (w["W2"]["label"], w["W3"]["label"]) else "MIXED"
    c = [carry1[a]["label"] == "CARRIES" for a in ("DERIVED", "PAID")]
    if all(c):
        return "READ_OUT"
    if not any(c) and all(carry1[a]["label"] == "NOT_DETECTED" for a in ("DERIVED", "PAID")):
        return "NOT_IN_STATE"
    return "UNRESOLVED"


def score(raw_sets, infos, ds):
    sets = {name: score_set(raw_sets[name], infos[name]) for name in raw_sets}
    by = {d["claim"]: name for name, d in ds.items() if d["claim"]}
    w = {c: sets[by[c]]["kind"] for c in CLAIMS}
    label = overall(w, sets[by["W1"]]["carries"])
    h = dict(zip(CLAIMS, holm([w[c]["sign_p"] for c in CLAIMS])))
    ok = lambda c: w[c]["label"] == "DERIVED_AHEAD" and h[c] is not None and h[c] <= ALPHA
    weak = label == "REPRESENTED" and not (ok("W1") and (ok("W2") or ok("W3")))
    return {"sets": sets, "claims": {c: by[c] for c in CLAIMS}, "W": w, "W4_link": sets[by["W1"]]["link"],
            "carries_W1": sets[by["W1"]]["carries"], "overall": label, "holm": h, "weak": weak}


def report(sc):
    L = ["# Track C swap, option W: what the hidden state carries after a meal", "",
         f"**Overall: {sc['overall']}{' (weak)' if sc['weak'] else ''}.** " +
         "; ".join(f"{c} ({sc['claims'][c]}) {sc['W'][c]['label']}" for c in CLAIMS) +
         ". Holm-adjusted p: " + ", ".join(f"{c} {fmt(v, 4)}" for c, v in sc["holm"].items()) + ".", "",
         f"W4 (link, {sc['claims']['W1']}): {sc['W4_link']['label']}; rho {fmt(sc['W4_link']['rho'], 2)}, permutation p "
         f"{fmt(sc['W4_link']['perm_p'], 4)}, n {sc['W4_link']['n']}.", "",
         "Kind information is what the hidden state adds, in bits per sample, about which variable was eaten 2-5 "
         "steps ago, beyond the current observation and the reading history.", "",
         "| set | usable | kind bits D / Y / P | derived ahead | sign p | Wilcoxon p | median difference | label | "
         "carries D / P | h-alone accuracy D / P | baseline accuracy D / P | meal bits D / P | trajectories matched D / Y / P |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name, s in sc["sets"].items():
        k, m, c = s["kind"], s["secondary"]["medians"], s["carries"]
        L.append(f"| {name} | {s['usable']} | " + " / ".join(fmt(m[a]["kind_bits"]) for a in ARMS) +
                 f" | {k['first_ahead']}/{k['n']} | {fmt(k['sign_p'], 4)} | {fmt(k['wilcoxon_p'], 4)} | "
                 f"{fmt(k['difference_median'])} | {k['label']} | {c['DERIVED']['label']} / {c['PAID']['label']} | "
                 f"{fmt(m['DERIVED']['kind_acc_h_alone'])} / {fmt(m['PAID']['kind_acc_h_alone'])} | "
                 f"{fmt(m['DERIVED']['kind_acc_baseline'])} / {fmt(m['PAID']['kind_acc_baseline'])} | "
                 f"{fmt(m['DERIVED']['meal_bits'])} / {fmt(m['PAID']['meal_bits'])} | " +
                 " / ".join(str(s["trajectory_match"][a]) for a in ARMS) + " |")
    L.append("")
    for name, s in sc["sets"].items():
        se = s["secondary"]
        tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)}, {t['label']})"
        L += [f"{name}: kind on all seeds {tt(se['kind_all_seeds'])}; meal {tt(se['meal'])}; h-alone accuracy "
              f"{tt(se['kind_h_alone_accuracy'])}; baseline bits {tt(se['kind_baseline_bits'])}; penalty 10 "
              f"{tt(se['kind_lambda']['10.0'])}, 100 {tt(se['kind_lambda']['100.0'])}; link {s['link']['label']} "
              f"(rho {fmt(s['link']['rho'], 2)}); within-arm rank correlation of kind bits with specificity derived "
              f"{fmt(se['within_arm_spearman']['DERIVED'], 2)}, paid {fmt(se['within_arm_spearman']['PAID'], 2)}; kind bits "
              "by steps since the meal (derived | paid): " +
              ", ".join(f"{k}: {fmt(se['medians']['DERIVED']['kind_by_step'][k], 2)} | {fmt(se['medians']['PAID']['kind_by_step'][k], 2)}"
                        for k in map(str, range(1, 11))) + ".", ""]
    return "\n".join(L)


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
                jobs.append(({"set": name, "seed": seed, "arm": arm}, p, 64, seed, rate, wcd, n_envs, episodes))
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
    meta = {"mode": args.mode, "datasets": ds, "n_jobs": len(jobs), "resumed_jobs": done,
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
    for c in CLAIMS:
        print(c, sc["claims"][c], sc["W"][c]["label"], sc["W"][c]["first_ahead"], "/", sc["W"][c]["n"])
    print("W4", sc["W4_link"]["label"], "overall", sc["overall"], "weak" if sc["weak"] else "")


def _job(job):
    label, p, hidden, seed, rate, wcd, n_envs, episodes = job
    sd = torch.load(p, weights_only=True)
    return run_agent_w((label, sd, hidden, seed, rate, wcd, n_envs, episodes))


if __name__ == "__main__":
    main()
