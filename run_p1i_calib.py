"""P1i: confirmation of the calibrated integrity discount on fresh seeds.

Protocol: P1I_CALIB_PROTOCOL.md. Training is P1g's frozen design (run_p1g_graded, BASE_F 0.012) on fresh seeds;
the analysis (trackc_swap/calibdisc.py) is frozen in the protocol commit before it is run on any of them.

    python run_p1i_calib.py --train --max-new 4                  # trains seeds 3400-3427 into p1i_calib/p1g_design
    python run_p1i_calib.py --discovery                          # the same analysis on P1g's seeds (discovery set)
    python run_p1i_calib.py --analyse                            # P1i analysis (after the protocol freeze)
    python run_p1i_calib.py --score p1i_calib/confirm
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
from run_p1h_evidence import relabel
from run_trackc_paid import PAY, WEAR
from run_trackc_paid2 import holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.calibdisc import calib_summary
from trackc_swap.evidence import DEC_VALID, collect_graded
from trackc_swap.env import WorldConfig
from trackc_swap.gradmon import KS_G
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C
from trackc_swap.selfmon import ARMS_M, P_MAX_M, RATE_M
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(3400, 3428))
OUT = "p1i_calib"
TRAIN_DIR = os.path.join(OUT, "p1g_design")
ARMS = ARMS_M
POINT = 3600
SOURCES = G.SOURCES + ["trackc_swap/evidence.py", "trackc_swap/calibdisc.py", "run_p1h_evidence.py",
                       "run_p1i_calib.py", "P1I_CALIB_PROTOCOL.md"]
SCALARS = ("M2_E", "rel_gap", "own_gap", "type2_resid", "type2_raw", "type2_ev_raw", "type2_resid_pabs",
           "trace_rho", "coverage", "dec_acc_none", "dec_acc_same", "dec_acc_conflict", "agent_acc_conflict")


def train(max_new):
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    jobs = [(s, asdict(wc), asdict(tc), list(G.POINTS), PAY[1], WARM_ITERS_C, WARM_WRONG_C, REG_ITERS_C, RATE_M,
             P_MAX_M, G.BASE_F, KS_G) for s in FINAL_SEEDS]
    recs, _ = G.run_jobs(TRAIN_DIR, jobs, max_new)
    if len(recs) < len(jobs):
        print(f"stopped after this batch: {len(recs)} of {len(jobs)} jobs finished", flush=True)
        return
    recs.sort(key=lambda r: r["seed"])
    path = os.path.join(TRAIN_DIR, "raw.json")
    if not os.path.exists(path):
        with open(path, "w") as fh:
            json.dump({"meta": {"seeds": FINAL_SEEDS, "base": G.BASE_F}, "seeds": recs}, fh)
    sc = G.score(recs)
    with open(os.path.join(TRAIN_DIR, "scores.json"), "w") as fh:
        json.dump({"scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(TRAIN_DIR, "REPORT.md"), "w") as fh:
        fh.write(G.report(sc).replace("# Track C P1g", "# P1i: replication of P1g's design (seeds 3400-3427)", 1))
    print("training finished; P1g replication report written", flush=True)


def analyse_seed(job):
    seed, wdir, base = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    weights = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{POINT}.pt"), weights_only=False) for a in ARMS}
    cols = collect_graded(seed, weights, wc, tc, PAY[1], base)
    return {"seed": seed, "arms": {a: {t: calib_summary(*cols[a][t], seed=seed) for t in ("early", "late")}
                                   for a in ARMS}}


def measures(rec, arm):
    runs = [rec["arms"][arm][t] for t in ("early", "late") if rec["arms"][arm][t].get("fitted")]
    mean = lambda vs: (float(np.mean([v for v in vs if v is not None])) if any(v is not None for v in vs) else None)
    m = {k: mean([r.get(k) for r in runs]) for k in SCALARS}
    for k in KS_G:
        m[f"M2_E_k{k}"] = mean([r["M2_E_k"][str(k)] for r in runs if r.get("M2_E_k")])
        m[f"rel_k{k}"] = mean([r["rel_k"][str(k)] for r in runs if r.get("rel_k")])
    ks = [k for k in KS_G if m[f"M2_E_k{k}"] is not None]
    if len(ks) >= 3:
        x, yv = np.array(ks, float), np.array([m[f"M2_E_k{k}"] for k in ks])
        m["dose_rho"] = float(np.corrcoef(np.argsort(np.argsort(x)), np.argsort(np.argsort(yv)))[0, 1])
    else:
        m["dose_rho"] = None
    return m


def score(recs, replication=None):
    per = {r["seed"]: {a: measures(r, a) for a in ARMS} for r in recs}
    keys = list(next(iter(per.values()))["PFATE"].keys())
    arms = {a: {k: med(per[s][a][k] for s in per) for k in keys} for a in ARMS}
    P = lambda key, a, b: [(per[s][a][key], per[s][b][key]) for s in per]
    one = lambda key, a, hi="PRESENT", lo="REVERSED": one_sample([per[s][a][key] for s in per], hi, lo)
    ident = lambda v: v
    t1 = pair_test(P("M2_E", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    t2 = pair_test(P("type2_resid", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    t3 = one("rel_gap", "PFATE")
    adj = holm([t1["sign_p"], t2["sign_p"], t3["sign_p"]])
    t1 = relabel(t1, adj[0], "DERIVED_AHEAD", "HOST_AHEAD")
    t2 = relabel(t2, adj[1], "DERIVED_AHEAD", "HOST_AHEAD")
    t3 = relabel(t3, adj[2], "PRESENT", "REVERSED")
    dec_ok = (arms["PFATE"]["dec_acc_none"] or 0) >= DEC_VALID and (arms["PFATE"]["dec_acc_same"] or 0) >= DEC_VALID
    rep_valid = True if replication is None else bool(replication.get("valid"))
    sc = {"n_seeds": len(per), "valid": dec_ok and rep_valid, "decoder_valid": dec_ok,
          "replication": replication, "P1I_1": t1, "P1I_2": t2, "P1I_3": t3, "arms": arms, "per_seed": per,
          "secondary": {
              "M2_E_PFATE_vs_PYOKED": pair_test(P("M2_E", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
              "M2_E_PYOKED_vs_PNOFATE": pair_test(P("M2_E", "PYOKED", "PNOFATE"), ident, "DERIVED", "HOST"),
              "type2_resid_PYOKED_vs_PNOFATE": pair_test(P("type2_resid", "PYOKED", "PNOFATE"), ident, "DERIVED",
                                                         "HOST"),
              "type2_resid_pabs_PFATE_vs_PNOFATE": pair_test(P("type2_resid_pabs", "PFATE", "PNOFATE"), ident,
                                                             "DERIVED", "HOST"),
              "own_gap_PFATE_vs_PNOFATE": pair_test(P("own_gap", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
              # first = PNOFATE: DERIVED_AHEAD when PFATE's correlation is the more negative (stronger coupling)
              "trace_rho_PFATE_more_negative": pair_test(P("trace_rho", "PNOFATE", "PFATE"), ident, "DERIVED",
                                                          "HOST"),
              "routes": {k: {a: one(k, a) for a in ARMS}
                         for k in ("M2_E", "rel_gap", "own_gap", "dose_rho")
                         + tuple(f"M2_E_k{k}" for k in KS_G)},
              "type2_routes": {k: {a: one_sample([None if per[s][a][k] is None else per[s][a][k] - 0.5 for s in per],
                                                 "ABOVE_CHANCE", "BELOW_CHANCE") for a in ARMS}
                               for k in ("type2_resid", "type2_raw", "type2_resid_pabs")}}}
    sc["overall"] = overall(sc)
    return sc


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    l1, l2, l3 = sc["P1I_1"]["label"], sc["P1I_2"]["label"], sc["P1I_3"]["label"]
    if "UNDETERMINED" in (l1, l2, l3):
        return "UNDETERMINED"
    if l1 != "DERIVED_AHEAD":
        return "NOT_CONFIRMED"
    if l3 != "PRESENT":
        return "DISCOUNT_UNWARRANTED"
    return "CALIBRATED_DISCOUNT_CONFIRMED" if l2 == "DERIVED_AHEAD" else "DISCOUNT_CONFIRMED_NOT_CALIBRATED"


def tline(name, t):
    if "positive" in t:
        return (f"- {name}: {t['positive']}/{t['n']} > 0 (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)};"
                f" median {fmt(t['median'], 4)}) {t['label']}")
    return (f"- {name}: {t['first_ahead']}/{t['n']} (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)}; "
            f"{fmt(t['first_median'], 4)} against {fmt(t['second_median'], 4)}) {t['label']}")


def report(sc, title):
    rep = sc["replication"]
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}.** Valid: {sc['valid']} (evidence decoder held-out accuracy, PFATE: none "
         f"{fmt(sc['arms']['PFATE']['dec_acc_none'])}, same {fmt(sc['arms']['PFATE']['dec_acc_same'])}, needed >= "
         f"{DEC_VALID}; P1g design valid: {None if rep is None else rep.get('valid')}). Seeds: {sc['n_seeds']}. "
         f"Point: {POINT}.", ""]
    if rep:
        L += [f"P1g replication on these seeds: overall {rep.get('overall')}; L0 {rep.get('arrow')}; "
              f"P1G_1 {rep.get('P1G_1')}; P1G_2 {rep.get('P1G_2')}; P1G_3 {rep.get('P1G_3')}.", ""]
    cols = ["M2_E", "rel_gap", "own_gap", "type2_resid", "type2_raw", "type2_ev_raw", "type2_resid_pabs",
            "trace_rho", "coverage", "dec_acc_conflict", "agent_acc_conflict"] + \
           [f"M2_E_k{k}" for k in KS_G] + [f"rel_k{k}" for k in KS_G] + ["dose_rho"]
    L += ["| arm | " + " | ".join(cols) + " |", "| --- " * (len(cols) + 1) + "|"]
    for a in ARMS:
        L.append(f"| {a} | " + " | ".join(fmt(sc["arms"][a][c], 4) for c in cols) + " |")
    L += ["", tline("P1I_1 learned discount: M2_E, PFATE against PNOFATE", sc["P1I_1"]),
          tline("P1I_2 calibrated: type-2 AUC beyond evidence, PFATE against PNOFATE", sc["P1I_2"]),
          tline("P1I_3 warranted: reliability gap at matched evidence, PFATE against 0", sc["P1I_3"])]
    for k, t in sc["secondary"].items():
        if k.endswith("routes"):
            continue
        L.append(tline(k, t))
    for grp in ("routes", "type2_routes"):
        for k, d in sc["secondary"][grp].items():
            L.append(f"- route {k}: " + "; ".join(
                f"{a} {t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'], 4)}) {t['label']}"
                for a, t in d.items()))
    return "\n".join(L) + "\n"


def replication_summary(path):
    with open(path) as fh:
        g = json.load(fh)["scores"]
    p = g["points"][str(g["primary_at"])]
    return {"valid": g["valid"], "overall": g["overall"], "arrow": g["arrow"],
            **{k: f"{p[k].get('positive', p[k].get('first_ahead'))}/{p[k]['n']} {p[k]['label']}"
               for k in ("P1G_1", "P1G_2", "P1G_3")}}


def analyse(out, seeds, wdir, replication, title, stage):
    os.makedirs(out, exist_ok=True)
    if os.path.exists(os.path.join(out, "raw.json")):
        sys.exit("refusing to overwrite raw.json")
    with Pool(min(len(seeds), os.cpu_count() or 1)) as pool:
        recs = []
        for k, r in enumerate(pool.imap_unordered(analyse_seed, [(s, wdir, G.BASE_F) for s in seeds]), 1):
            recs.append(r)
            print(f"[analysis {k}/{len(seeds)}] seed {r['seed']}", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"stage": stage, "title": title, "seeds": seeds, "point": POINT, "base": G.BASE_F,
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(os.path.join(out, "raw.json"), "w") as fh:
        json.dump({"meta": meta, "seeds": recs, "replication": replication}, fh)
    sc = score(recs, replication)
    with open(os.path.join(out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    rep = report(sc, title)
    with open(os.path.join(out, "REPORT.md"), "w") as fh:
        fh.write(rep)
    print(rep)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", action="store_true")
    ap.add_argument("--analyse", action="store_true")
    ap.add_argument("--discovery", action="store_true")
    ap.add_argument("--score")
    ap.add_argument("--max-new", type=int, default=0)
    args = ap.parse_args()
    if args.train:
        train(args.max_new)
        return
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        print(report(score(d["seeds"], d["replication"]), d["meta"]["title"]), end="")
        return
    if args.discovery:
        analyse(os.path.join(OUT, "discovery"), list(G.FINAL_SEEDS), "p1g_graded/weights",
                replication_summary("p1g_graded/scores.json"),
                "P1i discovery: the P1i analysis on P1g's seeds (3200-3227)", "discovery")
        return
    if args.analyse:
        if not os.path.exists(os.path.join(TRAIN_DIR, "scores.json")):
            sys.exit("training is not finished")
        analyse(os.path.join(OUT, "confirm"), FINAL_SEEDS, os.path.join(TRAIN_DIR, "weights"),
                replication_summary(os.path.join(TRAIN_DIR, "scores.json")),
                "P1i: the calibrated integrity discount on fresh seeds (3400-3427)", "confirm")
        return
    sys.exit("choose --train, --discovery, --analyse or --score")


if __name__ == "__main__":
    main()
