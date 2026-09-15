"""AC26: the scaled world's signal logic, and the criterion verified by construction.

What this must deliver
----------------------
AC25 measured the acceptance criterion: every PAIR of the B signals must be simultaneously present
in some reachable observation, and then -- and only then -- the controller's full `log2(B!)` order
structure is real. This module builds a world whose signals have that property BY CONSTRUCTION, and
verifies it, before any reaction chemistry exists.

The construction
----------------
Six maintenance needs, each a cyclic demand: need k is low for the first `WINDOW` ticks of every
`PERIODS[k]` ticks. Choose the periods pairwise COPRIME and the Chinese remainder theorem does the
work: for any pair (i,j) every phase combination occurs within `lcm(Pi,Pj)` ticks, so every pair of
signals is simultaneously low somewhere -- guaranteed, not sampled. The full six-way conjunction
takes `lcm` of all six periods, which is much longer; AC25 showed that is not needed, since pairwise
co-occurrence already suffices for the whole order.

Design consequences measured here
---------------------------------
* how long the world must run before the pair criterion is met (short: max over pairs of lcm);
* how long before EVERY subset of the six is reachable (long: the full lcm);
* and the control -- the same needs with the frozen world's habit of making groups mutually
  exclusive, which is the mechanism that produced the frozen 1.00 bit.
"""
import itertools
import json
import math
import numpy as np
import ac25_confront as cf

PERIODS=(5,7,11,13,17,19)          # pairwise coprime
WINDOW=2                           # ticks per period that the need counts as low
B=len(PERIODS)


def words(ticks):
    """Observation words for t = 0..ticks-1: bit k set while need k is low. Vectorized."""
    t=np.arange(ticks,dtype=np.int64)
    out=np.zeros(ticks,dtype=np.int64)
    for k,P in enumerate(PERIODS):
        out|=(t%P<WINDOW).astype(np.int64)<<k
    return out


def reachable(ticks):
    return sorted(set(int(w) for w in words(ticks)))


def pair_cooccurrence(family):
    """Which signal pairs are simultaneously low somewhere in `family`."""
    pairs={}
    for i,j in itertools.combinations(range(B),2):
        mask=(1<<i)|(1<<j)
        pairs[(i,j)]=any(w&mask==mask for w in family)
    return pairs


def first_pair_time():
    """The earliest tick by which every pair has co-occurred: max over pairs of lcm(Pi,Pj).
    With coprime periods that is Pi*Pj for the largest pair."""
    return max(PERIODS[i]*PERIODS[j] for i,j in itertools.combinations(range(B),2))


def full_lcm():
    lcm=1
    for P in PERIODS: lcm=math.lcm(lcm,P)
    return lcm


# --- control: the frozen world's habit, applied to the same needs -----------------------------

def epochs_family(ticks,group_size=2):
    """Same needs, but only one group is 'live' at a time (the frozen world's activation habit:
    a region is active only for individuals of its history). Needs outside the active group are
    forced satisfied, so only within-group pairs can ever co-occur."""
    t=np.arange(ticks,dtype=np.int64)
    groups=[list(range(g,min(g+group_size,B))) for g in range(0,B,group_size)]
    out=[]
    for tick in t:
        active=groups[int(tick//50)%len(groups)]
        word=0
        for k in active:
            if tick%PERIODS[k]<WINDOW: word|=1<<k
        out.append(word)
    return sorted(set(out))


def frozen_masks_family():
    """The frozen world's actual signal structure: masks 4,8,16,32; bit 5 never set; exactly one
    region varies in a given individual's run."""
    return [1<<2,1<<3,1<<2|1<<3]


if __name__=='__main__':
    rows={}
    codes=cf.unique_codes(B)
    print(f'{B} needs, periods {PERIODS} (pairwise coprime), low window {WINDOW} ticks\n')

    # 1. does every pair co-occur, and how early?
    tp=first_pair_time()
    fam_tp=reachable(tp)
    pc=pair_cooccurrence(fam_tp)
    print(f'every pair co-occurs within {tp} ticks (max pair lcm): {all(pc.values())}')
    print(f'  pairs found: {sum(pc.values())}/{len(pc)}')

    # 2. the criterion: behaviour classes over the permutation space
    c_tp=cf.classes(codes,fam_tp)
    print(f'\nreachable family at {tp} ticks: {len(fam_tp)} distinct words')
    print(f'  behaviour classes {c_tp} of {math.factorial(B)}  ->  {math.log2(c_tp):.2f} bits')
    rows['pairwise family (first_pair_time)']=dict(ticks=tp,words=len(fam_tp),classes=c_tp,
                                                   bits=math.log2(c_tp))

    # 3. how long until every subset is reachable, and does it buy anything extra?
    fl=full_lcm()
    fam_all=reachable(fl)
    c_all=cf.classes(codes,fam_all)
    print(f'\nfull lcm {fl} ticks: {len(fam_all)} distinct words (all subsets '
          f'{len(fam_all)==2**B})')
    print(f'  behaviour classes {c_all}  ->  {math.log2(c_all):.2f} bits')
    print(f'  so the pair criterion is met {fl/tp:.0f}x sooner and buys the same order structure')
    rows['all subsets (full lcm)']=dict(ticks=fl,words=len(fam_all),classes=c_all,
                                        bits=math.log2(c_all))

    # 4. controls
    fam_ep=epochs_family(2000)
    c_ep=cf.classes(codes,fam_ep)
    pairs_ep=pair_cooccurrence(fam_ep)
    print(f'\ncontrol -- needs made mutually exclusive by epochs (the frozen habit):')
    print(f'  distinct words {len(fam_ep)};  pairs co-occurring {sum(pairs_ep.values())}/'
          f'{len(pairs_ep)}')
    print(f'  behaviour classes {c_ep}  ->  {math.log2(c_ep):.2f} bits')
    rows['control: exclusive epochs']=dict(words=len(fam_ep),pairs=sum(pairs_ep.values()),
                                           classes=c_ep,bits=math.log2(c_ep))

    frozen=frozen_masks_family()
    c_fr=cf.classes([1<<2,1<<3,1<<4,1<<5],frozen,[2,3,4,5])
    print(f'\ncontrol -- the frozen world\'s own signals: classes {c_fr} -> {math.log2(c_fr):.2f} '
          f'bits  (AC24/AC25 measured 2 classes, 1.00 bit)')
    rows['control: frozen signals']=dict(words=len(frozen),classes=c_fr,bits=math.log2(c_fr))

    print(f'\ncriterion met by the independent-needs design: {c_tp==math.factorial(B)} '
          f'({c_tp}/{math.factorial(B)} classes)')
    json.dump(rows,open('ac26_signals_v1.json','w'),indent=2)
