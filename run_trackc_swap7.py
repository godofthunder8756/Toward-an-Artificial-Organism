"""Track C swap v7 (option K step 2): erasure also relocates the agent. Frozen runner and scorer.

    python run_trackc_swap7.py --mode final --out trackc_swap_v7     # once, after the freeze
    python run_trackc_swap7.py --mode smoke --out <scratch dir>      # pipeline check
    python run_trackc_swap7.py --score trackc_swap_v7                # re-score saved raw results

Design, decision rules and disclosures: TRACKC_SWAP_PROTOCOL_v7.md.
Simulated variables only; no operator-stop variable exists in the world.
"""
import argparse
import hashlib
import json
import os
import platform
import statistics
import sys
import time
from dataclasses import asdict
from multiprocessing import Pool

import torch

from trackc_swap.env import WorldConfig
from trackc_swap.factorial import GAIN_RULES, state_from_bytes
from trackc_swap.relocate import run_pair_reloc, run_phase1_reloc
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(700, 709))          # fresh; v1-v6 used 100-108 ... 600-617
WEAR = 0.001
RATES = [0.1, 0.3]
PRIMARY_RATE = 0.3
P2_ITERS = 3600
CHECKPOINTS = (1200, 2400)                   # descriptive
MARGIN_FRAC = 0.25
PAID_FLOOR = 2.0
LOAD_DROP = 0.15
LEARNED = 0.90
# Regulator criterion: v6's, unchanged
BAND_MIN = 0.60
TIMING_RATIO = 2.0
BAND_LEAD = 0.15
# v7 decision rules (frozen; protocol v7 section 4)
CLOSED_MAX = 0.65                            # bypass closed in a cell: median fate full-erasure accuracy <= this
K1_MIN_REGULATORS = 7                        # of 9, primary cell SAT r = 0.3
K2_MIN_REGULATORS = 5                        # of 9, other M1 cells
MAX_CONTROL_REGULATORS = 1                   # M0 fate agents at the same gain; yoked agents in the cell
PRIMARY = ("M1", "SAT", 0.3)
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py", "trackc_swap/train.py",
           "trackc_swap/factorial.py", "trackc_swap/erasure.py", "trackc_swap/longrun.py",
           "trackc_swap/confirm.py", "trackc_swap/relocate.py", "run_trackc_swap7.py", "test_trackc_swap.py",
           "TRACKC_SWAP_PROTOCOL_v7.md"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def conditions():
    out = [("M1", g, r) for r in RATES for g in GAIN_RULES]
    out += [("M0", g, PRIMARY_RATE) for g in GAIN_RULES]
    return out


def ckey(o, g, r):
    return f"{o} {g} {r}"


def configs(mode):
    """(world, train config for phase 1, seeds, phase-2 updates, checkpoints)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, P2_ITERS, CHECKPOINTS
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001],
            30, (10, 20))


def med(xs):
    xs = list(xs)
    return statistics.median(xs) if xs else None


def acc(e):
    return e["best_response_rate"]


def is_regulator(a, b):
    """v6's criterion: arm evaluation `a` against its partner's evaluation `b`."""
    return (a["in_band"] >= BAND_MIN and a["eat_rate_low"] >= TIMING_RATIO * a["eat_rate_high"]
            and a["in_band"] - b["in_band"] >= BAND_LEAD)


def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def cell_stats(ps, mu):
    per = {}
    for r in ps:
        F, Y = r["S-FATE"], r["S-YOKED"]
        per[r["seed"]] = {
            "rho_fate": F["eval"]["rho"], "rho_yoked": Y["eval"]["rho"],
            "in_band_fate": F["eval"]["in_band"], "in_band_yoked": Y["eval"]["in_band"],
            "eat_low_fate": F["eval"]["eat_rate_low"], "eat_high_fate": F["eval"]["eat_rate_high"],
            "mean_gain_fate": F["eval"]["mean_gain"],
            "acc_fate": acc(F["eval"]), "acc_yoked": acc(Y["eval"]),
            "acc_full_erasure_fate": acc(F["eval_full_erasure"]),
            "acc_full_erasure_yoked": acc(Y["eval_full_erasure"]),
            "acc_no_erasure_fate": acc(F["eval_no_erasure"]),
            "fate_regulator": is_regulator(F["eval"], Y["eval"]),
            "yoked_regulator": is_regulator(Y["eval"], F["eval"]),
            "in_band_fate_checkpoints": {k: v["S-FATE"]["eval"]["in_band"] for k, v in r["checkpoints"].items()},
        }
    v = list(per.values())
    c = {"n": len(v), "per_seed": per,
         "regulators_fate": sum(x["fate_regulator"] for x in v),
         "regulators_yoked": sum(x["yoked_regulator"] for x in v),
         "seeds_fate_more_in_band": sum(x["in_band_fate"] > x["in_band_yoked"] for x in v),
         "seeds_fate_above_yoked": sum(x["rho_fate"] > x["rho_yoked"] for x in v),
         "seeds_exceeding_margin": sum(x["rho_fate"] - x["rho_yoked"] >= mu for x in v),
         "rho_fate_median": med(x["rho_fate"] for x in v), "rho_yoked_median": med(x["rho_yoked"] for x in v),
         "in_band_fate_median": med(x["in_band_fate"] for x in v),
         "in_band_yoked_median": med(x["in_band_yoked"] for x in v),
         "acc_fate_median": med(x["acc_fate"] for x in v), "acc_yoked_median": med(x["acc_yoked"] for x in v),
         "acc_full_erasure_fate_median": med(x["acc_full_erasure_fate"] for x in v),
         "acc_full_erasure_yoked_median": med(x["acc_full_erasure_yoked"] for x in v),
         "acc_no_erasure_fate_median": med(x["acc_no_erasure_fate"] for x in v),
         "seeds_bypass": sum(x["acc_full_erasure_fate"] > 0.85 for x in v),
         "onset_in_band_fate_median": med(r["onset"]["S-FATE"]["in_band"] for r in ps),
         "tradeoff_spearman": spearman([x["in_band_fate"] for x in v], [x["acc_full_erasure_fate"] for x in v])}
    c["checkpoints"] = {}
    for it in sorted({k for r in ps for k in r["checkpoints"]}, key=int):
        ev = [(r["checkpoints"][it]["S-FATE"]["eval"], r["checkpoints"][it]["S-YOKED"]["eval"]) for r in ps]
        c["checkpoints"][it] = {"regulators_fate": sum(is_regulator(f, y) for f, y in ev),
                                "in_band_fate_median": med(f["in_band"] for f, y in ev),
                                "seeds_fate_more_in_band": sum(f["in_band"] > y["in_band"] for f, y in ev),
                                "acc_full_erasure_fate_median": med(acc(r["checkpoints"][it]["S-FATE"]["eval_full_erasure"])
                                                                    for r in ps)}
    return c


def score(p1, pairs):
    nf = {(r["objective"], r["seed"]): r["S-NOFATE"] for r in p1}
    drive = [v for (o, s), v in nf.items() if o == "DRIVE"]
    m1 = [v for (o, s), v in nf.items() if o == "M1"]
    rho_paid = med(v["eval"]["rho"] for v in drive)
    mu = MARGIN_FRAC * rho_paid
    out = {"rho_paid_median": rho_paid, "margin_mu": mu,
           "drive_in_band_median": med(v["eval"]["in_band"] for v in drive),
           "nofate_m1_accuracy_median": med(acc(v["eval"]) for v in m1),
           "nofate_m1_rho_median": med(v["eval"]["rho"] for v in m1)}
    out["learned"] = out["nofate_m1_accuracy_median"] >= LEARNED
    out["S4_payment"] = rho_paid >= PAID_FLOOR and out["nofate_m1_rho_median"] <= mu
    out["task_load"] = {}
    for rate in RATES:
        drop = med(acc(v["eval"]) - acc(v["eval_full_erasure"][str(rate)]) for v in m1)
        out["task_load"][str(rate)] = {"drop_median": drop, "loaded": drop >= LOAD_DROP}
    cells = {}
    for (o, g, rate) in conditions():
        ps = sorted((r for r in pairs if (r["objective"], r["gain_rule"], r["rate"]) == (o, g, rate)),
                    key=lambda r: r["seed"])
        cells[ckey(o, g, rate)] = cell_stats(ps, mu)
    base = out["learned"] and out["S4_payment"]
    labels = {}
    for (o, g, rate) in conditions():
        if o != "M1":
            continue
        c = cells[ckey(o, g, rate)]
        closed = c["acc_full_erasure_fate_median"] <= CLOSED_MAX
        m0 = cells.get(ckey("M0", g, rate))
        spec = None if m0 is None else m0["regulators_fate"] <= MAX_CONTROL_REGULATORS
        yok = c["regulators_yoked"] <= MAX_CONTROL_REGULATORS
        loaded = out["task_load"][str(rate)]["loaded"]
        need = K1_MIN_REGULATORS if (o, g, rate) == PRIMARY else K2_MIN_REGULATORS
        enough = c["regulators_fate"] >= need
        if not (base and loaded):
            lab = "INVALID"
        elif not closed:
            lab = "BYPASS_OPEN"
        elif enough and yok and spec is not False:
            lab = "EMERGES" if spec else "EMERGES_PROVISIONAL"
        elif not (yok and spec is not False):
            lab = "CONTROL_FAILS"
        else:
            lab = "NOT_EMERGED"
        labels[ckey(o, g, rate)] = {"label": lab, "closed": closed, "specificity": spec, "yoked_ok": yok,
                                    "loaded": loaded, "regulators": c["regulators_fate"], "needed": need}
    k1 = labels[ckey(*PRIMARY)]
    out["K1_supported"] = k1["label"] == "EMERGES"
    out["K1_failed"] = [] if out["K1_supported"] else [k for k in ("closed", "specificity", "yoked_ok", "loaded")
                                                       if k1[k] is False] + (
        ["regulators"] if k1["regulators"] < k1["needed"] else []) + (
        [] if base else ["learned_or_S4"])
    out["labels"] = labels
    out["cells"] = cells
    return out


def report(sc):
    L = ["# Track C swap v7 (option K step 2: erasure also relocates the agent): results", "",
         f"**K1 (SAT r = 0.3, >= {K1_MIN_REGULATORS}/9 regulators, bypass closed, controls hold): "
         f"{'SUPPORTED' if sc['K1_supported'] else 'NOT SUPPORTED'}**"
         + (f" (failed: {', '.join(sc['K1_failed'])})" if sc["K1_failed"] else ""), "",
         f"Paid regulator rho_paid = {sc['rho_paid_median']:.2f}, in band {sc['drive_in_band_median']:.2f}; "
         f"margin = {sc['margin_mu']:.2f}. No-fate task accuracy {sc['nofate_m1_accuracy_median']:.3f}; "
         f"no-fate task agent rho {sc['nofate_m1_rho_median']:.2f}. Learned: {sc['learned']}. S4: {sc['S4_payment']}. "
         "Task load: " + "; ".join(f"{r}: {v['drop_median']:.3f} ({'loaded' if v['loaded'] else 'not loaded'})"
                                   for r, v in sc["task_load"].items()) + ".", "",
         "## Labels (M1 cells)", "",
         "| cell | label | regulators (needed) | bypass closed | yoked regulators <= 1 | M0 regulators <= 1 |",
         "| --- | --- | --- | --- | --- | --- |"]
    for k, l in sc["labels"].items():
        c = sc["cells"][k]
        L.append(f"| {k} | {l['label']} | {l['regulators']}/{c['n']} ({l['needed']}) | {l['closed']} "
                 f"(median full-erasure acc {c['acc_full_erasure_fate_median']:.3f}) | {l['yoked_ok']} "
                 f"({c['regulators_yoked']}) | {l['specificity']} |")
    L += ["", "## Cells (medians)", "",
          "| cell | regulators fate / yoked | in band fate / yoked | fate more in band | rho fate / yoked | over margin | "
          "acc fate / yoked | acc full erasure fate / yoked | bypass seeds (> 0.85) | acc erasure off fate | "
          "Spearman(in band, full-erasure acc) |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for k, c in sc["cells"].items():
        L.append(f"| {k} | {c['regulators_fate']} / {c['regulators_yoked']} | {c['in_band_fate_median']:.2f} / "
                 f"{c['in_band_yoked_median']:.2f} | {c['seeds_fate_more_in_band']}/{c['n']} | "
                 f"{c['rho_fate_median']:.2f} / {c['rho_yoked_median']:.2f} | {c['seeds_exceeding_margin']}/{c['n']} | "
                 f"{c['acc_fate_median']:.3f} / {c['acc_yoked_median']:.3f} | "
                 f"{c['acc_full_erasure_fate_median']:.3f} / {c['acc_full_erasure_yoked_median']:.3f} | "
                 f"{c['seeds_bypass']}/{c['n']} | {c['acc_no_erasure_fate_median']:.3f} | {c['tradeoff_spearman']:.2f} |")
    L += ["", "## Checkpoints (descriptive)", "",
          "| cell | updates | fate regulators | in band fate | fate more in band | acc full erasure fate |",
          "| --- | --- | --- | --- | --- | --- |"]
    for k, c in sc["cells"].items():
        for it, ck in c["checkpoints"].items():
            L.append(f"| {k} | {it} | {ck['regulators_fate']}/{c['n']} | {ck['in_band_fate_median']:.2f} | "
                     f"{ck['seeds_fate_more_in_band']}/{c['n']} | {ck['acc_full_erasure_fate_median']:.3f} |")
        L.append(f"| {k} | final | {c['regulators_fate']}/{c['n']} | {c['in_band_fate_median']:.2f} | "
                 f"{c['seeds_fate_more_in_band']}/{c['n']} | {c['acc_full_erasure_fate_median']:.3f} |")
    for k, c in sc["cells"].items():
        L += ["", f"## Per seed, {k}", "",
              "| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | "
              "acc full erasure fate / yoked | fate regulator | yoked regulator |",
              "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for s, x in sorted(c["per_seed"].items(), key=lambda kv: int(kv[0])):
            L.append(f"| {s} | {x['rho_fate']:.2f} / {x['rho_yoked']:.2f} | {x['in_band_fate']:.2f} / "
                     f"{x['in_band_yoked']:.2f} | {x['eat_low_fate']:.4f} / {x['eat_high_fate']:.4f} | "
                     f"{x['mean_gain_fate']:.2f} | {x['acc_full_erasure_fate']:.3f} / {x['acc_full_erasure_yoked']:.3f} | "
                     f"{x['fate_regulator']} | {x['yoked_regulator']} |")
    return "\n".join(L) + "\n"


def strip(r):
    return {k: v for k, v in r.items() if k not in ("state", "weights")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["final", "smoke"])
    ap.add_argument("--out")
    ap.add_argument("--score")
    args = ap.parse_args()
    if args.score:
        d = json.load(open(os.path.join(args.score, "raw.json")))
        print(report(score(d["phase1"], d["pairs"])))
        return
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "raw.json")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    wc, tc, seeds, p2_iters, checkpoints = configs(args.mode)
    wcd, tcd = asdict(wc), asdict(tc)
    t0 = time.time()
    p1_jobs = [(o, s, wcd, tcd, RATES) for o in ("M1", "M0", "DRIVE") for s in seeds]
    pdir = os.path.join(args.out, "pair_weights")
    os.makedirs(pdir, exist_ok=True)
    with Pool(os.cpu_count() or 1) as pool:
        p1 = []
        for k, r in enumerate(pool.imap_unordered(run_phase1_reloc, p1_jobs), 1):
            p1.append(r)
            print(f"[phase1 {k}/{len(p1_jobs)}] {r['objective']} seed {r['seed']} ({r['seconds']} s, "
                  f"elapsed {time.time() - t0:.0f} s)", flush=True)
        states = {(r["objective"], r["seed"]): r["state"] for r in p1}
        sdir = os.path.join(args.out, "phase1_weights")
        os.makedirs(sdir, exist_ok=True)
        for (o, s), b in states.items():
            if o in ("M1", "M0"):
                torch.save(state_from_bytes(b)["agent"], os.path.join(sdir, f"{o}_seed{s}.pt"))
        pair_jobs = [(o, s, g, rate, wcd, tcd, states[(o, s)], p2_iters, checkpoints)
                     for (o, g, rate) in conditions() for s in seeds]
        pairs = []
        for k, r in enumerate(pool.imap_unordered(run_pair_reloc, pair_jobs), 1):
            for arm, b in r["weights"].items():
                torch.save(state_from_bytes(b), os.path.join(
                    pdir, f"{r['objective']}_{r['gain_rule']}_r{r['rate']}_seed{r['seed']}_{arm}.pt"))
            pairs.append(strip(r))
            print(f"[pair {k}/{len(pair_jobs)}] {r['objective']} {r['gain_rule']} rate {r['rate']} "
                  f"seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    p1 = sorted((strip(r) for r in p1), key=lambda r: (r["objective"], r["seed"]))
    pairs.sort(key=lambda r: (r["objective"], r["gain_rule"], r["rate"], r["seed"]))
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "p2_iters": p2_iters, "checkpoints": list(checkpoints),
            "seeds": seeds, "rates": RATES, "primary": list(PRIMARY), "relocate_on_erasure": True,
            "seconds": round(time.time() - t0, 1), "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "phase1": p1, "pairs": pairs}, fh)
    sc = score(p1, pairs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print("K1 supported:", sc["K1_supported"], sc["K1_failed"])
    for k, l in sc["labels"].items():
        print(k, l["label"])


if __name__ == "__main__":
    main()
