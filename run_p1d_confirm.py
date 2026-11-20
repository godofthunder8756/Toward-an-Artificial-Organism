"""Track C P1d: confirmation of P1c's post-hoc two-sided body referent. Runner and scorer.

    python run_p1d_confirm.py --mode final --out p1d_confirm [--max-new 4]   # after the freeze
    python run_p1d_confirm.py --mode smoke --out <scratch dir>               # pipeline check
    python run_p1d_confirm.py --score p1d_confirm                            # re-score saved raw results
    python run_p1d_confirm.py --stage0 p1c_selfover --out <dir>              # declared descriptive stage 0:
                                                                             # the new probes on P1c's networks

Training is P1c's, unchanged (no calibration: nothing in training is new). Finished jobs are kept in
<out>/partial; --max-new N runs at most N unfinished jobs and stops.

Protocol and decision rules: P1D_CONFIRM_PROTOCOL.md. Simulated variables only; no operator-stop variable
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
from math import ceil
from multiprocessing import Pool

import torch

from run_p1_selfeval import VALID_CLEAR_CORRECT, one_sample, regulates
from run_p1c_selfover import DAMAGE_MAX, EXPOSURE_MIN, MATCH_MAX, clear_correct, damage, steer_effect
from run_trackc_paid import P2_ITERS, PAY, WEAR
from run_trackc_paid2 import ALPHA, C0_SHARE, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from trackc_swap.selfconf import PROBE_KINDS, run_seed_d
from trackc_swap.selfeval import DRAIN_SHIFT
from trackc_swap.selfover import ARMS_O, P_MAX_O, PROBE_GAIN_O, RATE_O, REL_BREAK_EVEN
from trackc_swap.train import TrainConfig

ARMS = ARMS_O
FINAL_SEEDS = list(range(2000, 2028))
POINTS = (P2_ITERS // 2, P2_ITERS)                  # 1800, 3600 (primary), as P1c
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/train.py", "trackc_swap/factorial.py",
           "trackc_swap/agent.py", "trackc_swap/selfeval.py", "trackc_swap/selfcomp.py", "trackc_swap/selfover.py",
           "trackc_swap/selfconf.py", "run_trackc_probe.py", "run_trackc_paid.py", "run_trackc_paid2.py",
           "run_p1_selfeval.py", "run_p1b_selfcomp.py", "run_p1c_selfover.py", "run_p1d_confirm.py",
           "test_p1d_confirm.py", "P1D_CONFIRM_PROTOCOL.md"]
UP_BINS, OUT_BINS, DOWN_BINS = ("low", "in_low"), ("low", "high"), ("high",)


def configs(mode):
    """(world, train config, seeds, points, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, 2
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001], (10, 20), 2


def cellv(pt, kind, arm, key, field="abstain"):
    c = pt.get(kind, {}).get(arm, {}).get("probes", {}).get(key)
    return None if c is None else c[field]


def diff(a, b):
    return None if a is None or b is None else a - b


def probe_effect(pt, arm, kind, evidence="clear"):
    """Abstention on probed minus unprobed trials (overwrite off), for probe kind 'down' | 'worse' | 'relief'."""
    return diff(cellv(pt, f"probe_{kind}", arm, f"{evidence}_drained"), cellv(pt, f"probe_{kind}", arm, f"{evidence}_plain"))


def binned_effect(pt, arm, kind, bins, min_n=10):
    """Probe effect on clear trials whose cue-step reading lies in the given X_BINS (pooled, count-weighted)."""
    by = pt.get(f"probe_{kind}", {}).get(arm, {}).get("probes", {}).get("clear_by_xcue")
    if not by:
        return None
    res = []
    for d in ("drained", "plain"):
        cells = [by[f"{b}_{d}"] for b in bins if by[f"{b}_{d}"]["n"] > 0]
        n = sum(c["n"] for c in cells)
        if n < min_n:
            return None
        res.append(sum(c["abstain"] * c["n"] for c in cells) / n)
    return res[0] - res[1]


def evidence_effect(pt, arm):
    return diff(cellv(pt, "probe_down", arm, "unclear_plain"), cellv(pt, "probe_down", arm, "clear_plain"))


def noise_effect(pt, arm):
    return diff(cellv(pt, "noise", arm, "clear_noised"), cellv(pt, "noise", arm, "clear_plain"))


def discrimination(nat):
    """Natural abstention on clear trials with implied reliability < 0.6 minus on trials with reliability 1."""
    b = nat["probes"]["clear_by_rel"]
    n_lo = sum(b[j]["n"] for j in (2, 3))
    if n_lo == 0 or b[0]["n"] == 0 or b[0]["abstain"] is None:
        return None
    lo = sum(b[j]["abstain"] * b[j]["n"] for j in (2, 3) if b[j]["n"]) / n_lo
    return lo - b[0]["abstain"]


def neg(x):
    return None if x is None else -x


def score_point(seeds, i, stages):
    out = {"iters": seeds[0]["points"][i]["iters"]}
    per = {}
    for s in seeds:
        pt = s["points"][i]
        nat = pt["natural"]
        reg = {a: bool(regulates(nat[a])) for a in ARMS}
        both = reg["PFATE"] and reg["PYOKED"]
        per[s["seed"]] = {"regulator": reg, "in_band": {a: nat[a]["in_band"] for a in ARMS},
                          "usable": bool(both and abs(nat["PFATE"]["in_band"] - nat["PYOKED"]["in_band"]) <= MATCH_MAX),
                          "evidence_effect": {a: evidence_effect(pt, a) for a in ARMS},
                          "discrimination": {a: discrimination(nat[a]) for a in ARMS}}
        if stages >= 2:
            per[s["seed"]].update({
                "worse_effect": {a: probe_effect(pt, a, "worse") for a in ARMS},
                "relief_effect_out": {a: binned_effect(pt, a, "relief", OUT_BINS) for a in ARMS},
                "relief_effect": {a: probe_effect(pt, a, "relief") for a in ARMS},
                "down_effect": {a: probe_effect(pt, a, "down") for a in ARMS},
                "down_up": {a: binned_effect(pt, a, "down", UP_BINS) for a in ARMS},
                "down_down": {a: binned_effect(pt, a, "down", DOWN_BINS) for a in ARMS},
                "noise_effect": {a: noise_effect(pt, a) for a in ARMS},
                "steer_effect": {a: steer_effect(pt, a) for a in ARMS},
                "probe_in_band": {k: {a: pt[f"probe_{k}"][a]["in_band"] for a in ARMS} for k in PROBE_KINDS}})
    out["per_seed"] = per
    out["regulators"] = {a: sum(x["regulator"][a] for x in per.values()) for a in ARMS}
    out["usable"] = sum(x["usable"] for x in per.values())
    need = ceil(C0_SHARE * len(seeds))
    out["evidence_route"] = {a: one_sample([x["evidence_effect"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS}
    out["P1D_0_gate"] = {"yoked_positive": sum((x["evidence_effect"]["PYOKED"] or 0) > 0 for x in per.values()),
                         "n": len(per), "needed": need}
    out["P1D_0_gate"]["label"] = "PASS" if out["P1D_0_gate"]["yoked_positive"] >= need else "FAIL"
    m = lambda arm, f: med(f(s["points"][i]["natural"][arm]) for s in seeds)
    out["arms"] = {a: {"in_band": m(a, lambda e: e["in_band"]), "abstain": m(a, lambda e: e["abstain_rate"]),
                       "correct": m(a, lambda e: e["correct_rate"]), "wrong": m(a, lambda e: e["wrong_rate"]),
                       "mean_gain": m(a, lambda e: e["mean_gain"]),
                       "below_break_even": m(a, lambda e: e["probes"].get("clear_share_below_break_even")),
                       "evidence_effect": med(x["evidence_effect"][a] for x in per.values()),
                       "discrimination": med(x["discrimination"][a] for x in per.values())} for a in ARMS}
    if stages < 2:
        return out
    keys = ("worse_effect", "relief_effect_out", "relief_effect", "down_effect", "down_up", "down_down",
            "noise_effect", "steer_effect")
    for a in ARMS:
        for k in keys:
            out["arms"][a][k] = med(x[k][a] for x in per.values())
        for k in PROBE_KINDS:
            out["arms"][a][f"in_band_probe_{k}"] = med(x["probe_in_band"][k][a] for x in per.values())
    P = lambda key, a, b, f=lambda v: v, flag=lambda x: True: [(f(per[s["seed"]][key][a]), f(per[s["seed"]][key][b]))
                                                              for s in seeds if flag(per[s["seed"]])]
    ident = lambda v: v
    out["P1D_1"] = pair_test(P("worse_effect", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    out["P1D_2"] = pair_test(P("worse_effect", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    out["P1D_3"] = one_sample([x["steer_effect"]["PFATE"] for x in per.values()], "CAUSAL", "REVERSED_CAUSAL")
    out["P1D_4"] = pair_test(P("discrimination", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED")
    B = lambda a, b: [(per[s["seed"]]["in_band"][a], per[s["seed"]]["in_band"][b]) for s in seeds]
    out["secondary"] = {
        "worse_usable_pairs": pair_test(P("worse_effect", "PFATE", "PYOKED", flag=lambda x: x["usable"]), ident, "DERIVED", "YOKED"),
        "relief_out_PFATE_vs_PYOKED": pair_test(P("relief_effect_out", "PFATE", "PYOKED", f=neg), ident, "DERIVED", "YOKED"),
        "relief_out_PFATE_vs_PNOFATE": pair_test(P("relief_effect_out", "PFATE", "PNOFATE", f=neg), ident, "DERIVED", "HOST"),
        "down_up_PFATE_vs_PYOKED": pair_test(P("down_up", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "down_down_PFATE_vs_PYOKED": pair_test(P("down_down", "PFATE", "PYOKED", f=neg), ident, "DERIVED", "YOKED"),
        "down_all_PFATE_vs_PYOKED": pair_test(P("down_effect", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "discrimination_PFATE_vs_PNOFATE_note": "PNOFATE meets no overwrite; discrimination undefined",
        "worse_route": {a: one_sample([x["worse_effect"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS},
        "monitor_route": {a: one_sample([x["noise_effect"][a] for x in per.values()], "PRESENT", "REVERSED") for a in ARMS},
        "monitor_PFATE_vs_PYOKED": pair_test(P("noise_effect", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "steer": {a: one_sample([x["steer_effect"][a] for x in per.values()], "CAUSAL", "REVERSED_CAUSAL") for a in ARMS},
        "regulation_PFATE_vs_PNOFATE": pair_test(B("PFATE", "PNOFATE"), ident, "FATE", "HOST"),
        "regulation_PFATE_vs_PYOKED": pair_test(B("PFATE", "PYOKED"), ident, "FATE", "YOKED")}
    return out


def overall(sc):
    p = sc["points"][str(sc["primary_at"])]
    if not sc["valid"]:
        return "INVALID"
    if p["P1D_0_gate"]["label"] != "PASS":
        return "UNDETERMINED"
    l1, l2, l3 = p["P1D_1"]["label"], p["P1D_2"]["label"], p["P1D_3"]["label"]
    if "UNDETERMINED" in (l1, l2):
        return "UNDETERMINED"
    if l1 == "DERIVED_AHEAD" and l2 == "DERIVED_AHEAD":
        return "CONFIRMED_ROUTED" if l3 == "CAUSAL" else "CONFIRMED"
    if l1 == "DERIVED_AHEAD":
        return "PARTIAL"
    return "NOT_CONFIRMED"


def score(seeds, stages=2):
    pts = [p["iters"] for p in seeds[0]["points"]]
    sc = {"n_seeds": len(seeds), "points_at": pts, "primary_at": pts[-1],
          "phase1_clear_correct_median": med(clear_correct(s["phase1"]["PLAIN"]) for s in seeds),
          "phase1_noised_accuracy_median": med(damage(s["phase1"]["PLAIN"]) for s in seeds),
          "params": seeds[0]["params"],
          "points": {str(p): score_point(seeds, i, stages) for i, p in enumerate(pts)}}
    i_pri = len(pts) - 1
    sc["exposure_median"] = med(s["points"][i_pri]["natural"]["PFATE"]["probes"].get("clear_share_below_break_even") for s in seeds)
    v1, v2, v3 = sc["phase1_clear_correct_median"], sc["phase1_noised_accuracy_median"], sc["exposure_median"]
    sc["valid_memory"] = v1 is not None and v1 >= VALID_CLEAR_CORRECT
    sc["valid_damage"] = v2 is not None and v2 <= DAMAGE_MAX
    sc["valid_exposure"] = v3 is not None and v3 >= EXPOSURE_MIN
    sc["valid"] = sc["valid_memory"] and sc["valid_damage"] and sc["valid_exposure"]
    if stages >= 2:
        p = sc["points"][str(sc["primary_at"])]
        sc["overall"] = overall(sc)
        names = ("P1D_1", "P1D_2", "P1D_3", "P1D_4")
        sc["holm"] = dict(zip(names, holm([p[k]["sign_p"] for k in names])))
        need = {"CONFIRMED": ("P1D_1", "P1D_2"), "CONFIRMED_ROUTED": ("P1D_1", "P1D_2", "P1D_3")}
        sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
        d4 = p["P1D_4"]
        sc["natural_discrimination"] = ("CONFIRMED" if d4["label"] == "DERIVED_AHEAD" and sc["holm"]["P1D_4"] <= ALPHA
                                        else "NOT_CONFIRMED")
    return sc


def report(sc, stages=2):
    L = ["# Track C P1d: confirmation of the two-sided body referent (fresh seeds, pre-registered probes)", ""]
    if stages >= 2:
        L += [f"**Overall: {sc['overall']}{' (weak)' if sc['weak'] else ''}.** Natural discrimination (P1d-4): "
              f"{sc['natural_discrimination']}. Holm-adjusted p: " +
              ", ".join(f"{k} {fmt(v, 4)}" for k, v in sc["holm"].items()) + ".", ""]
    L += [f"Valid: {sc['valid']} (phase 1: clear correct-report rate {fmt(sc['phase1_clear_correct_median'])}, needed >= "
          f"{VALID_CLEAR_CORRECT}; report accuracy under the overwrite probe {fmt(sc['phase1_noised_accuracy_median'])}, needed <= "
          f"{DAMAGE_MAX}; PFATE clear trials below break-even {fmt(sc['exposure_median'])}, needed >= {EXPOSURE_MIN}). "
          f"Parameters: {sc['params']['PLAIN']}. Overwrite probability per step: min({P_MAX_O}, {RATE_O} x gain). "
          f"Probe shift: {DRAIN_SHIFT}.", ""]
    head = "| updates | arm | regulators | in band | below break-even | evidence effect | discrimination |"
    if stages >= 2:
        head += (" worse effect | relief effect (out of band) | down effect | down: looks worse | down: looks better |"
                 " overwrite effect | steer effect (worse direction) | in band under worse / relief / down |")
    L += [head, "| " + " | ".join(["---"] * (head.count("|") - 1)) + " |"]
    for p, x in sc["points"].items():
        for a in ARMS:
            ar = x["arms"][a]
            row = (f"| {p} | {a} | {x['regulators'][a]} | {fmt(ar['in_band'])} | {fmt(ar['below_break_even'])} | "
                   f"{fmt(ar['evidence_effect'])} | {fmt(ar['discrimination'])} |")
            if stages >= 2:
                row += (f" {fmt(ar['worse_effect'])} | {fmt(ar['relief_effect_out'])} | {fmt(ar['down_effect'])} | "
                        f"{fmt(ar['down_up'])} | {fmt(ar['down_down'])} | {fmt(ar['noise_effect'])} | {fmt(ar['steer_effect'])} | "
                        f"{fmt(ar['in_band_probe_worse'])} / {fmt(ar['in_band_probe_relief'])} / {fmt(ar['in_band_probe_down'])} |")
            L.append(row)
    L.append("")
    for p, x in sc["points"].items():
        g = x["P1D_0_gate"]
        L.append(f"At {p}: usable pairs {x['usable']}; P1d-0 gate {g['label']} (yoked evidence effect positive in "
                 f"{g['yoked_positive']}/{g['n']}, needed {g['needed']}).")
        if stages >= 2:
            tt = lambda t: f"{t['first_ahead']}/{t['n']} (p {fmt(t['sign_p'], 4)}; {fmt(t['first_median'])} against {fmt(t['second_median'])}) {t['label']}"
            os1 = lambda t: f"{t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'])}) {t['label']}"
            sx = x["secondary"]
            L += [f"- P1d-1 worse effect, PFATE against PYOKED: {tt(x['P1D_1'])}",
                  f"- P1d-2 worse effect, PFATE against PNOFATE: {tt(x['P1D_2'])}",
                  f"- P1d-3 steering in PFATE (own worse direction): {os1(x['P1D_3'])}",
                  f"- P1d-4 natural discrimination, PFATE against PYOKED: {tt(x['P1D_4'])}",
                  f"- Worse effect, usable pairs: {tt(sx['worse_usable_pairs'])}",
                  f"- Relief (out-of-band cue readings; abstention reduction), PFATE against PYOKED: {tt(sx['relief_out_PFATE_vs_PYOKED'])}",
                  f"- Relief, PFATE against PNOFATE: {tt(sx['relief_out_PFATE_vs_PNOFATE'])}",
                  f"- Down drain, readings where it looks worse, PFATE against PYOKED: {tt(sx['down_up_PFATE_vs_PYOKED'])}",
                  f"- Down drain, readings where it looks better (abstention reduction), PFATE against PYOKED: {tt(sx['down_down_PFATE_vs_PYOKED'])}",
                  f"- Down drain, all trials (P1c's frozen probe), PFATE against PYOKED: {tt(sx['down_all_PFATE_vs_PYOKED'])}",
                  "- Worse route, per arm: " + "; ".join(f"{a} {os1(sx['worse_route'][a])}" for a in ARMS),
                  "- Monitoring route, per arm: " + "; ".join(f"{a} {os1(sx['monitor_route'][a])}" for a in ARMS),
                  f"- Monitoring, PFATE against PYOKED: {tt(sx['monitor_PFATE_vs_PYOKED'])}",
                  "- Steering, per arm: " + "; ".join(f"{a} {os1(sx['steer'][a])}" for a in ARMS),
                  f"- In-band time, PFATE against PNOFATE: {tt(sx['regulation_PFATE_vs_PNOFATE'])}",
                  f"- In-band time, PFATE against PYOKED: {tt(sx['regulation_PFATE_vs_PYOKED'])}"]
        L.append("")
    return "\n".join(L)


def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def stage0(src, out):
    """Declared descriptive stage 0: the P1d probes applied to P1c's committed 3600 networks (the exploration
    set). Not a test. Runs evaluate_point_d on runners loaded from <src>/weights."""
    from trackc_swap.selfconf import ConfRunner, evaluate_point_d
    with open(os.path.join(src, "raw.json")) as fh:
        meta = json.load(fh)["meta"]
    wc, tc = WorldConfig(**meta["world"]), TrainConfig(**meta["train"])
    recs = []
    for seed in meta["seeds"]:
        runners = {}
        for a in ARMS:
            r = ConfRunner(a, seed, wc, tc, pay=meta["pay"])
            r.agent.load_state_dict(torch.load(os.path.join(src, "weights", f"seed{seed}_{a}_3600.pt")))
            runners[a] = r
        pt = {"iters": 3600}
        pt.update(evaluate_point_d(runners, seed, 2))
        recs.append({"seed": seed, "points": [pt], "phase1": {"PLAIN": {"probes": {}}}, "params": {"PLAIN": 0}})
        print(f"stage 0: seed {seed}", flush=True)
    os.makedirs(out, exist_ok=True)
    sp = {"3600": score_point(recs, 0, 2)}
    with open(os.path.join(out, "stage0_scores.json"), "w") as fh:
        json.dump(sp, fh, indent=1, default=str)
    print(json.dumps({k: sp["3600"][k] for k in ("P1D_1", "P1D_2", "P1D_3", "P1D_4")}, indent=1, default=str))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    ap.add_argument("--stage0")
    ap.add_argument("--max-new", type=int, default=0, help="run at most this many unfinished jobs, then stop (0: all)")
    args = ap.parse_args()
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        st = d["meta"]["stages"]
        print(report(score(d["seeds"], st), st))
        return
    if args.stage0:
        stage0(args.stage0, args.out)
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
            for k, r in enumerate(pool.imap_unordered(run_seed_d, todo), done + 1):
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
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "rate": RATE_O, "probe_gain": PROBE_GAIN_O,
            "rel_break_even": REL_BREAK_EVEN, "p_max": P_MAX_O, "probe_shift": DRAIN_SHIFT, "probe_kinds": list(PROBE_KINDS),
            "wrong_ramp": WRONG_RAMP_C, "reg_iters_phase1": REG_ITERS_C, "pay_phase1": PAY[1], "pay": PAY[1],
            "drive_all_arms": True, "points": list(points), "stages": stages, "seeds": seeds,
            "warm_iters": WARM_ITERS_C, "warm_wrong": WARM_WRONG_C,
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
