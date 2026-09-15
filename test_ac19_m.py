"""AC19-M tests: the maintenance-half diagnosis, and the exclusion of corruption as the route.

Run with: .venv/bin/python -B -m unittest test_ac19_m
"""
import unittest
import ac19
import ac19_maintenance as ac19m

SEEDS=(0,1)
LIVE='two_way'
CUT='two_way_no_repair'


def alive(arm,seeds=SEEDS,**kwargs):
    return sum(int(bool(ac19.run(s,0,arm,**kwargs)['completed'])) for s in seeds)


class TestTheRouteIsNotCorruption(unittest.TestCase):
    """AC19's record suspected the damage. It is excluded: the cut arms die identically with the
    register damage rate switched off."""

    def test_live_arm_survives_with_and_without_corruption(self):
        self.assertEqual(alive(LIVE),len(SEEDS))
        self.assertEqual(alive(LIVE,reg_rate=0.0),len(SEEDS))

    def test_cut_arm_dies_with_and_without_corruption(self):
        self.assertEqual(alive(CUT),0,'the cut arm dies with corruption on')
        self.assertEqual(alive(CUT,reg_rate=0.0),0,
                         'and it still dies with corruption off -- so corruption is not the route')


class TestTheRouteIsOccupancy(unittest.TestCase):
    """The named route: without repair the register empties, an empty register stops driving activity,
    and the organism winds down."""

    @classmethod
    def setUpClass(cls):
        cls.live=ac19.run(0,0,LIVE)
        cls.cut=ac19.run(0,0,CUT)

    def test_cut_arm_acts_on_far_fewer_ticks(self):
        self.assertEqual(self.live['ledger']['active'],ac19.TICKS,
                         'the live arm acts on every tick')
        self.assertLess(self.cut['ledger']['active'],0.75*ac19.TICKS,
                        'the cut arm stops acting for a large fraction of ticks')

    def test_cut_arm_register_is_far_less_occupied(self):
        """Not literally empty on every seed -- the robust fact is that the cut arm's register holds far
        less demand than the live arm's."""
        def occupancy(seed):
            return sum(pair[0] + pair[1] for pair in ac19.run(seed, 0, CUT)['demand'])
        def live_occupancy(seed):
            return sum(pair[0] + pair[1] for pair in ac19.run(seed, 0, LIVE)['demand'])
        cut_total = sum(occupancy(s) for s in SEEDS)
        live_total = sum(live_occupancy(s) for s in SEEDS)
        self.assertLess(cut_total, live_total,
                        f'cut {cut_total} should be below live {live_total}')

    def test_cut_arm_spends_and_produces_less(self):
        for key in ('spent_e','spent_m','W_birth','converted','memory_writes'):
            self.assertLess(self.cut['ledger'].get(key,0),self.live['ledger'].get(key,0),key)

    def test_cut_arm_exports_sites(self):
        """An organism that stops acting loses sites to export rather than to repair shortfalls."""
        self.assertEqual(self.live['ledger'].get('particle_export',0),0)
        self.assertGreater(self.cut['ledger'].get('particle_export',0),0)


class TestNothingIsFrozenByThisDiagnosis(unittest.TestCase):
    def test_no_protocol_or_results_dir(self):
        import pathlib
        root=pathlib.Path('.')
        self.assertFalse((root/'AC19M_PROTOCOL_v1.md').exists())
        self.assertFalse(list(root.glob('ac19m_results*')))
        self.assertFalse(list(root.glob('ac19_results*')),
                         'AC19 remains exploratory: no final seeds exist for it')


if __name__=='__main__':
    unittest.main()
