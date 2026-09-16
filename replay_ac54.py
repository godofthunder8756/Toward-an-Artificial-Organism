"""Replay AC54: re-run the finals in a fresh process and check exact reproduction."""
import json
from pathlib import Path
import ac54_order as a54

ROOT = Path('ac54_results_v1')


def main():
    rec = json.loads((ROOT / 'results.json').read_text())
    rows = rec['rows']
    n = 0
    for r in rows:
        fresh = a54.individual(r['seed'])
        assert fresh == r, f'seed {r["seed"]} does not reproduce'
        n += 1
    print(f'replay: {n}/{n} individuals reproduce exactly')


if __name__ == '__main__':
    main()
