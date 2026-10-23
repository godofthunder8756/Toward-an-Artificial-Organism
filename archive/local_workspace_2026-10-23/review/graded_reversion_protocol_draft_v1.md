# Graded joint recurrent reversion with oracle-referenced prefix-function loss: protocol (DRAFT v1)

> **DRAFT FOR ASTRA REVIEW. NOT FROZEN. NOT RUN.**
> - No phase A run has been made: no rollout, loss or curve has been computed on any checkpoint.
> - Nothing is committed, hashed as frozen, or pushed.
> - The only computations so far are the analytic construction checks in Appendix B: parameter shapes, displacement norms, the random-direction construction, trapezoid weights, and oracle-only scale. None touches a forecast.
>
> **This is a new study, not a reinterpretation of PR #7** (consult #14: "it is a new study, not a reinterpretation of this one"). It does not revise PR #7's failed SPECIFIC threshold. PR #7's labels stand, with errata E-1 to E-6 adopted as additive errata.
>
> **Phase A (EXPLORATORY, DEVELOPMENT ONLY, NEVER CONFIRMATORY)** uses the saved PR #7 checkpoints for seeds 100–109. It involves no training, so the Specialist states that standing authorization covers it. Even so, it runs only **after** this protocol's criterion text (§§3–8) has been hashed (§9.4).
>
> **Phase B (CONFIRMATION) trains fresh GRU-8 seeds 200–209 and needs Aidan's separate explicit training approval, which is STILL PENDING.**
> - No phase B training, and no scientific freeze that authorizes it, may occur before that approval is recorded with its date, time (ET) and source.
> - Appendix A (the wider rival grid) is further new training. It needs its own approval and does not gate anything here.

**Sources.**
- Astra consult #14 (`/workspace/astra_consult14_response.txt`; also "CONSULT #14 RESPONSE" in `astra_consult_5_raw.md`). It supplies the study recommendation, the path, the dose grid, the controls, the L_prefix definition, the claim ceiling and the localization ruling.
- FINAL protocol `/workspace/review/recurrent_core_transfer_protocol_FINAL.md`, sha256 `63c463c7b2df96d6feec49cfa34d1ec0f010ce017d4b31aab051f06af76e9506`. Its training recipe and integrity rules are inherited.
- PR #7: freeze `d118ae1` and results `5157f5d`, in the scratch clone `/workspace/scratch/pr7/clone`. Its code (`recurrent_core_transfer_*.py`) and checkpoints are under `recurrent_core_results_v1/checkpoints/`.
- Review `/workspace/review/rct_results_review_v1.md`, sha256 `1e68ead2…`.

**Scope guards.**
- GRU-8 only. This is the same `nn.GRU(9, 8)` + 8→32→3 family and the same W2 world.
- No new architecture family, and no protected controller or register.
- **Localization deprioritized** (consult #14): this study fits no decoder, searches no subspace, and runs no E3, P1 or P2. Consult #14: "Localization is not a prerequisite for demonstrating acquired causal organization."
- Below C4. No consciousness claim. No organism work.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate (§11).

---

## 0. Inherited, unchanged

Unless §§1–9 say otherwise, the following are inherited from FINAL §0.1 and §§1, 3 and 8 and from the PR #7 implementation:
- The W2 world, the exact oracle q* = `world.q`, the history probabilities P(h), and the TRAIN/TEST split (192/64).
- The input layout (INPUT_SIZE 9), the zero initial state, and float64 evaluation by exhaustive enumeration of all 256 histories.
- Bit order: reading k = bit (k−1) of h. So h = p + 16u, where p ∈ {0…15} is the prefix (readings 1–4) and u ∈ {0…15} is the continuation (readings 5–8).
- The training recipe, verbatim (FINAL §0.1; PR #7 `recurrent_core_transfer_train.py` at `d118ae1`):
  - 4000 steps, batch 256, Adam (0.9, 0.999, 1e-8), cosine learning rate 1e-3 → 1e-4, gradient clip 1.0;
  - ordinary outcome labels, with TEST rejection;
  - `set_num_threads(1)` and deterministic algorithms.
- Arms used here: **CAND** (source of W_T), **F-TRAINED** (W_T frozen, fresh 8→32→3 readout from torch seed 5000+s) and **F-INIT** (W_0 frozen, the same fresh readout initialization). The tuned rivals are not part of the main study (see Appendix A).
- The A-FIT gates, E1 prerequisite, transfer rule, validity rule, IDENTITY_TOL = 1e-9 and ε₀ = 1e-12 are those of FINAL §3.

## 1. Question and design

**Question (Q-CAUSE, organization level, bounded).** Does progressively and jointly removing the learned recurrent transformation, during continuation only and with the fresh readout fixed, increasingly disrupt the network's **correct use of earlier evidence**? Specifically, does it do so beyond matched random perturbations of the same per-block norm?

The measure is correctness of the prefix-dependent part of the forecast against the oracle, summarized over a predeclared dose path (§6). No favorable dose is selected afterward.

**Why this design (consult #14).**
- PR #7 showed transfer (Q-LEARN) and basic intervention dependence.
- Its single-matrix, endpoint, total-loss criterion was not met.
- A graded joint path can expose distributed contributions and endpoint saturation "without searching for a convenient subspace or revising PR #7's failed threshold".

**What it is not.**
- It is not a localization study.
- It is not a test that W_hh "stores" content.
- It does not test necessity.

## 2. Phases, seed ranges and safeguards

| phase | seeds | weights | training | status of results |
| --- | --- | --- | --- | --- |
| **A: EXPLORATORY** | **100–109** (PR #7) | saved PR #7 checkpoints `s{s}_f_trained.ckpt` (W_T + fresh readout) and `s{s}_f_init.ckpt` (W_0 + its fresh readout), each sha256-verified before use (§9) | **none** | **development only; never confirmatory** |
| **B: CONFIRMATION** | **200–209** (fresh; disjoint from PR #5's 0–9 and PR #7's 100–109) | newly trained CAND → W_T; F-TRAINED; F-INIT | 3 runs × 10 seeds, PR #7 recipe unchanged | the only phase that can earn a §7 label |
| Appendix A (optional) | 200–209 | phase B inits | 47-configuration rival grid | secondary robustness; separate approval |

**Safeguards (binding).** The intent is that no phase A result can be presented as confirmatory.

- **S1. Freeze-before-A.** The scientific criterion is fixed before any phase A output exists. It covers §3 (path and doses), §4 (controls and generators), §5 (outcomes and weighting), §6 (statistic, eligibility and thresholds), §7 (labels) and §8 (claim wording). This draft must be reviewed by Astra, the review edits applied, and the text sha256-hashed before phase A runs. At the latest, the criterion must be hashed **before any phase B training**. This draft chooses the stricter of these: before phase A.
- **S2. Separate label namespace.**
  - Every phase A output carries the prefix **"EXPLORATORY (PHASE A, PR #7 SEEDS 100–109; DEVELOPMENT ONLY; NOT CONFIRMATORY)"**.
  - Phase A never uses the words REPLICATED, DEMONSTRATED, SHOWN or CONFIRMED.
  - It reports per-seed numbers and curves with **no** count-out-of-ten verdict line.
  - The §7 labels can be produced only from phase B seeds 200–209.
- **S3. No carry-over of tuned thresholds.** No scientific parameter may be changed on the basis of phase A outputs, other than as provided in S4. This covers the dose grid, the number of random directions, generator seeds, the outcome definition, the weighting, the statistic, the materiality fraction, the eligibility rules and the replication count.
- **S4. If a change is unavoidable** (e.g. a defect revealed by phase A):
  - it is a new protocol version, reviewed by Astra and hashed before phase B training;
  - its deviation log states what phase A showed;
  - every phase B label and the claim carry the suffix **"(CRITERION REVISED AFTER EXPLORATORY PHASE A)"**.
- **S5. Engineering-only fixes** (bugs that do not touch any S3 parameter) are logged in `DEVIATIONS_AND_AMBIGUITIES` with the phase A evidence that revealed them. They need no suffix, but Astra is told.
- **S6. Pre-exposure disclosure.** Seeds 100–109 are not naive: PR #7's single-block endpoint results (r/z/n, α = 1, TEST E_total) are already known. Phase A reports must say so.
- **S7. Seed accounting.**
  - Phase B uses exactly 200–209, and no seed is replaced or added. Missing cells are reported.
  - Phase A seeds may never be pooled with phase B seeds in any count, mean or test.
- **S8. Separate artifacts.**
  - Phase A outputs are written to `graded_reversion_phaseA_exploratory/`, with "EXPLORATORY" in every file header.
  - Phase B outputs are written to `graded_reversion_results_v1/`.
  - The phase B results file cites phase A only in a separately headed "Development history" section.

## 3. Intervention path

**Target matrices.**
- **Primary:** the complete `rnn.weight_hh_l0` ∈ ℝ^{24×8} (W_hr, W_hz, W_hn stacked; rows 0–7, 8–15, 16–23).
- **Secondary:** each 8×8 block k ∈ {r, z, n} separately, with the other two blocks left at W_T.
- Biases (`bias_hh_l0`, `bias_ih_l0`) and `weight_ih_l0` stay trained and unchanged in every condition.

**Path (fixed).**
- W(α) = W_T + α (W_0 − W_T), with α ∈ 𝒜 = {0, 1/8, 1/4, 1/2, 3/4, 1}.
- W_T is the F-TRAINED core, which equals CAND's final recurrent weights. W_0 is CAND's initialization, which equals the F-INIT core. These were verified identical for seeds 100–109 (Appendix B).
- The computation is done in float64 from the stored float32 checkpoint values.
- For a secondary block k: W_hk(α) = W_hk^T + α δ_k, where δ_k = W_hk^0 − W_hk^T.

**When it applies.** The path applies at recurrent updates 5–8 only, i.e. `stage_idx` 4–7. This uses PR #7's `MatrixOverride` mechanism, with rows (0, 24) for the primary target and the block rows for the secondary ones. Updates 1–4 are intact.

**Readout.** The **fresh F-TRAINED readout is held fixed** at every dose. CAND's own readout is not used, even descriptively, in this study.

**Endpoint identity check.** ‖W(1) − W_0‖_max ≤ ε₀ and W(0) = W_T exactly. A failure invalidates the seed.

## 4. Controls

**Random directions.** There are 32 per seed. They are norm-matched **per gate block** and **reused across all doses**.
- **Generator:** `torch.Generator`, seed **40000 + 100·s**. This is disjoint from 1000+s, s, 5000+s, 6000+s, 9000-series and 30000+d.
- **Draws:** j = 1…32, in order. Each draw is one `torch.randn((24, 8), dtype=float64)` tensor E_j.
- **Per-block rescaling:** for k ∈ {r, z, n}, rows of block k are rescaled to Frobenius norm ‖δ_k‖_F, giving ε_j. As a consequence, ‖ε_j‖_F = ‖δ‖_F.
- **Random paths:**
  - primary: W_rand,j(α) = W_T + α ε_j;
  - secondary block k: W_hk^T + α ε_j[k], using **the same draw's block**.
- **Displacement too small.** If ‖δ_k‖_F ≤ ε₀ for any k, that seed is **not evaluable** (non-pass) for the primary target and for block k.
- **What the comparison is.** It is an empirical directional comparison against 32 prespecified draws. It is not a calibrated significance test, and reversion toward initialization is not exchangeable with isotropic directions (FINAL §5).

**Integrity checks (no evidential role; consult #12 and #14).**
- **SHAM:** the override hook substitutes a copy of W_T at steps 5–8, which is α = 0 through the hook. Forecasts must equal intact within ε₀.
- **RESTORE:** after α = 1, remove the override and rerun. The result must reproduce intact within IDENTITY_TOL.
- **ENDPOINT:** as in §3.
- **Checkpoints:** sha256 values must match. In phase A they are checked against `seeds/s{s}.json` at `5157f5d`; in phase B, against the phase B manifest.
- **Outputs:** finite and in (0, 1) at every dose and every direction.
- Any failure makes the seed **invalid** for §§6–7.
- Restoration is not rescue evidence.

## 5. Outcomes

Write f(p, u) ∈ (0, 1)³ for the forecast vector (X, Y, XOR) of history h = p + 16u under a given condition, and q*(p, u) for the oracle.

**Primary: oracle-referenced prefix-function loss** (consult #14). Consult #14 notes its formula was "transcribed from garbled rendering"; confirming it is open point O1. It is computed on the complete uniform 16×16 grid:

  L_prefix = (1/256) Σ_{p,u} ‖ [f(p,u) − f̄(u)] − [q*(p,u) − q̄*(u)] ‖²,

with f̄(u) = (1/16) Σ_p f(p,u) and q̄*(u) = (1/16) Σ_p q*(p,u).
- The value is 0 if and only if the forecast's prefix-dependent part equals the oracle's.
- A prefix-blind forecast scores exactly PD(q*).

**Secondary and descriptive outcomes.** All are reported at every dose and for every direction. None gates a label.
- **L_cont** is the analogous continuation quantity: (1/256) Σ ‖[f − f̃(p)] − [q* − q̃*(p)]‖², where f̃(p) and q̃*(p) are means over u.
- **L_prefix^XOR, L_prefix^X and L_prefix^Y** are the per-component terms of L_prefix. **XOR is reported separately** throughout: as L_prefix^XOR, as L_cont^XOR, and as the TEST XOR excess.
- **Linkage to PR #7:** the TEST and TRAIN excesses E_total, X, Y and XOR.
- **PD and CD** (FINAL §5): forecast variation, which is not correctness.
- **Probability-weighted versions** of L_prefix and L_cont, using P(p,u) with conditional means under P.
- **TEST-restricted versions**, with means taken within u (or p) over TEST members. This is descriptive, because the split couples p and u.

**Oracle scale** (computed in Appendix B; oracle only):
- PD(q*) = 0.013839 uniform, of which XOR is 0.010095, X 0.003046 and Y 0.000697. So about 73% of the oracle's prefix-dependent structure is in XOR.
- CD(q*) = 0.14172.

**Why the complete grid.** L_prefix uses all 256 histories, so it includes TRAIN histories. It measures the network's prefix *function*, not held-out generalization. Held-out loss is reported through the TEST excesses. Open point O2 asks whether this is the right primary weighting.

## 6. Curve-level statistic and per-seed criterion (declared in advance)

**Dose-loss curve.** For a condition c (REV, or random direction j):
- Δ_c(α) = L_prefix(c, α) − L_prefix(F-TRAINED intact).
- By the SHAM check, Δ_c(0) = 0 within ε₀.

**Statistic: trapezoidal area under the dose-excess curve over α ∈ [0, 1].**
- AUC_c = Σ_{α∈𝒜} w_α Δ_c(α), with trapezoid weights w = (1/16, 1/8, 3/16, 1/4, 1/4, 1/8) for α = (0, 1/8, 1/4, 1/2, 3/4, 1). The weights sum to 1 (Appendix B).
- AUC_c is therefore the dose-averaged excess prefix-function loss.
- There is a single statistic per target. No dose is selected, and no maximum over doses is taken.

**Prefix-function benefit (scale reference).**
- B_prefix = L_prefix(F-INIT) − L_prefix(F-TRAINED). These are the two fresh-readout arms, each with its own readout, so the α = 1 condition, which keeps the F-TRAINED readout, is **not** F-INIT.
- B_prefix is a scale reference only.

**Eligibility (seed must satisfy all; otherwise non-pass, not invalid).**
1. It is valid (§4).
2. It passes FINAL §3 transfer, recomputed on that seed: F-TRAINED A-FIT on TEST and E(F-TRAINED) ≤ ½ E(F-INIT).
3. B_prefix > ε₀.
4. ‖δ_k‖_F > ε₀ for all k (primary) or for the block in question (secondary).

**Per-seed GRADED-SPECIFIC(target).** Both conditions must hold:
- **(D) Directional:** AUC_REV > AUC_rand,j for **every** j = 1…32, i.e. rank 1 of 33.
- **(M) Materiality:** AUC_REV > ε₀ **and** AUC_REV ≥ **B_prefix / 4**.
  - The dose-averaged excess must reach at least a quarter of the training-attributable prefix-function benefit.
  - A curve that rises linearly to the full benefit at α = 1 has AUC = B_prefix/2, so this is stricter than PR #7's endpoint quarter rule applied to a linear curve. It is a conservative choice (§12).

**Descriptive curve diagnostics** (reported, never gating, and never used to pick a dose):
- Δ_REV(α) at each dose, and the per-dose rank of REV among the 33 curves.
- Monotonicity: the number of non-decreasing steps out of 5.
- Saturation index Δ(½)/Δ(1), using the E3-v2 ratio rule.
- The same curves for L_cont, L_prefix^XOR and E_total.
- Random-curve summaries: median, maximum and the full 32 values.

## 7. Labels and verdicts

**Phase B only (seeds 200–209).**
- **Prerequisites.**
  - E1 must be REPLICATED (FINAL §3), or the study is **UNRESOLVED (E1 not replicated)** and §§6–7 are descriptive.
  - Transfer is labelled as in FINAL §3, reported as a replication. If it is NOT SHOWN, the primary label is reported as below but the claim uses §8's transfer-failure branch.
- **Primary label (weight_hh):**
  - **"GRADED JOINT RECURRENT REVERSION EXCEEDS MATCHED RANDOM PERTURBATION (PREFIX FUNCTION): REPLICATED"** if ≥ **8/10** phase B seeds are eligible **and** pass GRADED-SPECIFIC(weight_hh).
  - **"UNRESOLVED"** if more than **2** seeds are invalid. Invalid seeds count neither for nor against.
  - **"GRADED JOINT REVERSION CRITERION NOT MET"** for any other outcome. There is no intermediate band.
- **Secondary labels (r, z, n).** These use the same rule, per block, and are reported in full.
  - They are labelled "secondary" and **cannot substitute for or upgrade the primary**. There is no "any k" upgrade.
  - The success wording appears only after the primary result, introduced by "Secondary (block-wise):".
- **Count semantics (E-3 lesson).** Every count is printed as "n/10 seeds **passed**". Per-condition counts are printed as D/M/joint. Wording is "below the declared materiality threshold", never "immaterial".

**Phase A (seeds 100–109).**
- The only allowed headline is **"EXPLORATORY (PHASE A …; NOT CONFIRMATORY): per-seed curve results"**.
- It gives per-seed D/M flags with **no** aggregate verdict.
- It may not be cited as support for any claim in §8.

## 8. Claim assembly (fixed in advance)

**Primary REPLICATED, with TRANSFER SHOWN (phase B):**

> "In W2, across 10 freshly trained GRU-8 seeds, progressively interpolating the complete learned hidden-to-hidden weight matrix toward its initialization during readings 5–8, with a fresh readout held fixed, increased oracle-referenced prefix-function loss (averaged over a predeclared dose path) more than each of 32 block-norm-matched random weight paths, and by at least one quarter of the training-attributable prefix-function benefit, in at least 8/10 seeds."

Appended separately:
- the transfer replication;
- the secondary block results;
- the L_cont, XOR and E_total curves (descriptive);
- the phase A exploratory note;
- the suffix from S4, if applicable.

This supports **Q-CAUSE at the organization level (bounded)**: jointly removing the learned recurrent transformation selectively disrupts correct use of earlier evidence beyond matched perturbations. It does not establish localized content, a mechanism, or necessity.

**Primary not met (TRANSFER SHOWN):**

> "In W2, recurrent training produced a GRU-8 core whose predictive advantage over its matched initialization survived readout replacement in [n]/10 fresh seeds. Graded joint recurrent reversion did not meet the prespecified curve-level criterion for prefix-function loss ([n]/10 seeds passed; directional [d]/10, materiality [m]/10)."

Append the secondary results and the descriptive curves. Consult #14's distinction applies: **basic intervention dependence** (forecast or loss changes under the specified weight changes) is reported as measured. Do **not** write "no causal effect" or "generic damage".

**UNRESOLVED:** "Graded joint recurrent reversion was UNRESOLVED (more than 2 invalid seeds)."

**TRANSFER NOT SHOWN:** use the FINAL §9 Q7 failure wording. The reversion results are then descriptive.

**Never claimed:**
- that weight_hh or any block "stores" prefix or chart content;
- localized or independently manipulable state;
- a gate-pathway mechanism;
- irreducible joint state;
- necessity of recurrent training (Q-NECESSITY);
- uniqueness;
- other architectures or budgets;
- any phase A result as confirmation;
- any change to PR #5 or PR #7 labels;
- C4, C5, consciousness or organism conclusions.

## 9. Integrity, determinism, reporting and freeze sequence

1. One process, deterministic algorithms, `set_num_threads(1)`, float64 evaluation, exhaustive 256-history enumeration.
2. **Generator seeds:**
   - phase B: s for initialization; 1000+s for episodes; 5000+s for fresh readouts;
   - random directions: 40000+100·s.
3. **Every table lists:**
   - all 10 seeds, both curves (REV and all 32 random), and all doses;
   - the primary target and r, z, n;
   - all outcomes (§5);
   - sham, restore and endpoint gaps;
   - eligibility flags, B_prefix, and invalid counts.

   Missing cells are reported, and no seed is replaced.
4. **Freeze sequence:**
   1. Astra review of this draft.
   2. Apply the edits and write the FINAL text.
   3. Hash the FINAL text, the code, and a test suite. The suite checks:
      - parameter counts (456/387/843);
      - path endpoints;
      - trapezoid weights;
      - random-direction block norms and generator seeds;
      - the L_prefix identities (L_prefix(q*) = 0; prefix-blind = PD(q*));
      - sham, restore and endpoint identity;
      - the label and claim strings.
   4. Phase A (exploratory).
   5. **Aidan's explicit phase B training approval**, recorded with time and source.
   6. Phase B training and evaluation.
   7. Results, with phase A in a separate development section.

   If a step-4 finding forces a change, S4 applies before step 6.

## 10. Thirteen admission answers

1. **Q1.** Q-CAUSE at the organization level (bounded): does the learned recurrent transformation, removed jointly and gradually, causally support correct use of earlier evidence beyond matched perturbations? This is a bounded prerequisite of the C3-type acquisition question. Q-LEARN appears only as a replicated prerequisite.
2. **Q2.** One hypothesis: in fresh seeds, the trapezoidal dose-averaged increase in oracle-referenced prefix-function loss under W_T → W_0 interpolation of the complete weight_hh at steps 5–8 exceeds that of all 32 block-norm-matched random paths **and** reaches ≥ B_prefix/4, jointly in ≥ 8/10 eligible valid seeds.
3. **Q3.** The falsifiers are:
   - "GRADED JOINT REVERSION CRITERION NOT MET" in phase B;
   - E1 not replicated, which gives UNRESOLVED;
   - more than 2 invalid seeds, which gives UNRESOLVED.

   Phase A outcomes falsify nothing and confirm nothing.
4. **Q4.** The strongest simpler explanations:
   - generic sensitivity to weight displacement of the same per-block norm (32 random paths per seed, shared across doses);
   - readout–core mismatch, which REV and random paths share because both keep the readout tuned to W_T;
   - endpoint-only effects (handled by the curve statistic);
   - single-matrix sufficiency (secondary blocks);
   - harness artifacts (SHAM, RESTORE, ENDPOINT);
   - total-loss confounds (the outcome is prefix-function correctness, with continuation and XOR reported separately);
   - post-hoc dose selection (excluded; single predeclared statistic).
5. **Q5.** Why this study is needed now:
   - PR #7 established transfer and basic intervention dependence, but its single-block, endpoint, total-loss SPECIFIC criterion was not met (1/10, 3/10, 3/10 passes).
   - Consult #14 names this design as the single most valuable next study, ahead of the wider rival grid and localization.
6. **Q6.** On success, record the §8 claim and move the ledger (§11) to "Q-CAUSE, preregistered organization-level specificity: bounded support". Any mechanism or localization follow-up needs separate approval and a new protocol.
7. **Q7.** On failure: "The prespecified curve-level criterion was not met." Report basic intervention dependence as measured. Do not record "generic damage", "no causal role" or "not learned". Any change to doses, outcome or threshold is a new protocol.
8. **Q8.** Resources:
   - Phase A: evaluation only. Per seed, 6 doses × 33 paths × 4 targets = 792 enumerations of 256 histories, plus checks.
   - Phase B: 30 training runs of 4000 steps on CPU (CAND, F-TRAINED and F-INIT × 10), plus the same evaluation.
   - Appendix A, if approved: 47 selection runs, plus the R-TUNED843 refit and F-TUNED32, per seed, i.e. 490 runs.
   - No organism model.
9. **Q9.** Organizational: whether acquired recurrent organization plays a causal role in using earlier evidence. Engineering: training, the hook and enumeration. No substrate claim.
10. **Q10.** The claim ceiling is in §8, including the "Never claimed" list.
11. **Q11.** The cognitive layer is a C3-type history-integrating predictive state. C4 (internal evaluation dissociable from first-order inference) and C5 remain unsupported and untested.
12. **Q12.**
    - **Supplied:** the GRU cell and its initialization, the timing scaffold, the readout architecture, losses, the split, the oracle used for **evaluation** only (never for training), the dose grid and the random-direction family.
    - **Acquired:** W_T and its contribution.
    - **Selected:** nothing; no dose or direction is selected.
13. **Q13.** How the ledger moves:
    - **Primary REPLICATED:** from "basic intervention dependence; PR #7 specific criterion not met" to "learned recurrent transformation causally supports correct use of earlier evidence beyond matched perturbations (bounded, joint, not localized)".
    - **Not met:** the ledger is unchanged except that the curve-level criterion is added as not met.
    - Q-NECESSITY stays NOT_ESTABLISHED, and Q-EXIST is not addressed, in every case.

## 11. Q-separation and the ledger

| Item | ORIGIN | ROLE (if shown) | REDUCTION (literal, if not) | Question |
| --- | --- | --- | --- | --- |
| Transfer of W_T (phase B replication) | ACQUIRED | predictive advantage surviving readout replacement | "transferable benefit not demonstrated" | Q-LEARN (prerequisite only) |
| Joint learned weight_hh, steps 5–8 | ACQUIRED | dose-averaged prefix-function disruption beyond matched paths, ≥ B_prefix/4 | "prespecified curve-level criterion not met" | Q-CAUSE, organization level (bounded) |
| Basic intervention dependence | ACQUIRED | forecasts and loss change under specified weight changes (reported as measured) | — | Q-CAUSE, basic |
| Single blocks r, z, n | ACQUIRED | secondary, as above | as above | Q-CAUSE (secondary) |
| Necessity of recurrent training | NOT TESTED | — | — | Q-NECESSITY |
| Existence of an exact solution | PR #4 / PR #5 K-EXACT erratum | — | — | Q-EXIST (not addressed) |

## 12. Values chosen where consult #14 left them open (conservative)

| item | value chosen | reason |
| --- | --- | --- |
| Curve statistic | trapezoidal AUC of Δ(α) on 𝒜 | a single predeclared summary with no dose choice |
| Directional rule | beats all 32 (rank 1/33) | same as PR #7 and FINAL §5 |
| Materiality | AUC ≥ B_prefix/4 (and > ε₀) | stricter than the PR #7 endpoint rule for linear curves |
| Scale reference | B_prefix from the two fresh-readout arms | oracle-referenced, the same quantity as the outcome |
| Replication | ≥ 8/10; more than 2 invalid → UNRESOLVED; no intermediate band | inherited |
| Eligibility | valid + transfer pass + B_prefix > ε₀ + ‖δ_k‖ > ε₀; failures are non-pass | inherited from PR #7 deviation #12 logic |
| Primary weighting | uniform complete 16×16 grid | FINAL §5 precedent; prob-weighted and TEST-restricted versions descriptive |
| Random generator | torch, seed 40000+100·s, one 24×8 draw per j, per-block rescale; the secondary blocks reuse the same draw | the same directions across doses and targets |
| Phase B seeds | 200–209 | fresh and disjoint |
| Freeze point | before phase A (the stricter option) | S1 |
| Change after phase A | new version + Astra + label suffix | S3/S4 |
| Secondary blocks | reported, cannot upgrade the primary | no family upgrade |
| Readout | F-TRAINED fresh readout only; no CAND-readout runs | removes a forking path |
| Appendix A grid | union of 47 configurations on seeds 200–209 | consult #14 |

## 13. Open points for Astra

- **O1.** Please confirm the L_prefix formula (yours was transcribed from a garbled rendering), including whether f̄(u) and q̄*(u) are uniform means over p.
- **O2.** Primary weighting: is the uniform complete grid right? It includes TRAIN histories, so it measures function, not generalization. Should the probability-weighted version be primary instead?
- **O3.** Statistic: is trapezoidal AUC on 𝒜 acceptable? Alternatives are the uniform mean over doses, or Δ at α = 1 together with the AUC. Should α = 0 carry weight, given Δ(0) ≡ 0?
- **O4.** Materiality: is AUC ≥ B_prefix/4 right? Consider B_prefix/8, which would be equivalent to PR #7's endpoint rule for a linear curve, or a PD(q*)-relative floor. Should B_prefix ≤ ε₀ seeds be non-pass (as drafted) or invalid?
- **O5.** Directional rule: beat all 32 (rank 1/33), or a predeclared rank threshold such as ≥ 31/32? We kept the stricter rule.
- **O6.** Readout–core mismatch: REV and random paths share a readout tuned to W_T. Should a descriptive arm re-fit the readout at α = 1? (That would be training.)
- **O7.** Should transfer pass be required for eligibility in phase B? It was inherited; the alternative is to evaluate the curve criterion on all valid seeds.
- **O8.** Secondary blocks: is reusing each random draw's block for the secondary paths acceptable, rather than independent per-block draws?
- **O9.** Phase A scope: may phase A also report the PR #7-style endpoint per-block ΔE under the new generator? Should phase A be barred from computing B_prefix-relative flags, so that it shows curves only?
- **O10.** Appendix A: run it on the phase B seeds (as drafted), or on separate fresh seeds 300–309? Is the edge rule "g* = 8 or b* = −6 in ≥ 3/10 seeds" right?
- **O11.** Is 32 random paths enough at curve level, or should it be 64 (still evaluation-only)?

---

## Appendix A. Optional wider tuned-rival grid (secondary robustness; separate approval; no gate)

**Status:** new training. It needs Aidan's separate approval and Astra review. It answers a robustness question about the PR #7 tuned rival ("secondary to the causal question", consult #14). It does not alter PR #7's labels.

- **Family (unchanged):** the frozen GRU-8 at each seed's own W_0. Scale `weight_hh_l0 ← g·weight_hh_l0`, and offset the update gate with `bias_hh_l0[8:16] += b` (FINAL §2).
- **Grid:** the **union of 47 configurations**:
  - the original 9: {0.5, 1, 2} × {−2, 0, 2};
  - the extension 42: {1, √2, 2, 2√2, 4, 4√2, 8} × {−6, −4, −3, −2, −1, 0};
  - overlap 4: {1, 2} × {−2, 0}.

  The count is 9 + 42 − 4 = 47.
- **Seeds:** fresh phase B seeds 200–209, using phase B CAND for ratio843. Not 100–109 (consult #14: work on 100–109 is follow-up informed by their results).
- **Selection:** per seed, on the same balanced 48-history VAL set, with the exact-oracle VAL criterion (the declared selection advantage). The 8→70→3 readout uses torch seed 6000+s, 4000 steps, and the same tie-break order (smaller |log₂g|, then |b|, then b, then g).
- **Refit and evaluation:** refit on 192 TRAIN histories, and evaluate TEST once. F-TUNED32 inherits (g*, b*) and is descriptive.
- **Labels** are FINAL §4 (i)/(ii), each qualified as "within the declared 47-configuration grid".
- **Edge rule:**
  - If g* = 8 or b* = −6 in ≥ 3/10 seeds, report **"TUNED RIVAL STILL EDGE-LIMITED"**, with no further extension.
  - Selections at the original g = 0.5 or b = +2 boundaries are also reported.
  - Absence of boundary selections does not certify global optimality (consult #14).
- **Magnitudes for context** (consult #14, corrected): defeating the ≤ ½ advantage threshold needs about 4.8–17.1× rival improvement; approximately matching CAND needs 10–34×. The 1.8–2.5× figure concerns only A-FIT's total-error clause, not the XOR clause.
- **Compute (charged separately):** 47 × 4000 selection steps per seed, plus the refit and F-TUNED32.

## Appendix B. Analytic construction checks already run (scratch; no phase A)

Script output is at `/workspace/scratch/graded/construction_check.txt`. No rollout, loss or curve was computed.

- **Checkpoint shapes** (`s100_f_trained.ckpt`): `weight_hh_l0` 24×8, `weight_ih_l0` 24×9, `bias_hh/ih` 24 each, readout 32×8, 32, 3×32, 3. Stored as float32; evaluation is in float64.
- **W_0 identity.** F-INIT `weight_hh` equals CAND-init `weight_hh` exactly in 10/10 seeds. F-TRAINED `weight_ih` equals CAND-final in 10/10.
- **Displacement norms** (seeds 100–109):
  - ‖δ‖_F: 3.60–4.63;
  - ‖δ_r‖: 1.86–2.72;
  - ‖δ_z‖: 2.36–3.05;
  - ‖δ_n‖: 1.78–2.26;
  - for comparison, ‖W_T‖_F is 4.69–5.62 and ‖W_0‖_F is 2.77–2.99.

  No seed is near ε₀. The full path is long relative to ‖W_0‖, which is one reason intermediate doses are informative.
- **Random-direction construction** (numpy stand-in, because torch is not installed on the box; the frozen generator is torch):
  - per-block norm match error ≤ 4.4e-16, and ‖ε_j‖_F = ‖δ‖_F;
  - cos(ε_j, δ) ranges from −0.11 to 0.14 (SD 0.065, against 1/√192 = 0.072), i.e. near-orthogonal to the reversion direction, as expected.
- **Path endpoint:** ‖W(1) − W_0‖_max = 0 for seed 100.
- **Trapezoid weights** for 𝒜: (1/16, 1/8, 3/16, 1/4, 1/4, 1/8), summing to 1.
- **Oracle scale** (oracle only): PD(q*) = 0.013839 (X 0.003046, Y 0.000697, XOR 0.010095) and CD(q*) = 0.14172 on the uniform grid. P(h) > 0 for all h.
