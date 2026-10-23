# Next causal question: planning note v1.1 (additive)

Constitutive agent, 2026-10-21. **Planning note only.** It proposes no spec, run, training or freeze. v1 (`next_causal_question_planning_note_v1.md`, sha256 `be3a9ffd…`) is unchanged, and this file supersedes v1 only where it says so. It answers the Delegate's adversarial review (`next_causal_question_planning_note_v1_adversarial_review_RD.md`, sha256 `81e2ac54…`), which was checked against Astra #34 (`bf724ca2…`).

**I accept every item: B1, B2, M1–M6 and m1–m10.** I own B2. My §5.4 saw the null(B) problem only as a matter of rank and conditioning. It missed that, once J ≈ L·B fits, both of v1's pass conditions follow from the algebra. That is the same structural trap as the 70/230 floor.

## A. Roster (B1, M3, m7). Replaces v1 §4 F-R
- **PR #5 is out:** no weights were persisted (Astra #34). Retraining is not proposed.
- **Primary roster: PR #7 seeds 100–109.** The arms are cand_final, F-TRAINED (frozen trained core with a new readout) and F-INIT (frozen init core with a new readout).
  - F-INIT is the better comparator. Its recurrence is untrained and its readout is trained.
  - The Delegate's figure of CAND E_XOR 4.49e-4 to 1.68e-3 is taken from their review and has not been re-read by me.
- **PR #8–#10 are optional.** Of these, PR #9 cand_final, seeds 300–309, is needed only for any S15 linkage. Without it, the S15 row is untouched and any link is hypothesis-only.
- **All comparator contrasts are descriptive (M3).** No Q-LEARN claim is tested.

## B. Primary test (B2, M2, M6). Replaces v1 §2 steps 2–3 as the decision basis
1. **Nested κ-row test, held out by prefix.**
   - Fit B on prefixes in some G-orbit groups and test on held-out groups, respecting orbits. Freeze every fit before any edit is scored (M6).
   - Compare a marginal-only map J ≈ L_μ·B_μ (2 rows) with the full map J ≈ L·B (3 rows) on held-out prefixes and continuations.
   - The statistic is the held-out gain from adding the κ row. Its floor is set separately from its headroom (E34-6), and B needs a numerical rank rule.
   - This can fail on its own: the κ row may add nothing held out.
2. **Edits that B does not define, scored by a finite-ε forward pass.**
   - Edit types: random edits within range(B), random full-state edits, data-defined chord edits ε·(z_k(b) − z_k(a)) toward held-out prefixes b, and equal-impact edits for pattern specificity.
   - For each edit, score the observed stage-8 response ΔF(u) against L·B·δ, with and without the κ row.
   - The κ claim needs the κ row to improve held-out prediction of responses to edits it did not construct.
3. **Downgraded to descriptive:** the v1 κ-edit (δ_κ = ε·B⁺e_κ), null(B) edits and the marginal edits (M2). Following m3, report both the minimum-norm δ_κ and its affine class.

## C. Oracle-only prechecks (B2, M2, M4)
These are oracle computations and need a recorded scope (m8). They are not hand arithmetic.
- **Non-collinearity:** check that L(u)e_κ is not in span{L(u)e_μx, L(u)e_μy} across u at the candidate stage.
- **Triviality:** take an exact filter written in arbitrary affine coordinates, and a near-affine accurate surrogate restricted to the reachable states. Check whether the test passes by construction. If it does, the stage is ineligible.
- **Stage choice from headroom, not from the continuation count** (M4). Covariance is zero before reading 2, so stage k must be chosen from the oracle headroom.
- **Bounds:** each statistic gets its upper bound, the stage where it is assessed, and a rule for an unreachable floor (meaning infeasible, not a failure). Checkpoint-dependent bounds are labelled as such.

## D. Wording and outcome map (M1, M5, m1, m4, m9). Replaces v1 §3
- **The rivals are kept separate (M1):**
  - **(i)** The terminal product of marginals is already excluded by 4E[c²], as a whole-set scale comparison (m5).
  - **(ii)** The step-by-step mean-field filter is UNVERIFIED until its oracle-only error has been computed.
  - **(iii)** Marginals plus a lookup cannot be excluded on reachable histories.
  - A positive outcome reads **"κ-aligned local influence geometry"**. It bears at most on (iii), as a local, off-manifold statement, and only if Astra rules that admissible (Q1). "Irreducible joint state" stays on the not-established list.
- **Every outcome is Q-CAUSE characterization only (m9).** Observables are terminal (stage-8) forecasts across continuations; intermediate updates are not observed (m4). B is described as "a fitted tangent-space map, not fitted to state content, errors or oracle probabilities", and predictions have "no parameters beyond the fitted B" (m1).
- **Outcome branches (the claim unit and quota go in the spec):**
  - **POSITIVE:** the κ row is needed, held out, and it predicts responses to edits that B did not construct.
  - **NOT SHOWN:** no held-out κ-row gain. This replaces v1's O-NOκ and O-DIFFUSE wording, and it is never "outside a recurrently carried coupling" or "not causal". E2 is untouched.
  - **UNRESOLVED:** rank rule failure, infeasible floor or integrity failure.
  - **NONLINEAR:** the Jacobian test passes but finite-ε responses diverge. Reported, not counted as a positive.
  - **MIXED:** below quota in either direction.
  - **COMPARATOR ALSO PASSES:** a pass in F-INIT means the geometry is not attributable to learned recurrence. Descriptive only.
  - **NEAR-ZERO SENSITIVITY:** ‖J‖ is below a prespecified floor, which makes the stage ineligible.

## E. Approval and rulings
- **Research Lead's rulings (Specialist, in the room).**
  - **Q4:** the PR #7 roster is acceptable, and Astra still rules on it.
  - **Q5:** Aidan's standing approval of 15:15 (`PI_STANDING_APPROVAL_2026-10-21_1515.md`) covers both the oracle-only feasibility package and the inference study. Each still needs a written scope record and a freeze before any computation, so nothing new goes to Aidan.
- **Nothing runs until Astra rules on Q1–Q3,** including the oracle-only computations. Astra #34 L48: "A future study still needs its concrete scope reviewed, frozen and recorded under that approval."
- v1's line 3, "separate approval from Aidan", is superseded by the Q5 ruling.

## F. Where each review item is resolved

| Item | Fix | Section |
| --- | --- | --- |
| B1 | PR #5 dropped. Primary roster is PR #7 cand_final, F-TRAINED and F-INIT, seeds 100–109; PR #8–#10 optional | A |
| B2 | Primary test is the nested held-out comparison of a marginal-only map against the full map, with its own floor and a rank rule. Edits that B doesn't define are scored by forward pass. The v1 κ-edit and null(B) edits become descriptive | B.1–B.3 |
| M1 | Three rivals kept separate. Positive result reads "κ-aligned"; "irreducible joint state" stays not established | D |
| M2 | Oracle-only triviality check. Marginal edits descriptive only | B.3, C |
| M3 | F-INIT and F-TRAINED as comparators, all contrasts descriptive, no Q-LEARN claim | A |
| M4 | Bounds, assessment stage and an unreachable-floor rule for every statistic. Stage chosen from oracle headroom. Checkpoint-dependent bounds labelled | C |
| M5 | Full outcome map. "Not shown" never reads as a negative mechanism claim. E2 untouched | D |
| M6 | Holdout by prefix, respecting orbits. Every fit frozen before any edit is scored | B.1 |
| m1 | "Tangent-space map, not fitted to content"; "no parameters beyond the fitted B" | D |
| m2 | Edit-size convention and saturation guard are deferred to the spec, which must fix one primary unit, report the other, and report clipping of edited states | open for spec |
| m3 | Minimum-norm δ_κ and its affine class both reported | B.3 |
| m4 | Observables are stage-8 forecasts only | D |
| m5 | 4E[c²] treated as a whole-set scale comparison | D |
| m6 | S12 and S15 cited to triage v1.4 (L425, L428, L465–476); E2 to `acquisition_results_v1/RESULTS.md` L7 and the protocol §8.2 | this table |
| m7 | S15 link only with PR #9 seeds 300–309, otherwise hypothesis-only. S15 keeps its own bound, "causal contribution, not necessity" | A |
| m8 | Oracle checks are computations that need a scope record | C, E |
| m9 | Q-CAUSE characterization only | D |
| m10 | Claim unit, quota, prefix aggregation, roster and primary damage control are fixed in the spec | B, D |
