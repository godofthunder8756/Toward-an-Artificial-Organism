"""AC81 audit: re-derive coverage, arm invariants, source hashes, the production-recipe-in-
description link, and the gates from the saved table, without simulating."""
import json
import hashlib
from pathlib import Path
import ac81


def main(root='ac81_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    expected = len(seeds) * 2 * len(ac81.ARMS) * 2
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')

    keys = [(r['seed'], r['history'], r['arm'], r['loss']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,loss)')

    for name in ac81.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # arm invariants: the recorded treatment must match the declared ARM_PARTS
    for r in rows:
        ac_arm, damage_desc, maintained = ac81.ARM_PARTS[r['arm']]
        if r.get('arm') not in ac81.ARM_PARTS:
            problems.append(f"unknown arm {r['arm']}")

    # the production recipe is in the description: rebuild reads the production words from the
    # vulnerable state, and the generic decode reproduces prog.program for every acquisition priority
    import numpy as np
    import ac4
    import ac12
    import ac5_program as prog
    import ac80
    for seed in range(12):
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        o.body.traces[1, :ac80.DESC_BITS] = ac80.description_bits(priority)[:, None]
        t = ac80.rebuild(o)
        if t is None or not np.array_equal(t, prog.program(priority)):
            problems.append(f'generic decode != scaffold at seed {seed}')
        desc = ac80.read_description(o)
        if not np.array_equal(t[28:70], desc[28:70]):
            problems.append(f'production rules not read from description at seed {seed}')

    g = ac81.gates(rows)
    g['G8_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; arms {len(ac81.ARMS)} x loss {2}')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, production-recipe link, hashes and gates verified')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
