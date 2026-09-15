import json
import hashlib
from pathlib import Path
import numpy as np
import ac8

root=Path('ac8_results_v1'); d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text()); assert s==d['hashes']
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in s.items())
rows=d['rows']; assert rows==[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert len(rows)==48 and {(r['seed'],r['arm']) for r in rows}=={(s,a) for s in range(800,808) for a in ac8.ARMS}
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+60+40+e['in_m']==M+4*N+2*B+e['writes']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    assert e['spent_e']==e['active']+e['writes']+2*e['W_birth']+4*e['C_birth']+2*e['B_birth']
    assert e['external_B']==0
    if r['seed']==801:
        assert json.loads(json.dumps(ac8.run(r['seed'],r['arm'])))==r
        replays.append(r['arm'])
g={a:[r for r in rows if r['arm']==a] for a in ac8.ARMS}
m={a:dict(completed=sum(r['completed'] for r in v),activity=float(np.mean([r['activity'] for r in v])),
          acquired=sum(r['acquired']['alive'] and r['acquired']['correct'] for r in v),
          correct=sum(r['final_correct'] for r in v),route_accuracy=float(np.mean([r['route_accuracy'] for r in v]))) for a,v in g.items()}
criteria=dict(reacquisition=m['remap_live']['completed']>=7 and m['remap_live']['correct']>=7
                            and m['remap_live']['acquired']==8
                            and m['remap_live']['activity']-m['remap_frozen']['activity']>=.2,
              maintenance=m['keep']['completed']>=7 and m['keep']['activity']-m['block_routes']['activity']>=.2
                          and m['keep']['route_accuracy']>m['block_routes']['route_accuracy'])
report=dict(ok=True,rows=48,exact_replays=replays,summary=m,criteria=criteria,
            reacquisition_ticks=[r['reacquired_tick'] for r in g['remap_live']],
            limits='Same-author engineering; access mappings, not new-need creation; finite-horizon selective ablation')
(root/'audit.json').open('x').write(json.dumps(report,indent=2)); print(json.dumps(report))
