Consult #36 - PRE-FREEZE REVIEW of the C-kappa ORACLE-ONLY SCOPE RECORD (follows your #35 READY WITH NAMED EDITS, raw sha 563e070c). Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

What is sent. BASE TEXT = scope record v1.1 (ckappa_oracle_scope_record_v1_1.md, sha256 e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c), IN FULL. AMENDMENT = v1.2 (ckappa_oracle_scope_record_v1_2.md, sha256 7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d), IN FULL; v1.2 = v1.1 plus its replacements, and v1.2 governs on conflict. v1 (1b450bcf...) is cited for lineage only. Planning note v1.3 (57899307...) carries your E35-1..12 verbatim. Both texts are transliterated to ASCII only (Greek letters spelled out, ** bold markers dropped); no content changed. Nothing has run; no code exists; no checkpoint is opened.

=== BASE TEXT: v1.1 (full) ===
# C-kappa oracle-only scope record v1.1 (DRAFT for Astra review. Not frozen, not approved, nothing run)

Constitutive agent, 2026-10-22. Additive. v1 (`ckappa_oracle_scope_record_v1.md`, sha256 `1b450bcf...`) is unchanged. v1.1 is a complete replacement text, and the freeze and Astra's review use v1.1 only.

It addresses:
- the Delegate's review `ckappa_oracle_scope_record_v1_adversarial_review_RD.md` (`6dbf3deb...`), accepted in full: S-M1-S-M6 and S-m1-S-m10;
- the Specialist's step-0 timing ruling.

It is governed by Astra #35 (`563e070c...`) and planning note v1.3 (`57899307...`, E35-1..12 verbatim).

Scope: oracle computations only. No checkpoint, weight file or training artifact is opened or loaded. No code exists yet. Every number below is fixed before any computation, and nothing executes until the manifest is sealed and the Research Lead's standing-approval application is filed.

Fix map

| Item | Fix | S |
| --- | --- | --- |
| S-M1 | Four transitions from stage 4 to stage 8. O1 reproduces all 256 terminal forecasts through Phi(b_a, u) | 1, 4 |
| S-M2 | Headroom is H*, the held-out loss of the *fitted* fixed-kappa comparator on the exact-filter control. H is descriptive only | 4 (O6), 5 |
| S-M3 + Specialist | No pre-freeze dry-run. Step 0 is a timing check after the seal, counted in the cap | 7 |
| S-M4 | kappa-component accuracy floor (L_full <= 1/2*L_mu), claim unit, quota, and fold-dependence stated | 6 |
| S-M5 | eps = 0.25 added. Counted sizes are {0.1, 0.25}; {0.02, 0.05} are descriptive | 4 (O6), 6 |
| S-M6 | Cross-stream marginal wording requires MARG to be available and to pass its own floors | 5, 6 |
| S-m1 | results.json at commit `5d9d8a7`. Beliefs are verified through forecasts, not matched directly | 1, 4 |
| S-m2 | Thresholds labelled as declared conventions. R_MARG added | 5 |
| S-m3 | R_G weighting stated | 4 (O5), 5 |
| S-m4 | Frozen three-band numerical-rank rule | 4 |
| S-m5 | Compute estimate corrected | 7 |
| S-m6 | One accounting rule for guard and validity failures. Pre-saturated units handled | 6 |
| S-m7 | PR #7 VAL membership tabulated as descriptive | 2 |
| S-m8 | MARG label | 3 |
| S-m9 | Fixtures O1, O2, O6, O7 before measurements O3-O5 | 4 |
| S-m10 | O7 is comparator-only, with a disclaimer. The symmetry reduction is reported, not assumed | 4 (O7) |
| E35-10 note | Threshold rationale no longer scaled on PR #5 | 5 |

## 1. World, chart and event order (frozen, inherited)
- World. W2 as in `TWOSTREAM_PROTOCOL_v1.md`, with frozen values in PR #4 `twostream_results_v1/results.json` at commit `5d9d8a7`. The local copy's sha256 is `bf2de92c...`; the freeze re-hashes it from that commit.
  - Uniform initial law on (X, Y).
  - Transition: X' = X(+)C(+)Dx, Y' = Y(+)C(+)Dy, with C ~ Bern(1/5), Dx ~ Bern(1/50) and Dy ~ Bern(1/40).
  - Readings come in the order X, Y, X, Y, X, Y, X, Y, each through a BSC(1/5).
  - h stores reading 1 in bit 0, and s = X + 2Y.
- Event order. The stage-k belief is the posterior after reading k and before the transition. For k < 8 a transition follows. Terminal forecasts come from the stage-8 belief.
- Stage k = 4 only. From the stage-4 belief to the stage-8 belief, the sequence is transition, reading 5, transition, reading 6, transition, reading 7, transition, reading 8. That is four transitions and four readings. Continuation u covers readings 5-8 (16 continuations), and h = a + 16*u. No stage is substituted.
- Chart. (mu_x, mu_y, kappa), with mu = 1 - 2m and kappa = 4c. The inverse chart is the one in `TWOSTREAM_PROTOCOL_v1.md` under "Coordinates".
- Phi(b, u). The terminal (q_X, q_Y, q_XOR) obtained by running the four-state filter from stage-4 belief b along continuation u. It is a ratio of linear functions of b.

## 2. Prefixes, orbits, folds and splits
- a in {0..15}, with b_a the exact stage-4 posterior.
- The flip group uses masks {0, 5, 10, 15}. Its orbits are A{0,5,10,15}, B{1,4,11,14}, C{2,7,8,13} and D{3,6,9,12}, and the fixture checks that the action is free.
- Folds. Six directed folds: AB->CD, CD->AB, AC->BD, BD->AC, AD->BC and BC->AD. That is three 2+2 splits, each run in both directions.
- Fold dependence. Each prefix is an evaluation prefix in 3 of the 6 folds, so folds are not independent. Continuation strings are shared between fit and evaluation (E35-8).
- Predictor-training splits, tabulated for every (a, u) and fold; descriptive only:
  - PR #5 S3 TEST: (a + u) mod 4 = 0.
  - PR #7 VAL: (a + u) mod 4 = 2 and u != (2 - a) mod 16, from PR #7 L55 and L131 as quoted by the Delegate. Whether F-TRAINED's readout training rejected VAL is UNVERIFIED.
  - Prefix holdout, continuation holdout and predictor-training holdout are reported separately.

## 3. Outputs and weights
- Groups:
  - MARG = the marginal-forecast component (q_X, q_Y);
  - XOR = the direct XOR forecast q_XOR;
  - ALL = all three outputs.
  - They are reported separately everywhere.
- Weights. w(a, u) = P(a*u), renormalized within the evaluated set. Directions, signs and edit magnitudes are weighted uniformly. Unweighted values are reported alongside.
- Loss. Weighted squared error summed within each group. Every bound names its target, norm, weighting and domain (E35-6).

## 4. Package: execution order O1 -> O2 -> O6 -> O7 -> O3 -> O4 -> O5
Fixtures come first. A failure in any fixture means STOP and report PIPELINE INVALID.

Rank rule (frozen, used throughout; E35-7). For singular values sigma_i/sigma_1:
- > 10^-6: resolved;
- < 10^-10: resolved zero;
- between the two: NUMERICALLY UNRESOLVED.

An unresolved rank in a fitted design (B or B_mu) makes that seed x fold cell UNRESOLVED; it is counted, not dropped.

- O1. World, chart and split fixtures.
  - Compute the 16 stage-4 beliefs in exact rationals.
  - Phi(b_a, u) must reproduce all 256 terminal forecasts stored in `results.json` exactly (rational equality, or the stored 50-digit truncation).
  - The chart must round-trip exactly, and the flip identities and P(h) invariance must hold.
  - Orbits A-D, and split counts of 64 TEST and 192 TRAIN.
- O2. Derivatives.
  - The closed-form L(a, u) = dPhi/d(mu_x, mu_y, kappa) must agree with central differences at step 10^-6 to a maximum absolute difference of 10^-8.
- O6. Positive implementation control (E35-5).
  - Synthetic state z = Q*D^-1(chart - chart_bar), where D is the P-weighted chart standard deviations over the 16 b_a and Q is an 8x3 matrix with orthonormal columns (seed 35006). The readout is Phi applied to the chart recovered from z.
  - Per fold, fit B (rank 3) and B_mu (rank 2, fixed kappa) by stacked Jacobian least squares over the fit prefixes and all continuations, with no ridge.
  - Edits: delta = eps*v, using 16 unit vectors v in R^8 (seed 35016), both signs, eps in {0.02, 0.05, 0.1, 0.25}, on the evaluation prefixes.
  - Predictions:
    - Pred_full = Phi(b_a + Bdelta) - Phi(b_a);
    - Pred_mu = Phi(b_a + B_mu-induced marginal change, kappa fixed) - Phi(b_a).
  - Expectations (frozen):
    - B = D*Q^T to <= 10^-9 maximum absolute difference;
    - Pred_full error <= 10^-9 on every valid edit.
  - Headroom quantity: H*_G(eps), the weighted held-out loss of Pred_mu against the control's actual response, pooled over folds. This is the gain actually available against the fitted comparator (S-M2). R*_G(eps) = H*_G divided by the weighted Sum||actual response||^2.
  - Label: oracle-scale under synthetic coordinates. The neural gain bound is the fitted comparator's own loss, which depends on the checkpoint (E35-9).
- O7. Restricted rival fixture (comparator only).
  - z = Q2*(standardized mu_x, mu_y), with Q2 8x2 drawn by seed 35007.
  - Forecasts are Phi at chart(mu_x, mu_y, g(mu_x, mu_y)), where g is the P-weighted least-squares quadratic fitted to the 16 reachable (mu, kappa).
  - Reported:
    - g's fitted coefficients, including whether flip symmetry reduces it to beta*mu_x*mu_y, as the Delegate derived by hand; this is reported, not assumed;
    - the stacked-Jacobian singular values, where rank 2 is expected under the rank rule and anything else is PIPELINE INVALID;
    - the O6-protocol gain over B_mu;
    - the reachable-set forecast error.
  - Disclaimer: this fixture is *one* explicit smooth two-coordinate system. It is not the reachable-set lookup; a smooth g of sufficient flexibility fits all 16 keys exactly. It cannot test or exclude the lookup rival, and no exclusion follows from any of its outcomes (E35-2).
- O3. Template geometry (descriptive).
  - Singular values per a of the stacked L for MARG (32x3), XOR (16x3) and ALL (48x3).
  - The principal angle theta between the kappa column and the marginal columns.
- O4. Oracle-unit perturbation validity.
  - Delta = D*s*r, with 64 unit vectors r in R^3 (seed 35004), both signs, s in {0.1, 0.25, 0.5}.
  - A perturbation is valid iff all four p >= 10^-6. Invalid perturbations are counted in the denominator and never replaced.
- O5. Naive kappa difference (descriptive only).
  - H_G(s) is the weighted mean of ||Phi(b_a + Delta) - Phi(b_a + Delta with kappa zeroed)||^2. R_G is H_G divided by the weighted mean of ||Phi(b_a + Delta) - Phi(b_a)||^2, with the S3 weights.
  - Not a headroom or a bound. It ignores the part of the kappa response that the comparator absorbs (~ H*sin^2theta to first order).

## 5. Headroom criterion at k = 4 (declared conventions, fixed before computation; E34-6, E35-7)
The thresholds are declared conventions. They are not derived from any checkpoint, and they cannot be changed after O6 is computed.
- ALL headroom met iff, at eps = 0.1 (the smallest counted size):
  - sqrtH*_ALL >= 1x10^-3;
  - R*_ALL >= 0.05;
  - at least 75% of O6 edits are valid.
- MARG claim available iff, at eps = 0.1:
  - sqrtH*_MARG >= 1x10^-4;
  - R*_MARG >= 0.02.
  - Otherwise the inference study may report MARG only descriptively.
- If ALL is not met: the result reads "HEADROOM NOT MET at k = 4". No mechanism-absence inference is drawn, no stage is substituted, and no inference spec is drafted without a new ruling.

## 6. Frozen now for the later inference study (not executed here; m2, E35-3, E35-4, E35-9)
- Edits.
  - Native post-reading-4 GRU hidden state h4 in (-1, 1)^8, Euclidean metric.
  - 16 unit directions per seed (PCG64 seed 36000 + seed_id), shared across prefixes and folds.
  - Both signs. eps in {0.02, 0.05, 0.1, 0.25}, absolute.
  - Counted toward the outcome: eps in {0.1, 0.25}. eps in {0.02, 0.05} are descriptive and serve as linear-regime references.
  - Descriptive edit families: kappa-directed, null(B), row(B), chord and equal-impact edits.
- Accounting (one rule).
  - An edit fails its guard if it moves any unit from |h_i| < 0.999 to |h_i| >= 0.999, or increases |h_i| for a unit already at |h_i| >= 0.999. Pre-saturated units are tabulated.
  - An edit is belief-invalid if b_a + Bdelta, or the B_mu counterpart, has any p < 10^-6.
  - Both kinds count in the denominator as failed predictions. They are never replaced or excluded.
  - A seed x fold x eps cell with more than 25% failures is UNRESOLVED.
- Per-seed pass, per group G, at each counted eps. All three must hold:
  - (a) the gain L_mu - L_full >= 1/2*L_mu, i.e. the full model removes at least half of the comparator's held-out loss (this is the kappa-component accuracy floor, S-M4);
  - (b) the normalized full error Sum||Pred_full - DeltaF||^2 / Sum||DeltaF||^2 <= 0.25;
  - (c) the rank rule is resolved for B and B_mu.
  - Pooling is over the 6 folds' evaluation sets, with each (fold, prefix) cell weighted by S3. The fold dependence is disclosed.
- Claim unit: the F-TRAINED seed (10).
  - POSITIVE (ALL): at least 8/10 seeds pass ALL at both counted eps.
  - NOT SHOWN: at most 2/10.
  - UNRESOLVED: more than 2 UNRESOLVED seeds.
  - MIXED: otherwise.
  - Cross-stream marginal wording requires MARG to be available under S5 *and* MARG POSITIVE by the same quota. Otherwise the result reads "ALL-group response prediction; marginal component not shown" (S-M6).
  - cand_final and F-INIT are descriptive (E35-10). The wording ceiling is Astra #35's closing paragraph.

## 7. Resources, step 0 and stop rules
- Cap: 1 CPU process, no GPU, a 4 GB address space and 10 cumulative wall-clock minutes, including setup, verification and step 0. No automatic retries.
- Step 0 (after the manifest seal and the filed application; S-M3): time O1, project the total from the declared propagation counts, and HALT and report if the projection exceeds 10 minutes.
- Paper estimate (UNVERIFIED):
  - O4: 16 x 16 x 128 x 3 ~ 9.8x10^4 propagations;
  - O6 and O7: 2 systems x 6 folds x 8 evaluation prefixes x 16 continuations x 32 edits x 4 eps x 2 predictions ~ 3.9x10^5;
  - O5, Jacobians and finite differences: ~ 1x10^5;
  - total ~ 6x10^5 four-state propagations, each a handful of 4x4 operations. That is expected to take well under 1 minute.
- Stop rules:
  - A fixture failure (O1, O2, O6, O7) means STOP and report PIPELINE INVALID, with no fix-and-rerun under this record.
  - Reaching the cap means STOP, with completed outputs preserved and the result reported as INCOMPLETE.
  - O3-O5 report only.
- Outputs: `results.json`; `REPORT.md`, which makes no interpretation beyond S5; a manifest with sha256 hashes of the code, the inputs and the outputs; and the run log. The report goes to the room and to Astra before any inference spec is drafted.

## 8. Claim ceiling
The package states oracle facts only: the event-order and forecast fixtures, derivatives, template geometry, perturbation validity, and headroom against the fitted fixed-kappa comparator at k = 4, plus the behavior of the two synthetic fixtures. It makes no neural, acquisition, mechanism, S12, S15, C4 or consciousness statement.

=== AMENDMENT: v1.2 (full) ===
# C-kappa oracle-only scope record v1.2: amendment to v1.1 (DRAFT for Astra #36. Not frozen, not approved, nothing run)

Constitutive agent, 2026-10-22 (ET). Additive. v1 (`1b450bcf...`) and v1.1 (`e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c`) are unchanged. v1.2 = v1.1 with the replacements and additions below; where they conflict, v1.2 governs. The freeze manifest will hash v1.1 and this file together.

It addresses the Delegate's delta check `ckappa_oracle_scope_record_v1_1_delta_check_RD.md` (`ff7b434a...`), accepted in full: D-1 to D-6. Governed by Astra #35 (`563e070c...`), E35-1..12 as quoted in planning note v1.3 (`57899307...`).

Nothing executes until the manifest is sealed and the standing-approval application is filed (v1.1 L11, L152 unchanged).

## D-1 (MAJOR). Separate oracle and neural perturbation units (E35-9)
- S4 O6, L85. Replace "eps in {0.02, 0.05, 0.1, 0.25}" with eps_syn in {0.02, 0.05, 0.1, 0.25}, in standardized synthetic-chart units (one unit of z = one P-weighted chart s.d. along a Q column). All O6 and O7 references to eps, H*_G(eps) and R*_G(eps) read eps_syn.
- S5, L115 and L119. Replace "at eps = 0.1 (the smallest counted size)" and "at eps = 0.1" with "at eps_syn = 0.1 (oracle-scale reference; not the neural achievable gain, which is the checkpoint's own L_mu; E35-9)".
- S6's eps stays the neural symbol, in absolute h4 units. No numerical equality between eps_syn and eps is implied, and S5 certifies no neural check (E35-9: "Oracle-only feasibility does not certify these neural checks.").

## D-2 (MAJOR). Frozen step-0 projection
Replace S7 L152 with:
- Step 0 (after the seal and the filed application). Run O1 in full (it is real work and is kept), recording its wall time T_O1 and its exact-rational propagation count n_O1. Then run the first 1,000 float64 O6 propagations in the frozen order (also kept as real work), recording t_sample.
- Let T_elapsed be the cumulative wall time so far, N_float the manifest's declared float64 propagation count remaining, and N_exact the declared exact-rational propagation count remaining (0 unless the code declares otherwise).
- T_rem = (N_float / 1000)*t_sample + N_exact*(T_O1 / n_O1).
- HALT and report if T_rem > (600 s - T_elapsed). No margin factor, no retry. The counts N_float, N_exact and n_O1 are written into the manifest before the seal.

## D-3 (MINOR). Neural headroom guard and seed roll-up
- (i) Neural headroom guard (E35-7). A seed x fold x eps x G cell whose held-out L_mu <= 10^-12*Sum||DeltaF||^2 reads NEURAL HEADROOM NOT MET. It stays in the denominator, is neither a pass nor a fail, and supports no mechanism-absence inference. L_mu / Sum||DeltaF||^2 is reported for every cell.
- (ii) Seed status for group G (pooled over folds, at each counted eps in {0.1, 0.25}):
  1. UNRESOLVED if any of its seed x fold x eps cells at a counted eps is UNRESOLVED (rank rule or more than 25% failures);
  2. else HEADROOM NOT MET if any such cell is NEURAL HEADROOM NOT MET;
  3. else PASS if (a), (b) and (c) hold at both counted eps;
  4. else FAIL.
- Package label for G, first match wins:
  1. NEURAL HEADROOM NOT MET if more than 2 seeds are HEADROOM NOT MET;
  2. UNRESOLVED if more than 2 seeds are UNRESOLVED or HEADROOM NOT MET combined;
  3. POSITIVE if at least 8/10 seeds PASS;
  4. NOT SHOWN if at most 2/10 seeds PASS;
  5. MIXED otherwise.
- The S-M6 marginal-wording rule (v1.1 L147) applies to these labels unchanged.

## D-4 (MINOR). Neural prediction definitions (E35-3)
Add to S6:
- Per seed and fold, B (8->3, rank <= 3) and B_mu (8->3 with the kappa row fixed at zero) are fitted by stacked Jacobian least squares, J(a, u) ~ L(a, u)*B, over the fit prefixes and all 16 continuations, with no ridge. Both are frozen and hashed before any evaluation-prefix edit is scored.
- DeltaF(delta, u) = F(h4 + delta, u) - F(h4, u), the checkpoint's actual output change with the readout unchanged.
- Pred_full(delta, u) = Phi(b_a + Bdelta, u) - Phi(b_a, u), with b_a + Bdelta meaning the inverse chart of chart(b_a) + Bdelta. Pred_mu is the same with B_mu.
- E35-3, verbatim: "Jacobian-fit results are reported separately and are not counted as independent replication of the intervention result."

## D-5 (MINOR). Failed edits in the loss sums
Replace v1.1 L135 with: A failed edit (guard or belief-invalid, under B or B_mu) is excluded from both L_full and L_mu and from Sum||DeltaF||^2, so both models are always scored on the same edit set. It counts toward the 25% UNRESOLVED rule and is never a pass. Failure counts by kind are reported per cell.

## D-6 (MINOR). Compute estimate
Replace S7 L153-L157 with: O6/O7 ~ 5.9x10^5 (three evaluations per edit: actual, Pred_full, Pred_mu), O5 ~ 3x10^5, Jacobians and finite differences ~ 1x10^5, O4 none. Total ~ 1x10^6 four-state propagations. Expected well under 10 minutes; UNVERIFIED until step 0.

## For Astra #36 (questions, not changes)
1. Floor (a) adequacy. With L_mu = E_s + K and L_full = E_s + e, floor (a) gives e <= 1/2K - 1/2E_s. At most about 50% of the kappa-part squared error (~71% RMS) may remain. Is 1/2 adequate, or should it be tightened (for example 1/4, <=50% RMS)?
2. Neural headroom. D-3(i) only catches float noise. Should a substantive neural floor be added (for example L_mu / Sum||DeltaF||^2 >= 0.02, matching R*_MARG)? Without one, a seed can pass by halving a comparator loss that was already negligible. Our lean: add it, declared now, at 0.02.

=== REVIEW CONTEXT ===
Delegate adversarial review of v1 (sha 6dbf3deb), briefly. MAJOR: S-M1 filter-composition error (wrong number of transitions stage 4->8); S-M2 headroom H did not match your separately fitted fixed-kappa comparator (H* is the right quantity); S-M3 a dry run was scheduled before freeze + application; S-M4 the inference floors allowed "two poor predictions"; S-M5 the eps range was small enough to collapse into the Jacobian test; S-M6 an ALL-group positive could be driven by XOR alone. MINOR: S-m1 results.json stores terminal exact rationals, not stage-4 beliefs (cite commit 5d9d8a7); S-m2 threshold rationale; S-m3 R_G weighting unstated; S-m4 no numerical-rank rule (E35-7); S-m5 compute undercounted; S-m6 guard vs belief-invalid accounting differed; S-m7 PR #7 VAL holdout tabulation; S-m8 MARG label wording; S-m9 package order; S-m10 O7 details/disclaimer.

Delegate delta check of v1.1 (sha ff7b434a): PASS WITH NOTES. All S-M1..6 resolved (S-M2 and S-M3 via D-1, D-2); S-m1..10 resolved (S-m5 partial). New items D-1 (MAJOR: one eps symbol for oracle and neural units, against E35-9), D-2 (MAJOR: step-0 projection undefined; exact-rational O1 timing unrepresentative), D-3 (neural low-headroom guard; seed roll-up precedence), D-4 (neural Pred_full with B frozen; E35-3 sentence), D-5 (failed edits in loss sums), D-6 (compute counts ~1e6). All six are addressed in v1.2. H* reading: H* is oracle-only and computed before any checkpoint, but it is NOT the neural achievable gain: O6 eps acts on standardized synthetic coordinates (a unit v moves the chart ~0.61*eps s.d. RMS), while neural eps acts on absolute GRU hidden units through the checkpoint's fitted B. So H*(eps_syn=0.1) is an oracle-scale resolvability reference; the neural floors are relative, so the neural achievable gain is the checkpoint's own L_mu. Floor arithmetic: write S = Sum||dF||^2, L_mu = E_s + K, L_full = E_s + e (shared non-kappa error E_s, kappa-part errors K and e). Floor (a) gives e <= K/2 - E_s/2: the full model must remove at least half the kappa-part squared error, i.e. at most ~71% RMS kappa error may remain; shared error makes (a) harder. At R*=0.05, E_s~0: K~0.05*S, (b) binds the comparator weakly and (a) requires e <= 0.025*S. It closes the "two poor predictions" case at the declared level but does not guarantee good kappa accuracy.

Research Lead rulings (binding): Step 0 (the timing check) runs only after the manifest seal and the filed standing-approval application. Cap: 1 CPU, no GPU, 4 GB, 10 cumulative minutes, no auto-retries, no checkpoint loading.

=== QUESTIONS ===
(1) Does the scope record (v1.1 + v1.2) conform to E35-1..12, especially E35-9 unit separation after the eps_syn rename?
(2) Is H* the right headroom basis, as an oracle-scale resolvability reference? Are the S5 thresholds acceptable as declared conventions?
(3) Is floor (a) (L_full <= L_mu/2) plus normalized error <= 0.25 adequate? Is the 1/2 enough, or tighten (e.g. 1/4)? Also rule on: the 8/10 seed quota with dependent folds; the roll-up precedence (UNRESOLVED > HEADROOM NOT MET > PASS > FAIL per seed; package NEURAL HEADROOM NOT MET if >2 seeds HEADROOM NOT MET, then UNRESOLVED, POSITIVE, NOT SHOWN, MIXED); and whether eps in {0.1, 0.25} escapes the linear regime.
(4) CNA question: the noise guard (L_mu <= 1e-12 * Sum||dF||^2) does not stop a seed passing by halving an already-negligible comparator loss. Should a declared neural floor L_mu / Sum||dF||^2 >= 0.02 be added now? Yes or no, and what value and rationale?
(5) Verdict: FREEZE, FREEZE WITH NAMED EDITS (give the edits verbatim, numbered E36-1..), or REVISE. List what must be in the freeze manifest.
