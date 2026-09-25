"""replay_ac116.py — sampled exact reruns of the AC116 frozen confirmation.

Re-runs a sample of the frozen rows from scratch via ac116.run and checks the terminal state_hash,
income, income_post, relinquishments, and routes are byte-identical to the frozen table. This is the
replay half of the split verification (audit_ac116.py is the other half).

Verification-tool: NOT in the frozen source hash set (AC16/AC17's rule).
"""

import json
import sys
from pathlib import Path

import numpy as np

import ac116

ROOT = Path(__file__).parent
ARMS = ('counter', 'tuned', 'estimate', 'no_write', 'scramble')
CONDITIONS = ('no_cause', 'move', 'cut')
FIELDS = ('state_hash', 'income', 'income_post', 'relinquishments', 'routes', 'completed',
          'n', 'holding')


def load_rows(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def replay(results_dir, seeds, q=0.9, max_samples=12, rng_seed=0):
    d = ROOT / results_dir
    rows = load_rows(d / 'rows.jsonl')
    rng = np.random.default_rng(rng_seed)
    sample = []
    for s in seeds[:2]:
        for h in (0, 1):
            for c in CONDITIONS:
                for a in ARMS:
                    sample += [r for r in rows if r['seed'] == s and r['history'] == h
                               and r['condition'] == c and r['arm'] == a]
    if max_samples and len(sample) > max_samples:
        idx = rng.choice(len(sample), max_samples, replace=False)
        sample = [sample[i] for i in idx]

    mismatches = []
    n = 0
    for r in sample:
        kw = dict(q=r['q'])
        if r['arm'] in ('counter', 'no_write', 'scramble'):
            kw['n_thr'] = r['n_thr']
        if r['arm'] == 'tuned':
            kw['p'] = r['p']
        rr = ac116.run(r['seed'], r['history'], r['arm'], r['condition'], **kw)
        n += 1
        for f in FIELDS:
            a = rr.get(f)
            b = r.get(f)
            if f == 'routes':
                a, b = list(a), list(b)
            if a != b:
                mismatches.append((r['seed'], r['history'], r['arm'], r['condition'], f, a, b))
    ok = not mismatches
    print('replay', results_dir, '->', 'PASS' if ok else 'FAIL', f'({n} rows)')
    for m in mismatches[:50]:
        print('  MISMATCH:', m)
    return dict(ok=ok, n_replayed=n, mismatches=mismatches)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('results_dir', default='ac116_results_v1')
    ap.add_argument('--seeds', default='6600-6607')
    ap.add_argument('--q', type=float, default=0.9)
    ap.add_argument('--max-samples', type=int, default=12)
    args = ap.parse_args()
    lo, hi = (int(x) for x in args.seeds.split('-'))
    r = replay(args.results_dir, list(range(lo, hi + 1)), q=args.q,
               max_samples=args.max_samples)
    sys.exit(0 if r['ok'] else 1)
