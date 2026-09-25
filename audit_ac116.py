"""audit_ac116.py — re-derive the AC116 frozen confirmation from the saved table, WITHOUT
simulating. Verifies: source hashes match the pre-run snapshot, row coverage is complete, the
arm/condition invariants hold, the causal-role (G3) and no-cause-identity (G2) checks hold, and the
graded verdict (G4) is recomputed from rows.jsonl (not trusted from results.json).

This is the split-verification audit (AC9's audit_ac9 pattern). replay_ac116.py does the sampled
exact reruns. The audit intentionally does NOT import ac116's runner (no simulation), only stdlib +
numpy for the table arithmetic.
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
ARMS = ('counter', 'tuned', 'estimate', 'no_write', 'scramble')
CONDITIONS = ('no_cause', 'move', 'cut')
CUT_TICK = 8192
N_STAR = 4
P_STAR = 1.0
COUNTER_W = -6


def load_rows(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_drop_tick(r):
    ts = [t for t, _p, _rr in r['drop_ticks']]
    return min(ts) if ts else None


def sign_flip(diffs):
    n = len(diffs)
    diffs = np.array(diffs, dtype=float)
    observed = float(diffs.sum())
    count = 0
    total = 0
    for mask in range(1 << n):
        total += 1
        s = 0.0
        for i in range(n):
            s += diffs[i] if (mask >> i) & 1 else -diffs[i]
        if abs(s) >= abs(observed) - 1e-9:
            count += 1
    return count / total


def audit(results_dir, seeds, q=0.9):
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
    if len(rows) != n_cohort:
        errors.append(f'row count {len(rows)} != expected {n_cohort}')

    # 2. coverage
    for s in seeds:
        for h in (0, 1):
            for c in CONDITIONS:
                for a in ARMS:
                    if not any(r['seed'] == s and r['history'] == h and r['condition'] == c
                               and r['arm'] == a for r in rows):
                        errors.append(f'missing row {s}/{h}/{c}/{a}')

    # 3. arm/condition invariants
    for r in rows:
        if r['condition'] == 'no_cause' and r['relinquishments'] != 0:
            errors.append(f'no_cause relinquish {r["seed"]}/{r["history"]}/{r["arm"]}')
        if r['condition'] == 'move' and r['arm'] in ('counter', 'tuned', 'estimate') \
                and r['relinquishments'] == 0:
            errors.append(f'move no-relinquish {r["seed"]}/{r["history"]}/{r["arm"]}')

    # 4. G2 (no-cause identity within the counter family)
    g2 = {}
    for s in seeds:
        for h in (0, 1):
            hashes = {r['arm']: r['state_hash'] for r in rows
                      if r['seed'] == s and r['history'] == h and r['condition'] == 'no_cause'}
            family = {a: hashes[a] for a in ('counter', 'tuned', 'no_write', 'scramble')}
            distinct = len(set(family.values()))
            g2[f'{s}/{h}'] = distinct == 1
            if distinct != 1:
                errors.append(f'G2 counter-family not identical {s}/{h}')

    # 5. G3 (causal role): counter vs scramble at N*
    c_move = {(r['seed'], r['history']): r for r in rows
              if r['arm'] == 'counter' and r['condition'] == 'move' and r['n_thr'] == N_STAR}
    sc_move = {(r['seed'], r['history']): r for r in rows
               if r['arm'] == 'scramble' and r['condition'] == 'move' and r['n_thr'] == N_STAR}
    c_cut = {(r['seed'], r['history']): r for r in rows
             if r['arm'] == 'counter' and r['condition'] == 'cut' and r['n_thr'] == N_STAR}
    sc_cut = {(r['seed'], r['history']): r for r in rows
              if r['arm'] == 'scramble' and r['condition'] == 'cut' and r['n_thr'] == N_STAR}
    earlier = equal = later = 0
    for k in sorted(c_move):
        a = first_drop_tick(c_move[k])
        b = first_drop_tick(sc_move[k])
        if a is None and b is None:
            equal += 1
        elif a is not None and b is not None:
            if a < b:
                earlier += 1
            elif a == b:
                equal += 1
            else:
                later += 1
        elif a is not None:
            earlier += 1
        else:
            later += 1
    cut_c = sum(1 for r in c_cut.values() if r['relinquishments'] >= 1)
    cut_sc = sum(1 for r in sc_cut.values() if r['relinquishments'] >= 1)
    g3a = (earlier >= 1 and later == 0)
    g3b = (cut_c >= 1 and cut_sc == 0)
    g3 = dict(earlier=earlier, equal=equal, later=later, cut_counter_false=cut_c,
              cut_scramble_false=cut_sc, g3a=g3a, g3b=g3b, pass_=g3a or g3b)
    if not (g3a or g3b):
        errors.append(f'G3 causal-role failed (F3): {g3}')

    # 6. G4 (the scientific question): seed-level paired sign-flip on combined income
    def combined(arm):
        tot = {}
        for r in rows:
            if r['arm'] != arm or r['condition'] not in ('move', 'cut'):
                continue
            if arm == 'counter' and r['n_thr'] != N_STAR:
                continue
            if arm == 'tuned' and r['p'] != P_STAR:
                continue
            tot.setdefault((r['seed'], r['history']), 0)
            tot[(r['seed'], r['history'])] += r['income_post']
        out = {}
        for (s, h), v in tot.items():
            out.setdefault(s, 0)
            out[s] += v
        return out

    c = combined('counter')
    t = combined('tuned')
    common = sorted(set(c) & set(t))
    diffs = np.array([c[s] - t[s] for s in common], dtype=float)
    observed = float(diffs.sum())
    p = sign_flip([c[s] - t[s] for s in common])
    mean_d = float(diffs.mean()) if len(diffs) else None
    verdict = dict(n_star=N_STAR, p_star=P_STAR, n_seeds=len(common), mean_diff=mean_d,
                   observed_sum=observed, sign_flip_p=p,
                   diffs=[int(x) for x in sorted(diffs.tolist())])
    if mean_d is None or p > 0.05:
        verdict['decision'] = 'F1 no-demonstrated-advantage'
    elif mean_d > 0:
        verdict['decision'] = 'SUPPORT'
    else:
        verdict['decision'] = 'F2 no-advantage'

    # 7. Pareto readout (reported)
    pareto = {}
    for arm in ('counter', 'tuned', 'scramble', 'no_write', 'estimate'):
        mv = [first_drop_tick(r) for r in rows if r['arm'] == arm and r['condition'] == 'move'
              and (r['arm'] not in ('counter', 'scramble', 'no_write') or r['n_thr'] == N_STAR)
              and (r['arm'] != 'tuned' or r['p'] == P_STAR)]
        cut = [r['relinquishments'] for r in rows if r['arm'] == arm and r['condition'] == 'cut'
               and (r['arm'] not in ('counter', 'scramble', 'no_write') or r['n_thr'] == N_STAR)
               and (r['arm'] != 'tuned' or r['p'] == P_STAR)]
        lat = [t - CUT_TICK for t in mv if t is not None]
        pareto[arm] = dict(move_lat_mean=(float(np.mean(lat)) if lat else None),
                           move_relinq=sum(1 for r in rows if r['arm'] == arm
                                           and r['condition'] == 'move' and r['relinquishments'] >= 1
                                           and (r['arm'] not in ('counter', 'scramble', 'no_write')
                                                or r['n_thr'] == N_STAR)
                                           and (r['arm'] != 'tuned' or r['p'] == P_STAR)),
                           cut_false_relinq=sum(1 for x in cut if x >= 1))

    ok = not errors
    print('audit', results_dir, '->', 'PASS' if ok else 'FAIL')
    for e in errors[:50]:
        print('  ERROR:', e)
    print('  rows:', len(rows), 'G2 distinct-violations:', sum(1 for v in g2.values() if not v))
    print('  G3:', json.dumps(g3))
    print('  G4 verdict:', json.dumps(verdict))
    print('  Pareto:', json.dumps(pareto, default=str))
    return dict(ok=ok, errors=errors, n_rows=len(rows), g2=g2, g3=g3, verdict=verdict,
                pareto=pareto, snapshot=snap)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('results_dir', default='ac116_results_v1')
    ap.add_argument('--seeds', default='6600-6607')
    ap.add_argument('--q', type=float, default=0.9)
    args = ap.parse_args()
    lo, hi = (int(x) for x in args.seeds.split('-'))
    r = audit(args.results_dir, list(range(lo, hi + 1)), q=args.q)
    sys.exit(0 if r['ok'] else 1)
