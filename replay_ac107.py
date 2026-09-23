"""AC107 replay: sampled exact reruns — re-run a sample of frozen rows and compare state_hash,
plus the determinism re-run (G6).

Distinct from audit_ac107.py (re-derives gates/hashes from the saved table WITHOUT simulating).
This file re-simulates a sample and checks byte-identity.
"""
import hashlib
import json
import sys
from pathlib import Path
import ac107

ROOT = 'ac107_results_v1'
# sample: first row of each arm x condition (covers all 15 cells) + the first row overall for G6.
def sample_rows(rows, seeds):
    cells = {}
    for r in rows:
        key = (r['arm'], r['condition'])
        cells.setdefault(key, r)
    return list(cells.values())


def load(root=ROOT):
    root = Path(root)
    rows = [json.loads(l) for l in (root / 'rows.jsonl').read_text().splitlines()]
    results = json.loads((root / 'results.json').read_text())
    snapshot = json.loads((root / 'pre_run_snapshot.json').read_text())
    return root, rows, results, snapshot


def main():
    root, rows, results, snapshot = load()
    sample = sample_rows(rows, results['seeds'])
    errors = []
    mismatches = 0
    for r in sample:
        got = ac107.run(r['seed'], r['history'], r['arm'], r['condition'])
        if got['state_hash'] != r['state_hash']:
            mismatches += 1
            errors.append(f"seed {r['seed']}/{r['history']} {r['arm']}/{r['condition']}: "
                          f"replay state_hash mismatch")
    print(f'replayed {len(sample)} sampled rows ({len(sample)} cells), {mismatches} mismatches')

    # G6 determinism: re-run the first row.
    first = rows[0]
    rerun = ac107.run(first['seed'], first['history'], first['arm'], first['condition'])
    determinism = rerun['state_hash'] == first['state_hash']
    print(f'G6 determinism re-run (first row {first["arm"]}/{first["condition"]} '
          f'seed {first["seed"]}/{first["history"]}): {determinism}')
    if not determinism:
        errors.append('G6 determinism re-run failed')
    if results['gates'].get('G6_completeness_determinism') != (
            len(rows) == len(results['seeds']) * len(ac107.ARMS) * 3 * 2 and determinism):
        errors.append('G6 recorded value inconsistent with re-derived determinism')

    if errors:
        print('\nFAILURES:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('\nAC107 replay passed: sampled rows reproduce state_hash exactly.')


if __name__ == '__main__':
    main()
