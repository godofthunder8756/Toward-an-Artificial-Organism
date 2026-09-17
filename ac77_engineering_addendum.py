"""AC77 addendum: (1) is the fixed point a frozen state or ongoing maintenance?
(2) characterize the stationary order-quality distribution in regime B (is the ceiling unique?)."""
import numpy as np
import ac30_acquire as acq
import ac32_reacquire as ac32

RATES_B = ac32.RATES_B
CEILING = ac32.DECLARED_OPTIMA['B'][0]
BURNIN = 8000
HORIZON = 12000


def run_detailed(order, seed):
    """Track live count, lost, renewed, material at burn-in and horizon."""
    w = acq.World(seed, rates=RATES_B)
    for t in range(1, HORIZON + 1):
        word = w.urgency()
        action = None
        for position in order:
            if word >> position & 1:
                action = position
                break
        w.tick(action)
        if t == BURNIN:
            n_burn = sum(1 for v in w.life if v > 0)
            lost_burn, renewed_burn, mat_burn = w.lost, w.renewed, w.material
    n_end = sum(1 for v in w.life if v > 0)
    return n_burn, n_end, lost_burn, w.lost, renewed_burn, w.renewed, mat_burn, w.material


print('--- is the fixed point frozen, or maintained with ongoing renewal? (ceiling, 6 seeds) ---')
for s in range(6):
    nb, ne, lb, le, rb, re, mb, me = run_detailed(CEILING, s)
    print(f'  seed {s}: count {nb}->{ne}  lost {lb}->{le}  renewed {rb}->{re}  '
          f'material {mb:.0f}->{me:.0f}')

print('\n--- stationary order-quality distribution (regime B) ---')
rng = np.random.default_rng(7701)
orders = [tuple(int(x) for x in rng.permutation(6)) for _ in range(40)]
orders += [CEILING, (3, 4, 1, 5, 0, 2)]  # reference: ceiling, AC30-best (bad in B)
seeds = tuple(range(8500, 8500 + 100))


def stat_mean(order, seed):
    w = acq.World(seed, rates=RATES_B)
    acc = 0.0
    for t in range(1, HORIZON + 1):
        word = w.urgency()
        action = None
        for position in order:
            if word >> position & 1:
                action = position
                break
        w.tick(action)
        if t > BURNIN:
            acc += sum(1 for v in w.life if v > 0)
    return acc / (HORIZON - BURNIN)


means = []
for o in orders:
    vals = [stat_mean(o, s) for s in seeds]
    means.append(float(np.mean(vals)))

means = np.array(means)
is_ceiling = np.array([o == CEILING for o in orders])
is_ac30best = np.array([o == (3, 4, 1, 5, 0, 2) for o in orders])
print(f'  n orders = {len(orders)}, seeds/order = {len(seeds)}')
print(f'  ceiling (2,0,1,3,5,4) stationary mean = {means[is_ceiling][0]:.3f}')
print(f'  AC30-best (3,4,1,5,0,2) stationary mean = {means[is_ac30best][0]:.3f}  (bad in regime B)')
print(f'  min {means.min():.3f}  median {np.median(means):.3f}  max {means.max():.3f}  '
      f'sd across orders {means.std(ddof=1):.3f}')
# how many orders are within 0.25 of the ceiling's stationary value?
within025 = (np.abs(means - means[is_ceiling][0]) <= 0.25).sum()
print(f'  orders within 0.25 of ceiling: {within025}/{len(orders)}')
print(f'  orders strictly above ceiling: {(means > means[is_ceiling][0]).sum()}')
# sort and show the top of the distribution
idx = np.argsort(-means)
print('  top of the stationary ranking (order, mean):')
for i in idx[:10]:
    tag = 'CEILING' if orders[i] == CEILING else ('AC30best' if orders[i] == (3, 4, 1, 5, 0, 2) else '')
    print(f'    {orders[i]}  {means[i]:.3f}  {tag}')
print('  bottom of the stationary ranking:')
for i in idx[-5:]:
    tag = 'CEILING' if orders[i] == CEILING else ('AC30best' if orders[i] == (3, 4, 1, 5, 0, 2) else '')
    print(f'    {orders[i]}  {means[i]:.3f}  {tag}')
