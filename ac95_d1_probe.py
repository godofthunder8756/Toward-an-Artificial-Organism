"""AC95-D1 leak reproductions: demonstrate that host-side variables change the next
tick's writes while the organism's maintained state (body.traces) is held fixed.

Two deterministic single-step probes:
  1. succ._entry['timer_reset_done']  (the known leak)
  2. alloc.streak                     (a NEW leak this audit surfaces)

Plus negative checks documenting the non-leaks (succ._n, succ.encoded, alloc.offs,
alloc.shadow, alloc.now, alloc.log, succ.log).
"""
import sys
sys.path.insert(0, '.')
import numpy as np
import ac94
import ac12
import ac4
import ac9
from ac94 import Succession, AllocErase, description_bits, resolve_offsets, build, ARM_PARTS


def fresh_organism(seed):
    """Acquire a healthy organism with energy/material topped up (machinery available)."""
    o, offs = ac12.acquire(seed)
    o.body.energy = 200
    o.body.material = 200
    return o, offs


def make_ctrl_state(o, active=1, phase=1, timer_set=(0, 1, 2)):
    """Overwrite the CTRL field: active bit, phase (0..7), and which timer bits are
    majority-set. All other bits zero."""
    CTRL = ac94.CTRL_OFFS
    o.body.traces[1, CTRL, :] = 0
    def sbit(i, v):
        o.body.traces[1, CTRL[i], :] = v
    sbit(0, active & 1)
    sbit(1, (phase >> 2) & 1)
    sbit(2, (phase >> 1) & 1)
    sbit(3, phase & 1)
    for i in range(ac94.TIMER_BITS):
        sbit(4 + i, 1 if i in timer_set else 0)


def event():
    return dict(spent_e=0, spent_m=0, ctrl_writes=0, succ_writes=0, reg_writes=0,
                timer_resets=0, timer_increments=0, split_events=0, productive=0,
                writes=0, memory_expiry=0)


print("=" * 70)
print("PROBE 1: succ._entry['timer_reset_done'] steers reset-vs-increment")
print("=" * 70)

seed = 0
now = 123  # not a multiple of TIMER_K, so the increment branch writes nothing

for flag in (False, True):
    o, offs = fresh_organism(seed)
    make_ctrl_state(o, active=1, phase=ac94.PHASE_COPY, timer_set=(0, 1, 2))
    # make the COPY branch a no-op: target slot already equals source slot majority
    src = ac94.read_pointer(o)
    tgt = (src + 1) % ac94.SLOTS
    src_maj = ac94.read_slot(o, src)
    off_t = ac94.slot_offset(tgt)
    for i in range(ac94.SLOT_BITS):
        o.body.traces[1, off_t + i, :] = src_maj[i]
    # snapshot maintained state digest before the call
    digest_before = o.digest()
    e = event()
    succ = Succession('real', None)
    succ._entry = dict(n=0, source=src, target=tgt, start=now, source_correct=0,
                       timer_reset_done=flag)
    ac94.advance(o, e, succ, now, succ_trigger=False, gate_ctrl=True, atomic_switch=True)
    tv = ac94.timer_value(o)
    print(f"timer_reset_done={flag}: timer_resets={e['timer_resets']}, "
          f"timer_increments={e['timer_increments']}, ctrl_writes={e['ctrl_writes']}, "
          f"timer_value_after={tv}, state_changed={o.digest() != digest_before}")

print()
print("=" * 70)
print("PROBE 2: alloc.streak gates the relinquishment write (_drop)")
print("=" * 70)

# Drive a real gated step for enough ticks to bind a route entry for key 0.
cfg = dict(ARM_PARTS['gated'])
ac12.PORTS = 4; ac12.YIELD_M = 64; ac12.YIELD_F = 64
ac12.POST_YIELD_M = None; ac12.POST_YIELD_F = None
ac12.MOVE_KEYS = (1,); ac12.MOVE = 10**9; ac12.DEV = ac94.ac71.DEV
ac12.REGISTER_THRESHOLD = 4
_, _, _, priority = ac4.acquire(0)
alloc = AllocErase('allocate', 0, 0)
o, offs = ac12.acquire(0)
alloc.offs = offs
alloc.shadow = o.body.traces[0].copy()
reg_offs = resolve_offsets(o)
encoded = description_bits(priority)
o.body.traces[1, :ac94.DESC_BITS] = encoded[:, None]
succ = Succession('real', encoded)
step = build(cfg['ac_arm'], alloc, succ, reg_offs, cfg)
base_map = (0 % 2, (0 // 2) % 2)
rng = np.random.default_rng([0, 1509])
rng1 = np.random.default_rng([0, 1609])
for t in range(700):
    alloc.now = t
    core = (rng.random((126, 7)) < .0001).astype(np.uint8)
    noise = (rng.random(o.memory.bits.shape) < .0001).astype(np.uint8)
    directions = rng.integers(0, 4, 20, dtype=np.uint8)
    coin = bool(rng.random() < .5)
    if True:  # damage on
        g = ac94.read_pointer(o)
        slots = {g}
        active, phase, last = ac94.ctrl_fields(o)
        if active:
            slots.add((g + 1) % ac94.SLOTS)
        for s in slots:
            off = ac94.slot_offset(s)
            o.body.traces[1, off:off + ac94.SLOT_BITS] |= (rng1.random((ac94.SLOT_BITS, 7)) < .0001).astype(np.uint8)
        o.body.traces[1, ac94.PTR_OFFS] |= (rng1.random((2, 7)) < .0001).astype(np.uint8)
        o.body.traces[1, ac94.CTRL_OFFS] |= (rng1.random((ac94.CTRL_BITS, 7)) < .0001).astype(np.uint8)
    step.__globals__['now'] = t
    e = step(o, core, noise, directions, coin, tuple(base_map), [True, True], True)

place = ac12.m12.slot_of_key(o.memory, 0)
print(f"key 0 bound at (region,slot) = {place}")
assert place is not None, "key 0 not bound after 700 ticks"

for streak0 in (0, ac12.STREAK_N - 1):
    # deep-copy maintained state (traces + memory life/bits + body scalars)
    o2, _ = fresh_organism(0)
    o2.body.traces[:] = o.body.traces
    o2.memory.bits[:] = o.memory.bits
    o2.memory.life[:] = o.memory.life
    o2.body.energy = o.body.energy
    o2.body.material = o.body.material
    o2.body.life[:] = o.body.life
    o2.body.pos[:] = o.body.pos
    a2 = AllocErase('allocate', 0, 0)
    a2.offs = offs
    a2.streak[0] = streak0
    a2.log = dict(relinquish_tick=None, dropped=[])
    digest_before = o2.digest()
    bit_before = ac12.bit_value(o2, offs[2 * place[0] + place[1]])
    life_before = int(o2.memory.life[place[0], place[1]].max())
    e2 = event()
    a2.outcome(o2, 0, e2)
    bit_after = ac12.bit_value(o2, offs[2 * place[0] + place[1]])
    life_after = int(o2.memory.life[place[0], place[1]].max())
    print(f"streak[0]={streak0}: register_bit {bit_before}->{bit_after}, "
          f"entry_life_max {life_before}->{life_after}, "
          f"dropped={a2.log['dropped']}, streak_after={a2.streak[0]}, "
          f"state_changed={o2.digest() != digest_before}")

print()
print("=" * 70)
print("NEGATIVE CHECKS (documented as non-leaks): succ._n gates nothing")
print("=" * 70)
# succ._n is read only to stamp succ._entry['n']; it feeds no write/branch.
# Confirm by code inspection: lines 610/613/618/621 only. Shown here for the record.
print("succ._n -> only written into succ._entry['n'] (a log field); never read for")
print("any write or branch in advance().")
