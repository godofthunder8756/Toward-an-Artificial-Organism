"""AC99-D2: a 3-bit Gray-coded relinquishment streak vs the binary streak.

The hypothesis under test: the binary streak's `3->4` increment (0b011 -> 0b100) changes
three logical bits = 21 replicas, so `ac95._cap = min(32, 8*W, energy, material)` needs
W >= 3. On AC98 seed 4436 (priority [1,3,0,2]) the post-move streak build is phase-shifted
into a repeated W-death window, the 3->4 increment is refused (W < 3), the streak stalls at
3, the drop never fires, and the organism dies (8430) — the AC98 G1 failure. A 3-bit
reflected-Gray counter makes every successive increment change ONE logical bit = 7 replicas
(needs W >= 1), so the relinquishment decision may become affordable at W = 1-2.

Held constant (everything but the counter's code): STREAK_N = 6, the sticky 1e-4 damage
model, the 7-replica majority read (threshold 4), resource prices (1 energy + 1 material
per replica), and the AC98/AC99-D1 reserve policy (level 21, drop/stall/wlow triggers,
atomic release+disarm). The streak still lives in the same dead-rule free bits
(`traces[0, streak_offs]`, resolved once at acquisition by `ac96.streak_offsets`), is damaged
by the same sticky program stream, and is repaired by the same paid bank-0 majority-restore.
The ONLY change is the encoding: binary <-> reflected Gray.

No protocol, no freeze — engineering only (D2 is a code-vs-code comparison on the AC98 finals
4436-4439 and the D1/D2 seeds 4412-4415; D3/D4 build the AC99 study on this evidence).

Gray code (3-bit reflected, g = n ^ (n >> 1)):
    n: 0 1 2 3 4 5 6 7
    g: 0 1 3 2 6 7 5 4   (000 001 011 010 110 111 101 100)
decode (3-bit): n = g ^ (g >> 1) ^ (g >> 2).
"""
from pathlib import Path
import json
import sys
import numpy as np
import ac99            # reserve primitives + constants + AllocEraseReserve (binary) + run()
import ac96            # streak storage/offsets + AllocEraseMaintained (base class)
import ac95            # _cap, build, maintain, Succession
import ac12
import ac4
import ac71
import ac9
import ac5_program as prog
import ac97

TICKS = ac95.TICKS
CORRUPT_TICK = ac95.CORRUPT_TICK
CORRUPT_BITS = ac95.CORRUPT_BITS
MOVE_TICK = ac95.MOVE_TICK
DEV = ac71.DEV
STREAK_N = ac12.STREAK_N
STREAK_THRESHOLD = ac96.STREAK_THRESHOLD

# reserve constants + primitives, unchanged from ac99 (the D1 atomic-release fix)
RESERVE_OFFS = ac99.RESERVE_OFFS
RESERVE_LEVEL = ac99.RESERVE_LEVEL
RESERVE_THRESHOLD = ac99.RESERVE_THRESHOLD
RESERVE_TRIGGER = ac99.RESERVE_TRIGGER
reserve_read = ac99.reserve_read
reserve_minority = ac99.reserve_minority
write_reserve = ac99.write_reserve
arm_reserve = ac99.arm_reserve
release_reserve = ac99.release_reserve
reg_reserve = ac99.reg_reserve
maintain = ac99.maintain           # ac95.maintain + reg_reserve (reserve bit repair)


# ---------------- Gray code + the Gray streak in maintained state ----------------
def gray_encode(n):
    """3-bit reflected Gray code of n (0..7)."""
    return n ^ (n >> 1)


def gray_decode(g):
    """Decode a 3-bit reflected Gray code to 0..7."""
    b = g ^ (g >> 1)
    b ^= b >> 2
    return b & 7


def gray_streak_read(o, key, streak_offs):
    """Majority read (>= STREAK_THRESHOLD) of the 3-bit GRAY counter for `key`.

    The three bits are read LSB-first (same offsets/order as ac96.streak_read) and the
    resulting 3-bit pattern is Gray-decoded to the count.
    """
    offs = streak_offs[3 * key: 3 * key + 3]
    g = sum(int(o.body.traces[0, off].sum() >= STREAK_THRESHOLD) << k
            for k, off in enumerate(offs))
    return gray_decode(g)


def gray_streak_write(o, e, key, new, streak_offs):
    """Atomic, W-gated paid write of the maintained GRAY streak for `key` to `new` (0..7).

    Encodes `new` as its Gray code, writes only the replicas whose value differs from the
    target, and refuses the whole transition if that count exceeds the produced machinery's
    paid capacity `ac95._cap`. A refused transition writes nothing (a partial Gray-counter
    transition would corrupt the value). Returns the number of replicas written (0 => refused).

    Same atomicity/W-gate semantics as ac96.streak_write; the only difference is the target
    bits are `gray_encode(new)` instead of `new`.
    """
    offs = np.array(streak_offs[3 * key: 3 * key + 3])
    if gray_streak_read(o, key, streak_offs) == new:
        return 0
    g = gray_encode(new)
    targets = np.array([(g >> k) & 1 for k in range(3)], dtype=np.uint8)
    sites = np.argwhere(o.body.traces[0, offs] != targets[:, None])
    n = len(sites)
    cap = ac95._cap(o.body)
    if n > cap:
        return 0
    for i, r in sites:
        o.body.traces[0, offs[i], r] = targets[i]
    o.body.energy -= n
    o.body.material -= n
    e['spent_e'] += n
    e['spent_m'] += n
    e['writes'] += n
    e['streak_writes'] = e.get('streak_writes', 0) + n
    return n


class GrayAllocEraseReserve(ac99.AllocEraseReserve):
    """AllocEraseReserve with the relinquishment streak read/written in GRAY code.

    Identical to ac99.AllocEraseReserve except the streak read/write calls go through
    `gray_streak_read`/`gray_streak_write`. The reserve (arm/release/repair) and the drop
    (register write + memory expiry) are byte-for-byte the ac99 logic.
    """

    def outcome(self, o, key, e):
        if self.arm != 'allocate':
            return
        key = int(key)
        if e['productive'] > 0:
            self._restore(o, e, key)
            gray_streak_write(o, e, key, 0, self.streak_offs)
            if self.reserve and key == 1 and self.now >= DEV:
                r = arm_reserve(o, e)
                if r:
                    self.reserve_events.append((self.now, 'arm', r))
            return
        cur = gray_streak_read(o, key, self.streak_offs)
        dropped = 0
        if cur + 1 >= STREAK_N:
            n_before = len(self.log['dropped'])
            self._drop(o, e, key)
            dropped = 1 if len(self.log['dropped']) > n_before else 0
        else:
            r = gray_streak_write(o, e, key, cur + 1, self.streak_offs)
            if r == 0 and self.reserve and reserve_read(o):
                rel = release_reserve(o, e)
                if rel:
                    self.reserve_events.append((self.now, 'stall', rel))
        if self.reserve and key == 1 and reserve_read(o):
            W = int(ac4.available(o.body)[:4].sum())
            if W < 3 and o.body.material <= 64:
                rel = release_reserve(o, e)
                if rel:
                    self.reserve_events.append((self.now, 'wlow', rel))
        self.streak_events.append((self.now, key, cur,
                                   gray_streak_read(o, key, self.streak_offs), dropped))

    def _drop(self, o, e, key):
        place = ac12.m12.slot_of_key(o.memory, key)
        if place is None:
            return
        off = self.offs[2 * place[0] + place[1]]
        sites = o.body.traces[0, off]
        n = int((sites != 1).sum())
        if n == 0:
            return
        if self.reserve and o.body.material < RESERVE_LEVEL:
            r = release_reserve(o, e)
            if r:
                self.reserve_events.append((self.now, 'drop', r))
        cap = min(32, 8 * int(ac4.available(o.body)[:4].sum()), o.body.energy, o.body.material)
        if n > cap:
            return
        o.body.energy -= n
        o.body.material -= n
        e['spent_e'] += n
        e['spent_m'] += n
        e['writes'] += n
        sites[:] = 1
        gray_streak_write(o, e, key, 0, self.streak_offs)
        self.log['dropped'].append(list(place))
        r, s = place
        live = int((o.memory.life[r, s] > 0).sum())
        if live:
            o.memory.life[r, s] = 0
            o.memory.bits[r, s] = 0
            e['memory_expiry'] += live


# ---------------- the run (faithful to ac99._run_internal, Gray streak only) ----------------
def _run_internal(seed, history, arm, reserve, damage, corrupt, transition,
                  ticks, move_tick, record_trace=False, swap_at=None,
                  damage_rate=1e-4):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    assert arm == 'gated', 'the maintained/reserve arms are the fixed architecture only'
    alloc = GrayAllocEraseReserve('allocate', seed, history, reserve=reserve)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    streak_offs = ac96.streak_offsets(o)
    alloc.streak_offs = streak_offs
    reg_offs = ac95.resolve_offsets(o)
    build_offs = reg_offs + streak_offs
    encoded = ac95.description_bits(priority)
    o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
    acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    cfg = dict(ac95.ARM_PARTS[arm])
    cfg['reserve'] = reserve
    if cfg.get('block_W'):
        raise NotImplementedError('AC99-D2 supports the gated arm only')
    succ = ac95.Succession('real', encoded)
    step = ac95.build(cfg['ac_arm'], alloc, succ, build_offs, cfg)
    step.__globals__['maintain'] = maintain
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    total['reg_writes'] = 0
    total['succ_writes'] = 0
    total['ctrl_writes'] = 0
    total['timer_increments'] = 0
    total['timer_resets'] = 0
    total['split_events'] = 0
    total['streak_writes'] = 0
    total['reserve_writes'] = 0
    total['reserve_m'] = 0
    total['reserve_released_m'] = 0
    post_move = {'W_birth': 0, 'C_birth': 0, 'B_birth': 0}
    first_dead = None
    drop_ticks = []
    restore_ticks = []
    trace = [] if record_trace else None
    was_bound = {0: False, 1: False}
    seen_bound = {0: False, 1: False}
    reacquire_ticks = {0: [], 1: []}
    swap_applied = False
    for t in range(ticks):
        alloc.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = GrayAllocEraseReserve('allocate', seed, history, reserve=reserve)
            alloc.streak_offs = streak_offs
            alloc.offs = offs
            alloc.shadow = o.body.traces[0].copy()
            alloc.now = t
            step.__globals__['succ'] = succ
            step.__globals__['alloc'] = alloc
            step.__globals__['allowance'] = alloc.allowance
            swap_applied = True
        core = (rng.random((126, 7)) < damage_rate).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage:
            g = ac95.read_pointer(o)
            slots = {g}
            active, phase, last = ac95.ctrl_fields(o)
            if active:
                slots.add((g + 1) % ac95.SLOTS)
            for s in slots:
                off = ac95.slot_offset(s)
                o.body.traces[1, off:off + ac95.SLOT_BITS] |= (rng1.random((ac95.SLOT_BITS, 7)) < .0001).astype(np.uint8)
            o.body.traces[1, ac95.PTR_OFFS] |= (rng1.random((2, 7)) < .0001).astype(np.uint8)
            o.body.traces[1, ac95.CTRL_OFFS] |= (rng1.random((ac95.CTRL_BITS, 7)) < .0001).astype(np.uint8)
            if reserve:
                o.body.traces[1, RESERVE_OFFS] |= (rng1.random(7) < .0001).astype(np.uint8)
        if t == CORRUPT_TICK and corrupt:
            for bit in range(CORRUPT_BITS):
                w = 1 - int(acquired[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(acquired[bit])
        step.__globals__['now'] = t
        prev_drops = len(alloc.log['dropped'])
        prev_restores = len(alloc.log.get('restored', []))
        e = step(o, core, noise, directions, coin,
                 tuple(ac95.mapping_at(base_map, t, transition, move_tick)), [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t >= move_tick:
            for k in post_move:
                post_move[k] += e.get(k, 0)
        for k in (0, 1):
            now_bound = o.memory.read(k) is not None
            if was_bound[k] is False and now_bound and seen_bound[k]:
                reacquire_ticks[k].append(t)
            if now_bound:
                seen_bound[k] = True
            was_bound[k] = now_bound
        if len(alloc.log['dropped']) > prev_drops:
            place = alloc.log['dropped'][-1]
            drop_ticks.append((t, list(place),
                               ac12.bit_value(o, offs[2 * place[0] + place[1]])))
        if len(alloc.log.get('restored', [])) > prev_restores:
            restore_ticks.append((t, list(alloc.log.get('restored', [])[-1])))
        if record_trace:
            trace.append((t, o.digest()))
        if first_dead is None and o.body.dead:
            first_dead = t
    arm_events = [ev for ev in alloc.reserve_events if ev[1] == 'arm']
    rel_events = [ev for ev in alloc.reserve_events if ev[1] in ('drop', 'stall', 'wlow')]
    rel_kinds = [(ev[0], ev[1]) for ev in rel_events]
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, reserve=reserve, damage=damage,
                corrupt=corrupt, transition=transition, ticks=ticks, move_tick=move_tick,
                completed=total['active'] == ticks, first_dead=first_dead,
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                drop_ticks=drop_ticks,
                restore_ticks=restore_ticks,
                streak_final={0: gray_streak_read(o, 0, streak_offs),
                              1: gray_streak_read(o, 1, streak_offs)},
                streak_events=getattr(alloc, 'streak_events', []),
                reacquire_ticks=reacquire_ticks,
                reserve_armed_end=reserve_read(o),
                reserve_minority_end=reserve_minority(o),
                reserve_arm_ticks=[ev[0] for ev in arm_events],
                reserve_release_ticks=[ev[0] for ev in rel_events],
                reserve_release_kinds=rel_kinds,
                swap_applied=swap_applied,
                reserve_m=int(total['reserve_m']),
                reserve_released_m=int(total['reserve_released_m']),
                reserve_writes=int(total['reserve_writes']),
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                W_births=int(total['W_birth']), C_births=int(total['C_birth']),
                B_births=int(total['B_birth']),
                W_births_post_move=int(post_move['W_birth']),
                C_births_post_move=int(post_move['C_birth']),
                B_births_post_move=int(post_move['B_birth']),
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                streak_writes=int(total['streak_writes']),
                state_hash=o.digest()), o, trace


def run(seed, history, arm='gated', reserve=False, damage=True, corrupt=False,
        transition='perm', ticks=TICKS, move_tick=MOVE_TICK):
    """Run one individual with the GRAY streak. `reserve=True` is the Gray reserve arm."""
    row, o, _ = _run_internal(seed, history, arm, reserve, damage, corrupt,
                              transition, ticks, move_tick, record_trace=False)
    return row


# ---------------- cost table (binary vs Gray, per transition) ----------------
def transition_cost_table():
    """Replica cost of each streak transition in binary vs Gray (7 replicas/bit).

    Increments 0->1 ... 4->5 (STREAK_N=6 means 5 is the highest reached; the drop fires at
    cur+1 >= 6, i.e. cur = 5) plus the reset 5->0. `bits` is the number of logical bits that
    change; `replicas = 7 * bits`.
    """
    rows = []
    for cur in range(5):
        nxt = cur + 1
        b_bits = (cur ^ nxt).bit_count()
        g_bits = (gray_encode(cur) ^ gray_encode(nxt)).bit_count()
        rows.append(dict(transition=f'{cur}->{nxt}', binary_bits=b_bits,
                         binary_replicas=7 * b_bits, gray_bits=g_bits,
                         gray_replicas=7 * g_bits))
    # reset 5->0 (the drop reset)
    b_bits = (5 ^ 0).bit_count()
    g_bits = (gray_encode(5) ^ gray_encode(0)).bit_count()
    rows.append(dict(transition='5->0 (reset)', binary_bits=b_bits,
                     binary_replicas=7 * b_bits, gray_bits=g_bits,
                     gray_replicas=7 * g_bits))
    return rows


def damage_read_table():
    """The majority-read distribution under sticky single-bit damage (0->1) for each count.

    For each counter value 0..5, flip each currently-0 bit (sticky SET is a no-op on a set
    bit) and report the decoded count in binary vs Gray. A value >= STREAK_N (=6) is a
    read that triggers an immediate drop on the next unproductive contact; a value BELOW the
    current count is a *decrease* (sticky damage erases progress).
    """
    rows = []
    for v in range(6):
        b = v
        g = gray_encode(v)
        b_out, g_out = set(), set()
        for bit in range(3):
            if not (b >> bit) & 1:
                b_out.add(b | (1 << bit))
            if not (g >> bit) & 1:
                g_out.add(gray_decode(g | (1 << bit)))
        rows.append(dict(value=v, binary_flip_reads=sorted(b_out),
                         gray_flip_reads=sorted(g_out)))
    return rows


# ---------------- engineering collector (binary vs Gray, reserve arm only) ----------------
def collect(root, seeds, transition='perm', damage=True, corrupt=False):
    """Compare the binary reserve arm (ac99) against the Gray reserve arm on the same
    individuals, per seed/history. Reports the cost table, the 4436 outcome, any regression,
    and the damaged-read distribution. No protocol, no freeze."""
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for code in ('binary', 'gray'):
                    if code == 'binary':
                        r = ac99.run(seed, history, 'gated', reserve=True, damage=damage,
                                     corrupt=corrupt, transition=transition)
                    else:
                        r = run(seed, history, 'gated', reserve=True, damage=damage,
                                corrupt=corrupt, transition=transition)
                    r['code'] = code
                    rows.append(r)
                    f.write(json.dumps(r) + '\n')
                    f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['code'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['streak_final'],
                 r['reserve_release_kinds'], r['streak_writes'])
                for r in rows[-4:]]), default=str), flush=True)
    by = {}
    for r in rows:
        by[(r['seed'], r['history'], r['code'])] = r
    per_ind = {}
    for seed in seeds:
        for history in (0, 1):
            b = by[(seed, history, 'binary')]
            g = by[(seed, history, 'gray')]
            per_ind[f'{seed}/{history}'] = dict(
                seed=seed, history=history,
                binary=dict(completed=b['completed'], first_dead=b['first_dead'],
                            relinquishments=b['relinquishments'], routes=b['routes'],
                            streak_final=b['streak_final'], streak_writes=b['streak_writes'],
                            release_kinds=b['reserve_release_kinds']),
                gray=dict(completed=g['completed'], first_dead=g['first_dead'],
                          relinquishments=g['relinquishments'], routes=g['routes'],
                          streak_final=g['streak_final'], streak_writes=g['streak_writes'],
                          release_kinds=g['reserve_release_kinds']),
            )
    cost = transition_cost_table()
    dmg = damage_read_table()
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), transition=transition, damage=damage, corrupt=corrupt,
             STREAK_N=STREAK_N, cost_table=cost, damage_read_table=dmg,
             per_individual=per_ind, rows=rows),
        indent=2, default=str))
    print(json.dumps(dict(cost_table=cost, damage_read_table=dmg), indent=2, default=str))
    print(json.dumps(dict(per_individual=per_ind), indent=2, default=str))
    return rows, per_ind, cost, dmg


def main():
    if '--cost' in sys.argv:
        print(json.dumps(dict(cost=transition_cost_table()), indent=2))
        return
    if '--damage' in sys.argv:
        print(json.dumps(dict(damage_read_table=damage_read_table()), indent=2))
        return
    collect('ac99_d2_engineering_v1', [4436, 4437, 4438, 4439, 4412, 4413, 4414, 4415])


if __name__ == '__main__':
    main()
