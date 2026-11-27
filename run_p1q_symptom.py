"""P1q: does precarity recruit the integrity monitor into self-maintenance when the body can only be sensed through
it? (Layers 0 + 1 + 4, trained)

Protocol: P1Q_SYMPTOM_PROTOCOL.md. P1o found no coupling between the integrity monitor and foraging in agents
whose interoception already told them most of what a corruption would. Here every arm is trained in P1g's world
with an effectively blind interoceptive channel (noise SD INTERO_SD_Q, the reading clipped to [0, 1]): the body
can be tracked only by dead reckoning (eating is seen, slow wear is regular) and, for PFATE alone, by the damage
its own body causes (a symptom). Training is P1g's (run_seed_g), all three arms. The analysis is P1o's
(collect_coupling) and the decision rules are P1o's frozen ones (run_p1o_coupling.score / overall); P1g's own
score of the training records (the monitor, regulation) is reported, and its validity is required.

    python run_p1q_symptom.py --train discovery --max-new 4   # P1g's seeds 3200-3207
    python run_p1q_symptom.py --train confirm --max-new 4     # P1i's seeds 3400-3427
    python run_p1q_symptom.py --analyse discovery
    python run_p1q_symptom.py --analyse confirm
    python run_p1q_symptom.py --score p1q_symptom/confirm
"""
import argparse
import dataclasses
import json
import os
import platform
import sys
from dataclasses import asdict
from multiprocessing import Pool

import torch

import run_p1g_graded as G
import run_p1o_coupling as O
from run_trackc_paid import PAY, WEAR
from run_trackc_probe import fmt, sha
from trackc_swap.coupling import collect_coupling
from trackc_swap.env import WorldConfig
from trackc_swap.gradmon import KS_G
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C
from trackc_swap.selfmon import ARMS_M, P_MAX_M, RATE_M
from trackc_swap.train import TrainConfig

INTERO_SD_Q = 100.0        # the interoceptive reading carries practically no information (protocol section 2)
SETS = {"discovery": list(range(3200, 3208)), "confirm": list(range(3400, 3428))}
OUT = "p1q_symptom"
POINT = 3600
SOURCES = sorted(set(O.SOURCES + ["run_p1q_symptom.py", "test_p1q_symptom.py", "P1Q_SYMPTOM_PROTOCOL.md"]))


def world():
    return WorldConfig(wear=WEAR, intero_sd=INTERO_SD_Q)


def train(set_name, max_new):
    wc, tc = world(), TrainConfig()
    jobs = [(s, asdict(wc), asdict(tc), list(G.POINTS), PAY[1], WARM_ITERS_C, WARM_WRONG_C, REG_ITERS_C, RATE_M,
             P_MAX_M, G.BASE_F, KS_G) for s in SETS[set_name]]
    recs, _ = G.run_jobs(os.path.join(OUT, f"train_{set_name}"), jobs, max_new, keep_weights=True)
    print(f"{len(recs)} of {len(jobs)} trained", flush=True)


def analyse_seed(job):
    seed, wdir = job
    torch.set_num_threads(1)
    wc, tc = world(), dataclasses.replace(TrainConfig(), eval_episodes=O.EVAL_EPISODES)
    weights = {a: torch.load(os.path.join(wdir, f"seed{seed}_{a}_{POINT}.pt"), weights_only=False) for a in ARMS_M}
    return {"seed": seed, "arms": collect_coupling(seed, weights, wc, tc, PAY[1], G.BASE_F, ARMS_M)}


def load_train(set_name):
    recs = []
    for s in SETS[set_name]:
        path = os.path.join(OUT, f"train_{set_name}", "partial", f"seed{s}.json")
        if not os.path.exists(path):
            sys.exit(f"training not finished: seed {s}")
        with open(path) as fh:
            recs.append(json.load(fh))
    return recs


def score_all(raw):
    g = G.score(raw["train"])
    o = O.score(raw["coupling"])
    if not g["valid"]:
        overall = "INVALID"
    else:
        overall = O.overall(o)
    return {"overall": overall, "P1g": g, "P1o": o}


def report(sc, title):
    g, o = sc["P1g"], sc["P1o"]
    p = g["points"][str(g["primary_at"])]
    L = [f"# {title}", "",
         f"**Overall: {sc['overall']}** (P1o's frozen rules, with P1g's validity on the trained agents). "
         f"Interoceptive noise SD {INTERO_SD_Q}. Seeds: {o['n_seeds']}.", "",
         f"- P1g on these agents: valid {g['valid']} (memory {g['valid_memory']}, damage {g['valid_damage']}, "
         f"exposure {g['valid_exposure']}; phase-1 clear correct {fmt(g['phase1_clear_correct_median'], 3)}, "
         f"exposure {fmt(g['exposure_median'], 3)}); P1g overall {g['overall']}, arrow {g['arrow']}.",
         O.tline("P1G_1 monitor learned: M, PFATE against PNOFATE", p["P1G_1"]),
         O.tline("P1G_3 monitor, PFATE against PYOKED", p["P1G_3"]),
         O.tline("regulation: in band, PFATE against PYOKED", p["secondary"]["regulation_PFATE_vs_PYOKED"]),
         O.tline("regulation: in band, PFATE against PNOFATE", p["secondary"]["regulation_PFATE_vs_PNOFATE"]),
         "- in band, PFATE / PYOKED / PNOFATE: " + " / ".join(fmt(p["arms"][a]["in_band"], 3) for a in ARMS_M),
         "", "## Coupling (P1o's analysis and rules)", ""]
    L += O.report(o, "P1o on the blind-body agents").splitlines()[2:]
    return "\n".join(L) + "\n"


def analyse(set_name):
    out = os.path.join(OUT, set_name)
    os.makedirs(out, exist_ok=True)
    if os.path.exists(os.path.join(out, "raw.json")):
        sys.exit("refusing to overwrite raw.json")
    raw = {"train": load_train(set_name)}
    wdir = os.path.join(OUT, f"train_{set_name}", "weights")
    seeds = SETS[set_name]
    with Pool(min(len(seeds), os.cpu_count() or 1)) as pool:
        raw["coupling"] = sorted(pool.imap_unordered(analyse_seed, [(s, wdir) for s in seeds]),
                                 key=lambda r: r["seed"])
    title = {"discovery": "P1q discovery: the integrity monitor and self-maintenance with a blind body, P1g's seeds "
                          "(3200-3207)",
             "confirm": "P1q: the integrity monitor and self-maintenance with a blind body, P1i's seeds "
                        "(3400-3427)"}[set_name]
    meta = {"stage": set_name, "title": title, "seeds": seeds, "intero_sd": INTERO_SD_Q,
            "python": platform.python_version(), "torch": torch.__version__,
            "source_sha256": {p: sha(p) for p in SOURCES if os.path.exists(p)}}
    with open(os.path.join(out, "raw.json"), "w") as fh:
        json.dump({"meta": meta, "raw": raw}, fh)
    sc = score_all(raw)
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
        print(report(score_all(d["raw"]), d["meta"]["title"]), end="")
        return
    sys.exit("choose --train, --analyse or --score")


if __name__ == "__main__":
    main()
