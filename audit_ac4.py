"""Same-author verification of AC4 raw rows and exact sampled reruns."""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac4

root=Path('ac4_results_v1')
d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text())
assert d['hashes']==s
assert all(hashlib.sha256(Path(n).read_bytes()).hexdigest()==v for n,v in s.items())
rows=d['rows']
expected={(seed,p,arm) for seed in range(4) for p in (.00005,.0001) for arm in ac4.ARMS}
assert len(rows)==len(expected)==48
assert {(r['seed'],r['p'],r['arm']) for r in rows}==expected
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+60+40+e['in_m']+2*e['external_B']==M+4*N+2*B+e['writes']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    assert e['spent_e']==e['active']+e['writes']+2*e['W_birth']+4*e['C_birth']+2*e['B_birth']
    if r['arm'] in ('no_B','no_B_rescue','no_B_retention'): assert e['B_birth']==0
    if r['arm']!='no_B_rescue': assert e['external_B']==0
    if r['seed']==0:
        replay=ac4.run(r['seed'],r['p'],r['arm'])
        # JSON normalizes tuple inventory to list.
        assert json.loads(json.dumps(replay))==r
        replays.append([r['seed'],r['p'],r['arm']])
summary=[]
for p in (.00005,.0001):
    groups={a:[r for r in rows if r['p']==p and r['arm']==a] for a in ac4.ARMS}
    means={a:{k:float(np.mean([r[k] for r in group])) for k in ('activity','policy_accuracy','payload_accuracy')} for a,group in groups.items()}
    criteria=dict(self_viable=means['self']['activity']>=.9,
                  self_information=all(r['policy_accuracy']>=.99 for r in groups['self']),
                  boundary_turnover=all(r['ledger']['B_birth']>40 for r in groups['self']),
                  boundary_dependence=means['self']['activity']-means['no_B']['activity']>=.2,
                  B_rescue=means['no_B_rescue']['activity']>=.9,
                  retention_rescue=means['no_B_retention']['activity']>=.9)
    summary.append(dict(p=p,means=means,criteria=criteria))
report=dict(ok=True,rows=48,exact_replays=replays,source_hashes_match=True,
            all_resource_balances=True,summary=summary,
            limits='Same-author engineering; not independent confirmation or full autopoiesis')
(root/'audit.json').open('x').write(json.dumps(report,indent=2))
print(json.dumps(report))
