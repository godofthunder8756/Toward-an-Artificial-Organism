"""Audit the saved AC10 table without rerunning the study.

Re-derives the ledger identities, arm mechanism invariants, coverage and source
hashes from `ac10_results_v1/results.json`, and cross-checks the frozen source
hashes against the AC9 controls v3 snapshot to show the inherited laws are the
same files. Sampled exact reruns live in `replay_ac10.py`.
"""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).parent
RESULT=ROOT/'ac10_results_v1'/'results.json'
V3=ROOT/'ac9_controls_results_v3'/'results.json'
ARMS=('keep','no_W','no_C','no_B','permeant','no_B_retention','B_rescue',
      'no_W_late','no_B_late')
SHARED=('ac9.py','ac9_priority_v2.py','ac9_memory.py','ac5.py','ac5_program.py',
        'ac4.py','ac4_transport.py','ac1.py')


def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_ledger(row):
    """The frozen AC9 v3 identity, extended only by the labelled external B term."""
    l=row['ledger']; inv=row['final_inventory']
    m0=128+24+40+l['in_m']+2*l['external_B']
    m1=inv[1]+4*inv[3]+2*inv[4]+sum(row['demand'])
    spent=l['writes']-l['memory_writes']
    losses=(l['memory_waste']+l['memory_expiry']+
            4*(l['particle_expiry']+l['particle_export'])+
            2*(l['B_expiry']+l['B_discard'])+l['overflow_m'])
    assert m0==m1+spent+losses,(row['seed'],row['history'],row['arm'],m0,m1,spent,losses)
    assert 64+8*l['converted']==inv[0]+l['spent_e'],(row['seed'],row['arm'])
    assert 32+l['in_f']==inv[2]+l['overflow_f']+l['converted'],(row['seed'],row['arm'])


def check_arm(row):
    l=row['ledger']; a=row['arm']; both=all(x is not None for x in row['routes'])
    if a=='keep':
        assert l['W_birth']>0 and l['C_birth']>0 and l['B_birth']>0
        assert l['external_B']==0 and l['particle_export']==0 and l['memory_bound']>0
    elif a=='no_W':
        assert l['W_birth']==0 and l['memory_bound']==0
        assert row['occupied_sites']==0 and row['routes']==[None,None]
    elif a=='no_C':
        assert l['C_birth']==0
    elif a=='no_B':
        assert l['B_birth']==0 and l['particle_export']>0 and not both
    elif a=='permeant':
        assert l['particle_export']>0 and not both
    elif a=='no_B_retention':
        assert l['B_birth']==0 and l['external_B']==0
        assert l['particle_export']==0 and both
        assert row['final_inventory'][4]==0
    elif a=='B_rescue':
        assert l['B_birth']==0 and l['external_B']>0
        assert l['particle_export']==0 and both
    elif a=='no_W_late':
        assert l['W_birth']-row['assay']['W_birth']>0 and row['assay']['W_birth']==0
    elif a=='no_B_late':
        assert l['B_birth']-row['assay']['B_birth']>0 and row['assay']['B_birth']==0


def main():
    data=json.loads(RESULT.read_text())
    rows=data['rows']; hashes=data['hashes']
    assert len(rows)==72,f'row count {len(rows)}'
    assert len({(r['seed'],r['history'],r['arm']) for r in rows})==72,'duplicate conditions'
    assert {r['seed'] for r in rows}=={1300,1301,1302,1303}
    for r in rows:
        assert r['arm'] in ARMS and r['history'] in (0,1) and r['ticks']==2048
        assert 0<=r['assay']['active']<=1536
        assert r['assay']['productive']<=r['assay']['contacts']
        assert 0<=r['activity']<=1
        check_ledger(r); check_arm(r)
    for name,digest in hashes.items():
        assert sha256(ROOT/name)==digest,f'source changed since freeze: {name}'
    v3=json.loads(V3.read_text())['rows'][0]
    assert 'hashes' in json.loads(V3.read_text())
    v3hashes=json.loads(V3.read_text())['hashes']
    for name in SHARED:
        assert hashes[name]==v3hashes[name],f'{name} differs from the AC9 v3 freeze'
    means={a:sum(r['activity'] for r in rows if r['arm']==a)/8 for a in ARMS}
    print(f'AC10 audit passed: {len(rows)} rows, ledgers, arm invariants and source '
          f'hashes valid; {len(SHARED)} inherited sources identical to the AC9 v3 freeze')
    for a in ARMS: print(f'  {a:16} mean activity {means[a]:.3f}')


if __name__=='__main__': main()
