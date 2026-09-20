"""AC100 tests: the move-schedule 2x2 factorial (binary/Gray x reserve/no-reserve).

Pins, at the single-step and single-move level:
- the schedule mapping: at [(8192, 'flip')] it reproduces ac95.mapping_at(..., 'perm') exactly,
  and the two-move schedule flips channel 1 and flips it back;
- the single-move byte-identity of each arm against its AC99 runner (the schedule change is the
  only change in the runner);
- the recorded finals outcome (4444-4447): G1 PASS (gray_ctl sustains both moves on every seed),
  the binary-no-reserve death on 4446 (the AC96 economic/W-bound stall), the no-harm gates, the
  reserve-redundancy, and seed-disjointness -- so a future code change that moves the record is
  caught.

Not hashed (AC17's rule) -- verification tool only.
"""
import unittest
from pathlib import Path
import json
import ac4
import ac9
import ac12
import ac95
import ac96
import ac99
import ac99_d2
import ac100


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac95.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestScheduleMapping(unittest.TestCase):
    """The schedule mapping is the only change from AC99: at the single-move schedule it is
    byte-identical to the frozen mapping, and the two-move schedule flips and flips back."""

    def test_single_move_equals_ac95_perm(self):
        for base in ((0, 0), (0, 1), (1, 0), (1, 1)):
            for t in (0, 1000, 8191, 8192, 10000, 16383):
                self.assertEqual(list(ac100.mapping_at(base, t, ac100.SINGLE_MOVE)),
                                 ac95.mapping_at(base, t, 'perm', ac95.MOVE_TICK),
                                 f'base={base} t={t}')

    def test_two_move_schedule(self):
        # flip at 8192, flip back at 12288
        for base in ((0, 0), (1, 1)):
            b1 = base[1]
            self.assertEqual(ac100.mapping_at(base, 5000, ac100.SCHEDULE)[1], b1)
            self.assertEqual(ac100.mapping_at(base, 9000, ac100.SCHEDULE)[1], 1 - b1)
            self.assertEqual(ac100.mapping_at(base, 13000, ac100.SCHEDULE)[1], b1)


class TestSingleMoveEquivalence(unittest.TestCase):
    """Each arm reproduces its AC99 runner byte-for-byte (state_hash) at the single-move schedule,
    proving the runner is a faithful extension and the schedule is the only change."""

    def test_arms_reproduce_ac99_at_single_move(self):
        for seed in (0, 4442):
            for h in (0, 1):
                refs = {
                    'bin_res': ac99.run(seed, h, 'gated', reserve=True, damage=True, corrupt=False, transition='perm'),
                    'gray_res': ac99_d2.run(seed, h, 'gated', reserve=True, damage=True, corrupt=False, transition='perm'),
                    'bin_ctl': ac99.run(seed, h, 'gated', reserve=False, damage=True, corrupt=False, transition='perm'),
                    'gray_ctl': ac99_d2.run(seed, h, 'gated', reserve=False, damage=True, corrupt=False, transition='perm'),
                }
                for code in ac100.ARMS:
                    got = ac100.run(seed, h, code, schedule=ac100.SINGLE_MOVE)
                    self.assertEqual(got['state_hash'], refs[code]['state_hash'],
                                     f'{seed}/{h}/{code}: single-move not byte-identical to AC99 runner')


FINALS = (4444, 4445, 4446, 4447)
ENGINEERING = (0, 1, 2, 3, 4, 5, 6, 7)


class TestFinals(unittest.TestCase):
    """AC100 finals (4444-4447): pins the RECORDED result -- G1 PASS, the binary-no-reserve death
    on 4446, the no-harm gates, reserve-redundancy, and seed-disjointness."""

    @classmethod
    def setUpClass(cls):
        cls.rows = {}
        for seed in FINALS:
            for h in (0, 1):
                for code in ac100.ARMS:
                    cls.rows[(seed, h, code)] = ac100.run(seed, h, code, schedule=ac100.SCHEDULE)

    def test_gray_ctl_sustains_both_moves_all_seeds(self):
        # G1: gray_ctl (Gray, no reserve) relinquishes + reacquires after EVERY move and survives
        for seed in FINALS:
            for h in (0, 1):
                r = self.rows[(seed, h, 'gray_ctl')]
                self.assertTrue(r['completed'], f'{seed}/{h}: gray_ctl did not survive')
                self.assertEqual(r['relinquishments_by_move'], [1, 1],
                                 f'{seed}/{h}: gray_ctl did not relinquish after every move')
                self.assertEqual(r['reacquisitions_by_move'], [1, 1],
                                 f'{seed}/{h}: gray_ctl did not reacquire after every move')

    def test_gray_ctl_production_every_window(self):
        for seed in FINALS:
            for h in (0, 1):
                r = self.rows[(seed, h, 'gray_ctl')]
                for i in (1, 2):  # post-move windows
                    w = r['births_by_window'][str(i)]
                    self.assertGreater(w['W_birth'], 0, f'{seed}/{h} w{i}: no W births')
                    self.assertGreater(w['C_birth'], 0, f'{seed}/{h} w{i}: no C births')
                    self.assertGreater(w['B_birth'], 0, f'{seed}/{h} w{i}: no B births')

    def test_bin_ctl_dies_on_4446(self):
        # the binary-no-reserve arm dies on 4446 (8448, the AC96 economic/W-bound stall), and
        # gray_ctl flips it -- the load-bearing direction carried by G1.
        for h in (0, 1):
            r = self.rows[(4446, h, 'bin_ctl')]
            self.assertFalse(r['completed'], f'4446/{h}: bin_ctl survived (record moved)')
            self.assertEqual(r['relinquishments'], 0, f'4446/{h}: bin_ctl dropped (record moved)')
            self.assertTrue(self.rows[(4446, h, 'gray_ctl')]['completed'],
                            f'4446/{h}: gray_ctl did not flip the binary death')

    def test_no_harm_encoding(self):
        # G2: no individual where bin_res survives and gray_res dies
        for seed in FINALS:
            for h in (0, 1):
                self.assertFalse(self.rows[(seed, h, 'bin_res')]['completed']
                                 and not self.rows[(seed, h, 'gray_res')]['completed'],
                                 f'{seed}/{h}: encoding no-harm violated')

    def test_no_harm_reserve(self):
        # G3: no individual where gray_ctl survives and gray_res dies
        for seed in FINALS:
            for h in (0, 1):
                self.assertFalse(self.rows[(seed, h, 'gray_ctl')]['completed']
                                 and not self.rows[(seed, h, 'gray_res')]['completed'],
                                 f'{seed}/{h}: reserve no-harm violated')

    def test_reserve_redundant_not_necessary(self):
        # Q1: the reserve is never load-bearing for Gray -- gray_res never succeeds where gray_ctl
        # fails. (The reserve is redundant for the Gray architecture on these finals.)
        for seed in FINALS:
            for h in (0, 1):
                self.assertFalse(not self.rows[(seed, h, 'gray_ctl')]['completed']
                                 and self.rows[(seed, h, 'gray_res')]['completed'],
                                 f'{seed}/{h}: reserve was load-bearing (record moved)')

    def test_endogenous_reserve(self):
        # G5: every reserve-arm individual withheld > 0 and released <= withheld
        for seed in FINALS:
            for h in (0, 1):
                for code in ('bin_res', 'gray_res'):
                    r = self.rows[(seed, h, code)]
                    self.assertGreater(r['reserve_m'], 0, f'{seed}/{h}/{code}: never armed')
                    self.assertLessEqual(r['reserve_released_m'], r['reserve_m'],
                                         f'{seed}/{h}/{code}: released > withheld')

    def test_final_seeds_disjoint(self):
        self.assertTrue(set(FINALS).isdisjoint(range(4444)), 'finals not disjoint from everything < 4444')
        self.assertTrue(set(FINALS).isdisjoint(set(ENGINEERING)), 'finals overlap engineering seeds')

    def test_results_seeds_and_arms_match(self):
        results = json.loads(Path('ac100_results_v1/results.json').read_text())
        self.assertEqual(results['seeds'], list(FINALS))
        self.assertEqual(results['arms'], ac100.ARMS)
        self.assertEqual(len(results['rows']), 4 * 2 * 4)

    def test_recorded_gates(self):
        results = json.loads(Path('ac100_results_v1/results.json').read_text())
        g = results['gates']
        self.assertTrue(g['G1_sustained_adaptation_no_reserve'])
        self.assertTrue(g['G2_no_harm_encoding_gray_res_vs_bin_res'])
        self.assertTrue(g['G3_no_harm_reserve_gray_res_vs_gray_ctl'])
        self.assertTrue(g['G4_state_sufficiency_per_tick_discard'])
        self.assertTrue(g['G5_endogenous_reserve_no_external_rescue'])
        self.assertTrue(g['G6_completeness_determinism_arm_identity'])


class TestObserverDiscardFinals(unittest.TestCase):
    """G4 on the finals: the per-tick observer-discard on gray_res at a mid-streak tick is
    byte-identical at every tick on every final seed (trajectory-level)."""

    def test_per_tick_swap_byte_identical_on_finals(self):
        for seed in FINALS:
            d = ac100.observer_discard_equivalence(seed, 0, ac100.SCHEDULE)
            self.assertNotEqual(d.get('status'), 'no_mid_streak', f'seed {seed}: no mid-streak tick')
            self.assertTrue(d['swap_applied'], f'seed {seed}: swap hook never fired')
            self.assertEqual(d['streak_at_swap'], 2, f'seed {seed}: swap not at a non-zero streak')
            self.assertTrue(d['per_tick_identical'], f'seed {seed}: discard changed the trajectory')


if __name__ == '__main__':
    unittest.main()
