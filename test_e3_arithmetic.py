"""Independent engineering fixtures for pure E3 integer arithmetic.

Fraction and fixed local Random fixtures are test oracles, not actual agents,
experimental targets, or production dependencies. The primitive counter below
checks independent mathematical instruction expressions, NOT execution traces
of production functions, VM registers, paid accesses, or micro-op conformance.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import operator
from random import Random
import unittest

from e3.arithmetic import (
    action_return,
    finalize_reward,
    select_action,
    task_return,
    td_update,
)


def reference_td(q, r, m, terminal=False):
    reward = sorted((-256, r, 256))[1]
    successor = 0 if terminal else m
    increment = round((Fraction(reward) + Fraction(15, 16) * successor - q) / 8)
    return sorted((-32768, q + increment, 32767))[1]


class PrimitiveCounter:
    """Independent expression counter; not a production or paid-VM trace."""

    OPERATIONS = {
        "lt": operator.lt, "gt": operator.gt, "eq": operator.eq,
        "add": operator.add, "sub": operator.sub, "shl": operator.lshift,
        "shr": operator.rshift, "and": operator.and_, "or": operator.or_,
        "select": lambda condition, yes, no: yes if condition else no,
        "mov": lambda value: value,
    }

    def __init__(self):
        self.count = 0

    def __call__(self, operation, *args):
        self.count += 1
        return self.OPERATIONS[operation](*args)


def independent_td_primitives(q, r, m):
    step = PrimitiveCounter()
    low = step("lt", r, -256)
    r = step("select", low, -256, r)
    high = step("gt", r, 256)
    r = step("select", high, 256, r)
    numerator = step("shl", r, 4)
    bootstrap = step("shl", m, 4)
    bootstrap = step("sub", bootstrap, m)
    numerator = step("add", numerator, bootstrap)
    old = step("shl", q, 4)
    numerator = step("sub", numerator, old)
    quotient = step("shr", numerator, 7)
    remainder = step("and", numerator, 127)
    above = step("gt", remainder, 64)
    tie = step("eq", remainder, 64)
    odd = step("and", quotient, 1)
    odd_tie = step("and", odd, tie)
    increment = step("or", above, odd_tie)
    quotient = step("add", quotient, increment)
    updated = step("add", q, quotient)
    low = step("lt", updated, -32768)
    updated = step("select", low, -32768, updated)
    high = step("gt", updated, 32767)
    updated = step("select", high, 32767, updated)
    return updated, step.count


def independent_selection_primitives(row, b, t, x):
    step = PrimitiveCounter()
    first = step("gt", row[0], row[1])
    maximum = step("select", first, row[0], row[1])
    last = step("gt", maximum, row[2])
    maximum = step("select", last, maximum, row[2])
    p0 = step("eq", row[0], maximum)
    p1 = step("eq", row[1], maximum)
    p2 = step("eq", row[2], maximum)
    count = step("add", p0, p1)
    count = step("add", count, p2)
    lowest = step("select", p1, 1, 2)
    lowest = step("select", p0, 0, lowest)
    highest = step("select", p1, 1, 0)
    highest = step("select", p2, 2, highest)
    ranked = step("select", b, highest, lowest)
    two = step("eq", count, 2)
    chosen = step("select", two, ranked, lowest)
    three = step("eq", count, 3)
    chosen = step("select", three, t, chosen)
    explore = step("eq", x, 0)
    chosen = step("select", explore, t, chosen)
    chosen = step("mov", chosen)
    return chosen, step.count


class TestE3Arithmetic(unittest.TestCase):
    def test_signed_ties_and_sign_extension_regression(self):
        for reward, expected in ((4, 0), (-4, 0), (12, 2), (-12, -2), (-1, 0)):
            self.assertEqual(td_update(0, reward, 0), expected)
        for reward in range(-256, 257):
            self.assertEqual(td_update(0, reward, 0), round(Fraction(reward, 8)))
        self.assertEqual(td_update(0, -32768, 0), -32)
        self.assertEqual(td_update(0, 32767, 0), 32)

    def test_small_q_reward_bin_cartesian_against_fraction(self):
        rewards = (-32768, -257, -256, -255, -12, -5, -4, -3, -1, 0,
                   1, 3, 4, 5, 12, 255, 256, 257, 32767)
        for q, r, m, terminal in product(range(-8, 9), rewards, range(-8, 9), (False, True)):
            self.assertEqual(td_update(q, r, m, terminal), reference_td(q, r, m, terminal))

    def test_boundary_words_clamps_terminal_and_numerator_extremes(self):
        words = (-32768, -32767, -4096, -257, -256, -1, 0, 1, 256, 257, 4096, 32766, 32767)
        for q, r, m, terminal in product(words, words, words, (False, True)):
            actual = td_update(q, r, m, terminal)
            self.assertEqual(actual, reference_td(q, r, m, terminal))
            self.assertGreaterEqual(actual, -32768)
            self.assertLessEqual(actual, 32767)
        self.assertEqual(16 * -256 + 15 * -32768 - 16 * 32767, -1019888)
        self.assertEqual(16 * 256 + 15 * 32767 - 16 * -32768, 1019889)
        self.assertEqual(16 * -256 - 16 * 32767, -528368)
        self.assertEqual(16 * 256 - 16 * -32768, 528384)
        self.assertEqual(td_update(32767, -32768, -32768), 24799)
        self.assertEqual(td_update(-32768, 32767, 32767), -24800)
        # At valid extrema the update points inward; saturation is defensive.
        self.assertEqual(td_update(32767, 32767, 32767), 32543)
        self.assertEqual(td_update(-32768, -32768, -32768), -32544)

    def test_every_remainder_and_half_threshold_with_both_signs(self):
        seen = set()
        for q, m in product((-32768, -1, 0, 1, 32767), range(-256, 257)):
            numerator = 15 * m - 16 * q
            seen.add(numerator % 128)
            self.assertEqual(td_update(q, 0, m), reference_td(q, 0, m))
        self.assertEqual(seen, set(range(128)))
        for r, m in product((-256, 0, 256), range(-128, 129)):
            self.assertEqual(td_update(7, r, m, True), reference_td(7, r, 0, True))

    def test_fixed_random_word_fixture_against_fraction(self):
        rng = Random(20260910)
        for _ in range(10000):
            q, r, m = (rng.randrange(-32768, 32768) for _ in range(3))
            terminal = bool(rng.randrange(2))
            self.assertEqual(td_update(q, r, m, terminal), reference_td(q, r, m, terminal))

    def test_independent_23_primitive_counter_is_not_production_trace(self):
        words = (-32768, -257, -256, -12, -4, -1, 0, 1, 4, 12, 256, 257, 32767)
        for q, r, m in product(words, repeat=3):
            result, count = independent_td_primitives(q, r, m)
            self.assertEqual(count, 23)
            self.assertEqual(result, reference_td(q, r, m))
            self.assertEqual(td_update(q, r, m), result)

    def test_all_accepted_yields_and_completed_prefixes(self):
        for n in (5, 20):
            for energy in range(65):
                self.assertEqual(action_return(0, accepted_energy=energy, n=n), energy // 4)
            for material in range(9):
                self.assertEqual(action_return(1, accepted_material=material, n=n), 2 * material)
            for writes in range(n + 1):
                self.assertEqual(action_return(2, completed_writes=writes, n=n), -writes)
            for action in (None, 0, 1, 2):
                self.assertEqual(action_return(action, n=n), 0)
        self.assertEqual(action_return(0, accepted_energy=63), 15)
        self.assertEqual(action_return(1, accepted_material=8), 16)

    def test_task_outcomes_and_missing_zero(self):
        for useful, correct in product(range(2), repeat=2):
            expected = (64 if correct else -64) if useful else 0
            self.assertEqual(task_return(useful, correct), expected)
        self.assertEqual(task_return(), 0)
        self.assertEqual(task_return(None, None), 0)
        # Missing, invalid, unaffordable and unplanned all have no outcome.
        for _ in ("missing", "invalid", "unaffordable", "unplanned", "no-feedback"):
            self.assertEqual(task_return(), 0)

    def test_objective_bounds_and_wide_finalization_before_clamp(self):
        prefixes = {action_return(0, accepted_energy=f) for f in range(65)}
        prefixes.update(action_return(1, accepted_material=p) for p in range(9))
        prefixes.update(action_return(2, completed_writes=w) for w in range(21))
        self.assertEqual(prefixes, set(range(-20, 17)))
        returns = set()
        for a, b in product(prefixes, (-64, 0, 64)):
            returns.add(finalize_reward(a, b))
            self.assertEqual(finalize_reward(a, b), a + b)
        self.assertEqual((min(returns), max(returns)), (-84, 80))
        for a, b in product(range(-32768, 32768), (-64, 0, 64)):
            self.assertEqual(finalize_reward(a, b), sorted((-256, a + b, 256))[1])
        self.assertEqual(finalize_reward(32767, 64), 256)
        self.assertEqual(finalize_reward(-32768, -64), -256)

    def test_every_maximal_subset_over_all_96_rank_inputs(self):
        for size in (1, 2, 3):
            for maxima in combinations(range(3), size):
                row = tuple(32767 if action in maxima else -32768 for action in range(3))
                all_counts = Counter()
                exploit_counts = Counter()
                explore_counts = Counter()
                for b, t, x in product(range(2), range(3), range(16)):
                    action = select_action(row, b, t, x)
                    all_counts[action] += 1
                    (explore_counts if x == 0 else exploit_counts)[action] += 1
                    expected = t if x == 0 or size == 3 else maxima[b if size == 2 else 0]
                    self.assertEqual(action, expected)
                self.assertEqual(sum(all_counts.values()), 96)
                self.assertEqual(sum(exploit_counts.values()), 90)
                self.assertEqual(explore_counts, {0: 2, 1: 2, 2: 2})
                for action in range(3):
                    expected = Fraction(1, 48)
                    if action in maxima:
                        expected += Fraction(15, 16 * size)
                        self.assertEqual(Fraction(exploit_counts[action], 90), Fraction(1, size))
                    else:
                        self.assertEqual(exploit_counts[action], 0)
                    self.assertEqual(Fraction(all_counts[action], 96), expected)

    def test_independent_selection_21_plus_padding_not_production_trace(self):
        for row in product((-1, 0, 1), repeat=3):
            for b, t, x in product(range(2), range(3), range(16)):
                result, count = independent_selection_primitives(row, b, t, x)
                self.assertEqual(count, 21)
                self.assertEqual(count + 3, 24)  # Declared unused slots, not hidden work.
                self.assertEqual(select_action(row, b, t, x), result)

    def test_selection_uses_current_row_without_mutation_or_cache(self):
        row = [0, 2, 0]
        self.assertEqual(select_action(row, 0, 0, 1), 1)
        self.assertEqual(row, [0, 2, 0])
        row[2] = 3
        self.assertEqual(select_action(row, 0, 0, 1), 2)
        self.assertEqual(row, [0, 2, 3])
        self.assertEqual(select_action((5, 0, 5), 0, 1, 1), 0)
        self.assertEqual(select_action((5, 0, 5), 1, 1, 1), 2)

    def test_td_validation_including_ignored_terminal_bootstrap(self):
        for index in range(3):
            for bad in (True, False, 1.0, "1", None):
                args = [0, 0, 0]
                args[index] = bad
                with self.assertRaises(TypeError):
                    td_update(*args, terminal=True)
            for bad in (-32769, 32768):
                args = [0, 0, 0]
                args[index] = bad
                with self.assertRaises(ValueError):
                    td_update(*args, terminal=True)
        for terminal in (0, 1, None, "False"):
            with self.assertRaises(TypeError):
                td_update(0, 0, 0, terminal)

    def test_action_validation_and_no_unselected_income(self):
        for action in (None, 0, 1, 2):
            for index, keyword in enumerate(("accepted_energy", "accepted_material", "completed_writes")):
                if index != action:
                    with self.assertRaises(ValueError):
                        action_return(action, **{keyword: 1})
        for action in (-1, 3):
            with self.assertRaises(ValueError):
                action_return(action)
        for action in (True, False, 1.0, "0"):
            with self.assertRaises(TypeError):
                action_return(action)
        for keyword in ("accepted_energy", "accepted_material", "completed_writes", "n"):
            for bad in (True, False, 0.0, "0", None):
                with self.assertRaises(TypeError):
                    action_return(2, **{keyword: bad})
        for kwargs in ({"accepted_energy": -1}, {"accepted_energy": 65},
                       {"accepted_material": -1}, {"accepted_material": 9},
                       {"completed_writes": -1}, {"completed_writes": 21},
                       {"completed_writes": 6, "n": 5}, {"n": 6}, {"n": 0}):
            with self.assertRaises(ValueError):
                action_return(2, **kwargs)

    def test_task_and_finalization_validation(self):
        for args in ((None, 0), (0, None), (-1, 1), (1, 2)):
            with self.assertRaises(ValueError):
                task_return(*args)
        for bad in (True, False, 1.0, "1"):
            with self.assertRaises(TypeError):
                task_return(bad, 1)
            with self.assertRaises(TypeError):
                task_return(1, bad)
        for index in (0, 1):
            for bad in (True, False, None, 1.0, "1"):
                args = [0, 0]
                args[index] = bad
                with self.assertRaises(TypeError):
                    finalize_reward(*args)
        for a, b in ((-32769, 0), (32768, 0), (0, -65), (0, 65), (0, 1), (0, -1)):
            with self.assertRaises(ValueError):
                finalize_reward(a, b)

    def test_selection_validation_even_for_unused_ranks(self):
        for row in ((), (0, 0), (0, 0, 0, 0)):
            with self.assertRaises(ValueError):
                select_action(row, 0, 0, 0)
        for row in (None, 1, iter((0, 0, 0))):
            with self.assertRaises(TypeError):
                select_action(row, 0, 0, 0)
        for bad in (True, False, 0.0, "0", None):
            with self.assertRaises(TypeError):
                select_action((0, 0, bad), 0, 0, 0)
            for index in range(3):
                ranks = [0, 0, 0]
                ranks[index] = bad
                with self.assertRaises(TypeError):
                    select_action((5, 0, 0), *ranks)
        for q in (-32769, 32768):
            with self.assertRaises(ValueError):
                select_action((q, 0, 0), 0, 0, 0)
        for ranks in ((-1, 0, 0), (2, 0, 0), (0, -1, 1), (0, 3, 1),
                      (0, 0, -1), (0, 0, 16)):
            with self.assertRaises(ValueError):
                select_action((5, 0, 0), *ranks)


if __name__ == "__main__":
    unittest.main()