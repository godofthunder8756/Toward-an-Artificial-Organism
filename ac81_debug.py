"""Debug: is the AC80 description repair actually firing and charging writes?"""
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
step = ac80.build('regen', alloc, ac80.reg_maintained)
base_map = (0 % 2, (0 // 2) % 2)
rng = np.random.default_rng([0, 1509]); rng1 = np.random.default_rng([0, 1609])
total = ac9.event()
last_report = 0
for t in range(16384):
    alloc.now = t
    core = (rng.random((126, 7)) < .0001).astype(np.uint8)
    noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
    directions = rng.integers(0, 4, 20, dtype=np.uint8)
    coin = bool(rng.random() < .5)
    o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
    dm = ac80.desc_minority(o)
    e = step(o, core, noise, directions, coin, base_map, [True, True], True)
    for k in total:
        total[k] += e.get(k, 0)
    if t % 2048 == 0:
        print(f't={t} desc_minority(pre-step)={dm} reg_writes_cum={total.get("reg_writes",0)} '
              f'desc_correct={int((ac80.read_description(o)==encoded).sum())}/78 '
              f'writes_cum={total["writes"]}')
print('FINAL desc_correct', int((ac80.read_description(o) == encoded).sum()), '/78')
print('FINAL reg_writes', total.get('reg_writes', 0))
print('desc_minority final', ac80.desc_minority(o))
# how many correct-0 bits, and their replica states
n0 = int((encoded == 0).sum())
sets = o.body.traces[1, encoded == 0].sum(axis=-1)
print(f'correct-0 bits: {n0}, set-replica distribution: {np.bincount(sets, minlength=8).tolist()}')
