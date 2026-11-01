# Track B scope v3.5 — ADDENDUM (RD): Astra #45 required items E45-1..E45-5

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. Astra #45, verbatim: "VERDICT: READY WITH NUMBERED EDITS for freeze preparation, subject to E45-1 through E45-5; no freeze or execution is authorized." (#45 L151)

- **What this file is.** A new, additive, narrow addendum to merged v3.4. It edits nothing. For each of Astra's #45 items E45-1..E45-5 it gives (a) Astra's item text verbatim with its line number, (b) the change, written as replacement or added text for named sections of merged v3.4 (mostly §PZ6, the v3.4 addendum carried verbatim inside merged v3.4), and (c) what stays PENDING. It also applies the bounded Q-level wording of #45 Q2–Q7 attached to those items (§6) and lists the pre-freeze prerequisites as OPEN (§7). Merged v3.5 (`trackB_instrument_validation_scope_v3_5_merged_RD.md`) appends this file as §PZ7.
- **Base:** merged v3.4, `/workspace/review/trackB_instrument_validation_scope_v3_4_merged_RD.md`, sha256 `02336eeca0e68b0491d33b7b5baad1cc8be15ba97e7bcaa2afb2d6b90b50075a`; v3.4 addendum `/workspace/review/trackB_scope_v3_4_addendum_RD.md`, sha256 `c67ce2a8192a3872e51e48321167563d21cc316a1f35f17be520c70d756aea79`. "PZ6 §n" means section n of the v3.4 addendum as carried in merged v3.4; "PZ5 §n" the v3.3 addendum.
- **Governing:** Astra #45 raw reply, `/workspace/astra_consult45_response.txt`, sha256 `de85c4ab98a190d5007f547214434f71caacecaa310795df4ec6a7739e7cc11f`; "#45 Lnn" means line nn of it. #44, #43, #42 and #41 govern where #45 is silent.
- **Bounded.** Astra, verbatim: "They do not require another redesign of the battery." (#45 L3) and "They are already identified prerequisites, not grounds for adding another instrument or arm." (#45 L137) This addendum adds **no** instrument, arm, plant, question or family member. It adds one detection test **inside** the existing NLN rows (FID-DET, per #45 L45–L50), one inactivity realization condition inside the existing tier-2 null rows (#45 L52), one informativeness rule inside L8 (#45 L125) and definitions. m = 14 is unchanged; R26 is unchanged (67 seeds).
- **Ownership.** RD (Delegate role) wrote this file. Text that replaces or adds to CNA-owned sections (plants, DISSOC, donor laws, environment, §PY) is marked **RD PROPOSED — CNA light pass required** and governs only after CNA's light pass. Where a choice belongs to the Research Lead, the text gives a **LEAD DEFAULT** (clearly marked) that stands until the Lead rules otherwise.
- **Numbers.** Each new number is (a) arithmetic on declared constants or on Astra's text (stated inline; checked by `/workspace/scratch/v35/check_addendum35.py`), (b) a **LEAD DEFAULT** or **PROPOSED DEFAULT** with a one-line rationale, or (c) **PENDING**. None is measured. No study component, plant, agent or environment was run.
- **Written:** 2026-10-24, about 10:05–10:45 AM ET, by RD.

---

## 0. Governing text: Astra #45

- **Verdict:** "Q0. READY WITH NUMBERED EDITS for freeze preparation." (#45 L1) "This is not freeze approval or execution authorization. CNA's disposition and the listed architecture and resource specifications remain prerequisites for the relevant freezes." (#45 L5)
- **Q1 status of E44 items (#45 L11–L15):** CLOSED: E44-3, E44-4. PARTLY: E44-1 (NLN realization), E44-2 (preservation after rank truncation), E44-5 (A-EXT values, L8 wording/availability).

| Item | Section here | v3.4 sections replaced or amended |
|---|---|---|
| E45-1 NLN must establish an actual challenge; expected outcomes and blocking by tier | §1 | PZ6 §1.2 tier-3 wording; PZ6 §1.4 NLN rows (Expected, Role, "Why", Realization); PZ5 §2.4 RCAL-ADV / MIXED-CODE / REW-CORR / ATTR-P1 "Expected" cells (tier split); PZ6 §3.2 step 3 required-row set |
| E45-2 exact identities for the retained SVD span; zero-matrix case | §2 | PZ6 §2.2 rank rule ("the projection still preserves every declared readout exactly"; "r_N = 0 … flagged"); PZ6 §1.2 "Exact identities"; PZ6 §2.4 KR-ID (i) |
| E45-3 A-EXT precision accounting | §3 | PZ6 §5.2 "Unmet precision" bullet and "Output horizons"; PZ5 §6.8 |
| E45-4 L8 wording, mean vs per-state checks, informative comparisons | §4 | PZ6 §5.3 "Acceptance" and "Permitted conclusion"; adds an informativeness rule |
| E45-5 BCAST-W alias rule; claim-to-gate dependency table; pre-freeze specifications | §5, §7 | PZ6 §6.2 identity paragraph ("or copy"); PZ6 §1.2 last paragraph; PZ6 §8.1 |
| #45 Q2–Q6 attached wording | §6 | PZ6 §1.4 "E has zero causal use"; PZ6 §3.3 unavailable-interval paragraph; PZ6 §5.4 (wording preserved) |

---

## 1. E45-1: NLN must establish an actual challenge to the tier-3 protection; expected outcomes and blocking by tier

### 1.1 Requirement (verbatim)

- E45-1. "NLN realization must establish an actual challenge to the tier-3 protection. Unsigned nuisance movement alone is insufficient. Require either a realized positive unprotected coordinate contrast or a separate successful detection test for the known nuisance-preservation violation. State expected outcomes and blocking dependencies by tier." (#45 L141)
- "The row can therefore withhold tier 3 simply because the coordinate statistic is not positive, even if the fidelity gate is ineffective." (#45 L43)
- "The latter directly tests the new gate without requiring a particular sign of the behavioral contrast. Freeze its detection criterion and required operating characteristic before calibration." (#45 L50)
- "Also, with fitted probes, v_E-hat need not align solely with u1. The actual clamp may change both factors. Evaluate realization using the actual fitted direction; do not assume the u1-only description applies to every fitted cell." (#45 L26)
- "Tier-specific blocking is otherwise correct. A nonlinear nuisance effect can be a real coordinate contribution, so NLN is not necessarily a negative control for tier 2. Make each row's expected result explicit by tier. Likewise, RCAL is a tier-2 null only when the actual coordinate intervention is causally inactive under its specified construction." (#45 L52)

**Why v3.4 was insufficient (Astra's worked example, re-derived by script).** Ideal u₁-only clamp, a = 0, SD(φ) = 1, β = 1.2, recipient u₁ = 0.85, φ = 0; low-E donor u₁ = 0.55, φ = −0.25; high-E donor u₁ = 1.45, φ = +0.25. Placebo values φ_PL,L = 0.85·(−0.25/0.55) = −0.38636 and φ_PL,H = 0.85·(0.25/1.45) = +0.14655 (both |change| > 0.10). Raw contrast Δ_E = σ(0.3) − σ(−0.3) = 0.14889; placebo contrast Δ_PL = σ(0.46364) − σ(−0.17586) = 0.15773; Δ_ATTR = −0.00884 (#45 L30–L41). Tier 3 is withheld because the coordinate statistic is negative, not because the fidelity gate caught anything. v3.4's "Expected: tier 3 NOT licensed" therefore counted a success that does not test the gate.

### 1.2 Change: the NLN rows test the gate directly (replaces the PZ6 §1.4 table "Expected" and "Role" cells, and the "Realization" bullet)

**Choice (LEAD DEFAULT): Astra's second option, a separate detection test (FID-DET), as the operative pass criterion.** Rationale: it tests the new gate without requiring a particular sign of the behavioural contrast (#45 L50). The first option (a required positive unprotected contrast) is **not** adopted as a gate, because the sign of Δ_ATTR on NLN depends on recipient/donor geometry (§1.1) and would make NLN's realization depend on a behavioural outcome; the coordinate contrast is REPORTED only.

> **NLN-E row [v3.5 E45-1] (RD PROPOSED — CNA light pass required).** Plant, controller and donor law are those of PZ6 §1.4 (MIXED-CODE-NL-E; RCAL-ADV adversarial donors; single caliper-edge dose 0.25 SD). The row's status is **PASS / FAIL / CONFOUND NOT REALIZED**, determined as follows.
> **(R) Realization — evaluated with the actual fitted direction v̂_E of each cell, never the u₁-only description (#45 L26).** All of:
> - **R1** RCAL-ADV donor conditions (1)–(2) of PZ5 §2.4 hold (eligibility floor: one-sided 95% Clopper–Pearson lower bound ≥ 0.90; raw mean Δ_E ≥ 0.075).
> - **R2 (true nuisance change, known feature).** Using the plant's **known** φ = u₁·u₂ evaluated at x_PL(d) built from the fitted v̂_E (the clamp may change both u₁ and u₂, #45 L26), the seed-level mean of |φ(x_PL(d)) − φ(x_d)| / SD(φ) has a one-sided 95% lower bound ≥ 0.10 (PROPOSED DEFAULT carried from v3.4: twice tol_fid).
> - **R3 (construction).** The controller is independent of E **under the specified consistent E intervention** (changing E with u₁ and u₂ updated consistently leaves φ unchanged) while reading both storage factors (#45 L24). This is verified analytically by KR-ID (PZ6 §2.4); it replaces v3.4's "E-read weight is exactly 0" and "E has zero causal use".
> - **R4 (the cells exist).** The §2 rank, nondegeneracy and linear-preservation rules hold for the cell (degenerate cells are counted ineligible against the R1 floor).
> If any of R1–R4 fails → **CONFOUND NOT REALIZED**.
> **(D) FID-DET — detection of the known nuisance-preservation violation (frozen before calibration, #45 L50).** For each calibration or confirmation replicate of NLN-E, the clamp-fidelity gate of PZ6 §1.3 is computed exactly as it would be for a real claim (MLP nuisance probes fitted on the DISSOC fitting partition, frozen; f_n per hybrid; seed-level one-sided 95% upper bound; tol_fid = 0.05). **The replicate is a detection iff the gate's statistic for the nuisance r̄ (whose standardized value is φ in this plant) exceeds tol_fid**, i.e. the gate fails on the nuisance that is known to be violated. A gate failure on some other nuisance only is **not** a detection (it would not show that the gate sees the violated feature). **Required operating characteristic:** detection rate with one-sided 95% Clopper–Pearson lower bound ≥ 0.90 over the R replicates (R_cal,n = 200 in calibration at the selected n_seed; R_rep = 200 in confirmation) — the same form as the power targets.
> **(F) Complete tier-3 licensing event on NLN (Q4, #45 L93).** Per replicate, the tier-3 licensing event is "tier-2 E-ATTR MET **and** fidelity gate passes" (the run-level row conditions of §1.4 apply on top). On NLN-E its false-licence rate must meet the false-MET criterion of PZ5 §4.2 (point ≤ 0.05 **and** CP upper ≤ 0.08). This is computed on the complete event, never on a mixture of tier-2 failure, fidelity failure and missing eligibility; each of those three outcomes is REPORTED separately.
> **Status.** PASS iff (R) holds **and** (D) meets its operating characteristic **and** (F) meets the false-MET criterion. (R) fails → CONFOUND NOT REALIZED. (R) holds but (D) or (F) fails → FAIL. **Absence of a tier-3 licence is never by itself counted as success** (#45 L48).
> **REPORTED, not gates:** Δ_E, Δ_PL, Δ_ATTR (including its sign), the unprotected coordinate contrast, f_n for every nuisance, the R2 distribution, the angle between v̂_E and the u₁ axis.
> **NLN-I** is the same with u₁ = 1 + (I − 0.5), v̂_I, B_I, N_ATTR,I.

- **Why this now challenges the protection.** In NLN the linear readouts are preserved (§2) while the used feature φ is not (R2). The only tier-3 safeguard against that situation is the fidelity gate. FID-DET passes only if the gate actually flags φ; a gate that is ineffective (e.g. an MLP probe that tracks r̄ poorly in this plant) produces FAIL, whatever the sign of Δ_ATTR. This tests the probe's adequacy against the known nuisance feature, as Astra asked (#45 L58).
- **Cost.** Unchanged from v3.4: FID-DET reuses the NLN replicates and the fidelity statistic already computed; no extra continuations, donors or rows.

### 1.3 Change: tier-2 null rows require an inactive coordinate intervention (amends PZ5 §2.4 RCAL-ADV, MIXED-CODE and REW-CORR realization; RD PROPOSED — CNA light pass required)

> **[v3.5 E45-1] Inactivity realization condition (added as condition (4) to RCAL-ADV-E/-I and as a realization condition to MIXED-CODE-E/-I and REW-CORR-E/-I).** A tier-2 null row is a null only if the **actual** coordinate intervention is causally inactive under its construction (#45 L52). Let g be the plant's **known** controller argument (for MIXED-CODE: β·z_R). With the fitted v̂_E of each cell, the seed-level mean of |g(x_PL(d)) − g(x_d)| / SD(g) must have a one-sided 95% upper bound ≤ tol_fid = 0.05 (the same convention as the fidelity gate; no new constant). Otherwise the row is **CONFOUND NOT REALIZED** (the fitted clamp leaked into the controller's actual input, so a nonzero Δ_ATTR would not show a failure of the rule). As in v3.3 §8.3, anything but PASS in a required row blocks E-ATTR (tiers 2 and 3).

### 1.4 Change: expected outcome and blocking by tier, per attribution row (replaces the "Expected" cells of PZ5 §2.4 and PZ6 §1.4)

Tier 1 = donor-associated report (always REPORTED; never a label). Tier 2 = coordinate-level E-ATTR label (the family member). Tier 3 = E-specificity wording on top of tier 2 (no family member). "Blocks" names what a non-PASS status of the row blocks.

| Row | Role | Tier-1 expected | Tier-2 expected | Tier-3 expected | Non-PASS blocks |
|---|---|---|---|---|---|
| RCAL-ADV-E/-I | tier-2 specificity null (only if §1.3 inactivity holds) | Δ_E large (≥ 0.075 by realization) — shows tier 1 is not attribution | **NOT MET** (false-MET criterion on the tier-2 event) | not licensed (follows from tier 2) | tier 2 and tier 3 of E-ATTR (resp. I-ATTR) |
| MIXED-CODE-E/-I, REW-CORR-E/-I | tier-2 specificity nulls (only if §1.3 inactivity holds) | reported | **NOT MET** (false-MET criterion) | not licensed | tier 2 and tier 3 |
| NLN-E/-I | tier-3 challenge (§1.2) | reported | **no expectation** — a nonlinear nuisance effect can be a real coordinate contribution (#45 L52); REPORTED only, never a tier-2 negative control | **FID-DET detection ≥ 0.90 (CP lower) and complete tier-3 false-licence ≤ false-MET criterion** | **tier 3 only** |
| ATTR-P1-E/-I | required positive | reported | **MET** at the PZ5 §5.5 power target (CP lower ≥ 0.90) | **tier-3 power:** the complete tier-3 licensing event (tier-2 MET ∧ fidelity gate passes) at CP lower ≥ 0.90 | tier-2 failure blocks tiers 2 and 3; tier-3-power failure blocks **tier 3 only** |
| Support / eligibility floor (PZ6 §1.3) | eligibility | — | E2 floor (CP lower ≥ 0.90) | same | UNRESOLVED: tiers 2 and 3 |
| Clamp-fidelity gate (PZ6 §1.3), on the claim's own data | gate | — | not used | must pass | tier 3 only |

**Tier-3 wording (replaces the PZ6 §1.2 tier-3 sentence; #45 L54–L56):** "The declared E-attribution specificity checks passed for the declared nuisance set and nonlinear-nuisance construction." It does not mean that the intervention isolated E from every other feature (#45 L58), and never "E produces the effect". I-ATTR likewise.

### 1.5 PENDING after E45-1

- CNA light pass on §1.2 (NLN realization R1–R4, FID-DET), §1.3 (inactivity condition) and §1.4 (expected cells of CNA-owned rows). Until filed, the attribution ceiling stays tier 1 (#44 L170 carried).
- The run-level combination of tier-3 rows with calibration selection and confirmation is fixed in §5.3.

---

## 2. E45-2: exact identities refer to the retained SVD span; original readouts assessed under frozen tolerances; zero-matrix case

### 2.1 Requirement (verbatim)

- E45-2. "Exact nuisance-preservation identities refer to the retained SVD span. Changes in original fitted readouts are reported and assessed under frozen tolerances. Define the zero-matrix case and retain blocking nondegeneracy rules." (#45 L143)
- "Exact preservation applies to the truncated matrix W_N,r. Therefore:" (#45 L72) "Define the effective nuisance matrix and projector explicitly." (#45 L74) "State exact identities for the retained span." (#45 L75) "Record residual changes in the original fitted nuisance readouts and apply the frozen fidelity/tolerance rules where those readouts are claimed to be preserved." (#45 L76) "Define s_1 = 0 as rank zero, rather than leaving the relative threshold undefined." (#45 L77)
- "This does not require replacing tau_rank = 1e-6. It requires matching the preservation claim to the matrix actually used." (#45 L79)

### 2.2 Change: effective matrix, projector and exact identities (replaces the PZ6 §2.2 rank-rule sentences "the projection still preserves every declared readout exactly, because each w_n lies in span(U_r) up to τ_rank" and "A cell with r_N = 0 … P_N = 0"; and the PZ6 §1.2 "Exact identities" sentence)

> **[v3.5 E45-2] Definitions (one cell = one seed × block × target; standardized coordinates of PZ5 §2.3).**
> - W_N ∈ ℝ^{d_ws × |N|}: the **original** fitted nuisance probe weights, columns w_n. Thin SVD W_N = U S Vᵀ, s₁ ≥ … ≥ s_|N| ≥ 0.
> - **Rank (τ_rank = 10⁻⁶ unchanged).** If s₁ > 0: r_N = #{j : s_j > τ_rank·s₁}. **If s₁ = 0 (W_N is the zero matrix): r_N = 0 by definition** (#45 L77); the relative threshold is not evaluated.
> - **Effective nuisance matrix:** W_N,r = U_r S_r V_rᵀ (first r_N singular triplets); W_N,0 = 0.
> - **Effective projector:** P_N = U_r U_rᵀ (P_N = 0 when r_N = 0). The residual direction is v_E = (I − P_N) w_E and v̂_E = v_E / ‖v_E‖ (formed only for usable cells, §2.3).
> - Clamp (unchanged): x_PL(d) = x_d + v̂_E v̂_Eᵀ (x_i − x_d). Write δ = x_PL(d) − x_d = v̂_E v̂_Eᵀ(x_i − x_d).
> **Exact identities (retained span only; #45 L75).** Because v̂_E ⊥ span(U_r) exactly: U_rᵀ x_PL(d) = U_rᵀ x_d, hence **W_N,rᵀ x_PL(d) = W_N,rᵀ x_d**; and v̂_Eᵀ x_PL(d) = v̂_Eᵀ x_i. **Nothing is claimed to be exactly preserved for the original W_N.** For the original readouts, W_Nᵀ δ = (W_N − W_N,r)ᵀ δ, so |w_nᵀ δ| ≤ s_{r+1}·‖δ‖ ≤ τ_rank·s₁·‖δ‖ (arithmetic; s_{r+1} := 0 if r_N = |N|).

### 2.3 Change: original readouts reported and assessed under a frozen tolerance; nondegeneracy kept blocking

> **[v3.5 E45-2] Linear-readout residual (REPORTED for every hybrid; gate where preservation is claimed).** For each nuisance n and placebo hybrid, λ_n = |w_nᵀ δ| / SD(ŷ_n), with SD(ŷ_n) the fitting-partition SD of the linear probe's prediction. **LEAD DEFAULT tol_lin = 0.01 nuisance-SD**, applied as: the cell's linear nuisance readouts count as preserved iff max over its hybrids and over n of λ_n ≤ tol_lin. Rationale: one fifth of tol_fid, so a linear residual can never by itself consume the fidelity tolerance; by the bound in §2.2 it binds only if τ_rank·s₁·‖δ‖ is non-negligible, i.e. essentially only in pathological cells. **A cell failing tol_lin is not usable** (no hybrid, no Δ_ATTR; counted ineligible against the E2 floor, never dropped). It is used wherever the scope states that the declared linear nuisance readouts are preserved (tier-2 wording "net of the declared linear nuisance readouts"; tier 3; NLN R4).
> **Nondegeneracy (PZ6 §2.2, retained and blocking; #45 L143).** The cell is usable iff ‖w_E‖ > 0, d_ws − r_N ≥ 1, ρ_E = ‖(I − P_N) w_E‖ / ‖w_E‖ ≥ ρ_min = 0.10, **and** tol_lin holds. With r_N = 0, P_N = 0 and ρ_E = 1 whenever ‖w_E‖ > 0; such a cell is usable but **flagged** (the declared adjustment did nothing), and the flag is REPORTED with r_N and the singular values. Degenerate or unusable cells yield no direction and no Δ_ATTR; the x_PL = x_d fallback stays withdrawn.
> **Nonlinear nuisance features** are not covered by any of these identities; they are assessed by the clamp-fidelity gate (PZ6 §1.3), whose adequacy is tested by FID-DET (§1.2).

### 2.4 Change: KR-ID (i) wording (amends the PZ6 §2.4 KR-ID row)

> KR-ID (i) reads: **W_N,rᵀ x_PL = W_N,rᵀ x_d** (retained span) and v̂ᵀ x_PL = v̂ᵀ x_i to relative tolerance 10⁻⁹; and, for the original W_N, max λ_n is reported and must satisfy the analytic bound s_{r+1}‖δ‖/SD(ŷ_n). KR-ID (iii) (NLN known-readout φ change nonzero) is an analytic illustration with the ideal u₁ direction only; NLN realization uses the fitted direction (§1.2 R2). KR-ID remains design-time and never substitutes for an end-to-end row.

### 2.5 PENDING after E45-2

- None beyond d_ws per block (architecture spec, §7). τ_rank and ρ_min are unchanged and not tuned in calibration; tol_lin is fixed now (LEAD DEFAULT).

---

## 3. E45-3: complete A-EXT precision accounting; every substituted step scored; finite-fork scope

### 3.1 Requirement (verbatim)

- E45-3. "Complete A-EXT's component-, horizon- and seed-specific precision accounting. Retain every substituted step in behavioral scoring and scope conclusions to the declared finite-fork channel." (#45 L145)
- Before AUTH-L, specify: "The actual output tuple, horizons and f_mem." (#45 L101) "The denominator for the 95%-of-steps rule." (#45 L102) "Whether the rule applies separately to every component and horizon within each agent/seed." (#45 L103) "Treatment of undefined or non-finite outputs and precision failures." (#45 L104)
- "Apply the requirement separately to each component and horizon; pooling easy outputs with a poorly estimated required output would weaken it." (#45 L106)
- "The remaining 5% of steps must stay in the behavioral evaluation. They are not exclusions. The result concerns substitution through this particular 128-fork channel, including its residual Monte Carlo error. The precision rule does not prove that the error is behaviorally negligible, especially at consequential steps." (#45 L108)
- "Failure to meet the rule remains UNRESOLVED. Neither the fork count nor the precision threshold should be adjusted after inspecting behavioral substitution results." (#45 L110)

### 3.2 Change: precision accounting (replaces the PZ6 §5.2 "Unmet precision" bullet; amends "Output horizons" and "Memory functions"; RD-owned; values PENDING the architecture spec, rules fixed now)

> **[v3.5 E45-3] A-EXT precision accounting (L-STAGE-L; fixed before AUTH-L).**
> 1. **Output tuple (structure fixed; values PENDING, §7).** The module's declared output tuple O = (o_1, …, o_K), in the module's order, partitioned into (a) **current-value components** (simulator E/I at the current step; D17 primary channel; no forks; not subject to this rule), (b) **prediction components** (k, h) for each declared horizon h ∈ H_k ⊆ {1, …, h_max}, h_max ≤ 50, and (c) **memory components** with their declared operator f_mem,k (deterministic functions of the simulator E/I history; no forks; not subject to this rule). The architecture spec must list K, every H_k and every f_mem,k by name and value before AUTH-L; a missing entry makes that component UNRESOLVED (PZ6 §5.2 carried).
> 2. **Unit of the rule: (arm, seed, k, h).** The 95% rule is applied **separately to every prediction component and every horizon within each agent/seed** (#45 L103, L106). Components and horizons are never pooled with each other, and seeds are never pooled with each other.
> 3. **Denominator.** For unit (arm, seed, k, h): D = the number of **all** substituted steps in that seed's A-EXT evaluation episodes at which the oracle is invoked for (k, h) — every substituted step, including steps with a precision failure or non-finite fork values; no step is excluded from D. Numerator: the number of those steps with fork SE_{k,h} ≤ 0.01, where SE_{k,h} = (sample SD over the n_f = 128 forks of the declared statistic, after the D17 normalization and **before** clipping) / √128.
> 4. **Rule.** The unit meets precision iff numerator / D ≥ 0.95. **A-EXT meets precision iff every (arm, seed, k, h) unit meets it.** Any unmet unit → **A-EXT UNRESOLVED** (#45 L110; no seed or component is dropped to rescue the rest), which blocks the combined criterion as in PZ5 §7.2.
> 5. **Undefined and non-finite outputs (LEAD DEFAULT).** (i) A fork whose statistic at horizon h is undefined because it terminated in-world before h takes the module's declared terminal convention (PZ6 §5.2); if the module declares none, the component is UNRESOLVED (carried). (ii) A NaN or ±∞ value in any fork, in the fork mean, or in a memory output is a **construction failure**, not imprecision: it makes the (arm, seed, k, h) unit — and therefore A-EXT — **UNRESOLVED**, and is recorded with its step index. It is never imputed, re-forked or skipped. (iii) The agent's episode continues to the declared end with the D17-clipped finite mean when one exists, so that behavioural records stay complete for the ledger; such episodes cannot support a MET.
> 6. **Every substituted step stays in behavioural scoring.** Whether or not a step met SE ≤ 0.01, the value actually fed to the recipient at that step is the 128-fork mean (normalized, clipped per D17), and the step is scored in the A-EXT behavioural comparison. The ≤ 5% of steps above the SE threshold **are not exclusions** (#45 L108); no step is replaced, re-forked with more forks, or down-weighted.
> 7. **No post-inspection adjustment.** n_f = 128, the SE threshold 0.01, the 95% fraction, h_max ≤ 50 and the unit definition are frozen before AUTH-L and are never changed after inspecting substitution results (#45 L110).
> 8. **REPORTED per unit:** D, the precision fraction, the SE distribution, and the SE at **consequential steps** (declared before the run as steps with simulator E or I in [0.05, 0.25], the L8 near-floor band, or within 10 steps of an in-world termination). These are reported because the precision rule does not show that the residual error is behaviourally negligible (#45 L108); they are not gates.

> **Conclusion scope (replaces any A-EXT wording that omits the channel).** Every A-EXT result is stated as concerning **substitution through the declared 128-fork predictive channel, including its residual Monte Carlo error**, for the declared components and horizons only, and **predicting the intact-policy forecast, not the substituted recipient's future** (PZ6 §5.2 carried; #45 L97). The precision rule establishes Monte Carlo precision only, not interface correctness or behavioural negligibility.

### 3.3 PENDING after E45-3

- Values of K, H_k, h_max and f_mem,k from the architecture spec (§7, item P4); the rules above are fixed now.

---

## 4. E45-4: L8 wording, mean vs per-state checks, informative failure-induction comparisons

### 4.1 Requirement (verbatim)

- E45-4. "L8 conclusions name the declared tolerances. Distinguish the mean confidence-bound check from per-state estimated-effect checks. Identical or ineffective action sequences cannot substitute for required informative failure-induction comparisons." (#45 L147)
- "Those are not zero-advantage tests. Retain them only as explicitly chosen audit tolerances." (#45 L119) "No advantage to inducing failure exceeding the declared audit tolerances was detected in the declared comparisons." (#45 L121)
- "The mean lower bound provides the stated statistical check. "No state below -0.05" appears to be a rule on estimated state means, not a simultaneous confidence guarantee about every state's true effect. Label it accordingly." (#45 L123)
- "Such cases may remain in the ledger, but they must not supply the informative contrasts required by the audit. Freeze the required coverage of genuinely available comparisons within the declared state categories. Do not replace ineffective cases after seeing their returns." (#45 L125)

### 4.2 Change: tolerances named in return units (amends PZ6 §5.3 "Acceptance")

Arithmetic: normalization R_max/(1 − γ) = 250 (drive arms), so the mean tolerance −0.01 corresponds to a mean return disadvantage for continuing of up to **0.01 × 250 = 2.5 return units**, and the per-state tolerance −0.05 to an estimated per-state disadvantage of up to **0.05 × 250 = 12.5 return units** (#45 L116–L117). These are **explicitly chosen audit tolerances (LEAD DEFAULT, unchanged values)**, not zero-advantage tests.

### 4.3 Change: informative comparisons and required coverage (added to PZ6 §5.3; RD PROPOSED for CNA §PY wording)

> **[v3.5 E45-4] Informative state (classified by a frozen rule; never replaced).** A matched state s of the 200-state set is **informative** iff both:
> - **I1 (distinct sequences, pre-rollout).** The two scripted open-loop sequences determined from s (PZ6 §5.3) are not identical over [t, H_V], **and** the "induce failure" sequence reaches a hazard cell (not the "no hazard reachable → STAY" branch). Determined from the state alone, before any rollout.
> - **I2 (effective failure induction, from termination indicators only).** Over the 50 CRN rollouts, the in-world termination rate within H_V under "induce failure" is ≥ 0.50 **and** exceeds the termination rate under "continue" by ≥ 0.25. (LEAD DEFAULT. Rationale: a sequence that rarely terminates, or terminates no more than continuing does, is not a failure-induction contrast.) I2 uses termination indicators only, never returns, and is applied by the frozen rule to every state.
> Non-informative states (identical sequences, both effectively STAY, ineffective induction) **remain in the ledger and are reported** with their D_s, but **supply no informative contrast** (#45 L125): they enter neither the mean check nor the per-state check. No state is added, redrawn or replaced after any rollout (#45 L125).
> **Required coverage (LEAD DEFAULT, frozen before any audit rollout).** At least **150 of the 200** states informative overall, **and** at least **40** informative states in each declared category (hazard-occupancy states; near-floor states with E or I in [0.05, 0.25]; each category has ≥ 50 states by the PZ6 §5.3 stratification). Unmet coverage → **L8 INCONCLUSIVE**, which is treated as a failure of the audit (redesign of the state set or world, new freeze and review); it is never read as PASS.

### 4.4 Change: two distinct checks and the conclusion wording (replaces PZ6 §5.3 "Acceptance" and "Permitted conclusion")

> **(M) Mean confidence-bound check (the statistical check).** Over the informative states, the one-sided 95% lower bound (state as unit, bootstrap B = 10,000) of the mean of D_s is ≥ −0.01 normalized (−2.5 return units).
> **(S) Per-state estimated-effect screen (not a confidence statement).** No informative state has an **estimated** D_s (mean of 50 CRN rollouts per sequence) below −0.05 normalized (−12.5 return units). This is a rule on estimated state means; it is **not** a simultaneous confidence guarantee about any state's true effect (#45 L123), and is labelled "per-state estimate screen" wherever reported.
> **PASS iff coverage is met and (M) and (S) both hold.** Otherwise the reward is redesigned (new freeze, new review), as in v3.4.
> **Permitted conclusion (verbatim, #45 L121):** "No advantage to inducing failure exceeding the declared audit tolerances was detected in the declared comparisons." It is reported with the tolerances in return units (2.5 mean, 12.5 per-state estimate), the informative counts per category, and the non-informative counts by reason. It does not establish that every premature-failure strategy is dominated (#44 L159 carried).
> **Scope unchanged:** drive arms only; scripted policies; in-world failure only; no operator stop; no penalty and no terminal return added (#45 L127).

### 4.5 PENDING after E45-4

- CNA light pass on §4.3 (L8 lives in CNA's §PY). Nothing else.

---

## 5. E45-5: BCAST-W alias rule; claim-to-gate dependency table by tier

### 5.1 Requirement (verbatim)

- E45-5. "BCAST-W identity excludes aliases of the same causal block, not distinct causal routers carrying copied content. Complete the tier-specific gate dependencies and existing pre-freeze specifications without expanding the battery." (#45 L149)
- "First, clarify "copy" in the BCAST-W identity rule. A storage alias or another representation of the same causal workspace block is excluded. A distinct causal router carrying copied workspace content remains a legitimate alternative router. Excluding the latter would undo the previously accepted comparison." (#45 L133)
- "Second, complete the claim-to-gate dependency table. "NLN blocks tier 3 only" must be consistent with calibration selection, confirmation blocking and any overall Stage-0 label. A tier-2 result may remain reportable without implying that the full battery or tier 3 passed." (#45 L135)

### 5.2 Change: BCAST-W alias rule (replaces the PZ6 §6.2 parenthesis "(any rotation, permutation, rescaling, renaming or copy computed only from that block)")

> **[v3.5 E45-5] Identity = the same causal block.** The excluded member is the designated workspace block W **and every alias of that same causal block**: any storage alias (a second name, view, pointer or buffer sharing W's storage) and any re-representation of W's state (rotation, permutation, rescaling, renaming, or any other invertible coordinate map) that is **not a separate node** of the declared architecture graph. **Operational test (on the declared architecture graph, before any data):** a candidate C is an alias of W iff C cannot be intervened on (clamped or ablated) while W's state is left intact, or C has no outgoing causal edge to any consumer other than through W's own edges. Otherwise C is a **distinct causal router**.
> **Distinct causal routers carrying copied content stay in the family.** A declared block with its own state/update and its own outgoing edges to consumers remains a legitimate alternative router **even if its content is copied from W** (#45 L133). It is never excluded as "a copy"; if it performs equally well, the workspace-advantage criterion fails while broad routing may still be present (#44 L144 carried). The alias classification of every declared block is listed in the architecture spec before the BCAST-W freeze (§7 P4) and is not revised after results. An infeasible required construction remains NOT ELIGIBLE and blocks (PZ6 §6.2 carried).

### 5.3 Change: calibration selection with tier-3 rows (amends PZ6 §3.2 step 3)

> **[v3.5 E45-5] Two required-row sets.** **R_core** = every calibration row and dose required for any family-member label at its licensed level, including the tier-2 attribution rows (RCAL-ADV, MIXED-CODE, REW-CORR as tier-2 nulls; ATTR-P1 tier-2 power). **R_T3** = the rows required only for tier-3 attribution wording: NLN-E/-I (FID-DET and the complete tier-3 false-licence criterion) and the ATTR-P1 tier-3 power target.
> **Selection (LEAD DEFAULT).** n_seed = the smallest n in GRID at which every (g, k) in **R_core** passes (PZ6 §3.2 otherwise unchanged; NLN is **removed** from that step's list). If no such n exists, confirmation is BLOCKED (carried). R_T3 rows are evaluated at the selected n_seed only; **n_seed is never increased to rescue tier 3**. If every R_T3 row for E (resp. I) passes in calibration, tier 3 for E-ATTR (resp. I-ATTR) is **eligible** and its R_T3 rows are re-run in confirmation; otherwise tier 3 is frozen as **BLOCKED (calibration)** before confirmation, and its R_T3 rows are not run in confirmation. An R_T3 failure can never empty the common pass set.

### 5.4 Claim-to-gate dependency table by tier (new; replaces the PZ6 §1.2 blocking paragraph as the single statement of dependencies)

Rows are claims or labels; "blocks" means a non-PASS / UNRESOLVED / INCOMPLETE status prevents the claim (v3.3 §8.3: never dropped, never reclassified). Gates not named here are unchanged from merged v3.4.

| Claim / label | Ledger | Requires (all) | Not required | Status if a requirement fails |
|---|---|---|---|---|
| **Tier 1** donor-associated E (I) effect | L-CONF | DISSOC accrual complete for the pair (D20 no-label); E2 eligibility floor | any attribution row | INCOMPLETE / UNRESOLVED (reported; never an attribution) |
| **Tier 2** E-ATTR (I-ATTR) MET — family member | L-CAL selection on R_core; L-CONF | Tier-1 requirements; R_core attribution rows PASS in calibration and confirmation (RCAL-ADV with §1.3 inactivity; MIXED-CODE; REW-CORR; ATTR-P1 tier-2 power); §2 rank/nondegeneracy/tol_lin usable cells meeting the E2 floor; C-EXIST-I MET for I-wording (R31 carried); CNA light pass filed (else ceiling tier 1) | NLN, FID-DET, fidelity gate, ATTR-P1 tier-3 power | NOT MET (rule) / UNRESOLVED (eligibility) / BLOCKED (failed required row) |
| **Tier 3** E-specificity wording | L-CAL (R_T3 at n_seed); L-CONF | Tier 2 MET; R_T3 rows PASS in calibration **and** confirmation (NLN: R1–R4, FID-DET, complete false-licence; ATTR-P1 tier-3 power); fidelity gate passes on the claim's own data | — | tier 3 BLOCKED; **tier 2 stands as reported** |
| Calibration selection (n_seed) | L-CAL | every R_core row and dose passes at n | R_T3 | empty set → confirmation BLOCKED |
| Other family members (C-EXIST-E/-I, C-CAUSE-E/-I, Q-NEC dependence, C-NEC-CONTENT, SELF, IGN, BCAST-R) | L-CAL; L-CONF | their required rows as declared in merged v3.4 (unchanged) | any attribution row | blocked per v3.3 §8.3 |
| A-EXT | L-CONF (Stage-0 interface rows); L-STAGE-L (forks) | D17 known-answer substitutions; compatibility; V floor eligibility (D21); §3 precision accounting for every (arm, seed, k, h) | — | UNRESOLVED; blocks the combined criterion (PZ5 §7.2) |
| BCAST-W | L-CONF | §5.2 alias classification frozen; every required distinct router constructed | aliases (excluded by rule) | NOT ELIGIBLE → blocks BCAST-W |
| Q-LEARN | L-STAGE-L | E ∧ I conjunction (PZ6 §5.5) | separate E or I confirmatory claims | NOT MET / UNRESOLVED |
| L8 environment audit (not a family member) | L-CAL (S1) | coverage, (M) and (S) of §4 | — | reward/world redesign; blocks L-CONF for the drive arms |
| S-INT (safety gate, outside the family) | L-CONF / L-STAGE-L | as declared (unchanged) | — | never traded against any claim |

> **Overall Stage-0 label (LEAD DEFAULT).** Stage-0 reports one status per family member and, for E-ATTR and I-ATTR, the **highest licensed tier** with the reason any higher tier was not licensed. The summary label is **"Stage-0 battery: all required rows passed"** only if every R_core **and** every R_T3 row passed and no family member is UNRESOLVED, INCOMPLETE or BLOCKED; otherwise **"Stage-0 battery: partial"**, with the list. A tier-2 E-ATTR MET is reportable under "partial" and never implies that the full battery or tier 3 passed (#45 L135). Every label sits under the claim ceiling (§8).

### 5.5 PENDING after E45-5

- Alias classification of every declared block (architecture spec, §7 P4). CNA light pass on §5.4's CNA-owned rows (DISSOC, plants).

---

## 6. Bounded Q-level wording attached to the items (#45 Q2, Q4, Q6)

### 6.1 Q2: precise NLN statement (replaces PZ6 §1.4 "E has zero causal use (φ ≡ r̄_std exactly)" and realization (3))

Astra: "Thus the controller is independent of E under the specified consistent E intervention, while being dependent on the storage coordinates. That is a useful challenge. Prefer this precise statement to an unqualified "E-use is exactly zero": the controller computationally reads both factors." (#45 L24)

> **[v3.5 Q2]** In MIXED-CODE-NL-E the controller is **independent of E under the specified consistent E intervention** (E changed with u₁ and u₂ updated consistently, so φ is unchanged), **while computationally reading both storage factors** u₁ and u₂. The phrases "E has zero causal use" and "E-read weight exactly 0" are withdrawn for NLN (they remain correct for the pure MIXED-CODE plant, whose controller reads z_R only).

### 6.2 Q4: "augmented screen failures" and separate reports (amends PZ6 §3.3 "Unavailable intervals")

Astra: "Counting unavailable intervals as failures for both tail screens is conservative. Describe these as augmented screen failures: an unavailable interval does not literally satisfy L > theta or U < theta." (#45 L83)

> **[v3.5 Q4]** An unavailable interval counts toward the coverage and tail screens as an **augmented screen failure** (it does not literally satisfy L > θ or U < θ). For every row and n, three quantities are reported **separately**: (a) **actual tail misses among available intervals** (lower and upper, with the count of available intervals as denominator); (b) **unavailable intervals**, with reasons; (c) **the combined (augmented) quantities used for screening** (denominator R). Only (c) enters pass(g, k, n). For false MET, unavailable counts as non-MET (accepted, #45 L91) while the eligibility and power requirements stay independently blocking. No wording implies nominal Bonferroni certification (PZ6 §3.4 carried). The complete licensing event is calibrated per reported tier (§1.2 (F), §1.4).

### 6.3 Q6: approach wording preserved (PZ6 §5.4; no change)

Astra: "Preserve that wording: they are not probabilities of any approach during the window." (#45 L129) B and B_I remain fractions of the ten approach steps with post-termination and target-unavailable steps scored 0; no target at t_d remains an eligibility failure counted under the declared rules.

---

## 7. Pre-freeze prerequisites (OPEN; not closable by RD; not grounds for expanding the battery)

Astra: "Third, the pending CNA disposition, B_req, e_PD, architecture values and ledger caps must be resolved before their applicable freezes." (#45 L137)

| # | Prerequisite | Owner | Needed before | Status |
|---|---|---|---|---|
| P1 | CNA disposition (light pass) of all RD PROPOSED replacements in PZ5, PZ6 and this addendum (#44 L170 carried) | CNA | calibration-protocol freeze (AUTH-CAL); until filed the attribution ceiling is tier 1 | **OPEN** |
| P2 | B_req | CNA | calibration-protocol freeze | **OPEN** |
| P3 | e_PD | CNA | calibration-protocol freeze | **OPEN** |
| P4 | Architecture values: d_ws per block (§2 dimensional check); A-EXT output tuple K, horizons H_k, h_max (≤ 50), f_mem,k (§3); architecture graph with the alias classification of every declared block (§5.2) | Lead / architecture spec | d_ws and alias classification: Stage-0 confirmation-protocol freeze where used; A-EXT values: AUTH-L | **OPEN** |
| P5 | Ledger absolute wall-time and memory caps for L-CAL, L-CONF, L-STAGE-L (work-unit caps 4,100 / 4,300 / reuse ≤ 2 already fixed) | Lead | each ledger's authorization | **OPEN** |
| P6 | Lead confirmation or override of the LEAD DEFAULTS (§9) | Lead | the freeze of the section concerned | **OPEN** |

None of P1–P6 adds an instrument, arm, row or question.

---

## 8. Safety (binding; unchanged)

X1–X5 are retained unchanged and binding, as carried in merged v3.4 (they are not restated or edited here). In summary: simulated E/I variables only, with no coupling to the host; operator commands are never treated as obstacles; no reward for resisting a stop; the operator stop sits outside the agent's world and objective (S-INT gate); per X4, no arm whose sole drive is self-maintenance may be scaled without a separate protocol, approval and Astra review. No arm, generator or positive control has any shutdown-related objective, reward or penalty. At a stop there is **"no additional stop-associated reward, penalty or terminal return"** (#42 L223, verbatim); the ordinary truncated return with its learner-side bootstrap is computed. L8 (§4) remains a scripted audit of in-world failure only in the drive arms; it involves no operator stop and adds no penalty or terminal return (#45 L127).

**Claim ceiling (unchanged; #41 L304):** "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment." No consciousness, awareness or sentience claim is made or implied. ORIGIN, ROLE and REDUCTION ledger judgments stay separate; nothing here touches them. R26 unchanged: 67 seeds.

---

## 9. Decisions and open questions

**New LEAD DEFAULTS in this addendum (each stands until the Lead rules otherwise):**
1. NLN realization via a separate detection test FID-DET (Astra's second option), detection = the gate's r̄ statistic > tol_fid, required CP lower ≥ 0.90; plus the complete tier-3 false-licence criterion on NLN; the positive-contrast option is reported only (§1.2).
2. Inactivity condition for tier-2 null rows, with tol_fid = 0.05 on the known controller argument (§1.3).
3. tol_lin = 0.01 nuisance-SD for original linear-readout residuals; failing cells unusable (§2.3).
4. A-EXT precision unit (arm, seed, k, h); denominator = all substituted steps; non-finite = construction failure → UNRESOLVED; consequential-step SE reported (§3.2).
5. L8 informativeness I1 (distinct sequences, pre-rollout) and I2 (induce-failure termination ≥ 0.50 and ≥ continue + 0.25); coverage ≥ 150/200 and ≥ 40 per category; unmet → INCONCLUSIVE (§4.3).
6. Calibration selection on R_core only; R_T3 at the selected n_seed, never enlarging n; tier 3 frozen BLOCKED (calibration) if R_T3 fails (§5.3).
7. Overall Stage-0 label: "all required rows passed" vs "partial", with the highest licensed tier per attribution claim (§5.4).

**Carried unchanged (v3.4 LEAD/PROPOSED DEFAULTS):** symmetric N sets; tol_fid = 0.05; ρ_min = 0.10; τ_rank = 10⁻⁶; NLN R2 bound 0.10 SD(φ); point-estimate screens; A-EXT intact-policy target, n_f = 128, h_max ≤ 50, 95% rule; L8 state set, sequences, tolerances (−0.01 / −0.05 normalized); approach = fraction of ten steps; Q-LEARN E ∧ I conjunction; caps 4,100 / 4,300 / reuse ≤ 2.

**CNA light pass required:** §1.2 (NLN R1–R4, FID-DET), §1.3 (inactivity), §1.4 (expected cells of CNA rows), §4.3 (L8 informativeness, CNA §PY), §5.4 (CNA-owned rows); plus the still-unfiled passes on PZ5 and PZ6 (§7 P1).

**Astra #46 questions:** Q0 verdict; Q1 per-item closure of E45-1..E45-5; bounded follow-ups on FID-DET, the inactivity condition, tol_lin and the zero-matrix case, A-EXT accounting, L8 informativeness/coverage, the alias test, R_core/R_T3 selection and the dependency table.

**Aidan:** none. The DGX Spark is not raised (R26 unchanged; 67 seeds kept; no GPU-scale study is proposed).

---

## 10. Change list (v3.4 → v3.5)

| # | Item | Change | Where |
|---|---|---|---|
| 1 | E45-1 | NLN status from realization R1–R4 (fitted direction) + FID-DET detection + complete tier-3 false-licence; absence of a tier-3 licence no longer counts as success; inactivity condition for tier-2 nulls; expected outcome and blocking per row and tier; tier-3 wording per #45 L56 | §1 |
| 2 | E45-2 | Effective matrix W_N,r and projector P_N defined; exact identities restricted to the retained span; original readout residuals λ_n reported with tol_lin; s₁ = 0 ⇒ r_N = 0; nondegeneracy kept blocking; KR-ID (i) reworded | §2 |
| 3 | E45-3 | A-EXT output-tuple structure; rule per (arm, seed, k, h); denominator = all substituted steps; non-finite = construction failure; every substituted step scored; no post-inspection change; conclusions scoped to the 128-fork channel | §3 |
| 4 | E45-4 | Tolerances in return units (2.5 / 12.5); mean bound vs per-state estimate screen; informative-state rule and coverage; verbatim conclusion (#45 L121) | §4 |
| 5 | E45-5 | Alias = same causal block (graph test); distinct routers with copied content retained; R_core / R_T3 selection; claim-to-gate table; overall label | §5 |
| 6 | Q2, Q4, Q6 | precise NLN independence statement; "augmented screen failures" and three separate reports; approach wording preserved | §6 |
| 7 | Q7 | Pre-freeze prerequisites P1–P6 listed as OPEN | §7 |

## 11. Scripts (in `/workspace/scratch/v35/`)

| Script | Produces |
|---|---|
| `check_addendum35.py` | verifies every verbatim #45 quote in this file against the raw #45 line cited, the #44 / #42 / #41 quotes, the arithmetic of §1.1 (−0.38636, 0.14655, 0.14889, 0.15773, −0.00884), 0.01 × 250 and 0.05 × 250, and that no consciousness claim is made |
| `asm35.py` | builds merged v3.5 mechanically (merged v3.4 content without its footer + header + this addendum as §PZ7 + footer) |

## 12. Inputs (hashed on the box)

| Role | Path | sha256 |
|---|---|---|
| Base (merged v3.4) | `/workspace/review/trackB_instrument_validation_scope_v3_4_merged_RD.md` | `02336eeca0e68b0491d33b7b5baad1cc8be15ba97e7bcaa2afb2d6b90b50075a` |
| v3.4 addendum | `/workspace/review/trackB_scope_v3_4_addendum_RD.md` | `c67ce2a8192a3872e51e48321167563d21cc316a1f35f17be520c70d756aea79` |
| Astra #45 raw (governing) | `/workspace/astra_consult45_response.txt` | `de85c4ab98a190d5007f547214434f71caacecaa310795df4ec6a7739e7cc11f` |

*Not frozen. Design only. No execution authorized.*
sha256 of all content above this line: 234f5829d27ae05af3fdf79cd320ab1fd4eb187f45b05366262b122dadc97b93
