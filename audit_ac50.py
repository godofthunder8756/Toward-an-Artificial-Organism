"""AC50 audit: recompute every declared gate from the frozen rows, independently of the runner.

Reads `ac50_results_v1/` only. Recomputes the per-arm statistics and the nine gates itself, taking the
sign-flip test from `ac38_variance`; G4 (horizon-robustness) is recomputed by re-running the learner at
600 and 1500 ticks. Verifies the source hashes. Exit 0 = internally consistent and gates hold.
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import ac38_variance as ac38
import ac50_heterogeneous as a50

ROOT = Path('ac50_results_v1')
ARMS = a50.ARMS
BAR = 500.0
P_BAR = 0.01
MIN_N = 8
DECLARED_N = 12
STEADY_LO, STEADY_HI = 2.4, 2.6


def load():
    rows = [json.loads(l) for l in (ROOT / 'rows.jsonl').read_text().splitlines() if l.strip()]
    res = json.loads((ROOT / 'results.json').read_text())
    snap = json.loads((ROOT / 'pre_run_snapshot.json').read_text())
    return rows, res, snap


def check_sources(snap):
    bad = []
    for name, sha in snap.items():
        p = Path(name)
        if not p.exists():
            bad.append((name, 'missing'))
        elif hashlib.sha256(p.read_bytes()).hexdigest() != sha:
            bad.append((name, 'hash changed since registration'))
    return bad


def recompute(rows, frozen_gates):
    post = lambda arm: [r[arm]['post'] for r in rows]
    learner = post('learner_both')
    no_rel = post('no_release')
    d = np.asarray([a - b for a, b in zip(learner, no_rel)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    l1500 = [a50.rating(r['learner_both']['held'], a50.RATES_B, a50.VALUES_B,
                        ticks=a50.HORIZON_TICKS) for r in rows]
    steady = float(np.mean(l1500)) / float(np.mean(learner))
    dead = sum(r[a]['dead'] for r in rows for a in ARMS)
    g = {}
    g['G1_resolvable'] = bool(res['p'] <= P_BAR and res['n'] >= MIN_N)
    g['G2_median_effect_in_value_units'] = bool(float(np.median(d)) >= BAR)
    g['G3_stability_no_death'] = bool(dead == 0)
    g['G4_horizon_robust_steady_state'] = bool(STEADY_LO <= steady <= STEADY_HI)
    g['G5_oracle_b_ceiling'] = bool(min(post('oracle_b')) >= min(learner))
    g['G6_state_blind_below_learner'] = bool(float(np.mean(post('no_search'))) < float(np.mean(learner))
                                             and float(np.mean(post('preserve'))) < float(np.mean(learner)))
    g['G7_all_individuals_complete'] = bool(len(rows) == DECLARED_N
                                             and len({r['seed'] for r in rows}) == DECLARED_N
                                             and all(arm in r for r in rows for arm in ARMS))
    g['G8_determinism'] = bool(frozen_gates.get('G8_determinism'))
    g['G9_register_in_the_loop'] = bool(all(len(r[arm]['held']) == 6 for r in rows for arm in ARMS))
    return g, res, d, steady, dead


def main():
    rows, res, snap = load()
    frozen = res['gates']
    g, signres, d, steady, dead = recompute(rows, frozen)
    mismatched = {k: (frozen.get(k), g[k]) for k in g if frozen.get(k) != g[k]}
    bad = check_sources(snap)

    learner = [r['learner_both']['post'] for r in rows]
    no_rel = [r['no_release']['post'] for r in rows]
    print(f'rows {len(rows)}   learner {min(learner):.0f}-{max(learner):.0f}  '
          f'no_release {min(no_rel):.0f}-{max(no_rel):.0f}')
    print(f'sign-flip p {signres["p"]:.5f}  median diff {np.median(d):.1f}  '
          f'steady {steady:.2f}  dead {dead}')
    for k in sorted(g):
        tag = '' if g[k] else '   <-- FAILED'
        print(f'  {k:36s} frozen {str(frozen.get(k)):>5s}  recomputed {str(g[k]):>5s}'
              f'{"   <-- MISMATCH" if k in mismatched else ""}{tag}')
    print(f'source hashes: {len(snap)} files checked, {len(bad)} problem(s)')
    for name, why in bad:
        print(f'  {name}: {why}')
    problems = len(mismatched) + len(bad) + sum(1 for v in g.values() if not v)
    print(f'\nAUDIT {"PASS" if problems == 0 else "FAIL"} ({problems} problem(s))')
    return 0 if problems == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
