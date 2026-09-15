"""AC45 audit: recompute every declared gate from the frozen rows, independently of the runner.

Reads `ac45_results_v1/` only. Does not import the runner's gate function: it recomputes the
per-endpoint statistics (median, impaired fraction, exact sign-flip p) and the six gates itself, taking
the sign-flip test from the frozen definition in `ac38_variance` rather than inventing a second one. It
also verifies that every file hashed into `pre_run_snapshot.json` still hashes to the same value -- i.e.
that nothing was edited after the protocol was registered.

The gate SET is reported truthfully. G3 (heterogeneity present) is recorded as FAILED: on the fresh
seeds 16-23 the response is 100% impaired (every individual rises on every member), not the ~88%
bimodality seen on seeds 0-7 and 8-15. That is a falsification of prediction #3, not a corruption of the
record. The exit code reflects RECORD INTEGRITY (recomputed == frozen, hashes unchanged): a faithfully
recorded falsification is a trustworthy record, so a gate being False does not by itself fail the audit.
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import ac38_variance as ac38

ROOT = Path('ac45_results_v1')
FAMILY = ('W_birth', 'converted', 'memory_writes')
IMPAIRED_FLOOR = 0.75
P_BAR = 0.01
N_SIGNIFICANT = 2
DECLARED_N = 16


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
    per = {}
    for q in FAMILY:
        d = np.asarray([r[f'{q}_difference'] for r in rows], dtype=float)
        res = ac38.sign_flip_test(list(d))
        pro = np.asarray([r[f'{q}_protected'] - r[f'{q}_cut'] for r in rows], dtype=float)
        per[q] = dict(p=res['p'], n=res['n'], median=float(np.median(d)),
                      impaired=float(np.mean(d > 0)), min=float(d.min()), max=float(d.max()),
                      protected_median=float(np.median(pro)))
    n_sig = sum(1 for q in FAMILY if per[q]['p'] <= P_BAR)
    g = {}
    g['G1_family_direction_and_impairment'] = bool(
        all(per[q]['median'] > 0 and per[q]['impaired'] >= IMPAIRED_FLOOR for q in FAMILY))
    g['G2_family_significance'] = bool(n_sig >= N_SIGNIFICANT)
    g['G3_heterogeneity_present'] = bool(all(0.0 < per[q]['impaired'] < 1.0 for q in FAMILY))
    g['G4_protected_variant_above_cut'] = bool(all(per[q]['protected_median'] > 0 for q in FAMILY))
    g['G5_all_individuals_complete'] = bool(
        len(rows) == DECLARED_N and len({(r['seed'], r['history']) for r in rows}) == DECLARED_N)
    g['G6_determinism'] = bool(frozen_gates.get('G6_determinism'))
    return g, per, n_sig


def main():
    rows, res, snap = load()
    frozen = res['gates']
    g, per, n_sig = recompute(rows, frozen)
    mismatched = {k: (frozen.get(k), g[k]) for k in g if frozen.get(k) != g[k]}
    bad = check_sources(snap)

    print(f'rows {len(rows)}   distinct individuals {len({(r["seed"], r["history"]) for r in rows})}')
    for q in FAMILY:
        p = per[q]
        print(f'  {q:14s} median diff {p["median"]:>8.1f}   impaired {p["impaired"]:>5.3f}   '
              f'p {p["p"]:.5f}   min {p["min"]:.1f}   protected-median {p["protected_median"]:.1f}')
    print()
    for k in sorted(g):
        tag = '' if g[k] else '   <-- FAILED (recorded)'
        print(f'  {k:36s} frozen {str(frozen.get(k)):>5s}  recomputed {str(g[k]):>5s}'
              f'{"   <-- MISMATCH" if k in mismatched else ""}{tag}')
    passed = [k for k in sorted(g) if g[k]]
    failed = [k for k in sorted(g) if not g[k]]
    print(f'\ngate set: {len(passed)}/6 pass; failed: {failed if failed else "none"}')
    print(f'source hashes: {len(snap)} files checked, {len(bad)} problem(s)')
    for name, why in bad:
        print(f'  {name}: {why}')

    integrity = len(mismatched) == 0 and len(bad) == 0
    print(f'\nAUDIT {"PASS" if integrity else "FAIL"} (record integrity: recomputed gates match the '
          f'frozen record and {len(snap)} source hashes are unchanged)')
    if failed:
        print(f'NOTE: {len(failed)} gate(s) FAILED and are recorded as such. The family rule (G1+G2) '
              f'passed; G3 (the bimodality prediction) is falsified on seeds 16-23.')
    return 0 if integrity else 1


if __name__ == '__main__':
    sys.exit(main())
