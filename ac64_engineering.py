"""AC64 engineering: repair + re-acquisition beats repair-only under corruption, at URGENT=4.

AC63 found the grace period (URGENT window) is the structural control on corruption's cost: at URGENT=4
corruption is costly (a random order loses ~65% of value), while at URGENT=16 it is cheap. This module
measures the complementarity AC61 identified, at URGENT=4, with AC62's single-disruption design:
a corruption event flips the register's majority; repair-only freezes the corrupted order, re-acquire
re-searches and recovers. Engineering only: no protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac29_register as reg
import ac50_heterogeneous as a50
import ac38_variance as ac38

acq.URGENT = 4                     # AC63's operating point: corruption is costly
URGENT = 4

STRESS_MULT = 7
VALUES_B = (0.5, 2.0, 3.0, 4.0, 5.0, 100.0)          # region 5 critical
RATES_B = tuple(r * STRESS_MULT for r in acq.stress_rates())   # region 5 LOW stress (rare-urgent)
TICKS = a50.TICKS
DISRUPT_TICK = 300
CORRUPT_RATE = 0.5

SCORING = tuple(range(9012, 9024))
ENG1 = tuple(range(4612, 4624))
ENG2 = tuple(range(4624, 4636))


def climb(rates, values, start, seeds=SCORING):
    cur = tuple(start)
    sc = a50.rating(cur, rates, values, seeds=seeds)
    while True:
        best, bs = cur, sc
        for cand in a50.asc.swaps(cur):
            s = a50.rating(cand, rates, values, seeds=seeds)
            if s > bs:
                best, bs = cand, s
        if best == cur:
            return cur, sc
        cur, sc = best, bs


def find_opt(nstarts=8):
    starts = [tuple(int(x) for x in np.random.default_rng([s, 6401]).permutation(6)) for s in range(nstarts)]
    return max([climb(RATES_B, VALUES_B, st) for st in starts], key=lambda r: r[1])[0]


def run(seed, arm, opt_b):
    rng = np.random.default_rng([seed, 6402])
    register = reg.Register()
    register.write(reg.lehmer(opt_b))
    w = a50.World(seed, RATES_B, VALUES_B)
    for t in range(TICKS):
        if w.dead:
            break
        if t == DISRUPT_TICK and arm != 'protected':
            register.damage(rng, CORRUPT_RATE)
            if arm == 'reacquire':
                found, _ = climb(RATES_B, VALUES_B,
                                 tuple(int(x) for x in np.random.default_rng([seed, 6403]).permutation(6)))
                register.write(reg.lehmer(found))
            elif arm == 'repair_only':
                register.repair(10)
        elif t > DISRUPT_TICK and arm != 'protected':
            register.damage(rng, 0.001)
            register.repair(10)
        order = register.read()
        word = w.urgency()
        action = None
        if order is not None:
            for pos in order:
                if word >> pos & 1:
                    action = pos
                    break
        w.tick(action)
    return dict(produced=w.produced, dead=w.dead)


def contrast(opt_b, seeds):
    re = [run(s, 'reacquire', opt_b) for s in seeds]
    ro = [run(s, 'repair_only', opt_b) for s in seeds]
    pr = [run(s, 'protected', opt_b) for s in seeds]
    d = np.asarray([a['produced'] - b['produced'] for a, b in zip(re, ro)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    retention = all(a['produced'] == b['produced'] for a, b in zip(re, pr))
    dead = sum(1 for s in seeds if any(run(s, arm, opt_b)['dead'] for arm in ('protected', 'reacquire', 'repair_only')))
    return dict(p=res['p'], median=float(np.median(d)), mean=float(np.mean(d)),
                impaired=sum(1 for a, b in zip(re, ro) if b['produced'] > a['produced']),
                dead=dead, retention=retention,
                reacquire=float(np.mean([o['produced'] for o in re])),
                repair_only=float(np.mean([o['produced'] for o in ro])),
                protected=float(np.mean([o['produced'] for o in pr])))


if __name__ == '__main__':
    print(f'URGENT={URGENT}, critical region low-stress, finding OPT_B...')
    OPT_B = find_opt()
    print(f'OPT_B = {OPT_B}')
    print()
    for name, seeds in [('ENG1', ENG1), ('ENG2', ENG2)]:
        c = contrast(OPT_B, seeds)
        ok = c['p'] <= 0.01 and c['impaired'] == 0 and c['dead'] == 0 and c['retention']
        print(f'{name}: p={c["p"]:.4f} md={c["median"]:.0f} imp={c["impaired"]} dead={c["dead"]} '
              f'retention={c["retention"]} | reacquire={c["reacquire"]:.0f} '
              f'repair_only={c["repair_only"]:.0f} protected={c["protected"]:.0f} {"PASS" if ok else "FAIL"}')
    import json
    json.dump(dict(OPT_B=list(OPT_B), URGENT=URGENT, VALUES_B=VALUES_B, RATES_B=RATES_B),
              open('/tmp/ac64_engineering.json', 'w'), indent=2)
