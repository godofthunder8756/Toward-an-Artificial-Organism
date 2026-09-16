"""AC46 replay: reproduce two individuals in a fresh process and compare against the frozen rows.

Cross-process reproducibility is the point: the frozen result was produced by a different process than
this one. Any hidden state (module-level caches, dict ordering, thread count) that changed a result
would show up here as a mismatch. Every arm's post and held order are compared.

Exit code 0 = both individuals reproduce exactly.
"""
import json
import sys
from pathlib import Path
import ac46_selfsufficiency as ac46

ROOT = Path('ac46_results_v1')
REPLAY = [4700, 4703]          # two of the twelve declared individuals, fixed in advance


def main():
    rows = {r['seed']: r
            for r in (json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines() if l.strip())}
    bad = []
    for seed in REPLAY:
        if seed not in rows:
            bad.append((seed, 'not in the frozen rows'))
            continue
        frozen = rows[seed]
        recomputed = ac46.individual(seed, ac46.DECLARED_OPTIMA)
        for arm in ac46.ARMS:
            ok = (recomputed[arm]['post'] == frozen[arm]['post']
                  and recomputed[arm]['held'] == frozen[arm]['held'])
            print(f'  seed {seed} {arm:12s}: post {recomputed[arm]["post"]:>7.2f} '
                  f'(frozen {frozen[arm]["post"]:>7.2f})  {"ok" if ok else "MISMATCH"}')
            if not ok:
                bad.append((seed, arm, 'values differ'))
    print(f'\nREPLAY {"PASS" if not bad else "FAIL"} ({len(REPLAY)} individuals x '
          f'{len(ac46.ARMS)} arms, {len(bad)} problem(s))')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
