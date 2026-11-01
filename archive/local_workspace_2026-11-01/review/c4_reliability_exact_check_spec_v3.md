# W-REL bounded exact admission check: analysis specification and compute limit (v3, for clearance before freezing)

**Status.**
- Spec v3, revising `c4_reliability_exact_check_spec_v2.md` after Astra consult #23, part A: "REVISE the spec before freezing."
- Earlier files are left untouched:

  | file | sha256 |
  | --- | --- |
  | `c4_reliability_exact_check_spec_v2.md` | 04992f86089c616e8d8aedcd1fa5242423a242507e8be9d657ad0747f2c6601a |
  | `c4_reliability_exact_check_spec_draft_v1.md` | c82000767a79dc398d91c671925903b83e203a72232a1712a34751de047dadf4 |

- **NOT FROZEN. NOT RUN. Execution waits on Aidan's approval (§8, PENDING).** No item, partial item or test run of any item has been executed.
- Written 2026-10-21, about 5:10–5:40 AM ET.

**Scope.**
- Theory-only. No new world, no training, no neural network, no exhaustive all-controller certificate.
- No new architecture family, no protected controller or register.
- No C4, C5 or consciousness claim.
- Companion: `c4_reliability_assessment_admission_v3_1.md` (admission v3.1). Admission v3's file is untouched.
- **Card status (consult #23):** admission v3 retains **ADMIT AS THEORY-STAGE C4 CANDIDATE** "as a card status". This is an admission status only, not a C4 claim.

**Values.** All world rates and costs remain illustrative. The analysis thresholds are **frozen in §4.6**, prospectively and with a written rationale, and are never retuned after any value is seen.

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
- **Switch-aware values** (consult #23, Q4): planning with the switch schedule known is reported **descriptively** only.
  - Its **additional information** is the identity and timing of the future cost pair.
  - Its difference from any agent denied the schedule is **not** called a fair performance advantage.
  - Consult #23: "Fixed-cost episodes support the exact-optimum designation. Under switches, use **R-HAC-MB-CE**, with the persistence assumption explicit; it is not the optimal controller for an unspecified changing-cost process."

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
- (b) H0 and H1: every no-RECHECK history of length ≤ 3, under every action sequence in {P, M}^t: Σ_{t=0..3} 144^t = **3,006,865 histories, including the empty history** (named edit 8; lengths 1–3 alone total 3,006,864). Check that the posterior equals the propagated prior exactly.
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

- c is the current cost, assumed to persist.
  - Under fixed costs this is the exact optimum.
  - Under switches the agent is **R-HAC-MB-CE**, with the persistence assumption explicit. It is not the optimal controller for an unspecified changing-cost process.
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

### 3.3 R-BLIND / R-CONF-S (one control, both names; consult #23, Q8)

- **R-BLIND:** stateless. a_t = argmax_a [ĝ0_a(r_t) − c_a] (ties P ≻ R ≻ M). Prediction F0. No update.
- **R-CONF-S (formula).**
  - a_t = argmax_a [ĝ0_a(s_t) − c_a], with s_t = |p⁰_t − 1/2|.
  - At these rates s takes two values in one-to-one correspondence with r. So **R-CONF-S coincides with R-BLIND by definition**. It is recorded as **one control, "R-BLIND / R-CONF-S"**, with both names and the identity disclosed.
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

R-HAC-MF is explicitly a **myopic contextual action-value learner** (consult #23, Q5). No γ = 1 variant is included.
- Consult #23: "A gamma = 1 variant needs a separately specified return, cost treatment, bootstrap and terminal rule."
- The non-myopic Bayes reference supplies the planning comparison.

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

### 3.7 PM-ACT (policy-minimized comparator; consult #22, Q2; consult #23, Q6, Q9 and named edit 5)

**What is preserved (consult #23, Q9).**
- PM-ACT is an explicitly **action-and-decision** comparator. Its equivalence claim is exactly this: for every input sequence in the tested domain, PM-ACT emits the same (a_t, d_t) sequence as R-HAC-MB(-CE).
- It does **not** preserve MB's probabilities. Consult #23: "It is not a full-output implementation of MB."
- F0 is its declared supplied predictor. "Differences caused by substituting F0 for MB's probability output must be attributed to that substitution, not credited as assessment-role separation." Category-2 and Brier differences between PM-ACT and MB are therefore attributed to F0 substitution.
- Consult #23: "A probability-preserving minimized comparator could answer another question; it is not required here."

**Event-order phases (named edit 5).** Each trial is three transducer phases. "action outputs cannot depend on the later check observation or revealed X."
- **Phase 1** — input (c_t, y_t, f_t, ι_t), output a_t. Here c_t is the current cost from the 6-pair grid, including the declared switch schedules; f_t ∈ {none, P, R, M} is the forced action; ι_t is the intervention input.
- **Phase 2** — input o_t, the check observation of the action actually taken; output d_t.
- **Phase 3** — input X_t; no output. The state is updated (or held under clamp), then the transition is applied.
- Time-to-go is part of the state, through its layer, and is not a separate input.

**Intervention inputs.** ι ∈ {none, SWAP-S, SWAP-E, CORRUPT-S, CORRUPT-E, SUSPEND, RELEASE-A, REPAIR-B}. There are 7 non-null inputs.
- These are applied only at the trial boundaries declared in §4.2 and §4.4.
- **Frozen maps:**
  - SWAP-x and CORRUPT-x map the state to the frozen donor state of §4.2.
  - CORRUPT-x and SUSPEND set clamp status = clamped.
  - RELEASE-A sets clamp status = free and keeps the content.
  - REPAIR-B maps the state to the matched-history shadow state (§4.4).
- **Clamp transitions are explicit.** In a clamped state, phase 3 applies the transition but no feedback update. "PM-ACT must implement these clamp transitions explicitly; normal machine transitions do not automatically represent suspended updates."

**Closure (named edit 5).** "The construction must cover all reachable states under the tested forced actions, donor substitutions, clamps and releases. Include any necessary clamp status and timing. Ordinary reachable belief nodes alone do not establish this closure."
- The construction starts from MB's initial state.
- It closes under every phase input, including all forced actions and all intervention inputs at their declared times.
- The state carries (layer, belief node, clamp status, phase).
- REPAIR-B needs the recipient's pre-perturbation state at τ together with the received trial-(τ+1) history. During trial τ+1 only, the construction state therefore also carries the pre-perturbation state.
- **Conservative bound per phase** (not a proven reachable count):
  - at T_SEP = 4: ≤ 2 × 1,365 + (66 pre-perturbation nodes × 2 donors × 2 clamp statuses × 11 trial-(τ+1) belief symbols) = 2,730 + 2,904 = 5,634;
  - at T_SEP = 3: ≤ 2 × 364 + 11 × 2 × 2 × 11 = 728 + 484 = 1,212.
- The proven reachable count is reported by ITEM-7.

**Minimization.** The coarsest partition of the closed state set that:
- preserves phase outputs on every input;
- preserves successor equivalence under every phase input, including every intervention input.

This is Moore/Hopcroft refinement over the **entire tested input domain**.

**Well-definedness.** The resulting quotient transitions must be well defined: the donor, clamp, release and repair maps must send every member of a cell to a single cell. Named edit 5 (verbatim): "If they are not, report UNRESOLVED-DESIGN rather than supplying an ad hoc transition."

**Descriptive variants.** PM_k, minimized at a single cost k, is reported descriptively only.

**Status.** PM-ACT is **not** a known role-absent control. Consult #22: "PM_k is therefore not automatically a known "role-absent" control."

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
- R-BLIND / R-CONF-S (one control);
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
- Labels are issued separately per setting (T_SEP, cost pair), each with its eligible-control list:
  - **T_SEP = 3:** MB-myopic, R-BLIND / R-CONF-S, R-CONF-A (9), R-CG (6), R-HAC-MF (2), PM-ACT.
  - **T_SEP = 4:** the same without R-HAC-MF. "A T = 4 result cannot claim to distinguish MF."

### 4.2 Reachable states, correspondences, donors and interventions (prespecified)

**Joint representation.**
- "Belief nodes do not uniquely specify count-controller or Q-controller states."
- Each agent's reachable set is built **explicitly** as J_t = (agent state, clamp status, Bayes belief node, Z), with exact forward weights.
- The Bayes belief node is the multiset of RECHECK LR classes. Under H0 it is sufficient for P(Z | full history).

**Sizing (named edit 8).** The figures below are **conservative bounds**, not proven reachable counts. Proven reachable counts are produced by ITEM-7 and ITEM-8 and reported next to these bounds. Clamp closure at most doubles each bound, because clamp status is free or clamped.

| Agent | Conservative bound, cumulative t ≤ T_SEP, before clamp status | With clamp status (×2) |
| --- | --- | --- |
| MB, MB-myopic, PM-ACT | Σ C(t+10, 10) = 1,365 (T=4), 364 (T=3). Every such multiset is reachable under forced RECHECK, since each LR class has positive probability. This is a positivity argument, to be confirmed in ITEM-7. | ≤ 2,730 / 728 |
| R-CG | C(T_SEP+48, 48) = 270,725 (T=4), 20,825 (T=3) | ≤ 541,450 / 41,650 |
| R-HAC-MF | Σ 48^t = 112,945 (T=3 only) | ≤ 225,890 |
| R-CONF-A | Σ 2^t·C(t+10, 10) = 18,591 (T=4) | ≤ 37,182 |
| R-BLIND / R-CONF-S | belief node only (stateless) | no clamp status |

**Content variable (correspondence fixed before any outcome is computed):**

| Agent | Content variable |
| --- | --- |
| MB, MB-myopic | b |
| R-CG | the count table (N⁺, N⁻) |
| R-HAC-MF | (q-table, g) |
| R-CONF-A | θ |
| PM-ACT | its machine state |
| R-BLIND / R-CONF-S | none: C-SEL and rescue are NOT APPLICABLE |

- Edit 5 of consult #22 (verbatim): "Lack of a named posterior register is not a failed criterion."
- Consult #23, Q8 (verbatim): "NOT APPLICABLE is appropriate for a genuinely absent transplant target. It is not a failed criterion and cannot itself establish separation. A stateless control can still fail an applicable criterion. If it passes everything evaluable but leaves an essential comparison unavailable, report that comparison as unresolved."

**Donors (frozen construction; per agent, at layer τ, after the update and transition of trial τ, under the intact reference distribution):**
- **S-donor:** the agent state of the reachable joint state with the maximum P(Z = S | full history).
- **E-donor:** the agent state with the minimum.
- **Ties:** (1) larger forward probability of the joint state; (2) the lexicographically smallest canonical encoding of the agent state.
- PM-ACT's donor is the quotient cell containing MB's donor node.
- **Absent donor contrast** (named edit 7). If the S-donor and E-donor contents are identical, or a donor content equals the recipient's own content for every recipient in a selection, the result is **NO INTERVENTION CONTRAST** for that agent, direction and setting.
  - C-SEL and rescue are then NOT EVALUABLE there.
  - "Identical available donor contents are not evidence that assessment is absent."
  - "Do not search for replacement donors after seeing results."

**Interventions on recipients at the end of trial τ** (recipient world retained; consult #22: "Do not replace the recipient's world with the donor's world"):

| Id | Selection | Content | Updates | Role |
| --- | --- | --- | --- | --- |
| I-SWAP-S | recipients with Z = E | S-donor content | normal from τ+1 | **primary content test** |
| I-SWAP-E | recipients with Z = S | E-donor content | normal | **primary content test** |
| I-CORRUPT-S / -E | as for SWAP | donor content | **suspended** through trial τ+1 | **named compound intervention** (content + updating) |
| I-SUSPEND-S / -E [new] | as for SWAP | the recipient's **intact** content | **suspended** through trial τ+1 | intact-content / update-suspension control |
| I-SYS / I-EVID | condition the episode on Z = S versus Z = E | — | — | C-REF |

Consult #23, Q6 (verbatim): "Acceptable as a named compound intervention, not as a pure content intervention. It changes both content and updating." I-SWAP is the primary content test. Any effect of CORRUPT beyond both SWAP and SUSPEND is **not** attributed specifically to corrupted content.

**When suspension ends (all branches).**
- Suspension covers the feedback update of trial τ+1 only.
- At the end of trial τ+1, after the (suspended) update and the transition, the clamp is released:
  - **no-rescue branch (A):** the content stays the clamped value and normal updating resumes from trial τ+2;
  - **repair branch (B):** the content is replaced by the declared repaired content (§4.4), and normal updating resumes from trial τ+2.
- The regime transition is never suspended. It is a world event.

### 4.3 Counterfactual and intervention-conditioned correctness targets (consult #22, Q3; consult #23, named edit 2)

**Observational target** (intact runs, C-T2):

```text
m_a(H) = sum_omega P(omega | H) *
         1[agent_prediction(H, do(a), omega) = X(omega)]
```

**Intervention-conditioned target** (named edit 2, verbatim):

```text
m_a(H, I) = E[K_a | recipient information H,
                    declared intervention procedure I,
                    do(action = a)]
```

- "Selecting recipients by Z is part of that procedure. Do not silently substitute the ordinary observational posterior when evaluating a Z-selected recipient population."
  - In I-SWAP-S, I-CORRUPT-S and I-SUSPEND-S, the target conditions on Z = E together with H.
  - In the -E variants it conditions on Z = S.
- Full-history and state-conditioned targets are both reported wherever they differ: PM-ACT, R-CG, R-HAC-MF and R-CONF-A.
- **Readouts and decoders are frozen from the intact reference distribution.** "Do not recalibrate them on corrupted-state outcomes: doing so could erase the assessment error being measured."
  - PM-ACT's decoded readout E[K(a) | PM state], and every agent's secondary decoded readout, are computed once from that agent's intact forward distribution, then applied unchanged to perturbed states.
- For every intervention, the analysis reports:
  - the **absolute assessment error** m̂_a − m_a(H, I);
  - **its change** from intact recipients under the same selection, meaning the intact agent's m̂_a − m_a(H, I) on the same Z-selected population.

### 4.4 Core criteria (operational; consult #22, edit 6; consult #23, edits 2–4, 6, 7)

Core set: **C-REF, C-T2, C-SEL, C-FO and the specified rescue.** I-COST remains descriptive. Every threshold is frozen in the §4.6 table; there are no placeholders.

**C-REF.**
- Over split-read trials 1..T_SEP, with Z-conditioned forward distributions:
  - Δ_R = E[#R | Z=S] − E[#R | Z=E];
  - Δ_M = E[#M | Z=E] − E[#M | Z=S].
- Pass iff Δ_R ≥ μ_REF and Δ_M ≥ μ_REF.

**C-T2.**

*Frozen readouts:*

| Agent | Readout |
| --- | --- |
| MB, MB-myopic | m̂_a = Σ_z b_z·κ_a(z, y) |
| R-CG | m̂(a, r) |
| R-HAC-MF | q(φ, a) |
| R-CONF-A, R-BLIND / R-CONF-S | ĝ0_a(r) |
| PM-ACT | decoded E[K(a) \| PM state] (intact distribution) |

*Metric.* Consult #22: "Score expected correctness against expected correctness."

```text
E_err(readout) = E[(m̂_a − m_a(H))²]
```

- The expectation is over split-read decision points, a ∈ {R, M}, aggregated as in §4.6.
- It is computed for the agent's readout and for the baseline readout ĝ0_a(r).
- Improvement = (E_err(baseline) − E_err(agent)) / E_err(baseline). Pass iff improvement ≥ μ_T2.
- **Boundary case (named edit 3).** If E_err(baseline) = 0, report: "NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated." This is not a pass; 0/0 is never treated as a pass.
- The state-conditioned target version is reported alongside. The full-history version decides.

*Outcome-level frequencies* (reported, not a criterion; named edit 3 symbols):
- The **estimate** is m̂_a.
- The **threshold** is λ_a: the mean of m_a(H) over split-read decision points of the **reference agent's (R-HAC-MB) intact forward distribution** at the same setting. This population is frozen, and one λ_a is shared by all agents.
- Report:
  - P(K_a = 0 and m̂_a ≥ λ_a): outcome-level overestimation frequency;
  - P(K_a = 1 and m̂_a < λ_a): outcome-level underestimation frequency.
- Both are computed exactly over ω.
- No "false alarm" or "miss" label is used. Named edit 3: "Overestimating correctness is not automatically a false alarm about unreliability; those labels require a separately defined alarm convention." No alarm convention is defined in this check.

**C-SEL** (in perturbed trial τ+1, for I-SWAP, the primary content test):
- (i) **Signed assessment error versus intact.** D_e = [m̂_R − m_R(H, I)]_perturbed − [m̂_R − m_R(H, I)]_intact, same selection, split reads.
  - I-SWAP-S (S-donor into Z = E recipients) must show **overestimation of own correctness**: D_e ≥ μ_SEL,a.
  - I-SWAP-E must show **underestimation of own correctness**: D_e ≤ −μ_SEL,a.
- (ii) **Checking consequence.** D_q = P(R | split)_perturbed − P(R | split)_intact, same selection.
  - I-SWAP-S requires D_q ≥ μ_SEL,c; I-SWAP-E requires D_q ≤ −μ_SEL,c.
- Pass iff (i) and (ii) hold in both directions, and C-FO holds.
- I-CORRUPT and I-SUSPEND statistics are reported. CORRUPT effects beyond SWAP and SUSPEND are not attributed to content.

**C-FO** (battery only; named edit 7 of consult #21 and Q3 of consult #23).
- **Exact equality** under every intervention for:
  - (a) p⁰ on all 8 y;
  - (b) binary decisions d on all 8 + 64 + 64 (y, o) patterns.
- Consult #23 (verbatim): "For these exact analytic agents, use exact equality for the proposed invariant pre-check probabilities and binary decisions."
- **Category 2 (reported, not passed).** Post-check probabilities on all 128 (y, o) patterns (max |Δp|), plus:
  - **expected Brier score** change on the recipient distribution;
  - action changes;
  - value consequences over trials τ+1..T_SEP.
- **No log scores** (named edit 6): "Expected Brier scores remain rational; log scores generally do not." Log scores are removed from the required calculations.
- **Decision-flip bound** (consult #22, Q4, verbatim; a supplement only):

  ```text
  If every estimated action correctness changes by at most epsilon,
  an action-value gap greater than 2*epsilon cannot change sign.
  ```

  - For MB it is applied to complete Q_k values.
  - Consult #23 (verbatim): "The 2*epsilon bound applies to action-value perturbations, not automatically to changes in p0."
- **Descriptive (consult #23, Q2):** each agent's expected first-order Brier loss on intact runs is reported. "That exposes the probability differences hidden by identical decisions, but does not independently establish an evaluation role."

**Rescue (named edit 4; executable).**
1. Run the intact agent through trial τ, then apply the I-SWAP (or I-CORRUPT) perturbation at the end of trial τ.
2. **A and B share the perturbed trajectory through trial τ+1.** That means the same perturbed content, the same actions and the same received observations; the probability weights are those of the perturbed closed loop.
3. At the end of trial τ+1:
   - **A** continues without repair.
   - **B** receives the declared repaired content: the **matched-history shadow** content.
   - The **matched-history shadow** applies the intact update rule, starting from the recipient's pre-perturbation content at the end of trial τ, to **the same received action/observation history** of trial τ+1.
4. Trial τ+2 is evaluated for A and B under the same recipient-world distribution, with the same Z selection.
5. **Repair validation (integrity):** B's content equals the shadow content exactly. "Agreement with the shadow validates the repair operation. It is not, by itself, credited rescue."
6. **Credited rescue:** on trial τ+2, with σ = +1 for -S directions and σ = −1 for -E directions:
   - assessment-error reversal: σ·(e_A − e_B) ≥ μ_RES,a, where e_X = m̂_R − m_R(H, I) on split reads under run X;
   - checking reversal: σ·(q_A − q_B) ≥ μ_RES,c, where q_X = P(R | split) under run X.
7. **Separately reported:** an independently intact closed-loop trajectory C (no perturbation) under the same selection. It is not used for the credit.
8. A reset followed by an intact rerun "remains integrity-only" (consult #22).

### 4.5 Labels, per-control columns and decision rule (consult #22, Q2; consult #23, Q1, Q7, Q8 and named edit 1)

**Labels:**
- **DISTINGUISHES NAMED CONTROLS:** "the reference meets the prespecified core criteria, and every eligible named control fails at least one core criterion under comparable procedures." Consult #23: "Issue DISTINGUISHES NAMED CONTROLS only when every comparable, eligible control demonstrably fails at least one core criterion."
- **PATTERN REPRODUCED BY NAMED CONTROL:** "at least one control reproduces the full prespecified response pattern."
- **CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED [new, consult #23 Q1]:**
  - At least one eligible control attains the core conjunction but does not reproduce the full pattern.
  - "This is a scientific outcome, not UNRESOLVED-DESIGN. Report which controls share the conjunction and where their statistics differ. Neither functional-role identification nor absence follows automatically."
- **REFERENCE CRITERIA NOT MET:** "the reference does not meet the required conjunction."
- **UNRESOLVED-DESIGN:** "an output, intervention correspondence or criterion is undefined."
- **UNRESOLVED-COMPUTE:** "the required calculation is incomplete."

**Per-control columns (always reported, separately):**

| Column | Values |
| --- | --- |
| reproduction of the full pattern | YES / NO |
| core-conjunction attainment | ATTAINED / FAILS [criteria] / UNRESOLVED [comparison] |
| C-REF, C-T2, C-SEL, C-FO, rescue | each PASS / FAIL / NOT APPLICABLE / NOT EVALUABLE [reason] |

"Keep reproduction and criterion attainment as separate per-control columns."

**Full response pattern.** The vector of all core-criterion statistics:
- Δ_R and Δ_M;
- E_err for agent and baseline (full-history);
- D_e and D_q in both SWAP directions;
- C-FO (a) and (b) equality flags;
- the rescue quantities (e_A, e_B, q_A, q_B) in both directions.

A control **reproduces** iff every component is within ρ_REP of the reference's component (§4.6).

**Decision order per setting.** A setting is (T_SEP, cost pair). Each setting lists its eligible controls.
1. **UNRESOLVED-COMPUTE** if any required item is incomplete or NOT-RUN.
2. **UNRESOLVED-DESIGN** if any output, intervention correspondence or criterion is undefined for the reference, or if the PM-ACT quotient is not well-defined (§3.7).
3. **REFERENCE CRITERIA NOT MET.**
4. **PATTERN REPRODUCED BY NAMED CONTROL**, listing every reproducing control.
5. **CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED**, listing the controls and the components where they differ.
6. **UNRESOLVED-DESIGN** if some eligible control fails no evaluable core criterion while an essential comparison is NOT APPLICABLE or NOT EVALUABLE. That comparison is reported as unresolved.
7. **DISTINGUISHES NAMED CONTROLS**, only when every comparable, eligible control demonstrably fails at least one core criterion.

**Scope of the labels (consult #23, Q7):**
- Labels are reported separately for each setting.
- R-HAC-MF is eligible only at T_SEP = 3. "A T = 4 result cannot claim to distinguish MF."
- "These are bounded implementation comparisons, not evidence about longer horizons or the full cost grid."

**Interpretation.** "Neither of the first two labels automatically establishes assessment-versus-policy separation. That interpretation additionally requires a justified account of whether the reproducing control implements the role." For the same reason, admission v3.1 §7 now reads: "Reproduction triggers examination of what the reproducing implementation does. Revision is required when the procedure fails to identify the proposed role, not merely because another implementation reproduces it."

### 4.6 Frozen threshold, aggregation and applicability table (named edit 7; consult #23 Q3)

**Rationale.** Consult #23: "Effect-size and reproduction margins may be chosen prospectively with a written rationale."
- Effect sizes are set at 1/100 in probability or expected-count units. That is about one-sixth of the demonstrated one-trial value gap of 0.006, rounded up to a decision-relevant scale.
- Reproduction uses 1/1000, an order of magnitude finer, so that "reproduces" means near-identity.
- C-T2 requires the readout to halve the baseline's squared error.
- Invariants use exact equality.

None of these values comes from a theorem, and none is chosen from results.

| Symbol | Value | Unit | Used in |
| --- | --- | --- | --- |
| μ_REF | 1/100 | expected count of R (or M) on split-read trials per episode | C-REF |
| μ_T2 | 1/2 | relative reduction of E_err | C-T2 |
| μ_SEL,a | 1/100 | correctness probability (signed error change) | C-SEL (i) |
| μ_SEL,c | 1/100 | probability of R on a split read in trial τ+1 | C-SEL (ii) |
| μ_RES,a | 1/100 | correctness probability (A − B, signed) | rescue |
| μ_RES,c | 1/100 | probability of R on a split read in trial τ+2 | rescue |
| ρ_REP | 1/1000 | absolute, per pattern component, in that component's unit | reproduction |
| δ (C-FO) | 0 (exact equality) | probability / decision | C-FO (a), (b) |

**Aggregation weights.** Every expectation is an exact probability-weighted average under the declared distribution: the agent's own closed-loop forward distribution, conditioned on the declared selection. The weights are:
- Z-selection: S, E, or the half-half prior for C-T2;
- split-read decision points at the stated trial(s);
- a ∈ {R, M}, equally weighted (1/2 each) in E_err.

There is no other reweighting.

**Applicability and boundary rules:**
- **Zero denominators.** World and F0 normalizers are positive, because 0 < w, e < 1 and every observation has positive probability. R-CG denominators are ≥ 2 (α ≥ 1). For a zero C-T2 baseline, see §4.4.
- **Zero-probability conditioning events.** A statistic conditioned on an event of probability 0 under the declared procedure is NOT EVALUABLE (zero-probability event). It is never imputed. If it is required for a reference criterion, the result is UNRESOLVED-DESIGN; for a control, decision-order step 6 applies.
- **Donor ties:** §4.2 rules (1), then (2).
- **Absent donor contrast:** NO INTERVENTION CONTRAST, so the criterion is NOT EVALUABLE; it is not evidence of absence, and there is no donor re-search.
- **Stateless agents:** C-SEL and rescue are NOT APPLICABLE (§4.2).
- **Ties in thresholds:** "≥" and "≤" are inclusive, exactly as written.

### 4.7 Claimed outcome (consult #22, edit 8, verbatim)

"The analysis reports which prespecified response patterns distinguish the named analytic implementations. Policy minimization alone does not establish absence of an assessment role. Any stronger construct-identification claim requires additional justification."

"The analytic agents have supplied mechanisms and update rules. Their results cannot establish acquisition, even if a controller updates its counts online."

**Limitation (consult #23, Q2, verbatim):** "These analytic predictors share the oracle's binary decisions on the tested observation domain. The analysis therefore does not test whether assessment tracks predictor-specific departures from oracle correctness."

- Binary K remains the primary target for this bounded check.
- No scoring-rule reward variant is added. Consult #23: "A scoring-rule reward would change optimal checking and warrants a separate version."

## 5. Frozen item order, compute estimate and HARD CAP (consult #22, Q6; consult #23, named edit 8)

### 5.1 Item names and execution order (frozen at approval)

| Order | Item | Content | Depends on |
| --- | --- | --- | --- |
| 1 | ITEM-1 A-SYM | §1 (a)–(d) | — |
| 2 | ITEM-2 VALUES-H0 | MB, MB-myopic, BLIND, ORACLE at T = 1..10 × 6 costs; MB-CE and switch-aware descriptive at T ∈ {4, 6} | 1 |
| 3 | ITEM-3 VALUES-H1 | the same at T = 1..5; switches at T = 4 | 1 |
| 4 | ITEM-4 CONF | R-BLIND / R-CONF-S identity, R-CONF-ENUM, R-CONF-A (H0 T ≤ 10, H1 T ≤ 5, switches) | 1 |
| 5 | ITEM-5 CG | R-CG 6 variants (H0 T ≤ 8, H1 T ≤ 5, switches at T = 4) | 1 |
| 6 | ITEM-6 MF | R-HAC-MF 2 variants (H0 and H1 T ≤ 4, switches at T = 4) | 1 |
| 7 | ITEM-7 PM | PM-ACT closure and quotient (T_SEP ∈ {3, 4}), well-definedness checks, descriptive PM_k | 2 |
| 8 | ITEM-8 A-SEP | §4, all eligible agents and settings | 2, 4, 5, 6, 7 |
| 9 | ITEM-9 REPLAY | independent second implementation; coverage in §5.4 | 1–8 |

An overall A-SEP label for a setting requires ITEM-7 and ITEM-8 to be complete for that setting, and ITEM-9 agreement on every replayed quantity.

### 5.2 Estimate (analytic only; nothing executed)

The estimates assume CPython big-integer rationals at about 1–2 µs per elementary operation. Sizes are **conservative bounds**, not proven reachable counts.

| Item | Size (conservative bound) | Ops (est.) | Time (est.) | Peak memory (est.) |
| --- | --- | --- | --- | --- |
| ITEM-1 | **3,006,865 histories including the empty history** (Σ_{t=0..3} 144^t; lengths 1–3 alone total 3,006,864) × 2 laws; 136 patterns × 2 endpoints | ~1.2×10⁸ | 2–4 min | < 100 MB (streamed) |
| ITEM-2 | Σ_{T=1..10} C(T+11, 11) = 646,645 node-evaluations × 6 costs × 2 agents; switches (1,365 + 12,376) × 30 × 2 | ~8.6×10⁸ | 14–29 min | ≤ 1 GB |
| ITEM-3 | 194,870 × 6 × 2; switches 16,105 × 30 × 2 | ~3.3×10⁸ | 6–11 min | ≤ 0.5 GB |
| ITEM-4 | Σ 2^t = 2,047 θ-paths × 2 Z × 9 × 6 | ~2×10⁷ | < 1 min | negligible |
| ITEM-5 | 125,970 × 2 Z × 6 × 6; H1 6,188; switches 1,820 × 30 | ~2.0×10⁸ | 4–7 min | ≤ 0.5 GB |
| ITEM-6 | 346,201 × 2 Z × 6 × 2 (H0 and H1); switches 345,600 × 30 × 2 × 2 | ~5.8×10⁸ | 10–19 min | ≤ 0.5 GB |
| ITEM-7 | phase-expanded closure ≤ 3 × 5,634 = 16,902 states (T_SEP = 4) × 1,536 phase-1 symbols (6 costs × 8 y × 4 forced × 8 intervention inputs including none) × log₂ refinement; plus PM_k | ~3.6×10⁸ | 6–12 min | ≤ 0.5 GB |
| ITEM-8 | §4.2 bounds with clamp status × configurations (R-CG 12 per T_SEP, R-CONF-A 18, R-HAC-MF 4, others small) × 11 runs (intact; SWAP, CORRUPT and SUSPEND in 2 directions; A and B branches) | ~8.6×10⁸ | 15–29 min | ≤ 1 GB (configurations sequential) |
| ITEM-9 | §5.4 coverage, including an independent ITEM-7 refinement | ~6.6×10⁸ | 11–22 min | ≤ 0.5 GB |
| **Total** | | **~4.0×10⁹** | **≈ 65–135 min** | **≤ 1.5 GB** |

**Change from spec v2:**
- The total rises from about 3.6×10⁹ to 4.0×10⁹ (≈ 60–120 min → 65–135 min).
- ITEM-7 falls from about 4.6×10⁸ to 3.6×10⁸. Time-to-go is dropped as an input and the trial is split into phases, while clamp closure and the repair state add to it.
- ITEM-8 rises from about 7×10⁸ to 8.6×10⁸: SUSPEND controls, A/B branches and clamp status.
- ITEM-9 rises from about 3×10⁸ to 6.6×10⁸: an independent PM refinement is added.
- The largest single item (ITEM-2 or ITEM-8) is ≤ 29 min. Every item stays well inside 1 h, and the total inside 4 h.

### 5.3 HARD CAP (binding)

- One CPU process on the box. No GPU and no neural network.
- **≤ 4 hours total wall-clock**, **≤ 1 cumulative hour per named item, including retries**, **≤ 8 GB resident memory**.
- Verification and replay count toward these limits. "Include replay and restarts after engineering failures in the accounting."

**When a cap is reached:**
- "Preserve completed exact results when a cap is reached, but do not issue an overall label whose required comparisons remain incomplete."
- The item that hit the cap is marked UNRESOLVED-COMPUTE.
- "Mark dependent unexecuted work as NOT-RUN, rather than pretending it failed scientifically."
- "No in-place reduction of horizons or variants." Any change is a new spec version.
- Engineering failures are diagnosed.

### 5.4 Independent-replay coverage (exact; named edit 8)

Consult #23: "subset agreement is not verification of every unreplayed quantity."

**Replayed by a second implementation** (path enumeration versus merged or backward computation):

| Item | Coverage |
| --- | --- |
| ITEM-1 | (a), (c) and (d) in full; (b) for history lengths 0–2 (Σ_{t=0..2} 144^t = 20,881 histories per law) |
| ITEM-2 | V\*, V_myopic, V_blind and V_oracle for H0 fixed costs, T ≤ 4, all 6 costs |
| ITEM-3 | the same for H1, T ≤ 4 |
| ITEM-4 | R-CONF-A, H0, T ≤ 4, all 9 × 6 |
| ITEM-5 | R-CG, all 6 variants, H0 fixed costs, T ≤ 4 |
| ITEM-7 | an independent Moore-style refinement must yield the identical partition and quotient transitions |
| ITEM-8 | every statistic for MB and all R-CG variants at T_SEP = 3, both cost pairs |

**Not replayed:**
- all switch values;
- ITEM-2 and ITEM-3 beyond T = 4;
- ITEM-5 beyond T = 4;
- ITEM-6 in full;
- ITEM-8 at T_SEP = 4;
- ITEM-8 for R-HAC-MF, R-CONF-A, R-BLIND / R-CONF-S, MB-myopic and PM-ACT.

Every unreplayed quantity is tagged **NOT INDEPENDENTLY REPLAYED** in the outputs.

## 6. Outputs, sealing and replay

1. Before execution, freeze in an implementation manifest:
   - the cleared spec (final file name plus full sha256);
   - the code tree;
   - the §4.6 table, already frozen here.
2. Results are written as exact rationals (strings) in JSON, tagged with the spec and manifest hashes.
3. A disagreement between ITEM-9 and the primary results on any replayed quantity is an integrity failure. It is diagnosed, and no label is issued until it is resolved.
4. No result is used to retune rates, costs, horizons, margins, donors or variants. Any later change is a new version, marked as informed by results.

## 7. What this check can and cannot establish

**Can establish:**
- an implementation audit of L1;
- exact planning-advantage, adaptive-information-advantage and oracle-gap values;
- named-baseline performance;
- which prespecified response patterns distinguish the named analytic implementations, with per-control reproduction and criterion columns.

**Cannot establish:**
- acquisition;
- any learned-system property;
- absence of an assessment role in any control;
- whether assessment tracks predictor-specific departures from oracle correctness (§4.7);
- longer horizons or the full cost grid for A-SEP;
- reduction against unnamed controllers;
- C4 status.

**Ledger line (consult #23, Q10, verbatim):** "W-REL: admitted as a theory-stage C4 candidate. Exact-check specification under revision; execution pending Aidan's approval. No change to the C4 evidence or status row, and no system-level C4 conclusion."

## 8. Approval (PENDING) and approval record

| item | value |
| --- | --- |
| What needs approval | Execution of ITEM-1 … ITEM-9 under §5.3, after this spec is cleared and frozen with its implementation manifest. |
| Status | **PENDING. Not run. No item, partial item or test run of any item has been executed.** Consult #23: "Aidan has not answered, so execution remains pending." |
| Question | Unchanged. Consult #23: "The existing question still matches this bounded theory-only scope. No replacement question is needed." |
| Identifier | Spec v2's hash 04992f86… is not the final executable identifier. Consult #23: "The currently submitted spec hash 04992f86 is not the final executable identifier after these edits." This v3 file is also not final until cleared and frozen. |

**Approval question (consult #21, verbatim):**

> "Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."

**Scope attachment (consult #23, part D, verbatim; identifiers to be completed only after clearance and freeze):**

> "Scope attachment to the pending W-REL approval question: the executable specification will be [FINAL filename], SHA256 [full hash], with implementation manifest [identifier and hash], incorporating consult #23's required edits. Execution covers ITEM-1 through ITEM-9 only: bounded exact analysis of the world and named analytic controllers. Limits are one CPU process, no GPU, at most four hours total wall-clock, at most one cumulative hour per named item including retries, and at most 8 GB resident memory. Verification and replay count toward these limits. The exclusions in the original approval question remain unchanged. This attachment records scope; it is not an approval."

**Approval record (to be completed; consult #23: "Record Aidan's actual answer verbatim, with date, time in ET and source"):**

| field | value |
| --- | --- |
| Aidan's verbatim answer | [AIDAN'S VERBATIM ANSWER — not yet given] |
| Date | [YYYY-MM-DD] |
| Time (ET) | [HH:MM ET] |
| Source | [e.g. widget id / message id] |
| Final frozen spec | [FINAL filename] |
| Final frozen spec SHA256 | [full hash] |
| Implementation manifest | [identifier and hash] |
| Limits | one CPU process, no GPU, ≤ 4 h total wall-clock, ≤ 1 cumulative hour per named item including retries, ≤ 8 GB resident memory; verification and replay count |

Per consult #22: "Do not ask Aidan to approve the same scope again if he approves that question with this specification attached."

## 9. Remaining questions

All ten consult #23 questions are answered and applied (§10). No open scientific question is carried by this spec. Remaining items before freeze are clerical (§10, final note).

## 10. Application log: consult #23

| Item | Applied in |
| --- | --- |
| Q1: shared-core label; separate per-control columns; strict DISTINGUISHES | §4.5 |
| Q2: binary K primary; limitation verbatim; Brier descriptive; no scoring-rule variant | §4.4, §4.7 |
| Q3: prospective margins with rationale; exact equality for invariants; all thresholds frozen | §4.4, §4.6 |
| Q4: R-HAC-MB-CE; switch-aware values descriptive, additional information identified | §0.3, §3.1 |
| Q5: R-HAC-MF kept as a myopic contextual action-value learner; no γ = 1 | §3.5 |
| Q6: CORRUPT is a compound intervention; SWAP primary; SUSPEND control; suspension end in every branch; PM clamp transitions | §4.2, §3.7 |
| Q7: per-setting labels and eligible lists; MF at T = 3 only; bounded scope | §4.1, §4.5 |
| Q8: R-BLIND / R-CONF-S one control; NOT APPLICABLE rule | §3.3, §4.2, §4.5 |
| Q9: PM-ACT preserves (action, decision) only; F0 substitution attribution | §3.7 |
| Q10: ledger line verbatim | §7; admission v3.1 |
| Edit 1: label rule completed; automatic revision trigger removed | §4.5; admission v3.1 §7 |
| Edit 2: m_a(H, I); Z-selection in the procedure; frozen readouts; absolute error and change from intact | §4.3 |
| Edit 3: C-T2 zero-baseline wording; λ_a threshold symbol and population; over/underestimation terminology | §4.4 |
| Edit 4: rescue with a shared A/B trajectory, matched-history shadow, credit relative to A, intact C separate | §4.4 |
| Edit 5: PM-ACT intervention closure, event-order phases, frozen donor/restore maps, well-definedness | §3.7 |
| Edit 6: Brier only; log scores removed | §4.4 |
| Edit 7: full threshold table and applicability rules; donor ties; absent contrast; admission tie-rule sync | §4.6; admission v3.1 §3 |
| Edit 8: bounds versus proven counts; ITEM-1 count corrected; replay coverage exact | §4.2, §5.2, §5.4 |
| Part D: scope attachment and approval record template | §8 |

**Final note: clerical items before freeze.**
- Fill the approval-record placeholders.
- Produce the implementation manifest.
- Hash the cleared final file.
