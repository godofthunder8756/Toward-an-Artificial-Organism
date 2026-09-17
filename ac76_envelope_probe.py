"""AC76 economic-envelope probe: instrument the catastrophic-corruption boundary.

AC76 (frozen) found >=16-bit sudden corruption is economically unrecoverable: the corruption idles
the program (no income) while the paid re-instantiation starves (504 writes, material out in ~4
ticks) -- the trigger and the payment are in tension.

This probe measures the resource trajectory at the corruption boundary so the three candidate
mechanisms (starvation buffer, staged regeneration, cheaper write) can be tested against the real
economics rather than assumed. Engineering only. No protocol, no final seeds, no claim.
"""
import numpy as np
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

# import the frozen AC76 runner's mechanism and build() machinery verbatim
import ac76_compressed_probe as cp

CORRUPT_TICK = 8192
TICKS = 16384


def run_traced(seed, history, arm='closed', nbits=16):
    """Run the compressed-description re-instantiation and record the resource trajectory around the
    corruption tick: energy, material, fuel, income per tick, and the regeneration writes actually
    performed. Returns the row plus a per-tick resource trace."""
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    o.body.traces[1, :8] = cp.encode_priority(priority)[:, None]
    step = cp.build(arm, alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event()
    first_dead = None
    trace = []   # (t, energy, material, fuel, in_m, in_f, reg_writes)
    for t in range(TICKS):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if t == CORRUPT_TICK:
            correct = prog.program(priority)
            for bit in range(nbits):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if first_dead is None and o.body.dead:
            first_dead = t
        if CORRUPT_TICK - 2 <= t <= CORRUPT_TICK + 12:
            trace.append((t, int(o.body.energy), int(o.body.material), int(o.body.fuel),
                          int(e.get('in_m', 0)), int(e.get('in_f', 0)),
                          int(e.get('reg_writes', 0)), bool(o.body.dead)))
    inv = ac4.inventory(o.body)
    target = prog.program(priority)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    return dict(seed=seed, nbits=nbits, completed=total['active'] == TICKS, first_dead=first_dead,
                program_correct=int((decoded == target).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                reg_writes_total=int(total.get('reg_writes', 0)),
                spent_m=int(total['spent_m']), in_m_total=int(total['in_m']),
                trace=trace)


if __name__ == '__main__':
    print('resource trajectory at the corruption boundary (seed 0, history 0):')
    for nbits in (8, 16, 32):
        r = run_traced(0, 0, 'closed', nbits)
        print(f'  nbits={nbits:3d}: completed={r["completed"]} dead={r["first_dead"]} '
              f'program_correct={r["program_correct"]}/126 reg_writes={r["reg_writes_total"]} '
              f'in_m_total={r["in_m_total"]}')
        for row in r['trace']:
            t, en, mat, fuel, inm, inf, rg, dead = row
            print(f'    t={t:5d} E={en:3d} M={mat:3d} F={fuel:2d} in_m={inm:3d} in_f={inf:2d} '
                  f'reg={rg:3d} dead={dead}')
        print()
