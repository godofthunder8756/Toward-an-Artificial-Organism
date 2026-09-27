"""Tests for the G2 task: generative model, quantization, anchors, and
observation equality across arms."""

import numpy as np

from phase3.config import BAYES_CEILING, MEMORYLESS_CLEAN, MEMORYLESS_PROBE, Phase3Config
from phase3.task import Quantizer, sample_episodes, token_stream_to_s, true_bayes_ceiling


def test_observation_equality_same_seed():
    cfg = Phase3Config()
    z1, x1 = sample_episodes(cfg.task, 256, 42)
    z2, x2 = sample_episodes(cfg.task, 256, 42)
    assert np.array_equal(z1, z2)
    assert np.array_equal(x1, x2)


def test_observation_equality_disjoint_seed_differs():
    cfg = Phase3Config()
    z1, x1 = sample_episodes(cfg.task, 256, 42)
    z2, x2 = sample_episodes(cfg.task, 256, 43)
    assert not np.array_equal(x1, x2)


def test_balanced_cause():
    cfg = Phase3Config()
    z, _ = sample_episodes(cfg.task, 2000, 0)
    assert abs(z.mean() - 0.5) < 0.05


def test_probe_window_is_neutral():
    cfg = Phase3Config()
    z, x = sample_episodes(cfg.task, 64, 0)
    probe = x[:, cfg.task.horizon - cfg.task.probe_window:]
    assert np.all(probe == 2)  # t3 = neutral


def test_quantizer_round_trip_resolution():
    cfg = Phase3Config()
    q = Quantizer(cfg.w)
    assert q.n_levels == 32
    s = np.array([0.0, 0.4, -0.4, 2.0, -2.0, 5.9, -5.9])
    w = q.round_trip(s)
    # sign preserved for |s| above half-resolution
    assert np.all(np.sign(w) == np.sign(np.where(s == 0, 1, s)))


def test_token_stream_matches_cumsum():
    cfg = Phase3Config()
    z, x = sample_episodes(cfg.task, 32, 0)
    s = token_stream_to_s(cfg.task, x)
    lam = np.asarray(cfg.task.token_lambda)
    manual = np.cumsum(lam[x], axis=-1)
    assert np.allclose(s, manual)


def test_memoryless_clean_bound():
    """The memoryless bound 0.606 (G2 §2.3) is reproduced from the model."""
    cfg = Phase3Config()
    # decide from the current token alone: argmax over P(z | x) = sigmoid(|lambda(x)|)
    z, x = sample_episodes(cfg.task, 20000, 7)
    lam = np.asarray(cfg.task.token_lambda)
    p_a = np.asarray(cfg.task.p_x_given_a)
    p_b = np.asarray(cfg.task.p_x_given_b)
    # marginal token prob and posterior
    pm = (p_a + p_b) / 2
    posterior_a = p_a / (p_a + p_b)  # P(A | x) per token
    acc = 0.0
    for tok in range(cfg.task.n_tokens):
        decide_a = posterior_a[tok] >= 0.5
        # correct if decide_a matches A (z=0)
        acc += pm[tok] * (posterior_a[tok] if decide_a else (1 - posterior_a[tok]))
    assert abs(acc - MEMORYLESS_CLEAN) < 0.01


def test_true_bayes_ceiling_above_812_bound():
    cfg = Phase3Config()
    ceiling = true_bayes_ceiling(cfg.task, n_episodes=8000, seed=3)
    # The true ceiling ~0.97 sits above the protocol's Chernoff *bound* 0.812.
    assert ceiling > BAYES_CEILING
    assert ceiling < 1.0
    assert MEMORYLESS_PROBE == 0.5
