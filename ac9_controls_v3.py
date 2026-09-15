from pathlib import Path
from types import FunctionType
import copy
import inspect
import hashlib
import json
import numpy as np
import ac9
import ac9_priority_v2 as v2

ARMS=('keep','block_old','block_other','swap_block_old','swap_block_other','read_disabled','protected_block_old','fixed_correct')


def relocate(o):
    o.memory.bits[:]=o.memory.bits[::-1].copy(); o.memory.life[:]=o.memory.life[::-1].copy()
    o.body.life[4:12]=o.body.life[4:12].reshape(2,4)[::-1].reshape(8).copy()
    o.body.pos[4:12]=o.body.pos[4:12].reshape(2,4,2)[::-1].reshape(8,2).copy()


def changed_read_step(reader):
    source=inspect.getsource(ac9.step)
    assert source.count('selected=o.memory.read(action)')==1
    source=source.replace('selected=o.memory.read(action)','selected=control_reader(action)')
    namespace=dict(vars(ac9),control_reader=reader)
    exec(compile(source,'ac9_explicit_read_control','exec'),namespace)
    return namespace['step']


def inputs(rng,o):
    return ((rng.random((126,7))<.0001).astype(np.uint8),
            (rng.random(o.memory.bits.shape)<.0001).astype(np.uint8),
            rng.integers(0,4,20,dtype=np.uint8),bool(rng.random()<.5))


def develop(seed,history,fixed=False):
    o=v2.acquire(seed); mapping=(seed%2,(seed//2)%2); total=ac9.event()
    if fixed:
        for _ in range(3): assert ac9.birth(o.body,1,0,total)
        for key in (0,1):
            charge=ac9.mem.deposit(o.memory,o.body,key,mapping[key],[True,False],[3,0])
            assert charge['bound']==21; ac9.memory_charge(total,charge); total['deposits']+=1
    rng=np.random.default_rng([seed,1509])
    for _ in range(512):
        e=ac9.step(o,*inputs(rng,o),mapping,[history==r for r in range(2)],True,None)
        for k in total: total[k]+=e[k]
    return o,total,copy.deepcopy(rng.bit_generator.state)


def run(seed,history,arm,development=None):
    if arm not in ARMS: raise ValueError(arm)
    if arm=='fixed_correct': development=develop(seed,history,True)
    elif development is None: development=develop(seed,history)
    o,total,rng_state=copy.deepcopy(development)
    checkpoint=dict(memory_hash=o.memory.digest(),demand=o.memory.demand().tolist(),
                    routes=[o.memory.read(k) for k in (0,1)])
    if arm.startswith('swap'): relocate(o)
    blocked=history if arm in ('block_old','swap_block_old','protected_block_old') else 1-history if arm in ('block_other','swap_block_other') else None
    protected=copy.deepcopy(o.memory) if arm=='protected_block_old' else None
    step=changed_read_step(lambda key:None) if arm=='read_disabled' else changed_read_step(protected.read) if protected is not None else ac9.step
    rng=np.random.default_rng(); rng.bit_generator.state=rng_state
    mapping=(seed%2,(seed//2)%2); assay=ac9.event()
    for _ in range(1536):
        e=step(o,*inputs(rng,o),mapping,[True,True],False,blocked)
        for k in total: total[k]+=e[k]; assay[k]+=e[k]
    return dict(seed=seed,history=history,arm=arm,checkpoint=checkpoint,
                mapping=mapping,routes=[o.memory.read(k) for k in (0,1)],demand=o.memory.demand().tolist(),
                activity=total['active']/2048,ledger=total,assay=assay,
                final_inventory=ac9.ac4.inventory(o.body),state_hash=o.digest(),
                protected_hash=protected.digest() if protected is not None else None)


def main():
    o,_,_=develop(1,0); before=o.digest(); inventory=ac9.ac4.inventory(o.body); sites=int(o.memory.occupied().sum())
    relocate(o); assert inventory==ac9.ac4.inventory(o.body) and sites==o.memory.occupied().sum()
    relocate(o); assert o.digest()==before
    root=Path('ac9_controls_results_v3'); root.mkdir(exist_ok=False)
    names=['ac9_controls_v3.py','ac9_priority_v2.py','ac9.py','ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','AC9_CONTROLS_PROTOCOL_v3.md']
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2)); rows=[]
    with (root/'rows.jsonl').open('x') as f:
        for seed in range(1200,1204):
            for history in (0,1):
                checkpoint=develop(seed,history)
                for arm in ARMS:
                    r=run(seed,history,arm,checkpoint); rows.append(r); f.write(json.dumps(r)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,outcomes=[(r['history'],r['arm'],r['routes']) for r in rows[-16:]])),flush=True)
    (root/'results.json').write_text(json.dumps(dict(hashes=hashes,rows=rows),indent=2))


if __name__=='__main__': main()
