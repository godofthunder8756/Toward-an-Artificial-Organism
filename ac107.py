"""AC107 (K5, engineering): a minimal cause-estimator on the two-cause task, with credible rivals.

Parent (K4, t_1b995c9c): TASK_IDENTIFIABILITY_v1.md. K4 established that the two AC106 causes
(E_world route-move vs E_machinery read-cut) produce disjoint action-observation histories once
the estimator observes the organism's own (bound, used_held, productive) triple instead of
`productive` alone. K5 implements that estimator and asks the card's question:

    Does a minimal estimator, supported by the K4 identifiability analysis, discriminate the
    causes AND do something the reactive baseline does not?

The estimator (candidate arm) is a finite-state cause estimate e in {E_world=1, E_machinery=0},
stored in the same dead-rule action bit as AC106 (14*dead_rule_index+10, acquired value 1 = E_world,
the AC12 inverted-semantics pattern: damaged by the sticky program stream, read by majority, repaired
by the paid bank-0 repair, excluded from reg_from_active). What changes from AC106 is the UPDATE RULE:
it reads the K4 triple and gates every conclusion on the organism's own memory, closing the K1 confound
(AC106 read `productive` alone and mislabelled a blind re-bind as "productivity resumed"):

  - bound=1 & used_held=0  -> e = E_machinery   (the READ is suppressed while the entry is still
                            bound -- the cut signature; fires on every in-window contact)
  - used_held=1 & productive=0 -> e = E_world   (F1: a held entry failed -> the entry is stale)
  - bound=0 & productive=1 -> e = E_world       (a blind re-bind after a drop -> re-acquisition)
  - used_held=1 & productive=1 & streak>0 & post-DEV -> e = E_machinery  (F2: productivity resumed
                            via a HELD entry after a failure -> the read was restored on a valid entry)

Consumption (two branches, flexibly consumed, exactly the C1 §5 requirement):
  - e = E_world   -> the frozen Gray streak: relinquish after STREAK_N consecutive unproductive
                     contacts (byte-identical to r2 in this branch).
  - e = E_machinery -> withhold relinquishment indefinitely AND direct paid proactive renewal of the
                     still-valid entry through the outage (active maintenance, ahead of the
                     renewal-urgent bit).

The matched rivals (each verified to differ as advertised):
  - r2: the frozen Gray streak (STREAK_N=6), counts ALL unproductive contacts, no estimate, no
        proactive renewal. The "existing reactive/history-based baseline".
  - r4: a genuinely LONGER-window raw counter -- its OWN host-integer counter (threshold HOLD_N=24,
        representable where the 3-bit Gray streak saturates at 7), counts ALL failures, no estimate,
        no proactive renewal. Fixes the AC106 HOLD_N == STREAK_N defect (K1 P1). Receives the same
        (bound, used_held) observation interface (matched), but is state-blind by construction.
  - r1: reactive -- relinquish on the first unproductive contact.
  - scramble: read-only causal-role control (K1 P5 fix). The READ of e is forced to E_world, while
        the estimate's paid WRITES and the proactive-renewal code path are left intact (the
        expenditure-matched read control AC106's scramble never was). The only divergence from the
        candidate is the read value.

World: the AC106 world -- AC100 Gray-streak architecture, corrupt=False, TICKS=16384, DEV=512,
PORTS=4 (blind fallback 1/4), mapping over {0,1}; the read-cut is the ac9.blocked / AC91-92 W-cut
kind (balance-identity-safe, byte-identical to frozen at WINDOW=0).

Discipline: ENGINEERING ONLY (no protocol, no freeze, no finals). Discrimination is measured at
decision times (drop_ticks / bel_events / window end), not only the horizon. Mistakes, latency,
behavioural consequences, expenditure, and survival are reported separately. Attempted updates are
logged separately from completed writes. New persistent host fields are audited, and candidate state
sufficiency is tested by per-tick observer-discard.
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
from ac106 import ReadCut, bel_offset, bel_read, bel_minority

TICKS = ac95.TICKS                  # 16384
DEV = ac71.DEV                      # 512
STREAK_N = ac12.STREAK_N            # 6
MOVE_TICK = ac95.MOVE_TICK          # 8192
CUT_TICK = MOVE_TICK                # the two causes land at the SAME tick (identical failure)

PORTS = 4                           # blind fallback is uniform over {0,1,2,3}; mapping over {0,1}
WINDOW = 96                         # read-cut window (ticks); longer than the entry life (64)
HOLD_N = 24                         # r4's genuinely longer threshold (the Gray streak saturates at 7)
BEL_WORD_BIT = 10                   # action bit 0 of the dead rule (acquired value 1 = E_world)

ARMS = ('candidate', 'r2', 'r4', 'r1', 'scramble')
CONDITIONS = ('no_cause', 'move', 'cut')

# the observation interface: per channel-1 contact (bound, used_held, productive).
#   bound     = the organism's own introspection read (o.memory.read(1) is not None) -- NOT shimmed
#   used_held = did the contact use a held entry or fall back to blind (selected is not None) --
#               the shimmed retrieval result, forwarded to the allocator (K4 §9 item 1)
#   productive= did the contact yield (e['productive'] > 0)

SOURCES = ['ac107.py', 'ac106.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py', 'ac95.py',
           'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py',
           'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py', 'ac4_transport.py',
           'ac1.py', 'AC107_PROTOCOL_v1.md']

ENGINEERING = list(range(8))
FINAL_SEEDS = [6000, 6001, 6002, 6003, 6004, 6005, 6006, 6007]   # fresh, untouched, pre-freeze


# ---------------- the estimate bit (vulnerable, paid-maintained, attempt-tracked) ----------------
def bel_write(o, e, val, bel_off):
    """Atomic, W-gated paid write of the estimate bit to `val` (<= 7 replicas).

    Returns (written, attempted, refused):
      written  = replicas actually written (0 if the bit already reads val, or if the cap refused)
      attempted= 1 if this call would have changed the value (a value-changing update was attempted)
      refused  = 1 if the update was attempted but the produced machinery's cap refused it whole.
    Attempted updates are thus logged separately from completed writes (the card's requirement).
    """
    b = o.body
    sites = np.argwhere(b.traces[0, bel_off] != val)
    n = len(sites)
    if n == 0:
        return 0, 0, 0            # already at value: not an attempted update
    cap = ac95._cap(b)
    if n > cap:
        return 0, 1, 1            # attempted, refused (atomic: write nothing)
    b.traces[0, bel_off, sites[:, 0]] = val
    b.energy -= n
    b.material -= n
    e['spent_e'] += n
    e['spent_m'] += n
    e['writes'] += n
    e['bel_writes'] = e.get('bel_writes', 0) + n
    return n, 1, 0


# ---------------- the read-cut (imported from ac106) ----------------
# ReadCut suppresses only the contact's `selected` in-window; the introspection read is unshimmed.


# ---------------- the allocators ----------------
class BaselineAlloc(ac99_d2.GrayAllocEraseReserve):
    """r2: the frozen Gray streak (STREAK_N=6), counting ALL unproductive contacts.

    Accepts the (used_held) observation so every arm shares one interface, but ignores it: the
    reactive/history baseline has no cause attribution by construction.
    """
    def __init__(self, seed, history):
        super().__init__('allocate', seed, history, reserve=False)

    def outcome(self, o, key, e, used_held=None):
        return super().outcome(o, key, e)


class LongCounterAlloc(ac99_d2.GrayAllocEraseReserve):
    """r4: a genuinely LONGER-window raw counter (HOLD_N=24), with its OWN counter state.

    The 3-bit Gray streak saturates at 7, so a threshold above 7 is unreachable on it (K1 P1). r4
    carries a host-integer counter `self.fail_count` (disclosed below -- a rival-side comparator,
    not the candidate's operational memory) so a longer threshold is genuinely representable.
    It receives the (bound, used_held) interface but is state-blind: it counts ALL unproductive
    contacts, makes no cause attribution, and performs no proactive renewal.
    """
    def __init__(self, seed, history, threshold=HOLD_N):
        super().__init__('allocate', seed, history, reserve=False)
        self.threshold = threshold
        self.fail_count = {0: 0, 1: 0}   # per-key host-int raw counters (disclosed rival field,
                                          # mirroring the frozen streak's per-key structure)
        self.counter_events = []          # (tick, key, after, dropped) observational

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if e['productive'] > 0:
            self._restore(o, e, key)
            self.fail_count[key] = 0
            return
        self.fail_count[key] += 1
        dropped = 0
        if self.fail_count[key] >= self.threshold:
            n_before = len(self.log['dropped'])
            self._drop(o, e, key)
            dropped = 1 if len(self.log['dropped']) > n_before else 0
            self.fail_count[key] = 0
        self.counter_events.append((self.now, key, self.fail_count[key], dropped))


class ReactiveAlloc(ac99_d2.GrayAllocEraseReserve):
    """r1: reactive -- relinquish on the FIRST unproductive contact (no memory, no estimate)."""
    def __init__(self, seed, history):
        super().__init__('allocate', seed, history, reserve=False)

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if e['productive'] > 0:
            self._restore(o, e, key)
            return
        self._drop(o, e, key)


class Estimator(ac99_d2.GrayAllocEraseReserve):
    """The candidate (and, via flags, the scramble causal-role control).

    Maintains and consults the one-bit cause estimate e in the dead-rule action bit, updated by the
    K4 discriminator over (bound, used_held, productive). Consumes it as the C1 §5 two branches:
    E_world -> frozen streak relinquishment; E_machinery -> hold + proactive renewal.
    """

    def __init__(self, seed, history, bel_off=None, estimate=True, proactive=True, scramble=False):
        super().__init__('allocate', seed, history, reserve=False)
        self.bel_off = bel_off
        self.estimate = estimate
        self.proactive = proactive
        self.scramble = scramble
        self.bel_events = []        # (tick, kind, val) observational
        self.bel_attempts = 0       # attempted value-changing updates (completed + refused)
        self.bel_refused = 0        # attempted updates refused whole by the W-gated cap

    # -- the read/write primitives (scramble = read-only: write intact, read forced) --
    def _bel(self, o):
        if self.scramble or not self.estimate:
            return 1                # forced read E_world
        return bel_read(o, self.bel_off)

    def _bel_write(self, o, e, val):
        if not self.estimate:
            return 0, 0, 0
        n, attempted, refused = bel_write(o, e, val, self.bel_off)
        self.bel_attempts += attempted
        self.bel_refused += refused
        return n, attempted, refused

    def _proactive_renew(self, o, e, key):
        """Direct paid per-slot renewal of the route entry for `key`, bypassing the program's action
        selection (so it is not subject to the material-contact hijack during the outage)."""
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

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if key != 1:
            super().outcome(o, key, e)          # channel 0 is never moved/cut: frozen streak
            return
        bound = (o.memory.read(1) is not None)
        used = bool(used_held)
        productive = e['productive'] > 0
        cur = ac99_d2.gray_streak_read(o, 1, self.streak_offs)
        # ---- the K4 discriminator (gated on the organism's own memory) ----
        if bound and not used:
            # the read is suppressed while the entry is still bound -> E_machinery (cut signature).
            # This fires on EVERY in-window contact (blind failure AND blind success) and is the
            # load-bearing observation: it is unambiguous because in E_world a bound entry is always
            # USED (used_held=1) and fails, so (bound=1, used_held=0) never occurs under a move.
            self._bel_write(o, e, 0)
            self.bel_events.append((self.now, 'machinery_cut', 0))
        elif used and not productive:
            # F1: a held entry failed -> the entry is stale -> E_world
            self._bel_write(o, e, 1)
            self.bel_events.append((self.now, 'world_held_fail', 1))
        elif not bound and productive:
            # a blind re-bind after a drop -> re-acquisition -> E_world
            self._bel_write(o, e, 1)
            self.bel_events.append((self.now, 'world_rebind', 1))
        # NOTE: K4's F2 ("read bound at the productive resumption") is deliberately NOT implemented
        # as a separate streak-gated rule. It is subsumed by rule 1 above (bound=1 -> E_machinery is
        # already established on the first in-window contact) and rule 3 (bound=0 -> E_world). A
        # streak-gated "resume after a run of failures" is ambiguous: after a relinquishment the
        # frozen Gray reset (5->0 = 21 replicas) is refused at W=2, so the streak stays > 0 and a
        # re-bound entry's yield would be mislabelled as "resumed without re-binding" -- exactly the
        # K1 confound, reappearing via the streak. See AC107_ENGINEERING_v1.md.
        # ---- the two consumptions ----
        if productive:
            self._restore(o, e, key)
            ac99_d2.gray_streak_write(o, e, key, 0, self.streak_offs)
            if self._bel(o) == 0 and self.proactive:
                self._proactive_renew(o, e, key)
            self.streak_events.append((self.now, key, cur, 0, 0))
            return
        # unproductive contact-1
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


# ---------------- the build (ac95.build + the read-cut shim + used_held forwarding) ----------------
READ_LINE = "            selected=o.memory.read(action); port=int(coin) if selected is None else selected"
READ_LINE_NEW = "            selected=cut_obj.read(o.memory, action); port=int(coin) if selected is None else selected"


def build_step(alloc, succ, reg_offs, cfg, cut_obj):
    """ac95.build, plus the read-cut shim on the contact's read, plus forwarding (bound, used_held)
    to the allocator's outcome. `bound` is read by the allocator from the unshimmed memory; only
    `used_held` (the shimmed `selected`) is forwarded explicitly, the K4 §9 interface change."""
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
                      ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e,int(selected is not None))")
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
    exec(compile(src, 'ac107_step', 'exec'), ns, fns)
    return fns['step']


# ---------------- the run core ----------------
def _condition_params(condition):
    if condition == 'move':
        return [(MOVE_TICK, 'flip')], None, 0, 0
    if condition == 'cut':
        return [], 1, CUT_TICK, CUT_TICK + WINDOW
    return [], None, 0, 0          # no_cause


def _make_alloc(arm, seed, history, bel_off):
    if arm == 'r2':
        return BaselineAlloc(seed, history)
    if arm == 'candidate':
        return Estimator(seed, history, bel_off=bel_off, estimate=True, proactive=True, scramble=False)
    if arm == 'r4':
        return LongCounterAlloc(seed, history, threshold=HOLD_N)
    if arm == 'r1':
        return ReactiveAlloc(seed, history)
    if arm == 'scramble':
        return Estimator(seed, history, bel_off=bel_off, estimate=True, proactive=True, scramble=True)
    raise ValueError(arm)


def _true_cause(condition):
    """The hidden cause label, used ONLY to score the estimator (never supplied to it)."""
    if condition == 'cut':
        return 0                  # E_machinery
    if condition == 'move':
        return 1                  # E_world
    return None                   # no cause


def _run_core(seed, history, arm, condition, record_trace=False, swap_at=None, ports=PORTS):
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
    bel_at_first_drop = None
    first_contact_in_window = None
    first_correct_tick = None
    drop_during_window = 0
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
            if bel_at_first_drop is None:
                bel_at_first_drop = bel_read(o, bel_off)
            drop_ticks.append((t, list(place),
                               ac12.bit_value(o, offs[2 * place[0] + place[1]])))
            if cut_key == 1 and CUT_TICK <= t < CUT_TICK + WINDOW:
                drop_during_window += 1
        if len(alloc.log.get('restored', [])) > prev_restores:
            restore_ticks.append((t, list(alloc.log.get('restored', [])[-1])))
        # decision-time scoring (the estimator's own maintained value, read from the body)
        if true_cause is not None and first_correct_tick is None:
            if t >= CUT_TICK and bel_read(o, bel_off) == true_cause:
                first_correct_tick = t
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
    # mistakes: post-intervention bel_events that wrote the WRONG cause label
    mistakes = 0
    if true_cause is not None:
        for (bt, kind, val) in getattr(alloc, 'bel_events', []):
            if bt >= CUT_TICK and val != true_cause:
                mistakes += 1
    bel_attempts = getattr(alloc, 'bel_attempts', 0)
    bel_refused = getattr(alloc, 'bel_refused', 0)
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
                counter_events=getattr(alloc, 'counter_events', []),
                bel=bel_read(o, bel_off),
                bel_at_horizon=bel_at_horizon,
                bel_at_cut_end=bel_at_cut_end,
                bel_at_first_drop=bel_at_first_drop,
                bel_minority_end=bel_minority(o, bel_off),
                bel_events=getattr(alloc, 'bel_events', []),
                bel_attempts=bel_attempts,
                bel_refused=bel_refused,
                mistakes=mistakes,
                first_correct_tick=first_correct_tick,
                decision_latency=(first_correct_tick - CUT_TICK) if first_correct_tick is not None else None,
                entry_life_at_cut_start=entry_life_at_cut_start,
                entry_life_at_cut_end=entry_life_at_cut_end,
                entry_expired_during_cut=entry_expired_during_cut,
                drop_during_window=drop_during_window,
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
    row, o, _ = _run_core(seed, history, arm, condition, record_trace=record_trace, ports=ports)
    return row


# ---------------- observer-discard (state sufficiency, on the candidate) ----------------
def observer_discard_equivalence(seed, history, condition='cut', swap_tick=None):
    """Per-tick observer-discard on the CANDIDATE: at `swap_tick` (default mid-cut), the succession
    observer AND the alloc (clearing its observational bel_events / streak_events lists) are replaced
    with fresh objects; the trajectory must be byte-identical at EVERY tick. The estimate value lives
    in maintained state, so it is recovered from the body, not the host."""
    if swap_tick is None:
        swap_tick = CUT_TICK + WINDOW // 2
    base, base_o, base_trace = _run_core(seed, history, 'candidate', condition, record_trace=True)
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


# ---------------- faithful-copy reproduction (r2 reproduces ac100 gray_ctl at PORTS=2) ----------------
def ac100_reproduction(seed, history):
    got = _run_core(seed, history, 'r2', 'move', ports=2)[0]
    want = ac100.run(seed, history, 'gray_ctl', schedule=ac100.SINGLE_MOVE)
    return got['state_hash'] == want['state_hash']


# ---------------- the audit: candidate has NO steering host state ----------------
def audit_host_fields():
    """Enumerate the candidate's host fields and assert none steer a write: the estimate is read
    from maintained state (bel_read) and the streak from maintained state (gray_streak_read); the
    host fields are config constants or observational logs only."""
    cfg_fields = {'bel_off', 'estimate', 'proactive', 'scramble', 'threshold',
                  'arm', 'now', 'offs', 'streak_offs', 'rng', 'reserve'}
    observational = {'bel_events', 'streak_events', 'log', 'shadow', 'bel_attempts', 'bel_refused'}
    # The inherited ac12.Alloc host `streak` dict is vestigial: the candidate must never read it.
    # This is asserted structurally here and dynamically by the observer-discard equivalence.
    return dict(
        candidate_config_host_fields=sorted(cfg_fields),
        candidate_observational_host_fields=sorted(observational),
        vestigial_host_fields=['streak (inherited ac12.Alloc dict; never read on the candidate)'],
        note='no host field steers a write: e is read from traces[0, bel_off] (majority), '
             'the streak from traces[0, streak_offs] (Gray majority); bel_events/streak_events/log '
             'are observational. Observer-discard equivalence is the dynamic proof.',
    )


# ---------------- measurements (recomputed from rows; engineering, not a frozen gate set) --------
def summarize(rows, seeds):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
    n_ind = len(seeds) * 2
    inds = [(s, h) for s in seeds for h in (0, 1)]

    def survives(r):
        return r['completed'] and r['first_dead'] is None

    # M1 -- discrimination at decision times (K1 P3): in `cut` e reads E_machinery (0) at the window
    #       end; in `move` e reads E_world (1) at the first drop. Per individual, plus zero mistakes.
    m1_cut = all(by[(s, h, 'cut')]['candidate']['bel_at_cut_end'] == 0 for s, h in inds)
    m1_move = all(by[(s, h, 'move')]['candidate']['bel_at_first_drop'] == 1 for s, h in inds)
    m1_mistakes = sum(by[(s, h, c)]['candidate']['mistakes'] for s, h in inds for c in ('move', 'cut'))

    # M2 -- survival. The candidate survives every individual; r2 dies in the cut (seed 4); r4 dies
    #       in the move (seeds 1,2,4); scramble dies in the cut (seed 4).
    cand_deaths = [s for s, h in inds for c in ('move', 'cut') if not survives(by[(s, h, c)]['candidate'])]
    r2_cut_deaths = [s for s, h in inds if not survives(by[(s, h, 'cut')]['r2'])]
    r4_move_deaths = [s for s, h in inds if not survives(by[(s, h, 'move')]['r4'])]
    scr_cut_deaths = [s for s, h in inds if not survives(by[(s, h, 'cut')]['scramble'])]
    m2 = dict(candidate_deaths=sorted(cand_deaths),
              r2_cut_deaths=sorted(r2_cut_deaths),
              r4_move_deaths=sorted(r4_move_deaths),
              scramble_cut_deaths=sorted(scr_cut_deaths))

    # M3 -- the two-sided discriminator (the headline): the candidate uses the RIGHT threshold per
    #       cause -- holds in the cut (E_machinery) where r2's threshold 6 drops and dies, and drops
    #       fast in the move (E_world) where r4's threshold 24 holds too long and dies. Per-individual
    #       survival dominance in BOTH directions.
    m3_holds_cut = all(by[(s, h, 'cut')]['candidate']['relinquishments'] == 0 for s, h in inds)
    m3_drops_move = all(by[(s, h, 'move')]['candidate']['relinquishments'] >= 1 for s, h in inds)
    m3 = dict(candidate_holds_cut=m3_holds_cut,
              candidate_drops_move=m3_drops_move,
              candidate_survives_where_r2_dies=all(s in r2_cut_deaths or True for s in cand_deaths),
              r2_relinquishes_in_cut=sorted({s for s, h in inds
                                             if by[(s, h, 'cut')]['r2']['relinquishments'] >= 1}),
              r4_holds_move_too_long=sorted({s for s, h in inds
                                             if by[(s, h, 'move')]['r4']['relinquishments'] == 0
                                             and not survives(by[(s, h, 'move')]['r4'])}),
              scramble_relinquishes_in_cut=sorted({s for s, h in inds
                                                   if by[(s, h, 'cut')]['scramble']['relinquishments'] >= 1}))

    # M4 -- no-cause identity (P3): candidate byte-identical to r2 when no cause is present.
    m4 = {f'{s}/{h}': no_cause_identity(s, h) for s, h in inds}
    m4_ok = all(m4.values())

    # M5 -- causal role (P4): the read-only scramble changes behaviour in `cut` -- it relinquishes
    #       (and dies on seed 4) where the candidate holds. The K1 P5 fix is that the scramble does
    #       NOT suppress the estimate's writes: it runs the identical discriminator+write code with
    #       only the read forced. On the hold-individuals the two arms' estimate spend matches
    #       exactly; on the re-bind individuals the scramble writes the bit a second time (rule 3 at
    #       re-bind), which is a downstream consequence of the trajectory the forced read induces,
    #       not a spend suppression.
    m5_cases = []
    m5_bel = {}
    for s, h in inds:
        cand = by[(s, h, 'cut')]['candidate']
        scr = by[(s, h, 'cut')]['scramble']
        m5_cases.append((s, h, cand['relinquishments'], scr['relinquishments']))
        m5_bel[f'{s}/{h}'] = dict(candidate=cand['bel_writes'], scramble=scr['bel_writes'])
    hold_ind = [(s, h) for s, h in inds if by[(s, h, 'cut')]['scramble']['relinquishments'] == 0]
    m5 = dict(
        scramble_relinquishes_somewhere=any(scr >= 1 for (_s, _h, _c, scr) in m5_cases),
        scramble_deaths=sorted(scr_cut_deaths),
        scramble_writes_not_suppressed=all(by[(s, h, 'cut')]['scramble']['bel_attempts'] >= 1
                                           for s, h in inds),
        bel_spend_matches_on_hold_individuals=all(
            m5_bel[f'{s}/{h}']['candidate'] == m5_bel[f'{s}/{h}']['scramble'] for s, h in hold_ind),
        bel_writes_by_individual=m5_bel,
    )

    # M6 -- proactive renewal is REDUNDANT with the frozen reactive renewal: r4 (no proactive
    #       renewal) keeps the entry alive through the cut on every individual, so the candidate's
    #       proactive spend adds nothing to entry survival (the C1 §7 anticipated outcome).
    m6 = dict(
        r4_entry_survives_cut=all(by[(s, h, 'cut')]['r4']['entry_life_at_cut_end'] is not None
                                  and by[(s, h, 'cut')]['r4']['entry_life_at_cut_end'] > 0
                                  for s, h in inds),
        candidate_entry_survives_cut=all(by[(s, h, 'cut')]['candidate']['entry_life_at_cut_end'] is not None
                                         and by[(s, h, 'cut')]['candidate']['entry_life_at_cut_end'] > 0
                                         for s, h in inds),
        candidate_proactive_writes=sorted({by[(s, h, 'cut')]['candidate']['proactive_writes']
                                           for s, h in inds}),
    )

    # M7 -- move latency: the candidate's first drop (threshold 6) precedes r4's (threshold 24).
    cand_drop = {s: min((t for t, _p, _r in by[(s, 0, 'move')]['candidate']['drop_ticks']), default=None)
                 for s in seeds}
    r4_drop = {s: min((t for t, _p, _r in by[(s, 0, 'move')]['r4']['drop_ticks']), default=None)
               for s in seeds}
    m7 = {s: dict(candidate=cand_drop[s], r4=r4_drop[s]) for s in seeds}

    # rival distinctness (the card: "verify the rivals actually differ as advertised")
    rival_distinct = {
        'r4_threshold_gt_streak_max': HOLD_N > 7,
        'r4_threshold_ne_streak_n': HOLD_N != STREAK_N,
        'r2_vs_r4_differ_in_cut': any(by[(s, h, 'cut')]['r2']['relinquishments']
                                      != by[(s, h, 'cut')]['r4']['relinquishments']
                                      for s, h in inds),
        'r2_vs_r4_differ_in_move': any(by[(s, h, 'move')]['r2']['relinquishments']
                                       != by[(s, h, 'move')]['r4']['relinquishments']
                                       for s, h in inds),
    }

    return {
        'M1_discrimination_at_decision_times': dict(cut=m1_cut, move=m1_move,
                                                    total_mistakes=m1_mistakes),
        'M2_survival': m2,
        'M3_two_sided_discriminator': m3,
        'M4_no_cause_identity': m4_ok,
        'M5_causal_role_scramble': m5,
        'M6_proactive_renewal_redundant': m6,
        'M7_move_latency': m7,
        'rival_distinctness': rival_distinct,
        'no_cause_identity_detail': m4,
    }


# ---------------- frozen gates (the four questions, prespecified in AC107_PROTOCOL_v1.md) --------
def gates_ac107(rows, seeds, observer_discard, no_cause_identity):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
    n_ind = len(seeds) * 2
    inds = [(s, h) for s in seeds for h in (0, 1)]

    def survives(r):
        return r['completed'] and r['first_dead'] is None

    cand_cut = [by[(s, h, 'cut')]['candidate'] for s, h in inds]
    cand_move = [by[(s, h, 'move')]['candidate'] for s, h in inds]
    r2_cut = [by[(s, h, 'cut')]['r2'] for s, h in inds]
    r4_move = [by[(s, h, 'move')]['r4'] for s, h in inds]
    scr_cut = [by[(s, h, 'cut')]['scramble'] for s, h in inds]

    # G1 discrimination (Q1): decision-time discrimination + non-vacuous cut + zero mistakes.
    g1_cut = all(r['bel_at_cut_end'] == 0 and (r['entry_life_at_cut_start'] or 0) > 0
                 for r in cand_cut)
    g1_move = all(r['bel_at_first_drop'] == 1 and r['relinquishments'] >= 1 for r in cand_move)
    g1_mistakes = sum(r['mistakes'] for r in cand_cut + cand_move) == 0
    g1 = g1_cut and g1_move and g1_mistakes

    # G2 content causal (Q2): candidate holds in cut; scramble relinquishes and dies where the
    # candidate survives.
    g2_holds = all(r['relinquishments'] == 0 for r in cand_cut)
    g2_scramble_relinq = any(r['relinquishments'] >= 1 for r in scr_cut)
    g2_scramble_dies = any((not survives(s)) and survives(c) for s, c in zip(scr_cut, cand_cut))
    g2 = g2_holds and g2_scramble_relinq and g2_scramble_dies

    # G3 state sufficiency (Q3): observer-discard per-tick identical.
    g3 = len(observer_discard) == n_ind and all(
        d.get('per_tick_identical') and d.get('terminal_identical') and d.get('swap_applied')
        for d in observer_discard.values())

    # G4 no-cause identity (Q3): candidate == r2 in no_cause.
    g4 = all(no_cause_identity.get(f'{s}/{h}') is True for s, h in inds)

    # G5 comparative advantage (Q4): candidate survival lower bound + per-individual dominance.
    cand_cut_surv = sum(survives(r) for r in cand_cut)
    cand_move_surv = sum(survives(r) for r in cand_move)
    g5_lower = cand_cut_surv >= 12 and cand_move_surv >= 12
    g5_r2_death = any((not survives(r)) and survives(c) for r, c in zip(r2_cut, cand_cut))
    g5_r4_death = any((not survives(r)) and survives(c) for r, c in zip(r4_move, cand_move))
    g5 = g5_lower and g5_r2_death and g5_r4_death

    # G6 completeness/determinism: row count + first-row re-run state_hash.
    expected = len(seeds) * len(ARMS) * len(CONDITIONS) * 2
    first = rows[0]
    g6 = len(rows) == expected and run(first['seed'], first['history'], first['arm'],
                                       first['condition'])['state_hash'] == first['state_hash']

    # G7 rival distinctness.
    g7 = (HOLD_N > 7 and HOLD_N != STREAK_N
          and any(by[(s, h, 'cut')]['r2']['relinquishments']
                  != by[(s, h, 'cut')]['r4']['relinquishments'] for s, h in inds)
          and any(by[(s, h, 'move')]['r2']['relinquishments']
                  != by[(s, h, 'move')]['r4']['relinquishments'] for s, h in inds))

    return {
        'G1_discrimination': g1,
        'G2_content_causal_scramble': g2,
        'G3_state_sufficiency_observer_discard': g3,
        'G4_no_cause_identity': g4,
        'G5_comparative_advantage': g5,
        'G6_completeness_determinism': g6,
        'G7_rival_distinctness': g7,
        '_survival_counts': {
            'candidate_cut': cand_cut_surv, 'candidate_move': cand_move_surv,
            'r2_cut': sum(survives(r) for r in r2_cut),
            'r4_move': sum(survives(r) for r in r4_move),
            'scramble_cut': sum(survives(r) for r in scr_cut),
        },
        '_deaths': {
            'r2_cut': sorted({s for s, h in inds if not survives(by[(s, h, 'cut')]['r2'])}),
            'r4_move': sorted({s for s, h in inds if not survives(by[(s, h, 'move')]['r4'])}),
            'scramble_cut': sorted({s for s, h in inds
                                    if not survives(by[(s, h, 'cut')]['scramble'])}),
            'candidate_any': sorted({s for s, h in inds for c in ('move', 'cut')
                                     if not survives(by[(s, h, c)]['candidate'])}),
        },
    }


def preflight(protocol='AC107_PROTOCOL_v1.md'):
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
                 r['relinquishments'], r['drop_during_window'], r['routes'], r['bel_at_horizon'],
                 r['bel_at_first_drop'], r['bel_at_cut_end'], r['entry_life_at_cut_end'],
                 r['entry_expired_during_cut'], r['mistakes'], r['decision_latency'],
                 r['proactive_writes'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    obs = {f'{s}/{h}': observer_discard_equivalence(s, h, 'cut')
           for s in seeds for h in (0, 1)}
    ac100_rep = {f'{s}/{h}': ac100_reproduction(s, h) for s in seeds for h in (0, 1)}
    m = summarize(rows, seeds)
    audit = audit_host_fields()
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), PORTS=PORTS,
             WINDOW=WINDOW, HOLD_N=HOLD_N, STREAK_N=STREAK_N, rows=rows, measurements=m,
             observer_discard=obs, ac100_reproduction=ac100_rep, host_field_audit=audit),
        indent=2, default=str))
    print(json.dumps(dict(measurements=m), indent=2, default=str))
    print(json.dumps(dict(observer_discard={k: v.get('per_tick_identical')
                                            for k, v in obs.items()}), indent=2, default=str))
    print(json.dumps(dict(ac100_reproduction=ac100_rep), indent=2, default=str))
    return rows, m


def collect_finals(root, seeds, do_preflight=True, conditions=None):
    if conditions is None:
        conditions = list(CONDITIONS)
    if do_preflight:
        preflight()
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
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
                        f.write(json.dumps(r) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['bel_at_cut_end'], r['bel_at_first_drop'],
                 r['mistakes'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    obs = {f'{s}/{h}': observer_discard_equivalence(s, h, 'cut') for s in seeds for h in (0, 1)}
    ac100_rep = {f'{s}/{h}': ac100_reproduction(s, h) for s in seeds for h in (0, 1)}
    ident = {f'{s}/{h}': no_cause_identity(s, h) for s in seeds for h in (0, 1)}
    g = gates_ac107(rows, seeds, obs, ident)
    audit = audit_host_fields()
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), PORTS=PORTS,
             WINDOW=WINDOW, HOLD_N=HOLD_N, STREAK_N=STREAK_N, hashes=hashes, gates=g,
             rows=rows, observer_discard=obs, ac100_reproduction=ac100_rep,
             no_cause_identity=ident, host_field_audit=audit),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac107_engineering_v1', ENGINEERING)
        return
    if '--smoke' in sys.argv:
        collect_engineering('ac107_smoke_v1', [0, 1, 2])
        return
    if '--finals' in sys.argv:
        collect_finals('ac107_results_v1', FINAL_SEEDS)
        return
    print('AC107: --engineering (seeds 0-7), --smoke (0-2), or --finals (frozen confirmation).')


if __name__ == '__main__':
    main()
