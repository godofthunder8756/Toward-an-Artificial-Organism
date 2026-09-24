"""audit_ac113.py — re-derive the AC113 frozen confirmation from the saved table, WITHOUT
simulating. Verifies: source hashes match the pre-run snapshot, row coverage is complete,
the arm/condition invariants hold, and the graded verdict is recomputed from rows.jsonl
(rather than trusted from results.json).

This is the split-verification audit (AC9's audit_ac9 pattern): it re-checks coverage,
ledgers, arm invariants and source hashes from the saved table only. replay_ac113.py does
the sampled exact reruns. The audit intentionally does NOT import ac113's runner (no
simulation), only stdlib + numpy for the table arithmetic.
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
THETA_GRID = [0.5, 0.55, 0.6, 0.66, 0.7, 0.8, 0.9]
SINGLE_GRID = [(-6, 1), (-6, 2), (-6, 4), (-4, 2), (-4, 4), (-2, 2), (-2, 4), (0, 1), (0, 2)]
ARMS = ('two_counter', 'single_counter', 'immediate', 'scramble')
CONDITIONS = ('no_cause', 'move', 'cut')
CUT_TICK = 8192


def load_rows(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_drop_tick(r):
    ts = [t for t, _p, _rr in r['drop_ticks']]
    return min(ts) if ts else None


def move_latency(r):
    t = first_drop_tick(r)
    return (t - CUT_TICK) if t is not None else None


def audit(results_dir, seeds, q=0.9, eps=0.08, theta_star=None, single_star=None):
    d = ROOT / results_dir
    errors = []
    snap = json.loads((d / 'pre_run_snapshot.json').read_text())

    # 1. source hashes
    for name, h in snap['hashes'].items():
        p = ROOT / name
        if not p.exists():
            errors.append(f'source {name} missing')
            continue
        if sha256(p) != h:
            errors.append(f'source {name} hash drift')

    rows = load_rows(d / 'rows.jsonl')
    n_cohort = len(seeds) * 2 * len(CONDITIONS) * len(ARMS)
    n_sweep = len(seeds) * 2 * (len(THETA_GRID) + len(SINGLE_GRID)) * 2
    n_causal = len(seeds) * 2 * 2      # scramble at theta=0.6, move+cut (V2)
    if len(rows) != n_cohort + n_sweep + n_causal:
        errors.append(f'row count {len(rows)} != expected {n_cohort}+{n_sweep}+{n_causal}')

    cohort = [r for r in rows if 'param' not in r]
    sweep = [r for r in rows if 'param' in r and r['param'] != 'scramble theta=0.60']
    causal = [r for r in rows if r.get('param') == 'scramble theta=0.60']

    # 2. coverage
    for s in seeds:
        for h in (0, 1):
            for c in CONDITIONS:
                for a in ARMS:
                    if not any(r['seed'] == s and r['history'] == h and r['condition'] == c
                               and r['arm'] == a for r in cohort):
                        errors.append(f'missing cohort row {s}/{h}/{c}/{a}')
            for th in THETA_GRID:
                for c in ('move', 'cut'):
                    if not any(r['seed'] == s and r['history'] == h and r['condition'] == c
                               and r['arm'] == 'two_counter' and r.get('theta') == th
                               for r in sweep):
                        errors.append(f'missing sweep row theta={th} {s}/{h}/{c}')
            for (w, n) in SINGLE_GRID:
                for c in ('move', 'cut'):
                    if not any(r['seed'] == s and r['history'] == h and r['condition'] == c
                               and r['arm'] == 'single_counter' and r.get('w') == w
                               and r.get('n_thr') == n for r in sweep):
                        errors.append(f'missing sweep row w={w},N={n} {s}/{h}/{c}')

    # 3. arm/condition invariants
    for r in cohort:
        if r['condition'] == 'no_cause' and r['relinquishments'] != 0:
            errors.append(f'no_cause relinquish {r["seed"]}/{r["history"]}/{r["arm"]}')
        if r['condition'] == 'move' and r['arm'] in ('two_counter', 'single_counter') \
                and r['relinquishments'] == 0:
            errors.append(f'move no-relinquish {r["seed"]}/{r["history"]}/{r["arm"]}')

    # 3b. V2 (causal role): scramble (theta=0.6) vs two_counter (theta=0.6)
    tc6 = {(r['seed'], r['history'], r['condition']): r['relinquishments']
           for r in sweep if r['arm'] == 'two_counter' and r.get('theta') == 0.6}
    sc6 = {(r['seed'], r['history'], r['condition']): r['relinquishments']
           for r in causal}
    v2 = {}
    if tc6 and sc6:
        tc6_move_drop = sum(tc6[(s, h, 'move')] >= 1 for s in seeds for h in (0, 1))
        sc6_move_drop = sum(sc6[(s, h, 'move')] >= 1 for s in seeds for h in (0, 1))
        tc6_cut_relinq = sum(tc6[(s, h, 'cut')] >= 1 for s in seeds for h in (0, 1))
        sc6_cut_relinq = sum(sc6[(s, h, 'cut')] >= 1 for s in seeds for h in (0, 1))
        v2 = dict(two_counter_move_drop=f'{tc6_move_drop}/16',
                  scramble_move_drop=f'{sc6_move_drop}/16',
                  two_counter_cut_relinq=f'{tc6_cut_relinq}/16',
                  scramble_cut_relinq=f'{sc6_cut_relinq}/16')
        v2['v2a_pass'] = (tc6_move_drop == 16 and sc6_move_drop <= 15)
        v2['v2b_pass'] = (tc6_cut_relinq >= 1 and sc6_cut_relinq == 0)
        # protocol V2 semantics: F3 (no-information) iff BOTH (a) AND (b) fail; V2 passes
        # if EITHER demonstration of causal efficacy holds (the content causally matters).
        v2['pass'] = v2['v2a_pass'] or v2['v2b_pass']
        if not v2['pass']:
            errors.append(f'V2 causal-role failed (F3): {v2}')

    # 4. recompute the verdict from rows.jsonl (fixed-parameter comparison)
    verdict = {}
    if theta_star is not None and single_star is not None:
        w_star, n_star = single_star

        def combined(arm):
            tot = {}
            for r in cohort:
                if r['arm'] != arm:
                    continue
                if r['condition'] not in ('move', 'cut'):
                    continue
                ok = (arm == 'two_counter' and r.get('theta') == theta_star) or \
                     (arm == 'single_counter' and r.get('w') == w_star and r.get('n_thr') == n_star)
                if not ok:
                    continue
                k = (r['seed'], r['history'])
                tot.setdefault(k, [0, 0])[0] += r['income_post']
                tot.setdefault(k, [0, 0])[1] += 1
            return {k: v[0] for k, v in tot.items()}

        tc = combined('two_counter')
        sc = combined('single_counter')
        common = sorted(set(tc) & set(sc))
        diffs = np.array([tc[k] - sc[k] for k in common])
        n = len(diffs)
        # exact sign-flip test over all 2^n sign assignments
        observed = diffs.sum()
        count = 0
        total = 0
        for mask in range(1 << n):
            total += 1
            s = 0.0
            for i in range(n):
                s += diffs[i] if (mask >> i) & 1 else -diffs[i]
            if abs(s) >= abs(observed) - 1e-9:
                count += 1
        p = count / total
        mean_d = float(diffs.mean()) if n else None
        verdict = dict(theta_star=theta_star, single_star=list(single_star), n_pairs=n,
                       mean_diff=mean_d, observed_sum=float(observed), sign_flip_p=p,
                       diffs=sorted(diffs.tolist()))
        if mean_d is None or p > 0.05:
            verdict['decision'] = 'F1 equivalence'
        elif mean_d > 0:
            verdict['decision'] = 'SUPPORT'
        else:
            verdict['decision'] = 'F2 no-advantage'

    # 5. the full sweep surface (declared diagnostic)
    surface = {}
    for r in sweep:
        key = (r['arm'], r['param'])
        surface.setdefault(key, []).append(r['income_post'])
    surface = {f'{a} {p}': (sum(v), len(v)) for (a, p), v in surface.items()}

    ok = not errors
    print('audit', results_dir, '->', 'PASS' if ok else 'FAIL')
    for e in errors[:50]:
        print('  ERROR:', e)
    print('  rows:', len(rows), 'cohort:', len(cohort), 'sweep:', len(sweep),
          'causal:', len(causal))
    print('  V2:', json.dumps(v2))
    print('  verdict:', json.dumps(verdict, default=str))
    return dict(ok=ok, errors=errors, n_rows=len(rows), verdict=verdict, v2=v2,
                surface=surface, snapshot=snap)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('results_dir', default='ac113_results_v1')
    ap.add_argument('--seeds', default='6400-6407')
    ap.add_argument('--eps', type=float, default=0.08)
    ap.add_argument('--theta-star', type=float, default=None)
    ap.add_argument('--single-star', default=None, help='w,N')
    args = ap.parse_args()
    lo, hi = (int(x) for x in args.seeds.split('-'))
    seeds = list(range(lo, hi + 1))
    single_star = tuple(int(x) for x in args.single_star.split(',')) if args.single_star else None
    r = audit(args.results_dir, seeds, eps=args.eps, theta_star=args.theta_star,
              single_star=single_star)
    sys.exit(0 if r['ok'] else 1)
