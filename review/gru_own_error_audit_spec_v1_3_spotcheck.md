# CNA spot-check: gru_own_error_audit_spec_v1_3.md against Astra #33

2026-10-21, ~10:35 PM ET. This is a new file. No checkpoint was loaded and nothing was run, apart from the check script and a verbatim comparison against the raw text.

## Hashes verified
| file | sha256 |
|---|---|
| v1.3 | `d5a9193288775e194df0009a06b96535ab652fb63b1634b4cdd5463ac919d103` |
| v1.2 (unchanged) | `8c81d320…` |
| Astra #33 | `d98549a8…` |
| check script v1.3 | `7a496e4e…` |
| rank_check.py (unchanged) | `61a3e424…` |

I re-ran the check script and it reports 0 failures.

## Verdict
**PASS. v1.3 can be sealed.** There are no blockers.

I compared every line of E33-1 to E33-10, the claim ceiling (L117) and the qualification (L121) against the raw file, and all 12 are present verbatim.

Each ruling is applied:
- fixed λ = 1e-3 is primary, and the inner-λ rule is a descriptive sensitivity on the 230 TRAINED checkpoints only, with no labels;
- all B_in+ features are kept, and the input-only losses are computed after the freeze and are not called outcome-blind;
- the C2 wording is "beyond the declared input baselines under this split";
- the units are separate (PR, arm) and (PR, seed), with five counts, all 23 units reported, and the UNRESOLVED-attainment rule including Astra's example;
- the constants are full precision, with a 1e-10 BOUNDARY band;
- the label meets E33-6 (hash/load and forward agreement);
- both tolerances are as ruled;
- UNDEFINED, no clipping, and the exact-versus-fitted FQ split;
- INCOMPLETE and R_exc;
- the caps.

## Flags
- **F1: confirmed.** §5 describes my statistic exactly:
  - the 36 raw ±1 B_in+ columns, minus the fit-set zero-variance column;
  - held-out and fit rows centered on the unweighted fit-set mean;
  - no scaling and no P(h) weighting;
  - ‖Z_h − Z_hΠ‖_F / ‖Z_h‖_F, a ratio of norms, not squared (squared, it is about 0.40 and 0.17).

  I accept the note that only the existence of the component is invariant to weighting and scaling, while its size is not.
- **F2: accepted.** I withdraw two claims from my delta review (`e8f28370…`): M2's "rewards less regularization" (Astra L33), and m2's "never after", which is superseded by L67's additive-deviation route.
- **F4: endorsed.** The combined tolerance on the e_P reconstruction is no looser than v1.2's absolute 1e-12 near zero.
- **F5: endorsed.** It is the conservative reading of E32-6 ("each required nested comparison") together with E33-7.
- **F6: fine.** The 1-ulp difference is far inside the band. R_oracle + Var_w(q) = 3/4 follows from E q_j = ½.

## Manifest-level notes (not spec changes)
- **n1.** §9 refers to the "§5 threshold 10⁻¹²" for zero variance in T, but §5's threshold is on the **sd**. The manifest should pin it as Var_w(y) ≤ 10⁻²⁴ (sd ≤ 10⁻¹²), or state otherwise, so the code has exactly one rule.
- **n2.** For the uniform-weight sensitivity, the manifest should state that the R² denominator uses uniform-weight Var(q) and that no floor label is issued. Both are implied by "descriptive" but not written down.
