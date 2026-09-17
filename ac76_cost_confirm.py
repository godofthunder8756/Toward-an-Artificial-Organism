"""Confirm the causal story: the cheaper (majority-only) write costs ~1 replica per corrupted bit
(not 4), which is why it fits inside the idle organism's material budget where the frozen full
re-instantiation (4 replicas/bit) does not. Measures per-tick material/energy around the corruption
tick for full vs majority at n=32.
"""
import numpy as np
import ac71, ac12, ac9, ac4, ac5_program as prog, ac76_compressed_probe as cp
import ac76_recovery_probe as rp


def trace_variant(seed, variant, nbits):
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
        if t == 8192:
            correct = prog.program(priority)
            for bit in range(nbits):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        if 8190 <= t <= 8196:
            out.append((t, int(o.body.energy), int(o.body.material), int(o.body.fuel),
                        int(e.get('reg_writes', 0)), bool(o.body.dead)))
    return out


if __name__ == '__main__':
    for variant in ('full', 'majority'):
        print(f'variant={variant} n=32, seed 0:')
        for t, en, mat, fuel, rg, dead in trace_variant(0, variant, 32):
            print(f'  t={t} E={en:3d} M={mat:3d} F={fuel:2d} reg_writes={rg:3d} dead={dead}')
        print()
