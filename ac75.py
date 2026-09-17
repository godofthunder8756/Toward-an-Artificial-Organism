"""AC75: erase-on-relinquish makes the reconciled closure world-accommodating.

The AC74 cascade (stale-route persistence window) is fixed by one change in the drop: when the organism
relinquishes a slot it also ERASES the entry (cleared immediately, booked as memory expiry, consistent
with the frozen decay law), so the next contact is blind instead of failing against the stale port. This
joins AC16's re-acquisition machinery (deposit open + restore rule) to the AC71 reconciled closure
(majority read + sticky damage + load-bearing repair), and the claim is that the result survives and
re-acquires through permanent AND temporary route changes with the repair still load-bearing.

The no-erase rival (`restore`) and the no-repair arm are the controls that isolate the erase's
contribution and the repair's necessity.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac71
import ac12
import ac9
import ac4

TICKS = 16384
DEV = ac71.DEV
MOVE_TICK = 8192
MOVE_BACK = 12288
TRANSITIONS = ('perm', 'temp', 'none')

SOURCES = ['ac75.py', 'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py',
           'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py', 'AC75_PROTOCOL_v1.md']


class AllocRestore(ac12.Alloc):
    """Two-way outcome-driven allocation (AC16's rule, restated for the AC71 world): on a productive
    contact the stored port is proven right, so restore maintenance (reset the register bit to 0)."""
    def outcome(self, o, key, e):
        if self.arm not in ('allocate',):
            return
        key = int(key)
        if e['productive'] > 0:
            self._restore(o, e, key)
            self.streak[key] = 0
            return
        self.streak[key] = self.streak.get(key, 0) + 1
        if self.streak[key] >= ac12.STREAK_N:
            self._drop(o, e, key)

    def _restore(self, o, e, key):
        place = ac12.m12.slot_of_key(o.memory, key)
        if place is None:
            return
        off = self.offs[2 * place[0] + place[1]]
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


class AllocErase(AllocRestore):
    """AllocRestore with erase-on-relinquish: the drop also clears the entry immediately."""
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


ALLOC = {'erase': AllocErase, 'restore': AllocRestore}


def mapping_at(base, t, transition):
    m = list(base)
    if transition == 'perm' and t >= MOVE_TICK:
        m[1] = 1 - base[1]
    elif transition == 'temp' and MOVE_TICK <= t < MOVE_BACK:
        m[1] = 1 - base[1]
    return m


def run(seed, history, arm, transition, ticks=TICKS):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    kind = 'erase' if 'erase' in arm else 'restore'
    alloc = ALLOC[kind]('allocate', seed, history)
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
        e = step(o, core, noise, directions, coin, tuple(mapping_at(base_map, t, transition)),
                 [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if first_relinquish is None and alloc.log['dropped']:
            first_relinquish = t
        if first_restore is None and alloc.log.get('restored'):
            first_restore = t
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, transition=transition, ticks=ticks,
                base=list(base_map), move_tick=MOVE_TICK, move_back=MOVE_BACK,
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
                actions=actions, state_hash=o.digest())


def preflight(protocol='AC75_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), \
        f'runner hashes {sorted(set(SOURCES))} but protocol declares {sorted(set(declared))}'
    missing = [s for s in declared if not Path(s).exists()]
    assert not missing, f'declared sources missing: {missing}'
    return declared


def gates(rows):
    def pick(arm, trans):
        return [r for r in rows if r['arm'] == arm and r['transition'] == trans]
    surv = lambda rs: all(r['first_dead'] is None for r in rs)
    erase_perm = pick('erase', 'perm')
    erase_temp = pick('erase', 'temp')
    erase_none = pick('erase', 'none')
    restore_temp = pick('restore', 'temp')
    restore_none = pick('restore', 'none')
    erase_nr_perm = pick('erase_no_repair', 'perm')
    g = {
        'G1_erase_survives_perm': surv(erase_perm),
        'G2_erase_survives_temp': surv(erase_temp),
        'G3_erase_reacquires_and_holds': all(r['route1_correct'] and r['demand'] == [42, 0]
                                             for r in erase_perm),
        'G4_erase_register_intact': (all(r['register'] == [False] * 4 for r in erase_perm)
                                     and all(r['register'] == [False] * 4 for r in erase_temp)),
        'G5_restore_fails_under_change': any(r['first_dead'] is not None for r in restore_temp),
        'G6_repair_load_bearing': all(r['first_dead'] is not None for r in erase_nr_perm),
        'G7_inert_without_change': (all(r['relinquishments'] == 0 and r['demand'] == [42, 0]
                                        for r in erase_none)
                                    and all(e['state_hash'] == r['state_hash']
                                            for e, r in zip(erase_none, restore_none))),
        'G8_completeness_determinism': None,
    }
    return g


def collect(root, seeds):
    preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    arms = ['erase', 'restore', 'erase_no_repair', 'restore_no_repair']
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for arm in arms:
                    for transition in TRANSITIONS:
                        r = run(seed, history, arm, transition)
                        rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
                print(json.dumps(dict(seed=seed, history=history, outcomes=[
                    (r['arm'], r['transition'], r['completed'], r['first_dead'],
                     r['routes'], r['demand'], r['register'])
                    for r in rows[-len(arms) * len(TRANSITIONS):]]), default=str), flush=True)
    g = gates(rows)
    g['G8_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(arms) * len(TRANSITIONS)
        and all(run(s, h, a, t) == orig for s, h, a, t, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0]['transition'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac75_engineering_v1', [0, 1, 2]); return
    collect('ac75_results_v1', [2900, 2901, 2902, 2903])


if __name__ == '__main__':
    main()
