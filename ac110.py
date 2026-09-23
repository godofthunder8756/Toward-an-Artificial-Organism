"""AC110 (C3): does maintaining an ALREADY-ACQUIRED, correct representation depend on ongoing
repair, distinct from re-acquiring the answer?

Parent (C2, t_a5ef427b): C2 established a task where the current observation is IDENTICAL across
the two AC107/108 causes while their histories differ -- the occluded-used_held gate (Bernoulli(q)
occludes the used_held bit on channel-1 contacts), so a maintained (persistent) cause-estimate is
load-bearing. C1 (AC109) measured the stored estimate INERT in the un-gated world (the discriminator
is a pure function of the current triple); C2 made history load-bearing.

C3 asks the NEXT question: after the estimate is ACQUIRED (correctly written), does its ongoing
CORRECTNESS depend on paid REPAIR of its vulnerable storage, separable from RE-ACQUIRING via fresh
diagnostics?

The representation under test is the AC107 one-bit cause estimate e in {E_world=1, E_machinery=0},
stored in the dead-rule action bit (traces[0, bel_off], 7 replicas, acquired value 1 = E_world),
damaged by the sticky-SET program stream, read by majority (>=4 of 7), and repaired by the paid
bank-0 majority-restore (action 2). It is EXCLUDED from reg_from_active (reconstruction), so action
2 is its ONLY repair path. Its reacquisition path is bel_write -- the discriminator reads the
current (bound, used_held, productive) triple and writes the conclusion.

The TWO maintenance paths of the estimate, kept apart:
  - REPAIR        = action 2's bank-0 majority-restore, which restores each bit of bank 0 (estimate
                    included) to its 7-replica majority. It preserves the STORED value against
                    minority damage. It carries no diagnostic input.
  - REACQUISITION = bel_write, which reads the current observation and (re)writes the conclusion.
                    It re-derives the answer from fresh diagnostics.

The C3 contrast (both arms keep reacquisition, only repair differs):
  - `maintained` : full repair -- action 2 repairs the estimate's storage (minority damage restored).
  - `no_repair`  : action 2's bank-0 majority-restore EXCLUDES the estimate bit (selective cut of
                    the representation's repair), while bel_write (reacquisition) stays intact.

Declared damage on the representation: the FROZEN ambient sticky-SET stream (1e-4 per replica per
tick, `b.traces[0,:126]|=core_flips`), which reaches the estimate by construction (it lives in bank
0). No elevated rate is needed: the ambient rate already flips the estimate's 7 replicas to a
majority over the post-window horizon, and the repair cut is exercised without degrading the whole
organism. (An elevated BEL_DAMAGE knob is retained as an engineering diagnostic only; the frozen
study runs at BEL_DAMAGE=0.0, i.e. ambient.)

The two causes (unchanged from AC107/108):
  - E_world (`move`): at t=8192 the channel-1 mapping flips; the route-1 entry is intact but STALE.
    Correct response: relinquish (e should read 1 = E_world).
  - E_machinery (`cut`): at t=8192 the read of route-1 is suppressed for [8192, 8288); the entry is
    intact and correct; contacts fall back to blind (success 1/4). Correct response: hold (e should
    read 0 = E_machinery).

The repair is load-bearing ONLY in the cut: the estimate's acquired value is 1 (E_world), and the
cut's correct value is 0 (E_machinery), so sticky-SET (0->1) DEGRADES the estimate toward the wrong
value exactly where the discriminator writes 0. In the move the estimate's value is 1 and sticky-SET
is a no-op, so the intervention is inert there (the clean-control condition).

Discipline: engineering first (verify the clean control, measure the endpoints), then a hashed
protocol, then disjoint finals. Negative findings are preserved; no gate is moved after seeing the
result.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import inspect
import numpy as np
import ac107
import ac106
import ac12
import ac95
import ac96
import ac100
import ac4
import ac9
import ac71
import ac99_d2
import ac5_program as prog

TICKS = ac107.TICKS
DEV = ac107.DEV
STREAK_N = ac107.STREAK_N
MOVE_TICK = ac107.MOVE_TICK
CUT_TICK = ac107.CUT_TICK
PORTS = ac107.PORTS
WINDOW = ac107.WINDOW
HOLD_N = ac107.HOLD_N
BEL_WORD_BIT = ac107.BEL_WORD_BIT

# ---- C3 declared world constants ----
Q = 0.5                       # Bernoulli occlusion probability of used_held on channel-1 contacts
BEL_DAMAGE = 0.0              # frozen study: ambient only (the frozen 1e-4 sticky-SET stream that
                              # already reaches the estimate). The elevated-damage knob below is an
                              # engineering diagnostic, NOT part of the frozen study.
BEL_DAMAGE_OFF = 1e-4         # the ambient rate the estimate already faces (part of the program stream)

ARMS = ('maintained', 'no_repair')
CONDITIONS = ('no_cause', 'move', 'cut')

ENGINEERING = list(range(8))
FINAL_SEEDS = [6200, 6201, 6202, 6203, 6204, 6205, 6206, 6207]   # fresh, disjoint, pre-freeze

SOURCES = ['ac110.py', 'ac107.py', 'ac106.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py',
           'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC110_PROTOCOL_v1.md']


# ---------------- the estimate primitives (re-exported from ac107) ----------------
bel_offset = ac107.bel_offset
bel_read = ac107.bel_read
bel_minority = ac107.bel_minority
bel_write = ac107.bel_write


# ---------------- the C2 gate: occlude used_held on Bernoulli(q) channel-1 contacts ----------------
# gate_used is installed as a closure in the step namespace (see build_step); the value 2 = 'occluded'
# is the declared third observation value. The gate is applied uniformly to every arm, i.i.d. per
# contact, NOT synchronized with the cause onset, and reveals no cause label (it withholds a bit).


# ---------------- the gated estimator (3-valued used_held discriminator) ----------------
class GatedEstimator(ac107.Estimator):
    """AC107.Estimator with the C2 three-valued used_held observation {blind=0, held=1, occluded=2}.

    The discriminator fires only on OPEN contacts (used=0 or 1); at an occluded contact (used=2) it
    matches no rule and falls through to the STORED e. The consumption reads the stored e everywhere,
    exactly as ac107 -- this is the C2 §8 "candidate needs no code change to bridge the gap" property,
    realised as a three-valued discriminator (the ac107 2-valued `bool(used_held)` cannot express
    'occluded' without firing one of the two unproductive rules).
    """

    def __init__(self, seed, history, bel_off=None, estimate=True, proactive=True, scramble=False):
        super().__init__(seed, history, bel_off=bel_off, estimate=estimate,
                         proactive=proactive, scramble=scramble)
        self.occluded_unproductive = 0   # occluded unproductive channel-1 contacts (observational)
        self.occluded_reads_1 = 0        # of those, contacts where the stored e read 1 (E_world)

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if key != 1:
            super().outcome(o, key, e)
            return
        bound = (o.memory.read(1) is not None)
        used = used_held                  # 0 = blind, 1 = held, 2 = occluded
        productive = e['productive'] > 0
        cur = ac99_d2.gray_streak_read(o, 1, self.streak_offs)
        # ---- the K4 discriminator, three-valued ----
        if bound and used == 0:
            # blind while bound -> E_machinery (cut signature); fires on every open in-window contact
            self._bel_write(o, e, 0)
            self.bel_events.append((self.now, 'machinery_cut', 0))
        elif used == 1 and not productive:
            # held entry failed -> E_world (F1)
            self._bel_write(o, e, 1)
            self.bel_events.append((self.now, 'world_held_fail', 1))
        elif not bound and productive:
            # blind re-bind after a drop -> E_world (re-acquisition)
            self._bel_write(o, e, 1)
            self.bel_events.append((self.now, 'world_rebind', 1))
        # used == 2 (occluded): no rule fires; the stored e carries the decision (C2's overlap).
        if used == 2 and not productive:
            self.occluded_unproductive += 1
            if self._bel(o) != 0:
                self.occluded_reads_1 += 1
        # ---- the two consumptions (identical to ac107, reading the STORED e) ----
        if productive:
            self._restore(o, e, key)
            ac99_d2.gray_streak_write(o, e, key, 0, self.streak_offs)
            if self._bel(o) == 0 and self.proactive:
                self._proactive_renew(o, e, key)
            self.streak_events.append((self.now, key, cur, 0, 0))
            return
        if self._bel(o) == 0:
            # E_machinery: withhold relinquishment + proactive renewal
            if self.proactive:
                self._proactive_renew(o, e, key)
            self.streak_events.append((self.now, key, cur,
                                       ac99_d2.gray_streak_read(o, 1, self.streak_offs), 0))
            return
        # E_world: the frozen streak relinquishment
        dropped = 0
        if cur + 1 >= STREAK_N:
            n_before = len(self.log['dropped'])
            self._drop(o, e, key)
            dropped = 1 if len(self.log['dropped']) > n_before else 0
        else:
            ac99_d2.gray_streak_write(o, e, key, cur + 1, self.streak_offs)
        self.streak_events.append((self.now, key, cur,
                                   ac99_d2.gray_streak_read(o, 1, self.streak_offs), dropped))


# ---------------- the selective repair cut (source surgery on ac4.react) ----------------
REACT_SRC = ac12.REACT_SRC
REACT_REPAIR = ("        sites=np.argwhere(b.traces[bank]!=majority[:,None])\n"
                "        cap=0 if arm=='no_policy_write' and bank<2 else int(a[4*bank:4*bank+4].sum())*8")
REACT_REPAIR_SKIP = ("        sites=np.argwhere(b.traces[bank]!=majority[:,None])\n"
                     "        if bank==0 and skip_est:\n"
                     "            sites=sites[sites[:,0]!=bel_off]\n"
                     "        cap=0 if arm=='no_policy_write' and bank<2 else int(a[4*bank:4*bank+4].sum())*8")


def react_skip_estimate(skip_est, bel_off):
    """ac4.react with the estimate bit EXCLUDED from action-2's bank-0 majority-restore.

    skip_est=False returns ac4.react itself (the maintained arm -- byte-identical to frozen).
    skip_est=True returns a react whose action-2 path skips bel_off, cutting the estimate's ONLY
    repair while leaving every other bit's majority-restore untouched. The estimate is still written
    by bel_write (reacquisition) and still damaged by the sticky stream; only its REPAIR is cut.
    """
    if not skip_est:
        return ac4.react
    src = REACT_SRC
    assert src.count(REACT_REPAIR) == 1, 'ac4.react source changed (repair block)'
    src = src.replace(REACT_REPAIR, REACT_REPAIR_SKIP)
    ns = dict(vars(ac4), skip_est=skip_est, bel_off=bel_off)
    fns = {}
    exec(compile(src, 'ac110_react', 'exec'), ns, fns)
    return fns['react']


# ---------------- the build (ac107.build_step + the gate + the selective repair cut) ----------------
def build_step(alloc, succ, reg_offs, cfg, cut_obj, bel_off=None, skip_est=False,
               gate_rng=None, q=Q):
    base, cut = ac71.arm_parts(cfg['ac_arm'])
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['maintain'] = ac95.maintain
    ns['succ'] = succ
    ns['reg_offs'] = reg_offs
    ns['cfg'] = cfg
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE,
                      ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e,gate_used(selected,action))")
    ns['alloc'] = alloc
    # ---- the C2 gate (closure over the declared gate RNG + q) ----
    def gate_used(selected, action):
        used = int(selected is not None)
        if action == 1 and gate_rng is not None and gate_rng.random() < q:
            return 2
        return used
    ns['gate_used'] = gate_used
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    assert src.count(ac107.READ_LINE) == 1
    src = src.replace(ac107.READ_LINE, ac107.READ_LINE_NEW)
    ns['cut_obj'] = cut_obj
    assert src.count(ac95.ACTION_LINE) == 1
    src = src.replace(ac95.ACTION_LINE, "        maintain(o,e,succ,reg_offs,cfg,now)\n" + ac95.ACTION_LINE)
    assert src.count(ac95.BALANCE_LINE) == 1
    src = src.replace(ac95.BALANCE_LINE,
                      "    e['writes']+=e.get('reg_writes',0)+e.get('succ_writes',0)+e.get('ctrl_writes',0)\n"
                      + ac95.BALANCE_LINE)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = react_skip_estimate(skip_est, bel_off)
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    ns['now'] = 0
    fns = {}
    exec(compile(src, 'ac110_step', 'exec'), ns, fns)
    return fns['step']


# ---------------- the run core ----------------
def _condition_params(condition):
    if condition == 'move':
        return [(MOVE_TICK, 'flip')], None, 0, 0
    if condition == 'cut':
        return [], 1, CUT_TICK, CUT_TICK + WINDOW
    return [], None, 0, 0          # no_cause


def _make_alloc(arm, seed, history, bel_off):
    if arm in ('maintained', 'no_repair'):
        return GatedEstimator(seed, history, bel_off=bel_off, estimate=True,
                              proactive=True, scramble=False)
    raise ValueError(arm)


def _true_cause(condition):
    if condition == 'cut':
        return 0                  # E_machinery
    if condition == 'move':
        return 1                  # E_world
    return None


def _run_core(seed, history, arm, condition, record_trace=False, ports=PORTS,
              q=Q, bel_damage=BEL_DAMAGE, swap_at=None):
    ac12.PORTS = ports; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    bel_off = bel_offset(o)
    skip_est = (arm == 'no_repair')
    alloc = _make_alloc(arm, seed, history, bel_off)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    streak_offs = ac96.streak_offsets(o)
    alloc.streak_offs = streak_offs
    reg_offs = ac95.resolve_offsets(o)
    build_offs = reg_offs + streak_offs + [bel_off]
    encoded = ac95.description_bits(priority)
    o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
    cfg = dict(ac95.ARM_PARTS['gated'])
    cfg['reserve'] = False
    succ = ac95.Succession('real', encoded)
    schedule, cut_key, cut_start, cut_end = _condition_params(condition)
    cut_obj = ac106.ReadCut(cut_key, cut_start, cut_end)
    gate_rng = np.random.default_rng([seed, 1809])
    bel_rng = np.random.default_rng([seed, 1709])
    step = build_step(alloc, succ, build_offs, cfg, cut_obj, bel_off=bel_off,
                      skip_est=skip_est, gate_rng=gate_rng, q=q)
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
    bel_minority_at_cut_end = None
    bel_ones_ever = 0
    bel_min_ever = 0
    bel_wrong_ever = 0
    bel_wrong_in_window = 0
    first_wrong_read = None
    true_cause = _true_cause(condition)
    swap_applied = False
    for t in range(TICKS):
        alloc.now = t
        cut_obj.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = _make_alloc(arm, seed, history, bel_off)
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
        coin = bool(rng.random() < .5) if ports == 2 else int(rng.integers(0, ports))
        # ---- declared damage on the representation (elevated sticky-SET, before the step) ----
        if bel_damage > 0:
            bel_flips = (bel_rng.random(7) < bel_damage).astype(np.uint8)
            o.body.traces[0, bel_off] |= bel_flips
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
        # ---- estimate degradation tracking ----
        ones = int(o.body.traces[0, bel_off].sum())
        bel_ones_ever = max(bel_ones_ever, ones)
        bel_min_ever = max(bel_min_ever, min(ones, 7 - ones))
        if true_cause is not None and t >= CUT_TICK and bel_read(o, bel_off) != true_cause:
            bel_wrong_ever += 1
            if first_wrong_read is None:
                first_wrong_read = t
        if true_cause is not None and CUT_TICK <= t < CUT_TICK + WINDOW \
                and bel_read(o, bel_off) != true_cause:
            bel_wrong_in_window += 1
        if condition == 'cut':
            if t == CUT_TICK + WINDOW - 1:
                bel_at_cut_end = bel_read(o, bel_off)
                bel_ones_at_cut_end = int(o.body.traces[0, bel_off].sum())
                bel_minority_at_cut_end = bel_minority(o, bel_off)
        if record_trace:
            trace.append((t, o.digest()))
        if first_dead is None and o.body.dead:
            first_dead = t
    bel_at_horizon = bel_read(o, bel_off)
    inv = ac4.inventory(o.body)
    return dict(seed=seed, history=history, arm=arm, condition=condition,
                ticks=TICKS, completed=total['active'] == TICKS, first_dead=first_dead,
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                drop_ticks=drop_ticks,
                restore_ticks=restore_ticks,
                streak_final={0: ac99_d2.gray_streak_read(o, 0, streak_offs),
                              1: ac99_d2.gray_streak_read(o, 1, streak_offs)},
                streak_events=getattr(alloc, 'streak_events', []),
                reacquire_ticks=reacquire_ticks,
                bel=bel_read(o, bel_off),
                bel_at_horizon=bel_at_horizon,
                bel_at_cut_end=bel_at_cut_end,
                bel_ones_at_cut_end=bel_ones_at_cut_end,
                bel_minority_at_cut_end=bel_minority_at_cut_end,
                bel_minority_end=bel_minority(o, bel_off),
                bel_ones_ever=bel_ones_ever,
                bel_min_ever=bel_min_ever,
                bel_wrong_ever=bel_wrong_ever,
                bel_wrong_in_window=bel_wrong_in_window,
                first_wrong_read=first_wrong_read,
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


def run(seed, history, arm, condition, ports=PORTS, record_trace=False, q=Q,
        bel_damage=BEL_DAMAGE):
    row, o, _ = _run_core(seed, history, arm, condition, record_trace=record_trace,
                          ports=ports, q=q, bel_damage=bel_damage)
    return row


# ---------------- clean control: no_repair == maintained in no_cause/move (e is 1, damage inert) ----
# This is the ONLY byte-identity gate. There is deliberately NO "no_repair == maintained in the cut"
# expectation: in the cut the estimate is written to 0 (E_machinery) and the ambient sticky-SET stream
# degrades it toward 1, so the repair cut IS exercised post-window (see AC110_PROTOCOL_v1.md).
def clean_control_identity(seed, history, condition):
    m = run(seed, history, 'maintained', condition)
    n = run(seed, history, 'no_repair', condition)
    return m['state_hash'] == n['state_hash']


# ---------------- collectors ----------------
def preflight(protocol='AC110_PROTOCOL_v1.md'):
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


def collect(root, seeds, conditions=None, do_preflight=False, q=Q, bel_damage=BEL_DAMAGE,
            finals=False):
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
                        r = run(seed, history, arm, cond, q=q, bel_damage=bel_damage)
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['bel_at_cut_end'], r['bel_ones_at_cut_end'],
                 r['bel_wrong_ever'], r['occluded_reads_1'], r['bel_writes'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    clean = {f'{s}/{h}/{c}': clean_control_identity(s, h, c)
             for s in seeds for h in (0, 1) for c in ('no_cause', 'move')}
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), PORTS=PORTS,
             Q=q, BEL_DAMAGE=bel_damage, WINDOW=WINDOW, rows=rows,
             clean_control=clean,
             hashes=hashes if do_preflight else None),
        indent=2, default=str))
    print(json.dumps(dict(clean_control=clean), indent=2, default=str))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac110_engineering_v1', ENGINEERING)
        return
    if '--smoke' in sys.argv:
        collect('ac110_smoke_v1', [0, 1, 2])
        return
    if '--finals' in sys.argv:
        collect('ac110_results_v1', FINAL_SEEDS, do_preflight=True, finals=True)
        return
    print('AC110: --engineering (seeds 0-7), --smoke (0-2), or --finals (6200-6207).')


if __name__ == '__main__':
    main()
