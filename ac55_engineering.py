"""AC55 engineering: concentrated value + demanding world; two-family four-check before the protocol.

AC54's freeze failed: the order effect was ~7.8% (near noise) and the world occasionally hit the ceiling.
This module applies AC54's own fix -- concentrate the value (AC51's lever) and raise the stress -- and,
crucially, pre-flights the four-check on TWO disjoint engineering seed families so a scoring-seed
overfit is caught before any protocol (AC54 only caught it at the finals).

Fixed regime B: region 5 most stressed (reversed stress_rates) and now most valuable (100x the rest).
"""
import numpy as np
import ac30_acquire as acq
import ac50_heterogeneous as a50
import ac38_variance as ac38

VALUES = (1.0, 1.0, 1.0, 1.0, 1.0, 100.0)   # region 5 critical
STRESS_MULT = 7
RATES = tuple(r * STRESS_MULT for r in reversed(acq.stress_rates()))   # region 5 highest stress

SCORING = tuple(range(9012, 9024))       # find OPT/WORST
ENG1 = tuple(range(4612, 4624))          # four-check family 1
ENG2 = tuple(range(4624, 4636))          # four-check family 2 (disjoint)


def rating(order, seeds=SCORING):
    return a50.rating(order, RATES, VALUES, seeds=seeds)


def climb_min(start, seeds=SCORING):
    cur = tuple(start); sc = rating(cur, seeds)
    while True:
        best, bs = cur, sc
        for cand in a50.asc.swaps(cur):
            s = rating(cand, seeds)
            if s < bs:
                best, bs = cand, s
        if best == cur:
            return cur, sc
        cur, sc = best, bs


def find_opt_worst(nstarts=12):
    starts = [tuple(int(x) for x in np.random.default_rng([s, 5501]).permutation(6)) for s in range(nstarts)]
    opts = [a50.climb(st, RATES, VALUES, seeds=SCORING) for st in starts]
    best = max(opts, key=lambda r: r[1])
    worsts = [climb_min(st) for st in starts]
    wst = min(worsts, key=lambda r: r[1])
    return best[0], best[1], wst[0], wst[1]


def four_check(opt, worst, seeds):
    do = [a50.run(opt, s, RATES, VALUES)['produced'] for s in seeds]
    dw = [a50.run(worst, s, RATES, VALUES)['produced'] for s in seeds]
    d = np.asarray([a - b for a, b in zip(do, dw)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(1 for s in seeds
               if a50.run(opt, s, RATES, VALUES)['dead'] or a50.run(worst, s, RATES, VALUES)['dead'])
    ceiling = 4.0 * sum(VALUES) * (a50.TICKS / a50.PRODUCTION_PERIOD)
    pinned = sum(1 for v in do if v >= ceiling - 1e-9)
    impaired = sum(1 for a, b in zip(do, dw) if b > a)
    return dict(p=res['p'], n=len(seeds), mean_diff=float(np.mean(d)),
                median_diff=float(np.median(d)), impaired=impaired, dead=dead,
                pinned=pinned, ceiling=ceiling, opt_mean=float(np.mean(do)))


if __name__ == '__main__':
    OPT, os, WORST, ws = find_opt_worst()
    print(f'OPT   = {OPT}  (scoring rating {os:.1f})')
    print(f'WORST = {WORST}  (scoring rating {ws:.1f})')
    print()
    for name, seeds in [('ENG1', ENG1), ('ENG2', ENG2)]:
        ck = four_check(OPT, WORST, seeds)
        ok = ck['p'] <= 0.01 and ck['impaired'] == 0 and ck['dead'] == 0 and ck['pinned'] == 0
        print(f'{name} ({seeds[0]}..{seeds[-1]}): p={ck["p"]:.4f} imp={ck["impaired"]} '
              f'dead={ck["dead"]} pinned={ck["pinned"]} median_diff={ck["median_diff"]:.0f} '
              f'opt_mean={ck["opt_mean"]:.0f}/{ck["ceiling"]:.0f} {"PASS" if ok else "FAIL"}')
    import json
    json.dump(dict(OPT=list(OPT), WORST=list(WORST), VALUES=VALUES, STRESS_MULT=STRESS_MULT,
                   RATES=RATES),
              open('/tmp/ac55_engineering.json', 'w'), indent=2)
