"""AC53 (engineering): repair, not birth, is what makes the six-region order load-bearing.

AC52: the six-region order (720 classes) is combinatorially real but inert under imposed demand.
This module first reproduced that with an EMERGENT demand (per-region stress) and birth-only renewal:
the landscape stayed flat (spread 0.0). Root cause: AC28's region action is BIRTH, which fills an
empty slot and therefore cannot SAVE a site from expiry -- it only replaces an already-dead site. No
demand regime can make a birth-only order load-bearing for survival.

This module adds the missing action: REGION REPAIR (reset an urgent site's life, the AC50 renewal
shape), which CAN save a site before it expires. Then, under per-region stress, the order's priority
decides which urgent region is saved -- and survival should grade. Engineering only.
"""
import numpy as np
import ac28_regions as ac28

STRESS = np.array([1, 1, 2, 2, 3, 3], dtype=np.int16)   # region k decays STRESS[k]/tick
REPAIR_ENERGY = 1
HORIZON = 800
WINDOW = ac28.URGENCY_WINDOW
CHILD_LIFE = ac28.CHILD_LIFE


def run(order, seed=0, horizon=HORIZON):
    """Stress-driven decay + order-driven repair (reset life). Score = sites alive at horizon."""
    rng = np.random.default_rng([seed, 5302])
    # uniform start so urgency timing is comparable across regions
    life = np.full((ac28.REGIONS, ac28.SITES), CHILD_LIFE, dtype=np.int16)
    energy = 200
    for _ in range(horizon):
        for k in range(ac28.REGIONS):
            seg = life[k]
            seg[seg > 0] -= STRESS[k]
            seg[seg < 0] = 0
        urgent = [k for k in range(ac28.REGIONS)
                  if np.any((life[k] > 0) & (life[k] <= WINDOW))]
        if urgent and energy >= REPAIR_ENERGY:
            for position in order:
                if position in urgent:
                    seg = life[position]
                    idx = int(np.argmin(seg))          # most-depleted alive site
                    seg[idx] = CHILD_LIFE               # repair: reset life
                    energy -= REPAIR_ENERGY
                    break
        energy += 2                                     # production influx
    return float((life > 0).sum())


def climb(start, horizon=HORIZON):
    import ac33_search
    cur = tuple(start)
    sc = run(cur, horizon=horizon)
    steps = 0
    while True:
        best, bs = cur, sc
        for cand in ac33_search.swaps(cur):
            s = run(cand, horizon=horizon)
            if s > bs:
                best, bs = cand, s
        if best == cur:
            return cur, sc, steps
        cur, sc, steps = best, bs, steps + 1


if __name__ == '__main__':
    starts = [tuple(int(x) for x in np.random.default_rng([s, 5302]).permutation(6)) for s in range(8)]
    results = [climb(st) for st in starts]
    orders = [r[0] for r in results]
    scores = [r[1] for r in results]
    print(f'stress {list(map(int, STRESS))}; repair-reset renewal; horizon {HORIZON}:')
    for st, (o, sc, stp) in zip(starts, results):
        print(f'  {st} -> {o}  score {sc:.0f}  ({stp} steps)')
    distinct = len(set(orders))
    spread = max(scores) - min(scores)
    print(f'\norders found: {distinct} distinct of 8 starts')
    print(f'score spread: {spread:.1f}  (birth-only was 0.0; AC52 imposed-demand was 2.0)')
    print(f'high-stress-first order would be: {tuple(int(x) for x in np.argsort(-STRESS))}')
    print(f'landscape graded (consistent optimum + spread > 0): {distinct <= 2 and spread > 0}')
