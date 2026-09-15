"""replay_ac32.py -- re-run the declared final seeds and compare to the frozen rows exactly.

Determinism across processes is the strongest available check on a frozen run: it shows the result
does not depend on anything unrecorded.
"""
import json
import sys
from pathlib import Path
import ac32_reacquire as ac

ROOT=Path('ac32_results_v1')


def main(seeds=(3300,3301)):
    stored={json.loads(l)['seed']:json.loads(l)
            for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()}
    exact=0
    for seed in seeds:
        fresh=ac.individual(seed,ac.DECLARED_OPTIMA)
        same=json.dumps(fresh,sort_keys=True)==json.dumps(stored[seed],sort_keys=True)
        exact+=same
        if not same:
            print(f'mismatch at seed {seed}')
            for arm in ac.ARMS:
                if fresh[arm]!=stored[seed][arm]:
                    print(f'  {arm}: fresh {fresh[arm]["post"]:.4f} vs stored '
                          f'{stored[seed][arm]["post"]:.4f}')
    print(f'replay: {exact}/{len(seeds)} individuals reproduced exactly')
    return 0 if exact==len(seeds) else 1


if __name__=='__main__':
    sys.exit(main())
