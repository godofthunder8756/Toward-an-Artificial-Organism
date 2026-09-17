"""AC74 diagnostic: why does seed 2 die even with the full re-acquisition machinery (variant C)?

Engineering only. Trace the body state and the moved route around the move for seed 2 vs seed 1.
"""
import json
import numpy as np
import ac74_engineering as e

def trace(seed, history, variant='C', arm='closed'):
    ac12 = e.ac12; ac9 = e.ac9; ac4 = e.ac4; ac71 = e.ac71
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 8192; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    alloc_cls = e.AllocRestore if variant == 'C' else ac12.Alloc
    alloc = alloc_cls('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    step = ac71.build(arm, alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    out = []
    for t in range(16384):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        a = int(ac12.prog.choose(o.body.traces, ac9.observe(o)))
        mapping = list(base_map)
        if t >= 8192:
            mapping[1] = 1 - base_map[1]
        grow = True
        activation = [True, True]
        ev = step(o, core, noise, directions, coin, tuple(mapping), activation, grow)
        if t % 16 == 0 or (8100 <= t <= 8600):
            inv = ac4.inventory(o.body)
            out.append(dict(t=t, a=a, E=inv[0], M=inv[1], F=inv[2],
                            W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                            r0=o.memory.read(0), r1=o.memory.read(1),
                            reg=[ac12.bit_value(o, off) for off in offs],
                            dead=o.body.dead,
                            in_m=ev.get('in_m', 0), spent_m=ev.get('spent_m', 0),
                            prod=ev.get('productive', 0)))
        if o.body.dead:
            break
    return out, base_map


if __name__ == '__main__':
    for seed, hist in ((2, 0), (1, 0)):
        out, base = trace(seed, hist)
        print(f'=== seed {seed} hist {hist} base {base} (key1 post-move={1-base[1]}) ===')
        # print a compact window around the move and the death
        for r in out:
            if 8100 <= r['t'] <= 8600 or r['dead']:
                print(f"  t={r['t']:5d} a={r['a']} E={r['E']:5.1f} M={r['M']:5.1f} F={r['F']:5.1f} "
                      f"W={r['W']} C={r['C']} r0={r['r0']} r1={r['r1']} reg={r['reg']} "
                      f"in_m={r['in_m']} spent_m={r['spent_m']} prod={r['prod']} DEAD={r['dead']}")
