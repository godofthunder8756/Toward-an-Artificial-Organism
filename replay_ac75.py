"""AC75 replay: sampled exact reruns from the frozen source, in a fresh process.

Re-runs a sample of declared (seed, history, arm, transition) rows and asserts they reproduce the frozen
`state_hash` (and endpoint fields) exactly. This is the determinism check the audit cannot do without
simulating. Run with `.venv/bin/python -B replay_ac75.py`.
"""
import json
from pathlib import Path
import ac75


def main(root='ac75_results_v1', n=6):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    # sample the first individual of each transition for the erase arm, plus one of each rival
    sample = [r for r in rows if r['arm'] == 'erase' and r['history'] == 0][:3]
    sample += [r for r in rows if r['arm'] in ('restore', 'erase_no_repair') and r['history'] == 0][:3]
    ok = 0
    for r in sample:
        rr = ac75.run(r['seed'], r['history'], r['arm'], r['transition'])
        match = rr['state_hash'] == r['state_hash']
        fields = all(rr[k] == r[k] for k in ('completed', 'first_dead', 'routes', 'demand',
                                             'register', 'relinquishments', 'restorations'))
        if match and fields:
            ok += 1
        else:
            print(f"MISMATCH seed={r['seed']} h={r['history']} arm={r['arm']} "
                  f"trans={r['transition']} hash_match={match} fields_match={fields}")
    print(f'replay: {ok}/{len(sample)} exact (state_hash and endpoint fields)')
    return ok == len(sample)


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
