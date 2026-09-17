"""AC68 replay: sampled exact reruns against the frozen table."""
import json
import sys
from pathlib import Path

import ac68

ROOT = Path(__file__).parent / 'ac68_results_v1'
SAMPLE = [(2700, 0), (2701, 1), (2702, 0), (2703, 1)]


def main():
    frozen = {}
    for r in json.loads((ROOT / 'results.json').read_text())['rows']:
        frozen[(r['seed'], r['history'])] = r

    ok = 0
    for seed, history in SAMPLE:
        row = ac68.run(seed, history)
        ref = frozen[(seed, history)]
        fields = ['state_hash', 'completed', 'first_dead', 'first_route_loss',
                  'energy', 'W_live', 'C_live', 'B_live', 'occupied', 'register']
        diffs = [f for f in fields if row.get(f) != ref.get(f)]
        if diffs:
            print(f'MISMATCH seed={seed} hist={history}: {diffs}')
            sys.exit(1)
        ok += 1
    print(f'replay: {ok}/{len(SAMPLE)} exact (state_hash and endpoint fields)')


if __name__ == '__main__':
    main()
