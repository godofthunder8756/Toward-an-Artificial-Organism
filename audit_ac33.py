"""audit_ac33.py -- independent checks on the frozen AC33 run. Exits nonzero on any audit failure."""
import hashlib
import json
import sys
from pathlib import Path
import ac33_reacquire as ac33

ROOT=Path('ac33_results_v1')
fails=[]


def check(cond,msg):
    if not cond: fails.append(msg)


def main():
    check(ROOT.is_dir(),'results directory missing')
    snapshot=json.loads((ROOT/'pre_run_snapshot.json').read_text())
    results=json.loads((ROOT/'results.json').read_text())
    rows=[json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]

    # 1. provenance: the snapshot must cover the protocol's declared list, and every hash must hold
    declared=ac33.preflight()
    check(sorted(snapshot)==sorted(declared),
          f'snapshot {sorted(snapshot)} != declared {sorted(declared)}')
    for name,digest in snapshot.items():
        p=Path(name)
        if not p.exists(): fails.append(f'hashed source missing: {name}'); continue
        check(hashlib.sha256(p.read_bytes()).hexdigest()==digest,f'source drift: {name}')

    # 2. shape
    check(len(rows)==12,f'row count {len(rows)}')
    check(all(sorted(k for k in r if k!='seed')==sorted(ac33.ARMS) for r in rows),'arm coverage')

    # 3. gates recomputed from the rows must equal the stored gates
    recomputed=ac33.gates(rows); recomputed['G7_determinism']=results['gates']['G7_determinism']
    check(recomputed==results['gates'],'stored gates disagree with recomputation')

    # 4. summary arithmetic
    for arm,vals in results['summary'].items():
        posts=[r[arm]['post'] for r in rows]
        check(abs(vals['min']-min(posts))<1e-9,f'{arm} min mismatch')
        check(abs(vals['mean']-sum(posts)/len(posts))<1e-9,f'{arm} mean mismatch')
        check(abs(vals['max']-max(posts))<1e-9,f'{arm} max mismatch')

    # 5. the recorded verdict must stay a pass, and the bar must not have moved
    check(all(v for k,v in results['gates'].items() if k!='G7_determinism') and
          results['gates']['G7_determinism'] is True,'a gate is no longer recorded as passing')
    check(results['bar']==12.00,'bar changed after the protocol')
    check(results['seeds']==list(range(3400,3412)),'final seeds changed')

    # 6. the runner cannot overwrite its output
    try:
        ac33.main(seeds=(),root='ac33_results_v1')
        fails.append('the runner reused an existing results directory')
    except FileExistsError:
        pass

    if fails:
        print('AC33 audit FAILED:')
        for f in fails: print('  -',f)
        return 1
    print(f'AC33 audit passed: {len(rows)} rows; {len(snapshot)} hashed sources match the protocol\'s '
          f'declared list ({len(declared)}) and are unchanged; gates and summary recomputed '
          f'consistently; bar 12.00 and seeds 3400-3411 unchanged; results directory cannot be '
          f'overwritten.')
    return 0


if __name__=='__main__':
    sys.exit(main())
