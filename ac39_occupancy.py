"""AC39: does repair-maintained OCCUPANCY keep the organism active? -- prerequisite first.

The claim this is a prerequisite for
------------------------------------
AC19-M diagnosed why AC19's register-cut arms die: not because of corruption (they die 0/4 even with the
register damage rate set to zero), but because without the repair action the register empties, an empty
register stops driving activity, and the organism winds down. So the closure question has a sharper
answer than AC14 or AC19 alone: the state's INTEGRITY is not load-bearing, its OCCUPANCY is.

The claim: an organism whose register occupancy is maintained by repair stays active longer than one
whose occupancy is not, **with corruption absent**, so the integrity channel is switched off by
construction.

Prerequisite, per the AC31/AC35/AC37 precedent and AC38's rules
---------------------------------------------------------------
1. the endpoint must resolve the contrast: |mean paired difference| / sigma_difference >= 3, with the
   difference taken per individual and sigma measured across them;
2. power: the exact sign-flip test's floor at n individuals is 2/2^n, so n >= 8 (0.0078) rather than the
   n = 4 every earlier engineering pass used (0.125, which can never be significant);
3. the integrity channel is off by construction: reg_rate = 0.

Engineering only until the prerequisite passes. No protocol, no final seeds, no claim.
"""
import json
import numpy as np
import ac19
import ac38_variance as ac38

SEEDS=tuple(range(8))
HISTORIES=(0,1)
LIVE='two_way'
CUT='two_way_no_repair'
SOURCES=[]                      # filled only if a protocol is written


def active_ticks(arm,seed,history,reg_rate=0.0):
    """The graded endpoint: how many ticks the organism acts on. 0.0 disables register corruption, so
    the integrity channel is off by construction."""
    r=ac19.run(seed,history,arm,reg_rate=reg_rate)
    return int(r['ledger']['active'])


def collect(arm):
    return {(seed,history):active_ticks(arm,seed,history)
            for seed in SEEDS for history in HISTORIES}


if __name__=='__main__':
    print(__doc__)
    print('--- prerequisite: contrast and power, corruption ABSENT ---')
    live=collect(LIVE); cut=collect(CUT)
    diffs=[live[k]-cut[k] for k in sorted(live)]
    m=float(np.mean(diffs)); sd=float(np.std(diffs))
    t=ac38.sign_flip_test(diffs)
    print(f'  individuals: {len(diffs)} (seeds {SEEDS[0]}-{SEEDS[-1]} x histories {HISTORIES})')
    print(f'  live active ticks: min {min(live.values())} mean {np.mean(list(live.values())):.0f}')
    print(f'  cut  active ticks: min {min(cut.values())} mean {np.mean(list(cut.values())):.0f}')
    print(f'  paired differences: {diffs}')
    print(f'  mean difference {m:.0f}   sigma_difference {sd:.1f}   ratio {m/sd if sd else float("inf"):.2f}')
    print(f'  sign-flip test: observed {t["observed"]:.0f}, p {t["p"]:.4f} (floor for n={len(diffs)} is '
          f'{2/2**len(diffs):.4f})')
    print(f'\n  criterion |mean delta| / sigma_delta >= 3: {sd>0 and abs(m)/sd>=3}')
    print(f'  power sufficient (n >= 8): {len(diffs)>=8}')
    print(f'  integrity channel off by construction (reg_rate=0): True')
    verdict=bool(sd>0 and abs(m)/sd>=3 and len(diffs)>=8)
    print(f'\n  PREREQUISITE: {"MET -- a protocol may be written" if verdict else "NOT MET"}')
    json.dump(dict(diffs=diffs,mean=m,sigma=sd,ratio=(m/sd if sd else None),p=t['p'],
                   n=len(diffs),verdict=verdict),
              open('/tmp/ac39_prerequisite.json','w'),indent=2)
