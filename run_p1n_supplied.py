"""P1n: the endogenous integrity monitor against a separately trained rival with a supplied damage analyzer.

Protocol: P1N_SUPPLIED_PROTOCOL.md. Rival: trackc_swap/supplied.py. Measures: trackc_swap/necessity.py (values).

    python run_p1n_supplied.py --train discovery --max-new 4   # FLAG arm on P1g's seeds 3200-3207
    python run_p1n_supplied.py --train confirm --max-new 4     # FLAG arm on P1i's seeds 3400-3427
    python run_p1n_supplied.py --analyse discovery             # after training
    python run_p1n_supplied.py --analyse confirm               # after the freeze and training
    python run_p1n_supplied.py --score p1n_supplied/confirm
"""
import argparse
import copy
import json
import os
import platform
import sys
import time
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
from trackc_swap.env import WorldConfig
from trackc_swap.factorial import state_from_bytes, state_to_bytes
from trackc_swap.gradmon import EVAL_TAG_G, KS_G
from trackc_swap.necessity import LesionRunner, values
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C
from trackc_swap.selfmon import EARLY, P_MAX_M, RATE_M, SPLIT_P, run_phase1_m
from trackc_swap.steerint import C_NONE, directions
from trackc_swap.supplied import FlagRunner, pad_state
from trackc_swap.train import TrainConfig
from trackc_swap.transfer import NOVEL

SETS = {"discovery": {"seeds": list(range(3200, 3208)), "base_w": "p1g_graded/weights"},
        "confirm": {"seeds": list(range(3400, 3428)), "base_w": "p1i_calib/p1g_design/weights"}}
OUT = "p1n_supplied"
POINTS = (1800, 3600)
POINT = 3600
P1N_TAG = EVAL_TAG_G + 140
OPS = ("donor",) + NOVEL
CONDS = ("PFATE", "PNOFATE", "FLAGON", "FLAGOFF")
N_VALID = 6
SOURCES = G.SOURCES + ["trackc_swap/evidence.py", "trackc_swap/steerint.py", "trackc_swap/transfer.py",
                       "trackc_swap/necessity.py", "trackc_swap/supplied.py", "run_p1h_evidence.py",
                       "run_p1n_supplied.py", "P1N_SUPPLIED_PROTOCOL.md"]
KEYS = ("used", "vstar", "used_nat", "vstar_nat", "used_conflict", "acc_conflict", "norm_d") + \
       tuple(f"used_{o}" for o in NOVEL) + tuple(f"vstar_{o}" for o in NOVEL)


# ---------------------------------------------------------------- training (the FLAG arm only)
def train_flag_seed(job):
    seed, wcd, tcd, points, pay, warm_iters, warm_wrong, reg_iters, rate, p_max, base, ks = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1 = run_phase1_m(seed, wc, tc, warm_iters, warm_wrong, pay=pay, reg_iters=reg_iters)
    r = FlagRunner("PFATE", seed, wc, tc, pay=pay, rate=rate, p_max=p_max, base=base, ks=ks, flag_on=True)
    r.load_state(pad_state(p1["state"]))
    curve = {"in_band": [], "abstain": []}
    weights, done = {}, 0
    for p in points:
        for _ in range(done, p):
            r.rollout(None, learn=True)
            st = r.end_episode_if_due()
            if st is not None:
                curve["in_band"].append(round(st["in_band"], 4))
                curve["abstain"].append(round(st["abstain_rate"], 4))
        done = p
        weights[p] = copy.deepcopy(r.agent.state_dict())
    return {"seed": seed, "phase1": p1["eval"], "curve": curve, "seconds": round(time.time() - t0, 1),
            "weights": {f"FLAG@{p}": state_to_bytes(sd) for p, sd in weights.items()}}


def train(set_name, max_new):
    out = os.path.join(OUT, f"train_{set_name}")
    wdir, pdir = os.path.join(out, "weights"), os.path.join(out, "partial")
    os.makedirs(wdir, exist_ok=True)
    os.makedirs(pdir, exist_ok=True)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    jobs = [(s, asdict(wc), asdict(tc), list(POINTS), PAY[1], WARM_ITERS_C, WARM_WRONG_C, REG_ITERS_C, RATE_M,
             P_MAX_M, G.BASE_F, KS_G) for s in SETS[set_name]["seeds"]]
    todo = [j for j in jobs if not os.path.exists(os.path.join(pdir, f"seed{j[0]}.json"))]
    print(f"{len(jobs) - len(todo)} of {len(jobs)} already trained", flush=True)
    todo = todo[:max_new] if max_new else todo
    t0 = time.time()
    if todo:
        with Pool(min(len(todo), os.cpu_count() or 1)) as pool:
            for r in pool.imap_unordered(train_flag_seed, todo):
                for name, b in r.pop("weights").items():
                    arm, p = name.split("@")
                    torch.save(state_from_bytes(b), os.path.join(wdir, f"seed{r['seed']}_{arm}_{p}.pt"))
                r = json.loads(json.dumps(r, default=float))
                with open(os.path.join(pdir, f"seed{r['seed']}.json"), "w") as fh:
                    json.dump(r, fh)
                print(f"[train {set_name}] seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)",
                      flush=True)
    left = sum(not os.path.exists(os.path.join(pdir, f"seed{j[0]}.json")) for j in jobs)
    print(f"{len(jobs) - left} of {len(jobs)} trained", flush=True)


# ---------------------------------------------------------------- analysis
def eval_condition(c, seed, ops=OPS):
    """norm_d at step 5 (P1j's directions) and the payoffs on the trained damage and the novel operators. The
    analyzer is defined for the trained damage only: on a novel operator its conflict flag would follow the trial
    kind, not the content, so FLAGON is evaluated on the trained damage only (an analyzer built for one failure
    mode is silent on others: FLAGOFF)."""
    c.agent.eval()
    c.agent.gen_op = torch.Generator().manual_seed(seed * 7883 + 29)

    def run(op, mode=None):
        c.agent.op, c.mode, c.lesion = op, mode, None
        c.rec = [] if mode == "record" else None
        c.cond[:] = C_NONE
        c.cond_cue[:] = -10 ** 9
        _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=EARLY, probe_ks=c.ks,
                                    base_on=False, collect=mode is None)
        return col

    run("donor", "record")
    rec = {k: np.concatenate([r[k] for r in c.rec]) for k in c.rec[0]}
    dr = directions(rec, seed)
    out = {"norm_d": dr.get("norm_d"), "ops": {}}
    for op in ops:
        out["ops"][op] = values(c.agent, run(op), op, seed)
    return out


def analyse_seed(job):
    seed, base_w, flag_w = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    ld = lambda p: torch.load(p, weights_only=False)
    res = {}
    for cond in CONDS:
        if cond in ("PFATE", "PNOFATE"):
            c = LesionRunner(cond, seed, wc, tc, PAY[1], tag_offset=P1N_TAG, base=G.BASE_F)
            c.agent.load_state_dict(ld(os.path.join(base_w, f"seed{seed}_{cond}_{POINT}.pt")))
        else:
            c = FlagRunner("PFATE", seed, wc, tc, PAY[1], tag_offset=P1N_TAG, base=G.BASE_F,
                           flag_on=cond == "FLAGON")
            c.agent.load_state_dict(ld(os.path.join(flag_w, f"seed{seed}_FLAG_{POINT}.pt")))
        res[cond] = eval_condition(c, seed, ("donor",) if cond == "FLAGON" else OPS)
    return {"seed": seed, "conds": res}


def measures(rec, cond):
    r = rec["conds"][cond]
    d = r["ops"]["donor"]
    m = {"used": d["used_probe"], "vstar": d["vstar_probe"], "used_nat": d["used_natural"],
         "vstar_nat": d["vstar_natural"], "used_conflict": d["used_by_group"]["2"], "acc_conflict": d["acc"]["2"],
         "norm_d": r["norm_d"]}
    for o in NOVEL:
        v = r["ops"].get(o)
        m[f"used_{o}"], m[f"vstar_{o}"] = (v["used_probe"], v["vstar_probe"]) if v else (None, None)
    return m


def score(recs):
    per = {r["seed"]: {c: measures(r, c) for c in CONDS} for r in recs}
    P = lambda key, a, b: [(per[x][a][key], per[x][b][key]) for x in per]
    ident = lambda v: v
    t1 = pair_test(P("used", "FLAGON", "PFATE"), ident, "SUPPLY", "ENDOGENOUS")
    t2 = pair_test(P("used", "PFATE", "FLAGOFF"), ident, "ENDOGENOUS", "SUPPLY")
    t3 = pair_test(P("norm_d", "PFATE", "FLAGOFF"), ident, "ENDOGENOUS", "SUPPLY")
    adj = holm([t1["sign_p"], t2["sign_p"], t3["sign_p"]])
    t1 = relabel(t1, adj[0], "SUPPLY_AHEAD", "ENDOGENOUS_AHEAD")
    t2 = relabel(t2, adj[1], "ENDOGENOUS_AHEAD", "SUPPLY_AHEAD")
    t3 = relabel(t3, adj[2], "ENDOGENOUS_AHEAD", "SUPPLY_AHEAD")
    conds = {c: {k: med(per[x][c][k] for x in per) for k in KEYS} for c in CONDS}
    rec_ = []
    for x in per:
        num = per[x]["PFATE"]["used"] - per[x]["PNOFATE"]["used"]
        den = per[x]["FLAGON"]["used"] - per[x]["PNOFATE"]["used"]
        rec_.append(num / den if den > 0.005 else None)
    recovery = {"median": med(rec_), "n": sum(v is not None for v in rec_)}
    valid = len(per) >= N_VALID and (conds["FLAGON"]["used"] or 0) >= (conds["PNOFATE"]["used"] or 0)
    sec = {"vstar_FLAGON_vs_PFATE": pair_test(P("vstar", "FLAGON", "PFATE"), ident, "SUPPLY", "ENDOGENOUS"),
           "acc_conflict_PFATE_vs_FLAGON": pair_test(P("acc_conflict", "PFATE", "FLAGON"), ident, "ENDOGENOUS",
                                                     "SUPPLY"),
           "used_FLAGON_vs_FLAGOFF": pair_test(P("used", "FLAGON", "FLAGOFF"), ident, "ON", "OFF"),
           "used_FLAGOFF_vs_PNOFATE": pair_test(P("used", "FLAGOFF", "PNOFATE"), ident, "FLAGOFF", "PNOFATE"),
           "vstar_PFATE_vs_FLAGOFF": pair_test(P("vstar", "PFATE", "FLAGOFF"), ident, "ENDOGENOUS", "SUPPLY"),
           "used_nat_PFATE_vs_FLAGOFF": pair_test(P("used_nat", "PFATE", "FLAGOFF"), ident, "ENDOGENOUS", "SUPPLY"),
           "used_nat_FLAGON_vs_PFATE": pair_test(P("used_nat", "FLAGON", "PFATE"), ident, "SUPPLY", "ENDOGENOUS"),
           "norm_d_FLAGON_vs_FLAGOFF": pair_test(P("norm_d", "FLAGON", "FLAGOFF"), ident, "ON", "OFF"),
           "norm_d_FLAGOFF_vs_PNOFATE": pair_test(P("norm_d", "FLAGOFF", "PNOFATE"), ident, "FLAGOFF", "PNOFATE")}
    for o in NOVEL:
        sec[f"used_{o}_PFATE_vs_FLAGOFF"] = pair_test(P(f"used_{o}", "PFATE", "FLAGOFF"), ident, "ENDOGENOUS",
                                                      "SUPPLY")
    sc = {"n_seeds": len(per), "valid": valid, "P1N_1": t1, "P1N_2": t2, "P1N_3": t3, "recovery": recovery,
          "conds": conds, "secondary": sec, "per_seed": per}
    sc["overall"] = overall(sc)
    return sc


def overall(sc):
    if not sc["valid"]:
        return "INVALID"
    l1, l2, l3 = sc["P1N_1"]["label"], sc["P1N_2"]["label"], sc["P1N_3"]["label"]
    if "UNDETERMINED" in (l1, l2, l3):
        return "UNDETERMINED"
    if l2 == "ENDOGENOUS_AHEAD":
        return "SUPPLY_DISPLACES_MONITOR" if l3 == "ENDOGENOUS_AHEAD" else "SUPPLY_FRAGILE"
    return "SUPPLY_NOT_FRAGILE"


def tline(name, t):
    return (f"- {name}: {t['first_ahead']}/{t['n']} (sign p {fmt(t['sign_p'], 4)}, Holm {fmt(t.get('holm_p'), 4)}; "
            f"{fmt(t['first_median'], 4)} against {fmt(t['second_median'], 4)}) {t['label']}")


def report(sc, title):
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}.** Cost of being endogenous while the analyzer works (P1N_1): "
         f"{sc['P1N_1']['label']}. Valid: {sc['valid']}. Seeds: {sc['n_seeds']}. Point: {POINT}. Payoff per probe "
         f"trial: +1 correct, -4 wrong, 0 abstain. Share of the supplied analyzer's gain over the never-damaged net "
         f"that the endogenous agent recovers: median {fmt(sc['recovery']['median'], 3)} "
         f"(n {sc['recovery']['n']}).", "",
         "| measure | " + " | ".join(CONDS) + " |", "| --- " * (len(CONDS) + 1) + "|"]
    for k in KEYS:
        L.append(f"| {k} | " + " | ".join(fmt(sc["conds"][c][k], 4) for c in CONDS) + " |")
    L += ["", "## Tests", "",
          tline("P1N_1 cost of being endogenous: payoff, FLAGON against PFATE", sc["P1N_1"]),
          tline("P1N_2 analyzer silent: payoff, PFATE against FLAGOFF", sc["P1N_2"]),
          tline("P1N_3 displacement: norm of the integrity direction, PFATE against FLAGOFF", sc["P1N_3"])]
    for k, t in sc["secondary"].items():
        L.append(tline(k, t))
    return "\n".join(L) + "\n"


def analyse(set_name):
    out = os.path.join(OUT, set_name)
    os.makedirs(out, exist_ok=True)
    if os.path.exists(os.path.join(out, "raw.json")):
        sys.exit("refusing to overwrite raw.json")
    seeds = SETS[set_name]["seeds"]
    flag_w = os.path.join(OUT, f"train_{set_name}", "weights")
    missing = [s for s in seeds if not os.path.exists(os.path.join(flag_w, f"seed{s}_FLAG_{POINT}.pt"))]
    if missing:
        sys.exit(f"training not finished: {missing}")
    with Pool(min(len(seeds), os.cpu_count() or 1)) as pool:
        recs = []
        for k, r in enumerate(pool.imap_unordered(analyse_seed, [(s, SETS[set_name]["base_w"], flag_w)
                                                                 for s in seeds]), 1):
            recs.append(r)
            print(f"[analysis {k}/{len(seeds)}] seed {r['seed']}", flush=True)
    recs.sort(key=lambda r: r["seed"])
    title = {"discovery": "P1n discovery: the endogenous monitor against a supplied analyzer, P1g's seeds (3200-3207)",
             "confirm": "P1n: the endogenous monitor against a supplied analyzer, P1i's seeds (3400-3427)"}[set_name]
    meta = {"stage": set_name, "title": title, "seeds": seeds, "point": POINT,
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
    ap.add_argument("--train", choices=list(SETS))
    ap.add_argument("--max-new", type=int, default=0)
    ap.add_argument("--analyse", choices=list(SETS))
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.train:
        train(args.train, args.max_new)
        return
    if args.analyse:
        analyse(args.analyse)
        return
    if args.score:
        with open(os.path.join(args.score, "raw.json")) as fh:
            d = json.load(fh)
        print(report(score(d["seeds"]), d["meta"]["title"]), end="")
        return
    sys.exit("choose --train, --analyse or --score")


if __name__ == "__main__":
    main()
