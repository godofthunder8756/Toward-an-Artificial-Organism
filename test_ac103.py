"""Unit tests for AC103: persistent triggering distinguishes resource shortage from premature
termination of repair.

Pins the mechanism at the unit-test level: the arm identities (current/current_staged reproduce
the frozen AC102 arms byte-for-byte), the persistent trigger (inert on the marginal seed's
immediate schedule, load-bearing where cementing would stall the staged reconstruction), the
resource-shortage / premature-termination distinction, the state-dependent defer, and the
cementing counter. The recorded final outcomes are pinned as regressions.
"""
import unittest
import numpy as np
import ac103
import ac102
import ac95
import ac4
import ac5_program as prog


def setUpModule():
    # pin the module globals the study depends on (order-independence: an earlier test file
    # leaving ac12 globals changed must not alter the world AC103's arms run in).
    ac103.ac12.PORTS = 4
    ac103.ac12.YIELD_M = 64
    ac103.ac12.YIELD_F = 64
    ac103.ac12.POST_YIELD_M = None
    ac103.ac12.POST_YIELD_F = None
    ac103.ac12.MOVE_KEYS = (1,)
    ac103.ac12.MOVE = 10**9
    ac103.ac12.DEV = ac103.DEV
    ac103.ac12.REGISTER_THRESHOLD = 4


class TestArmIdentity(unittest.TestCase):
    def test_current_is_ac102_both(self):
        for seed in (0, 1, 2):
            self.assertEqual(ac103.run(seed, 0, 'current')['state_hash'],
                             ac102.run(seed, 0, 'both')['state_hash'],
                             f'current != AC102 both on seed {seed}')

    def test_current_staged_is_ac102_staged(self):
        for seed in (0, 1, 2):
            self.assertEqual(ac103.run(seed, 0, 'current_staged')['state_hash'],
                             ac102.run(seed, 0, 'staged')['state_hash'],
                             f'current_staged != AC102 staged on seed {seed}')

    def test_persistent_inert_on_marginal_immediate(self):
        # on the marginal seed, the immediate reconstruction already completes, so the persistent
        # trigger never fires where the current trigger would not: byte-identical.
        self.assertEqual(ac103.run(1, 0, 'persistent')['state_hash'],
                         ac103.run(1, 0, 'current')['state_hash'])

    def test_persistent_differs_where_cementing_delays(self):
        # on a cementing seed, the immediate reconstruction is delayed by action 2, so the
        # persistent trigger fires and recovers earlier: NOT byte-identical.
        self.assertNotEqual(ac103.run(2, 0, 'persistent')['state_hash'],
                            ac103.run(2, 0, 'current')['state_hash'])
        c = ac103.run(2, 0, 'current')
        p = ac103.run(2, 0, 'persistent')
        self.assertLess(p['recovery_tick'], c['recovery_tick'])


class TestPersistentTrigger(unittest.TestCase):
    def test_persistent_staged_closes_cementing_stall(self):
        # the cementing stall (fw>0 under staged) is closed by persistence.
        for seed in (2, 3, 4, 5, 7):
            cs = ac103.run(seed, 0, 'current_staged')
            ps = ac103.run(seed, 0, 'persistent_staged')
            self.assertGreater(cs['flipped_still_wrong'], 0, f'seed {seed} is not a cementing seed')
            self.assertEqual(ps['flipped_still_wrong'], 0,
                             f'persistent_staged did not recover seed {seed}')

    def test_program_incomplete_majority_level(self):
        # a sub-majority (1-3 replica) damage does NOT make the program "incomplete"; a 4/7
        # majority flip does.
        import ac12 as m
        _, _, _, priority = ac4.acquire(1)
        o, offs = m.acquire(1)
        reg_offs = ac95.resolve_offsets(o)
        streak_offs = ac103.ac96.streak_offsets(o)
        build_offs = reg_offs + streak_offs
        encoded = ac95.description_bits(priority)
        o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]   # install the description, as the runner does
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        self.assertFalse(ac103.program_incomplete(o, build_offs))
        # flip 1 replica of a program bit (sub-majority): still complete
        o.body.traces[0, 0, 0] ^= 1
        self.assertFalse(ac103.program_incomplete(o, build_offs))
        # flip to a 4/7 wrong majority on that bit: now incomplete
        w = 1 - int(acquired[0])
        o.body.traces[0, 0, 0:4] = w
        o.body.traces[0, 0, 4:7] = int(acquired[0])
        self.assertTrue(ac103.program_incomplete(o, build_offs))


class TestResourceShortage(unittest.TestCase):
    def test_marginal_dies_under_all_trigger_arms(self):
        # the marginal seed (mat <= 72) dies with fw == 0 under every non-defer arm: the
        # reconstruction completes but the shared material budget still kills it.
        for arm in ('current', 'current_staged', 'persistent', 'persistent_staged'):
            r = ac103.run(1, 0, arm)
            self.assertFalse(r['completed'], f'{arm} survived the marginal seed')
            self.assertEqual(r['flipped_still_wrong'], 0, f'{arm} did not recover')

    def test_defer_preserves_adaptation_resources(self):
        # the state-dependent defer survives the marginal seed with recovery intact.
        for seed in (1, 3):
            r = ac103.run(seed, 0, 'persistent_defer')
            self.assertTrue(r['completed'], f'defer died on seed {seed}')
            self.assertEqual(r['flipped_still_wrong'], 0)


class TestCementingCounter(unittest.TestCase):
    def test_action2_cementing_counted(self):
        # a body with one 4/7 majority-flipped bit: action 2 writes the 3 correct replicas to the
        # wrong value -- all 3 are "cementing".
        o, offs = ac103.ac12.acquire(1)
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        # flip bit 0 to a 4/7 wrong majority
        w = 1 - int(acquired[0])
        o.body.traces[0, 0, 0:4] = w
        o.body.traces[0, 0, 4:7] = int(acquired[0])
        counters = {'action2_writes': 0, 'action2_cementing': 0}
        react = ac103.make_react_counted(ac4.react, acquired, counters)
        e = ac4.empty_event()
        react(o.body, 2, 'self', e)   # action 2 = bank-0 majority restore
        self.assertGreater(counters['action2_writes'], 0)
        # the 3 correct replicas of bit 0 are written toward the wrong majority -> cementing
        self.assertEqual(counters['action2_cementing'], 3)


class TestDeferGating(unittest.TestCase):
    def test_defer_gated_to_corrupt_tick(self):
        # the defer arm is byte-identical to the persistent (immediate) arm before the corruption
        # tick, and diverges only after it.
        corrupt, schedule, budget, _ = ac103._arm_config('persistent')
        fn = ac103._maintain_fn(budget, True)
        _, _, pt = ac103._run_core(1, 0, corrupt, schedule, budget, True, fn, record_trace=True)
        corrupt, schedule, budget, _ = ac103._arm_config('persistent_defer')
        fn = ac103._maintain_fn(budget, True)
        _, _, dt = ac103._run_core(1, 0, corrupt, schedule, budget, True, fn, record_trace=True)
        first_div = None
        for (t1, d1), (t2, d2) in zip(pt, dt):
            if d1 != d2:
                first_div = t1
                break
        self.assertEqual(first_div, ac103.CORRUPT_TICK + 1,
                         f'defer diverged at {first_div}, expected {ac103.CORRUPT_TICK + 1}')


class TestConservation(unittest.TestCase):
    def test_balance_holds_in_step(self):
        # ac4.balance asserts hold in-step for every arm on a sample seed (no conservation drift
        # from the persistent trigger or the defer spend).
        for arm in ac103.ARMS:
            ac103.run(2, 0, arm)  # raises if a within-step balance assert fails


if __name__ == '__main__':
    unittest.main()
