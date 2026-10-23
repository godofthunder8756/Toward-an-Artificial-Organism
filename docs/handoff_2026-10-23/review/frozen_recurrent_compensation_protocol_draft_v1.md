# Frozen recurrent matrices with learned compensation: protocol (DRAFT v1)

**Status:** DRAFT for Astra review. Nothing in this document is frozen. No training has been run for it.
**Training approval:** PENDING (§0.2). The ACI Research Specialist is requesting it.
**Source rulings:** Astra consult #18, §§6–8 and the closing recommendation, quoted verbatim where marked.
**Scope:** W2 world, GRU-8 family only. Below C4. No new architecture family, no protected controller or register, no organism work. No consciousness claim.

---

## 0. Framing (fixed)

This study is a **search for compensation and counterexamples to necessity. It is not a necessity certificate.**

The question it asks is narrow. Suppose every hidden-to-hidden matrix `weight_hh` is held at its random initialization W0 at all eight updates, and the input weights, both biases and the readout are trained instead. Can that remaining computation still reach the declared target T(θ) ≤ 1?

Consult #18, verbatim:

> "Compensation would not negate the existing causal result: parameters can contribute causally in one trained implementation without being indispensable to another."

> "One verified witness refutes absolute impossibility for that particular restricted class and target. An 8/10 rule establishes reproducibility, not the logical minimum needed for a counterexample."

> "Failure means only 'not reached within declared search.'"

A failure is not a certificate. The certificate Astra described is a validated lower bound inf T > 1 over the entire declared restricted domain, or a complete search of an explicitly finite class. This protocol does not attempt one (§8.3).

## 0.1 Inherited unchanged from PR #7 / PR #8 / PR #9

- The W2 world.
- The 256 histories h = p + 16u.
- The TEST and VAL split predicates (`is_test_history` and `is_val_history`).
- The oracle q*, PD(q*) = 0.0138386222 (recomputed as 0.013838622233977797, Appendix B).
- The A-FIT thresholds, frozen as `Fraction`s in `World.afit_threshold`:
  - TEST total = E_cur_TEST/4 = 0.0203873 (float);
  - TEST XOR = E_PROD_TEST/4 = 0.00228962 (float).
- `component_excess`, `afit_holds`, and `l_prefix` (graded_reversion_outcomes.py, uniform mean over the 16×16 grid, no /3).
- CoreGRU: `nn.GRU(9, 8)` with zero initial state. The input is the reading (±1) plus an 8-way stage one-hot. The readout is `8 → H → 3` (tanh hidden, sigmoid output).
- The PR #7 optimization recipe:
  - Adam (β from spec, eps from spec, weight decay 0);
  - STEPS = 4000, BATCH = 256;
  - cosine LR from 1e-3 to 1e-4;
  - grad-norm clip 1.0 over the trainable parameter list;
  - TEST histories rejected from training (VAL not rejected; see §5);
  - squared-error loss on sampled labels;
  - `set_num_threads(1)` and `use_deterministic_algorithms(True)`;
  - a per-run episode generator seeded 1000+s.
- eps0 = 1e-12; IDENTITY_TOL = 1e-9; the checkpoint format is canonical JSON/base64 float32 with sha256.

## 0.2 Approval record (PENDING)

| item | value |
| --- | --- |
| What needs approval | Training phase: **30 CPU training runs = 3 arms (CAND, R-FIX-32, R-FIX-48) × 10 seeds (400–409)**, plus evaluation-only scoring. |
| Count confirmation | 3 × 10 = 30. There is no F-TRAINED or F-INIT arm here, no restarts, and no LR grid in the primary analysis. Optional appendices A, C and D add runs and are **not** covered by this request. |
| Required | Aidan's **explicit** approval **AND** Astra clearance of the final protocol text. |
| Status | **PENDING.** Requested by the ACI Research Specialist. |
| Carry-over | **None.** Prior approvals do not carry over. This includes the PR #9 Phase B approval (1:05 AM ET, widget t23s2). |
| Before approval | Only evaluation of existing checkpoints and code reading (Appendix B). No training, no new seeds drawn into models beyond init-identity checks, nothing frozen. |

Consult #18, verbatim: "These 30 training runs require Aidan's explicit approval."

---

## 1. Arms (parameter accounting verified from code)

"32" and "48" are the **readout hidden width H** of the `8 → H → 3` head (`readout_fc1: 8→H`, `readout_fc2: H→3`). The readout has 12H + 3 parameters. The GRU core is fixed at 456 parameters:
- `weight_ih_l0` 216;
- `weight_hh_l0` 192;
- `bias_ih_l0` 24;
- `bias_hh_l0` 24.

These counts were verified by instantiating `CoreGRU(H)` from the frozen code (Appendix B, `feasibility.log`).

| arm | head H | frozen | trainable | # trainable | # stored total |
| --- | --- | --- | --- | --- | --- |
| **CAND** | 32 | nothing | everything | **843** (456 + 387) | 843 |
| **R-FIX-32** | 32 | `weight_hh_l0` = W0 (192) | W_ih, b_ih, b_hh, readout | **651** (216 + 48 + 387) | 843 |
| **R-FIX-48** | 48 | `weight_hh_l0` = W0 (192) | W_ih, b_ih, b_hh, readout | **843** (216 + 48 + 579) | 1035 |
| (R-FIX-70, not run) | 70 | `weight_hh_l0` | as above | 1107 (264 + 843) | 1299 |

**What "parameter-matched" means.** R-FIX-48 matches CAND in **number of trainable parameters**: 843 = 843. It is not matched in stored parameter count (1035 vs 843), because it also carries the 192 frozen W0 entries. It is not matched in where the parameters sit either: CAND has 456 recurrent and 387 readout, R-FIX-48 has 264 recurrent and 579 readout. R-FIX-32 is matched to CAND in **architecture and initialization** (identical model, identical init), but has 192 fewer trainable parameters.

The two R-FIX arms therefore separate two explanations of any shortfall: "fewer trainable parameters" versus "no recurrent-matrix learning".

**Discrepancies flagged.**
1. The 70-unit head gives 1107 trainable parameters, not 843 (Astra #18 correction, confirmed from code).
2. **Naming hazard:** "843" previously labelled the 70-head readout-only rival (readout 843). Here "843" means CAND or R-FIX-48 *trainable* totals. Reports must always write the arm name, never the bare number.
3. The existing `train_arm(freeze_recurrent=True)` freezes **all four** recurrent tensors. That is the F-INIT/F-TRAINED semantics, and it is **not** R-FIX. R-FIX needs a new freezing mode that sets `requires_grad=False` on `rnn.weight_hh_l0` only. This is a small harness change to be written and frozen with the protocol (§4). It is not an architecture change.
4. **F-INIT ≠ R-FIX.** F-INIT freezes the whole W0 core (W_ih, W_hh, both biases) and trains a fresh readout. R-FIX additionally trains W_ih and both biases. The historical F-INIT result (T between 11.5 and 16.9, Appendix B) says nothing about R-FIX.

## 2. Seeds, pairing and streams

| item | value |
| --- | --- |
| Seeds | **400–409** (fresh; disjoint from 100–109, 200–209, 300–309) |
| Init, CAND and R-FIX-32 | `build_initialized(s, 32)`. Same seed, same construction, so the **whole init is identical** (verified for 400 and 409). |
| Init, R-FIX-48 | `build_initialized(s, 48)`. The four GRU tensors are identical to CAND's (verified for s = 400 and 409), so **W0 is the same matrix in all three arms**. `readout_fc1.weight` rows 0–31 equal CAND's. `fc1.bias`, `fc2.weight` and `fc2.bias` differ in shape or RNG position. `fc2` also has a different default bound (1/√48 vs 1/√32, standard PyTorch init). This is the "where shapes permit" pairing. |
| Episode stream | generator `1000 + s` for all three arms of seed s (seeds 1400–1409), with identical rejection (TEST only). The streams are therefore **identical across arms**, batch for batch. |
| Budget | identical for all arms: 4000 Adam steps, batch 256, the same LR schedule and clip. One run per arm and seed. **No restarts.** |
| Draw order | All 30 inits are drawn and hashed (Stage 0) before any training. |

## 3. Target (fixed)

T(θ) = max( L_prefix(θ) / (τ·PD(q*)), E_total_TEST(θ) / thr_total_TEST, E_XOR_TEST(θ) / thr_XOR_TEST ).

τ = 0.25. **Target reached ⇔ T(θ) ≤ 1**, i.e. L_prefix ≤ 0.25·PD(q*) AND both TEST A-FIT inequalities hold (consult #18 §7).

**τ disclosure (mandatory wording):**

> "tau = 0.25 was chosen after prior results were known. Across the 30 existing CAND checkpoints (seeds 100–109, 200–209, 300–309), L_prefix/PD ranged 0.034–0.110, i.e. L_prefix/(0.25·PD) ≤ 0.44, and the XOR A-FIT term was the binding component of T in all 30. τ = 0.25 was therefore informed by, and is not binding for, the unrestricted reference."

- θ is the **final-step** parameters (step 4000).
- L_prefix is uniform over all 256 histories, including TEST, as evaluation. E is TEST-weighted (`component_excess`). All are computed in float64 from the float32 checkpoint, using the frozen evaluator.
- Validation selection: **none** (§5).

## 4. Harness additions (to be written and frozen with the protocol; engineering only)

1. **`train_arm_rfix(model, episode_seed)`.** This is PR #7 `train_arm` with one difference: `rnn.weight_hh_l0.requires_grad_(False)`, and every other tensor `True`.
   - The Adam parameter list and `clip_grad_norm_` cover exactly the trainable tensors.
   - Clipping therefore acts on a different parameter set than CAND's. This is disclosed and inherent to the arm.
   - Everything else is identical: the generator, `sample_batch`, the loss, the LR schedule and the failure checks.
2. **W0 integrity.** After training, `weight_hh_l0` must be **byte-equal** to the Stage-0 W0 (sha256 of the tensor bytes). If it is not equal, the run is invalid.
3. **Gradient check.** At step 0 of one seed, `weight_hh_l0.grad` must be `None`. Recorded.
4. **No evaluation of trained models in Stage 1.** Stage 1 logs the training loss only. Init-only evaluation is allowed, for the eligibility check of §6.

## 5. Validation selection, restarts, reporting (frozen)

- **Validation selection: none.** No early stopping, no checkpoint choice, no hyperparameter choice. VAL histories are not rejected from training, as for CAND in PR #7. VAL is reported descriptively only.
- **Restarts: none.** Exactly one run per arm and seed. A diverged or non-finite run is not re-run.
- **Hyperparameters:** the PR #7 recipe unchanged for all arms. No R-FIX-specific tuning in the primary analysis. Any extended budget is Appendix D, which needs separate approval and uses separate labels.
- **Reporting:** every seed and arm is reported, including invalid ones. For each one:
  - all three T components and T;
  - E_total and E_XOR for TEST and TRAIN;
  - L_prefix, B_prefix, C_prefix;
  - the final training loss;
  - the paired difference T(R-FIX) − T(CAND).

  The best and median T per arm are descriptive.

## 6. Validity and eligibility (per arm and seed)

- **Invalid:** any of the following:
  - training integrity failure (non-finite loss, gradients or weights, as in PR #7);
  - checkpoint round-trip mismatch;
  - `outputs_valid` false;
  - identity checks failing at IDENTITY_TOL;
  - the R-FIX W0 byte-equality failing;
  - a Stage-2 checkpoint sha not matching the sealed manifest.

  An invalid run supplies no witness and counts as a non-pass in the n/10 denominator.
- **Eligibility (A-LEARN analogue):** T(init) > 1 for the arm's own init. Historically CAND init T was between 16.5 and 20.5 (Appendix B), so this is expected to hold. If T(init) ≤ 1, the seed is ineligible for that arm and cannot supply a witness.
- **Unevaluable bound:** if more than 2 seeds are invalid or ineligible in an arm, that arm's reproducibility label is UNRESOLVED. The witness label (§7) is still determined by the valid, eligible seeds.

## 7. Labels (per arm; decided only from Stage 2)

A **verified witness** is a valid, eligible run of an R-FIX arm whose final checkpoint satisfies all of:
- T ≤ 1 − T_BOUNDARY_TOL, computed by the frozen evaluator;
- the same result recomputed by an independent float64 NumPy forward pass, agreeing on each T component to ≤ 1e-9 relative;
- the W0 byte-equality check;
- a sha that matches the sealed Stage-1 manifest.

If |T − 1| ≤ T_BOUNDARY_TOL, the run is **BOUNDARY (numerically indeterminate)**. It is not a witness and not a pass.

Labels, in order:
1. **CAND positive control.** "CAND TARGET REPRODUCED" if T ≤ 1 in ≥ 8/10 seeds. Otherwise "CAND TARGET NOT REPRODUCED". This is an unrestricted witness for the target in this cohort. The R-FIX labels below are reported either way, but if CAND is not reproduced the comparison is labelled **UNRESOLVED (positive control not reproduced)**. A witness found in an R-FIX arm still stands as a witness for that class and target.
2. **Per R-FIX arm (R-FIX-32, R-FIX-48), separately:**
   - **"R-FIX-H: WITNESS FOUND (n/10)"** if n ≥ 1 verified witnesses. One is sufficient for the counterexample statement (§8.1).
   - **"R-FIX-H: TARGET REACHED REPRODUCIBLY (n/10)"**, an *additional* label, if n ≥ 8 with the denominator of 10 retained.
   - **"R-FIX-H: TARGET NOT REACHED WITHIN DECLARED SEARCH (0/10)"** if there are no verified witnesses.
   - **UNRESOLVED (insufficient evaluable seeds)** for the reproducibility label only, under §6.
3. **No pooled R-FIX label** and no comparison test between arms. Differences between R-FIX-32 and R-FIX-48 are descriptive.

There is no multiplicity correction for the existence statement. It is a verified-instance claim, not a statistical inference. The disclosure that 20 R-FIX runs were searched is mandatory.

## 8. Claims (fixed in advance)

### 8.1 Allowed wording (verbatim templates)

- **Witness found:** "In W2, with GRU-8 hidden-to-hidden matrices frozen at their random initialization W0 at all eight updates, training of input weights, both biases and an 8→H→3 readout (H = __) reached the declared target T ≤ 1 (L_prefix ≤ 0.25·PD(q*) and both TEST A-FIT inequalities) in n/10 fresh seeds under the PR #7 budget. One verified witness refutes absolute impossibility for that particular restricted class and target. Compensation does not negate the existing causal result: parameters can contribute causally in one trained implementation without being indispensable to another. Q-NECESSITY of recurrent-matrix learning for this target is not supported in this class; Q-CAUSE is unchanged."
- **Reproducible** (adds): "The target was reached in at least 8/10 seeds, establishing reproducibility within the declared search, not a logical minimum."
- **Not reached:** "R-FIX-H did not reach the target within the declared search (one run per seed, 4000 steps, PR #7 recipe, no restarts). Failure means only 'not reached within declared search.' This is not a necessity certificate and does not establish that departing from W0 is necessary."
- **Mixed (CAND reproduced, R-FIX-32 not reached, R-FIX-48 witness or the reverse):** report each arm with its own label. Nothing is inferred about mechanism.

### 8.2 Forbidden wording

- "recurrent learning is necessary" / "necessity established" / "certificate" / "impossible without recurrent training";
- "the PR #8/#9 causal result is refuted or weakened by compensation";
- "R-FIX shows the recurrent matrix is irrelevant / not causal";
- any generalization beyond W2, GRU-8, W0-random-init, this target and this budget;
- any C4, C5, consciousness, agency or organism language.

### 8.3 Claim ceiling (consult #18, verbatim)

> "A certificate must establish `inf T(theta) > 1` throughout the restricted domain, alongside an unrestricted witness with `T <= 1`. The domain must specify the frozen matrix, remaining weight ranges or precision, readout size and supplied timing information."

> "That would establish necessity of **departing from that specified frozen matrix within that domain**. It would not establish universal necessity of recurrent training. A simple prefix-separation argument should not be presumed available: trainable input weights, gates and readout may retain substantial representational flexibility."

The ceiling of this study is the existence (or reproducibility) of a witness for the R-FIX class and target, or "not reached within declared search". It is never a certificate.

## 9. Two-stage sealed-manifest runner (consult #18 §6 applied)

Consult #18 verbatim: "For future studies, use a two-stage runner: write and seal the transformed-path manifest, then evaluate curves from that manifest. A separate commit or timestamped artifact improves provenance but is not a retroactive requirement here."

There are no transformed paths in this study. The analogue is a sealed **checkpoint manifest**:

- **Stage 0 (pre-training):** draw all 30 inits in seed order. Write `manifest_stage0.json` containing:
  - per arm and seed, the init checkpoint sha256 and the W0 tensor sha256 (equal across the three arms of a seed);
  - an episode-stream digest per seed (sha256 of all 4000 × 256 accepted bit and label arrays, regenerated from generator 1000+s without training);
  - the code-tree sha and the frozen protocol sha.

  Seal it with a commit or timestamped artifact.
- **Stage 1 (training only):** train the 30 runs and store the final checkpoints. Write `manifest_stage1.json` containing:
  - the checkpoint sha256 values;
  - training integrity flags, steps completed and final training loss;
  - the W0 byte-equality result;
  - the episode digests re-derived during training, which must equal Stage 0.

  No TEST, VAL or target evaluation of trained models. **Seal it with a separate commit** (required here, prospectively), before Stage 2 code runs.
- **Stage 2 (evaluation from manifest):** load only checkpoints whose sha matches Stage 1. Compute T and its components with the frozen evaluator and the independent NumPy re-evaluation. Assign labels mechanically.
- Any mismatch between stages makes that run invalid. There is no re-training.

## 10. Thirteen admission answers

1. **Q1. Question.** Q-NECESSITY, restricted-class form, bounded. With `weight_hh` frozen at W0, can input weights, both biases and the readout compensate enough to reach T ≤ 1? It is a search for counterexamples, not a certificate.
2. **Q2. Hypothesis and criterion.** There is no directional hypothesis; compensation is plausible but not predicted. The criteria are per arm:
   - witness: ≥ 1 verified run with T ≤ 1;
   - reproducibility: ≥ 8/10, with the denominator of 10;
   - positive control: CAND ≥ 8/10.
3. **Q3. Falsifiers.**
   - The impossibility of compensation in that class is falsified by one verified witness.
   - The "reproducible compensation" label is not reached at fewer than 8/10.
   - "Not reached within declared search" falsifies nothing and certifies nothing.
4. **Q4. Simpler explanations.**
   - Fewer trainable parameters: addressed by R-FIX-48 (trainable count matched).
   - Different init or data: paired init and identical episode streams.
   - Unequal budget: the identical recipe.
   - Evaluation artifacts: the dual evaluator and sealed manifests.
   - Leaky freezing: W0 byte-equality.
   - Post-hoc checkpoint or hyperparameter choice: excluded (§5).
   - τ tuned to the result: disclosed. τ is non-binding for CAND, and XOR A-FIT binds.

   **Limitations:**
   - one budget;
   - one frozen matrix per seed (random W0);
   - only H ∈ {32, 48};
   - no restarts, so under-optimization cannot be excluded on failure;
   - the gradient-clip set differs by construction.
5. **Q5. Why now.** Consult #18 identifies R-FIX as "the most informative next rival". PR #9 supports a bounded causal contribution of trained `weight_hh` (8/10). Whether that contribution is indispensable is a separate question (Q-NECESSITY NOT_ESTABLISHED).
6. **Q6. On success (witness).** Use the §8.1 wording. The ledger records a restricted-class counterexample (§11). Q-CAUSE is unchanged. No C-level change.
7. **Q7. On failure.** "Not reached within declared search." No necessity claim, and no certificate. Any extension (restarts, LR grid, longer budget, other H) is a new or appendix protocol, needing separate approval and fresh labels.
8. **Q8. Resources.**
   - 30 CPU runs × 4000 steps with the PR #7 recipe. That is roughly the PR #9 Phase B training cost, since PR #9 had the same 30-run count.
   - Evaluation: 30 checkpoints × 256 histories × 2 evaluators, taking seconds.
   - No organism model.
9. **Q9. Level.**
   - Organizational: whether the remaining computation can compensate for an untrained recurrent matrix.
   - Engineering: the freezing mode and the runner.
   - No substrate claim.
10. **Q10. Ceiling.** §8.3. Witness existence or reproducibility for one class, target and budget, never a certificate.
11. **Q11. C-level.** C3-type history-integrating predictive state at most. Below C4. C5 is untouched. No consciousness claim.
12. **Q12. Supplied, acquired and selected.**
    - **Supplied:** the GRU cell, the random W0, the stage one-hot timing scaffold, the readout architecture (H), the loss, the split, the target and τ, and the oracle (evaluation only).
    - **Acquired:** W_ih, the biases and the readout (R-FIX); everything (CAND).
    - **Selected:** nothing. There are no restarts and no selection. H ∈ {32, 48} is fixed in advance.
13. **Q13. Ledger movement.**
    - **Witness:** a new restricted-class entry, "R-FIX-H counterexample found (n/10)". Q-NECESSITY for this class and target is **NOT SUPPORTED** (impossibility refuted for that class and target). The overall Q-NECESSITY status stays NOT_ESTABLISHED for other classes.
    - **Not reached:** Q-NECESSITY stays NOT_ESTABLISHED, annotated "R-FIX-H not reached within declared search".
    - **UNRESOLVED:** no movement.
    - Q-CAUSE, Q-LEARN and Q-EXIST are unchanged in every case.

## 11. Q-separation and ledger

**Current ledger wording (consult #18, verbatim; unchanged by this protocol):**

> "Q-CAUSE, organization level: SUPPORTED, BOUNDED. In W2, continuation-stage joint recurrent reversion met the prespecified joint FO-and-ISO AUC criterion in 8/10 fresh GRU-8 seeds. In each passing seed, excess prefix-function loss exceeded every one of 32 first-order-matched paths and every one of 32 isotropic paths and met the materiality threshold. This supports a causal contribution of the trained hidden-to-hidden parameters under the specified intervention and fixed surrounding computation.
>
> The result meets the replication threshold exactly. Two passing seeds have thin margins against at least one family; each failing seed loses to one sampled ISO path. FO passed in 10/10 seeds and excluded no additional seeds beyond ISO. The claim concerns sampled controls and dose-averaged AUC, not arbitrary perturbations, every dose or the endpoint.
>
> Secondary blocks: criterion not met, r 0/10, z 0/10, n 5/10. The primary effect was not reproduced by any single block at the declared criterion; no localization or interaction mechanism is identified.
>
> Q-LEARN: E1 and transfer replicated 10/10. Q-NECESSITY: NOT_ESTABLISHED, not tested. Q-EXIST: not addressed; the supplied exact solution remains available. No C4, consciousness or organism conclusion."

| Item | Question | Possible outcomes from this study |
| --- | --- | --- |
| R-FIX-32 / R-FIX-48 vs target | Q-NECESSITY (restricted class) | witness (n/10), reproducible, not reached within declared search, UNRESOLVED |
| CAND | positive control (unrestricted witness) | reproduced / not reproduced |
| Causal contribution of trained W_T (PR #8/#9) | Q-CAUSE | **unchanged** in all outcomes |
| Acquisition / transfer | Q-LEARN | not addressed (CAND A-FIT is the positive control only) |
| Exact solution | Q-EXIST | not addressed |

## 12. Frozen numeric tolerances and values (proposed; frozen only on approval)

| item | value | note |
| --- | --- | --- |
| τ | 0.25 | disclosed as informed by prior results |
| PD(q*) | 0.0138386222… | recomputed from q* by the frozen code |
| A-FIT thresholds | `World.afit_threshold["TEST"]` (Fractions) | compared in float64, as in `afit_holds` |
| T_BOUNDARY_TOL | 1e-9 (absolute on T) | \|T − 1\| ≤ 1e-9 means BOUNDARY, not a witness |
| Dual-evaluator agreement | ≤ 1e-9 relative per T component | observed agreement on existing checkpoints ≤ 4.4e-16 in predictions |
| W0 integrity | byte-equal (sha256) | any difference makes the run invalid |
| eps0 / IDENTITY_TOL | 1e-12 / 1e-9 | inherited |
| Reproducibility | ≥ 8/10, denominator 10 | witness needs ≥ 1 |
| Unevaluable bound | > 2 invalid or ineligible per arm → UNRESOLVED (reproducibility only) | |
| Budget | 4000 steps, batch 256, cosine 1e-3→1e-4, clip 1.0, 1 run | identical for all arms |
| Seeds | 400–409; episodes 1400–1409 | |

## 13. Ambiguities resolved in this draft (for Astra to confirm)

1. **"32/48"** means the readout hidden width H. "Parameter-matched" means *trainable-count* matched (843 = 843), not stored-total matched (1035) and not matched in composition.
2. **Naming hazard:** the bare number "843" is banned in reports (§1).
3. **Freezing mode:** the existing `freeze_recurrent=True` is F-INIT semantics. R-FIX needs a W_hh-only freeze (§4). It is a new harness function, not a new architecture.
4. **Paired inits:** CAND and R-FIX-32 share the full init. R-FIX-48 shares W0 and the full GRU core, plus fc1.weight rows 0–31. Its other readout tensors differ (§2).
5. **Episode streams:** the same generator seed 1000+s for all arms, and TEST-only rejection, as for PR #7 CAND.
6. **Validation selection and restarts:** none. One final-step checkpoint per run. This is the most conservative reading of "freeze validation selection, restarts". It also means a failure is weak evidence (§7, Q4).
7. **L_prefix definition:** the `l_prefix` of graded_reversion_outcomes.py, uniform over all 256 histories (the definition that gives PD = 0.0138386). The TEST-only and probability-weighted variants are not used.
8. **Target evaluated on each arm's own trained readout.** There is no fresh-readout transfer step; that belongs to Q-LEARN and is out of scope.
9. **A witness** needs the dual evaluator, byte-equal W0, the sealed sha and a boundary margin. One witness suffices for the existence statement, and 8/10 is reported separately as reproducibility (consult #18 §7).
10. **CAND failing** its positive control does not void an R-FIX witness. It only makes the comparison UNRESOLVED.
11. **The two-stage runner** applies to checkpoints (there are no transformed paths). The Stage-1 manifest must be a separate commit, a prospective requirement.
12. **Invalid or diverged runs** count as non-passes and are not re-run.

## 14. Open questions for Astra

1. **Binding component.** In all 30 existing CAND checkpoints, the binding term of T is E_XOR_TEST/thr_XOR (0.20–0.73), and L_prefix/(0.25·PD) ≤ 0.44. The study therefore effectively tests the XOR A-FIT clause. Is that acceptable, or should τ be tightened prospectively? Note that any tightening is also informed by prior results.
2. **Budget adequacy.** With one run per seed and no LR or restart search, is "not reached within declared search" informative enough? Or should Appendix D (a declared R-FIX restart or LR grid with VAL selection, needing separate approval and separate labels) be pre-registered now as a second stage that runs only if the primary finds no witness?
3. **Clip set.** Should R-FIX clip over its own trainable set (as drafted), or should there be any attempt to match CAND's clip behaviour? The draft's view is that its own set is the natural one.
4. **R-FIX-48 readout init.** Is partial pairing acceptable (shared fc1.weight rows 0–31, a different fc2 bound)? The alternative is to initialize the R-FIX-48 readout from an independent seed for symmetry.
5. **Witness margin.** Is T_BOUNDARY_TOL = 1e-9 on T adequate? Or should a witness also be required to be robust in float32 (native) evaluation as well as float64?
6. **Ledger label.** Is "Q-NECESSITY NOT SUPPORTED for the R-FIX class and this target", with the overall status staying NOT_ESTABLISHED, the right ledger form on a witness?
7. **Low-rank appendix.** If Appendix C is ever run, should rank apply to the stacked 24×8 update or per block? The draft default is the stacked matrix.
8. **Certificate path.** Is a finite-class certificate (for example, quantized W_ih, biases and readout over a bounded grid) worth specifying for any later study? This draft does not attempt one.

---

## Appendix A. R-TUNE (OPTIONAL; excluded from the primary analysis; separate approval)

- Form: the weight_hh is a fixed, non-learned transform of W0, such as g·W0 plus an update-gate-bias initialization b, chosen on VAL.
- Consult #18 verbatim: "R-TUNE is admissible, but if update-gate biases subsequently train freely, `b` is an initialization/search choice, not a lasting class restriction. Charge its selection compute."
- If run, it has its own seeds, its own labels, all selection runs counted and reported, and TEST+VAL rejection for selection.
- It does not enter any §7 label.

## Appendix C. Low-rank recurrent updates (OPTIONAL; excluded; separate approval)

- Form: W_hh = W0 + U Vᵀ with rank k.
- Consult #18 verbatim: "Low-rank recurrent updates are a valid separate question about restricted recurrent learning; specify whether rank applies to the stacked 24x8 matrix or separately to each block. They should not complicate the primary no-recurrent-matrix-learning comparison."
- The draft default is the stacked 24×8 matrix (open question 7).
- It is not part of the primary no-recurrent-matrix-learning comparison.

## Appendix D. Extended R-FIX search (OPTIONAL; excluded; separate approval)

- A pre-declared grid with VAL selection and TEST+VAL rejection. For example, 3 LRs × 2 restarts per seed per R-FIX arm, which is 120 extra runs.
- It has its own labels ("R-FIX-H(EXT)") and its compute is charged and reported.
- It could supply witnesses for the same class and target, stated as reached under the extended search.

## Appendix B. Feasibility checks already run (scratch, read-only, no training)

Location: `/workspace/scratch/frozen_comp/`. The scripts import the frozen PR #9 code read-only from a scratch clone, using torch 2.14.1+cpu.

- `feasibility.py` (sha be069574fe7c5a91d55a98c639c84b901b989659e176bee259d30c1bdf9ca622) and its output `feasibility.log` (sha 166fb16ab16cb3fa37881b84fe26c2000804a4b654d155c7b88daa50afb1ebc5):
  - parameter counts for H = 32, 48 and 70;
  - init pairing for seeds 400 and 409;
  - T for existing checkpoints.
- `T_existing.json` (sha 7fd2c9c6833cabc75dbabde10561125ab51508e445d6de2297175a5ad19b1dbf).
- `crosscheck.py` and `crosscheck.log`: the independent NumPy evaluator agrees with the frozen `evaluate_arm` and `l_prefix` to ≤ 4.4e-16 in predictions, with identical L_prefix and E to 10 significant figures (seeds 100 and 305, CAND and F-INIT).

T(θ) of existing checkpoints, τ = 0.25:

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

The binding component is E_XOR in every case except one (PR8 f_trained, one seed, L_prefix binding).

**Reading:**
- The unrestricted target is met with margin: 30/30, max T 0.73.
- A fully frozen W0 core with a trained readout (F-INIT) misses by an order of magnitude, through the XOR clause.
- **No existing checkpoint is an R-FIX model.** F-INIT also freezes W_ih and the biases, so nothing here predicts R-FIX.
- A non-binding note: the stage one-hot feeds W_ih and the biases directly, so trainable W_ih and biases can set the update gates z stage by stage, which could give retention. Compensation is plausible but not predicted.
