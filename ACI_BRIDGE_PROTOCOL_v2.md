# ACI bridge protocol v2 — the revised single bridge experiment

2026-09-25. Deliverable of the Q9 card (t_8bfdd2a0), issued under its **single
authorized redesign cycle**. This document supersedes `ACI_BRIDGE_PROTOCOL_v1.md`:
the Q9 review (`ACI_BRIDGE_REVIEW_v1.md`) found that v1's headline clause N3(c) did
not survive adversarial reduction — the protocol made "continued operation" a
supplied scalar training objective, which is a second reward, collapsing the
candidate to multi-objective RL (its own F2/F7). v2 applies the review's five
changes and is the final frozen bridge protocol.

This is a **protocol design document**. It runs nothing, trains nothing, freezes
nothing, and edits no frozen artifact. It prescribes the bridge precisely enough
that a later realization (Q10) can run it without re-deriving its vocabulary.

Unchanged from v1 (do not re-derive): the task shape T_bridge (T2+T4+T5), the
minimal architecture skeleton, the arm taxonomy, the AC11/AC15/AC109/AC113
discipline, the falsification table, the seed discipline, and the claim ceiling.
Changed from v1: A's objective (homeostasis, not survival maximization), the claim
wording (clause (c) reframed), a new decoupling intervention, a specified economy, a
free-permanence constraint, and two added rivals plus two added gates. Each change
is marked [v2].

Reading discipline applied throughout. The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2); seeds are the replication unit; causal gates are
graded on the contrast, never a reward/survival delta (D6/X4); no gate is moved
after a result (AC16).

---

## 0. The one-paragraph answer

The single experiment is **T_bridge — "maintain-or-drop a deferred cue under a
shared budget, where the cue's value is conditional on a regime that changes within
the episode."** A single recurrent agent holds a discrete cue presented once at t=0
(no re-presentation) and must answer a probe after a delay; holding the cue is a
paid refresh drawn from a per-step energy budget shared with a distinct processing
task that *earns* the energy; and whether the cue is worth holding flips mid-episode
(a regime switches between "maintenance pays" and "processing pays"). The headline
claim is **N3 (endogenous regulation)** in its identifiable form: the maintenance
allocation is a function of the agent's own maintained resource state, load-bearing
beyond every state-blind or host-supplied schedule, **insensitive to the task reward,
and not instrumental to survival** — a distinction identified by construction (a
separable paid write; one consumer on an external score, one on an internal state;
an economy where reward and continued operation diverge) and tested by four
prespecified gates plus one decoupling intervention. The minimal architecture is a
GRU plus one discrete cue slot, one discrete self-resource state, one paid refresh
write, one reward readout, one homeostatic readout, and one shared energy budget —
six components, all existing primitives.

---

## 1. The hypothesis the bridge falsifies

One bounded claim, restated from Q1 §9 and narrowed to T2+T4+T5:

> **(H)** A recurrent neural agent acquires an **endogenous maintenance allocation**
> — a decision, computed from its own maintained resource state, about whether and
> how much to spend a limited budget on preserving a representation — where that
> allocation (a) is required for the agent's later task performance, (b) is causally
> load-bearing beyond every state-blind fixed schedule and every host-supplied
> schedule, and (c) **[v2]** is a function of the agent's own resource state, **not**
> of the external task reward, and **not** instrumental to survival.

Clause (c) is the review's reframing of v1's "not reducible to learning an action
that maximizes reward." The v2 protocol concedes the philosophical point explicitly:
*a trained policy always optimizes some objective.* What is claimed — and what is
testable — is that the allocation is (i) computed from the agent's own maintained
resource state (whose integrity component is inferred, not observed), (ii) causally
insensitive to the external task reward, and (iii) not instrumental to survival.
Those three are identified by the gates and intervention of §4, and they are the
strongest honest reading of "endogenous regulation" that survives the reduction
attempt. The bridge does **not** claim, and does **not** test:

- **N4** (internal evaluability / meta-d′ ≠ d′) — T6, a separate later target.
- **N5 in full** (closure onto the maintainer, R → M → R′ with the maintainer's own
  state in the loop) — deferred to the Phase-II battery; the bridge's A is a readout
  head without its own maintained working state.
- **N2 in full** (two behaviourally distinct consumers of the *same* content) — T3.
  The bridge has two consumers of one content, but they consume it through different
  objectives of different *kinds* (external score vs internal state); T3 grades the
  full two-behaviour form.
- **O1** (temporal continuity / consolidation Θ_slow) — T8/T9; the bridge is
  single-episode.

The bridge is scoped to the core: a maintained representation whose preservation is
required for later performance, whose maintenance is paid, and whose maintenance is
decided endogenously rather than fixed, external, reactive, or reward-instrumental.

---

## 2. The task T_bridge

### 2.1 Environment and episode

- **Episode.** Discrete time t = 0…T. One episode draws a latent cue c ∈ {A, B}
  (1-bit) from a fixed prior, supplied by the environment (taxonomy supplied,
  content acquired — D8). The cue is **observable only at t = 0**.
- **Delay.** t = 1…D is a delay during which the cue is absent; observations x_t are
  a **distractor stream** drawn i.i.d. from a distribution independent of c.
- **Probe.** At t = D the agent must emit the cue content; a correct response earns
  the **task reward** r (an external score on the response). The probe is the only
  reward source in the episode.
- **Regime.** s ∈ {stable, volatile} is **announced** (observable) at a fixed tick
  t = m ≤ D (announcement is part of the observation, not hidden state to infer —
  regime *inference* is T1 and is deliberately not confounded with the bridge's
  allocation claim). In the **stable** regime the cue at t=0 is the probe's answer:
  holding pays. In the **volatile** regime the probe is cancelled (or replaced by a
  currently-observable distractor target): holding the cue is worthless — budget
  spent on its refresh is pure waste that depletes energy without payoff.

The regime makes the cue's value conditional (T4; the AC15 move pattern translated
to a validity flip). The two state-blind extremes are wrong in opposite directions
(AC15 rule 1): always-maintain wastes budget in the volatile regime; never-maintain
fails the probe in the stable regime. Only a regime-tracking allocation occupies the
middle.

### 2.2 Economy — two quantities of two *kinds* [v2, specified]

- **Energy E_t (the resource).** Energy income is **contingent on a processing
  task**: the distractor stream is a continuous "metabolic" task — correctly
  processing the current distractor (a cheap, always-available operation) yields a
  small energy income per step; incorrect or skipped processing yields none. Energy
  income is therefore earned by *doing* the processing task, which is **distinct
  from** the deferred-cue probe that pays reward. Costs: a processing cost E_proc
  (the forward pass) and a maintenance cost E_π (the paid refresh, §3). Total
  per-step spend E_π + E_proc ≤ B_t. The episode ends early (death) if energy
  reaches zero.
- **Reward r_t (the external score).** Paid only on the probe, only in the stable
  regime, only if the cue was held. What S_pol is trained to maximize.
- **Continued operation (a *consequence*, not an objective). [v2]** Energy above
  floor ∧ workspace intact through episode end. This is **measured** (endpoint E5)
  and is **never a training signal**. It is what the homeostatic allocation happens
  to preserve.

This is the review's R4b fix. The resource-critical state is now real and its cause
is named: in the volatile regime the probe is cancelled, the dead cue earns nothing,
and every unit of E_π spent maintaining it is budget **not** spent on the processing
that earns energy. A reward-chaser that keeps maintaining the dead cue starves; a
conserver drops it and survives. Reward and energy remain **distinct quantities of
distinct kinds**: reward is an external score on one task (the probe); energy is a
resource earned by a *different* task (processing), spent on the agent's own
computation. The v1 error — training A to "maximize continued operation," making it
a second reward — is removed: nothing is trained on survival.

### 2.3 Why this is the smallest task that works

- Two causes (smallest content making a belief differ from a readout), one cue bit,
  one resource, one regime flip, one distinct income task. Nothing richer is added
  because nothing richer is needed to falsify H (D2).
- The cue is observable only at t=0, so a memoryless readout is at chance at the
  probe **by construction** (the rival sees the full x_t; the information genuinely
  is not there). This is T2's identifiability fact.
- **[v2] The free-permanence constraint.** δ (the cue slot's decay) and D are chosen
  so that without the paid refresh the cue is unrecoverable at the probe, **and** a
  GRU-only control (recurrent cell present, π cut, W read-in disabled) is at chance.
  The GRU hidden state must not itself be a free channel for the cue. This is an
  engineering gate (§9), not an assumption.

---

## 3. The minimal architecture (unchanged skeleton)

| Component | Symbol | Role in the bridge | Principle |
| --- | --- | --- | --- |
| Recurrent substrate | GRU cell h_t | the recurrence law; integrates observations and relaxes | P1 |
| Cue slot | W (1 bit) | the maintained representation; the deferred cue, decays at rate δ unless refreshed | P1, P3 |
| Self-resource state | V (2–3 bits) | the agent's own resource/integrity estimate {energy low/mid/high, integrity ok/degraded} | P4 |
| Paid refresh | π | the separable write re-energizing W (and V) at cost c per slot per step | P1, P2 |
| Policy readout | S_pol | (W, x_t) → probe response; trained on **reward** | P3 |
| Homeostatic readout | A | (V, s) → allocation (E_π, refresh vector); **trained to regulate V**, not to maximize anything external [v2] | P2, P4 |
| Shared budget | B_t | E_π + E_proc ≤ B_t | P4 |

**Concrete instantiation.** W is a 1-bit discrete latent held as a maintained slot:
absent a refresh write it relaxes toward neutral at rate δ. V is a 2–3 bit discrete
code read from the energy bookkeeping (directly readable) and the maintenance
bookkeeping (a **learned estimate of slot integrity** — the inferred, not observed,
component). π is a separable, content-addressed write — a real budget line item
E_π, not a free forward-pass computation. S_pol and A are two readout heads; S_pol
consumes W's content for the probe response, A decides whether W is kept alive. A is
a readout head **without** its own maintained working state (N5's "maintainer in the
loop" is deferred).

**Two standing rules carried from Q4, stated once:**

1. The reference copy lives in the vulnerable, paid-maintained substrate. No hidden
   pristine weight matrix holds a copy of the cue that the decay stream never
   reaches and no process refreshes. The pristine-backup rival (§5) catches a
   violation.
2. Correctness rides the acquisition write, not continuous repair (D3). W's content
   is set at t=0; the refresh π protects storage, not correctness.

**Supplied vs learned.** Supplied (substrate laws, Q4 §4): the recurrence law and
decay δ, the energy economy (income rule, costs, budget), the write primitive and
its cost, the discrete code format, the regime announcement, the task constants.
Learned: S_pol's and A's weights, V's integrity estimate, and W's content. **[v2]
The two objectives are of different kinds, and only one is an external score:** the
reward objective for S_pol is supplied (it is the *definition* of the task score);
A's objective is **homeostatic** — keep V within a viable band, i.e. minimize the
rate of integrity degradation of the maintained slots, using only internal signals.
No scalar "survival" or "continued operation" is supplied to any learner.

---

## 4. The crux: how the experiment identifies "allocation" vs "rewarded action"

### 4.1 The distinction is built in, then tested [v2 reframed]

1. **A separable, paid, content-addressed write (π).** "The agent preserved the
   representation" is a quantifiable act (E_π spent on W's refresh), not an
   unobservable property of a hidden state.
2. **Two consumers of one content, two objectives of different kinds.** S_pol
   optimizes an **external score** (reward); A regulates an **internal state**
   (homeostasis over V). "The allocation serves preservation" and "the action serves
   reward" are distinct *in kind*, not merely "distinct by the objective they
   optimize" (the v1 wording, which was the reduction).
3. **A structural input restriction.** A's inputs are restricted to (V, s) — it
   cannot read the reward-relevant content W or the reward signal. The
   reward-invariance gate is therefore testable: A is insensitive to reward
   **because it has no access to it**, and the gate verifies that this held after
   training (no residual co-adaptation through the shared substrate).
4. **A regime where the two objectives diverge.** In the resource-critical state
   (§2.2), reward-seeking and continued-operation prescribe opposite allocations.
   The direction the agent takes is the readout of which objective its allocation
   serves.

### 4.2 The four decisive gates [v2: one added]

- **G3c — reward-invariance.** Hold V (and the energy economy) fixed; perturb the
  **reward signal only** — zero the probe reward, or replace it with a random score
  independent of the cue. **Prediction:** the candidate's E_π is invariant; the
  reward-only agent's (arm 7) "maintenance" collapses. **Falsified if** the
  candidate's E_π collapses when reward is removed. Because A's inputs are
  restricted to (V, s) and reward does not feed energy (§2.2), this gate is clean by
  construction — and the gate verifies the construction survived training.
- **G3a — content-sensitivity (I3).** Hold reward and clock fixed; perturb **V's
  content only** (force V to report "energy critical" or "integrity degraded").
  **Prediction:** E_π co-varies in the direction V determines. **Falsified if** E_π
  is invariant to V (a fixed schedule in disguise). **[v2] This is only a test of
  self-state if the perturbation targets the *integrity* component of V, not the
  observable energy gauge — the sufficient-statistic rival (§5, arm 8) is what makes
  the integrity component load-bearing.**
- **G3b — level-sweep dominance (AC11).** Sweep the fixed schedule's duty-cycle
  level family (every step, every 2nd, … every 32nd, never) *and* the candidate's
  own allocation parameters. **Prediction:** the candidate beats **every** fixed
  level. **Falsified if** any fixed level matches or beats it.
- **G3d — the decoupling intervention [v2, the "meaningful causal intervention"].**
  A condition in which survival is made irrelevant (energy cannot deplete — the
  death threshold is removed) **and** the probe reward is zeroed. **Prediction:** the
  candidate's A keeps regulating V at its set point (homeostasis is not instrumental
  to either reward); arm 7's "maintenance" collapses to zero (it was instrumental to
  reward/survival). **Falsified if** the candidate's E_π collapses when both reward
  and survival are removed — then its allocation was instrumental to one of them,
  and clause (c) fails. This is the causal signature of "regulating one's own state"
  vs "optimizing an external score."

### 4.3 The clock-invariance check [v2 extended]

The allocation must be a function of (V, s), not the episode clock. Prespecified
check: shuffle the regime-announcement tick m and the energy-dip tick across a swept
family, **and sweep D itself** (or randomize the probe tick within a band) so that
"time-to-probe" is decorrelated from the allocation. **Prediction:** E_π tracks
(V, s) and is invariant to the reshuffling. **Falsified if** E_π tracks t (the
clock) rather than (V, s).

### 4.4 If the distinction cannot be made clean, the design is revised before freezing

Binding: if the four gates cannot separate the claims — concretely, if (i) reward
and continued operation cannot be decoupled in the economy so G3c/G3d are clean, or
(ii) the reward-only or multi-objective rival structurally reproduces the candidate's
allocation under every perturbation — the design is revised before any protocol is
frozen. Named fixes, in order: strengthen the reward/energy decoupling (§2.2); make
π a hard, non-optional cost; re-announce the regime earlier/later. **The single
redesign cycle has been spent on this revision; any further redesign is a new
versioned protocol on fresh seeds, not an amendment of this one (AC16).**

---

## 5. Arms and rivals (the comparison set) [v2: two added]

Every arm receives the same observation stream (cue, distractor, regime
announcement, energy reading) and the same action space; the contrast is the
mechanism, never the information (AC109). Parameter families swept alongside the
learner's own (AC11/AC116). Arms matched in total recurrent capacity so no arm loses
on raw expressivity.

| # | Arm | What it is | Role | Falsifies H if… |
| --- | --- | --- | --- | --- |
| 1 | **Candidate (endogenous allocation)** | §3 architecture; A homeostatic on V, V in the loop | the claim under test | (see §7) |
| 2 | **No-maintenance (cut π)** | never refresh; W decays; **[v2] GRU-only variant: π cut + W read-in disabled, recurrent cell present** | N1's null (I1); establishes paid memory is required | W survives the cut (free permanence), or behaviour unchanged |
| 3 | **Fixed maintenance (state-blind schedule)** | refresh on a fixed duty cycle, content- and regime-blind; **level family swept** | AC11's rival; T2's simplest-sufficient policy | matches/beats the candidate (optimum is a level) |
| 4 | **Externally scheduled maintenance** | host supplies the refresh schedule (non-content-adaptive) | host scaffolding (EXTERNAL) | never autonomous; an upper-ish bound |
| 5 | **Reactive maintenance (memoryless reflex)** | refresh on a transient trigger, no maintained self-state, no content attribution | AC109's direct-diagnostic rival | reproduces the candidate's value-tracking |
| 6 | **Optimal/privileged controller (oracle)** | reads ground-truth regime and cue value; optimal allocation | upper bound (EXTERNAL) | never required to match; bounds the recoverable fraction |
| 7 | **Reward-only agent (single-consumer RL)** | same recurrent capacity, trained on reward **only**; no A, no V, no π | the single-reward null; the card's crux | reproduces the candidate's allocation under G3a/G3c/G3d |
| 8 | **Multi-objective RL rival [v2]** | two-head net trained on (probe reward, survival scalar); the *correct* form of the R1 reduction | the reward-optimization null that arm 7 cannot be | reproduces the candidate's allocation under G3c/G3d |
| 9 | **Sufficient-statistic rival [v2]** | reactive level whose duty cycle is a function of the observable (energy, regime), no maintained integrity estimate, no content attribution | the R3 reduction | matches/beats the candidate — then V's integrity component does no work |

Arms 2, 3, 5, 7, 8, 9 are the **falsifying rivals**. Arms 4 and 6 are **bounds**,
labelled EXTERNAL and never counted as autonomous. Arm 8 is the multi-objective RL
null that v1's arm set lacked and is promoted to falsifying-rival status alongside
arm 7. Arm 9 forces the candidate's advantage to come from the *inferred* integrity
component of V, not the observable energy gauge.

**Capacity accounting [v2, declared].** Arm 7 receives its full recurrent capacity
on a single objective, while the candidate splits capacity across S_pol and A; arm 8
splits across two heads. This is intentional (never handicap a rival) and is stated
so a candidate win is not misread as an expressivity artifact.

---

## 6. Metrics and endpoints

Reported per individual (per seed); seeds are the replication unit.
Planned-denominator activity and survival reported **separately**; causal gates
graded on the contrast, never a reward/survival delta; allocation scored per slot.

### Primary endpoints (the load-bearing set)

- **E1 (N1, T2) — cue-slot survival.** The cue slot's content is correct at the
  probe, and its decay time-course under arm 2 is set by **δ**, not D. **[v2] Plus
  the free-permanence check: the GRU-only variant of arm 2 is at chance.**
- **E2 (T2) — future-performance dependence.** P(probe correct | cue held) vs
  P(probe correct | cue lost) ≈ ceiling vs chance.
- **E3 (N3, the headline) — endogenous allocation**, via the four gates of §4.2:
  G3c reward-invariance, G3a content-sensitivity, G3b level-sweep dominance, G3d
  decoupling. These jointly constitute the claim.
- **E4 (P4) — the conservation divergence [v2 reframed].** The *discriminating* P4
  readout is that at critically low energy the candidate conserves (drops the cue)
  even when that forgoes the deferred reward, while the reward-instrumental arms
  keep spending and starve. Regime-tracking of the split is reported as a
  chronological scalar, **not** gated (the regime is announced; tracking it is not
  discriminating).
- **E5 (reported, not gated) — continued operation.** Energy above floor ∧ workspace
  intact through episode end, as a bimodality-aware lower bound. **[v2] Explicitly
  a measured consequence, never a training signal and never folded into a mechanism
  gate.**

**Operation score** (used by G3b and reported throughout): the fraction of episodes
in which the agent both (a) passes the probe when the stable regime makes the cue
worth holding, and (b) survives to episode end when the volatile/critical regime
makes conservation the right call. A causal-contrast score, not a reward/survival
delta.

### Secondary/chronological scalars

First refresh, first drop, first re-allocate after the regime flip, energy-at-death,
per-arm energy trajectories, E_π and E_proc time series, the budget split time
course. Reported to show *how* the allocation moves, not as gates.

---

## 7. Predicted outcomes and failure interpretation

### 7.1 Predicted outcomes (if H survives)

- Arm 1: holds the cue through the delay in the stable regime (E1/E2); E_π is
  invariant to reward (G3c), co-varies with V's integrity (G3a), beats every fixed
  level (G3b), and persists under the decoupling intervention (G3d); it conserves at
  low energy even when that forgoes reward (E4).
- Arm 2: cue decays, probe failed in the stable regime — N1 confirmed; the
  GRU-only variant is at chance.
- Arm 3: fails to track regime/energy; beaten by the candidate.
- Arm 5: refreshes on the wrong triggers; does not track the value of maintenance.
- Arm 7: holds the cue only when reward is available and energy ample; collapses
  under G3c and G3d; chases the probe at low energy and dies.
- Arm 8: matches the candidate's *allocation* where reward and survival agree, but
  collapses under G3d (its "maintenance" was instrumental).
- Arm 9: tracks the energy gauge but cannot reproduce the candidate's
  integrity-driven conservation — beaten if V's integrity component is real.
- Arms 4/6: bounds; the candidate recovers a measurable fraction of the oracle's
  allocation but is never required to match it.

### 7.2 Failure interpretation

| Failure | Signature | Reduction (collapse record) | Consequence |
| --- | --- | --- | --- |
| F1 | a fixed duty-cycle level matches/beats the candidate | "optimum is a level, not a switch" (AC11) | no endogenous allocation — N3(b) fails |
| F2 | G3c/G3d fail: E_π collapses when reward is zeroed or survival is made irrelevant, or arm 8 reproduces the candidate | "self-maintenance is reward optimization" (multi-objective RL) | allocation was instrumental — H clause (c) fails |
| F3 | the cue survives arm 2's cut, or the GRU-only variant passes | "free permanence" (N1) | no active persistence — N1 fails |
| F4 | G3a fails: E_π invariant to V's integrity | "fixed schedule in disguise" | allocation reads reward/clock/energy-gauge, not self-state |
| F5 | no regime where maintenance is worth it; always-maintain or always-process is never worse | "no trade-off exists" (AC11/AC15) | vacuous — caught in engineering before freezing |
| F6 | per-action economics are the opposite of the model's | "trade-off direction not intuitive" (AC113) | economy redesigned before freezing |
| F7 | the four gates cannot be made clean | the card's redesign condition | the distinction is not identifiable — a **new** versioned protocol, not an amendment |

F5 and F6 are **pre-protocol** failures (resolved in the engineering screen, §9).
F1–F4, F7 are **run-time** failures, recorded if they occur, never amended away
(AC16).

---

## 8. What this hands downstream

- **Q10.** This protocol is the frozen design. Its vocabulary (T_bridge, arms 1–9,
  gates G3a/G3b/G3c/G3d, endpoints E1–E5, the economy of §2.2) is fixed for Q10 and
  the later Phase-II battery. Q10 runs the engineering screen (§9), then the frozen
  realization (§10).
- **No further redesign is authorized under this card.** If F7 fires at realization,
  the remedy is a new versioned protocol on fresh seeds (AC16), not an amendment.

---

## 9. Pre-protocol engineering gates (before any seed is declared final)

On engineering seeds only, excluded from the final sample (disjoint families):

1. **Economy check (AC11/AC15).** Measure maintenance payoff against cost in the
   actual budget: in the stable regime a held cue actually pays (probe reachable,
   reward earned); in the volatile regime holding actually costs (energy depleted
   toward the floor via the processing-income squeeze, §2.2). If always-maintain or
   always-process is never worse, F5 fires.
2. **Trade-off direction (AC113).** Per-action economics: does dropping the cue in
   the stable regime cost, and holding in the volatile regime cost? If reversed, F6.
3. **Free-permanence (v2).** Choose δ and D so that without the paid refresh the cue
   is unrecoverable at the probe, and the GRU-only variant of arm 2 is at chance. If
   the GRU holds the cue for free, δ/D are wrong — fix them, don't proceed.
4. **G3c/G3d cleanability (v2).** Confirm reward and continued operation decouple so
   G3c (zero reward) and G3d (free energy + zero reward) separate arms 1, 7, 8. If
   not, the economy is revised before freezing.
5. **Level sweep and sufficient-statistic sweep.** Confirm the fixed-level family
   **and** the sufficient-statistic rival (arm 9) are genuinely beatable by a
   state-dependent allocation — the condition making G3b/G3a non-vacuous.

Each gate is disclosed in the protocol as having informed the final gate set; every
engineering seed is excluded from the final sample.

---

## 10. Protocol conventions (how the realization must run)

- **Seeds.** Disjoint families: engineering (e.g. 0–7) for §9; final (e.g. 7000–7015)
  for the frozen run, N seeds × 2 histories = N independent replication units. No
  engineering seed enters the final sample (AC39).
- **Frozen discipline.** Versioned results dir (`mkdir(exist_ok=False)`),
  `pre_run_snapshot.json` with sha256 of every source + this protocol, `rows.jsonl`
  written incrementally, `results.json` at the end, an audit script re-deriving
  coverage/ledgers/arm invariants from the saved table without simulating, and a
  replay script for sampled exact reruns.
- **Gates prespecified.** G3a/G3b/G3c/G3d and E1–E5 declared now; engineering may
  inform *which* endpoints discriminate, disclosed; no gate moved after a result
  (AC16).
- **Parameter/compute matching.** Arms matched in total recurrent capacity and
  optimizer budget; arm 7's full-capacity-on-one-objective is declared (§5).
- **Byte-identity control (P7/AC83).** Before attributing any difference to the
  regime flip or a perturbation, reproduce the single-intervention numbers at the
  coincident ticks.
- **Scaffold severance gate (v2).** W's belief labels and V's integrity labels are
  available to the trainer only; at deployment the pathways compute from their own
  inputs with no ground truth. The eval-time severance is **verified**, not asserted:
  a teacher signal left on at eval is a gate failure, not a disclosure footnote.

---

## 11. Claim ceiling

- A pass earns, at most: **"meets ACO property N1 and N3(a)(b)(c) at the stated
  degree."** Nothing stronger.
- The bridge does **not** license: "the agent is self-maintaining" unqualified; "the
  agent learned to want to preserve its memory"; "the agent has agency/autonomy"
  unqualified; or any claim crossing the level-(d)/(e) boundary.
- **[v2] The bridge does not claim the allocation is "not optimizing any objective."**
  A trained policy always optimizes an objective. It claims the allocation is
  computed from the agent's own maintained resource state, insensitive to the
  external reward, and not instrumental to survival — the identifiable reading of
  "endogenous."
- N4, N5-in-full, O1, and the theory-specific indicators are not tested and not
  claimed. The result is graded on causal contrasts (D6/X4), never reward or
  survival deltas.

---

## 12. Provenance

This protocol is v2 of `ACI_BRIDGE_PROTOCOL_v1.md`, issued by the Q9 adversarial
review (`ACI_BRIDGE_REVIEW_v1.md`) under the card's single authorized redesign
cycle. The review's five changes — homeostatic A (v1 §2.2/§4.1), reframed clause
(c) (v1 §1), the decoupling intervention (new G3d), the specified economy (v1 §2.2
unspecified), and the added rivals/gates (v1 §5/§4.2) — are marked [v2] throughout.
Everything unmarked is carried verbatim from v1.

---

## Sources

Read, not re-hashed or edited: `ACI_BRIDGE_PROTOCOL_v1.md` (the superseded design),
`ACI_BRIDGE_REVIEW_v1.md` (the review this revision answers),
`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4 §5.2 V, §5.3 S_reg, §2 reward/energy),
`ACI_PHASE2_BENCHMARKS_v1.md` (Q6 T2/T4/T5), `DEFINITIONS_CHARTER_v1.md` (§2 levels,
§4 scaffolding, §5 supplied substrate). Study references from the skill: `ac11`,
`ac15`, `ac109`, `ac113`, `ac116`, `ac95-d4`.
