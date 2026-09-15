"""AC27: a demand schedule that presents every exact pair, and the learning frontier.

Where this comes from
--------------------
AC26 corrected AC25's criterion: it is not enough for pairs of signals to CO-OCCUR, because an
observation is read by first match and a third signal in the same word can pre-empt the comparison.
What the controller's full order needs is an EXACT PAIR WITNESS -- a reachable observation equal to
`{i,j}` and nothing else -- for every pair.

The cyclic coprime-needs design does eventually present exact pairs, but only at its full
conjunction period, which was 1,616,615 ticks for six needs. That is not a design to ship. This
module presents them DELIBERATELY: the world's demand pattern cycles through the pairs, so the
controller's order structure is fully determined after a small number of rounds rather than
eventually.

What "early" means is measured, not asserted: `frontier` returns the first schedule index at which
the number of distinguishable behaviours reaches `B!` -- the tick at which the world has, for the
first time, said everything about the order that it is ever going to say.
"""
import itertools
import json
import math
import ac25_confront as cf

B=6


def all_pairs():
    return [(1<<i)|(1<<j) for i,j in itertools.combinations(range(B),2)]


def all_singletons():
    return [1<<k for k in range(B)]


def pair_round_schedule(repeat=1):
    """The deliberate schedule: each exact pair, one per round, cycled `repeat` times, with the
    singletons and the empty demand interleaved so the world also shows every need alone (which the
    frozen world does too, and which a real chemistry would present anyway)."""
    out=[]
    for _ in range(repeat):
        for w in all_pairs(): out.append(w)
        for w in all_singletons(): out.append(w)
        out.append(0)
    return out


def frontier(schedule,codes=None):
    """First index at which the prefix's reachable family distinguishes B! behaviours, and the
    class counts along the way."""
    codes=codes if codes is not None else cf.unique_codes(B)
    target=math.factorial(B)
    seen=[]
    counts=[]
    for index,word in enumerate(schedule,start=1):
        if word not in seen: seen.append(word)
        counts.append(cf.classes(codes,seen))
        if counts[-1]==target:
            return dict(index=index,words=len(seen),classes=counts[-1],counts=counts)
    return dict(index=None,words=len(seen),classes=counts[-1] if counts else 0,counts=counts)


def minimal_schedule():
    """The smallest set of presentations that reaches the full order: the exact pairs alone
    (AC25's 'all pairs' family is exactly this, which is why it reached 720)."""
    return all_pairs()


if __name__=='__main__':
    codes=cf.unique_codes(B)
    target=math.factorial(B)
    rows={}
    print(f'{B} needs; target {target} behaviour classes ({math.log2(target):.2f} bits)\n')

    print('--- minimum: the exact pairs alone ---')
    c=cf.classes(codes,minimal_schedule())
    print(f'  {len(minimal_schedule())} presentations -> {c} classes ({math.log2(c):.2f} bits)')
    rows['exact pairs alone']=dict(presentations=len(minimal_schedule()),classes=c,bits=math.log2(c))

    print('\n--- the deliberate schedule and its frontier ---')
    sched=pair_round_schedule(repeat=1)
    fr=frontier(sched)
    print(f'  schedule length {len(sched)} rounds')
    print(f'  full order first distinguishable after {fr["index"]} rounds '
          f'({fr["words"]} distinct presentations) -> {fr["classes"]} classes')
    print(f'  class count after each round: {fr["counts"]}')
    rows['deliberate schedule']=dict(rounds=len(sched),frontier_index=fr['index'],
                                     classes=fr['classes'],counts=fr['counts'])

    print('\n--- robustness: do higher-order demands hurt? ---')
    pairs=all_pairs()
    c_pairs_only=cf.classes(codes,pairs)
    c_plus_single=cf.classes(codes,pairs+all_singletons()+[0])
    triples=[sum(t) for t in itertools.combinations([1<<k for k in range(B)],3)]
    c_plus_triples=cf.classes(codes,pairs+all_singletons()+triples+[0])
    c_all=cf.classes(codes,cf.family_all(codes))
    print(f'  exact pairs only                 {c_pairs_only:4d} classes')
    print(f'  + singletons + empty             {c_plus_single:4d} classes')
    print(f'  + all triples                    {c_plus_triples:4d} classes')
    print(f'  + every subset (2^B)             {c_all:4d} classes')
    print(f'  higher-order demands never REDUCE the count: '
          f'{min(c_pairs_only,c_plus_single,c_plus_triples,c_all)==target}')
    rows['robustness']=dict(pairs_only=c_pairs_only,pairs_singletons=c_plus_single,
                            plus_triples=c_plus_triples,all_subsets=c_all)

    print('\n--- against the cyclic design of AC26 ---')
    print(f'  coprime-oscillator needs: full order only at the full period (1,616,615 ticks)')
    print(f'  deliberate schedule:      full order after {fr["index"]} rounds, '
          f'{len(sched)} at most')
    print(f'  ratio: {1616615/fr["index"]:,.0f}x sooner')

    print('\n--- control: the schedule with groups made exclusive (the frozen habit) ---')
    groups=[[0,1],[2,3],[4,5]]
    excl=[]
    for g in groups:
        for k in g: excl.append(1<<k)
    c_excl=cf.classes(codes,excl)
    print(f'  one need at a time, grouped: {c_excl} classes ({math.log2(c_excl):.2f} bits)')
    rows['control: grouped exclusivity']=dict(classes=c_excl,bits=math.log2(c_excl))

    print(f'\nverified: schedule meets the AC26 criterion = {fr["classes"]==target}')
    json.dump(rows,open('ac27_schedule_v1.json','w'),indent=2)
