"""AC71 audit: recompute the five gates from the saved table, without simulating."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent / 'ac71_results_v1'


def main():
    rows = json.loads((ROOT / 'results.json').read_text())['rows']
    assert len(rows) == 16, f'expected 16 rows, got {len(rows)}'

    def arm(a):
        return [r for r in rows if r['arm'] == a]

    closed = arm('closed')
    no_repair = arm('no_repair')
    gates = {
        'G1': all(r['first_dead'] is None for r in closed),
        'G2': all(r['occupied'] > 0 for r in closed),
        'G3': all(r['W_live'] >= 1 and r['C_live'] >= 1 for r in closed),
        'G4': all(r['register'] == [False, False, False, False] for r in closed),
        'G5': all(r['first_dead'] is not None for r in no_repair),
    }
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in gates.items()})
    print('closed survive:', sum(r['first_dead'] is None for r in closed), '/8;',
          'routes held:', sum(r['occupied'] > 0 for r in closed), '/8;',
          'no_repair die:', sum(r['first_dead'] is not None for r in no_repair), '/8')

    for r in rows:
        assert isinstance(r['state_hash'], str)
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    print('snapshot hashes:', len(snap), 'files')

    if gates != {k: True for k in gates}:
        print('GATE FAILURE:', gates)
        sys.exit(1)
    print('audit passed: all five gates pass')


if __name__ == '__main__':
    main()
