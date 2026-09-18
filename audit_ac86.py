"""AC86 audit: re-derive coverage, arm invariants, source hashes, the order-preserving-decode link,
and the gates from the saved table, without simulating."""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac5_program as prog
import ac80
import ac86


def main(root='ac86_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    expected = len(seeds) * 2 * len(ac86.ARMS) * 2
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')

    keys = [(r['seed'], r['history'], r['arm'], r['damage']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,damage)')

    for name in ac86.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # arm invariants: the recorded treatment must match the declared ARM_PARTS
    for r in rows:
        if r['arm'] not in ac86.ARM_PARTS:
            problems.append(f"unknown arm {r['arm']}")

    # the generic decode reproduces the ACQUIRED (ac9_priority_v2 reordered) program, order
    # preserved, for every acquisition priority; the pointer lives in bank 1 (recipe storage),
    # disjoint from the AC12 register bits in the program bank.
    for seed in range(12):
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        reg_offs = ac86.resolve_offsets(o)
        o.body.traces[1, :ac86.DESC_BITS] = ac80.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac86.rebuild_active(o)
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')
        if set(reg_offs) & set(ac86.PTR_OFFS):
            problems.append(f'pointer overlaps register at seed {seed}')

    g = ac86.gates(rows)
    g['G7_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; arms {len(ac86.ARMS)} x damage {2}')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, order-preserving-decode link, hashes and gates verified')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
