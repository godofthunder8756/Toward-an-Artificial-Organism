import unittest
import numpy as np
import ac4


class Mechanisms(unittest.TestCase):
    def test_boundary_payment_locality(self):
        b,*_=ac4.acquire(0); b.boundary[:]=0; b.pos[:]=0
        e=ac4.empty_event(); ac4.react(b,8,'self',e)
        self.assertEqual(e['B_birth'],0)
        b.pos[0]=[2,0]; e=ac4.empty_event(); before=ac4.inventory(b)
        ac4.react(b,8,'self',e); ac4.balance(before,b,e)
        self.assertEqual(e['B_birth'],1); self.assertEqual(e['spent_m'],2)
        self.assertEqual(e['spent_e'],3)

    def test_outside_inactive(self):
        b,*_=ac4.acquire(0); b.pos[:]=[4,0]
        self.assertFalse(ac4.available(b).any())
        e=ac4.empty_event(); ac4.react(b,6,'self',e)
        self.assertEqual(e['W_birth'],0)
        b.traces[0,0,0]^=1; e=ac4.empty_event(); ac4.react(b,2,'self',e)
        self.assertEqual(e['writes'],0)

    def test_state_erasure_and_template_rejection(self):
        b,*_=ac4.acquire(0); other,*_=ac4.acquire(1)
        # Entire declared state reset, including positions and all lifetimes.
        for x in (b,other):
            x.traces[:]=0; x.life[:]=0; x.pos[:]=0; x.boundary[:]=0
            x.energy=x.material=x.fuel=0; x.dead=False
        z=np.zeros_like(b.traces); directions=np.zeros(20,dtype=int)
        self.assertEqual(ac4.step(b,z,directions),ac4.step(other,z,directions))
        self.assertEqual(b.digest(),other.digest())
        with self.assertRaises(ValueError): ac4.step(b,z,directions,protected=np.zeros(512))

    def test_expiry_export_and_replay(self):
        b,*_=ac4.acquire(0); b.life[:]=0; b.life[0]=1; b.life[1]=30
        b.pos[1]=[5,0]; b.boundary[:]=1
        e=ac4.step(b,np.zeros_like(b.traces),np.zeros(20,dtype=int),'no_B')
        self.assertEqual(e['particle_expiry'],1); self.assertEqual(e['particle_export'],1)
        self.assertEqual(e['B_expiry'],20)
        for arm in ac4.ARMS:
            self.assertEqual(ac4.run(9,.0001,arm,80),ac4.run(9,.0001,arm,80))


if __name__=='__main__': unittest.main()
