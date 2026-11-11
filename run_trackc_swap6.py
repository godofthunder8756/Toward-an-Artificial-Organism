"""Track C swap v6 (option J): confirmation of v5's SAT r = 0.3 regulators. Frozen runner and scorer.

    python run_trackc_swap6.py --mode final --out trackc_swap_v6     # once, after the freeze
    python run_trackc_swap6.py --mode smoke --out <scratch dir>      # pipeline check
    python run_trackc_swap6.py --score trackc_swap_v6                # re-score saved raw results

Design, decision rules and disclosures: TRACKC_SWAP_PROTOCOL_v6.md.
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

from trackc_swap.confirm import run_pair_saved
from trackc_swap.env import WorldConfig
from trackc_swap.erasure import run_phase1
from trackc_swap.factorial import state_from_bytes
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(600, 618))          # 18 fresh seeds; v1-v5 used 100-108 ... 500-508
WEAR = 0.001
GAIN = "SAT"
RATE = 0.3
P2_ITERS = 3600
CHECKPOINTS = (1200, 2400)                   # descriptive, as in v5
MARGIN_FRAC = 0.25
PAID_FLOOR = 2.0
LOAD_DROP = 0.15
LEARNED = 0.90
# Per-agent regulator criterion (frozen; protocol v6 section 4)
BAND_MIN = 0.60                              # in band at least this fraction of the evaluation
TIMING_RATIO = 2.0                           # eats at least twice as often when E < 0.5 as when E >= 0.5
BAND_LEAD = 0.15                             # in band at least this much more than its partner
# Confirmation thresholds (frozen)
MIN_REGULATORS = 6                           # of 18 M1 fate agents
MIN_BAND_SIGN = 13                           # of 18 M1 pairs fate more in band (one-sided sign test p = 0.048)
MAX_CONTROL_REGULATORS = 1                   # M0 fate agents; M1 yoked agents against their fate partners
TRADEOFF_RHO = -0.5                          # secondary prediction
SOURCES = ["trackc_swap/__init__.py", "trackc_swap/env.py", "trackc_swap/agent.py",
           "trackc_swap/train.py", "trackc_swap/factorial.py", "trackc_swap/erasure.py",
           "trackc_swap/longrun.py", "trackc_swap/confirm.py", "run_trackc_swap6.py",
           "test_trackc_swap.py", "TRACKC_SWAP_PROTOCOL_v6.md"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def configs(mode):
    """(world, train config for phase 1, seeds, phase-2 updates, checkpoints)."""
    if mode == "final":
        return WorldConfig(wear=WEAR), TrainConfig(), FINAL_SEEDS, P2_ITERS, CHECKPOINTS
    return (WorldConfig(horizon=100, wear=WEAR), TrainConfig(iters=10, n_envs=16, eval_episodes=1), [9000, 9001],
            30, (10, 20))


def med(xs):
    return statistics.median(list(xs))


def acc(e):
    return e["best_response_rate"]


def is_regulator(a, b):
    """Arm evaluation `a` against its partner's evaluation `b` (both from the final paired evaluation)."""
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
    drop = med(acc(v["eval"]) - acc(v["eval_full_erasure"][str(RATE)]) for v in m1)
    out["task_load"] = {"drop_median": drop, "loaded": drop >= LOAD_DROP}
    cells = {}
    for objective in ("M1", "M0"):
        ps = sorted((r for r in pairs if r["objective"] == objective), key=lambda r: r["seed"])
        per = {}
        for r in ps:
            F, Y = r["S-FATE"], r["S-YOKED"]
            per[r["seed"]] = {
                "rho_fate": F["eval"]["rho"], "rho_yoked": Y["eval"]["rho"],
                "in_band_fate": F["eval"]["in_band"], "in_band_yoked": Y["eval"]["in_band"],
                "eat_low_fate": F["eval"]["eat_rate_low"], "eat_high_fate": F["eval"]["eat_rate_high"],
                "mean_gain_fate": F["eval"]["mean_gain"],
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
             "acc_full_erasure_fate_median": med(x["acc_full_erasure_fate"] for x in v),
             "acc_full_erasure_yoked_median": med(x["acc_full_erasure_yoked"] for x in v),
             "acc_no_erasure_fate_median": med(x["acc_no_erasure_fate"] for x in v),
             "acc_fate_median": med(acc(r["S-FATE"]["eval"]) for r in ps),
             "acc_yoked_median": med(acc(r["S-YOKED"]["eval"]) for r in ps),
             "onset_in_band_fate_median": med(r["onset"]["S-FATE"]["in_band"] for r in ps),
             "onset_rho_fate_median": med(r["onset"]["S-FATE"]["rho"] for r in ps),
             "tradeoff_spearman": spearman([x["in_band_fate"] for x in v], [x["acc_full_erasure_fate"] for x in v])}
        c["checkpoints"] = {}
        for it in sorted({k for r in ps for k in r["checkpoints"]}, key=int):
            ev = [(r["checkpoints"][it]["S-FATE"]["eval"], r["checkpoints"][it]["S-YOKED"]["eval"]) for r in ps]
            c["checkpoints"][it] = {"regulators_fate": sum(is_regulator(f, y) for f, y in ev),
                                    "in_band_fate_median": med(f["in_band"] for f, y in ev),
                                    "seeds_fate_more_in_band": sum(f["in_band"] > y["in_band"] for f, y in ev)}
        cells[objective] = c
    m1c, m0c = cells["M1"], cells["M0"]
    crit = {
        "learned": out["learned"], "S4_payment": out["S4_payment"], "task_load": out["task_load"]["loaded"],
        "C1_regulators": m1c["regulators_fate"] >= MIN_REGULATORS,
        "C2_in_band_sign": m1c["seeds_fate_more_in_band"] >= MIN_BAND_SIGN,
        "C3_M0_specificity": m0c["regulators_fate"] <= MAX_CONTROL_REGULATORS,
        "C4_yoked_control": m1c["regulators_yoked"] <= MAX_CONTROL_REGULATORS,
    }
    out["criteria"] = crit
    out["verdict"] = "CONFIRMED" if all(crit.values()) else "NOT_CONFIRMED"
    out["failed"] = [k for k, ok in crit.items() if not ok]
    out["tradeoff_replicated"] = m1c["tradeoff_spearman"] <= TRADEOFF_RHO
    out["cells"] = cells
    return out


def report(sc):
    m1, m0 = sc["cells"]["M1"], sc["cells"]["M0"]
    n = m1["n"]
    L = ["# Track C swap v6 (option J: confirmation of SAT r = 0.3 regulators): results", "",
         f"**Verdict: {sc['verdict']}**" + (f" (failed: {', '.join(sc['failed'])})" if sc["failed"] else ""), "",
         f"Paid regulator rho_paid = {sc['rho_paid_median']:.2f}, in band {sc['drive_in_band_median']:.2f}; "
         f"margin = {sc['margin_mu']:.2f}. No-fate task accuracy {sc['nofate_m1_accuracy_median']:.3f}; "
         f"no-fate task agent rho {sc['nofate_m1_rho_median']:.2f}. Learned: {sc['learned']}. S4: {sc['S4_payment']}. "
         f"Task load at {RATE}: {sc['task_load']['drop_median']:.3f} ({'loaded' if sc['task_load']['loaded'] else 'not loaded'}).",
         "", "## Confirmation criteria", "", "| criterion | value | threshold | holds |", "| --- | --- | --- | --- |",
         f"| C1 M1 fate regulators | {m1['regulators_fate']}/{n} | >= {MIN_REGULATORS} | {sc['criteria']['C1_regulators']} |",
         f"| C2 M1 fate more in band | {m1['seeds_fate_more_in_band']}/{n} | >= {MIN_BAND_SIGN} | {sc['criteria']['C2_in_band_sign']} |",
         f"| C3 M0 fate regulators | {m0['regulators_fate']}/{m0['n']} | <= {MAX_CONTROL_REGULATORS} | {sc['criteria']['C3_M0_specificity']} |",
         f"| C4 M1 yoked regulators (roles swapped) | {m1['regulators_yoked']}/{n} | <= {MAX_CONTROL_REGULATORS} | {sc['criteria']['C4_yoked_control']} |",
         "", f"Secondary: Spearman(in band, full-erasure accuracy) over M1 fate agents = {m1['tradeoff_spearman']:.2f} "
         f"(predicted <= {TRADEOFF_RHO}): replicated {sc['tradeoff_replicated']}.", "",
         "## Cells (medians)", "",
         "| objective | rho fate / yoked | in band fate / yoked | fate > yoked rho | over margin | acc fate / yoked | "
         "acc full erasure fate / yoked | acc erasure off fate | onset in band |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for o, c in (("M1", m1), ("M0", m0)):
        L.append(f"| {o} | {c['rho_fate_median']:.2f} / {c['rho_yoked_median']:.2f} | "
                 f"{c['in_band_fate_median']:.2f} / {c['in_band_yoked_median']:.2f} | {c['seeds_fate_above_yoked']}/{c['n']} | "
                 f"{c['seeds_exceeding_margin']}/{c['n']} | {c['acc_fate_median']:.3f} / {c['acc_yoked_median']:.3f} | "
                 f"{c['acc_full_erasure_fate_median']:.3f} / {c['acc_full_erasure_yoked_median']:.3f} | "
                 f"{c['acc_no_erasure_fate_median']:.3f} | {c['onset_in_band_fate_median']:.2f} |")
    L += ["", "## Checkpoints (descriptive)", "", "| objective | updates | fate regulators | in band fate | fate more in band |",
          "| --- | --- | --- | --- | --- |"]
    for o, c in (("M1", m1), ("M0", m0)):
        for it, ck in c["checkpoints"].items():
            L.append(f"| {o} | {it} | {ck['regulators_fate']}/{c['n']} | {ck['in_band_fate_median']:.2f} | "
                     f"{ck['seeds_fate_more_in_band']}/{c['n']} |")
        L.append(f"| {o} | final | {c['regulators_fate']}/{c['n']} | {c['in_band_fate_median']:.2f} | "
                 f"{c['seeds_fate_more_in_band']}/{c['n']} |")
    for o, c in (("M1", m1), ("M0", m0)):
        L += ["", f"## Per seed, {o}", "",
              "| seed | rho fate / yoked | in band fate / yoked | eat rate E<0.5 / E>=0.5 (fate) | mean gain | "
              "acc full erasure fate / yoked | fate regulator | yoked regulator |",
              "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for s, x in sorted(c["per_seed"].items(), key=lambda kv: int(kv[0])):
            L.append(f"| {s} | {x['rho_fate']:.2f} / {x['rho_yoked']:.2f} | {x['in_band_fate']:.2f} / {x['in_band_yoked']:.2f} | "
                     f"{x['eat_low_fate']:.4f} / {x['eat_high_fate']:.4f} | {x['mean_gain_fate']:.2f} | "
                     f"{x['acc_full_erasure_fate']:.3f} / {x['acc_full_erasure_yoked']:.3f} | "
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
    p1_jobs = [(o, s, wcd, tcd, [RATE]) for o in ("M1", "M0", "DRIVE") for s in seeds]
    pdir = os.path.join(args.out, "pair_weights")
    os.makedirs(pdir, exist_ok=True)
    with Pool(os.cpu_count() or 1) as pool:
        p1 = []
        for k, r in enumerate(pool.imap_unordered(run_phase1, p1_jobs), 1):
            p1.append(r)
            print(f"[phase1 {k}/{len(p1_jobs)}] {r['objective']} seed {r['seed']} ({r['seconds']} s, "
                  f"elapsed {time.time() - t0:.0f} s)", flush=True)
        states = {(r["objective"], r["seed"]): r["state"] for r in p1}
        sdir = os.path.join(args.out, "phase1_weights")
        os.makedirs(sdir, exist_ok=True)
        for (o, s), b in states.items():
            if o in ("M1", "M0"):
                torch.save(state_from_bytes(b)["agent"], os.path.join(sdir, f"{o}_seed{s}.pt"))
        pair_jobs = [(o, s, GAIN, RATE, wcd, tcd, states[(o, s)], p2_iters, checkpoints)
                     for o in ("M1", "M0") for s in seeds]
        pairs = []
        for k, r in enumerate(pool.imap_unordered(run_pair_saved, pair_jobs), 1):
            for arm, b in r["weights"].items():
                torch.save(state_from_bytes(b), os.path.join(pdir, f"{r['objective']}_seed{r['seed']}_{arm}.pt"))
            pairs.append(strip(r))
            print(f"[pair {k}/{len(pair_jobs)}] {r['objective']} {r['gain_rule']} rate {r['rate']} "
                  f"seed {r['seed']} ({r['seconds']} s, elapsed {time.time() - t0:.0f} s)", flush=True)
    p1 = sorted((strip(r) for r in p1), key=lambda r: (r["objective"], r["seed"]))
    pairs.sort(key=lambda r: (r["objective"], r["seed"]))
    meta = {"mode": args.mode, "world": wcd, "train": tcd, "p2_iters": p2_iters, "checkpoints": list(checkpoints),
            "seeds": seeds, "gain_rule": GAIN, "rate": RATE, "seconds": round(time.time() - t0, 1),
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(path, "w") as fh:
        json.dump({"meta": meta, "phase1": p1, "pairs": pairs}, fh)
    sc = score(p1, pairs)
    with open(os.path.join(args.out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(args.out, "REPORT.md"), "w") as fh:
        fh.write(report(sc))
    print("verdict:", sc["verdict"], sc["failed"])


if __name__ == "__main__":
    main()
