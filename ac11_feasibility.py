"""AC11 feasibility (ENGINEERING ONLY — no final claim).

Two questions must be settled before an AC11 protocol can be written honestly:

F1. In the frozen AC9 world, is relinquishing the acquired memory (suppressing
    its paid renewal) at least as viable as maintaining it? If yes, "never
    maintain" dominates and a relinquishment study would be vacuous.
F2. Does a declared world change — a blind port space wider than the one bit an
    entry can encode, plus reduced resource yields — produce a regime where
    maintaining the route is necessary while the port is live AND relinquishing
    it is necessary after an unannounced port move?

Interventions are asserted source surgery on the frozen `ac9.step` / `ac4.react`
text; the maintain arm calls the frozen functions themselves. Engineering seeds
only; excluded from any later confirmatory sample.
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

STEP_SRC=inspect.getsource(ac9.step)
REACT_SRC=inspect.getsource(ac4.react)
RENEW_GUARD="            if r!=blocked:"
IN_F_LINE="        e['in_f']=32; e['overflow_f']=max(0,b.fuel+32-64); b.fuel=min(64,b.fuel+32)"
IN_M_LINE="        e['in_m']=64; e['overflow_m']=max(0,b.material+64-256); b.material=min(256,b.material+64)"


def react_world(yield_m=64,yield_f=32):
    """The frozen reaction law with declared world yields."""
    if (yield_m,yield_f)==(64,32): return ac4.react
    src=REACT_SRC
    if yield_f!=32:
        assert src.count(IN_F_LINE)==1
        src=src.replace(IN_F_LINE,f"        e['in_f']={yield_f}; e['overflow_f']=max(0,b.fuel+{yield_f}-64); b.fuel=min(64,b.fuel+{yield_f})")
    if yield_m!=64:
        assert src.count(IN_M_LINE)==1
        src=src.replace(IN_M_LINE,f"        e['in_m']={yield_m}; e['overflow_m']=max(0,b.material+{yield_m}-256); b.material=min(256,b.material+{yield_m})")
    fns={}
    exec(compile(src,'ac11_react','exec'),dict(vars(ac4)),fns)
    return fns['react']


def build(maintain=True,yield_m=64,yield_f=32):
    """Step function. maintain=False suppresses the paid renewal of the entries."""
    src=STEP_SRC; ns=dict(vars(ac9))
    if not maintain:
        assert src.count(RENEW_GUARD)==1,'unexpected step text (renew guard)'
        src=src.replace(RENEW_GUARD,"            if False:")
    if (yield_m,yield_f)!=(64,32):
        shim={k:getattr(ac4,k) for k in dir(ac4) if not k.startswith('_')}
        shim['react']=react_world(yield_m,yield_f); ns['ac4']=SimpleNamespace(**shim)
    fns={}
    exec(compile(src,'ac11_step','exec'),ns,fns)
    return fns['step']


def run(seed,history,maintain,phase2,ports=2,yield_m=64,yield_f=32,ticks=2048,
        onset=512,move_key=1):
    """phase2: 'open' keeps the mapping; 'moved' flips move_key's port at onset."""
    step=build(maintain,yield_m,yield_f)
    o=v2.acquire(seed)
    base=(seed%2,(seed//2)%2)
    rng=np.random.default_rng([seed,1509])
    total=ac9.event(); late=ac9.event()
    first_dead=None
    for t in range(ticks):
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        coin=int(rng.integers(0,ports))
        activation=[history==r for r in range(2)] if t<onset else [True,True]
        mapping=list(base)
        if t>=onset and phase2=='moved': mapping[move_key]=1-base[move_key]
        e=step(o,core,noise,directions,coin,tuple(mapping),activation,t<onset)
        for k in total: total[k]+=e[k]
        if t>=onset:
            for k in late: late[k]+=e[k]
        if first_dead is None and o.body.dead: first_dead=t
    return dict(seed=seed,history=history,maintain=maintain,phase2=phase2,ports=ports,
                yield_m=yield_m,yield_f=yield_f,ticks=ticks,onset=onset,
                activity=total['active']/ticks,completed=total['active']==ticks,
                first_dead=first_dead,routes=[o.memory.read(k) for k in (0,1)],
                occupied_sites=int(o.memory.occupied().sum()),
                late_productivity=late['productive']/max(1,late['contacts']),
                total_productivity=total['productive']/max(1,total['contacts']),
                ledger=total,late=late,final_inventory=ac4.inventory(o.body),
                state_hash=o.digest())


GRID=[]
for seed in (0,1):
    for maintain in (True,False):                 # maintain vs relinquish
        for phase2 in ('open','moved'):
            GRID.append(dict(seed=seed,history=0,maintain=maintain,phase2=phase2))   # F1: frozen world
for yield_m in (32,16,8):                          # F2: declared world changes
    for seed in (0,1):
        for maintain in (True,False):
            for phase2 in ('open','moved'):
                GRID.append(dict(seed=seed,history=0,maintain=maintain,phase2=phase2,
                                 ports=4,yield_m=yield_m,yield_f=16))


def main():
    root=Path('ac11_feasibility_v1'); root.mkdir(exist_ok=False)
    names=[n for n in ('ac11_feasibility.py','ac9.py','ac9_priority_v2.py','ac9_memory.py',
                       'ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py')
           if Path(n).exists()]
    (root/'pre_run_snapshot.json').write_text(json.dumps(
        {n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names},indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for cfg in GRID:
            r=run(**cfg); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
    (root/'results.json').write_text(json.dumps(dict(kind='engineering_feasibility',
                                                    rows=rows),indent=2))
    print(f"{'ports':>5} {'yM':>3} {'yF':>3} {'maintain':>8} {'phase2':>6} | "
          f"{'act':>6} {'alive':>5} {'dead@':>6} {'prod1st':>8} {'prod2nd':>8} "
          f"{'renWr':>6} {'in_m':>6} {'occ':>4}")
    for cfg in GRID:
        rs=[r for r in rows if r['ports']==cfg.get('ports',2)
            and r['yield_m']==cfg.get('yield_m',64) and r['yield_f']==cfg.get('yield_f',32)
            and r['seed']==cfg['seed'] and r['maintain']==cfg['maintain']
            and r['phase2']==cfg['phase2']]
        for r in rs:
            print(f"{r['ports']:5} {r['yield_m']:3} {r['yield_f']:3} {str(r['maintain']):>8} "
                  f"{r['phase2']:>6} | {r['activity']:6.3f} {str(r['completed'])[0]:>5} "
                  f"{str(r['first_dead']):>6} {r['total_productivity']:8.3f} "
                  f"{r['late_productivity']:8.3f} {r['ledger']['memory_writes']:6d} "
                  f"{r['ledger']['in_m']:6d} {r['occupied_sites']:4d}")


if __name__=='__main__': main()
