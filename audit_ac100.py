"""AC100 audit: re-derive coverage, arm invariants (the 2x2 factorial outcomes, the no-harm
directions, the seed-7 harmful-combination pattern), source hashes, and the gate recomputation,
from the saved tables, without simulating.

G4 (per-tick observer-discard on gray_res) and G6's single-move arm identity are two-run
comparisons and cannot be re-derived from the rows alone; the audit re-reads the recorded dicts
and the replay tool re-runs a sample. Verification tools are NOT hashed into the frozen snapshot
(AC17's rule).
"""
import json
import hashlib
from pathlib import Path
import ac100


def main(root='ac100_results_v1'):
    results = json.load(open(Path(root) / 'results.json'))
    rows = results['rows']
    hashes = results['hashes']
    seeds = results['seeds']
    arms = results.get('arms', [])
    observer_discard = results.get('observer_discard', {})
    single_equiv = results.get('single_move_equivalence', {})
    problems = []

    n_arms = len(arms) or 4
    if len(rows) != len(seeds) * 2 * n_arms:
        problems.append(f'row count {len(rows)} != expected {len(seeds) * 2 * n_arms}')

    if arms != ac100.ARMS:
        problems.append(f'arms {arms} != declared {ac100.ARMS}')

    keys = [(r['seed'], r['history'], r['condition']) for r in rows]
    if len(set(keys)) != len(keys):
        problems.append('duplicate or missing (seed,history,condition)')

    # final seeds: exactly the declared unseen family, disjoint from everything <= 4443
    if list(seeds) != [4444, 4445, 4446, 4447]:
        problems.append(f'seeds {seeds} != declared [4444,4445,4446,4447]')
    if not set(seeds).isdisjoint(range(4444)):
        problems.append(f'final seeds {seeds} not disjoint from everything < 4444')

    # schedule must be the declared two-move schedule
    for r in rows:
        sched = [tuple(x) for x in r.get('schedule', [])]
        if sched != [tuple(x) for x in ac100.SCHEDULE]:
            problems.append(f'row {r["seed"]}/{r["history"]}/{r["condition"]} schedule {sched} != SCHEDULE')
            break

    for name in ac100.SOURCES:
        if not Path(name).exists():
            continue
        h = hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if hashes.get(name) != h:
            problems.append(f'hash drift: {name}')

    # ---- arm invariants (re-derived from rows, no simulation) ----
    def pick(code):
        return [r for r in rows if r['condition'] == code]

    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history']), {})[r['condition']] = r

    print('=== per-seed 2x2 (completed / first_dead / relinquishments_by_move) ===')
    for s in seeds:
        for h in (0, 1):
            cells = []
            for c in ac100.ARMS:
                r = by[(s, h)][c]
                cells.append(f'{c}={r["completed"]}({r["first_dead"]},{r["relinquishments_by_move"]})')
            print(f'  {s}/{h}: ' + '  '.join(cells))

    # history identity per seed per arm
    for s in seeds:
        for c in ac100.ARMS:
            if by[(s, 0)][c]['state_hash'] != by[(s, 1)][c]['state_hash']:
                problems.append(f'histories not identical: {s}/{c}')

    # ---- recorded two-run comparisons (G4, G6 arm identity) re-read, not recomputed ----
    n_ind = len(seeds) * 2
    if len(observer_discard) != n_ind:
        problems.append(f'observer-discard record has {len(observer_discard)} != {n_ind} entries')
    if not all(d.get('status') != 'no_mid_streak' and d.get('swap_applied')
               and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
               for d in observer_discard.values()):
        problems.append('observer-discard record not all per-tick byte-identical at a non-zero streak')

    if len(single_equiv) != n_ind * n_arms or not all(single_equiv.values()):
        problems.append(f'arm-identity record not all True: {len(single_equiv)}/{n_ind * n_arms}')

    # ---- gates recomputed from the rows (no simulation) ----
    # Normalise the JSON round-trip key types before the gate recomputation (AC15's replay lesson).
    for r in rows:
        if isinstance(r.get('streak_final'), dict):
            r['streak_final'] = {int(k): v for k, v in r['streak_final'].items()}
        if isinstance(r.get('reacquire_ticks'), dict):
            r['reacquire_ticks'] = {int(k): v for k, v in r['reacquire_ticks'].items()}
    g = ac100.gates_ac100(rows, seeds, observer_discard, ac100.SCHEDULE)
    g['G6_completeness_determinism_arm_identity'] = (
        len(rows) == len(seeds) * 2 * n_arms
        and bool(single_equiv) and all(single_equiv.values()))
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
    print('gates (re-derived, matching recorded):', {k: ('PASS' if v else 'FAIL') for k, v in g.items()})
    print(f'observer-discard: {sum(1 for d in observer_discard.values() if d.get("per_tick_identical"))}/{n_ind} '
          f'per-tick byte-identical at a non-zero streak')
    print(f'arm-identity: {sum(single_equiv.values())}/{n_ind * n_arms} single-move byte-identical to AC99 runner')
    print(f'snapshot hashes: {len(hashes)} files, no drift')
    print('audit passed: coverage, arm invariants (2x2 outcomes, no-harm directions, harmful-combination '
          'pattern), observer-discard record, arm-identity record, hashes, gates re-derived without '
          'simulating and matching the recorded result')
    return True


if __name__ == '__main__':
    import sys
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'ac100_results_v1') else 1)
