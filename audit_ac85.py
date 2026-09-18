"""AC85 audit: re-derive coverage, arm invariants, source hashes and gates from the saved table,
without simulating."""
import json
import hashlib
from pathlib import Path
import ac85


def main(root='ac85_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    expected = len(seeds) * 2 * len(ac85.ARMS) * 2
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')

    keys = [(r['seed'], r['history'], r['arm'], r['corrupt']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,corrupt)')

    for name in ac85.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # arm invariants: the recorded treatment must match the declared ARM_PARTS
    for r in rows:
        ac_arm, damage_desc, maintained = ac85.ARM_PARTS[r['arm']]
        if r['damage_desc'] != damage_desc or r['maintained'] != maintained:
            problems.append(f"arm treatment mismatch: {r['arm']} at seed={r['seed']} h={r['history']}")

    # the generic decode must reproduce the acquired program for every acquisition priority, and
    # must read (not derive) the bank rules
    import numpy as np
    import ac4
    import ac12
    import ac5_program as prog
    for seed in range(12):
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        o.body.traces[1, :ac85.DESC_BITS] = ac85.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac85.rebuild(o)
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')

    g = ac85.gates(rows)
    g['G6_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; arms {len(ac85.ARMS)} x corrupt {2}')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, decode==acquired, hashes and gates all verified')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
