# C-κ oracle-only scope record v1 (DRAFT for review; not frozen, not approved, nothing run)

Constitutive agent, 2026-10-22. This record implements step (2) of the Specialist's order after Astra #35 (`/workspace/astra_consult35_response.txt`, sha256 `563e070c…`). It is governed by planning note v1.3 (`next_causal_question_planning_note_v1_3.md`, sha256 `57899307…`), which applies E35-1 to E35-12 verbatim.

**Scope:** oracle computations only, using exact rational arithmetic and float64. **No checkpoint, weight file or training artifact is opened or loaded.** No code exists yet. The code and manifest are written and frozen only after the Delegate and Astra have reviewed this record, and the Research Lead then files the standing-approval application. Every number below is fixed *before* any computation.

## 1. World, chart and event order (frozen, inherited)
- **World.** W2, as in `TWOSTREAM_PROTOCOL_v1.md` (PR #4; results.json sha256 `bf2de92c…`).
  - Hidden state (X, Y). Uniform initial law.
  - Transition: X' = X⊕C⊕Dx, Y' = Y⊕C⊕Dy, with C ~ Bern(1/5), Dx ~ Bern(1/50), Dy ~ Bern(1/40).
  - Readings follow the order X, Y, X, Y, X, Y, X, Y, each through BSC(1/5).
  - History integer h stores reading 1 in bit 0. State index s = X + 2Y.
- **Event order.** The stage-k belief is the posterior after reading k and before the transition. For k < 8, the transition follows. The terminal forecasts are taken from the stage-8 belief, with no transition after reading 8.
- **Stage: k = 4 only.** The belief is the posterior after readings X, Y, X, Y. The continuation u is readings 5–8 (X, Y, X, Y), giving 16 continuations, and h = a + 16·u. There is no stage substitution (v1.3 §2).
- **Chart.** (μ_x, μ_y, κ), with μ = 1 − 2m and κ = 4c. The inverse chart is p11 = m_x m_y + c, p10 = m_x(1 − m_y) − c, p01 = (1 − m_x)m_y − c, p00 = (1 − m_x)(1 − m_y) + c (`TWOSTREAM_PROTOCOL_v1.md`, Coordinates).
- **Oracle continuation map.** Φ(b, u) = (q_X, q_Y, q_XOR) at stage 8, starting from the stage-4 belief b. It is computed by the four-state filter: three transitions and four readings. Φ is a ratio of linear functions of b.

## 2. Prefixes, orbits, folds and splits
- **Prefixes.** a ∈ {0..15}, the four-reading prefixes. b_a is the exact stage-4 posterior of each.
- **Orbits.** The flip group is {id, flip-X (mask 5), flip-Y (mask 10), both (mask 15)}. The orbits are A{0,5,10,15}, B{1,4,11,14}, C{2,7,8,13} and D{3,6,9,12}. These match the v1.3 audit groups, and the fixture checks that the group acts freely.
- **Folds.** There are six directed two-group folds: a fit pair, and its complement as the evaluation pair (AB→CD, CD→AB, AC→BD, BD→AC, AD→BC, BC→AD).
  - Every evaluation pair is a whole set of orbits.
  - Continuation strings are shared between fit and evaluation, so this is **not** unseen-continuation generalization (E35-8).
- **Predictor-training split** (inherited from the PR #5 §3 rule, which PR #7 cites as unchanged; the reviewer should confirm that citation): h ∈ TEST ⇔ ((h mod 16) + ⌊h/16⌋) mod 4 = 0, which is (a + u) mod 4 = 0.
  - Every prefix therefore has exactly 4 TEST continuations out of 16.
  - The package tabulates TRAIN/TEST membership for every (a, u) in every fold. This is descriptive and does not gate anything. Prefix holdout, continuation holdout and predictor-training holdout are reported as three separate things (E35-8).

## 3. Outputs and weights
- **Output groups, reported separately everywhere:**
  - **MARG** = (q_X, q_Y): the cross-stream marginal-update component;
  - **XOR** = q_XOR: the direct XOR response;
  - **ALL** = the three outputs together.
  - An XOR-only effect is never reported as cross-stream marginal updating (Astra #35, order step 3).
- **Weights.** w(a, u) = P(a·u), the exact history probability, renormalized within the evaluated set. Unweighted values are reported alongside (as note n2 of the v1.3 audit asked).
- **Loss.** Weighted squared error per output, summed within each group. Each bound names its target, norm, weighting and domain (E35-6).

## 4. Package contents (O1–O7, in order; each must pass before the next)
- **O1. World, chart and split fixtures.**
  - Recompute the 256 terminal oracle forecasts and the 16 stage-4 beliefs in exact rationals. They must match the frozen PR #4 `results.json` exactly, or to its 50-digit truncation where only that is stored.
  - The chart must round-trip exactly.
  - The flip identities must hold: (μ_x, μ_y, κ) → (−μ_x, μ_y, −κ) under X-flip, with P(h) preserved.
  - The orbit groups must equal A–D. The split counts must be 64 TEST and 192 TRAIN.
- **O2. Derivative checks.**
  - L(a, u) = ∂Φ(b_a, u)/∂(μ_x, μ_y, κ) is computed in closed form, using the quotient rule on the linear filter.
  - It is checked against central finite differences with step 10⁻⁶. The tolerance is a maximum absolute difference of 10⁻⁸ per entry.
- **O3. Template separation (descriptive, E35-6).**
  - For each a, stack L(a, ·) over the 16 continuations, separately for MARG (32×3), XOR (16×3) and ALL (48×3).
  - Report the singular values and the principal angle between the κ column and span{μ_x column, μ_y column}.
  - These are reported, not asserted as bounds on any neural statistic.
- **O4. Finite oracle perturbation validity.**
  - **Units:** standardized chart units. Δ = D·s·r, where D = diag(σ_μx, σ_μy, σ_κ) holds the P-weighted standard deviations over the 16 reachable b_a. This rule is frozen; its values are computed in the package.
  - **Directions:** 64 unit vectors r in R³, drawn once with NumPy PCG64 seed 35004, plus their negatives.
  - **Magnitudes:** s ∈ {0.1, 0.25, 0.5}.
  - **Validity:** a perturbed belief is valid iff all four p ≥ 10⁻⁶.
  - **Accounting:** invalid perturbations are counted in the denominator and reported by magnitude. They are never replaced (E35-4 analogue).
- **O5. Oracle headroom (exact finite differences).**
  - For each valid (a, u, r, ±, s), compute the κ-attributable difference d_κ = Φ(b_a + Δ, u) − Φ(b_a + Δ_μ, u), where Δ_μ is Δ with its κ component set to 0.
  - H_G(s) is the weighted mean of ‖d_κ‖² within group G. It is the baseline squared error of an *exact* fixed-κ comparator under oracle-unit edits, so it is the maximum squared-error gain available to the full model at oracle scale (E35-6).
  - It is labelled oracle-scale only. The neural gain bound is the fitted comparator's own loss, which depends on the checkpoint (E35-9).
  - The share R_G(s) = Σ‖d_κ‖² / Σ‖Φ(b_a + Δ) − Φ(b_a)‖² is also reported.
- **O6. Positive implementation control (E35-5).**
  - Synthetic state z = Q·D⁻¹(chart − chart̄). Q is 8×3 with orthonormal columns, drawn once with seed 35006, so the coordinates are well-conditioned (cond = 1 in standardized units).
  - The readout is Φ applied to the chart recovered from z.
  - Fit B per fold by the J ≈ L·B least squares of v1.1 §B.1, stacked over the fold's fit prefixes and all continuations, with no ridge penalty.
  - Score finite edits δ = ε·v, using 16 unit v ∈ R⁸ (seed 35016), both signs and ε ∈ {0.02, 0.05, 0.1}, on the evaluation prefixes. Compare Pred_full against the control's actual response.
  - **Declared expectations:**
    - B = D·Qᵀ to a maximum absolute difference ≤ 10⁻⁹;
    - Pred_full prediction error ≤ 10⁻⁹ (max absolute difference) on every valid edit;
    - the gain over the separately fitted B_μ equals that comparator's loss to within 10⁻¹².
  - **Failure means PIPELINE INVALID, and the package stops.**
- **O7. Restricted rival fixture (comparator, E35-2 and E35-5).**
  - Two-coordinate smooth lookup: z = Q₂·(standardized μ_x, μ_y), with Q₂ 8×2 drawn by seed 35007.
  - Its forecasts are Φ at chart(μ_x, μ_y, g(μ_x, μ_y)). Here g is the P-weighted least-squares quadratic in (μ_x, μ_y) fitted to the 16 reachable (μ, κ). This supplies its off-manifold extension explicitly.
  - **Reported:**
    - the stacked-Jacobian singular values (expected rank 2, with σ₃/σ₁ ≤ 10⁻¹⁰);
    - the gain of the full model over B_μ under the same O6 edits (descriptive; it shows that a rank-2 system can produce a "κ-row gain");
    - its reachable-set forecast error against the oracle.
  - **Expectation:** a rank-2 Jacobian. Anything else is PIPELINE INVALID.
  - **Interpretation:** this is a comparator only. No exclusion of the rival follows from any outcome of this package.
- **Not in this package:**
  - R-MF-A, the mean-field controller (E35-11, unevaluated);
  - any rival-L panel;
  - any checkpoint quantity.

## 5. Headroom criterion at k = 4 (fixed now, E34-6, E35-7)
- **Primary rule:** k = 4 **meets oracle headroom** iff both hold at s = 0.25:
  - √H_ALL ≥ 1×10⁻³ and R_ALL ≥ 0.05;
  - at least 75% of the O4 perturbations at s = 0.25 are valid.
- **MARG-claim rule:** the cross-stream marginal claim is *available* to the later inference study iff √H_MARG ≥ 1×10⁻⁴ at s = 0.25.
  - Otherwise, that claim is pre-declared **unavailable**. The XOR or ALL result can then be reported only as such.
- **If the rule fails:** the report reads **"HEADROOM NOT MET at k = 4"**, with no mechanism-absence inference and no stage substitution.
- **Rationale for the thresholds:**
  - 10⁻³ RMS is about 1/20 of a well-trained network's per-output RMS error: √(E_total/3) ≈ 2×10⁻² at E_total ≈ 1.16×10⁻³, the PR #5 CAND GRU-8 minimum, used as a scale only. It was set without computing H.
  - 0.05 means κ carries at least 5% of the finite response under isotropic standardized edits.
  - The reviewer may challenge these numbers; they cannot be changed after O5 is computed.

## 6. Frozen now, for the later inference study only (m2, E35-4, E35-9; not executed here)
- **Edits.**
  - Native post-reading-4 GRU hidden state h₄ ∈ (−1, 1)⁸, Euclidean metric.
  - 16 unit directions per seed: PCG64 seed 36000 + seed_id, shared across prefixes and folds.
  - Both signs. ε ∈ {0.02, 0.05, 0.1}, absolute, not rescaled per checkpoint.
- **Saturation guard.** An edited state with any |h_i| ≥ 0.999 is a guard failure. It is counted in the denominator as failed and never replaced.
- **Belief validity.** An edit whose b_a + B·δ has any p < 10⁻⁶ is invalid. It is counted and excluded from scoring.
  - If invalid plus guard failures exceed 25% for a seed and fold at a given ε, that cell is UNRESOLVED and remains in the denominator.
- **Proposed inference floors** (to be frozen with the inference spec, but recorded here to keep the floor separate from the headroom):
  - gain over B_μ ≥ 10% of B_μ's held-out loss;
  - the full model's normalized held-out error Σ‖Pred_full − ΔF‖² / Σ‖ΔF‖² ≤ 0.25.
  - Both apply per seed and per group. The ALL group is primary; MARG counts only if available under §5.

## 7. Resources, stop rules and outputs
- **Cap:** 1 CPU process, no GPU, a 4 GB address space and 10 cumulative wall-clock minutes, including setup and verification. No automatic retries.
- **Estimate:** O4 and O5 need 16 × 16 × 128 × 3 ≈ 98k four-state filter propagations. O6 and O7 need 6 folds × 16 × 2 × 3 × 8 × 16 ≈ 74k propagations, plus O1's exact-rational replay of 256 histories. That is well under 1 minute in NumPy and Fractions. The estimate is to be confirmed by a timed dry-run of the frozen code on O1 only, as part of the freeze.
- **Stop rules:**
  - Any O1, O2, O6 or O7 fixture failure means STOP and report PIPELINE INVALID, with no fix-and-rerun under this record.
  - Reaching the cap means STOP. Completed per-step outputs are preserved, and the result is reported as INCOMPLETE.
  - O3 and O5 have no stopping thresholds; they report.
- **Outputs:** one `results.json` with every number above; a `REPORT.md` that does not interpret beyond §5; a manifest with sha256 hashes of code, inputs (PR #4 `results.json`) and outputs; and the run log.
- **Next step after the run:** the report goes to the room and to Astra *before* any inference spec is drafted.

## 8. Claim ceiling of this package
This package states only oracle facts: the derivatives, template geometry, finite-perturbation validity and headroom at k = 4, and the behavior of two synthetic fixtures. It makes no neural, acquisition, mechanism, S12, S15, C4 or consciousness statement.
