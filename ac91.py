"""AC91: production-dependencies test — can the organization replace the finite-lived components
enabling reconstruction and coordination?

The internal-state milestone (AC86-89) is accepted: internally stored controller information is
maintained, reconstructed, and repeatedly transferred to successor storage through the tested
environmental challenge. Full autopoiesis remains unestablished: CLOSURE_BOUNDARY_v2.md's
declaration that the succession mechanism is "substrate" is a modeling choice, not a settled
finding.

This study measures the production of the machinery that enacts reconstruction and coordination.
The produced, finite-lived component is the W repair catalyst (life[:4], 4 slots, life 64, born by
action 6 via `birth(b, 0, ...)`, expiring after 64 ticks). W's specified capability — the per-action
write capacity `min(32, 8*available_W)` — is what gates EVERY paid maintenance write on the
reconstruction and coordination paths: reconstruction (`reg_from_active`), description repair
(`reg_description_active`), pointer repair (`reg_pointer`), controller-state repair (`reg_ctrl`),
the succession slot copy/remove (`write_toward_slot`) and the pointer switch (`write_pointer`). The
succession state machine's transition LOGIC (`advance()`) is supplied format-level machinery (the
accepted boundary); what is produced and replaced is the W catalyst that executes its writes.

Three causal links (the prespecified gates):
1. Blocking W production reduces the machinery (W count), then reconstruction capacity (8*W) and
   coordination capacity, and kills the organism.
2. Restoring W production rescues reconstruction WITHOUT supplying controller content (the
   restoration un-blocks the W-birth reaction only; the description is never touched).
3. Ordinary operation replaces W repeatedly (W births >> the 4-slot complement) while controller
   information and organizational continuity persist.

Design constraints honoured: the finite component list is fixed (W/C/B produced; the 130-bit
description + pointer + controller state + 126-bit program are stored content; `advance()` and
`prog.choose` are supplied). No distinct coordinator component is introduced — W's capability
genuinely covers both functions. No arbitrary "alive" flag. The repair-only arm is retained
throughout (replacement is a demonstrated capability, not a necessary maintenance process).

This runner is derived from ac89.py (the corrected AC87 implementation). The shared arms
(succession / repair / unmaintained / no_repair) are byte-identical to ac89's: the only change is
the optional W-birth gate, injected only for the new arms (no_W / W_restore / W_restore_late), which
is a no-op for the shared arms. Equivalence with AC89 is verified by re-running the AC89 schedule.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import sys
import numpy as np
import ac76
import ac71
import ac12
import ac9
import ac4
import ac5_program as prog

TICKS = ac76.TICKS                  # 16384
CORRUPT_TICK = ac76.CORRUPT_TICK    # 8192
CORRUPT_BITS = ac76.CORRUPT_BITS    # 8
MOVE_TICK = CORRUPT_TICK            # SIMULTANEOUS schedule (kept for the AC89 equivalence check)

# ---- the W-birth block window constants (the AC91 intervention) ----
RESTORE_TICK = 50        # W_restore: un-block W-birth here. W drops to 1 (the life-64 catalyst
                         # survives) and then recovers endogenously. Must be < 64: the initial W
                         # endowment [32,48,64,0] is fully expired by t=64, and W-birth needs a live
                         # W parent (autocatalytic), so a later restore cannot restart W.
RESTORE_LATE_TICK = 100  # W_restore_late: un-block after W has hit 0 (t=64) -- irreversible.

# ---- description layout (AC85's 130-bit description, re-implemented here) ----
NWORDS = 5
WIDTH = prog.WIDTH                  # 14
PERM_BITS = 8
PERM_OFFSET = NWORDS * WIDTH        # 70
NMASK_BITS = 9
NACTION_BITS = 4
NBANKS = 4
MASK_OFFSET = PERM_OFFSET + PERM_BITS                  # 78
ACTION_OFFSET = MASK_OFFSET + NBANKS * NMASK_BITS      # 114
DESC_BITS = ACTION_OFFSET + NBANKS * NACTION_BITS      # 130

FIXED_WORDS = ((1, 1, 0), (1, 2, 1), (1, 64, 6), (1, 128, 7), (1, 256, 8))

# ---- replaceable storage + pointer + controller-state layout (all in bank 1) ----
SLOTS = 4
SLOT_BITS = DESC_BITS
SUCC_MIN_SPACING = 2400
SUCC_BUDGET = 6
DESC_TRIGGER = 2
POINTER_TRIGGER = 2
CTRL_TRIGGER = 2

PTR_BASE = SLOTS * SLOT_BITS                          # 520
PTR_OFFS = [PTR_BASE, PTR_BASE + 1]

CTRL_BASE = PTR_BASE + 2                              # 522
CTRL_BITS = 18
CTRL_OFFS = np.arange(CTRL_BASE, CTRL_BASE + CTRL_BITS)
# controller word layout: 0 ACTIVE, 1-3 PHASE, 4-17 LAST_START. source/target derived from pointer.
PHASE_IDLE, PHASE_COPY, PHASE_VERIFY, PHASE_SWITCH, PHASE_REMOVE = range(5)

ARMS = ('succession', 'repair', 'no_W', 'W_restore', 'W_restore_late',
        'unmaintained', 'no_repair')

# per-arm config. block_W gates bank-0 (W) births; restore_tick=None blocks forever, a tick value
# un-blocks from that tick onward.
ARM_PARTS = {
    'succession':        dict(ac_arm='regen',     repair=True,  regen=True,  succession=True,  ctrl_maintain=True),
    'repair':            dict(ac_arm='regen',     repair=True,  regen=True,  succession=False, ctrl_maintain=True),
    'no_W':              dict(ac_arm='regen',     repair=True,  regen=True,  succession=True,  ctrl_maintain=True, block_W=True, restore_tick=None),
    'W_restore':         dict(ac_arm='regen',     repair=True,  regen=True,  succession=True,  ctrl_maintain=True, block_W=True, restore_tick=RESTORE_TICK),
    'W_restore_late':    dict(ac_arm='regen',     repair=True,  regen=True,  succession=True,  ctrl_maintain=True, block_W=True, restore_tick=RESTORE_LATE_TICK),
    'unmaintained':      dict(ac_arm='regen',     repair=False, regen=True,  succession=False, ctrl_maintain=False),
    'no_repair':         dict(ac_arm='no_repair', repair=False, regen=False, succession=False, ctrl_maintain=False),
}

SOURCES = ['ac91.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC91_PROTOCOL_v1.md']


# ---------------- description encode / decode ----------------
def encode_perm(priority):
    return ac76.encode_priority(priority)


def decode_perm(bits):
    return tuple(int((bits[2 * i] << 1) | bits[2 * i + 1]) for i in range(4))


def encode_mask(mask):
    return np.array([(mask >> k) & 1 for k in range(NMASK_BITS)], dtype=np.uint8)


def encode_action(action):
    return np.array([(action >> k) & 1 for k in range(NACTION_BITS)], dtype=np.uint8)


def decode_mask(bits):
    return int((bits * (1 << np.arange(NMASK_BITS))).sum())


def decode_action(bits):
    return int((bits * (1 << np.arange(NACTION_BITS))).sum())


def description_bits(priority):
    words = np.concatenate([prog.encode_rule(*w) for w in FIXED_WORDS])
    masks = np.concatenate([encode_mask(4 << b) for b in priority])
    actions = np.concatenate([encode_action(2 + b) for b in priority])
    return np.concatenate([words, encode_perm(priority), masks, actions])


def read_masks(desc):
    return [decode_mask(desc[MASK_OFFSET + i * NMASK_BITS:MASK_OFFSET + (i + 1) * NMASK_BITS])
            for i in range(NBANKS)]


def read_actions(desc):
    return [decode_action(desc[ACTION_OFFSET + i * NACTION_BITS:ACTION_OFFSET + (i + 1) * NACTION_BITS])
            for i in range(NBANKS)]


def build_program(desc):
    """Rebuild the 126-bit program from the 130-bit description. GENERIC over SYNTAX and
    ORDER-PRESERVING (the only validity check is that the stored permutation is a permutation)."""
    perm = decode_perm(desc[PERM_OFFSET:PERM_OFFSET + PERM_BITS])
    if sorted(perm) != list(range(4)):
        return None
    masks = read_masks(desc)
    actions = read_actions(desc)
    words = desc[:PERM_OFFSET].reshape(NWORDS, WIDTH)
    bank = np.concatenate([prog.encode_rule(1, m, a) for m, a in zip(masks, actions)])
    return np.concatenate([words[:4].ravel(), bank, words[4]])


# ---------------- slot / pointer / controller reads ----------------
def slot_offset(g):
    return g * SLOT_BITS


def read_slot(o, g):
    off = slot_offset(g)
    return (o.body.traces[1, off:off + SLOT_BITS].sum(axis=-1) > 3).astype(np.uint8)


def read_pointer(o):
    bits = (o.body.traces[1, PTR_OFFS].sum(axis=-1) > 3).astype(np.uint8)
    return int(2 * bits[0] + bits[1])


def desc_minority_active(o):
    g = read_pointer(o)
    ones = o.body.traces[1, slot_offset(g):slot_offset(g) + SLOT_BITS].sum(axis=-1)
    return int(np.minimum(ones, 7 - ones).sum())


def pointer_minority(o):
    ones = o.body.traces[1, PTR_OFFS].sum(axis=-1)
    return int(np.minimum(ones, 7 - ones).sum())


def read_ctrl(o):
    return (o.body.traces[1, CTRL_OFFS].sum(axis=-1) > 3).astype(np.uint8)


def ctrl_minority(o):
    ones = o.body.traces[1, CTRL_OFFS].sum(axis=-1)
    return int(np.minimum(ones, 7 - ones).sum())


def ctrl_fields(o):
    c = read_ctrl(o)
    active = int(c[0])
    phase = int(4 * c[1] + 2 * c[2] + c[3])
    last = int((c[4:18] * (1 << np.arange(14))).sum())
    return active, phase, last


def encode_ctrl(active, phase, last):
    c = np.zeros(CTRL_BITS, dtype=np.uint8)
    c[0] = active & 1
    c[1] = (phase >> 2) & 1; c[2] = (phase >> 1) & 1; c[3] = phase & 1
    for k in range(14):
        c[4 + k] = (last >> k) & 1
    return c


def resolve_offsets(o):
    idx = ac12.dead_rule_index(o)
    return [14 * idx + 1 + k for k in range(4)]


# ---------------- paid write primitives ----------------
def _cap(b, budget=None):
    cap = min(32, int(ac4.available(b)[:4].sum()) * 8, b.energy, b.material)
    return min(cap, budget) if budget is not None else cap


def write_toward_slot(o, e, g, desired, budget=None):
    b = o.body
    off = slot_offset(g)
    sites = np.argwhere(b.traces[1, off:off + SLOT_BITS] != desired[:, None])
    n = min(_cap(b, budget), len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, off + idx[:, 0], idx[:, 1]] = desired[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['succ_writes'] = e.get('succ_writes', 0) + n
    return n


def write_pointer(o, e, g):
    b = o.body
    bits = np.array([(g >> 1) & 1, g & 1], dtype=np.uint8)
    sites = np.argwhere(b.traces[1, PTR_OFFS] != bits[:, None])
    n = min(_cap(b), len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, [PTR_OFFS[i] for i in idx[:, 0]], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['succ_writes'] = e.get('succ_writes', 0) + n
    return n


def write_ctrl(o, e, c):
    """Write the controller state word toward `c` (paid). ATOMIC for the MODE field, budgeted for
    the timestamp (the AC88 correction, unchanged). Distinct resource from W-catalyzed content
    repair: bounded by the register size (126 replicas), paid 1 energy + 1 material per replica,
    not gated by 8*W."""
    b = o.body
    mode_sites = np.argwhere(b.traces[1, CTRL_OFFS[:4]] != c[:4, None])
    n_mode = len(mode_sites)
    if n_mode:
        if b.energy < n_mode or b.material < n_mode:
            return 0
        idx = mode_sites
        b.traces[1, CTRL_BASE + idx[:, 0], idx[:, 1]] = c[idx[:, 0]]
        b.energy -= n_mode; b.material -= n_mode
        e['spent_e'] += n_mode; e['spent_m'] += n_mode
        e['ctrl_writes'] = e.get('ctrl_writes', 0) + n_mode
    last_sites = np.argwhere(b.traces[1, CTRL_OFFS[4:]] != c[4:, None])
    n_last = min(len(last_sites), b.energy, b.material)
    if n_last:
        idx = last_sites[:n_last]
        b.traces[1, CTRL_BASE + 4 + idx[:, 0], idx[:, 1]] = c[4 + idx[:, 0]]
        b.energy -= n_last; b.material -= n_last
        e['spent_e'] += n_last; e['spent_m'] += n_last
        e['ctrl_writes'] = e.get('ctrl_writes', 0) + n_last
    return n_mode + n_last


# ---------------- in-place maintenance ----------------
def reg_description_active(o, e):
    b = o.body
    g = read_pointer(o)
    bits = read_slot(o, g)
    off = slot_offset(g)
    sites = np.argwhere(b.traces[1, off:off + SLOT_BITS] != bits[:, None])
    n = min(_cap(b), len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, off + idx[:, 0], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n
    return bits


def reg_pointer(o, e):
    b = o.body
    bits = (b.traces[1, PTR_OFFS].sum(axis=-1) > 3).astype(np.uint8)
    sites = np.argwhere(b.traces[1, PTR_OFFS] != bits[:, None])
    n = min(_cap(b), len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, [PTR_OFFS[i] for i in idx[:, 0]], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n
    return bits


def reg_ctrl(o, e):
    b = o.body
    bits = read_ctrl(o)
    sites = np.argwhere(b.traces[1, CTRL_OFFS] != bits[:, None])
    n = min(_cap(b), len(sites))
    if n:
        idx = sites[:n]
        b.traces[1, CTRL_BASE + idx[:, 0], idx[:, 1]] = bits[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n
    return bits


def reg_from_active(o, e, reg_offs):
    b = o.body
    target = build_program(read_slot(o, read_pointer(o)))
    if target is None:
        return
    exclude = set(reg_offs)
    sites = np.argwhere(b.traces[0, :prog.PROGRAM_BITS] != target[:, None])
    sites = sites[[i for i in range(len(sites)) if int(sites[i, 0]) not in exclude]]
    n = min(_cap(b), len(sites))
    if n:
        idx = sites[:n]
        b.traces[0, idx[:, 0], idx[:, 1]] = target[idx[:, 0]]
        b.energy -= n; b.material -= n
        e['spent_e'] += n; e['spent_m'] += n
        e['reg_writes'] = e.get('reg_writes', 0) + n


# ---------------- succession state machine ----------------
class Succession:
    def __init__(self, mode, encoded):
        self.mode = mode
        self.encoded = encoded
        self.log = []
        self._n = 0
        self._entry = None


def advance(o, e, succ, now, succ_trigger):
    if succ.mode != 'real':
        return
    active, phase, last = ctrl_fields(o)
    if not active:
        if succ_trigger and now - last >= SUCC_MIN_SPACING:
            src = read_pointer(o)
            tgt = (src + 1) % SLOTS
            write_ctrl(o, e, encode_ctrl(1, PHASE_COPY, now))
            succ._entry = dict(n=succ._n, source=src, target=tgt, start=now,
                               source_correct=int(np.array_equal(read_slot(o, src), succ.encoded)))
            succ._n += 1
        return
    source = read_pointer(o)
    target = (source + 1) % SLOTS
    if succ._entry is None:
        succ._entry = dict(n=succ._n, source=source, target=target, start=now,
                           source_correct=int(np.array_equal(read_slot(o, source), succ.encoded)))
        succ._n += 1
    if phase == PHASE_COPY:
        src_maj = read_slot(o, source)
        write_toward_slot(o, e, target, src_maj, SUCC_BUDGET)
        if np.array_equal(read_slot(o, target), src_maj):
            write_ctrl(o, e, encode_ctrl(1, PHASE_VERIFY, last))
            succ._entry['copy_done'] = now
    elif phase == PHASE_VERIFY:
        src_maj = read_slot(o, source)
        tgt_maj = read_slot(o, target)
        valid = build_program(tgt_maj) is not None
        correct = bool(np.array_equal(tgt_maj, src_maj))
        succ._entry['verified_valid'] = int(valid)
        succ._entry['target_correct'] = int(correct and
                                            bool(np.array_equal(tgt_maj, succ.encoded)))
        if valid and correct:
            write_ctrl(o, e, encode_ctrl(1, PHASE_SWITCH, last))
        else:
            write_ctrl(o, e, encode_ctrl(1, PHASE_COPY, last))
    elif phase == PHASE_SWITCH:
        src_maj = read_slot(o, source)
        tgt_maj = read_slot(o, target)
        if not (bool(np.array_equal(tgt_maj, src_maj)) and build_program(tgt_maj) is not None):
            write_ctrl(o, e, encode_ctrl(1, PHASE_COPY, last))
        else:
            write_pointer(o, e, target)
            if read_pointer(o) == target:
                write_ctrl(o, e, encode_ctrl(1, PHASE_REMOVE, last))
                succ._entry['switch_tick'] = now
    elif phase == PHASE_REMOVE:
        old_source = (source - 1) % SLOTS
        write_toward_slot(o, e, old_source, np.zeros(SLOT_BITS, dtype=np.uint8), SUCC_BUDGET)
        if not o.body.traces[1, slot_offset(old_source):slot_offset(old_source) + SLOT_BITS].any():
            write_ctrl(o, e, encode_ctrl(0, PHASE_IDLE, last))
            succ._entry['remove_tick'] = now
            succ._entry['done'] = True
            succ.log.append(succ._entry)


# ---------------- the injected maintenance step ----------------
def maintain(o, e, succ, reg_offs, cfg, now):
    obs2 = bool(ac9.observe(o) & 4)
    dm = desc_minority_active(o)
    pm = pointer_minority(o)
    cm = ctrl_minority(o)
    reg_trigger = obs2 or (cfg['repair'] and (dm >= DESC_TRIGGER or pm >= POINTER_TRIGGER))
    succ_trigger = dm >= DESC_TRIGGER
    if cfg['repair']:
        if reg_trigger:
            reg_description_active(o, e)
        if pm >= POINTER_TRIGGER:
            reg_pointer(o, e)
        if cfg['ctrl_maintain'] and cm >= CTRL_TRIGGER:
            reg_ctrl(o, e)
    if cfg['succession']:
        advance(o, e, succ, now, succ_trigger)
    if cfg['regen'] and reg_trigger:
        reg_from_active(o, e, reg_offs)


ACTION_LINE = "        action=prog.choose(b.traces,observe(o))"
BALANCE_LINE = "    ac4.balance(before,b,e)"


# ---------------- the W-birth gate (the AC91 intervention) ----------------
def make_birth(ns, cfg):
    """Gate bank-0 (W) births. When cfg['block_W'] is set, refuse bank-0 births until
    cfg['restore_tick'] (None = forever). Banks 1 and 2 (memory-region catalysts) are never
    touched, so the cut isolates exactly the W-birth reaction. Content (traces[0]/traces[1]) is
    never written by the gate -- only the birth outcome differs, so no controller content is
    supplied or altered by the restoration."""
    orig = ns['birth']
    block = cfg.get('block_W', False)
    restore = cfg.get('restore_tick', None)

    def gated(b, bank, parent, e):
        if bank == 0 and block and (restore is None or ns['now'] < restore):
            return False
        return orig(b, bank, parent, e)
    return gated


def build(ac_arm, alloc, succ, reg_offs, cfg):
    base, cut = ac71.arm_parts(ac_arm)
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['maintain'] = maintain
    ns['succ'] = succ
    ns['reg_offs'] = reg_offs
    ns['cfg'] = cfg
    if cfg.get('block_W'):
        ns['birth'] = make_birth(ns, cfg)
    assert src.count(ac12.RENEW_BLOCK) == 1
    src = src.replace(ac12.RENEW_BLOCK, ac12.RENEW_BLOCK_NEW)
    ns['ac12_memory'] = ac12.m12
    ns['allowance'] = alloc.allowance
    assert src.count(ac12.OUTCOME_LINE) == 1
    src = src.replace(ac12.OUTCOME_LINE, ac12.OUTCOME_LINE + "\n            alloc.outcome(o,action,e)")
    ns['alloc'] = alloc
    assert src.count(ac71.DAMAGE_LINE) == 1
    src = src.replace(ac71.DAMAGE_LINE, ac71.DAMAGE_LINE_STICKY)
    assert src.count(ACTION_LINE) == 1
    src = src.replace(ACTION_LINE, "        maintain(o,e,succ,reg_offs,cfg,now)\n" + ACTION_LINE)
    assert src.count(BALANCE_LINE) == 1
    src = src.replace(BALANCE_LINE,
                      "    e['writes']+=e.get('reg_writes',0)+e.get('succ_writes',0)+e.get('ctrl_writes',0)\n"
                      + BALANCE_LINE)
    shim = {k: getattr(ac4, k) for k in dir(ac4) if not k.startswith('_')}
    react = ac12.react_world()
    if cut:
        react = (lambda b, action, a, e, _f=react: _f(b, action, 'no_policy_write', e))
    shim['react'] = react
    ns['ac4'] = SimpleNamespace(**shim)
    ns['now'] = 0
    fns = {}
    exec(compile(src, 'ac91_step', 'exec'), ns, fns)
    return fns['step']


# ---------------- allocation (erase-on-relinquish, AC75 + the AC82 _restore fix) ----------------
class AllocErase(ac12.Alloc):
    def outcome(self, o, key, e):
        if self.arm != 'allocate':
            return
        key = int(key)
        if e['productive'] > 0:
            self._restore(o, e, key)
            self.streak[key] = 0
            return
        self.streak[key] = self.streak.get(key, 0) + 1
        if self.streak[key] >= ac12.STREAK_N:
            self._drop(o, e, key)

    def _restore(self, o, e, key):
        place = ac12.m12.slot_of_key(o.memory, key)
        if place is None:
            return
        off = self.offs[2 * place[0] + place[1]]
        if not ac12.bit_value(o, off):
            return
        sites = o.body.traces[0, off]
        n = int((sites != 0).sum())
        if n == 0:
            return
        cap = min(32, 8 * int(ac4.available(o.body)[:4].sum()), o.body.energy, o.body.material)
        if n > cap:
            return
        o.body.energy -= n; o.body.material -= n
        e['spent_e'] += n; e['spent_m'] += n; e['writes'] += n
        sites[:] = 0
        self.log.setdefault('restored', []).append(list(place))

    def _drop(self, o, e, key):
        place = ac12.m12.slot_of_key(o.memory, key)
        if place is None:
            return
        off = self.offs[2 * place[0] + place[1]]
        sites = o.body.traces[0, off]
        n = int((sites != 1).sum())
        if n == 0:
            return
        cap = min(32, 8 * int(ac4.available(o.body)[:4].sum()), o.body.energy, o.body.material)
        if n > cap:
            return
        o.body.energy -= n; o.body.material -= n
        e['spent_e'] += n; e['spent_m'] += n; e['writes'] += n
        sites[:] = 1
        self.streak[key] = 0
        self.log['dropped'].append(list(place))
        r, s = place
        live = int((o.memory.life[r, s] > 0).sum())
        if live:
            o.memory.life[r, s] = 0
            o.memory.bits[r, s] = 0
            e['memory_expiry'] += live


# ---------------- run ----------------
def mapping_at(base, t, transition, move_tick=MOVE_TICK):
    m = list(base)
    if transition == 'perm' and t >= move_tick:
        m[1] = 1 - base[1]
    return m


def run(seed, history, arm, damage=True, corrupt=True, transition='none', ticks=TICKS,
        move_tick=MOVE_TICK):
    ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
    ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
    ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac71.DEV
    ac12.REGISTER_THRESHOLD = 4
    _, _, _, priority = ac4.acquire(seed)
    alloc = AllocErase('allocate', seed, history)
    o, offs = ac12.acquire(seed)
    alloc.offs = offs
    alloc.shadow = o.body.traces[0].copy()
    reg_offs = resolve_offsets(o)
    encoded = description_bits(priority)
    o.body.traces[1, :DESC_BITS] = encoded[:, None]
    acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    cfg = ARM_PARTS[arm]
    succ = Succession('real' if cfg['succession'] else 'none', encoded)
    step = build(cfg['ac_arm'], alloc, succ, reg_offs, cfg)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])
    total = ac9.event()
    total['reg_writes'] = 0
    total['succ_writes'] = 0
    total['ctrl_writes'] = 0
    first_dead = None
    first_W_empty = None
    W_min_seen = 99
    W_at_corruption = None
    alive_at_corruption = None
    description_correct_intervention = None
    description_correct_at_death = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage:
            g = read_pointer(o)
            slots = {g}
            active, phase, last = ctrl_fields(o)
            if active:
                slots.add((g + 1) % SLOTS)
            for s in slots:
                off = slot_offset(s)
                o.body.traces[1, off:off + SLOT_BITS] |= (rng1.random((SLOT_BITS, 7)) < .0001).astype(np.uint8)
            o.body.traces[1, PTR_OFFS] |= (rng1.random((2, 7)) < .0001).astype(np.uint8)
            o.body.traces[1, CTRL_OFFS] |= (rng1.random((CTRL_BITS, 7)) < .0001).astype(np.uint8)
        if t == CORRUPT_TICK and corrupt:
            for bit in range(CORRUPT_BITS):
                w = 1 - int(acquired[bit])
                o.body.traces[0, bit, 0:4] = w
                o.body.traces[0, bit, 4:7] = int(acquired[bit])
        step.__globals__['now'] = t
        e = step(o, core, noise, directions, coin, tuple(mapping_at(base_map, t, transition, move_tick)),
                 [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        W = int((o.body.life[:4] > 0).sum())
        W_min_seen = min(W_min_seen, W)
        if first_W_empty is None and W == 0:
            first_W_empty = t
        if t == CORRUPT_TICK:
            W_at_corruption = W
            alive_at_corruption = not o.body.dead
            description_correct_intervention = int((read_slot(o, read_pointer(o)) == encoded).sum())
        if first_dead is None and o.body.dead:
            first_dead = t
            description_correct_at_death = int((read_slot(o, read_pointer(o)) == encoded).sum())
    inv = ac4.inventory(o.body)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    static = np.ones(prog.PROGRAM_BITS, dtype=bool)
    static[list(reg_offs)] = False
    desc_bits = read_slot(o, read_pointer(o))
    desc_priority = decode_perm(desc_bits[PERM_OFFSET:PERM_OFFSET + PERM_BITS])
    active_end, phase_end, last_end = ctrl_fields(o)
    W_births_bank0 = int(total['W_birth'] - total['region0_births'] - total['region1_births'])
    return dict(seed=seed, history=history, arm=arm, damage=damage, corrupt=corrupt,
                transition=transition, ticks=ticks, move_tick=move_tick,
                completed=total['active'] == ticks, first_dead=first_dead,
                first_W_empty=first_W_empty, W_min_seen=W_min_seen,
                W_at_corruption=W_at_corruption,
                alive_at_corruption=alive_at_corruption,
                successions=len([s for s in succ.log if s['done']]),
                succession_log=succ.log,
                pointer=read_pointer(o),
                ctrl=(dict(active=active_end, phase=phase_end, last=last_end)),
                ctrl_idle_end=int(active_end == 0 and phase_end == PHASE_IDLE),
                ctrl_minority_end=ctrl_minority(o),
                description_correct=int((desc_bits == encoded).sum()),
                description_correct_intervention=description_correct_intervention,
                description_correct_at_death=description_correct_at_death,
                description_valid=int(sorted(desc_priority) == list(range(4))),
                description_same=int(desc_priority == tuple(priority)),
                program_correct=int((decoded[static] == acquired[static]).sum()),
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != acquired[:CORRUPT_BITS]).sum()),
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                W_births=int(total['W_birth']),
                region0_births=int(total['region0_births']),
                region1_births=int(total['region1_births']),
                W_births_bank0=W_births_bank0,
                C_births=int(total['C_birth']), B_births=int(total['B_birth']),
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                routes=[o.memory.read(k) for k in (0, 1)],
                demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                state_hash=o.digest())


# ---------------- gates ----------------
def gates(rows):
    def pick(arm, damage, corrupt, transition):
        return [r for r in rows
                if r['arm'] == arm and r['damage'] == damage and r['corrupt'] == corrupt
                and r['transition'] == transition]

    succ = pick('succession', True, True, 'none')      # damaged + corrupted, core schedule
    repair = pick('repair', True, True, 'none')
    no_W = pick('no_W', True, True, 'none')
    W_restore = pick('W_restore', True, True, 'none')
    W_restore_late = pick('W_restore_late', True, True, 'none')
    unmaintained = pick('unmaintained', True, True, 'none')
    no_repair = pick('no_repair', True, True, 'none')

    return {
        # Link 1: blocking production reduces the machinery (W -> 0), then reconstruction capacity
        # (8*W -> 0) and coordination capacity, and kills the organism.
        'G1_block_reduces_machinery_then_capacity': (
            all(r['first_W_empty'] is not None and r['first_W_empty'] <= 64 for r in no_W)
            and all(r['W'] == 0 and r['W_births_bank0'] == 0 for r in no_W)
            and all(not r['completed'] for r in no_W)
            and all(r['reg_writes'] < 100 for r in no_W)),
        # Link 2: restoring W production rescues reconstruction -- every W_restore individual
        # reconstructs (fw==0), keeps the description intact (130/130), and its W production resumes
        # (W_births_bank0 > 0). The restoration supplies no content (see G2b / unit test).
        'G2_restore_rescues_reconstruction': (
            all(r['completed'] and r['flipped_still_wrong'] == 0 and r['description_correct'] == DESC_BITS
                and r['W_births_bank0'] > 0 and r['W'] >= 2 for r in W_restore)),
        # Link 2 (autocatalytic boundary): a restore after W has died out (t=64) cannot restart W
        # -- W-birth needs a live W parent -- so W_restore_late dies exactly like no_W.
        'G3_restore_late_is_irreversible': (
            all(not r['completed'] and r['W'] == 0 and r['W_births_bank0'] == 0
                for r in W_restore_late)),
        # Link 3: ordinary operation replaces W repeatedly (births >= the 4-slot complement) while
        # controller information (desc 130/130) and organizational continuity (survival, fw==0)
        # persist -- unconditional (dead or alive).
        'G4_turnover_while_content_persists': (
            all(r['W_births_bank0'] >= 4 for r in succ + repair)
            and all(r['description_correct'] == DESC_BITS and r['flipped_still_wrong'] == 0
                    for r in succ + repair)),
        # Retained repair-only arm: replacement is a capability, not a necessity -- repair (succession
        # off) survives with the description intact and reconstruction working.
        'G5_repair_only_survives': (
            all(r['completed'] and r['successions'] == 0 and r['description_correct'] == DESC_BITS
                and r['flipped_still_wrong'] == 0 for r in repair)),
        # Controls: reconstruction + repair are load-bearing (unmaintained and no_repair die).
        'G6_controls_die': (
            all(not r['completed'] for r in unmaintained)
            and all(not r['completed'] for r in no_repair)),
        'G7_completeness_determinism': None,
    }


def equivalence_check():
    """Re-run the AC89 schedule (simultaneous corrupt+move) on the AC89 final seed family for the
    four shared arms and compare byte-identically (state_hash) to the frozen AC89 rows. Proves this
    runner is a correct extension: the W-birth gate is a no-op for the shared arms."""
    import ac89
    frozen = [json.loads(l) for l in Path('ac89_results_v1/rows.jsonl').read_text().splitlines()]
    shared = ('succession', 'repair', 'unmaintained', 'no_repair')
    seeds = [4052, 4054, 4096, 4110]
    n_checked = 0
    for seed in seeds:
        for history in (0, 1):
            for arm in shared:
                for damage in (True, False):
                    for corrupt in (True, False):
                        for transition in ('perm', 'none'):
                            want = [r for r in frozen
                                    if r['seed'] == seed and r['history'] == history
                                    and r['arm'] == arm and r['damage'] == damage
                                    and r['corrupt'] == corrupt and r['transition'] == transition]
                            if not want:
                                continue
                            got = run(seed, history, arm, damage, corrupt, transition,
                                      move_tick=MOVE_TICK)
                            assert got['state_hash'] == want[0]['state_hash'], \
                                f"mismatch {seed}/{history}/{arm}/{damage}/{corrupt}/{transition}"
                            n_checked += 1
    return n_checked


def preflight(protocol='AC91_PROTOCOL_v1.md'):
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


def collect(root, seeds, transition='none'):
    preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    conds = [(a, d, c) for a in ARMS for d in (True, False) for c in (True, False)]
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for (a, d, c) in conds:
                    r = run(seed, history, a, d, c, transition, move_tick=MOVE_TICK)
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['arm'], r['damage'], r['corrupt'], r['completed'], r['first_dead'],
                 r['first_W_empty'], r['W'], r['W_births_bank0'], r['flipped_still_wrong'],
                 r['description_correct'], r['successions'])
                for r in rows[-2 * len(conds):]]), default=str), flush=True)
    g = gates(rows)
    g['G7_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(conds)
        and all(run(s, h, a, d, c, transition, move_tick=MOVE_TICK) == orig
                for s, h, a, d, c, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0]['damage'],
                  rows[0]['corrupt'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows, transition=transition), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac91_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    if '--equivalence' in sys.argv:
        n = equivalence_check()
        print(f"equivalence check: {n} rows byte-identical to frozen AC89")
        return
    collect('ac91_results_v1', [4200, 4201, 4202, 4203])


if __name__ == '__main__':
    main()
