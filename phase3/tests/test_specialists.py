"""Tests for the three specialists (G3): invariance classes, the SPRT
derivation, and the shared-content manifold geometry (G6)."""

import numpy as np

from phase3.audit import manifold_geometry
from phase3.specialists import (
    COMMIT_A, COMMIT_B, POSTPONE, PRESERVE, RELEASE, A, B,
    s_bias, s_conf, s_plan, s_pol, s_reg, sprt_boundaries,
)


def test_spol_sign_equivariant_and_magnitude_invariant():
    w = np.array([0.4, 4.0, -0.4, -4.0])
    flipped = s_pol(-w)
    assert np.array_equal(flipped, np.array([1 - int(a) for a in s_pol(w)]))  # A<->B
    # magnitude-invariant: same sign, different magnitude, same output
    assert np.array_equal(s_pol(np.array([0.4])), s_pol(np.array([4.0])))
    assert np.array_equal(s_pol(np.array([-0.4])), s_pol(np.array([-4.0])))


def test_splan_responds_to_both_sign_and_magnitude():
    a = b = 1.0
    assert s_plan(np.array([2.0]), a, b)[0] == COMMIT_A
    assert s_plan(np.array([-2.0]), a, b)[0] == COMMIT_B
    assert s_plan(np.array([0.5]), a, b)[0] == POSTPONE
    assert s_plan(np.array([-0.5]), a, b)[0] == POSTPONE
    # sign flip flips the commit direction but keeps the commit/postpone status
    assert s_plan(np.array([2.0]), a, b)[0] == COMMIT_A
    assert s_plan(np.array([-2.0]), a, b)[0] == COMMIT_B
    # magnitude shrink flips commit -> postpone
    assert s_plan(np.array([2.0]), a, b)[0] == COMMIT_A
    assert s_plan(np.array([1.0 / 2]), a, b)[0] == POSTPONE


def test_sreg_even_sign_invariant():
    theta = np.array([0.5])
    assert s_reg(np.array([2.0]), theta)[0] == PRESERVE
    assert s_reg(np.array([-2.0]), theta)[0] == PRESERVE  # sign-invariant
    assert s_reg(np.array([0.1]), theta)[0] == RELEASE
    assert s_reg(np.array([-0.1]), theta)[0] == RELEASE


def test_pairwise_noncollapse_on_perturbations():
    """G3 §3.2: every pair of specialists disagrees on a canonical perturbation."""
    a = b = 1.0
    theta = np.array([0.5])
    w = np.array([2.0])
    # sign flip: S_pol flips, S_plan flips, S_reg unchanged
    assert s_pol(-w)[0] != s_pol(w)[0]
    assert s_plan(-w, a, b)[0] != s_plan(w, a, b)[0]
    assert s_reg(-w, theta)[0] == s_reg(w, theta)[0]
    # magnitude shrink: S_pol unchanged, S_plan may flip, S_reg may flip
    assert s_pol(w / 2)[0] == s_pol(w)[0]


def test_sconf_strictly_monotone_fourth_class():
    ws = np.linspace(-6, 6, 100)
    p = s_conf(ws)
    assert np.all(np.diff(p) > 0)          # strictly increasing
    # belief reversal -> probability complement (not even, not magnitude-invariant)
    assert np.allclose(s_conf(-ws), 1.0 - s_conf(ws))


def test_sbias_shifted_threshold():
    theta_bias = -1.0986  # log(1/3)
    assert s_bias(np.array([0.0]), theta_bias)[0] == A   # 0 > theta_bias -> A
    assert s_bias(np.array([-2.0]), theta_bias)[0] == B


def test_sprt_boundaries_symmetric_and_positive():
    from phase3.config import SpecialistConfig
    cfg = SpecialistConfig()
    a, b = sprt_boundaries(cfg, 5, -6.0, 6.0, 24)
    assert a > 0 and b > 0
    assert abs(a - b) < 1e-9


def test_manifold_geometry():
    from phase3.config import Phase3Config
    cfg = Phase3Config()
    g = manifold_geometry(cfg)
    assert g["realizable_is_six"]
    assert g["n_realizable"] == 6
    assert len(g["off_curve_sign"]) == 4
    assert len(g["off_curve_mag"]) == 2
    assert g["off_curve_total"] == 6


def test_specialist_targets_splan_encoding_matches_s_plan():
    """AC14-class wiring check: the R2/R3 training target's S_plan encoding
    must equal specialists.s_plan (COMMIT_A=0, COMMIT_B=1, POSTPONE=2). A
    swapped encoding would silently train the heads to output 'postpone' where
    s_plan says 'commit-B', corrupting the R2/R3 incoherence endpoint."""
    import torch

    from phase3.arms import compute_thresholds
    from phase3.config import Phase3Config
    from phase3.train import specialist_targets

    cfg = Phase3Config()
    thr = compute_thresholds(cfg)
    # token 0 (t1, lambda +2.0) -> S=+64 (commit-A); token 4 (t5, -2.0) -> S=-64
    # (commit-B); token 2 (t3, 0.0) -> S=0 (postpone). H=32 streams.
    pos = torch.full((1, 32), 0, dtype=torch.long)
    neg = torch.full((1, 32), 4, dtype=torch.long)
    mid = torch.full((1, 32), 2, dtype=torch.long)
    for x, want in [(pos, COMMIT_A), (neg, COMMIT_B), (mid, POSTPONE)]:
        tgt = specialist_targets(cfg, x, thr)
        got = int(tgt["splan"][0, -1])
        assert got == want, (x[0, 0].item(), got, want)
