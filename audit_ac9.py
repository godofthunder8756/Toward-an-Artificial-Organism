from pathlib import Path
import json
import hashlib
import numpy as np
import ac9

root=Path('ac9_results_v1'); d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text()); assert s==d['hashes']
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in s.items())
rows=d['rows']; assert len(rows)==32
assert rows==[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert {(r['seed'],r['history'],r['arm']) for r in rows}=={(s,h,a) for s in range(1000,1004) for h in (0,1) for a in ac9.ARMS}
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']; sites=sum(r['demand'])
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+24+40+e['in_m']==M+4*N+2*B+sites+e['writes']-e['memory_writes']+e['memory_waste']+e['memory_expiry']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    if r['arm']=='no_growth': assert sites==0 and e['region0_births']==e['region1_births']==0
    if r['seed']==1000:
        assert json.loads(json.dumps(ac9.run(r['seed'],r['history'],r['arm'])))==r
        replays.append([r['history'],r['arm']])
keeps=[r for r in rows if r['arm']=='keep']
intact=lambda r:r['routes']==r['mapping']
report=dict(ok=True,rows=32,exact_replays=replays,
            keep_completed=sum(r['completed'] for r in keeps),keep_correct=sum(intact(r) for r in keeps),
            checkpoint_correct=sum(r['checkpoint']['routes']==r['mapping'] for r in keeps),
            keep_details=[dict(seed=r['seed'],history=r['history'],activity=r['activity'],routes=r['routes'],demand=r['demand']) for r in keeps],
            primary_passed=all(r['completed'] and intact(r) and r['checkpoint']['routes']==r['mapping'] and r['checkpoint']['demand'][r['history']]==42 for r in keeps),
            limits='Same-author engineering; first integration, not full developmental validation')
(root/'audit.json').open('x').write(json.dumps(report,indent=2)); print(json.dumps(report))
