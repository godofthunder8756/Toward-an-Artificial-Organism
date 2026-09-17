"""AC78 engineering addendum 2: path dependence of the production signal.

The decisive structural question for content self-production: can the organism evaluate
a candidate priority against its own within-life signal, independent of its own history?

If the fixed point is path-dependent -- set by the early transient, unrecoverable by a later
course change -- then the organism cannot run a within-life counterfactual: the same priority
evaluated after a different history gives a systematically different outcome, so the organism
cannot compare two priorities from its own single trajectory.

Measurement: on the SAME seed, (a) GOOD order run from birth, vs (b) GOOD order adopted at
t=400 after a BAD transient. If (a) systematically beats (b), the priority's own value is
confounded with the history it inherits -- a single life cannot tell them apart.

Engineering only. No protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES_B = ac32.RATES_B
GOOD = (0, 1, 2, 3, 4, 5)
BAD = (5, 4, 2, 1, 0, 3)
HORIZON = 16000


def run_fixed(order, seed):
    w = acq.World(seed, rates=RATES_B)
    for t in range(1, HORIZON + 1):
        word = w.urgency()
        action = None
        for pos in order:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
    return sum(1 for v in w.life if v > 0)


def run_switch(order1, order2, seed, switch=400):
    w = acq.World(seed, rates=RATES_B)
    for t in range(1, HORIZON + 1):
        order = order1 if t <= switch else order2
        word = w.urgency()
        action = None
        for pos in order:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
    return sum(1 for v in w.life if v > 0)


def main():
    seeds = list(range(8600, 8624))   # 24 seeds
    print('paired path-dependence, 24 seeds (same seed):\n')
    fresh_good, adopted_good = [], []
    fresh_bad = []
    for s in seeds:
        fresh_good.append(run_fixed(GOOD, s))
        adopted_good.append(run_switch(BAD, GOOD, s, switch=400))
        fresh_bad.append(run_fixed(BAD, s))
    fg, ag, fb = np.array(fresh_good), np.array(adopted_good), np.array(fresh_bad)
    print(f'  GOOD from birth:          mean {fg.mean():.2f}  sd {fg.std(ddof=1):.2f}')
    print(f'  GOOD after BAD transient: mean {ag.mean():.2f}  sd {ag.std(ddof=1):.2f}')
    print(f'  BAD from birth:           mean {fb.mean():.2f}  sd {fb.std(ddof=1):.2f}')
    d = fg - ag
    print(f'\n  paired difference (GOOD-fresh minus GOOD-adopted-late): mean {d.mean():+.2f}  sd {d.std(ddof=1):.2f}')
    print(f'  P(fresh GOOD > adopted-late GOOD) = {(d > 0).mean():.2f}')
    print(f'  P(adopted-late GOOD still > BAD-fresh) = {(ag > fb).mean():.2f}')

    # the honest counterfactual comparison: within a life, the organism only ever sees ONE
    # trajectory.  The value of adopting GOOD late is not "GOOD's value" but "GOOD's value
    # conditional on the history BAD left", which is a different quantity.
    print(f'\n  interpretation: adopting GOOD at t=400 after BAD leaves '
          f'{fg.mean()-ag.mean():.2f} sites on the table vs a fresh GOOD start --')
    print(f'  the priority value is confounded with the history it inherits.')


if __name__ == '__main__':
    main()
