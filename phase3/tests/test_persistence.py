"""Tests for paid W persistence (H1.3 pi-cut) and the F1 free-recurrence test
(H1.4) — the two load-bearing MAINTAINED checks (G9 obligation 2)."""

import numpy as np

from phase3.arms import apply_specialists
from phase3.leakage import decode_accuracy
from phase3.task import token_stream_to_s, true_bayes_ceiling


def _probe_acc(w, cfg, thr, regime):
    out = apply_specialists(w, cfg, thr, regime)
    return out["spol"][..., -1]


def test_candidate_reaches_bayes_ceiling(cfg, candidate, thr, eval_data):
    z, x = eval_data
    tr = candidate.run(x)
    acc = float(np.mean(_probe_acc(tr["w"], cfg, thr, tr["regime"]) == z))
    ceiling = true_bayes_ceiling(cfg.task, n_episodes=8000, seed=5)
    # candidate reaches the empirical Bayes ceiling (equivalence, to a few %)
    assert acc >= ceiling - 0.05
    assert acc > 0.85


def test_pi_cut_decays_probe_accuracy(cfg, candidate, thr, eval_data):
    z, x = eval_data
    intact = candidate.run(x)
    cut = candidate.run(x, cut_pi=True)
    acc_intact = float(np.mean(_probe_acc(intact["w"], cfg, thr, intact["regime"]) == z))
    acc_cut = float(np.mean(_probe_acc(cut["w"], cfg, thr, cut["regime"]) == z))
    assert acc_intact > 0.85
    # the pi-cut collapses the probe to chance (memoryless bound 0.500)
    assert abs(acc_cut - 0.5) < 0.05


def test_pi_cut_decays_w_value(cfg, candidate, eval_data):
    _, x = eval_data
    intact = candidate.run(x)
    cut = candidate.run(x, cut_pi=True)
    # the stored value collapses toward neutral under the cut
    assert np.mean(np.abs(cut["w"][..., -1])) < np.mean(np.abs(intact["w"][..., -1]))


def test_free_recurrence_f1(cfg, candidate, eval_data):
    """F1: with pi cut AND W zeroed, h_t must not retain z at the probe."""
    z, x = eval_data
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    tr = candidate.run(x, cut_pi=True, zero_w=True)
    h = tr["h"]                                   # (N, H, d_h)
    h_probe = h[:, probe_entry:, :].reshape(len(z), -1)
    acc, _ = decode_accuracy(h_probe, z)
    assert abs(acc - 0.5) < 0.06


def test_weight_bypass_i2_scramble(cfg, candidate, thr, eval_data):
    """I2-scramble at the probe: S_pol's output must track the scrambled W,
    not z — the output decode from z falls to chance (no z-pathway through
    the weights, G8 §6 gate 4)."""
    from phase3.interventions import scramble
    z, x = eval_data
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    tr = candidate.run(x)
    w_scrambled = scramble(tr["w"], 0.0, probe_entry)
    out = apply_specialists(w_scrambled, cfg, thr, tr["regime"])
    spol = out["spol"][..., -1]
    assert abs(float(np.mean(spol == z)) - 0.5) < 0.05


def test_observation_equality_same_stream_all_arms(cfg, candidate, eval_data):
    """Every arm runs the identical token stream (G4 §8 rule 1)."""
    z, x = eval_data
    r4 = __import__("phase3.arms", fromlist=["Arm"]).Arm(cfg, encoders={}, arm_name="r4")
    tr_c = candidate.run(x)
    tr_4 = r4.run(x)
    # R4's free accumulator tracks S_t = cumsum(lambda(x)); same x in, same task.
    s = token_stream_to_s(cfg.task, x)
    from phase3.arms import quantize_w
    assert np.allclose(tr_4["w"], quantize_w(cfg, s))
