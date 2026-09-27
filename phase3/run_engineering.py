"""Phase-III engineering driver (the training + evaluation entry point).

Trains the six arms on engineering seeds and writes the raw results to a fresh
versioned results dir (``mkdir(exist_ok=False)`` — never overwriting a frozen
dir). This is the *engineering* run (model seeds 0-7): it validates the
implementation and informs which endpoints discriminate; the final run (G13)
uses the disjoint finals family 100-111.

The **model seed** is the replication unit (protocol §10.1): one independent
draw of the training RNG (weight init, curriculum order) *and* the
evaluation-episode stream. Each model seed therefore trains its own six arms
and evaluates them on its own episode stream — the model is *not* trained once
and re-evaluated across episode seeds (that would under-count the training-RNG
replication and silently break the N=12 pairing of §10.1).

Usage (from repo root, .venv-bridge, CPU-only):

    CUDA_VISIBLE_DEVICES= PYTHONPATH=. .venv-bridge/bin/python -B \
        phase3/run_engineering.py --out phase3_results_engineering_v1 --seeds 0 1 2 3 4 5 6 7

The driver is deterministic: re-running with the same args reproduces the same
rows (state_hash identity, the replay guarantee). The training schedule and
evaluation-episode count default to the frozen config (``TrainingConfig.steps``
= 2000, ``SeedConfig.eval_episodes_per_seed`` = 1024); override with ``--steps``
/ ``--n-episodes`` only for a deliberate engineering sweep, never silently.
"""

from __future__ import annotations

import argparse
import os
import sys

from phase3.config import Phase3Config
from phase3.runner import build_arm, endpoints, write_results, ARM_NAMES

SNAPSHOT_SOURCES = [
    "phase3/config.py", "phase3/task.py", "phase3/model.py",
    "phase3/specialists.py", "phase3/arms.py", "phase3/train.py",
    "phase3/interventions.py", "phase3/novel_consumer.py", "phase3/leakage.py",
    "phase3/runner.py", "ACI_PHASE3_PROTOCOL_v1.md",
]


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    p.add_argument("--n-episodes", type=int, default=1024)
    p.add_argument("--steps", type=int, default=2000)
    p.add_argument("--p-level", default="small")
    args = p.parse_args(argv)

    cfg = Phase3Config()
    cfg = _with_overrides(cfg, steps=args.steps, p_level=args.p_level)

    rows = []
    for seed in args.seeds:
        # Train a fresh model per seed (the model seed is the replication unit).
        arms = {name: build_arm(cfg, name, seed) for name in ARM_NAMES}
        rows.extend(endpoints(cfg, arms, seed, args.n_episodes))

    written = write_results(args.out, cfg, rows, SNAPSHOT_SOURCES)
    for k, v in written.items():
        print(f"{k}: {v}")
    print(f"seeds: {args.seeds}, rows: {len(rows)}")


def _with_overrides(cfg: Phase3Config, steps: int, p_level: str) -> Phase3Config:
    from dataclasses import replace
    cfg = replace(cfg, training=replace(cfg.training, steps=steps),
                  arm=replace(cfg.arm, p_level=p_level))
    return cfg


if __name__ == "__main__":
    main(sys.argv[1:])
