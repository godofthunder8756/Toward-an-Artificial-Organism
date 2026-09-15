"""AC31: re-acquisition -- can the organism follow the world when the world's demands change?

The claim, stated so the gate can follow its shape
--------------------------------------------------
After the environment's stress regime changes so that a DIFFERENT order is best, an organism that can
both release its stored order and search again ends up performing at the level the new regime
permits; an organism that is structurally unable to release its stored order, or unable to search at
all, does not.

This is a "cannot hold" claim, and by this line's standing lesson (AC16/AC17/AC18) its gate must be a
**separation of minima**: the capable arm's worst individual at or above the bar, and the incapable
arms' worst individuals below it. AC16's mean-margin gate was falsified by 0.006 and AC17's
"better in every individual" was unsatisfiable, so the shape is not a detail.

Prerequisites, measured before any claim
----------------------------------------
1. the two regimes have different optima (`best_A != best_B`);
2. the old optimum is MATERIALLY worse under the new regime, by more than the measurement noise --
   otherwise there is nothing to re-acquire and the study would repeat AC13's failure.

Arms
----
  learner_both   searches under A, stores; after the switch it releases and searches again
  no_release     searches under A, stores; after the switch it may NOT release or re-search
  no_search      never searches; acts on its initial order throughout
  preserve       state-blind control: keeps its initial order
  oracle_b       handed the new regime's optimum (SCAFFOLD: non-autonomous, used as the ceiling)

Endpoint: sites retained under regime B over the post-switch window, averaged over scoring seeds.

STATUS: this design was FALSIFIED by its own engineering controls (AC31_ENGINEERING_v1.md) before any
protocol was written or any final seed run. The capable arm did not beat the incapable arms, because
the comparison is unpaired and per-individual seed noise is comparable to the margin. See the module's
__main__ for the numbers and the candidate design fixes.
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
EVALS=80                       # search budget per phase, declared
SCORE_SEEDS=3                  # multi-seed scoring: the AC30 diagnosis of noisy single-seed search
TICKS=acq.TICKS
REGIMES={'A':RATES_A,'B':RATES_B}
ARMS=('learner_both','no_release','no_search','preserve','oracle_b')
SOURCES=['ac31_reacquire.py','ac30_acquire.py','ac29_register.py','ac27_schedule.py',
         'AC31_PROTOCOL_v1.md']


def rating(order,rates,seeds=(0,1,2),ticks=TICKS):
    return float(np.mean([acq.run(order,s,ticks,rates=rates)[0] for s in seeds]))


def sweep(rates,seeds=(0,1,2),ticks=TICKS):
    return {o:rating(o,rates,seeds,ticks) for o in itertools.permutations(range(6))}


def search(rates,rng,evals=EVALS,seeds=SCORE_SEEDS,ticks=TICKS):
    """Mutate-and-keep over the 720 orders, scored on multiple seeds (AC30 showed single-seed
    scoring makes the hill-climb stop early on a lucky draw)."""
    current=tuple(int(x) for x in rng.permutation(6))
    best=rating(current,rates,tuple(range(seeds)),ticks)
    for _ in range(evals):
        i,j=rng.integers(0,6,2)
        cand=list(current); cand[i],cand[j]=cand[j],cand[i]; cand=tuple(cand)
        s=rating(cand,rates,tuple(range(seeds)),ticks)
        if s>=best: current,best=cand,s
    return current,best


def arm(arm_name,seed,optima):
    """One individual. Returns the order it holds under regime B and the score it achieves there.

    The order of record lives in AC29's register: it is written and read back, so the store is
    genuinely in the loop. This study declares NO damage -- the register's integrity question was
    AC29/AC30's, and mixing it in here would confound re-acquisition with retention."""
    rng=np.random.default_rng([seed,3101])
    initial=tuple(int(x) for x in rng.permutation(6))
    stored=None
    if arm_name in ('learner_both','no_release'):
        stored,_=search(RATES_A,rng)                          # acquire under regime A
    if arm_name=='learner_both':
        # release: the register is overwritten with a placeholder, then a new order is acquired
        r=reg.Register(); r.write(reg.lehmer(initial))
        stored,_=search(RATES_B,rng)                          # re-acquire under regime B
    elif arm_name=='no_release':
        pass                                                  # structurally unable to overwrite
    elif arm_name in ('no_search','preserve'):
        stored=initial
    elif arm_name=='oracle_b':
        stored=optima['B'][0]
    r=reg.Register(); r.write(reg.lehmer(stored))
    held=r.read()
    assert held is not None, 'a written order must read back'
    return dict(arm=arm_name,seed=seed,held=list(held),
                post=rating(held,RATES_B,seeds=(seed,seed+100,seed+200)))


if __name__=='__main__':
    print(__doc__)
    print('STATUS: the design was FALSIFIED in engineering (seeds 0-3) before any protocol or final')
    print('seed. The capable arm did not beat the incapable ones: learner_both mean 11.83 vs')
    print('no_search 12.00 and oracle_b 12.33, against a 2.67-site margin. Cause: the arm comparison')
    print('is UNPAIRED and per-individual seed noise (~1 site) is comparable to the margin. See')
    print('AC31_ENGINEERING_v1.md. Candidate fixes are design changes -- pair the comparison on a')
    print('shared seed set, raise replication, and/or sharpen the world so a random order is worse')
    print('than 88% of optimal -- and must be re-engineered and re-declared BEFORE any final seed.')
    print('There is no AC31_PROTOCOL_v1.md and no ac31_results_* directory, by design.')
    raise SystemExit(0)
