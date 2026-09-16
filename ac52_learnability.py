"""AC52 (engineering): is the six-region order structure learnable in the AC28 chemistry?

AC28 built the chemistry (body-state signals, per-region births, conservation) but not the organism:
no acquisition, no register, no retention. Its next step is acquisition + retention over the 720-order
structure. Before building that, the bounded precursor (the AC24-27 habit) is: does a search actually
find a *distinct optimal order* in this chemistry, or is the fitness landscape flat?

This scores orders by births + survival over a long demand schedule, with site recycling (sites expire,
births refill empty slots), and hill-climbs. Engineering only: no protocol, no final seeds, no claim.
"""
import numpy as np
import ac28_regions as ac28
import ac27_schedule as sched


def score(order, rounds=8, seed=0):
    """Total births + final survival over `rounds` passes of the deliberate pair schedule."""
    b = ac28.acquire(seed)
    births = 0
    for word in sched.pair_round_schedule(repeat=rounds):
        for k in range(ac28.REGIONS):
            if word >> k & 1:
                # land the imposed urgency in the body so the action is supportable
                seg = ac28.region_sites(b, k)
                idx = int(np.flatnonzero(seg > 0)[0]) if np.any(seg > 0) else 0
                b.life[k * ac28.SITES + idx] = 8
        e, _ = ac28.step(b, tuple(order))
        births += e['region_births']
    return float(births) + float((b.life > 0).sum())


def climb(start, rounds=8):
    cur = tuple(start)
    sc = score(cur, rounds)
    steps = 0
    while True:
        best = cur
        bs = sc
        for cand in __import__('ac33_search').swaps(cur):
            s = score(cand, rounds)
            if s > bs:
                best, bs = cand, s
        if best == cur:
            return cur, sc, steps
        cur, sc = best, bs
        steps += 1


if __name__ == '__main__':
    starts = [tuple(int(x) for x in np.random.default_rng([s, 5201]).permutation(6)) for s in range(8)]
    results = [climb(st) for st in starts]
    scores = [r[1] for r in results]
    orders = [r[0] for r in results]
    print('hill-climb from 8 random starts (8 schedule rounds):')
    for st, (o, sc, stp) in zip(starts, results):
        print(f'  {st} -> {o}  score {sc:.0f}  ({stp} steps)')
    distinct = len(set(orders))
    spread = max(scores) - min(scores)
    print(f'\norders found: {distinct} distinct of 8 starts')
    print(f'score spread: {spread:.1f}  (0 = flat landscape, no learnable optimum)')
    print(f'landscape learnable (distinct optimum, consistent across starts): '
          f'{distinct <= 2 and spread > 0}')
