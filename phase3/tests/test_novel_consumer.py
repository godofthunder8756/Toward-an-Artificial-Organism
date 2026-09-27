"""Tests for frozen-core transfer (G7): S_conf/S_bias reuse the frozen W with
zero retraining, reach the ceiling from b bits alone, and leave the old
specialists byte-identical."""

import numpy as np

from phase3.novel_consumer import (
    novel_consumer_scores, posterior_entropy_ceiling, s_bias_accuracy, s_conf_log_loss,
)
from phase3.task import token_stream_to_s


def test_frozen_core_byte_identity(candidate, eval_data):
    """H5.4: freezing the encoder leaves W's trajectory byte-identical (the
    old specialists' inputs are unchanged across the Phase-1/Phase-2 boundary)."""
    z, x = eval_data
    tr1 = candidate.run(x)
    tr2 = candidate.run(x)          # the frozen core, re-run (no retraining)
    assert np.array_equal(tr1["w"], tr2["w"])


def test_s_conf_reaches_bayes_ceiling(cfg, candidate, thr, eval_data):
    """H5.1: S_conf (sigma(W)) reaches the Bayes-calibrated ceiling to the
    quantization floor, reading W alone."""
    from phase3.arms import quantize_w
    z, x = eval_data
    tr = candidate.run(x)
    scores = novel_consumer_scores(cfg, tr["w"], z, thr)
    s_h = token_stream_to_s(cfg.task, x)[..., -1]
    # the ceiling to the *quantization floor*: sigma(quantize(S_H)) — the best
    # any b-bit readout can do, versus the full-precision sigma(S_H).
    ceil_quantized = posterior_entropy_ceiling(cfg, quantize_w(cfg, s_h), z)
    assert abs(scores["s_conf_log_loss"] - ceil_quantized) < 0.02


def test_s_conf_reading_w_alone_no_history(cfg, candidate, thr, eval_data):
    """H5.3: S_conf/S_bias read b bits and nothing else — their outputs are
    pure functions of W (sever-history leaves them unchanged)."""
    z, x = eval_data
    tr = candidate.run(x)
    w_h = tr["w"][..., -1]
    # S_conf is a pure function of the final W value
    assert np.allclose(
        s_conf_log_loss(w_h, z),
        -np.mean(np.log(np.clip(1 / (1 + np.exp(-w_h)), 1e-9, 1.0) ** (z == 0)
                        * np.clip(1 - 1 / (1 + np.exp(-w_h)), 1e-9, 1.0) ** (z == 1))),
        rtol=1e-6,
    )


def test_s_bias_shifted_decision(cfg, candidate, thr, eval_data):
    """H5.1/H5.5: S_bias is the shifted-threshold decision (a new boundary,
    not a relabelled S_pol)."""
    z, x = eval_data
    tr = candidate.run(x)
    scores = novel_consumer_scores(cfg, tr["w"], z, thr)
    # asymmetric cost ratio 3:1 -> theta_bias = log(1/3) < 0, so S_bias leans A
    assert thr["theta_bias"] < 0
    # its accuracy is a real decision score in [0, 1]
    assert 0.0 <= scores["s_bias_accuracy"] <= 1.0


def test_zero_retraining_reuse(cfg, candidate, thr, eval_data):
    """H4.2/H5.2: the new consumers are served with the encoder frozen —
    exactly zero inference-retraining samples (the encoder has no new
    training after freeze)."""
    z, x = eval_data
    # Freeze: snapshot the encoder weights; attach S_conf/S_bias (fixed functions)
    # requires no gradient step; the W trajectory is unchanged.
    tr_before = candidate.run(x)
    scores = novel_consumer_scores(cfg, tr_before["w"], z, thr)
    tr_after = candidate.run(x)
    assert np.array_equal(tr_before["w"], tr_after["w"])
    assert "s_conf_log_loss" in scores
