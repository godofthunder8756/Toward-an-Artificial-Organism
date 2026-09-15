"""AC43 replay: reproduce two individuals in a fresh process and compare against the frozen rows.

Cross-process reproducibility is the point: the frozen result was produced by a different process than
this one. Any hidden state (module-level caches, dict ordering, thread count) that changed a result would
show up here as a mismatch.

Exit code 0 = both individuals reproduce exactly.
"""
import json
import sys
from pathlib import Path
import ac43_capability as ac43

ROOT=Path('ac43_results_v1')
REPLAY=[(8,0),(11,0)]          # two of the sixteen declared individuals, fixed in advance


def main():
    rows={(r['seed'],r['history']):r
          for r in (json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip())}
    bad=[]
    for key in REPLAY:
        s,h=key
        if key not in rows:
            bad.append((key,'not in the frozen rows'))
            continue
        frozen=rows[key]
        cap=ac43.births(ac43.CAPABLE,s,h)
        cut=ac43.births(ac43.CUT,s,h)
        pro=ac43.births(ac43.PROTECTED,s,h)
        ok=(cap==frozen['capable'] and cut==frozen['cut'] and pro==frozen['protected'])
        print(f'  seed {s} history {h}: capable {cap} (frozen {frozen["capable"]})  '
              f'cut {cut} (frozen {frozen["cut"]})  protected {pro} (frozen {frozen["protected"]})  '
              f'{"ok" if ok else "MISMATCH"}')
        if not ok:
            bad.append((key,'values differ'))
    print(f'\nREPLAY {"PASS" if not bad else "FAIL"} ({len(REPLAY)} individuals, '
          f'{len(bad)} problem(s))')
    return 0 if not bad else 1


if __name__=='__main__':
    sys.exit(main())
