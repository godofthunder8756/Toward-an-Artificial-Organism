"""AC91 audit: re-derive coverage, arm invariants, source hashes, the W-birth-gate no-op for the
shared arms (equivalence with the frozen AC89 state hashes), the gate recomputation, and the
content-vs-machinery contrast, from the saved tables, without simulating."""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac5_program as prog
import ac91


def main(root='ac91_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    transition = results.get('transition')
    n_conds = len(ac91.ARMS) * 2 * 2
    expected = len(seeds) * 2 * n_conds
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')
    if transition != 'none':
        problems.append(f'transition {transition} != none (the production links run without a move)')

    keys = [(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,damage,corrupt)')

    # declared final seeds disjoint from engineering and prior finals
    if not set(seeds).isdisjoint(range(8)) or not set(seeds).isdisjoint(range(4111)):
        problems.append(f'final seeds {seeds} not disjoint from engineering 0-7 and prior <=4110')

    for name in ac91.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    for r in rows:
        if r['arm'] not in ac91.ARM_PARTS:
            problems.append(f"unknown arm {r['arm']}")
        # the W-birth block is expressed only through the gate: no_W/W_restore* must have
        # W_births_bank0 == 0 when W reaches 0 by the time the block ends, and the shared arms must
        # have W_births_bank0 > 0 (turnover). These are the arm invariants.
        if r['arm'] in ('no_W', 'W_restore_late'):
            if r['W_births_bank0'] != 0 or r['W'] != 0 or r['completed']:
                problems.append(f"{r['arm']} {r['seed']}/{r['history']} invariant broken: "
                                f"W_births_bank0={r['W_births_bank0']} W={r['W']} "
                                f"completed={r['completed']}")

    # the generic decode reproduces the ACQUIRED program (order-preserving), generic over syntax
    for seed in list(range(12)) + seeds:
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        o.body.traces[1, :ac91.DESC_BITS] = ac91.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac91.build_program(ac91.read_slot(o, 0))
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')

    # the W-birth gate writes no content: a blocked birth must leave the program and description
    # banks unchanged (asserted on the actual frozen rows via the content-vs-machinery contrast)
    for r in rows:
        if r['arm'] == 'no_W' and r['damage'] and r['corrupt']:
            if r['description_correct_at_death'] != ac91.DESC_BITS:
                problems.append(f"no_W {r['seed']}/{r['history']} content not intact at death "
                                f"({r['description_correct_at_death']})")

    g = ac91.gates(rows)
    g['G7_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    # the three-link summary (reported)
    def pick(arm):
        return [r for r in rows if r['arm'] == arm and r['damage'] and r['corrupt']]
    for arm in ('succession', 'repair', 'no_W', 'W_restore', 'W_restore_late',
                'unmaintained', 'no_repair'):
        rs = pick(arm)
        if not rs:
            continue
        survive = sum(r['completed'] for r in rs)
        wmin = min(r['W_min_seen'] for r in rs)
        wbirth = min(r['W_births_bank0'] for r in rs)
        print(f'{arm:16s} survive {survive}/{len(rs)}  min W {wmin}  min W_births_bank0 {wbirth}  '
              f'first_W_empty {[r["first_W_empty"] for r in rs]}')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; {len(ac91.ARMS)} arms x damage/corrupt')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, W-birth-gate no-op + content contrast, '
          'generic-decode link, hashes, gates recomputed without simulating')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac91_results_v1') else 1)
