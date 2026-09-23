"""AC111 (I1): compose the supported cognitive mechanism with AC105's reconstruction + spending
architecture -- does composition introduce interference, or is any failure a standalone failure?

Parent chain: the supported cognitive mechanism is the AC107 one-bit cause estimate e in
{E_world=1, E_machinery=0}, stored in the dead-rule action bit (traces[0, bel_off]), in the C2
gated world (occluded used_held, q=0.5), as frozen by AC110 (C3). Its content is load-bearing
(AC108), its storage is inert (AC109), and its repair is inert (AC110): correctness during the
decision window is carried ENTIRELY by reacquisition (bel_write at open in-window contacts).

AC105's body is the reconstruction + spending architecture: the 130-bit description + succession
(AC85-89), a persistent reconstruction trigger (AC103: fire reg_from_active whenever
program_incomplete, not just on obs bit 2), and the allowance-42 budget rule (AC104:
budget = max(0, material - 42) reserved for the relinquishment decision).

The composition question (I1): when the cognitive mechanism's world is ALSO subject to AC105's
corruption (8 program bits majority-flipped at t=8192) and its spending rule, does reconstruction
interfere with the estimate's reacquisition -- or do the two mechanisms compose without
interference, so any failure is a standalone failure of one or the other?

The three challenges CO-OCCUR at t=8192 (the AC105 baseline schedule): corruption (reconstruction
challenge), route change (move = E_world), and access impairment (cut = E_machinery). The estimate
bit is excluded from reg_from_active BY CONSTRUCTION (AC110's build passes build_offs =
reg_offs + streak_offs + [bel_off] as the reconstruction exclude set), so reconstruction does NOT
overwrite the estimate directly. The open interference channels are (a) attention-hijack: the
corruption flips the contact rule (rule 0, mask 1) whose corrupted mask preempts other rules on the
corruption observation; (b) spending: the budget defers reconstruction when material < 42, while
bel_write is W-gated (not budget-gated). Both are measured here, not assumed.

Arms (bounded, matched):
  est               = AC110 maintained, corrupt=False. Reproduces AC110 byte-for-byte (the
                      cognitive mechanism alone).
  est_corrupt       = estimate + corruption, persistent trigger, unbounded reconstruction.
  est_corrupt_budget= estimate + corruption + allowance-42 budget (the full AC105 body).

Conditions (from AC110): no_cause, move, cut. CORRUPT_TICK = MOVE_TICK = CUT_TICK = 8192.

Discipline: engineering first (seeds 0-7), then a hashed protocol, then disjoint finals. A
negative result -- composition fails where neither mechanism fails alone -- is the finding.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac110
import ac107
import ac106
import ac104
import ac103
import ac12
import ac95
import ac96
import ac100
import ac4
import ac9
import ac71
import ac76
import ac99_d2
import ac5_program as prog

TICKS = ac110.TICKS
DEV = ac110.DEV
STREAK_N = ac110.STREAK_N
MOVE_TICK = ac110.MOVE_TICK
CUT_TICK = ac110.CUT_TICK
PORTS = ac110.PORTS
WINDOW = ac110.WINDOW
HOLD_N = ac110.HOLD_N
BEL_WORD_BIT = ac110.BEL_WORD_BIT
Q = ac110.Q
BEL_DAMAGE = ac110.BEL_DAMAGE

CORRUPT_TICK = ac95.CORRUPT_TICK            # 8192 == MOVE_TICK (the three challenges co-occur)
CORRUPT_BITS = ac76.CORRUPT_BITS            # 8 (rule 0, the contact/income rule)
DECISION_ALLOWANCE = ac104.DECISION_ALLOWANCE   # 42

ARMS = ('est', 'est_corrupt', 'est_corrupt_budget')
CONDITIONS = ('no_cause', 'move', 'cut')

ENGINEERING = list(range(8))
FINAL_SEEDS = [6300, 6301, 6302, 6303, 6304, 6305, 6306, 6307]   # fresh, disjoint, pre-freeze

SOURCES = ['ac111.py', 'ac110.py', 'ac107.py', 'ac106.py', 'ac104.py', 'ac103.py',
           'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py', 'ac95.py', 'ac76.py', 'ac71.py',
           'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py',
           'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py',
           'AC111_PROTOCOL_v1.md']


# ---------------- arm config ----------------
def _arm_config(arm):
    """(corrupt, maintain_fn, regen_budget, persistent) per arm."""
    return {
        'est':                (False, ac95.maintain,           None,      False),
        'est_corrupt':        (True,  ac103.MAINTAIN_PERSISTENT, None,    True),
        'est_corrupt_budget': (True,  ac104.MAINTAIN_BUDGET,    'budget', True),
    }[arm]


def _condition_params(condition):
    if condition == 'move':
        return [(MOVE_TICK, 'flip')], None, 0, 0
    if condition == 'cut':
        return [], 1, CUT_TICK, CUT_TICK + WINDOW
    return [], None, 0, 0          # no_cause


def _true_cause(condition):
    if condition == 'cut':
        return 0                  # E_machinery
    if condition == 'move':
        return 1                  # E_world
    return None


# ---------------- the run core (ac110._run_core + corruption + maintain_fn) ----------------
def _run_core(seed, history, arm, condition, corrupt, maintain_fn, regen_budget, persistent,
              record_trace=False, swap_at=None):
    ac12.PORTS = PORTS; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    bel_off = ac107.bel_offset(o)
    skip_est = False               # AC110's maintained arm (no_repair is out of scope here)
    alloc = ac110._make_alloc('maintained', seed, history, bel_off)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    streak_offs = ac96.streak_offsets(o)
    alloc.streak_offs = streak_offs
    reg_offs = ac95.resolve_offsets(o)
    build_offs = reg_offs + streak_offs + [bel_off]
    encoded = ac95.description_bits(priority)
    o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
    acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    cfg = dict(ac95.ARM_PARTS['gated'])
    cfg['reserve'] = False
    cfg['regen_budget'] = regen_budget
    cfg['persistent'] = persistent
    cfg['decision_allowance'] = DECISION_ALLOWANCE
    succ = ac95.Succession('real', encoded)
    schedule, cut_key, cut_start, cut_end = _condition_params(condition)
    cut_obj = ac106.ReadCut(cut_key, cut_start, cut_end)
    gate_rng = np.random.default_rng([seed, 1809])
    step = ac110.build_step(alloc, succ, build_offs, cfg, cut_obj, bel_off=bel_off,
                            skip_est=skip_est, gate_rng=gate_rng, q=Q)
    step.__globals__['maintain'] = maintain_fn
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    for k in ('reg_writes', 'succ_writes', 'ctrl_writes', 'timer_increments', 'timer_resets',
              'split_events', 'streak_writes', 'bel_writes', 'proactive_writes'):
        total[k] = 0
    first_dead = None
    drop_ticks = []
    restore_ticks = []
    trace = [] if record_trace else None
    was_bound = {0: False, 1: False}
    seen_bound = {0: False, 1: False}
    reacquire_ticks = {0: [], 1: []}
    bel_at_cut_end = None
    bel_ones_at_cut_end = None
    true_cause = _true_cause(condition)
    fw_at_corrupt = None
    recovery_tick = None
    swap_applied = False
    for t in range(TICKS):
        alloc.now = t
        cut_obj.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = ac110._make_alloc('maintained', seed, history, bel_off)
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
        coin = bool(rng.random() < .5) if PORTS == 2 else int(rng.integers(0, PORTS))
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
            fw_at_corrupt = int(((o.body.traces[0, :CORRUPT_BITS].sum(axis=-1) > 3).astype(np.uint8)
                                 != acquired[:CORRUPT_BITS]).sum())
        step.__globals__['now'] = t
        prev_drops = len(alloc.log['dropped'])
        prev_restores = len(alloc.log.get('restored', []))
        e = step(o, core, noise, directions, coin,
                 tuple(ac100.mapping_at(base_map, t, schedule)), [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
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
        if condition == 'cut' and t == CUT_TICK + WINDOW - 1:
            bel_at_cut_end = ac107.bel_read(o, bel_off)
            bel_ones_at_cut_end = int(o.body.traces[0, bel_off].sum())
        if corrupt and t >= CORRUPT_TICK and recovery_tick is None:
            fw_now = int(((o.body.traces[0, :CORRUPT_BITS].sum(axis=-1) > 3).astype(np.uint8)
                          != acquired[:CORRUPT_BITS]).sum())
            if fw_now == 0:
                recovery_tick = t
        if record_trace:
            trace.append((t, o.digest()))
        if first_dead is None and o.body.dead:
            first_dead = t
    bel_at_horizon = ac107.bel_read(o, bel_off)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, condition=condition,
                corrupt=bool(corrupt), regen_budget=regen_budget, persistent=persistent,
                ticks=TICKS, completed=total['active'] == TICKS, first_dead=first_dead,
                fw_at_corrupt=fw_at_corrupt, recovery_tick=recovery_tick,
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != acquired[:CORRUPT_BITS]).sum()),
                program_correct=int((decoded == acquired).sum()),
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                drop_ticks=drop_ticks,
                restore_ticks=restore_ticks,
                streak_final={0: ac99_d2.gray_streak_read(o, 0, streak_offs),
                              1: ac99_d2.gray_streak_read(o, 1, streak_offs)},
                reacquire_ticks=reacquire_ticks,
                bel=ac107.bel_read(o, bel_off),
                bel_at_horizon=bel_at_horizon,
                bel_at_cut_end=bel_at_cut_end,
                bel_ones_at_cut_end=bel_ones_at_cut_end,
                bel_events=getattr(alloc, 'bel_events', []),
                bel_attempts=getattr(alloc, 'bel_attempts', 0),
                bel_refused=getattr(alloc, 'bel_refused', 0),
                occluded_unproductive=getattr(alloc, 'occluded_unproductive', 0),
                occluded_reads_1=getattr(alloc, 'occluded_reads_1', 0),
                route1_bound_at_horizon=o.memory.read(1) is not None,
                swap_applied=swap_applied,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                streak_writes=int(total['streak_writes']),
                bel_writes=int(total['bel_writes']),
                proactive_writes=int(total['proactive_writes']),
                memory_writes=int(total['memory_writes']),
                state_hash=o.digest()), o, trace


def run(seed, history, arm, condition, record_trace=False):
    corrupt, maintain_fn, regen_budget, persistent = _arm_config(arm)
    row, o, _ = _run_core(seed, history, arm, condition, corrupt, maintain_fn,
                          regen_budget, persistent, record_trace=record_trace)
    return row


# ---------------- single-change license: est reproduces AC110 maintained byte-for-byte ----
def est_is_ac110(seed, history, condition):
    mine = run(seed, history, 'est', condition)
    ref = ac110.run(seed, history, 'maintained', condition, q=Q, bel_damage=BEL_DAMAGE)
    return mine['state_hash'] == ref['state_hash']


def preflight(protocol='AC111_PROTOCOL_v1.md'):
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


# ---------------- gates (recomputed from rows, no simulation) ----------------
def gates_ac111(rows, identity):
    """Recompute the prespecified gates from the saved rows and the est==AC110 identity dict.

    The core claim is NO INTERFERENCE between the estimate's reacquisition (bel_write) and
    AC105's reconstruction + spending (reg_from_active under the persistent trigger + allowance-42
    budget). The gates are categorical (seed-independent) wherever the claim is categorical;
    survival is reported as a bimodality-aware lower bound, not gated.
    """
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
    cells = sorted(by.keys())
    n_ind = len(rows) // (len(ARMS) * len(CONDITIONS))      # seeds x 2 histories

    # G1 -- single-change license: est reproduces AC110 maintained byte-for-byte everywhere.
    g1 = bool(identity) and all(identity.values())

    # G2 -- reconstruction completes under composition: est_corrupt_budget reaches fw==0 (the
    # estimate's presence does not block reg_from_active), non-vacuously (fw_at_corrupt == 8).
    cand_budget = [r for r in rows if r['arm'] == 'est_corrupt_budget']
    g2 = (len(cand_budget) == n_ind * len(CONDITIONS)
          and all(r['fw_at_corrupt'] == CORRUPT_BITS and r['flipped_still_wrong'] == 0
                  and r['recovery_tick'] is not None for r in cand_budget))

    # G3 -- cut: the estimate still reads E_machinery (0) and holds the route through the cut,
    # despite reconstruction firing on the same tick. Categorical.
    cut_cells = [c for c in cells if c[2] == 'cut']
    g3 = all(by[c]['est_corrupt_budget']['bel_at_cut_end'] == 0
             and by[c]['est_corrupt_budget']['relinquishments'] == 0
             and by[c]['est_corrupt_budget']['route1_bound_at_horizon']
             for c in cut_cells)

    # G4 -- move: the estimate still reads E_world and relinquishes the stale route, despite
    # reconstruction. The budget arm is the AC105 candidate (the unbounded arm is the known
    # starvation control). Relinquishment is the E_world consumption signature (E_machinery holds
    # indefinitely, so relinquishments==0 would be the discrimination failure).
    move_cells = [c for c in cells if c[2] == 'move']
    g4 = all(by[c]['est_corrupt_budget']['relinquishments'] >= 1 for c in move_cells)

    # G5 -- reacquisition untouched: bel_writes == 7 in the cut for the budget arm, identical to
    # the no-corruption est arm (the estimate is written exactly once and stays correct -- the
    # bel_off exclusion from reg_from_active is load-bearing; a reset would force a second write).
    g5 = all(by[c]['est_corrupt_budget']['bel_writes'] == 7 == by[c]['est']['bel_writes']
             for c in cut_cells)

    # G6 -- no-harm survival: the budget never introduces a survival penalty relative to the
    # unbounded arm (est_corrupt_budget survives wherever est_corrupt survives).
    g6 = True
    g6_cases = []
    for c in cells:
        if by[c]['est_corrupt']['completed'] and not by[c]['est_corrupt_budget']['completed']:
            g6 = False
            g6_cases.append(c)

    # reported (not gated): standalone failures of the two mechanisms acting alone.
    unbounded_dead = [(c, by[c]['est_corrupt']['first_dead'], by[c]['est_corrupt']['relinquishments'])
                      for c in cells if not by[c]['est_corrupt']['completed']]
    est_dead = [(c, by[c]['est']['first_dead']) for c in cells if not by[c]['est']['completed']]

    return {
        'G1_est_identity': g1,
        'G2_reconstruction_completes': g2,
        'G3_cut_estimate_holds': g3,
        'G4_move_estimate_relinquishes': g4,
        'G5_reacquisition_untouched': g5,
        'G6_no_harm_survival_budget': g6,
        '_g6_cases': g6_cases,
        '_unbounded_dead': unbounded_dead,
        '_est_dead': est_dead,
    }


def collect(root, seeds, conditions=None, do_preflight=False):
    if conditions is None:
        conditions = list(CONDITIONS)
    if do_preflight:
        preflight()
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    hashes = None
    if do_preflight:
        hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest()
                  for n in SOURCES if Path(n).exists()}
        (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for cond in conditions:
                    for arm in ARMS:
                        r = run(seed, history, arm, cond)
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['bel_at_cut_end'],
                 r['flipped_still_wrong'], r['recovery_tick'], r['bel_writes'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    ident = {f'{s}/{h}/{c}': est_is_ac110(s, h, c)
             for s in seeds for h in (0, 1) for c in conditions}
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), PORTS=PORTS, Q=Q,
             CORRUPT_TICK=CORRUPT_TICK, CORRUPT_BITS=CORRUPT_BITS,
             DECISION_ALLOWANCE=DECISION_ALLOWANCE, WINDOW=WINDOW, rows=rows,
             est_is_ac110=ident, hashes=hashes if do_preflight else None),
        indent=2, default=str))
    print(json.dumps(dict(est_is_ac110=ident), indent=2, default=str))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac111_engineering_v1', ENGINEERING)
        return
    if '--smoke' in sys.argv:
        collect('ac111_smoke_v1', [0, 1, 2])
        return
    if '--finals' in sys.argv:
        collect('ac111_results_v1', FINAL_SEEDS, do_preflight=True)
        return
    print('AC111: --engineering (seeds 0-7), --smoke (0-2), or --finals (6300-6307).')


if __name__ == '__main__':
    main()
