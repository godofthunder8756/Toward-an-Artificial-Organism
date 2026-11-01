# Adversarial review: C-κ oracle-only scope record v1

Research Delegate, 2026-10-22 (ET). **Review only.** I did not run the package, propagate any filter or load any checkpoint. The checks below are hand arithmetic and reads of files already on record. No existing file was edited.

**Reviewed:** `/workspace/review/ckappa_oracle_scope_record_v1.md`, sha256 `1b450bcf231324c6fc3c686cc2daa819ed5f09cd5725c7c3283a1b3e2c39c5bf` (verified).

**Governing texts:**
- Astra #35, `/workspace/astra_consult35_response.txt`, `563e070c…` (verified, read in full).
- Planning note v1.3 (`57899307…`, verified), v1.2 (`46b8c912…`, verified) and A1.
- My review `81e2ac54…` and delta check `e969b50a…`.

**Repo files read (read-only):**
- PR #4 `twostream_results_v1/results.json`: blob `680c8290`, sha256 `bf2de92c9cd09809…`. It is identical at `5d9d8a7`, `88b500a` and `379bb01`, and absent from `master`.
- PR #5 `TWOSTREAM_PROTOCOL_v1.md`.
- PR #7 `RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md` at `379bb01`.

## Verdict

**READY WITH NAMED FIXES.** There is no blocker. The record is close to what Astra #35 L183–192 asks for. Six MAJOR items should be fixed in an additive `ckappa_oracle_scope_record_v1_1.md` before it goes to Astra and before freeze:
- **S-M1:** a filter-composition error.
- **S-M2:** the headroom quantity does not match the comparator Astra specified.
- **S-M3:** a dry run is scheduled before the freeze and application.
- **S-M4:** the proposed inference floors allow "two poor predictions".
- **S-M5:** the ε range is small enough to collapse into the Jacobian test.
- **S-M6:** an ALL-group positive could be driven by XOR alone.

None of these needs a new consult question.

## 1. Conformance to E35-1 to E35-12

| Item | Where in record | Status | Note |
|---|---|---|---|
| E35-1 target claim and non-claims | §8; v1.3 by reference (L3) | CONFORMS | The package makes only oracle statements. Restate E35-1 verbatim in §6, where the inference floors appear. |
| E35-2 fixed-κ comparator is not the lookup rival | §4 O5 ("exact fixed-κ comparator"), O7 interpretation (L76, L79) | CONFORMS | §6 still says "B_μ". Name it "fixed-κ marginal-response model" (v1.3 §2) and add "a gain over it is not evidence against a smooth lookup". |
| E35-3 primary = held-out finite-edit prediction; gain AND absolute accuracy; Jacobian separate | §6 floors (L105–L108); O6 uses Pred_full | **PARTIAL** | Both criteria are present. Missing: (i) the neural Pred_full(δ,u) = Φ(b_a+Bδ,u) − Φ(b_a,u), B frozen before scoring, defined in §6; (ii) the statement that the nested Jacobian comparison is a diagnostic only and not replication; (iii) the floors are too weak to exclude "two poor predictions" (S-M4). |
| E35-4 gating = full-state random; signs and magnitudes frozen; no replacement; accounting | §6 L98–L104 | **PARTIAL** | Seeds, signs, magnitudes and no-replacement are frozen without B. ✔ The descriptive families (κ-directed, null(B), row(B), chord, equal-impact) are not listed. The magnitude set may collapse to the Jacobian test (S-M5). The invalid and guard accounting rules differ (S-m6). |
| E35-5 exact-filter positive control; N1 veto removed | §4 O6 (analytic expectations L66–L70); §5 has no surrogate veto | CONFORMS | The surrogate-ineligibility rule is gone. O7 is comparator-only (L79). ✔ |
| E35-6 bounds name target, norm, weighting, domain; only baseline-SE bound asserted | §3 L35; O5 L58–L59; O3 L49 | **PARTIAL** | O5 calls H "the maximum squared-error gain available to the full model". That is wrong for the *separately fitted* comparator (S-M2). R_G's weighting is unstated (S-m3). |
| E35-7 low rank/sensitivity is not an integrity failure; unresolved vs resolved rank; no switching | §5 L91; §6 L104 | **PARTIAL** | "HEADROOM NOT MET", no inference and no switch. ✔ No numerical-rank tolerance separates unresolved from resolved low rank for O3 (S-m4). |
| E35-8 one B per seed/arm/fold; three holdouts separate; continuation reuse | §2 L21–L26; O6 L64 | CONFORMS | Fold arithmetic is checked in §5 below. Add the PR #7 VAL subset to the predictor-training tabulation (S-m7). |
| E35-9 distinct units; native post-reading state; frozen metric; oracle does not certify neural checks | §4 O4 (standardized chart units); §6 (absolute h₄, Euclidean); O5 L59 | CONFORMS | Add E35-9's last sentence to §5 verbatim. |
| E35-10 F-TRAINED primary; PR #5 status; PR #8–#10 out | Not stated in record (v1.3 §2 only) | **PARTIAL** | §5's rationale scales on **PR #5** CAND GRU-8 E_total. PR #5 is not on the roster (S-m2). State the roster sentence once. |
| E35-11 matched comparisons; R-MF-A unevaluated | §4 "Not in this package" (L80–L83) | CONFORMS | |
| E35-12 48f4cdc6 unrecoverable | v1.3 §2 | CONFORMS (not applicable here) | |
| Astra L187: separate marginal effects from the direct XOR response | §3 L29–L33; §5 MARG rule | **PARTIAL** | Separation is declared. But ALL is primary and can pass on XOR alone (S-M6), and the MARG label wording is off (S-m8). |
| Astra L190: no silent stage substitution | §1 L14; §5 L91 | CONFORMS | |
| Astra L192: cap, no retries, preserve outputs, substantiate estimate | §7 | **PARTIAL** | The counts are undercounted (S-m5), and the dry run is mis-sequenced (S-M3). |

## 2. MAJOR findings

### S-M1. The oracle continuation map has the wrong number of transitions

§1 L13 fixes the stage-k belief as "the posterior after reading k and *before* the transition", with a transition after every reading except reading 8. The W2 protocol agrees: transitions follow each reading, and "No transition after the last reading".

So from the stage-4 belief to stage 8 the steps are: transition, reading 5, transition, reading 6, transition, reading 7, transition, reading 8. That is **four transitions and four readings**. §1 L16 says "three transitions and four readings".

As written, Φ(b_a, u) would skip one transition. Every L, H and R value would then be wrong. O1 would catch this only if it checks the composition directly.

**Fix:**
- Correct L16 to four transitions.
- Add an O1 fixture: for all 256 (a, u), Φ(b_a, u) must equal the stored terminal forecasts of history h = a + 16u. These are `marginal_x`, `marginal_y` and `xor_joint` in `per_history`, stored as **exact rationals**.

### S-M2. H is not the headroom of the comparator Astra defined

Astra's comparator, verbatim (L64): "uses the separately fitted B_mu, changes the two marginal coordinates, and keeps kappa fixed". E35-6, verbatim: "Baseline squared error bounds the corresponding squared-error improvement."

O5's H instead zeroes the κ component of Δ while keeping the *true* marginal components. That is the loss of an oracle-assisted fixed-κ model, not of a *fitted* one. Take the exact filter in any well-conditioned coordinates (the O6 fixture), with J = L·B_true. A least-squares fit of J ≈ L_μ·B_μ gives

B_μ = B_true,μ + P·B_true,κ, where P = (L_μᵀ W L_μ)⁻¹ L_μᵀ W L_κ

stacked over the fit prefixes and continuations. The fitted comparator absorbs the projection of the κ template onto the marginal templates. Its residual is only the orthogonal part (I − proj_μ)·L_κ·Δκ, to first order. So typically H* ≈ H·sin²θ, where θ is the O3 principal angle. With a small θ, H can pass §5 while the real available gain is far smaller. That is the R1/E34-1 trap in the optimistic direction.

**Fix:**
- Define the primary headroom H* as the **held-out loss of the separately fitted fixed-κ comparator on the O6 exact-filter fixture**, under the frozen oracle-scale edits, with finite differences and per output group.
- O6 already computes this: its expectation (iii) equates the gain with that loss.
- Keep H and R as descriptive context.
- Apply §5's thresholds to √H*_G and R*_G = H*_G / response. Coefficient absorption is invariant to the coordinate choice A, so H* is oracle-only.
- State that H* bounds the gain only for the exact-filter fixture. The neural bound is still the checkpoint-dependent comparator loss (E35-9).

### S-M3. The dry run before freeze breaks the order "nothing runs before freeze + application"

§7 L112 says the estimate "is to be confirmed by a timed dry-run of the frozen code on O1 only, as part of the freeze". That executes package code during the freeze, before the standing-approval application is filed.

Astra #35 L192, verbatim: "ten cumulative wall-clock minutes including setup and verification". Under that wording, a dry run is part of the capped execution.

**Fix:** either drop the dry run and rely on the paper estimate (corrected in S-m5), or allow it only **after** freeze and application, counted against the 10-minute cap and logged. Its outputs are part of the run record, not a pre-freeze calibration.

### S-M4. The proposed inference floors can pass "two poor predictions"

Astra L71, verbatim: "A relative improvement between two poor predictions is not sufficient."

The proposed floors are a gain of at least 10% of the comparator's loss, plus a normalized full-model error of at most 0.25 over ‖ΔF‖². Suppose R_ALL is small, say 0.05, which §5 would accept. Then ‖ΔF‖² is dominated by marginal-driven responses, and the comparator meets the 0.25 accuracy floor on its own. The full model can then pass with error equal to 90% of the comparator's error. That is roughly 90% of the κ effect itself, so the κ part is predicted poorly, yet both criteria are met.

**Fix.** These floors are recorded here only to keep floor and headroom separate, but fix them now:
- (a) Add a κ-component accuracy criterion: Σ‖Pred_full − ΔF‖² ≤ c·Σ‖Pred_full − Pred_μ‖², with c fixed in advance (for example 0.5). Error then has to be small relative to the predicted κ contribution.
- (b) Or raise the gain floor to a level that implies adequate κ-part accuracy, for example ≥ 50%.
- State the aggregation and quota: claim unit (seed), across 6 folds and 3 ε, with a ≥ 8/10 style quota. Make it a declared convention, as in E3/S15, frozen with the inference spec.
- Each prefix is evaluated in 3 of the 6 folds. Folds are not independent replications.

### S-M5. The magnitude set may make the gating test a restatement of the Jacobian fit

Astra L56, verbatim: "sufficiently small random-edit agreement with L*B*delta largely reproduces the Jacobian fit." L73, verbatim: "The magnitude rule must not be chosen to make the linear approximation succeed."

ε ∈ {0.02, 0.05, 0.1} in absolute units on h₄ ∈ (−1, 1)⁸ is about 0.007–0.035 per coordinate for a unit direction. All three are small. No checkpoint scale is available before inspection, and none may be used (E35-4). So the risk that all three sit in the linear regime cannot be ruled out. That would undo E35-3's separation from the diagnostic.

**Fix:**
- Add at least one non-small magnitude, for example ε = 0.25, still frozen and absolute.
- Declare in advance which magnitudes count toward a positive: all of them, or a stated subset, never chosen afterwards.
- Report the finite-versus-linear discrepancy at every ε.
- This uses no checkpoint information, so it stays consistent with m2 and E35-4.

### S-M6. An ALL-group positive could be XOR-only

ALL is primary (§6 L108). XOR responds to κ directly. MARG responds to κ only through readings of the other stream: the transition's marginal update does not involve c (W2 transition law), while the observation update does. So an ALL pass can be carried entirely by XOR.

§3 L33 forbids calling an *XOR-only effect* cross-stream marginal updating. It does not cover an ALL pass with a MARG failure.

**Fix.** Pre-write the rule: "cross-stream marginal" wording requires that MARG is *available* (§5) **and** passes its own floors. An ALL pass with a MARG failure or unavailable MARG reads "ALL-group response prediction; marginal component not shown". Per-group results are always reported. This follows Astra L187, verbatim: "An XOR-only finding does not establish covariance-mediated cross-stream marginal updating."

## 3. MINOR findings

- **S-m1. O1 cannot match stage-4 beliefs against results.json.** The file stores 256 *terminal* `per_history` records with exact rationals (probability, marginal_x, marginal_y, covariance, xor_joint, belief), not only 50-digit truncations. At stage 4 it stores only aggregates:
  - `storage.marginal_index_by_stage["4"]`: 16 distinct keys, exact lookup, total bits 1946/2076;
  - `descriptive_min_marginal_separation["4"]` = 404227584000000000/11798871063978072289.

  **Fix:** match terminals exactly via S-M1's composition check, and match stage-4 beliefs only against those aggregates. Also check P(a) = Σ_u P(a·u). Cite the file by commit `5d9d8a7` and blob `680c8290`, since it is not on `master`.
- **S-m2. Threshold rationale.**
  - The §5 arithmetic is correct: √(1.1585e-3/3) = 0.0197, and 1/20 of that is 9.8e-4. The value is PR #5 cand_gru8 s1 TEST total (4.658e-4 + 1.848e-4 + 5.079e-4).
  - But PR #5 is not the roster. The PR #7 F-TRAINED TEST E_total minimum is 1.552e-3 (s109), giving about 0.0227.
  - It also compares a *level* error with a *difference* effect.
  - The 10⁻⁴ MARG threshold and the 75% validity rule have no rationale. The thresholds are fixed before computation, which I accept on the author's attestation (no code exists). They are therefore not gameable after O5.

  **Fix:** label all §5 thresholds as declared practical conventions (cf. Astra #34 L26), not derived bounds. Re-cite the scale to PR #7 or drop it. Add R_MARG ≥ 0.05 next to √H_MARG, because MARG could otherwise be dominated by own-stream μ effects. The §5 decision does depend only on oracle quantities. ✔
- **S-m3. Weighting of R_G.** "Σ‖d_κ‖²/Σ‖…‖²" does not say whether it uses P-weights over valid perturbations. State it (P(a·u)-weighted, valid set, per s), and report the unweighted version.
- **S-m4. Rank tolerance (E35-7).** O3 needs a frozen numerical-rank rule, for example σ_i/σ₁ > 10⁻⁸ as in the PR #5 E3 rule, to separate "unresolved" from "resolved low rank". O7's σ₃/σ₁ ≤ 10⁻¹⁰ is a fixture expectation, not that rule.
- **S-m5. Compute estimate undercounted, though still plausible.**
  - O4/O5 needs Φ at b_a, b_a + Δ and b_a + Δ_μ for 16 × 16 × 128 × 3 = 98,304 cells, so about 197k propagations, not 98k.
  - O6 and O7 each need 6 × 16 × 2 × 3 × 8 × 16 = 73,728 cells. With Pred_full, Pred_μ and the actual response, that is about 4.4×10⁵ propagations.
  - Each 4-state, 8-step propagation is a few small matrix-vector products. Even in pure Python, at about 50–100 µs each, the total is under about 1 minute. Vectorized it is seconds. Exact Fractions for 256 histories is negligible. The total is well within 10 minutes (paper estimate, UNVERIFIED until run).
  - Fix the counts. Write per-step outputs incrementally so that "preserve completed outputs" holds.
- **S-m6. The two accounting rules differ.** A guard failure is "counted in the denominator as failed". A belief-invalid edit is "counted and excluded from scoring", and its denominator status is unclear. Freeze one rule for both (E35-4), for example: both stay in the denominator, both are unscored, and both count toward the 25% UNRESOLVED rule.
  - Add a rule for native saturation: if the unedited h₄ already has |h_i| ≥ 0.999, apply the guard to |h_i + δ_i| relative to native, or declare it. Otherwise every edit in that cell fails.
  - The 0.999 guard and the p ≥ 10⁻⁶ validity rule are otherwise reasonable conventions.
- **S-m7. Holdout tabulation.**
  - The split citation is confirmed. PR #7 §0.1 L31 inherits "h is TEST iff ((h mod 16) + ⌊h/16⌋) mod 4 = 0". Hand check: TEST ⇔ (a + u) mod 4 = 0, which gives 4 TEST continuations per prefix and 64 in all. ✔
  - PR #7 also defines a VAL subset (L55, L131): (p + u) mod 4 = 2 and u ≠ (2 − p) mod 16. Whether F-TRAINED's readout training rejected VAL is **UNVERIFIED** (L140 refers to the tuned-rival sampler). Tabulate VAL membership too, as descriptive.
- **S-m8. MARG wording.** "MARG = the cross-stream marginal-update component" (L30) labels the whole q_X, q_Y group. Only its κ-attributable part is cross-stream; μ-edit responses are own-stream. Reword as "marginal forecasts; their κ-attributable part arises only through other-stream readings".
- **S-m9. Package order.** "Each must pass before the next" is undefined for the report-only steps O3 and O5. Measurement also runs before the O6/O7 pipeline fixtures. Reorder to O1, O2, O6, O7 (fixtures, stop on failure), then O3, O4, O5 (report). Headroom numbers then never come from an invalidated pipeline.
- **S-m10. O7 details.**
  - Flip symmetry is assumed. κ is odd under X-flip and under Y-flip, while μ_x and μ_y flip one at a time. A P-weighted least-squares quadratic over flip-invariant data therefore keeps only the μ_x·μ_y term. So in effect g = β·μ_x·μ_y, with Dg = β(μ_y, μ_x). This is my hand derivation from the stated identities, UNVERIFIED numerically.
  - Add a validity accounting rule for O7's off-manifold charts.

## 4. Answers to the specific checks

**Q2, headroom thresholds.**
- They were fixed before computation (attested), so they cannot be gamed after O5.
- They are set apart from the inference floors: the relative 10% and 0.25 floors in §6 are separate from the absolute √H in §5. ✔ (E34-6)
- They are declared conventions. Only the ALL threshold has a scale story, and it is loose (S-m2).
- H is **not** the right headroom quantity for Astra's comparator. H* is (S-M2).
- The decision is purely oracle-side. ✔

**Q3, O7.**
- The quadratic is one arbitrary member of an infinite family. Any smooth g can interpolate the 16 distinct stage-4 marginal keys exactly (PR #4: 16 distinct keys, exact lookup). Astra L38, verbatim: "A finite lookup has no uniquely specified derivative off its keys."
- So O7 cannot test the rival. It is still useful, and it is sanctioned: L189 lists "explicitly defined restricted-rival fixtures". It shows concretely that a rank-2 system can produce a κ-row gain (E35-2), and it checks the rank pipeline.
- It is correctly labelled comparator-only with no exclusion (L79). Keep it. Add "one restricted extension among infinitely many; no inference about other g".
- It is not needed for any claim, and per Q3 R-MF-A is needed only before an exclusion claim.

**Q4, units.** Oracle edits are in standardized chart units and neural edits in absolute hidden-state units. They are distinct, as E35-9 requires. ✔ The neural ε is fixed now, before any precheck and without B or checkpoint data, so the m2 condition is met. ✔ The guard and validity rules are sensible, subject to S-m6. The remaining issue is the ε range (S-M5).

**Q5, folds.**
- 4 orbits split into 2+2 three ways (AB|CD, AC|BD, AD|BC). Each split has 2 directions, giving **6 directed folds**. ✔
- Twelve ordered orbit pairs and four leave-one-out folds are different designs, which Astra did not pick (L186).
- The orbits check by hand: X readings are bits 0 and 2, so mask 5; Y readings are bits 1 and 3, so mask 10. 0→{0,5,10,15}, 1→{1,4,11,14}, 2→{2,7,8,13}, 3→{3,6,9,12}. ✔
- The fold is fitted on 8 prefixes. Each prefix is evaluated in 3 folds, which are dependent.
- The shared-continuation wording is bounded correctly (L23, E35-8). ✔

**Q6, the O1 replay and O6.**
- The file exists and its sha256 matches. It holds exact terminal rationals but **no stage-4 beliefs** (S-m1).
- O6's analytic expectations are stated in advance and are correct by construction:
  - z = Q·D⁻¹(chart − mean) with orthonormal Q gives J = L·D·Qᵀ, so B = D·Qᵀ;
  - Pred_full then equals the actual response, and the gain equals the comparator's loss.
- The tolerances (10⁻⁹ and 10⁻¹²) are plausible for float64 at these scales. Also add the comparator loss as the H* output (S-M2).

**Q7, compute.** It is plausible within the cap, but the counts are undercounted (S-m5). The stop rules, no-retry rule and INCOMPLETE handling conform. The dry run must count against the cap and happen only after freeze and application (S-M3).

**Q8, outputs and wording.** MARG, XOR and ALL are separated. The XOR-only wording rule is present but incomplete (S-M6, S-m8). The claim ceiling is oracle-only, and there are no neural, Q-LEARN, S12, S15, C4 or consciousness statements. ✔ The inference-side wording must stay inside Astra's closing paragraph (L198) and E35-1.

## 5. What this review does not do

It runs nothing and changes no file or label. Whether k = 4 meets headroom is **UNVERIFIED**, because it needs the package.
