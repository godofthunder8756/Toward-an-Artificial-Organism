"""P1p: replication of the Layer 4 integrity monitor in a second architecture (a 35-cell CIFG-LSTM).

Protocol: P1P_REPLICATION_PROTOCOL.md. Architecture: trackc_swap/archswap.py. Training is P1g's (run_seed_g)
and the analyses are P1g's, P1j's, P1k's, P1l's and P1m's own, each with its own decision rules, run on the
CIFG agents.

    python run_p1p_replication.py --train discovery --max-new 4   # P1g's seeds 3200-3207, batches of four
    python run_p1p_replication.py --train confirm --max-new 4     # P1i's seeds 3400-3427
    python run_p1p_replication.py --analyse discovery             # after training
    python run_p1p_replication.py --analyse confirm               # after the freeze and training
    python run_p1p_replication.py --score p1p_replication/confirm
"""
import argparse
import json
import os
import platform
import sys
from dataclasses import asdict
from multiprocessing import Pool

import torch

from trackc_swap import archswap

archswap.install()          # every runner built in this process (and its forked workers) is a CIFG runner

import run_p1g_graded as G                    # noqa: E402
import run_p1j_steer as J                     # noqa: E402
import run_p1k_transfer as K                  # noqa: E402
import run_p1l_access as L                    # noqa: E402
import run_p1m_necessity as M                 # noqa: E402
from run_trackc_paid import PAY, WEAR         # noqa: E402
from run_trackc_probe import med, sha         # noqa: E402
from trackc_swap.env import WorldConfig       # noqa: E402
from trackc_swap.gradmon import KS_G          # noqa: E402
from trackc_swap.selfcomp import REG_ITERS_C, WARM_WRONG_C   # noqa: E402
from trackc_swap.selfmon import P_MAX_M, RATE_M   # noqa: E402
from trackc_swap.train import TrainConfig     # noqa: E402

SETS = {"discovery": list(range(3200, 3208)), "confirm": list(range(3400, 3428))}
OUT = "p1p_replication"
STUDIES = {"P1j": J, "P1k": K, "P1l": L, "P1m": M}
WARM_ITERS_P = 3600   # phase-1 warm-up for the CIFG (disclosed adjustment, protocol section 5): the CIFG learns the
                      # memory about half as fast as the GRU (p1p_replication/diagnostics), so 1,200 left it at chance
GRU_LABELS = {"P1g": "P1G_1 DERIVED_AHEAD", "P1j": "LEARNED_SIGNED_INTEGRITY_VARIABLE",
              "P1k": "GENERAL_INTEGRITY_VARIABLE", "P1l": "SHARED_GENERAL_ACCESS", "P1m": "VALUE_CREDITED"}
SOURCES = sorted(set(G.SOURCES + J.SOURCES + K.SOURCES + L.SOURCES + M.SOURCES
                     + ["trackc_swap/archswap.py", "run_p1p_replication.py", "test_p1p_replication.py",
                        "P1P_REPLICATION_PROTOCOL.md"]))


def train(set_name, max_new):
    seeds = SETS[set_name]
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    jobs = [(s, asdict(wc), asdict(tc), list(G.POINTS), PAY[1], WARM_ITERS_P, WARM_WRONG_C, REG_ITERS_C, RATE_M,
             P_MAX_M, G.BASE_F, KS_G) for s in seeds]
    out = os.path.join(OUT, f"train_{set_name}")
    recs, _ = G.run_jobs(out, jobs, max_new, keep_weights=True)
    print(f"{len(recs)} of {len(jobs)} trained", flush=True)


def _pool(fn, jobs):
    with Pool(min(len(jobs), os.cpu_count() or 1)) as pool:
        return sorted(pool.imap_unordered(fn, jobs), key=lambda r: r["seed"])


def p1g_label(sc):
    p = sc["points"][str(sc["primary_at"])]
    return p["P1G_1"]["label"]


def summarize(scores):
    """Per study: the study's own overall label, against the GRU's confirmed label."""
    g = scores["P1g"]
    lab = {"P1g": (f"P1G_1 {p1g_label(g)}" if g["valid"] else "INVALID"),
           **{k: scores[k]["overall"] for k in STUDIES}}
    match = {k: lab[k] == GRU_LABELS[k] for k in lab}
    return lab, match


def overall(scores):
    g = scores["P1g"]
    if not g["valid"]:
        return "INVALID"
    if g["n_seeds"] < 10 or p1g_label(g) == "UNDETERMINED":
        return "UNDETERMINED"
    if p1g_label(g) != "DERIVED_AHEAD":
        return "MONITOR_NOT_REPLICATED"
    _, match = summarize(scores)
    return "BLOCK_REPLICATED" if all(match.values()) else "PARTIAL_REPLICATION"


def score_all(raw):
    sc = {"P1g": G.score(raw["P1g"])}
    for k, mod in STUDIES.items():
        sc[k] = mod.score(raw[k])
    return sc


def report(scores, title, raw):
    lab, match = summarize(scores)
    g = scores["P1g"]
    p = g["points"][str(g["primary_at"])]
    L_ = [f"# {title}", "",
          f"**Overall: {overall(scores)}.** Architecture: CIFG-LSTM, 35 cells, packed state [h, c] of 70 "
          f"(the GRU's width); parameters {g['params']}. Seeds: {g['n_seeds']}. Each study's own decision rules.", "",
          "| study | label on the CIFG | label on the GRU (confirmed) | same |", "| --- | --- | --- | --- |"]
    for k in lab:
        L_.append(f"| {k} | {lab[k]} | {GRU_LABELS[k]} | {'yes' if match[k] else 'no'} |")
    L_ += ["", "## P1g (monitor; training records)", "",
           f"- valid {g['valid']} (memory {g['valid_memory']}, damage {g['valid_damage']}, exposure "
           f"{g['valid_exposure']}); phase-1 clear correct {g['phase1_clear_correct_median']}; exposure "
           f"{g['exposure_median']}; P1g overall {g['overall']}; arrow {g['arrow']}"]
    for t in ("P1G_1", "P1G_2", "P1G_3"):
        L_.append(J.tline(t, p[t]))
    for a in G.ARMS:
        A = p["arms"][a]
        L_.append(f"- {a}: M {A.get('M')}, M_early {A.get('M_early')}, in_band {A.get('in_band')}, "
                  f"acc_conflict {A.get('acc_conflict')}")
    for k, mod in STUDIES.items():
        L_ += ["", f"## {k}", ""]
        L_ += mod.report(scores[k], f"{k} on the CIFG").splitlines()[2:]
    return "\n".join(L_) + "\n"


def load_train(set_name):
    pdir = os.path.join(OUT, f"train_{set_name}", "partial")
    recs = []
    for s in SETS[set_name]:
        path = os.path.join(pdir, f"seed{s}.json")
        if not os.path.exists(path):
            sys.exit(f"training not finished: seed {s}")
        with open(path) as fh:
            recs.append(json.load(fh))
    return recs


def analyse(set_name):
    out = os.path.join(OUT, set_name)
    os.makedirs(out, exist_ok=True)
    if os.path.exists(os.path.join(out, "raw.json")):
        sys.exit("refusing to overwrite raw.json")
    raw = {"P1g": load_train(set_name)}
    wdir = os.path.join(OUT, f"train_{set_name}", "weights")
    for k, mod in STUDIES.items():
        raw[k] = _pool(mod.analyse_seed, [(s, wdir) for s in SETS[set_name]])
        print(f"[analysis] {k} done", flush=True)
    title = {"discovery": "P1p discovery: the Layer 4 battery on a CIFG-LSTM, P1g's seeds (3200-3207)",
             "confirm": "P1p: the Layer 4 battery on a CIFG-LSTM, P1i's seeds (3400-3427)"}[set_name]
    meta = {"stage": set_name, "title": title, "seeds": SETS[set_name], "arch": "CIFG", "n_cell": archswap.N_CELL,
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(os.path.join(out, "raw.json"), "w") as fh:
        json.dump({"meta": meta, "raw": raw}, fh)
    sc = score_all(raw)
    lab, match = summarize(sc)
    with open(os.path.join(out, "scores.json"), "w") as fh:
        json.dump({"meta": meta, "overall": overall(sc), "labels": lab, "match": match, "scores": sc}, fh,
                  indent=1, default=str)
    rep = report(sc, title, raw)
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
        print(report(score_all(d["raw"]), d["meta"]["title"], d["raw"]), end="")
        return
    sys.exit("choose --train, --analyse or --score")


if __name__ == "__main__":
    main()
