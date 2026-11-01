# Next causal question: planning note v1

Constitutive agent, 2026-10-21. **Planning note only.** It is not a spec. It proposes no run, no training and no freeze, and it modifies no existing artifact. It answers the Specialist's request after Astra #34 (`/workspace/astra_consult34_response.txt`, sha256 `bf724ca2…`). That request asked for the computation, an intervention that separates causal use from generic state damage, and an outcome that would change a named claim. Any study that follows needs its own reviewed and frozen scope recorded under the standing approval (Astra #34, L48). It also needs separate approval from Aidan, because this note authorizes nothing.

## 0. Why not repeat what failed
- **PR #5 E3** (`TWOSTREAM_ACQUISITION_PROTOCOL_v1.md` §6.3, `acquisition_results_v1/RESULTS.md` @ `88b500a`) has already tried a chart-decoder interchange.
  - The intervention was a ridge map from the stage-4 state to (m_x, m_y, c), then a partial transplant on col(W).
  - The result was **NOT LOCALIZED BY THIS INTERVENTION**.
  - A decoder finds where chart content *correlates* with the state. It does not find which state directions the recurrence *reads*. Moving that decoder earlier or later (to stage 2, 3 or 8) would not change this. That is Astra #34 L46.
- **The audit line (v1.3, PR #12) is closed.** It asked a decoding question, and its C2 null says nothing about use.
- **PR #9 (S15) is weight-level.** Graded W_hh reversion beats the FO and ISO controls at 8/10. It does not say *which* computation the trained W_hh contributes.

What follows defines the variable by its **effect on future behavior**, not by what it correlates with. The oracle is used only through its known update law, never as a regression target for states.

## 1. The computation (named)
**C-κ: the covariance-mediated cross-stream update.**
- In W2, the exact filter carries κ = 4·Cov(X, Y) between readings.
- The admission protocol (`TWOSTREAM_PROTOCOL_v1.md`, "Prefix alias") puts it exactly: "the next reading of the other variable moves that other marginal by a term proportional to κ". At stage 7, the carried κ appears in the terminal XOR forecast.
- A product-of-marginals (mean-field) filter has no such update. That is the **simplest rival** recorded for S12.
- **The behavioral prerequisite already exists.** PR #5 CAND GRU-8 has final TEST E_XOR of 5.1e-4 to 1.3e-3. That is below the analytic product excess 4E[c²] ≈ 7.95e-3, while K-FR (frozen recurrence) has E_XOR of about 0.025–0.039.
- **What is open is mechanism.** It is not known whether the trained recurrence carries a κ-like variable that later updates *read*, or whether the XOR advantage comes some other way, such as a history-specific terminal correction that never routes through a carried coupling.

**Question.** Does the trained GRU-8 carry, at stage k, a state variable whose *only route to later behavior* is the oracle's κ-route? Specifically: when that variable is edited, are later cross-stream updates and the terminal XOR forecast revised exactly as the exact filter revises them for the same κ change? And do equal-size edits outside it do much less?

## 2. Intervention (separating causal use from generic damage)
These are sketches; the spec fixes the details.
1. **Influence map, not a decoder.**
   - Fix a stage k and a reachable prefix a. For every continuation u of length 8−k, take the network's own response Jacobian J(u) = ∂F(a·u)/∂z_k (3×H).
   - Take the exact oracle's belief-response map L(u) = ∂q*(a·u)/∂(μ_x, μ_y, κ) at the stage-k belief (3×3).
   - The hypothesis "the future depends on z_k only through a chart-like variable" is J(u) ≈ L(u)·B, with a single B (3×H) shared over all u.
   - Fit B on one prespecified half of the continuations (U_fit). Report held-out agreement on the other half (U_test).
   - B is fitted to **how the state influences the future**, not to what the state contains. This is the main difference from E3.
2. **Edits** at z_k(a), all norm-matched, then run the unedited forward dynamics over U_test:
   - **κ-edit:** δ_κ = ε·B⁺e_κ. This moves only the network's own influence-defined κ coordinate.
   - **Marginal edits:** δ_μx and δ_μy, defined the same way. They test specificity, since they should give marginal patterns and not the κ pattern.
   - **Generic-damage edits:** random directions in null(B), at the same norm. Under C-κ they should barely change future behavior. Under "the state is used diffusely" they should matter as much as δ_κ.
   - **Same pipeline on matched controls:** INIT and K-FR GRU-8 of the same seed. K-FR has trained readout and frozen recurrence, so it is the "learned recurrence" contrast.
3. **Zero-parameter prediction.** For the κ-edit, the predicted change is ΔF(u) ≈ ε·L(u)e_κ on U_test, with no fitted scalar. The test is directional: it checks sign and shape across continuations, especially the X forecast after later Y readings and the terminal XOR. Generic damage has no reason to produce that structured pattern. That is the separation the brief asks for.
4. **Nonlinearity guard.** ε is set as a fraction of the reachable κ spread at stage k. The actual forward pass is scored, not the Jacobian.

**Why this is not the error decoder moved earlier:**
- No map from states to chart values or to errors is fitted.
- No oracle probability is a regression target.
- The claim rests on edits and held-out continuations.

## 3. Outcomes and the named claims they would change
- **O-USE.** In CAND, all three hold: high held-out agreement, the κ-edit reproduces the oracle κ pattern on U_test, and null(B) edits do much less at equal norm. K-FR and INIT do not show this.
  - **Changes S12** (PR #5, triage v1.4) and its ceiling's non-claim "irreducible joint state; marginal-filter or mean-field identification". The S12 mean-field rival becomes *excluded at the state level for the tested checkpoints*, bounded, as Q-CAUSE characterization.
  - **Sharpens S15** (PR #9): a candidate computation now exists for the weight-level contribution. A later, separate question could ask whether graded W_hh reversion removes the κ-row first. That is not proposed here.
  - E3's label is unchanged, because it was a different intervention.
- **O-NOκ.** The future is chart-funneled, but the κ-row is absent: the κ-edit is no better than null(B) edits.
  - This puts the CAND XOR advantage outside a recurrently carried coupling.
  - S12's mean-field rival stays *open*, and the S12/E2 reading ("recurrent adaptation") needs a ruling on what it adapted.
  - This is informative, not a null.
- **O-DIFFUSE.** Low held-out agreement, or null(B) edits that damage as much as δ_κ.
  - Reads "not shown by this intervention". S12 and S15 are unchanged.
  - Never "state not causal" or "distributed", following the PR #5 §8.3 rule.
- **K-FR caveat (as in the E3 qualifier).** K-FR fails A-FIT, so its failure can come from poor prediction. A CAND/K-FR contrast supports only "observed in CAND but not in the matched frozen-recurrence control". The primary discriminator is *within-network*: δ_κ against null(B).

## 4. Feasibility and headroom (E34-6) before any spec freezes
These are paper-level questions. None needs a checkpoint to be loaded.
- **F-H1 (headroom, oracle only).** For each candidate (k, a), compute the size of ε·L(u)e_κ over U_test. Stages and prefixes where it falls below the effect floor are excluded *before* any network is touched, and their count is reported. The effect floor and the headroom are prespecified separately (E34-6). The 70/230 lesson applies: no unit may be infeasible by construction.
- **F-H2 (stage choice).** Post-X stages (odd k) are preferred, because the next reading is Y and the cross-update is immediate. k = 3 gives 32 continuations, a 16/16 split, and 16·3·H equations for 3H unknowns in B.
- **F-H3 (chart validity).** The κ-edits are judged against the exact filter at the *edited* belief. That belief must stay a valid four-state distribution, which is guaranteed for ε small enough; the bound has to be stated. Under A0 (zero same-phase aliases), a κ change with fixed marginals is never a reachable history. The test is therefore about the network's response to a hypothetical belief, and the spec must say so.
- **F-R (roster).** PR #5 CAND GRU-8 and K-FR GRU-8, seeds 0–9, final checkpoints, plus INIT. Their availability and integrity must be confirmed from the PR #5 record before a spec is written. PR #7–#10 checkpoints are optional and secondary.
- **No training.** Evaluating these checkpoints is still a run, with its own protocol and approval.

## 5. Threats for the adversarial review (pre-registered against myself)
1. **B as a decoder in disguise.** It is fitted to response Jacobians, which are causal sensitivities, not to labels. But it *is* fitted. Held-out continuations must be enough, or prefixes must also be held out (one B shared across prefixes in a fold is the stronger claim).
2. **Local-linear artefact.** Agreement of the Jacobians could hold while the finite-ε forward pass diverges. The forward pass is the scored quantity.
3. **Accuracy implies the result.** A near-oracle network might pass trivially. Counter: off-manifold κ-edits are not constrained by training fit (A0), so passing is not implied by predictive accuracy. The Delegate should test this claim.
4. **Null(B) is the wrong damage control.** If null(B) is small in effect by construction (rank, conditioning), the comparison is unfair. Matched-norm random edits over the full state should be reported too.
5. **Multiplicity.** One stage, one ε, one split and one decision rule should be fixed in the spec. Everything else is descriptive.

## 6. What this note does not do
It writes no spec, runs nothing, selects no thresholds or ε values, and edits no frozen artifact or claim row. It adds no C4, C5, consciousness, necessity or organism claim, and it does not reopen Track B. Earlier causal findings remain unchanged (Astra #34 close-out).
