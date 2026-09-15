"""AC32: re-acquisition, re-engineered -- paired scoring, more replication, a justifiable bar.

What AC31 got wrong, and what changes here
------------------------------------------
AC31's engineering falsified its own design: `learner_both` (mean 11.83) came out BELOW `no_search`
(12.00) and `oracle_b` (12.33) against a 2.67-site margin. The diagnosis had two measured parts:

  1. **The comparison was unpaired.** Each arm's individuals were scored on their own seed sets, so
     scoring variance entered every arm independently. The oracle rated 12.0-13.0 per individual while
     the same order rated 13.67 on the sweep's seeds -- ~1 site of noise against a 2.67-site margin.
  2. **A random order was already ~88% of optimal**, so the per-individual learning margin was small
     relative to that noise.

This module changes the MEASUREMENT, not the claim, and it does so before looking at any arm:

  * **Paired scoring**: every arm's held order is rated on the SAME fixed set of scoring seeds, so the
    shared seed-set variance cancels in the arm comparison.
  * **More replication**: more individuals, and the search itself scores each candidate on more seeds
    (AC30's diagnosis: single-seed scoring makes the hill-climb stop on a lucky draw).
  * **A noise measurement up front**: a fixed order rated on many disjoint seed sets gives the
    per-order noise directly, so the required bar can be justified from a ratio rather than chosen.

What is NOT changed: the claim, the arms, the regime pair, and the gate shape (separation of minima).
The world is NOT retuned. If the margin still cannot clear the noise after the measurement is fixed,
the honest outcome is another falsification, recorded as such.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
import ac30_acquire as acq
import ac29_register as reg

RATES_A=acq.stress_rates()
RATES_B=tuple(reversed(RATES_A))
REGIMES={'A':RATES_A,'B':RATES_B}

# Paired design: ONE scoring set, shared by every arm.
SCORING_SEEDS=tuple(range(9000,9012))          # 12 seeds
SEARCH_EVALS=120                               # search budget per phase
SEARCH_SEEDS=tuple(range(0,5))                 # seeds used inside the search
TICKS=acq.TICKS

ARMS=('learner_both','no_release','no_search','preserve','oracle_a','oracle_b')
SOURCES=['ac32_reacquire.py','ac30_acquire.py','ac29_register.py','AC32_PROTOCOL_v1.md']


def rating(order,rates,seeds=SCORING_SEEDS,ticks=TICKS):
    """Rate an order: mean sites retained over the shared scoring seeds."""
    return float(np.mean([acq.run(order,s,ticks,rates=rates)[0] for s in seeds]))


def sweep(rates,seeds=SCORING_SEEDS,ticks=TICKS):
    return {o:rating(o,rates,seeds,ticks) for o in itertools.permutations(range(6))}


def optima(seeds=SCORING_SEEDS,ticks=TICKS):
    sA=sweep(RATES_A,seeds,ticks); sB=sweep(RATES_B,seeds,ticks)
    oA=max(sA,key=sA.get); oB=max(sB,key=sB.get)
    return dict(A=(oA,sA[oA]),B=(oB,sB[oB])),sA,sB


def search(rates,rng,restarts=4,evals_per_restart=40,seeds=SEARCH_SEEDS,ticks=TICKS):
    """Mutate-and-keep with RESTARTS, keeping the best result found.

    AC30 measured six starts converging to six distinct local optima -- premature convergence -- and
    named the fix: more seeds per evaluation or a population, not more iterations. This is that fix,
    applied before any arm comparison and derived from AC30's measurement rather than from whether the
    arms separate."""
    overall=None; overall_score=-1.0
    for _ in range(restarts):
        current=tuple(int(x) for x in rng.permutation(6))
        best=float(np.mean([acq.run(current,s,ticks,rates=rates)[0] for s in seeds]))
        for _ in range(evals_per_restart):
            i,j=rng.integers(0,6,2)
            cand=list(current); cand[i],cand[j]=cand[j],cand[i]; cand=tuple(cand)
            s=float(np.mean([acq.run(cand,k,ticks,rates=rates)[0] for k in seeds]))
            if s>=best: current,best=cand,s
        if best>overall_score: overall,overall_score=current,best
    return overall,overall_score


def hold(arm_name,seed,rng,opt):
    """The order an arm holds under regime B. Acquisition happens under A; the register is the store
    of record (written and read back). NO damage is applied: the register's integrity question
    belongs to AC29/AC30 and mixing it in would confound re-acquisition with retention."""
    initial=tuple(int(x) for x in rng.permutation(6))
    if arm_name in ('learner_both','no_release'):
        stored,_=search(RATES_A,rng)
    else:
        stored=initial
    if arm_name=='learner_both':
        r=reg.Register(); r.write(reg.lehmer(initial))    # release: overwrite the store
        stored,_=search(RATES_B,rng)                       # then re-acquire under B
    elif arm_name=='oracle_a':
        stored=opt['A'][0]
    elif arm_name=='oracle_b':
        stored=opt['B'][0]
    r=reg.Register(); r.write(reg.lehmer(stored))
    held=r.read()
    assert held is not None,'a written order must read back'
    return held


def individual(seed,opt):
    rng=np.random.default_rng([seed,3201])
    row=dict(seed=seed)
    for arm_name in ARMS:
        # a fresh rng per arm, but the same seed: arms differ only in their capabilities
        held=hold(arm_name,seed,np.random.default_rng([seed,3211]),opt)
        row[arm_name]=dict(held=list(held),post=rating(held,RATES_B))
    return row


def noise_of_order(order,sets=8,prefix=9100,ticks=TICKS):
    """Per-order scoring noise: the same order rated on many disjoint seed sets."""
    out=[rating(order,RATES_B,tuple(range(prefix+50*k,prefix+50*(k+1))),ticks) for k in range(sets)]
    return float(np.std(out)),float(min(out)),float(max(out))


# Declared optima, measured in engineering and recorded in AC32_PROTOCOL_v1.md. The full sweep at the
# paired scoring set is expensive (~4 minutes per regime), so the finals use the declared values rather
# than recomputing them; the protocol carries their provenance.
DECLARED_OPTIMA={'A':((2,5,3,4,0,1),12.83),'B':((2,0,1,3,5,4),12.67)}

FINAL_SEEDS=tuple(range(3300,3312))        # declared in AC32_PROTOCOL_v1.md
BAR=12.00                                  # declared in AC32_PROTOCOL_v1.md


def gates(rows):
    """The eight pre-declared gates. Nothing here may be adjusted after seeing the rows."""
    post=lambda arm: [r[arm]['post'] for r in rows]
    out={}
    out['G1_oracle_b_ceiling_at_or_above_bar']=min(post('oracle_b'))>=BAR
    out['G2_learner_worst_at_or_above_bar']=min(post('learner_both'))>=BAR
    out['G3_no_release_best_below_bar']=max(post('no_release'))<BAR
    out['G4_oracle_a_best_below_bar']=max(post('oracle_a'))<BAR
    out['G5_state_blind_means_below_bar']=(float(np.mean(post('no_search')))<BAR
                                           and float(np.mean(post('preserve')))<BAR)
    out['G6_all_arms_complete']=all(len(r)==len(ARMS)+1 for r in rows) and \
                               all(arm in r for r in rows for arm in ARMS)
    out['G8_register_in_the_loop']=all('held' in r[arm] and len(r[arm]['held'])==6
                                       for r in rows for arm in ARMS)
    out['G7_determinism']=None              # filled by the runner's spot check
    return out


def main(seeds=FINAL_SEEDS,root='ac32_results_v1'):
    outdir=Path(root); outdir.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES}
    (outdir/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (outdir/'rows.jsonl').open('x') as f:
        for seed in seeds:
            row=individual(seed,DECLARED_OPTIMA)
            rows.append(row); f.write(json.dumps(row)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,
                                  learner=row['learner_both']['post'],
                                  no_release=row['no_release']['post'],
                                  no_search=row['no_search']['post'],
                                  oracle_b=row['oracle_b']['post'])),flush=True)
    # G7: determinism spot check on the first two individuals
    spot=all(individual(s,DECLARED_OPTIMA)==r for s,r in zip(seeds[:2],rows[:2]))
    g=gates(rows); g['G7_determinism']=spot
    post=lambda arm: [r[arm]['post'] for r in rows]
    summary={arm:dict(min=min(post(arm)),mean=float(np.mean(post(arm))),max=max(post(arm)))
             for arm in ARMS}
    (outdir/'results.json').write_text(json.dumps(dict(bar=BAR,seeds=list(seeds),hashes=hashes,
                                                       gates=g,summary=summary,rows=rows),indent=2))
    print(json.dumps(dict(gates=g,summary=summary),indent=2))
    return g,summary


if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='finals': main()
    else:
        print(__doc__)
        print('Run the declared finals with: .venv/bin/python -B ac32_reacquire.py finals')
        print('Protocol: AC32_PROTOCOL_v1.md (frozen; final seeds 3300-3311; BAR=12.00)')
