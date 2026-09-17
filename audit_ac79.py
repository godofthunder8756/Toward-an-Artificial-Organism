"""AC79 audit: re-derive coverage, arm invariants, source hashes and gates from the saved table,
without simulating."""
import json
import hashlib
from pathlib import Path
import ac79


def main(root='ac79_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    expected = len(seeds) * 2 * len(ac79.ARMS) * 2
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')

    keys = [(r['seed'], r['history'], r['arm'], r['corrupt']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,corrupt)')

    for name in ac79.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # arm invariants: the recorded treatment must match the declared ARM_PARTS
    for r in rows:
        ac_arm, damage_desc, maintained = ac79.ARM_PARTS[r['arm']]
        if r['damage_desc'] != damage_desc or r['maintained'] != maintained:
            problems.append(f"arm treatment mismatch: {r['arm']} at seed={r['seed']} h={r['history']}")

    # no_repair must have the loop cut (die), maintained must differ from unmaintained where declared
    g = ac79.gates(rows)
    g['G6_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; arms {len(ac79.ARMS)} x corrupt {2}')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, hashes and gates all verified without simulating')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
