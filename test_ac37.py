"""AC37 tests: the self-funded economy that resolves orders, and the mechanism that makes it work.

Run with: .venv/bin/python -B -m unittest test_ac37
"""
import itertools
import pathlib
import unittest
import numpy as np
import ac37_selfsufficient as ac37


class TestTheChosenEconomy(unittest.TestCase):
    """Re-measured cheaply here: production period 4 / drain 3 is the selected self-funded economy."""

    @classmethod
    def setUpClass(cls):
        ac37.PRODUCTION_PERIOD, ac37.DRAIN = 4, 3
        sample = list(itertools.permutations(range(6)))[::20]      # 36 orders, cheap
        cls.scores = {o: ac37.rating(o, ac37.RATES_B, seeds=(0, 1), ticks=300) for o in sample}
        cls.spread = max(cls.scores.values()) - min(cls.scores.values())
        cls.mean = float(np.mean(list(cls.scores.values())))

    def test_spread_is_large(self):
        """AC35's world gave 1.00; this one gives ~11 at study scale."""
        self.assertGreater(self.spread, 3.0, f'spread {self.spread}')

    def test_population_is_in_the_graded_range_not_saturated(self):
        """Not pinned at carrying capacity (which is what erased AC35's differences) and not dying."""
        self.assertGreater(self.mean, 3.0)
        self.assertLess(self.mean, 24.0)

    def test_ratio_at_short_horizon_is_not_the_study_scale_story(self):
        """The scan's ratio of 22 came from 300 ticks and a small sample. It is recorded as a
        short-horizon finding only."""
        best = max(self.scores, key=self.scores.get)
        sd, _lo, _hi = ac37.noise_of_order(best, ac37.RATES_B, sets=4, ticks=300)
        self.assertGreater(sd, 0)
        self.assertGreater(self.spread / sd, 10.0, f'short-horizon ratio {self.spread/sd:.2f}')


class TestStudyScaleCriterionFails(unittest.TestCase):
    """The measurement that stopped the study. Asserted as recorded so it cannot be quietly relaxed:
    at the study's own scoring scale the endpoint does NOT meet the criterion this module declared."""

    @classmethod
    def setUpClass(cls):
        oA = (4, 5, 1, 2, 0, 3)          # regime A optimum, full 720 sweep on the paired seeds
        oB = (0, 4, 1, 3, 2, 5)          # regime B optimum
        cls.a_under_b = ac37.rating(oA, ac37.RATES_B)
        cls.b_rating = ac37.rating(oB, ac37.RATES_B)
        cls.margin = cls.b_rating - cls.a_under_b
        cls.sd = ac37.noise_of_order(oB, ac37.RATES_B, sets=4)[0]

    def test_margin_is_large(self):
        self.assertGreater(self.margin, 5.0)
        self.assertLess(self.a_under_b, 2.5, 'the old optimum is badly stuck under the new regime')

    def test_ratio_is_below_the_declared_criterion(self):
        ratio = self.margin / self.sd if self.sd else float('inf')
        self.assertGreater(self.sd, 0)
        self.assertLess(ratio, 10.0,
                        'if this ever passes the world changed; re-engineer before reusing the study')
        self.assertAlmostEqual(ratio, 7.16, delta=2.0, msg=f'ratio {ratio:.2f}')

    def test_no_protocol_and_no_finals(self):
        root = pathlib.Path('.')
        self.assertFalse((root / 'AC37_PROTOCOL_v1.md').exists(),
                         'the criterion failed: no protocol may exist for AC37')
        self.assertFalse(list(root.glob('ac37_results_*')),
                         'the criterion failed: no final seed may have been spent')
        self.assertEqual(ac37.SOURCES, [], 'SOURCES stays empty when no protocol was written')


class TestTheMechanism(unittest.TestCase):
    def test_the_drain_creates_the_graded_region(self):
        """Drain 1-2 leaves the population saturated (AC35's failure: spread 1.50); drain 3 opens a
        graded region (spread ~11). The spreads are compared rather than the means: at a short horizon
        both populations still fill the body, so the mean does not separate them yet."""
        def spread_at(drain, ticks=600):
            old = ac37.DRAIN; ac37.DRAIN = drain
            try:
                sample = list(itertools.permutations(range(6)))[::20]
                sc = [ac37.rating(o, ac37.RATES_B, seeds=(0,), ticks=ticks) for o in sample]
                return max(sc) - min(sc)
            finally:
                ac37.DRAIN = old
        saturated = spread_at(1)
        graded = spread_at(3)
        self.assertLess(saturated, 3.0, f'saturated world spread {saturated}')
        self.assertGreater(graded, saturated,
                           'the drain opens a graded region rather than a saturated one')
        self.assertGreater(graded, 3.0, f'graded spread {graded}')

    def test_death_when_the_population_floor_is_unreachable(self):
        """DRAIN * PRODUCTION_PERIOD above what the sites can produce means the organism cannot pay."""
        w = ac37.World(0)
        w.life[:] = [1] * len(w.life)                 # no productive sites at all
        for _ in range(200):
            w.tick(None)
        self.assertTrue(w.dead, 'a body that cannot cover its drain dies')

    def test_production_comes_from_the_organism_not_a_trickle(self):
        w = ac37.World(0)
        for _ in range(ac37.PRODUCTION_PERIOD * 3):
            w.tick(None)
        self.assertGreater(w.produced, 0)
        self.assertGreater(w.drained, 0)


class TestNotAFrozenStudyYet(unittest.TestCase):
    def test_no_protocol_or_results_exist(self):
        """Engineering only: the protocol and finals are the next step, with their own declared seeds."""
        root = pathlib.Path('.')
        self.assertFalse((root / 'AC37_PROTOCOL_v1.md').exists())
        self.assertFalse(list(root.glob('ac37_results_*')))
        self.assertEqual(ac37.SOURCES, [], 'SOURCES stays empty until a protocol declares one')


if __name__ == '__main__':
    unittest.main()
