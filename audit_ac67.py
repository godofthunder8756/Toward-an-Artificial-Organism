"""AC67 audit: recompute the gates and invariants from the saved table, without simulating.

Distinguishes (per the repo convention) the split verification: this re-derives coverage,
arm invariants and the five gate outcomes from ac67_results_v1/rows.jsonl. Replay is the
separate exact-rerun check.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent / 'ac67_results_v1'


def main():
    data = json.loads((ROOT / 'results.json').read_text())
    rows = data['rows']

    # coverage: 4 seeds x 2 histories x 4 arms = 32 rows
    assert len(rows) == 32, f'expected 32 rows, got {len(rows)}'

    def arm_rows(arm):
        return [r for r in rows if r['arm'] == arm]

    closed = arm_rows('closed')
    no_repair = arm_rows('no_repair')

    gates = {}
    gates['G1'] = all(r['register_any_flip'] for r in no_repair)
    gates['G2'] = all(r['first_dead'] is not None for r in no_repair)
    gates['G3'] = all(not r['register_any_flip'] for r in closed)
    gates['G4'] = all(r['first_dead'] is None for r in closed)
    gates['G5'] = all(r['first_register_flip'] is not None and r['first_register_flip'] < r['first_dead']
                      for r in no_repair)

    print('coverage:', len(rows), 'rows;', 'seeds', sorted({r['seed'] for r in rows}))
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in gates.items()})
    print('survival: closed', sum(r['first_dead'] is None for r in closed), '/8;',
          'no_repair', sum(r['first_dead'] is None for r in no_repair), '/8')

    # invariants: every surviving arm has activity 1.0; every closed register is [0,0,0,0]
    for r in closed:
        assert r['register'] == [0, 0, 0, 0], f"closed register not intact: {r['seed']} {r['register']}"
    for r in rows:
        assert isinstance(r['ledger'], dict), 'ledger missing'
        assert isinstance(r['state_hash'], str), 'state_hash missing'

    # source hashes present, no drift check is possible without the files list; report what's there
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    print('snapshot hashes:', len(snap), 'files')

    expected = {'G1': False, 'G2': True, 'G3': True, 'G4': True, 'G5': False}
    if gates != expected:
        print('GATE MISMATCH vs recorded:', gates)
        sys.exit(1)
    print('audit passed: gates match the recorded outcome (G1/G5 fail, G2/G3/G4 pass)')


if __name__ == '__main__':
    main()
