"""Unit tests for AC104: one explicit internal spending rule -- budget reconstruction from
spendable material minus a declared decision-transition allowance (no CORRUPT_TICK).

Pins the mechanism at the unit-test level: the control identity (persistent == AC103 persistent),
the budget rule (a pure function of material and the declared allowance, with NO challenge-time
knowledge), the non-binding behaviour on healthy material, the load-bearing rescue on the marginal
seed, the declared allowance value, the observer-discard on the candidate, conservation, and the
recorded final outcomes (read from the frozen rows) as regressions.
"""
import inspect
import json
import unittest
from pathlib import Path
import numpy as np
import ac104
import ac103
import ac102
import ac95
import ac4
import ac5_program as prog


def setUpModule():
    # pin the module globals the study depends on (order-independence).
    ac104.ac12.PORTS = 4
    ac104.ac12.YIELD_M = 64
    ac104.ac12.YIELD_F = 64
    ac104.ac12.POST_YIELD_M = None
    ac104.ac12.POST_YIELD_F = None
    ac104.ac12.MOVE_KEYS = (1,)
    ac104.ac12.MOVE = 10**9
    ac104.ac12.DEV = ac104.DEV
    ac104.ac12.REGISTER_THRESHOLD = 4


class TestArmIdentity(unittest.TestCase):
    def test_persistent_is_ac103_persistent(self):
        # the control is byte-identical to AC103's persistent arm (the frozen reference).
        for seed in (0, 1):
            self.assertEqual(ac104.run(seed, 0, 'persistent')['state_hash'],
                             ac103.run(seed, 0, 'persistent')['state_hash'],
                             f'persistent != AC103 persistent on seed {seed}')

    def test_budget_nonbinding_on_healthy_seed(self):
        # on a healthy seed (material >> allowance + _cap) the budget never binds: byte-identical.
        self.assertEqual(ac104.run(0, 0, 'persistent_budget')['state_hash'],
                         ac104.run(0, 0, 'persistent')['state_hash'])


class TestBudgetRule(unittest.TestCase):
    def test_budget_rule_formula(self):
        # budget = max(0, material - allowance).
        self.assertEqual(ac104.budget_rule(100, 42), 58)
        self.assertEqual(ac104.budget_rule(42, 42), 0)
        self.assertEqual(ac104.budget_rule(10, 42), 0)
        self.assertEqual(ac104.budget_rule(65, 42), 23)

    def test_no_corrupt_tick_in_budget_maintain(self):
        # the operational budget code has NO challenge-time knowledge; the AC103 defer (the
        # contrast) DID reference CORRUPT_TICK. The precise check: the gate pattern
        # `now >= CORRUPT_TICK` (AC103's defer) is absent from the AC104 budget surgery and
        # present in AC103's; and the budget_rule itself is a pure function of (material,
        # allowance) with no CORRUPT_TICK reference.
        self.assertNotIn('CORRUPT_TICK', inspect.getsource(ac104.budget_rule))
        self.assertNotIn('now >= CORRUPT_TICK', inspect.getsource(ac104._build_budget_maintain))
        self.assertIn('now >= CORRUPT_TICK', inspect.getsource(ac103._build_persistent_maintain))

    def test_decision_allowance_is_streak_n_times_7(self):
        # the declared allowance = STREAK_N * 7 (the full relinquishment: STREAK_N-1 Gray
        # increments + the drop register write, each 7 replicas).
        self.assertEqual(ac104.DECISION_ALLOWANCE, ac104.STREAK_N * 7)
        self.assertEqual(ac104.DECISION_ALLOWANCE, 42)


class TestBudgetLoadBearing(unittest.TestCase):
    def test_budget_rescues_marginal_seed(self):
        # on the engineering marginal seed 1 (material 65 at the corruption tick) the control
        # dies (streak stalls, no relinquishment) and the budget rescues it (survives, relinq 2).
        ctl = ac104.run(1, 0, 'persistent')
        cand = ac104.run(1, 0, 'persistent_budget')
        self.assertFalse(ctl['completed'], 'control should die on the marginal seed')
        self.assertEqual(ctl['relinquishments'], 0)
        self.assertTrue(cand['completed'], 'budget should rescue the marginal seed')
        self.assertEqual(cand['relinquishments'], 2)
        self.assertEqual(cand['flipped_still_wrong'], 0)
        self.assertNotEqual(ctl['state_hash'], cand['state_hash'])

    def test_budget_rescues_ac103_marginal_seed(self):
        # the AC103 marginal seed 5603 (diagnostic): the control dies, the budget survives.
        for h in (0, 1):
            ctl = ac104.run(5603, h, 'persistent')
            cand = ac104.run(5603, h, 'persistent_budget')
            self.assertFalse(ctl['completed'], f'control should die on 5603/{h}')
            self.assertTrue(cand['completed'], f'budget should rescue 5603/{h}')
            self.assertEqual(cand['relinquishments'], 2)


class TestObserverDiscard(unittest.TestCase):
    def test_observer_discard_on_candidate(self):
        # per-tick observer-discard on the CANDIDATE is byte-identical (state sufficiency).
        for seed in (0, 1):
            od = ac104.observer_discard_equivalence(seed, 0, 'persistent_budget')
            self.assertNotEqual(od.get('status'), 'no_mid_streak', f'no mid-streak on seed {seed}')
            self.assertTrue(od.get('swap_applied'))
            self.assertTrue(od.get('per_tick_identical'), f'not per-tick identical on {seed}')
            self.assertTrue(od.get('terminal_identical'))


class TestConservation(unittest.TestCase):
    def test_balance_holds_in_step(self):
        # ac4.balance asserts hold in-step for both arms on a sample seed.
        for arm in ac104.ARMS:
            ac104.run(2, 0, arm)   # raises if a within-step balance assert fails


class TestRecordedFinals(unittest.TestCase):
    @classmethod
    def _rows(cls):
        return [json.loads(l) for l in
                (Path('ac104_results_v1') / 'rows.jsonl').read_text().splitlines()]

    def test_final_sample_all_survive_under_both_arms(self):
        # the fresh final sample (5700-5707) contains no seed where the control dies, so the
        # rescue did not recur; every individual survives under both arms (recorded regression,
        # read from the frozen rows).
        by = {}
        for r in self._rows():
            by.setdefault((r['seed'], r['history']), {})[r['arm']] = r
        n_rescue = 0
        for seed in ac104.FINAL_SEEDS:
            for h in (0, 1):
                ctl = by[(seed, h)]['persistent']
                cand = by[(seed, h)]['persistent_budget']
                self.assertTrue(ctl['completed'], f'control died on {seed}/{h}')
                self.assertTrue(cand['completed'], f'candidate died on {seed}/{h}')
                self.assertEqual(cand['flipped_still_wrong'], 0)
                self.assertEqual(cand['relinquishments'], ctl['relinquishments'])
                if not ctl['completed'] and cand['completed']:
                    n_rescue += 1
        # the honest record: no rescue on the fresh sample (it contains no marginal seed)
        self.assertEqual(n_rescue, 0)

    def test_seed_5702_relinquishes_once(self):
        # the closest-to-marginal final seed (material 66) relinquishes once under BOTH arms
        # (recorded: the budget neither rescues nor harms it).
        by = {}
        for r in self._rows():
            by.setdefault((r['seed'], r['history']), {})[r['arm']] = r
        for h in (0, 1):
            self.assertEqual(by[(5702, h)]['persistent']['relinquishments'], 1)
            self.assertEqual(by[(5702, h)]['persistent_budget']['relinquishments'], 1)


if __name__ == '__main__':
    unittest.main()
