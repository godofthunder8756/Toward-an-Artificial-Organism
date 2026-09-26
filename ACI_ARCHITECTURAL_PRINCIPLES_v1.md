# ACI architectural principles v1 — which organism findings convert into principles, and which do not survive scrutiny

2026-09-25. Deliverable for the Q2 card (t_1c3a5e09): *which organism findings convert
into candidate architecture principles, and which do not survive scrutiny?*

This is a **synthesis/document**. It runs nothing, re-hashes nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not hashed
into any study's `pre_run_snapshot.json`. It reads its vocabulary from the two parent
deliverables — `ACI_MISSION_AUDIT_v1.md` (Q0: the evidence map and the P1–P7 shortlist) and
`ACI_TARGET_CONSTRUCT_v1.md` (Q1: the target construct ACO, properties N1–N5, rival set) —
and converts them into candidate architectural principles, each with the six fields the card
requires: originating evidence, counterevidence, computational interpretation, neural
implementation candidate, reason it might matter, and cheapest falsifying experiment.

**Reading discipline applied throughout.** (1) A principle is promoted only if it is
load-bearing for at least one ACO necessary property (N1–N5) **and** survives the concrete
falsifications the card names (AC109, AC110, AC113/116, AC115, AC117). (2) No principle is
promoted merely because it sounds biologically plausible; every promotion carries its own
falsification record, and every demotion is named with the experiment that killed it. (3)
Negative results are part of the specification, not noise: the demoted principles in §4 are
as much the deliverable as the promoted ones in §3. (4) "Frozen" = hashed protocol +
`mkdir(exist_ok=False)` results dir + audit (re-derives gates without simulating) + replay
(sampled exact reruns); "engineering" = pre-protocol, not frozen. (5) Seeds are the
replication unit (N seeds × 2 histories = N independent units). (6) The level-(d)/(e)
boundary is absolute (`DEFINITIONS_CHARTER_v1.md` §2): nothing here claims consciousness.

---

## 0. The one-paragraph answer

The organism program converts into **seven candidate architecture principles (P1–P7)**, each
promoted with a precise boundary, and **eight candidate principles that are demoted** because
a concrete experiment falsified them. The promotions are: (P1) representations have
maintenance costs — but that cost buys *correctness* only contextually, never as a default
(AC110); (P2) maintenance is internalized and funded through produced machinery — but
"controlled internally" means *enacted and funded* internally, not "the organism knows when
to repair" (AC117's trigger is the ambient damage count); (P3) cognitive state can be
causally load-bearing for future cognitive organization — but as a *content selector*, not a
memory, and behaviourally, not at survival level (AC109, AC116); (P4) organizational and
cognitive allocation share one budget and interact — but the trade-off direction must be
measured, not assumed (AC113); (P5) encoding is secondary to causal function and cost — the
single most decisive transfer, which *is* the lesson of the gradedness falsifications; (P6)
strong simple rivals are mandatory — the program's highest-value methodological invariant;
(P7) maintenance and cognition must eventually compose — established at the *mechanism*
level, bounded at the *survival* level, and costs interact (AC115, AC82/83). The demotions
are the record's sharpest negative result: graded/continuous is not intrinsically better,
more state is not better, ongoing repair does not carry in-window correctness, prediction is
not how a representation earns its keep, and the optimum is a level not a switch. **The
transfer to a neural architecture is these principles plus the discipline that produced them
— not the organism's physics, mechanisms, or specific encodings.**

---

## 1. How a candidate becomes a principle

The Q0 handoff fixed the shortlist (§2.1/§2.4 of `ACI_MISSION_AUDIT_v1.md`) and the Q1
handoff fixed the promotion rule: *a principle is promoted only if it is load-bearing for at
least one N-property and survives the concrete falsifications named in
`ACI_MISSION_AUDIT_v1.md` §1.2/§2.6.* This document applies that rule case by case. Three
load-bearing distinctions, carried from the program's own corrections, govern every entry:

1. **Content vs storage.** The representation's *content* is what is causally load-bearing;
   its *persistence* is a means whose value is bounded by whether the world's history is
   actually informative (AC109). A principle that confuses the two over-reaches.
2. **Causal load-bearing vs economic value.** A mechanism can be causally effective and
   economically invisible at the same time (AC110, AC116, AC117). A principle must not grade
   a representation's worth on its downstream reward delta.
3. **Mechanism vs survival.** Composition and correctness can hold at the *mechanism* level
   while failing at the *survival* level, because survival is bimodal and seed-dependent
   (AC115, AC68, AC39). A principle states which level it claims.

Each promoted principle is given a **verdict word** — *promote* (unqualified), *promote with
boundary* (true only under a stated condition), or *demote* (falsified). The verdict word is
the claim; the six fields are the evidence.

---

## 2. The verdict table

| # | Candidate principle (card's wording) | Verdict | Load-bearing for | Killed by / bounded by |
| --- | --- | --- | --- | --- |
| P1 | Representations have maintenance costs | **Promote with boundary** (cost is a fact; the cost buys correctness only contextually) | N1 | AC110 (in-window correctness rides reacquisition) |
| P2 | Maintenance is controlled internally | **Promote with boundary** (enacted/funded internally; the trigger may be supplied) | N3, N5 | AC117 (trigger = ambient damage count) |
| P3 | Cognitive state can be load-bearing (future organization, not just reward) | **Promote with boundary** (as a content selector, not a memory; behavioural, not survival) | N2, N3, N5 | AC109 (storage inert), AC116 (economically invisible) |
| P4 | Organizational and cognitive resource allocation interact | **Promote with boundary** (measure the per-action economics; direction is not intuitive) | N3, N5 | AC113 (false-relinquish refreshes; holding costs) |
| P5 | Representation matters more than encoding format | **Promote** (unqualified — the sharpest transfer) | N2 (any encoding realizes it) | — (this *is* the lesson of AC113/R2) |
| P6 | Strong simple rivals are mandatory | **Promote** (methodological invariant) | all N1–N5 (as gate) | — (its *violation* is what AC11/16/17/113/116/117 were) |
| P7 | Maintenance and cognition must eventually compose | **Promote with boundary** (mechanism-level yes; survival-level no) | the N1–N5 conjunction | AC115 (G4–G7), AC82/83 (cost interaction) |
| D1 | Graded/continuous representations are intrinsically better | **Demote** | — | R2/P2 (counter in float clothing), AC113 (tie) |
| D2 | More maintained state is better / richer internal state | **Demote** | — | AC109 (storage pure cost), AC116 (weakly dominant only) |
| D3 | Ongoing repair sustains in-window correctness | **Demote** (to: reacquisition carries correctness) | — | AC110 (repair unreachable in-window) |
| D4 | A representation earns its keep by predicting (reliability monitor) | **Demote** (to: control, not prediction) | — | AC117 (CONTROL-yes / PREDICTION-no) |
| D5 | The optimum is a learned all-or-nothing switch | **Demote** (to: the optimum is a level) | — | AC11 (state-blind duty cycle beats adaptive arm) |
| D6 | Causal load-bearing ⇒ survival/income advantage | **Demote** | — | AC110/116/117 (separable) |
| D7 | The posterior is its own confidence (ideal observer) | **Demote** | — | C0 collapse (valid only under the ideal-observer assumption) |
| D8 | Content self-production is a prerequisite for representation | **Demote / withdrawn** | — | AC78 (blocked, but not required) |

---

## 3. The promoted principles (P1–P7)

### P1 — Representations have maintenance costs

**Verdict: promote with boundary.** That a representation *costs* to keep alive is a
fact, established across the whole line. What does **not** survive is the stronger
claim that this cost is what buys *correctness* — in the decision window, correctness
rides reacquisition, not continuous repair.

- **Originating evidence.** Every acquired representation the program built lives in
  damageable, finite state and is paid-maintained through produced machinery: route memory
  (AC7/8/15/18/75), the decision register (AC96/99/100), the description (AC79/80/85/86),
  the cause-estimate (AC107/108). The maintenance machinery is itself load-bearing: block
  W-birth and the per-action write cap `min(32, 8·W)` goes to zero, the organism dies 8/8
  with content intact at death (AC91/92). The cost is not incidental — in the frozen AC9
  economy memory renewal is 1,723.6 writes ≈ 54% of all material spending (AC11 economy
  check).
- **Counterevidence.** AC110: within the decision window, correctness is carried entirely by
  `bel_write` (reacquisition at every open in-window contact); the paid repair (action 2) is
  structurally unreachable there — a single estimate bit contributes at most 3 minority
  replicas, below the whole-bank trigger's `min(ones, 7-ones) >= 4`. The repair's only
  effect is seed-dependent post-window storage drift (maintained 16/16 vs no_repair 8/16,
  G4). AC109: in the clean world the estimate's persistence is *pure cost* — 72–141
  redundant proactive renewals after the window, no decision benefit.
- **Computational interpretation.** Persistence is an active achievement, not a default: any
  state that outlives the observation that set it is held by a resource-consuming process
  gated by produced machinery. "Memory" is recurrence paid out of a budget, not a stored
  bit. The correct question is never "does it cost?" but "does the cost buy anything, here?"
- **Neural implementation candidate.** Recurrent attractor dynamics / working-memory
  maintenance as sustained recurrent activity that must be periodically re-energized (a
  cost), with the write/maintenance capacity gated by a produced resource (analogous to the
  W catalyst), and no hidden pristine backup — the reference copy must be in the same
  vulnerable, paid-maintained substrate as the working copy.
- **Reason it might matter.** P1 is the substrate of N1 (active persistence): without a
  non-trivial maintenance cost there is nothing for "internally maintained representation"
  to mean, and the ACO is just RAM plus a policy.
- **Cheapest falsifying experiment.** Hold R's initial value, the sensors, and every other
  process fixed; selectively cut the maintenance process π(R) and measure R's decay
  time-course and the behavioural co-decay. Rival: the pristine backup (a second copy the
  decay/damage stream never reaches and no process maintains). Falsified if R survives the
  cut unchanged (free permanence) or if behaviour is unchanged (R was never load-bearing).

---

### P2 — Maintenance is controlled internally

**Verdict: promote with boundary.** Maintenance is *enacted and funded* through the
organism's own vulnerable machinery (the S1–S4 internalization condition). It does **not**
mean the organism knows when to repair — the triggering signal may be a supplied observation
bit, and under ambient damage the whole-bank reflex does the work.

- **Originating evidence.** Repair/renewal is triggered by the organism's own corruption
  observation (obs bit 2; the description's own minority-count trigger `DESC_TRIGGER=2`),
  paid through produced W, and written through the organism's own vulnerable bank — the
  description is maintained 78/78 where a no-repair rival degrades to 22/78 (AC79/80/85/86).
  Erase-on-relinquishment is the organism's own write (AC75). The decision state is
  maintained through paid, W-gated writes (AC99/100). The maintenance *machinery* (W) is
  itself produced and load-bearing (AC91/92). The succession controller's working state was
  moved out of host Python fields into the maintained substrate (AC87).
- **Counterevidence.** AC117/M6: the monitor's *direction* knowledge is load-bearing for
  control (which way to repair — it keeps e correct 32/32 where majority-restore cements the
  flip), but the *trigger* that fires maintenance is the ambient damage count, which fires on
  *other* corruption and repairs the target bit as a side effect — the monitor is redundant
  with the whole-bank reflex under ambient damage. AC110: under ambient damage a single bit's
  own damage cannot reach the repair trigger at all. So "internally controlled" survives
  only as "internalized (in-world, damage-reachable, funded through produced machinery)";
  "the organism detects and decides to repair" does not.
- **Computational interpretation.** A maintenance controller that reads an internal
  integrity signal and allocates a shared budget to paid writes; the controller's own state
  is vulnerable and itself maintained (AC87). The honest distinction is *who funds and
  enacts* the write (internal) versus *who computes the trigger* (may be the supplied
  observation layer).
- **Neural implementation candidate.** Homeostatic / meta-plasticity machinery: a learning
  rule that gates synaptic maintenance by an internal integrity/error signal computed by the
  network itself, where the machinery is produced and maintained by the network (no external
  oracle, no hidden pristine reference). The design constraint is that the maintainer is
  *in* the loop it maintains.
- **Reason it might matter.** N3 (endogenous regulation) and N5 (closure onto the maintainer)
  require the representation to reach its own upkeep through the system's own machinery. If
  maintenance is external scaffolding, the ACO collapses to a representation plus a host.
- **Cheapest falsifying experiment.** The observer-discard equivalence (AC95-D4): strip the
  host-side knowledge of *when/what* to repair and show maintenance still runs from the
  organism's own state, byte-identically. Rival: a state-blind fixed maintenance schedule.
  Falsified if maintenance runs identically under a fixed external schedule (no endogenous
  dependence on the representation's own state).

---

### P3 — Cognitive state can be load-bearing for future cognitive organization, not just reward prediction

**Verdict: promote with boundary.** True as a *content selector* with causal coupling in
both directions — not as a memory, and behaviourally, not at survival level.

- **Originating evidence.** AC107: a one-bit cause-estimate discriminates two causes at
  ceiling accuracy (0/32 post-intervention mistakes). AC108 (7/7): the coupling runs both
  ways — maintenance→accuracy/use 16/16, content→adaptation/production 16/16 — and the same
  content drives two behaviourally distinct policies (relinquish vs maintain). AC109 settles
  the shape: the estimate's *content* (E_machinery vs E_world selects hold vs drop-fast) is
  load-bearing; only its *persistence* is inert.
- **Counterevidence.** AC109: storage is inert in the clean world — the discriminator is a
  pure function of the current (bound, used_held, productive) triple, so there is nothing for
  a stored bit to remember. AC116: the maintained counter is causally load-bearing (G3, 4/16
  vs 16/16 false-relinquishments) while economically invisible (income +0.5%, p=0.0625 at
  the resolution floor). AC110: repair is not load-bearing in-window. AC107 Q4: the
  estimate's causal role is behavioural, not survival-level. So "load-bearing" is bounded on
  three sides: content not storage, behaviour not survival, selector not memory.
- **Computational interpretation.** A minimal maintained state acts as a *selector* whose
  content is flexibly consumed — the same bit drives ≥2 distinct downstream outcomes — and
  whose causal role is in the loop that maintains future organization, not a passive
  reward/value predictor.
- **Neural implementation candidate.** A small discrete latent (a binary or low-cardinality
  code) whose content gates a downstream decision, maintained by the network, and consumed by
  at least two specialist readouts that need different information and drive different
  behaviour — with the readouts designed so that changing the code changes them *differently*.
- **Reason it might matter.** This is the bridge from level (c) (representation) to the
  ACO's N2/N3/N5: the representation must be *causally* in the loop that maintains future
  cognitive organization, not a passive predictor of reward. It is also the principle the
  program's own "monitor" (AC117) failed to satisfy, so it is the load-bearing target.
- **Cheapest falsifying experiment.** Scramble or retain R only, holding everything else
  fixed; at least two behaviours must co-vary with R. Rivals: a state-blind fixed policy and
  a content-free raw-history counter. Falsified if a rival reproduces the two-way consumption
  (the representation was a re-encoding, not a distinct cause).

---

### P4 — Organizational and cognitive resource allocation interact

**Verdict: promote with boundary.** The interaction is real and structural; but the
*trade-off direction* is not intuitive and must be measured in the actual per-action
economics, not assumed.

- **Originating evidence.** Allocation is a first-class resource decision throughout the
  line: the relinquishment/preservation studies (AC11/15/18/75), the internalized decision
  state (AC96/99/100/103), and the economy check that priced maintenance at 54% of material
  spending. AC82/83: the reconstruction's ~32-material cost and the route move's income cut
  *interact* to drop material below 64, set obs bit 1, and hijack the renewal — a paid
  cognition cost and an income cut landing together trip an observation threshold. AC111:
  composing autonomy and cognition trips a threshold neither alone triggers.
- **Counterevidence.** AC113: the decision-theoretic regret model did **not** transfer to
  the organism scale because the per-action economics are different — a false relinquish
  actually *refreshes* the entry (life=64 re-acquired), while holding has ongoing cost, so
  the "correct hold" configs collapsed and the "aggressive" configs won. AC116/AC117: the
  interaction is economically invisible at income level (causal but not priced). AC47/48: the
  self-funding world cannot be both stable and graded — allocation and organization are
  coupled at the structural level, so the graded region exists only as a transient of
  collapse.
- **Computational interpretation.** Maintenance and task action draw on one budget; the
  observation thresholds that gate allocation are set by the same resources the allocation
  affects — a feedback loop whose direction must be measured per action, not read off a
  regret model.
- **Neural implementation candidate.** A single attention/energy budget shared by
  memory-maintenance and task-processing, routed by a controller (analogous to neuromodulatory
  resource allocation), with the controller's own state vulnerable and maintained.
- **Reason it might matter.** N3 and N5 require the representation to reach the *allocation*
  of its own upkeep. The counterevidence is the design rule: before claiming a maintenance
  trade-off exists, measure the capability's payoff against its maintenance cost in the
  actual economy.
- **Cheapest falsifying experiment.** Change R's content only; measure whether upkeep spend
  co-varies (I3). Falsified if upkeep runs on a fixed schedule independent of R. The AC113
  check is the companion: verify that a false relinquish actually costs and that holding
  actually pays before building any allocation learner.

---

### P5 — Representation matters more than encoding format

**Verdict: promote (unqualified).** This is the sharpest transfer and the *lesson* of the
gradedness falsifications, not a claim they challenged.

- **Originating evidence.** AC99/100: Gray coding carries the success — a 2×2 factorial
  isolates the *encoding* (Gray vs binary) as the cause, the same decision state at a cheaper
  transition cost. R2/P2 (mathematical): the graded posterior is an integer counter in float
  clothing — `N = ceil(logit θ / LR)` exactly, and the strongest rival becomes bit-identical
  once the one omitted decisive observation is added. AC113: the heterogeneous two-counter
  ties the single counter at organism scale (sign-flip p > 0.05, F1 equivalence — the exact
  frozen sign-flip values are recorded in `ac113.md`). AC116: a 3-bit Gray
  counter suffices. AC85: the lesson applied in the other direction — store masks/actions as
  vulnerable state rather than deriving them by convention, so nothing on the decode path
  knows the correct policy.
- **Counterevidence.** None as a *challenge*; the principle is the invariant that *survived*
  AC113 and R2. The only caveat is a scope one: encoding is secondary **given the same causal
  function** — a change of encoding that changes what can be expressed is a change of function,
  not a free re-format (AC85's cross-check).
- **Computational interpretation.** An encoding is a cost-and-function choice, not a semantic
  change. Choose the encoding whose transitions are cheapest given the causal function the
  representation must serve; never choose an encoding because continuous/graded "looks"
  richer. Discrete is the default until a graded form is shown to buy a distinct causal
  capability.
- **Neural implementation candidate.** No particular code is mandated; the rule is to
  default to a discrete localist/sparse code and admit a continuous/population code only
  where it buys a distinct capability (e.g. graded confidence *if and only if* it is causally
  distinct — which the program showed it usually is not). Match the code's transition cost to
  the maintenance budget.
- **Reason it might matter.** It is a direct, concrete design rule for the neural
  architecture and a standing guard against the program's single most repeated collapse:
  elaborate graded machinery that is an equivalent discrete accumulator underneath.
- **Cheapest falsifying experiment.** Replace a graded/continuous representation with the
  discrete accumulator that has the same decisive observation and show the behaviour is
  bit-identical; if so, the graded form was redundant and the encoding claim is empty. (This
  is exactly R2's proof, and it is cheap.)

---

### P6 — Strong simple rivals are mandatory

**Verdict: promote.** A methodological invariant — the program's highest-value transfer, and
the instrument behind every demotion in §4.

- **Originating evidence.** The rival set is what falsified AC11 (a state-blind fixed duty
  cycle beat the adaptive arm), AC16/17 (gate-shape failures), AC109 (the direct-diagnostic
  rival = the candidate's own discriminator with storage removed), AC113 (the single
  counter), AC116 (the tuned memoryless rival with one free ambiguity parameter), and AC117
  (the transient `ones>=4` reflex that predicted perfectly). Each is a documented frozen
  falsification.
- **Counterevidence.** None as a principle; the only subtlety is that a *weak* rival is not
  a rival. AC109 rule 1: the direct-diagnostic rival must be the candidate's own discriminator
  with the storage removed, not a weaker rule set. AC116 rule 2 / AC11: the rival's parameter
  family must be swept, and your own learner's parameters must be swept too — selecting the
  learner's best member while leaving rivals at fixed settings is AC11's fatal error.
- **Computational interpretation.** For every claimed internal state, implement (i) the
  sufficient-statistic / memoryless rival (conditions only on the current observation),
  (ii) the reactive rival, (iii) the finite-state / direct-control rival, and (iv) the
  state-blind fixed policy; credit the state only if the rival that omits it provably fails.
- **Neural implementation candidate.** As a discipline, not a mechanism: every neural claim
  ships with a memoryless baseline (conditioned on the current observation only), a
  fixed/state-blind baseline, and a direct-control baseline, all swept over their parameters,
  and the claim is gated on the separation from the strongest of them.
- **Reason it might matter.** It is the difference between "the state does something" and
  "the state is necessary" — the exact distinction the ACO's N1–N5 require (each property is
  credited only if the rival that omits it fails).
- **Cheapest falsifying experiment.** The rival is the experiment: if a state-blind fixed
  policy matching the best learner configuration reproduces the behaviour, no acquired
  decision is demonstrated (AC11's signature). This check is effectively free and must
  precede any protocol.

---

### P7 — Maintenance and cognition must eventually compose

**Verdict: promote with boundary.** Established at the *mechanism* level; bounded at the
*survival* level; and paid mechanisms' *costs* interact, so composition must be tested, not
assumed.

- **Originating evidence.** AC115: the SR-2 admission gate composes with the AC105
  five-mechanism closure — G1 byte-identity, the four admission discriminations, six
  successions, desc 130/130, all 16/16. AC111: the direct channels (reconstruction never
  overwrites the estimate; the allowance never starves reacquisition) compose cleanly. AC89:
  the simultaneous challenge (corrupt + move at the same tick) closes 8/8 after the
  order-preserving decoder removed the causal path.
- **Counterevidence.** AC115 (frozen): survival-bundled gates fail on finals — G4 2/16,
  G5 2/16, G6 4/16, G7 6/16 — while the mechanism gates hold in every failing individual.
  AC111: full composition retains two failed gates (G3/G5 12/16). AC82/83: the three
  capabilities (reconstruction + description maintenance + route-move accommodation) do NOT
  compose unconditionally — the reconstruction cost and the move's income cut interact to
  hijack renewal. Composition is licensed by byte-identity, not prose, and it is bounded by
  cost interaction.
- **Computational interpretation.** Two paid mechanisms compose only if their *costs* do not
  interact at the shared resource — a paid reconstruction and an income cut landing together
  can trip an observation threshold the priority order cannot answer. The method is: prove
  the composition is byte-inert at the intact boundary (`state_hash` equality), then test the
  interaction explicitly.
- **Neural implementation candidate.** An architecture whose maintenance controller and
  cognitive readouts are jointly specified, with explicit simultaneous-intervention tests
  (corrupt + move together) and a byte-identity / invariance check at the intact boundary
  before any difference is attributed to the composition.
- **Reason it might matter.** The ACO requires N1–N5 *jointly*; a system that realizes each
  property in isolation but whose properties interfere when combined is not an ACO. This is
  the property that makes the ACO an *organization* rather than a representation plus its
  upkeep.
- **Cheapest falsifying experiment.** Run the two interventions simultaneously vs separately;
  if the simultaneous run differs from the separate runs (a cost interaction), composition is
  not unconditional. The control is the byte-identity reproduction at the coincident ticks
  (AC83: reproduce the prior study's numbers at the old schedule before attributing anything
  to the new design).

---

## 4. The principles that did NOT survive scrutiny (D1–D8)

These are the card's other half. Each started as a biologically plausible candidate and was
killed or bounded by a named experiment. They are part of the specification: a neural
architecture that silently re-commits one re-commits a known error.

### D1 — "Graded/continuous representations are intrinsically better" — demoted

Falsified twice: R2/P2 proved at the decision-theoretic level that the graded posterior is an
integer counter (`N = ceil(logit θ / LR)`, exact for every θ), and AC113 confirmed at organism
scale that the heterogeneous two-counter ties the single counter. Gradedness is not
intrinsically valuable; it earns its place only where it buys a distinct causal capability.
**The principle that survives is P5** — encoding is secondary to causal function and cost.

### D2 — "More maintained state is better / richer internal state" — demoted

AC109: the stored estimate is pure cost where the current observation is decisive (72–141
redundant renewals, zero benefit). AC116: the maintained counter is weakly dominant at the
resolution floor (p=0.0625), its only measurable edge income-invisible. State that is never
load-bearing is pure cost; add state only where a rival without it provably fails.

### D3 — "Ongoing repair sustains in-window correctness" — demoted to a scope claim

AC110: cutting repair does not degrade the estimate's correctness or use during the decision
window (G2/G3 48/48); correctness rides reacquisition. Repair is load-bearing only for
post-window storage protection (G4 8/16). **The surviving claim:** the *acquisition/update*
write carries correctness; continuous repair protects storage, not the decision.

### D4 — "A representation earns its keep by predicting (a reliability monitor)" — demoted

AC117/M6: the directioned count is *already* the wrongness signal under sticky-SET damage, so
direction knowledge is inert for prediction (a transient `ones>=4` reflex predicts perfectly,
AUC 1.0) and load-bearing only for *control* (which way to repair). The monitor is a
directional-repair controller, not a reliability grader. A representation's worth is not its
predictive accuracy.

### D5 — "The optimum is a learned all-or-nothing switch" — demoted

AC11: the learner's own threshold N∈{2,4,8,16} made no difference; the optimum was a *level*
(intermediate duty), so the whole adaptive family was beatable by a state-blind fixed duty
cycle. Sweep the level family before claiming a switch.

### D6 — "Causal load-bearing ⇒ survival/income advantage" — demoted

AC110, AC116, AC117: a mechanism is causally load-bearing and economically invisible at the
same time (retention 1.00, income +0.5%/+3%). Causal role and economic value are separate;
gate representational claims on the causal contrast, never on the reward delta.

### D7 — "The posterior is its own confidence (ideal observer)" — demoted

C0's collapse is valid only under the ideal-observer assumption, which the AC architecture
violates by construction. A monitoring/confidence state requires a *built separation*
(spatial/temporal/informational), not a re-reading of the decision state — this is the
meta-d′ ≠ d′ condition N4 names as a target.

### D8 — "Content self-production is a prerequisite for representation" — demoted / withdrawn

AC78 blocked content self-production (the production signal is a locked, path-dependent fixed
point; N_eff ≈ 1), and the roadmap removed it as a gate. Regenerating inherited organization
and discovering better organization are separate problems; a representation claim does not
wait on self-produced content.

---

## 5. The mandatory rival set (cross-cutting, inherited from P6)

Every positive claim of an ACO property is credited only if the rival that omits it fails.
The set, fixed here for Q4/Q5 to reuse (from `ACI_TARGET_CONSTRUCT_v1.md` §7):

- **State-blind fixed policy** — a maintenance/allocation schedule with no dependence on the
  representation's content.
- **Reactive / memoryless rival** — a sufficient statistic of the current observation (the
  direct-diagnostic rival, AC109).
- **Finite-state / direct-control rival** — no maintained representation, hardwired mapping.
- **First-order-only reflex** — where a second-order claim is made (the AC117 `ones>=4`
  reflex).

A rival is valid only if it is the *candidate's own mechanism with the contested piece
removed* (AC109 rule 1), and only if its parameter family is swept alongside the learner's
(AC11, AC116 rule 2). This set is the program's single highest-value transfer; it is how
AC11, AC16, AC17, AC113, AC116, and the AC117 monitor's prediction claim were all falsified.

---

## 6. Mapping principles onto the ACO (N1–N5)

The Q1 handoff fixed the promotion rule (a principle must be load-bearing for at least one
N-property). The compact map:

| ACO property | Load-bearing principles |
| --- | --- |
| N1 — active persistence (no free permanence) | P1 (cost), P2 (internalized), D3's correction (reacquisition, not repair) |
| N2 — multiple-specialist consumption | P3 (content selector), P5 (any encoding realizes it) |
| N3 — endogenous regulation | P2, P3, P4 (reach one's own upkeep) |
| N4 — internal evaluability (target, not achieved) | P6 (rival set), D4/D7's corrections (separation, control-not-prediction) |
| N5 — closure onto the maintainer (R→M→R′ cycle) | P2, P4, P7 (composition) |

P6 is not a property-serving principle but the *gate* on every N-property's test. P7 is the
property that makes the conjunction an organization.

---

## 7. What this hands downstream

- **Q3 / Q4 (minimal architecture).** Every component Q4 specifies must be justified by which
  N-property it serves, which principle (P1–P7) it instantiates, and which intervention
  (I1–I5) tests it. The design rules are: default to a discrete encoding (P5); put the
  reference copy in the vulnerable paid-maintained substrate (P1/P2); ship the rival set and
  sweep it (P6); test simultaneous interventions, not just separate ones (P7).
- **Q5 (indicator matrix).** The demotions D1/D4/D7 are the cautionary rows: do not let a
  theory-specific indicator smuggle back "graded is better" (O4 must be shown to buy a
  distinct capability, not assumed), "monitoring = prediction" (N4's dissociation signature
  is control-shaped per AC117), or the ideal-observer collapse.
- **Q7 (organism exit).** This document is the terminal hand-off of the cognition track: the
  organism program's *transferable content* is P1–P7 plus D1–D8, not its physics or
  mechanisms. The "more organism work?" judgment from the audit stands — NO — and this
  document is why: the principles are extracted; nothing further in-model changes them.

No autopoiesis claim and no consciousness claim is made anywhere in this document. The
strongest wording the organism program earns is unchanged: internalized paid maintenance and
causal-role-over-encoding are established; the ACO is a target, not a result.

---

## Sources

Repo (read, not re-hashed or edited): `ACI_MISSION_AUDIT_v1.md` (Q0 evidence map; P1–P7
shortlist §2.1/§2.4, counter-evidence §2.5, collapse record §2.6),
`ACI_TARGET_CONSTRUCT_v1.md` (Q1; ACO, N1–N5, rival set §7, failure conditions §8),
`DEFINITIONS_CHARTER_v1.md` (claim levels a–e; S1–S4 internalization; C1–C5 component list;
the frozen closure criterion). Study references read from the skill's `references/` dir:
`ac109.md`, `ac110.md`, `ac113.md`, `ac115.md`, `ac116.md`, `m6-harness-result.md` (AC117),
plus `ac111.md`, `ac112.md`, `ac114.md` as cross-references. Frozen results read, never
re-run or re-hashed. This document is derived and is not hashed into any study's
`pre_run_snapshot.json`.
