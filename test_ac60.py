"""Tests for AC60: pin the frozen record, its all-passing gates, and key summary numbers."""
import json
import unittest
from pathlib import Path
import ac60_order as a60

ROOT = Path('ac60_results_v1')


class TestAC60(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = json.loads((ROOT / 'results.json').read_text())

    def test_01_results_exist(self):
        self.assertTrue((ROOT / 'results.json').exists())
        self.assertTrue((ROOT / 'rows.jsonl').exists())
        self.assertTrue((ROOT / 'pre_run_snapshot.json').exists())

    def test_02_seeds_and_n(self):
        self.assertEqual(self.rec['seeds'], list(a60.FINAL_SEEDS))
        self.assertEqual(self.rec['n'], 7)

    def test_03_optima(self):
        self.assertEqual(tuple(self.rec['opt_a']), a60.OPT_A)
        self.assertEqual(tuple(self.rec['opt_b']), a60.OPT_B)
        self.assertEqual(tuple(self.rec['worst_b']), a60.WORST_B)

    def test_04_gates_all_true(self):
        for k in ('G1_load_resolvable', 'G2_load_effect', 'G3_reacq_resolvable', 'G4_reacq_effect',
                  'G5_stability_no_death', 'G6_horizon_robust', 'G7_state_blind', 'G8_headroom',
                  'G9_register_in_loop', 'G10_determinism'):
            self.assertTrue(self.rec['gates'][k], k)

    def test_05_resolvability(self):
        self.assertAlmostEqual(self.rec['summary']['load_resolvability']['p'], 0.00048828125, places=9)
        self.assertAlmostEqual(self.rec['summary']['reacq_resolvability']['p'], 0.00048828125, places=9)

    def test_06_effects(self):
        self.assertAlmostEqual(self.rec['summary']['load_median'], 16788.25, places=1)
        self.assertAlmostEqual(self.rec['summary']['reacq_median'], 19710.0, places=1)

    def test_07_dead_and_steady(self):
        self.assertEqual(self.rec['summary']['dead'], 0)
        self.assertAlmostEqual(self.rec['summary']['steady_state_ratio'], 2.484600256750235, places=6)

    def test_08_arm_means(self):
        s = self.rec['summary']
        self.assertAlmostEqual(s['optimal']['mean'], 71145.66666666667, places=0)
        self.assertAlmostEqual(s['worst']['mean'], 53548.5, places=0)
        self.assertAlmostEqual(s['learner']['mean'], 71034.375, places=0)
        self.assertAlmostEqual(s['no_release']['mean'], 49314.166666666664, places=0)

    def test_09_register_roundtrip(self):
        r = self.rec['rows'][0]['learner_order']
        self.assertEqual(a60.unlehmer7(a60.lehmer7(r)), tuple(r))

    def test_10_row_count_and_hashes(self):
        self.assertEqual(len(self.rec['rows']), 12)
        self.assertEqual(len(self.rec['hashes']), len(a60.SOURCES))


if __name__ == '__main__':
    unittest.main()
