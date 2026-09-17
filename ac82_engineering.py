"""AC82 engineering probe: combine reconstruction + description maintenance + route-move adaptation.

Not a frozen runner. Measures whether the combined architecture (AC80 internalized recipe +
AC75 erase-on-relinquish route-move accommodation) survives, recovers and re-acquires
unconditionally. Sweeps engineering seeds and prints a compact outcome table.

Declared change vs AC75's AllocErase: `_restore` fires only when the slot actually reads as
relinquished (majority >= REGISTER_THRESHOLD), not on any set replica. AC75's `_restore`
(fires on any set replica) is redundant with the bank-0 repair and, in the combined desc+reg
world, starves the renewal budget and loses routes (measured: seed 1 loses route 0).
"""
import numpy as np
import ac80
import ac75
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog
from ac12 import m12

TICKS = 16384
CORRUPT_TICK = 8192
CORRUPT_BITS = 8
MOVE_TICK = 8192

ARMS = ('internalized', 'pristine', 'unmaintained', 'no_repair', 'restore')

# (ac_arm for ac71.build-style surgery, damage the description?, maintain it?, erase-on-relinquish?)
ARM_PARTS = {
    'internalized':  ('regen',     True,  True,  True),
    'pristine':      ('regen',     False, False, True),
    'unmaintained':  ('regen',     True,  False, True),
    'no_repair':     ('no_repair', True,  False, True),
    'restore':       ('regen',     True,  True,  False),
}


class AllocErase(ac75.AllocErase):
    def _restore(self, o, e, key):
        place = m12.slot_of_key(o.memory, key)
        if place is None:
            return
        off = self.offs[2 * place[0] + place[1]]
        if not ac12.bit_value(o, off):   # already maintained (majority 0) -> no-op
            return
        sites = o.body.traces[0, off]
        n = int((sites != 0).sum())
        if n == 0:
            return
        cap = min(32, 8 * int(ac4.available(o.body)[:4].sum()), o.body.energy, o.body.material)
        if n > cap:
            return
        o.body.energy -= n; o.body.material -= n
        e['spent_e'] += n; e['spent_m'] += n; e['writes'] += n
        sites[:] = 0
        self.log.setdefault('restored', []).append(list(place))


class AllocRestore(AllocErase):
    def _drop(self, o, e, key):
        place = m12.slot_of_key(o.memory, key)
        if place is None:
            return
        off = self.offs[2 * place[0] + place[1]]
        sites = o.body.traces[0, off]
        n = int((sites != 1).sum())
        if n == 0:
            return
        cap = min(32, 8 * int(ac4.available(o.body)[:4].sum()), o.body.energy, o.body.material)
        if n > cap:
            return
        o.body.energy -= n; o.body.material -= n
        e['spent_e'] += n; e['spent_m'] += n; e['writes'] += n
        sites[:] = 1
        self.streak[key] = 0
        self.log['dropped'].append(list(place))


ALLOC = {True: AllocErase, False: AllocRestore}


def mapping_at(base, t, transition):
    m = list(base)
    if transition == 'perm' and t >= MOVE_TICK:
        m[1] = 1 - base[1]
    return m


def run(seed, history, arm, transition, corrupt=True, ticks=TICKS):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    ac_arm, damage_desc, maintained, erase = ARM_PARTS[arm]
    alloc = ALLOC[erase]('allocate', seed, history)
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
    total = ac9.event()
    first_dead = None
    alive_at_intervention = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage_desc:
            o.body.traces[1, :ac80.DESC_BITS] |= (rng1.random((ac80.DESC_BITS, 7)) < .0001).astype(np.uint8)
        if t == CORRUPT_TICK and corrupt:
            correct = prog.program(priority)
            for bit in range(CORRUPT_BITS):
                w = 1 - int(correct[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(correct[bit])
        e = step(o, core, noise, directions, coin, tuple(mapping_at(base_map, t, transition)),
                 [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == CORRUPT_TICK:
            alive_at_intervention = not o.body.dead
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    target = prog.program(priority)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    desc_bits = ac80.read_description(o)
    desc_priority = ac80.decode_perm(desc_bits[ac80.PERM_OFFSET:ac80.PERM_OFFSET + 8])
    return dict(seed=seed, history=history, arm=arm, transition=transition, corrupt=corrupt,
                completed=total['active'] == ticks, first_dead=first_dead,
                alive_at_intervention=alive_at_intervention,
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != target[:CORRUPT_BITS]).sum()),
                description_correct=int((desc_bits == encoded).sum()),
                description_valid=int(sorted(desc_priority) == list(range(4))),
                description_same=int(desc_priority == tuple(priority)),
                routes=[o.memory.read(k) for k in (0, 1)],
                route1_correct=bool(o.memory.read(1) == (1 - base_map[1])),
                demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                W=int((o.body.life[:16] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2], state_hash=o.digest())


def main():
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [0, 1, 2, 3, 4, 5, 6, 7]
    rows = []
    for seed in seeds:
        for history in (0, 1):
            for arm in ARMS:
                for transition in ('perm', 'none'):
                    for corrupt in (True, False):
                        r = run(seed, history, arm, transition, corrupt)
                        rows.append(r)
                        print(f"s{seed}h{history} {arm:13s} {transition:4s} corr={int(corrupt)} "
                              f"done={int(r['completed'])} dead={r['first_dead']} fw={r['flipped_still_wrong']} "
                              f"desc={r['description_correct']}/78 dv={r['description_valid']} "
                              f"routes={r['routes']} demand={r['demand']} reg={r['register']} "
                              f"rel={r['relinquishments']} rst={r['restorations']}")
    print('\n=== SUMMARY (perm, corrupt=True) ===')
    for arm in ARMS:
        rs = [r for r in rows if r['arm'] == arm and r['transition'] == 'perm' and r['corrupt']]
        surv = sum(r['completed'] for r in rs)
        recov = sum(r['completed'] and r['flipped_still_wrong'] == 0 and r['description_correct'] == 78
                    and r['routes'][0] is not None and r['routes'][1] is not None and r['route1_correct']
                    for r in rs)
        print(f"{arm:13s} survive {surv}/{len(rs)}  recover+reacquire {recov}/{len(rs)}  "
              f"deaths {[r['first_dead'] for r in rs if not r['completed']]}")
    print('\n=== SUMMARY (none, corrupt=False) — inertness control ===')
    for arm in ('internalized', 'restore'):
        rs = [r for r in rows if r['arm'] == arm and r['transition'] == 'none' and not r['corrupt']]
        print(f"{arm:13s} survive {sum(r['completed'] for r in rs)}/{len(rs)} rel={[r['relinquishments'] for r in rs]}")


if __name__ == '__main__':
    main()
