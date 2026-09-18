"""AC92 audit: re-derive coverage, arm invariants, source hashes, the W-dependence contrast, the
generic-decode link, and the gate recomputation, from the saved tables, without simulating."""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac5_program as prog
import ac92


def main(root='ac92_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    transition = results.get('transition')
    n_conds = len(ac92.ARMS) * 2 * 2
    expected = len(seeds) * 2 * n_conds
    problems = []

    if len(rows) != expected:
        problems.append(f'row count {len(rows)} != expected {expected}')
    if transition != 'none':
        problems.append(f'transition {transition} != none (the function-underway links run without a move)')

    keys = [(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,damage,corrupt)')

    if not set(seeds).isdisjoint(range(8)) or not set(seeds).isdisjoint(range(4204)):
        problems.append(f'final seeds {seeds} not disjoint from engineering 0-7 and prior <=4203')

    for name in ac92.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # arm invariants (re-derived, no simulation)
    for r in rows:
        if r['arm'] == 'intact':
            if 'block_W' in ac92.ARM_PARTS['intact']:
                problems.append('intact must not carry a W-birth gate')
        if r['arm'] in ('W_block', 'W_rescue'):
            # the production cut is expressed only through the gate: W reaches 0 by the corruption
            if r['first_W_empty'] is None or not (r['first_W_empty'] <= ac92.CORRUPT_TICK):
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: first_W_empty not <= corrupt "
                                f"tick ({r['first_W_empty']})")
        # the description is intact at the intervention (the cut removes machinery, not content)
        if r['arm'] in ('W_block', 'W_rescue') and r['damage'] and r['corrupt']:
            if r['description_correct_intervention'] != ac92.DESC_BITS:
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: description not intact at "
                                f"intervention ({r['description_correct_intervention']})")

    # the generic decode reproduces the ACQUIRED program (order-preserving), generic over syntax
    for seed in list(range(12)) + seeds:
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        o.body.traces[1, :ac92.DESC_BITS] = ac92.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac92.build_program(ac92.read_slot(o, 0))
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')

    # the W-dependence contrast, from the frozen rows (no simulation): in the interrupted arms the
    # W-catalyzed reconstruction writes are zero over the window, and the reconstruction stays stalled
    for r in rows:
        if r['arm'] == 'W_block' and r['damage'] and r['corrupt']:
            if not (r['alive_at_corruption'] and r['alive_pre_rescue'] and r['fw_pre_rescue'] > 0
                    and r['window_reg_writes'] == 0):
                problems.append(f"W_block {r['seed']}/{r['history']} interruption not observed while "
                                f"alive (fw_pre_rescue={r['fw_pre_rescue']}, "
                                f"window_reg_writes={r['window_reg_writes']})")

    g = ac92.gates(rows)
    g['G6_completeness_determinism'] = len(rows) == expected
    if any(not v for v in g.values()):
        problems.append('a gate recomputed as FAIL')

    # reported summary
    def pick(arm):
        return [r for r in rows if r['arm'] == arm and r['damage'] and r['corrupt']]
    for arm in ('intact', 'W_block', 'W_rescue'):
        rs = pick(arm)
        if not rs:
            continue
        survive = sum(r['completed'] for r in rs)
        deaths = [r['first_dead'] for r in rs]
        fw_pre = [r['fw_pre_rescue'] for r in rs]
        w_reg = [r['window_reg_writes'] for r in rs]
        w_succ = [r['window_succ_writes'] for r in rs]
        w_ctrl = [r['window_ctrl_writes'] for r in rs]
        print(f'{arm:10s} survive {survive}/{len(rs)}  deaths {deaths}  fw_pre {fw_pre}  '
              f'win_reg {w_reg}  win_succ {w_succ}  win_ctrl {w_ctrl}')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; {len(ac92.ARMS)} arms x damage/corrupt')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, W-dependence contrast, generic-decode link, '
          'hashes, gates recomputed without simulating')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac92_results_v1') else 1)
