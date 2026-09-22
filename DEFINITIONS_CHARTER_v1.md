# Definitions and claims charter v1 — the frozen criterion and the modeled boundary

2026-09-22. This is a **definitional document**, not a scientific finding. It freezes the
definitions, claim levels, modeled system boundary, and the finite closure criterion that
the assessment track (A1 → A2 → A3) applies. It does **not** declare that the organism
passes anything. It is a derived document and is **not** hashed into any study's
`pre_run_snapshot.json`.

Authoritative sources it stands on, in order of load-bearing weight:

- `CLOSURE_BOUNDARY_v2.md` — the settled generic-substrate vs organism-specific boundary,
  including its explicit note that "fixed transition logic is a modeling choice, not a
  settled finding."
- `BASELINE_v1.md` + `EVIDENCE_INDEX_v1.md` — the reference architecture (AC105 body,
  commit `8f0218a`) and the accepted/negative capability ledger.
- `AC79_ERRATA_v1.md` — the production-vs-invention distinction (§3, §4) and the
  "autopoiesis is not a prerequisite for a theory-specific investigation" note (§5).
- `DEPENDENCY_AUDIT_v1.md` — the component/causal inventory and the statement of the
  one structural gap (read for its inventory; its §6 gap is pre-AC79 and superseded).
- Primary literature: Maturana & Varela 1980 (autopoiesis); Montévil & Mossio 2015
  (organizational closure); Di Paolo 2005 (adaptivity); Butlin et al. 2023
  (consciousness indicator framework, arXiv:2308.08708).

---

## 1. What this charter is for

The assessment track exists to answer one question honestly: *does the reference
architecture achieve organizational closure under a criterion that was fixed before the
assessment began?* A criterion that is redefined to fit whatever the implementation turns
out to do cannot answer that question. So this charter fixes, now, in advance:

1. the five claim levels and what evidence each requires (what each does **not** establish);
2. the modeled system boundary and what crosses it;
3. the finite list of components whose production/replacement is at stake;
4. the finite closure criterion A3 must apply unchanged;
5. the contested modeling judgments that the criterion cannot itself resolve.

The failure mode this exists to prevent is the project's own recorded one: a label
("autopoietic", "self-maintaining", "conscious") applied to a mechanism that the code does
not bear out, or a claim level silently standing in for a stronger one. Every downstream
card (A1's ledger, A2's gap experiments, A3's verdict, C1's task) reads its vocabulary
from here.

---

## 2. The five claim levels, separated

The project's three-level split (NEW_AGENT_GUIDE §2: functional motivation, organismal
autonomy, subjectivity) is retained; this charter subdivides it into the five levels the
assessment must keep apart. Levels are ordered by strength. **Satisfying a lower level
never licenses the wording of a higher level.** Each level states its evidence bar and the
strongest wording its evidence may earn.

### Level (a) — Autopoietic organization

**Adopted definition** (Maturana & Varela 1980, the canonical three-part formulation):

> An autopoietic machine is a machine organized (defined as a unity) as a network of
> processes of production (transformation and destruction) of components which: (i)
> through their interactions and transformations continuously regenerate and realize the
> network of processes (relations) that produced them; and (ii) constitute it as a
> concrete unity in space in which the components exist by specifying the topological
> domain of its realization as such a network.

Operationalized for this model via Montévil & Mossio's closure of constraints: the
constraints that hold the organization together (the components whose presence makes the
production processes operate) are themselves produced and maintained by those processes —
mutually maintained constraints, not a fixed external coordinator. The project's own
shorthand for this is the goal's §2 sentence: *a network of processes that regenerates
the components realizing the network.*

**Evidence bar:** the finite closure criterion in §8, evaluated component-by-component
against a ledger (A1). Necessary properties: the components realizing the network are
produced/replaced by processes the organism funds, each such process depending on other
components of the network (mutual constraint), the whole realized as a bounded unity.

**Strongest wording earned:** "partial organizational self-maintenance under these
interventions" / "meets the finite closure criterion within the declared model and
operating range" — and only if the criterion is actually met. Never "alive", never
"autopoietic" unqualified. **This level is currently UNESTABLISHED** (BASELINE_v1
unresolved items); the A3 verdict decides it.

### Level (b) — Adaptive autonomy

**Adopted definition** (Di Paolo 2005): *adaptivity* — the capacity of an autonomous
system to regulate its own conditions in relation to its own viability, i.e. to change its
internal states to sustain the processes that sustain it, not merely to react to a fixed
external norm. Self-production (level a) states what is produced; adaptivity states that
the system can *redirect* that production when its viability is threatened.

**Evidence bar:** a demonstrated, within-lifetime change in what the organism spends
resources on, caused by a change in its own viability conditions, and attributable to the
organism's own state (not to an externally supplied diagnosis or fixed schedule). The
frozen record here is the Gray-coded relinquishment streak + allowance-42 spending rule
(AC99/AC100/AC104/AC105) and the two-way relinquish/restore of routes (AC15/AC18/AC75).

**Strongest wording earned:** "acquired an instrumental priority for X" / "adaptive
relinquishment of an obsolete route under a self-maintained decision state". Never
"wants", "needs", "desires", "has a self".

### Level (c) — Cognitive representation and learning

**Adopted definition:** a *representation* is an internal state whose content is
determined by (is about) something the organism has encountered, and whose role in
behaviour is not hardwired to a single reflex but *flexibly consumed* by more than one
downstream process. *Learning* is the within-lifetime acquisition of such content.

**Evidence bar:** content acquired during the lifetime from the organism's own
observations/outcomes; stored in damageable state; read by a general mechanism that uses
it in at least two behaviourally distinct ways. The frozen record here is the acquired
route memory (`mem.Memory`, key/port entries bound from productive contact outcomes,
AC7/AC8/AC15/AC18) and the acquired priority permutation.

**Known limit (stated, not hidden):** the organism's observation space is nine
host-computed threshold bits about its own resources and integrity (fuel-low,
material-low, corruption, renewal-urgent, low-W/C/B). There is **no content-bearing
perceptual representation of an external world** in the reference architecture — the
"representation" available is interoceptive/route-level, not perceptual. Level (c) is
therefore only partially populated, and no level-(d) indicator that presupposes
perceptual content can be met by this architecture (see §7 and the contested judgments).

### Level (d) — Theory-specific consciousness indicators

**Adopted definition** (Butlin et al. 2023): consciousness is assessed, not by a single
test, but by *indicator properties* derived from the science of consciousness, each
formulated in computational terms, and satisfied *to a degree*. The indicator families:
RPT-1/2 (recurrent processing), GWT-1..4 (global workspace), HOT-1..4 (higher-order
theories), PP-1 (predictive coding), AST-1 (attention schema), plus AE-1/2 (agency,
embodiment). Satisfaction is **graded and evidential**: a positive indicator raises the
probability that the system is conscious (p(H|E) > p(H)); it does **not** establish it.

**Evidence bar:** a concrete, falsifiable mechanism stated in computational terms for this
organism, satisfying a *named* indicator, with the satisfaction graded. This is R3/C1's
remit, handed down from here.

**Strongest wording earned:** "meets candidate indicator X at degree Y". Never
"conscious", never "has subjective experience". The framework's own authors deny the
inference from indicator satisfaction to phenomenal consciousness, so the ceiling of a
positive level-(d) result is a bounded, theory-specific claim.

### Level (e) — Phenomenal consciousness

**Adopted definition:** *phenomenal consciousness* — there is something it is like to be
the system; subjective experience.

**Evidence bar:** none. There is no accepted decisive test for artificial systems
(NEW_AGENT_GUIDE §2). This level is **not assessable** by any current experiment in this
project, and no card in the assessment track may claim progress on it. It is listed here
only so that levels (a)–(d) are never mistaken for it.

**The level-(d)/(e) boundary is absolute:** "meets a candidate indicator" is a
theory-specific functional claim; "is conscious" is a subjectivity claim. Nothing in this
project may cross it.

---

## 3. The modeled system boundary

The model is the AC105 body inherited from AC99–AC104, on the AC85–AC89 internal-state
substrate. The boundary of the *modeled system* (what is inside the organism vs what is
the world) is:

**Inside (the organism):** the body constituents W/C/B, the boundary B, the 130-bit
description (five rule words + 8-bit permutation + four bank-rule masks + four bank-rule
actions) in interchangeable slots, the generation pointer, the coordination state
(MODE/LAST), the route memory (`mem.Memory`), the decision register (the relinquishment
streak), and the derived 126-bit program. All of these live in damageable, finite state,
are damaged by the damage stream, and are maintained/replaced by paid operations.

**Outside (the environment/world):** the tick clock; the resource reservoirs and their
conservation laws; the contact/port channel that yields fuel and material; the damage
stream (sticky `|=` at 1e-4 per replica per tick); and the world constants (PORTS, YIELD,
TICKS, DEV, thresholds, trigger constants).

**The boundary itself is a produced component, not a label.** The B (boundary) sites are
born by the organism's action 8, require live W, and their causal role is **retention**
(particles outside the boundary export; AC10: forced retention with zero enclosure matter
and external B supply both preserve routes 8/8, so the enclosure's role is retention, not
mass). Whether the boundary "constitutes the system as a unity in space" is assessed under
the criterion's existence/unity clause (§8), not assumed from the word "boundary".

---

## 4. Permitted environmental inputs and developmental scaffolding

**Permitted environmental inputs** (the organism's only income): fuel (+32) via contact
action 0 and material (+64) via contact action 1, both obtained only by the organism
choosing a contact action against a channel. There is no free external matter, no external
repair, no externally supplied correct state — any such thing is an **EXTERNAL control
arm**, labelled and never counted as autonomous.

**Developmental scaffolding (permitted, and the criterion's content boundary):**

- **Inherited initial content is permitted.** The priority permutation and the five rule
  words are installed at acquisition/development. The organism does not have to *invent*
  them (see §6). This is the Maturana & Varela position: autopoiesis concerns the
  production of the *components* realizing the organization, not the origin of the
  inherited instructions.
- **The scaffold that was removed is the reconstruction *recipe*** (`prog.program`), not
  the content. AC79→AC80 replaced the host-supplied `prog.program(priority)` with a generic
  decode that reads the stored description; the description's *content* was never required
  to be self-invented.
- **The scaffold that remains** is the supplied substrate (§5). The assessment's central
  contested judgment (§9) is whether that remainder is acceptable substrate or an
  undeclared coordinator.

---

## 5. Supplied substrate (format-level, fixed, not produced)

These are the laws of the world. They are supplied by the simulator and are **not**
produced, repaired, or replaced by the organism; nothing in the arc claims otherwise
(CLOSURE_BOUNDARY_v2 §Q1):

| Substrate operation | What it is |
| --- | --- |
| `advance()` transition logic | the succession state machine's fixed sequence copy → verify → switch → remove |
| tick clock | `now`, the host-supplied counter |
| decode format | the 14-bit word `enabled \| mask<<1 \| action<<10`, read by majority of 7 replicas |
| write primitive | paid write, 1 energy + 1 material per replica, at the frozen per-action cap |
| interpreter fallthrough | `prog.choose` returns action 9 when no rule's mask matches the observation |
| conservation laws | `ac4.balance` (material/energy/fuel identities and in-step asserts) |
| observation function | `ac9.observe` (the 9-bit observation the program bank reads) |
| damage model | sticky SET (`\|=`) at 1e-4 per replica per tick, independent streams per bank |
| world constants | PORTS, YIELD, TICKS, DEV, thresholds, trigger constants |

The defensible principle (CLOSURE_BOUNDARY_v2): demanding that the *mechanism* also
self-rewrite is an infinite regress — a mechanism that rewrote its own transition logic
would need a second-order transition logic, ad infinitum. Every formalization of
self-maintenance bottoms out in a fixed substrate; the question is only where the boundary
is drawn. Drawing it at the *format level* (the same level as the interpreter and the
conservation laws) is this project's stated choice.

---

## 6. The production-vs-invention distinction (the decisive one)

Two things are named by the single verb "produce", and the whole assessment turns on
keeping them apart:

1. **Producing / replacing a functional component** — producing or replacing the storage
   and machinery that *realizes* a function during the organism's life, using resources
   the organism itself acquires, through processes that depend on other components of the
   organization. Examples in the frozen record: birthing W/C/B; copying the recipe to a
   successor slot and switching the pointer (succession); reconstructing the 126-bit
   program from the stored description (generic decode); repairing the description and
   coordination state.

2. **Inventing informational content** — producing *new* content (a better priority, a
   novel rule) that was not inherited at development. This is **content
   self-production**, it is **blocked** (AC78: the production signal is a locked,
   path-dependent fixed point; no within-life signal ranks priorities), and it is **not
   required** for autopoiesis.

**Rule:** the closure criterion (§8) tests property (1) only. A claim of level (a) requires
that the components realizing the organization are produced/replaced (property 1); it does
**not** require, and must not be taken to require, that their *content* was invented by the
organism (property 2). Regenerating inherited organization and discovering better
organization are separate problems (AC79 errata §3). Confusing them is the single most
common way this project overclaims — both directions matter: "the organism replaced its
recipe storage" is property 1; "the organism wrote a better policy" is property 2, and
nothing in the frozen record establishes it.

---

## 7. The finite component list (what the criterion ranges over)

Closure is only ever assessed over a **finite, pre-fixed** component list. If a component
is not on this list, its status cannot silently decide the verdict. The list (the
organism-specific components; the supplied substrate in §5 is excluded by declaration):

| # | Component | Realized by | Produced/replaced by |
| --- | --- | --- | --- |
| C1 | W (repair/production catalysts) | `life[:16]` | action 6 (birth), requires a live W parent |
| C2 | C (energy converters) | `life[16:20]` | action 7 (birth), requires a live W parent |
| C3 | B (boundary) | `boundary[20]` | action 8 (birth), requires live W |
| C4 | Controller description (130-bit) | description slots in bank 1 | succession copy + pointer switch; description repair |
| C5 | Generation pointer (2-bit) | bank 1, offset 312–313 (AC86) | pointer write (paid, atomic) |
| C6 | Coordination state (MODE/LAST) | maintained ctrl word | coordinator transition write (`write_ctrl`, W-independent) |
| C7 | Route memory (acquired function) | `mem.Memory` | deposit path (binds key/port on productive contact) |
| C8 | Decision register (relinquishment streak) | dead-rule mask bits | `_drop`/`_restore` writes + bank-0 repair |
| C9 | Derived 126-bit program | decoded from C4 | reconstruction (`reg_from_active`, generic decode) |

Notes on the list:

- **C9 is derived, not stored.** Its production edge is the reconstruction process reading
  C4. It is listed so the assessment states explicitly that the program is replaced *via*
  the description, not produced from nothing.
- **Observation, decoding, reconstruction-comparison, timing, and allowance computation
  are not components** — they are either substrate operations (§5) or the *logic* of the
  succession/reconstruction processes. A1's ledger must classify each; this charter fixes
  the vocabulary: if it is fixed code that operates on vulnerable values, it is substrate
  or process logic, not a component. If it is state that is damaged and maintained, it is
  a component (and must be on this list).
- **The coordinator's *state* (C6) is a component; the coordinator's *mechanism*
  (`advance()`) is not on this list.** That split is exactly the contested judgment §9
  names.

---

## 8. The finite closure criterion (frozen; A3 applies it unchanged)

Let **C = {C1..C9}** (§7) be the organism-specific components. Let **S** be the supplied
substrate (§5). The organism **achieves organizational closure within the declared model
and operating range** iff **every** component c ∈ C satisfies all four clauses:

**(C1) Existence.** c is concrete, damageable, finite-quantity state inside the simulated
world (an array/ledger element that the damage stream can reach and the conservation laws
constrain) — not a Python field in host memory, and not an abstract label.

**(C2) Production/replacement.** There exists a process p(c), funded by resources the
organism acquires through its own actions (material/energy it collected via contact), that
produces or replaces c during ordinary operation — i.e. c *turns over* (birth or copy
events are observed, not merely persistence), or is derived from a state that turns over
(C9 from C4). "Repaired against damage" alone is **not** production: restoration of a
component's existing value does not replace the component. "Replacement" requires that the
component be re-made from other maintained state (succession, reconstruction, birth).

**(C3) Within-network dependence.** p(c) depends on at least one other component c′ ∈ C
(the mutual-constraint condition). If p(c) depends only on substrate and free resources,
c is produced by the world, not by the organization. (Frozen examples: W-birth requires a
live W parent; reconstruction requires the maintained description; succession requires the
maintained pointer.)

**(C4) Content boundary.** The initial *content* of a component may be supplied at
development (the priority permutation, the rule words). What C2 requires is that the
*component* — the storage/machinery realizing the function — is produced/replaced during
life. Supplying initial content does not defeat closure; failing to replace the component
does.

**Verdict mapping (the four A3 outcomes are defined by this criterion, not chosen to fit):**

- **Supported** — every c ∈ C meets C1–C4 (under the §9 substrate classification), with
  the composing evidence named per component. Bounded to the declared model and operating
  range; not a universal-survival or optimal-allocation claim.
- **Partially supported** — a named, non-empty proper subset of C meets C1–C4; the missing
  components and their missing clauses are named.
- **Falsified** — at least one component is *necessary* (its removal breaks the
  organization, established by ablation) and fails a clause, with no contested judgment
  (§9) that could reclassify it.
- **Unresolved** — a §9 modeling judgment is decisive: the verdict changes with how the
  judgment is resolved, and the charter does not pick a side.

**The criterion is finite and checkable** because C is finite (§7), each clause is a
mechanical question answerable against A1's ledger and the frozen runners (a component's
realization, its production edge, its dependencies, and whether its content was inherited
are all code-verifiable facts), and no clause permits introducing a new component, a new
process, or a re-drawn boundary after the assessment begins.

**Necessary vs optional (the closure/robustness split).** A component is *necessary* if
ablating it breaks the organization (the organism dies or the network's core function
ceases); *optional* if cutting it degrades but does not break the organization.
Closure is a claim about the **necessary** components: they must all be produced/replaced.
Optional replacement is a *capability/robustness* finding and is reported separately,
never folded into the closure claim. (Frozen example: recipe succession is the demonstrated
capability and the milestone target, while in-place repair alone also survives at this
horizon — the claim rests on replacement occurring and being verified, and the
necessary/optional line is drawn by ablation, not by prose.)

---

## 9. Contested modeling judgments (named, not resolved here)

The charter cannot settle these; it names them so that A3 can pick the "unresolved"
verdict when one is decisive, and so that no downstream card silently converts one into a
finding.

**J1 — the substrate/component boundary for the coordinator mechanism and interpreter.**
Is `advance()`'s transition logic (copy → verify → switch → remove) and `prog.choose`
(the interpreter) acceptable generic substrate (format-level machinery operating on
vulnerable values), or are they always-available *coordinators* that assume a functional
service without demonstrating its production? CLOSURE_BOUNDARY_v2 declares them substrate
"a modeling choice, not a settled finding," and the AC90 review explicitly **left the
boundary unresolved** — it did not affirm the substrate reading. Two resolutions, two
verdicts: if substrate, C1–C4 is assessed over C1–C9 as listed; if they are
organism-specific functions, they are components with no production edge and the criterion
fails on them. **This is the most likely source of an "unresolved" verdict.**

**J2 — "format-level" vs "host-supplied functional service."** Naming an operation
format-level does not by itself establish that it is generic machinery rather than a
supplied controller (the AC90 review's point). Whether the decode format and write
primitive are "laws" or "services" is a judgment, not a code fact. The charter records it;
it does not decide it.

**J3 — the content-supply boundary.** Whether installing the priority permutation and rule
words at development is "inherited instructions" (permitted, Maturana & Varela) or
"undeclared external content" is a judgment. The charter adopts the former (permitted, §6)
as its stated position; a reviewer may contest it, and that contest is itself a modeling
judgment, not a fact.

**J4 — the boundary-vs-substrate line generally.** Whether B (the produced boundary)
"constitutes the system as a unity in space" (the second clause of the Maturana & Varela
definition) or merely retains particles is assessed, not assumed; the answer bears on
whether the criterion's unity clause is met, and it is a judgment about what counts as a
unity, not a measurement.

**J5 — the observation layer.** The observation is nine host-computed threshold bits
(§5). Whether a system with a host-computed observation over its own state can *represent*
anything at all is a judgment that bears on level (c) and on every level-(d) indicator.
The charter's position: level (c) is only partially populated (interoceptive/route
content, no perceptual content), and no content-presupposing level-(d) indicator is
reachable. This is stated as the charter's adopted position, not as a settled finding.

---

## 10. Necessary properties vs additional research ambitions

**Necessary, under the adopted definition (what the closure claim requires):** C1–C4 over
the finite component list, i.e. production/replacement of the components realizing the
network, with mutual dependence, from self-acquired resources, initial content permitted.

**Additional research ambitions (explicitly NOT required by the definition, and NOT
claimed by the frozen record):**

- Content self-production / discovering a better policy (AC78 blocked) — not required.
- Strong organismal autonomy beyond the declared model (the interpreter and transition
  logic are supplied; whether that disqualifies is J1, unresolved).
- Optimal allocation or universal survival — not required; survival is a bimodality-aware
  lower bound.
- Phenomenal consciousness — not assessable, not required, never claimed.

A card that shows "replacement of the recipe-bearing storage" has satisfied a *necessary*
property of the closure claim; a card that shows "the organism invented a better priority"
would be pursuing an *ambition*, and none exists in the frozen record. The two must not be
reported in the same sentence as if they were one result.

---

## 11. Known limitations of any simulated-autopoiesis claim

Whatever A3 concludes, the claim is bounded as follows, and these bounds are part of the
charter, not a footnote:

- **Bounded to the declared model and operating range.** Seeds 5800–5807 (2 histories
  each, 80 matched arm-pairs); 16,384-tick horizon; the AC105 schedule/priorities/moves.
  Not universal, not a per-seed-family survival guarantee (AC39/AC68 bimodality).
- **Seeds are the replication unit**; N seeds × 2 histories = N independent units, not 2N.
- **Survival is a bimodality-aware lower bound**; engineering-seed statistics do not
  transfer to final seeds.
- **Oracle/scaffold controls** (protected copy, fixed-correct oracle, machinery-only
  re-seed rescues) are labelled EXTERNAL and never counted as autonomous.
- **The interpreter and transition logic are supplied** (§5); the criterion is assessed
  over C1–C9 under the J1 substrate classification, and a verdict of "supported" carries
  that classification with it.

---

## 12. Disposition

This charter is a derived, definitional document. It freezes the criterion A3 applies; it
does not run anything, re-hash anything, or declare a result. If the assessment finds the
criterion itself was mis-stated (e.g. the component list omitted a load-bearing state, or a
clause was ambiguous in a way that changed the verdict), the fix is a **new version of this
charter** (v2) with the change and its reason recorded — never a silent edit to v1 after
the assessment has used it. The closure criterion is defined here, before assessment, and
that is the point.
