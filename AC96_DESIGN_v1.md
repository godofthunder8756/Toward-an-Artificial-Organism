# AC96-D1 — design: the 6-bit relinquishment failure-streak in maintained state

Parent: AC96 goal. Design only — no code, no protocol, no freeze. The implementer (D2)
is the audience: storage offsets, the damage/repair path, the exact read/write change,
the test world, and the comparator definition. `ac95.py`, `ac94.py`, `ac12.py` and every
freeze stay untouched; the runner is a new file `ac96.py` (parent decision).

---

## 1. What is being internalized

`alloc.streak` is a per-key counter over the two channels `{0,1}` (2 keys × 3 bits,
`STREAK_N = 6`) of consecutive unproductive contacts. It drives `_drop`
(erase-on-relinquish: set the decision-register bit to 1 and erase the memory entry).
Today it is `self.streak = {0:0, 1:0}` on the `AllocErase` object (`ac95.py:855`,
inherited from `ac12.Alloc`), read and written in `AllocErase.outcome`
(`ac95.py:856-866`): on a productive contact it resets to 0; on an unproductive
contact it increments, and at `>= STREAK_N` it fires `_drop`, which also resets it to
0. It is the second class-C host-side operational-memory leak the AC95-D1 audit found
(`ac95_d1_probe.py` probe 2: hold `body.traces` fixed, toggle the host dict, the next
relinquishment write flips). `alloc.streak` is *inert in the AC95 finals only because
the finals run `transition='none'`* (no stale route, streak never reaches 6); the
relinquishment mechanism itself is live on every arm.

The AC95-D1 leak reproduction was re-run for this design and confirms the leak:

```
streak[0]=0: register_bit False->False, entry_life_max 58->58, dropped=[], state_changed=False
streak[0]=5: register_bit False->True,  entry_life_max 58->0,  dropped=[[0,0]], state_changed=True
```

Same maintained state, only the host dict differed, and the maintained relinquishment
write changed. That is the defect AC96 removes.

---

## 2. Storage: six zero-valued bits of the permanently-dead rule

### 2.1 The dead rule and its free bits

The frozen program's four bank rules include exactly one **permanently dead rule**: the
rule whose mask is `32` (`DEAD_MASK`), i.e. the one that requires observation bit 5,
which `ac9.observe` can never set (it sets bits 0,1,2,3,4,6,7,8 only). Its 14-bit word
is `0b01010001000001`: `enabled=1` (bit 0), `mask=32` (word bits 1-9), `action=5`
(word bits 10-13). The word-bit → field mapping is `word = enabled | (mask<<1) |
(action<<10)`, so mask bit *i* lives at word bit *i+1* and action bit *j* at word bit
*j+10*.

The AC12 decision register already occupies **mask bits 0-3** of this rule
(`ac12.register_offsets` → word offsets `base+1 .. base+4`, resolved once at
acquisition). Setting any of them cannot make the dead rule live, because the mask
still requires observation bit 5. That precedent is exactly what AC96 reuses.

The verification run (`_ac96_verify_bits.py`, seeds 0-3) decodes the dead rule and
enumerates its zero-valued word bits. Every seed yields the same pattern; the register
uses word bits `{1,2,3,4}` (mask bits 0-3) and the **remaining zero-valued word bits
are exactly six**:

| word-bit k | offset (base+k) | field             | value in frozen program |
|------------|-----------------|-------------------|-------------------------|
| 5          | base+5          | mask bit 4  (16)  | 0                       |
| 7          | base+7          | mask bit 6  (64)  | 0                       |
| 8          | base+8          | mask bit 7  (128) | 0                       |
| 9          | base+9          | mask bit 8  (256) | 0                       |
| 11         | base+11         | action bit 1      | 0                       |
| 13         | base+13         | action bit 3      | 0                       |

The skipped offsets are the **set** bits that must stay 1: `base+0` (enabled),
`base+6` (mask bit 5 = the 32 marker), `base+10` and `base+12` (action bits 0 and 2 of
`action=5=0b0101`).

### 2.2 Answer to the task's verification question

> "Verify there are ≥ 6 free **mask** bits without changing the frozen program or its
> economy; if not, name an alternative location and justify it."

There are **not** 6 free mask bits. The dead rule's 9 mask bits are: 4 occupied by the
register (bits 0-3), 1 the immovable 32-marker (bit 5), leaving **4** free mask bits
(bits 4, 6, 7, 8). The remaining 2 bits are taken from the dead rule's **action field**
(action bits 1 and 3, both zero-valued). The justification is the same dead-rule
argument applied to a different field: **the dead rule never fires, so its action is
never read** — `prog.choose` returns a rule's action only when `enabled and
observation & mask == mask`, and the dead rule's mask is unsatisfiable by construction.
Setting a streak bit in the action field therefore cannot change behaviour, exactly as
setting a mask bit cannot make the rule live. Both kinds of bit are (a) zero-valued in
the frozen program, so a zero streak leaves the acquired organism byte-identical; (b)
inside `traces[0,:126]`, so damaged by the program stream; (c) repaired by the paid
bank-0 repair (action 2); and (d) decision state, so excluded from reconstruction
(§3.3). No alternative location is needed and none is cleaner: there is no other dead
rule, and `traces[0,126:]` is outside the program damage stream (using it would
require widening the damage stream and changing the frozen economy).

### 2.3 Exact offsets

```python
def streak_offsets(o):
    base = 14 * ac12.dead_rule_index(o)          # resolved once, at acquisition
    return [base+5, base+7, base+8, base+9, base+11, base+13]
# key 0 counter bits 0,1,2  -> offsets [0],[1],[2] of the list  (mask4, mask6, mask7)
# key 1 counter bits 0,1,2  -> offsets [3],[4],[5] of the list  (mask8, act1, act3)
```

`base = 14 * ac12.dead_rule_index(o)` is the same base `ac12.register_offsets` uses;
the six offsets are resolved once at acquisition from the pristine program (the AC12
rule: resolve register offsets once, before any damage or the first write changes the
mask you would match on). Verified: all six are `< 126` for every legal dead-rule
index (max `base+13 = 14*8+13 = 125`), all distinct from the register's
`{base+1..base+4}` and from each other, all zero-valued in the frozen program.

---

## 3. Damage, repair, and the read/write change

### 3.1 Damage stream

The **program-bank damage stream** reaches the streak bits by construction: the step
applies `b.traces[0,:126] |= core_flips` (sticky SET, `ac71.DAMAGE_LINE_STICKY`), with
`core = (rng.random((126,7)) < .0001)` — 1e-4 per replica per tick. The six streak
offsets are inside `[0,126)`, so they are flipped exactly like the register and the
program bank. This is the "vulnerable" requirement: the streak is damaged by the
ambient stream, not a pristine backup.

### 3.2 Repair

The paid **bank-0 repair** (frozen action 2, `ac4.react`) majority-restores
`traces[0]` (all 1024 bits, capped at 32 writes/action, W-gated by
`8 * available_W`). It reaches the streak bits for free — no new observation bit, no
new repair primitive. Its semantics are the register's semantics: it cements the
current majority, so it holds the streak's *value* against sub-majority sticky damage;
a 4-of-7 flip on one bit is catastrophic corruption of that bit, exactly the register's
and program's limit (AC67/AC71). The streak bits also contribute to the corruption
observation (obs bit 2 = `min(ones, 7-ones).sum() >= 4` over the 126 bits), so streak
damage participates in the existing self-monitoring loop.

### 3.3 Exclusion from reconstruction (the one structural change)

`reg_from_active` rebuilds the program from the description and writes every
non-excluded bit toward the description value. It currently excludes only the four
register offsets (`exclude = set(reg_offs)`). If the streak offsets were not excluded,
every reconstruction would write them back to their description value (0 for the mask
bits, 0 for action bits 1 and 3) and destroy the counter. **The ac96 runner must
extend the exclusion to `set(reg_offs) | set(streak_offs)`**, by the identical logic
that already excludes the register: the streak is decision state, not program content,
so reconstruction must not clobber it. This is a consequence of "the streak lives in
maintained state", not a second, independent design change. It is applied only to the
maintained-streak arm; the host-streak control keeps the frozen exclusion
(§5).

### 3.4 The read/write change in `outcome`

`outcome()` (and `_drop`) read and write the maintained streak; the host dict becomes
vestigial and is never read.

**Read** (majority, `REGISTER_THRESHOLD = 4`):

```python
def streak_read(o, key):
    offs = streak_offsets(o)[3*key : 3*key+3]
    bits = [(o.body.traces[0, off].sum() >= 4) for off in offs]
    return bits[0] + 2*bits[1] + 4*bits[2]
```

**Increment** (unproductive contact): `new = streak_read(o,key) + 1` (reached only when
the read was `< STREAK_N`, else `_drop` would have fired). Write the bits that change
`cur -> new` atomically: compute all replicas whose value differs from the target,
refuse the whole increment if that count exceeds the paid capacity
`cap = min(32, 8*available_W, energy, material)`; otherwise set them, charge
`1 energy + 1 material` per replica into `e['spent_e']/e['spent_m']` and
`e['writes']` (or a dedicated `streak_writes` counter for reporting). Atomicity is
required because a partial binary-counter transition corrupts the value (e.g. `011 ->
100` written partially reads as a wrong count). Max transition is 3 bits = 21 replicas,
which fits the W=3 steady-state cap of 24; at W=2 the 21-replica transition is refused
whole — the streak cannot count through the `3 -> 4` step, i.e. the relinquishment
decision, like every other coordinator write, is a W-dependent service.

**Reset** (productive contact, and inside `_drop` after the drop): `new = 0`. Write the
set bits `1 -> 0`, atomic, same cap. A reset from 0 is a no-op (0 replicas), so in the
mature no-move phase (every contact productive, streak already 0) no streak write is
paid.

`_drop` keeps its existing register write (`sites[:] = 1`) and memory-entry erase
unchanged, and additionally performs the maintained streak reset. `_restore` keeps its
register write unchanged. **No host-side counter survives**; `alloc.streak` is not read
anywhere on the maintained arm.

---

## 4. The test world

**`transition='perm'`** — the AC75 permanent route move (key 1 relabelled at
`MOVE_TICK`), exactly the parent decision. It is the world where relinquishment
actually fires, and it was measured with the *current* host-streak architecture
(`_ac96_perm_probe.py`, `ac95.run(..., transition='perm')`, gated arm, damage on):

| seed | corrupt | completed | relinquishments | restorations | routes |
|------|---------|-----------|-----------------|--------------|--------|
| 0    | False   | True      | 1               | 1            | [0, 1] |
| 1    | False   | True      | 1               | 1            | [1, 1] |
| 2    | False   | True      | 1               | 1            | [0, 0] |
| 3    | False   | True      | 1               | 1            | [1, 0] |
| 4404 | False   | True      | 1               | 1            | [0, 1] |
| 4405 | False   | True      | 1               | 1            | [1, 1] |

(with `corrupt=True` the same seeds give the same 1/1 counts). The streak reaches
`STREAK_N = 6` with a bound entry, fires one drop, re-acquires, and restores — so the
world is correct and non-vacuous. For the streak's own record the drop count is not the
gate: the gate is that **relinquishment fires at all** (≥ 1 per individual), which it
does. Note the streak peak measured per world (`_ac96_streak_probe.py`): `'none'` world
peaks 1-4 during development (blind contacts) and never drops; `'perm'` world peaks 6
post-move and drops once.

---

## 5. The comparator

Internalizing the streak changes the digests, so the frozen AC92/AC94/AC95
byte-identity comparators no longer apply to the maintained arm (AC95-D2's note). The
new comparator is **host-streak control vs maintained-streak arm**, with the only
difference being where the streak lives, and the equivalence is established in three
layers.

**Arms.** `streak_maintained ∈ {False, True}` parametrizes the relocation.
`streak_maintained=False` is the host-streak control (host dict `alloc.streak`,
`outcome` reads/writes it, reconstruction excludes only the register offsets) and must
be the frozen ac95 gated behaviour byte-for-byte. `streak_maintained=True` is the
maintained arm (§2-§3).

**L1 — extension correctness.** The host-streak control reproduces the frozen ac95
`gated` rows with byte-identical `state_hash`, in the `'none'` world against
`ac95_results_v1` (the `equivalence_check` analog) and in the `'perm'` world against a
fresh `ac95.run(..., transition='perm')`. This proves the runner is a correct extension
and that the `streak_maintained` toggle is a no-op when False.

**L2 — decision identity.** The maintained arm makes the same decisions as the
host-streak control per individual: identical `dropped`/`restored` event lists (tick
for tick), identical final `routes`, `register`, `completed`/`first_dead`. The
maintained streak encodes the same count as the host dict at every tick, so the
decisions are identical. Under ambient damage the arms *may* diverge only where a
streak bit's majority flips (4-of-7) before repair — that is the intended vulnerability,
not a defect; report any such divergence, don't gate L2 against it in the damaged world.
The clean, gateable form of L2 is the **damage-free** run (`damage=False`), where the
maintained bits are exactly the written values and the arms are decision-identical.

**L3 — leak closure, single-step (the task's prescribed test).** With the organism's
maintained state held *identical* (including the maintained streak bits forced to
encode a count `c`), toggling the vestigial host dict `alloc.streak` produces
**identical writes** on the maintained arm — the host dict steers nothing. The same
toggle on the host-streak control *changes* the writes (the AC95-D1 probe 2 leak,
reproduced above). That asymmetry is the whole point: it is the closed-vs-leaky
contrast in one step. Sketch (§6) pins it.

**The state-hash / "pre-relinquishment trajectory" scope, stated honestly.** The two
arms are byte-identical (`state_hash`) on the shared trajectory up to the **first
streak write** — the first tick at which the streak becomes non-zero, which is a
development-time blind contact, *not* the first relinquishment (measured: the streak
peaks 1-4 during development in the `'none'` world, so "byte-identical up to first
relinquishment" would be false). On that prefix the maintained streak bits are still 0
(equal to the frozen/host bits) and no streak write has been paid. After it the arms
diverge **only** in (a) the streak bits' current values and (b) the paid streak-write
economy — never in a decision. A clean-control form of the same claim: with the streak
mechanism disabled (outcome forced not to fire, or `STREAK_N` made unreachable), the
maintained arm reproduces the host-streak control's `state_hash` exactly, proving the
storage relocation is the sole change. The paid streak-write cost is the intended
consequence of making the counter vulnerable paid state (AC95-D2) and is reported as
such, not as a divergence.

---

## 6. Single-step test sketch (hand to D3)

Mirror of `ac95_d1_probe.py` probe 2, run against the maintained architecture:

1. Acquire an organism, run a gated step long enough to bind key 0 (as the probe does),
   then set the maintained streak bits for key 0 to `c = STREAK_N - 1 = 5` (write all
   7 replicas of each of the 3 bits to the majority value of 5 = `0b101`).
2. Deep-copy the maintained state (`traces`, `memory.bits/life`, `life`, `pos`,
   `energy`, `material`).
3. For `host_streak in (0, 5)`: set the vestigial `alloc.streak[0] = host_streak`,
   call `outcome(o2, 0, e2)` with an unproductive event, and record the writes
   (register bit, memory entry, streak bits, `spent_e/spent_m/writes`).
4. **Assert** the two runs are identical (same writes, same state digest) — the host
   dict is not read. The host-streak control version of the same test **must** differ
   (register bit flips for `host_streak=5`), which is the reproduced leak.

Companion observer-discard test (AC95-D4 precedent): rebind `alloc` to a fresh
`AllocErase` (empty host dict) at a mid-run tick and assert the trajectory is
byte-identical (`state_hash`) on the maintained arm — the streak survives the discard
because it lives in the organism, not the observer.

---

## 7. Economy and reporting

The relocation adds paid writes only where the streak actually changes: increments on
unproductive contacts (1-3 bits, ≤ 21 replicas, atomic) and resets on productive
contacts and on `_drop` (0 when already 0). Measured per individual in the `'perm'`
world this is a handful of increments (9-12 unproductive events) plus no-op resets, so
the cost is small and bounded; in the mature no-move phase it is exactly zero. Report
`streak_writes` (or fold into `writes` plus a dedicated counter) and the final
`energy/material` shift as the intended cost of vulnerable paid state — never as a
"divergence" against a gate written for the free-host-dict economy (AC95-D2).

---

## 8. What this does not claim

This is the last class-C host leak on the operational control path; it completes the
AC95 state-sufficiency arc, not a new autopoiesis claim. The streak is decision state,
not program content — its maintenance is the register's maintenance (majority-restore
cements the value against sub-majority damage). No content self-production claim
(AC78/AC79 scope, unchanged), no claim that a damaged majority flip is recoverable
(4-of-7 on a streak bit is catastrophic, as everywhere).
