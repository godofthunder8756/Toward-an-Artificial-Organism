import hashlib
import json
from pathlib import Path
import ac4
from ac4_followup import ARMS, summarize

root=Path('ac4_followup_results_v1')
d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text())
assert d['hashes']==s
assert all(hashlib.sha256(Path(n).read_bytes()).hexdigest()==v for n,v in s.items())
rows=d['rows']; logged=[json.loads(line) for line in (root/'rows.jsonl').read_text().splitlines()]
assert rows==logged and len(rows)==64
assert {(r['seed'],r['p'],r['arm']) for r in rows}=={(s,p,a) for s in range(100,108) for p in (.00005,.0001) for a in ARMS}
replays=[]
for r in rows:
    assert r['ticks']==8192
    e=r['ledger']; E,M,F,N,B=r['final_inventory']
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+60+40+e['in_m']+2*e['external_B']==M+4*N+2*B+e['writes']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    assert e['spent_e']==e['active']+e['writes']+2*e['W_birth']+4*e['C_birth']+2*e['B_birth']
    assert e['external_B']==0
    if r['arm']=='no_B_retention': assert e['B_birth']==0
    if r['seed']==100:
        replay=ac4.run(r['seed'],r['p'],r['arm'],8192)
        assert json.loads(json.dumps(replay))==r
        replays.append([r['seed'],r['p'],r['arm']])
assert summarize(rows)==d['summary']
report=dict(ok=True,rows=64,source_hashes=True,resource_balances=True,
            summary_recomputed=True,exact_replays=replays,
            limits='Same-author engineering audit; no independent confirmation')
(root/'audit.json').open('x').write(json.dumps(report,indent=2))
print(json.dumps(report))
