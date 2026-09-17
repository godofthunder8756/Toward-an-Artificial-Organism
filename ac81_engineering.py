"""AC81 engineering v2: replacement across generations of components — final design.

Milestone 2. AC80 froze the internalized recipe (78-bit description + generic decode).
This measures the next claim: the organism's PHYSICAL COMPONENTS (W, C, B) are constructed,
used, and replaced across multiple generations, driven by that internally retained recipe,
and a partial loss (a killed converter and boundary sites) is rebuilt.

Intervention: PARTIAL COMPONENT LOSS at t=8192 — kill 1 C converter (slot 16) and 5 B
boundary sites (slots 0-4). NOT all copies (the catastrophic-destruction analog is out of
scope). The organism must rebuild them via its production rules.

Arms (reuse AC80): internalized (desc damaged+maintained), pristine (desc never damaged),
unmaintained (desc damaged, NOT repaired), no_repair (loop cut).

Endpoints: turnover (births per class), use (repair writes, energy converted, routes),
partial-loss recovery (post-loss births, final populations), description integrity,
survival (bimodality-aware).

Engineering only — no protocol, no final seeds, no claim.
"""
import numpy as np
import ac80
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

LOSS_TICK = ac76.CORRUPT_TICK   # 8192
LOSS_C = (16,)                  # kill 1 C converter
LOSS_B = (0, 1, 2, 3, 4)        # kill 5 B sites


def run(seed, history, arm, loss=True, ticks=ac76.TICKS):
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
    alive_at_loss = None
    births_at_loss = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        if t == LOSS_TICK and loss:
            for idx in LOSS_C:
                o.body.life[idx] = 0
            for j in LOSS_B:
                o.body.boundary[j] = 0
        e = step(o, core, noise, directions, coin, base_map, [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == LOSS_TICK:
            alive_at_loss = not o.body.dead
            births_at_loss = (int(total['W_birth']), int(total['C_birth']), int(total['B_birth']))
        if first_dead is None and o.body.dead:
            first_dead = t
    desc_bits = ac80.read_description(o)
    desc_priority = ac80.decode_perm(desc_bits[ac80.PERM_OFFSET:ac80.PERM_OFFSET + 8])
    return dict(seed=seed, history=history, arm=arm, loss=loss,
                completed=total['active'] == ticks, first_dead=first_dead,
                alive_at_loss=alive_at_loss,
                W_birth=int(total['W_birth']), C_birth=int(total['C_birth']),
                B_birth=int(total['B_birth']),
                births_at_loss=births_at_loss,
                C_birth_post=int(total['C_birth']) - births_at_loss[1],
                B_birth_post=int(total['B_birth']) - births_at_loss[2],
                writes=int(total['writes']), converted=int(total['converted']),
                W_live=int((o.body.life[:16] > 0).sum()), C_live=int((o.body.life[16:20] > 0).sum()),
                B_live=int((o.body.boundary > 0).sum()),
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                description_correct=int((desc_bits == encoded).sum()),
                description_same=int(desc_priority == tuple(priority)),
                energy=int(ac4.inventory(o.body)[0]), material=int(ac4.inventory(o.body)[1]))


def main():
    seeds = tuple(range(8))
    arms = ('internalized', 'pristine', 'unmaintained', 'no_repair')
    print('AC81 engineering v2 — component replacement across generations, 16,384 ticks')
    print('intervention: partial component loss at t=8192 (kill 1 C + 5 B sites)')

    cache = {}
    for arm in arms:
        for s in seeds:
            for h in (0, 1):
                for loss in (True, False):
                    cache[(arm, s, h, loss)] = run(s, h, arm, loss=loss)

    def rows(arm, loss):
        return [cache[(arm, s, h, loss)] for s in seeds for h in (0, 1)]

    print('\nSURVIVAL + DESCRIPTION (with loss):')
    print(f'{"arm":14s} {"surv":>5s} {"descOK(surv)":>13s} {"deaths":>20s}')
    for arm in arms:
        rr = rows(arm, True)
        surv = [r for r in rr if r['completed']]
        dok = sum(1 for r in surv if r['description_correct'] == 78)
        print(f'{arm:14s} {len(surv):3d}/{len(rr)} {str(dok)+"/"+str(len(surv)):>13s} '
              f'{str([r["first_dead"] for r in rr]):>20s}')

    print('\nTURNOVER + USE + RECOVERY (internalized SURVIVORS, with loss):')
    print(f'{"s/h":6s} {"W_b":>5s} {"C_b":>5s} {"B_b":>5s} {"C_post":>6s} {"B_post":>6s} '
          f'{"writes":>6s} {"conv":>5s} {"W":>3s} {"C":>3s} {"B":>3s} {"routes":>14s} {"desc":>4s}')
    for r in rows('internalized', True):
        if r['completed']:
            print(f'{str(r["seed"])+"/"+str(r["history"]):6s} {r["W_birth"]:5d} {r["C_birth"]:5d} '
                  f'{r["B_birth"]:5d} {r["C_birth_post"]:6d} {r["B_birth_post"]:6d} '
                  f'{r["writes"]:6d} {r["converted"]:5d} {r["W_live"]:3d} {r["C_live"]:3d} '
                  f'{r["B_live"]:3d} {str(r["routes"]):14s} {r["description_correct"]:4d}')

    print('\npristine survivors (with loss), for comparison:')
    for r in rows('pristine', True):
        if r['completed']:
            print(f'  {r["seed"]}/{r["history"]} C_b={r["C_birth"]} B_b={r["B_birth"]} '
                  f'C_post={r["C_birth_post"]} B_post={r["B_birth_post"]} '
                  f'routes={r["routes"]} desc={r["description_correct"]}')

    print('\nunmaintained (with loss) — description integrity:')
    um = rows('unmaintained', True)
    print('  descCorrect:', [r['description_correct'] for r in um])
    print('  alive at loss:', [r['alive_at_loss'] for r in um])
    print('  routes:', [r['routes'] for r in um])

    print('\ncontrol (no loss): mechanism inert, same turnover:')
    for arm in ('internalized', 'pristine'):
        rr = rows(arm, False)
        surv = [r for r in rr if r['completed']]
        print(f'  {arm:14s} survive {len(surv)}/{len(rr)} '
              f'W_b={[r["W_birth"] for r in surv]} C_b={[r["C_birth"] for r in surv]}')


if __name__ == '__main__':
    main()
