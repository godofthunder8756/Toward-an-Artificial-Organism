"""Numerical, causal, resource-ledger and information-boundary tests."""
import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from e2.model import Config,Network
from e2.experiment import rollout

class TestE2(unittest.TestCase):
    def setUp(self):
        self.cfg=Config();self.net=Network(self.cfg,7);self.body=self.net.initial_body()
    def test_bptt_against_finite_differences(self):
        n=self.net;rng=np.random.default_rng(3);x=rng.normal(size=(3,7,8))
        q,l,c=n.forward(x,self.body.mass);dq=rng.normal(size=q.shape);dl=rng.normal(size=l.shape);g=n.grads(c,dq,dl)
        for k,idx in [('u',(0,0)),('u',(6,1)),('w',(0,0)),('b',(2,)),('v',(2,0)),('v',(2,4))]:
            old=n.p[k][idx];values=[]
            for sign in [1,-1]:
                n.p[k][idx]=old+sign*1e-6;q,l,_=n.forward(x,self.body.mass);values.append((q*dq).sum()+(l*dl).sum())
            n.p[k][idx]=old
            self.assertAlmostEqual(g[k][idx],(values[0]-values[1])/2e-6,places=7)
    def test_future_cue_cannot_change_resource_decision(self):
        obs=self.body.observe();a=self.net.forward(self.net.inputs(obs,0),self.body.mass)[0]
        b=self.net.forward(self.net.inputs(obs,1),self.body.mass)[0];np.testing.assert_array_equal(a,b)
    def test_no_current_task_answer_in_interoception(self):
        obs=self.body.observe('normal');self.body.energy-=.2
        changed=self.body.observe('normal');self.assertEqual(np.count_nonzero(obs!=changed),1)
        # Hidden chemistry interventions share the exact pre-event observation.
        np.testing.assert_equal(self.body.observe('normal'),self.body.observe('sham'))
        np.testing.assert_equal(self.body.observe('normal'),self.body.observe('swap'))
    def test_resource_and_biomass_mass_balance(self):
        b=self.body;rng=np.random.default_rng(4)
        for _ in range(1000):
            old=b.mass.copy();st=b.store.copy();a=int(rng.integers(0,3))
            r=b.update(a,rng.random(old.shape));self.assertLess(r['balance_error'],1e-12)
            self.assertTrue(np.all(b.store>=-1e-12));self.assertTrue(np.all(b.store<=self.cfg.store_cap+1e-12))
            # Each edge's material unit is normalized by target indegree.
            installed=((b.mass-(1-self.cfg.decay)*old).sum(0)/b.mask.sum(0)).sum()
            self.assertAlmostEqual(installed,r['consumed'],places=12)
    def test_sham_cannot_create_material(self):
        b=self.body;b.store[:]=0;old=b.mass.copy()
        r=b.update(1,np.ones_like(old),'sham');self.assertEqual(r['consumed'],0)
        np.testing.assert_allclose(b.mass,old*(1-self.cfg.decay))
    def test_rescue_is_external_material_not_stored_material(self):
        b=self.body;b.store[:]=0;r=b.update(0,np.ones_like(b.mass),'rescue')
        self.assertEqual(r['consumed'],0);self.assertGreater(r['external'],0)
        self.assertGreater(b.mass.sum(),self.cfg.initial_mass*b.mask.sum())
    def test_active_and_inactive_edges_diverge(self):
        a=self.body;b=copy.deepcopy(a)
        for _ in range(100):
            a.update(0,np.ones_like(a.mass)*.5,'rescue')
            b.update(0,np.zeros_like(b.mass),'rescue')
        self.assertGreater(a.mass.sum(),b.mass.sum()*2)
    def test_static_target_restores_without_growing(self):
        b=self.body;b.mass*=.1
        for _ in range(4):b.update(0,np.ones_like(b.mass),'rescue',structural='static')
        np.testing.assert_allclose(b.mass,self.cfg.initial_mass*b.mask,atol=1e-14)
    def test_all_tissue_lesion_disconnects_both_decisions(self):
        x=self.net.inputs(self.body.observe(),1)
        q,l,_=self.net.forward(x,self.body.mass,lesion=np.ones(self.cfg.hidden,dtype=bool))
        np.testing.assert_equal(q,0);np.testing.assert_equal(l,0)
    def test_no_recurrence_no_delayed_cue_information(self):
        self.net.p['w'][:]=0
        a=self.net.forward(self.net.inputs(self.body.observe(),0),self.body.mass)[1]
        b=self.net.forward(self.net.inputs(self.body.observe(),1),self.body.mass)[1]
        np.testing.assert_array_equal(a,b)
    def test_propensity_correction(self):
        # Enumeration, not simulation: successful loss weight has expectation 1
        # for either true answer even when the policy strongly favors the other.
        for preferred in [0,1]:
            for answer in [0,1]:
                total=sum((.15+.7*(a==preferred))*(a==answer)/(.15+.7*(a==preferred)) for a in [0,1])
                self.assertAlmostEqual(total,1.)
    def test_clone_and_saved_replay(self):
        n=self.net;b=self.body
        rollout(n,b,123,64,training=True)
        a=copy.deepcopy(n);bb=copy.deepcopy(b)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'state.npz';n.save(p,b);nn,b2=Network.load(p,self.cfg)
            r1=rollout(a,bb,999,60);r2=rollout(nn,b2,999,60)
            self.assertEqual(r1,r2)
        np.testing.assert_equal(n.p['w'],a.p['w'])
    def test_dead_trials_are_retained(self):
        self.body.energy=0;r=rollout(self.net,self.body,1,30)
        self.assertEqual(len(r),30);self.assertEqual(sum(x['active'] for x in r),0)
    def test_no_weight_updates_when_frozen(self):
        old=copy.deepcopy(self.net.p);rollout(self.net,self.body,1,100,training=True,freeze_weights=True)
        for k in old:np.testing.assert_array_equal(old[k],self.net.p[k])

if __name__=='__main__':unittest.main()
