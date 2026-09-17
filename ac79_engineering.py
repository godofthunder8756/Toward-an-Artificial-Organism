"""AC79 engineering: description maintenance — no hidden pristine backup.

The task "description maintenance" was premised on the priority being SELF-produced; AC78
falsified that premise (the production signal is a locked, path-dependent fixed point). But the
task's core survives independent of self-production: AC76's frozen turnover stores the 8-bit
priority description in dead bank 1, where the damage stream never reaches it and no action
repairs it — a hidden pristine backup, which the goal rules out as evidence of endogenous
reconstruction.

This engineering probe re-scopes the question to what is live and independent:

    Can the 8-bit priority description be stored in the vulnerable substrate, PUT IN the damage
    stream, and maintained through the organism's own paid vulnerable machinery — so the
    compressed-description turnover does not rely on a hidden pristine backup?

Mechanism under test (single declared change from AC76): (1) apply the same sticky 1e-4 damage
to bank 1's 8 description bits; (2) when the program's own corruption observation (obs bit 2)
fires, the re-instantiation step first repairs the description's 7-replica minority back to its
majority (paid, same primitive), then re-instantiates the program from the repaired description.

Engineering only. No protocol, no final seeds, no claim.
"""
import numpy as np
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

ORIG = ac76.reg_from_priority          # the frozen re-instantiation (no description repair)


def reg_description(o, e):
    """Paid majority-restore of the 8-bit description in bank 1; return decoded priority."""
    b = o.body
    bits = (b.traces[1, :8].sum(axis=-1) > 3).astype(np.uint8)
    sites = np.argwhere(b.traces[1, :8] != bits[:, None])
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, idx[:, 0], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n
    return ac76.decode_priority(bits)


def reg_maintained(o, e):
    """Description-maintained re-instantiation: repair description, then re-instantiate program."""
    b = o.body
    if not (ac9.observe(o) & 4):
        return
    priority = reg_description(o, e)
    if sorted(priority) != list(range(4)):
        return
    target = prog.program(priority)
    dead_idx = 4 + priority.index(3)
    exclude = {14 * dead_idx + 1 + k for k in range(4)}
    sites = np.argwhere(b.traces[0, :prog.PROGRAM_BITS] != target[:, None])
    sites = sites[[i for i in range(len(sites)) if int(sites[i, 0]) not in exclude]]
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    n = min(cap, len(sites))
    if n:
        idx = sites[:n]
        b.traces[0, idx[:, 0], idx[:, 1]] = target[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n


def make_step(arm, alloc, maintained):
    ac76.reg_from_priority = reg_maintained if maintained else ORIG
    return ac76.build(arm, alloc)


def run(seed, history, arm, damage_desc, maintained, corrupt=True, ticks=ac76.TICKS):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac12.Alloc('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    encoded = ac76.encode_priority(priority)
    o.body.traces[1, :8] = encoded[:, None]
    step = make_step(arm, alloc, maintained)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])      # independent damage stream for bank 1
    total = ac9.event()
    first_dead = None
    alive_at_corruption = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :8] |= (rng1.random((8, 7)) < .0001).astype(np.uint8)
        if t == ac76.CORRUPT_TICK and corrupt:
            correct = prog.program(priority)
            for bit in range(ac76.CORRUPT_BITS):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == ac76.CORRUPT_TICK:
            alive_at_corruption = not o.body.dead
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    target = prog.program(priority)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    desc_bits = (o.body.traces[1, :8].sum(axis=-1) > 3).astype(np.uint8)
    desc_priority = ac76.decode_priority(desc_bits)
    return dict(seed=seed, history=history, arm=arm, damage_desc=damage_desc,
                maintained=maintained, corrupt=corrupt,
                completed=total['active'] == ticks, first_dead=first_dead,
                alive_at_corruption=alive_at_corruption,
                program_correct=int((decoded == target).sum()),
                flipped_still_wrong=int((decoded[:ac76.CORRUPT_BITS] != target[:ac76.CORRUPT_BITS]).sum()),
                description_correct=int((desc_bits == encoded).sum()),
                description_valid=int(sorted(desc_priority) == list(range(4))),
                description_same=int(desc_priority == tuple(priority)),
                energy=inv[0], material=inv[1], fuel=inv[2])


CONFIGS = [
    ('maintained  ', 'regen',    True,  True),   # desc damaged + repaired + re-instantiated
    ('pristine    ', 'regen',    False, False),  # AC76 as-is: desc never damaged (hidden backup)
    ('unmaintained', 'regen',    True,  False),  # desc damaged, NO repair
    ('no_repair   ', 'no_repair', True,  False),  # loop cut (load-bearing control)
]


def main():
    seeds = tuple(range(8))
    print('AC79 engineering — description in damage stream + paid maintenance, 16,384 ticks')
    print('program corruption at t=8192: majority of program bits 0-7 flipped (AC76 intervention)')
    print(f'seeds {seeds[0]}..{seeds[-1]} x 2 histories = {2*len(seeds)} individuals/arm\n')

    # viability scan (no corruption): who is still alive at the corruption tick?
    scan = [run(s, h, 'regen', True, True, corrupt=False) for s in seeds for h in (0, 1)]
    alive = {(r['seed'], r['history']) for r in scan if r['alive_at_corruption']}
    print(f'viability scan (no corruption): {len(alive)}/{2*len(seeds)} alive at t=8192\n')

    print(f'{"arm":13s} {"survive":>7s} {"died<8192":>9s} {"alive@8192":>10s} '
          f'{"recover":>7s} {"descOK":>6s} {"descValid":>9s}')
    for arm, ac_arm, dd, mt in CONFIGS:
        rows = [run(s, h, ac_arm, dd, mt) for s in seeds for h in (0, 1)]
        survived = sum(1 for r in rows if r['completed'])
        pre_dead = sum(1 for r in rows if not r['alive_at_corruption'])
        alive_rows = [r for r in rows if r['alive_at_corruption']]
        recovered = sum(1 for r in alive_rows if r['flipped_still_wrong'] == 0 and r['completed'])
        dok = sum(1 for r in rows if r['description_correct'] == 8)
        dval = sum(1 for r in rows if r['description_valid'] == 1)
        print(f'{arm:13s} {survived:4d}/{len(rows)}  {pre_dead:9d} {len(alive_rows):10d} '
              f'{recovered:4d}/{len(alive_rows)} {dok:3d}/{len(rows)} {dval:9d}')

    print('\nper-individual detail (alive@8192 individuals only):')
    for arm, ac_arm, dd, mt in CONFIGS:
        rows = [r for r in [run(s, h, ac_arm, dd, mt) for s in seeds for h in (0, 1)]
                if r['alive_at_corruption']]
        fw = [r['flipped_still_wrong'] for r in rows]
        ds = [r['description_same'] for r in rows]
        dd_ = [r['first_dead'] for r in rows]
        print(f'  {arm:13s} flipWrong {fw}  descSame {ds}  deaths {dd_}')

    print('\ncontrol (no corruption at t=8192): mechanism must introduce no spurious change')
    for arm, ac_arm, dd, mt in [('maintained', 'regen', True, True), ('pristine', 'regen', False, False)]:
        rows = [run(s, h, ac_arm, dd, mt, corrupt=False) for s in seeds for h in (0, 1)]
        surv = sum(1 for r in rows if r['completed'])
        fw = [r['flipped_still_wrong'] for r in rows]
        print(f'  {arm:13s} survive {surv}/{len(rows)}  flippedStillWrong {fw}')


if __name__ == '__main__':
    main()
