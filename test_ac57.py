"""Tests for AC57: pin the frozen record, its all-passing gates, and key summary numbers."""
import json
import unittest
from pathlib import Path
import ac57_order as a57

ROOT = Path('ac57_results_v1')


class TestAC57(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = json.loads((ROOT / 'results.json').read_text())

    def test_01_results_exist(self):
        self.assertTrue((ROOT / 'results.json').exists())
        self.assertTrue((ROOT / 'rows.jsonl').exists())
        self.assertTrue((ROOT / 'pre_run_snapshot.json').exists())

    def test_02_seeds(self):
        self.assertEqual(self.rec['seeds'], list(a57.FINAL_SEEDS))

    def test_03_optima_and_world(self):
        self.assertEqual(tuple(self.rec['opt_a']), a57.OPT_A)
        self.assertEqual(tuple(self.rec['opt_b']), a57.OPT_B)
        self.assertEqual(tuple(self.rec['worst_b']), a57.WORST_B)
        self.assertEqual(tuple(self.rec['values_a']), a57.VALUES_A)

    def test_04_gates_all_true(self):
        for k in ('G1_load_resolvable', 'G2_load_effect', 'G3_reacq_resolvable', 'G4_reacq_effect',
                  'G5_stability_no_death', 'G6_horizon_robust', 'G7_state_blind', 'G8_headroom',
                  'G9_register_in_loop', 'G10_determinism'):
            self.assertTrue(self.rec['gates'][k], k)

    def test_05_load_resolvability(self):
        self.assertAlmostEqual(self.rec['summary']['load_resolvability']['p'], 0.001953125, places=9)

    def test_06_reacq_resolvability(self):
        self.assertAlmostEqual(self.rec['summary']['reacq_resolvability']['p'], 0.0068359375, places=9)

    def test_07_effects(self):
        self.assertAlmostEqual(self.rec['summary']['load_median'], 9056.75, places=1)
        self.assertAlmostEqual(self.rec['summary']['reacq_median'], 9728.0, places=1)

    def test_08_dead_zero_and_steady(self):
        self.assertEqual(self.rec['summary']['dead'], 0)
        self.assertAlmostEqual(self.rec['summary']['steady_state_ratio'], 2.489078634321917, places=6)

    def test_09_arm_means(self):
        s = self.rec['summary']
        self.assertAlmostEqual(s['optimal']['mean'], 68161.5, places=0)
        self.assertAlmostEqual(s['worst']['mean'], 57483.333333333336, places=0)
        self.assertAlmostEqual(s['learner']['mean'], 68214.41666666667, places=0)
        self.assertAlmostEqual(s['no_release']['mean'], 57952.5, places=0)

    def test_10_row_count_and_hashes(self):
        self.assertEqual(len(self.rec['rows']), 12)
        self.assertEqual(len(self.rec['hashes']), len(a57.SOURCES))


if __name__ == '__main__':
    unittest.main()
