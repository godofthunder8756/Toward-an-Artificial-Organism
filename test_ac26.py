"""AC26 tests: the scaled world's signal logic, and the corrected criterion.

Run with: .venv/bin/python -B -m unittest test_ac26
"""
import math
import unittest
import ac25_confront as cf
import ac26_signals as sig


class TestCorrectedCriterion(unittest.TestCase):
    """AC25 said pairwise co-occurrence suffices. It does NOT. Mere co-occurrence inside a larger
    word is not enough, because a word is read by first-match and a third signal can pre-empt the
    comparison. What suffices is an EXACT pair witness: a reachable observation equal to that pair
    and nothing else."""

    def test_exact_pair_witnesses_give_the_full_order(self):
        codes=cf.unique_codes(6)
        self.assertEqual(cf.classes(codes,cf.family_subsets(codes,2)),720)

    def test_co_occurrence_inside_larger_words_is_not_enough(self):
        codes=cf.unique_codes(6)
        self.assertLess(cf.classes(codes,cf.family_subsets(codes,3)),720,'triples only: 360')
        self.assertEqual(cf.classes(codes,cf.family_subsets(codes,3)),360)

    def test_the_cyclic_design_falls_short_at_first_pair_time(self):
        """All 15 pairs co-occur by 323 ticks, and yet only 680 of 720 orders are distinguishable.
        This is the measurement that corrected AC25."""
        fam=sig.reachable(sig.first_pair_time())
        self.assertTrue(all(sig.pair_cooccurrence(fam).values()),'all pairs do co-occur')
        c=cf.classes(cf.unique_codes(6),fam)
        self.assertEqual(c,680)
        self.assertLess(c,720)
        self.assertAlmostEqual(math.log2(c),9.41,places=2)

    def test_the_cyclic_design_does_reach_full_structure_at_the_full_period(self):
        """Because only then does every subset -- including every exact pair -- occur."""
        fam=sig.reachable(sig.full_lcm())
        self.assertEqual(len(fam),64,'all subsets reachable')
        self.assertEqual(cf.classes(cf.unique_codes(6),fam),720)


class TestStructureOfTheConstruction(unittest.TestCase):
    def test_periods_are_pairwise_coprime(self):
        P=sig.PERIODS
        for i in range(len(P)):
            for j in range(i+1,len(P)):
                self.assertEqual(math.gcd(P[i],P[j]),1,f'{P[i]},{P[j]}')

    def test_every_pair_occurs_within_its_max_pair_lcm(self):
        tp=sig.first_pair_time()
        self.assertTrue(all(sig.pair_cooccurrence(sig.reachable(tp)).values()))
        self.assertEqual(tp,17*19,'the largest coprime pair')

    def test_all_six_signals_are_live(self):
        fam=sig.reachable(sig.full_lcm())
        union=0
        for w in fam: union|=w
        self.assertEqual(union,(1<<6)-1)


class TestControls(unittest.TestCase):
    def test_exclusive_epochs_cost_almost_everything(self):
        """The frozen world's habit -- making groups mutually exclusive -- applied to the same
        needs. Only within-group pairs can co-occur, and the order structure collapses."""
        fam=sig.epochs_family(2000)
        pairs=sig.pair_cooccurrence(fam)
        self.assertLess(sum(pairs.values()),len(pairs))
        c=cf.classes(cf.unique_codes(6),fam)
        self.assertAlmostEqual(math.log2(c),3.0,places=2)

    def test_frozen_signals_reproduce_one_bit(self):
        c=cf.classes([1<<2,1<<3,1<<4,1<<5],sig.frozen_masks_family(),[2,3,4,5])
        self.assertEqual(c,2)


if __name__=='__main__':
    unittest.main()
