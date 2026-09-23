"""AC107 audit: split verification — re-derive source hashes, gate set, and invariants from the
saved table WITHOUT simulating.

Distinct from replay_ac107.py (sampled exact reruns, including the determinism re-run). This file
re-reads ac107_results_v1/ and re-computes every non-determinism claim from the frozen table +
hashes. It does NOT call ac107.run().
"""
import hashlib
import json
import sys
from pathlib import Path
import ac107

ROOT = 'ac107_results_v1'
CONDITIONS = ('no_cause', 'move', 'cut')


def load(root=ROOT):
    root = Path(root)
    rows = [json.loads(l) for l in (root / 'rows.jsonl').read_text().splitlines()]
    results = json.loads((root / 'results.json').read_text())
    snapshot = json.loads((root / 'pre_run_snapshot.json').read_text())
    return root, rows, results, snapshot


def check_source_hashes(snapshot, errors):
    for name, h in sorted(snapshot.items()):
        p = Path(name)
        if not p.exists():
            errors.append(f'source missing: {name}')
            continue
        cur = hashlib.sha256(p.read_bytes()).hexdigest()
        if cur != h:
            errors.append(f'hash drift: {name} (frozen {h[:12]} vs now {cur[:12]})')


def rederive_gates(rows, seeds, observer_discard, no_cause_identity):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
    n_ind = len(seeds) * 2
    inds = [(s, h) for s in seeds for h in (0, 1)]

    def survives(r):
        return r['completed'] and r['first_dead'] is None

    cand_cut = [by[(s, h, 'cut')]['candidate'] for s, h in inds]
    cand_move = [by[(s, h, 'move')]['candidate'] for s, h in inds]
    r2_cut = [by[(s, h, 'cut')]['r2'] for s, h in inds]
    r4_move = [by[(s, h, 'move')]['r4'] for s, h in inds]
    scr_cut = [by[(s, h, 'cut')]['scramble'] for s, h in inds]

    g1_cut = all(r['bel_at_cut_end'] == 0 and (r['entry_life_at_cut_start'] or 0) > 0
                 for r in cand_cut)
    g1_move = all(r['bel_at_first_drop'] == 1 and r['relinquishments'] >= 1 for r in cand_move)
    g1 = g1_cut and g1_move and sum(r['mistakes'] for r in cand_cut + cand_move) == 0

    g2_holds = all(r['relinquishments'] == 0 for r in cand_cut)
    g2_scramble_relinq = any(r['relinquishments'] >= 1 for r in scr_cut)
    g2_scramble_dies = any((not survives(s)) and survives(c) for s, c in zip(scr_cut, cand_cut))
    g2 = g2_holds and g2_scramble_relinq and g2_scramble_dies

    g3 = len(observer_discard) == n_ind and all(
        d.get('per_tick_identical') and d.get('terminal_identical') and d.get('swap_applied')
        for d in observer_discard.values())

    g4 = all(no_cause_identity.get(f'{s}/{h}') is True for s, h in inds)

    cand_cut_surv = sum(survives(r) for r in cand_cut)
    cand_move_surv = sum(survives(r) for r in cand_move)
    g5 = (cand_cut_surv >= 12 and cand_move_surv >= 12
          and any((not survives(r)) and survives(c) for r, c in zip(r2_cut, cand_cut))
          and any((not survives(r)) and survives(c) for r, c in zip(r4_move, cand_move)))

    g7 = (ac107.HOLD_N > 7 and ac107.HOLD_N != ac107.STREAK_N
          and any(by[(s, h, 'cut')]['r2']['relinquishments']
                  != by[(s, h, 'cut')]['r4']['relinquishments'] for s, h in inds)
          and any(by[(s, h, 'move')]['r2']['relinquishments']
                  != by[(s, h, 'move')]['r4']['relinquishments'] for s, h in inds))

    return {
        'G1_discrimination': g1,
        'G2_content_causal_scramble': g2,
        'G3_state_sufficiency_observer_discard': g3,
        'G4_no_cause_identity': g4,
        'G5_comparative_advantage': g5,
        'G7_rival_distinctness': g7,
    }


def check_coverage(rows, seeds, errors):
    expected = len(seeds) * len(ac107.ARMS) * len(CONDITIONS) * 2
    if len(rows) != expected:
        errors.append(f'row count {len(rows)} != {expected}')
    tuples = {(r['seed'], r['history'], r['arm'], r['condition']) for r in rows}
    if len(tuples) != expected:
        errors.append(f'duplicate/missing (seed,history,arm,condition): {len(tuples)} != {expected}')


def check_seed_disjointness(rows, seeds, errors):
    used_prior = (set(range(8)) | set(range(4412, 4452)) | {4466, 4481, 4504, 4510}
                  | set(range(4600, 4872)) | set(range(4880, 4951))
                  | set(range(5100, 5509)) | set(range(5600, 5608)) | set(range(5700, 5708))
                  | set(range(5800, 5808)) | set(range(5900, 5908)))
    finals = {r['seed'] for r in rows}
    if finals & used_prior:
        errors.append(f'final seeds overlap prior families: {sorted(finals & used_prior)}')
    if finals != set(seeds):
        errors.append(f'final seeds in table {sorted(finals)} != declared {sorted(seeds)}')


def main():
    root, rows, results, snapshot = load()
    errors = []
    check_source_hashes(snapshot, errors)
    seeds = results['seeds']
    check_coverage(rows, seeds, errors)
    check_seed_disjointness(rows, seeds, errors)

    gates = rederive_gates(rows, seeds, results['observer_discard'], results['no_cause_identity'])
    recorded = results['gates']
    for k, v in gates.items():
        if k in recorded and recorded[k] != v:
            errors.append(f'gate {k}: re-derived {v} != recorded {recorded[k]}')

    print(f'rows={len(rows)} seeds={len(seeds)} arms={len(ac107.ARMS)} conditions={len(CONDITIONS)}')
    print('gates (re-derived, no simulation):')
    print(json.dumps(gates, indent=2))
    if errors:
        print('\nFAILURES:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('\nAC107 audit passed: source hashes valid, gates re-derived without simulating, '
          'coverage + seed-disjointness invariants hold.')


if __name__ == '__main__':
    main()
