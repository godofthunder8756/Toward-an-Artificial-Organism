"""AC92 tests: the W-birth gate (no-op for `intact`, blocks bank-0 only from block_tick, writes no
content), the machinery-only rescue (restore_W touches only life/pos), the W-dependence of the content
writes vs the W-independence of the coordinator transition write, the final-seed disjointness, and the
gate shapes (G1-G5 categorical, per individual). Not hashed (AC17's rule)."""
import unittest
import json
from pathlib import Path
import numpy as np
import ac4
import ac9
import ac12
import ac92


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac92.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _ns():
    return dict(vars(ac9), now=0)


def _org(seed=0, W_zero=False):
    o, offs = ac12.acquire(seed)
    _, _, _, priority = ac4.acquire(seed)
    o.body.traces[1, :ac92.DESC_BITS] = ac92.description_bits(priority)[:, None]
    o.body.energy = 200
    o.body.material = 200
    if W_zero:
        o.body.life[:4] = 0
    return o, offs


class TestGateInjection(unittest.TestCase):
    def test_intact_has_no_gate(self):
        self.assertNotIn('block_W', ac92.ARM_PARTS['intact'],
                         'intact must run the frozen birth (no gate)')

    def test_block_rescue_do_gate(self):
        self.assertTrue(ac92.ARM_PARTS['W_block']['block_W'])
        self.assertTrue(ac92.ARM_PARTS['W_rescue']['block_W'])
        self.assertEqual(ac92.ARM_PARTS['W_block']['restore_tick'], None)
        self.assertEqual(ac92.ARM_PARTS['W_rescue']['restore_tick'], ac92.RESCUE_TICK)
        self.assertTrue(ac92.ARM_PARTS['W_rescue']['direct_restore'])


class TestGateSemantics(unittest.TestCase):
    def test_gate_blocks_from_block_tick_not_zero(self):
        ns = _ns()
        gate = ac92.make_birth(ns, dict(block_W=True, block_tick=8129, restore_tick=None))
        b = ac4.Body(np.zeros((4, 1024, 7), dtype=np.uint8),
                     np.array([32, 48, 64, 0] * 4 + [64, 96, 128, 0], dtype=np.int16),
                     np.zeros((20, 2), dtype=np.int16),
                     np.arange(128, 248, 6, dtype=np.int16))
        b.pos[:] = 0
        b.energy = 100; b.material = 200
        e = ac9.event()
        ns['now'] = 8128
        self.assertTrue(gate(b, 0, 0, e), 'before block_tick the gate must pass through')
        ns['now'] = 8129
        self.assertFalse(gate(b, 0, 0, e), 'from block_tick the gate must block bank-0 births')

    def test_gate_blocks_only_bank0_and_writes_no_content(self):
        ns = _ns()
        gate = ac92.make_birth(ns, dict(block_W=True, block_tick=0, restore_tick=None))
        b = ac4.Body(np.zeros((4, 1024, 7), dtype=np.uint8),
                     np.array([32, 48, 64, 0] * 4 + [64, 96, 128, 0], dtype=np.int16),
                     np.zeros((20, 2), dtype=np.int16),
                     np.arange(128, 248, 6, dtype=np.int16))
        b.pos[:] = 0
        b.energy = 100; b.material = 200
        before = b.traces.copy()
        ns['now'] = 10
        e0 = ac9.event()
        self.assertFalse(gate(b, 0, 0, e0), 'bank-0 blocked')
        self.assertEqual(e0['spent_m'], 0); self.assertEqual(e0['spent_e'], 0,
            'a blocked birth must not spend resources')
        self.assertTrue(gate(b, 1, 0, e0), 'bank-1 not blocked')
        np.testing.assert_array_equal(b.traces, before, 'the gate never touches content (traces)')

    def test_gate_unblocks_at_restore_tick(self):
        ns = _ns()
        gate = ac92.make_birth(ns, dict(block_W=True, block_tick=8129, restore_tick=8240))
        b = ac4.Body(np.zeros((4, 1024, 7), dtype=np.uint8),
                     np.array([32, 48, 64, 0] * 4 + [64, 96, 128, 0], dtype=np.int16),
                     np.zeros((20, 2), dtype=np.int16),
                     np.arange(128, 248, 6, dtype=np.int16))
        b.pos[:] = 0
        b.energy = 100; b.material = 200
        e = ac4.empty_event()
        ns['now'] = 8239
        self.assertFalse(gate(b, 0, 0, e))
        ns['now'] = 8240
        self.assertTrue(gate(b, 0, 0, e))


class TestRestoreIsMachineryOnly(unittest.TestCase):
    def test_restore_W_touches_only_life_and_pos(self):
        o, _ = _org(0)
        o.body.life[:4] = 0                    # simulate the depleted machinery
        before_traces = o.body.traces.copy()
        before_energy = o.body.energy
        before_material = o.body.material
        before_fuel = o.body.fuel
        before_life_rest = o.body.life[4:].copy()
        ac92.restore_W(o)
        np.testing.assert_array_equal(o.body.life[:4], [32, 48, 64, 0],
                                      'restored W endowment')
        np.testing.assert_array_equal(o.body.pos[:4], 0, 'restored W interior')
        np.testing.assert_array_equal(o.body.traces, before_traces,
                                      'restore_W must not touch content (traces)')
        self.assertEqual(o.body.energy, before_energy)
        self.assertEqual(o.body.material, before_material)
        self.assertEqual(o.body.fuel, before_fuel)
        np.testing.assert_array_equal(o.body.life[4:], before_life_rest,
                                      'restore_W must not touch C/B catalysts')
        # and W is now available (inside + live)
        self.assertEqual(int(ac4.available(o.body)[:4].sum()), 3)


class TestWDependenceOfContentWrites(unittest.TestCase):
    def _target(self, o):
        return ac92.build_program(ac92.read_slot(o, ac92.read_pointer(o)))

    def test_content_writes_stop_with_W_zero(self):
        o, offs = _org(0, W_zero=True)
        e = ac9.event()
        g = ac92.read_pointer(o)
        src_maj = ac92.read_slot(o, g)         # 130-bit slot content (the copy source)
        self.assertEqual(ac92.write_toward_slot(o, e, (g + 1) % 4, src_maj, ac92.SUCC_BUDGET), 0)
        self.assertEqual(ac92.write_pointer(o, e, (g + 1) % 4), 0)
        ac92.reg_description_active(o, e)
        ac92.reg_pointer(o, e)
        ac92.reg_ctrl(o, e)
        ac92.reg_from_active(o, e, offs)
        self.assertEqual(e.get('reg_writes', 0), 0)
        self.assertEqual(e.get('succ_writes', 0), 0)
        self.assertEqual(e['spent_e'], 0); self.assertEqual(e['spent_m'], 0)

    def test_content_writes_run_with_W_present(self):
        # with W present, a real differing write occurs (non-vacuous control)
        o, offs = _org(0)
        # corrupt one program bit to give reg_from_active real work
        o.body.traces[0, 0, 0:4] = 1 - o.body.traces[0, 0, 0]
        e = ac9.event()
        ac92.reg_from_active(o, e, offs)
        self.assertGreater(e.get('reg_writes', 0), 0)

    def test_coordinator_transition_write_is_W_independent(self):
        o, _ = _org(0, W_zero=True)            # W == 0, but energy/material available
        o.body.traces[1, ac92.CTRL_OFFS] = 0   # force a full mode transition
        e = ac9.event()
        n = ac92.write_ctrl(o, e, ac92.encode_ctrl(1, ac92.PHASE_COPY, 0))
        self.assertGreater(n, 0, 'the coordinator transition write must not be gated by W')
        self.assertGreater(e.get('ctrl_writes', 0), 0)


class TestDeclaredSeeds(unittest.TestCase):
    def test_final_seeds_disjoint(self):
        finals = {4300, 4301, 4302, 4303}
        self.assertTrue(finals.isdisjoint(range(8)), 'finals disjoint from engineering 0-7')
        self.assertTrue(finals.isdisjoint(range(4204)), 'finals disjoint from prior final families')


class TestGateShapes(unittest.TestCase):
    def test_gate_keys(self):
        self.assertEqual(set(ac92.gates([]).keys()),
                         {'G1_intact_reconstructs', 'G2_block_stalls_while_alive',
                          'G3_rescue_resumes_reconstruction',
                          'G4_content_writes_stop_description_intact',
                          'G5_controls_clean', 'G6_completeness_determinism'})

    def _row(self, arm, **over):
        # a complete row dict carrying every key the gates touch for this arm's condition
        base = dict(arm=arm, damage=True, corrupt=True, transition='none',
                    completed=False, flipped_still_wrong=0, alive_at_corruption=True,
                    alive_pre_rescue=True, fw_pre_rescue=8, window_reg_writes=0,
                    W_pre_rescue=0, window_succ_writes=0, description_correct_intervention=130,
                    fw_at_corruption=8)
        base.update(over)
        return base

    def test_G2_categorical(self):
        good = self._row('W_block', completed=False)
        bad = self._row('W_block', completed=True)
        self.assertTrue(ac92.gates([good])['G2_block_stalls_while_alive'])
        self.assertFalse(ac92.gates([bad])['G2_block_stalls_while_alive'])

    def test_G3_categorical(self):
        good = self._row('W_rescue', completed=True, flipped_still_wrong=0,
                         W_pre_rescue=0, fw_pre_rescue=8, window_reg_writes=0)
        bad = self._row('W_rescue', completed=True, fw_pre_rescue=0)
        self.assertTrue(ac92.gates([good])['G3_rescue_resumes_reconstruction'])
        self.assertFalse(ac92.gates([bad])['G3_rescue_resumes_reconstruction'])

    def test_G4_categorical(self):
        good = self._row('W_block', window_succ_writes=0, description_correct_intervention=130)
        bad = self._row('W_block', description_correct_intervention=120)
        self.assertTrue(ac92.gates([good])['G4_content_writes_stop_description_intact'])
        self.assertFalse(ac92.gates([bad])['G4_content_writes_stop_description_intact'])


class TestRecordedFreeze(unittest.TestCase):
    @unittest.skipUnless(Path('ac92_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac92_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac92.gates(rows)
        g['G6_completeness_determinism'] = len(rows) == len(results['seeds']) * 2 * 12
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')

    @unittest.skipUnless(Path('ac92_results_v1/results.json').exists(), 'finals not yet run')
    def test_block_content_intact_at_death(self):
        # the dying W_block individual loses the MACHINERY (W), not the content (description)
        with open('ac92_results_v1/results.json') as f:
            rows = json.load(f)['rows']
        for r in rows:
            if r['arm'] == 'W_block' and r['damage'] and r['corrupt']:
                self.assertEqual(r['description_correct_at_death'], 130,
                                 f"W_block seed {r['seed']}: content must be intact at death")


if __name__ == '__main__':
    unittest.main()
