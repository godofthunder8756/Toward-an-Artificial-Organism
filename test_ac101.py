"""AC101 tests: the composition test (gray_ctl + the corruption challenge + two route reversals).

Pins, at the single-step and recorded-outcome level:
- the schedule is AC100's two-move schedule (the corruption is the only new parameter);
- the corrupt=False arm identity (gray_ctl reproduces ac100's gray_ctl byte-for-byte, so corrupt is
  the ONLY change);
- the engineering screen's recorded outcomes (the seed-1 composition interaction: reconstruction +
  description intact but death at 8408; the seeds-6/7 passive first-move adaptation);
- the recorded finals outcomes (gates G1-G6, per-strata), re-derived from results.json;
- the per-tick observer-discard on gray_ctl under the combined challenge (state sufficiency);
- conservation (ac4.balance asserts run in-step, so a run that violated a law would raise).

Not hashed (AC17's rule) -- verification tool only.
"""
import unittest
from pathlib import Path
import json
import numpy as np
import ac4
import ac9
import ac12
import ac95
import ac96
import ac99_d2
import ac100
import ac101


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac95.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def prio(seed):
    rng = np.random.default_rng([seed, 1004])
    return list(map(int, rng.permutation(4)))


class TestScheduleAndIdentity(unittest.TestCase):
    """The corruption is the ONLY new parameter: the schedule is AC100's, and corrupt=False
    reproduces ac100's gray_ctl byte-for-byte."""

    def test_schedule_is_ac100(self):
        self.assertEqual(ac101.SCHEDULE, ac100.SCHEDULE)

    def test_corrupt_false_is_ac100_gray_ctl(self):
        for seed in (0, 1, 4444, 4448):
            for h in (0, 1):
                got = ac101.run(seed, h, corrupt=False)
                want = ac100.run(seed, h, 'gray_ctl', schedule=ac100.SCHEDULE)
                self.assertEqual(got['state_hash'], want['state_hash'],
                                 f'{seed}/{h}: corrupt=False not byte-identical to ac100 gray_ctl')


class TestEngineeringRecordedOutcomes(unittest.TestCase):
    """The engineering screen (seeds 0-7, gray_ctl + corrupt=True), pinned from the saved rows."""

    @classmethod
    def setUpClass(cls):
        cls.rows = {r['seed'] * 2 + r['history']: r
                    for r in [json.loads(l) for l in
                              Path('ac101_engineering_v1/rows.jsonl').read_text().splitlines()]}

    def test_internal_state_composition_unconditional(self):
        # fw 8->0, description intact (at death or horizon), >=1 succession, on EVERY individual
        for key, r in self.rows.items():
            self.assertEqual(r['fw_at_corrupt'], 8, f'{key}: corruption not applied')
            self.assertEqual(r['flipped_still_wrong'], 0, f'{key}: corruption not recovered')
            self.assertTrue(r['description_correct'] == 130
                            or r['description_correct_at_death'] == 130,
                            f'{key}: description not intact')
            self.assertGreaterEqual(r['successions'], 1, f'{key}: no recipe turnover')

    def test_seed_1_composition_interaction(self):
        # seed 1 (priority [0,1,3,2]) dies at 8408 with reconstruction complete and the
        # description intact at death -- the composition interaction, not a reconstruction failure.
        for h in (0, 1):
            r = self.rows[1 * 2 + h]
            self.assertFalse(r['completed'], f'1/{h}: seed 1 survived (record moved)')
            self.assertEqual(r['first_dead'], 8408, f'1/{h}: death tick moved')
            self.assertEqual(r['flipped_still_wrong'], 0, f'1/{h}: reconstruction did not complete')
            self.assertEqual(r['description_correct_at_death'], 130,
                             f'1/{h}: description not intact at death')
            self.assertEqual(r['relinquishments_by_move'], [0, 0], f'1/{h}: relinq moved')
            self.assertEqual(r['reacquisitions_by_move'], [0, 0], f'1/{h}: reacq moved')
            self.assertEqual(r['streak_final']['1'], 4, f'1/{h}: streak not stalled at 4')

    def test_seeds_6_7_passive_first_move(self):
        # seeds 6 (priority [0,1,2,3]) and 7 (adversarial [3,0,2,1]) survive but adapt the first
        # move PASSIVELY (expiry), actively relinquishing only the second move.
        for s in (6, 7):
            for h in (0, 1):
                r = self.rows[s * 2 + h]
                self.assertTrue(r['completed'], f'{s}/{h}: did not survive')
                self.assertEqual(r['relinquishments_by_move'], [0, 1],
                                 f'{s}/{h}: relinq not passive-then-active')
                self.assertEqual(r['reacquisitions_by_move'], [1, 1],
                                 f'{s}/{h}: did not reacquire at every move')

    def test_adversarial_engineering_survives(self):
        # the adversarial-priority engineering seeds (4, 7) both survive under the challenge
        for s in (4, 7):
            self.assertEqual(prio(s), [3, 0, 2, 1], f'{s}: not adversarial priority')
            for h in (0, 1):
                self.assertTrue(self.rows[s * 2 + h]['completed'], f'{s}/{h}: adversarial died')

    def test_engineering_arm_identity_and_discard(self):
        res = json.loads(Path('ac101_engineering_v1/results.json').read_text())
        self.assertTrue(all(res['arm_identity'].values()), 'arm identity not all True')
        obs = res['observer_discard']
        self.assertTrue(all(d.get('status') != 'no_mid_streak' and d.get('per_tick_identical')
                            for d in obs.values()), 'observer-discard not all per-tick identical')


class TestFinals(unittest.TestCase):
    """AC101 finals: pins the RECORDED result -- the gates and the per-strata outcomes."""

    @classmethod
    def setUpClass(cls):
        cls.results = json.loads(Path('ac101_results_v1/results.json').read_text())
        cls.rows = {r['seed'] * 2 + r['history']: r for r in cls.results['rows']}

    def test_strata(self):
        self.assertEqual(self.results['unseen'], [4448, 4449, 4450, 4451])
        self.assertEqual(self.results['adversarial'], [4466, 4481, 4504, 4510])
        for s in self.results['adversarial']:
            self.assertEqual(prio(s), [3, 0, 2, 1], f'{s}: not adversarial priority')
        for s in self.results['unseen']:
            self.assertNotEqual(prio(s), [3, 0, 2, 1], f'{s}: unseen seed has adversarial priority')

    def test_row_count_and_seeds(self):
        self.assertEqual(self.results['seeds'], [4448, 4449, 4450, 4451, 4466, 4481, 4504, 4510])
        self.assertEqual(len(self.results['rows']), 8 * 2)

    def test_recorded_gates(self):
        g = self.results['gates']
        self.assertTrue(g['G1_internal_state_composition'])
        # G2 (behavioural composition) is a REAL prespecified gate and FAILS on seed 4450 -- the
        # composition is not unconditional. Pin the recorded failure (AC16/17: do not move it).
        self.assertFalse(g['G2_behavioural_composition_adaptation_production_survival'])
        self.assertTrue(g['G3_state_sufficiency_observer_discard_gray_ctl'])
        self.assertTrue(g['G4_corrupt_is_the_only_change_arm_identity'])
        self.assertTrue(g['G5_completeness_determinism'])
        self.assertTrue(g['G6_adversarial_priority_stratum'])

    def test_seed_4450_composition_interaction(self):
        # seed 4450 (priority [0,3,2,1]) dies at 8408 with reconstruction complete (fw=0) and the
        # description intact at death (130) -- the composition interaction transfers from the
        # engineering seed 1 (identical death tick 8408, identical streak stall at 4).
        for h in (0, 1):
            r = self.rows[4450 * 2 + h]
            self.assertFalse(r['completed'], f'4450/{h}: survived (record moved)')
            self.assertEqual(r['first_dead'], 8408, f'4450/{h}: death tick moved')
            self.assertEqual(r['flipped_still_wrong'], 0, f'4450/{h}: reconstruction incomplete')
            self.assertEqual(r['description_correct_at_death'], 130,
                             f'4450/{h}: description not intact at death')
            self.assertEqual(r['relinquishments_by_move'], [0, 0], f'4450/{h}: relinq moved')
            self.assertEqual(r['reacquisitions_by_move'], [0, 0], f'4450/{h}: reacq moved')
            self.assertEqual(r['streak_final']['1'], 4, f'4450/{h}: streak not stalled at 4')

    def test_adversarial_stratum_full_composition(self):
        # every adversarial seed ([3,0,2,1]) fully composes -- the adversarial priority is NOT the
        # breaking point under the combined challenge.
        for s in self.results['adversarial']:
            for h in (0, 1):
                r = self.rows[s * 2 + h]
                self.assertTrue(r['completed'], f'{s}/{h}: adversarial did not survive')
                self.assertEqual(r['relinquishments_by_move'], [1, 1], f'{s}/{h}: relinq moved')
                self.assertEqual(r['reacquisitions_by_move'], [1, 1], f'{s}/{h}: reacq moved')
                self.assertEqual(r['flipped_still_wrong'], 0, f'{s}/{h}: reconstruction incomplete')

    def test_seed_disjointness(self):
        self.assertTrue(set(self.results['seeds']).isdisjoint(range(4448)),
                        'finals not disjoint from everything < 4448')
        self.assertTrue(set(self.results['seeds']).isdisjoint(set(range(8))),
                        'finals overlap engineering seeds')


class TestObserverDiscardFinals(unittest.TestCase):
    """G3 on the finals: the per-tick observer-discard on gray_ctl (corrupt=True) is byte-identical
    at every tick on every final individual (trajectory-level, state sufficiency)."""

    def test_per_tick_byte_identical_on_finals(self):
        for seed in (4448, 4466):
            d = ac101.observer_discard_equivalence(seed, 0, True)
            self.assertNotEqual(d.get('status'), 'no_mid_streak', f'seed {seed}: no mid-streak tick')
            self.assertTrue(d['swap_applied'], f'seed {seed}: swap hook never fired')
            self.assertTrue(d['per_tick_identical'], f'seed {seed}: discard changed the trajectory')


class TestConservation(unittest.TestCase):
    """A single gray_ctl corrupt=True run must not violate the conservation laws (ac4.balance
    asserts run in-step, so a violation raises inside the run)."""

    def test_run_respects_conservation(self):
        r = ac101.run(4448, 0, corrupt=True)
        # the run completed without raising; the balance asserts held at every step.
        self.assertIsInstance(r['state_hash'], str)


if __name__ == '__main__':
    unittest.main()
