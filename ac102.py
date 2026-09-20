"""AC102: does the TIMING of necessary maintenance cause the composition failure?

Parent: AC101 (frozen). AC101 froze the composition test (gray_ctl + corruption + two route
moves) and recorded a split: the internal-state composition (reconstruction, description,
recipe turnover) is UNCONDITIONAL (8/8), while the behavioural composition (adaptation +
production + survival) fails on the unseen seed 4450 (dies 8408) and the engineering seed 1
(dies 8408). AC101 left a HYPOTHESIS for that failure (not an established mechanism): the
reconstruction's material spend collides with the adaptation's decision budget — the ~32
material spent over t=8192-8193 drops material below 64, sets observation bit 1 (material <=
64), the program answers with a material contact on the now-stale route 1, the paid internalized
Gray streak stalls below its drop threshold, the stale entry is never erased, and the organism
dies of the W/C collapse.

AC102 tests that hypothesis DIRECTLY, before changing the resource model. The question: whether
the TIMING of necessary maintenance (rather than its existence or price) causes the composition
failure. Two experiments, all in the gray_ctl architecture with no reserve:

  1. THE INTERACTION (2x2 matched runs): {corrupt, no-corrupt} x {move, no-move}.
       `neither`      corrupt=False, no moves
       `move_only`    corrupt=False, two moves          (== AC100 gray_ctl)
       `corrupt_only` corrupt=True,  no moves
       `both`         corrupt=True,  two moves          (== AC101 gray_ctl)
     The death must require BOTH challenges: neither alone may kill.

  2. THE REPAIR SCHEDULE (one internally controlled schedule): bound the reconstruction's
     per-tick spending while preserving the same total prices (1 energy + 1 material per
     replica) and machinery requirements (the W-catalyzed `_cap` still applies). The ONLY
     change is a per-tick write budget on `reg_from_active` (the reconstruction that
     re-instantiates the 126-bit program from the maintained 130-bit description), mirroring
     the succession's existing SUCC_BUDGET. Three arms on the `both` condition:
       `both`    (== immediate)  regen_budget = None  (writes up to `_cap`, ~24/tick at W=3)
       `staged`  regen_budget = REPAIR_BUDGET (=8)    (the test)
       `never`   regen_budget = 0                     (the schedule that delays repair
                                                       indefinitely — must FAIL: no recovery)
     A schedule that delays repair indefinitely must FAIL (the fix must not be "never repair");
     a successful timing fix would be a budget that still recovers the controller AND adapts.

The runner is a faithful copy of ac101._run_internal for the gray_ctl arm, parametrized by
(corrupt, schedule, regen_budget). At corrupt=False + SCHEDULE it reproduces AC100's gray_ctl
byte-for-byte; at corrupt=True + SCHEDULE it reproduces AC101's gray_ctl byte-for-byte. The
budgeted maintain is built by asserted source surgery on ac95.maintain / ac95.reg_from_active
(with budget=None reproducing ac95.maintain byte-for-byte), so `staged` differs from `both`
ONLY by the regen_budget constant.

Discipline: engineering first (seeds 0-7), then hashed protocol, then disjoint final seeds.
A negative result is a finding, not a failure.
"""
from pathlib import Path
import hashlib
import inspect
import json
import sys
import numpy as np
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

TICKS = ac95.TICKS
CORRUPT_TICK = ac95.CORRUPT_TICK
CORRUPT_BITS = ac95.CORRUPT_BITS
MOVE_TICK = ac95.MOVE_TICK
DEV = ac71.DEV
STREAK_N = ac12.STREAK_N

SCHEDULE = ac100.SCHEDULE          # [(8192, 'flip'), (12288, 'flip')]
NO_MOVES = []
mapping_at = ac100.mapping_at
move_ticks = ac100.move_ticks

# the frozen maintain reference (ac99.maintain = ac95.maintain + reg_reserve; reserve=False
# makes reg_reserve a no-op, so this is byte-identical to ac95.maintain in this study).
maintain = ac99.maintain

# the staged-repair budget: bound reg_from_active to at most this many replica-writes per tick.
# Chosen from the engineering sweep: 8 = 1/3 of the W=3 `_cap` (24), so the reconstruction
# (32 sites) is spread over >= 4 ticks instead of 2. Budgets 16/8 leave the failing seed 4450's
# death UNCHANGED (8408) and turn the immediate-survivors into deaths (reconstruction stalls via
# the cementing path); budgets 2/1/0 kill every seed with the reconstruction incomplete.
REPAIR_BUDGET = 8

# the budget-trace window (recorded per row for the audit): [CORRUPT_TICK-4, CORRUPT_TICK+32).
TRACE_LO = CORRUPT_TICK - 4
TRACE_HI = CORRUPT_TICK + 32

SOURCES = ['ac102.py', 'ac101.py', 'ac100.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py',
           'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC102_PROTOCOL_v1.md']

UNSEEN = [4934, 5002, 4880, 4950]            # fresh, non-adversarial (priorities reported);
                                            # stratified to span the material regime: 4934/5002
                                            # are death-prone (mat<=72 at the corruption tick),
                                            # 4880/4950 survive (mat>=99) — disclosed, pre-freeze.
ADVERSARIAL = [4883, 4901, 4928, 5038]       # fresh, all [3,0,2,1]
FINAL_SEEDS = UNSEEN + ADVERSARIAL
ENGINEERING = list(range(8))

ARMS = ('neither', 'move_only', 'corrupt_only', 'both', 'staged', 'never')


# ---------------- the budgeted maintain (asserted source surgery, computed once) ----------------
def _build_budgeted_maintain():
    """Return a `maintain` whose reg_from_active takes a per-tick `budget` from
    cfg['regen_budget']. budget=None reproduces ac95.maintain byte-for-byte (asserted)."""
    ns = dict(vars(ac95))
    reg_src = inspect.getsource(ac95.reg_from_active)
    assert reg_src.count("def reg_from_active(o, e, reg_offs):") == 1, "reg_from_active signature"
    reg_src = reg_src.replace(
        "def reg_from_active(o, e, reg_offs):",
        "def reg_from_active(o, e, reg_offs, budget=None):")
    assert reg_src.count("    n = min(_cap(b), len(sites))") == 1, "reg_from_active write line"
    reg_src = reg_src.replace(
        "    n = min(_cap(b), len(sites))",
        "    n = min(_cap(b), len(sites))\n    if budget is not None:\n        n = min(n, budget)")
    exec(compile(reg_src, 'ac102_reg_from_active', 'exec'), ns)
    maint_src = inspect.getsource(ac95.maintain)
    assert maint_src.count("        reg_from_active(o, e, reg_offs)") == 1, "maintain regen line"
    maint_src = maint_src.replace(
        "        reg_from_active(o, e, reg_offs)",
        "        reg_from_active(o, e, reg_offs, cfg.get('regen_budget'))")
    exec(compile(maint_src, 'ac102_maintain', 'exec'), ns)
    return ns['maintain']


MAINTAIN_BUDGETED = _build_budgeted_maintain()


def _arm_config(arm):
    """(corrupt, schedule, regen_budget) for each arm."""
    return {
        'neither':      (False, NO_MOVES, None),
        'move_only':    (False, SCHEDULE, None),
        'corrupt_only': (True,  NO_MOVES, None),
        'both':         (True,  SCHEDULE, None),
        'staged':       (True,  SCHEDULE, REPAIR_BUDGET),
        'never':        (True,  SCHEDULE, 0),
    }[arm]


# ---------------- the run (faithful to ac101._run_internal, parametrized) ----------------
def _run_core(seed, history, corrupt, schedule, regen_budget, maintain_fn,
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
    succ = ac95.Succession('real', encoded)
    step = ac95.build(cfg['ac_arm'], alloc, succ, build_offs, cfg)
    step.__globals__['maintain'] = maintain_fn
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
                # corruption-applied guard: all 8 bits now read wrong (majority flipped)
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
        if TRACE_LO <= t < TRACE_HI:
            fw = int(((o.body.traces[0, :CORRUPT_BITS].sum(axis=-1) > 3).astype(np.uint8)
                      != acquired[:CORRUPT_BITS]).sum())
            budget_trace.append(dict(t=t, mat_after=o.body.material,
                                     reg_writes=e.get('reg_writes', 0),
                                     streak_writes=e.get('streak_writes', 0),
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
                budget_trace=budget_trace,
                state_hash=o.digest()), o, trace


def run(seed, history, arm='both'):
    corrupt, schedule, budget = _arm_config(arm)
    fn = maintain if budget is None else MAINTAIN_BUDGETED
    row, o, _ = _run_core(seed, history, corrupt, schedule, budget, fn,
                          record_trace=False)
    row['arm'] = arm
    return row


# ---------------- observer-discard (per-tick, on the `both` arm) ----------------
def _mid_streak_tick(row, key=1, before_value=2, since=MOVE_TICK):
    for (t, k, before, after, dropped) in row['streak_events']:
        if k == key and before == before_value and not dropped and t >= since:
            return t
    return None


def observer_discard_equivalence(seed, history):
    """Per-tick observer-discard on the `both` arm (gray_ctl + corrupt=True), carried from AC101."""
    base, base_o, base_trace = _run_core(seed, history, True, SCHEDULE, None, maintain,
                                         record_trace=True)
    swap_tick = _mid_streak_tick(base, key=1, before_value=2)
    if swap_tick is None:
        return dict(seed=seed, history=history, status='no_mid_streak',
                    streak_events=base['streak_events'])
    swapped, swapped_o, swapped_trace = _run_core(seed, history, True, SCHEDULE, None, maintain,
                                                  record_trace=True, swap_at=swap_tick)
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
    return dict(seed=seed, history=history, swap_tick=swap_tick,
                streak_at_swap=2, host_dict_cleared=True,
                swap_applied=swapped['swap_applied'],
                per_tick_identical=per_tick_identical,
                n_equal=n_equal, n_ticks=len(base_trace), first_div=first_div,
                terminal_identical=base['state_hash'] == swapped['state_hash'],
                base_hash=base['state_hash'], swapped_hash=swapped['state_hash'])


# ---------------- arm identity (the single-change equivalence checks) ----------------
def staged_nobudget_identity(seed, history):
    """The budgeted maintain with budget=None reproduces the frozen maintain byte-for-byte —
    i.e. the regen_budget is the ONLY change in the `staged`/`never` arms (AC89's rule)."""
    a, _, _ = _run_core(seed, history, True, SCHEDULE, None, maintain, record_trace=False)
    b, _, _ = _run_core(seed, history, True, SCHEDULE, None, MAINTAIN_BUDGETED, record_trace=False)
    return a['state_hash'] == b['state_hash']


def arm_identity(seed, history):
    """Byte-identity licenses:
      - `move_only` reproduces AC100's gray_ctl (the move is the only change vs AC100).
      - `both` reproduces AC101's gray_ctl (the corruption is the only change vs AC100).
    """
    return {
        'move_only_is_ac100': run(seed, history, 'move_only')['state_hash'] ==
                              ac100.run(seed, history, 'gray_ctl', schedule=SCHEDULE)['state_hash'],
        'both_is_ac101': run(seed, history, 'both')['state_hash'] ==
                         ac101.run(seed, history, corrupt=True, schedule=SCHEDULE)['state_hash'],
    }


# ---------------- gates (recomputed from rows, no simulation) ----------------
def gates_ac102(rows, seeds, observer_discard):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history']), {})[r['arm']] = r
    n_ind = len(seeds) * 2

    both_rows = [r for r in rows if r['arm'] == 'both']
    # G1 -- the interaction: neither / move_only / corrupt_only all survive on every individual
    # (the death requires BOTH challenges).
    g1 = len(both_rows) == n_ind and all(
        by[(r['seed'], r['history'])]['neither']['completed']
        and by[(r['seed'], r['history'])]['move_only']['completed']
        and by[(r['seed'], r['history'])]['corrupt_only']['completed']
        for r in both_rows)

    # G2 -- reconstruction recovers under `both` (the unconditional internal-state composition).
    g2 = len(both_rows) == n_ind and all(
        r['fw_at_corrupt'] == CORRUPT_BITS and r['flipped_still_wrong'] == 0
        for r in both_rows)

    # G3 -- the timing hypothesis is FALSIFIED: staging does NOT rescue a `both`-death.
    # For every individual, `both` survives OR `staged` also dies (no individual where `both`
    # dies but `staged` survives). `staged` death set is a superset of `both`'s.
    g3 = all(
        by[(r['seed'], r['history'])]['both']['completed']
        or (not by[(r['seed'], r['history'])]['staged']['completed'])
        for r in both_rows)

    # G4 -- the staged schedule does NOT break recovery: it recovers the controller eventually
    # (fw->0) on every individual. Expected to FAIL (the cementing path stalls the
    # reconstruction on the survivors); recording the failure pins "reconstruction must be
    # immediate", not "staging is a viable schedule".
    staged_rows = [r for r in rows if r['arm'] == 'staged']
    g4 = len(staged_rows) == n_ind and all(
        r['flipped_still_wrong'] == 0 for r in staged_rows)

    # G5 -- never-repair must FAIL: no recovery (fw still wrong) and death on every individual.
    never_rows = [r for r in rows if r['arm'] == 'never']
    g5 = len(never_rows) == n_ind and all(
        r['flipped_still_wrong'] > 0 and not r['completed'] for r in never_rows)

    # G6 -- state sufficiency: per-tick observer-discard on `both` (non-vacuous, byte-identical).
    g6 = observer_discard is not None and len(observer_discard) == n_ind and all(
        d.get('status') != 'no_mid_streak' and d.get('swap_applied')
        and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
        for d in observer_discard.values())

    # G7 -- adversarial stratum: every adversarial seed satisfies G1 (single-challenge arms
    # survive) and G2 (reconstruction recovers under both).
    g7 = all(
        by[(r['seed'], r['history'])]['neither']['completed']
        and by[(r['seed'], r['history'])]['move_only']['completed']
        and by[(r['seed'], r['history'])]['corrupt_only']['completed']
        and by[(r['seed'], r['history'])]['both']['fw_at_corrupt'] == CORRUPT_BITS
        and by[(r['seed'], r['history'])]['both']['flipped_still_wrong'] == 0
        for r in both_rows if r['seed'] in ADVERSARIAL)

    return {
        'G1_interaction_death_requires_both': g1,
        'G2_reconstruction_recovers_under_both': g2,
        'G3_timing_hypothesis_falsified_staged_does_not_rescue': g3,
        'G4_staged_recovers_controller_eventually': g4,
        'G5_never_repair_must_fail': g5,
        'G6_state_sufficiency_observer_discard': g6,
        'G7_adversarial_stratum': g7,
        'G8_completeness_determinism_arm_identity': None,
    }


def preflight(protocol='AC102_PROTOCOL_v1.md'):
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
                 r['description_correct'], r['successions'], r['relinquishments'],
                 r['reacquisitions_by_move'], r['streak_final'], r['mat_at_corrupt'],
                 r['mat_min_post_corrupt'], r['first_W_empty'], r['first_C_empty'])
                for r in rows[-len(ARMS) * 2:]]), default=str), flush=True)
    obs = {f'{s}/{h}': observer_discard_equivalence(s, h) for s in seeds for h in (0, 1)}
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), arms=list(ARMS), REPAIR_BUDGET=REPAIR_BUDGET,
             rows=rows, observer_discard=obs),
        indent=2, default=str))
    print(json.dumps(dict(observer_discard={k: (v.get('per_tick_identical'), v.get('status'))
                                            for k, v in obs.items()}), indent=2, default=str))
    return rows, obs


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
                 r['description_correct'], r['successions'], r['relinquishments'],
                 r['reacquisitions_by_move'], r['streak_final'], r['mat_at_corrupt'],
                 r['mat_min_post_corrupt'])
                for r in rows[-len(ARMS) * 2:]]), default=str), flush=True)
    obs = {}
    for seed in seeds:
        for history in (0, 1):
            obs[f'{seed}/{history}'] = observer_discard_equivalence(seed, history)
    ident = {}
    for seed in seeds:
        for history in (0, 1):
            a = arm_identity(seed, history)
            a['staged_nobudget_is_both'] = staged_nobudget_identity(seed, history)
            ident[f'{seed}/{history}'] = a
    g = gates_ac102(rows, seeds, obs)
    first = rows[0]
    rerun = run(first['seed'], first['history'], first['arm'])
    g['G8_completeness_determinism_arm_identity'] = (
        len(rows) == len(seeds) * len(ARMS) * 2
        and rerun['state_hash'] == first['state_hash']
        and all(v.get('move_only_is_ac100') and v.get('both_is_ac101')
                and v.get('staged_nobudget_is_both') for v in ident.values()))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), unseen=UNSEEN, adversarial=ADVERSARIAL, arms=list(ARMS),
             REPAIR_BUDGET=REPAIR_BUDGET, hashes=hashes, gates=g, rows=rows,
             observer_discard=obs, arm_identity=ident),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac102_engineering_v1', ENGINEERING)
        return
    collect_finals('ac102_results_v1', FINAL_SEEDS)


if __name__ == '__main__':
    main()
