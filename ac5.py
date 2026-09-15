"""AC5: vulnerable one-bit commitment revision in AC4 physical body."""
from pathlib import Path
import hashlib
import json
import numpy as np
import ac4
import ac4_transport as tr
import ac5_program as prog
from ac1 import decode

ARMS=('adaptive','frozen','random_feedback','informed','protected')
GATE=4*prog.WIDTH


def acquire(seed):
    b,bits,_,priority=ac4.acquire(seed)
    prog.install_at_acquisition(b.traces,priority)
    bits=decode(b.traces).copy()
    return b,bits,priority


def enabled(traces):
    return bool(decode(traces[0,GATE:GATE+1])[0])


def step(b,flips,directions,probe,random_feedback,retention,arm='adaptive',shadow=None):
    if arm not in ARMS or (shadow is not None and arm!='protected'):
        raise ValueError('Hidden protected program or invalid arm')
    if arm=='protected' and shadow is None: raise ValueError('Missing control program')
    e=ac4.empty_event(); e.update(crossings=0,learn_attempt=0,learn_success=0,learn_writes=0,gate_on=0)
    if b.dead: return e
    before=ac4.inventory(b); b.traces^=flips
    e['particle_expiry']=int((b.life==1).sum()); b.life[b.life>0]-=1
    e['B_expiry']=int((b.boundary==1).sum()); b.boundary[b.boundary>0]-=1
    inactive=b.life==0; old=inactive.copy()
    motion=tr.move(b.pos,inactive,b.boundary,directions,np.ones(20,dtype=bool),retention)
    e['crossings']=motion['outward']
    lost=inactive & ~old; e['particle_export']=int(lost.sum()); b.life[lost]=0
    a=ac4.available(b); units=min(int(a[16:].sum()),b.fuel,(128-b.energy)//8)
    b.fuel-=units; b.energy+=units*8; e['converted']=units
    if b.energy<1:
        b.dead=True; ac4.balance(before,b,e); return e
    source=shadow if arm=='protected' else b.traces
    gate=enabled(source); wanted=gate
    if arm=='informed': wanted=not retention
    elif arm!='frozen':
        signal=random_feedback if arm=='random_feedback' else e['crossings']>0
        if not gate and signal: wanted=True
        elif gate and probe: wanted=False
    if wanted!=gate:
        b.energy-=1; e['spent_e']+=1; e['active']=1; e['learn_attempt']=1
        cost=prog.paid_replace(b,GATE,[int(wanted)],int(a[:4].sum()))
        e['spent_e']+=cost['energy']; e['spent_m']+=cost['material']
        e['writes']+=cost['writes']; e['learn_writes']=cost['writes']
        e['learn_success']=int(cost['applied'])
        if cost['applied'] and arm=='protected': shadow[0,GATE]=int(wanted)
    else:
        action=prog.choose(source,ac4.observe(b)); ac4.react(b,action,'self',e)
    e['gate_on']=int(enabled(shadow if arm=='protected' else b.traces))
    ac4.balance(before,b,e)
    return e


def run(seed,arm,ticks=8192):
    b,bits,priority=acquire(seed); shadow=b.traces.copy() if arm=='protected' else None
    rng=np.random.default_rng([seed,1205])
    total=None; phases=[None]*3; windows=[dict(active=0,on=0),dict(active=0,on=0)]
    for t in range(ticks):
        flips=(rng.random(b.traces.shape,dtype=np.float32)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8)
        probe=bool(rng.random()<1/512); feedback=bool(rng.random()<1/512)
        phase=0 if t<2048 else 1 if t<6144 else 2
        e=step(b,flips,directions,probe,feedback,phase==1,arm,shadow)
        if total is None: total={k:0 for k in e}
        if phases[phase] is None: phases[phase]={k:0 for k in e}
        for k in e: total[k]+=e[k]; phases[phase][k]+=e[k]
        for i,(start,end) in enumerate(((5120,6144),(7168,8192))):
            if start<=t<end:
                windows[i]['active']+=e['active']; windows[i]['on']+=e['gate_on']
    decoded=decode(b.traces); match=decoded[0,:prog.PROGRAM_BITS]==bits[0,:prog.PROGRAM_BITS]
    structural=np.delete(match,GATE)
    payload=np.ones(bits.shape,dtype=bool); payload[0,:prog.PROGRAM_BITS]=False
    return dict(seed=seed,arm=arm,ticks=ticks,priority=priority,activity=total['active']/ticks,
                completed=total['active']==ticks,program_accuracy=float(match.mean()),
                structural_accuracy=float(structural.mean()),payload_accuracy=float((decoded[payload]==bits[payload]).mean()),
                windows=windows,phases=phases,ledger=total,final_inventory=ac4.inventory(b),state_hash=b.digest(),
                shadow_hash=hashlib.sha256(shadow.tobytes()).hexdigest() if shadow is not None else None)


def main():
    root=Path('ac5_results_v1'); root.mkdir(exist_ok=False)
    names=['ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','test_ac5.py','AC5_PROTOCOL_v1.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in range(200,208):
            for arm in ARMS:
                r=run(seed,arm); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,activity={r['arm']:r['activity'] for r in rows[-5:]})),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))


if __name__=='__main__': main()
