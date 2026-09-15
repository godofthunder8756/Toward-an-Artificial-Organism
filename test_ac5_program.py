import itertools
import unittest
import numpy as np
import ac4
import ac5_program as p


class CompactProgramTests(unittest.TestCase):
    def test_all_acquired_permutations_and_observations(self):
        b,*_=ac4.acquire(0)
        for priority in itertools.permutations(range(4)):
            p.install_at_acquisition(b.traces,priority)
            for o in range(512):
                self.assertEqual(p.choose(b.traces,o),ac4.demonstration(o,priority))

    def test_paid_commitment_change_and_damage(self):
        b,*_=ac4.acquire(0); p.install_at_acquisition(b.traces,[0,1,2,3])
        self.assertEqual(p.choose(b.traces,256|4),8)
        before=(b.energy,b.material)
        e=p.paid_replace(b,4*p.WIDTH,[0],2) # Disable acquired boundary rule.
        self.assertEqual(e['writes'],7)
        self.assertEqual((b.energy,b.material),(before[0]-7,before[1]-7))
        self.assertEqual(p.choose(b.traces,256|4),2)
        # Corrupting the majority of the enabled bit changes live behavior.
        b.traces[0,4*p.WIDTH,:4]=1
        self.assertEqual(p.choose(b.traces,256|4),8)

    def test_no_free_or_over_capacity_write(self):
        b,*_=ac4.acquire(0); p.install_at_acquisition(b.traces,[0,1,2,3])
        before=b.digest()
        self.assertFalse(p.paid_replace(b,4*p.WIDTH,[0],0)['applied'])
        self.assertEqual(b.digest(),before)
        b.energy=6; before=b.digest()
        self.assertFalse(p.paid_replace(b,4*p.WIDTH,[0],2)['applied'])
        self.assertEqual(b.digest(),before)


if __name__=='__main__': unittest.main()
