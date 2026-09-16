"""AC48 (engineering): does concave (diminishing-returns) production yield a stable, graded
self-funded world?

The question
------------
AC47 showed the self-funded world (linear production ∝ population) cannot be both stable and graded:
stable configs saturate (order irrelevant), graded configs collapse (bimodal death). The death spiral is
the positive feedback: production ∝ population, so a stochastically-depleted population produces less,
renews less, and dies. The burst test confirmed this is structural (not stress variance).

The fix under test here: make production a CONCAVE function of population — per-site production is high
when the population is low (recovery from depletion) and falls as it grows (no runaway saturation). This
is the standard mechanism that turns "saturate or spiral" into a stable interior equilibrium, at which the
order can matter. This scans it. Prerequisite only: no protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac46_selfsufficiency as a46


class ConcaveWorld(a46.World):
    """Same world, but production is concave in the living population: N * (1 - N/CAP)."""

    def __init__(self, seed, rates=None, cap=60.0):
        super().__init__(seed, rates)
        self.cap = cap

    def tick(self, action):
        self.tick_count += 1
        for i in range(acq.SLOTS):
            if self.life[i] == 1:
                self.life[i] = 0
            elif self.life[i] > 1:
                self.life[i] -= 1
        if self.tick_count % a46.PRODUCTION_PERIOD == 0:
            n = sum(1 for v in self.life if v >= 1)
            # concave in n, normalized so production at n=24 equals the linear world's 24
            productive = n * (1.0 - n / self.cap) / (1.0 - 24.0 / self.cap)
            self.energy += productive
            self.produced += productive
        self.energy -= a46.DRAIN
        self.drained += a46.DRAIN
        acted = False
        if action is not None:
            seg = slice(action * acq.SITES, (action + 1) * acq.SITES)
            live = [i for i in range(acq.SITES) if self.life[seg.start + i] > 0]
            if live and self.energy >= a46.RENEW_ENERGY:
                most_urgent = min(live, key=lambda i: self.life[seg.start + i])
                self.energy -= a46.RENEW_ENERGY
                self.life[seg.start + most_urgent] = acq.CHILD_LIFE
                self.renewals += 1
                acted = True
            elif live:
                self.refusals += 1
        self.starved = self.starved + 1 if (action is not None and not acted) else 0
        self.environment_tick()
        if sum(1 for v in self.life if v > 0) < 1 or self.starved >= a46.STARVATION_TICKS:
            self.dead = True


def drive(order, seed, ticks, rates, cap):
    w = ConcaveWorld(seed, rates=rates, cap=cap)
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
    return sum(1 for v in w.life if v > 0), w.energy, w.dead


def stat(order, ticks, rates, cap, seeds):
    v = [drive(order, s, ticks, rates, cap) for s in seeds]
    return float(np.mean([x[0] for x in v])), float(np.mean([x[1] for x in v])), sum(1 for x in v if x[2])


if __name__ == '__main__':
    B = (0, 4, 1, 3, 2, 5)
    A = (4, 5, 1, 2, 0, 3)
    SEEDS = tuple(range(9000, 9012))
    a46.PRODUCTION_PERIOD = 4
    a46.STRESS_MULTIPLIER = 3
    rates_b = tuple(reversed(tuple(r * 3 for r in acq.stress_rates())))

    print(f'{"cap":>5} {"drain":>6} | {"B@300":>6} {"B@600":>6} {"B@900":>6} {"B@1500":>6} {"Bdead":>5} | {"A@600":>6} {"spread":>6}')
    found = []
    for cap in (48.0, 60.0, 80.0, 120.0):
        for drain in (2.0, 2.5, 3.0, 3.5, 4.0):
            a46.DRAIN = drain
            b300, _, _ = stat(B, 300, rates_b, cap, SEEDS)
            b600, _, _ = stat(B, 600, rates_b, cap, SEEDS)
            b900, _, _ = stat(B, 900, rates_b, cap, SEEDS)
            b1500, b_e, bd = stat(B, 1500, rates_b, cap, SEEDS)
            a600, _, ad = stat(A, 600, rates_b, cap, SEEDS)
            spread = b600 - a600
            stable = (not bd) and (b1500 >= b300 - 1.0) and b_e >= 0
            graded = spread >= 3.0
            print(f'{cap:>5} {drain:>6} | {b300:>6.2f} {b600:>6.2f} {b900:>6.2f} {b1500:>6.2f} {bd:>4}/12 | {a600:>6.2f} {spread:>6.1f}')
            if stable and graded:
                found.append((cap, drain, spread, bd))
    print()
    print('stable AND graded (spread>=3, 0 dead, non-declining):', found if found else 'NONE')
