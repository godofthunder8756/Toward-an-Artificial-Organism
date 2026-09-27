# ACI bridge protocol v4 — Path B (latent-integrity) re-design, consistency audit, and documented STOP

2026-09-26. Deliverable of the N8b card (t_ad1b5a7d): *does the v4 protocol
incorporate the Path B re-design, the re-verified identifiability, and the
statistical plan — and is it consistent?* This is a **new file**; it supersedes
`ACI_BRIDGE_PROTOCOL_v3.md` in the reading order but **does not edit it** — v3
remains the frozen protocol that recorded the δ-decay STOP, and this document is
its successor for the Path B re-design.

This is a **protocol design document**. It runs nothing, trains nothing, freezes
nothing, and edits no frozen artifact (runner, protocol, results dir, hash, or
ledger). It is not hashed into any study's `pre_run_snapshot.json`. It reads the
bridge vocabulary from `ACI_BRIDGE_PROTOCOL_v2.md` §2–§4, `ACI_BRIDGE_PROTOCOL_v3.md`
§10, the N1–N7 corrections, `TBRIDGE_IDENTIFIABILITY_v2.md` (N6b), and
`TBRIDGE_STATISTICAL_PLAN_v2.md` (N7b), and does not re-derive them.

Reading discipline applied throughout. The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2); seeds are the replication unit; no gate is moved
after a result (AC16); "identifiable" carries N1 §3.3's meaning (the permitted
observation/history separates the integrity states), never "the candidate wins."

---

## 0. Verdict (read this first)

**STOP — documented.** The v4 protocol cannot be issued as a runnable experiment,
because the re-designed task it would specify — Path B, the unrevealed
corruption-stream replacement for δ-decay — is **not identifiable**, and the
failure is more fundamental than v3's: it is a **well-posedness** failure before it
is an identifiability failure.

Two findings, both established analytically in the predecessor N6b
(`TBRIDGE_IDENTIFIABILITY_v2.md`), and not re-argued here:

1. **No signal (identifiability).** Under the bridge's isolation constraints (cue
   observable only at t=0; distractor i.i.d. and independent of c; W the only record
   of c), W's correctness has **no observable correlate during the delay**. The
   corruption is unobservable in principle, the two-histories contrast has no pair
   with different optimal actions attributable to the latent, and the maintenance DP
   is degenerate — refresh has zero causal effect on probe success.
2. **No action (well-posedness).** The paid refresh π has **no correct content to
   write**: c is unobservable after t=0, and a pristine copy is forbidden by N3 §3.6.
   "Maintain-or-drop" is not a decision the substrate can execute as specified.

Consequence, stated once: the bridge's central question — **does a maintained,
*inferred* integrity estimate do causal work in the maintenance allocation?** — is
unanswerable in the Path B re-design, exactly as it was unanswerable in the δ-decay
design, but now for the deeper reason that the maintenance *action* is undefined.
Per N1 §3.3 and N5 §8.8, a "not identifiable" verdict is a **pre-protocol stop**,
not a run-time falsification. The experiment must not be implemented.

The v4 protocol is therefore carried forward here in the form that matters for the
record — the N1–N7 framework with the Path B re-design applied (§3–§8) — followed by
the consistency audit (§9), the statistical-plan disposition (§10), and the STOP
with the two honest successors (§11). Nothing in §3–§8 is to be read as authorizing
an implementation; it is recorded so a future card can see precisely what the
re-design would have required and why it fails.

---

## 1. What this document is, and what changed from v3

v3 carried the bridge's headline clause N3(c): the allocation is "a function of the
agent's own resource state, not of the external task reward, and not instrumental to
survival," with the integrity component "inferred, not observed." N1–N7 tested that
clause and found the δ-decay slot makes integrity **observed** (`I_t = f(d_t)`), not
inferred; v3 recorded the STOP and named two re-scope paths. The operator chose
**Path B** (2026-09-25): make integrity genuinely latent via an unrevealed
corruption stream, then re-verify identifiability and re-do the statistical plan.
N6b re-verified; N7b followed. This document incorporates both and runs the audit.

| Correction | Source | What it does in v4 |
| --- | --- | --- |
| N1 — no candidate-superiority requirement during engineering | `N1_RIVAL_SELECTION_CORRECTION_v1.md` | §5 carries the identifiability go/no-go, never a superiority precheck |
| N2 — same-information raw-bookkeeping rival | `N2_INPUT_SOURCE_AUDIT_v1.md` | arm 10 (P_rb) carried in §4; non-handicapping clauses stated |
| N3 — structural cue-leakage controls | `N3_LEAKAGE_AUDIT_v1.md` | §6 states S1–S4 and §3.6 (no pristine copy); the leakage tests carried |
| N4 — exact V loss, A objective, gradient paths | `N4_TRAINING_OBJECTIVES_v1.md` | §7 states L_V, J_A, the set point, the gradient table |
| N5 — reward/survival scoped to controls | `N5_EVIDENCE_HIERARCHY_v1.md` | §8 carries the three-tier hierarchy and the re-scoped failure table |
| N6b — re-design + re-verified identifiability | `TBRIDGE_IDENTIFIABILITY_v2.md` | §3 specifies Path B; §9.2 records the NO-GO; the STOP rests on it |
| N7b — statistical plan for the re-design | `TBRIDGE_STATISTICAL_PLAN_v2.md` | §10 records "no plan to write"; N=12 sign-flip plan of v1 does not transfer |

---

## 2. The central question (unchanged)

The bridge exists to falsify one bounded claim (v2 §1, narrowed to T2+T4+T5):

> **(H)** A recurrent neural agent acquires an **endogenous maintenance allocation** —
> a decision, computed from its own maintained resource state, about whether and how
> much to spend a limited budget on preserving a representation — where that
> allocation (a) is required for later task performance, (b) is causally load-bearing
> beyond every state-blind fixed schedule, and (c) is a function of the agent's own
> resource state, not of the external task reward, and not instrumental to survival.

Clause (c)(i) remains the load-bearing part: *the allocation is computed from the
agent's own maintained resource state, whose integrity component is **inferred, not
observed**.* N5 established (c)(ii) and (c)(iii) as controls. (c)(i) is the positive
claim — and it is the clause N6b shows has **no faithful realization in either
regime** (§11).

---

## 3. The re-designed task (Path B spec, from N6b §2)

The re-design is confined to the **decay law** and its **bookkeeping**; everything
else — the cue presented once at t=0, the delay 1…D, the distractor stream, the
announced regime, the energy economy, the paid refresh line item E_π, the arms, the
leakage controls, the identifiability test — is carried unchanged.

| Frozen element (v2/v3) | Re-design (Path B) |
| --- | --- |
| Decay law: W relaxes toward neutral at rate δ (erase, not overwrite) | Corruption law: W's content is **flipped** (A↔B) by a stochastic stream at rate ρ per step; a flip is **sticky** (persists until a repair writes over it) |
| Bookkeeping: substrate hands every arm the decay age `d_t` | Bookkeeping: the substrate does **not** reveal the flips; no age/corruption counter is handed over |
| Integrity `I_t = f(d_t)` (observed) | Integrity `I_t = 1[W_t = c]` (claimed latent) |
| Refresh π = re-energize (reset the age counter; content already correct) | Refresh π = **undefined until specified** (§4 of N6b) |

The sticky-|= model is the AC67–AC71 primitive lifted to the bridge. The intended
consequence (the card's words): the agent must infer "is W still correct" from
downstream consequences — prediction error, agreement signals, maintenance-machinery
bookkeeping — not from a readable age counter.

### 3.1 The observable tuple under Path B

At tick t every arm receives (N2 §5.3, N3 §2.2, minus the removed age counter):
(1) the distractor stream `x_t` (i.i.d., independent of c); (2) the announced regime
`s_t`; (3) the energy reading `E_t`; (4) its own action history (refresh choices,
which determine `E_t` through the economy). **Nothing in this tuple depends on W's
correctness during the delay.** Item 4 is a record of the agent's own actions, not
of the corruption stream. This single observation is the whole identifiability
verdict (§9.2): the re-design removes the one quantity (`d_t`) that made integrity
observable, without supplying any replacement that is observable under N3.

### 3.2 The three signal channels, named and pre-rejected

The re-design names three downstream consequences; N6b §6 examines each against the
bridge's isolation constraints, and none survives as a *content-blind, c-independent*
signal of integrity:

1. **Prediction error** — requires the distractor stream to depend on c, which breaks
   N3 S1 (c enters the GRU's input for free) and changes the task to T1/T7. Its
   sufficient statistic is a scalar counter.
2. **Agreement signals** — redundant replicas give an observable disagreement count,
   but with no retained baseline for "correct," a symmetric A↔B flip is
   information-theoretically invisible; the only reference for "correct" is the very
   content whose retention N3 S1/S2 forbid.
3. **Maintenance-machinery bookkeeping** — if the bookkeeping is an observable
   substrate counter, integrity is again a deterministic function of an observable
   (v1's `d_t` renamed); if it is itself in the corruption stream, it carries no
   information and reduces to §5.1's vacuity.

---

## 4. Arm definitions under Path B (carried forward, with what the re-design breaks)

The v3 arm set (§4) is carried forward in name and mechanism; the re-design changes
two things about it, both recorded because they are the reason the arms no longer
form a contrast:

| # | Arm | Role (carried) | Status under Path B |
| --- | --- | --- | --- |
| 1 | Candidate (endogenous allocation) | the claim under test | refresh primitive undefined (§4 of N6b) |
| 2 | No-maintenance (cut π) | N1's null (I1) | unchanged — trivially well-posed |
| 3 | Fixed maintenance (state-blind schedule) | AC11's rival | refresh primitive undefined |
| 4 | Externally scheduled maintenance | bound (EXTERNAL) | refresh primitive undefined |
| 5 | Reactive maintenance (memoryless reflex) | AC109's rival | refresh primitive undefined |
| 6 | Optimal/privileged controller (oracle) | bound (EXTERNAL) | oracle is degenerate (§9.2.1) |
| 7 | Reward-only agent (single-consumer RL) | the single-reward null | unchanged |
| 8 | Multi-objective RL rival | the R1 reduction | unchanged |
| 9 | Sufficient-statistic rival (read `d_t`) | the R3 reduction | **loses its input**: `d_t` is removed; no informative substitute under N3 |
| 10 | Raw-bookkeeping direct policy (P_rb) | strongest no-explicit-V rival | **loses its input**: same as arm 9 |

Two consequences of the re-design on the arm set, both fatal to the contrast:

- **The refresh primitive is undefined for every maintaining arm (1, 3, 4, 5, 6).**
  Under corruption, "re-energize" preserves the wrong value. Restoring correctness
  requires writing c, and the three sources of c are each blocked: a pristine copy
  (N3 §3.6), re-acquisition (cue observable only at t=0), or majority-restore
  (requires k replicas and a different architecture — §6.2 of N6b). The decision
  problem whose action has no defined effect is not identifiable; it is ill-posed.
- **Arms 9 and 10 lose the input that made them the oracle.** Under δ-decay they read
  `d_t` and become the memoryless state machine `allocate(s, E, d)` — the oracle in
  compact form. Under Path B there is no `d_t`, and no N3-permitted replacement
  carries correctness during the delay. The same-information rival no longer has an
  information channel to collapse onto — the collapse is replaced by vacuity, not
  cured.

The non-handicapping discipline for arm 10 (N2 §5.3) is carried unchanged wherever an
input survives; it is moot for the integrity input, which no longer exists.

---

## 5. Engineering gates (N1, carried forward)

On engineering seeds only, excluded from the final sample (disjoint families, AC39):

1. **Task non-vacuity (F5).** The probe is reachable in the stable regime.
2. **Trade-off direction (F6/AC113).** Per-action economics run in the modelled direction.
3. **Free-permanence (N1/N3).** The cue is unrecoverable without maintenance; the
   GRU-only variant is at chance.
4. **Leakage closure (N3).** The six leakage tests of §6.4 pass.
5. **Integrity-state identifiability (N1 §3.3).** Construct matched situations
   differing only in actual integrity; confirm the permitted observation/history
   distinguishes them. **Binary go/no-go, never a superiority score.**

**No superiority requirement of any form appears in this section** (N1 §4). Gate 5 is
where the STOP lands: run analytically on the re-design, N6b finds the matched
situations do not exist — integrity is absent from the observation, and the
maintenance action is undefined (§9.2). This is a pre-protocol stop, mirroring the
v3 outcome at the next level.

---

## 6. Architecture and isolation principles (N3, carried forward)

Components unchanged from v2 §3: GRU `h_t`, W (1-bit cue slot), V (2–3 bit
self-resource state), π (paid refresh), S_pol (probe readout), A (homeostatic
readout), shared budget B_t. The four isolation principles are unchanged:

- **S1 — forward-pass isolation.** c is an input to no component except the
  acquisition write into W.
- **S2 — gradient isolation.** W's write/read are stop-gradiented with respect to h_t.
- **S3 — content-blind integrity bookkeeping.** V's integrity estimate is read from
  the slot's age, never its value. *(Under Path B this is the principle that breaks:
  there is no age to read, and no c-independent replacement — §9.2.)*
- **S4 — readout isolation.** S_pol reads (W, x_t) only.

Structural constraints (N3 §3) carried unchanged: W non-recurrent; V, A fed only
c-independent inputs; no pristine copy of c anywhere (N3 §3.6); the acquisition-event
flag identity-free if kept. The six leakage tests of §6.4 remain executable and
remain pre-protocol stops if failed — they are the only part of the re-design that is
unaffected by the corruption law.

**The N6b architectural fact.** With S1–S4 honored, the only content-blind quantity
available to V under the δ-decay design was `d_t` (observable). Path B removes `d_t`
and supplies no observable replacement, so V's integrity estimate has **no input from
which to infer integrity**. The explicit V is no longer a re-encoding of an
observable (v3's failure); it is now a slot with nothing to read. This is worse, not
better: it converts a *redundant* component into a *vacuous* one.

---

## 7. Training objectives and gradient paths (N4, carried forward, with the V-loss problem)

The N4 objectives are carried forward verbatim in form:

```
v̂_t  = softmax( f_V( v_{t-1}, h_{t-1}, b_t ; θ_V ) )      b_t = (E_t, d_t)
L_V(θ_V) = (1/T) Σ_t [ λ_E·CE( v̂_E(t), y_E(t) ) + λ_I·CE( v̂_I(t), y_I(t) ) ]
I*(s_t, E_t) = intact if s_t = stable ∧ E_t ≥ E_crit, else released
c_homeo(t) = 1[ I_t ≠ I*(s_t, E_t) ]
J_A(θ_A) = E_rollouts [ Σ_t γ^t · c_homeo(t) ]
∇ J_A = E [ Σ_t ∇ log π_A( r_t | v_t, s_t ; θ_A ) · ( G_t − b(v_t, s_t) ) ]
```

The gradient-path table (N4 §6) is unchanged: no c-carrying gradient reaches a
recurrent state; V cannot be shaped by A's objective; A cannot be reward-instrumental
by construction.

**The Path B problem with L_V.** Under Path B the input `b_t = (E_t, d_t)` has no
`d_t` component, and the target label `y_I(t) = I_t` is **unavailable to the substrate
except at t=0** — after t=0, `I_t = 1[W_t = c]` depends on c, which the substrate
cannot read without retaining a pristine copy (N3 §3.6). So the V supervisor has
**neither an informative input nor a target**. The loss is vacuous: V learns nothing
about integrity because there is no integrity signal to fit. This is the
well-posedness blocker (§9.2.2) expressed in the training objective.

---

## 8. Gates and endpoints (N5, carried forward, with what the re-design breaks)

### 8.1 The three-tier evidence hierarchy (unchanged)

Tier 0 (preconditions), Tier 1 (mechanistic controls G3c/G3d), Tier 2 (**the rival
contrast** — the primary evidence). The Tier-2 contrast is the part the re-design
breaks.

### 8.2 Gates

- **G3c (reward-invariance)** and **G3d (decoupling)** — Tier-1 controls, carried
  unchanged; they verify the architecture, not the claim.
- **G3a (content-sensitivity, sharpened to the integrity component)** — *perturb the
  inferred integrity component of V.* Under Path B there is **no inferred integrity
  component to perturb** (V has no informative input and no target, §7). The gate is
  unexecutable.
- **G3b (level-sweep dominance)** and the **same-information contrast** — carried in
  form, but see §9.2: the contrast has no well-posed action and no latent to grade.

### 8.3 Endpoints

Primary (E1 free-permanence, E2 future-performance dependence, E3 endogenous
allocation via Tier-2, E4 conservation divergence reported-not-gated) and secondary/
chronological endpoints are carried in form. **E3 — the endogenous-allocation
endpoint — has no measurable subject under Path B**: the refresh primitive is
undefined and the DP is degenerate (§9.2.1). E1 and E2 survive (they concern content
persistence, which N6b leaves untouched); E4/E5 remain reported, never gated.

### 8.4 Failure interpretations (carried, re-scoped by the STOP)

| Failure | Signature | Reduction | Status under Path B |
| --- | --- | --- | --- |
| F1 | a fixed level matches/beats the candidate | "optimum is a level" (AC11) | unexecutable — refresh undefined |
| F2 | arm 8 reproduces the candidate | "self-maintenance is reward optimization" | unexecutable — refresh undefined |
| F3 | the cue survives arm 2's cut | "free permanence" (N1) | **unchanged, executable** |
| F4 | G3a fails, or arms 9/10 reproduce the candidate | "internal information, not self-state" | superseded — arms 9/10 have no input to reproduce from |
| F5 | no regime where maintenance is worth it | "no trade-off exists" (AC11/AC15) | **pre-protocol stop — this is where the re-design lands** |
| F6 | per-action economics run opposite to the model | "trade-off direction wrong" (AC113) | pre-protocol stop |
| F7 | the contrast cannot be made clean | the redesign condition | **triggered** — the redesign was made and still not identifiable |

---

## 9. The protocol-consistency audit

The card mandates the audit be run before implementation. Two parts, graded
separately.

### 9.1 Internal consistency (mechanical) — PASSED

- **No superiority precondition in engineering** (§5): only non-vacuity,
  trade-off-direction, free-permanence, leakage-closure, and identifiability checks. ✓
- **Every arm has a defined mechanism** (§4): carried from v3, with the two Path B
  consequences (undefined refresh; arms 9/10 lose their input) stated rather than
  hidden. ✓
- **Objectives are non-circular in form** (§7): `L_V` targets the measured `I_t`;
  `J_A` targets the measured `I_t` toward the supplied set point. The form is intact;
  the *well-posedness* of `L_V` under Path B is the separate failure in §9.2. ✓
- **Gradient paths are closed** (§7): unchanged from N4 §6 / N3 S2. ✓
- **Controls and evidence are separated** (§8): G3c/G3d are Tier-1; the Tier-2
  contrast is primary; E4/E5 reported, not gated. ✓
- **The failure table is consistent** (§8.4): F5 is a pre-protocol stop; F7 is
  triggered by the re-design. ✓

The carried-forward framework is **internally consistent** — the N1–N7 corrections
survive the re-design without introducing a mechanical contradiction. That is not the
question, however: the card asks whether the *protocol* is consistent, and a protocol
whose central contrast is unidentifiable and whose maintenance action is undefined is
not a runnable experiment, however clean its bookkeeping.

### 9.2 Identifiability of the central contrast — FAILED (the STOP)

The audit asks: can the Tier-2 contrast answer the central question? N6b established
**no**, for two independent reasons, the second of which survives even a fix to the
first:

1. **No signal (identifiability).** Under the bridge's isolation constraints, W's
   correctness has no observable correlate during the delay (N6b §6). The corruption
   is unobservable in principle; the two-histories contrast has no pair with
   different optimal actions attributable to the latent; the maintenance DP is
   degenerate — every refresh policy attains the same value, because refresh has zero
   causal effect on probe success (N6b §5.1). The oracle is the **constant** policy;
   there is no state-dependent allocation to discover. This is the AC109/AC113
   trade-off check pushed to its limit: **maintenance buys nothing.**
2. **No action (well-posedness).** The paid refresh has no correct content to write:
   c is unobservable after t=0 and a pristine copy is forbidden (N6b §4).
   "Maintain-or-drop" is not executable by the substrate as specified.

The sufficient-statistic collapse re-test (N6b §7) generalizes the point: wherever
the integrity state is made *inferable*, the inference has a compact observable or
scalar sufficient statistic that a simple rival maintains (a counter, or a memoryless
threshold on a count); wherever it is made genuinely *latent*, the inference has no
evidence and the maintenance action is vacuous. **There is no middle regime in which
integrity is latent, inferable, and a discrete paid-maintained self-state is the
load-bearing mechanism.** The δ-decay slot made integrity observed; the corruption
slot makes it absent or observed-as-damage.

Because both findings are structural facts of the task plus the permitted
information — not wording, not under-powering — the verdict is a **pre-protocol stop**
(N1 §3.3, N5 §8.8), never a run-time falsification and never a gate to move. Per the
card's directive, this document stops here and does not loop into a further redesign.

---

## 10. Statistical plan (N7b — none to write)

N7b's precondition was "conditional on identifiable," and N6b returned NO-GO. The
successor statistical plan (`TBRIDGE_STATISTICAL_PLAN_v2.md`) therefore records that
**there is no plan to write**: with no well-posed contrast there is no primary
contrast to define, no smallest effect worth distinguishing, and no sample size to
derive from engineering variance + minimum meaningful effect + the sign-flip
resolution floor.

The v1 statistical plan (N=12, exact sign-flip on paired per-seed differences, seed =
unit, two histories aggregated, α=0.01 per gate) remains frozen **for the δ-decay
design only** and does **not** transfer to Path B — it was derived from a contrast
that no longer exists. It is not superseded by this STOP; it is simply inapplicable.

---

## 11. Verdict: STOP, and the two honest successors

The bridge's central question — does a maintained, **inferred** integrity estimate do
causal work — is unanswerable in **both** the δ-decay design (v3: integrity observed)
and the Path B re-design (this document: integrity absent, maintenance action
undefined). There is no faithful realization of clause (c)(i): the δ-decay slot makes
integrity observed, and the corruption slot makes it absent or observed-as-damage.

The program's "inferred integrity" ambition, wherever it is honestly testable, is one
of two **different experiments** — neither the bridge:

- **T1 — maintained hidden-state inference over a cause.** The sufficient statistic is
  a scalar counter; the claim ceiling is **N1+N2** (active persistence + content
  load-bearing), never endogenous allocation, never "inferred self-state integrity."
- **T7 — internalized repair of OBSERVED damage.** The corruption regime the
  AC67–AC71 line actually implements: the damage signal is *observed* (a minority
  count computed from the system's own state), and the load-bearing question is *who
  enacts the repair* (system vs host watchdog), not whether integrity is inferred. T7
  does **not require latent integrity**.

Each needs its own card; neither inherits the bridge's clause (c)(i).

**The durable rule (this document's general output, from N6b §9.3).** A
representation's integrity can be (i) **observed** (age counter / damage count), (ii)
**inferred from consequences** (requires the content to be in continuous use against a
content-dependent stream — and the inference's sufficient statistic is a
scalar/counter), or (iii) **absent** (content held in isolation from any observable
consequence). **There is no fourth case in which a discrete paid-maintained self-state
is the load-bearing inference mechanism.** Any future "inferred self-state" claim must
first locate itself in case (ii) and then beat the scalar-integrator rival.

**Operator decision required.** The re-design path is exhausted (N6b NO-GO, N7b no
plan, this v4 STOP). The operator must choose whether to authorize T1 or T7 as a new
card, or drop the "inferred integrity" ambition. N8b and N9 must not proceed to
implementation against a STOP.

---

## 12. Claim ceiling

- The bridge, in either design, **claims nothing about "inferred integrity."** No
  wording may state or imply that the allocation is computed from an inferred
  integrity state.
- A T1 experiment (if authorized separately) earns, at most: **"active paid
  persistence (N1) + content load-bearing (N2)."** Nothing about endogeneity-from-
  inferred-integrity, nothing about "the agent wants to preserve its memory," no
  level-(d)/(e) claim.
- A T7 experiment earns, at most: **"the organism enacts the repair of observed damage
  (observer-discard equivalence, AC95-D4)."** A claim about *who* repairs, never about
  *whether integrity is inferred*.
- N4, N5-in-full, O1, and the theory-specific indicators are not tested and not
  claimed. Graded on causal contrasts, never reward or survival deltas.

---

## 13. What this hands downstream

- **N9 (implementation, t_b8bd3504).** **Do not implement.** Both the v3 protocol and
  this v4 STOP record that the bridge's central contrast is unidentifiable; the v4
  STOP additionally records that the maintenance action is undefined. Implementing the
  Path B architecture would produce a run whose central question is answered in the
  negative *by construction*, and whose maintenance primitive has no defined effect.
  A human decision is required before any implementation: authorize T1 or T7 as a new
  card, or drop the claim.
- **A future T1/T7 card.** The N1–N7 framework (arms §4, leakage §6, objectives §7,
  statistical machinery of `TBRIDGE_STATISTICAL_PLAN_v1.md`) is available as
  starting material, but each successor is a *new* experiment with its own claim
  ceiling and its own identifiability check — neither is "v5 of the bridge."

---

## 14. Provenance and sources

This document is v4 of the bridge protocol line, issued by N8b under the "issue v4,
run the consistency audit, STOP if not identifiable" directive. It supersedes
`ACI_BRIDGE_PROTOCOL_v3.md` in reading order; v3 remains frozen and unedited. It
records a documented STOP; it is not a runnable protocol.

Read, not edited or re-hashed: `ACI_BRIDGE_PROTOCOL_v3.md` (the δ-decay STOP, §10
Path B), `ACI_BRIDGE_PROTOCOL_v2.md` (the corrected design), `TBRIDGE_IDENTIFIABILITY_v2.md`
(N6b; §2 the re-design spec, §4 the refresh-content blocker, §5 the degenerate DP, §6
the three signal channels, §7 the sufficient-statistic collapse, §9 the NO-GO),
`TBRIDGE_STATISTICAL_PLAN_v2.md` (N7b; the "no plan to write" STOP, T1/T7 successors),
`TBRIDGE_IDENTIFIABILITY_v1.md` (N6), `TBRIDGE_STATISTICAL_PLAN_v1.md` (N7),
`N1_RIVAL_SELECTION_CORRECTION_v1.md`, `N2_INPUT_SOURCE_AUDIT_v1.md`,
`N3_LEAKAGE_AUDIT_v1.md`, `N4_TRAINING_OBJECTIVES_v1.md`, `N5_EVIDENCE_HIERARCHY_v1.md`,
`DEFINITIONS_CHARTER_v1.md` (§2 levels).

Study references from the skill: `ac11` (level-not-switch), `ac15` (asymmetric
intervention), `ac16`/`ac17` (gate-shape discipline), `ac38`/`ac46` (the sign-flip
test), `ac39` (disjoint seed families), `ac67`/`ac71` (sticky-|=, read/repair
threshold), `ac77` (fixed-point/counter collapse), `ac95-d4` (observer-discard
equivalence), `ac109` (storage inert where the current observation is decisive),
`ac113` (trade-off direction).
