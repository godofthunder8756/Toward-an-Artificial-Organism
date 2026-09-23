# Closure-criterion consistency (K2) — the update/repair/produce trichotomy and its consequences

2026-09-22. Definitional deliverable. Resolves the K2 question: under the accepted
substrate convention, is the closure criterion (charter C1–C4) applied consistently, or does
it silently count state updates and repairs as production/replacement?

**Answer, stated plainly: it does not apply consistently.** The charter's own §7 note
("state that is damaged and maintained … is a component") promotes the working state of the
supplied succession/allocation machinery (generation pointer, coordinator word, decision
register/streak) to *components*, while §8's C2 clause requires a component to be "re-made
from other maintained state (succession, reconstruction, birth)" and explicitly excludes
repair and value-updates. The ledger then asserts C2 for those three items by citing exactly
the update/repair operations C2 excludes. That is assertion, not verification. The fix is
**not** to relax C2 (that would be redefining to pass); it is to correct §7's classification
so that "damaged-and-maintained state" is split into *components* (whose realization turns
over) and *maintained state* (whose value is updated and repaired in place). This is issued
as `DEFINITIONS_CHARTER_v2.md`, preserving v1 unchanged.

Everything below is traced to the frozen runner chain, not to a status summary.

---

## 1. The three operations, stated consistently (deliverable 1)

Three things are done to vulnerable state, and only one of them is "production". The
distinction is **functional**, not mechanical — a paid write is a paid write at the level of
`b.energy -= n; b.material -= n`; what differs is whether the write, as a whole process,
re-makes the component's realization from other maintained state.

**UPDATE — write a new value into storage whose realization is unchanged.**
The storage cells persist; only the value they hold changes. The component is not re-made,
re-derived, or re-located; nothing turns over. Code: `write_pointer`
(`ac95.py:355`), the MODE transition in `write_ctrl` (`ac95.py:369-408`, bits 0–3),
`reset_timer` (`ac95.py:428-446`), `increment_timer` (`ac95.py:449-473`),
`write_rip` (`ac95.py:314-327`), `write_toward_slot`'s per-replica writes
(`ac95.py:341-352`), the register writes in `_drop`/`_restore` (`ac95.py:887-909`,
`sites[:]=1` / `sites[:]=0`), and `gray_streak_write` (`ac99_d2.py:88-117`).

**REPAIR — restore damaged replicas to the current majority.**
Restores the component's *existing* value against damage. Explicitly not production
(charter C2). Code: `reg_description_active` (`ac95.py:536`), `reg_pointer` (`ac95.py:552`),
`reg_ctrl` (`ac95.py:566`), and the bank-0 action-2 majority-restore (`ac4.py:89-96`).

**PRODUCE / REPLACE — re-make the realization from other maintained state.**
The component *turns over*: a new finite-lived particle is born, a slot is copied to a fresh
physical location and the old cleared, or the full program is re-derived from the description.
Code: birth (W/C/B, `ac4.py:97-115`, `ac9.py:42-49`); succession copy→verify→switch→remove
(`ac95.py:607-725`); reconstruction `reg_from_active` (`ac95.py:580-594`).

The decisive test is **turnover**: did the realization leave and get replaced by a new one,
or did the same cells merely change value? Birth = turnover (a dead `life==0` site becomes a
live particle that will itself die). Succession = turnover (the active slot's content is
copied to a successor slot and the old slot is cleared). Reconstruction = turnover-by-derivation
(the program is re-derived from C4; C2's explicit "or is derived from a state that turns over").
Pointer, timer, streak, register = no turnover (the same cells change value in place).

---

## 2. C2 for pointer / timer / streak writes — verified, not asserted (deliverable 2)

Charter C2: "replacement requires that the component be re-made from other maintained state
(succession, reconstruction, birth)." Applied to the three items the task names:

| Item | Realized by | Operations in the ledger | Turnover? | Verdict under C2 |
| --- | --- | --- | --- | --- |
| **Pointer (C5)** | `traces[1, PTR_OFFS]` = `[520,521]`, 2 bits × 7 replicas | `write_pointer` (in `commit_switch`, `ac95.py:476-532`) + `reg_pointer` (`ac95.py:552`) | No — the same 2 cells change value to `target=(source+1)%SLOTS`; no copy, no clear, no re-derivation | **Fails C2.** Update + repair, not replacement |
| **Timer (part of C6)** | `traces[1, CTRL_OFFS[4:17]]`, 13 unary counter bits | `reset_timer` (clear 1→0) + `increment_timer` (set 0→1) + `reg_ctrl` | No — the counter cells increment/decrement in place | **Fails C2.** Update + repair |
| **Streak (part of C8)** | dead-rule free bits, `ac96.streak_offsets` (`ac96.py:60-65`), 3 bits × 2 keys | `gray_streak_write` (Gray increment/reset, `ac99_d2.py:88`) + `_drop`/`_restore` register writes + bank-0 repair | No — the counter/register cells change value in place | **Fails C2.** Update + repair |

None of the three is "re-made from other maintained state". A pointer write writes a value
*computed* from the current pointer (`(source+1)%SLOTS`), not a value *copied or derived from
maintained content*; a timer write writes a counter; a streak write writes a count. Contrast
the three genuine production edges in the same code: succession copies `read_slot(o, source)`
into a *different* slot and clears the old (`ac95.py:660-725`); reconstruction computes
`build_program(read_slot(...))` from C4 (`ac95.py:580-594`); birth sets a dead `life` site
live (`ac4.py:101-105`). The difference is turnover, and it is what C2's own text names.

**Conclusion:** C5, C6 (timer), and C8 (streak/register) are **maintained state**, not
produced components. The AC87→AC95 line established something real and important about them —
they are *internalized* (vulnerable, in the damage stream, paid-maintained, no host Python
field) — but internalization is not production. Charter v2 gives them their own clause
(S1–S4, "state integrity") instead of forcing them through C2.

The same applies to the other members of the v1 list that are not constituents/templates:
the **route memory (C7)** and the **coordination MODE/RIP bits (rest of C6)** are maintained
state too — deposit writes acquired content into pre-allocated `mem.Memory` cells (content
acquisition, not constraint production), and `write_ctrl`/`write_rip` write state-machine
transitions in place.

---

## 3. The production-dependency network (deliverable 3) — criterion derived, then applied

### 3.1 The criterion, derived from the adopted account

The constraint forbids an arbitrary "every node connects to every other" (clique) test. The
criterion is instead derived from Maturana & Varela 1980 clause (i) — components "through
their interactions and transformations continuously regenerate and realize the network of
processes that produced them" — operationalized via Montévil & Mossio's closure of
constraints (constraints produced and maintained by the processes they enable).

Form the production-dependency digraph on the component set: a directed edge **c → c′**
means "the process that produces c′ depends on (is enabled/constrained by) c". Then:

> **Closure criterion.** The set of necessary components is closed iff **every necessary
> component lies on a directed cycle** — its production is transitively enabled by itself.
> Equivalently, the graph has **no external root** (no component whose production is
> ultimately grounded only in substrate + free resources).

Justification. (i) "Regenerate the network that produced them" states that each component's
production is grounded in the network *including that component itself* — which for a finite
set is exactly "on a cycle". (ii) This is the transitive closure of C3: C3 already requires
a *direct* within-network dependency for each production edge; the cycle condition closes
the chain so no dependency chain terminates in substrate. C3 alone is insufficient — "each
component depends on another" permits a chain c1→c2→c3 where c3 depends only on substrate,
which is a world-produced component wearing a network costume. (iii) It is deliberately
**not** clique: requiring each node to depend directly on every other would be a physical-
completeness demand, not a closure demand. Where the stronger condition (a single
strongly-connected component — one unity, not two disconnected cycles) holds, it is reported
as satisfied, not required.

### 3.2 The level-(a) component set

Under the v2 split, the components whose production/replacement is at stake are the
constituents and the template/controller: **W, C, B (constituents), description (C4), and
the derived program (C9)**. (Route memory, decision state, pointer, coordinator state are
maintained state — §2.)

### 3.3 The edges, verified from code

- **W-birth** (action 6): requires a live W parent (`ac9.py:108-111`, `parents = np.flatnonzero(a[bank*4:bank*4+4])`; for bank 0 that is the W sites) **and** a program choice of action 6. Edges **W→W** (autocatalytic) and **C9→W**.
- **C-birth** (action 7): requires a live W parent (`ac4.py:100-103`, `a[:4]`) **and** program action 7. Edges **W→C**, **C9→C**.
- **B-birth** (action 8): requires live W as position anchor (`ac4.py:108`, `wp=b.pos[:16][a[:16]]`) **and** program action 8. Edges **W→B**, **C9→B**.
- **Description succession (C4→C4)**: copy source slot → successor slot, W-catalyzed (`_cap`'s `8·W` term, `ac95.py:336-338`), content from the description itself. Edges **W→C4**, **C4→C4** (self: the successor is re-made from C4's own content).
- **Program reconstruction (C9)**: `reg_from_active` builds `build_program(read_slot(...))` from C4, W-catalyzed (`ac95.py:580-594`). Edges **C4→C9**, **W→C9**.
- **Energy (C→all)**: C converts fuel→energy, 8 energy per C site per tick (`ac9.py:80-81`, `ac4.py:147-148`), and `balance` pins `energy == E + 8·converted − spent_e` (`ac4.py:124`). Every paid write and birth is charged energy (`b.energy -= n`, `pay(b,e,4,2)`). AC10 no-C: conversion confined to the inherited endowment, death 8/8 at 200–232. So **C → energy → every production process** is a load-bearing edge.
- **B retention (B→W, B→C)**: `ac4_transport.tr.move` zeroes the `life` of particles outside the enclosure; AC10 no-B exports constituents 8/8 and dies 8/8 (472–1153). So **B's retention preserves the W/C catalysts** — a load-bearing B→W and B→C edge in the frozen world.

### 3.4 The cycles

- **C4 → C9 → W → C4** (description → program → W catalyst → description). All three mutually closed.
- **C9 → C → (energy) → C9** (program chooses action 7; C's energy funds reconstruction) and **W → C → (energy) → W** (W parents C-birth; C's energy funds W-birth and all W-catalyzed writes). C closed.
- **W → B → W** (W births B; B's retention preserves W) and **W → B → C** (retention preserves C too). B closed.
- **W → W** (autocatalysis) is a self-edge; it does not by itself confer closure (it needs the program to choose action 6 — C9 — and energy from C), but combined with the other edges every necessary component sits on at least one cycle.

**Result.** The five level-(a) components {W, C, B, description, program} form a single
strongly-connected mutual-constraint network — not merely "each depends on another", but each
is transitively enabled by itself, with no external root inside the declared substrate
convention. This is the honest re-verified structure the criterion exposes; it is **not** a
verdict (the verdict is K3's), and it is conditional on the J1 substrate classification
(`advance()` and `prog.choose` supplied) exactly as v1 recorded.

---

## 4. Boundary production and boundary function (deliverable 4)

**Production participates.** B is a produced, finite-lived constituent: action 8 costs 2 M +
2 E, requires live W as position anchor (`ac4.py:108-115`), decays each tick (`B_expiry`,
`ac9.py:76`), and is re-born. It is genuinely produced, not a label (charter §3's claim,
re-confirmed).

**Function participates.** B's function is **retention** — `tr.move` exports particles that
leave the enclosure. AC10 (frozen, 72 rows): `no_B` exports constituents 8/8, loses both
routes within 195–279 ticks, and dies 8/8 at 472–1153; `no_B_retention` (retention forced by
the kernel flag while B matter goes to zero) is indistinguishable from `keep` (8/8, both
routes, zero export); `B_rescue` (external B supply) likewise retains 8/8. So retention is
load-bearing for the acquired organization *and* for long-term constituent persistence, and
B is the organism's produced means of realizing it.

**The one qualification that must not be hidden.** Retention is *substitutable* by substrate:
the kernel flag and externally supplied B matter each reproduce `keep` with zero internally
produced boundary. This does **not** remove B from the closure cycle — in the frozen world
B's retention is the mechanism and it feeds back into W/C persistence (B→W→C). But it
sharply bounds the sense in which the boundary "constitutes the system as a unity in space"
(M&V clause ii): B realizes a *functional* retention, and that retention is replaceable by a
world-supplied substitute. Clause (i) (production closure) is satisfied for B; clause (ii)
(spatial unity) is **J4, unresolved**, and is now stated with the substitution fact attached
rather than asserted either way.

---

## 5. Which evidence composes in AC105, which comes only from earlier versions (deliverable 5)

The reference is AC105 (`ac105.py`), which runs the ac95 gated arm (succession + D2 RIP +
D3 W-funded timer + D4 atomic switch) + `ac99_d2.GrayAllocEraseReserve(reserve=False)` +
`ac104.budget_rule` (allowance-42) in one organism, across 5 conditions × 2 arms × seeds
5800–5807.

**Composes in AC105 (measured in the single combined run):**
- Turnover — `W_births`/`C_births`/`B_births` per move window (`ac105.py:191,257-258,347-348`).
- Description integrity — `description_correct` (`ac105.py:315`).
- Reconstruction completeness — `fw_at_corrupt`/`flipped_still_wrong` (gate G2, `ac105.py:444-448`).
- Succession continuing — `successions` count (`ac105.py:329`).
- Decision no-harm — relinquishments (G4) and state sufficiency / observer-discard byte-identity (G5, `ac105.py:383-415`).

These are *presence, persistence and turnover* evidence in the combined architecture.

**Only from earlier versions (not re-tested by AC105 — it has no ablation arm and does not
gate on succession verification):**
- **Necessity by ablation** — AC10 (no-W/no-C/no-B: death 8/8), AC91 (block W-birth → W=0 → death 8/8), AC92 (W=0 interrupt mid-function). AC105 inherits these; nothing in AC105 cuts a constituent.
- **Replacement verification** — `verified_valid`/`target_correct`/cycles 6–7 with source-intact-at-switch, established in AC87/AC89. AC105 records only the *count* of completed successions (`ac105.py:329`), not the verify fields.
- **Machinery-dependence of the rate-limiter** — the W-funded timer freezes at W=0 (AC95-D3).
- **Streak internalization correctness** — maintained-state streak vs the vestigial host dict, and the Gray code's W-bound resolution (AC96 / AC99-D2 / AC100).
- **The schedule-change license** — the 40/40 `state_hash` equivalence that lets AC89 attribute its result to the schedule alone.

In short: the **closure (level-a) evidence** — production, turnover, and necessity of the
constituents/template/controller — is inherited from AC10–AC95; **AC105 contributes the
level-(b) decision operating range**, not new level-(a) production evidence. A closure
verdict that cites AC105 alone would be citing the wrong study for the production claims;
the correct composition is AC105 (operating range) *plus* the AC10–AC95 ablation/turnover/
verification record.

---

## 6. What changes and what does not

- **Changed:** the classification of C5 (pointer), C6 (coordination state), C7 (route
  memory), C8 (decision state) from *components* to *maintained state*; the addition of the
  state-integrity clause (S1–S4) and the derived cycle criterion; the code-accurate offsets
  for the pointer/CTRL layout.
- **Unchanged:** C1–C4's substance for genuine components (repair ≠ production; replacement
  = re-made from other state); the substrate convention (J1); the level definitions; the
  claim-level discipline. No evidence bar was relaxed — the reclassification *removes* four
  items from the "produced components" ledger rather than granting any item a pass.
- **Not resolved here (by design):** J1 (substrate vs coordinator — decisive, K3's to apply);
  J4 (retention vs spatial unity); J3 (content-supply boundary). The verdict is K3's.

The reclassification is dictated by the adopted account (M&V's "components" are the
constituents the network produces; M&M's "constraints" are material structures, and a
pointer/counter/register value is a *state variable of a process*, not a constraint), and by
v1's own §2 (level (b) = the streak/decision, level (c) = the route representation — neither
is a level-(a) component). It is a tightening of conceptual rigor, not a relaxation.
