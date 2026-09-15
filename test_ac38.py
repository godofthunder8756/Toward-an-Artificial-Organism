"""AC38 tests: the variance structure of paired comparisons, and the exact test on the frozen studies.

Run with: .venv/bin/python -B -m unittest test_ac38
"""
import json
import pathlib
import unittest
import numpy as np
import ac38_variance as ac38
import ac36_survival as ac36


class TestSignFlipTest(unittest.TestCase):
    def test_floor_is_two_over_two_to_the_n(self):
        """The exact test's minimum p at n individuals: all differences the same sign."""
        for n in (4,8,12):
            t=ac38.sign_flip_test([1.0]*n)
            self.assertAlmostEqual(t['p'],2.0/(2**n),places=6,msg=f'n={n}')

    def test_a_null_contrast_is_not_significant(self):
        t=ac38.sign_flip_test([1.0,-1.0,1.0,-1.0,1.0,-1.0,1.0,-1.0])
        self.assertGreater(t['p'],0.5)

    def test_four_individuals_cannot_reach_significance(self):
        """The power floor that made AC37's encouraging engineering meaningless."""
        best=ac38.sign_flip_test([4.0,4.0,4.0,4.0])
        self.assertAlmostEqual(best['p'],0.125,places=4)
        self.assertGreater(best['p'],0.01,'n=4 can never reach conventional significance')


class TestVarianceStructure(unittest.TestCase):
    """The counterintuitive finding: in this endpoint the paired difference is NOISIER than the
    marginal rating, so the inherited criterion was lenient rather than conservative."""

    @classmethod
    def setUpClass(cls):
        cls.m=ac38.marginal_and_paired((1,0,2,3,4,5),(4,5,1,2,0,3),
                                       ac36.rating,ac36.RATES_B,sets=6)

    def test_pairing_does_not_reduce_the_noise_here(self):
        """Measured 0.82 at 8 seed sets and 1.06 at 6 -- i.e. no meaningful reduction either way. The
        robust claim is that the seed-set identity is NOT the dominant variance component, which is
        what invalidates the assumption that a paired design makes the marginal noise an overestimate."""
        self.assertAlmostEqual(self.m['reduction'],1.0,delta=0.5,
                               msg=f"reduction {self.m['reduction']:.2f} -- pairing bought nothing")
        self.assertGreaterEqual(self.m['sigma_delta'],0.9*self.m['sigma_marginal'],
                                'the difference is no quieter than the levels')

    def test_the_paired_difference_is_still_large(self):
        self.assertGreater(self.m['mean_delta'],1.0)

    def test_the_two_orders_share_the_seed_sets(self):
        """Both orders are scored on the same sets, which is what makes the difference paired."""
        self.assertEqual(len(self.m['a']),len(self.m['b']),len(self.m['delta']))


class TestFrozenStudies(unittest.TestCase):
    """Post-hoc exact tests on the recorded runs. Labelled post-hoc: they check results already
    declared, and are not the basis on which those results were declared."""

    def test_both_passing_claims_are_maximally_significant(self):
        for root in ('ac33_results_v1','ac36_results_v1'):
            rows=ac38.frozens_rows(root)
            t=ac38.contrast(rows,'learner_both','no_release')
            self.assertAlmostEqual(t['p'],2.0/2**12,places=6,
                                   msg=f'{root}: every individual must favour the capable arm')
            self.assertGreater(t['observed'],1.0)

    def test_ac32_contrast_was_significant_yet_it_failed(self):
        """AC32 failed G2, the reliability condition -- not its contrast. The gate shape worked."""
        rows=ac38.frozens_rows('ac32_results_v1')
        t=ac38.contrast(rows,'learner_both','no_release')
        self.assertLess(t['p'],0.01)
        results=json.loads((pathlib.Path('ac32_results_v1')/'results.json').read_text())
        self.assertFalse(results['gates']['G2_learner_worst_at_or_above_bar'],
                         'AC32 is recorded as failing the ceiling gate, not the contrast')

    def test_ac37_engineering_was_underpowered(self):
        t=ac38.sign_flip_test([5.08-2.58,5.92-1.75,7.67-1.75,6.33-2.58])
        self.assertAlmostEqual(t['p'],0.125,places=4)
        self.assertGreater(t['p'],0.01)

    def test_state_blind_contrasts_are_significant_in_the_passing_studies(self):
        for root in ('ac33_results_v1','ac36_results_v1'):
            rows=ac38.frozens_rows(root)
            self.assertLess(ac38.contrast(rows,'learner_both','no_search')['p'],0.01,msg=root)


class TestNothingWasFrozenByThisStudy(unittest.TestCase):
    def test_no_protocol_or_results_dir(self):
        root=pathlib.Path('.')
        self.assertFalse((root/'AC38_PROTOCOL_v1.md').exists(),
                         'AC38 is analysis: it declares no seeds and runs no finals')
        self.assertFalse(list(root.glob('ac38_results_*')))


if __name__=='__main__':
    unittest.main()
