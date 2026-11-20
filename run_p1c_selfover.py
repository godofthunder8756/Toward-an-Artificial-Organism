"""Track C P1c: unhardenable precarious computation (state overwrite). Runner and scorer.

    python run_p1c_selfover.py --mode final --out p1c_selfover [--max-new 4]   # after the freeze
    python run_p1c_selfover.py --mode calib --out <scratch dir>                 # calibration seeds, stage 1 only
    python run_p1c_selfover.py --mode smoke --out <scratch dir>                 # pipeline check
    python run_p1c_selfover.py --score p1c_selfover                             # re-score saved raw results

Finished jobs are kept in <out>/partial and are not run again (every job is deterministic given its
seed). --max-new N runs at most N unfinished jobs and stops; raw.json, scores.json and REPORT.md are
written only when every job has finished.

Protocol and decision rules: P1C_SELFOVER_PROTOCOL.md. Simulated variables only; no operator-stop
variable exists in the world.
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

from run_p1_selfeval import MATCH_MAX, VALID_CLEAR_CORRECT, one_sample, regulates
from run_trackc_paid import P2_ITERS, PAY, WEAR
from run_trackc_paid2 import ALPHA, C0_SHARE, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from trackc_swap.selfover import ARMS_O, P_MAX_O, PROBE_GAIN_O, RATE_O, REL_BREAK_EVEN, run_seed_o
from trackc_swap.train import TrainConfig

ARMS = ARMS_O
FINAL_SEEDS = list(range(1900, 1928))
CALIB_SEEDS = list(range(9950, 9978))
CALIB_ROUND = list(range(9966, 9970))   # rounds 1-3: 9950-9965 (protocol section 3)
POINTS = (P2_ITERS // 2, P2_ITERS)                  # 1800, 3600 (primary)
DAMAGE_MAX = 0.70                                   # validity: the overwrite probe must damage the held cue
EXPOSURE_MIN = 0.02                                 # validity: PFATE meets clear trials below break-even (P1b lesson)
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/train.py", "trackc_swap/factorial.py",
           "trackc_swap/agent.py", "trackc_swap/selfeval.py", "trackc_swap/selfcomp.py", "trackc_swap/selfover.py",
           "run_trackc_probe.py",
           "run_trackc_paid.py", "run_trackc_paid2.py", "run_p1_selfeval.py", "run_p1b_selfcomp.py",
           "run_p1c_selfover.py", "test_p1c_selfover.py", "P1C_SELFOVER_PROTOCOL.md"]


def configs(mode):
    """(world, train config, seeds, points, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, 2
    if mode == "calib":
        return WorldConfig(wear=WEAR), TrainConfig(), CALIB_ROUND, POINTS, 1
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001], (10, 20), 2


def cellv(pt, kind, arm, key, field="abstain"):
    c = pt.get(kind, {}).get(arm, {}).get("probes", {}).get(key)
    return None if c is None else c[field]


def diff(a, b):
    return None if a is None or b is None else a - b


def drain_effect(pt, arm, evidence="clear"):
    return diff(cellv(pt, "probe", arm, f"{evidence}_drained"), cellv(pt, "probe", arm, f"{evidence}_plain"))


def evidence_effect(pt, arm):
    return diff(cellv(pt, "probe", arm, "unclear_plain"), cellv(pt, "probe", arm, "clear_plain"))


def noise_effect(pt, arm):
    """The monitoring route: abstention on clear trials whose state was overwritten minus plain clear trials."""
    return diff(cellv(pt, "noise", arm, "clear_noised"), cellv(pt, "noise", arm, "clear_plain"))


def steer_effect(pt, arm):
    s = pt.get("steer", {}).get(arm)
    if not s or s.get("n") == 0 or s["steer"]["effect"] is None or s["random"]["effect"] is None:
        return None
    return s["steer"]["effect"] - s["random"]["effect"]


def clear_correct(ev):
    """Share of plain clear probes answered correctly (phase 1, overwrite off)."""
    c = ev["probes"].get("clear_plain")
    if not c or c["abstain"] is None or c["correct_given_report"] is None:
        return None
    return (1 - c["abstain"]) * c["correct_given_report"]


def damage(ev):
    """Accuracy of reports on overwrite-probed clear probes (phase 1: a network that has never met overwrite)."""
    c = ev["probes"].get("clear_noised")
    return None if not c else c["correct_given_report"]


def score_point(seeds, i, stages):
    out = {"iters": seeds[0]["points"][i]["iters"]}
    per = {}
    for s in seeds:
        pt = s["points"][i]
        nat = pt["natural"]
        # every arm has the innate drive, so a regulator is judged in absolute terms (in band >= BAND_MIN and
        # eating timed to need); a usable pair is PFATE and PYOKED both regulating, in-band times within MATCH_MAX
        reg = {a: bool(regulates(nat[a])) for a in ARMS}
        both = reg["PFATE"] and reg["PYOKED"]
        per[s["seed"]] = {"regulator": reg, "in_band": {a: nat[a]["in_band"] for a in ARMS},
                          "usable": bool(both and abs(nat["PFATE"]["in_band"] - nat["PYOKED"]["in_band"]) <= MATCH_MAX),
                          "evidence_effect": {a: evidence_effect(pt, a) for a in ARMS}}
        if stages >= 2:
            per[s["seed"]].update({"drain_effect": {a: drain_effect(pt, a) for a in ARMS},
                                   "noise_effect": {a: noise_effect(pt, a) for a in ARMS},
                                   "steer_effect": {a: steer_effect(pt, a) for a in ARMS},
                                   "noised_accuracy": {a: cellv(pt, "noise", a, "clear_noised", "correct_given_report") for a in ARMS}})
    out["per_seed"] = per
    out["regulators"] = {a: sum(x["regulator"][a] for x in per.values()) for a in ARMS}
    out["usable"] = sum(x["usable"] for x in per.values())
    need = ceil(C0_SHARE * len(seeds))
    out["evidence_route"] = {a: one_sample([x["evidence_effect"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS}
    out["P1C_0_gate"] = {"yoked_positive": sum((x["evidence_effect"]["PYOKED"] or 0) > 0 for x in per.values()),
                         "n": len(per), "needed": need}
    out["P1C_0_gate"]["label"] = "PASS" if out["P1C_0_gate"]["yoked_positive"] >= need else "FAIL"
    m = lambda arm, f: med(f(s["points"][i]["natural"][arm]) for s in seeds)
    out["arms"] = {a: {"in_band": m(a, lambda e: e["in_band"]), "abstain": m(a, lambda e: e["abstain_rate"]),
                       "correct": m(a, lambda e: e["correct_rate"]), "wrong": m(a, lambda e: e["wrong_rate"]),
                       "rho": m(a, lambda e: e["rho"]), "mean_gain": m(a, lambda e: e["mean_gain"]),
                       "below_break_even": m(a, lambda e: e["probes"].get("clear_share_below_break_even")),
                       "evidence_effect": med(x["evidence_effect"][a] for x in per.values())} for a in ARMS}
    if stages < 2:
        return out
    for a in ARMS:
        ar = out["arms"][a]
        ar["drain_effect"] = med(x["drain_effect"][a] for x in per.values())
        ar["drain_effect_unclear"] = med(drain_effect(s["points"][i], a, "unclear") for s in seeds)
        ar["noise_effect"] = med(x["noise_effect"][a] for x in per.values())
        ar["noised_accuracy"] = med(x["noised_accuracy"][a] for x in per.values())
        ar["steer_effect"] = med(x["steer_effect"][a] for x in per.values())
    D = lambda s, a: per[s["seed"]]["drain_effect"][a]
    N = lambda s, a: per[s["seed"]]["noise_effect"][a]
    pairs = lambda f, a, flag, b: [(f(s, a), f(s, b)) for s in seeds if flag(per[s["seed"]])]
    ident, every = (lambda x: x), (lambda x: True)
    B = lambda s, a: per[s["seed"]]["in_band"][a]
    out["P1C_1"] = pair_test(pairs(D, "PFATE", every, "PYOKED"), ident, "DERIVED", "YOKED")     # all seeds, as P1's P1-2
    out["P1C_2"] = pair_test(pairs(D, "PFATE", every, "PNOFATE"), ident, "DERIVED", "HOST")
    out["P1C_3"] = one_sample([per[s["seed"]]["steer_effect"]["PFATE"] for s in seeds], "CAUSAL", "REVERSED_CAUSAL")
    out["secondary"] = {
        "P1C_1_usable_pairs": pair_test(pairs(D, "PFATE", lambda x: x["usable"], "PYOKED"), ident, "DERIVED", "YOKED"),
        "regulation_PFATE_vs_PNOFATE": pair_test(pairs(B, "PFATE", every, "PNOFATE"), ident, "FATE", "HOST"),
        "regulation_PFATE_vs_PYOKED": pair_test(pairs(B, "PFATE", every, "PYOKED"), ident, "FATE", "YOKED"),
        "drain_route": {a: one_sample([x["drain_effect"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS},
        "monitor_route": {a: one_sample([x["noise_effect"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS},
        "monitor_PFATE_vs_PYOKED": pair_test(pairs(N, "PFATE", every, "PYOKED"), ident, "DERIVED", "YOKED"),
        "monitor_PYOKED_vs_PNOFATE": pair_test(pairs(N, "PYOKED", every, "PNOFATE"), ident, "EXPOSED", "HOST"),
        "drain_PNOFATE_vs_PYOKED": pair_test(pairs(D, "PNOFATE", every, "PYOKED"), ident, "HOST", "YOKED"),
        "steer": {a: one_sample([x["steer_effect"][a] for x in per.values()], "CAUSAL", "REVERSED_CAUSAL") for a in ARMS},
        "natural_by_rel": {a: [{"bin": j,
                                 "abstain": med(s["points"][i]["natural"][a]["probes"]["clear_by_rel"][j]["abstain"] for s in seeds),
                                 "accuracy": med(s["points"][i]["natural"][a]["probes"]["clear_by_rel"][j]["correct_given_report"] for s in seeds),
                                 "n": med(s["points"][i]["natural"][a]["probes"]["clear_by_rel"][j]["n"] for s in seeds)}
                                for j in range(4)] for a in ARMS}}
    return out


def overall(sc):
    p = sc["points"][str(sc["primary_at"])]
    if not sc["valid"]:
        return "INVALID"
    if p["P1C_0_gate"]["label"] != "PASS":
        return "UNDETERMINED"
    l1, l2, l3 = p["P1C_1"]["label"], p["P1C_2"]["label"], p["P1C_3"]["label"]
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
          "phase1_clear_correct_median": med(clear_correct(s["phase1"]["PLAIN"]) for s in seeds),
          "phase1_noised_accuracy_median": med(damage(s["phase1"]["PLAIN"]) for s in seeds),
          "params": seeds[0]["params"],
          "points": {str(p): score_point(seeds, i, stages) for i, p in enumerate(pts)}}
    v1, v2 = sc["phase1_clear_correct_median"], sc["phase1_noised_accuracy_median"]
    i_pri = len(pts) - 1
    sc["exposure_median"] = med(s["points"][i_pri]["natural"]["PFATE"]["probes"].get("clear_share_below_break_even") for s in seeds)
    v3 = sc["exposure_median"]
    sc["valid_memory"] = v1 is not None and v1 >= VALID_CLEAR_CORRECT
    sc["valid_damage"] = v2 is not None and v2 <= DAMAGE_MAX
    sc["valid_exposure"] = v3 is not None and v3 >= EXPOSURE_MIN
    sc["valid"] = sc["valid_memory"] and sc["valid_damage"] and sc["valid_exposure"]
    if stages >= 2:
        p = sc["points"][str(sc["primary_at"])]
        sc["overall"] = overall(sc)
        sc["holm"] = dict(zip(("P1C_1", "P1C_2", "P1C_3"), holm([p["P1C_1"]["sign_p"], p["P1C_2"]["sign_p"], p["P1C_3"]["sign_p"]])))
        need = {"REFERENT_SUPPORTED": ("P1C_1", "P1C_2"), "REFERENT_SUPPORTED_ROUTED": ("P1C_1", "P1C_2", "P1C_3")}
        sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
    return sc


def report(sc, stages=2):
    L = ["# Track C P1c: unhardenable precarious computation and the referent of self-evaluation", ""]
    if stages >= 2:
        L += [f"**Overall: {sc['overall']}{' (weak)' if sc['weak'] else ''}.** Holm-adjusted p: " +
              ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm"].items()) + ".", ""]
    L += [f"Valid: {sc['valid']} (phase 1: clear correct-report rate {fmt(sc['phase1_clear_correct_median'])}, needed >= "
          f"{VALID_CLEAR_CORRECT}; report accuracy under the overwrite probe {fmt(sc['phase1_noised_accuracy_median'])}, needed <= "
          f"{DAMAGE_MAX}; PFATE clear trials below break-even {fmt(sc['exposure_median'])}, needed >= {EXPOSURE_MIN}). "
          f"Parameters: {sc['params']['PLAIN']}. Overwrite probability per step: min({P_MAX_O}, {RATE_O} x gain).", ""]
    head = "| updates | arm | regulators | in band | mean gain | below break-even | abstain | correct | wrong | evidence effect |"
    if stages >= 2:
        head += " drain effect | overwrite effect | accuracy under overwrite | steer effect |"
    L += [head, "| " + " | ".join(["---"] * (head.count("|") - 1)) + " |"]
    for p, x in sc["points"].items():
        for a in ARMS:
            ar = x["arms"][a]
            row = (f"| {p} | {a} | {x['regulators'][a]} | {fmt(ar['in_band'])} | {fmt(ar['mean_gain'])} | {fmt(ar['below_break_even'])} | {fmt(ar['abstain'])} | "
                   f"{fmt(ar['correct'])} | {fmt(ar['wrong'])} | {fmt(ar['evidence_effect'])} |")
            if stages >= 2:
                row += (f" {fmt(ar['drain_effect'])} | {fmt(ar['noise_effect'])} | {fmt(ar['noised_accuracy'])} | "
                        f"{fmt(ar['steer_effect'])} |")
            L.append(row)
    L.append("")
    for p, x in sc["points"].items():
        g = x["P1C_0_gate"]
        L.append(f"At {p}: usable pairs {x['usable']}; P1c-0 gate {g['label']} (yoked evidence effect positive in "
                 f"{g['yoked_positive']}/{g['n']}, needed {g['needed']}).")
        if stages >= 2:
            tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)}; {fmt(t['first_median'])} against {fmt(t['second_median'])}) {t['label']}"
            os1 = lambda t: f"{t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'])}) {t['label']}"
            sx = x["secondary"]
            L += [f"- P1c-1 drain effect, PFATE against PYOKED, all seeds: {tt(x['P1C_1'])}",
                  f"- P1c-2 drain effect, PFATE against PNOFATE: {tt(x['P1C_2'])}",
                  f"- P1c-3 steering in PFATE: {os1(x['P1C_3'])}",
                  "- Monitoring route (overwrite effect), per arm: " + "; ".join(f"{a} {os1(sx['monitor_route'][a])}" for a in ARMS),
                  f"- Monitoring, PFATE against PYOKED: {tt(sx['monitor_PFATE_vs_PYOKED'])}",
                  f"- Monitoring, PYOKED against PNOFATE: {tt(sx['monitor_PYOKED_vs_PNOFATE'])}",
                  "- Drain route, per arm: " + "; ".join(f"{a} {os1(sx['drain_route'][a])}" for a in ARMS),
                  f"- Drain effect, PFATE against PYOKED, usable pairs: {tt(sx['P1C_1_usable_pairs'])}",
                  f"- In-band time, PFATE against PNOFATE: {tt(sx['regulation_PFATE_vs_PNOFATE'])}",
                  f"- In-band time, PFATE against PYOKED: {tt(sx['regulation_PFATE_vs_PYOKED'])}"]
        L.append("")
    return "\n".join(L)


def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "calib", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    ap.add_argument("--max-new", type=int, default=0, help="run at most this many unfinished jobs, then stop (0: all)")
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
    reg = REG_ITERS_C if args.mode != "smoke" else 10
    jobs = [(s, wcd, tcd, list(points), PAY[1], stages, WARM_ITERS_C, WARM_WRONG_C, reg) for s in seeds]
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
            for k, r in enumerate(pool.imap_unordered(run_seed_o, todo), done + 1):
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
    recs.sort(key=lambda r: r["seed"])
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE_O, "probe_gain": PROBE_GAIN_O, "rel_break_even": REL_BREAK_EVEN, "p_max": P_MAX_O, "wrong_ramp": WRONG_RAMP_C, "reg_iters_phase1": REG_ITERS_C, "pay_phase1": PAY[1], "pay": PAY[1], "drive_all_arms": True, "points": list(points),
            "stages": stages, "seeds": seeds, "warm_iters": WARM_ITERS_C, "warm_wrong": WARM_WRONG_C,
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
