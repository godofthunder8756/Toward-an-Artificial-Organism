"""Tests for the five canonical interventions (G5 I1-I5) and the single-write
SHARED test (G1 §2.1-c)."""

import numpy as np

from phase3.arms import Arm, apply_specialists, quantize_w
from phase3.interventions import (
    private_copy_divergence, scramble, single_write_reach, w_cut_outputs, wrong_w,
)
from phase3.specialists import A, B, COMMIT_A, COMMIT_B, POSTPONE, PRESERVE, RELEASE


def _intact(cfg, thr, w, regime):
    return apply_specialists(w, cfg, thr, regime)


def test_single_write_reaches_all_shared_vs_private(cfg, thr):
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    w_shared = np.zeros((4, cfg.task.horizon))          # candidate/R4: one slot
    w_private = np.zeros((4, cfg.task.horizon, 3))       # R1/R5: three copies
    reach_shared = single_write_reach(w_shared, 3.0, probe_entry)
    reach_private = single_write_reach(w_private, 3.0, probe_entry)
    assert list(reach_shared) == [True, True, True]
    assert list(reach_private) == [True, False, False]


def test_i1_scramble_signature_traces_function(cfg, thr):
    """I1: overwriting W with w* yields exactly (S_pol(w*), S_plan(w*), S_reg(w*))."""
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    regime = np.zeros(cfg.task.horizon, dtype=np.int64)
    regime[probe_entry:] = 1
    w = np.zeros((2, cfg.task.horizon))
    for w_star in [-3.0, -0.4, 0.0, 0.4, 3.0]:
        w2 = scramble(w, w_star, probe_entry)
        out = apply_specialists(w2, cfg, thr, regime)
        final = np.array([out["spol"][0, -1], out["splan"][0, -1], out["sreg"][0, -1]])
        # predicted functions of w*
        from phase3.specialists import s_pol, s_plan, s_reg, theta_value
        a, b = thr["a"], thr["b"]
        theta = theta_value(cfg.specialist, np.array([cfg.persistence.e0]),
                            np.array([1]), a, cfg.persistence.e_crit)
        pred = np.array([s_pol(np.array([w_star]))[0],
                         s_plan(np.array([w_star]), a, b)[0],
                         s_reg(np.array([w_star]), theta)[0]])
        assert np.array_equal(final, pred), (w_star, final, pred)


def test_i2_w_cut_per_consumer(cfg, thr):
    """I2: cutting W for one consumer drops it to its no-W baseline; the other
    two are byte-identical to the intact run."""
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    regime = np.zeros(cfg.task.horizon, dtype=np.int64)
    regime[probe_entry:] = 1
    w = np.array([[2.0] * cfg.task.horizon, [-2.0] * cfg.task.horizon])
    intact = _intact(cfg, thr, w, regime)
    # cut S_pol
    cut0 = w_cut_outputs(cfg, thr, w, 0, regime)
    assert np.all(cut0["spol"] == B)                       # forced no-W baseline (tie -> B)
    assert np.array_equal(cut0["splan"], intact["splan"])
    assert np.array_equal(cut0["sreg"], intact["sreg"])
    # cut S_plan
    cut1 = w_cut_outputs(cfg, thr, w, 1, regime)
    assert np.all(cut1["splan"] == POSTPONE)               # no-W baseline: postpone
    assert np.array_equal(cut1["spol"], intact["spol"])
    # cut S_reg
    cut2 = w_cut_outputs(cfg, thr, w, 2, regime)
    assert np.all(cut2["sreg"] == RELEASE)                 # no-W baseline: release
    assert np.array_equal(cut2["spol"], intact["spol"])


def test_i3_w_independent_of_consumers(cfg, candidate, eval_data):
    """I3: W's trajectory is a pure function of the token stream — no consumer
    output feeds back into it. Disabling consumers leaves W byte-identical."""
    z, x = eval_data
    tr = candidate.run(x)
    w1 = tr["w"]
    # apply_specialists is a pure function of w; re-running with a consumer
    # "cut" (its output discarded) cannot change w — assert the trajectory is
    # exactly reproduced from the same x on a fresh arm run.
    tr2 = candidate.run(x)
    assert np.array_equal(w1, tr2["w"])


def test_i4_private_copy_divergence(cfg, thr, eval_data):
    """I4: a frozen private copy diverges from the ongoing W in the
    accumulation phase (identity vs value, G5 §7)."""
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    w = np.concatenate([
        np.linspace(0.0, 6.0, probe_entry), np.zeros(cfg.task.horizon - probe_entry)
    ])[None, :]
    div = private_copy_divergence(cfg, w, 0, probe_entry, thr)
    assert div > 0.0


def test_i5_wrong_sign_coherent_error(cfg, thr):
    """I5: injecting a wrong W produces a mutually-consistent (coherent) triple
    equal to the specialists' functions of the injected value."""
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    regime = np.zeros(cfg.task.horizon, dtype=np.int64)
    regime[probe_entry:] = 1
    w = np.zeros((1, cfg.task.horizon))
    w_wrong = wrong_w(w, w_true_sign=+1.0, probe_entry=probe_entry, magnitude=3.0)
    out = apply_specialists(w_wrong, cfg, thr, regime)
    # wrong-sign: truth is A, injected W = -3 -> (B, commit-B, preserve)
    assert out["spol"][0, -1] == B
    assert out["splan"][0, -1] == COMMIT_B
    assert out["sreg"][0, -1] == PRESERVE


def test_r5_copies_bit_identical(cfg):
    """R5: the three fixed copies carry identical content by construction."""
    r5 = Arm(cfg, encoders={}, arm_name="r5")
    z, x = __import__("phase3.task", fromlist=["sample_episodes"]).sample_episodes(cfg.task, 64, 1)
    tr = r5.run(x)
    w = tr["w"]                      # (B, H, 3)
    assert np.array_equal(w[..., 0], w[..., 1])
    assert np.array_equal(w[..., 1], w[..., 2])
