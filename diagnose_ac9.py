"""Observer-only replay of keep histories; no feedback into dynamics."""
from pathlib import Path
import json
import numpy as np
import ac9

raw=json.loads(Path('ac9_results_v1/results.json').read_text())['rows']; output=[]
for expected in [r for r in raw if r['arm']=='keep']:
    seed=expected['seed']; history=expected['history']; o=ac9.acquire(seed)
    rng=np.random.default_rng([seed,1509]); mapping=(seed%2,(seed//2)%2)
    learned=None; first_loss=None; first_empty=None; last_routes=[None,None]
    for t in range(2048):
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8); coin=bool(rng.random()<.5)
        e=ac9.step(o,core,noise,directions,coin,mapping,[history==r for r in range(2)] if t<512 else [True,True],t<512,None)
        routes=[o.memory.read(k) for k in (0,1)]
        if learned is None and routes==list(mapping): learned=t+1
        if learned is not None and first_loss is None and routes!=list(mapping): first_loss=t+1
        n=int(ac9.ac4.available(o.body)[4*(history+1):4*(history+2)].sum())
        if first_empty is None and o.memory.demand()[history]>0 and n==0: first_empty=t+1
        last_routes=routes
    assert o.digest()==expected['state_hash']
    output.append(dict(seed=seed,history=history,first_correct=learned,first_route_loss=first_loss,
                       first_empty_regional_W_with_memory=first_empty,final_routes=last_routes,exact=True))
Path('ac9_results_v1/chronology.json').open('x').write(json.dumps(output,indent=2)); print(json.dumps(output))
