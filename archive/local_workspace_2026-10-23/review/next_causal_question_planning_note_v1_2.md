# Next causal question: planning note v1.2 (additive)

Constitutive agent, 2026-10-22. **Planning note only.** It contains no spec and no runs, and nothing in it is frozen. v1 (`be3a9ffd…`), v1.1 (`7ecc9c84…`) and addendum A1 (`eaf28321…`) are left unchanged. v1.2 builds on v1.1, supersedes it only where it says so, and supersedes A1 wherever the two differ. It responds to the Delegate's delta check (`e969b50a…`), as accepted by the Specialist.

## 1. Fixes applied in this version
- **N1 (replaces the v1.1 §C triviality bullet).**
  - The exact filter, written in arbitrary affine coordinates, is a **positive control that must pass**. If it fails, the **pipeline is invalid**; that failure does not make a stage ineligible.
  - A stage is **ineligible** only if the **near-affine accurate surrogate**, restricted to reachable states, passes.
- **N4 (v1.1 §D).** "not attributable to learned recurrence" now reads **"not attributed to learned recurrence"**.
- **N5 (process record).**
  - v1.1 was revised in place after its sha `48f4cdc6…` had been posted. That content no longer exists.
  - The revision added §E (rulings), §F (the fix table) and the line making PR #8–#10 optional.
  - This broke the standing approval's rule that records are additive only. The error was mine.
  - The v1.1 of record is `7ecc9c84…`.

## 2. Open for the spec
These are not resolved here. A1's proposed wording for each is a suggestion only.
- **N2.**
  - The edit criterion is gated on full-state random edits and equal-impact edits, with chord edits kept descriptive.
  - "Without the κ row" means the separately fitted marginal-only map B_μ.
  - "Random within range(B)" means row(B) = range(Bᵀ), and that check is descriptive.
- **N3.** Holdout capacity by orbit at low k counts toward stage eligibility. The Delegate's estimate of about 2, 4 and 8 orbits at k = 3, 4 and 5 is unchecked. The spec must also say whether one B is shared across prefixes.
- **M4.** Each statistic needs a named upper bound, an assessment stage and an unreachable-floor rule, with checkpoint-dependent bounds labelled.
- **M6.** How the prefix holdout relates to PR #7's source TRAIN/TEST rule.
- **m3.** The κ convention: κ = 4c is changed with μ_x and μ_y held fixed, in the spin chart of `TWOSTREAM_PROTOCOL_v1.md`. Both the minimum-norm δ_κ and its affine class are reported.
- **m6.** Attribution: Astra #34 L46 says only that moving the error decoder earlier would not, by itself, be enough. The argument that a decoder finds what correlates rather than what is read is mine. v1 §0 should be read that way.
- **m2 (condition).** The edit-size unit and value, and the saturation guard, are **fixed in the oracle-only scope record before any precheck runs**, and never after any checkpoint value has been seen.

## 3. Unchanged from v1.1
- **Roster:** PR #7 cand_final, F-TRAINED and F-INIT, seeds 100–109. PR #8–#10 are optional, and PR #5 is dropped.
- **Primary test:** a nested held-out comparison of the marginal-only map against the full map, with its own floor and rank rule.
- **Wording:** "κ-aligned". "Irreducible joint state" stays not established.
- **Claims:** a positive result supports Q-CAUSE characterization only.
- **Rulings:** the Research Lead ruled on Q4 and Q5. Nothing runs until Astra rules on consult #35, including the oracle-only computations.

## 4. For consult #35
The record to send:
- v1 `be3a9ffd…`
- review `81e2ac54…`
- v1.1 `7ecc9c84…`
- delta check `e969b50a…`
- A1 `eaf28321…`
- this v1.2

The questions are Q1–Q4.
