"""AC32 tests: the frozen re-acquisition run, its gates, and the recorded falsification.

Run with: .venv/bin/python -B -m unittest test_ac32
"""
import json
import pathlib
import unittest
import numpy as np
import ac32_reacquire as ac

ROOT=pathlib.Path('ac32_results_v1')


class TestFrozenRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results=json.loads((ROOT/'results.json').read_text())
        cls.rows=[json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]
        cls.snapshot=json.loads((ROOT/'pre_run_snapshot.json').read_text())

    def test_row_count_and_shape(self):
        self.assertEqual(len(self.rows),12)
        self.assertEqual(len(self.rows)*len(ac.ARMS),72)
        for row in self.rows:
            for arm in ac.ARMS:
                self.assertIn(arm,row)

    def test_seeds_are_the_declared_finals(self):
        self.assertEqual(self.results['seeds'],list(range(3300,3312)))

    def test_declared_bar(self):
        self.assertEqual(self.results['bar'],12.00)

    def test_snapshot_records_the_documented_discrepancy(self):
        """The protocol declared FIVE sources; the runner hashed FOUR, omitting ac27_schedule.py.
        Asserted as recorded, not tidied: the discrepancy must stay visible."""
        self.assertEqual(sorted(self.snapshot),['AC32_PROTOCOL_v1.md','ac29_register.py',
                                               'ac30_acquire.py','ac32_reacquire.py'])
        self.assertNotIn('ac27_schedule.py',self.snapshot)
        import hashlib,pathlib
        self.assertEqual(hashlib.sha256(pathlib.Path('ac27_schedule.py').read_bytes()).hexdigest(),
                         '402ae74b6c60943dbe982048b502e531d9ef111b350c97e44d977e68addc1896',
                         'the omitted source must still match its post-hoc verified hash')

    def test_verification_tools_are_not_hashed(self):
        """AC17's lesson: hashing a verification tool into the snapshot creates a self-inflicted
        drift the moment the tool is improved."""
        for name in ('test_ac32.py','audit_ac32.py','replay_ac32.py'):
            self.assertNotIn(name,self.snapshot)


class TestRecordedGates(unittest.TestCase):
    """The recorded outcome. G2 is asserted FALSE so a future attempt cannot quietly forget that the
    study is falsified and re-announce it as a pass."""

    @classmethod
    def setUpClass(cls):
        cls.g=json.loads((ROOT/'results.json').read_text())['gates']
        cls.s=json.loads((ROOT/'results.json').read_text())['summary']

    def test_G1_ceiling(self):
        self.assertTrue(self.g['G1_oracle_b_ceiling_at_or_above_bar'])

    def test_G2_FAILED_as_recorded(self):
        self.assertFalse(self.g['G2_learner_worst_at_or_above_bar'],
                         'G2 must remain recorded as FAILED')
        self.assertLess(self.s['learner_both']['min'],12.00)
        self.assertAlmostEqual(self.s['learner_both']['min'],11.75,places=2)

    def test_G3_and_G4_negative_half_established(self):
        self.assertTrue(self.g['G3_no_release_best_below_bar'])
        self.assertTrue(self.g['G4_oracle_a_best_below_bar'])
        self.assertLessEqual(self.s['no_release']['max'],11.00)
        self.assertAlmostEqual(self.s['oracle_a']['mean'],10.67,places=2)

    def test_G5_on_means_not_minima(self):
        """The protocol recorded in advance that individual state-blind runs can exceed BAR; G5 is
        therefore stated on the mean, and that choice is part of the record."""
        self.assertTrue(self.g['G5_state_blind_means_below_bar'])
        self.assertLess(self.s['no_search']['mean'],12.00)
        self.assertGreaterEqual(self.s['no_search']['max'],12.00,
                                'a single random order did exceed BAR, as disclosed')

    def test_G6_G7_G8(self):
        self.assertTrue(self.g['G6_all_arms_complete'])
        self.assertTrue(self.g['G7_determinism'])
        self.assertTrue(self.g['G8_register_in_the_loop'])

    def test_learner_is_at_the_ceiling_for_almost_every_individual(self):
        """The mechanism is real: 11 of 12 individuals sit within 0.25 of the scaffold ceiling."""
        posts=[r['learner_both']['post'] for r in
               [json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]]
        near_ceiling=sum(1 for p in posts if p>=12.33)
        self.assertEqual(near_ceiling,11)


class TestGateArithmeticOnSyntheticRows(unittest.TestCase):
    """The gate function itself, exercised independently of the frozen run."""

    def _rows(self,learner,no_release,oracle_a,blind):
        return [dict(seed=i,learner_both=dict(post=learner,held=[0,1,2,3,4,5]),
                     no_release=dict(post=no_release,held=[0,1,2,3,4,5]),
                     no_search=dict(post=blind,held=[0,1,2,3,4,5]),
                     preserve=dict(post=blind,held=[0,1,2,3,4,5]),
                     oracle_a=dict(post=oracle_a,held=[0,1,2,3,4,5]),
                     oracle_b=dict(post=12.67,held=[0,1,2,3,4,5])) for i in range(3)]

    def test_all_gates_pass_on_a_perfect_separation(self):
        g=ac.gates(self._rows(12.5,10.0,10.67,11.0))
        for k,v in g.items():
            if k!='G7_determinism': self.assertTrue(v,k)

    def test_g2_fails_when_the_learner_has_a_bad_individual(self):
        rows=self._rows(12.5,10.0,10.67,11.0)[:2]+[dict(seed=9,
                     learner_both=dict(post=11.0,held=[0,1,2,3,4,5]),
                     no_release=dict(post=10.0,held=[0,1,2,3,4,5]),
                     no_search=dict(post=11.0,held=[0,1,2,3,4,5]),
                     preserve=dict(post=11.0,held=[0,1,2,3,4,5]),
                     oracle_a=dict(post=10.67,held=[0,1,2,3,4,5]),
                     oracle_b=dict(post=12.67,held=[0,1,2,3,4,5]))]
        self.assertFalse(ac.gates(rows)['G2_learner_worst_at_or_above_bar'])


if __name__=='__main__':
    unittest.main()
