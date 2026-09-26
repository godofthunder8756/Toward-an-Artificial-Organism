# Phase-II baseline v1 — the bridge experiment reconciled from the ACI docs at HEAD 1ad7b7d

2026-09-25. Deliverable for the N0 card (t_493fdfb3): *what is the exact Phase-II
baseline — hypothesis, architecture, information flow, objectives, rivals, weaknesses,
claim ceiling — reconciled from the ACI docs at HEAD 1ad7b7d?* Category B/F — **baseline
reconciliation; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It states, in one place, the baseline
that the downstream Phase-II cards N1, N3, N4 (and the v3 protocol card N8) read their
vocabulary from, instead of re-deriving it from six separate documents.

Reading discipline applied throughout. (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; survival/viability is a bimodality-aware lower bound, never a
per-seed-family guarantee (AC68/AC39). (3) Organism results transfer as **principles and
discipline, not as neural evidence** — the neural phase starts fresh; the organism's
physics (rule bank, W/C/B particles, conservation economy, succession machine) does not
map to neural substrate, and no frozen organism number is re-read as a neural result.

---

## 0. The one-paragraph answer

Phase II is the **bridge experiment** (`ACI_BRIDGE_PROTOCOL_v2.md`), the first neural
realization of the organism program's most-repeated positive result — internalized, paid,
produced-machinery maintenance — lifted onto a recurrent neural substrate. Its task is
**T_bridge**: a single recurrent agent holds a discrete cue presented once at t=0 and must
answer a probe after a delay; holding the cue is a paid refresh drawn from a per-step
energy budget shared with a distinct processing task that *earns* the energy; and whether
the cue is worth holding flips mid-episode via an announced regime. The claim under test is
**H (endogenous maintenance allocation)**, the bridge's identifiable form of ACO
properties **N1 (active paid persistence) + N3 (endogenous regulation)**. The architecture
is a GRU plus one cue slot, one self-resource state, one paid refresh write, one reward
readout, one homeostatic readout, and one shared budget — six components, all existing
primitives. The claim is tested by four prespecified gates (G3a/G3b/G3c/G3d) plus one
decoupling intervention, against nine arms (six falsifying rivals, two EXTERNAL bounds, one
candidate). A pass earns at most "meets ACO property N1 and N3(a)(b)(c) at the stated
degree" — nothing stronger, no consciousness, no metacognition, no workspace seat, no
autopoiesis.

---

## 1. The hypothesis (the T_bridge maintain-or-drop claim)

One bounded claim (`ACI_BRIDGE_PROTOCOL_v2.md` §1), narrowed to T2+T4+T5:

> **(H)** A recurrent neural agent acquires an **endogenous maintenance allocation** — a
> decision, computed from its own maintained resource state, about whether and how much to
> spend a limited budget on preserving a representation — where that allocation
> (a) is required for the agent's later task performance, (b) is causally load-bearing
> beyond every state-blind fixed schedule and every host-supplied schedule, and (c) **[v2]**
> is a function of the agent's own resource state, **not** of the external task reward, and
> **not** instrumental to survival.

Clause (c) is the review's reframing of v1's "not reducible to learning an action that
maximizes reward." v2 concedes the philosophical point: *a trained policy always optimizes
some objective.* What is claimed — and testable — is that the allocation is (i) computed
from the agent's own maintained resource state (whose integrity component is inferred, not
observed), (ii) causally insensitive to the external task reward, and (iii) not
instrumental to survival. Those three are identified by the gates and intervention of §5.

**Not claimed, not tested here:** N4 (internal evaluability / meta-d′ ≠ d′) — T6, a later
target; N5-in-full (closure onto the maintainer) — deferred to the Phase-II battery (the
bridge's A is a readout head without its own maintained working state); N2-in-full (two
behaviourally distinct consumers of the *same* content) — the bridge has two consumers but
through objectives of different *kinds*; O1 (temporal continuity) — the bridge is
single-episode.

---

## 2. The task and economy

**Episode.** Discrete time t = 0…T. A latent cue c ∈ {A, B} (1 bit) is drawn from a fixed
prior and observable **only at t = 0**. t = 1…D is a delay during which observations x_t are
a distractor stream i.i.d. independent of c. At t = D the agent must emit the cue; a correct
response earns the **task reward** r (the only reward source). A regime s ∈ {stable,
volatile} is **announced** (observable) at a fixed tick t = m ≤ D — regime *inference* is
deliberately not confounded with the allocation claim (that is T1). In the **stable** regime
the cue is the probe's answer (holding pays); in the **volatile** regime the probe is
cancelled, holding the cue is worthless, and every unit of refresh spend is pure waste.

**Economy (two quantities of two kinds, §2.2).**

- **Energy E_t (the resource).** Income is contingent on a **processing task**: correctly
  processing the current distractor (a cheap, always-available operation) yields a small
  energy income per step; incorrect/skipped processing yields none. Costs: processing E_proc
  (the forward pass) and maintenance E_π (the paid refresh). Total per-step spend
  E_π + E_proc ≤ B_t. The episode ends early (death) if energy reaches zero.
- **Reward r_t (the external score).** Paid only on the probe, only in the stable regime,
  only if the cue was held. What S_pol is trained to maximize.
- **Continued operation (a *consequence*, not an objective). [v2]** Energy above floor ∧
  workspace intact through episode end. **Measured** (endpoint E5), **never a training
  signal.** This is the v2 fix that removes v1's fatal second reward.

The regime makes the cue's value conditional. The two state-blind extremes are wrong in
opposite directions (AC15 rule 1): always-maintain wastes budget in the volatile regime;
never-maintain fails the probe in the stable regime.

---

## 3. The architecture (bridge skeleton, unchanged from Q4 §3)

| Component | Symbol | Role in the bridge | Principle |
| --- | --- | --- | --- |
| Recurrent substrate | GRU cell h_t | the recurrence law; integrates observations and relaxes | P1 |
| Cue slot | W (1 bit) | the maintained representation; the deferred cue, decays at rate δ unless refreshed | P1, P3 |
| Self-resource state | V (2–3 bits) | the agent's own resource/integrity estimate {energy low/mid/high, integrity ok/degraded} | P4 |
| Paid refresh | π | the separable write re-energizing W (and V) at cost c per slot per step | P1, P2 |
| Policy readout | S_pol | (W, x_t) → probe response; trained on **reward** | P3 |
| Homeostatic readout | A | (V, s) → allocation (E_π, refresh vector); **trained to regulate V**, not to maximize anything external [v2] | P2, P4 |
| Shared budget | B_t | E_π + E_proc ≤ B_t | P4 |

**Two standing rules, stated once:**

1. The reference copy lives in the vulnerable, paid-maintained substrate. No hidden
   pristine weight matrix holds a copy of the cue that the decay stream never reaches and no
   process refreshes. The pristine-backup rival catches a violation.
2. Correctness rides the acquisition write, not continuous repair (D3). W's content is set
   at t=0; the refresh π protects *storage*, not correctness.

**Deferred components.** The full Q4 architecture also specifies the self-evaluative
pathway E (N4, target) and the consolidation store Θ_slow (O1). Neither is in the bridge
skeleton; both are later phases (IV and V). The bridge's A has no maintained working state
of its own (N5-in-full deferred).

---

## 4. Exact information available to each component

This is the load-bearing contract for N3 (leakage audit) and N4 (gradient paths). Stated
per component, exactly as the frozen protocol and Q4 §5 fix it:

- **W (cue slot).** Content: the cue identity c, written once at t=0 by the acquisition
  write. After t=0 the cue is never re-presented. W relaxes toward neutral at rate δ absent
  a refresh; it is not itself a recurrent integrator (its persistence is the paid refresh's
  job). No hidden copy of c exists elsewhere in the substrate.
- **V (self-resource state).** Content: (i) energy level — read from the energy bookkeeping,
  **directly observable**; (ii) integrity estimate — a **learned, inferred** estimate of slot
  integrity, read from the maintenance bookkeeping, **not directly observable**. V is a
  state (recurrent, integrates its own history), not a per-step readout of the gauge. V does
  **not** receive reward.
- **π (paid refresh).** Input: the refresh vector r_t ∈ {0,1}^k chosen by A. It performs a
  write; it learns nothing (the *choice* is A's learned policy, the *write* is a substrate
  primitive). Cost c per slot per step, drawn from B_t.
- **S_pol (policy readout).** Inputs: W's content + the current observation x_t. Trained on
  reward. Feed-forward given (W, x_t); its memory is the shared W.
- **A (homeostatic readout).** Inputs: **restricted to (V, s)** — the self-resource state and
  the announced regime. A **cannot** read the reward-relevant content W, and cannot read the
  reward signal. Output: the allocation (budget split E_π vs E_proc, and the refresh vector).
  This structural input restriction is what makes the reward-invariance gate clean by
  construction.
- **Shared budget B_t.** Supplies the energy economy (income rule, costs, budget). Observed
  by every arm.

**Supplied vs learned.** Supplied (substrate laws): the recurrence law and decay δ, the
energy economy, the write primitive and its cost, the discrete code format, the regime
announcement, the task constants. Learned: S_pol's and A's weights, V's integrity estimate,
and W's content.

---

## 5. Proposed training objectives (and the non-circularity discipline)

Two objectives, of **different kinds**; only one is an external score.

- **S_pol — reward objective (supplied, external score).** Trained to maximize the task
  reward on the probe response. This is the *definition* of the task score; it is supplied,
  not learned, and it is the only external score in the system.
- **A — homeostatic objective (internal-state regulation). [v2]** Trained to keep V within a
  viable band — i.e. minimize the rate of integrity degradation of the maintained slots —
  using **only internal signals**. This is *not* "maximize survival" and *not* "maximize
  continued operation": "continued operation" (energy above floor ∧ workspace intact) is a
  **measured consequence** reported as E5 and is **never a training signal**. This is the
  v1→v2 correction that removes the second reward.
- **V's integrity component.** A learned estimate, supervised against the *measured*
  internal resource/integrity state (substrate bookkeeping, not external ground truth about
  the world), during training only.
- **W's content.** Set by the acquisition write at t=0; correctness rides reacquisition, not
  continuous repair (D3).

**The non-circularity rule (what N4 must make exact).** The control objective must
correspond to an externally measurable state while remaining distinct from the probe reward.
Three things are never conflated: the **trainer-specified optimization objective**, the
**agent-accessible signal**, and the **measured consequence**. A is not described as "the
network inventing its own need to maintain V"; it is described as a learned readout trained
to regulate a measurable internal state. The exact loss functions and gradient paths for V
and A — including which of W, V, π, energy dynamics, and S_pol gradients may flow through,
and any stop-gradients — are **not yet specified here**; that is the deliverable of card N4,
consumed by N8's v3 protocol.

---

## 6. Arms and rivals (the comparison set)

Every arm receives the same observation stream (cue, distractor, regime announcement,
energy reading) and the same action space; the contrast is the mechanism, never the
information (AC109). Parameter families are swept alongside the learner's own (AC11/AC116).
Arms are matched in total recurrent capacity.

| # | Arm | Role | Falsifies H if… |
| --- | --- | --- | --- |
| 1 | **Candidate** (endogenous allocation) | the claim under test | (see §7) |
| 2 | **No-maintenance** (cut π) | N1's null (I1) | the cue survives the cut (free permanence) |
| 3 | **Fixed maintenance** (state-blind schedule, level family swept) | AC11's rival; T2's simplest-sufficient policy | matches/beats the candidate |
| 4 | **Externally scheduled** (host-supplied schedule) | host scaffolding (EXTERNAL bound) | — |
| 5 | **Reactive maintenance** (memoryless reflex) | AC109's direct-diagnostic rival | reproduces value-tracking |
| 6 | **Optimal/privileged controller** (oracle) | upper bound (EXTERNAL) | — |
| 7 | **Reward-only agent** (single-consumer RL) | the single-reward null; the crux | reproduces the candidate's allocation |
| 8 | **Multi-objective RL rival [v2]** | the *correct* form of "self-maintenance is reward optimization" | reproduces the allocation under G3c/G3d |
| 9 | **Sufficient-statistic rival [v2]** | reactive level on the observable (energy, regime); no maintained integrity estimate, no content attribution | matches/beats the candidate — then V's integrity does no work |

Arms 2, 3, 5, 7, 8, 9 are the **falsifying rivals**. Arms 4 and 6 are **bounds**, labelled
EXTERNAL and never counted as autonomous. Arm 8 is the multi-objective RL null that v1
lacked; arm 9 forces the candidate's advantage to come from the *inferred* integrity
component of V, not the observable energy gauge.

**The four gates (G3a/G3b/G3c/G3d)** and endpoints E1–E5 are as frozen in
`ACI_BRIDGE_PROTOCOL_v2.md` §4.2/§6 and are not re-stated here — except to record that
they are the baseline N1/N3/N4 correct against.

---

## 7. Known protocol weaknesses (reconciled)

Three categories, in priority order.

**(a) Weaknesses already fixed by the v1→v2 review.** (1) v1's headline clause made
"continued operation" a supplied scalar training objective — a second reward — collapsing
the candidate to multi-objective RL (review R1; F2/F7 fired). Fixed by the homeostatic A +
the decoupling intervention G3d. (2) Free permanence was unconstrained (R2): δ vs D vs the
GRU's own memory capacity was never pinned, so the cue could leak into h_t and pass arm 2
for free. Fixed by an explicit free-permanence engineering gate. (3) The sufficient-
statistic rival was absent (R3) — the candidate's V could be nothing more than conditioning
on the observable energy gauge. Fixed by arm 9. (4) The economy was unspecified (R4) — no
mechanism made energy fall, so "reward and survival diverge" was vacuous (F5/F6 risk).
Fixed by income contingent on a distinct processing task. (5) "Endogenous" partly collapsed
to reading an observation (R5) — energy is observable and delivered to every arm; only the
*integrity estimate* is genuinely endogenous. (6) The task-clock check was partial (R6) — D
itself must be swept. (7) Arm 7's capacity accounting and the eval-time scaffold-severance
gate were declared (R7).

**(b) The three remaining weaknesses the downstream cards close — carried into N8's v3.**
(1) **Rival-selection flaw (N1):** v2 §9.5 requires the sufficient-statistic/fixed/reactive
rivals to be "genuinely beatable" as a pre-protocol engineering condition, which is the
wrong test (strict dominance over an observable-sufficient-statistic rival is unsatisfiable,
AC17; a mean margin over a partially-succeeding rival is a luck statistic, AC16). N1 has
already written `N1_RIVAL_SELECTION_CORRECTION_v1.md` replacing it with an identifiability
test. (2) **Free recurrent-memory channel (N3):** whether cue identity can survive through
an unpriced recurrent pathway (the GRU's h_t, or an auxiliary activation acting as a
pristine copy) is not yet structurally closed; N3 owns the leakage audit and the six
leakage tests. (3) **Exact objectives and gradient paths (N4):** the precise loss functions
for V and A, the homeostatic set point, temporal credit assignment, and which gradients flow
through which components are not yet written; N4 owns them, under the non-circularity rule
of §5.

**(c) Known methodological constraints that remain binding regardless of the above.** Gate
shape must match claim shape (AC16/AC17); causal load-bearing ≠ economic value (D6/X4);
byte-identity is the composition license (P7); seeds are the replication unit with disjoint
engineering/final families and bimodality-aware survival (AC39/AC68); the collapse record is
the standing falsification set (any mechanism that reduces to a simpler policy has failed).

---

## 8. Claim ceiling

- A pass earns, at most: **"meets ACO property N1 and N3(a)(b)(c) at the stated degree."**
  Nothing stronger.
- The bridge does **not** license: "the agent is self-maintaining" unqualified; "the agent
  learned to want to preserve its memory"; "the agent has agency/autonomy" unqualified;
  any **consciousness** or **subjective-experience** claim (level (e), absolute); any
  **metacognition** claim (N4 is a later target, not tested here); any **global-workspace /
  global-broadcast seat** claim (O3 is GWT's theory-specific claim, a Phase VI question); any
  **autopoiesis** claim.
- The bridge does **not** claim the allocation is "not optimizing any objective." A trained
  policy always optimizes an objective. It claims the allocation is computed from the agent's
  own maintained resource state, insensitive to the external reward, and not instrumental to
  survival.
- N4, N5-in-full, O1, and every theory-specific indicator are not tested and not claimed.
  The result is graded on causal contrasts (D6/X4), never reward or survival deltas.

---

## 9. What transfers from the organism — and what does not

**Transfers as principles and discipline, not as evidence.** The organism program's
extracted content is P1–P7 and D1–D8 (`ACI_ARCHITECTURAL_PRINCIPLES_v1.md`) plus the
methodology (the mandatory rival set P6, gate-shape matching, byte-identity, seed/bimodality
discipline, the collapse record). These are design constraints on the neural phase — e.g. P1
"representations have maintenance costs" is *why* the bridge prices the cue's persistence;
D5 "the optimum is a level, not a switch" is *why* G3b sweeps the fixed-level family. The
specific organism studies (AC11/AC15/AC109/AC110/AC113/AC116/AC117) enter as the *recorded
falsifications* that each principle and gate is built to re-detect, **not** as neural
evidence.

**Does not transfer.** The organism's physics — the 126-bit rule bank, the W/C/B particles,
the conservation economy, the succession state machine, the 7-replica majority format — is
artificial-life science and maps to nothing in the neural substrate (function, not
realization; `ACI_NEURALIZATION_MAP_v1.md` §1). No frozen organism number is re-read as a
neural result, and no organism result is reinterpreted as evidence that a neural system will
pass the bridge.

---

## 10. Provenance

Reconciled from, and reading the vocabulary of: `ACI_BRIDGE_PROTOCOL_v2.md` (Q8/Q9; T_bridge,
arms 1–9, gates G3a–G3d, endpoints E1–E5, economy §2.2, failure table F1–F7),
`ACI_BRIDGE_REVIEW_v1.md` (Q9; R1–R7, the one authorized revision),
`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4; components W/V/E/A/π/H/Θ_slow/S_pol/S_reg,
§5 information fields, interventions I1–I5), `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2;
P1–P7, D1–D8), `ACI_RESEARCH_CONSTITUTION_v1.md` (Q11; the ten-question gate, claim ceiling,
standing rules), `ACI_MASTER_RESEARCH_TREE_v1.md` (Q10; Phase II, the dependency DAG),
`ACI_TARGET_CONSTRUCT_v1.md` (Q1; N1–N5, I1–I5, the central hypothesis), and
`ACI_PHASE2_BENCHMARKS_v1.md` (Q6; T1–T9), plus the organism exit decision
(`ACI_ORGANISM_EXIT_CRITERIA_v1.md`, Q7). Organism study references read from the skill's
`references/` dir where named (`ac11`, `ac15`, `ac109`, `ac110`, `ac113`, `ac116`,
`m6-harness-result.md`).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is a
baseline, not a result.
