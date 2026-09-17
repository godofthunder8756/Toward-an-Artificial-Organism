"""AC68 audit: recompute the gates from the saved table, without simulating."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent / 'ac68_results_v1'


def main():
    data = json.loads((ROOT / 'results.json').read_text())
    rows = data['rows']
    assert len(rows) == 8, f'expected 8 rows, got {len(rows)}'

    gates = {
        'G1': all(r['first_dead'] is None for r in rows),
        'G2': all(r['W_live'] >= 1 and r['C_live'] >= 1 for r in rows),
        'G3': all(r['occupied'] == 0 for r in rows),
    }
    print('gates:', {k: ('PASS' if v else 'FAIL') for k, v in gates.items()})
    print('survive:', sum(r['first_dead'] is None for r in rows), '/8;',
          'route-lapse:', sum(r['occupied'] == 0 for r in rows), '/8')

    for r in rows:
        assert isinstance(r['state_hash'], str)
    # register intact in survivors, degraded in the dying
    intact = sum(r['register'] == [False, False, False, False] for r in rows)
    assert intact == 4, f'expected 4 intact registers, got {intact}'

    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    print('snapshot hashes:', len(snap), 'files')

    expected = {'G1': False, 'G2': False, 'G3': True}
    if gates != expected:
        print('GATE MISMATCH vs recorded:', gates)
        sys.exit(1)
    print('audit passed: gates match the recorded outcome (G1/G2 fail, G3 pass)')


if __name__ == '__main__':
    main()
