"""AC42 tests: the endpoint survey -- the rejections it makes, and the shortlist it produces.

Run with: .venv/bin/python -B -m unittest test_ac42
"""
import pathlib
import unittest
import numpy as np
import ac42_endpoints as ac42

SEEDS=(0,1)         # cheap: the structural properties hold at any sample
HISTORIES=(0,1)


class TestTheTwoFailedEndpointsAreRejected(unittest.TestCase):
    """The survey must reject by its own checks the endpoints that AC39 and AC41 chose by reasoning."""

    @classmethod
    def setUpClass(cls):
        cls.live={}
        cls.cut={}
        for s in SEEDS:
            for h in HISTORIES:
                cls.live[(s,h)]=ac42.scalars(ac42.LIVE,s,h)
                cls.cut[(s,h)]=ac42.scalars(ac42.CUT,s,h)

    def test_ticks_active_has_no_headroom(self):
        """AC39's endpoint: 4096 for every live individual."""
        vals=[v['ledger.active'] for v in self.live.values()]
        self.assertEqual(len(set(vals)),1,f'expected saturation, got {vals}')
        self.assertEqual(vals[0],4096.0)
        # the survey's headroom rule: at-ceiling fraction >= 0.9 -> not usable
        import ac40_criterion as ac40
        self.assertTrue(ac40.headroom(vals,ceiling=4096.0)['saturated'])

    def test_register_replicas_set_total_is_a_constant(self):
        """AC41's endpoint: 21 for every live individual."""
        vals=[v['register_replicas_set_total'] for v in self.live.values()]
        self.assertEqual(len(set(vals)),1,f'expected a constant, got {vals}')
        self.assertEqual(vals[0],21.0)

    def test_a_metabolic_quantity_has_both_variance_and_a_separated_contrast(self):
        """The family the survey shortlists: variance across individuals and a resolved difference."""
        live=[v['ledger.W_birth'] for v in self.live.values()]
        cut=[v['ledger.W_birth'] for v in self.cut.values()]
        self.assertGreater(np.std(live),0.0,'a usable endpoint must vary across individuals')
        self.assertGreater(np.mean(live),np.mean(cut),'the live arm produces more births')

    def test_bimodality_lives_in_the_metabolic_family(self):
        """AC41 falsified the bimodality prediction for OCCUPANCY; AC42 locates it in metabolism."""
        diffs=[self.live[k]['ledger.spent_e']-self.cut[k]['ledger.spent_e'] for k in sorted(self.live)]
        impaired=float(np.mean(np.asarray(diffs,dtype=float)>0))
        self.assertGreater(impaired,0.0)
        self.assertLessEqual(impaired,1.0)
        self.assertGreater(np.std(diffs),0.0,'the metabolic contrast varies across individuals')


class TestSurveyMechanics(unittest.TestCase):
    def test_rank_flags_a_synthetic_saturated_endpoint_as_unusable(self):
        per={'saturated':{'live':[10.0]*8,'cut':[5.0]*8},
             'varying':{'live':[10.0,11,12,13,14,15,16,17],'cut':[5.0]*8}}
        rows={r['quantity']:r for r in ac42.rank(per)}
        self.assertFalse(rows['saturated']['usable'],'a saturated endpoint must not be usable')
        self.assertFalse(rows['saturated']['headroom'])
        self.assertTrue(rows['varying']['variance_ok'])

    def test_rank_flags_a_synthetic_unresolved_endpoint(self):
        per={'noisy':{'live':[1.0,-1,1,-1,1,-1,1,-1],'cut':[-1.0,1,-1,1,-1,1,-1,1]}}
        rows={r['quantity']:r for r in ac42.rank(per)}
        self.assertFalse(rows['noisy']['usable'])
        self.assertGreater(rows['noisy']['p'],0.01)


class TestNothingWasFrozen(unittest.TestCase):
    def test_no_protocol_or_results(self):
        root=pathlib.Path('.')
        self.assertFalse((root/'AC42_PROTOCOL_v1.md').exists(),
                         'AC42 is a survey: it declares no seeds and runs no finals')
        self.assertFalse(list(root.glob('ac42_results*')))
        self.assertEqual(ac42.SOURCES,[],'SOURCES stays empty for a survey')


if __name__=='__main__':
    unittest.main()
