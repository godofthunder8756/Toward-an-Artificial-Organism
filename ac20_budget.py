"""Where does the 9-slot rule format bind? A rule-budget analysis.

`ac20_feasibility.py` showed that on the present domain (5 constituent needs, 4 banks) the format
reproduces essentially any preference structure one can devise, so the format is not the
constraint at that scale. But the present design sits at exactly 9 slots:

    5 constituent rules (fuel, material, W, C, B)  +  4 bank-repair rules  =  9  =  the format

So the question becomes whether that is a knife-edge -- whether ANY domain growth makes the
format bind. This measures it directly on the budget, without building a new world: for a world
with C constituent needs and B banks, the 9 slots hold C fixed constituent rules and leave 9-C
slots for B banks, so full routing needs 9-C >= B, i.e. **C + B <= 9**. Beyond that the acquired
structure cannot cover every bank and the demonstration cannot be reproduced exactly.

This is a *budget* analysis, not a world simulation: it establishes where the format binds, not
how an organism behaves there. A world at that scale is the next build, not this one.
"""
import itertools
import numpy as np

SLOTS=9


def demo(o,C,B,order):
    """The general demand: constituent needs first (bits 0..C-1 -> actions 0..C-1), then the
    disagreeing banks (bits C..C+B-1) in the acquired order -> actions 2+bank."""
    for c in range(C):
        if o&(1<<c): return c
    for bank in order:
        if o&(1<<(C+bank)): return 2+bank
    return 9


def program_slots(C,B,order):
    """What the format can install: one rule per constituent need, then as many ordered bank
    rules as slots remain. Slots the format does not have are simply absent."""
    rules=[(1,1<<c,c) for c in range(C)]
    room=max(0,SLOTS-C)
    rules+=[(1,1<<(C+b),2+b) for b in order[:room]]
    return rules


def evaluate(rules,o):
    for enabled,mask,action in rules:
        if enabled and o&mask==mask: return action
    return 9


def coverage(C,B):
    """Best coverage over every acquired bank order the surviving slots can express."""
    best=0; best_order=None
    for order in itertools.permutations(range(B)):
        rules=program_slots(C,B,order)
        hit=sum(1 for o in range(1<<(C+B)) if evaluate(rules,o)==demo(o,C,B,order))
        if hit>best: best=hit; best_order=order
    return best,(1<<(C+B)),best_order


def main():
    print(f"the format holds {SLOTS} rules; full routing needs C + B <= {SLOTS}")
    print()
    print(f"{'C':>2} {'B':>2} {'C+B':>4} {'slots left for banks':>21} {'coverage':>10} {'acquired bits':>14}")
    for C in (4,5,6,7):
        for B in (3,4,5,6):
            if C+B>11: continue
            hit,total,order=coverage(C,B)
            room=max(0,SLOTS-C)
            import math
            bits=math.log2(math.factorial(B))
            flag='' if C+B<=SLOTS else '   <- format binds'
            print(f"{C:>2} {B:>2} {C+B:>4} {room:>21} {hit:>5}/{total:<4} = {100*hit/total:5.1f}% "
                  f"{bits:>13.2f}b{flag}")
    print()
    print("the present design (C=5, B=4) sits exactly on the boundary: C+B = 9 = the slot count.")
    print("one more constituent need, or one more bank, and the acquired structure loses a slot it")
    print("needs -- so the format binds at the very first growth of the domain.")


if __name__=='__main__':
    main()
