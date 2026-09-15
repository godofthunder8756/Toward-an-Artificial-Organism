import json
import unittest
import numpy as np
import ac9
import ac10
import ac4
import ac5_program as prog


def inputs(o,coin=0,directions=None):
    core=np.zeros((126,7),dtype=np.uint8); noise=np.zeros_like(o.memory.bits)
    d=np.zeros(20,dtype=int) if directions is None else directions
    return core,noise,d,bool(coin)


def force_action(o,want):
    """Set the constituent banks that select action 6 (make W) or 7 (make C)."""
    assert want in (6,7)
    o.body.life[0:4]=np.array([64,0,0,0] if want==6 else [32,48,64,0],dtype=np.int16)
    o.body.life[16:20]=np.array([0,0,0,0] if want==7 else [64,96,128,0],dtype=np.int16)
    o.body.fuel=32; o.body.material=128; o.body.energy=64
    return prog.choose(o.body.traces,ac9.observe(o))


def forced_step(arm,want,seed=0):
    o=ac10.v2.acquire(seed)
    assert force_action(o,want)==want,(arm,want)
    pre,_=ac10.build(arm); core,noise,d,coin=inputs(o)
    e=pre(o,core,noise,d,coin,(seed%2,(seed//2)%2),[True,False],True)
    return o,e


def norm(x): return json.loads(json.dumps(x))


def check_ledger(row):
    """The frozen AC9 v3 material/energy identity, plus the labelled external B input."""
    l=row['ledger']; inv=row['final_inventory']
    m0=128+24+40+l['in_m']+2*l['external_B']
    m1=inv[1]+4*inv[3]+2*inv[4]+sum(row['demand'])
    spent=l['writes']-l['memory_writes']
    losses=(l['memory_waste']+l['memory_expiry']+
            4*(l['particle_expiry']+l['particle_export'])+
            2*(l['B_expiry']+l['B_discard'])+l['overflow_m'])
    assert m0==m1+spent+losses,(row['seed'],row['arm'],m0,m1,spent,losses)
    assert 64+8*l['converted']==inv[0]+l['spent_e'],(row['seed'],row['arm'])
    assert 32+l['in_f']==inv[2]+l['overflow_f']+l['converted'],(row['seed'],row['arm'])


class FrozenLaws(unittest.TestCase):
    def test_keep_arm_is_the_frozen_function(self):
        self.assertIs(ac10.build('keep')[0],ac9.step)
        self.assertIs(ac10.build('keep')[1],ac9.step)

    def test_keep_reproduces_frozen_v2_rows(self):
        """The keep arm must match the frozen ac9_priority_v2 'priority' data exactly."""
        frozen={}
        with open('ac9_priority_results_v2/results.json') as f:
            for r in json.load(f)['rows']:
                if r['variant']=='priority': frozen[(r['seed'],r['history'])]=r
        keys=['seed','history','ticks','mapping','activity','completed','routes','demand',
              'ledger','final_inventory','state_hash']
        for seed in (1100,1103):
            for history in (0,1):
                live=norm(ac10.run(seed,history,'keep'))
                ref=frozen[(seed,history)]
                for k in keys:
                    self.assertEqual(live[k],ref[k],f'seed{seed} history{history} field {k}')

    def test_every_arm_keeps_the_frozen_ledger_identity(self):
        for arm in ac10.ARMS:
            check_ledger(ac10.run(7,0,arm,ticks=400))


class SingleStepIsolation(unittest.TestCase):
    def test_W_ablation_removes_only_the_W_reaction(self):
        ko,ke=forced_step('keep',6); wo,we=forced_step('no_W',6)
        self.assertEqual(ke['W_birth'],1); self.assertEqual(we['W_birth'],0)
        self.assertEqual(ke['spent_m']-we['spent_m'],4)
        self.assertEqual(ke['spent_e']-we['spent_e'],2)
        self.assertEqual(wo.body.energy-ko.body.energy,2)
        for k in ke:
            if k not in ('W_birth','spent_m','spent_e','region0_births','region1_births'):
                self.assertEqual(ke[k],we[k],k)

    def test_W_ablation_leaves_the_C_reaction_intact(self):
        ke=forced_step('keep',7)[1]; ne=forced_step('no_W',7)[1]
        self.assertEqual(ke['C_birth'],1); self.assertEqual(ne['C_birth'],1)
        self.assertEqual(ke,ne)

    def test_C_ablation_removes_only_the_C_reaction(self):
        ke=forced_step('keep',7)[1]; ne=forced_step('no_C',7)[1]
        self.assertEqual(ke['C_birth'],1); self.assertEqual(ne['C_birth'],0)
        self.assertEqual(ke['spent_m']-ne['spent_m'],4)
        self.assertEqual(ke['spent_e']-ne['spent_e'],4)
        for k in ke:
            if k not in ('C_birth','spent_m','spent_e'):
                self.assertEqual(ke[k],ne[k],k)

    def test_B_ablation_leaves_the_W_and_C_reactions_intact(self):
        for want in (6,7):
            ke=forced_step('keep',want)[1]; ne=forced_step('no_B',want)[1]
            self.assertEqual(ke,ne,want)

    def test_retention_ablation_changes_transport_only(self):
        """One step: an intact enclosure retains a rim particle, permeant does not."""
        def rim(arm,boundary_value):
            o=ac10.v2.acquire(0)
            o.body.pos[0]=np.array([2,0],dtype=np.int16); o.body.life[0]=64
            o.body.boundary[:]=boundary_value
            pre,_=ac10.build(arm); core,noise,d,coin=inputs(o,directions=np.zeros(20,dtype=int))
            pre(o,core,noise,d,coin,(0,0),[True,False],True)
            return np.array(o.body.pos[0])
        np.testing.assert_array_equal(rim('keep',100),np.array([2,0]))
        np.testing.assert_array_equal(rim('permeant',100),np.array([3,0]))

    def test_retention_rescue_blocks_without_any_boundary_matter(self):
        def rim(arm):
            o=ac10.v2.acquire(0)
            o.body.pos[0]=np.array([2,0],dtype=np.int16); o.body.life[0]=64
            o.body.boundary[:]=0
            pre,_=ac10.build(arm); core,noise,d,coin=inputs(o,directions=np.zeros(20,dtype=int))
            pre(o,core,noise,d,coin,(0,0),[True,False],True)
            return np.array(o.body.pos[0])
        np.testing.assert_array_equal(rim('no_B'),np.array([3,0]))
        np.testing.assert_array_equal(rim('no_B_retention'),np.array([2,0]))


class ConstituentAblations(unittest.TestCase):
    def test_no_W_never_allocates_an_entry(self):
        r=ac10.run(7,0,'no_W',ticks=1024)
        self.assertEqual(r['ledger']['W_birth'],0)
        self.assertEqual(r['ledger']['memory_bound'],0)
        self.assertEqual(r['occupied_sites'],0)
        self.assertEqual(r['routes'],[None,None])
        k=ac10.run(7,0,'keep',ticks=1024)
        self.assertGreater(k['ledger']['memory_bound'],0)

    def test_no_C_stops_converting_once_the_endowment_expires(self):
        r=ac10.run(7,0,'no_C',ticks=1024)
        self.assertEqual(r['ledger']['C_birth'],0)
        self.assertEqual(r['ledger']['converted'],ac10.run(7,0,'no_C',ticks=200)['ledger']['converted'])
        k=ac10.run(7,0,'keep',ticks=1024)
        self.assertGreater(k['ledger']['C_birth'],0)
        self.assertGreater(k['ledger']['converted'],r['ledger']['converted'])

    def test_no_B_never_produces_boundary(self):
        r=ac10.run(7,0,'no_B',ticks=1024); k=ac10.run(7,0,'keep',ticks=1024)
        self.assertEqual(r['ledger']['B_birth'],0); self.assertGreater(k['ledger']['B_birth'],0)
        self.assertEqual(k['final_inventory'][4],20)
        self.assertGreater(r['ledger']['particle_export'],0)
        self.assertEqual(k['ledger']['particle_export'],0)

    def test_permeant_loses_constituents_while_keep_retains_them(self):
        r=ac10.run(7,0,'permeant',ticks=1024)
        self.assertGreater(r['ledger']['particle_export'],0)
        self.assertEqual(ac10.run(7,0,'keep',ticks=1024)['ledger']['particle_export'],0)


class RetentionSubstitution(unittest.TestCase):
    def test_forced_retention_preserves_function_with_no_boundary_matter(self):
        r=ac10.run(7,0,'no_B_retention',ticks=2048); k=ac10.run(7,0,'keep',ticks=2048)
        self.assertEqual(r['ledger']['B_birth'],0)
        self.assertEqual(r['final_inventory'][4],0)      # no enclosure matter at all
        self.assertEqual(r['ledger']['particle_export'],0)
        self.assertEqual(r['completed'],True)
        self.assertEqual(r['routes'],k['routes'])

    def test_external_B_supply_is_an_equivalent_substitute(self):
        r=ac10.run(7,0,'B_rescue',ticks=2048); k=ac10.run(7,0,'keep',ticks=2048)
        self.assertEqual(r['ledger']['B_birth'],0)
        self.assertGreater(r['ledger']['external_B'],0)   # supplied, never produced
        self.assertEqual(r['final_inventory'][4],20)
        self.assertEqual(r['ledger']['particle_export'],0)
        self.assertEqual(r['routes'],k['routes'])


class LateOnset(unittest.TestCase):
    def test_late_arms_produce_only_before_onset(self):
        for arm,key in (('no_W_late','W_birth'),('no_B_late','B_birth')):
            r=ac10.run(7,0,arm,ticks=1024)
            self.assertGreater(r['ledger'][key]-r['assay'][key],0,arm)
            self.assertEqual(r['assay'][key],0,arm)

    def test_continuous_arms_never_produce(self):
        self.assertEqual(ac10.run(7,0,'no_W',ticks=1024)['ledger']['W_birth'],0)
        self.assertEqual(ac10.run(7,0,'no_B',ticks=1024)['ledger']['B_birth'],0)


class Integrity(unittest.TestCase):
    def erase(self,seed):
        o=ac10.v2.acquire(seed)
        o.body.traces[:]=0; o.body.life[:]=0; o.body.pos[:]=0; o.body.boundary[:]=0
        o.body.energy=64; o.body.material=128; o.body.fuel=32; o.body.dead=False
        o.memory.bits[:]=0; o.memory.life[:]=0
        return o

    def test_complete_erasure_noninterference(self):
        for arm in ac10.ARMS:
            a,b=self.erase(0),self.erase(1)
            self.assertEqual(a.digest(),b.digest(),arm)
            pre,_=ac10.build(arm); core,noise,d,coin=inputs(a)
            ea=pre(a,core,noise,d,coin,(1,1),[True,False],True)
            eb=pre(b,core,noise,d,coin,(1,1),[True,False],True)
            self.assertEqual(ea,eb,arm); self.assertEqual(a.digest(),b.digest(),arm)

    def test_ablations_do_not_change_the_acquired_program_field(self):
        """The acquired program is in traces[0,:126]; ablations touch other matter."""
        for arm in ac10.ARMS:
            o=ac10.v2.acquire(3)
            before=o.body.traces[0,:126].copy()
            pre,_=ac10.build(arm); core,noise,d,coin=inputs(o)
            pre(o,core,noise,d,coin,(1,1),[True,False],True)
            np.testing.assert_array_equal(o.body.traces[0,:126],before,arm)

    def test_exact_replay(self):
        for arm in ac10.ARMS:
            self.assertEqual(ac10.run(9,1,arm,ticks=300),ac10.run(9,1,arm,ticks=300),arm)

    def test_mapped_arms_draw_the_same_exogenous_stream(self):
        """Arms differ only in physics: identical setup and identical draws."""
        for arm in ac10.ARMS:
            self.assertEqual(ac10.run(5,0,arm,ticks=1)['mapping'],
                             ac10.run(5,0,'keep',ticks=1)['mapping'],arm)


if __name__=='__main__': unittest.main()
