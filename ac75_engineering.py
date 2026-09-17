"""AC75 engineering: erase-on-relinquish (goal §4 diagnostic) against the AC74 death cascade.

AC74 located the residual failure: on a route move the organism relinquishes the moved slot but does NOT
erase the entry, so `read(key)` keeps returning the stale port for the entry's full 64-tick life; the
material-low observation then makes the program loop on the failing contact, starve core W to 0, and close
the deposit path (no live W parent) -> death. Goal §4 directs erase-on-relinquish as the diagnostic
intervention: make the drop ALSO clear the entry immediately (booked as expiry, not a new cost), so the
next contact is blind (~1/2 success) instead of failing against a stale port.

Variants (all in the AC71 world: full yields, sticky damage, majority read, 16,384 ticks, move of channel
1 at t=8192):

  A  AC71 as-is                 grow=t<512   activation=[t<DEV]*2  one-way drop
  B  deposit open               grow=True    activation=[T,T]      one-way
  C  B + restore rule           grow=True    activation=[T,T]      two-way
  D  C + erase-on-relinquish    grow=True    activation=[T,T]      two-way + erase

Engineering. No protocol, no final seeds, no claim.
"""
import json
import numpy as np
import ac71
import ac12
import ac9
import ac4
import ac74_engineering as a74


class AllocErase(a74.AllocRestore):
    """Two-way allocation with erase-on-relinquish: dropping a slot also clears the entry."""
    def _drop(self, o, e, key):
        place = ac12.m12.slot_of_key(o.memory, key)
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
        r, s = place
        live = int((o.memory.life[r, s] > 0).sum())
        if live:
            o.memory.life[r, s] = 0
            o.memory.bits[r, s] = 0
            e['memory_expiry'] += live


ALLOC = {'A': (ac12.Alloc, 'gated'), 'B': (ac12.Alloc, 'open'),
         'C': (a74.AllocRestore, 'open'), 'D': (AllocErase, 'open')}


def run_move(seed, history, arm, variant, move_tick=8192, move_keys=(1,), ticks=16384):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = move_keys; ac12.MOVE = move_tick; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    alloc_cls, gate = ALLOC[variant]
    alloc = alloc_cls('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    step = ac71.build(arm, alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event(); actions = {}
    first_dead = None; first_relinquish = None; first_restore = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        a = int(ac12.prog.choose(o.body.traces, ac9.observe(o)))
        actions[a] = actions.get(a, 0) + 1
        mapping = list(base_map)
        if t >= move_tick:
            for k in move_keys:
                mapping[k] = 1 - base_map[k]
        if gate == 'open':
            grow = True
            activation = [True, True]
        else:
            grow = t < ac71.DEV
            activation = [t < ac71.DEV] * 2
        e = step(o, core, noise, directions, coin, tuple(mapping), activation, grow)
        for k in total:
            total[k] += e.get(k, 0)
        if first_relinquish is None and alloc.log['dropped']:
            first_relinquish = t
        if first_restore is None and alloc.log.get('restored'):
            first_restore = t
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, variant=variant, ticks=ticks,
                move_tick=move_tick, base=list(base_map),
                activity=total['active'] / ticks, completed=total['active'] == ticks,
                first_dead=first_dead, first_relinquish=first_relinquish, first_restore=first_restore,
                energy=inv[0], material=inv[1], fuel=inv[2],
                W_live=int((o.body.life[:4] > 0).sum()), C_live=int((o.body.life[16:20] > 0).sum()),
                B_live=int((o.body.boundary > 0).sum()),
                register=[ac12.bit_value(o, off) for off in offs],
                routes=[o.memory.read(k) for k in (0, 1)],
                route1_correct=bool(o.memory.read(1) == (1 - base_map[1])),
                demand=o.memory.demand().tolist(), occupied=int(o.memory.occupied().sum()),
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                contacts=total['contacts'], productive=total['productive'],
                state_hash=o.digest())


def main():
    rows = []
    for seed in (0, 1, 2):
        for history in (0, 1):
            for variant in ('A', 'B', 'C', 'D'):
                for arm in ('closed', 'no_repair'):
                    r = run_move(seed, history, arm, variant)
                    rows.append(r)
                    print(json.dumps(dict(
                        seed=r['seed'], h=r['history'], v=r['variant'], arm=r['arm'],
                        surv=r['completed'], dead=r['first_dead'],
                        relinq=r['first_relinquish'], rest=r['first_restore'],
                        W=r['W_live'], C=r['C_live'], r1=r['routes'][1], r1ok=r['route1_correct'],
                        demand=r['demand'], reg=r['register']), default=str), flush=True)
    json.dump(rows, open('/tmp/ac75_engineering.json', 'w'), indent=2, default=str)
    print('\n--- summary (closed arm, permanent move) ---')
    for v in ('A', 'B', 'C', 'D'):
        sub = [r for r in rows if r['variant'] == v and r['arm'] == 'closed']
        n = len(sub)
        surv = sum(1 for r in sub if r['completed'])
        body = sum(1 for r in sub if r['W_live'] >= 1 and r['C_live'] >= 1)
        reacq = sum(1 for r in sub if r['route1_correct'])
        print(f'{v}: survive {surv}/{n}, body stable {body}/{n}, moved-route re-acquired {reacq}/{n}')


if __name__ == '__main__':
    main()
