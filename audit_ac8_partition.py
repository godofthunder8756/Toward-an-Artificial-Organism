from pathlib import Path
from types import FunctionType
import hashlib
import json
import numpy as np
import ac5
import ac8
import ac8_partition as experiment

root=Path('ac8_partition_results_v1'); d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text()); assert d['hashes']==s
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in s.items())
for name,mask in experiment.MASKS.items():
    b,*_=ac5.acquire(0); b.traces[0,ac8.ROUTE_BITS,0]^=1; before=b.traces.copy()
    reaction=FunctionType(ac8.selective_react.__code__,dict(vars(ac8),ROUTE_BITS=np.array(mask,dtype=int)))
    event=ac8.ac4.empty_event(); reaction(b,2,'self',event,False)
    for bit in ac8.ROUTE_BITS:
        assert np.array_equal(before[0,bit],b.traces[0,bit])==(int(bit) in mask)
rows=d['rows']; assert rows==[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert len(rows)==32 and {(r['seed'],r['condition']) for r in rows}=={(s,a) for s in range(900,908) for a in experiment.MASKS}
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+60+40+e['in_m']==M+4*N+2*B+e['writes']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    assert e['spent_e']==e['active']+e['writes']+2*e['W_birth']+4*e['C_birth']+2*e['B_birth']
    if r['seed']==900:
        assert json.loads(json.dumps(experiment.run(900,r['condition'])))==r
        replays.append(r['condition'])
        if r['condition']=='all_routes':
            original=ac8.run(900,'block_routes'); original['condition']='all_routes'
            assert json.loads(json.dumps(original))==r
g={a:[r for r in rows if r['condition']==a] for a in experiment.MASKS}
m={a:dict(completed=sum(r['completed'] for r in v),activity=float(np.mean([r['activity'] for r in v])),
          correct=sum(r['final_correct'] for r in v),route_accuracy=float(np.mean([r['route_accuracy'] for r in v]))) for a,v in g.items()}
passed=m['keep']['completed']>=7 and m['keep']['activity']-m['selectors']['activity']>=.2 and m['keep']['route_accuracy']>m['selectors']['route_accuracy']
report=dict(ok=True,rows=32,mask_selectivity=True,exact_replays=replays,full_original_equivalence=True,
            summary=m,primary_passed=passed,limits='Same-author engineering; encoded selectors, finite horizon, not new-need creation')
(root/'audit.json').open('x').write(json.dumps(report,indent=2)); print(json.dumps(report))
