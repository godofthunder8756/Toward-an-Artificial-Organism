"""P1i: confirmation of the calibrated integrity discount on fresh seeds.

Protocol: P1I_CALIB_PROTOCOL.md. Training is P1g's frozen design (run_p1g_graded, BASE_F 0.012) on fresh seeds;
the analysis (trackc_swap/calibdisc.py) is frozen in the protocol commit before it is run on any of them.

    python run_p1i_calib.py --train --max-new 4                  # trains seeds 3400-3427 into p1i_calib/p1g_design
    python run_p1i_calib.py --analyse                            # P1i analysis (after the protocol freeze)
    python run_p1i_calib.py --score p1i_calib
"""
import argparse
import json
import os
import sys
from dataclasses import asdict

import run_p1g_graded as G
from run_trackc_paid import PAY, WEAR
from trackc_swap.env import WorldConfig
from trackc_swap.gradmon import KS_G
from trackc_swap.selfcomp import REG_ITERS_C, WARM_ITERS_C, WARM_WRONG_C
from trackc_swap.selfmon import P_MAX_M, RATE_M
from trackc_swap.train import TrainConfig

FINAL_SEEDS = list(range(3400, 3428))
OUT = "p1i_calib"
TRAIN_DIR = os.path.join(OUT, "p1g_design")


def train(max_new):
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    jobs = [(s, asdict(wc), asdict(tc), list(G.POINTS), PAY[1], WARM_ITERS_C, WARM_WRONG_C, REG_ITERS_C, RATE_M,
             P_MAX_M, G.BASE_F, KS_G) for s in FINAL_SEEDS]
    recs, _ = G.run_jobs(TRAIN_DIR, jobs, max_new)
    if len(recs) < len(jobs):
        print(f"stopped after this batch: {len(recs)} of {len(jobs)} jobs finished", flush=True)
        return
    recs.sort(key=lambda r: r["seed"])
    path = os.path.join(TRAIN_DIR, "raw.json")
    if not os.path.exists(path):
        with open(path, "w") as fh:
            json.dump({"meta": {"seeds": FINAL_SEEDS, "base": G.BASE_F}, "seeds": recs}, fh)
    sc = G.score(recs)
    with open(os.path.join(TRAIN_DIR, "scores.json"), "w") as fh:
        json.dump({"scores": sc}, fh, indent=1, default=str)
    with open(os.path.join(TRAIN_DIR, "REPORT.md"), "w") as fh:
        fh.write(G.report(sc).replace("# Track C P1g", "# P1i: replication of P1g's design (seeds 3400-3427)", 1))
    print("training finished; P1g replication report written", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", action="store_true")
    ap.add_argument("--analyse", action="store_true")
    ap.add_argument("--score")
    ap.add_argument("--max-new", type=int, default=0)
    args = ap.parse_args()
    if args.train:
        train(args.max_new)
        return
    sys.exit("analysis is added at the protocol freeze")


if __name__ == "__main__":
    main()
