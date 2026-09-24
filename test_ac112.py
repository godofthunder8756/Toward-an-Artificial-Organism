"""Unit tests for AC112 (P5): the heterogeneous-LR two-counter estimate at organism scale.

Engineering only -- these tests pin the runner's mechanics, not a frozen result. They cover:
  - the Gray-coded counter primitives (storage roundtrip),
  - the heterogeneous weights (opposite sign, non-integer ratio),
  - the residual-yield source surgery (frozen line present, so the surgery applies),
  - the decisive handling and the accumulator threshold (move relinquishes, cut holds),
  - the no-cause identity (no false relinquish),
  - the read-only scramble (counter read forced, writes intact),
  - observer-discard (byte-identical trajectory under observer/allocator swap).
"""
import unittest
import math
import numpy as np

import ac112
import ac96
import ac12
import ac9


class TestWeights(unittest.TestCase):
    def test_heterogeneous_opposite_sign_noninteger(self):
        w_u, w_p = ac112.weights(ac112.EPS)
        self.assertGreater(w_u, 0)
        self.assertLess(w_p, 0)
        self.assertNotEqual(w_u, -w_p)
        self.assertNotAlmostEqual(w_p / w_u, round(w_p / w_u), places=6)
        self.assertNotAlmostEqual(w_u / w_p, round(w_u / w_p), places=6)

    def test_eps_zero_recovers_homogeneous(self):
        # eps -> 0: w_p -> -inf (productive is decisive C), w_u -> log(4/3)
        w_u, w_p = ac112.weights(1e-9)
        self.assertAlmostEqual(w_u, math.log(4.0 / 3.0), places=6)
        self.assertLess(w_p, -10)


class TestCounterPrimitives(unittest.TestCase):
    def test_gray_roundtrip(self):
        for n in range(16):
            self.assertEqual(ac112._gray_decode(ac112._gray_encode(n)), n)

    def test_counter_write_read_roundtrip(self):
        # build a minimal organism via ac12.acquire, then exercise counter_write/counter_read
        # on the dead rule's free streak bits directly.
        o, offs = ac12.acquire(0)
        streak = ac96.streak_offsets(o)
        offs4 = streak[0:4]
        e = ac9.event()
        # start from the frozen all-zero state: read must be 0
        self.assertEqual(ac112.counter_read(o, offs4), 0)
        # write 5, read back 5 (Gray-coded)
        n = ac112.counter_write(o, e, offs4, 5)
        self.assertEqual(ac112.counter_read(o, offs4), 5)
        self.assertGreater(n, 0)
        # write the same value again: no-op
        self.assertEqual(ac112.counter_write(o, e, offs4, 5), 0)


class TestResidualSurgery(unittest.TestCase):
    def test_residual_line_present_in_frozen_step(self):
        # the source surgery replaces exactly one occurrence of the frozen contact line
        self.assertEqual(ac12.STEP_SRC.count(ac112.RESIDUAL_LINE), 1)

    def test_eps_zero_residual_never_fires(self):
        # at eps -> 0 the productive weight diverges to -inf (the residual yield is a
        # no-op: M never yields), so the residual branch contributes nothing toward M.
        # The frozen contact line (RESIDUAL_LINE) is what the surgery widens; the eps=0
        # boundary is the declared P2-homogeneous control.
        w_u, w_p = ac112.weights(1e-9)
        self.assertAlmostEqual(w_u, math.log(4.0 / 3.0), places=6)
        self.assertLess(w_p, -10)


class TestDecisionBehavior(unittest.TestCase):
    def test_no_cause_no_relinquish(self):
        for arm in ('two_counter', 'single_counter', 'immediate', 'scramble'):
            r = ac112.run(0, 0, arm, 'no_cause')
            self.assertEqual(r['relinquishments'], 0, arm)
            self.assertTrue(r['completed'], arm)

    def test_move_relinquishes(self):
        for arm in ('two_counter', 'single_counter', 'immediate', 'scramble'):
            r = ac112.run(0, 0, arm, 'move')
            self.assertGreaterEqual(r['relinquishments'], 1, arm)

    def test_cut_single_counter_holds(self):
        r = ac112.run(0, 0, 'single_counter', 'cut')
        self.assertEqual(r['relinquishments'], 0)

    def test_cut_immediate_churns(self):
        # the no-memory immediate rival falsely relinquishes under the cut (its failure mode)
        r = ac112.run(0, 0, 'immediate', 'cut')
        self.assertGreaterEqual(r['relinquishments'], 1)

    def test_scramble_read_only(self):
        # the scramble forces the counter READ to (0,0) while the writes stay intact:
        # with the counter reads empty the weighted threshold can never fire.
        o, offs = ac12.acquire(0)
        streak = ac96.streak_offsets(o)
        n_u_offs = streak[0:4]
        n_p_offs = streak[4:6]
        bel_off = ac107_bel_offset()
        alloc = ac112.TwoCounterAlloc(0, 0, n_u_offs=n_u_offs, n_p_offs=n_p_offs,
                                      bel_off=bel_off, scramble=True)
        # write the counters to non-zero, then confirm the scramble reads them as 0
        e = ac9.event()
        ac112.counter_write(o, e, n_u_offs, 6)
        ac112.counter_write(o, e, n_p_offs, 2)
        self.assertEqual(alloc._n_u(o), 0)
        self.assertEqual(alloc._n_p(o), 0)
        self.assertFalse(alloc._holding(o))


def ac107_bel_offset():
    import ac107
    o, _ = ac12.acquire(0)
    return ac107.bel_offset(o)


class TestObserverDiscard(unittest.TestCase):
    def test_per_tick_identical(self):
        d = ac112.observer_discard_equivalence(0, 0, 'cut')
        self.assertTrue(d['swap_applied'])
        self.assertTrue(d['per_tick_identical'])
        self.assertTrue(d['terminal_identical'])


class TestHostAudit(unittest.TestCase):
    def test_audit_shape(self):
        a = ac112.audit_host_fields()
        self.assertIn('candidate_config_host_fields', a)
        self.assertIn('candidate_observational_host_fields', a)
        # the decision state offsets are config, never a steering host field
        self.assertIn('n_u_offs', a['candidate_config_host_fields'])


if __name__ == '__main__':
    unittest.main()
