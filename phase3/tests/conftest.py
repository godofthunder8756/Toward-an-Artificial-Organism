"""Shared fixtures for the Phase-III test suite.

A single trained candidate encoder (session-scoped) is reused across tests so
the suite stays fast. Training uses seed 0; evaluation uses disjoint seeds
(no memorization). The candidates/rivals and thresholds are built fresh per
test from the frozen config.
"""

from __future__ import annotations

import numpy as np
import pytest

from phase3.arms import Arm, compute_thresholds
from phase3.config import Phase3Config
from phase3.model import Encoder
from phase3.train import train_encoder

TRAIN_SEED = 0
EVAL_SEED = 999


@pytest.fixture(scope="session")
def cfg() -> Phase3Config:
    from dataclasses import replace

    c = Phase3Config()
    # Train at the frozen default (2000 steps): a speed-reduced 400-step
    # encoder under-trains calibration and makes the H5.1 ceiling assertion
    # (test_s_conf_reaches_bayes_ceiling) fail at ~0.05 log-loss gap, right at
    # the threshold. 2000 steps is the config the finals actually run.
    return replace(c, training=replace(c.training, steps=2000))


@pytest.fixture(scope="session")
def encoder(cfg):
    # Pin the init RNG, not just the training loop: Encoder() uses xavier init,
    # which draws from the ambient torch RNG — an unseeded init makes the whole
    # suite order-/run-dependent (a bad init leaves a large S_conf calibration
    # gap that even 400 steps cannot always recover). Seeding here makes the
    # session-scoped encoder byte-deterministic across runs.
    import bridge.reproducibility as _rep

    _rep.seed_all(TRAIN_SEED)
    e = Encoder(cfg)
    train_encoder(cfg, e, cfg.training.steps, cfg.training.lr, TRAIN_SEED, "enc")
    return e


@pytest.fixture(scope="session")
def thr(cfg):
    return compute_thresholds(cfg)


@pytest.fixture(scope="session")
def candidate(cfg, encoder):
    return Arm(cfg, encoders={"enc": encoder}, arm_name="candidate")


@pytest.fixture(scope="session")
def eval_data(cfg):
    """A disjoint evaluation episode set (observation-equality basis)."""
    from phase3.task import sample_episodes
    z, x = sample_episodes(cfg.task, 2048, EVAL_SEED)
    return z, x
