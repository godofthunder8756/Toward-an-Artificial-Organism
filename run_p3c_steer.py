"""Track C P3c: confirmation and cause of the differentiated body readout (Layer 3 -> Layer 4). Runner and scorer.

    python run_p3c_steer.py --mode final --out p3c_steer [--max-new 4]  # after the freeze: new seeds, P3b training
    python run_p3c_steer.py --mode smoke --out <scratch dir>            # pipeline check
    python run_p3c_steer.py --stage0 p3b_diff --out <dir>               # declared stage 0: steering on P3b's nets
    python run_p3c_steer.py --calib p3b_diff --out <dir>                # steering-scale calibration (blind summary)
    python run_p3c_steer.py --score p3c_steer                           # re-score saved raw results
    python run_p3c_steer.py --score-stage0 <dir>                        # re-score a stage-0 run

Finished jobs are kept in <out>/partial; --max-new N runs at most N unfinished jobs and stops.

Protocol and decision rules: P3C_STEER_PROTOCOL.md. Simulated variables only; no operator-stop variable exists
in the world.
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

import run_p3b_diff as R3B
from run_p1_selfeval import one_sample
from run_p3_global import diff
from run_trackc_paid import PAY, WEAR
from run_trackc_paid2 import ALPHA, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.differentiate import REG_ITERS_D
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes
from trackc_swap.selfcomp import WARM_ITERS_C, WARM_WRONG_C
from trackc_swap.steerdiff import EVAL_TAG_S, STEER_EPISODES, STEER_SCALE, run_seed_s, steer_copies
from trackc_swap.train import TrainConfig

ARMS = R3B.ARMS
TYPES = R3B.TYPES
FINAL_SEEDS = list(range(2600, 2628))
CALIB_NETS = [2400, 2402, 2403, 2404, 2405]   # P3b final nets (usable; 2401 excluded by P3b's rule), point 3600
CALIB_SCALES = (1.0, 2.0, 4.0)
POINTS = R3B.POINTS
NAMES = ("P3C_B1", "P3C_B2", "P3C_SA", "P3C_SC")
SOURCES = R3B.SOURCES + ["trackc_swap/steerdiff.py", "run_p3c_steer.py", "test_p3c_steer.py", "P3C_STEER_PROTOCOL.md"]


def configs(mode):
    """(world, train config, seeds, points, stages)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, POINTS, 2
    return WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001], (10, 20), 2


# ---------------------------------------------------------------- measures
def neg(x):
    return None if x is None else -x


def _eff(st, key, t):
    e = st.get(key)
    return None if not e else e[t]["effect"]


def steer_measures(sp):
    """Per arm: directional effects (effect(+d) - effect(-d)), signed so that the expected direction is positive."""
    if not sp or not sp.get("steer"):
        return {k: None for k in ("S_A", "S_C", "X_AC", "X_CA", "V_C", "V_CA", "R_A", "R_C", "P_A", "P_C",
                                  "cos_uA_uC", "rel_uA", "rel_uC")}
    st = sp["steer"]
    dv = lambda name, t: diff(_eff(st, "+" + name, t), _eff(st, "-" + name, t))
    sym = lambda name, t: (None if _eff(st, "+" + name, t) is None or _eff(st, "-" + name, t) is None
                           else 0.5 * (_eff(st, "+" + name, t) + _eff(st, "-" + name, t)))
    return {"S_A": dv("u_A", "A"),             # A's look_low direction moves A (more abstention)
            "S_C": neg(dv("u_C", "C")),        # C's look_low direction moves C (less abstention: the release)
            "X_AC": neg(dv("u_A", "C")),       # A's direction read by C as release
            "X_CA": dv("u_C", "A"),            # C's direction read by A as danger
            "V_C": dv("v_C", "C"),             # C's look_high direction moves C (more abstention)
            "V_CA": neg(dv("v_C", "A")),       # ... read by A as safety (less abstention)
            "R_A": dv("rand_u_A", "A"), "R_C": dv("rand_u_C", "C"),          # controls: random directions
            "P_A": sym("rand_u_A", "A"), "P_C": sym("rand_u_C", "C"),        # symmetric perturbation effect
            "cos_uA_uC": sp["cos"]["u_A,u_C"], "rel_uA": sp["split_half_cos"]["u_A"],
            "rel_uC": sp["split_half_cos"]["u_C"]}


MEAS = ("S_A", "S_C", "X_AC", "X_CA", "V_C", "V_CA", "R_A", "R_C", "P_A", "P_C", "cos_uA_uC", "rel_uA", "rel_uC")


def steer_point(seeds, i):
    """Steering tests at point i over the given seeds."""
    per = {s["seed"]: {a: steer_measures(s["points"][i].get("steer", {}).get(a)) for a in ARMS} for s in seeds}
    one = lambda key, arm, hi="CAUSAL", lo="REVERSED_CAUSAL": one_sample([per[s][arm][key] for s in per], hi, lo)
    P = lambda key, a, b: [(per[s][a][key], per[s][b][key]) for s in per]
    ident = lambda v: v
    out = {"per_seed": per,
           "arms": {a: {k: med(per[s][a][k] for s in per) for k in MEAS} for a in ARMS},
           "SA": one("S_A", "PFATE"), "SC": one("S_C", "PFATE")}
    out["secondary"] = {
        "X_AC_PFATE": one("X_AC", "PFATE"), "X_CA_PFATE": one("X_CA", "PFATE"),
        "V_C_PFATE": one("V_C", "PFATE"), "V_CA_PFATE": one("V_CA", "PFATE"),
        "R_A_PFATE": one("R_A", "PFATE", "PRESENT", "REVERSED"), "R_C_PFATE": one("R_C", "PFATE", "PRESENT", "REVERSED"),
        "S_A_PFATE_vs_PYOKED": pair_test(P("S_A", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "S_C_PFATE_vs_PYOKED": pair_test(P("S_C", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "S_A_vs_random_PFATE": pair_test([(per[s]["PFATE"]["S_A"], per[s]["PFATE"]["R_A"]) for s in per], ident,
                                         "DIRECTION", "RANDOM"),
        "S_C_vs_random_PFATE": pair_test([(per[s]["PFATE"]["S_C"], neg(per[s]["PFATE"]["R_C"])) for s in per], ident,
                                         "DIRECTION", "RANDOM"),
        "P_A_PFATE_vs_PYOKED": pair_test(P("P_A", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "P_C_PFATE_vs_PYOKED": pair_test(P("P_C", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "cos_uA_uC_PFATE_vs_PYOKED": pair_test(P("cos_uA_uC", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
        "routes": {k: {a: one(k, a) for a in ARMS} for k in ("S_A", "S_C", "X_AC", "X_CA", "V_C")}}
    return out


def structure(sp):
    """Pre-registered reading of where the content lies, when both own-direction tests are CAUSAL."""
    if sp["SA"]["label"] != "CAUSAL" or sp["SC"]["label"] != "CAUSAL":
        return "NOT_APPLICABLE"
    xs = [sp["secondary"]["X_AC_PFATE"]["label"], sp["secondary"]["X_CA_PFATE"]["label"]]
    if all(x == "CAUSAL" for x in xs):
        return "ONE_DIRECTION_TWO_READOUTS"
    if not any(x in ("CAUSAL", "REVERSED_CAUSAL") for x in xs):
        return "SEPARATE_DIRECTIONS"
    return "PARTLY_SHARED"


def c_release_test(seeds, i):
    """P3C-B2: C_release = -C_low (P3b's look_low cell on C), PFATE against PYOKED."""
    pairs = []
    for s in seeds:
        pt = s["points"][i]
        a, b = R3B.look_effect(pt, "PFATE", "C", "low"), R3B.look_effect(pt, "PYOKED", "C", "low")
        pairs.append((neg(a), neg(b)))
    return pair_test(pairs, lambda v: v, "DERIVED", "YOKED")


def overall(sc):
    p = sc["points"][str(sc["primary_at"])]
    if not sc["valid"]:
        return "INVALID"
    if (sc["n_usable"] < 14 or p["gate"]["label"] != "PASS" or p["P3C_B1"]["label"] != "DERIVED_AHEAD"
            or p["P3C_B2"]["label"] == "UNDETERMINED"):
        return "UNDETERMINED"
    if p["P3C_B2"]["label"] != "DERIVED_AHEAD":
        return "NOT_CONFIRMED"
    if p["P3C_SA"]["label"] == "CAUSAL" and p["P3C_SC"]["label"] == "CAUSAL":
        return "CONFIRMED_CAUSAL"
    return "CONFIRMED_BEHAVIOURAL"


def score(seeds, stages=2):
    sc3 = R3B.score(seeds, stages)
    use = [s for s in seeds if R3B.phase1_usable(s)]
    sc = {k: sc3[k] for k in ("n_seeds", "n_usable", "excluded_seeds", "points_at", "primary_at", "params", "phase1",
                              "exposure_median", "valid", "valid_memory", "valid_damage", "valid_exposure")}
    sc["p3b_overall"], sc["p3b_partial_reading"] = sc3.get("overall"), sc3.get("partial_reading")
    sc["points"] = {}
    if not use:
        sc.update({"overall": "INVALID", "holm": {k: None for k in NAMES}, "weak": False, "structure": "NOT_APPLICABLE"})
        return sc
    for i, p in enumerate(sc["points_at"]):
        P3 = sc3["points"][str(p)]
        sp = steer_point(use, i)
        sc["points"][str(p)] = {
            "gate": P3["P3B_0_gate"], "P3C_B1": P3["P3B_0_referent_A"], "P3C_B2": c_release_test(use, i),
            "P3C_SA": sp["SA"], "P3C_SC": sp["SC"], "structure": structure(sp), "steer": sp,
            "p3b": {k: P3[k] for k in ("P3B_0_referent_C", "P3B_1", "P3B_2", "P3B_A", "P3B_C", "selectivity_PFATE")}
                   | {k: P3["secondary"][k] for k in ("G_cross_side_PFATE_vs_PYOKED", "A_high_PFATE_vs_PYOKED",
                                                       "A_discrimination_PFATE_vs_PYOKED", "C_discrimination_PFATE_vs_PYOKED",
                                                       "regulation_PFATE_vs_PYOKED", "regulation_PFATE_vs_PNOFATE")},
            "arms": P3["arms"]}
    p = sc["points"][str(sc["primary_at"])]
    sc["overall"] = overall(sc)
    sc["structure"] = p["structure"]
    sc["holm"] = dict(zip(NAMES, holm([p[k]["sign_p"] for k in NAMES])))
    need = {"CONFIRMED_CAUSAL": NAMES, "CONFIRMED_BEHAVIOURAL": ("P3C_B1", "P3C_B2")}
    sc["weak"] = any(sc["holm"][k] is None or sc["holm"][k] > ALPHA for k in need.get(sc["overall"], ()))
    return sc


def score_stage0(seeds):
    """Stage 0 (declared; not the confirmation): steering tests on P3b's usable nets at 3600."""
    use = [s for s in seeds if R3B.phase1_usable(s)]
    sp = steer_point(use, 0)
    return {"n_usable": len(use), "excluded_seeds": [s["seed"] for s in seeds if not R3B.phase1_usable(s)],
            "SA": sp["SA"], "SC": sp["SC"], "structure": structure(sp), "steer": sp}


# ---------------------------------------------------------------- report
_pt = R3B._pt
SCOLS = ("S_A", "S_C", "X_AC", "X_CA", "V_C", "R_A", "R_C", "P_A", "P_C", "cos_uA_uC", "rel_uA", "rel_uC")


def steer_lines(sp):
    L = ["| arm | " + " | ".join(SCOLS) + " |", "| --- | " + " | ".join("---" for _ in SCOLS) + " |"]
    for a in ARMS:
        L.append(f"| {a} | " + " | ".join(fmt(sp["arms"][a][k]) for k in SCOLS) + " |")
    L.append("")
    L.append(f"- SA, A's look_low direction moves A (PFATE): {_pt(sp['SA'])}")
    L.append(f"- SC, C's look_low direction releases C (PFATE): {_pt(sp['SC'])}")
    for k, r in sp["secondary"].items():
        if k == "routes":
            for m, rr in r.items():
                L.append(f"- route {m}: " + "; ".join(f"{a} {_pt(x)}" for a, x in rr.items()))
        else:
            L.append(f"- {k}: {_pt(r)}")
    return L


def report(sc, stages=2):
    h = sc["holm"]
    L = ["# Track C P3c: confirmation and cause of the differentiated body readout (Layer 3 -> Layer 4)", "",
         f"**Overall: {sc['overall']}**{' (weak)' if sc['weak'] else ''}. Structure reading: {sc['structure']}. "
         "Holm-adjusted p: " + ", ".join(f"{k} {fmt(h[k], 4)}" for k in NAMES) + ".", "",
         f"P3b's rules on these seeds: {sc['p3b_overall']} (partial reading {sc['p3b_partial_reading']}).", ""]
    v, em = sc["phase1"], sc["exposure_median"]
    L += [f"Valid: {sc['valid']} (phase 1 clear correct A / C {fmt(v['clear_correct_A'])} / {fmt(v['clear_correct_C'])}; "
          f"overwrite-probe accuracy A {fmt(v['damage_A'])}; PFATE clear trials below break-even A / C {fmt(em['A'])} / "
          f"{fmt(em['C'])}). Parameters: {sc['params']['PLAIN']}.", "",
          f"Usable seeds: {sc['n_usable']} of {sc['n_seeds']}; excluded: {sc['excluded_seeds'] or 'none'}. "
          "Every test below is on the usable seeds.", ""]
    if not sc["points"]:
        return "\n".join(L + ["No usable seed: nothing is tested."])
    cols = ["in_band", "A_low", "A_high", "C_low", "C_high", "D", "S", "G", "discrimination_A", "discrimination_C"]
    L += ["| updates | arm | " + " | ".join(cols) + " |", "| --- | --- | " + " | ".join("---" for _ in cols) + " |"]
    for p in sc["points_at"]:
        for a in ARMS:
            L.append(f"| {p} | {a} | " + " | ".join(fmt(sc["points"][str(p)]["arms"][a].get(c)) for c in cols) + " |")
    L.append("")
    for p in sc["points_at"]:
        P = sc["points"][str(p)]
        g = P["gate"]
        L += [f"## At {p}", "",
              f"Gate {g['label']} (yoked evidence positive A {g['yoked_A_evidence_positive']}/{g['n']}, C "
              f"{g['yoked_C_evidence_positive']}/{g['n']}, needed {g['needed']}).",
              f"- P3C-B1 memory referent A_low, PFATE against PYOKED: {_pt(P['P3C_B1'])}",
              f"- P3C-B2 C release (-C_low), PFATE against PYOKED: {_pt(P['P3C_B2'])}",
              f"- P3C-SA steering along u_A, directional effect on A, PFATE: {_pt(P['P3C_SA'])}",
              f"- P3C-SC steering along u_C, directional release on C, PFATE: {_pt(P['P3C_SC'])}",
              f"- Structure reading: {P['structure']}", ""]
        L += steer_lines(P["steer"])
        L.append("")
        L.append("P3b measures on these seeds:")
        for k, r in P["p3b"].items():
            L.append(f"- {k}: {fmt(r) if not isinstance(r, dict) else _pt(r)}")
        L.append("")
    return "\n".join(L)


def report_stage0(s0):
    L = ["# P3c stage 0 (declared; not the confirmation): steering on P3b's nets at 3600", "",
         f"Usable P3b nets: {s0['n_usable']}; excluded: {s0['excluded_seeds'] or 'none'}. Structure reading: "
         f"{s0['structure']}.", ""]
    return "\n".join(L + steer_lines(s0["steer"]))


def calib_summary(recs):
    """Steering-scale calibration (blind): direction norms and split-half reliability, steps per direction, the
    RANDOM-direction effects (both signs) and their symmetric part, unsteered abstention, and accuracy on steered
    trials over all runs. No directional effect along u_A, u_C or v_C, no cross effect and no cosine between
    directions is computed or printed."""
    L = ["# P3c steering calibration summary (blind to directional, cross and geometry measures)", ""]
    for scale in sorted({r["scale"] for r in recs}):
        L.append(f"## scale {scale}")
        agg = {a: {k: [] for k in ("P_A", "P_C", "corr_A", "corr_C")} for a in ARMS}
        for r in sorted((r for r in recs if r["scale"] == scale), key=lambda r: r["seed"]):
            row = [f"seed {r['seed']}"]
            for a in ARMS:
                sp = r["steer"][a]
                st = sp["steer"]
                e = lambda key, t: _eff(st, key, t)
                pa = [e("+rand_u_A", "A"), e("-rand_u_A", "A")]
                pc = [e("+rand_u_C", "C"), e("-rand_u_C", "C")]
                corr = {t: min((x[t]["correct_on"] for x in st.values() if x[t]["correct_on"] is not None), default=None)
                        for t in TYPES}
                off = {t: med(x[t]["abstain_off"] for x in st.values()) for t in TYPES}
                if None not in pa:
                    agg[a]["P_A"].append(sum(pa) / 2)
                if None not in pc:
                    agg[a]["P_C"].append(sum(pc) / 2)
                agg[a]["corr_A"].append(corr["A"])
                agg[a]["corr_C"].append(corr["C"])
                row.append(f"{a}: norm uA/uC/vC {fmt(sp['norm']['u_A'])}/{fmt(sp['norm']['u_C'])}/{fmt(sp['norm']['v_C'])} "
                           f"rel {fmt(sp['split_half_cos']['u_A'])}/{fmt(sp['split_half_cos']['u_C'])}/"
                           f"{fmt(sp['split_half_cos']['v_C'])} steps {min(min(v) for v in sp['n_steps_min'].values())} "
                           f"rand A +/- {fmt(pa[0])}/{fmt(pa[1])} C +/- {fmt(pc[0])}/{fmt(pc[1])} "
                           f"off A/C {fmt(off['A'])}/{fmt(off['C'])} min correct A/C {fmt(corr['A'])}/{fmt(corr['C'])}")
            L.append(" | ".join(row))
        for a in ARMS:
            L.append(f"median {a}: symmetric random effect A {fmt(med(agg[a]['P_A']))} C {fmt(med(agg[a]['P_C']))}; "
                     f"min correct on steered A {fmt(med(agg[a]['corr_A']))} C {fmt(med(agg[a]['corr_C']))}")
        L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- jobs on saved nets
def _net_job(job):
    """job = (weights dir, seed, point, scale): steering on saved nets of one seed (stage 0 or calibration)."""
    wdir, seed, p, scale = job
    torch.set_num_threads(1)
    t0 = time.time()
    states = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{p}.pt"), weights_only=False) for a in ARMS}
    out = steer_copies(states, seed, WorldConfig(wear=WEAR), TrainConfig(), PAY[1], scale)
    return {"seed": seed, "point": p, "scale": scale, "steer": out, "seconds": round(time.time() - t0, 1)}


def run_nets(src, out, seeds, points, scales, max_new):
    """Steering on saved nets (stage 0 or calibration); finished jobs kept in <out>/partial."""
    pdir = os.path.join(out, "partial")
    os.makedirs(pdir, exist_ok=True)
    wdir = os.path.join(src, "weights")
    jobs = [(wdir, s, p, sc) for s in seeds for p in points for sc in scales]
    lab = lambda seed, p, sc: f"seed{seed}_{p}_x{sc}"
    path = lambda name: os.path.join(pdir, name + ".json")
    recs, todo = [], []
    for j in jobs:
        f = path(lab(*j[1:]))
        if os.path.exists(f):
            recs.append(json.load(open(f)))
        else:
            todo.append(j)
    done = len(jobs) - len(todo)
    if done:
        print(f"resuming: {done} of {len(jobs)} jobs already finished", flush=True)
    if max_new:
        todo = todo[:max_new]
    t0 = time.time()
    if todo:
        with Pool(min(len(todo), os.cpu_count() or 1)) as pool:
            for k, r in enumerate(pool.imap_unordered(_net_job, todo), done + 1):
                r = json.loads(json.dumps(r, default=float))
                name = lab(r["seed"], r["point"], r["scale"])
                with open(path(name) + ".tmp", "w") as fh:
                    json.dump(r, fh)
                os.replace(path(name) + ".tmp", path(name))
                recs.append(r)
                print(f"[job {k}/{len(jobs)}] {name} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    return recs, len(jobs), done


def stage0_records(src, recs):
    """P3b's records (for the usability rule) with the stage-0 steering attached as point 0."""
    raw = json.load(open(os.path.join(src, "raw.json")))["seeds"]
    by = {r["seed"]: r for r in recs}
    out = []
    for s in raw:
        if s["seed"] in by:
            out.append({"seed": s["seed"], "phase1": s["phase1"], "points": [{"steer": by[s["seed"]]["steer"]}]})
    return out


def strip(r):
    return {k: v for k, v in r.items() if k != "weights"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    ap.add_argument("--score-stage0")
    ap.add_argument("--stage0")
    ap.add_argument("--calib")
    ap.add_argument("--max-new", type=int, default=0, help="run at most this many unfinished jobs, then stop (0: all)")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(report(score(d["seeds"])))
        return
    if args.score_stage0:
        d = json.load(open(os.path.join(args.score_stage0, "stage0_raw.json")))
        print(report_stage0(score_stage0(stage0_records(d["meta"]["source"], d["records"]))))
        return
    if args.calib:
        recs, n, _ = run_nets(args.calib, args.out, CALIB_NETS, [R3B.POINTS[-1]], CALIB_SCALES, args.max_new)
        if len(recs) == n:
            print(calib_summary(recs))
        return
    if args.stage0:
        raw = json.load(open(os.path.join(args.stage0, "raw.json")))
        seeds = [s["seed"] for s in raw["seeds"]]
        recs, n, done = run_nets(args.stage0, args.out, seeds, [R3B.POINTS[-1]], [STEER_SCALE], args.max_new)
        if len(recs) < n:
            print(f"stopped: {len(recs)} of {n} jobs finished", flush=True)
            return
        recs.sort(key=lambda r: r["seed"])
        meta = {"source": args.stage0, "point": R3B.POINTS[-1], "scale": STEER_SCALE, "steer_episodes": STEER_EPISODES,
                "eval_tag": EVAL_TAG_S, "python": platform.python_version(), "torch": torch.__version__,
                "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
        with open(os.path.join(args.out, "stage0_raw.json"), "w") as fh:
            json.dump({"meta": meta, "records": recs}, fh)
        s0 = score_stage0(stage0_records(args.stage0, recs))
        with open(os.path.join(args.out, "stage0_scores.json"), "w") as fh:
            json.dump({"meta": meta, "scores": s0}, fh, indent=1, default=str)
        with open(os.path.join(args.out, "STAGE0_REPORT.md"), "w") as fh:
            fh.write(report_stage0(s0))
        print(report_stage0(s0))
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
    reg = REG_ITERS_D if args.mode != "smoke" else 10
    warm = WARM_ITERS_C if args.mode != "smoke" else 5
    jobs = [(s, wcd, tcd, list(points), PAY[1], stages, warm, WARM_WRONG_C, reg, STEER_SCALE) for s in seeds]
    ppath = lambda seed: os.path.join(pdir, f"seed{seed}.json")
    recs, todo = [], []
    for job in jobs:
        if os.path.exists(ppath(job[0])):
            recs.append(json.load(open(ppath(job[0]))))
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
            for k, r in enumerate(pool.imap_unordered(run_seed_s, todo), done + 1):
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
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "p3b_training": "trackc_swap.differentiate.run_seed_x, unchanged",
            "steer_scale": STEER_SCALE, "steer_episodes": STEER_EPISODES, "eval_tag": EVAL_TAG_S,
            "reg_iters_phase1": reg, "warm_iters": warm, "warm_wrong": WARM_WRONG_C, "pay": PAY[1],
            "points": list(points), "stages": stages, "seeds": seeds,
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
