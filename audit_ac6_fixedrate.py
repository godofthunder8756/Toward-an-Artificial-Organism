import json
import hashlib
from pathlib import Path
import ac6
import ac6_fixedrate as experiment

root=Path('ac6_fixedrate_results_v1'); d=json.loads((root/'results.json').read_text())
s=json.loads((root/'pre_run_snapshot.json').read_text()); assert d['hashes']==s
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in s.items())
rows=d['rows']; assert rows==[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert len(rows)==40 and {(r['seed'],r['denominator']) for r in rows}=={(s,n) for s in range(400,408) for n in experiment.DENOMINATORS}
replays=[]
for r in rows:
    e=r['ledger']; E,M,F,N,B=r['final_inventory']
    assert 64+8*e['converted']==E+e['spent_e']
    assert 32+e['in_f']==F+e['overflow_f']+e['converted']
    assert 128+60+40+e['in_m']==M+4*N+2*B+e['writes']+4*(e['particle_expiry']+e['particle_export'])+2*(e['B_expiry']+e['B_discard'])+e['overflow_m']
    assert e['spent_e']==e['active']+e['writes']+2*e['W_birth']+4*e['C_birth']+2*e['B_birth']
    assert all(sum(p[k] for p in r['phases'])==e[k] for k in e)
    assert r['shadow_hash'] is None and e['external_B']==0
    if not r['denominator']: assert e['learn_attempt']==0
    if r['seed']==400:
        n=r['denominator']; replay=experiment.run(400,r['arm'],8192,n or 512); replay['denominator']=n
        assert json.loads(json.dumps(replay))==r
        replays.append(n)
        if n==512:
            original=ac6.run(400,'local'); original['denominator']=512
            assert json.loads(json.dumps(original))==r
assert experiment.summarize(rows)==d['summary']
report=dict(ok=True,rows=40,source_hashes=True,all_balances=True,summaries_recomputed=True,
            exact_replay_denominators=replays,full_default_equivalence=True,
            limits='Same-author engineering; not exhaustive fixed-policy comparison or independent confirmation')
(root/'audit.json').open('x').write(json.dumps(report,indent=2)); print(json.dumps(report))
