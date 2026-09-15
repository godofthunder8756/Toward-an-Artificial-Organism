"""AC34 engineering: is survival a discriminating question in this world?

Why this is the prerequisite, again
-----------------------------------
AC30's world declares a metabolic income (1 material + 1 energy per tick) precisely so that the budget
never binds and the score measures ORDERING rather than maintenance. That makes it useless for a
survival claim, and it is why random-fallback survival has stayed untouched while acquisition and
re-acquisition were studied.

A survival endpoint needs the organism's own state to fund its maintenance, or survival is either
guaranteed by a trickle or impossible for everyone. So this module gives the world the feedback loop
the frozen line actually had (particles -> energy conversion): **energy income is produced by the
organism's own living sites**. Then more living sites means more income, which means more renewals can
be afforded. The question here is only whether that makes survival discriminating:

  * if every one of the 720 orders survives, the endpoint is trivial and a claim about it is vacuous;
  * if every order dies, the world is unlivable and the design is wrong;
  * if some survive and some die, survival is a real endpoint and a study can be built on it.

This is engineering: no protocol, no final seeds, no claim. The death criterion used here is declared
below and is provisional -- a real study must declare its own, before its seeds.
"""
import itertools
import json
import numpy as np
import ac30_acquire as acq

RATES=acq.stress_rates()          # regime A, so this is comparable to AC30/AC32's baseline world
TICKS=1500
SEEDS=(0,1,2)

# Declared, provisional death/viability criterion for this engineering measurement only.
# My first version conflated IDLING with STARVING (it counted ticks with nothing urgent to do as
# starvation, so deaths clustered at exactly the threshold) and left the economy so loose that no
# order could fail. Both are fixed here: a renewal is dear, funded by the organism's own living
# sites, and starvation means wanting to act and being unable to afford it.
ENERGY_PER_SITE=1                 # a site with this much life or more yields energy
PRODUCTION_PERIOD=8               # ...once every this many ticks
RENEW_ENERGY=20                   # a renewal costs this much -- enough that population loss compounds
RENEW_MATERIAL=0                  # material plays no part in this world (declared simplification)
STARVATION_TICKS=40               # ticks WANTING to renew and unable to afford it = dead
SITE_FLOOR=1                      # no living sites at all = dead


class World:
    """AC30's world with the declared income replaced by production from the organism's own sites."""

    def __init__(self,seed,rates=None):
        self.rng=np.random.default_rng([seed,3401])
        self.rates=rates if rates is not None else RATES
        self.life=[acq.CHILD_LIFE]*acq.SLOTS
        self.energy=64; self.material=32
        self.tick_count=0; self.starved=0; self.dead=False; self.dead_at=None
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

    def production_tick(self):
        """The feedback loop: living, healthy sites produce energy."""
        if self.tick_count%PRODUCTION_PERIOD: return
        productive=sum(1 for v in self.life if v>=ENERGY_PER_SITE)
        self.energy+=productive; self.produced+=productive

    def tick(self,action):
        self.tick_count+=1
        for i in range(acq.SLOTS):
            if self.life[i]==1: self.life[i]=0
            elif self.life[i]>1: self.life[i]-=1
        self.production_tick()
        affordable=self.energy>=RENEW_ENERGY
        acted=False
        if action is not None:
            seg=slice(action*acq.SITES,(action+1)*acq.SITES)
            live=[i for i in range(acq.SITES) if self.life[seg.start+i]>0]
            if live and affordable:
                most_urgent=min(live,key=lambda i:self.life[seg.start+i])
                self.energy-=RENEW_ENERGY
                self.life[seg.start+most_urgent]=acq.CHILD_LIFE
                self.renewals+=1
                acted=True
        # starvation is WANTING to act and being unable to afford it -- never mere idleness
        self.starved=self.starved+1 if (action is not None and not acted) else 0
        self.environment_tick()
        if sum(1 for v in self.life if v>0)<SITE_FLOOR or self.starved>=STARVATION_TICKS:
            self.dead=True
            if self.dead_at is None: self.dead_at=self.tick_count


def run(order,seed,ticks=TICKS):
    w=World(seed)
    for _ in range(ticks):
        if w.dead: break
        word=w.urgency(); action=None
        for position in order:
            if word>>position&1: action=position; break
        w.tick(action)
    return dict(order=order,seed=seed,dead=w.dead,dead_at=w.dead_at,
                sites=sum(1 for v in w.life if v>0),energy=w.energy,material=w.material,
                renewals=w.renewals)


if __name__=='__main__':
    rows=[]
    for order in itertools.permutations(range(6)):
        for seed in SEEDS:
            rows.append(run(order,seed))
    surv={}
    for r in rows:
        surv.setdefault(r['order'],[]).append(0 if r['dead'] else 1)
    always=sorted(o for o,v in surv.items() if all(v))
    never=sorted(o for o,v in surv.items() if not any(v))
    mixed=[o for o in surv if o not in always and o not in never]
    print(f'orders tested: {len(surv)} x {len(SEEDS)} seeds, {TICKS} ticks')
    print(f'  survive on every seed:  {len(always)}')
    print(f'  die on every seed:      {len(never)}')
    print(f'  mixed across seeds:     {len(mixed)}')
    deaths=[r['dead_at'] for r in rows if r['dead']]
    if deaths:
        print(f'  death times: min {min(deaths)} median {int(np.median(deaths))} max {max(deaths)}')
    final_sites=[r['sites'] for r in rows if not r['dead']]
    if final_sites:
        print(f'  surviving final sites: min {min(final_sites)} mean {np.mean(final_sites):.2f} '
              f'max {max(final_sites)}')
    discriminating=(0<len(always)<len(surv))
    print(f'\nsurvival is DISCRIMINATING in this world: {discriminating}')
    if always:
        print(f'  example survivors: {always[:3]}')
    if never:
        print(f'  example non-survivors: {never[:3]}')
    json.dump(dict(survivors=[list(o) for o in always],never=[list(o) for o in never],
                   mixed=[list(o) for o in mixed],discriminating=discriminating,
                   deaths=deaths),open('/tmp/ac34_survival_engineering.json','w'),indent=2)
