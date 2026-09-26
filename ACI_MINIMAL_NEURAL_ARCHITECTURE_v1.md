# ACI minimal neural architecture v1 — the smallest architecture that can test the central ACI hypothesis

2026-09-25. Deliverable for the Q4 card (t_e1121928): *what is the smallest neural
architecture capable of testing the central ACI hypothesis?* Category B/C — **design
only, do not build.**

This is a **design document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It specifies one object — the minimum
neural architecture — precisely enough that Q5 (indicator matrix), Q6/Q7 (downstream),
and Q8 (bridge experiment) can each read their vocabulary from here instead of
re-deriving it.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is, or is meant as, a consciousness claim;
the strongest wording a *built* realization of this architecture earns is "meets the ACO
definition (N1–N5, at the stated degree)." (2) The architecture is **neutral** across the
six theory families (`ACI_TARGET_CONSTRUCT_v1.md` §10); it is defined by N1–N5, not by any
one theory, and no component adopts a theory-specific loading (F5). (3) The three Q3
"do not assume" clauses are enforced in every component: biological realism is not
required; Transformers/attention are not the default substrate (attention appears only as
the Q5-tested candidate for the *optional* workspace property O3, and nowhere else); no
novel architecture is assumed where an existing primitive suffices. (4) Every component is
justified by which N-property (or O-property the card requires) it serves and which
intervention (I1–I5) tests it; no component is added "for richness" (X3/X4/D2). (5) The
demoted principles D1–D8 (`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` §4) are the negative
constraints this architecture must not violate; they are listed in §8 and are as load-
bearing as the components themselves.

---

## 0. The one-paragraph answer

The smallest architecture that can test the central ACI hypothesis — *recurrent cognitive
organization of the form N1–N5 is what a neural architecture must realize before a
theory-specific consciousness-relevant question is well-posed* — is a **single recurrent
network with three maintained discrete state slots (a world-cause belief, a self-resource
state, and a self-evaluation state) held in a limited recurrent workspace under an
explicit per-step energy budget, two specialist readouts with different objectives, one
learned maintenance controller whose own state lives in the loop it maintains, one paid
refresh process, and one slow consolidation store for cross-episode carry**. Every
primitive it uses is existing and mature — a gated recurrent cell, a discrete latent
bottleneck, a mixture-of-experts router, fast/slow-weight pairs, a learned internal error
head, and a compute/energy budget. The novelty is **organizational** (N5's closure, the
representation→maintainer→representation cycle), not architectural; this is exactly
`ACI_NEURALIZATION_MAP_v1.md` §5's headline, made concrete. The eight components the card
names map onto the ACO properties as *candidate realizations* (not as the definition):
world model and specialists realize N2's flexible consumption; the workspace and the paid
refresh realize N1's active persistence; the self-resource model and the maintenance
controller realize N3's endogenous regulation and N5's closure; the self-evaluative
pathway realizes N4 (as a target); the consolidation store realizes O1 (temporal
continuity, which the card requires and Q1 grades as optional). Removing any one component
removes at least one N-property's testability, which is what makes this the minimum.

---

## 1. What "minimum" means here, and the two minimality tests

An architecture is **minimum** for the central hypothesis iff two tests both pass:

1. **Coverage.** Every component serves at least one N-property (or the one card-required
   O-property, O1), and every N-property is served by at least one component. A component
   that serves nothing is deleted; a property with no component is a gap. The coverage
   table is §9.
2. **Necessity.** For every component, the rival that omits it (its "no-<component>" arm)
   provably fails to realize the served property. This is P6 in its strongest form: a
   component earns its place only if the architecture without it cannot pass the property's
   minimal test (§3 of `ACI_TARGET_CONSTRUCT_v1.md`). The rival column of every component
   in §5 states which omission-arm must fail.

"Smallest" is therefore a **claim about the wiring**, not about model size: the
architecture may be realized at a few thousand parameters, but the minimality claim is
"no component can be removed without losing a testable N-property," not "this is the
smallest network that can be made to run." That second reading is an engineering fact,
not a design claim, and is out of scope for this card.

Two standing rules from the program carry into the design and are stated once here rather
than repeated per component:

- **The reference copy lives in the vulnerable, paid-maintained substrate.** No hidden
  pristine weight matrix that the decay/damage stream never reaches and no process
  refreshes (P1/P2; the program's `pristine backup` rival). Every maintained state below
  — W, V, E, and the maintenance controller's own working state — is damageable and
  paid-maintained, or it is a hidden backup and the component is not realized.
- **Discrete is the default.** Every state is discrete/sparse unless a graded form is
  shown to buy a distinct causal capability (P5/D1). No graded confidence, no continuous
  posterior, is assumed anywhere; where a small discrete code (2–3 bits) suffices it is
  what is specified. The self-evaluative pathway is binary or a small counter, not a
  graded confidence (D4/D7).

---

## 2. The probe task (the smallest environment that makes all eight components testable)

The world model needs "external causes" and the specialists need "different behaviour,"
so the architecture is stated against a minimal task. The task is the *smallest* one that
exercises all eight components, and it mirrors the organism program's own content
(contact/channel economy, two-cause attribution, relinquish-vs-maintain) translated to a
neural substrate — function, not realization (`ACI_NEURALIZATION_MAP_v1.md` §1 rule 1).

**T_min — two-cause discrimination under a resource bound.**

- **Episode.** Discrete time t = 0…T. An episode draws a latent external cause
  c ∈ {A, B} (e.g. "regime A / regime B") with fixed prior, supplied by the environment.
  The taxonomy {A, B} is the task's given structure (supplied content — D8: content need
  not be self-invented); *which* cause is active is inferred within life (learned).
- **Observations.** Each step the system receives x_t whose statistics depend on c (the
  same x can arise under both causes with different probabilities, so single-step
  discrimination is not always possible — the world-model belief is a *latent* inference
  over the history, not a readout of x_t). The system also reads its own internal state
  (energy remaining, workspace integrity bookkeeping, prediction-error statistics).
- **Actions.** The policy specialist emits an external action a_t (a contact against one
  of two channels); the correct channel depends on c, so a correct cause belief changes
  which action is rewarded. A correct contact yields **energy** (the resource); the
  **task reward** r_t is the external score on the contact.
- **Resource.** The system holds an energy budget that depletes with every computational
  operation (refresh, consolidation, processing). "Continued cognitive operation" =
  energy above a floor ∧ workspace representations intact through episode end. This is
  the *viability* content (§5.2), and it is **not** the task reward: energy is a
  substrate resource the system spends on its own computation; reward is the external
  score on the contact. The instruction "do not rename reward as viability" is met by
  making them two different quantities with two different consumers (§5.2, §5.3).
- **Two behaviours from one belief.** The same world-model value ĉ drives (i) the
  policy's channel choice (task behaviour) and (ii) the regulation specialist's
  relinquish-vs-maintain decision (upkeep behaviour): if ĉ says "the world changed, my
  belief is stale" the system relinquishes and re-acquires; if ĉ says "my access
  machinery is degraded but the belief is right" it spends on repair/maintenance instead.
  This is the organism's AC107/108 two-way consumption, and it is what makes N2 testable
  (§5.1, §5.3).

The task is declared minimal: it has exactly two causes (the smallest content that makes
a *belief* differ from a *readout*), two channels (the smallest action space that makes a
correct-vs-wrong belief behaviourally distinct), and one resource (the smallest economy
that makes maintenance a real cost). Nothing richer is added because nothing richer is
needed to test N1–N5 (D2).

---

## 3. Architecture overview

### 3.1 The one-line wiring

```
                    ┌────────────────────────────────────────────┐
   environment      │             energy budget B_t (shared)      │
   observations x_t │                                            │
        │           │   ┌───────────────┐                        │
        ▼           │   │  WORKSPACE H  │  k=3 maintained slots  │
  ┌───────────┐     │   │  W  V  E      │  (recurrence + refresh)│
  │ WORLD     │─────┼──▶│  (discrete)   │◀──────── refresh ───────┤
  │ MODEL     │ W   │   └───────┬───────┘                        │
  │ (belief   │     │           │ (content broadcast to          │
  │  update)  │     │           │  the specialists)              │
  └───────────┘     │   ┌───────┴───────────────┐                │
        ▲           │   │                       │                │
        │           │   ▼                       ▼                │
        │           │ ┌─────────────┐   ┌─────────────────────┐  │
        │           │ │ POLICY      │   │ REGULATION          │  │
        │           │ │ specialist  │   │ specialist          │  │
        │           │ │ S_pol: a_t  │   │ S_reg: relinquish/  │  │
        │           │ │ (task act)  │   │  maintain + alloc.  │  │
        │           │ └─────────────┘   └──────────┬──────────┘  │
        │           │                              │             │
        │           │   ┌──────────────────────────▼──────────┐  │
        │           │   │ MAINTENANCE CONTROLLER A (allocator)│  │
        │           │   │   its own state in the maintained    │  │
        │           │   │   loop; decides budget split +       │  │
        │           │   │   which slots to refresh             │  │
        │           │   └──────────┬───────────────────────────┘  │
        │           │              │  E_π(t) = Σ refresh_i c_i     │
        │           │   ┌──────────▼───────────────────────────┐  │
        │           │   │ ACTIVE MEMORY MAINTENANCE π (paid    │  │
        │           │   │   refresh writes)                    │  │
        │           │   └──────────────────────────────────────┘  │
        │           │         │ (sustains W,V,E against decay)     │
        │           │         ▼                                   │
        │           │   ┌──────────────────────────────────────┐  │
        │           │   │ SELF-EVALUATIVE PATHWAY E (verdict    │  │
        │           │   │   about W's integrity, no ground      │  │
        │           │   │   truth; feeds A)                    │  │
        │           │   └──────────────────────────────────────┘  │
        │           └────────────────────────────────────────────┘
        │
   ┌────▼─────────────────────────────────────────────────────┐
   │ TEMPORAL CONTINUITY: slow store Θ_slow (consolidation     │
   │   write of W,V,E across episode boundaries)               │
   └──────────────────────────────────────────────────────────┘
```

The **N5 closure cycle** is the loop V → A → π → V: the self-resource state V changes the
maintenance controller A's allocation, which changes which workspace slots are refreshed
and with what budget, which changes V's own future availability and value. The **N4**
pathway is E: it reads the system's own bookkeeping (not W's ground truth) and emits a
verdict about W's integrity that is dissociable from W, feeding A. Both edges are drawn
so they can be cut by a single selective intervention (§7).

### 3.2 Why this is the whole architecture

| Component (§5) | Symbol | ACO property served | Principle | One-line role |
| --- | --- | --- | --- | --- |
| World model | W | N2 (content), N3 (reach) | P3 | latent belief about the external cause |
| Self-resource model | V | N3, N5 | P4 | state of the system's own resources |
| Specialist modules | S_pol, S_reg | N2 | P3 | two consumers needing different information |
| Limited recurrent workspace | H | N1, N2 (substrate) | P1, P3 | the k maintained slots + recurrence |
| Active memory maintenance | π | N1 | P1 | the paid refresh that sustains the slots |
| Maintenance controller | A | N3, N5 | P2, P4 | the learned allocator, in the maintained loop |
| Self-evaluative pathway | E | N4 (target) | P6, D4/D7 | evidence about W's integrity, no ground truth |
| Temporal continuity | Θ_slow | O1 (card-required) | P1, P2 | cross-episode carry via consolidation |

---

## 4. Shared substrate (supplied, fixed — the neural analogue of the charter's §5)

These are the *laws* of the architecture, supplied by the trainer/host and not produced,
repaired, or replaced by the system. They are the neural form of the organism's format-
level substrate (`DEFINITIONS_CHARTER_v1.md` §5), and they are the boundary at which
"self-maintenance" bottoms out (the infinite-regress argument: a mechanism that rewrote
its own transition law would need a second-order law). They are declared here so that
"supplied vs learned" in §5 is unambiguous.

| Substrate item | What it is | Analogue of |
| --- | --- | --- |
| Recurrence law | the workspace update map (a gated recurrent cell or fixed-rate attractor), incl. its leak/decay rate δ | the organism's tick clock + memory `life` decay |
| Energy budget B_t | per-step energy available, split between processing and maintenance | the material/energy economy + write cap |
| Write primitive | a paid refresh: 1 write = 1 energy unit (or c_i per slot), bounded by the budget | the paid write (1 energy + 1 material per replica) |
| Discrete code format | the encoding of W, V, E (2–3 bit codes, sparse/localist) | the 14-bit word / 7-replica majority format |
| Damage/decay stream | the decay of unrenewed slots (and, optionally, an injected flip stream at a stated rate) | the sticky-SET damage stream |
| Task constants | cause prior, channel yields, episode length T, budget size | PORTS, YIELD, TICKS, thresholds |
| Training scaffold | the objective functions and the training labels (incl. the integrity labels E is trained against) | the inherited priority content |

**The two rules that make this the same discipline as the organism**, not a looser one:

1. **The reference copy is in the vulnerable substrate.** W, V, E, and A's own working
   state all live in the workspace (or in the slow store Θ_slow, which is *also*
   vulnerable and paid-maintained — §5.8). There is no weight matrix that holds a
   pristine copy of W that the decay stream never reaches and no process refreshes. If a
   copy is needed (e.g. a backup for the self-evaluative pathway's integrity check), it
   is itself damageable and maintained, or the design is rejected as a hidden backup.
2. **Correctness rides the acquisition/update write, not continuous repair (D3).** The
   world model's *accuracy* is carried by the belief-update write (re-inference on open
   evidence), not by the refresh process. The refresh process protects *storage* (post-
   window persistence), not in-window correctness. This is AC110, stated as an
   architectural invariant: the maintenance loop is not the correctness mechanism, and
   the design must not smuggle that assumption back.

---

## 5. The eight components

Each component is specified with the nine fields the card requires. Symbols match §3.2.

---

### 5.1 World model (W) — latent belief about the external cause

- **Inputs.** The observation history x_1…x_t (and, optionally, the system's own last
  action and its outcome — the organism's `bound`/`productive` analogues). Crucially, its
  input is **not** the externally correct cause c; the system receives observations, not
  the answer (the roadmap's §4 rule).
- **Outputs.** A discrete belief ĉ ∈ {A, B} (a 1–2 bit code), held in the workspace slot
  W. It is the *content* the specialists consume (P3's latent).
- **Recurrence.** The belief is a *latent* state updated over the history, not a per-step
  readout: W_t = update(W_{t-1}, x_t, a_{t-1}, outcome). The update is recurrent (it
  integrates evidence), which is what makes a stale W differ from a fresh readout and is
  the substrate of N1/N2.
- **Learning rule.** Trained to infer c by a predictive objective — e.g. a variational/
  ELBO bound over the latent cause, or a supervised cross-entropy against the cause label
  c during training (a disclosed scaffold). The *acquisition/update* write (re-inference
  on open evidence) is what carries correctness (D3); D4 does **not** apply here — D4 is
  about the *monitor*, not the model, and W's worth is its causal role as a selector
  (N2/N3), not its predictive accuracy.
- **Resource cost.** Its update is a processing cost against B_t; its *persistence*
  between updates is paid by the refresh process π (§5.5). So W costs twice: to update and
  to hold.
- **Failure mode.** W decays to an uninformative/neutral value when its refresh is cut
  (N1's decay time-course); W goes stale when the cause changes and the update write is
  not made (correctness rides reacquisition — D3). The two are distinct failures and are
  measured separately.
- **Relevant rival.** (i) The *pristine backup* — a second copy of W in state the decay
  stream never reaches and no process maintains (N1's rival); (ii) the *memoryless/
  sufficient-statistic rival* — a readout of the current observation only, no maintained
  belief (the direct-diagnostic rival, AC109). Both must fail: the backup must show the
  same decay when its (absent) maintenance is cut, and the memoryless rival must fail to
  reproduce the two-way consumption.
- **Intervention.** I2 (N2): scramble/retain W only, holding sensors, readouts, and all
  else fixed; ≥2 behaviours must co-vary. I1 (N1): cut π's refresh of slot W (not W, not
  the sensor); W must decay and behaviour track it.
- **Supplied or learned.** **Taxonomy supplied, belief learned.** The cause set {A, B} is
  the task's given structure (inherited content, permitted — D8); *which* cause is active
  is inferred within life. This is exactly the organism's split: inherited instructions,
  acquired content.

---

### 5.2 Self-resource model (V) — state of the system's own resources (the "viability" state)

- **Inputs.** The system's own bookkeeping: energy remaining (directly measurable),
  workspace-integrity statistics (how many slots are still intact, read from the
  maintenance bookkeeping), and throughput (operations completed per energy). These are
  *internal* variables — the state of the system's own computation. **Not** the external
  reward.
- **Outputs.** A small discrete state v̂ (e.g. a 2–3 bit code over {energy-low/ok,
  integrity-degraded/ok, throughput-slow/ok}, or a small counter), held in workspace slot
  V.
- **Recurrence.** V integrates its own history (it is a state, not a per-step readout of
  the energy gauge): V_t = update(V_{t-1}, bookkeeping_t). Its persistence between
  updates is paid (§5.5).
- **Learning rule.** Trained to *estimate* the system's own resource/integrity state from
  the bookkeeping; the estimation objective is a regression/classification against the
  *measured* internal resource state (which is substrate bookkeeping, not external ground
  truth about the world). The key discipline is downstream, not here: V's *causal role*
  is to reach the maintainer (N3), and its worth is graded on that causal contrast, never
  on the task-reward delta (D6).
- **Resource cost.** Its update is a processing cost; its persistence is paid via π. Its
  *effect* is to move maintenance spend, which is the N3 endpoint measured.
- **Failure mode.** If V is cut from the maintainer, upkeep spend runs on a fixed schedule
  (N3 falsified); if V is a re-encoding of the reward, changing V changes the policy but
  not the upkeep — the "renamed reward" failure the card forbids, and the exact test that
  catches it (I3).
- **Relevant rival.** The *state-blind fixed schedule* — a maintenance/allocation policy
  with no dependence on V's content (AC11's rival). It must fail: changing V's content
  must change upkeep spend in a direction V determines, which a fixed schedule cannot
  reproduce.
- **Intervention.** I3 (N3): change V's content only; upkeep spend must co-vary. The
  companion check (AC113, run *before* claiming any trade-off): measure the per-action
  economics in the actual energy budget — verify a false relinquish actually costs and
  holding actually pays — or the allocation controller is built on a model with the wrong
  trade-off direction.
- **Supplied or learned.** **Variables supplied (substrate), estimates learned.** The
  resource variables (energy, integrity, throughput) are defined by the substrate
  (§4); the *estimation* of them into a maintained state is learned. Energy-remaining is
  near-directly readable; integrity is a learned estimate from the maintenance
  bookkeeping. Neither is reward, and the design is explicit that they are two different
  quantities with two different consumers (S_pol reads W for reward; A reads V for
  upkeep).

---

### 5.3 Specialist modules (S_pol, S_reg) — at least two processes needing different information

Two specialists are specified; two is the minimum N2 requires ("at least two"). Both
consume the *same* world-model content W and drive *different* behaviour, which is what
makes N2's "same value, two distinct outcomes" testable.

**S_pol — policy specialist (task behaviour).**

- **Inputs.** The world-model content W (which cause) plus the current observation x_t.
- **Outputs.** The external action a_t (channel choice).
- **Recurrence.** Feed-forward given W and x_t (no recurrence of its own; its memory is
  the shared W).
- **Learning rule.** Trained to maximize task reward (RL or supervised on the correct
  channel given c).
- **Resource cost.** Processing cost against B_t (the `E_proc` term).
- **Failure mode.** Scrambling W changes a_t — if it does not, S_pol is not consuming W
  and the "content selector" role is absent.
- **Relevant rival.** The *finite-state / direct-control rival* — a hardwired channel
  choice with no maintained cause belief.
- **Intervention.** I2 (N2): scramble W; a_t must change.
- **Supplied or learned.** Learned (weights); the reward objective is supplied.

**S_reg — regulation specialist (upkeep behaviour).**

- **Inputs.** The same world-model content W **plus** the self-resource state V (it needs
  *different* information than S_pol: S_pol needs W+x to act; S_reg needs W+V to decide
  how to spend on upkeep).
- **Outputs.** A relinquish-vs-maintain decision: if W says "world changed / belief
  stale" → relinquish the stale content and re-acquire; if W says "machinery degraded,
  belief right" → spend on repair/maintenance. This is the organism's two-way
  consumption lifted to neural form.
- **Recurrence.** Feed-forward given (W, V).
- **Learning rule.** Trained to maximize **continued cognitive operation** (energy above
  floor ∧ workspace intact through episode end), **not** task reward. This is what makes
  S_pol and S_reg "different": different objectives, different inputs, different outputs.
- **Resource cost.** Processing cost; its *decision* moves maintenance spend (the N3
  endpoint).
- **Failure mode.** If S_reg's relinquish-vs-maintain is indistinguishable from a fixed
  duty cycle, the "content selects upkeep" claim collapses (AC11's signature); if S_reg
  re-encodes S_pol (both just optimize reward), the two are one specialist and N2 fails.
- **Relevant rival.** The *state-blind fixed policy* (a fixed duty cycle) and the
  *content-free raw-history counter* (a running failure count with no cause attribution)
  — both must fail to reproduce the relinquish-vs-maintain behaviour.
- **Intervention.** I2 (N2): scramble W; S_reg's relinquish-vs-maintain must change
  (differently from S_pol's action). I3 (N3): change V; upkeep spend must co-vary.
- **Supplied or learned.** Learned (weights); the continued-operation objective is
  supplied (it is the *definition* of viability, §2 — a supplied objective, not a
  learned one, and disclosed as such).

**N2 is the two-specialist test.** The same R-change (scramble W) must change S_pol's
output (channel choice) and S_reg's output (relinquish-vs-maintain) *differently* — two
behaviours, two different consumers, from one content value. A rival that omits the
shared content (a direct-control mapping) or that collapses the two behaviours into one
(a single reward-maximizing policy) must fail.

---

### 5.4 Limited recurrent workspace (H) — the bottleneck where selected representations are sustained

- **Inputs.** The read-in of the three maintained states (W, V, E) and the observations
  they integrate.
- **Outputs.** The k = 3 maintained slots (W, V, E), each a discrete code, sustained by
  recurrence and available to the specialists.
- **Recurrence.** This is the architecture's recurrence substrate: each slot is a gated
  recurrent state (GRU cell or point attractor) that integrates its input and relaxes
  toward a neutral value at rate δ when not re-energized. Recurrence here is the *one*
  necessary family substrate (`ACI_NEURALIZATION_MAP_v1.md` §5: RPT's load-bearing claim,
  and N1/N2's substrate).
- **Learning rule.** The read-in/read-out weights are learned end-to-end; the recurrence
  law (decay δ) is supplied (§4). The *sustaining* of a slot is not a learned weight — it
  is a paid refresh (§5.5), which is the point of N1.
- **Resource cost.** The workspace's capacity k is the bottleneck: only k representations
  can be sustained at once, and sustaining each costs refresh energy. Capacity-k is the
  "limited" in "limited recurrent workspace."
- **Failure mode.** The workspace decays when the refresh budget is exhausted (slots drop
  to neutral); the bottleneck forces *selection* — which content is sustained is a
  decision (§5.6), not a default.
- **Relevant rival.** The *unbounded* store (no capacity limit, everything sustained) — it
  must fail to be behaviourally equivalent, or the bottleneck is doing no work; and the
  *pristine* store (sustained by weights the decay stream never reaches) — N1's rival.
- **Intervention.** I1 (N1): cut the refresh into a slot; the slot decays on the network's
  time constant. The workspace is the substrate on which every I1–I5 is applied.
- **Supplied or learned.** **Dynamics supplied (recurrence law), read-in/read-out
  learned.** The bottleneck *claim* (that this limited set, made globally available, is
  the seat of consciousness) is **not** adopted here — that is GWT's O3, optional and
  theory-specific, tested by Q5. This architecture provides the *substrate* a bottleneck
  would occupy (`ACI_NEURALIZATION_MAP_v1.md` §5 "sparse recurrent workspaces … without
  the bottleneck claim"); it makes the selected representations available to the two
  specialists (N2), which is required, but it does not assert global-broadcast-as-seat
  (F5).

---

### 5.5 Active memory maintenance (π) — the paid refresh that keeps representations alive

- **Inputs.** The refresh vector r_t ∈ {0,1}^k chosen by the maintenance controller (§5.6),
  i.e. *which* slots to re-energize this step.
- **Outputs.** The re-energized slots — the writes that keep W, V, E from decaying.
- **Recurrence.** π is not itself recurrent; it is the *process* that the recurrence
  depends on to persist. It is periodic and resource-consuming.
- **Learning rule.** **None of its own.** π performs a write; it does not learn *what* to
  write (that is A's learned policy). This split — the write is a substrate primitive,
  the *choice* is learned — is the P2 distinction between *who funds/enacts* the write
  (internal, π) and *who computes the trigger/choice* (A, possibly partly supplied).
- **Resource cost.** Each refresh of slot i costs c_i energy, drawn from the budget:
  E_π(t) = Σ_i r_t(i) · c_i, with E_π + E_proc ≤ B_t. This is the neural analogue of the
  organism's paid write under the per-action cap `min(32, 8·W)`.
- **Failure mode.** Cutting π (r ≡ 0) lets the slots decay to neutral on timescale 1/δ —
  the N1 decay time-course, set by the network dynamics, not the environment. If a slot
  survives the cut, it was in immutable storage (free permanence, N1 fails).
- **Relevant rival.** The *pristine backup* — a copy of a slot in state π never touches
  and the decay stream never reaches; it must show the same decay when its (absent)
  maintenance is cut. The *state-blind fixed schedule* (refresh on a fixed duty cycle
  regardless of content) — it must fail to track the content's maintenance needs (P2).
- **Intervention.** I1 (N1): cut π's refresh of one slot, holding its initial value, the
  sensors, and every other process fixed; measure the decay and the behavioural co-decay.
- **Supplied or learned.** **Write primitive supplied (substrate law), the refresh
  *choice* learned (via A).** The write is a law (§4); what the write is applied to is
  the learned allocation decision. This is the exact shape of the organism's S3 paid
  maintenance: enacted and funded internally, trigger/choice possibly supplied.

---

### 5.6 Maintenance controller (A) — the learned allocator, whose own state is in the maintained loop

- **Inputs.** The self-resource state V (how much resource/integrity remains), the
  regulation specialist's relinquish-vs-maintain output, and the self-evaluative verdict
  E (§5.7). I.e. it reads the representations *about the system's own condition* and
  spends accordingly.
- **Outputs.** Two decisions: (i) the budget split E_π vs E_proc (how much energy to
  maintenance vs processing), and (ii) the refresh vector r_t (which slots to sustain).
- **Recurrence.** A is a small learned recurrent/stateful policy: its *working state*
  (the allocation it is currently committed to, e.g. the streak/level of maintenance it
  is holding) is a state that persists and is updated. That working state is **in the
  maintained loop** — damageable and paid-maintained, exactly as the organism moved its
  succession controller's state out of host fields into the maintained substrate
  (AC87/88). This is the P2 structural constraint: the maintainer's own state is
  maintained.
- **Learning rule.** Trained to maximize continued cognitive operation (the same
  objective as S_reg — A is the machinery S_reg's decision acts through), subject to the
  budget. The *level* vs *switch* discipline (D5) applies: the optimum allocation is
  swept as a level family first; a learned all-or-nothing switch is not assumed.
- **Resource cost.** Its own computation is a processing cost; **its own working state is
  a paid-maintained cost** (the closure N5 makes the maintainer a *target* of the
  maintained, so its state is not free). This is the key difference from a host-side
  allocator.
- **Failure mode.** If A's allocation is independent of V (runs on a fixed schedule),
  N3 fails; if A's own state lives in unmaintained host fields, N5 fails (one-way
  dependency: R ← M with no return edge).
- **Relevant rival.** The *state-blind fixed schedule* (AC11's rival — must fail); the
  *host-side allocator* (an externally computed allocation, which is EXTERNAL scaffolding
  and never counts as autonomous, charter §4).
- **Intervention.** I5 (N5): change V's content only; A's allocation must reconfigure
  (not just refresh rate), and that reconfiguration must change V's future availability —
  the R → M → R′ cycle. I3 (N3): change V; upkeep spend co-varies.
- **Supplied or learned.** **Learned policy; its state in-loop (a supplied *requirement*,
  a learned *realization*).** The requirement that A's working state be vulnerable and
  maintained is supplied (it is the P2/N5 condition); the allocation policy itself is
  learned.

---

### 5.7 Self-evaluative pathway (E) — evidence about W's integrity without W's ground truth

This is N4, and it is stated as a **target** (per Q1 §3.4d: the program established the
cause-estimate is first-order, and the monitor is control-yes/prediction-no; N4 is what a
neural architecture must make *testable*). It is the one component with no completed
organism precedent, so it carries the sharpest design constraints.

- **Inputs.** The system's own bookkeeping about W — **not** W's ground-truth answer.
  Concretely: (i) the network's own prediction-error statistics (how often W's implied
  predictions mismatched the observations), (ii) internal-consistency/agreement signals
  (e.g. disagreement across sub-components that encode W), and (iii) the maintenance-
  machinery bookkeeping (whether W's slot is intact or degraded). None of these is the
  correct answer to "what is c."
- **Outputs.** A discrete verdict ê (binary or small counter): "W is reliable" vs "W is
  unreliable/stale," held in workspace slot E. (Gradedness is *not* assumed — D1/D4; a
  small discrete code is the default.)
- **Recurrence.** E is itself a maintained state (slot E, paid-refreshed), and it
  integrates evidence over time (a counter, not a per-step reflex).
- **Learning rule.** Trained (supervised) against *integrity labels* (was W actually
  correct/stale) **during training only** — a disclosed scaffold. **At deployment, E
  computes its verdict from the bookkeeping inputs above, with no access to the answer.**
  The distinction is the roadmap's own rule: the trigger/labels may be supplied; the
  *computation* of the evaluation from internal evidence is the thing under test.
- **Resource cost.** Its update is a processing cost; its persistence is paid (§5.5).
- **Failure mode (the dissociation signature, D7/C1).** E must be able to be *wrong about
  W in both directions*: a false alarm (ê = "unreliable" while W is correct) and a miss
  (ê = "reliable" while W is corrupted/stale). If E always co-moves with W with no
  dissociable cases, E is a re-encoding of W (meta-d′ = d′), not a distinct computation,
  and N4 is not realized. This is the built separation D7 demands, made measurable.
- **Relevant rival.** (i) The *first-order-only reflex* — a transient statistic (the
  AC117 `ones>=4` analogue) with no stored E; (ii) the *state-blind fixed maintenance
  policy*; (iii) the *ε-estimator arm* (estimating a world parameter rather than W's
  integrity) — to show E is not merely world-parameter estimation (C1 §3's rival set).
- **Intervention.** I4 (N4): selectively damage E only (then W only), holding world
  evidence fixed; E and W must dissociate in both directions, and E's value must track
  the maintenance bookkeeping, not the world.
- **Supplied or learned.** **Learned mapping; integrity labels supplied (training
  scaffold, disclosed).** The answer is available to the *trainer*, never to the deployed
  pathway — this is the "no ground truth at evaluation time" condition, and it is what
  distinguishes N4 from an oracle (which is labelled EXTERNAL and never counted, charter
  §4).

---

### 5.8 Temporal continuity (Θ_slow) — cross-episode carry via consolidation

- **Inputs.** The workspace contents W, V, E at episode end (or at consolidation events).
- **Outputs.** A slower store Θ_slow holding a consolidated copy of the maintained states,
  read back into the workspace at the next episode's start.
- **Recurrence.** Θ_slow is a slow-changing store (slow weights, or a low-rate recurrent
  state); it persists across episode boundaries where the fast workspace is reset/decayed.
- **Learning rule.** A learned *consolidation write* — a fast→slow transfer (or a learned
  write of the workspace state into the slow store), gated and paid. This is the neural
  analogue of the organism's succession copy write.
- **Resource cost.** The consolidation write is paid (energy), and the slow store is
  itself **vulnerable and paid-maintained** — if Θ_slow were a pristine weight matrix the
  decay stream never reaches, it would be a hidden backup and the component would violate
  P1/P2. It is a slower store, not a free one.
- **Failure mode.** No cross-episode carry (episode-reset) — the state does not influence
  later processing.
- **Relevant rival.** The *no-consolidation / episode-reset* arm (fast weights only, reset
  each episode). O1 is credited only if this rival fails — i.e. only if the carried state
  measurably influences later processing.
- **Intervention.** Cut the consolidation write; the next episode's processing must lose
  the carried influence.
- **Supplied or learned.** **Store supplied (slow weights are a substrate structure), the
  consolidation *write rule* learned.** Note on status: temporal continuity is **O1**, a
  *graded/optional* property in the ACO definition (Q1 §4) — it is not load-bearing for
  any N-property. It is included because the Q4 card lists it as required content; its
  *necessity* (whether cross-episode carry is required for consciousness-relevant
  computation, vs merely available) is a theory-specific question Q5 tests, not something
  this architecture assumes.

---

## 6. Mathematical descriptions of the load-bearing mechanisms

Three mechanisms carry the architecture's claim and are worth stating exactly. The rest is
standard recurrent/RL machinery and is not reproduced.

### 6.1 Active persistence under a budget (N1, P1)

Let H hold k maintained slots. Each slot i has value h_i(t) and, absent refresh, relaxes
toward a neutral value with rate δ:

```
h_i(t+1) = (1 − δ) · h_i(t) + δ · h_i^0 + r_i(t) · g_i(·)
```

where r_i(t) ∈ {0,1} is the refresh decision, g_i(·) the re-energizing input, and h_i^0
the neutral (non-functional) value. The maintenance process is π: r(t) = π(A, V, E). The
per-step maintenance spend is

```
E_π(t) = Σ_i r_i(t) · c_i,   with  E_π(t) + E_proc(t) ≤ B_t
```

Two facts follow and are the *testable* form of N1: (a) cutting π (r ≡ 0) drives
h_i → h_i^0 with time constant 1/δ — the decay timescale is set by the network dynamics,
not the environment (C1); (b) persistence is an *achievement*: every surviving
representation is surviving because E_π was spent on it, and that spend is drawn from a
shared, finite budget (P1). The pristine-backup rival corresponds to a second copy h_i'
that (1−δ) never decays (δ=0 for the backup) and no refresh ever touches — N1 is falsified
if h_i survives the cut as the backup does.

### 6.2 The closure cycle (N5, P2/P4/P7)

The directed cycle is

```
V_t ──(content)──▶ A_t ──(allocation)──▶ π_t ──(refresh)──▶ V_{t+1}
```

stated as: A_t = alloc(V_t, S_reg(W_t), E_t); π_t = refresh(A_t); V_{t+1} = update(V_t,
bookkeeping(π_t, H_t)). The return edge is that V's content changes A's *configuration*
(the budget split and the refresh vector — not merely the refresh rate of one slot), and
that reconfiguration changes V's own future availability (whether V's slot is sustained,
and what resource state V reports next). N5 is falsified if A's configuration is fixed
under a change of V (one-way dependency R ← M, no return edge) — which is I5's test. The
self-evaluative edge E → A is a second representation→maintainer edge; it is *not* the
closure cycle itself (E is about W's integrity, not about its own upkeep) but it makes the
evaluation load-bearing by reaching the same maintainer.

### 6.3 The dissociation signature (N4, D7/C1)

Let C ∈ {0,1} be W's *actual* correctness (ground truth, unobserved by E), and Ê ∈ {0,1}
be E's verdict. E is a distinct second-order computation — not a re-encoding of W — iff it
is built on a *separated* input set σ_E(W) ≠ σ_W (different bookkeeping than W's own
content path: the separation D7 names), **and** the contingency table (C, Ê) has non-zero
off-diagonal in both directions:

```
P(Ê = "unreliable" | C = correct)  > 0     (false alarm)
P(Ê = "reliable"    | C = corrupted) > 0    (miss)
```

with type-2 sensitivity meta-d′ ≠ type-1 sensitivity d′ as the standard summary
(Fleming & Daw 2017; Maniscalco & Lau 2012). The first-order collapse (C0) is the case
where σ_E(W) = σ_W and the table is diagonal — "the posterior is its own confidence," the
ideal-observer assumption the architecture violates by construction. N4 is a *target*: the
architecture is specified so this table is measurable (I4), not so that it is already
satisfied.

---

## 7. Intervention map (I1–I5 → components), and the rival set

Each selective intervention cuts one link, holding everything else fixed; each is paired
with the rival that must fail. This is the Q1 §7 contract, applied to the components.

| Intervention | Property | Cut (what, not what) | Component(s) | Falsified if |
| --- | --- | --- | --- | --- |
| I1 | N1 | cut π's refresh of a slot, **not** the slot, **not** the sensor | π, H (on W/V/E) | slot survives the cut (free permanence) or behaviour unchanged (inert) |
| I2 | N2 | scramble/retain W only | W, S_pol, S_reg | a state-blind policy or a content-free history counter reproduces the two behaviours |
| I3 | N3 | change V's content only | V, A | upkeep spend runs on a fixed schedule independent of V |
| I4 | N4 | damage E only, then W only; world evidence held fixed | E, W | E always co-moves with W (re-encoding), or the first-order reflex reproduces E |
| I5 | N5 | change V; observe A's reconfiguration; observe V's future availability | V, A, π | A's configuration is fixed under V's change (one-way dependency) |

**Mandatory rival set (inherited from P6, restated in neural terms so Q5/Q8 reuse it
verbatim):**

- **State-blind fixed schedule** — a maintenance/allocation policy with no dependence on
  the representation's content (AC11's rival).
- **Reactive / memoryless rival** — a sufficient statistic of the current observation, no
  maintained state (AC109's direct-diagnostic rival).
- **Finite-state / direct-control rival** — a hardwired, no-recurrence mapping.
- **First-order-only reflex** — a transient statistic (the AC117 `ones>=4` analogue),
  required where a second-order claim (N4) is made.

A rival is valid only if it is the candidate's own mechanism with the contested piece
removed (AC109 rule 1), and only if its parameter family is swept alongside the learner's
own (AC11/AC116 rule 2). Every component in §5 names the rival it must beat; the four
above are the canonical set those per-component rivals draw from.

**Composition rule (P7).** N1–N5 are required *jointly*; the architecture is tested under
simultaneous interventions (e.g. cut π's refresh of W *and* move the cause c — the
neural analogue of corrupt + move), with a byte-identity check at the intact boundary
before any difference is attributed to the composition (AC83's method). If two paid
costs interact at the shared budget (E_π + E_proc ≤ B_t), the simultaneous run differs
from the separate runs and composition is not unconditional — the failure that makes a
system "a representation plus its upkeep" rather than an organization.

---

## 8. Negative design constraints (D1–D8), enforced

The demoted principles are the architecture's other half. Each is a constraint this
architecture is built *not* to violate, with the falsifiable negative it is checked
against. (Table from `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` §4, applied to this design.)

| # | Constraint | Where enforced here |
| --- | --- | --- |
| D1 | Discrete/sparse default; graded only where it buys a distinct capability | every state (W, V, E, A's working state) is 1–3 bits; no graded confidence assumed (§1, §5.7) |
| D2 | No state for richness; add state only where a rival without it fails | §1 minimality test 2; the necessity rival column in §5 |
| D3 | Correctness rides the acquisition/update write, not continuous repair | §4 rule 2; W's accuracy via re-inference, π protects storage only (§5.1) |
| D4 | A representation doesn't earn its keep by predicting; a monitor is a directional-repair controller | §5.7: E is graded by the dissociation contrast, not predictive accuracy; W's worth is selector-role, not prediction (§5.1) |
| D5 | The optimum is a level, not a learned switch; sweep the level family | §5.6: A's allocation swept as a level family before any switch claim |
| D6 | Causal load-bearing and economic value are separate; gate on the causal contrast | §5.2/§5.3: worth graded on the I1–I5 causal contrasts, never the reward delta (X4) |
| D7 | A confidence/monitoring state requires a built separation; the posterior is not its own confidence | §5.7 + §6.3: E on a separated input set, dissociation signature meta-d′ ≠ d′ |
| D8 | Content self-production is not a prerequisite; acquired content + internalized maintenance suffices | §5.1/§5.2: cause taxonomy and resource variables supplied; beliefs/estimates acquired (X3) |

---

## 9. Coverage and minimality tables

**Coverage (every component serves a property, every property has a component):**

| N/O property | Realized by | Principle |
| --- | --- | --- |
| N1 active persistence | π (paid refresh) + H (recurrence) + W/V/E (maintained states) | P1, P2, D3 |
| N2 multiple-specialist consumption | W (shared content) + S_pol, S_reg (two consumers) | P3, P5 |
| N3 endogenous regulation | V (self-resource) + A (allocator) + S_reg | P2, P3, P4 |
| N4 internal evaluability (target) | E (self-evaluative pathway, dissociable) | P6, D4/D7 |
| N5 closure onto the maintainer | V → A → π → V cycle | P2, P4, P7 |
| O1 temporal continuity (card-required) | Θ_slow (consolidation store) | P1, P2 |

**Necessity (the rival that must fail for each component to earn its place):**

| Component | If removed, lost | Rival that must fail |
| --- | --- | --- |
| W | no shared content → N2/N3 untestable | memoryless/direct-diagnostic rival |
| V | no self-resource content → N3/N5 untestable | state-blind fixed schedule |
| S_pol, S_reg | one behaviour → N2 untestable | direct-control rival; single-objective collapse |
| H | no recurrence substrate → N1/N2 untestable | unbounded/pristine store |
| π | no paid persistence → N1 untestable | pristine backup; state-blind schedule |
| A | no allocation → N3/N5 untestable | host-side allocator; state-blind schedule |
| E | no second-order access → N4 untestable | first-order reflex; ε-estimator |
| Θ_slow | no cross-episode carry → O1 untestable | episode-reset rival |

The conjunction is the architecture. Remove one component and at least one property's
minimal test becomes un-runnable; that is the minimality claim, and it is stated so that a
future realization can *check* it (build the no-<component> arm and show the property
fails), not just assert it.

---

## 10. What this hands downstream

- **Q5 (indicator matrix).** The architecture is the neutral core on which the six
  families' loadings are tested. The optional/theory-specific mechanisms are deliberately
  **outside** the core and named for Q5's rows: attention (a serial bottleneck) → O3/GWT;
  predictive coding / self-supervised internal models → O2/PP; differentiable memory →
  O1. The cautionary rows are the demotions D1/D4/D7: do not let a theory-specific
  indicator smuggle back "graded is better," "monitoring = prediction," or the
  ideal-observer collapse.
- **Q6/Q7 (downstream).** This document is the architecture Q6/Q7 operate on; their
  vocabulary (component symbols, interventions, rivals) is fixed here.
- **Q8 (bridge experiment).** The bridge composes the four-column map
  (`ACI_NEURALIZATION_MAP_v1.md` §3) into one runnable experiment. This document's
  constraint for Q8: the core uses no novel primitive, so the bridge is runnable with an
  existing recurrent architecture plus a budget, a routing layer, and a consolidation
  store — and it must ship the four rivals (§7) and the simultaneous-intervention test
  (§7, P7). The three mathematical mechanisms of §6 are the bridge's falsification
  targets.

No autopoiesis claim and no consciousness claim is made anywhere in this document. The
strongest wording the organism program earns is unchanged (internalized paid maintenance,
causal-role-over-encoding, at the bounded degrees recorded); the ACO is a target, not a
result; and this architecture is a *design* for the smallest system that can test the
central ACI hypothesis — not a system that has been shown to satisfy it.

---

## Sources

Repo (read, not re-hashed or edited): `ACI_TARGET_CONSTRUCT_v1.md` (Q1; ACO, N1–N5,
optional O1–O4, rival set §7, interventions I1–I5 §7, theory families §10),
`ACI_NEURALIZATION_MAP_v1.md` (Q3; P1–P7 mechanism map, necessary vs optional set §5,
demotions D1–D8 §4), `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2; P1–P7, D1–D8),
`ACI_MISSION_AUDIT_v1.md` (Q0; evidence map, collapse record §2.6),
`DEFINITIONS_CHARTER_v1.md` (claim levels a–e; supplied substrate §5; S1–S4
internalization; the level-(d)/(e) boundary), `CONSCIOUSNESS_ROADMAP_v1.md` (chosen
mechanism; the estimate; the no-ground-truth rule; the monitor control-yes/prediction-no
status). Study references read from the skill's `references/` dir: `ac109.md`,
`ac110.md`, `ac113.md`, `ac116.md`, `m6-harness-result.md` (AC117), `c1-reliability.md`.
Frozen results read, never re-run or re-hashed. This document is derived and is not hashed
into any study's `pre_run_snapshot.json`.
