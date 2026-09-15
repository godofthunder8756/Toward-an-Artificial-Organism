import unittest
import numpy as np
import ac9


class IntegratedAllocation(unittest.TestCase):
    def test_paid_seed_and_growth(self):
        o=ac9.acquire(0); o.body.fuel=0
        e=ac9.step(o,np.zeros((126,7),dtype=np.uint8),np.zeros_like(o.memory.bits),np.zeros(20,dtype=int),False,(0,0),[True,False])
        self.assertEqual(e['region0_births'],3); self.assertEqual(e['deposits'],1)
        self.assertEqual(e['spent_m'],33); self.assertEqual(e['memory_bound'],21)

    def test_empty_region_no_demand(self):
        o=ac9.acquire(0)
        self.assertFalse(ac9.observe(o)&64)
        self.assertEqual(o.memory.demand().sum(),0)

    def test_full_erasure(self):
        a=ac9.acquire(0); b=ac9.acquire(1)
        for o in (a,b):
            o.body.traces[:]=0; o.body.life[:]=0; o.body.pos[:]=0; o.body.boundary[:]=0
            o.body.energy=o.body.material=o.body.fuel=0; o.body.dead=False
            o.memory.bits[:]=0; o.memory.life[:]=0
        inputs=(np.zeros((126,7),dtype=np.uint8),np.zeros_like(a.memory.bits),np.zeros(20,dtype=int),False,(1,1),[True,False])
        self.assertEqual(ac9.step(a,*inputs),ac9.step(b,*inputs)); self.assertEqual(a.digest(),b.digest())

    def test_replay(self):
        for history in (0,1):
            for arm in ac9.ARMS: self.assertEqual(ac9.run(4,history,arm,80),ac9.run(4,history,arm,80))


if __name__=='__main__': unittest.main()
