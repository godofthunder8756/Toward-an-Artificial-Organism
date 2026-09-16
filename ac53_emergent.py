"""AC53 (engineering): three compounding causes of six-region order inertness, one fix.

AC52: the six-region order (720 classes / 9.49 bits) is combinatorially real but inert in the AC28
chemistry. This module finds three compounding causes and demonstrates the single fix that resolves all
three.

  Cause 1 -- birth cannot save a site. AC28's region action is birth into an empty slot: it refills a
  vacancy, it cannot prevent an urgent site from expiring. Under any demand regime a birth-only order
  cannot be load-bearing for survival. Fix: a REPAIR action (reset an urgent site's life before expiry).

  Cause 2 -- raw survival is too coarse. With repair, survival buckets all 720 orders into ~4 outcomes.
  The order's effect is *which* site survives, and that only matters when sites differ in value. Fix:
  VALUE-WEIGHTED production (score = sum over alive sites of region value).

  Cause 3 -- the optimum is a balance, not a sort. Naive "highest-value-first" scores ~40 while
  hill-climb reaches ~56: the true optimum spreads repairs across valuable regions instead of starving
  every region after the first. The landscape is graded (42->56) and rugged.

Synthesis: the scaled body = AC28's six-region order structure over AC50's value/stress world, with
repair renewal. Engineering only: no protocol, no final seeds, no claim.
"""
import itertools
import numpy as np
import ac28_regions as ac28

WINDOW = ac28.URGENCY_WINDOW
CHILD_LIFE = ac28.CHILD_LIFE
N = ac28.REGIONS


def run_repair(order, stress, horizon=800, seed=0):
    """Repair renewal (reset life) under per-region stress. Score = raw survival."""
    life = np.full((N, ac28.SITES), CHILD_LIFE, dtype=np.int16)
    energy = 200
    for _ in range(horizon):
        for k in range(N):
            seg = life[k]; seg[seg > 0] -= stress[k]; seg[seg < 0] = 0
        urgent = [k for k in range(N) if np.any((life[k] > 0) & (life[k] <= WINDOW))]
        if urgent and energy >= 1:
            for p in order:
                if p in urgent:
                    seg = life[p]; seg[int(np.argmin(seg))] = CHILD_LIFE; energy -= 1; break
        energy += 2
    return float((life > 0).sum())


def run_value(order, values, stress, horizon=800, seed=0):
    """Repair renewal + value-weighted production. Score = sum of alive-site value."""
    life = np.full((N, ac28.SITES), CHILD_LIFE, dtype=np.int16)
    energy = 300
    for _ in range(horizon):
        for k in range(N):
            seg = life[k]; seg[seg > 0] -= stress[k]; seg[seg < 0] = 0
        urgent = [k for k in range(N) if np.any((life[k] > 0) & (life[k] <= WINDOW))]
        if urgent and energy >= 1:
            for p in order:
                if p in urgent:
                    seg = life[p]; seg[int(np.argmin(seg))] = CHILD_LIFE; energy -= 1; break
        energy += 2
    return float(sum(values[k] * int((life[k] > 0).sum()) for k in range(N)))


def climb(start, score, steps_cap=200):
    import ac33_search
    cur = tuple(start); sc = score(cur); steps = 0
    while steps < steps_cap:
        best, bs = cur, sc
        for cand in ac33_search.swaps(cur):
            s = score(cand)
            if s > bs:
                best, bs = cand, s
        if best == cur:
            return cur, sc, steps
        cur, sc, steps = best, bs, steps + 1
    return cur, sc, steps


def landscape(score):
    scores = [score(o) for o in itertools.permutations(range(N))]
    return max(scores) - min(scores), len(set(scores)), max(scores), min(scores)


if __name__ == '__main__':
    print('=== Cause 1: birth-only is flat; repair restores some signal ===')
    stress_2lvl = [1, 1, 2, 2, 3, 3]
    sp, nu, hi, lo = landscape(lambda o: run_repair(o, stress_2lvl))
    print(f'  repair + raw survival, stress {stress_2lvl}: spread {sp:.0f}, '
          f'distinct {nu}, max {hi:.0f}, min {lo:.0f}  (720 orders -> ~4 outcomes)')

    print('\n=== Cause 2 + 3: value-weighted production grades the landscape ===')
    vals = [6, 5, 4, 3, 2, 1]
    for name, st in [('aligned', [6, 5, 4, 3, 2, 1]), ('reversed', [1, 2, 3, 4, 5, 6])]:
        sc = lambda o, st=st: run_value(o, vals, st)
        sp, nu, hi, lo = landscape(sc)
        vfirst = tuple(int(x) for x in np.argsort(-np.array(vals)))
        print(f'  value {vals}, stress {name} {st}: spread {sp:.0f}, distinct {nu}, '
              f'max {hi:.0f}, min {lo:.0f}; naive value-first scores {run_value(vfirst, vals, st):.0f}')

    print('\n=== Learnability: hill-climb under aligned value+stress ===')
    sc = lambda o: run_value(o, vals, stress_2lvl if False else [6, 5, 4, 3, 2, 1])
    starts = [tuple(int(x) for x in np.random.default_rng([s, 5401]).permutation(N)) for s in range(8)]
    results = [climb(st, sc) for st in starts]
    for st, (o, s, stp) in zip(starts, results):
        print(f'  {st} -> {o}  {s:.0f}  ({stp} steps)')
    print(f'  distinct optima {len(set(r[0] for r in results))}; score range '
          f'{min(r[1] for r in results):.0f}-{max(r[1] for r in results):.0f}')
