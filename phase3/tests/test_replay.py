"""Tests for replay support and the audit script (split verification).

Replay: a re-run on the same seed reproduces byte-identical rows (state_hash).
Audit: re-derives coverage and hash identity from the saved table without
simulating.
"""

import os
import tempfile

import numpy as np

from phase3.audit import audit_results, audit_wiring, verify_replay
from phase3.runner import evaluate_arm, state_hash, write_results


def test_replay_byte_identical(candidate, thr, eval_data, cfg):
    z, x = eval_data
    r1 = evaluate_arm(cfg, candidate, x, z, thr)
    r2 = evaluate_arm(cfg, candidate, x, z, thr)
    assert state_hash(r1) == state_hash(r2)


def test_verify_replay_function(cfg, candidate):
    assert verify_replay(cfg, candidate, seed=11, n_episodes=64) is True


def test_audit_wiring_consistency(cfg, candidate):
    w = audit_wiring(cfg, candidate)
    assert w["theta_le_a"] is True
    assert w["a_b_symmetric"] is True
    assert w["manifold"]["realizable_is_six"] is True
    assert w["parameter_counts"]["r4_total"] == 0


def test_write_and_audit_results_round_trip(cfg, candidate, thr, eval_data):
    from phase3.runner import evaluate_arm
    z, x = eval_data
    rows = [evaluate_arm(cfg, candidate, x, z, thr)]
    rows[0]["seed"] = 0
    rows[0]["n_episodes"] = len(z)
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "results_v1")
        written = write_results(out, cfg, rows, ["phase3/config.py"])
        assert os.path.exists(written["pre_run_snapshot.json"])
        aud = audit_results(out)
        assert aud["n_rows"] == 1
        assert aud["state_hash_matches"] is True
        # coverage re-derived from the saved table: only the candidate arm was
        # written, so the audit correctly flags the five missing arms per seed.
        assert aud["missing_arm_seed"] == {0: ["r1", "r2", "r3", "r4", "r5"]}


def test_state_hash_detects_change(cfg, candidate, thr, eval_data):
    z, x = eval_data
    r1 = evaluate_arm(cfg, candidate, x, z, thr)
    r2 = dict(r1)
    r2["probe_acc"] = float(r1["probe_acc"]) + 0.001
    assert state_hash(r1) != state_hash(r2)


def test_checkpoint_save_load_round_trip(cfg, candidate, thr, eval_data):
    """Checkpointing: saving and restoring an arm reproduces byte-identical rows."""
    from phase3.runner import save_checkpoint, load_checkpoint, evaluate_arm
    z, x = eval_data
    before = evaluate_arm(cfg, candidate, x, z, thr)
    with tempfile.TemporaryDirectory() as td:
        ck = os.path.join(td, "candidate.pt")
        save_checkpoint(candidate, ck)
        load_checkpoint(candidate, ck)
    after = evaluate_arm(cfg, candidate, x, z, thr)
    assert state_hash(before) == state_hash(after)
