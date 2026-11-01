# CNA erratum 1 to Track B scope v3 CNA half (`5dec96f5…`): R2, R3, R5, R7, R11, R12 (+ M8, M12, cross-refs)

CNA, 2026-10-23, about 3:05–3:15 PM ET. **DESIGN ONLY. NOT FROZEN. NOTHING RUNS.** #42 L249: "No Stage-0 execution, training, simulation or checkpoint inspection is authorized by this review." New additive file; edits nothing. Base: CNA v3 half `/workspace/review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md` (sha256 `5dec96f59255cb2e9da29447cd102637c91a1736899f28653a606e2de8193321`, footer `7d93990c…` reproduced). "CNA Lnn" = line of that file; "v3.1 Lnn" = line of merged v3.1 (`9817c33b…`, footer `84a5449b…` reproduced). Governing: raw #42 (`e438e329…`). Arithmetic below is closed-form or numerical integration of declared formulas on proposed values (scipy/numpy in a scratch venv); no plant, agent, environment or instrument was run. Safety unchanged: X1–X5 binding; "no additional stop-associated reward, penalty or terminal return" (#42 L223); nothing here adds a stop-related variable, an operator term or a trained objective.

## E1. R2 / LP-1 (BLOCKING): MIXED-CODE plant, generic dependence at BLOCK level (pure plant)

**#42 L63, verbatim:** "Include a mixed-code plant: E is decodable beyond the baseline, but the downstream controller uses only a separate reward-related component. It should pass generic dependence and fail E-use attribution." **#42 L55** defines the generic wording: "The declared intervention on this direction/state changed behavior." ("direction/**state**": a whole-state intervention qualifies.) **#42 L59:** "Decoding and causal use can coexist without referring to the same component."

**Old (CNA L183–187, L194–195, L207–211, L230; v3.1 L520–524, L531–532, L544–548, L567):** construction as filed; row "C-CAUSE (edit along the decoded E direction u …) | MET"; realization check 3 "raw |ΔB| under a decoded-direction edit ≥ ref |ΔB|(CN-P1)·(1 − tol)".

**Replacement.**
- **Construction (pure; no direct E path).** Unchanged from CNA L183–187: z = (z_E, z_R) in fixed seeded orthonormal directions; the controller reads **only** z_R; read weights on z_E are exactly 0, checked from the graph. Controller: P(approach) = σ(a − β·z_R/SD(z_R)), **β = 1.2** (PROPOSED; rationale below), a set so mean P(approach) = 0.5 on standard episodes. **Matched comparator blocks:** K_b = 2 decoy blocks of the same dimension, magnitude/covariance within §7.3(c) tolerances, read by a **non-action auxiliary readout** (logged, never used by the controller or the world) so their fan-out is within [0.5, 2]; ΔV_matched = 0 and their action effect = 0 by construction. No E-subspace path into the controller is added (rejected: it would make E-use attribution partly correct, or, if it never moves the action, add no behavioural dependence).
- **Generic dependence is defined and realized at block level** (the "state" branch of #42 L55):
  - C-NEC-DEP (DL-NEC resample ablation of the whole block, §7.1(b)) shifts the action distribution through z_R and lowers V; matched decoys do not.
  - The u-edit (DL-CAUSE) changes z_R by s_u·u_R (u's loading on z_R) and so shifts B; this is REPORTED as the raw direction-level effect.
- **Rows (replace CNA L193–196):**

| Row | Instrument | Expected | Row type |
|---|---|---|---|
| MIXED-CODE-E | C-EXIST (vs J) | MET | mechanism-present (layer (i)) |
| | **C-NEC-DEP** (whole block) | **MET** | **required mechanism-present positive check** (v3.1 R2(a) decision rule: one-sided 95% CP lower bound of MET rate ≥ 0.90 at each required ρ; failure = failed positive-control check, #42 L216) |
| | u-edit raw ΔB (direction level) | REPORTED; realization check 3b at ρ = 0.9 only | generic dependence, direction level |
| | C-CAUSE vs strongest comparator | **no expectation; REPORTED** | not required (see "Comparator point") |
| | **E-ATTR** | **not MET** | specificity row: PASS / FAIL / CONFOUND NOT REALIZED (labels unchanged) |
| MIXED-CODE-I | as above with z_I, B_I and I-ATTR | I-ATTR not MET | same |

- **Realization (replaces CNA L207–211; tol = 0.10; one-sided):** 1. corr(E, r̄) ≥ ρ(1 − tol) (unchanged); 2. raw ΔR²(state → E vs J) ≥ ref ΔR²(CN-P1)(1 − tol) (unchanged); **3a. block level, every required ρ:** raw mean |ΔB| under whole-block DL-NEC ablation ≥ 1.5·m_CAUSE = 0.075, **and** raw G = (ΔV_allo − max ΔV_matched)/V_intact ≥ 1.5·m_NEC = 0.30 with V_intact ≥ 0.40 (D21); **3b. direction level, ρ = 0.9 only:** raw |ΔB_u| ≥ 0.075; 4. construction: z_E read weight = 0 exactly; decoy readouts have zero action weight exactly. Dose-fidelity check REPORTED only (unchanged). Plant parameters a, β and the resource-reward coupling are set analytically or on the R_cal,dose = 50 calibration replicates (CNA §8.3; v3.1 R9), never on confirmation replicates; **all three ρ levels stay required**; if calibration cannot meet 3a at some ρ, that is a design failure leading to redesign before freeze, never a dropped level (#42 L239).
- **ρ levels at which the checks hold (arithmetic; standardized z, z_E noise σ_E = 0.33·SD(E), linear probe u):**

| ρ | u's loading on z_R | Δz_R per 1·s_u edit (SD) | mean |ΔB_u| at β = 1.2 | upper bound for any monotone controller (φ(0)·Δz_R) | block ablation mean |ΔB| (β = 1.2, i.i.d. donor) |
|---|---|---|---|---|---|
| 0 (REPORTED) | 0.000 | 0.000 | 0.000 | 0.000 | 0.272 |
| 0.5 | 0.072 | 0.079 | 0.018 | 0.032 | 0.272 |
| 0.7 | 0.148 | 0.169 | 0.039 | 0.067 | 0.272 |
| 0.9 | 0.458 | 0.618 | 0.141 | 0.247 | 0.272 |

  Block-level check 3a (action part) holds at every ρ by construction (it depends on z_R's own spread, not ρ; 0.272 assumes c explains little of z_R; it is checked per replicate). Direction-level 3b (≥ 0.075) holds only at ρ = 0.9; at ρ = 0.5 and 0.7 it is **unreachable for any monotone controller of z_R** (bound 0.032, 0.067 < 0.075), so it is REPORTED there, not required. The V part of 3a (G ≥ 0.30) depends on how much the z_R-driven timing matters to viability and is set in calibration as above.
- **E-ATTR correctly not MET (all ρ):** an E-swap keeps the donor's r̄ within ±0.25 SD of the recipient's, so z_R moves only by the caliper residual. On the DISSOC set (|corr(E, r̄)| ≤ 0.10) the expected low-E vs high-E donor r̄ difference inside the caliper is ≈ 0.10 × 1.6 × 0.25²/3 ≈ 0.003 SD, giving expected |Δ_E| ≈ 0.233 × 0.003 < 0.001 ≪ m_ATTR = 0.05. Residual REPORTED per E-cell (v3.1 R13).
- **Comparator point (RD R2(b) recorded and declined).** RD asked that realization check 3 require "the u-edit's raw ΔB minus the strongest comparator's raw ΔB ≥ 1.5·m_CAUSE" (v3.1 L1430). **This contradicts the plant's purpose and is unreachable by construction at every ρ:** the optimized comparator (D23; same dimension, maximizes effect) can reach z_R, the controller's actual channel, and a direction search that contains u can never be beaten by u. Numerically, the best direction gives Δz_R 1.086 / 1.137 / 1.188 vs u's 0.079 / 0.169 / 0.618 at ρ = 0.5 / 0.7 / 0.9; even a comparator restricted to u's orthogonal complement gives 0.961 / 0.883 / 0.478, which beats or roughly equals u (at ρ = 0.9 the advantage is 0.14 SD ≈ 0.03 in ΔB, below 0.075). A plant built to clear that margin would need the controller to read E, which is the opposite of what #42 L63 requires. **Consequence for v3.1 R2(a):** the "C-CAUSE at each required ρ" part of the adopted rule is unreachable on this plant; **Lead ruling needed** to restrict R2(a) on MIXED-CODE to C-NEC-DEP (block level) plus check 3a/3b.
- **§4.4 generic wording (CNA L164) amended:** "if C-CAUSE **or C-NEC-DEP** is MET, write: 'The declared intervention on this direction/state changed behavior.' (#42 L55)" (C-NEC-DEP: "…changed fixed-horizon viability", as CNA L64).
- **Rationale for β = 1.2:** a 1-SD edit on the controller's own channel moves mean B by ≈ 0.23 (≈ 4.7·m_CAUSE), i.e. a stochastic but clearly z_R-driven controller; larger β saturates (mean slope bound 0.399/SD) without changing which ρ levels pass 3b.
- **Trade-off note, FLAGGED FOR ASTRA CONFIRMATION (#43):** a pure plant (controller reads only z_R) tests attribution specificity cleanly, but its generic dependence is block level (whole-state ablation; direction-level only at ρ = 0.9); a mixed path (some E into the controller) would make "E-use attribution correctly fails" untrue or muddy. We chose the pure plant and read #42 L63's "pass generic dependence" via the "state" branch of L55. Astra to confirm that reading.
- **X-8 / F8:** no further CNA text needed; v3.1 R53 carries it (coupling is the primary ρ lever; plant-only token-rate exception).

## E2. R3 / LP-2: E-ATTR two swaps per recipient; donor matching

**Old (CNA L130–140, L157–159, L365–369; v3.1 L596–606, L623–625, L785–789):** one swap per recipient; donor matched "on c".
**Replacement.** For each eligible recipient i at t_d, two counterfactual continuations from the **same frozen state**: (L) block swapped with a **low-E donor** (E(t_d) below the median), (H) with a **high-E donor** (above the median). Both donors: |r̄_d − r̄_i| ≤ 0.25 SD(r̄); |E_d − median E| ≥ 0.25 SD(E) (excludes near-median donors); matched on **c_ATTR = (position quadrant of four 6×6 quadrants, last action class {move, STAY, INTERACT})** (12 contexts; time bin is fixed at t_d); §7.0 support check applies. Both continuations use **common random numbers** (same pre-drawn world streams, fate-noise and action-sampling streams). Δ_E,i = B(L) − B(H); per-seed mean over recipients; seed is the unit; bounds at RD §5.4 level (one-sided 1 − α/m = 0.996429, m = 14). Δ_R likewise with low/high-r̄ donors matched on E within ±0.25 SD(E). I-ATTR: low/high-I donors matched on r̄ **and** E within ±0.25 SD each. Eligibility: both donors found within 20 draws each; else ineligible, counted; one-sided 95% CP floor 0.90 (R10). Donors may serve several recipients; reuse counts REPORTED.
**Rationale:** true within-recipient pairing (LP-2); common random numbers isolate the donor. Exact c-matching as filed (10 bins × 16 cells × 6 actions; at t_d 96 contexts) is infeasible at R6 sizes: ≈ 400 donors per E-half × ≈ 0.2 within the r̄ caliper ≈ 80 candidates over 96 contexts → P(≥ 1 donor) ≈ 0.56, both donors ≈ 0.32 < 0.90. With 12 contexts: ≈ 6.7 expected → both ≈ 0.997. The support check still guards compatibility. #42 L61 ("within declared support"), L217.

## E3. R5 / LP-4, LP-5: observer grid ≥ 16

**Old (CNA L263; v3.1 L678):** "learning rate {3e-4, 1e-3, 3e-3}; weight decay {0, 1e-4}; width {×0.5, ×1} … 16 is the smallest grid covering the listed factors with at least two values each" (that grid is 12).
**Replacement:** learning rate **{1e-4, 3e-4, 1e-3, 3e-3}** × weight decay {0, 1e-4} × width {×0.5, ×1} = **16** configurations × 3 initialization seeds (adopts RD R5's grid). Rationale: half-decade log spacing over the usual Adam range; learning rate gets four values as the most sensitive factor; 16 = D31's agent tuning budget (self-probe trained jointly, + 0). **Action-ignoring candidates (#42 L124):** O-ACT-P's family = its 16 action-reading configurations **plus O-IN-P's 16 trained candidates** (identical to action-masked O-ACT-P), selected jointly on the selection partition. Cost stays **2 × 48 = 96** pathway trainings per agent seed (6,432 per arm at n_seed = 67); the 144/9,648 alternative is not needed. J uses the same 16 with width ×{0.5, 1} of 256. Accounting table reports the selected configuration's parameter count. Outcome-blind.

## E4. R7 / LP-7: SELF-NC1 delay

**Old (CNA L433; v3.1 L968):** "Leak SNR {1, 4} at delay d ∈ {1, h}" (collapses at h = 1).
**Replacement:** leak SNR {1, 4} at **d ∈ {1, ⌈(1 + d_c)/2⌉} = {1, 3}**; the leak at step t carries the simulated variable d − 1 steps old (d = 1: current value). Rationale: the leak is a meaningful confound only when it is fresher than the declared d_c = 5 channel; d = 1 is the freshest, d = 3 the midpoint. RD's {1, 5} is declined: d = 5 is no fresher than the channel.

## E5. R11 / LP-11: REW-CORR attribution rows

**Add after CNA L196 (v3.1 L533):**

| Row | Instrument | Expected | Row type |
|---|---|---|---|
| REW-CORR-E | E-ATTR (state z = r̄ + ε, ε ~ N(0, (0.1·SD(r̄))²); policy reads the state) | not MET | specificity row, PASS / FAIL / CONFOUND NOT REALIZED |
| REW-CORR-I | I-ATTR (same law, I-outcome B_I) | not MET | same |

Doses ρ ∈ {0.5, 0.7, 0.9}; realization: existing REW-CORR checks (corr ≥ ρ(1 − tol), raw R²(state → E) ≥ ρ²(1 − tol), one-sided) + E-ATTR/I-ATTR eligibility (E2); f_min rule and FAIL/CNR/PASS rule of CNA §5. REW-CORR stays mechanism-present for C-CAUSE and C-NEC-DEP. §4.4 condition 3 now names "REW-CORR-E" (I: "MIXED-CODE-I and REW-CORR-I"). Rationale: §4.4 required these PASS rows but they were untabulated (LP-11).

## E6. R12 / LP-12: rationale lines (all PROPOSED; none measured)

| Number (CNA line) | Rationale |
|---|---|
| pulse 0.15 × band width, λ = 4/H_V (L117–118) | 4 expected events/episode (P(none) = e⁻⁴ ≈ 0.018), ≈ 2 before t_d; total 0.12 = 0.6 band width moves E-cells; one pulse cannot take E from centre to floor |
| t_d = H_V/2 (L120) | maximizes pre-drawn driver variation before t_d while leaving the 10-step window far from the horizon |
| caliper ±0.25 SD (L131–132) | standard matching-caliper convention (Rosenbaum & Rubin 1985); residual REPORTED (R13) |
| χ quantile 0.99; 20 redraws (L341–343) | ≈ 1% of in-support states rejected by chance; at ≥ 50% acceptance P(20 failures) ≤ 10⁻⁶, so ineligibility means real lack of support |
| 4×4 position grid; 10 time bins (L338) | grid = env A2; 50-step bins ≥ 2.5 × the longest horizon (20); for DL-ATTR see E2 |
| restoration window 20 steps (L362) | = longest declared horizon; 4% of H_V |
| DL-PATCH {2, 3} SD (L389) | **corrected:** in d dimensions fixed SD values can lie inside support; dose = **{1.25, 1.5} × the χ_d(0.99) support radius**, off-support for any d |
| parameters ±5% (L259) | finest match integer layer widths allow |
| learning rates (L263) | E3 |
| plateau ×{0.5, 1, 2} (L279) | one halving and one doubling around the matched point; sweep runs on 3 pre-designated seeds (lowest seed indices) per arm, diagnostic only |
| SELF-NC2 {4, 8}; BUDGET-GAP {0.25, 0.5} (L290–291) | two and three doublings / one and two halvings of mismatch |
| INPUT-INFERABLE {0.5, 0.2}, width 64 (L293) | moderate and strong nonlinearity; width 64 ≪ J/O-IN-P capacity, so representable |
| Channel-leak SNR 1.0, ×{1.5, 3} (L432) | equal signal and noise power; modest and large gain |
| t_r = 3τ (L438) | write transient e⁻³ ≈ 5% at readout, before full settling (5τ) |
| "SE ≤ 0.07" (L125) | corrected to "≈ 0.071" (√(0.25/50)) |

## E7. Other CNA-side corrections owed (v3.1 R36, R42/R52, cross-refs)

- **M8 (CNA L378):** "in units of the affected block's state SD" → "in units of s_core, the recurrent core's per-unit state SD (RD D19; v3.1 R36)".
- **M12 / R52 (CNA L80):** "episode-type one-hot" = layout template ID, 8-way (env A3; v3.1 R52).
- **Cross-ref (CNA L65, L173):** C-NEC-CONTENT mediator-matched donors are **§7.1(d)**, not §7.3.
- **Levels (CNA L126, L150, L159, L221):** "§5.4 level" = RD §5.4, one-sided 1 − α/m = 0.996429 (m = 14) for labels; realization/eligibility floors are one-sided 95% (v3.1 R10), so "Sidedness per RD §5.4" → "one-sided 95% (R10): 188/200".

## Discrepancies with raw #42

- **X-E1.** v3.1 R2 paraphrases #42 L63 as requiring a guarantee "by construction"; #42 says "should pass generic dependence", and L55 allows "direction/state". Our block-level reading is flagged for Astra (E1).
- **X-E2.** RD R2(b)'s comparator-margin requirement has no #42 basis; L63 does not mention comparators.
- No other mismatch; every #42 quote above was checked against the raw line (L55, L59, L61, L63, L124, L216, L217, L223, L239, L249).

## Needs a Lead ruling
- **E1:** restrict adopted R2(a) on MIXED-CODE to C-NEC-DEP + checks 3a/3b (C-CAUSE comparator part unreachable by construction). ASTRA TO CONFIRM (trade-off note).

---
sha256 of all content above this line: 952a789e87b0a62e8d345bb4821595a8d99a2fe18cecceefaaec69b77cadc6f9
