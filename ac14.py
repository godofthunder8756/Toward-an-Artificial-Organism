"""AC14: is the organism's own decision state a maintained constraint in the loop?

The loop is physically present in the machinery AC12 built and verified:

    the allocation register (4 bits) lives inside traces[0,:126]
    -> the program bank is repaired only by the paid bank-0 repair action
    -> core interior W (group 0) is that repair's capacity
    -> core W is produced by the action-6 reaction, chosen by the program
    -> the program that contains the register

So maintenance of the decision depends on the machinery whose maintenance the
decision allocates. AC14 cuts the *repair* link and measures whether the decision
state itself degrades and whether that degradation propagates into the organism's
own decisions.

Why the repair link and not the W-supply link: blocking core-W births leaves
observation bit 6 (`low W`) permanently set, so the W rule fires every tick and the
organism does nothing else -- it dies at 251 with activity 0.123, identical to the
AC10 `no_W` arm. That measures attention hijack, not the loop. Blocking the
program-bank repair leaves the economy and the observations intact and is expressed
by a *frozen* mechanism: `ac4.react`'s existing `arm='no_policy_write'` guard, which
zeroes repair capacity for banks 0 and 1. In this organism bank 1 holds only zeroed
payload, so the guard bites exactly the program bank that carries the register.

Falsifier, recorded before running: if cutting the repair link does not degrade the
live register, or register/rules degradation does not change what the organism
maintains and does, or the protected register performs identically under the cut,
the loop is not load-bearing.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import inspect
import json
import sys
import numpy as np
import ac9
import ac12
import ac4
from ac1 import decode

ARMS=('closed','no_repair','protected_closed','protected_no_repair')

PORTS=4
YIELD_M=64
YIELD_F=64
TICKS=4096          # declared: twice the lineage standard, so unrepaired damage accumulates
DEV=512


def arm_parts(arm):
    """(ac12 base arm, cut the program-bank repair link?)"""
    return ('protected' if arm.startswith('protected') else 'allocate',
            '_no_repair' in arm)


def build(arm,alloc):
    base,cut=arm_parts(arm)
    src=ac12.STEP_SRC; ns=dict(vars(ac9))
    assert src.count(ac12.RENEW_BLOCK)==1
    src=src.replace(ac12.RENEW_BLOCK,ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory']=ac12.m12; ns['allowance']=alloc.allowance
    assert src.count(ac12.OUTCOME_LINE)==1
    src=src.replace(ac12.OUTCOME_LINE,ac12.OUTCOME_LINE+"\n            alloc.outcome(o,action,e)")
    ns['alloc']=alloc
    shim={k:getattr(ac4,k) for k in dir(ac4) if not k.startswith('_')}
    react=ac12.react_world()
    if cut:
        react=(lambda b,action,a,e,_f=react: _f(b,action,'no_policy_write',e))
    shim['react']=react; ns['ac4']=SimpleNamespace(**shim)
    if base=='protected':
        shadow=alloc.shadow
        ns['prog']=SimpleNamespace(choose=lambda tr,ob: ac12.choose_with_shadow(tr,ob,shadow))
    fns={}
    exec(compile(src,'ac14_step','exec'),ns,fns)
    return fns['step']


def run(seed,history,arm,ticks=TICKS):
    base,cut=arm_parts(arm)
    ac12.PORTS=PORTS; ac12.YIELD_M=YIELD_M; ac12.YIELD_F=YIELD_F
    ac12.POST_YIELD_M=None; ac12.MOVE_KEYS=(); ac12.MOVE=10**9
    ac12.DEV=DEV
    alloc=ac12.Alloc(base,seed,history)
    o,offs=ac12.acquire(seed)
    alloc.offs=offs
    alloc.shadow=o.body.traces[0].copy()
    installed=decode(o.body.traces[0,:126]).copy()
    step=build(arm,alloc)
    base_map=(seed%2,(seed//2)%2)
    rng=np.random.default_rng([seed,1509])
    total=ac9.event(); actions={}
    first_dead=None; first_register_flip=None; first_rule_error=None
    for t in range(ticks):
        alloc.now=t
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        coin=bool(rng.random()<.5)
        a=int(ac12.prog.choose(o.body.traces,ac9.observe(o)))
        actions[a]=actions.get(a,0)+1
        e=step(o,core,noise,directions,coin,base_map,[t<DEV]*2,t<DEV)
        for k in total: total[k]+=e.get(k,0)
        if first_register_flip is None and any(ac12.bit_value(o,off) for off in offs):
            first_register_flip=t
        if first_rule_error is None and (decode(o.body.traces[0,:126])!=installed).any():
            first_rule_error=t
        if first_dead is None and o.body.dead: first_dead=t
    dec=decode(o.body.traces[0,:126])
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,
                activity=total['active']/ticks,completed=total['active']==ticks,
                first_dead=first_dead,
                program_bits_damaged=int((dec!=installed).sum()),
                rules_touched=int(sum(1 for r in range(9)
                                      if (dec[14*r:14*r+14]!=installed[14*r:14*r+14]).any())),
                register=[ac12.bit_value(o,off) for off in offs],
                register_any_flip=any(ac12.bit_value(o,off) for off in offs),
                first_register_flip=first_register_flip,first_rule_error=first_rule_error,
                dropped=alloc.log['dropped'],actions=actions,
                demand=o.memory.demand().tolist(),occupied=int(o.memory.occupied().sum()),
                ledger=total,final_inventory=ac4.inventory(o.body),state_hash=o.digest())


NAMES=['ac14.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py','ac9_memory.py',
       'ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py',
       'test_ac14.py','AC14_PROTOCOL_v1.md']


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
                 r['program_bits_damaged'],r['rules_touched'],
                 [int(x) for x in r['register']],r['first_register_flip'])
                for r in rows[-2*len(ARMS):]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac14_engineering_v1',[0,1,2]); return
    collect('ac14_results_v1',[1700,1701,1702,1703])


if __name__=='__main__': main()
