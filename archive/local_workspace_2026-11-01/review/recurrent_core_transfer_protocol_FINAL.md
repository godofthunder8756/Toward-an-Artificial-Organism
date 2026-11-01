# Recurrent-core transfer with hidden-to-hidden matrix reversion: protocol (FINAL v1)

> **FINAL TEXT FOR HASHING. NOT RUN.**
> - Astra consult #12 (FREEZE WITH NAMED EDITS) has been applied in full (§0.2).
> - No code has been written, no run has been made, and nothing is committed or frozen in the repo.
> - This is a **new prospective study**. It is not a retroactive strengthening of PR #5 (consult #11 §4).
> - The study was formerly titled "…with gate-path reversion and rescue". It was renamed under consult #12, which asks for "hidden-to-hidden matrix reversion" wording. Restoration is an integrity check, not rescue evidence.
>
> **Approval gate (still pending).** The study trains new networks: 10 fresh GRU-8 seeds, plus fresh readouts and rival readouts. Aidan's direct approval of 2026-10-20 (4:41 PM ET) covered **the two-stream acquisition study only**. This study needs **Aidan's separate explicit approval** before any scientific freeze or run (consult #12: "The separate training approval recorded in the header remains necessary"). The §7 P2 synthetic harness is analytic and needs no training.

**Sources.**
- Astra consults #11 (§§2–4) and #12 (all edits).
- Draft v1: `/workspace/review/recurrent_core_transfer_protocol_draft_v1.md`, sha256 `5b74a9ec…`, left untouched.
- PR #5 head `b25a30a`: protocol `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md` (sha256 `5fa5a795…`) and metrics code (sha256 `bb7f0440…`).
- PR #5 errata commit `03751e7`. It contains the claim-wording erratum and the K-EXACT precision erratum, with the corrected ordering passing at 4 bits on TRAIN and TEST.
- ACI_RESEARCH_CONSTITUTION_v3.md.

**Scope guards.**
- GRU-8 only, in the same family. The tuned rival only rescales or offsets the frozen initialization of the same GRU-8.
- No new architecture family. P2 is an analysis instrument, not a candidate architecture (consult #12).
- No protected controller or register.
- Below C4. No organism work. No consciousness claim.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate (§10).

---

## 0.1 Inherited, unchanged from the PR #5 frozen protocol

Everything below is inherited unless §§1–8 say otherwise:
- The W2 world, the exact oracle `world.q` and the history probabilities.
- The TRAIN/TEST split: h is TEST iff ((h mod 16) + ⌊h/16⌋) mod 4 = 0. This gives 192 TRAIN and 64 TEST histories.
- The input layout: reading ±1, then the 8-stage one-hot as the external timing scaffold (INPUT_SIZE 9).
- The zero initial state and float64 evaluation.
- The A-FIT gates: ¼ of the split-specific current-only total excess, and ¼ of the 4c² product-XOR excess.
- The budget:
  - 4000 steps at batch 256, so 1,024,000 non-TEST episodes.
  - Adam (0.9, 0.999, 1e-8), weight decay 0, cosine LR 1e-3→1e-4, global gradient clip 1.0.
  - Loss: batch mean of the summed three squared terminal errors on **ordinary outcome labels**.
- Episode sampler: an independent float64 generator seeded 1000+s, with TEST rejection.
- `torch.set_num_threads(1)` and deterministic algorithms.
- IDENTITY_TOL = 1e-9.
- The PR #5 frozen E3 code is retained as a **historical diagnostic only** (§7.0). Prospective validation uses the versioned E3-v2 instrument.

**Numerical zero.** Throughout this protocol, ε₀ = 10⁻¹².

## 0.2 Edits applied (consult #12)

| # | Consult #12 edit (verbatim or closely paraphrased) | Where applied |
| --- | --- | --- |
| 1a | Keep transfer primary against F-INIT. Remove §3 condition (d). Report F-TUNED32 as robustness evidence. | §3 |
| 1b | Replace the competing verdicts with: "TRANSFER SHOWN requires A-FIT, integrity, and E(F-TRAINED) ≤ ½ E(F-INIT) in at least 8/10 seeds. Frozen-core A-FIT success is reported independently and does not override a demonstrated transfer advantage." | §3 |
| 1c | Apply the same separation to §4: report ratio843 advantage and R-TUNED843 A-FIT success independently. | §4 |
| 1d | Replace "co-adaptation loss" with "Original-versus-refitted-readout performance difference; this combines readout adaptation and optimization effects." | §3 |
| 2a | Per-seed reservoir selection. Note that it is not guaranteed to find the strongest possible reservoir. | §2 |
| 2b | Balanced VAL rule: p = h mod 16, u = ⌊h/16⌋, VAL iff (p+u) mod 4 = 2 and u ≠ (2−p) mod 16. This gives 48 TRAIN histories, 3 per prefix and 3 per continuation. FIT is the remaining 144. | §2 (verified in scratch) |
| 2c | Append smaller g to the tie-break. | §2 |
| 2d | Oracle-validation note, verbatim. | §2 |
| 2e | F-TUNED32 "inherits settings selected for the 843-parameter head", stays descriptive, and has no second nine-way search. | §1, §2, §3 |
| 3a | Remove the exact-p claim. Use the verbatim SPECIFIC condition 1 wording. | §5 |
| 3b | Keep the quarter-benefit rule. SPECIFIC applies only on transfer-passing seeds with B > 10⁻¹². Require ΔE > 10⁻¹² and ΔE ≥ B/4. "A zero displacement supplies no reversion test." | §5 |
| 3c | 32 draws are acceptable for this bounded comparison only. | §5 |
| 3d | The combined claim needs the same matrix to pass transfer and SPECIFIC **jointly** in ≥ 8/10 seeds. Integrity failures are invalid observations. More than 2 invalid seeds gives UNRESOLVED. | §3, §5, §6 |
| 4a | PD/CD on the complete 16×16 grid with uniform product weights. Report the probability-weighted and TEST-restricted versions separately. A denominator ≤ 10⁻¹² makes the ratio undefined. | §5 |
| 4b | Label renamed "PREFIX VARIATION REDUCED WITH CONTINUATION VARIATION RETAINED". On failure, write "selective variation reduction not demonstrated". It is not a prefix-content mechanism. | §5, §6 |
| 5a | Use "hidden-to-hidden matrix reversion" wording. Biases are excluded. | title, §5 |
| 5b | Sham and full restoration are integrity checks only, not causal rescue evidence. | §5 |
| 5c | Freeze the FOREIGN-INIT pairing (cyclic over seeds 100–109) and all other descriptive operators. | §5 |
| 6a | Replace V-1 with the verbatim E3-v2 ratio rule. The frozen rule is kept as historical. UNDEFINED never passes. | §7.0 |
| 6b | Apply E3-v2 consistently across ratio statistics. A perfect complement with a separated donor passes, and 0/0 does not. | §7.0, §4 |
| 6c | PR #5 erratum and audit of the saved statistics. | Out of scope here. The Specialist handles it separately (§7.0 note). |
| 7a | "DECODER ADEQUATE" becomes "DECODER PREDICTIVE AND CROSS-FOLD STABLE", with the verbatim definition. | §7.1 |
| 7b | In P2, report each fitted subspace's angle to span(Q), plus inter-fold angles and intervention outcomes. The 30° threshold is a declared diagnostic, not a causal criterion. | §7.1, §7.2 |
| 7c | Corrected pilot wording: marginal R² stays high while covariance R² deteriorates. | §7.3 |
| 7d | P2 full specification: seeds, nuisance initialization, matrix distributions and scaling, update order. | §7.2 |
| 7e | Explicit known-Q projector control. | §7.2 |
| 7f | Deterministic extension to invalid charts, with repair counts. | §7.2 |
| 7g | Clear ξ/ν notation and degree symbols. | §7.2 (notation box) |
| 7h | "Decodable but unused": verify zero effect of intervening on the known unused Q-copy. Learned-projector behavior is descriptive. | §7.2 |
| 7i | P2 failure limits E3 interpretation, not transfer. Rotations at zero nuisance are not independent demonstrations. | §7.2 |
| 8a | P1 runs on the new saved checkpoints. No PR #5 replay. Metric matching is not weight identity. | §7.1 |
| 8b | Replace the §9 failure statements, verbatim. | §9 Q7 |
| 8c | Resource-parity wording. | §1 |
| 8d | Allowed successful claim, verbatim. Append tuned-rival and variation results separately. | §6 |

---

## 1. Arms and parameter accounting

**Seeds.** There are 10 **fresh** seeds, s ∈ {100, …, 109}, disjoint from PR #5 seeds 0–9. Seed s sets the torch init seed s and the episode stream 1000+s.

**GRU-8 parameter count (verified).** The counts follow PyTorch's `nn.GRU(9, 8)` + `Linear` layout. They match `parameter_counts` in PR #5 `cand_gru8_s0.json`.

| block | shape | count |
| --- | --- | --- |
| `weight_ih_l0` (W_ir, W_iz, W_in stacked) | 24×9 | 216 |
| `weight_hh_l0` (**W_hr, W_hz, W_hn** stacked; rows 0–7 / 8–15 / 16–23) | 24×8 | 192 |
| `bias_ih_l0`, `bias_hh_l0` | 24 + 24 | 48 |
| **recurrent total** | | **456** |
| readout 8→32→3 (8·32+32 + 32·3+3) | | **387** |
| **CAND total trainable** | | **843** |
| readout 8→70→3 (8·70+70 = 630, 70·3+3 = 213) | | **843** |

**Arms (per seed s).** "Fresh" readouts share one initialization per seed: torch seed 5000+s, an identical 8→32→3. They use the same data stream (1000+s) and budget, with recurrence frozen.

| arm | core (frozen unless noted) | readout | role |
| --- | --- | --- | --- |
| **CAND** | GRU-8, trained (recurrent + readout) exactly as PR #5 CAND | own 8→32→3 | source of the trained core W^T. E1 replication in fresh seeds |
| **F-TRAINED** | CAND's trained core W^T, frozen | fresh 8→32→3 | transfer of learned recurrence (primary) |
| **F-INIT** | CAND's own init core W^0, frozen | fresh 8→32→3 | matched-initialization comparator (primary) |
| **F-TUNED32** | W^0(g*, b*), inheriting the settings selected for the 843-parameter head (§2) | fresh 8→32→3 | **robustness evidence only, descriptive** |
| **R-TUNED843** | W^0(g*, b*) | 8→70→3 (843 trainable) | parameter-budget robustness rival (§4) |

For every arm, W^0, W^T and all readouts are saved as `state_dict` checkpoints with sha256.

**Resource parity (consult #12 wording).**
- **F-TUNED32 has matched readout size.**
- **R-TUNED843 matches the original candidate's trainable parameter count**, while carrying additional frozen parameters and selection compute.
- Both tuned arms carry 456 frozen-random recurrent parameters plus 2 selected hyperparameters (g, b) from a 9-way grid (log₂9 ≈ 3.17 bits). Selection compute is 9 × 4000 steps per seed. All of this is charged separately.
- Larger frozen reservoirs are not run. If one is added later, it is labeled capacity sensitivity.

## 2. Tuned frozen GRU-8 robustness rival (per-seed selection)

**Rival definition.** The rival is the frozen GRU-8 at seed s's own init W^0, changed as follows:
- **Scale:** `weight_hh_l0 ← g · weight_hh_l0`. `bias_hh_l0` is unchanged.
- **Update-gate offset:** `bias_hh_l0[8:16] += b`. In PyTorch, z = σ(W_iz x + b_iz + W_hz h + b_hz) and h' = (1−z)⊙n + z⊙h.

The grid is g ∈ {0.5, 1, 2} × b ∈ {−2, 0, 2}, giving 9 frozen configurations.

**Per-seed selection.** Selection runs on each seed's own init. This tests whether tuning each supplied initialization removes the gap. **It is not guaranteed to find the strongest possible reservoir.**

**VAL subset (balanced).** Write p = h mod 16 and u = ⌊h/16⌋. Then h is in VAL iff (p + u) mod 4 = 2 and u ≠ (2 − p) mod 16. This gives 48 TRAIN histories, with three per prefix and three per continuation, and no continuation dropped. FIT is the remaining 144 TRAIN histories.

The rule was checked in scratch over all 256 histories:
- VAL has 48 members, all in TRAIN, and is disjoint from TEST, where (p+u) mod 4 = 0.
- Every p has exactly 3 VAL members, and so does every u.
- |TRAIN| − |VAL| = 144.
- VAL = {6, 10, 14, 21, 25, 29, 36, 40, 44, 51, 55, 59, 66, 70, 74, 81, 85, 89, 96, 100, 104, 115, 119, 127, 130, 134, 142, 145, 149, 157, 160, 164, 172, 179, 187, 191, 194, 202, 206, 209, 217, 221, 224, 232, 236, 247, 251, 255}.

**Selection runs.**
- The sampler rejects TEST and VAL histories.
- Otherwise the §0.1 budget applies.
- Each run trains a fresh 8→70→3 readout from torch seed 6000+s, the same for all 9 configurations.

**Criterion.** The criterion is the probability-weighted VAL total excess against `world.q`, normalized within VAL.

> **Hyperparameter selection uses exact oracle expected validation risk. This is an explicitly supplied selection advantage for the robustness rival; it is not finite-sample outcome-only validation.**

**Tie-break.** Two configurations tie when their criteria differ by ≤ ε₀. A tie goes, in order, to:
1. the smaller |log₂ g|;
2. the smaller |b|;
3. the smaller b;
4. **the smaller g**.

**Refit.** A fresh 8→70→3 readout (6000+s) is trained at (g*, b*) on all 192 TRAIN histories under the §0.1 budget, and TEST is evaluated **once**.

**F-TUNED32.** It inherits the settings selected for the 843-parameter head. It uses the same (g*, b*) with the fresh 8→32→3 (5000+s) on all 192 TRAIN histories. Its own head was **not** separately tuned, and no second nine-way search is run. It is descriptive robustness evidence only.

## 3. Transfer test (Q-LEARN; primary)

All metrics are TEST excesses against `world.q`, and TRAIN is also reported. E(·) denotes the TEST E_total.

- **Prerequisite (E1 replication).** CAND meets A-FIT on TEST, with A-LEARN and integrity, in ≥ 8/10 fresh seeds. If not, the study is **UNRESOLVED (E1 not replicated)**, and §§4–6 are descriptive.
- **Valid seed.** A seed is valid if integrity holds: finite outputs in (0, 1), identity and restoration ≤ IDENTITY_TOL, and saved-checkpoint hashes reproducible. **Integrity failures are invalid observations, not evidence against transfer.**
- **Per-seed transfer pass.** On a valid seed, F-TRAINED meets A-FIT on TEST **and** E(F-TRAINED) ≤ ½ · E(F-INIT). The former condition (d) against F-TUNED32 has been **removed**.
- **Verdict.**
  > **TRANSFER SHOWN requires A-FIT, integrity, and E(F-TRAINED) ≤ ½ E(F-INIT) in at least 8/10 seeds. Frozen-core A-FIT success is reported independently and does not override a demonstrated transfer advantage.**
  - **UNRESOLVED:** more than 2 invalid seeds.
  - **TRANSFER NOT SHOWN:** any other outcome. This is a conservative choice, with no intermediate category, so anything below 8/10 is not shown.
- **Reported independently (no verdict effect):**
  - F-INIT and F-TUNED32 A-FIT counts on TEST.
  - E(F-TRAINED)/E(F-TUNED32) per seed, as robustness evidence, with the §7.0 ratio rule.
  - A rival can satisfy A-FIT while being substantially worse. Its sufficiency does not refute the candidate's advantage or identify the candidate's mechanism.
- **Descriptive.** E(CAND) − E(F-TRAINED) is reported as the original-versus-refitted-readout performance difference. This combines readout adaptation and optimization effects.

## 4. Robustness comparison against R-TUNED843 (reported independently; not Q-NECESSITY)

- **ratio843(s)** = E(CAND) / E(R-TUNED843), computed with the §7.0 E3-v2 ratio rule. A seed with an UNDEFINED ratio does not pass.
- **Reported independently.** Neither statement below overrides the other or the §3 verdict.
  - (i) **"ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED"** applies if ratio843 ≤ ½ in ≥ 8/10 valid seeds. Otherwise the result is "not observed".
  - (ii) **"TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET"** applies if R-TUNED843 meets A-FIT on TEST in ≥ 8/10 seeds. The count is reported in every case.
  - If there are more than 2 invalid seeds, both statements are UNRESOLVED.
- Also reported: (g*, b*) per seed, the full VAL curve, selection compute, and a flag when a grid edge is selected.

## 5. Hidden-to-hidden matrix reversion (Q-CAUSE; bounded)

**Readout.** Interventions are applied to **F-TRAINED**: the trained core with its **fresh readout held fixed**. Running them with CAND's own readout is descriptive only.

**Interventions.** For k ∈ {r, z, n}, W_hk is the 8×8 block of `weight_hh_l0`: rows 0–7 for r, 8–15 for z, 16–23 for n. Write δ_k = W_hk^0 − W_hk^T. All three interventions are preregistered, and none is selected using TEST.

- **REV_k (hidden-to-hidden matrix reversion).** The recurrent updates for readings 5–8 use W_hk^0 in place of W_hk^T. Everything else stays trained: the input-to-hidden weights, all biases including `bias_hh` block k, and the other two matrices. Updates 1–4 are intact. This reverts one hidden-to-hidden matrix, **not** an entire gate pathway.
- **RND_k,j** (j = 1…32). The same steps use W_hk^T + ε_j. Each ε_j has i.i.d. N(0,1) entries in the 8×8 block, rescaled to ‖ε_j‖_F = ‖δ_k‖_F. The generator is torch seed 9000 + 100·(s−100) + 10·k_idx, with k_idx = 0, 1, 2 for r, z, n. Draws are taken in order j = 1…32.
- **Integrity checks only (no causal evidential role):**
  - **SHAM_k:** the override hook substitutes a copy of W_hk^T at steps 5–8. Forecasts must equal intact within ε₀.
  - **RESTORE_k:** after REV_k, remove the override and rerun. The result must reproduce intact within IDENTITY_TOL.
  - Restoration by rerunning the intact network is **not** independent causal rescue evidence. A failure of either check makes the seed **invalid** for §5.
- **Descriptive operators (frozen now):**
  - **TEMPORAL-RESTORE_k:** W_hk^0 at steps 5–6, then W_hk^T at steps 7–8.
  - **EARLY-REV_k:** W_hk^0 at steps 1–4 only.
  - **BIAS-REV_k:** REV_k, plus `bias_hh_l0` block k set to its init during steps 5–8.
  - **FOREIGN-INIT_k:** at steps 5–8, substitute W_hk^0 from seed σ(s) = 100 + ((s − 100 + 1) mod 10). This is a cyclic pairing: 100→101, …, 108→109, 109→100.
  - **ORIGINAL-READOUT REV_k:** REV_k with CAND's own readout.

**Metrics.** ΔE_k = E(REV_k) − E(F-TRAINED) is reported as total and as X, Y and XOR separately. TEST is primary and TRAIN is reported. ΔE_rand,j is defined the same way.

**Per-seed SPECIFIC(k).** SPECIFIC is evaluated only on a seed that passes the primary transfer criterion (§3) and has B = E(F-INIT) − E(F-TRAINED) > 10⁻¹². All of the following must hold:
1. **Reversion causes greater excess loss than each of the 32 prespecified matched-norm random perturbations.** That is, ΔE_k > ΔE_rand,j for every j. This is an empirical directional comparison, not a calibrated significance test. Reversion toward initialization is not exchangeable with isotropic random directions.
2. ΔE_k > 10⁻¹² and ΔE_k ≥ B/4. This is the quarter-benefit materiality criterion.
3. If ‖δ_k‖_F ≤ ε₀, SPECIFIC(k) is **not evaluated** for that seed and counts as non-pass. A zero displacement supplies no reversion test.

Thirty-two draws are acceptable for this bounded comparison. They do not establish superiority over generic damage generally.

**Verdict per k (joint, same matrix).**
- **REPLICATED SPECIFIC(k):** at least 8/10 seeds jointly pass transfer **and** SPECIFIC(k) for the **same** k. Two different sets of eight successes are not combined.
- **UNRESOLVED(k):** more than 2 seeds are invalid for §5 (integrity, sham or restore failures). Invalid seeds count neither for nor against.
- **SPECIFIC(k) NOT DEMONSTRATED:** any other outcome.

There is no "any k" family upgrade, and all three k are reported in full.

**Dependence analysis (descriptive thresholds).** Write f(p, u) for the forecast vector, where p is the 4-bit prefix (readings 1–4) and u the 4-bit continuation (readings 5–8), so h = p + 16u.
- **Primary (uniform, complete 16×16 grid).**
  - PD = (1/256) Σ_{p,u} ‖f(p,u) − f̄(u)‖², where f̄(u) = (1/16) Σ_p f(p,u).
  - CD = (1/256) Σ_{p,u} ‖f(p,u) − f̃(p)‖², where f̃(p) = (1/16) Σ_u f(p,u).
- **Reported separately:**
  - (a) the probability-weighted versions, using P(p,u) with conditional means;
  - (b) the TEST-restricted versions, over the 64 TEST histories with means taken within each u (or p) over its TEST members.

  The TEST split couples prefixes and continuations, so (b) is not primary.
- **Ratios.** PR_k = PD(REV_k)/PD(F-TRAINED) and CR_k = CD(REV_k)/CD(F-TRAINED), plus the same ratio for each RND draw. **A denominator ≤ 10⁻¹² makes its ratio undefined**, and an undefined ratio never passes. PD and CD of the exact oracle are reported for scale.
- **Label.** The label applies only when REPLICATED SPECIFIC(k) holds. Per seed, all of the following must hold on the primary uniform quantities:
  - PR_k ≤ ½;
  - PR_k < PR_rand,j for every j;
  - CR_k ≥ ¾.

  If ≥ 8/10 seeds pass (same validity rule), the label is **"PREFIX VARIATION REDUCED WITH CONTINUATION VARIATION RETAINED"**. Otherwise write **"selective variation reduction not demonstrated"**. Failure does **not** identify generic damage or any other alternative.
- PD and CD measure forecast variation, not whether that variation carries correct prefix information. The label is **not** a prefix-content mechanism.

## 6. Claim assembly (fixed in advance)

- **Allowed successful claim.** This applies when TRANSFER SHOWN holds and REPLICATED SPECIFIC(k) holds for some k (k is named):
  > "In W2, recurrent training produced a GRU-8 core whose predictive advantage over its matched initialization survived replacement and retraining of the readout. For the specified matrix, reverting learned weights during continuation caused greater held-out prediction loss than each of 32 matched-norm random perturbations, meeting the prespecified materiality criterion in at least 8/10 fresh seeds."

  Tuned-rival results (§3 independent reports, §4 (i)/(ii)) and variation results (the §5 label or its failure wording) are **appended separately**. This supports a learned, transferable recurrent contribution with bounded causal intervention evidence. It does not establish localized content, necessity, C4 or consciousness.
- **TRANSFER SHOWN, no REPLICATED SPECIFIC(k):** state the first sentence only, then "Hidden-to-hidden matrix reversion did not meet the prespecified joint criterion for any matrix" (or "was UNRESOLVED" where applicable). Append the rival and variation results separately.
- **TRANSFER NOT SHOWN:** use the §9 Q7 failure wording. Reversion results are descriptive only.
- **Never claimed:**
  - that W_hk "stores" prefix or chart content;
  - a localized or independently manipulable state component;
  - a gate-pathway mechanism;
  - necessity of recurrent training (Q-NECESSITY);
  - uniqueness;
  - other architectures or budgets;
  - irreducible joint state;
  - C4, consciousness or organism claims;
  - any retroactive change to PR #5 E2 or E3.

## 7. E3 pipeline validation (additive; prospective; no retroactive E3 success)

The purpose is to validate the E3 intervention instrument prospectively. Nothing here relabels PR #5's E3 (NOT LOCALIZED BY THIS INTERVENTION). P2 failure limits E3 interpretation, not the transfer experiment.

### 7.0 Ratio rule (E3-v2), replacing V-1

> **The frozen PR #5 rule is retained as a historical diagnostic. A separately versioned E3-v2 instrument is used for prospective validation. For ratio N/D: if D≤10⁻¹² and N>10⁻¹², return +∞; if both N and D≤10⁻¹², return UNDEFINED; otherwise return N/D. UNDEFINED never counts as a pass.**

- **Scope.** The rule applies consistently to every E3 ratio statistic: partial, complement and wrong-donor; vector and XOR; donor tracking; random-direction and random-subspace probes. It also applies to the robustness ratios in §3 and §4.
- **Exception: PD/CD ratios.** These use Astra's explicit §5 rule instead: a denominator ≤ 10⁻¹² makes the ratio undefined, and undefined never passes.
- **Thresholds** are the PR #5 values: partial ≤ ½, wrong ≤ ½, complement ≥ ¾. Under E3-v2, a perfect complement intervention with a separated donor (ratio +∞) passes, and 0/0 does not.
- **Reporting.** The frozen PR #5 rule is reported alongside as a historical diagnostic.
- **Out of scope here.** The PR #5 erratum on this defect and the audit of the saved PR #5 statistics are handled separately by the Specialist.

### 7.1 P1: held-out stage-4 decoder accuracy (new checkpoints only)

- **Cores.** P1 runs on the **new saved checkpoints** of the fresh seeds: F-TRAINED (= W^T), CAND and F-INIT cores. PR #5 replay is **not** part of this study. A replay matching recorded errors within 10⁻¹² would establish only a metric-matched reconstruction, not identical weights without checkpoint hashes.
- **Procedure.** For each parity fold, fit the frozen centered ridge (λ = 10⁻³) on the 8 fit-fold prefixes. Predict the 8 held-out prefixes' exact stage-4 chart.
- **Report:**
  - held-out R² per coordinate (m_x, m_y, c);
  - RMSE;
  - singular values;
  - the principal angles (in degrees) between the fold-0 and fold-1 bases.
- **Label.**
  > **DECODER PREDICTIVE AND CROSS-FOLD STABLE:** the declared R² and inter-fold-angle thresholds pass. This does not validate the intervention subspace.

  The declared thresholds are held-out R² ≥ 0.9 on all three coordinates on both folds, and a largest inter-fold principal angle ≤ 30°. **30° is a declared diagnostic threshold, not a sufficient causal criterion.** Both folds can agree on a misleading basis.

### 7.2 P2: synthetic harness (analytic; no training)

**Notation box.**
- z ∈ ℝ⁸ is the harness state.
- φ = (m_x, m_y, c) ∈ ℝ³ is the chart.
- **ν** ∈ ℝ⁵ is the **nuisance state**.
- **ξ** ∈ ℝ⁵ is the **nuisance initial value**.
- s ≥ 0 is the nuisance scale.
- Q ∈ ℝ^{8×3} and R ∈ ℝ^{8×5} are orthonormal complements.
- Angles are in degrees (°).

**Seeds and matrices.** There are draws d = 0…99, each using `numpy.random.default_rng(30000 + d)` in this order:
1. G ∈ ℝ^{8×8} with i.i.d. N(0,1) entries. Take its QR decomposition, G = O·T, and sign-fix so that diag(T) > 0. Then Q = O[:, 0:3] and R = O[:, 3:8].
2. A₀ ∈ ℝ^{5×5} with i.i.d. N(0,1) entries. Set A = 0.9 · A₀ / ρ(A₀), where ρ is the spectral radius.
3. a ∈ ℝ⁵ with i.i.d. N(0, 1/5) entries.
4. C ∈ ℝ^{5×8} with i.i.d. N(0, 1/5) entries.

**Initialization.** ξ = 0 ∈ ℝ⁵, ν₀ = ξ, φ₀ = (½, ½, 0) (the prior chart), and z₀ = Q φ₀ + s R ν₀.

**Update order at stage k = 1…8,** with reading r_k ∈ {0, 1}, signed reading r̂_k = 2r_k − 1 and one-hot e_k:
1. **Decode.** φ ← Qᵀ z. If s > 0, ν ← Rᵀ z / s; if s = 0, ν is carried as a separate state.
2. **Invalid-chart extension.** φ ← `_repair`(φ), using the frozen PR #5 repair: clip m_x and m_y to [0, 1], then clip c to the Fréchet interval. Increment the per-stage repair counter whenever φ changed.
3. **Transition.** If k > 1, φ ← `_transit_f`(φ).
4. **Observation.** φ ← `_observe_f`(φ, variable_k, r_k), where variable_k = X for odd k and Y for even k.
5. **Nuisance update.** ν ← tanh(A ν + a r̂_k + C e_k).
6. **Encode.** z ← Q φ + s R ν.

**Readout.** forecasts(`_repair`(Qᵀ z)), with repairs counted. The arithmetic is float64. The harness exposes `initial_state`, `step` and `readout`, so the E3-v2 suite runs on it unchanged apart from the §7.0 ratio rule. The hybrid states produced by transplants pass through step 2, which makes the extension deterministic. Repair counts are reported per stage and per intervention type.

**P2+ (known causal 3-d subspace).**
- Nuisance scales: s ∈ {0, 0.03, 0.1, 0.3, 1.0}. For reference, the stage-4 chart SD is about 0.167.
- **Report per draw:**
  - each fold's fitted-subspace largest principal angle to **span(Q)** (°);
  - the inter-fold angles (°);
  - held-out R² per coordinate;
  - the E3-v2 partial, complement and wrong ratios;
  - the LOCALIZED label;
  - repair counts.
- **Known-Q projector control.** The same suite is run with the fitted basis replaced by Q itself. This separates the intervention implementation from decoder recovery. Expectation: E3-v2 LOCALIZED at every s, with partial ≈ 0, wrong ≈ 0 and complement = +∞.
- **PIPELINE VALID (E3-v2)** requires both:
  - the known-Q control is LOCALIZED in 100/100 draws at every s;
  - the fitted-decoder suite is LOCALIZED in ≥ 95/100 draws at s ∈ {0, 0.03}.
- The curve over s is reported. At zero nuisance the rotations are largely equivalent tests, so **100 rotations are not 100 independent demonstrations of detection power.**

**P2− ("decodable but unused").**
- **State.** The Q-subspace holds a linear chart **copy** φ_c. For k ≤ 4, φ_c ← φ after step 4. For k ≥ 5, φ_c is left unchanged, i.e. not refreshed.
- **Causal code.** The causal chart is carried in R as a centered cubic code: ψ = κ · ((m_x − ½)³, (m_y − ½)³, (4c)³, 0, 0), with κ = 8. Dynamics decode φ from ψ by an elementwise real cube root and inversion.
- **Readout.** It reads only the R-code. The nuisance is omitted, i.e. s = 0.
- **Required zero-effect check.** Transplanting along the known unused Q-copy, with the basis set to Q, must change forecasts by ≤ ε₀ in every trial. If this check fails, the P2− harness is invalid.
- **Descriptive.** The fitted-decoder suite's outcome is descriptive only. The fitted decoder may overlap the used nonlinear code, so non-localization is **not** guaranteed and is not a gate.

### 7.3 Prior analytic pilot (scratch; informs §7.1 and §7.2; not an E3 result)

**Files.** `/workspace/scratch/pr5/repro/e3_decoder_pilot.py` and `.json`.

**Setup.** z4 = Qφ + s·Rν, with ν i.i.d. random per prefix and 200 draws.

**Fitted-subspace angle to span(Q).** The median largest principal angle between the frozen cross-fitted basis and span(Q) is:

| s | 0 | 0.01 | 0.03 | 0.1 | 0.3 | 1.0 |
| --- | --- | --- | --- | --- | --- | --- |
| median angle | ≈ 10⁻⁶° | 2.7° | 7.5° | 16.8° | 33.5° | 59° |

**R²:**
- Marginal R² stays high: m_x and m_y are ≥ 0.98 at every s.
- Covariance R² deteriorates: c goes 0.97 → 0.96 → 0.89 → 0.32 → −2.9 for s = 0, 0.03, 0.1, 0.3, 1.0.
- The pilot therefore does **not** demonstrate uniformly excellent three-coordinate prediction at large nuisance.
- High marginal R² can coexist with substantial basis error. This is why P2 reports the angle to span(Q).

## 8. Integrity, determinism and reporting

- One process, deterministic algorithms, `set_num_threads(1)`.
- Every checkpoint is saved with sha256.
- Generator seeds:
  - 1000+s for episodes;
  - s for initialization;
  - 5000+s for fresh 8→32→3 readouts;
  - 6000+s for 8→70→3 readouts;
  - 9000 + 100·(s−100) + 10·k_idx for RND draws;
  - 30000+d for P2.
- Missing cells are reported, and no seed is replaced.
- Every table lists all 10 seeds, all three k, every RND draw (summary and maximum), sham and restore gaps, PD/CD/PR/CR in all three versions, and invalid-seed counts.
- **Freeze before training.** The following must be hashed before any training run:
  - this text;
  - the code;
  - a test suite that checks parameter counts 456/387/843, VAL membership (48; 3 per p and per u), sham and restore identity, the E3-v2 ratio cases (+∞, UNDEFINED, ordinary), the FOREIGN-INIT pairing, and P2 seeds and determinism.

## 9. Thirteen admission answers

1. **Q1.** The study addresses Q-LEARN (does the learned GRU-8 recurrence carry a predictive advantage that survives readout replacement?) and a bounded Q-CAUSE prerequisite (does reverting a learned hidden-to-hidden matrix cause a specific, material loss?). Both are bounded prerequisites of the C3-type acquisition question.
2. **Q2.** One hypothesis is tested: the trained GRU-8 core keeps its predictive advantage over its matched initialization after the readout is replaced and retrained, and reverting a specific learned hidden-to-hidden matrix during continuation causes greater held-out loss than matched-norm random perturbations, jointly in ≥ 8/10 fresh seeds.
3. **Q3.** The falsifiers are:
   - TRANSFER NOT SHOWN;
   - SPECIFIC(k) NOT DEMONSTRATED for every k;
   - E1 not replicated (UNRESOLVED).

   More than 2 invalid seeds makes the relevant verdict UNRESOLVED.
4. **Q4.** The strongest simpler explanations, each with information and resource parity:
   - supplied random dynamics plus a trained readout (F-INIT, primary);
   - tuned frozen GRU-8 at matched readout size (F-TUNED32) or matched trainable count (R-TUNED843), as robustness evidence reported independently;
   - perturbation of the same norm (RND_k);
   - harness artifacts (SHAM_k, RESTORE_k);
   - original-readout specificity (fresh readouts).
5. **Q5.** PR #5's frozen evidence makes the study necessary:
   - E2 shows a recurrent-training benefit against one frozen init;
   - E3 did not localize, and K-FR's E3 is UNRESOLVED;
   - the frozen E3 ratio rule rejects ideal positive controls;
   - PR #5 saved no checkpoints;
   - consults #11 and #12 call for transfer, reversion and a tuned rival.
6. **Q6.** On success, record the §6 allowed claim, with rival and variation results appended. Update the ORIGIN/ROLE/REDUCTION row (§10). Any mechanism-level follow-up needs separate approval and must not claim localized content.
7. **Q7.** On failure or an UNRESOLVED result:
   - **"Transfer failure means transferable benefit was not demonstrated with this readout, optimization budget and split; it does not establish readout co-adaptation."**
   - **"Tuned-reservoir success establishes that the selected frozen alternative suffices under its declared resources; it does not explain away the candidate's learned contribution."**
   - If reversion is not demonstrated, record "the prespecified joint criterion was not met for any matrix". Do not record "generic damage".
   - Any architecture or budget change is a new protocol.
8. **Q8.** Small GRU-8 networks on CPU: 140 runs of 4000 steps, i.e. per seed CAND, F-INIT, F-TRAINED, 9 selection runs, the R-TUNED843 refit and F-TUNED32. P2 is an analytic harness with no training. Evaluation uses exact enumeration. No organism model.
9. **Q9.** Organizational: acquired recurrent organization and a bounded causal role. Engineering: training and the harness. No substrate claim.
10. **Q10.** The claim ceiling is in §6, including the "Never claimed" list.
11. **Q11.** The cognitive layer is a C3-type history-integrating predictive state. C4 (internal evaluation dissociable from first-order inference) and C5 remain unsupported and untested.
12. **Q12.**
    - **Supplied:** the GRU cell, its random init, the timing scaffold, the readout architecture, losses, feedback, the split, the tuned grid, and the oracle-risk selection advantage.
    - **Acquired, if shown:** the trained recurrent parameters and their transferable contribution.
    - **Supplied and selected, not acquired:** (g*, b*).
13. **Q13.** How the ledger moves on each decisive result:
    - **TRANSFER SHOWN plus REPLICATED SPECIFIC(k):** the ledger moves from "recurrent training helps against one frozen init" to "a learned, transferable recurrent contribution with bounded causal intervention evidence" (Q-CAUSE PARTIAL, bounded).
    - **Transfer not shown:** the transferable benefit is not demonstrated. This does not establish co-adaptation.
    - **Tuned rival meets A-FIT:** a frozen alternative suffices under its declared resources, which does not explain away the candidate's contribution.

    Q-NECESSITY stays NOT_ESTABLISHED in every case.

## 10. Q-separation and the ORIGIN/ROLE/REDUCTION ledger

| Item | ORIGIN | ROLE | REDUCTION (literal) | Question |
| --- | --- | --- | --- | --- |
| Trained recurrent core W^T | ACQUIRED (CAND training) | predictive advantage over matched init that survives readout replacement, if TRANSFER SHOWN | "transferable benefit not demonstrated" if observed | Q-LEARN |
| Tuned frozen core W^0(g*, b*) | SUPPLIED + SELECTED (oracle-risk selection) | robustness rival, reported independently | "tuned frozen GRU-8 meets A-FIT at this budget" if observed | Q-LEARN (robustness) |
| Learned W_hk^T | ACQUIRED | reversion during continuation causes specific, material loss, if REPLICATED SPECIFIC(k) | "joint criterion not met" if observed | Q-CAUSE (bounded) |
| Forecast variation pattern | — | "PREFIX VARIATION REDUCED WITH CONTINUATION VARIATION RETAINED", if shown | "selective variation reduction not demonstrated" | descriptive. This is not a content mechanism |
| Necessity of recurrent training | NOT TESTED | — | — | Q-NECESSITY (not addressed) |
| Existence of an exact solution | PR #4. The PR #5 K-EXACT precision erratum (`03751e7`) passes at 4 bits | — | — | Q-EXIST (not addressed here) |

## 11. Rulings recorded (consult #12) and residual notes

Draft-v1 flags, as ruled:
- **G1:** engineering criterion; the exact-p claim was removed.
- **G2:** F-TUNED32 is not a gate; it is descriptive robustness evidence.
- **G3:** per-seed selection.
- **G4:** replaced by the balanced VAL rule.
- **G5:** descriptive thresholds accepted; labels renamed.
- **G6:** matrix-only reversion kept, using "hidden-to-hidden matrix reversion" wording.
- **G7:** fresh readouts are primary.
- **G8:** P2 is an analysis instrument, not a new architecture family.
- **G9:** replaced by E3-v2 (§7.0).
- **G10:** the approval requirement stands.

Values chosen conservatively where consult #12 left them unspecified. Each is listed in the agent report:
- TRANSFER NOT SHOWN covers everything below 8/10, with no intermediate band.
- "SPECIFIC(k) NOT DEMONSTRATED" is the non-UNRESOLVED failure label.
- The §4 labels (i) and (ii) are named as above.
- The tie-break ordering puts smaller g last.
- Cyclic pairing is s → s+1 mod 10.
- Seeds and distributions for P2: 30000+d; A scaled to spectral radius 0.9; a and C drawn as N(0, 1/5); ξ = 0.
- κ = 8 for the P2− cubic code.
- The known-Q control requires 100/100.
- PD/CD ratios use Astra's "undefined" rule rather than +∞.
