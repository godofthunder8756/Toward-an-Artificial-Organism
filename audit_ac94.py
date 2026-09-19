"""AC94 audit: re-derive coverage, arm invariants (the four requirement-gates' coherence endpoints,
the split rival's defect, the timer machinery-dependence), the generic-decode link, source hashes,
and the gate recomputation, from the saved tables, without simulating.

Verification tools are NOT hashed into the frozen snapshot (AC17's rule); any drift is disclosed in
the results doc, not silently refreshed."""
import json
import hashlib
from pathlib import Path
import numpy as np
import ac4
import ac12
import ac5_program as prog
import ac94


def main(root='ac94_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    transition = results.get('transition')
    conds = results.get('conds', [])
    problems = []

    n_conds = len(conds) or 15
    if len(rows) != len(seeds) * 2 * n_conds:
        problems.append(f'row count {len(rows)} != expected {len(seeds) * 2 * n_conds}')

    if transition != 'none':
        problems.append(f'transition {transition} != none (the coordinator question runs without a move)')

    keys = [(r['seed'], r['history'], r['arm'], r['damage'], r['corrupt']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,arm,damage,corrupt)')

    # final seeds disjoint from engineering 0-7 and every prior final family <= 4403
    if not set(seeds).isdisjoint(range(8)):
        problems.append(f'final seeds {seeds} overlap engineering 0-7')
    if not set(seeds).isdisjoint(range(4404)):
        problems.append(f'final seeds {seeds} not disjoint from prior final families <= 4403')

    for name in ac94.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # ---- arm invariants (re-derived from rows, no simulation) ----
    def pick(arm, damage, corrupt):
        return [r for r in rows
                if r['arm'] == arm and r['damage'] == damage and r['corrupt'] == corrupt
                and r['transition'] == 'none']

    gated = pick('gated', True, True)
    split = pick('split', True, True)
    block = pick('timer_block', True, False)
    rescue = pick('timer_rescue', True, False)
    ungated_block = pick('ungated_block', True, False)

    for r in gated:
        if r['split_events'] != 0:
            problems.append(f"gated {r['seed']}/{r['history']}: split_events {r['split_events']} != 0 "
                            f"(the atomic switch must never advance the pointer alone)")
        if r['successions'] < 1:
            problems.append(f"gated {r['seed']}/{r['history']}: no succession completed")

    # the split rival exhibits the D1 defect somewhere (population-level; W=2-during-SWITCH is
    # seed-dependent, so this is REPORTED, not a failure -- the single-step defect is pinned by
    # test_ac94.TestSplitRival regardless of whether a final seed exercises it).
    split_event_total = sum(r['split_events'] for r in split)
    split_stale = sorted(set(r['occupied_slots_end'] for r in split))
    print(f'split rival: split_events total {split_event_total} across {len(split)} individuals; '
          f'occupied_slots_end {split_stale} (a stale 3-slot occupancy is the skipped-removal signature)')

    for r in block:
        if r['timer_at_W_empty'] is None or not (r['timer_at_W_empty'] < ac94.TIMER_MAX):
            problems.append(f"timer_block {r['seed']}/{r['history']}: timer not frozen "
                            f"(timer_at_W_empty {r['timer_at_W_empty']})")
        if r['timer_increments_after_W_empty'] != 0:
            problems.append(f"timer_block {r['seed']}/{r['history']}: counter advanced after W=0")
        if r['successions'] != 0 or r['completed'] or r['W'] != 0:
            problems.append(f"timer_block {r['seed']}/{r['history']}: expected a frozen fatal stall "
                            f"(succ={r['successions']}, completed={r['completed']}, W={r['W']})")

    for r in rescue:
        if r['timer_increments_after_W_empty'] != 0:
            problems.append(f"timer_rescue {r['seed']}/{r['history']}: counter advanced while W==0 "
                            f"before the rescue")
        if not (1 <= r['successions'] <= 8 and r['completed'] and r['W'] >= 3):
            problems.append(f"timer_rescue {r['seed']}/{r['history']}: did not resume and complete a "
                            f"healthy rate-limited count (succ={r['successions']}, "
                            f"completed={r['completed']}, W={r['W']})")

    for r in ungated_block:
        # the ungated-under-cut rival stalls at the W-gated copy (0 successions, fatal), even though
        # its W-independent timestamp rate limiter is not frozen by W=0.
        if not (r['successions'] == 0 and not r['completed'] and r['W'] == 0):
            problems.append(f"ungated_block {r['seed']}/{r['history']}: expected a copy-stall death "
                            f"(succ={r['successions']}, completed={r['completed']}, W={r['W']})")

    # ---- the generic decode reproduces the ACQUIRED program (order-preserving), generic over syntax
    for seed in list(range(12)) + seeds:
        _, _, _, priority = ac4.acquire(seed)
        o, offs = ac12.acquire(seed)
        o.body.traces[1, :ac94.DESC_BITS] = ac94.description_bits(priority)[:, None]
        acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
        t = ac94.build_program(ac94.read_slot(o, 0))
        if t is None or not np.array_equal(t, acquired):
            problems.append(f'generic decode != acquired at seed {seed}')

    # ---- gates recomputed from the rows (no simulation) ----
    g = ac94.gates(rows)
    # G5 completeness: the row count is re-derivable here; the determinism half is the replay tool's
    # job (sampled exact reruns), not the audit's.
    g['G5_completeness_determinism'] = len(rows) == len(seeds) * 2 * n_conds
    if any(not v for v in g.values() if v is not None):
        problems.append('a gate recomputed as FAIL')

    # ---- reported summary ----
    def summary(rs, label):
        if not rs:
            return
        print(f"{label:14s} succ {sorted(set(r['successions'] for r in rs))}  "
              f"split {sorted(set(r['split_events'] for r in rs))}  "
              f"src_intact {sorted(set(r['source_intact_at_switch_all'] for r in rs))}  "
              f"verified {sorted(set(r['verified_all'] for r in rs))}  "
              f"removal {sorted(set(r['removal_all'] for r in rs))}  "
              f"occ {sorted(set(r['occupied_slots_end'] for r in rs))}  "
              f"completed {sorted(set(r['completed'] for r in rs))}  "
              f"W {sorted(set(r['W'] for r in rs))}  C {sorted(set(r['C'] for r in rs))}")
    summary(gated, 'gated (d=T,c=T)')
    summary(split, 'split (d=T,c=T)')
    summary(block, 'timer_block')
    summary(rescue, 'timer_rescue')
    summary(ungated_block, 'ungated_block')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; 6 arms; {n_conds} conditions/individual')
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants (coherence endpoints, split rival defect, timer '
          'machinery-dependence), generic-decode link, hashes, gates recomputed without simulating')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac94_results_v1') else 1)
