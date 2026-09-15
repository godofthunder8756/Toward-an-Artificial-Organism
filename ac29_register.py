"""AC29: storing a six-position order -- the register, and how its integrity scales.

The question
-----------
AC14 asked whether the frozen organism's own decision state is a maintained constraint, and found it
"structurally present but arithmetically inert": the state was 7-fold replicated, damage was
self-reversing XOR, and a read needs a 4-of-7 majority, so a single flip could never change what the
organism read. Integrity was never actually at risk.

AC28 built a world whose acquired object is a **six-position order** -- 720 values, 9.49 bits. That is
a different object from the frozen one-bit route, and this module asks whether per-bit replication of
7 preserves it the way it preserved the one-bit one. It does not, for two arithmetic reasons:

  * a k-bit object has k chances to break instead of one, so at a fixed per-replica damage rate the
    time to first corruption falls roughly k-fold -- a weakest-link effect;
  * 10 bits represent 1024 values while only 720 are orders, so ~29.7% of reachable patterns are not
    orders at all. Damage does not merely reorder the rule positions; it can leave the space of
    orders entirely.

Method
------
Persistent damage has a closed form, so the retention curves here are EXACT rather than sampled. A
replica overwritten with a fresh random bit at rate `r` equals its original value at tick t with
probability `(1 + (1-r)^t)/2`; the stored bit's majority is wrong iff at least four of the seven
replicas differ, i.e. a binomial tail with `q = (1 - (1-r)^t)/2`. Bits are independent, so the
distribution over all 1024 codes -- and hence any statistic of the register -- follows directly. The
repair case is a dynamic process, so it is simulated, with a small explicit trial count.

The endpoint measured is BEHAVIOURAL: the fraction of demand words answered as the target order
would. Bit-level intactness is reported too, because the gap between the two is exactly the mistake
AC14 exposed -- a corrupted store need not answer incorrectly.
"""
import itertools
import json
import math
import numpy as np
import ac27_schedule as sched
import ac25_confront as cf

N=6
VALID=math.factorial(N)                  # 720
BITS=math.ceil(math.log2(VALID))         # 10
REPLICAS=7
MAJORITY=REPLICAS//2+1                   # 4


def lehmer(order):
    items=list(range(N)); code=0
    for position,item in enumerate(order):
        index=items.index(item); code=code*(N-position)+index; items.pop(index)
    return code


def unlehmer(code):
    """Inverse of `lehmer`; None when the code is not an order (codes >= 720).

    Digits are EXTRACTED from the least-significant end (radices 1,2,3,4,5,6 for positions
    5,4,3,2,1,0) but APPLIED left to right, consuming items as each is chosen. My first version
    conflated those two orders and popped a chosen item too early, which the round-trip test over
    all 720 permutations caught immediately."""
    if not 0<=code<VALID: return None
    digits=[0]*N
    for position in range(N-1,-1,-1):
        radix=N-position
        digits[position]=code%radix; code//=radix
    items=list(range(N))
    return tuple(items.pop(digits[position]) for position in range(N))


def p_bit_wrong(rate,t):
    """Exact: the stored bit's majority differs from its original value."""
    q=(1-(1-rate)**t)/2
    return sum(math.comb(REPLICAS,j)*q**j*(1-q)**(REPLICAS-j)
               for j in range(MAJORITY,REPLICAS+1))


def code_distribution(stored,rate,t):
    """Exact distribution over 10-bit codes at tick t."""
    p=p_bit_wrong(rate,t); bits=[(stored>>k)&1 for k in range(BITS)]
    out={}
    for code in range(1<<BITS):
        prob=1.0
        for k in range(BITS):
            prob*= (1-p) if ((code>>k)&1)==bits[k] else p
        if prob>1e-12: out[code]=prob
    return out


def behavioural_agreement(order,target,words):
    if order is None: return 0.0
    codes=cf.unique_codes(N); actions=list(range(N))
    hit=0
    for word in words:
        if cf.behaviour(order,codes,actions,[word])==cf.behaviour(target,codes,actions,[word]):
            hit+=1
    return hit/len(words)


class Register:
    """For the simulated repair case: a replica-encoded store for one six-position order."""

    def __init__(self,replicas=REPLICAS):
        self.bits=np.zeros((BITS,replicas),dtype=np.uint8); self.replicas=replicas

    def write(self,code):
        self.bits[:]=np.array([(code>>k)&1 for k in range(BITS)],dtype=np.uint8)[:,None]

    def raw(self):
        return sum(int(self.bits[k].sum()>=self.replicas//2+1)<<k for k in range(BITS))

    def read(self):
        return unlehmer(self.raw())

    def damage(self,rng,rate):
        hits=rng.random(self.bits.shape)<rate
        self.bits[hits]=rng.integers(0,2,int(hits.sum()),dtype=np.uint8)

    def repair(self,budget):
        fixed=0
        for k in range(BITS):
            if fixed>=budget: break
            ones=int(self.bits[k].sum())
            if ones in (0,self.replicas): continue
            majority=1 if ones>=MAJORITY else 0
            self.bits[k][self.bits[k]!=majority]=majority
            fixed+=1
        return fixed


if __name__=='__main__':
    target=tuple(range(N)); stored=lehmer(target)
    words=sched.all_pairs()+sched.all_singletons()+[0]
    rows={}

    print(f'six-position order: {VALID} values, {math.log2(VALID):.2f} bits, stored in {BITS} bits\n')

    print('--- the coding weakness ---')
    valid_codes=sum(1 for c in range(1<<BITS) if unlehmer(c) is not None)
    print(f'  codes in {1<<BITS}: {valid_codes} are orders ({valid_codes/(1<<BITS):.1%})')
    print(f'  a uniformly random 10-bit pattern is a well-formed order {valid_codes/(1<<BITS):.1%}'
          f' of the time')
    rows['coding']=dict(space=1<<BITS,valid=valid_codes,fraction=valid_codes/(1<<BITS))

    print('\n--- weakest link: exact time to a 1% chance of an error, rate 1e-4 per replica/tick ---')
    rate=1e-4
    def ticks_to_threshold(bit_count,threshold):
        """Time for the k-bit object to have probability `threshold` of being wrong somewhere."""
        for t in range(1,4000000):
            p=p_bit_wrong(rate,t)
            if 1-(1-p)**bit_count>=threshold: return t
        return None
    t1=ticks_to_threshold(1,0.01); t10=ticks_to_threshold(BITS,0.01)
    print(f'  1-bit object (the frozen route): 1% chance of an error by tick {t1}')
    print(f'  {BITS}-bit object (the order):        1% chance of an error by tick {t10}')
    print(f'  ratio {t1/t10:.2f}x   vs the naive weakest-link expectation of {BITS}x')
    print(f'  the majority-of-7 failure is a FOURTH-power process in time, so k bits cost only')
    print(f'  k^(1/4) in time rather than k: {BITS}**0.25 = {BITS**0.25:.2f}')
    sat1=ticks_to_threshold(1,0.4999)
    print(f'  note also that a 1-bit object saturates at p=0.5 (full replica randomisation) by tick')
    print(f'  {sat1}, which is why a "half-chance" metric would mislead: 0.5 is its maximum,')
    print(f'  not a comparable point on the curve.')
    rows['weakest_link']=dict(one_bit_one_percent=t1,ten_bit_one_percent=t10,ratio=t1/t10,
                              naive_expectation=BITS,law=f'k^(1/4) = {BITS**0.25:.2f}',
                              one_bit_saturation=sat1)

    print('\n--- exact retention and behaviour, no repair (rate 1e-4) ---')
    print(f'{"tick":>7s} {"P(intact order)":>16s} {"P(valid code)":>14s} {"behavioural agreement":>22s}')
    for t in (100,500,1000,2000,5000,20000):
        dist=code_distribution(stored,rate,t)
        p_intact=dist.get(stored,0.0)
        p_valid=sum(p for c,p in dist.items() if unlehmer(c) is not None)
        agree=sum(p*behavioural_agreement(unlehmer(c),target,words) for c,p in dist.items())
        print(f'  {t:>5d} {p_intact:>16.4f} {p_valid:>14.4f} {agree:>22.4f}')
        rows[f'tick={t}']=dict(intact=p_intact,valid=p_valid,agreement=agree)

    print('\n--- with repair (simulated; 20 trials x 600 ticks) ---')
    print(f'{"damage/tick":>11s} {"repair/tick":>11s} {"behavioural agreement":>22s} {"intact":>10s}')
    for rate_ in (1e-4,1e-3):
        for budget in (0,1,4):
            agrees=[]; intacts=[]
            for trial in range(20):
                rng=np.random.default_rng([3000+trial,int(rate_*1e6),budget])
                reg=Register(); reg.write(stored)
                hits=0; intact=0
                for tick in range(600):
                    reg.damage(rng,rate_)
                    if budget: reg.repair(budget)
                    if reg.raw()==stored: intact+=1
                    hits+=behavioural_agreement(reg.read(),target,words)
                agrees.append(hits/600); intacts.append(intact/600)
            print(f'  {rate_:>9.0e} {budget:>11d} {np.mean(agrees):>22.3f} {np.mean(intacts):>10.3f}')
            rows[f'sim rate={rate_},repair={budget}']=dict(agreement=float(np.mean(agrees)),
                                                           intact=float(np.mean(intacts)))
    json.dump(rows,open('ac29_register_v1.json','w'),indent=2,default=float)
