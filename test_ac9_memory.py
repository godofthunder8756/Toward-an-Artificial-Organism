import unittest
from types import SimpleNamespace
import numpy as np
import ac9_memory as m


class AllocatedMemoryTests(unittest.TestCase):
    def body(self): return SimpleNamespace(energy=1000,material=1000)

    def test_empty_is_physically_absent(self):
        x=m.Memory.empty(); b=self.body(); before=x.digest()
        self.assertIsNone(x.read(0)); self.assertEqual(x.demand().sum(),0)
        self.assertEqual(m.age(x,np.ones_like(x.bits)),0)
        self.assertEqual(x.digest(),before)
        self.assertEqual(m.renew(x,b,0,4)['writes'],0)

    def test_paid_local_deposition(self):
        x=m.Memory.empty(); b=self.body()
        e=m.deposit(x,b,0,1,[False,True],[3,3])
        self.assertEqual(e,dict(writes=21,bound=21,region=1))
        self.assertEqual((b.energy,b.material),(979,979))
        np.testing.assert_array_equal(x.demand(),[0,21]); self.assertEqual(x.read(0),1)
        self.assertEqual(m.deposit(x,b,0,1,[True,False],[3,3])['writes'],0)

    def test_no_free_seed_or_failed_transaction(self):
        for energy,material,W in ((100,100,0),(100,100,2),(20,100,4),(100,20,4)):
            x=m.Memory.empty(); before=x.digest(); b=SimpleNamespace(energy=energy,material=material)
            self.assertEqual(m.deposit(x,b,1,0,[True,False],[W,0])['writes'],0)
            self.assertEqual(x.digest(),before); self.assertEqual((b.energy,b.material),(energy,material))

    def test_expiry_erases_and_majority_has_no_target(self):
        x=m.Memory.empty(); b=self.body(); m.deposit(x,b,0,1,[True,False],[3,3])
        x.bits[0,0,2,:4]=0
        self.assertEqual(x.read(0),0)
        e=m.renew(x,b,0,4); self.assertEqual(e['writes'],3)
        self.assertEqual(x.read(0),0) # Never restores the original value from a target.
        waste=0
        for _ in range(64): waste+=m.age(x,np.zeros_like(x.bits))
        self.assertEqual(waste,21); self.assertEqual(x.digest(),m.Memory.empty().digest())

    def test_history_changes_local_demand_and_renewal(self):
        memories=[m.Memory.empty(),m.Memory.empty()]; bodies=[self.body(),self.body()]
        for region in range(2): m.deposit(memories[region],bodies[region],0,1,[region==0,region==1],[3,3])
        # Same later resources and renewal region: only region0 receives renewal.
        for _ in range(128):
            for x,b in zip(memories,bodies):
                m.age(x,np.zeros_like(x.bits)); m.renew(x,b,0,4)
        self.assertEqual(memories[0].read(0),1); self.assertIsNone(memories[1].read(0))


if __name__=='__main__': unittest.main()
