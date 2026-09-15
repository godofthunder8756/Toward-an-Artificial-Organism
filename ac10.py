"""AC10: integrated constituent ablations in the AC9 maintained organism.

Each arm removes one produced constituent of the frozen AC9 v2 priority organism
(regional W repair catalysts, C energy converters, B enclosure), disables the
enclosure's retention function, or applies one of the two rescue mechanisms the
frozen physics already expresses (external B restoration as in AC4, forced
retention as in AC4). Interventions are implemented by asserted source surgery
on the frozen `ac9.step` and `ac4.react` text; the `keep` arm performs no surgery
and calls the frozen `ac9.step` object itself.

Every arm pays the frozen reaction prices. No external matter, energy or correct
answer is supplied, and no conservation identity is modified.
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
import ac4_transport as tr
from ac1 import decode

ARMS=('keep','no_W','no_C','no_B','permeant','no_B_retention','B_rescue',
      'no_W_late','no_B_late')
LATE=('no_W_late','no_B_late')
ONSET=512

STEP_SRC=inspect.getsource(ac9.step)
REACT_SRC=inspect.getsource(ac4.react)

B_EXPIRY_LINE="    e['B_expiry']=int((b.boundary==1).sum()); b.boundary[b.boundary>0]-=1"
MOVE_CALL="tr.move(b.pos,inactive,b.boundary,directions,np.ones(20,dtype=bool))"
MOVE_CALL_NEW="tr.move(b.pos,inactive,b.boundary,directions,impermeant_mask,retention_rescue)"
C_GROUPS="        groups=range(4) if action==6 else [4]"
C_GROUPS_OFF="        groups=range(4) if action==6 else []"
B_ARM_GUARD="elif action==8 and arm not in ('no_B','no_B_rescue','no_B_retention'):"


def no_birth(b,bank,parent,e):
    """The W-producing reaction cannot occur; nothing is paid and nothing is made."""
    return False


def external_B_restore(b,e):
    """AC4's frozen no_B_rescue restoration, reused verbatim."""
    missing=b.boundary==0; e['external_B']=int(missing.sum()); b.boundary[missing]=256


def react_variant(no_C=False,no_B=False):
    """Compile ac4.react with one reaction suppressed, asserting the edit site."""
    src=REACT_SRC
    if no_C:
        assert src.count(C_GROUPS)==1, 'unexpected react text (C groups)'
        src=src.replace(C_GROUPS,C_GROUPS_OFF)
    fns={}
    exec(compile(src,'ac10_react','exec'),dict(vars(ac4)),fns)
    react=fns['react']
    if no_B:
        assert REACT_SRC.count(B_ARM_GUARD)==1, 'unexpected react text (B guard)'
        assert REACT_SRC.count("e['W_birth' if group<4 else 'C_birth']+=1")==1
        def react(b,action,arm,e,_f=react): return _f(b,action,'no_B',e)
    return react


def shim(react):
    ns={k:getattr(ac4,k) for k in dir(ac4) if not k.startswith('_')}
    ns['react']=react
    return SimpleNamespace(**ns)


def step_variant(no_W=False,no_C=False,no_B=False,permeant=False,
                 retention_rescue=False,rescue_B=False):
    """Return a step function equal to the frozen one apart from the named edit."""
    src=STEP_SRC
    ns=dict(vars(ac9))
    if permeant or retention_rescue or rescue_B:
        assert src.count(MOVE_CALL)==1, 'unexpected step text (transport call)'
        ns['impermeant_mask']=np.zeros(20,dtype=bool) if permeant else np.ones(20,dtype=bool)
        ns['retention_rescue']=bool(retention_rescue)
        src=src.replace(MOVE_CALL,MOVE_CALL_NEW)
    if rescue_B:
        assert src.count(B_EXPIRY_LINE)==1, 'unexpected step text (B expiry)'
        src=src.replace(B_EXPIRY_LINE,B_EXPIRY_LINE+'\n    external_B_restore(b,e)')
        ns['external_B_restore']=external_B_restore
    if no_W:
        assert src.count('birth(')==2, 'unexpected step text (W births)'
        ns['birth']=no_birth
    if no_C or no_B:
        ns['ac4']=shim(react_variant(no_C=no_C,no_B=no_B))
    fns={}
    exec(compile(src,'ac10_step','exec'),ns,fns)
    return fns['step']


def build(arm):
    """Return (step_pre_onset, step_post_onset). `keep` is the frozen function."""
    if arm=='keep': return ac9.step,ac9.step
    table={
        'no_W':dict(no_W=True),
        'no_C':dict(no_C=True),
        'no_B':dict(no_B=True),
        'permeant':dict(permeant=True),
        'no_B_retention':dict(no_B=True,retention_rescue=True),
        'B_rescue':dict(no_B=True,rescue_B=True),
        'no_W_late':dict(no_W=True),
        'no_B_late':dict(no_B=True),
    }
    step=step_variant(**table[arm])
    if arm in LATE: return ac9.step,step
    return step,step


def run(seed,history,arm,ticks=2048):
    assert arm in ARMS,arm
    pre,post=build(arm)
    o=v2.acquire(seed)
    mapping=(seed%2,(seed//2)%2)
    reference=decode(o.body.traces[0,:126]).copy()
    rng=np.random.default_rng([seed,1509])
    total=ac9.event(); assay=ac9.event()
    chrono=dict(first_acquire=None,first_loss=None,first_export=None,first_dead=None,
                first_w_empty=None,first_c_empty=None)
    had_both=False
    for t in range(ticks):
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8); coin=bool(rng.random()<.5)
        activation=[history==r for r in range(2)] if t<ONSET else [True,True]
        step=pre if t<ONSET else post
        e=step(o,core,noise,directions,coin,mapping,activation,t<ONSET)
        for k in total: total[k]+=e[k]
        if t>=ONSET:
            for k in assay: assay[k]+=e[k]
        routes=[o.memory.read(k) for k in (0,1)]
        both=all(r is not None for r in routes)
        if both:
            had_both=True
            if chrono['first_acquire'] is None: chrono['first_acquire']=t
        elif had_both and chrono['first_loss'] is None: chrono['first_loss']=t
        if chrono['first_export'] is None and total['particle_export']>0:
            chrono['first_export']=t
        if chrono['first_dead'] is None and o.body.dead: chrono['first_dead']=t
        a=ac4.available(o.body)
        if chrono['first_w_empty'] is None and int(a[:16].sum())==0: chrono['first_w_empty']=t
        if chrono['first_c_empty'] is None and int(a[16:].sum())==0: chrono['first_c_empty']=t
    good=decode(o.body.traces[0,:126])==reference
    return dict(seed=seed,history=history,arm=arm,ticks=ticks,mapping=mapping,
                activity=total['active']/ticks,completed=total['active']==ticks,
                routes=[o.memory.read(k) for k in (0,1)],demand=o.memory.demand().tolist(),
                occupied_sites=int(o.memory.occupied().sum()),
                policy_accuracy=float(good.mean()),
                final_available=ac4.available(o.body).astype(int).tolist(),
                chrono=chrono,ledger=total,assay=assay,
                final_inventory=ac4.inventory(o.body),state_hash=o.digest())


def snapshot(names):
    return {n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}


NAMES=['ac10.py','ac9.py','ac9_priority_v2.py','ac9_memory.py','ac5.py','ac5_program.py',
       'ac4.py','ac4_transport.py','ac1.py','test_ac10.py','AC10_PROTOCOL_v1.md']


def collect(root,seeds):
    root=Path(root); root.mkdir(exist_ok=False)
    hashes=snapshot([n for n in NAMES if Path(n).exists()])
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0,1):
                for arm in ARMS:
                    r=run(seed,history,arm); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,outcomes=[(r['history'],r['arm'],r['activity'],
                  r['routes'],r['occupied_sites']) for r in rows[-2*len(ARMS):]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac10_engineering_v1',[1,2]); return
    collect('ac10_results_v1',[1300,1301,1302,1303])


if __name__=='__main__': main()
