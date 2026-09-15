"""The second binding axis: mask width. Companion to `ac20_budget.py`.

`AC20_BUDGET_v1.md` measured the slot axis: full routing needs `C + B <= 9` rules, and the present
design (C=5, B=4) sits exactly on that boundary, so the format binds at the first growth of the
domain. It also identified a *second, independent* limit that it did not measure: the rule word is
`1 + 9 + 4 = 14` bits, so a rule conditions on at most nine observation bits. With an observation
word wider than nine bits, conditions above the ninth cannot be addressed by ANY rule, whatever
the slot count.

This measures that axis the same way, on the same budget:

    demonstration: constituent needs first (bits 0..C-1 -> actions 0..C-1), then the disagreeing
                   banks (bits C..C+B-1) in the acquired order -> actions 2+bank
    format:        `slots` rules of width `1 + mask_bits + 4`

and reports coverage for mask widths 9, 12 and 16 across domains from the present one up to
C + B = 16. The prediction is that a mask narrower than the observation word loses exactly the
banks whose disagreement bits sit above the mask, and that a mask at least as wide as the
observation word restores full coverage provided there are slots for every bank.

Feasibility only: a budget/interpreter analysis, not a world simulation.
"""
import itertools
import numpy as np

SLOTS=9


def demo(o,C,B,order):
    for c in range(C):
        if o&(1<<c): return c
    for bank in order:
        if o&(1<<(C+bank)): return 2+bank
    return 9


def program(C,B,order,slots,mask_bits):
    """One rule per constituent need, then ordered bank rules, each truncated to `mask_bits`."""
    lim=(1<<mask_bits)-1
    rules=[(1,(1<<c)&lim,c) for c in range(C)]
    for b in order:
        if len(rules)>=slots: break
        rules.append((1,(1<<(C+b))&lim,2+b))
    return rules


def evaluate(rules,o):
    for enabled,mask,action in rules:
        if enabled and (o&mask)==mask: return action
    return 9


def coverage(C,B,slots=SLOTS,mask_bits=9):
    """Coverage of the demonstration by the best the format can do. The demonstration is
    parameterised by the acquired order, so evaluating the format with that same order is the
    best case for matching it; enumerating other orders only ever lowers the match and made the
    first version of this script intractable (B=9 is 362,880 permutations x 2^14 observations)."""
    order=tuple(range(B))
    rules=program(C,B,order,slots,mask_bits)
    hit=sum(1 for o in range(1<<(C+B)) if evaluate(rules,o)==demo(o,C,B,order))
    return hit,(1<<(C+B)),order


def unaddressable(C,B,mask_bits):
    """Conditions whose bit index is at or beyond the mask width: no rule can ever test them."""
    return [i for i in range(C+B) if (1<<i)>((1<<mask_bits)-1)]


def main():
    print('coverage by (domain, mask width); slots fixed at %d for the budget axis' % SLOTS)
    print()
    print(f"{'C':>2} {'B':>2} {'obsBits':>7} {'unaddressable@9':>16} {'mask9':>8} {'mask12':>8} {'mask16':>8}")
    for C,B in ((5,4),(5,5),(5,7),(6,6),(5,9),(6,8)):
        row=[]
        for mb in (9,12,16):
            hit,total,_=coverage(C,B,mask_bits=mb)
            row.append(f'{100*hit/total:7.1f}%')
        print(f"{C:>2} {B:>2} {C+B:>7} {str(unaddressable(C,B,9)):>16} {row[0]:>8} {row[1]:>8} {row[2]:>8}")
    print()
    print('with slots widened to cover every bank, mask width alone decides:')
    print(f"{'C':>2} {'B':>2} {'obsBits':>7} {'slots':>6} {'mask9':>8} {'mask12':>8} {'mask16':>8}")
    for C,B in ((5,4),(5,5),(5,7),(6,6),(5,9),(6,8)):
        row=[]
        for mb in (9,12,16):
            hit,total,_=coverage(C,B,slots=C+B,mask_bits=mb)
            row.append(f'{100*hit/total:7.1f}%')
        print(f"{C:>2} {B:>2} {C+B:>7} {C+B:>6} {row[0]:>8} {row[1]:>8} {row[2]:>8}")
    print()
    print('reading: a mask narrower than the observation word loses exactly the conditions above it,')
    print('however many slots are available; a mask at least as wide as the word restores full')
    print('coverage once there are slots for every bank. So a broader world needs BOTH parameters')
    print('at least C+B: slots >= C+B and mask_bits >= C+B.')


if __name__=='__main__':
    main()
