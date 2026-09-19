"""AC94-D2 tests: the pointer/phase atomic-switch fix (commit_switch).

Pins, at the single-step level, that a refused SWITCH->REMOVE transition never advances the
pointer alone (the AC94-D1 defect), that pointer+MODE commit atomically under the W cap, and that
switch_tick (and the other phase-transition log fields) are recorded only when the write actually
committed. Also re-runs the ungated comparator equivalence (ungated == frozen AC92, 32/32) so the
fix is proven to be the ONLY change. Not hashed (AC17's rule) -- verification tool only.
"""
import unittest
from pathlib import Path
import numpy as np
import ac4
import ac9
import ac12
import ac94


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac94.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _switch_org(seed=0, W=2, source=0):
    """Build an organism in PHASE_SWITCH with a valid, equal source/target slot pair, pointer at
    `source`, and `W` live catalysts inside the boundary. source=0, target=(source+1)%4 holds a
    duplicate of the active slot, so the SWITCH branch's validity precondition passes."""
    o, offs = ac12.acquire(seed)
    _, _, _, priority = ac4.acquire(seed)
    encoded = ac94.description_bits(priority)
    o.body.traces[1, :ac94.DESC_BITS] = encoded[:, None]
    target = (source + 1) % ac94.SLOTS
    o.body.traces[1, ac94.slot_offset(target):ac94.slot_offset(target) + ac94.SLOT_BITS] = encoded[:, None]
    o.body.traces[1, ac94.PTR_OFFS] = 0
    o.body.traces[1, ac94.PTR_OFFS[0] + 0] = (source >> 1) & 1
    o.body.traces[1, ac94.PTR_OFFS[1]] = source & 1
    o.body.traces[1, ac94.CTRL_OFFS] = ac94.encode_ctrl(1, ac94.PHASE_SWITCH, 0)[:, None]
    o.body.life[:4] = [64] * W + [0] * (4 - W)
    o.body.pos[:4] = 0
    o.body.energy = 200
    o.body.material = 200
    succ = ac94.Succession('real', encoded)
    succ._entry = dict(n=0, source=source, target=target, start=0, source_correct=1)
    return o, offs, succ


class TestCommitSwitchAtomicity(unittest.TestCase):
    def test_W2_refuses_both_writes(self):
        # W=2 => cap 16; SWITCH->REMOVE is 21 replicas > 16, so the atomic commit refuses BOTH
        # the pointer advance and the MODE transition (the AC94-D1 defect is closed).
        o, _, _ = _switch_org(0, W=2)
        ptr_before = ac94.read_pointer(o)
        ctrl_before = ac94.read_ctrl(o)
        e = ac9.event()
        n = ac94.commit_switch(o, e, target=1, last=0)
        self.assertEqual(n, 0, 'refused transition returns 0 MODE replicas')
        self.assertEqual(ac94.read_pointer(o), ptr_before, 'pointer must NOT advance on refusal')
        self.assertEqual(ac94.read_ctrl(o).tolist(), ctrl_before.tolist(), 'MODE must NOT change')
        self.assertEqual(e.get('succ_writes', 0), 0)
        self.assertEqual(e.get('ctrl_writes', 0), 0)
        self.assertEqual(e['spent_e'], 0); self.assertEqual(e['spent_m'], 0)

    def test_W3_commits_both_writes(self):
        # W=3 => cap 24; 21 <= 24, so pointer AND MODE commit together in one atomic transition.
        o, _, _ = _switch_org(0, W=3)
        e = ac9.event()
        n = ac94.commit_switch(o, e, target=1, last=0)
        self.assertGreater(n, 0, 'committed transition writes MODE replicas')
        self.assertEqual(ac94.read_pointer(o), 1, 'pointer advanced to target')
        _, phase, _ = ac94.ctrl_fields(o)
        self.assertEqual(phase, ac94.PHASE_REMOVE, 'phase committed to REMOVE')

    def test_W0_refuses_both_writes(self):
        # W=0 => cap 0; nothing is affordable, so the atomic commit refuses the whole transition.
        o, _, _ = _switch_org(0, W=0)
        ptr_before = ac94.read_pointer(o)
        e = ac9.event()
        n = ac94.commit_switch(o, e, target=1, last=0)
        self.assertEqual(n, 0)
        self.assertEqual(ac94.read_pointer(o), ptr_before)
        self.assertEqual(e['spent_e'], 0); self.assertEqual(e['spent_m'], 0)

    def test_joint_funding_refuses_when_energy_short(self):
        # even at W=3, if the organism cannot jointly fund BOTH writes this tick (energy <
        # n_ptr + n_mode), the whole transition is refused rather than advancing the pointer
        # alone (the energy/material side of the same defect class).
        o, _, _ = _switch_org(0, W=3)
        o.body.energy = 20   # 7 pointer + 21 MODE = 28 > 20
        ptr_before = ac94.read_pointer(o)
        e = ac9.event()
        n = ac94.commit_switch(o, e, target=1, last=0)
        self.assertEqual(n, 0)
        self.assertEqual(ac94.read_pointer(o), ptr_before)

    def test_refused_transition_never_advances_pointer_alone(self):
        # the named invariant: across W in {0,1,2} the atomic commit never advances the pointer
        # without also committing the MODE transition.
        for W in (0, 1, 2):
            o, _, _ = _switch_org(0, W=W)
            ptr_before = ac94.read_pointer(o)
            n = ac94.commit_switch(o, ac9.event(), target=1, last=0)
            self.assertEqual(n, 0, f'W={W} should refuse')
            self.assertEqual(ac94.read_pointer(o), ptr_before,
                             f'W={W}: pointer advanced alone')


class TestSwitchTickOnCommit(unittest.TestCase):
    def test_switch_tick_not_logged_on_refusal(self):
        # at W=2 the transition is refused, so advance() must NOT record switch_tick.
        o, _, succ = _switch_org(0, W=2)
        e = ac9.event()
        ac94.advance(o, e, succ, 1000, succ_trigger=True, gate_ctrl=True)
        self.assertNotIn('switch_tick', succ._entry, 'refused switch must not be logged')

    def test_switch_tick_logged_on_commit(self):
        # at W=3 the transition commits, so switch_tick == now.
        o, _, succ = _switch_org(0, W=3)
        e = ac9.event()
        ac94.advance(o, e, succ, 1000, succ_trigger=True, gate_ctrl=True)
        self.assertEqual(succ._entry.get('switch_tick'), 1000)
        _, phase, _ = ac94.ctrl_fields(o)
        self.assertEqual(phase, ac94.PHASE_REMOVE)

    def test_remove_tick_only_on_idle_commit(self):
        # the same rule for the REMOVE->IDLE transition: a refused IDLE write must not mark the
        # succession done. W=1 => cap 8 < the 14-replica IDLE transition, so it is refused.
        o, _, succ = _switch_org(0, W=1)
        # put the machine in PHASE_REMOVE with pointer -> 1 (old_source = 0) and slot 0 EMPTY, so
        # the IDLE transition is actually attempted this tick.
        o.body.traces[1, ac94.slot_offset(0):ac94.slot_offset(0) + ac94.SLOT_BITS] = 0
        o.body.traces[1, ac94.CTRL_OFFS] = ac94.encode_ctrl(1, ac94.PHASE_REMOVE, 0)[:, None]
        o.body.traces[1, ac94.PTR_OFFS] = 0
        o.body.traces[1, ac94.PTR_OFFS[1]] = 1   # pointer -> 1 (so old_source = 0)
        succ._entry = dict(n=0, source=1, target=2, start=0)
        e = ac9.event()
        ac94.advance(o, e, succ, 2000, succ_trigger=True, gate_ctrl=True)
        self.assertNotIn('remove_tick', succ._entry, 'refused IDLE must not be logged as removed')
        self.assertNotIn('done', succ._entry)
        self.assertEqual(len(succ.log), 0)
        _, phase, _ = ac94.ctrl_fields(o)
        self.assertEqual(phase, ac94.PHASE_REMOVE, 'phase must stay REMOVE after a refused IDLE')


class TestComparatorEquivalence(unittest.TestCase):
    def test_ungated_byte_identical_to_frozen_ac92(self):
        # the fix is the ONLY change: the ungated arm must still reproduce frozen AC92 intact
        # byte-for-byte (32/32 state_hash).
        n = ac94.equivalence_check()
        self.assertEqual(n, 32)


class TestArmConfig(unittest.TestCase):
    def test_arms_preserved(self):
        # the D4 arm set: the fixed architecture + the split/ungated rivals + the two timer arms.
        self.assertEqual(ac94.ARMS,
                         ('gated', 'split', 'ungated', 'ungated_block', 'timer_block', 'timer_rescue'))
        self.assertTrue(ac94.ARM_PARTS['gated']['gate_ctrl'])
        self.assertTrue(ac94.ARM_PARTS['gated']['atomic_switch'])
        self.assertFalse(ac94.ARM_PARTS['ungated']['gate_ctrl'])
        self.assertFalse(ac94.ARM_PARTS['ungated']['atomic_switch'])
        # the split rival differs from gated ONLY in the switch mechanism (atomic_switch=False).
        self.assertTrue(ac94.ARM_PARTS['split']['gate_ctrl'])
        self.assertFalse(ac94.ARM_PARTS['split']['atomic_switch'])
        for k in ('ac_arm', 'repair', 'regen', 'succession', 'ctrl_maintain', 'gate_ctrl'):
            self.assertEqual(ac94.ARM_PARTS['gated'][k], ac94.ARM_PARTS['split'][k])
        for k in ('ac_arm', 'repair', 'regen', 'succession', 'ctrl_maintain'):
            self.assertEqual(ac94.ARM_PARTS['gated'][k], ac94.ARM_PARTS['ungated'][k])
        # the ungated_block rival is ungated + a W cut (rate limiter is the W-independent timestamp).
        self.assertFalse(ac94.ARM_PARTS['ungated_block']['gate_ctrl'])
        self.assertTrue(ac94.ARM_PARTS['ungated_block']['block_W'])
        # timer arms are the gated architecture + a W cut; only the restore differs.
        for a in ('timer_block', 'timer_rescue'):
            self.assertTrue(ac94.ARM_PARTS[a]['gate_ctrl'])
            self.assertTrue(ac94.ARM_PARTS[a]['atomic_switch'])
            self.assertTrue(ac94.ARM_PARTS[a]['block_W'])
            self.assertEqual(ac94.ARM_PARTS[a]['block_tick'], ac94.TIMER_BLOCK_TICK)
        self.assertIsNone(ac94.ARM_PARTS['timer_block']['restore_tick'])
        self.assertEqual(ac94.ARM_PARTS['timer_rescue']['restore_tick'], ac94.TIMER_RESCUE_TICK)


class TestSplitRival(unittest.TestCase):
    def test_split_advances_pointer_alone_at_W2(self):
        # at W=2 the split rival's two-step switch advances the pointer while the 21-replica MODE
        # transition is refused (the D1 defect), increments split_events, and logs switch_tick on
        # the refusal.
        o, _, succ = _switch_org(0, W=2)
        e = ac9.event()
        ac94.advance(o, e, succ, 1000, succ_trigger=True, gate_ctrl=True, atomic_switch=False)
        self.assertEqual(ac94.read_pointer(o), 1, 'split rival advances the pointer alone')
        _, phase, _ = ac94.ctrl_fields(o)
        self.assertEqual(phase, ac94.PHASE_SWITCH, 'MODE transition was refused (phase stays SWITCH)')
        self.assertEqual(e.get('split_events', 0), 1, 'the split event is recorded')
        self.assertEqual(succ._entry.get('switch_tick'), 1000, 'switch_tick logged on refusal')

    def test_atomic_never_splits(self):
        # the same organism at W=2 with the atomic switch refuses BOTH writes -- no split, no
        # switch_tick on refusal.
        o, _, succ = _switch_org(0, W=2)
        e = ac9.event()
        ac94.advance(o, e, succ, 1000, succ_trigger=True, gate_ctrl=True, atomic_switch=True)
        self.assertEqual(ac94.read_pointer(o), 0, 'atomic switch does not advance the pointer alone')
        self.assertEqual(e.get('split_events', 0), 0)
        self.assertNotIn('switch_tick', succ._entry, 'no switch_tick on a refused atomic transition')


class TestSeedDisjointness(unittest.TestCase):
    def test_final_seeds_fresh_and_disjoint(self):
        # the D4 finals are 4404-4407: disjoint from engineering 0-7 and every prior final family
        # <= 4403 (AC75..AC93) and the separate 4600-4871 order-line families.
        finals = {4404, 4405, 4406, 4407}
        self.assertTrue(finals.isdisjoint(range(8)), 'finals must not reuse engineering 0-7')
        self.assertTrue(finals.isdisjoint(range(4404)), 'finals must be > 4403')
        prior = (set(range(2900, 2904)) | set(range(3000, 3004)) | set(range(4004, 4032))
                 | {4052, 4054, 4096, 4110} | set(range(4200, 4204)) | set(range(4300, 4304))
                 | set(range(4400, 4404)))
        self.assertTrue(finals.isdisjoint(prior), 'finals must not reuse any prior final family')



def _timer_org(seed=0, W=3):
    """Minimal organism with the D3 counter at 0, `W` live bank-0 catalysts, and enough energy/
    material to fund timer writes. The description/program are not needed by the timer primitives."""
    o, offs = ac12.acquire(seed)
    _, _, _, priority = ac4.acquire(seed)
    encoded = ac94.description_bits(priority)
    o.body.traces[1, :ac94.DESC_BITS] = encoded[:, None]
    o.body.traces[1, ac94.CTRL_OFFS] = 0        # MODE idle, counter all-zero
    o.body.life[:4] = [64] * W + [0] * (4 - W)
    o.body.pos[:4] = 0
    o.body.energy = 300
    o.body.material = 300
    return o, offs


class TestTimerPrimitives(unittest.TestCase):
    def test_counter_starts_at_zero(self):
        o, _ = _timer_org(0, W=3)
        self.assertEqual(ac94.timer_value(o), 0)

    def test_increment_sets_lowest_clear_bit_atomic(self):
        o, _ = _timer_org(0, W=3)
        e = ac9.event()
        for _ in range(ac94.TIMER_MAX):
            n = ac94.increment_timer(o, e)
            self.assertGreater(n, 0, 'each increment writes at least one replica')
        self.assertEqual(ac94.timer_value(o), ac94.TIMER_MAX)
        # already full: no further advance
        n = ac94.increment_timer(o, e)
        self.assertEqual(n, 0)
        self.assertEqual(ac94.timer_value(o), ac94.TIMER_MAX)

    def test_increment_refuses_at_W0(self):
        # machinery-dependence: at W=0 the counter cannot advance (atomic refusal).
        o, _ = _timer_org(0, W=0)
        e = ac9.event()
        n = ac94.increment_timer(o, e)
        self.assertEqual(n, 0)
        self.assertEqual(ac94.timer_value(o), 0)
        self.assertEqual(e.get('timer_increments', 0), 0)
        self.assertEqual(e['spent_e'], 0)

    def test_reset_is_resumable_and_W_gated(self):
        # a full counter (TIMER_MAX set bits) is cleared incrementally at W=3, refused at W=0.
        o, _ = _timer_org(0, W=3)
        o.body.traces[1, ac94.CTRL_OFFS[4:4 + ac94.TIMER_BITS]] = 1
        self.assertEqual(ac94.timer_value(o), ac94.TIMER_MAX)
        e = ac9.event()
        total = 0
        for _ in range(20):
            total += ac94.reset_timer(o, e)
            if ac94.timer_value(o) == 0:
                break
        self.assertEqual(ac94.timer_value(o), 0)
        self.assertEqual(total, ac94.TIMER_BITS * 7)   # every replica paid exactly once
        # W=0: reset cannot re-arm
        o2, _ = _timer_org(0, W=0)
        o2.body.traces[1, ac94.CTRL_OFFS[4:4 + ac94.TIMER_BITS]] = 1
        e2 = ac9.event()
        self.assertEqual(ac94.reset_timer(o2, e2), 0)
        self.assertEqual(ac94.timer_value(o2), ac94.TIMER_MAX)

    def test_write_ctrl_gated_writes_mode_only(self):
        # the LAST field (former timestamp) is NOT written by write_ctrl on the gated path --
        # the rate limiter is the counter, not a W-independent timestamp write.
        o, _ = _timer_org(0, W=3)
        o.body.traces[1, ac94.CTRL_OFFS[4:18]] = 1   # seed the counter/LAST field with 1s
        e = ac9.event()
        n = ac94.write_ctrl(o, e, ac94.encode_ctrl(1, ac94.PHASE_COPY, 999), gate=True)
        self.assertGreater(n, 0)                       # MODE transition wrote
        # the timer field is untouched by the gated write_ctrl
        self.assertTrue((o.body.traces[1, ac94.CTRL_OFFS[4:18]] == 1).all())
        self.assertEqual(e.get('timer_resets', 0), 0)


if __name__ == '__main__':
    unittest.main()
