"""AC86 tests: pin the replaceable-storage layout, the order-preserving decode, the succession
machinery, the pointer maintenance, the gate shape, and the recorded outcomes."""
import inspect
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac76
import ac80
import ac86
import ac5_program as prog


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac86.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _acquire(seed):
    """Return (organism, reg_offs, encoded, priority) with the recipe installed in slot 0."""
    _, _, _, priority = ac86.ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    reg_offs = ac86.resolve_offsets(o)
    encoded = ac80.description_bits(priority)
    o.body.traces[1, :ac86.DESC_BITS] = encoded[:, None]
    return o, reg_offs, encoded, priority


class TestReplaceableStorage(unittest.TestCase):
    def test_pointer_in_recipe_bank(self):
        # the pointer lives in bank 1 after the four slots, not in the program bank
        self.assertEqual(ac86.PTR_BASE, ac86.SLOTS * ac86.SLOT_BITS)
        self.assertEqual(ac86.PTR_OFFS, [ac86.PTR_BASE, ac86.PTR_BASE + 1])
        o, reg_offs, encoded, priority = _acquire(0)
        self.assertNotIn(ac86.PTR_BASE, reg_offs)
        self.assertEqual(ac86.read_pointer(o), 0, 'acquired pointer must read 0 (slot 0 active)')

    def test_pointer_write_roundtrip(self):
        o, reg_offs, encoded, priority = _acquire(0)
        e = ac86.ac9.event()
        o.body.energy = 1000; o.body.material = 1000
        for g in (1, 2, 3, 0):
            ac86.write_pointer(o, e, g)
            self.assertEqual(ac86.read_pointer(o), g)

    def test_four_slots_cycle(self):
        o, reg_offs, encoded, priority = _acquire(0)
        for g in range(4):
            self.assertEqual(ac86.slot_offset(g), g * ac86.SLOT_BITS)


class TestOrderPreservingDecode(unittest.TestCase):
    def test_rebuild_active_equals_acquired(self):
        # the generic decode must reproduce the ACQUIRED (ac9_priority_v2 reordered) program, not
        # prog.program order (AC80's build_program reorders the bank)
        for seed in range(12):
            o, reg_offs, encoded, priority = _acquire(seed)
            target = ac86.rebuild_active(o)
            acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
            self.assertIsNotNone(target, f'rebuild returned None for seed {seed}')
            np.testing.assert_array_equal(target, acquired,
                                          f'rebuild != acquired for seed {seed}')

    def test_rebuild_returns_none_on_invalid_perm(self):
        o, reg_offs, encoded, priority = _acquire(0)
        # corrupt the permutation to a non-permutation
        o.body.traces[1, 70:72, :] = 1
        o.body.traces[1, 72:74, :] = 1
        self.assertIsNone(ac86.rebuild_active(o))

    def test_no_prog_program_on_reconstruction_path(self):
        src = inspect.getsource(ac86.rebuild_active)
        self.assertNotIn('prog.program(', src, 'prog.program must not be called on the reconstruction path')
        self.assertNotIn('ac80.build_program(', src,
                         'the reordering build_program must not be on the reconstruction path')


class TestPointerMaintenance(unittest.TestCase):
    def test_pointer_repair_is_paid(self):
        o, reg_offs, encoded, priority = _acquire(0)
        e = ac86.ac9.event()
        o.body.traces[1, ac86.PTR_OFFS[0], 0] ^= 1       # one minority replica on bit 0
        self.assertGreaterEqual(ac86.pointer_minority(o), 1)
        e0, m0 = int(o.body.energy), int(o.body.material)
        ac86.reg_pointer(o, e)
        self.assertEqual(len(set(o.body.traces[1, ac86.PTR_OFFS[0]].tolist())), 1,
                         'pointer bit 0 replicas must agree after repair')
        n = int(e['reg_writes'])
        self.assertGreaterEqual(n, 1)
        self.assertEqual(o.body.energy, e0 - n, 'one energy paid per repaired replica')
        self.assertEqual(o.body.material, m0 - n, 'one material paid per repaired replica')

    def test_pointer_minority_trigger_repairs(self):
        # two minority replicas on one pointer bit -> pointer_minority >= POINTER_TRIGGER -> repaired
        o, reg_offs, encoded, priority = _acquire(0)
        o.body.energy = 1000; o.body.material = 1000
        o.body.traces[1, ac86.PTR_OFFS[0], 0:2] = 1
        self.assertGreaterEqual(ac86.pointer_minority(o), ac86.POINTER_TRIGGER)
        e = ac86.ac9.event()
        ac86.reg_pointer(o, e)
        self.assertEqual(int(o.body.traces[1, ac86.PTR_OFFS[0]].sum()), 0,
                         'pointer bit 0 must be restored to majority 0')


class TestSuccessionMachinery(unittest.TestCase):
    def test_copy_verify_switch_remove_sequence(self):
        # a full succession cycle: copy completes, verifies valid+correct, switches, removes
        o, reg_offs, encoded, priority = _acquire(0)
        o.body.energy = 1000
        o.body.material = 1000
        succ = ac86.Succession('real', encoded, min_tick=0, min_spacing=0, budget=1000)
        e = ac86.ac9.event()
        succ.now = 0
        succ.advance(o, e, True)               # starts copy (slot 0 -> 1)
        self.assertTrue(succ.active)
        while succ.active:
            succ.now += 1
            succ.advance(o, e, True)
        self.assertEqual(len(succ.log), 1)
        s = succ.log[0]
        self.assertEqual((s['source'], s['target']), (0, 1))
        self.assertEqual(s['verified_valid'], 1)
        self.assertEqual(s['target_correct'], 1)
        self.assertLessEqual(s['start'], s['copy_done'])
        self.assertLessEqual(s['copy_done'], s['switch_tick'])
        self.assertLessEqual(s['switch_tick'], s['remove_tick'])
        self.assertEqual(ac86.read_pointer(o), 1)
        # old slot cleared, successor holds the recipe
        self.assertEqual(int(o.body.traces[1, :ac86.SLOT_BITS].sum()), 0)
        np.testing.assert_array_equal(ac86.read_slot(o, 1), encoded)
        self.assertGreater(e['succ_writes'], 0, 'succession writes must be charged')

    def test_succession_is_paid(self):
        o, reg_offs, encoded, priority = _acquire(0)
        o.body.energy = 1000; o.body.material = 1000
        succ = ac86.Succession('real', encoded, min_tick=0, min_spacing=0, budget=10)
        e = ac86.ac9.event()
        e0, m0 = int(o.body.energy), int(o.body.material)
        succ.now = 0
        succ.advance(o, e, True)
        n = int(e['succ_writes'])
        self.assertGreater(n, 0)
        self.assertEqual(o.body.energy, e0 - n, 'one energy paid per succession write')
        self.assertEqual(o.body.material, m0 - n, 'one material paid per succession write')

    def test_no_succession_without_damage(self):
        # the succession trigger is the recipe's own degradation: with a clean slot it never fires
        o, reg_offs, encoded, priority = _acquire(0)
        succ = ac86.Succession('real', encoded)
        e = ac86.ac9.event()
        for t in range(100):
            succ.now = t
            succ.advance(o, e, False)
        self.assertEqual(len(succ.log), 0)
        self.assertFalse(succ.active)

    def test_mode_none_is_inert(self):
        o, reg_offs, encoded, priority = _acquire(0)
        succ = ac86.Succession('none', encoded)
        e = ac86.ac9.event()
        for t in range(100):
            succ.now = t
            succ.advance(o, e, True)
        self.assertEqual(len(succ.log), 0)
        self.assertEqual(e.get('succ_writes', 0), 0)


class TestGateShape(unittest.TestCase):
    def test_gate_keys(self):
        g = ac86.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_succession_occurs', 'G2_successor_functional', 'G3_remove_after_verify',
            'G4_recipe_maintained', 'G5_succession_is_the_replacer', 'G6_control_clean',
            'G7_completeness_determinism'})


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac86_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac86_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac86.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        succ = [r for r in rows if r['arm'] == 'succession' and r['damage']]
        repair = [r for r in rows if r['arm'] == 'repair' and r['damage']]
        unmaintained = [r for r in rows if r['arm'] == 'unmaintained' and r['damage']]
        surv = [r for r in succ if r['completed']]
        self.assertTrue(all(r['successions'] >= 2 and r['description_correct'] == 78
                            for r in surv))
        self.assertTrue(all(r['successions'] == 0 for r in repair))
        self.assertTrue(all(r['description_correct'] < 78 for r in unmaintained))


if __name__ == '__main__':
    unittest.main()
