"""AC106: does an internally maintained cause-estimate carry causal role?

Parent (C1, t_aa472bae): MAINTAINED_BELIEF_TASK_v1.md. The task is a two-cause,
partially-observed world in which the SAME immediate failure -- a contact on channel 1
fails to yield income -- arises from two distinct causes that no single observation bit
separates:

  E_world     (condition `move`): the channel-1 mapping flips at tick T (post-DEV). The
              route-1 entry is intact but STALE; contacts fail forever until it is re-bound.
  E_machinery (condition `cut`):  the organism's READ of the route-1 entry is suppressed for
              a declared window [T, T+WINDOW), so contacts fall back to blind search. The
              entry is intact and correct; contacts fail at the blind rate during the window
              and resume without re-binding once the read is restored.

The estimate under test is a ONE-BIT second-order state e in {E_world, E_machinery}, stored
in a dead-rule action bit (14*dead_rule_index + 10, the AC12/AC96 free-bit treatment): damaged
by the ambient sticky-SET program stream, read by majority, repaired by the paid bank-0
majority-restore (action 2), excluded from reg_from_active. The acquired value is 1 (= E_world,
the AC12 inverted-semantics pattern), so the acquired organism is byte-identical to the frozen
one and the "surprise" state e=0 (E_machinery) is what must be actively written and maintained.

Its update rule uses only the organism's own contact outcomes:

  - on a productive contact-1 that follows a failure (productivity resumed WITHOUT re-binding)
    => e = E_machinery (the failure was a transient access outage);
  - on relinquishment (a stale route was dropped) => e = E_world.

Its two consumptions (flexible use, the R3/C1 requirement):

  - e = E_world     => relinquish after HOLD_N consecutive failures (the stale route is dropped);
  - e = E_machinery => withhold relinquishment INDEFINITELY and direct spend to PROACTIVE
    renewal of the still-valid entry through the outage (active maintenance, ahead of the
    renewal-urgent observation bit).

The matched rivals: r2 = the frozen Gray streak (relinquish after STREAK_N=6, the natural
history-based rival); r4 = a longer-threshold counter (relinquish after HOLD_N, NO proactive
renewal -- the sharpest falsification, a raw counter with a bigger threshold); r1 = reactive
(relinquish on the FIRST failure); r3 = state-blind duty cycle; scramble = the candidate with
the estimate bit forced to E_world (the causal-role control, P4).

World: the AC100 Gray-streak architecture, corrupt=False, TICKS=16384, DEV=512, PORTS=4
(blind fallback 1/4), mapping over {0,1}. The read-cut is the same kind of
machinery-suppression the frozen arc already sanctions (ac9.blocked / AC91-92 W-cut): it
changes only which port the contact uses, so the ac4.balance identities hold unchanged and,
with the cut disabled (WINDOW=0), the contact is byte-identical to the frozen one.

Discipline: engineering first (seeds 0-7, economy + discriminability measured, not assumed),
then a hashed protocol, then disjoint final seeds. A negative result -- the estimate adds
nothing over the longer-threshold counter -- is a finding and completes the card honestly.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac99_d2
import ac96
import ac95
import ac12
import ac4
import ac71
import ac9
import ac100
import ac5_program as prog
from ac1 import decode

TICKS = ac95.TICKS                  # 16384
DEV = ac71.DEV                      # 512
STREAK_N = ac12.STREAK_N            # 6
MOVE_TICK = ac95.MOVE_TICK          # 8192
CUT_TICK = MOVE_TICK                # the two causes land at the SAME tick (identical failure)

# ---- declared world constants ----
PORTS = 4                           # blind fallback is uniform over {0,1,2,3}; mapping over {0,1}
WINDOW = 96                         # read-cut window (ticks); longer than the entry life (64)
HOLD_N = STREAK_N                   # the candidate's E_world threshold IS the frozen streak threshold
                                    # (the 3-bit Gray streak saturates at 7, so any larger threshold is
                                    # unreachable; e=E_machinery instead switches to an infinite threshold)
DUTY_PERIOD = 12                    # the state-blind duty rival's fixed relinquish period
BEL_WORD_BIT = 10                   # action bit 0 of the dead rule (acquired value 1)

ARMS = ('candidate', 'r2', 'r4', 'r1', 'r3', 'scramble')
CONDITIONS = ('no_cause', 'move', 'cut')

SOURCES = ['ac106.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py', 'ac95.py', 'ac76.py',
           'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py',
           'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py',
           'ac1.py', 'AC106_PROTOCOL_v1.md']

UNSEEN = [5900, 5901, 5902, 5903, 5904, 5905, 5906, 5907]
FINAL_SEEDS = UNSEEN
ENGINEERING = list(range(8))


def bel_offset(o):
    """The estimate bit's offset: action bit 0 (word bit 10) of the dead rule, resolved once at
    acquisition (the AC12 rule). Acquired value 1 = E_world."""
    return 14 * ac12.dead_rule_index(o) + BEL_WORD_BIT


# ---------------- the estimate bit (vulnerable, paid-maintained) ----------------
def bel_read(o, bel_off):
    """Majority read (>= 4 of 7) of the estimate bit. 1 = E_world, 0 = E_machinery."""
    return int(o.body.traces[0, bel_off].sum() >= 4)


def bel_minority(o, bel_off):
    ones = int(o.body.traces[0, bel_off].sum())
    return min(ones, 7 - ones)


def bel_write(o, e, val, bel_off):
    """Atomic, W-gated paid write of the estimate bit to `val` (<= 7 replicas)."""
    b = o.body
    sites = np.argwhere(b.traces[0, bel_off] != val)
    n = len(sites)
    if n and n <= ac95._cap(b):
        b.traces[0, bel_off, sites[:, 0]] = val
        b.energy -= n
        b.material -= n
        e['spent_e'] += n
        e['spent_m'] += n
        e['writes'] += n
        e['bel_writes'] = e.get('bel_writes', 0) + n
        return n
    return 0


# ---------------- the read-cut (machinery suppression, mirror of ac9.blocked) ----------------
class ReadCut:
    """Suppress the organism's read of the route-1 entry during [start, end).

    Returns None for key==1 in the window (blind fallback), the frozen read otherwise.
    With end <= start (or key None) it is the identity -- byte-identical to the frozen world.
    """
    def __init__(self, key, start, end):
        self.key = key
        self.start = start
        self.end = end
        self.now = 0

    def read(self, memory, key):
        if self.key is not None and key == self.key and self.start <= self.now < self.end:
            return None
        return memory.read(key)


# ---------------- the allocators ----------------
class BeliefAlloc(ac99_d2.GrayAllocEraseReserve):
    """The candidate (and, via flags, the r4 / r1 / scramble rivals).

    estimate  : maintain and consult the estimate bit.
    threshold : relinquish after this many consecutive unproductive contacts when e == E_world.
    proactive : when e == E_machinery, direct a paid renewal of the route entry on every
                contact-1 (active maintenance through the outage, ahead of the renewal-urgent bit).
    scramble  : the estimate bit is READ as E_world (1) and never WRITTEN (causal-role control).
    """

    def __init__(self, seed, history, bel_off=None, estimate=True, threshold=HOLD_N,
                 proactive=True, scramble=False):
        super().__init__('allocate', seed, history, reserve=False)
        self.bel_off = bel_off
        self.estimate = estimate
        self.threshold = threshold
        self.proactive = proactive
        self.scramble = scramble
        self.bel_events = []   # (tick, kind, val) observational

    def _bel(self, o):
        """1 = E_world, 0 = E_machinery."""
        if self.scramble or not self.estimate:
            return 1
        return bel_read(o, self.bel_off)

    def _bel_write(self, o, e, val):
        if self.scramble or not self.estimate:
            return 0
        return bel_write(o, e, val, self.bel_off)

    def _proactive_renew(self, o, e, key):
        """Direct paid per-slot renewal of the route entry for `key`, bypassing the program's
        action selection (so it is not subject to the material-contact hijack during the outage)."""
        place = ac12.m12.slot_of_key(o.memory, key)
        if place is None:
            return 0
        r, s = place
        result = ac12.m12.renew_alloc(o.memory, o.body, r,
                                      int(ac4.available(o.body)[4 * (r + 1):4 * (r + 2)].sum()),
                                      [s == 0, s == 1])
        if result['writes']:
            ac9.memory_charge(e, result)
            e['proactive_writes'] = e.get('proactive_writes', 0) + result['writes']
        return result['writes']

    def outcome(self, o, key, e):
        if self.arm != 'allocate':
            return
        key = int(key)
        if key != 1:
            super().outcome(o, key, e)          # channel 0 is never moved/cut
            return
        cur = ac99_d2.gray_streak_read(o, key, self.streak_offs)
        if e['productive'] > 0:
            self._restore(o, e, key)
            ac99_d2.gray_streak_write(o, e, key, 0, self.streak_offs)
            if cur > 0 and self.now >= DEV:
                # productivity resumed after a failure, WITHOUT re-binding => transient cause
                # (gated on post-DEV: before DEV a failure is the ordinary acquisition process,
                # not a possible outage)
                self._bel_write(o, e, 0)
                self.bel_events.append((self.now, 'set_transient', 0))
            if self._bel(o) == 0 and self.proactive:
                self._proactive_renew(o, e, key)
            self.streak_events.append((self.now, key, cur, 0, 0))
            return
        # unproductive contact-1
        threshold = 10**9 if self._bel(o) == 0 else self.threshold
        dropped = 0
        if cur + 1 >= threshold:
            n_before = len(self.log['dropped'])
            self._drop(o, e, key)
            dropped = 1 if len(self.log['dropped']) > n_before else 0
        else:
            ac99_d2.gray_streak_write(o, e, key, cur + 1, self.streak_offs)
        if self._bel(o) == 0 and self.proactive and not dropped:
            self._proactive_renew(o, e, key)
        self.streak_events.append((self.now, key, cur,
                                   ac99_d2.gray_streak_read(o, key, self.streak_offs), dropped))

    def _drop(self, o, e, key):
        super()._drop(o, e, key)
        if key == 1:
            self._bel_write(o, e, 1)
            self.bel_events.append((self.now, 'reset_world', 1))


class DutyAlloc(ac99_d2.GrayAllocEraseReserve):
    """r3: a state-blind fixed duty cycle. Relinquishes key 1 every `period` contacts,
    regardless of productivity or cause (no attribution)."""

    def __init__(self, seed, history, period=DUTY_PERIOD):
        super().__init__('allocate', seed, history, reserve=False)
        self.period = period
        self.contact_count = 0

    def outcome(self, o, key, e):
        key = int(key)
        if key != 1:
            return
        self.contact_count += 1
        if self.contact_count >= self.period:
            self._drop(o, e, key)
            self.contact_count = 0
        self.streak_events.append((self.now, key, 0,
                                   ac99_d2.gray_streak_read(o, key, self.streak_offs),
                                   int(self.contact_count == 0)))


# ---------------- the build (ac95.build + the read-cut shim) ----------------
READ_LINE = "            selected=o.memory.read(action); port=int(coin) if selected is None else selected"
READ_LINE_NEW = "            selected=cut_obj.read(o.memory, action); port=int(coin) if selected is None else selected"


def build_step(alloc, succ, reg_offs, cfg, cut_obj):
    """ac95.build, plus the read-cut shim on the contact's read."""
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
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    assert src.count(READ_LINE) == 1
    src = src.replace(READ_LINE, READ_LINE_NEW)
    ns['cut_obj'] = cut_obj
    assert src.count(ac95.ACTION_LINE) == 1
    src = src.replace(ac95.ACTION_LINE, "        maintain(o,e,succ,reg_offs,cfg,now)\n" + ac95.ACTION_LINE)
    assert src.count(ac95.BALANCE_LINE) == 1
    src = src.replace(ac95.BALANCE_LINE,
                      "    e['writes']+=e.get('reg_writes',0)+e.get('succ_writes',0)+e.get('ctrl_writes',0)\n"
                      + ac95.BALANCE_LINE)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac12.react_world()
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    ns['now'] = 0
    fns = {}
    exec(compile(src, 'ac106_step', 'exec'), ns, fns)
    return fns['step']


# ---------------- the run core ----------------
def _condition_params(condition):
    """(schedule, cut_key, cut_start, cut_end) per condition."""
    if condition == 'move':
        return [(MOVE_TICK, 'flip')], None, 0, 0
    if condition == 'cut':
        return [], 1, CUT_TICK, CUT_TICK + WINDOW
    return [], None, 0, 0          # no_cause


def _make_alloc(arm, seed, history, bel_off):
    if arm == 'r2':
        return ac99_d2.GrayAllocEraseReserve('allocate', seed, history, reserve=False)
    if arm == 'candidate':
        return BeliefAlloc(seed, history, bel_off=bel_off, estimate=True, threshold=HOLD_N,
                           proactive=True, scramble=False)
    if arm == 'r4':
        return BeliefAlloc(seed, history, bel_off=bel_off, estimate=False, threshold=HOLD_N,
                           proactive=False, scramble=False)
    if arm == 'r1':
        return BeliefAlloc(seed, history, bel_off=bel_off, estimate=False, threshold=1,
                           proactive=False, scramble=False)
    if arm == 'r3':
        return DutyAlloc(seed, history, period=DUTY_PERIOD)
    if arm == 'scramble':
        return BeliefAlloc(seed, history, bel_off=bel_off, estimate=True, threshold=HOLD_N,
                           proactive=True, scramble=True)
    raise ValueError(arm)


def _run_core(seed, history, arm, condition, record_trace=False, swap_at=None,
              ports=PORTS, damage=True):
    ac12.PORTS = ports; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    bel_off = bel_offset(o)
    alloc = _make_alloc(arm, seed, history, bel_off)
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
    succ = ac95.Succession('real', encoded)
    schedule, cut_key, cut_start, cut_end = _condition_params(condition)
    cut_obj = ReadCut(cut_key, cut_start, cut_end)
    step = build_step(alloc, succ, build_offs, cfg, cut_obj)
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
    entry_life_at_cut_start = None
    entry_life_at_cut_end = None
    entry_expired_during_cut = False
    bel_at_cut_end = None
    bel_at_horizon = None
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
        if condition == 'cut':
            if t == CUT_TICK:
                place = ac12.m12.slot_of_key(o.memory, 1)
                entry_life_at_cut_start = 0 if place is None else int(
                    o.memory.life[place[0], place[1]].max())
            if t == CUT_TICK + WINDOW - 1:
                place = ac12.m12.slot_of_key(o.memory, 1)
                entry_life_at_cut_end = 0 if place is None else int(
                    o.memory.life[place[0], place[1]].max())
                bel_at_cut_end = bel_read(o, bel_off)
            if CUT_TICK <= t < CUT_TICK + WINDOW and entry_life_at_cut_start is not None \
                    and ac12.m12.slot_of_key(o.memory, 1) is None:
                entry_expired_during_cut = True
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
                bel_minority_end=bel_minority(o, bel_off),
                bel_events=getattr(alloc, 'bel_events', []),
                entry_life_at_cut_start=entry_life_at_cut_start,
                entry_life_at_cut_end=entry_life_at_cut_end,
                entry_expired_during_cut=entry_expired_during_cut,
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


def run(seed, history, arm, condition, ports=PORTS, record_trace=False):
    row, o, _ = _run_core(seed, history, arm, condition, record_trace=record_trace,
                          ports=ports)
    return row


# ---------------- observer-discard (host-state dependence, on the candidate) ----------------
def observer_discard_equivalence(seed, history, condition='cut', swap_tick=None):
    """Per-tick observer-discard on the CANDIDATE: at `swap_tick` (default mid-cut), the
    succession observer AND the alloc (clearing its observational bel_events list) are replaced
    with fresh objects; the trajectory must be byte-identical at EVERY tick. The estimate value
    lives in maintained state (the dead-rule action bit), so it is recovered from the body, not
    the host -- this is the state-sufficiency / host-state-dependence check the card requires."""
    if swap_tick is None:
        swap_tick = CUT_TICK + WINDOW // 2
    base, base_o, base_trace = _run_core(seed, history, 'candidate', condition,
                                         record_trace=True)
    swapped, swapped_o, swapped_trace = _run_core(seed, history, 'candidate', condition,
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
    return dict(seed=seed, history=history, condition=condition, swap_tick=swap_tick,
                swap_applied=swapped['swap_applied'],
                per_tick_identical=per_tick_identical,
                n_equal=n_equal, n_ticks=len(base_trace), first_div=first_div,
                terminal_identical=base['state_hash'] == swapped['state_hash'],
                base_hash=base['state_hash'], swapped_hash=swapped['state_hash'])


# ---------------- arm identity: candidate == r2 in no_cause ----------------
def no_cause_identity(seed, history):
    cand = run(seed, history, 'candidate', 'no_cause')
    r2 = run(seed, history, 'r2', 'no_cause')
    return cand['state_hash'] == r2['state_hash']


# ---------------- faithful-copy reproduction (r2 reproduces ac100 gray_ctl) ----------------
def ac100_reproduction(seed, history):
    """r2 at the AC100 single-move world (PORTS=2, blind 1/2) reproduces ac100 gray_ctl
    byte-for-byte -- the single-change license that the runner is a faithful copy of ac100's
    run loop (the ONLY declared change here is PORTS=4 in the AC106 world)."""
    got = _run_core(seed, history, 'r2', 'move', ports=2, damage=True)[0]
    want = ac100.run(seed, history, 'gray_ctl', schedule=ac100.SINGLE_MOVE)
    return got['state_hash'] == want['state_hash']


# ---------------- gates (recomputed from rows) ----------------
def gates_ac106(rows, seeds, ident=None):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
    n_ind = len(seeds) * 2

    # G1 -- the estimate carries relevant information: e=0 (E_machinery) in `cut`,
    #       e=1 (E_world) in `move`, on every individual.
    g1 = True
    for s in seeds:
        for h in (0, 1):
            cut = by[(s, h, 'cut')]['candidate']
            move = by[(s, h, 'move')]['candidate']
            if not (cut['bel_at_horizon'] == 0 and move['bel_at_horizon'] == 1):
                g1 = False

    # G2 -- guidance in E_machinery (P1): the candidate holds route-1 (zero relinquishments)
    #       while r2 relinquishes (>= 1). Per-individual dominance.
    g2 = True
    g2_cases = []
    for s in seeds:
        for h in (0, 1):
            cand = by[(s, h, 'cut')]['candidate']
            r2 = by[(s, h, 'cut')]['r2']
            if not (cand['relinquishments'] == 0 and r2['relinquishments'] >= 1):
                g2 = False
                g2_cases.append((s, h, cand['relinquishments'], r2['relinquishments']))

    # G3 -- guidance in E_world (P2): the candidate relinquishes the stale route (>= 1).
    g3 = all(by[(s, h, 'move')]['candidate']['relinquishments'] >= 1
             for s in seeds for h in (0, 1))

    # G4 -- no-cause identity (P3): candidate byte-identical to r2 when no cause is present.
    g4 = ident is not None and len(ident) == n_ind and all(ident.values())

    # G5 -- causal role (P4): scrambling the estimate changes behaviour in `cut` --
    #       the candidate holds the entry through the outage (entry survives) while the
    #       scrambled estimate lets it lapse (entry expired during the cut window).
    g5 = True
    g5_cases = []
    for s in seeds:
        for h in (0, 1):
            cand = by[(s, h, 'cut')]['candidate']
            scr = by[(s, h, 'cut')]['scramble']
            if not (cand['entry_expired_during_cut'] is False and
                    scr['entry_expired_during_cut'] is True):
                g5 = False
                g5_cases.append((s, h, cand['entry_expired_during_cut'],
                                 scr['entry_expired_during_cut']))

    # G6 -- proactive renewal vs the longer counter (the sharpest falsification): in `cut`,
    #       the candidate's entry survives to cut-end (life > 0) while r4's expires.
    g6 = True
    g6_cases = []
    for s in seeds:
        for h in (0, 1):
            cand = by[(s, h, 'cut')]['candidate']
            r4 = by[(s, h, 'cut')]['r4']
            if not (cand['entry_life_at_cut_end'] is not None and
                    cand['entry_life_at_cut_end'] > 0 and
                    (r4['entry_life_at_cut_end'] == 0 or r4['entry_expired_during_cut'])):
                g6 = False
                g6_cases.append((s, h, cand['entry_life_at_cut_end'], r4['entry_life_at_cut_end']))

    return {
        'G1_estimate_carries_information': g1,
        'G2_guidance_holds_in_emachinery': g2,
        'G3_guidance_relinquishes_in_eworld': g3,
        'G4_no_cause_identity': g4,
        'G5_causal_role_scramble': g5,
        'G6_proactive_renewal_beats_longer_counter': g6,
        'G7_completeness_determinism': None,
        '_g2_cases': g2_cases,
        '_g5_cases': g5_cases,
        '_g6_cases': g6_cases,
    }


# ---------------- collectors ----------------
def collect_engineering(root, seeds, conditions=None):
    if conditions is None:
        conditions = list(CONDITIONS)
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for cond in conditions:
                    for arm in ARMS:
                        r = run(seed, history, arm, cond)
                        rows.append(r)
                        f.write(json.dumps(r) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['bel_at_horizon'],
                 r['entry_life_at_cut_end'], r['entry_expired_during_cut'],
                 r['proactive_writes'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    ident = {f'{s}/{h}': no_cause_identity(s, h) for s in seeds for h in (0, 1)}
    ac100_rep = {f'{s}/{h}': ac100_reproduction(s, h) for s in seeds for h in (0, 1)}
    g = gates_ac106(rows, seeds, ident=ident)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), PORTS=PORTS,
             WINDOW=WINDOW, HOLD_N=HOLD_N, rows=rows, gates=g,
             no_cause_identity=ident, ac100_reproduction=ac100_rep),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    print(json.dumps(dict(no_cause_identity=ident, ac100_reproduction=ac100_rep),
                     indent=2, default=str))
    return rows, g


def preflight(protocol='AC106_PROTOCOL_v1.md'):
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


def collect_finals(root, seeds, do_preflight=True, conditions=None):
    if conditions is None:
        conditions = list(CONDITIONS)
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
                for cond in conditions:
                    for arm in ARMS:
                        r = run(seed, history, arm, cond)
                        rows.append(r)
                        f.write(json.dumps(r) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['bel_at_horizon'],
                 r['entry_life_at_cut_end'], r['entry_expired_during_cut'],
                 r['proactive_writes'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    ident = {f'{s}/{h}': no_cause_identity(s, h) for s in seeds for h in (0, 1)}
    g = gates_ac106(rows, seeds, ident=ident)
    first = rows[0]
    rerun = run(first['seed'], first['history'], first['arm'], first['condition'])
    g['G7_completeness_determinism'] = (
        len(rows) == len(seeds) * len(ARMS) * len(conditions) * 2
        and rerun['state_hash'] == first['state_hash'])
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), PORTS=PORTS,
             WINDOW=WINDOW, HOLD_N=HOLD_N, hashes=hashes, gates=g, rows=rows,
             no_cause_identity=ident),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac106_engineering_v1', ENGINEERING)
        return
    collect_finals('ac106_results_v1', FINAL_SEEDS)


if __name__ == '__main__':
    main()
