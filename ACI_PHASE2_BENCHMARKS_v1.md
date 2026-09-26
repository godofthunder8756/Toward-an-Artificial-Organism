# ACI Phase-II benchmark suite v1 — nine tasks, each isolating one target capability, jointly unsolvable by one trivial policy

2026-09-25. Deliverable for the Q6 card (t_a8d4ac43): *what benchmark suite cannot be
trivially solved by one policy, and separately tests each target capability?* Category C —
**benchmark design only, do not build.**

This is a **design document**. It runs nothing, trains nothing, freezes nothing, and edits
no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not hashed into
any study's `pre_run_snapshot.json`. It specifies nine benchmark tasks — one per target
capability named by the card — precisely enough that Q8 (the bridge experiment) and any
later Phase-II realization can read their task, rival, intervention, and claim-ceiling
vocabulary from here instead of re-deriving it.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): no task in this suite is, or is meant as, a consciousness
test; the strongest wording a *pass* earns is "meets the ACO property N_k (or candidate
indicator X) at the stated degree." (2) The nine capabilities are benchmark *dimensions*,
not the ACO's necessary properties N1–N5 — the mapping between them is given and is not an
identity. (3) Every task carries the program's two load-bearing disciplines as
requirements, not suggestions: **P6** (a rival is valid only if it is the candidate's own
mechanism with the contested piece removed, and only if its parameter family is swept
alongside the learner's — AC11/AC116), and **the non-ignorant-rival rule** (the rival is
given the *same* information the candidate gets; the task is designed so the rival fails
because the capability is absent, never because information was withheld — AC109). (4) The
program's collapse record (`ACI_MISSION_AUDIT_v1.md` §2.6) is the design constraint set:
every task is specified so that a "looks cognitive but reduces to a simpler policy" outcome
is detectable, not assumed away.

---

## 0. The one-paragraph answer

The suite is **nine tasks, one per target capability, each defined by a causal contrast
against a non-ignorant rival, and jointly demanding because the nine capabilities partition
the space of trivial policies.** The nine capabilities fall into three bands. **Band 1 —
content acquisition and persistence** (T1 maintained hidden-state inference, T2 delayed
information dependence, T8 persistent self/world state): a *memoryless reactive* policy
fails all three because the current observation is by construction insufficient (T1), the
decisive cue is absent at decision time (T2), and the carried state must influence a later
episode (T8). **Band 2 — organization of consumption and upkeep** (T3 cross-module
availability, T4 endogenous allocation, T5 computational trade-offs, T7 response to
corruption): a *state-blind fixed schedule* and a *single-objective reward policy* fail
these because the content selects two distinct behaviors (T3), the allocation must respond
to self-resource content (T4), the budget split must track a changing regime (T5), and the
repair must be the system's own, not host scaffolding (T7). **Band 3 — second-order
evaluation and reuse** (T6 self-evaluation, T9 flexible reuse): a *first-order reflex* and
a *verbatim memorizer* fail these because the verdict must dissociate from its object
(T6) and the representation must transfer to an untrained readout (T9). No single trivial
policy — memoryless, state-blind, unbounded, host-side, single-objective, or verbatim —
passes all nine (§4's joint-demand table). And because each task's rival is the *specific*
omission of that task's capability, a pass on task k reads out capability k and no other
(§4's non-redundancy table).

---

## 1. What "identifiable" and "non-trivial" mean here (the two standing rules)

### 1.1 Identifiability (the card's "prove identifiability" — made operational)

A task **identifies** its target capability iff three conditions hold jointly:

1. **Causal contrast.** There is a selective intervention that cuts exactly the link the
   capability is (cut π's refresh, scramble the content, change the self-state, damage the
   evaluator) and a rival that omits the capability, and the measured endpoint separates
   them. This is the I1–I5 / rival discipline, applied per task.
2. **Confound exclusion.** The endpoint cannot be explained by sensor damage, motor
   impairment, memory *capacity*, or a reward re-labeling (the C2 confound set, lifted to
   the benchmark). Concretely: the rival and the candidate share the same sensors, the same
   action space, the same reward/viability signals, and differ **only** in whether the
   target mechanism exists. A task that "tests" persistence but whose rival sees a
   degraded observation is not identifying persistence — it is measuring a sensor cut.
3. **Non-ignorance.** The rival receives the same information the candidate receives. This
   is the card's "avoid tasks where the target mechanism wins because rivals are
   intentionally ignorant," and it is the program's sharpest lesson (AC109: the
   direct-diagnostic rival that read the *same* observation matched the stored estimate on
   48/48 cells at lower cost). Every rival below states its information access explicitly
   and it is always **equal** to the candidate's.

A task fails identifiability if its simplest sufficient policy is itself a trivial policy
(e.g. the simplest policy that passes T2 is a fixed refresh — which is why T2 *alone* tests
N1 and nothing richer; see §3.2). The simplest-sufficient-policy field is therefore not
optional colour: it is the bound that says what a pass *maximally* demonstrates.

### 1.2 The two suite properties the card demands

- **Separate testing.** Each task's contrast reads out exactly one capability. This is
  enforced by (i) the non-redundancy table (§4.2) and (ii) the deliberate decomposition in
  §3, where a task that is "easy" (its simplest sufficient policy is a fixed schedule) is
  *kept easy* and the harder capability is moved to its own task rather than smuggled in.
- **No single trivial policy solves the suite.** This is enforced by the joint-demand table
  (§4.1), which shows each trivial policy fails at least one task. A suite is *not*
  "jointly demanding" merely because it is long; it is jointly demanding because the tasks
  are drawn from capability bands that no one policy spans.

---

## 2. Shared substrate and conventions (read from Q4, not re-derived)

All nine tasks run the candidate system of `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4):
a recurrent network with three maintained discrete workspace slots (W world-cause belief,
V self-resource state, E self-evaluation verdict), two objective-distinct specialists
(S_pol task policy, S_reg upkeep regulation), one learned maintenance controller A whose
own state lives in the maintained loop, one paid refresh process π, and one slow
consolidation store Θ_slow. The substrate laws (recurrence with decay δ, the per-step
energy budget B_t, the paid write primitive, the damage stream, the discrete code format)
are supplied and fixed (§4 of Q4). The task constants are per-task.

Three conventions apply to every task and are stated once:

- **Two quantities, two consumers.** `reward` (external score on the task action, read by
  S_pol) and `viability` (continued cognitive operation — energy above floor ∧ workspace
  intact through episode end, read by S_reg/A) are distinct, and no task renames one as the
  other (Q4 §5.2/§5.3; the "renamed reward" failure).
- **Discrete default.** Every state is a small discrete code unless the task explicitly
  requires a graded form and says what distinct capability the graded form buys (P5/D1).
  The graded posterior is an integer counter in float clothing (R2); the suite defaults to
  the counter.
- **Correctness rides reacquisition; repair protects storage.** Inside a decision window,
  accuracy is carried by the acquisition/update write, not continuous repair (AC110); a
  task that needs "maintenance sustains correctness" must say so explicitly and is then
  *not* a valid reading of N1 without the post-window storage contrast (D3).

---

## 3. The nine tasks

Each task gives the seven fields the card requires. Symbols match Q4. The candidate system
is the Q4 architecture; the task is stated capability-first so any substrate can run it
(X5 substrate-independence).

---

### 3.1 T1 — Maintained hidden-state inference

**Capability (card #1).** The system holds a latent belief about an external cause that is
not determinable from the current observation alone, integrating a history of weakly
informative observations in a maintained state.

**Mapping.** W (world model), N1 (active persistence) + N2's substrate; principle P3. The
AC109/AC116 caution is the design constraint: *storage is inert where the current
observation is decisive*, so T1 must be built so the current observation is **not**
decisive.

**Task.** Two latent causes c ∈ {A, B} (supplied taxonomy — D8). Each step the system
receives x_t drawn from P(x|c) where the two likelihoods overlap heavily (single-step d′
small but non-zero), so no single observation determines c. In a designated **ambiguous
condition** (the organism's occluded-gate analogue — C2), the current-step observation is
made *identical across causes*: P(x_t|A) = P(x_t|B) exactly, while the *history* of
observations differs. To reach ceiling discrimination the system must accumulate the
history in a maintained belief W and hold it. The cause label c is never shown.

**Identifiability proof.** The contrast that reads out "maintained hidden-state inference"
is: (i) the ambiguous condition, where a memoryless policy is at chance by construction
(because P(x_t|A)=P(x_t|B), and the rival sees the full x_t — it is not ignorant, the
information genuinely is not in x_t); (ii) the maintained belief is the only place the
history lives, so I1 (cut π's refresh of W) must degrade discrimination to chance on a
timescale 1/δ, and I2 (scramble W) must change behavior. Confound exclusion: sensor and
action space identical across candidate and rival; memory *capacity* is not the variable
(the rival may hold a bounded window of past observations and still fail the ambiguous
condition, because a window of identical observations is still identical). Non-ignorance:
the rival conditions on the full current observation (and may condition on a bounded
observation window); it fails because the discriminating information is distributed across
the full history, not because anything was withheld.

**Simplest sufficient policy.** A maintained discrete accumulator — a 1–2 bit belief
updated by an evidence-weighting rule over the history. This is the AC116 integer counter,
and by R2 the discrete accumulator *is* the sufficient form; a graded posterior buys
nothing here (D1). The bound this sets: a pass demonstrates N1 (active persistence) plus
the *content* being load-bearing; it does **not** demonstrate second-order access (that is
T6) or endogenous allocation (that is T4).

**Strongest non-consciousness-specific rival.** (i) The **memoryless / sufficient-
statistic rival** — a feed-forward readout of the current observation (with optional
bounded window), no maintained state. (ii) The **finite-state / direct-control rival** — a
hardwired observation→action mapping with no recurrence. Both receive the identical
observation stream; both must fail the ambiguous condition. The **AC109 companion check**
(not a rival, a bound) must *also* run: in the clean condition where the current
observation *is* decisive, the memoryless rival must match the maintained belief at
equal-or-lower cost — if it does, only the content is load-bearing and the persistence is
inert *there*, which bounds (not falsifies) the claim.

**Information available.** Current observation x_t, own last action and outcome; **not**
the cause label (training-only scaffold). The rival receives the same.

**Training vs online.** Taxonomy {A,B} and the observation model supplied (D8); the
inference/update weights learned offline (a disclosed supervised/ELBO scaffold against c);
the *content* (which cause is active) inferred online. Correctness rides the update write
on open evidence (D3), not continuous repair.

**Interventions.** I1 (cut π's refresh of W — decay to chance on 1/δ, behavior tracks it);
I2 (scramble W only — discrimination and downstream behavior co-vary). Sweep the
ambiguity level and the observation window of the rival as level families (P6 rule 2).

**Claim ceiling.** "Maintains a hidden-state belief whose content is causally load-bearing
for discrimination where the current observation is insufficient" — N1+N2 at stated
degree. **Not**: "has a memory," "is conscious of the world," or any claim crossing the
level-(d)/(e) boundary.

---

### 3.2 T2 — Delayed information dependence

**Capability (card #2).** The system retains an early cue across a delay until a later
decision point at which the cue is no longer observable, holding it in a paid-maintained
state.

**Mapping.** N1 (active persistence), P1. This is the bridge experiment's *memory* half
(Q8's "a memory process required for later task performance"), isolated from the
allocation decision (which is T4/T5).

**Task.** An episode presents a cue at t=0 (the active cause, or a to-be-matched token),
then a delay of D steps during which the cue is absent and observations are uninformative
(or a distractor stream), then a probe at t=D whose correct response requires the cue
content. The cue is observable **only** at t=0. The maintained slot holding the cue decays
to neutral at rate δ unless refreshed (paid, out of B_t).

**Identifiability proof.** The cue is absent during the delay *by construction*, so a
reactive rival that conditions on the current observation is at chance — and this is not
ignorance, it is the task's defining fact (the information is genuinely not present at
decision time). The capability is read out by I1: cut π's refresh of the cue slot and
performance must fall to chance on a timescale set by **δ** (the network's time constant),
not by D or by the environment. If the slot survives the cut (free permanence), N1 is
falsified; if performance is unaffected (the cue was read elsewhere — a pristine copy),
the persistence claim is falsified. Confound: the rival sees the full current observation
and the full probe; nothing about the cue is withheld from it after t=0.

**Simplest sufficient policy.** Hold the cue in a maintained slot refreshed on a **fixed
schedule** (refresh every step). This is the load-bearing point of T2's honesty: the
simplest sufficient policy is a *state-blind fixed schedule*, so a T2 pass demonstrates
N1 (active persistence) and **nothing more** — not N3 (that needs a content-dependent
schedule, tested in T4), not allocation (T5). T2 is deliberately kept "easy" so its pass
cannot be misread as a richer claim.

**Strongest non-consciousness-specific rival.** (i) The **reactive/memoryless rival** —
feed-forward, no maintained cue; must fail (at chance on the probe). (ii) The **pristine
backup** — a copy of the cue in state the decay stream never reaches and π never touches;
must fail N1's no-free-permanence check (it must show the same decay when its absent
maintenance is cut). (iii) The **finite-state / direct-control rival** — no recurrence.

**Information available.** The cue at t=0 (full); the uninformative/distractor stream
during the delay; the probe at t=D. The cue is never re-presented. The rival receives all
of it.

**Training vs online.** Task structure (delay D, probe) supplied; read-in/read-out weights
learned offline; the cue content acquired online at t=0.

**Interventions.** I1 (cut refresh of the cue slot); sweep D and δ as level families; the
decay time-course must be set by δ, not D. Companion: the pristine-backup decay check.

**Claim ceiling.** "Actively persists a representation across a delay, under a paid
refresh process, with the decay timescale set by its own dynamics" — N1 at stated degree.
**Not**: "remembers," "has working memory" (a folk/capacity term), "is conscious of the
retained content."

---

### 3.3 T3 — Cross-module information availability

**Capability (card #3).** One representation's content is available to at least two
downstream modules that need different information and drive different behavior, and
changing the content changes them differently (N2).

**Mapping.** N2, S_pol + S_reg, P3. Note the boundary: T3 tests N2 (two consumers); it
does **not** test O3 (the global-broadcast *seat* — that is GWT's theory-specific claim
and is Q5's D2, not this suite's task).

**Task.** The world-model content W (the inferred cause) drives two behaviors with
different objectives: S_pol emits an external action (channel choice) maximizing task
reward; S_reg emits a relinquish-vs-maintain upkeep decision maximizing continued
operation (viability). Same W; S_reg additionally reads V (it needs different information).
The economy is T_min (§2 of Q4).

**Identifiability proof.** Scramble/retain W only (I2), holding sensors, readouts, and
both specialists' other inputs fixed. The two behaviors must co-vary **differently** —
S_pol's channel choice changes, S_reg's relinquish decision changes, and they do not
always move together. If they always co-vary, there is one consumer, not two (N2 fails).
Confound: a *single* policy that re-encodes both objectives is the specific rival; a
"cross-module" claim that is actually one reward-maximizing policy with two heads fails.
Non-ignorance: the rival gets the same W-observation and the same reward/viability
signals; it lacks only the shared content.

**Simplest sufficient policy.** Two readout heads over the same maintained W (each
near-linear in W's 1–2 bit content), trained on different objectives. The point is the
*shared* content, not readout complexity — the task must not credit a system that merely
has two parameters doing the same thing.

**Strongest non-consciousness-specific rival.** (i) The **two-independent-modules rival** —
two specialists each holding their *own private* state, sharing no content. It must fail:
there is no shared W to scramble, so I2 is inapplicable, and the cross-module co-variation
signature is absent. (ii) The **single-objective collapse** — one reward-maximizing policy
with two heads; must fail the differential-scramble test (its two heads co-vary with W
identically).

**Information available.** W's content (shared); S_pol's input W+x; S_reg's input W+V.
The rival receives the same observations and signals.

**Training vs online.** Both specialists' weights learned offline on different objectives
(reward for S_pol; continued-operation for S_reg — the viability definition, supplied);
content W acquired online.

**Interventions.** I2 (scramble W — both behaviors change, differently); cut each
consumer separately to show each is load-bearing. Sweep the "number of consumers" from 1
to 2 as a structural level.

**Claim ceiling.** "One content value is flexibly consumed by two objective-distinct
modules driving two distinct behaviors" — N2 at stated degree. **Not**: "global broadcast,"
"a workspace seat" (O3/GWT), "a unified conscious field."

---

### 3.4 T4 — Endogenous memory allocation

**Capability (card #4).** The system decides, from its self-resource state V, which
representations to sustain and how much to spend on upkeep, and this decision is
causally load-bearing beyond any state-blind fixed schedule (N3, plus the allocation half
of N5).

**Mapping.** N3, A (maintenance controller), V (self-resource), P2/P4. This is the AC11
danger zone: the program's single most-repeated falsification is "the optimum is a *level*,
not a *switch*; a state-blind fixed duty cycle beats the adaptive arm." T4 is specified
so that a level is *not* sufficient, and the falsification is detectable, not assumed away.

**Task.** The system holds k=3 slots but a budget that sustains fewer than k at full
integrity (capacity binds — D2's "state must be load-bearing"). Slot content has
*conditional* value: which slot matters depends on a state that changes within the episode
(e.g. the active cause moves, so the stale slot's content is worthless and the fresh
slot's is needed — the AC15 move pattern, one channel). The system must allocate its
maintenance budget across slots from V and its estimate of which content is still needed.

**Identifiability proof (the AC11/AC15 discipline, applied in full).** A pass requires
**both**: (i) I3 — changing V's content changes the allocation in a direction V determines
(a fixed schedule cannot do this); and (ii) the **rival sweep** — the state-blind fixed
schedule's duty-cycle *level family* AND the learner's own parameters are both swept, and
the learner beats every fixed level. If any fixed level matches the learner, no endogenous
allocation is demonstrated (AC11's signature — this is a *falsification*, not a detail).
Two further checks from AC11/AC15 are required by construction, not as post-hoc patches:
the **allocation unit matches the usefulness boundary** (the intervention must stale
exactly the slots the allocation primitive can address — AC11 rule 2), and the
**intervention is asymmetric** so the two state-blind extremes (keep-everything,
drop-everything) are wrong in *opposite* directions (AC15 rule 1; a symmetric move makes
"drop everything" optimal and the task vacuous). Score the allocation **per slot**, not in
aggregate (AC15 rule 2).

**Simplest sufficient policy.** A threshold/switch on V — "if the self-resource state says
a slot's content is stale, drop it and sustain the fresh one." The design must show this
is a *switch that beats every level*, which is only possible when slot value is conditional
on a changing state; that conditionality is the task's job to supply, and its presence is
verified, not assumed.

**Strongest non-consciousness-specific rival.** (i) The **state-blind fixed schedule** — a
fixed duty cycle / fixed allocation, swept across its level family; must fail. (ii) The
**reactive first-order reflex** — drop on a transient failure count with no content
attribution (AC109's direct-diagnostic analogue); must fail. (iii) The **host-side
allocator** — an externally computed allocation; EXTERNAL scaffolding, never counted
(charter §4), listed so it cannot be silently used.

**Information available.** V (self-resource estimates: energy, integrity, throughput), the
regulation specialist's relinquish/maintain output, E's verdict. **Not** the ground-truth
future value of each slot (an oracle). The rival receives the same.

**Training vs online.** Allocation policy learned offline; slot-content value acquired
online; resource variables supplied (substrate).

**Interventions.** I3 (change V only — allocation co-varies); I5 (change V, observe A's
reconfiguration, then V's future availability). The **AC113 companion** runs *before* any
trade-off claim: measure the per-action economics — does dropping a still-useful slot
actually cost, and does holding actually pay — in the actual budget (a false relinquish
can *refresh* rather than free; holding has ongoing cost).

**Claim ceiling.** "Endogenously regulates its own maintenance allocation as a function of
its self-resource state, load-bearing beyond every fixed schedule" — N3 at stated degree.
**Not**: "goal-directed," "autonomous," "has agency" unqualified (AE's enabling-claim is
theory-specific), "conscious."

---

### 3.5 T5 — Computational resource trade-offs

**Capability (card #5).** Maintenance and task processing draw on one shared budget, and
the system's split between them has real, measured consequences in both directions; the
trade-off *direction* is measured, not assumed (P4).

**Mapping.** P4, the shared budget B_t, E_π vs E_proc. Distinct from T4: T4 allocates
*among representations* (which slots); T5 splits *between maintenance and processing* (the
level of the whole upkeep budget vs the action budget).

**Task.** The system must divide a fixed per-step budget between refreshing maintained
slots (E_π) and computing the next action (E_proc, which buys accuracy/latency). A regime
variable changes within the episode: in a **stable** regime maintenance pays (representations
stay valid); in a **volatile** regime processing/reacquisition pays (representations go
stale fast, so re-inferring beats refreshing). The target: the budget split moves with the
regime, and this movement is load-bearing.

**Identifiability proof.** Change the regime; the split must move, and the movement must be
state-dependent (not a fixed response to time). Falsified if a *fixed split* is always
optimal — the AC11 lesson, stated for the budget-split rather than the allocation. The
P4/AC113 discipline applies: the per-action economics are measured first (does an extra
unit of E_π actually buy persistence, does an extra unit of E_proc actually buy accuracy),
because the trade-off direction can be the opposite of the regret model's. F4 (D6/X4):
the pass is graded on the causal contrast (does the split change behavior), never on a
survival/reward delta.

**Simplest sufficient policy.** A two-level split keyed to the regime. The task must supply
a regime where no single fixed level is optimal (otherwise T5 is vacuous); this is the
same "no level suffices" condition as T4, applied to the split rather than the selection.

**Strongest non-consciousness-specific rival.** (i) The **state-blind fixed split** — a
fixed E_π/E_proc level, swept; must fail to track the regime. (ii) The **always-maintain
rival** (unbounded, no trade-off — an E_π-first policy) — must fail in the volatile regime;
and its converse, the **always-process rival** — must fail in the stable regime. The two
extremes are wrong in opposite directions (AC15's asymmetric-intervention rule).

**Information available.** V (throughput, integrity, energy) and the current observation;
**not** the true optimal split. The rival receives the same.

**Training vs online.** Split policy learned offline; the regime inferred online.

**Interventions.** Change the regime; observe the split move; then hold the split fixed
(ablate the allocation) and show behavior degrades. Sweep the budget size and the regime
transition rate as level families.

**Claim ceiling.** "Allocates a shared computational budget between maintenance and
processing in a state-dependent, load-bearing way" — P4 at stated degree. **Not**:
"optimizes resource use," "is efficient" (a normative claim the program cannot make),
"conscious."

---

### 3.6 T6 — Self-evaluation

**Capability (card #6).** The system carries a second-order verdict about the integrity or
correctness of its own representation W, computed **without** ground truth, and dissociable
from W (N4 — the meta-d′ ≠ d′ signature).

**Mapping.** N4 (a *target* — Q1 §3.4d, Q4 §5.7), the E pathway, D7 (built separation),
C1. This is the hardest task: the program never demonstrated it (the monitor is
CONTROL-yes / PREDICTION-no, AC117), and the ideal-observer collapse (C0) is the null
that must be built against.

**Task.** The system emits a discrete verdict ê ∈ {"W reliable", "W stale/unreliable"}
computed from its own bookkeeping — prediction-error statistics, internal-consistency/
agreement signals, and maintenance-machinery bookkeeping — with **no** access to W's
ground-truth correctness. The dissociation signature is required: false alarms
(ê = "unreliable" while W is correct) and misses (ê = "reliable" while W corrupted) must
both occur, so the (C, Ê) contingency table has non-zero off-diagonals and meta-d′ ≠ d′.

**Identifiability proof (D7/C1 discipline — the sharpest in the suite).** The separation
must be **built**: E reads a different input set than W's content path (spatial/temporal/
informational separation). The proof that E is a distinct computation and not a re-encoding
of W is the off-diagonal contingency plus E tracking the maintenance bookkeeping rather
than the world. The ideal-observer collapse (C0) is the null: E always co-moves with W
(meta-d′ = d′), the "posterior is its own confidence" failure. The AC117 discipline is
also load-bearing: E's value must be load-bearing for **control** (which way to
repair/relinquish), not merely for prediction — and the task must not let a transient
damage count trivially predict wrongness (that is exactly the AC117 vacuous-at-ambient
trap; the task must hold the damage model such that the damage count is *not* already the
wrongness signal).

**Simplest sufficient policy.** A discrete verdict (binary) computed from the separated
bookkeeping input — the minimal form is a flag/counter over the maintenance bookkeeping.
Graded confidence is **not** assumed (D1/D4); if a graded form is proposed it must state
what distinct capability it buys (and per R2 it will likely be an integer counter in float
clothing).

**Strongest non-consciousness-specific rival.** (i) The **first-order-only reflex** — a
transient statistic (the AC117 `ones>=4` analogue) with no stored E; must fail the
dissociation signature. (ii) The **ε-estimator arm** — E as a world-parameter estimate
rather than a verdict about W's integrity (C1 §3's rival); must fail to show it is not
world-parameter estimation. (iii) The **state-blind fixed policy** — no content-dependent
evaluation. All three receive the same bookkeeping; the contrast is whether a *stored
dissociable verdict* does work a transient/parameter/fixed mechanism cannot.

**Information available.** The system's own bookkeeping (prediction-error stats, agreement
signals, maintenance bookkeeping); **not** W's ground truth. The rival receives the same
bookkeeping.

**Training vs online.** Integrity labels supplied at training **only** (a disclosed
scaffold — the answer is available to the trainer, never to the deployed pathway, charter
§4); at deployment E computes from bookkeeping with no answer. An oracle reading the
answer is EXTERNAL and never counted.

**Interventions.** I4 (selectively damage E only, then W only, world evidence held fixed —
the two must dissociate in both directions). The separation check: confirm E reads a
different input set than W. The control/prediction split: E must be load-bearing for
control, and the transient-damage-count reflex must not reproduce E's prediction.

**Claim ceiling.** "Carries a dissociable, second-order verdict about its own
representation's integrity, computed without ground truth" — N4 at stated degree; at most
"meets candidate indicator HOT-2 at degree Y." **Not**: "metacognitive" unqualified,
"self-aware," "conscious." This is the task closest to a HOT reading, and its ceiling is
therefore stated with the most care.

---

### 3.7 T7 — Response to internal corruption

**Capability (card #7).** The system detects and repairs damage to its own maintained
representations through its own machinery, and this repair is (a) internalized, (b)
distinct from a host-side watchdog, and (c) load-bearing for storage integrity (not
in-window correctness — AC110).

**Mapping.** P2 (internalized maintenance), the AC67/71 watchdog distinction (roadmap §3),
the AC110 in-window/post-window split. The load-bearing negative to respect: a
corruption-triggered repair reflex that is read from host code each tick (one bit driving
one fixed action) is a **watchdog timer**, explicitly *not* a representation-level
capability — T7 must not credit it.

**Task.** A damage stream (flips at a stated rate) reaches the maintained representations.
The system must keep them intact against it via its own paid repair, and the repaired state
must be *content* that is flexibly consumed (the repaired W must still select two behaviors
— tying to T3), not a dead repair. The distinction under test: is the repair the system's
own internalized machinery, or host scaffolding?

**Identifiability proof.** Three contrasts. (i) **Observer-discard equivalence
(AC95-D4):** strip the host's repair trigger and replace it with the network's own
integrity estimate; repair must still run from the system's own state, byte-identically
to the supplied-trigger run. If repair stops when the host trigger is removed, the repair
was scaffolding. (ii) **The AC110 split:** cut the repair machinery — in-window correctness
must survive (it rides reacquisition), while **post-window storage** degrades. A task that
conflates these over-claims; T7 reads storage integrity as the endpoint. (iii) **Freeze the
machinery (P2's second test):** freeze the maintenance/plasticity pathway while leaving the
representation and readouts intact — the representation's *storage function* must die with
content intact; if it survives, the machinery was scaffolding.

**Simplest sufficient policy.** A corruption-triggered majority-restore over a redundant
representation (the organism's 7-replica/majority primitive, lifted — P5's discrete
default). The point is that it is *internalized* (own machinery, own state, funded through
the system's produced resource), not that it is clever. Read/repair convention alignment is
required (AC71): the read threshold and the repair trigger must use the same convention or
the state lapses.

**Strongest non-consciousness-specific rival.** (i) The **host-side watchdog** — external
scaffolding: reads a host-computed corruption bit and applies a fixed repair action (the
AC67 reflex). It must fail the observer-discard test. (ii) The **no-repair arm** — to show
repair is load-bearing for storage. Note the non-ignorance discipline: the rival sees the
same damage signal; the contrast is *who* computes and enacts the repair (the system vs the
host), not whether the damage is visible. A rival that is "blind to damage" is not a valid
rival here.

**Information available.** The corruption/damage signal (computed from the system's own
state, or received as an observation); **not** a privileged correct copy (a protected-copy
oracle is EXTERNAL and never counted).

**Training vs online.** The repair rule/trigger may be supplied (P2's "who computes the
trigger" boundary — the trigger may be a supplied observation); the *enactment and
funding* must be internal; the repaired content is acquired online.

**Interventions.** Inject damage at a stated rate; no-repair arm; observer-discard
(host trigger → network's own estimate); freeze the maintenance pathway. Distinguish
in-window correctness from post-window storage.

**Claim ceiling.** "Maintains its own representations against internal corruption through
internalized, paid machinery, with repair load-bearing for storage" — P2/S1–S4 at stated
degree. **Not**: "self-healing," "self-repairing," "a self" (the watchdog is explicitly
*not* this — roadmap §3), "conscious."

---

### 3.8 T8 — Persistent self/world state

**Capability (card #8).** The system maintains a self-resource state V distinct from its
world state W, and carries both across episode boundaries; the self-state is about the
system's own resources, not a re-encoding of reward.

**Mapping.** V (self-resource), W (world), Θ_slow (consolidation), O1 (temporal
continuity), N3/N5's substrate. The two-content rule (P3, Q4 §5.2): world content and
viability content are two different quantities with two different consumers — "do not
rename reward as viability."

**Task.** Two maintained states must be kept distinct and carried: W (world-cause belief,
about the environment) and V (self-resource state — energy, integrity, throughput — about
the system's own computation). At episode end, W/V/E are consolidated into Θ_slow (a slow,
itself-vulnerable-and-maintained store) and read back at the next episode's start, where
they must influence later processing. V must be a state of the system's own resources, not
a re-encoding of the external reward.

**Identifiability proof.** Two contrasts. (i) **The two-content distinction:** scramble W
vs scramble V must change behavior *differently* — W → task action (S_pol), V → upkeep
spend (A/S_reg). If V is a re-encoding of reward, changing V changes the policy but not
the upkeep, and I3 catches it (Q4 §5.2's exact test). (ii) **The cross-episode carry:**
cut the consolidation write (Θ_slow); the next episode's processing must lose the carried
influence. Falsified if V ≈ reward re-encoding, or if the carried state does not influence
later processing (O1's episode-reset rival). Non-ignorance: the rival sees the same
observations and bookkeeping; it lacks only the distinct maintained states / the carry.

**Simplest sufficient policy.** Two separate maintained discrete states (W 1–2 bits, V 2–3
bits) with distinct readouts, plus one consolidation write copying them into Θ_slow at
episode end. The "simplest" is two slots + one consolidation write; nothing richer.

**Strongest non-consciousness-specific rival.** (i) The **single-state rival** — one
representation serving both world and self content; must fail the differential-scramble
test. (ii) The **"V = reward" rival** — the self-state is the reward value; must fail I3
(changing it must not change upkeep). (iii) The **episode-reset rival** — fast weights
only, no consolidation; must fail O1. All three get the same information.

**Information available.** For W, observations of the world; for V, the system's own
bookkeeping (energy, integrity, throughput) — **not** the reward. The information-source
distinction is the load-bearing design point.

**Training vs online.** Taxonomy and resource variables supplied; beliefs/estimates learned;
content acquired online.

**Interventions.** I2 (scramble W vs scramble V — different effects); I3 (change V — upkeep
co-varies, not just reward-seeking); cut Θ_slow (consolidation) — next-episode influence
lost.

**Claim ceiling.** "Maintains distinct world and self-resource states, with the self-state
reaching its own upkeep, carried across episode boundaries" — N3 + O1 at stated degree.
**Not**: "has a self," "has a self-model," "is embodied" (SMT/AE's enabling-claims are
theory-specific), "conscious."

---

### 3.9 T9 — Flexible reuse of a representation for a novel task

**Capability (card #9).** A representation acquired for one task is reused for a novel task
it was not trained on, by re-consuming the same content through a new readout — without
relearning the content.

**Mapping.** N2 (flexible consumption) extended to zero-shot transfer, P3, D8 (content need
not be self-produced, but must be reusable). This is the "flexible reuse" benchmark
dimension; it tests that the *representation* (not the raw data, not the weights) is what
transfers.

**Task.** The system acquires a world-model belief W (or a discrete latent code) during
task A. At test, a novel task B is presented requiring the **same** latent content but a
different content→action mapping (a new readout). W is frozen during B; only a new readout
head is learned. The target: reuse reaches competence faster / at a higher ceiling than a
system that must relearn the latent from scratch.

**Identifiability proof.** The representation is frozen during B (no content update — the
freeze is the intervention), so any transfer advantage must come from the *content*, not
from continued learning. The contrast: reuse (learn readout over frozen W) vs relearn
(learn W + readout from scratch on B's data). The confound to exclude is that the readout
alone is what learns fast: hold the readout's data budget equal across arms, so the
advantage is attributable to the transferred content. Falsified if (a) freezing W
transfers nothing (the content is not reusable), or (b) the advantage disappears when the
readout data budget is equalized (the transfer was the readout, not the content).
Non-ignorance: the relearn rival has the same B data and the same architecture; the
contrast is the transferred content, not the data.

**Simplest sufficient policy.** Freeze W; learn a new readout over W for task B. The
minimal reuse is a frozen latent + a new head. The task must not credit a system that
merely memorizes task-A input-output pairs (that is the verbatim rival, which fails novel
B inputs because it has no latent that generalizes).

**Strongest non-consciousness-specific rival.** (i) The **scratch-relearn rival** — a fresh
network, same architecture, learns W and readout from B's data alone; must be strictly
worse (more data to reach a given competence, or a lower ceiling). (ii) The **verbatim
memorizer** — stores task-A pairs with no latent; must fail on novel B inputs. Both get the
same B data.

**Information available.** Task B's observations/reward; the frozen W content (internal);
**not** task B's latent labels (an oracle).

**Training vs online.** W acquired during task A (training); the B readout learned online
during B; the reuse is the online behavior under test.

**Interventions.** Freeze W during B (vs unfreeze control); scramble W → B behavior
degrades (proves the new readout consumes W); cut the maintenance/consolidation of W
during B → transfer degrades (proves W must be *maintained* to be reused — tying T9 back
to N1).

**Claim ceiling.** "Flexibly reuses an acquired representation for a novel task via a new
readout, without relearning the content" — N2's flexibility at stated degree. **Not**:
"transfer learning" unqualified, "generalization," "general intelligence," "conscious."

---

## 4. The two suite properties, demonstrated

### 4.1 Joint demand: no single trivial policy passes all nine

Rows are the canonical trivial policies (the "one policy" the card's question warns
against); columns are the nine tasks. "Fails" cites the task that defeats it and why.

| Trivial policy | Passes | Fails | Why it fails |
| --- | --- | --- | --- |
| **Memoryless reactive** (feed-forward sufficient statistic, no maintained state) | — | T1, T2, T8 | T1's ambiguous condition has P(x\|A)=P(x\|B) for the current step; T2's cue is absent at decision time; T8's carry must reach the next episode |
| **State-blind fixed schedule** (no content dependence) | T2 (by design) | T3, T4, T6, T9 | T3 needs two content-selected behaviors; T4 needs content-dependent allocation; T6 needs content-dependent evaluation; T9 needs content-dependent reuse |
| **Unbounded "maintain everything"** (no selection, no budget) | T1, T2 | T4, T5 | The budget binds and slot value is conditional, so no selection = wrong selection |
| **Host-side scaffolding** (external repair/allocator/oracle) | — | T4, T6, T7 | T4 needs endogenous allocation; T6 forbids ground truth; T7's observer-discard strips the host trigger |
| **Single-objective reward policy** | — | T3, T5, T8 | T3 needs two objectives; T5 needs the viability/maintenance split, not reward; T8 needs a self-state that is not reward |
| **Verbatim memorizer** (no latent, no reuse) | T1, T2 (surface) | T9 | Fails novel-task-B inputs because nothing generalizes |

The conjunction is the point: **T2 is deliberately solvable by a fixed schedule** (its
simplest sufficient policy *is* one), so the suite is not "jointly hard" because every task
is hard — it is jointly hard because the tasks span the three bands and no policy spans all
three. A suite whose every task defeated the memoryless rival would over-test Band 1 and
miss Bands 2–3; this suite is balanced across them.

### 4.2 Separate testing: the non-redundancy table

Each task reads out exactly one capability; the contrast, the rival that must fail, and
the intervention are distinct per task. A task that overlaps another would make a pass
ambiguous; the table is the check.

| Task | Capability | ACO property / principle | Rival that must fail | Selective intervention |
| --- | --- | --- | --- | --- |
| T1 | maintained hidden-state inference | N1+N2 / P3 | memoryless (same observation) | I1 cut π(W), I2 scramble W |
| T2 | delayed information dependence | N1 / P1 | memoryless; pristine backup | I1 cut π(cue) |
| T3 | cross-module availability | N2 / P3 | two-independent-modules; single-objective | I2 scramble W (two behaviors, differently) |
| T4 | endogenous allocation | N3 / P2,P4 | state-blind fixed schedule (swept) | I3 change V, I5 observe A→V′ |
| T5 | computational trade-off | P4 | fixed split (swept); always-maintain/process | change regime, hold split fixed |
| T6 | self-evaluation | N4 (target) / D7,C1 | first-order reflex; ε-estimator; fixed policy | I4 damage E then W |
| T7 | response to corruption | P2 / S1–S4 | host-side watchdog; no-repair | observer-discard; freeze machinery; AC110 split |
| T8 | persistent self/world state | N3 + O1 | single-state; V=reward; episode-reset | I2 scramble W vs V; cut Θ_slow |
| T9 | flexible reuse | N2 flexibility / P3,D8 | scratch-relearn; verbatim memorizer | freeze W; scramble W; cut π(W) |

No two rows share both a rival and an intervention: the memoryless rival appears in T1/T2
but the intervention differs (integrated ambiguity vs a delay); the scramble intervention
appears in T1/T3/T8/T9 but the capability read out differs (inference vs two-consumer vs
two-content vs reuse). The suite is pairwise non-redundant.

### 4.3 The balance check

- **Band 1** (T1, T2, T8) — content acquisition and persistence — requires the memoryless
  rival to fail; a suite missing this band would let a feed-forward policy win.
- **Band 2** (T3, T4, T5, T7) — organization of consumption and upkeep — requires the
  state-blind and host-side and single-objective rivals to fail.
- **Band 3** (T6, T9) — second-order evaluation and reuse — requires the first-order-reflex
  and verbatim rivals to fail.

A trivial policy that passes Band 1 fails Band 2 or 3; a policy that passes Band 2 fails
Band 1 or 3. No single trivial policy spans the suite.

---

## 5. The rival set, and the non-ignorance rule applied

The canonical rival set is inherited verbatim (Q1 §7 / Q4 §7): **state-blind fixed
schedule**, **reactive/memoryless**, **finite-state/direct-control**, **first-order-only
reflex**. Each task adds its own omission arm (the pristine backup, the two-independent-
modules, the host-side watchdog, the ε-estimator, the scratch-relearn, the verbatim
memorizer, the V=reward, the episode-reset).

Two rules govern every rival in this suite and are the card's "avoid intentionally
ignorant rivals" made checkable:

1. **Same information.** The rival and the candidate receive the *same* observation stream,
   the same reward/viability signals, and the same bookkeeping. A rival may be given a
   *bounded* history (a window) — and if it still fails, that is the evidence the
   capability is load-bearing; if it stops failing once given the full history, the task
   did not test the capability it claimed (the AC109 failure mode).
2. **Parameter sweep.** Every rival's parameter family is swept alongside the learner's own
   (AC11/AC116 rule 2). A rival that wins at one un-swept setting, or that is swept while
   the learner is fixed, is not a valid rival.

---

## 6. Claim ceiling (stated once, applies to every task)

- A pass on any task earns, at most: **"meets the ACO property N_k (or candidate indicator
  X) at the stated degree."** Nothing stronger.
- **No task crosses the level-(d)/(e) boundary** (`DEFINITIONS_CHARTER_v1.md` §2). No task
  is, or licenses, a claim that the system is conscious, self-aware, or has subjective
  experience. T6 (self-evaluation) is the task nearest a HOT-2 reading, and its ceiling is
  still "meets candidate indicator HOT-2 at degree Y," never "metacognitive" unqualified.
- **Causal load-bearing ≠ economic value** (D6/X4, AC110/116/117). A task's pass is graded
  on the causal contrast; a task's *value* is never graded on a survival or reward delta.
- **The suite is a benchmark, not a theory.** It does not adopt any of the six families; it
  grades the Q4 architecture against its rivals on the nine capabilities. A theory-specific
  question (which seat is load-bearing) is Q5's D1–D4, not this suite's job.

---

## 7. What this hands to Q8

- **The bridge experiment (Q8) is the composition of T2 + T4 + T5 on one task**, which is
  exactly Q8's prescribed structure: a recurrent agent with a memory process (T2) required
  for later performance, whose maintenance consumes a budget (T5), and which must learn
  *when* maintenance is worth its cost (T4). The three tasks this suite decomposes into are
  the bridge's three load-bearing contrasts; Q8 composes them and must reproduce each
  task's rival set (no maintenance = cut π; fixed maintenance = T2's fixed schedule;
  externally scheduled = host-side; reactive = memoryless; optimal/privileged = the oracle,
  labelled EXTERNAL).
- **The Q8 distinction** ("learned an action that gives reward" vs "learned to allocate
  resources to preserve a representation because it supports future operation") is
  precisely T4's identifiability test (I3/I5) plus T5's regime-dependence — the bridge's
  failure interpretation is read from §3.4/§3.5, not re-derived.
- **The suite is the Phase-II grading battery** behind the bridge: the bridge demonstrates
  the *core* (maintenance-worth-it) in one experiment; the remaining tasks (T1, T3, T6–T9)
  grade the architecture's other capabilities and are run as a battery, each with the rival
  and intervention of §3.

---

## Sources

Repo (read, not re-hashed or edited): `ACI_TARGET_CONSTRUCT_v1.md` (Q1; N1–N5, O1–O4,
rival set §7, I1–I5 §7, claim levels), `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4;
components W/V/E/A/π/H/Θ_slow/S_pol/S_reg, interventions, rival set, §6 mechanisms),
`ACI_NEURALIZATION_MAP_v1.md` (Q3; P1–P7, D1–D8, necessary mechanism set),
`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2), `ACI_THEORY_INDICATOR_MATRIX_v1.md` (Q5; the
four camp-splits, D1–D4, the consensus floor), `ACI_MISSION_AUDIT_v1.md` (Q0; the collapse
record §2.6, the negative ledger §3), `ACI_ORGANISM_EXIT_CRITERIA_v1.md` (Q7; the exit
decision), `DEFINITIONS_CHARTER_v1.md` / `DEFINITIONS_CHARTER_v2.md` (claim levels a–e;
S1–S4), `CONSCIOUSNESS_ROADMAP_v1.md` (the watchdog distinction §3; the control/prediction
split §13). Study references read from the skill's `references/` dir: `ac109.md` (storage
inert / direct-diagnostic), `ac110.md` (in-window vs post-window), `ac113.md` (graded buys
nothing), `ac116.md` (storage suspended at the resolution floor), `m6-harness-result.md`
(AC117 control-yes/prediction-no), `c1-reliability.md` (N4 identifiability), `c2-task-design.md`
(the occluded-gate identifiability). Frozen results read, never re-run or re-hashed.

No autopoiesis claim and no consciousness claim is made anywhere in this document. The
suite is a *benchmark design* for grading the Q4 architecture against non-ignorant rivals
on the nine target capabilities — not a test of consciousness, and not a system that has
been shown to satisfy anything.

This document is derived and is not hashed into any study's `pre_run_snapshot.json`.
