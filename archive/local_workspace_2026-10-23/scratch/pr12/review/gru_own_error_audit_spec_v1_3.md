# GRU hidden-state oracle-accessibility audit: specification v1.3 (FINAL)

2026-10-21, ~10:40 PM ET. New file and additive. It is derived from v1.2 (`gru_own_error_audit_spec_v1_2.md`, sha256 `8c81d32070ba12ef94af7adbc3d224661ae4c76ddacb7239d170564e2eb4fdcd`, unchanged). v1 (`c0fad75a18b867622b75187a75a023f8c6684a02822ee2771292b268d61452a1`), v1.1 (`4661a8895ef495c28a1a41ff7405f029ff3c9f4451a12b1a1af9ccc701641ccf`), v1.2 and all earlier check scripts are not edited.

**Status: FINAL text.** Astra #33 verdict (L1, verbatim): "Verdict: FREEZE WITH NAMED EDITS." This file applies those named edits. It becomes the frozen spec when it is sealed in the implementation manifest (§0).

Inputs, all verified by sha256 (§14):
- Astra #33: `/workspace/astra_consult33_response.txt`, sha256 `d98549a85bb2562a31a0e6f15dca072412beba09a47d255c2746f3f0d837981f`. "L*n*" without a prefix below means line *n* of this file.
- Astra #32: `/workspace/astra_consult32_response.txt`, sha256 `99378f762fe2a21ae519b1a8368ab52b48339cba9e2477c94884cf49f9f7df7b`. Its lines are cited as "#32 L*n*".
- CNA v1.2 delta review: `gru_own_error_audit_spec_v1_2_delta_review.md`, `e8f28370eaf508909029c696d2428ed9419781eaa3157880e7604ce331276502`.
- CNA geometry script cited by the delta review: `/workspace/scratch/gru_v12_delta/rank_check.py`, `61a3e4243c45a897253022a3351c19c0f8aac6248faff6a775d5a11f9a64811d` (input bits only).
- Earlier CNA documents: v1 review `f6b2db6f…`, v1.1 addendum `721100d1…`, erratum c32 `4a5ad4f3…`.

Astra #33 L5 says Astra has "not independently verified the artifacts or hashes". They are re-verified by script here (§14).

## 0. Status, scope and claim ceiling

**Verdict being applied.** Astra #33 L1: "Verdict: FREEZE WITH NAMED EDITS." L5: "This clears the bounded oracle-accessibility audit, not the earlier own-error interpretation."

**Not executable until** (L123) all of the following are done:
1. This v1.3 text, the roster (`gru_own_error_audit_roster_v1.json`, `7ad145b4…`) and an implementation manifest are sealed. The manifest lists the code files and their hashes, plus the frozen source-field map of §6.
2. The Research Lead records the application of `PI_STANDING_APPROVAL_2026-10-21_1515.md` (`5cc6f12a…`) to the sealed set.

Astra #33 L123: "No duplicate approval question or further scientific review cycle is needed unless implementation introduces a substantive departure."

No checkpoint has been loaded and no inference has run. No q-decoding quantity of any kind, including the input-only B_in+ → q losses of §4, has been computed.

**Reframe (unchanged from v1.2).** The question is bounded accessibility of oracle probabilities from hidden state. A pass shows decoder accessibility only. It does not show error assessment, monitoring or tracking of an assessed predictor, acquisition, causal use, C4, or anything about consciousness.

**Primary question** (#32 L31, verbatim):
> "On the declared held-out history groups, how much does adding hidden state improve prediction of the oracle probabilities beyond the predictor's output and the declared input features?"

Under E33-1, "beyond the declared input features" is read as "beyond the declared input baselines under this split".

**Claim ceiling** (Astra #33 L117, verbatim; identical to #32 L223). This is the strongest permitted positive wording:
> "On the declared W2 history domain and orbit-respecting decoder splits, adding hidden state improved prediction of oracle probabilities beyond the specified output and input baselines by the prespecified margin in the reported checkpoint blocks. This demonstrates bounded decoder accessibility under the declared analysis. It does not establish that the predictors assess or use knowledge of their own errors."

**Appended qualification** (L121, verbatim). It is always printed directly after the ceiling:
> "The comparison is conditional on the declared feature sets, regularization and split. Input-baseline extrapolation and changes in effective shrinkage may contribute to the gain."

"Reported checkpoint blocks" in the ceiling means the (PR, arm) claim-reporting units of §8 (L39). Elsewhere this spec does not use "block". It names claim-reporting units (PR, arm) and integrity-failure units (PR, seed) separately.

**No training.** There are no gradient updates. The only fitted objects are closed-form ridge decoders (§5).

**Why the reframe (unchanged).**
- e_P(h) = Σ_j (f_P,j(h) − q_j(h))² and d_P = f_P − q are exact functions of (f_P, q).
- The v1 review's A2 is cited only together with erratum `4a5ad4f3…`. v1.3 relies on none of the claims that erratum withdraws.

## 1. Roster (unchanged from v1.2)

**PR #5.** #32 L133, verbatim: "PR #5: MISSING PERSISTED CHECKPOINTS; NOT EVALUATED." Nothing is retrained or substituted, and PR #5 is not excluded for performance.

**Scope wording** (#32 L137): "available persisted checkpoints from PRs #7-#10".

**Roster contents.** There are 290 files: 230 TRAINED and 60 INIT. INIT is descriptive only. Roles are fixed by file name, and nothing is excluded on any outcome.

**Duplicates.** The 10 PR #10 init duplicates (CAND init = R-FIX-32 init) are kept for provenance and are not independent evidence (E32-8).

**Frozen-core wording** (#32 L141–L142):
- "f_init can be described as a frozen random recurrent core with a trained readout."
- "R-FIX has frozen W_hh with other core parameters and the readout trained. Its entire recurrent core is not frozen."

Each arm is a separate tier in every table.

## 2. Inputs, weights, target and signed deviation (unchanged from v1.2, except tolerance)

- One hashed 256×8 bit array is passed unchanged to every checkpoint, encoded by the line's `CoreGRU.forward`.
- Each predictor yields a stage-8 state s_P(h) ∈ ℝ⁸ and an output f_P(h) ∈ (0,1)³, computed in float64 from the float32 weights.
- w(h) = P(h) from the W2 certificate (file sha `bf2de92c…`), with Σ_h w(h) = 1. P(h) weighting is primary, and uniform weighting is a descriptive sensitivity.

**Fitted target: q** (E32-2). q(h) = (q_X, q_Y, q_XOR) is fitted jointly as 3 columns with one shared λ. ℓ(h) = Σ_j (q̂_P,j(h) − q_j(h))².

**Signed deviation (constructed, not fitted).** d̂_P = f_P − q̂_P, so Σ_j (d̂_P,j − d_P,j)² = Σ_j (q̂_P,j − q_j)² exactly. The identity is checked numerically as integrity, using the E33-8 tolerance (§6).

**Original predictor's excess Brier risk (new, L79).** For every checkpoint, the report gives
R_exc(P) = Σ_h w(h)·e_P(h) = Σ_h w(h) Σ_j (f_P,j(h) − q_j(h))²,
which is the predictor's own excess Brier risk over the oracle. It is reported next to L(base) and L(full) of §4, and on the same pooled scale: each history is evaluated 3 times, so the 3·Σw pooling of the full domain equals R_exc(P). Astra #33 L79: "A gain over the fitted baseline does not necessarily improve on the original predictor's output." R_exc is descriptive and never a gate.

**Descriptive only.** e_P variation (weighted mean, sd, quantiles) and pairwise corr_w(e_P, e_Q) are not gates. A correlation whose weighted variance is zero for either argument is **UNDEFINED** and is not imputed (E33-8).

## 3. Split (unchanged from v1.2)

- Groups are the G-orbits of the depth-4 prefix, with G = {id, ⊕0x55, ⊕0xAA, ⊕0xFF}: A = {0,5,10,15}, B = {1,4,11,14}, C = {2,7,8,13}, D = {3,6,9,12}. Each group has 64 histories.
- The 3 bipartitions AB|CD, AC|BD and AD|BC are each used in both directions, giving 6 folds. Every history is evaluated in exactly 3 folds.
- Only stage-8 states are decoded.

**Prefix statement** (E32-9; correction credited to the CNA addendum `721100d1…`):
- Lengths 1–2 are necessarily shared.
- Length 3 is shared in 4 of the 6 folds, and the two AC|BD folds share none.
- Lengths ≥ 4 are shared in no fold.
- Short-prefix sharing is not called harmless.

**AC|BD sensitivity** (descriptive, prespecified). The two AC|BD folds are used, with denominator 1 × Σw. It uses fixed λ (§5).

## 4. Primary nested comparisons (E32-3) and input-only losses (E33-4)

**Feature blocks.** All are computed per checkpoint P on the same h.
- **B_conf**: f_P and f_P(1 − f_P). 6 features.
- **B_in+**: the 8 readings as ±1 and all 28 pairwise products. 36 features. **All declared B_in+ features are retained** (L19, E33-4), including r₀r₂ and r₁r₃.
- **STATE**: s_P. 8 features.

| comparison | base | full | features (base → full), each plus intercept |
|---|---|---|---|
| C1 | B_conf | B_conf + STATE | 6 → 14 |
| C2 | B_conf + B_in+ | B_conf + B_in+ + STATE | 42 → **50** |

**Wording (E33-1).** C2 measures improvement **beyond the declared input baselines under this split**. Hidden state is itself computed from the inputs (L13), and the predictors learned from source-study histories that span the decoder's held-out groups, whereas the fitted baseline receives oracle targets only on its fit groups.

**Pooled held-out loss** (E32-7): L(model) = Σ_f Σ_{h ∈ Eval_f} w(h)·ℓ_f(h) / (3·Σ_h w(h)).

**Effect statistics.**
- Gain: Δ_c(P) = L(base) − L(full).
- R² gain: Δ_c(P) / Var_w(q), with Var_w(q) the fixed full-domain value at full precision (§7).
- Foldwise results and AC|BD results are reported separately.
- Interpretation (L23, E33-9): adding correlated state features can change ridge's effective shrinkage on predictions the baseline can already represent. A gain therefore establishes improvement under this feature-and-regularization procedure, not necessarily a larger representable function class.

**Input-only B_in+ → q losses (new; declared here, computed only after the freeze).** A ridge decoder with B_in+ alone (36 features plus intercept) is fitted to q under §5 with the fixed primary λ = 1e-3 and P(h) weighting, on each of the 6 folds. The report gives the held-out loss for each fold and the pooled loss under the E32-7 denominator.
- These losses are checkpoint-independent, so they are computed once, not per checkpoint.
- They are descriptive. They are not a gate and do not change any label.
- Per E33-4 and L21, this is a target-decoding calculation. It is **not** described as outcome-blind merely because it needs no checkpoint. It has not been computed by anyone before the freeze.

**Not a gate.** There is no comparison against a baseline supplied with q (E32-4).

## 5. Ridge decoder: objective, fixed λ, intercept, zero variance, rank, no clipping

These rules are fixed before any inference and are the same for every model, fold and tier.

**Objective (unchanged, the "normalized objective in Sec.5" of E33-2).** On a fit set S, let ŵ(h) = w(h)/Σ_{h∈S} w(h). Let Z be the features standardized with the fit-set ŵ-weighted mean and the ŵ-weighted population sd. The fit minimizes

J(b, β) = Σ_{h∈S} ŵ(h)·‖q(h) − b − Z(h)β‖² + λ‖β‖²_F,

where b ∈ ℝ³ is an **unpenalized intercept** (b = Σ ŵ q). Eval-set features use the fit-set mean and sd only. The solution is computed by SVD of diag(√ŵ)·Z, so it is defined for any rank. For uniform-weight analyses, w is replaced by the uniform weight before normalization.

**Primary λ (E33-2, L27).** **λ = 1e-3 is fixed** for every primary C1/C2 fit, the INIT tier, the input-only B_in+ → q losses, AC|BD, all uniform-weight analyses and descriptive T. Each model in a nested pair uses the same fixed λ. No λ is selected for any primary or decision-bearing quantity.

**Inherited value, not inherited regularization (L35).** The value 1e-3 is inherited from the line. That is not a claim that this audit reproduces the source studies' effective regularization: loss normalization and feature scaling determine the effective regularization, and the explicit objective above governs.

**Inner-λ sensitivity (descriptive only; E33-2, E33-3, L29–L33).**
- Scope: C1 and C2 only, on the **230 TRAINED checkpoints only**, P(h) weighting only. It is not applied to INIT, uniform weighting, AC|BD, the input-only losses or T, and it is not crossed with any other sensitivity (L31).
- Rule (v1.2's former primary rule, unchanged in its mechanics): grid Λ = {10⁻⁶, 10⁻⁵, …, 10¹}. Each outer fit set (128 histories) is split into its 4 depth-5 prefix orbits. λ is chosen by leave-one-orbit-out inner loss pooled over the 4 held-out orbits, weighted by w and divided by the fit-set mass. Ties within 10⁻¹² relative go to the largest λ. The model is then refit on the outer fit set and scored on Eval_f.
- Reported: selected λ per model and fold, pooled and foldwise L(base), L(full), Δ and R² gain, and the difference from the fixed-λ primary values.
- It carries **no meets-floor, below-floor or BOUNDARY label**. It cannot replace the primary analysis or determine its labels (E33-2, L29).
- **Geometry, with no direction claimed** (E33-3). The inner depth-5 split shares depth-4 prefixes with the inner fit set, which the outer split holds out (CNA delta review M2). It is a **mismatched validation geometry**. **No direction of bias in the selected λ is asserted before the results are seen** (L33). The delta review's "rewards less regularization" is not adopted (§11).

**Zero-variance features (unchanged).** A feature with fit-set ŵ-weighted sd ≤ 10⁻¹² (raw scale) is excluded from that fit (coefficient 0) and listed per model and fold.

**No clipping (E33-8, L76).** Ridge predictions q̂ are **not clipped** to [0,1] or to any range. All losses use the unclipped predictions, so q̂ can fall outside [0,1].

**Finite values (E33-8).** Every compared quantity must be finite: states, outputs, features, coefficients, predictions, losses, Δ and R_exc. A non-finite value is an integrity failure of its (PR, seed) unit (§6).

**Rank and conditioning (unchanged).** For every fit the report gives: the feature count after exclusion; the numerical rank of diag(√ŵ)·Z with tolerance σ_max·max(n,p)·ε_float64; the condition number σ_max/σ_min (∞ if rank-deficient); and σ_max/σ_rank. A rank-deficient fit is flagged RANK-DEFICIENT and is still defined. It is not UNRESOLVED and not a failure.

**B_in+ structure (known in advance, outcome-blind, §12).**
- In AB, CD, AC and BD: 1 zero-variance feature, leaving 35, with rank 28.
- In AD and BC: 0 zero-variance features, 36 kept, rank 33.
- Some input-feature coefficient directions are therefore unidentified by the fit groups. Ridge's minimum-norm solution is **one particular extrapolation choice** for them. A different supplied prior or structural constraint could assign them differently (L15, E33-1). These directions are not recoverable from fit-set observations alone.

**Held-out feature-space geometry (geometric diagnostics, E33-1; credited to the CNA delta review M1).** The CNA reported these outcome-blind, input-bits-only figures:

| fit set (folds) | CNA diagnostic |
|---|---|
| AB, CD, AC, BD | 0.632 |
| AD, BC | 0.408 |

- **What they are.** In Astra's words (L17): they "describe feature-space geometry. They are not estimates of the fraction of C2 gain, prediction error or oracle information attributable to that geometry." In E33-1's words, they are "geometric diagnostics, not fractions of prediction error or observed gain." This spec does not describe them as a share of signal, gain, error or information.
- **How they were computed (centering, scaling and weighting, as L17 requires).** The delta review states only "share of held-out centered B_in+ row norm outside the fit-set row space". It does **not** state the scaling or weighting (**flag F1**, §15). The following is read from the CNA's cited script `rank_check.py` (`61a3e424…`), not assumed, and the script reproduces both figures (§14):
  - **Features:** the 36 raw B_in+ columns (±1 readings and ±1 products), minus columns with zero (unweighted) sd on that fit set (r₁r₃ in AB and CD, r₀r₂ in AC and BD, none in AD and BC). The excluded column's held-out values are dropped too.
  - **Centering:** fit-set rows and held-out rows are both centered on the **unweighted** fit-set column mean.
  - **Scaling:** **none**. Columns are not standardized. This differs from the §5 decoder, which standardizes by ŵ-weighted sd.
  - **Weighting:** **none**. All histories have equal weight, not P(h).
  - **Statistic:** ‖Z_h − Z_h·Π‖_F / ‖Z_h‖_F, where Z_h are the centered held-out rows of the 128 held-out histories and Π = pinv(Z_c)·Z_c is the projector onto the row space of the centered fit-set rows Z_c. This is a ratio of Frobenius norms, **not** of squared norms. The corresponding squared-norm ratios, by arithmetic only, are about 0.40 and 0.17.
- Whether a nonzero component exists is invariant to positive row weights and nonzero column scaling. Its **size** is not. P(h)-weighted or standardized versions are not computed here.

## 6. S0 integrity: scope, tiers, label, tolerances, units

**Scope wording (unchanged).** S0 is integrity work without outcome-based selection. It is not "no outcome". Nothing in S0 can remove a checkpoint or change a rule.

**Three integrity tiers, reported separately.** Hash provenance, historical-metric replay and independent forward verification are kept separate (L57).
- **(i) Hash/load.** Each file's sha256 matches the roster. It is loaded from a copy outside the repo with `python -B`. The input array hash is identical for all checkpoints. This covers all 290 files.
- **(ii) Source-metric replay.** Replay the recorded metric through the source code's float64 path, with tolerance 10⁻¹² absolute. Coverage is unchanged from v1.2:

| PR | checkpoints | recorded float64 field |
|---|---|---|
| #7 | cand_final, cand_init, f_init, f_trained, f_tuned32, r_tuned843 | `seeds/s*.json` → `{arm}.errors` / `cand.init_errors` (TRAIN/TEST × X, Y, XOR, total), via `evaluate_arm` |
| #7 | sel_* (9 per seed) | `selection.grid[i].criterion` (VAL total excess), via `predict_histories` + `probability_excess` |
| #8, #9 | f_trained, f_init | `evaluation.intact_outcomes` / `f_init_outcomes` (`E_TEST_*`, `E_TRAIN_*`), via `module_from_state` → `eval_copy` |
| #8, #9 | cand_final, cand_init | **none recorded**, so SOURCE-REPLAY UNAVAILABLE |
| #10 | CAND, R-FIX-32, R-FIX-48, init and final | `stage2/results.json` `runs[*].{init,final}.E1` (torch float64 `evaluate_arm`) and `.E2` (independent numpy float64) |

- **(iii) Independent numerical verification, for all 290.** An independent numpy float64 GRU forward is compared with the torch float64 forward on the 256 histories.
  - **States and outputs must agree to max-abs ≤ 1e-10** (L59). This is a prospective numerical convention, not a certified bound on downstream fitted gains.
  - All values must be finite.
  - The output-plus-oracle reconstruction (E32-4) uses known coefficients and no fitting: d_P = f_P − q and e_P = Σ_j(f_j² − 2f_j q_j + q_j²).
  - The d̂-equivalence identity of §2 uses **abs(a-b) <= 1e-12 + 1e-12*max(abs(a), abs(b))** (E33-8), replacing v1.2's relative-only 10⁻¹². The same combined form is also applied to the e_P reconstruction (Delegate's declared extension; **flag F4**).
  - These are integrity controls, **not scientific gates**.

**Frozen source-field map (L67, E33-6).** The field map above, including the mapping of PR #8/#9 "intact" to f_trained, is frozen in the implementation manifest **before execution**.
- A field not confirmed in the manifest is declared unavailable **in the manifest, before the freeze**.
- After execution, a tier (ii) mismatch is reported with its value, the recorded value and the field compared (CNA m2). It cannot be dismissed by relabelling the field unavailable.
- If a genuine mapping error is found after execution, it may be corrected only through an additive engineering deviation and a new manifest, and the original mismatch and record are preserved (L67). This follows Astra over CNA m2's "never after" (§11).

**SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED (E33-6, L55).** This applies to the 20 PR #8/#9 cand_final (decision-bearing) and 20 PR #8/#9 cand_init (INIT) checkpoints.
- The label means: **source-metric replay is unavailable, but tier (i) hash/load and tier (iii) independent numerical forward agreement between the numpy and torch implementations passed**. "Independently verified" means **numerical forward agreement only**.
- It does **not** certify agreement with an unavailable historical metric.
- Such a checkpoint stays in the roster and in every denominator. It is decision-bearing only if tiers (i) and (iii) pass, and it is never reported as source-replay verified.

**Integrity-failure unit: (PR, seed)** (E33-5). Any tier (i), (ii) or (iii) failure, or any non-finite compared value, for any checkpoint makes that whole **(PR, seed) integrity unit** UNRESOLVED. No replacement seed is admitted, and the fixed denominators are kept.

## 7. Practical-significance floor (E32-6) and BOUNDARY band (E33-7)

**F0 removed** (unchanged). The correlation-based F0 (s_PQ ≥ ½) is **removed as an admission gate**.

**Floor.** R_oracle = Σ_h w(h) Σ_j q_j(h)(1 − q_j(h)). Floor = 0.01·R_oracle in loss units, for each of C1 and C2.

**Label, as Astra #32 gives it.**
- #32 L96: "The rationale is explicit: require an improvement equivalent to one percent of the task's mean irreducible Brier risk. This is a prospective practical-significance convention, not a theorem or a natural boundary of cognition."
- #32 L106: "This recommendation is made with the disclosed prior results known. It is prospective relative to the unrun audit, not historically outcome-blind. Preserve that distinction. Do not change it after seeing the new decoding results."

**Full-precision executable constants (E33-7, L73).** The executable floor and variance denominator are derived by the audit code from the certificate's exact rational per-history values: R_oracle, Var_w(q), the floor and the R²-gain floor are computed in exact rationals and each converted once to float64 (round-to-nearest). The executable values are:
- R_oracle = 0.5823877685694766
- Var_w(q) = 0.16761223143052342
- floor = 0.01·R_oracle = 0.005823877685694766
- R²-gain floor = 0.034746137772820054

The v1.2 pre-freeze file (`prefreeze_constants_v1_2.json`, `430d56c9…`) summed in float64 and holds 0.5823877685694765, 0.005823877685694765 and 0.03474613777282004. These differ from the exact-rational roundings by 1 ulp or less (about 1·10⁻¹⁶). The exact-rational values above govern (**flag F6**). The difference is far inside the 1e-10 BOUNDARY band.

The six-decimal figures (R_oracle 0.582388, floor 0.00582388, Var_w(q) 0.167612, R²-gain floor 0.034746) are display summaries only and are never used in code (L73). Consistency note (L81): R_oracle + Var_w(q) = 3/4 exactly in rationals (each weighted component mean is exactly ½), as expected for three components with weighted mean ½. Astra notes that this "is not independent verification of the certificate".

**BOUNDARY band (E33-7, L74).** For each comparison c ∈ {C1, C2}, with a fixed absolute guard g = 1e-10 in loss units:
- Δ_c > floor + 1e-10 gives **meets-floor**;
- Δ_c < floor − 1e-10 gives **below-floor**;
- otherwise (|Δ_c − floor| ≤ 1e-10) the result is **BOUNDARY**.

The band is "a reporting convention, not a propagated-error certificate". The label is decided in loss units. The R² gain is reported but not used for labelling.

## 8. Decision accounting and reporting (E33-5)

**Per verified TRAINED checkpoint** (Delegate's declared combination rule, **flag F5**):
- **meets-floor** if C1 and C2 are both meets-floor;
- **below-floor** if C1 or C2 is below-floor;
- **BOUNDARY** otherwise, meaning neither comparison is below-floor and at least one is BOUNDARY.

Per checkpoint, the report gives absolute L(base), L(full), Δ and R² gain for each comparison, foldwise and AC|BD values, the original predictor's R_exc(P) (§2), and the per-comparison labels.

Two more categories cover the remaining checkpoints:
- **UNRESOLVED**: the checkpoint's (PR, seed) integrity unit failed (§6).
- **INCOMPLETE / unfinished**: the checkpoint was not computed before a cap (§10).

**Claim-reporting unit: (PR, arm), across its ten declared seed checkpoints** (E33-5, L39). There are 23 units: 14 for PR #7 and 3 each for PRs #8, #9 and #10. **All 23 are reported**, including units below the quota (L41). For each unit, five counts are reported separately and sum to 10:
- m = verified meets-floor;
- b = verified below-floor;
- x = BOUNDARY;
- u = UNRESOLVED;
- i = INCOMPLETE/unfinished.

**Unresolved cases are never counted as below-floor** (E33-5). INCOMPLETE cases are also never counted as below-floor, and no omitted computation is treated as a scientific failure (E33-10).

**8/10 quota (descriptive, L41, E33-5).** "The 8/10 quota is descriptive and carries no automatic inferential significance." 56/1024 is reported only as arithmetic under ten independent fair Bernoulli trials and is not a p-value. With verified = m + b + x:
1. If verified < 8, the unit is **UNRESOLVED (insufficient verified checkpoints)**. No completed unit-level classification is issued (L49).
2. Otherwise, if m ≥ 8, the **quota is attained**. The claim ceiling plus the qualification (§0) may be used for that (PR, arm), with the remaining unresolved or unfinished cases disclosed (L47).
3. Otherwise, if m + u + i < 8, the **quota is not attained**.
4. Otherwise the unresolved or unfinished cases could change the outcome, so **quota attainment is UNRESOLVED** (L48). Astra's example (L51): m = 7, b = 1, u = 2 does not establish failure.

A BOUNDARY checkpoint is verified but is not meets-floor, so it never contributes to m (**flag F5**).

**PR-level.** A PR whose (PR, seed) integrity units leave fewer than 8 verified seeds is reported as UNRESOLVED as a whole (unchanged from v1.2). A PR-level median never becomes a claim about every arm or checkpoint.

**Per-seed summaries (descriptive).** For each (PR, seed), the median Δ over TRAINED checkpoints is given, with separate arm tables.

**Descriptive, never decision-bearing:**
- the INIT tier;
- uniform weighting;
- TEST/TRAIN strata;
- AC|BD;
- the inner-λ sensitivity (§5);
- the input-only B_in+ → q losses (§4);
- R_exc(P);
- e_P variation and correlations;
- rank and conditioning;
- T (§9).

## 9. T (descriptive only, E32-5)

**Definition (unchanged).** For a pair (P, Q) on identical inputs, let R(S→y) be the held-out R² of y ∈ {e_P, e_Q}, pooled as in §4 with the fixed full-domain Var_w(y) as denominator, using the §5 decoder at **fixed λ = 1e-3** (E33-2).
- β_P = R(S_P→e_P) − R(S_Q→e_P)
- β_Q = R(S_Q→e_Q) − R(S_P→e_Q)
- T = β_P + β_Q

**Reported:** β_P, β_Q, T and the four underlying held-out losses, all separately, for three feature types: STATE, CONF = [f, f(1−f)], and fitted FQ = [f_S, q, f_S², q², f_S·q] per head.

**Zero variance (E33-8).** If Var_w(e_P) or Var_w(e_Q) is zero (to the §5 threshold 10⁻¹²), the affected R², brackets and T are **UNDEFINED**. They are not imputed or set to zero.

**Exact reconstruction vs fitted FQ (E33-9, L77).** The **exact FQ reconstruction** is the §6 tier (iii) integrity identity. It uses known coefficients, with no fitting, and is not part of T. The **fitted FQ regressions** in T are penalized ridge fits on the FQ features. They are separate objects, are never called exact reconstructions, and need not reproduce e_P exactly.

**Astra's corrections (unchanged).**
- A positive sum is not called a double dissociation.
- Carrying its own output does not guarantee T > 0.
- τ_fq is not a universal ceiling.
- The 2√s bound is not used.
- No T result establishes an error-assessment role.

**Pair rosters (unchanged).** Within-seed, cross-arm pairs total 910 + 30 + 30 + 30 = 1000. Same-arm, cross-seed pairs total 45 × 23 = 1035. They are kept separate by PR and arm, are never pooled, and pairs sharing checkpoints are not independent.

## 10. Caps, INCOMPLETE and runtime estimate

**Caps (L65).** One pinned CPU (taskset), a **4 GB address-space limit**, single-threaded BLAS, and a **50-minute cumulative wall-clock cap that includes setup and verification**. Aggregate CPU time is reported (L65). On one pinned CPU, CPU time ≤ wall time, so the brief's 50 CPU-min is also met. No new human gate is needed.

| stage | cap |
|---|---|
| S0 | 10 min |
| P (primary C1/C2, TRAINED + INIT, input-only B_in+ → q, R_exc) | 15 min |
| D (descriptive: inner-λ sensitivity, uniform weights, T, summaries) | 20 min |
| report | 5 min |
| total | 50 min (cumulative cap) |

P runs before D. The cumulative cap binds.

**INCOMPLETE (E33-10, L78).**
- Anything unfinished when a cap is reached is marked **INCOMPLETE**.
- Completed and verified primary analyses keep their scoped labels if a later descriptive stage is incomplete.
- If any part is INCOMPLETE, **the audit as a whole is not described as complete**.
- No omitted computation is treated as a scientific failure.
- Reaching a cap is "not permission to reduce the analysis in place" (#32 L185).

**Paper estimate (updated for fixed λ; estimates, not bounds).** Rates are assumed at 10⁹ flop/s with 30 µs per SVD (optimistic) and 10⁸ flop/s with 300 µs per SVD (conservative, adopting CNA m1's 10× overhead). Thin SVD cost is 4np². Ridge via one SVD serves the whole λ grid, so the grid does not multiply the SVD count.
- **Inference:** about 6.0·10⁸ flops per implementation, 1.2·10⁹ for both, plus ~6 s of model construction (unchanged).
- **Primary C1/C2 (fixed λ, outer fits only):** 290 × 6 folds × 4 models = 6,960 SVDs at n = 128, about 4.0·10⁹ flops. This is down from 34,800 SVDs and 1.6·10¹⁰ in v1.2, because the primary no longer runs inner fits.
- **Input-only B_in+ → q:** 6 SVDs (p = 36), about 4·10⁶ flops.
- **Inner-λ sensitivity (230 TRAINED, C1/C2):** 230 × 6 × 4 × (4 inner + 1 refit) = 27,600 SVDs, about 1.27·10¹⁰ flops.
- **Uniform weights (230 TRAINED, fixed λ):** 5,520 SVDs, about 3.2·10⁹ flops (down from 1.27·10¹⁰).
- **T (fixed λ):** ≤ 4,300 source-target combinations × 3 types × 6 folds = 77,400 SVDs with p ∈ {6, 8, 15}, about 4.3·10⁹ flops (down from 387,000 SVDs and 1.7·10¹⁰).
- **Total:** about 0.6 min optimistic and about 4.9 min conservative (v1.2: 1.1–8.2 min), against the 50-minute cap. Stage P is about 0.2–1.0 min and stage D about 0.4–3.9 min, each well under its own cap.
- **Memory:** under 0.5 GB including torch.

## 11. Successor requirements and delta-review minor points

**E31 and E32 requirements** carry forward as applied in v1.2 §11 and §13. The E32 texts are retained verbatim in §13 below.

**CNA delta review (`e8f28370…`): disposition.**
- **M1** (input-baseline geometry): applied (§4, §5, §12) with Astra's corrections. "No linear decoder fit on the fit set can use those directions … whatever λ is" is restated as "not recoverable from fit-set observations alone; ridge makes one particular extrapolation choice" (L15). "63% of the input-feature signal" is not used. The figures are geometric diagnostics only (L17). The optional input-only decoder is adopted, but computed only after the freeze (L21).
- **M2** (λ): option (b) adopted as primary and (a) kept as a descriptive sensitivity, as the CNA leaned. **Conflict:** the review's "Inner validation therefore rewards less regularization than the outer task does" is **not** adopted. Astra L33 says that direction "is not established without results", so only a mismatched geometry is stated (E33-3).
- **m1** (SVD overhead): adopted, with 300 µs per SVD in the conservative estimate (§10).
- **m2** (tier (ii) mismatch reporting): adopted for reporting value and field. **Conflict:** the review says a field-map error is corrected "before the freeze, never after". Astra L67 allows a genuine post-execution mapping error to be corrected through an additive engineering deviation and a new manifest, with the original mismatch preserved. **Astra is followed** (§6).
- **m3** (unit and 8/10): confirmed by Astra L39–L41 (§8).

## 12. Exposure and provenance disclosures

**Prior observations (unchanged).** These remain prior observations, and the audit is not a fresh discovery that oracle quantities are decodable:
- the source studies' published performance results and reviews;
- PR #7's chart/E3 decoders of oracle quantities;
- PR #5's chart probe;
- one recorded excess value for PR #7 s100 CAND (TRAIN errors, **about 7·10⁻⁴ total**), seen while inventorying.

**PRE-FREEZE DISCLOSURES carried forward (outcome-blind, not S0 results).**
- Group masses A–D: 0.319 / 0.240 / 0.241 / 0.201.
- Fold fit-set n_eff: 111–121.
- R_oracle, Var_w(q), the floor and the R²-gain floor, from `prefreeze_constants_v1_2.py` (`d2a1735e…`) and its output `430d56c9…`. Their full-precision values are now quoted in §7.
- The B_in+ fit-set rank pattern of §5.
- The §6 coverage table, built from source code and result field names only.

**New for v1.3 (outcome-blind, input bits only).** The CNA's held-out feature-space geometry diagnostics, 0.632 (AB, CD, AC, BD) and 0.408 (AD, BC), computed by `rank_check.py` (`61a3e424…`) with the centering, scaling and weighting given in §5.
- The v1.3 check script reproduces them from the bits only.
- They are disclosed before the freeze as geometric diagnostics, not fractions of prediction error or observed gain (E33-1).
- The disclosure states that part of any C2 gain may reflect input-baseline extrapolation under this split (L121). C2 is reported only as improvement beyond the declared input baselines under this split.

**Floor provenance (unchanged).** The floor convention was set by Astra with the prior results known. It is fixed now and will not change after the decoding results.

**Not yet computed by anyone for this audit:** any own-error, q-decoding, Δ, T or correlation quantity. In particular, the **input-only B_in+ → q losses have not been computed**. They are computed only after the freeze. Per E33-4, they are not described as outcome-blind merely because they need no checkpoint.

**Historical status (E32-10).** The audit is prospective in its unrun comparisons and analysis rules, but is not described as historically outcome-blind.

## 13. Named edits

### 13a. E33-1 to E33-10, claim ceiling and qualification (verbatim, Astra #33 L85–L121)

**E33-1** (L86): "C2 measures improvement beyond the declared input baselines under this split, not beyond the information in the inputs. Some input-feature coefficient directions are unidentified by the fit groups, and ridge supplies a particular extrapolation. The reported held-out feature-space fractions are geometric diagnostics, not fractions of prediction error or observed gain."
*Met by* §4 (C2 wording), §5 (unidentified directions, minimum-norm extrapolation, and the 0.632/0.408 geometric diagnostics with their centering, scaling and weighting) and §12. The check script verifies the wording.

**E33-2** (L89): "The primary ridge coefficient is fixed at lambda = 1e-3 under the normalized objective in Sec.5. Inner depth-5-orbit selection is a descriptive C1/C2 sensitivity on the TRAINED roster only. It cannot replace the primary analysis or determine its labels. Uniform-weight analyses and descriptive T use fixed lambda."
*Met by* §5 (fixed λ = 1e-3 under the unchanged normalized objective; the inner-λ sensitivity is C1/C2, 230 TRAINED, unlabelled), §8 (labels come only from fixed-λ primary results) and §9 (T at fixed λ).

**E33-3** (L92): "The inner depth-5 validation split shares depth-4 prefixes that the outer split holds out. It therefore uses different generalization geometry. No direction of bias in selected lambda is asserted before observing the results."
*Met by* §5 ("mismatched validation geometry", no direction asserted) and §11 (the CNA's direction claim is not adopted).

**E33-4** (L95): "All declared B_in+ features are retained. Input-only B_in+ -> q losses are reported per fold and pooled after freeze, using the fixed primary lambda. This target-decoding calculation is not described as outcome-blind merely because it requires no checkpoint."
*Met by* §4 (all 36 features retained; input-only losses declared per fold and pooled at λ = 1e-3, after the freeze) and §12 (not computed; not called outcome-blind).

**E33-5** (L98): "Claim-reporting units are (PR, arm), each with ten declared seed checkpoints. Integrity-failure units are (PR, seed). Verified meets-floor, verified below-floor, BOUNDARY, unresolved and unfinished counts are reported separately. Unresolved cases are never counted as below-floor. The 8/10 quota is descriptive and carries no automatic inferential significance."
*Met by* §0 (units named separately), §6 ((PR, seed) integrity unit) and §8 (five separate counts m/b/x/u/i, all 23 units reported, the quota rule including UNRESOLVED attainment).

**E33-6** (L101): "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED means that source-metric replay is unavailable but the declared hash/load checks and independent numerical forward comparison passed. It does not certify agreement with an unavailable historical metric. Frozen source-field mappings are not silently changed after a mismatch."
*Met by* §6 (the label's definition, the frozen field map, and post-execution corrections only through an additive deviation).

**E33-7** (L104): "Executable floor and variance constants are derived from the full-precision certificate, not rounded report values. A gain more than 1e-10 above the floor is meets-floor; a gain more than 1e-10 below it is below-floor; otherwise it is BOUNDARY. This guard is a reporting convention, not a propagated-error certificate."
*Met by* §7 (exact-rational derivation, the full float64 values, and the BOUNDARY band).

**E33-8** (L107): "Ridge predictions are not clipped. All compared quantities must be finite. Signed-deviation loss identity checks use abs(a-b) <= 1e-12 + 1e-12*max(abs(a),abs(b)). Descriptive correlations and T with zero target variance are UNDEFINED and are not imputed."
*Met by* §5 (no clipping; finite values), §6 (combined tolerance; the 1e-10 numpy-vs-torch check), §2 (UNDEFINED correlations) and §9 (UNDEFINED T).

**E33-9** (L110): "The exact FQ reconstruction uses known coefficients without fitting. Fitted FQ regressions in descriptive T are separate objects and are not called exact reconstructions. Adding correlated features can alter effective ridge shrinkage even without adding representable functions; observed gains are interpreted under the declared estimator."
*Met by* §9 (exact reconstruction vs fitted FQ), §6 (exact reconstruction as integrity) and §4 (shrinkage interpretation).

**E33-10** (L113): "Completed and verified primary analyses retain their scoped results if a later descriptive stage is incomplete. Unfinished outputs are marked INCOMPLETE, and the audit as a whole is not described as complete. No omitted computation is treated as a scientific failure."
*Met by* §10 (INCOMPLETE rule) and §8 (INCOMPLETE never counted as below-floor).

**Claim ceiling** (L117): "On the declared W2 history domain and orbit-respecting decoder splits, adding hidden state improved prediction of oracle probabilities beyond the specified output and input baselines by the prespecified margin in the reported checkpoint blocks. This demonstrates bounded decoder accessibility under the declared analysis. It does not establish that the predictors assess or use knowledge of their own errors."
*Met by* §0 (quoted; "reported checkpoint blocks" means the (PR, arm) units) and §8 (usable only for a (PR, arm) with the quota attained).

**Qualification** (L121): "The comparison is conditional on the declared feature sets, regularization and split. Input-baseline extrapolation and changes in effective shrinkage may contribute to the gain."
*Met by* §0 (always printed after the ceiling), §4 and §12.

### 13b. E32-1 to E32-10 (verbatim, Astra #32 L189–L217; retained from v1.2)

**E32-1** (#32 L190): "The audit tests bounded accessibility of oracle probabilities from hidden state beyond declared output and input baselines. It does not identify error assessment, monitoring of an assessed predictor, acquisition, causal use or C4 status."
*Met by* §0.

**E32-2** (#32 L193): "The primary fitted target is q. Signed-deviation predictions are constructed as d_hat_P = f_P - q_hat_P, so their squared prediction error equals the oracle-probability prediction error exactly. Separate penalized fits are not used to assert this equivalence."
*Met by* §2 and §6.

**E32-3** (#32 L196): "The primary nested comparisons are B_conf versus B_conf plus STATE, and B_conf plus B_in+ versus B_conf plus B_in+ plus STATE. Each comparison uses identical targets, folds, weights and evaluation histories."
*Met by* §4 (both models in each pair also share the fixed λ).

**E32-4** (#32 L199): "Output-plus-oracle reconstruction is an algebraic integrity control. Known coefficients reconstruct d_P and e_P without fitting. Improvement beyond this exact reconstruction is not a scientific gate."
*Met by* §6 and §9.

**E32-5** (#32 L202): "T is descriptive. Its two directional brackets, their sum and their underlying held-out losses are reported separately. A positive sum is not called a double dissociation. No T result establishes an error-assessment role."
*Met by* §9.

**E32-6** (#32 L205): "The correlation-based F0 is removed as an admission gate for the reframed audit. Error variation and pairwise correlations remain descriptive. The primary practical-significance floor is an absolute held-out squared-error reduction of 0.01 times mean oracle Brier risk in each required nested comparison. This is a declared convention, not a derived cognitive boundary."
*Met by* §7.

**E32-7** (#32 L208): "Primary held-out loss pools weighted evaluation losses across folds and divides by three times total history mass, because every history is evaluated in three folds. Primary R^2 gains use the fixed full-domain oracle-target variance. Foldwise results and AC|BD results are reported separately."
*Met by* §4.

**E32-8** (#32 L211): "PR #5 is MISSING PERSISTED CHECKPOINTS and is not evaluated. The audit covers the declared available checkpoints from PRs #7-#10. Duplicate records and pairs sharing checkpoints are not counted as independent evidence."
*Met by* §1 and §9.

**E32-9** (#32 L214): "Whole-orbit holdout necessarily shares prefixes of lengths 1-2. Length-3 prefixes are shared in four declared folds and are disjoint in the two AC|BD folds. Prefixes of length at least 4 are disjoint in every fold. This is decoder-analysis generalization, not held-out predictor training."
*Met by* §3.

**E32-10** (#32 L217): "Prior source-study performance and oracle-decoding results remain disclosed development information. The revised audit is prospective in its unrun comparisons and analysis rules, but is not described as historically outcome-blind."
*Met by* §12.

## 14. Check script

`/workspace/scratch/gru_audit/check_gru_audit_spec_v1_3.py` is run with `python3 -B`. It loads no checkpoint, runs no inference and computes no q-decoding loss. It checks:
- the input hashes, and that v1, v1.1, v1.2, the reviews, the constants files and all earlier check scripts are unchanged;
- E33-1 to E33-10, the claim ceiling and the qualification, verbatim against the raw #33 file, each followed by "Met by";
- E32-1 to E32-10, verbatim against #32;
- that items 2–10 of the application brief are present;
- the full-precision constants, recomputed from the certificate in exact rationals;
- the BOUNDARY band and the quota-rule logic, on synthetic counts;
- the CNA geometry diagnostics (0.632 and 0.408), reproduced from the input bits;
- the runtime arithmetic, the caps and the 6/14/42/50 feature counts;
- the forbidden-wording rules: the prohibited C2 phrase occurs only inside E33-1's own negation, the withdrawn T wording occurs only in negated lines, no out-of-scope status terms appear except in the §0 and E32-1 disclaimers, and the audit is never called historically outcome-blind.

## 15. Open questions and flags

**v1.2 open questions, all resolved by Astra #33.**
1. "Reported checkpoint blocks": **resolved** (L39). These are (PR, arm) claim-reporting units, and (PR, seed) is the integrity-failure unit.
2. Descriptive replication requirement: **resolved** (L41). It is a descriptive quota, with no p-value or population guarantee, and all 23 units are reported.
3. λ rule: **resolved** (L27–L33). Fixed 1e-3 is primary, and the inner rule is a descriptive sensitivity.
4. B_in+ rank deficiency: **resolved** (L19). All features are kept, the limitation is disclosed, and the input-only losses come after the freeze.
5. Replay without a source metric: **resolved** (L55–L57, E33-6). The label is kept, with "independently verified" meaning numerical forward agreement.
6. The 1e-10 tolerance: **resolved** (L59). It is accepted as a prospective convention, with finite values required.
7. Caps: **resolved** (L65). The 50-minute cumulative wall-clock cap includes setup and verification, with 1 pinned CPU, 4 GB address space and aggregate CPU reported.

**Carried forward (not scientific questions; implementation-manifest items):**
- The source-field map and the "intact" → f_trained mapping are confirmed and frozen in the manifest before execution (§6).

**Flags raised in writing v1.3:**
- **F1.** The delta review gives centering for 0.632/0.408 ("centered") but not scaling or weighting. These are taken from the CNA's cited script (`61a3e424…`): unweighted fit-set-mean centering, no scaling, no weighting, a Frobenius norm ratio (not squared), and fit-set zero-variance columns dropped. The CNA should confirm that this matches its intended statistic. The geometry differs from the §5 decoder's ŵ-weighted standardization.
- **F2.** Conflicts with the delta review are resolved in Astra's favour: no direction of λ bias (M2), and post-execution mapping corrections through an additive deviation (m2) (§11).
- **F3.** The room summary of #33 omitted several raw-text requirements, which are applied here from the raw text: the minimum of 8 verified checkpoints before a unit-level classification; quota attainment is UNRESOLVED when unresolved cases could change it; all 23 units are reported; finite values are required; aggregate CPU is reported; the frozen field map with an additive-deviation route; inherited λ is not inherited effective regularization; and the shrinkage qualification. The summary described the replay label as "numerical forward agreement only". E33-6 additionally requires the declared hash/load checks to pass, and §6 requires both.
- **F4.** The E33-8 combined tolerance is specified for the signed-deviation loss identity. v1.3 also applies it to the e_P known-coefficient reconstruction, which v1.2 checked at 10⁻¹². This is the Delegate's extension.
- **F6.** The v1.2 pre-freeze constants file was summed in float64. Its R_oracle and floor differ by 1 ulp, and its R²-gain floor by about 1.4·10⁻¹⁷, from the exact-rational roundings that E33-7 requires. v1.3 uses the exact-rational values (§7). This has no effect on any label at the 1e-10 band.
- **F5.** The checkpoint-level combination of C1 and C2 labels (meets only if both meet; below if either is below; otherwise BOUNDARY), and treating BOUNDARY as not contributing to m in the quota, are the Delegate's declared rules. They follow E33-7 and v1.2 §8, but Astra did not state them explicitly.

## Change log from v1.2

- **Status:** DRAFT changed to **FINAL**, recording #33's "FREEZE WITH NAMED EDITS". The execution preconditions are now the sealed manifest plus the Research Lead's application record (L123).
- **λ (item 2):** the nested inner rule is replaced by **fixed λ = 1e-3** as primary under the unchanged §5 objective. The inner depth-5-orbit rule becomes a descriptive C1/C2 sensitivity on 230 TRAINED only, with no labels. Uniform weights, AC|BD, the input-only losses and T use fixed λ. The inner split is described as a mismatched validation geometry, with no direction of bias. The inherited value is distinguished from effective regularization.
- **B_in+ (item 3):** all features are kept. The input-only B_in+ → q losses (per fold and pooled, fixed λ) are declared for after the freeze and are not computed.
- **Wording (item 4):** C2 is improvement "beyond the declared input baselines under this split". 0.632/0.408 are geometric diagnostics credited to the CNA, with centering, scaling and weighting stated (flag F1). The minimum-norm extrapolation is described per L15. The shrinkage qualification is added.
- **Units and counts (item 5):** (PR, arm) is the claim unit and (PR, seed) the integrity unit, and "block" is no longer used for either. There are five separate counts (m/b/x/u/i), all 23 units are reported, and the quota rule includes UNRESOLVED attainment. Unresolved and incomplete are never counted as below-floor.
- **Constants (item 6):** full-precision float64 constants from exact rationals (1-ulp difference from the v1.2 float-summed file; flag F6). Six-decimal values are display-only. The 1e-10 BOUNDARY band is added.
- **Replay label (item 7):** defined as numerical forward agreement plus hash/load, not historical-metric agreement. The field map is frozen before execution, and post-execution corrections go only through an additive deviation.
- **Tolerances (item 8):** numpy-vs-torch max-abs ≤ 1e-10, with finite values required. The signed-deviation identity uses the combined absolute-relative tolerance (replacing relative-only 10⁻¹²).
- **Estimator details (item 9):** zero-variance correlations and T are UNDEFINED. There is no clipping of ridge predictions. Exact FQ reconstruction is separated from the fitted FQ regressions in T.
- **Caps (item 10):** an INCOMPLETE rule is added, under which the audit is never called complete if anything is unfinished. The original predictor's excess Brier risk R_exc(P) is reported. Caps are restated: 50 min cumulative wall-clock including setup and verification, 1 pinned CPU, 4 GB address space and aggregate CPU reported.
- **Delta-review minor points (item 11):** m1 is adopted. m2 is adopted except for "never after", where Astra is followed. m3 is confirmed. The M2 direction claim is not adopted.
- **Open questions (item 12):** Q1–Q7 are resolved by #33. The field-map confirmation is carried forward to the manifest. The runtime is updated to ~0.6–4.9 min (from 1.1–8.2). Disclosures are kept and extended (§12).
- **Unchanged:** roster, split, feature blocks, objective, zero-variance rule, rank reporting, floor convention, T definition, pair rosters, E32 texts.
