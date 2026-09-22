"""Unit tests for AC105: the operating range of the frozen persistent-trigger + allowance-42
architecture.

Pins the mechanism at the unit-test level: the baseline identity (both arms == AC104 at `simult`),
the budget rule (a pure function of material and the declared allowance, with NO challenge-time
knowledge), the declared allowance value, the condition grid (5 conditions, corruption + >= 2 moves
each, baseline == ac100.SCHEDULE), the load-bearing rescue on the diagnostic marginal seeds, the
late-corruption reconstruction-harm boundary (5603), conservation, and the recorded final outcomes
(read from the frozen rows) as regressions.
"""
import inspect
import json
import unittest
from pathlib import Path
import numpy as np
import ac105
import ac104
import ac103
import ac100
import ac95
import ac4
import ac5_program as prog


def setUpModule():
    # pin the module globals the study depends on (order-independence).
    ac105.ac12.PORTS = 4
    ac105.ac12.YIELD_M = 64
    ac105.ac12.YIELD_F = 64
    ac105.ac12.POST_YIELD_M = None
    ac105.ac12.POST_YIELD_F = None
    ac105.ac12.MOVE_KEYS = (1,)
    ac105.ac12.MOVE = 10**9
    ac105.ac12.DEV = ac105.DEV
    ac105.ac12.REGISTER_THRESHOLD = 4


class TestArmIdentity(unittest.TestCase):
    def test_baseline_identity_both_arms(self):
        # at `simult` both arms are byte-identical to AC104 (the single-change license).
        for seed in (0, 1, 2):
            self.assertEqual(ac105.run(seed, 0, 'persistent', 'simult')['state_hash'],
                             ac104.run(seed, 0, 'persistent')['state_hash'],
                             f'persistent != AC104 persistent on seed {seed}')
            self.assertEqual(ac105.run(seed, 0, 'persistent_budget', 'simult')['state_hash'],
                             ac104.run(seed, 0, 'persistent_budget')['state_hash'],
                             f'persistent_budget != AC104 persistent_budget on seed {seed}')


class TestBudgetRule(unittest.TestCase):
    def test_budget_rule_formula(self):
        self.assertEqual(ac105.budget_rule(100, 42), 58)
        self.assertEqual(ac105.budget_rule(42, 42), 0)
        self.assertEqual(ac105.budget_rule(10, 42), 0)
        self.assertEqual(ac105.budget_rule(65, 42), 23)

    def test_no_challenge_time_knowledge(self):
        # the operational budget code has NO challenge-time knowledge: the budget rule is a pure
        # function of (material, allowance); the AC104 budget surgery has no CORRUPT_TICK gate; the
        # AC103 defer (the contrast) DID reference CORRUPT_TICK.
        self.assertNotIn('CORRUPT_TICK', inspect.getsource(ac105.budget_rule))
        self.assertNotIn('now >= CORRUPT_TICK', inspect.getsource(ac104._build_budget_maintain))
        self.assertIn('now >= CORRUPT_TICK', inspect.getsource(ac103._build_persistent_maintain))

    def test_decision_allowance_is_streak_n_times_7(self):
        self.assertEqual(ac105.DECISION_ALLOWANCE, ac105.STREAK_N * 7)
        self.assertEqual(ac105.DECISION_ALLOWANCE, 42)


class TestConditions(unittest.TestCase):
    def test_five_conditions_predeclared(self):
        self.assertEqual(list(ac105.CONDITIONS),
                         ['simult', 'simult3', 'corrupt_first', 'move_first', 'late'])

    def test_baseline_reproduces_ac100_schedule(self):
        corrupt_tick, schedule = ac105.CONDITIONS['simult']
        self.assertEqual(corrupt_tick, ac105.CORRUPT_TICK)
        self.assertEqual(schedule, ac100.SCHEDULE)

    def test_every_condition_has_corruption_and_two_plus_moves(self):
        for cond, (ct, schedule) in ac105.CONDITIONS.items():
            self.assertIsInstance(ct, int)
            self.assertGreaterEqual(len(schedule), 2, f'{cond} has < 2 moves')

    def test_repeated_move_condition(self):
        # simult3 is the repeated-move condition (three moves).
        _, schedule = ac105.CONDITIONS['simult3']
        self.assertEqual(len(schedule), 3)
        self.assertEqual(len(ac105.move_ticks(schedule)), 3)


class TestLoadBearingRescue(unittest.TestCase):
    def test_rescue_marginal_seed_1(self):
        # on the engineering marginal seed 1 (priority (0,1,3,2), mat 65 at corruption) the control
        # dies and the budget rescues it, at `simult` and `simult3`.
        for cond in ('simult', 'simult3'):
            ctl = ac105.run(1, 0, 'persistent', cond)
            cand = ac105.run(1, 0, 'persistent_budget', cond)
            self.assertFalse(ctl['completed'], f'control should die on seed 1/{cond}')
            self.assertTrue(cand['completed'], f'budget should rescue seed 1/{cond}')
            self.assertEqual(cand['flipped_still_wrong'], 0)

    def test_rescue_marginal_seed_5603(self):
        # the AC104 marginal seed 5603 (priority (1,2,3,0)).
        for cond in ('simult', 'simult3'):
            for h in (0, 1):
                ctl = ac105.run(5603, h, 'persistent', cond)
                cand = ac105.run(5603, h, 'persistent_budget', cond)
                self.assertFalse(ctl['completed'], f'control should die on 5603/{h}/{cond}')
                self.assertTrue(cand['completed'], f'budget should rescue 5603/{h}/{cond}')

    def test_late_boundary_reconstruction_harm(self):
        # under `late`, 5603 dies under BOTH arms, but the candidate fails to reconstruct
        # (fw > 0) where the control recovered (fw == 0) -- the recorded reconstruction-level harm.
        ctl = ac105.run(5603, 0, 'persistent', 'late')
        cand = ac105.run(5603, 0, 'persistent_budget', 'late')
        self.assertFalse(ctl['completed'])
        self.assertFalse(cand['completed'])
        self.assertEqual(ctl['flipped_still_wrong'], 0)
        self.assertGreater(cand['flipped_still_wrong'], 0)


class TestConservation(unittest.TestCase):
    def test_balance_holds_in_step(self):
        # ac4.balance asserts hold in-step for both arms on a sample seed/condition.
        for arm in ac105.ARMS:
            for cond in ('simult', 'late'):
                ac105.run(2, 0, arm, cond)   # raises if a within-step balance assert fails


class TestRecordedFinals(unittest.TestCase):
    @classmethod
    def _rows(cls):
        return [json.loads(l) for l in
                (Path('ac105_results_v1') / 'rows.jsonl').read_text().splitlines()]

    @classmethod
    def _by(cls):
        by = {}
        for r in cls._rows():
            by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
        return by

    def test_all_six_gates_pass(self):
        res = json.loads((Path('ac105_results_v1') / 'results.json').read_text())
        for k in ('G1_control_identity', 'G2_candidate_reconstructs_all_conditions',
                  'G3_no_harm_survival', 'G4_no_harm_relinquishment',
                  'G5_state_sufficiency_observer_discard_candidate',
                  'G6_completeness_determinism'):
            self.assertTrue(res['gates'][k], f'gate {k} should pass')

    def test_rescue_new_marginal_priority_5804(self):
        # the untouched finals contain a fresh marginal economy (5804, priority (0,3,2,1), mat 71)
        # where the control dies and the budget rescues it -- a NEW priority, distinct from the
        # AC104 diagnostics (1,2,3,0) and (0,1,3,2).
        by = self._by()
        for cond in ('simult', 'simult3'):
            for h in (0, 1):
                ctl = by[(5804, h, cond)]['persistent']
                cand = by[(5804, h, cond)]['persistent_budget']
                self.assertFalse(ctl['completed'], f'control should die 5804/{h}/{cond}')
                self.assertTrue(cand['completed'], f'budget should rescue 5804/{h}/{cond}')
                self.assertEqual(cand['flipped_still_wrong'], 0)

    def test_move_first_both_die_5802(self):
        # under move_first, 5802 dies under BOTH arms (re-acquisition fails after the 2nd move,
        # fw==0 both) -- an operating-range boundary that is not budget-specific (recorded).
        by = self._by()
        for h in (0, 1):
            ctl = by[(5802, h, 'move_first')]['persistent']
            cand = by[(5802, h, 'move_first')]['persistent_budget']
            self.assertFalse(ctl['completed'])
            self.assertFalse(cand['completed'])
            self.assertEqual(ctl['flipped_still_wrong'], 0)
            self.assertEqual(cand['flipped_still_wrong'], 0)

    def test_late_relinquishment_improvement(self):
        # under `late` (corruption coincides with the 2nd move), the control relinquishes only the
        # 1st move while the budget relinquishes both, on three final seeds (recorded).
        by = self._by()
        for seed in (5800, 5805, 5806):
            for h in (0, 1):
                ctl = by[(seed, h, 'late')]['persistent']
                cand = by[(seed, h, 'late')]['persistent_budget']
                self.assertEqual(ctl['relinquishments_by_move'], [1, 0], f'{seed}/{h}/late ctl')
                self.assertEqual(cand['relinquishments_by_move'], [1, 1], f'{seed}/{h}/late cand')

    def test_no_reconstruction_harm_on_finals(self):
        # no final individual has the candidate failing to reconstruct where the control recovered
        # (the 5603-late boundary was diagnostic-only).
        by = self._by()
        for (seed, h, cond) in by:
            ctl = by[(seed, h, cond)]['persistent']
            cand = by[(seed, h, cond)]['persistent_budget']
            if cand['flipped_still_wrong'] > 0:
                self.assertGreater(ctl['flipped_still_wrong'], 0,
                                   f'{seed}/{h}/{cond}: cand fw>0 where ctl fw==0')


if __name__ == '__main__':
    unittest.main()
