# Recurrent-core transfer with gate-path reversion and rescue: protocol (DRAFT v1)

> **DRAFT FOR ASTRA REVIEW. NOT FROZEN.** No code has been written, no run has been made, and nothing is committed. This is a **new prospective study**. It is not a retroactive strengthening of PR #5 (consult #11 §4).
> **Approval gate.** The study trains new networks: 10 fresh GRU-8 seeds plus fresh readouts and rival readouts. Aidan's direct approval of 2026-10-20 (4:41 PM ET) covered **the two-stream acquisition study only**. This study needs **Aidan's separate explicit approval** before any freeze or run. The analytic pieces (the §7 P2 synthetic harness) need no training.

**Sources.**
- Astra consult #11, §§2–4.
- PR #5 head `b25a30a`: protocol `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md` (sha256 `5fa5a795…`), metrics code sha256 `bb7f0440…`.
- Errata drafts `pr5_results_erratum_v1.md` and `pr5_quantization_erratum_v1.md`.
- ACI_RESEARCH_CONSTITUTION_v3.md.

**Scope guards.** The study stays within the following limits:
- GRU-8 only, same family. The tuned rival only rescales or offsets the frozen initialization of the same GRU-8.
- No new architecture family.
- No protected controller or register.
- Below C4. No organism work. No consciousness claim.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate (§10).

---

## 0. Inherited, unchanged from the PR #5 frozen protocol

Everything below is inherited unless §§1–8 say otherwise:
- The W2 world, the exact oracle `world.q` and the history probabilities.
- The TRAIN/TEST split: h is TEST iff ((h mod 16) + ⌊h/16⌋) mod 4 = 0. This gives 192 TRAIN and 64 TEST histories.
- The input layout: reading ±1, then the 8-stage one-hot as the external timing scaffold (INPUT_SIZE 9).
- The zero initial state and float64 evaluation.
- The A-FIT gates: ¼ of the split-specific current-only total excess, and ¼ of the 4c² product-XOR excess.
- The training budget:
  - 4000 steps, batch 256, so 1,024,000 non-TEST episodes.
  - Adam (0.9, 0.999, 1e-8), no weight decay, cosine LR 1e-3→1e-4, global gradient clip 1.0.
  - Loss: the batch mean of the sum of three squared terminal errors on **ordinary outcome labels**.
- The episode sampler: independent float64 generator seeded 1000+s, with TEST rejection.
- `torch.set_num_threads(1)` and deterministic algorithms.
- IDENTITY_TOL = 1e-9 and RATIO_TIE = 1e-12.
- The E3 suite code, for §7, used unchanged.

## 1. Arms and parameter accounting

**Seeds.** There are 10 **fresh** seeds, s ∈ {100, …, 109}. They are disjoint from PR #5 seeds 0–9. Seed s sets the torch init seed s and the episode stream 1000+s.

**GRU-8 parameter count (verified).** The counts below come from the PyTorch `nn.GRU(9, 8)` + `Linear` layout. They match `parameter_counts` in `acquisition_results_v1/runs/cand_gru8_s0.json`.

| block | shape | count |
| --- | --- | --- |
| `weight_ih_l0` (W_ir, W_iz, W_in stacked) | 24×9 | 216 |
| `weight_hh_l0` (**W_hr, W_hz, W_hn** stacked, rows 0–7 / 8–15 / 16–23) | 24×8 | 192 |
| `bias_ih_l0`, `bias_hh_l0` | 24 + 24 | 48 |
| **recurrent total** | | **456** |
| readout 8→32→3 (`fc1` 8·32+32, `fc2` 32·3+3) | | **387** |
| **CAND total trainable** | | **843** |
| readout 8→70→3 (`fc1` 8·70+70 = 630, `fc2` 70·3+3 = 213) | | **843** ✔ |

The 843-parameter figure for the 8→70→3 readout is **verified**. It equals the original candidate's total trainable count.

**Arms (per seed s).** Readouts marked "fresh" share one initialization per seed: torch seed 5000+s, an identical 8→32→3. They are trained with the identical data stream (1000+s) and budget, with recurrence frozen.

| arm | core (frozen unless noted) | readout | role |
| --- | --- | --- | --- |
| **CAND** | GRU-8, trained (recurrent + readout), exactly as PR #5 CAND | own 8→32→3 | source of the trained core W^T. Its E1 is replicated in fresh seeds |
| **F-TRAINED** | CAND's trained core W^T, frozen | fresh 8→32→3 | transfer of learned recurrence |
| **F-INIT** | CAND's own init core W^0, frozen | fresh 8→32→3 | matched-init readout-only (a K-FR replica with a fresh readout) |
| **F-TUNED32** | selected tuned frozen core W^0(g*, b*) (§2) | fresh 8→32→3 | tuned-reservoir transfer comparator, readout matched |
| **R-TUNED843** | selected tuned frozen core W^0(g*, b*) | 8→70→3 (843 trainable) | parameter-budget robustness rival (§2) |

For every arm, W^0 and W^T are saved: `state_dict` checkpoints plus their sha256. PR #5 saved no checkpoints, so this is new.

**Charging.**
- R-TUNED843 and F-TUNED32 also carry **456 frozen-random recurrent parameters**, plus **2 selected hyperparameters (g, b)** chosen from a 9-way grid (log₂9 ≈ 3.17 bits of selection). These are charged separately, not as trainable parameters.
- Selection compute is 9 × 4000 steps per seed, reported separately.
- **Larger frozen reservoirs are not run.** If one is added later, it is labeled capacity sensitivity, not an equal-state rival.

## 2. Tuned frozen GRU-8 robustness rival (optional piece (i), folded in)

The rival is the frozen GRU-8 at seed s's own init W^0, with two changes:
- **Scale.** Every hidden-to-hidden matrix is scaled: `weight_hh_l0 ← g · weight_hh_l0`. `bias_hh_l0` is unchanged.
- **Update-gate offset.** b is added to the update-gate preactivation: `bias_hh_l0[8:16] += b`. In PyTorch, z = σ(W_iz x + b_iz + W_hz h + b_hz) and h' = (1−z)⊙n + z⊙h, so b > 0 lengthens retention.

The grid is g ∈ {0.5, 1, 2} × b ∈ {−2, 0, 2}, giving **9 frozen configurations**. Hidden size, inputs, initial state and precision are unchanged.

**Selection (per seed; no TEST access).**
- **VAL subset (deterministic, 48 TRAIN histories):** h is VAL iff h is TRAIN, ((h mod 16) + ⌊h/16⌋) mod 4 = 2, and ⌊h/16⌋ < 12. This gives 3 histories per stage-4 prefix (all 16 covered) and 4 per high nibble 0–11 (checked in scratch).
- **FIT subset:** the other 144 TRAIN histories. Selection runs reject TEST and VAL histories in the sampler. Everything else is the §0 budget, with a fresh 8→70→3 readout (torch seed 6000+s, the same for all 9 configurations).
- **Criterion:** the probability-weighted VAL total excess against `world.q`, normalized within VAL (the same form as `component_excess`). This equals the expected VAL outcome Brier minus the oracle Brier, so it is an outcome-equivalent criterion.
- **Tie-break:** two configurations tie when their criteria differ by ≤ 1e-12. Ties go to the smaller |log₂ g|, then the smaller |b|, then the smaller b.
- **Refit:** a fresh 8→70→3 (torch seed 6000+s) on all 192 TRAIN histories at the selected (g*, b*). The §0 budget applies. TEST is evaluated **once**.
- F-TUNED32 uses the same (g*, b*) with the fresh 8→32→3 (5000+s) on all 192 TRAIN histories.

This rival is a **parameter-budget robustness comparison**. It does not replace the original matched-network control (consult #11 §2).

## 3. Transfer test (Q-LEARN)

All metrics are TEST excesses against `world.q`; TRAIN excesses are also reported. Write E(·) for the TEST E_total.

- **Prerequisite (E1 replication).** CAND meets A-FIT on TEST, with A-LEARN and integrity, in ≥ 8/10 fresh seeds. If not, the study is **UNRESOLVED (E1 not replicated)**, and §§4–6 are reported as descriptive only.
- **Per-seed transfer pass.** All of the following hold:
  - (a) integrity (finite outputs in (0,1); identity and restoration ≤ 1e-9);
  - (b) F-TRAINED meets A-FIT on TEST;
  - (c) E(F-TRAINED) ≤ ½ · E(F-INIT);
  - (d) E(F-TRAINED) ≤ ½ · E(F-TUNED32).
- **Verdict labels:**
  - **TRANSFER SHOWN:** ≥ 8/10 seeds pass.
  - **FROZEN-CORE READOUT SUFFICIENT AT THIS BUDGET:** F-INIT or F-TUNED32 meets A-FIT on TEST in ≥ 8/10 seeds. This label takes precedence over TRANSFER SHOWN, and when it applies, the learned core's advantage is not established by this comparison.
  - **TRANSFER NOT SHOWN:** ≤ 2/10 seeds pass.
  - **UNRESOLVED:** any other outcome.
- **Descriptive.** E(CAND) − E(F-TRAINED) measures co-adaptation loss, i.e. how much the original readout mattered.

## 4. Robustness comparison against R-TUNED843 (Q-LEARN robustness, not Q-NECESSITY)

- **ratio843(s)** = E(CAND) / E(R-TUNED843).
- **ADVANTAGE ROBUST TO TUNED FROZEN GRU-8 (843 TRAINABLE):** ratio843 ≤ ½ in ≥ 8/10 seeds, and R-TUNED843 meets A-FIT in ≤ 2/10.
- **TUNED FROZEN GRU-8 READOUT SUFFICIENT AT THIS BUDGET:** R-TUNED843 meets A-FIT on TEST in ≥ 8/10 seeds.
- **UNCLEAR:** any other outcome.
- The selected (g*, b*) per seed, the full VAL curve and the selection compute are reported. A selection that lands on a grid edge is flagged descriptively.

## 5. Gate-path reversion, controls and rescue (Q-CAUSE)

Interventions are applied to **F-TRAINED**, the trained core with its **fresh readout held fixed**. Running them with CAND's own co-adapted readout is reported descriptively only.

**Interventions (all three preregistered; none selected using TEST).** For k ∈ {r, z, n}, let W_hk be the 8×8 block of `weight_hh_l0`: rows 0–7 for r, 8–15 for z, 16–23 for n. Its displacement is δ_k = W_hk^0 − W_hk^T.

- **REV_k.** The recurrent updates for readings 5, 6, 7 and 8 (continuation steps 5–8) use W_hk^0 in place of W_hk^T. All other parameters stay trained. Updates 1–4 are intact.
- **RND_k,j** (j = 1…32): the same steps use W_hk^T + ε_j. Each ε_j has i.i.d. N(0,1) entries in the 8×8 block and is rescaled to ‖ε_j‖_F = ‖δ_k‖_F. The generator is torch seed 9000 + 100·(s−100) + 10·k_idx + 0, with k_idx = 0, 1, 2 for r, z, n. Draws are taken in order j = 1…32.
- **SHAM_k.** The same override hook substitutes a copy of W_hk^T at steps 5–8. Integrity requires forecasts identical to intact within 1e-12.
- **RESCUE_k.** After REV_k has been run, the override is removed (trained W_hk^T restored), and a fresh pass is run on the same inputs. Integrity requires that it reproduces the intact forecasts within IDENTITY_TOL = 1e-9. A failure here means the harness leaked state.
- **Descriptive only:**
  - TEMPORAL-RESCUE_k: revert at steps 5–6 and restore at steps 7–8.
  - EARLY-REV_k: revert at steps 1–4 only.
  - BIAS-REV_k: also revert `bias_hh` block k.
  - FOREIGN-INIT_k: substitute the W_hk^0 of a different fresh seed. This is a distribution-matched rather than norm-matched control.

**Metrics (all 256 histories are evaluated; TEST is primary).**
- ΔE_k = E(REV_k) − E(F-TRAINED), reported as total and separately for X, Y and XOR. ΔE_rand,j is defined the same way.
- **Prefix dependence.** For forecasts f(p, u), where p is the 4-bit prefix (readings 1–4) and u the 4-bit continuation:
  PD = Σ_u Σ_p P(p,u) ‖f(p,u) − f̄(u)‖², with f̄(u) = Σ_p P(p|u) f(p,u).
- **Continuation dependence CD** is the same with the roles of p and u swapped.
- PR_k = PD(REV_k) / PD(F-TRAINED) and CR_k = CD(REV_k) / CD(F-TRAINED). The analogous ratios are computed for every RND draw. PD and CD of the exact oracle are reported for scale.

**Per-seed SPECIFIC(k).** All of the following hold:
1. ΔE_k > max_j ΔE_rand,j. This is a one-sided exact rank test with p ≤ 1/33.
2. ΔE_k ≥ ¼ · (E(F-INIT) − E(F-TRAINED)). The effect must be material, i.e. at least a quarter of the transfer benefit.
3. SHAM_k and RESCUE_k integrity hold.

A seed that fails integrity counts as not SPECIFIC.

**Verdicts per k:**
- **REPLICATED SPECIFIC(k):** ≥ 8/10 seeds are SPECIFIC(k).
- **NOT SPECIFIC(k):** ≤ 2/10.
- **UNRESOLVED(k):** any other outcome.

**Content selectivity.** This is evaluated only when REPLICATED SPECIFIC(k) holds. Per seed, PREFIX-SELECTIVE(k) requires all of:
- PR_k ≤ ½,
- PR_k < min_j PR_rand,j,
- CR_k ≥ ¾.

The label **PREFIX-SELECTIVE EFFECT OF REVERTING W_hk** requires ≥ 8/10 seeds. Otherwise the result is "generic damage beyond matched-norm random perturbation, not shown to be prefix-content selective". Generic damage alone does not establish content-specific organization (consult #11 §4).

**Multiplicity.** The three k are reported in full. Each label needs its own ≥ 8/10 replication. No "any k" family upgrade is allowed.

## 6. Claim assembly (fixed in advance)

- **TRANSFER SHOWN and ≥ 1 REPLICATED SPECIFIC(k):**
  > "In the frozen W2 task, across 10 fresh GRU-8 seeds, trained recurrent cores transferred predictive structure to fresh, identically initialized readouts beyond their matched initial cores and the selected tuned frozen GRU-8, under the declared budget. Reverting the trained [W_hk] to its initialization during continuation steps 5–8 degraded held-out prediction beyond matched-norm random perturbations, with sham and rescue holding, reproducibly across seeds."

  The sentence "This effect selectively reduced prefix dependence." is appended only when the PREFIX-SELECTIVE label holds.
- **TRANSFER SHOWN, no REPLICATED SPECIFIC:** transfer is stated. "Gate-path reversion effects were not distinguishable from matched-norm perturbation or were not replicated."
- **TRANSFER NOT SHOWN or FROZEN-CORE READOUT SUFFICIENT:** that label is stated. Reversion results are descriptive only.
- **Never claimed:**
  - that W_hk "stores" the prefix or the chart;
  - a localized or independently manipulable state component;
  - that recurrent training is necessary (Q-NECESSITY);
  - a mechanism, or that the intervention is unique;
  - other architectures or budgets;
  - irreducible joint state;
  - C4, consciousness or organism claims;
  - any retroactive change to PR #5 E2 or E3.

## 7. E3 pipeline validation (optional piece (ii), folded in; additive, no retroactive E3 success)

The purpose is to test whether PR #5's E3 instrument can detect a known localized code. Nothing here relabels PR #5's E3 (NOT LOCALIZED BY THIS INTERVENTION). The complement-transplant result is **not** reinterpreted as a successful E3 (consult #11 §3).

**P1. Held-out stage-4 decoder accuracy** (on F-TRAINED, CAND and F-INIT cores of the fresh seeds).
- For each parity fold, fit the frozen centered ridge (λ = 1e-3) on the 8 fit-fold prefixes. Predict the held-out 8 prefixes' exact stage-4 chart.
- Report:
  - R² per coordinate (m_x, m_y, c);
  - RMSE;
  - the principal angles between the fold-0 and fold-1 bases;
  - the singular values.
- **DECODER ADEQUATE:** held-out R² ≥ 0.9 on all three coordinates on both folds, **and** the largest inter-fold principal angle ≤ 30°.
- Otherwise the label is **DECODER-LIMITED**, and any E3-type null on that seed is reported with that tag.
- PR #5 seeds 0–9 saved no checkpoints. P1 on them is possible only through an exact deterministic replay of the frozen cells, verified by matching recorded final errors within 1e-12. That replay needs its own approval. It is optional and descriptive.

**P2. Synthetic positive and negative controls (analytic harness; no training).**
- **The harness.** z ∈ ℝ⁸, z = Q φ + s·R ν:
  - Q (8×3) and R (8×5) are orthonormal complements, drawn from a fixed seed. The study uses 100 draws.
  - φ is the exact chart (m_x, m_y, c).
  - The harness's `step` decodes φ = Qᵀz and applies the exact transition (stage > 1) and observation.
  - The nuisance follows ν' = tanh(A ν + a·reading + C·onehot), with A fixed at spectral radius 0.9.
  - The `readout` is `forecasts(Qᵀz)`, so ν carries no forecast content.
- **The test.** The frozen PR #5 E3 suite (`interventions`) is run **unchanged** with the harness in place of the model.
- **P2+ (known causal 3-d subspace).** Nuisance scales s ∈ {0, 0.03, 0.1, 0.3, 1.0} (chart SD ≈ 0.167).
  - **PIPELINE VALID** requires E3 LOCALIZED in ≥ 95/100 draws at s ∈ {0, 0.03}.
  - The curve over s is reported.
- **P2− ("decodable but unused").** A linear chart copy is placed in Q and refreshed at stage 4 only. The forecast reads a nonlinear (elementwise cubic) chart code carried in R. Expectation: not LOCALIZED. This is descriptive.
- **Analytic pilot already run (scratch; informs P1 and P2, not an E3 result).**
  - Files: `/workspace/scratch/pr5/repro/e3_decoder_pilot.py` and `.json`.
  - With z4 = Qφ + s·Rν and random ν, the frozen cross-fitted decoder recovers span(Q) exactly at s = 0 (max angle ~1e-6°).
  - The median largest principal angle grows with nuisance: **2.7° at s = 0.01, 7.5° at 0.03, 16.8° at 0.1, 33.5° at 0.3 and 59° at 1.0** (200 draws).
  - Held-out R² on m_x and m_y stays ≥ 0.98 throughout; only c degrades (0.97 → 0.32 → −2.9).
  - So **held-out R² alone cannot certify the transplant basis**, and P1 includes the principal-angle criterion for that reason. With 8 fit points in 8-d, low-variance chart directions (c) are the most exposed.
- **Known frozen-code edge case (flag V-1).** In an ideal positive control the complement transplant leaves forecasts exactly at the recipient's, so the complement ratio's denominator is 0. `_rho` then returns None, and the frozen rule counts None as failing LOCALIZED. P2+ therefore reports, separately, (a) the frozen rule verbatim and (b) the rule with complement-None read as +∞, which passes ≥ ¾. Only (a) is the pipeline-valid gate. (b) is a proposed future-protocol amendment.

## 8. Integrity, determinism and reporting

- Single process, deterministic algorithms, `set_num_threads(1)`.
- All W^0, W^T and readout checkpoints are saved with sha256.
- Generator seeds are fixed as stated: 1000+s episodes, s init, 5000+s fresh readout, 6000+s for the 843-parameter rival, 9000+… for random perturbations.
- Missing cells are reported. No seed is replaced.
- Every table lists all 10 seeds, all three k, all 32 random draws (summary plus maximum), sham and rescue gaps, and PD, PR, CD and CR.
- Freezing happens before training: the protocol hash, code hashes and test suite (covering override-hook sham identity, rescue identity and parameter counts 456/387/843) are frozen first.

## 9. Thirteen admission answers

1. **Q1.** This addresses Q-LEARN (does the learned GRU-8 recurrence carry transferable predictive structure?) and a bounded Q-CAUSE prerequisite (does a learned recurrent component contribute causally and specifically to prediction?). It is a bounded prerequisite of the ACI C3-type acquisition question.
2. **Q2.** One hypothesis: the trained GRU-8 recurrent core carries predictive structure that transfers to fresh readouts, and reverting a trained hidden-to-hidden gate matrix during continuation degrades prediction beyond matched-norm random damage, reproducibly.
3. **Q3.** Falsifiers:
   - TRANSFER NOT SHOWN, or FROZEN-CORE READOUT SUFFICIENT.
   - NOT SPECIFIC(k) for every k.
   - E1 not replicated, which gives UNRESOLVED.

   Sham or rescue failures invalidate the affected seeds.
4. **Q4.** Strongest simpler explanations, each with information and resource parity:
   - Supplied random dynamics plus a trained readout: F-INIT.
   - A better-tuned frozen GRU-8 at an equal trainable count: R-TUNED843 and F-TUNED32.
   - Generic damage from any perturbation of that size: RND_k.
   - Harness artifacts: SHAM_k and RESCUE_k.
   - Co-adapted readout specificity: the fresh readouts.
5. **Q5.** PR #5's frozen evidence makes this necessary:
   - E2 shows a benefit from recurrent training, but only against one frozen init.
   - E3 did not localize content, and K-FR E3 is UNRESOLVED.
   - No checkpoints were saved.
   - Consult #11 calls for transfer, reversion and a tuned rival before any claim about a learned recurrent component.
6. **Q6.** After success, record the §6 scoped ceiling and the ORIGIN/ROLE/REDUCTION row: "learned W_hk contributes specifically under reversion". Then consider a separately approved, mechanism-level study (e.g. which gate path carries prefix retention) without claiming localization of content.
7. **Q7.** After failure or UNRESOLVED:
   - If transfer fails, the learned structure is readout-co-adapted, and the E2 benefit is not attributed to a transferable core.
   - If reversion is non-specific, record generic sensitivity only.
   - If the tuned rival suffices, E2's generality is limited to the untuned init.

   Any architecture or budget change is a new protocol.
8. **Q8.** Small GRU-8 networks on CPU: 140 runs of 4000 steps. The P2 analytic harness needs no training. Exact enumeration is used for evaluation. No organism model.
9. **Q9.** Organizational (acquired recurrent organization and its causal role) plus engineering (training, harness). No substrate claim.
10. **Q10.** The claim ceiling is §6, including the "Never claimed" list.
11. **Q11.** Cognitive layer: a C3-type history-integrating predictive state. C4 (internal evaluation dissociable from first-order inference) and C5 remain unsupported and untested.
12. **Q12.**
    - Supplied: the GRU cell, its random initialization, the timing scaffold, the readout architecture, losses, feedback, the split, and the tuned grid.
    - Acquired (if shown): the trained recurrent parameters and their transferable contribution.
    - The tuned (g, b) is supplied and selected, not acquired.
13. **Q13.** Belief changes by result:
    - TRANSFER SHOWN plus REPLICATED SPECIFIC: "recurrent training helps" moves to "a learned recurrent component transfers and contributes specifically under reversion" (Q-CAUSE PARTIAL, bounded).
    - Transfer fails: E2 is read as readout co-adaptation.
    - Tuned rival suffices: "K-FR failure reflects an untuned init."

    Q-NECESSITY stays NOT_ESTABLISHED in every case.

## 10. Q-separation and the ORIGIN/ROLE/REDUCTION ledger

| Item | ORIGIN | ROLE | REDUCTION (literal) | Question |
| --- | --- | --- | --- | --- |
| Trained recurrent core W^T | ACQUIRED (CAND training) | carries transferable predictive structure, if TRANSFER SHOWN | "frozen-core readout sufficient" if observed | Q-LEARN |
| Tuned frozen core W^0(g*, b*) | SUPPLIED + SELECTED | robustness rival | "tuned frozen GRU-8 readout sufficient" if observed | Q-LEARN (robustness) |
| Gate matrix W_hk^T contribution | ACQUIRED | contributes specifically under REV_k, if REPLICATED SPECIFIC(k) | "indistinguishable from matched-norm damage" if observed | Q-CAUSE |
| Prefix-content selectivity | UNRESOLVED unless PREFIX-SELECTIVE(k) | — | "generic damage" | Q-CAUSE |
| Necessity of recurrent training | NOT TESTED | — | — | Q-NECESSITY (not addressed) |
| Existence of an exact solution | from PR #4 (and the K-EXACT precision erratum B) | — | — | Q-EXIST (not addressed here) |

## 11. Open flags for Astra

- **G1.** The SPECIFIC rule: exceed all 32 matched-norm draws (p ≤ 1/33) **and** ≥ ¼ of the transfer benefit. Is 32 draws enough, and is materiality relative to E(F-INIT) − E(F-TRAINED) the right scale?
- **G2.** The transfer thresholds: ½ against **both** F-INIT and F-TUNED32, plus A-FIT. Should F-TUNED32 be a gate or descriptive?
- **G3.** Selection is **per seed** on that seed's own init, which gives the strongest rival. The alternative is a single pooled (g*, b*).
- **G4.** The VAL rule omits high nibbles 12–15 by construction: any 3-of-4 choice per prefix drops 4 high nibbles. Is that acceptable, or should VAL be drawn by a different deterministic rule?
- **G5.** The content-selectivity thresholds (PR ≤ ½, CR ≥ ¾) and the PD/CD definitions are new engineering choices.
- **G6.** `bias_hh` blocks are excluded from REV_k (BIAS-REV_k is descriptive). Confirm.
- **G7.** Interventions run on the fresh-readout core (F-TRAINED). CAND's own readout is descriptive. Confirm this primary choice, which follows consult #11 §4: "With those readouts fixed".
- **G8.** The P2 harness is an analysis instrument with exact-filter dynamics. It is not a candidate architecture. Confirm it is not a "new architecture family".
- **G9 (= V-1).** The complement-None tie rule in the frozen E3 code (§7).
- **G10.** Approval: the study needs Aidan's separate explicit approval for new training (header).
