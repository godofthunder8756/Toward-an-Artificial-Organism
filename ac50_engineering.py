"""AC50 engineering: characterize the regime-dependent heterogeneous-value re-acquisition effect.

The design (from AC49)
----------------------
Site value is regime-dependent: under regime A sites in region 0 are most valuable (5.0 down to 0.5);
under regime B the value pattern reverses (region 5 most valuable). Stress also reverses (RATES_B =
reversed(RATES_A)), so the high-value region is always the high-stress region. Re-acquisition therefore
means re-prioritizing to the new regime's high-value region. Endpoint: cumulative value-weighted
production under B (horizon-robust, like AC43's ledger totals).

This measures, before any protocol: the value-optimal orders under A and B, the paired learner-vs-keeper
effect (12 individuals), the sign-flip test, and the two properties AC47/AC48 made the point --
stability (0 dead) and horizon-robustness (steady state, not a collapse transient).
"""
import json
import numpy as np
import ac30_acquire as acq
import ac49_heterogeneous as a49
import ac38_variance as ac38

VALUES_A = (5.0, 4.0, 3.0, 2.0, 1.0, 0.5)
VALUES_B = tuple(reversed(VALUES_A))
RATES_A = tuple(r * 3 for r in acq.stress_rates())
RATES_B = tuple(reversed(RATES_A))


class RegimeWorld(a49.HeteroWorld):
    def __init__(self, seed, rates, values):
        a49.HeteroWorld.__init__(self, seed, rates)
        self.values = values

    def tick(self, action):
        self.tick_count += 1
        for i in range(acq.SLOTS):
            if self.life[i] == 1:
                self.life[i] = 0
            elif self.life[i] > 1:
                self.life[i] -= 1
        if self.tick_count % a49.a46.PRODUCTION_PERIOD == 0:
            val = sum(self.values[k] * sum(1 for v in self.life[k * 4:(k + 1) * 4] if v >= 1)
                      for k in range(6))
            self.energy += val
            self.produced += val
        self.energy -= a49.a46.DRAIN
        self.drained += a49.a46.DRAIN
        acted = False
        if action is not None:
            seg = slice(action * 4, (action + 1) * 4)
            live = [i for i in range(4) if self.life[seg.start + i] > 0]
            if live and self.energy >= a49.a46.RENEW_ENERGY:
                mu = min(live, key=lambda i: self.life[seg.start + i])
                self.energy -= a49.a46.RENEW_ENERGY
                self.life[seg.start + mu] = acq.CHILD_LIFE
                self.renewals += 1
                acted = True
            elif live:
                self.refusals += 1
        self.starved = self.starved + 1 if (action is not None and not acted) else 0
        self.environment_tick()
        if sum(1 for v in self.life if v > 0) < 1 or self.starved >= a49.a46.STARVATION_TICKS:
            self.dead = True


def run(order, seed, rates, values, ticks):
    w = RegimeWorld(seed, rates, values)
    for _ in range(ticks):
        if w.dead:
            break
        word = w.urgency()
        action = None
        for pos in order:
            if word >> pos & 1:
                action = pos
                break
        w.tick(action)
    return w.produced, w.dead


def rating(order, rates, values, seeds, ticks=600):
    out = [run(order, s, rates, values, ticks) for s in seeds]
    return float(np.mean([o[0] for o in out]))


def climb(start, rates, values, seeds):
    cur = tuple(start)
    score = rating(cur, rates, values, seeds)
    while True:
        best = cur
        bs = score
        n = len(cur)
        for i in range(n):
            for j in range(i + 1, n):
                c = list(cur)
                c[i], c[j] = c[j], c[i]
                c = tuple(c)
                s = rating(c, rates, values, seeds)
                if s > bs:
                    best, bs = c, s
        if best == cur:
            return cur, score
        cur, score = best, bs


if __name__ == '__main__':
    a49.a46.DRAIN = 2.0
    a49.a46.PRODUCTION_PERIOD = 4
    SEEDS = tuple(range(9000, 9012))
    CLIMB_SEEDS = tuple(range(9000, 9008))

    start = tuple(int(x) for x in np.random.default_rng([4700, 3701]).permutation(6))
    optA, sA = climb(start, RATES_A, VALUES_A, CLIMB_SEEDS)
    optB, sB = climb(start, RATES_B, VALUES_B, CLIMB_SEEDS)
    print(f'value-optimal under A: {optA}  (score {sA:.0f})')
    print(f'value-optimal under B: {optB}  (score {sB:.0f})')

    # paired learner (optB) vs keeper (optA), scored under B, 12 individuals
    rows = []
    for s in SEEDS:
        lp, ld = run(optB, s, RATES_B, VALUES_B, 600)
        kp, kd = run(optA, s, RATES_B, VALUES_B, 600)
        rows.append((lp, kp, ld, kd))
    d = np.asarray([r[0] - r[1] for r in rows], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(1 for r in rows if r[2] or r[3])
    print(f'\npaired (12 individuals), learner {optB} vs keeper {optA} under B:')
    print(f'  differences: {[round(x) for x in d]}')
    print(f'  sign-flip: n={res["n"]} mean={res["observed"]:.0f} p={res["p"]:.5f} '
          f'impaired={np.mean(d > 0):.3f}')
    print(f'  dead seeds (either arm): {dead}/12')
    print(f'  learner mean {np.mean([r[0] for r in rows]):.0f}  keeper mean '
          f'{np.mean([r[1] for r in rows]):.0f}  ratio {np.mean([r[0] for r in rows])/np.mean([r[1] for r in rows]):.3f}')

    # horizon-robustness: is production steady-state (linear in time)?
    lb = [run(optB, s, RATES_B, VALUES_B, t)[0] for s in SEEDS for t in (600, 1500)]
    prod600 = np.mean(lb[0::2])
    prod1500 = np.mean(lb[1::2])
    print(f'\nhorizon-robustness: optB production @600 {prod600:.0f}  @1500 {prod1500:.0f}  '
          f'ratio {prod1500/prod600:.2f} (linear steady-state would be 2.50)')

    json.dump(dict(optA=list(optA), optB=list(optB),
                   differences=[float(x) for x in d], p=res['p'], dead=dead,
                   learner_mean=float(np.mean([r[0] for r in rows])),
                   keeper_mean=float(np.mean([r[1] for r in rows]))),
              open('/tmp/ac50_engineering.json', 'w'), indent=2)
