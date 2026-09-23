# A1 — Physical realization ledger: pointer, coordination, route memory, decision state

2026-09-23. Derived accounting deliverable for the A1 card (t_293cdb2c). It answers one
question: *how are the four necessary operational-state items physically realized, and is
each realization covered by a produced component, an explicit substrate provision, or an
unaccounted dependency?*

It is a definitional/code-trace document. No study is re-run, no frozen row, hash, or
ledger is touched. Every offset and operation below is read from the frozen sources at
HEAD 77ace95 (`ac105.py`, `ac95.py`, `ac96.py`, `ac12.py`, `ac9.py`, `ac9_memory.py`,
`ac5_program.py`, `ac4.py`, `ac1.py`) and the storage geometry is re-derived at runtime
(`_a1_verify_offsets.py`, seeds 5800). Vocabulary is charter v2 (§7 components vs
maintained state vs §5 substrate) plus the dependency-audit correction.

---

## 0. The one fact the ledger stands on

Every item's **value** is a finite set of bits with 7 replicas each, held in a fixed
region of one of three arrays. All three arrays are **allocated at development** by the
simulator's `acquire()` scaffold and **never re-allocated, created, or destroyed during
life**:

| Storage medium | Allocation | Shape | Holds |
| --- | --- | --- | --- |
| `body.traces` (bank 0) | `ac4.acquire` → `np.zeros((4,1024,7))` | `[0, 0:126, :]` | program (C9) + decision state (C8) in the dead rule's free bits |
| `body.traces` (bank 1) | same array | `[1, 0:540, :]` | description slots (C4, 0:520) + pointer (C5, 520:522) + coordination (C6, 522:540) |
| `o.memory` (`mem.Memory`) | `ac9.acquire` → `Memory.empty()` | `(2,2,3,7)` bits + `(2,2,3,7)` life | route memory (C7) |

Verified at runtime: `traces.shape == (4,1024,7)`, `memory.bits.shape == (2,2,3,7)`,
`PTR_OFFS == [520,521]`, `CTRL_OFFS == 522..539` (18 bits, RIP at 539), description slots
span `[0, 520)` (4 × 130), register offsets `[99,100,101,102]` + streak offsets
`[103,105,106,107,109,111]` for seed 5800 (dead rule = word 5185, mask 32, action 5).

This is the *same* storage status the components C4 (description) and C9 (program) have:
their "turnover" (succession, reconstruction) is turnover of **values within fixed slots**,
never of the array. So "the storage does not turn over" cannot be a special indictment of
the four maintained-state items — it is equally true of every component. Demanding that
the arrays themselves be replaced is the over-reach the A1 constraints forbid.

---

## 1. Pointer (C5)

- **(i) Informational value.** 2 bits encoding `g ∈ {0,1,2,3}`, the generation pointer
  selecting which of the four description slots is authoritative (`ac95.read_pointer`,
  `PTR_OFFS`). It is the "which copy of the recipe is live" decision.
- **(ii) Storage medium / functional realization.** `body.traces[1, 520:522]`, 2 bits × 7
  replicas, majority-read (≥4). A fixed region of the bank-1 array, **adjacent to but
  outside** the four description slots (`[0,520)`). It is never a succession target —
  `advance()` copies only between slots 0–3.
- **(iii) Acquisition and state update.** Initialized to 0 at development (natural
  acquisition state). Updated only by the succession process's own transitions:
  `write_pointer` (single-field) or `commit_switch` (AC94-D2: pointer advance + MODE
  SWITCH→REMOVE as one atomic W-gated commit, `ac95.py:476-532`). Correctness-neutral:
  the value is derived from the current pointer (`source = read_pointer`, `target =
  (source+1) % SLOTS`), never supplied externally.
- **(iv) Damage repair.** `reg_pointer` (`ac95.py:552`), majority-restore of the 2 bits,
  fired when `pointer_minority >= POINTER_TRIGGER (2)`, paid 1 E + 1 M per replica through
  the W-gated `_cap`.
- **(v) Production / replacement / renewal.** None. The storage does not turn over; the
  value is updated and repaired in place.

**Classification: (b) substrate provision (storage) + maintained state (value).** The
storage is the development-allocated bank-1 array (substrate, §5's write/damage primitives
write into it). The value satisfies S1–S4 (in-world, damage-reachable, paid-maintained via
W, correctness-neutral). Not (a): the region is outside the description's succession
turnover. Not (c): the storage is supplied, and its maintenance is paid through produced W.

---

## 2. Coordination state (C6)

- **(i) Informational value.** 18 bits = MODE (bit 0 ACTIVE, bits 1–3 PHASE ∈
  {IDLE, COPY, VERIFY, SWITCH, REMOVE}) + the W-funded unary rate-limit timer (bits 4–16,
  13-bit counter 0..TIMER_MAX) + RIP (bit 17, reset-in-progress). The succession state
  machine's working state (`ac95.ctrl_fields`, `CTRL_BITS=18`).
- **(ii) Storage medium.** `body.traces[1, 522:540]`, 18 bits × 7 replicas. Same fixed
  bank-1 array as the pointer and the description.
- **(iii) Acquisition and state update.** Initialized 0. Updated by `write_ctrl` (MODE,
  atomic W-gated on the gated arm; distinct-resource on the ungated comparator),
  `reset_timer` / `increment_timer` (unary counter, W-funded, atomic — frozen at W=0), and
  `write_rip` (RIP bit). All driven by `advance()` — the supplied succession state machine
  (§5 substrate). Correctness-neutral: values are set by the succession process's own
  transitions, never externally.
- **(iv) Damage repair.** `reg_ctrl` (`ac95.py:566`), majority-restore, fired when
  `ctrl_minority >= CTRL_TRIGGER (2)`, paid W-gated.
- **(v) Production / replacement / renewal.** None. Updated in place.

**Classification: (b) substrate provision (storage) + maintained state (value).** The
mechanism that updates it (`advance()`) is §5 substrate under J1; the state it writes is
maintained. This is exactly the J1 split charter v2 sharpened: the coordinator's *state*
is maintained state, the coordinator's *mechanism* is substrate. The storage is the
supplied bank-1 array.

---

## 3. Route memory (C7)

- **(i) Informational value.** Acquired key/port entries — each entry 3 bits
  (valid, key, value), bound from productive contact outcomes. 2 regions × 2 slots, each
  entry with a 64-tick `life`. This is also the level-(c) representation (charter v1 §2:
  "acquired route memory … bound from productive contact outcomes").
- **(ii) Storage medium.** `o.memory` — a dedicated `mem.Memory` object
  (`ac9_memory.Memory`), bits `(2,2,3,7)` + life `(2,2,3,7)`, created empty at
  `ac9.acquire` (`Memory.empty()`). Not part of `traces`; a separate fixed array.
- **(iii) Acquisition and state update.** `deposit` binds an entry on a productive contact
  (21 paid writes; gated on `grow` + `activation` + a live W parent); `age` decrements
  life and expires (life→0 clears the bits); `renew` refreshes; `_drop` (erase-on-
  relinquish) clears an entry. Content is acquired from the organism's own outcomes.
- **(iv) Damage repair.** `renew` — majority-restore of the surviving majority (including
  key/validity), triggered by the aging signal / observation; paid.
- **(v) Production / replacement / renewal.** Content turns over (deposit → expire →
  re-deposit), but the **storage** (the Memory arrays) is fixed and never re-allocated.
  This is content acquisition + expiry, not "re-made from other maintained state" — which
  is why it is maintained state, not a component.

**Classification: (b) substrate provision (storage) + maintained state + content
acquisition (value).** The storage is a development-time empty array (substrate). The
value satisfies S1–S4 **and** the charter's "(+ content acquisition)" note — C7 is the one
item with a level-(c) content dimension in addition to the S1–S4 maintenance dimension.

---

## 4. Decision state (C8)

- **(i) Informational value.** Two sub-states (charter v2 §7b note): (a) a 4-bit
  allocation register (one bit per (region, slot), 1 = relinquished); (b) a 6-bit
  Gray-coded failure streak (3 bits per key, reflected Gray, 1-bit transitions). Together
  they drive erase-on-relinquishment (the level-(b) adaptive decision).
- **(ii) Storage medium.** Free bits of the permanently-dead rule in `body.traces[0]`
  (bank 0, the program bank). Register: mask bits 1–4 (`base+1..base+4`, `ac12.py:88-91`);
  streak: `base+5, base+7, base+8, base+9, base+11, base+13`
  (`ac96.py:60-65`); `base = 14 · dead_rule_index`. The dead rule (mask 32, action 5) can
  never fire because `ac9.observe` never sets observation bit 5, so its mask/action bits
  are free storage.
- **(iii) Acquisition and state update.** Initialized 0 (byte-identical to the frozen
  program — the AC12 inverted-semantics pattern). Updated by `_drop` / `_restore`
  (register) and `gray_streak_write` (streak) on the organism's own contact outcomes.
  Correctness-neutral.
- **(iv) Damage repair.** The paid bank-0 repair (action 2 majority-restore) repairs these
  bits exactly like every other bank-0 bit; they are **excluded from `reg_from_active`
  reconstruction** (`ac95.py:585-587`) so reconstruction does not clobber the decision
  state.
- **(v) Production / replacement / renewal.** None. Updated in place; explicitly excluded
  from reconstruction.

**Classification: (b) substrate provision (storage) + maintained state (value).** The
storage is the bank-0 array (substrate), physically *inside* the program component's bank
but **not covered by it**: reconstruction explicitly skips these offsets, so the program's
turnover does not carry the decision state. Not (a) for that reason; not (c) because the
storage is supplied and its writes are paid through W.

---

## 5. The ledger, complete

| Item | (i) value | (ii) medium | (iii) acquisition/update | (iv) repair | (v) turnover | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| C5 pointer | 2-bit active-slot selector | `traces[1,520:522]` | succession's own pointer write / atomic switch | `reg_pointer` (paid) | none | **(b) substrate + maintained state** |
| C6 coordination | MODE + W-funded timer + RIP (18b) | `traces[1,522:540]` | `advance()` (substrate) → `write_ctrl`/timer/RIP | `reg_ctrl` (paid) | none | **(b) substrate + maintained state** |
| C7 route memory | key/port entries | `mem.Memory` (fixed `(2,2,3,7)`×2) | deposit / expire / renew / drop | `renew` (paid) | content only (deposit↔expiry) | **(b) substrate + maintained state + content** |
| C8 decision | register (4b) + Gray streak (6b) | dead-rule free bits in `traces[0]` | `_drop`/`_restore`/`gray_streak_write` | bank-0 repair; excluded from reconstruction | none | **(b) substrate + maintained state** |

Every item is **(b) an explicit substrate provision** for its *storage medium* and
**maintained state (S1–S4)** for its *value*. **No item is (a)** — none of the four storage
regions is produced or replaced during life, and even where a region is physically adjacent
to (or inside) a component's array, the component's production process specifically
excludes or bypasses it (reconstruction skips the decision bits; succession copies only the
four description slots, never the pointer/ctrl region). **No item is (c)** — no storage
medium is a dependency that neither the organism nor the declared substrate provides: the
arrays are supplied by the simulator's `acquire()` scaffold, and the writes that maintain
them are paid through the produced W catalyst.

---

## 6. The one genuine finding, and its scoped consequence

The ledger is consistent, but it surfaces one gap of **explicitness**, not of production.

Charter §5 lists the substrate as *operations and constants* — `advance()`, tick clock,
decode format, write primitive, interpreter fallthrough, conservation laws, observation
function, damage model, world constants. It does **not** name the *storage media* those
laws act on: the `traces`/`life`/`boundary` arrays and the `mem.Memory` object, their
allocation at development, and their fixed geometry (bank 1 = 4×130-bit slots + 2-bit
pointer + 18-bit ctrl; bank 0 = 126-bit program with the dead rule's 10 free bits carrying
the decision state). The storage's provenance is currently carried only implicitly, by
§3 ("inside the organism … damageable finite state"), §4 ("developmental scaffolding:
inherited initial content is permitted"), and C4 ("initial content may be supplied").

This is **not** an unaccounted dependency in the strong sense: the storage is provided
(supplied substrate), and the constraint's own first clause — *do not require literal
replacement of Python arrays* — makes "the array is fixed" the correct boundary, not a
failure. And it is **not** a relabeling dodge: the ledger does not say "the pointer is just
maintained state, therefore its storage needs no account." It accounts for the storage
explicitly (substrate) and applies S1–S4 only to the value, whose maintenance is paid
through produced W.

**Scoped consequence for the closure claim:** the K3 verdict (production closure
SUPPORTED within the declared model and range) is **unaffected**. The four items' physical
realization is fully accounted for — substrate storage + internalized, paid-maintained
value — with no missing production edge. The residual is a **definitional amendment to
§5**: state explicitly that the body's finite array structure (the storage geometry,
allocated at development by the simulator's `acquire()`) is supplied substrate, the
physical medium the supplied write/damage/decode laws read and write. Whether that
"storage = substrate" reading is accepted, or whether the storage arrays should instead be
a named component with a production requirement, is a boundary decision — that is A2's
question ("resolve the boundary criterion"), and this ledger hands A2 the precise,
code-verified statement of what the storage is and why it is currently only implicit.

The constraint's second clause — *do not remove a necessary organizational dependency
merely by relabeling it "maintained state"* — is discharged as follows: the necessary
dependency is the storage medium; the ledger names it (substrate) rather than hiding it
behind the "maintained state" label, and the "maintained state" classification is applied
only to the value, which S1–S4 already tie to produced machinery (paid W-gated writes).

---

## Sources

`ac105.py` (offsets via `ac95.resolve_offsets` + `ac96.streak_offsets`), `ac95.py`
(`PTR_OFFS`/`CTRL_OFFS`/`RIP_OFFS`, `write_pointer`/`write_ctrl`/`reset_timer`/
`increment_timer`/`write_rip`/`commit_switch`, `reg_pointer`/`reg_ctrl`/`reg_from_active`,
`advance`/`maintain`, `resolve_offsets`), `ac96.py` (`streak_offsets`, `streak_read`/
`streak_write`, `AllocEraseMaintained`), `ac12.py` (`dead_rule_index`, `register_offsets`,
`Alloc._drop`/`_restore`, `bit_value`), `ac9.py` (`Organism`, `acquire` → `Memory.empty()`,
`observe` never sets bit 5), `ac9_memory.py` (`Memory`, `deposit`, `renew`, `age`),
`ac5_program.py` (`RULES=9`, `WIDTH=14`, `PROGRAM_BITS=126`, `choose`), `ac4.py`
(`acquire` → `np.zeros((4,1024,7))`, `Body`), `ac1.py` (`decode`), `DEFINITIONS_CHARTER_v2.md`
(§7b, §7c, §5), `DEPENDENCY_AUDIT_v2_CORRECTION.md`. Runtime verification:
`_a1_verify_offsets.py`.
