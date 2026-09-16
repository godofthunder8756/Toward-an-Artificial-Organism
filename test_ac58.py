"""Tests for AC58: pin the frozen record, its all-passing gates, and key summary numbers."""
import json
import unittest
from pathlib import Path
import ac58_order as a58

ROOT = Path('ac58_results_v1')


class TestAC58(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = json.loads((ROOT / 'results.json').read_text())

    def test_01_results_exist(self):
        self.assertTrue((ROOT / 'results.json').exists())
        self.assertTrue((ROOT / 'rows.jsonl').exists())
        self.assertTrue((ROOT / 'pre_run_snapshot.json').exists())

    def test_02_seeds(self):
        self.assertEqual(self.rec['seeds'], list(a58.FINAL_SEEDS))

    def test_03_world_params(self):
        self.assertEqual(tuple(self.rec['opt_b']), a58.OPT_B)
        self.assertEqual(self.rec['damage_rate'], a58.DAMAGE_RATE)
        self.assertEqual(self.rec['repair_cost'], a58.REPAIR_COST)

    def test_04_gates_all_true(self):
        for k in ('G1_resolvable', 'G2_effect', 'G3_retention', 'G4_repaired_stability',
                  'G5_protected_stability', 'G6_corruption_consequential', 'G7_horizon_robust',
                  'G8_determinism'):
            self.assertTrue(self.rec['gates'][k], k)

    def test_05_resolvability(self):
        self.assertAlmostEqual(self.rec['summary']['resolvability']['p'], 0.0009765625, places=9)

    def test_06_effect(self):
        self.assertAlmostEqual(self.rec['summary']['median_difference'], 20077.25, places=1)
        self.assertAlmostEqual(self.rec['summary']['mean_difference'], 18020.166666666668, places=1)

    def test_07_retention_exact(self):
        s = self.rec['summary']
        self.assertEqual(s['repaired']['mean'], s['protected']['mean'])

    def test_08_dead_unrepaired(self):
        self.assertEqual(self.rec['summary']['dead_unrepaired'], 3)

    def test_09_steady_state(self):
        self.assertAlmostEqual(self.rec['summary']['steady_state_ratio'], 2.486856828887504, places=6)

    def test_10_row_count_and_hashes(self):
        self.assertEqual(len(self.rec['rows']), 12)
        self.assertEqual(len(self.rec['hashes']), len(a58.SOURCES))


if __name__ == '__main__':
    unittest.main()
