"""AC42: which endpoint can carry the occupancy claim? A survey of the quantities already measured.

Why a survey
------------
Two consecutive prerequisite stops failed on the ENDPOINT rather than the world:
  AC39: "ticks active" saturated (4096 for every live individual -- no headroom).
  AC41: "register occupancy" was a structural constant (21 for every live individual -- no variance).
Both were chosen by reasoning and rejected on measurement. `ac19.run` already returns a rich set of
scalar quantities per individual, so the cheap move is to survey all of them at once and rank them by the
properties a claim needs:

  * VARIANCE across individuals (a constant cannot be an endpoint);
  * HEADROOM (no ceiling that the maintained arm already sits on);
  * RESOLUTION of the live-vs-cut contrast (exact sign-flip test, with power n >= 8);
  * an IMPAIRED FRACTION away from 100% (the bimodality AC41 predicted and did not find in occupancy).

This is a survey, not a study: no protocol, no final seeds, no claim. Its output is a shortlist.
"""
import json
import numpy as np
import ac19
import ac38_variance as ac38

SEEDS=tuple(range(8))
HISTORIES=(0,1)
LIVE='two_way'
CUT='two_way_no_repair'
SKIP={'arm','seed','history','sticky','targeted','damage_rate','reg_rate','cut_mode','corruption',
      'move','ticks','state_hash','ledger','demand','register_history','chan_late'}
SOURCES=[]


def scalars(arm,seed,history,reg_rate=0.0):
    """Every numeric, non-container field of the run result, plus two useful ledger entries."""
    r=ac19.run(seed,history,arm,reg_rate=reg_rate)
    out={}
    for k,v in r.items():
        if k in SKIP: continue
        if isinstance(v,(int,float)) and not isinstance(v,bool): out[k]=float(v)
    led=r.get('ledger') or {}
    for k in ('active','spent_e','W_birth','memory_writes','deposits','converted','spent_m'):
        if k in led: out[f'ledger.{k}']=float(led[k])
    return out


def survey():
    per={}
    for label,arm in (('live',LIVE),('cut',CUT)):
        for s in SEEDS:
            for h in HISTORIES:
                for k,v in scalars(arm,s,h).items():
                    per.setdefault(k,{'live':[],'cut':[]})[label].append(v)
    return per


def rank(per):
    rows=[]
    for k,d in per.items():
        live=np.asarray(d['live'],dtype=float); cut=np.asarray(d['cut'],dtype=float)
        if len(live)!=len(cut) or len(live)<8: continue
        diffs=live-cut
        rel=ac38.sign_flip_test(diffs)
        mx=float(np.max(live)) if len(live) else 0.0
        at_ceiling=float(np.mean(live>=mx)) if mx else 1.0
        rows.append(dict(
            quantity=k,
            live_mean=float(np.mean(live)),live_sd=float(np.std(live)),
            cut_mean=float(np.mean(cut)),cut_sd=float(np.std(cut)),
            variance_ok=bool(np.std(np.concatenate([live,cut]))>0),
            headroom=bool(at_ceiling<0.9 and np.std(live)>0),
            p=rel['p'],impaired_fraction=float(np.mean(diffs>0)),
            median_difference=float(np.median(diffs)),
            bimodal=bool(0.0<np.mean(diffs>0)<1.0),
            usable=bool(np.std(np.concatenate([live,cut]))>0 and at_ceiling<0.9
                        and rel['p']<=0.01 and rel['n']>=8)))
    return sorted(rows,key=lambda r:(not r['usable'],not r['bimodal'],-abs(r['median_difference'])))


if __name__=='__main__':
    print(__doc__)
    per=survey()
    rows=rank(per)
    print(f'quantities surveyed: {len(rows)}    individuals per arm: {len(SEEDS)*len(HISTORIES)}')
    print(f'\n{"quantity":34s} {"live mean":>10s} {"live sd":>8s} {"cut mean":>9s} {"p":>7s} '
          f'{"impaired":>9s} {"usable":>7s} {"bimodal":>8s}')
    for r in rows:
        print(f'{r["quantity"]:34s} {r["live_mean"]:>10.1f} {r["live_sd"]:>8.1f} '
              f'{r["cut_mean"]:>9.1f} {r["p"]:>7.4f} {r["impaired_fraction"]:>8.0%} '
              f'{str(r["usable"]):>7s} {str(r["bimodal"]):>8s}')
    usable=[r for r in rows if r['usable']]
    print(f'\nusable endpoints (variance, headroom, resolved at n>={8}): {len(usable)}')
    for r in usable[:6]:
        print(f'  {r["quantity"]:32s} median difference {r["median_difference"]:.0f}  '
              f'impaired {r["impaired_fraction"]:.0%}  {"BIMODAL" if r["bimodal"] else ""}')
    json.dump(rows,open('/tmp/ac42_survey.json','w'),indent=2)
