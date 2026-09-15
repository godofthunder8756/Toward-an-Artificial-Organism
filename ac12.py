"""AC12: can maintenance be allocated per acquired entry?

AC11 failed because the frozen renewal primitive is region-granular while the
usefulness boundary is per-key. AC12 supplies the missing granularity
(`ac12_memory.renew_alloc`, capacity shared exactly as the frozen law shares it)
and asks the same question again:

    after an unannounced post-development relabelling makes ONE acquired entry
    stale, can an organism whose per-slot maintenance allocation is stored in its
    own vulnerable, repairable program bank and revised by its own realized
    contact outcomes keep maintaining the still-valid entry while relinquishing
    the stale one, and remain viable where state-blind allocation does not?

The allocation register lives in the nine mask bits of the frozen program's
permanently dead rule -- the bank rule whose mask is 32, which `ac9.observe`
can never set because it never sets observation bit 5. Disabling that rule is
behaviourally identical to the frozen program, so the organism, its economy and
its viability are the frozen ones; only the granularity of the renewal decision
is new. The eight bits actually used are four (region, slot) allocation bits,
each stored as seven replicas inside `traces[0,:126]`, flipped by the same damage
stream and repaired only by the same paid bank-0 repair as everything else.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import inspect
import json
import sys
import numpy as np
import ac9
import ac9_priority_v2 as v2
import ac4
import ac5_program as prog
import ac12_memory as m12
from ac1 import decode

ARMS=('allocate','preserve','relinquish','fixed_schedule','random','protected','no_learning')

PORTS=4
YIELD_M=16
YIELD_F=16
TICKS=2048
DEV=512
MOVE=1024
MOVE_KEYS=(1,)
STREAK_N=6
FIXED_PERIOD=2
RANDOM_P=0.5
DEAD_MASK=32          # the mask `ac9.observe` can never produce
REGISTER_SLOTS=((0,0),(0,1),(1,0),(1,1))

STEP_SRC=inspect.getsource(ac9.step)
REACT_SRC=inspect.getsource(ac4.react)
OUTCOME_LINE="            e['contacts']=1; e['productive']=int(e['in_m']+e['in_f']>0)"
RENEW_BLOCK=("            if r!=blocked:\n"
             "                result=mem.renew(o.memory,b,r,int(a[4*(r+1):4*(r+2)].sum()))\n"
             "                memory_charge(e,result)")
RENEW_BLOCK_NEW=("            if r!=blocked:\n"
                 "                result=ac12_memory.renew_alloc(o.memory,b,r,"
                 "int(a[4*(r+1):4*(r+2)].sum()),allowance(o,r))\n"
                 "                memory_charge(e,result)")
IN_F_LINE="        e['in_f']=32; e['overflow_f']=max(0,b.fuel+32-64); b.fuel=min(64,b.fuel+32)"
IN_M_LINE="        e['in_m']=64; e['overflow_m']=max(0,b.material+64-256); b.material=min(256,b.material+64)"


def dead_rule_index(o):
    """Index of the frozen program's dead bank rule (mask 32). Deterministic."""
    bits=decode(o.body.traces[0,:126]).reshape(9,14)
    word=(bits*(1<<np.arange(14))).sum(axis=1)
    mask=(word>>1)&511
    idx=np.flatnonzero(mask==DEAD_MASK)
    assert len(idx)==1,f'expected exactly one dead rule, found {len(idx)}'
    return int(idx[0])


def register_offsets(o):
    """Bit offsets of the four (region,slot) allocation bits, in the dead rule."""
    base=14*dead_rule_index(o)
    return [base+1+k for k in range(4)]     # mask bits 1..4 of the dead rule


def acquire(seed):
    """Install the AC12 organism: the frozen program, byte for byte.

    The allocation register occupies mask bits 1-4 of the frozen program's
    permanently dead rule (mask 32), which `ac9.observe` can never match because
    it never sets observation bit 5. Those bits are zero in the frozen program, so
    a zero register means "maintain every slot" and the acquired organism is
    identical to the frozen one. Setting a bit cannot make the dead rule live,
    because its mask still requires observation bit 5, which is never set. The
    offsets are resolved once here, from the pristine program.
    """
    o=v2.acquire(seed)
    idx=dead_rule_index(o)
    return o,[14*idx+1+k for k in range(4)]


def bit_value(o,off): return bool(decode(o.body.traces[0,off:off+1])[0])


def react_world():
    if (YIELD_M,YIELD_F)==(64,32): return ac4.react
    src=REACT_SRC
    if YIELD_F!=32:
        assert src.count(IN_F_LINE)==1
        src=src.replace(IN_F_LINE,f"        e['in_f']={YIELD_F}; e['overflow_f']=max(0,b.fuel+{YIELD_F}-64); b.fuel=min(64,b.fuel+{YIELD_F})")
    if YIELD_M!=64:
        assert src.count(IN_M_LINE)==1
        src=src.replace(IN_M_LINE,f"        e['in_m']={YIELD_M}; e['overflow_m']=max(0,b.material+{YIELD_M}-256); b.material=min(256,b.material+{YIELD_M})")
    fns={}
    exec(compile(src,'ac12_react','exec'),dict(vars(ac4)),fns)
    return fns['react']


class Alloc:
    """Per-slot maintenance allocation for one arm and one individual.

    Declared supplied machinery: the unproductive streak is input derived from
    the organism's own realized contact outcomes (experience, not the answer).
    The allocation itself -- which slots stay maintained -- is the register bits
    in the body's program bank except in the `protected` scaffold arm.
    """
    def __init__(self,arm,seed,history):
        assert arm in ARMS,arm
        self.arm=arm
        self.streak={0:0,1:0}
        self.opportunities=0
        self.rng=np.random.default_rng([seed,history,12012])
        self.shadow=None                 # protected copy of the whole program bank
        self.offs=None                   # register offsets, resolved at acquisition
        self.log=dict(relinquish_tick=None,dropped=[])

    def allowance(self,o,region):
        offs=self.offs
        def read(slot):
            """Register bit set means this slot has been relinquished."""
            bit=2*region+slot
            if self.arm=='preserve': return True
            if self.arm=='relinquish': return False
            if self.arm=='protected': return not bool(self.shadow[offs[bit]][0])
            return not bit_value(o,offs[bit])
        if self.arm=='fixed_schedule':
            self.opportunities+=1
            on=(self.opportunities % FIXED_PERIOD)==0
            return (on,on)
        if self.arm=='random':
            self.opportunities+=1
            return (bool(self.rng.random()<RANDOM_P),bool(self.rng.random()<RANDOM_P))
        return (read(0),read(1))

    def outcome(self,o,key,e):
        if self.arm not in ('allocate','protected','no_learning'): return
        self.streak[int(key)]=0 if e['productive']>0 else self.streak[int(key)]+1
        if self.streak[int(key)]>=STREAK_N: self._drop(o,e,int(key))

    def _drop(self,o,e,key):
        place=m12.slot_of_key(o.memory,key)
        if place is None: return
        off=self.offs[2*place[0]+place[1]]
        sites=self.shadow[off] if self.arm=='protected' else o.body.traces[0,off]
        n=int((sites!=1).sum())
        if n==0: return
        cap=min(32,8*int(ac4.available(o.body)[:4].sum()),o.body.energy,o.body.material)
        if n>cap: return
        o.body.energy-=n; o.body.material-=n
        e['spent_e']+=n; e['spent_m']+=n; e['writes']+=n
        if self.arm=='protected': self.shadow[off]=1
        elif self.arm=='no_learning': pass          # paid, not written (sham)
        else: sites[:]=1                            # vulnerable maintained write
        self.streak[key]=0
        self.log['dropped'].append(list(place))


def build(arm,alloc):
    src=STEP_SRC; ns=dict(vars(ac9))
    assert src.count(RENEW_BLOCK)==1,'unexpected step text (renewal block)'
    src=src.replace(RENEW_BLOCK,RENEW_BLOCK_NEW)
    ns['ac12_memory']=m12; ns['allowance']=alloc.allowance
    if arm in ('allocate','protected','no_learning'):
        assert src.count(OUTCOME_LINE)==1,'unexpected step text (contact outcome)'
        src=src.replace(OUTCOME_LINE,OUTCOME_LINE+"\n            alloc.outcome(o,action,e)")
        ns['alloc']=alloc
    if (YIELD_M,YIELD_F)!=(64,32):
        shim={k:getattr(ac4,k) for k in dir(ac4) if not k.startswith('_')}
        shim['react']=react_world(); ns['ac4']=SimpleNamespace(**shim)
    if arm=='protected':
        shadow=alloc.shadow
        ns['prog']=SimpleNamespace(choose=lambda tr,ob: choose_with_shadow(tr,ob,shadow))
    fns={}
    exec(compile(src,'ac12_step','exec'),ns,fns)
    return fns['step']


def choose_with_shadow(traces,observation,shadow):
    t=traces.copy(); t[0,:126]=shadow[:126]
    return prog.choose(t,observation)


def run(seed,history,arm,ticks=TICKS):
    alloc=Alloc(arm,seed,history)
    o,offs=acquire(seed)
    alloc.offs=offs                         # resolved once, before any damage
    alloc.shadow=o.body.traces[0].copy()
    step=build(arm,alloc)
    base=(seed%2,(seed//2)%2)
    rng=np.random.default_rng([seed,1509])
    total=ac9.event(); phases=[ac9.event() for _ in range(3)]
    first_dead=None
    for t in range(ticks):
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        coin=bool(rng.random()<.5) if PORTS==2 else int(rng.integers(0,PORTS))
        activation=[history==r for r in range(2)] if t<DEV else [True,True]
        mapping=list(base)
        if t>=MOVE:
            for k in MOVE_KEYS: mapping[k]=1-base[k]
        e=step(o,core,noise,directions,coin,tuple(mapping),activation,t<DEV)
        for k in total: total[k]+=e.get(k,0)
        p=0 if t<DEV else 1 if t<MOVE else 2
        for k in phases[p]: phases[p][k]+=e.get(k,0)
        if alloc.log['relinquish_tick'] is None and alloc.log['dropped']:
            alloc.log['relinquish_tick']=t
        if first_dead is None and o.body.dead: first_dead=t
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,mapping=base,
                move_keys=list(MOVE_KEYS),
                activity=total['active']/ticks,completed=total['active']==ticks,
                first_dead=first_dead,routes=[o.memory.read(k) for k in (0,1)],
                demand=o.memory.demand().tolist(),
                register=[bit_value(o,off) for off in offs],
                slots=[[m12.decoded_key(o.memory,r,s) for s in range(2)] for r in range(2)],
                alloc=alloc.log,ledger=total,phases=phases,
                final_inventory=ac4.inventory(o.body),state_hash=o.digest())


NAMES=['ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py','ac9_memory.py','ac5.py',
       'ac5_program.py','ac4.py','ac4_transport.py','ac1.py','test_ac12.py','AC12_PROTOCOL_v1.md']


def collect(root,seeds):
    root=Path(root); root.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in NAMES if Path(n).exists()}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0,1):
                for arm in ARMS:
                    r=run(seed,history,arm); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,outcomes=[
                (r['history'],r['arm'],round(r['activity'],3),r['completed'],
                 r['alloc']['dropped']) for r in rows[-2*len(ARMS):]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac12_engineering_v2',[0,1,2]); return
    collect('ac12_results_v1',[1500,1501,1502,1503])


if __name__=='__main__': main()
