"""AC36: insufficiency -- population retained when maintenance is unaffordable in full.

What AC30 and AC35 established
------------------------------
AC30's world declared an income generous enough that the budget never bound, and its spread across
orders was 5.00 sites of 24 -- because the endpoint measured pure ordering quality.
AC35 removed the declared income and had the organism's own sites produce energy; the spread
collapsed to 1.00 site against 0.30 of noise, because production scales with the living population and
that negative feedback equalizes every order toward carrying capacity.

This world does the third thing: **a declared income that is deliberately insufficient.** Energy
arrives at a fixed rate independent of the organism's state, and a renewal costs more than one tick of
it, so the organism can never maintain everything and must spend what it has on ONE region per renewal.
No population-scaled feedback, so nothing equalizes; a finite, non-scalable budget, so the order has to
choose.

Claim to be tested: after the environment's stress regime changes so a different order is best, an
organism that can release its stored order and search again retains more population than one that
cannot. Gate shape: separation of minima, as in AC18/AC32/AC33.

This module holds the study machinery AND the prerequisite measurement. No protocol exists until the
prerequisite passes; see __main__.
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

# The economy: fixed income, dear renewals, stress heavy enough that demand meets capacity.
INCOME_ENERGY=1                    # energy per tick, independent of the organism's state
RENEW_ENERGY=5                     # one renewal costs five ticks of income
STRESS_MULTIPLIER=3                # urgency arrives three times as often as in AC30's regime
BURST_PROBABILITY=0.03             # correlated stress: several regions at once
BURST_WIDTH=3
STARVATION_TICKS=60
TICKS=600
RATES_A=tuple(r*STRESS_MULTIPLIER for r in acq.stress_rates())
RATES_B=tuple(reversed(RATES_A))
REGIMES={'A':RATES_A,'B':RATES_B}
SCORING_SEEDS=ac32.SCORING_SEEDS
ARMS=ac32.ARMS
SOURCES=[]                         # filled by the protocol; the runner refuses to run without one


class World:
    def __init__(self,seed,rates=None):
        self.rng=np.random.default_rng([seed,3601])
        self.rates=rates if rates is not None else RATES_A
        self.life=[acq.CHILD_LIFE]*acq.SLOTS
        self.energy=48
        self.tick_count=0; self.starved=0; self.dead=False
        self.renewals=0; self.afforded_refusals=0

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
        if self.rng.random()<BURST_PROBABILITY:
            weights=np.array(self.rates); weights=weights/weights.sum()
            for k in self.rng.choice(acq.REGIONS,size=BURST_WIDTH,replace=False,p=weights):
                self._stress_one(int(k))

    def tick(self,action):
        self.tick_count+=1
        for i in range(acq.SLOTS):
            if self.life[i]==1: self.life[i]=0
            elif self.life[i]>1: self.life[i]-=1
        self.energy+=INCOME_ENERGY
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
                self.afforded_refusals+=1        # wanted to act, could not afford it
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
                refusals=w.afforded_refusals)


def rating(order,rates,seeds=SCORING_SEEDS,ticks=TICKS):
    return float(np.mean([run(order,s,ticks,rates=rates)['sites'] for s in seeds]))


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


def noise_of_order(order,rates,sets=8,prefix=9300,ticks=TICKS):
    out=[rating(order,rates,tuple(range(prefix+50*k,prefix+50*(k+1))),ticks) for k in range(sets)]
    return float(np.std(out)),float(min(out)),float(max(out))


def hold(arm_name,seed,opt):
    start=tuple(int(x) for x in np.random.default_rng([seed,3601]).permutation(6))
    if arm_name in ('learner_both','no_release'):
        stored,_=search(RATES_A,start)
    else:
        stored=start
    if arm_name=='learner_both':
        r=reg.Register(); r.write(reg.lehmer(start))
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


# Declared optima: the best of a full 720-order sweep on the paired scoring seeds (engineering,
# recorded in AC36_PROTOCOL_v1.md). Selection on a smaller seed set picks a different order -- the
# learner's engineering value exceeded the 3-seed "optimum" -- so the full sweep was used.
DECLARED_OPTIMA={'A':((4,5,1,2,0,3),6.92),'B':((1,0,2,3,4,5),6.83)}

FINAL_SEEDS=tuple(range(3500,3512))          # declared in AC36_PROTOCOL_v1.md
BAR=6.45                                     # declared in AC36_PROTOCOL_v1.md

# The protocol declares exactly this set; preflight enforces the equality (AC32's lesson, AC33's fix).
SOURCES=['ac36_survival.py','ac33_search.py','ac32_reacquire.py','ac30_acquire.py',
         'ac29_register.py','AC36_PROTOCOL_v1.md']


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


def preflight(protocol='AC36_PROTOCOL_v1.md'):
    """Parse the protocol's declared source list and require it to equal what this runner hashes."""
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


def main(seeds=FINAL_SEEDS,root='ac36_results_v1'):
    preflight()
    outdir=Path(root); outdir.mkdir(exist_ok=False)
    hashes={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES}
    (outdir/'pre_run_snapshot.json').write_text(json.dumps(hashes,indent=2))
    rows=[]
    with (outdir/'rows.jsonl').open('x') as f:
        for seed in seeds:
            row=individual(seed,DECLARED_OPTIMA)
            rows.append(row); f.write(json.dumps(row)+'\n'); f.flush()
            print(json.dumps(dict(seed=seed,learner=row['learner_both']['post'],
                                  no_release=row['no_release']['post'],
                                  no_search=row['no_search']['post'],
                                  oracle_b=row['oracle_b']['post'])),flush=True)
    g=gates(rows)
    g['G7_determinism']=all(individual(s,DECLARED_OPTIMA)==r for s,r in zip(seeds[:2],rows[:2]))
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
        print('Run the declared finals with: .venv/bin/python -B ac36_survival.py finals')
        print('Protocol: AC36_PROTOCOL_v1.md (final seeds 3500-3511, BAR=6.45)')
