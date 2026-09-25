"""AC115 (I3, engineering): the integrated successor — SR-2 admission gate on the AC105 closure.

Implements the I2 design (I2_INTEGRATED_EXCHANGE_DESIGN_v1.md): the AC114 SR-2 link-specific
admission gate composed with the AC105 five-mechanism closure architecture, in ONE organism and
ONE run.

Base architecture (fixed): AC105 `persistent_budget` at the `simult` condition (corruption@8192 +
move@8192,12288, TICKS=16384, DECISION_ALLOWANCE=42) — the full five-mechanism candidate
(description turnover, succession coordination, reconstruction, internalized operational memory,
decision allowance). The ONLY addition is the admission gate on `ac4.react` actions 0/1:

    ADMIT(b, c) in {site, count, none}

`site` admits iff the channel's declared gate link is live (`b.boundary[GATE_LINKS[c]] > 0`),
`count` is the aggregate-B-count rival (live links >= B_MIN), `none` is the frozen always-admit
bypass. The gate reads organism state only — no host state, no challenge-time knowledge.

The gate + the boundary interventions (puncture, retention-rescue, external B, permeant) are
applied to `ac12.react_world()` (yields 64/64) and the AC105-built step via the SAME markers as
AC114, composed with `ac95.build`'s surgery. Yields are AC105's (`in_f=64`, `in_m=64`), a
DISCLOSED difference from AC114's frozen `in_f=32` (I2 §8): the gate is yield-agnostic, so the
discriminations transfer but the intake scalars do not.

Engineering (I3) first, then frozen confirmation (I4). `--engineering` collects the
engineering cohort (seeds 0-7, disclosed); `--finals` collects the untouched final cohort
(seeds 6600-6607) into `ac115_results_v1/` after `AC115_PROTOCOL_v1.md` is hashed. The
single-change license (G1) is verified directly — the intact-boundary `keep`/`rival`/
`reference` arms are byte-identical to each other AND to AC105 `persistent_budget` at
`simult` (state_hash).
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import inspect
import json
import sys
import numpy as np
import ac105
import ac104
import ac102
import ac100
import ac99_d2
import ac96
import ac95
import ac114
import ac12
import ac4
import ac71
import ac9
import ac5_program as prog
from ac1 import decode

TICKS = ac95.TICKS                  # 16384
CORRUPT_TICK = ac95.CORRUPT_TICK    # 8192
CORRUPT_BITS = ac95.CORRUPT_BITS    # 8
MOVE_TICK = ac95.MOVE_TICK          # 8192
MOVE2_TICK = 12288
DEV = ac71.DEV
STREAK_N = ac12.STREAK_N
DECISION_ALLOWANCE = ac104.DECISION_ALLOWANCE    # 42

mapping_at = ac100.mapping_at
move_ticks = ac100.move_ticks

# ---------------------------------------------------------------------------
# Supplied world constants (charter v2 §5). Fixed at protocol time.
# ---------------------------------------------------------------------------
GATE_LINKS = ac114.GATE_LINKS          # {0: (0,), 1: (1,)}
B_MIN = ac114.B_MIN                    # 10
PUNCTURE_LINKS = ac114.PUNCTURE_LINKS  # (0,)
NONGATE_PUNCTURE_LINKS = ac114.NONGATE_PUNCTURE_LINKS  # (5,)
YIELD_F = 64                           # AC105 reaction yield (DISCLOSED vs AC114's 32)
YIELD_M = 64                           # AC105 reaction yield

# Puncture timing: discrimination arms puncture a MATURE organism (AC114 rule 2);
# composition-stress arms puncture coincident with corruption + move (AC105 baseline).
PUNCTURE_TICK = 512
PUNCTURE_TICK_SIMULT = CORRUPT_TICK    # 8192

ARMS = ('keep', 'reference', 'rival',
        'puncture', 'rival_puncture', 'puncture_non_gate',
        'no_B', 'no_B_retention', 'no_B_retention_ref', 'B_rescue',
        'puncture_simult', 'rival_puncture_simult',
        'permeant')

# gate per arm (the admission model). `none` is the frozen always-admit bypass.
GATE = {'keep': 'site', 'rival': 'count', 'reference': 'none',
        'puncture': 'site', 'rival_puncture': 'count', 'puncture_non_gate': 'site',
        'no_B': 'site', 'no_B_retention': 'site', 'no_B_retention_ref': 'none',
        'B_rescue': 'site',
        'puncture_simult': 'site', 'rival_puncture_simult': 'count',
        'permeant': 'site'}

# challenge per arm: 'simult' = corruption@8192 + move@8192,12288 (AC105 baseline);
# 'none' = no corruption, no move (the boundary intervention is the sole event).
CHALLENGE = {'keep': 'simult', 'reference': 'simult', 'rival': 'simult',
             'puncture': 'none', 'rival_puncture': 'none', 'puncture_non_gate': 'none',
             'no_B': 'none', 'no_B_retention': 'none', 'no_B_retention_ref': 'none',
             'B_rescue': 'none',
             'puncture_simult': 'simult', 'rival_puncture_simult': 'simult',
             'permeant': 'none'}

# B production suppressed (AC114/AC10: action 8 routed through the frozen `no_B` arm guard).
NO_B_ARMS = ('no_B', 'no_B_retention', 'no_B_retention_ref', 'B_rescue')

CONDITIONS = {
    'none':   (False, []),
    'simult': (True, [(MOVE_TICK, 'flip'), (MOVE2_TICK, 'flip')]),
}

ADMIT_FN = ac114.ADMIT_FN   # {'site': _admit_site, 'count': _admit_count, 'none': _admit_none}

ENGINEERING = list(range(8))
FINAL_SEEDS = list(range(6600, 6608))   # untouched, disjoint from every prior family (I2 §10)

SOURCES = ['ac115.py', 'ac105.py', 'ac104.py', 'ac103.py', 'ac102.py', 'ac101.py', 'ac100.py',
           'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py', 'ac95.py', 'ac76.py', 'ac71.py',
           'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py',
           'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py', 'ac114.py',
           'AC115_PROTOCOL_v1.md']

# ---------------------------------------------------------------------------
# Surgery markers (asserted before every replacement; shared with ac12/ac114/ac71/ac95).
# ---------------------------------------------------------------------------
STEP_SRC = ac12.STEP_SRC          # inspect.getsource(ac9.step)
REACT_SRC = ac114.REACT_SRC       # inspect.getsource(ac4.react)

IN_F_LINE = ac12.IN_F_LINE
IN_M_LINE = ac12.IN_M_LINE
CANDIDATES_LINE = ac114.CANDIDATES_LINE
CANDIDATES_LINE_PUNCTURED = ac114.CANDIDATES_LINE_PUNCTURED
B_EXPIRY_LINE = ac114.B_EXPIRY_LINE
MOVE_CALL = ac114.MOVE_CALL
MOVE_CALL_NEW = ac114.MOVE_CALL_NEW

# The gate wraps actions 0/1 in `if ADMIT(b,c):` at AC105's yields (64/64).
GATED_IN_F = ("        if ADMIT(b,0):\n"
              "            e['in_f']=64; e['overflow_f']=max(0,b.fuel+64-64); b.fuel=min(64,b.fuel+64)")
GATED_IN_M = ("        if ADMIT(b,1):\n"
              "            e['in_m']=64; e['overflow_m']=max(0,b.material+64-256); b.material=min(256,b.material+64)")


def make_react_gated(admit, puncture_mask, no_B=False):
    """Compile ac4.react with the admission gate (yields 64/64) and the puncture mask.

    The gate wraps actions 0/1 in `if ADMIT(c)`. The puncture adds `& ~PUNCTURE` to the
    action-8 candidate set. `no_B` suppresses action 8 entirely via the frozen `arm` guard.
    """
    src = REACT_SRC
    assert src.count(IN_F_LINE) == 1, 'unexpected react text (in_f)'
    src = src.replace(IN_F_LINE, GATED_IN_F)
    assert src.count(IN_M_LINE) == 1, 'unexpected react text (in_m)'
    src = src.replace(IN_M_LINE, GATED_IN_M)
    assert src.count(CANDIDATES_LINE) == 1, 'unexpected react text (candidates)'
    src = src.replace(CANDIDATES_LINE, CANDIDATES_LINE_PUNCTURED)
    ns = dict(vars(ac4))
    ns['ADMIT'] = admit
    ns['PUNCTURE'] = puncture_mask
    fns = {}
    exec(compile(src, 'ac115_react', 'exec'), ns, fns)
    react = fns['react']
    if no_B:
        def react(b, action, arm, e, _f=react):
            return _f(b, action, 'no_B', e)
    return react


def build_integrated(ac_arm, alloc, succ, reg_offs, cfg, admit, puncture_mask=None,
                     no_B=False, retention_rescue=False, rescue_B=False,
                     puncture_links=None, permeant=False):
    """The AC105 build (ac95.build surgery) + AC114's boundary surgery + the gated react.

    Faithful to ac95.build (same source, same markers, same namespace), with the admission
    gate substituted for `ac12.react_world()` and the boundary interventions applied at the
    same markers AC114 uses on `ac9.step` (B-expiry line for puncture/external-B; the transport
    call for retention-rescue/permeant). No conservation identity is patched.
    """
    base, cut = ac71.arm_parts(ac_arm)
    src = STEP_SRC
    ns = dict(vars(ac9))
    ns['maintain'] = ac95.maintain
    ns['succ'] = succ
    ns['reg_offs'] = reg_offs
    ns['cfg'] = cfg
    if cfg.get('block_W'):
        ns['birth'] = ac95.make_birth(ns, cfg)
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    assert src.count(ac95.ACTION_LINE) == 1
    src = src.replace(ac95.ACTION_LINE, "        maintain(o,e,succ,reg_offs,cfg,now)\n" + ac95.ACTION_LINE)
    assert src.count(ac95.BALANCE_LINE) == 1
    src = src.replace(ac95.BALANCE_LINE,
                      "    e['writes']+=e.get('reg_writes',0)+e.get('succ_writes',0)+e.get('ctrl_writes',0)\n"
                      + ac95.BALANCE_LINE)
    # ---- AC114 boundary step-level surgery (composed with the AC105 build) ----
    if retention_rescue or permeant or rescue_B:
        assert src.count(MOVE_CALL) == 1, 'unexpected step text (transport call)'
        ns['impermeant_mask'] = np.zeros(20, dtype=bool) if permeant else np.ones(20, dtype=bool)
        ns['retention_rescue'] = bool(retention_rescue)
        src = src.replace(MOVE_CALL, MOVE_CALL_NEW)
    if rescue_B:
        assert src.count(B_EXPIRY_LINE) == 1, 'unexpected step text (B expiry)'
        src = src.replace(B_EXPIRY_LINE, B_EXPIRY_LINE + '\n    external_B_restore(b,e)')
        ns['external_B_restore'] = ac114.external_B_restore
    if puncture_links is not None:
        assert src.count(B_EXPIRY_LINE) == 1, 'unexpected step text (B expiry)'
        src = src.replace(B_EXPIRY_LINE, B_EXPIRY_LINE + '\n    puncture_gate(b,e)')
        ns['puncture_gate'] = ac114.make_puncture_gate(puncture_links)
    # ---- gated react (AC114 gate + AC105 yields 64/64) ----
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    if puncture_mask is None:
        puncture_mask = np.zeros(20, dtype=bool)
    react = make_react_gated(admit, puncture_mask, no_B=no_B)
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    ns['now'] = 0
    fns = {}
    exec(compile(src, 'ac115_step', 'exec'), ns, fns)
    return fns['step']


# ---------------- measurement wrappers (observational, no host state read by the organism) -----
def make_react_counted(react_fn, acquired, counters):
    """Cementing measurement on action 2 (carried from ac105, observational)."""
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


def make_admission_recorder(react_fn, admission, clock):
    """Record per-contact admission (action 0/1 = channel contact with port match).

    A react call with action in (0,1) is an ATTEMPTED contact (ac9.step calls react only on
    port match); `e['in_f']`/`e['in_m']` afterwards is the admission. Observational only: the
    organism never reads `admission` or `clock`.
    """
    def recorded(b, action, arm, e):
        r = react_fn(b, action, arm, e)
        if action in (0, 1):
            admitted = int((e.get('in_f', 0) if action == 0 else e.get('in_m', 0)) > 0)
            admission[f'ch{action}_attempted'] += 1
            admission[f'ch{action}_admitted'] += admitted
            admission['events'].append((clock['t'], action, admitted))
        return r
    return recorded


# ---------------- the run (faithful to ac105._run_core + the gate/boundary deltas) -------------
def _run_core(seed, history, corrupt, schedule, admit, no_B, puncture_links, puncture_tick,
              retention_rescue=False, rescue_B=False, permeant=False,
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
    cfg['regen_budget'] = 'budget'
    cfg['persistent'] = True
    cfg['decision_allowance'] = DECISION_ALLOWANCE
    succ = ac95.Succession('real', encoded)

    def _build(p_mask, p_links):
        return build_integrated(cfg['ac_arm'], alloc, succ, build_offs, cfg, admit,
                                puncture_mask=p_mask, no_B=no_B,
                                retention_rescue=retention_rescue, rescue_B=rescue_B,
                                puncture_links=p_links, permeant=permeant)

    if puncture_links is not None:
        mask = np.zeros(20, dtype=bool)
        for link in puncture_links:
            mask[link] = True
        step_pre = _build(np.zeros(20, dtype=bool), None)
        step_post = _build(mask, puncture_links)
    else:
        step_pre = step_post = _build(np.zeros(20, dtype=bool), None)

    cement = {'action2_writes': 0, 'action2_cementing': 0}
    admission = {'events': [], 'ch0_attempted': 0, 'ch0_admitted': 0,
                 'ch1_attempted': 0, 'ch1_admitted': 0}
    clock = {'t': 0}
    for s in (step_pre, step_post):
        s.__globals__['maintain'] = ac104.MAINTAIN_BUDGET
        react = s.__globals__['ac4'].react
        react = make_admission_recorder(react, admission, clock)
        react = make_react_counted(react, acquired, cement)
        s.__globals__['ac4'].react = react

    def _bind(**kw):
        for s in (step_pre, step_post):
            for k, v in kw.items():
                s.__globals__[k] = v

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
    allowance_breached = 0
    min_material_seen = 10**9
    fw_by_move = {}
    mt_set = set(mts)
    gate0_dead_tick = None
    gate1_dead_tick = None
    first_gate_dead = None

    for t in range(TICKS):
        alloc.now = t
        clock['t'] = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = Alloc('allocate', seed, history, reserve=False)
            alloc.streak_offs = streak_offs
            alloc.offs = offs
            alloc.shadow = o.body.traces[0].copy()
            alloc.now = t
            _bind(succ=succ, alloc=alloc, allowance=alloc.allowance)
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
        step = step_pre if (puncture_tick is not None and t < puncture_tick) else step_post
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
        if t in mt_set:
            fw_by_move[t] = int(((o.body.traces[0, :CORRUPT_BITS].sum(axis=-1) > 3).astype(np.uint8)
                                 != acquired[:CORRUPT_BITS]).sum())
        if ac102.TRACE_LO <= t < ac102.TRACE_HI:
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
        min_material_seen = min(min_material_seen, o.body.material)
        if t >= CORRUPT_TICK and o.body.material < DECISION_ALLOWANCE:
            allowance_breached += 1
        if t >= CORRUPT_TICK:
            mat_min_post_corrupt = min(mat_min_post_corrupt, o.body.material)
        if gate0_dead_tick is None and not (o.body.boundary[GATE_LINKS[0][0]] > 0):
            gate0_dead_tick = t
        if gate1_dead_tick is None and not (o.body.boundary[GATE_LINKS[1][0]] > 0):
            gate1_dead_tick = t
        if first_gate_dead is None and gate0_dead_tick is not None and gate1_dead_tick is not None:
            first_gate_dead = t
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
                n_moves=len(mts), schedule=[list(s) for s in schedule],
                ticks=TICKS, completed=total['active'] == TICKS, first_dead=first_dead,
                fw_at_corrupt=fw_at_corrupt, recovery_tick=recovery_tick,
                fw_by_move={str(k): v for k, v in fw_by_move.items()},
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
                B_discard=int(total['B_discard']), external_B=int(total['external_B']),
                particle_export=int(total['particle_export']), B_expiry=int(total['B_expiry']),
                first_W_empty=first_W_empty, first_C_empty=first_C_empty,
                mat_at_corrupt=mat_at_corrupt, mat_min_post_corrupt=mat_min_post_corrupt,
                min_material_seen=min_material_seen, allowance_breached=allowance_breached,
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                streak_writes=int(total['streak_writes']),
                action2_writes=cement['action2_writes'],
                action2_cementing=cement['action2_cementing'],
                admission=dict(ch0_attempted=admission['ch0_attempted'],
                               ch0_admitted=admission['ch0_admitted'],
                               ch1_attempted=admission['ch1_attempted'],
                               ch1_admitted=admission['ch1_admitted']),
                admission_events=admission['events'],
                gate0_dead_tick=gate0_dead_tick, gate1_dead_tick=gate1_dead_tick,
                first_gate_dead=first_gate_dead,
                budget_trace=budget_trace,
                state_hash=o.digest()), o, trace


def _arm_params(arm):
    """(admit, no_B, retention_rescue, rescue_B, permeant, puncture_links, puncture_tick)."""
    admit = ADMIT_FN[GATE[arm]]
    no_B = arm in NO_B_ARMS
    retention_rescue = arm in ('no_B_retention', 'no_B_retention_ref')
    rescue_B = arm == 'B_rescue'
    permeant = arm == 'permeant'
    if arm in ('puncture', 'rival_puncture', 'puncture_non_gate'):
        links = NONGATE_PUNCTURE_LINKS if arm == 'puncture_non_gate' else PUNCTURE_LINKS
        tick = PUNCTURE_TICK
    elif arm in ('puncture_simult', 'rival_puncture_simult'):
        links = PUNCTURE_LINKS
        tick = PUNCTURE_TICK_SIMULT
    else:
        links = None
        tick = None
    return admit, no_B, retention_rescue, rescue_B, permeant, links, tick


def run(seed, history, arm):
    corrupt, schedule = CONDITIONS[CHALLENGE[arm]]
    admit, no_B, retention_rescue, rescue_B, permeant, links, tick = _arm_params(arm)
    row, o, _ = _run_core(seed, history, corrupt, schedule, admit, no_B, links, tick,
                          retention_rescue=retention_rescue, rescue_B=rescue_B,
                          permeant=permeant, record_trace=False)
    row['arm'] = arm
    row['challenge'] = CHALLENGE[arm]
    row['gate'] = GATE[arm]
    return row


# ---------------- observer-discard on the integrated candidate (the keep arm) ----------------
def _mid_streak_tick(row, key=1, before_value=2, since=MOVE_TICK):
    for (t, k, before, after, dropped) in row['streak_events']:
        if k == key and before == before_value and not dropped and t >= since:
            return t
    return None


def observer_discard_keep(seed, history):
    """Per-tick observer-discard on the KEEP arm (the integrated candidate).

    At a mid-streak tick the succession observer and the alloc (host-side streak dict) are
    replaced with fresh objects; the trajectory must stay byte-identical — state sufficiency
    is a property of the maintained substrate, and the gate adds no host state (ADMIT reads
    organism state only).
    """
    corrupt, schedule = CONDITIONS['simult']
    admit, no_B, retention_rescue, rescue_B, permeant, links, tick = _arm_params('keep')
    kw = dict(admit=admit, no_B=no_B, retention_rescue=retention_rescue, rescue_B=rescue_B,
              permeant=permeant, puncture_links=links, puncture_tick=tick)
    base, base_o, base_trace = _run_core(seed, history, corrupt, schedule,
                                         record_trace=True, **kw)
    swap_tick = _mid_streak_tick(base, key=1, before_value=2)
    if swap_tick is None:
        return dict(seed=seed, history=history, arm='keep', status='no_mid_streak',
                    streak_events=base['streak_events'])
    swapped, swapped_o, swapped_trace = _run_core(seed, history, corrupt, schedule,
                                                  record_trace=True, swap_at=swap_tick, **kw)
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
    return dict(seed=seed, history=history, arm='keep', swap_tick=swap_tick, streak_at_swap=2,
                swap_applied=swapped['swap_applied'],
                per_tick_identical=per_tick_identical, n_equal=n_equal, n_ticks=len(base_trace),
                first_div=first_div, terminal_identical=base['state_hash'] == swapped['state_hash'],
                base_hash=base['state_hash'], swapped_hash=swapped['state_hash'])


# ---------------- the single-change license (G1): keep == AC105 persistent_budget -------------
def arm_identity(seed, history):
    keep = run(seed, history, 'keep')['state_hash']
    ac105_base = ac105.run(seed, history, 'persistent_budget', 'simult')['state_hash']
    return dict(keep_is_ac105=keep == ac105_base, keep_hash=keep, ac105_hash=ac105_base)


# ---------------- gates (recomputed from rows, no simulation) ----------------
def _alive_admission(row, channel, lo):
    first_dead = row['first_dead']
    end = first_dead if first_dead is not None else TICKS
    lo = lo if lo is not None else 0
    attempted = admitted = 0
    for (t, ch, adm) in row['admission_events']:
        if ch == channel and lo <= t < end:
            attempted += 1
            admitted += adm
    return attempted, admitted


def gates_ac115(rows, seeds):
    by = {}
    for r in rows:
        by[(r['seed'], r['history'], r['arm'])] = r
    n_ind = len(seeds) * 2
    detail = {}

    def all_ind(pred, arm):
        ok = True
        bad = []
        for seed in seeds:
            for history in (0, 1):
                r = by[(seed, history, arm)]
                if not pred(r):
                    ok = False
                    bad.append((seed, history))
        return ok, bad

    # G1 -- single-change license: keep/rival/reference byte-identical to each other AND to
    # AC105 persistent_budget; non-vacuous (corruption applied + succession recorded).
    ident = {}
    for seed in seeds:
        for history in (0, 1):
            ident[f'{seed}/{history}'] = arm_identity(seed, history)
    keep = by[(seeds[0], 0, 'keep')]
    reference = by[(seeds[0], 0, 'reference')]
    rival = by[(seeds[0], 0, 'rival')]
    g1_same = all(
        by[(s, h, 'keep')]['state_hash'] == by[(s, h, 'reference')]['state_hash']
        == by[(s, h, 'rival')]['state_hash'] == ident[f'{s}/{h}']['ac105_hash']
        for s in seeds for h in (0, 1))
    g1_nonvacuous = all(
        by[(s, h, 'keep')]['fw_at_corrupt'] == CORRUPT_BITS
        and by[(s, h, 'keep')]['successions'] >= 1
        and by[(s, h, 'keep')]['flipped_still_wrong'] == 0
        for s in seeds for h in (0, 1))
    g1 = g1_same and g1_nonvacuous

    # G2 -- D1 link-specific admission: puncture (site) ch0 alive-window admission == 0 (attempted
    # > 0), rival_puncture (count) ch0 alive-window admission > 0 (window [512, first_dead]).
    g2 = True
    g2_bad = []
    for s in seeds:
        for h in (0, 1):
            p = by[(s, h, 'puncture')]
            rp = by[(s, h, 'rival_puncture')]
            p_att, p_adm = _alive_admission(p, 0, PUNCTURE_TICK)
            rp_att, rp_adm = _alive_admission(rp, 0, PUNCTURE_TICK)
            if not (p_att > 0 and p_adm == 0 and rp_adm > 0):
                g2 = False
                g2_bad.append((s, h, p_att, p_adm, rp_att, rp_adm))
    detail['g2'] = g2_bad

    # G3 -- D2 local admission: puncture_non_gate admits > 0 on BOTH channels post-puncture.
    g3 = True
    g3_bad = []
    for s in seeds:
        for h in (0, 1):
            r = by[(s, h, 'puncture_non_gate')]
            c0_att, c0_adm = _alive_admission(r, 0, PUNCTURE_TICK)
            c1_att, c1_adm = _alive_admission(r, 1, PUNCTURE_TICK)
            if not (c0_adm > 0 and c1_adm > 0):
                g3 = False
                g3_bad.append((s, h, c0_adm, c1_adm))
    detail['g3'] = g3_bad

    # G4 -- T2 boundary production supports entry: no_B (site) gate links dead + admission == 0 on
    # BOTH channels (per-channel alive window; non-vacuous on the material channel) and does NOT
    # complete; no_B_retention_ref (none) admits every contact on both channels and completes.
    g4 = True
    g4_bad = []
    for s in seeds:
        for h in (0, 1):
            nb = by[(s, h, 'no_B')]
            nr = by[(s, h, 'no_B_retention_ref')]
            nb0a, nb0d = _alive_admission(nb, 0, nb['gate0_dead_tick'])
            nb1a, nb1d = _alive_admission(nb, 1, nb['gate1_dead_tick'])
            nr0a, nr0d = _alive_admission(nr, 0, nr['gate0_dead_tick'])
            nr1a, nr1d = _alive_admission(nr, 1, nr['gate1_dead_tick'])
            ok = (nb['gate0_dead_tick'] is not None and nb['gate1_dead_tick'] is not None
                  and nb0d == 0 and nb1d == 0 and nb1a > 0 and not nb['completed']
                  and nr0d == nr0a and nr1d == nr1a and nr1a > 0 and nr['completed'])
            if not ok:
                g4 = False
                g4_bad.append((s, h, (nb0a, nb0d), (nb1a, nb1d), nb['completed'],
                               (nr0a, nr0d), (nr1a, nr1d), nr['completed']))
    detail['g4'] = g4_bad

    # G5 -- retention vs admission separated: no_B_retention (site) gate dead + admission == 0 on
    # both channels and does NOT complete; no_B_retention_ref admits and completes. The retention
    # rescue (kernel flag) restores retention but NOT admission (gate links still dead).
    g5 = True
    g5_bad = []
    for s in seeds:
        for h in (0, 1):
            nbr = by[(s, h, 'no_B_retention')]
            nr = by[(s, h, 'no_B_retention_ref')]
            nbr0a, nbr0d = _alive_admission(nbr, 0, nbr['gate0_dead_tick'])
            nbr1a, nbr1d = _alive_admission(nbr, 1, nbr['gate1_dead_tick'])
            nr0a, nr0d = _alive_admission(nr, 0, nr['gate0_dead_tick'])
            nr1a, nr1d = _alive_admission(nr, 1, nr['gate1_dead_tick'])
            ok = (nbr['gate0_dead_tick'] is not None and nbr['gate1_dead_tick'] is not None
                  and nbr0d == 0 and nbr1d == 0 and nbr1a > 0 and not nbr['completed']
                  and nr0d == nr0a and nr1d == nr1a and nr1a > 0 and nr['completed'])
            if not ok:
                g5 = False
                g5_bad.append((s, h, (nbr0a, nbr0d), (nbr1a, nbr1d), nbr['completed'],
                               (nr0a, nr0d), (nr1a, nr1d), nr['completed']))
    detail['g5'] = g5_bad

    # G6 -- endogenous renewal vs external restoration.
    g6 = True
    g6_bad = []
    for s in seeds:
        for h in (0, 1):
            k = by[(s, h, 'keep')]
            br = by[(s, h, 'B_rescue')]
            if not (k['B_births'] > 0 and k['external_B'] == 0 and k['particle_export'] == 0
                    and br['external_B'] > 0 and br['B_births'] == 0 and br['completed']):
                g6 = False
                g6_bad.append((s, h))
    detail['g6'] = g6_bad

    # G7 -- composition under stress: rival_puncture_simult reconstructs + holds desc + completes;
    # puncture_simult ch0 admission == 0 post-puncture under corruption+move.
    g7 = True
    g7_bad = []
    for s in seeds:
        for h in (0, 1):
            rps = by[(s, h, 'rival_puncture_simult')]
            ps = by[(s, h, 'puncture_simult')]
            ps_att, ps_adm = _alive_admission(ps, 0, PUNCTURE_TICK_SIMULT)
            if not (rps['fw_at_corrupt'] == CORRUPT_BITS and rps['flipped_still_wrong'] == 0
                    and rps['description_correct'] == 130 and rps['successions'] >= 1
                    and rps['completed']
                    and ps_att > 0 and ps_adm == 0):
                g7 = False
                g7_bad.append((s, h, ps_att, ps_adm))
    detail['g7'] = g7_bad

    # G8 -- completeness + determinism (sampled exact rerun).
    first = rows[0]
    rerun = run(first['seed'], first['history'], first['arm'])
    g8 = (len(rows) == n_ind * len(ARMS)
          and rerun['state_hash'] == first['state_hash'])

    return {
        'G1_single_change_license': g1,
        'G2_D1_link_specific_admission': g2,
        'G3_D2_local_admission': g3,
        'G4_T2_boundary_supports_entry': g4,
        'G5_retention_vs_admission': g5,
        'G6_endogenous_vs_external': g6,
        'G7_composition_under_stress': g7,
        'G8_completeness_determinism': g8,
        'detail': detail,
        'arm_identity': ident,
    }


# ---------------- collectors ----------------
def collect(root, seeds):
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest()
              for n in SOURCES if Path(n).exists()}
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
                (r['arm'], r['challenge'], r['history'], r['completed'], r['first_dead'],
                 r['fw_at_corrupt'], r['recovery_tick'], r['flipped_still_wrong'],
                 r['successions'], r['description_correct'], r['B_births'],
                 r['external_B'], r['particle_export'], r['gate0_dead_tick'],
                 r['admission'], r['relinquishments'], r['W'], r['C'])
                for r in rows[-2 * len(ARMS):]]), default=str), flush=True)
    obs = {}
    for seed in seeds:
        for history in (0, 1):
            obs[f'{seed}/{history}'] = observer_discard_keep(seed, history)
    g = gates_ac115(rows, seeds)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), arms=list(ARMS), hashes=hashes, gates=g, rows=rows,
             observer_discard_keep=obs), indent=2, default=str))
    print(json.dumps(dict(rows=len(rows), gates={k: v for k, v in g.items() if not k.startswith('detail') and k != 'arm_identity'}, dir=root), indent=2, default=str))
    return rows, g, obs


def main():
    if '--engineering' in sys.argv:
        collect('ac115_engineering_v1', ENGINEERING)
        return
    collect('ac115_results_v1', FINAL_SEEDS)


if __name__ == '__main__':
    main()
