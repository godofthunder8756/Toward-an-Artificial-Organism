"""AC108 audit: split verification — re-derive source hashes, coverage, seed disjointness, and the
table-derivable gates (G1-G6 + the G7 row-count) from the saved table WITHOUT simulating.

Distinct from replay_ac108.py (sampled exact reruns, including the determinism re-run that closes G7).
This file re-reads ac108_results_v1/ and re-computes every non-determinism claim from the frozen table
+ hashes + the frozen-copy reproduction dict. It does NOT call ac108.run().
"""
import hashlib
import json
import sys
from pathlib import Path
import ac108

ROOT = 'ac108_results_v1'
CONDITIONS = ac108.CONDITIONS

TABLE_GATES = ('G1_maintenance_to_accuracy', 'G2_maintenance_to_use',
               'G3_content_to_adaptation_move', 'G4_content_causal_cut', 'G5_clean_control',
               'G6_frozen_copy_reproduction')


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


def check_coverage(rows, seeds, errors):
    expected = len(seeds) * len(ac108.ARMS) * len(CONDITIONS) * 2
    if len(rows) != expected:
        errors.append(f'row count {len(rows)} != {expected}')
    tuples = {(r['seed'], r['history'], r['arm'], r['condition']) for r in rows}
    if len(tuples) != expected:
        errors.append(f'duplicate/missing (seed,history,arm,condition): {len(tuples)} != {expected}')


def check_seed_disjointness(rows, seeds, errors):
    used_prior = (set(range(8)) | set(range(4412, 4452)) | {4466, 4481, 4504, 4510}
                  | set(range(4600, 4872)) | set(range(4880, 4951))
                  | set(range(5100, 5509)) | set(range(5600, 5608)) | set(range(5700, 5708))
                  | set(range(5800, 5808)) | set(range(5900, 5908)) | set(range(6000, 6008)))
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

    # re-derive the table-derivable gates (determinism passed as True so no simulation runs);
    # the determinism half of G7 is verified by replay_ac108.py.
    repro = results.get('frozen_copy_reproduction')
    gates = ac108.gates_ac108(rows, seeds, repro, determinism=True)
    recorded = results['gates']
    for k in TABLE_GATES:
        if recorded.get(k) != gates[k]:
            errors.append(f'gate {k}: re-derived {gates[k]} != recorded {recorded.get(k)}')
    # row-count half of G7, re-derived here; determinism is the replay's job
    expected = len(seeds) * len(ac108.ARMS) * len(CONDITIONS) * 2
    if len(rows) != expected:
        errors.append(f'G7 row count {len(rows)} != {expected}')

    print(f'rows={len(rows)} seeds={len(seeds)} arms={len(ac108.ARMS)} conditions={len(CONDITIONS)}')
    print('gates (re-derived, no simulation):')
    print(json.dumps({k: gates[k] for k in TABLE_GATES}, indent=2))
    print('reported survival:', json.dumps(gates['_survival_counts']))
    print('reported deaths:', json.dumps(gates['_deaths']))
    if errors:
        print('\nFAILURES:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('\nAC108 audit passed: source hashes valid, gates re-derived without simulating, '
          'coverage + seed-disjointness invariants hold.')


if __name__ == '__main__':
    main()
