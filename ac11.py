"""AC11: acquired allocation of preservation spending under a post-development port move.

One bounded organism decides whether to keep paying for its acquired access
capability. The decision is stored in the vulnerable, repairable program bank
(the enabled bit of the region's renewal rule) and is revised by the organism's
own realized contact outcomes through paid writes. The world is the declared
AC11 regime: a blind port space of four, material and fuel yields of 16, and an
unannounced port move at tick 1024.

`preserve` calls the frozen functions themselves apart from the declared world
constants (yields), and is checked row-for-row against the frozen AC9 v2 rows.
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
from ac1 import decode

ARMS=('adaptive','preserve','relinquish','fixed_schedule','random','protected','no_learning')

# Declared world constants (AC11_PROTOCOL_v1.md). Everything else is frozen.
PORTS=4
YIELD_M=16
YIELD_F=16
TICKS=2048
DEV=512
MOVE=1024
MOVE_KEYS=(1,)   # ports relabelled by the post-development intervention
STREAK_N=8        # consecutive unproductive contacts for one key before relinquishing
FIXED_PERIOD=2    # renewal opportunities skipped by the spending-matched schedule
RANDOM_P=0.5      # renewal probability for the random-allocator rival

STEP_SRC=inspect.getsource(ac9.step)
REACT_SRC=inspect.getsource(ac4.react)
OUTCOME_LINE="            e['contacts']=1; e['productive']=int(e['in_m']+e['in_f']>0)"
RENEW_GUARD="            if r!=blocked:"
IN_F_LINE="        e['in_f']=32; e['overflow_f']=max(0,b.fuel+32-64); b.fuel=min(64,b.fuel+32)"
IN_M_LINE="        e['in_m']=64; e['overflow_m']=max(0,b.material+64-256); b.material=min(256,b.material+64)"


def react_world():
    """The frozen reaction law with the declared AC11 yields."""
    if (YIELD_M,YIELD_F)==(64,32): return ac4.react
    src=REACT_SRC
    if YIELD_F!=32:
        assert src.count(IN_F_LINE)==1,'unexpected react text (fuel yield)'
        src=src.replace(IN_F_LINE,f"        e['in_f']={YIELD_F}; e['overflow_f']=max(0,b.fuel+{YIELD_F}-64); b.fuel=min(64,b.fuel+{YIELD_F})")
    if YIELD_M!=64:
        assert src.count(IN_M_LINE)==1,'unexpected react text (material yield)'
        src=src.replace(IN_M_LINE,f"        e['in_m']={YIELD_M}; e['overflow_m']=max(0,b.material+{YIELD_M}-256); b.material=min(256,b.material+{YIELD_M})")
    fns={}
    exec(compile(src,'ac11_react','exec'),dict(vars(ac4)),fns)
    return fns['react']


def renewal_rule_offset(o,r):
    """Bit offset of the enabled bit of the rule that renews region r."""
    bits=decode(o.body.traces[0,:126]).reshape(9,14)
    word=(bits*(1<<np.arange(14))).sum(axis=1)
    idx=np.flatnonzero(((word>>10)&15)==(3+r))
    return int(14*int(idx[0])) if len(idx) else None


def choose_with_shadow(traces,observation,shadow):
    t=traces.copy(); t[0,:126]=shadow[:126]
    return prog.choose(t,observation)


class Alloc:
    """The organism's allocation machinery for one arm and one individual.

    Declared supplied machinery: the unproductive streak is input state derived
    from the organism's own realized contact outcomes (it records experience, not
    the answer). The decision itself -- whether the region's renewal rule stays
    enabled -- lives in the vulnerable program bank except in the `protected`
    scaffold arm.
    """
    def __init__(self,arm,seed,history):
        assert arm in ARMS,arm
        self.arm=arm
        self.streak={0:0,1:0}
        self.relinquished=False
        self.opportunities=0
        self.rng=np.random.default_rng([seed,history,11011])   # declared auxiliary stream
        self.shadow=None
        self.log=dict(relinquish_tick=None,relinquish_writes=0,streaks={})

    def renew_allowed(self,r,o,e):
        self.opportunities+=1
        if self.arm=='relinquish': return False
        if self.arm=='fixed_schedule': return (self.opportunities % FIXED_PERIOD)==0
        if self.arm=='random': return bool(self.rng.random()<RANDOM_P)
        return True

    def outcome(self,o,key,e):
        if self.relinquished: return
        self.streak[int(key)]=0 if e['productive']>0 else self.streak[int(key)]+1
        if self.streak[int(key)]>=STREAK_N: self._try_relinquish(o,e)

    def _try_relinquish(self,o,e):
        demand=o.memory.demand(); r=int(np.argmax(demand))
        if int(demand[r])==0: return
        off=renewal_rule_offset(o,r)
        if off is None: return
        sites=o.body.traces[0,off]                     # seven replicas of the enabled bit
        n=int((sites!=0).sum())
        cap=min(32,8*int(ac4.available(o.body)[:4].sum()),o.body.energy,o.body.material)
        if n>cap: return                               # unaffordable; try again next tick
        o.body.energy-=n; o.body.material-=n
        e['spent_e']+=n; e['spent_m']+=n; e['writes']+=n
        if self.arm=='protected': self.shadow[0,off]=0
        elif self.arm=='no_learning': pass             # paid, not written (sham)
        else: sites[:]=0                               # vulnerable maintained write
        self.relinquished=True
        self.log['relinquish_tick']=None                # filled by the runner
        self.log['relinquish_writes']=n


def build(arm,alloc):
    src=STEP_SRC; ns=dict(vars(ac9))
    if arm in ('adaptive','protected','no_learning'):
        assert src.count(OUTCOME_LINE)==1,'unexpected step text (contact outcome)'
        src=src.replace(OUTCOME_LINE,OUTCOME_LINE+"\n            alloc.outcome(o,action,e)")
        ns['alloc']=alloc
    if arm in ('relinquish','fixed_schedule','random'):
        assert src.count(RENEW_GUARD)==1,'unexpected step text (renew guard)'
        src=src.replace(RENEW_GUARD,"            if r!=blocked and alloc.renew_allowed(r,o,e):")
        ns['alloc']=alloc
    if (YIELD_M,YIELD_F)!=(64,32):
        shim={k:getattr(ac4,k) for k in dir(ac4) if not k.startswith('_')}
        shim['react']=react_world(); ns['ac4']=SimpleNamespace(**shim)
    if arm=='protected':
        shadow=alloc.shadow
        ns['prog']=SimpleNamespace(choose=lambda tr,ob: choose_with_shadow(tr,ob,shadow))
    fns={}
    exec(compile(src,'ac11_step','exec'),ns,fns)
    return fns['step']


def event():
    e=ac9.event(); e.update(relinquish_writes=0); return e


def run(seed,history,arm,ticks=TICKS):
    alloc=Alloc(arm,seed,history)
    o=v2.acquire(seed)
    alloc.shadow=o.body.traces[0].copy()
    step=build(arm,alloc)
    base=(seed%2,(seed//2)%2)
    rng=np.random.default_rng([seed,1509])
    total=event(); phases=[event() for _ in range(3)]
    first_dead=None
    for t in range(ticks):
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        coin=int(rng.integers(0,PORTS))
        activation=[history==r for r in range(2)] if t<DEV else [True,True]
        mapping=list(base)
        if t>=MOVE:
            for k in MOVE_KEYS: mapping[k]=1-base[k]
        e=step(o,core,noise,directions,coin,tuple(mapping),activation,t<DEV)
        for k in total: total[k]+=e.get(k,0)
        p=0 if t<DEV else 1 if t<MOVE else 2
        for k in phases[p]: phases[p][k]+=e.get(k,0)
        if alloc.relinquished and alloc.log['relinquish_tick'] is None:
            alloc.log['relinquish_tick']=t
        if first_dead is None and o.body.dead: first_dead=t
    alloc.log['streaks']={str(k):int(v) for k,v in alloc.streak.items()}
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,mapping=base,
                move_keys=list(MOVE_KEYS),
                activity=total['active']/ticks,completed=total['active']==ticks,
                first_dead=first_dead,routes=[o.memory.read(k) for k in (0,1)],
                demand=o.memory.demand().tolist(),occupied_sites=int(o.memory.occupied().sum()),
                relocated=alloc.relinquished,alloc=alloc.log,
                ledger=total,phases=phases,final_inventory=ac4.inventory(o.body),
                state_hash=o.digest())


NAMES=['ac11.py','ac9.py','ac9_priority_v2.py','ac9_memory.py','ac5.py','ac5_program.py',
       'ac4.py','ac4_transport.py','ac1.py','test_ac11.py','AC11_PROTOCOL_v1.md']


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
                 r['relocated'],r['alloc']['relinquish_tick']) for r in rows[-2*len(ARMS):]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac11_engineering_v1',[0,1,2]); return
    collect('ac11_results_v1',[1400,1401,1402,1403])


if __name__=='__main__': main()
