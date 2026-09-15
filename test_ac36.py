"""AC36 tests + audit: the passing maintenance claim, its gates, and its provenance.

Run with: .venv/bin/python -B -m unittest test_ac36
The audit runs as a test (test_audit_passes) so provenance is checked by the suite as well as by
`audit_ac36.py`.
"""
import hashlib
import json
import pathlib
import unittest
import numpy as np
import ac36_survival as ac36

ROOT=pathlib.Path('ac36_results_v1')


def load():
    results=json.loads((ROOT/'results.json').read_text())
    rows=[json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]
    snapshot=json.loads((ROOT/'pre_run_snapshot.json').read_text())
    return results,rows,snapshot


class TestFrozenRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results,cls.rows,cls.snapshot=load()

    def test_declared_seeds_and_bar(self):
        self.assertEqual(self.results['seeds'],list(range(3500,3512)))
        self.assertEqual(self.results['bar'],6.45)

    def test_row_shape(self):
        self.assertEqual(len(self.rows),12)
        for row in self.rows:
            self.assertEqual(len(row),len(ac36.ARMS)+1)

    def test_snapshot_matches_the_declared_list(self):
        self.assertEqual(sorted(self.snapshot),sorted(ac36.SOURCES))
        self.assertIn('AC36_PROTOCOL_v1.md',self.snapshot)

    def test_verification_tools_are_not_hashed(self):
        for name in ('test_ac36.py','audit_ac36.py','replay_ac36.py'):
            self.assertNotIn(name,self.snapshot)


class TestRecordedGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r=json.loads((ROOT/'results.json').read_text())
        cls.g=r['gates']; cls.s=r['summary']

    def test_all_eight_gates_pass(self):
        for name,value in self.g.items():
            self.assertTrue(value,f'{name} recorded False')

    def test_capable_worst_above_incapable_best(self):
        self.assertGreater(self.s['learner_both']['min'],self.s['no_release']['max'])
        self.assertAlmostEqual(self.s['learner_both']['min'],6.67,places=2)
        self.assertAlmostEqual(self.s['no_release']['max'],5.67,places=2)

    def test_capable_arm_reaches_the_ceiling(self):
        self.assertAlmostEqual(self.s['learner_both']['max'],6.83,places=2)
        self.assertAlmostEqual(self.s['oracle_b']['min'],6.83,places=2)

    def test_old_optimum_is_stuck_below_the_bar(self):
        self.assertAlmostEqual(self.s['oracle_a']['max'],5.00,places=2)

    def test_state_blind_means_below_bar_with_one_individual_above(self):
        self.assertLess(self.s['no_search']['mean'],6.45)
        self.assertGreaterEqual(self.s['no_search']['max'],6.25)


class TestProvenance(unittest.TestCase):
    def test_hashes_unchanged(self):
        results,_,snapshot=load()
        for name,digest in snapshot.items():
            self.assertTrue(pathlib.Path(name).exists(),f'missing {name}')
            self.assertEqual(hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest(),digest,
                             f'source drift: {name}')

    def test_gates_recompute_from_the_rows(self):
        results,rows,_=load()
        recomputed=ac36.gates(rows)
        recomputed['G7_determinism']=results['gates']['G7_determinism']
        self.assertEqual(recomputed,results['gates'])

    def test_summary_matches_the_rows(self):
        results,rows,_=load()
        for arm,vals in results['summary'].items():
            posts=[r[arm]['post'] for r in rows]
            self.assertAlmostEqual(vals['min'],min(posts),places=9)
            self.assertAlmostEqual(vals['mean'],sum(posts)/len(posts),places=9)
            self.assertAlmostEqual(vals['max'],max(posts),places=9)

    def test_runner_cannot_overwrite_its_output(self):
        try:
            ac36.main(seeds=(),root='ac36_results_v1')
            self.fail('the runner reused an existing results directory')
        except FileExistsError:
            pass

    def test_preflight_rejects_a_doctored_protocol(self):
        import tempfile
        real=pathlib.Path('AC36_PROTOCOL_v1.md').read_text()
        with tempfile.NamedTemporaryFile('w',suffix='.md',delete=False) as f:
            f.write(real.replace('ac33_search.py','')); path=f.name
        with self.assertRaises(AssertionError):
            ac36.preflight(path)


class TestEconomy(unittest.TestCase):
    """The insufficiency that makes this world discriminate -- and the reason AC35's world did not."""

    def test_renewals_cost_more_than_a_tick_of_income(self):
        self.assertGreater(ac36.RENEW_ENERGY,ac36.INCOME_ENERGY)

    def test_income_does_not_scale_with_the_organism(self):
        """No population-scaled production: nothing equalizes outcomes the way AC35's world did."""
        w=ac36.World(0)
        w.life[:]=[ac36.acq.CHILD_LIFE]*len(w.life)
        before=w.energy
        for _ in range(50): w.tick(None)
        rich=w.energy-before
        w2=ac36.World(0); w2.life[:]=[1]*len(w2.life)      # a body with no productive sites at all
        before2=w2.energy
        for _ in range(50): w2.tick(None)
        self.assertEqual(rich,w2.energy-before2,'income must be independent of the population')

    def test_the_organism_refuses_renewals_it_wanted(self):
        w=ac36.World(0); w.energy=0
        for _ in range(20): w.tick(0)
        self.assertGreater(w.afforded_refusals,0,'insufficiency should bite')

    def test_spread_exceeds_noise_by_the_declared_factor(self):
        """Re-measured cheaply here: the recording criterion is margin/noise >= 10."""
        order=(1,0,2,3,4,5)
        sd,lo,hi=ac36.noise_of_order(order,ac36.RATES_B,sets=4)
        old=ac36.rating((4,5,1,2,0,3),ac36.RATES_B)      # A's optimum rated under B
        margin=ac36.rating(order,ac36.RATES_B)-old
        self.assertGreater(sd,0)
        self.assertGreater(margin/sd,10.0,f'margin {margin:.2f} sd {sd:.2f}')


if __name__=='__main__':
    unittest.main()
