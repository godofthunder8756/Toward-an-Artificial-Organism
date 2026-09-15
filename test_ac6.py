import unittest
import numpy as np
import ac4
import ac5
import ac6


class LocalTests(unittest.TestCase):
    def test_paid_action_change(self):
        b,*_=ac6.acquire(0); z=np.zeros_like(b.traces); d=np.zeros(20,dtype=int)
        e=ac6.step(b,z,d,True,False,False)
        self.assertEqual(e['learn_writes'],7); self.assertFalse(ac6.enabled(b.traces))
        self.assertEqual(ac6.prog.choose(b.traces,256),10)
        b.boundary[:]=0; b.pos[0]=[2,0]
        e=ac6.step(b,z,d,False,False,False)
        self.assertTrue(ac6.enabled(b.traces)); self.assertGreater(e['crossings'],0)

    def test_local_exclusion_and_payment(self):
        b,*_=ac6.acquire(0); b.boundary[:]=0; b.pos[:]=[2,0]
        e=ac6.ac4.empty_event(); before=ac4.inventory(b)
        ac6.local_boundary(b,e); ac4.balance(before,b,e)
        self.assertEqual(b.boundary[0],0); self.assertEqual(e['B_birth'],1)

    def test_phase_and_erasure(self):
        a,*_=ac6.acquire(0); b,*_=ac6.acquire(0)
        z=np.zeros_like(a.traces); d=np.zeros(20,dtype=int)
        self.assertEqual(ac6.step(a,z,d,False,False,False),ac6.step(b,z,d,False,False,True))
        with self.assertRaises(ValueError): ac6.step(a,z,d,False,False,False,shadow=b.traces)
        a,*_=ac6.acquire(2)
        for x in (a,b):
            x.traces[:]=0; x.life[:]=0; x.pos[:]=0; x.boundary[:]=0
            x.energy=x.material=x.fuel=0; x.dead=False
        ac6.step(a,z,d,True,False,False); ac6.step(b,z,d,True,False,False)
        self.assertEqual(a.digest(),b.digest())

    def test_global_comparator(self):
        expected=ac5.run(99,'adaptive',80); expected['arm']='global'
        self.assertEqual(ac6.run(99,'global',80),expected)
        for arm in ac6.ARMS:
            self.assertEqual(ac6.run(99,arm,80),ac6.run(99,arm,80))


if __name__=='__main__': unittest.main()
