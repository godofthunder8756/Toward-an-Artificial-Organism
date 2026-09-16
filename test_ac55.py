"""Tests for AC55: pin the frozen record, its (all-passing) gates, and its descriptive impaired count."""
import json
import unittest
from pathlib import Path
import ac55_order as a55

ROOT = Path('ac55_results_v1')


class TestAC55(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = json.loads((ROOT / 'results.json').read_text())

    def test_01_results_exist(self):
        self.assertTrue((ROOT / 'results.json').exists())
        self.assertTrue((ROOT / 'rows.jsonl').exists())
        self.assertTrue((ROOT / 'pre_run_snapshot.json').exists())

    def test_02_seeds(self):
        self.assertEqual(self.rec['seeds'], list(a55.FINAL_SEEDS))

    def test_03_optima_and_world(self):
        self.assertEqual(tuple(self.rec['opt']), a55.OPT)
        self.assertEqual(tuple(self.rec['worst']), a55.WORST)
        self.assertEqual(tuple(self.rec['values']), a55.VALUES)
        self.assertEqual(self.rec['stress_mult'], a55.STRESS_MULT)

    def test_04_gates_pinned_exact(self):
        self.assertEqual(self.rec['gates'], {
            'G1_resolvable': True,
            'G2_median_effect': True,
            'G3_stability_no_death': True,
            'G4_horizon_robust': True,
            'G5_state_blind': True,
            'G6_headroom': True,
            'G7_complete': True,
            'G8_determinism': True,
        })

    def test_05_resolvability_recorded(self):
        r = self.rec['summary']['resolvability']
        self.assertEqual(r['n'], 12)
        self.assertAlmostEqual(r['p'], 0.0078125, places=9)

    def test_06_effect_size(self):
        self.assertAlmostEqual(self.rec['summary']['median_difference'], 13982.5, places=1)
        self.assertAlmostEqual(self.rec['summary']['mean_difference'], 15591.416666666666, places=1)

    def test_07_dead_zero(self):
        self.assertEqual(self.rec['summary']['dead'], 0)

    def test_08_impaired_descriptive(self):
        # Descriptive, not a gate: 3/12 final seeds where worst > optimal (1 light-draw, 2 near-ties).
        self.assertEqual(self.rec['summary']['impaired'], 3)

    def test_09_steady_state(self):
        self.assertAlmostEqual(self.rec['summary']['steady_state_ratio'], 2.4947501879906158, places=6)

    def test_10_row_count_and_hashes(self):
        self.assertEqual(len(self.rec['rows']), 12)
        self.assertEqual(len(self.rec['hashes']), len(a55.SOURCES))


if __name__ == '__main__':
    unittest.main()
