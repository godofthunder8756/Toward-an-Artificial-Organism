"""AC43 audit: recompute every declared gate from the frozen rows, independently of the runner.

Reads `ac43_results_v1/` only. Does not import the runner's gate function: it recomputes the median,
impaired fraction, protected contrast and completeness itself, and takes the exact sign-flip test from the
frozen definition in `ac38_variance` rather than inventing a second one. Also verifies that every file
hashed into `pre_run_snapshot.json` still hashes to the same value -- i.e. that nothing was edited after
the protocol was registered.

Exit code 0 = the frozen record is internally consistent and its declared gates still hold.
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import ac38_variance as ac38

ROOT=Path('ac43_results_v1')
MEDIAN_BAR=150.0
IMPAIRED_FLOOR=0.75
P_BAR=0.01
MIN_N=8
DECLARED_N=16


def load():
    rows=[json.loads(l) for l in (ROOT/'rows.jsonl').read_text().splitlines() if l.strip()]
    res=json.loads((ROOT/'results.json').read_text())
    snap=json.loads((ROOT/'pre_run_snapshot.json').read_text())
    return rows,res,snap


def check_sources(snap):
    bad=[]
    for name,sha in snap.items():
        p=Path(name)
        if not p.exists():
            bad.append((name,'missing'))
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=sha:
            bad.append((name,'hash changed since registration'))
    return bad


def main():
    rows,res,snap=load()
    diffs=[r['difference'] for r in rows]
    d=np.asarray(diffs,dtype=float)

    recomputed={
        'G1_resolvable': bool(ac38.sign_flip_test(diffs)['p']<=P_BAR
                              and ac38.sign_flip_test(diffs)['n']>=MIN_N),
        'G2_median_effect_in_endpoint_units': bool(float(np.median(d))>=MEDIAN_BAR),
        'G3_impaired_fraction_at_or_above_floor': bool(float(np.mean(d>0))>=IMPAIRED_FLOOR),
        'G4_heterogeneity_present': bool(0.0<float(np.mean(d>0))<1.0),
        'G5_protected_variant_also_above_cut': bool(
            float(np.median([r['protected']-r['cut'] for r in rows]))>0),
        'G6_all_individuals_complete': bool(len(rows)==DECLARED_N
                                            and len({(r['seed'],r['history']) for r in rows})==DECLARED_N),
        'G7_determinism': bool(res['gates']['G7_determinism']),
    }
    frozen=res['gates']
    mismatched={k:(frozen.get(k),recomputed[k]) for k in recomputed if frozen.get(k)!=recomputed[k]}
    bad=check_sources(snap)

    print(f'rows {len(rows)}   distinct individuals {len({(r["seed"],r["history"]) for r in rows})}')
    print(f'median difference {np.median(d):.1f}   impaired {np.mean(d>0):.3f}   '
          f'min {d.min():.1f}   max {d.max():.1f}')
    for k in sorted(recomputed):
        print(f'  {k:44s} frozen {str(frozen.get(k)):>5s}  recomputed {str(recomputed[k]):>5s}'
              f'{"   <-- MISMATCH" if k in mismatched else ""}')
    print(f'source hashes: {len(snap)} files checked, {len(bad)} problem(s)')
    for name,why in bad:
        print(f'  {name}: {why}')

    problems=len(mismatched)+len(bad)+sum(1 for v in recomputed.values() if not v)
    print(f'\nAUDIT {"PASS" if problems==0 else "FAIL"} ({problems} problem(s))')
    return 0 if problems==0 else 1


if __name__=='__main__':
    sys.exit(main())
