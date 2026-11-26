"""P1k: is P1j's integrity variable general across damage types never seen in training?

Protocol: P1K_TRANSFER_PROTOCOL.md. Analysis: trackc_swap/transfer.py. Evaluation only, on saved weights (3600).

    python run_p1k_transfer.py --discovery      # P1g's seeds 3200-3227 (discovery set, before the freeze)
    python run_p1k_transfer.py --confirm        # P1i's seeds 3400-3427 (after the freeze)
    python run_p1k_transfer.py --score p1k_transfer/confirm
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
from trackc_swap.env import WorldConfig
from trackc_swap.gradmon import KS_G
from trackc_swap.selfmon import ARMS_M
from trackc_swap.train import TrainConfig
from trackc_swap.transfer import NOVEL, OPS, collect_transfer

DISCOVERY_SET = list(range(3200, 3228))
CONFIRM_SET = list(range(3400, 3428))
DISCOVERY_W = "p1g_graded/weights"
CONFIRM_W = "p1i_calib/p1g_design/weights"
OUT = "p1k_transfer"
ARMS = ARMS_M
POINT = 3600
CONTENT_TOL = 0.02
N_VALID = 20
SOURCES = G.SOURCES + ["trackc_swap/evidence.py", "trackc_swap/steerint.py", "trackc_swap/transfer.py",
                       "run_p1h_evidence.py", "run_p1k_transfer.py", "P1K_TRANSFER_PROTOCOL.md"]
OKEYS = ("act", "alpha", "cos", "shift_norm", "dose_rho", "rescue", "gap", "rescue_share", "rescue_abs", "gap_abs",
         "acc_d_minus_r", "acc_dmg") + tuple(f"act_k{k}" for k in KS_G) + tuple(f"acc_k{k}" for k in KS_G)


def analyse_seed(job):
    seed, wdir = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    weights = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{POINT}.pt"), weights_only=False) for a in ARMS}
    return {"seed": seed, "arms": collect_transfer(seed, weights, wc, tc, PAY[1], G.BASE_F, ARMS)}


def _rank(x):
    return np.argsort(np.argsort(np.asarray(x, float)))


def measures(rec, arm, op):
    r = rec["arms"][arm]["ops"].get(op)
    m = {k: None for k in OKEYS}
    if not r:
        m["fitted"] = False
        return m
    a, s = r["activation"], r["rescue"]
    m["act"], m["cos"], m["shift_norm"] = a.get("act"), a.get("cos"), a.get("shift_norm")
    ref = rec["arms"][arm]["ops"].get("donor", {}).get("activation", {}).get("act")
    m["alpha"] = (m["act"] / ref) if (m["act"] is not None and ref) else None
    for k in KS_G:
        m[f"act_k{k}"] = (a.get("act_k") or {}).get(str(k))
        m[f"acc_k{k}"] = (s.get("acc_k") or {}).get(str(k)) if s.get("fitted") else None
    ks = [k for k in KS_G if m[f"act_k{k}"] is not None]
    m["dose_rho"] = (float(np.corrcoef(_rank(ks), _rank([m[f"act_k{k}"] for k in ks]))[0, 1])
                     if len(ks) >= 3 else None)
    for k in ("rescue", "gap", "rescue_share", "rescue_abs", "gap_abs", "acc_d_minus_r", "acc_dmg"):
        m[k] = s.get(k) if s.get("fitted") else None
    m["fitted"] = m["act"] is not None and m["rescue"] is not None
    return m


def score(recs):
    per = {r["seed"]: {a: {op: measures(r, a, op) for op in OPS} for a in ARMS} for r in recs}
    one = lambda key, a, op, hi="PRESENT", lo="REVERSED": one_sample([per[x][a][op][key] for x in per], hi, lo)
    P = lambda key, a, b, op: [(per[x][a][op][key], per[x][b][op][key]) for x in per]
    ident = lambda v: v
    prim = {}
    for op in NOVEL:
        prim[f"P1K_ACT_{op}"] = one("act", "PFATE", op)
        prim[f"P1K_RES_{op}"] = one("rescue", "PFATE", op)
    names = list(prim)
    adj = holm([prim[k]["sign_p"] for k in names])
    prim = {k: relabel(prim[k], p, "PRESENT", "REVERSED") for k, p in zip(names, adj)}
    ref_res = one("rescue", "PFATE", "donor")
    ref_act = one("act", "PFATE", "donor")
    n_fit = {a: sum(per[x][a]["donor"]["fitted"] for x in per) for a in ARMS}
    valid = n_fit["PFATE"] >= N_VALID and n_fit["PNOFATE"] >= N_VALID and ref_res["label"] == "PRESENT"
    content = {op: one("acc_d_minus_r", "PFATE", op) for op in OPS}
    confounded = {op: content[op]["label"] == "PRESENT" and (content[op]["median"] or 0) >= CONTENT_TOL for op in OPS}
    per_op = {op: op_label(prim[f"P1K_ACT_{op}"]["label"], prim[f"P1K_RES_{op}"]["label"], confounded[op])
              for op in NOVEL}
    arms = {a: {op: {k: med(per[x][a][op][k] for x in per) for k in OKEYS} for op in OPS} for a in ARMS}
    sec = {}
    sec["act_same_vs_scramble_PFATE"] = pair_test([(per[x]["PFATE"]["same"]["act"], per[x]["PFATE"]["scramble"]["act"])
                                                   for x in per], ident, "SAME", "SCRAMBLE")
    for op in OPS:
        sec[f"act_{op}_PFATE_vs_PNOFATE"] = pair_test(P("alpha", "PFATE", "PNOFATE", op), ident, "DERIVED", "HOST")
        sec[f"rescue_{op}_PFATE_vs_PNOFATE"] = pair_test(P("rescue", "PFATE", "PNOFATE", op), ident, "DERIVED", "HOST")
        sec[f"rescue_{op}_PFATE_vs_PYOKED"] = pair_test(P("rescue", "PFATE", "PYOKED", op), ident, "DERIVED", "YOKED")
    routes = {op: {k: {a: one(k, a, op) for a in ARMS} for k in ("act", "rescue", "rescue_abs", "gap", "dose_rho",
                                                                 "cos", "acc_d_minus_r")} for op in OPS}
    sc = {"n_seeds": len(per), "valid": valid, "n_fitted": n_fit, "reference": {"act": ref_act, "rescue": ref_res},
          "primaries": prim, "content": content, "confounded": confounded, "per_op": per_op, "arms": arms,
          "secondary": sec, "routes": routes, "per_seed": per}
    sc["overall"] = overall(sc)
    return sc


def op_label(act, res, confounded):
    if "UNDETERMINED" in (act, res):
        return "UNDETERMINED"
    a, r = act == "PRESENT", res == "PRESENT"
    if r and confounded:
        return "CONTENT_CONFOUNDED"
    if a and r:
        return "GENERALIZES"
    if a:
        return "ACTIVATES_NOT_USED"
    if r:
        return "USED_NOT_ACTIVATED"
    return "NOT_GENERAL"


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    labs = list(sc["per_op"].values())
    if "UNDETERMINED" in labs:
        return "UNDETERMINED"
    n = sum(l == "GENERALIZES" for l in labs)
    if n == len(labs):
        return "GENERAL_INTEGRITY_VARIABLE"
    return "PARTIAL_GENERALITY" if n else "DONOR_SPECIFIC"


def tline(name, t):
    if "positive" in t:
        return (f"- {name}: {t['positive']}/{t['n']} > 0 (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)};"
                f" median {fmt(t['median'], 4)}) {t['label']}")
    return (f"- {name}: {t['first_ahead']}/{t['n']} (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)}; "
            f"{fmt(t['first_median'], 4)} against {fmt(t['second_median'], 4)}) {t['label']}")


def report(sc, title):
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}.** Per operator: " + ", ".join(f"{op} {l}" for op, l in sc["per_op"].items())
         + f". Valid: {sc['valid']} (fitted seeds {sc['n_fitted']}, needed >= {N_VALID} for PFATE and PNOFATE; "
         f"reference rescue on donor conflicts {sc['reference']['rescue']['label']}). Seeds: {sc['n_seeds']}. "
         f"Point: {POINT}.", ""]
    for a in ARMS:
        L += [f"## {a}", "", "| measure | " + " | ".join(OPS) + " |", "| --- " * (len(OPS) + 1) + "|"]
        for k in OKEYS:
            L.append(f"| {k} | " + " | ".join(fmt(sc["arms"][a][op][k], 4) for op in OPS) + " |")
        L.append("")
    L += ["## Tests", "",
          tline("reference: activation on donor conflicts, PFATE", sc["reference"]["act"]),
          tline("reference: rescue on donor conflicts, PFATE (validity)", sc["reference"]["rescue"])]
    for k, t in sc["primaries"].items():
        L.append(tline(k, t))
    for op, t in sc["content"].items():
        L.append(tline(f"content {op}: accuracy (-d) - (-r), PFATE", t) + f"; confounded {sc['confounded'][op]}")
    for k, t in sc["secondary"].items():
        L.append(tline(k, t))
    for op, d in sc["routes"].items():
        for k, dd in d.items():
            L.append(f"- route {op} {k}: " + "; ".join(
                f"{a} {t['positive']}/{t['n']} (p {fmt(t['sign_p'], 4)}; median {fmt(t['median'], 4)}) {t['label']}"
                for a, t in dd.items()))
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
    meta = {"stage": stage, "title": title, "seeds": seeds, "point": POINT, "ops": list(OPS),
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
                "P1k discovery: the integrity variable under damage never seen in training, P1g's seeds (3200-3227)",
                "discovery")
        return
    if args.confirm:
        analyse(os.path.join(OUT, "confirm"), CONFIRM_SET, CONFIRM_W,
                "P1k: the integrity variable under damage never seen in training, P1i's seeds (3400-3427)", "confirm")
        return
    sys.exit("choose --discovery, --confirm or --score")


if __name__ == "__main__":
    main()
