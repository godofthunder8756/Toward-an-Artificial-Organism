"""AC29 tests: the register for a six-position order, and how its integrity scales.

Run with: .venv/bin/python -B -m unittest test_ac29
"""
import itertools
import math
import unittest
import numpy as np
import ac29_register as rg


class TestEncoding(unittest.TestCase):
    def test_round_trip_over_all_720_orders(self):
        """The check that caught two harness bugs in this module."""
        for order in itertools.permutations(range(rg.N)):
            self.assertEqual(rg.unlehmer(rg.lehmer(order)),order)

    def test_codes_are_dense_and_bounded(self):
        codes={rg.lehmer(o) for o in itertools.permutations(range(rg.N))}
        self.assertEqual(codes,set(range(720)))

    def test_out_of_range_codes_are_not_orders(self):
        self.assertIsNone(rg.unlehmer(720))
        self.assertIsNone(rg.unlehmer(1023))
        self.assertIsNone(rg.unlehmer(-1))

    def test_the_space_is_not_filled_by_orders(self):
        """10 bits hold 1024 values, only 720 of which are orders: the coding weakness."""
        valid=sum(1 for c in range(1<<rg.BITS) if rg.unlehmer(c) is not None)
        self.assertEqual(valid,720)
        self.assertLess(valid,1<<rg.BITS)


class TestDamageModel(unittest.TestCase):
    def test_bit_wrong_probability_is_bounded_and_monotone(self):
        prev=0.0
        for t in (10,100,1000,10000,100000):
            p=rg.p_bit_wrong(1e-4,t)
            self.assertGreaterEqual(p,prev); self.assertLessEqual(p,0.5)
            prev=p

    def test_bit_wrong_saturates_at_half(self):
        """A fully randomised replica set is right half the time by symmetry -- which is why a
        'half-chance' metric is not comparable between objects of different width."""
        self.assertAlmostEqual(rg.p_bit_wrong(1e-4,10**7),0.5,places=4)

    def test_distribution_is_a_probability_distribution(self):
        dist=rg.code_distribution(0,1e-4,1000)
        self.assertAlmostEqual(sum(dist.values()),1.0,places=9)


class TestRegisterBehaviour(unittest.TestCase):
    def test_an_intact_register_agrees_with_itself(self):
        """The measurement that exposed the broken inverse: an intact store must score 1.0."""
        target=tuple(range(rg.N))
        reg=rg.Register(); reg.write(rg.lehmer(target))
        self.assertEqual(reg.read(),target)
        words=__import__('ac27_schedule').all_pairs()
        self.assertEqual(rg.behavioural_agreement(reg.read(),target,words),1.0)

    def test_repair_restores_light_damage(self):
        rng=np.random.default_rng(0)
        reg=rg.Register(); reg.write(rg.lehmer(tuple(range(rg.N))))
        for _ in range(20): reg.damage(rng,0.001)
        reg.repair(rg.BITS)
        self.assertEqual(reg.read(),tuple(range(rg.N)))

    def test_repair_cannot_correct_a_flipped_majority(self):
        """Majority-write repair is error-PRESERVING, not error-correcting: it writes the majority
        back, so a bit whose majority has already flipped is frozen wrong. Holding a multi-bit
        object against sustained damage needs an external reference or an error-correcting code, not
        more replication -- which is why the frozen world's `protected` arm had to keep its own
        copy."""
        rng=np.random.default_rng(1)
        reg=rg.Register(); reg.write(rg.lehmer(tuple(range(rg.N))))
        for _ in range(400): reg.damage(rng,0.02)
        reg.repair(rg.BITS)
        for k in range(rg.BITS):
            ones=int(reg.bits[k].sum())
            self.assertIn(ones,(0,reg.replicas),'repair makes every bit unanimous')
        self.assertNotEqual(reg.read(),tuple(range(rg.N)),
                            'and it does not restore the original order')

    def test_unreadable_store_scores_zero_agreement(self):
        self.assertEqual(rg.behavioural_agreement(None,tuple(range(rg.N)),[1]),0.0)

    def test_a_wrong_order_can_still_answer_some_words_correctly(self):
        """The AC14 lesson: bit-level correctness is not the endpoint. A reordered store may agree
        with the target on words whose first urgent region happens to be the same."""
        target=(0,1,2,3,4,5); other=(1,0,2,3,4,5)
        words=[1<<0|1<<1]
        self.assertEqual(rg.behavioural_agreement(other,target,words),0.0)
        words=[1<<2|1<<3]
        self.assertEqual(rg.behavioural_agreement(other,target,words),1.0)


class TestScaling(unittest.TestCase):
    def test_weakest_link_is_k_to_the_quarter_not_k(self):
        """The majority-of-7 failure is a fourth-power process, so widening the stored object from
        1 bit to 10 costs only 10^(1/4) ~ 1.78 in time, not 10x."""
        self.assertAlmostEqual(rg.BITS**0.25,1.78,places=2)

    def test_bits_are_the_ceiling_of_log2_of_the_order_count(self):
        self.assertEqual(rg.BITS,math.ceil(math.log2(720)))
        self.assertEqual(rg.VALID,720)


if __name__=='__main__':
    unittest.main()
