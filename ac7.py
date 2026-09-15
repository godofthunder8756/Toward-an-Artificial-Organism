"""Unknown port mapping acquired via paid changes to vulnerable route actions."""
from pathlib import Path
import hashlib
import json
import numpy as np
import ac4
import ac5
import ac5_program as prog
import ac4_transport as tr
from ac1 import decode

ARMS=('adaptive','no_learning','random_ports','protected','hold_routes','erase_routes')


def route_actions(traces):
    bits=decode(traces[0,:prog.PROGRAM_BITS]).reshape(9,14)
    return [int((bits[i,10:14]*(1<<np.arange(4))).sum()) for i in (0,1)]


def route_correct(traces,mapping):
    return route_actions(traces)==[12*mapping[0],1+12*mapping[1]]


def erase_routes(b):
    changed=0
    for rule,action in ((0,0),(1,1)):
        bits=np.array([(action>>k)&1 for k in range(4)],dtype=np.uint8)
        sites=b.traces[0,rule*14+10:rule*14+14]
        changed+=int((sites!=bits[:,None]).sum()); sites[:]=bits[:,None]
    return changed


def contact(b,action,mapping,e):
    resource=action%2; port=int(action>=12)
    if port==mapping[resource]: ac4.react(b,resource,'self',e)
    else: b.energy-=1; e['active']=1; e['spent_e']+=1
    e['contacts']=1
    e['productive']=int(e['in_f']+e['in_m']>0)
    return resource,e['productive']>0


def learn_from_contact(b,source,resource,productive,e,shadow=None):
    """No environment mapping, seed, target or future outcome argument."""
    if productive: return
    action=route_actions(source)[resource]^12
    bits=np.array([(action>>k)&1 for k in range(4)],dtype=np.uint8)
    e['learn_attempt']=1
    cost=prog.paid_replace(b,resource*14+10,bits,int(ac4.available(b)[:4].sum()))
    e['writes']+=cost['writes']; e['learn_writes']+=cost['writes']
    e['spent_e']+=cost['energy']; e['spent_m']+=cost['material']
    e['learn_success']=int(cost['applied'])
    if cost['applied'] and shadow is not None: shadow[0,resource*14+10:resource*14+14]=bits[:,None]


def step(b,flips,directions,coin,mapping,arm='adaptive',learning=True,shadow=None):
    if arm not in ARMS or (shadow is not None and arm!='protected'): raise ValueError('Invalid control')
    if arm=='protected' and shadow is None: raise ValueError('Missing explicit program')
    e=ac4.empty_event(); e.update(contacts=0,productive=0,learn_attempt=0,learn_success=0,learn_writes=0)
    if b.dead: return e
    before=ac4.inventory(b); b.traces^=flips
    e['particle_expiry']=int((b.life==1).sum()); b.life[b.life>0]-=1
    e['B_expiry']=int((b.boundary==1).sum()); b.boundary[b.boundary>0]-=1
    inactive=b.life==0; old=inactive.copy()
    tr.move(b.pos,inactive,b.boundary,directions,np.ones(20,dtype=bool))
    lost=inactive & ~old; e['particle_export']=int(lost.sum()); b.life[lost]=0
    a=ac4.available(b); units=min(int(a[16:].sum()),b.fuel,(128-b.energy)//8)
    b.fuel-=units; b.energy+=units*8; e['converted']=units
    if b.energy<1: b.dead=True
    else:
        source=shadow if arm=='protected' else b.traces
        action=prog.choose(source,ac4.observe(b))
        if action in (0,1,12,13):
            if arm=='random_ports': action=action%2+12*int(coin)
            resource,productive=contact(b,action,mapping,e)
            if learning and arm not in ('no_learning','random_ports'):
                learn_from_contact(b,source,resource,productive,e,shadow)
        else: ac4.react(b,action,'self',e)
    ac4.balance(before,b,e); return e


def run(seed,arm,ticks=8192):
    b,bits,priority=ac5.acquire(seed); mapping=(seed%2,(seed//2)%2)
    shadow=b.traces.copy() if arm=='protected' else None
    rng=np.random.default_rng([seed,1407]); total=None; mid=None; overwritten=0
    for t in range(ticks):
        if t==4096:
            mid=dict(alive=not b.dead,correct=route_correct(b.traces,mapping),actions=route_actions(b.traces))
            if arm=='erase_routes': overwritten=erase_routes(b)
        flips=(rng.random(b.traces.shape,dtype=np.float32)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8); coin=bool(rng.random()<.5)
        learning=not(arm in ('hold_routes','erase_routes') and t>=4096)
        e=step(b,flips,directions,coin,mapping,arm,learning,shadow)
        if total is None: total={k:0 for k in e}
        for k in e: total[k]+=e[k]
    dec=decode(b.traces); mask=np.ones(prog.PROGRAM_BITS,dtype=bool)
    mask[10:14]=False; mask[24:28]=False
    return dict(seed=seed,arm=arm,ticks=ticks,mapping=mapping,priority=priority,midpoint=mid,
                activity=total['active']/ticks,completed=total['active']==ticks,
                final_correct=route_correct(b.traces,mapping),actions=route_actions(b.traces),
                structural_accuracy=float((dec[0,:126][mask]==bits[0,:126][mask]).mean()),
                ledger=total,externally_overwritten=overwritten,final_inventory=ac4.inventory(b),
                state_hash=b.digest(),shadow_hash=hashlib.sha256(shadow.tobytes()).hexdigest() if shadow is not None else None)


def main():
    root=Path('ac7_results_v1'); root.mkdir(exist_ok=False)
    names=['ac7.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','test_ac7.py','AC7_PROTOCOL_v1.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2)); rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in range(700,708):
            for arm in ARMS:
                r=run(seed,arm); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,activity={r['arm']:r['activity'] for r in rows[-6:]})),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))


if __name__=='__main__': main()
