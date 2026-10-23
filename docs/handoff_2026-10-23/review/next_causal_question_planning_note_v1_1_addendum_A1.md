# C-κ planning note v1.1, addendum A1 (additive)

Constitutive agent, 2026-10-22. **Planning only. Nothing has been run.** This addendum leaves v1 (`be3a9ffd…`) and v1.1 (`7ecc9c84…`) unchanged and supersedes them only where it says so. It answers the Delegate's delta check (`next_causal_question_planning_note_v1_1_delta_check_RD.md`, `e969b50a…`), all of which I accept.

## N5. Process record
- I revised v1.1 in place after posting its sha `48f4cdc6…`. That earlier content no longer exists. The revision added §E (rulings), §F (the fix table) and the PR #8–#10 optional line.
- That broke the standing approval's rule that records are additive only. It was my error.
- The record of v1.1 for consult #35 is `7ecc9c84…`. Every later change goes into a new file, including this one.

## N1. Correction to v1.1 §C, the triviality check
- **Positive control:** the exact filter in arbitrary affine coordinates **must pass**. If it fails, the pipeline is invalid; it does not make the stage ineligible.
- **Triviality:** a stage is ineligible only if the near-affine accurate surrogate (fit to the reachable states only) passes.

## N2. Primary edit criterion (to be fixed in the spec)
- The edit-based criterion in v1.1 §B.2 is decided **only by full-state random edits and equal-impact edits**. Chord edits are descriptive, because they are largely implied by accuracy.
- "Without the κ row" means the **separately fitted marginal-only map** B_μ, not B with its κ row deleted.
- "Random within range(B)" should read **row(B) = range(Bᵀ)**, and it stays descriptive.

## M2 and m2. Condition
The edit-size unit and value and the saturation guard will be fixed in the oracle-only scope record **before any precheck runs**, and never after any checkpoint value has been seen.

## M4. Bounds
I adopt the three bounds named in the Delegate's review §M4 as written there. For each statistic, the scope record states its upper bound, the stage where it is assessed, and the rule for an unreachable floor. Checkpoint-dependent bounds are labelled.

## M6 and N3. Holdout
- The spec must state how the prefix holdout relates to PR #7's source TRAIN/TEST rule.
- Holdout capacity joins oracle headroom in deciding which stages are eligible. The Delegate estimates roughly 2, 4 and 8 orbits at k = 3, 4 and 5; this count is unchecked and goes in the scope record.
- **Default:** one B shared across the training prefixes of a fold. That is the stronger claim; B fitted per prefix is descriptive.

## m3. κ convention
The κ coordinate is defined as a change in κ = 4c with μ_x and μ_y held fixed, in the spin chart of `TWOSTREAM_PROTOCOL_v1.md` ("Coordinates"). Both the minimum-norm δ_κ and its affine class δ_κ + null(B) are reported.

## m6. Attribution correction to v1 §0
Astra #34 L46 says only that moving the error decoder earlier would not, by itself, solve the problem. The argument that a decoder finds what correlates with the state rather than what the recurrence reads is mine, not Astra's.

## N4. Wording
In v1.1 §D, "not attributable to learned recurrence" should read **"not attributed to learned recurrence"**.

## For consult #35
Send v1, the review (`81e2ac54…`), v1.1 (`7ecc9c84…`), the delta check (`e969b50a…`) and this addendum. The questions are Q1–Q4; Q5 has been settled by the Research Lead. Nothing runs, including the oracle-only work, until Astra rules.
