# C-kappa oracle package: implementation questions (phase 1)

These points are unresolved by the governing set. The code contains one provisional reading of each so the package is complete enough to review. That reading is not a ruling. Phase 1 stops here: the manifest is unsealed, and no package stage has been run.

Precedence used while reading the scope:

1. The E36 verbatim text (Astra #36, in v1.3_E36 `f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5`) governs over everything else.
2. Then: closure note `4ad1d217aaab0bd45d2be6fd3e24872a4b22407d0c8abc2fa36a5a1ac7c45c9c` > v1_4_N `3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359` > rest of v1.3_E36 `f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5` > v1.2 `7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d` > v1.1 `e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c`.
3. RL records (`CKAPPA_SCOPE_GOVERNING_SET_RL.md` `6a5e0f24995a1349664349713e1ee0a550267ac06ab0e4b462b121d931c15c63`, `CKAPPA_SCOPE_RL_RULING_B2_B3.md` `6d75918f7cc2ae06386d80400645345539d7e6f0d893f105bbb7fa0b2c563edd`, `review/CKAPPA_PR13_RL_RULING_Q1_Q11.md` `9a2ea59bc6a1063eed108b66d23a8c8e7edcec6f683393be2be0dc51ab1d0c1d`) are implementation rulings. They are subordinate to E36 and cannot override it.

## 1. Scheduled float count

v1.2 D-6 states approximate totals: O6/O7 ≈ 5.9×10⁵, O5 ≈ 3×10⁵, Jacobians and finite differences ≈ 1×10⁵, total ≈ 1×10⁶. The loops named elsewhere multiply to 788480 float64 continuations Φ:

| piece | count |
| --- | --- |
| O2 central differences, 16×16×3×2 | 1536 |
| shared true-chart baselines, 16×16 | 256 |
| O6 edits, 6×8×16×16×2×4×3 | 294912 |
| O7 baselines, upper bound 16×16 | 256 |
| O7 edits, same upper bound as O6 | 294912 |
| O5 off-baseline, 16×16×64×2×3×2 | 196608 |
| O4 and O3 | 0 |

The closed-form Jacobian is a linear map, so it is not given a propagation count. Provisional declaration in `ckappa_oracle/schedule.py` and the draft manifest: the scheduled upper count is 788480. A run whose float64 continuation count exceeds that integer is `PIPELINE INVALID`. The D-6 approximations are not added as further calls.

## 2. O7 direction seed

v1.3 §3 names direction seeds for O6 (35016), O4 (35004), and §6 (36100–36109). It names no O7 seed. Closure N-b still requires a hash for the O7 direction array. Provisional reading: O7 reuses the O6 draw. `outputs/drawn_array_hashes.json` gets an `O7_directions` record with the O6 seed, shape, dtype, and raw-byte sha256, and `shared_with: O6_directions`. There is no second `standard_normal` call. `drawn_arrays.npz` stores that same array under `O7_directions`.

## 3. Chart mean, D, g's weights, and O7 standardization

v1.1 defines D as the P-weighted chart standard deviations over the 16 prefixes, and O7's coordinate as `z = Q2 · (standardized μx, μy)`. v1.3 fits g by P-weighted least squares over the 16 reachable `(μ, κ)`. The texts do not say whether "P" is the prefix mass P(a), whether the mean inside D is weighted, whether the divisor is `sum(w)` or `sum(w) − 1`, or whether "standardized" is a diagonal scaling or a 2×2 whitening. Provisional reading, one convention for all of these:

- weights are P(a), the sum of P(h) over the 16 continuations;
- the chart mean is the P(a)-weighted mean;
- each chart coordinate's standard deviation uses divisor `sum(w)` (population);
- g is fit with those same P(a) weights on the raw monomials;
- O7 z = Q2 * D_mu^-1 ((mu_x, mu_y) - mu_bar) is centered with the same P(a)-weighted mean and the same mu block of D as O6.

## 4. Prefixes in the O7 sigma stack

B3 says the sigma report uses the stacked Jacobian over the non-voided prefixes per fold. It does not say whether a fold contributes its fit prefixes, its evaluation prefixes, or both. Each fold's fit and evaluation prefixes partition the 16 prefixes. Provisional reading: the stack for a fold is `∂Φ/∂z` on the non-voided fit prefixes, all 16 continuations, and all three outputs. The derivative is the closed-form L at the O7 baseline chart times `dθ/dz`. Voided prefixes are omitted. An empty stack has no third singular value and is not a stop.

## 5. Rank-unresolved g

N3 leaves an unresolved design unscored. It does not say what the package does when the single quadratic g is rank-unresolved. Without coefficients there is no per-prefix void test and no `∇g`. Provisional reading: O7's status is `G RANK UNRESOLVED`. Coefficients are not scored. Derivatives, the sigma report, and finite predictions are skipped. The status is not `PIPELINE INVALID`. The package continues to O3. g is not refit.

## 6. O5 and invalid perturbed charts

E36-4 defines the scoreable-edit mask for O6 and O7. O4 has its own validity count. O5's definition does not mention the mask. A perturbed chart can also make a one-step predictive probability exactly 0, which the float filter raises as `ValueError`, or can return a non-finite forecast. Ruling: O5 uses the O4 perturbations and the O4 validity rule (all four p >= 1e-6), checked before Phi is evaluated, on both Phi(b_a + Delta) and its kappa-zeroed counterpart. One common mask applies to the numerator and the denominator of R_G. Invalid, ValueError and non-finite cases are left out of both means and reported by count and law mass, per size and per group. O5 stays descriptive.

## 7. Coverage when an O6 fold is rank-unresolved

N3 says an unresolved cell is not scored and stays in the denominator. Closure B1 says that any rank-unresolved O6 B or B_μ design yields `REFERENCE RANK UNRESOLVED` and that no pooled §5 statistic is formed. N1, as amended by B1, checks coverage before that label. Ruling: keep the logic (coverage on resolved folds, coverage failure checked first). Every unresolved fold still gets a coverage row marked "not propagated" (E36-4 requires every fold).

- coverage is computed on the resolved folds, and a coverage failure there is checked first;
- every unresolved fold still gets a coverage row marked "not propagated";
- if any fold is unresolved and no resolved fold fails coverage, the label is `REFERENCE RANK UNRESOLVED` and the pooled §5 statistic is `not_formed`;
- if a resolved fold fails the integer count test or its law-mass coverage is clearly below 0.75, the label is `REFERENCE COVERAGE NOT MET`.

## 8. O6 sample shorter than 1,000

The projection consumes the first 1,000 O6 float64 propagations. Under the ruling on question 7, a rank-unresolved fold is not propagated. If every fold is unresolved, the O6 stage ends with fewer than 1,000 propagations. The scope does not name a stop for that event. Ruling: exit code 6 stays. The O6 stage file is written, then the package stops with stop kind `STEP 0 SAMPLE SHORT` and exit code 6. `driver.py` must not overwrite O6's outcome label with the stop kind; both are recorded separately. This kind is separate from `PROJECTION HALT`, `CAP RESERVE REACHED`, and `CAP REACHED`. One resolved fold produces far more than 1,000 propagations, so this stop is reached only when every fold is unresolved.

## 9. Contents of t_sample

E36-13 retains the first 1,000 O6 propagations and does not recompute them for timing. It does not say whether fit time, hash writes, or the projection check sit inside `t_sample`. Provisional reading: `t_sample` is the sum of `time.perf_counter` intervals around those 1,000 `Φ` calls. Fit time and the projection check are outside the intervals. `T_rem = (N_float_remaining / 1000) · t_sample`. `N_exact` remaining after step 0 is declared 0, so the `T_O1 / n_O1` term is omitted. `N_float_remaining` is the declared upper count minus float64 continuations already performed, including O2.

## 10. Guard-failing edits inside the O6 and O7 loops

The scoreable-edit rule says an invalid edit is excluded from the loss, stays in the coverage denominator, and is not replaced. It does not say whether that edit's three forecasts are still computed. Skipping them would make the identity of the first 1,000 calls depend on the guard. Ruling: propagate every edit. On guard-failing edits, catch ValueError and non-finite results, count them, store them as null. The same failure on a scoreable edit is PIPELINE INVALID.

## 11. Propagation nest

The governing text calls the O6 sample order frozen and does not list the nest. Provisional nest, for O6 and again for O7:

1. folds in the v1.1 order AB→CD, CD→AB, AC→BD, BD→AC, AD→BC, BC→AD;
2. evaluation prefixes ascending;
3. continuation `u = 0..15`;
4. the baseline `Φ` for that prefix and continuation, on first use;
5. direction rows in draw order;
6. signs `+1` then `−1`;
7. `eps_syn` in the order 0.02, 0.05, 0.1, 0.25;
8. for each edit, actual, then `Pred_full`, then `Pred_μ`.

O6 fits every fold and writes `outputs/fit_freeze_O6.json` before any O6 edit propagation. A resolved fold whose fitted B misses `D Qᵀ` by more than `1e-9` stops as an O6 fixture failure before those propagations. Unresolved folds are not propagated. O7 writes `outputs/fit_freeze_O7.json` before O7 scoring propagations. Row order inside a weighted least-squares design does not change the minimum-norm solution of a fixed row multiset; the code stacks fit prefixes ascending and `u = 0..15`.
