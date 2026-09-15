"""AC18 unit tests: the minima-separation gate and the structural claims, on fresh seeds.

Run with: .venv/bin/python -B -m unittest test_ac18
"""
import json
import unittest
from pathlib import Path
import ac18, ac17, ac16, ac15, ac12


def setUpModule():
    """Pin the module state these tests assert in, so the suite stays order-independent."""
    ac15.GRADE=1
    ac12.REGISTER_THRESHOLD=4
    ac12.DEV=ac18.ac17.DEV
    ac16.RESTORE=True


class TestGateShape(unittest.TestCase):
    """The gate is the claim's shape, and it must be able to pass and to fail."""

    def test_separation_of_minima_is_wellposed(self):
        """The bar sits below the ceiling, so strict separation of minima is satisfiable;
        if the bar were 1.0 the gate would be unsatisfiable by construction, which is the
        error AC17 made with per-individual strict dominance."""
        self.assertEqual(ac18.BAR,0.90)
        self.assertLess(ac18.BAR,1.0)
        self.assertGreater(ac18.BAR,0.0)

    def test_fresh_seeds_are_disjoint_from_every_earlier_family(self):
        used={2300,2301,2302,2303,2100,2101,2102,2103,1900,1901,1902,1903,
              1800,1801,1802,1803,1400,1401,1402,1403,1600,1601,1602,1603,
              0,1,2,3,4,5,6,7,8}
        self.assertFalse(used & set(ac18.SEEDS),'AC18 must not reuse a seed family')
        self.assertEqual(len(ac18.SEEDS),4)


class TestStructuralClaimsOnFreshSeeds(unittest.TestCase):
    """Claim A and the barred-keeping results must reproduce on the new seeds."""

    def test_restore_only_is_barred(self):
        for seed in (2500,2501):
            r=ac18.run(seed,0,'restore_only')
            self.assertEqual(r['productivity_moved'] or 0.0,0.0)
            self.assertIsNone(r['reacquired_at'])
            self.assertEqual(r['relinquishments'],0)

    def test_keeping_arms_are_barred(self):
        for arm in ('preserve','no_learning'):
            r=ac18.run(2500,0,arm)
            self.assertIsNone(r['reacquired_at'])
            self.assertEqual(r['productivity_moved'] or 0.0,0.0)

    def test_consistency_equalities(self):
        pr=ac18.run(2500,0,'preserve'); sn=ac18.run(2500,0,'streak_never')
        fp=ac18.run(2500,0,'fixed_period_1'); al=ac18.run(2500,0,'allocate')
        rd=ac18.run(2500,0,'restore_disabled')
        self.assertEqual(pr['state_hash'],sn['state_hash'])
        self.assertEqual(pr['state_hash'],fp['state_hash'])
        self.assertEqual(al['state_hash'],rd['state_hash'])


class TestProtocolGates(unittest.TestCase):
    BAR=0.90

    @classmethod
    def setUpClass(cls):
        p=Path('ac18_results_v1/results.json')
        if not p.exists(): raise unittest.SkipTest('final table not collected yet')
        cls.rows=json.loads(p.read_text())['rows']
        cls.by={}
        for r in cls.rows: cls.by.setdefault(r['arm'],[]).append(r)

    def worst(self, arm):
        return min((r['productivity_moved'] or 0.0) for r in self.by[arm])

    def test_g1_learner_worst_individual_clears_the_bar(self):
        self.assertGreaterEqual(self.worst('allocate_restore'),self.BAR)

    def test_g2_one_way_worst_individual_fails_to_hold(self):
        self.assertLess(self.worst('allocate'),self.BAR)

    def test_g3_keepers_exactly_zero_and_never_rebind(self):
        for arm in ('preserve','no_learning','fixed_schedule','random'):
            for r in self.by[arm]:
                self.assertEqual(r['productivity_moved'] or 0.0,0.0)
                self.assertIsNone(r['reacquired_at'])

    def test_g4_no_sacrifice(self):
        for r in self.by['allocate_restore']: self.assertGreaterEqual(r['productivity_kept'] or 0.0,0.95)

    def test_g5_consistency_exact(self):
        def by_id(a): return {(r['seed'],r['history']):r for r in self.by[a]}
        pr,sn,fp,al,rd=by_id('preserve'),by_id('streak_never'),by_id('fixed_period_1'),by_id('allocate'),by_id('restore_disabled')
        for k in pr:
            self.assertEqual(pr[k]['state_hash'],sn[k]['state_hash'])
            self.assertEqual(pr[k]['state_hash'],fp[k]['state_hash'])
            self.assertEqual(al[k]['state_hash'],rd[k]['state_hash'])

    def test_g6_claim_a_structural(self):
        for r in self.by['restore_only']:
            self.assertEqual(r['productivity_moved'] or 0.0,0.0)
            self.assertIsNone(r['reacquired_at'])

    def test_g7_no_blind_rival_reaches_the_bar(self):
        for arm in ('fixed_schedule','random'):
            for r in self.by[arm]: self.assertLess(r['productivity_moved'] or 0.0,self.BAR)

    def test_g8_declared_arms_complete(self):
        for arm in ('allocate_restore','allocate','preserve','no_learning','restore_only',
                    'fixed_period_1','streak_never','restore_disabled'):
            for r in self.by[arm]: self.assertTrue(r['completed'],f'{arm} died')

    def test_table_covers_every_arm_and_seed(self):
        self.assertEqual(len(self.rows),len(ac18.ARMS)*8)

    def test_frozen_sources_hashed_including_tools(self):
        h=json.loads(Path('ac18_results_v1/results.json').read_text())['hashes']
        for name in ('AC18_PROTOCOL_v1.md','ac18.py','test_ac18.py','audit_ac18.py','replay_ac18.py'):
            self.assertIn(name,h,f'{name} not in the frozen snapshot')


if __name__=='__main__':
    unittest.main()
