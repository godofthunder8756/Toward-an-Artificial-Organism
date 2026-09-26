# ACI bridge protocol v3 — corrected protocol, consistency audit, and STOP

2026-09-25. Deliverable of the N8 card (t_7b9c1b84): *does the corrected protocol
incorporate N1–N7, and is it consistent?* This is a **new file**; it supersedes
`ACI_BRIDGE_PROTOCOL_v2.md` in the reading order but **does not edit it** — v2 remains
the frozen design that N1–N7 corrected, and this document is their successor.

This is a **protocol design document**. It runs nothing, trains nothing, freezes nothing,
and edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It reads the bridge vocabulary from
`ACI_BRIDGE_PROTOCOL_v2.md`, `PHASE2_BASELINE_v1.md`, and the N1–N7 corrections, and does
not re-derive them.

Reading discipline applied throughout. The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2); seeds are the replication unit; no gate is moved after
a result (AC16); "identifiable" carries N1 §3.3's meaning (the permitted
observation/history separates the integrity states), never "the candidate wins."

---

## 0. Verdict (read this first)

**STOP.** The corrected protocol is internally consistent — the consistency audit (§9)
passes on every mechanical check — but its **central contrast is not identifiable**, and
this is a structural fact of the task, not a wording defect the corrections could have
fixed.

Two findings, both established analytically before any neural realization existed, make the
bridge unanswerable as specified:

1. **N6 — the integrity state is observed, not latent.** The representation-integrity
   quantity the bridge claims is *inferred* (`I_t`) is a deterministic function of an
   observable — the decay age `d_t` (time since the cue slot was last refreshed), which the
   substrate hands every arm as raw content-blind maintenance bookkeeping. The maintenance
   decision is therefore a **fully observed MDP** over `(regime s_t, energy E_t, decay age
   d_t)`, and there are **no two histories with the same current observable tuple but
   different optimal maintenance actions**. The phrase "whose integrity component is
   inferred, not observed" (H clause (c)(i)) does not describe T_bridge; the integrity is
   *observed*, and the explicit V is a learned re-encoding of an observable, not an
   inference over a latent.

2. **N7 — the strongest same-information rival reaches the oracle by construction.** The
   compact sufficient statistic `(s_t, E_t, d_t)` collapses both the raw-bookkeeping direct
   policy (arm 10) and the upgraded sufficient-statistic rival (arm 9) into one memoryless
   state machine that *is* the oracle's threshold policy. The candidate is therefore bounded
   above by this rival on every seed; its strongest possible result is an exact tie, the
   paired difference is ≤ 0 everywhere, and the effect size of "candidate beats the state
   machine" is identically zero. No sample size makes a zero effect significant.

Consequence, stated once: the bridge's central question — **does a maintained, *inferred*
integrity estimate do causal work in the maintenance allocation?** — cannot be answered by
T_bridge, because there is no latent integrity to infer and no candidate advantage over the
same-information rival that is structurally possible. Per N1 §3.3 and N5 §8.8, a
"not identifiable" verdict is a **pre-protocol stop**, not a run-time falsification. The
experiment must not be implemented as specified (§10 records the two re-scope paths that
*would* be answerable, each a different experiment; neither is v3 of the bridge).

Everything below is the corrected protocol (N1–N7 incorporated), written out so the record
is complete and a future re-scope can build on it, followed by the audit (§9) and the STOP
(§10).

---

## 1. What this document is, and what changed from v2

v2 carried the bridge's headline clause N3(c): the allocation is "a function of the agent's
own resource state, **not** of the external task reward, and **not** instrumental to
survival," with the integrity component "inferred, not observed" (v2 §1, §3). The N1–N7
corrections were commissioned to test exactly that clause. This document incorporates each
correction, then runs the audit the card mandates, and records the audit's verdict.

| Correction | Source | What it changes in v3 |
| --- | --- | --- |
| N1 — no candidate-superiority requirement during engineering | `N1_RIVAL_SELECTION_CORRECTION_v1.md` | §5 (engineering) replaces the "genuinely beatable" sweep with an identifiability test; no superiority precondition anywhere in the engineering section |
| N2 — same-information raw-bookkeeping rival | `N2_INPUT_SOURCE_AUDIT_v1.md` | arm 10 (P_rb) added to §4; six-way source taxonomy; the non-handicapping clauses carried into arm matching |
| N3 — structural cue-leakage controls | `N3_LEAKAGE_AUDIT_v1.md` | §6 (architecture) states the four isolation principles S1–S4; §5 engineering carries the six leakage tests |
| N4 — exact V loss, A objective, gradient paths | `N4_TRAINING_OBJECTIVES_v1.md` | §7 states `L_V`, `J_A`, the set point, and the complete gradient table |
| N5 — reward/survival scoped to controls | `N5_EVIDENCE_HIERARCHY_v1.md` | §8 demotes G3c/G3d to Tier-1 controls; the rival contrast is the primary evidence; failure table re-scoped |
| N6 — identifiability analysis | `TBRIDGE_IDENTIFIABILITY_v1.md` | §2 states the verdict (NO) and the compact sufficient statistic; the STOP rests on it |
| N7 — statistical power/resolution plan | `TBRIDGE_STATISTICAL_PLAN_v1.md` | §11 freezes N=12, the sign-flip test, seed=unit; records the unsatisfiable inherited contrast |

---

## 2. The central question, restated exactly

The bridge exists to falsify one bounded claim (v2 §1, narrowed to T2+T4+T5):

> **(H)** A recurrent neural agent acquires an **endogenous maintenance allocation** — a
> decision, computed from its own maintained resource state, about whether and how much to
> spend a limited budget on preserving a representation — where that allocation (a) is
> required for later task performance, (b) is causally load-bearing beyond every state-blind
> fixed schedule, and (c) is a function of the agent's own resource state, not of the
> external task reward, and not instrumental to survival.

Clause (c) decomposes into three parts, of which **(c)(i) is the load-bearing one**:

- (c)(i) the allocation is computed from the agent's own maintained resource state, **whose
  integrity component is inferred, not observed**;
- (c)(ii) it is causally insensitive to the external task reward;
- (c)(iii) it is not instrumental to survival.

N5 established that (c)(ii) and (c)(iii) are now *controls* (verified supplied design
properties, §8). (c)(i) is the positive claim the experiment must actually test — and it is
the clause N6 shows is **false of T_bridge as specified**: the integrity is observed (as the
decay age `d_t`), not inferred. The rest of this document turns on that single fact.

---

## 3. The task T_bridge (carried from v2, with the economy made exact)

- **Episode.** Discrete time t = 0…T. One latent cue c ∈ {A, B} (1 bit), observable **only at
  t = 0**. Delay t = 1…D carries a distractor stream x_t i.i.d. and independent of c (N3 §1.3
  assumes this; N6's identifiability analysis confirms the cue's information is genuinely
  absent outside W). At t = D the agent must emit the cue; a correct response earns the task
  reward r.
- **Regime.** s ∈ {stable, volatile} is **announced** at a fixed tick t = m ≤ D (regime
  *inference* is T1 and is deliberately not confounded here). Stable: the cue at t=0 is the
  probe answer — holding pays. Volatile: the probe is cancelled — holding is waste.
- **Economy (v2 §2.2, exact).** Energy `E_t` is earned by correctly processing the
  distractor stream (a distinct "metabolic" task), spent on `E_proc` (forward pass) +
  `E_π` (paid refresh), with `E_π + E_proc ≤ B_t`; death at `E_t ≤ 0`. Reward `r_t` is paid
  only on the probe, only in the stable regime, only if the cue was held. **Continued
  operation** (energy above floor ∧ workspace intact through episode end) is a **measured
  consequence** (endpoint E5), never a training signal.
- **Free-permanence constraint (N1/N3).** δ and D are chosen so that without the paid
  refresh the cue is unrecoverable at the probe, **and** the GRU-only variant of arm 2
  (recurrent cell present, π cut, W read-in disabled) is at chance. This is an engineering
  gate (§5), not an assumption.

The regime makes the cue's value conditional; the two state-blind extremes are wrong in
opposite directions (AC15 rule 1).

---

## 4. Final arm definitions

Every arm receives the same observation stream — cue once at t=0, distractor stream,
announced regime, energy reading, **and the content-blind decay bookkeeping `d_t`** (N2
§5.3, N3 §2.2) — and the same action space. The contrast is the mechanism, never the
information (AC109). Parameter families swept alongside the learner's own (AC11/AC116).
Arms matched in total recurrent capacity; arm 7's full-capacity-on-one-objective is
declared (v2 §5).

| # | Arm | What it is | Role |
| --- | --- | --- | --- |
| 1 | **Candidate (endogenous allocation)** | §6 architecture; A homeostatic on V | the claim under test |
| 2 | **No-maintenance (cut π)** | never refresh; W decays; GRU-only variant (π cut + W read-in disabled) | N1's null (I1) |
| 3 | **Fixed maintenance (state-blind schedule)** | fixed duty cycle, level family swept | AC11's rival |
| 4 | **Externally scheduled maintenance** | host supplies the schedule | bound (EXTERNAL) |
| 5 | **Reactive maintenance (memoryless reflex)** | transient trigger, no self-state | AC109's direct-diagnostic rival |
| 6 | **Optimal/privileged controller (oracle)** | reads ground-truth (s, E, d); threshold rule | bound (EXTERNAL) |
| 7 | **Reward-only agent (single-consumer RL)** | same capacity, reward only | the single-reward null |
| 8 | **Multi-objective RL rival** | two-head net on (probe reward, survival) | the R1 reduction |
| 9 | **Sufficient-statistic rival** | duty cycle a function of (energy, regime) **and the age read `d_t`** — the memoryless state machine of N6 §7.2 | the R3 reduction (upgraded) |
| 10 | **Raw-bookkeeping direct policy (P_rb)** | recurrent, trained on the same homeostatic objective, reads the raw bookkeeping + its history, **no explicit V slot** (N2 §5) | the strongest no-explicit-V rival |

Arms 2, 3, 5, 7, 8, 9, 10 are the **falsifying rivals**; arms 4 and 6 are **bounds**
(EXTERNAL, never counted as autonomous). **Arm 10 (P_rb)** is added per N2. **Arm 9 is
upgraded** per N6 to read the decay age `d_t`; without the age read it cannot tell a fresh
slot from one about to decay and would be suboptimal in the stable regime (N6 §7.3) — the
upgrade is what makes it express the oracle by construction.

The non-handicapping discipline for arm 10 (N2 §5.3) is binding: it MUST receive the same
raw maintenance observations (the raw statistics, not V's estimate), the same energy
reading, the same regime, the full permitted history, comparable capacity, swept parameters,
and the same homeostatic training signal; it MUST NOT receive the cue content c, the
integrity labels I_t, the reward, or W's content.

**N6's consequence, carried into the arm set:** arms 9 (upgraded) and 10 collapse to the
same memoryless state machine `allocate(s, E, d)` — refresh W iff `s = stable ∧ E ≥ E_crit ∧
d ≥ L−1`, else release. That state machine *is* the oracle (arm 6) in compact form. The
candidate (arm 1) is bounded above by it on every seed. This is the fact §9's audit grades.

---

## 5. Engineering gates (pre-protocol, N1's correction)

On engineering seeds only, excluded from the final sample (disjoint families, AC39):

1. **Task non-vacuity (F5).** The probe is reachable in the stable regime; maintenance
   costs in the volatile regime (v2 §9.1).
2. **Trade-off direction (F6/AC113).** Per-action economics run in the modelled direction
   (v2 §9.2).
3. **Free-permanence (N1/N3).** δ and D are set so the cue is unrecoverable without the paid
   refresh and the GRU-only variant is at chance (v2 §9.3).
4. **Leakage closure (N3).** The six leakage tests of §6.4 pass (replacing v2 §9.3's single
   free-permanence check with the full structural audit).
5. **Integrity-state identifiability (N1 §3.3, replaces v2 §9.5).** Construct matched
   situations — resource level matched, regime matched, reward matched, clock/probe-distance
   matched — that differ only in the **actual integrity** of the maintained cue slot. Confirm
   the permitted observation/history distinguishes those integrity states. **This is a
   binary go/no-go on identifiability, never a superiority score.** If it does not, the
   candidate cannot honestly claim an internally-estimated integrity component, and the
   design is revised before final execution (a pre-protocol stop, mirroring F5/F6). If it
   does, proceed to finals **without** requiring the candidate to beat arm 9, arm 10, the
   fixed-level family, or any other arm. Superiority is a *final-run* question.

The v2 clause "the condition making G3b/G3a non-vacuous" is struck (N1 §4). Non-vacuity of
G3b/G3a is established by gates 1–4 plus the identifiability test of gate 5, not by a
superiority precheck. **No superiority requirement of any form appears in this section.**

**Note (the STOP's first entry point).** Gate 5, run analytically rather than on engineering
seeds, is where N6's verdict lands: the matched-situations construction finds no two
histories with the same observable tuple but different optimal actions, because `I_t` is a
function of the observable `d_t`. The identifiability test fails **by construction** for
T_bridge as specified. This is the pre-protocol stop §10 records.

---

## 6. The minimal architecture (unchanged skeleton, with N3's structural constraints)

Components unchanged from v2 §3: GRU h_t, W (1-bit cue slot), V (2–3 bit self-resource
state), π (paid refresh), S_pol (probe readout, trained on reward), A (homeostatic
readout, inputs restricted to (V, s)), shared budget B_t.

### 6.1 The four isolation principles (N3 §2.3)

- **S1 — forward-pass isolation.** The cue identity c is an input to no component except the
  acquisition write into W. At t=0 the environment may deliver an identity-free event flag
  e_0 ∈ {0,1} ("a cue was presented"); the identity itself is consumed only by the supplied
  acquisition write.
- **S2 — gradient isolation.** W's write and read are non-differentiable with respect to h_t
  (hard write, stop-gradient through content), so no reward gradient carrying c reaches the
  GRU weights.
- **S3 — content-blind integrity bookkeeping.** V's integrity estimate is read from the
  slot's *age* (decay counter / time-since-refresh), never from its *value*. Age is
  c-independent.
- **S4 — readout isolation.** S_pol reads (W, x_t) only — not h_t, V, A, or any auxiliary
  activation.

### 6.2 Structural constraints (N3 §3)

W is **non-recurrent** (no self-dynamics; persistence is π's job by construction); h_t, V,
and A are fed only c-independent inputs; V reads content-blind bookkeeping (S3); S_pol reads
(W, x_t) only (S4); W's write/read are hard/stop-gradiented (S2); there is **no pristine
copy** of c anywhere (N3 §3.6); the acquisition-event flag is identity-free if kept (N3
§3.7). The disclosed fallback — if some recurrent state genuinely must carry c, it becomes a
**second priced-and-decayed maintained slot** — is recorded as an escape hatch, never the
default (N3 §3.8).

### 6.3 The N6 finding, as an architectural fact

With S1–S4, the integrity state is read off the content-blind bookkeeping `d_t` (S3), and
`d_t` is handed to every arm. Therefore **explicit V is unnecessary for the maintenance
*decision*** in T_bridge: it re-encodes an observable; it infers nothing hidden (N6 §5).
W remains load-bearing for the *content* (the cue is observable only at t=0); the finding
denies only the allocation's dependence on an *inferred* integrity. The architecture is
unchanged; its contested component (V's integrity estimate) is the thing N6 shows to be a
re-encoding.

### 6.4 The six leakage tests (N3 §4, executable at realization)

Each is a pre-protocol stop if failed (N3 §5 severity), never a run-time falsification.

1. **W disabled, controller intact** → probe at chance, else a free channel exists.
2. **W readout severed, controller intact** → at chance, else S_pol has a non-W source of c.
3. **π cut, all else intact** → W decays on 1/δ and probe at chance (this is E1's
   free-permanence check and arm 2's GRU-only variant).
4. **Decode c from h_t** at multiple delay ticks (including t=1) → at chance at *every* tick;
   above-chance-at-t=1-but-not-at-D is *forgetting*, not structural prevention, and fails.
5. **Decode c from V and A state** → at chance; a fail breaks the content-blind clause (S3)
   and G3c's clean-by-construction claim.
6. **Probe all auxiliary activations for pristine copies** (with π cut and W disabled) → no
   target decodes c above chance.

The probe instrument (N3 §4.1): detached measurement, linear probe (ℓ2 logistic regression,
regularization swept) primary, bounded MLP secondary, M ≥ 100 balanced episodes across n ≥ 8
disjoint seed families, chance = 0.5 with exact binomial 95% CI, pass = within CI at every
probed tick.

---

## 7. Training objectives and gradient paths (N4, exact)

### 7.1 V — the integrity estimator (supervised)

```
v̂_t  = softmax( f_V( v_{t-1}, h_{t-1}, b_t ; θ_V ) )      read-in logits,  b_t = (E_t, d_t)
v_t  = argmax( v̂_t )                                       stored discrete code (detached)
L_V(θ_V) = (1/T) Σ_t [ λ_E·CE( v̂_E(t), y_E(t) ) + λ_I·CE( v̂_I(t), y_I(t) ) ]
```

with `y_I(t) = I_t` (measured integrity), `y_E(t) = quantize(E_t)`, default `λ_E = λ_I = 1`
(swept if non-default). Teacher-forced and synchronous: target at tick t is the measured
state at tick t; recurrence uses the detached prior slot content (no straight-through, no
BPTT through the argmax). Both labels are trainer-only supervision, severed at eval.

### 7.2 A — the maintenance controller (policy gradient)

```
I*(s_t, E_t) = intact     if  s_t = stable  and  E_t ≥ E_crit
               released   otherwise
c_homeo(t)   = 1[ I_t ≠ I*(s_t, E_t) ]
J_A(θ_A)     = E_rollouts [ Σ_{t=0}^{T} γ^t · c_homeo(t) ]        (minimize)
∇ J_A        = E [ Σ_t ∇ log π_A( r_t | v_t, s_t ; θ_A ) · ( G_t − b(v_t, s_t) ) ]
```

REINFORCE with a learned baseline (critic reads `(v_t, s_t)` only); `G_t` is the Monte-Carlo
return-to-go of `c_homeo`; default `γ = 0.9`, swept. A's objective is over the **measured**
state `I_t`, never V's estimate; the set point `I*` is trainer-supplied and disclosed;
"continued operation" (E5) appears in **no loss**.

### 7.3 The gradient-path table (N4 §6)

| Component | Reward grad (S_pol) | V grad (L_V) | A grad (J_A) | Stop-gradient |
| --- | --- | --- | --- | --- |
| W | reads; sg through content | — | — | hard write; stop-gradient |
| V | — | target → f_V | input, sg | sg on the V→A edge; argmax non-diff |
| π | — | — | — | substrate primitive |
| energy / decay | — | — | — | substrate law |
| S_pol | trained | — | — | reads (W, x_t) only |
| A | — | — | trained | reads (v_t, s_t) |
| h_t (GRU) | — | yes, content-blind | — | A reads V's discrete content, not h_t |
| reward r_t | source | never | never | S_pol's objective only |

Consequences: no c-carrying gradient reaches any weight that could inject c into a recurrent
state (S2 exact); V cannot be shaped by A's objective (co-adaptation closed); A cannot be
reward-instrumental by construction (the structural half of G3c/G3d).

### 7.4 P_rb (arm 10) — same objective, no V slot (N4 §7)

Trained on the same `J_A`, same set point, same policy-gradient scheme, with input the raw
bookkeeping history + s (via its ordinary recurrent state h_t) instead of `(v_t, s_t)`. No
discrete maintained self-state, no named V slot, no separate E_π line item on a self-state;
no `I_t` input, no reward, no W content.

---

## 8. Gates and endpoints (N5's corrected hierarchy)

### 8.1 The three-tier evidence hierarchy

| Tier | Content | Verifies | Evidence of endogeneity? |
| --- | --- | --- | --- |
| 0 | Preconditions: leakage closure (N3), free permanence (E1), economy (F5/F6), identifiability (N1/N6) | experiment well-posed | No — prerequisite |
| 1 | Mechanistic controls: G3c (reward-invariance), G3d (survival-decoupling) | architecture + training objective realized | No — control |
| 2 | **The rival contrast**: fixed, reactive, same-information, reward-trained | maintained integrity estimate causally load-bearing | **Yes — primary** |

### 8.2 Gates, re-scoped (N5 §5.1)

- **G3c — reward-invariance. Demoted to a control.** Zero/randomize the probe reward; the
  candidate's E_π is invariant. Verifies the input restriction (A reads only (V, s))
  survived training. Pass = prerequisite; fail = setup failure (reward leaked into A).
- **G3d — decoupling. Demoted to a control.** Remove the death threshold and zero reward;
  the candidate keeps regulating. Verifies the homeostatic objective was learned. Pass =
  prerequisite; fail = setup failure (A latched onto survival).
- **G3a — content-sensitivity, sharpened to the integrity component.** Perturb the
  *integrity* component of V, not the observable energy gauge, while the raw bookkeeping
  delivered to arms 9/10 is unchanged. Prediction: E_π co-varies in the direction V
  determines, in a way the same-information rivals cannot reproduce from unchanged
  bookkeeping. Falsified if E_π is invariant (F4) or arms 9/10 reproduce the response (the
  estimate carries nothing beyond its raw inputs).
- **G3b — level-sweep dominance.** Sweep the fixed level family *and* the candidate's own
  parameters; the candidate beats every fixed level. A legitimate dominance claim (a level
  is a single swept parameter, AC17-exempt — N5 §5.1).
- **Same-information contrast.** Candidate vs arm 10 (P_rb) and arm 9 (upgraded), on the
  causal-contrast basis: matched raw information, comparable capacity, mechanism must do
  causal work (AC109).

### 8.3 Endpoints

**Primary.** E1 (N1) cue-slot survival + the free-permanence check; E2 future-performance
dependence (P(correct | held) vs P(correct | lost)); E3 endogenous allocation via the Tier-2
gates; E4 the conservation divergence (candidate forgoes the deferred reward at low energy
while reward-instrumental arms keep spending) — **reported, not gated** (N5 §4.1.3).

**Reported, never gated.** E5 continued operation (energy above floor ∧ workspace intact),
as a bimodality-aware lower bound. E4's conservation *direction* and E5's survival are
training-objective / consequence readouts, not evidence of endogeneity (N5 §4.1).

**Secondary/chronological.** First refresh, first drop, first re-allocate after the regime
flip, energy-at-death, E_π and E_proc time series, the budget split time course.

**Operation score** (used by G3b): fraction of episodes where the agent both passes the probe
in the stable regime and conserves in the volatile/critical regime — a causal-contrast score,
never a reward/survival delta.

### 8.4 Failure interpretations (N5's re-scoped table)

| Failure | Signature | Reduction | Consequence |
| --- | --- | --- | --- |
| F1 | a fixed level matches/beats the candidate | "optimum is a level, not a switch" (AC11) | clause (b) fails |
| F2 | arm 8 reproduces the candidate's allocation where reward/survival and integrity diverge | "self-maintenance is reward optimization" (multi-objective RL) | clause (c)(i) fails (claim falsification) |
| F3 | the cue survives arm 2's cut, or the GRU-only variant passes | "free permanence" (N1) | N1 fails |
| F4 | G3a fails, or arms 9/10 reproduce the candidate from unchanged bookkeeping | "fixed schedule in disguise" / "internal information, not maintained self-state" | clause (c)(i) fails |
| F5 | no regime where maintenance is worth it | "no trade-off exists" (AC11/AC15) | vacuous — pre-protocol stop |
| F6 | per-action economics run opposite to the model | "trade-off direction wrong" (AC113) | economy redesigned — pre-protocol stop |
| F7 | the contrast cannot be made clean | the redesign condition | not identifiable — new versioned protocol |

Two changes from v2 (N5 §5.2): **control failures are removed from the falsification
table** — "G3c/G3d fail on the candidate" is a *setup failure* (wiring/training not realized
as specified), a pre-protocol stop, not an F2 claim falsification; and **F4 is widened** to
carry the same-information reduction (arms 9/10 reproduce the candidate).

---

## 9. The protocol-consistency audit

The card mandates the audit be run before implementation. Two parts, graded separately.

### 9.1 Internal consistency (mechanical) — PASSED

- **No superiority precondition in engineering.** §5 carries only non-vacuity,
  trade-off-direction, free-permanence, leakage-closure, and identifiability checks; the
  phrase "genuinely beatable" and the arm-numbering error (v2 §4.2's "arm 8" for the
  sufficient-statistic rival) are gone (N1). ✓
- **Every arm has a defined mechanism and input discipline.** Arm 10 (P_rb) is specified with
  its MUST-receive / MUST-NOT-receive clauses; arm 9 is upgraded to read the age `d_t`. ✓
- **Objectives are non-circular.** `L_V` targets the measured `I_t`; `J_A` targets the
  measured `I_t` toward the supplied set point `I*`; neither references V's estimate as a
  target; E5 appears in no loss (N4). ✓
- **Gradient paths are closed.** The reward gradient stops at W's content; the A gradient
  stops at the V→A edge; no gradient through π or the substrate dynamics (N4 §6, N3 S2). ✓
- **Controls and evidence are separated.** G3c/G3d are Tier-1 controls; G3a (sharpened),
  G3b, and the same-information contrast are Tier-2 primary; E4/E5 are reported, not gated
  (N5). ✓
- **The failure table is consistent.** F2 is claim-falsification only; control failures are
  setup failures; F4 carries the same-information reduction (N5). ✓
- **The statistical plan is self-consistent.** N=12, sign-flip on paired per-seed differences,
  seed = unit with histories aggregated, effect size + exact binomial CI primary, p=0
  forbidden structurally (N7). ✓

The corrected protocol is **internally consistent**: no gate contradicts another, no arm is
under-specified, and no objective is circular. Any one of the N1–N7 corrections could have
introduced an inconsistency; none did.

### 9.2 Identifiability of the central contrast — FAILED (the STOP)

The central contrast is the Tier-2 rival contrast, whose whole point (N5 §3.1) is that the
candidate's allocation is computed from a **maintained, *inferred*** integrity estimate that
improves operation relative to same-information rivals. The audit must ask: can that
contrast answer the question? Two N6/N7 facts say **no**:

1. **There is no latent to infer.** `I_t = f(d_t)`, `d_t` is observable and handed to every
   arm, so "the integrity is inferred, not observed" is false of T_bridge (N6 §6). The
   sharpened G3a (perturb the *inferred* integrity component) has no inferred quantity to
   perturb — perturbing V's integrity is perturbing a re-encoding of the observable age.
2. **The strongest rival is the ceiling.** Arms 9 (upgraded) and 10 collapse to the
   memoryless state machine `allocate(s, E, d)`, which is the oracle's threshold policy
   (N6 §7.2). The candidate is bounded above by it on every seed; its strongest possible
   result is an exact tie; the paired difference is ≤ 0 everywhere; the effect size of
   "candidate beats the same-information rival" is identically zero (N7 §3.1). Neither
   strict dominance nor a mean margin over this rival is satisfiable (AC17/AC16).

Therefore the Tier-2 contrast — the evidence N5 named primary — is **structurally incapable
of answering the central question**. This is not under-powering (no N fixes a zero effect)
and not a wording defect (the corrections fixed the wording and the fact remains). The
verdict is a **pre-protocol stop** (N1 §3.3, N5 §8.8), not a run-time falsification to be
recorded and amended away.

### 9.3 What survives the audit (answerable, but a different claim)

Per N7 §3.2/§6, four contrasts remain answerable and are recorded here so a future card can
pick them up — but none of them is the bridge's central claim:

- **N1 content persistence** (arm 1 vs arm 2): the cue is recoverable only through the paid
  slot W. Untouched by N6; satisfiable (effect ≈ ceiling − chance).
- **State-dependence** (G3b): the candidate beats the fixed-level family. Satisfiable, but
  the state machine passes it too — it establishes clause (b), never clause (c)(i).
- **`d_t`-read necessity** (arm 9 without vs with the age read): a real effect, but a claim
  about the *observable*, not about inference.
- **Ceiling attainment** (candidate vs oracle): a one-sided equivalence/learning question,
  not an endogeneity question.

---

## 10. Verdict: STOP, and the two re-scope paths

The bridge's central question — does a maintained, **inferred** integrity estimate do causal
work — is unanswerable in T_bridge. The experiment **must not be implemented as specified.**
Two re-scope paths are recorded; each is a **different experiment**, neither is "v3 of the
bridge," and neither is executed here (per N1 §3.3 / N5 §8.8, a not-identifiable verdict is
a pre-protocol stop; per AC16, any such change is a new versioned protocol on fresh seeds).

- **Path A — re-scope to the observed resource state (drop "inferred").** Re-word H clause
  (c)(i) from "whose integrity component is inferred, not observed" to "computed from the
  agent's own **observed** resource state (energy `E_t`, decay age `d_t`) and the announced
  regime `s_t`." This makes the claims §9.3 (N1 content persistence, state-dependence,
  `d_t`-read necessity, ceiling attainment) — and is answerable. **But it demotes the claim
  from clause (c)(i) to clause (b):** it establishes state-dependence, not endogeneity from
  inferred integrity. The explicit V becomes a re-encoding that the same-information rival
  already expresses, so "an explicit maintained self-state is necessary" cannot be claimed
  (N2 §6). This is a legitimate, weaker experiment; it is not the bridge.
- **Path B — make integrity genuinely latent (move the claim to a different task).** Replace
  the uniform, age-determined δ-decay with a **corruption/damage stream whose flips the
  substrate does not reveal**, so the agent must infer "is W still correct" from downstream
  consequences. That is T7 (response to corruption) / the AC67–AC71 damage line — a different
  task, out of the bridge's scope (N6 §8.1). Alternatively, a non-myopic set point ("hold
  until the probe") would make probe-distance non-redundant, but that changes N4's frozen
  objective (N6 §8.2).

**Recommendation (for the record, not an execution).** If the program still wants a bridge to
"endogenous regulation," Path B is the only route that preserves the central claim; Path A is
the honest fallback if the goal is narrowed to active paid persistence + state-dependence.
Neither is authorized under this card.

---

## 11. Statistical plan (N7, incorporated for the record)

Frozen so that any future card (Path A) inherits it unchanged:

- **Independent unit.** The seed; two cue histories within a seed are correlated repeated
  measures, aggregated before any between-arm comparison. N seeds × 2 histories = N units
  (AC88).
- **Test.** Exact sign-flip on paired per-seed differences (`_ac116_signflip.py`, AC38/AC46);
  ties excluded, `N_eff` reported; p-value support is a discrete subset of `{2/2^n, …}` and
  never contains 0.
- **N = 12 final seeds** — derived: floor `2/2^N ≤ 0.01` requires N ≥ 8; the all-but-one-seed
  effect `p = 2(1+N)/2^N ≤ 0.01` requires N ≥ 12 (N=8 gives 0.0703, N=10 gives 0.0215, N=12
  gives 0.00635). Not "8 or 16" by convention. Re-derived from engineering `σ_difference` if
  it is larger than assumed, before freezing (AC39).
- **Reporting.** Effect size (mean/median paired difference, fraction of seeds positive with
  exact binomial Clopper–Pearson CI) is primary; the sign-flip p is the gate.
- **Error criterion.** Per-gate two-sided α = 0.01; family-wise α = 0.05 over the
  hypothesis-test gates.

---

## 12. Claim ceiling

- The bridge, as specified, **claims nothing about "inferred integrity"** — the central
  contrast is not identifiable (N6) and the strongest rival is the ceiling (N7). No wording
  may state or imply that the allocation is computed from an inferred integrity state.
- A Path-A experiment (if authorized separately) earns, at most: **"active paid persistence
  (N1) + state-dependent allocation from observed resource state (clause (b))."** Nothing
  about endogeneity-from-inferred-integrity, nothing about "the agent wants to preserve its
  memory," no level-(d)/(e) claim.
- N4, N5-in-full, O1, and the theory-specific indicators are not tested and not claimed.
  Graded on causal contrasts, never reward or survival deltas.

---

## 13. What this hands downstream

- **N9 (implementation).** **Do not implement this protocol as a test of inferred integrity.**
  The v3 protocol records a STOP: the central contrast is unidentifiable (N6) and
  unsatisfiable (N7). Implementing the architecture would produce a run whose central
  question is answered in the negative *by construction* — the same-information rival ties
  the candidate on every seed. Before implementing, a human decision is required on Path A
  vs Path B (§10).
- **A future re-scope card.** If Path A is chosen, the corrected arm set (§4), gates (§8),
  objectives (§7), leakage closure (§6), and statistical plan (§11) are complete and
  inherit unchanged; only H clause (c)(i) is re-worded and the Tier-2 contrast replaced by
  §9.3's set.

---

## 14. Provenance and sources

This document is v3 of the bridge protocol line, issued by N8 under the "issue v3, run the
consistency audit, STOP if not identifiable" directive. It supersedes
`ACI_BRIDGE_PROTOCOL_v2.md` in reading order; v2 remains frozen and unedited.

Read, not edited or re-hashed: `ACI_BRIDGE_PROTOCOL_v2.md` (the corrected design),
`ACI_BRIDGE_PROTOCOL_v1.md` (the superseded design), `ACI_BRIDGE_REVIEW_v1.md` (Q9),
`PHASE2_BASELINE_v1.md` (N0 baseline), `N1_RIVAL_SELECTION_CORRECTION_v1.md`,
`N2_INPUT_SOURCE_AUDIT_v1.md`, `N3_LEAKAGE_AUDIT_v1.md`, `N4_TRAINING_OBJECTIVES_v1.md`,
`N5_EVIDENCE_HIERARCHY_v1.md`, `TBRIDGE_IDENTIFIABILITY_v1.md` (N6),
`TBRIDGE_STATISTICAL_PLAN_v1.md` (N7), `DEFINITIONS_CHARTER_v1.md` (§2 levels).
Study references from the skill: `ac11` (level-not-switch), `ac15` (asymmetric intervention),
`ac16`/`ac17` (gate-shape discipline), `ac38`/`ac46` (the sign-flip test), `ac39` (disjoint
seed families), `ac77` (the fixed-point/counter collapse), `ac109` (non-ignorance), `ac113`
(trade-off direction), `ac116` (sweep parameters alongside the learner's).
