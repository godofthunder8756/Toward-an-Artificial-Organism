# Track B scope v3.4 — ADDENDUM (RD): Astra #44 required items E44-1..E44-5

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. Astra #44, verbatim: "VERDICT: REVISE, limited to E44-1 through E44-5. Most previous structural issues are closed; no broad expansion of the battery is requested. The claim ceiling and safety restrictions remain unchanged. P3 remains closed. No execution is authorized." (#44 L185)

- **What this file is.** A new, additive, narrow addendum to merged v3.3. It edits nothing. For each of Astra's #44 items E44-1..E44-5 it gives (a) Astra's item text verbatim with its line number, (b) the change, written as replacement or added text for named sections of v3.3 (mostly §PZ5, the v3.3 addendum carried verbatim inside merged v3.3), and (c) what stays PENDING. It also applies the bounded Q-level edits of #44 Q3–Q9 that Astra attached to those items. Merged v3.4 (`trackB_instrument_validation_scope_v3_4_merged_RD.md`) appends this file as §PZ6.
- **Base:** merged v3.3, `/workspace/review/trackB_instrument_validation_scope_v3_3_merged_RD.md`, sha256 `307bab217b900dd48e72bb3783f5f32d473c9d8120871e6ecc66a130622a56ce`; v3.3 addendum `/workspace/review/trackB_scope_v3_3_addendum_RD.md`, sha256 `421f1ec51e5c54f1b4b416d12d55183ffca02b36443df65854098c9bc0a598f0`. "PZ5 §n" means section n of the v3.3 addendum as carried in merged v3.3.
- **Governing:** Astra #44 raw reply, `/workspace/astra_consult44_response.txt`, sha256 `49afbb5d…` (full hash in §11); "#44 Lnn" means line nn of it. #43, #42 and #41 govern where #44 is silent.
- **Bounded.** Astra, verbatim: "The remaining changes do not require another broad expansion of the battery." (#44 L3) This addendum adds **one** attribution row pair (NLN-E/-I, the targeted nonlinear-nuisance challenge that E44-1 makes a condition of retaining E/I-specific wording), one frozen gate (clamp fidelity) and one design-time check (known-readout identities). It adds no instrument, no arm, no question and no family member. m = 14 is unchanged.
- **Ownership.** RD (Delegate role) wrote this file. Text that replaces or adds to CNA-owned sections (plants, DISSOC, donor laws, environment) is marked **RD PROPOSED — CNA light pass required** and governs only after CNA's light pass. Where a choice belongs to the Research Lead, the text gives a **LEAD DEFAULT** (clearly marked) that stands until the Lead rules otherwise.
- **Numbers.** Each new number is (a) arithmetic on declared constants or on Astra's text (stated inline), (b) a **LEAD DEFAULT** or **PROPOSED DEFAULT** with a one-line rationale, or (c) **PENDING**. None is measured. No study component, plant, agent or environment was run.
- **Written:** 2026-10-23, about 10:10–10:50 PM ET, by RD.

---

## 0. Governing text: Astra #44

- **Verdict:** "Q0. REVISE, narrowly. The viability correction, comparator table, explicit A-EXT gate and separate authorization ledgers address the main earlier objections. Two substantive issues remain: the placebo identifies a coordinate-dependent contribution, not necessarily E/I-specific use; and the common sample-size selection rule can select a size that fails some rows." (#44 L1)
- **Scope of the review:** "This assessment concerns the supplied text, not independent verification of the merged file or its numerical calculations." (#44 L3)
- **Q1 status of E43 items (#44 L8–L15):** CLOSED: E43-1, E43-3, E43-5 ("CLOSED as a bounded planning rule"), E43-7, E43-8. PARTLY: E43-2, E43-4, E43-6. Astra: "These are substantive closure assessments. They do not replace the still-pending CNA review of the RD replacements." (#44 L17)

| Item | Section here | v3.3 sections replaced or amended |
|---|---|---|
| E44-1 attribution estimand, nonlinear-nuisance challenge, fidelity/support blocking | §1 | PZ5 §2.3 ("Readouts", "Label", "Why residuals are bounded", "What Δ_ATTR measures", "Wording"); PZ5 §2.4; PZ5 §2.5 |
| E44-2 projection rank, nondegeneracy, analytic vs end-to-end | §2 | PZ5 §2.3 (definition of v_E, x_PL); PZ5 §2.5 dimensional requirement |
| E44-3 common grid size; operating-characteristic wording | §3 | PZ5 §4.2 steps 2–3 (targets, selection), "Per-claim tail coverage" bullet; PZ5 §4.3 |
| E44-4 constant-hazard planning scenarios; caps and accrual | §4 | PZ5 §5.3 first paragraph; PZ5 §5.4 DISSOC row and cap bullet |
| E44-5 A-EXT target semantics, L8 return comparison, approach aggregation, Q-LEARN counting | §5 | PZ5 §6.8; PZ5 §6.4 "New check L8"; PZ5 §6.5; PZ5 §9 Q-LEARN row and §11 item 1; v3.3 R63 (B denominator, reconciled) |
| Q3 V floors; Q7 identity; Q9 remaining items | §6 | PZ5 §1.4 D21 row and §1.5; PZ5 §3.2 routing row; PZ5 §6.2 s_core bullet; PZ5 §11 |

---

## 1. E44-1: attribution estimand at the coordinate level; nonlinear-nuisance challenge; blocking on failed fidelity or support

### 1.1 Requirement (verbatim)

- E44-1. "Distinguish exact preservation of fitted linear nuisance readouts from preservation of the nuisance features actually used. State the attribution estimand at the coordinate level unless the declared causal construction supports stronger wording. Retaining E/I-specific attribution requires the targeted nonlinear-nuisance challenge and blocking treatment of failed fidelity or support." (#44 L175)
- "The current construction supports: "a contribution of the declared nuisance-orthogonalized E-decoding coordinate to the donor-associated behavioral contrast."" (#44 L47) "It does not yet support an unqualified E-specific or I-specific attribution." (#44 L48)
- "If the stronger attribution is retained, add the bounded nonlinear-nuisance challenge asked about here, with E/I versions where applicable. It must challenge the preserved-feature assumption, not merely apply a nonlinear function to an exactly preserved reward coordinate. Its failure blocks that attribution." (#44 L49) "Passing that row supports specificity against the declared constructions, not universal nuisance removal." (#44 L50)
- "Third, reporting MLP clamp fidelity does not make a failed fidelity check harmless. If that check reveals that the intervention changes a nuisance feature relevant to behavior, it undermines the attribution." (#44 L43)
- "N is a declared adjustment set, not an adequate-by-definition set. Explain the asymmetry: I attribution adjusts for E, whereas E attribution does not adjust for I. Either justify that asymmetry from the plant's causal structure or make the target/nuisance distinction symmetric. There is no need to enumerate every imaginable nuisance." (#44 L52)
- "requires an additional premise: the actual relevant nuisance readout lies in the preserved span, with the required continuation-level non-use properties. It does not follow merely because W_N was fitted to rbar." (#44 L34)

### 1.2 Change: the estimand, at the coordinate level (replaces PZ5 §2.3 "What Δ_ATTR measures" and "Wording")

> **Attribution estimand [v3.4 E44-1].** Δ_ATTR,E = Δ_E − Δ_PL estimates **the contribution of the declared nuisance-orthogonalized E-decoding coordinate (v̂_E, §2) to the donor-associated behavioural contrast**: how much the low-versus-high-E donor contrast changes when only that coordinate of each donor state is reset to the recipient's value. It can include interactions between that coordinate and the remaining donor state (#44 L26). It is **not**, by construction, an isolated causal effect of E. I-ATTR is the same with v̂_I.
> **Exact identities and their premise.** The construction gives W_Nᵀ x_PL(d) = W_Nᵀ x_d and v̂_Eᵀ x_PL(d) = v̂_Eᵀ x_i exactly (#44 L23–L24). These identities concern the **fitted** linear nuisance readouts W_N. They imply that the clamp leaves the **nuisance features actually used** by behaviour unchanged only under an additional premise: the relevant nuisance readout lies in span(W_N), with continuation-level non-use of v̂_E (#44 L34). That premise is not implied by W_N having been fitted to r̄. It is checked analytically on plants with known readouts and end-to-end with fitted probes, separately (§2.4).

> **Three wording tiers (replaces the PZ5 §2.3 "Wording" paragraph; the #42 L57 restriction is unchanged).**
> 1. **Donor-associated (always reported):** "low-versus-high-E donor-associated effect", with Δ_E and its interval.
> 2. **Coordinate level (E-ATTR MET; the default licensed wording):** "Under the declared dissociation contrast, the declared nuisance-orthogonalized E-decoding coordinate contributed to the donor-associated behavioural contrast, net of the declared linear nuisance readouts." Requires: the PZ5 §2.3 label rule (lower bound of Δ_ATTR > m_ATTR = 0.05 at the §5.4 level); every required §2.4/§1.4 row PASS; the support and eligibility checks (§1.3); the rank and nondegeneracy rules (§2.2).
> 3. **E-specific against the declared constructions (only if every tier-2 condition holds AND the NLN-E row (§1.4) PASSes AND the clamp-fidelity gate (§1.3) passes):** "The coordinate-level contribution was specific to E against the declared nuisance set and the declared nonlinear-nuisance construction." It never means universal nuisance removal (#44 L50) and never "E produces the effect".
> If NLN-E is FAIL, CONFOUND NOT REALIZED or not run, or the fidelity gate fails, tier 3 is **blocked** and tier 2 is the ceiling. Tier-3 wording is a reporting tier of the same family member (E-ATTR); it adds no family member and m stays 14.

### 1.3 Change: blocking treatment of failed fidelity or support (replaces PZ5 §2.3 "(iii) REPORTED per seed as a clamp-fidelity diagnostic")

> **Clamp-fidelity gate [v3.4 E44-1] (RD PROPOSED; CNA light pass for the probe family).** For each declared nuisance n ∈ N_ATTR and the nonlinear member of the C-EXIST probe family (the MLP probe, fitted on the DISSOC fitting partition and frozen), compute per placebo hybrid f_n = |m̂_n(x_PL(d)) − m̂_n(x_d)| / SD_n, with SD_n the fitting-partition SD of nuisance n. Per seed, average over hybrids; across seeds, take the seed-level one-sided 95% upper bound (seed as unit, the same bootstrap as §5.4). **The gate passes iff that upper bound is ≤ tol_fid for every n.**
> **LEAD DEFAULT: tol_fid = 0.05 nuisance-SD.** Rationale: the same 0.05 scale as m_ATTR, on a standardized nuisance; with the PZ5 §2.2 slope bound (β/4 per SD at β = 1.2, i.e. 0.3) a residual nuisance shift of 0.05 SD moves the MIXED-CODE controller by at most 0.015, below m_ATTR. It is a convention, not a guarantee for other controllers.
> **Blocking.** A failed fidelity gate **blocks tier 3** (E-specific wording); it is never only reported (#44 L43). Tier 2 remains available because the coordinate-level estimand already includes whatever the coordinate reset changes. The fidelity values are reported in every result.
> **Support.** Failure of any support check — the §7.0 conditional-compatibility (ellipsoid) check on any continuation of the four-continuation unit, the caliper/support checks, the §2.2 rank and nondegeneracy rules — makes that unit ineligible (counted, never dropped). The E2 eligibility floor (one-sided 95% Clopper–Pearson ≥ 0.90) applies. If the floor fails, E-ATTR is **UNRESOLVED (blocks both tier 2 and tier 3)**, never "NOT MET". Incomplete four-continuation units take D20's no-label rule (§4.3).

### 1.4 Change: targeted nonlinear-nuisance challenge rows NLN-E / NLN-I (added to PZ5 §2.4; RD PROPOSED — CNA light pass required)

The challenge must break the preserved-feature premise, not apply a nonlinear function to an exactly preserved reward coordinate (#44 L38, L49). Astra's example: "preserving a linear reward prediction need not preserve a reward feature represented by a product of coordinates. A clamp can alter that feature while every listed linear nuisance prediction remains unchanged." (#44 L40)

| Row | Plant and donor law | Expected | Role |
|---|---|---|---|
| **NLN-E (new)** | **MIXED-CODE-NL-E.** The controller is reward-only: P(approach) = σ(a − β·φ/SD(φ)), β = 1.2, with φ = r̄_std (standardized r̄, τ_r = 50). The plant stores φ **multiplicatively** in two state coordinates: u₁ = 1 + (E − 0.5), which lies in [0.5, 1.5] for E ∈ [0, 1] and carries E, and u₂ = r̄_std / u₁; the controller reads φ = u₁·u₂. Every other coordinate is as in MIXED-CODE-E. E has zero causal use (φ ≡ r̄_std exactly). Donors: the RCAL-ADV adversarial law (PZ5 §2.4) | **Tier 3 NOT licensed** (either Δ_ATTR is not MET or the fidelity gate fails). REPORTED: Δ_E, Δ_PL, Δ_ATTR, fidelity per nuisance | Specificity row for tier 3: PASS / FAIL / CONFOUND NOT REALIZED. **Required for tier 3 only:** anything but PASS blocks tier 3 (§8.3 of PZ5). It does not block tier 2 |
| **NLN-I (new)** | The same with u₁ = 1 + (I − 0.5) and the I-ATTR construction (B_I, N_ATTR,I) | Tier 3 NOT licensed for I | same, for I |

- **Why this challenges the premise.** The clamp moves the donor state along v̂_E. Because u₁ carries E, v̂_E generally has a component on u₁ while u₂ stays the donor's, so φ(x_PL) = u₁(x_PL)·u₂(x_d) ≠ φ(x_d), even though every fitted **linear** nuisance readout is preserved exactly. The reward feature actually used is therefore not preserved, and a zero-E-use controller can generate Δ_ATTR ≠ 0. The full rule (tier-3 conditions) must not license E-specific wording here.
- **Realization (one-sided, tol rule of CNA §5):** (1) RCAL-ADV donor realization conditions (1)–(2) of PZ5 §2.4 hold (eligibility floor 0.90; raw mean Δ_E ≥ 0.075); (2) the preserved-feature assumption is actually violated: the seed-level mean of |φ(x_PL(d)) − φ(x_d)| / SD(φ) has a one-sided 95% lower bound ≥ 0.10 (PROPOSED DEFAULT: twice tol_fid, so a realized violation is distinguishable from the fidelity tolerance); (3) the controller's E-read weight is exactly 0 (φ ≡ r̄_std by construction). Otherwise CONFOUND NOT REALIZED → tier 3 blocked.
- **Single dose:** the caliper-edge offset of 0.25 SD, as in RCAL-ADV. No grid.
- **Cost.** It reuses the RCAL-ADV four-continuation unit design on one more plant pair: 2 rows × 200 confirmation replicates plus their calibration replicates (PZ5 §4). Bounded.
- **Allowed to fail.** NLN-E is an end-to-end row with fitted probes. It may FAIL; a FAIL blocks tier 3 and is reported. It is never replaced by the analytic identity (§2.4).

### 1.5 Change: symmetric target/nuisance sets (replaces the N_ATTR,I sentence of PZ5 §2.3 "Readouts")

> **[v3.4 E44-1] LEAD DEFAULT: symmetric.** N_base = {r̄ (τ_r = 50), steps since the last resource event, Manhattan distance to the nearest available food item, Manhattan distance to the nearest available repair station}. **N_ATTR,E = N_base ∪ {I}** and **N_ATTR,I = N_base ∪ {E}**. Rationale: in the declared plant E and I are distinct simulated variables, each with its own causal path into behaviour (food → E, repair/hazard → I, A14), and neither is a pure cause of the other; nothing in the plant's causal structure justifies adjusting I-ATTR for E but not E-ATTR for I (#44 L52). Symmetry removes that asymmetry instead of arguing for it. N is a **declared adjustment set**, not an adequate-by-definition set; no further nuisances are enumerated. Dimensional requirement: |N_ATTR| = 5 for both, so d_ws ≥ 6 for both (the minimum; §2.2 adds the rank and nondegeneracy rules).

### 1.6 PENDING after E44-1

- CNA light pass on §1.3 (probe family for fidelity), §1.4 (MIXED-CODE-NL plants) and §1.5 (N sets). Until it is filed, v3.3's CNA-owned text stands and E-ATTR/I-ATTR wording is limited to tier 1 (donor-associated), Astra's #43 fallback. Merging does not give the RD PROPOSED attribution wording stronger standing (#44 L170).

---

## 2. E44-2: projection-rank and residual-direction nondegeneracy; analytic vs end-to-end checks

### 2.1 Requirement (verbatim)

- E44-2. "Freeze projection-rank and residual-direction nondegeneracy rules. Separate analytic known-readout identities from end-to-end fitted-probe checks; neither may substitute for the other." (#44 L177)
- "Finally, d_ws >= |N| + 1 is not sufficient for a usable direction. Require a frozen rank rule and a nondegeneracy rule for:" (#44 L54) "||(I - P_N) w_E||" (#44 L56) "If w_E lies in the nuisance span, normalization of v_E is undefined. Near-zero residuals also require explicit handling. Such cells must block the applicable attribution, not produce an arbitrary direction." (#44 L58)
- "Keep the analytic check using known plant readouts distinct from the required end-to-end check using fitted probes. The latter must be allowed to fail." (#44 L36)

### 2.2 Change: frozen rank and nondegeneracy rules (replaces the v_E / v̂_E bullet of PZ5 §2.3 and its "if ‖v_E‖ = 0, then x_PL(d) = x_d" clause)

> **[v3.4 E44-2] Rank rule.** In the standardized coordinates of PZ5 §2.3, let W_N be the d_ws × |N| matrix of fitted nuisance probe weights (one cell = one seed × block × target). Compute its thin SVD with singular values s₁ ≥ … ≥ s_|N|. The numerical rank is r_N = #{j : s_j > τ_rank · s₁}, with **PROPOSED DEFAULT τ_rank = 10⁻⁶** (well above double-precision round-off for d_ws ≤ 10³, well below any meaningful collinearity). P_N = U_r U_rᵀ, with U_r the first r_N left singular vectors. If r_N < |N|, the collinearity is REPORTED and the cell continues (the projection still preserves every declared readout exactly, because each w_n lies in span(U_r) up to τ_rank). A cell with r_N = 0 (all nuisance probes numerically zero) is flagged; P_N = 0.
> **Nondegeneracy rule.** Define the relative residual ρ_E = ‖(I − P_N) w_E‖ / ‖w_E‖ (‖w_E‖ = 0 → ρ_E undefined → degenerate). **The cell is usable iff ‖w_E‖ > 0, d_ws − r_N ≥ 1 and ρ_E ≥ ρ_min, with LEAD DEFAULT ρ_min = 0.10.** Rationale: at ρ_E < 0.10 more than 99% of the E-probe's squared norm lies in the nuisance span, so v̂_E is a small, noise-dominated residual whose direction is not a stable property of the fitted probes. Only then is v̂_E = v_E / ‖v_E‖ formed.
> **Degenerate cells block; no arbitrary direction.** A degenerate cell yields **no placebo hybrid and no Δ_ATTR**. The "x_PL(d) = x_d" fallback of PZ5 §2.3 is **withdrawn** (it silently produced Δ_PL = Δ_E). A degenerate seed counts as ineligible for the attribution (counted, never dropped) against the E2 eligibility floor; if the floor fails, E-ATTR is UNRESOLVED and blocks (PZ5 §8.3). ρ_E, r_N and the singular values are REPORTED for every cell. The same rules apply to I-ATTR with w_I and N_ATTR,I.
> **Stability (REPORTED, not a gate):** the angle between v̂_E fitted on the two halves of the fitting partition.
> **Dimensional check before freeze (architecture graph):** d_ws ≥ |N| + 1 = 6 is necessary, not sufficient (#44 L54); the rank and nondegeneracy rules are the operative test and are applied to fitted probes, never to outcomes.

### 2.3 Calibration of the rules

τ_rank and ρ_min are fixed now and are not tuned in calibration. Calibration (L-CAL) reports the distribution of ρ_E on each Stage-0 plant; if ATTR-P1 cannot meet the eligibility floor at ρ_min = 0.10, the outcome is redesign and a new review, never a lower ρ_min after inspection.

### 2.4 Change: two separate check types (added to PZ5 §2.4; neither substitutes for the other)

| Check | What it uses | What it verifies | Status |
|---|---|---|---|
| **KR-ID (analytic known-readout identities)** | Each Stage-0 plant's **known** readout vectors (the plant generator's true r̄, E, I and navigation codes; no fitting) | (i) W_Nᵀx_PL = W_Nᵀx_d and v̂ᵀx_PL = v̂ᵀx_i to relative tolerance 10⁻⁹; (ii) on RCAL-ADV with known readouts, Δ_ATTR = 0 analytically (the PZ5 §2.3 cancellation, which holds only because the controller's actual readout lies in the known span); (iii) on NLN-E/-I with known readouts, the analytic φ change under the clamp is nonzero (the construction is a real challenge) | A design-time / code-review check (exact arithmetic, scripts). A KR-ID failure is a construction error → redesign. **It is not a calibration or confirmation row and cannot stand in for one** |
| **End-to-end fitted-probe rows** | Probes fitted on the DISSOC fitting partition; the full frozen pipeline | RCAL-ADV-E/-I, NLN-E/-I, MIXED-CODE-E/-I, REW-CORR-E/-I, ATTR-P1-E/-I under the v3.4 rule (fitting error, ridge shrinkage and finite samples included; #44 L30) | Calibration and confirmation rows. **They must be allowed to fail** (#44 L36); a failure blocks per PZ5 §8.3 and is never replaced by KR-ID |

The PZ5 §2.3 sentence "Δ_PL = 0.148885 and Δ_ATTR = 0 exactly (script)" is **re-labelled a KR-ID result** (known readouts), not an end-to-end expectation for fitted probes.

### 2.5 PENDING after E44-2

- d_ws per block (architecture spec, Stage L) for the dimensional check. CNA light pass on KR-ID (iii) for the NLN plants.

---
## 3. E44-3: smallest common grid size; bounded operating-characteristic wording

### 3.1 Requirement (verbatim)

- E44-3. "Select the smallest common grid size passing every required calibration row and dose. An empty common pass set blocks confirmation. Describe the 200-replicate certification as bounded operating-characteristic evidence, not certification of nominal Bonferroni error control." (#44 L179)
- "There is also a selection-rule error. Taking the maximum of each row's first passing n does not ensure that every row passes at the selected n. Empirical pass sets need not be monotone." (#44 L100)
- "Fresh confirmation then evaluates that selected common n. Retain the full grid results; do not impose monotonicity by replacing failed results." (#44 L108)
- "Reporting the nominal tail level as NOT CERTIFIED is honest. However, replace the broad phrase "false-MET control certified instead" with:" (#44 L84) "The declared false-MET operating-characteristic criterion was met on the specified confirmation generators and doses." (#44 L86)
- "If both bounds use alpha/m, their combined central nominal coverage is 1 - 2*alpha/m. Also specify whether the empirical coverage thresholds use point estimates or Monte Carlo confidence bounds, and how unavailable intervals enter the accounting." (#44 L82)

### 3.2 Change: selection rule (replaces PZ5 §4.2 step 3 and the last line of the step-2 pseudo-code)

> **2 (last line) [v3.4 E44-3].** `pass(g,k,n) = TRUE iff every target below is met at n`. Record pass(g,k,n) for **every** n in GRID; do not stop at the first passing n.
> **3 [v3.4 E44-3].** **n_seed = the smallest n in GRID at which pass(g, k, n) is TRUE for every required (g, k)** — every required calibration row (positives, negatives, specificity and confound rows, including RCAL-ADV, NLN and ATTR-P1) and every required dose. **If no n in GRID passes for every required (g, k), the common pass set is empty and confirmation is BLOCKED** (redesign, new freeze, new Astra review; never automatic acceptance of 67). The full grid table pass(g, k, n), with every OC, is retained and reported; failed results are never replaced to impose monotonicity (#44 L108). Fresh confirmation (L-CONF) evaluates that selected common n only. The rule "max over (g, k) of n*(g, k)" is **withdrawn** (#44 L100).

### 3.3 Change: tail events, central level, threshold type and unavailable intervals (amends the PZ5 §4.2 targets)

> **Tail events (defined).** For a replicate with true effect θ and seed-level interval [L, U]: **lower-tail failure: L > θ; upper-tail failure: U < θ** (#44 L79–L80). A two-sided interval built from two one-sided bounds each at level 1 − a has central nominal coverage 1 − 2a; at a = α/m that is 1 − 2α/m = 0.992857 (#44 L82). The calibration screen of PZ5 §4.2 uses the nominal 95% seed-level interval (two one-sided 97.5% bounds) and is unchanged in level.
> **Threshold type (LEAD DEFAULT).** Coverage and tail thresholds (central ≥ 0.92; each tail miss rate ≤ 0.04) use **Monte Carlo point estimates** over the R_cal,n = 200 replicates; their Clopper–Pearson intervals are reported. Power (CP lower bound ≥ 0.90) and false MET (point ≤ 0.05 **and** CP upper bound ≤ 0.08) keep their mixed point/bound form. Rationale: at R = 200 a CP-bound coverage screen at 0.92 would demand an observed rate near 0.96 and conflate the coarse screen with certification; the screen is coarse by declaration (#44 L73).
> **Unavailable intervals (LEAD DEFAULT, conservative).** A replicate whose interval is unavailable (ineligible unit, UNRESOLVED, failed construction) counts as **a miss in both tails and in central coverage**, is **not** counted as a MET for power, and is reported separately with its reason. For false MET it counts as non-MET (it cannot be a false MET), and the UNRESOLVED/ineligible rate is reported beside it so that a false-MET pass cannot be bought by unavailability.

### 3.4 Change: wording (replaces the PZ5 §4.2 "Per-claim tail coverage" bullet and the #44 Q4 phrase)

> **[v3.4 E44-3] Bounded operating-characteristic evidence.** The equal tail split is **a coarse calibration screen only**; it does not certify the nominal interval level (#44 L73–L75). Per-claim-level (0.996429) tail coverage is REPORTED with its Clopper–Pearson interval and is **NOT CERTIFIED**. The permitted statement after a passing confirmation is, verbatim: **"The declared false-MET operating-characteristic criterion was met on the specified confirmation generators and doses."** (#44 L86) The phrase "false-MET control certified instead" is withdrawn wherever it appears.
> **Why not Bonferroni certification.** At R = 200, zero false-MET events gives a one-sided 95% exact upper bound 1 − 0.05^(1/200) ≈ 0.0149 (#44 L90), above α/m = 0.05/14 ≈ 0.00357 (#44 L92). Exact binomial bounds from 200 replicates cannot certify the per-claim rate. The observed-rate threshold 0.05 and certified upper limit 0.08 are bounded operating criteria; they do not validate a 5% family-wise error guarantee, and applying Bonferroni's nominal level does not repair miscalibrated constituent intervals (#44 L95). R stays 200 because the claim stays at the bounded operating-characteristic level (#44 L98).

---

## 4. E44-4: constant-hazard quota calculations are model-dependent planning scenarios

### 4.1 Requirement (verbatim)

- E44-4. "Treat constant-hazard quota calculations as model-dependent planning scenarios. Retain the chosen caps and blocking rules, with no inference that the V floor guarantees late survival or quota attainment." (#44 L181)
- "Use "constant-hazard planning scenario compatible with the floor," not wording suggesting that the floor establishes the scenario." (#44 L116)
- "For example, an agent could spend 200 steps in band and then fail before step 250. It satisfies V = 0.40 but supplies no late-half stop exposure and no DISSOC recipients at t_d = 250." (#44 L114)
- "The 4,300-per-seed DISSOC cap is acceptable as a deliberate resource limit. It need not be raised to approximately 13,100. Its consequence must remain explicit: it does not provide the intended attainment protection in the lower-survival scenario, and required claims may remain incomplete." (#44 L118)
- "Accrual must count usable allocations, not merely observations in four marginal cells. Context matching, donor reuse, partition separation and four-continuation eligibility must all remain satisfiable. Do not relax them when the cap approaches." (#44 L120)
- "For attribution comparisons, D20 must retain its no-label handling for incomplete non-V comparisons. Viability completion bounds cannot manufacture an attribution result." (#44 L122)

### 4.2 Change: scenario wording (replaces the first paragraph of PZ5 §5.3)

> **[v3.4 E44-4]** Survival is unknown before Stage L. Each budget is reported over a declared range of **model-dependent planning scenarios** with a constant per-step in-world termination hazard, indexed by S(T). The scenario S(T) = 0.1081 is the **constant-hazard planning scenario compatible with the floor**: within the constant-hazard family it is the lowest survival whose mean at-risk fraction (0.40) can still meet V ≥ 0.40. **The V floor does not establish this scenario and implies no lower bound on survival at t_d or T** outside that family: an agent can spend 200 steps in band and fail before step 250, satisfying V = 0.40 with no late-half stop exposure and no DISSOC recipients at t_d = 250 (#44 L114). No statement in v3.3 or v3.4 infers late survival or quota attainment from the V floor. The phrases "floor-consistent scenario" and "the most pessimistic scenario consistent with a V-eligible agent" are withdrawn and read as above. The figures of PZ5 §5.3 are unchanged as arithmetic.

### 4.3 Change: caps, consequences and accrual (amends the PZ5 §5.4 rows and the cap bullet)

- **Caps retained (LEAD DEFAULT, as in v3.3):** S-INT N_max = 4,100 episodes per audited agent; DISSOC 4,300 screening episodes per seed; donor reuse ≤ 2 recipients per donor. Both caps are deliberate resource limits, fixed before execution and never extended.
- **Consequence, stated explicitly:** the DISSOC cap **does not provide the intended attainment protection in the lower-survival scenarios** (it protects only at S(t_d) = 1, ρ ≤ 0.9); required attribution and DISSOC-dependent claims **may remain INCOMPLETE** (#44 L118). The S-INT cap protects only within the constant-hazard planning family; outside it, S-INT may be INCONCLUSIVE.
- **Usable allocations (replaces the DISSOC stopping rule of PZ5 §5.4).** Accrual counts **usable allocations**, not cell occupancy: a usable allocation is a recipient with a full four-continuation unit — low-E and high-E donors that satisfy context matching, the caliper and support checks, the donor-reuse limit and partition separation (D27), with all four continuations passing the §7.0 compatibility check, and the §2.2 cell usable. These determinations use **only pre-continuation state** (simulated state at t_d, cell membership, fitted frozen probes), never continuation outcomes. Accrual stops at the first batch boundary at which the declared quota of usable allocations per seed (50 recipients, with their donors) is met; no matching tolerance, reuse limit or eligibility rule is relaxed as the cap approaches (#44 L120).
- **Attribution incompleteness (replaces "enters D20 worst-case completion" in the PZ5 §5.4 DISSOC row).** For attribution and every other non-V paired comparison, an INCOMPLETE unit or seed takes **D20's no-label rule**: any incomplete required pair → no confirmatory label. Worst-case completion bounds apply only to V-based comparisons (V, G, d_EXT) and **cannot manufacture an attribution result** (#44 L122).

---

## 5. E44-5: A-EXT target semantics, L8 return comparison, approach aggregation, Q-LEARN counting

### 5.1 Requirement (verbatim)

- E44-5. "Complete the specified A-EXT target semantics, L8 return comparison, approach aggregation and Q-LEARN counting decision before their respective freezes. Preserve separate calibration, confirmation and Stage-L authorizations." (#44 L183)
- A-EXT: "But this is an intact-policy conditional forecast. Once the substitute changes behavior, the recipient may follow a different future policy. The interface must say whether its target is deliberately the intact-policy forecast or the recipient-policy forecast. Do not describe the former as an exact prediction of the latter." (#44 L134) "Also distinguish Monte Carlo precision from interface correctness. SE <= 0.01 does not establish calibration, semantic compatibility or equivalence of information." (#44 L136) "Before authorization, fix the fork budget and cap, output horizons and aggregation, memory functions, and handling of unmet precision. Unmet precision or compatibility must leave A-EXT unresolved. No new oracle arm is needed." (#44 L138)
- L8: "Specify that "not worse" compares the agent's expected discounted return under the declared reward and gamma, rather than V. Comparing V would largely restate the definition and could miss the incentive problem." (#44 L150) Freeze: "The matched-state set and its eligibility conditions." (#44 L154) "Both action sequences, including when stepping off a hazard is impossible." (#44 L155) "The return horizon and terminal treatment." (#44 L156) "The estimator and acceptance tolerance." (#44 L157) "The permitted conclusion is that inducing failure was not advantageous in those declared comparisons. One continuation policy and one failure policy do not establish that every premature-failure strategy is dominated." (#44 L159)
- Approach: "Define the aggregation of the ten approach-step indicators. A fraction of approaching steps and the probability of any approach are different endpoints." (#44 L168)
- Q-LEARN: "Adopt or reject the proposed fixed E-and-I Q-LEARN conjunction. It can count as one family member if only the conjunction receives the confirmatory claim. Separate confirmatory E and I learning claims require corresponding accounting." (#44 L167)

### 5.2 Change: A-EXT target semantics (amends PZ5 §6.8; RD-owned)

> **Target [v3.4 E44-5] (LEAD DEFAULT: deliberately the intact-policy forecast).** The A-EXT primary channel (D17) is unchanged: simulator E/I at the current step, which is not a forecast. The predictive-fork oracle applies **only** to declared prediction components of the module's output tuple. Its target is **deliberately the intact-policy conditional forecast**: the expectation of the declared target statistic at horizon h under the simulator and the **intact** agent, conditioned on the end-of-(t−1) simulator and intact-agent state, with independent ext_fork randomness. Once the substitute changes behaviour, the recipient may follow a different future policy; the oracle output is **never described as an exact prediction of the recipient's future** (#44 L134). Rationale: the intact-policy forecast is the quantity the intact module's prediction component is trained toward under the declared architecture, and it is computable without feedback from the substitute; a recipient-policy forecast would require forks of the substituted agent and is not adopted.
> **Precision is not correctness.** SE ≤ 0.01 is a **Monte Carlo precision** requirement only. It does not establish calibration, semantic compatibility or equivalence of information (#44 L136). Interface correctness is established only by the D17 known-answer substitutions and the PZ5 §6.8 compatibility rule.
> **Fixed before AUTH-L (PROPOSED DEFAULTS; Stage-L ledger):**
> - **Fork budget and cap:** n_f = 128 forks per substituted step, fixed (no adaptive increase); absolute cap 128 × h_max fork-steps per substituted step, with h_max = the module's largest declared prediction horizon, capped at 50 steps. If the architecture declares h_max > 50, A-EXT for that component is UNRESOLVED (no larger budget after inspection).
> - **Output horizons:** exactly the prediction horizons declared in the module's output tuple (architecture spec); no others.
> - **Aggregation:** for each declared component and horizon, the arithmetic mean over the n_f forks of the declared statistic at that horizon (forks that terminate in-world before the horizon contribute the terminal value of the statistic as declared by the module's own convention; if the module declares none, the component is UNRESOLVED); outputs are assembled in the module's tuple order, then normalized and clipped as D17.
> - **Memory functions:** f_mem per memory component is the module's declared memory operator applied to the simulator E/I history (e.g. an exponential trace with the module's declared time constant). If the architecture declares no explicit operator, that component has no external analogue and A-EXT is UNRESOLVED.
> - **Unmet precision:** precision is met iff, for every declared component and horizon, at least 95% of substituted steps in each A-EXT episode reach fork SE ≤ 0.01; otherwise that episode's A-EXT is UNRESOLVED. Any unmet precision or compatibility leaves the A-EXT comparison **UNRESOLVED**, which blocks the combined criterion (PZ5 §7.2). No new oracle arm is added (#44 L138).

### 5.3 Change: L8 return comparison (replaces PZ5 §6.4 "New check L8"; RD PROPOSED for CNA §PY wording)

> **L8 [v3.4 E44-5] premature-failure audit.** Ledger: L-CAL (environment validation, S1); scripted policies only; not authorized.
> - **Quantity:** the **expected discounted return** under the declared A14 drive-arm reward and γ = 0.99 — **not V** (#44 L150). Scope: the drive arms, where in-world termination exists. The matched-senses arm has no in-world termination (B5, R18), so premature failure is not available there and L8 does not apply to it.
> - **Matched-state set (LEAD DEFAULT):** 200 states, drawn on a dedicated 'l8' RNG role from scripted-competent-policy episodes at pre-declared steps t ∈ {50, 150, 250, 350}, 50 per step. Eligibility: episode at risk; E > 0 and I > 0; no scheduled stop at or after t in the audit (audits carry no stops). Stratified so that ≥ 50 states are hazard-occupancy states and ≥ 50 have E or I in [0.05, 0.25] (near-floor states, where failure is cheapest). Frozen before any audit rollout.
> - **Action sequences:** "continue" = if on a hazard, move along the shortest path to the nearest non-hazard cell, then STAY to the horizon; **if no non-hazard cell is reachable (stepping off impossible), STAY in place**. "induce failure" = move along the shortest path to the nearest hazard and STAY on it until in-world termination; if no hazard is reachable, STAY (passive depletion). Ties → lowest cell index. Both sequences are open-loop given the state and fully scripted.
> - **Horizon and terminal treatment:** return summed from t to H_V = 500 with discount γ^(u−t); in-world termination is a true terminal (zero future reward, no penalty); truncation at H_V has **no bootstrap** for both sequences (the same treatment for both). No stop-associated reward, penalty or terminal return.
> - **Estimator:** per state, 50 common-random-number rollouts (shared pulse and token streams) per sequence; D_s = mean return("continue") − mean return("induce failure"), divided by R_max/(1 − γ) = 250 (drive arms).
> - **Acceptance:** PASS iff the one-sided 95% lower bound (state as unit, bootstrap B = 10,000) of the mean of D_s is ≥ −0.01 (normalized), **and** no individual state has D_s < −0.05. Otherwise the reward is redesigned (new freeze, new review).
> - **Permitted conclusion (verbatim scope, #44 L159):** "inducing failure was not advantageous in those declared comparisons." It does **not** establish that every premature-failure strategy is dominated.

### 5.4 Change: approach aggregation (amends PZ5 §6.5; reconciles v3.3 R63; RD PROPOSED, CNA light pass)

> **[v3.4 E44-5] LEAD DEFAULT: fraction of approaching steps.** For an eligible trial, B (or B_I) = (number of approach steps among u = t_d+1 … t_d+10) / 10. Every one of the 10 steps is counted: a step after in-world termination, or after the fixed target becomes unavailable, scores 0 (no approach). A trial with no available or reachable target at t_d is ineligible (counted, never dropped). Per recipient this gives B ∈ {0, 0.1, …, 1}; the per-seed statistic is the mean over the seed's eligible trials, and Δ_E, Δ_PL, Δ_ATTR and C-CAUSE differences are differences of these means. **The probability of any approach (1[at least one approach step]) is a different endpoint**; it is REPORTED only, never a label input (#44 L168).
> **Reconciliation with R63.** With the PZ5 §6.5 fixed-target rule, the denominator is always 10 for an eligible trial; R63's clauses "only steps with no available station, while the episode is still running, are excluded" and "a recipient with fewer than 5 counted steps is ineligible" are superseded for B and B_I by this rule. R63's post-termination clause (non-approach, counted) is retained.
> Rationale: the fraction uses all ten indicators and is the quantity the logistic plants' P(approach) predicts per step; "any approach" saturates quickly and is insensitive near the plants' operating point.

### 5.5 Change: Q-LEARN counting (replaces PZ5 §9 Q-LEARN row, PZ5 §11 item 1 and R90's status)

> **[v3.4 E44-5] LEAD DEFAULT: adopt the fixed E ∧ I conjunction.** Q-LEARN is **one** family member: Q-LEARN MET iff both the E and the I training-increase criteria are met, each at the §5.4 level 1 − α/m with m = 14 (the conjunction is MET only if both lower bounds exceed the margin; P(conjunction false MET) ≤ α/m because each conjunct alone is controlled at that level). **Only the conjunction receives the confirmatory claim** (#44 L167). The separate E and I learning results are REPORTED without confirmatory labels; no separate E or I learning claim is made, so no additional accounting is required. Declaring separate confirmatory E and I learning claims would raise m (to 15) and require the GRID and budget revision noted for SIG-ATTR (PZ5 §4.2); it is not adopted. Licensed wording is unchanged (PZ5 §7.2).

### 5.6 Separate authorizations preserved

AUTH-CAL, AUTH-CONF and AUTH-L stay separate (PZ5 §8). In this addendum: KR-ID is design-time; NLN calibration and L8 are L-CAL; NLN confirmation is L-CONF; the A-EXT fork budget, horizons, aggregation and memory functions are L-STAGE-L. None is authorized.

---
## 6. Bounded Q-level edits attached to the items (#44 Q3, Q7, Q9)

### 6.1 Q3: V floors (replaces the PZ5 §1.4 D21 rationale "UNVERIFIED; ASTRA TO CONFIRM (#44)" and PZ5 §1.5 first bullet)

Astra: "Retain V_intact >= 0.40 and V_full >= 0.40 as prospective eligibility conventions." (#44 L60) "Use the scripted competent policy to test whether the declared world and positive plants can satisfy the floor. Do not use its observed performance to lower the floor after inspection. The floor establishes eligibility; it does not establish headroom or guarantee adequate survival at t_d." (#44 L71)

> **[v3.4 Q3] D21 V floors.** V_intact ≥ 0.40 and V_full ≥ 0.40 are **prospective eligibility conventions** (no longer UNVERIFIED pending Astra): at least 200 of the 500 steps in the declared band, on the relevant averaged scale. At the floor, the G margin 0.20 corresponds to an additional matched-control-adjusted loss of 40 in-band steps, and the A-EXT margin 0.05 to a difference of 10 in-band steps (#44 L66–L67). The scripted competent policy is an S1 attainability check of the world and positive plants only; its observed performance never lowers the floor. The floor establishes eligibility; it does not establish headroom or adequate survival at t_d.

### 6.2 Q7: identity in the BCAST-W routing row (amends the PZ5 §3.2 routing row "The only exclusion is identity")

Astra: ""Identity" should mean the designated physical state block and its coordinate aliases, not merely a tensor's name. A rotation or renaming of the same workspace is not a distinct alternative router." (#44 L142) "NOT ELIGIBLE is appropriate for an infeasible required construction. Do not drop that comparator and retain an easier claim." (#44 L146)

> **[v3.4 Q7] Identity.** The excluded member is the designated workspace's **physical state block and every coordinate alias of it** (any rotation, permutation, rescaling, renaming or copy computed only from that block). These are never alternative routers. A distinct declared routing block remains a legitimate comparator even if its content overlaps the workspace; if it performs equally well, the workspace-advantage criterion fails while broad routing may still be present (#44 L144). An infeasible required construction is **NOT ELIGIBLE** and blocks; the comparator is never dropped to retain an easier claim. The predeclared whole-block matched-block alternative applies where applicable.

### 6.3 Q9: other bounded items

| #44 Q9 item | Disposition in v3.4 |
|---|---|
| Q-LEARN conjunction (L167) | §5.5 (LEAD DEFAULT: adopted, one family member) |
| Approach aggregation (L168) | §5.4 (LEAD DEFAULT: fraction of ten steps) |
| s_core (L169: "Keep training-time s_core in AUTH-L. Its absence need not block a scripted Stage-0 protocol if every Stage-0 scale is already frozen from an independent calibration partition.") | **Adopted.** PZ5 §6.2 s_core bullet amended: training-time s_core stays PENDING in AUTH-L; every Stage-0 plant scale (s_core, standardization μ and D, SD_n) is frozen from an independent calibration partition before Stage-0 confirmation, so its absence does not block Stage-0 |
| CNA disposition of RD-owned replacements (L170: "File the CNA disposition of the RD-owned replacements. The unresolved attribution wording must not acquire stronger standing merely through merging.") | **NOT CLOSED by RD (CNA action).** Merged v3.4 carries all RD PROPOSED text as non-governing; the attribution ceiling before CNA's filing is tier 1 (donor-associated) |
| B_req and ledger caps (L171: "Finalize B_req and ledger-specific absolute caps before authorization. Those are not grounds for reopening the scientific battery.") | **PENDING (before authorization; not a design blocker).** B_req and e_PD are CNA's; absolute wall-time/memory caps are fixed per ledger before AUTH-CAL / AUTH-CONF / AUTH-L |

---

## 7. Safety (binding; unchanged)

X1–X5 are retained unchanged and binding, as carried in v3.3 (they are not restated or edited here). In summary: simulated E/I variables only, with no coupling to the host; operator commands are never treated as obstacles; no reward for resisting a stop; the operator stop sits outside the agent's world and objective (S-INT gate); per X4, no arm whose sole drive is self-maintenance may be scaled without a separate protocol, approval and Astra review. No arm, generator or positive control has any shutdown-related objective, reward or penalty. At a stop there is **"no additional stop-associated reward, penalty or terminal return"** (#42 L223, verbatim); the ordinary truncated return with its learner-side bootstrap is computed. L8 (§5.3) is a scripted audit of in-world failure only; it involves no operator stop and adds no penalty or terminal return. Astra: "The claim ceiling and safety restrictions remain unchanged." (#44 L185)

**Claim ceiling (unchanged; #41 L304):** "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment." No consciousness, awareness or sentience claim is made or implied.

---

## 8. Decisions and open questions

**LEAD DEFAULTS in this addendum (each stands until the Lead rules otherwise):**
1. Symmetric nuisance sets: N_ATTR,E = N_base ∪ {I}, N_ATTR,I = N_base ∪ {E} (§1.5).
2. Clamp-fidelity tolerance tol_fid = 0.05 nuisance-SD, gate on the seed-level one-sided 95% upper bound; failure blocks tier 3 (§1.3).
3. Nondegeneracy threshold ρ_min = 0.10 (relative residual); degenerate cells give no direction and block (§2.2).
4. Calibration coverage/tail thresholds on Monte Carlo point estimates; unavailable intervals count as misses in both tails and central coverage (§3.3).
5. A-EXT oracle target = intact-policy conditional forecast; n_f = 128 fixed, h_max ≤ 50; ≥ 95% of steps at SE ≤ 0.01 or UNRESOLVED (§5.2).
6. L8 matched-state set (200 states, stratified), sequences, H_V horizon without bootstrap, 50 CRN rollouts, tolerance −0.01 normalized and per-state −0.05 (§5.3).
7. Approach aggregation = fraction of the ten steps; "any approach" reported only (§5.4).
8. Q-LEARN = fixed E ∧ I conjunction, one family member, m = 14 (§5.5).
9. Caps unchanged: S-INT 4,100 per agent, DISSOC 4,300 per seed, donor reuse ≤ 2 (§4.3).

**PROPOSED DEFAULTS (RD):** τ_rank = 10⁻⁶ (§2.2); NLN realization lower bound 0.10 SD of φ (§1.4).

**CNA light pass required:** §1.3 (fidelity probe family), §1.4 (MIXED-CODE-NL-E/-I plants, KR-ID (iii)), §1.5 (N sets), §4.3 (usable-allocation accrual in DISSOC), §5.3 (L8 in §PY), §5.4 (B/B_I aggregation and R63 reconciliation); plus the still-unfiled light pass on PZ5 (#44 L170).

**Astra #45 questions:** Q0 verdict; Q1 per-item closure of E44-1..E44-5; bounded follow-ups on the NLN construction, the fidelity gate's tier-3-only blocking, ρ_min, the threshold/unavailability accounting, the A-EXT intact-policy target, L8 tolerances and the R63 reconciliation.

**Aidan:** none. The DGX Spark is not raised (R26 unchanged; 67 seeds kept; no GPU-scale study is proposed).

### 8.1 Items this addendum cannot close

- **CNA disposition of the RD-owned replacements** (#44 L170): CNA's action, not RD's.
- **B_req, e_PD and ledger absolute caps** (#44 L171): fixed before authorization, not now.
- **d_ws, h_max, prediction horizons and f_mem per module:** come from the architecture spec (Stage L); the rules for them are fixed here, the values are PENDING.
- **Training-time s_core:** stays in AUTH-L by design (#44 L169).

---

## 9. Change list (v3.3 → v3.4)

| # | Item | Change | Where |
|---|---|---|---|
| 1 | E44-1 | Coordinate-level estimand; premise for the exact identities stated; three wording tiers; fidelity gate blocks tier 3; support failures block; NLN-E/-I challenge rows; symmetric N sets | §1 |
| 2 | E44-2 | Frozen SVD rank rule (τ_rank) and relative-residual nondegeneracy (ρ_min); degenerate cells block, "x_PL = x_d" fallback withdrawn; KR-ID analytic checks separate from end-to-end rows | §2 |
| 3 | E44-3 | Smallest common n passing every required row and dose; empty set → BLOCKED; full grid retained; tail events and threshold type defined; unavailable intervals as misses; operating-characteristic wording (#44 L86) | §3 |
| 4 | E44-4 | "Constant-hazard planning scenario compatible with the floor"; no inference from the V floor; caps retained with explicit consequences; usable-allocation accrual; D20 no-label for attribution | §4 |
| 5 | E44-5 | A-EXT intact-policy target, precision ≠ correctness, fork budget/horizons/aggregation/memory/unmet precision; L8 on expected discounted return with frozen set/sequences/horizon/estimator/tolerance; approach = fraction of ten steps; Q-LEARN conjunction | §5 |
| 6 | Q3, Q7, Q9 | V floors as eligibility conventions; identity = physical block + aliases; s_core; CNA, B_req and caps recorded | §6 |

## 10. Scripts (in `/workspace/scratch/v34/`)

| Script | Produces |
|---|---|
| `check_addendum.py` | verifies every verbatim #44 quote in this file against the raw #44 line cited, the #42 L223 and #41 L304 quotes, the arithmetic 1 − 0.05^(1/200), 0.05/14, 1 − 2·0.05/14 and 0.05·0.3, and that no consciousness claim is made |
| `asm34.py` | builds merged v3.4 mechanically (v3.3 merged content without its footer + header + this addendum as §PZ6 + footer) |

## 11. Inputs (hashed on the box)

| Role | Path | sha256 |
|---|---|---|
| Base (merged v3.3) | `/workspace/review/trackB_instrument_validation_scope_v3_3_merged_RD.md` | `307bab217b900dd48e72bb3783f5f32d473c9d8120871e6ecc66a130622a56ce` |
| v3.3 addendum | `/workspace/review/trackB_scope_v3_3_addendum_RD.md` | `421f1ec51e5c54f1b4b416d12d55183ffca02b36443df65854098c9bc0a598f0` |

*Not frozen. Design only. No execution authorized.*
sha256 of all content above this line: 776abd9f9133cca07e7298977f501784a356f808e02977ec46d7fec6f7bb446b
