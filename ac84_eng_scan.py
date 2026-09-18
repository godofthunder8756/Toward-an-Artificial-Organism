"""AC84 engineering: broad internalized scan to confirm the predeclared floors are safe
against the earliest possible W/C collapse, and to check the proposed finals seeds.
Engineering only.
"""
import ac84

# broad scan: seeds 0-63, internalized, horizon 4096
rows = [ac84.run(s, h, 'internalized', ticks=4096) for s in range(64) for h in (0, 1)]

dead = [r for r in rows if not r['completed']]
print(f"internalized seeds 0-63: {len(dead)}/128 dead")
print("death times:", sorted(r['first_dead'] for r in dead))
print("min W_birth:", min(r['W_birth'] for r in rows))
print("min C_birth:", min(r['C_birth'] for r in rows))
print("min B_birth:", min(r['B_birth'] for r in rows))
print("min writes:", min(r['writes'] for r in rows))
print("min converted:", min(r['converted'] for r in rows))
print("min desc_correct among dead:", min(r['description_correct'] for r in dead))
print("missing first_acquire:", sum(1 for r in rows
      if r['first_acquire'][0] is None or r['first_acquire'][1] is None))

# proposed finals seeds
print("\nproposed finals 4020-4023, internalized @4096:")
for s in (4020, 4021, 4022, 4023):
    for h in (0, 1):
        r = ac84.run(s, h, 'internalized', ticks=4096)
        print(f"  seed={s} hist={h} completed={r['completed']} dead@={r['first_dead']} "
              f"W={r['W_birth']} C={r['C_birth']} B={r['B_birth']} "
              f"writes={r['writes']} conv={r['converted']} desc={r['description_correct']} "
              f"routes={r['routes']} first_acquire={r['first_acquire']}")

# also check finals seeds for unmaintained / no_repair (for the load-bearing gates)
print("\nproposed finals 4020-4023, all arms @4096:")
for arm in ac84.ARMS:
    for s in (4020, 4021, 4022, 4023):
        for h in (0, 1):
            r = ac84.run(s, h, arm, ticks=4096)
            print(f"  {arm:13s} seed={s} hist={h} completed={r['completed']} dead@={r['first_dead']} "
                  f"desc={r['description_correct']} W={r['W_birth']} C={r['C_birth']} B={r['B_birth']}")
