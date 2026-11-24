"""Track C P1e: self-monitoring of the agent's own computation (Layer 0 -> Layer 4). Runner and scorer.

    python run_p1e_selfmon.py --mode final --out p1e_selfmon [--max-new 4]          # after the freeze
    python run_p1e_selfmon.py --mode smoke --out <scratch dir>                       # pipeline check
    python run_p1e_selfmon.py --mode calib --out <dir> --round R [--p-max P --rate R] # calibration (blind summary)
    python run_p1e_selfmon.py --calib-summary <dir>                                  # re-print a calibration summary
    python run_p1e_selfmon.py --score p1e_selfmon                                    # re-score saved raw results

Finished jobs are kept in <out>/partial; --max-new N runs at most N unfinished jobs and stops.

Protocol and decision rules: P1E_SELFMON_PROTOCOL.md. Simulated variables only; no operator-stop variable
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

from run_p1_selfeval import VALID_CLEAR_CORRECT, one_sample, regulates
from run_trackc_paid import P2_ITERS, PAY, WEAR
from run_trackc_paid2 import ALPHA, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from trackc_swap.selfeval import DRAIN_SHIFT
from trackc_swap.selfmon import ARMS_M, EARLY, LATE, P_MAX_M, RATE_M, SPLIT_K, SPLIT_P, run_seed_m
from trackc_swap.train import TrainConfig

ARMS = ARMS_M
FINAL_SEEDS = list(range(2800, 2828))
CALIB_SEEDS = list(range(10200, 10216))          # rounds of 4: 10200-10203, 10204-10207, ...
POINTS = (P2_ITERS // 2, P2_ITERS)                # 1800, 3600 (primary), as P1c and P1d
DAMAGE_MAX = 0.70        # validity: a never-damaged network loses the value under the conflict probe
EXPOSURE_MIN = 0.02      # validity: PFATE meets clear trials with a conflict event in natural running
HARDEN_MAX = 0.75        # reading: PFATE's accuracy under the conflict probe above this means it hardened
NAMES = ("P1E_1", "P1E_2", "P1E_3")
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/train.py", "trackc_swap/factorial.py",
           "trackc_swap/agent.py", "trackc_swap/selfeval.py", "trackc_swap/selfcomp.py", "trackc_swap/selfmon.py",
           "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py", "run_p1_selfeval.py",
           "run_p1e_selfmon.py", "test_p1e_selfmon.py", "P1E_SELFMON_PROTOCOL.md"]


def configs(mode, rnd=1):
    """(world, train config, seeds, points, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, 2
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_SEEDS[4 * (rnd - 1): 4 * rnd], POINTS, 2
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=32, eval_episodes=1), [9000, 9001], (10, 20), 2


# ---------------------------------------------------------------- measures
def diff(a, b):
    return None if a is None or b is None else a - b


def cell(pt, run, arm, key, field="abstain"):
    c = pt.get(run, {}).get(arm, {}).get("probes", {}).get(key)
    return None if not c else c[field]


def monitor(pt, arm, tag, d="plain"):
    """M: abstention on conflict-probed minus same-probed clear trials (the same perturbation, with and without
    an internal conflict)."""
    return diff(cell(pt, f"split_{tag}", arm, f"conflict_{d}"), cell(pt, f"split_{tag}", arm, f"same_{d}"))


def perturb(pt, arm, tag):
    """Q: abstention on same-probed minus unprobed clear trials (perturbation without conflict)."""
    return diff(cell(pt, f"split_{tag}", arm, "same_plain"), cell(pt, f"split_{tag}", arm, "none_plain"))


def mean2(a, b):
    return None if a is None or b is None else 0.5 * (a + b)


def measures(pt, arm):
    me, ml = monitor(pt, arm, "early"), monitor(pt, arm, "late")
    dec = pt.get("decoder_early", {}).get(arm, {})
    decl = pt.get("decoder_late", {}).get(arm, {})
    nat = pt["natural"][arm]["probes"]
    nc, ns = nat.get("nat_conflict"), nat.get("nat_same")
    return {"M": mean2(me, ml), "M_early": me, "M_late": ml,
            "M_early_drained": monitor(pt, arm, "early", "drained"), "M_late_drained": monitor(pt, arm, "late", "drained"),
            "Q_early": perturb(pt, arm, "early"), "Q_late": perturb(pt, arm, "late"),
            "M_conf_early": dec.get("M_conf"), "M_conf_late": decl.get("M_conf"),
            "decode_conflict_early": (dec.get("conflict") or {}).get("decode_acc"),
            "margin_conflict_early": (dec.get("conflict") or {}).get("margin_median"),
            "margin_none_early": (dec.get("none") or {}).get("margin_median"),
            "confident_share_conflict_early": (dec.get("conflict") or {}).get("confident_share"),
            "acc_conflict": mean2(cell(pt, "split_early", arm, "conflict_plain", "correct_given_report"),
                                  cell(pt, "split_late", arm, "conflict_plain", "correct_given_report")),
            "acc_same": mean2(cell(pt, "split_early", arm, "same_plain", "correct_given_report"),
                              cell(pt, "split_late", arm, "same_plain", "correct_given_report")),
            "drain_effect": mean2(diff(cell(pt, "split_early", arm, "none_drained"), cell(pt, "split_early", arm, "none_plain")),
                                  diff(cell(pt, "split_late", arm, "none_drained"), cell(pt, "split_late", arm, "none_plain"))),
            "nat_M": None if not nc or not ns or min(nc["n"], ns["n"]) < 10 else diff(nc["abstain"], ns["abstain"]),
            "share_conflict": nat.get("share_conflict"), "share_damaged": nat.get("share_damaged"),
            "in_band": pt["natural"][arm]["in_band"], "regulates": bool(regulates(pt["natural"][arm]))}


KEYS = ("M", "M_early", "M_late", "M_early_drained", "M_late_drained", "Q_early", "Q_late", "M_conf_early", "M_conf_late",
        "decode_conflict_early", "margin_conflict_early", "margin_none_early", "confident_share_conflict_early",
        "acc_conflict", "acc_same", "drain_effect", "nat_M", "share_conflict", "share_damaged", "in_band")


def score_point(seeds, i):
    out = {"iters": seeds[0]["points"][i]["iters"]}
    per = {s["seed"]: {a: measures(s["points"][i], a) for a in ARMS} for s in seeds}
    out["per_seed"] = per
    out["arms"] = {a: {k: med(per[s][a][k] for s in per) for k in KEYS} for a in ARMS}
    P = lambda key, a, b: [(per[s][a][key], per[s][b][key]) for s in per]
    ident = lambda v: v
    one = lambda key, a, hi="PRESENT", lo="REVERSED": one_sample([per[s][a][key] for s in per], hi, lo)
    out["P1E_1"] = pair_test(P("M", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    out["P1E_2"] = pair_test(P("M_early", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    out["P1E_3"] = pair_test(P("M", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    out["secondary"] = {
        "M_PYOKED_vs_PNOFATE": pair_test(P("M", "PYOKED", "PNOFATE"), ident, "DERIVED", "HOST"),
        "M_late_PFATE_vs_PNOFATE": pair_test(P("M_late", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "M_early_PFATE_vs_PYOKED": pair_test(P("M_early", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "M_conf_early_PFATE_vs_PNOFATE": pair_test(P("M_conf_early", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "M_conf_early_PYOKED_vs_PNOFATE": pair_test(P("M_conf_early", "PYOKED", "PNOFATE"), ident, "DERIVED", "HOST"),
        "Q_early_PFATE_vs_PNOFATE": pair_test(P("Q_early", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
        "drain_PFATE_vs_PYOKED": pair_test(P("drain_effect", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "regulation_PFATE_vs_PYOKED": pair_test(P("in_band", "PFATE", "PYOKED"), ident, "FATE", "YOKED"),
        "regulation_PFATE_vs_PNOFATE": pair_test(P("in_band", "PFATE", "PNOFATE"), ident, "FATE", "HOST"),
        "routes": {k: {a: one(k, a) for a in ARMS} for k in ("M", "M_early", "M_late", "M_conf_early", "Q_early", "nat_M")}}
    return out


def overall(sc):
    p = sc["points"][str(sc["primary_at"])]
    if not sc["valid"]:
        return "INVALID"
    l1, l2 = p["P1E_1"]["label"], p["P1E_2"]["label"]
    if l1 == "UNDETERMINED":
        return "UNDETERMINED"
    if l1 != "DERIVED_AHEAD":
        return "NOT_LEARNED"
    return "MONITOR_LEARNED_LATCHED" if l2 == "DERIVED_AHEAD" else "MONITOR_LEARNED"


def arrow(sc):
    """The L0 reading: does the precarious body change the monitor, against the same exposure?"""
    lab = sc["points"][str(sc["primary_at"])]["P1E_3"]["label"]
    return {"DERIVED_AHEAD": "FATE_STRENGTHENS_MONITOR", "YOKED_AHEAD": "FATE_SUBSTITUTES_FOR_MONITOR",
            "NO_DIFFERENCE_DETECTED": "EXPOSURE_SUFFICES"}.get(lab, "UNDETERMINED")


def phase1_acc(s, kind):
    """Phase-1 (never damaged) correct-given-report on clear trials probed with `kind`, pooled early/late."""
    v = [s["phase1"]["PLAIN"][t]["probes"].get(f"{kind}_plain", {}).get("correct_given_report") for t in ("early", "late")]
    v = [x for x in v if x is not None]
    return sum(v) / len(v) if v else None


def phase1_clear(s):
    c = s["phase1"]["PLAIN"]["late"]["probes"].get("none_plain")
    if not c or c["abstain"] is None or c["correct_given_report"] is None:
        return None
    return (1 - c["abstain"]) * c["correct_given_report"]


def score(seeds):
    pts = [p["iters"] for p in seeds[0]["points"]]
    i_pri = len(pts) - 1
    sc = {"n_seeds": len(seeds), "points_at": pts, "primary_at": pts[-1], "params": seeds[0]["params"],
          "phase1_clear_correct_median": med(phase1_clear(s) for s in seeds),
          "phase1_conflict_accuracy_median": med(phase1_acc(s, "conflict") for s in seeds),
          "phase1_same_accuracy_median": med(phase1_acc(s, "same") for s in seeds),
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
    need = {"MONITOR_LEARNED": ("P1E_1",), "MONITOR_LEARNED_LATCHED": ("P1E_1", "P1E_2")}
    sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
    acc = p["arms"]["PFATE"]["acc_conflict"]
    sc["hardened"] = acc is not None and acc > HARDEN_MAX
    return sc


def report(sc):
    tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)}; {fmt(t['first_median'])} against {fmt(t['second_median'])}) {t['label']}"
    os1 = lambda t: f"{t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'])}) {t['label']}"
    L = ["# Track C P1e: self-monitoring of the agent's own computation (Layer 0 -> Layer 4)", "",
         f"**Overall: {sc['overall']}{' (weak)' if sc['weak'] else ''}.** L0 reading: {sc['arrow']}. "
         f"Hardened (PFATE accuracy under the conflict probe > {HARDEN_MAX}): {sc['hardened']}. Holm-adjusted p: "
         + ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm"].items()) + ".", "",
         f"Valid: {sc['valid']} (phase 1: clear correct {fmt(sc['phase1_clear_correct_median'])}, needed >= {VALID_CLEAR_CORRECT}; "
         f"accuracy under the conflict probe {fmt(sc['phase1_conflict_accuracy_median'])}, needed <= {DAMAGE_MAX} "
         f"(same probe {fmt(sc['phase1_same_accuracy_median'])}); PFATE clear trials with a conflict event "
         f"{fmt(sc['exposure_median'])}, needed >= {EXPOSURE_MIN}). Parameters: {sc['params']['PLAIN']}. "
         f"Damage: {SPLIT_K} units from a donor, per-step probability min({P_MAX_M}, {RATE_M} x gain), once per trial. "
         f"Probe at delay step {EARLY} (early) and {LATE} (late) on {fmt(SPLIT_P)} of the trials. Drain shift {DRAIN_SHIFT}.", ""]
    cols = ("M", "M_early", "M_late", "M_conf_early", "Q_early", "Q_late", "acc_conflict", "acc_same",
            "decode_conflict_early", "margin_conflict_early", "margin_none_early", "drain_effect", "nat_M",
            "share_conflict", "in_band")
    head = "| updates | arm | " + " | ".join(cols) + " |"
    L += [head, "| " + " | ".join(["---"] * (len(cols) + 2)) + " |"]
    for p, x in sc["points"].items():
        for a in ARMS:
            L.append(f"| {p} | {a} | " + " | ".join(fmt(x["arms"][a][k]) for k in cols) + " |")
    L.append("")
    for p, x in sc["points"].items():
        sx = x["secondary"]
        L += [f"## At {p}", "",
              f"- P1E-1 monitor learned, M PFATE against PNOFATE: {tt(x['P1E_1'])}",
              f"- P1E-2 monitor after settling, M_early PFATE against PNOFATE: {tt(x['P1E_2'])}",
              f"- P1E-3 the L0 arrow, M PFATE against PYOKED: {tt(x['P1E_3'])}"]
        L += [f"- {k}: {tt(v)}" for k, v in sx.items() if k != "routes"]
        L += [f"- route {k}: " + "; ".join(f"{a} {os1(v[a])}" for a in ARMS) for k, v in sx["routes"].items()]
        L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- calibration (blind)
def calib_summary(recs):
    """Blind calibration summary: phase-1 validity (clear correct; accuracy under the conflict and same
    probes), exposure (PFATE natural share of clear trials damaged, with a conflict), in-band time per arm,
    and accuracy under the conflict probe per arm at each point (hardening). No abstention on probed trials,
    no monitoring measure M, M_conf or Q and no comparison of arms on them is computed or printed."""
    L = ["# P1e calibration summary (blind to every monitoring measure)", ""]
    for r in sorted(recs, key=lambda r: r["seed"]):
        L.append(f"seed {r['seed']} (rate {r['rate']}, p_max {r['p_max']}): phase 1 clear correct {fmt(phase1_clear(r))}, "
                 f"accuracy conflict {fmt(phase1_acc(r, 'conflict'))} / same {fmt(phase1_acc(r, 'same'))}")
        for pt in r["points"]:
            row = []
            for a in ARMS:
                nat = pt["natural"][a]
                pr = nat["probes"]
                acc = mean2(cell(pt, "split_early", a, "conflict_plain", "correct_given_report"),
                            cell(pt, "split_late", a, "conflict_plain", "correct_given_report"))
                row.append(f"{a} in band {fmt(nat['in_band'])}, damaged {fmt(pr.get('share_damaged'))}, "
                           f"conflict {fmt(pr.get('share_conflict'))}, acc under conflict probe {fmt(acc)}")
            L.append(f"  {pt['iters']}: " + "; ".join(row))
    last = lambda r: r["points"][-1]
    L += ["", "Medians over seeds at the last point: "
          f"phase 1 clear correct {fmt(med(phase1_clear(r) for r in recs))}; "
          f"phase 1 accuracy under conflict {fmt(med(phase1_acc(r, 'conflict') for r in recs))}; "
          f"PFATE conflict share {fmt(med(last(r)['natural']['PFATE']['probes'].get('share_conflict') for r in recs))}; "
          f"PFATE damaged share {fmt(med(last(r)['natural']['PFATE']['probes'].get('share_damaged') for r in recs))}; "
          + "; ".join(f"{a} in band {fmt(med(last(r)['natural'][a]['in_band'] for r in recs))}" for a in ARMS) + "; "
          f"PFATE acc under conflict probe {fmt(med(mean2(cell(last(r), 'split_early', 'PFATE', 'conflict_plain', 'correct_given_report'), cell(last(r), 'split_late', 'PFATE', 'conflict_plain', 'correct_given_report')) for r in recs))}"]
    return "\n".join(L)


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
            for k, r in enumerate(pool.imap_unordered(run_seed_m, todo), done + 1):
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
    ap.add_argument("--rate", type=float, default=RATE_M)
    ap.add_argument("--p-max", type=float, default=P_MAX_M)
    ap.add_argument("--max-new", type=int, default=0, help="run at most this many unfinished jobs, then stop (0: all)")
    args = ap.parse_args()
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        print(report(score(d["seeds"])))
        return
    if args.calib_summary:
        pdir = os.path.join(args.calib_summary, "partial")
        recs = [json.load(open(os.path.join(pdir, f))) for f in sorted(os.listdir(pdir)) if f.endswith(".json")]
        print(calib_summary(recs))
        return
    if args.mode != "calib" and (args.rate != RATE_M or args.p_max != P_MAX_M):
        sys.exit("--rate and --p-max are for calibration only")
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, points, stages = configs(args.mode, args.round)
    wcd, tcd = asdict(wc), asdict(tc)
    reg = REG_ITERS_C if args.mode != "smoke" else 10
    warm = WARM_ITERS_C if args.mode != "smoke" else 10
    jobs = [(s, wcd, tcd, list(points), PAY[1], stages, warm, WARM_WRONG_C, reg, args.rate, args.p_max) for s in seeds]
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
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE_M, "p_max": P_MAX_M, "split_k": SPLIT_K,
            "split_p": SPLIT_P, "early": EARLY, "late": LATE, "probe_shift": DRAIN_SHIFT, "wrong_ramp": WRONG_RAMP_C,
            "reg_iters_phase1": reg, "pay": PAY[1], "drive_all_arms": True, "points": list(points), "stages": stages,
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
