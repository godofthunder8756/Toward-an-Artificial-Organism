"""AC81 tests: pin the production-recipe-in-description link, the partial-loss semantics, the gate
shape, and the recorded outcomes."""
import inspect
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac76
import ac80
import ac81
import ac5_program as prog


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac81.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestProductionRecipeInDescription(unittest.TestCase):
    def test_production_words_are_the_birth_rules(self):
        # the description's words 3-5 must be exactly the W/C/B birth rules (the production recipe)
        for seed in range(12):
            _, _, _, priority = ac81.ac4.acquire(seed)
            desc = ac80.description_bits(priority)
            self.assertEqual(desc[28:42].tolist(), prog.encode_rule(1, 64, 6).tolist())
            self.assertEqual(desc[42:56].tolist(), prog.encode_rule(1, 128, 7).tolist())
            self.assertEqual(desc[56:70].tolist(), prog.encode_rule(1, 256, 8).tolist())

    def test_rebuild_copies_production_words_verbatim(self):
        # the program's production rules (bits 28-69) come from the description's bits 28-69,
        # i.e. the component-construction recipe is read from the vulnerable state, not hard-coded
        for seed in range(12):
            _, _, _, priority = ac81.ac4.acquire(seed)
            o, offs = ac12.acquire(seed)
            o.body.traces[1, :ac80.DESC_BITS] = ac80.description_bits(priority)[:, None]
            desc = ac80.read_description(o)
            target = ac80.rebuild(o)
            self.assertIsNotNone(target)
            np.testing.assert_array_equal(target[28:70], desc[28:70],
                                          f'production rules not read from description (seed {seed})')
            np.testing.assert_array_equal(target, prog.program(priority),
                                          f'generic decode != scaffold (seed {seed})')

    def test_rebuild_does_not_call_prog_program(self):
        src = inspect.getsource(ac80.rebuild) + inspect.getsource(ac80.build_program)
        self.assertNotIn('prog.program(', src)


class TestPartialLossSemantics(unittest.TestCase):
    def test_loss_slots_are_exactly_one_C_and_five_B(self):
        # the declared partial loss kills one C converter and five B boundary sites, nothing else
        self.assertEqual(ac81.LOSS_C, (16,))
        self.assertEqual(ac81.LOSS_B, (0, 1, 2, 3, 4))
        self.assertEqual(len(ac81.LOSS_C), 1)
        self.assertEqual(len(ac81.LOSS_B), 5)

    def test_loss_is_partial_not_catastrophic(self):
        # the loss must NOT destroy every usable copy: W is untouched, and 3 of 4 C / 15 of 20 B
        # remain (the catastrophic-destruction analog is out of scope)
        self.assertFalse(any(i in ac81.LOSS_C for i in (17, 18, 19)))   # 3 C copies survive
        self.assertFalse(any(i in ac81.LOSS_B for i in range(5, 20)))   # 15 B sites survive
        self.assertEqual(len(ac81.LOSS_C), 1, 'kills exactly 1 C, not all 4')


class TestGateShape(unittest.TestCase):
    def test_gate_keys(self):
        g = ac81.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_turnover', 'G2_use', 'G3_partial_loss_recovery', 'G4_recipe_maintained',
            'G5_maintenance_load_bearing', 'G6_no_repair_dies', 'G7_control_clean',
            'G8_completeness_determinism'})


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac81_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac81_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac81.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        internalized = [r for r in rows if r['arm'] == 'internalized' and r['loss']]
        unmaintained = [r for r in rows if r['arm'] == 'unmaintained' and r['loss']]
        surv_i = [r for r in internalized if r['completed']]
        self.assertTrue(all(r['description_correct'] == 78 and r['W_birth'] >= 100
                            and r['C_birth'] >= 20 and r['B_birth'] >= 100
                            and r['routes'][0] is not None and r['routes'][1] is not None
                            for r in surv_i),
                        'internalized survivors must retain the recipe and keep turning over components')
        self.assertTrue(all(r['description_correct'] < 78 for r in unmaintained),
                        'unmaintained must degrade the recipe')


if __name__ == '__main__':
    unittest.main()
