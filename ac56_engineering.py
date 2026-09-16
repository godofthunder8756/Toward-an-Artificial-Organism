"""AC56 engineering: is the six-position order acquirable and re-acquirable? Two-family four-check.

AC55 proved the order load-bearing in the scaled body. AC56 asks the developmental-function arc's own
question (AC28's stated next step): can the order be ACQUIRED (search finds the value-optimal order),
RETAINED (held in a register), and RE-ACQUIRED (release + re-search after a regime change beats keeping
the stale order)?

World: AC55's concentrated-value scaled body, with TWO regimes (A: region 0 critical; B: region 5
critical, reversing with the stress). The contrast: after a regime A->B flip, a learner that releases
and re-acquires under B vs one that keeps the A-optimal order (stale under B).

Engineering only: no protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac50_heterogeneous as a50
import ac38_variance as ac38

STRESS_MULT = 7
VALUES_A = (100.0, 1.0, 1.0, 1.0, 1.0, 1.0)
VALUES_B = (1.0, 1.0, 1.0, 1.0, 1.0, 100.0)
RATES_A = tuple(r * STRESS_MULT for r in acq.stress_rates())          # region 0 highest stress
RATES_B = tuple(r * STRESS_MULT for r in reversed(acq.stress_rates())) # region 5 highest stress

SCORING = tuple(range(9012, 9024))
ENG1 = tuple(range(4612, 4624))
ENG2 = tuple(range(4624, 4636))


def find_opt(rates, values, nstarts=12):
    starts = [tuple(int(x) for x in np.random.default_rng([s, 5601]).permutation(6)) for s in range(nstarts)]
    opts = [a50.climb(st, rates, values, seeds=SCORING) for st in starts]
    return max(opts, key=lambda r: r[1])[0]


def contrast(opt_a, opt_b, seeds):
    """learner (re-acquired under B) vs no_release (stale opt_a), scored under regime B."""
    lr = [a50.run(opt_b, s, RATES_B, VALUES_B)['produced'] for s in seeds]
    nr = [a50.run(opt_a, s, RATES_B, VALUES_B)['produced'] for s in seeds]
    d = np.asarray([a - b for a, b in zip(lr, nr)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(1 for s in seeds
               if a50.run(opt_b, s, RATES_B, VALUES_B)['dead'] or a50.run(opt_a, s, RATES_B, VALUES_B)['dead'])
    impaired = sum(1 for a, b in zip(lr, nr) if b > a)
    return dict(p=res['p'], median_diff=float(np.median(d)), mean_diff=float(np.mean(d)),
                impaired=impaired, dead=dead, learner_mean=float(np.mean(lr)),
                no_release_mean=float(np.mean(nr)))


if __name__ == '__main__':
    print('finding OPT_A and OPT_B (12-start climbs on scoring seeds)...')
    OPT_A = find_opt(RATES_A, VALUES_A)
    OPT_B = find_opt(RATES_B, VALUES_B)
    print(f'OPT_A = {OPT_A}  (region 0 critical)')
    print(f'OPT_B = {OPT_B}  (region 5 critical)')
    print()
    for name, seeds in [('ENG1', ENG1), ('ENG2', ENG2)]:
        ck = contrast(OPT_A, OPT_B, seeds)
        ok = ck['p'] <= 0.01 and ck['impaired'] == 0 and ck['dead'] == 0
        print(f'{name}: p={ck["p"]:.4f} imp={ck["impaired"]} dead={ck["dead"]} '
              f'median_diff={ck["median_diff"]:.0f} learner={ck["learner_mean"]:.0f} '
              f'no_release={ck["no_release_mean"]:.0f} {"PASS" if ok else "FAIL"}')
    import json
    json.dump(dict(OPT_A=list(OPT_A), OPT_B=list(OPT_B), VALUES_A=VALUES_A, VALUES_B=VALUES_B,
                   RATES_A=RATES_A, RATES_B=RATES_B, STRESS_MULT=STRESS_MULT),
              open('/tmp/ac56_engineering.json', 'w'), indent=2)
