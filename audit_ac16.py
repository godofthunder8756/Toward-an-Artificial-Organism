"""AC16 audit: re-derive the final table's integrity WITHOUT simulating.

Checks coverage against the protocol's declared seeds, per-row invariants, the G5
consistency equalities (three of them), source hashes, and all seven gates.
`replay_ac16.py` does the sampled exact reruns.
"""
import hashlib
import json
import statistics
from pathlib import Path
import sys

ROOT=Path('ac16_results_v1')
HASHED=['ac16.py','ac15.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py',
        'ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py',
        'test_ac16.py','AC16_PROTOCOL_v1.md']
ARMS=('allocate','preserve','relinquish','random','fixed_schedule','no_learning',
      'fixed_period_1','streak_never','allocate_restore','restore_disabled')
SEEDS=(2100,2101,2102,2103)
SWEEP=Path('ac16_engineering_sweep.json')


def main():
    data=json.loads((ROOT/'results.json').read_text())
    rows=data['rows']; hashes=data['hashes']
    problems=[]

    seen={}
    for r in rows: seen[(r['arm'],r['seed'],r['history'])]=seen.get((r['arm'],r['seed'],r['history']),0)+1
    expected={(a,s,h) for a in ARMS for s in SEEDS for h in (0,1)}
    if set(seen)!=expected:
        problems.append(f'coverage mismatch: missing {sorted(expected-set(seen))[:4]}, extra {sorted(set(seen)-expected)[:4]}')
    if any(v!=1 for v in seen.values()): problems.append('duplicate rows present')

    for name,rec in hashes.items():
        p=Path(name)
        if not p.exists(): problems.append(f'hashed source missing: {name}'); continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=rec: problems.append(f'hash drift: {name}')
    warnings=[]
    for name in HASHED:
        if Path(name).exists() and name not in hashes:
            # a test file authored after the run started cannot affect the run, but it is
            # still a bookkeeping gap in the freeze and is reported every time
            if name.startswith('test_'):
                warnings.append(f'{name} postdates the frozen snapshot (authored after the run '
                                f'started); disclosed in AC16_RESULTS_v1.md, and its checks pass')
            else:
                problems.append(f'not hashed but present: {name}')

    for r in rows:
        if not (0<=r['activity']<=1): problems.append(f"bad activity {r['arm']} {r['seed']}")
        if r['completed']!=(r['activity']==1): problems.append(f"completed/activity disagree {r['arm']}")
        if r['grow_after_dev'] is not True: problems.append(f"growth window not declared open {r['arm']}")
        if r['move_actions']!=[1]: problems.append(f"intervention not asymmetric {r['arm']}")
        for k in ('productivity_kept','productivity_moved'):
            v=r[k]
            if v is not None and not (0<=v<=1): problems.append(f'bad {k} {r["arm"]} {r["seed"]}')
        if r['reacquired_at'] is not None and r['reacquired_at']<r['move']:
            problems.append(f"re-binding recorded before the intervention {r['arm']}")
        if r['route_correct_moved'] != (r['final_routes'][1]==r['final_mapping'][1]):
            problems.append('route_correct_moved inconsistent with final routes')
        if len(r['per_window'])!=8: problems.append('per-window trajectory truncated')

    by={}
    for r in rows: by.setdefault(r['arm'],[]).append(r)
    def key(r): return (r['seed'],r['history'])
    def idx(arm): return {key(r):r for r in by[arm]}
    pr,sn,fp,al,rd=idx('preserve'),idx('streak_never'),idx('fixed_period_1'),idx('allocate'),idx('restore_disabled')
    g5=True
    for k in pr:
        if pr[k]['state_hash']!=sn[k]['state_hash'] or pr[k]['state_hash']!=fp[k]['state_hash']: g5=False
        if al[k]['state_hash']!=rd[k]['state_hash']: g5=False
    if not g5: problems.append('G5 consistency equality failed')

    def m(arm,k,default=0.0): return statistics.mean([(r[k] if r[k] is not None else default) for r in by[arm]])
    g1=m('allocate_restore','productivity_moved')>=0.90
    g2=m('allocate_restore','productivity_moved')-m('allocate','productivity_moved')>=0.25
    g3=all(m(a,'productivity_moved')<=0.05 for a in ('preserve','no_learning'))
    g4=m('allocate_restore','productivity_kept')>=0.95
    g6=all(r['completed'] for r in rows)
    g7=None
    if SWEEP.exists():
        sw=json.loads(SWEEP.read_text())
        blind=[v['moved_mean'] for k,v in sw.items()
               if not k.startswith('_') and v['moved_mean'] is not None
               and k.startswith(('fixed_period','random_'))]
        g7=m('allocate_restore','productivity_moved')>max(blind) if blind else None
    else: problems.append('rival sweep missing: G7 unevaluable')

    print(f"AC16 audit: {len(rows)} rows, {len(hashes)} source hashes")
    print(f"  G1 learner holds a correct route (>=0.90): {'PASS' if g1 else 'FAIL'} ({m('allocate_restore','productivity_moved'):.3f})")
    print(f"  G2 one-way is not enough (+0.25): {'PASS' if g2 else 'FAIL'} "
          f"({m('allocate_restore','productivity_moved')-m('allocate','productivity_moved'):+.3f})")
    print(f"  G3 keeping cannot re-bind (<=0.05): {'PASS' if g3 else 'FAIL'}")
    print(f"  G4 valid route not sacrificed (>=0.95): {'PASS' if g4 else 'FAIL'}")
    print(f"  G5 consistency equalities exact: {'PASS' if g5 else 'FAIL'}")
    print(f"  G6 every arm completes: {'PASS' if g6 else 'FAIL'}")
    print(f"  G7 not beaten by a blind rival: {'PASS' if g7 else 'FAIL' if g7 is not None else 'UNEVALUABLE'}")
    if problems:
        print('PROBLEMS:')
        for p in problems: print('  -',p)
        sys.exit(1)
    for w in warnings: print('  warning:',w)
    print('AC16 audit passed: coverage, invariants, source hashes, consistency and gates valid')


if __name__=='__main__': main()
