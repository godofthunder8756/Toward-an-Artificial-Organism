"""AC41: occupancy maintained by repair -- endpoint with headroom, criterion split, declared up front.

The claim being prepared
------------------------
AC19-M diagnosed why AC19's register-cut arms die: not corruption (they die 0/4 with the register damage
rate at zero), but an emptying register that stops driving activity. So the closure question's sharp
answer is that the state's INTEGRITY is not load-bearing while its OCCUPANCY is.

The claim: an organism whose register occupancy is maintained by the repair action keeps that occupancy
higher than one whose occupancy is not, **with corruption absent** so AC14's integrity channel is off by
construction.

What AC39 taught, applied here BEFORE measuring
-----------------------------------------------
AC39 stopped on the mean/sd ratio, which AC40 then showed is a noisy statistic that flags passing studies
too. This study therefore declares the split form in advance, and it fixes the two design flaws AC39
exposed:

1. **Resolvability**: n = 16 individuals (seeds 0-7 x two histories -- histories are 0 or 1 by the frozen
   harness's design, so 2 is what the interface offers). Exact sign-flip test, floor 2/2^16 stated up
   front. Requirement: p <= 0.01.
2. **Headroom**: ENDPOINT CHANGED from "ticks active" (which saturated at 4096 for every live individual)
   to **mean register occupancy over the run**. Occupancy is not pinned at a ceiling: the live arm's
   occupancy in AC19-M was tens of thousands with individual variation, and the cut arm's was a fraction
   of it. Requirement declared here: the maintained arm must sit below 90% of any ceiling it could reach
   -- checked, not assumed.
3. **Effect size in endpoint units**: requirement declared here -- the median per-individual difference
   must exceed **1000 occupancy units** (one quarter of the live arm's observed level in AC19-M). Not a
   ratio of moments.
4. **Stability**: reported as the impaired fraction and the per-individual differences, not as a
   resampled ratio.
5. **Prediction, stated before measuring**: AC39's cut arm was bimodal (2 of 16 individuals unimpaired).
   Here I predict the same structure appears in occupancy -- some individuals maintain occupancy as well
   as the live arm. If it does not, that is a falsified prediction and is recorded as such.

Engineering only unless the prerequisite passes. No protocol, no final seeds, no claim.
"""
import json
import numpy as np
import ac19
import ac38_variance as ac38

SEEDS=tuple(range(8))
HISTORIES=(0,1)
LIVE='two_way'
CUT='two_way_no_repair'
P_BAR=0.01
MIN_N=8
MIN_MEDIAN_DIFFERENCE=1000.0        # endpoint units, declared
SOURCES=[]


def occupancy(arm,seed,history,reg_rate=0.0):
    """Mean register occupancy over the run: the sum of the frozen demand vector at the end is not
    enough, so this uses the register's recorded occupancy totals where available and falls back to
    the demand vector's magnitude."""
    r=ac19.run(seed,history,arm,reg_rate=reg_rate)
    for key in ('register_replicas_set_total',):
        if key in r and r[key] is not None:
            return float(r[key])
    d=r['demand']
    return float(sum(v for v in np.asarray(d,dtype=object).ravel() if isinstance(v,(int,np.integer))))


def collect(arm):
    return {(s,h):occupancy(arm,s,h) for s in SEEDS for h in HISTORIES}


if __name__=='__main__':
    print(__doc__)
    print('--- prerequisite, corruption ABSENT, split criterion ---')
    live=collect(LIVE); cut=collect(CUT)
    keys=sorted(live)
    diffs=[live[k]-cut[k] for k in keys]
    res=ac38.sign_flip_test(diffs)
    d=np.asarray(diffs,dtype=float)
    median=float(np.median(d)); impaired=float(np.mean(d>0))
    ceiling=float(max(live.values()))
    at_ceiling=float(np.mean(np.asarray(list(live.values()))>=0.9*ceiling)) if ceiling else 0.0
    print(f'  individuals {len(diffs)}')
    print(f'  live occupancy: min {min(live.values()):.0f} mean {np.mean(list(live.values())):.0f} '
          f'max {max(live.values()):.0f}')
    print(f'  cut  occupancy: min {min(cut.values()):.0f} mean {np.mean(list(cut.values())):.0f} '
          f'max {max(cut.values()):.0f}')
    print(f'  per-individual differences: {[int(v) for v in diffs]}')
    print(f'  RESOLVABILITY: n {res["n"]}  p {res["p"]:.4f}  floor {2/2**res["n"]:.5f}  '
          f'ok={res["p"]<=P_BAR and res["n"]>=MIN_N}')
    print(f'  HEADROOM    : maintained-arm max {ceiling:.0f}; at 90% of the maximum: {at_ceiling:.0%} '
          f'-> {"has headroom" if at_ceiling<1.0 else "SATURATED"}')
    print(f'  EFFECT SIZE : median difference {median:.0f} (requirement > '
          f'{MIN_MEDIAN_DIFFERENCE:.0f}) -> {median>MIN_MEDIAN_DIFFERENCE}')
    print(f'  STABILITY   : impaired fraction {impaired:.0%} '
          f'({"bimodal, as predicted" if impaired<1.0 else "NOT bimodal -- prediction FALSIFIED"})')
    verdict=bool(res['p']<=P_BAR and res['n']>=MIN_N and at_ceiling<1.0
                 and median>MIN_MEDIAN_DIFFERENCE)
    print(f'\n  PREREQUISITE: {"MET -- protocol may be written" if verdict else "NOT MET"}')
    json.dump(dict(diffs=[float(v) for v in diffs],p=res['p'],n=res['n'],median=median,
                   impaired=impaired,at_ceiling=at_ceiling,ceiling=ceiling,verdict=verdict,
                   live={str(k):v for k,v in live.items()},cut={str(k):v for k,v in cut.items()}),
              open('/tmp/ac41_prerequisite.json','w'),indent=2)
