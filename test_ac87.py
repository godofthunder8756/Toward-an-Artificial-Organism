"""AC87 tests: pin the integrated-successor layout, the generic-over-syntax order-preserving decode,
the succession machinery with a real verify gate, the controller-state maintenance, the gate shape,
and the recorded outcomes."""
import inspect
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac76
import ac87
import ac5_program as prog


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac87.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _acquire(seed):
    """Return (organism, reg_offs, encoded, priority) with the recipe installed in slot 0."""
    _, _, _, priority = ac87.ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    reg_offs = ac87.resolve_offsets(o)
    encoded = ac87.description_bits(priority)
    o.body.traces[1, :ac87.DESC_BITS] = encoded[:, None]
    return o, reg_offs, encoded, priority


class TestLayout(unittest.TestCase):
    def test_offsets(self):
        self.assertEqual(ac87.PERM_OFFSET, 70)
        self.assertEqual(ac87.MASK_OFFSET, 78)
        self.assertEqual(ac87.ACTION_OFFSET, 114)
        self.assertEqual(ac87.DESC_BITS, 130)
        self.assertEqual(ac87.SLOT_BITS, 130)
        self.assertEqual(ac87.PTR_BASE, 4 * 130)
        self.assertEqual(ac87.PTR_OFFS, [520, 521])
        self.assertEqual(ac87.CTRL_BASE, 522)
        self.assertEqual(ac87.CTRL_BITS, 18)

    def test_pointer_and_ctrl_in_recipe_bank(self):
        o, reg_offs, encoded, priority = _acquire(0)
        self.assertEqual(ac87.read_pointer(o), 0)
        self.assertNotIn(ac87.PTR_BASE, reg_offs)
        ctrl = set(range(ac87.CTRL_BASE, ac87.CTRL_BASE + ac87.CTRL_BITS))
        self.assertFalse(ctrl & set(reg_offs), 'controller state must be disjoint from the register')

    def test_ctrl_roundtrip(self):
        o, reg_offs, encoded, priority = _acquire(0)
        o.body.energy = 1000; o.body.material = 1000
        e = ac87.ac9.event()
        for (active, phase, last) in [(1, 1, 12345), (0, 3, 8192), (1, 4, 0)]:
            ac87.write_ctrl(o, e, ac87.encode_ctrl(active, phase, last))
            self.assertEqual(ac87.ctrl_fields(o), (active, phase, last))


class TestGenericDecode(unittest.TestCase):
    def test_rebuild_equals_acquired(self):
        for seed in range(12):
            o, reg_offs, encoded, priority = _acquire(seed)
            acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
            t = ac87.build_program(ac87.read_slot(o, 0))
            self.assertIsNotNone(t, f'rebuild returned None for seed {seed}')
            np.testing.assert_array_equal(t, acquired, f'rebuild != acquired for seed {seed}')

    def test_rebuild_returns_none_on_invalid_perm(self):
        o, reg_offs, encoded, priority = _acquire(0)
        o.body.traces[1, 70:72, :] = 1
        o.body.traces[1, 72:74, :] = 1
        self.assertIsNone(ac87.build_program(ac87.read_slot(o, 0)))

    def test_generic_over_syntax(self):
        # a stored mask flipped to another syntactically valid value must decode FAITHFULLY, not be
        # rejected by an external correctness rule (m == 4<<b)
        for seed in range(4):
            o, reg_offs, encoded, priority = _acquire(seed)
            new_mask = 8 if (4 << priority[0]) != 8 else 16
            o.body.traces[1, ac87.MASK_OFFSET:ac87.MASK_OFFSET + 9, :] = \
                ac87.encode_mask(new_mask)[:, None]
            desc = ac87.read_slot(o, 0)
            t = ac87.build_program(desc)
            self.assertIsNotNone(t, 'a syntactically valid mask must decode, not be rejected')
            self.assertEqual(ac87.read_masks(desc)[0], new_mask)
            acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
            self.assertFalse(np.array_equal(t, acquired),
                             'the rebuilt program must follow the flipped internal description')

    def test_no_external_correctness_rule_on_reconstruction_path(self):
        src = inspect.getsource(ac87.build_program)
        self.assertNotIn('prog.program(', src)
        # the reconstruction path must not reject a mask/action by the 4<<b / 2+b convention
        self.assertNotIn('(4 << b)', src)
        self.assertNotIn('(2 + b)', src)
        self.assertIn('prog.encode_rule(1, m, a)', src,
                      'bank rules must be built from the READ mask/action values')


class TestSuccessionMachinery(unittest.TestCase):
    def test_full_cycle_with_verify_gate(self):
        o, reg_offs, encoded, priority = _acquire(0)
        o.body.energy = 5000
        o.body.material = 5000
        succ = ac87.Succession('real', encoded)
        e = ac87.ac9.event()
        t = 0
        while not succ.log and t < 5000:
            ac87.advance(o, e, succ, t, True)
            t += 1
        self.assertEqual(len(succ.log), 1, 'one cycle should complete')
        s = succ.log[0]
        self.assertEqual(s['verified_valid'], 1)
        self.assertEqual(s['target_correct'], 1)
        self.assertLessEqual(s['start'], s['copy_done'])
        self.assertLessEqual(s['copy_done'], s['switch_tick'])
        self.assertLessEqual(s['switch_tick'], s['remove_tick'])
        self.assertEqual(ac87.read_pointer(o), 1)
        self.assertEqual(int(o.body.traces[1, :ac87.SLOT_BITS].sum()), 0, 'old slot cleared')
        np.testing.assert_array_equal(ac87.read_slot(o, 1), encoded)
        self.assertGreater(e['succ_writes'], 0)

    def test_verify_gate_blocks_switch_on_invalid_successor(self):
        o, reg_offs, encoded, priority = _acquire(0)
        o.body.energy = 5000
        o.body.material = 5000
        succ = ac87.Succession('real', encoded)
        e = ac87.ac9.event()
        t = 0
        p = None
        while t < 5000:
            ac87.advance(o, e, succ, t, True)
            a, p, l = ac87.ctrl_fields(o)
            if a and p == ac87.PHASE_VERIFY:
                break
            t += 1
        self.assertEqual(p, ac87.PHASE_VERIFY, 'should reach the verify phase')
        # damage the successor's permutation to an invalid value between verify and switch
        o.body.traces[1, ac87.slot_offset(1) + 70:ac87.slot_offset(1) + 74, :] = 1
        ac87.advance(o, e, succ, t + 1, True)
        a, p, l = ac87.ctrl_fields(o)
        self.assertIn(p, (ac87.PHASE_COPY, ac87.PHASE_VERIFY),
                      'verify must not switch an invalid successor')
        self.assertEqual(ac87.read_pointer(o), 0, 'pointer must not advance')

    def test_succession_writes_paid(self):
        o, reg_offs, encoded, priority = _acquire(0)
        o.body.energy = 5000; o.body.material = 5000
        succ = ac87.Succession('real', encoded)
        e = ac87.ac9.event()
        e0, m0 = int(o.body.energy), int(o.body.material)
        for t in (2400, 2401, 2402):        # start + first copy writes
            ac87.advance(o, e, succ, t, True)
        n = int(e.get('ctrl_writes', 0)) + int(e.get('succ_writes', 0))
        self.assertGreater(n, 0)
        self.assertEqual(o.body.energy, e0 - n)
        self.assertEqual(o.body.material, m0 - n)

    def test_mode_none_is_inert(self):
        o, reg_offs, encoded, priority = _acquire(0)
        succ = ac87.Succession('none', encoded)
        e = ac87.ac9.event()
        for t in range(2600):
            ac87.advance(o, e, succ, t, True)
        self.assertEqual(len(succ.log), 0)
        self.assertEqual(e.get('succ_writes', 0), 0)


class TestControllerStateMaintenance(unittest.TestCase):
    def test_reg_ctrl_is_paid(self):
        o, reg_offs, encoded, priority = _acquire(0)
        e = ac87.ac9.event()
        o.body.traces[1, ac87.CTRL_BASE, 0] ^= 1
        self.assertGreaterEqual(ac87.ctrl_minority(o), 1)
        e0, m0 = int(o.body.energy), int(o.body.material)
        ac87.reg_ctrl(o, e)
        self.assertEqual(len(set(o.body.traces[1, ac87.CTRL_BASE].tolist())), 1)
        n = int(e['reg_writes'])
        self.assertGreaterEqual(n, 1)
        self.assertEqual(o.body.energy, e0 - n)
        self.assertEqual(o.body.material, m0 - n)


class TestGateShape(unittest.TestCase):
    def test_gate_keys(self):
        g = ac87.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_succession_occurs', 'G2_successor_functional', 'G3_remove_after_verify',
            'G4_recipe_maintained', 'G5_succession_is_the_replacer', 'G6_controller_state_maintained',
            'G7_control_clean', 'G8_composition', 'G9_completeness_determinism'})


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac87_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac87_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac87.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        succ = [r for r in rows if r['arm'] == 'succession' and r['damage']
                and not r['corrupt'] and r['transition'] == 'none']
        surv = [r for r in succ if r['completed']]
        self.assertTrue(all(r['successions'] >= 2 and r['description_correct'] == 130
                            and r['ctrl_idle_end'] == 1 for r in surv))


if __name__ == '__main__':
    unittest.main()
