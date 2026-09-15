"""Post-protocol intervention: change acquired B decisions, leave laws fixed."""
import json
from pathlib import Path
import numpy as np
import ac4

original,*_=ac4.acquire(0)
changed,*_=ac4.acquire(0)
for b in (original,changed):
    b.boundary[:]=0
    b.pos[:]=[2,0]
p=ac4.policy(changed)
replaced=int((p==8).sum())
p[p==8]=9
bits=((p[:,None]>>np.arange(4))&1).reshape(2,1024)
changed.traces[:2]=np.repeat(bits[:,:,None],7,axis=2)
flips=np.zeros_like(original.traces)
directions=np.ones(20,dtype=int) # Step west to [1,0], still near the east link.
a=ac4.step(original,flips,directions)
b=ac4.step(changed,flips,directions)
assert a['B_birth']==1 and b['B_birth']==0
report=dict(kind='post_protocol_mechanism_probe',changed_policy_rows=replaced,
            original_B_births=a['B_birth'],intervened_B_births=b['B_birth'],
            interpretation='Changing acquired decisions blocks B production with identical physical laws and immediate inputs; not autonomous acquisition of needs.')
Path('ac4_results_v1/policy_intervention.json').open('x').write(json.dumps(report,indent=2))
print(json.dumps(report))
