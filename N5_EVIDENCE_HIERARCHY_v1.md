# N5 evidence hierarchy v1 — reward/survival demoted to controls; the maintained-integrity rival contrast is the primary evidence

2026-09-25. Deliverable for the N5 card (t_67f1337c), consumed by N8 (v3
protocol) and read by N6/N7. This document answers the card's question — *what
is the primary discriminating evidence, now that A is structurally denied
reward input and trained for homeostasis?* — by (1) demoting G3c (reward
removal) and G3d (survival decoupling) from headline evidence to mechanistic
controls, (2) naming the rival contrast as the primary discriminating evidence,
and (3) re-mapping the gates and failure table so that success never depends on
behaviour the architecture was structurally forced to exhibit.

This is a **derived design document**. It runs nothing, trains nothing, freezes
nothing, and edits no frozen artifact (runner, protocol, results dir, hash, or
ledger). It is not hashed into any study's `pre_run_snapshot.json`. It reads the
bridge vocabulary from `PHASE2_BASELINE_v1.md` §4–§7, `ACI_BRIDGE_PROTOCOL_v2.md`
§4–§7, and the N1–N4 corrections, and does not re-derive them.

Reading discipline applied throughout. (1) The level-(d)/(e) boundary is
absolute; nothing here is a consciousness claim. (2) This document makes no
empirical claim about T_bridge and no prediction about which arm wins. (3)
"Endogenous," per the review and N4, means "computed from the agent's own
maintained resource state, whose integrity component is inferred not observed"
— it does **not** mean "persists when its objective is removed." That latter
reading is exactly the confusion this card exists to close.

**Disambiguation, stated once.** This card (N5) is a correction card in the
N-series N0–N8, not the ACO property N5. The ACO property "N5-in-full" (closure
onto the maintainer, R → M → R′ with the maintainer's own state in the loop)
is deferred by the bridge (baseline §1, bridge §1) and is untouched here. This
document scopes only the bridge's N3 claim — endogenous allocation.

---

## 0. The one-paragraph answer

The primary discriminating evidence is no longer reward-invariance or
survival-decoupling, and cannot be, because both were made satisfiable *by
construction and by training*. N4 made two facts exact: A's inputs are
restricted to `(V, s)` (so A cannot read reward — N2 §3.2), and A is trained by
`J_A` over the measured integrity `I_t` toward a trainer-supplied set point
`I*` (so A is trained for homeostasis, not reward, not survival — N4 §4).
Consequently "A's E_π is invariant when reward is zeroed" (G3c) and "A keeps
regulating when survival is made irrelevant" (G3d) each partly verify a
*supplied property* of the design — the input restriction and the training
objective respectively — rather than detecting a property the design was
supposed to *earn*. They are **mechanistic controls**: necessary, and their
failure is diagnostic of a wiring or training failure, but their passing is not
evidence of emergent endogenous regulation. The primary discriminating evidence
is the **rival contrast**: given matched raw information and comparable
capacity, does the **maintained internal integrity estimate** — the inferred,
content-blind, paid-maintained component of V — support a maintenance
allocation that improves the candidate's operation relative to **fixed,
reactive, direct same-information, and reward-trained** rivals? That is the
question the claim H actually stakes, and it is the one the gates must grade.

---

## 1. The question, and why v2's ordering no longer holds

### 1.1 The question

The card asks: *what is the primary discriminating evidence, now that A is
structurally denied reward input and trained for homeostasis?* It is a question
about the **ordering** of evidence, not about the arm set or the endpoints. The
v2 protocol lists "the four decisive gates" G3a/G3b/G3c/G3d and says they
"jointly constitute the claim" (v2 §6, E3). N5 corrects that: two of the four
are no longer decisive, because the v1→v2 changes made them pass for a reason
that carries no information about endogeneity.

### 1.2 Two structural facts N4 made exact

1. **A cannot read reward.** A's deployment inputs are restricted to `(V, s)`
   (baseline §4, N2 §3.2). Reward `r_t` reaches S_pol's objective only; it is
   not an input to A, not an input to V, and not a gradient path to either (N4
   §6, the stop-gradient table). A's reward-insensitivity is therefore
   **architectural**: A is insensitive to reward because it has no access to
   it.

2. **A is trained for homeostasis.** A's objective is
   `J_A = −E[ Σ_t γ^t c_homeo(t) ]` with `c_homeo(t) = 1[ I_t ≠ I*(s_t, E_t) ]`
   and a trainer-supplied set point `I*(stable, E≥E_crit) = intact, else
   released` (N4 §4). A is trained to drive the *measured* integrity to the
   set point; "continued operation" is E5, a measured consequence in no loss
   (N4 §5.3). A's survival-independence is therefore **trained**: A was never
   given survival or reward to optimize.

### 1.3 The consequence

A gate that is clean *by construction* is a **control**, not **evidence**. v2
already concedes this for G3c ("this gate is clean by construction — and the
gate verifies the construction survived training," v2 §4.2). N5 draws the
conclusion v2 did not: the same is true of G3d, and therefore neither gate
belongs in the set that *constitutes the claim*. The two gates verify that the
design was realized as specified; they do not detect a property the design had
to earn.

**The decisive test that exposes the ordering error:** both G3c and G3d pass
**trivially for state-blind rivals too.** A fixed schedule (arm 3) is
reward-invariant and survival-decoupled by construction — it responds to
nothing, so of course it does not respond to reward removal or to survival
removal. If a control passes for the fixed-schedule rival exactly as it passes
for the candidate, it cannot be the evidence that distinguishes the candidate
from the fixed schedule. What distinguishes them is the *contrast*: does the
candidate's allocation, driven by the maintained integrity estimate, do
**better** than the fixed schedule in the regime where only the integrity
estimate knows what to do?

---

## 2. The corrected evidence hierarchy

The evidence for the bridge's N3 claim is re-ordered into three tiers. Only
Tier 2 is primary discriminating evidence; Tiers 0–1 are prerequisites and
controls that make Tier 2 interpretable.

| Tier | Content | What it verifies | Evidence of endogeneity? |
| --- | --- | --- | --- |
| 0 | Preconditions (leakage closure, free permanence, economy, identifiability) | the experiment is well-posed | No — prerequisite |
| 1 | Mechanistic controls (G3c reward-invariance, G3d decoupling) | architecture + training objective realized | No — control |
| 2 | **The rival contrast** (fixed, reactive, same-information, reward-trained) | the maintained integrity estimate is causally load-bearing | **Yes — primary** |

### 2.1 Tier 0 — preconditions (not evidence, prerequisites)

The experiment is well-posed only if four things hold, none of which is
evidence of the claim:

1. **Leakage closure (N3).** The cue identity survives through no unpriced
   recurrent pathway; the six leakage tests pass. Without this, N1 (active paid
   persistence) is not identified and everything downstream is confounded.
2. **Free-permanence (E1, N1).** δ and D are set so the cue is unrecoverable
   without the paid refresh, and the GRU-only variant of arm 2 is at chance.
   Without this, maintenance costs nothing and the "paid" claim is empty.
3. **Economy / trade-off (F5/F6).** Holding pays in the stable regime and costs
   in the volatile regime, in the modelled direction. Without this, the
   allocation decision is vacuous (AC11/AC15/AC113).
4. **Identifiability (N1/N6).** The integrity state is distinguishable from the
   permitted observation/history. Without this, the candidate cannot honestly
   claim an internally-estimated integrity component at all (N1 §3.3).

These are the N1/N3/N6 engineering and leakage gates. They are pre-protocol
stops (F5/F6, N3 severity, N1 §3.2), not run-time evidence.

### 2.2 Tier 1 — mechanistic controls (G3c, G3d), scoped

**G3c (reward-removal) verifies the architecture.** Hold V and the energy
economy fixed; zero the probe reward. Prediction: the candidate's E_π is
invariant. **What this verifies:** the input restriction — A reads only
`(V, s)` — survived training with no residual co-adaptation through the shared
substrate (N3 test 5 protects the same property from the content side). **What
it cannot conclude:** that the allocation is endogenously driven. A
reward-invariant allocation is produced equally by the fixed schedule, the
reactive reflex, and the sufficient-statistic rival — all reward-blind. Reward
invariance is a *negative* property (the allocation is not reward-driven); it
says nothing about the *positive* property (the allocation is driven by the
maintained integrity estimate).

**G3d (survival-decoupling) verifies the training objective.** Make survival
irrelevant (remove the death threshold) and zero reward. Prediction: the
candidate's A keeps regulating V at its set point. **What this verifies:** A
actually learned the homeostatic objective — that it was not secretly
instrumental to reward or survival despite the trainer's specification (N4
§4.2). **What it cannot conclude:** that the allocation is endogenously driven.
"Keeps regulating when survival is removed" is exactly what a head trained to
regulate `I_t` toward `I*` does; it is the training objective doing what it was
trained to do, not a network inventing its own need.

**Their failure is still load-bearing — but as a setup failure, not a claim
falsification.** If the *candidate's* E_π collapses under G3c, reward leaked
into A (input restriction violated). If it collapses under G3d, A latched onto
survival (training objective violated). Either means the architecture was not
realized as specified and the Tier-2 contrast is uninterpretable. That is a
**control failure** (§4.2), resolved by fixing the wiring/objective and
re-verifying — not a recorded falsification of H.

### 2.3 Tier 2 — the rival contrast (primary discriminating evidence)

The positive claim — that the allocation is computed from a *maintained,
inferred* integrity estimate, and that this is what makes the allocation good —
is tested only by the contrast with rivals that have the same information but
not the maintained estimate. This is §3.

---

## 3. The primary discriminating evidence, defined exactly

### 3.1 The claim shape

The claim under test, stripped of what the architecture now guarantees, is:

> Given matched raw information and comparable capacity, the **maintained
> internal integrity estimate** — the learned, content-blind, paid-maintained
> integrity component of V — supports a maintenance allocation that improves
> the candidate's operation relative to **fixed**, **reactive**, **direct
> same-information**, and **reward-trained** rivals.

This is clause (c)(i) of H (computed from the agent's own maintained resource
state, whose integrity component is inferred not observed), made load-bearing.
It is the *positive* half of "endogenous regulation." Clauses (c)(ii) and
(c)(iii) — reward-insensitivity and survival-non-instrumentality — are the
*negative* half, and they are now covered by the Tier-1 controls, not by this
contrast.

### 3.2 The contrast (rival classes and their arm mapping)

The four rival classes in the card's definition map to the arm set as follows
(N2 §5.4, baseline §6):

| Rival class | Arms | What it omits (the "contested piece" per N2 §6) |
| --- | --- | --- |
| **Fixed** (state-blind schedule, level family swept) | arm 3 | all state — no regime, energy, or integrity |
| **Reactive** (memoryless reflex) | arm 5 | history and maintained state — no integration, no self-state |
| **Direct same-information** | arm 9 (sufficient-statistic: observable energy/regime only) + arm 10 (P_rb: raw bookkeeping + history, trained, no V slot) | the **maintained inferred integrity estimate** — arm 9 omits the bookkeeping read entirely; arm 10 has the raw bookkeeping and its history but no explicit paid-maintained self-state |
| **Reward-trained** | arm 7 (reward-only RL) + arm 8 (multi-objective RL) | the integrity estimate — they optimize reward/survival instead |

Arms 4 (externally scheduled) and 6 (oracle) remain EXTERNAL bounds, never
counted as autonomous, and are not part of the discriminating contrast.

The hierarchy of the direct same-information rivals matters and is carried
from N1/N2 unchanged: arm 10 (P_rb) is the **strongest** no-explicit-V rival —
recurrent, trained on the same homeostatic objective, reading the raw
bookkeeping and its full history — and is the one whose failure is required
before the *maintained self-state* clause can be credited. Arm 9 is the
memoryless special case that makes G3a's integrity-component reading legible.
Neither may be required to lose at engineering (N1 §3.2); both must be capable
of defeating H at finals (N1 §3.4).

### 3.3 What "improves the candidate's operation" means

The contrast is graded on **allocation quality**, not on reward or survival
deltas (D6/X4, v2 §6). The operation score — pass the probe in the stable
regime when holding pays, and conserve in the volatile/critical regime when
conservation is the right call — is the primary vehicle, with the two parts
reported **separately** and per slot. Two refinements make it honest under this
card's reframing:

1. **The conservation half is graded on the *allocation*, not on survival.**
   "Survives to episode end" is E5 (a measured consequence, never gated) and
   must not be smuggled in as the discriminating metric — A was never trained
   on survival, so "the candidate survived where arm 7 starved" partly restates
   the training objective (a Tier-1 control, §2.2). The discriminating readout
   is the **per-slot allocation decision**: did the candidate release the dead
   cue in the volatile regime and hold the live cue in the stable regime,
   *where the raw observable did not already dictate the answer*?
2. **The causal attribution rides the integrity component, not the gauge.** A
   rival that conditions on the observable energy and regime (arm 9) can
   reproduce any allocation that is a function of the observable alone. The
   candidate's advantage, if any, must come from the *inferred integrity*
   component — the part that is learned from content-blind bookkeeping and
   maintained in a paid slot. This is N2 §6's "internal information matters"
   vs "an explicit maintained self-state is necessary" distinction, now stated
   as the primary contrast.

### 3.4 Gate-shape discipline (N1/AC16/AC17, carried into N7's power plan)

The contrast must be graded so it does not re-import the two gate-shape
failures N1 already ruled out:

1. **No strict dominance over a ceiling-reaching rival (AC17).** Arm 9 and arm
   10 can reach the ceiling, so "candidate > rival on every individual" is
   unsatisfiable by construction. The contrast is not a strict-inequality
   score.
2. **No mean margin over a partially-succeeding rival (AC16).** Arms 9/10
   partially succeed by tracking the observable; a mean margin over them is a
   luck statistic, not a mechanism statistic.
3. **The graded quantity is the causal contrast on the integrity component**
   (the AC109 form: same information, different mechanism, mechanism must do
   causal work). Concretely, the sharpened G3a (§5) and the level-sweep G3b
   (§5) carry the load; the same-information arms (9, 10) are the *causal
   controls* that make those two gates tests of the integrity estimate rather
   than of the observable. N7 specifies the power/resolution for each; N5 fixes
   only the claim shape and the discipline.

---

## 4. What "do not make success depend on forced behaviour" means

### 4.1 The concrete prohibitions

The card's closing constraint — *do NOT make success depend on behaviour the
architecture was structurally forced to exhibit* — forbids, specifically:

1. **G3c must not be a pass gate for the claim.** "The candidate's E_π is
   reward-invariant" is forced by the input restriction; it cannot be scored as
   evidence of endogeneity. It remains a control: its *failure* is a setup
   failure, its *passing* is a prerequisite.
2. **G3d must not be a pass gate for the claim.** "The candidate keeps
   regulating when survival is removed" is forced by the homeostatic training
   objective. Same status as G3c.
3. **E4's conservation direction must not be gated as endogeneity evidence.**
   That the candidate conserves at low energy is partly forced by the
   trainer's set point `I*(stable, E<E_crit) = released` (N4 §4.2). The
   conservation *contrast* (candidate forgoes reward where arms 7/8 chase it)
   is real but is a training-objective readout, a Tier-1 control — report it,
   do not gate it.
4. **No wording may slide a control into a headline.** v3 must not say "the
   four gates jointly constitute the claim" (§6), must not say "G3c/G3d show
   the allocation is endogenous," and must not say "the candidate survived so
   its regulation is endogenously driven."

### 4.2 The control-failure vs claim-falsification distinction

Two failure kinds, now kept apart. This is the single most important
re-mapping N5 hands N8.

| Kind | Fired by | Meaning | Remedy |
| --- | --- | --- | --- |
| **Control failure** | G3c or G3d fails *on the candidate* | reward leaked into A, or A latched onto survival — the architecture/training was not realized as specified | fix the wiring or the objective, re-verify; a pre-protocol stop, not a falsification |
| **Claim falsification** | a Tier-2 rival (3, 5, 7, 8, 9, 10) matches/beats the candidate on the allocation-quality contrast | the maintained integrity estimate does no causal work — the allocation reduces to a level (F1), the observable (F4), or reward/survival (F2) | recorded, never amended (AC16) |

v2's F2 conflated the two: "G3c/G3d fail … or arm 8 reproduces the candidate"
→ "self-maintenance is reward optimization." N5 splits it. G3c/G3d failing on
the candidate is a *setup* failure (the reduction happened in the build, not in
the claim). Arm 8 reproducing the candidate's allocation on the *contrast* — a
reward+survival-trained rival matching the integrity-driven allocation in the
regime where the objectives diverge — is the *claim* falsification (the
multi-objective RL reduction R1, surviving v2's fix). The two have different
remedies and must not share one failure entry.

---

## 5. Re-mapping the gates and the failure table (what v3 writes)

### 5.1 The gates, re-scoped

- **G3c — reward-invariance.** **Demoted to control.** Verifies the input
  restriction survived training. Falsifies nothing on its own; its failure is
  a setup failure (§4.2).
- **G3d — decoupling.** **Demoted to control.** Verifies the homeostatic
  training objective was learned. Falsifies nothing on its own; its failure is
  a setup failure (§4.2).
- **G3a — content-sensitivity, sharpened.** **Primary (with G3b).** The
  perturbation must target the **integrity component** of V, not the observable
  energy gauge (v2 §4.2's note, now made the rule, not a note). Prediction:
  E_π co-varies with the integrity component in the direction it determines,
  *while* the raw bookkeeping delivered to arms 9 and 10 is unchanged — so a
  response the same-information rivals cannot produce is attributable to the
  maintained estimate. Falsified if E_π is invariant to the integrity
  component (a fixed schedule in disguise, F4), or if the same-information
  rivals reproduce the response from the unchanged bookkeeping (the estimate
  carries nothing beyond its raw inputs — N2 §6).
- **G3b — level-sweep dominance.** **Primary (with G3a).** Sweep the fixed
  level family and the candidate's own parameters; the candidate must beat
  every fixed level on the allocation-quality score. Falsified if any level
  matches/beats it (F1, AC11). This is a legitimate dominance claim because a
  level is a single swept parameter, not a partial-success rival (distinct from
  the AC17 prohibition, which targets ceiling-reaching *rivals*).
- **New — the same-information contrast.** The candidate's allocation quality
  is compared against arm 10 (P_rb) and arm 9 (sufficient-statistic) on the
  causal-contrast basis of §3.4, under matched raw information and capacity.
  This is the *strongest* form of the primary evidence: it is where "an
  explicit maintained self-state is necessary" is settled (N2 §6).

### 5.2 The failure table, re-scoped

| Failure | Signature | Reduction | Consequence |
| --- | --- | --- | --- |
| F1 | a fixed duty-cycle level matches/beats the candidate | "optimum is a level, not a switch" (AC11) | no endogenous allocation — clause (b) fails |
| F2 | arm 8 reproduces the candidate's allocation on the contrast (where reward/survival and integrity diverge) | "self-maintenance is reward optimization" (multi-objective RL, R1) | the allocation is not distinguished by being integrity-driven — clause (c)(i) fails |
| F3 | the cue survives arm 2's cut, or the GRU-only variant passes | "free permanence" (N1) | no active persistence — N1 fails |
| F4 | G3a fails: E_π invariant to the integrity component, or arms 9/10 reproduce it | "fixed schedule in disguise" / "internal information, not maintained self-state" | allocation reads the gauge/bookkeeping, not the maintained estimate — clause (c)(i) fails |
| F5 | no regime where maintenance is worth it | "no trade-off exists" | vacuous — pre-protocol stop |
| F6 | per-action economics run opposite to the model | "trade-off direction wrong" (AC113) | economy redesigned — pre-protocol stop |
| F7 | the contrast cannot be made clean (control failures persist) | the redesign condition | the distinction is not identifiable — a new versioned protocol |

Two changes from v2. **First**, the control failures are removed from the
falsification table: "G3c/G3d fail on the candidate" is no longer an F2 entry —
it is a setup failure (§4.2), a pre-protocol stop in the style of N3's leakage
tests, not a run-time falsification of H. **Second**, F4 is widened to carry the
same-information reduction (arms 9/10 reproduce the candidate), so "the
integrity estimate is load-bearing" and "the maintained self-state is
necessary" fail under one entry rather than hiding behind G3a's original
narrow wording.

---

## 6. What this hands N8

N8 writes `ACI_BRIDGE_PROTOCOL_v3.md` (a new file). N5 hands it the following,
each a concrete instruction:

1. **Reorder E3.** Replace "the four gates G3a/G3b/G3c/G3d jointly constitute
   the claim" (v2 §6) with the three-tier hierarchy of §2: G3c/G3d are
   mechanistic controls (Tier 1); G3a (sharpened to the integrity component)
   and G3b (level sweep) plus the same-information contrast (arms 9/10) are the
   primary discriminating evidence (Tier 2).
2. **Scope the controls.** State, in the gate section, that G3c verifies the
   architecture (input restriction) and G3d verifies the training objective
   (homeostasis), and that each is a control whose passing is a prerequisite and
   whose failing is a setup failure (§2.2, §4.2) — never evidence of
   endogeneity, never a claim gate.
3. **Write the primary claim in the contrast form.** Use the card's definition
   verbatim as the headline of the N3 section: given matched raw information and
   comparable capacity, does the maintained internal integrity estimate support
   maintenance allocation that improves operation relative to fixed, reactive,
   direct same-information, and reward-trained rivals?
4. **Add arm 10 (P_rb).** Slot it into the arm table as the strongest
   same-information rival (N2 §5.4), with the non-handicapping clauses (N2
   §5.3) carried into the arm-matching section; keep arm 9 as the memoryless
   special case.
5. **Re-scope the failure table** per §5.2: split F2's control-failure from its
   claim-falsification; widen F4 to carry the same-information reduction.
6. **Do not gate E4's conservation direction or E5's survival as evidence.**
   Report both as behavioural/measured scalars (v2 already treats E5 so; extend
   the same treatment to E4's direction).
7. **Carry the gate-shape discipline** (§3.4) into the endpoint section for N7
   to instantiate with power/resolution: no strict dominance over arms 9/10, no
   mean margin over them, the causal contrast on the integrity component is the
   graded quantity.
8. **Run the consistency audit** against this hierarchy: if, after these
   corrections, the central contrast is still not identifiable, N8 must STOP
   (its own completion condition), not execute an experiment whose central
   contrast is structurally incapable of answering the question.

---

## 7. Claim discipline

- This document makes no empirical claim about T_bridge, no prediction about
  which arm wins, and no claim crossing the level-(d)/(e) boundary.
- "Control" means "verifies a supplied property of the design (input
  restriction, training objective) was realized as specified" — it is
  necessary, its failure is diagnostic, but its passing is not evidence of
  emergence.
- "Primary discriminating evidence" means "the contrast that separates the
  candidate from rivals that omit the maintained integrity estimate while
  retaining the same raw information and comparable capacity."
- "Endogenous" carries its review/N4 meaning — computed from the maintained
  resource state, integrity inferred — and does **not** mean "persists when the
  objective is removed." The latter is the reading G3c/G3d were demoted for
  encouraging.
- No frozen artifact is edited, re-run, or re-hashed. This is a design note
  consumed by N8/N6/N7; `ACI_BRIDGE_PROTOCOL_v2.md` remains the frozen design
  until N8 issues v3 as a new file.

## Sources

Read, not edited: `PHASE2_BASELINE_v1.md` (N0; §1 clause (c), §4 the input
restriction, §6 the arm table, §7(b) weaknesses, §8 claim ceiling),
`ACI_BRIDGE_PROTOCOL_v2.md` (§4.2 the four gates, §6 E3/E4/E5, §7.2 the
failure table), `N1_RIVAL_SELECTION_CORRECTION_v1.md` (identifiability-not-
superiority; §2.3 the arm-9 role; §6 the constitution note), `N2_INPUT_SOURCE_
AUDIT_v1.md` (§3.2 A's inputs, §5 the raw-bookkeeping direct policy P_rb, §6
the maintained-self-state-vs-internal-information distinction), `N3_LEAKAGE_
AUDIT_v1.md` (test 5 protecting G3c's content-blindness), `N4_TRAINING_
OBJECTIVES_v1.md` (§4 the A objective and set point, §6 the gradient table and
its consequence (c), §7 P_rb). Study references from the skill: `ac11`
(level-not-switch), `ac15` (asymmetric intervention / vacuous pass), `ac16`
(mean margin over a partially-succeeding rival), `ac17` (strict dominance
unsatisfiable at the ceiling), `ac109` (non-ignorance: same information,
mechanism must do causal work), `ac113` (trade-off direction), `ac116`
(economically invisible).
