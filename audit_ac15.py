"""AC15 audit: re-derive the final table's integrity WITHOUT simulating.

Checks coverage, per-row invariants, the G3 consistency equality, the protocol's
gates and every source hash against the files on disk. This is an audit, not a
replay: `replay_ac15.py` does the sampled exact reruns.
"""
import hashlib
import json
import statistics
from pathlib import Path
import sys

ROOT=Path('ac15_results_v1')
HASHED_INCLUDE=['ac15.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py',
                'ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py',
                'ac1.py','AC15_PROTOCOL_v1.md']
ARMS=('allocate','preserve','relinquish','random','fixed_schedule','no_learning',
      'fixed_period_1','streak_never')
SEEDS=(1900,1901,1902,1903)


def main():
    data=json.loads((ROOT/'results.json').read_text())
    rows=data['rows']; hashes=data['hashes']
    problems=[]

    # 1. coverage: every arm x seed x history exactly once
    seen={}
    for r in rows: seen[(r['arm'],r['seed'],r['history'])]=seen.get((r['arm'],r['seed'],r['history']),0)+1
    expected={(a,s,h) for a in ARMS for s in SEEDS for h in (0,1)}
    if set(seen)!=expected: problems.append(f'coverage mismatch: missing {sorted(expected-set(seen))}, extra {sorted(set(seen)-expected)}')
    if any(v!=1 for v in seen.values()): problems.append('duplicate rows present')

    # 2. source hashes still match the files on disk
    for name,rec in hashes.items():
        p=Path(name)
        if not p.exists(): problems.append(f'hashed source missing: {name}'); continue
        cur=hashlib.sha256(p.read_bytes()).hexdigest()
        if cur!=rec: problems.append(f'hash drift: {name}')
    for name in HASHED_INCLUDE:
        if Path(name).exists() and name not in hashes: problems.append(f'not hashed but present: {name}')
    if 'AC15_PROTOCOL_v1.md' not in hashes: problems.append('protocol not hashed (the protocol must precede the run)')

    # 3. per-row invariants
    for r in rows:
        if not (0<=r['activity']<=1): problems.append(f"bad activity {r['arm']} {r['seed']}: {r['activity']}")
        if r['completed']!=(r['activity']==1): problems.append(f"completed/activity disagree {r['arm']} {r['seed']}")
        for a in ('0','1'):
            v=r['chan_productivity'][a]
            if v is not None and not (0<=v<=1): problems.append(f'bad channel productivity {r["arm"]} {r["seed"]}: {v}')
        if r['move_actions']!=[1]: problems.append(f"intervention not asymmetric {r['arm']} {r['seed']}")
        if not (0<=r['mean_chan_productivity']<=1): problems.append('bad mean productivity')
        if r['productivity_kept'] is not None and r['chan_productivity']['0']!=r['productivity_kept']:
            problems.append('kept-channel field inconsistent')

    # 4. G3: the consistency arms must equal preserve exactly, including the state hash
    by={}
    for r in rows: by.setdefault(r['arm'],[]).append(r)
    for other in ('fixed_period_1','streak_never'):
        for a,b in zip(sorted(by['preserve'],key=lambda r:(r['seed'],r['history'])),
                       sorted(by[other],key=lambda r:(r['seed'],r['history']))):
            if a['state_hash']!=b['state_hash']: problems.append(f'G3 state hash differs: preserve vs {other} seed {a["seed"]}')
            if a['demand']!=b['demand']: problems.append(f'G3 demand differs: preserve vs {other} seed {a["seed"]}')

    # 5. the gates, recomputed
    def m(arm,key): return statistics.mean(r[key] for r in by[arm])
    L=m('allocate','mean_chan_productivity')
    g1=(L-m('preserve','mean_chan_productivity')>=0.08) and (L-m('relinquish','mean_chan_productivity')>=0.08)
    g4=all(r['completed'] for r in rows)
    g5=(m('allocate','productivity_kept')>=0.95) and (m('allocate','productivity_moved')>0)
    sweep=ROOT/'g2_rival_sweep.json'
    g2=None
    if sweep.exists():
        sw=json.loads(sweep.read_text())
        best=max(v['mean'] for k,v in sw.items() if not k.startswith('allocate'))
        g2=L>best
    else: problems.append('G2 rival sweep missing: G2 cannot be evaluated')

    print(f"AC15 audit: {len(rows)} rows, {len(hashes)} source hashes")
    print(f"  G1 learner beats both blind extremes: {'PASS' if g1 else 'FAIL'} ({L:.4f})")
    print(f"  G2 learner beats the best state-blind rival: "
          f"{'PASS' if g2 else 'FAIL' if g2 is not None else 'UNEVALUABLE'}")
    print(f"  G3 consistency arms equal preserve exactly: "
          f"{'PASS' if not any('G3' in p for p in problems) else 'FAIL'}")
    print(f"  G4 every arm completes: {'PASS' if g4 else 'FAIL'}")
    print(f"  G5 kept what was valid, not what was not: {'PASS' if g5 else 'FAIL'}")
    if problems:
        print('PROBLEMS:')
        for p in problems: print('  -',p)
        sys.exit(1)
    print('AC15 audit passed: coverage, per-row invariants, source hashes and gates valid')


if __name__=='__main__': main()
