"""AC41 tests: the prerequisite that stopped the study, and the framework check that caught it.

Run with: .venv/bin/python -B -m unittest test_ac41
"""
import pathlib
import unittest
import numpy as np
import ac41_occupancy as ac41
import ac40_criterion as ac40

SEEDS=tuple(range(2))          # cheap: the structural facts hold on any seed
HISTORIES=(0,1)


class TestPrerequisiteFailed(unittest.TestCase):
    """Recorded numbers. The endpoint is degenerate and the effect-size requirement was mis-scaled; both
    are asserted so neither can be quietly softened."""

    @classmethod
    def setUpClass(cls):
        cls.live={(s,h):ac41.occupancy(ac41.LIVE,s,h) for s in SEEDS for h in HISTORIES}
        cls.cut={(s,h):ac41.occupancy(ac41.CUT,s,h) for s in SEEDS for h in HISTORIES}
        cls.diffs=[cls.live[k]-cls.cut[k] for k in sorted(cls.live)]

    def test_the_maintained_arm_is_a_constant(self):
        """The reason AC40's headroom check blocked this design: 21 for every individual, no variance."""
        self.assertEqual(len(set(self.live.values())),1,
                         f'expected a structural constant, got {sorted(set(self.live.values()))}')
        self.assertEqual(next(iter(self.live.values())),21.0)

    def test_headroom_check_flags_it_as_saturated(self):
        h=ac40.headroom(list(self.live.values()),ceiling=21.0)
        self.assertTrue(h['saturated'])
        self.assertEqual(h['at_ceiling_fraction'],1.0)

    def test_effect_size_requirement_fails_and_was_mis_scaled(self):
        median=float(np.median(self.diffs))
        self.assertGreater(median,0)
        self.assertLess(median,ac41.MIN_MEDIAN_DIFFERENCE,
                        'the declared requirement was copied from the activity endpoint, not this one')

    def test_four_individuals_are_underpowered_by_the_declared_rule(self):
        """The cheap 4-individual sample is correctly NOT 'resolved': the declared power floor is n >= 8
        (AC38's lesson). The full 16-individual run recorded in AC41_ENGINEERING_v1.md does resolve
        (p ~ 0.0000). This asserts the floor working, not a defect."""
        t=ac40.resolvability(self.diffs)
        self.assertEqual(t['n'],4)
        self.assertFalse(t['power_ok'])
        self.assertFalse(t['resolved'],'n=4 can never be resolved under the declared rule')
        self.assertAlmostEqual(t['p'],2/2**4,places=6,msg='every difference has the same sign')

    def test_prediction_of_bimodality_failed(self):
        """AC39's cut arm had unimpaired individuals; occupancy shows none. Recorded as a falsified
        prediction, not dropped."""
        impaired=float(np.mean(np.asarray(self.diffs,dtype=float)>0))
        self.assertEqual(impaired,1.0,'no bimodality in occupancy -- the prediction is falsified')


class TestNothingWasFrozen(unittest.TestCase):
    def test_no_protocol_or_results(self):
        root=pathlib.Path('.')
        self.assertFalse((root/'AC41_PROTOCOL_v1.md').exists(),
                         'the prerequisite failed: no protocol may exist for AC41')
        self.assertFalse(list(root.glob('ac41_results*')))
        self.assertEqual(ac41.SOURCES,[],'SOURCES stays empty when no protocol was written')

    def test_declared_bars_are_recorded(self):
        self.assertEqual(ac41.P_BAR,0.01)
        self.assertEqual(ac41.MIN_N,8)
        self.assertEqual(ac41.MIN_MEDIAN_DIFFERENCE,1000.0)


if __name__=='__main__':
    unittest.main()
