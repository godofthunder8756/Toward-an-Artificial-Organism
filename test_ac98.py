"""AC98-D2 tests: the revised reserve's release triggers, the AC97-flip regression, no-harm,
and the no-reserve byte-identity to ac97.

Pins, at the single-step level (unchanged AC97 primitives + the two new triggers):
- arm withholds exactly RESERVE_LEVEL from intake and the pool and sets the bit (paid, W-gated),
  rolling back whole if the arm write is refused (no W, or material below RESERVE_LEVEL);
- release restores the withheld material and disarms, never releasing more than was withheld;
- the reserve bit is read by majority and written atomically (paid);
- `stall`: a refused streak increment (streak_write returns 0 in the cur -> cur+1 branch)
  releases the reserve;
- `wlow`: W < 3 and material <= 64 on a key-1 unproductive contact releases the reserve.

Plus the engineering-level checks (one cached pass over the 16 individuals):
- 4434 flips death -> relinquish + survive (via the stall release);
- 4435 flips death -> survive (honest residual: survives without relinquishing; wlow fires);
- no regression on 4432/4433/4412-4415 (relinquish + survive);
- no-harm: no individual where the no-reserve control survives and the reserve arm dies;
- the no-reserve control is byte-identical to ac97's no-reserve arm.

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
import ac97
import ac98

SEEDS = (4432, 4433, 4434, 4435, 4412, 4413, 4414, 4415)
FINALS = (4436, 4437, 4438, 4439)


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
    assert ac98.reserve_read(o) == 0
    return o, offs


def _ev(in_m=0):
    e = ac9.event()
    e['in_m'] = in_m
    return e


def _alloc(o, offs, seed=0, history=0, reserve=True):
    alloc = ac98.AllocEraseReserve('allocate', seed, history, reserve=reserve)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    alloc.streak_offs = ac96.streak_offsets(o)
    alloc.now = ac95.MOVE_TICK
    return alloc


class TestReservePrimitive(unittest.TestCase):
    """The unchanged AC97 primitives (re-verified against the copied module)."""

    def test_arm_withholds_and_sets_bit(self):
        o, _ = _fresh(0)
        e = _ev(in_m=64)
        self.assertEqual(ac98.arm_reserve(o, e), 21)
        self.assertEqual(o.body.material, 200 - 21 - 7, 'withhold 21 + paid write 7')
        self.assertEqual(o.body.energy, 200 - 7)
        self.assertEqual(e['in_m'], 64 - 21, 'intake reduced by exactly RESERVE_LEVEL')
        self.assertEqual(e['spent_m'], 7)
        self.assertEqual(e['reserve_m'], 21)
        self.assertEqual(e['reserve_writes'], 7)
        self.assertEqual(ac98.reserve_read(o), 1, 'bit armed')

    def test_arm_refuses_when_poor(self):
        o, _ = _fresh(0)
        o.body.material = 10          # < RESERVE_LEVEL
        e = _ev(in_m=64)
        self.assertEqual(ac98.arm_reserve(o, e), 0)
        self.assertEqual(o.body.material, 10, 'unchanged')
        self.assertEqual(e['in_m'], 64, 'unchanged')
        self.assertEqual(ac98.reserve_read(o), 0)

    def test_arm_refuses_when_no_W(self):
        o, _ = _fresh(0)
        o.body.life[:4] = 0           # no produced machinery -> _cap == 0 -> write refused
        e = _ev(in_m=64)
        self.assertEqual(ac98.arm_reserve(o, e), 0)
        self.assertEqual(o.body.material, 200, 'rolled back whole')
        self.assertEqual(ac98.reserve_read(o), 0, 'never a half-armed reserve')

    def test_release_restores_and_disarms(self):
        o, _ = _fresh(0)
        e = _ev(in_m=64)
        ac98.arm_reserve(o, e)
        self.assertEqual(ac98.reserve_read(o), 1)
        o.body.material = 3            # collapse the pool (the drop shortfall)
        e2 = _ev()
        self.assertEqual(ac98.release_reserve(o, e2), 21)
        self.assertEqual(o.body.material, 3 + 21 - 7, 'release 21 + paid write 7')
        self.assertEqual(e2['in_m'], 21, 'released as intake (reverse of arming)')
        self.assertEqual(e2['reserve_released_m'], 21)
        self.assertEqual(ac98.reserve_read(o), 0, 'bit disarmed')
        self.assertLessEqual(e2['reserve_released_m'], e['reserve_m'], 'never release > withheld')

    def test_read_is_majority(self):
        o, _ = _fresh(0)
        self.assertEqual(ac98.reserve_read(o), 0)
        o.body.traces[1, ac98.RESERVE_OFFS, :4] = 1    # 4 of 7 -> armed
        self.assertEqual(ac98.reserve_read(o), 1)
        o.body.traces[1, ac98.RESERVE_OFFS, 0] = 0     # 3 of 7 -> disarmed
        self.assertEqual(ac98.reserve_read(o), 0)

    def test_write_is_atomic_and_paid(self):
        o, _ = _fresh(0)
        e = _ev()
        n = ac98.write_reserve(o, e, 1)               # 0 -> 1: all 7 replicas differ
        self.assertEqual(n, 7)
        self.assertEqual(o.body.energy, 200 - 7)
        self.assertEqual(o.body.material, 200 - 7)
        self.assertEqual(e['spent_e'], 7)
        self.assertEqual(e['writes'], 7)


class TestReleaseTriggers(unittest.TestCase):
    """The two new release conditions, exercised at the single-step level."""

    def _armed(self, seed=0):
        o, offs = _fresh(seed)
        e = _ev(in_m=64)
        assert ac98.arm_reserve(o, e) == 21
        assert ac98.reserve_read(o) == 1
        return o, offs

    def test_stall_release_on_refused_increment(self):
        # W=3 (cap 24), material=6: the 0->1 increment needs 7 replicas but cap = 6, so
        # streak_write refuses and the stall release returns the withheld 21 (AC97 seed 4434).
        o, offs = self._armed(0)
        o.body.life[3:4] = 0            # W = 3
        o.body.material = 6
        alloc = _alloc(o, offs)
        e = _ev()
        alloc.outcome(o, 1, e)
        self.assertEqual(ac98.reserve_read(o), 0, 'stall release disarmed the reserve')
        self.assertEqual(o.body.material, 6 + 21 - 7, 'release 21 then disarm write 7')
        kinds = [ev[1] for ev in alloc.reserve_events if ev[1] in ('drop', 'stall', 'wlow')]
        self.assertEqual(kinds, ['stall'])

    def test_wlow_release_on_failing_catalyst(self):
        # W=2 (< 3) and material=54 (<= 64): the key-1 unproductive contact releases the
        # reserve so material rises above 64 and obs bit 1 clears (AC97 seed 4435's survival).
        o, offs = self._armed(0)
        o.body.life[2:4] = 0            # W = 2
        o.body.material = 54
        alloc = _alloc(o, offs)
        e = _ev()
        alloc.outcome(o, 1, e)
        self.assertEqual(ac98.reserve_read(o), 0, 'wlow release disarmed the reserve')
        kinds = [ev[1] for ev in alloc.reserve_events if ev[1] in ('drop', 'stall', 'wlow')]
        self.assertIn('wlow', kinds)
        # streak increment (7) succeeded first (cap 16 >= 7), then the release (21) and the
        # disarm write (7): 54 - 7 + 21 - 7 = 61.
        self.assertEqual(o.body.material, 54 - 7 + 21 - 7)

    def test_no_release_when_disarmed(self):
        # with no reserve armed, neither trigger fires (the no-reserve control's outcome is
        # untouched by the new paths).
        o, offs = _fresh(0)
        o.body.life[2:4] = 0
        o.body.material = 54
        alloc = _alloc(o, offs, reserve=False)
        e = _ev()
        alloc.outcome(o, 1, e)
        kinds = [ev[1] for ev in alloc.reserve_events if ev[1] in ('drop', 'stall', 'wlow')]
        self.assertEqual(kinds, [], 'no release on the no-reserve control')


class TestEngineering(unittest.TestCase):
    """One cached pass over the 16 individuals (8 seeds x 2 histories), then the flip /
    no-regression / no-harm / byte-identity assertions."""

    @classmethod
    def setUpClass(cls):
        cls.nr = {}
        cls.res = {}
        cls.ac97nr = {}
        for seed in SEEDS:
            for h in (0, 1):
                cls.nr[(seed, h)] = ac98.run(seed, h, 'gated', reserve=False, damage=True,
                                             corrupt=False, transition='perm')
                cls.res[(seed, h)] = ac98.run(seed, h, 'gated', reserve=True, damage=True,
                                              corrupt=False, transition='perm')
                cls.ac97nr[(seed, h)] = ac97.run(seed, h, 'gated', reserve=False, damage=True,
                                                 corrupt=False, transition='perm')

    def test_4434_flip_death_to_relinquish_survive(self):
        for h in (0, 1):
            r = self.res[(4434, h)]
            self.assertTrue(r['completed'], f'4434/{h}: reserve arm did not survive')
            self.assertGreaterEqual(r['relinquishments'], 1, f'4434/{h}: drop did not fire')
            self.assertIn('stall', [k for (_t, k) in r['reserve_release_kinds']],
                          f'4434/{h}: the stall release did not fire')

    def test_4435_flip_death_to_survive(self):
        # honest residual: 4435 survives WITHOUT relinquishing (the 3->4 increment is W-bound;
        # the wlow release stops the death cascade but cannot make the drop fire).
        for h in (0, 1):
            r = self.res[(4435, h)]
            self.assertTrue(r['completed'], f'4435/{h}: reserve arm did not survive')
            self.assertEqual(r['relinquishments'], 0, f'4435/{h}: honest residual moved')
            self.assertIn('wlow', [k for (_t, k) in r['reserve_release_kinds']],
                          f'4435/{h}: the wlow release did not fire')

    def test_no_regression_on_4432_4433_4412_4415(self):
        for seed in (4432, 4433, 4412, 4413, 4414, 4415):
            for h in (0, 1):
                r = self.res[(seed, h)]
                self.assertTrue(r['completed'], f'{seed}/{h}: regressed (died)')
                self.assertGreaterEqual(r['relinquishments'], 1,
                                        f'{seed}/{h}: regressed (no relinquishment)')

    def test_no_harm(self):
        for seed in SEEDS:
            for h in (0, 1):
                self.assertFalse(self.nr[(seed, h)]['completed']
                                 and not self.res[(seed, h)]['completed'],
                                 f'{seed}/{h}: no-harm violated (control survives, reserve dies)')

    def test_no_reserve_byte_identical_to_ac97(self):
        for seed in SEEDS:
            for h in (0, 1):
                self.assertEqual(self.nr[(seed, h)]['state_hash'],
                                 self.ac97nr[(seed, h)]['state_hash'],
                                 f'{seed}/{h}: no-reserve diverged from ac97')


class TestD3Finals(unittest.TestCase):
    """AC98-D3 finals: the unseen family 4436-4439. Pins the RECORDED result (the G1 falsification
    on 4436 and the G2 no-harm pass), the per-tick observer-discard, the no-reserve byte-identity to
    ac97, seed-disjointness, and the recorded gates -- so a future code change that moves the record
    is caught instead of silently absorbed."""

    @classmethod
    def setUpClass(cls):
        cls.res = {}
        cls.nr = {}
        for seed in FINALS:
            for h in (0, 1):
                cls.nr[(seed, h)] = ac98.run(seed, h, 'gated', reserve=False, damage=True,
                                             corrupt=False, transition='perm')
                cls.res[(seed, h)] = ac98.run(seed, h, 'gated', reserve=True, damage=True,
                                              corrupt=False, transition='perm')

    def test_g1_fails_on_4436(self):
        # the recorded falsification: seed 4436's reserve arm stalls the streak at 3 (the W-bound
        # 3->4 increment) and dies without relinquishing.
        for h in (0, 1):
            r = self.res[(4436, h)]
            self.assertFalse(r['completed'], f'4436/{h}: recorded G1 failure moved (survived)')
            self.assertEqual(r['relinquishments'], 0, f'4436/{h}: recorded G1 failure moved (dropped)')
            self.assertEqual(r['streak_final'].get('1', r['streak_final'].get(1)), 3,
                             f'4436/{h}: the streak did not stall at 3')

    def test_g1_passes_on_4437_4438_4439(self):
        for seed in (4437, 4438, 4439):
            for h in (0, 1):
                r = self.res[(seed, h)]
                self.assertTrue(r['completed'], f'{seed}/{h}: reserve arm did not survive')
                self.assertGreaterEqual(r['relinquishments'], 1, f'{seed}/{h}: drop did not fire')

    def test_g2_no_harm_holds_on_finals(self):
        # no distinct seed where the no-reserve control survives and the reserve arm dies
        for seed in FINALS:
            for h in (0, 1):
                self.assertFalse(self.nr[(seed, h)]['completed']
                                 and not self.res[(seed, h)]['completed'],
                                 f'{seed}/{h}: no-harm violated (control survives, reserve dies)')

    def test_4436_control_also_dies(self):
        # on 4436 both arms die, so the reserve's death is a G1 failure (not enough) rather than a
        # G2 harm (the control does not survive). Pin that the control dies too.
        for h in (0, 1):
            self.assertFalse(self.nr[(4436, h)]['completed'],
                             f'4436/{h}: the control now survives (would make 4436 a no-harm hit)')

    def test_no_reserve_byte_identical_to_ac97_finals(self):
        for seed in FINALS:
            for h in (0, 1):
                b = ac97.run(seed, h, 'gated', reserve=False, damage=True, corrupt=False,
                             transition='perm')
                self.assertEqual(self.nr[(seed, h)]['state_hash'], b['state_hash'],
                                 f'{seed}/{h}: no-reserve diverged from ac97')

    def test_final_seeds_disjoint(self):
        self.assertTrue(set(FINALS).isdisjoint(range(4436)),
                        'finals not disjoint from everything < 4436')
        self.assertTrue(set(FINALS).isdisjoint(set(SEEDS)),
                        'finals overlap the D2 engineering seeds')
        self.assertTrue(set(FINALS).isdisjoint(range(8)), 'finals overlap engineering 0-7')

    def test_results_seeds_match(self):
        results = json.loads(Path('ac98_results_v1/results.json').read_text())
        self.assertEqual(results['seeds'], list(FINALS))
        self.assertEqual(results['transition'], 'perm')
        self.assertEqual(len(results['rows']), 4 * 2 * 2)

    def test_recorded_gates(self):
        results = json.loads(Path('ac98_results_v1/results.json').read_text())
        g = results['gates']
        self.assertFalse(g['G1_unconditional_adaptation'],
                         'G1 recorded as PASS but the reserve arm dies on 4436')
        self.assertTrue(g['G2_no_harm'], 'G2 recorded as FAIL (the no-harm gate moved)')
        self.assertTrue(g['G3_state_sufficiency_per_tick_discard'])
        self.assertTrue(g['G4_endogenous_reserve_no_external_rescue'])
        self.assertTrue(g['G5_completeness_determinism_control_equivalence'])


class TestObserverDiscardFinals(unittest.TestCase):
    """G3 on the finals: the per-tick observer-discard (succession observer + host streak dict) at a
    mid-streak tick is byte-identical at every tick on every final seed (trajectory-level)."""

    def test_per_tick_swap_byte_identical_on_finals(self):
        for seed in FINALS:
            d = ac98.observer_discard_equivalence(seed, 0)
            self.assertNotEqual(d.get('status'), 'no_mid_streak', f'seed {seed}: no mid-streak tick')
            self.assertTrue(d['swap_applied'], f'seed {seed}: swap hook never fired')
            self.assertEqual(d['streak_at_swap'], 2, f'seed {seed}: swap not at a non-zero streak')
            self.assertTrue(d['per_tick_identical'], f'seed {seed}: discard changed the trajectory')


if __name__ == '__main__':
    unittest.main()
