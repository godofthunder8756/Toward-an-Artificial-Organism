"""Track C P1f: confirmation of the self-monitor with exposure secured, and the second-order test (Layer 4).
Runner and scorer.

    python run_p1f_confirm.py --mode stage0 --out p1f_stage0                         # declared stage 0 on P1e's nets
    python run_p1f_confirm.py --mode final --out p1f_confirm [--max-new 4]           # after the freeze
    python run_p1f_confirm.py --mode smoke --out <scratch dir>                       # pipeline check
    python run_p1f_confirm.py --mode calib --out <dir> --round R --rate X            # calibration (blind summary)
    python run_p1f_confirm.py --calib-summary <dir>                                  # re-print a calibration summary
    python run_p1f_confirm.py --score p1f_confirm                                    # re-score saved raw results
    python run_p1f_confirm.py --score-stage0 p1f_stage0                              # re-score stage 0

Training and the P1e measures are P1e's, unchanged (trackc_swap.selfmon.run_seed_m, run_p1e_selfmon.measures);
only the damage rate differs (calibrated). The second-order pass (trackc_swap.secondorder) runs on the trained
weights of every arm at every point. Finished jobs are kept in <out>/partial; --max-new N runs at most N
unfinished jobs and stops.

Protocol and decision rules: P1F_CONFIRM_PROTOCOL.md. Simulated variables only; no operator-stop variable
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
from multiprocessing import Pool

import torch

import run_p1e_selfmon as R
from run_p1_selfeval import VALID_CLEAR_CORRECT, one_sample
from run_trackc_paid import PAY, WEAR
from run_trackc_paid2 import ALPHA, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.secondorder import BIN_MIN, DEC_BINS, EVAL_TAG_F, evaluate_second_order
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from trackc_swap.selfeval import DRAIN_SHIFT
from trackc_swap.selfmon import ARMS_M, EARLY, LATE, SPLIT_K, SPLIT_P, run_seed_m
from trackc_swap.train import TrainConfig

ARMS = ARMS_M
RATE_F = None            # per-step damage probability per unit gain: set by calibration at the freeze
P_MAX_F = 0.3            # cap on the per-step damage probability (P1e's)
FINAL_SEEDS = list(range(3000, 3028))
CALIB_SEEDS = list(range(10300, 10324))          # rounds of 8: 10300-10307, 10308-10315, 10316-10323
STAGE0_DIR = "p1e_selfmon"                       # P1e's saved weights, seeds 2800-2827
STAGE0_POINT = 3600
POINTS = R.POINTS                                 # 1800, 3600 (primary)
THIN_COVERAGE = 0.25     # flag: PFATE's median share of conflict trials in matched bins (own margin) below this
NAMES = ("P1F_1", "P1F_2", "P1F_3")
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/train.py", "trackc_swap/factorial.py",
           "trackc_swap/agent.py", "trackc_swap/selfeval.py", "trackc_swap/selfcomp.py", "trackc_swap/selfmon.py",
           "trackc_swap/secondorder.py", "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py",
           "run_p1_selfeval.py", "run_p1e_selfmon.py", "run_p1f_confirm.py", "test_p1f_confirm.py",
           "P1F_CONFIRM_PROTOCOL.md"]


def configs(mode, rnd=1):
    """(world, train config, seeds, points)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_SEEDS[8 * (rnd - 1): 8 * rnd], POINTS
    if mode == "stage0":
        return WorldConfig(wear=WEAR), TrainConfig(), R.FINAL_SEEDS, (STAGE0_POINT,)
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=32, eval_episodes=1), [9000, 9001], (10, 20)


# ---------------------------------------------------------------- jobs
def run_seed_f(job):
    """job = P1e's run_seed_m job + (second_order,). Trains as P1e, then (unless calibrating) runs the
    second-order pass on every arm's weights at every point."""
    *mjob, second = job
    torch.set_num_threads(1)
    r = run_seed_m(tuple(mjob))
    if second:
        seed, wcd, tcd, pay = mjob[0], mjob[1], mjob[2], mjob[4]
        wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
        t0 = time.time()
        r["second_order"] = {str(p): {a: evaluate_second_order(a, seed, state_from_bytes(r["weights"][f"{a}@{p}"]), wc, tc, pay)
                                      for a in ARMS} for p in r["points_at"]}
        r["seconds_second_order"] = round(time.time() - t0, 1)
        r["seconds"] = round(r["seconds"] + r["seconds_second_order"], 1)
    return r


def run_stage0_seed(job):
    """job = (seed, wcd, tcd, pay, weight dir, point): the second-order pass on P1e's saved weights."""
    seed, wcd, tcd, pay, wdir, p = job
    torch.set_num_threads(1)
    t0 = time.time()
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    so = {a: evaluate_second_order(a, seed, torch.load(os.path.join(wdir, f"seed{seed}_{a}_{p}.pt"), weights_only=False),
                                   wc, tc, pay) for a in ARMS}
    return {"seed": seed, "point": p, "second_order": {str(p): so}, "seconds": round(time.time() - t0, 1)}


def run_jobs(out, jobs, max_new, fn, keep_weights=True):
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
            for k, r in enumerate(pool.imap_unordered(fn, todo), done + 1):
                if keep_weights and "weights" in r:
                    for name, b in r["weights"].items():
                        arm, p = name.split("@")
                        torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}_{p}.pt"))
                r = json.loads(json.dumps(R.strip(r), default=float))
                with open(ppath(r["seed"]) + ".tmp", "w") as fh:
                    json.dump(r, fh)
                os.replace(ppath(r["seed"]) + ".tmp", ppath(r["seed"]))
                recs.append(r)
                print(f"[job {k}/{len(jobs)}] seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    return recs, done


# ---------------------------------------------------------------- second-order measures
def so_run(rec, p, arm, tag, key):
    x = (rec.get("second_order", {}).get(str(p), {}).get(arm, {}).get(tag) or {}).get(key)
    return x or {}


def avail_mean(vals):
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else None


def so_measures(rec, p, arm):
    """M2 at matched own margin and at matched LDA margin: the mean over EARLY and LATE of the runs that
    have one; coverage likewise; the raw (unmatched) difference for reference."""
    out = {}
    for key in ("own", "lda"):
        e, l = so_run(rec, p, arm, "early", key), so_run(rec, p, arm, "late", key)
        out[f"M2_{key}"] = avail_mean([e.get("M2"), l.get("M2")])
        out[f"M2_{key}_early"] = e.get("M2")
        out[f"M2_{key}_late"] = l.get("M2")
        out[f"coverage_{key}"] = avail_mean([e.get("coverage") if e.get("M2") is not None else None,
                                             l.get("coverage") if l.get("M2") is not None else None])
        out[f"raw_{key}"] = avail_mean([e.get("raw"), l.get("raw")])
        out[f"conf_conflict_{key}"] = avail_mean([e.get("median_conflict"), l.get("median_conflict")])
        out[f"conf_same_{key}"] = avail_mean([e.get("median_same"), l.get("median_same")])
    return out


SO_KEYS = ("M2_own", "M2_own_early", "M2_own_late", "M2_lda", "M2_lda_early", "M2_lda_late", "coverage_own",
           "coverage_lda", "raw_own", "conf_conflict_own", "conf_same_own", "conf_conflict_lda", "conf_same_lda")


def so_tests(per, P, one):
    return {
        "M2_own_PFATE_vs_PNOFATE": pair_test(P("M2_own", "PFATE", "PNOFATE"), lambda v: v, "DERIVED", "HOST"),
        "M2_own_PYOKED_vs_PNOFATE": pair_test(P("M2_own", "PYOKED", "PNOFATE"), lambda v: v, "DERIVED", "HOST"),
        "M2_lda_PFATE_vs_PNOFATE": pair_test(P("M2_lda", "PFATE", "PNOFATE"), lambda v: v, "DERIVED", "HOST"),
        "M2_lda_PYOKED_vs_PNOFATE": pair_test(P("M2_lda", "PYOKED", "PNOFATE"), lambda v: v, "DERIVED", "HOST"),
        "M2_own_PFATE_vs_PYOKED": pair_test(P("M2_own", "PFATE", "PYOKED"), lambda v: v, "DERIVED", "YOKED"),
        "routes": {k: {a: one(k, a) for a in ARMS} for k in ("M2_own", "M2_own_early", "M2_own_late", "M2_lda")}}


# ---------------------------------------------------------------- stage 0 (declared; not the confirmation)
def score_stage0(recs):
    p = STAGE0_POINT
    per = {r["seed"]: {a: so_measures(r, p, a) for a in ARMS} for r in recs}
    P = lambda key, a, b: [(per[s][a][key], per[s][b][key]) for s in per]
    one = lambda key, a: one_sample([per[s][a][key] for s in per], "PRESENT", "REVERSED")
    sc = {"n_seeds": len(recs), "point": p, "per_seed": per,
          "arms": {a: {k: med(per[s][a][k] for s in per) for k in SO_KEYS} for a in ARMS},
          "tests": so_tests(per, P, one)}
    lab = sc["tests"]["M2_own_PFATE_vs_PNOFATE"]["label"]
    sc["stage0"] = {"DERIVED_AHEAD": "SECOND_ORDER_SIGNAL", "UNDETERMINED": "UNDETERMINED"}.get(lab, "FIRST_ORDER_ONLY")
    sc["thin"] = (sc["arms"]["PFATE"]["coverage_own"] or 0.0) < THIN_COVERAGE
    return sc


def report_stage0(sc):
    tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)}; {fmt(t['first_median'])} against {fmt(t['second_median'])}) {t['label']}"
    os1 = lambda t: f"{t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'])}) {t['label']}"
    L = ["# Track C P1f stage 0: the second-order test on P1e's nets (declared; not the confirmation)", "",
         f"**Stage 0: {sc['stage0']}{' (thin overlap)' if sc['thin'] else ''}.** P1e's saved weights at {sc['point']}, "
         f"seeds {min(sc['per_seed'])}-{max(sc['per_seed'])} ({sc['n_seeds']}). P1e's run was INVALID on exposure.", "",
         f"Matched confidence: {DEC_BINS} quantile bins, at least {BIN_MIN} conflict and {BIN_MIN} same trials per kept bin; "
         f"split probe on {fmt(SPLIT_P)} of the trials at delay step {EARLY} and {LATE}; no drain; evaluation tag {EVAL_TAG_F}.", ""]
    cols = SO_KEYS
    L += ["| arm | " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * (len(cols) + 1)) + " |"]
    for a in ARMS:
        L.append(f"| {a} | " + " | ".join(fmt(sc["arms"][a][k]) for k in cols) + " |")
    L.append("")
    t = sc["tests"]
    L += [f"- {k}: {tt(v)}" for k, v in t.items() if k != "routes"]
    L += [f"- route {k}: " + "; ".join(f"{a} {os1(v[a])}" for a in ARMS) for k, v in t["routes"].items()]
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- final scoring
def score_point(seeds, i):
    out = R.score_point(seeds, i)
    p = out["iters"]
    per = {s["seed"]: {a: R.measures(s["points"][i], a) | so_measures(s, p, a) for a in ARMS} for s in seeds}
    out["per_seed"] = per
    keys = R.KEYS + SO_KEYS
    out["arms"] = {a: {k: med(per[s][a][k] for s in per) for k in keys} for a in ARMS}
    P = lambda key, a, b: [(per[s][a][key], per[s][b][key]) for s in per]
    one = lambda key, a: one_sample([per[s][a][key] for s in per], "PRESENT", "REVERSED")
    out["P1F_1"] = out.pop("P1E_1")
    out["P1F_2"] = pair_test(P("M2_own", "PFATE", "PNOFATE"), lambda v: v, "DERIVED", "HOST")
    out["P1F_3"] = out.pop("P1E_3")
    out["secondary"]["M_early_PFATE_vs_PNOFATE"] = out.pop("P1E_2")
    so = so_tests(per, P, one)
    out["secondary"]["routes"].update(so.pop("routes"))
    out["secondary"].update(so)
    return out


def overall(sc):
    p = sc["points"][str(sc["primary_at"])]
    if not sc["valid"]:
        return "INVALID"
    l1, l2 = p["P1F_1"]["label"], p["P1F_2"]["label"]
    if l1 == "UNDETERMINED":
        return "UNDETERMINED"
    if l1 != "DERIVED_AHEAD":
        return "NOT_CONFIRMED"
    if l2 == "DERIVED_AHEAD":
        return "MONITOR_SECOND_ORDER"
    if l2 == "UNDETERMINED":
        return "MONITOR_ORDER_UNDETERMINED"
    return "MONITOR_FIRST_ORDER"


def arrow(sc):
    lab = sc["points"][str(sc["primary_at"])]["P1F_3"]["label"]
    return {"DERIVED_AHEAD": "FATE_STRENGTHENS_MONITOR", "YOKED_AHEAD": "FATE_SUBSTITUTES_FOR_MONITOR",
            "NO_DIFFERENCE_DETECTED": "EXPOSURE_SUFFICES"}.get(lab, "UNDETERMINED")


def score(seeds):
    pts = [p["iters"] for p in seeds[0]["points"]]
    i_pri = len(pts) - 1
    sc = {"n_seeds": len(seeds), "points_at": pts, "primary_at": pts[-1], "params": seeds[0]["params"],
          "rate": seeds[0]["rate"], "p_max": seeds[0]["p_max"],
          "phase1_clear_correct_median": med(R.phase1_clear(s) for s in seeds),
          "phase1_conflict_accuracy_median": med(R.phase1_acc(s, "conflict") for s in seeds),
          "phase1_same_accuracy_median": med(R.phase1_acc(s, "same") for s in seeds),
          "exposure_median": med(s["points"][i_pri]["natural"]["PFATE"]["probes"].get("share_conflict") for s in seeds),
          "points": {str(p): score_point(seeds, i) for i, p in enumerate(pts)}}
    v1, v2, v3 = sc["phase1_clear_correct_median"], sc["phase1_conflict_accuracy_median"], sc["exposure_median"]
    sc["valid_memory"] = v1 is not None and v1 >= VALID_CLEAR_CORRECT
    sc["valid_damage"] = v2 is not None and v2 <= R.DAMAGE_MAX
    sc["valid_exposure"] = v3 is not None and v3 >= R.EXPOSURE_MIN
    sc["valid"] = sc["valid_memory"] and sc["valid_damage"] and sc["valid_exposure"]
    p = sc["points"][str(sc["primary_at"])]
    sc["overall"] = overall(sc)
    sc["arrow"] = arrow(sc) if sc["valid"] else "NOT_APPLICABLE"
    sc["holm"] = dict(zip(NAMES, holm([p[k]["sign_p"] for k in NAMES])))
    need = {"MONITOR_FIRST_ORDER": ("P1F_1",), "MONITOR_ORDER_UNDETERMINED": ("P1F_1",),
            "MONITOR_SECOND_ORDER": ("P1F_1", "P1F_2")}
    sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
    acc = p["arms"]["PFATE"]["acc_conflict"]
    sc["hardened"] = acc is not None and acc > R.HARDEN_MAX
    cov = p["arms"]["PFATE"]["coverage_own"]
    sc["thin"] = cov is None or cov < THIN_COVERAGE
    return sc


def report(sc):
    tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)}; {fmt(t['first_median'])} against {fmt(t['second_median'])}) {t['label']}"
    os1 = lambda t: f"{t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'])}) {t['label']}"
    L = ["# Track C P1f: confirmation of the self-monitor and the second-order test (Layer 0 -> Layer 4)", "",
         f"**Overall: {sc['overall']}{' (weak)' if sc['weak'] else ''}{' (thin overlap)' if sc['thin'] else ''}.** "
         f"L0 reading: {sc['arrow']}. Hardened (PFATE accuracy under the conflict probe > {R.HARDEN_MAX}): {sc['hardened']}. "
         "Holm-adjusted p: " + ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm"].items()) + ".", "",
         f"Valid: {sc['valid']} (phase 1: clear correct {fmt(sc['phase1_clear_correct_median'])}, needed >= {VALID_CLEAR_CORRECT}; "
         f"accuracy under the conflict probe {fmt(sc['phase1_conflict_accuracy_median'])}, needed <= {R.DAMAGE_MAX} "
         f"(same probe {fmt(sc['phase1_same_accuracy_median'])}); PFATE clear trials with a conflict event "
         f"{fmt(sc['exposure_median'])}, needed >= {R.EXPOSURE_MIN}). Parameters: {sc['params']['PLAIN']}. "
         f"Damage: {SPLIT_K} units from a donor, per-step probability min({sc['p_max']}, {sc['rate']} x gain), once per trial. "
         f"Probe at delay step {EARLY} (early) and {LATE} (late) on {fmt(SPLIT_P)} of the trials. Drain shift {DRAIN_SHIFT}. "
         f"Matched confidence: {DEC_BINS} quantile bins, at least {BIN_MIN} of each kind per kept bin.", ""]
    cols = ("M", "M_early", "M_late", "M2_own", "M2_lda", "coverage_own", "coverage_lda", "raw_own", "Q_early",
            "acc_conflict", "drain_effect", "nat_M", "share_conflict", "in_band")
    L += ["| updates | arm | " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * (len(cols) + 2)) + " |"]
    for p, x in sc["points"].items():
        for a in ARMS:
            L.append(f"| {p} | {a} | " + " | ".join(fmt(x["arms"][a][k]) for k in cols) + " |")
    L.append("")
    for p, x in sc["points"].items():
        sx = x["secondary"]
        L += [f"## At {p}", "",
              f"- P1F-1 monitor confirmed, M PFATE against PNOFATE: {tt(x['P1F_1'])}",
              f"- P1F-2 second order, M2 (matched own margin) PFATE against PNOFATE: {tt(x['P1F_2'])}",
              f"- P1F-3 the L0 arrow, M PFATE against PYOKED: {tt(x['P1F_3'])}"]
        L += [f"- {k}: {tt(v)}" for k, v in sx.items() if k != "routes"]
        L += [f"- route {k}: " + "; ".join(f"{a} {os1(v[a])}" for a in ARMS) for k, v in sx["routes"].items()]
        L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke", "calib", "stage0"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    ap.add_argument("--score-stage0")
    ap.add_argument("--calib-summary")
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--rate", type=float, default=RATE_F)
    ap.add_argument("--p-max", type=float, default=P_MAX_F)
    ap.add_argument("--max-new", type=int, default=0, help="run at most this many unfinished jobs, then stop (0: all)")
    args = ap.parse_args()
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            print(report(score(json.load(fh)["seeds"])))
        return
    if args.score_stage0:
        with open(os.path.join(args.score_stage0, "raw.json")) as fh:
            print(report_stage0(score_stage0(json.load(fh)["seeds"])), end="")
        return
    if args.calib_summary:
        pdir = os.path.join(args.calib_summary, "partial")
        recs = [json.load(open(os.path.join(pdir, f))) for f in sorted(os.listdir(pdir)) if f.endswith(".json")]
        print(R.calib_summary(recs).replace("P1e calibration", "P1f calibration"))
        return
    if args.mode == "final" and (RATE_F is None or args.rate != RATE_F or args.p_max != P_MAX_F):
        sys.exit("final mode runs only at the frozen RATE_F and P_MAX_F")
    if args.mode in ("calib", "smoke") and args.rate is None:
        sys.exit("--rate is required before the freeze")
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, points = configs(args.mode, args.round)
    wcd, tcd = asdict(wc), asdict(tc)
    if args.mode == "stage0":
        jobs = [(s, wcd, tcd, PAY[1], os.path.join(STAGE0_DIR, "weights"), STAGE0_POINT) for s in seeds]
        recs, done = run_jobs(args.out, jobs, args.max_new, run_stage0_seed, keep_weights=False)
        if len(recs) < len(jobs):
            print(f"stopped after this batch: {len(recs)} of {len(jobs)} jobs finished", flush=True)
            return
        recs.sort(key=lambda r: r["seed"])
        meta = {"mode": "stage0", "weights": STAGE0_DIR, "point": STAGE0_POINT, "seeds": seeds, "eval_tag": EVAL_TAG_F,
                "bins": DEC_BINS, "bin_min": BIN_MIN, "split_p": SPLIT_P, "early": EARLY, "late": LATE,
                "seconds": round(sum(r["seconds"] for r in recs), 1), "resumed_jobs": done,
                "python": platform.python_version(), "torch": torch.__version__,
                "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
        with open(path, "w") as fh:
            json.dump({"meta": meta, "seeds": recs}, fh)
        sc = score_stage0(recs)
        with open(os.path.join(args.out, "scores.json"), "w") as fh:
            json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
        with open(os.path.join(args.out, "STAGE0_REPORT.md"), "w") as fh:
            fh.write(report_stage0(sc))
        print(report_stage0(sc), end="")
        return
    reg = REG_ITERS_C if args.mode != "smoke" else 10
    warm = WARM_ITERS_C if args.mode != "smoke" else 10
    second = args.mode != "calib"                 # calibration is blind: no second-order pass
    jobs = [(s, wcd, tcd, list(points), PAY[1], 2, warm, WARM_WRONG_C, reg, args.rate, args.p_max, second) for s in seeds]
    recs, done = run_jobs(args.out, jobs, args.max_new, run_seed_f, keep_weights=args.mode != "calib")
    if len(recs) < len(jobs):
        print(f"stopped after this batch: {len(recs)} of {len(jobs)} jobs finished", flush=True)
        return
    recs.sort(key=lambda r: r["seed"])
    if args.mode == "calib":
        s = R.calib_summary(recs).replace("P1e calibration", "P1f calibration")
        with open(os.path.join(args.out, "CALIB_SUMMARY.md"), "w") as fh:
            fh.write(s)
        print(s)
        return
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": args.rate, "p_max": args.p_max, "split_k": SPLIT_K,
            "split_p": SPLIT_P, "early": EARLY, "late": LATE, "probe_shift": DRAIN_SHIFT, "wrong_ramp": WRONG_RAMP_C,
            "reg_iters_phase1": reg, "pay": PAY[1], "drive_all_arms": True, "points": list(points), "stages": 2,
            "seeds": seeds, "warm_iters": warm, "warm_wrong": WARM_WRONG_C, "eval_tag_second_order": EVAL_TAG_F,
            "bins": DEC_BINS, "bin_min": BIN_MIN,
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
