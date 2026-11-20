"""P1c calibration: run one stage-1 calibration round with a given overwrite rate and cap on given seeds.

    python p1c_selfover_calibration/calib_variant.py --rate 0.6 --pmax 1.0 --seeds 9958 9959 9960 9961 --out <dir>

The module constants are set before the worker pool forks, so every worker uses them. Not used by the final run.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import run_p1c_selfover as R          # noqa: E402
import trackc_swap.selfover as SO     # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--rate", type=float, required=True)
ap.add_argument("--pmax", type=float, required=True)
ap.add_argument("--seeds", type=int, nargs="+", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
assert set(a.seeds) <= set(R.CALIB_SEEDS)
SO.RATE_O, SO.P_MAX_O = a.rate, a.pmax
R.RATE_O = a.rate   # recorded in meta and the report
R.CALIB_ROUND = a.seeds
sys.argv = [sys.argv[0], "--mode", "calib", "--out", a.out]
R.main()
