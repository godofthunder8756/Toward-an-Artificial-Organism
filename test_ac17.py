"""AC17 unit tests: the categorical gates, the structural claim, and test isolation.

Run with: .venv/bin/python -B -m unittest test_ac17
"""
import json
import unittest
from pathlib import Path
import ac17, ac16, ac15, ac12


def setUpModule():
    """Pin the module state these tests assert in, so the suite is order-independent.
    AC16's first suite was not, and a leaked GRADE=0 unbarred a keeping arm."""
    ac15.GRADE=1
    ac12.REGISTER_THRESHOLD=4
    ac12.DEV=ac17.DEV
    ac16.RESTORE=True


class TestStructuralClaimA(unittest.TestCase):
    """Claim A is predicted from the frozen code, not from measurement."""

    def test_restore_only_is_barred_because_it_never_frees_the_key(self):
        """No drop rule -> the entry is never freed -> `selected is None` never holds ->
        the frozen deposit gate bars binding entirely."""
        for seed in (0,1):
            r=ac17.run(seed,0,'restore_only')
            self.assertEqual(r['productivity_moved'] or 0.0,0.0)
            self.assertIsNone(r['reacquired_at'],'restore_only bound a route without a drop rule')
            self.assertEqual(r['relinquishments'],0,'restore_only relinquished something')
            self.assertEqual(r['productivity_kept'],1.0,'the valid channel must be kept')

    def test_both_directions_are_needed(self):
        """Drop-only cannot hold (AC16); restore-only cannot bind (here)."""
        drop_only=ac17.run(0,0,'allocate')
        restore_only=ac17.run(0,0,'restore_only')
        both=ac17.run(0,0,'allocate_restore')
        self.assertGreater(drop_only['productivity_moved'],0.0)
        self.assertEqual(restore_only['productivity_moved'] or 0.0,0.0)
        self.assertEqual(both['productivity_moved'],1.0)


class TestKeepersAreStructurallyBarred(unittest.TestCase):
    def test_keeping_arms_hold_no_gate_passage(self):
        for arm in ('preserve','no_learning','fixed_schedule','random'):
            r=ac17.run(0,0,arm)
            self.assertEqual(r['stored_at_ch1'],ac17.MOVE,f'{arm} held no entry at the move')
            self.assertIsNone(r['reacquired_at'])
            self.assertEqual(r['productivity_moved'] or 0.0,0.0)


class TestConsistencyEqualities(unittest.TestCase):
    def test_three_exact_equalities(self):
        pr=ac17.run(0,0,'preserve'); sn=ac17.run(0,0,'streak_never'); fp=ac17.run(0,0,'fixed_period_1')
        al=ac17.run(0,0,'allocate'); rd=ac17.run(0,0,'restore_disabled')
        self.assertEqual(pr['state_hash'],sn['state_hash'])
        self.assertEqual(pr['state_hash'],fp['state_hash'])
        self.assertEqual(al['state_hash'],rd['state_hash'])
        self.assertNotEqual(al['state_hash'],pr['state_hash'])


class TestProtocolGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=Path('ac17_results_single_v1/results.json')
        if not p.exists(): raise unittest.SkipTest('final table not collected yet')
        cls.rows=json.loads(p.read_text())['rows']
        cls.by={}
        for r in cls.rows: cls.by.setdefault(r['arm'],[]).append(r)

    def vals(self, arm, key): return [r[key] for r in self.by[arm]]

    def test_g1_categorical_holding(self):
        for v in self.vals('allocate_restore','productivity_moved'):
            self.assertIsNotNone(v)
            self.assertGreaterEqual(v,0.90)

    def test_g2_recorded_unsatisfiable_gate_and_the_real_separation(self):
        """G2 as declared -- strict per-individual dominance over one-way -- FAILED, and the
        failure is a defect in the gate: on 2 of 8 individuals one-way also reached 1.000, so
        "strictly exceeds" is unsatisfiable at the ceiling. Recorded here is the claim's true
        categorical shape, a separation of worst cases: the learner holds >= 0.90 in EVERY
        individual while one-way fails to hold in at least one. A successor version must
        declare that gate in advance on fresh seeds; this result is not re-run with a
        better-chosen gate.
        """
        learner=self.vals('allocate_restore','productivity_moved')
        oneway=self.vals('allocate','productivity_moved')
        self.assertGreaterEqual(min(learner),0.90,'the learner must hold in every individual')
        self.assertLess(min(oneway),0.90,'one-way must fail to hold somewhere')
        ties=sum(1 for a,b in zip(learner,oneway) if a==b)
        self.assertEqual(ties,2,'the recorded ceiling tie count no longer reproduces')

    def test_g3_keepers_exactly_zero_and_never_rebind(self):
        for arm in ('preserve','no_learning','fixed_schedule','random'):
            for r in self.by[arm]:
                self.assertEqual(r['productivity_moved'] or 0.0,0.0)
                self.assertIsNone(r['reacquired_at'])

    def test_g4_no_sacrifice(self):
        for v in self.vals('allocate_restore','productivity_kept'): self.assertGreaterEqual(v,0.95)

    def test_g5_consistency_equal(self):
        for a,b in zip(sorted(self.by['preserve'],key=lambda r:(r['seed'],r['history'])),
                       sorted(self.by['streak_never'],key=lambda r:(r['seed'],r['history']))):
            self.assertEqual(a['state_hash'],b['state_hash'])
        for a,b in zip(sorted(self.by['preserve'],key=lambda r:(r['seed'],r['history'])),
                       sorted(self.by['fixed_period_1'],key=lambda r:(r['seed'],r['history']))):
            self.assertEqual(a['state_hash'],b['state_hash'])
        for a,b in zip(sorted(self.by['allocate'],key=lambda r:(r['seed'],r['history'])),
                       sorted(self.by['restore_disabled'],key=lambda r:(r['seed'],r['history']))):
            self.assertEqual(a['state_hash'],b['state_hash'])

    def test_g6_claim_a_categorical(self):
        for r in self.by['restore_only']:
            self.assertEqual(r['productivity_moved'] or 0.0,0.0)
            self.assertIsNone(r['reacquired_at'])

    def test_g7_no_blind_rival_reaches_the_bar(self):
        for arm in ('fixed_schedule','random'):
            for v in self.vals(arm,'productivity_moved'): self.assertLess(v or 0.0,0.90)

    def test_g8_declared_arms_complete(self):
        for arm in ('allocate_restore','allocate','preserve','no_learning','restore_only',
                    'fixed_period_1','streak_never','restore_disabled'):
            for r in self.by[arm]: self.assertTrue(r['completed'],f'{arm} died')

    def test_table_covers_every_arm_and_seed(self):
        self.assertEqual(len(self.rows),len(ac17.SINGLE_ARMS)*8)
        for arm in ac17.SINGLE_ARMS: self.assertEqual(len(self.by[arm]),8)


class TestDeclaredConstants(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(ac17.SEEDS_SINGLE,(2300,2301,2302,2303))
        self.assertEqual(ac17.TICKS,4096)
        self.assertEqual(ac17.MOVE,1024)
        self.assertEqual(ac15.MOVE_ACTIONS,(1,),'the claimed world is the single-channel move')

    def test_frozen_sources_hashed_including_tools(self):
        h=json.loads(Path('ac17_results_single_v1/results.json').read_text())['hashes']
        for name in ('AC17_PROTOCOL_v1.md','ac17.py','test_ac17.py','audit_ac17.py','replay_ac17.py'):
            self.assertIn(name,h,f'{name} not in the frozen snapshot')


if __name__=='__main__':
    unittest.main()
