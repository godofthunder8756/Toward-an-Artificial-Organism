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

