"""AC78 engineering: characterize the regime-B coarse structure vs single-life noise.

The prerequisite (AC77) answered the signal-horizon question NO and reframed the
target: content self-production should gate on the COARSE good-vs-bad separation
(~1.5 sites), not the fine/ceiling margin. Before building the learner study, this
measures exactly what the organism's own single-life signal can distinguish.

Three measurements:
  1. The stationary ranking of a sample of orders (good plateau vs bad tail).
  2. The single-life (snapshot@800) signal for a good order vs a bad order,
     and the paired within-seed good-minus-bad difference.
  3. The coarse good-vs-bad gap vs the single-life noise floor: is 1.5 sites
     resolvable from ONE life, or does it need the multi-seed oracle?

Engineering only. No protocol, no final seeds, no claim.
"""
import itertools
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES_B = ac32.RATES_B
CEILING = ac32.DECLARED_OPTIMA['B'][0]          # (2,0,1,3,5,4)
MEDIOCRE = (0, 1, 2, 3, 4, 5)
BURNIN = 8000
HORIZON = 12000
N_SURVEY = 30                                   # orders in the stationary survey
N_SEEDS = 30                                    # survey seeds per order


def run_once(order, seed, ticks=800):
    """One life, snapshot sites retained at `ticks`."""
    w = acq.World(seed, rates=RATES_B)
    for t in range(1, ticks + 1):
        word = w.urgency()
        action = None
        for pos in order:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
    return sum(1 for v in w.life if v > 0)


def run_stationary(order, seed):
    """Time-average live sites over [BURNIN, HORIZON] (the fixed-point mean)."""
    w = acq.World(seed, rates=RATES_B)
    acc = 0.0
    for t in range(1, HORIZON + 1):
        word = w.urgency()
        action = None
        for pos in order:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
        if t > BURNIN:
            acc += sum(1 for v in w.life if v > 0)
    return acc / (HORIZON - BURNIN)


def main():
    rng = np.random.default_rng(7701)
    orders = [tuple(int(x) for x in rng.permutation(6)) for _ in range(N_SURVEY)]
    orders += [CEILING, MEDIOCRE]
    seeds = tuple(range(8500, 8500 + N_SEEDS))   # disjoint family

    print(f'=== 1. stationary ranking (regime B, {len(orders)} orders x {N_SEEDS} seeds) ===')
    means = {}
    for o in orders:
        vals = [run_stationary(o, s) for s in seeds]
        means[o] = float(np.mean(vals))
    ranked = sorted(means.items(), key=lambda kv: -kv[1])
    vals_arr = np.array(list(means.values()))
    print(f'  ceiling (2,0,1,3,5,4) = {means[CEILING]:.3f}')
    print(f'  min {vals_arr.min():.3f}  median {np.median(vals_arr):.3f}  max {vals_arr.max():.3f}')
    print(f'  sd across orders {vals_arr.std(ddof=1):.3f}')
    print(f'  coarse spread (max-min) {vals_arr.max()-vals_arr.min():.3f}')
    print('  top 6:')
    for o, v in ranked[:6]:
        tag = 'CEILING' if o == CEILING else ''
        print(f'    {o}  {v:.3f}  {tag}')
    print('  bottom 6:')
    for o, v in ranked[-6:]:
        tag = 'MEDIOCRE' if o == MEDIOCRE else ''
        print(f'    {o}  {v:.3f}  {tag}')
    bad_order = ranked[-1][0]
    good_order = ranked[0][0]
    print(f'  -> good order {good_order} ({means[good_order]:.3f}), '
          f'bad order {bad_order} ({means[bad_order]:.3f})')

    print('\n=== 2. single-life signal: good vs bad, paired within-seed (100 seeds) ===')
    good_snap = [run_once(good_order, s) for s in seeds]
    bad_snap = [run_once(bad_order, s) for s in seeds]
    d = np.array(good_snap) - np.array(bad_snap)
    print(f'  good snap@800: mean {np.mean(good_snap):.3f}  sd {np.std(good_snap, ddof=1):.3f}')
    print(f'  bad  snap@800: mean {np.mean(bad_snap):.3f}  sd {np.std(bad_snap, ddof=1):.3f}')
    print(f'  paired good-bad: mean {d.mean():+.3f}  sd {d.std(ddof=1):.3f}  '
          f'se {d.std(ddof=1)/np.sqrt(len(d)):.3f}')
    print(f'  P(good > bad on the same seed) = {(d > 0).mean():.3f}')

    print('\n=== 3. the coarse gap vs single-life noise ===')
    gap_stationary = means[good_order] - means[bad_order]
    # single-life noise = sd of one order's snapshot score across seeds
    noise = np.std(good_snap, ddof=1)
    print(f'  coarse stationary gap (good-bad) = {gap_stationary:.3f} sites')
    print(f'  single-life noise (sd of snapshot) = {noise:.3f} sites')
    print(f'  ratio gap/noise = {gap_stationary/noise:.3f}')
    # what a single-life learner can see: it evaluates each candidate on ONE seed,
    # so its pairwise comparison noise is sd of (cand1 - cand2) across seeds = sqrt(2)*noise
    print(f'  single-life pairwise-comparison noise = {noise*np.sqrt(2):.3f} sites')

    # a self-directed learner must rank candidates by their own realized single life.
    # how many independent lives would it take to resolve the coarse gap?
    # se of the mean of n lives = noise/sqrt(n); need se << gap
    n_for_1se = (noise / gap_stationary) ** 2
    print(f'  lives needed for se == gap: ~{n_for_1se:.1f}')
    print(f'  (a single life gives se == noise = {noise:.2f}, gap {gap_stationary:.2f})')


if __name__ == '__main__':
    main()
