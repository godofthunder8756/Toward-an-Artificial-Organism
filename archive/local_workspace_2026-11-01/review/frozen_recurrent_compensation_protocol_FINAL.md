# Frozen recurrent matrices with learned compensation: protocol (FINAL v1)

**Status:** FINAL text, applying Astra consult #19 (verdict: **FREEZE WITH NAMED EDITS**). It is ready to be frozen by the ACI Research Specialist together with the implementation. This document freezes nothing itself, and no training has been run for it.
**Training approval:** Aidan's approval is **PENDING** (§0.2, widget t26s1).
**Source rulings:** Astra consult #18, §§6–8 and the closing recommendation, and consult #19 (Findings 1–4, Edits 1–7, the §13 and §14 rulings, and the final approval question). Both are quoted verbatim where marked.
**Scope:** W2 world, GRU-8 family only. Below C4. No new architecture family, no protected controller or register, no organism work. No consciousness claim.
**Predecessor:** `frozen_recurrent_compensation_protocol_draft_v1.md` (sha256 60517040881208ed6508e5ff2d4f18213fbf9d70370bab8b7e42cceb695ec41b), left untouched.

Consult #19, verbatim: "This remains below C4, within the GRU family. Scientific clearance does not authorize training."

---

## 0. Framing (fixed)

This study is a **search for compensation and counterexamples to necessity. It is not a necessity certificate.**

The question: hold every hidden-to-hidden matrix `weight_hh` at its random initialization W0 at all eight updates, and let the input weights, both biases and the readout learn. Can that remaining computation reach the declared target T(θ) ≤ 1?

Consult #19, Finding 2, verbatim: "Freeze only `weight_hh_l0`. Training W_ih and the biases can change the recurrent dynamics despite that fixed matrix. Do not describe R-FIX as having an entirely untrained or fixed recurrent computation."

Consult #18, verbatim:

> "Compensation would not negate the existing causal result: parameters can contribute causally in one trained implementation without being indispensable to another."

> "One verified witness refutes absolute impossibility for that particular restricted class and target. An 8/10 rule establishes reproducibility, not the logical minimum needed for a counterexample."

> "Failure means only 'not reached within declared search.'"

A failure is not a certificate. The certificate Astra described is a validated lower bound inf T > 1 over the entire declared restricted domain, or a complete search of an explicitly finite class. This protocol does not attempt one (§8.3).

## 0.1 Inherited unchanged from PR #7 / PR #8 / PR #9

- The W2 world and its 256 histories h = p + 16u.
- The TEST and VAL split predicates (`is_test_history` and `is_val_history`).
- The oracle q*. PD(q*) = 0.0138386222, recomputed as 0.013838622233977797 (Appendix B).
- The A-FIT thresholds, frozen as `Fraction`s in `World.afit_threshold`:
  - TEST total = E_cur_TEST/4 = 0.0203873 (float);
  - TEST XOR = E_PROD_TEST/4 = 0.00228962 (float).
- `component_excess`, `afit_holds`, and `l_prefix` (graded_reversion_outcomes.py: the uniform mean over the 16×16 grid, no /3).
- CoreGRU: `nn.GRU(9, 8)` with zero initial state. Input is the reading (±1) plus an 8-way stage one-hot. Readout is `8 → H → 3` (tanh hidden, sigmoid output).
- The PR #7 optimization recipe:
  - Adam (betas and eps from the spec, weight decay 0);
  - STEPS = 4000, BATCH = 256;
  - cosine LR 1e-3 → 1e-4;
  - grad-norm clip 1.0 over each arm's own trainable parameter list;
  - TEST histories rejected from training, VAL not rejected (§5);
  - squared-error loss on sampled labels;
  - `set_num_threads(1)` and `use_deterministic_algorithms(True)`;
  - a per-run episode generator seeded 1000+s.
- eps0 = 1e-12 and IDENTITY_TOL = 1e-9.
- Canonical JSON/base64 float32 checkpoints with sha256.

## 0.2 Approval record (PENDING)

| item | value |
| --- | --- |
| What needs approval | The training phase: **30 CPU training runs = 3 arms (CAND, R-FIX-32, R-FIX-48) × 10 seeds (400–409)**, followed by the specified evaluation. |
| Count confirmation | 3 × 10 = 30, one run per arm per seed. There is no F-TRAINED or F-INIT arm. |
| Required | Aidan's **explicit** approval **AND** Astra clearance. |
| Astra clearance | Consult #19: FREEZE WITH NAMED EDITS. Clearance is conditional on those edits being applied (this document) and on the protocol and implementation being frozen. "Scientific clearance does not authorize training." |
| Aidan's approval | **PENDING.** Outstanding widget **t26s1**. |
| Carry-over | **None.** Prior approvals do not carry over, including PR #9 Phase B (1:05 AM ET, widget t23s2). |

**Outstanding widget t26s1, question verbatim:**

> "Approve fresh-seed GRU-8 training (seeds 400-409, 30 runs: normal plus two frozen-recurrent variants) for the frozen-recurrent compensation study once Astra clears the protocol?"

**Scope statement: Astra consult #19 final approval question, verbatim.** This governs what any approval covers:

> "Approve 30 CPU training runs for 'Frozen recurrent matrices with learned compensation': seeds 400-409, with CAND, R-FIX-32 and R-FIX-48 trained once per seed for 4000 steps under the PR #7 recipe, followed by the specified evaluation, once Astra's named edits are applied and the protocol and implementation are frozen? This approval excludes Appendix A, C and D, restarts, hyperparameter searches and additional training runs."

**Exclusions (from the scope statement):**
- no Appendix A, C or D;
- no restarts;
- no hyperparameter searches;
- no additional training runs.

The synthetic-fixture freezing test of §4 is not a fresh-seed study run; see §4 and ambiguity A3.

**Wording comparison: t26s1 vs Astra's scope question. Material differences are flagged.**

The two agree on:
- the seeds (400–409);
- the count (30);
- the arms ("normal plus two frozen-recurrent variants" means CAND, R-FIX-32 and R-FIX-48).

t26s1 does not state:
1. any exclusions: Appendices A, C and D, restarts, hyperparameter searches and additional training runs are not mentioned;
2. the per-run budget ("trained once per seed for 4000 steps under the PR #7 recipe");
3. the condition that the protocol **and implementation** be frozen after the named edits. t26s1 conditions only on "once Astra clears the protocol".

Items 1 and 3 are **material**. On its face, t26s1 is broader and less conditioned than Astra's scope.

This protocol reads any "yes" on t26s1 as limited to Astra's scope statement above. The parent or Specialist should decide whether to re-ask Aidan with Astra's exact wording before treating approval as granted.

---

## 1. Arms (parameter accounting verified from code)

"32" and "48" are the **readout hidden width H** of the `8 → H → 3` head (`readout_fc1: 8→H`, `readout_fc2: H→3`). The readout has 12H + 3 parameters. The GRU core is fixed at 456 parameters:
- `weight_ih_l0`: 216;
- `weight_hh_l0`: 192;
- `bias_ih_l0`: 24;
- `bias_hh_l0`: 24.

These counts come from instantiating `CoreGRU(H)` in the frozen code (Appendix B).

| arm | head H | frozen | trainable | # trainable | # stored total |
| --- | --- | --- | --- | --- | --- |
| **CAND** | 32 | nothing | everything | **843** (456 + 387) | 843 |
| **R-FIX-32** | 32 | `weight_hh_l0` = W0 (192) | W_ih, b_ih, b_hh, readout | **651** (216 + 48 + 387) | 843 |
| **R-FIX-48** | 48 | `weight_hh_l0` = W0 (192) | W_ih, b_ih, b_hh, readout | **843** (216 + 48 + 579) | 1035 |
| (R-FIX-70, not run) | 70 | `weight_hh_l0` | as above | 1107 (264 + 843) | 1299 |

**What "parameter-matched" means.** Consult #19, Finding 1: "R-FIX-48 matches CAND's trainable count, not stored count, allocation or optimization geometry."

R-FIX-48 matches CAND in **number of trainable parameters** (843 = 843). It does not match in:
- stored total: 1035 vs 843;
- allocation: CAND has 456 recurrent + 387 readout, R-FIX-48 has 264 recurrent + 579 readout;
- optimization geometry.

R-FIX-32 has the same architecture as CAND and an identical initialization, but 192 fewer trainable parameters.

Consult #19, Finding 1, verbatim replacement text:

> "R-FIX-32 tests compensation with the original architecture. R-FIX-48 additionally tests compensation with an equal total trainable-parameter count allocated differently. These comparisons do not isolate parameter count from readout width, parameter allocation or optimization effects."

**Accounting notes:**
1. The 70-unit head gives 1107 trainable parameters, not 843. This is the consult #18 correction, confirmed from code.
2. **Naming rule (§13 ruling 2):** "Accept arm-specific naming; bare counts must not identify arms." The bare number "843" previously labelled the 70-head readout-only rival. Reports always use the arm name.
3. The existing `train_arm(freeze_recurrent=True)` freezes **all four** recurrent tensors. That is F-INIT/F-TRAINED semantics, **not** R-FIX. R-FIX needs a freezing mode that freezes `rnn.weight_hh_l0` only (§4). This is a harness change, not an architecture change.
4. **F-INIT ≠ R-FIX.** F-INIT freezes the whole W0 core (W_ih, W_hh, both biases) and trains a fresh readout. R-FIX also trains W_ih and both biases, which can change the recurrent dynamics despite the fixed matrix (Finding 2). The historical F-INIT result says nothing about R-FIX: T ≈ 11.55–17.36 across the 30 existing F-INIT checkpoints (Appendix B).

## 2. Seeds, pairing and streams

| item | value |
| --- | --- |
| Seeds | **400–409**: fresh, and disjoint from 100–109, 200–209 and 300–309. All ten seeds are retained regardless of initialization results. **No seed replacement.** |
| Init, CAND and R-FIX-32 | `build_initialized(s, 32)`. The **whole init is identical** between the two arms. |
| Init, R-FIX-48 | `build_initialized(s, 48)`. **Partially paired** (see below). |
| Episode stream | Generator `1000 + s` (1400–1409) for all three arms of seed s, with identical rejection (TEST only). Streams are therefore **identical across arms**, batch for batch, and checked by digest (§9). |
| Budget | Identical for all arms: 4000 Adam steps, batch 256, the same LR schedule and clip value. One run per arm and seed. **No restarts.** |
| Draw order | All 30 inits are drawn and hashed (Stage 0) before any training. |

**R-FIX-48 pairing.** The four GRU tensors are identical to CAND's, so **W0 is the same matrix in all three arms of a seed**. `readout_fc1.weight` rows 0–31 equal CAND's. The other readout tensors differ:
- `fc1.bias`, `fc2.weight` and `fc2.bias` differ in shape or RNG position;
- `fc2` also has a different default bound (1/√48 vs 1/√32).

The wider head is **partially paired only**. Complete initialization matching is not claimed.

**Pairing assertion (Finding 3: "Assert the full-core equality for all ten seeds, not just the two feasibility examples").** The Stage-0 runner must assert, for **every** seed 400–409, that:
- all four GRU tensors are equal between `build_initialized(s, 32)` and `build_initialized(s, 48)`;
- the CAND and R-FIX-32 inits are fully equal.

Any failure is an integrity failure for that seed. A pre-freeze read-only check (init construction only, no training, no evaluation) already confirms this for all ten seeds (Appendix B, `pairing_all.log`). The Stage-0 assertion remains mandatory.

## 3. Target (fixed)

T(θ) = max( L_prefix(θ) / (τ·PD(q*)), E_total_TEST(θ) / thr_total_TEST, E_XOR_TEST(θ) / thr_XOR_TEST ).

τ = 0.25. The target is L_prefix ≤ 0.25·PD(q*) AND both TEST A-FIT inequalities (consult #18 §7). Numerical decisions follow the dual-evaluator rule of §3.1.

**τ disclosure (mandatory wording):**

> "tau = 0.25 was chosen after prior results were known. Across the 30 existing CAND checkpoints (seeds 100–109, 200–209, 300–309), L_prefix/PD ranged 0.034–0.110, i.e. L_prefix/(0.25·PD) ≤ 0.44."

Followed by consult #19, Finding 4, verbatim:

> "The XOR term determines T in all 30 existing CAND checkpoints. The prefix-loss constraint is satisfied with margin in those checkpoints. Which constraint limits R-FIX is unknown; all three target components remain decision-bearing."

Further rules:
- §14 ruling 1: report all components and their binding frequencies, per arm. The study is **not** described as effectively XOR-only before R-FIX is observed.
- T is evaluated at the init checkpoint (descriptive, plus the witness and acquisition rules of §7) and at the **final-step** checkpoint (step 4000).
- L_prefix is uniform over all 256 histories, as evaluation (§13 ruling 7). E is TEST-weighted (`component_excess`).
- Evaluation is in float64 from the float32 checkpoint.
- Validation selection: **none** (§5).

### 3.1 Numerical decision rule (consult #19, Edit 2; applies identically to CAND, R-FIX-32 and R-FIX-48, at init and final)

The two evaluators are:
- (E1) the frozen evaluator: `evaluate_arm`, `l_prefix` and `component_excess`;
- (E2) an independent float64 NumPy forward pass and metric implementation.

Each evaluator computes the three normalized components and T independently. Verbatim:

```text
t = 1e-9

VERIFIED TARGET PASS:
    both evaluators give T < 1 - t

VERIFIED TARGET FAIL:
    both evaluators give T > 1 + t

BOUNDARY / NUMERICALLY UNRESOLVED:
    neither condition holds

Evaluator disagreement beyond the agreement tolerance:
    integrity failure
```

Agreement, for each normalized component `x, y`, verbatim:

```text
abs(x-y) <= 1e-12 + 1e-9*max(abs(x), abs(y))
```

Consult #19 verbatim: "Both evaluators must independently pass the target rule; agreement alone is insufficient. Call these **numerically verified witnesses under the declared float64 evaluation**, not formal real-arithmetic certificates."

Float32 (native) evaluation may be reported descriptively. It does not gate any claim (§14 ruling 5). Consult #19 verbatim: "Dual evaluation is a numerical cross-check, not a validated error bound for real arithmetic."

## 4. Harness additions (written and frozen with the protocol; engineering only)

1. **`train_arm_rfix(model, episode_seed)`.** PR #7 `train_arm` with exactly one difference: `rnn.weight_hh_l0.requires_grad_(False)`, and every other tensor `True`.
   - The Adam parameter list and `clip_grad_norm_` cover exactly that arm's trainable tensors.
   - §14 ruling 3, verbatim: "clip each arm's actual trainable parameter set. Do not compute artificial gradients through frozen parameters to imitate CAND's clipping."
   - Everything else is identical to `train_arm`: the generator, `sample_batch`, the loss, the LR schedule and the failure checks.
2. **Freezing checks (consult #19, Edit 4, verbatim):**

   > "For every R-FIX run, assert before optimization that weight_hh is the only frozen parameter tensor, is absent from the optimizer parameter list, and has requires_grad=False. Check after backward that its gradient remains None. Check W0 byte equality after training and after checkpoint reload."

   - The "after backward" gradient check runs at every step, or at minimum the first and last step. This is an implementation choice to be fixed at freeze; see ambiguity A4.
   - Byte equality uses sha256 of the tensor bytes, compared with the Stage-0 W0 hash.
   - Any failure makes the run invalid.
3. **Synthetic-fixture test of the freezing implementation (Edit 4).** Verbatim: "A `.grad is None` check before backward is vacuous. Test the freezing implementation on a synthetic fixture; do not consume an additional fresh-seed training run."
   - The fixture is a model built from a non-study seed, on synthetic inputs, run for a handful of optimizer steps.
   - It exercises `train_arm_rfix`'s checks, including a deliberately mis-frozen negative case that must be caught.
   - It is not a study run, has no evidential role, and uses none of seeds 400–409 or streams 1400–1409.
   - It is run as part of implementation freezing, not by this drafting task.
4. **No evaluation of trained models in Stage 1.** Stage 1 logs training loss only. Init checkpoints are evaluated only in Stage 2, together with the finals, so that no outcome information exists before the Stage-1 seal.

## 5. Validation selection, restarts, reporting (frozen)

- **Validation selection: none.** No early stopping, no checkpoint choice and no hyperparameter choice.
  - VAL histories are not rejected from training, as for CAND in PR #7.
  - The former VAL subset is therefore an **in-sample descriptive subset** in this study, because it participates in training. It is reported descriptively only.
- **Restarts: none.** Exactly one run per arm and seed. Diverged or invalid runs are not re-run and seeds are not replaced (§13 rulings 6 and 12).
  - §13 ruling 6: "Accept no selection or restarts. This limits negative conclusions; it is not inherently the strongest search."
- **Hyperparameters:** the PR #7 recipe, unchanged, for all arms.
- **Reporting:** every seed and arm, including invalid and boundary runs. For init and final:
  - each evaluator's three normalized T components and T;
  - the §3.1 classification;
  - E_total and E_XOR (TEST and TRAIN);
  - L_prefix;
  - **C_prefix** and **G_prefix** (below);
  - the in-sample descriptive subset (former VAL) errors;
  - the final training loss.

  Also reported:
  - the paired difference T(R-FIX) − T(CAND), descriptive;
  - binding-component frequencies per arm;
  - best and median T per arm, descriptive.

**Prefix quantities (consult #19, Edit 5, verbatim):**

```text
C_prefix = PD(q*) - L_prefix(final)
G_prefix = L_prefix(init) - L_prefix(final)
```

`G_prefix` is named "within-run prefix-loss improvement." Neither quantity gates the target.

The old paired-arm quantity from PR #7/#8 is undefined here, because there is no F-INIT arm. It is not reported.

## 6. Validity (per arm and seed)

A run is **invalid** on any of the following:
- a training integrity failure (non-finite loss, gradients or weights, as in PR #7);
- a checkpoint round-trip mismatch;
- `outputs_valid` false;
- identity checks failing at IDENTITY_TOL;
- any §4 freezing check failing (R-FIX);
- a Stage-0 pairing assertion failing;
- an episode digest mismatch;
- a Stage-2 checkpoint sha not matching the sealed manifest;
- **evaluator disagreement beyond the §3.1 agreement tolerance.**

Invalid checkpoints supply no witness.

**Eligibility: consult #19, Edit 1, verbatim replacement of the initialization eligibility rule:**

> "T(init) is descriptive and does not determine eligibility for an existence witness. A valid initialization or final checkpoint that passes the numerical verification rule supplies a witness for its specified frozen W0 and head width. Report initialization witnesses separately. Acquisition of target attainment requires a verified above-target initialization followed by a verified below-target final checkpoint."

"Retain all ten seeds and all 30 scheduled runs regardless of initialization results. Do not replace seeds."

"For the acquisition annotation, use both evaluators to establish `T(init) > 1 + T_BOUNDARY_TOL`. An initialization near the boundary cannot establish the initially-failing condition."

The acquisition annotation for a run therefore requires both of the following under §3.1:
- init classified VERIFIED TARGET FAIL;
- final classified VERIFIED TARGET PASS.

## 7. Labels (per arm; decided only in Stage 2)

**Witnesses.** A **numerically verified witness under the declared float64 evaluation** is a valid checkpoint, initialization or final, classified VERIFIED TARGET PASS under §3.1.

- R-FIX final witnesses need W0 byte-equal after training and after reload.
- An init checkpoint has `weight_hh` = W0 by construction, so a verified-pass initialization is an existence witness for its W0 and head width.
- Because the CAND and R-FIX-32 inits of a seed are identical, one such init witness is a single witness. It is reported once, under H = 32, with CAND noted. See ambiguity A1.

**Label rules (consult #19, Edit 3, verbatim):**

> "Per arm, report final verified target passes out of ten, initialization witnesses, invalid runs and boundary runs separately. One verified checkpoint supplies an existence witness. At least eight final verified passes earns TARGET REACHED REPRODUCIBLY. If more than two runs are invalid or numerically unresolved, the reproducibility label is UNRESOLVED; otherwise fewer than eight passes gives REPRODUCIBILITY CRITERION NOT MET."

When zero witnesses are found (verbatim):
- "If all ten final evaluations resolve above target, use `TARGET NOT REACHED WITHIN DECLARED SEARCH`."
- "Otherwise use `NO VERIFIED WITNESS FOUND`, with unresolved and invalid counts."

"CAND follows the same numerical and evaluability rules. CAND failure still does not invalidate an R-FIX witness."

**Per-arm report block (mandatory, all three arms):**
- final verified passes: n/10;
- initialization witnesses: count;
- acquisition annotations: count;
- invalid runs: count, with reasons;
- boundary or numerically unresolved runs: count;
- existence label: WITNESS FOUND, `TARGET NOT REACHED WITHIN DECLARED SEARCH`, or `NO VERIFIED WITNESS FOUND`;
- reproducibility label: TARGET REACHED REPRODUCIBLY, REPRODUCIBILITY CRITERION NOT MET, or UNRESOLVED.

**CAND** is the unrestricted comparator. Its labels are reported with the same rules. If CAND does not reach TARGET REACHED REPRODUCIBLY, the R-FIX-vs-CAND comparison is reported as UNRESOLVED (comparator not reproduced). R-FIX witnesses still stand (§13 ruling 10).

There is no pooled R-FIX label and no comparison test between arms. R-FIX-32 vs R-FIX-48 differences are descriptive.

There is no multiplicity correction for existence statements: they are verified-instance claims, not statistical inferences. The search size must be disclosed: 20 final R-FIX checkpoints plus their 20 inits.

## 8. Claims (fixed in advance)

### 8.1 Allowed wording

**Witness (consult #19, Edit 6, verbatim):**

> "For the reported W0 and head width H, a numerically verified GRU-8 checkpoint reaches the declared target while weight_hh remains at W0 throughout all eight updates. This is a counterexample to the claim that departing from that specified W0 is necessary for this target within the declared architecture. It does not establish success for other frozen matrices or negate the existing causal contribution of trained matrices in other implementations."

If initialization failed and training succeeded (the acquisition annotation), append verbatim:

> "The target was attained after training input weights, both biases and the readout, without training weight_hh."

If the witness is an initialization witness, state that it is one. It demonstrates existence for that W0 and H, not acquisition.

**Reproducible (adds):** "At least eight of ten final checkpoints were verified target passes, establishing reproducibility within the declared search, not a logical minimum."

**Not reached:** "R-FIX-H: TARGET NOT REACHED WITHIN DECLARED SEARCH (one run per seed, 4000 steps, PR #7 recipe, no restarts). Failure means only 'not reached within declared search.' This is not a necessity certificate and does not establish that departing from W0 is necessary."

**No verified witness:** "R-FIX-H: NO VERIFIED WITNESS FOUND (u unresolved, i invalid)." No inference beyond the counts.

**Scope of other questions (consult #19, Edit 6, verbatim). This replaces the blanket "unchanged" statement:**

> "Earlier acquisition, transfer and exact-solution results are unchanged. This study can add restricted-class existence evidence and, where the initialization-to-final condition holds, evidence of acquired target attainment. It does not test transfer or add a new causal-organization claim."

**Mixed outcomes:** each arm is reported with its own labels. Nothing is inferred about mechanism.

### 8.2 Forbidden wording

- "recurrent learning is necessary", "necessity established", "certificate", "impossible without recurrent training";
- "formally verified" or "proved" for a numerically verified witness;
- "the PR #8/#9 causal result is refuted or weakened by compensation";
- "R-FIX shows the recurrent matrix is irrelevant or not causal";
- describing R-FIX as having an entirely untrained or fixed recurrent computation (Finding 2);
- "the study is XOR-only" or "τ is irrelevant" (§14 ruling 1);
- claiming success for other frozen matrices, or any generalization beyond W2, GRU-8, the reported W0 and H, this target and this budget;
- describing an initialization witness as acquisition;
- any C4, C5, consciousness, agency or organism language.

### 8.3 Claim ceiling (consult #18, verbatim)

> "A certificate must establish `inf T(theta) > 1` throughout the restricted domain, alongside an unrestricted witness with `T <= 1`. The domain must specify the frozen matrix, remaining weight ranges or precision, readout size and supplied timing information."

> "That would establish necessity of **departing from that specified frozen matrix within that domain**. It would not establish universal necessity of recurrent training. A simple prefix-separation argument should not be presumed available: trainable input weights, gates and readout may retain substantial representational flexibility."

The ceiling of this study is one of the following, never a certificate:
- numerically verified existence (or reproducibility) of a witness for the reported W0 and H, under the declared float64 evaluation;
- "not reached within declared search";
- "no verified witness found".

## 9. Two-stage sealed-manifest runner (consult #18 §6 applied; §13 ruling 11)

Consult #18 verbatim: "For future studies, use a two-stage runner: write and seal the transformed-path manifest, then evaluate curves from that manifest. A separate commit or timestamped artifact improves provenance but is not a retroactive requirement here."

There are no transformed paths in this study. The analogue is a sealed **checkpoint manifest**.

- **Stage 0 (pre-training).** Draw all 30 inits in seed order and run the §2 pairing assertions for all ten seeds. Write `manifest_stage0.json` containing:
  - the init checkpoint sha256 and W0 tensor sha256 per arm and seed (W0 is equal across the three arms of a seed);
  - an episode-stream digest per seed: sha256 of all 4000 × 256 accepted bit and label arrays, regenerated from generator 1000+s without training;
  - the code-tree sha, the frozen protocol sha and the synthetic-fixture test result.

  Seal it with a commit or timestamped artifact.
- **Stage 1 (training only).** Train the 30 runs. Write `manifest_stage1.json` containing:
  - the final checkpoint sha256 values;
  - training integrity flags, steps completed and final training loss;
  - all §4 freezing-check results;
  - the episode digests re-derived during training, which must equal Stage 0.

  There is no evaluation of any checkpoint against the target in Stage 1. **Seal it with a separate commit** (required here, prospectively) before Stage 2 code runs.
- **Stage 2 (evaluation from the manifest).** Load only init and final checkpoints whose sha matches the sealed manifests. Run E1 and E2 and apply §3.1. Assign §7 labels mechanically.
- Any mismatch between stages makes that run invalid. There is no re-training.

## 10. Thirteen admission answers

1. **Q1. Question.** Q-NECESSITY, restricted-class form, bounded. With `weight_hh` frozen at W0, can input weights, both biases and the readout compensate enough to reach the target? This is a search for counterexamples, not a certificate.
2. **Q2. Hypothesis and criterion.** There is no directional hypothesis. Per arm, the criteria are:
   - existence: ≥ 1 numerically verified witness (an initialization or final checkpoint);
   - reproducibility: ≥ 8/10 final verified passes, with denominator 10;
   - acquisition annotation: a verified-fail init followed by a verified-pass final.

   CAND follows the same rules.
3. **Q3. Falsifiers.**
   - One numerically verified witness falsifies the claim that departing from the specified W0 is necessary for this target within the declared architecture.
   - Fewer than 8 passes gives REPRODUCIBILITY CRITERION NOT MET.
   - "Not reached within declared search" and "no verified witness found" falsify nothing and certify nothing.
4. **Q4. Simpler explanations.**
   - Fewer trainable parameters: R-FIX-48 matches the trainable count. Per Finding 1 this does not isolate count from width, allocation or optimization effects.
   - Different init or data: paired cores (all ten seeds asserted) and identical, digest-checked streams.
   - Unequal budget: the identical recipe.
   - Evaluation artifacts: the dual evaluator and the non-overlapping rule.
   - Leaky freezing: the Edit 4 checks and the synthetic fixture.
   - Post-hoc choice: excluded (§5).
   - τ informed by prior results: disclosed, and all three components remain decision-bearing.

   **Limitations:**
   - one budget;
   - one frozen matrix per seed (random W0);
   - H ∈ {32, 48} only;
   - no restarts, which limits negative conclusions;
   - numerical, not real-arithmetic, verification.
5. **Q5. Why now.** Consult #18 identifies R-FIX as "the most informative next rival". PR #9 supports a bounded causal contribution of trained `weight_hh` (8/10). Whether that contribution is indispensable is a separate question (Q-NECESSITY NOT_ESTABLISHED). Consult #19: "The most valuable outcome would be a valid compensation witness. It would narrow what must be learned without diminishing what the earlier interventions demonstrated causally."
6. **Q6. On success (witness).** Use the §8.1 Edit 6 wording, plus the acquisition sentence where it applies. The ledger records a scoped counterexample (§11). No C-level change.
7. **Q7. On failure.** Use "TARGET NOT REACHED WITHIN DECLARED SEARCH" or "NO VERIFIED WITNESS FOUND", with counts. No necessity claim and no certificate. Any extension (restarts, LR grid, longer budget, other H) is a separately specified and approved protocol with fresh labels. Appendix D is not activated automatically (§14 ruling 2).
8. **Q8. Resources.**
   - 30 CPU runs × 4000 steps on the PR #7 recipe, comparable to PR #9's 30-run training.
   - Evaluation: 60 checkpoints (init and final) × 256 histories × 2 evaluators, taking seconds.
   - One synthetic-fixture test of a few steps, which is not a study run.
   - No organism model.
9. **Q9. Level.** Organizational: whether training the input weights, biases and readout compensates for a hidden-to-hidden matrix held at W0. Those parameters can still change the recurrent dynamics. Engineering: the freezing mode and the runner. No substrate claim.
10. **Q10. Ceiling.** §8.3: numerically verified existence or reproducibility for the reported W0 and H, target and budget. Never a certificate.
11. **Q11. C-level.** At most a C3-type history-integrating predictive state. Below C4; C5 untouched. No consciousness claim.
12. **Q12. Supplied, acquired, selected.**
    - **Supplied:** the GRU cell, the random W0, the stage one-hot timing scaffold, the readout architecture (H), the loss, the split, the target and τ, and the oracle (evaluation only).
    - **Acquired:** W_ih, the biases and the readout for R-FIX; everything for CAND.
    - **Selected:** nothing. No restarts or selection; H ∈ {32, 48} is fixed in advance.
13. **Q13. Ledger movement.**
    - **Witness:** a scoped counterexample entry per §11 (the Edit 6 wording), with initialization witnesses and acquisition annotations stated separately. Broader Q-NECESSITY remains NOT_ESTABLISHED.
    - **Not reached / no verified witness:** Q-NECESSITY remains NOT_ESTABLISHED, annotated with the label and counts.
    - **UNRESOLVED:** no movement.
    - **All cases:** "Earlier acquisition, transfer and exact-solution results are unchanged. This study can add restricted-class existence evidence and, where the initialization-to-final condition holds, evidence of acquired target attainment. It does not test transfer or add a new causal-organization claim."

## 11. Q-separation and ledger

**Current ledger wording (consult #18, verbatim; not altered by this protocol):**

> "Q-CAUSE, organization level: SUPPORTED, BOUNDED. In W2, continuation-stage joint recurrent reversion met the prespecified joint FO-and-ISO AUC criterion in 8/10 fresh GRU-8 seeds. In each passing seed, excess prefix-function loss exceeded every one of 32 first-order-matched paths and every one of 32 isotropic paths and met the materiality threshold. This supports a causal contribution of the trained hidden-to-hidden parameters under the specified intervention and fixed surrounding computation.
>
> The result meets the replication threshold exactly. Two passing seeds have thin margins against at least one family; each failing seed loses to one sampled ISO path. FO passed in 10/10 seeds and excluded no additional seeds beyond ISO. The claim concerns sampled controls and dose-averaged AUC, not arbitrary perturbations, every dose or the endpoint.
>
> Secondary blocks: criterion not met, r 0/10, z 0/10, n 5/10. The primary effect was not reproduced by any single block at the declared criterion; no localization or interaction mechanism is identified.
>
> Q-LEARN: E1 and transfer replicated 10/10. Q-NECESSITY: NOT_ESTABLISHED, not tested. Q-EXIST: not addressed; the supplied exact solution remains available. No C4, consciousness or organism conclusion."

**Ledger entry on a witness.** §14 ruling 6: "prefer the explicit scoped counterexample wording above over merely 'NOT SUPPORTED.' A witness refutes the specified impossibility claim. Broader necessity remains NOT_ESTABLISHED." The entry is:

- "Q-NECESSITY (restricted class R-FIX-H, W2, GRU-8, declared target):"
- then the Edit 6 witness wording verbatim (§8.1);
- then the acquisition sentence if it applies;
- then the counts block (§7);
- then "Broader Q-NECESSITY: NOT_ESTABLISHED."

| Item | Question | Possible outcomes from this study |
| --- | --- | --- |
| R-FIX-32 / R-FIX-48 vs target | Q-NECESSITY (restricted class, scoped to the reported W0 and H) | WITNESS FOUND (init and/or final, with acquisition annotation), TARGET REACHED REPRODUCIBLY, REPRODUCIBILITY CRITERION NOT MET, TARGET NOT REACHED WITHIN DECLARED SEARCH, NO VERIFIED WITNESS FOUND, UNRESOLVED |
| CAND | unrestricted comparator | same label set |
| Causal contribution of trained W_T (PR #8/#9) | Q-CAUSE | not altered; no new causal-organization claim |
| Acquisition / transfer / exact solution | Q-LEARN / Q-EXIST | "Earlier acquisition, transfer and exact-solution results are unchanged. This study can add restricted-class existence evidence and, where the initialization-to-final condition holds, evidence of acquired target attainment. It does not test transfer or add a new causal-organization claim." |

## 12. Frozen numeric tolerances and values (frozen only when the Specialist freezes protocol and implementation)

| item | value | note |
| --- | --- | --- |
| τ | 0.25 | disclosed as informed by prior results; retained (Finding 4) |
| PD(q*) | 0.0138386222… | recomputed from q* by the frozen code |
| A-FIT thresholds | `World.afit_threshold["TEST"]` (Fractions) | compared in float64, as in `afit_holds` |
| t (T_BOUNDARY_TOL) | 1e-9 | VERIFIED PASS: both T < 1 − t. VERIFIED FAIL: both T > 1 + t. Otherwise BOUNDARY / NUMERICALLY UNRESOLVED |
| Evaluator agreement | abs(x−y) ≤ 1e-12 + 1e-9·max(abs(x), abs(y)) per normalized component | disagreement means integrity failure |
| W0 integrity | byte-equal (sha256) after training and after reload | Edit 4 |
| eps0 / IDENTITY_TOL | 1e-12 / 1e-9 | inherited |
| Reproducibility | ≥ 8/10 final verified passes, denominator 10 | existence needs ≥ 1 verified checkpoint |
| Unresolved bound | > 2 runs invalid or numerically unresolved per arm → reproducibility UNRESOLVED | Edit 3 |
| Budget | 4000 steps, batch 256, cosine 1e-3→1e-4, clip 1.0 over own trainable set, 1 run | identical for all arms |
| Seeds | 400–409; episodes 1400–1409; no replacement | |

## 13. Rulings on draft ambiguities (consult #19, verbatim)

| Item | Ruling |
| --- | --- |
| 1 | Accept counts and the qualified meaning of matching. |
| 2 | Accept arm-specific naming; bare counts must not identify arms. |
| 3 | Accept, with the freezing checks above. |
| 4 | Accept partial pairing; verify every seed. |
| 5 | Accept identical streams and digest checks. |
| 6 | Accept no selection or restarts. This limits negative conclusions; it is not inherently the strongest search. |
| 7 | Accept uniform-grid L_prefix as primary. |
| 8 | Accept each arm's own trained readout; no transfer step. |
| 9 | Amend witness eligibility and boundary handling as above. |
| 10 | Accept: CAND failure cannot erase a restricted-class witness. |
| 11 | Accept the separately committed checkpoint manifest. |
| 12 | Accept no reruns or replacement; use the revised unresolved rules. |

The draft items these refer to were:
1. the meaning of 32/48 and of matching;
2. the naming hazard;
3. the freezing mode;
4. paired inits;
5. episode streams;
6. no selection or restarts;
7. the L_prefix definition;
8. each arm's own readout;
9. the witness definition;
10. CAND failure;
11. the two-stage runner;
12. invalid runs.

They are applied in §§1–9 above.

### 13.1 Residual ambiguities resolved in this FINAL (for the Specialist to confirm at freeze)

- **A1. Shared init witness.** The CAND and R-FIX-32 inits are identical. A verified-pass init in either is counted once, as an H = 32 init witness, and noted under both arms. The R-FIX-48 init is a separate (H = 48) init witness.
- **A2. Init evaluation timing.** All init evaluations run in Stage 2, after the Stage-1 seal. Inits are never evaluated before training, so no outcome information precedes training.
- **A3. Synthetic fixture.** It uses a non-study seed and synthetic inputs, runs a few steps, includes a negative case, and has no evidential role. It is treated as implementation testing within the frozen implementation, not as an "additional training run" under the scope exclusions. If the Specialist or Aidan reads it otherwise, it needs explicit mention in the approval.
- **A4. Gradient-None check frequency.** The default is every optimizer step, because it is cheap. Edit 4 requires it at least "after backward".
- **A5. Displaced fragments (Edit 7).** The only displaced material identified in draft v1 was the appendix order: Appendix B was placed after D. The appendices are restored to A, B, C, D order. No other text was found out of place; if Astra meant specific fragments, they should be named.
- **A6. Reproducibility "numerically unresolved" count** includes BOUNDARY finals only. Init boundary results affect only the acquisition annotation.

## 14. Rulings on draft open questions (consult #19, verbatim)

1. **Binding component:** keep tau. Report all components and their binding frequencies; do not call the new study effectively XOR-only before observing R-FIX.
2. **Budget:** the primary search is worthwhile because success is informative. Failure is deliberately limited. Do not activate Appendix D automatically. Leave it as a separately specified and approved extension, with exact selection and refit costs counted.
3. **Clipping:** clip each arm's actual trainable parameter set. Do not compute artificial gradients through frozen parameters to imitate CAND's clipping.
4. **Wider-head initialization:** retain partial pairing. An independent head seed would change the design without resolving allocation and width differences.
5. **Witness margin:** 1e-9 is acceptable with the repaired dual-evaluator rule. Float32 evaluation may be descriptive; it need not gate a claim explicitly defined in float64. Dual evaluation is a numerical cross-check, not a validated error bound for real arithmetic.
6. **Ledger:** prefer the explicit scoped counterexample wording above over merely "NOT SUPPORTED." A witness refutes the specified impossibility claim. Broader necessity remains NOT_ESTABLISHED.
7. **Low rank:** if later studied, use the stacked 24x8 update as the primary definition. It has at most `32*k` factor parameters before accounting for factorization redundancy. It tests restricted recurrent-matrix learning, not compensation with no matrix learning.
8. **Finite-class certificate:** worth a feasibility analysis, not yet an exhaustive-search commitment. A later certificate must cover the entire declared finite domain, preserve a verified unrestricted success comparator, and state that its conclusion depends on the chosen bounds and precision. A coarse grid that excludes useful solutions may certify a narrow fact with little bearing on the present continuous model.

---

## Appendix A. R-TUNE (OPTIONAL; EXCLUDED from this study and from the approval scope)

- Form: weight_hh is a fixed, non-learned transform of W0 (for example g·W0), plus an update-gate-bias initialization b, chosen on a held-out subset.
- Consult #18 verbatim: "R-TUNE is admissible, but if update-gate biases subsequently train freely, `b` is an initialization/search choice, not a lasting class restriction. Charge its selection compute."
- If ever run, it needs its own protocol, seeds, labels and approval, with all selection runs counted.
- It does not enter any §7 label.

## Appendix B. Feasibility checks already run (scratch, read-only, no training)

Location: `/workspace/scratch/frozen_comp/`. Scripts import the frozen PR #9 code read-only from a scratch clone (torch 2.14.1+cpu).

| file | sha256 | contents |
| --- | --- | --- |
| `feasibility.py` | be069574fe7c5a91d55a98c639c84b901b989659e176bee259d30c1bdf9ca622 | parameter counts (H = 32/48/70), init pairing (seeds 400 and 409), T of existing checkpoints |
| `feasibility.log` | 166fb16ab16cb3fa37881b84fe26c2000804a4b654d155c7b88daa50afb1ebc5 | output of the above |
| `T_existing.json` | 7fd2c9c6833cabc75dbabde10561125ab51508e445d6de2297175a5ad19b1dbf | T values for the existing checkpoints |
| `crosscheck.py` / `crosscheck.log` | 874a0d95cb6352affbc5aebfd10dfa93788e870c5c20404b59d288839c3831b0 / 7f4140e6de078fe26c63f3f3e6f163b8163b4ebbbc1d3ea0d09ea81f5c51b631 | independent NumPy evaluator vs the frozen `evaluate_arm`/`l_prefix` |
| `pairing_all.py` / `pairing_all.log` | 48e0db8bdf6ea1639a70038b845da849ee31b3b41ec08927fbf559a9b80eb0b7 / 981a03946834ffe9d7107b788d6c3db12481ad11461852b712b7cc6ff46c63e1 | init construction only, all ten seeds 400–409 |

- **Crosscheck result:** agreement ≤ 4.4e-16 in predictions; L_prefix and E identical to 10 significant figures (seeds 100 and 305, CAND and F-INIT).
- **Pairing result:** for every seed 400–409, the GRU core is equal between H = 32 and H = 48, the CAND and R-FIX-32 inits are fully equal, and fc1.weight rows 0–31 are equal. No model was evaluated or trained.

**T(θ) of existing checkpoints (τ = 0.25):**

| group | arm | T range | T ≤ 1 | L/PD | E_tot/thr | E_XOR/thr |
| --- | --- | --- | --- | --- | --- | --- |
| PR7 100–109 | cand_final | 0.196–0.732 | 10/10 | 0.034–0.110 | 0.057–0.219 | 0.196–0.732 |
| PR7 | f_trained | 0.194–0.709 | 10/10 | 0.040–0.111 | 0.076–0.233 | 0.194–0.709 |
| PR7 | f_init | 11.55–16.86 | 0/10 | 0.961–1.144 | 1.81–3.30 | 11.55–16.86 |
| PR7 | cand_init | 16.47–20.54 | 0/10 | 0.999–1.002 | 8.46–9.41 | 16.47–20.54 |
| PR8 200–209 | cand_final | 0.234–0.599 | 10/10 | 0.038–0.101 | 0.065–0.191 | 0.234–0.599 |
| PR8 | f_trained | 0.219–0.600 | 10/10 | 0.040–0.099 | 0.063–0.178 | 0.219–0.600 |
| PR8 | f_init | 12.99–17.36 | 0/10 | 0.962–1.103 | 2.04–3.24 | 12.99–17.36 |
| PR8 | cand_init | 16.75–20.05 | 0/10 | 0.999–1.002 | 8.35–9.40 | 16.75–20.05 |
| PR9 300–309 | cand_final | 0.207–0.572 | 10/10 | 0.038–0.053 | 0.071–0.104 | 0.207–0.572 |
| PR9 | f_trained | 0.211–0.506 | 10/10 | 0.041–0.056 | 0.075–0.108 | 0.211–0.506 |
| PR9 | f_init | 12.13–15.25 | 0/10 | 0.992–1.129 | 1.98–3.42 | 12.13–15.25 |
| PR9 | cand_init | 16.51–19.11 | 0/10 | 0.998–1.002 | 8.16–9.63 | 16.51–19.11 |

**Binding frequencies:**
- The XOR term binds in all 30 existing CAND checkpoints.
- The one exception overall is an F-TRAINED checkpoint (PR8, one seed), where L_prefix binds.

**Historical F-INIT range across all 30 checkpoints:** approximately **11.55–17.36**. Minimum 11.549 (PR7); maximum 17.356 (PR8).

**Reading:**
- The unrestricted target is met with margin in all 30 existing CAND checkpoints (maximum T 0.73).
- A fully frozen W0 core with a trained readout (F-INIT) misses by an order of magnitude.
- **No existing checkpoint is an R-FIX model.** F-INIT also freezes W_ih and the biases, so nothing here predicts R-FIX.
- Which constraint limits R-FIX is unknown (Finding 4).

## Appendix C. Low-rank recurrent updates (OPTIONAL; EXCLUDED from this study and from the approval scope)

- Form: W_hh = W0 + U Vᵀ of rank k.
- §14 ruling 7: if later studied, the **stacked 24×8 update is the primary definition**. It has at most 32·k factor parameters before accounting for factorization redundancy.
- Consult #18 verbatim: "Low-rank recurrent updates are a valid separate question about restricted recurrent learning; specify whether rank applies to the stacked 24x8 matrix or separately to each block. They should not complicate the primary no-recurrent-matrix-learning comparison."
- It tests restricted recurrent-matrix learning, not compensation with no matrix learning.

## Appendix D. Extended R-FIX search (OPTIONAL; EXCLUDED from this study and from the approval scope)

- A pre-declared grid with selection on a held-out subset and both TEST and the held-out subset rejected from training. For example, 3 LRs × 2 restarts per seed per R-FIX arm, which is 120 extra runs.
- It would carry its own labels ("R-FIX-H(EXT)").
- §14 ruling 2: "Do not activate Appendix D automatically. Leave it as a separately specified and approved extension, with exact selection and refit costs counted."
