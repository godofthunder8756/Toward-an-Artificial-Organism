"""AC45 replay: reproduce two individuals in a fresh process and compare against the frozen rows.

Cross-process reproducibility is the point: the frozen result was produced by a different process than
this one. Any hidden state (module-level caches, dict ordering, thread count) that changed a result
would show up here as a mismatch. All three family endpoints are compared, for capable, cut and
protected.

Exit code 0 = both individuals reproduce exactly.
"""
import json
import sys
from pathlib import Path
import ac45_family as ac45

ROOT = Path('ac45_results_v1')
REPLAY = [(16, 0), (19, 0)]          # two of the sixteen declared individuals, fixed in advance


def main():
    rows = {(r['seed'], r['history']): r
            for r in (json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines() if l.strip())}
    bad = []
    for key in REPLAY:
        s, h = key
        if key not in rows:
            bad.append((key, 'not in the frozen rows'))
            continue
        frozen = rows[key]
        for q in ac45.FAMILY:
            cap = ac45.quantity(ac45.CAPABLE, s, h, q)
            cut = ac45.quantity(ac45.CUT, s, h, q)
            pro = ac45.quantity(ac45.PROTECTED, s, h, q)
            ok = (cap == frozen[f'{q}_capable'] and cut == frozen[f'{q}_cut']
                  and pro == frozen[f'{q}_protected'])
            print(f'  seed {s} history {h} {q:14s}: capable {cap} (frozen {frozen[f"{q}_capable"]})  '
                  f'cut {cut} (frozen {frozen[f"{q}_cut"]})  protected {pro} '
                  f'(frozen {frozen[f"{q}_protected"]})  {"ok" if ok else "MISMATCH"}')
            if not ok:
                bad.append((key, q, 'values differ'))
    print(f'\nREPLAY {"PASS" if not bad else "FAIL"} ({len(REPLAY)} individuals x '
          f'{len(ac45.FAMILY)} endpoints, {len(bad)} problem(s))')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
