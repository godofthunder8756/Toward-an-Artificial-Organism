"""AC67 tests: pin the recorded gate outcomes, including the G1/G5 falsification.

The suite must stay green without hiding the falsification: the register-only claim
failed on seed 2601 (observation hijack), so the tests assert the recorded outcome —
G2/G3/G4 pass, G1/G5 fail — plus the survival separation (8/8 vs 8/8) and the two
mechanisms. A code change that alters the record is caught instead of absorbed.
"""
import json
import unittest
from pathlib import Path

import ac12

ROOT = Path(__file__).parent / 'ac67_results_v1'


def setUpModule():
    # pin the global the study depends on, so test order cannot leak a threshold
    ac12.REGISTER_THRESHOLD = 1


def load_rows():
    with (ROOT / 'results.json').open() as f:
        return json.load(f)['rows']


def arm_rows(rows, arm):
    return [r for r in rows if r['arm'] == arm]


class TestSurvivalSeparation(unittest.TestCase):
    def test_closed_all_survive(self):
        rows = load_rows()
        self.assertEqual(sum(r['first_dead'] is None for r in arm_rows(rows, 'closed')), 8)

    def test_no_repair_all_die(self):
        rows = load_rows()
        self.assertEqual(sum(r['first_dead'] is not None for r in arm_rows(rows, 'no_repair')), 8)

    def test_closed_register_intact(self):
        rows = load_rows()
        self.assertTrue(all(r['register_any_flip'] is False for r in arm_rows(rows, 'closed')))


class TestRecordedFalsification(unittest.TestCase):
    def test_G1_fails_on_2601(self):
        """G1 (no_repair register degraded in all 8) fails: seed 2601 register stays clean."""
        rows = load_rows()
        degraded = sum(r['register_any_flip'] for r in arm_rows(rows, 'no_repair'))
        self.assertEqual(degraded, 6)          # recorded: 6/8, not 8/8

    def test_G5_fails_on_2601(self):
        """G5 (register flips before death in all 8) fails: seed 2601 never flips."""
        rows = load_rows()
        r2601 = [r for r in arm_rows(rows, 'no_repair') if r['seed'] == 2601]
        self.assertEqual(len(r2601), 2)
        self.assertTrue(all(r['first_register_flip'] is None for r in r2601))

    def test_two_mechanisms(self):
        """6/8 register path (flip < death); 2/8 observation hijack (no flip, no routes)."""
        rows = load_rows()
        nr = arm_rows(rows, 'no_repair')
        register_path = [r for r in nr if r['first_register_flip'] is not None
                         and r['first_register_flip'] < r['first_dead']]
        hijack = [r for r in nr if r['first_register_flip'] is None]
        self.assertEqual(len(register_path), 6)
        self.assertEqual(len(hijack), 2)
        self.assertTrue(all(r['demand'] == [0, 0] for r in hijack))  # routes never acquired


class TestNoDrift(unittest.TestCase):
    def test_snapshot_present_and_runner_hashed(self):
        snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
        self.assertIn('ac67.py', snap)
        self.assertIn('ac12.py', snap)


if __name__ == '__main__':
    unittest.main()
