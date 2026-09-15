"""AC30 tests: acquisition in the six-region world.

Run with: .venv/bin/python -B -m unittest test_ac30
"""
import itertools
import math
import unittest
import numpy as np
import ac30_acquire as acq
import ac29_register as reg
import ac27_schedule as sched

# One cached sweep at test scale (the recorded study used 2 seeds x 800 ticks; 1 x 600 is enough for
# the ordering to be stable and keeps the suite fast).
TEST_TICKS=600
_SWEEP=None


def sweep():
    global _SWEEP
    if _SWEEP is None:
        _SWEEP={o:acq.score(o,seeds=(0,),ticks=TEST_TICKS) for o in itertools.permutations(range(6))}
    return _SWEEP


def best_of():
    return max(sweep().values())


class TestTheWorldIsNotDegenerate(unittest.TestCase):
    def test_every_region_keeps_sites(self):
        """My first version of this world retained ZERO sites for every one of the 720 orders,
        because its only action filled empty slots -- so an urgent site could never be saved and
        every region collapsed. A world that scores everything zero ranks nothing."""
        for order in (tuple(range(6)),tuple(reversed(range(6))),(2,0,4,1,5,3)):
            retained,_=acq.run(order,0)
            self.assertGreater(retained,0,f'{order} retained nothing')

    def test_renewal_targets_a_live_site_in_the_chosen_region(self):
        w=acq.World(0)
        w.life[0:4]=[5,30,0,20]                 # region 0: the most urgent LIVE site is index 0
        w.tick(0)
        self.assertGreater(w.life[0],5,'the most urgent live site was renewed')
        self.assertEqual(w.renewed,1)

    def test_a_region_with_no_live_site_gets_nothing(self):
        w=acq.World(0)
        w.life[0:4]=[0,0,0,0]
        w.tick(0)
        self.assertEqual(w.renewed,0)


class TestTheWorldRanksOrders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scores=sweep()
        cls.ranked=sorted(cls.scores.items(),key=lambda kv:-kv[1])

    def test_spread_is_material(self):
        """Measured 5.00 sites of 24 at study scale. Contention is what makes a priority order
        consequential; an earlier design where income exceeded renewal cost ranked almost nothing
        (spread 1.5), so this is the prerequisite for any acquisition claim."""
        spread=self.ranked[0][1]-self.ranked[-1][1]
        self.assertGreaterEqual(spread,2.0,f'spread {spread}')

    def test_the_stress_order_is_not_the_best(self):
        """Falsified hypothesis, kept as a regression guard. URGENT is the same for every region, so
        the deadline is region-independent and the urgency signal does not encode how close to loss a
        site is; the best fixed order is a heuristic over correlated stress phases, discoverable only
        by evaluation."""
        rates=acq.stress_rates()
        stress_order=tuple(sorted(range(6),key=lambda k:-rates[k]))
        rank=1+sum(1 for _,v in self.ranked if v>self.scores[stress_order])
        self.assertGreater(rank,10,'stress order unexpectedly optimal')

    def test_ranking_is_a_strict_order_not_a_tie(self):
        self.assertGreater(self.ranked[0][1],self.ranked[-1][1])


class TestAcquisition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scores=sweep(); cls.best=best_of()
        cls.found=[]
        for seed in range(6):
            rng=np.random.default_rng([seed,3101])
            current=tuple(int(x) for x in rng.permutation(6))
            best=acq.score(current,seeds=(seed,),ticks=TEST_TICKS)
            for _ in range(60):
                i,j=rng.integers(0,6,2)
                cand=list(current); cand[i],cand[j]=cand[j],cand[i]; cand=tuple(cand)
                s=acq.score(cand,seeds=(seed,),ticks=TEST_TICKS)
                if s>=best: current,best=cand,s
            cls.found.append(current)

    def test_learners_land_well_up_the_distribution(self):
        """Measured at study scale: mean gap 1.83 sites against a 5.00 spread, one learner within
        0.50 of the best. Acquisition here is real but noisy."""
        gaps=[self.best-self.scores[o] for o in self.found]
        spread=self.best-min(self.scores.values())
        self.assertLessEqual(float(np.mean(gaps)),spread*0.7,f'mean gap {np.mean(gaps)} of {spread}')

    def test_learners_beat_the_stress_order_on_average(self):
        rates=acq.stress_rates()
        stress=tuple(sorted(range(6),key=lambda k:-rates[k]))
        learned=np.mean([self.scores[o] for o in self.found])
        self.assertGreaterEqual(learned,self.scores[stress])


class TestRetentionAndTheReferenceQuestion(unittest.TestCase):
    """AC30 corrects AC29 §4: 'mode-majority repair cannot hold a multi-bit object' was too strong.
    It holds it perfectly when the repair budget keeps pace with the broken-bit rate; an external
    reference is needed only when it cannot."""

    def setUp(self):
        self.target=(3,4,1,5,0,2); self.code=reg.lehmer(self.target)

    def _run(self,repair_budget,reference=False,ticks=400,damage=1e-3,seed=7):
        rng=np.random.default_rng(seed)
        r=reg.Register(); r.write(self.code)
        intact=agree=0
        for _ in range(ticks):
            r.damage(rng,damage)
            if reference:
                if r.read()!=self.target: r.write(self.code)
            elif repair_budget: r.repair(repair_budget)
            intact+= (r.raw()==self.code)
            agree+= reg.behavioural_agreement(r.read(),self.target,sched.all_pairs())
        return intact/ticks, agree/ticks

    def test_no_repair_degrades_under_real_damage(self):
        """At 1e-3 over a few hundred ticks the store often survives untouched -- so the test uses
        damage high enough that degradation is certain, rather than a threshold that depends on the
        seed."""
        intact,_=self._run(0,ticks=400,damage=0.01)
        self.assertLess(intact,1.0)

    def test_one_bit_repaired_per_tick_holds_it_perfectly(self):
        intact,agree=self._run(1)
        self.assertEqual(intact,1.0)
        self.assertEqual(agree,1.0)

    def test_an_external_reference_buys_nothing_at_this_budget(self):
        """The correction to AC29 §4: at a budget that keeps pace, protection is redundant."""
        self.assertEqual(self._run(1),self._run(1,reference=True))

    def test_more_repair_never_hurts_and_protection_always_works(self):
        """At heavy damage the ordering by outcome is: no repair <= tight repair <= full repair
        <= protection. This is what AC29 §4 should have said: a reference is needed when the budget
        cannot keep pace, not because majority repair is impossible in principle."""
        none_=self._run(0,ticks=400,damage=0.05)[0]
        tight=self._run(1,ticks=400,damage=0.05)[0]
        full=self._run(reg.BITS,ticks=400,damage=0.05)[0]
        protected=self._run(0,ticks=400,damage=0.05,reference=True)[0]
        self.assertLessEqual(none_,tight)
        self.assertLessEqual(tight,full)
        self.assertLessEqual(full,protected)
        self.assertEqual(protected,1.0,'protection always holds the store')


if __name__=='__main__':
    unittest.main()
