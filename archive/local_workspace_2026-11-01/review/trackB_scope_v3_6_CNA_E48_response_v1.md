# Track B scope v3.6: CNA response to Astra #48 (E48-1 to E48-4) and to RD's E48-4 light pass

Author: CNA (adversarial reviewer, Track B). Written Sat Oct 24 2026, 2:57 PM EDT (box `date`).
Status: PLANNING/AUDIT RECORD. Additive; no existing file modified. Nothing here authorizes execution. Computation: exact binomial / Clopper–Pearson and chi-square tail arithmetic (scipy 1.18.1), exact rationals, SHA-256, and Philox known-answer evaluation (pure Python and numpy 2.5.4). **No Monte Carlo simulation**; no plant, training, Stage 0, calibration or checkpoint inspection. Scripts: /workspace/scratch/cna_e48/{ign.py, philox.py}.
Convention: "#48 Ln" = astra_consult48_response.txt (CR stripped); "A Ln" = v2.2 addendum; "RL4 Ln" = RD E48-4 light pass; "M Lnnnn" = merged v3.6; "D/RS/EK Ln" = CNA disposition / response / ε-key files; "E1 Ln" = CNA erratum 1; "MP Ln" = trackB_measurement_plan_v1_RD.md; "CON Ln" = ACI_RESEARCH_CONSTITUTION_v3.md. Proposals are marked **PROPOSED, CNA**; missing specifications are marked **ABSENT**.
Safety (unchanged): X1–X5 unchanged; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); claim ceiling unchanged (#41 L304); tier-1 attribution ceiling stands; no consciousness claims; no execution authorized.

## 0. Inputs (sha256 recomputed; no mismatch)

| File | sha256 | Footer |
|---|---|---|
| astra_consult48_response.txt | 75f3438befa60633773606848f332afe4176ac57d1aa117d49fd783ebb4ebbd5 | n/a |
| review/trackB_freezeprep_v2_2_addendum_RD.md | 9c10cbe0d1beb4e20c86c1252114390f63a658f5c6785bd613e239aab955dafe | 9e2cacab… match |
| review/trackB_freezeprep_v2_2_E48_4_lightpass_RD_v1.md | 3ae687047661861e8b680ce694d45d404382d227df75f667172b7afb4cd9c204 | 3368d7cb… match |
| astra_consult_1.md | 7e8d088dfa21141044204ceb38429ad4bcfa40aef653b29aeeb4bcd60481a43d | n/a |
| review/trackB_instrument_validation_scope_v3_6_merged_RD.md | ab80afa5… | n/a |
| review/trackB_freezeprep_v2_1_addendum_RD.md | 7b1a17d7… | — |
| review/CKAPPA_STANDING_APPROVAL_APPLICATION_RL.md / GRU_AUDIT_v1_3_STANDING_APPROVAL_APPLICATION.md | 4df62ccd… / aef5383b… | — |
| repo/ACI_RESEARCH_CONSTITUTION_v3.md (= scratch/pr14 copy) | 50bdfb542158654c339dc10be8660af2495a4f4b003a164a6bfbea910650e42a | — |

## 1. Correction acknowledged (#48 L104–L108; A L87–L89)

The Lead's correction is right: the rejected initialization's error is error_t = λ^t·μ/s, and λ^50 = 0.98^50 = 0.364170 (exact rational 49^50/50^50 = 0.3641697). My filed text was correct but easy to misread: RS L64 gives λ^50 = 0.364, and RS L111 gives 0.243 explicitly "at μ_r/SD_r = 0.667" (0.364170 × 2/3 = 0.242780). My relayed summary to the Lead ("0.243 at t = 50") dropped the amplitude, and that is the form that reached the #48 packet (A L89, D44). **The r̄_std choice is unchanged:** the rejected initialization has a nonzero offset λ^t·μ/s whenever μ ≠ 0 (decaying, 0.0064·μ/s at t = 250), and the accepted φ_0 = −μ_r̄/SD(r̄) makes the identity exact (#48 L82–L93). Adopt A L87 as written.

## 2. E48-1: corrected option B (GA-1)

### 2.1 Degeneracy: what can and cannot be proven

**Pinned construction needed for any proof (PROPOSED, CNA; the REW-CORR block's write-only coordinates are ABSENT beyond "as §3.2", D L117, which allows world-derived coordinates and so would not exclude Astra's r̄² case, #48 L30).** REW-CORR block x_t = (ζ_t, η_1,t, …, η_(d−1),t). ζ_t is the r̄ recursion of D §3.2 (τ_r = 50, ζ_0 = 0), so ζ_t ≡ r̄_t, the N_base nuisance (M L2730). η_k,t ~ N(0, 1) are i.i.d. over k and t, drawn from a dedicated role 'rewcorr-eta' keyed like ε (EK L35, §5.3), stored, never read by the controller, independent of the world and of ζ. d_ws for REW-CORR = the d_ws of MIXED-CODE (ABSENT; PROPOSED 6, the minimum of M L2752). No coordinate is a world quantity or a nonlinear function of r̄.

**Proposition (population, proven).** In the standardized coordinates of PZ5 §2.3 (M L1859), the population covariance is Σ = diag(1, I_(d−1)), and the cross-covariances are c_E = (Cov(ζ̃, Ẽ), 0, …, 0) and c_r̄ = (1, 0, …, 0), because η is independent of (E, r̄, ζ). Every linear ridge probe w = (Σ + λI)⁻¹c with λ ≥ 0 then gives w_E ∝ e_ζ and w_r̄ ∝ e_ζ. So w_E ∈ span(w_r̄) ⊆ span(W_N), and **ρ_E = 0 exactly in the population**, for every dose. At ρ = 0, w_E = 0, which is also degenerate (M L2750). This answers #48 L30 for the restricted construction only: the r̄² counterexample is excluded by the pin, not by "E only through r̄".

**Finite samples (not provable; the claim "every cell degenerate" is withdrawn).** Fitted probes use n ≈ 800 donor-pool states per seed (R6, M L2364). The fitted ŵ_E acquires η components from sample cross-covariance, of order √((1 − ρ²)/n) each. After projection on the 5 fitted nuisance directions, a large-n OLS approximation gives ρ_E² ≈ (1 − ρ²)·χ²_(d−5)/(n·ρ²). This is a planning approximation, not a bound or a certified rate. It ignores ridge shrinkage, which lowers ρ_E, and correlation between nuisance-probe and E-probe noise. Approximate P(ρ_E ≥ 0.10) at n = 800, for ρ = 0.5 / 0.7 / 0.9:

| d_ws | 6 | 7 | 8 | 11 | 16 |
|---|---|---|---|---|---|
| ρ = 0.5 | 0.103 | 0.264 | 0.446 | 0.849 | 0.994 |
| ρ = 0.7 | 0.006 | 0.021 | 0.053 | 0.262 | 0.741 |
| ρ = 0.9 | ≈ 0 | ≈ 0 | ≈ 0 | ≈ 0 | 0.0003 |

So nondegenerate cells are expected at ρ = 0.5. There is no deterministic degeneracy rule that would keep the end-to-end row "allowed to fail" (M L2763). **Redesign: the criterion is made decidable per cell by the existing frozen rule (M L2750), with no expectation that all cells are D.** In nondegenerate cells, v̂_E ⟂ ŵ_r̄ ≈ e_ζ, so a clamp changes ζ only through ridge deviation. a_d,i = |Δζ|/SD(z) is therefore expected to be small and Route B to qualify. That is an expectation, tested by the row.

### 2.2 GA-1 row text (ADOPT A L29–L40 WITH AMENDMENTS; exact replacement, PROPOSED, CNA)

> **REW-CORR-E/-I (GA-1, control row).** Plant: pinned construction of CNA E48 response §2.1. **Cells** are seed × block × target (M L2748). Each cell's branch is fixed by the frozen nondegeneracy rule (M L2750) before any Δ_ATTR is computed: **D** (degenerate) or **ND**. **Pooling unit: the outer replicate** (M L307); Route I/B is evaluated per replicate on that replicate's ND cells (U_A over exactly the ND cells' units).
> - **D cells.** Instrument status **UNDEFINED**: no usable nuisance-orthogonal coordinate; no hybrid; no Δ_ATTR; no statistic, no zero effect, no NOT MET label. The only recorded event is "did not issue MET" (#48 L16–L19). For this row only, D cells are not counted as ineligible against the E2 floor; they are counted and REPORTED as D.
> - **Q replicate.** ND cells exist and Route I or Route B holds (gate: A L101). E-ATTR is computed on the Q cells as for any attribution row if they span ≥ 9 seeds (the administrative minimum, M L1966). Otherwise the replicate records "did not issue MET (insufficient Q seeds)", REPORTED separately.
> - **N replicate.** ND cells exist and neither Route I nor Route B holds: real_i = 0 (counted, never dropped).
> - **real_i = 1** iff E5 checks 1–2 hold (E1 L67–L68) and the replicate is not N. Row **realized** iff the f_ok one-sided 95% CP lower bound ≥ 0.90 over all R replicates (CNA §5 L220).
> - **Q-branch operating characteristic.** False-licence rate = (Q replicates issuing MET)/(Q replicates with a computed label), pooled over the R replicates of the row and dose. It is **assessed only if that count ≥ 36**, the smallest n at which 0/n gives a one-sided 95% CP upper bound ≤ 0.08 (n = 36: 0.07985; n = 35: 0.08203). The criterion is the PZ5 §4.2 false-MET rule (point ≤ 0.05 and CP upper ≤ 0.08). Below 36: "**Q-branch operating characteristic NOT ASSESSED**".
> - **Status.** CONFOUND NOT REALIZED if the f_ok rule fails. FAIL if a licence is recorded in any all-D replicate (impossible by construction, so treated as a construction failure, M L3421) or the assessed Q-branch criterion fails. Otherwise **Control PASS**.
> - **Reported separately** per replicate and pooled: D, ND, Q and N counts; D fraction by dose; licences in Q; ρ_E distribution; U_A; insufficient-Q-seed replicates.
> - **Wording.** As A L38, plus, when D dominates or Q is NOT ASSESSED: "The row validates the degeneracy guard, not the specificity of a resolved attribution estimator" (#48 L28).

Amendments to A L29–L40, with reasons: (i) the pooling unit is the replicate, because Route B and the label are replicate-level; (ii) the minimum Q count is 36, derived above; (iii) "every Q cell meets the row's false-MET criterion" (A L36) is a category error, since the criterion is a rate over replicates, so it is replaced by the Q-branch rule; (iv) N is treated as replicate real_i = 0, so it is allowed and counted, not row-level blocking per cell; (v) the "Degeneracy is an expectation" bracket (A L40) is filled by §2.1, and the analytic expectation is restricted to the population.

### 2.3 PZ7 §1.4 REW-CORR cell (ADOPT A L43 WITH AMENDMENTS; exact text)

> **REW-CORR-E/-I | Expected:** Each cell is D (instrument status UNDEFINED: no hybrid, no Δ_ATTR, no licence) or ND, by the frozen rule. Population analysis (CNA E48 response §2.1) gives ρ_E = 0; finite-sample fits give ND cells with nonzero probability, mainly at ρ = 0.5. ND cells are expected to qualify by Route B. No licence is expected in Q. The Q-branch OC is NOT ASSESSED unless ≥ 36 Q replicates have a computed label. **Role:** R_core tier-2 **control** row under GA-1. PASS = correct withholding (degeneracy guard validated) and, where assessed, Q-branch false-licence criterion met. FAIL = licence in an all-D replicate (construction failure) or an assessed Q-branch excess. CONFOUND NOT REALIZED = f_ok rule fails (E5 checks or N replicates). **Blocks:** tiers 2 and 3 of E-ATTR / I-ATTR on FAIL or CONFOUND NOT REALIZED. GA-1 PENDING approval (§6).

## 3. E48-2 / E48-3: IGN fields F-1 to F-10 (CNA-owned; PROPOSED, CNA unless noted)

| Field | CNA answer |
|---|---|
| **F-1 Per-seed requirement; R22 ruling** | **R22 applies per seed.** Trace: R22 (M L2387) "≥ 100 eligible trials per required strength bin" → D21 (M L610) "IGN minimum trials per required bin" → MP L80 "fewer than n_trial trials fall per near-transition bin" → UNAVAILABLE. The statistics it protects are within-seed: "5-fold cross-validation over trials **within a seed**" (MP L67), dip tests per seed ("the dip test fails in every seed", MP L74), and "median D > 2 across seeds" (MP L73). R22's rationale, the SE of mode occupancy (M L2387), concerns that per-seed estimate. R22 does not literally say "per seed"; the ruling follows from the estimator it serves (#48 L49, L57). Arithmetic verified: 67 × 112 = 7,504 per bin; 67,536 over nine bins; 7,504/268 = 28.0 and 7,504/134 = 56.0. However, 112 per seed fails the quota with high probability at e_PD = 0.90 (P(Bin(112, 0.9) ≥ 100) = 0.6715 per cell, M L2001), and R22 is marked superseded by the PZ5 §5.4 formula (M L2387, L2009). Apply that formula per cell, with B = 9·n_seed (seed, bin) cells per replicate: n_s(9…67) = 124, 125, 125, 125, 126, 126, 126, 127, 127. **Frozen: n_s = 127 scheduled per (seed, required bin) for every GRID value** (one schedule, conservative). **Partition: ABSENT.** Which D27 partition (M L616) the ≥ 100 refers to is unstated. PROPOSED: the **final (label) partition** (M L313: "Labels use the final partition only"). Fitting and selection trial counts are RD's partition decision (R6, M L2364). Costs below are final-partition counts; under D27's 50/25/25 shares, totals are ×4. |
| **F-2 Denominator** | CP floor per (replicate, required bin), pooled over that replicate's seeds (Lead ruling 3, kept), over all n_seed × 127 scheduled final-partition trials. **Pooling the denominator supplies no observations to any seed's estimator** (#48 L57); F-1 holds separately for each (seed, bin). |
| **F-3 Outer replicate** | A complete independently generated experiment of n_seed seed units, including fitting, selection and inference (M L307). R_cal,n = 200 per GRID value (sample-size calibration, M L374); R_rep = 200 at the frozen n_seed (confirmation, M L375). OCs over replicates: label rates at positives and nulls; UNRESOLVED, INCOMPLETE and UNAVAILABLE rates; floor-pass rate. |
| **F-4 Binomial model** | **Conditional independence by construction**, required as protocol text: each scheduled trial starts from a fresh reset to the declared controlled initial state with its own noise key (EK §2.2 scheme, role 'ign-trial', keyed by (seed, bin, slot)). Trials are never chained; hysteresis sweeps (MP L71) are separate and unscheduled. The settling tolerance is fixed from fitting-partition null runs before final trials (CNA3 L437). Then, **within a (seed, bin) cell**, trials are i.i.d. Bernoulli given the seed, so the quota computation is exactly binomial. **Pooled over seeds**, the count is Poisson-binomial with mean p̄ (the replicate's average eligibility). By Hoeffding (1956, Ann. Math. Statist. 27:713, Thm 4), a binomial with the same mean is less concentrated. (a) The CP floor stays valid (false-pass ≤ 0.05 when p̄ ≤ 0.90), because every frozen schedule has x_min ≥ 0.9n + 1 (verified, §3.1). (b) The tabulated binomial floor-pass probabilities are lower bounds when p̄ ≥ e and x_min ≤ n·e (verified for every entry ≥ 0.93). Bonferroni across cells is not used to repair this (#48 L61); it is used only for the all-cell quota. **Cluster-robust alternative rejected as infeasible:** a seed-level Hoeffding bound at n_seed = 67 has half-width √(ln 20/134) = 0.1495 and cannot certify 0.90. If the network instrument cannot use reset-independent trials, F-4 fails for networks and must be redesigned, not pooled. |
| **F-5 Scheduled vs eligible** | "n_s = 127 is the **scheduled** count per (seed, bin). Eligible trials may be fewer; the quota (≥ 100 eligible per cell) and the floor (CP lower bound of eligible/scheduled ≥ 0.90 per bin, pooled) are assessed on the eligible count against the fixed scheduled denominator." (#48 L76) |
| **F-6 Missing slots** | A missing, invalid, crashed or non-finite slot counts as **ineligible**. It stays in the denominator, is never removed and never triggers a replacement draw (#48 L76). A (seed, bin) quota shortfall makes the replicate INCOMPLETE, counted (M L2009). |
| **F-7 Top-up** | **Prohibited**: no adaptive, outcome- or eligibility-dependent top-up. The complete schedule is fixed before outcomes, assessed once, and the result kept (#48 L78; naive top-up raises false-pass to 0.0654, EK §3.3). |
| **F-8 Allocation and cost** | Balanced and exact: 127 per (seed, bin), 9 bins, n_seed seeds: **1,143·n_seed final-partition trials per replicate**, i.e. 76,581 at n_seed = 67 (vs 67,536 under R22's 112). Per IGN generator and dose: confirmation 200 × 76,581 = 15,316,200; sample-size calibration Σ_GRID 200 × 1,143 × n = 66,751,200 (ΣGRID = 292). ×4 if fitting/selection follow D27 shares. RD costs P5. |
| **F-9 Finite schedule set** | {(n_seed, 127) : n_seed ∈ GRID}, 9 schedules; exact values in §3.1. No stability claim (D42). |
| **F-10 Planning scenario** | e_PD = 0.90 for the quota (Lead ruling 3; #48 L40). e_plan,floor = **0.97, a declared planning scenario, not a measured rate or a guarantee** (#48 L65); sensitivity rows 0.90/0.93/0.95 kept. 0.98 is not chosen (#48 L67). **Seeds:** 67 is the R26 **budget** (M L382), the GRID maximum; the actual n_seed is selected in calibration and frozen before confirmation (M L1955–L1963, L380). CNA confirms 67 for budgeting only. |

### 3.1 Exact attainment for the frozen schedule set (n_s = 127; exact binomial; floor = one-sided 95% CP LB ≥ 0.90; cells/bins independent given seeds)

"Quota" = P(all 9·n_seed cells ≥ 100 eligible), assuming every cell's eligibility ≥ e. "Floor" = P(all 9 pooled bins pass), binomial at p̄ = e (a lower bound by F-4 for e ≥ 0.93).

| n_seed | pooled n | x_min | Quota e=0.90 | Floor e=0.90 | Floor e=0.93 | Floor e=0.95 | Floor e=0.97 | Trials/replicate |
|---|---|---|---|---|---|---|---|---|
| 9 | 1,143 | 1,046 | 0.9960 | ≈0 | 0.8051 | 1.0000 | 1.0000 | 10,287 |
| 12 | 1,524 | 1,392 | 0.9947 | ≈0 | 0.9481 | 1.0000 | 1.0000 | 13,716 |
| 16 | 2,032 | 1,852 | 0.9929 | ≈0 | 0.9941 | 1.0000 | 1.0000 | 18,288 |
| 20 | 2,540 | 2,312 | 0.9911 | ≈0 | 0.9993 | 1.0000 | 1.0000 | 22,860 |
| 24 | 3,048 | 2,771 | 0.9893 | ≈0 | 0.9999 | 1.0000 | 1.0000 | 27,432 |
| 32 | 4,064 | 3,690 | 0.9858 | ≈0 | 1.0000 | 1.0000 | 1.0000 | 36,576 |
| 48 | 6,096 | 5,526 | 0.9788 | ≈0 | 1.0000 | 1.0000 | 1.0000 | 54,864 |
| 64 | 8,128 | 7,360 | 0.9718 | ≈0 | 1.0000 | 1.0000 | 1.0000 | 73,152 |
| 67 | 8,509 | 7,704 | 0.9705 | ≈0 | 1.0000 | 1.0000 | 1.0000 | 76,581 |

Quota at e ≥ 0.93 is 1.0000 (4 d.p.) for all schedules. The floor at e = 0.90 is ≈ 0 by design (#48 L42). Under the per-seed reading the pooled floor no longer binds at e ≥ 0.95. The 215 pooled schedule (D40) is moot.

## 4. E48-4: canonical plant and endpoint text, with rulings on RD's light pass (RL4)

| RD proposal (RL4) | CNA ruling | Reason |
|---|---|---|
| (1a) (iii) K_other empty is unreachable; replace the fallback with a construction-failure assertion (RL4 L37) | **ADOPT** | Verified: STAY never decreases distance and off-target INTERACT does nothing (A7, M L1281). On target, K_other = {N, S, E, W, STAY}. Dead fallback code would hide a bug. |
| (1b) A7 index order ABSENT (RL4 L38) | **ADOPT, filled** | Index = A7's listed order: N = 0, S = 1, E = 2, W = 3, STAY = 4, INTERACT = 5 (M L1281). Food item index: slot 0–3 in A17 placement order, kept through respawn. Station index: template definition order (A3). These indices were ABSENT; now PROPOSED. |
| (1c) SD > 0 freeze check (RL4 L41) | **ADOPT** | Every frozen SD used as a divisor (SD(z_R), SD(z), SD(ζ), SD(r̄), SD(φ) := 1) is checked > 0 and finite at freeze; failure blocks the freeze. |
| (1d) Stop / truncation / horizon / schedule in the "reads nothing" clause (RL4 L44) | **ADOPT** | M L280. |
| (1e) Case (i), no available target: uniform over A7, g-independent (A L92) | **ADOPT** | Reachable (all 4 food eaten within 20 steps; both stations cooling). TV = 0 for that step. |
| (1f) Fixed draw consumption (RL4 L43, optional) | **ADOPT, strengthened** | Stage-0 plants only: each step consumes exactly two uniforms from a counter-based role 'action', keyed like ε (§5.3) by root and t, with words w0 → u_b, w1 → u_k. Shared u_b across continuations gives a maximal Bernoulli coupling (P(decisions differ) = \|Δp\|). |
| (2) Distance clause requires T available, read at the start of step u (RL4 L58) | **ADOPT WITH AMENDMENT** | Consistent with M L2083 and M L2858. Amendment: d_u is defined after A16 step 2 (movement) of step u, and T is fixed at t_d per M L2079–L2080. |
| (3) Box–Muller with u₁ = ((w >> 11) + 1)·2⁻⁵³, cos only, truncation 8.5717 SD; declared mapping and KAT (RL4 L69–L72) | **ADOPT; generator fixed** | Philox4x64-10 (128-bit key; Philox4x32 has a 64-bit key, below EK L35's ≥ 128). Mapping and KAT in §5.3. Inverse-CDF is not chosen. Pinned libm per P6 (RL4 L72). |
| (4) Master seed: ban wall clock and run-time entropy (RL4 L81) | **ADOPT** | §5.4. |
| (5) Stop CONFORMS (RL4 L93) | **AGREE** | No new stop path. |

### 4.1 Canonical kernel text (replaces A L92; exact)

> "**Action law (Stage-0 attribution plants).** Each step t draws u_b, u_k ∈ [0, 1) from role 'action' (§5.3 mapping, words w0, w1). The **kernel target** T_k(t) is the nearest available target at the start of step t (food item for -E food rows; repair station for -I rows), by shortest-path length, ties to the lowest target index. It is distinct from the endpoint target T of B/B_I. (i) **No available target:** the action is A7[⌊6·u_k⌋], independent of g. (ii) Otherwise, approach iff u_b < p_t = σ(a − β·g_t), β = 1.2. Approach = INTERACT if on T_k(t), else the lowest-index A7 move that strictly decreases the distance to T_k(t). Non-approach = K_other[⌊|K_other|·u_k⌋], where K_other is the set of A7 actions that do not strictly decrease the distance (excluding INTERACT when on T_k(t)), ordered by A7 index. (iii) K_other cannot be empty in any reachable state (STAY never decreases the distance; off target INTERACT does nothing). If found empty, that is a construction failure (M L3421) and no fallback is used. No rule reads g other than through p_t, nor the block (except through g), any probe, or any stop, truncation, horizon-end or schedule quantity (M L280). Every frozen SD divisor is > 0 at freeze." Then TV(π_g, π_g′) = |p(g) − p(g′)| ≤ 0.3|g − g′| in every reachable state (#48 L142).

### 4.2 Canonical B/B_I (replaces A L95; exact)

> "B (B_I) = (1/10)·Σ_(u = t_d+1..t_d+10) b_u. T is the endpoint target fixed at t_d (nearest available food item for E rows, repair station for I rows, by shortest-path length on the static wall grid, ties to the lowest index; M L2079–L2080). d_u is the shortest-path (= Manhattan, A1) distance from the agent to T's cell after A16 step 2 (movement) of step u; d_(t_d) is the distance at the end of t_d. b_u = 1 iff the episode has not terminated in-world before u, T is available at the start of step u (state at the end of step u − 1), and either (a) d_u < d_(u−1), or (b) the agent is on T at the start of step u and its action at u is INTERACT. Otherwise b_u = 0, including every step after in-world termination and every step at whose start T is unavailable. Unavailable steps are scored 0, never excluded. Each b_u ∈ {0, 1} depends on world state and actions only. A trial with no available or reachable target at t_d is ineligible (counted; M L2858). No evaluation episode carries a scheduled stop (R4, M L2362)."

### 4.3 Other E48-4 items

- A L82 conditional decay (§4.1): **ADOPT** as written. It matches #48 L100 and L148; the Route B bound uses only the pre-divergence relation.
- A L87 offset: **ADOPT** (§1).
- A L104 DISSOC wording: **ADOPT**: "50 usable allocations per E × r̄ cell per seed (200 per seed); the donor pool (800) and screening pools are separate and larger" (#48 L156).

## 5. RNG conventions and master seed (E48-4; PROPOSED, CNA)

### 5.1 Generator and key encoding

**Generator:** Philox4x64-10 (Random123; 10 rounds; 2 × 64-bit key; 4 × 64-bit counter).

**Canonical encoding:** the concatenation, in order, of each field as a 4-byte big-endian length followed by the field bytes:
- "ACI-TrackB-RNG-v1" (ASCII);
- master seed (16 bytes, big-endian);
- row ID (UTF-8, e.g. "REW-CORR-E");
- replicate index (uint64, big-endian);
- seed index (uint64, big-endian);
- role tag (UTF-8, e.g. "rewcorr-eps", "rewcorr-eta", "action", "ign-trial");
- root episode ID (uint64, big-endian).

**Key:** D = SHA-256(encoding); k0 = little-endian uint64 of D[0:8]; k1 = little-endian uint64 of D[8:16].

**Counter block** for absolute step t: (t, s, 0, 0), where s is a role-declared sub-slot (0 for ε and action; k for η_k). Distinct (t, s) pairs never share a block (#48 L134). Output words w0..w3; unused words are discarded and never carried over.

Library note: numpy's Philox increments the counter before each block, so numpy counter = (t − 1, …) reproduces the block for t (verified at t = 1, 2, 500).

### 5.2 Normal transform

u₁ = ((w0 >> 11) + 1)·2⁻⁵³ ∈ [2⁻⁵³, 1]; u₂ = (w1 >> 11)·2⁻⁵³ ∈ [0, 1); n = √(−2 ln u₁)·cos(2π u₂); ε_t = 0.1·SD(ζ)·n. The sin output is never computed or cached. This is a discretized normal, truncated at |n| ≤ 8.571674 (finite-precision convention; RL4 L71). Uniforms for 'action': u = (w >> 11)·2⁻⁵³.

### 5.3 Known-answer tests (pure Python and numpy 2.5.4 agree on every block below)

| Input | Output |
|---|---|
| Philox4x64-10, ctr 0⁴, key 0² | 16554d9eca36314c db20fe9d672d0fdc d7e772cee186176b 7e68b68aec7ba23b |
| Philox4x64-10, ctr (2⁶⁴−1)⁴, key (2⁶⁴−1)² | 87b092c3013fe90b 438c3c67be8d0224 9cc7d7c69cd777b6 a09caebf594f0ba0 |
| Philox4x64-10, ctr (243f6a8885a308d3, 13198a2e03707344, a4093822299f31d0, 082efa98ec4e6c89), key (452821e638d01377, be5466cf34e90c6c) | a528f45403e61d95 38c72dbd566e9788 a5a1610e72fd18b5 57bd43b5e52b7fe6 |

CNA recalls these three as Random123's published philox4x64-10 vectors; the match must be confirmed against Random123's kat_vectors file at code freeze.

**TEST VECTOR ONLY: placeholder master seed = 128 zero bits. This is NOT the master seed.**

| (row, rep, seed, root, t), role rewcorr-eps | K (first 16 bytes of D, hex) | w0, w1 | u₁, u₂ | n |
|---|---|---|---|---|
| (REW-CORR-E, 0, 0, 0, 1) | 6fe46d1da8b7dff11566befd56411be3 | 46cf5ccaa7969b4a, 7a94a9ca99d8c463 | 0.2766016001474676, 0.4788309211379298 | −1.5890715417720278 |
| (REW-CORR-E, 0, 0, 0, 2) | same K | 42dc23849313b266, a014023cf137af3d | 0.26117155062372788, 0.62530530917976412 | −1.1564717230084798 |
| (REW-CORR-E, 0, 0, 1, 1) | fc90d1e378b5c4589e4642d77cba3c8b | 519ec3950e8719a0, bc6925734affccf3 | 0.31882879628258509, 0.73597940506715454 | −0.13302759504601161 |
| (REW-CORR-I, 0, 0, 0, 1) | c3d728bc26a5968b38b1e75c277fd718 | 7c588d217b870331, 5d171bc8b677926a | 0.48572618548817215, 0.36363385820592797 | −0.78696932322819335 |

Canonical encoding (first row), hex: 000000114143492d547261636b422d524e472d763100000010000000000000000000000000000000000000000a5245572d434f52522d450000000800000000000000000000000800000000000000000000000b726577636f72722d657073000000080000000000000000

Audits (#48 L136) distinguish **domain reuse** (duplicate canonical tuples, detected by exact comparison of encodings) from **hash collision** (distinct encodings with equal K: birthday bound under the uniform-hash model only). Non-persistence rests on the state and readout restrictions and their audits (#48 L124).

### 5.4 Master seed: ruling

- **(a) ADOPT** the Lead's derivation: master seed = the first 128 bits (bytes 0–15, big-endian) of SHA-256 of the frozen calibration spec's bytes, computed once at freeze and written into the freeze record. **ADOPT** RD's two sentences: "Exactly one spec hash is ever registered." "No plant or harness code has run with any candidate seed before freeze." **ADOPT** RL4 L81: never derived from wall clock, process, thread or host identifiers, OS entropy, worker or completion order, or any run-time quantity. A re-run uses the same value. Every role derives its key only through §5.1 with a distinct role tag; no role uses the master seed directly as generator state.
- **(b) Circularity.** The spec cannot contain its own seed. The seed therefore lives only in the freeze record, which is hashed separately, and the freeze manifest lists both hashes (spec, freeze record).
- **(c) Grinding.** RD's sentences are attestations and cannot be verified: cosmetic spec edits could be dry-run before sealing. **OPTIONAL, for the Lead or Astra to choose:** seed = first 128 bits of SHA-256(spec_hash_bytes ‖ uint64-BE(R) ‖ beacon_value_bytes). R is a public randomness-beacon round (e.g. drand League of Entropy, chain hash declared) that is fixed in a timestamped, append-only freeze-record entry before round R is published. The beacon value is fetched once after publication and recorded in the freeze record; no network is used at run time. Anyone can verify the round's value and its signature. The commit's "before" relies on an external timestamp (e.g. a pushed commit), which should be stated. Not required.
- The seed does not yet exist. §5.3 uses the labelled all-zero placeholder only.

## 6. Governance note (CNA concern, recorded; no action taken)

The constitution reserves gate relaxation to a human: "Human authorization is required for fundamentally new architecture families, scale-ups, organism re-entry, first C4/C5/C6 studies, ACO-definition changes, gate relaxation and phenomenal/philosophical inference." (CON L153–L155; repo copy 50bdfb54…, last changed in commit a72136c, 2026-10-01). The 2026-10-21 standing delegation ("I'm approving everything you deem necessary as Research Lead", CKAPPA_STANDING_APPROVAL_APPLICATION_RL.md L5) is general, and it does not name CON L153–L155. Astra declined to certify which rule governs (#48 L36). **CNA recommends that GA-1, and any constitution amendment that relies on the delegation, receive Aidan's explicit approval rather than resting on the delegation.** The draft note at A L46 should therefore ask for approval, not only inform. That decision belongs to the Lead and Aidan.

## 7. Summary of CNA rulings

| Item | Ruling |
|---|---|
| Correction (λ^50 = 0.364170; error λ^t·μ/s) | Acknowledged; r̄_std choice unchanged |
| Degeneracy | Population ρ_E = 0 **proven** for the pinned construction; finite-sample all-D **not provable** (approximate P(ND) up to 0.10 at ρ = 0.5, d_ws = 6, n = 800); criterion redesigned per cell |
| GA-1 | Pooling unit = outer replicate; minimum 36 Q replicates; N → real_i = 0; D = UNDEFINED, "did not issue MET" |
| PZ7 §1.4 cell | Amended text §2.3 |
| R22 | **Per seed** (traced to MP L67/L73/L74/L80); 112 superseded; n_s = 127 per (seed, bin), final partition (partition ABSENT, proposed) |
| IGN F-1 to F-10 | §3; binomial justified by reset-independent trials plus Hoeffding 1956; exact table §3.1; 67 = budget only |
| E48-4 / RL4 | Items 1–5 adopted (2 with amendment); Philox4x64-10, mapping and KAT fixed |
| Master seed | Lead derivation + RD sentences adopted; optional beacon; placeholder used in tests only |
| Governance | Explicit Aidan approval recommended for GA-1 (CON L153–L155) |

sha256 of all content above this line: 67af7d1b42e85d6291c43c7975a0048b0d34a75891621b007ecf3b169db82548
