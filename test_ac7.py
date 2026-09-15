import inspect
import unittest
import numpy as np
import ac7
import ac5


class RoutingTests(unittest.TestCase):
    def test_paid_learning_from_physical_failure(self):
        b,*_=ac5.acquire(0); e=ac7.ac4.empty_event()
        e.update(contacts=0,productive=0,learn_attempt=0,learn_success=0,learn_writes=0)
        resource,success=ac7.contact(b,0,(1,0),e)
        self.assertFalse(success); self.assertEqual(e['in_f'],0)
        ac7.learn_from_contact(b,b.traces,resource,success,e)
        self.assertEqual(ac7.route_actions(b.traces)[0],12)
        self.assertEqual(e['learn_writes'],14); self.assertEqual(e['spent_e'],15)
        self.assertNotIn('mapping',inspect.signature(ac7.learn_from_contact).parameters)

    def test_resource_rejection_and_erasure_specificity(self):
        b,*_=ac5.acquire(0); b.life[:4]=0
        e=dict(writes=0,learn_writes=0,spent_e=0,spent_m=0,learn_attempt=0,learn_success=0)
        ac7.learn_from_contact(b,b.traces,0,False,e)
        self.assertEqual(e['learn_success'],0)
        b,*_=ac5.acquire(0)
        for resource in (0,1): ac7.learn_from_contact(b,b.traces,resource,False,e)
        self.assertEqual(ac7.route_actions(b.traces),[12,13])
        copy=b.traces.copy(); n=ac7.erase_routes(b)
        self.assertEqual(n,28); self.assertEqual(ac7.route_actions(b.traces),[0,1])
        copy[0,10:14]=b.traces[0,10:14]; copy[0,24:28]=b.traces[0,24:28]
        np.testing.assert_array_equal(copy,b.traces)

    def test_full_erasure_and_replay(self):
        a,*_=ac5.acquire(0); b,*_=ac5.acquire(1)
        for x in (a,b):
            x.traces[:]=0; x.life[:]=0; x.pos[:]=0; x.boundary[:]=0
            x.energy=x.material=x.fuel=0; x.dead=False
        z=np.zeros_like(a.traces); dirs=np.zeros(20,dtype=int)
        ac7.step(a,z,dirs,False,(1,1)); ac7.step(b,z,dirs,False,(1,1))
        self.assertEqual(a.digest(),b.digest())
        with self.assertRaises(ValueError): ac7.step(a,z,dirs,False,(1,1),shadow=b.traces)
        for arm in ac7.ARMS: self.assertEqual(ac7.run(17,arm,80),ac7.run(17,arm,80))


if __name__=='__main__': unittest.main()
