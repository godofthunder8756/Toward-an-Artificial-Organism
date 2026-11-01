# Graded joint recurrent reversion with oracle-referenced prefix-function loss: protocol (FINAL v1)

> **FINAL TEXT FOR HASHING. NOT RUN.**
> - Astra consult #15 (FREEZE WITH NAMED EDITS) is applied in full (§0.1), together with its rulings on O1–O11 (§13).
> - No phase A run has been made: no rollout, loss or curve exists for any checkpoint. Nothing is committed, frozen or pushed in the repo.
> - The only computations are the analytic scratch checks in Appendix B. They use the oracle and synthetic forecasts only, plus checkpoint shapes and norms.
>
> **Authorization.**
> - **Phase A** (EXPLORATORY: evaluation only, on the saved PR #7 checkpoints, seeds 100–109, with no training) **is covered by standing authorization once this file has been hashed** (consult #15: "Phase A can proceed under its stated standing authorization after hashing").
> - **Phase B** (CONFIRMATION: fresh GRU-8 seeds 200–209) **still waits on Aidan's explicit training approval, which is PENDING.** No phase B training may occur before that approval is recorded with its date, time (ET) and source.
> - **Appendix A** (the wider rival grid) is further training and needs its own approval.
>
> **This is a new study, not a reinterpretation of PR #7.** PR #7's labels stand, with errata E-1 to E-6 adopted as additive errata (consult #14).

**Sources.**
- Astra consults #14 and #15:
  - `/workspace/astra_consult14_response.txt`
  - `/workspace/astra_consult15_response.txt`
  - both also appear in `astra_consult_5_raw.md`.
- Draft v1: `/workspace/review/graded_reversion_protocol_draft_v1.md`, sha256 `4d071a08d4e9f5cb21b1aea464a569b53047b815052b7aba6f2b365bef43dd94`, left untouched.
- Recurrent-core FINAL: `/workspace/review/recurrent_core_transfer_protocol_FINAL.md`, sha256 `63c463c7…`. It supplies the inherited recipe and integrity rules.
- PR #7: freeze `d118ae1`, results `5157f5d`, code `recurrent_core_transfer_*.py`.
- Review: `/workspace/review/rct_results_review_v1.md`.

**Scope guards.**
- GRU-8 only, in the same family and the same W2 world.
- No new architecture family, and no protected controller or register.
- **Localization is deprioritized** (consult #14). This study fits no decoder, searches no subspace, and runs no E3, P1 or P2.
- Below C4. No consciousness claim. No organism work.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate (§11).

---

## 0. Inherited, unchanged

Unless §§1–9 say otherwise, the following are inherited from recurrent-core FINAL §0.1, §1, §3 and §8 and from the PR #7 implementation:
- The W2 world, the exact oracle q_star = `world.q`, P(h), and the TRAIN/TEST split (192/64).
- INPUT_SIZE 9, the zero initial state, and float64 evaluation by exhaustive enumeration of all 256 histories.
- Reading k = bit (k−1) of h. So h = p + 16u, where p (readings 1–4) and u (readings 5–8) range over 0…15.
- **The training recipe, verbatim** (`recurrent_core_transfer_train.py` at `d118ae1`):
  - 4000 steps, batch 256, Adam (0.9, 0.999, 1e-8), cosine LR 1e-3→1e-4, clip 1.0;
  - ordinary outcome labels, with TEST rejection;
  - `set_num_threads(1)` and deterministic algorithms.
- **Arms:**
  - **CAND** is the source of W_T.
  - **F-TRAINED** is W_T frozen, with a fresh 8→32→3 readout from torch seed 5000+s.
  - **F-INIT** is W_0 frozen, with the same fresh readout initialization, trained separately.
  - The tuned rivals appear in Appendix A only.
- A-FIT, the E1 prerequisite, the transfer rule, the validity rule, IDENTITY_TOL = 1e-9 and eps0 = 1e-12 are taken from recurrent-core FINAL §3.

## 0.1 Edits applied (consult #15)

| # | Consult #15 edit (verbatim or closely paraphrased) | Where applied |
| --- | --- | --- |
| 1 | The exact ASCII L_prefix definition, with no division by three. Its consequences: L_prefix(q_star) = 0; prefix-blind = PD(q_star); L_prefix = 0 permits continuation-dependent error; L_prefix and L_cont overlap and are not additive. The complete uniform grid stays primary, and TEST errors are kept separate. | §5 |
| 2a | C_prefix = PD(q_star) − L_prefix(F-TRAINED). Eligibility needs C_prefix > eps0; otherwise the seed is a non-pass, not invalid. Report L_prefix(F-TRAINED), B_prefix and C_prefix both absolutely and divided by PD(q_star). | §6 |
| 2b | Keep B_prefix/4, with no PD-relative floor. A small baseline benefit stays visible in the continuous results. | §6 |
| 2c | "training-attributable prefix-function benefit" becomes "paired prefix-loss advantage over F-INIT after separate readout training", throughout. | §6, §8, §10 |
| 3a | AUC interpolant disclaimer, verbatim. Negative excesses are retained, with no clipping. The zero-dose weight is kept and nothing is renormalized. | §6 |
| 3b | Saturation-index rule, verbatim: UNDEFINED unless Delta_REV(1) > eps0. Signed values are kept, and the E3 ratio convention is not applied. | §6 |
| 3c | "D passes iff AUC_REV − max_j AUC_rand,j > eps0." | §6 |
| 3d | A linear curve ending at d has AUC = d/2, so M requires d ≥ B_prefix/2. This is stricter than an endpoint-quarter rule on the same outcome. It is **not directly comparable with PR #7**. | §6 |
| 4a | The α = 1 endpoint explanation, verbatim. | §3 |
| 4b | The readout and compatibility limitation, verbatim. It replaces "readout–core mismatch … handled". | §4, §10 Q4 |
| 5a | Displacement and zero-block rule, verbatim: primary eligibility needs ‖delta‖_F > eps0; a zero block gets a zero random perturbation; secondary eligibility needs ‖delta_k‖_F > eps0. | §4, §6 |
| 5b | Transfer and B_prefix > eps0 eligibility are kept. Eligibility failures are non-passes; integrity failures are invalid. | §6 |
| 5c | The denominator sentence, verbatim. It replaces "8/10 eligible valid seeds". | §7, §10 Q2 |
| 5d | Explicit precedence: E1 failure or more than two invalid seeds gives UNRESOLVED before the success count. | §7 |
| 6a | "increasingly disrupts" becomes "produces a positive dose-averaged disruption". "selectively" is removed from the interpretation and the ledger. | §1, §8, §10, §11 |
| 6b | Success paragraph and limitation sentence, verbatim. | §8 |
| 6c | Vector success does not establish an XOR-specific effect. XOR stays explicit but descriptive. | §5, §8 |
| 7a | Section order restored. It was already in order in the draft file (§0.2). | whole document |
| 7b | Engineering fixes are versioned and hashed before phase B. | §2 S5, §9 |
| 7c | Appendix A's oracle-assisted selection is marked as an exception to "oracle used only for evaluation". | §10 Q12, Appendix A |
| 7d | The ledger uses "criterion not met; no reduction identified" for failed criteria. | §11 |
| 7e | The NumPy check validates the rescaling algebra only. A test of the Torch draw sequence in the frozen implementation is required. | §4, §9, Appendix B |
| O1–O11 | Rulings applied. | §13 |

## 0.2 Section-order note

Consult #15 reported that §§5, 8–10, 12 and Appendix A were interleaved. The draft file on the box (`graded_reversion_protocol_draft_v1.md`, sha `4d071a08…`) was checked by its headings, and its order is §0–§13 followed by Appendices A and B, all in sequence. **The interleaving was an artifact of the chunked paste, not of the draft.** This FINAL text keeps the same sequential order.

---

## 1. Question and design

**Question (Q-CAUSE, organization level, bounded).** The intervention removes the learned recurrent transformation jointly and gradually, during continuation only, with the trained input weights, biases and fresh readout held fixed. Does it **produce a positive dose-averaged disruption** of the network's accurate prefix-dependent prediction, beyond matched random perturbations of the same per-block norm?

The outcome is the oracle-referenced prefix-function loss (§5), summarized over a predeclared dose path (§6). No dose is selected afterward.

**What a success does not show.**
- A success does not require, and does not establish, a monotonic dose response.
- It does not establish disruption that is preferential relative to continuation processing; L_cont is descriptive.

**Not:**
- localization;
- a "stores content" claim;
- a necessity test;
- an XOR-specific test.

## 2. Phases, seed ranges and safeguards

| phase | seeds | weights | training | results status |
| --- | --- | --- | --- | --- |
| **A: EXPLORATORY** | **100–109** (PR #7) | `s{s}_f_trained.ckpt`, `s{s}_f_init.ckpt` and `s{s}_cand_init.ckpt` at `5157f5d`, sha256-verified | none | **development only; never confirmatory**. Covered by standing authorization after this file is hashed |
| **B: CONFIRMATION** | **200–209** (fresh; disjoint from 0–9 and 100–109) | newly trained CAND → W_T, F-TRAINED, F-INIT | 3 runs × 10 seeds, PR #7 recipe unchanged | the only phase that can earn a §7 label. **Needs Aidan's explicit training approval (pending)** |
| Appendix A (optional) | 200–209 | phase B inits | 47-configuration rival grid | secondary robustness. **Separate approval** |

**Safeguards (binding).**

- **S1. Freeze before phase A.** This text, the code and the test suite (§9) are hashed before any phase A output exists. The criterion therefore exists before both phases.
- **S2. Separate label namespace.**
  - Every phase A output is prefixed **"EXPLORATORY (PHASE A, PR #7 SEEDS 100–109; DEVELOPMENT ONLY; NOT CONFIRMATORY)"**.
  - Phase A never uses REPLICATED, DEMONSTRATED, SHOWN or CONFIRMED.
  - Phase A gives no out-of-ten verdict line.
  - §7 labels are produced only from seeds 200–209.
- **S3. No carry-over of parameters tuned on phase A.** Scientific parameters may not change on the basis of phase A outputs. These are the dose grid, the number of random directions, the generator seeds, the outcome definition and weighting, the statistic, the eligibility rules, the materiality fraction and the replication rule.
- **S4. Scientific changes after phase A.** Any such change is a new protocol version, reviewed by Astra and hashed before phase B training. Its deviation log states what phase A showed. Every phase B label and the claim then carry **"(CRITERION REVISED AFTER EXPLORATORY PHASE A)"**.
- **S5. Engineering-only fixes** (bugs that touch no S3 parameter) carry no S4 suffix, but **they are versioned and hashed before phase B** (consult #15).
  - Each is logged in `DEVIATIONS_AND_AMBIGUITIES`, with the phase A evidence that revealed it, and Astra is told.
  - Phase A outputs made under superseded code are retained and labelled with their code version.
- **S6. Pre-exposure disclosure.** Seeds 100–109 are not naive, because PR #7's single-block, endpoint TEST E_total results are known.
- **S7. Seed accounting.**
  - Phase B uses exactly 200–209. No seed is replaced or added, and missing cells are reported.
  - Phase A seeds are never pooled with phase B seeds.
- **S8. Separate artifacts.**
  - Phase A outputs go to `graded_reversion_phaseA_exploratory/`, with "EXPLORATORY" in every file header.
  - Phase B outputs go to `graded_reversion_results_v1/`. They cite phase A only in a separately headed "Development history" section.
- **S9. Phase A reporting scope (O9).**
  - Phase A may report endpoint block errors and B-relative D and M flags, explicitly as exploratory, per seed only.
  - Pooling across seeds, and use as confirmation, remain prohibited.

## 3. Intervention path

**Targets.**
- **Primary:** the complete `rnn.weight_hh_l0` (24×8: W_hr, W_hz, W_hn stacked; rows 0–7, 8–15, 16–23).
- **Secondary:** each 8×8 block k ∈ {r, z, n}, with the other blocks left at W_T.
- `weight_ih_l0`, `bias_ih_l0` and `bias_hh_l0` stay trained in every condition.

**Path.**
- W(α) = W_T + α·(W_0 − W_T), for α ∈ 𝒜 = {0, 1/8, 1/4, 1/2, 3/4, 1}.
- The computation is in float64, from the stored float32 values.
- W_T is the F-TRAINED core, which equals CAND's final recurrent weights. W_0 is CAND's initialization, which equals the F-INIT core.
- For a secondary block: W_hk(α) = W_hk^T + α·delta_k, where delta_k = W_hk^0 − W_hk^T. The full displacement is delta = W_0 − W_T.

**When applied.** At recurrent updates 5–8 only (`stage_idx` 4–7), using PR #7's `MatrixOverride`. The rows are (0, 24) for the primary target and the block rows for the secondary ones. Updates 1–4 are intact.

**Readout.** The fresh F-TRAINED readout is held fixed at every dose. CAND's own readout is not used.

**α = 1 endpoint (consult #15, verbatim):**
> "At alpha=1, only the hidden-to-hidden matrices during updates 5–8 equal their initialization. Input-to-hidden weights, biases, updates 1–4 and the fresh readout remain trained. This condition is not F-INIT, even apart from the readout difference."

**Endpoint identity check.** ‖W(1) − W_0‖_max ≤ eps0, and W(0) = W_T exactly. A failure makes the seed invalid.

## 4. Controls

**Random directions.** There are 32 per seed. They are matched per gate block in norm and reused across every dose and target.
- **Generator:** `torch.Generator`, seed **40000 + 100·s**. This is disjoint from 1000+s, s, 5000+s, 6000+s, the 9000-series and 30000+d.
- **Draws:** j = 1…32 in order, each one `torch.randn((24, 8), dtype=torch.float64, generator=...)` call giving E_j.
- **Displacement and zero-block rule (consult #15, verbatim):**
  > "Primary eligibility requires ||delta||_F > eps0. A block with exactly zero displacement receives a zero random perturbation. Nonzero blocks are rescaled to their own displacement norm. Secondary eligibility requires ||delta_k||_F > eps0 for the tested block."

  "Exactly zero displacement" is implemented as ‖delta_k‖_F ≤ eps0 (§12).
- **Rescaling:** for each block k with ‖delta_k‖_F > eps0, the rows of block k of E_j are rescaled to Frobenius norm ‖delta_k‖_F. The result is eps_j, and ‖eps_j‖_F = ‖delta‖_F.
- **Paths:**
  - primary: W_rand,j(α) = W_T + α·eps_j;
  - secondary block k: W_hk^T + α·eps_j[k], using the same draw's block (O8).
- **Correlation (O8).** The secondary results are correlated with each other and with the primary. They are not independent replications.
- **Status of the comparison.** It is empirical and directional, not a calibrated p-value (O5). Reversion toward initialization is not exchangeable with isotropic directions.

**Readout and compatibility limitation (consult #15, verbatim):**
> "Holding the same readout fixed in REV and random conditions controls readout identity, but does not eliminate differential disruption of compatibility among recurrent matrices, input weights, biases and the readout."

This bounds the explanation. It does not invalidate the experiment.

**Draw-sequence test (consult #15).** The NumPy construction check in Appendix B validates the rescaling algebra only. **The frozen implementation's test suite must test the Torch draw sequence itself.** It must:
- regenerate the 32 draws per seed twice in separate processes and require byte-identical float64 arrays;
- record the sha256 of the concatenated draws for each seed in the freeze manifest before any phase A output;
- check per-block norms within 1e-12 relative tolerance;
- check zero-block handling on a synthetic delta.

**Integrity checks (no evidential role).**
- **SHAM:** the hook substitutes a copy of W_T at steps 5–8. Forecasts must equal intact within eps0.
- **RESTORE:** after α = 1, remove the override and rerun. The result must reproduce intact within IDENTITY_TOL.
- **ENDPOINT:** as in §3.
- **Checkpoints:** sha256 must match. Phase A checks against `seeds/s{s}.json` at `5157f5d`, or the committed file hash for `cand_init`. Phase B checks against its own manifest.
- **Outputs:** finite and in (0, 1) at every dose and direction.

Any failure makes the seed **invalid**. Restoration is not rescue evidence.

## 5. Outcomes

**Primary: oracle-referenced prefix-function loss (consult #15, exact ASCII definition):**

```
p, u = 0,...,15
t in {X, Y, XOR}

f_bar_u[u,t] = (1/16) * sum_p f[p,u,t]
q_bar_u[u,t] = (1/16) * sum_p q_star[p,u,t]

L_prefix(f) =
    (1/256) * sum_p sum_u sum_t
    (
        (f[p,u,t]      - f_bar_u[u,t])
        -
        (q_star[p,u,t] - q_bar_u[u,t])
    )^2
```

- f[p,u,t] is the forecast of output t for history h = p + 16u under the given condition. q_star is the oracle.
- **There is no division by three over output components.** Both means are uniform over prefixes (O1).

**Properties (consult #15).** L_prefix measures the variation across prefixes of the forecast error, holding the continuation fixed. Consequently:
- L_prefix(q_star) = 0.
- Every prefix-blind forecast has L_prefix = PD(q_star).
- L_prefix = 0 permits an arbitrary continuation-dependent forecast error. It does not imply globally correct forecasts.
- L_prefix and L_cont overlap through prefix–continuation interactions. They are not an additive decomposition of total error.

These were verified analytically in Appendix B.

**Weighting (O2).**
- The complete uniform 16×16 grid is primary. It measures the forecast **function**, including trained histories.
- The primary causal statistic is **not** described as held-out generalization.
- TEST prediction errors are reported separately.

**Secondary and descriptive outcomes.** All are reported at every dose and for every path. None gates a label.
- **L_cont:** the same form, with means over u for each p.
- **Per-component terms** L_prefix^X, ^Y and ^XOR; L_cont components; the TEST XOR excess.
  - **XOR is reported explicitly but descriptively.** Vector success does not establish an XOR-specific effect.
- **TEST and TRAIN excesses** E_total, X, Y and XOR (linkage to PR #7). Endpoint loss is descriptive (O3).
- **PD and CD** (forecast variation, not correctness).
- **Probability-weighted and TEST-restricted** versions of L_prefix and L_cont.

**Oracle scale (Appendix B):** PD(q_star) = 0.013839 (X 0.003046, Y 0.000697, XOR 0.010095) and CD(q_star) = 0.14172.

## 6. Curve statistic and per-seed criterion (declared in advance)

**Dose-excess curve.** For a condition c (REV, or random path j):
- Delta_c(α) = L_prefix(c, α) − L_prefix(F-TRAINED intact).
- Delta_c(0) = 0 within eps0 (SHAM).

**AUC.** AUC_c = Σ_{α∈𝒜} w_α · Delta_c(α), with:

```
alpha:   0     1/8    1/4    1/2    3/4    1
weight:  1/16  1/8    3/16   1/4    1/4    1/8
```

- The zero-dose weight is kept, and nothing is renormalized after dropping its zero contribution (O3).
- There is one statistic per target. No dose is selected, and no maximum is taken over doses.

> "AUC is the integral of the piecewise-linear interpolant through the six measured dose-excess values. It is not a certified integral of the network's continuous dose response. Negative excesses are retained; no clipping or absolute-value transformation is applied."

**Baselines (reported for every seed, absolutely and divided by PD(q_star)).** L_prefix(F-TRAINED), B_prefix and C_prefix.
- **B_prefix** = L_prefix(F-INIT) − L_prefix(F-TRAINED). It is the **paired prefix-loss advantage over F-INIT after separate readout training**. It does not attribute the whole advantage specifically to weight_hh.
- **C_prefix** = PD(q_star) − L_prefix(F-TRAINED). This establishes that the intact trained core's prefix-dependent forecast is more accurate than the prefix-blind reference.

**Eligibility.** A failure is a **non-pass, not invalid**.
1. Valid (§4).
2. Passes recurrent-core FINAL §3 transfer, recomputed on that seed: F-TRAINED A-FIT on TEST, and E(F-TRAINED) ≤ ½·E(F-INIT) (O7).
3. B_prefix > eps0. Nonpositive B is a non-pass (O4).
4. **C_prefix > eps0** (consult #15).
5. Primary: ‖delta‖_F > eps0. Secondary block k: ‖delta_k‖_F > eps0.

Curves are still reported for valid seeds that fail eligibility. They are never upgraded into confirmatory passes (O7).

**Per-seed GRADED-SPECIFIC(target).** Both conditions must hold.
- **(D) Directional:** "D passes iff AUC_REV − max_j AUC_rand,j > eps0."
- **(M) Materiality:** AUC_REV > eps0 **and** AUC_REV ≥ B_prefix/4.
  - There is no additional PD-relative floor. A small baseline benefit stays visible in the continuous results through the reported B_prefix/PD(q_star) and C_prefix/PD(q_star).
  - For a linear excess curve ending at d, AUC = d/2, so M requires d ≥ B_prefix/2. That is stricter than an endpoint-quarter rule on the same outcome and baseline. It is **not directly comparable** with PR #7's different outcome and scale.

**Descriptive diagnostics** (never gating, never used to pick a dose):
- Delta_REV(α) at each dose, and the per-dose rank of REV among the 33 paths.
- The number of non-decreasing steps out of 5. Monotonicity is descriptive only, and AUC success does not require it.
- **Saturation index (consult #15, verbatim):** "Report Delta_REV(1/2) / Delta_REV(1) only when Delta_REV(1) > eps0; otherwise report UNDEFINED. Negative numerators remain signed. Do not apply the nonnegative E3 ratio convention to signed loss differences."
- The same curves for L_cont, the L_prefix components and E_total.
- Random-path summaries: median, maximum and all 32 values.

## 7. Labels and verdicts

**Phase B only (seeds 200–209). Precedence is evaluated in this order:**
1. **E1 not replicated** (recurrent-core FINAL §3) gives **"UNRESOLVED (E1 not replicated)"**. Sections 6–7 are then descriptive.
2. **More than two invalid seeds** gives **"UNRESOLVED"**.
3. Only then is the success count evaluated (consult #15, verbatim):
   > "At least eight of the ten prespecified phase-B seeds jointly satisfy validity, eligibility, D and M. The denominator remains ten; seeds are not removed from it."

**Labels.**
- **Primary (weight_hh):**
  - **"GRADED JOINT RECURRENT REVERSION EXCEEDS MATCHED RANDOM PERTURBATION (PREFIX FUNCTION): REPLICATED"** if the count rule holds.
  - Otherwise **"GRADED JOINT REVERSION CRITERION NOT MET"**. There is no intermediate band.
- **Transfer** (recurrent-core FINAL §3 rule) is reported as a replication. Because eligibility includes a per-seed transfer pass, primary REPLICATED implies at least 8/10 transfer passes.
- **Secondary (r, z, n):**
  - The same rule and precedence, per block, with the label prefix "Secondary (block-wise):".
  - They are correlated with the primary (O8). They cannot substitute for or upgrade it, and there is no "any k" upgrade.
- **Counts** are printed as "n/10 seeds **passed**", with D/M/joint counts out of ten. Wording is "below the declared materiality threshold", never "immaterial".

**Phase A (seeds 100–109).**
- The only allowed headline is "EXPLORATORY (PHASE A …; NOT CONFIRMATORY): per-seed curve results".
- It gives per-seed D/M flags and endpoint block errors (S9), with no aggregate verdict.
- It is never cited as support for a §8 claim.

## 8. Claim assembly (fixed in advance)

**Primary REPLICATED (phase B).** The success paragraph (consult #15, verbatim):

> "In W2, interpolation of the complete hidden-to-hidden matrix toward its initialization during updates 5–8, with trained input weights, biases and a fresh readout held fixed, increased oracle-referenced prefix-function loss over the predeclared dose grid. In at least eight of ten fresh seeds, the trapezoidal excess exceeded that of every one of 32 block-norm-matched random paths and reached at least one quarter of the paired prefix-loss advantage over F-INIT. The intact trained cores also outperformed the prefix-blind reference."

Then append (consult #15, verbatim):

> "This supports a bounded causal contribution of the trained hidden-to-hidden parameters to accurate prefix-dependent prediction under the specified intervention and fixed surrounding computation. It does not establish monotonicity, selectivity over continuation processing, localized content, necessity, or a uniquely identified mechanism."

Appended separately:
- the transfer replication;
- the secondary block results (correlated);
- the L_cont, XOR and E_total curves, descriptive. **Vector success does not establish an XOR-specific effect.**
- the phase A exploratory note;
- the S4 suffix, if applicable.

**Primary not met:**

> "Graded joint recurrent reversion did not meet the prespecified curve-level criterion for prefix-function loss ([n]/10 seeds passed; directional [d]/10, materiality [m]/10; eligibility failures [e]/10)."

- Add the transfer replication line and the secondary and descriptive results.
- Basic intervention dependence (forecast or loss changes under the specified weight changes) is reported as measured.
- Do **not** write "no causal effect", "generic damage" or "not learned".

**UNRESOLVED:** "Graded joint recurrent reversion was UNRESOLVED ([E1 not replicated | more than two invalid seeds])."

**Never claimed:**
- that weight_hh or any block "stores" content;
- localized or independently manipulable state;
- a gate-pathway mechanism;
- monotonicity;
- selectivity over continuation processing;
- an XOR-specific effect;
- irreducible joint state;
- necessity (Q-NECESSITY);
- uniqueness;
- other architectures or budgets;
- any phase A result as confirmation;
- any change to PR #5 or PR #7 labels;
- C4, C5, consciousness or organism conclusions.

## 9. Integrity, determinism, reporting and freeze sequence

1. One process, deterministic algorithms, `set_num_threads(1)`, float64 evaluation, exhaustive 256-history enumeration.
2. **Generator seeds:**
   - phase B: s for initialization, 1000+s for episodes, 5000+s for fresh readouts;
   - random directions: 40000+100·s;
   - Appendix A only: 6000+s.
3. **Tables list:**
   - all 10 seeds, the REV path and all 32 random paths, at all doses;
   - the primary target and r, z, n;
   - all §5 outcomes;
   - sham, restore and endpoint gaps;
   - eligibility flags;
   - L_prefix(F-TRAINED), B_prefix and C_prefix, both absolute and divided by PD(q_star);
   - invalid counts.

   No seed is replaced, and missing cells are reported.
4. **The test suite (hashed with the code) checks:**
   - parameter counts (456/387/843);
   - path endpoints;
   - trapezoid weights;
   - **the Torch random-direction draw sequence** (§4), plus block norms and zero-block handling;
   - the L_prefix identities: L_prefix(q_star) = 0; prefix-blind = PD(q_star); continuation-only error gives 0;
   - C_prefix and B_prefix signs on synthetic cases;
   - the D margin, the M rule and the saturation UNDEFINED rule;
   - verdict precedence;
   - sham, restore and endpoint identity;
   - the exact label and claim strings.
5. **Freeze sequence:**
   1. Hash this FINAL text, the code and the test suite, together with the draw-sequence manifest.
   2. Phase A, which is exploratory and covered by standing authorization.
   3. Any engineering fix: new version, hashed (S5). Any scientific change: new version, Astra review and the S4 suffix.
   4. **Aidan's explicit phase B training approval**, recorded with date, time (ET) and source.
   5. Phase B training and evaluation.
   6. Results, with phase A placed in a separate development section.

## 10. Thirteen admission answers

1. **Q1.** Q-CAUSE at the organization level (bounded). Does gradual joint removal of the learned recurrent transformation produce a positive dose-averaged disruption of accurate prefix-dependent prediction, beyond matched perturbations? This is a bounded prerequisite of the C3-type acquisition question. Q-LEARN appears only as a replicated prerequisite.
2. **Q2.** One hypothesis: for the complete weight_hh, interpolated W_T → W_0 at updates 5–8, the trapezoidal dose-averaged increase in oracle-referenced prefix-function loss exceeds that of every one of 32 block-norm-matched random paths by more than eps0, **and** reaches at least B_prefix/4. "At least eight of the ten prespecified phase-B seeds jointly satisfy validity, eligibility, D and M. The denominator remains ten; seeds are not removed from it."
3. **Q3.** The falsifiers are:
   - "GRADED JOINT REVERSION CRITERION NOT MET" in phase B;
   - UNRESOLVED from E1 failure or more than two invalid seeds, evaluated first.

   Phase A falsifies and confirms nothing.
4. **Q4.** The strongest simpler explanations:
   - generic sensitivity to displacement of the same per-block norm (32 random paths, shared across doses);
   - endpoint-only effects (the curve statistic);
   - single-matrix sufficiency (secondary, correlated);
   - harness artifacts (SHAM, RESTORE, ENDPOINT);
   - total-loss confounds (the prefix-function outcome; L_cont and XOR are descriptive);
   - post-hoc dose selection (excluded);
   - an intact prefix function no better than prefix-blind (the C_prefix eligibility).

   **Limitation (verbatim):** "Holding the same readout fixed in REV and random conditions controls readout identity, but does not eliminate differential disruption of compatibility among recurrent matrices, input weights, biases and the readout."
5. **Q5.** Why now:
   - PR #7 established transfer and basic intervention dependence, but its single-block, endpoint, total-loss SPECIFIC criterion was not met (1/10, 3/10 and 3/10 seeds passed).
   - Consult #14 names this design as the most valuable next study.
6. **Q6.** On success:
   - Record the §8 paragraph and limitation sentence.
   - Ledger (§11): "Q-CAUSE, preregistered organization-level contribution: bounded support".
   - Any mechanism or localization follow-up needs separate approval and a new protocol.
7. **Q7.** On failure:
   - Record "criterion not met; no reduction identified".
   - Report basic intervention dependence as measured.
   - Never write "generic damage", "no causal role" or "not learned".
   - Any change to doses, outcome or threshold is a new protocol.
8. **Q8.** Resources:
   - Phase A: evaluation only. Per seed, 6 doses × 33 paths × 4 targets = 792 enumerations of 256 histories, plus checks.
   - Phase B: 30 CPU runs of 4000 steps, plus the same evaluation.
   - Appendix A, if approved: 49 runs per seed, 490 in total.
   - No organism model.
9. **Q9.** Organizational: the causal contribution of acquired recurrent parameters to the use of earlier evidence. Engineering: training, the hook and enumeration. No substrate claim.
10. **Q10.** The ceiling is in §8, including the "Never claimed" list.
11. **Q11.** C3-type history-integrating predictive state. C4 (internal evaluation dissociable from first-order inference) and C5 remain unsupported and untested.
12. **Q12.**
    - **Supplied:**
      - the GRU cell and its initialization, the timing scaffold, the readout architecture, losses, the split, the dose grid and the random-direction family;
      - the oracle, used for **evaluation only** in the main study. **Exception:** Appendix A's tuned rival uses oracle-assisted hyperparameter selection, a disclosed selection advantage (recurrent-core FINAL §2).
    - **Acquired:** W_T and its contribution.
    - **Selected:** nothing in the main study. Appendix A: (g*, b*).
13. **Q13.** How the ledger moves:
    - **Primary REPLICATED:** from "basic intervention dependence; PR #7 specific criterion not met" to "bounded causal contribution of the trained hidden-to-hidden parameters to accurate prefix-dependent prediction under the specified intervention and fixed surrounding computation".
    - **Not met:** "criterion not met; no reduction identified".
    - Q-NECESSITY stays NOT_ESTABLISHED, and Q-EXIST is not addressed, in every case.

## 11. Q-separation and the ledger

| Item | ORIGIN | ROLE (if shown) | REDUCTION | Question |
| --- | --- | --- | --- | --- |
| Transfer of W_T (phase B replication) | ACQUIRED | predictive advantage surviving readout replacement | criterion not met; no reduction identified | Q-LEARN (prerequisite only) |
| Complete learned weight_hh, updates 5–8 | ACQUIRED | positive dose-averaged prefix-function disruption beyond matched paths, ≥ B_prefix/4; bounded causal contribution | criterion not met; no reduction identified | Q-CAUSE, organization level (bounded) |
| Basic intervention dependence | ACQUIRED | forecasts and loss change under the specified weight changes (as measured) | — | Q-CAUSE, basic |
| Single blocks r, z, n | ACQUIRED | secondary, correlated, as above | criterion not met; no reduction identified | Q-CAUSE (secondary) |
| Necessity of recurrent training | NOT TESTED | — | — | Q-NECESSITY |
| Existence of an exact solution | PR #4 / PR #5 K-EXACT erratum | — | — | Q-EXIST (not addressed) |

## 12. Values chosen where consults #14 and #15 left them open (conservative)

| item | value | note |
| --- | --- | --- |
| Statistic | trapezoidal AUC on 𝒜, zero-dose weight kept | O3 confirmed |
| Directional | beat all 32 by more than eps0 | O5 confirmed; margin from consult #15 |
| Materiality | AUC > eps0 and AUC ≥ B_prefix/4; no PD floor | O4 confirmed |
| Eligibility | valid + transfer pass + B_prefix > eps0 + C_prefix > eps0 + displacement rule; failures non-pass | consult #15 |
| "Exactly zero" block displacement | implemented as ‖delta_k‖_F ≤ eps0 | conservative numerical reading (ambiguity A1) |
| Replication | ≥ 8 of 10; denominator fixed at 10; UNRESOLVED precedence | consult #15 |
| Weighting | uniform complete grid primary | O2 |
| Random generator | torch, 40000+100·s, one 24×8 draw per j, per-block rescale, shared across targets and doses | O8 |
| Number of random paths | 32 | O11 |
| Phase B seeds | 200–209 | — |
| Freeze point | before phase A | S1 |
| Engineering fixes | versioned and hashed before phase B; phase A outputs retained with their code version | consult #15; retention is my choice |
| Phase A | per-seed D/M flags and endpoint block errors allowed; no pooling or aggregate verdict | O9 |
| Draw-sequence test | two-process byte identity + manifest sha before phase A | consult #15; details are my choice |
| Readout refit at α = 1 | not run | O6 |
| Appendix A seeds | 200–209; text fixed in this hash before any phase B exposure | O10 |
| Appendix A edits after phase B results | not allowed; any change becomes a new protocol on new seeds | conservative (A3) |

## 13. Rulings on O1–O11 (consult #15), as applied

- **O1, formula.** Correct as written; both means are uniform over prefixes. Applied as the exact ASCII in §5.
- **O2, weighting.** The complete uniform grid is primary and measures the forecast function, including trained histories. The primary statistic is not called held-out generalization (§5).
- **O3, AUC.** Trapezoidal AUC and the zero-dose weight are kept. Endpoint loss is descriptive (§§5–6).
- **O4, materiality.** B_prefix/4 is kept, with the C_prefix eligibility and the reporting edits. Nonpositive B is a non-pass, not invalid (§6).
- **O5, directional.** Beat all 32, with the eps0 margin. It is an empirical comparison, not a calibrated p-value (§§4, 6).
- **O6, refit endpoint readout.** Not added. Refitting would test recoverability under readout adaptation, which is a different question, and needs no training here (§12).
- **O7, transfer eligibility.** Kept. Curves are reported for valid but ineligible seeds and never upgraded (§6).
- **O8, shared random blocks.** Accepted. The secondary results are correlated and are not independent replications (§§4, 7).
- **O9, phase A reporting.** Endpoint block errors and B-relative flags are allowed when explicitly exploratory. The bans on pooling and confirmation are kept (§2 S9, §7).
- **O10, rival seeds and boundary rule.** Seeds 200–209 are used, with the appendix fixed before exposure. The ≥ 3/10 rule is a boundary-selection flag, not proof that the optimum lies outside the grid (Appendix A).
- **O11, 32 versus 64.** 32 is kept. More draws would make "beat every draw" more stringent; it is not merely a precision improvement (§12).

**Residual ambiguities, resolved conservatively and listed:**
- **A1.** "Exactly zero displacement" is read as ≤ eps0 numerically.
- **A2.** C_prefix applies to secondary targets too, as a seed-level eligibility condition.
- **A3.** Appendix A text cannot be edited after any phase B result is seen.
- **A4.** S5's hashing requirement for engineering fixes is satisfied by a new versioned file hashed before phase B. Phase A need not be rerun, but superseded outputs carry their code version.

---

## Appendix A. Optional wider tuned-rival grid (secondary robustness; separate approval; no gate)

**Status.**
- This is new training. It needs Aidan's separate approval and does not alter PR #7's labels.
- It is secondary to the causal question (consult #14).
- Its text is fixed in this hash, before any exposure to phase B results (O10).

**Oracle exception.** Hyperparameter selection here uses the exact oracle's expected VAL risk. **This is an explicit exception to "oracle used only for evaluation"** (§10 Q12), and a disclosed selection advantage for the rival (recurrent-core FINAL §2).

**Design.**
- **Family (unchanged):** the frozen GRU-8 at each seed's own W_0, with `weight_hh_l0 ← g·weight_hh_l0` and `bias_hh_l0[8:16] += b`.
- **Grid:** the union of **47 configurations**:
  - the original 9: {0.5, 1, 2} × {−2, 0, 2};
  - the extension 42: {1, √2, 2, 2√2, 4, 4√2, 8} × {−6, −4, −3, −2, −1, 0};
  - overlap 4: {1, 2} × {−2, 0}.
- **Seeds:** 200–209, paired with phase B CAND for ratio843.
- **Selection:**
  - per seed, on the balanced 48-history VAL set;
  - 8→70→3 readout from torch seed 6000+s, 4000 steps;
  - tie-break: smaller |log₂g|, then smaller |b|, then smaller b, then smaller g.
- **Refit and evaluation:** refit on 192 TRAIN histories and evaluate TEST once. F-TUNED32 inherits (g*, b*) and is descriptive.

**Labels.** Recurrent-core FINAL §4 (i)/(ii), each qualified as "within the declared 47-configuration grid".

**Boundary flag.**
- If g* = 8 or b* = −6 in ≥ 3/10 seeds, report "TUNED RIVAL STILL EDGE-LIMITED", with no further extension.
- This is a boundary-selection flag, not proof that the optimum lies outside the grid.
- Selections at g = 0.5 or b = +2 are also reported.
- Absence of boundary selections does not certify global optimality.

**Context (consult #14).** Defeating the ≤ ½ threshold needs about 4.8–17.1× rival improvement; matching CAND needs 10–34×. The 1.8–2.5× figure concerns only A-FIT's total clause, not its XOR clause.

**Compute (charged separately):** 47 × 4000 selection steps per seed, plus the refit and F-TUNED32.

## Appendix B. Analytic checks already run (scratch; no phase A)

No rollout, loss or curve was computed on any network. The outputs are:
- `/workspace/scratch/graded/construction_check.txt`
- `/workspace/scratch/graded/lprefix_identity_check.txt`

**Checkpoints and norms.**
- **Shapes** (`s100_f_trained.ckpt`): `weight_hh_l0` 24×8, `weight_ih_l0` 24×9, biases 24 each, readout 32×8, 32, 3×32 and 3. Stored as float32.
- **W_0 identity.** The F-INIT `weight_hh` equals the CAND-init `weight_hh` in 10/10 seeds. The F-TRAINED `weight_ih` equals CAND-final in 10/10.
- **Displacement norms** (seeds 100–109):
  - ‖delta‖_F: 3.60–4.63;
  - ‖delta_r‖: 1.86–2.72;
  - ‖delta_z‖: 2.36–3.05;
  - ‖delta_n‖: 1.78–2.26;
  - for comparison, ‖W_T‖_F is 4.69–5.62 and ‖W_0‖_F is 2.77–2.99.

  No block is near eps0, so the zero-block rule is not triggered on these seeds.

**Random-direction rescaling algebra** (NumPy stand-in; torch is not installed on the box):
- block-norm error ≤ 4.4e-16, and ‖eps_j‖_F = ‖delta‖_F;
- cos(eps_j, delta) ranges from −0.11 to 0.14 (SD 0.065, against 1/√192 = 0.072).
- **This validates the algebra only. The Torch draw sequence must be tested in the frozen implementation (§4, §9).**

**Path, weights and the L_prefix definition.**
- ‖W(1) − W_0‖_max = 0 for seed 100. The trapezoid weights sum to 1.
- **L_prefix identities** (consult #15 ASCII definition; oracle and synthetic forecasts only):
  - L_prefix(q_star) = 0.
  - A random prefix-blind forecast gives L_prefix = 0.0138386 = PD(q_star).
  - q_star plus a continuation-only error gives L_prefix = 2e-32 ≈ 0, although the forecasts are wrong.

**Oracle scale.** PD(q_star) = 0.013839 (X 0.003046, Y 0.000697, XOR 0.010095) and CD(q_star) = 0.14172. P(h) > 0 for all h.
