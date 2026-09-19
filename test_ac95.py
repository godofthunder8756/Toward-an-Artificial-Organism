"""AC95-D2 tests: the reset-progress flag is carried by maintained state (RIP bit), not a host
dict key, and the succession observer is strictly observational.

Pins, at the single-step level and on the full trajectory, that:
- the reviewer's isolated harness (identical maintained state, observer cleared vs kept) returns the
  SAME counter value and energy spend -- the class-C leak is closed;
- the RIP bit lives in maintained state (CTRL bit 17), is damaged by the ambient stream and repaired
  by reg_ctrl, and the reset completes through it (no host memory);
- deleting the observer (swap_succ_at) leaves the gated trajectory byte-identical;
- the comparator arms are untouched: ungated == frozen AC92 (32/32) and split == frozen AC94 (32/32).

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


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac95.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _fresh(seed=0):
    o, offs = ac12.acquire(seed)
    o.body.energy = 200
    o.body.material = 200
    return o, offs


def _set_ctrl(o, active=0, timer_set=(), rip_val=0, phase=0):
    CTRL = ac95.CTRL_OFFS
    o.body.traces[1, CTRL, :] = 0
    o.body.traces[1, CTRL[0], :] = active & 1
    o.body.traces[1, CTRL[1], :] = (phase >> 2) & 1
    o.body.traces[1, CTRL[2], :] = (phase >> 1) & 1
    o.body.traces[1, CTRL[3], :] = phase & 1
    for i in range(ac95.TIMER_BITS):
        o.body.traces[1, CTRL[4 + i], :] = 1 if i in timer_set else 0
    o.body.traces[1, ac95.RIP_OFFS, :] = rip_val & 1


def _ev():
    e = ac9.event()
    e.update(ctrl_writes=0, succ_writes=0, reg_writes=0, timer_resets=0, timer_increments=0,
             split_events=0)
    return e


class TestReviewerHarnessClosed(unittest.TestCase):
    """The reviewer's isolated harness: identical idle state (counter=5, active=0), the write must
    be independent of the observer object and of the (now-absent) host flag."""

    def _run_harness(self, entry):
        o, _ = _fresh(0)
        _set_ctrl(o, active=0, timer_set=(0, 1, 2, 3, 4), rip_val=0)  # counter=5, idle
        e = _ev()
        succ = ac95.Succession('real', None)
        succ._entry = entry
        ac95.advance(o, e, succ, 200, succ_trigger=False, gate_ctrl=True,
                     atomic_switch=True, timer_maintained=True)
        return ac95.timer_value(o), e['spent_e'], e['ctrl_writes'], e['timer_increments']

    def test_observer_cleared_vs_kept_same_result(self):
        kept = self._run_harness(dict(n=0, source=0, target=1, start=200, source_correct=0))
        cleared = self._run_harness(None)
        self.assertEqual(kept, cleared, 'observer cleared vs kept must steer identical writes')
        # the counter advanced by exactly one bit at the coarse tick: 5 -> 6, 7 replicas paid
        self.assertEqual(kept, (6, 7, 7, 1))

    def test_stale_host_flag_does_not_steer(self):
        # the old class-C flag, if a stale observer still carries it, must NOT change the write.
        flag_false = self._run_harness(dict(n=0, source=0, target=1, start=200,
                                            source_correct=0, timer_reset_done=False))
        flag_true = self._run_harness(dict(n=0, source=0, target=1, start=200,
                                           source_correct=0, timer_reset_done=True))
        self.assertEqual(flag_false, flag_true)
        self.assertEqual(flag_false, (6, 7, 7, 1))


class TestRIPMaintainedState(unittest.TestCase):
    def test_reset_completes_through_the_rip_bit(self):
        # mid-reset organism (RIP=1, counter partway cleared): advance() keeps clearing via the
        # maintained RIP bit until the counter reads 0, then clears the RIP bit -- no host memory.
        o, _ = _fresh(0)
        _set_ctrl(o, active=1, timer_set=(3, 4, 5, 6), rip_val=1, phase=ac95.PHASE_COPY)
        e = _ev()
        succ = ac95.Succession('real', None)
        succ._entry = dict(n=0, source=0, target=1, start=0, source_correct=0)
        # keep driving until the reset completes (counter 0 and RIP cleared)
        for _ in range(40):
            if ac95.timer_value(o) == 0 and ac95.rip(o) == 0:
                break
            ac95.advance(o, e, succ, 0, succ_trigger=False, gate_ctrl=True,
                         atomic_switch=True, timer_maintained=True)
        self.assertEqual(ac95.timer_value(o), 0, 'counter fully reset')
        self.assertEqual(ac95.rip(o), 0, 'RIP bit cleared once the reset is done')

    def test_rip_bit_damaged_and_repaired_by_reg_ctrl(self):
        # RIP=0 with 2 sticky-damaged replicas set: reg_ctrl (fired on ctrl minority >= 2) repairs
        # them back to the majority (0). The RIP bit is vulnerable and paid-maintained like the rest.
        o, _ = _fresh(0)
        _set_ctrl(o, active=0, timer_set=(), rip_val=0)
        o.body.traces[1, ac95.RIP_OFFS, 0:2] = 1          # sticky-SET damage: 2 minority replicas
        self.assertEqual(ac95.rip(o), 0, 'majority still reads 0 (2 < 4)')
        e = _ev()
        ac95.reg_ctrl(o, e)
        self.assertEqual(int(o.body.traces[1, ac95.RIP_OFFS].sum()), 0, 'reg_ctrl repaired the RIP bit')

    def test_rip_bit_write_is_w_gated_and_paid(self):
        # at W=0 the RIP write is refused whole (atomic, machinery-dependent); at W=3 it commits
        # and pays energy + material per replica.
        o, _ = _fresh(0)
        _set_ctrl(o, active=0, timer_set=(), rip_val=0)
        o.body.life[:4] = 0                                # W=0
        e = _ev()
        n = ac95.write_rip(o, e, 1)
        self.assertEqual(n, 0, 'W=0 refuses the RIP write')
        self.assertEqual(ac95.rip(o), 0)
        self.assertEqual(e['spent_e'], 0)
        o2, _ = _fresh(0)
        _set_ctrl(o2, active=0, timer_set=(), rip_val=0)
        o2.body.life[:4] = [64, 64, 64, 0]                 # W=3
        e2 = _ev()
        n2 = ac95.write_rip(o2, e2, 1)
        self.assertEqual(n2, 7)
        self.assertEqual(ac95.rip(o2), 1)
        self.assertEqual(e2['spent_e'], 7)
        self.assertEqual(e2['spent_m'], 7)


class TestObserverDiscardEquivalence(unittest.TestCase):
    """Replacing the succession observer with a fresh object at a mid-run tick leaves the fixed
    architecture's trajectory byte-identical (the observer is strictly observational)."""

    def test_gated_trajectory_identical_under_observer_discard(self):
        base = ac95.run(0, 0, 'gated', True, False, 'none')
        for swap in (2000, 8192):
            r = ac95.run(0, 0, 'gated', True, False, 'none', swap_succ_at=swap)
            self.assertEqual(r['state_hash'], base['state_hash'],
                             f'gated trajectory diverged after observer discard at {swap}')


class TestResetInterruption(unittest.TestCase):
    """AC95-D3: the multi-tick reset freezes when W is cut mid-way and resumes from maintained
    state alone when W is restored -- no host-side reset phase."""

    def test_cut_W_is_machinery_only(self):
        o, _ = _fresh(0)
        _set_ctrl(o, active=1, timer_set=(0, 1, 2, 3, 4, 5, 6), rip_val=1, phase=ac95.PHASE_COPY)
        before_traces = o.body.traces.copy()
        before_inv = ac95.ac4.inventory(o.body)
        ac95.cut_W(o)
        self.assertEqual(int((o.body.life[:4] > 0).sum()), 0, 'W zeroed')
        self.assertTrue(np.array_equal(o.body.traces, before_traces),
                        'cut_W must not touch content (traces)')
        # energy/material/fuel are untouched; the live-particle count (inv[3]) legitimately drops
        # because W itself is removed -- that is the cut, not a content leak.
        self.assertEqual(ac95.ac4.inventory(o.body)[:3], before_inv[:3],
                         'cut_W must not touch energy/material/fuel')

    def test_reset_frozen_at_W0(self):
        # mid-reset organism (RIP=1, counter part-way at 4) with W=0: the reset writes nothing.
        o, _ = _fresh(0)
        _set_ctrl(o, active=1, timer_set=(3, 4, 5, 6), rip_val=1, phase=ac95.PHASE_COPY)
        o.body.life[:4] = 0
        e = _ev()
        succ = ac95.Succession('real', None)
        succ._entry = dict(n=0, source=0, target=1, start=0, source_correct=0)
        ac95.advance(o, e, succ, 0, succ_trigger=False, gate_ctrl=True,
                     atomic_switch=True, timer_maintained=True)
        self.assertEqual(ac95.timer_value(o), 4, 'reset must not progress at W=0')
        self.assertEqual(e['timer_resets'], 0)

    def test_reset_block_freezes_mid_reset(self):
        for seed in (0, 1):
            r = ac95.run(seed, 0, 'reset_block', True, False, 'none')
            self.assertTrue(r['reset_froze'], f'seed {seed}: reset must freeze part-way')
            self.assertTrue(0 < r['reset_progress_at_cut'] < ac95.TIMER_MAX,
                            f'seed {seed}: cut landed part-way (got {r["reset_progress_at_cut"]})')
            self.assertIsNone(r['reset_completed_tick'],
                              f'seed {seed}: reset must not complete without W (no host memory)')
            self.assertEqual(r['successions'], 0, f'seed {seed}: interrupted succession never completes')

    def test_reset_rescue_resumes_and_completes(self):
        for seed in (0, 1):
            r = ac95.run(seed, 0, 'reset_rescue', True, False, 'none')
            self.assertTrue(r['reset_froze'], f'seed {seed}: reset froze before rescue')
            self.assertIsNotNone(r['reset_completed_tick'],
                                 f'seed {seed}: reset completed after rescue')
            self.assertGreater(r['reset_completed_tick'], r['reset_start'] + ac95.RESET_CUT_OFFSET,
                               f'seed {seed}: completion must be after the cut')
            self.assertTrue(r['completed'], f'seed {seed}: organism survives the interruption')
            self.assertGreaterEqual(r['successions'], 4,
                                    f'seed {seed}: succession fires at the healthy rate')

    def test_reset_rescue_observer_discard_identical(self):
        for seed in (0, 1):
            base = ac95.run(seed, 0, 'reset_rescue', True, False, 'none')
            swap = ac95.run(seed, 0, 'reset_rescue', True, False, 'none', swap_succ_at='rescue')
            self.assertEqual(swap['state_hash'], base['state_hash'],
                             f'seed {seed}: observer discard at the rescue tick diverged')


class TestComparatorByteIdentity(unittest.TestCase):
    def test_ungated_byte_identical_to_frozen_ac92(self):
        n = ac95.equivalence_check()
        self.assertEqual(n, 32)

    def test_split_byte_identical_to_frozen_ac94(self):
        frozen = [json.loads(l)
                  for l in Path('ac94_results_v1/rows.jsonl').read_text().splitlines()]
        seeds = [4404, 4405, 4406, 4407]
        n = 0
        for seed in seeds:
            for history in (0, 1):
                for damage in (True, False):
                    for corrupt in (True, False):
                        want = [r for r in frozen
                                if r['seed'] == seed and r['history'] == history
                                and r['arm'] == 'split' and r['damage'] == damage
                                and r['corrupt'] == corrupt]
                        if not want:
                            continue
                        got = ac95.run(seed, history, 'split', damage, corrupt, 'none')
                        self.assertEqual(got['state_hash'], want[0]['state_hash'],
                                         f'split mismatch {seed}/{history}/{damage}/{corrupt}')
                        n += 1
        self.assertEqual(n, 32)


class TestArmConfig(unittest.TestCase):
    def test_timer_maintained_flags(self):
        self.assertTrue(ac95.ARM_PARTS['gated']['timer_maintained'])
        self.assertTrue(ac95.ARM_PARTS['timer_block']['timer_maintained'])
        self.assertTrue(ac95.ARM_PARTS['timer_rescue']['timer_maintained'])
        self.assertFalse(ac95.ARM_PARTS['split']['timer_maintained'])
        self.assertFalse(ac95.ARM_PARTS['ungated']['timer_maintained'])
        self.assertFalse(ac95.ARM_PARTS['ungated_block']['timer_maintained'])

    def test_split_differs_from_gated_only_in_switch_and_timer_flag(self):
        g = ac95.ARM_PARTS['gated']; s = ac95.ARM_PARTS['split']
        for k in ('ac_arm', 'repair', 'regen', 'succession', 'ctrl_maintain', 'gate_ctrl'):
            self.assertEqual(g[k], s[k])
        self.assertTrue(g['atomic_switch']); self.assertFalse(s['atomic_switch'])
        self.assertTrue(g['timer_maintained']); self.assertFalse(s['timer_maintained'])


class TestObserverDiscardMidSuccession(unittest.TestCase):
    """AC95-D4 G1: the mid-succession observer discard (during an active succession, mid-COPY) is
    byte-identical, and the swap demonstrably fired (the fresh observer re-stamps the in-flight
    succession's start at succ_start + MID_SUCC_OFFSET)."""

    def test_gated_mid_succession_discard_byte_identical(self):
        for seed in (0, 1):
            base = ac95.run(seed, 0, 'gated', True, True, 'none')
            swap = ac95.run(seed, 0, 'gated', True, True, 'none', swap_succ_at='mid_succession')
            self.assertEqual(swap['state_hash'], base['state_hash'],
                             f'seed {seed}: mid-succession observer discard diverged')
            # the observer was actually discarded: the fresh observer re-stamped the in-flight
            # succession's start at a later tick than the true succession start.
            self.assertNotEqual(swap['succession_log'][0]['start'],
                                base['succession_log'][0]['start'],
                                f'seed {seed}: the mid-succession swap never fired')


class TestFinalSeedDisjointness(unittest.TestCase):
    def test_final_seeds_disjoint_from_engineering_and_prior_families(self):
        finals = [4408, 4409, 4410, 4411]
        self.assertEqual(len(set(finals)), 4)
        self.assertTrue(set(finals).isdisjoint(range(8)), 'finals overlap engineering 0-7')
        self.assertTrue(set(finals).isdisjoint(range(4408)), 'finals not disjoint from <= 4407')


if __name__ == '__main__':
    unittest.main()
