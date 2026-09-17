"""AC78 engineering addendum 3: a within-life self-directed learner.

The behavioral test of content self-production. The organism lives ONE life (one seed,
one environment) and must produce a priority from its OWN realized production signal,
with no re-runs, no oracle, no external correct state. The mechanism is the AC72-proposed
AC30 learner transplanted into a single life: the organism holds a priority; every REVIEW
ticks it proposes a swap, holds the candidate for one WINDOW, and keeps it iff the realized
production (mean live sites over the window) did not worsen versus the previous window.

The fixed-point + path-dependence measurements (addendum 1, 2) predict this FAILS: the
production signal is a locked fixed point set by early history, and a mid-life course
change cannot recover what the earlier priority already lost -- the value of the priority
is confounded with the history it inherits, and the confound (~1.8 sites) is the same size
as the entire coarse good-vs-bad gap (~1.9 sites).

Reported score is the STATIONARY quality of the final order (re-run fresh from birth, many
seeds) -- the honest measure of whether the organism produced a good priority. The learner
never sees this; it only sees its own within-life running signal.

Engineering only. No protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES_B = ac32.RATES_B
HORIZON = 16000
REVIEW = 800            # review interval (ticks)
WINDOW = 800            # evaluation window (ticks)
LAST_REVIEW = 8000      # stop revising after the transient (the signal is then locked)


def within_life_learner(seed):
    """One life. Returns the final priority order produced by the organism's own signal.

    Bookkeeping: the organism always acts with either `held` (the incumbent) or `candidate`
    (under test). Every WINDOW ticks it compares the candidate's mean production over the
    window to the incumbent's mean over the previous window, and keeps the candidate iff it
    did not worsen. A candidate that equals the incumbent is a no-op.
    """
    rng = np.random.default_rng([seed, 7801])
    held = tuple(int(x) for x in rng.permutation(6))
    candidate = None
    # window accumulators
    cur_win = 0.0          # sum of live sites in the current window
    cur_win_ticks = 0
    prev_mean = None       # incumbent's mean over the previous window (comparison baseline)
    cand_sum = 0.0         # candidate's sum over its window
    cand_ticks = 0

    w = acq.World(seed, rates=RATES_B)
    for t in range(1, HORIZON + 1):
        # which order acts this tick
        active = candidate if candidate is not None else held
        word = w.urgency()
        action = None
        for pos in active:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
        nlive = sum(1 for v in w.life if v > 0)

        cur_win += nlive
        cur_win_ticks += 1
        if candidate is not None:
            cand_sum += nlive
            cand_ticks += 1

        # window boundary: decide the candidate
        if t % WINDOW == 0 and t <= LAST_REVIEW:
            if candidate is not None and cand_ticks > 0:
                cand_mean = cand_sum / cand_ticks
                if prev_mean is not None and cand_mean >= prev_mean:
                    held = candidate          # keep the swap
                candidate = None              # done testing
                cand_sum = 0.0
                cand_ticks = 0
            # incumbent's mean for this just-ended window becomes the next baseline
            prev_mean = cur_win / cur_win_ticks
            cur_win = 0.0
            cur_win_ticks = 0
            # propose the next candidate (a swap of the current held)
            if t < LAST_REVIEW:
                i, j = rng.integers(0, 6, 2)
                cand = list(held)
                cand[i], cand[j] = cand[j], cand[i]
                candidate = tuple(cand)
    return held


def stationary(order, seed, burnin=8000, horizon=12000):
    w = acq.World(seed, rates=RATES_B)
    acc = 0.0
    for t in range(1, horizon + 1):
        word = w.urgency()
        action = None
        for pos in order:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
        if t > burnin:
            acc += sum(1 for v in w.life if v > 0)
    return acc / (horizon - burnin)


def main():
    seeds = list(range(8600, 8616))            # 16 learner seeds
    produced = [within_life_learner(s) for s in seeds]
    print('within-life self-directed learner, 16 seeds:')
    for s, o in zip(seeds, produced):
        print(f'  seed {s}: {o}')

    stat_seeds = tuple(range(8700, 8730))      # 30 scoring seeds, disjoint
    quals = np.array([float(np.mean([stationary(o, s) for s in stat_seeds])) for o in produced])

    rng = np.random.default_rng(7802)
    rand_quals = np.array([
        float(np.mean([stationary(tuple(int(x) for x in rng.permutation(6)), s)
                       for s in stat_seeds]))
        for _ in range(16)])

    good = np.mean([stationary((0, 1, 2, 3, 4, 5), s) for s in stat_seeds])
    bad = np.mean([stationary((5, 4, 2, 1, 0, 3), s) for s in stat_seeds])

    print(f'\n  stationary quality of PRODUCED orders: mean {quals.mean():.3f}  sd {quals.std(ddof=1):.3f}')
    print(f'  stationary quality of RANDOM orders:   mean {rand_quals.mean():.3f}  sd {rand_quals.std(ddof=1):.3f}')
    print(f'  good order reference: {good:.3f}; bad order reference: {bad:.3f}')
    print(f'  produced - random = {quals.mean()-rand_quals.mean():+.3f}')
    print(f'  produced in the good plateau (>= good-0.5): {(quals >= good-0.5).sum()}/{len(quals)}')
    print(f'  random in the good plateau (>= good-0.5): {(rand_quals >= good-0.5).sum()}/{len(rand_quals)}')


if __name__ == '__main__':
    main()
