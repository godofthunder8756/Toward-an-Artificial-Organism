"""replay_ac33.py -- re-run declared final seeds and compare to the frozen rows exactly."""
import json
import sys
from pathlib import Path
import ac33_reacquire as ac33

ROOT=Path('ac33_results_v1')


def main(seeds=(3400,3401)):
    stored={json.loads(l)['seed']:json.loads(l)
            for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()}
    exact=0
    for seed in seeds:
        fresh=ac33.individual(seed)
        same=json.dumps(fresh,sort_keys=True)==json.dumps(stored[seed],sort_keys=True)
        exact+=same
        if not same:
            print(f'mismatch at seed {seed}')
            for arm in ac33.ARMS:
                if fresh[arm]!=stored[seed][arm]:
                    print(f'  {arm}: fresh {fresh[arm]["post"]:.4f} stored '
                          f'{stored[seed][arm]["post"]:.4f}')
    print(f'replay: {exact}/{len(seeds)} individuals reproduced exactly')
    return 0 if exact==len(seeds) else 1


if __name__=='__main__':
    sys.exit(main())
