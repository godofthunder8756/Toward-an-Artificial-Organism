"""AC93: coordinator transitions enacted by produced machinery (write_ctrl becomes W-gated).

AC92 established the functional interruption-and-rescue of reconstruction, and pinned the
W-DEPENDENT / W-INDEPENDENT split: every content write on the reconstruction/coordination path is
gated by the W repair catalyst's per-action capacity `_cap = min(32, 8*available_W, energy,
material)`, EXCEPT the coordinator's own transition write `write_ctrl`, which AC88 declared a
DISTINCT resource (bounded by register size 126 replicas, paid 1 energy + 1 material per replica,
NOT gated by 8*W).

AC93 revokes that distinct-resource declaration on a NEW architecture (the frozen AC88/AC92 rows
remain the comparator) and makes `write_ctrl` gated by the same `_cap` as every other content
write, so coordinator state transitions become a service the produced finite-lived machinery
performs, not a host operation always available for energy and material alone.

The machinery is the W repair catalyst (bank 0, `body.life[:4]`): finite-lived (life 64),
produced (action 6, paid 4 material + 2 energy), autocatalytic (a bank-0 birth needs a live bank-0
parent, so W=0 is irreversible without an external re-seed). The write-capacity term is
`available_W = int(ac4.available(b)[:4].sum())`; W=0 => cap 0, W=3 (the deterministic steady
state) => cap 24.

The gating rule (Decision 2 of AC93_DESIGN_v1.md, as amended by errata E2), preserving the AC88
atomic-vs-budgeted field split:

1. MODE field (bits 0-3: active + phase) -- atomic, all-or-nothing, now under `_cap`. If
   `len(mode_sites) > _cap(b)`, refuse the whole transition and write nothing (retried next tick);
   otherwise write all mode_sites. A mode transition changes at most 3 of the 4 bits (<= 21
   replicas), so with W=3 the added 8*W=24 term never binds and gated MODE coincides with ungated.
2. LAST field (bits 4-17: start timestamp) -- budgeted by energy + material ALONE (the frozen
   AC88 distinct-resource model), NOT W-gated. E2 amendment: the timestamp is rate-limit
   bookkeeping, not a state transition; its succession-start write is bounded by the timestamp
   DELTA (~35-69 replicas), which 8*W=24 cannot fund, and a permanently-truncated timestamp
   disables the SUCC_MIN_SPACING rate limiter (E1).

What remains W-independent (re-classified honestly -- Decision 3): (a) memory-region renewal
(`mem.renew`, actions 3-5) is gated by the region catalysts (banks 1-2) via the capacity argument,
a different produced-catalyst population with its own per-action capacity; (b) the production
reactions themselves (`ac4.react`: W/C births, B birth, energy conversion) produce the machinery
and cannot be 8*W-gated without circularity (W produces W); (c) environmental decay (damage stream,
memory aging/expiry) is not a write. So the honest statement is: every paid write the coordinator
and reconstruction machinery performs is W-gated; the only non-W-gated paid activity is the
production of the machinery itself and the region-catalyst renewal, both enacted by produced
catalysts under their own physical prerequisites.

Arms (D2 engineering):
- `gated`   -- the AC93 architecture: `write_ctrl` W-gated (Decision 2). All other primitives
               already W-gated, unchanged. Baseline mechanism arm.
- `ungated` -- the frozen comparator: `write_ctrl` NOT W-gated (the AC88/AC92 distinct-resource
               model), reproduced byte-for-byte from the frozen AC92 `intact` rows to prove the
               runner is a correct extension.

Clean-control expectation (declared up front, AC93_DESIGN_v1.md section 5): with W at the
deterministic steady state 3 and no interruption, 8*W=24 >= 21 (largest MODE transition), so the
added W condition in the MODE refusal never binds and `gated` and `ungated` must be
state_hash-identical on every condition. D2 verifies this empirically; any divergence is an errata
candidate, not a silent fix.

Arms (D4 finals):
- `gated`/`ungated` — the AC93 architecture vs the frozen AC88/AC92 comparator (write_ctrl
  W-gated vs distinct-resource). Swept on all four (damage x corrupt) conditions.
- `W_block`/`W_rescue` — `gated` + W production cut during a FORCED succession; `W_rescue`
  adds the machinery-only restore at RESCUE_TICK.
- `W_block_ungated` — the direct rival: the UNGATED architecture + the same W cut, proving the
  stall is the pre-existing W-gated slot copy, NOT the write_ctrl gate (D4's correction of D3's
  attribution; see AC93_PROTOCOL_v1.md).

This runner is derived from ac92.py. The `ungated` arm is byte-identical to AC92's `intact` arm
(the gate is a no-op when disabled); the only addition is the gate toggle and the `gated` arm.
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
MOVE_TICK = CORRUPT_TICK            # kept for the comparator (transition='none' here)

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

ARMS = ('gated', 'ungated', 'W_block', 'W_rescue', 'W_block_ungated')

# ---- the AC93-D3 interruption (land W depletion DURING an actual succession cycle) ----
# The succession is FORCED to start at FORCE_TICK (a deterministic damage pulse guarantees
# desc_minority_active >= DESC_TRIGGER; the rate limiter is open because last==0 until the first
# succession, so 2400 - 0 >= SUCC_MIN_SPACING). W production is cut from the SAME tick, so W
# depletes naturally to 0 ~50-63 ticks later -- mid-copy (the copy phase is ~150 ticks). W_rescue
# restores W at RESCUE_TICK (machinery-only, EXTERNAL); W_block never restores.
FORCE_TICK = 2400
RESCUE_TICK = 2490

# per-arm config. gate_ctrl=True makes write_ctrl MODE W-gated (the AC93 mechanism); False is the
# frozen AC88/AC92 distinct-resource model (the comparator). W_block/W_rescue force the succession
# at FORCE_TICK and cut bank-0 W production from the same tick (block_W), differing only in whether
# the machinery is restored (direct_restore at RESCUE_TICK).
ARM_PARTS = {
    'gated':   dict(ac_arm='regen', repair=True, regen=True, succession=True, ctrl_maintain=True,
                    gate_ctrl=True),
    'ungated': dict(ac_arm='regen', repair=True, regen=True, succession=True, ctrl_maintain=True,
                    gate_ctrl=False),
    'W_block': dict(ac_arm='regen', repair=True, regen=True, succession=True, ctrl_maintain=True,
                    gate_ctrl=True, force_succession=True, block_W=True,
                    block_tick=FORCE_TICK, restore_tick=None, direct_restore=False),
    'W_rescue': dict(ac_arm='regen', repair=True, regen=True, succession=True, ctrl_maintain=True,
                     gate_ctrl=True, force_succession=True, block_W=True,
                     block_tick=FORCE_TICK, restore_tick=RESCUE_TICK, direct_restore=True),
    'W_block_ungated': dict(ac_arm='regen', repair=True, regen=True, succession=True,
                            ctrl_maintain=True, gate_ctrl=False, force_succession=True,
                            block_W=True, block_tick=FORCE_TICK, restore_tick=None,
                            direct_restore=False),
}

SOURCES = ['ac93.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC93_PROTOCOL_v1.md']


# ---------------- description encode / decode ---------------- (unchanged from ac92/ac89)
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
    ORDER-PRESERVING (unchanged from ac89/ac91)."""
    perm = decode_perm(desc[PERM_OFFSET:PERM_OFFSET + PERM_BITS])
    if sorted(perm) != list(range(4)):
        return None
    masks = read_masks(desc)
    actions = read_actions(desc)
    words = desc[:PERM_OFFSET].reshape(NWORDS, WIDTH)
    bank = np.concatenate([prog.encode_rule(1, m, a) for m, a in zip(masks, actions)])
    return np.concatenate([words[:4].ravel(), bank, words[4]])


# ---------------- slot / pointer / controller reads ---------------- (unchanged)
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


# ---------------- paid write primitives ---------------- (write_ctrl gains the gate)
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


def write_ctrl(o, e, c, gate=True):
    """Write the controller state word toward `c` (paid). ATOMIC for the MODE field, budgeted for
    the timestamp.

    - MODE (bits 0-3: active + phase) is the coordinator's STATE TRANSITION. When `gate` is True
      (the AC93 architecture) it is W-gated: if the transition's replicas exceed the W repair
      catalyst's per-action capacity `_cap`, the whole transition is refused (atomic, Decision 2
      item 1). When False it is the frozen AC88/AC92 distinct-resource model (refused only on
      energy/material shortfall).
    - LAST (bits 4-17: start timestamp) is rate-limit BOOKKEEPING, not a state transition. It is
      ALWAYS budgeted by energy + material alone (the AC88 distinct-resource model), NEVER gated by
      8*W -- Decision 2 item 2 as amended by errata E2: the timestamp write is bounded by its value
      DELTA (~35-69 replicas at succession start), which the W cap (8*W=24) cannot fund, and a
      permanently-truncated timestamp disables the SUCC_MIN_SPACING rate limiter (E1). The rate
      limiter's integrity is load-bearing, so the timestamp keeps its distinct budget.

    Both fields are paid 1 energy + 1 material per replica into e['ctrl_writes']/e['spent_e']/
    e['spent_m']; conservation is untouched by construction (Decision 2 item 4)."""
    b = o.body
    # MODE (bits 0-3): atomic, all-or-nothing
    mode_sites = np.argwhere(b.traces[1, CTRL_OFFS[:4]] != c[:4, None])
    n_mode = len(mode_sites)
    if n_mode:
        if gate:
            if n_mode > _cap(b):
                return 0            # atomic: refuse the whole mode transition, never a partial mode
        else:
            if b.energy < n_mode or b.material < n_mode:
                return 0
        idx = mode_sites
        b.traces[1, CTRL_BASE + idx[:, 0], idx[:, 1]] = c[idx[:, 0]]
        b.energy -= n_mode; b.material -= n_mode
        e['spent_e'] += n_mode; e['spent_m'] += n_mode
        e['ctrl_writes'] = e.get('ctrl_writes', 0) + n_mode
    # LAST (bits 4-17): budgeted toward (rate-limit bookkeeping; energy+material alone, never W-gated)
    last_sites = np.argwhere(b.traces[1, CTRL_OFFS[4:]] != c[4:, None])
    n_last = min(len(last_sites), b.energy, b.material)
    if n_last:
        idx = last_sites[:n_last]
        b.traces[1, CTRL_BASE + 4 + idx[:, 0], idx[:, 1]] = c[4 + idx[:, 0]]
        b.energy -= n_last; b.material -= n_last
        e['spent_e'] += n_last; e['spent_m'] += n_last
        e['ctrl_writes'] = e.get('ctrl_writes', 0) + n_last
    return n_mode + n_last


# ---------------- in-place maintenance ---------------- (unchanged)
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


# ---------------- succession state machine ---------------- (gate threaded through)
class Succession:
    def __init__(self, mode, encoded):
        self.mode = mode
        self.encoded = encoded
        self.log = []
        self._n = 0
        self._entry = None


def advance(o, e, succ, now, succ_trigger, gate_ctrl=True):
    if succ.mode != 'real':
        return
    active, phase, last = ctrl_fields(o)
    if not active:
        if succ_trigger and now - last >= SUCC_MIN_SPACING:
            src = read_pointer(o)
            tgt = (src + 1) % SLOTS
            write_ctrl(o, e, encode_ctrl(1, PHASE_COPY, now), gate_ctrl)
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
            write_ctrl(o, e, encode_ctrl(1, PHASE_VERIFY, last), gate_ctrl)
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
            write_ctrl(o, e, encode_ctrl(1, PHASE_SWITCH, last), gate_ctrl)
        else:
            write_ctrl(o, e, encode_ctrl(1, PHASE_COPY, last), gate_ctrl)
    elif phase == PHASE_SWITCH:
        src_maj = read_slot(o, source)
        tgt_maj = read_slot(o, target)
        if not (bool(np.array_equal(tgt_maj, src_maj)) and build_program(tgt_maj) is not None):
            write_ctrl(o, e, encode_ctrl(1, PHASE_COPY, last), gate_ctrl)
        else:
            write_pointer(o, e, target)
            if read_pointer(o) == target:
                write_ctrl(o, e, encode_ctrl(1, PHASE_REMOVE, last), gate_ctrl)
                succ._entry['switch_tick'] = now
    elif phase == PHASE_REMOVE:
        old_source = (source - 1) % SLOTS
        write_toward_slot(o, e, old_source, np.zeros(SLOT_BITS, dtype=np.uint8), SUCC_BUDGET)
        if not o.body.traces[1, slot_offset(old_source):slot_offset(old_source) + SLOT_BITS].any():
            write_ctrl(o, e, encode_ctrl(0, PHASE_IDLE, last), gate_ctrl)
            succ._entry['remove_tick'] = now
            succ._entry['done'] = True
            succ.log.append(succ._entry)


# ---------------- the injected maintenance step ---------------- (gate threaded through)
def maintain(o, e, succ, reg_offs, cfg, now):
    obs2 = bool(ac9.observe(o) & 4)
    dm = desc_minority_active(o)
    pm = pointer_minority(o)
    cm = ctrl_minority(o)
    reg_trigger = obs2 or (cfg['repair'] and (dm >= DESC_TRIGGER or pm >= POINTER_TRIGGER))
    succ_trigger = dm >= DESC_TRIGGER
    gate_ctrl = cfg.get('gate_ctrl', True)
    if cfg['repair']:
        if reg_trigger:
            reg_description_active(o, e)
        if pm >= POINTER_TRIGGER:
            reg_pointer(o, e)
        if cfg['ctrl_maintain'] and cm >= CTRL_TRIGGER:
            reg_ctrl(o, e)
    if cfg['succession']:
        advance(o, e, succ, now, succ_trigger, gate_ctrl)
    if cfg['regen'] and reg_trigger:
        reg_from_active(o, e, reg_offs)


ACTION_LINE = "        action=prog.choose(b.traces,observe(o))"
BALANCE_LINE = "    ac4.balance(before,b,e)"


# ---------------- the AC93-D3 intervention: force a succession, then cut/restore W ----------------
def force_succession(o, encoded):
    """Induce a succession at the current tick (scheduled, deterministic, damage-model-consistent).
    Sets 2 replicas of the least-damaged correct-0 bit of the ACTIVE slot to 1, guaranteeing
    `desc_minority_active >= DESC_TRIGGER` (2). Same sticky-SET model as the ambient damage stream --
    the pulse differs only in being deterministic and scheduled rather than stochastic. Applied BEFORE
    the step, so maintain() reads dm >= 2 and fires the succession (the rate limiter must already be
    open at the tick -- it is at FORCE_TICK, where last==0). The description is repaired by the same
    tick's reg_description_active (which fires on the dm>=2 trigger), but that repair runs AFTER dm is
    read, so the succession still fires. No controller content is supplied: only the description's own
    replicas are flipped, and the succession then copies them as-is."""
    g = read_pointer(o)
    off = slot_offset(g)
    bits = o.body.traces[1, off:off + SLOT_BITS]
    ones = bits.sum(axis=-1)
    cand = [i for i in range(SLOT_BITS) if encoded[i] == 0 and int(ones[i]) <= 1]
    assert cand, "no correct-0 bit with <= 1 set replica to force a succession"
    i = min(cand, key=lambda i: int(ones[i]))
    zero_reps = [r for r in range(7) if bits[i, r] == 0]
    for r in zero_reps[:2]:
        o.body.traces[1, off + i, r] = 1


def make_birth(ns, cfg):
    """Gate bank-0 (W) births from cfg['block_tick'] until cfg['restore_tick'] (None = forever).
    Banks 1 and 2 (memory-region catalysts) are never touched. Content (traces[0]/traces[1]) is never
    written by the gate -- only the birth outcome differs, so no controller content is supplied or
    altered. Before block_tick (and after restore_tick) the gate passes through to the frozen birth.
    (Carried from ac92.py.)"""
    orig = ns['birth']
    block = cfg.get('block_W', False)
    block_tick = cfg.get('block_tick', 0)
    restore = cfg.get('restore_tick', None)

    def gated(b, bank, parent, e):
        if bank == 0 and block and ns['now'] >= block_tick and (restore is None or ns['now'] < restore):
            return False
        return orig(b, bank, parent, e)
    return gated


def restore_W(o):
    """MACHINERY-ONLY rescue, labeled EXTERNAL: re-seed the W catalyst population (the produced
    finite-lived machinery), leaving the description, program, pointer, coordinator state, memory,
    energy, material and fuel untouched. life[:4] is reset to the frozen acquisition endowment and
    pos[:4] to the interior (0,0), so W is available. Called once at RESCUE_TICK for the W_rescue arm
    only, BEFORE the step, so the conservation identities (ac4.balance) hold within the step.
    (Carried from ac92.py.)"""
    o.body.life[:4] = np.array([32, 48, 64, 0], dtype=np.int16)
    o.body.pos[:4] = 0


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
    exec(compile(src, 'ac93_step', 'exec'), ns, fns)
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


# ---------------- run ---------------- (unchanged world; adds the gate toggle + D3 interruption)
def mapping_at(base, t, transition, move_tick=MOVE_TICK):
    m = list(base)
    if transition == 'perm' and t >= move_tick:
        m[1] = 1 - base[1]
    return m


def copy_progress(o, source, target):
    """Replicas of the target slot matching the source slot's majority read (0..SLOT_BITS*7)."""
    src_maj = read_slot(o, source)
    off = slot_offset(target)
    return int((o.body.traces[1, off:off + SLOT_BITS] == src_maj[:, None]).sum())


def run(seed, history, arm, damage=True, corrupt=True, transition='none', ticks=TICKS,
        move_tick=MOVE_TICK, force_tick=FORCE_TICK, rescue_tick=RESCUE_TICK):
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
    cfg = dict(ARM_PARTS[arm])
    if cfg.get('block_W'):
        cfg['block_tick'] = force_tick
        cfg['restore_tick'] = rescue_tick if cfg.get('direct_restore') else None
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
    description_correct_at_death = None
    # ---- D3 interruption measurement ----
    forced_src = None
    forced_tgt = None
    succession_start_observed = None
    first_W_empty = None
    phase_at_W_empty = None
    pointer_at_W_empty = None
    copy_progress_at_W_empty = None
    W_min_seen = 99
    phase_at_rescue = None
    pointer_at_rescue = None
    copy_progress_at_rescue = None
    W_at_rescue = None
    phase_at_death = None
    pointer_at_death = None
    copy_progress_at_death = None
    stall_ticks = None
    phase_changes_during_stall = 0
    prev_phase_in_stall = None
    window_succ_writes = 0
    window_ctrl_writes = 0
    window_reg_writes = 0
    rescue_applied = 0
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
        # the D3 interventions (force a succession; restore W), both BEFORE the step so conservation
        # identities hold within the step.
        if t == force_tick and cfg.get('force_succession'):
            force_succession(o, encoded)
        if t == rescue_tick and cfg.get('direct_restore'):
            restore_W(o)
            rescue_applied = 1
        step.__globals__['now'] = t
        e = step(o, core, noise, directions, coin, tuple(mapping_at(base_map, t, transition, move_tick)),
                 [True, True], True)
        for k in total:
            total[k] += e.get(k, 0)
        # ---- after-step measurement ----
        W_now = int((o.body.life[:4] > 0).sum())
        W_min_seen = min(W_min_seen, W_now)
        active_now, phase_now, last_now = ctrl_fields(o)
        if cfg.get('force_succession') and succession_start_observed is None and active_now == 1:
            succession_start_observed = t
            forced_src = read_pointer(o)
            forced_tgt = (forced_src + 1) % SLOTS
        if first_W_empty is None and W_now == 0:
            first_W_empty = t
            phase_at_W_empty = phase_now
            pointer_at_W_empty = read_pointer(o)
            if forced_src is not None:
                copy_progress_at_W_empty = copy_progress(o, forced_src, forced_tgt)
        if first_W_empty is not None and t < rescue_tick:
            window_succ_writes += e.get('succ_writes', 0)
            window_ctrl_writes += e.get('ctrl_writes', 0)
            window_reg_writes += e.get('reg_writes', 0)
            if prev_phase_in_stall is None:
                prev_phase_in_stall = phase_now
            elif phase_now != prev_phase_in_stall:
                phase_changes_during_stall += 1
                prev_phase_in_stall = phase_now
        if t == rescue_tick - 1 and cfg.get('direct_restore'):
            phase_at_rescue = phase_now
            pointer_at_rescue = read_pointer(o)
            W_at_rescue = W_now
            if forced_src is not None:
                copy_progress_at_rescue = copy_progress(o, forced_src, forced_tgt)
        if first_dead is None and o.body.dead:
            first_dead = t
            phase_at_death = phase_now
            pointer_at_death = read_pointer(o)
            if forced_src is not None:
                copy_progress_at_death = copy_progress(o, forced_src, forced_tgt)
            stall_ticks = (t - first_W_empty) if first_W_empty is not None else None
            description_correct_at_death = int((read_slot(o, read_pointer(o)) == encoded).sum())
    inv = ac4.inventory(o.body)
    decoded = (o.body.traces[0, :prog.PROGRAM_BITS].sum(axis=-1) > 3).astype(np.uint8)
    static = np.ones(prog.PROGRAM_BITS, dtype=bool)
    static[list(reg_offs)] = False
    desc_bits = read_slot(o, read_pointer(o))
    desc_priority = decode_perm(desc_bits[PERM_OFFSET:PERM_OFFSET + PERM_BITS])
    active_end, phase_end, last_end = ctrl_fields(o)
    W_births_bank0 = int(total['W_birth'] - total['region0_births'] - total['region1_births'])
    forced_done = [s for s in succ.log if s.get('done') and s.get('start', -1) >= force_tick - 2]
    return dict(seed=seed, history=history, arm=arm, damage=damage, corrupt=corrupt,
                transition=transition, ticks=ticks, move_tick=move_tick,
                force_tick=force_tick, rescue_tick=rescue_tick, rescue_applied=rescue_applied,
                completed=total['active'] == ticks, first_dead=first_dead,
                succession_start_observed=succession_start_observed,
                first_W_empty=first_W_empty, W_min_seen=W_min_seen,
                phase_at_W_empty=phase_at_W_empty,
                pointer_at_W_empty=pointer_at_W_empty,
                copy_progress_at_W_empty=copy_progress_at_W_empty,
                phase_at_rescue=phase_at_rescue,
                pointer_at_rescue=pointer_at_rescue,
                copy_progress_at_rescue=copy_progress_at_rescue,
                W_at_rescue=W_at_rescue,
                phase_at_death=phase_at_death,
                pointer_at_death=pointer_at_death,
                copy_progress_at_death=copy_progress_at_death,
                stall_ticks=stall_ticks,
                phase_changes_during_stall=phase_changes_during_stall,
                window_succ_writes=window_succ_writes,
                window_ctrl_writes=window_ctrl_writes,
                window_reg_writes=window_reg_writes,
                succession_completed=int(len(forced_done) > 0),
                succession_completion_tick=(forced_done[0]['remove_tick'] if forced_done else None),
                successions=len([s for s in succ.log if s['done']]),
                succession_log=succ.log,
                pointer=read_pointer(o),
                ctrl=(dict(active=active_end, phase=phase_end, last=last_end)),
                ctrl_idle_end=int(active_end == 0 and phase_end == PHASE_IDLE),
                ctrl_minority_end=ctrl_minority(o),
                description_correct=int((desc_bits == encoded).sum()),
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


def equivalence_check():
    """Re-run the frozen AC92 `intact` arm and compare byte-identically (state_hash) to the frozen
    AC92 rows, with the AC93 runner's gate DISABLED (`ungated`). Proves the runner is a correct
    extension of ac92 and that the gate toggle is a no-op when disabled."""
    frozen = [json.loads(l) for l in Path('ac92_results_v1/rows.jsonl').read_text().splitlines()]
    seeds = [4300, 4301, 4302, 4303]
    n_checked = 0
    for seed in seeds:
        for history in (0, 1):
            for damage in (True, False):
                for corrupt in (True, False):
                    want = [r for r in frozen
                            if r['seed'] == seed and r['history'] == history and r['arm'] == 'intact'
                            and r['damage'] == damage and r['corrupt'] == corrupt
                            and r['transition'] == 'none']
                    if not want:
                        continue
                    got = run(seed, history, 'ungated', damage, corrupt, 'none')
                    assert got['state_hash'] == want[0]['state_hash'], \
                        f"ungated mismatch {seed}/{history}/{damage}/{corrupt}"
                    n_checked += 1
    return n_checked


def collect(root, seeds, transition='none'):
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
                 r['flipped_still_wrong'], r['successions'], r['ctrl_writes'],
                 r['succ_writes'], r['reg_writes'], r['W'], r['C'],
                 r['energy'], r['material'])
                for r in rows[-2 * len(conds):]]), default=str), flush=True)
    # equivalence: gated vs ungated state_hash per condition (the clean-control expectation)
    per_cond_equal = {}
    for (a, d, c) in conds:
        if a == 'ungated':
            continue
        g = [r for r in rows if r['arm'] == 'gated' and r['damage'] == d and r['corrupt'] == c
             and r['transition'] == transition]
        u = [r for r in rows if r['arm'] == 'ungated' and r['damage'] == d and r['corrupt'] == c
             and r['transition'] == transition]
        gm = {r['seed'] * 2 + r['history']: r['state_hash'] for r in g}
        um = {r['seed'] * 2 + r['history']: r['state_hash'] for r in u}
        per_cond_equal[(d, c)] = gm == um
    clean_control = all(per_cond_equal.values())
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, rows=rows, transition=transition,
             clean_control=clean_control, per_cond_equal={str(k): v for k, v in per_cond_equal.items()}),
        indent=2))
    print(json.dumps(dict(clean_control=clean_control, per_cond_equal={str(k): v for k, v in per_cond_equal.items()}),
                     indent=2, default=str))
    return rows, clean_control, per_cond_equal


def collect_d3(root, seeds):
    """D3 engineering: record the interruption-during-succession demonstration. The comparator arms
    (gated/ungated) sweep all four (damage x corrupt) conditions for the near-equivalence record; the
    interruption arms (W_block/W_rescue) run on damage=True, corrupt=False only -- the succession is
    the sole event (corruption would be a second, unrelated challenge at t=8192)."""
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    comparator_conds = [(a, d, c) for a in ('gated', 'ungated') for d in (True, False) for c in (True, False)]
    d3_conds = [(a, True, False) for a in ('W_block', 'W_rescue')]
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for (a, d, c) in comparator_conds + d3_conds:
                    r = run(seed, history, a, d, c, 'none')
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, history=history, d3=[(
                r['arm'], r['succession_start_observed'], r['first_W_empty'], r['phase_at_W_empty'],
                r['copy_progress_at_W_empty'], r['phase_at_rescue'], r['copy_progress_at_rescue'],
                r['phase_changes_during_stall'], r['succession_completed'],
                r['succession_completion_tick'], r['first_dead'], r['completed'])
                for r in rows[-len(comparator_conds + d3_conds):]]), default=str), flush=True)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, rows=rows, transition='none',
             FORCE_TICK=FORCE_TICK, RESCUE_TICK=RESCUE_TICK), indent=2, default=str))
    print(json.dumps(dict(rows=len(rows), dir=root), indent=2, default=str))
    return rows


def gates(rows):
    """Recompute the prespecified categorical gates from the saved rows (no simulation)."""
    def pick(arm, damage, corrupt):
        return [r for r in rows
                if r['arm'] == arm and r['damage'] == damage and r['corrupt'] == corrupt
                and r['transition'] == 'none']

    gated_dc = pick('gated', True, True)
    ungated_dc = pick('ungated', True, True)
    block = pick('W_block', True, False)
    rescue = pick('W_rescue', True, False)
    block_ung = pick('W_block_ungated', True, False)

    # G3 near-equivalence: per individual, gated and ungated agree on every OUTCOME on every
    # (damage, corrupt) condition. State-hash divergence (the W=2 SWITCH->REMOVE 1-2 tick delay)
    # is reported, not gated; the outcome fields must not diverge, and the succession count may
    # differ by at most 1.
    near_equiv = True
    for d in (True, False):
        for c in (True, False):
            g = {r['seed'] * 2 + r['history']: r for r in pick('gated', d, c)}
            u = {r['seed'] * 2 + r['history']: r for r in pick('ungated', d, c)}
            for k in g:
                if (g[k]['completed'] != u[k]['completed']
                        or g[k]['flipped_still_wrong'] != u[k]['flipped_still_wrong']
                        or g[k]['description_correct'] != u[k]['description_correct']
                        or abs(g[k]['successions'] - u[k]['successions']) > 1):
                    near_equiv = False

    no_damage = (pick('gated', False, True) + pick('gated', False, False)
                 + pick('ungated', False, True) + pick('ungated', False, False))

    return {
        # Link 1 (baseline mechanism): the W-gated architecture reconstructs the corrupted
        # program and survives -- the gate does not break reconstruction at W=3.
        'G1_gated_reconstructs': all(
            r['completed'] and r['flipped_still_wrong'] == 0 for r in gated_dc),
        # Comparator: the ungated (frozen AC88/AC92) architecture reconstructs and survives.
        # (Runner correctness is the pre-final equivalence_check: ungated == frozen AC92 intact
        # byte-for-byte, 32/32.)
        'G2_ungated_comparator_reconstructs': all(
            r['completed'] and r['flipped_still_wrong'] == 0 for r in ungated_dc),
        # The gate is inert at the healthy fixed point (near-equivalence, not byte-identity).
        'G3_gate_inert_at_healthy_fixed_point': near_equiv,
        # Link 2 (interruption stalls the succession -- the COPY -- while alive): every blocked
        # individual forces the succession, W empties mid-COPY, the slot copy and every
        # W-catalyzed write stop, the phase freezes (the copy precondition is never met), the
        # succession never completes, and the organism dies with the description intact.
        'G4_block_stalls_succession_while_alive': all(
            r['succession_start_observed'] == FORCE_TICK
            and r['first_W_empty'] is not None
            and r['phase_at_W_empty'] == PHASE_COPY
            and 0 < r['copy_progress_at_W_empty'] < SLOT_BITS * 7
            and r['window_succ_writes'] == 0
            and r['window_ctrl_writes'] == 0
            and r['phase_changes_during_stall'] == 0
            and r['succession_completed'] == 0
            and r['description_correct_at_death'] == DESC_BITS
            and not r['completed'] and r['W'] == 0 and r['C'] == 0
            for r in block),
        # The stall is the pre-existing W-gated slot copy, NOT the write_ctrl gate: the UNGATED
        # architecture under the same W cut freezes identically (phase frozen, ctrl writes zero).
        'G5_stall_is_the_copy_not_the_gate': all(
            r['succession_start_observed'] == FORCE_TICK
            and r['first_W_empty'] is not None
            and r['phase_at_W_empty'] == PHASE_COPY
            and r['window_succ_writes'] == 0
            and r['window_ctrl_writes'] == 0
            and r['phase_changes_during_stall'] == 0
            and r['succession_completed'] == 0
            and r['description_correct_at_death'] == DESC_BITS
            and not r['completed'] and r['W'] == 0 and r['C'] == 0
            for r in block_ung),
        # Link 3 (rescue resumes the succession): every rescued individual was stalled at COPY
        # with W == 0 before the machinery-only rescue, then the succession completes (bounded
        # after RESCUE_TICK) and the organism survives with W=3, C=2.
        'G6_rescue_resumes_succession': all(
            r['phase_at_rescue'] == PHASE_COPY
            and r['W_at_rescue'] == 0
            and r['window_succ_writes'] == 0
            and r['phase_changes_during_stall'] == 0
            and r['succession_completed'] == 1
            and r['succession_completion_tick'] is not None
            and RESCUE_TICK < r['succession_completion_tick'] < RESCUE_TICK + 80
            and r['completed'] and r['W'] == 3 and r['C'] == 2
            for r in rescue),
        # Controls clean: with no damage stream the gated/ungated arms complete with fw == 0
        # (no succession fires; the corruption, when present, is reconstructed by the machinery).
        'G7_no_damage_controls_complete': all(
            r['completed'] and r['flipped_still_wrong'] == 0 for r in no_damage),
        'G8_completeness_determinism': None,
    }


def preflight(protocol='AC93_PROTOCOL_v1.md'):
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


def collect_finals(root, seeds):
    """D4 finals: the comparator arms (gated/ungated) sweep all four (damage x corrupt)
    conditions for the near-equivalence record; the interruption arms (W_block/W_rescue/
    W_block_ungated) run on damage=True, corrupt=False only -- the succession is the sole event
    (corruption at t=8192 would be a second, unrelated challenge)."""
    preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    comparator_conds = [(a, d, c) for a in ('gated', 'ungated') for d in (True, False)
                        for c in (True, False)]
    intr_conds = [(a, True, False) for a in ('W_block', 'W_rescue', 'W_block_ungated')]
    conds = comparator_conds + intr_conds
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for (a, d, c) in conds:
                    r = run(seed, history, a, d, c, 'none')
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, history=history, intr=[(
                r['arm'], r['succession_start_observed'], r['first_W_empty'],
                r['phase_at_W_empty'], r['copy_progress_at_W_empty'],
                r['phase_changes_during_stall'], r['succession_completed'],
                r['succession_completion_tick'], r['first_dead'], r['completed'],
                r['window_succ_writes'], r['window_ctrl_writes'], r['W'], r['C'])
                for r in rows[-len(intr_conds):]]), default=str), flush=True)
    g = gates(rows)
    # determinism: one sampled exact rerun of the first row
    first = rows[0]
    rerun = run(first['seed'], first['history'], first['arm'], first['damage'], first['corrupt'],
                'none')
    g['G8_completeness_determinism'] = (
        len(rows) == len(seeds) * 2 * len(conds) and rerun['state_hash'] == first['state_hash'])
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows, transition='none',
             FORCE_TICK=FORCE_TICK, RESCUE_TICK=RESCUE_TICK, conds=[list(c) for c in conds]),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--engineering' in sys.argv:
        collect('ac93_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    if '--d3-engineering' in sys.argv:
        collect_d3('ac93_d3_engineering_v1', [0, 1, 2, 3, 4, 5, 6, 7]); return
    if '--equivalence' in sys.argv:
        n = equivalence_check()
        print(f"equivalence check: {n} rows byte-identical to frozen AC92 intact")
        return
    collect_finals('ac93_results_v1', [4400, 4401, 4402, 4403])


if __name__ == '__main__':
    main()
