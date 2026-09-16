"""AC58 engineering: does repair retain the acquired order under corruption? Two-family four-check.

AC43 froze the maintenance line with corruption ABSENT (reg_rate=0 -- AC14's integrity channel off by
construction). AC57 froze the developmental line (the six-position order is load-bearing and
re-acquirable). AC58 joins them: the acquired order is held in a replica-encoded register that is
CORRUPTED over the run, and the question is whether paying to REPAIR it retains the acquired function
better than leaving it to degrade.

World: AC57's scaled body (regime B, concentrated head + graded tail), with the order read back from the
register each tick. Arms: protected (no damage, ceiling), repaired (damage + repair each tick at an
energy cost), unrepaired (damage only). Engineering only: no protocol, no final seeds, no claim.
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

DAMAGE_RATE = 0.005     # per replica per tick
REPAIR_COST = 1         # energy per repair call
REPAIR_BUDGET = 10      # bits fixable per call (all)


def run_register(seed, arm, rate=DAMAGE_RATE):
    rng = np.random.default_rng([seed, 5801])
    register = reg.Register()
    register.write(reg.lehmer(OPT_B))
    w = a50.World(seed, RATES_B, VALUES_B)
    for _ in range(TICKS):
        if w.dead:
            break
        if arm == 'repaired':
            register.damage(rng, rate)
            if w.energy >= REPAIR_COST:
                register.repair(REPAIR_BUDGET)
                w.energy -= REPAIR_COST
        elif arm == 'unrepaired':
            register.damage(rng, rate)
        # 'protected': no damage
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


def contrast(arm_a, arm_b, seeds):
    a = [run_register(s, arm_a)['produced'] for s in seeds]
    b = [run_register(s, arm_b)['produced'] for s in seeds]
    d = np.asarray([x - y for x, y in zip(a, b)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(1 for s in seeds if run_register(s, arm_a)['dead'] or run_register(s, arm_b)['dead'])
    return dict(p=res['p'], median=float(np.median(d)), mean=float(np.mean(d)),
                impaired=sum(1 for x, y in zip(a, b) if y > x), dead=dead)


if __name__ == '__main__':
    ENG1 = tuple(range(4612, 4624))
    ENG2 = tuple(range(4624, 4636))
    print(f'DAMAGE_RATE={DAMAGE_RATE}, REPAIR_COST={REPAIR_COST}, budget={REPAIR_BUDGET}')
    for name, seeds in [('ENG1', ENG1), ('ENG2', ENG2)]:
        # repaired vs unrepaired (the claim)
        c = contrast('repaired', 'unrepaired', seeds)
        # repaired vs protected (the cost of repair vs no corruption)
        cp = contrast('protected', 'repaired', seeds)
        # unrepaired vs protected (the cost of corruption)
        cu = contrast('protected', 'unrepaired', seeds)
        print(f'{name}: repaired-vs-unrepaired p={c["p"]:.4f} md={c["median"]:.0f} imp={c["impaired"]} '
              f'dead={c["dead"]} | prot-rep md={cp["median"]:.0f} | prot-unrep md={cu["median"]:.0f}')
