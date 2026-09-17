"""AC78 engineering addendum: is the within-life production signal responsive to the priority?

The content self-production question, in its sharpest form: can the organism revise its
priority against its OWN realized production signal within ONE life? For that to be possible,
the production signal must (a) carry priority-quality information, and (b) RESPOND when the
priority changes.

AC77 measured that the live-site count converges to a seed-specific fixed point (N_eff~1):
the count is set by the early transient, then constant while renewals continue. This predicts
that changing the priority AFTER the transient changes nothing observable -- the fixed point
is locked by early history.

This measures that prediction directly, two ways:
  1. Late switch: run good order for 8000 ticks, switch to bad order for the next 8000.
     Does the live-site count move after the switch?
  2. Early switch: switch at tick 400 (during the transient). Does the signal respond then?
  3. Two runs of the SAME final order from the same switch point, to separate the order's
     effect from the trajectory already taken.

Engineering only. No protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES_B = ac32.RATES_B
GOOD = (0, 1, 2, 3, 4, 5)        # top of the stationary ranking (measured)
BAD = (5, 4, 2, 1, 0, 3)         # bottom of the stationary ranking (measured)
HORIZON = 16000
SWITCH = 8000


def run_with_switch(order1, order2, seed, switch=SWITCH):
    """One life: order1 until `switch`, order2 after. Track live-site count over time."""
    w = acq.World(seed, rates=RATES_B)
    series = []
    for t in range(1, HORIZON + 1):
        order = order1 if t <= switch else order2
        word = w.urgency()
        action = None
        for pos in order:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
        series.append(sum(1 for v in w.life if v > 0))
    return series


def main():
    seeds = list(range(8600, 8612))   # 12 seeds, disjoint
    print(f'late switch at t={SWITCH}, 12 seeds (order1 -> order2):\n')

    print('--- 1. GOOD -> BAD (late switch) ---')
    pre_ends, post_means, post_ends = [], [], []
    for s in seeds:
        series = run_with_switch(GOOD, BAD, s)
        pre = series[SWITCH - 1]
        post = series[SWITCH:]          # after switch
        pre_ends.append(pre)
        post_means.append(np.mean(post))
        post_ends.append(post[-1])
    print(f'  live count just before switch: {pre_ends}')
    print(f'  live count just after switch:  {[run_with_switch(GOOD, BAD, s)[SWITCH] for s in seeds]}')
    print(f'  live count at end:             {post_ends}')
    print(f'  mean over post-switch window:  {[round(x,2) for x in post_means]}')
    moved = sum(1 for p, e in zip(pre_ends, post_ends) if e != p)
    print(f'  seeds where the count MOVED after the switch: {moved}/{len(seeds)}')

    print('\n--- 2. GOOD -> GOOD (late switch, control: same order both halves) ---')
    pre_ends, post_ends = [], []
    for s in seeds:
        series = run_with_switch(GOOD, GOOD, s)
        pre_ends.append(series[SWITCH - 1])
        post_ends.append(series[-1])
    moved = sum(1 for p, e in zip(pre_ends, post_ends) if e != p)
    print(f'  seeds where the count moved (no real switch): {moved}/{len(seeds)}')
    print(f'  pre {pre_ends}  end {post_ends}')

    print('\n--- 3. BAD -> GOOD (late switch, reverse direction) ---')
    pre_ends, post_ends = [], []
    for s in seeds:
        series = run_with_switch(BAD, GOOD, s)
        pre_ends.append(series[SWITCH - 1])
        post_ends.append(series[-1])
    moved = sum(1 for p, e in zip(pre_ends, post_ends) if e != p)
    print(f'  seeds where the count moved after BAD->GOOD: {moved}/{len(seeds)}')
    print(f'  pre {pre_ends}  end {post_ends}')

    print('\n--- 4. EARLY switch at t=400: does the transient respond? ---')
    pre_ends, post_ends = [], []
    for s in seeds:
        series = run_with_switch(BAD, GOOD, s, switch=400)
        pre_ends.append(series[399])
        post_ends.append(series[-1])
    print(f'  BAD->GOOD at t=400: pre {pre_ends}  end {post_ends}')
    print(f'  count changed by end in {(np.array(post_ends)!=np.array(pre_ends)).sum()}/{len(seeds)} seeds')


if __name__ == '__main__':
    main()
