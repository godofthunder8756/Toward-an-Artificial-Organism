# Definitions and claims charter v2 — the corrected closure criterion

2026-09-22. **Supersedes `DEFINITIONS_CHARTER_v1.md` on the closure criterion only (§7 and
§8 below, plus the change record §13).** v1 is preserved unchanged and remains authoritative
for §1–§6 (levels, boundary, permitted inputs, substrate, production-vs-invention) and
§9–§12 (contested judgments, necessary-vs-additional, limitations, disposition) except where
this document amends them. v2 is issued by K2 ("resolve closure-criterion consistency"), not
by any new experiment, and not to make the organism pass anything: it *removes* four items
from the "produced components" ledger and sharpens the production criterion. It is a
definitional document and is not hashed into any study's `pre_run_snapshot.json`.

## What changed, and why (read this first)

v1 contained one genuine inconsistency, in two clauses that cannot both be applied:

1. **§7's note** ("if it is state that is damaged and maintained, it is a component and must
   be on this list") put the generation pointer (C5), the coordination word (C6), the route
   memory (C7) and the decision register/streak (C8) on the component list — on the strength
   of being damaged-and-maintained alone.
2. **§8's C2** requires a component to be "re-made from other maintained state (succession,
   reconstruction, birth)" and states that "repair alone is not production" and that
   updating a value does not replace a component.

C5/C6/C7/C8 are damaged-and-maintained state whose only operations are **update** (write a
value into existing storage) and **repair** (majority-restore). Under C2 they fail; the
ledger (`DEPENDENCY_AUDIT_v2.md` §5) then asserted their C2 by citing exactly those
update/repair operations. That is the inconsistency: v1 simultaneously demands (C2) that
they be re-made from other state and lists (a §7 note) no such re-making process for them.

The fix is **not** to relax C2. It is to correct §7's classification. Being damaged and
maintained is a necessary condition for being *internalized*; it is not sufficient for being
a *component* (a constraint whose realization turns over). The adopted account dictates the
split: Maturana & Varela's "components" are the constituents the network produces;
Montévil & Mossio's "constraints" are material structures — and a pointer, counter, or
register *value* is a state variable of a process, not a constraint. v1's own §2 makes the
same point from inside: level (b) is the streak/decision (C8) and level (c) is the route
representation (C7); neither is a level-(a) component. Listing them in the level-(a)
component set was a cross-level error.

Consequence, stated plainly: the level-(a) closure component set is **{W, C, B, description,
derived program}**. C5/C6/C7/C8 move to a new **maintained-state** classification with their
own clause (S1–S4). This does not weaken the criterion for any genuine component; it stops
counting updates and repairs as production.

---

## 7. The finite component list (v2 — corrected)

Closure is assessed over a **finite, pre-fixed** set, split into **components** (whose
realization turns over) and **maintained state** (whose value is updated and repaired in
place). The supplied substrate (§5) is excluded from both by declaration.

### 7a. Components (level (a) — the production criterion C2 ranges over these)

| # | Component | Realized by | Produced/replaced by |
| --- | --- | --- | --- |
| C1 | W (repair/production catalysts) | `life[:16]` | action 6 (birth), requires a live W parent — autocatalytic |
| C2 | C (energy converters) | `life[16:20]` | action 7 (birth), requires a live W parent |
| C3 | B (boundary) | `boundary[20]` | action 8 (birth), requires live W as position anchor |
| C4 | Controller description (130-bit) | description slots in bank 1 | succession copy → verify → switch → remove; description repair |
| C9 | Derived 126-bit program | decoded from C4 | reconstruction (`reg_from_active`, generic decode) |

C9 is derived, not stored (its production edge is the reconstruction reading C4), exactly as
v1 stated.

### 7b. Maintained state (internalized, but NOT produced components — C2 does not apply)

| # | Item | Realized by | Its operations | Clause |
| --- | --- | --- | --- | --- |
| C5 | Generation pointer (2-bit) | `traces[1, 520:522]`, 7 replicas/bit | `write_pointer`/`commit_switch` (update); `reg_pointer` (repair) | S1–S4 |
| C6 | Coordination state (MODE + W-funded timer + RIP) | `traces[1, 522:540]`, 18 bits | `write_ctrl` (MODE update), `reset_timer`/`increment_timer` (counter update), `write_rip` (flag update); `reg_ctrl` (repair) | S1–S4 |
| C7 | Route memory (acquired function) | `mem.Memory` (regions × slots × bits × replicas + `life`) | deposit (content acquisition from own outcomes); renewal (refresh) | S1–S4 (+ content acquisition) |
| C8 | Decision memory (allocation register + Gray streak) | dead-rule free bits in `traces[0,:126]` | `_drop`/`_restore` (register update); `gray_streak_write` (counter update); bank-0 repair | S1–S4 |

Notes (correcting v1 where the code disagrees):

- **C5 offset** is `[520,521]` in the AC105 architecture (`ac95.PTR_OFFS`), not "312–313
  (AC86)" — v1 recorded the AC86 layout; the component identity is unchanged, the offset is
  implementation-specific.
- **C6 shape** is MODE (ACTIVE + PHASE, bits 0–3) + the W-funded unary rate-limiter timer
  (bits 4–16) + the RIP bit (bit 17), not "MODE/LAST" — the AC88 "LAST timestamp" was
  replaced by the W-funded counter (AC94-D3) and the reset-progress flag moved into
  maintained state (AC95-D2).
- **C8** is two decision sub-states (4-bit allocation register + 6-bit Gray streak), not one
  register; both are damaged-and-maintained and excluded from reconstruction.
- **Observation, decoding, reconstruction-comparison, timing (the tick clock), and allowance
  computation are not components and not maintained state** — they are substrate operations
  (§5) or process logic (fixed code over vulnerable values). The *rate-limiter timer* is
  maintained state (C6); the *tick clock* is substrate. The split is: fixed code over values
  → substrate/process logic; value that is damaged and updated/repaired in place → maintained
  state; realization that turns over (birth/copy/derivation) → component.

### 7c. The state-integrity clause (what maintained state must satisfy — replaces the C2 requirement v1 wrongly imposed on C5/C6/C7/C8)

A maintained-state item is *internalized* iff all four hold:

- **(S1) Realization in the world.** It lives in the simulated world's vulnerable storage
  (`traces[0]` or `traces[1]` / `mem.Memory`), not in host Python memory.
- **(S2) Damage reachability.** The damage stream reaches it (it is in a damaged bank).
- **(S3) Paid maintenance.** Its writes and its repair are paid (1 E + 1 M per replica),
  through the produced machinery's capacity (`_cap`, the `8·W` term) or the declared
  distinct-resource model (AC88's coordinator register); no host-side write.
- **(S4) Correctness-neutral.** Its *value* is set by the organism's own outcomes
  (streak/register from contact outcomes; pointer/MODE/timer/RIP from the succession
  process's own transitions), never by an externally supplied correct value.

This is the claim the AC87→AC95 (C5/C6) and AC96→AC99 (C8) lines actually establish. It is
**not** production: no turnover is required, none is claimed. State integrity is a
level-(b)/(c) property (adaptive/cognitive machinery internalized), not a level-(a) one.

---

## 8. The finite closure criterion (v2 — corrected; A3 applies this unchanged)

Let **C = {W, C, B, description, program}** be the components (§7a), **M = {pointer,
coordination, route memory, decision state}** the maintained state (§7b), and **S** the
supplied substrate (§5). The organism achieves **organizational closure within the declared
model and operating range** iff **every** component c ∈ C satisfies C1–C4 **and** the network
criterion C5, and every item in M satisfies S1–S4.

**(C1) Existence.** c is concrete, damageable, finite-quantity state in the simulated world
(an array/ledger element the damage stream reaches and the conservation laws constrain) —
not a Python field, not an abstract label.

**(C2) Production/replacement.** There is a process p(c), funded by resources the organism
acquires through its own actions, that produces or replaces c during ordinary operation —
c **turns over** (birth or copy events observed, not mere persistence), or is derived from a
state that turns over (C9 from C4). **Update (writing a new value into unchanged storage)
and repair (restoring damaged replicas to the majority) are NOT production.** Replacement
requires re-making from other maintained state: succession, reconstruction, birth.

**(C3) Within-network dependence.** p(c) depends on at least one other component c′ ∈ C
(or on c itself, autocatalytically). If p(c) depends only on substrate and free resources, c
is produced by the world, not the organization.

**(C4) Content boundary.** The initial content of a component may be supplied at development
(the priority permutation, the rule words). C2 requires the *component* — the storage/
machinery realizing the function — to be produced/replaced during life; supplying initial
content does not defeat closure.

**(C5) Network criterion (derived, replaces the implicit "each depends on another").**
Form the production-dependency digraph on C with edge c → c′ meaning "the process producing
c′ depends on c". Closure requires **every necessary component to lie on a directed cycle**
— its production is transitively enabled by itself. This is the transitive closure of C3: it
rules out external roots (a chain c1→c2→c3 whose terminus depends only on substrate). It is
**not** a clique requirement — no node is required to depend directly on every other. Where
the stronger condition holds (a single strongly-connected component — one unity, not two
disconnected cycles), it is reported, not required.

Derivation of C5: Maturana & Varela 1980 clause (i) — components "through their interactions
and transformations continuously regenerate and realize the network of processes that
produced them" — states that each component's production is grounded in the network including
itself, which for a finite set is exactly "on a cycle"; Montévil & Mossio's closure of
constraints is the same condition (a constraint set closed under the production relation has
no externally-produced member).

**Verdict mapping** (unchanged from v1, restated for completeness): **Supported** (every
c ∈ C meets C1–C5 and every m ∈ M meets S1–S4, under the §9 substrate classification, with
composing evidence named per component); **Partially supported** (a named non-empty proper
subset meets the clauses; the missing components/items and clauses are named);
**Falsified** (a necessary component, established necessary by ablation, fails a clause with
no contested judgment that reclassifies it); **Unresolved** (a §9 judgment is decisive).

**Necessary vs optional** (unchanged): closure is a claim about the **necessary** components
(cut them and the organization breaks). Optional replacement is a capability/robustness
finding, reported separately.

---

## 9. Contested modeling judgments (v1's list, amended where v2 sharpens them)

J1–J5 are unchanged in substance. v2 makes two of them sharper:

- **J1 (substrate/component boundary for the coordinator mechanism and interpreter)** is
  unchanged and decisive. v2's contribution: the coordinator's *state* (C6, and the pointer
  C5 it writes) is now classified as maintained state, not as a component — so J1 concerns
  only the *mechanism* (`advance()`'s copy→verify→switch→remove sequence and `prog.choose`),
  not the state. If that mechanism is substrate, C1–C5 range over C as listed; if it is an
  organism-specific function, it is a component with no production edge and the criterion
  fails on it.
- **J4 (boundary vs spatial unity)** is sharpened by the AC10 substitution fact: B is
  produced and on the closure cycle (retention preserves W/C), but retention is substitutable
  by substrate (kernel flag or external B matter both reproduce `keep` with zero internal
  boundary). So clause (i) (production closure) is met for B; clause (ii) (spatial unity) is
  unresolved, and the substitution fact is now part of the record, not a footnote.

---

## 10–12. Unchanged

The necessary-properties-vs-additional-ambitions section, the limitations of any
simulated-autopoiesis claim, and the disposition are carried over from v1 unchanged. In
particular: content self-production is blocked (AC78) and not required; survival is a
bimodality-aware lower bound; seeds are the replication unit; oracle/scaffold controls are
labelled EXTERNAL; the interpreter and transition logic are supplied.

---

## 13. Change record (v1 → v2)

| # | Change | Reason |
| --- | --- | --- |
| 1 | §7 split into components (7a) and maintained state (7b) | Correct the "damaged-and-maintained → component" over-classification (K2). |
| 2 | C5/C6/C7/C8 moved from components to maintained state | Their only operations are update/repair; under C2 they fail; counting them as produced was assertion, not verification. |
| 3 | New clause S1–S4 (state integrity) for maintained state | The correct claim for internalized state; distinct from production (no turnover). |
| 4 | New clause C5 (network criterion: every necessary component on a production cycle) | Replace the insufficient "each depends on another"; derived from M&V clause (i) + M&M closure; not clique. |
| 5 | Code-accurate offsets/layout for C5/C6 (PTR `[520,521]`, CTRL `[522,540]`, MODE+timer+RIP) | v1 recorded the AC86/AC88 layout; the AC105 architecture re-implements it. |
| 6 | C8 recorded as two sub-states (register + Gray streak) | Code holds two; v1 named one. |

None of these changes relaxes an evidence bar for any genuine component; none grants a pass
to C5/C6/C7/C8 (they now face a *stricter* requirement — internalization via S1–S4 — rather
than a production requirement they could not meet). The reclassification removes four items
from the produced-components ledger; it makes the criterion *narrower and stricter*, not
easier.
