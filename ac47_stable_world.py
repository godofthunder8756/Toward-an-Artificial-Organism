"""AC47 (prerequisite, engineering): can a stable, graded self-funded world exist?

The question
------------
AC46's post-hoc sanity check showed the drain world (period 4, drain 3) is bimodal and
horizon-unstable: the learner-vs-keeper advantage is a transient of the population dying, not a stable
self-maintenance result. The open question is whether ANY (period, drain, stress) configuration of this
architecture yields a world where the population and energy reach a *stationary band* over several
horizons AND the order still meaningfully differentiates the outcome (graded, not saturated).

This scans the space. It is a prerequisite, not a study: no protocol, no final seeds, no claim.

What it measures
----------------
For each (period, drain, stress-multiplier), the B-optimum order (0,4,1,3,2,5) is run at horizons
300/600/900/1500 over 8 scoring seeds, reporting mean sites, mean energy, and the number of dead seeds.
A config is "stable" if the population and energy are not declining across horizons and 0/8 seeds die;
"graded" if the B-vs-A spread (B mean - A mean at 600) is substantial. The two are in tension, and the
scan's job is to show whether any config satisfies both.
"""
import numpy as np
import ac30_acquire as acq
import ac46_selfsufficiency as a46

B = (0, 4, 1, 3, 2, 5)
A = (4, 5, 1, 2, 0, 3)
SEEDS = tuple(range(9000, 9008))


def drive(order, seed, ticks, rates):
    w = a46.World(seed, rates=rates)
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


def trajectory(order, tickses, rates):
    out = []
    for t in tickses:
        v = [drive(order, s, t, rates) for s in SEEDS]
        out.append((float(np.mean([x[0] for x in v])),
                    float(np.mean([x[1] for x in v])),
                    sum(1 for x in v if x[2])))
    return out


def scan():
    rows = []
    for period in (4, 6, 8):
        for sm in (1, 2, 3):
            rates_b = tuple(reversed(tuple(r * sm for r in acq.stress_rates())))
            for drain in (1.0, 1.5, 2.0, 2.25, 2.5, 2.75, 3.0):
                a46.PRODUCTION_PERIOD = period
                a46.DRAIN = drain
                tb = trajectory(B, (300, 600, 900, 1500), rates_b)
                va = [drive(A, s, 600, rates_b) for s in SEEDS]
                a_mean = float(np.mean([x[0] for x in va]))
                spread = tb[1][0] - a_mean
                dead = tb[3][2]
                declining = tb[3][0] < tb[0][0] - 1.0          # lost >1 site over the horizons
                energy_neg = tb[3][1] < 0
                rows.append(dict(period=period, sm=sm, drain=drain,
                                 sites=[r[0] for r in tb], energy=[r[1] for r in tb],
                                 dead=dead, spread=spread, declining=declining,
                                 energy_neg=energy_neg))
    return rows


if __name__ == '__main__':
    rows = scan()
    stable = [r for r in rows if not r['declining'] and not r['energy_neg'] and r['dead'] == 0]
    graded = [r for r in rows if r['spread'] >= 3.0]
    both = [r for r in rows if r in stable and r in graded]

    print('configs scanned:', len(rows))
    print(f'stable (stationary, energy>=0, 0 dead): {len(stable)}')
    print(f'graded (spread >= 3 sites):             {len(graded)}')
    print(f'BOTH stable and graded:                 {len(both)}')
    print()
    print('best spread among STABLE configs:')
    for r in sorted(stable, key=lambda x: -x['spread'])[:5]:
        print(f"  p{r['period']} sm{r['sm']} d{r['drain']}: spread {r['spread']:.1f}  "
              f"sites {[round(s,1) for s in r['sites']]}  dead {r['dead']}")
    print()
    print('best stability among GRADED configs (spread >= 3):')
    for r in sorted(graded, key=lambda x: (x['dead'], x['declining']))[:5]:
        print(f"  p{r['period']} sm{r['sm']} d{r['drain']}: spread {r['spread']:.1f}  "
              f"dead {r['dead']}  declining {r['declining']}  energy_neg {r['energy_neg']}")
    print()
    print('VERDICT: a stable AND graded self-funded world exists: '
          + ('YES' if both else 'NO (the two requirements exclude each other)'))
