"""AC113 (P6): frozen confirmation of the heterogeneous-LR two-counter estimate.

The P6 confirmation of P5's AC112 candidate. The world and arms are the AC112
architecture (two-cause move-vs-cut world, occlusion gate q, residual yield eps,
maintained two-counter candidate + single-counter / immediate / scramble rivals).
The P5 feasibility decision fixes three things this runner realises:

  1. HIGH OCCLUSION: q = 0.9 (at q=0.7 the open decisive path does most of the work).
  2. GRADED ENDPOINT: post-cause income + move latency + cut false-relinquish, gated on
     the graded (income/regret) endpoint -- NOT categorical dominance -- with both
     parameter families swept (theta for the candidate, (w,N) for the single counter).
  3. EQUIVALENCE / NO-ADVANTAGE are legitimate recorded falsification outcomes (F1/F2),
     alongside no-information (F3). A failed hypothesis is NOT converted into a passing
     gate.

This is a FROZEN confirmation: the protocol (AC113_PROTOCOL_v1.md) is hashed before the
finals are accessed, engineering seeds are excluded, and the finals use untouched seeds.
The runner records per-individual post-cause income (in_m+in_f over [CUT_TICK, TICKS)),
move first-drop latency, cut relinquishment count, and expenditure -- the endpoints the
protocol gates on. It reuses AC112's build_step, arms, and source surgeries unmodified
(imported), adding only the income accumulator and full (theta, w, N) parameterisation
to a single run core.
"""

from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import math
import sys
import numpy as np

import ac112
from ac112 import (TICKS, DEV, MOVE_TICK, CUT_TICK, PORTS, WINDOW, STREAK_N,
                   weights, logit, counter_read, counter_write, hold_read, hold_write,
                   build_step, _drop_no_streak, TwoCounterAlloc, SingleCounterAlloc,
                   ImmediateAlloc, _condition_params, _true_cause, ARMS, CONDITIONS)
import ac12
import ac4
import ac95
import ac96
import ac100
import ac106
import ac107

# ---- declared world constants for the confirmation (from the P5 feasibility decision) ----
Q = 0.9                                # high occlusion: the accumulator is load-bearing
EPS = 0.08                             # primary residual yield (informative-heterogeneous)
EPS_SECONDARY = 0.02                   # secondary: the most heterogeneous end (P4's largest gap)

# ---- prespecified parameter grids (both families swept, AC11's rule) ----
THETA_GRID = [0.5, 0.55, 0.6, 0.66, 0.7, 0.8, 0.9]
SINGLE_GRID = [(-6, 1), (-6, 2), (-6, 4), (-4, 2), (-4, 4), (-2, 2), (-2, 4), (0, 1), (0, 2)]

ENGINEERING = list(range(4))           # engineering screen (q=0.9), disclosed, excluded
FINALS = list(range(6400, 6408))       # untouched confirmation seeds (8 seeds x 2 histories)

# Fixed comparison parameters, selected on the ENGINEERING cohort's combined post-cause
# income (disclosed here, fixed for the finals -- no in-sample selection on the finals):
THETA_STAR = 0.5                       # two_counter's income-maximising theta (max combined)
SINGLE_STAR = (-6, 4)                  # single_counter's income-maximising (w, N)

# Frozen source set (the declaration + the simulation code, NOT the verification tools;
# AC16/AC17's rule). ac112.py is the P5 runner this study freezes; its transitively
# imported frozen dependencies are hashed through ac112.SOURCES.
SOURCES = ['ac113.py', 'ac112.py', 'AC113_PROTOCOL_v1.md']


def _make_alloc(arm, seed, history, n_u_offs, n_p_offs, n_offs, bel_off,
                theta=ac112.THETA, w=ac112.SINGLE_W, n_thr=ac112.SINGLE_N):
    if arm == 'two_counter':
        return TwoCounterAlloc(seed, history, n_u_offs=n_u_offs, n_p_offs=n_p_offs,
                               bel_off=bel_off, scramble=False, theta=theta)
    if arm == 'scramble':
        return TwoCounterAlloc(seed, history, n_u_offs=n_u_offs, n_p_offs=n_p_offs,
                               bel_off=bel_off, scramble=True, theta=theta)
    if arm == 'single_counter':
        return SingleCounterAlloc(seed, history, n_offs=n_offs, bel_off=bel_off,
                                  w=w, n_thr=n_thr)
    if arm == 'immediate':
        return ImmediateAlloc(seed, history)
    raise ValueError(arm)


def _run_core(seed, history, arm, condition, record_trace=False, ports=PORTS,
              q=Q, eps=EPS, theta=ac112.THETA, w=ac112.SINGLE_W, n_thr=ac112.SINGLE_N,
              swap_at=None):
    """Faithful copy of ac112._run_core with (a) an income accumulator and
    (b) full (theta, w, N) parameterisation for the single-counter rival."""
    ac12.PORTS = ports; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    o, offs = ac12.acquire(seed)
    streak_offs = ac96.streak_offsets(o)
    n_u_offs = streak_offs[0:4]
    n_p_offs = streak_offs[4:6]
    n_offs = streak_offs[0:3]
    bel_off = ac107.bel_offset(o)
    alloc = _make_alloc(arm, seed, history, n_u_offs, n_p_offs, n_offs, bel_off,
                        theta=theta, w=w, n_thr=n_thr)
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
    total = _event_total()
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
    income = 0
    income_post = 0
    for t in range(TICKS):
        alloc.now = t
        cut_obj.now = t
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = _make_alloc(arm, seed, history, n_u_offs, n_p_offs, n_offs, bel_off,
                                theta=theta, w=w, n_thr=n_thr)
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
                income=income, income_post=income_post,
                q=q, eps=eps, theta=theta, w=w, n_thr=n_thr,
                state_hash=o.digest()), o, trace


def _event_total():
    import ac9
    total = ac9.event()
    for k in ('reg_writes', 'succ_writes', 'ctrl_writes', 'timer_increments', 'timer_resets',
              'split_events', 'streak_writes', 'bel_writes', 'proactive_writes',
              'counter_writes', 'hold_writes'):
        total[k] = 0
    return total


def run(seed, history, arm, condition, ports=PORTS, record_trace=False, q=Q, eps=EPS,
        theta=ac112.THETA, w=ac112.SINGLE_W, n_thr=ac112.SINGLE_N):
    row, o, _ = _run_core(seed, history, arm, condition, record_trace=record_trace,
                          ports=ports, q=q, eps=eps, theta=theta, w=w, n_thr=n_thr)
    return row


def observer_discard_equivalence(seed, history, condition='cut', q=Q, eps=EPS,
                                 theta=ac112.THETA, swap_tick=None):
    """Per-tick observer-discard on the candidate (inherited from AC112, re-run at q=0.9)."""
    if swap_tick is None:
        swap_tick = CUT_TICK + WINDOW // 2
    base, base_o, base_trace = _run_core(seed, history, 'two_counter', condition,
                                         record_trace=True, q=q, eps=eps, theta=theta)
    swapped, swapped_o, swapped_trace = _run_core(seed, history, 'two_counter', condition,
                                                  record_trace=True, q=q, eps=eps,
                                                  theta=theta, swap_at=swap_tick)
    n_equal = 0
    first_div = None
    for (t1, d1), (t2, d2) in zip(base_trace, swapped_trace):
        assert t1 == t2
        if d1 == d2:
            n_equal += 1
        elif first_div is None:
            first_div = t1
    per_tick_identical = (first_div is None and len(base_trace) == len(swapped_trace)
                          and n_equal == len(base_trace))
    return dict(seed=seed, history=history, condition=condition, swap_tick=swap_tick,
                swap_applied=swapped['swap_applied'], per_tick_identical=per_tick_identical,
                n_equal=n_equal, n_ticks=len(base_trace), first_div=first_div,
                terminal_identical=base['state_hash'] == swapped['state_hash'])


# ---------------- the graded endpoint and gates ----------------------------------------------
def first_drop_tick(row):
    ts = [t for t, _p, _r in row['drop_ticks']]
    return min(ts) if ts else None


def move_latency(row):
    t = first_drop_tick(row)
    return (t - CUT_TICK) if t is not None else None


def summarize(rows, seeds, conditions=None):
    """Recompute the graded endpoint and gates from the raw rows (audit-independent)."""
    if conditions is None:
        conditions = list(CONDITIONS)
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition'], r['arm'],
                       r.get('theta'), r.get('w'), r.get('n_thr')), r)
    inds = [(s, h) for s in seeds for h in (0, 1)]
    out = {'n_individuals': len(inds)}
    for cond in conditions:
        out[cond] = {}
        for arm in ARMS:
            out[cond][arm] = {}
            for (s, h) in inds:
                key = (s, h, cond, arm, ac112.THETA, ac112.SINGLE_W, ac112.SINGLE_N)
                if key not in by:
                    continue
                r = by[key]
                out[cond][arm][(s, h)] = dict(
                    relinquishments=r['relinquishments'],
                    move_latency=move_latency(r),
                    income_post=r['income_post'],
                    income=r['income'],
                    completed=r['completed'], first_dead=r['first_dead'],
                    counter_writes=r['counter_writes'],
                    reg_writes=r['reg_writes'],
                    routes=r['routes'])
    return out


# ---------------- collectors -------------------------------------------------------------------
def snapshot_hashes(protocol_path):
    """sha256 of every declared source plus the protocol (the frozen source of truth)."""
    h = {}
    for name in SOURCES + ac112.SOURCES:
        p = Path(name)
        if p.exists():
            h[name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return h


def collect_frozen(root, seeds, q=Q, eps=EPS, protocol_path='AC113_PROTOCOL_v1.md',
                   theta_star=None, single_star=None):
    """The frozen confirmation: full cohort + parameter sweep, snapshot first, rows last."""
    if theta_star is None:
        theta_star = THETA_STAR
    if single_star is None:
        single_star = SINGLE_STAR
    w_star, n_star = single_star
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    snapshot = dict(seeds=list(seeds), q=q, eps=eps, theta_star=theta_star,
                    single_star=list(single_star),
                    theta_grid=THETA_GRID, single_grid=SINGLE_GRID,
                    arms=list(ARMS), conditions=list(CONDITIONS),
                    hashes=snapshot_hashes(protocol_path),
                    note='FROZEN confirmation: protocol hashed pre-run; engineering excluded.')
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(snapshot, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        # full cohort at the fixed comparison parameters (theta*, (w,N)*), selected on
        # engineering and declared; scramble also at theta*.
        for seed in seeds:
            for history in (0, 1):
                for cond in CONDITIONS:
                    for arm in ARMS:
                        kw = {}
                        if arm in ('two_counter', 'scramble'):
                            kw['theta'] = theta_star
                        if arm == 'single_counter':
                            kw['w'] = w_star
                            kw['n_thr'] = n_star
                        r = run(seed, history, arm, cond, q=q, eps=eps, **kw)
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, cohort=[(r['arm'], r['condition'], r['history'],
                                                      r['relinquishments'], r['income_post'])
                                                     for r in rows[-len(CONDITIONS) * len(ARMS) * 2:]]),
                              default=str), flush=True)
        # parameter sweep on the informative conditions (both families)
        for seed in seeds:
            for history in (0, 1):
                for theta in THETA_GRID:
                    for cond in ('move', 'cut'):
                        r = run(seed, history, 'two_counter', cond, q=q, eps=eps, theta=theta)
                        r['param'] = 'theta=%.2f' % theta
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                for (w, n_thr) in SINGLE_GRID:
                    for cond in ('move', 'cut'):
                        r = run(seed, history, 'single_counter', cond, q=q, eps=eps,
                                w=w, n_thr=n_thr)
                        r['param'] = 'w=%d,N=%d' % (w, n_thr)
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                f.flush()
            print(json.dumps(dict(seed=seed, sweep_done=True), default=str), flush=True)
        # causal-role control: scramble (read forced (0,0)) at theta=0.6, where the read
        # content is load-bearing (V2). At theta*=0.5 the threshold passes through (0,0) and
        # the scramble degenerates -- a declared boundary, not a gate failure.
        for seed in seeds:
            for history in (0, 1):
                for cond in ('move', 'cut'):
                    r = run(seed, history, 'scramble', cond, q=q, eps=eps, theta=0.6)
                    r['param'] = 'scramble theta=0.60'
                    rows.append(r)
                    f.write(json.dumps(r, default=str) + '\n')
            f.flush()
            print(json.dumps(dict(seed=seed, causal_role_done=True), default=str), flush=True)
    obs = {f'{s}/{h}': observer_discard_equivalence(s, h, 'cut', q=q, eps=eps,
                                                     theta=theta_star)
           for s in seeds for h in (0, 1)}
    results = dict(seeds=list(seeds), q=q, eps=eps, arms=list(ARMS),
                   conditions=list(CONDITIONS), theta_grid=THETA_GRID,
                   single_grid=SINGLE_GRID, snapshot=snapshot,
                   observer_discard={k: dict(per_tick_identical=v['per_tick_identical'],
                                             first_div=v['first_div'])
                                     for k, v in obs.items()},
                   n_rows=len(rows))
    (outdir / 'results.json').write_text(json.dumps(results, indent=2, default=str))
    print(json.dumps(dict(n_rows=len(rows), observer_discard={
        k: (v['per_tick_identical'], v['first_div']) for k, v in obs.items()},
        snapshot=snapshot), indent=2, default=str))
    return rows, results


def sweep(root, seeds, q=Q, eps=EPS):
    """Engineering parameter screen (disclosed, excluded): decision surface at the run q/eps."""
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for theta in THETA_GRID:
                for cond in ('move', 'cut'):
                    r = run(seed, 0, 'two_counter', cond, q=q, eps=eps, theta=theta)
                    r['param'] = 'theta=%.2f' % theta
                    rows.append(r); f.write(json.dumps(r, default=str) + '\n')
            for (w, n_thr) in SINGLE_GRID:
                for cond in ('move', 'cut'):
                    r = run(seed, 0, 'single_counter', cond, q=q, eps=eps, w=w, n_thr=n_thr)
                    r['param'] = 'w=%d,N=%d' % (w, n_thr)
                    rows.append(r); f.write(json.dumps(r, default=str) + '\n')
            for arm in ('immediate', 'scramble'):
                for cond in ('move', 'cut'):
                    r = run(seed, 0, arm, cond, q=q, eps=eps)
                    r['param'] = '-'
                    rows.append(r); f.write(json.dumps(r, default=str) + '\n')
            f.flush()
            print(json.dumps(dict(seed=seed, sweep=[(r['param'], r['condition'],
                                                     r['relinquishments'], r['income_post'],
                                                     move_latency(r))
                                                    for r in rows[-2 * (len(THETA_GRID) + len(SINGLE_GRID) + 2):]]),
                              default=str), flush=True)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), q=q, eps=eps, theta_grid=THETA_GRID, single_grid=SINGLE_GRID,
             n_rows=len(rows)), indent=2, default=str))
    print(json.dumps(dict(sweep_complete=len(rows)), default=str))
    return rows


def main():
    if '--engineering' in sys.argv:
        sweep('ac113_engineering_v1', ENGINEERING)
        return
    if '--finals' in sys.argv:
        collect_frozen('ac113_results_v1', FINALS)
        return
    if '--finals-eps002' in sys.argv:
        collect_frozen('ac113_results_v1_eps002', FINALS, eps=EPS_SECONDARY,
                       single_star=(-6, 1))
        return
    if '--smoke' in sys.argv:
        collect_frozen('ac113_smoke_v1', [6400, 6401])
        return
    print('AC113: --engineering (seeds 0-3), --finals (seeds 6400-6407), '
          '--finals-eps002, --smoke.')


if __name__ == '__main__':
    main()
