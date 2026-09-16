"""AC46 tests: the frozen record, its declared gates, and its registered source hashes.

Run with: .venv/bin/python -B -m unittest test_ac46
"""
import hashlib
import json
import pathlib
import unittest
import numpy as np
import ac46_selfsufficiency as ac46
import ac38_variance as ac38

ROOT = pathlib.Path('ac46_results_v1')


def load():
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines() if l.strip()]
    res = json.loads((ROOT / 'results.json').read_text())
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    return rows, res, snap


class TestProtocolWasRegisteredFirst(unittest.TestCase):
    def test_declared_sources_equal_the_hashed_set(self):
        declared = ac46.preflight()
        self.assertEqual(sorted(set(declared)), sorted(set(ac46.SOURCES)))
        self.assertEqual(len(set(declared)), 6)

    def test_declared_sources_are_unchanged_since_registration(self):
        _, _, snap = load()
        changed = [n for n, sha in snap.items()
                   if not pathlib.Path(n).exists()
                   or hashlib.sha256(pathlib.Path(n).read_bytes()).hexdigest() != sha]
        self.assertEqual(changed, [], f'edited after registration: {changed}')

    def test_result_dir_is_frozen(self):
        self.assertTrue(ROOT.is_dir())
        self.assertTrue((ROOT / 'pre_run_snapshot.json').exists())
        self.assertTrue((ROOT / 'rows.jsonl').exists())


class TestFrozenGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.res, cls.snap = load()
        cls.gates = cls.res['gates']

    def test_all_nine_gates_pass(self):
        self.assertEqual(sorted(self.gates),
                         ['G1_resolvable', 'G2_median_effect_in_sites', 'G3_separation_of_minima',
                          'G4_oracle_b_ceiling_above_bar', 'G5_oracle_a_floor_below_bar',
                          'G6_state_blind_means_below_bar', 'G7_all_individuals_complete',
                          'G8_determinism', 'G9_register_in_the_loop'])
        self.assertTrue(all(self.gates.values()), self.gates)

    def test_contrast_resolves_at_the_power_floor(self):
        learner = [r['learner_both']['post'] for r in self.rows]
        no_rel = [r['no_release']['post'] for r in self.rows]
        d = [a - b for a, b in zip(learner, no_rel)]
        t = ac38.sign_flip_test(d)
        self.assertEqual(t['n'], 12)
        self.assertAlmostEqual(t['p'], 2 / 2**12, delta=0.001)

    def test_separation_of_minima_holds(self):
        learner = [r['learner_both']['post'] for r in self.rows]
        no_rel = [r['no_release']['post'] for r in self.rows]
        self.assertGreaterEqual(min(learner), ac46.BAR)
        self.assertLess(max(no_rel), ac46.BAR)

    def test_effect_size_clears_the_declared_bar(self):
        s = self.res['summary']
        self.assertGreaterEqual(s['median_difference'], ac46.MEDIAN_BAR)
        self.assertEqual(s['impaired_fraction'], 1.0)

    def test_seeds_are_disjoint_from_the_engineering_seeds(self):
        used = {r['seed'] for r in self.rows}
        self.assertEqual(used, set(range(4700, 4712)))
        self.assertEqual(used & set(range(4600, 4612)), set(), 'finals must not reuse engineering seeds')

    def test_every_individual_is_present_once(self):
        keys = [r['seed'] for r in self.rows]
        self.assertEqual(len(keys), 12)
        self.assertEqual(len(set(keys)), 12)


class TestClaimDiscipline(unittest.TestCase):
    def test_no_claim_of_experience_or_life_is_recorded(self):
        text = (ROOT / 'results.json').read_text().lower()
        for banned in ('conscious', 'experience', 'sentien', 'autopoi', 'alive', 'life'):
            self.assertNotIn(banned, text, f'results.json mentions {banned!r}')

    def test_protocol_states_the_self_funded_world(self):
        proto = pathlib.Path('AC46_PROTOCOL_v1.md').read_text()
        self.assertIn('production period 4, drain 3', proto)
        self.assertIn('self-funded', proto)

    def test_runner_pins_the_ac37_economy(self):
        self.assertEqual(ac46.PRODUCTION_PERIOD, 4)
        self.assertEqual(ac46.DRAIN, 3)
        self.assertEqual(ac46.BAR, 4.0)


if __name__ == '__main__':
    unittest.main()
