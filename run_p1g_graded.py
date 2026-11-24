"""Track C P1g: self-monitoring with exposure fixed by design and graded damage (Layer 0 -> Layer 4).

    python run_p1g_graded.py --mode smoke --base 0.012 --out /tmp/p1g_smoke                 # plumbing check
    python run_p1g_graded.py --mode calib --round R --base B --out p1g_graded_calibration/roundR  # blind summary
    python run_p1g_graded.py --mode final --out p1g_graded [--max-new N]                    # final (frozen BASE_F)
    python run_p1g_graded.py --score p1g_graded                                             # re-score
    python run_p1g_graded.py --calib-summary <dir>                                          # re-print a summary

Protocol: P1G_GRADED_PROTOCOL.md. Module: trackc_swap/gradmon.py. Simulated variables only; no operator, stop,
shutdown or host variable exists; no process is terminated.
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

import run_p1e_selfmon as R
from run_p1_selfeval import VALID_CLEAR_CORRECT, one_sample
from run_trackc_paid import PAY, WEAR
from run_trackc_paid2 import ALPHA, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.gradmon import CALIPER, EVAL_TAG_G, KS_G, NN_MIN, run_seed_g
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from trackc_swap.selfeval import DRAIN_SHIFT
from trackc_swap.selfmon import ARMS_M, EARLY, LATE, P_MAX_M, RATE_M, SPLIT_K, SPLIT_P
from trackc_swap.train import TrainConfig

ARMS = ARMS_M
BASE_F = 0.012           # base per-step damage probability: frozen after calibration round 1
FINAL_SEEDS = list(range(3200, 3228))
CALIB_SEEDS = list(range(10400, 10424))          # rounds of 8
POINTS = R.POINTS                                 # 1800, 3600 (primary)
DAMAGE_MAX, EXPOSURE_MIN, HARDEN_MAX = R.DAMAGE_MAX, R.EXPOSURE_MIN, R.HARDEN_MAX
THIN_COVERAGE = 0.25     # flag: PFATE median caliper coverage (own margin) below this
NAMES = ("P1G_1", "P1G_2", "P1G_3")
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/train.py", "trackc_swap/factorial.py",
           "trackc_swap/agent.py", "trackc_swap/selfeval.py", "trackc_swap/selfcomp.py", "trackc_swap/selfmon.py",
           "trackc_swap/secondorder.py", "trackc_swap/gradmon.py", "run_trackc_probe.py", "run_trackc_paid.py",
           "run_trackc_paid2.py", "run_p1_selfeval.py", "run_p1e_selfmon.py", "run_p1g_graded.py",
           "test_p1g_graded.py", "P1G_GRADED_PROTOCOL.md"]


def configs(mode, rnd=1):
    """(world, train config, seeds, points)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_SEEDS[8 * (rnd - 1): 8 * rnd], POINTS
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=32, eval_episodes=1), [9000, 9001], (10, 20)


# ---------------------------------------------------------------- measures
def avail_mean(vals):
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else None


def g_measures(pt, arm):
    """Second-order and graded measures, averaged over the EARLY and LATE graded runs where available."""
    runs = [pt.get(f"graded_{t}", {}).get(arm) or {} for t in ("early", "late")]

    def get(run, conf, kind, field):
        c = run.get(conf)
        return None if not c else c[kind][field]
    out = {}
    for conf in ("own", "lda"):
        e, l = (get(r, conf, "nn", "M2") for r in runs)
        out[f"M2_nn_{conf}"], out[f"M2_nn_{conf}_early"], out[f"M2_nn_{conf}_late"] = avail_mean([e, l]), e, l
        out[f"coverage_nn_{conf}"] = avail_mean([get(r, conf, "nn", "coverage") for r in runs])
        out[f"balance_{conf}"] = avail_mean([get(r, conf, "nn", "balance") for r in runs])
        out[f"M2_bins_{conf}"] = avail_mean([get(r, conf, "bins", "M2") for r in runs])
    out["own_conflict"] = avail_mean([(r.get("own") or {}).get("median_conflict") for r in runs])
    out["own_same"] = avail_mean([(r.get("own") or {}).get("median_same") for r in runs])
    for kk in KS_G:
        d = []
        for r in runs:
            c = (r.get("per_k") or {}).get(str(kk)) or {}
            if c.get("abstain_conflict") is not None and c.get("abstain_same") is not None:
                d.append(c["abstain_conflict"] - c["abstain_same"])
        out[f"M_k{kk}"] = avail_mean(d)
    return out


def measures(pt, arm):
    return R.measures(pt, arm) | g_measures(pt, arm)


KEYS = R.KEYS + ("M2_nn_own", "M2_nn_own_early", "M2_nn_own_late", "coverage_nn_own", "balance_own", "M2_bins_own",
                 "M2_nn_lda", "coverage_nn_lda", "balance_lda", "M2_bins_lda", "own_conflict", "own_same") \
    + tuple(f"M_k{k}" for k in KS_G)


def score_point(seeds, i):
    out = {"iters": seeds[0]["points"][i]["iters"]}
    per = {s["seed"]: {a: measures(s["points"][i], a) for a in ARMS} for s in seeds}
    out["per_seed"] = per
    out["arms"] = {a: {k: med(per[s][a][k] for s in per) for k in KEYS} for a in ARMS}
    P = lambda key, a, b: [(per[s][a][key], per[s][b][key]) for s in per]
    ident = lambda v: v
    one = lambda key, a: one_sample([per[s][a][key] for s in per], "PRESENT", "REVERSED")
    out["P1G_1"] = pair_test(P("M", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    out["P1G_2"] = one("M2_nn_own", "PFATE")
    out["P1G_3"] = pair_test(P("M", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    out["secondary"] = {
        "M_early_PFATE_vs_PNOFATE": pair_test(P("M_early", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "M_PYOKED_vs_PNOFATE": pair_test(P("M", "PYOKED", "PNOFATE"), ident, "DERIVED", "HOST"),
        "M2_nn_own_PFATE_vs_PYOKED": pair_test(P("M2_nn_own", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "M_conf_early_PFATE_vs_PNOFATE": pair_test(P("M_conf_early", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "drain_PFATE_vs_PYOKED": pair_test(P("drain_effect", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "regulation_PFATE_vs_PYOKED": pair_test(P("in_band", "PFATE", "PYOKED"), ident, "FATE", "YOKED"),
        "regulation_PFATE_vs_PNOFATE": pair_test(P("in_band", "PFATE", "PNOFATE"), ident, "FATE", "HOST"),
        "routes": {k: {a: one(k, a) for a in ARMS}
                   for k in ("M", "M2_nn_own", "M2_nn_own_early", "M2_nn_own_late", "M2_nn_lda", "M2_bins_own",
                             "Q_early", "nat_M") + tuple(f"M_k{k}" for k in KS_G)}}
    return out


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    p = sc["points"][str(sc["primary_at"])]
    l1, l2 = p["P1G_1"]["label"], p["P1G_2"]["label"]
    if l1 == "UNDETERMINED":
        return "UNDETERMINED"
    if l1 != "DERIVED_AHEAD":
        return "NOT_CONFIRMED"
    if l2 == "PRESENT":
        return "MONITOR_SECOND_ORDER"
    if l2 == "UNDETERMINED":
        return "MONITOR_ORDER_UNDETERMINED"
    return "MONITOR_FIRST_ORDER"


def arrow(sc):
    lab = sc["points"][str(sc["primary_at"])]["P1G_3"]["label"]
    return {"DERIVED_AHEAD": "FATE_STRENGTHENS_MONITOR", "YOKED_AHEAD": "FATE_SUBSTITUTES_FOR_MONITOR",
            "NO_DIFFERENCE_DETECTED": "EXPOSURE_SUFFICES"}.get(lab, "UNDETERMINED")


def score(seeds):
    pts = [p["iters"] for p in seeds[0]["points"]]
    i_pri = len(pts) - 1
    sc = {"n_seeds": len(seeds), "points_at": pts, "primary_at": pts[-1], "params": seeds[0]["params"],
          "phase1_clear_correct_median": med(R.phase1_clear(s) for s in seeds),
          "phase1_conflict_accuracy_median": med(R.phase1_acc(s, "conflict") for s in seeds),
          "phase1_same_accuracy_median": med(R.phase1_acc(s, "same") for s in seeds),
          "exposure_median": med(s["points"][i_pri]["natural"]["PFATE"]["probes"].get("share_conflict") for s in seeds),
          "points": {str(p): score_point(seeds, i) for i, p in enumerate(pts)}}
    v1, v2, v3 = sc["phase1_clear_correct_median"], sc["phase1_conflict_accuracy_median"], sc["exposure_median"]
    sc["valid_memory"] = v1 is not None and v1 >= VALID_CLEAR_CORRECT
    sc["valid_damage"] = v2 is not None and v2 <= DAMAGE_MAX
    sc["valid_exposure"] = v3 is not None and v3 >= EXPOSURE_MIN
    sc["valid"] = sc["valid_memory"] and sc["valid_damage"] and sc["valid_exposure"]
    p = sc["points"][str(sc["primary_at"])]
    sc["overall"] = overall(sc)
    sc["arrow"] = arrow(sc) if sc["valid"] else "NOT_APPLICABLE"
    sc["holm"] = dict(zip(NAMES, holm([p[k]["sign_p"] for k in NAMES])))
    need = {"MONITOR_FIRST_ORDER": ("P1G_1",), "MONITOR_ORDER_UNDETERMINED": ("P1G_1",),
            "MONITOR_SECOND_ORDER": ("P1G_1", "P1G_2")}
    sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
    cov = p["arms"]["PFATE"]["coverage_nn_own"]
    sc["thin"] = cov is None or cov < THIN_COVERAGE
    acc = p["arms"]["PFATE"]["acc_conflict"]
    sc["hardened"] = acc is not None and acc > HARDEN_MAX
    return sc


def report(sc):
    tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)}; {fmt(t['first_median'])} against {fmt(t['second_median'])}) {t['label']}"
    os1 = lambda t: f"{t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'])}) {t['label']}"
    flags = [f for f, on in (("weak", sc["weak"]), ("thin overlap", sc["thin"])) if on]
    L = ["# Track C P1g: self-monitoring with exposure fixed by design and graded damage (Layer 0 -> Layer 4)", "",
         f"**Overall: {sc['overall']}{' (' + ', '.join(flags) + ')' if flags else ''}.** L0 reading: {sc['arrow']}. "
         f"Hardened (PFATE accuracy under the conflict probe > {HARDEN_MAX}): {sc['hardened']}. Holm-adjusted p: "
         + ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm"].items()) + ".", "",
         f"Valid: {sc['valid']} (phase 1: clear correct {fmt(sc['phase1_clear_correct_median'])}, needed >= {VALID_CLEAR_CORRECT}; "
         f"accuracy under the conflict probe {fmt(sc['phase1_conflict_accuracy_median'])}, needed <= {DAMAGE_MAX} "
         f"(same probe {fmt(sc['phase1_same_accuracy_median'])}); PFATE clear trials with a conflict event "
         f"{fmt(sc['exposure_median'])}, needed >= {EXPOSURE_MIN}). Parameters: {sc['params']['PLAIN']}. "
         f"Damage: per-step probability min({P_MAX_M}, base {BASE_F} + {RATE_M} x gain), K units from a donor with K "
         f"in {list(KS_G)}, once per trial. Split probe A (K {SPLIT_K}, drain on half) and graded probe B (K in "
         f"{list(KS_G)}, no drain) at delay step {EARLY} (early) and {LATE} (late) on {fmt(SPLIT_P)} of the trials. "
         f"Caliper {CALIPER} pooled SD, at least {NN_MIN} pairs. Drain shift {DRAIN_SHIFT}.", ""]
    cols = ("M", "M_early", "M_late", "M2_nn_own", "M2_nn_own_early", "M2_nn_own_late", "coverage_nn_own",
            "balance_own", "M2_nn_lda", "M2_bins_own", "own_conflict", "own_same") + tuple(f"M_k{k}" for k in KS_G) \
        + ("Q_early", "acc_conflict", "drain_effect", "share_conflict", "in_band")
    L += ["| updates | arm | " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * (len(cols) + 2)) + " |"]
    for p, x in sc["points"].items():
        for a in ARMS:
            L.append(f"| {p} | {a} | " + " | ".join(fmt(x["arms"][a][k]) for k in cols) + " |")
    L.append("")
    for p, x in sc["points"].items():
        sx = x["secondary"]
        L += [f"## At {p}", "",
              f"- P1G-1 monitor confirmed, M PFATE against PNOFATE: {tt(x['P1G_1'])}",
              f"- P1G-2 second order, M2_nn_own PFATE against 0: {os1(x['P1G_2'])}",
              f"- P1G-3 the L0 arrow, M PFATE against PYOKED: {tt(x['P1G_3'])}"]
        L += [f"- {k}: {tt(v)}" for k, v in sx.items() if k != "routes"]
        L += [f"- route {k}: " + "; ".join(f"{a} {os1(v[a])}" for a in ARMS) for k, v in sx["routes"].items()]
        L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- calibration (blind)
def calib_summary(recs):
    """P1e's blind summary plus the overlap of first-order confidence on the graded probe (caliper coverage
    of conflict trials by same trials, own margin; computed from the margins alone, before any abstention)
    and the median own margins. No abstention on probed trials and no monitoring measure is printed."""
    s = R.calib_summary(recs).replace("# P1e calibration summary", "# P1g calibration summary", 1)
    L = [s, "", "Overlap on the graded probe (own margin; PFATE; EARLY / LATE): caliper coverage, median margin conflict / same"]
    covs = []
    for r in sorted(recs, key=lambda r: r["seed"]):
        pt = r["points"][-1]
        row = []
        for t in ("early", "late"):
            g = (pt.get(f"graded_{t}", {}).get("PFATE") or {}).get("own") or {}
            nn = g.get("nn") or {}
            covs.append(nn.get("coverage"))
            row.append(f"{t} {fmt(nn.get('coverage'))} ({fmt(g.get('median_conflict'))} / {fmt(g.get('median_same'))})")
        L.append(f"seed {r['seed']} at {pt['iters']}: " + "; ".join(row))
    per_seed = [avail_mean(covs[2 * i: 2 * i + 2]) for i in range(len(covs) // 2)]
    L.append(f"Median over seeds of PFATE caliper coverage (mean of EARLY and LATE): {fmt(med(per_seed))}")
    return "\n".join(L)


# ---------------------------------------------------------------- jobs
def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def run_jobs(out, jobs, max_new, keep_weights=True):
    wdir, pdir = os.path.join(out, "weights"), os.path.join(out, "partial")
    os.makedirs(pdir, exist_ok=True)
    if keep_weights:
        os.makedirs(wdir, exist_ok=True)
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
    if max_new:
        todo = todo[:max_new]
    t0 = time.time()
    if todo:
        with Pool(min(len(todo), os.cpu_count() or 1)) as pool:
            for k, r in enumerate(pool.imap_unordered(run_seed_g, todo), done + 1):
                if keep_weights:
                    for name, b in r["weights"].items():
                        arm, p = name.split("@")
                        torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}_{p}.pt"))
                r = json.loads(json.dumps(strip(r), default=float))
                with open(ppath(r["seed"]) + ".tmp", "w") as fh:
                    json.dump(r, fh)
                os.replace(ppath(r["seed"]) + ".tmp", ppath(r["seed"]))
                recs.append(r)
                print(f"[job {k}/{len(jobs)}] seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    return recs, done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke", "calib"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    ap.add_argument("--calib-summary")
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--base", type=float, default=BASE_F)
    ap.add_argument("--max-new", type=int, default=0, help="run at most this many unfinished jobs, then stop (0: all)")
    args = ap.parse_args()
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        print(report(score(d["seeds"])))
        return
    if args.calib_summary:
        pdir = os.path.join(args.calib_summary, "partial")
        recs = []
        for f in sorted(os.listdir(pdir)):
            if f.endswith(".json"):
                with open(os.path.join(pdir, f)) as fh:
                    recs.append(json.load(fh))
        print(calib_summary(recs))
        return
    if args.mode == "final" and (BASE_F is None or args.base != BASE_F):
        sys.exit("final mode runs only at the frozen BASE_F")
    if args.base is None:
        sys.exit("--base is required before the freeze")
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, points = configs(args.mode, args.round)
    wcd, tcd = asdict(wc), asdict(tc)
    reg = REG_ITERS_C if args.mode != "smoke" else 10
    warm = WARM_ITERS_C if args.mode != "smoke" else 10
    jobs = [(s, wcd, tcd, list(points), PAY[1], warm, WARM_WRONG_C, reg, RATE_M, P_MAX_M, args.base, KS_G) for s in seeds]
    recs, done = run_jobs(args.out, jobs, args.max_new, keep_weights=args.mode != "calib")
    if len(recs) < len(jobs):
        print(f"stopped after this batch: {len(recs)} of {len(jobs)} jobs finished", flush=True)
        return
    recs.sort(key=lambda r: r["seed"])
    if args.mode == "calib":
        s = calib_summary(recs)
        with open(os.path.join(args.out, "CALIB_SUMMARY.md"), "w") as fh:
            fh.write(s)
        print(s)
        return
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE_M, "p_max": P_MAX_M, "base": args.base,
            "ks": list(KS_G), "split_k": SPLIT_K, "split_p": SPLIT_P, "early": EARLY, "late": LATE,
            "caliper": CALIPER, "nn_min": NN_MIN, "eval_tag": EVAL_TAG_G, "probe_shift": DRAIN_SHIFT,
            "wrong_ramp": WRONG_RAMP_C, "reg_iters_phase1": reg, "pay": PAY[1], "points": list(points),
            "seeds": seeds, "warm_iters": warm, "warm_wrong": WARM_WRONG_C,
            "seconds": round(sum(r["seconds"] for r in recs), 1), "resumed_jobs": done,
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "seeds": recs}, fh)
    sc = score(recs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print(report(sc))


if __name__ == "__main__":
    main()
