"""AC16 unit tests: the restore primitive, the re-acquisition mechanism, and the gates.

Run with: .venv/bin/python -B -m unittest test_ac16
"""
import json
import statistics
import unittest
from pathlib import Path
import numpy as np
import ac16, ac15, ac12, ac9, ac4
from ac1 import decode


def setUpModule():
    """Pin the module state these tests assert in.

    Without this the suite is order-dependent: an earlier test file that leaves
    `ac15.GRADE` at 0 or `ac12.REGISTER_THRESHOLD` at another value changes the world the
    AC16 arms run in, and a keeping arm that never bound a key during development is not
    barred by the deposit gate. The tests must control their environment rather than
    inherit it.
    """
    ac15.GRADE=1
    ac12.REGISTER_THRESHOLD=4
    ac12.DEV=ac16.DEV
    ac16.RESTORE=True


class TestRestorePrimitive(unittest.TestCase):
    """The two-way rule: symmetric with the drop, equally paid, same vulnerable bank."""

    def test_restore_disabled_reproduces_one_way_allocate_exactly(self):
        """The G5 control on the primitive itself: with the restore rule off, the two-way
        arm must be the one-way arm, state hash included."""
        ac16.RESTORE=False
        one=ac16.run(0,0,'allocate')
        two=ac16.run(0,0,'restore_disabled')
        ac16.RESTORE=True
        self.assertEqual(one['state_hash'],two['state_hash'])
        self.assertEqual(one['productivity_moved'],two['productivity_moved'])

    def test_restore_writes_the_same_bank_the_damage_stream_flips(self):
        """No protected copy: a restoration is a write into traces[0,:126]."""
        ac16.RESTORE=True
        r=ac16.run(0,0,'allocate_restore')
        self.assertGreater(r['restorations'],0,'the two-way arm restored nothing')
        self.assertTrue(r['route_correct_moved'])
        self.assertEqual(r['final_routes'][1],r['final_mapping'][1])

    def test_restore_is_paid_and_the_ledger_stays_consistent(self):
        """A restoration charges one energy and one material per replica, and the frozen
        conservation identity `spent_m == writes + 4*(W_birth+C_birth) + 2*B_birth` must
        still hold exactly with the restore booked."""
        r=ac16.run(0,0,'allocate_restore')
        led=r['ledger']
        self.assertGreater(led['writes'],0)
        self.assertEqual(led['spent_m'],
                         led['writes']+4*(led['W_birth']+led['C_birth'])+2*led['B_birth'])

    def test_arm_specific_constants_survive_the_defaults(self):
        """Regression: applying defaults after the arm overrides made `streak_never`
        run with the learner's threshold and score as the learner."""
        ac16.RESTORE=True
        for k,v in ac15.DEFAULTS.items(): setattr(ac12,k,v)
        never=ac16.run(0,0,'streak_never')
        preserve=ac16.run(0,0,'preserve')
        self.assertEqual(never['state_hash'],preserve['state_hash'],
                         'streak_never must be indistinguishable from preserve')


class TestReAcquisitionMechanism(unittest.TestCase):
    """Keeping cannot re-bind; one-way can bind but not hold; two-way holds."""

    def test_keeping_arms_are_barred_from_binding(self):
        """An arm that *holds* an entry for the moved key when the move happens cannot bind
        anything: the frozen deposit gate requires `selected is None`. The precondition is
        asserted rather than assumed — an arm that never bound that key during development
        has nothing for the gate to bar, and `stored_after_move_at == MOVE` is how the row
        records that it did hold one."""
        for arm in ('preserve','no_learning','fixed_schedule','random'):
            r=ac16.run(0,0,arm)
            self.assertEqual(r['stored_after_move_at'],ac16.MOVE,
                             f'{arm} held no entry for the moved key at the move')
            self.assertIsNone(r['reacquired_at'],
                              f'{arm} re-bound a route while holding an entry for that key')
            self.assertEqual(r['productivity_moved'] or 0.0,0.0,f'{arm} scored on the moved channel')

    def test_relinquishing_arms_do_bind(self):
        """Dropping the stale entry is what makes binding possible at all."""
        for arm in ('allocate','allocate_restore','relinquish'):
            r=ac16.run(0,0,arm)
            self.assertIsNotNone(r['reacquired_at'],f'{arm} never re-bound despite relinquishing')
            self.assertGreaterEqual(r['reacquired_at'],ac16.MOVE)

    def test_two_way_holds_what_one_way_cannot(self):
        one=ac16.run(0,0,'allocate'); two=ac16.run(0,0,'allocate_restore')
        self.assertGreater(two['productivity_moved'],one['productivity_moved'])
        self.assertEqual(two['productivity_moved'],1.0)

    def test_kept_channel_is_not_sacrificed(self):
        r=ac16.run(0,0,'allocate_restore')
        self.assertEqual(r['productivity_kept'],1.0)


class TestProtocolGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=Path('ac16_results_v1/results.json')
        if not p.exists(): raise unittest.SkipTest('final table not collected yet')
        cls.rows=json.loads(p.read_text())['rows']
        cls.by={}
        for r in cls.rows: cls.by.setdefault(r['arm'],[]).append(r)

    def mean(self, arm, key, default=0.0):
        vals=[(r[key] if r[key] is not None else default) for r in self.by[arm]]
        return statistics.mean(vals)

    def test_g1_learner_holds_a_correct_route(self):
        self.assertGreaterEqual(self.mean('allocate_restore','productivity_moved'),0.90)

    def test_g2_margin_recorded_as_failing_and_learner_dominates_every_individual(self):
        """G2 as declared (+0.25) FAILED: measured +0.2437, short by 0.006, so the claim as
        specified is falsified and the protocol was not amended. What survives is recorded
        here instead: the learner is strictly better than one-way on every individual, and
        the margin stays below the declared threshold. Any future change to the code that
        alters either fact invalidates `AC16_RESULTS_v1.md`.
        """
        margin=self.mean('allocate_restore','productivity_moved')-self.mean('allocate','productivity_moved')
        self.assertGreater(margin,0.0)
        self.assertLess(margin,0.25,'the recorded G2 failure no longer reproduces')
        pairs=[(r['productivity_moved'],b['productivity_moved'])
               for r in self.by['allocate_restore']
               for b in self.by['allocate']
               if (r['seed'],r['history'])==(b['seed'],b['history'])]
        self.assertEqual(len(pairs),8)
        self.assertTrue(all(a>b for a,b in pairs),'the learner must dominate one-way per individual')

    def test_g3_keeping_cannot_rebind(self):
        for arm in ('preserve','no_learning'):
            self.assertLessEqual(self.mean(arm,'productivity_moved'),0.05)
            self.assertTrue(all(r['reacquired_at'] is None for r in self.by[arm]))

    def test_g4_valid_route_not_sacrificed(self):
        self.assertGreaterEqual(self.mean('allocate_restore','productivity_kept'),0.95)

    def test_g5_consistency_arms_are_exact(self):
        def by_id(arm): return { (r['seed'],r['history']): r for r in self.by[arm] }
        pr, sn, fp = by_id('preserve'), by_id('streak_never'), by_id('fixed_period_1')
        al, rd = by_id('allocate'), by_id('restore_disabled')
        for k in pr:
            self.assertEqual(pr[k]['state_hash'],sn[k]['state_hash'])
            self.assertEqual(pr[k]['state_hash'],fp[k]['state_hash'])
            self.assertEqual(al[k]['state_hash'],rd[k]['state_hash'])

    def test_g6_recorded_scope_failure(self):
        """G6 as declared (every arm completes) FAILED: the crude always-relinquish arm dies
        in 4 of 8 individuals. G6 is not in the protocol's falsification list, so this is a
        scope note, not a falsification. Recorded: the learner and every arm it is compared
        against complete the horizon in all 8.
        """
        for arm in ('allocate_restore','allocate','preserve','no_learning','restore_disabled'):
            self.assertTrue(all(r['completed'] for r in self.by[arm]),f'{arm} failed to complete')
        dead=[a for a in ac16.ARMS if any(not r['completed'] for r in self.by[a])]
        self.assertEqual(dead,['relinquish'],'the recorded G6 failure no longer reproduces')

    def test_table_covers_every_arm_and_seed(self):
        self.assertEqual(len(self.rows),len(ac16.ARMS)*8)
        for arm in ac16.ARMS: self.assertEqual(len(self.by[arm]),8)


class TestDeclaredConstants(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(ac16.TICKS,4096)
        self.assertEqual(ac16.MOVE,1024)
        self.assertEqual(ac16.DEV,512)
        self.assertEqual(ac15.MOVE_ACTIONS,(1,),'the intervention must stay asymmetric')
        self.assertTrue(ac16.RESTORE)

    def test_protocol_is_hashed_with_the_run(self):
        h=json.loads(Path('ac16_results_v1/results.json').read_text())['hashes']
        self.assertIn('AC16_PROTOCOL_v1.md',h)
        self.assertIn('ac16.py',h)


if __name__=='__main__':
    unittest.main()
