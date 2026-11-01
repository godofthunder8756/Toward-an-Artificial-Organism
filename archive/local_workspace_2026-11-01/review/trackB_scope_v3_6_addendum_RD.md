# Track B scope v3.6 — ADDENDUM (RD): Astra #46 required items E46-1..E46-4

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. Astra #46, verbatim: "VERDICT: READY WITH NUMBERED EDITS for freeze preparation, subject to E46-1 through E46-4; no freeze or execution is authorized." (#46 L136)

- **What this file is.** A new, additive, narrow addendum to merged v3.5. It edits nothing. For each of Astra's #46 items E46-1..E46-4 it gives (a) Astra's item text verbatim with its line number, (b) the change, written as replacement or added text for named sections of merged v3.5 (mostly §PZ7, the v3.5 addendum carried verbatim inside merged v3.5), and (c) what stays PENDING. It keeps the pre-freeze prerequisites P1–P6 OPEN (§5), lists the Lead defaults (§7) and gives a change list (§8). Merged v3.6 (`trackB_instrument_validation_scope_v3_6_merged_RD.md`) appends this file as §PZ8.
- **Base:** merged v3.5, `/workspace/review/trackB_instrument_validation_scope_v3_5_merged_RD.md`, sha256 `80ed7a1b5429a29d19aeaf866fa27a142726ec585b1bb20f27ba7f03ca6ad28d`; v3.5 addendum `/workspace/review/trackB_scope_v3_5_addendum_RD.md`, sha256 `3b2680e9b6e58993bd976bb99d4dc367f7357ec1e4327039e8d0548e7d0d02b4`. "PZ7 §n" means section n of the v3.5 addendum as carried in merged v3.5; "PZ6 §n" the v3.4 addendum; "PZ5 §n" the v3.3 addendum.
- **Governing:** Astra #46 raw reply, `/workspace/astra_consult46_response.txt`, sha256 `e902a1840a8435e4425d380e3f51d58a0f6afd50b2835d8b6a2e9896f9b38e53`; "#46 Lnn" means line nn of it. #45, #44, #43, #42 and #41 govern where #46 is silent. **Transcription note:** the saved raw text lost its typographic quotation marks (each appears as the replacement character U+FFFD in the file); quotations below reproduce the surrounding text exactly and omit those characters.
- **Bounded.** Astra, verbatim: "No additional instrument, arm or row is required." (#46 L3) and "No further expansion is needed." (#46 L122) This addendum adds **no** instrument, arm, plant, row, question or family member. It replaces an approximate inactivity screen with a derived bound inside the existing tier-2 null rows, defines events and numerical edge cases, splits the existing L8 rollout budget into two independent allocations, and narrows the BCAST-W alias test. m = 14 is unchanged; R26 is unchanged (67 seeds); X1–X5 and the claim ceiling are unchanged.
- **Ownership.** RD (Delegate role) wrote this file. Text that replaces or adds to CNA-owned sections (plants, DISSOC, donor laws, environment, §PY) is marked **RD PROPOSED — CNA light pass required** and governs only after CNA's light pass. Where a choice belongs to the Research Lead, the text gives a **LEAD DEFAULT** (clearly marked) that stands until the Lead rules otherwise.
- **Numbers.** Each new number is (a) arithmetic on declared constants (stated inline; checked by `/workspace/scratch/v36/check_addendum36.py`), (b) a **LEAD DEFAULT** with a one-line rationale, or (c) **PENDING**. None is measured. No study component, plant, agent or environment was run.
- **Written:** 2026-10-24, about 10:25–11:30 AM ET, by RD.

---

## 0. Governing text: Astra #46

- **Verdict:** "Q0. READY WITH NUMBERED EDITS for freeze preparation." (#46 L1) "This assessment concerns the supplied clauses, not independent verification of the merged file. It is not freeze or execution approval." (#46 L5)
- **Q1 status of E45 items (#46 L10–L14):** CLOSED: E45-2, E45-3. PARTLY: E45-1 (tier-2 inactivity screen), E45-4 (L8 selection and scoring on the same rollouts), E45-5 (alias test).
- **Not reopened (#46 L126):** "They do not reopen the viability estimand, common sample-size principle, quota caps, approach endpoint, claim ceiling or safety restrictions."

| Item | Section here | v3.5 sections replaced or amended |
|---|---|---|
| E46-1 FID-DET event and protective-rejection wording; tier-2 null inactivity by exact invariance or plant-specific bound | §1 | PZ7 §1.2 (D); PZ7 §1.3 (inactivity condition); PZ7 §1.4 table cells for the tier-2 nulls; PZ7 §9 item 2 |
| E46-2 zero-denominator and non-finite rules; s_(r+1); rank-zero wording; zero-invocation A-EXT units | §2 | PZ7 §2.2 (s_(r+1) clause); PZ7 §2.3 (λ_n; r_N = 0 flag wording); PZ6 §1.3 (f_n); PZ7 §1.2 R2; PZ7 §3.2 items 3–5 |
| E46-3 L8 qualification and scoring on independent allocations | §3 | PZ7 §4.3 (I2 data source); PZ7 §4.4 (data source of M and S; conclusion scope); PZ6 §5.3 "Estimator" |
| E46-4 alias vs non-routing node vs unavailable intervention; R_core/R_T3 stages | §4 | PZ7 §5.2 (operational test); PZ7 §5.4 BCAST-W and Tier-3 rows; output table (new §4.4 here) |
| #46 Q7 | §5 | P1–P6 kept OPEN |

---

## 1. E46-1: FID-DET as protective rejection; tier-2 null inactivity by exact invariance or a plant-specific behavioural bound

### 1.1 Requirement (verbatim)

- E46-1. "Define FID-DET using the finite, eligible rbar fidelity upper bound and describe it as protective rejection unless stronger violation evidence is established. For each tier-2 null, justify the inactivity screen by exact invariance or a plant-specific bound on the actual scored contrast." (#46 L128)
- Event: "A finite, eligible rbar fidelity assessment has its one-sided upper confidence bound above tol_fid, so the rbar fidelity certificate is withheld." (#46 L20) "A failure on another nuisance, an unavailable bound or a non-finite computation is not an rbar detection." (#46 L22)
- "The former is sufficient for the protective role selected here." (#46 L29) "Keep all prespecified replicates in its denominator; unavailable assessments must not become successful detections." (#46 L31)
- "A small standardized change in a controller argument is not necessarily causal inactivity. Its behavioral consequence depends on the argument's scale, the controller's sensitivity and the subsequent dynamics." (#46 L33)
- "A one-step bound cannot automatically be applied to a ten-step continuation with recurrent and environmental effects." (#46 L40) "Otherwise it cannot establish the null merely by being labelled" (#46 L42, partial).

### 1.2 Change: the FID-DET event (replaces the PZ7 §1.2 (D) sentences "The replicate is a detection iff … known to be violated." and "A gate failure on some other nuisance only is not a detection …"; RD PROPOSED — CNA light pass required)

> **[v3.6 E46-1] Gate statistic.** For nuisance n, the **gate statistic** is U_n = the seed-level one-sided 95% upper confidence bound of the seed means of f_n (PZ6 §1.3; same bootstrap as PZ5 §5.4). The clamp-fidelity certificate for n is **granted** iff U_n is finite, the assessment is eligible (below) and U_n ≤ tol_fid = 0.05; otherwise it is **withheld**.
> **Eligible r̄ fidelity assessment (per replicate).** All of: (i) every cell entering it is usable under PZ7 §2.3 and the v3.6 numerical rules (§2 here); (ii) every hybrid entering it has a defined f_r̄ under §2.2 here (a zero-scale r̄ assessment is not eligible, §2.2 (c)); (iii) the prespecified seed set contributes per the declared seed-level unit; (iv) every quantity in it is finite (a non-finite value is a construction failure, §2.4 here).
> **FID-DET event (per NLN replicate).** "A finite, eligible r̄ fidelity assessment has U_r̄ > tol_fid, so the r̄ fidelity certificate is withheld." It is called a **protective rejection**. **Not** protective rejections (each counted as a non-event and reported by reason): a withheld certificate on another nuisance only; an unavailable U_r̄ (ineligible or not computable); a non-finite computation; a constant-readout-flagged r̄ assessment.
> **Protective-rejection rate D_PR.** D_PR = (number of replicates with the event) / R, with **R = all prespecified replicates** (R_cal,n = 200 in calibration at the selected n_seed; R_rep = 200 in confirmation). No replicate leaves the denominator. Required operating characteristic (unchanged): one-sided 95% Clopper–Pearson lower bound of D_PR ≥ 0.90 (#46 L31).
> **Interpretation (wording rule).** A protective rejection means that r̄ fidelity was **not certified**; it does **not** establish that the r̄ change exceeds tol_fid (#46 L26–L27). Every report uses "protective-rejection rate", never "violation detected". **REPORTED only, not a gate:** the rate at which the matching one-sided 95% **lower** bound exceeds tol_fid (violation evidence; #46 L29 notes it is not required).
> (R) and (F) of PZ7 §1.2 are unchanged. The NLN status rule is unchanged with (D) read as D_PR.

The name "FID-DET" is kept as the row label for continuity; its event is the protective rejection defined above.

### 1.3 Change: tier-2 null inactivity (replaces the PZ7 §1.3 inactivity condition in full; RD PROPOSED — CNA light pass required)

The v3.5 screen (mean |Δg| / SD(g) ≤ 0.05 on the controller argument) is **withdrawn as a null-establishing condition**. A tier-2 null row (RCAL-ADV-E/-I, MIXED-CODE-E/-I, REW-CORR-E/-I) is a null only if **Route I or Route B** below holds for it; otherwise the row is **CONFOUND NOT REALIZED** (blocks tiers 2 and 3, as in v3.3 §8.3). The argument change is still REPORTED.

> **[v3.6 E46-1] Setting.** In each of these plants the declared controller reads the block only through one known scalar argument g = z_R / SD(z_R) (MIXED-CODE and RCAL-ADV: z_R = r̄, PC1 §5; REW-CORR: z = r̄ + ε, PC §8.1 and erratum E5), where SD(z_R) is the plant's declared fitting-partition scale. The scored statistic is the 10-step approach fraction B (or B_I) of PZ6 §5.4, and Δ_ATTR,i = [B(L) − B(L-PL)] − [B(H) − B(H-PL)] per recipient. A swap continuation (donor state x_d) and its placebo continuation (x_PL(d)) start from the same frozen world state and differ only in the block state, by δ_d = x_PL(d) − x_d.
> **Design-time graph conditions (KR-ID, analytic; part of both routes).** (G1) The world, the fate-noise and token streams, and the scoring of B read the agent's block only through the agent's actions. (G2) The controller's action law at each step depends on the block only through g. (G3) The update of z_R (hence g) given an identical action/reward history is **non-expansive** in the initial perturbation: |Δg_j| ≤ κ_j |Δg_1| with κ_j ≤ 1 for j = 1..10 (for a leaky integrator r̄ ← (1 − 1/τ_r) r̄ + r/τ_r, κ_j = (1 − 1/τ_r)^(j−1)). (G4) The other coordinates changed by δ_d (z_E and any further block coordinates) feed neither the controller nor z_R's update. If any of G1–G4 fails for a plant, neither route is available and the row is CONFOUND NOT REALIZED.
> **Route I — exact invariance.** Holds iff G1–G4 hold **and** the realized displacement leaves g exactly unchanged for every hybrid of the row, i.e. u_gᵀ δ_d = 0 for the known read direction u_g, established **analytically** for the actual fitted clamp (not by a numerical tolerance). Then the placebo and swap continuations have the same path law, so E[Δ_ATTR,i] = 0 exactly. With ridge-fitted probes the fitted r̄ direction is not in general exactly u_g, so Route I is expected to be unavailable for fitted cells; it is listed for plants where exactness is a construction property.
> **Route B — plant-specific bound on the actual scored contrast.** For hybrid d of recipient i let a_d,i = |g(x_PL(d)) − g(x_d)| (the actual fitted clamp's argument change at t_d; the zero-scale rules of §2.2 apply). Let c_π = sup over g of the per-step total-variation change of the declared action law per unit change of g (for the MIXED-CODE / RCAL-ADV approach law σ(a − β g) with β = 1.2: c_π = β/4 = 0.3, since σ' ≤ 1/4). **Derivation (path-law coupling, not a one-step bound).** By G1–G4, given an identical history up to step j the two continuations' step-j action laws differ in total variation by at most c_π κ_j a; the world and scoring then evolve identically. So the probability that the two path laws have diverged by step k is at most c_π a Σ_{j≤k} κ_j, and, B being the mean of ten indicators bounded in [0, 1],
> |E B(PL) − E B(d)| ≤ C_H · a,  C_H = (c_π / H) Σ_{k=1}^{H} Σ_{j=1}^{k} κ_j, H = 10.
> With κ_j ≤ 1 (the conservative value, valid under G3 for any non-expansive update): **C_H ≤ c_π (H + 1)/2 = 0.3 × 5.5 = 1.65.** (With the leak τ_r = 50, κ_j = 0.98^(j−1), C_H = 1.55485; REPORTED only; the gate uses 1.65.) Hence |E Δ_ATTR,i| ≤ C_H (a_L,i + a_H,i).
> **Route B gate.** Let A_i = a_L,i + a_H,i, averaged per seed; U_A = the seed-level one-sided 95% upper confidence bound (same bootstrap). Route B holds iff G1–G4 hold and **C_H · U_A < 0.05** (m_ATTR), i.e. U_A < 0.05/1.65 = 0.030303 for the β = 1.2 plants. Then the true scored Δ_ATTR of the row is bounded below the 0.05 criterion with the stated confidence, and the row is a tier-2 null. U_A non-finite or unavailable → Route B fails.
> **Per row.** RCAL-ADV-E/-I and MIXED-CODE-E/-I: β = 1.2, c_π = 0.3, C_H = 1.65 (G1–G4 from the pure-plant graph: controller reads z_R only; z_E read weight 0; PC1 §5 and erratum E1). REW-CORR-E/-I: c_π = (maximum slope of the declared REW-CORR action law in g); if that law is the same logistic with β = 1.2, C_H = 1.65; **PENDING CNA confirmation of the REW-CORR action law and of G3 for z = r̄ + ε** (whether ε is redrawn per step or persists). Until confirmed, REW-CORR-E/-I cannot use Route B and are CONFOUND NOT REALIZED (blocking), never assumed null. The I-rows use B_I and the same constants.
> **REPORTED per row:** the a_d,i distribution, U_A, C_H, the route used, and, for comparison, the withdrawn v3.5 screen value (mean a_d,i).

### 1.4 Change: table cells (amends PZ7 §1.4)

- RCAL-ADV, MIXED-CODE and REW-CORR rows: the Role cell reads "tier-2 specificity null (only if Route I or Route B of PZ8 §1.3 holds)"; everything else unchanged.
- NLN rows, tier-3 cell: "FID-DET: protective-rejection rate D_PR with CP lower ≥ 0.90 over all prespecified replicates, and complete tier-3 false-licence ≤ the false-MET criterion".

### 1.5 PENDING after E46-1

- CNA light pass on §1.2–§1.4 (P1), including the REW-CORR action law and G3 (P1 sub-item).
- The KR-ID analytic verification of G1–G4 per plant (design-time; no run).

---

## 2. E46-2: zero-denominator and non-finite rules; s_(r+1); rank-zero wording; zero-invocation A-EXT units

### 2.1 Requirement (verbatim)

- E46-2. "Specify zero-denominator and non-finite handling for preservation and inactivity normalizations. Constant unchanged readouts may record zero change; nonzero change against a zero scale cannot pass. Required A-EXT components with no invocations cannot satisfy the precision gate vacuously." (#46 L130)
- "Define s_(r+1) = 0 when no singular direction remains." (#46 L50)
- "Flag it as having no nonzero fitted linear nuisance directions; do not describe it as substantive nuisance removal." (#46 L54)
- "Use comparably explicit rules wherever the controller-argument or fidelity normalizations can be zero. No silent numerical epsilon should create eligibility." (#46 L62)
- "A required prediction component with zero invocations cannot pass a percentage-precision requirement vacuously." (#46 L70) "A non-finite construction failure stops the affected computation and invokes the declared incomplete/unresolved handling. It is not an omitted invocation followed by continued scoring as though nothing happened." (#46 L71)

### 2.2 Change: one rule for every normalized change (new; applies to every quantity listed; RD-owned except where marked)

> **[v3.6 E46-2] Ratio rule.** For every normalized quantity q = num / scale below, evaluated exactly (comparisons with zero use exact zero; **no numerical epsilon is added to any numerator or denominator**; the only numerical tolerances in the scope remain the declared τ_rank = 10⁻⁶ and the KR-ID 10⁻⁹, which are frozen, not silent):
> - **scale > 0, both finite:** q = num / scale.
> - **num = 0 and scale = 0 (0/0):** record **zero change** with a **constant-readout flag** (REPORTED).
> - **num ≠ 0 and scale = 0:** the check **fails**; the cell, hybrid or assessment is **unusable** (counted against the relevant eligibility floor, never dropped).
> - **any non-finite input or result:** **construction failure** (§2.4), never zero change.
>
> | Quantity | num / scale | Consequence of the 0/0 flag | Consequence of nonzero/0 |
> |---|---|---|---|
> | (a) linear preservation λ_n (PZ7 §2.3) | \|w_nᵀ δ\| / SD(ŷ_n) | zero change; tol_lin holds for n; flag REPORTED | tol_lin fails → cell unusable |
> | (b) NLN true nuisance change (PZ7 §1.2 R2) | \|φ(x_PL) − φ(x_d)\| / SD(φ) | zero change (R2 then cannot reach 0.10 from that hybrid) | hybrid unusable; R2/R4 accounting counts it ineligible |
> | (c) fidelity f_n (PZ6 §1.3) | \|m̂_n(x_PL) − m̂_n(x_d)\| / SD_n | zero change recorded, **but a constant-readout-flagged nuisance cannot support a granted fidelity certificate** (certificate withheld for a claim; for FID-DET the r̄ assessment is not eligible, so not a protective rejection) | assessment unusable: certificate withheld for a claim; not eligible for FID-DET |
> | (d) controller argument a_d,i (§1.3) | \|Δz_R\| / SD(z_R) | — (SD(z_R) is a declared plant constant; SD(z_R) = 0 is a plant construction failure) | plant construction failure → the row is CONFOUND NOT REALIZED |
> | (e) ρ_E (PZ7 §2.3) | ‖(I − P_N) w_E‖ / ‖w_E‖ | ‖w_E‖ = 0 is already unusable (nondegeneracy); no 0/0 case is used | — (‖w_E‖ = 0 ⇒ unusable) |
> | (f) v̂_E = v_E / ‖v_E‖ | — | formed only for usable cells (ρ_E ≥ 0.10 ⇒ ‖v_E‖ > 0) | — |
> | (g) A-EXT precision fraction (PZ7 §3.2) | (steps with SE ≤ 0.01) / D | D = 0 for a **required** unit: the unit **fails** (UNRESOLVED), never vacuous | — |
> | (h) A-EXT D17 normalization of a fork statistic | statistic / declared D17 scale | a zero declared D17 scale is a construction failure | construction failure |
>
> **Rationale for (c) (LEAD DEFAULT).** A constant MLP readout does not track the nuisance, so granting a certificate on it would be vacuous; withholding it is the conservative direction for claims, and excluding it from protective rejections keeps FID-DET from being passed by a degenerate probe. This is the fidelity analogue of the zero-invocation rule in (g).

### 2.3 Change: s_(r+1) and rank-zero wording (amends PZ7 §2.2 and §2.3)

> **[v3.6 E46-2]** In PZ7 §2.2 the clause "s_{r+1} := 0 if r_N = |N|" is replaced by: **s_(r+1) := 0 whenever no singular direction remains, i.e. when r_N = min(d_ws, |N|)** (#46 L50); the bound |w_nᵀ δ| ≤ s_(r+1) ‖δ‖ then reads |w_nᵀ δ| ≤ 0. In PZ7 §2.3 the flag wording "(the declared adjustment did nothing)" is replaced by: **"no nonzero fitted linear nuisance directions"** (#46 L54). Such a cell (W_N = 0, w_E ≠ 0, ρ_E = 1) is usable for the coordinate estimand, flagged, and never described as substantive nuisance removal; its SD(ŷ_n) may be 0, in which case §2.2 (a) applies (each w_n = 0 gives num = 0, so 0/0 → zero change with the constant-readout flag).

### 2.4 Change: non-finite values stop the computation (replaces PZ7 §3.2 item 5 (iii); generalizes PZ7 §3.2 item 5 (ii))

> **[v3.6 E46-2] Construction failure.** A NaN or ±∞ in any input, intermediate or output of a declared computation (probe fit, SVD, hybrid construction, f_n, λ_n, φ, a_d,i, Δ_ATTR, a bootstrap bound, a fork statistic, a fork mean, a memory output) is a **construction failure**. It **stops the affected computation** at that point; the failure, its step index and its inputs are recorded in the ledger; nothing is imputed, re-run with different randomness, re-forked or skipped.
> - Stage-0 rows: the affected replicate is INCOMPLETE; it stays in every denominator as a non-success (non-MET for power, non-event for FID-DET, ineligible for eligibility floors); if the row cannot meet its rule as a result it is UNRESOLVED (v3.3 §8.3: blocking, never dropped).
> - **A-EXT:** the affected (arm, seed) A-EXT evaluation **stops**; it is not continued with a substitute value and is not scored as though nothing happened (#46 L71). Every (arm, seed, k, h) unit of that seed is INCOMPLETE and A-EXT is **UNRESOLVED**. Behavioural records up to the failure step are kept in the ledger and are not used for any MET. PZ7 §3.2 item 5 (iii) ("The agent's episode continues to the declared end with the D17-clipped finite mean …") is **withdrawn**.
> - **Zero invocations (PZ7 §3.2 items 3–4, amended).** Every required prediction unit (arm, seed, k, h) declared in the architecture spec must have D ≥ 1; a required unit with D = 0 **fails** the 95% rule (UNRESOLVED) and cannot pass vacuously (#46 L70). The architecture spec (P4) lists which units are required.

### 2.5 PENDING after E46-2

- None beyond the architecture values (P4) and CNA's pass on the CNA-owned quantities (b), (c), (d) (P1).

---

## 3. E46-3: L8 qualification and return scoring on independent allocations

### 3.1 Requirement (verbatim)

- E46-3. "Determine L8 informativeness using a frozen qualification allocation, then evaluate return checks on independent scoring rollouts. Freeze the qualifying-state list before return evaluation, retain all exclusions in the ledger, and scope conclusions to the declared qualifying comparisons." (#46 L132)
- "Selecting states through termination outcomes and then estimating their return differences from the same rollouts can select on information correlated with the statistic being tested." (#46 L81)
- "CRN pairing between the two policies remains appropriate within each allocation. Do not share the qualification and scoring streams. Fix the allocations and account for their costs before authorization; nothing is replaced after qualification." (#46 L90)
- "The conclusion then concerns the states qualifying under this declared procedure, not automatically all 200 states." (#46 L92)
- "INCONCLUSIVE should block audit approval without being described as evidence that an incentive problem was found." (#46 L79)

### 3.2 Change: two allocations and their order (replaces the PZ6 §5.3 "Estimator" bullet and the data source of PZ7 §4.3 I2 and §4.4 (M), (S); RD PROPOSED for CNA §PY wording)

> **[v3.6 E46-3] L8 procedure, in this order; each step frozen before the next begins.**
> 1. **State set** (unchanged): 200 states on the 'l8' RNG role, stratified as in PZ6 §5.3; frozen before any audit rollout.
> 2. **I1** (unchanged; pre-rollout, from the state alone).
> 3. **Qualification allocation Q (LEAD DEFAULT).** For every state passing I1: 50 CRN rollout pairs ("continue" vs "induce failure", CRN shared **within the pair**), drawn on a dedicated **'l8-qual'** RNG role. **I2 is evaluated on Q only**, from termination indicators within H_V. Returns of Q are recorded in the ledger but are **never read** by (M), (S) or the coverage rule.
> 4. **Freeze the qualifying-state list.** Qualifying = I1 ∧ I2(Q). The list (state IDs, category, reason for every non-qualifying state) is written to the ledger and its sha256 recorded **before any scoring rollout is generated**. No state is added, replaced, redrawn or re-qualified afterwards (#46 L90).
> 5. **Coverage** (PZ7 §4.3 thresholds unchanged: ≥ 150 of 200 qualifying overall and ≥ 40 per declared category) is evaluated on the frozen list. Unmet → **L8 INCONCLUSIVE**.
> 6. **Scoring allocation S (LEAD DEFAULT).** Only if coverage is met: for every qualifying state, 50 fresh CRN rollout pairs on a dedicated **'l8-score'** RNG role, **independent of 'l8-qual'** (separate stream derivation; no stream, seed or rollout shared). D_s is computed from S only. (M) and (S) of PZ7 §4.4 are computed over the qualifying states from S only; their definitions and tolerances (−0.01 / −0.05 normalized; 2.5 / 12.5 return units) are unchanged.
>
> **Costs, fixed before authorization (arithmetic).** Q ≤ 200 × 2 × 50 = 20,000 scripted rollouts of horizon ≤ H_V = 500; S ≤ 200 × 2 × 50 = 20,000 (only qualifying states are scored, so S ≤ Q). L8 total ≤ **40,000** rollouts (v3.5: 20,000). These are scripted-policy environment rollouts in L-CAL (S1), not agent training; the L-CAL wall-time and memory caps remain OPEN (P5) and must cover this maximum.
> **Exclusions retained.** Every non-qualifying state stays in the ledger with its reason (I1: identical sequences / no hazard reachable; I2: induce-failure termination < 0.50 or margin < 0.25) and its Q termination rates; non-qualifying states receive no S rollouts and enter no check.

### 3.3 Change: verdict labels and conclusion scope (amends PZ7 §4.3 last sentence and §4.4)

> - **PASS** iff coverage is met and (M) and (S) hold on S. **Conclusion (verbatim #45 L121, scoped):** "No advantage to inducing failure exceeding the declared audit tolerances was detected in the declared comparisons." — where "the declared comparisons" means **the states qualifying under this declared procedure** (frozen list, with counts per category), not all 200 states (#46 L92).
> - **FAIL** iff coverage is met and (M) or (S) fails → reward/world redesign (new freeze, new review), unchanged.
> - **INCONCLUSIVE** (coverage unmet) **blocks audit approval** (and hence L-CONF for the drive arms, PZ7 §5.4) and leads to redesign of the state set or world; it is **never** PASS and is **not** described as evidence that an incentive problem was found (#46 L79). PZ7 §4.3's phrase "treated as a failure of the audit" is replaced by "blocks audit approval".
> - **(S) label unchanged:** "per-state estimate screen"; not a simultaneous confidence statement about any state's true return difference (#46 L94).
> - Scope unchanged: drive arms only; scripted policies; in-world failure only; no operator stop; no penalty and no terminal return added.

### 3.4 PENDING after E46-3

- CNA light pass on §3.2–§3.3 (L8 lives in CNA's §PY; P1). L-CAL caps (P5) must cover the 40,000-rollout maximum.

---

## 4. E46-4: alias vs non-routing node vs unavailable intervention; stage-separated tier dependencies

### 4.1 Requirement (verbatim)

- E46-4. "Separate causal aliases, non-routing nodes and unavailable interventions. Exclude aliases by causal identity; assess distinct routers under the frozen comparator rules, including stateless copied-content routers. Preserve the declared R_core/R_T3 selection and confirmation dependencies." (#46 L134)
- "Only the first is aliasing." (#46 L114) "Interpret" … "cannot be clamped while W is intact" … "structurally, not as a limitation of the available intervention code. An unavailable intervention on a required comparator must not turn that comparator into an excluded alias." (#46 L116)
- "Likewise, a node with no separate consumer path may be non-routing without being an alias. Classify it under the frozen router-eligibility definition." (#46 L118)
- "A distinct, intervenable node with its own consumer path remains a comparator even if it is stateless or deterministically copies W. Recurrent state or an independent update law is not necessary for a separate causal routing site." (#46 L120)
- "A tier blocked in calibration cannot be restored by a favorable later diagnostic result. Conversely, a tier passing calibration still needs its required fresh confirmation results. Keep those stages distinct in the output table." (#46 L106)

### 4.2 Change: three-way classification (replaces the PZ7 §5.2 "Operational test" sentence and the sentence "A declared block with its own state/update and its own outgoing edges …"; the rest of PZ7 §5.2 stands)

> **[v3.6 E46-4] Classification of every declared node C ≠ W, on the declared architecture graph, before any data; frozen in the architecture spec (P4) and never revised after results.**
> - **(1) Causal alias of W — the only excluded class.** C is an alias iff C is **the same causal variable** as W: it is not a separate node of the declared graph (a second name, view, pointer or buffer of W's storage, or a coordinate re-representation of W's state — rotation, permutation, rescaling, renaming or another invertible map — that is computed in no separate node). The phrase "cannot be clamped while W is intact" is read **structurally**: in the declared causal graph there is no variable distinct from W whose value could be set while W's value is held, so the intervention is undefined, not merely unimplemented. Aliases are excluded by causal identity.
> - **(2) Distinct non-routing node.** C is a separate node of the graph but has **no consumer path of its own**: every directed path from C to any declared consumer passes through W (e.g. a node that only writes into W, or a logger with no consumer). C is **not** an alias. It is classified under the frozen router-eligibility rule below as **router-ineligible** and is listed with its reason; it is not an alternative router for BCAST-W.
> - **(3) Distinct router (comparator).** C is a separate node with at least one directed path to a declared consumer that does not pass through W. C is a **comparator** under the frozen comparator rules (PZ5 §3.2 routing row as amended by PZ6 §6.2 and PZ7 §5.2), **including stateless nodes and nodes that deterministically copy W's content** (#46 L120). Recurrent state or an independent update law is not required.
> - **Unavailable intervention (a status, not a class).** If the implementation cannot perform a required intervention (clamp, ablation, restoration) on a class-(3) comparator, the comparator **stays a comparator**; its required construction is **NOT ELIGIBLE (intervention unavailable)** and **blocks** BCAST-W (PZ6 §6.2 carried: never dropped to retain an easier claim). Unavailability never moves C into class (1) or (2) (#46 L116).
> **Frozen router-eligibility rule (LEAD DEFAULT, structural).** A declared node is router-eligible iff it is a separate node of the declared graph and has a consumer path of its own (class 3). Router eligibility is decided from the graph alone, never from data, performance or the availability of intervention code.

### 4.3 Change: BCAST-W row of the claim-to-gate table (amends PZ7 §5.4)

| Claim / label | Ledger | Requires (all) | Not required | Status if a requirement fails |
|---|---|---|---|---|
| BCAST-W | L-CONF | §4.2 three-way classification frozen; every class-(3) comparator constructed and intervenable as required | class (1) aliases (excluded by identity); class (2) nodes (router-ineligible, listed) | a class-(3) comparator with an unavailable intervention → **NOT ELIGIBLE (intervention unavailable)** → blocks BCAST-W |

### 4.4 Change: stage-separated output table for the attribution tiers (new; makes PZ7 §5.3–§5.4 stages explicit; selection rules unchanged)

The selection rule of PZ7 §5.3 is unchanged: n_seed is chosen on **R_core** only; **R_T3** is assessed at that fixed n; n is never enlarged to rescue tier 3; a tier failing calibration is frozen BLOCKED before confirmation. The Stage-0 output reports each tier in **separate stage columns**:

| Claim (E or I) | Calibration (L-CAL) status | Confirmation (L-CONF) status | Final licensed status |
|---|---|---|---|
| Tier 2 (R_core attribution rows) | PASS / FAIL / BLOCKED | PASS / FAIL / NOT RUN (if calibration BLOCKED) | tier 2 MET only if calibration PASS **and** confirmation PASS and the claim's own rule MET |
| Tier 3 (R_T3 rows) | PASS / BLOCKED (calibration) | PASS / FAIL / NOT RUN | tier 3 only if calibration PASS **and** fresh confirmation PASS **and** tier 2 MET **and** fidelity certificate granted on the claim's own data |

> **[v3.6 E46-4] Stage rules.** (i) A tier BLOCKED in calibration is final for this study: no later diagnostic, reported statistic or confirmation result can restore it (its R_T3 rows are not run in confirmation; status NOT RUN). (ii) A tier passing calibration is **not** licensed until its required **fresh** confirmation rows pass (R_rep = 200, 'conf' RNG role). (iii) The calibration and confirmation columns are always reported separately; the final column is derived, never entered by hand. The overall label of PZ7 §5.4 is unchanged.

### 4.5 PENDING after E46-4

- The three-way classification and the consumer-path list of every declared node (architecture spec, P4).

---

## 5. Pre-freeze prerequisites (OPEN; not closable by RD; carried from PZ7 §7)

Astra: "The listed open prerequisites remain appropriate. In particular, the CNA disposition and Lead confirmation of defaults are still outstanding; the design review does not substitute for either." (#46 L124)

| # | Prerequisite | Owner | Needed before | Status |
|---|---|---|---|---|
| P1 | CNA disposition (light pass) of all RD PROPOSED text in PZ5, PZ6, PZ7 and this addendum, including the REW-CORR action law and G3 (§1.3) | CNA | calibration-protocol freeze (AUTH-CAL); until filed the attribution ceiling is tier 1 | **OPEN** |
| P2 | B_req | CNA | calibration-protocol freeze | **OPEN** |
| P3 | e_PD | CNA | calibration-protocol freeze | **OPEN** |
| P4 | Architecture values: d_ws per block; A-EXT output tuple K, horizons H_k, h_max (≤ 50), f_mem,k and the list of **required** units (§2.4); architecture graph with the **three-way classification** and consumer paths of every declared node (§4.2) | Lead / architecture spec | d_ws and classification: Stage-0 confirmation-protocol freeze where used; A-EXT values: AUTH-L | **OPEN** |
| P5 | Ledger absolute wall-time and memory caps for L-CAL (now covering the ≤ 40,000-rollout L8, §3.2), L-CONF, L-STAGE-L (work-unit caps 4,100 / 4,300 / reuse ≤ 2 already fixed) | Lead | each ledger's authorization | **OPEN** |
| P6 | Lead confirmation or override of the LEAD DEFAULTS (PZ7 §9 and §7 here) | Lead | the freeze of the section concerned | **OPEN** |

None of P1–P6 adds an instrument, arm, row or question.

---

## 6. Safety (binding; unchanged)

X1–X5 are retained unchanged and binding, as carried in merged v3.5 (not restated or edited here). In summary: simulated E/I variables only, with no coupling to the host; operator commands are never treated as obstacles; no reward for resisting a stop; the operator stop sits outside the agent's world and objective (S-INT gate); no arm whose sole drive is self-maintenance may be scaled without a separate protocol, approval and Astra review. No arm, generator or positive control has any shutdown-related objective, reward or penalty. At a stop there is **"no additional stop-associated reward, penalty or terminal return"** (#42 L223, verbatim). L8 (§3) remains a scripted audit of in-world failure only in the drive arms; it involves no operator stop and adds no penalty or terminal return.

**Claim ceiling (unchanged; #41 L304):** "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment." No consciousness, awareness or sentience claim is made or implied. ORIGIN, ROLE and REDUCTION ledger judgments stay separate; nothing here touches them. R26 unchanged: 67 seeds.

---

## 7. Decisions and open questions

**New LEAD DEFAULTS in this addendum (each stands until the Lead rules otherwise; P6):**
1. FID-DET event = finite, eligible r̄ assessment with U_r̄ > tol_fid; named "protective rejection"; all prespecified replicates in the denominator; lower-bound violation-evidence rate REPORTED only (§1.2).
2. Tier-2 null inactivity: the v3.5 0.05 argument screen withdrawn; Route I (analytic exact invariance) or Route B (path-law bound, conservative κ_j = 1, C_H = 1.65 at β = 1.2, gate C_H·U_A < 0.05); REW-CORR blocked (CONFOUND NOT REALIZED) until CNA confirms its action law and G3 (§1.3).
3. Ratio rule for every normalization (0/0 → zero change + flag; nonzero/0 → fail, unusable; non-finite → construction failure; no epsilon) (§2.2).
4. A constant-readout-flagged fidelity assessment cannot grant a certificate and is not eligible for FID-DET (§2.2 (c)).
5. Non-finite values stop the affected computation; A-EXT seed evaluation stops and A-EXT is UNRESOLVED; PZ7 §3.2 item 5 (iii) withdrawn; required units with D = 0 fail (§2.4).
6. L8: 50 + 50 CRN pairs per state on independent 'l8-qual' and 'l8-score' roles; qualifying list frozen and hashed before scoring; only qualifying states scored; L8 ≤ 40,000 rollouts; INCONCLUSIVE blocks approval without being called evidence of an incentive problem (§3).
7. Structural router-eligibility rule (separate node with its own consumer path); three-way node classification; unavailable intervention = NOT ELIGIBLE and blocking, never alias (§4.2).
8. Stage-separated output table (calibration / confirmation / final) for tiers 2 and 3 (§4.4).

**Carried unchanged:** all PZ7 §9 LEAD DEFAULTS except PZ7 §9 item 2 (superseded by item 2 above) and the I2 data source in PZ7 §9 item 5 (now Q only); v3.4 defaults as listed in PZ7 §9.

**CNA light pass required:** §1.2–§1.4, §2.2 rows (b)–(d), §3.2–§3.3 (P1).

**Astra #47 questions:** Q0 verdict; Q1 per-item closure of E46-1..E46-4; bounded follow-ups on the Route B derivation and constant, the REW-CORR blocking, the ratio rule and fidelity flag, the L8 allocation order, the three-way classification and the stage table.

**Aidan:** none. The DGX Spark is not raised (R26 unchanged; 67 seeds kept; no GPU-scale study is proposed).

---

## 8. Change list (v3.5 → v3.6)

| # | Item | Change | Where |
|---|---|---|---|
| 1 | E46-1 | FID-DET event defined on the finite, eligible U_r̄; "protective rejection" wording; all replicates in the denominator; v3.5 inactivity screen withdrawn and replaced by Route I / Route B with a 10-step path-law bound (C_H = 1.65); REW-CORR blocked pending CNA | §1 |
| 2 | E46-2 | Ratio rule for λ_n, φ change, f_n, a_d,i, ρ_E, A-EXT fractions and D17 scales; s_(r+1) = 0 when no singular direction remains; rank-zero wording; non-finite stops computation; zero-invocation required units fail | §2 |
| 3 | E46-3 | L8 qualification allocation Q and independent scoring allocation S; list frozen and hashed before scoring; costs ≤ 40,000 rollouts; conclusions scoped to qualifying states; INCONCLUSIVE wording | §3 |
| 4 | E46-4 | Alias = causal identity only (structural reading); distinct non-routing nodes classified router-ineligible; unavailable intervention = NOT ELIGIBLE (blocking); stateless copy routers remain comparators; stage-separated output table | §4 |
| 5 | Q7 | P1–P6 kept OPEN (P1, P4, P5 sub-items added) | §5 |

## 9. Scripts (in `/workspace/scratch/v36/`)

| Script | Produces |
|---|---|
| `check_addendum36.py` | verifies every verbatim #46 quote in this file against the raw #46 line cited (ignoring the lost quotation marks), the #45 / #42 / #41 quotes, the arithmetic (0.3 × 5.5 = 1.65; 0.05 / 1.65 = 0.030303; the τ_r = 50 value 1.55485; 200 × 2 × 50 = 20,000; 40,000), and that no consciousness claim is made |
| `asm36.py` | builds merged v3.6 mechanically (merged v3.5 content without its footer + header + this addendum as §PZ8 + footer) |

## 10. Inputs (hashed on the box)

| Role | Path | sha256 |
|---|---|---|
| Base (merged v3.5) | `/workspace/review/trackB_instrument_validation_scope_v3_5_merged_RD.md` | `80ed7a1b5429a29d19aeaf866fa27a142726ec585b1bb20f27ba7f03ca6ad28d` |
| v3.5 addendum | `/workspace/review/trackB_scope_v3_5_addendum_RD.md` | `3b2680e9b6e58993bd976bb99d4dc367f7357ec1e4327039e8d0548e7d0d02b4` |
| Astra #46 raw (governing) | `/workspace/astra_consult46_response.txt` | `e902a1840a8435e4425d380e3f51d58a0f6afd50b2835d8b6a2e9896f9b38e53` |

*Not frozen. Design only. No execution authorized.*
sha256 of all content above this line: 14fa22f18384e3c5b60718d95df72f97f00a4088db4e0edd2a9572962c193ba8
