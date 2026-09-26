# ACI target construct v1 — the intermediate object: an Artificial Conscious Organization (ACO)

2026-09-25. Deliverable for the Q1 card (t_a7e256b7): *what is the formal research
definition of the intermediate object we are trying to construct — NOT phenomenal
consciousness?*

This is a **definitional/theory document**. It runs nothing, re-hashes nothing, freezes
nothing, and edits no frozen artifact (runner, protocol, results dir, hash, ledger). It is
not hashed into any study's `pre_run_snapshot.json`. It defines one object — the target
construct — precisely enough that the downstream cards (Q2 architectural principles, Q4
minimal architecture, Q5 indicator matrix) can each read their vocabulary from here
instead of re-deriving it.

**Reading discipline applied throughout.** (1) The word "conscious" in the construct's name
is a *target designation*, not a claim: the construct is defined by functional/causal
properties, and satisfying them never licenses calling a system conscious. (2) The five
claim levels of `DEFINITIONS_CHARTER_v1.md` §2 are authoritative; this document places the
construct on that ladder and never crosses the level-(d)/(e) boundary. (3) The Q0 handoff is
binding: the construct **starts from level (c)** — internally maintained representations
causally coupled to their maintenance — and does **not** presuppose "metacognitive
monitoring" as an achieved tier. (4) The organism program's recorded negatives are part of
the specification: every property below is stated so that a rival that collapses to a
simpler control policy is detectable, not assumed away.

---

## 0. The one-paragraph answer

The intermediate object is an **Artificial Conscious Organization (ACO)**: a *recurrent
cognitive organization* realized in a single system, in which a set of **internally
maintained representations of the world and of the system itself** jointly satisfy five
causal properties — (N1) they persist **only through active, resource-consuming processes**
that keep them alive; (N2) their content is **flexibly consumed by at least two
specialized cognitive systems** that need different information and drive different
behaviour; (N3) at least one such consumption is **endogenous regulation** — the
representation changes how the system spends on its own upkeep, not just how it predicts
reward; (N4) some internal process can carry **evidence about the correctness or integrity
of another internal representation without receiving its ground-truth answer**, and is
**dissociable** from it; and (N5) the representations **affect the maintenance and future
organization of the very processes that maintain them** — a directed cycle from
representation to maintainer back to representation.

The ACO is the **first target of the ACI program** (the broader objective: neural-architecture
building blocks for consciousness-relevant computation). It is not a theory of consciousness,
not an operational definition of phenomenal experience, and not a claim that any existing
organism in this repository realizes it. It is a **specification**: the smallest coherent
organization a neural architecture must realize before a *theory-specific* question about
consciousness-relevant computation can even be asked about it. The four building-block themes
the program names (recurrent integration, self/world modeling, self-evaluation, endogenous
regulation) are the construct's content; the five properties N1–N5 are its form.

---

## 1. The name, and why the word "conscious" is kept

**Name:** Artificial Conscious Organization (ACO). "Organization" is the load-bearing noun:
the target is a *configuration of cognitive processes and their causal relations*, not an
"intelligence," a "mind," or an "agent," and not a substrate.

"Conscious" is kept for exactly one reason: the theory families surveyed in §10 associate
specific *organizations of cognitive processing* with consciousness-relevant computation, and
the ACO is the organization those families would each need to locate before their own
indicator could be tested. The name marks the object's *position* in the research program
(the object those theories are about), not a property the object provably has. Two rules
follow and are load-bearing:

1. **Satisfying the ACO definition is never evidence of consciousness.** The strongest wording
   a realized ACO earns is "meets the ACO definition (N1–N5, at the stated degree)." Any
   stronger claim — "conscious," "has subjective experience" — crosses the level-(d)/(e)
   boundary (`DEFINITIONS_CHARTER_v1.md` §2) and is forbidden.
2. **The ACO is not defined in terms of any one theory.** It is defined by the five causal
   properties; the theories enter only in §10, where they are compared and *not* adopted. A
   construct defined by a theory would be unfalsifiable by that theory; a construct defined by
   causal properties is testable against all of them.

**Level placement.** On the charter's ladder (§2): the ACO **contains** level (c) (cognitive
representation, flexibly consumed) as its substrate, **adds** level (b) (adaptive autonomy)
as one of its properties (N3), and **reaches toward but does not claim** level (d)
(theory-specific indicators). It sits on the (c)→(d) interface. Its necessary properties are
satisfiable from the program's *established* tier — maintained representations causally
coupled to their maintenance (AC107/108, AC99–105) — and it deliberately does **not** require
HOT-2 metacognitive monitoring, a graded posterior, or any self-produced content as
preconditions (§6).

---

## 2. Definitions used

These are fixed so that every property in §3–§5 reads unambiguously. They reuse the charter's
vocabulary where it exists.

- **System.** A bounded computational entity with (i) a state, (ii) a set of processes that
  transform its state over time, (iii) at least one input stream from an environment, and
  (iv) at least one output that affects the environment or its own future inputs. "Bounded"
  is functional (there is an inside/outside for the purposes of attribution), not spatial.
- **Representation R.** An internal state variable whose *content* is determined by something
  the system has encountered (a world cause or one of its own internal conditions), and whose
  *role* in behaviour is set by its content — not hardwired one-to-one to a single reflex
  (`DEFINITIONS_CHARTER_v1.md` level c). A representation can be interoceptive or
  self-referential; the charter's contested judgment J5 (can a host-observed system represent
  anything at all) is a *position*, not settled, and is recorded, not assumed.
- **Maintenance process π(R).** An internal, resource-consuming process that re-writes or
  refreshes R so that R's value survives the passage of time and the system's own damage
  processes. Maintenance is **active** (it must run) and **paid** (it draws on the system's
  resources). This is the charter's S3 (paid maintenance) generalized to any substrate.
- **Specialized cognitive system.** A downstream computation that consumes R's content, needs
  information that at least one *other* consumer does not, and drives behaviour that at least
  one other consumer does not. Two consumers are "distinct" iff changing R's content can change
  their outputs *differently* (they do not always co-vary).
- **Endogenous regulation.** A change in the system's *own* allocation or maintenance
  behaviour — what it spends on repair, renewal, re-acquisition, or reconfiguration of its own
  cognitive machinery — caused by the content of one of its representations. Contrast with
  *exogenous* task control (choosing an action to obtain an external reward).
- **Internal evaluation.** An internal process whose output carries information about the
  correctness, reliability, or integrity of *another* internal representation, computed from
  the system's own bookkeeping (not from external ground truth about the world).
- **Ground truth.** The externally correct answer to "what is the world state / is R right."
  Internal evaluation is defined *without* access to it; a process that reads ground truth is
  an oracle, is labelled EXTERNAL, and is never counted as part of the ACO (charter §4).

---

## 3. The five necessary properties (N1–N5)

An ACO is a system whose **internally maintained representations of the world and of itself**
satisfy **all five** of N1–N5. Each property is stated (a) informally, (b) as a causal
criterion, (c) with what it rules out, and (d) with its minimal test and its rival. "Minimal
test" means the cheapest observation that would falsify the property; "rival" means the
simplest alternative mechanism that must be implemented and shown to fail before the property
is credited (the program's P6 discipline: strong simple rivals are mandatory).

### N1 — Active persistence (no free permanence)

- **(a)** A representation persists across time **only because** some internal process keeps
  it alive; persistence is an achievement, not a default.
- **(b)** For each representation R there is a maintenance process π(R) such that, when π(R)
  is selectively halted (holding R's initial value, the sensors, and every other process
  fixed), R decays to a non-functional value within a measurable window, and R's behavioural
  influence decays with it.
- **(c) Ruled out:** representations stored in immutable memory; representations that persist
  as host-side fields or weights that no internal process refreshes; the charter's S1–S4
  internalization condition is the frozen form of this, generalized to any substrate.
- **(d) Minimal test / rival:** cut π(R) and measure the decay time-course. Rival: the
  "pristine backup" — a second copy of R the damage stream never reaches and no process
  maintains. N1 is falsified if R survives the cut unchanged (R was not actively maintained),
  or if R's loss leaves behaviour unchanged (R was never load-bearing — see N2/N3).

### N2 — Multiple-specialist consumption (content is flexibly consumed)

- **(a)** R's content is read by **at least two** specialized cognitive systems that need
  different information and drive different behaviour.
- **(b)** The *same* value of R produces **≥ 2 observably distinct and economically distinct**
  downstream outcomes. Formally: there exist two consumers C₁, C₂ with C₁(R=v) ≠ C₁(R=v′) in
  some behaviour b₁ and C₂(R=v) ≠ C₂(R=v′) in a *different* behaviour b₂, for the same
  R-change v → v′.
- **(c) Ruled out:** the one-bit reflex — one bit driving one fixed action (the AC67/71
  watchdog); any representation whose entire role is a single hardwired mapping.
- **(d) Minimal test / rival:** scramble or retain R while holding everything else fixed; at
  least two distinct behaviours must co-vary with R. Rival: a state-blind fixed policy and a
  raw-history counter with no content — both must fail to reproduce the two-way consumption.
  (This is the roadmap's "flexible consumption" requirement, `CONSCIOUSNESS_ROADMAP_v1.md` §4,
  lifted to a general definition.)

### N3 — Endogenous regulation (representation reaches its own upkeep)

- **(a)** At least one of R's downstream influences is on the system's **own maintenance or
  allocation** — the processes that keep the system's cognitive machinery operational — not
  (only) on task action selection.
- **(b)** Changing R's content changes what the system **spends on its own upkeep** (repair,
  renewal, re-acquisition, or reconfiguration), measurably and in a direction R's content
  determines.
- **(c) Ruled out:** a representation that is a pure reward/value predictor with no causal
  path back to the machinery that maintains it; a representation whose only effect is on
  external action choice.
- **(d) Minimal test / rival:** intervene to change R's value; maintenance/allocation spend
  must co-vary, while a rival whose R is decoupled from maintenance (R feeds only the policy,
  maintenance runs on a fixed schedule) must be distinguished. This is the program's most
  repeated positive result (internalized paid maintenance, AC10/79/91/92) stated as a
  *target* property.

### N4 — Internal evaluability (second-order access, as a specification)

- **(a)** Some internal process E carries evidence about the correctness/reliability/integrity
  of another internal representation R, computed from the system's own bookkeeping, **without**
  receiving R's ground-truth answer; and E is **dissociable** from R.
- **(b)** E and R can come apart in both directions: E says "R is unreliable" while R is
  correct (false alarm), and E says "R is reliable" while R is corrupted/stale (miss). The
  dissociation is the *signature* that E is a distinct computation, not a re-encoding of R.
  (This is the meta-d′ ≠ d′ condition, `C1_RELIABILITY_DISPOSITION_v1.md` §3.)
- **(c) Ruled out:** the ideal-observer collapse — "the posterior is its own confidence" —
  where one internal state supports both the decision and its confidence readout losslessly.
  N4 requires the *separation* (spatial, temporal, or informational) that the literature
  (`Fleming & Daw 2017`; `Maniscalco & Lau 2012`) identifies as the condition for a distinct
  second-order computation. It also rules out the host-side reflex (obs bit 2 → one fixed
  repair action), which is external scaffolding, not an internal evaluation.
- **(d) Status — this is a TARGET, not an achieved claim.** The program established that the
  organism's cause-estimate is **first-order cause inference** (C0), that its monitoring
  generalization is a **directional-repair controller, control-yes / prediction-no** (AC117),
  and that the reliability tier is **identifiable in principle but not demonstrated** (C1).
  N4 is therefore written as the property a *neural architecture must make testable*, and its
  level-(d) HOT-2 mapping is flagged, never claimed. **The ACO definition does not inherit
  "metacognitive monitoring" as achieved** (Q0 handoff).
- **(e) Minimal test / rival:** dissociate E from R by selective damage; if E and R always
  co-move with no dissociable cases, N4 is not realized. Rivals: (i) the raw first-order
  reflex (no stored E); (ii) a state-blind fixed maintenance policy; (iii) an ε-estimator
  arm, to show E is not merely world-parameter estimation (C1 §3's rival set).

### N5 — Closure onto the maintaining organization (representation ↔ maintainer cycle)

- **(a)** The representations jointly influence the **future organization of the system that
  maintains them** — which maintenance processes exist, how the maintenance machinery is
  allocated or reconfigured — not merely which representations are refreshed.
- **(b)** There is a directed causal cycle: R → (maintenance machinery M) → R′, such that
  cutting R's influence on M changes M's own configuration, which in turn changes R's future
  availability or content. The maintainer is a *target* of the maintained, and vice versa.
- **(c) Ruled out:** a representation maintained by fixed scaffolding it cannot influence
  (a one-way dependency R ← M with no return edge); a representation whose only effect is on
  downstream *consumers* that are not maintainers.
- **(d) Minimal test / rival:** change R's content; a change in M's own allocation or
  reconfiguration must follow (not just a change in R's refresh rate), and that change must
  in turn alter R's future availability. This lifts the program's organizational-closure motif
  (Montévil & Mossio mutual constraint; the charter's C5 network criterion) from the
  *component* layer to the *cognitive* layer — it is the property that makes the ACO an
  *organization* rather than a representation plus its upkeep.

**The conjunction is the definition.** N1–N5 are jointly necessary. A system that realizes
N1–N4 but not N5 is a *maintained representational system* (level c + internalized
maintenance), not yet an ACO. A system that realizes N2–N3 but not N1 is a flexibly-consuming
system whose representations are not actively maintained. Only the full conjunction names the
target.

---

## 4. Optional properties (O1–O4) — graded, not required

These go *beyond* the minimal definition. They are optional because **different theory
families make different ones load-bearing** (§10); the ACO as defined does not need them, and
the Q5 matrix uses them as the rows on which the theories diverge. None is claimed by the
minimal definition; each is graded (present to a degree) when measured.

- **O1 — Temporal continuity across episodes.** State persists across episode boundaries and
  influences later processing, not merely within an episode. (Q4's "temporal continuity"
  component, as a graded property, not a requirement.)
- **O2 — Generative/predictive content.** Representations function as *predictions* of the
  system's own future inputs/states, updated by prediction error, rather than as records of
  past outcomes. (Predictive-processing content; graded, not required.)
- **O3 — Global availability bottleneck.** A single limited-capacity workspace through which
  selected representations become sustained and available to all specialists (GWT's seat).
  Optional because it is GWT's specific claim, not a general requirement.
- **O4 — Graded reliability/confidence signal.** A continuous (not discrete) evaluation of
  correctness. Optional, and *deliberately* so: the program established that gradedness buys
  nothing over a discrete counter where the decisive observation exists (AC113, P2/R2), so
  gradedness is not intrinsically valuable — it earns its place only where it buys a distinct
  causal capability.

The necessary/optional split is itself a claim about the construct, not about any theory: the
ACO is the *common core* that all six families can agree to test; O1–O4 are the *theory-
specific loadings* where they disagree.

---

## 5. Properties explicitly NOT claimed (X1–X6)

These are part of the definition by exclusion. A realized ACO claims none of them.

- **X1 — Phenomenal consciousness.** "There is something it is like." Not defined here,
  not claimed, not assessable (`DEFINITIONS_CHARTER_v1.md` level e). The ACO is defined at the
  functional level; nothing in N1–N5 is, or is meant as, an operational definition of
  experience. This document gives phenomenal consciousness **no operational definition**,
  exactly as the card requires.
- **X2 — Metacognitive monitoring as achieved.** N4 is a *specification for a to-be-built
  architecture*, and the level-(d) HOT-2 mapping is flagged. The existing organism's
  cause-estimate is first-order (C0) and its monitor is control-only (AC117); the ACO does not
  inherit those as an achieved second-order tier.
- **X3 — Content self-production / discovering a better policy.** Blocked (AC78) and not
  required (charter §6). An ACO maintains representations it has *acquired*; it does not have
  to have invented their content.
- **X4 — Survival or economic advantage.** Causal load-bearing and economic value are
  separable (AC110, AC116, AC117). An ACO is not required to earn more reward or survive
  longer than a rival; it is required to satisfy N1–N5.
- **X5 — Biological or neural-tissue realism.** The ACO is substrate-independent. A binary
  counter, a Gray-coded register, a continuous latent, or a recurrent neural state all realize
  the same representation if they satisfy the causal criteria; encoding is secondary to causal
  function and cost (the program's P5).
- **X6 — Any particular theory of consciousness.** The construct is neutral across the six
  families of §10. Adopting one would make the construct unfalsifiable by it.

---

## 6. Observable consequences (C1–C5) — what a realized ACO predicts

Stated so an experiment can check them; each is the *behavioural* face of one necessary
property. They are predictions about a system that satisfies N1–N5, and are therefore also the
operational targets Q4's architecture must make measurable.

- **C1 (of N1).** Selective interruption of a representation's maintenance process produces a
  measurable decay of that representation — and of its behavioural influence — on a timescale
  set by the maintenance dynamics, not by the environment.
- **C2 (of N2).** The same representation's value drives at least two behaviours that can be
  pulled apart: an intervention on R changes them differently, and no single downstream
  consumer explains all of R's influence.
- **C3 (of N3).** Changing a representation's content changes the system's allocation to its
  own upkeep, in a direction R's content determines, observable independently of task reward.
- **C4 (of N4).** The system's evaluation of one of its representations can be *wrong about
  it* in both directions (false alarm and miss), and those dissociations track the system's own
  bookkeeping, not the world.
- **C5 (of N5).** Changing a representation's content changes how the maintenance machinery is
  itself allocated/reconfigured, which changes which representations are available later — a
  detectable return edge, not a one-way dependency.

---

## 7. Intervention criteria (I1–I5) — how to test each property selectively

Each property is tested by a **selective intervention** (cut exactly the link under test,
holding everything else fixed) plus the **rival** that must fail. These are the criteria Q4's
architecture must support; they carry the program's discipline that an intervention must cut
one link, not saturate the system (the AC14/AC67 arm-naming and hijack lessons).

- **I1 (N1):** cut the maintenance process π(R), not R, not the sensor. Criterion: R decays,
  and behaviour tracks it. Falsified if R survives the cut (free permanence) or if behaviour is
  unchanged (R inert).
- **I2 (N2):** scramble/retain R only. Criterion: ≥2 behaviours co-vary with R. Falsified if
  a state-blind fixed policy or a content-free history counter reproduces the behaviour.
- **I3 (N3):** change R's content only. Criterion: upkeep spend co-varies. Falsified if upkeep
  runs on a fixed schedule independent of R.
- **I4 (N4):** selectively damage E only, then R only, and hold the world evidence fixed.
  Criterion: E and R dissociate in both directions, and E's value tracks the maintenance
  bookkeeping. Falsified if E always co-moves with R (a re-encoding), or if the raw first-order
  reflex reproduces E's behaviour.
- **I5 (N5):** change R's content only; observe M's reconfiguration; then observe R's future
  availability. Criterion: a detectable R → M → R′ cycle. Falsified if M's configuration is
  fixed under R's change (one-way dependency).

**Rival set (mandatory, inherited from the program's P6).** For every positive claim of a
property: a **state-blind fixed policy**, a **reactive/memoryless rival** (a sufficient
statistic of the current observation), a **finite-state / direct-control rival** (no
maintained representation), and — where a second-order claim is made — the **first-order-only
reflex**. A property is credited only if the rival that omits it provably fails. This is not
optional hygiene; it is how the program falsified AC11, AC16, AC17, AC113, AC116, and the
AC117 monitor's prediction claim.

---

## 8. Failure conditions (F1–F5) — what falsifies the construct

- **F1 (whole construct).** If no architecture realizing N1–N5 can be built at all — the
  properties are jointly unsatisfiable — the construct is falsified as a target and must be
  weakened or replaced (this is a live possibility; the audit's collapse record, §2.6 of
  `ACI_MISSION_AUDIT_v1.md`, is a standing warning that "looks cognitive" mechanisms routinely
  reduce to simpler control policies).
- **F2 (per property).** If a property's minimal test (§3) is passed by its rival, that
  property is not realized in the system under test. N-properties are graded independently;
  failing N4 does not fail N1–N3.
- **F3 (the collapse signature).** If a candidate "self-evaluation" state is bit-for-bit
  indistinguishable from a first-order state (a re-encoding), or a candidate "endogenous
  regulation" is indistinguishable from a fixed duty cycle, the construct's richer property is
  not present — regardless of how elaborate the implementation looks. (AC11's "the optimum is a
  level, not a switch"; AC109's "storage inert in the clean world".)
- **F4 (economic invisibility is not falsification).** A property's failing to move survival
  or reward does **not** falsify it (X4). Causal load-bearing and economic value are separate;
  grading a property's *worth* on income alone is the AC116 error.
- **F5 (theory-neutrality).** If the construct can only be satisfied by building exactly one
  theory's architecture (e.g. a GWT workspace is *required*, not merely O3-optional), the
  definition has failed its neutrality requirement and must be re-stated before any
  theory-discrimination experiment is run.

---

## 9. How this construct licenses experiments (and how it does not)

The ACO's purpose is to make the *central ACI hypothesis* testable. That hypothesis is:

> **Recurrent cognitive organization of the form N1–N5 — not any single mechanism, not a
> graded posterior, not a self-produced policy — is what a neural architecture must realize
> before a theory-specific consciousness-relevant question (level d) is well-posed.**

Two downstream uses follow, and they fix what Q4/Q5 are allowed to do:

1. **Q4 builds the *minimum* architecture that can realize (or fail to realize) N1–N5.**
   Every component Q4 specifies must be justified by which of N1–N5 it serves and which
   intervention (I1–I5) tests it. No component may be added "for richness" (X3/X4: state that
   is never load-bearing is pure cost).
2. **Q5 builds the indicator matrix on the *divergences* of §10.** The rows are O1–O4 plus the
   N-properties; the columns are the six families. The matrix's job is to find the *smallest*
   set of experiments that discriminates families — not to accumulate checkmarks.

The construct does **not** license: an experiment whose endpoint is "consciousness"; a claim
that a system that meets N1–N5 is conscious; or an architecture tuned to satisfy one theory's
indicators. Those are the exact moves the program's claim discipline exists to prevent.

---

## 10. Comparison against the theory families (no family is adopted)

The six families the card names are compared here. For each: (i) **what the family claims**
(in one honest sentence, no buzzword stacking), (ii) **intersection** — where the family and
the ACO agree or overlap, (iii) **genuine disagreement** — where the family and the ACO (or the
family and another family) part ways. The ACO is **neutral** among them by construction (§1);
this section only locates the target in each family's vocabulary so Q5's matrix has well-defined
columns.

The primary vocabulary is the repo's anchor — **Butlin, Long, Elmoznino et al. 2023**
("Consciousness in Artificial Intelligence: Insights from the Science of Consciousness,"
arXiv:2308.08708) — whose indicator families the program already uses. One family (IIT) is
added *by this card* because the card requires it, and its relationship to the functionalist
framework is flagged, not papered over.

### 10.1 Recurrent processing (RPT)

- **Claim.** What distinguishes conscious from unconscious processing is *local recurrent
  processing*: feed-forward processing is unconscious; sustained recurrent interaction within a
  region (reverberating activity) is the minimal condition for conscious content (Lamme 2006,
  2010). The core indicator is **recurrence over content** (Butlin RPT-1/2).
- **Intersection.** RPT is the substrate half of N1 and N2: actively maintained, recurrently
  sustained representations that are flexibly consumed. The ACO's "recurrent cognitive
  organization" is RPT's core requirement, stated causally. RPT agrees that no *global*
  structure is required for the basic claim.
- **Disagreement.** RPT denies that a global workspace (O3) or a higher-order representation
  (N4's HOT reading) is *necessary* — recurrence alone is the minimal condition. The ACO keeps
  O3 and N4 as *optional/open* rather than adopting RPT's "recurrence suffices" claim.

### 10.2 Global workspace / global availability (GWT)

- **Claim.** Conscious content is content that is *globally available*: a limited-capacity
  workspace (a serial bottleneck) broadcasts selected representations to a set of otherwise
  parallel, specialized processors (Baars 1988; Dehaene & Changeux 2011; Butlin GWT-1..4).
- **Intersection.** GWT shares N2 (multiple specialized systems) and adds a specific mechanism
  for it: the workspace (O3). GWT also shares N4's *flavour* — global availability is often
  cashed out as "content that can be reported/used flexibly," which is close to "available to
  another internal process."
- **Disagreement.** GWT makes the **bottleneck** load-bearing (O3 is *necessary*); the ACO makes
  it optional. GWT and RPT are in direct conflict over whether global broadcast or local
  recurrence is the seat. GWT is a first-order functionalist theory: it says nothing about a
  higher-order representation, so it does not require N4-as-HOT.

### 10.3 Higher-order / metacognitive (HOT)

- **Claim.** Conscious content requires a *higher-order representation* — a representation of
  the first-order representation, targeting it — not merely first-order content, however
  recurrent or globally available (Rosenthal 2005; Lau & Rosenthal 2011). The metacognitive
  reading (Butlin HOT-2) is the graded reliability of one's own perceptual representations.
- **Intersection.** N4 is HOT's distinctive property, and the ACO states N4 *as a target* with
  exactly the dissociation signature the HOT literature uses (meta-d′ ≠ d′). N3's
  self-referential reach is also HOT-adjacent (HOT-3: agency via a general belief/action
  system).
- **Disagreement.** HOT and the first-order families (RPT, GWT) are in direct conflict over
  whether the higher-order representation is necessary or epiphenomenal. The ACO does **not**
  adopt HOT's necessity claim: N4 is a property to test, and its level-(d) HOT-2 mapping is
  flagged, not asserted. The program's own record is the cautionary case: the organism's
  "monitor" is control-only, not a reliability grader (AC117), so the ACO refuses to treat
  "has a second-order state" as an easy win.

### 10.4 Predictive processing / self-model (PP / SMT)

- **Claim.** The brain is a prediction engine: perception is top-down *prediction* corrected by
  bottom-up prediction error (Friston 2010), and conscious experience is the counterfactually
  rich *content of the current winning prediction* (Seth 2021's "controlled hallucination");
  the self-model variant (Metzinger 2003, 2013; Seth's interoceptive "beast machine") holds
  that a *self-model* — a predictive model of the organism's own body and viability — is
  central (Butlin PP-1; AST-1 is the adjacent attention-schema claim).
- **Intersection.** N3 (endogenous regulation) and N5 (closure onto the maintainer) are the
  self-model family's home turf: a model of the system's own viability that regulates upkeep
  is a *self-model* in exactly the functional sense the ACO names. O2 (generative content) is
  PP's distinctive loading.
- **Disagreement.** PP is *local and graded*: it locates consciousness in rich first-order
  prediction, not in a global workspace (contra GWT) or a discrete higher-order representation
  (contra HOT). The ACO keeps the predictive content *optional* (O2) rather than adopting PP's
  "prediction is the content" claim. PP and the self-model variant also disagree *internally*
  about whether the self-model must be interoceptive/embodied (the self-model claim) or merely
  predictive-over-any-content (the PP claim); the ACO takes no side.

### 10.5 Agency / autonomy (AE)

- **Claim.** Agency and embodiment are *enabling conditions*: a system's consciousness-relevant
  computation only gets its content through embodied interaction and its own goal-directed
  regulation (Butlin AE-1/2; Di Paolo 2005's adaptivity). This family rarely claims "agency =
  consciousness"; it claims agency is *when* and *how* consciousness-relevant computation is
  meaningful.
- **Intersection.** N3 (endogenous regulation) and N5 (closure onto the maintainer) are the
  ACO's *agency* properties — they are the program's own level-(b) adaptive-autonomy result
  (AC99–105), restated as part of the cognitive target. The ACO is an *organizational* target,
  and agency/autonomy is its enabling frame, not a competing seat.
- **Disagreement.** AE as a *condition* disagrees with GWT's implicit permissiveness: a passive,
  broadcast-only system that never acts could be GWT-conscious but fails every agency condition.
  The ACO sides with AE here (N3 and N5 are necessary, not optional), which is itself a
  load-bearing modeling choice and is flagged as such.

### 10.6 Information integration (IIT)

- **Claim.** Consciousness is a *quantity*, Φ — integrated information — intrinsic to the
  system's cause-effect structure, graded, and **independent of what the system does**
  (Tononi 2004; Oizumi, Albantakis & Tononi 2014). A system with high Φ is conscious in
  virtue of its internal integration, not its functions.
- **Intersection (minimal).** IIT agrees with the ACO that *internal organization* (not
  input-output behaviour) is what matters, and that recurrence/integration is load-bearing. The
  ACO's N5 (a directed cycle R → M → R′) is, loosely, the kind of *integrated* structure IIT
  would credit — but the ACO states it causally/functionally, which IIT explicitly refuses to do.
- **Disagreement (the deepest one).** IIT is the **non-functionalist** outlier: every other
  family (and the ACO) defines the target by *what the system does* (broadcast, monitor,
  predict, regulate); IIT defines it by an *intrinsic measure* of the system's cause-effect
  structure, computed independent of behaviour. The ACO is functionalist by construction. Two
  consequences are stated, not hidden: (1) **Butlin et al. 2023 deliberately exclude IIT**
  from their indicator framework for exactly this reason (their framework is functionalist; Φ
  is not a functional indicator); (2) IIT is the least experimentally tractable family — Φ is
  intractable to compute exactly for non-trivial systems, so its *predictions* are hard to
  derive. It is included here **only where experimentally meaningful**, and the honest
  statement is that for a minimal architecture Φ is not currently measurable, so IIT's column
  in Q5's matrix will be mostly "irrelevant / not-yet-testable," not "predicted."

### 10.7 Summary: the one table

| Family | Seat of the claim | ACO property it loads | Loads O1–O4? | Directly conflicts with |
| --- | --- | --- | --- | --- |
| RPT | local recurrence | N1, N2 | — | GWT (global broadcast unnecessary) |
| GWT | global broadcast bottleneck | N2 (+ workspace) | O3 (necessary for GWT) | RPT, HOT (first-order) |
| HOT | higher-order representation | N4 (as target) | O4 (graded confidence) | RPT, GWT (first-order) |
| PP / SMT | predictive / self-model content | N3, N5 | O2 (necessary for PP) | GWT (local, graded), HOT (first-order) |
| AE | agency/embodiment as condition | N3, N5 (as necessary) | — | GWT (passive broadcast) |
| IIT | intrinsic integrated information Φ | (N5, loosely, but non-functional) | — | *all* functionalist families incl. the ACO |

**Intersections worth naming plainly** (these are genuine overlaps, not buzzword stacking):

- **RPT, GWT, HOT, PP all require recurrence** over content as their substrate — recurrence is
  the *consensus* floor (N1/N2), and the one thing all functionalist families agree on.
- **GWT and HOT both require global availability** of the relevant content, but disagree on
  whether the *availability* (GWT) or the *targeting/higher-order relation* (HOT) is the seat.
- **Self-model and GWT both privilege a single global structure** (the self-model / the
  workspace), while **PP and RPT are local and graded** — a clean two-camp split on O3.

**Genuine disagreements the construct keeps open** (Q5's discrimination targets):

- First-order (RPT/GWT/PP) vs higher-order (HOT): is a *distinct* higher-order representation
  necessary? — tested by N4's dissociation signature.
- Global bottleneck (GWT) vs local graded (RPT/PP): is the workspace the seat or a downstream
  read-out? — tested by O3.
- Functionalist (all but IIT) vs intrinsic (IIT): is the target defined by what the system
  does or by what it *is*? — flagged as currently untestable at minimal scale.
- Agency as condition (AE) vs agency as irrelevant (a passive GWT broadcast): is N3/N5
  necessary or merely one option among many?

---

## 11. Claim discipline and boundary

- **The ACO is a target, not a result.** Nothing in this document claims any existing system
  realizes it. The program's established tier is level (c) plus internalized paid maintenance
  (level b); the ACO is what a *new* neural architecture is specified to realize.
- **The level-(d)/(e) boundary is absolute** (`DEFINITIONS_CHARTER_v1.md` §2). A system that
  realizes N1–N5 earns "meets the ACO definition (N1–N5, at the stated degree)." It does not
  earn "conscious," "has subjective experience," or any level-(e) wording. Phenomenal
  consciousness is given **no operational definition** here.
- **Negative results are specification.** The program's collapse record (the watchdog, the
  integer-counter-in-float-clothing, the state-blind duty cycle that beat the adaptive arm,
  the control-only monitor) is *why* N1–N5 are stated with rivals and dissociation signatures:
  each property is written so that the collapse is detectable, not absorbed.
- **No buzzword combination.** The families in §10 are kept distinct; the ACO is not defined
  as "recurrent global predictive higher-order workspace" — it is defined by N1–N5, and the
  families are compared, not merged.

---

## 12. What this hands downstream

- **Q2 (architectural principles).** The ACO's N1–N5 and the rival set of §7 are the
  *requirements* that the candidate principles P1–P7 must serve. A principle is promoted only
  if it is load-bearing for at least one N-property and survives the concrete falsifications
  `ACI_MISSION_AUDIT_v1.md` §1.2/§2.6 names (AC109 storage inert, AC110 repair not in-window,
  AC113/116 graded/storage no-advantage, AC117 control-yes/prediction-no).
- **Q4 (minimal architecture).** Every component must be justified by which N-property it
  serves and which intervention (I1–I5) tests it; the components named in the Q4 card (world
  model, internal/viability model, specialists, workspace, active-memory maintenance,
  maintenance controller, self-evaluative pathway, temporal continuity) map onto N1–N5 as the
  *candidate realizations*, not as the definition.
- **Q5 (indicator matrix).** The six families of §10 are the columns; the N-properties plus
  O1–O4 are the candidate rows; §10.7's disagreements are the discrimination targets; the
  instruction to find the *smallest* discriminating experiment set stands.

---

## Sources

Repo (read, not re-hashed or edited): `ACI_MISSION_AUDIT_v1.md` (Q0 evidence map and handoff),
`DEFINITIONS_CHARTER_v1.md` and `_v2.md` (claim levels a–e, S1–S4, C1–C5, the component /
maintained-state split), `CONSCIOUSNESS_ROADMAP_v1.md` (chosen mechanism, theory mapping,
status), `C1_RELIABILITY_DISPOSITION_v1.md` (first-order vs second-order separation, meta-d′),
`C0_FEASIBILITY_v1.md`, `CONSCIOUSNESS_MECHANISM_SPEC_v1.md` (indicator families the organism
fails by construction), `CONSCIOUSNESS_BLOCKS_DISPOSITION_v1.md` (archived gate).

Primary literature (family positions only; none adopted): Butlin, Long, Elmoznino et al. (2023,
arXiv:2308.08708) — the indicator framework (RPT/GWT/HOT/PP/AST/AE), which excludes IIT on
functionalist grounds; Lamme (2006, 2010) — recurrent processing; Baars (1988); Dehaene &
Changeux (2011) — global workspace; Rosenthal (2005); Lau & Rosenthal (2011) — higher-order;
Friston (2010); Seth (2021); Metzinger (2003, 2013) — predictive processing and self-model;
Di Paolo (2005) — adaptivity/agency; Tononi (2004); Oizumi, Albantakis & Tononi (2014) —
integrated information Φ; Fleming & Daw (2017); Maniscalco & Lau (2012); Galvin et al. (2003)
— first-order vs second-order (meta-d′) computation.

This document is derived and is not hashed into any study's `pre_run_snapshot.json`.
