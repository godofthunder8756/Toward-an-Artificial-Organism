"""AC89: re-test the integrated architecture on the previously-failing priority and the
simultaneous challenge.

AC87's composition result (succession holds both routes 8/8 under corrupt@t=8192 + channel-1
move@t=12288) has two recorded gaps, which this study closes as a BOUNDED RE-TEST -- not new
machinery:

1. AC87's finals 4028-4031 have priorities [3,2,1,0], [1,2,3,0], [1,2,0,3], [3,0,1,2] -- NONE
   ranks the bank-1 renewal rule LAST. AC83 located the route-holding failure in exactly the
   adversarial priority [3,0,2,1] (renewal rule last, after the boundary rule, so renewal is
   preempted and the route churns/expires). This study runs the composition on final seeds whose
   acquisition priority IS [3,0,2,1].
2. AC87 SEPARATES the two interventions in time (corrupt@8192, move@12288). AC82 showed the
   SIMULTANEOUS (coincident-tick) corruption+move drives the non-composition (reconstruction cost +
   the move's income cut set obs bit 1, preempting renewal). This study runs the SIMULTANEOUS
   challenge: corruption and the route move land on the SAME tick (MOVE_TICK == CORRUPT_TICK).

Both are tested with the CORRECTED (post-AC88) runner -- the MODE/last atomic controller write, the
distinct-resource model, the order-preserving generic-over-syntax decoder -- and AC75's
erase-on-relinquish route adaptation. Survival, reconstruction (fw==0), description integrity
(130/130) and route-holding are reported UNCONDITIONALLY (per individual, dead or alive), with the
AC68-bimodality-aware lower-bound caveat. If the adversarial priority or the simultaneous challenge
breaks composition, that is the honest answer and is recorded, not softened.

This runner is derived from ac88.py (the corrected AC87 implementation). The ONLY differences from
ac88.py are: (1) MOVE_TICK == CORRUPT_TICK (simultaneous schedule) instead of 12288, (2) the final
seed family (adversarial priority [3,0,2,1]), and (3) the gate shape for the composition re-test
(G8 is unconditional on reconstruction, and route-holding/survival are reported, not gated).
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
MOVE_TICK = CORRUPT_TICK            # SIMULTANEOUS: the route move lands on the same tick as the
                                    # corruption (AC82's coincident-tick challenge), not t=12288.

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
DESC_TRIGGER = 2          # active-slot minority-count trigger (description repair + succession)
POINTER_TRIGGER = 2       # pointer's own minority-count trigger
CTRL_TRIGGER = 2          # controller state's own minority-count trigger

PTR_BASE = SLOTS * SLOT_BITS                          # 520
PTR_OFFS = [PTR_BASE, PTR_BASE + 1]

CTRL_BASE = PTR_BASE + 2                              # 522
CTRL_BITS = 18
CTRL_OFFS = np.arange(CTRL_BASE, CTRL_BASE + CTRL_BITS)
# controller word layout (0-based within the word):
#   0: ACTIVE (1 bit)  1-3: PHASE (3 bits)  4-17: LAST_START (14 bits)
# source/target are NOT stored: they are derived from the generation pointer (itself vulnerable and
# maintained) -- source = the active slot (read_pointer) during copy/verify/switch, and the slot to
# clear during remove is (pointer-1)%SLOTS; target = (pointer+1)%SLOTS. Only the non-derivable
# working state (active, phase, last-start) is stored.
PHASE_IDLE, PHASE_COPY, PHASE_VERIFY, PHASE_SWITCH, PHASE_REMOVE = range(5)

ARMS = ('succession', 'repair', 'ctrl_unmaintained', 'unmaintained', 'no_repair')

# per-arm config
ARM_PARTS = {
    'succession':        dict(ac_arm='regen',     repair=True,  regen=True,  succession=True,  ctrl_maintain=True),
    'repair':            dict(ac_arm='regen',     repair=True,  regen=True,  succession=False, ctrl_maintain=True),
    'ctrl_unmaintained': dict(ac_arm='regen',     repair=True,  regen=True,  succession=True,  ctrl_maintain=False),
    'unmaintained':      dict(ac_arm='regen',     repair=False, regen=True,  succession=False, ctrl_maintain=False),
    'no_repair':         dict(ac_arm='no_repair', repair=False, regen=False, succession=False, ctrl_maintain=False),
}

SOURCES = ['ac89.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC89_PROTOCOL_v1.md']


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
    """The 130-bit description installed at acquisition (inherited content)."""
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
    ORDER-PRESERVING.

    The only validity check is syntactic: the stored permutation must be a permutation. A stored
    mask or action that is syntactically valid (any 9-bit mask, any 4-bit action) but NOT the
    designer's convention (mask 4<<b, action 2+b) decodes FAITHFULLY into a working, possibly worse
    program -- it is not rejected by an external correctness rule. The five rule words are copied
    verbatim; the four bank rules are READ from the stored masks/actions (never derived from a bank
    index); the boundary word (mask 256) is placed LAST per the acquired layout.
    """
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
    """Write slot g's replicas toward `desired` (130-bit), paid at the frozen per-action cap."""
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
    the timestamp.

    The 18-bit word is two fields: MODE (active+phase, bits 0-3) and LAST (start timestamp, bits
    4-17). MODE is the load-bearing transition state: a partially-written mode (e.g. phase read as a
    different valid phase mid-transition) is what corrupted the first AC87 build, so it is written
    all-or-nothing -- if energy or material cannot fund the full mode transition, NOTHING is written
    and the transition is refused (retried next tick). Mode transitions change at most 3 of the 4
    bits (<= 21 replicas). LAST is rate-limit bookkeeping, read only by the SUCC_MIN_SPACING check
    while idle (~300 ticks after a start); a partially-updated timestamp is still a valid 14-bit
    integer and cannot corrupt the state machine, so it is written toward the target in
    energy/material-budgeted increments (the frozen behaviour), like write_toward_slot.

    Resource model (distinct resource): the controller register is the coordinator's OWN working
    state -- its program counter, SET by the machine's own transitions, not repaired content. It is a
    distinct resource from the W-catalyzed CONTENT repair (ac4.react actions 2-5, where the 8*W term
    is the repair catalyst's per-action capacity): the controller write is bounded by the register
    size (18 bits x 7 = 126 replicas) and pays the physical price (1 energy + 1 material per replica,
    so the conservation identities hold), but it is not gated by 8*W. Returns the number of replicas
    written (0 if the mode transition was refused)."""
    b = o.body
    # MODE (bits 0-3): atomic, all-or-nothing
    mode_sites = np.argwhere(b.traces[1, CTRL_OFFS[:4]] != c[:4, None])
    n_mode = len(mode_sites)
    if n_mode:
        if b.energy < n_mode or b.material < n_mode:
            return 0                      # atomic: refuse the whole mode transition, never a partial mode
        idx = mode_sites
        b.traces[1, CTRL_BASE + idx[:, 0], idx[:, 1]] = c[idx[:, 0]]
        b.energy -= n_mode; b.material -= n_mode
        e['spent_e'] += n_mode; e['spent_m'] += n_mode
        e['ctrl_writes'] = e.get('ctrl_writes', 0) + n_mode
    # LAST (bits 4-17): budgeted toward (rate-limit bookkeeping, frozen behaviour)
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


# ---------------- succession state machine (working state in the substrate) ----------------
class Succession:
    """Observer-side provenance for the succession machinery. The working state (active / source /
    target / phase / last-start) lives in the vulnerable substrate; this object holds only the
    per-cycle observation log."""
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
    # source/target are derived from the generation pointer (vulnerable + maintained): during
    # copy/verify/switch the active slot is the source and (pointer+1)%SLOTS is the target; during
    # remove the slot to clear is (pointer-1)%SLOTS (the old source, after the pointer advanced).
    source = read_pointer(o)
    target = (source + 1) % SLOTS
    # A spurious activation (active read as 1 without a recorded start, from unmaintained controller
    # damage) is treated as a start at the current tick: the machinery stays well-defined on any
    # controller state, and the degradation is measured at the endpoint, not by crashing.
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
        # re-verify before switching: the successor is exposed to damage, so it may have been hit
        # after the verify phase passed.
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


def build(ac_arm, alloc, succ, reg_offs, cfg):
    base, cut = ac71.arm_parts(ac_arm)
    src = ac12.STEP_SRC
    ns = dict(vars(ac9))
    ns['maintain'] = maintain
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
    exec(compile(src, 'ac87_step', 'exec'), ns, fns)
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
        if not ac12.bit_value(o, off):       # already maintained -> no-op
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


def run(seed, history, arm, damage=True, corrupt=True, transition='perm', ticks=TICKS,
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
    o.body.traces[1, :DESC_BITS] = encoded[:, None]          # slot 0 = acquisition recipe
    acquired = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    cfg = ARM_PARTS[arm]
    succ = Succession('real' if cfg['succession'] else 'none', encoded)
    step = build(cfg['ac_arm'], alloc, succ, reg_offs, cfg)
    base_map = (seed % 2, (seed // 2) % 2)
    rng = np.random.default_rng([seed, 1509])
    rng1 = np.random.default_rng([seed, 1609])      # independent damage stream for bank 1
    total = ac9.event()
    total['reg_writes'] = 0
    total['succ_writes'] = 0
    total['ctrl_writes'] = 0
    first_dead = None
    alive_at_corruption = None
    alive_at_move = None
    description_correct_intervention = None
    for t in range(ticks):
        alloc.now = t
        core = (rng.random((126, 7)) < .0001).astype(np.uint8)
        noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
        directions = rng.integers(0, 4, 20, dtype=np.uint8)
        coin = bool(rng.random() < .5)
        if damage:
            # damage the ACTIVE slot AND the successor (target) slot -- not only the active slot --
            # plus the pointer and the controller state, all sticky.
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
        # `now` is the host-supplied tick clock injected into the built step namespace.
        step.__globals__['now'] = t
        e = step(o, core, noise, directions, coin, tuple(mapping_at(base_map, t, transition, move_tick)),
                 [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        if t == CORRUPT_TICK:
            alive_at_corruption = not o.body.dead
            description_correct_intervention = int((read_slot(o, read_pointer(o)) == encoded).sum())
        if t == move_tick:
            alive_at_move = not o.body.dead
        if first_dead is None and o.body.dead:
            first_dead = t
    inv = ac4.inventory(o.body)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    static = np.ones(prog.PROGRAM_BITS, dtype=bool)
    static[list(reg_offs)] = False
    desc_bits = read_slot(o, read_pointer(o))
    desc_priority = decode_perm(desc_bits[PERM_OFFSET:PERM_OFFSET + PERM_BITS])
    active_end, phase_end, last_end = ctrl_fields(o)
    final_port1 = (1 - base_map[1]) if transition == 'perm' else base_map[1]
    return dict(seed=seed, history=history, arm=arm, damage=damage, corrupt=corrupt,
                transition=transition, ticks=ticks, move_tick=move_tick,
                completed=total['active'] == ticks, first_dead=first_dead,
                alive_at_corruption=alive_at_corruption, alive_at_move=alive_at_move,
                successions=len([s for s in succ.log if s['done']]),
                succession_log=succ.log,
                pointer=read_pointer(o),
                ctrl=(dict(active=active_end, phase=phase_end, last=last_end)),
                ctrl_idle_end=int(active_end == 0 and phase_end == PHASE_IDLE),
                ctrl_minority_end=ctrl_minority(o),
                description_correct=int((desc_bits == encoded).sum()),
                description_correct_intervention=description_correct_intervention,
                description_valid=int(sorted(desc_priority) == list(range(4))),
                description_same=int(desc_priority == tuple(priority)),
                program_correct=int((decoded[static] == acquired[static]).sum()),
                flipped_still_wrong=int((decoded[:CORRUPT_BITS] != acquired[:CORRUPT_BITS]).sum()),
                W=int((o.body.life[:4] > 0).sum()), C=int((o.body.life[16:20] > 0).sum()),
                energy=inv[0], material=inv[1], fuel=inv[2],
                writes=int(total['writes']), reg_writes=int(total['reg_writes']),
                succ_writes=int(total['succ_writes']), ctrl_writes=int(total['ctrl_writes']),
                routes=[o.memory.read(k) for k in (0, 1)],
                route1_correct=bool(o.memory.read(1) == final_port1),
                demand=o.memory.demand().tolist(),
                register=[ac12.bit_value(o, off) for off in offs],
                relinquishments=len(alloc.log['dropped']),
                restorations=len(alloc.log.get('restored', [])),
                state_hash=o.digest())


def gates(rows):
    def pick(arm, damage, corrupt, transition):
        return [r for r in rows
                if r['arm'] == arm and r['damage'] == damage and r['corrupt'] == corrupt
                and r['transition'] == transition]

    succ = pick('succession', True, False, 'none')
    repair = pick('repair', True, False, 'none')
    ctrl_unm = pick('ctrl_unmaintained', True, False, 'none')
    unmaintained = pick('unmaintained', True, True, 'perm')
    no_repair = pick('no_repair', True, True, 'perm')
    succ_ctrl = pick('succession', False, False, 'none')
    repair_ctrl = pick('repair', False, False, 'none')
    succ_comp = pick('succession', True, True, 'perm')
    return {
        'G1_succession_occurs': all(
            r['successions'] >= 2 for r in succ if r['completed']),
        'G2_successor_functional': all(
            (r['successions'] >= 2
             and all(s['verified_valid'] == 1 and s['target_correct'] == 1
                     for s in r['succession_log'] if s['done'])
             and r['description_correct'] == DESC_BITS and r['description_valid'] == 1)
            for r in succ if r['completed']),
        'G3_remove_after_verify': all(
            all(s['remove_tick'] >= s['switch_tick'] >= s['copy_done'] >= s['start']
                for s in r['succession_log'] if s['done'])
            for r in succ if r['completed']),
        'G4_recipe_maintained': (
            all(r['description_correct'] == DESC_BITS for r in succ if r['completed'])
            and all(r['description_correct'] == DESC_BITS for r in repair if r['completed'])
            and all(r['description_correct'] < DESC_BITS for r in unmaintained)),
        'G5_succession_is_the_replacer': (
            all(r['successions'] == 0 for r in repair)
            and all(r['successions'] == 0 for r in unmaintained)
            and all(r['successions'] >= 2 for r in succ if r['completed'])),
        'G6_controller_state_maintained': (
            all(r['ctrl_idle_end'] == 1 and r['ctrl_minority_end'] <= 1
                for r in succ if r['completed'])
            and all(r['ctrl_minority_end'] >= 4 for r in ctrl_unm)),
        'G7_control_clean': (
            all(r['successions'] == 0 for r in succ_ctrl + repair_ctrl)
            and all(r['description_correct'] == DESC_BITS for r in succ_ctrl + repair_ctrl)
            and all(succ_ctrl[i]['state_hash'] == repair_ctrl[i]['state_hash']
                    for i in range(len(succ_ctrl)))),
        'G8_composition': (
            # reconstruction is UNCONDITIONAL: fw==0 in EVERY individual, dead or alive (AC82)
            all(r['flipped_still_wrong'] == 0 for r in succ_comp)
            # description intact at the intervention in every individual, and at end in every
            # survivor (post-mortem degradation is excluded -- AC79's survivor-conditioning caveat)
            and all(r['description_correct_intervention'] == DESC_BITS for r in succ_comp)
            and all(r['description_correct'] == DESC_BITS for r in succ_comp if r['completed'])
            # the repair/reconstruction is load-bearing: no repair -> die
            and all(not r['completed'] for r in unmaintained)
            and all(not r['completed'] for r in no_repair)
            # non-vacuity: the mechanism is exercised (at least one succession survivor)
            and any(r['completed'] for r in succ_comp)),
        'G9_completeness_determinism': None,
    }


def composition_report(rows):
    """The unconditional (per-individual, dead or alive) composition endpoints the card asks to
    report: survival, reconstruction (fw==0), description integrity (130/130), route-holding.
    Returned as a dict; NOT gates (survival is a bimodality-aware lower bound; route-holding is the
    endpoint that may legitimately fail under the adversarial priority + simultaneous challenge)."""
    succ_comp = [r for r in rows if r['arm'] == 'succession' and r['damage'] and r['corrupt']
                 and r['transition'] == 'perm']
    n = len(succ_comp)
    survive = [r['completed'] for r in succ_comp]
    fw = [r['flipped_still_wrong'] == 0 for r in succ_comp]
    desc_end = [r['description_correct'] == DESC_BITS for r in succ_comp]
    desc_int = [r['description_correct_intervention'] == DESC_BITS for r in succ_comp]
    hold = [r['completed'] and r['routes'][0] is not None and r['routes'][1] is not None
            and r['route1_correct'] for r in succ_comp]
    per = [dict(seed=r['seed'], history=r['history'], completed=r['completed'],
                first_dead=r['first_dead'], fw=r['flipped_still_wrong'],
                desc_end=r['description_correct'], desc_int=r['description_correct_intervention'],
                routes=r['routes'], route1_correct=r['route1_correct'], demand=r['demand'],
                W=r['W'], C=r['C'], energy=r['energy'])
           for r in succ_comp]
    return dict(n=n, survive=sum(survive), fw_zero=sum(fw),
                desc_end=sum(desc_end), desc_int=sum(desc_int), hold_both=sum(hold),
                per_individual=per)


def preflight(protocol='AC89_PROTOCOL_v1.md'):
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


def collect(root, seeds, move_tick=MOVE_TICK):
    preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    conds = [(a, d, c, t) for a in ARMS for d in (True, False)
             for c in (True, False) for t in ('perm', 'none')]
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for (a, d, c, t) in conds:
                    r = run(seed, history, a, d, c, t, move_tick=move_tick)
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, outcomes=[
                (r['arm'], r['damage'], r['corrupt'], r['transition'], r['completed'],
                 r['first_dead'], r['successions'], r['description_correct'],
                 r['flipped_still_wrong'], r['routes'])
                for r in rows[-2 * len(conds):]]), default=str), flush=True)
    g = gates(rows)
    g['G9_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(conds)
        and all(run(s, h, a, d, c, t, move_tick=move_tick) == orig
                for s, h, a, d, c, t, orig in
                [(rows[0]['seed'], rows[0]['history'], rows[0]['arm'], rows[0]['damage'],
                  rows[0]['corrupt'], rows[0]['transition'], rows[0])]))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows, move_tick=move_tick,
             composition_report=composition_report(rows)), indent=2))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    print(json.dumps(dict(composition_report=composition_report(rows)), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac89_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    collect('ac89_results_v1', [4052, 4054, 4096, 4110])


if __name__ == '__main__':
    main()
