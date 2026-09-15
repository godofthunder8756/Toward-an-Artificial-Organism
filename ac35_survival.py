"""AC35: graded maintenance -- population retained when the organism funds its own maintenance.

What AC34 established, and what this does with it
-------------------------------------------------
AC34 removed AC30's declared metabolic income and had the organism's own sites produce energy. It then
found that a BINARY alive/dead endpoint is unusable: outcomes flip with the run horizon (the same
configuration gives survive-fraction 0.40 at 400 ticks and 0.00 at 800), because production is
proportional to the living population and the viability loop sits near a threshold. A binary criterion
also discards the graded information the rule ORDER actually controls.

So the endpoint here is **population retained at the end of the run** -- graded rather than
all-or-nothing -- and it is a *maintenance* measure: the order decides which sites get renewed,
production decides how many renewals are affordable, and the two feed back.

Claim to be tested: after the environment's stress regime changes so a different order is best, an
organism that can release its stored order and search again retains more population than one that
cannot. Gate shape: separation of minima (the "cannot hold" form), as in AC18/AC32/AC33.

This module contains the study machinery AND the prerequisite measurement. No protocol exists until the
prerequisite is met; see __main__.
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

# Settled by AC34's scan: the graded regime (sampled orders end with 17, 18 or 19 sites of 24).
ENERGY_PER_SITE=1
PRODUCTION_PERIOD=4
RENEW_ENERGY=5
STARVATION_TICKS=40
TICKS=600
RATES_A=acq.stress_rates()
RATES_B=tuple(reversed(RATES_A))
REGIMES={'A':RATES_A,'B':RATES_B}
SCORING_SEEDS=ac32.SCORING_SEEDS          # paired: one fixed set shared by every arm
ARMS=ac32.ARMS

SOURCES=[]                                # filled by the protocol; the runner refuses to run without it


class World:
    """Six regions of sites, stressed by the environment, maintained out of the organism's own
    production. Copied from AC34's engineering module rather than mutating it, so AC34's tests keep
    their meaning; the parameters are the settled ones."""

    def __init__(self,seed,rates=None):
        self.rng=np.random.default_rng([seed,3501])
        self.rates=rates if rates is not None else RATES_A
        self.life=[acq.CHILD_LIFE]*acq.SLOTS
        self.energy=64
        self.tick_count=0; self.starved=0; self.dead=False
        self.renewals=0; self.produced=0

    def urgency(self):
        word=0
        for k in range(acq.REGIONS):
            seg=self.life[k*acq.SITES:(k+1)*acq.SITES]
            if any(0<v<=acq.URGENT for v in seg): word|=1<<k
        return word

    def _stress_one(self,k):
        seg=slice(k*acq.SITES,(k+1)*acq.SITES)
        occupied=[i for i in range(acq.SITES) if self.life[seg.start+i]>0]
        if occupied:
            i=occupied[int(self.rng.integers(0,len(occupied)))]
            self.life[seg.start+i]=acq.URGENT

    def environment_tick(self):
        for k,rate in enumerate(self.rates):
            if self.rng.random()<rate: self._stress_one(k)

    def tick(self,action):
        self.tick_count+=1
        for i in range(acq.SLOTS):
            if self.life[i]==1: self.life[i]=0
            elif self.life[i]>1: self.life[i]-=1
        if self.tick_count%PRODUCTION_PERIOD==0:
            productive=sum(1 for v in self.life if v>=ENERGY_PER_SITE)
            self.energy+=productive; self.produced+=productive
        acted=False
        if action is not None:
            seg=slice(action*acq.SITES,(action+1)*acq.SITES)
            live=[i for i in range(acq.SITES) if self.life[seg.start+i]>0]
            if live and self.energy>=RENEW_ENERGY:
                most_urgent=min(live,key=lambda i:self.life[seg.start+i])
                self.energy-=RENEW_ENERGY
                self.life[seg.start+most_urgent]=acq.CHILD_LIFE
                self.renewals+=1; acted=True
        self.starved=self.starved+1 if (action is not None and not acted) else 0
        self.environment_tick()
        if sum(1 for v in self.life if v>0)<1 or self.starved>=STARVATION_TICKS:
            self.dead=True


def run(order,seed,ticks=TICKS,rates=None):
    w=World(seed,rates=rates)
    for _ in range(ticks):
        if w.dead: break
        word=w.urgency(); action=None
        for position in order:
            if word>>position&1: action=position; break
        w.tick(action)
    return dict(sites=sum(1 for v in w.life if v>0),dead=w.dead,renewals=w.renewals,
                produced=w.produced)


def rating(order,rates,seeds=SCORING_SEEDS,ticks=TICKS):
    return float(np.mean([run(order,s,ticks,rates=rates)['sites'] for s in seeds]))


def climb(start,neighbourhood=asc.swaps,rates=RATES_A):
    """Steepest ascent over the swap neighbourhood, scored by RETAINED POPULATION.

    AC33's `asc.climb` cannot be reused: it calls `ac32.rating` internally, which scores sites retained
    in the AC30 world with a declared income. This study's endpoint is the same quantity in a world
    the organism funds itself, so the climb is rebuilt here against that rating -- a small duplication,
    declared rather than hidden."""
    current=tuple(start); score=rating(current,rates); steps=0
    while True:
        best=current; best_score=score
        for cand in neighbourhood(current):
            s=rating(cand,rates)
            if s>best_score: best,best_score=cand,s
        if best==current: return current,score,steps
        current,score=best,best_score; steps+=1


def search(rates,start):
    order,score,_=climb(start,asc.swaps,rates)
    return order,score


def noise_of_order(order,rates,sets=8,prefix=9200,ticks=TICKS):
    out=[rating(order,rates,tuple(range(prefix+50*k,prefix+50*(k+1))),ticks) for k in range(sets)]
    return float(np.std(out)),float(min(out)),float(max(out))


def hold(arm_name,seed,opt):
    start=tuple(int(x) for x in np.random.default_rng([seed,3501]).permutation(6))
    if arm_name in ('learner_both','no_release'):
        stored,_=search(RATES_A,start)
    else:
        stored=start
    if arm_name=='learner_both':
        r=reg.Register(); r.write(reg.lehmer(start))      # release: overwrite the store
        stored,_=search(RATES_B,start)
    elif arm_name=='oracle_a':
        stored=opt['A'][0]
    elif arm_name=='oracle_b':
        stored=opt['B'][0]
    r=reg.Register(); r.write(reg.lehmer(stored))
    held=r.read(); assert held is not None
    return held


def individual(seed,opt):
    row=dict(seed=seed)
    for arm_name in ARMS:
        held=hold(arm_name,seed,opt)
        row[arm_name]=dict(held=list(held),post=rating(held,RATES_B))
    return row


if __name__=='__main__':
    print(__doc__)
    print('--- prerequisite: does graded retention discriminate under regime B? ---')
    sample=list(itertools.permutations(range(6)))[::6]        # 120 orders
    scores={o:rating(o,RATES_B,seeds=(0,1,2)) for o in sample}
    ranked=sorted(scores.items(),key=lambda kv:-kv[1])
    print(f'  sample {len(sample)} orders: best {ranked[0][1]:.2f}  median '
          f'{ranked[len(ranked)//2][1]:.2f}  worst {ranked[-1][1]:.2f}  '
          f'spread {ranked[0][1]-ranked[-1][1]:.2f}')
    sd,lo,hi=noise_of_order(ranked[0][0],RATES_B)
    print(f'  per-order noise on 8 disjoint seed sets: sd {sd:.2f} range {lo:.2f}-{hi:.2f}')
    margin=ranked[0][1]-ranked[-1][1]
    print(f'  margin/noise = {margin/sd:.2f}' if sd else '  noise zero')
    print(f'  validity criterion (>=10): {sd>0 and margin/sd>=10}')
