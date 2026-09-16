"""AC54 engineering: is the six-region order load-bearing? (AC40 four-check before the protocol.)

Claim to be frozen: in the scaled body (six regions, repair renewal, value-weighted production, a fixed
stress/value regime), the six-position order is load-bearing -- the value-optimal order produces
significantly more value than the value-worst order, at a stable equilibrium, graded and resolvable.

This module measures the four checks (resolvability, effect size, headroom, stability) and finds the
declared OPT (max) and WORST (min) orders, on engineering seeds disjoint from any final seed. Reuses
AC50's verified World mechanics, fixed to regime B (region 5 most valuable).
"""
import numpy as np
import ac50_heterogeneous as a50
import ac38_variance as ac38

RATES = a50.RATES_B
VALUES = a50.VALUES_B
TICKS = a50.TICKS
HORIZON = a50.HORIZON_TICKS
ENG_SEEDS = tuple(range(4612, 4624))     # engineering, disjoint from AC50 4600-4611
SCORING = tuple(range(9012, 9024))       # scoring, disjoint from AC50 9000-9011


def rating(order, seeds=SCORING, ticks=TICKS):
    return a50.rating(order, RATES, VALUES, seeds=seeds, ticks=ticks)


def climb_min(start, seeds=SCORING):
    """Steepest descent to the value-WORST order."""
    cur = tuple(start)
    sc = rating(cur, seeds)
    while True:
        best, bs = cur, sc
        for cand in a50.asc.swaps(cur):
            s = rating(cand, seeds)
            if s < bs:
                best, bs = cand, s
        if best == cur:
            return cur, sc
        cur, sc = best, bs


def climb_max(start, seeds=SCORING):
    return a50.climb(start, RATES, VALUES, seeds=seeds)


def four_check(opt, worst, seeds=ENG_SEEDS):
    do = [a50.run(opt, s, RATES, VALUES)['produced'] for s in seeds]
    dw = [a50.run(worst, s, RATES, VALUES)['produced'] for s in seeds]
    d = np.asarray([a - b for a, b in zip(do, dw)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(1 for s in seeds
               if a50.run(opt, s, RATES, VALUES)['dead'] or a50.run(worst, s, RATES, VALUES)['dead'])
    # ceiling: all 24 sites alive all ticks -> production = 4 * sum(values) * (ticks/period)
    period = a50.PRODUCTION_PERIOD
    ceiling = 4.0 * sum(VALUES) * (TICKS / period)
    opt_frac_ceiling = float(np.mean(do)) / ceiling
    worst_frac_ceiling = float(np.mean(dw)) / ceiling
    return dict(
        n=len(seeds), p=res['p'], resolved=res['p'] <= 0.01 and len(seeds) >= 8,
        mean_opt=float(np.mean(do)), mean_worst=float(np.mean(dw)),
        median_diff=float(np.median(d)), mean_diff=float(np.mean(d)),
        impaired=float(np.mean([1 if w > o else 0 for o, w in zip(do, dw)])),
        per_individual=list(d), dead=dead,
        ceiling=ceiling, opt_frac_ceiling=opt_frac_ceiling, worst_frac_ceiling=worst_frac_ceiling,
    )


if __name__ == '__main__':
    # find OPT and WORST via 24-start climbs on the scoring seeds
    starts = [tuple(int(x) for x in np.random.default_rng([s, 5402]).permutation(6)) for s in range(24)]
    opts = [climb_max(st) for st in starts]
    best = max(opts, key=lambda r: r[1])
    worsts = [climb_min(st) for st in starts]
    wst = min(worsts, key=lambda r: r[1])
    OPT, WORST = best[0], wst[0]
    print(f'OPT  = {OPT}  (scoring rating {best[1]:.1f})')
    print(f'WORST= {WORST}  (scoring rating {wst[1]:.1f})')
    print()
    ck = four_check(OPT, WORST)
    print('four-check (engineering seeds %d..%d):' % (ENG_SEEDS[0], ENG_SEEDS[-1]))
    for k, v in ck.items():
        if k != 'per_individual':
            print(f'  {k:22s} {v}')
    print(f'  per-individual diffs: {[round(x,1) for x in ck["per_individual"]]}')
    # horizon robustness: optimal production at 1500 vs 600
    o600 = np.mean([a50.run(OPT, s, RATES, VALUES, ticks=TICKS)['produced'] for s in SCORING])
    o1500 = np.mean([a50.run(OPT, s, RATES, VALUES, ticks=HORIZON)['produced'] for s in SCORING])
    print(f'  horizon: production@1500 / @600 = {o1500/o600:.3f} (linear steady state = 2.50)')
    import json
    json.dump(dict(OPT=list(OPT), WORST=list(WORST), four_check=ck, horizon_ratio=o1500/o600),
              open('/tmp/ac54_engineering.json', 'w'), indent=2)
