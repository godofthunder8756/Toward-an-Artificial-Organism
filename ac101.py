"""AC101: composition test -- internal memory + controller reconstruction + machinery turnover
+ adaptation in the SAME organism (gray_ctl baseline + the corruption challenge).

Parent: AC100 (frozen). AC100 consolidated AC99's success as the Gray encoding, not the reserve:
on the unseen cohort both `gray_ctl` (Gray, no reserve) and `bin_res` (binary + reserve) satisfy
the full per-move adaptation criterion (relinquish + re-acquire after every move + continued W/C/B
production + survive) on 4/4 distinct seeds. `gray_ctl` is adopted as the next baseline. One thing
AC100 did NOT do: it ran every condition with `corrupt=False` and treated the observer-discard as
"carrying forward" the controller-reconstruction challenge. Those are different tests -- discarding
observational history does not DAMAGE the controller, so the reconstruction machinery
(`reg_from_active`, re-instantiating the 126-bit program from the 130-bit description) was never
exercised against an actually-corrupted controller in the AC100 world.

AC101 asks the composition question: do the four demonstrated capabilities -- (1) internal memory
(the acquired routes), (2) controller reconstruction, (3) machinery turnover (W/C/B production +
recipe-succession), (4) adaptation (the Gray relinquishment streak + erase-on-relinquishment
re-acquisition) -- work together in the SAME tested organism, under the COMBINED challenge of a
controller corruption AND two successive route reversals?

The runner is a faithful copy of ac100._run_internal for the `gray_ctl` arm (Gray streak, no
reserve), with ONE parameter change: `corrupt=True`. At `corrupt=False` (the AC100 world) the runner
reproduces ac100's gray_ctl byte-for-byte (state_hash) -- that equivalence licenses attributing any
difference to the corruption alone (AC89's rule). The corruption is the AC80/85/87/89/92 challenge:
at CORRUPT_TICK == MOVE_TICK == 8192 (the simultaneous schedule) the first 8 bits of rule 0 are
flipped (4 of 7 replicas set to the wrong value), and the organism must re-instantiate the program
from its maintained 130-bit description through the paid, W-catalyzed `reg_from_active`.

Two seed strata, predeclared:
  - UNSEEN (4448-4451): fresh seeds, priorities reported not prespecified.
  - ADVERSARIAL (4466, 4481, 4504, 4510): fresh seeds whose acquired priority is AC83's
    adversarial [3,0,2,1] (the bank-1 renewal rule ranked last), predeclared SEPARATELY.

Discipline: engineering first (seeds 0-7, disjoint), then hashed protocol, then the two disjoint
final strata. A negative result is a finding, not a failure. Conservation (ac4.balance), the
observer-discard (on gray_ctl), the adaptation endpoints, and survival comparisons are kept.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import ac100            # the two-move schedule + mapping_at + move_ticks (the adopted baseline runner)
import ac99_d2          # Gray streak + GrayAllocEraseReserve
import ac99             # reserve primitives + constants (maintain = ac95.maintain + reg_reserve)
import ac96             # streak storage/offsets
import ac95             # _cap, build, maintain, Succession, description encode/decode, offset helpers
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

SCHEDULE = ac100.SCHEDULE          # [(8192, 'flip'), (12288, 'flip')] -- the two route reversals
mapping_at = ac100.mapping_at
move_ticks = ac100.move_ticks

# the reserve is NOT part of AC101 (the adopted baseline gray_ctl has no reserve); keep the
# maintain reference to ac99.maintain (== ac95.maintain + reg_reserve) so the corrupt=False path
# is byte-identical to ac100's gray_ctl (whose cfg['reserve']=False makes reg_reserve a no-op).
maintain = ac99.maintain

SOURCES = ['ac101.py', 'ac100.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py',
           'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC101_PROTOCOL_v1.md']

UNSEEN = [4448, 4449, 4450, 4451]
ADVERSARIAL = [4466, 4481, 4504, 4510]
FINAL_SEEDS = UNSEEN + ADVERSARIAL
ENGINEERING = list(range(8))


# ---------------- the run (faithful to ac100._run_internal, gray_ctl + corrupt, extra endpoints) ----
def _run_internal(seed, history, corrupt=True, schedule=None, ticks=TICKS,
                  record_trace=False, swap_at=None, damage=True):
    if schedule is None:
        schedule = SCHEDULE
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
    births_by_window = {i: {'W_birth': 0, 'C_birth': 0, 'B_birth': 0}
                        for i in range(len(mts) + 1)}
    first_dead = None
    description_correct_at_death = None
    fw_at_corrupt = None
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
            # the corruption is applied: count how many of the 8 corrupted bits now read wrong
            # (must be 8 = CORRUPT_BITS, by construction, unless the runner silently skipped the
            # corruption -- this is the "corruption actually happened" guard).
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
        if first_dead is None and o.body.dead:
            first_dead = t
            description_correct_at_death = int(
                (ac95.read_slot(o, ac95.read_pointer(o)) == encoded).sum())
    win_edges = mts + [ticks]
    relinq_by_move = []
    reacq_by_move = []
    for i, mt in enumerate(mts):
        lo, hi = mt, win_edges[i + 1]
        relinq_by_move.append(sum(1 for (dt, _p, _r) in drop_ticks if lo <= dt < hi))
        reacq_by_move.append(sum(1 for dt in reacquire_ticks[1] if lo <= dt < hi))
    inv = ac4.inventory(o.body)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    static = np.ones(prog.PROGRAM_BITS, dtype=bool)
    static[list(build_offs)] = False
    desc_bits = ac95.read_slot(o, ac95.read_pointer(o))
    desc_priority = ac95.decode_perm(desc_bits[ac95.PERM_OFFSET:ac95.PERM_OFFSET + ac95.PERM_BITS])
    active_end, phase_end, _ = ac95.ctrl_fields(o)
    return dict(seed=seed, history=history, corrupt=corrupt, schedule=[list(s) for s in schedule],
                ticks=ticks, completed=total['active'] == ticks, first_dead=first_dead,
                fw_at_corrupt=fw_at_corrupt,
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != acquired[:CORRUPT_BITS]).sum()),
                program_correct=int((decoded[static] == acquired[static]).sum()),
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
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                streak_writes=int(total['streak_writes']),
                state_hash=o.digest()), o, trace


def run(seed, history, corrupt=True, schedule=None, ticks=TICKS):
    row, o, _ = _run_internal(seed, history, corrupt, schedule, ticks, record_trace=False)
    return row


# ---------------- observer-discard (per-tick, on gray_ctl with corrupt=True) ----------------
def _mid_streak_tick(row, key=1, before_value=2, since=MOVE_TICK):
    for (t, k, before, after, dropped) in row['streak_events']:
        if k == key and before == before_value and not dropped and t >= since:
            return t
    return None


def observer_discard_equivalence(seed, history, corrupt=True, schedule=None):
    """Per-tick observer-discard on the gray_ctl arm, corrupt=True. At a mid-streak tick the
    succession observer AND the alloc (clearing the vestigial host streak dict) are replaced with
    fresh objects; the trajectory must be byte-identical at EVERY tick. The Gray streak must be
    recovered from maintained state alone (state sufficiency under the combined challenge)."""
    if schedule is None:
        schedule = SCHEDULE
    base, base_o, base_trace = _run_internal(seed, history, corrupt, schedule, TICKS,
                                             record_trace=True)
    swap_tick = _mid_streak_tick(base, key=1, before_value=2)
    if swap_tick is None:
        return dict(seed=seed, history=history, status='no_mid_streak',
                    streak_events=base['streak_events'])
    swapped, swapped_o, swapped_trace = _run_internal(seed, history, corrupt, schedule, TICKS,
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


# ---------------- corrupt-is-the-only-change (arm identity vs the AC100 gray_ctl baseline) ----
def arm_identity(seed, history):
    """gray_ctl with corrupt=False reproduces ac100's gray_ctl byte-for-byte (state_hash) at the
    same two-move schedule -- proving the corruption parameter is the ONLY change vs the adopted
    baseline (AC89's single-change equivalence rule)."""
    got = run(seed, history, corrupt=False)
    want = ac100.run(seed, history, 'gray_ctl', schedule=SCHEDULE)
    return got['state_hash'] == want['state_hash']


# ---------------- gates (recomputed from rows, no simulation) ----------------
def gates_ac101(rows, seeds, observer_discard, schedule=None):
    if schedule is None:
        schedule = SCHEDULE
    mts = move_ticks(schedule)
    n_win = len(mts) + 1
    n_ind = len(seeds) * 2

    def desc_intact(r):
        # description intact at death (for a non-survivor) or at the horizon (for a survivor)
        if r['completed']:
            return r['description_correct'] == 130
        return r['description_correct_at_death'] == 130

    def production(r):   # W/C/B births > 0 in every post-move window
        return all(r['births_by_window'].get(str(i), {}).get(k, 0) > 0
                   for i in range(1, n_win) for k in ('W_birth', 'C_birth', 'B_birth'))

    def reacq(r):        # >= 1 None->bound of key 1 in every post-move window
        return len(r['reacquisitions_by_move']) == len(mts) and \
            all(n >= 1 for n in r['reacquisitions_by_move'])

    # G1 -- reconstruction + description + recipe turnover (the internal-state composition),
    # unconditional per individual.
    g1 = len(rows) == n_ind and all(
        r['fw_at_corrupt'] == CORRUPT_BITS and r['flipped_still_wrong'] == 0
        and desc_intact(r) and r['successions'] >= 1
        for r in rows)

    # G2 -- adaptation + production + survival (the behavioural composition), per individual.
    g2 = len(rows) == n_ind and all(
        reacq(r) and production(r) and r['completed']
        for r in rows)

    # G3 -- state sufficiency: per-tick observer-discard on gray_ctl (non-vacuous).
    g3 = observer_discard is not None and len(observer_discard) == n_ind and all(
        d.get('status') != 'no_mid_streak' and d.get('swap_applied')
        and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
        for d in observer_discard.values())

    # G6 -- adversarial-priority stratum: G1 and G2 criteria hold on every adversarial seed.
    adv = [r for r in rows if r['seed'] in ADVERSARIAL]
    g6 = len(adv) == len(ADVERSARIAL) * 2 and all(
        r['fw_at_corrupt'] == CORRUPT_BITS and r['flipped_still_wrong'] == 0
        and desc_intact(r) and r['successions'] >= 1
        and reacq(r) and production(r) and r['completed']
        for r in adv)

    return {
        'G1_internal_state_composition': g1,
        'G2_behavioural_composition_adaptation_production_survival': g2,
        'G3_state_sufficiency_observer_discard_gray_ctl': g3,
        'G4_corrupt_is_the_only_change_arm_identity': None,
        'G5_completeness_determinism': None,
        'G6_adversarial_priority_stratum': g6,
    }


def preflight(protocol='AC101_PROTOCOL_v1.md'):
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
def collect_engineering(root, seeds, schedule=None):
    """AC101 engineering (no protocol, no freeze): gray_ctl + corrupt=True on the given seeds,
    with the extra composition endpoints. Reports per-seed outcomes and the observer-discard."""
    if schedule is None:
        schedule = SCHEDULE
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                r = run(seed, history, corrupt=True, schedule=schedule)
                rows.append(r)
                f.write(json.dumps(r) + '\n')
                f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['history'], r['completed'], r['first_dead'], r['fw_at_corrupt'],
                 r['flipped_still_wrong'], r['description_correct'],
                 r['description_correct_at_death'], r['successions'], r['routes'],
                 r['relinquishments_by_move'], r['reacquisitions_by_move'], r['streak_final'],
                 r['W'], r['C'], r['energy'], r['material'], r['fuel'])
                for r in rows[-2:]]), default=str), flush=True)
    obs = {f'{s}/{h}': observer_discard_equivalence(s, h, True, schedule)
           for s in seeds for h in (0, 1)}
    ident = {f'{s}/{h}': arm_identity(s, h) for s in seeds for h in (0, 1)}
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), schedule=[[list(s)] for s in schedule], rows=rows,
             observer_discard=obs, arm_identity=ident),
        indent=2, default=str))
    print(json.dumps(dict(observer_discard={k: (v.get('per_tick_identical'), v.get('status'))
                                            for k, v in obs.items()},
                          arm_identity=ident), indent=2, default=str))
    return rows, obs, ident


def collect_finals(root, seeds, schedule=None, do_preflight=True):
    """AC101 finals: gray_ctl + corrupt=True on the two predeclared strata. Gates derived from the
    rows; G3 (observer-discard) and G4 (arm identity) are two-run comparisons recorded here."""
    if schedule is None:
        schedule = SCHEDULE
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
                r = run(seed, history, corrupt=True, schedule=schedule)
                rows.append(r)
                f.write(json.dumps(r) + '\n')
                f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['history'], r['completed'], r['first_dead'], r['fw_at_corrupt'],
                 r['flipped_still_wrong'], r['description_correct'],
                 r['description_correct_at_death'], r['successions'], r['routes'],
                 r['relinquishments_by_move'], r['reacquisitions_by_move'],
                 [r['births_by_window'][str(i)]['W_birth'] for i in range(len(move_ticks(schedule)) + 1)])
                for r in rows[-2:]]), default=str), flush=True)
    obs = {}
    for seed in seeds:
        for history in (0, 1):
            obs[f'{seed}/{history}'] = observer_discard_equivalence(seed, history, True, schedule)
    ident = {f'{s}/{h}': arm_identity(s, h) for s in seeds for h in (0, 1)}
    g = gates_ac101(rows, seeds, obs, schedule)
    first = rows[0]
    rerun = run(first['seed'], first['history'], corrupt=True, schedule=schedule)
    g['G4_corrupt_is_the_only_change_arm_identity'] = bool(ident) and all(ident.values())
    g['G5_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 and rerun['state_hash'] == first['state_hash'])
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), unseen=UNSEEN, adversarial=ADVERSARIAL, hashes=hashes, gates=g,
             rows=rows, schedule=[[list(s)] for s in schedule], observer_discard=obs,
             arm_identity=ident),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac101_engineering_v1', ENGINEERING)
        return
    collect_finals('ac101_results_v1', FINAL_SEEDS)


if __name__ == '__main__':
    main()
