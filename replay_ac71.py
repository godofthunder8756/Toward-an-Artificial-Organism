"""AC71 replay: sampled exact reruns against the frozen table."""
import json
import sys
from pathlib import Path

import ac71

ROOT = Path(__file__).parent / 'ac71_results_v1'
SAMPLE = [(2800, 0, 'closed'), (2800, 0, 'no_repair'), (2801, 1, 'closed'),
          (2802, 0, 'no_repair'), (2803, 1, 'closed')]


def main():
    frozen = {}
    for r in json.loads((ROOT / 'results.json').read_text())['rows']:
        frozen[(r['seed'], r['history'], r['arm'])] = r

    ok = 0
    for seed, history, arm in SAMPLE:
        row = ac71.run(seed, history, arm)
        ref = frozen[(seed, history, arm)]
        fields = ['state_hash', 'completed', 'first_dead', 'energy', 'W_live', 'C_live',
                  'B_live', 'occupied', 'register', 'demand']
        diffs = [f for f in fields if row.get(f) != ref.get(f)]
        if diffs:
            print(f'MISMATCH seed={seed} hist={history} arm={arm}: {diffs}')
            sys.exit(1)
        ok += 1
    print(f'replay: {ok}/{len(SAMPLE)} exact (state_hash and endpoint fields)')


if __name__ == '__main__':
    main()
