"""AC33 engineering: does a stronger search mechanism actually remove the 1-in-12 failure?

Why measure the landscape before declaring anything
---------------------------------------------------
AC32's G2 failed because one individual's search landed on an order rated 11.75 while its peers
reached 12.33-12.42 against a scaffold ceiling of 12.67. The diagnosis was local optima: mutate-and-
keep with random single swaps cannot leave a basin. Before writing a protocol for a "fixed" mechanism,
the question is whether ANY climb with a better neighbourhood reliably reaches the ceiling -- and that
is a property of the search landscape, measurable directly and cheaply, with no arms and no claim.

Method
------
With paired 12-seed scoring the rating is a DETERMINISTIC function of the order, so steepest ascent
over a neighbourhood is well defined: evaluate every neighbour, move to the best, repeat until no
improvement. Then:
  * climb from many random starts under the swap-only neighbourhood (AC32's effective mechanism);
  * climb from the same starts under swaps + insertions + reversals;
  * compare the distributions of the resulting local optima.
If the stronger neighbourhood's WORST start still falls short of the ceiling, no restart scheme of
this family will fix AC32's failure and the representation is what needs changing -- which is a much
cheaper thing to learn here than after another frozen run.

This is engineering. No protocol, no final seeds, no claim.
"""
import itertools
import json
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES=ac32.RATES_B
CEILING_ORDER=ac32.DECLARED_OPTIMA['B'][0]
CEILING=ac32.DECLARED_OPTIMA['B'][1]


def swaps(order):
    n=len(order)
    return [tuple(order[:i]+(order[j],)+order[i+1:j]+(order[i],)+order[j+1:])
            for i in range(n) for j in range(i+1,n)]


def insertions(order):
    """Move one element to another position."""
    out=set()
    n=len(order)
    for i in range(n):
        for j in range(n):
            if i==j: continue
            rest=list(order); item=rest.pop(i); rest.insert(j,item)
            out.add(tuple(rest))
    return sorted(out)


def reversals(order):
    out=set()
    n=len(order)
    for i in range(n):
        for j in range(i+2,n+1):
            out.add(tuple(order[:i]+tuple(reversed(order[i:j]))+order[j:]))
    return sorted(out)


NEIGHBOURHOODS={'swaps_only':swaps,
                'swaps+insertions+reversals':lambda o: swaps(o)+insertions(o)+reversals(o)}


def climb(start,neighbourhood,rates=RATES):
    current=tuple(start)
    score=ac32.rating(current,rates)
    steps=0
    while True:
        best=current; best_score=score
        for cand in neighbourhood(current):
            s=ac32.rating(cand,rates)
            if s>best_score:
                best,best_score=cand,s
        if best==current: return current,score,steps
        current,score=best,best_score; steps+=1


if __name__=='__main__':
    starts=[tuple(int(x) for x in np.random.default_rng([s,3301]).permutation(6))
            for s in range(24)]
    print(f'ceiling: {CEILING_ORDER} = {CEILING:.2f}\n')
    rows={}
    for name,nh in NEIGHBOURHOODS.items():
        results=[climb(st,nh) for st in starts]
        scores=[r[1] for r in results]
        steps=[r[2] for r in results]
        distinct=len({r[0] for r in results})
        at_ceiling=sum(1 for s in scores if s>=CEILING-1e-9)
        near=sum(1 for s in scores if s>=CEILING-0.34)
        print(f'{name}:')
        print(f'  local optima reached: min {min(scores):.2f}  mean {np.mean(scores):.2f}  '
              f'max {max(scores):.2f}  distinct {distinct}')
        print(f'  at the ceiling exactly: {at_ceiling}/{len(starts)};  within 0.34: {near}/'
              f'{len(starts)}')
        print(f'  climb lengths: mean {np.mean(steps):.1f} steps')
        rows[name]=dict(scores=[float(s) for s in scores],distinct=distinct,
                        at_ceiling=at_ceiling,near=near,mean=float(np.mean(scores)),
                        worst=float(min(scores)),mean_steps=float(np.mean(steps)))
    json.dump(rows,open('/tmp/ac33_landscape.json','w'),indent=2)
