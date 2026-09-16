"""AC49 (engineering): heterogeneous site value -- can the order grade a stable self-funded world?

The question
------------
AC47/AC48 delimited the self-funded world: the order's only lever (which site to renew) moves the
outcome only under scarcity, and scarcity in self-funding is the death regime -- so the graded region
is a transient of collapse, under every production shape and stress regime tested.

The one untested fix changes *what the order acts on* rather than the world dynamics: make sites
**heterogeneous in production value**, so that under a scarcity of *renewal action* (one renewal per
tick, energy abundant, no death spiral) the order determines *which* sites survive, and a good order
keeps the high-value ones. The endpoint is **cumulative value-weighted production** (horizon-robust,
like AC43's ledger totals), not a terminal site count.

This scans that world. Prerequisite only: no protocol, no final seeds, no claim.
"""
import numpy as np
import ac30_acquire as acq
import ac46_selfsufficiency as a46

REGION_VALUES = (5.0, 4.0, 3.0, 2.0, 1.0, 0.5)   # region 0 is worth 10x region 5


class HeteroWorld(a46.World):
    """Same world, but production is the sum of each living site's region value, not a site count."""

    def tick(self, action):
        self.tick_count += 1
        for i in range(acq.SLOTS):
            if self.life[i] == 1:
                self.life[i] = 0
            elif self.life[i] > 1:
                self.life[i] -= 1
        if self.tick_count % a46.PRODUCTION_PERIOD == 0:
            value = 0.0
            for k in range(acq.REGIONS):
                seg = self.life[k * acq.SITES:(k + 1) * acq.SITES]
                value += REGION_VALUES[k] * sum(1 for v in seg if v >= 1)
            self.energy += value
            self.produced += value
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


def drive(order, seed, ticks, rates):
    w = HeteroWorld(seed, rates=rates)
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
    return dict(pop=sum(1 for v in w.life if v > 0), produced=w.produced,
                energy=w.energy, dead=w.dead)


def stat(order, ticks, rates, seeds):
    v = [drive(order, s, ticks, rates) for s in seeds]
    return (float(np.mean([x['produced'] for x in v])),
            float(np.mean([x['pop'] for x in v])),
            sum(1 for x in v if x['dead']))


if __name__ == '__main__':
    B = (0, 4, 1, 3, 2, 5)
    A = (4, 5, 1, 2, 0, 3)
    SEEDS = tuple(range(9000, 9012))
    a46.PRODUCTION_PERIOD = 4

    print(f'{"sm":>3} {"drain":>6} | {"Bprod@600":>9} {"Bprod@1500":>10} {"Bdead":>5} | '
          f'{"Aprod@600":>9} {"ratio":>6} {"Bpop@1500":>9}')
    found = []
    for sm in (3, 4, 5, 6, 8):
        rates_b = tuple(reversed(tuple(r * sm for r in acq.stress_rates())))
        for drain in (1.0, 2.0, 3.0):
            a46.DRAIN = drain
            bp600, bpop600, _ = stat(B, 600, rates_b, SEEDS)
            bp1500, bpop1500, bd = stat(B, 1500, rates_b, SEEDS)
            ap600, _, _ = stat(A, 600, rates_b, SEEDS)
            ratio = bp600 / ap600 if ap600 > 0 else float('inf')
            print(f'{sm:>3} {drain:>6} | {bp600:>9.0f} {bp1500:>10.0f} {bd:>4}/12 | '
                  f'{ap600:>9.0f} {ratio:>6.2f} {bpop1500:>9.1f}')
            if bd == 0 and ratio > 1.5 and bpop1500 > 0:
                found.append((sm, drain, ratio, bpop1500))
    print()
    print('stable (0 dead) AND graded (B/A production ratio > 1.5):',
          found if found else 'NONE')
