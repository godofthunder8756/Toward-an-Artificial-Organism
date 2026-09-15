"""Isolate route repair and unannounced environment remapping."""
from pathlib import Path
import inspect
import hashlib
import json
import numpy as np
import ac7
import ac4
import ac5
from ac1 import decode

ARMS=('remap_live','remap_frozen','remap_random','keep','block_routes','block_routes_live')
ROUTE_BITS=np.array([10,11,12,13,24,25,26,27])


def selective_react(b,action,arm,e,repair_routes):
    if repair_routes or action!=2:
        ac4.react(b,action,arm,e); return
    b.energy-=1; e['spent_e']+=1; e['active']=1
    majority=decode(b.traces[0]); sites=np.argwhere(b.traces[0]!=majority[:,None])
    sites=sites[~np.isin(sites[:,0],ROUTE_BITS)]
    n=min(int(ac4.available(b)[:4].sum())*8,32,len(sites),b.energy,b.material)
    if n:
        sites=sites[:n]; b.traces[0,sites[:,0],sites[:,1]]=majority[sites[:,0]]
        ac4.pay(b,e,n,n); e['writes']=n


source=inspect.getsource(ac7.step)
assert source.count("learning=True,shadow=None):")==1
assert source.count("else: ac4.react(b,action,'self',e)")==1
source=source.replace('learning=True,shadow=None):','learning=True,shadow=None,repair_routes=True):')
source=source.replace("else: ac4.react(b,action,'self',e)","else: selective_react(b,action,'self',e,repair_routes)")
namespace=dict(vars(ac7)); namespace['selective_react']=selective_react
exec(compile(source,'ac8_derived_step','exec'),namespace); step=namespace['step']


def run(seed,arm,ticks=8192):
    b,bits,priority=ac5.acquire(seed); initial=(seed%2,(seed//2)%2)
    rng=np.random.default_rng([seed,1407]); total=None; acquired=None; reacquired=None
    final_mapping=initial
    for t in range(ticks):
        if t==2048: acquired=dict(alive=not b.dead,correct=ac7.route_correct(b.traces,initial))
        mapping=tuple(1-x for x in initial) if arm.startswith('remap') and t>=4096 else initial
        final_mapping=mapping
        flips=(rng.random(b.traces.shape,dtype=np.float32)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8); coin=bool(rng.random()<.5)
        learning=t<2048 or arm in ('remap_live','block_routes_live')
        repairs=not(arm in ('block_routes','block_routes_live') and t>=2048)
        e=step(b,flips,directions,coin,mapping,'random_ports' if arm=='remap_random' else 'adaptive',learning,None,repairs)
        if total is None: total={k:0 for k in e}
        for k in e: total[k]+=e[k]
        if arm.startswith('remap') and t>=4096 and reacquired is None and not b.dead and ac7.route_correct(b.traces,mapping):
            reacquired=t+1
    expected=np.array([12*final_mapping[0],1+12*final_mapping[1]])
    target=((expected[:,None]>>np.arange(4))&1).ravel()
    route_bits=decode(b.traces)[0,ROUTE_BITS]
    return dict(seed=seed,arm=arm,ticks=ticks,initial_mapping=initial,final_mapping=final_mapping,
                acquired=acquired,reacquired_tick=reacquired,activity=total['active']/ticks,
                completed=total['active']==ticks,final_correct=ac7.route_correct(b.traces,final_mapping),
                route_accuracy=float((route_bits==target).mean()),ledger=total,
                final_inventory=ac4.inventory(b),state_hash=b.digest())


def main():
    root=Path('ac8_results_v1'); root.mkdir(exist_ok=False)
    names=['ac8.py','ac7.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','test_ac8.py','AC8_PROTOCOL_v1.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2)); rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in range(800,808):
            for arm in ARMS:
                r=run(seed,arm); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,activity={r['arm']:r['activity'] for r in rows[-6:]})),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))


if __name__=='__main__': main()
