# ACI organism exit criteria v1 — when to stop investing in the current organism, and which questions are essential before neuralization

2026-09-25. Deliverable for the Q7 card (t_06ea9f9c): *when should we stop investing in
the current organism, and which unresolved organism questions are essential before
neuralization?* Category A/F — organizational exit decision.

This is a **decision/classification document**. It runs nothing, re-hashes nothing,
freezes nothing, and edits no frozen artifact (runner, protocol, results dir, hash, or
ledger). It is not hashed into any study's `pre_run_snapshot.json`. It classifies the
organism program's unresolved questions against a single decision criterion — *would
resolving this question change the neural architecture we would build?* — and issues the
exit decision.

Vocabulary and evidence are read from the predecessor deliverables: Q0
(`ACI_MISSION_AUDIT_v1.md`, the evidence map and its "more organism work?" column), Q2
(`ACI_ARCHITECTURAL_PRINCIPLES_v1.md`, P1–P7 promoted / D1–D8 demoted), Q3
(`ACI_NEURALIZATION_MAP_v1.md`, the function-not-realization translation), Q4
(`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md`, the minimum architecture), and the autonomy
verdict and successor spec (`A0_AUTONOMY_VERDICT_v1.md`, `S0_CONTINUATION_DECISION_v1.md`,
`S1_SPATIAL_SUCCESSOR_SPEC_v1.md`). Reading discipline as in every Q-series document: seeds
are the replication unit; survival is a bimodality-aware lower bound (AC68), never a
per-seed-family guarantee; "frozen" means hashed protocol + `mkdir(exist_ok=False)` +
audit + replay.

---

## 0. The decision, stated first

**Stop investing in the organism line for neural-architecture purposes now. Zero unresolved
organism questions are essential before neuralization.** The transferable content of the
program is already fully extracted: Q2 promoted P1–P7 and demoted D1–D8, Q3 translated each
principle into a computational function plus a neural mechanism, and Q4 specified the minimum
architecture those principles require. Nothing that remains unresolved in the organism would,
if resolved, change what that architecture builds.

**The one genuinely forward organism question — the clause-(ii) spatial informational-core
successor (S1, R1–R4 tested by T1–T5) — is classified PAPER-ONLY.** Resolving it would NOT
change the neural architecture. Its transferable core (retention vulnerability, no hidden
pristine backup) is already encoded in the neural architecture as P1/P2 and D1; its remaining
content is organism physics (spatial realization, transport, produced particle substrate) that
the neural map explicitly does not inherit. It is preserved for the artificial-life paper, not
pursued as neural-architecture input.

Every other unresolved organism question is likewise not load-bearing for the neural design:
they are split between DEFER (the reliability tier's re-open condition, which is a *neural*
mechanism question, not an organism one) and NO LONGER WORTH PURSUING (storage, already
suspended at the resolution floor; survival-level composition, the AC68 bimodality wall;
content self-production, already withdrawn as a prerequisite).

The organism has reached its information-theoretic endpoint as an instrument. It is not
"exhausted" in the sense that no experiment could ever be run — a causal dependency can always
be tested — it is exhausted in the only sense that matters for the decision: **no further
organism result would change the neural architecture we are about to build.** Continuing to run
organism experiments "merely because another causal dependency can be tested" is exactly the
failure mode the card forbids.

Neither autopoiesis nor consciousness is claimed anywhere in this document. This is an exit
decision, not a claim that the organism program achieved its own autopoiesis goal.

---

## 1. The decision criterion

The card fixes one criterion, and this document uses exactly that criterion and nothing else:
**would resolving the question change the neural architecture we would build?**

"The neural architecture we would build" is `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4): a
single recurrent network with three maintained discrete workspace slots (W, V, E), two
specialist readouts (S_pol, S_reg), one learned maintenance controller A whose own state lives
in the maintained loop, one paid refresh process π, and one slow consolidation store Θ_slow.
Its component-to-property mapping is fixed; every component is justified by which ACO property
(N1–N5) it serves and which intervention (I1–I5) tests it.

Two disciplines from Q3 make the criterion sharp, and both must be applied to every candidate
organism question:

1. **Function, not realization.** The organism's specific machinery — the 126-bit rule bank,
   the W/C/B particles, the conservation economy, the succession state machine — does not map
   to neural substrate. Only the *computational property* it instantiates maps. So an organism
   question whose only residue is "how a specific organism physics behaves" is, by this rule,
   not load-bearing for the neural design.
2. **The negative constraints are as load-bearing as the positives.** D1–D8 are part of the
   architecture specification. An organism question is "resolved for neural purposes" when its
   outcome is already fixed as a design constraint — including a *negative* one. A question
   that can only re-affirm an already-demoted principle (e.g. "is graded better?", "is more
   state better?", "does a monitor predict?") is already answered by D1/D2/D4 and needs no
   further organism work.

A question is **ESSENTIAL BEFORE NEURALIZATION** only if its answer would *add, remove, or
change* a component of the Q4 architecture or a principle/constraint in Q2/Q3. A question is
**USEFUL BUT PARALLEL** if its answer could refine, but not change, the architecture and can be
pursued without blocking it. **PAPER-ONLY** means the answer is genuine artificial-life science
with no neural-architecture consequence. **DEFER** means set aside with a named re-open
condition. **NO LONGER WORTH PURSUING** means the question is already answered (positively or
negatively) or suspended by its own recorded floor.

---

## 2. The classification of unresolved organism questions

The unresolved questions at HEAD (eb79ecb), classified under §1:

| Question | Status at HEAD | Would resolving it change the neural architecture? | Classification |
| --- | --- | --- | --- |
| S1 — clause-(ii) spatial informational-core realization (R1–R4, T1–T5) | Specified, design-only, AWAITING separate execution authorization | **No** — transferable core (R2/R3) already in P1/P2 + D1; the residue is spatial/physical realization the map does not inherit | **PAPER-ONLY** |
| Reliability/monitor tier (AC117 CONTROL-yes/PREDICTION-no) | Bounded at the harness level; re-openable only by bidirectional damage with an acquired 1-value (K9 gate) | **No** for the organism — the transferable lesson (D4, control-not-prediction) is already a constraint; the *re-open condition itself* is a neural-mechanism question, not an organism one | **DEFER** (organism-scale re-open parked; the neural analogue is N4, already a target in Q4) |
| Maintained storage vs memoryless rival (AC116) | Suspended at the resolution floor (p=0.0625), not closed not demonstrated | **No** — D2 ("more state is not better") already encodes the outcome; further storage runs are explicitly not licensed (S0) | **NO LONGER WORTH PURSUING** (organism-scale; suspended by its own floor) |
| Survival-level composition of the six functions (AC115 G4–G7) | Retained as failed; the AC68 W/C bimodality wall | **No** — the *fact* is ALife lineage-specific; the *lesson* (bimodality-aware gates, lower-bound survival) already carries as methodology | **PAPER-ONLY** (the fact); the lesson is already inherited |
| Content self-production (AC78) | Blocked (locked fixed point, N_eff≈1); removed as a prerequisite (roadmap §2) | **No** — D8 explicitly withdraws it as a requirement; the neural architecture assumes acquired content | **NO LONGER WORTH PURSUING** (as a prerequisite — withdrawn) |
| Graded/weighted generalization (AC113) | Resolved negative (no advantage over integer counter) | **No** — D1/P5 already encode it | **NO LONGER WORTH PURSUING** (resolved negative) |

**The headline: the ESSENTIAL BEFORE NEURALIZATION bucket is empty.** Nothing the organism
program still has open would add, remove, or change a component of the Q4 architecture or a
principle in Q2/Q3. This is the same conclusion Q0 reached in its audit ("More organism work?
NO across the board") — this document is the justification of that column, item by item,
against the architecture Q4 actually specifies.

The rest of this section gives each classification its one-paragraph justification. §3 then
evaluates the S1 successor — the one forward question — in full, per R and per T, because the
card explicitly demands it.

### 2.1 S1 — PAPER-ONLY (full evaluation in §3)

The only genuinely forward organism question. Its transferable core is already in the neural
architecture; its residue is physical realization. §3 works through R1–R4 and T1–T5 one at a
time and shows none of them, if resolved, changes the Q4 architecture.

### 2.2 Reliability tier — DEFER

The organism-scale reliability question is answered at the harness level: the monitor's
retained direction-knowledge is load-bearing for *control* (directional repair, e correct
32/32) and inert for *prediction* (a transient `ones>=4` reflex predicts wrongness perfectly
under sticky-SET damage). That outcome is already a neural design constraint: D4, "a
representation earns its keep by control, not prediction," and the demotion of the
"reliability *predictor*" reading. The named re-open condition — bidirectional damage
introducing a non-zero error rate where the damage count is *not* already the wrongness signal,
with an acquired value that can be 1 — is a property of a *different mechanism*, not a further
experiment on the frozen organism. The neural architecture makes that property testable as N4
(internal evaluability, the meta-d′ ≠ d′ dissociation signature), which is already a target in
Q4 and Q5. So the organism-scale tier is parked (K9 gate); its neural analogue is already in
the design. No organism work is required to reach it.

### 2.3 Storage — NO LONGER WORTH PURSUING (organism-scale)

AC116 measured the maintained integer counter against the strongest tuned memoryless rival and
returned weak dominance at the sign-flip resolution floor (p=0.0625, the n=8 floor). S0 records
this as "not a license for further storage-comparison runs." The neural consequence is already
fixed: D2 ("more maintained state is not better"), P1's boundary ("the cost buys correctness
only contextually"), and AC109's sharper form ("storage is inert where the current observation
is decisive"). Re-running the storage comparison at organism scale would only re-measure the
same floor; it would not change the architecture, because the architecture already assumes
discrete default codes and adds state only where a rival without it provably fails (D2).

### 2.4 Survival-level composition — PAPER-ONLY (the fact); the lesson is already inherited

AC115 composed the exchange boundary with the five-mechanism closure and held at the mechanism
level (G1–G3, G8 16/16) while the survival-bundled gates (G4–G7) failed on a minority of
finals. A0 corrected the classification without moving any gate: three seeds die, one leaks a
particle, zero failures are description-integrity failures. This is the AC68 W/C bimodality
re-entering through the long horizon — a *fact about this lineage's* stochastic stress, not a
gap that further organism runs would close (AC47/48/49/50 showed the structural limit is not a
tuning miss). The fact is ALife-paper material. The *lesson* — gate survival as a
bimodality-aware lower bound, use disjoint seed families, never fold survival into a mechanism
gate — already carries into the neural program as methodology (and the neural architecture is
explicitly graded on causal contrast, not survival, per D6/X4). Resolving "can the six
functions compose at survival level" would not change the architecture, because the
architecture does not gate on survival.

### 2.5 Content self-production — NO LONGER WORTH PURSUING (as a prerequisite)

AC78 showed the production signal is a locked, path-dependent fixed point (N_eff ≈ 1), and the
roadmap removed content self-production as a gate. D8 encodes the withdrawal: an ACO maintains
representations it has *acquired*; it does not have to have invented their content. The neural
architecture assumes acquired content (W's taxonomy is supplied, the belief is learned). The
question is not open for neural purposes.

### 2.6 Graded generalization — NO LONGER WORTH PURSUING (resolved negative)

AC113 ran the heterogeneous two-counter against the single counter and returned no demonstrated
advantage (R1 corrected the F1 "equivalence" label). D1 and P5 encode the outcome: gradedness
is not intrinsically better; a graded form earns its place only where it buys a distinct causal
capability. Nothing further to resolve.

---

## 3. The S1 successor evaluated against the criterion

The card requires the spatial informational-core successor (S1, R1–R4 tested by T1–T5) to be
evaluated per item: for each, *would resolving this question change the neural architecture we
would build?* The successor is specified in `S1_SPATIAL_SUCCESSOR_SPEC_v1.md` (architecture +
gates) and `S1_SPATIAL_CORE_PROTOCOL_v1.md` (proposed protocol, AWAITING authorization). It
realizes the informational core (program, description, pointer, coordination, route memory) as
a produced, finite-lived, position-bearing component class "I," read and written only through
produced position-mediated machinery.

The evaluation rule applied to each item is the same two-step: (a) is the item's *transferable
core* already in the neural architecture (Q2/Q3/Q4)? (b) is the item's *residue* organism
physics the map does not inherit? If (a) is yes and (b) is no, the item is PAPER-ONLY.

### 3.1 R1 — realization-by-production (informational substrate is a produced, finite-lived, position-bearing component class)

- **What it claims in the organism.** Each informational bit is instantiated in finite-lived
  material substrate the organism produces (I-particles, born by action 6, autocatalytic via a
  live W parent, decaying every tick), turning over like W/C/B rather than persisting in a
  declared array.
- **Would resolving it change the neural architecture? No.** The transferable core — *the
  substrate that holds a representation is itself produced and maintained, not scaffolding* —
  is already P2 ("maintenance is enacted and funded through the system's own vulnerable
  machinery"; the W catalyst is "produced, not scaffolding") and N5 (the maintainer is a target
  of the maintained loop; the maintenance controller A's own working state lives in the
  maintained loop). The neural architecture encodes this as "the maintenance machinery is
  itself plastic and maintained" (fast/slow weight pairs, plastic recurrent connectivity). The
  residue — particles with lattice positions, finite lifetimes, autocatalytic births, a
  material economy — is exactly the organism physics Q3's rule 1 says not to inherit. R1's
  *property* is already a neural requirement; R1's *encoding* (produced particles) is
  artificial-life science.

### 3.2 R2 — local access (reads and paid writes are position-mediated through produced machinery; no host dereference)

- **What it claims in the organism.** A read of a bit is performed by a live W catalyst
  co-located with the site; a site with no reader returns unreadable; there is no host
  dereference of the informational array.
- **Would resolving it change the neural architecture? No.** The transferable core is the
  *no-hidden-pristine-backup / no-host-oracle* constraint, which is already the Q4 architecture's
  standing rule: "the reference copy lives in the vulnerable, paid-maintained substrate — no
  hidden pristine weight matrix that the decay stream never reaches and no process refreshes."
  This is P1/P2's rival set (the "pristine backup" must fail) and the AC95-D4 observer-discard
  discipline. The residue — position-mediated access, co-located reader catalysts, "unreadable
  where the reader is absent" — is a *spatial* property with no neural analogue: a neural
  representation does not have lattice positions, and "no host dereference" is already enforced
  by construction in the neural design (there is no host array holding W/V/E). The property is
  inherited; the spatial mechanism is ALife.

### 3.3 R3 — retention vulnerability (informational substrate is in the transport and damage streams; a puncture degrades it; renewal is paid and W-gated)

- **What it claims in the organism.** The informational substrate decays and exports like the
  constituents; its retention is paid by the organism's own W-gated spending; a boundary
  puncture leaks it; there is no hidden pristine backup.
- **Would resolving it change the neural architecture? No.** The transferable core is N1
  (active persistence, no free permanence) plus P1 (representations cost to maintain) — the
  *definitional* property the whole neural architecture is built to realize, and already
  specified as the paid refresh process π under an energy budget, with the decay-time-course
  and pristine-backup rival as the N1 minimal test. The residue — transport streams, boundary
  punctures, W-gated write caps in material units — is the organism's economy, which the neural
  map replaces with a per-step compute/energy budget (Q3 P1: "the budget is the analogue of the
  paid write cap"). The property is the architecture's substrate property; the transport
  mechanism is ALife.

### 3.4 R4 — mutual constraint (informational substrate lies on the production-dependency cycle with W/C/B)

- **What it claims in the organism.** Production maintains I and I constrains production,
  through the local coupling, so I and W/C/B lie on the same strongly-connected
  production-dependency network (C5 extended).
- **Would resolving it change the neural architecture? No.** The transferable core is N5
  (closure onto the maintainer — the representation↔maintainer cycle R → M → R′) and P4/P7
  (allocation interaction and composition). These are already the load-bearing properties of
  the Q4 architecture: the N5 cycle V → A → π → V, the jointly-specified maintenance+cognition
  wiring, and the simultaneous-intervention composition test (P7). The residue — the specific
  production-dependency *network* over particle banks W/C/B/I — is the organism's material
  realization of C5, which the neural map replaces with the closure cycle over *cognitive*
  components. The property is the architecture's defining property (N5); the particle-network
  realization is ALife.

### 3.5 T1–T5 — the candidate tests

The five tests are the operationalization of R1–R4, and the same split applies. **Their
transferable content is the intervention *patterns*, which are already the neural architecture's
I1–I5:**

| S1 test | Pattern | Already in the neural architecture as |
| --- | --- | --- |
| T1 localized read ablation | ablate the reader, assert unreadability + endogenous restore | I2/I1 (scramble/cut exactly the link under test, not the representation) |
| T2 retention vulnerability | puncture the boundary, assert degradation + paid restore; transport-exempt contrast arm | N1's decay + pristine-backup rival; the "cut π, not R" test |
| T3 production dependency | block production mid-function, assert stall + EXTERNAL machinery-only rescue | I1 (cut π, not R) + the AC92 functional-interruption pattern Q4 inherits |
| T4 mutual-constraint directionality | two directed cuts with separable effects | I5 (change R, observe M reconfiguration, then R′), the AC108 both-direction pattern |
| T5 no hidden backup | observer-discard, byte-identical trajectory | the AC95-D4 observer-discard equivalence, the P1/P2 pristine-backup rival |

Each test's *residue* — the specific I-particles, the reader catalyst, the puncture gate, the
production-block flag — is organism physics. So resolving T1–T5 would confirm (or falsify) the
organism's *spatial realization* of properties the neural architecture already assumes and
already tests in its own substrate by I1–I5. It would not change what Q4 builds.

**Conclusion for S1.** Resolving the spatial informational-core successor would upgrade the
organism's autopoiesis verdict by one bounded step — clause (ii) for the informational core
from "declared" to "produced" — and nothing more. It would not add, remove, or change any
component, principle, or constraint of the neural architecture. The successor's R2/R3 core is
already in the architecture (P1/P2/D1, the no-hidden-backup rule); its R1/R4 core is already
the architecture's defining property (N5/P2); its T1–T5 patterns are already the architecture's
I1–I5. **PAPER-ONLY.** Do not authorize S1 as a neuralization prerequisite; preserve it for the
artificial-life paper, where completing the clause-(ii) claim is genuine science with its own
value.

---

## 4. The exit rule

The exit decision is a *rule*, not just a one-time verdict, so the program can apply it again
without re-litigating it:

1. **Invest in the organism line only while a result can change the neural architecture.**
   That was true through Q2/Q3/Q4; it is now false. The transferable content is extracted
   (P1–P7, D1–D8, the rival-set and gate-shape discipline, byte-identity, observer-discard).
2. **A causal dependency that can still be tested is not a reason to continue.** The card's
   exact prohibition. S1 is the canonical case: it is a real, finite, testable causal
   requirement, and it is PAPER-ONLY because resolving it does not touch the neural design.
3. **The organism line may be re-opened only by a specific trigger:** a *neural* result that
   creates a question the frozen organism model is uniquely positioned to answer and that the
   neural substrate cannot answer itself. No such trigger exists at HEAD, and none is expected:
   the neural program is substrate-independent by construction (Q3), so a question it cannot
   answer in its own substrate is unlikely to be answerable in the *more* constrained organism
   physics.
4. **The ALife paper proceeds independently and does not gate neuralization.** The paper-ready
   claims (production closure SUPPORTED bounded; adaptive autonomy ESTABLISHED; representational
   coupling SUPPORTED with the survival caveat — Q0 §0) are complete as they stand. The S1
   successor, if the ALife track ever authorizes it, would add one more bounded result to that
   paper and change nothing here.

The remaining organism work, if any, is owned by the artificial-life paper, not by the ACI
neural program. Nothing on the organism line is ESSENTIAL BEFORE NEURALIZATION or even USEFUL
BUT PARALLEL.

---

## 5. What stays behind for the artificial-life paper

Preserved, not pursued as neural input:

1. **The clause-(ii) spatial successor (S1, R1–R4/T1–T5).** The one open autopoiesis question —
   a finite, spec'd, falsifiable design — with its proposed protocol AWAITING authorization. It
   would upgrade clause (ii) for the informational core from "declared" to "produced," one
   bounded step, not full autopoiesis.
2. **The three paper-ready claims** (Q0 §0): production closure SUPPORTED bounded; adaptive
   autonomy ESTABLISHED (AC99–105); representational coupling SUPPORTED with the survival caveat
   (AC107/108).
3. **The lineage facts:** the AC68 W/C bimodality, the AC47/48/49/50 stable-vs-graded structural
   limit, the AC39 engineering-vs-finals transfer failure — as facts about *this* lineage, they
   belong to the paper; their *lessons* already carry forward as methodology.

---

## 6. Disposition and what this hands downstream

- **The exit decision is issued:** stop investing in the organism line for neural-architecture
  purposes. Zero unresolved organism questions are essential before neuralization.
- **Classification:** S1 → PAPER-ONLY; reliability tier → DEFER (neural analogue = N4);
  storage / content self-production / graded generalization → NO LONGER WORTH PURSUING;
  survival-level composition → PAPER-ONLY (fact) with its lesson already inherited.
- **The S1 successor is not authorized as a neuralization prerequisite.** It is a design-only
  spec awaiting *separate* execution authorization under the ALife track, if ever. The ACI
  neural program proceeds without it.
- **Unblocks Q8** (t_6fcfb2f0, the bridge experiment): Q8's predecessors now include this exit
  decision, so the bridge experiment is designed from the *extracted principles* (P1–P7/D1–D8,
  N1–N5, I1–I5) without any remaining dependency on further organism work. The bridge's rival
  set, metrics, and failure interpretation come from Q3/Q4, not from the organism's physics.

Neither autopoiesis nor consciousness is claimed. The organism program's transferable content is
fully extracted; its unresolved remainder is artificial-life science; and the neural
architecture proceeds on the principles, not on the organism.

---

## Sources

`ACI_MISSION_AUDIT_v1.md` (Q0; §0 the three paper-ready claims, §1.1 the "more organism work?"
column, §4 the Q7 handoff), `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2; P1–P7 §3, D1–D8 §4, rival
set §5), `ACI_NEURALIZATION_MAP_v1.md` (Q3; function-not-realization §1, P1–P7 map §3, D1–D8
negative constraints §4, necessary mechanism set §5), `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md`
(Q4; §4 shared substrate, §5 the eight components, §7 interventions, §8 the D1–D8 constraints),
`ACI_TARGET_CONSTRUCT_v1.md` (Q1; N1–N5 §3, I1–I5 §7), `A0_AUTONOMY_VERDICT_v1.md` (§0 verdict,
§3 supplied substrate, §5 R1–R4, §6 T1–T5), `S0_CONTINUATION_DECISION_v1.md` (decision (c), §3
the single strongest next step), `S1_SPATIAL_SUCCESSOR_SPEC_v1.md` (the successor architecture
and gate set), `S1_SPATIAL_CORE_PROTOCOL_v1.md` (proposed protocol, AWAITING authorization),
`CONSCIOUSNESS_ROADMAP_v1.md` (§13 the M1/M2/M3/M6/A0 status). Frozen results read, never
re-run or re-hashed: `ac114_results_v1/`, `ac115_results_v1/`, `ac116_results_v1/`,
`ac117_results_v1/` and the earlier frozen dirs. This document is derived and is not hashed
into any study's `pre_run_snapshot.json`.
