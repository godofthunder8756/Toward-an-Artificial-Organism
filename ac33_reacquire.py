"""AC33: re-acquisition with a STEEPEST-ASCENT search -- the AC32 failure removed by mechanism.

What AC32 left open
-------------------
AC32 (paired scoring) passed 7 of 8 gates; G2 failed because one individual's search settled on an
order rated 11.75 while its peers reached 12.33-12.42 against a 12.67 ceiling. The cause was the
mechanism: mutate-and-keep accepting RANDOM single swaps, 40 evaluations per restart, which stops as
soon as no random neighbour improves.

What AC33 changes -- measured before it was declared
---------------------------------------------------
`ac33_search.py` measured the landscape directly: with paired scoring the rating is a deterministic
function of the order, so steepest ascent is well defined. Results over 24 random starts:

    swaps only                    min 12.33  mean 12.62  max 12.67   24/24 within 0.34 of ceiling
    swaps+insertions+reversals    min 12.33  mean 12.65  max 12.67   24/24 within 0.34 of ceiling

So the landscape is not the problem and a richer neighbourhood is not needed: the weaker *mechanism*
was. **Steepest ascent** -- evaluate every neighbour, move to the best, repeat until nothing improves
-- reaches within 0.34 of the ceiling from every start, in ~2.4 steps, and costs FEWER rating calls
than AC32's search (~36 versus ~160). There are 6 distinct local optima under swaps and the worst is
12.33, above the declared bar of 12.00.

Everything else is held fixed: regimes, arms, endpoint, paired 12-seed scoring, gate shape
(separation of minima), and the bar. The claim is the same claim AC32 tested; only the mechanism that
is supposed to satisfy it has changed.
"""
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np
import ac30_acquire as acq
import ac29_register as reg
import ac32_reacquire as ac32
import ac33_search as asc

RATES_A=ac32.RATES_A
RATES_B=ac32.RATES_B
SCORING_SEEDS=ac32.SCORING_SEEDS          # paired: one fixed set shared by every arm
TICKS=ac32.TICKS
ARMS=ac32.ARMS
DECLARED_OPTIMA=ac32.DECLARED_OPTIMA
BAR=12.00
FINAL_SEEDS=tuple(range(3400,3412))       # declared in AC33_PROTOCOL_v1.md

# The protocol declares exactly this set. The pre-flight check below enforces the equality, which is
# AC32's process lesson: AC32 declared five sources and hashed four.
SOURCES=['ac33_reacquire.py','ac33_search.py','ac32_reacquire.py','ac30_acquire.py',
         'ac29_register.py','AC33_PROTOCOL_v1.md']


def search(rates,start):
    """Steepest ascent over the swap neighbourhood from `start`. Deterministic given the start."""
    order,score,_steps=asc.climb(start,asc.swaps,rates=rates)
    return order,score


def hold(arm_name,seed,opt):
    """The order an arm holds under regime B. The register is the store of record; NO damage."""
    start=tuple(int(x) for x in np.random.default_rng([seed,3301]).permutation(6))
    if arm_name in ('learner_both','no_release'):
        stored,_=search(RATES_A,start)
    else:
        stored=start
    if arm_name=='learner_both':
        r=reg.Register(); r.write(reg.lehmer(start))     # release: overwrite the store
        stored,_=search(RATES_B,start)                    # then re-acquire under B
    elif arm_name=='oracle_a':
        stored=opt['A'][0]
    elif arm_name=='oracle_b':
        stored=opt['B'][0]
    r=reg.Register(); r.write(reg.lehmer(stored))
    held=r.read(); assert held is not None
    return held


def individual(seed,opt=DECLARED_OPTIMA):
    row=dict(seed=seed)
    for arm_name in ARMS:
        held=hold(arm_name,seed,opt)
        row[arm_name]=dict(held=list(held),post=ac32.rating(held,RATES_B))
    return row


def gates(rows):
    post=lambda arm: [r[arm]['post'] for r in rows]
    return {
        'G1_oracle_b_ceiling_at_or_above_bar': min(post('oracle_b'))>=BAR,
        'G2_learner_worst_at_or_above_bar': min(post('learner_both'))>=BAR,
        'G3_no_release_best_below_bar': max(post('no_release'))<BAR,
        'G4_oracle_a_best_below_bar': max(post('oracle_a'))<BAR,
        'G5_state_blind_means_below_bar': (float(np.mean(post('no_search')))<BAR
                                           and float(np.mean(post('preserve')))<BAR),
        'G6_all_arms_complete': all(len(r)==len(ARMS)+1 for r in rows)
                                and all(arm in r for r in rows for arm in ARMS),
        'G7_determinism': None,
        'G8_register_in_the_loop': all(len(r[arm]['held'])==6 for r in rows for arm in ARMS),
    }


def preflight(protocol='AC33_PROTOCOL_v1.md'):
    """AC32's lesson, made real: parse the PROTOCOL's declared source list and require that it equals
    the set this runner hashes. My first version compared SOURCES to itself, which is theatre -- it
    would have passed while AC32's actual failure (5 declared, 4 hashed) went undetected."""
    text=Path(protocol).read_text()
    marker='SOURCES (declared):'
    line=[l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line,f'{protocol} declares no source list'
    declared=[w.strip() for w in line[0].split(marker,1)[1].split() if w.strip()]
    assert set(declared)==set(SOURCES),(
        f'runner hashes {sorted(set(SOURCES))} but the protocol declares {sorted(set(declared))}')
    missing=[s for s in declared if not Path(s).exists()]
    assert not missing,f'declared sources missing on disk: {missing}'
    return declared


def main(seeds=FINAL_SEEDS,root='ac33_results_v1'):
    preflight()
    outdir=Path(root); outdir.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES}
    (outdir/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (outdir/'rows.jsonl').open('x') as f:
        for seed in seeds:
            row=individual(seed)
            rows.append(row); f.write(json.dumps(row)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,learner=row['learner_both']['post'],
                                  no_release=row['no_release']['post'],
                                  no_search=row['no_search']['post'],
                                  oracle_b=row['oracle_b']['post'])),flush=True)
    g=gates(rows)
    g['G7_determinism']=all(individual(s)==r for s,r in zip(seeds[:2],rows[:2]))
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
        print('Protocol: AC33_PROTOCOL_v1.md (final seeds 3400-3411, BAR=12.00)')
