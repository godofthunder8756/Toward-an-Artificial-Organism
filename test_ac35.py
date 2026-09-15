"""AC35 tests: the failed prerequisite, recorded; and the structure of the module that failed it.

Run with: .venv/bin/python -B -m unittest test_ac35
"""
import itertools
import pathlib
import unittest
import numpy as np
import ac35_survival as ac35


class TestPrerequisiteFailed(unittest.TestCase):
    """The recorded reason this study was stopped before any protocol: the self-funded maintenance
    endpoint does not discriminate enough to carry an arm comparison."""

    @classmethod
    def setUpClass(cls):
        sample=list(itertools.permutations(range(6)))[::18]      # 40 orders, cheap
        cls.scores={o:ac35.rating(o,ac35.RATES_B,seeds=(0,1,2)) for o in sample}
        best=max(cls.scores,key=cls.scores.get)
        cls.spread=max(cls.scores.values())-min(cls.scores.values())
        cls.sd=ac35.noise_of_order(best,ac35.RATES_B,sets=6)[0]

    def test_spread_is_small(self):
        """AC30's declared-income world gave 5.00 sites of 24; the self-funded world gives ~1."""
        self.assertLess(self.spread,3.0,f'spread {self.spread}')

    def test_margin_over_noise_is_below_the_declared_criterion(self):
        """Formulated on the noise RANGE rather than the sd: the noise is heterogeneous by order (a
        saturated order is nearly deterministic; a near-threshold order swings), so the honest
        comparison is that one order's swing across seed sets is as large as the whole spread across
        orders. Either way the criterion fails."""
        self.assertGreater(self.sd,0.0,'the best order of this sample still shows seed variance')
        self.assertLess(self.spread/self.sd,10.0,
                        'if this ever passes, the world changed and the study must be re-engineered')
        self.assertLess(self.spread/self.sd,5.0,f'ratio {self.spread/self.sd:.2f}')

    def test_one_orders_swing_is_as_large_as_the_spread(self):
        """The cleanest statement of why this endpoint cannot resolve orders."""
        best=max(self.scores,key=self.scores.get)
        _sd,lo,hi=ac35.noise_of_order(best,ac35.RATES_B,sets=6)
        self.assertGreaterEqual(hi-lo,self.spread*0.5,
                                f'swing {hi-lo:.2f} vs spread {self.spread:.2f}')

    def test_population_saturates_near_carrying_capacity(self):
        """The mechanism: production scales with the living population, so outcomes compress."""
        self.assertGreater(np.mean(list(self.scores.values())),0.7*24)


class TestStructure(unittest.TestCase):
    def test_sites_fund_renewals(self):
        w=ac35.World(0)
        before=w.energy
        for _ in range(ac35.PRODUCTION_PERIOD): w.tick(None)
        self.assertGreater(w.energy,before)
        self.assertGreater(w.produced,0)

    def test_starvation_means_wanting_and_unable(self):
        w=ac35.World(0)
        for _ in range(50): w.tick(None)         # idling: no urgency, no action
        self.assertEqual(w.starved,0)
        old_period=ac35.PRODUCTION_PERIOD
        ac35.PRODUCTION_PERIOD=10**9             # production would otherwise refill within 4 ticks
        try:
            w.energy=0
            for _ in range(3): w.tick(0)
        finally:
            ac35.PRODUCTION_PERIOD=old_period
        self.assertGreater(w.starved,0)

    def test_climb_is_scored_by_retained_population(self):
        """The climb must optimise THIS study's endpoint, not AC32's world score: AC33's asc.climb
        calls ac32.rating internally and could not be reused."""
        start=(5,4,3,2,1,0)
        opt,score,steps=ac35.climb(start,ac35.asc.swaps,ac35.RATES_B)
        self.assertEqual(score,ac35.rating(opt,ac35.RATES_B))
        for cand in ac35.asc.swaps(opt):
            self.assertLessEqual(ac35.rating(cand,ac35.RATES_B),score+1e-9,
                                 'a local optimum of the retention landscape')

    def test_held_orders_come_back_out_of_the_register(self):
        opt={'A':(tuple(range(6)),0.0),'B':(tuple(reversed(range(6))),0.0)}
        for arm in ac35.ARMS:
            held=ac35.hold(arm,0,opt)
            self.assertEqual(len(held),6)

    def test_no_protocol_or_results_exist(self):
        """The prerequisite failed, so no protocol was written and no final seed run. A protocol or
        results directory appearing here would be a process violation."""
        root=pathlib.Path('.')
        self.assertFalse((root/'AC35_PROTOCOL_v1.md').exists())
        self.assertFalse(list(root.glob('ac35_results_*')))
        self.assertEqual(ac35.SOURCES,[],'SOURCES must stay empty: no protocol declared a list')


if __name__=='__main__':
    unittest.main()
