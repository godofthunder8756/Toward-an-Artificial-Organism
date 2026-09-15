import hashlib
import json
from pathlib import Path
import numpy as np
import ac7

root=Path('ac7_results_v1'); d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text()); assert s==d['hashes']
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in s.items())
rows=d['rows']; assert rows==[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert len(rows)==48 and {(r['seed'],r['arm']) for r in rows}=={(s,a) for s in range(700,708) for a in ac7.ARMS}
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+60+40+e['in_m']==M+4*N+2*B+e['writes']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    assert e['spent_e']==e['active']+e['writes']+2*e['W_birth']+4*e['C_birth']+2*e['B_birth']
    assert e['external_B']==0
    if r['arm']!='erase_routes': assert r['externally_overwritten']==0
    if r['arm'] in ('no_learning','random_ports'): assert e['learn_attempt']==0
    if r['arm']!='protected': assert r['shadow_hash'] is None
    if r['seed']==701:
        assert json.loads(json.dumps(ac7.run(r['seed'],r['arm'])))==r
        replays.append(r['arm'])
g={a:[r for r in rows if r['arm']==a] for a in ac7.ARMS}
summary={a:dict(completed=sum(r['completed'] for r in v),activity=float(np.mean([r['activity'] for r in v])),
                midpoint_correct=sum(r['midpoint']['correct'] and r['midpoint']['alive'] for r in v),
                contacts=float(np.mean([r['ledger']['contacts'] for r in v])),
                productive=float(np.mean([r['ledger']['productive'] for r in v])),
                material=float(np.mean([r['ledger']['spent_m'] for r in v]))) for a,v in g.items()}
paired={(r['seed'],r['arm']):r for r in rows}
delta=[paired[s,'hold_routes']['activity']-paired[s,'erase_routes']['activity'] for s in range(700,708) if any(paired[s,'hold_routes']['mapping'])]
criteria=dict(acquired_viability=summary['adaptive']['completed']>=7,
              acquired_mapping=summary['adaptive']['midpoint_correct']==8,
              frozen_limit=summary['no_learning']['completed']<=2,
              protected_viability=summary['protected']['completed']>=7,
              erasure_dependence=bool(np.mean(delta)>=.2),
              structural=all(r['structural_accuracy']>=.99 for r in g['adaptive'] if r['completed']))
report=dict(ok=True,rows=48,exact_replays=replays,summary=summary,
            hold_minus_erase_nonzero_mapping=float(np.mean(delta)),criteria=criteria,
            limits='Same-author engineering; two unknown access bits, not new-need creation')
(root/'audit.json').open('x').write(json.dumps(report,indent=2)); print(json.dumps(report))
