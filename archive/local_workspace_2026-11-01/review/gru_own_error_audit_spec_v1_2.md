# GRU hidden-state oracle-accessibility audit: specification v1.2 (DRAFT, not frozen)

2026-10-21, ~8:40 PM ET. New file and additive. It is derived from v1.1 (`gru_own_error_audit_spec_v1_1.md`, sha256 `4661a8895ef495c28a1a41ff7405f029ff3c9f4451a12b1a1af9ccc701641ccf`, unchanged). v1 (`c0fad75a18b867622b75187a75a023f8c6684a02822ee2771292b268d61452a1`) and v1.1 are not edited.

Inputs, all verified:
- Astra #32: `/workspace/astra_consult32_response.txt`, sha256 `99378f762fe2a21ae519b1a8368ab52b48339cba9e2477c94884cf49f9f7df7b`. Line numbers below are L*n* of that file.
- CNA review: `gru_own_error_audit_spec_v1_review.md`, `f6b2db6f…`.
- CNA addendum: `gru_own_error_audit_spec_v1_1_review_addendum.md`, `721100d1…`.
- CNA erratum: `gru_own_error_audit_review_erratum_c32.md`, `4a5ad4f3…`.

Astra #32 L7 notes that Astra did not independently verify the inventory, code or hashes. Here they are re-verified by script (§14).

## 0. Status, scope and claim ceiling

**Verdict being applied.** Astra #32 L1 says: "Verdict: DO NOT FREEZE v1.1. Choose Q1(a), with a correction: the output-plus-oracle comparison must be an algebraic control, not a second gate requiring improvement." L227 says: "v1.1 remains unapproved for execution."

**Not executable.** Nothing runs until all of the following are done, in this order:
1. A CNA delta review of v1.2 and Astra's quick check.
2. A freeze of this spec, the roster (`gru_own_error_audit_roster_v1.json`, `7ad145b4…`) and an implementation manifest. The manifest lists the code files and their hashes, plus the replay field map of §6.
3. The Research Lead's application line under `PI_STANDING_APPROVAL_2026-10-21_1515.md` (`5cc6f12a…`). Astra #32 L225 says: "The Research Lead should attach the existing standing approval to the revised, reviewed and frozen specification, roster and implementation manifest."

No checkpoint has been loaded and no inference has run.

**Reframe.** The question changes from own-error assessment to bounded accessibility of oracle probabilities from hidden state. A pass shows decoder accessibility only. It does not show error assessment, monitoring or tracking of an assessed predictor, acquisition, causal use, C4, or anything about consciousness.

**Primary question** (L31, verbatim):
> "On the declared held-out history groups, how much does adding hidden state improve prediction of the oracle probabilities beyond the predictor's output and the declared input features?"

**Claim ceiling** (§9, L223, verbatim). This is the strongest permitted positive wording:
> "On the declared W2 history domain and orbit-respecting decoder splits, adding hidden state improved prediction of oracle probabilities beyond the specified output and input baselines by the prespecified margin in the reported checkpoint blocks. This demonstrates bounded decoder accessibility under the declared analysis. It does not establish that the predictors assess or use knowledge of their own errors."

"Reported checkpoint blocks" is defined in §8. That definition is an interpretation and is flagged as Q1.

**No training.** There are no gradient updates. The only fitted objects are closed-form ridge decoders (§5).

**Why the reframe (identifiability, CNA review A1, adopted by Astra L11–L33).**
- e_P(h) = Σ_j (f_P,j(h) − q_j(h))² and d_P = f_P − q are exact functions of (f_P, q). Given the output and the oracle, nothing is left over.
- The audit can address only two things: restricted decodability, and improvement beyond declared output features (L23–L27).
- The v1 review's A2 (T passable by output-carrying) is cited here only together with its erratum (`4a5ad4f3…`). That erratum withdraws three claims: that T is "trivially passed or impossible", that T > 0 is a "double dissociation", and that τ_fq is a ceiling. It also narrows the 2√s check to the population setting.
- v1.2 relies on none of those withdrawn claims.

## 1. Roster (unchanged from v1.1 §2, except for wording)

**PR #5.** Astra L133, verbatim: "PR #5: MISSING PERSISTED CHECKPOINTS; NOT EVALUATED." Its 120 run records have no persisted weights. Nothing is retrained or substituted, and PR #5 is not excluded for performance (L135).

**Scope wording** (L137): "available persisted checkpoints from PRs #7-#10". The audit makes no claim about the whole GRU line.

**Roster contents.** There are 290 files: 230 TRAINED and 60 INIT. The INIT files are descriptive only (L139). Roles are fixed by file name, and nothing is excluded on any outcome.

**Duplicates.** The 10 PR #10 init duplicates (CAND init = R-FIX-32 init) are kept for provenance. They are not independent evidence (L144, E32-8).

**Frozen-core wording** (L141–L142; this replaces v1.1's E31-5 application):
- "f_init can be described as a frozen random recurrent core with a trained readout."
- "R-FIX has frozen W_hh with other core parameters and the readout trained. Its entire recurrent core is not frozen."

**Tiers.** These two descriptions apply to the PR #7–#9 f_init arms and the PR #10 R-FIX-32/R-FIX-48 arms. Each arm is a separate tier in every table (CNA m3). CAND, f_trained, f_tuned32, r_tuned843 and sel_* are described by their source-study roles.

## 2. Inputs, weights, target and signed deviation

**Inputs and weights (unchanged from v1.1 §3).**
- One hashed 256×8 bit array is passed unchanged to every checkpoint. The encoding is the line's `CoreGRU.forward`, and `recurrent_core_transfer_models.py` is byte-identical from PR #7 to #10.
- Each predictor yields a stage-8 state s_P(h) ∈ ℝ⁸ and an output f_P(h) ∈ (0,1)³. Both are computed in float64 from the float32 weights.
- w(h) = P(h) from the W2 certificate (file sha `bf2de92c…`), with Σ_h w(h) = 1. P(h) weighting is primary, and uniform weighting is a descriptive sensitivity (L169).

**Fitted target: q** (E32-2). The oracle q(h) = (q_X, q_Y, q_XOR) is fitted jointly as 3 columns with one shared λ. Per-history loss is ℓ(h) = Σ_j (q̂_P,j(h) − q_j(h))².

**Signed deviation (constructed, not fitted).**
- d̂_P(h) = f_P(h) − q̂_P(h), with d_P = f_P − q.
- Then Σ_j (d̂_P,j − d_P,j)² = Σ_j (q̂_P,j − q_j)² exactly (L41–L42), so the signed deviation inherits every q result.
- No separate ridge fit to d or e is used to assert this equivalence (L46, E32-2). The identity is verified numerically as an integrity check (§6).

**Descriptive only.** e_P variation is reported as weighted mean, sd and quantiles per tier, stratum and group, plus pairwise corr_w(e_P, e_Q). These are not gates (L108, E32-6).

## 3. Split (v1.1 §4 retained; the Q1 statement is corrected)

**Unchanged from v1.1.**
- Groups are the G-orbits of the depth-4 prefix, where G = {id, ⊕0x55, ⊕0xAA, ⊕0xFF}: A = {0,5,10,15}, B = {1,4,11,14}, C = {2,7,8,13}, D = {3,6,9,12}. Each group has 64 histories.
- The 3 bipartitions AB|CD, AC|BD and AD|BC are each used in both directions, giving 6 folds. Every history is evaluated in exactly 3 folds.
- Only stage-8 states are decoded.

**Corrected prefix statement.** The correction is due to the CNA addendum (`721100d1…`, §2) and accepted by Astra L148–L155. E32-9 is quoted in §13.
- Prefixes of lengths 1–2 are necessarily shared under any whole-orbit holdout.
- Length-3 prefixes are shared in 4 of the 6 folds (AB|CD, AD|BC, both directions). The two AC|BD folds share none, because A ∪ C and B ∪ D are the two depth-3 orbits.
- Lengths ≥ 4 are shared in no fold.
- v1/v1.1's claim that sharing is forced at every length below k₀ is withdrawn.
- Short-prefix sharing is **not** called harmless. It permits reuse of short-prefix structure, which is compatible with a bounded stage-8 decoder-generalization claim but limits stronger claims about wholly unfamiliar histories (L157).

**AC|BD sensitivity (descriptive, prespecified).** This analysis uses the two AC|BD folds only, with denominator 1 × Σw because each history is evaluated once there. It reuses the declared folds, so there is no split search (L155).

## 4. Primary nested comparisons (E32-3)

**Feature blocks.** All are computed per checkpoint P on the same h.
- **B_conf**: f_P and f_P(1 − f_P). 6 features.
- **B_in+**: the 8 readings as ±1 and all 28 pairwise products. 36 features. This is "a stronger named input benchmark, not a complete representation of all functions of history" (L53).
- **STATE**: s_P. 8 features.

**Comparisons.** Each comparison uses identical targets, folds, weights and evaluation histories.

| comparison | base | full | features (base → full), each plus intercept |
|---|---|---|---|
| C1 | B_conf | B_conf + STATE | 6 → 14 |
| C2 | B_conf + B_in+ | B_conf + B_in+ + STATE | 42 → **50** |

**Pooled held-out loss** (E32-7, L161–L167):

L(model) = Σ_f Σ_{h ∈ Eval_f} w(h)·ℓ_f(h) / (3·Σ_h w(h)).

**Effect statistics.**
- Gain: Δ_c(P) = L(base) − L(full).
- R² gain: Δ_c(P) / Var_w(q), where Var_w(q) = Σ_j Var_w(q_j) over the full 256-history domain. This is a fixed denominator, and fold ratios are not averaged (L167).
- Foldwise results and AC|BD results are reported separately.

**Not a gate.** There is no comparison against a baseline supplied with q (L55, E32-4; see §6).

## 5. Ridge decoder: objective, λ rule, intercept, zero variance, rank (§7 blockers)

These rules are fixed before any inference, and are the same for every model, fold and tier.

**Objective.** On a fit set S, let ŵ(h) = w(h)/Σ_{h∈S} w(h), which normalizes the weighted loss. Let Z be the features standardized with the fit-set ŵ-weighted mean and the ŵ-weighted population sd. The fit minimizes

J(b, β) = Σ_{h∈S} ŵ(h)·‖q(h) − b − Z(h)β‖² + λ‖β‖²_F,

where b ∈ ℝ³ is an **unpenalized intercept**, so the solution has b = Σ ŵ q − (Σ ŵ Z)β = Σ ŵ q. Eval-set features are transformed with the fit-set mean and sd only (fit-only standardization). The solution is computed by SVD of diag(√ŵ)·Z, so it is defined for any rank.

**λ rule (stated in advance, nested within the fit set only).**
- Grid: Λ = {10⁻⁶, 10⁻⁵, …, 10¹}, 8 values. Λ > 0, so ridge is unique under rank deficiency.
- Inner folds: each outer fit set (2 groups, 128 histories) is split into its **4 depth-5 prefix orbits**. Each depth-4 group splits into exactly 2 of the 8 depth-5 orbits.
- Selection: run leave-one-orbit-out over those 4 inner folds (inner fit sets of 96 histories). For each λ, take the inner loss pooled over the 4 held-out orbits, weighted by w and divided by the fit-set mass. Choose the λ with the smallest inner loss. Ties within 10⁻¹² relative go to the **largest** λ.
- Refit on the full outer fit set with the chosen λ and score on Eval_f.
- No eval-set or outer information enters the choice of λ. Selected λ values are reported for every model and fold.
- Each model in a nested pair chooses its own λ under the same rule.

**Zero-variance features.** A feature with fit-set ŵ-weighted sd ≤ 10⁻¹² (raw scale) is excluded from that fit, meaning its coefficient is 0. The exclusion is listed per model and fold. The same rule applies inside the inner folds.

**Rank and conditioning** (L177–L178).
- For every outer and inner fit, the report gives: the feature count after exclusion; the numerical rank of diag(√ŵ)·Z, with tolerance σ_max·max(n,p)·ε_float64; the condition number σ_max/σ_min (∞ if rank-deficient); and the effective conditioning σ_max/σ_rank.
- **Declared action if rank-deficient:** nothing changes. Ridge with λ ∈ Λ is still defined, and no feature is dropped beyond the zero-variance rule. The fit is flagged RANK-DEFICIENT.
- Rank deficiency is not UNRESOLVED and not a failure. Effective sample size exceeding the parameter count is not taken as a guarantee of rank, conditioning or generalization. The old "> 10" support rationale is removed (L177).
- **Known in advance** (outcome-blind, §12):
  - B_in+ is structurally rank-deficient in every outer fit set, because each orbit group fixes the group-invariant products r₀r₂ and r₁r₃ (readings indexed from 0). A two-group fit set therefore holds one of them constant (AB, CD, AC, BD) or ties them (AD, BC), and induces further exact collinearities among the readings and products.
  - In AB, CD, AC and BD: 1 zero-variance feature, leaving 35, with rank 28.
  - In AD and BC: 0 zero-variance features, 36 kept, rank 33.
  - Ridge then splits coefficients across collinear columns by minimum norm, and the held-out groups extrapolate that split. This is part of the declared analysis (Q4).

## 6. S0 integrity: scope, float64 coverage, unverified replay, block minimum

**Scope wording (L182).** S0 is integrity work without outcome-based selection. Source-performance replay necessarily evaluates outputs and errors, so S0 is **not** "no outcome". Nothing in S0 can remove a checkpoint or change a rule.

**Three integrity tiers (L179), reported separately.**
- **(i) Hash/load.** Each file's sha256 matches the roster. It is loaded from a copy outside the repo with `python -B`. The input array hash is identical for all checkpoints. This tier covers all 290 files.
- **(ii) Source-metric replay.** Replay the recorded metric through the source code's own float64 path (`eval_copy` → `.double()`, from source review). The tolerance is 10⁻¹² absolute (EPS0, valid because the path is the same). Coverage, from reading the source code and result *field names* only, without reading values:

| PR | checkpoints | recorded float64 field |
|---|---|---|
| #7 | cand_final, cand_init, f_init, f_trained, f_tuned32, r_tuned843 | `seeds/s*.json` → `{arm}.errors` / `cand.init_errors` (TRAIN/TEST × X, Y, XOR, total), via `evaluate_arm` |
| #7 | sel_* (9 per seed) | `selection.grid[i].criterion` (VAL total excess), via `predict_histories` + `probability_excess` |
| #8, #9 | f_trained, f_init | `evaluation.intact_outcomes` / `f_init_outcomes` (`E_TEST_*`, `E_TRAIN_*`), via `module_from_state` → `eval_copy` |
| #8, #9 | cand_final, cand_init | **none recorded**, so SOURCE-REPLAY UNAVAILABLE |
| #10 | CAND, R-FIX-32, R-FIX-48, init and final | `stage2/results.json` `runs[*].{init,final}.E1` (torch float64 `evaluate_arm`) and `.E2` (independent numpy float64) |

The field map and the mapping of PR #8/#9 "intact" to f_trained are confirmed against the code in the implementation manifest before the freeze. An unconfirmed mapping is treated as unavailable.

- **(iii) Independent numerical verification, for all 290.** An independent numpy float64 GRU forward is compared with the torch float64 forward on the 256 histories. States and outputs must agree to max-abs ≤ 10⁻¹⁰, a declared convention for different operation order. In addition:
  - the output-plus-oracle reconstruction (E32-4) must hold to 10⁻¹²: d_P = f_P − q, and e_P = Σ_j(f_j² − 2f_j q_j + q_j²), both with **known coefficients and no fitting**;
  - the d̂-equivalence identity of §2 must hold to 10⁻¹² relative.

  These checks are integrity controls, **not scientific gates** (L55, E32-4).

**Missing replay references (L180).** That means 20 decision-bearing checkpoints (PR #8/#9 cand_final) and 20 INIT checkpoints. Such a checkpoint:
- stays in the roster and in every denominator;
- is decision-bearing only if tiers (i) and (iii) pass;
- is labelled **SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED** in every table;
- is never reported as source-replay verified.

If tier (i) or (iii) fails, its whole (PR, seed) block is UNRESOLVED.

**Integrity failure.** Any tier (i), (ii) or (iii) failure in a block makes that whole (PR, seed) block UNRESOLVED. No replacement seed is admitted, and the fixed denominators are kept (L181).

**Declared minimum of verified blocks.** Each (PR, arm) has a fixed denominator of 10 seeds. If fewer than **8** of its seed blocks are verified, its result is **UNRESOLVED (insufficient verified blocks)**, not a scientific failure. A PR with fewer than 8 verified seed blocks is UNRESOLVED as a whole. 8 is the minimum at which the 8/10 replication requirement (§8) can still be met.

## 7. Practical-significance floor (E32-6), replacing F0

**F0 removed.** The correlation-based F0 (s_PQ ≥ ½) is **removed as an admission gate** (L84–L86). In Astra's words (L86), the quantity "does not divide variance into "shared task content" and "predictor-specific content."" Correlations and e_P variation stay descriptive.

**Floor.** R_oracle = Σ_h w(h) Σ_j q_j(h)(1 − q_j(h)) (L92). A comparison meets the floor for checkpoint P when Δ_c(P) ≥ 0.01·R_oracle. The equivalent R² gain is Δ_c/Var_w(q) ≥ 0.01·R_oracle/Var_w(q) (L100). No separate R² floor is added (L98).

**Label, as Astra gives it.**
- L96: "The rationale is explicit: require an improvement equivalent to one percent of the task's mean irreducible Brier risk. This is a prospective practical-significance convention, not a theorem or a natural boundary of cognition."
- L106: "This recommendation is made with the disclosed prior results known. It is prospective relative to the unrun audit, not historically outcome-blind. Preserve that distinction. Do not change it after seeing the new decoding results."

**Values** (outcome-blind, from the certificate, §12):
- R_oracle = 0.582388
- floor = 0.00582388
- Var_w(q) = 0.167612
- R²-gain floor = 0.034746

## 8. Decision accounting and reporting

**Per TRAINED checkpoint.** A checkpoint is **meets-floor** if C1 and C2 both have Δ ≥ 0.01·R_oracle. Results are reported per checkpoint, with absolute L(base), L(full), Δ and R² gain for each comparison, and with foldwise and AC|BD values.

**Replication requirement** (L110). The inherited 8/10 rule "can remain a descriptive replication requirement on top of the effect floor". It is applied per **(PR, arm)**:
- The claim-ceiling wording (§0) may be used for a (PR, arm) only if at least 8 of its 10 seed checkpoints are meets-floor and the block is not UNRESOLVED (§6).
- These (PR, arm) units are the "reported checkpoint blocks". There are 23: 14 for PR #7 and 3 each for PRs #8, #9 and #10.
- 56/1024 is reported only as arithmetic under ten independent fair Bernoulli trials. It is not a p-value (L110).

**Per-seed summaries.** These are descriptive: for each (PR, seed), the median Δ over TRAINED checkpoints, with separate arm tables. A PR-level median never becomes a claim about every arm or checkpoint (L127).

**Accounting (E31-4, retained).** Each seed is counted once. The categories are reported separately: S0-UNRESOLVED, insufficient-verified-blocks UNRESOLVED, below floor, and INCOMPLETE (cap reached, §10). Counts are unions of seed sets.

**Descriptive, never decision-bearing:**
- the INIT tier;
- uniform weighting;
- TEST/TRAIN strata;
- AC|BD;
- e_P variation and correlations;
- selected λ, rank and conditioning;
- T (§9).

## 9. T (descriptive only, E32-5)

**Definition.** For a pair (P, Q) on identical inputs, let R(S→y) be the held-out R² of y ∈ {e_P, e_Q}. It is pooled as in §4, with denominator the fixed full-domain Var_w(y), and uses the §5 decoder. The two brackets are:
- β_P = R(S_P→e_P) − R(S_Q→e_P)
- β_Q = R(S_Q→e_Q) − R(S_P→e_Q)

T = β_P + β_Q.

**What is reported.** β_P, β_Q, their sum, and the four underlying held-out losses, all separately. This is done for three feature types: STATE, CONF = [f, f(1−f)], and FQ = [f_S, q, f_S², q², f_S·q] per head.

**Astra's corrections (L63–L80; CNA erratum `4a5ad4f3…`).**
- T > 0 does **not** require both brackets to be positive. A positive sum is **not called a double dissociation** (L63).
- Carrying its own output does not guarantee T > 0 (L65).
- Exact own-target reconstruction by the complete output-plus-oracle control **does not make τ_fq a universal ceiling** on τ_state. T subtracts foreign-target performance, and held-out R² can be negative (L67–L69).
- The 2√s bound applies only to population projections. It is not a bound on these cross-validated, standardized ridge predictions (L80). It is not used.
- The sound reading (L73–L76): T is confounded by output accessibility and decoder geometry; a positive T cannot establish an additional error-assessment representation; and failing to exceed τ_fq would not establish absence of assessment.

**Pair rosters.** These are fixed descriptive rosters (L116–L121), reported separately by PR and arm and never pooled. Pairs that share checkpoints are not independent (E32-8).
- Within-seed, cross-arm pairs: 910 + 30 + 30 + 30 = 1000.
- Same-arm, cross-seed pairs: C(10,2) = 45 per arm × 23 arms = 1035.

## 10. Caps and runtime estimate (E31-8)

**Caps.** One CPU (taskset), a 4 GB address-space limit and single-threaded BLAS. There is a **50-minute cumulative cap measured as wall-clock time** (L185), and CPU time is reported as well. On one pinned CPU, CPU time ≤ wall time, so the 50 CPU-min limit in the task brief also holds (conflict flagged in §15). The caps include verification, extraction and all setup.

| stage | cap |
|---|---|
| S0 | 10 min |
| P (primary C1/C2, TRAINED + INIT) | 15 min |
| D (descriptive: uniform weights, T, summaries) | 20 min |
| report | 5 min |
| total | 50 min (cumulative cap) |

The cumulative cap binds. P runs before D. Reaching any cap gives **INCOMPLETE** for the unfinished part. It is "not permission to reduce the analysis in place" (L185).

**Paper estimate.** These are estimates, not bounds (E31-8). They are derived from counts with no timing run. Flop rates are assumed at 10⁸ flop/s (conservative) and 10⁹ flop/s (optimistic), with ~30 µs of overhead per SVD.

- **Inference.** 290 × 256 histories × 8 steps = 593,920 GRU steps at about 816 flops each, plus 74,240 readouts at ≤ 1,540 flops. That is about 6·10⁸ flops per implementation and about 1.2·10⁹ flops for torch plus numpy. Time is ~1–12 s, plus ~6 s of model construction.
- **Primary.** 290 checkpoints × 4 models × 6 folds × 5 fits (4 inner + 1 outer) = 34,800 thin SVDs. Each SVD costs 4np², with n = 96 or 128 and p ∈ {6, 14, 42, 50}. Per checkpoint and fold, the outer and inner fits together come to about 9.2·10⁶ flops, so the total is about 1.6·10¹⁰ flops: ~16–160 s, plus ~1 s of overhead.
- **Uniform-weight sensitivity** (230 TRAINED). About 1.27·10¹⁰ flops: ~13–127 s.
- **T.** 230 own plus ≤ 4,070 cross decoders, giving ≤ 4,300 source-target combinations. Each runs 3 types × 6 folds × 5 fits, for ≤ 387,000 SVDs with p ∈ {6, 8, 15}. That is about 1.7·10¹⁰ flops: ~17–172 s, plus ~12 s of overhead.
- **Total.** About 1.1 min optimistic and about 8.2 min conservative, against the 50-minute cap. Each stage estimate is also under its own cap.
- **Memory.** The states and outputs are about 10 MB. With torch the total is under 0.5 GB.

## 11. Successor requirements carried forward

The E31-2 to E31-9 texts are quoted in v1.1 §8, unchanged, and their applications stand with these amendments:
- **E31-2.** The F0 and 2√s statements are removed (§7, §9).
- **E31-5.** The frozen-core wording is replaced by L141–L142 (§1).
- **E31-6.** The split is §3 with the corrected prefix statement.
- **E31-9.** Superseded and extended by §12 and E32-10.

## 12. Exposure and provenance disclosures (E31-9, E32-10, L183)

**Prior observations.** These remain prior observations, and the audit is not a fresh discovery that oracle quantities are decodable (L183).
- The source studies' published performance results and reviews.
- PR #7's chart/E3 decoders of oracle quantities from hidden states.
- PR #5's chart probe.
- One recorded excess value for PR #7 s100 CAND (TRAIN errors, **about 7·10⁻⁴ total**), seen while inventorying.

**PRE-FREEZE DISCLOSURES from v1.1, carried forward.** These are outcome-blind and are not S0 results:
- group masses A–D: 0.319 / 0.240 / 0.241 / 0.201;
- fold fit-set n_eff: 111–121.

**New for v1.2.** These are outcome-blind, from the certificate and the input bits only, with no checkpoint loaded. They were computed by `/workspace/scratch/gru_audit/prefreeze_constants_v1_2.py` (sha `d2a1735e…`, output `prefreeze_constants_v1_2.json`, sha `430d56c9…`) after the rules in §5 and §7 were written:
- R_oracle = 0.582388, Var_w(q) = 0.167612, floor = 0.00582388 and R²-gain floor = 0.034746;
- the B_in+ fit-set rank pattern of §5;
- reading only source code and result **field names** (not values) to build the §6 coverage table.

**Floor provenance.** The floor convention was set by Astra with the prior results known (L106). It is fixed now and will not change after the decoding results.

**Not yet computed by anyone for this audit:** any own-error, q-decoding, Δ, T or correlation quantity.

## 13. Named edits E32-1 to E32-10 (verbatim, Astra #32 §8, L189–L217)

**E32-1** (L190): "The audit tests bounded accessibility of oracle probabilities from hidden state beyond declared output and input baselines. It does not identify error assessment, monitoring of an assessed predictor, acquisition, causal use or C4 status."
*Met by* §0: the question, the claim ceiling and the reframe. No assessment, monitoring, acquisition, causal or C4 wording appears anywhere.

**E32-2** (L193): "The primary fitted target is q. Signed-deviation predictions are constructed as d_hat_P = f_P - q_hat_P, so their squared prediction error equals the oracle-probability prediction error exactly. Separate penalized fits are not used to assert this equivalence."
*Met by* §2: q is fitted, d̂ is constructed, and the identity is checked as integrity in §6. There is no ridge fit to d or e.

**E32-3** (L196): "The primary nested comparisons are B_conf versus B_conf plus STATE, and B_conf plus B_in+ versus B_conf plus B_in+ plus STATE. Each comparison uses identical targets, folds, weights and evaluation histories."
*Met by* §4 C1/C2: same q, same 6 folds, same w, same Eval_f.

**E32-4** (L199): "Output-plus-oracle reconstruction is an algebraic integrity control. Known coefficients reconstruct d_P and e_P without fitting. Improvement beyond this exact reconstruction is not a scientific gate."
*Met by* §6 tier (iii): the identities with known coefficients are integrity checks only. No baseline supplied with q is a gate.

**E32-5** (L202): "T is descriptive. Its two directional brackets, their sum and their underlying held-out losses are reported separately. A positive sum is not called a double dissociation. No T result establishes an error-assessment role."
*Met by* §9: β_P, β_Q, T and the four losses are reported, and T is never a gate.

**E32-6** (L205): "The correlation-based F0 is removed as an admission gate for the reframed audit. Error variation and pairwise correlations remain descriptive. The primary practical-significance floor is an absolute held-out squared-error reduction of 0.01 times mean oracle Brier risk in each required nested comparison. This is a declared convention, not a derived cognitive boundary."
*Met by* §7: F0 is removed, the floor is 0.01·R_oracle in C1 and C2, and it is labelled as Astra labels it.

**E32-7** (L208): "Primary held-out loss pools weighted evaluation losses across folds and divides by three times total history mass, because every history is evaluated in three folds. Primary R^2 gains use the fixed full-domain oracle-target variance. Foldwise results and AC|BD results are reported separately."
*Met by* §4: the pooled L with denominator 3·Σw and R² gain over Var_w(q). Foldwise and AC|BD results are reported separately in §3 and §4.

**E32-8** (L211): "PR #5 is MISSING PERSISTED CHECKPOINTS and is not evaluated. The audit covers the declared available checkpoints from PRs #7-#10. Duplicate records and pairs sharing checkpoints are not counted as independent evidence."
*Met by* §1 (PR #5 and duplicates) and §9 (pairs are not independent and not pooled).

**E32-9** (L214): "Whole-orbit holdout necessarily shares prefixes of lengths 1-2. Length-3 prefixes are shared in four declared folds and are disjoint in the two AC|BD folds. Prefixes of length at least 4 are disjoint in every fold. This is decoder-analysis generalization, not held-out predictor training."
*Met by* §3, with the corrected statement verified by script in §14. The split is decoder-analysis only, because the predictors were trained on their source TRAIN histories.

**E32-10** (L217): "Prior source-study performance and oracle-decoding results remain disclosed development information. The revised audit is prospective in its unrun comparisons and analysis rules, but is not described as historically outcome-blind."
*Met by* §12. Nowhere does this spec call the audit historically outcome-blind.

## 14. Check script

`/workspace/scratch/gru_audit/check_gru_audit_spec_v1_2.py` checks the following. It loads no checkpoint.
- Hashes of the inputs.
- E32-1 to E32-10, the §9 ceiling and the other Astra quotes, verbatim.
- Roster counts and pair counts (1000 and 1035).
- Group and fold structure, including the corrected prefix statement and the depth-5 inner orbits.
- The constants and the floor arithmetic.
- The pooled-loss denominator, including that each history is evaluated 3 times.
- The rank pattern of B_in+.
- Feature counts (6/14/42/50).
- The runtime arithmetic.
- The caps.
- That v1, v1.1 and the earlier scripts are untouched.

## 15. Open questions for Astra's quick check

1. **"Reported checkpoint blocks".** v1.2 defines these as (PR, arm) units across 10 seeds, with 8/10 meets-floor as the descriptive replication requirement for using the claim wording. Is that the intended unit, rather than (PR, seed) blocks?
2. **"Descriptive replication requirement" (L110).** v1.2 reads this as a requirement on the claim wording that carries no inferential weight. Is that correct?
3. **λ rule.** Is the inner leave-one-depth-5-orbit-out selection over a fixed 8-value grid acceptable? The alternative is the fixed λ = 10⁻³ inherited from the line.
4. **B_in+ rank deficiency.** It is structural: the orbit groups fix or tie r₀r₂ and r₁r₃. It is handled by minimum-norm ridge and flagged, with no feature change. Is that acceptable, or should the group-invariant products be declared out of B_in+ in advance?
5. **Replay without a source metric** (PR #8/#9 cand_final). Is "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED" an adequate consequence for decision-bearing checkpoints?
6. **The 10⁻¹⁰ tolerance** for independent numpy-versus-torch verification is a declared convention. Is it acceptable?
7. **Caps.** The task brief said 50 CPU-minutes, and Astra L185 says 50 minutes of wall-clock. v1.2 binds on wall-clock and also reports CPU time. Is that acceptable?

## Change log from v1.1

- **Retitled and reframed** to oracle-probability accessibility (L1, L3, L31). The own-error question of #31 L204 is no longer primary.
- **Claim ceiling** replaced by §9 L223, verbatim.
- **Target** is now q. The signed deviation d̂ = f − q̂ is constructed, not fitted.
- **F1** (STATE alone against each baseline alone) is replaced by the nested comparisons C1 and C2. B_in+ is now decision-bearing as part of C2. B_orc and B_co are dropped as gates (L55).
- **F0** (s_PQ ≥ ½) is removed. The 0.01·R_oracle floor is added (§7).
- **Output-plus-oracle reconstruction** is an algebraic integrity control (§6).
- **T** is descriptive only, with Astra's corrections and the CNA erratum (§9). The "double dissociation" wording is removed. τ_in, τ_conf and the 2√s ceiling are no longer used as controls or bounds.
- **Aggregation:** the pooled loss divided by 3·Σw. The R² gain uses the fixed Var_w(q).
- **Ridge:** the objective, the λ rule, the unpenalized intercept, the zero-variance rule, and rank and condition reporting are specified. The "> 10" support rule is removed.
- **S0:** scope reworded. It now has three integrity tiers, a float64 coverage table, a declared consequence for unavailable replay, and a minimum of 8 verified blocks with UNRESOLVED below it.
- **Prefix statement** corrected (credited to the CNA addendum). AC|BD is added as a descriptive sensitivity.
- **PR #5** recorded verbatim per L133. Wording changed to "available persisted checkpoints from PRs #7-#10".
- **f_init and R-FIX wording** corrected (L141–L142).
- **Pair rosters:** within-seed (1000) and same-arm cross-seed (1035), descriptive and kept separate.
- **Caps:** the 50-minute cumulative wall-clock cap is kept. The runtime estimate is updated on paper. INCOMPLETE replaces in-place reduction.
- **Disclosures** carried forward and extended (§12).
