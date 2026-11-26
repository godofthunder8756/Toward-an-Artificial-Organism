"""P1l: is the integrity variable accessible to a second consumer, and is it the same variable?

Protocol: P1L_ACCESS_PROTOCOL.md. Analysis: trackc_swap/access.py. Evaluation only, on saved weights (3600).

    python run_p1l_access.py --discovery      # P1g's seeds 3200-3227 (discovery set, before the freeze)
    python run_p1l_access.py --confirm        # P1i's seeds 3400-3427 (after the freeze)
    python run_p1l_access.py --score p1l_access/confirm
"""
import argparse
import json
import os
import platform
import sys
from multiprocessing import Pool

import numpy as np
import torch

import run_p1g_graded as G
from run_p1_selfeval import one_sample
from run_p1h_evidence import relabel
from run_trackc_paid import PAY, WEAR
from run_trackc_paid2 import holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.access import collect_access
from trackc_swap.env import WorldConfig
from trackc_swap.selfmon import ARMS_M
from trackc_swap.train import TrainConfig
from trackc_swap.transfer import NOVEL

DISCOVERY_SET = list(range(3200, 3228))
CONFIRM_SET = list(range(3400, 3428))
DISCOVERY_W = "p1g_graded/weights"
CONFIRM_W = "p1i_calib/p1g_design/weights"
OUT = "p1l_access"
ARMS = ARMS_M
POINT = 3600
AUC_VALID = 0.70
N_VALID = 20
SOURCES = G.SOURCES + ["trackc_swap/evidence.py", "trackc_swap/calibdisc.py", "trackc_swap/steerint.py",
                       "trackc_swap/transfer.py", "trackc_swap/access.py", "run_p1h_evidence.py",
                       "run_p1l_access.py", "P1L_ACCESS_PROTOCOL.md"]
OPS_AUC = ("donor", "donor_vs_same", "same") + NOVEL
KEYS = tuple(f"auc_{o}" for o in OPS_AUC) + ("auc_novel", "signed_rep", "induce_rep", "rescue_rep", "gap_rep",
                                             "induce_conf", "rescue_conf", "corr_d9", "corr_c9")


def analyse_seed(job):
    seed, wdir = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    weights = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{POINT}.pt"), weights_only=False) for a in ARMS}
    return {"seed": seed, "arms": collect_access(seed, weights, wc, tc, PAY[1], G.BASE_F, ARMS)}


def measures(rec, arm):
    r = rec["arms"][arm]
    m = {k: None for k in KEYS}
    m["fitted"] = bool(r.get("fitted"))
    if not m["fitted"]:
        return m
    for o in OPS_AUC:
        m[f"auc_{o}"] = r["auc"].get(o)
    nov = [m[f"auc_{o}"] for o in NOVEL]
    m["auc_novel"] = float(np.mean(nov)) if all(x is not None for x in nov) else None
    for k in ("signed_rep", "induce_rep", "rescue_rep", "gap_rep", "induce_conf", "rescue_conf", "corr_d9",
              "corr_c9"):
        m[k] = r.get(k)
    return m


def score(recs):
    per = {r["seed"]: {a: measures(r, a) for a in ARMS} for r in recs}
    c05 = lambda v: None if v is None else v - 0.5
    one = lambda key, a, f=lambda v: v, hi="PRESENT", lo="REVERSED": one_sample([f(per[x][a][key]) for x in per],
                                                                                 hi, lo)
    P = lambda key, a, b: [(per[x][a][key], per[x][b][key]) for x in per]
    ident = lambda v: v
    t1 = one("auc_novel", "PFATE", c05)
    t2 = pair_test(P("auc_novel", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    t3 = one("signed_rep", "PFATE")
    adj = holm([t1["sign_p"], t2["sign_p"], t3["sign_p"]])
    t1 = relabel(t1, adj[0], "PRESENT", "REVERSED")
    t2 = relabel(t2, adj[1], "DERIVED_AHEAD", "HOST_AHEAD")
    t3 = relabel(t3, adj[2], "PRESENT", "REVERSED")
    arms = {a: {k: med(per[x][a][k] for x in per) for k in KEYS} for a in ARMS}
    n_fit = {a: sum(per[x][a]["fitted"] for x in per) for a in ARMS}
    valid = (n_fit["PFATE"] >= N_VALID and n_fit["PNOFATE"] >= N_VALID
             and (arms["PFATE"]["auc_donor"] or 0) >= AUC_VALID)
    sec = {"signed_rep_PFATE_vs_PNOFATE": pair_test(P("signed_rep", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
           "auc_novel_PFATE_vs_PYOKED": pair_test(P("auc_novel", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
           "auc_donor_PFATE_vs_PNOFATE": pair_test(P("auc_donor", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
           "auc_scramble_vs_same_PFATE": pair_test([(per[x]["PFATE"]["auc_scramble"], per[x]["PFATE"]["auc_same"])
                                                    for x in per], ident, "SCRAMBLE", "SAME")}
    routes = {}
    for k in KEYS:
        f = c05 if k.startswith("auc_") else ident
        routes[k] = {a: one(k, a, f) for a in ARMS}
    sc = {"n_seeds": len(per), "valid": valid, "n_fitted": n_fit, "P1L_1": t1, "P1L_2": t2, "P1L_3": t3,
          "arms": arms, "secondary": sec, "routes": routes, "per_seed": per}
    sc["overall"] = overall(sc)
    return sc


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    l1, l2, l3 = sc["P1L_1"]["label"], sc["P1L_2"]["label"], sc["P1L_3"]["label"]
    if "UNDETERMINED" in (l1, l2, l3):
        return "UNDETERMINED"
    if l1 != "PRESENT":
        return "NOT_GENERAL"
    learned, shared = l2 == "DERIVED_AHEAD", l3 == "PRESENT"
    if shared:
        return "SHARED_GENERAL_ACCESS" if learned else "SHARED_ACCESS_NOT_LEARNED"
    return "GENERAL_ACCESS_SEPARATE_ROUTE" if learned else "GENERAL_ACCESS_NOT_LEARNED"


def tline(name, t):
    if "positive" in t:
        return (f"- {name}: {t['positive']}/{t['n']} > 0 (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)};"
                f" median {fmt(t['median'], 4)}) {t['label']}")
    return (f"- {name}: {t['first_ahead']}/{t['n']} (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)}; "
            f"{fmt(t['first_median'], 4)} against {fmt(t['second_median'], 4)}) {t['label']}")


def report(sc, title):
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}.** Valid: {sc['valid']} (fitted seeds {sc['n_fitted']}, needed >= {N_VALID} for "
         f"PFATE and PNOFATE; PFATE held-out AUC on the trained damage {fmt(sc['arms']['PFATE']['auc_donor'], 3)}, "
         f"needed >= {AUC_VALID}). Seeds: {sc['n_seeds']}. Point: {POINT}.", "",
         "| measure | " + " | ".join(ARMS) + " |", "| --- " * (len(ARMS) + 1) + "|"]
    for k in KEYS:
        L.append(f"| {k} | " + " | ".join(fmt(sc["arms"][a][k], 4) for a in ARMS) + " |")
    L += ["", "## Tests", "",
          tline("P1L_1 general: mean AUC on the three novel damage types - 0.5, PFATE", sc["P1L_1"]),
          tline("P1L_2 learned access: mean novel AUC, PFATE against PNOFATE", sc["P1L_2"]),
          tline("P1L_3 shared variable: signed_rep (moving d moves the read-out), PFATE", sc["P1L_3"])]
    for k, t in sc["secondary"].items():
        L.append(tline(k, t))
    for k, d in sc["routes"].items():
        L.append(f"- route {k}" + (" (- 0.5)" if k.startswith("auc_") else "") + ": " + "; ".join(
            f"{a} {t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'], 4)}) {t['label']}"
            for a, t in d.items()))
    return "\n".join(L) + "\n"


def analyse(out, seeds, wdir, title, stage):
    os.makedirs(out, exist_ok=True)
    if os.path.exists(os.path.join(out, "raw.json")):
        sys.exit("refusing to overwrite raw.json")
    with Pool(min(len(seeds), os.cpu_count() or 1)) as pool:
        recs = []
        for k, r in enumerate(pool.imap_unordered(analyse_seed, [(s, wdir) for s in seeds]), 1):
            recs.append(r)
            print(f"[analysis {k}/{len(seeds)}] seed {r['seed']}", flush=True)
    recs.sort(key=lambda r: r["seed"])
    meta = {"stage": stage, "title": title, "seeds": seeds, "point": POINT,
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(os.path.join(out, "raw.json"), "w") as fh:
        json.dump({"meta": meta, "seeds": recs}, fh)
    sc = score(recs)
    with open(os.path.join(out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    rep = report(sc, title)
    with open(os.path.join(out, "REPORT.md"), "w") as fh:
        fh.write(rep)
    print(rep)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--discovery", action="store_true")
    ap.add_argument("--confirm", action="store_true")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        print(report(score(d["seeds"]), d["meta"]["title"]), end="")
        return
    if args.discovery:
        analyse(os.path.join(OUT, "discovery"), DISCOVERY_SET, DISCOVERY_W,
                "P1l discovery: a second consumer of the integrity variable, P1g's seeds (3200-3227)",
                "discovery")
        return
    if args.confirm:
        analyse(os.path.join(OUT, "confirm"), CONFIRM_SET, CONFIRM_W,
                "P1l: a second consumer of the integrity variable, P1i's seeds (3400-3427)", "confirm")
        return
    sys.exit("choose --discovery, --confirm or --score")


if __name__ == "__main__":
    main()
