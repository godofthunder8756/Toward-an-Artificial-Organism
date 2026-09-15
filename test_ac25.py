"""AC25 tests: confrontability -- what makes a rule order learnable.

Run with: .venv/bin/python -B -m unittest test_ac25
"""
import itertools
import math
import unittest
import ac25_confront as cf


class TestOrderInformationRequiresConfrontation(unittest.TestCase):
    """The two theorems, measured."""

    def test_singletons_alone_give_zero_order_information(self):
        """However many signals are live, if no two ever co-occur the order is invisible."""
        for B in (2,3,4,6):
            codes=cf.unique_codes(B)
            self.assertEqual(cf.classes(codes,cf.family_subsets(codes,1)),1,f'B={B}')

    def test_pairs_suffice_for_the_full_order(self):
        """A total order is determined by its pairwise comparisons."""
        codes=cf.unique_codes(6)
        self.assertEqual(cf.classes(codes,cf.family_subsets(codes,2)),math.factorial(6))
        self.assertAlmostEqual(cf.effective_bits(codes,cf.family_subsets(codes,2)),9.49,places=2)

    def test_higher_arity_is_not_monotone(self):
        """All triples buy LESS than all pairs: a triple reveals only the winner and hides the
        pairwise relations among the two it beat."""
        codes=cf.unique_codes(6)
        triples=cf.classes(codes,cf.family_subsets(codes,3))
        pairs=cf.classes(codes,cf.family_subsets(codes,2))
        self.assertEqual(triples,360)
        self.assertLess(triples,pairs)

    def test_singletons_plus_pairs_is_maximal(self):
        codes=cf.unique_codes(6)
        self.assertEqual(cf.classes(codes,cf.family_subsets(codes,1)+cf.family_subsets(codes,2)),
                         math.factorial(6))
        self.assertEqual(cf.classes(codes,cf.family_all(codes)),math.factorial(6))


class TestDilution(unittest.TestCase):
    def test_one_dead_position_costs_a_quarter_of_the_structure(self):
        codes=cf.unique_codes(6)
        obs=cf.family_subsets(codes[1:],2)+cf.family_subsets(codes[1:],1)
        self.assertEqual(cf.classes(codes[1:],obs),120)
        self.assertAlmostEqual(cf.effective_bits(codes[1:],obs),6.91,places=2)

    def test_four_live_positions_all_confronted_give_the_full_4_58(self):
        """Which is what proves the frozen world's 1.00 bit is a deadness effect, not a property of
        four-position controllers."""
        codes=cf.unique_codes(6)
        obs=cf.family_subsets(codes[2:],2)+cf.family_subsets(codes[2:],1)
        self.assertEqual(cf.classes(codes[2:],obs),24)
        self.assertAlmostEqual(cf.effective_bits(codes[2:],obs),4.58,places=2)

    def test_fusing_mask_and_action_costs_what_a_dead_position_costs(self):
        codes=cf.unique_codes(6)
        fused=[codes[0],codes[0]]+codes[1:5]
        obs=sorted(set(cf.family_subsets(codes[:5],1)+cf.family_subsets(codes[:5],2)))
        self.assertEqual(cf.classes(fused,obs,[0,0,1,2,3,4]),120,'fused pair = one position')

    def test_fused_mask_with_distinct_actions_recovers_half(self):
        codes=cf.unique_codes(6)
        fused=[codes[0],codes[0]]+codes[1:5]
        obs=sorted(set(cf.family_subsets(codes[:5],1)+cf.family_subsets(codes[:5],2)))
        self.assertEqual(cf.classes(fused,obs,[0,99,1,2,3,4]),240,'2 x 120')


class TestFrozenControl(unittest.TestCase):
    def test_frozen_configuration_reproduces_ac24(self):
        """Two independent methods, same number: 2 behaviour classes, 1.00 bit."""
        frozen=[1<<2,1<<3,1<<4,1<<5]
        obs=[1<<2,1<<3,1<<2|1<<3]
        c=cf.classes(frozen,obs,[2,3,4,5])
        self.assertEqual(c,2)
        self.assertAlmostEqual(math.log2(c),1.0)


class TestScaledCriterion(unittest.TestCase):
    def test_the_acceptance_number_is_720(self):
        """The scaled world's criterion, recorded so a future build is checked against it rather
        than argued about."""
        codes=cf.unique_codes(6)
        self.assertEqual(cf.classes(codes,cf.family_subsets(codes,2)),720)
        self.assertEqual(math.factorial(6),720)


if __name__=='__main__':
    unittest.main()
