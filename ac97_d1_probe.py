"""AC97-D1 probe: instrument the maintained-arm relinquishment world to locate the
decisive budget shortfall behind the stuck streak-5.

Measurement only. Monkeypatches the write primitives to record, immediately before
each event, the available resources (energy, material, W, _cap) and the write's
replica count and accept/refuse outcome. The trajectory is byte-identical to the
un-instrumented run (verified against the frozen state_hash).

Events recorded:
  kind='streak_write'  : increment (new=cur+1) or reset (new=0, cur>0) -- the paid
                         atomic counter write (refused whole when n > cap).
  kind='drop'          : the relinquishment register write (<=7 replicas) at the
                         6th unproductive contact (cur=5 -> drop fires).
  kind='reg_from_active' : the bank-0 repair (reconstruction from the description),
                         which maintains the program (register + streak excluded)
                         and competes for the same material/energy.
"""
import numpy as np
import ac96, ac95, ac12, ac4, ac76, ac71, ac9
import ac5_program as prog

PROBE_NOW = -1
RECORDS = []


def _W(b):
    return int(ac4.available(b)[:4].sum())


def _cap(b):
    return ac95._cap(b)


# ---------------- instrument streak_write (ac96 module global) ----------------
_orig_streak_write = ac96.streak_write


def _instr_streak_write(o, e, key, new, streak_offs):
    b = o.body
    offs = np.array(streak_offs[3 * key: 3 * key + 3])
    cur = ac96.streak_read(o, key, streak_offs)
    targets = np.array([(new >> k) & 1 for k in range(3)], dtype=np.uint8)
    sites = np.argwhere(b.traces[0, offs] != targets[:, None])
    n = int(len(sites))
    cap = _cap(b)
    energy = int(b.energy); material = int(b.material); W = _W(b)
    r = _orig_streak_write(o, e, key, new, streak_offs)
    RECORDS.append(dict(kind='streak_write', tick=PROBE_NOW, key=int(key),
                        cur=int(cur), new=int(new), n=n, cap=cap,
                        energy=energy, material=material, W=W,
                        accepted=bool(r > 0), replicas_written=int(r)))
    return r


ac96.streak_write = _instr_streak_write


# ---------------- instrument the _drop register write ----------------
_orig_drop = ac96.AllocEraseMaintained._drop


def _instr_drop(self, o, e, key):
    place = ac12.m12.slot_of_key(o.memory, key)
    if place is None:
        RECORDS.append(dict(kind='drop', tick=PROBE_NOW, key=int(key), place=None))
        return _orig_drop(self, o, e, key)
    off = self.offs[2 * place[0] + place[1]]
    sites = o.body.traces[0, off]
    n = int((sites != 1).sum())
    cap = min(32, 8 * _W(o.body), o.body.energy, o.body.material)
    energy = int(o.body.energy); material = int(o.body.material); W = _W(o.body)
    n_before = len(self.log['dropped'])
    r = _orig_drop(self, o, e, key)
    RECORDS.append(dict(kind='drop', tick=PROBE_NOW, key=int(key),
                        place=list(place), n=n, cap=cap,
                        energy=energy, material=material, W=W,
                        accepted=len(self.log['dropped']) > n_before))
    return r


ac96.AllocEraseMaintained._drop = _instr_drop


# ---------------- instrument the bank-0 repair (ac95 module global) ----------------
_orig_reg_from_active = ac95.reg_from_active


def _instr_reg_from_active(o, e, reg_offs):
    b = o.body
    target = ac95.build_program(ac95.read_slot(o, ac95.read_pointer(o)))
    if target is None:
        RECORDS.append(dict(kind='reg_from_active', tick=PROBE_NOW, target=None))
        return _orig_reg_from_active(o, e, reg_offs)
    exclude = set(reg_offs)
    sites = np.argwhere(b.traces[0, :prog.PROGRAM_BITS] != target[:, None])
    sites = sites[[i for i in range(len(sites)) if int(sites[i, 0]) not in exclude]]
    n_avail = int(len(sites))
    cap = _cap(b)
    energy = int(b.energy); material = int(b.material); W = _W(b)
    r = _orig_reg_from_active(o, e, reg_offs)
    RECORDS.append(dict(kind='reg_from_active', tick=PROBE_NOW, n_avail=n_avail,
                        cap=cap, energy=energy, material=material, W=W))
    return r


ac95.reg_from_active = _instr_reg_from_active


def probe_run(seed, history, transition='perm', ticks=ac95.TICKS,
              move_tick=ac95.MOVE_TICK, damage=True, corrupt=False):
    global PROBE_NOW
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = ac96.AllocEraseMaintained('allocate', seed, history)
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
    succ = ac95.Succession('real', encoded)
    step = ac95.build(cfg['ac_arm'], alloc, succ, build_offs, cfg)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    first_dead = None
    first_streak_write_tick = None
    for t in range(ticks):
        PROBE_NOW = t
        alloc.now = t
        core = (rng.random((126, 7)) < 1e-4).astype(np.uint8)
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
        if t == ac95.CORRUPT_TICK and corrupt:
            for bit in range(ac95.CORRUPT_BITS):
                w = 1 - int(acquired[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(acquired[bit])
        step.__globals__['now'] = t
        e = step(o, core, noise, directions, coin,
                 tuple(ac95.mapping_at(base_map, t, transition, move_tick)), [True, True], True)
        if first_streak_write_tick is None and e.get('streak_writes', 0) > 0:
            first_streak_write_tick = t
        if first_dead is None and o.body.dead:
            first_dead = t
    return dict(seed=seed, history=history, first_dead=first_dead,
                completed=not o.body.dead, state_hash=o.digest(),
                streak_final={k: ac96.streak_read(o, k, streak_offs) for k in (0, 1)},
                routes=[o.memory.read(k) for k in (0, 1)],
                relinquishments=len(alloc.log['dropped']))
