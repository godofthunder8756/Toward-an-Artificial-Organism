# GRU own-error audit: specification v1.1 (DRAFT, not frozen)

2026-10-21, ~6:30 PM ET. New file, copied from v1 (`gru_own_error_audit_spec_v1.md`, sha256 `c0fad75a18b867622b75187a75a023f8c6684a02822ee2771292b268d61452a1`), which stays unchanged. See the change log at the end. Correction: v1's header time "~6:45 PM ET" was an estimate and is too late. v1 was finished before 6:26 PM ET. v1 is not edited. It follows Astra #31 §4 (`/workspace/astra_consult31_response.txt`, sha256 `b67ff37b55c5e21f0dbcca5f1ed740d517fbeb64cfb7fed39e666c2f5a86f0ed`, L196–L239). `acquired_self_correctness_spec_v2` stays DESIGN NOT ADMITTED (close-out sha `eebf7126…`). This spec does not change it.

**Status.** This is a draft for CNA review and then Astra review. It is **not executable**. Astra #31 L210 says: "This is a proposed successor audit, not an executable protocol." L247 says: "His standing approval should be attached to the concrete reviewed and frozen scope, as previously agreed." Execution therefore needs three things: (a) this spec revised after review, (b) a freeze commit, and (c) a Research Lead application line recorded under `PI_STANDING_APPROVAL_2026-10-21_1515.md` (sha `5cc6f12a…`). That record's only application so far covers N1/N2 of spec v1.

**Execution order.** S0 and F0 wait for these three steps, in this order:
1. CNA review of this spec.
2. Astra consult #32.
3. A frozen spec plus the Research Lead's application line under `PI_STANDING_APPROVAL_2026-10-21_1515.md` (sha256 `5cc6f12a…`).

Nothing runs before then. That includes no checkpoint inference, no S0, no F0, no F1 and no T.

**Claim ceiling.** A positive result supports only *bounded accessibility of predictor-specific error information* in the stage-8 hidden state of these fixed GRU-8 checkpoints on W2. It does not support an assessment role, any use of the information, a causal claim, C4, or any consciousness claim (§8, E31-7).

**No training.** The audit performs no gradient updates and no neural training. The only fitted objects are closed-form ridge decoders on fixed features (§6).

## 1. Question (Astra #31 L204, verbatim)

> "Across a fixed roster of trained predictors, does hidden-state content predict that predictor's own errors beyond confidence and declared input baselines, and does the prediction track which predictor is being assessed on the same inputs?"

## 2. Fixed roster (CNA point 1)

**Declared from inventory, before any inference.** `/workspace/scratch/gru_audit/inventory.py` (sha `bbdbcf1a…`) uses only `git ls-tree`/`git show` and writes nothing to the repo. Its output is copied unchanged to `/workspace/review/gru_own_error_audit_roster_v1.json` (sha256 `7ad145b4384d3ba615c35187358236dc633918efc530b681c567e4c306c4cab3`), which lists the path, commit, file sha256, byte size and tensor shapes for every file. No checkpoint has been loaded into a model or evaluated for this audit.

| PR | head | directory | seeds | files per seed | TRAINED | INIT |
|---|---|---|---|---|---|---|
| #5 | `88b500a` | `acquisition_results_v1/runs` | 0–9 | 12 run records, **no weights** | — | — |
| #7 | `379bb01` | `recurrent_core_results_v1/checkpoints` | 100–109 | cand_init, cand_final, f_init, f_trained, f_tuned32, r_tuned843, 9 × sel_g{0.5,1,2}_b{−2,0,2} | 140 | 10 |
| #8 | `a5225eb` | `graded_reversion_results_v1/checkpoints` | 200–209 | cand_init, cand_final, f_init, f_trained | 30 | 10 |
| #9 | `4f6fc4c` | `first_order_control_results_v1/checkpoints` | 300–309 | same four | 30 | 10 |
| #10 | `0329818` | `frozen_recurrent_compensation_results_v1/stage{0,1}/checkpoints` | 400–409 | CAND, R-FIX-32, R-FIX-48 (stage0 = init, stage1 = final) | 30 | 30 |

That gives 290 checkpoint files: **230 TRAINED** and **60 INIT**. All of them are GRU(9→8) cores with readouts 8→32→3 (or 8→70→3 for r_tuned843 and the 9 sel runs, and 8→48→3 for R-FIX-48), stored as canonical float32 JSON/base64. Every file is byte-identical at every later PR head. No unexpected files exist, and no expected file is missing in #7–#10. The 20 PR #10 stage-0 duplicates (CAND init = R-FIX-32 init, by the shared-W0 design) are kept as listed.

**Missing (finding).** PR #5's 120 runs (cand/kfr × gru4/gru8/gru16/rnn8, k2d_gru2, k2dmlp_mlp2, kpco_gru8, ktab_table0, × 10 seeds) have run records and no persisted weights. PR #5's protocol evaluates "the final checkpoint" in memory only. PR #5 is therefore **absent from the roster**. Nothing is retrained or substituted, and no claim covers PR #5's predictors.

**Role rule (fixed by file name, never by outcome).**
- **TRAINED** means the final state of a run that updated parameters: cand_final, f_trained, f_init (W0 core frozen, readout trained), f_tuned32, r_tuned843, sel_*, and the stage-1 CAND/R-FIX files. These 230 files form the **primary roster**.
- **INIT** means an untrained initialization. These 60 files are evaluated and reported **descriptively**. They enter no gate.

**No exclusion.** No checkpoint is dropped for performance, A-FIT status, verdict, seed validity in its source study, outlier status, or any F0/F1/T quantity.
- An integrity failure in S0 (sha mismatch, load failure, replay mismatch) makes its **whole (PR, seed) block UNRESOLVED**. The failure is reported in its own category (E31-4). The checkpoint is not removed from the denominator.
- Only that block's seed counts as unresolved. No replacement seed is admitted.

## 3. Matched histories and targets (CNA point 2)

**Inputs.**
- W2 has 256 terminal histories h. Bit t of h is reading t+1 (`all_bits`, the line's convention). Readings alternate X, Y, X, …
- One 256×8 bit array is built once, hashed, and passed **unchanged to every checkpoint**. The encoding is the line's own `CoreGRU.forward`: a reading of ±1 plus a one-hot stage over 9 inputs, with zero initial state. `recurrent_core_transfer_models.py` is byte-identical from PR #7 to PR #10.
- Every predictor therefore sees the same input sequences, in the same order, at the same stages. A predictor's stage-8 state s_P(h) ∈ ℝ⁸ and forecast f_P(h) ∈ (0,1)³ are evaluated in float64 from the float32 weights.

**Weights.** w(h) = P(h) from the frozen W2 certificate (`twostream_results_v1/results.json`, blob `680c829…`, identical at PR #5 and #10, file sha `bf2de92c…`). Every mean, variance and MSE below is w-weighted over the histories in the stated set.

**Targets on the same h.** Oracle q(h) = (q_X, q_Y, q_XOR) comes from the certificate.
- **Own error:** e_P(h) = Σ_heads (f_P(h) − q(h))². This is exactly the per-history excess Brier risk over the oracle, so the oracle-irreducible part is already removed. The signed components d_P = f_P − q (3-vector) are reported descriptively.
- **Foreign error:** e_Q(h) for another roster predictor Q on the same h.
- **Oracle target:** r(h) = Σ_heads q(1 − q), the oracle's own Bayes risk. It measures task difficulty and is not predictor-specific.

**Pair family (declared).**
- The primary pairs are all unordered pairs of TRAINED checkpoints within one (PR, seed) block: C(14,2)=91 per PR #7 seed and C(3,2)=3 per PR #8/#9/#10 seed. That is 910 + 30 + 30 + 30 = **1000 pairs**.
- Cross-seed same-arm pairs are descriptive only.

## 4. Orbit-respecting, prefix-consistent split (CNA point 3; E31-6)

**Symmetry group.** G = {id, F_X, F_Y, F_X F_Y}, where F_X flips every X reading (h ↦ h ⊕ 0x55) and F_Y flips every Y reading (h ↦ h ⊕ 0xAA). The certificate states that P(h) is invariant and that (μ_x, μ_y, κ) ↦ (−μ_x, μ_y, −κ) and (μ_x, −μ_y, −κ) (TWOSTREAM_PROTOCOL_v1 L401–403). So q_X ↦ 1−q_X and q_XOR ↦ 1−q_XOR under F_X, and r is invariant. The check script re-verifies this exactly. Every terminal orbit has size 4, which gives 64 orbits. Predictors are not equivariant, so e_P need not be G-invariant. That is why orbits must not be split.

**Groups.** The assignment unit is the G-orbit of the depth-k₀ prefix h mod 2^k₀, with **k₀ = 4**. G acts on prefixes compatibly (prefix(g·h) = g·prefix(h)), so each group is a union of whole terminal orbits. The groups are:
- A = {0,5,10,15}
- B = {1,4,11,14}
- C = {2,7,8,13}
- D = {3,6,9,12}

Each group holds 64 histories and 16 terminal orbits. Each also holds exactly 16 of the source studies' TEST histories, because each prefix has 4 TEST continuations.

**Why k₀ = 4 (fixed by counting, not by data).**
- Prefix orbits at depth k number 2^(k−2) for k ≥ 2.
- k₀ = 3 gives two groups and a single 1|1 split, with no replication.
- k₀ = 4 is the smallest depth with at least three distinct balanced bipartitions.
- It also coincides with the line's frozen early/continuation boundary (readings 1–4 / 5–8, `EARLY_STAGES`/`CONTINUATION_STAGES`).

**Folds.** The 3 bipartitions {AB|CD, AC|BD, AD|BC} are each used in both directions, giving **6 folds**. Each history is evaluated in exactly 3 folds. Fold-averaged held-out MSE is the primary statistic.

**Prefix consistency (what is guaranteed and what is impossible).**
- Decoded items are stage-8 states only. No prefix state is decoded.
- In every fold, no prefix of length ≥ 4 belongs to both a fit history and an eval history. A length-k prefix with k ≥ 4 fixes the depth-4 prefix and hence the group.
- Shorter prefixes are necessarily shared. F_X flips reading 1, so every group contains both length-1 prefixes. Hence **any** whole-orbit holdout with two or more groups shares the length-1 prefixes between fit and eval. Strict "no shared prefix of any length" is incompatible with orbit holdout. The guarantee is therefore stated for lengths ≥ k₀, and the shared-short-prefix leak is disclosed (open question Q1).
- The decoder split is an analysis split only. The predictors were trained in their source studies on those studies' TRAIN histories. e_P is reported separately on source-TEST and source-TRAIN strata.

## 5. Report before any decoding claim

These are reported for every roster checkpoint (TRAINED and INIT), before F1 or T is read:
- **Support:** (computed in S0, after the freeze; the pre-freeze figures in §8 E31-9 are disclosures, not S0 results) the mass and effective size n_eff = (Σw)²/Σw² of each group and of each fold's fit and eval sets, plus TEST/TRAIN mass per group.
- **Target variation:** the mean and w-sd of e_P overall, per group and per stratum. The specific fraction s_PQ = 1 − c_PQ², with c_PQ = corr_w(e_P, e_Q), for every declared pair.
- **Absolute predictability:** held-out MSE and RMSE in Brier units, and held-out R² = 1 − MSE/Var_w,eval, for STATE and for every baseline. This is not only relative gain.

There are no interventions in this audit. A later causal phase would need its own spec (E31-7).

## 6. Order of falsifiers (cheapest first)

**S0, integrity (no outcome).**
- Re-verify each roster sha256 against the roster file.
- Load from copies outside the repo (checkpoints and the line's model source extracted by `git show` into the run directory, run with `python -B`, so no `__pycache__` lands in the repo).
- Assert one input array hash for all checkpoints.
- Replay fidelity: replayed per-arm TRAIN/TEST excess (X, Y, XOR, total) must match the values recorded in each source study (`*/seeds/s*.json` `errors` for #7–#9 including `selection`, and `stage2/results.json` for #10) within 10⁻¹² absolute. The line's EPS0 is inherited, and the replay uses the same code and float64 path.
- A checkpoint with no recorded value is marked "replay unverified". It is not excluded.

**F0, predictor-specific variation (cheapest science falsifier; needs inference, no decoder).**
- **Seed rule:** a seed passes if the median, over its declared pairs, of s_PQ is ≥ ½. An undefined c (zero variance at the 10⁻¹² floor) counts as s = 0.
- **PR rule:** a PR passes if at least 8 of 10 seeds pass. If a PR fails F0, the study **STOPs for that PR**. If all four PRs fail, the audit stops.
- Justification for ½ (first principles, not data):
  - s_PQ is the share of e_P's variance that Q's errors do not explain linearly. ½ is the point where the predictor-specific part is at least as large as the shared part. Below it, any decoding of "own error" is dominated by content common to both predictors.
  - Independently, in-sample (population) least squares gives |τ| ≤ 2√(1 − c²) = 2√s for the tracking index of T (proof: τ = aᵀMa − bᵀMb with unit a, b and ‖M‖ ≤ 1 for a difference of projections). Tracking vanishes as s → 0.
  - This is a **ceiling, not an attainability bound** (E31-2). It is not used to set F1/T thresholds. The withdrawn √μ1_abs argument (erratum `967e99b4…`) is not used anywhere.
- Justification for 8/10: it is the line's inherited SHOWN_MIN. Under a null of symmetric per-seed signs, P(≥ 8/10) = 56/1024 ≈ 0.055.

**F1, decoding beyond baselines.**
- Decoders are ridge regressions with intercept, λ = 10⁻³ (inherited RIDGE_LAMBDA), w-weighted, fit on the fold's fit set and scored on its eval set. Features are standardized on the fit set.
- Feature sets:
  - STATE: s_P (8 features).
  - B0: constant.
  - B_conf: f_P and f_P(1 − f_P) (6 features, the confidence baseline).
  - B_in: the 8 readings as ±1 (8 features, the declared input baseline, matched in dimension to STATE).
  - B_orc: q and q(1 − q) (6 features, oracle difficulty).
- For each TRAINED P: G_P = min over {B0, B_conf, B_in, B_orc} of fold-averaged MSE, minus the STATE MSE.
- **Seed rule:** a seed passes if the median over its TRAINED checkpoints of G_P is > 0. **PR rule:** at least 8/10 seeds. If no PR passes F1, the audit **STOPs** with "no decoding improvement beyond the baselines".
- Descriptive only: B_in+ (readings plus all 28 pairwise products, 36 features) and B_co = B_conf ∪ B_orc (12 features). Whether either should gate is Q3.
- Support condition, declared now: every fold's fit set must have n_eff > 10, which is the largest feature count plus intercept (9) plus one residual degree. Otherwise the fold is UNRESOLVED.

**T, tracks which predictor (CNA point 4).** For a declared pair (P, Q) on identical inputs, let R(S→y) be the fold-averaged held-out R² of a decoder from features of S to target y.

τ_state(P,Q) = [R(s_P→e_P) − R(s_Q→e_P)] + [R(s_Q→e_Q) − R(s_P→e_Q)].

τ is positive only if each predictor's own state decodes its own error better than the other predictor's state decodes it, with the **target held fixed and the inputs identical**. It is a double dissociation.

- **Why an input-only decoder cannot pass.** A decoder whose features depend on h alone (B_in, B_in+, B_orc, or any function of h) produces the same features for both rows of each bracket. Each bracket is then zero by construction, so τ_in ≡ 0.
  - τ_in is computed and must equal 0 to 10⁻¹². A nonzero value is an implementation failure and makes the result UNRESOLVED.
  - A state that is an input encoding *shared* by P and Q likewise gives τ = 0. Only state content that differs between the predictors on the same inputs can make τ > 0.
- **Confidence control.** τ_conf is the same index with features f_P, f_P(1−f_P) in place of the state. This rules out tracking that is carried entirely by the predictor's own outputs. e_P is a function of f_P and q, so this is the main confound.
- **Seed rule:** median over pairs of τ_state > 0 **and** median of (τ_state − τ_conf) > 0. **PR rule:** at least 8/10 seeds.
- T is reported only for PRs that pass F0 and F1. If T fails, the reading is "decodable but not shown to track the predictor".

**Seed accounting (E31-4).** Each seed is counted once per gate. The categories are reported separately: S0-UNRESOLVED, F0 fail, F1 fail, F1 UNRESOLVED (support), T fail. Failure counts are sizes of unions of seed sets.

## 7. Budget (E31-8)

The hardware is one CPU (taskset), 4 GB address-space limit, and single-threaded BLAS. Limits measure **wall-clock time**, and they include verification, extraction and all setup.

| stage | cap |
|---|---|
| S0 | 10 min |
| F0 | 10 min |
| F1+T | 25 min |
| report | 5 min |

The cumulative cap is **50 min** and it binds. The stage caps sum to 50.

Estimate (not a bound): 290 checkpoints × 256 histories × 8 steps is about 0.6 M GRU steps (seconds). F1+T needs about 1000 pairs × 6 folds × (4 STATE + 4 conf + 2 input) ridge fits on 9 or fewer features, plus 230 × 6 × 7 for F1: about 7·10⁴ small solves (well under a minute). Memory is under 200 MB.

## 8. Successor requirements E31-2 to E31-9 (verbatim, Astra #31 L217–L239)

**E31-2** (L218): "CF1a, CF1b and K1 concern different targets: Delta^F, lambda and m. A variance bound for Delta^F is not an attainability bound for decoding lambda or m. The equality delta_div = sqrt(mu1_abs) is not used as such a theorem."
*Application.* Here the targets are e_P (own), e_Q (foreign) and r (oracle), and each has its own statistic. F0's variation rule and the τ ≤ 2√s ceiling are not attainability bounds for decoding (§6). Passing F0 does not imply that F1 or T will pass. No √μ1_abs equality, and no threshold derived from it, appears.

**E31-3** (L221): "With sigma_q defined as the direction of the perturbation-induced checking change, the rescue reversal statistic is sigma_q*(q_A - q_B). Repair must oppose the perturbation-induced checking change. Repair identity alone is an integrity check."
*Application.* This audit has no perturbation, rescue or repair arm. Any later intervention spec must adopt this sign convention. The audit's identity checks (replay fidelity, τ_in ≡ 0) are integrity checks only and carry no evidential weight.

**E31-4** (L224): "Each seed is counted once in stop-rule accounting. Failure counts are counts of unions of seed sets, not sums of overlapping flags. A missing required checking direction, a first-order preservation failure and an unresolved comparison are reported separately."
*Application.* §6 seed accounting. The analogues are: S0-UNRESOLVED, failed gate and support-UNRESOLVED, each reported separately. The 8/10 rules count seeds, not pairs or flags.

**E31-5** (L227): "Acquisition credit requires verified final conjunction attainment and verified non-attainment in the required initialization and paired frozen-core comparisons. Invalid or unresolved comparisons do not establish absence. Success with K-FR is described as attainment with a frozen random recurrent core and trained readouts."
*Application.* The audit grants **no acquisition credit**. A positive result for f_init or R-FIX checkpoints is described as accessibility "with a frozen random recurrent core and trained readouts" (R-FIX: frozen W_hh, trained W_ih, biases and readout). CAND-versus-F-INIT differences are descriptive. INIT checkpoints are descriptive and establish no absence.

**E31-6** (L230): "The identification/evaluation split is a decoder-analysis split; learner training samples the task law unrestricted. The v2 split separates received histories but places mirror-related histories in opposite splits. Any successor claiming generalization beyond this symmetry uses a prospectively specified orbit-respecting split."
*Application.* §4: the split is decoder-analysis only, G-orbits are never split, and it is specified before any inference. Predictor training (in the source studies) is not restricted by this split.

**E31-7** (L233): "Prediction of learner-specific error and causal manipulation of CON/DIS content are separate findings. Their conjunction is not described as causal use of learner-specific correctness unless the intervention analysis connects the manipulated content to that target."
*Application.* The audit contains prediction only. A positive F1+T is "bounded accessibility" and nothing more. No causal or use language is permitted.

**E31-8** (L236): "Numerical throughput projections are estimates under stated hardware and implementation assumptions, not proven runtime bounds. The cumulative cap overrides individual stage allowances. The protocol states whether limits measure wall time or CPU time and includes verification and all permitted setup computations."
*Application.* §7: wall-clock limits, a binding cumulative cap of 50 min, stage caps that sum to 50 (checked by script), and estimates labeled as estimates.

**E31-9** (L239): "All development-informed changes retain their provenance. A newly frozen rule does not make earlier observed reference results unseen. Historical specifications and results remain unchanged; corrections and successor decisions are additive."
*Application.* The following was seen before this draft:
- The source studies' published performance results and reviews, including PR #7's verdicts and its chart/E3 decoders of oracle quantities from hidden states (an oracle-target decoding).
- PR #5's chart probe.
- While inventorying, one recorded excess value for PR #7 s100 CAND (TRAIN errors, about 7·10⁻⁴ total).
- The file inventory and tensor shapes.

**PRE-FREEZE DISCLOSURES** (outcome-blind support figures, already computed):
- These came from the spec check script (`check_gru_audit_spec.py`, sha `d2449113…`, output sha `46547235…`). It used the exact W2 masses of the published certificate and loaded no checkpoint.
- Group masses A–D: 0.319 / 0.240 / 0.241 / 0.201.
- Fold fit-set n_eff: 111–121. The declared minimum is > 10, and that rule was written before the figures were computed.
- These are **not S0 results**. S0 has not run. S0 will recompute support after the freeze, and its figures are the reportable ones.
- Like the CAND s100 exposure above, these figures stay seen. They were known before the freeze.

No own-error, foreign-error, s_PQ, G_P or τ quantity has been computed by this author. All PR files, specs and results stay unchanged. This file and the roster file are additive.

## 9. Open questions for Astra

1. **Short-prefix sharing.** Orbit holdout forces shared length < k₀ prefixes (proof in §4). Is "no shared prefix of length ≥ 4, stage-8 items only" acceptable? Or should a k₀ = 3 single-split sensitivity be added as descriptive?
2. **Specific-fraction threshold.** Is s_PQ ≥ ½ (median over pairs, 8/10 seeds) the right F0? Or should F0 use only an absolute variation floor and leave specificity to T?
3. **Baselines.** Should B_co (confidence ∪ oracle, 12 features) or B_in+ (36 features) be decision-bearing in F1 rather than descriptive? A linear decoder from [f_P, q] can approximate e_P = ‖f_P − q‖² closely.
4. **Pair family.** Within-seed pairs mix very different arms (for example CAND vs sel_g0.5_b−2). Should cross-seed same-arm pairs be primary for the "which predictor" test?
5. **Weights.** P(h)-weighting concentrates mass, and n_eff is reported. Is uniform weighting needed as a co-primary?
6. **INIT checkpoints.** Descriptive only, or should they serve as a negative-control tier for T?
7. **PR #5.** Its 120 runs have no weights, so the roster omits the K-FR/GRU-4/16/RNN-8 arms. Is the audit still "the existing GRU line" for Astra's purpose?

## 10. Part 2 status

Under this spec, the checkpoint-inference checks (S0 replay and F0 target variation) are **not run**. F0 is this audit's primary falsifier. Running it before review would make its thresholds post-observation (E31-9), and Astra #31 L247 ties the standing approval to the reviewed and frozen scope. They are marked **NEEDS-APPROVED-RUN**. Only the outcome-blind arithmetic and support checks in the check script were run. Those are exact W2 masses from the published certificate, with no checkpoint loaded. They are pre-freeze disclosures (§8 E31-9), **not S0 results**.

**Status.** S0 and F0 wait for (1) CNA review, (2) Astra consult #32, and (3) a frozen spec plus the Research Lead's application line under `5cc6f12a…`, in that order. Nothing runs before then.

## Change log

- **v1.1 (2026-10-21, ~6:30 PM ET).** Copied from v1 (sha `c0fad75a…`, unchanged).
  - The title and date are changed, and v1's late header time is corrected here, not in v1.
  - An execution-order block is added under Status.
  - The outcome-blind support figures (group masses 0.319/0.240/0.241/0.201, fold fit-set n_eff 111–121) are listed as PRE-FREEZE DISCLOSURES in §8 E31-9, next to the CAND s100 exposure.
  - §5 and §10 now mark those figures as not S0 results.
  - The §10 status line is added.
  - No rule, threshold, roster, split, falsifier or budget changed.
