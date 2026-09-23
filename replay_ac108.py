"""AC108 replay: sampled exact reruns — re-run a sample of frozen rows and compare state_hash,
plus the determinism re-run that closes G7.

Distinct from audit_ac108.py (re-derives gates/hashes from the saved table WITHOUT simulating).
This file re-simulates a sample and checks byte-identity.
"""
import json
import sys
from pathlib import Path
import ac108

ROOT = 'ac108_results_v1'


def sample_rows(rows):
    # first row of each arm x condition (covers all 18 cells)
    cells = {}
    for r in rows:
        cells.setdefault((r['arm'], r['condition']), r)
    return list(cells.values())


def load(root=ROOT):
    root = Path(root)
    rows = [json.loads(l) for l in (root / 'rows.jsonl').read_text().splitlines()]
    results = json.loads((root / 'results.json').read_text())
    snapshot = json.loads((root / 'pre_run_snapshot.json').read_text())
    return root, rows, results, snapshot


def main():
    root, rows, results, snapshot = load()
    sample = sample_rows(rows)
    errors = []
    mismatches = 0
    for r in sample:
        got = ac108.run(r['seed'], r['history'], r['arm'], r['condition'])
        if got['state_hash'] != r['state_hash']:
            mismatches += 1
            errors.append(f"seed {r['seed']}/{r['history']} {r['arm']}/{r['condition']}: "
                          f"replay state_hash mismatch")
    print(f'replayed {len(sample)} sampled rows ({len(sample)} cells), {mismatches} mismatches')

    # G7 determinism: re-run the first row.
    first = rows[0]
    rerun = ac108.run(first['seed'], first['history'], first['arm'], first['condition'])
    determinism = rerun['state_hash'] == first['state_hash']
    expected = len(results['seeds']) * len(ac108.ARMS) * len(ac108.CONDITIONS) * 2
    g7 = (len(rows) == expected) and determinism
    print(f'G7 determinism re-run (first row {first["arm"]}/{first["condition"]} '
          f'seed {first["seed"]}/{first["history"]}): determinism={determinism}, rowcount_ok={len(rows) == expected}')
    if results['gates'].get('G7_completeness_determinism') != g7:
        errors.append('G7 recorded value inconsistent with re-derived determinism + row count')

    if errors:
        print('\nFAILURES:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('\nAC108 replay passed: sampled rows reproduce state_hash exactly.')


if __name__ == '__main__':
    main()
