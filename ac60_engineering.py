"""AC60 engineering: does the developmental function survive a seven-region domain?

AC59 measured that the order structure scales combinatorially (N=7 -> 5040 classes, 12.30 bits) and that
the rule format is the binding axis (9 slots). This module builds the seven-region world and measures
whether the two properties frozen at six positions -- load-bearing (AC55) and re-acquisition (AC57) --
survive the wider domain. Engineering only: no protocol, no final seeds, no claim.

World: AC50's World generalized to seven regions (7 stress rates, 7 values with a concentrated head +
graded tail), regime A (region 0 critical) and B (region 6 critical).
"""
import numpy as np
import ac38_variance as ac38

N = 7
SITES = 4
SLOTS = N * SITES
CHILD_LIFE = 64
URGENT = 16
STRESS_MULT = 7
PRODUCTION_PERIOD = 4
DRAIN = 2.0
RENEW_ENERGY = 5
STARVATION_TICKS = 60
BURST_PROBABILITY = 0.03
BURST_WIDTH = 3
TICKS = 600
HORIZON_TICKS = 1500

STRESS7 = (0.020, 0.016, 0.012, 0.009, 0.006, 0.004, 0.003)
VALUES_A = (100.0, 6.0, 5.0, 4.0, 3.0, 2.0, 0.5)
VALUES_B = tuple(reversed(VALUES_A))
RATES_A = tuple(r * STRESS_MULT for r in STRESS7)
RATES_B = tuple(reversed(RATES_A))

SCORING = tuple(range(9012, 9024))
ENG1 = tuple(range(4612, 4624))
ENG2 = tuple(range(4624, 4636))


class World7:
    def __init__(self, seed, rates, values):
        self.rng = np.random.default_rng([seed, 3701])
        self.rates = rates
        self.values = values
        self.life = [CHILD_LIFE] * SLOTS
        self.energy = 48
        self.tick_count = 0
        self.starved = 0
        self.dead = False
        self.renewals = 0
        self.refusals = 0
        self.produced = 0.0

    def urgency(self):
        word = 0
        for k in range(N):
            seg = self.life[k * SITES:(k + 1) * SITES]
            if any(0 < v <= URGENT for v in seg):
                word |= 1 << k
        return word

    def _stress_one(self, k):
        seg = slice(k * SITES, (k + 1) * SITES)
        occupied = [i for i in range(SITES) if self.life[seg.start + i] > 0]
        if occupied:
            i = occupied[int(self.rng.integers(0, len(occupied)))]
            self.life[seg.start + i] = URGENT

    def environment_tick(self):
        for k, rate in enumerate(self.rates):
            if self.rng.random() < rate:
                self._stress_one(k)
        if self.rng.random() < BURST_PROBABILITY:
            weights = np.array(self.rates)
            weights = weights / weights.sum()
            for k in self.rng.choice(N, size=BURST_WIDTH, replace=False, p=weights):
                self._stress_one(int(k))

    def tick(self, action):
        self.tick_count += 1
        for i in range(SLOTS):
            if self.life[i] == 1:
                self.life[i] = 0
            elif self.life[i] > 1:
                self.life[i] -= 1
        if self.tick_count % PRODUCTION_PERIOD == 0:
            val = sum(self.values[k] * sum(1 for v in self.life[k * SITES:(k + 1) * SITES] if v >= 1)
                      for k in range(N))
            self.energy += val
            self.produced += val
        self.energy -= DRAIN
        acted = False
        if action is not None:
            seg = slice(action * SITES, (action + 1) * SITES)
            live = [i for i in range(SITES) if self.life[seg.start + i] > 0]
            if live and self.energy >= RENEW_ENERGY:
                most_urgent = min(live, key=lambda i: self.life[seg.start + i])
                self.energy -= RENEW_ENERGY
                self.life[seg.start + most_urgent] = CHILD_LIFE
                self.renewals += 1
                acted = True
            elif live:
                self.refusals += 1
        self.starved = self.starved + 1 if (action is not None and not acted) else 0
        self.environment_tick()
        if sum(1 for v in self.life if v > 0) < 1 or self.starved >= STARVATION_TICKS:
            self.dead = True


def run(order, seed, rates, values, ticks=TICKS):
    w = World7(seed, rates, values)
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
    return dict(produced=w.produced, dead=w.dead)


def rating(order, rates, values, seeds=SCORING, ticks=TICKS):
    return float(np.mean([run(order, s, rates, values, ticks)['produced'] for s in seeds]))


def swaps(order):
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            cand = list(order)
            cand[i], cand[j] = cand[j], cand[i]
            yield tuple(cand)


def climb(rates, values, start, minimize=False, seeds=SCORING):
    cur = tuple(start)
    sc = rating(cur, rates, values, seeds)
    while True:
        best, bs = cur, sc
        for cand in swaps(cur):
            s = rating(cand, rates, values, seeds)
            if (s < bs if minimize else s > bs):
                best, bs = cand, s
        if best == cur:
            return cur, sc
        cur, sc = best, bs


def find_opt(rates, values, minimize=False, nstarts=8):
    starts = [tuple(int(x) for x in np.random.default_rng([s, 6001]).permutation(N)) for s in range(nstarts)]
    results = [climb(rates, values, st, minimize) for st in starts]
    return (min(results, key=lambda r: r[1]) if minimize else max(results, key=lambda r: r[1]))[0]


def effect(opt_b, other, seeds):
    a = [run(opt_b, s, RATES_B, VALUES_B)['produced'] for s in seeds]
    b = [run(other, s, RATES_B, VALUES_B)['produced'] for s in seeds]
    d = np.asarray([x - y for x, y in zip(a, b)], dtype=float)
    res = ac38.sign_flip_test(list(d))
    dead = sum(1 for s in seeds
               if run(opt_b, s, RATES_B, VALUES_B)['dead'] or run(other, s, RATES_B, VALUES_B)['dead'])
    return dict(p=res['p'], median=float(np.median(d)), impaired=sum(1 for x, y in zip(a, b) if y > x),
                dead=dead, opt_mean=float(np.mean(a)), other_mean=float(np.mean(b)))


if __name__ == '__main__':
    print(f'seven-region world: N={N}, values_A={VALUES_A}')
    print('finding optima (8-start climbs)...')
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
        print(f'{name}: load p={lb["p"]:.4f} md={lb["median"]:.0f} imp={lb["impaired"]} dead={lb["dead"]} '
              f'| re-acq p={re["p"]:.4f} md={re["median"]:.0f} imp={re["impaired"]} dead={re["dead"]}')
        print(f'      opt={lb["opt_mean"]:.0f} worst={lb["other_mean"]:.0f} stale={re["other_mean"]:.0f}')
    import json
    json.dump(dict(OPT_A=list(OPT_A), OPT_B=list(OPT_B), WORST_B=list(WORST_B), VALUES_A=VALUES_A,
                   VALUES_B=VALUES_B, STRESS7=STRESS7),
              open('/tmp/ac60_engineering.json', 'w'), indent=2)
