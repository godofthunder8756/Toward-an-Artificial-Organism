"""AC30: acquisition -- the world defines a good order, a learner finds one, the register holds it.

Why the score must come from the world
--------------------------------------
AC13 was falsified because its headline saving did not replicate, and the deeper reason there was
that the world barely distinguished the arms. For an order to be *acquirable* the world must first
*rank* orders, with a margin large enough to find and to keep. So this module starts by measuring
the ranking, not by building a learner:

  * six regions, four sites each, every site's life ticking down;
  * the environment stresses regions at different rates, so each region periodically has a site near
    loss;
  * one action per tick, and it must be *one region's* maintenance (AC28's birth: 4 material + 2
    energy, child life 64, into an empty slot of that region);
  * score = sites retained over a run.

The world's ranking is then a fact to be measured: the best fixed order should prioritise the
most-stressed region, and the spread between best and worst is what any learner has to work with.

Then: a mutate-and-keep search over the 720 orders, scored by actually running the world, writing its
result into AC29's register -- and the reference question from AC29 §4 answered explicitly, because
majority-write repair cannot hold a multi-bit object on its own.
"""
import itertools
import json
import math
import numpy as np
import ac29_register as reg
import ac27_schedule as sched

REGIONS=6
SITES=4
SLOTS=REGIONS*SITES
CHILD_LIFE=64
BIRTH_MATERIAL=4
BIRTH_ENERGY=2
URGENT=16                      # a site this close to loss is urgent
RENEW_MATERIAL=3               # deliberately dearer than income, so renewals contend for budget
RENEW_ENERGY=1
INCOME_MATERIAL=1              # declared metabolic income: 1 material + 1 energy per tick
INCOME_ENERGY=1
BURST_PROBABILITY=0.05         # correlated stress: several regions at once
BURST_WIDTH=3
TICKS=800                      # enough for the ranking to be stable; keeps the 720-order sweep cheap
SEEDS=(0,1)


def stress_rates():
    """The environment's per-region urgency rate. Deliberately unequal, so a best order exists."""
    return (0.020,0.016,0.012,0.009,0.006,0.004)


class World:
    """Six regions of sites with an environment that stresses them at different rates."""

    def __init__(self,seed,rates=None):
        self.rng=np.random.default_rng([seed,3001])
        self.rates=rates if rates is not None else stress_rates()
        self.life=[CHILD_LIFE]*SLOTS
        self.energy=64; self.material=128
        self.lost=0; self.renewed=0

    def urgency(self):
        word=0
        for k in range(REGIONS):
            seg=self.life[k*SITES:(k+1)*SITES]
            if any(0<v<=URGENT for v in seg): word|=1<<k
        return word

    def environment_tick(self):
        """Stress the regions. Two sources, deliberately: a slow per-region drizzle and occasional
        BURSTS that hit several regions at once.

        The bursts exist because the first version of this world did not rank orders at all (spread
        1.5 sites of 24, stress-order ranking 457th of 720). The mechanism was that income exceeded
        the cost of a renewal, so the organism could renew every tick, and an unaddressed urgent site
        has 16 ticks of life -- two simultaneous urgencies were both comfortably handled and priority
        almost never mattered. Contention is what makes a priority order consequential, so the world
        has to supply it."""
        for k,rate in enumerate(self.rates):
            if self.rng.random()<rate:
                self._stress_one(k)
        if self.rng.random()<BURST_PROBABILITY:
            weights=np.array(self.rates); weights=weights/weights.sum()
            for k in self.rng.choice(REGIONS,size=BURST_WIDTH,replace=False,p=weights):
                self._stress_one(int(k))

    def _stress_one(self,k):
        seg=slice(k*SITES,(k+1)*SITES)
        occupied=[i for i in range(SITES) if self.life[seg.start+i]>0]
        if occupied:
            i=occupied[int(self.rng.integers(0,len(occupied)))]
            self.life[seg.start+i]=URGENT

    def tick(self,action):
        """A site at life 1 is lost; then the chosen region's most urgent LIVE site is renewed.

        Renewal is the frozen world's `renew` semantics (actions 3,4 there): the action addresses an
        *existing* site rather than only filling empty slots. My first version only filled empty
        slots, so an urgent site could never be saved and every region collapsed to zero within a
        few hundred ticks -- all 720 orders scored 0.00 and the world ranked nothing at all.

        Metabolic income (2 material + 1 energy per tick) is a declared simplification: it keeps the
        budget from being the binding constraint so that ORDERING is what the score measures. This is
        not a survival or autopoiesis claim and is not offered as one."""
        for i in range(SLOTS):
            if self.life[i]==1: self.life[i]=0; self.lost+=1
            elif self.life[i]>1: self.life[i]-=1
        self.material+=INCOME_MATERIAL; self.energy+=INCOME_ENERGY
        if action is not None:
            seg=slice(action*SITES,(action+1)*SITES)
            live=[i for i in range(SITES) if self.life[seg.start+i]>0]
            if live and self.material>=RENEW_MATERIAL and self.energy>=RENEW_ENERGY:
                most_urgent=min(live,key=lambda i:self.life[seg.start+i])
                self.material-=RENEW_MATERIAL; self.energy-=RENEW_ENERGY
                self.life[seg.start+most_urgent]=CHILD_LIFE
                self.renewed+=1
        self.environment_tick()


def run(order,seed,ticks=TICKS):
    w=World(seed)
    for _ in range(ticks):
        word=w.urgency()
        action=None
        for position in order:
            if word>>position&1: action=position; break
        w.tick(action)
    return sum(1 for v in w.life if v>0), w.lost


def score(order,seeds=SEEDS,ticks=TICKS):
    return float(np.mean([run(order,s,ticks)[0] for s in seeds]))


if __name__=='__main__':
    rows={}
    rates=stress_rates()
    print(f'{REGIONS} regions, rates {rates}\n')

    print('--- does the world rank orders at all? all 720, 3 seeds, 1500 ticks ---')
    steps=0
    scores={}
    for order in itertools.permutations(range(REGIONS)):
        steps+=1
        scores[order]=score(order)
    ranked=sorted(scores.items(),key=lambda kv:-kv[1])
    print(f'  scored {steps} orders')
    print(f'  best  {ranked[0][0]} = {ranked[0][1]:.2f} sites retained')
    print(f'  worst {ranked[-1][0]} = {ranked[-1][1]:.2f}')
    print(f'  median {ranked[len(ranked)//2][1]:.2f}')
    print(f'  spread {ranked[0][1]-ranked[-1][1]:.2f} sites out of {SLOTS}')
    expected=tuple(sorted(range(REGIONS),key=lambda k:-rates[k]))
    print(f'  order by descending stress rate: {expected} -> {scores[expected]:.2f}')
    rank_of_expected=1+sum(1 for _,v in ranked if v>scores[expected])
    print(f'  that order ranks {rank_of_expected} of {steps}')
    rows['ranking']=dict(best=list(ranked[0][0]),best_score=ranked[0][1],
                         worst=list(ranked[-1][0]),worst_score=ranked[-1][1],
                         spread=ranked[0][1]-ranked[-1][1],
                         by_stress=list(expected),by_stress_score=scores[expected],
                         by_stress_rank=rank_of_expected)

    print('\n--- acquisition: mutate-and-keep over the 720 orders ---')
    learner=[]
    for seed in range(6):
        rng=np.random.default_rng([seed,3101])
        current=tuple(int(x) for x in rng.permutation(REGIONS)); best=score(current,seeds=(seed,))
        for _ in range(60):
            i,j=rng.integers(0,REGIONS,2)
            candidate=list(current); candidate[i],candidate[j]=candidate[j],candidate[i]
            candidate=tuple(candidate)
            s=score(candidate,seeds=(seed,))
            if s>=best: current,best=candidate,s
        learner.append((current,best))
    found=[o for o,_ in learner]
    best_found=ranked[0][1]
    print(f'  learners converged to {len(set(found))} distinct orders')
    # the honest comparison is against the BEST order found by the sweep, on the same 2-seed score
    print(f'  {"learner":>8s} {"2-seed score":>12s} {"gap to best ({:.2f})".format(best_found):>22s}'
          f' {"percentile among 720":>22s}')
    gaps=[]
    for i,o in enumerate(found):
        s=scores[o]
        percentile=100*sum(1 for _,v in ranked if v>s)/len(ranked)
        gaps.append(best_found-s)
        print(f'  {i:>8d} {s:>12.2f} {best_found-s:>22.2f} {percentile:>21.1f}%')
    print(f'  mean gap to best {np.mean(gaps):.2f} sites; worst {max(gaps):.2f}; '
          f'best-vs-worst spread in the world {ranked[0][1]-ranked[-1][1]:.2f}')
    print(f'  stress-ordered order scored {scores[expected]:.2f} (rank {rank_of_expected}) -- so the')
    print(f'  world\'s ranking is NOT the stress order; it must be found by evaluation, not reasoning')
    rows['learner']=dict(found=[list(o) for o in found],distinct=len(set(found)),
                         gaps=[float(g) for g in gaps],mean_gap=float(np.mean(gaps)),
                         worst_gap=float(max(gaps)),best_found=best_found,
                         spread=ranked[0][1]-ranked[-1][1])

    print('\n--- retention of the learned order: the reference question (AC29 §4) ---')
    target=found[0]
    code=reg.lehmer(target)
    variants=(('no_damage','no repair, no damage -- the ceiling'),
              ('damage_no_repair','damage only: what the redundancy alone buys'),
              ('damage_repair_1bit','damage + one bit repaired per tick (a tight budget)'),
              ('damage_repair_all','damage + every disagreeing bit repaired (the frozen write)'),
              ('damage_with_reference','damage + an external copy of the correct order (PROTECTED:'
                                       ' non-autonomous)'))
    for variant,label in variants:
        rng=np.random.default_rng(7)
        r=reg.Register(); r.write(code)
        reference=code if variant=='damage_with_reference' else None
        agree=0; intact=0; ticks=600
        for _ in range(ticks):
            if variant!='no_damage':
                r.damage(rng,1e-3)
                if reference is not None and r.read()!=target: r.write(reference)
                elif variant=='damage_repair_1bit': r.repair(1)
                elif variant=='damage_repair_all': r.repair(reg.BITS)
            if r.raw()==code: intact+=1
            agree+=reg.behavioural_agreement(r.read(),target,sched.all_pairs())
        print(f'  {label:70s} intact {intact/ticks:.3f}  agreement {agree/ticks:.3f}')
        rows[variant]=dict(intact=intact/ticks,agreement=agree/ticks,label=label)

    json.dump(rows,open('ac30_acquire_v1.json','w'),indent=2,default=float)
