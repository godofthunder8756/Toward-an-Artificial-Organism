"""Evidence scope audit before interpreting routing as developmental novelty."""
from pathlib import Path
import hashlib
import json
import math

paths=['ac7_results_v1/results.json','ac8_results_v1/results.json',
       'ac8_partition_results_v1/results.json','E2_PROTOCOL.md']
d=json.loads(Path(paths[0]).read_text())
learners=[r for r in d['rows'] if r['arm']=='adaptive']
groups={}
for r in learners:
    mapping=tuple(r['mapping']); actions=tuple(r['actions'])
    assert actions==(12*mapping[0],1+12*mapping[1])
    groups.setdefault(mapping,set()).add(actions)
assert len(groups)==4 and all(len(x)==1 for x in groups.values())
assert all(r['completed'] for r in learners)
changed=sum(tuple(r['actions'])!=(0,1) for r in learners)
second=json.loads(Path(paths[1]).read_text())
remapped=[r for r in second['rows'] if r['arm']=='remap_live']
assert all(r['final_correct'] and r['completed'] for r in remapped)
report=dict(kind='developmental_claim_scope_audit',
            source_hashes={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths},
            acquired_individuals=len(learners),observed_mapping_classes=len(groups),
            observed_route_action_classes=len({tuple(r['actions']) for r in learners}),
            initial_guesses_changed=changed,initial_guesses_already_correct=len(learners)-changed,
            mapping_information_bits=math.log2(len(groups)),
            within_mapping_final_route_variants={str(k):len(v) for k,v in groups.items()},
            remap_successes=len(remapped),
            supported='Physical-outcome acquisition, reacquisition, and causal maintenance of encoded resource-access decisions.',
            not_established='History-dependent creation of a new material-production requirement, self-produced memory scaffold, or developmental reorganization of reaction dependencies.',
            inference_limit='Observed routing diversity alone cannot establish those larger claims. Zero within-mapping routing variation is not a general argument against autonomy or deterministic learning.')
Path('DEVELOPMENTAL_SCOPE_AUDIT_v1.json').open('x').write(json.dumps(report,indent=2))
print(json.dumps(report))
