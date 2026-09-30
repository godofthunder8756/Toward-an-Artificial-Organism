"""Bounded exact A1/A2 checks; no neural training or frozen-file imports."""

from fractions import Fraction
from itertools import product
import unittest

from r10a_v1.decoder_capacity import (
    _rational_feasible,
    codebook_slope_consistent,
    d1_features,
    d2_features,
    decode_witness,
    shared_context_count,
    shared_context_feasible,
    shared_context_witness,
    single_context_count,
    single_context_maps,
    slope_pair_alphabets,
    weak_order_pair_alphabet,
    weak_slope_orders,
)


class CapacityTests(unittest.TestCase):
    def test_exact_eight_word_counts(self):
        self.assertEqual(single_context_count(2), 2 * 3**8 - 2**8)
        self.assertEqual(single_context_count(2), 12866)
        self.assertEqual(single_context_count(3), 6 * 6**8 - 6 * 5**8 + 3**8)
        self.assertEqual(single_context_count(3), 7740507)

    def test_small_combinatorial_enumeration(self):
        for actions in (2, 3):
            for words in (1, 2, 3):
                maps = list(single_context_maps(actions, words))
                self.assertEqual(len(maps), len(set(maps)))
                self.assertEqual(len(maps), single_context_count(actions, words))
        # Every individual pair is realizable, not every joint pair assignment.
        self.assertEqual(set(single_context_maps(2, 1)),
                         {((a, b),) for a, b in product(range(2), repeat=2)})
        self.assertEqual(single_context_count(3, 1), 9)

    def test_weak_orders_and_ties_add_no_pairs(self):
        self.assertEqual(len(weak_slope_orders(3)), 13)
        strict = slope_pair_alphabets(3)
        for ranks in weak_slope_orders(3):
            weak = weak_order_pair_alphabet(ranks)
            self.assertTrue(any(weak <= alphabet for alphabet in strict))
        self.assertEqual(weak_order_pair_alphabet((0, 0, 0)),
                         frozenset((a, a) for a in range(3)))

    def test_single_context_exact_feasibility_matches_combinatorics(self):
        for actions in (2, 3):
            pairs = tuple(product(range(actions), repeat=2))
            for codebook in product(pairs, repeat=2):
                self.assertEqual(shared_context_feasible((codebook,), actions),
                                 codebook_slope_consistent(codebook, actions))

    def test_codebook_and_cross_context_obstructions(self):
        self.assertFalse(shared_context_feasible((((0, 1), (1, 0)),), 2))
        self.assertFalse(shared_context_feasible((((0, 1), (1, 2), (2, 0)),), 3))
        self.assertFalse(shared_context_feasible(
            (((0, 1),), ((1, 2),), ((2, 0),)), 3))
        # Every cell is a constant pair, so global slopes alone accept it.
        crossing = (((1, 1), (0, 0)), ((0, 0), (1, 1)))
        self.assertTrue(codebook_slope_consistent(
            (pair for context in crossing for pair in context), 2))
        self.assertFalse(shared_context_feasible(crossing, 2))
        self.assertFalse(shared_context_feasible(crossing, 3))

    def test_shared_binary_two_by_two_against_exhaustive_integer_grid(self):
        # Independent finite grid constructs all 104 feasible maps in this case.
        # Equality to exact feasibility, not the grid alone, certifies completeness.
        observed = set()
        for u0, u1, v, slope in product(range(-4, 5), repeat=4):
            u = (u0, u1)
            observed.add(tuple(tuple(tuple(int(u[m] + (v if c else 0) +
                                                slope * bit > 0)
                                          for bit in (0, 1))
                                    for m in range(2)) for c in range(2)))
        feasible = set()
        for pairs in product(tuple(product(range(2), repeat=2)), repeat=4):
            table = (pairs[:2], pairs[2:])
            witness = shared_context_witness(table, 2)
            if witness is not None:
                self.assertEqual(decode_witness(witness), table)
                self.assertTrue(all(isinstance(x, Fraction) for x in witness["slope"]))
                feasible.add(table)
        self.assertEqual(feasible, observed)
        self.assertEqual(len(feasible), 104)
        self.assertEqual(shared_context_count(2, words=2, contexts=2), 104)
        self.assertEqual(shared_context_count(3, words=1, contexts=2), 75)

    def test_exact_simplex_and_lowest_index_ties(self):
        # Zero logits select action zero, and strict higher-index wins need margin.
        zero = {"message": [[0], [0], [0]],
                "context": [[0], [0], [0]], "slope": [0, 0, 0]}
        self.assertEqual(decode_witness(zero), (((0, 0),),))
        self.assertIsNotNone(shared_context_witness((((2, 0),),), 3))
        self.assertIsNotNone(shared_context_witness((((0, 0),),), 3))
        self.assertIsNone(_rational_feasible([[1], [-1]], [0, -1], 1))
        self.assertEqual(_rational_feasible([[3], [-3]], [1, -1], 1),
                         (Fraction(1, 3),))
        self.assertEqual(_rational_feasible([], [], 2), (0, 0))
        self.assertIsNone(_rational_feasible([[0]], [-1], 1))


class UpgradeTests(unittest.TestCase):
    def test_d1_constructs_every_single_context_two_word_ternary_map(self):
        for table in product(tuple(product(range(3), repeat=2)), repeat=2):
            weights = []
            for action in range(3):
                intercept = [int(pair[0] == action) for pair in table]
                change = [int(pair[1] == action) - int(pair[0] == action)
                          for pair in table]
                weights.append(intercept + [0] + change)
            for m, pair in enumerate(table):
                for bit, target in enumerate(pair):
                    feature = d1_features(m, bit, words=2)
                    scores = [sum(w * x for w, x in zip(row, feature))
                              for row in weights]
                    self.assertEqual(max(range(3), key=scores.__getitem__), target)

    def test_d2_fixed_relu_hidden_is_lookup(self):
        for m, bit in product(range(8), range(2)):
            feature = d2_features(m, bit)
            self.assertEqual(sum(feature), 1)
            self.assertEqual(feature[2 * m + bit], 1)
        for c, m, bit in product(range(4), range(8), range(2)):
            feature = d2_features(m, bit, context=c, full_context=True)
            self.assertEqual(sum(feature), 1)
            self.assertEqual(feature[2 * (c * 8 + m) + bit], 1)

    def test_full_context_upgrades_construct_arbitrary_table(self):
        # Includes slope cycles, opposite bit directions, and context crossing.
        table = (((0, 1), (1, 0), (2, 2)),
                 ((2, 0), (0, 2), (1, 1)))
        contexts, words, actions = 2, 3, 3
        weights1, weights2 = [], []
        base = 2 * words + 1 + contexts
        for action in range(actions):
            intercept = [int(pair[0] == action) for context in table for pair in context]
            change = [int(pair[1] == action) - int(pair[0] == action)
                      for context in table for pair in context]
            weights1.append([0] * base + intercept + change)
            weights2.append([int(target == action) for context in table
                             for pair in context for target in pair])
        for c, m, bit in product(range(contexts), range(words), range(2)):
            for features, weights in (
                (d1_features(m, bit, words, c, contexts, True), weights1),
                (d2_features(m, bit, words, c, contexts, True), weights2),
            ):
                scores = [sum(w * x for w, x in zip(row, features)) for row in weights]
                self.assertEqual(max(range(actions), key=scores.__getitem__),
                                 table[c][m][bit])

    def test_validation(self):
        with self.assertRaises(ValueError):
            shared_context_witness((((0, 2),),), 2)
        with self.assertRaises(ValueError):
            shared_context_count(2, contexts=0)
        for feature in (d1_features, d2_features):
            with self.assertRaises(ValueError):
                feature(0, 0, full_context=True)
            with self.assertRaises(ValueError):
                feature(8, 0)


if __name__ == "__main__":
    unittest.main()
