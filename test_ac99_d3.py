"""AC99-D3 verification (not hashed — AC17's rule): pins the recorded outcomes so a future code
change that moves the record is caught instead of silently absorbed.

No freeze, no protocol — this is an engineering rival, verified by:
  1. byte-identity: wb_first=False reproduces ac99.run(reserve=True) (state_hash) on the failing seed;
  2. the declared priority-change cost (2 words x 5 logical bits = 10 bits = 70 replicas);
  3. the recorded 4436 flip: binary reserve arm dies (8430, streak stuck 3, W_births_post_move=0),
     the W-birth-priority rival survives + relinquishes + re-acquires both routes (W=3, 768 births);
  4. the W availability-vs-birth reconciliation: frozen 4436's W decays monotonically 3->0 with zero
     post-move W-birth events (the narrative's "W recovers once" is wrong).
"""
import unittest
import numpy as np
import ac99
import ac99_d3


class TestPriorityChange(unittest.TestCase):
    def test_cost_is_10_bits_70_replicas(self):
        bits, replicas = ac99_d3.priority_change_cost()
        self.assertEqual(bits, 10)
        self.assertEqual(replicas, 70)

    def test_wb_first_description_swaps_words_1_and_2(self):
        priority = [1, 3, 0, 2]   # 4436's acquired priority
        base = ac99_d3.ac95.description_bits(priority)
        wb = ac99_d3.wb_first_description(priority)
        # words 1 and 2 (description bits 14:42) are swapped; the rest is identical
        base_words = base[14:42].reshape(2, 14)
        wb_words = wb[14:42].reshape(2, 14)
        self.assertTrue(np.array_equal(wb_words[0], base_words[1]))
        self.assertTrue(np.array_equal(wb_words[1], base_words[0]))
        self.assertTrue(np.array_equal(wb[:14], base[:14]))
        self.assertTrue(np.array_equal(wb[42:], base[42:]))

    def test_rebuilt_program_has_wb_first_order(self):
        priority = [1, 3, 0, 2]
        prog = ac99_d3.ac95.build_program(ac99_d3.wb_first_description(priority))
        words = prog.reshape(9, 14)
        word = (words * (1 << np.arange(14))).sum(axis=1)
        # position 1 must now be mask 64 action 6 (W-birth), position 2 mask 2 action 1 (contact)
        self.assertEqual((int(word[1]) >> 1) & 511, 64)
        self.assertEqual((int(word[1]) >> 10) & 15, 6)
        self.assertEqual((int(word[2]) >> 1) & 511, 2)
        self.assertEqual((int(word[2]) >> 10) & 15, 1)


class TestByteIdentity(unittest.TestCase):
    def test_wb_first_false_reproduces_ac99(self):
        # the rival is the ONLY change: wb_first=False must be byte-identical to ac99.run
        n = ac99_d3.frozen_reproduction([4436])
        self.assertEqual(n, 2)   # 2 histories


class TestRecorded4436Flip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = ac99_d3.run(4436, 0, 'gated', reserve=True, damage=True,
                                 corrupt=False, transition='perm', wb_first=False)
        cls.wb = ac99_d3.run(4436, 0, 'gated', reserve=True, damage=True,
                             corrupt=False, transition='perm', wb_first=True)

    def test_frozen_arm_dies_streak_stuck_at_3(self):
        self.assertFalse(self.frozen['completed'])
        self.assertEqual(self.frozen['first_dead'], 8430)
        self.assertEqual(self.frozen['relinquishments'], 0)
        self.assertEqual(self.frozen['streak_final'], {0: 0, 1: 3})
        self.assertEqual(self.frozen['W_births_post_move'], 0)

    def test_wb_first_rival_relinquishes_and_survives(self):
        self.assertTrue(self.wb['completed'])
        self.assertIsNone(self.wb['first_dead'])
        self.assertEqual(self.wb['relinquishments'], 1)
        self.assertEqual(self.wb['routes'], [0, 1])
        self.assertEqual(self.wb['streak_final'], {0: 0, 1: 0})
        self.assertEqual(self.wb['W'], 3)
        self.assertGreater(self.wb['W_births_post_move'], 0)

    def test_rival_is_paid_and_internal(self):
        # the full 70-replica swap is paid through the program bank (energy-limited at acquisition,
        # completed over the first few ticks via the body's own conversion). Internal, no external W.
        self.assertEqual(self.wb['priority_writes'], 70)


class TestWReconciliation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row, _, _, cls.wt = ac99_d3._run_internal(
            4436, 0, 'gated', True, True, False, 'perm',
            ac99_d3.TICKS, ac99_d3.MOVE_TICK, wb_first=False, record_w_trace=True)

    def test_W_never_recovers(self):
        # W availability monotonically decays post-move: never increases
        ws = [d['W'] for d in self.wt if d['t'] >= 8192]
        for i in range(1, len(ws)):
            self.assertLessEqual(ws[i], ws[i - 1],
                                 f'W increased at tick {8192 + i}: {ws[i-1]} -> {ws[i]}')

    def test_zero_post_move_W_birth_events(self):
        births = [d['t'] for d in self.wt if d['W_birth'] > 0 and d['t'] >= 8192]
        self.assertEqual(births, [])

    def test_material_never_clears_64_in_window(self):
        # the narrative claims "material rises above 64"; it does not in the post-step trace
        mats = [d['material'] for d in self.wt if 8228 <= d['t'] <= 8235]
        self.assertTrue(all(m <= 64 for m in mats), f'material rose above 64: {mats}')


if __name__ == '__main__':
    unittest.main()
