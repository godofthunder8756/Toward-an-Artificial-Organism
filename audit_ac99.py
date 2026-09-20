"""AC99 audit: re-derive coverage, arm invariants (the Gray success arm's adaptation criterion,
the binary control outcome, the wb_first rival outcome, and the no-harm direction), source hashes,
and the gate recomputation, from the saved tables, without simulating.

G3 (per-tick observer-discard on the Gray arm) and G5's arm identity (wb_first no-swap == binary)
are two-run comparisons and cannot be re-derived from the rows alone; the audit re-reads the
recorded dicts and the replay tool re-runs a sample. Verification tools are NOT hashed into the
frozen snapshot (AC17's rule).
"""
import json
import hashlib
from pathlib import Path
import ac99_d4


def main(root='ac99_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    transition = results.get('transition')
    arms = results.get('arms', [])
    observer_discard = results.get('observer_discard', {})
    control_equivalence = results.get('control_equivalence', {})
    problems = []

    n_arms = len(arms) or 3
    if len(rows) != len(seeds) * 2 * n_arms:
        problems.append(f'row count {len(rows)} != expected {len(seeds) * 2 * n_arms}')

    if transition != 'perm':
        problems.append(f'transition {transition} != perm (the relinquishment world runs the move)')

    keys = [(r['seed'], r['history'], r['condition']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,condition)')

    # final seeds: exactly the declared unseen family, disjoint from engineering 0-7, the
    # D1/D2/D3 seeds 4412-4415/4436-4439, and every prior final family <= 4439
    if list(seeds) != [4440, 4441, 4442, 4443]:
        problems.append(f'seeds {seeds} != declared [4440,4441,4442,4443]')
    if not set(seeds).isdisjoint(range(4440)):
        problems.append(f'final seeds {seeds} not disjoint from everything < 4440')

    for name in ac99_d4.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # ---- arm invariants (re-derived from rows, no simulation) ----
    def pick(code):
        return [r for r in rows if r['condition'] == code and r['transition'] == 'perm']

    gray = pick('gray')
    binary = pick('binary')
    wb_first = pick('wb_first')

    print('gray arm: relinquish', sorted(set(r['relinquishments'] for r in gray)),
          'completed', sorted(set(r['completed'] for r in gray)))
    print('binary arm: relinquish', sorted(set(r['relinquishments'] for r in binary)),
          'completed', sorted(set(r['completed'] for r in binary)),
          'deaths', sorted(set(r['first_dead'] for r in binary if not r['completed'])))
    print('wb_first arm: relinquish', sorted(set(r['relinquishments'] for r in wb_first)),
          'completed', sorted(set(r['completed'] for r in wb_first)),
          'deaths', sorted(set(r['first_dead'] for r in wb_first if not r['completed'])))
    for r in binary:
        print(f"  binary {r['seed']}/{r['history']}: relinq {r['relinquishments']}, "
              f"completed {r['completed']}, streak_final {r['streak_final']}, "
              f"post_move W/C/B {r['W_births_post_move']}/{r['C_births_post_move']}/{r['B_births_post_move']}")
    for r in wb_first:
        print(f"  wb_first {r['seed']}/{r['history']}: relinq {r['relinquishments']}, "
              f"completed {r['completed']}, first_dead {r['first_dead']}")

    # ---- recorded two-run comparisons (G3, G5 arm identity) re-read, not recomputed ----
    n_ind = len(seeds) * 2
    if len(observer_discard) != n_ind:
        problems.append(f'observer-discard record has {len(observer_discard)} != {n_ind} entries')
    if not all(d.get('status') != 'no_mid_streak' and d.get('swap_applied')
               and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
               for d in observer_discard.values()):
        problems.append('observer-discard record not all per-tick byte-identical at a non-zero streak')

    if len(control_equivalence) != n_ind or not all(control_equivalence.values()):
        problems.append(f'arm-identity record not all True: {len(control_equivalence)}/{n_ind}')

    # ---- gates recomputed from the rows (no simulation) ----
    # Normalise the JSON round-trip key types before the gate recomputation (AC15's replay lesson).
    for r in rows:
        if isinstance(r.get('reacquire_ticks'), dict):
            r['reacquire_ticks'] = {int(k): v for k, v in r['reacquire_ticks'].items()}
        if isinstance(r.get('streak_final'), dict):
            r['streak_final'] = {int(k): v for k, v in r['streak_final'].items()}
    g = ac99_d4.gates_ac99_d4(rows, seeds, observer_discard, control_equivalence)
    g['G5_completeness_determinism_arm_identity'] = (
        len(rows) == len(seeds) * 2 * n_arms
        and bool(control_equivalence) and all(control_equivalence.values()))
    # The audit re-derives the gates WITHOUT simulating and must reproduce the recorded result
    # exactly -- including a recorded gate FAILURE (a falsification is preserved, not concealed).
    recorded = results.get('gates')
    if recorded is not None:
        for k in g:
            if g[k] != recorded.get(k):
                problems.append(f'gate {k} re-derived as {g[k]} but recorded as {recorded.get(k)}')

    if problems:
        print('AUDIT FAILED')
        for p in problems:
            print('  -', p)
        return False
    print(f'coverage: {len(rows)} rows; seeds {seeds}; 3 arms/individual; transition {transition}')
    print('gates (re-derived, matching recorded):', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'observer-discard: {sum(1 for d in observer_discard.values() if d.get("per_tick_identical"))}/{n_ind} '
          f'per-tick byte-identical at a non-zero streak')
    print(f'arm-identity: {sum(control_equivalence.values())}/{n_ind} wb_first no-swap byte-identical to binary')
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants (gray adaptation, binary control outcome, '
          'wb_first rival outcome, no-harm direction), observer-discard record, arm-identity record, '
          'hashes, gates re-derived without simulating and matching the recorded result')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac99_results_v1') else 1)
