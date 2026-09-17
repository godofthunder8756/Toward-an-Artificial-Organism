"""AC75 addendum: the §4 diagnostic panel for erase-on-relinquish (variant D).

Completes the goal-§4 conditions beyond the permanent move: TEMPORARY outage (port flips at t=8192 and
flips back at t=12288 — two transitions) and UNCHANGED world (no move — the AC71 steady-state control).
Paired with variant C (restore, no erase) so the erase's contribution is isolated.
"""
import json
import numpy as np
import ac75_engineering as e75


def run_sched(seed, history, arm, variant, sched, ticks=16384):
    ac12 = e75.ac12; ac9 = e75.ac9; ac4 = e75.ac4; ac71 = e75.ac71
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    alloc_cls, gate = e75.ALLOC[variant]
    alloc = alloc_cls('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    step = ac71.build(arm, alloc)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    total = ac9.event(); first_dead = None
    n_relinq = 0
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        a = int(ac12.prog.choose(o.body.traces, ac9.observe(o)))
        mapping = list(base_map)
        for k, flip_at, back_at in sched:
            if back_at is None:      # permanent
                if t >= flip_at:
                    mapping[k] = 1 - base_map[k]
            else:                    # temporary
                if flip_at <= t < back_at:
                    mapping[k] = 1 - base_map[k]
        if gate == 'open':
            grow = True; activation = [True, True]
        else:
            grow = t < ac71.DEV; activation = [t < ac71.DEV] * 2
        e = step(o, core, noise, directions, coin, tuple(mapping), activation, grow)
        for k in total:
            total[k] += e.get(k, 0)
        n_relinq = len(alloc.log['dropped'])
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, variant=variant,
                completed=total['active'] == ticks, first_dead=first_dead,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(), register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=n_relinq, restorations=len(alloc.log.get('restored', [])))


def main():
    # sched: (key, flip_at, back_at_or_None)
    perm = [(1, 8192, None)]
    temp = [(1, 8192, 12288)]
    none = []
    rows = []
    for sched_name, sched in (('perm', perm), ('temp', temp), ('none', none)):
        for variant in ('C', 'D'):
            for seed in (0, 1, 2):
                for history in (0, 1):
                    r = run_sched(seed, history, 'closed', variant, sched)
                    r['sched'] = sched_name
                    rows.append(r)
    json.dump(rows, open('/tmp/ac75_addendum.json', 'w'), indent=2, default=str)
    for sched_name in ('perm', 'temp', 'none'):
        for v in ('C', 'D'):
            sub = [r for r in rows if r['sched'] == sched_name and r['variant'] == v]
            n = len(sub)
            surv = sum(1 for r in sub if r['completed'])
            reacq = sum(1 for r in sub if r['routes'][1] is not None)
            held = sum(1 for r in sub if r['demand'] == [42, 0])
            print(f'{sched_name:5s} {v}: survive {surv}/{n}, route1 held {reacq}/{n}, '
                  f'both-routes {held}/{n}, mean relinq {np.mean([r["relinquishments"] for r in sub]):.1f}')


if __name__ == '__main__':
    main()
