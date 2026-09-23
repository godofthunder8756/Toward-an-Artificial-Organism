"""replay_ac110.py — sampled exact reruns of the frozen AC110 rows, comparing state_hash.

This is the SPLIT verification second half (audit_ac110.py re-derives without simulating; this does
sampled exact reruns). Re-running a sampled subset of (seed, history, condition, arm) from scratch
must reproduce the recorded state_hash field-for-field.
"""

import json
from pathlib import Path
import ac110

ROOT = Path('ac110_results_v1')


def main():
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines()]
    by = {(r['seed'], r['history'], r['condition'], r['arm']): r for r in rows}

    # sample: first 2 seeds, both histories, cut + move + no_cause, both arms
    sample = []
    for s in (6200, 6203):
        for h in (0, 1):
            for c in ('no_cause', 'move', 'cut'):
                for a in ('maintained', 'no_repair'):
                    sample.append((s, h, c, a))

    matched = 0
    for (s, h, c, a) in sample:
        r = ac110.run(s, h, a, c, q=0.5, bel_damage=0.0)
        rec = by[(s, h, c, a)]
        ok = r['state_hash'] == rec['state_hash']
        if ok:
            matched += 1
        else:
            print(f'MISMATCH {s}/{h}/{c}/{a}: rerun hash {r["state_hash"]} != '
                  f'recorded {rec["state_hash"]}')
    print(f'replay: {matched}/{len(sample)} sampled rows reproduce state_hash exactly')
    assert matched == len(sample)
    print('replay AC110 passed')


if __name__ == '__main__':
    main()
