"""AC100: consolidation — binary/Gray streak x reserve/no-reserve factorial under repeated route changes.

Parent: AC99 (frozen). AC99 froze the Gray-coded streak (cheaper transitions) + the AC98/AC99
revised reserve and passed all five gates on unseen seeds 4440-4443. Three questions remain open
about whether that success depends on the *combination*, and none is answered by AC99 alone:

  1. Is the reserve necessary?  Every final Gray run includes it, and two never release it
     (D2's near-redundancy prediction). Redundancy has NOT been shown — it requires a
     Gray-without-reserve comparison.
  2. Does the cheaper transition generalize, or only shift the failure?  Gray changes write
     costs, reset costs, and damage responses wherever the counter operates.
  3. Is the acquired function sustainable across SUCCESSIVE disruptions, or does the dearer
     Gray reset (drop 7 + reset 21 = 28 replicas > RESERVE_LEVEL 21) compound under repeated
     route changes?

This runner is a 2x2 factorial — {binary, gray} streak x {no-reserve, reserve} — in the AC96/97/98/99
relinquishment world, with a *move schedule* (repeated route changes) instead of a single move. The
four arms, per individual:

  - `bin_ctl`  = ac99.AllocEraseReserve(reserve=False)          binary streak, no reserve
  - `bin_res`  = ac99.AllocEraseReserve(reserve=True)           binary streak + reserve (AC98/99 arch.)
  - `gray_ctl` = ac99_d2.GrayAllocEraseReserve(reserve=False)   Gray streak, no reserve
  - `gray_res` = ac99_d2.GrayAllocEraseReserve(reserve=True)    Gray streak + reserve (AC99 success arm)

The run loop is a faithful copy of ac99_d2._run_internal / ac99._run_internal (the two are identical
except for the allocator class and the streak read), parametrized by `code` and by a `schedule` of
channel-1 port moves. At the single-move schedule `[(8192, 'flip')]` each arm reproduces its AC99
runner byte-for-byte (state_hash) — that equivalence is what licenses attributing any difference to the
schedule change alone (AC89's rule).

Everything else (reserve policy level 21 with drop/stall/wlow triggers and the D1 atomic release+disarm,
sticky 1e-4 damage on both banks, 7-replica majority read threshold 4, prices 1 energy + 1 material per
replica, STREAK_N=6, erase-on-relinquishment, corrupt=False) is byte-for-byte the AC99 architecture.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import ac99            # binary streak + AllocEraseReserve + reserve primitives + constants
import ac99_d2         # Gray streak + GrayAllocEraseReserve
import ac96            # binary streak storage/read/write + AllocEraseMaintained base
import ac95            # _cap, build, maintain, Succession, mapping_at
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

# ---- reserve constants, unchanged (imported through ac99) ----
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

SOURCES = ['ac100.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py',
           'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC100_PROTOCOL_v1.md']

# ---- the move schedule (repeated route changes) ----
# The AC99 world moves channel 1 ONCE at t=8192 (transition='perm': port flips base[1] -> 1-base[1]).
# AC100 moves it REPEATEDLY so the dearer Gray reset (28-replica drop+reset) is exercised more than
# once. `SCHEDULE` is a list of (tick, 'flip') applied cumulatively: at each tick the mapping for
# channel 1 is base[1] flipped once per schedule entry with tick <= t.
MOVE2_TICK = 12288
SCHEDULE = [(MOVE_TICK, 'flip'), (MOVE2_TICK, 'flip')]   # flip at 8192, flip back at 12288
SINGLE_MOVE = [(MOVE_TICK, 'flip')]                       # reproduces AC99 transition='perm'


def mapping_at(base, t, schedule):
    """Channel mapping as a function of t under a move schedule (cumulative flips).

    `base` is the (seed % 2, (seed // 2) % 2) base mapping; the schedule is a list of
    (tick, 'flip' | port). Each entry with tick <= t applies: 'flip' toggles channel 1's
    port, an int sets it. At schedule == [(8192, 'flip')] this is identical to
    `ac95.mapping_at(base, t, 'perm', 8192)`.
    """
    m = list(base)
    for tick, kind in schedule:
        if t >= tick:
            if kind == 'flip':
                m[1] = 1 - m[1]
            else:
                m[1] = int(kind)
    return m


def move_ticks(schedule):
    return sorted({tick for (tick, _) in schedule})


# ---------------- the run (faithful to ac99/ac99_d2._run_internal, schedule-based) ----------------
def _run_internal(seed, history, code, reserve, damage, corrupt, schedule,
                  ticks, record_trace=False, swap_at=None, damage_rate=1e-4):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    assert code in ('binary', 'gray'), code
    if code == 'binary':
        Alloc = ac99.AllocEraseReserve
        streak_read = ac96.streak_read
    else:
        Alloc = ac99_d2.GrayAllocEraseReserve
        streak_read = ac99_d2.gray_streak_read
    alloc = Alloc('allocate', seed, history, reserve=reserve)
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
    cfg['reserve'] = reserve
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
    mts = move_ticks(schedule)
    # births per window: window 0 = [0, mts[0]), window i = [mts[i-1], mts[i]), last = [mts[-1], ticks)
    births_by_window = {i: {'W_birth': 0, 'C_birth': 0, 'B_birth': 0}
                        for i in range(len(mts) + 1)}
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
            alloc = Alloc('allocate', seed, history, reserve=reserve)
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
        if first_dead is None and o.body.dead:
            first_dead = t
    arm_events = [ev for ev in alloc.reserve_events if ev[1] == 'arm']
    rel_events = [ev for ev in alloc.reserve_events if ev[1] in ('drop', 'stall', 'wlow')]
    rel_kinds = [(ev[0], ev[1]) for ev in rel_events]
    inv = ac4.inventory(o.body)
    # per-move relinquishment / reacquisition counts (window [mts[i], mts[i+1]) or to horizon)
    win_edges = mts + [ticks]
    relinq_by_move = []
    reacq_by_move = []
    for i, mt in enumerate(mts):
        lo, hi = mt, win_edges[i + 1]
        relinq_by_move.append(sum(1 for (dt, _p, _r) in drop_ticks if lo <= dt < hi))
        reacq_by_move.append(sum(1 for dt in reacquire_ticks[1] if lo <= dt < hi))
    return dict(seed=seed, history=history, code=code, reserve=reserve, damage=damage,
                corrupt=corrupt, schedule=[list(s) for s in schedule], ticks=ticks,
                completed=total['active'] == ticks, first_dead=first_dead,
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
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                streak_writes=int(total['streak_writes']),
                state_hash=o.digest()), o, trace


def run(seed, history, code='gray_res', reserve=None, damage=True, corrupt=False,
        schedule=None, ticks=TICKS):
    """Run one individual under one of the four arms.

    `code` is one of 'bin_ctl', 'bin_res', 'gray_ctl', 'gray_res' (reserve is implied by the
    suffix; an explicit `reserve` overrides for low-level callers). `schedule` defaults to
    SCHEDULE (the repeated moves); pass SINGLE_MOVE to reproduce the AC99 single-move world.
    """
    if schedule is None:
        schedule = SCHEDULE
    if code in ('bin_ctl', 'bin_res'):
        enc = 'binary'
        rv = reserve if reserve is not None else (code == 'bin_res')
    elif code in ('gray_ctl', 'gray_res'):
        enc = 'gray'
        rv = reserve if reserve is not None else (code == 'gray_res')
    else:
        raise ValueError(f'unknown arm code {code!r}')
    row, o, _ = _run_internal(seed, history, enc, rv, damage, corrupt,
                              schedule, ticks, record_trace=False)
    row['condition'] = code
    return row


ARMS = ['bin_ctl', 'bin_res', 'gray_ctl', 'gray_res']


# ---------------- observer-discard (per-tick, on the gray_res success arm) ----------------
def _mid_streak_tick(row, key=1, before_value=2, since=MOVE_TICK):
    for (t, k, before, after, dropped) in row['streak_events']:
        if k == key and before == before_value and not dropped and t >= since:
            return t
    return None


def observer_discard_equivalence(seed, history, schedule=None, damage=True, corrupt=False):
    """Per-tick observer-discard on the gray_res arm (the success arm), schedule-aware.

    At a mid-streak tick the succession observer AND the alloc (clearing the vestigial host
    streak dict) are replaced with fresh objects; the trajectory must be byte-identical at
    EVERY tick. The Gray streak and the reserve must be recovered from maintained state alone.
    """
    if schedule is None:
        schedule = SCHEDULE
    base, base_o, base_trace = _run_internal(seed, history, 'gray', True, damage, corrupt,
                                             schedule, TICKS, record_trace=True)
    swap_tick = _mid_streak_tick(base, key=1, before_value=2)
    if swap_tick is None:
        return dict(seed=seed, history=history, status='no_mid_streak',
                    streak_events=base['streak_events'])
    swapped, swapped_o, swapped_trace = _run_internal(seed, history, 'gray', True, damage,
                                                      corrupt, schedule, TICKS,
                                                      record_trace=True, swap_at=swap_tick)
    assert base_trace is not None and swapped_trace is not None
    n_equal = 0
    first_div = None
    for (t1, d1), (t2, d2) in zip(base_trace, swapped_trace):
        assert t1 == t2, f'tick grid mismatch {t1} vs {t2}'
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


# ---------------- protocol freeze + the standing gates ----------------
def preflight(protocol='AC100_PROTOCOL_v1.md'):
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


def gates_ac100(rows, seeds, observer_discard=None, schedule=None):
    """Recompute the AC100 gates from the saved rows (no simulation).

    G1 (sustained adaptation WITHOUT the reserve, on gray_ctl) and G5 (endogenous reserve) are
    derived from the rows; G2/G3 (no-harm, encoding and reserve directions) compare gray_res
    against its two direct controls (bin_res for the encoding, gray_ctl for the reserve); G4
    (per-tick observer-discard) is re-read from its recorded dict. G6 (completeness/determinism/
    arm identity) is set by the collector.
    """
    if schedule is None:
        schedule = SCHEDULE
    mts = move_ticks(schedule)
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history']), {})[r['condition']] = r
    n_ind = len(seeds) * 2

    def a_relinq(r):   # relinquished after EVERY move (a drop with the register bit set, per move)
        return (len(r['relinquishments_by_move']) == len(mts)
                and all(n >= 1 for n in r['relinquishments_by_move'])
                and all(reg for (_t, _p, reg) in r['drop_ticks']))

    def a_reacq(r):    # re-acquired after EVERY move (a None->bound transition per move window)
        return len(r['reacquisitions_by_move']) == len(mts) and \
            all(n >= 1 for n in r['reacquisitions_by_move'])

    def a_prod(r):     # continued W/C/B production in EVERY post-move window
        n_win = len(mts) + 1
        return all(r['births_by_window'].get(str(i), {}).get(k, 0) > 0
                   for i in range(1, n_win) for k in ('W_birth', 'C_birth', 'B_birth'))

    def a_surv(r):     # survival to the horizon
        return bool(r['completed'])

    # G1: sustained adaptation WITHOUT the reserve — every gray_ctl individual satisfies all four
    gray_ctl = [r for r in rows if r['condition'] == 'gray_ctl']
    g1 = len(gray_ctl) == n_ind and all(
        a_relinq(r) and a_reacq(r) and a_prod(r) and a_surv(r) for r in gray_ctl)

    # G2 (encoding no-harm): no individual where bin_res survives and gray_res dies
    # G3 (reserve no-harm):   no individual where gray_ctl survives and gray_res dies
    g2_enc, g3_res = True, True
    for s in seeds:
        for h in (0, 1):
            gr = by.get((s, h), {}).get('gray_res')
            bn = by.get((s, h), {}).get('bin_res')
            gc = by.get((s, h), {}).get('gray_ctl')
            if gr and bn and bn['completed'] and not gr['completed']:
                g2_enc = False
            if gr and gc and gc['completed'] and not gr['completed']:
                g3_res = False

    # G4: state sufficiency — per-tick observer-discard on the gray_res arm (carry AC99's G3)
    g4 = observer_discard is not None and len(observer_discard) == n_ind and all(
        d.get('status') != 'no_mid_streak' and d.get('swap_applied')
        and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
        for d in observer_discard.values())

    # G5: endogenous reserve — no external rescue (release never exceeds withhold), both reserve arms
    res_arms = [r for r in rows if r['condition'] in ('gray_res', 'bin_res')]
    g5 = all(r['reserve_m'] > 0 and r['reserve_released_m'] <= r['reserve_m'] for r in res_arms)

    return {
        'G1_sustained_adaptation_no_reserve': g1,
        'G2_no_harm_encoding_gray_res_vs_bin_res': g2_enc,
        'G3_no_harm_reserve_gray_res_vs_gray_ctl': g3_res,
        'G4_state_sufficiency_per_tick_discard': g4,
        'G5_endogenous_reserve_no_external_rescue': g5,
        'G6_completeness_determinism_arm_identity': None,
    }


def collect_engineering(root, seeds, schedule=None, do_single_move_equiv=True):
    """AC100 engineering (no protocol, no freeze): the 2x2 factorial on the given seeds.

    Reports, per seed, the four arms' outcomes, the three question contrasts (Q1 reserve
    necessity, Q2 Gray generalization vs shift, Q3 sustainability), and the single-move
    byte-identity of each arm against its AC99 runner.
    """
    if schedule is None:
        schedule = SCHEDULE
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for code in ARMS:
                    r = run(seed, history, code, schedule=schedule, damage=True, corrupt=False)
                    rows.append(r)
                    f.write(json.dumps(r) + '\n')
                    f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['relinquishments_by_move'],
                 r['reacquisitions_by_move'], r['reserve_release_kinds'], r['streak_final'])
                for r in rows[-len(ARMS) * 2:]]), default=str), flush=True)
    # single-move byte-identity: each arm reproduces its AC99 runner at SINGLE_MOVE
    equiv = {}
    if do_single_move_equiv:
        for seed in seeds:
            for history in (0, 1):
                for code, ref in (('bin_res', 'binary'), ('gray_res', 'gray'),
                                  ('bin_ctl', 'binary_no_reserve'), ('gray_ctl', 'gray_no_reserve')):
                    if code == 'bin_res':
                        want = ac99.run(seed, history, 'gated', reserve=True, damage=True,
                                        corrupt=False, transition='perm')
                    elif code == 'gray_res':
                        want = ac99_d2.run(seed, history, 'gated', reserve=True, damage=True,
                                           corrupt=False, transition='perm')
                    elif code == 'bin_ctl':
                        want = ac99.run(seed, history, 'gated', reserve=False, damage=True,
                                        corrupt=False, transition='perm')
                    else:
                        want = ac99_d2.run(seed, history, 'gated', reserve=False, damage=True,
                                           corrupt=False, transition='perm')
                    got = run(seed, history, code, schedule=SINGLE_MOVE, damage=True, corrupt=False)
                    equiv[f'{seed}/{history}/{code}'] = got['state_hash'] == want['state_hash']
    # per-tick observer-discard on the gray_res arm (state sufficiency)
    obs = {f'{s}/{h}': observer_discard_equivalence(s, h, schedule, True, False)
           for s in seeds for h in (0, 1)}
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), schedule=[[list(s)] for s in schedule],
             single_move_equivalence=equiv, observer_discard=obs, rows=rows),
        indent=2, default=str))
    print(json.dumps(dict(single_move_equivalence=equiv), indent=2, default=str))
    print(json.dumps(dict(observer_discard={k: (v.get('per_tick_identical'), v.get('status'))
                                            for k, v in obs.items()}), indent=2, default=str))
    return rows, equiv, obs


def collect_finals(root, seeds, schedule=None, do_preflight=True):
    """AC100 finals: the 2x2 factorial in the repeated-move world. Gates are derived from the
    rows; G3 (observer-discard) and G5's arm identity are computed here and recorded.
    do_preflight=False is for a smoke run (the protocol is frozen only before finals)."""
    if schedule is None:
        schedule = SCHEDULE
    if do_preflight:
        preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for code in ARMS:
                    r = run(seed, history, code, schedule=schedule, damage=True, corrupt=False)
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['relinquishments_by_move'],
                 r['reacquisitions_by_move'],
                 [r['births_by_window'][str(i)]['W_birth'] for i in range(len(move_ticks(schedule)) + 1)],
                 r['reserve_m'], r['reserve_released_m'], r['reserve_release_kinds'])
                for r in rows[-len(ARMS) * 2:]]), default=str), flush=True)
    # ---- G3 per-tick observer-discard (two-run comparison, per gray_res individual) ----
    obs = {}
    for seed in seeds:
        for history in (0, 1):
            obs[f'{seed}/{history}'] = observer_discard_equivalence(seed, history, schedule)
    # ---- G6 arm identity: each arm reproduces its AC99 runner byte-for-byte at the single-move
    # schedule, proving the schedule change is the ONLY change (and the runner is a faithful extension).
    single_equiv = {}
    for seed in seeds:
        for history in (0, 1):
            refs = {
                'bin_res': ac99.run(seed, history, 'gated', reserve=True, damage=True, corrupt=False, transition='perm'),
                'gray_res': ac99_d2.run(seed, history, 'gated', reserve=True, damage=True, corrupt=False, transition='perm'),
                'bin_ctl': ac99.run(seed, history, 'gated', reserve=False, damage=True, corrupt=False, transition='perm'),
                'gray_ctl': ac99_d2.run(seed, history, 'gated', reserve=False, damage=True, corrupt=False, transition='perm'),
            }
            for code in ARMS:
                single_equiv[f'{seed}/{history}/{code}'] = \
                    run(seed, history, code, schedule=SINGLE_MOVE)['state_hash'] == refs[code]['state_hash']
    g = gates_ac100(rows, seeds, obs, schedule)
    first = rows[0]
    rerun = run(first['seed'], first['history'], first['condition'], schedule=schedule)
    g['G6_completeness_determinism_arm_identity'] = (
        len(rows) == len(seeds) * 2 * len(ARMS)
        and rerun['state_hash'] == first['state_hash']
        and bool(single_equiv) and all(single_equiv.values()))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows, schedule=[[list(s)] for s in schedule],
             arms=ARMS, observer_discard=obs, single_move_equivalence=single_equiv),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac100_engineering_v1', list(range(8)))
        return
    if '--eng8' in sys.argv:
        collect_engineering('ac100_engineering_v2', list(range(8, 16)))
        return
    collect_finals('ac100_results_v1', [4444, 4445, 4446, 4447])


if __name__ == '__main__':
    main()
