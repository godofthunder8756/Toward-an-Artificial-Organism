"""AC28: six-region maintenance chemistry -- signals derived from body state, with conservation.

What the scaled world needs, now that the accounting is clear
-------------------------------------------------------------
AC24/AC25/AC26/AC27 established that the controller's order structure is real only when six
independently varying signals are presented pairwise. AC24 also showed the frozen world fails this
not for want of signals -- `ac9.observe` produces eight -- but because exactly one W region is
active per individual, and because observation bit 5 is never set, leaving two of four rule
positions structurally mute.

So what the scaled world needs is not new kinds of signal. It needs **six independently varying
maintenance needs of one kind**: six W regions, each a group of four parent sites whose occupancy
can drop toward expiry on its own schedule. The rule positions then condition one per region, and
their order is the acquired object -- 720 orders, 9.49 bits, when the regions can be confronted
pairwise.

This module builds that chemistry. The signals are computed from body state (not synthetic bit
words), the actions are real births with the frozen costs, and conservation is asserted every step
with the frozen identity's form.

What it reuses, and what it changes
-----------------------------------
Reused verbatim: `ac4.pay` (cost accounting), `ac4.empty_event` (ledger keys), the birth cost of
4 material + 2 energy per site with child life 64, the expiry rule (a site at life 1 is lost), and
the balance identity's shape.

Changed, deliberately and declared: the frozen action 6 births into *all* demanding groups at once,
whereas here each region has its own maintenance action. That is the refinement the six distinct
rule positions require, and it means this chemistry is a PARALLEL of the frozen one rather than a
reducible special case -- stated plainly rather than dressed up as reducibility.
"""
from dataclasses import dataclass
import json
import numpy as np
import ac4
import ac25_confront as cf

REGIONS=6
SITES=4
SLOTS=REGIONS*SITES
URGENCY_WINDOW=16
CHILD_LIFE=64
BIRTH_MATERIAL=4
BIRTH_ENERGY=2
REGION_ACTIONS=tuple(range(10,10+REGIONS))     # 10..15: distinct from the frozen 0..9


@dataclass(slots=True)
class RegionBody:
    life: np.ndarray
    pos: np.ndarray
    boundary: np.ndarray
    traces: np.ndarray              # the frozen chemistry's program bank; unused by region rules
    energy: int=64
    material: int=128
    fuel: int=32                    # carried so the frozen actions remain usable
    dead: bool=False

    def digest(self):
        raw=b''.join(x.tobytes() for x in (self.traces,self.life,self.pos,self.boundary))
        return f'{hash(raw)}:{self.energy}:{self.material}:{self.fuel}:{self.dead}'


def acquire(seed):
    rng=np.random.default_rng([seed,2801])
    life=np.tile(np.array([32,48,64,0],dtype=np.int16),REGIONS)
    pos=rng.integers(-2,3,(SLOTS,2),dtype=np.int16)
    boundary=np.arange(128,128+6*SLOTS,6,dtype=np.int16)[:SLOTS]
    traces=np.zeros((1,1024,7),dtype=np.uint8)
    return RegionBody(life,pos,boundary,traces)


def region_sites(b,region):
    return b.life[region*SITES:(region+1)*SITES]


def urgency(b,region,window=URGENCY_WINDOW):
    """The region's need signal: a site is near expiry. Zero-expiry sites are not 'urgent' -- a dead
    region is not a need, exactly as in the frozen urgency rule."""
    seg=region_sites(b,region)
    return int(np.any((seg>0)&(seg<=window)))


def signal(b):
    """The six-bit demand word, computed from body state."""
    word=0
    for k in range(REGIONS): word|=urgency(b,k)<<k
    return word


def birth_region(b,region,e):
    """One site born into `region` from a parent already there, at the frozen cost."""
    seg=region_sites(b,region)
    parents=np.flatnonzero(seg>0); empty=np.flatnonzero(seg==0)
    if not len(parents) or not len(empty): return False
    if not ac4.pay(b,e,BIRTH_MATERIAL,BIRTH_ENERGY): return False
    parent=region*SITES+int(parents[0]); child=region*SITES+int(empty[0])
    b.pos[child]=b.pos[parent]; b.life[child]=CHILD_LIFE
    e['region_births']+=1
    return True


def fresh_event():
    e=ac4.empty_event(); e['region_births']=0
    return e


def react(b,action,e):
    """Dispatch: region actions are this module's; everything else is the frozen chemistry."""
    action=int(action)
    if action in REGION_ACTIONS: return birth_region(b,action-REGION_ACTIONS[0],e)
    return ac4.react(b,action,'self',e)


def step(b,order,signal_word=None):
    """One tick: expiry, death check, one action chosen by the rule ORDER, conservation check.

    `order` is a permutation of the six rule positions -- the acquired object. A position k holds the
    rule conditioned on region k and acts on region k, so the first position whose region is urgent
    wins. `signal_word` overrides the body-derived demand (used only by the verification harness,
    which imposes the AC27 schedule)."""
    e=fresh_event()
    if b.dead: return e,None
    before_sites=int((b.life>0).sum()); before_E=b.energy; before_M=b.material
    e['particle_expiry']=int((b.life==1).sum()); b.life[b.life>0]-=1
    action=None
    if b.energy<1: b.dead=True
    else:
        word=signal(b) if signal_word is None else int(signal_word)
        for position in order:
            if word>>position&1:
                action=REGION_ACTIONS[position]; break
        b.energy-=1; e['spent_e']+=1; e['active']=1
        if action is not None: react(b,action,e)
    # conservation, in the frozen identity's shape
    assert int((b.life>0).sum())==before_sites+e['region_births']-e['particle_expiry']
    assert b.energy==before_E-e['spent_e']
    assert b.material==before_M-e['spent_m']
    assert e['spent_m']==BIRTH_MATERIAL*e['region_births']
    return e,action


def choose(order,word):
    for position in order:
        if word>>position&1: return position
    return None


if __name__=='__main__':
    print(f'{REGIONS} regions of {SITES} sites; actions {REGION_ACTIONS}\n')
    import ac27_schedule as sched

    b=acquire(0)
    print('--- signals come from body state ---')
    print(f'  initial signal word: {signal(b):06b}')
    # force one region urgent by draining its sites toward expiry
    b.life[2*SITES]=8
    print(f'  after draining one site in region 2: {signal(b):06b}  (bit 2 set)')

    print('\n--- one action, one region, with conservation ---')
    b2=acquire(1)
    b2.life[0]=48; b2.life[1]=0
    before_sites=int((b2.life>0).sum())
    e=ac4.empty_event(); e['region_births']=0
    ok=birth_region(b2,0,e)
    after_sites=int((b2.life>0).sum())
    print(f'  birth into region 0: {ok}; occupied 0-region sites now '
          f'{int((b2.life[:SITES]>0).sum())}; spent {e["spent_m"]} material, {e["spent_e"]} energy')
    print(f'  life-count identity: {after_sites} == {before_sites} + {e["region_births"]} '
          f'-> {after_sites==before_sites+e["region_births"]}')
    print(f'  material identity:   spent_m == 4 * births -> '
          f'{e["spent_m"]==BIRTH_MATERIAL*e["region_births"]}')

    print('\n--- the order structure over six region rules ---')
    codes=cf.unique_codes(REGIONS)
    classes=cf.classes(codes,sched.all_pairs())
    print(f'  exact-pair demand schedule -> {classes} behaviour classes '
          f'({np.log2(classes):.2f} bits)')
    print(f'  criterion met: {classes==720}')

    print('\n--- controls ---')
    one=[1<<k for k in range(REGIONS)]
    c1=cf.classes(codes,one)
    print(f'  one region urgent at a time (the frozen habit at its limit): {c1} class '
          f'({np.log2(c1):.2f} bits)  <- AC25 singletons-only result')
    # the frozen world's actual shape: a program-disagreement signal that co-occurs with a region
    frozen_codes=codes+[1<<6]
    frozen_obs=[1<<0,1<<0|1<<6]
    cf_=cf.classes(frozen_codes,frozen_obs)
    print(f'  frozen shape: a program signal co-occurring with one region: {cf_} classes '
          f'({np.log2(cf_):.2f} bits)  <- reproduces AC24/AC25/AC26\'s 1.00 bit')

    print('\n--- a driven run: schedule imposes the demand, chemistry answers ---')
    b3=acquire(2); order=tuple(range(REGIONS)); births=0; actions=[]
    for word in sched.pair_round_schedule(repeat=1):
        # harness imposes the demand word; the organism's own state must still support the action,
        # so land the imposed urgency in the body before acting
        for k in range(REGIONS):
            if word>>k&1:
                b3.life[k*SITES]=max(1,int(b3.life[k*SITES]))
                b3.life[k*SITES]=8
        e3,act=step(b3,order)
        births+=e3['region_births']; actions.append(act)
    print(f'  ticks {len(actions)}; births {births}; final occupied sites '
          f'{int((b3.life>0).sum())}; energy {b3.energy}; material {b3.material}')
    print(f'  distinct actions taken: {sorted(set(a for a in actions if a is not None))}')
    json.dump(dict(classes=classes,control_one_region=c1,births=births,
                   actions=[a for a in actions]),
              open('ac28_regions_v1.json','w'),indent=2)
