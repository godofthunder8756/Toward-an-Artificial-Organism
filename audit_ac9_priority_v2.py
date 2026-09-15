from pathlib import Path
import hashlib
import json
import numpy as np
import ac9_priority_v2 as experiment

root=Path('ac9_priority_results_v2'); d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text()); assert s==d['hashes']
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in s.items())
rows=d['rows']; assert rows==[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert len(rows)==40 and {(r['seed'],r['history'],r['variant']) for r in rows}=={(s,h,a) for s in range(1100,1104) for h in (0,1) for a in experiment.ARMS}
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']; sites=sum(r['demand'])
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+24+40+e['in_m']==M+4*N+2*B+sites+e['writes']-e['memory_writes']+e['memory_waste']+e['memory_expiry']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    if r['variant']=='no_growth': assert sites==0 and e['region0_births']==e['region1_births']==0
    if r['seed']==1100:
        assert json.loads(json.dumps(experiment.run(r['seed'],r['history'],r['variant'])))==r
        replays.append([r['history'],r['variant']])
good=lambda r:r['routes']==r['mapping']
g={a:[r for r in rows if r['variant']==a] for a in experiment.ARMS}
m={a:dict(completed=sum(r['completed'] for r in v),retained=sum(good(r) for r in v),
          activity=float(np.mean([r['activity'] for r in v])),exports=float(np.mean([r['ledger']['particle_export'] for r in v])),
          final_B=float(np.mean([r['final_inventory'][4] for r in v]))) for a,v in g.items()}
criteria=dict(baseline=all(r['completed'] and good(r) and r['checkpoint']['routes']==r['mapping'] and r['checkpoint']['demand'][r['history']]==42 and r['checkpoint']['demand'][1-r['history']]==0 for r in g['priority']))
for history in (0,1):
    same=[r for r in rows if r['history']==history and r['variant']==f'block{history}']
    other=[r for r in rows if r['history']==history and r['variant']==f'block{1-history}']
    criteria[f'history{history}_specific']=sum(not good(r) for r in same)>=3 and sum(good(r) for r in other)>=3
report=dict(ok=True,rows=40,exact_replays=replays,summary=m,criteria=criteria,
            limits='Same-author first-stage developmental maintenance; survival can continue by random fallback; broader controls pending')
(root/'audit.json').open('x').write(json.dumps(report,indent=2)); print(json.dumps(report))
