"""AC50 replay: reproduce two individuals in a fresh process and compare against the frozen rows."""
import json
import sys
from pathlib import Path
import ac50_heterogeneous as a50

ROOT = Path('ac50_results_v1')
REPLAY = [4800, 4803]


def main():
    rows = {r['seed']: r
            for r in (json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines() if l.strip())}
    bad = []
    for seed in REPLAY:
        if seed not in rows:
            bad.append((seed, 'not in the frozen rows'))
            continue
        frozen = rows[seed]
        recomputed = a50.individual(seed, a50.DECLARED_OPTIMA)
        for arm in a50.ARMS:
            ok = (recomputed[arm]['post'] == frozen[arm]['post']
                  and recomputed[arm]['held'] == frozen[arm]['held']
                  and recomputed[arm]['dead'] == frozen[arm]['dead'])
            print(f'  seed {seed} {arm:12s}: post {recomputed[arm]["post"]:>9.2f} '
                  f'(frozen {frozen[arm]["post"]:>9.2f})  {"ok" if ok else "MISMATCH"}')
            if not ok:
                bad.append((seed, arm, 'values differ'))
    print(f'\nREPLAY {"PASS" if not bad else "FAIL"} ({len(REPLAY)} individuals x '
          f'{len(a50.ARMS)} arms, {len(bad)} problem(s))')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
