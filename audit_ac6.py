import hashlib
import json
from pathlib import Path
import numpy as np
import ac6

root=Path('ac6_results_v1'); d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text()); assert d['hashes']==s
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in s.items())
rows=d['rows']; assert rows==[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert len(rows)==40 and {(r['seed'],r['arm']) for r in rows}=={(s,a) for s in range(300,308) for a in ac6.ARMS}
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+60+40+e['in_m']==M+4*N+2*B+e['writes']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    assert e['spent_e']==e['active']+e['writes']+2*e['W_birth']+4*e['C_birth']+2*e['B_birth']
    assert all(sum(p[k] for p in r['phases'])==e[k] for k in e)
    if r['arm']=='frozen': assert e['learn_attempt']==0
    if r['arm']!='protected': assert r['shadow_hash'] is None
    if r['seed']==300:
        assert json.loads(json.dumps(ac6.run(r['seed'],r['arm'])))==r
        replays.append(r['arm'])
groups={a:[r for r in rows if r['arm']==a] for a in ac6.ARMS}
summary={}
for a,g in groups.items():
    summary[a]=dict(completed=sum(r['completed'] for r in g),activity=float(np.mean([r['activity'] for r in g])),
                    structural_accuracy=float(np.mean([r['structural_accuracy'] for r in g])),
                    support_B=float(np.mean([r['phases'][1]['B_birth'] for r in g])),
                    support_B0=None if a=='global' else float(np.mean([r['phases'][1]['B0_birth'] for r in g])),
                    support_omission=float(np.mean([(r['windows'][0]['active']-r['windows'][0]['on'])/1024 for r in g])),
                    support_active=float(np.mean([r['windows'][0]['active']/1024 for r in g])),
                    return_on=float(np.mean([r['windows'][1]['on']/1024 for r in g])),
                    spent_material=float(np.mean([r['ledger']['spent_m'] for r in g])),
                    exports=float(np.mean([r['ledger']['particle_export'] for r in g])))
a=summary['local']; f=summary['frozen']
criteria=dict(completion=a['completed']>=7,activity=a['activity']>=.9,
              relinquishment=a['support_omission']>=.8 and a['support_active']>=.9,
              reacquisition=a['return_on']>=.8,local_B_saving=a['support_B0']<=.5*f['support_B0'],
              structural_integrity=all(r['structural_accuracy']>=.99 for r in groups['local'] if r['completed']))
report=dict(ok=True,rows=40,exact_replays=replays,summary=summary,criteria=criteria,
            limits='Same-author local-revision engineering; not discovery of new needs or full autonomy')
(root/'audit.json').open('x').write(json.dumps(report,indent=2)); print(json.dumps(report))
