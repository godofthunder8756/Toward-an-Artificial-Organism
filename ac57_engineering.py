"""AC57 engineering: the reconciling value structure — load-bearing AND re-acquisition, both resolvable.

AC56 found the tension: concentrated value gives load-bearing (AC55) but negligible re-acquisition;
graded value (AC50) gives re-acquisition but weak load-bearing. The resolution, found here, is a
'concentrated head + graded tail': one critical region (100) with a graded tail (5..0.5) so that, under
regime A, the *future*-critical region (5, value 0.5) is lowest and the A-optimal order deprioritises it
— making the stale order neglect the new critical region under B.

This module finds the exact optima (12-start climbs) and four-checks BOTH effects on TWO disjoint
families. Engineering only: no protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac50_heterogeneous as a50
import ac38_variance as ac38

STRESS_MULT = 7
VALUES_A = (100.0, 5.0, 4.0, 3.0, 2.0, 0.5)
VALUES_B = tuple(reversed(VALUES_A))
RATES_A = tuple(r * STRESS_MULT for r in acq.stress_rates())
RATES_B = tuple(r * STRESS_MULT for r in reversed(acq.stress_rates()))

SCORING = tuple(range(9012, 9024))
ENG1 = tuple(range(4612, 4624))
ENG2 = tuple(range(4624, 4636))


def climb(rates, values, start, minimize=False, seeds=SCORING):
    cur = tuple(start)
    sc = a50.rating(cur, rates, values, seeds=seeds)
    while True:
        best, bs = cur, sc
        for cand in a50.asc.swaps(cur):
            s = a50.rating(cand, rates, values, seeds=seeds)
            if (s < bs if minimize else s > bs):
                best, bs = cand, s
        if best == cur:
            return cur, sc
        cur, sc = best, bs


def find_opt(rates, values, minimize=False, nstarts=12):
    starts = [tuple(int(x) for x in np.random.default_rng([s, 5701]).permutation(6)) for s in range(nstarts)]
    results = [climb(rates, values, st, minimize) for st in starts]
    return (min(results, key=lambda r: r[1]) if minimize else max(results, key=lambda r: r[1]))[0]


def effect(opt_b, other, seeds):
    a = [a50.run(opt_b, s, RATES_B, VALUES_B)['produced'] for s in seeds]
    b = [a50.run(other, s, RATES_B, VALUES_B)['produced'] for s in seeds]
    d = np.asarray([x - y for x, y in zip(a, b)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(1 for s in seeds
               if a50.run(opt_b, s, RATES_B, VALUES_B)['dead'] or a50.run(other, s, RATES_B, VALUES_B)['dead'])
    return dict(p=res['p'], median_diff=float(np.median(d)), impaired=sum(1 for x, y in zip(a, b) if y > x),
                dead=dead)


if __name__ == '__main__':
    print('finding optima (12-start climbs on scoring seeds)...')
    OPT_A = find_opt(RATES_A, VALUES_A)
    OPT_B = find_opt(RATES_B, VALUES_B)
    WORST_B = find_opt(RATES_B, VALUES_B, minimize=True)
    print(f'OPT_A   = {OPT_A}')
    print(f'OPT_B   = {OPT_B}')
    print(f'WORST_B = {WORST_B}')
    print()
    for name, seeds in [('ENG1', ENG1), ('ENG2', ENG2)]:
        re = effect(OPT_B, OPT_A, seeds)
        lb = effect(OPT_B, WORST_B, seeds)
        print(f'{name}: re-acq p={re["p"]:.4f} md={re["median_diff"]:.0f} imp={re["impaired"]} '
              f'dead={re["dead"]} | load p={lb["p"]:.4f} md={lb["median_diff"]:.0f} imp={lb["impaired"]}')
    import json
    json.dump(dict(OPT_A=list(OPT_A), OPT_B=list(OPT_B), WORST_B=list(WORST_B),
                   VALUES_A=VALUES_A, VALUES_B=VALUES_B, RATES_A=RATES_A, RATES_B=RATES_B,
                   STRESS_MULT=STRESS_MULT),
              open('/tmp/ac57_engineering.json', 'w'), indent=2)
