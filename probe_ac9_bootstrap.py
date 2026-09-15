"""Observer-only reference timing; not a simulation of the new AC9 body."""
from pathlib import Path
import hashlib
import json
import numpy as np
import ac7
import ac5

rows=[]
for seed in range(700,708):
    body,_,_=ac5.acquire(seed)
    rng=np.random.default_rng([seed,1407]); mapping=(seed%2,(seed//2)%2)
    for t in range(256):
        flips=(rng.random(body.traces.shape,dtype=np.float32)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8); coin=bool(rng.random()<.5)
        e=ac7.step(body,flips,directions,coin,mapping)
        if e['productive']:
            rows.append(dict(seed=seed,first_productive_tick=t+1,
                             unrenewed_initial_W=sum(t+1<x for x in (32,48,64)),
                             whole_entry_required_W=3))
            break
report=dict(kind='reference_bootstrap_timing',rows=rows,
            source_hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest()
                           for n in ('ac7.py','ac5.py','ac9_memory.py')},
            limitation='AC7 renews all regional W; the unrenewed count is an arithmetic counterfactual at its observed contact times. AC9 altered demand/costs can change those times. This does not predict integrated AC9 outcomes.')
Path('AC9_BOOTSTRAP_REFERENCE_v1.json').open('x').write(json.dumps(report,indent=2))
print(json.dumps(report))
