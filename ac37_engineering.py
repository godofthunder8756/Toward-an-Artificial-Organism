"""AC37 engineering: the full-720 optima on the paired seeds, and the arm ranges that size the bar.

Engineering, not a hashed source. Run with:
    OPENBLAS_NUM_THREADS=1 PYTHONPATH=. .venv/bin/python -B ac37_engineering.py
"""
import itertools
import json
import numpy as np
import ac37_selfsufficient as ac37

print('economy: production period %d, drain %d, renew cost %d, ticks %d'
      % (ac37.PRODUCTION_PERIOD, ac37.DRAIN, ac37.RENEW_ENERGY, ac37.TICKS))

out = {}
for name, rates in (('A', ac37.RATES_A), ('B', ac37.RATES_B)):
    sc = {o: ac37.rating(o, rates) for o in itertools.permutations(range(6))}
    top = max(sc, key=sc.get)
    vals = sorted(sc.values())
    out[name] = {'order': list(top), 'rating': sc[top], 'median': vals[360], 'worst': vals[0],
                 'spread': vals[-1] - vals[0]}
    print('%s optimum %s rating %.2f median %.2f worst %.2f spread %.2f'
          % (name, top, sc[top], vals[360], vals[0], vals[-1] - vals[0]))

oA = tuple(out['A']['order'])
old_under_B = ac37.rating(oA, ac37.RATES_B)
print('A optimum rated under B: %.2f' % old_under_B)
margin = out['B']['rating'] - old_under_B
print('margin: %.2f' % margin)
sd = ac37.noise_of_order(tuple(out['B']['order']), ac37.RATES_B)[0]
print('noise sd on the B optimum: %.2f   margin/noise %.2f' % (sd, margin / sd if sd else float('inf')))

opt = {'A': (oA, out['A']['rating']), 'B': (tuple(out['B']['order']), out['B']['rating'])}
rows = [ac37.individual(seed, opt) for seed in range(4)]
print('\nengineering arms (4 individuals):')
for arm in ac37.ARMS:
    posts = [round(r[arm]['post'], 2) for r in rows]
    print('  %-13s %s  min %.2f mean %.2f max %.2f'
          % (arm, posts, min(posts), float(np.mean(posts)), max(posts)))

json.dump({'optima': {k: {'order': list(v[0]), 'rating': v[1]} for k, v in opt.items()},
           'old_under_B': old_under_B, 'margin': margin, 'noise': sd, 'sweep': out},
          open('/tmp/ac37_engineering.json', 'w'), indent=2)
