"""AC25: what makes a controller's rule ORDER learnable -- confrontability, measured.

The question
-----------
AC24 measured the frozen world's developmental function at 1.00 effective bit: two of its four rule
positions can never fire, so 24 permutations collapse to 2 behaviours. The scaled world is supposed
to carry more. What exactly must the world present for `log2(B!)` of order structure to be real?

Order information can only come from CONFRONTATION: a rule's position is revealed only when another
rule also matches the same observation and the earlier one wins. So:

  * if every reachable observation sets exactly ONE signal, each observation matches exactly one
    rule, the chosen action is that rule's action, and the order is invisible -- all B! permutations
    behave identically (ZERO effective bits, however many signals are live);
  * a total order is determined by its pairwise comparisons, so it suffices for every PAIR of
    signals to be set simultaneously in some reachable observation -- then all B! orders are
    distinguished.

This module measures that ladder rather than asserting it. It is pure design-space arithmetic: no
chemistry, no organism, no world. Its output is the design criterion the scaled world must meet.

Codes are observation bit masks, one per rule position. A "family" is the set of observation words
the world can present; `classes` counts distinct first-match behaviours over all permutations.
"""
import itertools
import json
import math


def behaviour(permutation,masks,actions,observations):
    """Which ACTION fires first for each observation (or None if none matches).

    It records the action rather than the rule's index, because the action is what the world sees:
    two rule positions that share a mask AND an action are behaviourally one thing, and their
    relative order is then unobservable. Recording the index would hide that dilution."""
    out=[]
    for obs in observations:
        chosen=None
        for index in permutation:
            if obs&masks[index]==masks[index]:
                chosen=actions[index]; break
        out.append(chosen)
    return tuple(out)


def classes(masks,observations,actions=None):
    """Distinct behaviours over all permutations of the rule positions: the honest count of what the
    controller's order can express in a world that presents `observations`."""
    actions=actions if actions is not None else list(range(len(masks)))
    return len({behaviour(p,masks,actions,observations)
                for p in itertools.permutations(range(len(masks)))})


def effective_bits(masks,observations,actions=None):
    return math.log2(classes(masks,observations,actions))


# --- reachability families -------------------------------------------------------------------

def family_subsets(codes,size):
    """All observations setting exactly `size` of the codes."""
    return [sum(c for c in combo) for combo in itertools.combinations(codes,size)]


def family_upto(codes,size):
    return [w for k in range(size+1) for w in family_subsets(codes,k)]


def family_all(codes):
    return family_upto(codes,len(codes))


def unique_codes(n):
    """One disjoint bit per rule position: bit 0 .. bit n-1."""
    return [1<<k for k in range(n)]


def report(name,codes,observations,rows):
    c=classes(codes,observations); bits=math.log2(c)
    rows[name]=dict(codes=len(codes),observations=len(observations),classes=c,
                    nominal_bits=math.log2(math.factorial(len(codes))),bits=bits)
    print(f'  {name:50s} obs {len(observations):4d}  classes {c:6d}  bits {bits:5.2f}')
    return c


if __name__=='__main__':
    B=6
    codes=unique_codes(B)
    nominal=math.log2(math.factorial(B))
    print(f'B = {B} rule positions -> {math.factorial(B)} permutations, nominal {nominal:.2f} bits')
    rows={}

    print('\n--- the ladder: how much co-occurrence buys ---')
    report('singletons only (each observation sets one signal)',codes,family_subsets(codes,1),rows)
    report('all pairs',codes,family_subsets(codes,2),rows)
    report('all triples',codes,family_subsets(codes,3),rows)
    report('all subsets (2^B)',codes,family_all(codes),rows)
    report('singletons + pairs (no triples or higher)',codes,
           family_subsets(codes,1)+family_subsets(codes,2),rows)

    print('\n--- dilution: what each defect costs, with all pairs otherwise reachable ---')
    obs5=family_subsets(codes[1:],2)+family_subsets(codes[1:],1)
    report('one position dead (5 live, all pairs)',codes[1:],obs5,rows)
    obs4=family_subsets(codes[2:],2)+family_subsets(codes[2:],1)
    report('two positions dead (4 live, all pairs)',codes[2:],obs4,rows)

    # two positions sharing a mask: their order is invisible. The duplicated mask must still
    # co-occur with the others, otherwise the row measures "never confronted" rather than
    # "fused", which is a different defect.
    dupm=[codes[0],codes[0]]+codes[1:5]                 # 6 positions, first two fused
    obs_dup=sorted(set(family_subsets(codes[:5],1)+family_subsets(codes[:5],2)))
    c=classes(dupm,obs_dup,[0,0,1,2,3,4])
    rows['two rules share mask and action']=dict(codes=6,observations=len(obs_dup),classes=c,
                                                 nominal_bits=nominal,bits=math.log2(c))
    print(f'  {"two rules share mask AND action":50s} obs {len(obs_dup):4d}  '
          f'classes {c:6d}  bits {math.log2(c):5.2f}')

    # same fused mask but different actions: the order of the fused pair IS observable
    c2=classes(dupm,obs_dup,[0,99,1,2,3,4])
    rows['two rules share mask, actions differ']=dict(codes=6,observations=len(obs_dup),classes=c2,
                                                      nominal_bits=nominal,bits=math.log2(c2))
    print(f'  {"same mask, different actions":50s} obs {len(obs_dup):4d}  '
          f'classes {c2:6d}  bits {math.log2(c2):5.2f}')

    print('\n--- control: the frozen configuration, re-measured with the same method ---')
    frozen=[1<<2,1<<3,1<<4,1<<5]
    obs_frozen=[1<<2,1<<3,1<<2|1<<3]        # bit 5 never set; only one region varies per history
    c=classes(frozen,obs_frozen,[2,3,4,5])
    rows['frozen configuration (control)']=dict(codes=4,observations=len(obs_frozen),classes=c,
                                               nominal_bits=math.log2(24),bits=math.log2(c))
    print(f'  {"frozen: masks 4,8,16,32; bit 5 unset; one region varies":50s} '
          f'obs {len(obs_frozen):4d}  classes {c:6d}  bits {math.log2(c):5.2f}'
          f'   <- AC24 measured 2 classes, 1.00 bit')

    target=rows['all pairs']
    print(f"\ntarget for the scaled world: every PAIR of the {B} signals co-occurring in some\n"
          f"reachable observation -> {target['classes']} behaviour classes = {target['bits']:.2f} "
          f"bits, i.e. the full nominal order structure.")
    json.dump(rows,open('ac25_confront_v1.json','w'),indent=2)
