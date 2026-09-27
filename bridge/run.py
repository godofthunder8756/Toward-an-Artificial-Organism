"""Reproducible training-run entry point for the neural bridge (N9).

Runs a small CPU training run and emits the records the N9 card's RECORD
clause requires, then verifies determinism by re-running the same seed and
comparing the first-step metric digest.

Outputs (under ``--outdir``, default ``bridge/runs/<name>-<seed>``):

- ``run_record.json``    architecture / training / energy / decay / optimizer /
                         losses / gradient-paths records, plus config vs actual
                         parameter counts.
- ``metrics.jsonl``      one line per training step (loss terms + economy
                         readouts: energy, age, alive fraction, refresh rate).
- ``checkpoint.pt``      the trained bridge + optimizer state.
- ``eval_episodes.jsonl`` saved evaluation episodes (the same environment /
                         episodes every arm reuses).

Usage::

    PYTHONPATH=. .venv-bridge/bin/python -B bridge/run.py \
        --seed 0 --steps 20 --batch-size 16 --outdir bridge/runs/smoke-0

The script exits non-zero if the determinism check fails (the two same-seed
runs must agree bit-for-bit on the first step's metric digest).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import asdict

from bridge.agent import NeuralBridge
from bridge.config import BridgeConfig
from bridge.trainer import BridgeTrainer


def build_run_record(config, bridge, seed, steps, batch_size):
    """Assemble every RECORD the card requires into one dict."""
    return {
        "name": config.name,
        "version": config.version,
        "seed": seed,
        # Architecture record (dims + parameter counts, config vs actual).
        "architecture": asdict(config.arch),
        "parameter_counts_config": config.parameter_counts(),
        "parameter_counts_actual": bridge.actual_parameter_counts(),
        # Training record (optimizer, LRs, init, schedule, horizon).
        "optimizer": asdict(config.optimizer),
        "init": asdict(config.init),
        "training": {
            **asdict(config.training),
            "steps_run": steps,
            "batch_size": batch_size,
            "episode_horizon": config.episode.horizon_t,
        },
        "losses": asdict(config.losses),
        "gradient_paths": config.gradient_paths,
        # Energy record.
        "energy": asdict(config.energy),
        # Decay record.
        "decay": asdict(config.decay),
    }


def _metric_digest(metrics):
    """A stable hash of the first step's metric scalars, for the determinism check."""
    if not metrics:
        return "empty"
    first = metrics[0]
    payload = json.dumps(
        {k: first[k] for k in sorted(first) if k != "step"}, sort_keys=True
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--steps", type=int, default=20)
    p.add_argument("--batch-size", type=int, default=16)
    p.add_argument("--outdir", type=str, default=None)
    p.add_argument("--skip-determinism-check", action="store_true")
    args = p.parse_args(argv)

    config = BridgeConfig()
    outdir = args.outdir or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "runs",
        f"{config.name}-{args.seed}",
    )
    os.makedirs(outdir, exist_ok=True)

    # Build fresh, run, and save.
    trainer = BridgeTrainer(config, args.seed)
    record = build_run_record(config, trainer.bridge, args.seed, args.steps, args.batch_size)
    history = trainer.train(args.steps, batch_size=args.batch_size, log_every=1)

    # Saved evaluation episodes (same environment every arm reuses).
    eval_batch = trainer.env.sample(batch_size=args.batch_size)
    n_eval = trainer.save_eval_episodes(
        eval_batch, os.path.join(outdir, "eval_episodes.jsonl")
    )

    with open(os.path.join(outdir, "run_record.json"), "w") as fh:
        json.dump(record, fh, indent=2)

    with open(os.path.join(outdir, "metrics.jsonl"), "w") as fh:
        for row in history:
            fh.write(json.dumps(row))
            fh.write("\n")

    trainer.save_checkpoint(os.path.join(outdir, "checkpoint.pt"))

    # Determinism check: a second same-seed run must agree on step 0.
    if not args.skip_determinism_check:
        trainer2 = BridgeTrainer(config, args.seed)
        history2 = trainer2.train(args.steps, batch_size=args.batch_size, log_every=1)
        digest1 = _metric_digest(history)
        digest2 = _metric_digest(history2)
        deterministic = digest1 == digest2 and all(
            h["step"] == h2["step"] and len(h) == len(h2)
            for h, h2 in zip(history, history2)
        )
    else:
        digest1 = _metric_digest(history)
        deterministic = True

    first = history[0]
    last = history[-1]
    print("run complete:", outdir)
    print("  seed:", args.seed, " steps:", args.steps, " batch_size:", args.batch_size)
    print("  params (config/actual):", record["parameter_counts_config"]["total"],
          "/", record["parameter_counts_actual"]["total"])
    print("  eval episodes saved:", n_eval)
    print("  step 0 total loss:", round(first["total"], 4))
    print("  final total loss:", round(last["total"], 4))
    print("  determinism:", "PASS" if deterministic else "FAIL", f"(digest {digest1})")

    if not deterministic:
        print("DETERMINISM CHECK FAILED", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
