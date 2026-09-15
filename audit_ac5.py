import json
import hashlib
from pathlib import Path
import numpy as np
import ac5

root=Path('ac5_results_v1'); d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text())
assert s==d['hashes']
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in s.items())
rows=d['rows']; assert rows==[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert len(rows)==40 and {(r['seed'],r['arm']) for r in rows}=={(s,a) for s in range(200,208) for a in ac5.ARMS}
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+60+40+e['in_m']==M+4*N+2*B+e['writes']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    assert e['spent_e']==e['active']+e['writes']+2*e['W_birth']+4*e['C_birth']+2*e['B_birth']
    assert e['external_B']==0 and e['learn_writes']<=e['writes']
    assert all(sum(p[k] for p in r['phases'])==e[k] for k in e)
    if r['arm']=='frozen': assert e['learn_attempt']==0
    if r['arm']!='protected': assert r['shadow_hash'] is None
    if r['seed']==200:
        assert json.loads(json.dumps(ac5.run(r['seed'],r['arm'])))==r
        replays.append(r['arm'])
groups={a:[r for r in rows if r['arm']==a] for a in ac5.ARMS}
summary={a:dict(completed=sum(r['completed'] for r in g),activity=float(np.mean([r['activity'] for r in g])),
                structural_accuracy=float(np.mean([r['structural_accuracy'] for r in g])),
                support_B=float(np.mean([r['phases'][1]['B_birth'] for r in g])),
                support_on=float(np.mean([r['windows'][0]['on']/1024 for r in g])),
                support_active=float(np.mean([r['windows'][0]['active']/1024 for r in g])),
                return_on=float(np.mean([r['windows'][1]['on']/1024 for r in g]))) for a,g in groups.items()}
a=summary['adaptive']; f=summary['frozen']
criteria=dict(completion=a['completed']>=7,activity=a['activity']>=.9,
              relinquishment=a['support_on']<=.2 and a['support_active']>=.9,
              reacquisition=a['return_on']>=.8,
              lower_B_production=a['support_B']<=.5*f['support_B'],
              structural_integrity=all(r['structural_accuracy']>=.99 for r in groups['adaptive'] if r['completed']))
# Activity requirement prevents dead individuals being counted as relinquishing.
report=dict(ok=True,rows=40,exact_replays=replays,summary=summary,criteria=criteria,
            limits='Same-author engineering. Empty completing set makes structural criterion vacuous; lower production during death is not adaptive success.')
(root/'audit.json').open('x').write(json.dumps(report,indent=2)); print(json.dumps(report))
