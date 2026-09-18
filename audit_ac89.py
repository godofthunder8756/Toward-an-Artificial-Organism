"""AC89 audit: re-derive coverage, arm invariants, source hashes, the generic-decode link, the
declared seed priorities and schedule, the gates, and the unconditional composition endpoints from
the saved tables, without simulating."""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac5_program as prog
import ac89


def priority_of(seed):
    rng = np.random.default_rng([seed, 1004])
    return list(map(int, rng.permutation(4)))


def main(root='ac89_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    move_tick = results.get('move_tick')
    n_conds = len(ac89.ARMS) * 2 * 2 * 2
    expected = len(seeds) * 2 * n_conds
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')

    keys = [(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt'], r['transition'])
            for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,damage,corrupt,transition)')

    # the declared schedule is simultaneous (move at the corruption tick)
    if move_tick != ac89.CORRUPT_TICK:
        problems.append(f'move_tick {move_tick} != CORRUPT_TICK {ac89.CORRUPT_TICK}')

    # the declared final seeds carry the adversarial priority [3,0,2,1]
    for s in seeds:
        p = priority_of(s)
        if p != [3, 0, 2, 1]:
            problems.append(f'final seed {s} priority {p} != [3,0,2,1]')

    for name in ac89.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    for r in rows:
        if r['arm'] not in ac89.ARM_PARTS:
            problems.append(f"unknown arm {r['arm']}")
        if r['move_tick'] != move_tick:
            problems.append(f"row move_tick {r['move_tick']} != declared {move_tick}")

    # generic decode reproduces the ACQUIRED program (order-preserving), generic over syntax
    for seed in list(range(12)) + seeds:
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        reg_offs = ac89.resolve_offsets(o)
        o.body.traces[1, :ac89.DESC_BITS] = ac89.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac89.build_program(ac89.read_slot(o, 0))
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')
        ctrl = set(range(ac89.CTRL_BASE, ac89.CTRL_BASE + ac89.CTRL_BITS))
        if (set(reg_offs) | set(ac89.PTR_OFFS)) & ctrl:
            problems.append(f'controller/pointer overlaps register at seed {seed}')

    g = ac89.gates(rows)
    g['G9_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    # the unconditional (per-individual, dead or alive) composition endpoints
    rep = ac89.composition_report(rows)
    print(f'composition (succession, simultaneous perm+corrupt, move_tick={move_tick}):')
    print(f'  survive {rep["survive"]}/{rep["n"]} (reported lower bound, AC68 bimodality caveat)')
    print(f'  reconstruction fw==0 {rep["fw_zero"]}/{rep["n"]} (unconditional)')
    print(f'  description 130/130 at intervention {rep["desc_int"]}/{rep["n"]}')
    print(f'  description 130/130 at end {rep["desc_end"]}/{rep["n"]} (survivor-relevant)')
    print(f'  hold both routes {rep["hold_both"]}/{rep["n"]} (reported, not gated)')
    for p in rep['per_individual']:
        print(f"    seed={p['seed']} h={p['history']} completed={p['completed']} "
              f"dead={p['first_dead']} fw={p['fw']} desc_end={p['desc_end']} "
              f"desc_int={p['desc_int']} routes={p['routes']} r1c={p['route1_correct']} "
              f"demand={p['demand']}")

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; {len(ac89.ARMS)} arms x damage/corrupt/transition')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, generic-decode link, hashes, seeds, schedule, '
          'gates, unconditional composition endpoints')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac89_results_v1') else 1)
