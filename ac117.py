"""AC117 (M6): the estimator-monitoring feasibility harness -- does a maintained monitor
state m track the damage-component wrongness of the first-order cause estimate e, add value
beyond simpler rivals, and causally influence maintenance?

Parent: M5 (t_7e673e39), which froze the harness design (M5_MONITOR_HARNESS_DESIGN_v1.md).
Predecessor M4 (t_6145d172) returned the identifiability verdict this design is conditioned on:
the referent "P(decoded e wrong)" splits by observability -- only the DAMAGE component is
identifiable (staleness is an unavoidable miss, the pure decision window has no error variance).

The world is the AC110 cut condition, post-window damage regime [8288, 16384). The first-order
machinery is the AC110 GatedEstimator (C2 occluded-used_held gate q=0.5, the discriminator that
writes e on open contacts, the frozen streak/hold consumption). Arms differ ONLY in the
maintenance policy of e.

The monitor m:
  - SUBSTRATE: the retained write-value (last bel_write direction), stored in the dead rule's
    action bit 2 (word bit 12), a free '1' bit acquired as 1 = "retained E_world", written 0 =
    "retained E_machinery" under cut. Distinct from bel_off (word bit 10) and the streak free bits
    (word bits 5,7,8,9,11,13). Majority-read, W-gated paid writes, IN the program damage stream
    (sticky-SET 0->1), repaired by action 2's bank-0 majority-restore, excluded from
    reg_from_active (decision state, not program content).
  - INPUTS: (1) directioned count ones at bel_off; (2) retained write-value m_off; (3) shared
    obs bit 2 + resource signals (W<2 / material<=64 / fuel<=8 / _cap refusal), repair_at_risk
    DERIVED from the resource signals.
  - READOUT r in {0,1,2,3}: r = min(3, ones) when last_write==0 else 0; case 4 (repair_at_risk)
    contributes r=3 even when ones<=3. Categorical: unreliable iff (last_write==0 AND ones>=4)
    OR (last_write==0 AND repair_at_risk).
  - CONTROL (H2): when unreliable, a targeted per-bit repair of bel_off toward the retained
    value (write the flipped replicas back to 0), W-gated by ac95._cap.

Design interpretation recorded here (M5 'whether they store m'): the direction record m_off is
written by the SHARED discriminator in every arm (it is the discriminator's own conclusion, a
substrate record that survives observer-discard); the arms differ in whether they READ it for
control -- only `monitor` consumes m_off. This is required so H1 (the monitor readout scored on
the fixed_duty trajectory) is well-defined from substrate.

Five arms (maintenance policy of e; all share action 2's frozen bank-0 repair):
  - monitor   : readout m; targeted repair toward the retained value when unreliable.
  - fixed_duty: state-blind; majority-restore e on a fixed schedule (spend-matched to monitor).
  - reflex    : the obs-bit-2 watchdog; action 2 only (== AC110 `maintained`). The correct null.
  - direct    : readout ones>=4 (no retained direction); majority-restore (cements, no fix).
  - history   : state-blind to e; a corruption-event counter; majority-restore on threshold.

Discipline: engineering first (non-vacuity, spend-match, causal-role), then a hashed protocol,
then disjoint finals. Negative results are preserved; no gate is moved after seeing the result.
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
import ac99_d2
import ac96
import ac95
import ac12
import ac4
import ac71
import ac9
import ac100
import ac5_program as prog

bel_read = ac107.bel_read
bel_offset = ac107.bel_offset

TICKS = ac110.TICKS                  # 16384
DEV = ac110.DEV                      # 512
MOVE_TICK = ac110.MOVE_TICK          # 8192
CUT_TICK = ac110.CUT_TICK            # 8192 (the two causes land at the same tick)
PORTS = ac110.PORTS                  # 4
WINDOW = ac110.WINDOW                # 96 (read-cut window)
STREAK_N = ac110.STREAK_N            # 6

POST_WINDOW = CUT_TICK + WINDOW      # 8288 -- the damage regime's start

Q = 0.5                              # C2 occlusion probability (the AC110 anchor)
BEL_DAMAGE = 0.01                    # declared elevated damage on the estimate bit (the M5 §8.3
                                     # diagnostic: at ambient 1e-4, case 3 base rate = 0 and the
                                     # harness is vacuous). 0.01 makes e drift so the monitor's
                                     # catch is exercised. Disclosed BEFORE the finals.

ARMS = ('monitor', 'fixed_duty', 'reflex', 'direct', 'history')
CONDITIONS = ('no_cause', 'move', 'cut')

ENGINEERING = list(range(8))                        # disclosed, excluded from finals
FINAL_SEEDS = list(range(6800, 6816))               # 16 fresh disjoint seeds (32 individuals)

# ---- fixed-duty spend-match + history threshold, SELECTED ON THE ENGINEERING COHORT ----
# fixed_duty's spend is discontinuous (preventive majority-restore ~513 @ K=12 vs cementing ~50
# @ K>=20); K=12 is the cheapest state-blind schedule that keeps e correct, ~19% above the
# monitor's ~432 directional spend. history repairs on the corruption-event threshold (a weak
# state-blind rival: its majority-restore cements, it does not keep e correct).
DUTY_PERIOD = 12
HISTORY_THRESHOLD = 2

SOURCES = ['ac117.py', 'ac110.py', 'ac107.py', 'ac106.py', 'ac99_d2.py', 'ac99.py',
           'ac97.py', 'ac96.py', 'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py',
           'ac12_memory.py', 'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py',
           'ac5_program.py', 'ac4.py', 'ac4_transport.py', 'ac1.py',
           'AC117_PROTOCOL_v1.md']


# ---------------- the monitor's retained write-value (word bit 12 of the dead rule) ----------------
def m_offset(o):
    """The retained write-value bit: action bit 2 (word bit 12) of the dead rule. Acquired 1 =
    'retained E_world'; written 0 = 'retained E_machinery' under cut. Distinct from bel_off
    (word bit 10) and the streak free bits (word bits 5,7,8,9,11,13)."""
    return 14 * ac12.dead_rule_index(o) + 12


def m_read(o, m_off):
    """Majority read (>=4 of 7). 1 = retained E_world direction, 0 = retained E_machinery."""
    return int(o.body.traces[0, m_off].sum() >= 4)


def m_write(o, e, val, m_off):
    """Atomic, W-gated paid write of the retained write-value to `val` (<=7 replicas)."""
    b = o.body
    sites = np.argwhere(b.traces[0, m_off] != val)
    n = len(sites)
    if n == 0:
        return 0
    cap = ac95._cap(b)
    if n > cap:
        return 0
    b.traces[0, m_off, sites[:, 0]] = val
    b.energy -= n
    b.material -= n
    e['spent_e'] += n
    e['spent_m'] += n
    e['writes'] += n
    e['m_writes'] = e.get('m_writes', 0) + n
    return n


# ---------------- shared signal primitives (re-derived from substrate, never host logs) ------------
def obs_bit2(o):
    """The frozen whole-bank corruption observation (ac9.observe line 56)."""
    ones = o.body.traces[0, :126].sum(axis=1)
    return int(np.minimum(ones, 7 - ones).sum() >= 4)


def repair_at_risk(o, bel_off):
    """The derived leading indicator (M4 section 2b): repair is about to be refused. W<2 / obs
    bit 6, material<=64 / obs bit 1, fuel<=8 / obs bit 0, or ac95._cap would refuse the needed
    e-repair write (ones replicas)."""
    b = o.body
    ones = int(b.traces[0, bel_off].sum())
    W = int(ac4.available(b)[:4].sum())
    return (W < 2) or (b.material <= 64) or (b.fuel <= 8) or (ac95._cap(b) < ones)


def readout_monitor(o, m_off, bel_off):
    """m's readout: (unreliable, graded_r)."""
    ones = int(o.body.traces[0, bel_off].sum())
    last_write = m_read(o, m_off)
    risk = repair_at_risk(o, bel_off)
    unreliable = (last_write == 0 and ones >= 4) or (last_write == 0 and risk)
    if last_write == 1:
        r = 0
    elif risk:
        r = 3
    else:
        r = min(3, ones)
    return unreliable, r


def readout_reflex(o):
    """The obs-bit-2 reflex readout: unreliable iff obs bit 2 fires."""
    ob = obs_bit2(o)
    return bool(ob), (1 if ob else 0)


def readout_direct(o, bel_off):
    """The transient direct readout: unreliable iff ones >= 4 (no retained direction)."""
    ones = int(o.body.traces[0, bel_off].sum())
    return (ones >= 4), min(3, ones)


# ---------------- targeted per-bit repair of e (the monitor's control primitive) -------------------
def erepair(o, e, target, bel_off):
    """Targeted paid repair of bel_off toward `target`, W-gated by ac95._cap. NOT action 2's
    whole-bank restore: a single estimate bit contributes at most 3 minority replicas and can
    never trigger obs bit 2 (AC110 rule 1)."""
    b = o.body
    sites = np.argwhere(b.traces[0, bel_off] != target)
    n = min(ac95._cap(b), len(sites))
    if n == 0:
        return 0
    idx = sites[:n]
    b.traces[0, bel_off, idx[:, 0]] = target
    b.energy -= n
    b.material -= n
    e['spent_e'] += n
    e['spent_m'] += n
    e['writes'] += n
    e['erepair_writes'] = e.get('erepair_writes', 0) + n
    return n


# ---------------- the monitored estimator (shared discriminator + m_off tracking + policy) ---------
class MonitoredEstimator(ac110.GatedEstimator):
    """The AC110 GatedEstimator extended with the direction record (m_off) and the per-arm
    maintenance policy of e. The discriminator writes BOTH e and m_off (the shared direction
    record); the arm policy determines the per-tick maintenance of e.

    scramble_e maps to the base `scramble` (force e's DECISION read to 1, writes intact) -- the
    decision-direction causal control. scramble_m forces the monitor READOUT to reliable (so the
    targeted repair never fires) -- the maintenance-direction causal control."""

    def __init__(self, seed, history, bel_off=None, m_off=None, arm='monitor',
                 duty_period=None, history_threshold=None, scramble_m=False, scramble_e=False):
        super().__init__(seed, history, bel_off=bel_off, estimate=True,
                         proactive=True, scramble=scramble_e)
        self.m_off = m_off
        self.policy = arm
        self.scramble_m = scramble_m
        self.duty_period = duty_period
        self.history_threshold = history_threshold
        self.duty_counter = 0
        self.corrupt_counter = 0
        self.last_key = None
        self.repair_events = []       # (tick, kind, replicas) observational

    # the discriminator also records the direction (shared across all arms)
    def _bel_write(self, o, e, val):
        n, attempted, refused = super()._bel_write(o, e, val)
        m_write(o, e, val, self.m_off)
        return n, attempted, refused

    def outcome(self, o, key, e, used_held=None):
        self.last_key = int(key)
        super().outcome(o, key, e, used_held)

    def readout(self, o):
        if self.scramble_m:
            return False, 0
        return readout_monitor(o, self.m_off, self.bel_off)

    def monitor_tick(self, o, e):
        """Per-tick maintenance of e, dispatched by arm. Fired AFTER the damage stream, BEFORE
        action selection (injected alongside ac95.maintain)."""
        bel = bel_read(o, self.bel_off)          # the majority (decode) value of e
        ones = int(o.body.traces[0, self.bel_off].sum())
        if self.policy == 'monitor':
            unreliable, _ = self.readout(o)
            if unreliable:
                target = m_read(o, self.m_off)   # repair toward the retained direction
                n = erepair(o, e, target, self.bel_off)
                if n:
                    self.repair_events.append((self.now, 'monitor_repair', n))
        elif self.policy == 'fixed_duty':
            self.duty_counter += 1
            if self.duty_counter >= self.duty_period:
                n = erepair(o, e, bel, self.bel_off)
                self.duty_counter = 0
                if n:
                    self.repair_events.append((self.now, 'fixed_duty_repair', n))
        elif self.policy == 'reflex':
            pass                                 # action 2 (frozen) only
        elif self.policy == 'direct':
            if ones >= 4:
                n = erepair(o, e, bel, self.bel_off)   # majority-restore: cements, no fix
                if n:
                    self.repair_events.append((self.now, 'direct_repair', n))
        elif self.policy == 'history':
            if obs_bit2(o):
                self.corrupt_counter += 1
            if self.corrupt_counter >= self.history_threshold:
                n = erepair(o, e, bel, self.bel_off)
                self.corrupt_counter = 0
                if n:
                    self.repair_events.append((self.now, 'history_repair', n))
        else:
            raise ValueError(self.policy)


# ---------------- the build (ac110.build_step + the monitor per-tick hook) -------------------------
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
    src = src.replace(ac95.ACTION_LINE,
                      "        maintain(o,e,succ,reg_offs,cfg,now)\n"
                      "        alloc.monitor_tick(o,e)\n" + ac95.ACTION_LINE)
    assert src.count(ac95.BALANCE_LINE) == 1
    src = src.replace(ac95.BALANCE_LINE,
                      "    e['writes']+=e.get('reg_writes',0)+e.get('succ_writes',0)+e.get('ctrl_writes',0)\n"
                      + ac95.BALANCE_LINE)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac110.react_skip_estimate(skip_est, bel_off)
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    ns['now'] = 0
    fns = {}
    exec(compile(src, 'ac117_step', 'exec'), ns, fns)
    return fns['step']


# ---------------- the run core ---------------------------------------------------------------------
def _condition_params(condition):
    return ac110._condition_params(condition)


def _true_cause(condition):
    if condition == 'cut':
        return 0
    if condition == 'move':
        return 1
    return None


def _make_alloc(arm, seed, history, bel_off, m_off, duty_period, history_threshold,
                scramble_m=False, scramble_e=False):
    return MonitoredEstimator(seed, history, bel_off=bel_off, m_off=m_off, arm=arm,
                              duty_period=duty_period, history_threshold=history_threshold,
                              scramble_m=scramble_m, scramble_e=scramble_e)


def _run_core(seed, history, arm, condition, record_trace=False, ports=PORTS, q=Q,
              duty_period=DUTY_PERIOD, history_threshold=HISTORY_THRESHOLD,
              scramble_m=False, scramble_e=False, bel_damage=0.0, swap_at=None):
    ac12.PORTS = ports; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    bel_off = ac107.bel_offset(o)
    m_off = m_offset(o)
    skip_est = False                      # every arm keeps action 2's bank-0 repair (the shared
                                          # baseline); the arm policy adds e-specific repair
    alloc = _make_alloc(arm, seed, history, bel_off, m_off, duty_period, history_threshold,
                        scramble_m=scramble_m, scramble_e=scramble_e)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    streak_offs = ac96.streak_offsets(o)
    alloc.streak_offs = streak_offs
    reg_offs = ac95.resolve_offsets(o)
    build_offs = reg_offs + streak_offs + [bel_off, m_off]   # m_off is decision state: excluded
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
              'split_events', 'streak_writes', 'bel_writes', 'proactive_writes',
              'erepair_writes', 'm_writes'):
        total[k] = 0
    first_dead = None
    drop_ticks = []
    restore_ticks = []
    trace = [] if record_trace else None
    was_bound = {0: False, 1: False}
    seen_bound = {0: False, 1: False}
    reacquire_ticks = {0: [], 1: []}
    bel_wrong_ever = 0
    bel_wrong_in_window = 0
    first_wrong_read = None
    true_cause = _true_cause(condition)
    swap_applied = False
    income_post = 0
    post_window_ticks = 0
    post_window_bound = 0
    # H1 bookkeeping (per tick, t >= CUT_TICK): recorded only for the fixed_duty arm
    h1 = [] if (arm == 'fixed_duty' and condition != 'no_cause') else None
    for t in range(TICKS):
        alloc.now = t
        cut_obj.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = _make_alloc(arm, seed, history, bel_off, m_off, duty_period,
                                history_threshold, scramble_m=scramble_m, scramble_e=scramble_e)
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
        # ---- declared elevated damage on the estimate bit (the M5 §8.3 diagnostic) ----
        if bel_damage > 0:
            bel_flips = (bel_rng.random(7) < bel_damage).astype(np.uint8)
            o.body.traces[0, bel_off] |= bel_flips
        step.__globals__['now'] = t
        prev_drops = len(alloc.log['dropped'])
        prev_restores = len(alloc.log.get('restored', []))
        e = step(o, core, noise, directions, coin,
                 tuple(ac100.mapping_at(base_map, t, schedule)), [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        contact1 = (getattr(alloc, 'last_key', None) == 1)
        inc = int(e.get('in_m', 0)) + int(e.get('in_f', 0))
        if t >= POST_WINDOW:
            income_post += inc
            post_window_ticks += 1
            if o.memory.read(1) is not None:
                post_window_bound += 1
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
        if true_cause is not None and t >= CUT_TICK and bel_read(o, bel_off) != true_cause:
            bel_wrong_ever += 1
            if first_wrong_read is None:
                first_wrong_read = t
        if true_cause is not None and CUT_TICK <= t < CUT_TICK + WINDOW \
                and bel_read(o, bel_off) != true_cause:
            bel_wrong_in_window += 1
        if h1 is not None and t >= CUT_TICK:
            ones = int(o.body.traces[0, bel_off].sum())
            last_write = m_read(o, m_off)
            ob2 = obs_bit2(o)
            risk = repair_at_risk(o, bel_off)
            wrong = int(bel_read(o, bel_off) != true_cause)
            h1.append((t, ones, last_write, ob2, risk, wrong, int(contact1)))
        if record_trace:
            trace.append((t, o.digest()))
        if first_dead is None and o.body.dead:
            first_dead = t
    bel_at_horizon = bel_read(o, bel_off)
    inv = ac4.inventory(o.body)
    row = dict(seed=seed, history=history, arm=arm, condition=condition,
               ticks=TICKS, completed=total['active'] == TICKS, first_dead=first_dead,
               routes=[o.memory.read(k) for k in (0, 1)],
               demand=o.memory.demand().tolist(),
               register=[ac12.bit_value(o, off) for off in offs],
               relinquishments=len(alloc.log['dropped']),
               restorations=len(alloc.log.get('restored', [])),
               drop_ticks=drop_ticks,
               restore_ticks=restore_ticks,
               reacquire_ticks=reacquire_ticks,
               bel=bel_read(o, bel_off),
               bel_at_horizon=bel_at_horizon,
               bel_wrong_ever=bel_wrong_ever,
               bel_wrong_in_window=bel_wrong_in_window,
               first_wrong_read=first_wrong_read,
               m_final=m_read(o, m_off),
               post_window_bound=post_window_bound,
               post_window_ticks=post_window_ticks,
               route1_retention=(post_window_bound / post_window_ticks) if post_window_ticks else 0.0,
               income_post=income_post,
               swap_applied=swap_applied,
               W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
               energy=inv[0], material=inv[1], fuel=inv[2],
               writes=int(total['writes']), reg_writes=int(total['reg_writes']),
               succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
               streak_writes=int(total['streak_writes']),
               bel_writes=int(total['bel_writes']),
               proactive_writes=int(total['proactive_writes']),
               erepair_writes=int(total['erepair_writes']),
               m_writes=int(total['m_writes']),
               memory_writes=int(total['memory_writes']),
               repair_events=getattr(alloc, 'repair_events', []),
               state_hash=o.digest())
    if h1 is not None:
        row['h1_series'] = h1
    return row, o, trace


def run(seed, history, arm, condition, ports=PORTS, record_trace=False, q=Q,
        duty_period=DUTY_PERIOD, history_threshold=HISTORY_THRESHOLD,
        scramble_m=False, scramble_e=False, bel_damage=BEL_DAMAGE):
    row, o, _ = _run_core(seed, history, arm, condition, record_trace=record_trace,
                          ports=ports, q=q, duty_period=duty_period,
                          history_threshold=history_threshold, scramble_m=scramble_m,
                          scramble_e=scramble_e, bel_damage=bel_damage)
    return row


# ---------------- clean control: all five arms byte-identical in no_cause/move ---------------------
def clean_control_identity(seed, history, condition, q=Q, duty_period=DUTY_PERIOD,
                           history_threshold=HISTORY_THRESHOLD):
    hashes = [run(seed, history, arm, condition, q=q, duty_period=duty_period,
                  history_threshold=history_threshold)['state_hash'] for arm in ARMS]
    return len(set(hashes)) == 1


# ---------------- collectors -----------------------------------------------------------------------
def preflight(protocol='AC117_PROTOCOL_v1.md'):
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


def collect(root, seeds, conditions=None, do_preflight=False, q=Q,
            duty_period=DUTY_PERIOD, history_threshold=HISTORY_THRESHOLD,
            bel_damage=BEL_DAMAGE, finals=False):
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
                        r = run(seed, history, arm, cond, q=q, duty_period=duty_period,
                                history_threshold=history_threshold, bel_damage=bel_damage)
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['bel_at_horizon'], r['bel_wrong_ever'],
                 r['erepair_writes'], round(r['route1_retention'], 3))
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    clean = {}
    if do_preflight:
        clean = {f'{s}/{h}/{c}': clean_control_identity(s, h, c, q=q, duty_period=duty_period,
                                                        history_threshold=history_threshold)
                 for s in seeds for h in (0, 1) for c in ('no_cause', 'move')}
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), PORTS=PORTS,
             Q=q, DUTY_PERIOD=duty_period, HISTORY_THRESHOLD=history_threshold,
             BEL_DAMAGE=bel_damage, POST_WINDOW=POST_WINDOW, rows=rows,
             clean_control=clean, hashes=hashes if do_preflight else None),
        indent=2, default=str))
    print(json.dumps(dict(clean_control=clean, n_rows=len(rows)), indent=2, default=str))
    return rows


def main():
    if '--engineering' in sys.argv:
        collect('ac117_engineering_v1', ENGINEERING,
                duty_period=DUTY_PERIOD, history_threshold=HISTORY_THRESHOLD)
        return
    if '--smoke' in sys.argv:
        collect('ac117_smoke_v1', [0, 1, 2], duty_period=DUTY_PERIOD,
                history_threshold=HISTORY_THRESHOLD)
        return
    if '--finals' in sys.argv:
        collect('ac117_results_v1', FINAL_SEEDS, do_preflight=True, finals=True)
        return
    print('AC117: --engineering (0-7), --smoke (0-2), --finals (6800-6815).')


if __name__ == '__main__':
    main()
