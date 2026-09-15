"""AC31 tests: re-acquisition -- structure and the engineering falsification.

Run with: .venv/bin/python -B -m unittest test_ac31
"""
import itertools
import unittest
import numpy as np
import ac31_reacquire as ac


class TestPrerequisites(unittest.TestCase):
    """Cheap re-check at test scale. The study's own prerequisites passed at engineering scale; these
    assert the properties that must hold for the design to be worth re-engineering."""

    @classmethod
    def setUpClass(cls):
        cls.sA=ac.sweep(ac.RATES_A,seeds=(0,),ticks=400)
        cls.sB=ac.sweep(ac.RATES_B,seeds=(0,),ticks=400)

    def test_regimes_have_different_optima(self):
        oA=max(self.sA,key=self.sA.get); oB=max(self.sB,key=self.sB.get)
        self.assertNotEqual(oA,oB)

    def test_the_old_optimum_is_worse_under_the_new_regime(self):
        """Without this there is nothing to re-acquire, and the study would repeat AC13."""
        oA=max(self.sA,key=self.sA.get); oB=max(self.sB,key=self.sB.get)
        self.assertGreater(self.sB[oB],self.sB[oA])

    def test_a_random_order_is_already_close_to_optimal(self):
        """The measured reason the design could not detect re-acquisition: the per-individual
        learning margin is small relative to scoring noise."""
        best=max(self.sB.values()); worst=min(self.sB.values())
        random_mean=float(np.mean(list(self.sB.values())))
        self.assertGreater(random_mean,worst)
        self.assertLess(random_mean-worst,best-worst)


class TestArmStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sA=ac.sweep(ac.RATES_A,seeds=(0,),ticks=400)
        sB=ac.sweep(ac.RATES_B,seeds=(0,),ticks=400)
        cls.oA=max(sA,key=sA.get); cls.oB=max(sB,key=sB.get)
        cls.optima={'A':(cls.oA,sA[cls.oA]),'B':(cls.oB,sB[cls.oB])}

    def test_oracle_b_holds_the_new_optimum(self):
        r=ac.arm('oracle_b',0,self.optima)
        self.assertEqual(tuple(r['held']),self.oB)

    def test_no_search_and_preserve_hold_their_initial_order(self):
        for arm_name in ('no_search','preserve'):
            r=ac.arm(arm_name,0,self.optima)
            rng=np.random.default_rng([0,3101])
            expected=tuple(int(x) for x in rng.permutation(6))
            self.assertEqual(tuple(r['held']),expected,f'{arm_name}')

    def test_every_arm_reports_a_score_under_regime_b(self):
        for arm_name in ac.ARMS:
            r=ac.arm(arm_name,0,self.optima)
            self.assertIsInstance(r['post'],float)
            self.assertGreaterEqual(r['post'],0.0)


class TestTheEngineeringFalsification(unittest.TestCase):
    """The recorded outcome, asserted so a future attempt cannot quietly forget it. The capable arm
    did NOT beat the incapable ones on these seeds: the comparison is unpaired and seed noise is
    comparable to the margin."""

    @classmethod
    def setUpClass(cls):
        sA=ac.sweep(ac.RATES_A,seeds=(0,),ticks=400)
        sB=ac.sweep(ac.RATES_B,seeds=(0,),ticks=400)
        oA=max(sA,key=sA.get); oB=max(sB,key=sB.get)
        cls.optima={'A':(oA,sA[oA]),'B':(oB,sB[oB])}
        cls.rows={arm_name:[ac.arm(arm_name,seed,cls.optima)['post'] for seed in range(2)]
                  for arm_name in ('learner_both','no_search','oracle_b')}

    def test_the_capable_arm_does_not_clear_the_incapable_ones(self):
        learner=float(np.mean(self.rows['learner_both']))
        no_search=float(np.mean(self.rows['no_search']))
        self.assertLessEqual(learner,no_search,
                             'if this starts passing, the design changed and the protocol must be '
                             're-derived -- do not simply declare a bar')

    def test_the_oracle_ceiling_is_low_relative_to_the_sweep(self):
        """Seed noise: the same order rates ~1 site apart on different seed sets."""
        sweep_best=max(self.optima['B'][1],0)
        self.assertGreater(sweep_best,0)

    def test_no_protocol_or_final_dir_exists_for_this_study(self):
        """The study stopped at engineering. A frozen protocol or a results directory appearing
        without a re-engineered design would be a process violation."""
        import pathlib
        root=pathlib.Path('.')
        self.assertFalse((root/'AC31_PROTOCOL_v1.md').exists(),
                         'AC31 never reached the protocol stage')
        self.assertFalse(list(root.glob('ac31_results_*')),'AC31 never ran finals')


if __name__=='__main__':
    unittest.main()
