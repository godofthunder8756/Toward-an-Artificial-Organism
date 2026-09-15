import unittest
import numpy as np
import ac4
import ac5
import ac7
import ac8


class RouteMaintenanceTests(unittest.TestCase):
    def test_exact_default_step(self):
        a,*_=ac5.acquire(0); b,*_=ac5.acquire(0)
        z=np.zeros_like(a.traces); d=np.zeros(20,dtype=int)
        for _ in range(80):
            self.assertEqual(ac7.step(a,z,d,False,(1,1)),ac8.step(b,z,d,False,(1,1)))
            self.assertEqual(a.digest(),b.digest())

    def test_repair_selectivity_and_payment(self):
        b,*_=ac5.acquire(0); b.traces[0,10,0]^=1; b.traces[0,50,0]^=1
        route=b.traces[0,10].copy(); other=b.traces[0,50].copy()
        e=ac4.empty_event(); before=ac4.inventory(b)
        ac8.selective_react(b,2,'self',e,False); ac4.balance(before,b,e)
        np.testing.assert_array_equal(route,b.traces[0,10])
        self.assertFalse(np.array_equal(other,b.traces[0,50]))
        self.assertEqual(e['writes'],1)

    def test_replay(self):
        for arm in ac8.ARMS: self.assertEqual(ac8.run(1,arm,80),ac8.run(1,arm,80))


if __name__=='__main__': unittest.main()
