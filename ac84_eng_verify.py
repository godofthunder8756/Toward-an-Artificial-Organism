"""AC84 engineering verification: settle the load-bearing gates and the survivor-scoped
recipe gate. Engineering only.
"""
import ac84

SEEDS = list(range(0, 32))
H = 4096

rows = []
for seed in SEEDS:
    for hist in (0, 1):
        for arm in ac84.ARMS:
            rows.append(ac84.run(seed, hist, arm, ticks=H))

unm = [r for r in rows if r['arm'] == 'unmaintained']
intl = [r for r in rows if r['arm'] == 'internalized']
norep = [r for r in rows if r['arm'] == 'no_repair']

print("unmaintained desc_correct distribution:", sorted(r['description_correct'] for r in unm))
print("  max desc_correct:", max(r['description_correct'] for r in unm))
print("  survivors (completed):", [(r['seed'], r['history'], r['description_correct'],
                                   r['W_birth'], r['C_birth'], r['B_birth']) for r in unm if r['completed']])
print("  dead count:", sum(1 for r in unm if not r['completed']), "/", len(unm))

print("\ninternalized survivors desc_correct:", sorted(set(r['description_correct'] for r in intl if r['completed'])))
print("  internalized dead desc_correct:", sorted(set(r['description_correct'] for r in intl if not r['completed'])))

print("\nno_repair all dead:", all(not r['completed'] for r in norep), " (dead", sum(1 for r in norep if not r['completed']), "/", len(norep), ")")
print("  no_repair B_birth range:", min(r['B_birth'] for r in norep), "-", max(r['B_birth'] for r in norep))

# The early-collapse seeds (unmaintained failing the turnover floor)
fails = [r for r in unm if not (r['W_birth'] >= 32 and r['C_birth'] >= 8 and r['B_birth'] >= 40)]
print("\nunmaintained floor-failures:", [(r['seed'], r['history'], r['first_dead'],
      r['W_birth'], r['C_birth'], r['B_birth']) for r in fails])

# internalized: verify the floor is met by all, and first_acquire both non-None
print("\ninternalized floor-failures:", sum(1 for r in intl if not (
    r['W_birth'] >= 32 and r['C_birth'] >= 8 and r['B_birth'] >= 40)))
print("internalized missing first_acquire:", sum(1 for r in intl
      if r['first_acquire'][0] is None or r['first_acquire'][1] is None))
