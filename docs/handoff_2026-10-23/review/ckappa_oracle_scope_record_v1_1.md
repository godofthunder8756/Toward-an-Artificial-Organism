# C-κ oracle-only scope record v1.1 (DRAFT for Astra review. Not frozen, not approved, nothing run)

Constitutive agent, 2026-10-22. **Additive.** v1 (`ckappa_oracle_scope_record_v1.md`, sha256 `1b450bcf…`) is unchanged. v1.1 is a complete replacement text, and the freeze and Astra's review use v1.1 only.

It addresses:
- the Delegate's review `ckappa_oracle_scope_record_v1_adversarial_review_RD.md` (`6dbf3deb…`), accepted in full: S-M1–S-M6 and S-m1–S-m10;
- the Specialist's step-0 timing ruling.

It is governed by Astra #35 (`563e070c…`) and planning note v1.3 (`57899307…`, E35-1..12 verbatim).

**Scope:** oracle computations only. **No checkpoint, weight file or training artifact is opened or loaded.** No code exists yet. Every number below is fixed before any computation, and nothing executes until the manifest is sealed and the Research Lead's standing-approval application is filed.

**Fix map**

| Item | Fix | § |
| --- | --- | --- |
| S-M1 | Four transitions from stage 4 to stage 8. O1 reproduces all 256 terminal forecasts through Φ(b_a, u) | 1, 4 |
| S-M2 | Headroom is H\*, the held-out loss of the *fitted* fixed-κ comparator on the exact-filter control. H is descriptive only | 4 (O6), 5 |
| S-M3 + Specialist | No pre-freeze dry-run. Step 0 is a timing check after the seal, counted in the cap | 7 |
| S-M4 | κ-component accuracy floor (L_full ≤ ½·L_μ), claim unit, quota, and fold-dependence stated | 6 |
| S-M5 | ε = 0.25 added. Counted sizes are {0.1, 0.25}; {0.02, 0.05} are descriptive | 4 (O6), 6 |
| S-M6 | Cross-stream marginal wording requires MARG to be available and to pass its own floors | 5, 6 |
| S-m1 | results.json at commit `5d9d8a7`. Beliefs are verified through forecasts, not matched directly | 1, 4 |
| S-m2 | Thresholds labelled as declared conventions. R_MARG added | 5 |
| S-m3 | R_G weighting stated | 4 (O5), 5 |
| S-m4 | Frozen three-band numerical-rank rule | 4 |
| S-m5 | Compute estimate corrected | 7 |
| S-m6 | One accounting rule for guard and validity failures. Pre-saturated units handled | 6 |
| S-m7 | PR #7 VAL membership tabulated as descriptive | 2 |
| S-m8 | MARG label | 3 |
| S-m9 | Fixtures O1, O2, O6, O7 before measurements O3–O5 | 4 |
| S-m10 | O7 is comparator-only, with a disclaimer. The symmetry reduction is reported, not assumed | 4 (O7) |
| E35-10 note | Threshold rationale no longer scaled on PR #5 | 5 |

## 1. World, chart and event order (frozen, inherited)
- **World.** W2 as in `TWOSTREAM_PROTOCOL_v1.md`, with frozen values in PR #4 `twostream_results_v1/results.json` at commit `5d9d8a7`. The local copy's sha256 is `bf2de92c…`; the freeze re-hashes it from that commit.
  - Uniform initial law on (X, Y).
  - Transition: X' = X⊕C⊕Dx, Y' = Y⊕C⊕Dy, with C ~ Bern(1/5), Dx ~ Bern(1/50) and Dy ~ Bern(1/40).
  - Readings come in the order X, Y, X, Y, X, Y, X, Y, each through a BSC(1/5).
  - h stores reading 1 in bit 0, and s = X + 2Y.
- **Event order.** The stage-k belief is the posterior after reading k and before the transition. For k < 8 a transition follows. Terminal forecasts come from the stage-8 belief.
- **Stage k = 4 only.** From the stage-4 belief to the stage-8 belief, the sequence is **transition, reading 5, transition, reading 6, transition, reading 7, transition, reading 8**. That is **four transitions** and four readings. Continuation u covers readings 5–8 (16 continuations), and h = a + 16·u. No stage is substituted.
- **Chart.** (μ_x, μ_y, κ), with μ = 1 − 2m and κ = 4c. The inverse chart is the one in `TWOSTREAM_PROTOCOL_v1.md` under "Coordinates".
- **Φ(b, u).** The terminal (q_X, q_Y, q_XOR) obtained by running the four-state filter from stage-4 belief b along continuation u. It is a ratio of linear functions of b.

## 2. Prefixes, orbits, folds and splits
- a ∈ {0..15}, with b_a the exact stage-4 posterior.
- The flip group uses masks {0, 5, 10, 15}. Its orbits are A{0,5,10,15}, B{1,4,11,14}, C{2,7,8,13} and D{3,6,9,12}, and the fixture checks that the action is free.
- **Folds.** Six directed folds: AB→CD, CD→AB, AC→BD, BD→AC, AD→BC and BC→AD. That is three 2+2 splits, each run in both directions.
- **Fold dependence.** Each prefix is an evaluation prefix in 3 of the 6 folds, so folds are not independent. Continuation strings are shared between fit and evaluation (E35-8).
- **Predictor-training splits, tabulated for every (a, u) and fold; descriptive only:**
  - PR #5 §3 TEST: (a + u) mod 4 = 0.
  - PR #7 VAL: (a + u) mod 4 = 2 and u ≠ (2 − a) mod 16, from PR #7 L55 and L131 as quoted by the Delegate. Whether F-TRAINED's readout training rejected VAL is UNVERIFIED.
  - Prefix holdout, continuation holdout and predictor-training holdout are reported separately.

## 3. Outputs and weights
- **Groups:**
  - **MARG** = the marginal-forecast component (q_X, q_Y);
  - **XOR** = the direct XOR forecast q_XOR;
  - **ALL** = all three outputs.
  - They are reported separately everywhere.
- **Weights.** w(a, u) = P(a·u), renormalized within the evaluated set. Directions, signs and edit magnitudes are weighted uniformly. Unweighted values are reported alongside.
- **Loss.** Weighted squared error summed within each group. Every bound names its target, norm, weighting and domain (E35-6).

## 4. Package: execution order O1 → O2 → O6 → O7 → O3 → O4 → O5
Fixtures come first. A failure in any fixture means **STOP and report PIPELINE INVALID**.

**Rank rule (frozen, used throughout; E35-7).** For singular values σ_i/σ_1:
- **> 10⁻⁶:** resolved;
- **< 10⁻¹⁰:** resolved zero;
- **between the two:** NUMERICALLY UNRESOLVED.

An unresolved rank in a fitted design (B or B_μ) makes that seed × fold cell UNRESOLVED; it is counted, not dropped.

- **O1. World, chart and split fixtures.**
  - Compute the 16 stage-4 beliefs in exact rationals.
  - Φ(b_a, u) must reproduce all 256 terminal forecasts stored in `results.json` exactly (rational equality, or the stored 50-digit truncation).
  - The chart must round-trip exactly, and the flip identities and P(h) invariance must hold.
  - Orbits A–D, and split counts of 64 TEST and 192 TRAIN.
- **O2. Derivatives.**
  - The closed-form L(a, u) = ∂Φ/∂(μ_x, μ_y, κ) must agree with central differences at step 10⁻⁶ to a maximum absolute difference of 10⁻⁸.
- **O6. Positive implementation control (E35-5).**
  - Synthetic state z = Q·D⁻¹(chart − chart̄), where D is the P-weighted chart standard deviations over the 16 b_a and Q is an 8×3 matrix with orthonormal columns (seed 35006). The readout is Φ applied to the chart recovered from z.
  - Per fold, fit B (rank 3) and B_μ (rank 2, fixed κ) by stacked Jacobian least squares over the fit prefixes and all continuations, with no ridge.
  - Edits: δ = ε·v, using 16 unit vectors v ∈ R⁸ (seed 35016), both signs, ε ∈ {0.02, 0.05, 0.1, 0.25}, on the evaluation prefixes.
  - Predictions:
    - Pred_full = Φ(b_a + Bδ) − Φ(b_a);
    - Pred_μ = Φ(b_a + B_μ-induced marginal change, κ fixed) − Φ(b_a).
  - **Expectations (frozen):**
    - B = D·Qᵀ to ≤ 10⁻⁹ maximum absolute difference;
    - Pred_full error ≤ 10⁻⁹ on every valid edit.
  - **Headroom quantity:** H\*_G(ε), the weighted held-out loss of Pred_μ against the control's actual response, pooled over folds. This is the gain actually available against the fitted comparator (S-M2). R\*_G(ε) = H\*_G divided by the weighted Σ‖actual response‖².
  - **Label:** oracle-scale under synthetic coordinates. The neural gain bound is the fitted comparator's own loss, which depends on the checkpoint (E35-9).
- **O7. Restricted rival fixture (comparator only).**
  - z = Q₂·(standardized μ_x, μ_y), with Q₂ 8×2 drawn by seed 35007.
  - Forecasts are Φ at chart(μ_x, μ_y, g(μ_x, μ_y)), where g is the P-weighted least-squares quadratic fitted to the 16 reachable (μ, κ).
  - Reported:
    - g's fitted coefficients, including whether flip symmetry reduces it to β·μ_x·μ_y, as the Delegate derived by hand; this is reported, not assumed;
    - the stacked-Jacobian singular values, where rank 2 is expected under the rank rule and anything else is PIPELINE INVALID;
    - the O6-protocol gain over B_μ;
    - the reachable-set forecast error.
  - **Disclaimer:** this fixture is *one* explicit smooth two-coordinate system. It is not the reachable-set lookup; a smooth g of sufficient flexibility fits all 16 keys exactly. It cannot test or exclude the lookup rival, and no exclusion follows from any of its outcomes (E35-2).
- **O3. Template geometry (descriptive).**
  - Singular values per a of the stacked L for MARG (32×3), XOR (16×3) and ALL (48×3).
  - The principal angle θ between the κ column and the marginal columns.
- **O4. Oracle-unit perturbation validity.**
  - Δ = D·s·r, with 64 unit vectors r ∈ R³ (seed 35004), both signs, s ∈ {0.1, 0.25, 0.5}.
  - A perturbation is valid iff all four p ≥ 10⁻⁶. Invalid perturbations are counted in the denominator and never replaced.
- **O5. Naive κ difference (descriptive only).**
  - H_G(s) is the weighted mean of ‖Φ(b_a + Δ) − Φ(b_a + Δ with κ zeroed)‖². R_G is H_G divided by the weighted mean of ‖Φ(b_a + Δ) − Φ(b_a)‖², with the §3 weights.
  - **Not a headroom or a bound.** It ignores the part of the κ response that the comparator absorbs (≈ H·sin²θ to first order).

## 5. Headroom criterion at k = 4 (declared conventions, fixed before computation; E34-6, E35-7)
The thresholds are declared conventions. They are not derived from any checkpoint, and they cannot be changed after O6 is computed.
- **ALL headroom met** iff, at **ε = 0.1** (the smallest counted size):
  - √H\*_ALL ≥ 1×10⁻³;
  - R\*_ALL ≥ 0.05;
  - at least 75% of O6 edits are valid.
- **MARG claim available** iff, at ε = 0.1:
  - √H\*_MARG ≥ 1×10⁻⁴;
  - R\*_MARG ≥ 0.02.
  - Otherwise the inference study may report MARG only descriptively.
- **If ALL is not met:** the result reads "HEADROOM NOT MET at k = 4". No mechanism-absence inference is drawn, no stage is substituted, and no inference spec is drafted without a new ruling.

## 6. Frozen now for the later inference study (not executed here; m2, E35-3, E35-4, E35-9)
- **Edits.**
  - Native post-reading-4 GRU hidden state h₄ ∈ (−1, 1)⁸, Euclidean metric.
  - 16 unit directions per seed (PCG64 seed 36000 + seed_id), shared across prefixes and folds.
  - Both signs. ε ∈ {0.02, 0.05, 0.1, 0.25}, absolute.
  - **Counted toward the outcome:** ε ∈ {0.1, 0.25}. ε ∈ {0.02, 0.05} are descriptive and serve as linear-regime references.
  - Descriptive edit families: κ-directed, null(B), row(B), chord and equal-impact edits.
- **Accounting (one rule).**
  - An edit fails its guard if it moves any unit from |h_i| < 0.999 to |h_i| ≥ 0.999, or increases |h_i| for a unit already at |h_i| ≥ 0.999. Pre-saturated units are tabulated.
  - An edit is belief-invalid if b_a + Bδ, or the B_μ counterpart, has any p < 10⁻⁶.
  - **Both kinds count in the denominator as failed predictions.** They are never replaced or excluded.
  - A seed × fold × ε cell with more than 25% failures is UNRESOLVED.
- **Per-seed pass, per group G, at each counted ε.** All three must hold:
  - **(a)** the gain L_μ − L_full ≥ ½·L_μ, i.e. the full model removes at least half of the comparator's held-out loss (this is the κ-component accuracy floor, S-M4);
  - **(b)** the normalized full error Σ‖Pred_full − ΔF‖² / Σ‖ΔF‖² ≤ 0.25;
  - **(c)** the rank rule is resolved for B and B_μ.
  - Pooling is over the 6 folds' evaluation sets, with each (fold, prefix) cell weighted by §3. The fold dependence is disclosed.
- **Claim unit:** the F-TRAINED seed (10).
  - **POSITIVE (ALL):** at least 8/10 seeds pass ALL at both counted ε.
  - **NOT SHOWN:** at most 2/10.
  - **UNRESOLVED:** more than 2 UNRESOLVED seeds.
  - **MIXED:** otherwise.
  - **Cross-stream marginal wording** requires MARG to be available under §5 *and* MARG POSITIVE by the same quota. Otherwise the result reads "ALL-group response prediction; marginal component not shown" (S-M6).
  - cand_final and F-INIT are descriptive (E35-10). The wording ceiling is Astra #35's closing paragraph.

## 7. Resources, step 0 and stop rules
- **Cap:** 1 CPU process, no GPU, a 4 GB address space and 10 cumulative wall-clock minutes, including setup, verification and step 0. No automatic retries.
- **Step 0** (after the manifest seal and the filed application; S-M3): time O1, project the total from the declared propagation counts, and HALT and report if the projection exceeds 10 minutes.
- **Paper estimate (UNVERIFIED):**
  - O4: 16 × 16 × 128 × 3 ≈ 9.8×10⁴ propagations;
  - O6 and O7: 2 systems × 6 folds × 8 evaluation prefixes × 16 continuations × 32 edits × 4 ε × 2 predictions ≈ 3.9×10⁵;
  - O5, Jacobians and finite differences: ≈ 1×10⁵;
  - total ≈ 6×10⁵ four-state propagations, each a handful of 4×4 operations. That is expected to take well under 1 minute.
- **Stop rules:**
  - A fixture failure (O1, O2, O6, O7) means STOP and report PIPELINE INVALID, with no fix-and-rerun under this record.
  - Reaching the cap means STOP, with completed outputs preserved and the result reported as INCOMPLETE.
  - O3–O5 report only.
- **Outputs:** `results.json`; `REPORT.md`, which makes no interpretation beyond §5; a manifest with sha256 hashes of the code, the inputs and the outputs; and the run log. The report goes to the room and to Astra before any inference spec is drafted.

## 8. Claim ceiling
The package states oracle facts only: the event-order and forecast fixtures, derivatives, template geometry, perturbation validity, and headroom against the fitted fixed-κ comparator at k = 4, plus the behavior of the two synthetic fixtures. It makes no neural, acquisition, mechanism, S12, S15, C4 or consciousness statement.
