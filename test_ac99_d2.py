"""AC99-D2 tests: the 3-bit Gray-coded streak vs the binary streak.

Pins, at the primitive level:
- the 3-bit reflected Gray code round-trips (encode/decode 0..7);
- every Gray increment 0->1 ... 4->5 changes ONE logical bit (7 replicas), and in particular
  the 3->4 increment that stalls the binary streak is 1 bit in Gray vs 3 bits in binary;
- the reset 5->0 is THREE bits (21 replicas) in Gray vs TWO (14) in binary -- Gray is NOT
  uniformly cheaper (recorded against the task's "same as binary" parenthetical);
- Gray and binary agree at value 0 (both encode 000), so a reset-to-zero writes the same
  target bits;
- the decisive 4436 flip: the binary reserve arm dies at 8430 with the streak stuck at 3
  (the AC98 G1 failure), the Gray reserve arm relinquishes + re-acquires both routes + survives.

Not hashed (AC17's rule) -- verification tool only.
"""
import unittest
import ac4
import ac9
import ac12
import ac95
import ac96
import ac99
import ac99_d2


def setUpModule():
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac95.ac71.DEV
    ac12.REGISTER_THRESHOLD = 4


def _fresh(seed=0):
    o, offs = ac12.acquire(seed)
    o.body.life[:4] = 64          # four live W catalysts -> _cap >= 32
    o.body.pos[:4] = 0
    o.body.energy = 200
    o.body.material = 200
    return o, ac96.streak_offsets(o)


def _ev():
    return ac9.event()


class TestGrayCode(unittest.TestCase):
    def test_round_trip(self):
        for n in range(8):
            self.assertEqual(ac99_d2.gray_decode(ac99_d2.gray_encode(n)), n)

    def test_adjacent_values_differ_in_one_bit(self):
        # the defining Gray property: consecutive counts differ in exactly one bit
        for cur in range(7):
            self.assertEqual(
                (ac99_d2.gray_encode(cur) ^ ac99_d2.gray_encode(cur + 1)).bit_count(), 1)


class TestTransitionCosts(unittest.TestCase):
    def test_three_to_four_is_single_bit_in_gray(self):
        # binary 3 (011) -> 4 (100) = 3 bits = 21 replicas; Gray 3 (010) -> 4 (110) = 1 bit
        self.assertEqual((3 ^ 4).bit_count(), 3)
        self.assertEqual((ac99_d2.gray_encode(3) ^ ac99_d2.gray_encode(4)).bit_count(), 1)

    def test_one_to_two_is_single_bit_in_gray(self):
        # binary 1 (001) -> 2 (010) = 2 bits = 14 replicas; Gray 1 (001) -> 2 (011) = 1 bit
        self.assertEqual((1 ^ 2).bit_count(), 2)
        self.assertEqual((ac99_d2.gray_encode(1) ^ ac99_d2.gray_encode(2)).bit_count(), 1)

    def test_reset_is_three_bits_in_gray_two_in_binary(self):
        # the drop reset 5->0: Gray 5 (111) -> 0 = 3 bits = 21 replicas; binary 5 (101) -> 0 = 2
        # bits = 14 replicas. Gray is MORE expensive on reset, not the same as binary.
        self.assertEqual((5 ^ 0).bit_count(), 2)
        self.assertEqual((ac99_d2.gray_encode(5) ^ ac99_d2.gray_encode(0)).bit_count(), 3)

    def test_every_increment_is_one_bit_in_gray(self):
        for cur in range(5):
            g = (ac99_d2.gray_encode(cur) ^ ac99_d2.gray_encode(cur + 1)).bit_count()
            self.assertEqual(g, 1, f'Gray {cur}->{cur+1} is {g} bits, expected 1')


class TestStreakWriteReplicas(unittest.TestCase):
    def test_gray_three_to_four_writes_seven_replicas(self):
        o, offs = _fresh(0)
        e = _ev()
        self.assertEqual(ac99_d2.gray_streak_write(o, e, 1, 3, offs), 7)  # 0 -> 3 (010): 1 bit
        self.assertEqual(ac99_d2.gray_streak_read(o, 1, offs), 3)
        e2 = _ev()
        self.assertEqual(ac99_d2.gray_streak_write(o, e2, 1, 4, offs), 7)  # 3 -> 4 (110): 1 bit
        self.assertEqual(ac99_d2.gray_streak_read(o, 1, offs), 4)

    def test_binary_three_to_four_writes_twenty_one_replicas(self):
        o, offs = _fresh(0)
        e = _ev()
        self.assertEqual(ac96.streak_write(o, e, 1, 3, offs), 14)  # 0 -> 3 (011): 2 bits
        self.assertEqual(ac96.streak_read(o, 1, offs), 3)
        e2 = _ev()
        self.assertEqual(ac96.streak_write(o, e2, 1, 4, offs), 21)  # 3 -> 4 (100): 3 bits
        self.assertEqual(ac96.streak_read(o, 1, offs), 4)

    def test_value_zero_encodes_identically(self):
        # reset-to-zero writes the same target bits (000) in both codes
        self.assertEqual(ac99_d2.gray_encode(0), 0)
        o, offs = _fresh(0)
        self.assertEqual(ac99_d2.gray_streak_read(o, 1, offs),
                         ac96.streak_read(o, 1, offs))


class TestRecorded4436Flip(unittest.TestCase):
    def test_4436_binary_dies_gray_relinquishes_and_survives(self):
        # the AC98 G1 failure seed: binary reserve arm dies at 8430 (streak stuck 3), the Gray
        # reserve arm relinquishes and survives. A future code change that moves this record
        # is caught. (Slow-ish but ~0.7s total.)
        for h in (0, 1):
            b = ac99.run(4436, h, 'gated', reserve=True)
            g = ac99_d2.run(4436, h, 'gated', reserve=True)
            self.assertFalse(b['completed'], f'4436/{h} binary should still die (AC98 G1)')
            self.assertEqual(b['first_dead'], 8430)
            self.assertEqual(b['relinquishments'], 0)
            self.assertEqual(b['streak_final'][1], 3, 'binary streak should be stuck at 3')
            self.assertTrue(g['completed'], f'4436/{h} gray should survive')
            self.assertEqual(g['relinquishments'], 1, f'4436/{h} gray should relinquish')
            self.assertEqual(g['routes'], [0, 1], f'4436/{h} gray should hold both routes')


if __name__ == '__main__':
    unittest.main()
