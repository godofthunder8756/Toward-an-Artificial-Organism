"""AC24: what the frozen developmental function IS, in effective bits.

Why this comes before the scaled step
-------------------------------------
The word "bank" has been doing three different jobs in this project, and the AC22/AC23 framing
blurred them:

  (a) **site groups**: `life[4*bank:4*bank+4]`, the birth targets. Groups 0,1,2 are core + two W
      regions; group 3 is never a birth target.
  (b) **trace banks**: `b.traces[bank]`, a 1024x7 replica store. Only bank 0 is used.
  (c) **rule positions in the controller**: the frozen program's four bank rules carry masks
      `4<<bank` = observation bits 2,3,4,5. These four positions are the AC11-onward "four routing
      classes", and the acquired object is their ORDER.

The "B banks" that AC20/AC21/AC22 grew is sense (c): the number of rule positions, hence the size
of the acquired object. But one of those positions -- mask 32, bit 5 -- conditions on an
observation bit that `ac9.observe` can never set. A rule that can never fire cannot contribute
behaviour, so permutations that differ only in WHERE THE DEAD RULE SITS are behaviourally
identical. That means the frozen world's developmental function is smaller than log2(4!) = 4.58,
and any scaled world that repeats the mistake would have part of its "broader" function vacuous.

So: measure effective bits directly, by counting distinct BEHAVIOURS over the reachable observation
set rather than by counting permutations. This is a measurement, not an argument.
"""
import itertools
import json
import numpy as np
import ac9
import ac5_program as prog
import ac4
from ac23_body import FROZEN_BITS


def reachable_observations(seed=1200,history=0,arm='block0',ticks=2048):
    """The observations a real frozen run actually visits. Behaviour must be compared on these,
    not on all 2^12 combinations: two permutations that differ only on an unreachable observation
    are not behaviourally distinct in this world."""
    seen=set()
    o=ac9.acquire(seed); mapping=(seed%2,(seed//2)%2); rng=np.random.default_rng([seed,1509])
    import ac9_memory as mem
    for t in range(ticks):
        core=(rng.random((126,7))<.0001).astype(np.uint8)
        noise=(rng.random(o.memory.bits.shape)<.0001).astype(np.uint8)
        directions=rng.integers(0,4,20,dtype=np.uint8); coin=bool(rng.random()<.5)
        activation=[history==r for r in range(2)] if t<512 else [True,True]
        blocked=int(arm[-1]) if t>=512 and arm.startswith('block') else None
        seen.add(ac9.observe(o))
        ac9.step(o,core,noise,directions,coin,mapping,activation,t<512 and arm!='no_growth',blocked)
    return sorted(seen)


def frozen_rules(priority):
    """The frozen program's rule list, exactly as `ac5_program` builds it (AC22 verified this
    reproduces the installed bits for all 24 permutations). `prog.program()` returns packed bits,
    not a rule list, which is why this is constructed here."""
    return ([(1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8)]
            +[(1,4<<bank,2+bank) for bank in priority])


def behaviour(priority,observations):
    """The controller's behaviour: for each reachable observation, which action it selects (or
    None when no rule matches and the blind fallback is used)."""
    rules=frozen_rules(priority)
    out=[]
    for obs in observations:
        chosen=None
        for enabled,mask,action in rules:
            if enabled and (obs&mask)==mask:
                chosen=action; break
        out.append(chosen)
    return tuple(out)


def live_positions(observations):
    """Which of the four rule positions can ever fire, given the reachable observations. The
    program's bank rules are masks 4<<bank for bank in 0..3."""
    live=[]
    for bank in range(4):
        mask=4<<bank
        live.append(any((obs&mask)==mask for obs in observations))
    return live


def co_occurrence(observations,live):
    """Do the live masks ever fire together? If they never co-occur, their relative ORDER cannot
    matter and even the one bit the live pair seems to carry would be dead."""
    masks=[4<<bank for bank,l in enumerate(live) if l]
    pairs=0
    for obs in observations:
        if all((obs&m)==m for m in masks): pairs+=1
    return masks,pairs


if __name__=='__main__':
    overall={}
    for history in (0,1):
        obs=reachable_observations(history=history)
        live=live_positions(obs)
        masks,pairs=co_occurrence(obs,live)
        classes={}
        for priority in itertools.permutations(range(4)):
            classes.setdefault(behaviour(priority,obs),[]).append(priority)
        sizes=sorted(len(v) for v in classes.values())
        print(f'--- history {history} ---')
        print(f'  reachable observations: {len(obs)};  bit 5 set in: '
              f'{sum(1 for o in obs if (o>>5)&1)}')
        print(f'  live rule positions of the four: {live}  -> {sum(live)} live, '
              f'{4-sum(live)} structurally dead')
        print(f'  live masks: {[bin(m) for m in masks]};  observations where they co-occur: '
              f'{pairs}')
        print(f'  permutations 24 -> distinct behaviours {len(classes)} (class sizes {sizes})')
        print(f'  nominal   log2(24)     = {np.log2(24):.2f} bits')
        print(f'  EFFECTIVE log2({len(classes)})      = {np.log2(len(classes)):.2f} bits')
        overall[history]=dict(observations=len(obs),live=live,co_occurrences=pairs,
                              behaviours=len(classes),effective_bits=float(np.log2(len(classes))))
    import math
    print('--- what the scaled world must avoid ---')
    print(f'  6 positions all live:               log2(6!)    = '
          f'{math.log2(math.factorial(6)):.2f} bits')
    print(f'  6 positions, one structurally dead: log2(6!/6)  = '
          f'{math.log2(math.factorial(6)/6):.2f} bits')
    print(f'  6 positions, four dead (2 live):    log2(2)     = '
          f'{math.log2(2):.2f} bits  <- the frozen world\'s situation, scaled up')
    open('ac24_functional_v1.json','w').write(json.dumps(overall,indent=2))
