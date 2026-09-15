"""AC34 tests: the survival endpoint engineering -- structure, and the recorded design finding.

Run with: .venv/bin/python -B -m unittest test_ac34
"""
import itertools
import unittest
import numpy as np
import ac30_acquire as acq
import ac34_survival as ac34


class TestIdlingIsNotStarving(unittest.TestCase):
    """My first version counted ticks with nothing urgent to do as starvation, so deaths clustered at
    exactly the threshold. Starvation must mean WANTING to act and being unable to afford it."""

    def test_idling_does_not_touch_the_starvation_counter(self):
        """Idling costs SITES (they expire) but must never read as starvation. My first test asserted
        the organism survives idling, which is wrong: an organism that never renews does die here, of
        site loss, and that is correct behaviour."""
        w=ac34.World(0)
        for _ in range(200):
            w.tick(None)
        self.assertEqual(w.starved,0,'idling must not count as starvation')
        self.assertLess(sum(1 for v in w.life if v>0),ac34.acq.SLOTS,'...but idling still costs sites')

    def test_wanting_to_act_without_energy_starves(self):
        w=ac34.World(0)
        old_period=ac34.PRODUCTION_PERIOD
        ac34.PRODUCTION_PERIOD=10**9              # no production: nothing can refill energy
        try:
            w.energy=0
            for _ in range(ac34.STARVATION_TICKS): w.tick(0)
        finally:
            ac34.PRODUCTION_PERIOD=old_period
        self.assertTrue(w.dead)
        self.assertEqual(w.dead_at,ac34.STARVATION_TICKS)

    def test_acting_resets_the_starvation_counter(self):
        w=ac34.World(0)
        w.energy=0
        for _ in range(5): w.tick(0)          # wants to act, cannot afford it
        self.assertGreater(w.starved,0,'wanting to act without energy must accumulate')
        w.energy=ac34.RENEW_ENERGY*2
        w.tick(0)                              # now it can afford the renewal
        self.assertEqual(w.starved,0,'a successful renewal resets the counter')


class TestProductionFunding(unittest.TestCase):
    def test_sites_produce_energy(self):
        w=ac34.World(0)
        before=w.energy
        for _ in range(ac34.PRODUCTION_PERIOD): w.tick(None)
        self.assertGreater(w.energy,before,'living sites must fund the organism')
        self.assertGreater(w.produced,0)

    def test_losing_sites_reduces_production(self):
        w=ac34.World(0)
        w.life[:]=[ac34.acq.URGENT-1]*len(w.life)   # nothing productive
        produced_before=w.produced
        for _ in range(ac34.PRODUCTION_PERIOD): w.tick(None)
        self.assertLessEqual(w.produced-produced_before,
                             sum(1 for v in w.life if v>=ac34.ENERGY_PER_SITE))

    def test_no_sites_means_death(self):
        w=ac34.World(0)
        w.life[:]=[0]*len(w.life)
        w.tick(None)
        self.assertTrue(w.dead,'a body with no sites is dead')


class TestTheRecordedDesignFinding(unittest.TestCase):
    """The binary alive/dead endpoint is UNSTABLE in this world rather than cleanly bistable: my scan
    grid found only 0.00 and 1.00, but a finer look found an intermediate 0.40 -- and the SAME
    configuration gives 0.00 at 800 ticks and 0.40 at 400. An endpoint that flips with the run horizon
    and the sampled orders is not a sound thing to build a claim on. Asserted as recorded, since it is
    the reason the survival study must use graded retention instead."""

    def _survive_fraction(self,renew,period,ticks,orders=None):
        old_renew,old_period=ac34.RENEW_ENERGY,ac34.PRODUCTION_PERIOD
        ac34.RENEW_ENERGY,ac34.PRODUCTION_PERIOD=renew,period
        try:
            orders=orders or list(itertools.permutations(range(6)))[::12]
            alive=[not ac34.run(o,0,ticks=ticks)['dead'] for o in orders]
            return float(np.mean(alive))
        finally:
            ac34.RENEW_ENERGY,ac34.PRODUCTION_PERIOD=old_renew,old_period

    def test_the_coarse_scan_grid_is_all_or_nothing(self):
        """The 12-configuration scan found only extremes -- which is what made the endpoint look
        clean, and why a coarse grid is not evidence of bistability."""
        for renew,period in ((5,4),(5,16),(10,8),(20,4),(40,16)):
            frac=self._survive_fraction(renew,period,800)
            self.assertIn(frac,(0.0,1.0),f'renew {renew}, period {period} gave {frac}')

    def test_the_same_configuration_flips_with_the_horizon(self):
        """The recorded instability: intermediate outcomes exist, and they are horizon-dependent."""
        short=self._survive_fraction(5,16,400)
        long=self._survive_fraction(5,16,800)
        self.assertNotAlmostEqual(short,long,places=2,
                                  msg='the horizon-flip that makes this endpoint unusable')

    def test_the_endpoint_that_would_be_usable_is_graded(self):
        """Retained population is graded where alive/dead flips: at renewal 5 / period 4 the sampled
        orders end with 17, 18 or 19 sites out of 24 -- the AC30 spread surviving into this
        production-funded world."""
        old_renew,old_period=ac34.RENEW_ENERGY,ac34.PRODUCTION_PERIOD
        ac34.RENEW_ENERGY,ac34.PRODUCTION_PERIOD=5,4
        try:
            orders=list(itertools.permutations(range(6)))[::24]
            sites={ac34.run(o,0,ticks=600)['sites'] for o in orders}
            self.assertGreater(len(sites),1,
                               'retained population should be graded, not all-or-nothing')
            self.assertTrue(all(15<=s<=24 for s in sites),f'unexpected spread {sorted(sites)}')
        finally:
            ac34.RENEW_ENERGY,ac34.PRODUCTION_PERIOD=old_renew,old_period

    def test_no_protocol_or_frozen_run_exists_for_this_study(self):
        """AC34 is engineering. A protocol or a results directory appearing here would be a process
        violation: the endpoint it was testing was rejected."""
        import pathlib
        root=pathlib.Path('.')
        self.assertFalse((root/'AC34_PROTOCOL_v1.md').exists())
        self.assertFalse(list(root.glob('ac34_results_*')))


if __name__=='__main__':
    unittest.main()
