"""AC97-D3 tests: the internal minimum resource reserve funds the relinquishment, and the
per-tick observer-discard equivalence holds on the finals.

Pins, at the single-step level, that:
- the reserve arms on a productive material contact (withholds exactly RESERVE_LEVEL from the
  intake and the spendable pool, sets the bit via a paid W-gated write), and rolls back whole if
  the arm write is refused (no W catalyst, or material below RESERVE_LEVEL);
- the release restores the withheld material and disarms, never releasing more than was withheld;
- the reserve bit is read by majority and is genuinely vulnerable (W-gated paid write).

Plus the finals-level checks: the per-tick observer-discard is byte-identical on every final seed,
the no-reserve control is byte-identical to ac96's maintained arm, and the final family is disjoint
from engineering and every prior final family.

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


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac95.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _fresh(seed=0):
    """A healthy organism with a disarmed reserve bit, W available, and abundant resources."""
    o, offs = ac12.acquire(seed)
    o.body.life[:4] = 64          # four live W catalysts -> _cap >= 32
    o.body.pos[:4] = 0            # interior (inside the boundary)
    o.body.energy = 200
    o.body.material = 200
    assert ac97.reserve_read(o) == 0
    return o, offs


def _ev(in_m=0):
    e = ac9.event()
    e['in_m'] = in_m
    return e


class TestReservePrimitive(unittest.TestCase):
    def test_arm_withholds_and_sets_bit(self):
        o, _ = _fresh(0)
        e = _ev(in_m=64)
        self.assertEqual(ac97.arm_reserve(o, e), 21)
        self.assertEqual(o.body.material, 200 - 21 - 7, 'withhold 21 + paid write 7')
        self.assertEqual(o.body.energy, 200 - 7)
        self.assertEqual(e['in_m'], 64 - 21, 'intake reduced by exactly RESERVE_LEVEL')
        self.assertEqual(e['spent_m'], 7)
        self.assertEqual(e['reserve_m'], 21)
        self.assertEqual(e['reserve_writes'], 7)
        self.assertEqual(ac97.reserve_read(o), 1, 'bit armed')

    def test_arm_refuses_when_poor(self):
        o, _ = _fresh(0)
        o.body.material = 10          # < RESERVE_LEVEL
        e = _ev(in_m=64)
        self.assertEqual(ac97.arm_reserve(o, e), 0)
        self.assertEqual(o.body.material, 10, 'unchanged')
        self.assertEqual(e['in_m'], 64, 'unchanged')
        self.assertEqual(ac97.reserve_read(o), 0)

    def test_arm_refuses_when_no_W(self):
        o, _ = _fresh(0)
        o.body.life[:4] = 0           # no produced machinery -> _cap == 0 -> write refused
        e = _ev(in_m=64)
        self.assertEqual(ac97.arm_reserve(o, e), 0)
        self.assertEqual(o.body.material, 200, 'rolled back whole')
        self.assertEqual(ac97.reserve_read(o), 0, 'never a half-armed reserve')

    def test_release_restores_and_disarms(self):
        o, _ = _fresh(0)
        e = _ev(in_m=64)
        ac97.arm_reserve(o, e)
        self.assertEqual(ac97.reserve_read(o), 1)
        o.body.material = 3            # collapse the pool (the drop shortfall)
        e2 = _ev()
        self.assertEqual(ac97.release_reserve(o, e2), 21)
        self.assertEqual(o.body.material, 3 + 21 - 7, 'release 21 + paid write 7')
        self.assertEqual(e2['in_m'], 21, 'released as intake (reverse of arming)')
        self.assertEqual(e2['reserve_released_m'], 21)
        self.assertEqual(ac97.reserve_read(o), 0, 'bit disarmed')
        self.assertLessEqual(e2['reserve_released_m'], e['reserve_m'], 'never release > withheld')

    def test_read_is_majority(self):
        o, _ = _fresh(0)
        self.assertEqual(ac97.reserve_read(o), 0)
        o.body.traces[1, ac97.RESERVE_OFFS, :4] = 1    # 4 of 7 -> armed
        self.assertEqual(ac97.reserve_read(o), 1)
        o.body.traces[1, ac97.RESERVE_OFFS, 0] = 0     # 3 of 7 -> disarmed
        self.assertEqual(ac97.reserve_read(o), 0)

    def test_write_is_atomic_and_paid(self):
        o, _ = _fresh(0)
        e = _ev()
        n = ac97.write_reserve(o, e, 1)               # 0 -> 1: all 7 replicas differ
        self.assertEqual(n, 7)
        self.assertEqual(o.body.energy, 200 - 7)
        self.assertEqual(o.body.material, 200 - 7)
        self.assertEqual(e['spent_e'], 7)
        self.assertEqual(e['writes'], 7)


class TestControlEquivalence(unittest.TestCase):
    def test_no_reserve_byte_identical_to_ac96(self):
        # the frozen ac96 maintained arm, reproduced byte-for-byte by this runner with the
        # reserve disabled (the reserve is the only change).
        for seed in (4432, 4433, 4434, 4435):
            for hist in (0, 1):
                a = ac97.run(seed, hist, 'gated', reserve=False, damage=True, corrupt=False,
                             transition='perm')
                b = ac96.run(seed, hist, 'gated', True, False, 'perm', streak_maintained=True)
                self.assertEqual(a['state_hash'], b['state_hash'],
                                 f'no-reserve diverged from ac96 {seed}/{hist}')

    def test_d2_reproduction(self):
        self.assertEqual(ac97.no_reserve_reproduction([4412, 4413, 4414, 4415]), 8)


class TestSeedDisjointness(unittest.TestCase):
    def test_final_seeds_disjoint(self):
        finals = [4432, 4433, 4434, 4435]
        self.assertTrue(set(finals).isdisjoint(range(8)), 'finals overlap engineering 0-7')
        self.assertTrue(set(finals).isdisjoint(range(4432)), 'finals not disjoint from < 4432')

    def test_results_seeds_match(self):
        results = json.loads(Path('ac97_results_v1/results.json').read_text())
        self.assertEqual(results['seeds'], [4432, 4433, 4434, 4435])
        self.assertEqual(results['transition'], 'perm')
        self.assertEqual(len(results['rows']), 4 * 2 * 2)


class TestObserverDiscardFinals(unittest.TestCase):
    """G3 on the finals: the per-tick observer-discard (succession observer + host streak dict) at a
    mid-streak tick is byte-identical at every tick on every final seed (trajectory-level)."""

    def test_per_tick_swap_byte_identical_on_finals(self):
        for seed in (4432, 4433, 4434, 4435):
            d = ac97.observer_discard_equivalence(seed, 0)
            self.assertNotEqual(d.get('status'), 'no_mid_streak', f'seed {seed}: no mid-streak tick')
            self.assertTrue(d['swap_applied'], f'seed {seed}: swap hook never fired')
            self.assertEqual(d['streak_at_swap'], 2, f'seed {seed}: swap not at a non-zero streak')
            self.assertTrue(d['per_tick_identical'], f'seed {seed}: discard changed the trajectory')


class TestRecordedFalsification(unittest.TestCase):
    """Pin the recorded G1 failure (AC16's recorded-outcome regression): on unseen seeds 4434/4435
    the reserve arm dies while the no-reserve control survives. A future code change that moves
    this record is caught here instead of silently absorbed."""

    def test_reserve_arm_dies_on_4434_4435(self):
        for seed in (4434, 4435):
            r = ac97.run(seed, 0, 'gated', reserve=True, damage=True, corrupt=False,
                         transition='perm')
            self.assertFalse(r['completed'], f'seed {seed}: recorded falsification moved')
            self.assertEqual(r['relinquishments'], 0, f'seed {seed}: recorded falsification moved')
            self.assertGreater(r['reserve_m'], 0, f'seed {seed}: reserve armed but never released')
            self.assertEqual(r['reserve_released_m'], 0)

    def test_no_reserve_control_survives_on_4434_4435(self):
        for seed in (4434, 4435):
            r = ac97.run(seed, 0, 'gated', reserve=False, damage=True, corrupt=False,
                         transition='perm')
            self.assertTrue(r['completed'], f'seed {seed}: control no longer survives')

    def test_recorded_gates(self):
        results = json.loads(Path('ac97_results_v1/results.json').read_text())
        self.assertFalse(results['gates']['G1_unconditional_adaptation'],
                         'G1 recorded as PASS but the reserve arm dies on 4434/4435')
        self.assertTrue(results['gates']['G3_state_sufficiency_per_tick_discard'])
        self.assertTrue(results['gates']['G4_endogenous_reserve_no_external_rescue'])


if __name__ == '__main__':
    unittest.main()
