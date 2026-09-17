"""AC77 engineering: does a long-lived organism's own accumulated production signal
resolve the rule-value plateau?

Why this, now
-------------
AC73 (eac25e7) falsified the population premise: in the AC32/33 regime-B world a
population on single-life scoring caps at the same ~0.85 sites below the ceiling as
AC30's single-climber; only oracle (12-seed) scoring reaches the ceiling (0.09 gap).
The cause is measured, not guessed: the ceiling order (2,0,1,3,5,4) and a mediocre
order (0,1,2,3,4,5) differ by only ~0.25 sites on the oracle scale, while a single
life's snapshot score carries sd 0.94 -- the fine plateau is below the single-life
noise floor.

The open question (the prerequisite for content self-production): does a LONG-LIVED
organism accumulate enough *independent* environmental signal within one lifetime to
resolve the plateau? Before building any "better learner", measure whether the signal
exists to learn from.

What this measures
------------------
1. Whether the organism's own production signal (live-site count) accumulates
   independent samples over a long life, or settles to a seed-specific FIXED POINT
   (one sample per environment, however long the life).
2. Whether the fine ceiling-vs-mediocre gap (AC73's 0.25) is a stationary fact or an
   artifact of the 12-seed oracle.
3. Whether the coarse ranking (best vs worst, the bulk of the margin) survives the same
   measurement -- i.e. whether the world carries ANY self-directed signal.

This is engineering. No protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES_B = ac32.RATES_B
CEILING = ac32.DECLARED_OPTIMA['B'][0]          # (2,0,1,3,5,4), oracle 12.67
MEDIOCRE = (0, 1, 2, 3, 4, 5)                   # AC73's "mediocre"
WORST = (1, 0, 3, 2, 5, 4)                      # AC30's worst, 9.00 (regime A)
GOOD = (3, 4, 1, 5, 0, 2)                       # AC30's best (regime A), for coarse context

SEEDS = tuple(range(8400, 8400 + 400))          # disjoint from every frozen/engineering family
BURNIN = 8000                                    # fixed point reached well before this
HORIZON = 16000


def run_stats(order, seed):
    """One life to HORIZON, returning (snapshot@800, stationary mean over [BURNIN,HORIZON],
    live-count at burn-in, live-count at horizon, lost at burn-in, lost at horizon)."""
    w = acq.World(seed, rates=RATES_B)
    snap800 = None
    n_burn = None
    lost_burn = None
    acc = 0.0
    for t in range(1, HORIZON + 1):
        word = w.urgency()
        action = None
        for position in order:
            if word >> position & 1:
                action = position
                break
        w.tick(action)
        nlive = sum(1 for v in w.life if v > 0)
        if t == 800:
            snap800 = nlive
        if t == BURNIN:
            n_burn = nlive
            lost_burn = w.lost
        if t > BURNIN:
            acc += nlive
    stat = acc / (HORIZON - BURNIN)
    return snap800, stat, n_burn, nlive, lost_burn, w.lost


def measure(name, order):
    rows = np.array([run_stats(order, s) for s in SEEDS], dtype=np.float64)
    snap800, stat, n_burn, n_end, lost_burn, lost_end = rows.T
    return dict(
        name=name, order=order,
        snap800_mean=snap800.mean(), snap800_sd=snap800.std(ddof=1),
        stat_mean=stat.mean(), stat_sd=stat.std(ddof=1),
        # fixed-point structure
        n_burn_unique=np.unique(n_burn), n_end_unique=np.unique(n_end),
        fixed_fraction=float((n_burn == n_end).mean()),
        turnover_continues=float((lost_end > lost_burn).mean()),
        lost_burn_mean=lost_burn.mean(), lost_end_mean=lost_end.mean(),
    )


def main():
    print('--- order-level measurement (regime B, 400 seeds) ---')
    orders = [CEILING, MEDIOCRE, WORST, GOOD]
    res = {o: measure('', o) for o in orders}
    res = {('ceiling' if o == CEILING else 'mediocre' if o == MEDIOCRE
            else 'worst' if o == WORST else 'good'): measure('', o) for o in orders}
    hdr = f'{"order":>9s} {"snap@800":>10s} {"stat. mean":>11s} {"stat. sd":>9s} ' \
          f'{"fixed%":>7s} {"turnover%":>10s} {"end values":>12s}'
    print(hdr)
    for k in ('ceiling', 'mediocre', 'worst', 'good'):
        r = res[k]
        print(f'{k:>9s} {r["snap800_mean"]:>10.3f} {r["stat_mean"]:>11.3f} {r["stat_sd"]:>9.3f} '
              f'{r["fixed_fraction"]*100:>6.0f}% {r["turnover_continues"]*100:>9.0f}% '
              f'{list(map(int, r["n_end_unique"]))}')

    print('\n--- the fine gap (ceiling vs mediocre): does the 0.25 oracle gap replicate? ---')
    c = res['ceiling']
    m = res['mediocre']
    # paired (same-seed) differences
    cd = np.array([run_stats(CEILING, s) for s in SEEDS])
    md = np.array([run_stats(MEDIOCRE, s) for s in SEEDS])
    d_snap = cd[:, 0] - md[:, 0]
    d_stat = cd[:, 1] - md[:, 1]
    for label, d in (('snapshot@800', d_snap), ('stationary mean', d_stat)):
        se = d.std(ddof=1) / np.sqrt(len(d))
        print(f'  ceiling-minus-mediocre {label:16s}: mean {d.mean():+.3f}  sd {d.std(ddof=1):.3f}  '
              f'se {se:.3f}   (oracle claimed +0.25)')

    print('\n--- the coarse gap (ceiling vs worst): does the world still rank? ---')
    w = res['worst']
    d_snap = cd[:, 0] - np.array([run_stats(WORST, s)[0] for s in SEEDS])
    print(f'  ceiling stat.mean {c["stat_mean"]:.2f} vs worst stat.mean {w["stat_mean"]:.2f}  '
          f'= coarse gap {c["stat_mean"] - w["stat_mean"]:+.2f} sites')
    print(f'  snapshot@800 coarse gap (paired): mean {d_snap.mean():+.2f}')

    print('\n--- accumulation: is the stationary mean spread the fixed-point spread? ---')
    print(f'  ceiling  stationary sd {c["stat_sd"]:.3f} (fixed-point spread across seeds)')
    print(f'  mediocre stationary sd {m["stat_sd"]:.3f}')
    print(f'  turnover continues in {c["turnover_continues"]*100:.0f}% of ceiling lives '
          f'(lost {c["lost_burn_mean"]:.1f} -> {c["lost_end_mean"]:.1f})')


if __name__ == '__main__':
    main()
