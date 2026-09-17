"""AC67 replay: sampled exact reruns against the frozen table.

Re-runs a few (seed, history, arm) conditions from scratch and compares the full row
(state_hash included) to the frozen record. This is the exact-rerun half of the split
verification; audit_ac67.py is the table-only half.
"""
import json
import sys
from pathlib import Path

import ac12
import ac67

ROOT = Path(__file__).parent / 'ac67_results_v1'
SAMPLE = [(2600, 0, 'closed'), (2600, 0, 'no_repair'), (2601, 1, 'no_repair'),
          (2602, 0, 'no_repair'), (2603, 1, 'closed')]


def main():
    frozen = {}
    for r in json.loads((ROOT / 'results.json').read_text())['rows']:
        frozen[(r['seed'], r['history'], r['arm'])] = r

    ok = 0
    for seed, history, arm in SAMPLE:
        row = ac67.run(seed, history, arm)
        ref = frozen[(seed, history, arm)]
        # compare the load-bearing fields; state_hash is the real equality test
        fields = ['state_hash', 'activity', 'completed', 'first_dead',
                  'register', 'routes', 'demand', 'program_bits_damaged']
        diffs = [f for f in fields if row.get(f) != ref.get(f)]
        if diffs:
            print(f'MISMATCH seed={seed} hist={history} arm={arm}: {diffs}')
            sys.exit(1)
        ok += 1
    print(f'replay: {ok}/{len(SAMPLE)} exact (state_hash and endpoint fields)')


if __name__ == '__main__':
    main()
