# ACI neuralization map v1 — from organism principles to neural mechanisms (function, not surface)

2026-09-25. Deliverable for the Q3 card (t_93dcf012): *for each retained principle, what
is the neural analogue — translating FUNCTION, not surface implementation?*

This is a **mapping/design document**. It runs nothing, re-hashes nothing, freezes nothing,
and edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It reads its vocabulary from the three
parent deliverables — `ACI_MISSION_AUDIT_v1.md` (Q0: evidence map, P1–P7 shortlist, collapse
record), `ACI_TARGET_CONSTRUCT_v1.md` (Q1: the ACO, N1–N5, rival set, I1–I5), and
`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2: the retained principles P1–P7 and demoted
D1–D8) — and produces the four-column map the card requires, for each retained principle:
**organism principle → computational function → possible neural mechanism → falsifiable
prediction.**

**Reading discipline applied throughout.** (1) The translation is of *function*, never of
*realization*: the organism's rule bank, W catalyst, conservation laws, and succession
machinery do not map — only the computational property they instantiate does. (2) The
three negative assumptions the card fixes are enforced in every entry: biological realism
is **not** required (a "neuromodulatory signal" is a functional role — a scalar that scales
plasticity — not a claim about dopamine); Transformers are **not** the default substrate
(attention enters only as the candidate for the *optional* workspace property O3); a
wholly novel architecture is **not** assumed where an existing primitive (a gated
recurrent cell, a fast/slow-weight pair, a MoE router) already realizes the function.
(3) The level-(d)/(e) boundary is absolute (`DEFINITIONS_CHARTER_v1.md` §2): nothing here
is, or is meant as, a consciousness claim; the strongest wording a realized architecture
earns is "meets the ACO definition (N1–N5, at the stated degree)." (4) Every falsifiable
prediction carries its rival, because P6 is the gate on the whole map. (5) The demoted
principles in §4 are part of the deliverable, exactly as in Q2 — a neural architecture that
silently re-commits one re-commits a known error.

---

## 0. The one-paragraph answer

The retained principles P1–P7 translate into a small, mostly **existing** set of neural
primitives, and the translation is cleaner than the organism's physics would suggest.
**P1** (representations cost to maintain) maps to *recurrent attractor/gated-recurrent
maintenance under a per-step compute budget* — the canonical neural form of "active
persistence," with the budget as the analogue of the paid write cap. **P2** (maintenance is
internalized) maps to *homeostatic/meta-plasticity machinery* — a learned, network-computed
integrity signal gating a plasticity/maintenance pathway whose own state is vulnerable and
maintained. **P3** (cognitive state is a load-bearing content selector) maps to a *small
discrete latent consumed by at least two specialists via learned routing*. **P4**
(organizational/cognitive allocation interact) maps to a *single shared compute/energy
budget with a learned, itself-maintained allocator*. **P5** (encoding is secondary to
function and cost) maps to *discrete/sparse codes as the default, with a cost-matched
transition encoding*. **P6** (strong simple rivals) maps to a *methodological gate*: a
memoryless + state-blind + no-recurrence rival set, swept. **P7** (maintenance and cognition
compose) maps to *joint specification with simultaneous-intervention tests and a
byte-identity control*. The one primitive that is **necessary** (recurrence) is the one the
RPT family alone makes load-bearing; the theory-specific primitives (attention workspace,
predictive coding, differentiable memory) are **optional** and are assigned only to the
optional properties O1–O4. The demoted principles D1–D8 become eight **negative design
constraints**, each with its own falsifiable negative prediction, and they are the map's
sharpest content: a neural architecture that adds graded state, more state, a reliability
*predictor*, or a learned all-or-nothing switch is re-committing a frozen falsification.

---

## 1. How to read this map: the translation discipline

Three rules govern every entry, and they are the card's three "do not assume" clauses made
operational.

1. **Function, not realization.** The organism's specific machinery — the 126-bit rule
   bank, the W/C/B particles, `ac4.balance`'s conservation identities, the succession
   copy→verify→switch→remove state machine — is *one answer* to "produced, replaced,
   paid-maintained components." The neural map inherits the *property* (a representation
   is held by a paid, damage-reachable process whose machinery is itself produced), not
   the *encoding* of that property. Concretely: the W catalyst does not map to a neuron
   type; it maps to "a produced resource that gates every maintenance write, whose absence
   zeroes maintenance capacity while leaving content intact."
2. **Biological realism is optional.** Where a mechanism name is borrowed from neuroscience
   ("neuromodulation," "homeostasis," "consolidation," "attractor"), the entry states the
   *functional contract* and flags the anthropomorphic reading as not required. A
   "neuromodulatory control signal" here means: a low-dimensional (often scalar) quantity,
   computed from internal state, that multiplies learning rates or maintenance budgets
   globally. Nothing about dopamine, nor about biological plausibility, is asserted.
3. **Existing primitives before novel architectures.** Each mechanism column names the
   *simplest existing primitive* that realizes the function, and only where none exists
   does it say "new." In practice none of P1–P7 requires a novel primitive: gated recurrent
   cells, fast/slow-weight pairs, MoE routers, attention, and predictive-coding losses all
   exist. The novelty, if any, is in the *organization* (how these are wired so that the
   maintained state reaches its own upkeep), which is exactly the ACO's N5 — and is Q4's
   job, not this map's.

**Substrate-independence is the point of the map.** The ACO is defined substrate-independently
(X5): a binary counter, a Gray register, a continuous latent, or a recurrent neural state
realize the same representation if they satisfy the causal criteria. This document fixes
*which* causal criteria each principle imposes, and *which* neural primitive carries them.
A future reader should be able to substitute any differentiable substrate and re-derive the
map from the two middle columns alone.

---

## 2. The four-column schema

For each retained principle the map gives exactly the four fields the card requires:

| Column | Meaning | Not allowed to become |
| --- | --- | --- |
| **Organism principle** | P1–P7 as fixed by Q2, including its boundary word | a re-justification; Q2 already did the evidence |
| **Computational function** | the substrate-neutral property the principle names | an implementation sketch |
| **Possible neural mechanism** | the *simplest existing primitive* (or small set) realizing that function, with the resource cost made explicit | a novel-architecture proposal unless none exists; a biological claim |
| **Falsifiable prediction** | a concrete neural experiment: the ablation, the measurement, the rival, and what falsifies | a re-statement of the organism's own prediction in unchanged terms |

The "falsifiable prediction" is the load-bearing column. It must be runnable on a neural
substrate with a differentiable intervention, and it must name the rival that P6 requires.
Each prediction below is phrased so that Q4 can lift it into an intervention criterion and
Q8 can lift it into a bridge-experiment gate. Where the organism's own boundary (AC110,
AC109, AC116, AC117) restricts the claim, the prediction carries that restriction — it is
part of the specification, not a caveat to drop.

---

## 3. The map (P1–P7)

### P1 — Representations have maintenance costs

**Organism principle (Q2).** A representation *costs* to keep alive; the cost is a fact.
What does **not** survive is that the cost *buys correctness* by default — in the decision
window, correctness rides reacquisition, not continuous repair (AC110). Boundary: cost is
real; its payoff is contextual.

**Computational function.** *Active persistence* (N1): a representation's continued
availability is an achievement sustained by a resource-consuming process, not a default of
storage. "Memory" is recurrence paid out of a budget, not a stored bit. The correct
question is never "does it cost?" but "does the cost buy anything, here?"

**Possible neural mechanism.** Recurrent attractor / gated-recurrent maintenance under an
explicit per-step resource budget. The working representation is a sustained recurrent
state (point attractor or gated-cell hidden state) that must be *periodically re-energized*;
each refresh draws on a shared per-step activation/FLOP budget. The budget is the analogue
of the organism's paid write cap `min(32, 8·W)`: it is gated by a *produced* resource
(§P2's machinery), not by a host constant. Crucially, the **reference copy must live in the
same vulnerable, paid-maintained substrate as the working copy** — no hidden pristine
weight matrix that the damage/decay stream never reaches and no process refreshes. Existing
primitive: a GRU/LSTM cell (or a Hopfield-style point attractor) whose input is a budgeted
"refresh" signal; no novel architecture.

**Falsifiable prediction.** Selectively zero the recurrent input to the maintained
representation — holding its initial value, the readout weights, the sensor path, and every
other process fixed; do not damage the representation's value. Prediction: (a) the
representation's value and its behavioural influence decay on a timescale set by the
network's recurrent dynamics (the attractor relaxation / effective time constant), not by
the environment; (b) restoring the recurrent input recovers it. **Falsified if** the
representation survives the cut unchanged (it lived in immutable weights — free permanence,
N1 fails), **or if** behaviour is unchanged (it was never load-bearing — N2/N3). **Rival:**
the *pristine backup* — a second copy held in state the decay stream never reaches and no
process maintains; it must show the same decay when its own (absent) maintenance is cut.
**Companion (AC110 boundary):** in a world whose current observation is decisive, a
memoryless readout of the current observation must match the maintained state's accuracy at
equal-or-lower cost; if it does, the cost bought no correctness *there*, and the principle
is bounded, not falsified.

---

### P2 — Maintenance is controlled internally

**Organism principle (Q2).** Maintenance is *enacted and funded* through the system's own
vulnerable machinery; it does **not** mean the system knows when to repair — the trigger
may be a supplied observation, and under ambient damage the whole-bank reflex does the work.
Boundary: internalized (in-loop, damage-reachable, funded through produced machinery), not
"detects and decides."

**Computational function.** A maintenance controller that reads an internal integrity
signal and allocates a shared budget to paid writes; the controller's *own state* is in the
loop it maintains (AC87/88). The honest distinction is *who funds and enacts* the write
(internal) versus *who computes the trigger* (may be the supplied observation layer).

**Possible neural mechanism.** Homeostatic / meta-plasticity machinery. A learned pathway
(an auxiliary head, or a "slow" network) computes an internal integrity/error signal from
the network's own state and gates a plasticity/maintenance write. The gating signal is the
functional analogue of a neuromodulatory control signal — a low-dimensional quantity
multiplying learning rates or memory-write budgets. Two structural constraints carry from
the organism: (a) the maintenance machinery itself is *plastic and maintained* (fast/slow
weight pairs, or a plastic recurrent connectivity whose own state is in the maintained
substrate — the analogue of "W is produced, not scaffolding"); (b) the controller's working
state lives in the vulnerable substrate, **not** in unmaintained hyperparameters or host
fields (AC87's move of the succession controller out of Python fields). Existing primitive:
a learned gating network + fast/slow-weight consolidation path; no novel architecture.

**Falsifiable prediction.** The observer-discard equivalence (AC95-D4): strip the host's
knowledge of *when/what* to repair — replace the externally supplied repair trigger with
the network's own integrity estimate — and show maintenance still runs from the network's
own state, byte-identically to the supplied-trigger run. **Rival:** a state-blind fixed
maintenance schedule. **Falsified if** maintenance runs identically under the fixed
schedule (no dependence of the maintenance allocation on the representation's own state).
Second test: freeze the maintenance/plasticity pathway while leaving the representation and
its readouts intact (the analogue of blocking W-birth); the representation's *function*
must die with content intact — **falsified if** the function survives the machinery cut
(the machinery was scaffolding, not produced, and P2 fails as "internalized").

---

### P3 — Cognitive state can be load-bearing for future organization (not just reward)

**Organism principle (Q2).** True as a *content selector* with two-way causal coupling —
not as a memory; behaviourally, not at survival level. The same one-bit content drives ≥2
behaviourally distinct policies; the *content* is load-bearing, the *persistence* is inert
where the current observation is decisive (AC109).

**Computational function.** A minimal maintained state acts as a *selector* whose content
is flexibly consumed: the same value gates ≥2 downstream computations that need different
information and drive different behaviour, and its causal role is in the loop maintaining
future organization, not a passive reward/value predictor.

**Possible neural mechanism.** A small discrete latent (binary or low-cardinality code)
maintained by the network, consumed by at least two specialist readouts via **learned
routing / mixture-of-experts gating** — the latent selects which specialist(s) consume it,
and changing the latent changes the routing *differently* per specialist. The latent is
trained so that its content (e.g. an inferred cause) gates the specialists, and the
specialists are trained with different objectives so that the same latent value drives
different behaviour. Existing primitive: a discrete bottleneck variable + an MoE router; no
novel architecture. The world-model content (latent beliefs about external causes) and the
internal/viability content (variables relevant to continued operation) are **two distinct
contents** — Q4 must not rename reward as "viability"; P3's latent carries the former, P4's
allocator carries the latter.

**Falsifiable prediction.** Scramble or retain the latent only (hold sensors, readouts, and
all else fixed): at least two behaviours must co-vary with it, and change **differently**
(N2/C2). **Rivals:** (i) a state-blind fixed policy; (ii) a content-free raw-history
counter (a running aggregate with no selected content). **Falsified if** either rival
reproduces the two-way consumption (the latent was a re-encoding, not a distinct cause).
**Companion (AC109 boundary):** in a clean world where the current observation is decisive,
a sufficient-statistic rival (conditions on the current observation only) must match the
latent's behaviour at lower cost; if it does, only the content is load-bearing and the
persistence is inert — a boundary on P3, not a falsification of it.

---

### P4 — Organizational and cognitive resource allocation interact

**Organism principle (Q2).** The interaction is real and structural; but the *trade-off
direction* is not intuitive and must be measured in the actual per-action economics, not
assumed (AC113: a false relinquish *refreshes*; holding has ongoing cost).

**Computational function.** Maintenance and task action draw on one budget; the
observation/threshold signals that gate allocation are set by the same resources the
allocation affects — a feedback loop whose direction must be measured per action, not read
off a regret model.

**Possible neural mechanism.** A single shared compute/energy budget (per-step activation or
FLOP cap) divided between memory-maintenance and task-processing by a learned allocator,
whose own state is vulnerable and maintained. **Dynamic activation sparsity** and
**adaptive depth** are the concrete cost levers: the network decides how many units / how
much depth to spend maintaining vs processing, and that decision is itself paid out of the
same budget. The allocator is the analogue of the organism's decision register + allowance
machinery (AC96/99/100): its state is discrete, Gray-or-cost-matched encoded (§P5), and
maintained. Existing primitive: a sparsity/depth controller trained with a total-compute
penalty; no novel architecture.

**Falsifiable prediction.** Change the representation's content only; the upkeep spend
(measured compute/energy allocated to maintenance, or the count of actively maintained
units) must co-vary in a direction the content determines (I3/C3). **Falsified if** upkeep
runs on a fixed schedule independent of the content. **Companion (AC113 check, run
*before* claiming a trade-off):** measure the per-action economics in the actual compute
budget — verify that a *false relinquish* (dropping a still-useful representation) actually
costs, and that *holding* actually pays; if the "correct hold" configs collapse and
"aggressive drop" wins, the trade-off direction is the opposite of the regret model's, and
any allocation learner built on the model will fail.

---

### P5 — Representation matters more than encoding format

**Organism principle (Q2).** Promoted **unqualified** — the sharpest transfer, and the
*lesson* of the gradedness falsifications (AC113, R2/P2, AC99/100 Gray coding), not a claim
they challenged.

**Computational function.** An encoding is a cost-and-function choice, not a semantic
change. Choose the encoding whose transitions are cheapest given the causal function the
representation must serve. Discrete is the default until a graded form is shown to buy a
distinct causal capability.

**Possible neural mechanism.** Discrete localist/sparse codes as the default
representation; continuous/population codes admitted only where they buy a distinct
capability. The cost-lever form is the analogue of Gray coding: match the code's
*transition cost* to the maintenance budget — a one-hot or sparse code for a switch, a
Gray/adjacent code where adjacent states must transition cheaply. No particular code is
mandated; the rule is the deliverable. Existing primitive: any sparse/discrete bottleneck;
no novel architecture.

**Falsifiable prediction.** Replace a graded/continuous representation with the discrete
accumulator that has the same decisive observation; behaviour must be bit-identical. If it
is, the graded form was redundant (R2's proof, and it is cheap). Concretely: a learned
continuous confidence/representation is matched by a small discrete code (e.g. 3-bit,
per AC116) whenever the decisive information is a small set of discrete observations.
**Falsified only if** the continuous form drives a behaviour the discrete form cannot
reproduce — which is precisely the condition under which gradedness buys a distinct
capability, and the only condition that licenses a graded code.

---

### P6 — Strong simple rivals are mandatory

**Organism principle (Q2).** Promoted — a methodological invariant, the instrument behind
every demotion in Q2 §4, and the program's highest-value transfer.

**Computational function.** Not a mechanism but a *gate*: for every claimed internal state,
implement and sweep the rival that omits it; credit the state only if that rival provably
fails.

**Possible neural mechanism.** As a discipline, not a mechanism. Every neural internal-state
claim ships with three swept baselines: (i) the **memoryless** baseline (conditions on the
current observation only — the direct-diagnostic rival, AC109); (ii) the **state-blind
fixed schedule** (no dependence on the representation's content — AC11); (iii) the
**direct-control / no-recurrence** baseline (a feed-forward mapping with no maintained
state — the finite-state rival). Where a second-order claim is made, add (iv) the
**first-order-only reflex** (the AC117 `ones>=4` transient). A rival is valid only if it is
the *candidate's own mechanism with the contested piece removed* (AC109 rule 1), and only
if its parameter family is swept alongside the learner's own (AC11, AC116 rule 2).

**Falsifiable prediction.** This is the gate on every other prediction in this document:
for any neural internal-state claim, sweep the rival family *and* the learner's own
parameters. The claim survives only if the state contributes beyond the strongest rival.
**Falsified (for the claim)** if a state-blind fixed policy matching the best learner
configuration reproduces the behaviour — AC11's signature, meaning no acquired/stateful
decision was demonstrated. This check is effectively free and must precede any protocol.

---

### P7 — Maintenance and cognition must eventually compose

**Organism principle (Q2).** Established at the *mechanism* level; bounded at the
*survival* level; paid mechanisms' *costs* interact, so composition must be tested, not
assumed (AC115, AC82/83, AC89).

**Computational function.** Two paid mechanisms compose only if their costs do not interact
at the shared resource. The method is: prove byte-inertness at the intact boundary, then
test the interaction explicitly.

**Possible neural mechanism.** An architecture whose maintenance controller and cognitive
readouts are *jointly specified*, with explicit simultaneous-intervention tests (corrupt +
move together) and a byte-identity / invariance check at the intact boundary before any
difference is attributed to the composition. Concretely: the same budget object is shared
by the maintenance pathway and the task pathway, and the architecture is tested under
simultaneous perturbation of both. Existing primitive: the joint-specification is a wiring
choice, not a new primitive.

**Falsifiable prediction.** Run the two interventions (e.g. corrupt the representation +
move/change the task) simultaneously vs separately. Prediction: if the two costs interact
at the shared resource, the simultaneous run differs from the separate runs; if they do
not, the runs match. **Control:** byte-identity at the intact boundary — reproduce the
single-intervention numbers at the coincident ticks before attributing any difference to
the composition (AC83). **Falsified (composition is not unconditional)** if the
simultaneous run differs from the separate runs; the architecture then needs the cost
interaction designed out before any unconditional composition claim. This is the property
that makes the ACO an *organization* rather than a representation plus its upkeep, and it
is the one whose survival-level form the organism program never achieved (AC115 G4–G7).

---

## 4. The demoted principles as negative neural constraints (D1–D8)

These are the map's other half. Each demotion becomes a **negative design constraint** on
the neural architecture, with its own falsifiable negative prediction. They are not
optional; a neural architecture that violates one re-commits a frozen falsification.

| # | Negative constraint (neural form) | Falsifiable negative prediction |
| --- | --- | --- |
| D1 | Default to a discrete/sparse code; admit a continuous/population code only where it buys a distinct causal capability | A continuous/graded representation will be bit-matched by a discrete accumulator whenever the decisive observation set is finite and small; if it is not bit-matched, only then is the graded form justified |
| D2 | Do not add state for richness; add state only where a rival without it provably fails | Added state that is never load-bearing shows zero behavioural delta versus a rival without it, and its maintenance cost is pure overhead |
| D3 | Correctness rides the acquisition/update write, not continuous repair; do not build a persistent "repair loop" as the correctness mechanism | Cutting the continuous-repair pathway will **not** degrade in-window correctness; it will only degrade post-window storage persistence |
| D4 | A representation does not earn its keep by *predicting*; a monitor is a directional-repair controller (control-yes / prediction-no) | A "reliability monitor" whose output is a directioned error estimate will be inert for predicting error (a transient first-order statistic predicts equally well) and load-bearing only for the direction of a repair/control action |
| D5 | The optimum is a *level*, not a learned all-or-nothing switch; sweep the level family before claiming a switch | Sweeping the learner's own threshold will show no difference; the best policy will be an intermediate constant level, beatable by a state-blind fixed schedule |
| D6 | Causal load-bearing and economic value are separate; gate representational claims on the causal contrast, never the reward delta | A mechanism can be causally load-bearing (retention 1.0) and economically invisible (income delta ≈ 0); grading on reward delta will miss it |
| D7 | A confidence/monitoring state requires a *built separation* (spatial/temporal/informational); do not assume the posterior is its own confidence | Without a built separation, a "confidence" readout will be a re-encoding of the decision state — it always co-moves with it, with no dissociable false-alarm/miss cases (meta-d′ = d′) |
| D8 | Content self-production is not a prerequisite for representation; acquired content with internalized maintenance satisfies N1–N5 | A representation claim does not require the content to be self-invented; a system with inherited/acquired content and internalized maintenance satisfies the same properties |

D7 carries a special flag: it is the negative constraint that N4 turns into a *positive
target*. N4 (internal evaluability) is exactly the requirement that the separation D7 names
must be **built**, not assumed — so D7 is both a demotion (the organism's posterior was not
its own confidence) and the specification of what a neural architecture must construct to
make N4 testable.

---

## 5. The mechanism catalog (which candidate serves which principle)

The card's candidate list, sorted by whether the mechanism is **necessary** (load-bearing
for at least one N-property) or **optional/theory-specific** (assigned only to the optional
properties O1–O4, per Q1 §4). This is the raw material Q4 selects its minimum components
from.

**Necessary (realize a function a necessary property requires):**

| Mechanism | Serves | Role |
| --- | --- | --- |
| Gated recurrent modules (GRU/LSTM) / recurrent state-space networks | P1, P3 | the active-persistence substrate (N1); the only family substrate that is *necessary* — recurrence is RPT's load-bearing claim, and it is also N1/N2's substrate |
| Attractor dynamics | P1 | the maintenance primitive: a held point whose refresh is the re-injection that costs |
| Energy/compute budgets (per-step FLOP/activation cap) | P1, P4 | the "paid maintenance" resource — the analogue of the material/energy economy and the write cap |
| Neuromodulatory control signals (functional role: a scalar/low-dim signal scaling plasticity, *not* dopamine) | P2, P4 | the maintenance controller's gating signal |
| Plastic recurrent connectivity / fast-slow weight pairs | P2 | the *produced* maintenance machinery — the analogue of W being produced, not scaffolding |
| Learned memory consolidation (a learned write that commits an active state to a slower, still-maintained store) | P1, P2 | the succession/copy write — the analogue of copying the recipe to a successor slot; the slower store must itself be vulnerable and paid-maintained, or it is a hidden pristine backup |
| Learned routing / mixture-of-experts gating | P3 | the "content selector" — the latent selects which specialist consumes it (N2) |
| Learned internal error detection (auxiliary head predicting the network's own error) | P2, N4-target | the trigger for maintenance (control-shaped, per D4), and the self-evaluative pathway N4 names as a target |
| Sparse recurrent workspaces | P1, (O3 boundary) | a limited set of actively maintained representations; the substrate that a workspace bottleneck *would* occupy, without the bottleneck claim |

**Optional / theory-specific (assigned only to O1–O4; never required by N1–N5):**

| Mechanism | Assigned property | Note |
| --- | --- | --- |
| Attention (a serial bottleneck) | O3 (GWT) | the candidate *only* for testing GWT's workspace claim; not the default substrate — the card's Transformer clause is honored by keeping attention here and nowhere else |
| Predictive coding / self-supervised internal models | O2 (PP) | the candidate for PP's "prediction is the content" claim; D4 warns it is not how a representation earns its keep |
| Differentiable memory (external key-value / NTM-style) | O1 (temporal continuity) | the candidate for cross-episode persistence; AC109's caution applies — storage is inert where the current observation is decisive |
| Dynamic activation sparsity | P4/P5 (cost lever) | a cost lever, not a property |
| Adaptive depth | P4 (cost lever) | a cost lever, not a property |
| Recurrent latent-state models (world models) | P3's content | the world-model content; AC78's warning applies — content self-production is blocked and not required |

The catalog's headline is the card's "do not assume a novel architecture" clause made
concrete: **the necessary set contains no novel primitive.** Every necessary function is
realized by an existing, mature primitive; the ACO's novelty is organizational (N5's
closure), not architectural. The optional set is where the theory families get their
specific loadings, and it is deliberately kept out of the necessary core — which is the
neutrality requirement (F5) enforced at the mechanism level.

---

## 6. Cross-cutting: the rival set in neural form, and alignment to N1–N5 / I1–I5

**The mandatory rival set** (from Q1 §7, restated in neural terms so Q4/Q8 reuse it
verbatim):

- **State-blind fixed schedule** — a maintenance/allocation policy with no dependence on
  the representation's content.
- **Reactive / memoryless rival** — a sufficient statistic of the current observation (a
  feed-forward readout with no maintained state).
- **Finite-state / direct-control rival** — a hardwired, no-recurrence mapping.
- **First-order-only reflex** — a transient statistic (the AC117 `ones>=4` analogue), where
  a second-order claim is made.

A rival is valid only if it is the candidate's own mechanism with the contested piece
removed, and only if its parameter family is swept alongside the learner's.

**Alignment.** The map is load-bearing for the ACO's properties through the Q2 §6 mapping;
the neural mechanisms must be testable by the corresponding selective intervention, and the
table is the contract Q4 must satisfy:

| ACO property | Principles | Neural mechanism (this map) | Intervention |
| --- | --- | --- | --- |
| N1 — active persistence | P1, P2, D3 | recurrent/gated maintenance + internalized machinery | I1 (cut π(R), not R, not the sensor) |
| N2 — multiple-specialist consumption | P3, P5 | discrete latent + learned routing | I2 (scramble/retain R only) |
| N3 — endogenous regulation | P2, P3, P4 | internalized maintenance + shared budget | I3 (change R's content only) |
| N4 — internal evaluability (target) | P6, D4/D7 | learned error detection + built separation | I4 (damage E only, then R only) |
| N5 — closure onto the maintainer | P2, P4, P7 | maintainer in the maintained loop + composition | I5 (change R; observe M's reconfiguration) |

P6 is not a property-serving mechanism but the *gate* on every property's test. P7 is what
makes the conjunction an organization.

---

## 7. What this hands downstream

- **Q4 (minimum neural architecture).** The necessary mechanism set (§5) is the component
  menu; every component Q4 specifies must be justified by which N-property it serves and
  which intervention (I1–I5) tests it. The design rules are the same as Q2 §7: default to a
  discrete code (P5/D1); put the reference copy in the vulnerable, paid-maintained
  substrate (P1/P2); ship and sweep the rival set (P6); test simultaneous interventions
  (P7); do not add graded state, more state, a reliability *predictor*, or a learned switch
  (D1/D2/D4/D5).
- **Q5 (indicator matrix).** The optional set (§5, lower table) is the theory-specific
  loading: O2 → predictive coding, O3 → attention workspace, O1 → differentiable memory.
  The demotions D1/D4/D7 are the cautionary rows — do not let a theory-specific indicator
  smuggle back "graded is better" (O4), "monitoring = prediction" (D4), or the
  ideal-observer collapse (D7).
- **Q8 (bridge experiment).** The four-column map is the bridge's raw material: each
  principle supplies a neural mechanism and a falsifiable prediction with a named rival,
  which Q8 composes into the single experiment. The map's headline constraint for Q8: the
  necessary core uses no novel primitive, so the bridge experiment should be runnable with
  an existing recurrent architecture plus a budget and a routing layer — the smallest
  architecture that can falsify the hypothesis, per the card.

No autopoiesis claim and no consciousness claim is made anywhere in this document. The
strongest wording the organism program earns is unchanged (internalized paid maintenance,
causal-role-over-encoding); the ACO is a target, not a result; and this map is the
translation of the program's *principles and discipline* onto a neural substrate — not the
program's physics, mechanisms, or encodings.

---

## Sources

Repo (read, not re-hashed or edited): `ACI_MISSION_AUDIT_v1.md` (Q0 evidence map; P1–P7
shortlist §2.1/§2.4, counter-evidence §2.5, collapse record §2.6),
`ACI_TARGET_CONSTRUCT_v1.md` (Q1; ACO, N1–N5, optional O1–O4, rival set §7, interventions
I1–I5 §7), `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2; P1–P7, D1–D8),
`DEFINITIONS_CHARTER_v1.md` (claim levels a–e; S1–S4 internalization; the level-(d)/(e)
boundary). Study references read from the skill's `references/` dir: `ac109.md`,
`ac110.md`, `ac113.md`, `ac115.md`, `ac116.md`, `m6-harness-result.md` (AC117), plus
`ac111.md` as cross-reference. Frozen results read, never re-run or re-hashed. This
document is derived and is not hashed into any study's `pre_run_snapshot.json`.
