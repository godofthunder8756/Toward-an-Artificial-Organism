# C-κ oracle-only scope record v1.3: Astra #36 named edits E36-1..14 (DRAFT for freeze. Not sealed, nothing run)

Constitutive agent, 2026-10-22 (ET). **Additive.** Leaves unchanged: v1 (`1b450bcf…`), v1.1 (`e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c`), v1.2 (`7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d`). Source: Astra #36, `/workspace/astra_consult36_response.txt`, sha256 `c8342d5aa27c659dda5657e1e9ad70006a5e30759cc43eb25101d5546e756002`. Verdict (verbatim, L1): "FREEZE WITH NAMED EDITS for the oracle-only package. This does not clear checkpoint inference or establish a complete neural acceptance protocol."

## 0. Precedence (frozen)
**v1.3 (this file) > v1.2 > v1.1.** Where texts conflict, the higher one governs. Within v1.3, the verbatim E36 text in §1 governs over my supersession map (§2) and declared values (§3); if §2 or §3 is found to conflict with §1, §1 governs and the conflict is resolved additively before execution (Astra L162). Nothing in v1.3 authorizes the later inference study (E36-1).

## 1. E36-1..14, verbatim
Extracted by script from the raw file and each checked as an exact substring of it (`> ` prefix included). Astra's unquoted note directly following an edit is reproduced verbatim as "Note".

**E36-1.**

> "This freeze authorizes only the oracle package. Section 6 records prospective neural design commitments and does not constitute an executable inference protocol. No checkpoint is opened. The later inference specification must be reviewed and frozen before checkpoint inspection, including its absolute response-magnitude floor and complete numerical and outcome-accounting rules."


**E36-2.**

> "Use p for the four-state probability vector and theta=(mu_x,mu_y,kappa) for its chart. Phi(p,u) is a ratio of linear functions of p. Chart perturbations mean p'=inverse_chart(theta(p)+Delta). In O5, 'kappa zeroed' means setting the kappa component of Delta to zero while retaining the recipient's baseline kappa. The O5 contrast is descriptive and is not assigned an H*sin^2(theta) interpretation without a derivation for its exact target and weighting."


**E36-3.**

> "Fit B and B_mu by weighted least squares using ALL output components, fitting-prefix law weights and all continuations. Use the same fitted maps for ALL, MARG and XOR reporting. B_mu has its kappa row fixed to zero; neither fit is constrained to attain a specified rank. The minimum-norm solution convention and numerical solver are frozen in the manifest. O6's predicted-response identity is checked componentwise to maximum absolute error 1e-9 on valid edits."


**E36-4.**

> "For O6 and O7, an edit is scoreable only when the control's actual perturbed belief and both predicted perturbed beliefs satisfy the declared probability guard. Both models and response energy use exactly the same scoreable-edit mask. Invalid edits are not assigned zero error and are never replaced. Report raw-count and law-mass coverage for every fold and size. The oracle reference requires at least 75% coverage by both measures in every fold."

Note (verbatim, unquoted in source): For O7, an invalid baseline requires special handling under E36-6 rather than treating all of its edits as ordinary invalid perturbations.

**E36-5.**

> "Pool evaluated occurrences using their original w(a,u), with equal direction and sign weights, and normalize once over the pooled scoreable occurrences. Do not average separately normalized fold losses. With complete coverage, each history occurs in three evaluation folds, giving denominator three times total history mass, apart from the uniform edit factor. With incomplete coverage, report the retained mass and state that losses are conditional on the common scoreable-edit subset. H*, response energy and their ratio use identical masks and weights."

Note (verbatim, unquoted in source): This resolves both the fold-mass ambiguity and the conditional nature of D-5.

**E36-6.**

> "O7 is an exploratory restricted-comparator fixture, not a required behavioral negative control. Specify the polynomial basis, coefficient normalization and minimum-norm fitting convention for g. Evaluate its derivatives and finite predictions about its own baseline chart (mu_x,mu_y,g(mu_x,mu_y)); report disagreement with the true reachable oracle separately. Check baseline belief validity before derivative evaluation. Failure of the quadratic to define a valid baseline is reported as RESTRICTED COMPARATOR NOT ADMISSIBLE, not automatically as PIPELINE INVALID. It does not trigger refitting or replacement."


**E36-7.**

> "O7's two-coordinate construction implies Jacobian rank at most two. Exact rank two requires a separate argument for the specified outputs and domain. Resolved lower rank is reported, not automatically treated as an implementation failure. A resolved third direction contradicts the fixture's structural construction and requires an integrity diagnosis. Numerical ambiguity is reported as unresolved."

Note (verbatim, unquoted in source): O7 should not stop the rest of the package merely because an unconstrained quadratic is not a valid probability model everywhere. A demonstrated implementation contradiction should still stop it.

**E36-8.**

> "The rank rule includes equality cases in the unresolved band. An identically zero singular spectrum has numerical rank zero without forming sigma_i/sigma_1. Report sigma_1 as well as relative singular values; relative rank is not a sensitivity measure. Freeze the treatment of zero response energy and numerical boundary cases before execution. Undefined ratios are not replaced by zero or counted as passing thresholds."

Note (verbatim, unquoted in source): Use a declared numerical boundary band for S5 comparisons, and keep boundary outcomes distinct from HEADROOM NOT MET. Do not improvise a tolerance after seeing a value.

**E36-9.**

> "H* is the synthetic comparator loss and ideal improvement headroom when the full synthetic predictor is exact. Report the actual measured gain separately. For a neural checkpoint, L_mu is an upper bound on possible squared-error improvement, not a guarantee of attainable gain. The condition L_full<=L_mu/2 concerns total comparator prediction error and is not interpreted as a bound on a separately identified kappa-error component."


**E36-10.**

> "The prospective neural substantive-headroom condition is pooled L_mu/S>=0.02 for each counted size and output group. It is a declared relative-effect convention. Together with halving L_mu it requires improvement of at least 0.01*S. A separate absolute response-magnitude floor remains required before inference. Foldwise headroom is reported but does not independently determine the seed's headroom status."


**E36-11.**

> "For each output group, report disjoint seed counts p, f, u and h for PASS, verified FAIL, UNRESOLVED and HEADROOM NOT MET. More than two unresolved seeds gives UNRESOLVED; otherwise more than two headroom-limited seeds gives HEADROOM NOT MET; otherwise more than two combined gives UNRESOLVED for insufficient evaluable seeds. With those checks satisfied, p>=8 gives POSITIVE. NOT SHOWN requires p+u+h<=2. MIXED requires 3<=p and p+u+h<8. Remaining cases are UNRESOLVED because unavailable comparisons can change the outcome category. No unavailable comparison is counted as verified failure."

Note (verbatim, unquoted in source): An absolute low-response outcome can be included within h, with its reason retained separately.

**E36-12.**

> "The counted neural edit magnitudes are finite intervention commitments, not proof of nonlinearity. Report actual finite responses, Jacobian predictions and their discrepancy at every declared size. Agreement in a linear regime is not counted as independent mechanistic replication of the Jacobian fit. No magnitude is substituted after inspection."


**E36-13.**

> "Step 0 performs O1 and O2 before sampling O6 work. The first 1,000 sampled O6 propagations are retained and not recomputed for timing. Remaining propagation counts use frozen scheduled upper counts with completed work subtracted. The projection is a heuristic that omits or separately estimates non-propagation overhead; it is not a runtime bound. A projection-triggered stop is distinguished from reaching the hard cap."

Note (verbatim, unquoted in source): The current amendment samples O6 before completing O2, despite specifying derivative validation before O6. That ordering needs correction.

**E36-14.**

> "The cumulative wall-clock interval starts before interpreter imports and setup and includes final serialization and report writing. Enforce the ten-minute limit independently of the throughput projection. Preserve completed outputs on stopping. The pre-execution manifest is immutable; output hashes and run accounting are written to a separate post-run index referencing that manifest."


## 2. Supersession map (what in v1.1/v1.2 each edit replaces)
| v1.1/v1.2 text | Edit | Now reads |
| --- | --- | --- |
| v1.1 L44, "ratio of linear functions of b" | E36-2 | Φ(p,u) is a ratio of linear functions of p, not of the chart θ. Notation: p = four-state vector, θ = (μ_x, μ_y, κ), perturbed p' = inverse_chart(θ(p)+Δ). |
| v1.1 O5 L110–111, "≈ H·sin²θ" | E36-2 | Withdrawn. O5 is descriptive with no H·sin²θ reading. "κ zeroed" = κ component of Δ set to 0, baseline κ kept. |
| v1.1 O6 L84 "B (rank 3) and B_μ (rank 2)"; v1.2 D-4 "rank ≤ 3" | E36-3 | Weighted LS on ALL outputs, fit-prefix law weights, all continuations; same maps for ALL/MARG/XOR; no rank constraint; minimum-norm solver frozen in manifest. Applies to O6 and O7; carried as a design commitment for §6. |
| v1.1 §4 O6 validity; v1.2 D-5 | E36-4, E36-5 | One common scoreable-edit mask: actual perturbed belief and both predicted beliefs must pass p ≥ 10⁻⁶. Losses and S on the same mask; count and law-mass coverage per fold and size; ≥ 75% by both in every fold for the oracle reference. v1.1 §5's "≥ 75% of O6 edits valid" is replaced by this per-fold rule. |
| v1.1 §6 L141 pooling; v1.1 O6 L92 "pooled over folds" | E36-5 | Pool occurrences with original w(a,u), normalize once over pooled scoreable occurrences. No averaging of fold-normalized losses. Losses are conditional on the common mask; retained mass reported. |
| v1.1 O7 L99 "rank 2 expected … anything else is PIPELINE INVALID"; v1.1 O7 as a fixture whose failure stops | E36-6, E36-7 | O7 is exploratory. Invalid quadratic baseline → RESTRICTED COMPARATOR NOT ADMISSIBLE (no stop, no refit). Rank ≤ 2; lower resolved rank reported; a resolved third direction → integrity diagnosis; ambiguity → unresolved. A demonstrated implementation contradiction still stops (Astra L109). Execution order O1→O2→O6→O7→O3→O4→O5 unchanged. |
| v1.1 L68–73 rank rule | E36-8 | Equality at 10⁻⁶ or 10⁻¹⁰ falls in the unresolved band. σ_1 = 0 exactly → rank 0 without forming ratios. σ_1 always reported. |
| v1.1 L93 / v1.2 D-1 "neural achievable gain" | E36-9 | Replace with: "for a neural checkpoint, L_μ is an upper bound on possible squared-error improvement, not a guarantee of attainable gain." O6 reports measured gain H\* − L_full alongside H\*. |
| v1.2 Astra question 1 (my "≈71% RMS κ error" reading, and the Delegate's E_s/K/e arithmetic) | E36-9 | **Withdrawn.** Exact identity (Astra L48): L_μ − L_full = 2⟨r_μ, d⟩ − ‖d‖². Floor (a) halves total comparator error; it is not a κ-component bound. L_full ≤ L_μ/2 kept, not tightened. |
| v1.2 D-3(i) noise guard (10⁻¹²) | E36-10 | Substantive pooled floor L_μ/S ≥ 0.02 per counted size and group (ALL and MARG). The 10⁻¹² band is retained only as a reported numerical boundary marker; it no longer defines headroom status. Absolute response-magnitude floor is still required before inference (E36-1). |
| v1.2 D-3(ii) seed roll-up and package labels | E36-11 | Replaced in full by E36-11's disjoint p/f/u/h counts and ordering. An absolute low-response outcome counts in h with its reason kept. |
| v1.1 §6 L129–130 counted ε as "beyond linear-regime references" | E36-12 | Counted sizes are finite commitments, not evidence of nonlinearity. Finite response, Jacobian prediction and discrepancy reported at every size. |
| v1.2 D-2 step 0 | E36-13 | Order: O1, then O2, then the first 1,000 O6 propagations (retained, not recomputed). Remaining counts are frozen scheduled upper counts minus completed. Projection is a heuristic, not a bound; overhead estimated separately. A projection stop is reported as PROJECTION HALT, distinct from CAP REACHED. |
| v1.1 §7 L151 cap; v1.1 §7 L162 manifest with output hashes | E36-14 | Clock starts before interpreter imports. Hard cap enforced independently of the projection. Manifest immutable; output hashes and run accounting go in a separate post-run index referencing the manifest sha. |
| v1.1 §5 at ε_syn = 0.1 | Astra L30 | Other ε_syn sizes reported but never replace a failed reference. |

## 3. Values declared now (required by E36-3, E36-6, E36-8 and Astra L115; frozen before execution)
Implementation may not change these. If one proves unworkable, it is resolved additively before execution (Astra L162).
- **§5 numerical boundary band.** A §5 statistic x compared with threshold t is BOUNDARY if |x − t| ≤ 10⁻⁶·t. BOUNDARY is reported as its own outcome, distinct from HEADROOM NOT MET, and is not a pass.
- **Zero response energy.** If S = 0 exactly in a pooled cell, R\* and L_μ/S are UNDEFINED. The oracle cell reads ZERO RESPONSE (low sensitivity), not a pass, not PIPELINE INVALID, and no ratio is replaced by 0. For §6 it is an h outcome with reason "zero response".
- **Solver.** All least-squares fits use `numpy.linalg.lstsq(A, y, rcond=None)` (SVD, minimum-norm) on the √w-weighted system, float64. B_μ is fitted on the reduced 2-column chart design (κ row fixed at 0).
- **O7 basis.** g(μ_x, μ_y) = c₀ + c₁μ_x + c₂μ_y + c₃μ_x² + c₄μ_xμ_y + c₅μ_y², raw (unscaled) monomials, P-weighted least squares over the 16 reachable (μ, κ), minimum-norm via the solver above. Baseline validity (p ≥ 10⁻⁶ at (μ_x, μ_y, g)) is checked per prefix before derivatives.
- **RNG and Q.** `numpy.random.Generator(PCG64(seed))`. Q (8×3, seed 35006) and Q₂ (8×2, seed 35007): one `standard_normal((8, k))` draw, row-major; reduced `numpy.linalg.qr`; columns sign-flipped so diag(R) > 0. Directions (O6 seed 35016, O4 seed 35004, §6 seed 36000+seed_id): one `standard_normal((n, dim))` draw, each row divided by its Euclidean norm; both signs taken as +v then −v in row order.
- **Threads.** One process, `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1`, CPU affinity pinned to one core, `RLIMIT_AS` = 4 GiB.

## 4. Draft MANIFEST CONTENTS checklist (mirrors Astra #36 §6, L149–160, items verbatim)
Each item is filled by the implementer and checked before sealing. "Source" says where the frozen value already lives.

1. [ ] **Full hashes of the base scope, amendment and E36 correction file, with an unambiguous precedence rule.**
   - Source: sha256 of v1.1, v1.2, this file; precedence from §0.
2. [ ] **The exact W2 source commit, certificate, protocol and all implementation files.**
   - Source: PR #4 `results.json` @ `5d9d8a7` (re-hashed from the commit; local copy `bf2de92c…`), certificate, `TWOSTREAM_PROTOCOL_v1.md`, every implementation file with sha256.
3. [ ] **The chart notation, four-transition event order, output groups and derivative method.**
   - Source: v1.1 §1 (four transitions), §3 groups; O2 closed form + central differences at 10⁻⁶; notation per E36-2.
4. [ ] **Exact folds, weights, pooling formulas, validity masks and coverage rules.**
   - Source: v1.1 §2 folds; v1.1 §3 weights; E36-4/E36-5 mask, pooling and ≥75% count and mass coverage per fold.
5. [ ] **O6 and O7 state reconstruction, fitting objectives, polynomial basis and solver conventions.**
   - Source: v1.1 O6/O7 constructions; E36-3 objectives; §3 basis, solver and minimum-norm convention.
6. [ ] **RNG algorithm, seeds, draw order, direction normalization, QR procedure and sign convention for Q and Q2. Seeds alone are insufficient.**
   - Source: §3 RNG, draw order, normalization, QR and sign rule; seeds 35004, 35006, 35007, 35016, 36000+seed_id.
7. [ ] **All thresholds, units, numerical bands, zero-denominator rules and fixture expectations.**
   - Source: v1.1 §5 and E36-10 thresholds; ε_syn vs ε units (v1.2 D-1); §3 boundary band and zero-denominator rule; E36-8 rank rule; O1/O2/O6 fixture tolerances (exact; 10⁻⁸; 10⁻⁹).
8. [ ] **Which outcomes stop execution, which merely describe a restricted comparator, and which determine S5.**
   - Source: Stops: O1, O2, O6 failure or a demonstrated O7 implementation contradiction → PIPELINE INVALID. Descriptive only: O7 admissibility and rank, O3–O5. Determines §5: O6 at ε_syn = 0.1.
9. [ ] **Scheduled operation-count definitions, timing projection, execution order and hard-cap enforcement.**
   - Source: Per-stage scheduled upper counts (≈1×10⁶ total, v1.2 D-6); E36-13 projection; order O1→O2→O6→O7→O3→O4→O5; E36-14 hard cap from before imports.
10. [ ] **Runtime versions, numeric precision, CPU affinity, thread settings and memory limit.**
   - Source: Python/NumPy versions, float64 throughout (exact rationals in O1), §3 affinity, threads and memory.
11. [ ] **Output schema and paths, partial-output behavior, and the separate post-run hash index.**
   - Source: `results.json`, `REPORT.md`, run log; partial outputs kept on any stop; separate post-run hash index (E36-14).
12. [ ] **The Research Lead's application of the standing approval to this exact oracle-only scope.**
   - Source: Filed by the Specialist after sealing; references the manifest sha.

## 5. Claim ceiling
Unchanged from v1.1 §8 and Astra L164: oracle-only. No neural, acquisition, S12, S15, C4 or consciousness finding. No checkpoint is opened. Nothing runs before the manifest is sealed and the application is filed.
