"""AC98-D2: a revised reserve whose withholding cannot starve the decision it funds.

Parent design: AC98_DESIGN_v1.md. This is the AC97 reserve with the release gate
broadened from drop-only to three release-on-maintained-state triggers, so the
one-time 21-unit withholding can never become a permanent loss and can never tip
the organism into the W/C death cascade:

  - `drop`  (original, unchanged): inside `_drop`, when material < RESERVE_LEVEL,
    before the cap check -- funds the drop register write (7) + streak reset (14).
  - `stall` (the revision): a streak increment is refused (`ac96.streak_write`
    returns 0 for a cur -> cur+1 transition, reached only when cur+1 < STREAK_N).
    This is the direct fix for AC97 seed 4434 (the 4->5 increment starved by 1
    material unit): the release returns 21, the increment and the drop are funded.
  - `wlow`  (survival): on a key-1 contact when available_W < 3 and material <= 64.
    Releasing the 21 units lifts material above 64, clearing observation bit 1, so
    the frozen priority order runs the W-birth rule (action 6) instead of the stale
    material contact (action 1) and W recovers before the death cascade. This stops
    seed 4435 from dying; it does not (cannot) make 4435's 3->4 increment succeed,
    because that increment is W-bound (recorded as an honest residual).

Arming, level (21), storage (traces[1, 540]) and repair (paid majority-restore on
minority >= RESERVE_TRIGGER) are unchanged from AC97. The no-reserve control
(`reserve=False`) is byte-identical to the AC97 no-reserve arm (state_hash), because
the stall/wlow paths are gated on `self.reserve` and never disturb the rng stream or
the frozen write order when the reserve is disabled.

No protocol, no freeze. Engineering only, on the AC97 finals 4432-4435 and the
D1/D2 seeds 4412-4415, in the relinquishment world (`transition='perm'`).
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog
import ac95
import ac96
import ac97

TICKS = ac95.TICKS
CORRUPT_TICK = ac95.CORRUPT_TICK
CORRUPT_BITS = ac95.CORRUPT_BITS
MOVE_TICK = ac95.MOVE_TICK
DEV = ac71.DEV
STREAK_N = ac12.STREAK_N

SOURCES = ['ac98.py', 'ac97.py', 'ac96.py', 'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py',
           'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py',
           'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py', 'AC98_PROTOCOL_v1.md']

# ---- the reserve ----
# The reserve is a single maintained-state bit in a free bank-1 region (bank 1 is
# traces[1, :1024]; slots 0-519, pointer 520-521, CTRL 522-539 are used, so bit 540
# is free and is untouched by the frozen damage/repair). 1 = armed (RESERVE_LEVEL
# material is withheld), 0 = disarmed. Read by majority (>= 4 of 7), written with an
# atomic W-gated paid write, damaged by the bank-1 sticky stream, repaired by a paid
# majority-restore (reg_reserve) on minority >= RESERVE_TRIGGER.
RESERVE_OFFS = 540
RESERVE_LEVEL = 21          # exactly the drop (7) + reset (14) material cost
RESERVE_THRESHOLD = 4       # majority read convention (7 replicas / bit)
RESERVE_TRIGGER = 2         # minority count that triggers reg_reserve (as DESC_TRIGGER)


def reserve_read(o):
    """Majority read of the reserve bit. 1 = armed, 0 = disarmed."""
    return int(o.body.traces[1, RESERVE_OFFS].sum() >= RESERVE_THRESHOLD)


def reserve_minority(o):
    """Sub-majority damage on the reserve bit: min(ones, 7-ones). 0 = clean."""
    ones = int(o.body.traces[1, RESERVE_OFFS].sum())
    return min(ones, 7 - ones)


def write_reserve(o, e, val):
    """Atomic, W-gated paid write of the reserve bit to `val` (<= 7 replicas).

    Refused whole if the transition exceeds the produced machinery's per-action
    capacity `ac95._cap`. Returns the number of replicas written (0 => refused).
    """
    b = o.body
    sites = np.argwhere(b.traces[1, RESERVE_OFFS] != val)
    n = len(sites)
    if n and n <= ac95._cap(b):
        b.traces[1, RESERVE_OFFS, sites[:, 0]] = val
        b.energy -= n
        b.material -= n
        e['spent_e'] += n
        e['spent_m'] += n
        e['writes'] += n
        e['reserve_writes'] = e.get('reserve_writes', 0) + n
        return n
    return 0


def arm_reserve(o, e):
    """Withhold RESERVE_LEVEL material from a productive material contact's intake.

    Called on a productive material contact when the reserve is disarmed. Reduces
    `b.material` and `e['in_m']` by RESERVE_LEVEL (the withheld material is not in the
    spendable pool, so no lower-priority write can reach it), and sets the reserve bit
    (paid, W-gated). The `ac4.balance` identity `b.material == M + in_m - overflow_m
    - spent_m` holds by construction because `in_m` is a variable (AC15's primitive).
    Returns RESERVE_LEVEL on success, 0 if the reserve was already armed or the arm
    write was refused.
    """
    if reserve_read(o):
        return 0
    b = o.body
    if b.material < RESERVE_LEVEL or e.get('in_m', 0) < RESERVE_LEVEL:
        return 0
    b.material -= RESERVE_LEVEL
    e['in_m'] -= RESERVE_LEVEL
    e['reserve_m'] = e.get('reserve_m', 0) + RESERVE_LEVEL
    if not write_reserve(o, e, 1):
        # arm write refused: roll the withholding back (never a half-armed reserve)
        b.material += RESERVE_LEVEL
        e['in_m'] += RESERVE_LEVEL
        e['reserve_m'] = e.get('reserve_m', 0) - RESERVE_LEVEL
        return 0
    return RESERVE_LEVEL


def release_reserve(o, e):
    """Release the reserve into the spendable pool so the drop + reset can be paid.

    Adds RESERVE_LEVEL material back to `b.material` (accounted as `in_m`, the reverse
    of arming) and disarms the reserve bit (paid, W-gated). The released material is
    the organism's own previously-withheld income, not an injected resource. Returns
    RESERVE_LEVEL on success, 0 if the reserve was already disarmed.
    """
    if not reserve_read(o):
        return 0
    b = o.body
    room = 256 - b.material
    rel = min(RESERVE_LEVEL, room)
    if rel <= 0:
        return 0
    b.material += rel
    e['in_m'] += rel
    e['reserve_released_m'] = e.get('reserve_released_m', 0) + rel
    write_reserve(o, e, 0)
    return rel


def reg_reserve(o, e):
    """Paid majority-restore of the reserve bit (in-place, like reg_ctrl)."""
    b = o.body
    bit = int(b.traces[1, RESERVE_OFFS].sum() > 3)
    sites = np.argwhere(b.traces[1, RESERVE_OFFS] != bit)
    n = min(ac95._cap(b), len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, RESERVE_OFFS, idx[:, 0]] = bit
        b.energy -= n
        b.material -= n
        e['spent_e'] += n
        e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n


# ---------------- the allocator (ac96 maintained + reserve arm/release) ----------------
class AllocEraseReserve(ac96.AllocEraseMaintained):
    """AllocEraseMaintained with the reserve armed on productive material contacts and
    released at the drop. The reserve state lives in `traces[1, RESERVE_OFFS]`; this
    object holds no reserve state (observer-discard safe)."""

    def __init__(self, arm, seed, history, reserve=False):
        super().__init__(arm, seed, history)
        self.reserve = reserve
        self.reserve_events = []   # (tick, kind, amount) for arm/release, observational

    def outcome(self, o, key, e):
        if self.arm != 'allocate':
            return
        key = int(key)
        if e['productive'] > 0:
            self._restore(o, e, key)
            ac96.streak_write(o, e, key, 0, self.streak_offs)
            if self.reserve and key == 1 and self.now >= DEV:
                r = arm_reserve(o, e)
                if r:
                    self.reserve_events.append((self.now, 'arm', r))
            return
        cur = ac96.streak_read(o, key, self.streak_offs)
        dropped = 0
        if cur + 1 >= STREAK_N:
            n_before = len(self.log['dropped'])
            self._drop(o, e, key)            # `drop` release lives inside _drop (unchanged)
            dropped = 1 if len(self.log['dropped']) > n_before else 0
        else:
            r = ac96.streak_write(o, e, key, cur + 1, self.streak_offs)
            if r == 0 and self.reserve and reserve_read(o):
                # `stall`: the increment was refused (n > cap; the only way streak_write
                # returns 0 in this branch, since new = cur+1 != cur). Return the withheld
                # material the moment continuing to withhold would starve the buildup.
                rel = release_reserve(o, e)
                if rel:
                    self.reserve_events.append((self.now, 'stall', rel))
        # `wlow` (survival): on a key-1 contact where the repair catalyst is failing and
        # material is at/below the obs-bit-1 threshold, return the withheld material so obs
        # bit 1 clears and the frozen priority order runs W-birth (action 6) instead of the
        # stale material contact (action 1).
        if self.reserve and key == 1 and reserve_read(o):
            W = int(ac4.available(o.body)[:4].sum())
            if W < 3 and o.body.material <= 64:
                rel = release_reserve(o, e)
                if rel:
                    self.reserve_events.append((self.now, 'wlow', rel))
        self.streak_events.append((self.now, key, cur,
                                   ac96.streak_read(o, key, self.streak_offs), dropped))

    def _drop(self, o, e, key):
        place = ac12.m12.slot_of_key(o.memory, key)
        if place is None:
            return
        off = self.offs[2 * place[0] + place[1]]
        sites = o.body.traces[0, off]
        n = int((sites != 1).sum())
        if n == 0:
            return
        # the drop (7) + reset (14) need <= RESERVE_LEVEL material in total; release the
        # reserve if the spendable pool cannot cover both.
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
        ac96.streak_write(o, e, key, 0, self.streak_offs)
        self.log['dropped'].append(list(place))
        r, s = place
        live = int((o.memory.life[r, s] > 0).sum())
        if live:
            o.memory.life[r, s] = 0
            o.memory.bits[r, s] = 0
            e['memory_expiry'] += live


# ---------------- maintenance: ac95's + the reserve repair ----------------
def maintain(o, e, succ, reg_offs, cfg, now):
    ac95.maintain(o, e, succ, reg_offs, cfg, now)
    if cfg.get('reserve') and reserve_minority(o) >= RESERVE_TRIGGER:
        reg_reserve(o, e)


# ---------------- the run ----------------
def _run_internal(seed, history, arm, reserve, damage, corrupt, transition,
                  ticks, move_tick, record_trace=False, swap_at=None,
                  damage_rate=1e-4):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    assert arm == 'gated', 'the maintained/reserve arms are the fixed architecture only'
    alloc = AllocEraseReserve('allocate', seed, history, reserve=reserve)
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
        raise NotImplementedError('AC97-D2 supports the gated arm only')
    succ = ac95.Succession('real', encoded)
    step = ac95.build(cfg['ac_arm'], alloc, succ, build_offs, cfg)
    step.__globals__['maintain'] = maintain   # add the reserve repair to maintenance
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
    first_arm_tick = None
    first_release_tick = None
    swap_applied = False
    for t in range(ticks):
        alloc.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = AllocEraseReserve('allocate', seed, history, reserve=reserve)
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
                # the reserve bit is damaged by the same bank-1 sticky stream (last draw,
                # so the reserve=False run is byte-identical to ac96).
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
        if first_arm_tick is None and e.get('reserve_writes', 0) > 0:
            # first reserve write is the arm (or a repair); the arm event is recorded
            # in alloc.reserve_events with kind='arm'
            pass
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
                streak_final={0: ac96.streak_read(o, 0, streak_offs),
                              1: ac96.streak_read(o, 1, streak_offs)},
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
    """Run one individual. `reserve=False` is the no-reserve control (byte-identical to
    ac96's maintained arm); True is the reserve arm."""
    row, o, _ = _run_internal(seed, history, arm, reserve, damage, corrupt,
                              transition, ticks, move_tick, record_trace=False)
    return row


# ---------------- no-reserve control: byte-identical to the ac97 no-reserve arm ----------------
def no_reserve_reproduction(seeds, transition='perm', damage=True, corrupt=False):
    """The no-reserve control reproduces ac97's no-reserve arm byte-for-byte (state_hash).
    ac97's no-reserve is itself byte-identical to ac96's maintained arm, so this also pins
    the ac96 identity; the direct comparator named by the design is ac97."""
    n = 0
    for seed in seeds:
        for history in (0, 1):
            got = run(seed, history, 'gated', reserve=False, damage=damage,
                      corrupt=corrupt, transition=transition)
            want = ac97.run(seed, history, 'gated', reserve=False, damage=damage,
                            corrupt=corrupt, transition=transition)
            assert got['state_hash'] == want['state_hash'], \
                f"no-reserve mismatch {seed}/{history}"
            n += 1
    return n


# ---------------- observer-discard: per-tick trajectory comparison ----------------
def _mid_streak_tick(row, key=1, before_value=2):
    for (t, k, before, after, dropped) in row['streak_events']:
        if k == key and before == before_value and not dropped and t >= MOVE_TICK:
            return t
    return None


def observer_discard_equivalence(seed, history, transition='perm', damage=True,
                                 corrupt=False):
    """Observer-discard on the streak, compared PER-TICK.

    At a mid-streak tick, replace the succession observer AND the alloc (clearing the
    vestigial host streak dict) with fresh objects; resume; require the trajectory to be
    byte-identical at EVERY tick (per-tick digest equality), with the terminal state_hash
    comparison kept as a regression. The streak and the reserve must be recovered from
    maintained state alone.
    """
    base, base_o, base_trace = _run_internal(seed, history, 'gated', True, damage, corrupt,
                                             transition, TICKS, MOVE_TICK, record_trace=True)
    swap_tick = _mid_streak_tick(base, key=1, before_value=2)
    if swap_tick is None:
        return dict(seed=seed, history=history, status='no_mid_streak',
                    streak_events=base['streak_events'])
    swapped, swapped_o, swapped_trace = _run_internal(seed, history, 'gated', True, damage,
                                                      corrupt, transition, TICKS, MOVE_TICK,
                                                      record_trace=True, swap_at=swap_tick)
    n_equal = 0
    first_div = None
    for (t1, d1), (t2, d2) in zip(base_trace, swapped_trace):
        assert t1 == t2, f"tick grid mismatch {t1} vs {t2}"
        if d1 == d2:
            n_equal += 1
        elif first_div is None:
            first_div = t1
    per_tick_identical = (first_div is None
                          and len(base_trace) == len(swapped_trace)
                          and n_equal == len(base_trace))
    return dict(seed=seed, history=history, swap_tick=swap_tick,
                streak_at_swap=2, host_dict_cleared=True,
                swap_applied=swapped['swap_applied'],
                per_tick_identical=per_tick_identical,
                n_equal=n_equal, n_ticks=len(base_trace), first_div=first_div,
                terminal_identical=base['state_hash'] == swapped['state_hash'],
                base_hash=base['state_hash'], swapped_hash=swapped['state_hash'])


# ---------------- engineering collector ----------------


def per_individual_summary(rows):
    """Per-(seed, history) outcome table with the no-harm flag (AC97's gate-shape lesson:
    no individual where the no-reserve control survives and the reserve arm dies)."""
    by = {}
    for r in rows:
        by[(r['seed'], r['history'], r['reserve'])] = r
    seeds = sorted({r['seed'] for r in rows})
    hists = sorted({r['history'] for r in rows})
    out = {}
    for s in seeds:
        for h in hists:
            nr = by[(s, h, False)]
            rs = by[(s, h, True)]
            out[f'{s}/{h}'] = dict(
                seed=s, history=h,
                no_reserve=dict(completed=nr['completed'], first_dead=nr['first_dead'],
                                relinquishments=nr['relinquishments']),
                reserve=dict(completed=rs['completed'], first_dead=rs['first_dead'],
                             relinquishments=rs['relinquishments'],
                             release_kinds=rs['reserve_release_kinds'],
                             reserve_m=rs['reserve_m'],
                             reserve_released_m=rs['reserve_released_m'],
                             reserve_writes=rs['reserve_writes'],
                             streak_final=rs['streak_final'],
                             routes=rs['routes']),
                no_harm=not (nr['completed'] and not rs['completed']),
            )
    return out


def per_seed_table(summary):
    """Aggregate the per-individual summary to per distinct seed (2 histories each)."""
    seeds = sorted({int(k.split('/')[0]) for k in summary})
    out = {}
    for s in seeds:
        inds = [summary[f'{s}/{h}'] for h in (0, 1)]
        nr_survives = any(i['no_reserve']['completed'] for i in inds)
        nr_dies = any(not i['no_reserve']['completed'] for i in inds)
        rs_survives = any(i['reserve']['completed'] for i in inds)
        rs_dies = any(not i['reserve']['completed'] for i in inds)
        rs_relinq = any(i['reserve']['relinquishments'] >= 1 for i in inds)
        out[s] = dict(
            no_reserve=('survives' if nr_survives and not nr_dies
                        else 'dies' if not nr_survives
                        else 'mixed'),
            reserve=('survives' if rs_survives and not rs_dies
                     else 'dies' if not rs_survives
                     else 'mixed'),
            reserve_relinquishes=rs_relinq,
            no_harm=all(i['no_harm'] for i in inds),
        )
    return out


def collect_engineering(root, seeds, transition='perm', damage=True, corrupt=False):
    """AC98-D2 engineering (no protocol, no freeze): the no-reserve control and the revised
    reserve arm, per individual, in the relinquishment world. Reports, per seed, the flip
    (4434/4435 death -> survive), the no-regression on 4432/4433/4412-4415, the no-harm
    check, the per-tick observer-discard, and the maintenance trade-off numbers."""
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for rv in (False, True):
                    r = run(seed, history, 'gated', reserve=rv, damage=damage,
                            corrupt=corrupt, transition=transition)
                    rows.append(r)
                    f.write(json.dumps(r) + '\n')
                    f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['history'], r['reserve'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['streak_final'],
                 r['reserve_release_kinds'], r['reserve_m'], r['reserve_released_m'])
                for r in rows[-4:]]), default=str), flush=True)
    summary = per_individual_summary(rows)
    seed_table = per_seed_table(summary)
    # no-reserve control byte-identity to ac97's no-reserve arm (per individual)
    control_equiv = {}
    for seed in seeds:
        for history in (0, 1):
            a = run(seed, history, 'gated', reserve=False, damage=damage,
                    corrupt=corrupt, transition=transition)
            b = ac97.run(seed, history, 'gated', reserve=False, damage=damage,
                         corrupt=corrupt, transition=transition)
            control_equiv[f'{seed}/{history}'] = a['state_hash'] == b['state_hash']
    # per-tick observer-discard (state sufficiency, unchanged)
    obs = {f'{s}/{h}': observer_discard_equivalence(s, h, transition, damage, corrupt)
           for s in seeds for h in (0, 1)}
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), transition=transition, damage=damage, corrupt=corrupt,
             RESERVE_OFFS=RESERVE_OFFS, RESERVE_LEVEL=RESERVE_LEVEL,
             summary=summary, per_seed=seed_table,
             control_equivalence=control_equiv, observer_discard=obs,
             rows=rows),
        indent=2, default=str))
    print(json.dumps(dict(per_seed=seed_table), indent=2, default=str))
    print(json.dumps(dict(control_equivalence=control_equiv), indent=2, default=str))
    print(json.dumps(dict(observer_discard={k: (v.get('per_tick_identical'),
                                                v.get('status')) for k, v in obs.items()}),
                     indent=2, default=str))
    return rows, summary, seed_table, obs


# ---------------- finals: protocol freeze + unconditional criterion + no-harm gate ----------------
def preflight(protocol='AC98_PROTOCOL_v1.md'):
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


def _reacq_ticks(r):
    rt = r.get('reacquire_ticks') or {}
    return {int(k): v for k, v in rt.items()}


def gates_ac98(rows, seeds, observer_discard=None, control_equiv=None):
    """Recompute the AC98-D3 gates from the saved rows (no simulation).

    G1 (unconditional adaptation), G2 (no-harm) and G4 (endogenous reserve) are derived from
    the rows. G3 (per-tick observer-discard) and G5's control equivalence are two-run comparisons
    re-read from their recorded dicts. G5's determinism (sampled rerun) is set by the collector.
    """
    reserve = [r for r in rows if r['reserve'] is True and r['transition'] == 'perm']
    no_reserve = [r for r in rows if r['reserve'] is False and r['transition'] == 'perm']
    n_ind = len(seeds) * 2

    def a1(r):   # relinquishment: the drop fired with the register bit set
        return r['relinquishments'] >= 1 and bool(r['drop_ticks']) and \
            all(reg for (_t, _p, reg) in r['drop_ticks'])

    def a2(r):   # reacquisition: key 1 re-bound after the drop
        reacq = _reacq_ticks(r).get(1) or []
        drop = r['drop_ticks'][0][0] if r['drop_ticks'] else None
        return bool(reacq) and (drop is None or reacq[0] > drop)

    def a3(r):   # continued machinery production post-move
        return r['W_births_post_move'] > 0 and r['C_births_post_move'] > 0 \
            and r['B_births_post_move'] > 0

    def a4(r):   # survival
        return bool(r['completed'])

    # G1: unconditional adaptation — every final individual satisfies all four measures
    g1 = len(reserve) == n_ind and all(a1(r) and a2(r) and a3(r) and a4(r) for r in reserve)

    # G2: no-harm — no distinct seed where the no-reserve control survives and the reserve dies
    by_seed = {}
    for r in rows:
        by_seed.setdefault(r['seed'], {}).setdefault(r['reserve'], []).append(r)
    g2 = True
    for s in seeds:
        nr = by_seed.get(s, {}).get(False, [])
        rs = by_seed.get(s, {}).get(True, [])
        if nr and rs and any(r['completed'] for r in nr) and any(not r['completed'] for r in rs):
            g2 = False

    # G3: state sufficiency — per-tick observer-discard, trajectory-level
    g3 = observer_discard is not None and len(observer_discard) == n_ind and all(
        d.get('status') != 'no_mid_streak' and d.get('swap_applied')
        and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
        for d in observer_discard.values())

    # G4: endogenous reserve — no external rescue (release never exceeds withhold)
    g4 = all(r['reserve_m'] > 0 and r['reserve_released_m'] <= r['reserve_m'] for r in reserve)

    return {
        'G1_unconditional_adaptation': g1,
        'G2_no_harm': g2,
        'G3_state_sufficiency_per_tick_discard': g3,
        'G4_endogenous_reserve_no_external_rescue': g4,
        'G5_completeness_determinism_control_equivalence': None,
    }


def collect_finals(root, seeds, do_preflight=True):
    """AC98-D3 finals: two arms per individual (reserve / no_reserve) in the relinquishment world
    (`transition='perm'`, damage on, corrupt off). G1/G2/G4 are derived from the rows; G3 (per-tick
    observer-discard) and G5's control equivalence (no-reserve == ac97 no-reserve) are computed here
    and recorded. do_preflight=False is for a smoke run (the protocol is frozen only before finals)."""
    if do_preflight:
        preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    arms = [('reserve', True), ('no_reserve', False)]
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for (label, rv) in arms:
                    r = run(seed, history, 'gated', reserve=rv, damage=True,
                            corrupt=False, transition='perm')
                    r['condition'] = label
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], _reacq_ticks(r).get(1),
                 r['W_births_post_move'], r['C_births_post_move'], r['B_births_post_move'],
                 r['reserve_m'], r['reserve_released_m'], r['reserve_release_kinds'])
                for r in rows[-len(arms) * 2:]]), default=str), flush=True)
    # ---- G3 per-tick observer-discard (two-run comparison, per individual) ----
    obs = {}
    for seed in seeds:
        for history in (0, 1):
            obs[f'{seed}/{history}'] = observer_discard_equivalence(seed, history)
    # ---- G5 control equivalence (no-reserve == ac97 no-reserve, byte-for-byte) ----
    control_equiv = {}
    for seed in seeds:
        for history in (0, 1):
            a = run(seed, history, 'gated', reserve=False, damage=True, corrupt=False, transition='perm')
            b = ac97.run(seed, history, 'gated', reserve=False, damage=True, corrupt=False, transition='perm')
            control_equiv[f'{seed}/{history}'] = a['state_hash'] == b['state_hash']
    g = gates_ac98(rows, seeds, obs, control_equiv)
    first = rows[0]
    rerun = run(first['seed'], first['history'], 'gated', reserve=first['reserve'],
                damage=first['damage'], corrupt=first['corrupt'], transition='perm')
    g['G5_completeness_determinism_control_equivalence'] = (
        len(rows) == len(seeds) * 2 * len(arms)
        and rerun['state_hash'] == first['state_hash']
        and bool(control_equiv) and all(control_equiv.values()))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows, transition='perm',
             arms=arms, observer_discard=obs, control_equivalence=control_equiv),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--reproduce' in sys.argv:
        n = no_reserve_reproduction([4432, 4433, 4434, 4435, 4412, 4413, 4414, 4415])
        print(f'no-reserve control byte-identical to ac97 no-reserve arm: {n} rows')
        return
    if '--discard' in sys.argv:
        for seed in (4432, 4433, 4434, 4435, 4412, 4413, 4414, 4415):
            for history in (0, 1):
                print(json.dumps(observer_discard_equivalence(seed, history), default=str))
        return
    if '--engineering' in sys.argv:
        collect_engineering('ac98_d2_engineering_v1',
                            [4432, 4433, 4434, 4435, 4412, 4413, 4414, 4415])
        return
    collect_finals('ac98_results_v1', [4436, 4437, 4438, 4439])


if __name__ == '__main__':
    main()
