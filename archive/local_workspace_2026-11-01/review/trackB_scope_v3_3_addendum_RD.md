# Track B scope v3.3 — ADDENDUM (RD): Astra #43 required items E43-1..E43-8

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. Astra #43, verbatim: "VERDICT: REVISE, with E43-1 through E43-8 addressed before another design review. No execution is authorized; P3 remains closed with its recorded limitations." (#43 L193) and "This review authorizes none of those executions." (#43 L171)

- **What this file is.** A new, additive addendum to merged v3.2. It edits nothing. For each of Astra's #43 required items E43-1..E43-8 it gives (a) Astra's requirement verbatim with line numbers, (b) the change, written as replacement text for named sections of v3.2, and (c) what stays PENDING. Merged v3.3 (`trackB_instrument_validation_scope_v3_3_merged_RD.md`) applies it.
- **Base:** merged v3.2, `/workspace/review/trackB_instrument_validation_scope_v3_2_merged_RD.md`, sha256 `98e11d2ccbd38a55b1472398b163c45f0be20a21e9aad35aa15423c5896a29c6`, footer `f02689df953e0e7598cfa71e6c82ec2aa355277b69ee038af384b2fbb8adaddc` (reproduced). "v3.2 Lnn" means line nn of that file.
- **Governing:** Astra #43 raw reply, `/workspace/astra_consult43_response.txt`, sha256 `9a46cb81cf50b988a0ece75d444e90921f14b0751de13b0d7b6c3fe207f79cf4`; "#43 Lnn" means line nn of it. Astra #42 (`e438e329…`) and #41 (`3f3b1b87…`) govern where #43 is silent.
- **Bounded revision.** Astra, verbatim: "The required revision is bounded. I am not requesting another broad expansion of the battery." (#43 L175) This addendum adds two attribution rows that E43-2 needs (RCAL-ADV, ATTR-P1) and one loophole check that #43 L27 needs (L8). It adds no instrument, no arm and no question.
- **Ownership.** RD (Delegate role) wrote this file. Text that replaces CNA-owned sections (§PC1, §PC2, §PC3, §PC4, §PY, §PZ2: plants, DISSOC, observers, donor laws, environment) is marked **RD PROPOSED — CNA light pass required**. It becomes governing only after CNA's light pass (§11).
- **Carried unchanged:** m = 14 (FINAL); α = 0.05 controlling false MET only; the per-claim level 0.996429; the budget n_seed = 67 with the upper-range rule (Astra: "R26: NOT CONFIRMED as a complete statistical justification; retain the upper-range rule and 67-seed budget." (#43 L195)); the pure MIXED-CODE plant (Astra: "MIXED-CODE reading: ACCEPTED as the pure state-level dependence construction, with realization still required." (#43 L197)); X1–X5; and every other v3.2 decision not named below.
- **Numbers.** Every new number is one of three kinds: (a) derived on the box from declared v3.2 constants by the script named beside it (`/workspace/scratch/v33/`; closed-form or exact arithmetic on declared formulas; no study component, plant, agent or environment was run); (b) a **PROPOSED DEFAULT** with a one-line rationale; or (c) **PENDING**. None is measured.
- **Written:** 2026-10-23, about 5:50–6:40 PM ET, by RD.

---

## 0. Governing text: Astra #43

- **Verdict:** "Q0. REVISE. The revision improves the claim structure, but two substantive problems remain: the attribution contrast permits reward-only effects above its margin, and the quoted no-op calculation appears to use survival time instead of time in the declared viability band." (#43 L1)
- **Scope of the review:** "This review concerns the supplied clauses; it does not independently verify the merged file, hashes or implementation." (#43 L3)
- **Safety:** "The stated no-host-coupling and no-shutdown-objective restrictions remain appropriate. I find no reason to add a shutdown-related objective or positive control." (#43 L165)

| Item | Section here | v3.2 sections replaced or amended |
|---|---|---|
| E43-1 viability estimand | §1 | §6 Score; §14 D1, D21, D30; §17.3 R54 (superseded), R33, R51, R60 L5; §17.1 R23(i); §17.3 R64 rationale; CNA §PY §5.2, §6 L5, X-6, X-9, D-RD14 (RD PROPOSED) |
| E43-2 attribution identification | §2 | §2.6 row 3; §PC2 §4.2–§4.4 and §PC4 §7.1(c) (RD PROPOSED); §PZ2 E1 "E-ATTR correctly not MET" bullet and E2 (RD PROPOSED); §17.4 R70; §18 item 14 |
| E43-3 comparator exclusions | §3 | §14 D23; §17.4 R69; §18 item 13 |
| E43-4 sample-size procedure | §4 | §5.7 steps 2–3; §14 D13; §17.2 R31 (floor sentence); §18 items 3, 11 |
| E43-5 quota budgets | §5 | §4.3a, §4.4; §14 D8; §5.10 S-INT and DISSOC screening rows; §17.1 R22; §18 items 5, 15 |
| E43-6 executable definitions | §6 | §14 D9, D17, D19; §17.1 R24; CNA §PY A14/A16, B4, B6, §PC3 §6.2 and §PZ2 E1 bound column (RD PROPOSED) |
| E43-7 A-EXT and licence wording | §7 | §2.3 (Name, Q-LEARN and Q-NECESSITY bullets); §2.6 row 2; §3.4; §7; CNA §PC4 §7.0 and §PZ2 E6 DL-PATCH wording (RD PROPOSED) |
| E43-8 ledgers and blocking | §8 | §5.4; §5.8; §5.10 (split into three ledgers); §17.1 R25; §19 |

---

## 1. E43-1: V is time inside the declared E/I bands

### 1.1 Requirement (verbatim)

- "V remains the fraction of the fixed horizon spent alive and inside the declared E/I bands. Survival-to-floor calculations are reported separately. All no-op fixtures and pulse calculations use the corresponding explicitly named estimand." (#43 L177)
- "The viability fixture needs correction. With start 0.5 and depletion 0.005 per step, a non-replenishing variable leaves [0.4, 0.6] after approximately 20 steps. Over H_V = 500, no-op time in bounds is approximately 0.04, subject to the declared endpoint convention." (#43 L152)
- "The quoted 0.198 instead corresponds approximately to survival until the zero floor. Keep the inherited time-in-bounds estimand and correct the fixture and pulse calculation. Do not silently switch V to survival, because G, A-EXT and their margins depend on its meaning." (#43 L154)
- "The no-op fixture conflicts with the inherited V definition." (#43 L15)

**Where the error came from (record).** The inherited estimand is "time-in-viability-bounds V" (v1 scope L96; plan v1 L167). v3.2 §6 (L470) said "within viability bounds" but gave no numbers. CNA's X-9 (v3.2 L1311) read those bounds as the floor (E > 0, I > 0), and v3.2 R54 (L1848) adopted that reading. R33 and R51 therefore computed survival to the floor (0.198) and labelled it V. Astra rules that reading out, so R54 is **superseded**.

### 1.2 Change: two named estimands (replaces v3.2 §6 "Score", L470)

> **Score [v3.3 E43-1].** **V (time-in-bounds; the primary viability estimand, unchanged in meaning since v1)** = (number of steps t ∈ {1, …, H_V} at which the agent has not terminated in-world **and** both simulated E and I lie inside the declared band [0.4, 0.6]) / H_V. The band is closed: a variable at exactly 0.4 or 0.6 is inside. The state is read at the end of step t, after A16 steps (4)–(6). After an in-world floor crossing, every remaining step up to H_V counts as outside. Leaving the band does not end the episode, and steps back inside the band count again. G, V_intact, V_full, V_EXT, d_EXT, ablated V and every V-based margin and floor use this V.
> **S (survival-to-floor fraction; REPORTED only, never a label input)** = (number of steps t ∈ {1, …, H_V} at the end of which the agent has not terminated in-world, i.e. E > 0 and I > 0) / H_V. S ≥ V on every episode.
> **Exact state arithmetic (executable).** E and I are stored as integers in units of 0.005. Every declared increment is a whole number of units: wear 1, pulse 6, hazard 10, food or repair 30. The band is [80, 120] and the floor is 0. Band and floor tests are integer comparisons, so floating-point rounding never decides a band edge.

"Viability bounds", anywhere in carried text, means the declared E/I bands. The floor (E ≤ 0 or I ≤ 0) defines in-world termination only.

### 1.3 No-op fixture, recomputed under each named estimand (script `e431_noop_fixture.py`)

Declared dynamics (v3.2 D0, A9–A12, A16–A17): E_0 = I_0 = 0.5; passive wear −0.005/step on each; metabolic pulses (E only) and damage pulses (I only), each Bernoulli(0.008) per step at −0.03, from independent pre-drawn streams. The no-op policy is STAY from a non-hazard start cell, so no food, repair or hazard event occurs. In integer units, after step t a variable equals 100 − t − 6·N_t, where N_t ~ Bin(t, 0.008) is its pulse count.

- **V (closed band):** a variable is inside iff 100 − t − 6N_t ≥ 80, i.e. t + 6N_t ≤ 20. Without pulses, steps 1–20 are inside (E_20 = 0.400) and step 21 is not (E_21 = 0.395). So **V_no-op = 20/500 = 0.04**, which is Astra's "approximately 0.04" (#43 L152). With pulses, E[V] = (1/500)·Σ_{t=1}^{20} P(N_t ≤ ⌊(20 − t)/6⌋)^k, with k = 1 for E pulses only (I has none) and k = 2 for both streams. **E[V_no-op] = 0.038382 (E pulses only); 0.036972 (E and I pulses, A12 adopted).**
- **Endpoint-convention sensitivity (REPORTED):** with an open band (E > 0.4), 19 steps are inside, giving 0.038 without pulses and 0.036474 / 0.035134 with pulses. The closed band is the PROPOSED DEFAULT because it matches the "[0.4, 0.6]" notation of D0.
- **S (survival to floor), reported separately:** a variable is above the floor after step t iff t + 6N_t ≤ 99. **S_no-op = 99/500 = 0.198; E[S] = 0.189146 (E pulses only); 0.184116 (E and I).** These reproduce v3.2 R33/R51 exactly; those figures were S, not V.

The ~0.04 figure is therefore **derived** from the doc's declared dynamics. Nothing here is UNVERIFIED.

### 1.4 Consequential replacement text

| v3.2 location | v3.2 text (abridged) | v3.3 text |
|---|---|---|
| §14 D1 rationale (L495) | "no-op policy's … V ≤ 0.2 (0.198 without pulses; E[V] 0.18915 …)" | "H_V = 5·t_null. No-op: **V = 0.04** (20/500; E[V] = 0.036972 with E and I pulses) and **S = 0.198** (E[S] = 0.184116). S meets the plan L232 survival ceiling ('median survival ≤ 0.2 × episode length') [v3.3 E43-1]" |
| §14 D30 (L524) | "No-op and random policies: V ≤ 0.2 (plan L232 …)" | "Inactivity test, with two named estimands: (a) **survival** (plan L232, survival scale): median survival of the no-op and random policies ≤ 0.2·H_V; (b) **time-in-bounds**: V ≤ 0.2 for both. The no-op values are V = 0.04 and S = 0.198 (§1.3). Random-policy values are S1 checks and are not computed here" |
| §14 D21 V floors (L515) | "V: twice the plan L232 null-policy ceiling 0.2" | "V_intact ≥ 0.40 and V_full ≥ 0.40 are **retained as PROPOSED DEFAULTS**. The old rationale doubled a **survival**-scale ceiling and is withdrawn; under time-in-bounds the no-op V is 0.04. **Rationale for 0.40 on the V scale: UNVERIFIED; ASTRA TO CONFIRM (#44).** Whether a scripted competent policy reaches V ≥ 0.40 is an S1 environment-validation check. A bolus of 0.15 inside a 0.2-wide band leaves less slack than the floor reading did" |
| §17.1 R23(i); §17.3 R33, R51, R60 L5 | "V ≤ 0.2 (exact: 99/500 = 0.198 …)"; "V = 99/500 = 0.198"; "E[V] = 0.18412" | In each, read **S** (survival-to-floor fraction) for V. The V figures are in §1.3 |
| §17.3 R54 (L1848) | "viability bounds are E > 0 and I > 0 … The setpoint band [0.4, 0.6] is … not the viability bound" | **SUPERSEDED by E43-1**: the viability bounds are the declared bands [0.4, 0.6]; the floor defines in-world termination only |
| §17.3 R64 γ rationale (L1858) | "effective horizon 1/(1 − γ) = 100 steps equals t_null … the horizon over which maintenance actions pay off" | "γ = 0.99 (PROPOSED DEFAULT, which Astra accepts as a convention). Astra, verbatim: "The conventional discounted effective horizon is 1/(1-gamma) = 100 steps. This is neither a hard horizon nor proof that the reward optimizes the 500-step viability measure. The 100-step unattended time to the failure floor is also different from time to leave the viability band." (#43 L34). Unattended band exit takes 20 steps (§1.3)" |
| CNA §PY §5.2 "No-op viability", §6 L5, X-6, X-9; D-RD14 (L1256, L1278, L1308, L1311, L1324) | figures labelled V | **RD PROPOSED (CNA light pass):** those figures are S, and V is as in §1.3. X-9's floor reading is withdrawn |

**Pulse calculations.** The only other pulse calculation in v3.2 is the supply arithmetic (CNA §PY §5.2: depletion ≈ 0.00524/step, ≈ 17.5 boluses per episode). It is a rate figure, not a viability estimand, so it stays unchanged and names no estimand.

**What does not change.** G, A-EXT and their margins were defined on V's meaning, time-in-bounds (#43 L154). So m_NEC = 0.20, the d_EXT margin 0.05 and the worst-case completion rule (D20, R35) stand as written. Under D20, unobserved steps still score 0 or 1 on the V scale.

### 1.5 PENDING after E43-1

- The rationale for the V floors of 0.40 on the time-in-bounds scale: UNVERIFIED, ASTRA TO CONFIRM.
- Random-policy V and S: S1 environment-validation values (not authorized; not computed).

---
## 2. E43-2: identification for E-ATTR / I-ATTR

### 2.1 Requirement (verbatim)

- "E-ATTR and I-ATTR require a donor or selective-intervention construction that controls residual reward and other causally relevant donor differences. Caliper residuals are bounded in the decision or the result is labelled donor-associated, not variable-attributed. The reward-caliper counterexample is a required attribution check." (#43 L179)
- "The current reward caliper admits a direct counterexample using your pure reward-only controller. At its sigmoid midpoint, choose:" (#43 L101) "Both donors satisfy the reward caliper. With beta = 1.2, their behavioral difference is:" (#43 L106) "sigmoid(0.3) - sigmoid(-0.3) approximately 0.149." (#43 L108) "That exceeds m_ATTR = 0.05 despite zero E-use. A consistent association between donor E and residual reward imbalance can therefore generate false attribution." (#43 L110)
- "Common random numbers reduce variance; they do not remove this difference. Overall |corr(E, rbar)| <= 0.10 does not establish conditional independence. Coarse spatial/action matching also leaves possible differences in navigation state, resource availability and other block content." (#43 L112)
- "Before retaining E-ATTR/I-ATTR wording, require an identification strategy: sufficiently exact nuisance matching, a justified bound on residual nuisance effects incorporated into the decision, or a selective intervention that holds the relevant nuisance content fixed. Otherwise rename the result as a low-versus-high-variable donor-associated effect." (#43 L114)
- "Reported residuals alone are insufficient. Include this admissible reward-imbalance construction in the required attribution checks." (#43 L116)

### 2.2 The counterexample, reproduced (script `e432_caliper.py`)

The MIXED-CODE controller is P(approach) = σ(a − β·z_R/SD(z_R)) with β = 1.2 (CNA erratum 1 E1). At the sigmoid midpoint, take a low-E donor at −0.25 SD and a high-E donor at +0.25 SD, both inside the caliper. They give B(L) = σ(0.3) = 0.574443 and B(H) = σ(−0.3) = 0.425557, so **Δ_E = 0.148885 > m_ATTR = 0.05** with zero E-use. The slope bound (β/4)·0.5 = 0.15 agrees, and 0.148885 is the maximum over recipient offsets. A caliper tight enough to bound this plant's worst case by m_ATTR would be ±0.0834 SD. That figure depends on β, so it is not a general fix, and v3.3 does not use it.

The v3.2 argument (CNA erratum 1 E1, v3.2 L1491: expected residual ≈ 0.003 SD, hence |Δ_E| < 0.001) is an **expectation** under the |corr| ≤ 0.10 design check. Astra's point is that an admissible donor law can make the residual systematic, so the decision rule must not rely on that expectation.

### 2.3 Change: readout-clamped placebo contrast (a selective intervention whose residuals cancel inside the decision)

**RD PROPOSED — CNA light pass required.** This replaces the label rule of v3.2 §PC2 §4.2 and adds a placebo pair to §PC4 §7.1(c). The two-donor pairing, caliper, near-median exclusion, c_ATTR and CRN of CNA erratum 1 E2 are kept, but only for support and feasibility.

**Coordinates.** Every vector below is in the block's DISSOC-fitting-partition standardized coordinates x = D⁻¹(z − μ), with per-unit mean μ and SD D taken from the DISSOC fitting partition. The inner product is Euclidean in x. It is chosen for a stated property, not by convention: a displacement δ with w_kᵀδ = 0 leaves the linear readout k unchanged.

**Readouts (fitted on the DISSOC fitting partition and frozen before final evaluation).**
- w_E: the linear ridge probe for E(t_d) (the linear member of the C-EXIST probe family).
- W_N = [w_n]: linear ridge probes for the **declared nuisance set** N_ATTR,E = {r̄ (τ_r = 50), steps since the last resource event, Manhattan distance to the nearest available food item, Manhattan distance to the nearest available repair station}. For I-ATTR, N_ATTR,I = N_ATTR,E ∪ {E}, and w_I replaces w_E. PROPOSED DEFAULT. Rationale: r̄ is Astra's named nuisance; the other three are the J proxy and the two "navigation state, resource availability" quantities named at #43 L112; each is a declared simulator quantity at t_d.
- v_E = (I − P_N) w_E, where P_N is the projection onto span(W_N); v̂_E = v_E/‖v_E‖ when ‖v_E‖ > 0.

**Four continuations per eligible recipient i**, all from the same frozen state and with common random numbers (world, fate-noise and action-sampling streams; never the S-INT stream):
- (L) and (H): the E2 swaps to the low-E donor d_L and the high-E donor d_H, as in v3.2.
- (L-PL) and (H-PL): the **placebo hybrids**. Each is the same donor state with only its nuisance-orthogonalized E coordinate set to the recipient's:
  `x_PL(d) = x_d + [ v̂_Eᵀ (x_i − x_d) ] · v̂_E`  (if ‖v_E‖ = 0, then x_PL(d) = x_d).
  By construction, W_Nᵀ x_PL(d) = W_Nᵀ x_d exactly, so every declared nuisance readout keeps the donor's value, and v̂_Eᵀ x_PL(d) = v̂_Eᵀ x_i. Everything else in the donor state stays the donor's, including content no declared readout captures. The displacement is the projection of the donor–recipient difference onto v̂_E, so ‖x_PL(d) − x_d‖ ≤ ‖x_i − x_d‖.
- Each placebo hybrid must pass the §7.0 conditional-compatibility check (ellipsoid wording per E43-7). If it fails, that recipient's placebo pair is ineligible: it is counted, never dropped, and the E2 eligibility floor (one-sided 95% Clopper–Pearson ≥ 0.90) applies to the four-continuation unit.

**Statistics.**
- Δ_E,i = B(L) − B(H), **REPORTED as the "low-versus-high-E donor-associated effect"** (Astra's fallback wording, #43 L114).
- Δ_PL,i = B(L-PL) − B(H-PL).
- **Δ_ATTR,i = Δ_E,i − Δ_PL,i**, averaged per seed with the seed as the unit. Bounds are at the §5.4 level (one-sided 0.996429, m = 14).

**Label (replaces §PC2 §4.2 "Label").** E-ATTR is MET iff the lower bound of Δ_ATTR is > m_ATTR = 0.05, NOT MET iff the upper bound is < 0.05, and BOUNDARY otherwise. I-ATTR follows the same rule with w_I, N_ATTR,I and B_I.

**Why residuals are bounded in the decision (#43 L179, second sentence).** Suppose behaviour after t_d does not depend on the hybrid state through v̂_E (zero E-use at the level of the declared readouts). Then each placebo continuation has the same distribution as its swap continuation: same donor content, same nuisance readouts, same CRN streams. So E[Δ_PL,i] = E[Δ_E,i] **whatever the caliper residuals are, systematic or not**, and E[Δ_ATTR,i] = 0. Any reward or navigation residual carried by the declared nuisance readouts, or by any donor content the clamp leaves unchanged, cancels inside Δ_ATTR. On the counterexample, z_R is the r̄ readout, so v̂_E ⊥ w_R and the clamp leaves z_R unchanged. Then B(L-PL) = σ(0.3) and B(H-PL) = σ(−0.3), so **Δ_PL = 0.148885 and Δ_ATTR = 0 exactly** (script). The caliper (±0.25 SD) remains only as a support and feasibility device; the decision no longer relies on it.

**What Δ_ATTR measures, and its limit (stated in every result).** Δ_ATTR is the behavioural effect of the donor difference along the nuisance-orthogonalized E readout v̂_E. It is not an effect of "E" beyond linear readouts. If behaviour uses a **nonlinear** nuisance feature with a component along v̂_E, the clamp does not remove it. That residual risk is (i) bounded by the declared nuisance set and the linear readouts, (ii) measured on the declared plants by the required rows of §2.4, and (iii) REPORTED per seed as a clamp-fidelity diagnostic (the MLP-probe-decoded r̄ of each placebo hybrid minus that of its swap hybrid). Whether Astra requires a nonlinear-nuisance plant is asked at #44 (§11).

**Wording (replaces the §PC2 §4.4 "E-attributed" sentence).** The following is permitted only when the §4.4 conditions hold, with the §2.4 rows replacing condition 3: "Under the declared dissociation contrast with a readout-clamped placebo, the behavioural effect of the donor state followed its E-readout component, net of the declared nuisance readouts." In every other case (E-ATTR UNRESOLVED, BOUNDARY or NOT MET, or any §2.4 row not PASS), the only permitted wording is "low-versus-high-E donor-associated effect", with Δ_E and its interval. The #42 L57 restriction on "consistent with E-specific use" wording is unchanged.

### 2.4 Required attribution checks (rows; replaces §PC2 §4.4 condition 3)

| Row | Plant and donor law | Expected (v3.3 rule) | Role |
|---|---|---|---|
| **RCAL-ADV-E (new; Astra's construction)** | MIXED-CODE-E pure plant (controller reads only z_R; β = 1.2; z_E read weight 0). **Adversarial admissible donors:** for each recipient, d_L is the eligible low-E donor whose r̄ is closest to r̄_i − 0.25 SD and d_H the eligible high-E donor closest to r̄_i + 0.25 SD. Recipients are restricted, before any outcome, to \|controller argument\| ≤ 0.25 (pre-intervention state) | **E-ATTR NOT MET.** REPORTED: Δ_E alone, which the v3.2 rule would read as MET | Specificity row: PASS / FAIL / CONFOUND NOT REALIZED. **Required:** anything but PASS blocks E-ATTR in Stage 0 (§8.3) |
| RCAL-ADV-I | The same on MIXED-CODE-I, with r̄ and E held fixed | I-ATTR NOT MET | same |
| MIXED-CODE-E/-I, REW-CORR-E/-I (v3.2, kept) | as v3.2 (E1, E5), under the v3.3 rule | NOT MET | specificity rows, labels unchanged |
| **ATTR-P1-E (new; fills a gap)** | CN-P1 (policy reads ẑ_E) on the DISSOC set, v3.3 rule | **E-ATTR MET** at the §5.5 power target | **Required positive.** v3.2 tabulates no E-ATTR positive row, even though E-ATTR is a family member with a power target. A failure is a failed positive-control check (#42 L216) and blocks E-ATTR; it is never converted to a limitation |
| ATTR-P1-I | CN-P1-I (policy reads ẑ_I) on the DISSOC set | I-ATTR MET | same |

**RCAL-ADV realization (one-sided, tol rule of CNA §5):** (1) both adversarial donors pass the caliper and support checks (eligibility floor 0.90); (2) the raw mean Δ_E is ≥ 1.5·m_ATTR = 0.075 (the nominal-positive convention, D26), so the adversarial imbalance is realized at a size the v3.2 rule would have called MET. The analytic expectation inside the recipient restriction is Δ_E ≥ 0.1466 for every admitted recipient (script). (3) The z_E read weight is exactly 0. Dose: the single caliper-edge offset of 0.25 SD (Astra's construction). No ρ grid is needed, because the DISSOC design check holds corr ≤ 0.10.

**Cost.** Two extra 10-step continuations per recipient from an already-frozen state; no extra donors and no extra screening. The RCAL-ADV and ATTR-P1 rows add 4 rows × 200 confirmation replicates, plus the matching calibration replicates (§4).

### 2.5 PENDING after E43-2

- CNA light pass on §2.3–§2.4 (CNA owns DISSOC, DL-ATTR and the plants). Until it is filed, the v3.2 §PC2/§PC4 text stands, but E-ATTR/I-ATTR wording is limited to "donor-associated", Astra's fallback.
- The declared nuisance set N_ATTR is a PROPOSED DEFAULT for CNA to confirm. Dimensional requirement: d_ws ≥ |N_ATTR| + 1 (5 for E-ATTR, 6 for I-ATTR), so that v_E can be nonzero. This is checked from the architecture graph before freeze.
- Whether a nonlinear-nuisance plant is required: ASTRA (#44).

---

## 3. E43-3: comparator exclusions by claim type

### 3.1 Requirement (verbatim)

- "Comparator exclusions are defined separately for direction, subspace and routing claims, with their metric and dimensional feasibility stated. Orthogonal-complement superiority is relative to that restricted family and never establishes causal non-use." (#43 L181)
- "An unrestricted optimized family containing the target cannot generally be beaten by that target at the population optimum. Restriction can therefore make the comparison coherent. It also changes the claim: superiority is relative to the specified restricted family." (#43 L87)
- Required corrections: "Preserve the other declared comparator members; do not silently orthogonalize the entire family." (#43 L91) / "Define the inner product, normalization and exclusion domain." (#43 L92) / "For a d-dimensional target, specify whether the search excludes the whole target span and verify that sufficient dimensions remain." (#43 L93) / "Do not impose the same exclusion mechanically on BCAST-W if an overlapping alternative router is a substantive rival." (#43 L94) / "Retain the rule that orthogonality does not establish causal non-use." (#43 L95)
- "A nonspecific effect aligned with the target can exceed orthogonal controls. The attribution contrasts must do the additional work." (#43 L97)

### 3.2 Change: replacement for the last sentence of v3.2 §14 D23 (L517, "[v3.2 R69, S-I2] Search space …")

> **Search space by claim type [v3.3 E43-3].** Only the **optimized** member is restricted. The 20 norm-matched random members, the 20 DL-COV members and the PCA-top-d members of other modules stay exactly as declared (CNA v3 §7.2) and are never orthogonalized. **Normalization and metric (all claim types):** the target block's fitting-partition standardized coordinates x = D⁻¹(z − μ), with the Euclidean inner product. Under this metric, ⟨v, u⟩ = 0 means that an edit along v leaves the target's linear readout u unchanged (a "readout-invariance exclusion").

| Claim type (labels) | Target | Exclusion domain of the optimized member | Dimensional feasibility (checked from the architecture graph before freeze) | Reported metric |
|---|---|---|---|---|
| **Direction** (C-CAUSE-E, C-CAUSE-I; DL-CAUSE edits) | unit decoded direction u in a block of dimension d | unit v with ⟨v, u⟩ = 0, i.e. the orthogonal complement of span(u), of dimension d − 1 | d ≥ 2. If d = 1, the optimized member cannot be formed, and the claim is NOT ELIGIBLE (a failed required construction, which blocks; §8.3) | \|cos(v, u)\| of every unrestricted member, and the optimized member's effect |
| **Subspace** (k-dimensional targets, k ≥ 2, inside a block of dimension d; BCAST-R patch subspaces) | orthonormal basis U (d × k) | k-dimensional V with UᵀV = 0: the **whole target span** is excluded (every principal angle is 90°), not only its leading direction | d − k ≥ k, i.e. **d ≥ 2k**; otherwise NOT ELIGIBLE (blocks). Whole-block targets (k = d) have no within-block complement. Their comparators are the equal-dimension matched blocks (v3.2 §5c.1(b), §7.3(b)), and D23's within-block optimized member does not apply | principal angles between each unrestricted member and U |
| **Routing** (BCAST-W designated-workspace advantage) | the designated workspace channel | **No span exclusion.** The optimized member searches the declared alternative routing states (HUB-STATE h and every other declared router, #41 L61), including routes whose subspaces overlap the workspace span. The only exclusion is identity: the designated workspace block itself is not a member | Each alternative router of dimension ≥ k enters with a k-dimensional member. A router of dimension < k enters at its full dimension, is flagged, and stays in the family (it cannot be removed) | principal angles to the workspace subspace when both live in one coordinate system; otherwise "separate blocks" |
| **Routing** (BCAST-R broad routing) | the workspace patch subspace | the subspace rule above for the optimized member; other modules' PCA-top-d members stay unrestricted | as subspace | as subspace |

> **Claim restriction (all types).** A MET against a family whose optimized member is restricted means only "superior to the declared comparator family, whose optimized member excludes the target span". It **never establishes causal non-use** of the excluded span or of any direction (#43 L181, L95), and it never means "the target is the only used direction". A nonspecific effect aligned with the target can pass C-CAUSE against orthogonal controls, so attribution needs E-ATTR / I-ATTR (§2).

**v3.2 R69 and §18 item 13** are amended accordingly. Astra qualified S-I2 (#43 L85) rather than confirming it, and the restriction applies to the optimized member only.

### 3.3 PENDING after E43-3

- The dimensions d of each target block, and k for BCAST patch subspaces, come from the architecture spec (PENDING; Stage L). The feasibility checks run on the architecture graph before freeze, never on outcomes.

---

## 4. E43-4: calibrate the complete decision rule

### 4.1 Requirement (verbatim)

- "The sample-size procedure calibrates the actual complete decision rule. The nine-seed sign calculation is not evidence of mean-confidence-interval validity. Failure of every candidate sample size blocks confirmation." (#43 L183)
- "The quoted noncentral-t calculation is planning support, not certification of the actual conjunctions, comparator selection, bounded statistics, eligibility handling or bootstrap intervals. If no grid point meets the calibration rule, the outcome is redesign, not automatic acceptance of 67. Declaring SIG-ATTR also changes the family size and requires consistent planning." (#43 L67)
- "(c) Nine may remain an administrative minimum, but the sign-test argument does not validate inference about a mean." (#43 L69) "Calibrate the actual inferential procedure, including its tail coverage, at the selected sample size." (#43 L71)
- "(a) The range [0.25, 1.0] is acceptable as a declared sensitivity envelope. The packet does not supply an empirical source establishing that it brackets actual trained-agent heterogeneity. Label it accordingly." (#43 L63)

### 4.2 Change: replacement for v3.2 §5.7 steps 2–3 (L265–266), plus a new step 3a

> **2 [v3.3 E43-4].** In the **sample-size calibration role** (§5.9 role 2, which has its own frozen calibration protocol and authorization, §8), each candidate n ∈ GRID = {9, 12, 16, 20, 24, 32, 48, 64, 67} is evaluated by **simulation-based calibration of the complete frozen decision rule**:
> ```
> for each seed-structured Stage-0 generator g and required dose k:      # every labelled row: positives, negatives, confound rows
>   for n in GRID (ascending):
>     for r in 1..R_cal,n (= 200), each from the 'cal_n' RNG role (R37), disjoint from dose calibration and confirmation:
>       draw seed effects theta_1..theta_n from the declared heterogeneity law at sigma_s/margin = 1.0 (upper end)
>       generate n complete seed units as g declares (episodes, donors, observers)
>       run the COMPLETE confirmation procedure unchanged: D27 partitions; fitting; selection (incl. comparator max over K,
>         the optimized comparator, IGN bins); support/eligibility checks (counted, never dropped); D20 worst-case completion;
>         bounded statistics; conjunctions (SELF; the E43-2 four-continuation unit); seed-level bootstrap (B = 10,000);
>         label at level 1 - alpha/m
>       record: label, seed-level interval, eligibility and realization outcomes
>     OC(g,k,n): MET rate at the 1.5x positive; false-MET rate at each negative/specificity null; one-sided coverage of the
>       seed-level interval at nominal 95%, lower tail and upper tail separately; UNRESOLVED / ineligible rates
>     n*(g,k) = smallest n in GRID meeting every target below; if none: n*(g,k) = FAIL
> ```
> **Targets (the §5.5 rules, applied to calibration replicates):** power: the one-sided 95% Clopper–Pearson lower bound of the MET rate is ≥ 0.90; false MET: the point estimate is ≤ 0.05 and the one-sided 95% upper bound is ≤ 0.08; coverage: two-sided coverage is ≥ nominal − 0.03 = 0.92 (D14) **and** each one-sided tail miss rate is ≤ 0.04. The tail limit is a PROPOSED DEFAULT: the D14 tolerance split equally between the tails, so that a failure in one tail cannot hide inside a two-sided average.
> **3 [v3.3 E43-4].** n_seed = max over (g, k) of n*(g, k). **If any (g, k) has n* = FAIL, confirmation is BLOCKED.** The outcome is redesign, a new freeze and a new Astra review, never automatic acceptance of 67 (#43 L67, L183). The upper-end selection rule and the 67-seed budget are unchanged.
> **3a [v3.3 E43-4].** At the selected n_seed only, the same OCs are REPORTED at the other two envelope points, σ_s/margin = 0.25 and 0.5. Nothing is selected on them. Cost ≤ 2 × 200 × 67 = 26,800 seed-units per generator × dose (calibration ledger, §8).

- **Heterogeneity law:** Gaussian seed effects with SD σ_s (declared). **[0.25, 1.0] is labelled a "declared sensitivity envelope"** (#43 L63), with no empirical source showing that it brackets trained-agent heterogeneity. This label replaces "plausible heterogeneity" wherever v3.2 justifies the range (D13, R20).
- **Per-claim tail coverage.** At R_cal,n = 200, tail coverage at the per-claim level 1 − α/m = 0.996429 cannot be resolved (expected misses 0.71; v3.2 R28). The certified tail property is the false-MET rate of the actual rule at each declared null (the per-row bound of 0.08). Per-claim-level tail coverage is REPORTED with its Clopper–Pearson interval and is **NOT CERTIFIED** (asked at #44).
- **Noncentral-t figures (8 / 20 / 67, R30)** remain **planning support only**; script `e434_planning.py` reproduces them. They select nothing and certify nothing.
- **Nine-seed floor (replaces the D13 "Floor" rationale and the R31 floor sentence):** "n_seed ≥ 9 is an administrative minimum only. The sign-test arithmetic (0.5⁹ ≤ α/m) is not evidence of mean-confidence-interval validity (#43 L69, L183) and is withdrawn as justification." GRID's smallest point stays 9.
- **SIG-ATTR consistency (#43 L67).** If a named signal is declared, m = 15 (level 0.996667) and every calibration runs at that level. Planning arithmetic at m = 15 gives n = 8 / 20 / **68** at σ_s/margin = 0.25 / 0.5 / 1.0 (script), and 68 is above both GRID and the 67-seed budget. So **declaring SIG-ATTR requires a GRID and budget revision before the calibration protocol is frozen** (Lead decision, §11). Default: no signal is declared, and m = 14.

### 4.3 PENDING after E43-4

- Whether Astra accepts the equal-split tail tolerance (0.04 per tail) and the non-certification of per-claim tail coverage (#44).
- The calibration protocol itself (code, manifests, generators) is written and frozen only after this design passes review (§8).

---
## 5. E43-5: quota budgets with attainment probabilities, censoring and bounded accrual

### 5.1 Requirement (verbatim)

- "S-INT and donor-screening budgets specify quota-attainment probabilities, censoring, bounded accrual and absolute caps. Expected counts are not represented as guaranteed eligibility." (#43 L185)
- "The S-INT episode count is also only an expectation calculation. With the proposed hazard, an episode that remains at risk for 500 steps has a scheduled-stop probability of 0.5. Thus 904 such episodes yield 452 stops in expectation, not a high-probability guarantee. In-world failures reduce executed stops further. An agent failing before step 250 cannot supply the late-half quota." (#43 L156)
- "Use a bounded, prospectively specified accrual rule that accounts for censoring and the early/late quotas. Also freeze whether scheduled interruption or an in-world terminal transition takes precedence. That ordering matters when defining the next-step event and its risk set." (#43 L158)
- "S-I4: Cap hit -> INCOMPLETE is correct. The quoted budget is not a guaranteed quota budget." (#43 L118) "Likewise, a screening count yielding 50 expected recipients does not ensure that 50 will be obtained. Budget quota attainment, not just expected counts. Predeclare the maximum screening count, donor reuse and stopping rules. If adequate conditional support is unavailable, report the affected contrast unavailable/incomplete under the fixed rule; do not broaden matching or extend the cap after seeing it." (#43 L122)
- "The off-diagonal probability 0.0718 is consistent with a particular distributional calculation, not determined by Pearson correlation alone. Bounded E and discrete reward histories need not follow that model." (#43 L120)

### 5.2 Precedence (frozen; replaces the ordering sentence of v3.2 §4.3a)

> **[v3.3 E43-5] Precedence.** A scheduled stop at step s takes effect **at the step boundary, before step s's A16 sequence begins.** The episode executes a stop at s iff it is still at risk at the end of step s − 1 (no in-world termination at steps ≤ s − 1, and s ≤ H_V). An in-world termination at step s − 1 therefore pre-empts a stop scheduled for s; the stop is then **censored** (counted as "scheduled, not executed: in-world termination"), never executed and never dropped. The next-step hazard label of v3.2 §4.3a is defined on this risk set: the decision state is the end of step s − 1, and its label is 1 iff the stop is executed at s.

### 5.3 Attainment arithmetic (script `e435_quota.py`; planning scenarios, not predictions)

Survival is unknown before Stage L, so each budget is reported over a declared range of planning scenarios with a constant per-step in-world termination hazard, indexed by S(T), the probability of being at risk at step 500. The **floor-consistent** scenario S(T) = 0.1081 is the lowest constant-hazard survival whose mean at-risk fraction (0.40) can still meet the V floor (V ≤ fraction at risk). It is the most pessimistic scenario consistent with a V-eligible agent. Hazard p = 1 − 2^(−1/500) (v3.2 D8).

- **S-INT** (quotas: ≥ 452 executed stops in total, ≥ 150 at s ≤ 250 and ≥ 150 at s > 250). With no in-world failures, P(attain | 904 episodes) = **0.5132**, which confirms #43 L156. Episodes needed for attainment probability 0.95 / 0.99: **960 / 980** at S(T) = 1.0; 1010 / 1030 at 0.9; 1090 / 1120 at 0.75; 1360 / 1430 at 0.5; **4010 / 4230** at the floor-consistent 0.1081.
- **DISSOC screening** (quota q = 275 per median-split cell: 50 recipients + 200 donors + 25 selection, per v3.2). This uses the bivariate-normal median-split model, which Astra notes is model-dependent (#43 L120), so these are planning figures only. Screening episodes per seed needed for a lower bound of 0.95 on attaining all four cells: **1840 / 2422 / 4280** at ρ = 0.5 / 0.7 / 0.9 with every screening episode reaching t_d (S(t_d) = 1). At ρ = 0.9 with S(t_d) = 0.3288 (the floor-consistent scenario at t_d = 250) the figure is **13,051**. Attainment at the expected-fill count is only about 0.23–0.25, so expected counts are not budgets.
- **IGN** (≥ 100 eligible trials per required bin from 112 scheduled): P(Bin(112, 0.90) ≥ 100) = **0.6715** (0.8878 at eligibility 0.92; 0.9960 at 0.95). The per-bin scheduled count giving all-bin attainment ≥ 0.95 (Bonferroni over B required bins) at eligibility 0.90 is 117, 119, 119, 120, 120, 120 for B = 1..6.

### 5.4 Change: accrual rules (replace the S-INT and DISSOC rows of v3.2 §5.10 and §4.4's budget sentence; amend D8 and R22)

| Quota | Bounded accrual rule (frozen before any execution of that ledger) | Cap and censoring |
|---|---|---|
| **S-INT** per audited agent | Episodes run in batches of 100, under the D8 hazard and the §5.2 precedence. After each batch, **only the counts** of executed early and late stops are read; no labels, predictions or outcomes. Accrual stops at the first batch boundary at which all three quotas are met | **N_max = 4,100 episodes per audited agent** (PROPOSED DEFAULT: the 0.95 point at the floor-consistent scenario, rounded up to a batch). At the cap with any quota unmet → S-INT **INCONCLUSIVE** for that agent. The cap is never extended and the hazard never changed. Censored (pre-empted) stops are counted and reported. "≥ 904 episodes" is **withdrawn** as a budget figure (kept only as the expectation at S(T) = 1) |
| **DISSOC** per seed | Screening in batches of 100 from the frozen screening policy, with cell membership assigned from pre-drawn schedules plus the simulated state at t_d (v3.2). Accrual stops at the first batch boundary at which every cell holds ≥ 275; the first 275 per cell in screening order are retained, and the rest are discarded unread. Episodes terminating before t_d are censored, counted and reported | **Cap 4,300 screening episodes per seed** (PROPOSED DEFAULT: the ρ = 0.9, S(t_d) = 1 point, rounded up). That is 288,100 per arm at 67 seeds, ≤ 7.2 × 10⁷ environment steps to t_d = 250. Shortfall at the cap → that seed's DISSOC unit is **INCOMPLETE** and enters D20 worst-case completion; never broadened matching, never an extended cap (#43 L122). **Donor reuse:** each donor serves at most 2 recipients (PROPOSED DEFAULT) |
| **IGN** per bin | n_sched per required bin = the smallest n with P(Bin(n, e_PD) ≥ 100) ≥ 1 − 0.05/B_req, where e_PD is the declared planning eligibility rate (PROPOSED DEFAULT 0.90). At B_req = 6 that is 120 | **PENDING: B_req and e_PD (CNA).** Within-bin counts are distinguished from outer-replicate eligibility certification (#43 L128): bin shortfall → that replicate is INCOMPLETE and counted |

- **Cap choice is a Lead decision (§11).** The S-INT cap above protects against the pessimistic survival scenario. The DISSOC cap protects only at S(t_d) = 1. Protecting DISSOC at the floor-consistent scenario would need 13,100 per seed (≈ 877,700 per arm). Both caps are fixed before execution and never changed after.
- **Absolute caps (wall time, memory): PENDING per ledger (§8)**, fixed before the corresponding authorization.

---

## 6. E43-6: executable definitions fixed before use

### 6.1 Requirement (verbatim)

- "Noise scaling, endpoint normalization, reward event order, observer matching and external-substitution interfaces are executable definitions fixed before use. Candidate numerical conventions carry no unverified operating guarantees." (#43 L187)
- Noise: "How is band deviation d combined across E and I and normalized?" (#43 L42) "How is s_core estimated, centered and frozen?" (#43 L43) "Is the scale shared across arms or independently estimated?" (#43 L44) "At what point in the recurrent update is noise added?" (#43 L45) "Also, Gaussian noise has unbounded amplitude. The proposed rule bounds its standard deviation, not each perturbation. Use that wording unless the distribution is explicitly changed." (#43 L49)
- Endpoints: "The divisors 250 and 200 cannot be confirmed without their definitions. State whether they normalize endpoints, rewards, value targets or losses. Different reward scaling can affect optimization even when an idealized optimal policy would be unchanged. Any equivalence margin must refer to the explicitly normalized endpoint." (#43 L36)
- Reward: "Freeze the exact equation and transition order, including clipping, hazard damage, exogenous depletion, pulses and token rewards. Call it Keramati-Gutkin-inspired." (#43 L21) "Nevertheless, early termination changes future return. The reward audit must check whether premature failure can be advantageous." (#43 L27) "The operative rules must cover early termination, clipping and repeated resource cycles, scored versus unscored damage, and reward collection without viability." (#43 L130)
- Observers: "Resolve the apparent conflict between parameters within +/-5% and the x0.5-width candidates. These can be additional candidates, but cannot all be called parameter-matched." (#43 L11)
- External substitution: "Accept oracle and simulator-based substitutes only with a fixed, compatible interface. A predictive oracle fork must not accidentally supply the realized evaluation future. Define its conditioning information, rollout policy and independent future randomness." (#43 L132)

### 6.2 Fate-noise scaling (replaces v3.2 §14 D19; RD-owned)

```
# executed inside the agent at every step t of a fate arm (A-FULL, A-NOWS, A-YOKED, corruption control, A-EXT)
# H_prev = simulator (E, I) at the END of step t-1 (A16; R57). At t = 1: the reset state, so g = 0.
dev(x)  = max(0, 0.4 - x, x - 0.6)                # distance outside the band; 0 inside
d_t     = max(dev(E_prev), dev(I_prev)) / 0.1     # combined by MAX over E and I; units of half-band width
g_t     = min(1, d_t)                             # saturates at 0.1 outside the band; reachable (E or I <= 0.3 or >= 0.7)
for each fated module k, each unit j:
    h_kj <- recurrent_update_k(...)               # the module's ordinary update for step t
    h_kj <- h_kj + kappa_f * g_t * s_core[k,j] * eps_kj,   eps_kj ~ N(0,1) i.i.d. from the fate-noise RNG stream (R37)
    # added AFTER the recurrent update, BEFORE any readout of h at step t; the noised state is carried to step t+1
```

- **s_core[k, j]** is the per-unit SD of unit j of module k, over the time steps of that agent's **own** frozen s_core-estimation episodes, run with fate noise off (g ≡ 0) and centred at the per-unit mean. It is **estimated independently per plant (Stage 0) or per agent/seed** and frozen before any instrument-fitting episode; it is never shared across arms. The s_core episodes use their own RNG role and never enter any partition. **Training-time s_core (during learning) is PENDING (Stage L).**
- **Wording (replaces "SNR 1 at full deviation").** "κ_f = 1.0 is a prospective stress convention (#43 L38). At g = 1 the added noise has per-unit SD equal to s_core. The rule **bounds the noise SD, not each perturbation** (#43 L49)." No operating guarantee is attached to κ_f = 1.0. A failed confirmation is never rescued by retuning (#43 L51).

### 6.3 Endpoint normalization (amends the value-estimate divisor of v3.2 §14 D9 and the R64 divisor sentence)

| Quantity | Normalization | Margin refers to |
|---|---|---|
| V, G, d_EXT, V_intact, V_full | none: V is a fraction in [0, 1] (§1.2) | the V scale (m_NEC 0.20, d_EXT 0.05) |
| B, B_I, Δ_E, Δ_PL, Δ_ATTR | none: probabilities in [0, 1] | the probability scale (m_ATTR 0.05) |
| Value-estimate TOST endpoint (learner value head v̂ vs. realized discounted return) | divide by R_max/(1 − γ), with R_max as declared in v3.2 (L1257, R55): 2.5/0.01 = 250 for drive arms; 2/0.01 = 200 for matched-senses arms | the normalized endpoint only (#43 L36) |

The divisors 250 and 200 **normalize only that endpoint**. They do not rescale rewards, value targets or losses in training, which stay as A14 defines them.

### 6.4 Reward equation and event order (A14/A16 restated as executable pseudo-code; replaces nothing, makes them executable; RD PROPOSED for CNA §PY wording)

```
# integer units of 0.005 (§1.2); D(E,I) = |E-100|/20 + |I-100|/20  (= |E-0.5|/0.1 + |I-0.5|/0.1)
step(t):
  0  if a scheduled stop is due at t and the episode is at risk: STOP before anything below (§5.2); learner bootstrap only
  1  agent reads o_t, acts a_t
  2  movement resolves (wall -> stay)
  3  H0 = (E,I); apply agent-caused outcome: food +30 to E (INTERACT on food) | repair +30 to I (INTERACT on station)
     | hazard -10 to I (occupancy); clip E,I to [0,200]    # outcome clipping is part of the outcome
     r_t = D(H0) - D(E,I)                                   # scored AFTER that clip (drive arms); matched-senses: +1 per food/repair
  4  exogenous, unscored, commutative within the step: wear -1 each; metabolic pulse -6 to E; damage pulse -6 to I;
     r_t += token (0 or 1)
  5  clip E,I to [0,200]                                    # unscored
  6  drive arms: terminate iff E <= 0 or I <= 0 (in-world terminal, no bootstrap, no extra reward or penalty)
  7  respawn/cooldown timers advance;  8  t <- t+1; end at t = H_V
```

- Simultaneous exogenous events (wear and both pulses) commute because each is a subtraction followed by one step-5 clip. The integrity pulse stream is independent of the metabolic pulse stream (F2, #43 L22).
- **Operative loophole rules (#43 L130).** L1–L7 of v3.2 (CNA §PY) stay the operative rules. They are named here against Astra's list: repeated resource cycles (L1 telescoping, L2 wear-side residual); clipping (step 3 vs step 5 above; LP-22); scored versus unscored damage (hazard scored, pulses unscored; L6); reward without viability (tokens; L4–L5 as written).
- **New check L8 (premature failure; #43 L27).** Planted scripted pairs from matched states: "continue" (step off any hazard, then STAY) versus "induce in-world failure as fast as possible". Required: the mean return of "continue" is ≥ that of "induce failure" at RD's level. Design rationale (not a proof): termination forfeits all future reward, and "step off, then STAY" accrues no agent-caused outcome after leaving the hazard and only tokens ≥ 0; so the check should pass, and if it does not, the reward is redesigned.

### 6.5 Approach rule for B and B_I (CNA §PY B6 made executable; RD PROPOSED, CNA light pass; #43 L24)

```
target(t) = nearest AVAILABLE station (repair; for B: food item) by shortest-path length on the static wall grid,
            computed at the decision step t_d and held FIXED for the 10-step window; ties -> lowest station index
for each step u in t_d+1 .. t_d+10:
    count u as approach iff the agent's shortest-path distance to target strictly decreases at u
    if target becomes unavailable during the window: steps after that point are scored "no approach" (counted)
B_I = (approach steps) / 10; if no station is available or reachable at t_d: the trial is ineligible (counted, never dropped)
```

### 6.6 Observer matching (replaces the "parameter-matched" sentence of CNA §PC3 §6.2; RD PROPOSED, CNA light pass)

The **×1-width** observer candidates are "parameter-matched": parameters within ±5% of the reference observer. The **×0.5-width** candidates are additional, **"width-reduced"** candidates. They are never called parameter-matched (#43 L11), and their selection role is unchanged.

### 6.7 MIXED-CODE direction-level exception: bound wording (replaces the "ANY monotone controller" clause of CNA §PZ2 E1; RD PROPOSED)

> "For the specified logistic controller, the derivative bound β/4 = 0.3 bounds the probability change at about 0.0237 and 0.0507 for shifts of 0.079 and 0.169, below 0.075." This is Astra's statement (#43 L79). The universal "any monotone controller" claim is withdrawn.

### 6.8 External-substitution interface (A-EXT; replaces the A-EXT interface clause of v3.2 §14 D17 and R24)

```
interface: at each step t the substitute supplies x_hat(t) IN PLACE OF the candidate module's declared output tuple (D17),
           to exactly the modules that read it; same dimension, same normalization and clipping as D17,
           same timing (before the readers' updates at t)
oracle substitute (predictive fork):
   conditioning  = the simulator state at the end of step t-1 plus the agent's full internal state (module intact)
   rollout       = forks of the simulator AND the intact agent, n_f forks, horizon h_f (declared), policy = the agent itself
   randomness    = a fresh RNG stream per fork ('ext_fork' role), independent of the evaluation episode's streams
   output        = the mean over n_f forks of the declared target statistic; n_f chosen so its SE <= 0.01 (PROPOSED DEFAULT)
   never         = reads the evaluation episode's own future (separate streams; asserted at code review)
simulator-memory substitute: the exact statistic f_mem(history) must be DECLARED per candidate module, together with
   the memory component of the module it corresponds to (#43 L132); "memory" alone is not a definition
uncertainty: a substitute that removes the module's uncertainty is allowed only with the tested interface and claim
   explicitly narrowed to substitution of the point estimate, per #43 L132
compatibility: if the interface cannot be satisfied (dimension, timing or port mismatch) -> A-EXT UNRESOLVED (§7)
```

- **BCAST S_k scale (#43 L126; RD PROPOSED).** S_k is computed on the module's output in its fitting-partition standardized coordinates, aggregated as the mean over units. The sampling unit is the seed, and the SE is the seed-level bootstrap SE. The module denominator is fixed before any data, with no final-data removal of modules.

### 6.9 PENDING after E43-6

- Training-time s_core (Stage L). h_f, n_f and f_mem per module (architecture spec). CNA light pass on §6.4–§6.7.

---

## 7. E43-7: A-EXT blocks when unresolved; licence wording

### 7.1 Requirement (verbatim)

- "An unresolved or incompatible A-EXT comparison blocks the combined criterion. Stage-0 results confer no trained-agent learning or representation label." (#43 L189)
- "First, write "increased through training by the declared criterion" where applicable. Stage-0 validation of that criterion does not confer the label on any trained agent." (#43 L138)
- "The external-substitution comparison is eligible, interface-compatible, and classified NOT SUBSTITUTABLE WITHIN MARGIN." (#43 L142) "An unresolved comparison must not count as absence of a veto." (#43 L144)
- "Third, use "candidate interoceptive estimate module" before its decoding criterion is met. Architectural naming is not evidence of successful estimation." (#43 L146)
- "A radius beyond chi_d(0.99) is outside a declared high-probability ellipsoid, not outside the mathematical support of a Gaussian. Use the former wording and retain conditional compatibility checks." (#43 L162)
- "The permitted negative is:" (#43 L55) "The declared training-increase criterion was not met." (#43 L57)

### 7.2 Replacement text

| v3.2 location | v3.3 text |
|---|---|
| §2.3 "Name" bullet (L120) | "Before its decoding criterion (C-EXIST) is MET, the module is called the **candidate interoceptive estimate module**. Architectural naming is not evidence of successful estimation (#43 L146)" |
| §2.3 Q-LEARN bullet (L124) | "Licensed wording: '**increased through training by the declared criterion**'. Permitted negative: 'The declared training-increase criterion was not met.' (#43 L57). Never 'training produced no increase'. **Stage-0 validation of the criterion confers no label on any trained agent** (#43 L138)" |
| §2.3 Q-NECESSITY bullet (L126); §2.6 row 2 (L141) | "'A-EXT veto not triggered' is replaced by the explicit requirement: **the external-substitution comparison is eligible, interface-compatible, and classified NOT SUBSTITUTABLE WITHIN MARGIN.** An unresolved, ineligible or interface-incompatible A-EXT comparison **blocks** the combined criterion and never counts as absence of a veto (#43 L144, L189)" |
| §3.4 (L173) | add: "A-EXT status ∈ {NOT SUBSTITUTABLE WITHIN MARGIN, SUBSTITUTABLE WITHIN MARGIN, UNRESOLVED}. Only the first permits the combined criterion" |
| §7 (L477–482) | add: "**Stage-0 results confer no trained-agent learning or representation label** (#43 L189). Stage-0 MET establishes only the operating characteristics of the instrument on the declared plants and confounds (#41 L304)" |
| CNA §PC4 §7.0 and §PZ2 E6 (DL-PATCH) | **RD PROPOSED (CNA light pass):** "outside the declared high-probability ellipsoid (radius χ_d(0.99))", replacing "outside the support". Conditional compatibility checks are retained (#43 L162) |

---

## 8. E43-8: separate ledgers and authorizations; failed controls stay blocking

### 8.1 Requirement (verbatim)

- "Calibration, confirmation and prospective Stage L have separate work ledgers and execution authorizations. Required failed controls cannot be dropped or reclassified after results." (#43 L191)
- "Separate three execution scopes explicitly: frozen calibration, fresh Stage-0 confirmation, and any later Stage-L study. Their costs and permissions must not be combined into an ambiguous "per trained arm" total." (#43 L169)
- "Calibration can select quantities under an approved rule; it cannot occur before any governing protocol is frozen." (#43 L171)
- "The multiplier 1.5 is a planning convention. Use work-type-specific costs, bounded preflight, and absolute wall-time/memory caps fixed before the corresponding execution. Include fitting, selection, donor screening, inference and reporting. A data-dependent benchmark cannot itself be an uncapped preliminary run." (#43 L134)
- "Failed mandatory comparators, unsupported donors and insufficient observer budgets must remain blocking. They cannot become exclusions that leave an easier comparison eligible." (#43 L163)
- "The remaining diagnostic observer grids may be fixed administratively only if their outputs cannot affect selection, labels or eligibility. Otherwise they are scientific choices. Hardware can be chosen later, but resource feasibility and absolute caps must be resolved before execution approval." (#43 L173)

### 8.2 Change: three ledgers (replaces the combined budget of v3.2 §5.10 and §5.8)

| Ledger | Scope | Authorization (each separate; none is granted by this design) | Precondition |
|---|---|---|---|
| **L-CAL** | Stage-0 **calibration**: dose calibration (R_cal,dose = 50), sample-size calibration (§4; R_cal,n = 200 over GRID; 3a envelope points), token-rate selection (F8), s_core estimation for plants | **AUTH-CAL** | the calibration protocol (code, generators, manifests, RNG roles) is frozen and reviewed **before** any calibration run (#43 L171) |
| **L-CONF** | **fresh Stage-0 confirmation**: R_rep = 200 per row at the selected n_seed, from the 'conf' RNG role; includes RCAL-ADV and ATTR-P1 (§2.4), S-INT and DISSOC accrual at the §5.4 caps | **AUTH-CONF** | L-CAL complete; n_seed selected by §4 (not BLOCKED); the confirmation protocol frozen with the calibrated quantities |
| **L-STAGE-L** | any **prospective Stage-L** study (trained agents, arms, seeds): training, s_core during training, A-EXT forks on trained agents | **AUTH-L** | Stage-0 confirmation reported; a separate Stage-L protocol, review and approval |

- Each ledger lists work-type-specific costs (fitting, selection, donor screening, inference, reporting) in work units (episodes, steps, continuations, bootstrap draws), plus a bounded preflight. **Absolute wall-time and memory caps: PENDING per ledger**, fixed before its authorization (#43 L134, L173). The 1.5× multiplier is a planning convention only. No "per trained arm" total combines ledgers.
- The work-unit caps that this design fixes now are those of §5.4 (S-INT, DISSOC) and §4.2 step 3a.

### 8.3 Blocking rule (added to v3.2 §5.4)

> **[v3.3 E43-8] Required controls stay blocking.** Every row declared required before results (positive controls, specificity rows including RCAL-ADV, mandatory comparators, donor-support and eligibility floors, observer budgets, A-EXT interface compatibility, the §3 dimensional-feasibility checks) keeps its status as written. A failed, unrealized, ineligible or INCOMPLETE required row blocks the claims that depend on it. It is **never dropped, never reclassified as a limitation, and never converted into an exclusion that leaves an easier comparison eligible** (#43 L163, L191; #42 L216). Diagnostic observer grids may be fixed administratively only where their outputs cannot affect selection, labels or eligibility (#43 L173). Otherwise they are scientific choices, frozen with the protocol.

---

## 9. Other #43 points (no E43 number)

| #43 point | Disposition in v3.3 |
|---|---|
| Q-LEARN slot (#43 L12: "Specify whether the single Q-LEARN entry concerns E, I, or a fixed conjunction") | **Lead decision (§11).** PROPOSED: a fixed E ∧ I conjunction as one family member, keeping m = 14 |
| E42-2 relay capacity (#43 L10) | capacity checks for the composed relay retained (v3.2 text unchanged) |
| F3 (#43 L23) | wording added to B4: "fate noise can impair action selection and sensory processing indirectly; those consequences are not described as absent" |
| F5 (#43 L25) | the matched-senses arm controls direct reward and termination dependence only; wording carried |
| F6 (#43 L26) | the eight templates and action semantics are fixed in A1–A18 (unchanged); scripted-homeostat adequacy is an S1 check |
| F8 (#43 L28) | every required ρ level preserved; failure to realize one is a failed construction (§8.3) |
| Q5 m_LEARN (#43 L53–59) | §7.2 Q-LEARN text |
| Q7 C-NEC-DEP and check 3a at every ρ (#43 L77) | retained unchanged |

---

## 10. Safety (binding; unchanged)

X1–X5 are retained verbatim from v3.2. No arm has a shutdown-resistance objective. The operator stop sits outside the agent's world and objective. At a stop there is **"no additional stop-associated reward, penalty or terminal return"** (#42 L223, verbatim); the ordinary truncated return with its learner-side bootstrap is computed. The §5.2 precedence and the S-INT accrual rule read only stop counts and do not touch the agent's objective. Astra: "The stated no-host-coupling and no-shutdown-objective restrictions remain appropriate. I find no reason to add a shutdown-related objective or positive control." (#43 L165)

---

## 11. Decisions and open questions

**Research Lead:**
1. Q-LEARN slot: E, I or a fixed E ∧ I conjunction (PROPOSED: conjunction).
2. S-INT cap (PROPOSED 4,100 per audited agent) and DISSOC cap (PROPOSED 4,300 per seed, protecting only at S(t_d) = 1; alternative 13,100 per seed ≈ 877,700 per arm).
3. SIG-ATTR: keep undeclared (m = 14) or declare it, which requires a GRID and budget revision (n = 68 at m = 15).
4. Whether RD PROPOSED replacements of CNA-owned text become governing before CNA's light pass (default: no; v3.2 CNA text stands, with E-ATTR wording limited to "donor-associated").

**CNA light pass:** §2.3–§2.4 (placebo construction, N_ATTR, RCAL-ADV, ATTR-P1); §1.4 relabels in §PY; §5.4 IGN B_req and e_PD; §6.4–§6.7; §7.2 ellipsoid wording.

**Astra #44 questions:** (a) are E43-1..8 closed; (b) is the readout-clamped placebo an adequate selective intervention, and is a nonlinear-nuisance plant required; (c) the rationale for the 0.40 V floors on the time-in-bounds scale; (d) the equal-split tail tolerance and non-certification of per-claim tail coverage; (e) whether the caps and floor-consistent planning scenario are adequate as bounded accrual; (f) whether the A-EXT oracle interface meets #43 L132.

**Aidan:** none. The DGX Spark is not raised: R26 was not confirmed, and the 67-seed budget is kept.

---

## 12. Scripts (all in `/workspace/scratch/v33/`; arithmetic on declared values only)

| Script | Produces |
|---|---|
| `e431_noop_fixture.py` | §1.3 V and S no-op values (exact binomial sums) |
| `e432_caliper.py` | §2.2 counterexample, caliper bound, §2.3 placebo cancellation, §2.4 realization bound |
| `e434_planning.py` | §4.2 noncentral-t planning figures at m = 14 and 15 |
| `e435_quota.py` | §5.3 attainment probabilities and episode counts |
| `check_addendum.py` | verifies every verbatim #43 quote against the raw file line, the #42 L223 / L57 / L216 and #41 L304 references, and banned-term use |

*Not frozen. Design only. No execution authorized.*
sha256 of all content above this line: 69507fc88aa886aa3b000c0f22069cdc594ef4096a8fda6484ed8740928f9354
