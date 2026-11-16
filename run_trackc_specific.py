"""Track C swap, option G2: specificity of post-meal suppression in the two-variable cell.
Frozen runner and scorer.

    python run_trackc_specific.py --mode final --out trackc_specific   # once, after the freeze
    python run_trackc_specific.py --mode smoke --out <scratch dir>     # pipeline check
    python run_trackc_specific.py --score trackc_specific              # re-score saved raw results

A final run that was interrupted is continued by the same command: finished jobs are kept in
<out>/partial and are not run again (every job is deterministic given its seed).

Design, decision rules and disclosures: TRACKC_SPECIFIC_PROTOCOL.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import json
import os
import platform
import sys
import time
from dataclasses import asdict

import torch

from run_trackc_general import ARMS, RUN, SIZES, cross, k_agent, k_res, part, score_cell, spearman
from run_trackc_length import at, change_test, median_interval, overall
from run_trackc_paid import P2_ITERS, RATE, WEAR
from run_trackc_paid2 import ALPHA, MIN_PAIRS, combined, first_sustained, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.specific import run_seed_s
from trackc_swap.train import TrainConfig

# Frozen (protocol section 2). Seeds are fresh: v1-v8 used 100-808, R 900-917, R2 1000-1027,
# R3 1100-1127, R4 1200-1227, G 1300-1327 and 1400-1427, T 1500-1527; calibration and timing
# seeds were 9000-9800.
FINAL_SEEDS = list(range(1600, 1628))
POINTS = (P2_ITERS, 2 * P2_ITERS, 3 * P2_ITERS, 4 * P2_ITERS)   # 3600, 7200, 10 800 (option G's B2), 14 400
PAY = RUN["B2"]["pay"]                               # option G's B2 payment weight
MIN_OWN = 0.1                                        # the specific share needs an own-meal K above this
NEEDS = {"PERSISTS": ("S1", "S2"), "PERSISTS_SMALLER": ("S1", "S2", "S3"), "CLOSES": ("S1", "S3")}
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py", "trackc_swap/relocate.py",
           "trackc_swap/probe.py", "trackc_swap/causal.py", "trackc_swap/paid.py", "trackc_swap/paid2.py",
           "trackc_swap/general.py", "trackc_swap/length.py", "trackc_swap/specific.py", "run_trackc_probe.py",
           "run_trackc_paid.py", "run_trackc_paid2.py", "run_trackc_general.py", "run_trackc_length.py",
           "run_trackc_specific.py", "test_trackc_swap.py", "TRACKC_SPECIFIC_PROTOCOL.md"]


def configs(mode):
    """(world, phase-1 train config, seeds, measurement points, downstream sizes, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, SIZES, 2
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1),
            [9000, 9001], (20, 40, 60, 80), (16, 1), 2)


def _minus(a, b):
    return None if a is None or b is None else a - b


def _mean(v):
    return None if any(x is None for x in v) else sum(v) / len(v)


def _k(c):
    return combined({"suppression": {"S": c["S"]}, "approach": {"M": c["M"]}})


def spec(d):
    """Specificity: own-meal K minus other-meal K, each the mean over the two variables. This is
    the quantity of option G's post-hoc contrast."""
    return _minus(k_agent(d), cross(d))


def share(d):
    """The specific share 1 - (other-meal K / own-meal K); undefined unless own-meal K > MIN_OWN."""
    own, cr = k_agent(d), cross(d)
    return None if own is None or cr is None or own <= MIN_OWN else 1.0 - cr / own


def spec_part(sub):
    """Specificity of one part: S ("suppression") or M ("approach")."""
    key = {"S": "suppression", "M": "approach"}[sub]
    return lambda d: _minus(part(d, key, sub), _mean([c[sub] for c in d["cross"]]))


def spec_var(r):
    """Specificity for body variable r alone."""
    return lambda d: _minus(k_res(d)[r], _k(d["cross"][r]))


def clean(d):
    """Own-meal K over steps with no recent meal of the other kind (mean over variables)."""
    return _mean([_k(c) for c in d["own_clean"]])


def spec_clean(d):
    """Specificity with both sides measured away from the other kind of meal."""
    return _minus(clean(d), cross(d))


MEASURES = {"own_K": k_agent, "cross_K": cross, "spec": spec, "share": share, "clean_own_K": clean,
            "spec_clean": spec_clean}


def within(recs, f, g, hi, lo):
    """Paired test of f against g on the same agents."""
    vals = [(f(d), g(d)) for d in recs]
    return pair_test([(a, b) for a, b in vals], lambda x: x, hi, lo)


def score(seeds):
    pts = [p["iters"] for p in seeds[0]["points"]]
    assert len(pts) >= 2
    cells = [score_cell(at(seeds, i)) for i in range(len(pts))]
    ip, il = len(pts) - 2, len(pts) - 1                      # the primary point and the last point
    out = {"n_seeds": len(seeds), "points_at": pts, "primary_at": pts[ip], "last_at": pts[il],
           "points": dict(zip(map(str, pts), cells))}
    prim, last = cells[ip], cells[il]
    g0 = (prim["G0_regulation"]["label"], last["G0_regulation"]["label"])
    out["S0_regulation"] = {"primary": prim["G0_regulation"], "last": last["G0_regulation"],
                            "label": "INVALID" if "INVALID" in g0 else "HOLDS" if g0 == ("HOLDS", "HOLDS")
                            else "DOES_NOT_HOLD"}
    per = lambda i, s: cells[i]["per_seed"][s["seed"]]
    out["regulators_at_each_point"] = {str(p): cells[i]["regulators"] for i, p in enumerate(pts)}
    if "G1_combined" not in last:
        return out                                           # stage 1 only
    ds = lambda s, i, arm: s["points"][i]["downstream"][arm]
    pairs = lambda i, flag: [(ds(s, i, "DERIVED"), ds(s, i, "PAID")) for s in seeds if flag(per(i, s))]
    test = lambda prs, f: pair_test(prs, f, "DERIVED", "PAID")
    usable = lambda x: x["usable"]
    contrast = lambda s, i, f=spec: _minus(f(ds(s, i, "DERIVED")), f(ds(s, i, "PAID")))
    s1, s2 = test(pairs(ip, usable), spec), test(pairs(il, usable), spec)
    for t, c in ((s1, prim), (s2, last)):
        if not c["learned"]:
            t["label"] = "INVALID"
    both = [s for s in seeds if per(ip, s)["usable"] and per(il, s)["usable"]]
    s3 = change_test([(contrast(s, ip), contrast(s, il)) for s in both])
    if "INVALID" in (s1["label"], s2["label"]):
        s3["label"] = "INVALID"
    out["S1_primary"], out["S2_last"], out["S3_change"] = s1, s2, s3
    out["usable_at_primary_and_last"] = len(both)
    out["overall"] = label = overall(s1, s2, s3)
    h = dict(zip(("S1", "S2", "S3"), holm([s1["sign_p"], s2["sign_p"], s3["sign_p"]])))
    out["holm"] = h
    out["weak"] = any(h[k] is None or h[k] > ALPHA for k in NEEDS.get(label, ()))
    # ---- secondary, per point
    sec = {}
    for i, p in enumerate(pts):
        c = cells[i]
        us, reg = pairs(i, usable), lambda arm: [ds(s, i, arm) for s in seeds if per(i, s)["regulator"][arm]]
        sec[str(p)] = {
            "spec": test(us, spec),
            "spec_all_seeds": test(pairs(i, lambda x: True), spec),
            "spec_tight_pairs": test(pairs(i, lambda x: x["tight"]), spec),
            "share": test(us, share),
            "spec_S": test(us, spec_part("S")),
            "spec_M": test(us, spec_part("M")),
            "spec_clean": test(us, spec_clean),
            "spec_each_variable": [test(us, spec_var(r)) for r in (0, 1)],
            "cross_K": test(us, cross),
            "interval": median_interval([contrast(s, i) for s in seeds if per(i, s)["usable"]]),
            "own_above_cross": {arm: within(reg(arm), k_agent, cross, "OWN", "CROSS") for arm in ("DERIVED", "PAID")},
            "medians": {arm: {name: med(f(ds(s, i, arm)) for s in seeds) for name, f in MEASURES.items()}
                        for arm in ARMS},
            "medians_regulators": {arm: {name: med(f(d) for d in reg(arm)) for name, f in MEASURES.items()}
                                   for arm in ("DERIVED", "PAID")}}
    out["secondary"] = sec
    # ---- secondary, across points
    regs = lambda arm, *idx: [s for s in seeds if all(per(i, s)["regulator"][arm] for i in idx)]
    acr = {"change": {}, "change_all_seeds": change_test([(contrast(s, ip), contrast(s, il)) for s in seeds])}
    for arm in ("DERIVED", "PAID"):                          # each arm's own measures, last point against primary
        keep = regs(arm, ip, il)
        acr["change"][arm] = {name: pair_test([(ds(s, il, arm), ds(s, ip, arm)) for s in keep], f, "LAST", "FIRST")
                              for name, f in (("spec", spec), ("own_K", k_agent), ("cross_K", cross))}
    # stage-matched: derived agents at the last point against paid agents at the primary point
    sm = [s for s in seeds if per(il, s)["regulator"]["DERIVED"] and per(ip, s)["regulator"]["PAID"]]
    acr["stage_matched"] = pair_test([(ds(s, il, "DERIVED"), ds(s, ip, "PAID")) for s in sm], spec, "DERIVED", "PAID")
    onset = lambda s, arm: first_sustained(s["curves"][arm]["in_band"][:s["points"][il]["episodes"]])
    per_ep = seeds[0]["points"][0]["iters"] / seeds[0]["points"][0]["episodes"]      # updates per episode
    def since(s, i, arm):
        o = onset(s, arm)
        return None if o is None else s["points"][i]["iters"] - per_ep * o
    acr["onset_median_updates"] = {arm: med(None if onset(s, arm) is None else per_ep * onset(s, arm) for s in seeds)
                                   for arm in ARMS}
    acr["updates_since_onset_median"] = {str(p): {arm: med(since(s, i, arm) for s in regs(arm, i))
                                                  for arm in ("DERIVED", "PAID")} for i, p in enumerate(pts)}
    acr["stage_matched"]["updates_since_onset_median"] = {"DERIVED": med(since(s, il, "DERIVED") for s in sm),
                                                          "PAID": med(since(s, ip, "PAID") for s in sm)}
    acr["spec_vs_updates_since_onset_spearman"] = {
        str(pts[i]): {arm: spearman([since(s, i, arm) for s in regs(arm, i)], [spec(ds(s, i, arm)) for s in regs(arm, i)])
                      for arm in ("DERIVED", "PAID")} for i in (ip, il)}
    out["across"] = acr
    return out


def report(sc):
    L = ["# Track C swap, option G2: specificity of post-meal suppression in the two-variable cell", ""]
    pts = sc["points_at"]
    s0 = sc["S0_regulation"]
    if "overall" in sc:
        h = sc["holm"]
        L += [f"**Overall: {sc['overall']}{' (weak)' if sc['weak'] else ''}.** S1 (at {sc['primary_at']}) "
              f"{sc['S1_primary']['label']}; S2 (at {sc['last_at']}) {sc['S2_last']['label']}; S3 (change) "
              f"{sc['S3_change']['label']}. Holm-adjusted p: " + ", ".join(f"{k} {fmt(v, 4)}" for k, v in h.items()) + ".", ""]
    L += [f"**S0 (derived regulation at {sc['primary_at']} and {sc['last_at']}): {s0['label']}.** Derived regulators "
          f"{s0['primary']['derived_regulators']}/{s0['primary']['n']} then {s0['last']['derived_regulators']}/"
          f"{s0['last']['n']} (needed {s0['primary']['needed']}); yoked {s0['primary']['yoked_regulators']} then "
          f"{s0['last']['yoked_regulators']}.", ""]
    if "overall" not in sc:
        L += ["| updates | regulators D / Y / P | usable | in band D / Y / P |", "| --- | --- | --- | --- |"]
        for p in pts:
            c = sc["points"][str(p)]
            L.append(f"| {p} | " + " / ".join(str(c["regulators"][a]) for a in ARMS) + f" | {c['usable']} | " +
                     " / ".join(fmt(c["arms"][a]["in_band_median"]) for a in ARMS) + " |")
        return "\n".join(L + [""])
    L += ["Specificity is own-meal K minus other-meal K. Tests are paired sign tests, derived against paid, over usable pairs.",
          "",
          "| updates | regulators D / Y / P | usable | in band D / Y / P | own K D / P | other-meal K D / P | specificity D / P | "
          "derived more specific | sign p | Wilcoxon p | median difference | interval | label |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    two = lambda m, name: f"{fmt(m['DERIVED'][name])} / {fmt(m['PAID'][name])}"
    for p in pts:
        c, s = sc["points"][str(p)], sc["secondary"][str(p)]
        t, m, iv = s["spec"], s["medians_regulators"], s["interval"]
        L.append(f"| {p} | " + " / ".join(str(c["regulators"][a]) for a in ARMS) + f" | {c['usable']} | " +
                 " / ".join(fmt(c["arms"][a]["in_band_median"]) for a in ARMS) +
                 f" | {two(m, 'own_K')} | {two(m, 'cross_K')} | {two(m, 'spec')} | {t['first_ahead']}/{t['n']} | "
                 f"{fmt(t['sign_p'], 4)} | {fmt(t['wilcoxon_p'], 4)} | {fmt(t['difference_median'])} | " +
                 ("n/a" if iv is None else f"{fmt(iv[0])} to {fmt(iv[1])}") + f" | {t['label']} |")
    s3, acr = sc["S3_change"], sc["across"]
    L += ["", "Medians per arm are over that arm's regulators at the point.", "",
          f"**S3 (change in the contrast, {sc['primary_at']} to {sc['last_at']}): {s3['label']}.** Seeds usable at both: "
          f"{sc['usable_at_primary_and_last']}. Smaller at the end in {s3['smaller_at_end']}/{s3['n']} (sign p "
          f"{fmt(s3['sign_p'], 4)}); median {fmt(s3['first_median'])} then {fmt(s3['last_median'])}; median change "
          f"{fmt(s3['change_median'])}.", ""]
    sm = acr["stage_matched"]
    L += [f"Stage-matched (derived at {sc['last_at']} against paid at {sc['primary_at']}): derived more specific in "
          f"{sm['first_ahead']}/{sm['n']} (sign p {fmt(sm['sign_p'], 4)}); {fmt(sm['first_median'])} against "
          f"{fmt(sm['second_median'])}; median updates since regulation began "
          f"{fmt(sm['updates_since_onset_median']['DERIVED'], 0)} and {fmt(sm['updates_since_onset_median']['PAID'], 0)}; "
          f"{sm['label']}.", "",
          f"| arm (regulating at {sc['primary_at']} and {sc['last_at']}) | measure | higher at the end | sign p | at the end | "
          "before | median change |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for arm, d in acr["change"].items():
        for name, t in d.items():
            L.append(f"| {arm} | {name} | {t['first_ahead']}/{t['n']} | {fmt(t['sign_p'], 4)} | {fmt(t['first_median'])} | "
                     f"{fmt(t['second_median'])} | {fmt(t['difference_median'])} |")
    L.append("")
    for p in pts:
        c, s = sc["points"][str(p)], sc["secondary"][str(p)]
        g = c["G1_combined"]
        tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)})"
        oc = s["own_above_cross"]
        L += [f"At {p} updates. K, derived against paid: {tt(g)}, {fmt(g['first_median'])} against {fmt(g['second_median'])}, "
              f"{g['label']}. Other-meal K: {tt(s['cross_K'])}, {s['cross_K']['label']}. Specificity on all seeds "
              f"{tt(s['spec_all_seeds'])}; pairs within 0.05 {tt(s['spec_tight_pairs'])}; specific share {tt(s['share'])}; "
              f"S part {tt(s['spec_S'])}; M part {tt(s['spec_M'])}; away from the other kind of meal {tt(s['spec_clean'])}; "
              f"variable 0 {tt(s['spec_each_variable'][0])}, variable 1 {tt(s['spec_each_variable'][1])}. Own-meal K above "
              f"other-meal K within arm: derived {tt(oc['DERIVED'])}, paid {tt(oc['PAID'])}.", ""]
    sp = sc["points"][str(pts[-1])]["learning_speed"]
    on = acr["onset_median_updates"]
    L += [f"Derived reached sustained regulation sooner than paid in {sp['derived_sooner']}/{sp['n']} (p {fmt(sp['sign_p'], 4)}); "
          f"median updates to sustained regulation: derived {fmt(on['DERIVED'], 0)}, paid {fmt(on['PAID'], 0)}. No-fate task "
          f"accuracy {fmt(sc['points'][str(pts[-1])]['nofate_accuracy_median'])}.", ""]
    return "\n".join(L)


def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
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
    wc, tc, seeds, points, sizes, stages = configs(args.mode)
    wcd, tcd = asdict(wc), asdict(tc)
    wdir, pdir = os.path.join(args.out, "weights"), os.path.join(args.out, "partial")
    os.makedirs(wdir, exist_ok=True)
    os.makedirs(pdir, exist_ok=True)
    t0 = time.time()
    jobs = [(s, wcd, tcd, RATE, list(points), PAY, sizes, stages) for s in seeds]
    ppath = lambda seed: os.path.join(pdir, f"seed{seed}.json")
    recs, todo = [], []
    for job in jobs:                                         # keep what an interrupted run finished
        if os.path.exists(ppath(job[0])):
            recs.append(json.load(open(ppath(job[0]))))
        else:
            todo.append(job)
    done = len(jobs) - len(todo)
    if done:
        print(f"resuming: {done} of {len(jobs)} jobs already finished", flush=True)
    from multiprocessing import Pool
    with Pool(os.cpu_count() or 1) as pool:
        for k, r in enumerate(pool.imap_unordered(run_seed_s, todo), done + 1):
            for name, b in r["weights"].items():
                arm, p = name.split("@")
                torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}_{p}.pt"))
            with open(ppath(r["seed"]) + ".tmp", "w") as fh:
                json.dump(strip(r), fh)
            os.replace(ppath(r["seed"]) + ".tmp", ppath(r["seed"]))
            recs.append(json.load(open(ppath(r["seed"]))))
            print(f"[job {k}/{len(jobs)}] seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE, "pay": PAY, "points": list(points),
            "seeds": seeds, "sizes": list(sizes), "seconds": round(sum(r["seconds"] for r in recs), 1),
            "resumed_jobs": done, "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "seeds": recs}, fh)
    sc = score(recs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    for p in sc["points_at"]:
        c = sc["points"][str(p)]
        print(p, "regulators:", c["regulators"], "usable:", c["usable"], c["G0_regulation"]["label"],
              sc.get("secondary", {}).get(str(p), {}).get("spec", {}).get("label"))
    print("S0", sc["S0_regulation"]["label"], "S3", sc.get("S3_change", {}).get("label"), "overall", sc.get("overall"),
          "weak" if sc.get("weak") else "")


if __name__ == "__main__":
    main()
