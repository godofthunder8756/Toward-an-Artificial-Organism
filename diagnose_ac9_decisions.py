from collections import deque
from types import FunctionType
from pathlib import Path
import json
import numpy as np
import ac9

raw=json.loads(Path('ac9_results_v1/results.json').read_text())['rows']; report=[]
for expected in [r for r in raw if r['arm']=='keep']:
    seed,h=expected['seed'],expected['history']; o=ac9.acquire(seed)
    rng=np.random.default_rng([seed,1509]); mapping=(seed%2,(seed//2)%2)
    ring=deque(maxlen=24); capture=[]; losses=[]; learned=False; was_correct=False
    def observed(o):
        obs=ac9.observe(o); b=o.body; life=o.memory.life[h]
        capture.append(dict(obs=obs,action=ac9.prog.choose(b.traces,obs),E=b.energy,M=b.material,
                            W=ac9.ac4.available(b)[4*(h+1):4*(h+2)].astype(int).tolist(),
                            W_life=b.life[4*(h+1):4*(h+2)].tolist(),
                            min_life=[int(x[x>0].min()) if (x>0).any() else None for x in life],
                            present=[(x>0).sum(axis=1).tolist() for x in life],
                            slots=[o.memory.decoded_slot(h,i) for i in range(2)]))
        return obs
    replay_step=FunctionType(ac9.step.__code__,dict(vars(ac9),observe=observed),argdefs=ac9.step.__defaults__)
    for t in range(2048):
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8); coin=bool(rng.random()<.5); capture.clear()
        e=replay_step(o,core,noise,directions,coin,mapping,[h==r for r in range(2)] if t<512 else [True,True],t<512,None)
        if capture:
            snapshot=capture[0]; snapshot.update(tick=t+1,memory_writes=e['memory_writes'],expired=e['memory_expiry'])
            ring.append(snapshot)
        correct=[o.memory.read(k) for k in (0,1)]==list(mapping)
        if learned and was_correct and not correct:
            losses.append(dict(tick=t+1,window=list(ring)))
        learned|=correct; was_correct=correct
    assert o.digest()==expected['state_hash']
    report.append(dict(seed=seed,history=h,exact=True,losses=losses))
Path('ac9_results_v1/decision_chronology.json').open('x').write(json.dumps(report,indent=2))
for r in report:
    if r['losses']:
        w=r['losses'][0]['window']; print(json.dumps(dict(seed=r['seed'],history=r['history'],loss=r['losses'][0]['tick'],last=w[-5:])))
