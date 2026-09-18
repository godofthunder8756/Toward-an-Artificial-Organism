import ac84
rows = [ac84.run(s, h, 'internalized', ticks=4096) for s in range(128) for h in (0, 1)]
dead = [r for r in rows if not r['completed']]
print('internalized seeds 0-127:', len(dead), '/', len(rows), 'dead')
print('death times:', sorted(r['first_dead'] for r in dead))
print('min W_birth:', min(r['W_birth'] for r in rows))
print('min C_birth:', min(r['C_birth'] for r in rows))
print('min B_birth:', min(r['B_birth'] for r in rows))
print('min writes:', min(r['writes'] for r in rows), 'min converted:', min(r['converted'] for r in rows))
print('floor-fail (W<16 or C<4 or B<20):',
      sum(1 for r in rows if not (r['W_birth'] >= 16 and r['C_birth'] >= 4 and r['B_birth'] >= 20)))
