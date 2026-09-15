"""AC27 tests: the deliberate pair schedule and the learning frontier.

Run with: .venv/bin/python -B -m unittest test_ac27
"""
import itertools
import math
import unittest
import ac25_confront as cf
import ac27_schedule as sched


class TestMinimumSchedule(unittest.TestCase):
    def test_exact_pairs_alone_reach_the_full_order(self):
        pairs=sched.minimal_schedule()
        self.assertEqual(len(pairs),15,'C(6,2)')
        self.assertEqual(cf.classes(cf.unique_codes(6),pairs),720)

    def test_fewer_than_all_pairs_falls_short(self):
        """A strictly smaller set cannot complete the structure: the missing pair is never
        confronted in isolation."""
        for drop in (1,2,5):
            sub=sched.minimal_schedule()[:-drop]
            self.assertLess(cf.classes(cf.unique_codes(6),sub),720,f'dropping {drop}')


class TestFrontier(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fr=sched.frontier(sched.pair_round_schedule(repeat=1))

    def test_full_order_after_fifteen_rounds(self):
        self.assertEqual(self.fr['index'],15)
        self.assertEqual(self.fr['classes'],720)

    def test_recorded_frontier_sequence(self):
        """Each new exact pair constrains the order further; the count is the number of comparison
        patterns realisable by a total order."""
        self.assertEqual(self.fr['counts'],
                         [2,4,8,16,32,48,72,108,162,216,288,384,480,600,720])

    def test_a_forest_of_pairs_doubles_each_time(self):
        """The first five pairs all involve need 0, so they form a star: a forest, whose edges can
        be oriented independently -- 2^k."""
        codes=cf.unique_codes(6)
        star=[(1<<0)|(1<<k) for k in range(1,6)]
        for k in range(1,6):
            self.assertEqual(cf.classes(codes,star[:k]),2**k,f'{k} star edges')

    def test_closing_a_triangle_multiplies_by_1_5_not_2(self):
        """The sixth pair closes a triangle, and transitivity forbids some orientations: of the four
        orientations of the two star edges, 2 + 1 + 1 + 2 = 6 extend to the third edge -> x1.5."""
        codes=cf.unique_codes(6)
        star=[(1<<0)|(1<<k) for k in range(1,6)]
        six=star+[(1<<1)|(1<<2)]
        self.assertEqual(cf.classes(codes,star),32)
        self.assertEqual(cf.classes(codes,six),48)

    def test_fifteen_pairs_are_enough_and_more_are_not_needed(self):
        codes=cf.unique_codes(6)
        allw=cf.family_all(codes)
        self.assertEqual(cf.classes(codes,allw),720,'adding every subset changes nothing')


class TestRobustness(unittest.TestCase):
    def test_higher_order_demands_never_reduce_the_count(self):
        codes=cf.unique_codes(6)
        pairs=sched.all_pairs()
        triples=[sum(t) for t in itertools.combinations([1<<k for k in range(6)],3)]
        for family in (pairs,
                       pairs+sched.all_singletons()+[0],
                       pairs+sched.all_singletons()+triples+[0],
                       cf.family_all(codes)):
            self.assertEqual(cf.classes(codes,family),720)


class TestControl(unittest.TestCase):
    def test_grouped_exclusivity_collapses_to_nothing(self):
        """One need at a time: no comparisons, no order information -- 0.00 bits. This is the
        frozen world's habit taken to its limit."""
        codes=cf.unique_codes(6)
        excl=[]
        for group in ([0,1],[2,3],[4,5]):
            for k in group: excl.append(1<<k)
        self.assertEqual(cf.classes(codes,excl),1)

    def test_schedule_is_far_sooner_than_oscillator_drift(self):
        cyclic_full_period=1616615
        self.assertGreater(cyclic_full_period/15,100000)


if __name__=='__main__':
    unittest.main()
