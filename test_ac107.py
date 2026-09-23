"""Tests for AC107 (K5, engineering — the minimal cause-estimator with credible rivals).

These pin the mechanism and the RECORDED engineering finding, so a future code change that alters
the record is caught instead of silently absorbed. AC107 is engineering-only (no freeze): the tests
assert the measured result (the estimator discriminates and the two-sided discriminator is
survival-relevant) alongside the mechanism's correctness (byte-identity, read-cut inertness, the
estimate offset, rival distinctness, state sufficiency).

Run: .venv/bin/python -B -m unittest test_ac107
"""
import unittest
import numpy as np
import ac107
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
    ac12.DEV = ac107.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestEstimateStorage(unittest.TestCase):
    def test_offset_and_acquired_value(self):
        o, offs = ac12.acquire(0)
        bel_off = ac106.bel_offset(o)
        self.assertEqual(bel_off, 14 * ac12.dead_rule_index(o) + 10)
        # acquired value is 1 (E_world): dead-rule action bit 0 is set (action 5 = 0b0101)
        self.assertEqual(ac106.bel_read(o, bel_off), 1)

    def test_offset_is_within_program_and_not_register_or_streak(self):
        o, offs = ac12.acquire(0)
        bel_off = ac106.bel_offset(o)
        self.assertLess(bel_off, 126)
        self.assertNotIn(bel_off, offs)
        self.assertNotIn(bel_off, ac96.streak_offsets(o))


class TestRivalDistinctness(unittest.TestCase):
    def test_hold_n_defect_fixed(self):
        # K1 P1: r4's threshold is genuinely longer than the 3-bit Gray streak's maximum (7).
        self.assertGreater(ac107.HOLD_N, 7)
        self.assertNotEqual(ac107.HOLD_N, ac107.STREAK_N)

    def test_r4_has_own_counter_not_the_streak(self):
        # r4 uses a per-key host-integer counter, not the saturating Gray streak.
        alloc = ac107.LongCounterAlloc(0, 0)
        self.assertIsInstance(alloc.fail_count, dict)
        self.assertEqual(set(alloc.fail_count), {0, 1})


class TestMechanism(unittest.TestCase):
    def test_no_cause_identity_candidate_equals_r2(self):
        # P3: the estimate is inert by construction when no cause is present.
        self.assertTrue(ac107.no_cause_identity(0, 0))
        self.assertTrue(ac107.no_cause_identity(0, 1))

    def test_ac100_reproduction_r2_is_faithful_copy(self):
        # single-change license: r2 at the AC100 single-move world (PORTS=2) reproduces ac100.
        self.assertTrue(ac107.ac100_reproduction(0, 0))
        self.assertTrue(ac107.ac100_reproduction(1, 0))

    def test_read_cut_is_imported_and_inert_at_zero_window(self):
        # the read-cut is the ac106 primitive; a zero window is the identity.
        o, _ = ac12.acquire(0)
        cut = ac107.ReadCut(None, 0, 0)
        self.assertIsNone(cut.read(o.memory, 1))


class TestDiscrimination(unittest.TestCase):
    def test_discriminator_reads_cause_correctly(self):
        # M1: e reads E_machinery (0) in `cut`, E_world (1) in `move`, at decision times, with
        # zero post-intervention mistakes on seed 0.
        cut = ac107.run(0, 0, 'candidate', 'cut')
        move = ac107.run(0, 0, 'candidate', 'move')
        self.assertEqual(cut['bel_at_cut_end'], 0)
        self.assertEqual(move['bel_at_first_drop'], 1)
        self.assertEqual(move['bel_at_horizon'], 1)
        self.assertEqual(cut['mistakes'], 0)
        self.assertEqual(move['mistakes'], 0)

    def test_holds_in_cut_relinquishes_in_move(self):
        # the two consumptions: hold in E_machinery, relinquish in E_world.
        cut = ac107.run(0, 0, 'candidate', 'cut')
        move = ac107.run(0, 0, 'candidate', 'move')
        self.assertEqual(cut['relinquishments'], 0)
        self.assertGreaterEqual(move['relinquishments'], 1)


class TestTwoSidedDiscriminator(unittest.TestCase):
    """The recorded engineering finding (survival contrast), on the discriminator seeds."""

    def test_candidate_survives_cut_where_r2_dies(self):
        # seed 4 cut: r2 (threshold 6) relinquishes a valid route and dies; the candidate holds.
        cand = ac107.run(4, 0, 'candidate', 'cut')
        r2 = ac107.run(4, 0, 'r2', 'cut')
        self.assertIsNone(cand['first_dead'])
        self.assertEqual(cand['relinquishments'], 0)
        self.assertIsNotNone(r2['first_dead'])
        self.assertGreaterEqual(r2['relinquishments'], 1)

    def test_candidate_survives_move_where_r4_dies(self):
        # seed 1 move: r4 (threshold 24) holds the stale route too long and dies; the candidate
        # drops at 6 and survives.
        cand = ac107.run(1, 0, 'candidate', 'move')
        r4 = ac107.run(1, 0, 'r4', 'move')
        self.assertIsNone(cand['first_dead'])
        self.assertGreaterEqual(cand['relinquishments'], 1)
        self.assertIsNotNone(r4['first_dead'])

    def test_scramble_read_only_dies_in_cut(self):
        # P4: the read-only scramble (read forced E_world, writes NOT suppressed) relinquishes and
        # dies on seed 4 cut, where the candidate holds and survives.
        cand = ac107.run(4, 0, 'candidate', 'cut')
        scr = ac107.run(4, 0, 'scramble', 'cut')
        self.assertIsNone(cand['first_dead'])
        self.assertIsNotNone(scr['first_dead'])
        # the K1 P5 fix: the scramble still WRITES (maintains) the estimate bit -- it is not a
        # suppressed-write control (AC106's three-way confound).
        self.assertGreaterEqual(scr['bel_attempts'], 1)
        self.assertGreaterEqual(scr['bel_writes'], 7)

    def test_scramble_spend_matches_on_hold_individual(self):
        # on a hold-individual (seed 0, where the forced read does not change the trajectory) the
        # scramble's estimate-maintenance spend matches the candidate's exactly.
        cand = ac107.run(0, 0, 'candidate', 'cut')
        scr = ac107.run(0, 0, 'scramble', 'cut')
        self.assertEqual(cand['relinquishments'], scr['relinquishments'])  # both hold on seed 0
        self.assertEqual(cand['bel_writes'], scr['bel_writes'])


class TestAttemptTracking(unittest.TestCase):
    def test_completed_writes_separate_from_attempts(self):
        # the estimate bit flips 1->0 exactly once in the cut (7 replicas, 1 attempt, 0 refused).
        cut = ac107.run(0, 0, 'candidate', 'cut')
        self.assertEqual(cut['bel_writes'], 7)
        self.assertEqual(cut['bel_attempts'], 1)
        self.assertEqual(cut['bel_refused'], 0)


class TestObserverDiscard(unittest.TestCase):
    def test_host_state_dependence_on_candidate(self):
        # the estimate value lives in maintained state; discarding the observer mid-cut leaves the
        # trajectory byte-identical (state sufficiency).
        d = ac107.observer_discard_equivalence(0, 0, 'cut')
        self.assertTrue(d['per_tick_identical'])
        self.assertTrue(d['terminal_identical'])


if __name__ == '__main__':
    unittest.main()
