import json
import unittest
import numpy as np
import ac9
import ac12
import ac13
import ac4


def planted(seed=0):
    """An AC13 organism with a readable entry for key 1 in region 0, slot 1."""
    o,offs=ac12.acquire(seed)
    o.memory.bits[0,1]=np.array([1,1,0],dtype=np.uint8)[:,None]
    o.memory.life[0,1]=64
    return o,offs


def alloc_for(arm,o,offs,seed=0,history=0):
    a=ac12.Alloc(arm,seed,history); a.offs=offs; a.shadow=o.body.traces[0].copy()
    return a


def unproductive(a,o,key,n):
    e=ac9.event()
    for _ in range(n): a.outcome(o,key,e)
    return e


class FrozenBehaviour(unittest.TestCase):
    def test_preserve_reproduces_the_frozen_rows_in_the_inert_world(self):
        """Ports 2, frozen yields, no intervention: preserve must equal AC9 v2."""
        ac12.PORTS=2; ac12.YIELD_M=64; ac12.YIELD_F=32
        ac12.POST_YIELD_M=None; ac12.MOVE_KEYS=(); ac12.MOVE_MODE='flip'
        try:
            frozen={}
            with open('ac9_priority_results_v2/results.json') as f:
                for r in json.load(f)['rows']:
                    if r['variant']=='priority': frozen[(r['seed'],r['history'])]=r
            keys=['seed','history','ticks','mapping','activity','completed','routes',
                  'demand','ledger','final_inventory','state_hash']
            for seed in (1100,1102):
                for h in (0,1):
                    live=json.loads(json.dumps(ac12.run(seed,h,'preserve')))
                    for k in keys: self.assertEqual(live[k],frozen[(seed,h)][k],f'{seed}/{h}/{k}')
        finally:
            ac13.apply_world()

    def test_register_cannot_make_the_dead_rule_fire(self):
        """The register lives in a rule whose mask needs a never-set observation bit."""
        o,offs=planted()
        for off in offs: o.body.traces[0,off]=1
        seen=set()
        rng=np.random.default_rng([0,1509])
        for t in range(600):
            core=(rng.random((126,7))<.0001).astype(np.uint8)
            noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
            seen.add(ac9.observe(o))
            ac9.step(o,core,noise,rng.integers(0,4,20,dtype=np.uint8),False,(0,0),[t<512]*2,t<512)
            if o.body.dead: break
        self.assertFalse(any(v & ac12.DEAD_MASK for v in seen))


class VulnerablePaidState(unittest.TestCase):
    def test_drop_lands_in_the_program_bank_and_is_paid_per_replica(self):
        o,offs=planted(); a=alloc_for('allocate',o,offs)
        before=(o.body.energy,o.body.material)
        e=unproductive(a,o,1,ac12.STREAK_N)
        self.assertEqual([tuple(x) for x in a.log['dropped']],[(0,1)])
        self.assertTrue(ac12.bit_value(o,offs[1]))                 # written
        self.assertFalse(ac12.bit_value(o,offs[0]))                # other slot untouched
        self.assertEqual(o.body.energy,before[0]-7)                # one per replica
        self.assertEqual(o.body.material,before[1]-7)
        self.assertEqual(e['writes'],7)

    def test_streak_resets_on_a_productive_contact(self):
        o,offs=planted(); a=alloc_for('allocate',o,offs)
        e=ac9.event()
        for _ in range(ac12.STREAK_N-1): a.outcome(o,1,e)
        e['productive']=0
        a.outcome(o,0,e)                                            # productive, other key
        a.streak[1]=0
        for _ in range(ac12.STREAK_N-1): a.outcome(o,1,e)
        self.assertFalse(a.log['dropped'])

    def test_drop_is_gated_by_the_frozen_w_economy(self):
        o,offs=planted(); a=alloc_for('allocate',o,offs)
        o.body.life[:4]=0                                           # no core W to pay with
        unproductive(a,o,1,ac12.STREAK_N*3)
        self.assertFalse(a.log['dropped'])
        self.assertFalse(ac12.bit_value(o,offs[1]))

    def test_sham_write_pays_but_does_not_change_the_register(self):
        o,offs=planted(); a=alloc_for('no_learning',o,offs)
        before=(o.body.energy,o.body.material)
        e=unproductive(a,o,1,ac12.STREAK_N)
        self.assertTrue(a.log['dropped'])                           # attempt recorded
        self.assertFalse(ac12.bit_value(o,offs[1]))                 # sham: unchanged
        self.assertEqual((o.body.energy,o.body.material),(before[0]-7,before[1]-7))

    def test_protected_keeps_the_decision_out_of_the_body(self):
        o,offs=planted(); a=alloc_for('protected',o,offs)
        unproductive(a,o,1,ac12.STREAK_N)
        self.assertTrue(a.log['dropped'])
        self.assertFalse(ac12.bit_value(o,offs[1]))                 # body register intact
        self.assertTrue(bool(a.shadow[offs[1]][0]))                 # shadow holds it


class TheIntervention(unittest.TestCase):
    def test_worthlessness_is_not_harmful(self):
        """For a surviving organism, the stored value stops earning more than blind
        search, yet still earns blind-rate income rather than nothing."""
        ac13.apply_world()
        r=ac12.run(1600,0,'preserve')
        def prod(p):
            l=r['phases'][p]; return l['productive']/max(1,l['contacts'])
        self.assertGreater(prod(1),0.90)          # worth its cost while valid
        self.assertLess(prod(2),0.45)             # worthless after the intervention
        self.assertGreater(prod(2),0.15)          # but not harmful: income continues

    def test_the_route_is_required_before_the_intervention(self):
        ac13.apply_world()
        def p1(arm,ticks=1024):
            r=ac12.run(1600,0,arm,ticks=ticks)
            l=r['phases'][1]
            return l['productive']/max(1,l['contacts'])
        self.assertGreater(p1('preserve'),0.90)
        self.assertLess(p1('relinquish'),0.40)


class Integrity(unittest.TestCase):
    def check_ledger(self,row):
        l=row['ledger']; inv=row['final_inventory']
        m0=128+24+40+l['in_m']+2*l['external_B']
        m1=inv[1]+4*inv[3]+2*inv[4]+sum(row['demand'])
        spent=l['writes']-l['memory_writes']
        losses=(l['memory_waste']+l['memory_expiry']+
                4*(l['particle_expiry']+l['particle_export'])+
                2*(l['B_expiry']+l['B_discard'])+l['overflow_m'])
        self.assertEqual(m0,m1+spent+losses,(row['seed'],row['arm']))
        self.assertEqual(64+8*l['converted'],inv[0]+l['spent_e'],row['arm'])
        self.assertEqual(32+l['in_f'],inv[2]+l['overflow_f']+l['converted'],row['arm'])

    def test_ledger_identities_hold_for_every_arm(self):
        ac13.apply_world()
        for arm in ac13.ARMS:
            self.check_ledger(ac12.run(1600,0,arm,ticks=400))

    def erase(self,seed):
        o,_=ac12.acquire(seed)
        o.body.traces[:]=0; o.body.life[:]=0; o.body.pos[:]=0; o.body.boundary[:]=0
        o.body.energy=64; o.body.material=128; o.body.fuel=32; o.body.dead=False
        o.memory.bits[:]=0; o.memory.life[:]=0
        return o

    def test_complete_erasure_noninterference(self):
        ac13.apply_world()
        for arm in ac13.ARMS:
            a,b=self.erase(0),self.erase(1)
            aa=ac12.Alloc(arm,0,0); aa.offs=ac12.acquire(0)[1]; aa.shadow=a.body.traces[0].copy()
            ab=ac12.Alloc(arm,1,0); ab.offs=ac12.acquire(1)[1]; ab.shadow=b.body.traces[0].copy()
            sa=ac12.build(arm,aa); sb=ac12.build(arm,ab)
            self.assertEqual(a.digest(),b.digest(),arm)
            inputs=(np.zeros((126,7),dtype=np.uint8),np.zeros_like(a.memory.bits),
                    np.zeros(20,dtype=int),False,(1,1),[True,False])
            ea=sa(a,*inputs,True); eb=sb(b,*inputs,True)
            self.assertEqual(ea,eb,arm); self.assertEqual(a.digest(),b.digest(),arm)

    def test_exact_replay(self):
        ac13.apply_world()
        for arm in ac13.ARMS:
            self.assertEqual(ac12.run(1601,1,arm,ticks=300),ac12.run(1601,1,arm,ticks=300),arm)


if __name__=='__main__': unittest.main()
