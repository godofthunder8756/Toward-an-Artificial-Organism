"""Trace why seed 5 dies at t=261 under `staged` but survives under `full` (no corruption).

Compare the two orderings tick-by-tick for body state (W, C, energy, material, fuel) and the reg
writes, around the divergence. The hypothesis to test: income-first ordering writes rule 1 (material)
replicas before rule 0 (fuel), so on the ticks where the fuel rule's enabled bit is damaged, the
program does not respond to fuel-low, and the ordering determines whether the fuel response is
restored before the organism's fuel/energy runs out.
"""
import numpy as np
import ac71, ac12, ac9, ac4, ac5_program as prog, ac76_compressed_probe as cp
import ac76_recovery_probe as rp


def trace(seed, variant, end=280):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, 0)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    o.body.traces[1, :8] = cp.encode_priority(priority)[:, None]
    step = rp.build('closed', alloc, rp.VARIANTS[variant])
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    out = []
    for t in range(16384):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        if t <= end or o.body.dead:
            W = int((o.body.life[:4] > 0).sum())
            C = int((o.body.life[16:20] > 0).sum())
            # fuel rule (rule 0) enabled bit majority: bit 0
            fuel_enabled = int(o.body.traces[0, 0].sum() >= 4)
            out.append((t, W, C, int(o.body.energy), int(o.body.material), int(o.body.fuel),
                        fuel_enabled, int(e.get('reg_writes', 0)), bool(o.body.dead)))
            if o.body.dead:
                break
    return out


if __name__ == '__main__':
    for variant in ('full', 'staged'):
        print(f'variant={variant} seed=5 (W, C, E, M, F, fuel_enabled, reg_writes, dead):')
        for row in trace(5, variant):
            print('  t=%d W=%d C=%d E=%d M=%d F=%d fuel_en=%d reg=%d dead=%s' % row)
        print()
