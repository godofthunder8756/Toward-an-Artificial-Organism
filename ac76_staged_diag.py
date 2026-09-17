"""Diagnose the staged variant's 4/14 pre-corruption deaths.

Hypothesis: income-first ordering starves the non-income rules (rules 2-8) of regeneration, because
every tick the per-action cap (24 writes) is consumed re-writing rule-1 (material) and rule-0 (fuel)
drift first, and the non-income rules' drift never gets a budget -> they decay to death.

Test: run staged with NO corruption and, at the death tick (or horizon), report per-rule wrong-majority
counts -- are rules 2-8 the ones that flipped majority, while rules 0-1 stayed clean?
"""
import numpy as np
import ac71, ac12, ac9, ac4, ac5_program as prog, ac76_compressed_probe as cp
import ac76_recovery_probe as rp


def staged_rule_drift(seed, hist):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, hist)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    o.body.traces[1, :8] = cp.encode_priority(priority)[:, None]
    step = rp.build('closed', alloc, rp.VARIANTS['staged'])
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    first_dead = None
    for t in range(16384):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        if first_dead is None and o.body.dead:
            first_dead = t
    target = prog.program(priority)
    decoded = (o.body.traces[0, :126].sum(axis=-1) > 3).astype(np.uint8)
    per_rule_wrong = [(r, int((decoded[14*r:14*r+14] != target[14*r:14*r+14]).sum()))
                      for r in range(9)]
    return first_dead, per_rule_wrong


if __name__ == '__main__':
    print('staged, no corruption: per-rule wrong-majority counts at death/horizon')
    for s, h in ((0, 0), (4, 0), (5, 0), (6, 0), (7, 0), (1, 0), (3, 0)):
        dead, wrong = staged_rule_drift(s, h)
        # rule names: 0 fuel,1 material,2 W-birth,3 C-birth,4 B-birth,5-8 bank repair
        names = ['fuel', 'mat', 'Wbr', 'Cbr', 'Bbr', 'bk0', 'bk1', 'bk2', 'bk3']
        print(f'  seed={s} hist={h}: dead={dead}  ' +
              ' '.join(f'{n}:{w}' for n, (r, w) in zip(names, wrong)))
