"""AC33 tests: the mechanism fix, the frozen run, and the passing gate.

Run with: .venv/bin/python -B -m unittest test_ac33
"""
import json
import pathlib
import tempfile
import unittest
import ac33_reacquire as ac33
import ac33_search as asc

ROOT=pathlib.Path('ac33_results_v1')


class TestFrozenRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results=json.loads((ROOT/'results.json').read_text())
        cls.rows=[json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]
        cls.snapshot=json.loads((ROOT/'pre_run_snapshot.json').read_text())

    def test_declared_seeds_and_bar(self):
        self.assertEqual(self.results['seeds'],list(range(3400,3412)))
        self.assertEqual(self.results['bar'],12.00)

    def test_row_shape(self):
        self.assertEqual(len(self.rows),12)
        for row in self.rows:
            self.assertEqual(len(row),len(ac33.ARMS)+1)
            for arm in ac33.ARMS: self.assertIn(arm,row)

    def test_snapshot_matches_the_declared_list_exactly(self):
        """The AC32 discrepancy (5 declared, 4 hashed) must not recur: the snapshot must cover every
        declared source, including ac27/ac30/ac29/ac32 and the protocol."""
        self.assertEqual(sorted(self.snapshot),sorted(ac33.SOURCES))
        self.assertIn('AC33_PROTOCOL_v1.md',self.snapshot)
        self.assertIn('ac33_search.py',self.snapshot)

    def test_verification_tools_are_not_hashed(self):
        for name in ('test_ac33.py','audit_ac33.py','replay_ac33.py'):
            self.assertNotIn(name,self.snapshot)


class TestRecordedGates(unittest.TestCase):
    """All eight pass. Asserted as recorded, with the numbers, so the result cannot drift."""

    @classmethod
    def setUpClass(cls):
        r=json.loads((ROOT/'results.json').read_text())
        cls.g=r['gates']; cls.s=r['summary']

    def test_all_eight_gates_pass(self):
        for name,value in self.g.items():
            self.assertTrue(value,f'{name} recorded False')

    def test_G2_the_failure_AC32_could_not_pass(self):
        """AC32's worst capable individual was 11.75. Here it is 12.33, exactly the worst local
        optimum the landscape engineering predicted."""
        self.assertGreaterEqual(self.s['learner_both']['min'],12.00)
        self.assertAlmostEqual(self.s['learner_both']['min'],12.33,places=2)

    def test_negative_half_still_strict(self):
        self.assertLess(self.s['no_release']['max'],12.00)
        self.assertAlmostEqual(self.s['oracle_a']['max'],10.67,places=2)

    def test_capable_arm_reaches_the_ceiling_somewhere(self):
        self.assertAlmostEqual(self.s['learner_both']['max'],12.67,places=2)
        self.assertAlmostEqual(self.s['oracle_b']['min'],12.67,places=2)

    def test_state_blind_mean_below_bar_with_one_individual_above(self):
        """G5 is on the mean, as disclosed in the protocol; a single random order can exceed BAR."""
        self.assertLess(self.s['no_search']['mean'],12.00)
        self.assertGreaterEqual(self.s['no_search']['max'],12.00)


class TestPreflightActuallyChecks(unittest.TestCase):
    """AC32's process lesson, tested rather than asserted: the pre-flight must parse the protocol's
    declared list and FAIL when it disagrees with what the runner hashes."""

    def test_preflight_passes_on_the_real_protocol(self):
        self.assertEqual(sorted(ac33.preflight()),sorted(ac33.SOURCES))

    def test_preflight_rejects_a_protocol_that_omits_a_source(self):
        real=pathlib.Path('AC33_PROTOCOL_v1.md').read_text()
        doctored=real.replace('ac33_search.py','')
        with tempfile.NamedTemporaryFile('w',suffix='.md',delete=False) as f:
            f.write(doctored); path=f.name
        with self.assertRaises(AssertionError):
            ac33.preflight(path)

    def test_preflight_rejects_a_protocol_declaring_an_extra_source(self):
        real=pathlib.Path('AC33_PROTOCOL_v1.md').read_text()
        doctored=real.replace('ac33_search.py','ac33_search.py nonexistent_extra.py')
        with tempfile.NamedTemporaryFile('w',suffix='.'.join(['md']),delete=False) as f:
            f.write(doctored); path=f.name
        with self.assertRaises(AssertionError):
            ac33.preflight(path)


class TestMechanism(unittest.TestCase):
    def test_steepest_ascent_is_deterministic(self):
        start=(0,1,2,3,4,5)
        a=asc.climb(start,asc.swaps,rates=ac33.RATES_A)
        b=asc.climb(start,asc.swaps,rates=ac33.RATES_A)
        self.assertEqual(a,b)

    def test_swaps_neighbourhood_has_fifteen_members(self):
        self.assertEqual(len(asc.swaps((0,1,2,3,4,5))),15)

    def test_climb_returns_a_one_swap_local_optimum(self):
        """No single swap may improve the result -- that is what 'local optimum' means here."""
        opt,score,steps=asc.climb((5,4,3,2,1,0),asc.swaps,rates=ac33.RATES_B)
        for cand in asc.swaps(opt):
            self.assertLessEqual(ac33.ac32.rating(cand,ac33.RATES_B),score+1e-9)

    def test_runner_cannot_overwrite_its_output(self):
        try:
            ac33.main(seeds=(),root='ac33_results_v1')
            self.fail('the runner reused an existing results directory')
        except FileExistsError:
            pass


if __name__=='__main__':
    unittest.main()
