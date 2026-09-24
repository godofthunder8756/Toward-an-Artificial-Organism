"""AC112 (P5): the heterogeneous-likelihood-ratio two-counter estimate at organism scale.

Parent (P4, t_260b4671): P4_COGNITION_CONTINUATION_v1.md selected design 2 -- relax the C4
premise "M never yields" to a residual yield eps, giving TWO weak likelihood ratios,
w_u = log((4/3)(1-eps)) (occluded-unproductive, weak M) and w_p = log(4*eps)
(occluded-productive, weak C), whose ratio is non-integer. P4 demonstrated at the harness
level (_p4_heterogeneous_lr.py) that (i) the sufficient statistic is the integer PAIR
(n_u, n_p) consumed as the weighted sum n_u*w_u + n_p*w_p, (ii) a graded log-odds register
is EXACTLY equal to that two-counter finite-state rival (so gradedness stays non-load-bearing),
and (iii) the weighted policy beats the strongest single-counter rival in the informative
regime (eps <= ~0.125, q >= ~0.7) and reverses only at the uninformative boundary.

This runner realises that design AT THE ORGANISM SCALE (engineering only, no protocol, no
freeze). The world is the AC107/AC110 two-cause world -- move (channel-1 mapping flips) vs
cut (route-1 read suppressed) -- with two world changes, both declared and applied uniformly
to every arm:

  1. THE C2 OCCLUSION GATE (q): on a Bernoulli(q) fraction of channel-1 contacts the
     `used_held` bit is occluded (forwarded as 2), so the two causes' signatures -- open
     held-fail (move) vs open blind (cut) -- are hidden and the estimator must fall back to
     the accumulated weak evidence. (Identical to AC110's gate.)

  2. RESIDUAL YIELD (eps): under the move cause a HELD stale entry yields with residual
     probability eps instead of never (the old port retains residual activity). This is the
     one change that makes the two weak LRs genuinely heterogeneous. Implemented by source
     surgery on the frozen contact line: a contact whose held entry misses the flipped
     mapping still calls ac4.react (income) with probability eps. Balance-identity-safe by
     construction -- the same react path fires, only its trigger widens.

The candidate is a MAINTAINED TWO-COUNTER estimate: two integer counters (n_u, n_p) live in
the dead rule's free bits (the AC12/AC96 pattern extended to two low-bit-width counters),
plus a one-bit hold latch (the AC107 estimate bit) for the decisive "open blind -> hold
forever" branch. Weights w_u, w_p and threshold theta are SUPPLIED frozen constants (the
first-order content tier; the learned reliability tier is the deferred next-after, P4 §9).
On every post-cause occluded contact the candidate updates the relevant counter (atomic,
W-gated, Gray-coded, paid) and relinquishes when n_u*w_u + n_p*w_p >= logit(theta). Open
held-fail relinquishes immediately (decisive M); open blind latches hold (decisive C).

The matched rivals (same observation stream, same decisive handling, differing only in the
accumulation):
  - `single_counter`: ONE integer counter (n += 1 unproductive, n += w integer productive,
    clamped >= 0), relinquish at n >= N. The strongest single-integer rival (P4's rival 3).
  - `immediate`: no state at all -- relinquish on any unproductive contact, hold on
    productive/blind. The same-information immediate policy (C4's binary+imm, stripped of
    accumulation).
  - `scramble`: the candidate with the counter READ forced to (0,0) (writes intact) -- the
    read-only causal-role control (AC107's scramble pattern).

Discipline: ENGINEERING ONLY. Decision utility (relinquish/hold correctness, latency) is the
primary endpoint, gated NOT on survival (the P4 handoff). Host-state audit + observer-discard
on the candidate. Interventions verified clean. No gate is moved after seeing a result.
"""

from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import math
import sys
import numpy as np
import ac110
import ac107
import ac106
import ac99_d2
import ac96
import ac95
import ac12
import ac4
import ac71
import ac9
import ac100
import ac5_program as prog

TICKS = ac107.TICKS                  # 16384
DEV = ac107.DEV                      # 512
MOVE_TICK = ac107.MOVE_TICK          # 8192
CUT_TICK = ac107.CUT_TICK            # 8192 (the two causes land at the same tick)
PORTS = ac107.PORTS                  # 4 (blind fallback uniform over {0,1,2,3})
WINDOW = ac107.WINDOW                # 96 (read-cut window)
STREAK_N = ac107.STREAK_N            # 6 (the frozen Gray streak; the candidate does NOT use it)

# ---- declared world constants (the heterogeneous-LR informative regime) ----
Q = 0.7                              # occlusion probability of used_held on channel-1 contacts
EPS = 0.08                           # residual yield of a stale held entry under move (in (0,1/4))
THETA = 0.6                          # the supplied decision threshold (logit = log(THETA/(1-THETA)))
N_U_BITS = 4                         # n_u counter width (0..15)
N_P_BITS = 2                         # n_p counter width (0..3)
SINGLE_W = -6                        # single-counter rival's integer productive weight
SINGLE_N = 4                         # single-counter rival's threshold

ARMS = ('two_counter', 'single_counter', 'immediate', 'scramble')
CONDITIONS = ('no_cause', 'move', 'cut')

ENGINEERING = list(range(8))

SOURCES = ['ac112.py', 'ac110.py', 'ac107.py', 'ac106.py', 'ac99_d2.py', 'ac99.py',
           'ac97.py', 'ac96.py', 'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py',
           'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py',
           'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py']


def weights(eps=EPS):
    """Log-LRs toward M of the two weak (occluded) observations. w_u > 0 > w_p, |w_p|/w_u != 1."""
    w_u = math.log((4.0 / 3.0) * (1.0 - eps))
    w_p = math.log(4.0 * eps)
    return w_u, w_p


def logit(theta):
    return math.log(theta / (1.0 - theta))


# ---------------- the two counters (vulnerable, paid, Gray-coded, in the dead rule's free bits) --
def _gray_encode(n):
    return n ^ (n >> 1)


def _gray_decode(g):
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n


def counter_read(o, offs):
    """Majority read of a Gray-coded counter (LSB first) stored at `offs` (list of bit offsets)."""
    g = 0
    for k, off in enumerate(offs):
        if o.body.traces[0, off].sum() >= ac96.STREAK_THRESHOLD:
            g |= (1 << k)
    return _gray_decode(g)


def counter_write(o, e, offs, new):
    """Atomic, W-gated paid write of a Gray-coded counter to `new` (0..2^len(offs)-1).

    Encodes `new` in Gray, writes only the replicas whose value differs, and refuses the whole
    transition if it exceeds the produced machinery's `ac95._cap`. Returns replicas written.
    """
    offs = np.asarray(offs, dtype=int)
    bits = len(offs)
    if counter_read(o, offs) == new:
        return 0
    g = _gray_encode(new)
    targets = np.array([(g >> k) & 1 for k in range(bits)], dtype=np.uint8)
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
    e['counter_writes'] = e.get('counter_writes', 0) + n
    return n


# ---------------- the hold latch (the AC107 estimate bit; physical 1 = not holding) --------------
def hold_read(o, bel_off):
    """1 = holding (confirmed C), 0 = not holding. Physical bit 0 => holding (inverted)."""
    return int(o.body.traces[0, bel_off].sum() < ac96.STREAK_THRESHOLD)


def hold_write(o, e, holding, bel_off):
    """Paid write of the hold latch. holding=1 writes physical 0, holding=0 writes physical 1."""
    return ac107.bel_write(o, e, 0 if holding else 1, bel_off)


# ---------------- residual yield (source surgery on the frozen contact line) ----------------------
RESIDUAL_LINE = "            if port==mapping[action]: ac4.react(b,action,'self',e)"
RESIDUAL_LINE_NEW = ("            if port==mapping[action] or "
                     "(selected is not None and residual()): ac4.react(b,action,'self',e)")


# ---------------- the build (ac110.build_step minus the repair cut, plus the residual yield) -----
def build_step(alloc, succ, exclude_offs, cfg, cut_obj, gate_rng=None, q=Q,
               residual_rng=None, eps=EPS):
    base, cut = ac71.arm_parts(cfg['ac_arm'])
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['maintain'] = ac95.maintain
    ns['succ'] = succ
    ns['reg_offs'] = exclude_offs
    ns['cfg'] = cfg
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE,
                      ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e,gate_used(selected,action))")
    ns['alloc'] = alloc

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
    assert src.count(RESIDUAL_LINE) == 1, 'frozen contact line changed (residual-yield surgery)'
    src = src.replace(RESIDUAL_LINE, RESIDUAL_LINE_NEW)

    def residual():
        return residual_rng.random() < eps
    ns['residual'] = residual
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
    exec(compile(src, 'ac112_step', 'exec'), ns, fns)
    return fns['step']


# ---------------- the drop (register write + memory expiry, no streak reset) ----------------------
def _drop_no_streak(alloc, o, e, key):
    """The AC75 erase-on-relinquish drop WITHOUT the streak reset (the streak bits are the
    counters on the candidate arms)."""
    place = ac12.m12.slot_of_key(o.memory, key)
    if place is None:
        return
    off = alloc.offs[2 * place[0] + place[1]]
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
    alloc.log['dropped'].append(list(place))
    r, s = place
    live = int((o.memory.life[r, s] > 0).sum())
    if live:
        o.memory.life[r, s] = 0
        o.memory.bits[r, s] = 0
        e['memory_expiry'] += live


# ---------------- the candidate: maintained two-counter accumulator -------------------------------
class TwoCounterAlloc(ac99_d2.GrayAllocEraseReserve):
    """Two integer counters (n_u, n_p) + a one-bit hold latch, all in the dead rule's free bits.

    The counters and latch are the ONLY decision state; every host field is config or an
    observational log (observer-discard safe)."""
    def __init__(self, seed, history, n_u_offs=None, n_p_offs=None, bel_off=None,
                 scramble=False, theta=THETA):
        super().__init__('allocate', seed, history, reserve=False)
        self.n_u_offs = n_u_offs
        self.n_p_offs = n_p_offs
        self.bel_off = bel_off
        self.scramble = scramble
        self.theta = theta
        self.w_u, self.w_p = weights()
        self.counter_events = []   # (tick, kind) observational
        self.hold_events = []      # (tick, kind) observational

    def _n_u(self, o):
        if self.scramble:
            return 0
        return counter_read(o, self.n_u_offs)

    def _n_p(self, o):
        if self.scramble:
            return 0
        return counter_read(o, self.n_p_offs)

    def _holding(self, o):
        if self.scramble:
            return False
        return hold_read(o, self.bel_off)

    def _decide(self, o):
        n_u = self._n_u(o)
        n_p = self._n_p(o)
        return n_u * self.w_u + n_p * self.w_p >= logit(self.theta)

    def _reset(self, o, e):
        counter_write(o, e, self.n_u_offs, 0)
        counter_write(o, e, self.n_p_offs, 0)
        if hold_read(o, self.bel_off):
            hold_write(o, e, 0, self.bel_off)

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if key != 1 or self.now < CUT_TICK:
            # channel 0 never moves/cuts and its streak never advances: nothing to do.
            return
        bound = (o.memory.read(1) is not None)
        used = used_held                  # 0 blind, 1 held, 2 occluded
        prod = e['productive'] > 0

        # ---- decisive discriminator (open observations, any productivity) ----
        if bound and used == 0:
            # open blind while bound -> decisive C (the read is suppressed, entry valid): hold.
            if not hold_read(o, self.bel_off):
                hold_write(o, e, 1, self.bel_off)
                self.hold_events.append((self.now, 'set_hold'))
        elif used == 1 and not prod:
            # open held-fail -> decisive M (the held entry is stale): relinquish now.
            _drop_no_streak(self, o, e, key)
            self._reset(o, e)
            self.counter_events.append((self.now, 'drop_decisive'))

        # ---- consumption ----
        if prod:
            self._restore(o, e, key)
            if not bound:
                self._reset(o, e)          # re-bound: episode over
            elif used == 2:
                counter_write(o, e, self.n_p_offs,
                              min(self._n_p(o) + 1, (1 << N_P_BITS) - 1))   # weak C
            return
        # unproductive
        if not bound or used in (0, 1):
            return                          # re-binding / open blind (hold) / open held (dropped)
        if used == 2:
            if self._holding(o):
                return                      # confirmed C: hold
            counter_write(o, e, self.n_u_offs,
                          min(self._n_u(o) + 1, (1 << N_U_BITS) - 1))       # weak M
            if self._decide(o):
                _drop_no_streak(self, o, e, key)
                self._reset(o, e)
                self.counter_events.append((self.now, 'drop_weighted'))


# ---------------- the single-counter rival -------------------------------------------------------
class SingleCounterAlloc(ac99_d2.GrayAllocEraseReserve):
    """ONE integer counter (n += 1 unproductive, n += w productive, clamped >= 0) + hold latch.

    The strongest single-integer rival (P4 rival 3): it can approximate the optimal weighting
    ratio only by an INTEGER productive weight w, which is the handicap under heterogeneous LRs."""
    def __init__(self, seed, history, n_offs=None, bel_off=None, w=SINGLE_W, n_thr=SINGLE_N):
        super().__init__('allocate', seed, history, reserve=False)
        self.n_offs = n_offs               # 3 bits (0..7)
        self.bel_off = bel_off
        self.w = w
        self.n_thr = n_thr
        self.counter_events = []

    def _n(self, o):
        return counter_read(o, self.n_offs)

    def _holding(self, o):
        return hold_read(o, self.bel_off)

    def _reset(self, o, e):
        counter_write(o, e, self.n_offs, 0)
        if hold_read(o, self.bel_off):
            hold_write(o, e, 0, self.bel_off)

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if key != 1 or self.now < CUT_TICK:
            return
        bound = (o.memory.read(1) is not None)
        used = used_held
        prod = e['productive'] > 0
        if bound and used == 0:
            if not hold_read(o, self.bel_off):
                hold_write(o, e, 1, self.bel_off)
        elif used == 1 and not prod:
            _drop_no_streak(self, o, e, key)
            self._reset(o, e)
            self.counter_events.append((self.now, 'drop_decisive'))
        if prod:
            self._restore(o, e, key)
            if not bound:
                self._reset(o, e)
            elif used == 2:
                counter_write(o, e, self.n_offs, max(self._n(o) + self.w, 0))
            return
        if not bound or used in (0, 1):
            return
        if used == 2:
            if self._holding(o):
                return
            counter_write(o, e, self.n_offs, min(self._n(o) + 1, (1 << 3) - 1))
            if self._n(o) >= self.n_thr:
                _drop_no_streak(self, o, e, key)
                self._reset(o, e)
                self.counter_events.append((self.now, 'drop_threshold'))


# ---------------- the immediate rival (no maintained state) --------------------------------------
class ImmediateAlloc(ac99_d2.GrayAllocEraseReserve):
    """No state at all: relinquish on any unproductive channel-1 contact, hold on productive/blind.

    The same-information immediate policy (C4's binary+imm with accumulation removed)."""
    def __init__(self, seed, history):
        super().__init__('allocate', seed, history, reserve=False)

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if key != 1 or self.now < CUT_TICK:
            return
        bound = (o.memory.read(1) is not None)
        used = used_held
        prod = e['productive'] > 0
        if not bound:
            return
        if used == 0 or prod:
            return                          # open blind (decisive C) or productive: hold
        _drop_no_streak(self, o, e, key)    # unproductive (held-fail or occluded): relinquish now


# ---------------- the run core -------------------------------------------------------------------
def _condition_params(condition):
    if condition == 'move':
        return [(MOVE_TICK, 'flip')], None, 0, 0
    if condition == 'cut':
        return [], 1, CUT_TICK, CUT_TICK + WINDOW
    return [], None, 0, 0          # no_cause


def _make_alloc(arm, seed, history, n_u_offs, n_p_offs, n_offs, bel_off):
    if arm == 'two_counter':
        return TwoCounterAlloc(seed, history, n_u_offs=n_u_offs, n_p_offs=n_p_offs,
                               bel_off=bel_off, scramble=False)
    if arm == 'scramble':
        return TwoCounterAlloc(seed, history, n_u_offs=n_u_offs, n_p_offs=n_p_offs,
                               bel_off=bel_off, scramble=True)
    if arm == 'single_counter':
        return SingleCounterAlloc(seed, history, n_offs=n_offs, bel_off=bel_off)
    if arm == 'immediate':
        return ImmediateAlloc(seed, history)
    raise ValueError(arm)


def _true_cause(condition):
    if condition == 'cut':
        return 0                  # C (hold is correct)
    if condition == 'move':
        return 1                  # M (relinquish is correct)
    return None


def _run_core(seed, history, arm, condition, record_trace=False, ports=PORTS,
              q=Q, eps=EPS, theta=THETA, swap_at=None):
    ac12.PORTS = ports; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    streak_offs = ac96.streak_offsets(o)
    n_u_offs = streak_offs[0:4]            # 4 bits (word 5,7,8,9)
    n_p_offs = streak_offs[4:6]            # 2 bits (word 11,13)
    n_offs = streak_offs[0:3]              # 3 bits (single counter)
    bel_off = ac107.bel_offset(o)
    alloc = _make_alloc(arm, seed, history, n_u_offs, n_p_offs, n_offs, bel_off)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    alloc.streak_offs = streak_offs
    if isinstance(alloc, TwoCounterAlloc):
        alloc.theta = theta
        alloc.w_u, alloc.w_p = weights(eps)
    reg_offs = ac95.resolve_offsets(o)
    exclude_offs = reg_offs + streak_offs + [bel_off]
    encoded = ac95.description_bits(priority)
    o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
    cfg = dict(ac95.ARM_PARTS['gated'])
    cfg['reserve'] = False
    succ = ac95.Succession('real', encoded)
    schedule, cut_key, cut_start, cut_end = _condition_params(condition)
    cut_obj = ac106.ReadCut(cut_key, cut_start, cut_end)
    gate_rng = np.random.default_rng([seed, 1809])
    residual_rng = np.random.default_rng([seed, 2009])
    step = build_step(alloc, succ, exclude_offs, cfg, cut_obj, gate_rng=gate_rng, q=q,
                      residual_rng=residual_rng, eps=eps)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    for k in ('reg_writes', 'succ_writes', 'ctrl_writes', 'timer_increments', 'timer_resets',
              'split_events', 'streak_writes', 'bel_writes', 'proactive_writes',
              'counter_writes', 'hold_writes'):
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
    route1_bound_at_cut_end = None
    swap_applied = False
    for t in range(TICKS):
        alloc.now = t
        cut_obj.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = _make_alloc(arm, seed, history, n_u_offs, n_p_offs, n_offs, bel_off)
            alloc.streak_offs = streak_offs
            alloc.offs = offs
            alloc.shadow = o.body.traces[0].copy()
            alloc.now = t
            if isinstance(alloc, TwoCounterAlloc):
                alloc.theta = theta
                alloc.w_u, alloc.w_p = weights(eps)
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
                route1_bound_at_cut_end = o.memory.read(1) is not None
            if CUT_TICK <= t < CUT_TICK + WINDOW and entry_life_at_cut_start is not None \
                    and ac12.m12.slot_of_key(o.memory, 1) is None:
                entry_expired_during_cut = True
        if record_trace:
            trace.append((t, o.digest()))
        if first_dead is None and o.body.dead:
            first_dead = t
    n_u_final = counter_read(o, n_u_offs)
    n_p_final = counter_read(o, n_p_offs)
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
                reacquire_ticks=reacquire_ticks,
                n_u=n_u_final, n_p=n_p_final,
                holding=hold_read(o, bel_off),
                counter_events=getattr(alloc, 'counter_events', []),
                hold_events=getattr(alloc, 'hold_events', []),
                entry_life_at_cut_start=entry_life_at_cut_start,
                entry_life_at_cut_end=entry_life_at_cut_end,
                entry_expired_during_cut=entry_expired_during_cut,
                route1_bound_at_cut_end=route1_bound_at_cut_end,
                swap_applied=swap_applied,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                counter_writes=int(total['counter_writes']),
                memory_writes=int(total['memory_writes']),
                state_hash=o.digest()), o, trace


def run(seed, history, arm, condition, ports=PORTS, record_trace=False, q=Q, eps=EPS,
        theta=THETA):
    row, o, _ = _run_core(seed, history, arm, condition, record_trace=record_trace,
                          ports=ports, q=q, eps=eps, theta=theta)
    return row


# ---------------- observer-discard (state sufficiency, on the candidate) -------------------------
def observer_discard_equivalence(seed, history, condition='cut', swap_tick=None):
    """Per-tick observer-discard on the candidate: at `swap_tick` the succession observer AND the
    alloc (clearing its observational logs) are replaced with fresh objects; the trajectory must be
    byte-identical at EVERY tick. The counters and hold latch live in maintained state."""
    if swap_tick is None:
        swap_tick = CUT_TICK + WINDOW // 2
    base, base_o, base_trace = _run_core(seed, history, 'two_counter', condition, record_trace=True)
    swapped, swapped_o, swapped_trace = _run_core(seed, history, 'two_counter', condition,
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


# ---------------- host-field audit (no steering host state on the candidate) --------------------
def audit_host_fields():
    cfg_fields = {'n_u_offs', 'n_p_offs', 'n_offs', 'bel_off', 'scramble', 'theta', 'w_u', 'w_p',
                  'w', 'n_thr', 'arm', 'now', 'offs', 'streak_offs', 'rng', 'reserve'}
    observational = {'counter_events', 'hold_events', 'log', 'shadow', 'streak_events',
                     'reserve_events'}
    return dict(
        candidate_config_host_fields=sorted(cfg_fields),
        candidate_observational_host_fields=sorted(observational),
        note='no host field steers a write: n_u/n_p are read from traces[0, streak_offs] '
             '(Gray majority), the hold latch from traces[0, bel_off] (majority); the weights and '
             'threshold are supplied constants; counter_events/hold_events/log are observational. '
             'Observer-discard equivalence is the dynamic proof.',
    )


# ---------------- measurements (engineering, not a frozen gate set) ------------------------------
def _by(rows):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
    return by


def summarize(rows, seeds):
    by = _by(rows)
    inds = [(s, h) for s in seeds for h in (0, 1)]
    n_ind = len(inds)

    def survives(r):
        return r['completed'] and r['first_dead'] is None

    # decision utility: move -> relinquish (correct), cut -> hold (no relinquish, correct).
    tc = lambda s, h, c, a: by[(s, h, c)][a]
    move_relinq = {a: [tc(s, h, 'move', a)['relinquishments'] >= 1 for s, h in inds] for a in ARMS}
    cut_relinq = {a: [tc(s, h, 'cut', a)['relinquishments'] >= 1 for s, h in inds] for a in ARMS}
    cut_hold = {a: [tc(s, h, 'cut', a)['route1_bound_at_cut_end'] for s, h in inds] for a in ARMS}
    move_drop_tick = {a: [min((t for t, _p, _r in tc(s, h, 'move', a)['drop_ticks']), default=None)
                          for s, h in inds] for a in ARMS}
    survival = {a: {c: sum(survives(tc(s, h, c, a)) for s, h in inds) for c in CONDITIONS}
                for a in ARMS}
    m = {
        'move_relinquishes': {a: (sum(v), n_ind) for a, v in move_relinq.items()},
        'cut_false_relinquishes': {a: (sum(v), n_ind) for a, v in cut_relinq.items()},
        'cut_holds_route': {a: (sum(v), n_ind) for a, v in cut_hold.items()},
        'move_first_drop_tick': {a: [None if x is None else int(x) for x in v]
                                 for a, v in move_drop_tick.items()},
        'survival': survival,
        'weights': dict(w_u=round(weights()[0], 4), w_p=round(weights()[1], 4),
                        theta=THETA, q=Q, eps=EPS),
        'counter_writes_cut': {a: sorted({tc(s, h, 'cut', a)['counter_writes'] for s, h in inds})
                               for a in ARMS},
    }
    return m


# ---------------- collectors ---------------------------------------------------------------------
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
                 r['relinquishments'], r['routes'], r['n_u'], r['n_p'], r['holding'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    obs = {f'{s}/{h}': observer_discard_equivalence(s, h, 'cut') for s in seeds for h in (0, 1)}
    audit = audit_host_fields()
    m = summarize(rows, seeds)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), Q=Q, EPS=EPS,
             THETA=THETA, N_U_BITS=N_U_BITS, N_P_BITS=N_P_BITS, SINGLE_W=SINGLE_W,
             SINGLE_N=SINGLE_N, rows=rows, measurements=m, observer_discard=obs,
             host_field_audit=audit),
        indent=2, default=str))
    print(json.dumps(dict(measurements=m), indent=2, default=str))
    print(json.dumps(dict(observer_discard={k: (v.get('per_tick_identical'), v.get('first_div'))
                                            for k, v in obs.items()}), indent=2, default=str))
    return rows, m, obs


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac112_engineering_v1', ENGINEERING)
        return
    if '--smoke' in sys.argv:
        collect_engineering('ac112_smoke_v1', [0, 1, 2])
        return
    if '--sweep' in sys.argv:
        sweep('ac112_sweep_v1', [0, 1, 2, 3])
        return
    print('AC112: --engineering (seeds 0-7), --smoke (0-2), or --sweep (0-3).')


def sweep(root, seeds):
    """Engineering parameter screen: the two-counter's theta grid vs the single-counter's
    (w, N) grid, on the decision-utility endpoints (move relinquish rate, cut false-relinquish
    rate). This is the 'sweep the rival family AND your learner's parameters' check (AC11's rule)
    -- it shows the arms DISCRIMINATE, not that any one configuration wins."""
    thetas = [0.5, 0.6, 0.7, 0.8, 0.9]
    single_grid = [(-6, 4), (-6, 2), (-4, 4), (-2, 2), (0, 1)]
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for theta in thetas:
                for cond in ('move', 'cut'):
                    r = run(seed, 0, 'two_counter', cond, theta=theta)
                    r['param'] = f'theta={theta}'
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            for (w, n_thr) in single_grid:
                for cond in ('move', 'cut'):
                    r = _run_single(seed, 0, cond, w=w, n_thr=n_thr)
                    r['param'] = f'w={w},N={n_thr}'
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, sweep=[
                (r['param'], r['condition'], r['relinquishments'], r['routes'])
                for r in rows[-2 * (len(thetas) + len(single_grid)):]]), default=str), flush=True)
    table = {}
    for r in rows:
        key = (r['param'], r['condition'])
        table.setdefault(key, []).append(r['relinquishments'] >= 1)
    summary = {}
    for (param, cond), v in sorted(table.items()):
        summary.setdefault(param, {})[cond] = (sum(v), len(v))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), thetas=thetas, single_grid=single_grid, summary=summary,
             rows=rows), indent=2, default=str))
    print(json.dumps(dict(sweep_summary=summary), indent=2, default=str))
    return summary


def _run_single(seed, history, condition, w, n_thr):
    """Run the single-counter rival with an explicit (w, N)."""
    ac12.PORTS = PORTS; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    streak_offs = ac96.streak_offsets(o)
    n_offs = streak_offs[0:3]
    bel_off = ac107.bel_offset(o)
    alloc = SingleCounterAlloc(seed, history, n_offs=n_offs, bel_off=bel_off, w=w, n_thr=n_thr)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    alloc.streak_offs = streak_offs
    reg_offs = ac95.resolve_offsets(o)
    exclude_offs = reg_offs + streak_offs + [bel_off]
    encoded = ac95.description_bits(priority)
    o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
    cfg = dict(ac95.ARM_PARTS['gated'])
    cfg['reserve'] = False
    succ = ac95.Succession('real', encoded)
    schedule, cut_key, cut_start, cut_end = _condition_params(condition)
    cut_obj = ac106.ReadCut(cut_key, cut_start, cut_end)
    gate_rng = np.random.default_rng([seed, 1809])
    residual_rng = np.random.default_rng([seed, 2009])
    step = build_step(alloc, succ, exclude_offs, cfg, cut_obj, gate_rng=gate_rng, q=Q,
                      residual_rng=residual_rng, eps=EPS)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    for k in ('reg_writes', 'succ_writes', 'ctrl_writes', 'counter_writes'):
        total[k] = 0
    first_dead = None
    drop_ticks = []
    for t in range(TICKS):
        alloc.now = t
        cut_obj.now = t
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
        step.__globals__['now'] = t
        prev_drops = len(alloc.log['dropped'])
        e = step(o, core, noise, directions, coin,
                 tuple(ac100.mapping_at(base_map, t, schedule)), [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if len(alloc.log['dropped']) > prev_drops:
            place = alloc.log['dropped'][-1]
            drop_ticks.append((t, list(place), ac12.bit_value(o, offs[2 * place[0] + place[1]])))
        if first_dead is None and o.body.dead:
            first_dead = t
    return dict(seed=seed, history=history, arm='single_counter', condition=condition,
                completed=total['active'] == TICKS, first_dead=first_dead,
                routes=[o.memory.read(k) for k in (0, 1)],
                relinquishments=len(alloc.log['dropped']),
                drop_ticks=drop_ticks, state_hash=o.digest())


if __name__ == '__main__':
    main()

