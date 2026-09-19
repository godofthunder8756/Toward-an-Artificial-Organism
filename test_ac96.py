"""AC96-D2 tests: the relinquishment failure-streak lives in maintained state, not a host dict.

Pins, at the single-step level, that:
- toggling the vestigial host dict `alloc.streak` produces identical writes on the maintained
  arm (the AC95-D1 section 2.2 leak is closed) while it still changes the host-streak control
  (the leak, reproduced);
- the streak bits are damaged by the ambient program stream and repaired by the paid bank-0
  majority-restore;
- `_drop` reads the maintained majority and a streak that reaches the threshold behaves exactly
  like the host-streak arm reaching it;
- a productive contact resets the maintained streak to 0 (a paid write).

Plus the comparator regression checks: the host-streak control is byte-identical to the frozen
ac95 gated arm, and the maintained arm is byte-identical to it on the shared trajectory up to the
first streak write.

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


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac95.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _fresh_bound(seed=0):
    """A healthy organism with key 0 bound at (0,0), plus a host and a maintained alloc."""
    o, offs = ac12.acquire(seed)
    o.body.energy = 200
    o.body.material = 200
    streak_offs = ac96.streak_offsets(o)
    r = ac9.mem.deposit(o.memory, o.body, 0, 0, [True, True], [3, 3])
    assert r['bound'] == 21, r
    place = ac12.m12.slot_of_key(o.memory, 0)
    assert place is not None
    host = ac95.AllocErase('allocate', seed, 0)
    host.offs = offs
    host.shadow = o.body.traces[0].copy()
    maint = ac96.AllocEraseMaintained('allocate', seed, 0)
    maint.offs = offs
    maint.streak_offs = streak_offs
    return o, offs, streak_offs, place, host, maint


def _clone(o, seed=0):
    o2, _ = ac12.acquire(seed)
    o2.body.traces[:] = o.body.traces
    o2.memory.bits[:] = o.memory.bits
    o2.memory.life[:] = o.memory.life
    o2.body.life[:] = o.body.life
    o2.body.pos[:] = o.body.pos
    o2.body.boundary[:] = o.body.boundary
    o2.body.energy = o.body.energy
    o2.body.material = o.body.material
    o2.body.fuel = o.body.fuel
    o2.body.dead = o.body.dead
    return o2


def _set_streak(o, key, val, streak_offs):
    for k in range(3):
        o.body.traces[0, streak_offs[3 * key + k], :] = (val >> k) & 1


def _ev():
    e = ac9.event()
    e['streak_writes'] = 0
    return e


class TestStreakOffsets(unittest.TestCase):
    def test_offsets_zero_and_distinct_from_register(self):
        for seed in (0, 1, 2, 3):
            o, offs = ac12.acquire(seed)
            so = ac96.streak_offsets(o)
            self.assertTrue(all(o.body.traces[0, x].sum() == 0 for x in so),
                            f'seed {seed}: streak bits not zero in frozen program')
            self.assertTrue(all(x < 126 for x in so), f'seed {seed}: streak offset >= 126')
            self.assertEqual(len(set(so + offs)), 10, f'seed {seed}: streak/register overlap')


class TestLeakClosed(unittest.TestCase):
    """AC95-D1 section 2.2 reproduction on the maintained arm: identical maintained state +
    toggled host dict -> identical writes; on the host control the same toggle changes the writes."""

    def test_host_dict_does_not_steer_maintained_writes(self):
        o, offs, streak_offs, place, host, maint = _fresh_bound(0)
        _set_streak(o, 0, 5, streak_offs)          # streak at STREAK_N - 1
        sigs = []
        for host_streak in (0, 5):
            o2 = _clone(o)
            m2 = ac96.AllocEraseMaintained('allocate', 0, 0)
            m2.offs = offs
            m2.streak_offs = streak_offs
            m2.streak[0] = host_streak             # vestigial host dict
            e = _ev()
            m2.outcome(o2, 0, e)
            sigs.append((o2.digest(), e['spent_e'], e['spent_m'], e['writes'],
                         e['streak_writes'], ac12.bit_value(o2, offs[2 * place[0] + place[1]])))
        self.assertEqual(sigs[0], sigs[1], 'host dict steered the maintained arm')
        # and the drop actually fired (streak 5 -> 6 >= STREAK_N)
        self.assertGreater(sigs[0][1], 0)
        self.assertEqual(sigs[0][5], 1, 'register bit not set on drop')

    def test_host_control_still_leaks(self):
        o, offs, streak_offs, place, host, maint = _fresh_bound(0)
        sigs = []
        for host_streak in (0, 5):
            o2 = _clone(o)
            h2 = ac95.AllocErase('allocate', 0, 0)
            h2.offs = offs
            h2.streak[0] = host_streak
            e = _ev()
            h2.outcome(o2, 0, e)
            sigs.append((o2.digest(), e['spent_e'], e['writes'],
                         ac12.bit_value(o2, offs[2 * place[0] + place[1]])))
        self.assertNotEqual(sigs[0], sigs[1], 'the host-streak control should still leak')


class TestStreakDamageRepair(unittest.TestCase):
    def test_streak_bits_damaged_and_repaired_by_bank0(self):
        o, offs, streak_offs, place, host, maint = _fresh_bound(0)
        self.assertEqual(ac96.streak_read(o, 0, streak_offs), 0)
        o.body.traces[0, streak_offs[0], 0:2] = 1   # sticky damage: 2 minority replicas
        self.assertEqual(ac96.streak_read(o, 0, streak_offs), 0, '2 < 4 replicas: majority holds')
        e = _ev()
        ac4.react(o.body, 2, 'self', e)             # paid bank-0 majority-restore (action 2)
        self.assertEqual(int(o.body.traces[0, streak_offs[0]].sum()), 0, 'repair restored the 2 replicas')
        self.assertEqual(e['writes'], 2, '2 replicas repaired')
        self.assertEqual(e['spent_e'], 3, '1 (action living cost) + 2 (paid writes)')


class TestDropReadsMajority(unittest.TestCase):
    def test_corrupted_streak_reaching_threshold_behaves_like_host(self):
        for seed in (0, 1):
            o, offs, streak_offs, place, host, maint = _fresh_bound(seed)
            reg_off = offs[2 * place[0] + place[1]]
            # maintained: streak majority = 5, unproductive -> drop
            o_m = _clone(o)
            _set_streak(o_m, 0, 5, streak_offs)
            e_m = _ev()
            maint.outcome(o_m, 0, e_m)
            # host: dict streak = 5, unproductive -> drop
            o_h = _clone(o)
            host.streak[0] = 5
            e_h = _ev()
            host.outcome(o_h, 0, e_h)
            for org in (o_m, o_h):
                self.assertEqual(ac12.bit_value(org, reg_off), 1, 'register must be set on drop')
                self.assertIsNone(ac12.m12.slot_of_key(org.memory, 0), 'entry must be erased')
                self.assertEqual(ac96.streak_read(org, 0, streak_offs), 0, 'streak reset')
            # identical decision state; only the paid streak reset (14 replicas) differs
            self.assertEqual(e_m['writes'], e_h['writes'] + 14,
                             'maintained drop pays the streak reset the host control does not')


class TestProductiveReset(unittest.TestCase):
    def test_productive_contact_resets_streak_to_zero(self):
        o, offs, streak_offs, place, host, maint = _fresh_bound(0)
        _set_streak(o, 0, 3, streak_offs)
        reg_off = offs[2 * place[0] + place[1]]
        e = _ev()
        e['productive'] = 1
        maint.outcome(o, 0, e)
        self.assertEqual(ac96.streak_read(o, 0, streak_offs), 0)
        self.assertEqual(e['streak_writes'], 14, 'clearing 0b011 costs 2 bits x 7 replicas')
        self.assertEqual(ac12.bit_value(o, reg_off), 0, 'productive reset must not relinquish')


class TestComparator(unittest.TestCase):
    def test_host_control_byte_identical_to_ac95(self):
        for seed in (0, 1, 2, 3):
            for hist in (0, 1):
                a = ac96.run(seed, hist, 'gated', True, False, 'perm', streak_maintained=False)
                b = ac95.run(seed, hist, 'gated', True, False, 'perm')
                self.assertEqual(a['state_hash'], b['state_hash'],
                                 f'host control diverged from ac95 {seed}/{hist}')

    def test_host_control_reproduces_frozen_ac95(self):
        self.assertEqual(ac96.frozen_reproduction(), 32)

    def test_prefix_byte_identity_until_first_divergence(self):
        # arms are identical through the tick before the first divergence, and the first
        # divergence is at or before the first paid streak write (the exclusion can fire earlier).
        for seed in (0, 1):
            for hist in (0, 1):
                fsw, first_div, n_eq = ac96.prefix_equivalence(seed, hist, 'perm', True, False)
                self.assertEqual(n_eq, first_div, 'prefix identical through the tick before divergence')
                self.assertLessEqual(first_div, fsw, 'divergence is at or before the first streak write')

    def test_exclusion_causes_pre_write_divergence_on_seed7(self):
        # seed 7: the first divergence (t=19) precedes the first streak write (t=100). It is the
        # reg_from_active exclusion -- ambient damage set a streak bit, the host control's
        # reconstruction reset it (paid), the maintained arm skipped it. Confined to the streak bits
        # and their 1-replica cost, not a behavioural divergence.
        fsw, first_div, n_eq = ac96.prefix_equivalence(7, 0, 'perm', True, False)
        self.assertLess(first_div, fsw)
        self.assertEqual(n_eq, first_div)

    def test_perm_world_exercises_relinquishment(self):
        # the frozen host control relinquishes once per individual on all 8 seeds
        for seed in range(8):
            r = ac96.run(seed, 0, 'gated', True, False, 'perm', streak_maintained=False)
            self.assertEqual(r['relinquishments'], 1, f'seed {seed}: world does not fire the drop')
        # the maintained arm relinquishes on SOME individuals -- the fix is exercised, and the
        # divergence (paid-write starvation in the material-starved move transient) is a finding,
        # recorded here as a lower-bound style assertion rather than hidden.
        counts = [ac96.run(seed, 0, 'gated', True, False, 'perm', streak_maintained=True)['relinquishments']
                  for seed in range(8)]
        self.assertTrue(any(c > 0 for c in counts), 'the maintained arm never exercises the drop')


class TestSeedDisjointness(unittest.TestCase):
    """The final family 4412-4415 is disjoint from engineering 0-7 and every prior final
    family <= 4411, and matches the frozen results.json."""

    def test_final_seeds_disjoint(self):
        finals = [4412, 4413, 4414, 4415]
        self.assertTrue(set(finals).isdisjoint(range(8)), 'finals overlap engineering 0-7')
        self.assertTrue(set(finals).isdisjoint(range(4412)), 'finals not disjoint from <= 4411')

    def test_results_seeds_match(self):
        results = json.loads(Path('ac96_results_v1/results.json').read_text())
        self.assertEqual(results['seeds'], [4412, 4413, 4414, 4415])
        self.assertEqual(results['transition'], 'perm')
        self.assertEqual(len(results['rows']), 4 * 2 * 3)


class TestObserverDiscardFinals(unittest.TestCase):
    """G1 on the finals: observer-discard (succession observer + host streak dict) at a mid-streak
    tick is byte-identical on every final seed."""

    def test_mid_streak_swap_byte_identical_on_finals(self):
        for seed in (4412, 4413, 4414, 4415):
            d = ac96.observer_discard_equivalence(seed, 0)
            self.assertNotEqual(d.get('status'), 'no_mid_streak', f'seed {seed}: no mid-streak tick')
            self.assertTrue(d['swap_applied'], f'seed {seed}: swap hook never fired')
            self.assertEqual(d['streak_at_swap'], 2, f'seed {seed}: swap not at a non-zero streak')
            self.assertTrue(d['identical'], f'seed {seed}: observer-discard changed the trajectory')


if __name__ == '__main__':
    unittest.main()
