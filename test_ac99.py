"""AC99-D1 tests: the release+disarm atomicity fix.

Pins, at the single-step level:
- with write capacity forced to zero (W=0 => `_cap`=0), `release_reserve` credits NOTHING
  and leaves the reserve armed -- no 21 -> 42 double-release (the reviewer's reproduction);
- a refused release is a no-op (bit armed, no material credited) and never releases more
  than was withheld (the G4 `released <= withheld` conservation regression);
- the successful release path is byte-for-byte unchanged from ac98 (credit 21, disarm paid
  out of the credit, net = 21 - replicas), so the fix is inert wherever the disarm succeeds;
- `arm_reserve`'s rollback on a refused arm write is unchanged (kept green).

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
import ac98
import ac99
import ac99_d2
import ac99_d4


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac95.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _fresh(seed=0):
    """A healthy organism with a disarmed reserve bit, W available, abundant resources."""
    o, offs = ac12.acquire(seed)
    o.body.life[:4] = 64          # four live W catalysts -> _cap >= 32
    o.body.pos[:4] = 0            # interior (inside the boundary)
    o.body.energy = 200
    o.body.material = 200
    assert ac99.reserve_read(o) == 0
    return o, offs


def _ev(in_m=0):
    e = ac9.event()
    e['in_m'] = in_m
    return e


def _armed(seed=0):
    o, offs = _fresh(seed)
    e = _ev(in_m=64)
    assert ac99.arm_reserve(o, e) == 21
    assert ac99.reserve_read(o) == 1
    return o, offs


class TestReleaseAtomicity(unittest.TestCase):
    """The AC99-D1 fix: release and disarm succeed or fail together."""

    def test_refused_disarm_credits_nothing_and_stays_armed(self):
        # W=0 => _cap = 0 => every paid write is refused. The release must credit nothing
        # and leave the reserve armed (the reviewer's reproduction, now failing on ac98).
        o, _ = _armed(0)
        o.body.life[:4] = 0           # no produced machinery -> _cap == 0
        o.body.material = 3           # collapsed pool (the drop shortfall)
        e = _ev()
        self.assertEqual(ac99.release_reserve(o, e), 0, 'refused release returned a non-zero amount')
        self.assertEqual(o.body.material, 3, 'material was credited despite the refused disarm')
        self.assertEqual(e.get('in_m', 0), 0, 'in_m was credited despite the refused disarm')
        self.assertEqual(e.get('reserve_released_m', 0), 0, 'release was counted despite refusal')
        self.assertEqual(ac99.reserve_read(o), 1, 'bit was disarmed despite the refused write')

    def test_no_double_release_21_to_42(self):
        # two refused releases must credit 0 in total (ac98 credited 42 against 21 withheld).
        o, _ = _armed(0)
        o.body.life[:4] = 0
        o.body.material = 3
        e1 = _ev(); e2 = _ev()
        self.assertEqual(ac99.release_reserve(o, e1), 0)
        self.assertEqual(ac99.release_reserve(o, e2), 0)
        released = e1.get('reserve_released_m', 0) + e2.get('reserve_released_m', 0)
        self.assertEqual(released, 0, 'double-release credited material twice')
        self.assertEqual(o.body.material, 3, 'pool grew despite both releases being refused')
        self.assertEqual(ac99.reserve_read(o), 1, 'bit left armed after refused releases')

    def test_conservation_released_never_exceeds_withheld(self):
        # G4: with one arm (21 withheld) and a refused release, released (0) <= withheld (21).
        o, _ = _armed(0)
        o.body.life[:4] = 0
        o.body.material = 3
        e = _ev()
        ac99.release_reserve(o, e)
        self.assertLessEqual(e.get('reserve_released_m', 0), 21,
                             'refused release broke the released <= withheld invariant')

    def test_successful_release_unchanged_from_ac98(self):
        # the successful path is byte-for-byte identical to ac98: release 21, disarm paid out
        # of the credit (7), net material = 3 + 21 - 7 = 17, bit disarmed.
        o, _ = _armed(0)
        o.body.material = 3
        e = _ev()
        self.assertEqual(ac99.release_reserve(o, e), 21)
        self.assertEqual(o.body.material, 3 + 21 - 7)
        self.assertEqual(e['in_m'], 21)
        self.assertEqual(e['reserve_released_m'], 21)
        self.assertEqual(ac99.reserve_read(o), 0, 'bit not disarmed on the successful path')

    def test_successful_release_matches_ac98_field_for_field(self):
        # two independent single-step releases, one on ac98 and one on ac99, agree exactly
        # (proving the fix is inert wherever the disarm succeeds).
        oa, _ = _armed(0)
        ob, _ = _armed(0)
        oa.body.material = ob.body.material = 3
        ea, eb = _ev(), _ev()
        ra = ac98.release_reserve(oa, ea)
        rb = ac99.release_reserve(ob, eb)
        self.assertEqual(ra, rb)
        self.assertEqual(oa.body.material, ob.body.material)
        self.assertEqual(oa.body.energy, ob.body.energy)
        self.assertEqual(ea['reserve_released_m'], eb['reserve_released_m'])
        self.assertEqual(ea['spent_m'], eb['spent_m'])
        self.assertEqual(ac98.reserve_read(oa), ac99.reserve_read(ob))


class TestArmReserveUnchanged(unittest.TestCase):
    """arm_reserve's rollback is untouched by the fix (kept green)."""

    def test_arm_refuses_when_no_W_and_rolls_back(self):
        o, _ = _fresh(0)
        o.body.life[:4] = 0           # no W -> _cap == 0 -> arm write refused
        e = _ev(in_m=64)
        self.assertEqual(ac99.arm_reserve(o, e), 0)
        self.assertEqual(o.body.material, 200, 'rolled back whole')
        self.assertEqual(e['in_m'], 64, 'withholding not rolled back')
        self.assertEqual(e.get('reserve_m', 0), 0)
        self.assertEqual(ac99.reserve_read(o), 0, 'never a half-armed reserve')


class TestGrayCode(unittest.TestCase):
    """The Gray counter's code properties that carry the AC99-D4 claim (single-step, pure)."""

    def test_gray_roundtrip(self):
        for n in range(8):
            self.assertEqual(ac99_d2.gray_decode(ac99_d2.gray_encode(n)), n)

    def test_gray_3to4_is_one_bit(self):
        # the decisive transition: binary 3->4 changes 3 bits (21 replicas, W >= 3); Gray 3->4
        # changes ONE bit (7 replicas, W >= 1).
        self.assertEqual((3 ^ 4).bit_count(), 3)
        self.assertEqual((ac99_d2.gray_encode(3) ^ ac99_d2.gray_encode(4)).bit_count(), 1)

    def test_gray_removes_two_wbound_increments(self):
        # binary 1->2 is 2 bits (14 replicas, W >= 2) and 3->4 is 3 bits (21, W >= 3); both are
        # 1 bit (7 replicas, W >= 1) in Gray.
        cost = {r['transition']: r for r in ac99_d2.transition_cost_table()}
        self.assertEqual(cost['1->2']['binary_replicas'], 14)
        self.assertEqual(cost['1->2']['gray_replicas'], 7)
        self.assertEqual(cost['3->4']['binary_replicas'], 21)
        self.assertEqual(cost['3->4']['gray_replicas'], 7)

    def test_gray_reset_is_dearer(self):
        # the one operation where Gray loses: 5->0 reset is 3 bits (21) vs binary 2 bits (14), so
        # drop (7) + reset (21) = 28 now exceeds RESERVE_LEVEL = 21 (binary 7 + 14 = 21 filled it).
        cost = {r['transition']: r for r in ac99_d2.transition_cost_table()}
        self.assertEqual(cost['5->0 (reset)']['gray_replicas'], 21)
        self.assertEqual(cost['5->0 (reset)']['binary_replicas'], 14)

    def test_gray_damage_can_decrease(self):
        # sticky-SET damage on a Gray counter can ERASE progress (a decrease), where binary sticky
        # damage only ever increases the count.
        dmg = {r['value']: r for r in ac99_d2.damage_read_table()}
        self.assertLess(min(dmg[3]['gray_flip_reads']), 3, 'Gray damage at value 3 must be able to decrease')
        self.assertTrue(all(v > 3 for v in dmg[3]['binary_flip_reads']),
                        'binary damage at value 3 must only increase')


FINALS = (4440, 4441, 4442, 4443)
ENGINEERING = (0, 1, 2, 3, 4, 5, 6, 7, 4412, 4413, 4414, 4415, 4436, 4437, 4438, 4439)


class TestD4Finals(unittest.TestCase):
    """AC99-D4 finals: the unseen family 4440-4443. Pins the RECORDED result -- G1 PASS (the Gray
    success arm satisfies all four measures on every seed), the binary control's death on 4442 (the
    same economic/W-bound stall class as AC98's 4436, at streak 5), the wb_first rival's PRE-MOVE
    death on 4441 (the priority swap's own cost), the no-harm gate, seed-disjointness, and the
    recorded gates -- so a future code change that moves the record is caught."""

    @classmethod
    def setUpClass(cls):
        cls.rows = {}
        for seed in FINALS:
            for h in (0, 1):
                for code in ac99_d4.ARMS:
                    cls.rows[(seed, h, code)] = ac99_d4.run(seed, h, code, transition='perm',
                                                            damage=True, corrupt=False)

    def test_gray_survives_and_relinquishes_all_seeds(self):
        for seed in FINALS:
            for h in (0, 1):
                r = self.rows[(seed, h, 'gray')]
                self.assertTrue(r['completed'], f'{seed}/{h}: gray arm did not survive')
                self.assertGreaterEqual(r['relinquishments'], 1, f'{seed}/{h}: drop did not fire')

    def test_gray_continues_production_all_seeds(self):
        for seed in FINALS:
            for h in (0, 1):
                r = self.rows[(seed, h, 'gray')]
                self.assertGreater(r['W_births_post_move'], 0, f'{seed}/{h}: no post-move W births')
                self.assertGreater(r['C_births_post_move'], 0, f'{seed}/{h}: no post-move C births')
                self.assertGreater(r['B_births_post_move'], 0, f'{seed}/{h}: no post-move B births')

    def test_binary_dies_on_4442(self):
        # the binary control (the AC98/AC99 architecture) dies on 4442 with the streak stuck at 5 --
        # the same economic/W-bound stall class as AC98's 4436 (streak 3), now at streak 5. Gray flips it.
        for h in (0, 1):
            r = self.rows[(4442, h, 'binary')]
            self.assertFalse(r['completed'], f'4442/{h}: binary control survived (record moved)')
            self.assertEqual(r['relinquishments'], 0, f'4442/{h}: binary control dropped (record moved)')
            self.assertEqual(r['streak_final'].get('1', r['streak_final'].get(1)), 5,
                             f'4442/{h}: the streak did not stall at 5')
            g = self.rows[(4442, h, 'gray')]
            self.assertTrue(g['completed'], f'4442/{h}: gray arm did not flip the binary death')

    def test_wb_first_dies_on_4441_premove(self):
        # the labeled rival dies on 4441 BEFORE the move (t=5501 < MOVE_TICK=8192): the priority
        # swap is the only change, so the swap itself kills the organism where both gray and binary
        # survive -- the rival's cost, reported not gated.
        for h in (0, 1):
            r = self.rows[(4441, h, 'wb_first')]
            self.assertFalse(r['completed'], f'4441/{h}: wb_first rival survived (record moved)')
            self.assertLess(r['first_dead'], 8192, f'4441/{h}: wb_first death was not pre-move')
            self.assertTrue(self.rows[(4441, h, 'gray')]['completed'],
                            f'4441/{h}: gray arm did not survive (rival death is not the no-harm direction)')
            self.assertTrue(self.rows[(4441, h, 'binary')]['completed'],
                            f'4441/{h}: binary control did not survive (rival death is not the no-harm direction)')

    def test_no_harm(self):
        # no distinct seed where the binary control survives and the gray arm dies
        for seed in FINALS:
            for h in (0, 1):
                self.assertFalse(self.rows[(seed, h, 'binary')]['completed']
                                 and not self.rows[(seed, h, 'gray')]['completed'],
                                 f'{seed}/{h}: no-harm violated (binary survives, gray dies)')

    def test_final_seeds_disjoint(self):
        self.assertTrue(set(FINALS).isdisjoint(range(4440)), 'finals not disjoint from everything < 4440')
        self.assertTrue(set(FINALS).isdisjoint(set(ENGINEERING)), 'finals overlap the engineering seeds')

    def test_results_seeds_match(self):
        results = json.loads(Path('ac99_results_v1/results.json').read_text())
        self.assertEqual(results['seeds'], list(FINALS))
        self.assertEqual(results['transition'], 'perm')
        self.assertEqual(results['arms'], ['gray', 'binary', 'wb_first'])
        self.assertEqual(len(results['rows']), 4 * 2 * 3)

    def test_recorded_gates(self):
        results = json.loads(Path('ac99_results_v1/results.json').read_text())
        g = results['gates']
        self.assertTrue(g['G1_unconditional_adaptation'], 'G1 recorded as FAIL (gray arm moved)')
        self.assertTrue(g['G2_no_harm'], 'G2 recorded as FAIL (the no-harm gate moved)')
        self.assertTrue(g['G3_state_sufficiency_per_tick_discard'])
        self.assertTrue(g['G4_endogenous_reserve_no_external_rescue'])
        self.assertTrue(g['G5_completeness_determinism_arm_identity'])


class TestObserverDiscardFinals(unittest.TestCase):
    """G3 on the finals: the per-tick observer-discard on the GRAY success arm (succession observer +
    host streak dict) at a mid-streak tick is byte-identical at every tick on every final seed
    (trajectory-level)."""

    def test_per_tick_swap_byte_identical_on_finals(self):
        for seed in FINALS:
            d = ac99_d4.observer_discard_equivalence_gray(seed, 0)
            self.assertNotEqual(d.get('status'), 'no_mid_streak', f'seed {seed}: no mid-streak tick')
            self.assertTrue(d['swap_applied'], f'seed {seed}: swap hook never fired')
            self.assertEqual(d['streak_at_swap'], 2, f'seed {seed}: swap not at a non-zero streak')
            self.assertTrue(d['per_tick_identical'], f'seed {seed}: discard changed the trajectory')


if __name__ == '__main__':
    unittest.main()
