"""AC43: repair capability keeps the metabolic endpoint higher -- a frozen study.

The claim
---------
An organism whose register occupancy is maintained by the repair action produces more W births over a run
than one whose occupancy is not, **with corruption absent** so AC14's integrity channel is off by
construction (`reg_rate = 0`). Endpoint: `ledger.W_birth` -- chosen from AC42's survey of 15 quantities as
usable (variance, headroom, resolution) and metabolic.

Why the gate is an aggregate and not a separation of minima
-----------------------------------------------------------
AC42 measured that the cut arm's response is **bimodal**: 88% of individuals impaired, 12% not. A
separation-of-minima gate would therefore fail by construction, and declaring one would be a design error
of the AC17 kind ("better in every individual" was unsatisfiable). The claim's own shape is an *aggregate*
difference with a stated heterogeneity, so the gate is stated that way: resolvability (exact sign-flip
test, power n >= 8), an effect size in the endpoint's OWN units, and an impaired fraction with a floor.

Declared from AC42's engineering (16 individuals, corruption absent, seeds 0-7 x histories 0,1):
    live W_birth   mean 369.0  sd 4.5
    cut  W_birth   mean 199.6
    median per-individual difference 208      p 0.0001      impaired 88%
The bar below sits under that median with margin; the impaired floor sits under 88%.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ac19
import ac38_variance as ac38

ENDPOINT='W_birth'
CAPABLE='two_way'
CUT='two_way_no_repair'
PROTECTED='two_way_protected'
REG_RATE=0.0                      # corruption absent: AC14's integrity channel off by construction
FINAL_SEEDS=tuple(range(8,16))    # fresh: engineering used 0-7
HISTORIES=(0,1)
MEDIAN_BAR=150.0                  # births; AC42 measured 208
IMPAIRED_FLOOR=0.75               # AC42 measured 0.88
P_BAR=0.01
MIN_N=8
SOURCES=['ac43_capability.py','ac19.py','ac38_variance.py','AC43_PROTOCOL_v1.md']


def births(arm,seed,history):
    return float(ac19.run(seed,history,arm,reg_rate=REG_RATE)['ledger'][ENDPOINT])


def individuals(seeds=FINAL_SEEDS,histories=HISTORIES):
    return [(s,h) for s in seeds for h in histories]


def run_study(seeds=FINAL_SEEDS,histories=HISTORIES):
    rows=[]
    for s,h in individuals(seeds,histories):
        cap=births(CAPABLE,s,h); cut=births(CUT,s,h); pro=births(PROTECTED,s,h)
        rows.append(dict(seed=s,history=h,capable=cap,cut=cut,protected=pro,difference=cap-cut))
    return rows


def gates(rows):
    diffs=[r['difference'] for r in rows]
    res=ac38.sign_flip_test(diffs)
    d=np.asarray(diffs,dtype=float)
    impaired=float(np.mean(d>0))
    return {
        'G1_resolvable': bool(res['p']<=P_BAR and res['n']>=MIN_N),
        'G2_median_effect_in_endpoint_units': bool(float(np.median(d))>=MEDIAN_BAR),
        'G3_impaired_fraction_at_or_above_floor': bool(impaired>=IMPAIRED_FLOOR),
        'G4_heterogeneity_present': bool(0.0<impaired<1.0),
        'G5_protected_variant_also_above_cut': bool(
            float(np.median([r['protected']-r['cut'] for r in rows]))>0),
        'G6_all_individuals_complete': len(rows)==len(individuals(SEQ_SEEDS,SEQ_HISTORIES)),
        'G7_determinism': None,
    }, res, impaired


SEQ_SEEDS=FINAL_SEEDS
SEQ_HISTORIES=HISTORIES


def preflight(protocol='AC43_PROTOCOL_v1.md'):
    text=Path(protocol).read_text()
    marker='SOURCES (declared):'
    line=[l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line,f'{protocol} declares no source list'
    declared=[w.strip() for w in line[0].split(marker,1)[1].split() if w.strip()]
    assert set(declared)==set(SOURCES),(
        f'runner hashes {sorted(set(SOURCES))} but the protocol declares {sorted(set(declared))}')
    assert all(Path(s).exists() for s in declared),'a declared source is missing on disk'
    return declared


def main(seeds=FINAL_SEEDS,root='ac43_results_v1'):
    preflight()
    outdir=Path(root); outdir.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES}
    (outdir/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=run_study(seeds)
    with (outdir/'rows.jsonl').open('x') as f:
        for r in rows: f.write(json.dumps(r)+'\n')
    g,res,impaired=gates(rows)
    det=all(births(CAPABLE,s,h)==r['capable'] and births(CUT,s,h)==r['cut']
            for (s,h),r in zip(individuals(seeds),rows))
    g['G7_determinism']=det
    summary=dict(n=len(rows),median_difference=float(np.median([r['difference'] for r in rows])),
                 mean_difference=float(np.mean([r['difference'] for r in rows])),
                 impaired_fraction=impaired,p=res['p'],
                 capable_mean=float(np.mean([r['capable'] for r in rows])),
                 cut_mean=float(np.mean([r['cut'] for r in rows])))
    (outdir/'results.json').write_text(json.dumps(dict(endpoint=ENDPOINT,bar=MEDIAN_BAR,
                                                       impaired_floor=IMPAIRED_FLOOR,seeds=list(seeds),
                                                       gates=g,summary=summary,rows=rows),indent=2))
    print(json.dumps(dict(gates=g,summary=summary),indent=2))
    return g,summary


if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='finals': main()
    else:
        print(__doc__)
        print('Run the declared finals with: .venv/bin/python -B ac43_capability.py finals')
        print('Protocol: AC43_PROTOCOL_v1.md (fresh seeds 8-15 x 2 histories, median bar 150)')
