import numpy as np
import ac83
import ac75
import ac12
import ac9
import ac4
import ac5_program as prog
import ac80
import ac71

def route_hold_frac_ac75(seed, history):
    # Mirror ac75.run for the erase arm, perm transition, recording demand per tick.
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    alloc = ac75.ALLOC['erase']('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    step = ac71.build('allocate', alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    held_ticks = 0
    for t in range(ac75.TICKS):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        e = step(o, core, noise, directions, coin, tuple(ac75.mapping_at(base_map, t, 'perm')),
                 [True, True], True)
        if o.memory.demand().tolist() == [42, 0]:
            held_ticks += 1
    return held_ticks / ac75.TICKS, [o.memory.read(k) for k in (0, 1)]


def route_hold_frac_ac83(seed, history):
    corrupt_tick, move_tick = ac83.DESIGNS['corrupt_then_move']['corrupt_tick'], ac83.DESIGNS['corrupt_then_move']['move_tick']
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    ac_arm, damage_desc, maintained, erase = ac83.ARM_PARTS['internalized']
    alloc = ac83.ALLOC[erase]('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    encoded = ac80.description_bits(priority)
    o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]
    step = ac80.build(ac_arm, alloc, ac80.reg_maintained)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    held_ticks = 0
    for t in range(ac83.TICKS):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        if t == corrupt_tick:
            correct = prog.program(priority)
            for bit in range(ac83.CORRUPT_BITS):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, tuple(ac83.mapping_at(base_map, t, 'perm', move_tick)),
                 [True, True], True)
        if o.memory.demand().tolist() == [42, 0]:
            held_ticks += 1
    return held_ticks / ac83.TICKS, [o.memory.read(k) for k in (0, 1)]


for seed in (0, 4, 5):
    for history in (0, 1):
        f75, r75 = route_hold_frac_ac75(seed, history)
        f83, r83 = route_hold_frac_ac83(seed, history)
        print(f"s{seed}h{history}: AC75 erase  hold-frac={f75:.3f} final={r75} | "
              f"AC83 internalized  hold-frac={f83:.3f} final={r83}")
