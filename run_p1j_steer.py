"""P1j: does a content-free integrity variable causally set the agent's confidence in its own memory?

Protocol: P1J_STEER_PROTOCOL.md. Analysis: trackc_swap/steerint.py. Evaluation only, on saved weights (3600).

    python run_p1j_steer.py --discovery      # P1g's seeds 3200-3227 (discovery set, before the freeze)
    python run_p1j_steer.py --confirm        # P1i's seeds 3400-3427 (after the freeze)
    python run_p1j_steer.py --score p1j_steer/confirm
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
from trackc_swap.selfmon import ARMS_M
from trackc_swap.steerint import NORM_FIX, S_INJ, collect_steer
from trackc_swap.train import TrainConfig

DISCOVERY_SEEDS = list(range(3200, 3228))
CONFIRM_SEEDS = list(range(3400, 3428))
DISCOVERY_W = "p1g_graded/weights"
CONFIRM_W = "p1i_calib/p1g_design/weights"
OUT = "p1j_steer"
ARMS = ARMS_M
POINT = 3600
S_LIST = (3, S_INJ, 7)          # push steps; S_INJ (5) is primary
CONTENT_TOL = 0.02              # an accuracy change larger than this (median, detected) confounds the push
N_VALID = 20                    # at least this many seeds with a fitted primary run, PFATE and PNOFATE
SOURCES = G.SOURCES + ["trackc_swap/evidence.py", "trackc_swap/steerint.py", "run_p1h_evidence.py",
                       "run_p1j_steer.py", "P1J_STEER_PROTOCOL.md"]
KEYS = ("induce", "rescue", "gap", "induce_abs", "rescue_abs", "gap_abs", "induce_none", "acc_same_d_minus_r",
        "acc_conflict_d_minus_r", "random_same", "random_conflict", "induce_share", "rescue_share")
FKEYS = ("induce", "rescue", "induce_abs", "rescue_abs", "induce_none", "acc_same_d_minus_r",
         "acc_conflict_d_minus_r", "random_same", "random_conflict")
DKEYS = ("norm_d", "norm_d_raw", "norm_c", "norm_a", "share_d_kept", "cos_draw_c", "cos_draw_a")


def analyse_seed(job):
    seed, wdir = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    weights = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{POINT}.pt"), weights_only=False) for a in ARMS}
    return {"seed": seed, "s": {str(s): collect_steer(seed, weights, wc, tc, PAY[1], G.BASE_F, ARMS, s_inj=s)
                                for s in S_LIST}}


def measures(rec, arm, s):
    r = rec["s"][str(s)][arm]
    st, sf, dr = r["steer"], r["steer_fix"], r["dirs"]
    m = {k: (st.get(k) if st.get("fitted") else None) for k in KEYS}
    m.update({f"{k}_fix": (sf.get(k) if sf.get("fitted") else None) for k in FKEYS})
    m.update({k: dr.get(k) for k in DKEYS})
    two = lambda a, b: None if a is None or b is None else float(a + b)
    m["signed"] = two(m["induce"], m["rescue"])                # > 0 only for a signed variable (both ways)
    m["signed_fix"] = two(m["induce_fix"], m["rescue_fix"])
    m["fitted"] = bool(st.get("fitted")) and m["induce"] is not None and m["rescue"] is not None
    return m


def score(recs):
    per = {r["seed"]: {str(s): {a: measures(r, a, s) for a in ARMS} for s in S_LIST} for r in recs}
    P = lambda key, a, b, s=S_INJ: [(per[x][str(s)][a][key], per[x][str(s)][b][key]) for x in per]
    one = lambda key, a, s=S_INJ, hi="PRESENT", lo="REVERSED": one_sample([per[x][str(s)][a][key] for x in per],
                                                                          hi, lo)
    ident = lambda v: v
    t1 = one("induce", "PFATE")
    t2 = one("rescue", "PFATE")
    t3 = pair_test(P("signed", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    t4 = pair_test(P("signed_fix", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    adj = holm([t1["sign_p"], t2["sign_p"], t3["sign_p"], t4["sign_p"]])
    t1 = relabel(t1, adj[0], "PRESENT", "REVERSED")
    t2 = relabel(t2, adj[1], "PRESENT", "REVERSED")
    t3 = relabel(t3, adj[2], "DERIVED_AHEAD", "HOST_AHEAD")
    t4 = relabel(t4, adj[3], "DERIVED_AHEAD", "HOST_AHEAD")
    allk = KEYS + ("signed", "signed_fix") + tuple(f"{k}_fix" for k in FKEYS) + DKEYS
    arms = {str(s): {a: {k: med(per[x][str(s)][a][k] for x in per) for k in allk} for a in ARMS}
            for s in S_LIST}
    n_fit = {a: sum(per[x][str(S_INJ)][a]["fitted"] for x in per) for a in ARMS}
    valid = n_fit["PFATE"] >= N_VALID and n_fit["PNOFATE"] >= N_VALID
    c_same = one("acc_same_d_minus_r", "PFATE")
    c_conf = one("acc_conflict_d_minus_r", "PFATE")
    conf_same = c_same["label"] == "REVERSED" and (c_same["median"] or 0) <= -CONTENT_TOL
    conf_conf = c_conf["label"] == "PRESENT" and (c_conf["median"] or 0) >= CONTENT_TOL
    sec = {"induce_PFATE_vs_PNOFATE": pair_test(P("induce", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
           "induce_fix_PFATE_vs_PNOFATE": pair_test(P("induce_fix", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
           "signed_PFATE_vs_PYOKED": pair_test(P("signed", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
           "rescue_fix_PFATE_vs_PNOFATE": pair_test(P("rescue_fix", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
           "rescue_PFATE_vs_PNOFATE": pair_test(P("rescue", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
           "induce_PFATE_vs_PYOKED": pair_test(P("induce", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
           "induce_abs_PFATE_vs_PNOFATE": pair_test(P("induce_abs", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
           "norm_d_PFATE_vs_PNOFATE": pair_test(P("norm_d", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")}
    routes = {f"s{s}": {k: {a: one(k, a, s) for a in ARMS}
                        for k in KEYS[:2] + ("induce_abs", "rescue_abs", "induce_none", "acc_same_d_minus_r",
                                             "acc_conflict_d_minus_r", "random_same", "random_conflict")
                        + ("signed", "signed_fix") + tuple(f"{k}_fix" for k in FKEYS)}
              for s in S_LIST}
    sc = {"n_seeds": len(per), "valid": valid, "n_fitted": n_fit, "P1J_1": t1, "P1J_2": t2, "P1J_3": t3, "P1J_4": t4,
          "content": {"same": c_same, "conflict": c_conf, "confounded_induce": conf_same,
                      "confounded_rescue": conf_conf},
          "arms": arms, "secondary": sec, "routes": routes, "per_seed": per}
    sc["overall"] = overall(sc)
    return sc


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    l1, l2, l3, l4 = (sc[k]["label"] for k in ("P1J_1", "P1J_2", "P1J_3", "P1J_4"))
    if "UNDETERMINED" in (l1, l2, l3, l4):
        return "UNDETERMINED"
    ind, res = l1 == "PRESENT", l2 == "PRESENT"
    if (ind and sc["content"]["confounded_induce"]) or (res and sc["content"]["confounded_rescue"]):
        return "CONTENT_CONFOUNDED"
    if ind and res:
        if l3 != "DERIVED_AHEAD":
            return "CAUSAL_NOT_LEARNED"
        return "LEARNED_SIGNED_INTEGRITY_VARIABLE" if l4 == "DERIVED_AHEAD" else "LEARNED_VARIABLE_GENERIC_COUPLING"
    if ind or res:
        return "ONE_WAY"
    return "NO_CAUSAL_SIGNAL"


def tline(name, t):
    if "positive" in t:
        return (f"- {name}: {t['positive']}/{t['n']} > 0 (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)};"
                f" median {fmt(t['median'], 4)}) {t['label']}")
    return (f"- {name}: {t['first_ahead']}/{t['n']} (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)}; "
            f"{fmt(t['first_median'], 4)} against {fmt(t['second_median'], 4)}) {t['label']}")


def report(sc, title):
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}.** Valid: {sc['valid']} (seeds with a fitted primary run: "
         f"{sc['n_fitted']}; needed >= {N_VALID} for PFATE and PNOFATE). Seeds: {sc['n_seeds']}. Point: {POINT}. "
         f"Primary push step: {S_INJ}.", ""]
    allk = KEYS + ("signed", "signed_fix") + tuple(f"{k}_fix" for k in FKEYS) + DKEYS
    for s in S_LIST:
        L += [f"## Push at delay step {s}" + (" (primary)" if s == S_INJ else ""), "",
              "| measure | " + " | ".join(ARMS) + " |", "| --- " * (len(ARMS) + 1) + "|"]
        for k in allk:
            L.append(f"| {k} | " + " | ".join(fmt(sc["arms"][str(s)][a][k], 4) for a in ARMS) + " |")
        L.append("")
    L += ["## Tests", "",
          tline("P1J_1 induce: |z|(same, +r) - |z|(same, +d), PFATE against 0", sc["P1J_1"]),
          tline("P1J_2 rescue: |z|(conflict, -d) - |z|(conflict, -r), PFATE against 0", sc["P1J_2"]),
          tline("P1J_3 learned variable: signed (induce + rescue, natural size), PFATE against PNOFATE", sc["P1J_3"]),
          tline(f"P1J_4 learned use: signed at push norm {NORM_FIX}, PFATE against PNOFATE", sc["P1J_4"]),
          tline("content, same trials: accuracy (+d) - (+r), PFATE", sc["content"]["same"]),
          tline("content, conflict trials: accuracy (-d) - (-r), PFATE", sc["content"]["conflict"]),
          f"- content confound flags: induce {sc['content']['confounded_induce']}, rescue "
          f"{sc['content']['confounded_rescue']} (tolerance {CONTENT_TOL})"]
    for k, t in sc["secondary"].items():
        L.append(tline(k, t))
    for s, d in sc["routes"].items():
        for k, dd in d.items():
            L.append(f"- route {s} {k}: " + "; ".join(
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
    meta = {"stage": stage, "title": title, "seeds": seeds, "point": POINT, "s_list": list(S_LIST),
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
        analyse(os.path.join(OUT, "discovery"), DISCOVERY_SEEDS, DISCOVERY_W,
                "P1j discovery: steering the integrity direction on P1g's seeds (3200-3227)", "discovery")
        return
    if args.confirm:
        analyse(os.path.join(OUT, "confirm"), CONFIRM_SEEDS, CONFIRM_W,
                "P1j: steering the integrity direction on P1i's seeds (3400-3427)", "confirm")
        return
    sys.exit("choose --discovery, --confirm or --score")


if __name__ == "__main__":
    main()
