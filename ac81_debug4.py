"""Debug 4: properly count reg_description fires + writes in the internalized arm."""
import numpy as np
import ac80
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV; ac12.REGISTER_THRESHOLD = 4
_, _, _, priority = ac4.acquire(0)
alloc = ac12.Alloc('allocate', 0, 0)
o, offs = ac12.acquire(0)
alloc.offs = offs; alloc.shadow = o.body.traces[0].copy()
encoded = ac80.description_bits(priority)
o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]

# wrap reg_description and keep the wrapper active through the whole loop
state = {'fires': 0, 'writes': 0}
_orig = ac80.reg_description
def wrapped(o, e):
    state['fires'] += 1
    r = _orig(o, e)
    state['writes'] += e.get('reg_writes', 0)
    return r
ac80.reg_description = wrapped
step = ac80.build('regen', alloc, ac80.reg_maintained)
# do NOT restore until after loop

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
ac80.reg_description = _orig
print('reg_description fires:', state['fires'], 'writes via reg:', state['writes'])
print('total reg_writes:', total.get('reg_writes', 0))
print('desc_correct:', int((ac80.read_description(o) == encoded).sum()), '/78')
print('desc_minority final:', ac80.desc_minority(o))
