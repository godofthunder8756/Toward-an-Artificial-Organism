"""AC96-D2: the relinquishment failure-streak moved from a host dict into maintained state.

This is the implementation of AC96-D1 (see AC96_DESIGN_v1.md). It closes the second
class-C host-side operational-memory leak that the AC95-D1 audit found: `alloc.streak`,
the per-key (2 keys x 3 bits) count of consecutive unproductive contacts that drives the
AC75 erase-on-relinquishment write. Today it is a host dict (`ac12.Alloc.__init__` /
`ac95.AllocErase.outcome`); here it lives in the frozen program's permanently-dead rule's
six zero-valued bits, damaged by the ambient program stream and repaired by the paid
bank-0 majority-restore, and read/written by `outcome`/`_drop` by majority with an atomic,
W-gated paid increment/reset. The host dict is vestigial and never read on the maintained
arm.

Storage (AC96-D1 section 2): the dead rule (mask 32, action 5) contributes six zero-valued
word bits beyond the AC12 register (mask bits 0-3): mask bits 4/6/7/8 (word bits 5/7/8/9)
and action bits 1/3 (word bits 11/13). `base = 14 * ac12.dead_rule_index(o)`; the six
offsets are `[base+5, base+7, base+8, base+9, base+11, base+13]`, resolved once at
acquisition. Key k's 3-bit counter is offsets `[3k:3k+3]`, LSB first. The offsets are
excluded from `reg_from_active` alongside the register (decision state is not program
content), otherwise reconstruction would clobber the counter.

The comparator (AC96-D1 section 5) is host-streak control vs maintained arm:
`streak_maintained=False` runs the frozen ac95 gated behaviour byte-for-byte (the host
dict; reconstruction excludes only the register). `streak_maintained=True` is the
maintained arm. The two arms are byte-identical (state_hash) on the shared trajectory up
to the first streak write (the first development-time unproductive contact), and diverge
only in the streak bits' values and the paid streak-write economy.

No protocol, no freeze. Engineering only, seeds 0-7, in the relinquishment world
(`transition='perm'`).
"""
from pathlib import Path
from types import SimpleNamespace
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

TICKS = ac95.TICKS                  # 16384
CORRUPT_TICK = ac95.CORRUPT_TICK    # 8192
CORRUPT_BITS = ac95.CORRUPT_BITS    # 8
MOVE_TICK = ac95.MOVE_TICK          # 8192

STREAK_N = ac12.STREAK_N            # 6
STREAK_THRESHOLD = 4                # replicas that must be set for a streak bit to read 1
                                    # (the majority convention; 7 replicas/bit)

SOURCES = ['ac96.py', 'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py',
           'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py',
           'ac4.py', 'ac4_transport.py', 'ac1.py', 'AC96_PROTOCOL_v1.md']


# ---------------- the streak in maintained state ----------------
def streak_offsets(o):
    """The six zero-valued free bits of the permanently-dead rule, resolved once at
    acquisition (the AC12 rule: resolve register offsets from the pristine program, before
    any damage or write changes the mask you would match on)."""
    base = 14 * ac12.dead_rule_index(o)
    return [base + 5, base + 7, base + 8, base + 9, base + 11, base + 13]


def streak_read(o, key, streak_offs):
    """Majority read (>= STREAK_THRESHOLD) of the 3-bit counter for `key`. LSB first."""
    offs = streak_offs[3 * key: 3 * key + 3]
    return sum(int(o.body.traces[0, off].sum() >= STREAK_THRESHOLD) << k
               for k, off in enumerate(offs))


def streak_write(o, e, key, new, streak_offs):
    """Atomic, W-gated paid write of the maintained streak for `key` to `new` (0..7).

    Writes only the replicas whose value differs from the target; refuses the whole
    transition if that count exceeds the produced machinery's paid capacity
    `min(32, 8*available_W, energy, material)`. A refused transition writes nothing (a
    partial binary-counter transition would corrupt the value). Returns the number of
    replicas written (0 => refused)."""
    offs = np.array(streak_offs[3 * key: 3 * key + 3])
    if streak_read(o, key, streak_offs) == new:
        return 0
    targets = np.array([(new >> k) & 1 for k in range(3)], dtype=np.uint8)
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


def streak_minority(o, streak_offs):
    """Sub-majority damage on the six streak bits: sum over offsets of min(ones, 7-ones).
    0 = clean (the frozen all-zero acquisition value); grows as the sticky program stream
    sets replicas and the paid repair is unavailable. Distinct from streak_advance (a paid
    `streak_write`), which changes the MAJORITY value, not the minority replicas."""
    ones = o.body.traces[0, streak_offs].sum(axis=-1)
    return int(np.minimum(ones, 7 - ones).sum())


def streak_bits_at(o, streak_offs):
    """The six streak bits' majority values (0/1) -- the counter's 'true' read state at this
    moment. All six are 0 in the frozen program; a 1 means either an outcome write (paid advance)
    or a damage-induced majority flip (degradation), which `streak_degraded_bits_end` separates by
    comparing against the value at cut."""
    return [int(o.body.traces[0, off].sum() >= STREAK_THRESHOLD) for off in streak_offs]


class AllocEraseMaintained(ac95.AllocErase):
    """AllocErase with the relinquishment streak read/written in maintained state.

    `self.streak` (the host dict inherited from `ac12.Alloc`) is vestigial and never read.
    The maintained counter lives in the dead rule's six free bits; `self.streak_offs` is
    resolved once at acquisition and passed to every read/write.
    """

    def __init__(self, arm, seed, history):
        super().__init__(arm, seed, history)
        self.streak_offs = None
        self.streak_events = []   # D3: (tick, key, streak_before, streak_after, dropped) for
                                  # unproductive contacts only (productive resets are silent)

    def outcome(self, o, key, e):
        if self.arm != 'allocate':
            return
        key = int(key)
        if e['productive'] > 0:
            self._restore(o, e, key)
            streak_write(o, e, key, 0, self.streak_offs)
            return
        cur = streak_read(o, key, self.streak_offs)
        dropped = 0
        if cur + 1 >= STREAK_N:
            n_before = len(self.log['dropped'])
            self._drop(o, e, key)
            dropped = 1 if len(self.log['dropped']) > n_before else 0
        else:
            streak_write(o, e, key, cur + 1, self.streak_offs)
        self.streak_events.append((self.now, key, cur,
                                   streak_read(o, key, self.streak_offs), dropped))

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
        o.body.energy -= n
        o.body.material -= n
        e['spent_e'] += n
        e['spent_m'] += n
        e['writes'] += n
        sites[:] = 1
        streak_write(o, e, key, 0, self.streak_offs)
        self.log['dropped'].append(list(place))
        r, s = place
        live = int((o.memory.life[r, s] > 0).sum())
        if live:
            o.memory.life[r, s] = 0
            o.memory.bits[r, s] = 0
            e['memory_expiry'] += live


# ---------------- the run (faithful to ac95.run, streak-maintained toggle) ----------------
def _run_internal(seed, history, arm, streak_maintained, damage, corrupt, transition,
                  ticks, move_tick, record_trace=False,
                  swap_at=None, cut_tick=None, rescue_tick=None, damage_rate=1e-4):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    if streak_maintained:
        assert arm == 'gated', 'the maintained arm is the fixed architecture only'
        alloc = AllocEraseMaintained('allocate', seed, history)
    else:
        alloc = ac95.AllocErase('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    streak_offs = streak_offsets(o)          # resolved once, at acquisition
    if streak_maintained:
        alloc.streak_offs = streak_offs
    reg_offs = ac95.resolve_offsets(o)       # register offsets (decision state, scoring)
    build_offs = reg_offs + streak_offs if streak_maintained else reg_offs
    encoded = ac95.description_bits(priority)
    o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
    acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    cfg = dict(ac95.ARM_PARTS[arm])
    if cfg.get('block_W'):
        raise NotImplementedError('AC96-D2 supports the gated arm only (no W-block arms)')
    succ = ac95.Succession('real' if cfg['succession'] else 'none', encoded)
    step = ac95.build(cfg['ac_arm'], alloc, succ, build_offs, cfg)
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
    first_dead = None
    first_streak_write_tick = None
    drop_ticks = []
    restore_ticks = []
    trace = [] if record_trace else None
    # ---- D3 instrumentation (all observational; none steer a write) ----
    was_bound = {0: False, 1: False}
    seen_bound = {0: False, 1: False}
    reacquire_ticks = {0: [], 1: []}
    first_W_empty = None
    streak_writes_before_cut = None
    streak_writes_after_cut = 0
    streak_at_cut = None
    streak_at_rescue = None
    streak_minority_at_cut = None
    streak_bits_at_cut = None
    swap_applied = False
    for t in range(ticks):
        alloc.now = t
        # ---- D3: observer-discard + host-streak-state clear (fresh succ AND fresh alloc) ----
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real' if cfg['succession'] else 'none', encoded)
            if streak_maintained:
                alloc = AllocEraseMaintained('allocate', seed, history)
                alloc.streak_offs = streak_offs
            else:
                alloc = ac95.AllocErase('allocate', seed, history)
            alloc.offs = offs
            alloc.shadow = o.body.traces[0].copy()
            alloc.now = t
            step.__globals__['succ'] = succ
            step.__globals__['alloc'] = alloc
            step.__globals__['allowance'] = alloc.allowance
            swap_applied = True
        # ---- D3: machinery-only W cut / rescue (ac95's EXTERNAL primitives), BEFORE the step ----
        if cut_tick is not None and t == cut_tick:
            ac95.cut_W(o)
            streak_at_cut = {k: streak_read(o, k, streak_offs) for k in (0, 1)}
            streak_minority_at_cut = streak_minority(o, streak_offs)
            streak_bits_at_cut = streak_bits_at(o, streak_offs)
            streak_writes_before_cut = int(total['streak_writes'])
        if rescue_tick is not None and t == rescue_tick:
            ac95.restore_W(o)
            streak_at_rescue = {k: streak_read(o, k, streak_offs) for k in (0, 1)}
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
        # ---- D3: re-acquisition (entry re-bound this tick, i.e. a None->bound transition after
        # a prior bound->None), and W-empty / streak-degradation tracking ----
        for k in (0, 1):
            now_bound = o.memory.read(k) is not None
            if was_bound[k] is False and now_bound and seen_bound[k]:
                reacquire_ticks[k].append(t)
            if now_bound:
                seen_bound[k] = True
            was_bound[k] = now_bound
        if cut_tick is not None and t >= cut_tick:
            streak_writes_after_cut += e.get('streak_writes', 0)
        if first_W_empty is None and int((o.body.life[:4] > 0).sum()) == 0:
            first_W_empty = t
        if len(alloc.log['dropped']) > prev_drops:
            place = alloc.log['dropped'][-1]
            drop_ticks.append((t, list(place),
                               ac12.bit_value(o, offs[2 * place[0] + place[1]])))
        if len(alloc.log.get('restored', [])) > prev_restores:
            restore_ticks.append((t, list(alloc.log.get('restored', [])[-1])))
        if first_streak_write_tick is None and e.get('streak_writes', 0) > 0:
            first_streak_write_tick = t
        if record_trace:
            trace.append((t, o.digest()))
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, damage=damage, corrupt=corrupt,
                transition=transition, ticks=ticks, move_tick=move_tick,
                streak_maintained=streak_maintained,
                completed=total['active'] == ticks, first_dead=first_dead,
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                drop_ticks=drop_ticks,
                restore_ticks=restore_ticks,
                streak_writes=int(total['streak_writes']),
                streak_final={0: streak_read(o, 0, streak_offs),
                              1: streak_read(o, 1, streak_offs)},
                first_streak_write_tick=first_streak_write_tick,
                streak_events=getattr(alloc, 'streak_events', []),
                reacquire_ticks=reacquire_ticks,
                first_W_empty=first_W_empty,
                streak_writes_before_cut=streak_writes_before_cut,
                streak_writes_after_cut=streak_writes_after_cut,
                streak_at_cut=streak_at_cut,
                streak_at_rescue=streak_at_rescue,
                streak_minority_at_cut=streak_minority_at_cut,
                streak_minority_end=streak_minority(o, streak_offs),
                streak_bits_at_cut=streak_bits_at_cut,
                streak_degraded_bits_end=(0 if streak_bits_at_cut is None else
                    sum(1 for i in range(6)
                        if streak_bits_at_cut[i] == 0
                        and o.body.traces[0, streak_offs[i]].sum() >= STREAK_THRESHOLD)),
                swap_applied=swap_applied,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                state_hash=o.digest()), o, trace


def run(seed, history, arm='gated', damage=True, corrupt=True, transition='none',
        ticks=TICKS, move_tick=MOVE_TICK, streak_maintained=False):
    """Run one individual. `streak_maintained=False` is the host-streak control (the frozen
    ac95 gated behaviour); True is the maintained-streak arm."""
    row, o, _ = _run_internal(seed, history, arm, streak_maintained, damage, corrupt,
                              transition, ticks, move_tick, record_trace=False)
    return row


# ---------------- the comparator (host-streak control vs maintained arm) ----------------
def host_control_equivalence(seeds, transition='none', damage=True, corrupt=True):
    """L1: the host-streak control (`streak_maintained=False`) reproduces the frozen ac95
    gated arm byte-for-byte (state_hash). Returns the number of matched rows."""
    n = 0
    for seed in seeds:
        for history in (0, 1):
            got = run(seed, history, 'gated', damage, corrupt, transition,
                      streak_maintained=False)
            want = ac95.run(seed, history, 'gated', damage, corrupt, transition)
            assert got['state_hash'] == want['state_hash'], \
                f"host control mismatch {seed}/{history}/{damage}/{corrupt}/{transition}"
            n += 1
    return n


def frozen_reproduction(seeds=(4408, 4409, 4410, 4411)):
    """The host-streak control reproduces the frozen ac95_results_v1 gated rows (state_hash).
    This is re-verifying the frozen runner's determinism against its own recorded freeze."""
    frozen = [json.loads(l) for l in Path('ac95_results_v1/rows.jsonl').read_text().splitlines()]
    n = 0
    for seed in seeds:
        for history in (0, 1):
            for damage in (True, False):
                for corrupt in (True, False):
                    want = [r for r in frozen
                            if r['seed'] == seed and r['history'] == history
                            and r['arm'] == 'gated' and r['damage'] == damage
                            and r['corrupt'] == corrupt and r['transition'] == 'none']
                    if not want:
                        continue
                    got = run(seed, history, 'gated', damage, corrupt, 'none',
                              streak_maintained=False)
                    assert got['state_hash'] == want[0]['state_hash'], \
                        f"frozen mismatch {seed}/{history}/{damage}/{corrupt}"
                    n += 1
    return n


def prefix_equivalence(seed, history, transition='perm', damage=True, corrupt=False):
    """Byte-identity on the shared trajectory up to the first divergence tick.

    The maintained and host arms are identical (state_hash at every tick) through the tick
    before the first divergence, and the first divergence is the earlier of (a) the first paid
    streak write (an unproductive contact -- the host dict is free, the maintained write is paid),
    or (b) the first reconstruction (reg_from_active) that touches a damaged streak bit -- the
    host control's exclusion covers only the register, so it resets the damaged bit to 0; the
    maintained arm excludes the streak bits, so it skips them and leaves the damage. Both are the
    streak-storage change. Returns (first_streak_write_tick, first_divergence_tick, n_prefix_equal)."""
    host_row, host_o, host_trace = _run_internal(seed, history, 'gated', False, damage,
                                                 corrupt, transition, TICKS, MOVE_TICK,
                                                 record_trace=True)
    maint_row, maint_o, maint_trace = _run_internal(seed, history, 'gated', True, damage,
                                                    corrupt, transition, TICKS, MOVE_TICK,
                                                    record_trace=True)
    fsw = maint_row['first_streak_write_tick']
    assert fsw is not None, f'seed {seed}/{history}: no streak write ever fired in {transition}'
    # host trace is recorded at the same tick grid; find the first divergence
    first_div = None
    n_eq = 0
    for (t1, d1), (t2, d2) in zip(host_trace, maint_trace):
        assert t1 == t2
        if d1 == d2:
            n_eq += 1
        elif first_div is None:
            first_div = t1
    return fsw, first_div, n_eq


def decision_identity(seed, history, transition='perm', damage=False, corrupt=False):
    """Compare the two arms' decision signature: drop/restore ticks, routes, register, survival.
    Returns (same, host_row, maint_row). In the perm world this is False on every individual --
    the paid streak write is starved by the move's material collapse (damage-independent), so the
    maintained arm's relinquishment stalls. Not a gate; a recorded measurement."""
    host = run(seed, history, 'gated', damage, corrupt, transition, streak_maintained=False)
    maint = run(seed, history, 'gated', damage, corrupt, transition, streak_maintained=True)
    same = (host['drop_ticks'] == maint['drop_ticks']
            and host['restore_ticks'] == maint['restore_ticks']
            and host['routes'] == maint['routes']
            and host['register'] == maint['register']
            and host['completed'] == maint['completed']
            and host['first_dead'] == maint['first_dead'])
    return same, host, maint


# ---------------- engineering collector ----------------
def collect_engineering(root, seeds, transition='perm', damage=True, corrupt=False):
    """Engineering run (no protocol, no freeze): both arms in the relinquishment world.
    Records the per-individual relinquishment count and the comparator equivalence."""
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for sm in (False, True):
                    r = run(seed, history, 'gated', damage, corrupt, transition,
                            streak_maintained=sm)
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['history'], r['streak_maintained'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['restorations'], r['routes'], r['streak_writes'],
                 r['streak_final'], r['first_streak_write_tick'])
                for r in rows[-4:]]), default=str), flush=True)
    # comparator equivalence: byte-identity up to the first streak write, per individual
    prefix = {}
    for seed in seeds:
        for history in (0, 1):
            fsw, first_div, n_eq = prefix_equivalence(seed, history, transition, damage, corrupt)
            prefix[f'{seed}/{history}'] = dict(first_streak_write=fsw,
                                               first_divergence=first_div, prefix_equal=n_eq)
    # decision identity (damage-free), per individual
    decisions = {}
    for seed in seeds:
        for history in (0, 1):
            same, host, maint = decision_identity(seed, history, transition, False, corrupt)
            decisions[f'{seed}/{history}'] = same
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), transition=transition, damage=damage, corrupt=corrupt,
             rows=rows, prefix_equivalence=prefix, decision_identity=decisions),
        indent=2, default=str))
    print(json.dumps(dict(prefix_equivalence=prefix, decision_identity=decisions),
                     indent=2, default=str))
    return rows, prefix, decisions


# ---------------- D3: relinquishment fires / observer-discard / interruption ----------------
def _mid_streak_tick(row, key=1, before_value=2):
    """The tick of the first post-move unproductive contact on `key` whose streak reads
    `before_value` before the contact -- a mid-streak tick (streak non-zero but below STREAK_N)
    where the bound entry is going stale. Returns None if no such tick exists."""
    for (t, k, before, after, dropped) in row['streak_events']:
        if k == key and before == before_value and not dropped and t >= MOVE_TICK:
            return t
    return None


def d3_relinquishment(seeds, histories=(0, 1), transition='perm', damage=True, corrupt=False):
    """Item 1: relinquishment fires. Per individual: first unproductive contact (post-move),
    streak progression, drop tick (with the register bit read at the drop), re-acquisition tick."""
    rows = {}
    for seed in seeds:
        for history in histories:
            r = run(seed, history, 'gated', damage, corrupt, transition, streak_maintained=True)
            key = 1
            events = [e for e in r['streak_events'] if e[1] == key and e[0] >= MOVE_TICK]
            progression = [(e[0], e[2], e[3]) for e in events]          # (tick, before, after)
            drop_events = [e for e in events if e[4] == 1]
            drop_tick = drop_events[0][0] if drop_events else None
            register_at_drop = next((rb for (t, _p, rb) in r['drop_ticks']
                                     if t == drop_tick), None) if drop_tick is not None else None
            reacquire = r['reacquire_ticks'].get(key, [])
            reacquire_tick = reacquire[0] if reacquire else None
            rows[f'{seed}/{history}'] = dict(
                completed=r['completed'], first_dead=r['first_dead'],
                first_unproductive_contact=events[0][0] if events else None,
                streak_progression=progression,
                drop_tick=drop_tick, register_at_drop=register_at_drop,
                reacquire_tick=reacquire_tick,
                routes=r['routes'], streak_writes=r['streak_writes'])
    return rows


def observer_discard_equivalence(seed, history, transition='perm', damage=True, corrupt=False):
    """Item 2: observer-discard on the streak. At a mid-streak tick, replace the succession
    observer AND the alloc (clearing the vestigial host streak dict) with fresh objects; resume;
    require byte-identical trajectory (state_hash). The streak must be recovered from maintained
    state alone. Returns the per-individual record."""
    base = run(seed, history, 'gated', damage, corrupt, transition, streak_maintained=True)
    swap_tick = _mid_streak_tick(base, key=1, before_value=2)
    if swap_tick is None:
        return dict(seed=seed, history=history, status='no_mid_streak',
                    streak_events=base['streak_events'])
    streak_at_swap = 2   # the `before` value the anchor tick was selected on
    swapped = _run_internal(seed, history, 'gated', True, damage, corrupt, transition,
                            TICKS, MOVE_TICK, swap_at=swap_tick)[0]
    return dict(seed=seed, history=history, swap_tick=swap_tick,
                streak_at_swap=streak_at_swap,
                host_dict_cleared=True,          # the fresh alloc's `streak` is {0:0, 1:0}
                swap_applied=swapped['swap_applied'],
                identical=base['state_hash'] == swapped['state_hash'],
                base_hash=base['state_hash'], swapped_hash=swapped['state_hash'])


def interruption_equivalence(seed, history, transition='perm', damage=True, corrupt=False,
                             rescue_offset=30, damage_rate=1e-4):
    """Item 3: interruption during a streak. Cut W (machinery-only) at a mid-streak tick while a
    bound entry is going stale; verify the streak degrades under the damage stream when W=0 (no
    paid repair) and that a machinery-only rescue restores the correct count from maintained
    state. The no-rescue and rescue arms share the cut tick; the streak writes after the cut are
    counted separately so streak-degradation (damage, unpaid) is never confounded with
    streak-advance (outcome, a paid `streak_write`). `damage_rate` is the program-stream rate
    (frozen 1e-4; stated together with the majority read threshold STREAK_THRESHOLD=4)."""
    base = run(seed, history, 'gated', damage, corrupt, transition, streak_maintained=True)
    cut_tick = _mid_streak_tick(base, key=1, before_value=2)
    if cut_tick is None:
        return dict(seed=seed, history=history, status='no_mid_streak',
                    streak_events=base['streak_events'])
    cut = _run_internal(seed, history, 'gated', True, damage, corrupt, transition,
                        TICKS, MOVE_TICK, cut_tick=cut_tick, damage_rate=damage_rate)[0]
    rescue = _run_internal(seed, history, 'gated', True, damage, corrupt, transition,
                           TICKS, MOVE_TICK, cut_tick=cut_tick,
                           rescue_tick=cut_tick + rescue_offset, damage_rate=damage_rate)[0]
    return dict(seed=seed, history=history, cut_tick=cut_tick,
                rescue_tick=cut_tick + rescue_offset,
                damage_rate=damage_rate,
                streak_at_cut=cut['streak_at_cut'],
                streak_bits_at_cut=cut['streak_bits_at_cut'],
                cut=dict(completed=cut['completed'], first_dead=cut['first_dead'],
                         first_W_empty=cut['first_W_empty'],
                         streak_writes_after_cut=cut['streak_writes_after_cut'],
                         streak_minority_at_cut=cut['streak_minority_at_cut'],
                         streak_minority_end=cut['streak_minority_end'],
                         streak_degraded_bits_end=cut['streak_degraded_bits_end'],
                         streak_final=cut['streak_final'],
                         relinquishments=cut['relinquishments'],
                         W=cut['W'], C=cut['C'], material=cut['material']),
                rescue=dict(completed=rescue['completed'], first_dead=rescue['first_dead'],
                            streak_at_rescue=rescue['streak_at_rescue'],
                            streak_writes_after_cut=rescue['streak_writes_after_cut'],
                            streak_minority_at_cut=rescue['streak_minority_at_cut'],
                            streak_minority_end=rescue['streak_minority_end'],
                            streak_degraded_bits_end=rescue['streak_degraded_bits_end'],
                            streak_final=rescue['streak_final'],
                            relinquishments=rescue['relinquishments'],
                            W=rescue['W'], C=rescue['C'], material=rescue['material']))

def d3_degradation_sweep(seed, history=0, transition='perm', damage=True, corrupt=False,
                         rates=(1e-4, 1e-3, 5e-3)):
    """Item 3 companion: the degradation-vs-rate sweep. Runs the no-rescue cut arm at the frozen
    rate and higher program-stream rates (stated with the majority read threshold
    STREAK_THRESHOLD=4) to show that, with W=0 so no paid repair fires, the streak's should-be-0
    bits accumulate sticky-SET damage and majority-flip as the rate rises -- i.e. the streak
    degrades when un-repaired, and the read value drifts up (damage), which is NOT the same as the
    paid advance (streak_write, which is refused whole at W=0)."""
    base = run(seed, history, 'gated', damage, corrupt, transition, streak_maintained=True)
    cut_tick = _mid_streak_tick(base, key=1, before_value=2)
    if cut_tick is None:
        return dict(seed=seed, status='no_mid_streak', streak_events=base['streak_events'])
    out = {}
    for rate in rates:
        r = _run_internal(seed, history, 'gated', True, damage, corrupt, transition,
                          TICKS, MOVE_TICK, cut_tick=cut_tick, damage_rate=rate)[0]
        out[str(rate)] = dict(cut_tick=cut_tick, first_dead=r['first_dead'],
                              streak_at_cut=r['streak_at_cut'],
                              streak_bits_at_cut=r['streak_bits_at_cut'],
                              streak_final=r['streak_final'],
                              streak_minority_end=r['streak_minority_end'],
                              streak_degraded_bits_end=r['streak_degraded_bits_end'],
                              streak_writes_after_cut=r['streak_writes_after_cut'],
                              relinquishments=r['relinquishments'])
    return dict(seed=seed, history=history, cut_tick=cut_tick, rates=out)


def collect_d3(root, seeds, histories=(0, 1), transition='perm', damage=True, corrupt=False,
               rescue_offset=30):
    """D3 engineering collector (no protocol, no freeze). Runs the three items and records the
    per-individual results. `rows.jsonl` holds the undisturbed maintained-arm rows (item 1's
    source); `results.json` holds all three items' derived records."""
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in histories:
                r = run(seed, history, 'gated', damage, corrupt, transition,
                        streak_maintained=True)
                rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
    relinq = d3_relinquishment(seeds, histories, transition, damage, corrupt)
    discard = {f'{s}/{h}': observer_discard_equivalence(s, h, transition, damage, corrupt)
               for s in seeds for h in histories}
    interruption = {f'{s}/{h}': interruption_equivalence(s, h, transition, damage, corrupt,
                                                         rescue_offset)
                    for s in seeds for h in histories}
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), histories=list(histories), transition=transition,
             damage=damage, corrupt=corrupt, rescue_offset=rescue_offset,
             relinquishment=relinq, observer_discard=discard, interruption=interruption),
        indent=2, default=str))
    print(json.dumps(dict(relinquishment=relinq), indent=2, default=str))
    print(json.dumps(dict(observer_discard=discard), indent=2, default=str))
    print(json.dumps(dict(interruption=interruption), indent=2, default=str))
    return relinq, discard, interruption


# ---------------- D4: preflight + finals collector + gates ----------------


def preflight(protocol='AC96_PROTOCOL_v1.md'):
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


def gates_ac96(rows, observer_discard=None, interruption=None, host_equiv=None):
    """Recompute the AC96-D4 gates from the saved rows (no simulation).

    G1 state sufficiency (observer-discard) is a two-run comparison and is re-read from the
       recorded `observer_discard` dict (re-derived by the collector; the replay tool re-runs a
       sample). G3 (streak maintained) is a single-step pin held by test_ac96.py (not derivable
       from rows). G4 (interruption) is a two-run comparison re-read from `interruption`. G5 is set
       by the collector (row count + sampled rerun + host-equivalence).
    """
    def pick(sm, dmg):
        return [r for r in rows
                if r['streak_maintained'] is sm and r['damage'] is dmg
                and r['transition'] == 'perm']

    maintained = pick(True, True)
    host = pick(False, True)
    nodmg = pick(True, False)

    # G1: observer-discard byte-identity at a mid-streak tick (streak==2, non-vacuous)
    g1 = observer_discard is not None and bool(observer_discard) and all(
        d.get('status') != 'no_mid_streak' and d.get('swap_applied')
        and d.get('streak_at_swap') == 2 and d.get('identical')
        for d in observer_discard.values())

    # G2: test-world (>=1 relinquishment) + well-formed drop on the relinquishing individuals
    g2_testworld = sum(r['relinquishments'] for r in maintained) >= 1
    g2_drops = all(
        bool(r['drop_ticks'])
        and all(reg for (_t, _p, reg) in r['drop_ticks'])
        and bool(r['reacquire_ticks'].get(1))
        and r['reacquire_ticks'][1][0] > r['drop_ticks'][0][0]
        for r in maintained if r['relinquishments'] >= 1)
    g2 = g2_testworld and g2_drops

    # G4: W cut stops paid streak writes (no host-assisted drop), sub-threshold degradation only,
    # machinery-only rescue resumes the correct count
    g4 = interruption is not None and bool(interruption) and all(
        d.get('status') != 'no_mid_streak'
        and d['cut']['streak_writes_after_cut'] == 0
        and d['cut']['relinquishments'] == 0
        and d['cut']['streak_degraded_bits_end'] == 0
        and not d['cut']['completed']
        and d['rescue']['completed']
        and d['rescue']['streak_at_rescue'] == d['streak_at_cut']
        and d['rescue']['streak_writes_after_cut'] > 0
        for d in interruption.values())

    return {
        'G1_state_sufficiency_observer_discard': g1,
        'G2_relinquishment_mechanism': g2,
        'G3_streak_maintained_singlestep': None,   # pinned by test_ac96.py
        'G4_interruption_rescue': g4,
        'G5_completeness_determinism_host_equivalence': None,
    }


def collect_finals(root, seeds, do_preflight=True):
    """AC96-D4 finals: three conditions per individual (maintained / host / maintained_nodmg) in the
    relinquishment world (`transition='perm'`, damage stream on, corrupt off). G1 (observer-discard)
    and G4 (interruption) are two-run comparisons computed here and recorded; G5's host-equivalence
    compares the host-streak control byte-for-byte to ac95.run('gated'). do_preflight=False is for
    the engineering run (the protocol is frozen only before the finals)."""
    if do_preflight:
        preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    conds = [('maintained', True, True), ('host', False, True), ('maintained_nodmg', True, False)]
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for (label, sm, dmg) in conds:
                    r = run(seed, history, 'gated', dmg, False, 'perm', streak_maintained=sm)
                    r['condition'] = label
                    rows.append(r); f.write(json.dumps(r) + chr(10)); f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['streak_final'])
                for r in rows[-len(conds) * 2:]]), default=str), flush=True)
    # ---- G1 observer-discard (two-run comparison, per individual) ----
    obs = {}
    for seed in seeds:
        for history in (0, 1):
            obs[f'{seed}/{history}'] = observer_discard_equivalence(seed, history)
    # ---- G4 interruption (two-run comparison, per individual) ----
    interruption = {}
    for seed in seeds:
        for history in (0, 1):
            interruption[f'{seed}/{history}'] = interruption_equivalence(seed, history)
    # ---- G5 host-equivalence (host control == ac95 gated, byte-for-byte) ----
    host_equiv = {}
    for seed in seeds:
        for history in (0, 1):
            a = run(seed, history, 'gated', True, False, 'perm', streak_maintained=False)
            b = ac95.run(seed, history, 'gated', True, False, 'perm')
            host_equiv[f'{seed}/{history}'] = a['state_hash'] == b['state_hash']
    g = gates_ac96(rows, obs, interruption, host_equiv)
    first = rows[0]
    rerun = run(first['seed'], first['history'], 'gated', first['damage'], False, 'perm',
                streak_maintained=first['streak_maintained'])
    g['G5_completeness_determinism_host_equivalence'] = (
        len(rows) == len(seeds) * 2 * len(conds)
        and rerun['state_hash'] == first['state_hash']
        and bool(host_equiv) and all(host_equiv.values()))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows, transition='perm',
             conds=conds, observer_discard=obs, interruption=interruption,
             host_equivalence=host_equiv),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac96_engineering_v1', list(range(8)), transition='perm',
                            damage=True, corrupt=False)
        return
    if '--d3' in sys.argv:
        collect_d3('ac96_d3_engineering_v1', [0, 3], transition='perm',
                   damage=True, corrupt=False)
        return
    if '--equivalence' in sys.argv:
        n = host_control_equivalence(list(range(8)), 'perm', True, False)
        print(f'host control byte-identical to ac95 gated in perm world: {n} rows')
        return
    if '--frozen' in sys.argv:
        n = frozen_reproduction()
        print(f'host control reproduces frozen ac95_results_v1 gated: {n} rows')
        return
    if '--finals' in sys.argv:
        collect_finals('ac96_results_v1', [4412, 4413, 4414, 4415])
        return
    collect_finals('ac96_results_v1', [4412, 4413, 4414, 4415])


if __name__ == '__main__':
    main()
