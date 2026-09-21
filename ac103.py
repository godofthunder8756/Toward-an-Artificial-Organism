"""AC103: distinguish resource shortage from premature termination of repair.

Parent: AC102 (frozen). AC102 established the corruption-move interaction and rejected the
eight-write staging policy (budget REPAIR_BUDGET=8), but left the CAUSE of the failure open.
The staged budget still crossed the material threshold on the marginal seeds (material <= 72 at
the corruption tick, so any spend >= 8 drops material below 64 and fires obs bit 1), and staging
introduced a SECOND failure on the high-material seeds: the program's own majority repair
(action 2) cements the 4/7 corruption flip and removes the reconstruction's trigger (obs bit 2's
minority count drops to zero once the flip is cemented), so the staged reconstruction stalls
(fw stays nonzero) and the organism dies.

AC103 asks WHICH of two distinct causes is at work, holding prices and W requirements UNCHANGED:

  1. CURRENT vs PERSISTENT repair triggering. Persistent: the reconstruction remains engaged
     until an internally determined completion condition holds (the DECODED program matches the
     description-derived target), rather than only while the obs2/description-minority trigger
     is live. The completion condition is DERIVED from the organism's own state (program bank +
     description) -- no added host-side pending state, no corruption flag, no observer's
     pristine template. This is the strongest possible internalization: persistence is a pure
     function of the maintained state, so there is no latch whose damage/repair could shift the
     pre-challenge economy.
  2. IMMEDIATE vs STAGED reconstruction (per-tick write budget, exactly AC102's regen_budget).

Also measured: whether ordinary majority repair REVERSES reconstruction progress -- action 2
cements the corruption (writes correct replicas toward a wrong majority) and suppresses the
trigger. Quantified per tick as `action2_writes` / `action2_cementing`.

Decisive sequence: (1) determine whether staging can complete reliably when its trigger cannot
disappear prematurely (persistent_staged vs current_staged); (2) test whether a state-dependent
spending policy (defer the reconstruction while material <= the obs-bit-1 threshold) can preserve
adaptation resources (persistent_defer).

The runner is a faithful copy of ac102._run_core for the `both` condition (corrupt=True + the
two-move SCHEDULE), parametrized by (trigger, regen_budget). `current` reproduces AC102 `both`
byte-for-byte; `current_staged` reproduces AC102 `staged` byte-for-byte. The persistent arms
differ ONLY by the trigger condition (`reg_trigger OR program_incomplete`), which is inert
whenever the program already matches the description-derived target -- so the persistent
immediate arm is byte-identical to `current` wherever the immediate reconstruction outruns
cementing, and diverges only where the trigger would otherwise disappear mid-reconstruction.

Discipline: engineering first (seeds 0-7), then hashed protocol, then disjoint final seeds.
A negative result is a finding, not a failure.
"""
from pathlib import Path
import hashlib
import inspect
import json
import sys
import numpy as np
import ac102
import ac101
import ac100
import ac99_d2
import ac99
import ac96
import ac95
import ac12
import ac4
import ac71
import ac9
import ac5_program as prog
from ac1 import decode

TICKS = ac95.TICKS
CORRUPT_TICK = ac95.CORRUPT_TICK
CORRUPT_BITS = ac95.CORRUPT_BITS
MOVE_TICK = ac95.MOVE_TICK
DEV = ac71.DEV
STREAK_N = ac12.STREAK_N

SCHEDULE = ac100.SCHEDULE
mapping_at = ac100.mapping_at
move_ticks = ac100.move_ticks

# the frozen maintain references (from ac102, so the current arms are byte-identical).
maintain = ac102.maintain                # ac99.maintain (= ac95.maintain when reserve=False)
MAINTAIN_BUDGETED = ac102.MAINTAIN_BUDGETED   # ac95.maintain + per-tick regen budget

REPAIR_BUDGET = ac102.REPAIR_BUDGET       # 8

# the state-dependent spending policy's material threshold: while material <= DEFER_THRESHOLD
# (the obs-bit-1 boundary) the reconstruction defers (budget 0), so it does not compete with the
# material contact and the paid decision write during the scarcity window.
DEFER_THRESHOLD = 64

ARMS = ('current', 'current_staged', 'persistent', 'persistent_staged', 'persistent_defer')

SOURCES = ['ac103.py', 'ac102.py', 'ac101.py', 'ac100.py', 'ac99_d2.py', 'ac99.py', 'ac97.py',
           'ac96.py', 'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC103_PROTOCOL_v1.md']

UNSEEN = [5600, 5601, 5602, 5603, 5604, 5605, 5606, 5607]   # fresh, untouched, disclosed pre-freeze
FINAL_SEEDS = UNSEEN
ENGINEERING = list(range(8))


def program_incomplete(o, reg_offs):
    """Internally determined completion condition: does the DECODED program (majority read)
    differ from the description-derived target (excluding the decision-state offsets)? True =
    reconstruction not yet complete. Majority-level: sub-majority ambient damage does NOT count
    as incomplete (it does not change what the program reads), so the persistent trigger fires
    only on a corruption-scale majority flip, not on the ordinary ambient repair cycle. The
    target is rebuilt from the organism's own description -- no observer template, no corruption
    flag."""
    target = ac95.build_program(ac95.read_slot(o, ac95.read_pointer(o)))
    if target is None:
        return True
    exclude = set(reg_offs)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    return any(int(decoded[i]) != int(target[i])
               for i in range(prog.PROGRAM_BITS) if i not in exclude)


# ---------------- the persistent maintain (asserted source surgery) ----------------
def _build_persistent_maintain():
    ns = dict(vars(ac95))
    # budgeted reg_from_active (the ONLY change vs ac95: a per-tick budget, via _cap(b, budget)).
    reg_src = inspect.getsource(ac95.reg_from_active)
    assert reg_src.count("def reg_from_active(o, e, reg_offs):") == 1, "reg_from_active signature"
    reg_src = reg_src.replace(
        "def reg_from_active(o, e, reg_offs):",
        "def reg_from_active(o, e, reg_offs, budget=None):")
    assert reg_src.count("    n = min(_cap(b), len(sites))") == 1, "reg_from_active write line"
    reg_src = reg_src.replace(
        "    n = min(_cap(b), len(sites))",
        "    n = min(_cap(b, budget), len(sites))")
    exec(compile(reg_src, 'ac103_reg_from_active', 'exec'), ns)
    ns['program_incomplete'] = program_incomplete
    ns['DEFER_THRESHOLD'] = DEFER_THRESHOLD
    # the maintain surgery: replace the regen trigger with the persistent trigger
    maint_src = inspect.getsource(ac95.maintain)
    regen_anchor = "    if cfg['regen'] and reg_trigger:\n        reg_from_active(o, e, reg_offs)"
    assert maint_src.count(regen_anchor) == 1, "maintain regen anchor"
    regen_new = (
        "    if cfg['regen']:\n"
        "        fire = reg_trigger or (cfg.get('persistent', False) and program_incomplete(o, reg_offs))\n"
        "        if fire:\n"
        "            budget = cfg.get('regen_budget')\n"
        "            if budget == 'defer':\n"
        "                budget = 0 if (now >= CORRUPT_TICK and o.body.material <= DEFER_THRESHOLD) else None\n"
        "            reg_from_active(o, e, reg_offs, budget)")
    maint_src = maint_src.replace(regen_anchor, regen_new)
    exec(compile(maint_src, 'ac103_maintain_persistent', 'exec'), ns)
    return ns['maintain']


MAINTAIN_PERSISTENT = _build_persistent_maintain()


# ---------------- cementing measurement (wrapped react) ----------------
def make_react_counted(react_fn, acquired, counters):
    """Wrap the shimmed react so action 2 (bank-0 majority restore) records how many replica
    writes move toward a WRONG majority (`cementing`): a write to a program bit whose current
    majority differs from the acquired correct value. Read-only: does not alter the trajectory."""
    def counted(b, action, arm, e):
        if action == 2:
            majority = (b.traces[0].sum(axis=-1) > 3).astype(np.uint8)
            sites = np.argwhere(b.traces[0] != majority[:, None])
            a = ac4.available(b)
            cap = int(a[0:4].sum()) * 8
            n = min(cap, 32, len(sites), b.energy, b.material)
            cement = 0
            for i, r in sites[:n]:
                if int(i) < prog.PROGRAM_BITS and int(majority[i]) != int(acquired[i]):
                    cement += 1
            counters['action2_writes'] += n
            counters['action2_cementing'] += cement
        return react_fn(b, action, arm, e)
    return counted


# ---------------- arm config ----------------
def _arm_config(arm):
    """(corrupt, schedule, regen_budget, persistent) per arm."""
    return {
        'current':           (True, SCHEDULE, None,          False),
        'current_staged':    (True, SCHEDULE, REPAIR_BUDGET, False),
        'persistent':        (True, SCHEDULE, None,          True),
        'persistent_staged': (True, SCHEDULE, REPAIR_BUDGET, True),
        'persistent_defer':  (True, SCHEDULE, 'defer',       True),
    }[arm]


def _maintain_fn(regen_budget, persistent):
    if persistent:
        return MAINTAIN_PERSISTENT
    return maintain if regen_budget is None else MAINTAIN_BUDGETED


# ---------------- the run (faithful to ac102._run_core, parametrized) ----------------
def _run_core(seed, history, corrupt, schedule, regen_budget, persistent, maintain_fn,
              record_trace=False, swap_at=None):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    Alloc = ac99_d2.GrayAllocEraseReserve
    streak_read = ac99_d2.gray_streak_read
    alloc = Alloc('allocate', seed, history, reserve=False)
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
    cfg = dict(ac95.ARM_PARTS['gated'])
    cfg['reserve'] = False
    cfg['regen_budget'] = regen_budget
    cfg['persistent'] = persistent
    succ = ac95.Succession('real', encoded)
    step = ac95.build(cfg['ac_arm'], alloc, succ, build_offs, cfg)
    step.__globals__['maintain'] = maintain_fn
    # cementing counter (read-only wrap of the shimmed react)
    cement = {'action2_writes': 0, 'action2_cementing': 0}
    step.__globals__['ac4'].react = make_react_counted(
        step.__globals__['ac4'].react, acquired, cement)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    for k in ('reg_writes', 'succ_writes', 'ctrl_writes', 'timer_increments', 'timer_resets',
              'split_events', 'streak_writes', 'reserve_writes', 'reserve_m',
              'reserve_released_m'):
        total[k] = 0
    mts = move_ticks(schedule)
    births_by_window = {i: {'W_birth': 0, 'C_birth': 0, 'B_birth': 0}
                        for i in range(len(mts) + 1)}
    first_dead = None
    description_correct_at_death = None
    fw_at_corrupt = None
    recovery_tick = None
    drop_ticks = []
    restore_ticks = []
    trace = [] if record_trace else None
    budget_trace = []
    was_bound = {0: False, 1: False}
    seen_bound = {0: False, 1: False}
    reacquire_ticks = {0: [], 1: []}
    swap_applied = False
    first_W_empty = None
    first_C_empty = None
    mat_at_corrupt = None
    mat_min_post_corrupt = 10**9
    cement_last = (0, 0)
    for t in range(TICKS):
        alloc.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = Alloc('allocate', seed, history, reserve=False)
            alloc.streak_offs = streak_offs
            alloc.offs = offs
            alloc.shadow = o.body.traces[0].copy()
            alloc.now = t
            step.__globals__['succ'] = succ
            step.__globals__['alloc'] = alloc
            step.__globals__['allowance'] = alloc.allowance
            swap_applied = True
        core = (rng.random((126, 7)) < 1e-4).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
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
        if t == CORRUPT_TICK:
            mat_at_corrupt = o.body.material
            if corrupt:
                for bit in range(CORRUPT_BITS):
                    w = 1 - int(acquired[bit])
                    o.body.traces[0, bit, 0:4] = w
                    o.body.traces[0, bit, 4:7] = int(acquired[bit])
                fw_at_corrupt = int(((o.body.traces[0, :CORRUPT_BITS].sum(axis=-1) > 3).astype(np.uint8)
                                     != acquired[:CORRUPT_BITS]).sum())
        step.__globals__['now'] = t
        prev_drops = len(alloc.log['dropped'])
        prev_restores = len(alloc.log.get('restored', []))
        e = step(o, core, noise, directions, coin,
                 tuple(mapping_at(base_map, t, schedule)), [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        win = sum(1 for mt in mts if t >= mt)
        for k in births_by_window[win]:
            births_by_window[win][k] += e.get(k, 0)
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
        if ac102.TRACE_LO <= t < ac102.TRACE_HI:
            fw = int(((o.body.traces[0, :CORRUPT_BITS].sum(axis=-1) > 3).astype(np.uint8)
                      != acquired[:CORRUPT_BITS]).sum())
            a2w = cement['action2_writes'] - cement_last[0]
            a2c = cement['action2_cementing'] - cement_last[1]
            cement_last = (cement['action2_writes'], cement['action2_cementing'])
            budget_trace.append(dict(t=t, mat_after=o.body.material,
                                     reg_writes=e.get('reg_writes', 0),
                                     streak_writes=e.get('streak_writes', 0),
                                     action2_writes=a2w, action2_cementing=a2c,
                                     obs=int(ac9.observe(o)), fw=fw))
        if recovery_tick is None and corrupt and t >= CORRUPT_TICK:
            fw_now = int(((o.body.traces[0, :CORRUPT_BITS].sum(axis=-1) > 3).astype(np.uint8)
                          != acquired[:CORRUPT_BITS]).sum())
            if fw_now == 0:
                recovery_tick = t
        W = int((o.body.life[:4] > 0).sum())
        C = int((o.body.life[16:20] > 0).sum())
        if first_W_empty is None and W == 0:
            first_W_empty = t
        if first_C_empty is None and C == 0:
            first_C_empty = t
        if t >= CORRUPT_TICK:
            mat_min_post_corrupt = min(mat_min_post_corrupt, o.body.material)
        if first_dead is None and o.body.dead:
            first_dead = t
            description_correct_at_death = int(
                (ac95.read_slot(o, ac95.read_pointer(o)) == encoded).sum())
    win_edges = mts + [TICKS]
    relinq_by_move = []
    reacq_by_move = []
    for i, mt in enumerate(mts):
        lo, hi = mt, win_edges[i + 1]
        relinq_by_move.append(sum(1 for (dt, _p, _r) in drop_ticks if lo <= dt < hi))
        reacq_by_move.append(sum(1 for dt in reacquire_ticks[1] if lo <= dt < hi))
    inv = ac4.inventory(o.body)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    desc_bits = ac95.read_slot(o, ac95.read_pointer(o))
    desc_priority = ac95.decode_perm(desc_bits[ac95.PERM_OFFSET:ac95.PERM_OFFSET + ac95.PERM_BITS])
    active_end, phase_end, _ = ac95.ctrl_fields(o)
    return dict(seed=seed, history=history, corrupt=corrupt,
                n_moves=len(mts), regen_budget=regen_budget, schedule=[list(s) for s in schedule],
                persistent=persistent,
                ticks=TICKS, completed=total['active'] == TICKS, first_dead=first_dead,
                fw_at_corrupt=fw_at_corrupt, recovery_tick=recovery_tick,
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != acquired[:CORRUPT_BITS]).sum()),
                program_correct=int((decoded == acquired).sum()),
                description_correct=int((desc_bits == encoded).sum()),
                description_correct_at_death=description_correct_at_death,
                description_valid=int(sorted(desc_priority) == list(range(4))),
                description_same=int(desc_priority == tuple(priority)),
                successions=len([s for s in succ.log if s.get('done')]),
                ctrl_idle_end=int(active_end == 0 and phase_end == ac95.PHASE_IDLE),
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                drop_ticks=drop_ticks,
                restore_ticks=restore_ticks,
                streak_final={0: streak_read(o, 0, streak_offs),
                              1: streak_read(o, 1, streak_offs)},
                streak_events=getattr(alloc, 'streak_events', []),
                reacquire_ticks=reacquire_ticks,
                relinquishments_by_move=relinq_by_move,
                reacquisitions_by_move=reacq_by_move,
                births_by_window={str(k): v for k, v in births_by_window.items()},
                swap_applied=swap_applied,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                W_births=int(total['W_birth']), C_births=int(total['C_birth']),
                B_births=int(total['B_birth']),
                first_W_empty=first_W_empty, first_C_empty=first_C_empty,
                mat_at_corrupt=mat_at_corrupt, mat_min_post_corrupt=mat_min_post_corrupt,
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                streak_writes=int(total['streak_writes']),
                action2_writes=cement['action2_writes'],
                action2_cementing=cement['action2_cementing'],
                budget_trace=budget_trace,
                state_hash=o.digest()), o, trace


def run(seed, history, arm='current'):
    corrupt, schedule, budget, persistent = _arm_config(arm)
    fn = _maintain_fn(budget, persistent)
    row, o, _ = _run_core(seed, history, corrupt, schedule, budget, persistent, fn,
                          record_trace=False)
    row['arm'] = arm
    return row


# ---------------- observer-discard (per-tick, on `current`, carried from AC102) ----------------
def _mid_streak_tick(row, key=1, before_value=2, since=MOVE_TICK):
    for (t, k, before, after, dropped) in row['streak_events']:
        if k == key and before == before_value and not dropped and t >= since:
            return t
    return None


def observer_discard_equivalence(seed, history, arm='current'):
    """Per-tick observer-discard: replace the succession observer AND the alloc at a mid-streak
    tick; the trajectory must be byte-identical at every tick (the decision state is recovered
    from maintained state alone). Carried from AC102's G6; the persistent arms add no host-side
    state (the trigger is derived from the maintained program + description)."""
    corrupt, schedule, budget, persistent = _arm_config(arm)
    fn = _maintain_fn(budget, persistent)
    base, base_o, base_trace = _run_core(seed, history, corrupt, schedule, budget, persistent, fn,
                                         record_trace=True)
    swap_tick = _mid_streak_tick(base, key=1, before_value=2)
    if swap_tick is None:
        return dict(seed=seed, history=history, arm=arm, status='no_mid_streak',
                    streak_events=base['streak_events'])
    swapped, swapped_o, swapped_trace = _run_core(seed, history, corrupt, schedule, budget,
                                                  persistent, fn, record_trace=True,
                                                  swap_at=swap_tick)
    n_equal = 0
    first_div = None
    for (t1, d1), (t2, d2) in zip(base_trace, swapped_trace):
        assert t1 == t2, f'tick grid mismatch {t1} vs {t2}'
        if d1 == d2:
            n_equal += 1
        elif first_div is None:
            first_div = t1
    per_tick_identical = (first_div is None and len(base_trace) == len(swapped_trace)
                          and n_equal == len(base_trace))
    return dict(seed=seed, history=history, arm=arm, swap_tick=swap_tick,
                streak_at_swap=2, host_dict_cleared=True,
                swap_applied=swapped['swap_applied'],
                per_tick_identical=per_tick_identical,
                n_equal=n_equal, n_ticks=len(base_trace), first_div=first_div,
                terminal_identical=base['state_hash'] == swapped['state_hash'],
                base_hash=base['state_hash'], swapped_hash=swapped['state_hash'])


# ---------------- arm identity (the single-change equivalence checks) ----------------
def arm_identity(seed, history):
    """Byte-identity licenses:
      - `current` == AC102 `both`; `current_staged` == AC102 `staged` (the frozen references).
      - `persistent` (immediate) == `current` (immediate): persistent triggering is INERT on the
        immediate schedule (the immediate reconstruction outruns the cementing, so the persistent
        trigger never fires where the current trigger would not).
    """
    return {
        'current_is_ac102_both': run(seed, history, 'current')['state_hash'] ==
                                  ac102.run(seed, history, 'both')['state_hash'],
        'current_staged_is_ac102_staged': run(seed, history, 'current_staged')['state_hash'] ==
                                           ac102.run(seed, history, 'staged')['state_hash'],
        'persistent_is_current': run(seed, history, 'persistent')['state_hash'] ==
                                 run(seed, history, 'current')['state_hash'],
    }


# ---------------- gates (recomputed from rows, no simulation) ----------------
def gates_ac103(rows, seeds, obs_current):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history']), {})[r['arm']] = r
    n_ind = len(seeds) * 2
    cur_st = [r for r in rows if r['arm'] == 'current_staged']
    per_st = [r for r in rows if r['arm'] == 'persistent_staged']
    per_defer = [r for r in rows if r['arm'] == 'persistent_defer']

    g1 = None  # set by the collector (needs live rerun vs ac102)

    # G2 -- persistent staging completes reconstruction reliably (premature termination is a
    # RECOVERY failure, closed by persistence): every final individual's `persistent_staged`
    # recovers (fw -> 0). Non-vacuous: at least one final individual's `current_staged` does NOT
    # recover (the cementing stall is present and was closed).
    g2 = (len(per_st) == n_ind
          and all(r['flipped_still_wrong'] == 0 for r in per_st)
          and any(r['flipped_still_wrong'] > 0 for r in cur_st))

    # G3 -- the state-dependent defer preserves adaptation resources (resource shortage is a
    # SURVIVAL failure, closed by the defer): every final individual's `persistent_defer`
    # recovers (fw -> 0) AND survives (`completed`).
    g3 = (len(per_defer) == n_ind
          and all(r['flipped_still_wrong'] == 0 and r['completed'] for r in per_defer))

    # G4 -- the two failure modes are distinct: every final individual where `persistent_staged`
    # dies with fw == 0 (recovery complete, survival failed) is survived by `persistent_defer`.
    # Non-vacuous: at least one such individual (persistence closes recovery but not survival).
    residual = [r for r in per_st if not r['completed'] and r['flipped_still_wrong'] == 0]
    g4 = (len(per_st) == n_ind
          and len(residual) > 0
          and all(by[(r['seed'], r['history'])]['persistent_defer']['completed']
                  and by[(r['seed'], r['history'])]['persistent_defer']['flipped_still_wrong'] == 0
                  for r in residual))

    # G5 -- state sufficiency: per-tick observer-discard byte-identical on `current` (carried
    # from AC102). The persistent arms add no host-side state, so this is unchanged.
    g5 = (obs_current is not None and len(obs_current) == n_ind
          and all(d.get('status') != 'no_mid_streak' and d.get('swap_applied')
                  and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
                  for d in obs_current.values()))

    return {
        'G1_arm_identity': g1,
        'G2_persistent_staging_completes_reconstruction': g2,
        'G3_state_dependent_defer_preserves_adaptation_resources': g3,
        'G4_two_failure_modes_are_distinct': g4,
        'G5_state_sufficiency_observer_discard': g5,
        'G6_completeness_determinism': None,
    }


def preflight(protocol='AC103_PROTOCOL_v1.md'):
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


# ---------------- collectors ----------------
def collect_engineering(root, seeds):
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for arm in ARMS:
                    r = run(seed, history, arm)
                    rows.append(r)
                    f.write(json.dumps(r) + '\n')
                    f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['history'], r['completed'], r['first_dead'],
                 r['fw_at_corrupt'], r['recovery_tick'], r['flipped_still_wrong'],
                 r['action2_writes'], r['action2_cementing'],
                 r['mat_at_corrupt'], r['streak_final'])
                for r in rows[-len(ARMS) * 2:]]), default=str), flush=True)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), arms=list(ARMS), REPAIR_BUDGET=REPAIR_BUDGET, rows=rows),
        indent=2, default=str))
    print(json.dumps(dict(rows=len(rows), dir=root), indent=2, default=str))
    return rows


def collect_finals(root, seeds, do_preflight=True):
    if do_preflight:
        preflight()
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for arm in ARMS:
                    r = run(seed, history, arm)
                    rows.append(r)
                    f.write(json.dumps(r) + '\n')
                    f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['history'], r['completed'], r['first_dead'],
                 r['fw_at_corrupt'], r['recovery_tick'], r['flipped_still_wrong'],
                 r['action2_writes'], r['action2_cementing'],
                 r['mat_at_corrupt'], r['streak_final'])
                for r in rows[-len(ARMS) * 2:]]), default=str), flush=True)
    obs_current = {}
    for seed in seeds:
        for history in (0, 1):
            obs_current[f'{seed}/{history}'] = observer_discard_equivalence(seed, history, 'current')
    ident = {}
    for seed in seeds:
        for history in (0, 1):
            ident[f'{seed}/{history}'] = arm_identity(seed, history)
    g = gates_ac103(rows, seeds, obs_current)
    first = rows[0]
    rerun = run(first['seed'], first['history'], first['arm'])
    g['G1_arm_identity'] = all(
        v.get('current_is_ac102_both') and v.get('current_staged_is_ac102_staged')
        for v in ident.values())
    g['G6_completeness_determinism'] = (
        len(rows) == len(seeds) * len(ARMS) * 2
        and rerun['state_hash'] == first['state_hash'])
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), arms=list(ARMS), REPAIR_BUDGET=REPAIR_BUDGET,
             DEFER_THRESHOLD=DEFER_THRESHOLD,
             hashes=hashes, gates=g, rows=rows,
             observer_discard_current=obs_current, arm_identity=ident),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac103_engineering_v1', ENGINEERING)
        return
    collect_finals('ac103_results_v1', FINAL_SEEDS)


if __name__ == '__main__':
    main()
