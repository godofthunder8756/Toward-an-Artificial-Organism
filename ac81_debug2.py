"""Debug 2: measure the raw description damage stream (rng1) and what touches traces[1]."""
import numpy as np
import ac80
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

# raw rng1 damage count over 16384 ticks
rng1 = np.random.default_rng([0, 1609])
total_sets = 0
for t in range(16384):
    total_sets += int((rng1.random((ac80.DESC_BITS, 7)) < .0001).sum())
print('raw rng1 SETs over 16384 ticks:', total_sets, '(expected ~', 546 * 1e-4 * 16384, ')')

# program damage stream for comparison
rng = np.random.default_rng([0, 1509])
total_core = 0
for t in range(16384):
    total_core += int((rng.random((126, 7)) < .0001).sum())
print('raw core SETs over 16384 ticks:', total_core, '(expected ~', 126 * 7 * 1e-4 * 16384, ')')

# Now instrument the built step to count reg fires and desc minority WITHOUT the desc damage,
# to see whether reg fires at all and whether desc_minority grows.
ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV; ac12.REGISTER_THRESHOLD = 4
_, _, _, priority = ac4.acquire(0)
alloc = ac12.Alloc('allocate', 0, 0)
o, offs = ac12.acquire(0)
alloc.offs = offs; alloc.shadow = o.body.traces[0].copy()
encoded = ac80.description_bits(priority)
o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]

# Count reg fires by monkeypatching reg_description
fires = [0]
orig_reg = ac80.reg_description
def counting_reg(o, e):
    fires[0] += 1
    return orig_reg(o, e)
ac80.reg_description = counting_reg
step = ac80.build('regen', alloc, ac80.reg_maintained)
ac80.reg_description = orig_reg

base_map = (0 % 2, (0 // 2) % 2)
rng = np.random.default_rng([0, 1509]); rng1 = np.random.default_rng([0, 1609])
total = ac9.event()
for t in range(16384):
    alloc.now = t
    core = (rng.random((126, 7)) < .0001).astype(np.uint8)
    noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
    directions = rng.integers(0, 4, 20, dtype=np.uint8)
    coin = bool(rng.random() < .5)
    o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
    e = step(o, core, noise, directions, coin, base_map, [True, True], True)
    for k in total:
        total[k] += e.get(k, 0)
print('reg_description fires:', fires[0])
print('reg_writes cum:', total.get('reg_writes', 0))
print('desc_correct final:', int((ac80.read_description(o) == encoded).sum()), '/78')
print('desc_minority final:', ac80.desc_minority(o))
n0 = int((encoded == 0).sum())
sets = o.body.traces[1, :ac80.DESC_BITS][encoded == 0].sum(axis=-1)
print(f'correct-0 bits: {n0}, set-replica distribution: {np.bincount(sets, minlength=8).tolist()}')
