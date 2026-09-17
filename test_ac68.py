"""AC68 tests: pin the recorded gate outcomes — G3 passes, G1/G2 falsified by bimodality."""
import json
import unittest
from pathlib import Path

import ac12

ROOT = Path(__file__).parent / 'ac68_results_v1'


def setUpModule():
    ac12.REGISTER_THRESHOLD = 1


def rows():
    with (ROOT / 'results.json').open() as f:
        return json.load(f)['rows']


class TestRecordedOutcome(unittest.TestCase):
    def test_G3_function_lapses_all(self):
        self.assertEqual(sum(r['occupied'] == 0 for r in rows()), 8)

    def test_G1_body_survival_is_bimodal(self):
        r = rows()
        self.assertEqual(sum(x['first_dead'] is None for x in r), 4)   # recorded: 4/8 survive

    def test_G2_body_machinery_bimodal(self):
        r = rows()
        maintained = sum(x['W_live'] >= 1 and x['C_live'] >= 1 for x in r)
        self.assertEqual(maintained, 4)

    def test_dying_seeds_collapse_late(self):
        dying = [x for x in rows() if x['first_dead'] is not None]
        self.assertEqual(len(dying), 4)
        self.assertTrue(all(7300 < x['first_dead'] < 8000 for x in dying))   # late collapse

    def test_register_intact_only_in_survivors(self):
        # register intact in the 4 survivors, degraded (via _drop) in the 4 dying
        intact = sum(r['register'] == [False, False, False, False] for r in rows())
        self.assertEqual(intact, 4)
        for r in rows():
            if r['first_dead'] is not None:
                self.assertNotEqual(r['register'], [False, False, False, False])


class TestNoDrift(unittest.TestCase):
    def test_snapshot_present(self):
        snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
        self.assertIn('ac68.py', snap)


if __name__ == '__main__':
    unittest.main()
