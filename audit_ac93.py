"""AC93 audit: re-derive coverage, arm invariants, the W-dependence contrast (the copy stalls with
zero W-catalyzed writes in BOTH the gated and ungated architectures), the generic-decode link,
source hashes, and the gate recomputation, from the saved tables, without simulating.

Verification tools are NOT hashed into the frozen snapshot (AC17's rule); any drift is disclosed in
the results doc, not silently refreshed."""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac5_program as prog
import ac93


def main(root='ac93_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    transition = results.get('transition')
    n_conds = len(results.get('conds', ac93.ARMS))
    problems = []

    if len(rows) != len(seeds) * 2 * 11:
        problems.append(f'row count {len(rows)} != expected {len(seeds) * 2 * 11}')

    if transition != 'none':
        problems.append(f'transition {transition} != none (the coordinator question runs without a move)')

    keys = [(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,damage,corrupt)')

    if not set(seeds).isdisjoint(range(8)) or not set(seeds).isdisjoint(range(4304)):
        problems.append(f'final seeds {seeds} not disjoint from engineering 0-7 and prior <= 4303')

    for name in ac93.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # ---- arm invariants (re-derived from rows, no simulation) ----
    for r in rows:
        if r['arm'] in ('W_block', 'W_rescue', 'W_block_ungated') and r['damage'] and not r['corrupt']:
            if r['succession_start_observed'] != ac93.FORCE_TICK:
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: succession not forced at "
                                f"FORCE_TICK ({r['succession_start_observed']})")
            if r['first_W_empty'] is None or not (r['first_W_empty'] <= ac93.FORCE_TICK + 63):
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: first_W_empty not within "
                                f"the W lifetime ({r['first_W_empty']})")
            if r['phase_at_W_empty'] != ac93.PHASE_COPY:
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: W emptied outside COPY "
                                f"(phase {r['phase_at_W_empty']})")
            # the W-dependence contrast: every W-catalyzed write stopped over the stall window
            if r['window_succ_writes'] != 0 or r['window_ctrl_writes'] != 0:
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: a W-catalyzed write ran over "
                                f"the stall window (succ={r['window_succ_writes']}, "
                                f"ctrl={r['window_ctrl_writes']})")
            if r['phase_changes_during_stall'] != 0:
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: phase advanced during the stall")
        if r['arm'] in ('W_block', 'W_block_ungated') and r['damage'] and not r['corrupt']:
            if r['succession_completed'] != 0 or r['completed'] or r['W'] != 0 or r['C'] != 0:
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: expected an incomplete, fatal "
                                f"stall (completed={r['completed']}, W={r['W']}, C={r['C']})")
            if r['description_correct_at_death'] != ac93.DESC_BITS:
                problems.append(f"{r['arm']} {r['seed']}/{r['history']}: description not intact at death "
                                f"({r['description_correct_at_death']}) -- the cut must remove machinery, "
                                f"not content")
        if r['arm'] == 'W_rescue' and r['damage'] and not r['corrupt']:
            if not (r['phase_at_rescue'] == ac93.PHASE_COPY and r['W_at_rescue'] == 0):
                problems.append(f"W_rescue {r['seed']}/{r['history']}: not stalled at rescue "
                                f"(phase {r['phase_at_rescue']}, W {r['W_at_rescue']})")
            if not (r['succession_completed'] == 1 and r['completed'] and r['W'] == 3 and r['C'] == 2):
                problems.append(f"W_rescue {r['seed']}/{r['history']}: did not resume and survive "
                                f"(done={r['succession_completed']}, completed={r['completed']}, "
                                f"W={r['W']}, C={r['C']})")

    # ---- the generic decode reproduces the ACQUIRED program (order-preserving), generic over syntax
    for seed in list(range(12)) + seeds:
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        o.body.traces[1, :ac93.DESC_BITS] = ac93.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac93.build_program(ac93.read_slot(o, 0))
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')

    # ---- gates recomputed from the rows (no simulation) ----
    g = ac93.gates(rows)
    g['G8_completeness_determinism'] = len(rows) == len(seeds) * 2 * 11
    if any(not v for v in g.values() if v is not None):
        problems.append('a gate recomputed as FAIL')

    # ---- reported summary ----
    def pick(arm):
        return [r for r in rows if r['arm'] == arm and r['damage'] and not r['corrupt']]
    for arm in ('W_block', 'W_rescue', 'W_block_ungated'):
        rs = pick(arm)
        if not rs:
            continue
        print(f"{arm:16s} start {[r['succession_start_observed'] for r in rs][:1]}  "
              f"W_empty {sorted(set(r['first_W_empty'] for r in rs))}  "
              f"phase_chg {sorted(set(r['phase_changes_during_stall'] for r in rs))}  "
              f"win_succ {sorted(set(r['window_succ_writes'] for r in rs))}  "
              f"win_ctrl {sorted(set(r['window_ctrl_writes'] for r in rs))}  "
              f"done {sorted(set(r['succession_completed'] for r in rs))}  "
              f"dead {sorted(set(r['first_dead'] for r in rs if r['first_dead'] is not None))}  "
              f"W {sorted(set(r['W'] for r in rs))}  C {sorted(set(r['C'] for r in rs))}")

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; 5 arms; 11 conditions/individual')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants, W-dependence contrast (copy stalls in both '
          'architectures), generic-decode link, hashes, gates recomputed without simulating')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac93_results_v1') else 1)
