"""AC37: self-sufficiency -- the organism funds its own maintenance, with a graded endpoint.

The problem AC35 left
---------------------
AC35 had the organism's own productive sites supply its energy, and the endpoint collapsed to a 1.00-site
spread against 0.30 of noise, because production scales with the living population: a population near
carrying capacity produces plenty and can maintain itself, so every order converges to 76-80% of the
maximum and the ORDER stops mattering.

The design fix, stated before it is tested
------------------------------------------
Add a **constant metabolic drain** that does not scale with the population. Then the energy balance is

    E' = E + (productive sites)/PRODUCTION_PERIOD - DRAIN - RENEW_ENERGY * renewals

so self-sufficiency requires `productive sites > DRAIN * PRODUCTION_PERIOD`: a **population floor** set
by the economy rather than by carrying capacity. An order that wastes renewals sits nearer that floor; a
good order sits above it. The punishment is graded and continuous rather than a collapse, which is what
AC35's world could not provide -- and nothing scales the drain with the organism's state, so the
feedback that erased AC35's differences is not present in the same form.

Claim to be tested: after the stress regime changes so a different order is best, an organism that can
release its stored order and search again retains more population than one that cannot. Gate shape:
separation of minima. Prerequisite first -- the endpoint must resolve orders (spread/noise >= 10) --
measured in __main__ before any protocol exists.
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
import ac36_survival as ac36

# The chosen economy: settled by the scan in AC37_ENGINEERING_v1.md (production period 4, drain 3 --
# mean 16.22 sites, spread 11.00, noise 0.50, ratio 22.1). Pinned here as the default before the
# protocol is written, because the module becomes a hashed source at that point.
PRODUCTION_PERIOD=4
DRAIN=3
RENEW_ENERGY=5
STARVATION_TICKS=60
TICKS=600
RATES_A=ac36.RATES_A
RATES_B=ac36.RATES_B
SCORING_SEEDS=ac32.SCORING_SEEDS
ARMS=ac32.ARMS
SOURCES=[]


class World:
    def __init__(self,seed,rates=None):
        self.rng=np.random.default_rng([seed,3701])
        self.rates=rates if rates is not None else RATES_A
        self.life=[acq.CHILD_LIFE]*acq.SLOTS
        self.energy=48
        self.tick_count=0; self.starved=0; self.dead=False
        self.renewals=0; self.refusals=0; self.produced=0; self.drained=0

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
        if self.rng.random()<ac36.BURST_PROBABILITY:
            weights=np.array(self.rates); weights=weights/weights.sum()
            for k in self.rng.choice(acq.REGIONS,size=ac36.BURST_WIDTH,replace=False,p=weights):
                self._stress_one(int(k))

    def tick(self,action):
        self.tick_count+=1
        for i in range(acq.SLOTS):
            if self.life[i]==1: self.life[i]=0
            elif self.life[i]>1: self.life[i]-=1
        if self.tick_count%PRODUCTION_PERIOD==0:
            productive=sum(1 for v in self.life if v>=1)
            self.energy+=productive; self.produced+=productive
        self.energy-=DRAIN; self.drained+=DRAIN        # the constant cost of being alive
        acted=False
        if action is not None:
            seg=slice(action*acq.SITES,(action+1)*acq.SITES)
            live=[i for i in range(acq.SITES) if self.life[seg.start+i]>0]
            if live and self.energy>=RENEW_ENERGY:
                most_urgent=min(live,key=lambda i:self.life[seg.start+i])
                self.energy-=RENEW_ENERGY
                self.life[seg.start+most_urgent]=acq.CHILD_LIFE
                self.renewals+=1; acted=True
            elif live:
                self.refusals+=1
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
                refusals=w.refusals,produced=w.produced,drained=w.drained)


def rating(order,rates,seeds=SCORING_SEEDS,ticks=TICKS):
    return float(np.mean([run(order,s,ticks,rates=rates)['sites'] for s in seeds]))


def noise_of_order(order,rates,sets=8,prefix=9400,ticks=TICKS):
    out=[rating(order,rates,tuple(range(prefix+50*k,prefix+50*(k+1))),ticks) for k in range(sets)]
    return float(np.std(out)),float(min(out)),float(max(out))


def climb(start,neighbourhood=asc.swaps,rates=RATES_A):
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


def hold(arm_name,seed,opt):
    start=tuple(int(x) for x in np.random.default_rng([seed,3701]).permutation(6))
    if arm_name in ('learner_both','no_release'):
        stored,_=search(RATES_A,start)
    else:
        stored=start
    if arm_name=='learner_both':
        r=reg.Register(); r.write(reg.lehmer(start)); stored,_=search(RATES_B,start)
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


def validity(production_period,drain,tick_s=300,seeds=(0,1)):
    """Scan helper: the endpoint's resolving power for a candidate economy."""
    global PRODUCTION_PERIOD,DRAIN
    old=(PRODUCTION_PERIOD,DRAIN)
    PRODUCTION_PERIOD,DRAIN=production_period,drain
    try:
        sample=list(itertools.permutations(range(6)))[::10]
        sc={o:rating(o,RATES_B,seeds=seeds,ticks=tick_s) for o in sample}
        best=max(sc,key=sc.get)
        spread=max(sc.values())-min(sc.values())
        sd,lo,hi=noise_of_order(best,RATES_B,sets=4,ticks=tick_s)
        return dict(spread=spread,sd=sd,mean=float(np.mean(list(sc.values()))),
                    ratio=(spread/sd if sd else float('inf')),production_period=production_period,
                    drain=drain)
    finally:
        PRODUCTION_PERIOD,DRAIN=old


if __name__=='__main__':
    print(__doc__)
    print('--- economy scan: which self-funded world resolves orders? ---')
    print(f'{"period":>7s} {"drain":>6s} {"mean sites":>11s} {"spread":>7s} {"noise sd":>9s} '
          f'{"ratio":>7s}')
    results=[]
    for period in (4,6,8):
        for drain in (1,2,3,4,5,6):
            v=validity(period,drain)
            results.append(v)
            print(f'{period:>7d} {drain:>6d} {v["mean"]:>11.2f} {v["spread"]:>7.2f} '
                  f'{v["sd"]:>9.2f} {v["ratio"]:>7.2f}')
    good=[v for v in results if v['ratio']>=10 and 3.0<v['mean']<20.0]
    print(f'\ncandidates (ratio >= 10, mean in the graded range): {len(good)}')
    for v in sorted(good,key=lambda v:-v['ratio'])[:5]:
        print(f"  period {v['production_period']} drain {v['drain']}: spread {v['spread']:.2f} "
              f"noise {v['sd']:.2f} ratio {v['ratio']:.2f} mean {v['mean']:.2f}")
    json.dump(results,open('/tmp/ac37_scan.json','w'),indent=2)
