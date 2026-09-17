"""AC81 milestone-2 engineering probe: component turnover in the AC80 world.

Measure, in the internalized AC80 world (no corruption), what the component
turnover actually looks like: births, deaths, uses, per component class, over
16,384 ticks. This decides what a "multiple turnover cycles" gate can require.
"""
import numpy as np
import ac80
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog


def run_probe(seed, history, ticks=16384):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV; ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs; alloc.shadow = o.body.traces[0].copy()
    encoded = ac80.description_bits(priority)
    o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]
    step = ac80.build('regen', alloc, ac80.reg_maintained)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509]); rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    W_pop = []; C_pop = []; B_pop = []
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t % 512 == 0:
            W_pop.append(int((o.body.life[:4] > 0).sum()))
            C_pop.append(int((o.body.life[16:20] > 0).sum()))
            B_pop.append(int((o.body.boundary > 0).sum()))
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, alive=total['active'] == ticks,
                W_birth=total['W_birth'], C_birth=total['C_birth'], B_birth=total['B_birth'],
                particle_expiry=total['particle_expiry'], particle_export=total['particle_export'],
                B_expiry=total['B_expiry'], B_discard=total['B_discard'],
                writes=total['writes'], converted=total['converted'],
                reg_writes=total.get('reg_writes', 0),
                W_pop=W_pop, C_pop=C_pop, B_pop=B_pop,
                W_live=int((o.body.life[:4] > 0).sum()), C_live=int((o.body.life[16:20] > 0).sum()),
                B_live=int((o.body.boundary > 0).sum()),
                inv=inv, priority=priority)


def main():
    seeds = range(8)
    rows = []
    for s in seeds:
        for h in (0, 1):
            rows.append(run_probe(s, h))
    print('component turnover in the AC80 internalized world (no corruption), 16,384 ticks')
    print(f'{"seed/h":8s} {"alive":>5s} {"W_b":>5s} {"C_b":>5s} {"B_b":>5s} {"W_exp":>5s} {"C_conv":>8s} {"writes":>6s} {"regW":>5s} {"W":>3s} {"C":>3s} {"B":>3s}')
    for r in rows:
        print(f'{str(r["seed"])+"/"+str(r["history"]):8s} {str(r["alive"]):>5s} {r["W_birth"]:5d} {r["C_birth"]:5d} '
              f'{r["B_birth"]:5d} {r["particle_expiry"]:5d} {r["converted"]:8d} {r["writes"]:6d} '
              f'{r["reg_writes"]:5d} {r["W_live"]:3d} {r["C_live"]:3d} {r["B_live"]:3d}')
    print()
    print('initial complement: W slots=16 (4 live per bank max, but acquisition sets 3/4 per bank -> '
          'see life array), C=4, B=20')
    import ac4 as a4
    b, bits, target, priority = a4.acquire(0)
    print('acquisition life array (20 particles):', list(map(int, b.life)))
    print('acquisition boundary (20 sites):', list(map(int, b.boundary)))
    print()
    print('population trajectories (sampled every 512 ticks):')
    for r in rows[:4]:
        print(f'  seed/h {r["seed"]}/{r["history"]}: W {r["W_pop"]}')
        print(f'  seed/h {r["seed"]}/{r["history"]}: C {r["C_pop"]}')
        print(f'  seed/h {r["seed"]}/{r["history"]}: B {r["B_pop"]}')


if __name__ == '__main__':
    main()
