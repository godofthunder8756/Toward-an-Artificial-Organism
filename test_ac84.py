"""AC84 tests: pin the production-recipe-in-description link, the unconditional-gating shape, the
arm set, the floors, and the recorded outcomes."""
import inspect
import json
import unittest
from pathlib import Path
import numpy as np
import ac12
import ac76
import ac80
import ac84
import ac5_program as prog


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac84.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


class TestProductionRecipeInDescription(unittest.TestCase):
    def test_production_words_are_the_birth_rules(self):
        # the description's words 3-5 must be exactly the W/C/B birth rules (the production recipe)
        for seed in range(12):
            _, _, _, priority = ac84.ac4.acquire(seed)
            desc = ac80.description_bits(priority)
            self.assertEqual(desc[28:42].tolist(), prog.encode_rule(1, 64, 6).tolist())
            self.assertEqual(desc[42:56].tolist(), prog.encode_rule(1, 128, 7).tolist())
            self.assertEqual(desc[56:70].tolist(), prog.encode_rule(1, 256, 8).tolist())

    def test_rebuild_copies_production_words_verbatim(self):
        for seed in range(12):
            _, _, _, priority = ac84.ac4.acquire(seed)
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


class TestUnconditionalGating(unittest.TestCase):
    def test_arms_are_the_three_load_bearing_arms(self):
        self.assertEqual(ac84.ARMS, ('internalized', 'unmaintained', 'no_repair'))

    def test_floors_are_the_slot_complements(self):
        self.assertEqual(ac84.W_BIRTH_FLOOR, ac84.W_SLOTS)
        self.assertEqual(ac84.C_BIRTH_FLOOR, ac84.C_SLOTS)
        self.assertEqual(ac84.B_BIRTH_FLOOR, ac84.B_SLOTS)
        self.assertEqual((ac84.W_SLOTS, ac84.C_SLOTS, ac84.B_SLOTS), (16, 4, 20))

    def test_g1_does_not_filter_on_completed(self):
        # the AC84 fix: turnover must be gated on the full cohort, dead or alive. Build a synthetic
        # table where every internalized individual meets the floors but half are dead, and confirm
        # G1 passes; then break one dead individual's floor and confirm G1 fails regardless of death.
        def row(arm, completed, W, C, B):
            return dict(arm=arm, completed=completed, W_birth=W, C_birth=C, B_birth=B,
                        writes=10, converted=10, first_acquire=[1, 1],
                        description_correct=78, first_dead=None)
        rows = ([row('internalized', True, 300, 60, 400)] * 4
                + [row('internalized', False, 90, 20, 100)] * 4
                + [row('unmaintained', False, 90, 20, 100, )] * 8
                + [row('no_repair', False, 30, 10, 3)] * 8)
        self.assertTrue(ac84.gates(rows)['G1_turnover_unconditional'],
                        'dead individuals meeting the floors must still pass G1')
        broken = rows[:] + [row('internalized', False, 15, 3, 19)]   # dead, below a floor
        self.assertFalse(ac84.gates(broken)['G1_turnover_unconditional'],
                         'a below-floor individual must fail G1 even though it is dead')

    def test_gate_keys(self):
        g = ac84.gates([])
        self.assertEqual(set(g.keys()), {
            'G1_turnover_unconditional', 'G2_use_unconditional', 'G3_loop_load_bearing',
            'G4_recipe_degrades_unmaintained', 'G5_recipe_maintained_survivors',
            'G6_completeness_determinism'})


class TestRecordedOutcomes(unittest.TestCase):
    @unittest.skipUnless(Path('ac84_results_v1/results.json').exists(), 'finals not yet run')
    def test_recorded_freeze(self):
        with open('ac84_results_v1/results.json') as f:
            results = json.load(f)
        rows = results['rows']
        g = ac84.gates(rows)
        self.assertTrue(all(v for v in g.values() if v is not None), f'gates not all pass: {g}')
        internalized = [r for r in rows if r['arm'] == 'internalized']
        # the claim: turnover and use are unconditional, including for the dead individual
        self.assertTrue(all(r['W_birth'] >= 16 and r['C_birth'] >= 4 and r['B_birth'] >= 20
                            and r['writes'] > 0 and r['converted'] > 0
                            for r in internalized),
                        'every internalized individual, dead or alive, must turn over and use')
        self.assertTrue(all(r['description_correct'] == 78
                            for r in internalized if r['completed']),
                        'internalized survivors must retain the recipe')
        unmaintained = [r for r in rows if r['arm'] == 'unmaintained']
        self.assertTrue(all(r['description_correct'] < 78 for r in unmaintained),
                        'unmaintained must degrade the recipe')


if __name__ == '__main__':
    unittest.main()
