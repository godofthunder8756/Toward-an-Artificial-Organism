"""AC84 engineering probe: all four arms across horizons, to settle the horizon and the
unconditional turnover floors. Engineering only -- no protocol, no claim.

Uses ac84.run (which mirrors AC80's mechanism with no kill intervention) directly.
"""
import json
import ac84

SEEDS = list(range(0, 32))
HORIZONS = (2048, 4096, 8192)

rows = []
for seed in SEEDS:
    for hist in (0, 1):
        for arm in ac84.ARMS:
            for H in HORIZONS:
                rows.append(ac84.run(seed, hist, arm, ticks=H))

print("=== per-horizon, per-arm aggregate (64 individuals = 32 seeds x 2 histories) ===")
for H in HORIZONS:
    for arm in ac84.ARMS:
        rs = [r for r in rows if r['ticks'] == H and r['arm'] == arm]
        dead = [r for r in rs if not r['completed']]
        Ws = [r['W_birth'] for r in rs]
        Cs = [r['C_birth'] for r in rs]
        Bs = [r['B_birth'] for r in rs]
        wr = [r['writes'] for r in rs]
        cv = [r['converted'] for r in rs]
        px = [r['particle_export'] for r in rs]
        print(f"H={H} {arm:13s}: dead={len(dead)}/64 "
              f"deaths={sorted(r['first_dead'] for r in dead)}")
        print(f"    W_birth min/max={min(Ws)}/{max(Ws)}  C_birth min/max={min(Cs)}/{max(Cs)}  "
              f"B_birth min/max={min(Bs)}/{max(Bs)}")
        print(f"    writes min={min(wr)}  converted min={min(cv)}  particle_export min/max={min(px)}/{max(px)}")
        descmin = min(r['description_correct'] for r in rs)
        descmin_dead = min((r['description_correct'] for r in dead), default=None)
        print(f"    desc_correct min={descmin}  (min among dead: {descmin_dead})")

print("\n=== unconditional floor check (G1 floors W>=32, C>=8, B>=40; G2 writes>0, converted>0) ===")
for H in HORIZONS:
    for arm in ac84.ARMS:
        rs = [r for r in rows if r['ticks'] == H and r['arm'] == arm]
        fail_turnover = [r for r in rs if not (r['W_birth'] >= 32 and r['C_birth'] >= 8 and r['B_birth'] >= 40)]
        fail_use = [r for r in rs if not (r['writes'] > 0 and r['converted'] > 0)]
        flag = "  <- FAILS" if fail_turnover else ""
        print(f"H={H} {arm:13s}: turnover-fail={len(fail_turnover)} use-fail={len(fail_use)}{flag}")

print("\n=== collapse seeds (internalized, at 4096): which seeds die, and their turnover ===")
rs = [r for r in rows if r['ticks'] == 4096 and r['arm'] == 'internalized' and not r['completed']]
for r in sorted(rs, key=lambda x: x['first_dead']):
    print(f"  seed={r['seed']} hist={r['history']} dead@={r['first_dead']} "
          f"W={r['W_birth']} C={r['C_birth']} B={r['B_birth']} "
          f"writes={r['writes']} conv={r['converted']} exp={r['particle_export']} "
          f"routes={r['routes']} first_acquire={r['first_acquire']} first_loss={r['first_route_loss']} "
          f"Wl={r['W_live']} Cl={r['C_live']} Bl={r['B_live']} desc={r['description_correct']}")
