"""AC71 tests: pin the recorded gate outcomes — all five pass at majority read."""
import json
import unittest
from pathlib import Path

import ac12

ROOT = Path(__file__).parent / 'ac71_results_v1'


def setUpModule():
    ac12.REGISTER_THRESHOLD = 4


def rows():
    with (ROOT / 'results.json').open() as f:
        return json.load(f)['rows']


def arm(rows_, a):
    return [r for r in rows_ if r['arm'] == a]


class TestRecordedOutcome(unittest.TestCase):
    def test_G1_closed_survives(self):
        self.assertEqual(sum(r['first_dead'] is None for r in arm(rows(), 'closed')), 8)

    def test_G2_routes_held(self):
        self.assertEqual(sum(r['occupied'] > 0 for r in arm(rows(), 'closed')), 8)

    def test_G3_body_stable(self):
        c = arm(rows(), 'closed')
        self.assertEqual(sum(r['W_live'] >= 1 and r['C_live'] >= 1 for r in c), 8)

    def test_G4_register_intact(self):
        self.assertTrue(all(r['register'] == [False, False, False, False] for r in arm(rows(), 'closed')))

    def test_G5_repair_necessary(self):
        self.assertEqual(sum(r['first_dead'] is not None for r in arm(rows(), 'no_repair')), 8)


class TestNoDrift(unittest.TestCase):
    def test_snapshot_present(self):
        snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
        self.assertIn('ac71.py', snap)


if __name__ == '__main__':
    unittest.main()
