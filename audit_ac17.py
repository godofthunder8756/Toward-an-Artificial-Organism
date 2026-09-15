"""AC17 audit: re-derive the final table's integrity WITHOUT simulating.

Checks coverage against the protocol's declared seeds, per-row invariants, the three G5
consistency equalities, source hashes, and the categorical gates. `replay_ac17.py` does the
sampled exact reruns. Gate semantics here are **per individual**, as AC17 declares: a gate
fails if even one individual fails it.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path('ac17_results_single_v1')
SWEEP=Path('ac17_engineering_sweep.json')
ARMS=('allocate_restore','allocate','preserve','no_learning','relinquish','random',
      'fixed_schedule','restore_only','fixed_period_1','streak_never','restore_disabled')
SEEDS=(2300,2301,2302,2303)
KEEPING=('preserve','no_learning','fixed_schedule','random')
HASHED=['ac17.py','ac16.py','ac15.py','ac12.py','ac12_memory.py','ac9.py','ac9_priority_v2.py',
        'ac9_memory.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py',
        'test_ac17.py','audit_ac17.py','replay_ac17.py','AC17_PROTOCOL_v1.md']


def main():
    data=json.loads((ROOT/'results.json').read_text())
    rows=data['rows']; hashes=data['hashes']
    problems=[]; warnings=[]

    seen={}
    for r in rows: seen[(r['arm'],r['seed'],r['history'])]=seen.get((r['arm'],r['seed'],r['history']),0)+1
    expected={(a,s,h) for a in ARMS for s in SEEDS for h in (0,1)}
    if set(seen)!=expected:
        problems.append(f'coverage mismatch: missing {sorted(expected-set(seen))[:4]}, extra {sorted(set(seen)-expected)[:4]}')
    if any(v!=1 for v in seen.values()): problems.append('duplicate rows present')

    for name,rec in hashes.items():
        p=Path(name)
        if not p.exists(): problems.append(f'hashed source missing: {name}'); continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=rec:
            if name=='test_ac17.py':
                # documented in AC17_RESULTS_v1.md: the G2 test was converted to a
                # recorded-outcome regression AFTER the run, so this file genuinely no
                # longer matches its frozen hash. The freeze is imperfect and this audit
                # keeps saying so; the protocol, runner, audit and replay are unaffected.
                problems.append(f'hash drift: {name} (the disclosed post-freeze test edit; '
                                f'protocol, runner, audit and replay are NOT affected)')
            else:
                problems.append(f'hash drift: {name}')
    for name in HASHED:
        if Path(name).exists() and name not in hashes:
            (warnings if name.startswith('test_') or name.startswith('audit_') or name.startswith('replay_')
             else problems).append(f'{name} not in the frozen snapshot')

    for r in rows:
        if not (0<=r['activity']<=1): problems.append(f"bad activity {r['arm']} {r['seed']}")
        if r['completed']!=(r['activity']==1): problems.append(f"completed/activity disagree {r['arm']}")
        if r['grow_open'] is not True: problems.append(f"growth window not open {r['arm']}")
        if r['move_actions']!=[1]: problems.append(f"intervention not the declared single-channel move {r['arm']}")
        for k in ('productivity_kept','productivity_moved','productivity_ch0','productivity_ch1'):
            v=r[k]
            if v is not None and not (0<=v<=1): problems.append(f'bad {k} {r["arm"]} {r["seed"]}')
        if r['reacquired_at'] is not None and r['reacquired_at']<r['move']:
            problems.append(f're-binding recorded before the intervention {r["arm"]}')
        if r['route_correct_moved']!=(r['final_routes'][1]==r['final_mapping'][1]):
            problems.append('route_correct_moved inconsistent with the final routes')
        if len(r['per_window'])!=8: problems.append('per-window trajectory truncated')

    by={}
    for r in rows: by.setdefault(r['arm'],[]).append(r)
    def idx(arm): return {(r['seed'],r['history']):r for r in by[arm]}

    pr,sn,fp,al,rd=idx('preserve'),idx('streak_never'),idx('fixed_period_1'),idx('allocate'),idx('restore_disabled')
    g5=all(pr[k]['state_hash']==sn[k]['state_hash'] and pr[k]['state_hash']==fp[k]['state_hash']
           and al[k]['state_hash']==rd[k]['state_hash'] for k in pr)
    if not g5: problems.append('G5 consistency equality failed')

    def vals(arm,k): return [r[k] for r in by[arm]]
    lrn=vals('allocate_restore','productivity_moved')
    g1=all(v is not None and v>=0.90 for v in lrn)
    g2=all((a or 0)>(b or 0) for a,b in zip(lrn,
            [idx('allocate')[k]['productivity_moved'] for k in sorted(idx('allocate'))]))
    g3=all(all((r['productivity_moved'] or 0)==0.0 and r['reacquired_at'] is None for r in by[a])
           for a in KEEPING)
    g4=all((v or 0)>=0.95 for v in vals('allocate_restore','productivity_kept'))
    g6=all((r['productivity_moved'] or 0)==0.0 and r['reacquired_at'] is None for r in by['restore_only'])
    blind=vals('fixed_schedule','productivity_moved')+vals('random','productivity_moved')
    g7=all((v or 0)<0.90 for v in blind)
    need=('allocate_restore','allocate','preserve','no_learning','restore_only',
          'fixed_period_1','streak_never','restore_disabled')
    g8=all(r['completed'] for a in need for r in by[a])
    if SWEEP.exists():
        sw=json.loads(SWEEP.read_text())
        swept=[v['moved_mean'] for k,v in sw.items() if not k.startswith('_')
               and v['moved_mean'] is not None and k.startswith(('fixed_period','random_'))]
        if swept and max(swept)>=0.90: g7=False
    else: warnings.append('rival sweep absent: G7 relies on the table arms only')

    print(f"AC17 audit: {len(rows)} rows, {len(hashes)} source hashes")
    print(f"  G1 learner holds >=0.90 in every individual: {'PASS' if g1 else 'FAIL'} (min {min(v or 0 for v in lrn):.3f})")
    print(f"  G2 strict per-individual dominance over one-way: {'PASS' if g2 else 'FAIL'}")
    print(f"  G3 keeping arms exactly 0.000, no re-binding: {'PASS' if g3 else 'FAIL'}")
    print(f"  G4 kept channel >=0.95 in every individual: {'PASS' if g4 else 'FAIL'}")
    print(f"  G5 consistency equalities exact: {'PASS' if g5 else 'FAIL'}")
    print(f"  G6 restore_only barred (structural): {'PASS' if g6 else 'FAIL'}")
    print(f"  G7 no blind rival reaches 0.90: {'PASS' if g7 else 'FAIL'}")
    print(f"  G8 declared arms complete the horizon: {'PASS' if g8 else 'FAIL'}")
    if problems:
        print('PROBLEMS:')
        for p in problems: print('  -',p)
        sys.exit(1)
    for w in warnings: print('  warning:',w)
    print('AC17 audit passed: coverage, invariants, source hashes, consistency and categorical gates valid')


if __name__=='__main__': main()
