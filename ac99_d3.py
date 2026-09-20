"""AC99-D3: a paid W-birth-priority rival, to separate write demand from catalyst production.

Parent: AC99-D2. Engineering only; no protocol, no freeze.

The AC98 G1 failure (seed 4436, priority [1,3,0,2]) dies at 8430 with the binary relinquishment
streak stuck at 3: the 3->4 increment is 3 logical bits = 21 replicas, so
`_cap = min(32, 8*W, energy, material) >= 21` needs W >= 3, and 4436's phase-shifted post-move
build runs through a repeated W-death window where W < 3. AC99-D2 showed a Gray-coded streak
(1-bit increments, W >= 1) removes the stall and 4436 relinquishes + survives -- the bottleneck
is the binary counter's WRITE COST. This runner builds the orthogonal rival: keep the BINARY
streak, but reorder the acquired program so the W-birth rule (action 6, mask 64) fires AHEAD of
the material contact (action 1, mask 2) whenever material <= 64 (obs bit 1 set). If the rival
keeps W >= 3 and the binary 3->4 then succeeds, the stall is also (in part) a catalyst-PRODUCTION
/ priority shortfall; if the rival does not change the outcome, the bottleneck is the write demand
alone.

The rival is a PAID architectural change, kept internal (no external W supply, no external
correct state):
  - the stored description's fixed words are the W-birth-first order (word 1 = mask 64 action 6,
    word 2 = mask 2 action 1), installed at acquisition exactly as the frozen description is;
  - the already-developed program bank is rewritten from the frozen order to match, PAID 1 energy
    + 1 material per changed replica, W-gated by `ac95._cap` (so the write spreads over a few
    actions at W=3). Cost = 2 words x 5 changed logical bits x 7 replicas = 70 replicas.

Everything else (binary streak, the AC98/AC99-D1 reserve level 21 + drop/stall/wlow triggers +
atomic release, the sticky 1e-4 damage, the 7-replica majority read, prices) is byte-for-byte the
AC99 architecture. `wb_first=False` reproduces `ac99.run(reserve=True)` exactly (state_hash).
"""
from pathlib import Path
import json
import sys
import numpy as np
import ac99            # reserve primitives + AllocEraseReserve (binary) + run()
import ac96            # streak storage
import ac95            # build, description, _cap, build_program, Succession
import ac12
import ac71
import ac4
import ac9
import ac5_program as prog

TICKS = ac95.TICKS
CORRUPT_TICK = ac95.CORRUPT_TICK
CORRUPT_BITS = ac95.CORRUPT_BITS
MOVE_TICK = ac95.MOVE_TICK
DEV = ac71.DEV
STREAK_N = ac12.STREAK_N

# reserve constants + primitives, unchanged from ac99 (the D1 atomic-release fix)
RESERVE_OFFS = ac99.RESERVE_OFFS
RESERVE_LEVEL = ac99.RESERVE_LEVEL
reserve_read = ac99.reserve_read
reserve_minority = ac99.reserve_minority
write_reserve = ac99.write_reserve
arm_reserve = ac99.arm_reserve
release_reserve = ac99.release_reserve
reg_reserve = ac99.reg_reserve
maintain = ac99.maintain           # ac95.maintain + reg_reserve (reserve bit repair)


# ---------------- the W-birth-first rule order (the rival's stored priority) ----------------
WB_FIRST_WORDS = ((1, 1, 0), (1, 64, 6), (1, 2, 1), (1, 128, 7), (1, 256, 8))


def wb_first_description(priority):
    """The rival's 130-bit description: the five fixed rule words with W-birth (mask 64, action 6)
    ahead of the material contact (mask 2, action 1). Identical to `ac95.description_bits` except
    words 1 and 2 are swapped. The permutation, masks and actions are unchanged."""
    words = np.concatenate([prog.encode_rule(*w) for w in WB_FIRST_WORDS])
    masks = np.concatenate([ac95.encode_mask(4 << b) for b in priority])
    actions = np.concatenate([ac95.encode_action(2 + b) for b in priority])
    return np.concatenate([words, ac95.encode_perm(priority), masks, actions])


def priority_change_cost():
    """Replicas changed by the swap in the PROGRAM bank: word 1 (mask 2, action 1) -> (mask 64,
    action 6) and word 2 (mask 64, action 6) -> (mask 2, action 1). The two words differ in 5
    logical bits each (mask bit 1 vs 6, action bits 0 vs 1+2), = 10 logical bits = 70 replicas."""
    w = {}
    w['m'] = prog.encode_rule(1, 2, 1)
    w['w'] = prog.encode_rule(1, 64, 6)
    bits = int((w['m'] != w['w']).sum()) * 2
    return bits, 7 * bits


def wb_first_program_target():
    """The W-birth-first target for program words 1 and 2 (28 bits = 2 words x 14 bits): word 1
    becomes (mask 64, action 6) and word 2 becomes (mask 2, action 1)."""
    return np.concatenate([prog.encode_rule(1, 64, 6), prog.encode_rule(1, 2, 1)])


# ---------------- the run (faithful to ac99._run_internal; adds wb_first + W trace) ----------------
def _run_internal(seed, history, arm, reserve, damage, corrupt, transition,
                  ticks, move_tick, record_trace=False, swap_at=None,
                  damage_rate=1e-4, wb_first=False, record_w_trace=False):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    assert arm == 'gated', 'the maintained/reserve arms are the fixed architecture only'
    alloc = ac99.AllocEraseReserve('allocate', seed, history, reserve=reserve)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    streak_offs = ac96.streak_offsets(o)
    alloc.streak_offs = streak_offs
    reg_offs = ac95.resolve_offsets(o)
    build_offs = reg_offs + streak_offs
    encoded = wb_first_description(priority) if wb_first else ac95.description_bits(priority)
    o.body.traces[1, :ac95.DESC_BITS] = encoded[:, None]
    acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    cfg = dict(ac95.ARM_PARTS[arm])
    cfg['reserve'] = reserve
    if cfg.get('block_W'):
        raise NotImplementedError('AC99-D3 supports the gated arm only')
    succ = ac95.Succession('real', encoded)
    step = ac95.build(cfg['ac_arm'], alloc, succ, build_offs, cfg)
    step.__globals__['maintain'] = maintain
    # ---- the rival's paid priority change: written through the program bank over the first few
    # ticks. The frozen acquisition endowment is energy 64, material 128, while the swap (2 words x
    # 5 logical bits x 7 replicas = 70 replicas) costs 70 energy + 70 material, so it is paid
    # incrementally (W-gated by `_cap`) as the body's own fuel->energy conversion replenishes energy
    # each tick. Internal: no external W, no external correct state. The description (bank 1) is the
    # rival's stored priority, installed at acquisition as the frozen description is. ----
    swap_tgt = wb_first_program_target() if wb_first else None
    swap_done = False
    priority_writes = 0
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
    post_move = {'W_birth': 0, 'C_birth': 0, 'B_birth': 0}
    first_dead = None
    drop_ticks = []
    restore_ticks = []
    trace = [] if record_trace else None
    w_trace = [] if record_w_trace else None
    was_bound = {0: False, 1: False}
    seen_bound = {0: False, 1: False}
    reacquire_ticks = {0: [], 1: []}
    swap_applied = False
    for t in range(ticks):
        alloc.now = t
        # ---- paid priority change (rival): write the remaining swap replicas, W-gated ----
        if swap_tgt is not None and not swap_done:
            sites = np.argwhere(o.body.traces[0, 14:42] != swap_tgt[:, None])
            if len(sites) == 0:
                swap_done = True
            else:
                n = min(ac95._cap(o.body), len(sites))
                if n:
                    idx = sites[:n]
                    o.body.traces[0, 14 + idx[:, 0], idx[:, 1]] = swap_tgt[idx[:, 0]]
                    o.body.energy -= n
                    o.body.material -= n
                    total['writes'] += n
                    total['spent_e'] += n
                    total['spent_m'] += n
                    priority_writes += n
        if swap_at is not None and t == swap_at:
            succ = ac95.Succession('real', encoded)
            alloc = ac99.AllocEraseReserve('allocate', seed, history, reserve=reserve)
            alloc.streak_offs = streak_offs
            alloc.offs = offs
            alloc.shadow = o.body.traces[0].copy()
            alloc.now = t
            step.__globals__['succ'] = succ
            step.__globals__['alloc'] = alloc
            step.__globals__['allowance'] = alloc.allowance
            swap_applied = True
        core = (rng.random((126, 7)) < damage_rate).astype(np.uint8)
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
            if reserve:
                o.body.traces[1, RESERVE_OFFS] |= (rng1.random(7) < .0001).astype(np.uint8)
        if t == CORRUPT_TICK and corrupt:
            for bit in range(CORRUPT_BITS):
                w = 1 - int(acquired[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(acquired[bit])
        step.__globals__['now'] = t
        prev_drops = len(alloc.log['dropped'])
        prev_restores = len(alloc.log.get('restored', []))
        e = step(o, core, noise, directions, coin,
                 tuple(ac95.mapping_at(base_map, t, transition, move_tick)), [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t >= move_tick:
            for k in post_move:
                post_move[k] += e.get(k, 0)
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
        if record_w_trace:
            w_trace.append(dict(t=t,
                                W=int((o.body.life[:4] > 0).sum()),
                                C=int((o.body.life[16:20] > 0).sum()),
                                material=int(o.body.material),
                                energy=int(o.body.energy),
                                fuel=int(o.body.fuel),
                                W_birth=int(e.get('W_birth', 0)),
                                C_birth=int(e.get('C_birth', 0)),
                                contacts=int(e.get('contacts', 0)),
                                productive=int(e.get('productive', 0)),
                                obs1=int(o.body.material <= 64),
                                obs6=int((o.body.life[:4] > 0).sum() < 2)))
        if first_dead is None and o.body.dead:
            first_dead = t
    arm_events = [ev for ev in alloc.reserve_events if ev[1] == 'arm']
    rel_events = [ev for ev in alloc.reserve_events if ev[1] in ('drop', 'stall', 'wlow')]
    rel_kinds = [(ev[0], ev[1]) for ev in rel_events]
    inv = ac4.inventory(o.body)
    row = dict(seed=seed, history=history, arm=arm, reserve=reserve, damage=damage,
               corrupt=corrupt, transition=transition, ticks=ticks, move_tick=move_tick,
               wb_first=wb_first,
               completed=total['active'] == ticks, first_dead=first_dead,
               routes=[o.memory.read(k) for k in (0, 1)],
               demand=o.memory.demand().tolist(),
               register=[ac12.bit_value(o, off) for off in offs],
               relinquishments=len(alloc.log['dropped']),
               restorations=len(alloc.log.get('restored', [])),
               drop_ticks=drop_ticks,
               restore_ticks=restore_ticks,
               streak_final={0: ac96.streak_read(o, 0, streak_offs),
                             1: ac96.streak_read(o, 1, streak_offs)},
               streak_events=getattr(alloc, 'streak_events', []),
               reacquire_ticks=reacquire_ticks,
               reserve_armed_end=reserve_read(o),
               reserve_minority_end=reserve_minority(o),
               reserve_arm_ticks=[ev[0] for ev in arm_events],
               reserve_release_ticks=[ev[0] for ev in rel_events],
               reserve_release_kinds=rel_kinds,
               swap_applied=swap_applied,
               reserve_m=int(total['reserve_m']),
               reserve_released_m=int(total['reserve_released_m']),
               reserve_writes=int(total['reserve_writes']),
               priority_writes=int(priority_writes),
               W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
               W_births=int(total['W_birth']), C_births=int(total['C_birth']),
               B_births=int(total['B_birth']),
               W_births_post_move=int(post_move['W_birth']),
               C_births_post_move=int(post_move['C_birth']),
               B_births_post_move=int(post_move['B_birth']),
               energy=inv[0], material=inv[1], fuel=inv[2],
               writes=int(total['writes']), reg_writes=int(total['reg_writes']),
               succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
               streak_writes=int(total['streak_writes']),
               state_hash=o.digest())
    return row, o, trace, w_trace


def run(seed, history, arm='gated', reserve=False, damage=True, corrupt=False,
        transition='perm', ticks=TICKS, move_tick=MOVE_TICK, wb_first=False):
    """Run one individual with the BINARY streak. `wb_first=True` is the W-birth-priority rival;
    `wb_first=False` reproduces `ac99.run(reserve=...)` byte-for-byte."""
    row, o, _, _ = _run_internal(seed, history, arm, reserve, damage, corrupt,
                                 transition, ticks, move_tick, record_trace=False,
                                 wb_first=wb_first, record_w_trace=False)
    return row


# ---------------- byte-identity: wb_first=False must reproduce ac99 exactly ----------------
def frozen_reproduction(seeds, transition='perm', damage=True, corrupt=False, reserve=True):
    """wb_first=False reproduces ac99.run(reserve=True) exactly (state_hash) on every individual."""
    n = 0
    for seed in seeds:
        for history in (0, 1):
            got = run(seed, history, 'gated', reserve=reserve, damage=damage, corrupt=corrupt,
                      transition=transition)
            want = ac99.run(seed, history, 'gated', reserve=reserve, damage=damage,
                            corrupt=corrupt, transition=transition)
            assert got['state_hash'] == want['state_hash'], \
                f"frozen reproduction mismatch {seed}/{history}"
            n += 1
    return n


# ---------------- engineering collector (binary frozen vs W-birth-first rival) ----------------
def collect(root, seeds, transition='perm', damage=True, corrupt=False):
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for wb in (False, True):
                    r = run(seed, history, 'gated', reserve=True, damage=damage,
                            corrupt=corrupt, transition=transition, wb_first=wb)
                    rows.append(r)
                    f.write(json.dumps(r) + '\n')
                    f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['history'], r['wb_first'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['streak_final'],
                 r['reserve_release_kinds'], r['streak_writes'], r['priority_writes'],
                 r['W'], r['W_births_post_move'])
                for r in rows[-4:]]), default=str), flush=True)
    by = {}
    for r in rows:
        by[(r['seed'], r['history'], r['wb_first'])] = r
    per_ind = {}
    for seed in seeds:
        for history in (0, 1):
            f = by[(seed, history, False)]
            w = by[(seed, history, True)]
            per_ind[f'{seed}/{history}'] = dict(
                seed=seed, history=history,
                frozen=dict(completed=f['completed'], first_dead=f['first_dead'],
                            relinquishments=f['relinquishments'], routes=f['routes'],
                            streak_final=f['streak_final'], streak_writes=f['streak_writes'],
                            release_kinds=f['reserve_release_kinds'], W=f['W'],
                            W_births_post_move=f['W_births_post_move']),
                wb_first=dict(completed=w['completed'], first_dead=w['first_dead'],
                              relinquishments=w['relinquishments'], routes=w['routes'],
                              streak_final=w['streak_final'], streak_writes=w['streak_writes'],
                              release_kinds=w['reserve_release_kinds'], W=w['W'],
                              W_births_post_move=w['W_births_post_move'],
                              priority_writes=w['priority_writes']),
            )
    bits, replicas = priority_change_cost()
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), transition=transition, damage=damage, corrupt=corrupt,
             STREAK_N=STREAK_N, priority_change=dict(logical_bits=bits, replicas=replicas),
             per_individual=per_ind, rows=rows),
        indent=2, default=str))
    print(json.dumps(dict(priority_change=dict(logical_bits=bits, replicas=replicas),
                          per_individual=per_ind), indent=2, default=str))
    return rows, per_ind


def main():
    if '--cost' in sys.argv:
        bits, replicas = priority_change_cost()
        print(json.dumps(dict(logical_bits=bits, replicas=replicas)))
        return
    collect('ac99_d3_engineering_v1', [4436, 4437, 4438, 4439])


if __name__ == '__main__':
    main()
