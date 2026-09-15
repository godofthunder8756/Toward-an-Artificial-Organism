import unittest
import numpy as np
import ac4_transport as t


class TransportTests(unittest.TestCase):
    def test_each_link_bidirectional(self):
        inner = []; outer = []
        for axis, side in ((0, 3), (0, -3), (1, 3), (1, -3)):
            for other in range(-2, 3):
                p = [0, 0]; q = [0, 0]
                p[axis] = 2 if side > 0 else -2; q[axis] = side
                p[1-axis] = q[1-axis] = other
                inner.append(p); outer.append(q)
        a, b = np.array(inner), np.array(outer)
        np.testing.assert_array_equal(t.crossing_link(a, b), np.arange(20))
        np.testing.assert_array_equal(t.crossing_link(b, a), np.arange(20))

    def test_species_and_export(self):
        pos = np.array([[2, 0], [2, 0], [5, 0]], dtype=np.int16)
        exported = np.zeros(3, dtype=bool)
        event = t.move(pos, exported, np.ones(20), np.zeros(3, dtype=int), np.array([1, 0, 0], dtype=bool))
        np.testing.assert_array_equal(pos, [[2, 0], [3, 0], [6, 0]])
        self.assertEqual(event['blocked'], 1)
        t.move(pos, exported, np.ones(20), np.ones(3, dtype=int), np.zeros(3, dtype=bool))
        self.assertEqual(pos[2, 0], 6)

    def test_paired_interventions_and_expiry(self):
        r = {a: t.run(21, a) for a in t.ARMS}
        self.assertEqual(r['open']['state_hash'], r['permeant']['state_hash'])
        self.assertEqual(r['intact']['state_hash'], r['retention_rescue']['state_hash'])
        self.assertTrue(all(x == [512, 0, 0] for x in r['decaying']['inventories'][:31]))
        self.assertGreaterEqual(r['decaying']['first_crossing'], 32)
        self.assertLess(r['decaying']['interior'], 1)
        self.assertEqual(r['intact']['interior'], 1)


if __name__ == '__main__':
    unittest.main()
