# N2 input-source audit v1 — the six-way information taxonomy + the raw-bookkeeping direct policy

2026-09-25. Deliverable for the N2 card (t_5b805bd2), consumed by N4 (training
objectives and gradient paths) and N6 (analytic identifiability), and by N8 (v3).
This document answers the card's two questions — *does every candidate input have a
classified source, and does the strongest direct rival receive the SAME raw
information?* — by (1) auditing every input to V and A against a six-way source
taxonomy, (2) drawing the complete information-flow diagram, and (3) defining and
strengthening the **raw-bookkeeping direct policy**: a rival that maps the raw
maintenance/bookkeeping information available to V directly into allocation, with no
explicit maintained self-state V.

It is a **derived design document**. It runs nothing, trains nothing, freezes nothing,
and edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is
not hashed into any study's `pre_run_snapshot.json`. It reads the bridge vocabulary
from `PHASE2_BASELINE_v1.md` §4 and `ACI_BRIDGE_PROTOCOL_v2.md` §3 and does not
re-derive them.

Reading discipline applied throughout. (1) The level-(d)/(e) boundary is absolute;
nothing here is a consciousness claim. (2) This document makes no empirical claim
about T_bridge and no prediction about which arm wins. (3) "Same information" is a
statement about the *input interface*, never about the trained outcome (AC109).

---

## 0. The one-paragraph answer

Yes on both questions. **Every** input to V and A — and every input elsewhere in the
bridge — has a classified source, and the six-way taxonomy below assigns each one
exactly. And the strongest direct rival is defined to receive the **same raw
information** as V: the raw-bookkeeping direct policy gets the identical energy
reading, the identical maintenance bookkeeping, the identical regime announcement,
the identical permitted history, and comparable function capacity and training — it
differs from the candidate in exactly one respect, that it does **not** reify any of
that information into an explicit, discrete, paid-maintained self-state V. That
single-respect difference is what makes the rival a clean test of the architectural
necessity of V: if it reproduces candidate behaviour/utility, then what the
experiment has established is "internal information is load-bearing," **not** "an
explicit maintained self-state representation is necessary." Those two claims are
distinct, and the bridge must not let the second inherit credit from the first.

---

## 1. The question and what N2 owns

The card asks: *does every candidate input have a classified source, and does the
strongest direct rival receive the SAME raw information?* Its deliverable is the
input-source audit, the information-flow diagram, and the strengthened rival
definition. N2's scope is the **bridge** (`ACI_BRIDGE_PROTOCOL_v2.md` §3), the frozen
design N4/N6/N8 operate on: six components (GRU h_t, W, V, π, S_pol, A, shared budget
B_t). The full Q4 architecture's extra inputs to A — S_reg's relinquish-vs-maintain
output and E's self-evaluative verdict — are **deferred** (E is N4's target, S_reg is
folded out of the bridge), and N2 flags them only so N4 knows the boundary of what it
must specify now.

N2 does **not** answer whether the raw-bookkeeping rival wins or loses — that is N6's
analytic question and, finally, the empirical run. N2 answers *what the rival is* and
*what information discipline makes it a valid falsifier*. It is the concrete
implementation of N1's identifiability test (§3.3): N1 established *what* must be
shown (identifiability, not superiority); N2 hands back the *rival* that makes the
matched-situations construction non-vacuous.

---

## 2. The six-way source taxonomy

Every quantity that reaches any component's computation is one of exactly six kinds,
classified by **role at the point of consumption** (a single quantity can appear in
different roles at different stages — the audit flags every such case, because a
severed label reappearing as a deployment input is precisely the leak the audit
exists to catch).

1. **Raw environmental observation** — a signal originating outside the agent: the
   distractor stream x_t, the cue c at t=0 (its only presentation), the announced
   regime s, and the probe reward r_t (an external score the environment emits).
2. **Raw internal bookkeeping** — a substrate-measured variable about the agent's own
   computation, directly readable with **no learned transformation**: energy E_t,
   slot-integrity/decay statistics (the maintenance bookkeeping), throughput.
3. **Learned transformation** — the output of a learned mapping: W's belief update,
   V's integrity estimate, the GRU hidden state h_t, S_pol's and A's readouts.
4. **Maintained state** — a discrete state slot whose persistence is the paid refresh
   π's job: W's content, V's content. ("Maintained" names *how it persists*, not
   *where its content came from*.)
5. **Trainer-only supervision** — a label or objective available only during training
   and **severed at evaluation**: the integrity labels I_t, the cause label c (as a
   scaffold for W's belief training), the homeostatic set point / viable band.
6. **Evaluator-only ground truth** — the answer used only to *score*, never present in
   any deployed component's computation: the correct cue c at the probe (from which
   r_t, E1 and E2 are computed).

The classification is by role, so three boundary cases must be stated once:

- **c is triple-role.** Raw environmental observation at t=0 (W's acquisition write);
  trainer-only supervision (the label W's belief inference is trained against);
  evaluator-only ground truth (the probe answer the scorer uses). After t=0, c
  reaches no component as c — only as W's maintained content.
- **r_t is evaluator-derived but raw-in-delivery.** The reward is a function of
  evaluator-only ground truth (correct response vs c), but it is delivered as a raw
  environmental signal — and only to S_pol's training objective. A and V structurally
  never receive it (baseline §4; the reward-invariance gate G3c is clean by this
  construction).
- **The homeostatic set point is trainer-only supervision, not bookkeeping.** A's
  objective — keep V within a viable band — is *defined* by a trainer-supplied target.
  The measured state A regulates *against* is bookkeeping; the *band itself* is a
  supplied training constant.

---

## 3. The audit: every input to V and A, classified

### 3.1 V (self-resource state, 2–3 bits) — content = (energy level, integrity estimate)

| Input | Role in V | Source | Classification |
| --- | --- | --- | --- |
| Energy level E_t | the energy component of V | the energy economy / budget B_t | **raw internal bookkeeping** (directly readable) |
| Maintenance bookkeeping (slot integrity / decay statistics) | the *raw input* to the integrity component | the substrate's own record of W's decay state | **raw internal bookkeeping** |
| V_{t−1} (own prior state) | recurrence: V integrates its own history | workspace slot V | **maintained state** |
| Integrity labels I_t (measured actual slot integrity) | the *training target* of the integrity component | measured substrate bookkeeping, available to the trainer only | **trainer-only supervision** (severed at eval) |

V's **output** v̂ — the integrity estimate — is a **learned transformation** of the
maintenance bookkeeping. The distinction the audit pins down: the *energy* component
is raw bookkeeping re-encoded; the *integrity* component is raw bookkeeping
**transformed by learned weights and then maintained**. The energy component is
near-directly readable; the integrity component is the inferred, not observed, part
(baseline §4, Q4 §5.2). Neither is reward; V does not receive reward.

### 3.2 A (homeostatic readout) — inputs restricted to (V, s)

| Input | Role in A | Source | Classification |
| --- | --- | --- | --- |
| V (the self-resource state, both components) | the content A allocates against | workspace slot V | **maintained state** (whose content is in turn a learned transformation of raw bookkeeping) |
| s (announced regime) | the validity cue that makes the allocation conditional | the environment | **raw environmental observation** |

A's **output** — the allocation (budget split E_π vs E_proc, and the refresh vector
r_t) — is a **learned transformation**. A **cannot** read W (the reward-relevant
content), and **cannot** read the reward signal; this structural input restriction is
what makes G3c (reward-invariance) and G3d (decoupling) clean by construction
(baseline §4, bridge §4.1.3). In the bridge A is a readout head **without** its own
maintained working state (N5-in-full deferred), so there is no A-internal maintained
state to classify here.

### 3.3 The rest of the bridge, for the complete diagram

| Component | Input | Classification |
| --- | --- | --- |
| W (cue slot) | c at t=0, the acquisition write | **raw environmental observation** (one-shot) |
| W (cue slot) | π's refresh (persistence) | **maintained state** (sustained, not re-set) |
| S_pol | W's content | **maintained state** |
| S_pol | x_t | **raw environmental observation** |
| S_pol (training) | r_t | **raw environmental observation** (external score; the only external score in the system) |
| π | r_t (the refresh vector chosen by A) | **learned transformation** (A's decision; π learns nothing of its own) |
| B_t | the energy economy (income rule, costs, budget) | **raw internal bookkeeping** (the substrate law every arm observes) |
| h_t (GRU) | x_t, integrated | **learned transformation** (the recurrence's induced state) |

Training-time supervision (severed at eval, bridge §10 scaffold-severance): the cause
label c for W's belief training and the integrity labels I_t for V — both
**trainer-only supervision**. The homeostatic set point for A is **trainer-only
supervision** (a supplied constant, not a measured state). Evaluator-only ground
truth is the correct cue c at the probe, used to compute r_t, E1 and E2 and never a
deployment input.

---

## 4. The information-flow diagram

Deployment-time flow (solid edges). Training/evaluator layers are drawn separately
because they are severed at evaluation.

```
                          ENVIRONMENT
        x_t (env obs)     c @ t=0 (env obs, one-shot)
             │                    │
             ▼                    ▼
       ┌───────────┐       ┌─────────────┐
       │   S_pol   │◀──W───│  W  (slot)  │
       │ (learned) │       │ (maintained)│
       └─────┬─────┘       └──────▲──────┘
             │ probe response     │ refresh π
             ▼                    │
        r_t (reward,              │
        delivered to S_pol only)  │
                                  │
   ┌──────────────────────────────┼─────────────────────────┐
   │  BOOKKEEPING (substrate-measured, raw)                 │
   │   E_t (energy)      maintenance bookkeeping (slot      │
   │                     integrity / decay statistics)      │
   └───────────┬────────────────────┬───────────────────────┘
               │                    │
               ▼                    ▼
        ┌─────────────────────────────────┐
        │   V  (slot, maintained)         │◀────────────────── s
        │   = (energy, integrity est.)    │
        └────────────────┬────────────────┘
                         │ V
                         ▼
        ┌─────────────────────────────────┐
        │   A  (homeostatic readout)      │◀────────────────── s
        │   inputs RESTRICTED to (V, s)   │
        └────────────────┬────────────────┘
                         │ allocation (E_π, r_t)
                         ▼
        ┌─────────────────────────────────┐
        │   π  (paid refresh, substrate)  │──refresh──▶ W, V
        └─────────────────────────────────┘

        s = announced regime (raw environmental observation)
        E_π + E_proc ≤ B_t   (shared budget: raw internal bookkeeping,
                              observed by every arm)

   TRAINER-ONLY LAYER (severed at eval)
        c ──(label)──▶ W's belief training          (trainer-only supervision)
        I_t ─(label)─▶ V's integrity training        (trainer-only supervision)
        set point/band ─▶ A's homeostatic objective  (trainer-only supervision)

   EVALUATOR-ONLY LAYER (never a deployment input)
        c @ probe ──▶ computes r_t, E1, E2           (evaluator-only ground truth)
```

The diagram makes the two load-bearing facts visible. First, V's **only** deployment
inputs are raw internal bookkeeping (energy, maintenance statistics) plus its own
prior maintained state — the reward and W's content never reach it. Second, A's
**only** deployment inputs are V (maintained state) and s (raw environmental
observation) — the structural restriction that keeps G3c/G3d clean.

---

## 5. The raw-bookkeeping direct policy (the strengthened rival)

### 5.1 Definition

A policy **P_rb** that maps the same current **and historical** maintenance/bookkeeping
information available to V directly into the maintenance allocation (the budget split
E_π vs E_proc and the refresh vector r_t), **without maintaining an explicit self-state
V**. Concretely:

- **Inputs (identical in kind to V's raw inputs).** The energy reading E_t; the raw
  maintenance bookkeeping (the slot-integrity/decay statistics — the *raw statistics
  V's integrity estimate is computed from*, **not** the estimate itself); the announced
  regime s; and the permitted history of all three (the sequences E_{1..t},
  bookkeeping_{1..t}, s_{1..t}).
- **Function capacity.** A recurrent policy (the shared GRU substrate h_t plus a
  readout head of capacity comparable to the candidate's A) — so P_rb is not denied
  history or compute. It introduces **no** discrete bottleneck slot and **no**
  separately paid-maintained self-state: its memory is the ordinary recurrent state
  h_t, exactly the recurrence the candidate also has.
- **Output.** The allocation directly, exactly as A's output — E_π, r_t.
- **Training.** P_rb is **trained**, not hand-coded: on the same homeostatic objective
  (keep the maintained slots' integrity within the viable band), against the same
  measured bookkeeping. "Raw bookkeeping" describes its *inputs*, not that it is
  untrained.

### 5.2 The single respect in which it differs

P_rb differs from the candidate in **exactly one respect**: it does not reify the raw
bookkeeping into an **explicit, discrete, paid-maintained self-state V**. The
candidate's V is (a) a 2–3 bit discrete representation, (b) held in a named slot,
(c) whose persistence is a paid refresh line item (E_π spent on V), (d) that A reads.
P_rb has the same raw information, the same history, the same recurrence, and the same
training — but no named V slot and no paid maintenance of a discrete self-state.

This single-respect difference is the whole point. The claim H is that the allocation
is computed from the agent's *own maintained resource state* (baseline §1, clause
(c)). P_rb concedes every other premise — internal information is available, is
recurrent, is trained on — and contests only whether the *maintained discrete
self-state* is doing work. If P_rb reproduces candidate behaviour/utility, H's
"maintained self-state" clause is falsified; what survives is the weaker claim that
internal bookkeeping matters, which is not the architectural claim the program is
testing.

### 5.3 The non-handicapping discipline (what P_rb MUST and MUST NOT receive)

P_rb **MUST** receive:

1. The **same raw maintenance observations** — the slot-integrity/decay statistics,
   exactly as V reads them (the raw statistics, not the post-estimate).
2. The **same energy observations** — E_t.
3. The **same regime observation** — s.
4. The **full permitted history** — recurrent, so the entire history is available; no
   truncation, no window the candidate's V does not also face.
5. **Comparable function capacity** — matched total recurrent parameters and matched
   optimizer budget against the candidate's V+A path (bridge §5 capacity accounting).
6. **Swept parameters** — any level/threshold/decay the policy uses is swept alongside
   the learner's own (AC11/AC116); no arbitrary fixed threshold.
7. The **same training signal** — the homeostatic objective against the same measured
   bookkeeping; it is not forced to be untrained or hand-wired.

P_rb **MUST NOT** receive:

1. **Hidden ground truth** — not the actual cue c, not the integrity labels I_t, not
   the cause. (The integrity labels are trainer-only supervision, severed at eval, for
   P_rb exactly as for V.)
2. The **reward signal** r_t — the same structural restriction A carries.
3. **W's content** — the reward-relevant cue; A cannot read it, and neither can P_rb.

Clause 2 and 3 keep P_rb's input interface identical to A's *by construction*: P_rb is
"V's raw information, mapped straight through," and V does not see W or reward either.

### 5.4 Where it sits in the arm set

P_rb is a **falsifying rival**, and it is strictly stronger than the two existing
no-explicit-V arms:

- **Arm 5 (reactive, memoryless)** conditions on a transient trigger, no history, no
  content attribution. P_rb has history and training; it subsumes arm 5's family.
- **Arm 9 (sufficient-statistic, memoryless)** conditions the duty cycle on the current
  (energy, regime) only, and does **not** read the maintenance bookkeeping. P_rb reads
  the maintenance bookkeeping and the full history and is trained — it is the
  *strongest* "no explicit V" rival, the one whose failure is actually required before
  the maintained-integrity component can be credited (N1 §2.3: arm 9 exists to make
  G3a a test of self-state; P_rb is the same principle pushed to its honest limit).

The design intent: P_rb replaces "the sufficient-statistic rival" as the *strongest*
direct rival. Arm 9 remains as the memoryless special case (it is the one that makes
G3a's integrity-component interpretation legible); P_rb is added as the recurrent,
trained, bookkeeping-reading rival that must be beaten if "explicit maintained V" is
to be credited. N8 slots P_rb into the v3 arm table (working designation: **arm 10**,
the raw-bookkeeping direct policy).

---

## 6. The distinction the audit enforces

Two claims that the bridge must not conflate:

- **"Internal information matters."** The energy reading, the maintenance bookkeeping,
  and their history carry information about what maintenance to perform, and the
  allocation depends on that information. This is *not* contested by P_rb — P_rb uses
  all of it. It is a claim about the *information*, not the *architecture*.
- **"An explicit maintained self-state representation is necessary."** That the
  allocation must be computed *from a discrete, paid-maintained V slot* — that
  reifying the bookkeeping into a named, paid-persisted self-state buys something that
  mapping the raw bookkeeping history straight into the allocation cannot. This is the
  claim H's clause (c) carries, and it is what P_rb exists to contest.

The gates separate them by construction: G3a (content-sensitivity) only proves the
second claim if the perturbed quantity is the *inferred integrity component of V*, not
the observable energy gauge — and P_rb is the rival that forces that reading, because
P_rb already has the energy gauge, the maintenance bookkeeping, and their history. If
E_π co-varies with V's integrity but P_rb (given the same raw bookkeeping) reproduces
it, then the integrity *estimate* carries no information beyond its raw inputs, and
the explicit V adds nothing — the second claim fails while the first survives.

The discipline for N6, stated once: the raw-bookkeeping rival's recurrent state is a
candidate sufficient statistic of the raw bookkeeping history. N6's question — whether
(time-since-acquisition, time-since-refresh, energy, regime, probe-distance) is a
*compact* sufficient statistic — is the analytic form of "does P_rb's memory collapse
to a small state machine." If N6 finds such a statistic, that state machine becomes the
**strongest** form of P_rb (a hand-verifiable rival, not a weaker one), and it is
**included**, never hidden (N6's own instruction). N2 hands N6 the general rival; N6
returns whether a compact form suffices.

---

## 7. What this hands downstream

- **N4 (training objectives / gradient paths).** The audit's classification is the
  contract N4 must make exact: V's integrity loss supervises against **trainer-only
  supervision** (I_t), severed at eval; A's objective regulates against **raw internal
  bookkeeping** (measured integrity) toward a **trainer-only** set point; no gradient
  may flow reward → A or reward → V (they are not inputs). P_rb's training shares
  A's objective, so N4 specifies both with the same homeostatic loss; the only
  difference N4 must encode is the *absence* of a maintained V slot in P_rb (its
  recurrent state is ordinary h_t, no discrete bottleneck, no separate E_π line item
  on a self-state).
- **N6 (analytic identifiability).** P_rb is the rival whose collapse N6 tests. The
  compact sufficient statistic N6 seeks is a special case of P_rb's memory; if found,
  it is the strongest P_rb and is included as a rival.
- **N8 (v3).** Add P_rb to the arm table (working designation arm 10); keep arm 9 as
  the memoryless sufficient-statistic special case; carry the non-handicapping clauses
  of §5.3 into the arm-matching section; do not let any wording claim "maintained
  self-state is necessary" off a result that only shows "internal information
  matters" (§6).

---

## 8. Claim discipline

- This document makes no empirical claim about T_bridge and no prediction about which
  arm wins. "Same information" is a statement about the input interface, not the
  trained outcome (AC109); "P_rb is the strongest direct rival" is a statement about
  its input set and capacity relative to arms 5 and 9, not a claim that it will win.
- "Necessary" means "the no-V rival provably fails to reproduce the candidate" — a
  final-run, per-gate result (constitution §4), never an engineering precondition
  (N1 §3.2), and never inferred from the weaker "internal information matters."
- No frozen artifact is edited. This is a design note consumed by N4/N6/N8, and it
  does not itself amend the protocol: `ACI_BRIDGE_PROTOCOL_v2.md` remains frozen until
  N8 issues v3 as a new file.

## Sources

Read, not edited: `PHASE2_BASELINE_v1.md` (N0; §4 per-component information, §5
objectives, §6 arms, §7(b) weaknesses), `N1_RIVAL_SELECTION_CORRECTION_v1.md` (N1;
§3.3 identifiability test, §5 the hand-off to N2), `ACI_BRIDGE_PROTOCOL_v2.md`
(§2.2 economy, §3 architecture, §4.1 input restriction, §4.2 gates, §5 arms, §10
scaffold severance), `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4; §4 substrate,
§5.2 V, §5.6 A, §6.2 closure cycle, §7 rival set). Study references from the skill:
`ac11` (level-not-switch; sweep the level family), `ac15` (asymmetric intervention),
`ac16`/`ac17` (gate-shape discipline), `ac109` (non-ignorance: same information),
`ac113` (trade-off direction), `ac116` (sweep parameters alongside the learner's).
The organism-side "same-information rival" pattern (`C4_TASK_DESIGN_v1.md` §8: `raw`
streak vs `binary` vs `binary+imm` strongest-heuristic vs `graded`) is the template
for "strengthen the direct rival to its strongest form rather than a strawman."
