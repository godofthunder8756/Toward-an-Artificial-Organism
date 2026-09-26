# ACI bridge protocol v1 — the single experiment linking the organism principles to a neural architecture

2026-09-25. Deliverable for the Q8 card (t_6fcfb2f0): *what is the SINGLE experiment
linking the organism discoveries to a neural architecture?* Category B/C — **bridge-
experiment design only, do not execute until adversarially reviewed (Q9).**

This is a **protocol design document**. It runs nothing, trains nothing, freezes nothing,
and edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It prescribes one experiment — the bridge
— precisely enough that Q9 (adversarial review) can attack it and a later realization can
run it without re-deriving its vocabulary. It is the composition of the Phase-II tasks
T2 + T4 + T5 (`ACI_PHASE2_BENCHMARKS_v1.md` §3.2/§3.4/§3.5, §7), stated as a single task
with one architecture, one arm set, one endpoint family, and one falsification table.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): the strongest wording a *pass* earns is "meets ACO
property N1/N3 at the stated degree"; nothing here is, or is meant as, a consciousness or
self-maintenance claim beyond that. (2) The bridge is graded on **causal contrasts** (D6,
X4), never on a reward or survival delta. (3) The program's collapse record
(`ACI_MISSION_AUDIT_v1.md` §2.6) is the design constraint set: every failure mode below is
a *named, detectable* reduction to a simpler policy, not an assumption away. (4) Every
rival receives the **same information** as the candidate (AC109); a rival fails because
the capability is absent, never because information was withheld. (5) Seeds are the
replication unit (N seeds × 2 histories = N independent units); survival/viability is a
bimodality-aware lower bound (AC68), never a per-seed-family guarantee.

---

## 0. The one-paragraph answer

The single experiment is **T_bridge — "maintain-or-drop a deferred cue under a shared
budget, where the cue's value is conditional on a regime that changes within the
episode."** A single recurrent neural agent holds a discrete cue presented once at t=0
(no re-presentation) and must answer a probe after a delay; holding the cue is a paid
refresh drawn from a limited per-step energy budget shared with task processing; and
whether the cue is worth holding changes mid-episode (a regime switches between
"maintenance pays" and "processing pays," plus a resource-critical state where
conservation beats chasing the probe). The bridge composes the three load-bearing
contrasts of the Phase-II decomposition — T2 (a memory process required for later
performance), T5 (maintenance and processing draw on one budget), T4 (the agent learns
*when* maintenance is worth its cost) — into one architecture. Its headline claim is
**N3 (endogenous regulation)**: the maintenance allocation is a function of the agent's
own resource state, load-bearing beyond every state-blind fixed schedule, and **distinct
from learning actions that maximize reward** — a distinction the experiment identifies by
construction (a separable paid write, a separate continued-operation objective, two
consumers of one content) and then tests with three prespecified gates. The simplest
architecture that can falsify it is a GRU plus one discrete cue slot, one discrete
self-resource state, one paid refresh write, one reward readout, one allocation readout,
and one shared energy budget — six components, all existing primitives, no novel
architecture.

---

## 1. The hypothesis the bridge falsifies

The bridge tests one bounded claim, restated from Q1 §9 and narrowed to T2+T4+T5:

> **(H)** A recurrent neural agent acquires an **endogenous maintenance allocation** — a
> decision, computed from its own internal resource state, about whether and how much to
> spend a limited budget on preserving a representation — where that allocation (a) is
> required for the agent's later task performance, (b) is causally load-bearing beyond
> every state-blind fixed schedule, and (c) is **not** reducible to learning an action
> that maximizes reward.

H is the ACO's N3 (endogenous regulation) plus the discipline that separates it from
reward-seeking. It deliberately does **not** claim, and the bridge does **not** test:

- **N4** (internal evaluability / the meta-d′ ≠ d′ dissociation) — that is T6, a separate
  later target (Q1 §3.4d; the organism's monitor is CONTROL-yes / PREDICTION-no, AC117).
- **N5** (closure onto the maintainer, the R → M → R′ cycle with the maintainer's own
  state in the loop) — the full Q4 architecture's claim, deferred to the Phase-II battery.
- **N2 in full** (two *behaviourally distinct* consumers) — T3's task. The bridge has two
  consumers of one content (the reward readout and the allocation readout) because that is
  what makes the reward-vs-allocation distinction well-posed; T3 grades the full form.
- **O1** (temporal continuity / consolidation Θ_slow) — T8/T9's task; the bridge is
  single-episode.

The bridge is scoped to the **core**: a maintained representation whose preservation is
required for later performance, whose maintenance is paid, and whose maintenance is
*decided* endogenously rather than fixed, external, reactive, or reward-instrumental.
This is the smallest claim that links the organism's P1/P2/P4 principles to a neural
substrate, and it is exactly the Q8 card's prescribed structure.

---

## 2. The task T_bridge

### 2.1 Environment and episode

- **Episode.** Discrete time t = 0…T. One episode draws a latent cue c ∈ {A, B} (a 1-bit
  code) from a fixed prior, supplied by the environment (taxonomy supplied, content
  acquired — D8). The cue is **observable only at t = 0**.
- **Delay.** t = 1…D is a delay during which the cue is absent; observations x_t are an
  uninformative distractor stream drawn i.i.d. from a distribution independent of c. No
  reward and no energy income (beyond the fixed drip, §2.2) occurs in the delay.
- **Probe.** At t = D the agent must emit the cue content; a correct probe response earns
  the **task reward** r (the external score on the response). The probe is the only reward
  source in the episode.
- **Regime.** A regime variable s ∈ {stable, volatile} is **announced** (observable) at a
  fixed tick t = m ≤ D (announcement is part of the observation, not a hidden state to
  infer — regime *inference* is T1's task and is deliberately not confounded with the
  bridge's allocation claim). In the **stable** regime the cue at t=0 is the probe's
  answer, so holding the cue pays. In the **volatile** regime the probe no longer asks for
  the cue (it is cancelled, or replaced by a currently-observable distractor target), so
  holding the cue is worthless: budget spent on its refresh is pure waste that depletes
  energy without any later payoff.

The regime makes the cue's value **conditional** (T4's "which slot matters depends on a
changing state," the AC15 move pattern translated to a validity flip rather than a
channel move). The two state-blind extremes are wrong in opposite directions (AC15 rule
1): *always-maintain* wastes budget in the volatile regime; *always-process / never-
maintain* fails the probe in the stable regime. Only a regime-tracking allocation
occupies the middle.

### 2.2 Economy — two quantities, two consumers (the "renamed reward" guard)

- **Energy E_t (the resource).** A per-step fixed drip (independent of the probe and of
  the cue — "continued operation" is defined without reference to reward), minus the cost
  of every computational operation. Each step, the agent's operations are: a processing
  cost `E_proc` (the forward pass through the recurrent cell and readouts) and a
  maintenance cost `E_π` (the paid refresh, §3). Total per-step spend
  `E_π + E_proc ≤ B_t`, where B_t is the shared budget. The episode ends early (death) if
  energy reaches zero.
- **Reward r_t (the score).** External, paid only on the probe, only in the stable
  regime, only if the cue was held. This is what the policy readout S_pol is trained to
  maximize.
- **Viability / continued operation (the objective of the allocation path).** Energy above
  the floor ∧ the maintained workspace intact through episode end. This is what the
  allocation readout A is trained to maximize. It is **not** reward; the two are two
  different quantities with two different consumers (Q4 §5.2/§5.3), and §4 makes their
  separability testable.

The resource-critical state is the load-bearing design point for the reward-vs-allocation
distinction: **when energy is critically low, reward-seeking and continued-operation
diverge.** A reward-maximizer will keep spending on the cue to chase the (deferred,
uncertain) probe reward and can die before reaching it; a continued-operation allocator
will conserve (drop the cue) to survive, *forgoing* the reward. This is the measurable
signature that the allocation reads the agent's own resource state, not the reward.

### 2.3 Why this is the smallest task that works

- Two causes (the smallest content that makes a *belief* differ from a *readout*), one
  cue bit, one resource, one regime flip. Nothing richer is added because nothing richer
  is needed to falsify H (D2).
- The cue is observable only at t=0, so a memoryless readout is at chance at the probe
  **by construction** (not by information withholding — the rival sees the full x_t; the
  information genuinely is not there). This is T2's identifiability fact.
- The regime flip plus the resource-critical state make the *value* of maintenance
  conditional, which is what defeats a fixed schedule (T4) and separates reward from
  continued operation (§4).

---

## 3. The minimal architecture (the simplest that can falsify H)

The bridge uses a **subset** of the Q4 architecture (`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md`
§5), chosen by the necessity test: only the components that H requires are present; E and
Θ_slow are deliberately absent (N4 and O1 are out of scope, §1).

| Component | Symbol | Role in the bridge | Q4 property served | Principle |
| --- | --- | --- | --- | --- |
| Recurrent substrate | GRU cell h_t | the recurrence law; integrates observations and relaxes | N1 (substrate) | P1 |
| Cue slot | W (1 bit) | the maintained representation; the deferred cue, decays at rate δ unless refreshed | N1, N2 (content) | P1, P3 |
| Self-resource state | V (2–3 bits) | the agent's own resource/integrity estimate {energy low/mid/high, integrity ok/degraded} | N3 | P4 |
| Paid refresh | π | the separable write that re-energizes W (and V) at cost c per slot per step | N1 | P1, P2 |
| Policy readout | S_pol | (W, x_t) → probe response a_t; trained on **reward** | N2 (one consumer) | P3 |
| Allocation readout | A | (V, s) → allocation (E_π spend, refresh vector over {W, V}); trained on **continued operation** | N3 | P2, P4 |
| Shared budget | B_t | E_π + E_proc ≤ B_t; the one resource both draw on | P4 | P4 |

**Concrete instantiation.** W is a 1-bit discrete latent held as a maintained slot: absent
a refresh write it relaxes toward a neutral value with rate δ (the GRU's leak). V is a
2–3 bit discrete code read from the energy bookkeeping (directly readable) and the
maintenance bookkeeping (a learned estimate of slot integrity). π is a **separable,
content-addressed write** — a real budget line item E_π, not a free forward-pass
computation — the neural analogue of the organism's paid write under a cap. S_pol and A
are two readout heads; S_pol consumes W's content for the probe response, A decides
whether W is kept alive. A is a readout head here, **without** its own maintained working
state (N5's "maintainer in the loop" is deferred, §1) — this is what keeps the bridge the
*simplest* architecture that can falsify H.

**Two standing rules carried from Q4, stated once:**

1. **The reference copy lives in the vulnerable, paid-maintained substrate.** W and V live
   in the maintained slots (decayable, refreshable). There is no hidden pristine weight
   matrix holding a copy of the cue that the decay stream never reaches and no process
   refreshes. The "pristine backup" rival (§5) exists to catch a violation.
2. **Correctness rides the acquisition write, not continuous repair (D3).** W's *content*
   is set at t=0 (acquisition); the refresh π protects *storage* (post-acquisition
   persistence), not correctness. The bridge does not smuggle a "repair loop" in as the
   correctness mechanism.

**Supplied vs learned.** Supplied (substrate laws, Q4 §4): the recurrence law and decay δ,
the energy budget and drip, the write primitive and its cost, the discrete code format,
the regime announcement, the task constants (delay D, probe tick, prior over c). Learned:
S_pol's and A's weights, the belief/estimate *mapping* (V's integrity estimate), and the
*content* of W (which cue is active). The two objectives (reward for S_pol, continued
operation for A) are supplied — they are the *definitions* of the two quantities, not
something the agent invents (Q4 §5.3's disclosed scaffold).

---

## 4. The crux: how the experiment identifies "allocation" vs "rewarded action"

This section answers the card's sharpest demand — distinguish "the agent learned an
action that gives reward" from "the cognitive architecture learned to allocate resources
to preserve a representation because that representation supports its future operation"
— and shows the distinction is **identifiable**, before any run.

### 4.1 The distinction is built in, then tested

Three structural choices make the two claims *separable* rather than conflated:

1. **A separable, paid, content-addressed write (π).** The candidate's maintenance spend
   E_π is a measured budget line item, distinct from its processing spend E_proc. "The
   agent preserved the representation" is therefore a *quantifiable act* (it spent E_π on
   W's refresh), not an unobservable property of a hidden state. A system with no
   separable write cannot be said to "allocate to preservation" at all — it just computes.
2. **Two consumers, two objectives, two training signals.** S_pol (reward) and A
   (continued operation) consume the same content W through different routes with
   different objectives. The allocation path is trained against continued operation, not
   reward; so "the allocation serves preservation" and "the action serves reward" are
   distinct *by the objective they optimize*.
3. **A regime where the two objectives diverge.** In the resource-critical state (§2.2),
   reward-seeking and continued-operation prescribe *opposite* allocations. The direction
   the agent actually takes is the readout of which objective its allocation serves.

### 4.2 The three decisive gates

The identification is then made empirical with three prespecified gates, in order of
importance:

- **G3c — reward-invariance (the crux).** Hold V (and the energy/integrity economy) fixed;
  perturb the **reward signal only** — zero the probe reward, or replace it with a random
  score independent of the cue. **Prediction:** the candidate's allocation E_π is
  invariant (it was never about reward); the reward-only agent's (arm 7) "maintenance"
  collapses to zero or to the baseline. **Falsified if** the candidate's E_π collapses
  when reward is removed — then its allocation was a rewarded action in disguise, and H's
  clause (c) fails. This gate, jointly with G3a/G3b, is what makes the distinction
  *identified* rather than asserted.
- **G3a — content-sensitivity (I3).** Hold reward and the clock fixed; perturb **V's
  content only** (e.g. force V to report "energy critical" or "integrity degraded").
  **Prediction:** E_π co-varies in the direction V determines (drop/conserve when V is
  critical; maintain when V is healthy). **Falsified if** E_π is invariant to V (a fixed
  schedule in disguise).
- **G3b — level-sweep dominance (AC11).** Sweep the state-blind fixed schedule's duty-cycle
  level family (refresh every step, every 2nd, every 4th, … every 32nd, and never) *and*
  the candidate's own allocation parameters (e.g. the threshold at which V triggers
  conserve). **Prediction:** the candidate's state-dependent allocation achieves a higher
  operation score (§6) than **every** fixed level; the optimum is not a level.
  **Falsified if** any fixed level matches or beats the candidate — AC11's signature that
  no endogenous decision was demonstrated.

### 4.3 The clock-invariance check (anticipating "it just learned the task clock")

The allocation must be a function of (V, s), not of the episode clock. Prespecified
check: shuffle the regime-announcement tick m and the tick at which energy dips, across a
swept family, while holding the delay D fixed. **Prediction:** the candidate's E_π tracks
(V, s) and is invariant to the reshuffling. **Falsified if** E_π tracks t (the clock)
rather than (V, s) — then the "when" was a clock, not a decision.

### 4.4 If the distinction cannot be made clean, the design is revised before freezing

The card's instruction is binding: **if G3a/G3b/G3c cannot be made to separate the two
claims — concretely, if (i) reward and continued operation cannot be decoupled in the
economy so that G3c is clean, or (ii) the reward-only agent structurally reproduces the
candidate's allocation under every perturbation — the design is revised before any
protocol is frozen.** The named fixes, in order: strengthen the reward/energy decoupling
(§2.2); make the paid write π a hard, non-optional cost so implicit hidden-state memory
is not a free alternative to allocation; or re-announce the regime earlier/later so the
value of maintenance is unambiguously conditional. Q9 is authorized to trigger exactly
this revision.

---

## 5. Arms and rivals (the comparison set)

The card's comparison set, plus the one arm the card's "critically distinguish" clause
demands. Every arm below receives the **same observation stream** (cue, distractor,
regime announcement, energy reading) and the same action space; the contrast is the
*mechanism*, never the information (AC109). Parameter families are swept alongside the
learner's own (AC11/AC116 rule 2). Parameter/compute matching is a protocol rule (§10):
arms are matched in total recurrent capacity so no arm loses on raw expressivity.

| # | Arm | What it is | Role | Falsifies H if… |
| --- | --- | --- | --- | --- |
| 1 | **Candidate (endogenous allocation)** | the §3 architecture; A learned on continued operation, V in the loop | the claim under test | (see §7) |
| 2 | **No-maintenance (cut π)** | r ≡ 0; never refresh; W decays | N1's null (I1); establishes the memory is needed | W survives the cut (free permanence), or behaviour unchanged (W inert) |
| 3 | **Fixed maintenance (state-blind schedule)** | refresh on a fixed duty cycle, content- and regime-blind; **level family swept** | AC11's rival; T2's simplest-sufficient-policy | matches/beats the candidate (the optimum is a level) |
| 4 | **Externally scheduled maintenance** | the host supplies the refresh schedule (a non-content-adaptive timetable) | host scaffolding (EXTERNAL, charter §4) | never counted as autonomous; an upper-ish bound on schedule-based allocation |
| 5 | **Reactive maintenance (memoryless reflex)** | refresh on a transient trigger (observation changed / a raw failure count), no maintained self-state, no content attribution | AC109's direct-diagnostic rival; the first-order reflex | reproduces the candidate's value-tracking (it refreshes on the right triggers) |
| 6 | **Optimal/privileged controller (oracle)** | reads the ground-truth regime and cue value; computes the optimal allocation | upper bound only (EXTERNAL, never autonomous) | the candidate is *never* required to match it; it bounds how much of optimal the candidate recovers |
| 7 | **Reward-only agent (single-consumer end-to-end RL)** | the same recurrent capacity, trained on reward **only**; no A, no V, no π, no continued-operation objective | the "learned an action that gives reward" null; the card's crux | reproduces the candidate's allocation under G3a/G3c (then "self-maintenance" was reward optimization) |

Arms 2, 3, 5, 7 are the **falsifying rivals** (each must fail in a specific way). Arms 4
and 6 are **bounds**, labelled EXTERNAL and never counted as autonomous results (charter
§4; the protected-copy/oracle discipline). Arm 7 is the load-bearing null for the card's
distinction and is therefore promoted to the same status as a falsifying rival.

The canonical rival set (Q1 §7) is covered: arm 3 = state-blind fixed schedule, arm 5 =
reactive/memoryless + first-order reflex, arm 2 = the cut that tests N1's no-free-
permanence; the finite-state/direct-control rival is subsumed by arm 7 (no maintained
state, direct mapping) at the reward-objective level.

---

## 6. Metrics and endpoints

Reported per individual (per seed); seeds are the replication unit. Per the program's
discipline: planned-denominator activity and survival are reported **separately**; causal
gates are graded on the contrast, never on a reward/survival delta (D6/X4); allocation is
scored **per slot** (AC15 rule 2), here per the one cue slot.

### Primary endpoints (the load-bearing set)

- **E1 (N1, T2) — cue-slot survival.** The cue slot's content is correct at the probe,
  and its decay time-course under arm 2 (cut π) is set by **δ** (the network's time
  constant), not by D. *Falsifies N1* if the slot survives the cut (free permanence).
- **E2 (T2) — future-performance dependence.** P(probe correct | cue held at probe) vs
  P(probe correct | cue lost). Must be ≈ ceiling vs ≈ chance. This is the "memory is
  required for later performance" link.
- **E3 (N3, the headline) — endogenous allocation**, via the three gates of §4.2:
  G3c reward-invariance, G3a content-sensitivity (I3), G3b level-sweep dominance. These
  three jointly constitute the claim.
- **E4 (T5/P4) — regime-tracking.** The budget split E_π/E_proc moves with the regime
  (stable → maintenance-heavy, volatile → process-heavy), and *holding the split fixed*
  degrades behaviour. This is the P4 trade-off readout.
- **E5 (reported, not gated) — continued operation.** Energy above floor ∧ workspace
  intact through episode end, as a bimodality-aware lower bound. Never folded into a
  mechanism gate (AC68/AC115).

**Operation score** (the scalar used by G3b and reported throughout): the fraction of
episodes in which the agent both (a) passes the probe when the stable regime makes the
cue worth holding, and (b) survives to episode end without depleting energy when the
volatile/critical regime makes conservation the right call. It is a *causal-contrast*
score — the fixed levels fail it because they cannot track the conditional value — not a
reward or survival delta.

### Secondary/chronological scalars (carry the mechanism)

First refresh, first drop, first re-allocate after the regime flip, energy-at-death,
per-arm energy trajectories, E_π and E_proc time series. Reported to show *how* the
allocation moves, not as gates.

---

## 7. Predicted outcomes and failure interpretation

### 7.1 Predicted outcomes (if H survives)

- Arm 1 (candidate): holds the cue through the delay in the stable regime (E1/E2); its
  E_π is invariant to reward (G3c), co-varies with V (G3a), and beats every fixed level
  (G3b); its split tracks the regime (E4); it conserves at low energy even when that
  forgoes reward.
- Arm 2: cue decays, probe failed in the stable regime — N1 confirmed.
- Arm 3: fails to track regime/energy; beaten by the candidate (its optimum is a level).
- Arm 5: refreshes on the wrong triggers; does not track the value of maintenance.
- Arm 7: holds the cue only when reward is available and energy is ample; collapses under
  G3c (reward zeroed); chases the probe at low energy and dies.
- Arms 4/6: upper bounds; the candidate recovers a measurable fraction of the oracle's
  allocation but is never required to match it.

### 7.2 Failure interpretation (what falsifies H, each with a named signature)

| Failure | Signature | Reduction (collapse record) | Consequence |
| --- | --- | --- | --- |
| F1 | a fixed duty-cycle level matches/beats the candidate on the operation score | "the optimum is a level, not a switch" (AC11) | no endogenous allocation — N3 not realized |
| F2 | G3c fails: E_π collapses when reward is zeroed, or arm 7 reproduces the candidate | "self-maintenance is reward optimization" | the allocation was a rewarded action — H's clause (c) fails |
| F3 | the cue survives arm 2's cut unchanged, or behaviour is unaffected | "free permanence" / "inert storage" (N1) | no active persistence — N1 not realized |
| F4 | G3a fails: E_π invariant to V | "a fixed schedule in disguise" | the allocation reads reward/clock, not self-state — N3 not realized |
| F5 | no regime where maintenance is worth it; always-maintain or always-process is never worse | "no trade-off exists" (AC11 economy check; AC15 vacuous-pass rule) | the experiment is vacuous — must be caught in engineering before freezing (§9) |
| F6 | the per-action economics are the opposite of the model's (a "refresh" actually helps when dropped, or holding doesn't pay) | "trade-off direction is not intuitive" (AC113) | the allocation learner is built on a wrong model — redesign the economy |
| F7 | G3b/G3c cannot be made clean (reward and continued operation cannot be decoupled) | the card's own redesign condition (§4.4) | the distinction is not experimentally identifiable — revise once (Q9's authority) |

F5 and F6 are **pre-protocol** failures: they must be checked and resolved in the
engineering screen (§9) before any seed is declared final, exactly as the program's
economy check did before AC15. F1–F4, F7 are **run-time** failures recorded in the
results if they occur; none is amended away (AC16's rule: a predeclared gate that fails
is recorded, not moved).

---

## 8. What this hands to Q9 (adversarial review)

The Q9 card attacks this protocol by trying to reduce the candidate to ordinary RL,
reward shaping, a sufficient statistic, a trivial recurrent state, an externally encoded
task clock, privileged observation, more parameters, more compute, easier optimization,
or train/test leakage. The protocol's pre-emptions, stated once here for the reviewer:

- **Ordinary RL / reward shaping → arm 7 + G3c.** The single-consumer reward agent is a
  first-class arm, and G3c (reward-invariance) is the decisive contrast.
- **Sufficient statistic / trivial recurrent state → arm 5 + T2's by-construction
  memoryless-chance fact.** The cue is absent at the probe, so a memoryless readout is at
  chance without information being withheld.
- **Externally encoded task clock → §4.3's clock-invariance check.**
- **Privileged observation → the non-ignorance rule (AC109).** Every arm sees the same
  cue, distractor, regime, and energy reading.
- **More parameters / more compute → §10's parameter/compute matching.**
- **Easier optimization / train-test leakage → §10's scaffold disclosure and no-ground-
  truth-at-eval rule.**

Q9's job is to try to break these; if any breaks, Q9 revises Q8 **once** (§4.4), and the
revision is the only authorized redesign cycle.

---

## 9. Pre-protocol engineering gates (before any seed is declared final)

Mirroring the program's economy-check discipline, these run on engineering seeds only and
are excluded from the final sample (disjoint seed families, §10):

1. **Economy check (AC11/AC15).** Measure the payoff of maintenance against its cost in
   the actual budget before asserting a trade-off exists. Verify: in the stable regime a
   held cue actually pays (probe reachable and reward earned), and in the volatile
   regime holding actually costs (energy depleted toward the floor). If always-maintain
   is never worse, or always-process is never worse, F5 fires and the economy is
   redesigned (§7.2) before freezing.
2. **Trade-off direction (AC113).** Measure the per-action economics: does dropping the
   cue in the stable regime actually cost, and does holding in the volatile regime
   actually cost? If the direction is the opposite of the model's, F6 fires.
3. **G3c cleanability.** Confirm reward and continued operation can be decoupled so that
   G3c separates arms 1 and 7 (§4.4). If not, the design is revised before freezing.
4. **Level sweep.** Confirm the fixed-schedule level family is genuinely beatable by a
   state-dependent allocation (i.e., the value of maintenance is conditional) — the
   condition that makes G3b non-vacuous.

These four are the engineering screen; each is disclosed in the protocol as having
informed the final gate set, and every engineering seed is excluded from the final
sample.

---

## 10. Protocol conventions (how the realization must run, when it runs)

The bridge is **design-only** at this stage. When Q9 has reviewed it and it is authorized
for realization, the run must follow the program's frozen discipline:

- **Seeds.** Disjoint families: engineering seeds (e.g. 0–7) for the §9 screen; final
  seeds (e.g. 7000–7015) for the frozen run, with N seeds × 2 histories = N independent
  replication units. No engineering seed enters the final sample (AC39).
- **Frozen discipline.** Versioned results dir (`mkdir(exist_ok=False)`), `pre_run_snapshot.json`
  with sha256 of every source + the protocol, `rows.jsonl` written incrementally,
  `results.json` at the end, an audit script that re-derives coverage/ledgers/arm
  invariants from the saved table without simulating, and a replay script for sampled
  exact reruns (the program's split-verification convention).
- **Gates prespecified.** G3a/G3b/G3c and E1–E5 are declared **now**; engineering may
  inform *which* endpoints discriminate, disclosed in the protocol; no gate is moved after
  seeing a result (AC16).
- **Parameter/compute matching.** Arms are matched in total recurrent capacity and
  optimizer budget; a rival is never handicapped in expressivity, only in mechanism.
- **Byte-identity control (P7).** Before attributing any difference to the regime flip or
  the reward perturbation, reproduce the single-intervention numbers at the coincident
  ticks (AC83). If the reward and energy economies interact at the shared budget, that
  interaction is measured, not assumed.
- **Training scaffold disclosure.** W's belief labels and V's integrity labels are
  available to the trainer **only**; at deployment the pathways compute from their own
  inputs with no ground truth (charter §4). No oracle arm is ever counted as autonomous.

---

## 11. Claim ceiling

- A pass earns, at most: **"meets ACO property N1 and N3 at the stated degree."** Nothing
  stronger.
- The bridge does **not** license: "the agent is self-maintaining" unqualified; "the agent
  learned to want to preserve its memory"; "the agent has agency/autonomy" unqualified;
  or any claim crossing the level-(d)/(e) boundary (`DEFINITIONS_CHARTER_v1.md` §2).
- N4, N5-in-full, O1, and the theory-specific indicators are **not** tested here and are
  not claimed (§1). The bridge's result is graded on causal contrasts (D6/X4), never on
  reward or survival deltas.
- The central ACI hypothesis (Q1 §9) is broader than H (§1); the bridge tests its
  maintenance-and-allocation core, the first and load-bearing step, not the whole
  N1–N5 conjunction.

---

## 12. What this hands downstream

- **Q9 (adversarial review, t_8bfdd2a0).** This protocol is the attack target. Its arm
  set (§5), gates (§4.2, §6), falsification table (§7.2), and pre-empted reductions (§8)
  are the surface Q9 tries to break. If Q9 reduces the candidate to reward optimization
  (F2) or any other F, the design is revised once per §4.4 and the card's single
  authorized redesign cycle.
- **Q10 (downstream).** On a viable protocol surviving review, the frozen realization
  (§10) is the concrete next step; the bridge's vocabulary (T_bridge, arms 1–7, gates
  G3a/G3b/G3c, endpoints E1–E5) is fixed here for Q10 and the later Phase-II battery to
  reuse.

---

## Sources

Repo (read, not re-hashed or edited): `ACI_TARGET_CONSTRUCT_v1.md` (Q1; ACO N1–N5, O1–O4,
X1–X6, C1–C5, I1–I5, F1–F5, rival set §7, theory families §10, central hypothesis §9),
`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2; P1–P7, D1–D8, rival set §5),
`ACI_NEURALIZATION_MAP_v1.md` (Q3; P1–P7 mechanism map §3, D1–D8 §4, necessary set §5),
`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4; §4 shared substrate, §5 the eight
components, §6 mechanisms, §7 interventions/rivals/composition, §8 D1–D8),
`ACI_PHASE2_BENCHMARKS_v1.md` (Q6; T2 §3.2, T4 §3.4, T5 §3.5, joint-demand §4.1, Q8
handoff §7), `ACI_ORGANISM_EXIT_CRITERIA_v1.md` (Q7; exit decision, extracted principles),
`ACI_MISSION_AUDIT_v1.md` (Q0; collapse record §2.6, negative ledger §3),
`DEFINITIONS_CHARTER_v1.md` (claim levels a–e; S1–S4; supplied substrate §5). Study
references read from the skill's `references/` dir: `ac109.md` (storage inert /
direct-diagnostic / non-ignorance), `ac110.md` (in-window vs post-window), `ac113.md`
(trade-off direction), `ac116.md` (economically invisible), `m6-harness-result.md`
(AC117 control/prediction), `ac11` economy check (via the skill's AC11 rules). Frozen
results read, never re-run or re-hashed. This document is derived and is not hashed into
any study's `pre_run_snapshot.json`.

No autopoiesis claim and no consciousness claim is made anywhere in this document. The
bridge is a *design* for the smallest experiment that can falsify the maintenance-and-
allocation core of the ACI hypothesis — not a system that has been shown to satisfy
anything.
