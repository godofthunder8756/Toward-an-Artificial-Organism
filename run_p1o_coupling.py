"""P1o: is the integrity monitor coupled to self-maintenance only when computation is precarious?

Protocol: P1O_COUPLING_PROTOCOL.md. Analysis: trackc_swap/coupling.py. Evaluation only, on saved weights (3600).

    python run_p1o_coupling.py --discovery      # P1g's seeds 3200-3227 (discovery set, before the freeze)
    python run_p1o_coupling.py --confirm        # P1i's seeds 3400-3427 (after the freeze)
    python run_p1o_coupling.py --score p1o_coupling/confirm
"""
import argparse
import dataclasses
import json
import os
import platform
import sys
from multiprocessing import Pool

import torch

import run_p1g_graded as G
from run_p1_selfeval import one_sample
from run_p1h_evidence import relabel
from run_trackc_paid import PAY, WEAR
from run_trackc_paid2 import holm, pair_test
from run_trackc_probe import fmt, med, sha
from trackc_swap.coupling import collect_coupling
from trackc_swap.env import WorldConfig
from trackc_swap.selfmon import ARMS_M
from trackc_swap.train import TrainConfig

DISCOVERY_SET = list(range(3200, 3228))
CONFIRM_SET = list(range(3400, 3428))
DISCOVERY_W = "p1g_graded/weights"
CONFIRM_W = "p1i_calib/p1g_design/weights"
OUT = "p1o_coupling"
ARMS = ARMS_M
POINT = 3600
EVAL_EPISODES = 4          # twice the default: the foraging contrasts are small per trial
ROOM_MIN = 0.05            # validity: a damage event raises P(out of band) by at least this, PFATE, median
N_VALID = 20
SOURCES = G.SOURCES + ["trackc_swap/evidence.py", "trackc_swap/steerint.py", "trackc_swap/transfer.py",
                       "trackc_swap/necessity.py", "trackc_swap/coupling.py", "run_p1h_evidence.py",
                       "run_p1o_coupling.py", "P1O_COUPLING_PROTOCOL.md"]
KEYS = ("M_signed", "steer_signed", "M_conf", "M_conf_high", "M_none", "F_conflict", "F_same", "F_none", "M_nat", "steer", "induce", "rescue",
        "random_none", "steer_high", "room", "p_out_event", "p_out_all", "norm_d")


def analyse_seed(job):
    seed, wdir = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), dataclasses.replace(TrainConfig(), eval_episodes=EVAL_EPISODES)
    weights = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{POINT}.pt"), weights_only=False) for a in ARMS}
    return {"seed": seed, "arms": collect_coupling(seed, weights, wc, tc, PAY[1], G.BASE_F, ARMS)}


def measures(rec, arm):
    r = rec["arms"][arm]
    lo, hi, pu, rm = r["probe"]["low"], r["probe"]["high"], r["push"], r["room"]
    m = {"M_conf": lo["M_conf"], "M_conf_high": hi["M_conf"], "M_none": lo["M_none"], "F_conflict": lo["F_conflict"],
         "F_same": lo["F_same"], "F_none": lo["F_none"], "M_nat": r["natural"].get("M_nat"),
         "steer": pu.get("steer"), "induce": pu.get("induce"), "rescue": pu.get("rescue"),
         "random_none": pu.get("random_none"), "room": rm.get("room"), "p_out_event": rm.get("p_out_event"),
         "p_out_all": rm.get("p_out_all"), "norm_d": r.get("norm_d")}
    m["steer_high"] = r.get("push_high", {}).get("steer")
    dif = lambda a, b: None if a is None or b is None else float(a - b)
    m["M_signed"] = dif(m["M_conf"], m["M_conf_high"])
    m["steer_signed"] = dif(m["steer"], m["steer_high"])
    m["fitted"] = m["M_signed"] is not None and m["steer_signed"] is not None
    return m


def score(recs):
    per = {r["seed"]: {a: measures(r, a) for a in ARMS} for r in recs}
    one = lambda key, a, hi="PRESENT", lo="REVERSED": one_sample([per[x][a][key] for x in per], hi, lo)
    P = lambda key, a, b: [(per[x][a][key], per[x][b][key]) for x in per]
    ident = lambda v: v
    t1 = one("M_signed", "PFATE")
    t2 = pair_test(P("M_signed", "PFATE", "PYOKED"), ident, "FATE", "YOKED")
    t3 = one("steer_signed", "PFATE")
    adj = holm([t1["sign_p"], t2["sign_p"], t3["sign_p"]])
    t1 = relabel(t1, adj[0], "PRESENT", "REVERSED")
    t2 = relabel(t2, adj[1], "FATE_AHEAD", "YOKED_AHEAD")
    t3 = relabel(t3, adj[2], "PRESENT", "REVERSED")
    room = one("room", "PFATE")
    room_ok = room["label"] == "PRESENT" and (room["median"] or 0) >= ROOM_MIN
    n_fit = {a: sum(per[x][a]["fitted"] for x in per) for a in ARMS}
    valid = n_fit["PFATE"] >= N_VALID and n_fit["PYOKED"] >= N_VALID and room_ok
    arms = {a: {k: med(per[x][a][k] for x in per) for k in KEYS} for a in ARMS}
    sec = {"v1_P1O_1_M_conf_PFATE": one("M_conf", "PFATE"),
           "v1_P1O_2_M_conf_PFATE_vs_PYOKED": pair_test(P("M_conf", "PFATE", "PYOKED"), ident, "FATE", "YOKED"),
           "v1_P1O_3_steer_PFATE": one("steer", "PFATE"),
           "M_signed_PYOKED": one("M_signed", "PYOKED"), "M_signed_PNOFATE": one("M_signed", "PNOFATE"),
           "M_signed_PFATE_vs_PNOFATE": pair_test(P("M_signed", "PFATE", "PNOFATE"), ident, "FATE", "NOFATE"),
           "steer_signed_PFATE_vs_PYOKED": pair_test(P("steer_signed", "PFATE", "PYOKED"), ident, "FATE", "YOKED"),
           "steer_signed_PYOKED": one("steer_signed", "PYOKED"), "steer_signed_PNOFATE": one("steer_signed", "PNOFATE"),
           "steer_high_PFATE": one("steer_high", "PFATE"),
           "M_conf_PYOKED": one("M_conf", "PYOKED"), "M_conf_PNOFATE": one("M_conf", "PNOFATE"),
           "M_conf_PFATE_vs_PNOFATE": pair_test(P("M_conf", "PFATE", "PNOFATE"), ident, "FATE", "NOFATE"),
           "M_nat_PFATE": one("M_nat", "PFATE"), "M_nat_PYOKED": one("M_nat", "PYOKED"),
           "M_nat_PFATE_vs_PYOKED": pair_test(P("M_nat", "PFATE", "PYOKED"), ident, "FATE", "YOKED"),
           "steer_PFATE_vs_PYOKED": pair_test(P("steer", "PFATE", "PYOKED"), ident, "FATE", "YOKED"),
           "induce_PFATE": one("induce", "PFATE"), "rescue_PFATE": one("rescue", "PFATE"),
           "steer_PYOKED": one("steer", "PYOKED"), "steer_PNOFATE": one("steer", "PNOFATE"),
           "M_conf_high_PFATE": one("M_conf_high", "PFATE"), "M_none_PFATE": one("M_none", "PFATE"),
           "room_PYOKED": one("room", "PYOKED"),
           "room_PFATE_vs_PYOKED": pair_test(P("room", "PFATE", "PYOKED"), ident, "FATE", "YOKED")}
    sc = {"n_seeds": len(per), "valid": valid, "n_fitted": n_fit, "room": room, "room_ok": room_ok,
          "P1O_1": t1, "P1O_2": t2, "P1O_3": t3, "arms": arms, "secondary": sec, "per_seed": per}
    sc["overall"] = overall(sc)
    return sc


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    l1, l2, l3 = sc["P1O_1"]["label"], sc["P1O_2"]["label"], sc["P1O_3"]["label"]
    if "UNDETERMINED" in (l1, l2, l3):
        return "UNDETERMINED"
    if l1 != "PRESENT":
        return "NO_COUPLING"
    if l2 != "FATE_AHEAD":
        return "COUPLED_NOT_PRECARITY"
    return "PRECARITY_COUPLES_MONITOR" if l3 == "PRESENT" else "COUPLED_NOT_CAUSAL"


def tline(name, t):
    if "positive" in t:
        return (f"- {name}: {t['positive']}/{t['n']} > 0 (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)};"
                f" median {fmt(t['median'], 4)}) {t['label']}")
    return (f"- {name}: {t['first_ahead']}/{t['n']} (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)}; "
            f"{fmt(t['first_median'], 4)} against {fmt(t['second_median'], 4)}) {t['label']}")


def report(sc, title):
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}.** Valid: {sc['valid']} (fitted seeds {sc['n_fitted']}, needed >= {N_VALID} for "
         f"PFATE and PYOKED; room, PFATE median >= {ROOM_MIN}: {sc['room_ok']}). Seeds: {sc['n_seeds']}. Point: "
         f"{POINT}. Foraging drive f per delay step in [-1, 1]; F = mean over delay steps 2-8; low side: true "
         f"energy at delay step 1 below 0.5; signed = low side - high side.", "",
         "| measure | " + " | ".join(ARMS) + " |", "| --- " * (len(ARMS) + 1) + "|"]
    for k in KEYS:
        L.append(f"| {k} | " + " | ".join(fmt(sc["arms"][a][k], 4) for a in ARMS) + " |")
    L += ["", "## Tests", "",
          tline("P1O_1 body-appropriate coupling: M_signed = M_conf(low) - M_conf(high), PFATE", sc["P1O_1"]),
          tline("P1O_2 precarity: M_signed, PFATE against PYOKED", sc["P1O_2"]),
          tline("P1O_3 cause: steer_signed = steer(low) - steer(high), PFATE", sc["P1O_3"]),
          tline("room: P(out of band | event) - P(out | no event) at the shown reading, PFATE", sc["room"])]
    for k, t in sc["secondary"].items():
        L.append(tline(k, t))
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
    meta = {"stage": stage, "title": title, "seeds": seeds, "point": POINT, "eval_episodes": EVAL_EPISODES,
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
                "P1o discovery: the integrity monitor and self-maintenance, P1g's seeds (3200-3227)", "discovery")
        return
    if args.confirm:
        analyse(os.path.join(OUT, "confirm"), CONFIRM_SET, CONFIRM_W,
                "P1o: the integrity monitor and self-maintenance, P1i's seeds (3400-3427)", "confirm")
        return
    sys.exit("choose --discovery, --confirm or --score")


if __name__ == "__main__":
    main()
