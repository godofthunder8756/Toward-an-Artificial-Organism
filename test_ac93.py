"""AC93 tests: the write_ctrl gate toggle (gated MODE refuses under W=0, ungated writes on energy+
material alone), the MODE atomicity under _cap, the LAST budget difference, the low-bit-first
partial-write fact, and the arm config. Not hashed (AC17's rule). Engineering only -- the
clean-control identity is recorded, not gated here."""
import unittest
import json
from pathlib import Path
import numpy as np
import ac4
import ac9
import ac12
import ac93


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac93.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _org(seed=0, W_zero=False):
    o, offs = ac12.acquire(seed)
    _, _, _, priority = ac4.acquire(seed)
    o.body.traces[1, :ac93.DESC_BITS] = ac93.description_bits(priority)[:, None]
    o.body.energy = 200
    o.body.material = 200
    if W_zero:
        o.body.life[:4] = 0
    return o, offs


class TestArmConfig(unittest.TestCase):
    def test_arms(self):
        self.assertEqual(ac93.ARMS, ('gated', 'ungated', 'W_block', 'W_rescue', 'W_block_ungated'))
        self.assertTrue(ac93.ARM_PARTS['gated']['gate_ctrl'])
        self.assertFalse(ac93.ARM_PARTS['ungated']['gate_ctrl'])
        # both arms otherwise share the same world config (regen/repair/succession/ctrl_maintain)
        for k in ('ac_arm', 'repair', 'regen', 'succession', 'ctrl_maintain'):
            self.assertEqual(ac93.ARM_PARTS['gated'][k], ac93.ARM_PARTS['ungated'][k])
        # D3 arms: W_block/W_rescue force the succession, block W, are gated, and differ only in
        # whether the machinery is restored (direct_restore / restore_tick).
        for arm in ('W_block', 'W_rescue'):
            self.assertTrue(ac93.ARM_PARTS[arm]['gate_ctrl'])
            self.assertTrue(ac93.ARM_PARTS[arm]['force_succession'])
            self.assertTrue(ac93.ARM_PARTS[arm]['block_W'])
            self.assertEqual(ac93.ARM_PARTS[arm]['block_tick'], ac93.FORCE_TICK)
        self.assertFalse(ac93.ARM_PARTS['W_block']['direct_restore'])
        self.assertIsNone(ac93.ARM_PARTS['W_block']['restore_tick'])
        self.assertTrue(ac93.ARM_PARTS['W_rescue']['direct_restore'])
        self.assertEqual(ac93.ARM_PARTS['W_rescue']['restore_tick'], ac93.RESCUE_TICK)
        # D4 rival: W_block_ungated is the UNGATED architecture under the same W cut (gate_ctrl
        # False), differing from W_block ONLY in the gate toggle -- the direct rival that pins the
        # stall as the copy, not the gate.
        self.assertFalse(ac93.ARM_PARTS['W_block_ungated']['gate_ctrl'])
        self.assertTrue(ac93.ARM_PARTS['W_block_ungated']['force_succession'])
        self.assertTrue(ac93.ARM_PARTS['W_block_ungated']['block_W'])
        self.assertEqual(ac93.ARM_PARTS['W_block_ungated']['block_tick'], ac93.FORCE_TICK)
        self.assertIsNone(ac93.ARM_PARTS['W_block_ungated']['restore_tick'])
        self.assertFalse(ac93.ARM_PARTS['W_block_ungated']['direct_restore'])
        for k in ('ac_arm', 'repair', 'regen', 'succession', 'ctrl_maintain',
                  'force_succession', 'block_W', 'block_tick', 'restore_tick', 'direct_restore'):
            self.assertEqual(ac93.ARM_PARTS['W_block'][k], ac93.ARM_PARTS['W_block_ungated'][k])


class TestWriteCtrlGate(unittest.TestCase):
    def test_gated_mode_refuses_with_W_zero(self):
        # gated: W == 0 => _cap == 0, so even a full mode transition is refused (atomic)
        o, _ = _org(0, W_zero=True)
        o.body.traces[1, ac93.CTRL_OFFS] = 0
        e = ac9.event()
        n = ac93.write_ctrl(o, e, ac93.encode_ctrl(1, ac93.PHASE_COPY, 0), gate=True)
        self.assertEqual(n, 0)
        self.assertEqual(e.get('ctrl_writes', 0), 0)
        self.assertEqual(e['spent_e'], 0); self.assertEqual(e['spent_m'], 0)
        # and nothing was written
        self.assertEqual(int(o.body.traces[1, ac93.CTRL_OFFS].sum()), 0)

    def test_ungated_mode_writes_with_W_zero(self):
        # ungated (frozen comparator): W == 0 but energy/material available => the coordinator
        # transition write proceeds on energy + material alone (the distinct-resource model)
        o, _ = _org(0, W_zero=True)
        o.body.traces[1, ac93.CTRL_OFFS] = 0
        e = ac9.event()
        n = ac93.write_ctrl(o, e, ac93.encode_ctrl(1, ac93.PHASE_COPY, 0), gate=False)
        self.assertGreater(n, 0)
        self.assertGreater(e.get('ctrl_writes', 0), 0)

    def test_gated_mode_atomic_under_cap(self):
        # gated: a mode transition larger than _cap is refused whole (never a partial mode).
        # W=1 => cap=8; PHASE_SWITCH from 0 flips 3 bits (21 replicas) > 8, so refuse everything.
        o, _ = _org(0)
        o.body.life[:4] = [64, 0, 0, 0]   # exactly one live W catalyst inside the boundary
        o.body.pos[:4] = 0
        o.body.traces[1, ac93.CTRL_OFFS] = 0
        before = o.body.traces[1, ac93.CTRL_OFFS].copy()
        e = ac9.event()
        n = ac93.write_ctrl(o, e, ac93.encode_ctrl(1, ac93.PHASE_SWITCH, 0), gate=True)
        self.assertEqual(n, 0)
        self.assertEqual(e.get('ctrl_writes', 0), 0)
        np.testing.assert_array_equal(o.body.traces[1, ac93.CTRL_OFFS], before)

    def test_last_budget_is_w_independent(self):
        # E2 amendment: the LAST (timestamp) field is rate-limit BOOKKEEPING, budgeted by energy +
        # material alone, NEVER W-gated. A 14-bit all-ones timestamp transition (98 replicas) is
        # written FULLY in BOTH arms even though it exceeds 8*W=24 -- the gate only affects the
        # MODE field. (Under E1's pre-amendment rule gated would write 24, truncating the timestamp
        # and breaking the SUCC_MIN_SPACING rate limiter.)
        o, _ = _org(0)
        o.body.traces[1, ac93.CTRL_OFFS] = 0
        e = ac9.event()
        target = ac93.encode_ctrl(0, ac93.PHASE_IDLE, 16383)  # all 14 LAST bits set, MODE unchanged
        n_gated = ac93.write_ctrl(o, e, target, gate=True)
        self.assertEqual(n_gated, 98)    # 0 mode replicas + 98 LAST replicas (full timestamp)
        o2, _ = _org(0)
        o2.body.traces[1, ac93.CTRL_OFFS] = 0
        e2 = ac9.event()
        n_ungated = ac93.write_ctrl(o2, e2, target, gate=False)
        self.assertEqual(n_ungated, 98)  # identical: LAST is never W-gated in either arm

    def test_mode_still_gated_with_W_zero(self):
        # the load-bearing part of the split: at W == 0 the MODE transition is refused (atomic)
        # while the LAST timestamp would still be affordable. Pin that a full mode transition is
        # refused under the gate with W == 0 (already covered above), and that LAST + MODE together
        # are both skipped when MODE is refused (the AC88 return-early behaviour, preserved).
        o, _ = _org(0, W_zero=True)
        o.body.traces[1, ac93.CTRL_OFFS] = 0
        e = ac9.event()
        target = ac93.encode_ctrl(1, ac93.PHASE_COPY, 16383)   # mode transition + full timestamp
        n = ac93.write_ctrl(o, e, target, gate=True)
        self.assertEqual(n, 0)                                   # MODE refused -> whole write skipped
        self.assertEqual(int(o.body.traces[1, ac93.CTRL_OFFS].sum()), 0)

    def test_gate_binds_gradedly_in_W(self):
        # the gate is graded in the W population (E3): the 21-replica SWITCH->REMOVE transition
        # (phase 011 -> 100, 3 bits) exceeds 8*W at W=2 (16) and is refused atomic, but proceeds at
        # W=3 (24). This is the gate's organism-level signature, pinned at the single-step level.
        from_sw = ac93.encode_ctrl(1, ac93.PHASE_SWITCH, 0)
        to_rm = ac93.encode_ctrl(1, ac93.PHASE_REMOVE, 0)
        o2, _ = _org(0)
        o2.body.life[:4] = [64, 64, 0, 0]; o2.body.pos[:4] = 0
        o2.body.traces[1, ac93.CTRL_OFFS] = from_sw[:, None]
        e2 = ac9.event()
        self.assertEqual(ac93.write_ctrl(o2, e2, to_rm, gate=True), 0)   # W=2: 21 > 16 -> refused
        o3, _ = _org(0)
        o3.body.life[:4] = [64, 64, 64, 0]; o3.body.pos[:4] = 0
        o3.body.traces[1, ac93.CTRL_OFFS] = from_sw[:, None]
        e3 = ac9.event()
        self.assertEqual(ac93.write_ctrl(o3, e3, to_rm, gate=True), 21)  # W=3: 21 <= 24 -> written


class TestLowBitFirst(unittest.TestCase):
    def test_last_partial_write_truncates_low_bits(self):
        # np.argwhere over CTRL_OFFS[4:] lists sites in increasing index order => LEAST-significant
        # bit first. A budget-limited LAST write truncates the HIGH-order bits and leaves them at
        # their previous value. Target 16383 (all 14 bits set = 98 replicas), material budget 24:
        # 24 replicas = bits 0,1,2 (7 each) + 3 replicas of bit 3. The majority read is 0b111 = 7;
        # bits 4-13 unwritten. (E1's benign truncation direction -- the ungated arm only ever drops
        # HIGH bits when material briefly dips, leaving a large, near-correct timestamp.)
        o, _ = _org(0)
        o.body.traces[1, ac93.CTRL_OFFS] = 0
        o.body.energy = 24
        o.body.material = 24
        e = ac9.event()
        ac93.write_ctrl(o, e, ac93.encode_ctrl(0, ac93.PHASE_IDLE, 16383), gate=True)
        bits = (o.body.traces[1, ac93.CTRL_OFFS].sum(axis=-1) > 3).astype(np.uint8)
        last = int((bits[4:18] * (1 << np.arange(14))).sum())
        self.assertEqual(last, 0b111)                       # only the low 3 bits reached majority
        self.assertEqual(int(bits[4 + 13]), 0, 'MSB must not be written by a budget-limited LAST write')

    def test_low_bit_first_writes_lsb(self):
        # the LAST write is low-bit-first (np.argwhere over CTRL_OFFS[4:] lists sites in increasing
        # index order), so a material-limited timestamp write truncates the HIGH bits (E1's benign
        # truncation in the ungated arm). Use a 2-bit target with energy/material budget 7: the LSB
        # (bit 0) is written before bit 1.
        o, _ = _org(0)
        o.body.traces[1, ac93.CTRL_OFFS] = 0
        o.body.energy = 7
        o.body.material = 7
        e = ac9.event()
        ac93.write_ctrl(o, e, ac93.encode_ctrl(0, ac93.PHASE_IDLE, 0b11), gate=True)
        bits = (o.body.traces[1, ac93.CTRL_OFFS].sum(axis=-1) > 3).astype(np.uint8)
        self.assertEqual(int(bits[4]), 1, 'LSB written first')
        self.assertEqual(int(bits[5]), 0, 'bit 1 not written under a 7-replica budget')


class TestCleanControlRecorded(unittest.TestCase):
    def test_gate_toggle_flips_with_W_zero(self):
        # the load-bearing difference: gated refuses a mode write at W=0, ungated writes it
        o1, _ = _org(0, W_zero=True); o1.body.traces[1, ac93.CTRL_OFFS] = 0
        e1 = ac9.event()
        n1 = ac93.write_ctrl(o1, e1, ac93.encode_ctrl(1, ac93.PHASE_COPY, 0), gate=True)
        o2, _ = _org(0, W_zero=True); o2.body.traces[1, ac93.CTRL_OFFS] = 0
        e2 = ac9.event()
        n2 = ac93.write_ctrl(o2, e2, ac93.encode_ctrl(1, ac93.PHASE_COPY, 0), gate=False)
        self.assertEqual(n1, 0)
        self.assertGreater(n2, 0)


class TestD3Intervention(unittest.TestCase):
    def test_force_succession_guarantees_dm(self):
        # the deterministic damage pulse sets 2 replicas of the least-damaged correct-0 bit of the
        # active slot, guaranteeing desc_minority_active >= DESC_TRIGGER (2) so a succession fires.
        o, _ = _org(0)
        encoded = ac93.description_bits(ac4.acquire(0)[3])
        dm_before = ac93.desc_minority_active(o)
        set_before = int(o.body.traces[1, :ac93.DESC_BITS].sum())
        ac93.force_succession(o, encoded)
        self.assertGreaterEqual(ac93.desc_minority_active(o), ac93.DESC_TRIGGER)
        self.assertGreaterEqual(ac93.desc_minority_active(o), dm_before)
        # exactly 2 replicas of a correct-0 bit were set (sticky-SET, damage-model-consistent)
        self.assertEqual(int(o.body.traces[1, :ac93.DESC_BITS].sum()), set_before + 2)

    def test_restore_W_machinery_only(self):
        # restore_W touches ONLY the W catalyst population (life[:4], pos[:4]); content, energy,
        # material and fuel are left untouched (the anti-scaffold condition, AC92's shape).
        o, _ = _org(0)
        o.body.life[:4] = [0, 0, 0, 0]
        o.body.pos[:4] = 99
        before_traces = o.body.traces.copy()
        before_e, before_m = o.body.energy, o.body.material
        ac93.restore_W(o)
        np.testing.assert_array_equal(o.body.life[:4], [32, 48, 64, 0])
        np.testing.assert_array_equal(o.body.pos[:4], 0)
        np.testing.assert_array_equal(o.body.traces, before_traces)
        self.assertEqual(o.body.energy, before_e)
        self.assertEqual(o.body.material, before_m)

    def test_make_birth_gates_bank0_only(self):
        # the W-birth gate blocks bank 0 (W) only during [block_tick, restore_tick); banks 1 and 2
        # (region catalysts) are never touched, and it passes through outside the window.
        ns = {'birth': lambda b, bank, parent, e: True, 'now': 0}
        gated = ac93.make_birth(ns, dict(block_W=True, block_tick=100, restore_tick=200))
        self.assertTrue(gated(None, 0, None, {}))          # before block: pass through
        ns['now'] = 150
        self.assertFalse(gated(None, 0, None, {}))         # bank 0 blocked in-window
        self.assertTrue(gated(None, 1, None, {}))          # bank 1 never blocked
        self.assertTrue(gated(None, 2, None, {}))          # bank 2 never blocked
        ns['now'] = 250
        self.assertTrue(gated(None, 0, None, {}))          # after restore: pass through


class TestDeclaredSeeds(unittest.TestCase):
    def test_final_seeds_disjoint(self):
        finals = {4400, 4401, 4402, 4403}
        self.assertTrue(finals.isdisjoint(range(8)), 'finals disjoint from engineering 0-7')
        self.assertTrue(finals.isdisjoint(range(4304)),
                        'finals disjoint from prior final families <= 4303')


class TestGateShapes(unittest.TestCase):
    def test_gate_keys(self):
        self.assertEqual(set(ac93.gates([]).keys()),
                         {'G1_gated_reconstructs', 'G2_ungated_comparator_reconstructs',
                          'G3_gate_inert_at_healthy_fixed_point',
                          'G4_block_stalls_succession_while_alive',
                          'G5_stall_is_the_copy_not_the_gate',
                          'G6_rescue_resumes_succession',
                          'G7_no_damage_controls_complete',
                          'G8_completeness_determinism'})

    def test_G4_categorical(self):
        # the stall gate is categorical per individual: a completed succession must fail it
        good = dict(arm='W_block', damage=True, corrupt=False, transition='none',
                    succession_start_observed=ac93.FORCE_TICK, first_W_empty=2415,
                    phase_at_W_empty=ac93.PHASE_COPY, copy_progress_at_W_empty=500,
                    window_succ_writes=0, window_ctrl_writes=0, phase_changes_during_stall=0,
                    succession_completed=0, description_correct_at_death=130, completed=False,
                    W=0, C=0)
        bad = dict(good, succession_completed=1)
        self.assertTrue(ac93.gates([good])['G4_block_stalls_succession_while_alive'])
        self.assertFalse(ac93.gates([bad])['G4_block_stalls_succession_while_alive'])

    def test_G5_categorical(self):
        # the rival gate is categorical: if the ungated architecture advanced the phase (it does
        # not), the stall would not be "the copy, not the gate"
        good = dict(arm='W_block_ungated', damage=True, corrupt=False, transition='none',
                    succession_start_observed=ac93.FORCE_TICK, first_W_empty=2415,
                    phase_at_W_empty=ac93.PHASE_COPY, window_succ_writes=0, window_ctrl_writes=0,
                    phase_changes_during_stall=0, succession_completed=0,
                    description_correct_at_death=130, completed=False, W=0, C=0)
        bad = dict(good, phase_changes_during_stall=3)
        self.assertTrue(ac93.gates([good])['G5_stall_is_the_copy_not_the_gate'])
        self.assertFalse(ac93.gates([bad])['G5_stall_is_the_copy_not_the_gate'])

    def test_G6_categorical(self):
        good = dict(arm='W_rescue', damage=True, corrupt=False, transition='none',
                    phase_at_rescue=ac93.PHASE_COPY, W_at_rescue=0, window_succ_writes=0,
                    phase_changes_during_stall=0, succession_completed=1,
                    succession_completion_tick=2551, completed=True, W=3, C=2)
        bad = dict(good, succession_completed=0, succession_completion_tick=None)
        self.assertTrue(ac93.gates([good])['G6_rescue_resumes_succession'])
        self.assertFalse(ac93.gates([bad])['G6_rescue_resumes_succession'])


class TestRecordedFreeze(unittest.TestCase):
    @unittest.skipUnless(Path('ac93_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac93_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac93.gates(rows)
        g['G8_completeness_determinism'] = len(rows) == len(results['seeds']) * 2 * 11
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')

    @unittest.skipUnless(Path('ac93_results_v1/results.json').exists(), 'finals not yet run')
    def test_block_machinery_not_content(self):
        # the dying blocked individual loses MACHINERY (W), not content (the description)
        with open('ac93_results_v1/results.json') as f:
            rows = json.load(f)['rows']
        for r in rows:
            if r['arm'] in ('W_block', 'W_block_ungated') and r['damage'] and not r['corrupt']:
                self.assertEqual(r['description_correct_at_death'], 130,
                                 f"{r['arm']} seed {r['seed']}: content must be intact at death")

    @unittest.skipUnless(Path('ac93_results_v1/results.json').exists(), 'finals not yet run')
    def test_rival_stall_identical(self):
        # the direct rival (ungated + W cut) stalls identically to the gated W_block: the stall is
        # the pre-existing copy dependence, not the write_ctrl gate (D4's correction of D3).
        with open('ac93_results_v1/results.json') as f:
            rows = json.load(f)['rows']

        def stall(arm):
            return [(r['first_W_empty'], r['phase_at_W_empty'], r['phase_changes_during_stall'],
                     r['window_succ_writes'], r['window_ctrl_writes'], r['succession_completed'],
                     r['W'], r['C']) for r in rows
                    if r['arm'] == arm and r['damage'] and not r['corrupt']]
        self.assertEqual(stall('W_block'), stall('W_block_ungated'))


if __name__ == '__main__':
    unittest.main()
