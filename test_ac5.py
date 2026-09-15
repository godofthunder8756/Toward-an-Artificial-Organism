import unittest
import numpy as np
import ac5
import ac4


class AdaptiveMechanisms(unittest.TestCase):
    def test_paid_probe_and_feedback(self):
        b,*_=ac5.acquire(1); z=np.zeros_like(b.traces); dirs=np.zeros(20,dtype=int)
        e=ac5.step(b,z,dirs,True,False,False)
        self.assertEqual(e['learn_writes'],7); self.assertEqual(e['spent_e'],8)
        self.assertFalse(ac5.enabled(b.traces))
        b.boundary[:]=0; b.pos[0]=[2,0]
        e=ac5.step(b,z,dirs,False,False,False)
        self.assertGreater(e['crossings'],0); self.assertTrue(ac5.enabled(b.traces))
        self.assertEqual(e['learn_writes'],7)

    def test_retention_not_direct_phase_signal(self):
        a,*_=ac5.acquire(1); b,*_=ac5.acquire(1)
        z=np.zeros_like(a.traces); dirs=np.zeros(20,dtype=int)
        # Intact physical boundary makes retention interventions redundant here.
        self.assertEqual(ac5.step(a,z,dirs,False,False,False),ac5.step(b,z,dirs,False,False,True))
        self.assertEqual(a.digest(),b.digest())
        with self.assertRaises(ValueError): ac5.step(a,z,dirs,False,False,False,shadow=b.traces)

    def test_erasure_and_capacity(self):
        a,*_=ac5.acquire(0); b,*_=ac5.acquire(1)
        for x in (a,b):
            x.traces[:]=0; x.life[:]=0; x.pos[:]=0; x.boundary[:]=0
            x.energy=x.material=x.fuel=0; x.dead=False
        z=np.zeros_like(a.traces); dirs=np.zeros(20,dtype=int)
        ac5.step(a,z,dirs,True,True,False); ac5.step(b,z,dirs,True,True,False)
        self.assertEqual(a.digest(),b.digest())
        a,*_=ac5.acquire(1); a.life[:4]=0
        e=ac5.step(a,z,dirs,True,False,False)
        self.assertEqual(e['learn_success'],0); self.assertEqual(e['learn_writes'],0)

    def test_short_replay(self):
        for arm in ac5.ARMS:
            self.assertEqual(ac5.run(99,arm,80),ac5.run(99,arm,80))


if __name__=='__main__': unittest.main()
