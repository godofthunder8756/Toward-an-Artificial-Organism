"""Robustness check for AC78 addendum 2: path-dependence with 50 seeds.

Tightens the linchpin number: is the path-dependence confound (~1.8 sites) the same size as
the coarse good-vs-bad gap (~1.9 sites)? 50 seeds, same-seed paired comparison.
"""
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES_B = ac32.RATES_B
GOOD = (0, 1, 2, 3, 4, 5)
BAD = (5, 4, 2, 1, 0, 3)
H = 16000


def fixed(o, s):
    w = acq.World(s, rates=RATES_B)
    for t in range(1, H + 1):
        wd = w.urgency()
        a = None
        for p in o:
            if wd >> p & 1:
                a = p
                break
        w.tick(a)
    return sum(1 for v in w.life if v > 0)


def switch(o1, o2, s, sw=400):
    w = acq.World(s, rates=RATES_B)
    for t in range(1, H + 1):
        o = o1 if t <= sw else o2
        wd = w.urgency()
        a = None
        for p in o:
            if wd >> p & 1:
                a = p
                break
        w.tick(a)
    return sum(1 for v in w.life if v > 0)


if __name__ == '__main__':
    seeds = list(range(8600, 8650))   # 50 seeds
    fg = np.array([fixed(GOOD, s) for s in seeds])
    ag = np.array([switch(BAD, GOOD, s) for s in seeds])
    fb = np.array([fixed(BAD, s) for s in seeds])
    d = fg - ag
    print(f'n = {len(seeds)}')
    print(f'GOOD fresh {fg.mean():.2f}  sd {fg.std(ddof=1):.2f}')
    print(f'GOOD late  {ag.mean():.2f}  sd {ag.std(ddof=1):.2f}')
    print(f'BAD fresh  {fb.mean():.2f}  sd {fb.std(ddof=1):.2f}')
    print(f'path-dependence confound (fresh - late) = {d.mean():+.2f}  sd {d.std(ddof=1):.2f}')
    print(f'P(fresh > late) = {(d > 0).mean():.2f}')
    print(f'coarse gap (good - bad, fresh) = {fg.mean() - fb.mean():+.2f}')
