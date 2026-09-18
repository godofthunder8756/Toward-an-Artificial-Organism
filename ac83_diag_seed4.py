import numpy as np
import ac83
import ac12
import ac9
import ac4
import ac5_program as prog
import ac80
import ac71

seed, history = 4, 0
arm = 'internalized'
transition = 'perm'
corrupt = True
corrupt_tick, move_tick = ac83.DESIGNS['corrupt_then_move']['corrupt_tick'], ac83.DESIGNS['corrupt_then_move']['move_tick']

ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
ac12.REGISTER_THRESHOLD = 4
_, _, _, priority = ac4.acquire(seed)
ac_arm, damage_desc, maintained, erase = ac83.ARM_PARTS[arm]
alloc = ac83.ALLOC[erase]('allocate', seed, history)
o, offs = ac12.acquire(seed)
alloc.offs = offs
alloc.shadow = o.body.traces[0].copy()
encoded = ac80.description_bits(priority)
o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]
reg_fn = ac80.reg_maintained
step = ac80.build(ac_arm, alloc, reg_fn)
base_map = (seed % 2, (seed // 2) % 2)
rng = np.random.default_rng([seed, 1509])
rng1 = np.random.default_rng([seed, 1609])

def route_life(o, key):
    for r in range(2):
        for s in range(2):
            if ac12.m12.decoded_key(o.memory, r, s) == key:
                return int(o.memory.life[r, s].min())
    return None

print(f"seed={seed} hist={history} priority={priority} base_map={base_map} "
      f"corrupt_tick={corrupt_tick} move_tick={move_tick}")
actions = {}
first_route_loss = {}
prev_demand = o.memory.demand().tolist()
for t in range(ac83.TICKS):
    alloc.now = t
    core = (rng.random((126, 7)) < .0001).astype(np.uint8)
    noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
    directions = rng.integers(0, 4, 20, dtype=np.uint8)
    coin = bool(rng.random() < .5)
    o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
    if t == corrupt_tick and corrupt:
        correct = prog.program(priority)
        for bit in range(ac83.CORRUPT_BITS):
            w = 1 - int(correct[bit])
            o.body.traces[0, bit, 0:4] = w
            o.body.traces[0, bit, 4:7] = int(correct[bit])
    a = int(ac12.prog.choose(o.body.traces, ac9.observe(o)))
    e = step(o, core, noise, directions, coin, tuple(ac83.mapping_at(base_map, t, transition, move_tick)),
             [True, True], True)
    actions[a] = actions.get(a, 0) + 1
    for key in (0, 1):
        if first_route_loss.get(key) is None and route_life(o, key) is None and prev_demand[0] > 0:
            first_route_loss[key] = t
    prev_demand = o.memory.demand().tolist()
    if t in (12288, 12300, 12350, 12400, 12500, 12600, 13000, 13500, 14000, 14500, 15000, 15500, 16000):
        print(f"t={t} mat={o.body.material} W={int((o.body.life[:4]>0).sum())} "
              f"C={int((o.body.life[16:20]>0).sum())} r0={route_life(o,0)} r1={route_life(o,1)} "
              f"demand={o.memory.demand().tolist()} action={a}")
print(f"FINAL routes={[o.memory.read(k) for k in (0,1)]} demand={o.memory.demand().tolist()} "
      f"first_route_loss={first_route_loss} actions={actions}")
print(f"W={int((o.body.life[:4]>0).sum())} C={int((o.body.life[16:20]>0).sum())} "
      f"register={[ac12.bit_value(o, off) for off in offs]}")
# decoded program correctness vs target
target = prog.program(priority)
decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
print(f"program_correct={int((decoded==target).sum())}/126")
