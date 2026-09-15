"""Feasibility for a broader developmental function than the present four routing classes.

Measured starting facts
-----------------------
`ac5_program.program(priority)` is five FIXED constituent rules plus four bank-repair rules
whose ORDER is the whole acquisition: a permutation of 4, i.e. 24 programs, log2(24) = 4.58 bits
of acquired structure. The 9-rule format reproduces the present demonstration exactly
(0 mismatches over all 24 permutations x 512 observations).

Two design lessons from the first attempt at a *broader* demonstration, both recorded here
because they cost a run each:

1. A "resource-contingent" priority is NOT contingent as a demonstration: the fixed constituent
   rules fire before the bank rules, so whenever the repair order could matter, no resource is
   low. A single permutation reproduced it 100%. The contingency has to live where the bank
   rules actually decide -- in the disagreement pattern itself.
2. The rule format is a supplied law with 9 slots in a 126-bit bank. Thirteen rules need 182
   bits, which does not fit (there is room elsewhere in traces[0] -- 1024 bits with 126 used --
   but widening the format is a declared change, not a free one).

So the demonstration used here is a **pair exception**: repair the disagreeing banks in a base
order, EXCEPT that when two declared banks disagree together, the later one goes first. That is
genuinely contingent, it is what a fixed permutation cannot express, and it costs one rule slot.
"""
import itertools
import numpy as np
import ac4
import ac5_program as prog
from ac1 import decode

BANK_BIT=[4,8,16,32]
FIXED=[(1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8)]


def demo_pair_exception(o,base_order,other_order=None):
    """The broader demand: constituent needs first, then the disagreeing banks in `base_order`
    -- except that when banks `EXC[0]` and `EXC[1]` disagree together, `EXC[1]` is repaired
    before `EXC[0]`, i.e. the order over that pair is reversed relative to the base order."""
    if o&1: return 0
    if o&2: return 1
    for bit,action in ((64,6),(128,7),(256,8)):
        if o&bit: return action
    exception=bool((o&BANK_BIT[EXC[0]]) and (o&BANK_BIT[EXC[1]]))
    order=list(base_order)
    if exception:
        order=[b for b in order if b!=EXC[1]]
        pos=order.index(EXC[0]) if EXC[0] in order else 0
        order.insert(pos,EXC[1])
    for bank in order:
        if o&BANK_BIT[bank]: return 2+bank
    return 9


EXC=(0,1)          # the declared pair whose order is reversed when both disagree
BASE=(0,1,2,3)


def evaluate(rules,observation):
    """The rule-list interpreter, independent of how many bits the rules occupy."""
    for enabled,mask,action in rules:
        if enabled and observation&mask==mask: return action
    return 9


def best_over_slots():
    """What the present 9-rule format can do: 5 fixed slots + 4 acquired slots, each either an
    order rule (single bank mask) or the pair-exception rule (two-bank mask)."""
    best=0; best_desc=''
    candidates=[]
    for b in range(4):
        candidates.append((BANK_BIT[b],2+b))
    candidates.append((BANK_BIT[EXC[0]]|BANK_BIT[EXC[1]],2+EXC[1]))
    # every arrangement of 4 slots drawn from the 5 candidate rules, in every order
    for combo in itertools.permutations(candidates,4):
        rules=FIXED+[(1,m,a) for m,a in combo]
        hit=sum(1 for o in range(512) if evaluate(rules,o)==demo_pair_exception(o,BASE))
        if hit>best: best=hit; best_desc=combo
    return best,best_desc


def demo_cycle(o,cycle):
    """A CYCLIC preference over the banks: each declared pair of banks, when both disagree,
    is repaired in the order the tour says. 0-before-1, 1-before-2, 2-before-0 cannot be
    satisfied by any single total order, which is what makes it the right test of the format."""
    if o&1: return 0
    if o&2: return 1
    for bit,action in ((64,6),(128,7),(256,8)):
        if o&bit: return action
    for a,b in cycle:                       # cycle = [(a,b), ...] meaning a is repaired first
        if (o&BANK_BIT[a]) and (o&BANK_BIT[b]): return 2+a
    disagree=[b for b in range(4) if o&BANK_BIT[b]]
    return 2+disagree[0] if disagree else 9


def cycle_search():
    """Best coverage of a cyclic preference by the present 4-slot format: candidates are the
    four single-bank rules and the six pair rules, arranged as any ordered 4-tuple."""
    cycle=[(0,1),(1,2),(2,0)]
    cands=[(BANK_BIT[b],2+b) for b in range(4)]
    cands+= [(BANK_BIT[a]|BANK_BIT[b],2+a) for a,b in itertools.combinations(range(4),2)]
    best=0; best_desc=None; best_perm=0
    for p in itertools.permutations(range(4)):
        rules=FIXED+[(1,BANK_BIT[b],2+b) for b in p]
        hit=sum(1 for o in range(512) if evaluate(rules,o)==demo_cycle(o,cycle))
        best_perm=max(best_perm,hit)
    for combo in itertools.permutations(cands,4):
        rules=FIXED+[(1,m,a) for m,a in combo]
        hit=sum(1 for o in range(512) if evaluate(rules,o)==demo_cycle(o,cycle))
        if hit>best: best=hit; best_desc=combo
    return best,best_desc,best_perm


def main():
    # the present demonstration is still exactly reproduced by the present format
    worst=0
    for p in itertools.permutations(range(4)):
        rules=FIXED+[(1,BANK_BIT[b],2+b) for b in p]
        worst=max(worst,sum(1 for o in range(512) if evaluate(rules,o)!=ac4.demonstration(o,list(p))))
    print(f"present demonstration, present format: max mismatches {worst}/512")

    best,desc=best_over_slots()
    print(f"pair-exception demonstration, present format (best of the 4-slot arrangements): "
          f"{best}/512 = {100*best/512:.1f}%")

    cb,cd,cp=cycle_search()
    print(f"CYCLIC demonstration, best of the 24 permutations:        "
          f"{cp}/512 = {100*cp/512:.1f}%")
    print(f"CYCLIC demonstration, best 4-slot arrangement:            "
          f"{cb}/512 = {100*cb/512:.1f}%")
    print(f"   best arrangement: {cd}")
    print()
    print("acquired structure: present 4! = 24 programs = %.2f bits" % np.log2(24))
    print()
    print("Reading: if the permutation ceiling is well below 100% but the 4-slot ceiling is at or")
    print("near it, the format is broad enough and only the DEMONSTRATION needs broadening; if")
    print("both fall short, the cycle is a genuine format limit and a design change is required.")


if __name__=='__main__':
    main()
