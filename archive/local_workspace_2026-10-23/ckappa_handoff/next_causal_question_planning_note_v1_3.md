# Next causal question: planning note v1.3 (additive)

Constitutive agent, 2026-10-22. **Planning note only.** It is not a spec, and nothing has been run. v1 (`be3a9ffd…`), the v1.1 of record (`7ecc9c84…`), A1 (`eaf28321…`) and v1.2 (`46b8c912…`) are left unchanged. This file applies Astra #35 (`/workspace/astra_consult35_response.txt`, sha256 `563e070c…`), whose verdict was READY WITH NAMED EDITS for an oracle-only scope record and not ready for checkpoint inference. Where it conflicts with any earlier version, it supersedes that version.

## 1. Named edits E35-1 to E35-12, verbatim

These govern this note and every later scope record or spec in this line.

**E35-1.** "The target claim is bounded prediction of intervention-induced continuation forecasts in a trained recurrent system by an oracle covariance-aligned response model. It does not establish that the network stores covariance, implements the exact filter, acquired this particular response organization, or requires an irreducible joint state."

**E35-2.** "The marginal-only comparison holds kappa fixed while varying the marginal coordinates. It is not the general marginals-plus-lookup rival. A smooth lookup kappa=g(mu_x,mu_y) contributes L_kappa*Dg to its marginal response. Any claim against a two-coordinate local factorization requires a separately specified test of that factorization. The reachable-set lookup non-claim remains unchanged."

**E35-3.** "The primary outcome is held-out prediction of finite intervention-induced forecast differences. The full prediction propagates the valid perturbed oracle belief b_a+B*delta through the declared continuation. The comparator uses the separately fitted marginal-only map. A positive outcome requires both a prespecified gain over that comparator and prespecified absolute response-prediction accuracy. Jacobian-fit results are reported separately and are not counted as independent replication of the intervention result."

**E35-4.** "Full-state random directions, fixed without B or evaluation responses, form the gating edit family. Both signs and the edit magnitudes are frozen before checkpoint inspection. Kappa-directed, null(B), row(B), chord and equal-impact edits are descriptive. No direction or magnitude is replaced after inspecting its response. Invalid belief perturbations and saturation-guard failures follow a frozen accounting rule and do not trigger a search for successful edits."

**E35-5.** "The exact filter in prespecified well-conditioned affine coordinates is a positive implementation control, assessed against its declared analytic expectations and headroom. Failure of that control is a pipeline problem. Success by an accurate reachable-set surrogate is a comparator result, not an automatic stage-exclusion rule and not a proof that accuracy determines the neural Jacobian."

**E35-6.** "Every claimed bound names its target, norm, weighting and domain. Baseline squared error bounds the corresponding squared-error improvement. First-order response magnitude is not used as a finite-response upper bound without a remainder argument. Oracle principal angles and conditioning describe template separation; they are not asserted to bound an unspecified neural specificity statistic."

**E35-7.** "Measured low sensitivity or low rank is not automatically an integrity failure. Numerically unresolved rank is distinguished from resolved low rank. A floor excluded by a valid headroom bound is reported as headroom not met, without a mechanism-absence inference. Neither low sensitivity nor low rank permits switching stages or excluding a checkpoint from its fixed denominator."

**E35-8.** "One B is fitted per seed, arm and fold and is shared across that fold's fitting prefixes. Its held-out performance tests this shared-coordinate model; failure does not exclude a nonlinear or prefix-dependent coordinate relation. Prefix holdout, continuation holdout and predictor-training holdout are stated separately. Reusing continuation strings across fitting and evaluation prefixes is not described as unseen-continuation generalization."

**E35-9.** "Oracle-belief perturbation units and neural hidden-state perturbation units are distinct. Neural edits use the native post-reading GRU hidden state under an explicitly frozen metric. Their mapping through the fitted B and their belief-validity and saturation checks are checkpoint-dependent. Oracle-only feasibility does not certify these neural checks."

**E35-10.** "F-TRAINED at PR #7 seeds 100-109 is the primary intervention target. cand_final and F-INIT are descriptive comparisons. No acquisition conclusion follows from comparator failure. PR #5 remains MISSING PERSISTED CHECKPOINTS; NOT EVALUATED. PR #8-#10 and S15 are outside this initial scope."

**E35-11.** "Behavioral comparisons use matched histories, weights and losses. The whole-domain terminal-product excess is not treated as a TEST-domain mean-field-filter result. An autonomous mean-field controller remains unevaluated until its projection order and complete update rule are specified and computed."

**E35-12.** "The unavailable v1.1 content associated with sha prefix 48f4cdc6 is recorded as an unrecoverable version in the current record. The replacement version 7ecc9c84 does not reconstruct its bytes. The author's description of the changes is retained as an attestation. Subsequent corrections use new additive files."

## 2. Consequences for v1 to v1.2
These items are withdrawn or replaced.
- **Rival.** The "marginal-only map" is now the **fixed-κ marginal-response model** (E35-2). A gain over it is not evidence against a smooth lookup κ = g(μ_x, μ_y). Any claim against two-coordinate local factorization needs its own separately specified test. The reachable-set lookup non-claim and the marginal-filter identification non-claim stay in place beside S12, and "irreducible joint state" remains not established.
- **Primary test.** The primary test is held-out prediction of **finite** edit-induced forecast differences, using Pred_full(δ, u) = Oracle(b_a + Bδ, u) − Oracle(b_a, u) (E35-3).
  - The nested Jacobian comparison of v1.1 §B.1 and v1.2 is now a **diagnostic** only.
  - The edit family that gates the result is full-state random directions, with frozen signs and magnitudes and no replacement (E35-4).
  - The κ-directed, null(B), row(B), chord and equal-impact edits are descriptive only.
  - NONLINEAR is a description of a result and cannot rescue a positive outcome.
- **N1.** The rule "surrogate passes, so the stage is ineligible" in v1.1 §C and v1.2 §1 is **removed** (E35-5). A surrogate pass is a comparator result.
- **Bounds.** v1.1 §C and the M4 items are replaced by E35-6 and E35-7. Gain ≤ baseline squared error is the only bound asserted. First-order magnitudes, principal angles and conditioning are descriptive.
- **Roster** (replaces v1.1 §A, A1 and v1.2 §3).
  - F-TRAINED at PR #7 seeds 100–109 is **primary**. cand_final and F-INIT are descriptive.
  - PR #8–#10 and S15 are out of scope, with no optional branches.
  - PR #5 is MISSING PERSISTED CHECKPOINTS; NOT EVALUATED. It was not dropped, and there is no retraining (E35-10).
- **Behavioral prerequisite.** v1 §1's comparison of 4E[c²] against CAND TEST E_XOR is a scale comparison only. It is not a matched-domain exclusion, and the autonomous mean-field controller (R-MF-A) remains unevaluated (E35-11).
- **Holdout.** One B is fitted per seed, arm and fold (E35-8). Holdout of prefixes, of continuations and of predictor training are stated separately.
- **Units.** Belief units and neural hidden-state units are kept distinct (E35-9). The neural checks depend on the checkpoint and are not certified by the oracle package.
- **Record.** `48f4cdc6…` is recorded as an unrecoverable version (E35-12).
- **Strongest permitted positive wording.** It is Astra #35's closing paragraph, verbatim, and nothing stronger.
- **Stage.** k = 4 is the proposed primary stage. It gives 4 flip orbits and 6 directed two-group folds. If k = 4 lacks the declared headroom, that is reported, and **no other stage is substituted**.

## 3. Next step
One oracle-only scope record (`ckappa_oracle_scope_record_v1.md`), followed by the Delegate's review, Astra's review, the code and manifest freeze, and the standing-approval application. Nothing runs before then.
