"""P1h: is P1g's second-order residue explained by a non-linear read of the content evidence?

Protocol: P1H_EVIDENCE_PROTOCOL.md. Module: trackc_swap/evidence.py.

    python run_p1h_evidence.py --stage 1 --out p1h_evidence/stage1          # P1g's saved weights (3200-3227)
    python run_p1h_evidence.py --stage 2 --out p1h_evidence/stage2 [--max-new N]
        # fresh seeds 3300-3327 under P1g's frozen design; runs only if stage 1 is SECOND_ORDER_SURVIVES
        # and outside the leak range
    python run_p1h_evidence.py --score p1h_evidence/stage1
    python run_p1h_evidence.py --smoke --out /tmp/p1h_smoke
"""
import argparse
import json
import os
import platform
import sys
from dataclasses import asdict
from multiprocessing import Pool

import numpy as np
import torch

import run_p1g_graded as G
from run_p1_selfeval import one_sample
from run_trackc_paid import PAY, WEAR
from run_trackc_paid2 import ALPHA, holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.env import WorldConfig
from trackc_swap.evidence import DEC_VALID, collect_graded, evidence_summary
from trackc_swap.gradmon import KS_G
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C
from trackc_swap.selfmon import ARMS_M, P_MAX_M, RATE_M
from trackc_swap.train import TrainConfig

ARMS = ARMS_M
POINT = 3600
STAGE1_SEEDS = list(G.FINAL_SEEDS)                 # P1g's final seeds, saved weights
FINAL_SEEDS = list(range(3300, 3328))              # stage 2: fresh seeds, trained under P1g's frozen design
THIN_COVERAGE = 0.25
LEAK_SHARE = 0.005     # largest leak of the joint match in the synthetic first-order-only controls (0.4% of the
                       # unmatched conflict-same gap), rounded up: a residue below this share is within the leak range
NAMES = ("P1H_1", "P1H_2")
SOURCES = G.SOURCES + ["trackc_swap/evidence.py", "run_p1h_evidence.py", "P1H_EVIDENCE_PROTOCOL.md"]
VARIANTS = ("E", "E_sampled", "E_alt", "own_p", "own_sampled", "lda_p", "joint_p")


def analyse_seed(job):
    """job = (seed, weights_dir, wcd, tcd, base, point)."""
    seed, wdir, wcd, tcd, base, point = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    weights = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{point}.pt"), weights_only=False) for a in ARMS}
    cols = collect_graded(seed, weights, wc, tc, PAY[1], base)
    out = {"seed": seed, "arms": {}}
    for a in ARMS:
        out["arms"][a] = {t: evidence_summary(*cols[a][t], seed=seed) for t in ("early", "late")}
    return out


def measures(rec, arm):
    """Per seed and arm: the mean over EARLY and LATE runs that have a value."""
    runs = [rec["arms"][arm][t] for t in ("early", "late") if rec["arms"][arm][t].get("fitted")]
    mean = lambda vs: (float(np.mean([v for v in vs if v is not None]))
                       if any(v is not None for v in vs) else None)
    m = {}
    for v in VARIANTS:
        m[f"M2_{v}"] = mean([r[v]["M2"] for r in runs])
    m["coverage_E"] = mean([r["E"]["coverage"] for r in runs])
    m["balance_E"] = mean([r["E"].get("balance") for r in runs])
    m["coverage_joint"] = mean([r["joint_p"]["coverage"] for r in runs])
    for k in ("dec_acc_none", "dec_acc_same", "dec_acc_conflict", "ev_conflict", "ev_same", "pabs_conflict",
              "pabs_same", "pabs_none"):
        m[k] = mean([r[k] for r in runs])
    m["trace_auc"] = mean([r["trace"]["auc"] for r in runs])
    m["trace_pair_auc"] = mean([r["trace"]["pair_auc"] for r in runs])
    for t in ("early", "late"):
        r = rec["arms"][arm][t]
        m[f"M2_E_{t}"] = r["E"]["M2"] if r.get("fitted") else None
    return m


def relabel(test, p_adj, hi, lo):
    t = dict(test)
    t["holm_p"] = p_adj
    if t["label"] != "UNDETERMINED" and p_adj is not None:
        side = t.get("positive", t.get("first_ahead"))
        n = t["n"]
        if p_adj > ALPHA:
            t["label"] = "NOT_DETECTED" if "positive" in t else "NO_DIFFERENCE_DETECTED"
        else:
            t["label"] = hi if side > n - side else lo
    return t


def score(recs, reproduction=None):
    per = {r["seed"]: {a: measures(r, a) for a in ARMS} for r in recs}
    keys = list(next(iter(per.values()))["PFATE"].keys())
    arms = {a: {k: med(per[s][a][k] for s in per) for k in keys} for a in ARMS}
    P = lambda key, a, b: [(per[s][a][key], per[s][b][key]) for s in per]
    one = lambda key, a: one_sample([per[s][a][key] for s in per], "PRESENT", "REVERSED")
    t1 = one("M2_joint_p", "PFATE")
    t2 = pair_test(P("M2_joint_p", "PFATE", "PNOFATE"), lambda v: v, "DERIVED", "HOST")
    adj = holm([t1["sign_p"], t2["sign_p"]])
    t1 = relabel(t1, adj[0], "PRESENT", "REVERSED")
    t2 = relabel(t2, adj[1], "DERIVED_AHEAD", "HOST_AHEAD")
    dec_ok = (arms["PFATE"]["dec_acc_none"] or 0) >= DEC_VALID and (arms["PFATE"]["dec_acc_same"] or 0) >= DEC_VALID
    valid = dec_ok and (reproduction is None or reproduction["mismatches"] == 0)
    sc = {"n_seeds": len(per), "valid": valid, "decoder_valid": dec_ok, "reproduction": reproduction,
          "P1H_1": t1, "P1H_2": t2, "arms": arms, "per_seed": per,
          "thin": (arms["PFATE"]["coverage_joint"] or 0) < THIN_COVERAGE,
          "gap_PFATE": med((per[s]["PFATE"]["pabs_conflict"] or 0) - (per[s]["PFATE"]["pabs_same"] or 0) for s in per),
          "secondary": {
              "M2_E_PYOKED_vs_PNOFATE": pair_test(P("M2_E", "PYOKED", "PNOFATE"), lambda v: v, "DERIVED", "HOST"),
              "M2_E_PFATE_vs_PYOKED": pair_test(P("M2_E", "PFATE", "PYOKED"), lambda v: v, "DERIVED", "YOKED"),
              "routes": {k: {a: one(k, a) for a in ARMS}
                         for k in [f"M2_{v}" for v in VARIANTS] + ["M2_E_early", "M2_E_late"]},
              "trace_routes": {k: {a: one_sample([None if per[s][a][k] is None else per[s][a][k] - 0.5
                                                  for s in per], "ABOVE_CHANCE", "BELOW_CHANCE") for a in ARMS}
                               for k in ("trace_auc", "trace_pair_auc")}}}
    g, m = sc["gap_PFATE"], arms["PFATE"]["M2_joint_p"]
    sc["residue_share"] = (m / g) if (g and m is not None) else None
    sc["within_leak_range"] = sc["residue_share"] is not None and sc["residue_share"] < LEAK_SHARE
    sc["overall"] = overall(sc)
    return sc


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    l1, l2 = sc["P1H_1"]["label"], sc["P1H_2"]["label"]
    if l1 == "UNDETERMINED":
        return "UNDETERMINED"
    if l1 != "PRESENT":
        return "EXPLAINED_BY_EVIDENCE"
    return "SECOND_ORDER_SURVIVES" if l2 == "DERIVED_AHEAD" else "NOT_SPECIFIC"


def test_line(name, t):
    if "positive" in t:
        return (f"- {name}: {t['positive']}/{t['n']} > 0 (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)};"
                f" median {fmt(t['median'], 4)}) {t['label']}")
    return (f"- {name}: {t['first_ahead']}/{t['n']} (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)}; "
            f"{fmt(t['first_median'], 4)} against {fmt(t['second_median'], 4)}) {t['label']}")


def report(sc, title):
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}.** Valid: {sc['valid']} (evidence decoder held-out accuracy, PFATE: none "
         f"{fmt(sc['arms']['PFATE']['dec_acc_none'])}, same {fmt(sc['arms']['PFATE']['dec_acc_same'])}, needed >= "
         f"{DEC_VALID}; reproduction: {sc['reproduction']}). Thin (PFATE joint coverage < {THIN_COVERAGE}): "
         f"{sc['thin']}. Residue as a share of PFATE's unmatched conflict-same gap in p_abs "
         f"({fmt(sc['gap_PFATE'], 4)}): {fmt(sc['residue_share'], 4)}; within the leak range (< {LEAK_SHARE}): "
         f"{sc['within_leak_range']}. Seeds: {sc['n_seeds']}. Point: {POINT}.", ""]
    cols = ["M2_joint_p", "coverage_joint", "M2_E", "M2_E_early", "M2_E_late", "coverage_E", "balance_E",
            "M2_E_sampled", "M2_E_alt", "M2_own_p",
            "M2_own_sampled", "M2_lda_p", "ev_conflict", "ev_same", "pabs_conflict",
            "pabs_same", "dec_acc_conflict", "trace_auc", "trace_pair_auc"]
    L += ["| arm | " + " | ".join(cols) + " |", "| --- " * (len(cols) + 1) + "|"]
    for a in ARMS:
        L.append(f"| {a} | " + " | ".join(fmt(sc["arms"][a][c], 4) for c in cols) + " |")
    L += ["", test_line("P1H_1 residue at matched own margin and evidence: M2_joint_p of PFATE against 0", sc["P1H_1"]),
          test_line("P1H_2 specific to damage training: M2_joint_p, PFATE against PNOFATE", sc["P1H_2"])]
    for k, t in sc["secondary"].items():
        if k in ("routes", "trace_routes"):
            continue
        L.append(test_line(k, t))
    for grp in ("routes", "trace_routes"):
        for k, d in sc["secondary"][grp].items():
            L.append(f"- route {k}: " + "; ".join(
                f"{a} {t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'], 4)}) {t['label']}"
                for a, t in d.items()))
    return "\n".join(L) + "\n"


def reproduction_check(recs):
    """Stage 1: P1g's declared M2_nn_own (sampled abstention, own margin) must be reproduced exactly."""
    with open("p1g_graded/raw.json") as fh:
        raw = {s["seed"]: s for s in json.load(fh)["seeds"]}
    bad = n = 0
    for r in recs:
        pt = [p for p in raw[r["seed"]]["points"] if p["iters"] == POINT][0]
        for a in ARMS:
            for t in ("early", "late"):
                want = pt[f"graded_{t}"][a]["own"]["nn"]["M2"]
                run = r["arms"][a][t]
                got = run["own_sampled"]["M2"] if run.get("fitted") else None
                n += 1
                if not ((want is None and got is None) or
                        (want is not None and got is not None and abs(want - got) < 1e-12)):
                    bad += 1
    return {"runs": n, "mismatches": bad}


def run_analysis(out, seeds, wdir, wc, tc, base, point=POINT):
    os.makedirs(out, exist_ok=True)
    jobs = [(s, wdir, asdict(wc), asdict(tc), base, point) for s in seeds]
    with Pool(min(len(jobs), os.cpu_count() or 1)) as pool:
        recs = []
        for k, r in enumerate(pool.imap_unordered(analyse_seed, jobs), 1):
            recs.append(r)
            print(f"[analysis {k}/{len(jobs)}] seed {r['seed']}", flush=True)
    return sorted(recs, key=lambda r: r["seed"])


def write(out, recs, meta, reproduction, title):
    with open(os.path.join(out, "raw.json"), "w") as fh:
        json.dump({"meta": meta, "seeds": recs, "reproduction": reproduction}, fh)
    sc = score(recs, reproduction)
    with open(os.path.join(out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    rep = report(sc, title)
    with open(os.path.join(out, "REPORT.md"), "w") as fh:
        fh.write(rep)
    print(rep)
    return sc


def meta_for(stage, seeds, wc, tc):
    return {"stage": stage, "seeds": seeds, "point": POINT, "world": asdict(wc), "train": asdict(tc),
            "base": G.BASE_F, "ks": list(KS_G), "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, choices=[1, 2])
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--score")
    ap.add_argument("--max-new", type=int, default=0)
    args = ap.parse_args()
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        print(report(score(d["seeds"], d["reproduction"]), f"P1h stage {d['meta']['stage']}"))
        return
    if args.smoke:
        wc, tc = WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=32, eval_episodes=1)
        jobs = [(s, asdict(wc), asdict(tc), [10, 20], PAY[1], 10, WARM_WRONG_C, 10, RATE_M, P_MAX_M, G.BASE_F, KS_G)
                for s in (9000, 9001)]
        G.run_jobs(args.out, jobs, 0)
        recs = run_analysis(args.out, [9000, 9001], os.path.join(args.out, "weights"), wc, tc, G.BASE_F, point=20)
        sc = score(recs)
        print(report(sc, "P1h smoke"))
        return
    if os.path.exists(os.path.join(args.out, "raw.json")):
        sys.exit("refusing to overwrite raw.json")
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    if args.stage == 1:
        recs = run_analysis(args.out, STAGE1_SEEDS, "p1g_graded/weights", wc, tc, G.BASE_F)
        rp = reproduction_check(recs)
        write(args.out, recs, meta_for(1, STAGE1_SEEDS, wc, tc), rp,
              "P1h stage 1: residue at matched evidence, P1g's saved weights")
        return
    # stage 2
    try:
        with open("p1h_evidence/stage1/scores.json") as fh:
            s1 = json.load(fh)["scores"]
    except FileNotFoundError:
        sys.exit("stage 2 needs stage 1's scores")
    if s1["overall"] != "SECOND_ORDER_SURVIVES" or s1["within_leak_range"]:
        sys.exit("stage 2 runs only if stage 1 is SECOND_ORDER_SURVIVES and outside the leak range "
                 f"(stage 1: {s1['overall']}, within leak range {s1['within_leak_range']})")
    train_dir = os.path.join(args.out, "p1g_design")
    jobs = [(s, asdict(wc), asdict(tc), list(G.POINTS), PAY[1], WARM_ITERS_C, WARM_WRONG_C, REG_ITERS_C, RATE_M,
             P_MAX_M, G.BASE_F, KS_G) for s in FINAL_SEEDS]
    trecs, done = G.run_jobs(train_dir, jobs, args.max_new)
    if len(trecs) < len(jobs):
        print(f"stopped after this batch: {len(trecs)} of {len(jobs)} jobs finished", flush=True)
        return
    trecs.sort(key=lambda r: r["seed"])
    gsc = G.score(trecs)
    with open(os.path.join(train_dir, "scores.json"), "w") as fh:
        json.dump({"scores": gsc}, fh, indent=1, default=str)
    with open(os.path.join(train_dir, "REPORT.md"), "w") as fh:
        fh.write(G.report(gsc).replace("# Track C P1g", "# P1h stage 2: replication of P1g's design (seeds 3300-3327)", 1))
    with open(os.path.join(train_dir, "raw.json"), "w") as fh:
        json.dump({"meta": {"seeds": FINAL_SEEDS}, "seeds": trecs}, fh)
    recs = run_analysis(args.out, FINAL_SEEDS, os.path.join(train_dir, "weights"), wc, tc, G.BASE_F)
    write(args.out, recs, meta_for(2, FINAL_SEEDS, wc, tc), None,
          "P1h stage 2: residue at matched evidence, fresh seeds (confirmatory)")


if __name__ == "__main__":
    main()
