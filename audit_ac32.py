"""audit_ac32.py -- independent checks on the frozen AC32 run. Exits nonzero on any audit failure.

It verifies provenance, arithmetic and internal consistency. It does NOT treat the recorded G2 failure
as an audit failure: a falsified claim is a result, not a defect.
"""
import hashlib
import json
import sys
from pathlib import Path
import ac32_reacquire as ac

ROOT=Path('ac32_results_v1')
fails=[]


def check(cond,msg):
    if not cond: fails.append(msg)


def main():
    check(ROOT.is_dir(),'results directory missing')
    snapshot=json.loads((ROOT/'pre_run_snapshot.json').read_text())
    results=json.loads((ROOT/'results.json').read_text())
    rows=[json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]

    # 1. provenance: every hashed source must still hash the same
    for name,digest in snapshot.items():
        p=Path(name)
        if not p.exists(): fails.append(f'hashed source missing: {name}'); continue
        now=hashlib.sha256(p.read_bytes()).hexdigest()
        check(now==digest,f'source drift: {name}')

    # 2. shape
    check(len(rows)==len(results['seeds'])==12,f'row count {len(rows)}')
    check(all(sorted(k for k in r if k!="seed")==sorted(ac.ARMS) for r in rows),'arm coverage')

    # 3. gates recomputed from the rows must equal the stored gates
    recomputed=ac.gates(rows); recomputed['G7_determinism']=results['gates']['G7_determinism']
    check(recomputed==results['gates'],'stored gates disagree with recomputation from the rows')

    # 4. the recorded summary must match the rows
    for arm,vals in results['summary'].items():
        posts=[r[arm]['post'] for r in rows]
        check(abs(vals['min']-min(posts))<1e-9,f'{arm} min mismatch')
        check(abs(vals['mean']-sum(posts)/len(posts))<1e-9,f'{arm} mean mismatch')
        check(abs(vals['max']-max(posts))<1e-9,f'{arm} max mismatch')

    # 5. the falsification must still be recorded as such
    check(results['gates']['G2_learner_worst_at_or_above_bar'] is False,
          'G2 is no longer recorded as failed -- AC32 is falsified as written')
    check(results['bar']==12.00,'bar changed after the protocol')

    # 6. the runner must be unable to overwrite its own output
    try:
        ac.main(seeds=(),root='ac32_results_v1')
        fails.append('the runner was able to reuse an existing results directory')
    except FileExistsError:
        pass

    if fails:
        print('AC32 audit FAILED:')
        for f in fails: print('  -',f)
        return 1
    print(f'AC32 audit passed: {len(rows)} rows, {len(snapshot)} hashed sources identical, '
          f'gates and summary recomputed consistently, G2 still recorded as FAILED (the '
          f'falsification is preserved), and the results directory cannot be overwritten.')
    return 0


if __name__=='__main__':
    sys.exit(main())
