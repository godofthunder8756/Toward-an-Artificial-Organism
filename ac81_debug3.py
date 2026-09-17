"""Debug 3: what repairs the description? Check action histogram + traces[1] non-desc bits."""
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
# make a copy of the built step but with the reg DISABLED to isolate action-3's effect
step_noreg = ac80.build('regen', alloc, None)  # regen False -> reg_from_priority = no-op
base_map = (0 % 2, (0 // 2) % 2)
rng = np.random.default_rng([0, 1509]); rng1 = np.random.default_rng([0, 1609])
total = ac9.event(); actions = {}
for t in range(16384):
    alloc.now = t
    core = (rng.random((126, 7)) < .0001).astype(np.uint8)
    noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
    directions = rng.integers(0, 4, 20, dtype=np.uint8)
    coin = bool(rng.random() < .5)
    o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
    a = int(prog.choose(o.body.traces, ac9.observe(o)))
    actions[a] = actions.get(a, 0) + 1
    e = step_noreg(o, core, noise, directions, coin, base_map, [True, True], True)
    for k in total:
        total[k] += e.get(k, 0)
print('priority', priority)
print('action histogram (no reg):', dict(sorted(actions.items())))
print('desc_correct (no reg):', int((ac80.read_description(o) == encoded).sum()), '/78')
print('desc_minority (no reg):', ac80.desc_minority(o))
n0 = int((encoded == 0).sum())
sets = o.body.traces[1, :ac80.DESC_BITS][encoded == 0].sum(axis=-1)
print(f'correct-0 bits: {n0}, set-replica distribution: {np.bincount(sets, minlength=8).tolist()}')
# non-description bank-1 bits (78..1023) — should be all 0, check
print('non-desc bank-1 bits nonzero count:', int((o.body.traces[1, ac80.DESC_BITS:].sum(axis=-1) > 0).sum()))
