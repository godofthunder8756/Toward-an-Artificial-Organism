"""AC62 engineering: repair + re-acquisition beats repair-only under threshold-crossing corruption.

AC61 established that register repair is preventive, not curative: it restores bits to their CURRENT
majority, so once corruption flips a bit's majority, repair freezes the wrong order. The consequence:
repair (AC58) and re-acquisition (AC57) are complementary. This module measures that complementarity:
under a corruption regime where intermittent repair allows the majority threshold to be crossed, an
organism that ALSO re-acquires (re-writes the register to the re-searched order) retains more value than
one that only repairs. Engineering only: no protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac29_register as reg
import ac50_heterogeneous as a50
import ac38_variance as ac38

STRESS_MULT = 7
VALUES_B = (0.5, 2.0, 3.0, 4.0, 5.0, 100.0)
RATES_B = tuple(r * STRESS_MULT for r in reversed(acq.stress_rates()))
OPT_B = (5, 1, 2, 4, 3, 0)
TICKS = a50.TICKS

DAMAGE_RATE = 0.005
REPAIR_EVERY = 50          # intermittent: corruption can cross the threshold between repairs
REACQUIRE_EVERY = 100      # re-write the register to the re-searched order
REPAIR_BUDGET = 10


def run(seed, arm, rate=DAMAGE_RATE):
    rng = np.random.default_rng([seed, 6201])
    register = reg.Register()
    register.write(reg.lehmer(OPT_B))
    w = a50.World(seed, RATES_B, VALUES_B)
    for t in range(TICKS):
        if w.dead:
            break
        register.damage(rng, rate)
        if t % REPAIR_EVERY == 0 and t > 0:
            register.repair(REPAIR_BUDGET)
        if arm == 'repair_reacquire' and t % REACQUIRE_EVERY == 0 and t > 0:
            register.write(reg.lehmer(OPT_B))   # re-search result: the recovered order
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


def contrast(seeds):
    a = [run(s, 'repair_reacquire')['produced'] for s in seeds]
    b = [run(s, 'repair_only')['produced'] for s in seeds]
    d = np.asarray([x - y for x, y in zip(a, b)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(1 for s in seeds if run(s, 'repair_reacquire')['dead'] or run(s, 'repair_only')['dead'])
    return dict(p=res['p'], median=float(np.median(d)), mean=float(np.mean(d)),
                impaired=sum(1 for x, y in zip(a, b) if y > x), dead=dead,
                reacquire_mean=float(np.mean(a)), repair_mean=float(np.mean(b)))


if __name__ == '__main__':
    ENG1 = tuple(range(4612, 4624))
    ENG2 = tuple(range(4624, 4636))
    print(f'DAMAGE_RATE={DAMAGE_RATE}, REPAIR_EVERY={REPAIR_EVERY}, REACQUIRE_EVERY={REACQUIRE_EVERY}')
    for name, seeds in [('ENG1', ENG1), ('ENG2', ENG2)]:
        c = contrast(seeds)
        print(f'{name}: p={c["p"]:.4f} md={c["median"]:.0f} imp={c["impaired"]} dead={c["dead"]} '
              f'reacquire={c["reacquire_mean"]:.0f} repair_only={c["repair_mean"]:.0f}')
