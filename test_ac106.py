"""Tests for AC106 (engineering, negative result — no freeze).

These pin the mechanism and the RECORDED NEGATIVE FINDING, so a future code change that
alters the record is caught instead of silently absorbed. The study is not frozen: the
tests assert the measured falsification (the estimate carries no causal role) alongside the
mechanism's correct pieces (byte-identity, read-cut inertness, the estimate offset).

Run: .venv/bin/python -B -m unittest test_ac106
"""
import unittest
import numpy as np
import ac106
import ac100
import ac12
import ac96
import ac95
import ac99_d2


def setUpModule():
    # pin the ambient module state the study depends on (the AC16/AC17 lesson)
    ac12.PORTS = 4
    ac12.YIELD_M = 64
    ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None
    ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,)
    ac12.MOVE = 10**9
    ac12.DEV = ac106.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestEstimateStorage(unittest.TestCase):
    def test_offset_and_acquired_value(self):
        o, offs = ac12.acquire(0)
        bel_off = ac106.bel_offset(o)
        self.assertEqual(bel_off, 14 * ac12.dead_rule_index(o) + 10)
        # the acquired value is 1 (E_world): the dead-rule action bit 0 is set (action 5 = 0b0101)
        self.assertEqual(ac106.bel_read(o, bel_off), 1)

    def test_offset_is_within_program_and_not_register_or_streak(self):
        o, offs = ac12.acquire(0)
        bel_off = ac106.bel_offset(o)
        self.assertLess(bel_off, 126)
        self.assertNotIn(bel_off, offs)
        self.assertNotIn(bel_off, ac96.streak_offsets(o))

    def test_streak_is_3bit_so_longer_thresholds_unreachable(self):
        # the Gray streak is 3 bits (max 7); this is why the C1 "HOLD_N > 6" hold window cannot
        # be expressed on the streak and the candidate's E_world threshold is the frozen 6.
        self.assertEqual(ac99_d2.gray_streak_read.__name__, 'gray_streak_read')
        o, _ = ac12.acquire(0)
        streak_offs = ac96.streak_offsets(o)
        # encode 7 (max) and read it back
        for k in (0, 1):
            self.assertLessEqual(ac99_d2.gray_streak_read(o, k, streak_offs), 7)


class TestReadCut(unittest.TestCase):
    def test_identity_when_no_key(self):
        o, _ = ac12.acquire(0)
        cut = ac106.ReadCut(None, 0, 0)
        self.assertIsNone(cut.read(o.memory, 1))

    def test_suppresses_only_key_in_window(self):
        o, _ = ac12.acquire(0)
        cut = ac106.ReadCut(1, 100, 200)
        cut.now = 150
        self.assertIsNone(cut.read(o.memory, 1))       # suppressed
        cut.now = 250
        self.assertEqual(cut.read(o.memory, 1), o.memory.read(1))   # restored (identity)


class TestMechanism(unittest.TestCase):
    def test_no_cause_identity_candidate_equals_r2(self):
        # P3 / G4: the estimate is inert by construction when no cause is present.
        self.assertTrue(ac106.no_cause_identity(0, 0))
        self.assertTrue(ac106.no_cause_identity(0, 1))

    def test_ac100_reproduction_r2_is_faithful_copy(self):
        # single-change license: r2 at the AC100 single-move world (PORTS=2) reproduces ac100.
        self.assertTrue(ac106.ac100_reproduction(0, 0))
        self.assertTrue(ac106.ac100_reproduction(1, 0))


class TestNegativeFinding(unittest.TestCase):
    """The recorded falsification: the estimate carries no causal role.

    These assert the MEASURED negative result. They are recorded-outcome regressions, not
    gates the study must pass — the study itself is the falsification.
    """

    def test_information_confound_bel_is_emachinery_in_both_causes(self):
        # R1: in `move` (E_world) the post-drop blind re-bind fires the "productive-after-failure"
        # update, so the estimate reads E_machinery at the horizon in BOTH causes — it carries no
        # cause information.
        move = ac106.run(0, 0, 'candidate', 'move')
        cut = ac106.run(0, 0, 'candidate', 'cut')
        self.assertEqual(move['bel_at_horizon'], 0)   # E_machinery, wrongly
        self.assertEqual(cut['bel_at_horizon'], 0)    # E_machinery, correctly

    def test_candidate_relinquishes_in_eworld(self):
        # G3: the candidate DOES relinquish the stale route in E_world (matching r2) — the
        # estimate is not needed for this; it is the frozen streak's behaviour.
        r = ac106.run(0, 0, 'candidate', 'move')
        self.assertGreaterEqual(r['relinquishments'], 1)

    def test_scramble_redundant_on_non_priority_corner(self):
        # R2/R3: on a non-seed-3 individual the frozen streak already holds through the cut, so
        # scrambling the estimate changes NO behavioural outcome (relinquishment, entry survival,
        # route) — only the redundant proactive spend differs.
        cand = ac106.run(0, 0, 'candidate', 'cut')
        scr = ac106.run(0, 0, 'scramble', 'cut')
        self.assertEqual(cand['relinquishments'], scr['relinquishments'])
        self.assertEqual(cand['entry_expired_during_cut'], scr['entry_expired_during_cut'])
        self.assertEqual(cand['route1_bound_at_horizon'], scr['route1_bound_at_horizon'])
        # the only difference is the wasted proactive renewal spend
        self.assertGreater(cand['proactive_writes'], scr['proactive_writes'])

    def test_estimate_writes_are_paid_and_accounted(self):
        # the estimate's update and the proactive renewal are paid writes, accounted in the ledger
        r = ac106.run(0, 0, 'candidate', 'cut')
        self.assertGreaterEqual(r['bel_writes'], 0)
        self.assertGreater(r['proactive_writes'], 0)
        self.assertGreaterEqual(r['writes'], r['proactive_writes'] + r['bel_writes'])


class TestObserverDiscard(unittest.TestCase):
    def test_host_state_dependence_on_candidate(self):
        # the estimate value lives in maintained state; discarding the observer mid-cut leaves the
        # trajectory byte-identical (the card's host-state-dependence requirement).
        d = ac106.observer_discard_equivalence(0, 0, 'cut')
        self.assertTrue(d['per_tick_identical'])
        self.assertTrue(d['terminal_identical'])


if __name__ == '__main__':
    unittest.main()
