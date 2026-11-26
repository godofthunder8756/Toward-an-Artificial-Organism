"""P1m (Q-NECESSITY): does the integrity variable add value for the agent against the strongest simpler rival?

Protocol: P1M_NECESSITY_PROTOCOL.md. Analysis: trackc_swap/necessity.py. Evaluation only, on saved weights (3600).

    python run_p1m_necessity.py --discovery      # P1g's seeds 3200-3227 (discovery set, before the freeze)
    python run_p1m_necessity.py --confirm        # P1i's seeds 3400-3427 (after the freeze)
    python run_p1m_necessity.py --score p1m_necessity/confirm
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
from trackc_swap.necessity import collect_necessity
from trackc_swap.selfmon import ARMS_M
from trackc_swap.train import TrainConfig
from trackc_swap.transfer import NOVEL

DISCOVERY_SET = list(range(3200, 3228))
CONFIRM_SET = list(range(3400, 3428))
DISCOVERY_W = "p1g_graded/weights"
CONFIRM_W = "p1i_calib/p1g_design/weights"
OUT = "p1m_necessity"
ARMS = ARMS_M
POINT = 3600
OPS = ("donor",) + NOVEL
CONTENT_TOL = 0.02
FLAG_MIN = 0.005
N_VALID = 20
SOURCES = G.SOURCES + ["trackc_swap/evidence.py", "trackc_swap/steerint.py", "trackc_swap/transfer.py",
                       "trackc_swap/necessity.py", "run_p1h_evidence.py", "run_p1m_necessity.py",
                       "P1M_NECESSITY_PROTOCOL.md"]
KEYS = ("dV_star", "dV_used", "room", "dV_star_nat", "dV_used_nat", "room_nat", "dV_star_strict", "room_strict",
        "vstar_intact", "vstar_lesion", "vstar_flag_lesion", "vstar_oracle_lesion", "recovery", "used_intact", "used_lesion", "d_used_none", "d_used_same", "d_used_dmg", "d_acc_none",
        "d_acc_dmg", "acc_dmg_intact")


def analyse_seed(job):
    seed, wdir = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    weights = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{POINT}.pt"), weights_only=False) for a in ARMS}
    return {"seed": seed, "arms": collect_necessity(seed, weights, wc, tc, PAY[1], G.BASE_F, ARMS)}


def measures(rec, arm, op):
    r = rec["arms"][arm]
    m = {k: None for k in KEYS}
    m["fitted"] = bool(r.get("fitted")) and op in r.get("ops", {})
    if not m["fitted"]:
        return m
    i, l = r["ops"][op]["intact"], r["ops"][op]["lesion"]
    dif = lambda a, b: None if a is None or b is None else float(a - b)
    m["dV_star"], m["dV_used"] = dif(i["vstar_probe"], l["vstar_probe"]), dif(i["used_probe"], l["used_probe"])
    m["dV_star_nat"], m["dV_used_nat"] = dif(i["vstar_natural"], l["vstar_natural"]), \
        dif(i["used_natural"], l["used_natural"])
    m["vstar_intact"], m["vstar_lesion"], m["vstar_flag_lesion"] = i["vstar_probe"], l["vstar_probe"], \
        l["vstar_flag_probe"]
    m["vstar_oracle_lesion"] = l["vstar_oracle_probe"]
    m["room"] = dif(l["vstar_oracle_probe"], l["vstar_probe"])
    m["room_nat"] = dif(l["vstar_oracle_natural"], l["vstar_natural"])
    m["dV_star_strict"] = dif(i["vstar_strict"], l["vstar_strict"])
    m["room_strict"] = dif(l["vstar_oracle_strict"], l["vstar_strict"])
    den = m["room"]
    m["recovery"] = (m["dV_star"] / den) if den is not None and den > FLAG_MIN else None
    m["used_intact"], m["used_lesion"] = i["used_probe"], l["used_probe"]
    ug = lambda d, g: d["used_by_group"].get(g)
    m["d_used_none"], m["d_used_same"], m["d_used_dmg"] = (dif(ug(i, g), ug(l, g)) for g in ("0", "1", "2"))
    m["d_acc_none"], m["d_acc_dmg"] = dif(i["acc"]["0"], l["acc"]["0"]), dif(i["acc"]["2"], l["acc"]["2"])
    m["acc_dmg_intact"] = i["acc"]["2"]
    return m


def score(recs):
    per = {r["seed"]: {a: {op: measures(r, a, op) for op in OPS} for a in ARMS} for r in recs}
    one = lambda key, a, op="donor", hi="PRESENT", lo="REVERSED": one_sample([per[x][a][op][key] for x in per], hi, lo)
    P = lambda key, a, b, op="donor": [(per[x][a][op][key], per[x][b][op][key]) for x in per]
    ident = lambda v: v
    t1 = one("dV_star", "PFATE")
    t2 = one("dV_used", "PFATE")
    t3 = pair_test(P("dV_star", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST")
    adj = holm([t1["sign_p"], t2["sign_p"], t3["sign_p"]])
    t1 = relabel(t1, adj[0], "PRESENT", "REVERSED")
    t2 = relabel(t2, adj[1], "PRESENT", "REVERSED")
    t3 = relabel(t3, adj[2], "DERIVED_AHEAD", "HOST_AHEAD")
    room = one("room", "PFATE")
    room_ok = room["label"] == "PRESENT" and (room["median"] or 0) >= FLAG_MIN
    n_fit = {a: sum(per[x][a]["donor"]["fitted"] for x in per) for a in ARMS}
    valid = n_fit["PFATE"] >= N_VALID and n_fit["PNOFATE"] >= N_VALID
    c_dmg, c_none = one("d_acc_dmg", "PFATE"), one("d_acc_none", "PFATE")
    confounded = ((c_dmg["label"] == "PRESENT" and (c_dmg["median"] or 0) >= CONTENT_TOL)
                  or (c_none["label"] == "PRESENT" and (c_none["median"] or 0) >= CONTENT_TOL))
    arms = {a: {op: {k: med(per[x][a][op][k] for x in per) for k in KEYS} for op in OPS} for a in ARMS}
    sec = {"dV_used_PFATE_vs_PNOFATE": pair_test(P("dV_used", "PFATE", "PNOFATE"), ident, "DERIVED", "HOST"),
           "dV_star_PFATE_vs_PYOKED": pair_test(P("dV_star", "PFATE", "PYOKED"), ident, "DERIVED", "YOKED"),
           "vstar_intact_PFATE_vs_PNOFATE": pair_test(P("vstar_intact", "PFATE", "PNOFATE"), ident, "DERIVED",
                                                      "HOST")}
    routes = {op: {k: {a: one(k, a, op) for a in ARMS}
                   for k in ("dV_star", "dV_used", "room", "dV_star_nat", "dV_used_nat", "room_nat", "dV_star_strict",
                             "room_strict", "recovery", "d_used_none",
                             "d_used_same", "d_used_dmg", "d_acc_none", "d_acc_dmg")} for op in OPS}
    sc = {"n_seeds": len(per), "valid": valid, "n_fitted": n_fit, "P1M_1": t1, "P1M_2": t2, "P1M_3": t3,
          "content": {"dmg": c_dmg, "none": c_none, "confounded": confounded}, "room": room, "room_ok": room_ok, "arms": arms, "secondary": sec,
          "routes": routes, "per_seed": per}
    sc["overall"] = overall(sc)
    return sc


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    l1, l2, l3 = sc["P1M_1"]["label"], sc["P1M_2"]["label"], sc["P1M_3"]["label"]
    if "UNDETERMINED" in (l1, l2, l3):
        return "UNDETERMINED"
    if l1 == "PRESENT" and sc["content"]["confounded"]:
        return "CONTENT_CONFOUNDED"
    if l1 == "PRESENT":
        if l3 != "DERIVED_AHEAD":
            return "VALUE_NOT_LEARNED"
        return "VALUE_CREDITED" if l2 == "PRESENT" else "VALUE_CREDITED_NOT_AS_USED"
    if not sc["room_ok"]:
        return "NECESSITY_NOT_TESTABLE_USED" if l2 == "PRESENT" else "NECESSITY_NOT_TESTABLE"
    if l2 == "PRESENT":
        return "USED_NOT_NECESSARY"
    return "VARIABLE_COSTLY" if l1 == "REVERSED" else "NO_VALUE_DETECTED"


def tline(name, t):
    if "positive" in t:
        return (f"- {name}: {t['positive']}/{t['n']} > 0 (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)};"
                f" median {fmt(t['median'], 4)}) {t['label']}")
    return (f"- {name}: {t['first_ahead']}/{t['n']} (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)}; "
            f"{fmt(t['first_median'], 4)} against {fmt(t['second_median'], 4)}) {t['label']}")


def report(sc, title):
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}.** Valid: {sc['valid']} (fitted seeds {sc['n_fitted']}, needed >= {N_VALID} for "
         f"PFATE and PNOFATE). Content confound: {sc['content']['confounded']}. Room (the supplied oracle adds value "
         f"over the re-tuned lesioned agent, PFATE, median >= {FLAG_MIN}): {sc['room_ok']}. Seeds: {sc['n_seeds']}. "
         f"Point: {POINT}. Payoff per probe trial: +1 correct, -4 wrong, 0 abstain.", ""]
    for a in ARMS:
        L += [f"## {a}", "", "| measure | " + " | ".join(OPS) + " |", "| --- " * (len(OPS) + 1) + "|"]
        for k in KEYS:
            L.append(f"| {k} | " + " | ".join(fmt(sc["arms"][a][op][k], 4) for op in OPS) + " |")
        L.append("")
    L += ["## Tests", "",
          tline("P1M_1 value against the strongest simpler rival: V*(intact) - V*(lesion, re-tuned), PFATE",
                sc["P1M_1"]),
          tline("P1M_2 value as used: own policy, intact - lesion, PFATE", sc["P1M_2"]),
          tline("P1M_3 learned value: dV_star, PFATE against PNOFATE", sc["P1M_3"]),
          tline("room: V*(lesion + supplied flag and K) - V*(lesion), PFATE", sc["room"]),
          tline("content: accuracy on conflicts, intact - lesion, PFATE", sc["content"]["dmg"]),
          tline("content: accuracy on undamaged trials, intact - lesion, PFATE", sc["content"]["none"])]
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
                "P1m discovery: Q-NECESSITY of the integrity variable, P1g's seeds (3200-3227)",
                "discovery")
        return
    if args.confirm:
        analyse(os.path.join(OUT, "confirm"), CONFIRM_SET, CONFIRM_W,
                "P1m: Q-NECESSITY of the integrity variable, P1i's seeds (3400-3427)", "confirm")
        return
    sys.exit("choose --discovery, --confirm or --score")


if __name__ == "__main__":
    main()
