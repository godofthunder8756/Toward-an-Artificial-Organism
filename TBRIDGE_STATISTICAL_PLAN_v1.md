# T_bridge statistical plan v1 — the inherited primary contrast is unsatisfiable; the frozen plan covers what N6 left answerable

2026-09-25. Deliverable for the N7 card (t_d1f5cdc5), consumed by N8 (v3
protocol). This document answers the card's question — *what is the frozen
statistical plan: sample size, primary contrast, and resolution, chosen before
final seeds are generated?* — by (1) computing, from N6's verdict, that the
inherited primary contrast has effect size identically zero and cannot satisfy
any superiority gate, (2) re-deriving the set of contrasts that **are**
answerable and assigning each its gate shape and test, and (3) deriving the
final sample size from the error criterion, the resolution floor, and the
minimum effect worth distinguishing — never from the convention of "8 or 16
seeds."

This is a **derived design document**. It runs nothing, trains nothing, freezes
nothing, and edits no frozen artifact (runner, protocol, results dir, hash, or
ledger). It is not hashed into any study's `pre_run_snapshot.json`. It reads
the bridge vocabulary from `ACI_BRIDGE_PROTOCOL_v2.md` §4–§6 and the N1–N6
corrections, and does not re-derive them.

Reading discipline applied throughout. (1) The level-(d)/(e) boundary is
absolute (`DEFINITIONS_CHARTER_v1.md` §2); nothing here is a consciousness
claim. (2) This document makes no empirical claim about T_bridge and no
prediction about which arm wins. (3) Seeds are the replication unit; the two
cue histories within a seed are correlated repeated measures, aggregated before
any between-arm comparison. (4) No gate is moved after a result (AC16).

---

## 0. The one-paragraph answer

The plan must be written against a primary contrast that no longer exists.
N6 established that the representation-integrity state `I_t` is a deterministic
function of the observable decay age `d_t` (`I_t = f(d_t)`), so the strongest
same-information rival — the memoryless state machine `(s_t, E_t, d_t) →
allocation` — **reaches the oracle by construction**. It is the oracle, in
compact form: the oracle's threshold policy and the state machine's rule are the
same function of the same three observables. The candidate can therefore never
exceed it; its best possible result is an exact tie on every seed, the paired
difference is ≤ 0 everywhere, and the effect size of "candidate beats the state
machine" is identically zero. No sample size makes a zero effect significant,
and the exact sign-flip test on a zero-effect contrast has no non-tie data at
all. The card's mandated calculation — *whether the strongest theoretically
possible result can satisfy the frozen inference gate* — is therefore **NO** for
the contrast as inherited, and this plan records that as a re-scope-or-stop
signal for N8 (N6's own instruction, restated as a statistical consequence).

What survives is a smaller, honest set. **N1 content persistence** (arm 1 vs
arm 2: the cue is recoverable only through the paid slot W) is untouched by N6
and is the one clause that still carries a satisfiable, load-bearing effect.
**State-dependence** (candidate vs the fixed-level family, G3b) is satisfiable
but weaker — the state machine passes it too, so it establishes clause (b) of H,
never clause (c)(i). **The `d_t`-read necessity** (arm 9 without vs with the age
read) is a real, observable-scoped diagnostic. **Ceiling attainment** (candidate
vs oracle) is an equivalence question about learning, not about endogeneity. The
plan freezes, for each: the independent sampling unit (the seed), the exact
sign-flip test on paired per-seed differences (p-value floor `2/2^N`, so p = 0
is impossible by construction), the effect-size + exact-binomial-CI reporting
mandate, and **N = 12 final seeds** — derived, not conventional.

---

## 1. The question and what N7 owns

The card's four asks, in its own words:

1. **DEFINE the primary contrast and the smallest effect worth distinguishing.**
2. **Choose the final sample size** from expected variance (engineering only),
   minimum meaningful effect, the chosen confidence/error criterion, and the
   exact resolution of the proposed test — not because prior studies used 8 or
   16 seeds.
3. **Explicitly calculate whether the strongest theoretically possible result
   can satisfy the frozen inference gate**, stating the independent sampling
   unit, aggregating correlated histories within seed, computing the discrete
   p-value resolution, and never reporting p = 0.
4. **PREFER confidence intervals + effect sizes** alongside hypothesis tests,
   and **FREEZE the analysis before final runs.**

N7 decides: the primary contrast and its smallest meaningful effect; the sample
size and its derivation; the test and its resolution; and the per-gate
satisfiability calculation. N7 does **not** decide the claim's re-scoping
(that is N8's job, handed to it in §7), the arm set (N2/N5), or the objectives
(N4). N7's output is the statistical contract those documents must instantiate.

The load-bearing input is N6's hand-off, quoted because the whole plan turns on
it: *"the primary contrast is now vs the (s,E,d) state machine that reaches the
oracle by construction; strict dominance and mean margin over it are both ruled
out (N1/AC16/AC17)"*, and *"the honest question N7 faces is whether any
candidate advantage survives, and on what residual it could rest."*

---

## 2. What N6 changed (the collapse, restated)

N6's verdict, in one table, is the premise of every decision below
(`TBRIDGE_IDENTIFIABILITY_v1.md` §6–§7):

| N6 fact | Content |
| --- | --- |
| The "latent" | `I_t` (slot integrity) is a **deterministic function of the observable decay age** `d_t` (`I_t = f(d_t)`, content-blind, uniform δ-decay). It is observed, not inferred. |
| The state | The maintenance decision is a **fully observed MDP** over `q_t = (s_t, E_t, d_t)` — regime, energy, decay age. |
| The oracle | A threshold policy: refresh iff `s_t = stable ∧ E_t ≥ E_crit ∧ d_t ≥ L−1`. It needs no privileged access to `I_t` beyond `d_t`. |
| The sufficient statistic | `(s_t, E_t, d_t)`; time-since-acquisition and probe-distance are both redundant (the set point is myopic; the probe reward reaches S_pol only). |
| The strongest rival | The memoryless state machine `allocate(s,E,d)` is **the collapse of P_rb (arm 10)** and **the upgrade of arm 9** (add the age read). It is the strongest no-explicit-V rival and is included, never hidden. |

The statistical consequence is sharp and is the whole point of this card:

> Because the state machine *is* the oracle's policy, the "strongest
> same-information rival" and the "ceiling" are now the **same arm**. The
> candidate is bounded above by it on every seed. The contrast that N5 named the
> primary evidence — *does the maintained integrity estimate improve the
> candidate's operation relative to the same-information rival?* — has effect
> size zero by construction.

This is AC17's "strict dominance unsatisfiable at the ceiling" in its terminal
form: not merely "the rival can reach the ceiling on some seeds," but "the rival
is the ceiling, on every seed, by construction."

---

## 3. The primary contrast, honestly re-derived

### 3.1 The inherited contrast is unsatisfiable (the required calculation)

The card asks for an explicit calculation of whether the strongest possible
result can satisfy the frozen gate. Run it for the inherited primary contrast:

- **Contrast.** Candidate (arm 1) vs the `(s,E,d)` memoryless state machine
  (the upgraded arm 9 / collapsed arm 10), on allocation quality.
- **Bound.** The state machine applies the oracle's threshold rule exactly. The
  candidate's allocation is bounded above by the oracle's optimality on every
  seed, so the paired per-seed difference `Δ_seed = candidate − state machine`
  satisfies `Δ_seed ≤ 0` for **every** seed, with equality iff the candidate has
  perfectly learned the threshold rule.
- **Strongest possible result.** The candidate learns the oracle perfectly:
  `Δ_seed = 0` on all N seeds. Effect size = 0. Every paired difference is a
  tie.
- **Gate satisfiability.** The exact sign-flip test (§4.2) operates on non-tie
  paired differences. Under the strongest result there are **no non-tie
  differences**: `N_eff = 0`, the test has no data, and p is not even defined
  (equivalently p = 1.0). No N — not 12, not 1000 — changes this: a zero effect
  has no positive significance at any sample size. A gate phrased "candidate
  beats the state machine" (or any positive candidate advantage over it) is
  unsatisfiable **by construction**, not underpowered.

Conclusion, stated once: **the strongest theoretically possible result cannot
satisfy the inherited primary gate, because the rival is the ceiling and the
ceiling is a tie.** The phrase "the strongest same-information rival is what
makes the integrity component load-bearing" (N5 §2.3) described a contrast whose
rival now sits exactly at the oracle. That contrast is gone.

### 3.2 What survives and is answerable

Each candidate claim is classified by its status after N6:

| Claim | Status after N6 | Gate shape | Satisfiable? |
| --- | --- | --- | --- |
| **N1 / E1 / E2** — active paid persistence (the cue is recoverable only through W) | **Untouched.** Memory for *content* is still required (N6 §4). | Categorical: arm 2 at chance, arm 1 above chance; per-seed sign-flip on probe accuracy | **YES** (effect ≈ ceiling − chance) |
| **G3b** — candidate beats every fixed level (state-dependence) | Survives, but the state machine passes it too. | Dominance over the swept level family (a level is a single swept parameter — AC17-exempt, N5 §5.1) | **YES**, but establishes clause (b) only |
| **G3a** — E_π co-varies with V's *integrity* component | **Collapses.** Perturbing V's integrity is perturbing a re-encoding of `d_t`; the state machine reproduces the same response from the same observable. | — | **UNSUPPORTED as an integrity-inference test** |
| **Same-information contrast** — candidate vs P_rb / arm 9 (as superiority) | **Collapses to ceiling.** P_rb reads `d_t` too; the state machine is its compact form. | Becomes ceiling attainment (equivalence), §6.4 | As superiority: NO. As equivalence: YES. |
| **`d_t`-read necessity** — arm 9 `(s,E)` vs arm 9 `(s,E,d)` | A real residual: arm 9 *without* the age read is genuinely suboptimal in the stable regime (N6 §7.3). | Per-seed sign-flip on the allocation score between the two arm-9 forms | **YES**, but it is a claim about the **observable**, not about inference |
| **G3c / G3d** — reward-invariance / decoupling | Demoted to Tier-1 controls (N5 §2.2). | Pass/fail within a pre-specified tolerance — not a hypothesis test | n/a (control) |

### 3.3 The re-scoped primary contrast

The plan's frozen premise, handed to N8: the **primary discriminating contrast
of the final run is N1 content persistence** (arm 1 vs arm 2), because it is the
only headline claim that survives N6 with a satisfiable, load-bearing effect.
The allocation half of H is re-scoped — either to what the task can honestly
support (the allocation is computed from the agent's own **observed** resource
state `(E_t, d_t)` and the regime `s_t`), whose empirical questions are
**state-dependence** (G3b) and **ceiling attainment** (§6.4), or the "inferred
integrity" wording is dropped and the task changed to make integrity genuinely
latent (N6 §8). What may **not** happen is a final gate that grades the
candidate against the `(s,E,d)` state machine for a positive advantage; §3.1
shows such a gate is unsatisfiable before the first seed runs.

---

## 4. The inference framework

### 4.1 The independent sampling unit is the seed

One seed is one independent replication unit. Within a seed the bridge runs two
cue histories (c ∈ {A, B}); these share the seed's regime draw, distractor
realization, and energy dynamics, differing only in the cue value — they are
**correlated repeated measures**, not independent units. Every endpoint is
therefore aggregated over the two histories **within** the seed first (mean, or
the appropriate per-seed scalar), producing one value per seed per arm. The
between-arm test then runs on the N per-seed values. "N seeds × 2 histories =
N independent units, not 2N" (the AC88 lesson, applied here from the outset).

### 4.2 The test: exact sign-flip on paired per-seed differences

Because every arm runs on the **same** seeds, arm comparisons are paired, and
the marginal (across-seed-family) variance cancels from the difference — the
honest test is the exact sign-flip on the paired per-seed differences, exactly
as implemented in this repo (`_ac116_signflip.py`, AC38/AC46):

```
diffs = [candidate(seed) − rival(seed)  for seed in finals]   (ties excluded)
p = |{ sign-assignments σ ∈ {±1}^n : |Σ σ_i · diffs_i| ≥ |Σ diffs_i| }|  /  2^n
```

Under the null that arm labels carry no information, each difference's sign is
equally likely either way, so all `2^n` sign assignments are equiprobable. The
test is **exact and assumption-free** (no normality, no t-approximation), and —
the property the card demands — its p-value support is a discrete subset of
`{2/2^n, 4/2^n, …}`. **It never contains 0.** "Never report p = 0" is enforced
structurally by using the exact test rather than an asymptotic one, which is the
source of spurious `p = 0` outputs.

### 4.3 The resolution floor

The minimum p achievable at n non-tie differences is `2/2^n` (all n differences
of one sign). Carried from AC38 §3:

| n | floor `2/2^n` | verdict |
| --- | ---: | --- |
| 4 | 0.1250 | cannot demonstrate anything (AC37's engineering was powerless for exactly this reason) |
| 8 | 0.0078 | |
| 12 | 0.00049 | the size that made AC33/AC36's passes real |
| 16 | 0.00003 | |

The plan binds on this: **a gate may be declared passed only if its p-value
clears the frozen per-gate α at a resolution the sample actually supports**; a
result that reaches the floor but not α is reported as an effect size, never as
a pass.

### 4.4 Ties

Paired differences of exactly zero are excluded from the sign-flip and reported.
`N_eff = N − (ties)` is stated alongside every test. If `N_eff` falls below the
resolution-critical size (§5), the gate is reported **underpowered**, not
passed — a real possibility for the ceiling-attainment contrast (§6.4), where
ties are the expected outcome, and exactly why that contrast is graded as an
equivalence question, not a superiority one.

### 4.5 Effect sizes + confidence intervals are the primary reported quantities

Per the card's preference, every gate reports:

1. The **effect size** — the mean and median paired difference, and the
   **fraction of seeds with a positive difference**, the last with an **exact
   binomial (Clopper–Pearson) 95% CI**.
2. The sign-flip p as the **gate**, never as the headline.

The fraction-of-seeds-positive is the quantity that survives a coarse/bimodal
endpoint; the CI on it, not the point p, is what carries the finding when the
p-value sits at the resolution floor.

---

## 5. Sample size (the derivation)

N is derived, not inherited. Three quantities are **frozen constants**, fixed
before any engineering seed is scored:

- **Error criterion.** Per-gate two-sided α = 0.01; family-wise α = 0.05 over
  the primary hypothesis-test gates (N1-content, G3b state-dependence, and the
  `d_t`-read necessity — §6.1–§6.3). The equivalence and control checks (§6.4,
  §6.5) are not hypothesis tests and do not draw on the family budget.
- **Minimum meaningful effect.** The smallest effect worth distinguishing is
  "the candidate is strictly better than the rival in **all but one** seed"
  (fraction positive `(N−1)/N`). Anything below that is reported as an effect
  size, not claimed.
- **Resolution.** The sign-flip floor `2/2^N`.

N must satisfy two inequalities:

1. **The floor clears the criterion.** `2/2^N ≤ 0.01` → `N ≥ 8`.
2. **The minimum meaningful effect is detectable.** For an all-but-one-seed
   effect (one negative sign among n, all |diffs| equal), the exact sign-flip
   gives `p = 2(1+n)/2^n`. This must be ≤ 0.01:

   | N | floor | p(all-but-one) | clears α = 0.01? |
   | ---: | ---: | ---: | --- |
   | 8 | 0.0078 | 0.0703 | ✗ (an 88% effect is undetectable) |
   | 10 | 0.00195 | 0.0215 | ✗ (misses 0.01; clears only 0.05) |
   | **12** | **0.00049** | **0.00635** | **✓** |
   | 16 | 0.00003 | 0.00052 | ✓ |

   **N = 12** is the smallest N that satisfies both. It is not "8 or 16"; both
   are rejected on the merits — 8 cannot detect even an 88% effect at the
   frozen criterion, and 16 is the default the card forbids. N = 12 is the
   point where the resolution floor and the minimum-effect requirement first
   meet.

**Re-derivation rule (the "expected variance, engineering only" clause).** The
sign-flip assumes nothing about effect magnitude, so N above is not variance-
dependent — but the *paired criterion* is. AC38's rule is carried forward:
report `σ_difference` (the sd of the paired difference across engineering seeds,
measured on a seed range the final run does **not** score on), and require
`|mean paired difference| / σ_difference ≥ 3` on data the study does not then
judge. If the engineering `σ_difference` is larger than the minimum meaningful
effect assumes, N is recomputed **before freezing** so that the paired criterion
and the sign-flip floor both hold at the frozen α. The constants (α, the
minimum-effect definition, the floor) are frozen; only N is re-derived from
measured engineering variance, and every engineering seed used to measure it is
excluded from the final sample (AC39).

---

## 6. Gate-by-gate statistical plan

Each gate is stated as: contrast, endpoint, test, resolution, and its
satisfiability calculation. All tests are two-sided sign-flips on paired
per-seed differences (§4.2) unless stated otherwise.

### 6.1 G-N1 — active paid persistence (PRIMARY)

- **Contrast.** Arm 1 (candidate) vs arm 2 (no-maintenance), including arm 2's
  GRU-only variant (W read-in disabled).
- **Endpoint.** Probe accuracy in the stable regime; per-seed scalar = accuracy
  over the seed's cue histories (and any per-seed episode replicates the
  realization adds), plus E1's deterministic cue-slot-survival read.
- **Two parts, both frozen:**
  1. *Arm 2 at chance.* Arm 2's per-seed accuracy lies within the exact binomial
     95% CI around 0.5. Fail (above chance) = F3, free permanence.
  2. *Arm 1 above chance, load-bearingly.* Per-seed sign-flip on
     `candidate − no_maintenance` over probe accuracy; effect size = the
     fraction of seeds where the candidate beats the no-maintenance arm, with
     exact binomial CI.
- **Satisfiability (the required calculation).** The effect is ≈ ceiling −
  chance ≈ 0.5, far above any variance floor, and the contrast is a genuine
  inequality (arm 2 is structurally blind to the cue). The strongest possible
  result — the candidate holds the cue on every seed while arm 2 is at chance on
  every seed — is all-N-positive, giving p = floor = 0.00049 at N = 12, which
  clears α = 0.01. **Satisfiable.** This is the one gate that can honestly carry
  an N1 headline.

### 6.2 G3b — state-dependence (candidate vs the fixed-level family)

- **Contrast.** Arm 1 vs arm 3 (fixed schedule), level family swept (every step,
  every 2nd, …, never) alongside the learner's own parameters (AC11/AC116).
- **Endpoint.** Operation score (v2 §6) — per-seed scalar.
- **Test.** For each level ℓ, a per-seed sign-flip on `candidate − level`, plus
  the fraction-of-seeds-positive with exact binomial CI. **Dominance over the
  family**: the candidate must not be beaten by any level, and must be strictly
  better than the best level (this is a legitimate dominance claim — a level is
  a single swept parameter, not a partial-success rival; AC17 does not apply,
  N5 §5.1).
- **Satisfiability.** A fixed level is state-blind and cannot track the regime
  flip, so the best level is beaten by a regime-tracking allocation on the
  stable/volatile contrast. Satisfiable. **But scope it honestly:** the
  `(s,E,d)` state machine passes this gate too, so a pass establishes clause (b)
  of H (load-bearing beyond state-blind schedules), **never** clause (c)(i)
  (computed from inferred integrity). The results doc must state this scoping.

### 6.3 `d_t`-read necessity (arm 9 without vs with the age read)

- **Contrast.** Arm 9 as written (`(s_t, E_t)` only, no age read) vs arm 9
  upgraded with the age read (`(s_t, E_t, d_t)`). The latter is the compact
  state machine of N6 §7.2.
- **Endpoint.** Allocation score, per-seed.
- **Test.** Per-seed sign-flip on `arm9(d) − arm9(no-d)`; effect size with
  exact binomial CI.
- **Satisfiability.** The no-`d` form cannot tell a fresh slot from one about to
  decay, so it under-refreshes in the stable regime (N6 §7.3) — a real,
  positive effect. Satisfiable. **Scope:** this shows the **observable age
  read** matters for optimality, not that V's learned re-encoding of the age
  adds information; it must not be reported as evidence of an inferred-integrity
  mechanism.

### 6.4 Ceiling attainment (candidate vs oracle) — an equivalence, not a superiority

- **Contrast.** Arm 1 vs arm 6 (oracle), the EXTERNAL ceiling. The candidate is
  bounded above by the oracle on every seed.
- **Question.** Does the trained candidate *learn* the oracle's allocation?
  This is the only genuinely open empirical question about the candidate's
  allocation left by N6, and it is a **learning** question, not an endogeneity
  question.
- **Test.** **One-sided non-inferiority / equivalence** against the oracle: the
  candidate's per-seed allocation score is within a pre-specified equivalence
  margin `ε` of the oracle's, with `ε` declared in the protocol (from the
  engineering screen's estimate of the operation-score noise floor). A candidate
  detectably below the oracle is a learning failure, reported as such — not a
  falsification of H, because H no longer claims to beat the oracle.
- **Satisfiability.** Trivially satisfiable (the candidate can tie the oracle),
  which is exactly why it is graded as equivalence and never presented as
  evidence of the claim. Ties are expected here (§4.4); the gate is the margin,
  not a sign test.

### 6.5 G3c / G3d — mechanistic controls (not hypothesis tests)

- **Form.** Pass/fail checks, not sign-flips: the candidate's `E_π` is invariant
  within a pre-specified tolerance when (G3c) the probe reward is zeroed /
  randomized, and (G3d) the death threshold is removed and reward zeroed.
- **Failure meaning.** A control failure is a **setup failure** (reward leaked
  into A, or A latched onto survival) — a pre-protocol stop, never a recorded
  falsification (N5 §4.2). No p-value is computed; the tolerance is declared in
  the protocol.

---

## 7. What this hands N8

1. **Re-scope or stop, not a superiority gate.** N8 must not write any final
   gate that grades the candidate against the `(s,E,d)` state machine (or P_rb,
   its trained form) for a positive advantage — §3.1 shows it is unsatisfiable
   by construction. Either (a) re-scope H clause (c)(i) from "inferred, not
   observed" to "computed from the agent's own observed resource state `(E_t,
   d_t)` and the announced regime," making the allocation claims §6.2–§6.4; or
   (b) move the "inferred integrity" claim to a task whose integrity is
   genuinely latent (N6 §8) and STOP the bridge as written (N5 §8.8). The
   "inferred integrity" wording cannot be retained over a δ-decay slot with a
   readable age counter.
2. **Freeze the contrast set** of §6 (G-N1 primary; G3b; the `d_t`-read
   necessity; ceiling attainment as equivalence; G3c/G3d as controls), with the
   gate shapes and scoping notes above.
3. **Freeze N = 12 final seeds** (2 cue histories each), derived per §5; state
   the re-derivation rule if engineering `σ_difference` is larger than assumed.
   Disjoint engineering and final families; no engineering seed in the final
   sample (AC39).
4. **Freeze the inference discipline** (§4): seed is the unit; histories
   aggregated within seed; exact sign-flip, never asymptotic; p = 0 is
   forbidden structurally; effect size + exact binomial CI are the primary
   reported quantities; ties excluded and `N_eff` reported.
5. **Record the identifiability outcome** (N6) as a Tier-0 prerequisite (N5
   §2.1), not as evidence, and record this plan's §3.1 calculation as the
   pre-protocol reason the contrast was re-scoped — a disclosed,
   outcome-independent design decision, not a post-hoc gate move.

---

## 8. Claim discipline

- This document makes no empirical claim about T_bridge and no prediction about
  which arm wins. "Unsatisfiable" here means "the contrast has effect size zero
  by construction, so no sample size yields a positive significant result" — a
  property of the task + permitted information (N1 §3.3's "identifiable"), not
  a verdict that the candidate fails, and not a claim that the mechanism is
  inert. Memory for the *content* (W) is unaffected; only the *allocation's*
  dependence on an *inferred* integrity is denied.
- "Primary contrast" (N1 content persistence) is the strongest claim the final
  run can honestly grade; it is a level-(b)/(c) representational claim about
  active paid persistence, and it crosses no level-(d)/(e) boundary.
- No frozen artifact is edited, re-run, or re-hashed. `ACI_BRIDGE_PROTOCOL_v2.md`
  remains the frozen design until N8 issues v3 as a new file; this plan is a
  design note consumed by N8.

---

## Sources

Read, not edited: `TBRIDGE_IDENTIFIABILITY_v1.md` (N6; §3 the oracle and DP,
§6 the two-histories verdict, §7 the sufficient statistic, §8 the boundary, §9
the N7 hand-off), `N5_EVIDENCE_HIERARCHY_v1.md` (N5; §2 the three-tier
hierarchy, §3.4 the gate-shape discipline, §5.1 the gate re-scoping),
`N1_RIVAL_SELECTION_CORRECTION_v1.md` (N1; §3.3 the identifiability test, §2 the
AC16/AC17 argument), `N2_INPUT_SOURCE_AUDIT_v1.md` (N2; §5 P_rb, §6 the
maintained-self-state-vs-internal-information distinction), `N3_LEAKAGE_AUDIT_v1.md`
(N3; §3.3 content-blind bookkeeping, §4 the six tests), `N4_TRAINING_OBJECTIVES_v1.md`
(N4; §4.2 the set point, §4.3 the homeostatic cost, §6 the gradient table),
`ACI_BRIDGE_PROTOCOL_v2.md` (§4.2 gates, §6 endpoints, §10 seed discipline),
`PHASE2_BASELINE_v1.md` (N0; §6 arms, §7(b)(1) the rival-selection flaw).
Repo statistics precedents: `AC38_CRITERION_v1.md` (the exact sign-flip, the
`2/2^n` floor, the paired criterion, "n = 4 cannot demonstrate anything"),
`AC46_RESULTS_v1.md` (the sign-flip at the 2/2^12 floor), `_ac116_signflip.py`
(the exact sign-flip implementation), and the skill's `ac16`/`ac17` (gate-shape
discipline), `ac39` (disjoint seed families; engineering does not transfer),
`ac11` (sweep the level family and the learner's own parameters).
