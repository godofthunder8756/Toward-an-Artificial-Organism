# W-REL bounded exact admission check: analysis specification and compute limit (v2, for review before freezing)

**Status.**
- Spec v2, revising `c4_reliability_exact_check_spec_draft_v1.md` after Astra consult #22, part B: "REVISE the exact-check spec before freezing."
- That earlier file is left untouched (sha256 c82000767a79dc398d91c671925903b83e203a72232a1712a34751de047dadf4).
- **NOT FROZEN. NOT RUN. Execution waits on Aidan's approval (§8, PENDING).** This is the completed specification submitted for review (consult #23).
- Consult #22: "The next step is to resolve the agent definitions and A-SEP procedure, obtain review of that completed spec, and freeze the approved specification and code before running it."
- Written 2026-10-21, about 4:40–5:10 AM ET.

**Scope.**
- Theory-only.
- No neural training, no neural network, no exhaustive all-controller certificate.
- No new architecture family, no protected controller or register.
- No C4 or consciousness claim.

Consult #22: "Constructing and minimizing a named finite comparator is not an exhaustive all-controller certificate." Companion: `c4_reliability_assessment_admission_v3.md` (admission v3). Its admission status, "ADMIT AS THEORY-STAGE C4 CANDIDATE", is an admission status, not a C4 claim.

All parameter values below are **illustrative proposals**. They are frozen only with the approved spec and code, and are never retuned after any value is seen.

---

## 0. World, event order, information, arithmetic

### 0.1 World W-REL-B (admission v3 §1)

- Regimes:
  - Z_t ∈ {S, E};
  - S: (w, e) = (1/20, 1/5);
  - E: (w, e) = (1/5, 1/20).
- n = 3 evidence bits, X_t uniform.
- Actions:
  - P = PREDICT;
  - R = RECHECK (cost c_r: same evidence, fresh internal noise, y′);
  - M = RESAMPLE (cost c_s: fresh world bits, read once, y″).
- Reward per trial: 1[d_t = X_t] − cost(a_t). No discounting. Trials are indexed 1 … T.
- Transition laws:
  - **H0 (primary):** Z constant within an episode.
  - **H1 (secondary):** symmetric switching with h = 1/20 after each trial.
  - In both, P(Z_1 = S) = 1/2.

**Assumptions (consult #22, Q1, verbatim):** "State explicitly that X values, costs and policy randomization are independent of Z, and that Z evolves exogenously." Accordingly:
- X_t ⟂ Z;
- the cost schedule ⟂ Z;
- agent randomization ⟂ Z given observables;
- the transition law is unaffected by actions or outcomes.

### 0.2 Event order (named edit 1, verbatim)

```text
prior over current Z
-> current y
-> action
-> check observation, if any
-> prediction
-> outcome X revealed
-> posterior update using feedback
-> regime transition
-> next trial
```

**Frozen binary prediction rule:** prediction 1 iff `p > 1/2`, otherwise 0. This applies to every agent.

**Action tie rule (all agents):** among equal-valued actions, the order is P ≻ R ≻ M.

**Likelihood-ratio classes.**
- The ten S/E likelihood-ratio classes of a RECHECK trial are indexed by (n_ac, n_aw, n_d). These count, among the 3 bits:
  - n_ac: y_i = y′_i = X;
  - n_aw: y_i = y′_i ≠ X;
  - n_d: y_i ≠ y′_i.
- There are C(5,2) = 10 such classes.
- "The ten likelihood-ratio classes use revealed X. They may compress the feedback update; they must not leak X into the preceding prediction" (edit 1).
- The prediction at step 5 uses only (y, check observation) and the agent's pre-trial state.

### 0.3 Cost information and switch timing (named edit 2)

**Information.**
- **Only current costs are visible.** Each agent sees (c_r, c_s) of trial t at the start of trial t.
- Future costs and the switch schedule are **not** known to any agent.
- The time index t and the horizon T are visible to every agent; only R-HAC-MB uses them.
- "Bayes planning must use the same available information as the rivals." R-HAC-MB therefore plans under the declared **certainty-equivalent assumption** that the current costs persist to T, and re-plans every trial.
- A switch-aware planning value, with the schedule known, may be reported **descriptively** as a labelled non-comparator.

**Cost grid:** K = 6 pairs, c_r ∈ {1/100, 1/50, 1/25} × c_s ∈ {3/50, 1/10}.
- All six pairs satisfy the single-trial D2 region conditions (by hand from the DRAFT region: c_r < 3456/44275; c_r < c_s − 15563907/885500000; c_r > 9747/1416800). This is stated, not computed here.

**Switch definition (edit 2, verbatim form):**
- "old costs through trial `floor(T/2)`, new costs thereafter".
- All 30 ordered pairs k → k′ with k ≠ k′.
- No switch experiments at T = 1.
- Switch experiments are **descriptive (I-COST generalization)**, at T ∈ {4, 6} under H0, T = 4 under H1, and T = 4 for R-CG and R-HAC-MF.

### 0.4 Exact arithmetic (named edit 7, verbatim)

"Primitive world probabilities have terminating decimal denominators. Posterior normalization, count estimates and randomized policies may introduce other factors. All computations use exact rationals with unrestricted positive integer denominators."

For example, ε-greedy over three actions introduces factors of 3. No floating-point value enters any decision, label or reported comparison.

### 0.5 Common supplied first-order predictor (edit 4)

"A common fixed first-order predictor is permissible for analytic controls, but must be declared as supplied and used consistently."

**F0 (SUPPLIED):** the prior-marginal Bayes predictor

```text
P0(X=1 | obs) = sum_z (1/2) P(X=1, obs | z) / sum_z (1/2) P(obs | z)
```

- obs is y (pre-check), (y, y′) or (y, y″).
- p⁰ = P0(X=1 | y) is the pre-check probability.
- It is used by R-BLIND, R-CONF-S, R-CONF-A, R-CG, R-HAC-MF and PM-ACT.
- R-HAC-MB variants and the oracle use belief-weighted or regime-specific predictors (§3).

**Analytic note A11.**
- At these rates, DRAFT D5 found identical S-model and E-model Bayes decisions on all 64 recheck observations. For default and resample observations they agree trivially.
- p(b) − 1/2 has the sign of a function linear in b. So every belief-weighted predictor then makes the same binary decisions as F0.
- ITEM-1(d) re-verifies this exactly under the frozen tie rule, at b = 0 and b = 1, which suffices by linearity.

---

## 1. ITEM-1 A-SYM: history-level symmetry (implementation audit)

**Role.** Consult #22 (verbatim): "The T <= 3 audit checks the implementation. The factorization proof, not that finite audit alone, supports the general horizon claim."

**Conclusion wording to be used if VERIFIED (consult #22, verbatim):** "Without recheck observations, the observation history supplies no information about Z beyond its propagated prior. Recheck observations can be informative. This does not imply perfect identification of the realized regime within a finite horizon."

**Computations:**
- (a) Equality of the per-trial emission tables under S and E: P/feedback (X, y), 16 cells; M (X, y, y″), 128 cells. RECHECK tables (X, y, y′) differ.
- (b) H0 and H1: every no-RECHECK history of length ≤ 3, under every action sequence in {P, M}^t: Σ_{t≤3} 144^t = 3,006,865 histories. Check that the posterior equals the propagated prior exactly.
- (c) One RECHECK yields exactly the 10 (n_ac, n_aw, n_d) likelihood-ratio classes. Each class's ratio is checked against the 128 patterns.
- (d) A11: for all 8 + 64 + 64 observation patterns, F0, S-model and E-model decisions coincide under the tie rule.

**Output:**
- VERIFIED, or a discrepancy with its first counterexample.
- A discrepancy is diagnosed first: implementation error, or an assumption violation.
- If (d) fails, A11 is withdrawn and own-versus-Bayes decisions differ. That is reported, and it is not a failure of L1.

## 2. ITEM-2 / ITEM-3 finite-horizon value comparisons (named edit 3)

**Labels (edit 3, verbatim):**

```text
planning_advantage_T = V* - V_myopic
adaptive_information_advantage_T = V* - V_blind
oracle_gap_T = V_oracle - V*
```

"Both Bayes agents acquire and use information, so their difference is not total information value." No quantity is labelled VOI.

**Comparators:**
- **V\***: R-HAC-MB, the exact finite-horizon optimum. Fixed-cost episodes only; under switched costs, R-HAC-MB-CE (§3.1) is reported descriptively.
- **V_myopic**: R-HAC-MB-myopic.
- **V_blind**: R-BLIND (§3.3).
  - Operationally: it uses the current trial's check observation, through F0, to predict X. It carries **no** source information across trials and plans each trial from the propagated prior, which is 1/2 under H0 and H1.
  - **"Regime-blind" also restricts the prediction rule:** predictions use F0, not a belief.
  - Under fixed costs and the half-half prior, V_blind = T·v_blind(c), where v_blind(c) is the best one-trial value of a map from read class to action under F0. Under switched costs it is the per-trial sum Σ_t v_blind(c_t).
- **V_oracle**: Z_t is known at every trial and predictions use the regime-specific Bayes rule. V_oracle = Σ_t ½ Σ_z v_z(c_t).

**Outputs**, for H0 T = 1…10 and H1 T = 1…5, per cost pair:
- the four values and three labelled differences, exactly;
- expected number of RECHECKs, overall and in unanimous-read states;
- the distribution of time to first RECHECK;
- the exploration cost actually paid.

No exploration schedule is supplied to any agent. If one were supplied, it would be charged and disclosed.

## 3. Agents: complete prediction and update maps (named edit 4)

**Notation:**
- r(y) ∈ {U, Sp}: unanimous or split read.
- o: the check observation (none, y′ or y″).
- d: the binary decision (§0.2).
- ĝ0_a(r): expected correctness of the F0 decision after action a given read class r, under the half-half prior. This is the prior-marginal readout.

"Own correctness cannot be evaluated from an action policy alone" (edit 4), so every agent below has its p⁰, post-action p, d, feedback update and terminal handling declared.

### 3.1 R-HAC-MB (reference) and R-HAC-MB-myopic

**State.** b_t = P(Z_t = S | history before y_t), with b_1 = 1/2.

**Prediction.** p = P_b(X=1 | y, o), the mixture with weight b. p⁰ = P_b(X=1 | y) = P0(X=1 | y), by D1.

**Action (non-myopic).**
- With k = T − t + 1 trials to go:

  ```text
  a_t = argmax_a Q_k(b, y, a; c)
  Q_k = E[1[d = X] | b, y, a] − c_a + E[V_{k−1}(b′) | b, y, a]
  V_k(b) = E_y[max_a Q_k(b, y, a; c)]
  V_0 = 0
  ```

- c is the current cost, assumed to persist (certainty-equivalent; "R-HAC-MB-CE" under switches).
- Ties: P ≻ R ≻ M.

**Action (myopic).** Q⁽my⁾ = E[1[d = X] | b, y, a] − c_a.

**Update after X.**
- b̃ = b·L_S / (b·L_S + (1 − b)·L_E), with L_z = P(y, o, X | z, a).
- L_S = L_E for P and M, so the belief changes only after R, through its LR class.
- Then the transition: H0 gives b′ = b̃; H1 gives b′ = (1 − h)·b̃ + h·(1 − b̃).

**Terminal.** No continuation at t = T.

**Model constants supplied:** w, e, h, T. These go in the ledger.

### 3.2 Oracle

Z_t is known. Prediction uses P(X=1 | y, o; Z_t). The action is the one-trial argmax, which is optimal because trials are independent given Z. No update.

### 3.3 R-BLIND and R-CONF-S

- **R-BLIND:** stateless. a_t = argmax_a [ĝ0_a(r_t) − c_a] (ties P ≻ R ≻ M). Prediction F0. No update.
- **R-CONF-S (formula).**
  - a_t = argmax_a [ĝ0_a(s_t) − c_a], with s_t = |p⁰_t − 1/2|.
  - At these rates s takes two values in one-to-one correspondence with r. So **R-CONF-S coincides with R-BLIND by definition**; it is reported once, with this identity disclosed.
- **R-CONF-ENUM (descriptive only).** The 3² = 9 deterministic maps r → action, applied at every cost. Consult #22: "the nine deterministic tables are an enumeration of mappings, not automatically nine versions of that formula." They are not eligible A-SEP controls.

### 3.4 R-CONF-A (complete cost-dependent threshold rule)

**State.** θ_t ∈ [0, 1/2], with θ_1 = (s_U + s_Sp)/2.
- s_U = 456533/468700 − 1/2.
- s_Sp = 27/100.

**Action.**
- If s_t > θ_t: a_t = P.
- Otherwise: a_t = argmax_{a∈{P,R,M}} [ĝ0_a(r_t) − c_a] (ties P ≻ R ≻ M).

**Prediction.** F0.

**Update after X.**
- err_t = 1[d⁰_t ≠ X_t], where d⁰_t is F0's pre-check decision on y_t, defined whatever the action.
- θ_{t+1} = min(1/2, max(0, θ_t + η·(err_t − α\*))).

**Grid.** η ∈ {1/20, 1/10, 1/5} × α\* ∈ {1/20, 1/10, 1/5}, giving 9 named controls.

**Terminal.** None.

**Analytic bound (restricted to this information set).** By L1, err histories are independent of the Z path, so V ≤ Σ_t v_blind(c_t).

### 3.5 R-HAC-MF (secondary; complete)

**State.**
- A q-table q(φ, a) over φ = (r, g), where g ∈ {none, 0, 1, 2, 3} is the y/y′ agreement count (3 − n_d) at the most recent RECHECK in the episode.
- 10 φ × 3 actions.
- **Initialization** q = 1 everywhere (optimistic gross correctness). g_1 = none.

**Action.**
- v(φ, a) = q(φ, a) − c_a (costs visible).
- **ε-greedy distribution:** with probability 1 − ε, the argmax of v (ties P ≻ R ≻ M); with probability ε, uniform over {P, R, M}, each ε/3.
- So the greedy action has total probability 1 − 2ε/3, and each other action ε/3.
- Variants: ε ∈ {0, 1/10}.

**Prediction.** F0.

**TD target (exact).** γ = 0: target_t = 1[d_t = X_t], gross correctness only, because cost enters at decision time.
- **Update:** q(φ_t, a_t) ← q + (1/4)(target_t − q).
- Then, if a_t = R: g ← agreement count of (y_t, y′_t). No X is used in g.
- **Terminal:** the same update at t = T, with no bootstrap.

This is a myopic contextual learner by declaration. A bootstrapped variant is an open question (§9).

### 3.6 R-CG (consult #22 wording)

R-CG is "A prespecified family of cost-general conventional baselines; conclusions are restricted to these implementations."

**State.** Counts N⁺(a, r) and N⁻(a, r) for a ∈ {P, R, M} and r ∈ {U, Sp}, initialized to (α_s, α_f) in every cell.

**Prediction rule (correctness estimate).** m̂(a, r) = N⁺ / (N⁺ + N⁻).

**Bonus formula.** bonus(a, r) = β / (N⁺(a, r) + N⁻(a, r)). It is action-specific through that action's own count, so it does not cancel across actions (consult #22, Q5).

**Action.** a_t = argmax_a [m̂(a, r_t) + bonus(a, r_t) − c_a] (ties P ≻ R ≻ M).

**First-order prediction.** F0.

**Update.**
- Only actually received feedback: N⁺(a_t, r_t) += 1 if d_t = X_t, otherwise N⁻(a_t, r_t) += 1.
- No update for untaken actions. "Untaken-action replay remains analysis-only."

**Terminal.** None.

**Variants.** (α_s, α_f) ∈ {(1,1), (2,1)} × β ∈ {0, 1/20, 1/10}, giving 6 named baselines.

**Disclosure.** All bonus-driven checks are charged in the value. The number of actions where the argmax differs from the β = 0 argmax is reported. Consult #22: these variants "may also adapt poorly to regime changes. That is a limitation of these variants, not of conventional correctness estimation generally."

### 3.7 PM-ACT (policy-minimized comparator; consult #22, Q2)

**Machine.** The minimal Mealy machine equivalent to R-HAC-MB(-CE) over the **entire tested input domain**:
- per-trial inputs: time-to-go k ≤ T_SEP; current cost c ∈ the 6-pair grid, including the declared switch schedules; y; forced action f ∈ {none, P, R, M}; check observation o; X; intervention input ι ∈ {none, S-donor, E-donor, S-clamp, E-clamp} (§4.2);
- outputs: (a_t, d_t).

**Construction.**
- Start from MB's explicitly reachable (layer, belief-node) states: 1,365 at T_SEP = 4 and 364 at T_SEP = 3.
- Refine to the coarsest partition preserving outputs on every input **and successor equivalence under every input**, including ι (Moore/Hopcroft refinement).
- Consult #22: "preserving the current optimal action does not define a valid minimal state machine."

**First-order probabilities.** PM-ACT has none of its own. It declares F0 as its supplied predictor, which is consistent with its d outputs by A11 (verified in ITEM-1(d)).

**Single-cost machines.** PM_k (minimized at a single cost k) is reported **descriptively only**. Out-of-domain results are not used against it.

**Status.** PM-ACT is **not** a known role-absent control. Consult #22: "A compressed policy state may encode that content implicitly. PM_k is therefore not automatically a known "role-absent" control."

### 3.8 Resource ledger (reported per agent; not equalized)

For each agent:
- state precision (exact rational);
- number of state variables;
- policy parameters;
- computation per step;
- model constants supplied (MB: w, e, h, T; F0: w, e, prior);
- supplied buffers (the world-side recheck evidence; the supplied F0).

## 4. ITEM-7 / ITEM-8 A-SEP: response patterns of named implementations (named edit 5)

### 4.1 Reference, controls, horizon

**Reference.** R-HAC-MB (non-myopic).

**Eligible named controls:**
- R-HAC-MB-myopic;
- R-BLIND (≡ R-CONF-S);
- R-CONF-A (9);
- R-CG (6);
- R-HAC-MF (2);
- PM-ACT.

R-CONF-ENUM and PM_k are descriptive only.

**Settings.**
- H0.
- **T_SEP ∈ {3, 4}**: every agent at 3; every agent except R-HAC-MF at 4.
- Cost pairs **K_SEP = {(1/50, 3/50), (1/100, 1/10)}**.
- Intervention time τ = T_SEP − 2, so trial τ+1 is the perturbed trial and trial τ+2 the measured rescue trial.
- Labels are issued per (T_SEP, cost pair).

### 4.2 Reachable states, correspondences and donors (prespecified)

**Joint representation.**
- "Belief nodes do not uniquely specify count-controller or Q-controller states."
- Each agent's reachable set is built **explicitly** as a joint representation J_t = (agent state, Bayes belief node, Z), with exact forward weights.
- The Bayes belief node is the multiset of RECHECK LR classes, sufficient for P(Z | full history) under H0.

**Joint-state bounds**, cumulative over t ≤ T_SEP:

| Agent | Bound | Count |
| --- | --- | --- |
| MB, MB-myopic, PM-ACT | Σ C(t+10, 10) | 1,365 (T=4); 364 (T=3) |
| R-CG | multisets over a 48-symbol per-trial alphabet (a, r, success, LR class if R): C(T_SEP+48, 48) | 270,725 (T=4); 20,825 (T=3) |
| R-HAC-MF | ordered over the same 48 symbols: Σ 48^t | 112,945 (T=3) |
| R-CONF-A | ordered error bits × LR multiset: Σ 2^t·C(t+10, 10) | 18,591 (T=4) |
| R-BLIND | belief node only (stateless agent) | as MB |

The 9,075 belief-node figure from spec draft v1 is **not** applied to other agents.

**Content variable (correspondence fixed before any outcome is computed):**

| Agent | Content variable |
| --- | --- |
| MB, MB-myopic | b |
| R-CG | the count table (N⁺, N⁻) |
| R-HAC-MF | (q-table, g) |
| R-CONF-A | θ |
| PM-ACT | its machine state |
| R-BLIND | none (stateless): C-SEL and rescue are NOT APPLICABLE |

Edit 5 (verbatim): "Lack of a named posterior register is not a failed criterion."

**Donors (per agent, at layer τ, after the update and transition of trial τ).**
- **S-donor:** the agent state of the joint state with the maximum P(Z = S | full history).
- **E-donor:** the agent state of the joint state with the minimum.
- **Ties:** (1) larger forward probability of the joint state; (2) the lexicographically smallest canonical encoding of the agent state.
- PM-ACT's donor is the cell containing MB's donor node.
- Consult #22: "An extreme Bayes belief need not correspond to a unique count or Q state."

**Interventions on recipients at the end of trial τ.**
- **I-SWAP-S:** S-donor content into recipients with Z = E. **I-SWAP-E:** E-donor content into recipients with Z = S. Updates proceed normally afterwards.
- **I-CORRUPT-S / I-CORRUPT-E:** the same donor contents, held clamped with updates suspended through trial τ+1.
- **Recipient world retained.** Consult #22: "retain the recipient's world distribution while changing the specified agent content. Do not replace the recipient's world with the donor's world."
- **I-SYS / I-EVID (C-REF):** condition the episode on Z = S versus Z = E.

### 4.3 Counterfactual correctness targets (consult #22, Q3)

```text
m_a(H) = sum_omega P(omega | H) *
         1[agent_prediction(H, do(a), omega) = X(omega)]
```

- H is the declared observable information at the decision.
- ω includes the remaining latent variables (Z, X, evidence bits) and observation noise.
- Two targets:
  - **Full-history target** m_a(H): conditions on the full observable history via the joint belief node.
  - **State-conditioned target** m_a(s): conditions on the agent's compressed state under its own forward distribution.
- They are reported separately wherever they differ: PM-ACT, R-CG, R-HAC-MF and R-CONF-A.
- Common random numbers are not used; this is exact expectation.

### 4.4 Core criteria (operational; named edit 6)

Core set (consult #22): **C-REF, C-T2, C-SEL, C-FO and the specified rescue.** I-COST remains descriptive.

All margins below are ILLUSTRATIVE placeholders. They are frozen with written rationale before execution, and are never set from results.

**C-REF.**
- For split-read trials 1..T_SEP: Δ_R = E[#R | Z=S] − E[#R | Z=E] and Δ_M = E[#M | Z=E] − E[#M | Z=S].
- Pass iff both are ≥ μ_REF (placeholder 1/100 per episode).

**C-T2.**

*Frozen readout per agent:*

| Agent | Readout |
| --- | --- |
| MB, MB-myopic | m̂_a = Σ_z b_z·κ_a(z, y), where κ_a(z, y) is the probability that the agent's own decision after a is correct given z and y |
| R-CG | m̂(a, r) |
| R-HAC-MF | q(φ, a) |
| R-CONF-A, R-BLIND | ĝ0_a(r) |
| PM-ACT | decoded state-conditioned readout E[K(a) \| PM state] (exact; analysis-only decoder) |

The same decoded state-conditioned readout is also reported for every agent as a secondary readout.

*Metric:* "Score expected correctness against expected correctness."
- Over decision points on split reads, a ∈ {R, M}, under the agent's own forward distribution:

  ```text
  E_err = E[(m̂_a − m_a(H))²]
  ```

  computed against the full-history target, and separately against the state-conditioned target.
- Baseline: the pre-check confidence readout ĝ0_a(r).
- Pass iff the relative reduction of E_err against the full-history target is ≥ μ_T2 (placeholder 1/2).

*Separately reported (not a criterion):* outcome-level false-alarm and miss frequencies, computed exactly over ω, with m̄_a the agent's marginal mean correctness for a:
- FA_a = P(K_a = 0 and m̂_a ≥ m̄_a);
- Miss_a = P(K_a = 1 and m̂_a < m̄_a).

"even a perfectly calibrated predictor sometimes encounters an unlikely outcome."

**C-SEL.** In perturbed trial τ+1, for each direction and intervention type (SWAP, CORRUPT):
- (i) **Directional assessment error:** m̂_R − m_R(H_recipient) on split reads.
  - S-donor into E-world must give > 0 (false-alarm direction); E-donor into S-world must give < 0 (miss direction).
  - Magnitude ≥ μ_SEL,a (placeholder 1/100).
- (ii) **Directional checking consequence:** the change in P(R | split) versus intact recipients, with the same signs. Magnitude ≥ μ_SEL,c (placeholder 1/100).
- Pass iff (i) and (ii) hold in both directions for SWAP, with C-FO holding. CORRUPT is reported, and must not reverse sign.

**C-FO (battery only; consult #21, edit 4).** Battery:
- (a) p⁰ on all 8 y;
- (b) d on all 8 + 64 + 64 (y, o) patterns.

Pass iff (a) and (b) are unchanged under the intervention within δ (illustrative). For the analytic agents, (a) and (b) are expected to hold exactly by D1 and A11; this is stated, not computed.

Category-2 effects are reported, not passed: post-check probabilities on all 128 (y, o) patterns.

Per consult #22, Q4, every intervention reports:
- probability-vector changes (max |Δp|);
- calibration and proper-score changes (Brier and log score, on the recipient distribution);
- action changes;
- value consequences (expected reward over trials τ+1..T_SEP).

Decision-flip bound, as a supplement only (consult #22, Q4, verbatim):

```text
If every estimated action correctness changes by at most epsilon,
an action-value gap greater than 2*epsilon cannot change sign.
```

For MB this is applied to complete Q_k, including continuation. It "can supplement category-2 reporting, but cannot replace it."

**Rescue (executable sequence).**
1. Run the intact agent through trial τ.
2. At the end of trial τ, apply I-SWAP or I-CORRUPT.
3. Run trial τ+1 with the perturbed content. SWAP updates normally; CORRUPT is clamped.
4. At the end of trial τ+1, after feedback and transition, **restore**: set the content to what the intact agent's update rule yields from its trial-τ content and the recipient's **realized** trial-(τ+1) observations.
5. Run trial τ+2.

**What stays fixed:** the recipient's world distribution, costs, time-to-go, the supplied predictor F0 and the battery.

**Measured consequence.** In trial τ+2: P(R | split), P(M | split) and the readout error, for three runs: (A) perturbed-continued with no restore, (B) restored, (C) intact.

**Credited rescue** iff both hold:
- |B − C| ≤ ρ_RES (placeholder 1/1000);
- |A − C| ≥ μ_RES (placeholder 1/100) in the C-SEL direction.

"A reset followed by an intact rerun remains integrity-only": it is reported as an integrity check, not credited.

### 4.5 Labels and decision rule (consult #22, Q2, verbatim labels)

- **DISTINGUISHES NAMED CONTROLS:** "the reference meets the prespecified core criteria, and every eligible named control fails at least one core criterion under comparable procedures."
- **PATTERN REPRODUCED BY NAMED CONTROL:** "at least one control reproduces the full prespecified response pattern."
- **REFERENCE CRITERIA NOT MET:** "the reference does not meet the required conjunction."
- **UNRESOLVED-DESIGN:** "an output, intervention correspondence or criterion is undefined."
- **UNRESOLVED-COMPUTE:** "the required calculation is incomplete."

**Full response pattern.** The vector of all core-criterion statistics:
- Δ_R and Δ_M;
- E_err (both targets);
- C-SEL (i) and (ii) in both directions, for SWAP and CORRUPT;
- C-FO (a) and (b);
- the rescue triples (A, B, C).

A control "reproduces" iff every component is within ρ_REP (placeholder 1/1000, absolute) of the reference's.

**Order of evaluation** (per T_SEP and cost pair):
1. UNRESOLVED-COMPUTE if any required item is incomplete or NOT-RUN.
2. UNRESOLVED-DESIGN if any correspondence, output or criterion is undefined for the reference. Also UNRESOLVED-DESIGN for a control that fails no evaluable criterion while one of its criteria is NOT APPLICABLE.
3. REFERENCE CRITERIA NOT MET.
4. PATTERN REPRODUCED BY NAMED CONTROL, listing every reproducing control.
5. DISTINGUISHES NAMED CONTROLS.
6. **Unassigned case (flagged for consult #23):** a control meets every core criterion without reproducing the full pattern. Provisionally this is UNRESOLVED-DESIGN, with reason "label rule incomplete".

"At least one PM fails" is never sufficient. Consult #22 (verbatim): "Neither of the first two labels automatically establishes assessment-versus-policy separation. That interpretation additionally requires a justified account of whether the reproducing control implements the role."

### 4.6 Claimed outcome (named edit 8, verbatim)

"The analysis reports which prespecified response patterns distinguish the named analytic implementations. Policy minimization alone does not establish absence of an assessment role. Any stronger construct-identification claim requires additional justification."

"The analytic agents have supplied mechanisms and update rules. Their results cannot establish acquisition, even if a controller updates its counts online."

## 5. Frozen item order, compute estimate and HARD CAP (consult #22, Q6)

### 5.1 Item names and execution order (frozen at approval)

| Order | Item | Content | Depends on |
| --- | --- | --- | --- |
| 1 | ITEM-1 A-SYM | §1 (a)–(d) | — |
| 2 | ITEM-2 VALUES-H0 | MB, MB-myopic, BLIND, ORACLE, T = 1..10, 6 costs; switches T ∈ {4, 6} | 1 |
| 3 | ITEM-3 VALUES-H1 | the same at T = 1..5; switches T = 4 | 1 |
| 4 | ITEM-4 CONF | R-CONF-S/BLIND identity, R-CONF-ENUM, R-CONF-A (H0 T ≤ 10, H1 T ≤ 5, switches) | 1 |
| 5 | ITEM-5 CG | R-CG 6 variants (H0 T ≤ 8, H1 T ≤ 5, switches T = 4) | 1 |
| 6 | ITEM-6 MF | R-HAC-MF 2 variants (H0 and H1 T ≤ 4, switches T = 4) | 1 |
| 7 | ITEM-7 PM | PM-ACT (T_SEP ∈ {3, 4}) and descriptive PM_k | 2 |
| 8 | ITEM-8 A-SEP | §4, all eligible agents | 2, 4, 5, 6, 7 |
| 9 | ITEM-9 REPLAY | independent second implementation (path enumeration versus merged/backward): ITEM-1 T ≤ 2; ITEM-2 and ITEM-3 T ≤ 4; ITEM-5 T ≤ 4; ITEM-8 for MB and R-CG at T_SEP = 3 | 1–8 |

An overall A-SEP label requires ITEM-7, ITEM-8 and ITEM-9 (exact agreement on the replayed quantities) to be complete.

### 5.2 Estimate (analytic only; nothing executed)

The estimates assume CPython big-integer rationals at about 1–2 µs per elementary operation.

| Item | Size (analytic bound) | Ops (est.) | Time (est.) | Peak memory (est.) |
| --- | --- | --- | --- | --- |
| ITEM-1 | 3,006,865 histories × 2 laws; plus 136 patterns × 2 endpoints | ~1.2×10⁸ | 2–4 min | < 100 MB (streamed) |
| ITEM-2 | Σ_{T=1..10} C(T+11, 11) = 646,645 node-evaluations × 6 costs × 2 agents; switches (1,365 + 12,376) × 30 × 2 | ~8.6×10⁸ | 14–29 min | ≤ 1 GB |
| ITEM-3 | Σ_{T=1..5} Σ_{t≤T} 11^t = 194,870 × 6 × 2; switches 16,105 × 30 × 2 | ~3.3×10⁸ | 6–11 min | ≤ 0.5 GB |
| ITEM-4 | θ states ≤ Σ 2^t (2,047 at T = 10) × 2 Z × 9 × 6 | ~2×10⁷ | < 1 min | negligible |
| ITEM-5 | C(20, 12) = 125,970 × 2 Z × 6 costs × 6 variants; H1 C(17, 12) = 6,188; switches 1,820 × 30 | ~2.0×10⁸ | 4–7 min | ≤ 0.5 GB |
| ITEM-6 | Σ_{t≤4} 24^t = 346,201 × 2 Z × 6 × 2 (H0 and H1); switches 345,600 × 30 × 2 × 2 | ~5.8×10⁸ | 10–19 min | ≤ 0.5 GB |
| ITEM-7 | 1,365 states × about 15,360 input symbols × log₂; plus PM_k × 6 | ~4.6×10⁸ | 8–15 min | ≤ 0.5 GB |
| ITEM-8 | §4.2 joint bounds × configurations (R-CG 12 per T_SEP, R-CONF-A 18, R-HAC-MF 4, others small) × (intact + 8 intervention runs) | ~7×10⁸ | 12–24 min | ≤ 1 GB (configurations sequential) |
| ITEM-9 | subsets listed | ~3×10⁸ | 5–10 min | ≤ 0.5 GB |
| **Total** | | **~3.6×10⁹** | **≈ 60–120 min** | **≤ 1.5 GB** |

**Change from spec draft v1** (~1.6×10⁹ ops, 30–75 min):
- values are now computed per T;
- explicit joint reachable states replace belief-node reuse;
- complete agent maps;
- the PM input alphabet now includes intervention inputs;
- the replay is broader.

The largest single item, ITEM-2, is estimated at ≤ 29 min, inside the 1 h per-item limit.

### 5.3 HARD CAP (binding)

- One CPU process on the box. No GPU and no neural network.
- **≤ 4 hours total wall-clock**, **≤ 1 hour per named item**, **≤ 8 GB resident memory**.
- **Accounting:** "Include replay and restarts after engineering failures in the accounting." ITEM-9 counts toward the total. Any restart counts toward both its item's hour and the total.

**When a cap is reached:**
- "Preserve completed exact results when a cap is reached, but do not issue an overall label whose required comparisons remain incomplete."
- The item that hit the cap is marked UNRESOLVED-COMPUTE.
- "Mark dependent unexecuted work as NOT-RUN, rather than pretending it failed scientifically."
- "No in-place reduction of horizons or variants." Any change is a new spec version.
- Engineering failures are diagnosed.

## 6. Outputs, sealing and replay

1. Before execution:
   - freeze the approved spec (final identifier = file name plus sha256) and the code tree in a manifest;
   - freeze the margins with rationale.
2. Results are written as exact rationals (strings) in JSON, tagged with the spec sha.
3. A disagreement between ITEM-9 and the primary results on any compared quantity is an integrity failure. It is diagnosed, and no label is issued until it is resolved.
4. No result is used to retune rates, costs, horizons, margins or variants. Any later change is a new version, marked as informed by results.

## 7. What this check can and cannot establish

**Can establish:**
- an implementation audit of L1;
- exact planning-advantage, adaptive-information-advantage and oracle-gap values;
- named-baseline performance;
- which prespecified response patterns distinguish the named analytic implementations (edit 8).

**Cannot establish:**
- acquisition;
- any learned-system property;
- absence of an assessment role in any control;
- reduction against unnamed controllers;
- C4 status.

"Theory-stage C4 candidate" is an admission status, not a result of this check.

## 8. Approval (PENDING)

| item | value |
| --- | --- |
| What needs approval | Execution of ITEM-1 … ITEM-9 under §5.3, after this spec is reviewed (consult #23), revised if needed, and frozen with its code. |
| Status | **PENDING. Not run. No item, partial item or test run of any item has been executed.** |
| Approval record must include (consult #22) | "Add the final spec identifier and the four-hour/one-hour/eight-GB limits to the approval record." The identifier is the frozen file name plus sha256, recorded at freeze. The limits are ≤ 4 h total, ≤ 1 h per named item, ≤ 8 GB, one CPU process. |
| Re-approval | "Do not ask Aidan to approve the same scope again if he approves that question with this specification attached." |
| Scope match | Consult #22: "The existing question still matches this revised analytic scope." |

Proposed approval question (consult #21, verbatim):

> "Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."

## 9. Open questions for consult #23

1. **Label gap (§4.5 case 6).** How should a control be labelled if it meets every core criterion but does not reproduce the full pattern?
2. **A11.** At these rates, binary own-correctness of the analytic agents coincides with Bayes correctness. Should C-T2 be scored on probabilities or proper scores instead of binary K? Should a scoring-rule reward variant be added so that own-versus-oracle correctness is exercised?
3. **Margins.** Can placeholder margins (μ_REF, μ_SEL, μ_T2, μ_RES, ρ_RES, ρ_REP, δ) be frozen by written rationale alone, before any result? Or should they be derived analytically from the 2ε bound and D2 gaps first?
4. **Certainty-equivalent cost planning.** Is it acceptable that R-HAC-MB plans as if current costs persist, with switch-aware values reported descriptively?
5. **R-HAC-MF.** It is myopic by declaration (γ = 0). Should a bootstrapped variant (γ = 1, terminal target without continuation) be added? It would roughly double ITEM-6.
6. **I-CORRUPT.** Is "donor content with updates suspended through the perturbed trial" an acceptable cross-agent corruption definition?
7. **A-SEP scope.** Is the restriction to K_SEP (2 cost pairs) and T_SEP ∈ {3, 4}, with R-HAC-MF at 3 only, acceptable for comparable procedures?
8. **R-BLIND ≡ R-CONF-S.** Should these be recorded as one control? Should stateless agents' C-SEL and rescue be NOT APPLICABLE, as proposed?
9. **PM-ACT outputs.** Is (action, decision) the right output set, with F0 as its declared predictor? Or must PM-ACT preserve probabilities, which would likely prevent compression?
