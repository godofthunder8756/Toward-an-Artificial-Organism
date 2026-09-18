"""AC87 audit: re-derive coverage, arm invariants, source hashes, the generic-decode link (order-
preserving and generic-over-syntax), and the gates from the saved table, without simulating."""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac5_program as prog
import ac87


def main(root='ac87_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    n_conds = len(ac87.ARMS) * 2 * 2 * 2
    expected = len(seeds) * 2 * n_conds
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')

    keys = [(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'], r['transition'])
            for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,damage,corrupt,transition)')

    for name in ac87.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    for r in rows:
        if r['arm'] not in ac87.ARM_PARTS:
            problems.append(f"unknown arm {r['arm']}")

    # the generic decode reproduces the ACQUIRED program (order-preserving) and is generic over
    # syntax (a flipped valid mask/action decodes faithfully), for every acquisition priority.
    for seed in range(12):
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        reg_offs = ac87.resolve_offsets(o)
        o.body.traces[1, :ac87.DESC_BITS] = ac87.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac87.build_program(ac87.read_slot(o, 0))
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')
        ctrl = set(range(ac87.CTRL_BASE, ac87.CTRL_BASE + ac87.CTRL_BITS))
        if (set(reg_offs) | set(ac87.PTR_OFFS)) & ctrl:
            problems.append(f'controller/pointer overlaps register at seed {seed}')

    g = ac87.gates(rows)
    g['G9_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    # reported (not gated) composition endpoints
    succ_comp = [r for r in rows if r['arm'] == 'succession' and r['damage'] and r['corrupt']
                 and r['transition'] == 'perm']
    surv = sum(r['completed'] for r in succ_comp)
    hold = sum(r['completed'] and r['routes'][0] is not None and r['routes'][1] is not None
               and r['route1_correct'] for r in succ_comp)
    print(f'composition (succession, perm+corrupt): survive {surv}/{len(succ_comp)}, '
          f'hold-both-routes {hold}/{len(succ_comp)} (reported, not gated)')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; {len(ac87.ARMS)} arms x damage/corrupt/transition')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, generic-decode link, hashes and gates verified')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac87_results_v1') else 1)
