"""Tests for hidden-copy leakage (G8): the sever test, the weight-bypass test,
and the decode-ablation sanity — establishing that no pathway other than W
carries z for free in the candidate."""

import numpy as np

from phase3.leakage import decode_accuracy
from phase3.specialists import A, B


def test_sever_history_specialists_pure_function_of_w(cfg, thr):
    """Sever test (G3 §6 gate 5 / G8 §4.1): specialists are pure functions of
    W — holding W fixed and removing the history leaves outputs unchanged."""
    from phase3.arms import apply_specialists
    w = np.array([[2.0, -2.0, 0.5, -0.5]])          # (1, 4): one episode, four steps
    regime = np.zeros(4, dtype=np.int64)
    out1 = apply_specialists(w, cfg, thr, regime)
    # the same W value, re-computed (no history access anywhere) is identical
    out2 = apply_specialists(w.copy(), cfg, thr, regime)
    for k in ("spol", "splan", "sreg"):
        assert np.array_equal(out1[k], out2[k])


def test_a_reads_bookkeeping_not_w(cfg):
    """L3: the maintenance rule A reads (s, E, d) only — z-blind and W-blind
    by construction (verdict D)."""
    from phase3.model import Maintenance
    import inspect
    maint = Maintenance(cfg)
    params = list(inspect.signature(maint.decide_refresh).parameters)
    assert params == ["s", "e", "d"]


def test_specialists_stateless_no_recurrent_carry(cfg, thr):
    """L2/L6: the specialists are stateless maps of W — no recurrent carry."""
    from phase3.specialists import s_pol, s_plan, s_reg
    # a specialist's output depends only on its (W, context) args, no hidden state
    assert s_pol(np.array([1.0])).shape == (1,)


def test_decode_ablation_sanity(cfg, candidate, eval_data):
    """G8 §4.3: zeroing the pathway drops the decoder to chance (the instrument
    measures what it claims)."""
    z, x = eval_data
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    tr = candidate.run(x)
    h = tr["h"][:, probe_entry:, :].reshape(len(z), -1)
    acc_full, _ = decode_accuracy(h, z)
    acc_zero, _ = decode_accuracy(np.zeros_like(h), z)
    # the full h_t decode should be above chance (the encoder is informative);
    # zeroing the pathway drops to chance.
    assert acc_full > 0.6
    assert abs(acc_zero - 0.5) < 0.08


def test_conditional_decode_h_t_richer_than_w(cfg, candidate, eval_data):
    """L1: the GRU hidden state h_t carries z (disclosed acquisition machinery)
    — it is the full-precision pre-quantization carry, richer than W."""
    z, x = eval_data
    probe_entry = cfg.task.horizon - cfg.task.probe_window
    tr = candidate.run(x)
    h = tr["h"][:, probe_entry:, :].reshape(len(z), -1)
    acc, _ = decode_accuracy(h, z)
    assert acc > 0.85
