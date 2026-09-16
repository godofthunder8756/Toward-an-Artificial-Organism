"""Tests for AC54: pin the frozen record and its (failed) gates, so they cannot be silently flipped."""
import json
import unittest
from pathlib import Path
import ac54_order as a54

ROOT = Path('ac54_results_v1')


class TestAC54(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = json.loads((ROOT / 'results.json').read_text())

    def test_01_results_exist(self):
        self.assertTrue((ROOT / 'results.json').exists())
        self.assertTrue((ROOT / 'rows.jsonl').exists())
        self.assertTrue((ROOT / 'pre_run_snapshot.json').exists())

    def test_02_seeds(self):
        self.assertEqual(self.rec['seeds'], list(a54.FINAL_SEEDS))

    def test_03_optimima_recorded(self):
        self.assertEqual(tuple(self.rec['opt']), a54.OPT)
        self.assertEqual(tuple(self.rec['worst']), a54.WORST)

    def test_04_gates_pinned_exact(self):
        # The freeze FAILED on fresh seeds: G1, G5, G7 false. Pin them so a later reclassification
        # (or a silent flip) is impossible.
        self.assertEqual(self.rec['gates'], {
            'G1_resolvable': False,
            'G2_median_effect': True,
            'G3_stability_no_death': True,
            'G4_horizon_robust': True,
            'G5_consistency': False,
            'G6_state_blind': True,
            'G7_headroom': False,
            'G8_determinism': True,
        })

    def test_05_resolvability_recorded(self):
        r = self.rec['summary']['resolvability']
        self.assertEqual(r['n'], 12)
        self.assertAlmostEqual(r['p'], 0.03662109375, places=9)

    def test_06_three_impaired(self):
        self.assertEqual(self.rec['summary']['impaired'], 3)

    def test_07_dead_zero(self):
        self.assertEqual(self.rec['summary']['dead'], 0)

    def test_08_steady_state(self):
        self.assertAlmostEqual(self.rec['summary']['steady_state_ratio'], 2.4892382777468347, places=6)

    def test_09_row_count(self):
        self.assertEqual(len(self.rec['rows']), 12)

    def test_10_hashes(self):
        self.assertEqual(len(self.rec['hashes']), len(a54.SOURCES))


if __name__ == '__main__':
    unittest.main()
