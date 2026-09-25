"""AC116 (C3): does maintained retained history (an accumulated counter) beat the strongest
TUNED memoryless policy at the organism scale, in the pure occluded-`used_held` world (eps=0)?

Parent (C2, t_04ae4ff3): `C2_STORAGE_COMPARISON_v1.md` identified the one storage comparison the
AC109-AC113 arc left open: the POSITIVE direction of the C2 gate's claim. In the occluded-`used_held`
world the current observation `(bound, used_held=occluded, productive=0)` is IDENTICAL across the two
causes (move vs cut) while the correct action differs, so retained history is the only separator.
AC109 ran the UN-gated world (storage inert by construction), AC110/AC111 ran the gated world but only
repair/composition contrasts, and AC112/AC113 ran the eps>0 world with an UNTUNED churning immediate
rival and a CONfounded scramble read. The decisive arm -- a clean, TUNED, hold-on-occluded memoryless
rival in the PURE gated world -- has never been run.

This runner realises that comparison on the AC110 world (the pure C2-gated world, eps=0 -- ac110 has no
residual yield), extended with the counter candidate and its rivals. World: move (channel-1 mapping
flips at t=8192; the route-1 entry is stale -> correct response RELINQUISH) vs cut (route-1 read
suppressed for [8192, 8288); the entry is intact -> correct response HOLD), with the C2 gate occluding
`used_held` on a Bernoulli(q) fraction of channel-1 contacts.

Arms (decision-time information prespecified; the utility measure is post-cause income per channel plus
relinquish latency under move and false-relinquish rate under cut):
  - `counter`  : the sufficient statistic -- ONE integer counter (3 bits, Gray-coded, vulnerable, paid,
                 in the dead rule's free bits) + a one-bit hold latch (the AC107 estimate bit), negative
                 productive weight w, relinquish at counter >= N. This IS retained history.
  - `tuned`    : the strongest MEMORYLESS rival -- a policy over the current triple with ONE free
                 ambiguity parameter p = P(relinquish | occluded-unproductive). Open contacts are forced
                 by the decisive observations (relinquish on open held-fail, hold on open blind/
                 productive); those are not free. p=1 is AC113's churning immediate, p=0 is
                 hold-on-occluded. NO maintained state, NO latch.
  - `estimate` : the one-bit cause estimate (AC107/AC110 GatedEstimator) -- retained history WITHOUT
                 accumulation, the C2 design's original candidate (predicted non-load-bearing). It also
                 serves as the clean-control arm: at q=0.5 it reproduces the frozen AC110 `maintained`
                 arm byte-for-byte (state_hash), licensing the world.
  - `no_write` : the counter with the counter's paid write DISABLED (read honest) -- the AC108
                 direction-1 acquisition cut. Separates "the accumulated value is load-bearing" from
                 "the write machinery is load-bearing".
  - `scramble` : the counter with the counter READ forced to 0 (writes intact) -- the read-only
                 causal-role control (AC107's scramble pattern). Separates "the read content is
                 load-bearing" from "the write machinery is load-bearing".

Repair intervention deliberately OMITTED (C2 §5): the claim is about acquisition (accumulating occluded
evidence), not repair; AC110 already established repair is not load-bearing in-window. Retained-history
dependence (counter vs tuned) is tested SEPARATELY from ongoing-repair dependence (AC110's question,
not re-tested here), so no combined pass/fail label obscures which capability succeeds.

Calibration deliberately OMITTED: the counter is a categorical latch (drop when n >= N), not a
probabilistic confidence estimate, so no confidence score is invented to satisfy a gate (the card's
requirement).

Discipline: engineering first (parameter sweep, disclosed + excluded), then a hashed protocol, then
untouched finals with a seed-level paired sign-flip gate (n=8 seeds, histories aggregated within seed).
A negative comparative result bounds usefulness in the tested task; it does NOT erase any prior
representational finding.
"""

from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np

import ac110
import ac112
import ac107
import ac106
import ac99_d2
import ac96
import ac95
import ac12
import ac4
import ac9
import ac71
import ac100
from ac112 import (counter_read, counter_write, hold_read, hold_write, _drop_no_streak,
                   weights, logit)
import ac5_program as prog

TICKS = ac110.TICKS                  # 16384
DEV = ac110.DEV                      # 512
MOVE_TICK = ac110.MOVE_TICK          # 8192
CUT_TICK = ac110.CUT_TICK            # 8192 (the two causes land at the same tick)
PORTS = ac110.PORTS                  # 4 (blind fallback uniform over {0,1,2,3})
WINDOW = ac110.WINDOW                # 96 (read-cut window)
STREAK_N = ac110.STREAK_N            # 6

# ---- declared world constants (the C2 gated world, PURE: no residual yield) ----
# eps = 0 by construction: ac110's contact line has no residual-yield surgery, so a held stale
# entry yields exactly 0 under move. This is the world C2 §5 names as the clean comparison.
Q_CLEAN = 0.5                        # the AC110 anchor (clean control / world license only)
Q_GRID = [0.7, 0.9]                  # the informative end (the accumulator is load-bearing only
                                     # at high occlusion; C4 rule 3)
EPS = 0.0

# ---- candidate / rival parameter grids (both families swept on engineering -- AC11's rule) ----
# counter: integer productive weight w fixed at -6 (reset-on-productive, the design's "negative
# productive weight"); threshold N swept.
# tuned: ambiguity parameter p swept.
COUNTER_W = -6
N_GRID = [1, 2, 3, 4, 5, 6]
P_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]

ARMS = ('counter', 'tuned', 'estimate', 'no_write', 'scramble')
CONDITIONS = ('no_cause', 'move', 'cut')

ENGINEERING = list(range(8))         # disclosed, excluded from the finals
FINALS = list(range(6600, 6608))     # fresh untouched family (8 seeds x 2 histories)

# Fixed comparison parameters, selected on the ENGINEERING cohort's combined post-cause income
# (disclosed here before the finals; see AC116_PROTOCOL_v1.md).
N_STAR = 4                           # counter threshold (income-maximising)
P_STAR = 1.0                         # tuned ambiguity parameter (income-maximising)

# Frozen source set (the declaration + the simulation code, NOT the verification tools; AC16/17).
SOURCES = ['ac116.py', 'ac110.py', 'ac112.py', 'ac107.py', 'ac106.py', 'ac99_d2.py', 'ac99.py',
           'ac97.py', 'ac96.py', 'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py',
           'ac9.py', 'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py',
           'ac4.py', 'ac4_transport.py', 'ac1.py', 'AC116_PROTOCOL_v1.md']


# ---------------- the counter candidate (single integer counter + hold latch) ----------------
class CounterAlloc(ac99_d2.GrayAllocEraseReserve):
    """ONE integer counter (3 bits, Gray, vulnerable, paid) + a one-bit hold latch, in the dead
    rule's free bits. This is the maintained sufficient statistic (retained history).

    `scramble=True` forces the counter READ to 0 (writes intact) -- the causal-role control.
    `no_write=True` disables the counter's paid write (read honest) -- the acquisition cut.
    The hold latch is the AC107 estimate bit (physical 0 = holding); it is NOT cut by no_write
    (no_write cuts only the accumulation write, the retained-history object under test).
    """

    def __init__(self, seed, history, n_offs=None, bel_off=None, w=COUNTER_W, n_thr=N_STAR,
                 scramble=False, no_write=False):
        super().__init__('allocate', seed, history, reserve=False)
        self.n_offs = n_offs
        self.bel_off = bel_off
        self.w = w
        self.n_thr = n_thr
        self.scramble = scramble
        self.no_write = no_write
        self.counter_events = []    # (tick, kind) observational
        self.hold_events = []       # (tick, kind) observational

    def _n(self, o):
        if self.scramble:
            return 0
        return counter_read(o, self.n_offs)

    def _holding(self, o):
        return hold_read(o, self.bel_off)

    def _write(self, o, e, new):
        if self.no_write:
            return 0
        return counter_write(o, e, self.n_offs, new)

    def _reset(self, o, e):
        self._write(o, e, 0)
        if hold_read(o, self.bel_off):
            hold_write(o, e, 0, self.bel_off)

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if key != 1 or self.now < CUT_TICK:
            return                        # channel 0 never moves/cuts: nothing to do
        bound = (o.memory.read(1) is not None)
        used = used_held                  # 0 blind, 1 held, 2 occluded
        prod = e['productive'] > 0
        # ---- decisive discriminator (open observations, any productivity) ----
        if bound and used == 0:
            # open blind while bound -> decisive C (read suppressed, entry valid): hold.
            if not hold_read(o, self.bel_off):
                hold_write(o, e, 1, self.bel_off)
                self.hold_events.append((self.now, 'set_hold'))
        elif used == 1 and not prod:
            # open held-fail -> decisive M (held entry is stale): relinquish now.
            _drop_no_streak(self, o, e, key)
            self._reset(o, e)
            self.counter_events.append((self.now, 'drop_decisive'))
        # ---- consumption ----
        if prod:
            self._restore(o, e, key)
            if not bound:
                self._reset(o, e)          # re-bound: episode over
            elif used == 2:
                self._write(o, e, max(self._n(o) + self.w, 0))   # weak C (reset)
            return
        if not bound or used in (0, 1):
            return                          # re-binding / open blind (hold) / open held (dropped)
        if used == 2:
            if self._holding(o):
                return                      # confirmed C: hold
            self._write(o, e, min(self._n(o) + 1, (1 << 3) - 1))  # weak M
            if self._n(o) >= self.n_thr:
                _drop_no_streak(self, o, e, key)
                self._reset(o, e)
                self.counter_events.append((self.now, 'drop_threshold'))


# ---------------- the tuned memoryless rival ---------------------------------------------------
class TunedAlloc(ac99_d2.GrayAllocEraseReserve):
    """The strongest MEMORYLESS rival: a policy over the current triple with one free ambiguity
    parameter p = P(relinquish | occluded-unproductive). NO maintained state, NO latch. The open
    contacts are forced by the decisive observations (relinquish on open held-fail, hold on open
    blind/productive). p=1 is AC113's churning immediate, p=0 is hold-on-occluded.
    """

    def __init__(self, seed, history, p=P_STAR):
        super().__init__('allocate', seed, history, reserve=False)
        self.p = p
        self.coin = np.random.default_rng([seed, history, 7777])
        self.tuned_events = []        # (tick, kind) observational

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
            return                          # re-binding: wait for the deposit path
        if prod:
            self._restore(o, e, key)
            return                          # productive: hold
        if used == 0:
            return                          # open blind: hold (decisive C)
        if used == 1:
            _drop_no_streak(self, o, e, key)  # open held-fail: relinquish (decisive M)
            self.tuned_events.append((self.now, 'drop_open_held'))
            return
        # used == 2 (occluded-unproductive): the one free ambiguity response
        if self.coin.random() < self.p:
            _drop_no_streak(self, o, e, key)
            self.tuned_events.append((self.now, 'drop_occluded'))


# ---------------- the estimate control (ac110's GatedEstimator, re-exported) -------------------
def _make_estimate(seed, history, bel_off):
    return ac110.GatedEstimator(seed, history, bel_off=bel_off, estimate=True,
                                proactive=True, scramble=False)


# ---------------- the run core -----------------------------------------------------------------
def _condition_params(condition):
    return ac110._condition_params(condition)


def _make_alloc(arm, seed, history, n_offs, bel_off, w=COUNTER_W, n_thr=N_STAR, p=P_STAR):
    if arm == 'counter':
        return CounterAlloc(seed, history, n_offs=n_offs, bel_off=bel_off, w=w, n_thr=n_thr)
    if arm == 'no_write':
        return CounterAlloc(seed, history, n_offs=n_offs, bel_off=bel_off, w=w, n_thr=n_thr,
                            no_write=True)
    if arm == 'scramble':
        return CounterAlloc(seed, history, n_offs=n_offs, bel_off=bel_off, w=w, n_thr=n_thr,
                            scramble=True)
    if arm == 'tuned':
        return TunedAlloc(seed, history, p=p)
    if arm == 'estimate':
        return _make_estimate(seed, history, bel_off)
    raise ValueError(arm)


def _run_core(seed, history, arm, condition, record_trace=False, ports=PORTS, q=0.9,
              w=COUNTER_W, n_thr=N_STAR, p=P_STAR, swap_at=None):
    ac12.PORTS = ports; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    bel_off = ac107.bel_offset(o)
    streak_offs = ac96.streak_offsets(o)
    n_offs = streak_offs[0:3]            # 3 bits (the counter lives in the dead rule's free bits)
    alloc = _make_alloc(arm, seed, history, n_offs, bel_off, w=w, n_thr=n_thr, p=p)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    alloc.streak_offs = streak_offs
    if isinstance(alloc, CounterAlloc):
        alloc.n_offs = n_offs
        alloc.bel_off = bel_off
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
    step = ac110.build_step(alloc, succ, build_offs, cfg, cut_obj, bel_off=bel_off,
                            skip_est=False, gate_rng=gate_rng, q=q)
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
    income = 0
    income_post = 0
    swap_applied = False
    for t in range(TICKS):
        alloc.now = t
        cut_obj.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = _make_alloc(arm, seed, history, n_offs, bel_off, w=w, n_thr=n_thr, p=p)
            alloc.offs = offs
            alloc.shadow = o.body.traces[0].copy()
            alloc.streak_offs = streak_offs
            if isinstance(alloc, CounterAlloc):
                alloc.n_offs = n_offs
                alloc.bel_off = bel_off
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
        inc = int(e.get('in_m', 0)) + int(e.get('in_f', 0))
        income += inc
        if t >= CUT_TICK:
            income_post += inc
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
    n_final = counter_read(o, n_offs)
    holding_final = hold_read(o, bel_off)
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
                n=n_final, holding=holding_final,
                counter_events=getattr(alloc, 'counter_events', []),
                hold_events=getattr(alloc, 'hold_events', []),
                tuned_events=getattr(alloc, 'tuned_events', []),
                swap_applied=swap_applied,
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                counter_writes=int(total['counter_writes']),
                bel_writes=int(total['bel_writes']),
                memory_writes=int(total['memory_writes']),
                income=income, income_post=income_post,
                q=q, w=w, n_thr=n_thr, p=p,
                state_hash=o.digest()), o, trace


def run(seed, history, arm, condition, ports=PORTS, record_trace=False, q=0.9,
        w=COUNTER_W, n_thr=N_STAR, p=P_STAR):
    row, o, _ = _run_core(seed, history, arm, condition, record_trace=record_trace,
                          ports=ports, q=q, w=w, n_thr=n_thr, p=p)
    return row


# ---------------- the graded endpoints ---------------------------------------------------------
def first_drop_tick(row):
    ts = [t for t, _p, _r in row['drop_ticks']]
    return min(ts) if ts else None


def move_latency(row):
    t = first_drop_tick(row)
    return (t - CUT_TICK) if t is not None else None


def clean_control_identity(seed, history, condition, q=Q_CLEAN):
    """G1 (world license): the estimate arm reproduces the frozen AC110 `maintained` arm
    byte-for-byte (state_hash) at q=0.5 -- the world is the AC110 world, correctly built."""
    m = run(seed, history, 'estimate', condition, q=q)
    n = ac110.run(seed, history, 'maintained', condition, q=q)
    return m['state_hash'] == n['state_hash']


# ---------------- observers / collectors -------------------------------------------------------
def snapshot_hashes(protocol_path):
    h = {}
    for name in SOURCES:
        p = Path(name)
        if p.exists():
            h[name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return h


def collect_engineering(root, seeds, q=0.9, conditions=None):
    """Engineering screen (disclosed, excluded): the full arm cohort at the default parameters,
    plus the parameter sweep (N grid for the counter, p grid for the tuned rival)."""
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
                        r = run(seed, history, arm, cond, q=q)
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, cohort=[
                (r['arm'], r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['income_post'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
        # sweep N (counter) and p (tuned) on move+cut
        for seed in seeds:
            for history in (0, 1):
                for n_thr in N_GRID:
                    for cond in ('move', 'cut'):
                        r = run(seed, history, 'counter', cond, q=q, n_thr=n_thr)
                        r['param'] = 'counter N=%d' % n_thr
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                for p in P_GRID:
                    for cond in ('move', 'cut'):
                        r = run(seed, history, 'tuned', cond, q=q, p=p)
                        r['param'] = 'tuned p=%.2f' % p
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                f.flush()
            print(json.dumps(dict(seed=seed, sweep_done=True), default=str), flush=True)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), q=q, arms=list(ARMS), conditions=list(conditions),
             N_GRID=N_GRID, P_GRID=P_GRID, n_rows=len(rows)),
        indent=2, default=str))
    print(json.dumps(dict(n_rows=len(rows)), default=str))
    return rows


def collect_frozen(root, seeds, q=0.9, protocol_path='AC116_PROTOCOL_v1.md',
                   n_star=None, p_star=None):
    """The frozen confirmation: full cohort at the fixed comparison parameters (N*, p*),
    snapshot first, rows last."""
    if n_star is None:
        n_star = N_STAR
    if p_star is None:
        p_star = P_STAR
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    snapshot = dict(seeds=list(seeds), q=q, eps=EPS, n_star=n_star, p_star=p_star,
                    w=COUNTER_W, N_GRID=N_GRID, P_GRID=P_GRID,
                    arms=list(ARMS), conditions=list(CONDITIONS),
                    hashes=snapshot_hashes(protocol_path),
                    note='FROZEN confirmation: protocol hashed pre-run; engineering excluded.')
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(snapshot, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for cond in CONDITIONS:
                    for arm in ARMS:
                        kw = {}
                        if arm in ('counter', 'no_write', 'scramble'):
                            kw['n_thr'] = n_star
                        if arm == 'tuned':
                            kw['p'] = p_star
                        r = run(seed, history, arm, cond, q=q, **kw)
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, cohort=[
                (r['arm'], r['condition'], r['history'], r['relinquishments'], r['income_post'],
                 r['routes'])
                for r in rows[-len(CONDITIONS) * len(ARMS) * 2:]]), default=str), flush=True)
    # G1 (world license): estimate reproduces AC110 maintained at q=0.5, on the AC110 frozen seeds
    ac110_seeds = [6200, 6201, 6202, 6203, 6204, 6205, 6206, 6207]
    clean = {}
    for s in ac110_seeds:
        for h in (0, 1):
            for c in ('no_cause', 'move', 'cut'):
                clean[f'{s}/{h}/{c}'] = clean_control_identity(s, h, c, q=Q_CLEAN)
    results = dict(seeds=list(seeds), q=q, eps=EPS, arms=list(ARMS),
                   conditions=list(CONDITIONS), n_star=n_star, p_star=p_star,
                   snapshot=snapshot, clean_control=clean, n_rows=len(rows))
    (outdir / 'results.json').write_text(json.dumps(results, indent=2, default=str))
    print(json.dumps(dict(n_rows=len(rows), clean_control_all=all(clean.values()),
                          clean_n=len(clean)), indent=2, default=str))
    return rows, results


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac116_engineering_v1', ENGINEERING, q=0.9)
        return
    if '--engineering-q07' in sys.argv:
        collect_engineering('ac116_engineering_q07_v1', ENGINEERING, q=0.7)
        return
    if '--finals' in sys.argv:
        collect_frozen('ac116_results_v1', FINALS, q=0.9)
        return
    if '--finals-q07' in sys.argv:
        collect_frozen('ac116_results_q07_v1', FINALS, q=0.7)
        return
    if '--smoke' in sys.argv:
        collect_engineering('ac116_smoke_v1', [0, 1, 2], q=0.9)
        return
    print('AC116: --engineering (0-7), --engineering-q07, --finals (6600-6607), '
          '--finals-q07, --smoke.')


if __name__ == '__main__':
    main()
