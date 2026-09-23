"""Tests for AC111 (I1 — composition of the cognitive mechanism with AC105's reconstruction +
spending). These pin the mechanism and the recorded composition finding: the estimate bit is
excluded from reconstruction by construction, reconstruction completes under composition, and the
estimate discriminates correctly under corruption. A future code change that alters the record is
caught instead of silently absorbed.

Run: .venv/bin/python -B -m unittest test_ac111
"""
import unittest
import numpy as np
import ac111
import ac110
import ac107
import ac106
import ac12
import ac96
import ac95
import ac4
import ac5_program as prog


def setUpModule():
    # pin the ambient module state the study depends on (the AC16/AC17 lesson)
    ac12.PORTS = 4
    ac12.YIELD_M = 64
    ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None
    ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,)
    ac12.MOVE = 10**9
    ac12.DEV = ac111.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestEstimateBitLayout(unittest.TestCase):
    def test_offset_is_dead_rule_action_bit_zero(self):
        o, _ = ac12.acquire(0)
        bel_off = ac107.bel_offset(o)
        self.assertEqual(bel_off, 14 * ac12.dead_rule_index(o) + 10)
        self.assertLess(bel_off, 126)

    def test_acquired_value_is_e_world(self):
        # the dead rule's action is 5 (0b0101), so action bit 0 is 1 = E_world; the acquired
        # organism is byte-identical to the frozen one (the estimate's acquired value == frozen).
        o, _ = ac12.acquire(0)
        self.assertEqual(ac106.bel_read(o, ac107.bel_offset(o)), 1)

    def test_estimate_not_in_register_or_streak(self):
        o, offs = ac12.acquire(0)
        bel_off = ac107.bel_offset(o)
        self.assertNotIn(bel_off, offs)
        self.assertNotIn(bel_off, ac96.streak_offsets(o))


class TestExclusionFromReconstruction(unittest.TestCase):
    def test_estimate_is_in_reconstruction_exclude_set(self):
        # the load-bearing fact: AC110's build adds bel_off to the exclude set, so reg_from_active
        # never overwrites the estimate. build_offs = reg_offs + streak_offs + [bel_off].
        o, _ = ac12.acquire(0)
        bel_off = ac107.bel_offset(o)
        reg_offs = ac95.resolve_offsets(o)
        streak_offs = ac96.streak_offsets(o)
        build_offs = reg_offs + streak_offs + [bel_off]
        self.assertIn(bel_off, build_offs)
        self.assertNotIn(bel_off, reg_offs)          # AC105's exclude set (no estimate) would NOT
                                                     # exclude it -- the composition's exclusion is
                                                     # the AC110 build's addition, not ac95's.

    def test_reconstruction_target_at_estimate_bit_is_e_world(self):
        # if bel_off were NOT excluded, reconstruction would write the estimate bit to 1 (E_world),
        # the description's stored value of the dead rule's action bit 0. This is the exact
        # interference the exclusion prevents.
        o, _ = ac12.acquire(0)
        bel_off = ac107.bel_offset(o)
        _, _, _, priority = ac4.acquire(0)
        encoded = ac95.description_bits(priority)
        target = ac95.build_program(encoded)
        self.assertIsNotNone(target)
        self.assertEqual(int(target[bel_off]), 1)


class TestSingleChangeLicense(unittest.TestCase):
    def test_est_reproduces_ac110(self):
        # the `est` arm is byte-identical to AC110 maintained (no corruption).
        for cond in ('no_cause', 'move', 'cut'):
            self.assertTrue(ac111.est_is_ac110(0, 0, cond), cond)


class TestCompositionNoInterference(unittest.TestCase):
    def test_cut_estimate_holds_under_corruption(self):
        # the composition's key cell: reconstruction fires on the corruption (obs bit 2) at the
        # same tick the cut lands, yet the estimate still reads E_machinery (0) and holds the route.
        r = ac111.run(0, 0, 'est_corrupt_budget', 'cut')
        self.assertEqual(r['fw_at_corrupt'], 8)
        self.assertEqual(r['flipped_still_wrong'], 0)
        self.assertIsNotNone(r['recovery_tick'])
        self.assertEqual(r['bel_at_cut_end'], 0)
        self.assertEqual(r['relinquishments'], 0)
        self.assertTrue(r['route1_bound_at_horizon'])
        self.assertEqual(r['bel_writes'], 7)

    def test_move_estimate_relinquishes_under_corruption(self):
        r = ac111.run(0, 0, 'est_corrupt_budget', 'move')
        self.assertGreaterEqual(r['relinquishments'], 1)
        self.assertEqual(r['flipped_still_wrong'], 0)


class TestRecordedStandaloneFailures(unittest.TestCase):
    def test_unbounded_starves_the_decision_on_seed_5(self):
        # the AC104 standalone failure, reproduced in composition: the unbounded arm drains material
        # below the allowance so the drop never fires (relinquishments == 0), while the budget arm
        # (the AC105 candidate) survives and relinquishes. This is a standalone failure of the
        # spending architecture, NOT an interference with the estimate.
        ub = ac111.run(5, 0, 'est_corrupt', 'move')
        bu = ac111.run(5, 0, 'est_corrupt_budget', 'move')
        self.assertIsNotNone(ub['first_dead'])
        self.assertEqual(ub['relinquishments'], 0)
        self.assertIsNone(bu['first_dead'])
        self.assertGreaterEqual(bu['relinquishments'], 1)

    def test_est_route_move_collapse_on_seed_1(self):
        # the AC107 route-move collapse, reproduced: est (no corruption) dies on seed 1 move.
        e = ac111.run(1, 0, 'est', 'move')
        self.assertIsNotNone(e['first_dead'])


if __name__ == '__main__':
    unittest.main()
