# Phase-III specialists v1 — three consumers of W that compute genuinely different functions

2026-09-27. Deliverable for the G3 card (t_f60e1f5d): *what ≥2 (prefer 3) specialist
processes need the latent content W for DIFFERENT computations, such that a W
intervention produces different predictable effects on each?* Category B/F — **design /
formalization; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It instantiates the specialist-specific
parts of the generative model that `SHARED_CONTENT_DEFINITION_v1.md` (G1) fixed the
vocabulary of, on the inference task that `PHASE3_INFERENCE_TASK_v1.md` (G2) fixed. It
does **not** design the architecture alternatives (G4); it fixes the *consumers* those
alternatives wire to the same W.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; discrimination and retention are planned-denominator readouts
reported per seed family, never per-family guarantees (AC39/AC68). (3) "Different
function" is the FUNCTIONALLY_DISTINCT criterion of G1 §2.3, made precise below — it is
not "different weights," and two linear heads trained against effectively identical
targets fail it by construction. (4) The baseline's demotions bind: V is removed, A is a
fixed/reactive rule, and this document does not re-introduce either.

---

## 0. The one-paragraph answer

Three specialists consume the *same* maintained W and compute three functions of it that
differ in **objective kind**, **output space**, and **functional form**. **S_pol**
(≡ S_action, the baseline's consumer 1) is the immediate forced-choice decision: it
reads (W, x_t) and emits a direction ẑ ∈ {A, B} — its function of W is the **sign**
(`ẑ = A iff W > 0`). **S_plan** (new, the "prefer 3" third) is a delayed-commitment
stopping controller: it reads W (plus the fixed commitment-cost parameters) and, at every
step, either **commits** to the believed cause or **postpones** for one more token — its
function of W is a **two-sided threshold** (commit-A iff W ≥ +a, commit-B iff W ≤ −b,
else postpone), i.e. it depends on both sign *and* confidence and has a "postpone" region
S_pol lacks. **S_reg** (the baseline's consumer 2, input simplified per G0) is the
retention decision: it reads (W, E, d, s) — the belief plus raw bookkeeping — and emits
**preserve** vs **release**, i.e. whether the belief is still worth paying to hold — its
function of W is **even in W** (`preserve iff |W| ≥ θ(E, d, s)`), a value-of-information
gate whose threshold *moves* with the resource state. The three functions are guaranteed
non-collapsing because they have **distinct invariance signatures**: S_pol is sign-
equivariant (odd), S_plan is sign-and-magnitude dependent, S_reg is sign-invariant
(even). A sign flip changes S_pol and S_plan but not S_reg; a magnitude shrink changes
S_plan and S_reg but not S_pol. Every pair disagrees on at least one canonical W-
perturbation, which is exactly the G1 §2.3 "no collapse" condition stated so it can be
tested.

---

## 1. What "genuinely distinct" means here — and the rival that fails it

The card forbids "two linear heads trained against effectively identical targets." That
phrase names G1's **single-objective collapse** rival (§2.3-d): two readouts that share
one objective (both scalarize the same reward) and therefore co-vary with W identically.
Distinctness is earned, not asserted, on three joints, and all three must hold at once:

1. **Different objective in kind** (G1 §2.3-b.1). The three objectives are an external
   accuracy score, a speed-accuracy-cost tradeoff under a different consequence
   structure, and a resource-economy/continued-operation quantity. They are not three
   scalarizations of one reward; the training signal each consumer is graded against is a
   *different quantity* (§2, "objective kind" field per specialist).
2. **Distinguishable output spaces** (G1 §2.3-b.2). `{A, B}` vs
   `{commit-A, commit-B, postpone}` vs `{preserve, release}`. A consumer's output is not
   another consumer's output re-labelled, and the spaces have different cardinality and
   different semantics (direction, timing, retention).
3. **Non-collapsing functional form** (G1 §2.3-b.2, made sharp in §4). For the *same*
   W-change, the three consumers change in three *different behaviours*, and no pair
   always co-varies. This is guaranteed by construction (distinct invariance classes),
   not hoped for from different random seeds.

**The rival that must fail.** A single reward-maximizing policy with three heads — each
head a linear map of (W, context) to a scalar, all trained against the *same* decision
target (or trivially isomorphic targets, e.g. "choose A vs B" and "don't choose B").
Every head of such a rival is odd-in-W (it flips exactly when the direction flips), so
the whole set co-varies on sign flips and the differential-scramble test (§5) is flat.
The design below fails this rival by giving the three specialists different objective
kinds, different output spaces, and different sign/magnitude sensitivity.

---

## 2. The three specialists

Field schema (matches G1 §1's consumer form S_i : W × U_i → Y_i): role, inputs (the
shared W plus the consumer's own context u_i), the function of W (an explicit decision
rule), objective kind, output space, consequence structure, invariance signature, the
analytic optimum (derived before training, kept as the rival), and the I2 effect. Symbols
S1/S2/S3 are the card's; S_pol/S_plan/S_reg are the repo's.

### 2.1 S1 = S_pol (S_action) — the immediate decision specialist

- **Role.** The baseline's consumer 1; the terminal discriminator. Emits the task
  decision ẑ ∈ {A, B} at t = H ("LEFT/RIGHT").
- **Inputs.** The shared W (the graded scalar log-likelihood ratio S_H, quantized to b
  bits per G2 §4.2) **plus** the current observation x_H — the baseline's `(W, x_t)`.
  In the probe window x_H is neutral (G2 §1.3), so the optimal policy ignores it; it is
  retained for the accumulation phase and for generality, not because the decision needs
  it.
- **Function of W.** The Bayes-optimal rule, already derived in G2 §2.1:
  `ẑ = A iff W > 0`. A **single threshold at 0**; the output is the sign of W. Forced
  choice: every W maps to an action, no abstention.
- **Objective kind.** External accuracy: `r = +1 if ẑ = z else 0` (G2 §1.4). A pure
  discrimination score with no time or cost dimension.
- **Output space.** Y_1 = {A, B} (cardinality 2).
- **Consequence structure.** Symmetric: getting A wrong and getting B wrong cost the
  same; there is no penalty for *when* the decision is made (it is made once, at H).
- **Invariance signature.** **Odd / sign-equivariant.** `S_pol(−W) = flip(S_pol(W))`;
  `S_pol` is invariant to any positive scaling of |W| (a belief of magnitude 0.4 and one
  of magnitude 4.0, same sign, produce the same action).
- **Analytic optimum (rival kept).** The sign rule at threshold 0 — G2's §2.1/§2.2
  scalar accumulator with the posterior-odds threshold. The candidate differs from it
  only in learned-vs-fixed update and shared-maintained-vs-free-broadcast (G2 §4.1),
  never in the function form.
- **I2 effect (scramble W).** In the probe, accuracy → 0.500 (chance) exactly, because
  x_H is neutral and W was the only carrier of z (G2 §3.2). The effect is *total* — this
  is the G2 causal test, run on consumer 1.

### 2.2 S2 = S_plan — the delayed-commitment (stopping) specialist

- **Role.** New consumer (the "prefer 3" third). A sequential stopping controller: at
  each step t it either **commits** to a decision now or **postpones** for one more
  observation, under a *different consequence structure* than S_pol's.
- **Inputs.** The shared W (the running S_t) **plus** the fixed commitment-cost
  parameters (supplied, not learned). It does not read the observation history x_1..x_t
  — W is a sufficient statistic (G2 §2.1), so the posterior and hence the optimal
  stopping rule are functions of W alone. This is the AVAILABLE criterion held: S_plan
  computes from W, not from a replay of the history.
- **Function of W.** A **two-sided threshold (Wald SPRT)**: commit-A iff W ≥ +a,
  commit-B iff W ≤ −b, else postpone, for thresholds a, b > 0 (symmetric default a = b).
  The **postpone region** (−b, +a) is the thing S_pol lacks: at weak beliefs (|W| below
  the boundary) S_pol still forces a direction, while S_plan abstains and pays for one
  more token. The output therefore depends on **both sign and magnitude** of W.
- **Objective kind.** A speed-accuracy-cost tradeoff: committing correctly earns
  `+R_correct` (optionally with an early-commitment bonus), committing incorrectly costs
  `−R_wrong`, postponing costs `−c_obs` per extra token, and never committing by H earns
  the abstain payoff 0. This is *not* a scalarization of S_pol's reward — it introduces a
  cost term and a timing term S_pol's objective has no place for.
- **Output space.** Y_2 = {commit-A, commit-B, postpone} (cardinality 3). The card's
  "postpone vs commit" is this third output; the two commit directions are the sign of W
  *conditioned on* having crossed the boundary.
- **Consequence structure (the "delayed action under a different consequence
  structure").** The commitment is made *now* but its correctness is revealed only at the
  end (z is scored at H); the timing of the action is itself a decision variable with a
  cost, and the payoff is asymmetric across the two commit directions under the
  asymmetric-cost variant (§3.3). Deliberately *different* from S_pol's once-at-H forced
  choice with no cost and symmetric payoff.
- **Invariance signature.** **Sign-and-magnitude dependent.** `S_plan(−W)` flips the
  commit direction (commit-A ↔ commit-B) but *keeps* the commit/postpone status;
  shrinking |W| below the boundary flips commit → postpone without touching the sign.
  S_plan responds to both canonical perturbations.
- **Analytic optimum (rival kept).** The SPRT: for the fixed-cause i.i.d. token stream,
  the optimal stopping rule is exactly this two-threshold form (Wald; the free boundaries
  a, b solve a Bellman equation and are functions of R_correct, R_wrong, c_obs and the
  per-step drift D_KL = 0.288 from G2 §2.3). The *form* is derived before training; the
  numeric boundaries are computed from the cost model at implementation and swept (§7).
  The candidate differs from it only in learned-vs-fixed boundaries and
  shared-maintained-vs-free-broadcast — never in the stop-vs-go structure.
- **I2 effect (scramble W).** At the probe (where W is the only signal), a scrambled W
  drives the commitment rate to ~0 — S_plan postpones forever and lands on the abstain
  payoff — because no confidence survives to cross a boundary. This is a *different*
  predictable effect from S_pol's (whose accuracy collapses to chance but which still
  emits a forced direction).

### 2.3 S3 = S_reg — the retention (value-of-information) specialist

- **Role.** The baseline's consumer 2, input simplified per G0 §3.5 (reads raw
  bookkeeping, not the removed V). Decides whether the represented information remains
  worth preserving.
- **Inputs.** The shared W **plus** the raw bookkeeping `(E, d, s)` — remaining
  maintenance budget E, the age/countdown d of W since last refresh, and the announced
  regime s ∈ {accumulate, probe} (G0 §3.2). These are internal/resource variables, not
  the external reward, and not the removed V.
- **Function of W.** A **value-of-information gate, even in W**: `preserve iff |W| ≥
  θ(E, d, s)`. The value of a belief is its decisiveness, which depends on the posterior
  distance from ½ and hence on |W| only — a strong A-belief and a strong B-belief are
  equally worth keeping (equally decisive), and a weak belief is not worth its refresh
  cost. The threshold θ moves with the resource state: it *rises* as E falls (scarcer
  budget → require more confidence before paying), and it *falls* in the probe (s =
  probe, where W is the only discriminator and hence more valuable). The dependence on W
  is through its **magnitude alone**.
- **Objective kind.** Continued operation / resource economy: maximize energy-above-floor
  and workspace integrity through episode end (G0 §3.5, the baseline's supplied
  continued-operation objective), *not* task reward. This is a different *kind* of
  objective from S_pol's accuracy and S_plan's tradeoff — it is about the system's own
  upkeep, not the external decision.
- **Output space.** Y_3 = {preserve, release} (cardinality 2, different semantics from
  S_pol's {A, B}).
- **Consequence structure.** Preserve pays the refresh cost c and holds W for another
  step; release stops paying and lets W decay on timescale 1/δ (G1 §2.5). The consequence
  is realized in the *availability* of W downstream, not in any immediate external score.
- **Invariance signature.** **Even / sign-invariant.** `S_reg(−W) = S_reg(W)`
  (a direction flip never changes a retention decision); S_reg is maximally sensitive to
  |W| crossing θ. This is the property that makes S_reg non-collapsing with S_pol (odd)
  and S_plan (sign-dependent).
- **Analytic optimum (rival kept).** The threshold rule `preserve iff |W| ≥ θ(E, d, s)`
  with θ the value-of-information boundary derived from the cost model (refresh cost c,
  decay rate δ, remaining horizon, budget E). The *form* (even threshold, monotone
  directions) is derived before training; the numeric θ is computed at implementation and
  swept (§7). Per verdict D, a fixed/reactive θ is ALLOWED — the baseline does not assume
  a learned adaptive θ.
- **I2 effect (scramble W).** A scrambled W (magnitude collapsed toward 0) drives the
  decision to **release** — no confidence survives to clear θ. This is a *third*,
  different predictable effect: S_pol's accuracy → chance (but still acts), S_plan's
  commitment → abstain, S_reg's retention → release.

---

## 3. The KEY REQUIREMENT table, and how each specialist differs for the same W

### 3.1 The requirement table (symmetric default)

The card's requirement is that the same W produces three outputs in three different
spaces, and that each specialist changes with W. The symmetric default of §2:

| W (belief) | S1 = S_pol | S2 = S_plan | S3 = S_reg |
| --- | --- | --- | --- |
| belief(z=A), strong (W = +large) | **LEFT** (A) | **commit-A** | **preserve** |
| belief(z=B), strong (W = −large) | **RIGHT** (B) | **commit-B** | **preserve** |
| belief ≈ 0 (uninformative) | chance (forced choice) | **postpone** | **release** |

Three different output kinds (direction / timing / retention) change *differently* as W
moves. The card's exact column entries are an illustration of "different outputs," not a
hard constraint on the sign-asymmetry; §3.3 shows how the literal A→postpone / B→commit
and A→preserve / B→release reading is realized if a sign-asymmetric consequence structure
is wanted.

### 3.2 The non-collapse signature (the two canonical W-perturbations)

The strongest form of G1 §2.3-b.2 — "the two outputs do not always co-vary" — is checked
by two canonical perturbations of W, each holding every other input fixed:

| Perturbation | S_pol (odd) | S_plan (sign+mag) | S_reg (even) |
| --- | --- | --- | --- |
| **Sign flip** W → −W | flips A↔B | flips commit-A↔commit-B | **unchanged** |
| **Magnitude shrink** W → W/2 (same sign) | **unchanged** | may flip commit→postpone | may flip preserve→release |

- S_pol vs S_reg disagree on the sign flip (one flips, one is invariant).
- S_pol vs S_plan disagree on the magnitude shrink (one is invariant, one may flip).
- S_plan vs S_reg disagree on the sign flip (one flips, one is invariant).

Every pair disagrees on at least one canonical perturbation; no two specialists co-vary
everywhere. This is the formal, testable guarantee that the three are genuinely distinct
functions, not three heads on one signal. The two-linear-heads rival fails it outright
(all its heads are odd and co-vary on sign flips).

### 3.3 The asymmetric-consequence variant (realizes the card's literal mapping)

The card's literal "W=belief(A) → S2 postpones, S3 preserves; W=belief(B) → S2 commits,
S3 releases" is realizable by making the *consequence structure* sign-
asymmetric, which is the honest place such an asymmetry can live (it is a property of the
task's payoff, not of the representation):

- Make committing to A risky when wrong (large R_wrong^A) and committing to B cheap
  (small R_wrong^B). Then the SPRT boundary for A is farther out than for B (a > b), so a
  *moderate* A-belief falls in the postpone region while the equally-moderate B-belief
  crosses b → S_plan literally postpones on A and commits on B.
- Give the retained belief asymmetric downstream value (an A-belief will be acted on with
  high stakes, a B-belief with low stakes). Then θ is lower on the A side, so S_reg
  preserves A-beliefs and releases B-beliefs at the same magnitude.

**Both variants are documented; the symmetric default (§3.1) is the non-collapse
anchor.** The asymmetric variant makes S_plan and S_reg *co-vary on sign* (both respond
to the A/B axis), which weakens the §3.2 signature (S_plan vs S_reg no longer disagree on
the sign flip); it must therefore be adopted deliberately, with the §3.2 check re-run and
reported, never as a default. The symmetric default keeps the three invariance classes
cleanly separated and is what v1 specifies.

---

## 4. The anti-collapse guarantee, stated as three invariance classes

The design's core move is to pin "different function of W" to **different behaviour under
W's two symmetry axes** — sign and magnitude. This is stronger than "different
objectives" alone: two consumers can optimize different objectives and still co-vary (two
scalarizations of the same direction signal), but two consumers with different
sign/magnitude sensitivity cannot be the same function regardless of objective.

- **S_pol is odd** (sign-equivariant): its output is the direction, so it is invariant to
  magnitude and equivariant to sign.
- **S_plan is sign-and-magnitude dependent**: its output has a middle "postpone" region,
  so it depends on magnitude (crossing the boundary) and sign (which boundary).
- **S_reg is even** (sign-invariant): its output is retention value, so it is invariant
  to sign and sensitive to magnitude.

These three classes are pairwise distinct, so the three functions are pairwise
distinct — the FUNCTIONALLY_DISTINCT condition (G1 §2.3) is satisfied by construction,
and the single-objective-collapse rival is excluded because it occupies only the odd
class. No two of the three can be replaced by one linear head without changing the set of
W-perturbations the system responds to.

---

## 5. The W intervention produces three different, predictable effects (I2), and I1

The card asks that "a W intervention produces different predictable effects on each."
The differential-scramble test (I2, G1 §2.2/§2.3 — scramble W only, holding every
sensor and every other input fixed) delivers exactly that, and each effect is *predicted
by the specialist's function of W* before the run:

| Intervention | S_pol | S_plan | S_reg |
| --- | --- | --- | --- |
| I2 — scramble W (probe) | accuracy → 0.500 (chance); still emits a forced direction | commitment rate → ~0 (abstain/postpone); payoff → 0 | preserve → release (no confidence clears θ) |
| I2 — scramble W (accumulation, then restore) | direction follows the (wrong) scrambled W | commit decisions follow the (wrong) scrambled W | retention follows the (wrong) scrambled W's magnitude |

The three effects are distinct *behaviours* (direction, timing, retention), each in a
different output space, each predicted from the specialist's rule in §2. This is the
operational content of "different predictable effects on each."

- **I1 — cut π's refresh of W** (G1 §2.5): W decays on 1/δ, and the *co-decay* is
  likewise three distinct behaviours — S_pol's probe accuracy falls to chance, S_plan's
  commitment rate falls to abstention, S_reg's decision flips to release (its own value
  gate sees |W| decay below θ). I1 pins that W is paid-maintained and that all three
  consumers ride the *same* maintained W; I2 pins that each consumes it *differently*.
- **Shared and available, both held.** All three read the one W slot (SHARED — a single
  write reaches all three, G1 §2.1) and none re-derives the history (AVAILABLE — severing
  the history channel leaves each output unchanged, because S_pol uses W+x_t, S_plan uses
  W+cost-params, S_reg uses W+bookkeeping; none reads x_1..x_t, G1 §2.4).

---

## 6. Consistency checks a runner must assert (pre-declared gates)

These are the minimal assertions that distinguish "three genuinely distinct consumers"
from "one policy with three heads." Each is pre-declared, and none may be amended after
seeing results (AC16/17 discipline).

1. **Three distinct invariance classes (the anti-collapse gate).** On a fixed seed
   family, measure the sign-flip and magnitude-shrink response matrices of §3.2. Assert:
   S_pol is sign-equivariant and magnitude-invariant; S_plan responds to both; S_reg is
   sign-invariant and magnitude-sensitive — up to the finite-sample resolution. A failure
   (e.g. S_reg co-varying with S_pol on sign flips) is a falsification of the design, not
   a tuning miss.
2. **The two-linear-heads rival fails the differential-scramble test.** A three-head
   policy trained against the same decision target must show flat (co-varying) I2
   responses where the candidate shows the three distinct §5 effects. This is the rival
   the card names, stated so it can lose.
3. **Each specialist's analytic optimum is kept as a co-equal rival.** sign(W) for S_pol,
   the SPRT for S_plan, the even threshold for S_reg (§2). The candidate differs from
   each only in learned-vs-fixed and shared-maintained-vs-broadcast — never in function
   form (G2 §4.1, per specialist).
4. **Per-consumer causal test, one at a time.** Scramble W and hold that consumer's other
   inputs fixed; that consumer's output must change (CAUSAL, G1 §2.2). Run per consumer,
   not pooled.
5. **Sever-the-history test per consumer.** Hold W and the consumer's context fixed and
   remove access to x_1..x_t; output unchanged (AVAILABLE, G1 §2.4). A consumer whose
   output degrades was re-inferring from the history, not reading W.
6. **Single-write reaches all three.** One write to the one W slot changes all three
   consumers' inputs (SHARED, G1 §2.1); two independent writes to reach all three would
   mean duplicated content.

---

## 7. Parameters (concrete defaults, swept as level families)

| Parameter | Symbol | Default | Swept / note |
| --- | --- | --- | --- |
| Number of specialists | n | 3 | minimal pair (S_pol, S_reg) per G0; S_plan is the "prefer 3" third |
| S_pol threshold | θ_pol | 0 (posterior-odds) | fixed (G2 §6) |
| S_plan thresholds | a, b | a = b (symmetric) | swept with the cost model; asymmetric under §3.3 |
| S_plan payoffs | R_correct, R_wrong, c_obs | computed at impl. | swept as level families |
| S_reg threshold | θ(E, d, s) | fixed/reactive form | swept; learned adaptive θ NOT assumed (verdict D) |
| Refresh cost / decay | c, δ | computed at impl. | from G1 §2.5 / G0 §3.6 |
| Bookkeeping | E, d, s | budget, age, regime | supplied (G0 §3.2); s ∈ {accumulate, probe} |
| W quantization | b | 5 bits | swept; rival at same b (G2 §4.2) |
| Seeds | — | disjoint eng/finals families | AC39: per-family, never mixed |

The analytic optima (§2) are computed from the same cost model before training, exactly
as G2 derived the decision threshold and the Bayes ceiling. No specialist enriches W
beyond the b-bit sufficient statistic (D2/P5): the distinctness is in the *functions of
W*, not in giving each consumer a richer private representation.

---

## 8. Scope, claim ceiling, and what this does NOT claim

- **Claim ceiling.** A Phase-III pass earns, at most: **"one maintained representation's
  content is available to two-or-more objective-distinct modules that need different
  information and drive different behaviour — N2 at the stated degree."** The third
  specialist strengthens the FUNCTIONALLY_DISTINCT evidence (three-way non-collapse is a
  stronger test than two-way) but does not raise the ceiling; it is still N2, not a new
  property.
- **S_reg's retention decision is a consumer output, not a maintenance controller.** The
  baseline (G0 §3.3) simplified the *mechanism* A to a fixed/reactive rule, per verdict
  D. This document keeps that: S_reg's preserve/release is a genuine function of W and is
  measured as a readout that must track W (§2.3, gate 1), but whether that decision
  *gates* π is the allocation question (T4 / verdict D), which N2 does **not** test.
  Wiring S_reg's decision to π would re-open D and require the fixed-schedule rival
  (AC11/116 discipline); v1 does not do it, and does not claim "the organism learns to
  allocate maintenance."
- **S_plan is a G3-authorized task extension.** G2 fixed the inference problem (cause,
  likelihood, probe, the forced decision). G3 adds S_plan's commitment action and
  consequence structure *over the same token stream* — a new action space and objective,
  not a re-litigation of the inference problem. This is disclosed as a design extension,
  and the token stream is unaffected by S_plan's choices (postponing reveals the next
  token; it does not re-draw it).
- **Not claimed:** that the specialists are "modules" in any biological sense; that the
  three behaviours are realized in separated anatomy (they are functions of the same
  maintained W, which is the point); that any consumer is conscious of its use of W
  (N4/T6 is a later target); any claim crossing the level-(d)/(e) boundary. This is a
  level-(b)/(c) design.

---

## 9. Provenance

Instantiates the consumer-specific parts of the generative model fixed in
`SHARED_CONTENT_DEFINITION_v1.md` (G1 §1: the consumer form S_i(W, u_i), and §2's five
criteria — the FUNCTIONALLY_DISTINCT condition of §2.3 is the "genuinely distinct"
requirement this card operationalizes), on the task fixed in
`PHASE3_INFERENCE_TASK_v1.md` (G2: the scalar LLR sufficient statistic W, the b-bit
quantization, the probe window, the derived decision threshold and Bayes ceiling). The
two retained consumers and their input signatures are `PHASE3_BASELINE_v1.md` (G0 §3.4
S_pol, §3.5 S_reg) and `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (§5.3: S_pol reads
(W, x_t) on reward, S_reg reads (W, V→bookkeeping) on continued operation, the AC107/108
two-way consumption). The rival discipline (P5, P6, D1, D2, D8) and the demotions (D9 no
V, D10 no learned allocator) are `ACI_ARCHITECTURAL_PRINCIPLES_v1.md`; the SPRT/stopping
form is standard optimal-stopping (Wald), stated in the same "derive before training"
spirit G2 used for the Bayes ceiling. Organism study references read from the skill's
`references/` dir where named (`ac11`/`ac16`/`ac17` — gate-shape and rival-sweep
discipline; `ac39`/`ac68` — seed/bimodality discipline; `ac107`/`ac108` — the two-way
relinquish-vs-repair consumption; `ac109` — storage inert where the observation is
decisive).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is
a specialist design, not a result.
