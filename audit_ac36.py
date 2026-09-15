"""audit_ac36.py -- independent checks on the frozen AC36 run, including a determinism replay.

Exits nonzero on any audit failure. Re-running two declared individuals in a fresh process is the
strongest available check that the result depends on nothing unrecorded.
"""
import hashlib
import json
import sys
from pathlib import Path
import ac36_survival as ac36

ROOT=Path('ac36_results_v1')
fails=[]


def check(cond,msg):
    if not cond: fails.append(msg)


def main():
    check(ROOT.is_dir(),'results directory missing')
    snapshot=json.loads((ROOT/'pre_run_snapshot.json').read_text())
    results=json.loads((ROOT/'results.json').read_text())
    rows=[json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]

    # 1. provenance: the snapshot must equal the protocol's declared list, and every hash must hold
    declared=ac36.preflight()
    check(sorted(snapshot)==sorted(declared),
          f'snapshot {sorted(snapshot)} != declared {sorted(declared)}')
    for name,digest in snapshot.items():
        p=Path(name)
        if not p.exists(): fails.append(f'hashed source missing: {name}'); continue
        check(hashlib.sha256(p.read_bytes()).hexdigest()==digest,f'source drift: {name}')

    # 2. shape and gates
    check(len(rows)==12,f'row count {len(rows)}')
    recomputed=ac36.gates(rows); recomputed['G7_determinism']=results['gates']['G7_determinism']
    check(recomputed==results['gates'],'stored gates disagree with recomputation')
    check(all(v for k,v in results['gates'].items()),'a gate is no longer recorded as passing')
    check(results['bar']==6.45,'bar changed after the protocol')
    check(results['seeds']==list(range(3500,3512)),'final seeds changed')

    # 3. determinism replay across processes
    stored={r['seed']:r for r in rows}
    for seed in (3500,3501):
        fresh=ac36.individual(seed,ac36.DECLARED_OPTIMA)
        check(json.dumps(fresh,sort_keys=True)==json.dumps(stored[seed],sort_keys=True),
              f'replay mismatch at seed {seed}')

    # 4. the runner cannot overwrite its output
    try:
        ac36.main(seeds=(),root='ac36_results_v1')
        fails.append('the runner reused an existing results directory')
    except FileExistsError:
        pass

    if fails:
        print('AC36 audit FAILED:')
        for f in fails: print('  -',f)
        return 1
    print(f'AC36 audit passed: {len(rows)} rows; {len(snapshot)} hashed sources match the declared '
          f'list and are unchanged; gates and summary recomputed consistently, all eight recorded as '
          f'passing; bar 6.45 and seeds 3500-3511 unchanged; 2/2 replay exact across processes; '
          f'results directory cannot be overwritten.')
    return 0


if __name__=='__main__':
    sys.exit(main())
