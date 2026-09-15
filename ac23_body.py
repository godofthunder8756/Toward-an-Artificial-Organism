"""AC23: the scaled body layer — banks, probes and the observation word, as data.

Where this sits
---------------
`AC22_WORLD_v1.md` built the scaled world's declarative layer at C = 6 constituents / B = 6 banks.
This builds the **body** it needs and proves the body layer reduces to the frozen one. It does
not build the step: no reactions, no accounting, no simulation. That is the next increment.

The frozen body, read rather than assumed
-----------------------------------------
`ac4.acquire` builds `life = [32,48,64,0]*4 + [64,96,128,0]`: **4 parent sites per bank** for 4
banks (indices 0-15) then **4 particle slots** (16-19). `available` slices `a[4*bank:4*bank+4]`
per bank and the step reads particles as `a[16:]`, so the frozen 16 is exactly `4 * banks` and the
layout generalizes without a shift: with B banks the bank sites are `0..4B-1` and particles start
at `4B`.

The observation word, read rather than assumed
----------------------------------------------
`ac9.observe` is NOT the same function as `ac4.observe`, and I had been treating them as one. It
produces eight meaningful bits plus one that is **never set**:

    bit 0  fuel <= 8
    bit 1  material <= 64
    bit 2  the PROGRAM BANK's disagreement: min(ones, 7-ones).sum() >= 4 over traces[0,:126]
    bit 3  memory urgency, region 0     (a slot near expiry, or a slot disagreeing with its decode)
    bit 4  memory urgency, region 1
    bit 5  NEVER SET                    <- which is why AC12's mask-32 rule is permanently dead
    bit 6  W low: core group < 2 sites, or a region with demand below 3 sites
    bit 7  particles < 2
    bit 8  boundary min <= 64

My AC22 note called bits 2-5 "per-bank disagreement" — that is `ac4.observe`'s convention, not
`ac9`'s. The frozen *program* does use masks `4<<bank` (bits 2-5) for its four bank rules, which is
why AC22's reducibility check still passed: the masks match even though the bit semantics I had
written down were wrong. This module carries the semantics as data, taken from `ac9.observe`.

Scale-up keeps the frozen positions and adds above them: bit 9 for the added constituent, bits
10-11 for the added banks.
"""
from dataclasses import dataclass
import hashlib
import json
import numpy as np
import ac4
import ac5
import ac4_transport as tr
from ac1 import decode

BANKS=4
PARTICLES=4
BANK_SITES=4
CORE_BANK=0
REGION_BANKS=(1,2)
OBS_BITS=12

# quantity -> observation bit, the frozen positions preserved and the additions above bit 8
FROZEN_QUANTITIES=('fuel','material','program_disagreement','urgency0','urgency1','W','particles',
                   'boundary')
FROZEN_BITS=(0,1,2,3,4,6,7,8)
SCALED_EXTRA_QUANTITIES=('added_constituent','bank4','bank5')
SCALED_EXTRA_BITS=(9,10,11)


@dataclass(slots=True)
class Body:
    traces: np.ndarray
    life: np.ndarray
    pos: np.ndarray
    boundary: np.ndarray
    energy: int = 64
    material: int = 128
    fuel: int = 32
    dead: bool = False

    def digest(self):
        raw=b''.join(x.tobytes() for x in (self.traces,self.life,self.pos,self.boundary))
        return hashlib.sha256(raw+json.dumps([self.energy,self.material,self.fuel,
                                               self.dead]).encode()).hexdigest()


def available(b):
    """The frozen formula needs no change: it only ever used the body's own shapes."""
    return (b.life>0) & tr.inside(b.pos)


def banks_of(b):
    return int(b.traces.shape[0])


def particles_offset(b):
    return BANK_SITES*banks_of(b)


def inventory(b):
    return (b.energy,b.material,b.fuel,int((b.life>0).sum()),int((b.boundary>0).sum()))


def acquire(seed,banks=BANKS,particles=PARTICLES):
    """The frozen acquisition, and an explicit refusal beyond it.

    At the frozen counts this returns `ac5.acquire(seed)` unchanged, so the body layer IS the
    frozen body and the observation check has something real to compare against. The scaled
    acquisition -- six banks, their parent sites, a widened particle array -- is the next increment
    (`ac24`). It raises rather than quietly returning a four-bank body, because a silent fallback
    here would make every scaled measurement meaningless."""
    if (banks,particles)!=(BANKS,PARTICLES):
        raise NotImplementedError(
            f'scaled acquisition (banks={banks}, particles={particles}) is not built yet; this '
            f'module supplies the layout, the probes and the observation word')
    b,_,_=ac5.acquire(seed)
    return b


# --- the frozen quantities, verbatim from ac9.observe ----------------------------------------
# Each takes the organism (body plus memory), because the frozen observation reads both.

def q_fuel(o):
    return int(o.body.fuel<=8)


def q_material(o):
    return int(o.body.material<=64)


def q_program_disagreement(o):
    ones=o.body.traces[0,:126].sum(axis=1)
    return int(np.minimum(ones,7-ones).sum()>=4)


def q_urgency(o,region):
    life=o.memory.life[region]; bits=o.memory.bits[region]
    urgent=bool(np.any((life>0)&(life<=16)))
    for slot in range(2):
        v=o.memory.decoded_slot(region,slot)
        if v is not None:
            urgent|=bool(np.any((life[slot]>0)&(bits[slot]!=np.array(v)[:,None])))
    return int(urgent)


def q_urgency0(o):
    return q_urgency(o,0)


def q_urgency1(o):
    return q_urgency(o,1)


def q_W(o):
    a=available(o.body); demand=o.memory.demand()
    low=int(a[:4].sum())<2
    for region in range(2):
        low|=bool(demand[region]>0 and a[4*(region+1):4*(region+2)].sum()<3)
    return int(low)


def q_particles(o):
    b=o.body
    return int(available(b)[particles_offset(b):].sum()<2)


def q_boundary(o):
    return int(o.body.boundary.min()<=64)


# --- the added quantities, DECLARED (no frozen analogue) -------------------------------------

def q_added_constituent(o):
    """The added constituent: the reserve of bank-parent sites outside the core group and the two
    W regions is short. DECLARED, not derived -- it is a placeholder with a stated meaning, and it
    is the one quantity whose formula the world build may change once the added constituent's
    chemistry exists in the step."""
    b=o.body; a=available(b)
    extra=[bank for bank in range(banks_of(b)) if bank not in (CORE_BANK,)+REGION_BANKS]
    if not extra: return 0
    total=sum(int(a[4*bank:4*(bank+1)].sum()) for bank in extra)
    return int(total<2*len(extra))


def q_bank(o,bank):
    """Disagreement of an *extra* bank's rule row. Only meaningful for banks >= 4, whose rows are
    additional repair targets (the frozen world repairs banks 0-3 through the program-disagreement
    and urgency bits, not through per-bank bits)."""
    ones=o.body.traces[bank,:126].sum(axis=1)
    return int(np.minimum(ones,7-ones).sum()>=4)


FROZEN_PROBES={'fuel':q_fuel,'material':q_material,'program_disagreement':q_program_disagreement,
               'urgency0':q_urgency0,'urgency1':q_urgency1,'W':q_W,'particles':q_particles,
               'boundary':q_boundary}


def observe(o,frozen_only=True):
    """The observation word at the frozen width (default), or the scaled 12-bit word.

    At the frozen width this must equal `ac9.observe` exactly -- checked against the real function
    on random states in the tests and in __main__, not asserted."""
    word=0
    for name,bit in zip(FROZEN_QUANTITIES,FROZEN_BITS):
        word|=int(FROZEN_PROBES[name](o))<<bit
    if not frozen_only:
        word|=int(q_added_constituent(o))<<SCALED_EXTRA_BITS[0]
        for bank,bit in ((4,SCALED_EXTRA_BITS[1]),(5,SCALED_EXTRA_BITS[2])):
            if bank<banks_of(o.body): word|=int(q_bank(o,bank))<<bit
    return word


def _randomize(o,rng):
    o.body.traces=rng.integers(0,2,o.body.traces.shape,dtype=np.uint8)
    o.body.life=rng.integers(0,80,o.body.life.shape,dtype=np.int16)
    o.body.boundary=rng.integers(0,260,o.body.boundary.shape,dtype=np.int16)
    o.body.fuel=int(rng.integers(0,64)); o.body.material=int(rng.integers(0,256))
    for region in range(2):
        for slot in range(2):
            o.memory.life[region,slot]=64 if rng.random()<0.5 else 0
    return o


if __name__=='__main__':
    import ac9
    rng=np.random.default_rng(0)
    checked=mismatches=0
    for seed in (0,1):
        o=ac9.acquire(seed)
        for _ in range(300):
            _randomize(o,rng)
            mine=observe(o); theirs=ac9.observe(o); checked+=1
            if mine!=theirs:
                mismatches+=1
                if mismatches<4: print(f'  mismatch: mine {bin(mine)} frozen {bin(theirs)}')
    print(f"observation-word reducibility: {checked} randomized states, {mismatches} mismatches "
          f"vs ac9.observe")
    print(f"frozen quantities at bits {FROZEN_BITS}; bit 5 is never set (mask-32 is dead by "
          f"construction); additions at bits {SCALED_EXTRA_BITS}")
