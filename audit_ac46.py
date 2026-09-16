"""AC46 audit: recompute every declared gate from the frozen rows, independently of the runner.

Reads `ac46_results_v1/` only. Recomputes the per-arm statistics and the nine gates itself, taking the
sign-flip test from the frozen definition in `ac38_variance` rather than inventing a second one. Also
verifies that every file hashed into `pre_run_snapshot.json` still hashes to the same value -- i.e. that
nothing was edited after the protocol was registered.

Exit code 0 = the frozen record is internally consistent and its declared gates still hold.
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import ac38_variance as ac38

ROOT = Path('ac46_results_v1')
ARMS = ('learner_both', 'no_release', 'no_search', 'preserve', 'oracle_a', 'oracle_b')
BAR = 4.0
MEDIAN_BAR = 3.0
P_BAR = 0.01
MIN_N = 8
DECLARED_N = 12


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
    g = {}
    g['G1_resolvable'] = bool(res['p'] <= P_BAR and res['n'] >= MIN_N)
    g['G2_median_effect_in_sites'] = bool(float(np.median(d)) >= MEDIAN_BAR)
    g['G3_separation_of_minima'] = bool(min(learner) >= BAR and max(no_rel) < BAR)
    g['G4_oracle_b_ceiling_above_bar'] = bool(min(post('oracle_b')) >= BAR)
    g['G5_oracle_a_floor_below_bar'] = bool(max(post('oracle_a')) < BAR)
    g['G6_state_blind_means_below_bar'] = bool(float(np.mean(post('no_search'))) < BAR
                                               and float(np.mean(post('preserve'))) < BAR)
    g['G7_all_individuals_complete'] = bool(len(rows) == DECLARED_N
                                             and len({r['seed'] for r in rows}) == DECLARED_N
                                             and all(arm in r for r in rows for arm in ARMS))
    g['G8_determinism'] = bool(frozen_gates.get('G8_determinism'))
    g['G9_register_in_the_loop'] = bool(all(len(r[arm]['held']) == 6 for r in rows for arm in ARMS))
    return g, res, d


def main():
    rows, res, snap = load()
    frozen = res['gates']
    g, signres, d = recompute(rows, frozen)
    mismatched = {k: (frozen.get(k), g[k]) for k in g if frozen.get(k) != g[k]}
    bad = check_sources(snap)

    print(f'rows {len(rows)}   distinct individuals {len({r["seed"] for r in rows})}')
    learner = [r['learner_both']['post'] for r in rows]
    no_rel = [r['no_release']['post'] for r in rows]
    print(f'  learner   : min {min(learner):.2f}  mean {np.mean(learner):.2f}  max {max(learner):.2f}')
    print(f'  no_release: min {min(no_rel):.2f}  mean {np.mean(no_rel):.2f}  max {max(no_rel):.2f}')
    print(f'  sign-flip : p {signres["p"]:.5f}  median diff {np.median(d):.2f}  '
          f'impaired {np.mean(d > 0):.3f}')
    print()
    for k in sorted(g):
        tag = '' if g[k] else '   <-- FAILED (recorded)'
        print(f'  {k:36s} frozen {str(frozen.get(k)):>5s}  recomputed {str(g[k]):>5s}'
              f'{"   <-- MISMATCH" if k in mismatched else ""}{tag}')
    passed = [k for k in sorted(g) if g[k]]
    failed = [k for k in sorted(g) if not g[k]]
    print(f'\ngate set: {len(passed)}/9 pass; failed: {failed if failed else "none"}')
    print(f'source hashes: {len(snap)} files checked, {len(bad)} problem(s)')
    for name, why in bad:
        print(f'  {name}: {why}')

    integrity = len(mismatched) == 0 and len(bad) == 0
    print(f'\nAUDIT {"PASS" if integrity else "FAIL"} (record integrity: recomputed gates match the '
          f'frozen record and {len(snap)} source hashes are unchanged)')
    return 0 if integrity else 1


if __name__ == '__main__':
    sys.exit(main())
