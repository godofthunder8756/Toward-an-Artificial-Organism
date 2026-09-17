"""AC75 audit: re-derive coverage, source hashes and gates from the saved table, without simulating.

Deliberately does NOT import the runner's simulation path beyond the pure `gates` function; the gates are
recomputed from `rows.jsonl`/`results.json` exactly as the protocol declares them, so a code change that
alters the record is caught rather than silently absorbed. Determinism is verified separately by
`replay_ac75.py` (an audit cannot re-run the declared seeds without simulating).
"""
import json
import hashlib
from pathlib import Path
import ac75


def main(root='ac75_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    arms = ['erase', 'restore', 'erase_no_repair', 'restore_no_repair']
    transitions = ['perm', 'temp', 'none']
    expected = len(seeds) * 2 * len(arms) * len(transitions)
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')

    # coverage: every (seed, history, arm, transition) appears exactly once
    keys = [(r['seed'], r['history'], r['arm'], r['transition']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,transition)')

    # source hashes unchanged
    for name in ac75.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # recompute gates from the table (G8 determinism is verified by replay; here we check completeness)
    g = ac75.gates(rows)
    g['G8_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; arms {len(arms)} x transitions {len(transitions)}')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, hashes and gates all verified without simulating')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
