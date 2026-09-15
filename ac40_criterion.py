"""AC40: the split criterion -- resolvability, effect size, stability, headroom.

Why
---
AC39 stopped on the criterion AC38 handed down: |mean paired difference| / sigma_difference >= 3. It
failed at 2.45 while the exact paired test gave p = 0.0001 at n = 16 -- and a 3-seed subset of the same
world gave 10.17. A single mean/sd ratio mixes three different questions and is unstable because of it:

  * RESOLVABILITY -- can the design tell the arms apart at all? Power (n) and an exact test on the
    paired differences answer this, with no distributional assumption.
  * EFFECT SIZE -- how large is the difference? A ratio of mean to sd is one way to state it, and it is
    NOT a significance measure; it must be declared separately and justified for the endpoint.
  * STABILITY -- is the answer the same whichever individuals you sampled? AC39's ratio was not: it
    moved by a factor of four on a seed subset, because the population was bimodal.
  * HEADROOM -- does the endpoint have room to show the maintained arm's advantage, or is that arm
    pinned at a ceiling? AC39's live arm sat at exactly 4096 ticks (every tick), so a large part of its
    variance structure was an artefact of saturation.

This module computes all four, so a successor can declare each part in advance instead of inheriting one
number that quietly stands in for the others. It is a framework, not a study: no world, no protocol, no
final seeds, and no claim.
"""
import json
from pathlib import Path
import numpy as np
import ac38_variance as ac38

P_VALUE_BAR=0.01
MIN_N=8
STABILITY_BAR=1.5          # the ratio must not vary by more than this across halves of the individuals


def resolvability(differences):
    t=ac38.sign_flip_test(differences)
    n=t['n']
    return dict(n=n,mean=t['observed'],null_sd=t['null_sd'],p=t['p'],floor=2.0/2**n,
                power_ok=n>=MIN_N,significant=t['p']<=P_VALUE_BAR,
                resolved=bool(n>=MIN_N and t['p']<=P_VALUE_BAR))


def effect_size(differences):
    d=np.asarray(differences,dtype=float)
    sd=float(np.std(d))
    return dict(mean=float(np.mean(d)),sd=sd,
                ratio=(float(np.mean(d)/sd) if sd>0 else float('inf')),
                median=float(np.median(d)),impaired_fraction=float(np.mean(d>0)))


def stability(differences):
    """Split the individuals in half two ways and compare the effect-size ratio across the parts.
    AC39's world moves by a factor of four, because its population is bimodal."""
    d=list(differences); n=len(d)
    if n<4: return dict(ratios=[],spread=None,stable=None)
    halves=[d[:n//2],d[n//2:],d[0::2],d[1::2]]
    ratios=[]
    for part in halves:
        arr=np.asarray(part,dtype=float)
        ratios.append(float(np.mean(arr)/np.std(arr)) if np.std(arr)>0 else float('inf'))
    finite=[r for r in ratios if np.isfinite(r)]
    spread=(max(finite)/min(finite) if len(finite)>=2 and min(finite)>0 else None)
    return dict(ratios=[round(r,2) for r in ratios],spread=spread,
                stable=(spread is not None and spread<=STABILITY_BAR))


def headroom(values,ceiling):
    arr=np.asarray(values,dtype=float)
    at=float(np.mean(arr>=ceiling))
    return dict(ceiling=ceiling,at_ceiling_fraction=at,saturated=bool(at>=0.9))


def audit(differences,live_values=None,ceiling=None):
    out=dict(resolvability=resolvability(differences),effect_size=effect_size(differences),
             stability=stability(differences))
    if live_values is not None and ceiling is not None:
        out['headroom']=headroom(live_values,ceiling)
    print(f'  resolvability : n={out["resolvability"]["n"]}  p={out["resolvability"]["p"]:.4f} '
          f'(floor {out["resolvability"]["floor"]:.4f})  resolved={out["resolvability"]["resolved"]}')
    e=out['effect_size']
    print(f'  effect size   : mean {e["mean"]:.1f}  sd {e["sd"]:.1f}  ratio {e["ratio"]:.2f}  '
          f'median {e["median"]:.0f}  impaired {e["impaired_fraction"]:.0%}')
    s=out['stability']
    print(f'  stability     : half-sample ratios {s["ratios"]}  spread {s["spread"]}  '
          f'stable={s["stable"]}')
    if 'headroom' in out:
        h=out['headroom']
        print(f'  headroom      : {h["at_ceiling_fraction"]:.0%} of individuals at the ceiling '
              f'({h["ceiling"]})  saturated={h["saturated"]}')
    return out


if __name__=='__main__':
    print(__doc__)
    import ac19
    print('\n--- AC39 engineering data (16 individuals, corruption absent) ---')
    seeds=range(8); histories=(0,1)
    cut={(s,h):int(ac19.run(s,h,'two_way_no_repair',reg_rate=0.0)['ledger']['active'])
         for s in seeds for h in histories}
    live={(s,h):int(ac19.run(s,h,'two_way',reg_rate=0.0)['ledger']['active'])
          for s in seeds for h in histories}
    diffs=[live[k]-cut[k] for k in sorted(live)]
    ac39=audit(diffs,live_values=list(live.values()),ceiling=ac19.TICKS)
    print(f'  -> AC39 stays STOPPED: the split was not declared before its data.')

    print('\n--- the frozen studies, post hoc (labelled as such) ---')
    out={}
    for root,arms,label in (('ac33_results_v1',('learner_both','no_release'),'AC33'),
                            ('ac36_results_v1',('learner_both','no_release'),'AC36'),
                            ('ac32_results_v1',('learner_both','no_release'),'AC32')):
        rows=[json.loads(l) for l in (Path(root)/'rows.jsonl').read_text().splitlines() if l.strip()]
        d=[r[arms[0]]['post']-r[arms[1]]['post'] for r in rows]
        print(f'  {label}:')
        out[label]=audit(d)
    out['AC39']=ac39
    json.dump(out,open('/tmp/ac40_criterion.json','w'),indent=2,default=str)
