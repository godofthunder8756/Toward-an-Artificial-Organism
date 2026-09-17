"""AC81 engineering measure 2: find a clean partial-loss intervention, and check
whether the unmaintained arm's component construction (births) halts before death.

The production-rule corruption (42 bits) and the hard partial loss (2W+1C+5B) both
trigger the AC68 W/C collapse bimodality. This measures MILDER partial losses and
the unmaintained arm's turnover trajectory, to decide the protocol's intervention.
"""
import numpy as np
import ac80
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog


def run_loss(seed, history, arm, loss, ticks=ac76.TICKS):
    """loss: dict of component slots to zero at t=8192 (partial loss)."""
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    encoded = ac80.description_bits(priority)
    o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]
    ac_arm, damage_desc, maintained = ac80.ARM_PARTS[arm]
    reg_fn = ac80.reg_maintained if maintained else (ac80.reg_pristine if ac_arm == 'regen' else None)
    step = ac80.build(ac_arm, alloc, reg_fn)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    first_dead = None
    births_at_loss = None
    births_after = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        if t == ac76.CORRUPT_TICK and loss:
            for idx in loss.get('W', []):
                o.body.life[idx] = 0
            for idx in loss.get('C', []):
                o.body.life[idx] = 0
            for j in loss.get('B', []):
                o.body.boundary[j] = 0
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == ac76.CORRUPT_TICK:
            births_at_loss = (total['W_birth'], total['C_birth'], total['B_birth'])
        if first_dead is None and o.body.dead:
            first_dead = t
    births_after = (total['W_birth'], total['C_birth'], total['B_birth'])
    return dict(seed=seed, history=history, arm=arm, completed=total['active'] == ticks,
                first_dead=first_dead, births_at_loss=births_at_loss,
                births_after=births_after,
                W_live=int((o.body.life[:16] > 0).sum()), C_live=int((o.body.life[16:20] > 0).sum()),
                B_live=int((o.body.boundary > 0).sum()),
                desc_correct=int((ac80.read_description(o) == encoded).sum()))


def run_traj(seed, history, arm, ticks=ac76.TICKS):
    """Unmaintained arm: births trajectory every 1024 ticks, to see if construction halts before death."""
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    encoded = ac80.description_bits(priority)
    o.body.traces[1, :ac80.DESC_BITS] = encoded[:, None]
    ac_arm, damage_desc, maintained = ac80.ARM_PARTS[arm]
    reg_fn = ac80.reg_maintained if maintained else (ac80.reg_pristine if ac_arm == 'regen' else None)
    step = ac80.build(ac_arm, alloc, reg_fn)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    traj = []
    first_dead = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t % 1024 == 0:
            traj.append((t, total['W_birth'], total['C_birth'], total['B_birth'],
                         int((ac80.read_description(o) == encoded).sum()),
                         int((o.body.life[:16] > 0).sum()), int((o.body.life[16:20] > 0).sum())))
        if first_dead is None and o.body.dead:
            first_dead = t
    return dict(seed=seed, history=history, arm=arm, first_dead=first_dead, traj=traj)


def main():
    seeds = range(4)
    print('=== MILDER PARTIAL LOSSES (internalized arm, t=8192) ===')
    variants = {
        'kill 1 W (slot 0)': {'W': [0]},
        'kill 1 C (slot 16)': {'C': [16]},
        'kill 5 B sites': {'B': [0, 1, 2, 3, 4]},
        'kill 1 W + 5 B': {'W': [0], 'B': [0, 1, 2, 3, 4]},
    }
    for name, loss in variants.items():
        res = []
        for s in seeds:
            for h in (0, 1):
                res.append(run_loss(s, h, 'internalized', loss))
        surv = sum(1 for r in res if r['completed'])
        # did the component get rebuilt? compare final live vs the loss
        print(f'{name:20s} survive {surv}/{len(res)}  deaths {[r["first_dead"] for r in res]}')

    print('\n=== UNMAINTAINED ARM: construction halts before death? ===')
    for s in (0, 1):
        r = run_traj(s, 0, 'unmaintained')
        print(f'seed {s}/0 first_dead={r["first_dead"]}')
        print(f'  {"t":>6s} {"W_b":>6s} {"C_b":>5s} {"B_b":>6s} {"desc":>5s} {"W":>3s} {"C":>3s}')
        for (t, wb, cb, bb, dc, wl, cl) in r['traj']:
            print(f'  {t:6d} {wb:6d} {cb:5d} {bb:6d} {dc:5d} {wl:3d} {cl:3d}')

    print('\n=== INTERNALIZED ARM (control): construction continues ===')
    for s in (0, 1):
        r = run_traj(s, 0, 'internalized')
        print(f'seed {s}/0 first_dead={r["first_dead"]}')
        print(f'  {"t":>6s} {"W_b":>6s} {"C_b":>5s} {"B_b":>6s} {"desc":>5s} {"W":>3s} {"C":>3s}')
        for (t, wb, cb, bb, dc, wl, cl) in r['traj']:
            print(f'  {t:6d} {wb:6d} {cb:5d} {bb:6d} {dc:5d} {wl:3d} {cl:3d}')


if __name__ == '__main__':
    main()
