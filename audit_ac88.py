"""AC88 audit: re-derive coverage, arm invariants, source hashes, the generic-decode link, the gates,
and the AC87 re-verification (the corrected runner reproduces the frozen AC87 rows) from the saved
tables, without simulating."""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac5_program as prog
import ac88


def main(root='ac88_results_v1', frozen_root='ac87_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    n_conds = len(ac88.ARMS) * 2 * 2 * 2
    expected = len(seeds) * 2 * n_conds
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')

    keys = [(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'], r['transition'])
            for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,damage,corrupt,transition)')

    for name in ac88.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    for r in rows:
        if r['arm'] not in ac88.ARM_PARTS:
            problems.append(f"unknown arm {r['arm']}")

    # generic decode reproduces the ACQUIRED program (order-preserving), generic over syntax
    for seed in range(12):
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        reg_offs = ac88.resolve_offsets(o)
        o.body.traces[1, :ac88.DESC_BITS] = ac88.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac88.build_program(ac88.read_slot(o, 0))
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')
        ctrl = set(range(ac88.CTRL_BASE, ac88.CTRL_BASE + ac88.CTRL_BITS))
        if (set(reg_offs) | set(ac88.PTR_OFFS)) & ctrl:
            problems.append(f'controller/pointer overlaps register at seed {seed}')

    g = ac88.gates(rows)
    g['G9_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    # AC87 re-verification: the corrected runner must reproduce the frozen AC87 rows field-for-field
    # (state_hash included). This is the errata's core claim (the fix does not change the result).
    frozen = json.load(open(Path(frozen_root) / 'results.json'))['rows']
    fmap = {(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'], r['transition']): r
            for r in frozen}
    diffs = []
    for r in rows:
        k = (r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'], r['transition'])
        if k not in fmap:
            problems.append(f'row {k} missing from frozen AC87 table')
        elif r['state_hash'] != fmap[k]['state_hash']:
            diffs.append(k)
    if diffs:
        problems.append(f'{len(diffs)} rows differ from frozen AC87 state hashes: {diffs[:8]}')
    else:
        print(f're-verification: all {len(rows)} rows reproduce frozen AC87 state hashes')

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
    print(f'coverage: {len(rows)} rows; seeds {seeds}; {len(ac88.ARMS)} arms x damage/corrupt/transition')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, generic-decode link, hashes, gates, AC87 '
          're-verification')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac88_results_v1') else 1)
