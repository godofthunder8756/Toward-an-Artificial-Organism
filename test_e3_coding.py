"""Constructed coding conformance fixtures, not experimental target draws.

Only pure values are checked. No agent, physical writes, paid scan, protected
copy, training, runner, or kernel execution-trace conformance is exercised.
"""

from collections import Counter
from dataclasses import FrozenInstanceError
from itertools import combinations, product
import unittest

from e3.coding import (
    CODEBOOK,
    GENERATOR_COLUMNS,
    DecodeResult,
    decode_block,
    decode_repetition,
    encode,
)


def reference_word(payload):
    """Independent four-term binary dot product, not production parity code."""
    columns = (*range(1, 16), 1, 2, 4, 8, 15)
    bits = tuple((payload // (2 ** k)) % 2 for k in range(4))
    return tuple(
        sum(bits[k] * ((column // (2 ** k)) % 2) for k in range(4)) % 2
        for column in columns
    )


REFERENCE_WORDS = tuple(reference_word(payload) for payload in range(16))


def reference_decode(symbols, words):
    """Offline exhaustive oracle over generic words, never a true label."""
    positions = [i for i, value in enumerate(symbols) if value in (0, 1)]
    if not positions:
        return (None, 0, 0, None, len(words))
    distances = [sum(symbols[i] != word[i] for i in positions) for word in words]
    best = min(distances)
    winners = [i for i, distance in enumerate(distances) if distance == best]
    if len(winners) > 1:
        return (None, 1, len(positions), best, len(winners))
    health = 2 if len(positions) == len(symbols) and best == 0 else 3
    return (winners[0], health, len(positions), best, 1)


def fields(result):
    return (
        result.payload, result.health, result.observed,
        result.disagreements, result.ties_count,
    )


class TestE3Coding(unittest.TestCase):
    def test_all_sixteen_encodings_and_immutable_generic_rom(self):
        self.assertEqual(GENERATOR_COLUMNS, (*range(1, 16), 1, 2, 4, 8, 15))
        self.assertIsInstance(CODEBOOK, tuple)
        self.assertEqual(len(set(CODEBOOK)), 16)
        for payload, reference in enumerate(REFERENCE_WORDS):
            word = encode(payload)
            self.assertIsInstance(word, tuple)
            self.assertEqual(len(word), 20)
            self.assertTrue(all(type(symbol) is int and symbol in (0, 1) for symbol in word))
            self.assertEqual(word, reference)
            self.assertEqual(CODEBOOK[payload], reference)
            self.assertEqual(fields(decode_block(word)), (payload, 2, 20, 0, 1))
        with self.assertRaises(TypeError):
            CODEBOOK[0][0] = 1

    def test_result_is_frozen_and_has_no_mutable_instance_dictionary(self):
        result = decode_block(REFERENCE_WORDS[7])
        self.assertIsInstance(result, DecodeResult)
        self.assertFalse(hasattr(result, "__dict__"))
        for name in ("payload", "health", "observed", "disagreements", "ties_count"):
            with self.assertRaises(FrozenInstanceError):
                setattr(result, name, 0)

    def test_all_120_full_and_punctured_pair_distances(self):
        full = Counter()
        punctured = Counter()
        for left, right in combinations(REFERENCE_WORDS, 2):
            full[sum(a != b for a, b in zip(left, right))] += 1
            punctured[sum(left[i] != right[i] for i in range(12))] += 1
        self.assertEqual(sum(full.values()), 120)
        self.assertEqual(full, {10: 80, 12: 40})
        self.assertEqual(punctured, {5: 16, 6: 48, 7: 48, 8: 8})
        self.assertEqual(min(full), 10)
        self.assertEqual(min(punctured), 5)

    def test_empty_erased_invalid_and_mixed_abstain_without_mutation(self):
        for decoder, n, ties in ((decode_block, 20, 16), (decode_repetition, 5, 2)):
            for source in ([2] * n, [3] * n, [2, 3] * (n // 2) + [2] * (n % 2)):
                before = source[:]
                for _ in range(3):
                    self.assertEqual(fields(decoder(source)), (None, 0, 0, None, ties))
                    self.assertEqual(source, before)

    def test_all_repetition_inputs_against_independent_oracle(self):
        words = ((0,) * 5, (1,) * 5)
        for symbols in product(range(4), repeat=5):
            self.assertEqual(fields(decode_repetition(symbols)), reference_decode(symbols, words))

    def test_every_single_binary_block_observation_is_ambiguous(self):
        for index, bit, missing in product(range(20), range(2), (2, 3)):
            source = [missing] * 20
            source[index] = bit
            self.assertEqual(fields(decode_block(source)), (None, 1, 1, 0, 8))

    def test_all_single_and_double_flips_and_four_flip_boundary(self):
        for payload, word in enumerate(REFERENCE_WORDS):
            for size in (1, 2):
                for flipped in combinations(range(20), size):
                    source = list(word)
                    for index in flipped:
                        source[index] = 1 - source[index]
                    self.assertEqual(fields(decode_block(source)), (payload, 3, 20, size, 1))
            # Four flips are guaranteed correct by d=10; use every window.
            for start in range(20):
                source = list(word)
                for offset in range(4):
                    index = (start + offset) % 20
                    source[index] = 1 - source[index]
                self.assertEqual(fields(decode_block(source)), (payload, 3, 20, 4, 1))

    def test_minimum_distance_midpoints_and_nine_erasure_boundary(self):
        pairs = 0
        for left, right in combinations(REFERENCE_WORDS, 2):
            differing = [i for i in range(20) if left[i] != right[i]]
            if len(differing) != 10:
                continue
            pairs += 1
            midpoint = list(left)
            for index in differing[:5]:
                midpoint[index] = right[index]
            self.assertEqual(fields(decode_block(midpoint)), reference_decode(midpoint, REFERENCE_WORDS))
            self.assertIsNone(decode_block(midpoint).payload)
            self.assertEqual(decode_block(midpoint).health, 1)
            for missing in (2, 3):
                erased = [missing if i in differing else left[i] for i in range(20)]
                tied = decode_block(erased)
                self.assertIsNone(tied.payload)
                self.assertEqual(tied.health, 1)
                self.assertEqual(tied.disagreements, 0)
                for survivor in differing:
                    source = erased[:]
                    source[survivor] = left[survivor]
                    self.assertEqual(
                        fields(decode_block(source)),
                        (REFERENCE_WORDS.index(left), 3, 11, 0, 1),
                    )
        self.assertEqual(pairs, 80)

    def test_physical_layers_three_four_erased_and_all_two_survivor_flips(self):
        erased_positions = {4 * k + r for k in (3, 4) for r in range(4)}
        self.assertEqual(erased_positions, set(range(12, 20)))
        for payload, word in enumerate(REFERENCE_WORDS):
            for size in (0, 1, 2):
                for flipped in combinations(range(12), size):
                    source = list(word[:12]) + [2] * 8
                    for index in flipped:
                        source[index] = 1 - source[index]
                    self.assertEqual(fields(decode_block(source)), (payload, 3, 12, size, 1))
            for bit in (0, 1):
                self.assertEqual(fields(decode_repetition([bit] * 3 + [2] * 2)), (bit, 3, 3, 0, 1))

    def test_punctured_three_flip_miscorrection_is_not_oracle_repaired(self):
        left, right = next(
            (a, b) for a, b in combinations(REFERENCE_WORDS, 2)
            if sum(a[i] != b[i] for i in range(12)) == 5
        )
        source = list(left[:12]) + [2] * 8
        differing = [i for i in range(12) if left[i] != right[i]]
        for index in differing[:3]:
            source[index] = right[index]
        self.assertEqual(
            fields(decode_block(source)),
            (REFERENCE_WORDS.index(right), 3, 12, 2, 1),
        )

    def test_wrong_self_consistent_words_are_intact_and_no_history_is_kept(self):
        for payload in range(16):
            decode_block(REFERENCE_WORDS[payload])
            other = payload ^ 15
            self.assertEqual(fields(decode_block(REFERENCE_WORDS[other])), (other, 2, 20, 0, 1))
            self.assertEqual(decode_block([2] * 20).health, 0)
        decode_repetition([0] * 5)
        self.assertEqual(fields(decode_repetition([1] * 5)), (1, 2, 5, 0, 1))

    def test_sixteen_fixed_label_tables_are_constructed_fixtures_only(self):
        # Every row is a fixed 16-cue algebraic fixture, not an individual or draw.
        tables = tuple(
            tuple(sum(((mask >> k) & 1) * ((cue >> k) & 1) for k in range(4)) % 2
                  for cue in range(16))
            for mask in range(16)
        )
        for table in tables:
            for block in range(4):
                payload = sum(table[4 * block + k] * (2 ** k) for k in range(4))
                self.assertEqual(decode_block(encode(payload)).payload, payload)
                self.assertIsNone(decode_block([2] * 20).payload)

    def test_input_validation_rejects_bool_coercion_lengths_and_encodings(self):
        for value in (True, False, 1.0, "1", None, [1]):
            with self.assertRaises(TypeError):
                encode(value)
        for value in (-1, 16, 65535):
            with self.assertRaises(ValueError):
                encode(value)
        for decoder, n in ((decode_block, 20), (decode_repetition, 5)):
            for size in (0, n - 1, n + 1):
                with self.assertRaises(ValueError):
                    decoder([0] * size)
            for value in (True, False, 0.0, "0", None):
                source = [0] * n
                source[-1] = value
                with self.assertRaises(TypeError):
                    decoder(source)
            for value in (-1, 4, 255):
                source = [0] * n
                source[-1] = value
                with self.assertRaises(ValueError):
                    decoder(source)
            for source in (None, 42, iter([0] * n), {0}):
                with self.assertRaises(TypeError):
                    decoder(source)
            with self.assertRaises(TypeError):
                decoder("0" * n)


if __name__ == "__main__":
    unittest.main()