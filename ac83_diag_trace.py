import numpy as np
import ac83
import ac12
import ac9
import ac4
import ac5_program as prog
import ac80
import ac71

# Reconstruct the pristine seed-0 run with an instrumented loop, mirroring ac83.run exactly.
seed, history = 0, 0
arm = 'pristine'
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
reg_fn = ac80.reg_maintained if maintained else (ac80.reg_pristine if ac_arm == 'regen' else None)
step = ac80.build(ac_arm, alloc, reg_fn)
base_map = (seed % 2, (seed // 2) % 2)
rng = np.random.default_rng([seed, 1509])
rng1 = np.random.default_rng([seed, 1609])

def route0_life(o):
    # region 0, slot 0 holds key 0 (find its slot)
    for s in range(2):
        if ac12.m12.decoded_key(o.memory, 0, s) == 0:
            return int(o.memory.life[0, s].min())
    return None

print(f"priority={priority} base_map={base_map} corrupt_tick={corrupt_tick} move_tick={move_tick}")
for t in range(ac83.TICKS):
    alloc.now = t
    core = (rng.random((126, 7)) < .0001).astype(np.uint8)
    noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
    directions = rng.integers(0, 4, 20, dtype=np.uint8)
    coin = bool(rng.random() < .5)
    if damage_desc:
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
    r0 = route0_life(o)
    obs = ac9.observe(o)
    mat = o.body.material
    # log windows around interventions and any tick where route 0 life drops sharply
    if t in (8190, 8191, 8192, 8193, 8194, 8195, 8196, 8197, 8200, 8205, 8210,
             12286, 12287, 12288, 12289, 12290, 12291, 12292, 12295, 12300, 12305, 12310, 12320):
        print(f"t={t} mat={mat} obs1={int(bool(obs&2))} obs3={int(bool(obs&8))} "
              f"r0life={r0} action={a} W={int((o.body.life[:16]>0).sum())} "
              f"routes={[o.memory.read(k) for k in (0,1)]} demand={o.memory.demand().tolist()}")
    if r0 is not None and r0 <= 8:
        print(f"  >> t={t} mat={mat} obs1={int(bool(obs&2))} obs3={int(bool(obs&8))} "
              f"r0life={r0} action={a} demand={o.memory.demand().tolist()}")
print(f"FINAL routes={[o.memory.read(k) for k in (0,1)]} demand={o.memory.demand().tolist()}")
