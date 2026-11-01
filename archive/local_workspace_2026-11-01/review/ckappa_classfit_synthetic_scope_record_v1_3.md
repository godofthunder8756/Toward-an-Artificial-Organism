# C-κ class-fit validation package: synthetic-only scope record v1.3 (consolidated, after Astra #39)

**Status: SCOPE APPROVED FOR FREEZE PER ASTRA #39 (E39-1), PENDING ANNEX COMPLETION AND INDEPENDENT PRE-SEAL CONFORMANCE REVIEW. NOT SEALED. NOTHING RUNS.**

*Why this wording.* The requested line was "SCOPE FROZEN PER ASTRA #39 PENDING ANNEX CONFORMANCE REVIEW". #39 does not quite support it, so this line follows #39's own words:
- #39 says the design "is approved for freeze with the Consult #39 amendments" (E39-1). It does not say the design is frozen.
- "The Research Lead completes the frozen bundle" (#39 L169).
- The pre-seal review checks the whole bundle's implementation details, not only an annex (#39 L168, E39-1).

Research Delegate (Track A), 2026-10-23 (ET). This is a new file.
- v1.2 (`79ea0eeb1658e7d265aae3a68d31c6fb385ceab23a91eb654fee61a4aa64561c`) and its NOTE_1 (`832d9bcfb5855ad20abf242888bfda0f372f3ad83e48f197005e3d37905033b9`) are not edited.
- v1.3 is a complete replacement text that consolidates v1.2, NOTE_1 and E39-1 to E39-11.
- **Implementation annex:** `review/ckappa_classfit_implementation_annex_v1.md`. It is referenced here by path only (scheme in C9.6).

**The design is fixed (#39 L175).** "A proposed change to the estimator, controls, masks, thresholds, directions, sizes, caps or claim ceiling would require a new ruling." v1.3 changes nothing in those categories beyond what #39 orders.

I executed nothing: no oracle, solver, fit, simulation, checkpoint or memory measurement. "RD arithmetic" means my own arithmetic on committed numbers in the PR #13 outputs at `14376f38`. Every derived expectation is **UNVERIFIED** until an approved, sealed run. Nothing in this file authorizes execution. #39 authorizes no synthetic pilot and no checkpoint inspection (#39 L237).

**Selected design (E38-1, unchanged).**
- The confound treatment is descriptive-only.
- Each flip class gets plain, separately fitted maps: a full unrestricted 3×8 B and a fixed-κ [A; 0], where A is an unrestricted 2×8 matrix.
- The global comparator is one pair of maps per fold.
- All seven systems are included.
- There is no augmented basis, no shared e, no tied-bilinear fit and no empirical neural floor.

**Systems**

| Name | Role |
|---|---|
| SYS-O6 | Existing affine exact-filter control (implementation identity) |
| SYS-PC | Sign-dependent positive control (identities, plus the separate HEADROOM label). Affine only within a sign branch. |
| SYS-FK | Genuinely fixed-κ control: globally zero κ on product-chart designs |
| SYS-NC1 | **Varying-κ two-coordinate confound** (O7 lookup), **nonlinear** in z. Not a fixed-κ control and not a gain-negative control. |
| SYS-NC2 | Affine symmetry-breaking two-coordinate confound (descriptive) |
| SYS-NC3 | Cubic two-coordinate confound, **nonlinear** in z (descriptive) |
| SYS-LIM | Orbit-indexed limit control, REPORTED ONLY. Affine only within a threshold branch. **Not** a two-coordinate system (E39-11). |

"NC" is a legacy label only. Stage labels and system labels are kept apart by C8.0.

## Change log relative to v1.2 + NOTE_1

Each entry cites its #39 source. v1.2's own change log (relative to v1.1) remains in v1.2 and is not repeated here.

**Adopted**
1. **NOTE_1 N1** (premise rows for D6 and SYS-NC1 global) is adopted into C3.3(b), C4.4 and C4.5, with diagnostic roles unchanged (E39-8; #39 L44).
2. **NOTE_1 N2** (rank categories) is adopted as C3.3(a′). The empty design is UNAVAILABLE and kept separate from a nonempty zero matrix (E39-8; #39 L46–59).
3. **NOTE_1 N3** is adopted as clarified: an exact-rational ΣP = 1 assertion; c₂ = ρ_NC1/sqrt(float(P_sum_exact)); a frozen summation order for ρ and c₃; failure stops with no rescaling (E39-9; #39 L61–70). See C4.4.R.

**Q-R rulings applied**
4. **Q-R1.** D7 INVESTIGATE is non-stopping and outside VALIDATION and HEADROOM, retained prominently, and accompanies any later neural decision (E39-8; #39 L15). See C4.5, C7.4, C10.13.
5. **Q-R2.** SYS-FK class zero-gain is checked per fold/class/group/size, with no pooled replacement (#39 L16). See C4.3.
6. **Q-R3.** SYS-O6 and SYS-FK rank lapses prevent VALIDATION MET. Resolved-lower and unresolved rank are kept distinct (E39-8; #39 L17). See C7.2.
7. **Q-R4, narrowed.**
   - The guard-consistency stop applies only to actual-recovery predictors.
   - SYS-PC global equality is checked where both global predictions are valid, and its invalid predictions are coverage exclusions.
   - A guard mismatch is reported as an operational inconsistency, with margins and residuals (E39-4; #39 L18–40).
   - See C4.2(g), C5.3(c), C10.11.
8. **Q-R5.** Unweighted B3 stacks are accepted. The band result is UNRESOLVED-B3: never a passed guard, no automatic stop, and it does not by itself make a map unavailable (E39-8; #39 L19). See C3.11.
9. **Q-R6.** Per-system baselines and no deduplication are accepted. The P0 dependency is corrected, and identity checks stream during evaluation (E39-2, E39-3; #39 L20, L126–145). See C8.1, C5.3(c).

**Corrected**
10. **Stage order.** S3 is now system construction (including the SYS-NC1 refit and the L, J and G tables) and S4 is P0, swapped from v1.2. Fits come at S5 and evaluation, with streaming checks, at S6 (E39-2). C8.0 adds label hygiene.
11. **Streaming identity checks, tested-edit counts and NOT EVALUATED for empty domains** (E39-3). See C5.3(c), C7.1, C7.2.
12. **HEADROOM eligibility gates restored:** maps, fits, reference-size coverage per fold/class, positive denominator, S > 0 (E39-5; #39 L147–156). See C7.3.
13. **C7.2 wording.** Confound gains and descriptive expectations stay outside VALIDATION; mandatory integrity checks, including SYS-NC1 P0, stay mandatory (E39-5; #39 L158).
14. **Loss accounting.** 5,040 is replaced by **16,128 mode-indexed base loss records**, and stored aggregates are enumerated separately (E39-6; #39 L96–114). See C3.6(c), C8.3.
15. **Single-prefix local fits disabled** (E39-6; #39 L116). See C3.8.
16. **One terminal accounting category per scheduled call,** with precedence prior stop > system inadmissibility > prefix void > unavailable map. An inadmissible system gets no fits or propagations. After forced termination, counts beyond the last durable record are UNKNOWN (E39-7; #39 L118–120). See C3.9, C8.4.
17. **Artifacts.** The 21 core files are kept. The wrapper post-run index and logs are listed separately (#39 L122; E39-10). See C8.3 and annex A5.
18. **C9.5 "no value is set" corrected:** frozen-rule computed values are permitted execution outputs (E39-9; #39 L72).
19. **Readout claims made system- and domain-specific** (C4.R). SYS-LIM is no longer grouped under "two-coordinate mediation" in C6 or in the E37-7 binding note (E39-11; #39 L74).
20. **P0 applicability domains and omitted voided pairs** (E39-10). See C4.0 and annex A7.
21. **Reused arrays** are loaded as authenticated existing arrays, with conventions in the annex (E39-10; #39 L171). See C5.2 and annex A1.
22. **Memory estimate** moved to the annex (A4), covering every component #39 L173 names (E39-10).

**Added**
23. **E39-1 to E39-11** quoted verbatim, with compliance tables and the other binding #39 text (§2c).
24. **Annex reference scheme** (C9.6) and the fixed-design statement (C9.7; #39 L175).

**Closed**
25. **Q-R1 to Q-R6** are closed by #39 (§11).

## 0. Sources, hashes and precedence

| Source | sha256 | Role |
|---|---|---|
| `/workspace/astra_consult39_response.txt` (Astra #39 raw, 237 lines, E39-1..11) | `e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482` | **Governs over everything**, including this file and any summary of #39 |
| `/workspace/astra_consult38_response.txt` (Astra #38 raw, 385 lines, E38-1..16) | `87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5` | Governs below #39 |
| `/workspace/astra_consult37_response.txt` (Astra #37 raw) | `ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2` | Governs below #38 |
| `review/ckappa_classfit_synthetic_scope_record_v1_2.md` | `79ea0eeb1658e7d265aae3a68d31c6fb385ceab23a91eb654fee61a4aa64561c` | Superseded base text (unchanged) |
| `review/ckappa_classfit_synthetic_scope_record_v1_2_NOTE_1.md` | `832d9bcfb5855ad20abf242888bfda0f372f3ad83e48f197005e3d37905033b9` | Superseded additive note (unchanged); N1–N3 adopted |
| `review/ckappa_classfit_implementation_annex_v1.md` | by path only (C9.6); sha in the posted report and the manifest | Implementation annex (E39-1, E39-10) |
| `/workspace/astra_consult36_response.txt` (Astra #36 raw, E36-1..14) | `c8342d5aa27c659dda5657e1e9ad70006a5e30759cc43eb25101d5546e756002` | Governs the inherited oracle definitions, below #37 |
| `review/ckappa_classfit_synthetic_scope_record_v1_1.md` | `97165ac6cb90fbd9433fa3a8777c017319b7cefc88b6ed45d9f902f3aaca23aa` | Superseded base text (unchanged) |
| `review/ckappa_classfit_synthetic_scope_record_v1_1_NOTE_1.md` | `00ec1902fcd16f2d722447c8f52d67123a5eb305bbe0c73c3657afb73b531aea` | Superseded additive note (unchanged); item 3 withdrawn |
| `review/CKAPPA_SCOPE_GOVERNING_SET_RL.md` | `6a5e0f24995a1349664349713e1ee0a550267ac06ab0e4b462b121d931c15c63` | Oracle governing set |
| `review/CKAPPA_SCOPE_RL_RULING_B2_B3.md` | `6d75918f7cc2ae06386d80400645345539d7e6f0d893f105bbb7fa0b2c563edd` | B2/B3 |
| `review/ckappa_oracle_scope_v1_4_N_closure_note.md` | `4ad1d217aaab0bd45d2be6fd3e24872a4b22407d0c8abc2fa36a5a1ac7c45c9c` | B1, 595 s, N-b |
| `review/ckappa_oracle_scope_record_v1_4_N.md` | `3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359` | N1–N4, n1–n5 |
| `review/ckappa_oracle_scope_record_v1_3_E36.md` | `f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5` | E36 verbatim, §3 values |
| `review/ckappa_oracle_scope_record_v1_1.md` | `e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c` | World, folds, O6/O7 definitions |
| `review/ckappa_oracle_results_review_RD.md` | `617e983d96c0487f7345fdaae83fe972cf9d5ffe5102f84a4b37e94ad73f64ba` | M-1 |
| PR #13 scratch clone `/workspace/scratch/pr13` @ `14376f38fe09157eef85bfac1cc4a4433d49bebc` | code: `stages.py` 936d3378, `linalg_fit.py` de6f4034, `geometry.py` 117e98e9, `world.py` 3d235fca, `pinned.py` 03c55323. Outputs: `stage_O1.json` 794746a7, `stage_O7.json` 994dda0a, `results.json` 6adb5de2, `fit_freeze_O6.json` b6f817c8, `fit_freeze_O7.json` 347bcd51 | Read only |

**Precedence (proposed for freeze).**
1. Astra #39 raw text.
2. Astra #38 raw text, where #39 does not revise it.
3. Astra #37 raw text, where #38 and #39 do not revise it.
4. E36 raw text.
5. This record, then the implementation annex, which may not change the design (C9.7).
6. The oracle governing set. It supplies every inherited definition that this record does not replace.

A summary of #38 or #39 that departs from the raw text, including the Specialist's or the Research Lead's, has no standing. See §12.3.

**Development-informed disclosure.**
- #37 L162: "This is development-informed work: O7 and its cancellation are already known. New freezing does not make them unseen."
- Q, Q₂ and the directions are reused per #38 Q10, and that reuse is likewise development-informed.

## 1. Claim ceiling (C1)

E38-15, verbatim (also quoted in §2b):

> "This package tests implementation identities, synthetic response headroom and limitations of declared intervention-prediction models on specified synthetic systems. It establishes no result about trained GRUs and answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY. Confound gains do not identify an independent covariance register or exclude two-coordinate mediation or reachable-set lookup implementations. Failure of a class-conditioned criterion does not exclude nonlinear, prefix-dependent or orbit-dependent covariance codes. No result establishes acquisition, recurrent-transition-specific use, necessity, irreducible joint state, C4, C5, consciousness, autopoiesis or life."

- **C1.1 Synthetic-only.** The package concerns declared synthetic systems only.
- **C1.2 No checkpoint.** No checkpoint or weight file is opened (E37-9, E38-16).
- **C1.3 Q-tags.** None of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY is answered, and the four stay separate. The package's only forward role is to inform whether a later, separately frozen **Q-CAUSE** measurement specification is warranted (#37 L164). That is a decision input, not a Q-CAUSE result.
- **C1.4 Neural ceiling.** E37-10 (§2) plus the #38 L202 sentence, which must be retained explicitly:

  > "Failure of the declared class-conditioned criterion does not exclude orbit-dependent covariance codes, including codes whose local coordinate relation differs on held-out orbits."

- **C1.5 No consciousness, C4, C5, autopoiesis/"autopoietic", life/"alive"** claim is made or implied.
- **C1.6 Unchanged by #39.** "The claim ceiling remains E38-15, including no result about trained GRUs, no answer to any of the four Q-tags, no exclusion of general two-coordinate or lookup implementations, and no consciousness, C4/C5, autopoiesis or life claim. The explicit limitation concerning orbit-dependent codes also remains." (#39 L235)

## 2. Astra #37 items: verbatim text and compliance map (kept from v1.1)

The E37 quotes are carried over unchanged. Where #38 or #39 revises the mapped clause, the later rule governs, as shown in §2b and §2c.

Each E37 item is quoted as an exact substring of the raw file, with the raw-file line in brackets.

**E37-1** [L170]
> "The completed oracle package is closed with ALL = MET and MARG = AVAILABLE under its frozen synthetic embedding, edits, weights, comparator and thresholds. These labels establish oracle-scale headroom only. They establish no result about GRU computation, acquisition, causal use, necessity, S12 or S15."

*Binding here:* C1.2 and C10.3. No oracle label is used as neural evidence or as a neural floor.

**E37-2** [L174]
> "The sealed manifest, code and outputs remain unchanged. Stale phase, version and sealing-description strings are documented additively. Runtime versions are described as asserted at preflight; elapsed-time and memory claims identify their recorded sources. The frozen exact-zero flag is retained and distinguished from the analytic symmetry statement."

*Binding here:* C9.4. The new package records observed runtime versions as observations, not pinned constants. It does not hard-code phase or seal strings, and it names the source of every timing or memory figure. Exact-zero flags are kept separate from tolerance checks (C5.5).

**E37-3** [L178]
> "O7's zero gain follows from its symmetry-preserving global least-squares construction: complete flip-orbit fits, invariant continuation weights, a constant marginal-state map, and the declared odd-in-each-marginal lookup. It is not evidence that two-coordinate systems generally lack kappa-row gain. Comparator loss divided by response energy is not described as an orthogonal allocation of that energy."

*Binding here:* C5.4 and C10.2. Every R-type ratio is worded as "comparator squared prediction error divided by actual response energy" (#37 L26).

**E37-4** [L182]
> "Failure of the global-map intervention criterion means that the declared criterion was not met. It does not establish absence of covariance sensitivity, absence of a global direction, or absence of a nonlinear or prefix-dependent coordinate relation. The prospective S6 design does not proceed to checkpoint inference unchanged."

*Binding here:* C10.1 (negative wording) and C1.2 (no checkpoint).

**E37-5** [L186]
> "The next candidate model uses four flip-class-conditioned maps while retaining whole-orbit outer holdout. Class labels are defined by the unique flip taking the smallest representative of each orbit to the prefix. Full and fixed-kappa maps are separately fitted within each class using fitting prefixes only. The supplied class labels and increased model flexibility are disclosed."

| Requirement | Clause |
|---|---|
| four flip-class-conditioned maps | C3.2 |
| whole-orbit outer holdout retained | C3.1 (the six v1.1 folds, unchanged) |
| class = unique flip taking the smallest orbit representative to the prefix | C3.1 table |
| full and fixed-κ maps fitted separately within each class, on fitting prefixes only | C3.2, C3.5 |
| supplied labels and added flexibility disclosed | C3.7 |

*Note (#38):* E38-1 selects plain, separately fitted per-class maps, which satisfies E37-5 literally. v1.1's B-repaired departure is withdrawn.

**E37-6** [L190]
> "The synthetic validation includes an explicitly defined sign-dependent positive control and a genuinely fixed-kappa control. Positive-control expectations are derived before execution. Class-dependent response generation is implemented by the synthetic system's declared state and readout, not supplied only to the analysis."

| Requirement | Clause |
|---|---|
| explicitly defined sign-dependent positive control | C4.2 (system SYS-PC, "PC±") |
| genuinely fixed-κ control | C4.3 (system SYS-FK, "FK") |
| PC expectations derived before execution | C4.2, derivations D1–D3 (written here; UNVERIFIED; first-order qualification per E38-2) |
| class-dependence generated by the system's own state and readout | C4.2: the readout computes sign(ψ₁ψ₂) from the state itself; the analyst's class label does not enter response generation |

**E37-7** [L194]
> "Smooth two-coordinate lookup systems are confound controls, not required gain-negative controls. A kappa-row gain in such a system is compatible with two-coordinate mediation. Neither the global nor the class-conditioned gain statistic identifies an independent covariance register or excludes the reachable-set lookup rival."

*Binding here:* C4.4 and C6. SYS-NC1–NC3 have **no** gain-must-vanish criterion, and neither does SYS-LIM, which is not a two-coordinate system (E39-11). Their gains are reported, not passed or failed. No floor and no augmented basis is used (E38-1). Exclusion of two-coordinate mediation would need the different test in #37 L142, which is out of scope.

**E37-8** [L198]
> "The new package stores fitted matrices as well as their hashes, numerical ranks, class and orbit losses, and the weighted normal-equation terms used to assess cancellation. Per-prefix local fits and kappa-row norms are diagnostic only and do not replace held-out finite-intervention prediction."

| Requirement | Clause |
|---|---|
| fitted matrices stored, not only hashes | C3.6(a) |
| hashes | C3.6(a), N-b raw-byte convention |
| numerical ranks | C3.6(b) |
| class and orbit losses | C3.6(c) |
| weighted normal-equation terms used to assess cancellation | C3.6(d), C3.6(e) |
| per-prefix local fits and κ-row norms diagnostic only | C3.8 |

**E37-9** [L202]
> "The next executable work is one separately reviewed and frozen synthetic-only package, with its standing-approval application filed before execution. No checkpoint is opened. Its design is informed by the completed O7 result. No control, coefficient, grouping, edit or threshold is replaced after its new results are inspected."

| Requirement | Clause |
|---|---|
| one package, separately reviewed and frozen | C9.1 |
| synthetic-only | C1.1 |
| standing-approval application filed before execution | C9.2 (N2 sequence inherited) |
| no checkpoint opened | C1.2, C9.3 (preflight asserts that no checkpoint path is read) |
| design informed by O7, disclosed | §0 |
| no post-inspection replacement of a control, coefficient, grouping, edit or threshold | C9.5. Every TO BE FIXED BEFORE FREEZE item must be fixed in a frozen file before any execution. |

**E37-10** [L206]
> "Any subsequent neural result is limited to prediction of intervention-induced forecasts by the declared prefix-conditioned oracle response models. It does not identify the reachable-history algorithm, establish acquisition, isolate the recurrent transition from the readout, exclude general lookup implementations, or establish irreducible joint state, C4 or consciousness."

*Binding here:* C1 and C10.4. It is carried forward verbatim as the ceiling for any neural spec this package might lead to, together with the #38 L202 sentence.

## 2b. Astra #38 items: verbatim text and compliance map (kept from v1.2; clause references resolve in v1.3)

Each E38 item is quoted below as an exact substring of the raw file (sha `87fd77e0…ca2a5`), with its raw line in brackets. The check is re-run in §12. Each requirement is mapped to a numbered clause of this record.

**E38-1** [L308]
> "The selected confound treatment is descriptive-only. The package uses separately fitted plain full and fixed-kappa maps in each of four flip classes, with whole-orbit outer holdout. No augmented basis, shared-e fit, tied-bilinear fit or empirical neural floor is included. SYS-O6, SYS-PC, SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3 and SYS-LIM are included."

| Requirement | Clause |
|---|---|
| descriptive-only confound treatment | C6 |
| separately fitted plain full (3×8) and fixed-κ ([A;0], A 2×8) maps in each of four flip classes | C3.2 (with effective basis stated, Q2d) |
| whole-orbit outer holdout | C3.1 (six directed 2+2 folds, inherited) |
| no augmented basis, shared-e, tied-bilinear fit or empirical neural floor | C3.2, C6; change log 1–5 |
| all seven systems included | C4.1–C4.5; §8 accounting |

**E38-2** [L312]
> "On a non-crossing SYS-PC edit, the chart increment S_g C delta is exact. J_a delta is the first-order forecast response. Exact finite forecast discrepancies are computed by propagating the actual and predicted perturbed charts through Phi. SYS-LIM loss-scaling formulas derived from Jacobians are first-order statements unless a separate finite identity is established."

| Requirement | Clause |
|---|---|
| chart increment S_g C δ exact on non-crossing SYS-PC edits | C4.2(c) |
| J_a δ is the first-order forecast response | C4.2(c), C4.2(d) |
| exact finite discrepancies by propagating actual and predicted perturbed charts through Φ | C4.2(d), C5.6, §8 (5 propagations per edit) |
| SYS-LIM Jacobian loss-scaling formulas first-order only | C4.5 D6/D7 |

**E38-3** [L316]
> "Coefficient-recovery and held-out prediction identities require their stated full-column-rank premises. A resolved lower-rank minimum-norm fit does not inherit those identities merely because its fitting responses are reproduced. This rule applies consistently to all systems. Missing a required rank premise is EXPECTATION NOT APPLICABLE (RANK), not an implementation identity failure."

| Requirement | Clause |
|---|---|
| recovery / held-out identities require full-column-rank premises | C3.3(b), C4.1, C4.2(e), C4.3, C4.4 (D5) |
| resolved lower-rank min-norm fit does not inherit identities | C3.3(b) |
| applies to all systems | C3.3(b) premise table |
| missing premise = EXPECTATION NOT APPLICABLE (RANK), not identity failure | C7.1 item 7 |

**E38-4** [L320]
> "SYS-PC global cancellation is checked through the fitted full and reduced matrices, equality of the resulting finite predictions, and equality of losses. Loss equality alone does not establish predictor equality. All declared identity checks retain their fold and edit-size resolution."

| Requirement | Clause |
|---|---|
| SYS-PC global checked via fitted full and reduced matrices | C4.2(g)(i)–(ii) |
| equality of resulting finite predictions | C4.2(g)(iii) |
| equality of losses (as consequence, per cell) | C4.2(g)(iv), C5.5 |
| fold and edit-size resolution retained for all identity checks | C5.3(d), C7.0 |

**E38-5** [L324]
> "P0 uses exact rational history probabilities for probability-invariance checks. Numerical L, G and cancellation checks use the tolerances specified in Consult #38. P0 is required on the true-chart, SYS-FK and admissible SYS-NC1 constructions where the corresponding symmetry is asserted. A failed applicable P0 check stops the package."

| Requirement | Clause |
|---|---|
| exact rational history probabilities for probability invariance | C4.0(ii) |
| #38 tolerances for L, G, cancellation | C4.0, C5.5 |
| P0 on true chart, SYS-FK and admissible SYS-NC1 | C4.0 (charts) |
| failed applicable P0 check stops the package | C4.0, C7.1 item 1 |

**E38-6** [L328]
> "The rank-two Jacobian guard for SYS-FK and SYS-NC1-NC3 is justified by their common, prefix-independent right factor D_mu Q2^T. Its stacking convention is frozen explicitly. It is not generalized to arbitrary two-coordinate neural systems with prefix-dependent marginal-state Jacobians. Zero matrices and numerical rank bands receive explicit handling."

| Requirement | Clause |
|---|---|
| rank-two guard justified by common right factor D_μQ₂ᵀ | C3.11 |
| stacking convention frozen explicitly | C3.11(b) |
| not generalized to neural systems | C3.11(e), C10.6 |
| explicit handling of zero matrices and rank bands | C3.11(c)–(d) |

**E38-7** [L340]
> "Common masks govern comparative losses. An otherwise applicable exact-control identity is not hidden by invalidity of a different predictor. Matrix identities are checked before evaluation masking. Finite recovery identities are checked on actual-valid, non-crossing edits for which the relevant exactness premise applies. Ordinary predicted-belief guard failures remain coverage exclusions unless they themselves contradict an applicable exact-recovery identity."

| Requirement | Clause |
|---|---|
| common masks govern comparative losses | C5.3(a) |
| exact-control identity not hidden by another predictor's invalidity | C5.3(c) |
| matrix identities checked before evaluation masking | C5.3(b) |
| finite recovery on actual-valid non-crossing edits where premise applies | C5.3(c) |
| predicted-belief guard failures are coverage exclusions unless contradicting an exact-recovery identity | C5.3(c)–(d) |

**E38-8** [L344]
> "Any unavailable or unresolved map required by the common-mask comparison prevents that comparison from being pooled. All admissibility, rank and coverage flags are stored even when a higher-priority display label applies. No missing map is replaced by a zero map, no unresolved cell is silently dropped, and no pooled statistic is formed from a selected subset of resolved classes."

| Requirement | Clause |
|---|---|
| unavailable/unresolved required map prevents pooling of that comparison | C3.9, C7.1 item 4 |
| all admissibility, rank and coverage flags stored even under a higher-priority label | C7.0 |
| no zero-map substitution, no silent dropping, no subset pooling | C3.9, C7.0 |

**E38-9** [L348]
> "SYS-LIM is reported only. Its midpoint is computed from the declared exact-law A and D representative magnitudes. No additional split is tested. Its negative result concerns the specified global and flip-class map families and does not establish impossibility for predictors supplied with a different declared transport rule."

| Requirement | Clause |
|---|---|
| SYS-LIM reported only | C4.5, C7.1 item 8, C7.2 |
| midpoint from exact-law A and D magnitudes | C4.5 (exact rational t) |
| no additional split | C4.5 |
| negative result limited to declared map families; no impossibility for transport-rule predictors | C4.5 'Limit exposed', C10.7 |

**E38-10** [L352]
> "SYS-FK is a globally zero-kappa control on product-chart designs. It does not test the true-chart designs used by SYS-O6 and SYS-PC. Autonomous controls with kappa fixed only under a declared intervention family are possible, but are outside this package. No impossibility of same-baseline autonomous controls is claimed."

| Requirement | Clause |
|---|---|
| SYS-FK globally zero-κ on product-chart designs | C4.3 |
| does not test true-chart designs | C4.3 (report sentence) |
| intervention-fixed autonomous controls possible but out of scope | C4.3 'Alternatives' |
| no impossibility claim | C4.3; change log 15 |

**E38-11** [L356]
> "All synthetic normalization rules, probability weights, draws and coefficient rules are fixed before execution. Normalization is system-level and is not recomputed separately by fold. SYS-NC2 and SYS-NC3 coefficients use exact-law prefix probabilities through the frozen RMS rule. Their equal gradient RMS does not imply equal forecast response, conditioning or transferability."

| Requirement | Clause |
|---|---|
| normalization, weights, draws, coefficient rules fixed before execution | C3.12, C4.4.R, C5.2, C9.5 |
| system-level normalization, not per fold | C3.12 |
| c₂, c₃ from exact-law prefix probabilities via frozen RMS rule | C4.4.R |
| equal gradient RMS ≠ equal response, conditioning or transferability | C4.4.R, C10.8 |

**E38-12** [L360]
> "CLASS-FIT VALIDATION MET requires every required control identity and its rank premise. A required SYS-PC class cell with EXPECTATION NOT APPLICABLE (RANK) makes validation NOT MET (RANK). SYS-PC headroom is formed only after validation is met, with H defined as L_mu,class. Headroom thresholds are synthetic conventions and supply no neural response floor."

| Requirement | Clause |
|---|---|
| VALIDATION requires every required control identity and its rank premise | C7.2 |
| rank-lapsed required SYS-PC class cell gives NOT MET (RANK) | C7.2 |
| headroom only after validation; H = L_μ,class | C7.3 |
| thresholds synthetic conventions; no neural floor | C7.3, C10.5 |

**E38-13** [L364]
> "Before freeze, the package specifies stage order, baseline-cache policy, identity-check domains, exact scheduled edit counts, maximum propagation counts, and accounting for voided, unresolved, invalid and prematurely stopped work. Setup, diagnostics, output serialization and reporting are included in the workload and resource accounting. Outcome-dependent omissions do not become unexplained count mismatches."

| Requirement | Clause |
|---|---|
| stage order | C8.1 |
| baseline-cache policy | C8.2 |
| identity-check domains | C5.3, C8.3 (identity rows) |
| exact scheduled edit counts; maximum propagation counts | C8.3 |
| accounting for voided, unresolved, invalid, prematurely stopped work | C8.4 |
| setup, diagnostics, serialization, reporting in workload/resource accounting | C8.3, C8.5 |
| outcome-dependent omissions not unexplained mismatches | C8.4 (closure identity) |

**E38-14** [L376]
> "Execution uses one CPU, no GPU, RLIMIT_AS of 4,000,000,000 bytes, and a cumulative wall-clock limit of 600 seconds beginning before imports and including setup and reporting. The operational stop is 540 seconds, with the declared reserve and hard termination no later than 595 seconds. There are no automatic retries, parameter substitutions or post-result tolerance changes. Cap-limited work is incomplete, not a scientific negative."

| Requirement | Clause |
|---|---|
| 1 CPU, no GPU, RLIMIT_AS 4,000,000,000 bytes | C8.5 |
| 600 s cumulative from before imports incl. setup/reporting | C8.5 |
| operational stop 540 s; declared reserve; hard termination ≤ 595 s | C8.5 |
| no retries, substitutions, post-result tolerance changes | C8.5, C9.5 |
| cap-limited work incomplete, not a scientific negative | C7.1 (cap labels), C10.1 |

**E38-15** [L380]
> "This package tests implementation identities, synthetic response headroom and limitations of declared intervention-prediction models on specified synthetic systems. It establishes no result about trained GRUs and answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY. Confound gains do not identify an independent covariance register or exclude two-coordinate mediation or reachable-set lookup implementations. Failure of a class-conditioned criterion does not exclude nonlinear, prefix-dependent or orbit-dependent covariance codes. No result establishes acquisition, recurrent-transition-specific use, necessity, irreducible joint state, C4, C5, consciousness, autopoiesis or life."

| Requirement | Clause |
|---|---|
| ceiling text | C1 (verbatim), C10.4 |

**E38-16** [L384]
> "Consult #38 requires a revised scope before freeze. The revision incorporates these rulings and resolves the remaining execution specifications without inspecting new experimental outputs. No checkpoint is opened and no synthetic package is executed before the revised scope is reviewed and the standing-approval application and seal are completed."

| Requirement | Clause |
|---|---|
| revised scope before freeze; no new outputs inspected | this file; §12 |
| no checkpoint, no execution before review, application and seal | C9.2, status line |

**Other binding #38 body text (verbatim excerpts, raw line in brackets).** These lines carry rulings outside E38-1..16, and they bind as written.

- **[L5]** "I select the descriptive-only confound treatment explicitly offered in S6/Q1. Keep the plain four-class model and all seven systems. Do not adopt an empirical neural floor or the augmented basis in this package."
- **[L38]** "This establishes equality of the two predicted perturbed charts, and therefore equality of their finite forecast predictions wherever propagation is defined."
- **[L46]** "is the first-order forecast discrepancy. It is not generally the exact finite discrepancy."
- **[L57]** "Likewise, C4.2(c) should say that the chart increment is exactly `S_g C delta` on a non-crossing edit. `J_a delta` is its first-order forecast response."
- **[L69]** "If the stacked full design has resolved rank 3, least squares uniquely recovers `S_g C`. Finite prediction is then exact on valid, non-crossing edits."
- **[L71]** "If the design has lower rank, a minimum-norm solution can reproduce fitting responses without reproducing the intended coefficient matrix or held-out responses."
- **[L73]** "Apply that distinction consistently to SYS-O6, SYS-PC, SYS-FK and SYS-NC2. C4.3's statement that D4 holds "for every resolved design" is too broad. Full-rank recovery, or a separate proof of prediction invariance across the null space, is required."
- **[L83]** "That supports the exact-rank premises. It does not establish numerical rank under the frozen singular-value thresholds."
- **[L94]** "That conclusion is sound. In general, nested models fitted on fitting prefixes need not have nonnegative held-out gain. Keep negative gains for confounds and SYS-LIM."
- **[L96]** "Also correct the wording around `B_mu`: the adjustment to `C_mu` is generally nonzero. Saying the whole `B_mu` is "generally != 0" does not express the intended point."
- **[L118]** "But the loss ratio `(1 + lambda)^2`, and the wrong-sign factor 4, are Jacobian-level results. They are not automatically exact at eps_syn = 0.1 or 0.25."
- **[L120]** "Equality of a predicted chart with the actual chart does give exact finite recovery. Scaling a chart error does not generally scale the finite forecast error by the same factor."
- **[L124]** "Equal pooled losses alone do not establish equal predictors. Different predictions can have equal losses."
- **[L134]** "Report loss equality as a consequence. Do not make it the sole operational definition of "GLOBAL CANCELLATION AS DERIVED.""
- **[L138]** "I choose the descriptive-only alternative already offered by the record. This applies to confound interpretation; the implementation identities and separate SYS-PC headroom assessment remain."
- **[L154]** "Both use the specified weighted objective and fitting prefixes only. Each class is fitted separately. The global comparator uses one corresponding pair of maps per fold."
- **[L156]** "There are no `mu_x`, `mu_y`, polynomial or shared-e augmentation terms."
- **[L158]** "I do not approve Option A's proposed later-neural hurdle. A ratio measured on SYS-NC1 is a result for that fixture. RMS-matching gradients does not match its state geometry, forecast derivatives, finite responses, validity masks or nonlinearities to a GRU. Calling the number a "floor" gives it a calibration role that has not been established."
- **[L160]** "Also, the final question's description of A as a floor on the "fixed-kappa NC" is incorrect. SYS-NC1 is a varying-kappa, two-coordinate confound. SYS-FK is the genuinely fixed-kappa fixture."
- **[L164]** "- Withdraw v1 Option B. Its coefficient ambiguity can invalidate the desired held-out PC recovery."
- **[L183]** "- I accept that conditional algebra. I do not approve the departure from separate class fitting for this package."
- **[L184]** "- Option C supplies no general transfer calibration. Exceeding a proposed bound falsifies that bound for the tested law. Not exceeding it establishes no bound for other laws."
- **[L186]** "NC2 and NC3 remain useful descriptive confounds under the plain model. Their common symmetry helps organize the comparison, but their different baselines and derivatives mean this is not a comparison in which only functional form changes."
- **[L190]** "Include it, reported only, using the declared A-versus-BCD midpoint. Do not add a B-isolating split."
- **[L192]** "Its purpose is to expose a limitation of the selected constant-per-class maps. It is not necessary to introduce a much smaller boundary margin to make that point."
- **[L194]** "The phrase "no fit type here can carry it to a held-out orbit" should identify the exact failure: in the CD, BD and BC fitting folds, full-rank recovery produces the negative-sign chart map, which is wrong on held-out A whenever the edit has a nonzero relevant component."
- **[L196]** "Do not turn this into an impossibility claim about every predictor that could be constructed. A declared transport rule using the state's magnitude could represent this system; the selected maps do not contain that rule."
- **[L198]** "Keep D7 as a reported analytic diagnostic. A failure of an exact, applicable D7 identity warrants investigation, but SYS-LIM should not become an additional positive criterion for CLASS-FIT VALIDATION MET."
- **[L204]** "SYS-LIM is autonomous in the relevant sense. Its branch is selected from its own state, not supplied by the analyst at response generation."
- **[L208]** "Retain `kappa == 0` on the product chart. It meets the requested control role. Keep the disclosure that it checks different L matrices from SYS-O6/SYS-PC."
- **[L210]** "A globally constant kappa cannot simultaneously reproduce true baselines having different kappa values. That is a real restriction."
- **[L221]** "This uses the true baseline chart and its L, while the intervention Jacobian has a zero kappa row. The register is part of the synthetic state. It is not a prefix label supplied only to the analyst."
- **[L223]** "It would be an intervention-fixed control, not a globally constant-kappa system. It also changes the state/intervention specification, so I do not add it here."
- **[L225]** "The stronger rejection of a two-coordinate plateau construction is also unjustified. Distinct marginal pairs can themselves distinguish this finite set of prefixes. A smooth function can be locally constant near each distinct pair without receiving a separate prefix identifier. Its finite-edit neighborhoods would need their own specification."
- **[L227]** "Correct the impossibility statement; do not expand this package to implement those alternatives."
- **[L249]** "Use full-precision values computed under the frozen normalization rule. The displayed rounded numbers explain the bound; they must not govern its implementation."
- **[L251]** "An observed crossing under these verified construction premises is an integrity failure. No replacement edit is allowed."
- **[L296]** "Apply the gain tolerance within each required fold/group/size cell, using that cell's common-mask losses and S. Pooled equality cannot override a failing cell. Report the absolute difference and its scale."
- **[L298]** "These are prospective numerical acceptance conventions, not certified forward-error bounds. Do not loosen them if a poorly conditioned fit fails."
- **[L300]** "Exact probability invariance should be checked using the exact rational history probabilities already available from O1. Do not equate "exact law identity" with a requirement that independently accumulated floating-point sums have identical bytes."
- **[L302]** "Retain the inherited rank bands and headroom boundary convention."
- **[L336]** "with the same `C_mu` across prefixes. It would not follow from local two-coordinate mediation alone."
- **[L372]** "That is not yet the complete package count. O1/O2 and any additional diagnostic propagation must be accounted for. The historical runtime supports a feasibility estimate, not a guarantee. No unapproved pilot is needed to make the deterministic schedule explicit."

**#38 Q-rulings (verbatim, L255–276).**

| Question | Ruling |
|---|---|
| Q1 | Descriptive-only confound handling; plain four-class fits; all seven systems. No empirical neural floor. |
| Q2a | Withdraw v1 Option B. |
| Q2b | Accept the conditional D2' algebra; do not include B-repaired or approve coupled class fitting in this package. |
| Q2c | No tied-bilinear solver in this package. |
| Q2d | Yes. State the effective basis explicitly, including that the selected model has no augmentation. |
| Q3 | Yes. An unresolved required class design suppresses that system's pooled class statistic. Do not pool only the resolved survivors. |
| Q4 | Retain the proposed ALL/MARG thresholds as synthetic reporting conventions only. Define `H = L_mu,class`. No prediction that PC will meet them. |
| Q5 | Stop on applicable control failures. A failed identity is an operational failure diagnosis, not conclusive proof that the mathematical derivation rather than the implementation is correct. |
| Q6 | Keep SYS-FK with its product-chart limitation. Correct the claim that autonomous same-baseline alternatives are impossible. |
| Q7 | Accept the cubic and RMS rules. Use exact-law prefix probabilities, not probabilities reconstructed from rounded SDs. No coefficient adjustment after inspection. |
| Q8 | Yes. SYS-PC's marginal coordinates carry the signs used by its autonomous readout. |
| Q9 | Use the numerical conventions below. |
| Q10 | Reuse Q, Q2 and the directions, including their generation conventions and hashes. Disclose development-informed reuse. |
| Q11 | P0 supports the symmetry premise. It must be combined with the specified state map, weights, complete fitting orbits and rank conditions. |
| Q12 | Keep all four sizes; 0.1 remains the sole headroom reference. |
| Q13 | Yes. Including SYS-O6 in a separately identified package is allowed. It does not reopen, replace or retry the completed oracle package. |
| Q14 | Keep the declared A-versus-BCD midpoint. No additional split. |
| Q15 | SYS-LIM remains reported only. Any required SYS-PC class cell lacking the rank premise makes validation NOT MET (RANK); it is not silently omitted. |
| Q16 | Not applicable to the selected design. No augmented SYS-LIM fit is executed. |
| Q17 | Yes. Reading the threshold branch from the synthetic state's own magnitude satisfies the autonomy requirement here. |

## 2c. Astra #39 items: verbatim text and compliance map

Each E39 item is quoted below as an exact substring of the raw file (sha `e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482`), with its raw line in brackets. The check is re-run in §12. Each requirement maps to a clause of this record or of the annex.

**E39-1** [L181]
> "The scientific design is approved for freeze with the Consult #39 amendments. Remaining implementation details are completed in an immutable, hash-referenced specification annex or manifest and checked by an independent pre-seal conformance review. The complete frozen bundle, standing-approval application and seal are required before S0. No experimental outcome is inspected to choose those details."

| Requirement | Clause |
|---|---|
| scientific design approved for freeze with #39 amendments | status line; C9.1 |
| remaining implementation details in immutable, hash-referenced annex or manifest | C9.6; annex |
| independent pre-seal conformance review | C9.1, C9.2 step 2 |
| frozen bundle, standing-approval application and seal before S0 | C9.2 |
| no experimental outcome inspected to choose details | C9.5, C9.7; annex A8 |

**E39-2** [L185]
> "System construction and the required L, J and G tables precede their P0 checks. The stage sequence is preflight, O1, O2, system construction, applicable P0 checks, response-map fitting and fit freeze, finite evaluation, aggregation, and reporting. The SYS-NC1 coefficient refit belongs to system construction. No intervention-response-map fit precedes the applicable P0 checks."

| Requirement | Clause |
|---|---|
| system construction and L, J, G tables precede P0 | C8.1 (stages S3 → S4), C4.0 |
| stage sequence preflight … reporting | C8.1 |
| SYS-NC1 coefficient refit is system construction | C8.1 stage S3, C4.0 |
| no response-map fit precedes P0 | C8.1, C4.0 |

**E39-3** [L189]
> "Finite identity and guard-consistency checks are evaluated during propagation as soon as their required values are available. An applicable stopping failure stops further evaluation. S7 aggregates stored residuals and forms labels; it does not defer all finite identity checking until evaluation has finished. Identity reports include the number of tested edits. An empty test domain is NOT EVALUATED, not a passed identity."

| Requirement | Clause |
|---|---|
| finite identity and guard checks evaluated during propagation | C5.3(c), C8.1 stage S6 |
| applicable stopping failure stops further evaluation | C5.3(c), C7.1 item 1 |
| S7 aggregates and labels; no deferred checking | C8.1 stage S7 |
| identity reports include tested-edit counts | C5.3(c), C7.1 item 7 |
| empty test domain = NOT EVALUATED | C5.3(c), C7.1, C7.2 |

**E39-4** [L193]
> "Actual-valid guard consistency applies to predictors required to recover the actual perturbed chart. SYS-PC global cancellation instead requires equality between its two predicted charts and forecasts; it does not require either predictor to recover the actual response. Its finite forecast equality is checked where both predictions are valid, independently of unrelated predictor masks. Ordinary invalid global predictions are coverage exclusions. For an actual-recovery predictor, a validity-guard mismatch is a stopping operational inconsistency, with probability margins and numerical residuals reported; it is not automatically evidence that the recovery tolerance was exceeded."

| Requirement | Clause |
|---|---|
| guard consistency only for actual-recovery predictors | C5.3(c) |
| SYS-PC global: equality of predicted charts/forecasts, not actual recovery | C4.2(g)(iii) |
| equality checked where both predictions valid, independent of unrelated masks | C4.2(g)(iii) |
| invalid global predictions are coverage exclusions | C4.2(g)(iii), C5.3(c) |
| guard mismatch = stopping operational inconsistency, margins and residuals reported, not proof of tolerance excess | C5.3(c), C7.1, C10.11 |

**E39-5** [L197]
> "VALIDATION MET is necessary but not sufficient for a SYS-PC headroom threshold label. Headroom also requires available required maps, resolved required fits, the declared reference-size count and law-mass coverage in every required fold/class, a positive scoreable denominator, and S greater than zero. Missing eligibility receives its applicable status and cannot yield HEADROOM MET. Confound gains and descriptive expectations do not enter VALIDATION; mandatory applicable integrity checks, including P0, remain mandatory."

| Requirement | Clause |
|---|---|
| VALIDATION MET necessary, not sufficient | C7.3 |
| eligibility: maps, resolved fits, reference-size count and law-mass coverage per fold/class, positive denominator, S > 0 | C7.3 items 1–5 |
| missing eligibility gets applicable status, never HEADROOM MET | C7.3 |
| confound gains and descriptive expectations outside VALIDATION; mandatory integrity checks incl. P0 remain | C7.2, C4.0 |

**E39-6** [L201]
> "Loss records retain fit type, fold, class, evaluation orbit, group, size and weighting mode. The scheduled maximum is 16,128 mode-indexed base loss records across seven systems and both fit types, with each record holding L_mu, L_full, S and gain. Additional aggregates are enumerated separately if stored. Optional single-prefix fits are disabled. The propagation maximum remains 3,443,968 float calls plus 272 exact calls under the inherited counting conventions."

| Requirement | Clause |
|---|---|
| loss records keyed by fit type, fold, class, orbit, group, size, mode | C3.6(c) |
| 16,128 base records, each with L_mu, L_full, S, gain | C3.6(c), C8.3 |
| stored aggregates enumerated separately | C8.3 |
| single-prefix fits disabled | C3.8, C8.3 |
| 3,443,968 float + 272 exact | C8.3 |

**E39-7** [L205]
> "Every scheduled propagation has one terminal accounting category. An already attempted call is counted as attempted. For an unattempted call, a preceding stop takes priority; otherwise whole-system inadmissibility, prefix voiding and unavailable-map skipping are applied in that order. Systems declared RESTRICTED COMPARATOR NOT ADMISSIBLE receive no subsequent response-map fits or evaluation propagations; their skipped work is counted separately. A normally completed run must close its accounting exactly. After forced termination, unavailable final counters are reported as unknown beyond the last durable record, not fabricated and not treated as a scientific result."

| Requirement | Clause |
|---|---|
| one terminal category per scheduled propagation | C8.4 |
| attempted counted as attempted | C8.4 |
| precedence: prior stop, inadmissibility, voiding, unavailable map | C8.4 |
| inadmissible systems: no fits or propagations; counted separately | C3.9, C8.4 |
| normal run closes exactly | C8.4 |
| forced termination: unknown beyond last durable record | C8.4; annex A5 |

**E39-8** [L209]
> "NOTE_1 N1 and N2 are adopted. Empty designs are unavailable and are distinguished from nonempty zero matrices. Extended-B3 band cases are recorded as UNRESOLVED-B3 without an automatic stop and are never described as passed guards. They do not by themselves make a fitted response map unavailable. A resolved third direction retains the integrity stop. Required control fit-rank lapses prevent VALIDATION MET. D7 INVESTIGATE remains non-stopping and outside VALIDATION and HEADROOM, but accompanies any later decision about neural work."

| Requirement | Clause |
|---|---|
| N1 and N2 adopted | C3.3(a′), C3.3(b), C4.4, C4.5 |
| empty designs unavailable; distinct from nonempty zero matrices | C3.3(a′), C3.9 |
| UNRESOLVED-B3 recorded, no automatic stop, never a passed guard, does not make map unavailable | C3.11(d), C8.4, C10.12 |
| resolved third direction keeps integrity stop | C3.11(d), C8.6 |
| required control fit-rank lapses prevent VALIDATION MET | C7.2 |
| D7 INVESTIGATE non-stopping, outside VALIDATION/HEADROOM, accompanies neural decision | C4.5, C7.4, C10.13 |

**E39-9** [L213]
> "The exact rational prefix-probability sum is asserted to equal one before RMS-matched coefficients are computed. The c2 denominator uses that exact sum converted once to float64. The summation conventions for rho and c3 are frozen. No failed normalization is repaired by rescaling. Values computed under frozen deterministic rules are permitted execution outputs; no discretionary rule, parameter or threshold is chosen or changed after outputs are inspected."

| Requirement | Clause |
|---|---|
| exact ΣP = 1 asserted before RMS coefficients | C4.4.R step 2 |
| c2 denominator = exact sum converted once | C4.4.R steps 3, 6 |
| summation conventions for rho and c3 frozen | C4.4.R step 5 |
| no rescaling repair | C4.4.R step 2, C7.1 |
| frozen-rule values permitted; no discretionary post-output choice | C9.5 |

**E39-10** [L217]
> "The complete frozen bundle specifies authenticated reused arrays and generation conventions, output schema and paths, full artifact inventory, resource estimates, and deterministic event ordering. It identifies the applicability domain of each P0 comparison and records omitted voided pairs. Losses, identities and coverage are not silently evaluated on different undeclared domains. Numerical rank, headroom and fixture outcomes remain prospective."

| Requirement | Clause |
|---|---|
| authenticated reused arrays and conventions | C5.2; annex A1 |
| output schema and paths | annex A2, A3 |
| full artifact inventory | C8.3; annex A5 |
| resource estimates | C8.7; annex A4 |
| deterministic event ordering | C8.1; annex A6 |
| P0 applicability domains; omitted voided pairs recorded | C4.0; annex A7 |
| no undeclared domains for losses, identities, coverage | C5.3; annex A7, A6 |
| rank, headroom, fixture outcomes prospective | §12.2 |

**E39-11** [L221]
> "Claims of affine readouts are system- and domain-specific. SYS-PC and SYS-LIM have affine chart maps within their declared non-crossing branches; SYS-NC1 and SYS-NC3 are nonlinear. The statement that a positive confound gain is compatible with two-coordinate mediation applies to SYS-NC1-NC3 and is not used to classify SYS-LIM as a two-coordinate system."

| Requirement | Clause |
|---|---|
| affine claims system- and domain-specific | C4.R, C10.10 |
| SYS-PC, SYS-LIM affine within non-crossing branches; SYS-NC1, SYS-NC3 nonlinear | C4.R |
| two-coordinate-mediation statement for SYS-NC1–NC3 only; not used for SYS-LIM | C6, §2 E37-7 note, C10.10 |

**#39 Q-R rulings (verbatim, L13–20).**

| Question | Ruling |
|---|---|
| Q-R1: D7 failure | Accept `D7 INVESTIGATE`, with no automatic stop and no change to VALIDATION or HEADROOM. Retain the failed diagnostic prominently. A later decision about neural work must address it; unchanged labels do not resolve the discrepancy. |
| Q-R2: class zero-gain granularity | Confirm `fold/class/group/size` for SYS-FK class losses. Do not replace those checks with a pooled check. |
| Q-R3: other controls' rank lapses | Confirm. Missing a required SYS-O6 or SYS-FK rank premise prevents VALIDATION MET, just as for SYS-PC. Distinguish resolved lower rank from unresolved rank. |
| Q-R4: guard failure | Accept for predictors required to recover the actual perturbed chart, with the qualifications below. Do not apply it indiscriminately to SYS-PC global predictor equality. |
| Q-R5: extended B3 | Accept the unweighted fitting-prefix stacks, both global and class-specific. Accept an unresolved band result without an automatic stop. It must remain explicitly unresolved, not be reported as a passed guard. |
| Q-R6: caching and order | Accept per-system baseline propagation and no prediction deduplication. Correct the construction/P0 dependency and perform stopping identity checks during evaluation, not only after all evaluation finishes. |

**Other binding #39 body text (verbatim excerpts, raw line in brackets).** These lines bind as written.

- **[L1]** "Verdict: FREEZE WITH NAMED EDITS."
- **[L3]** "The scientific design can now be fixed. The remaining corrections are explicit execution and reporting rules; they do not require another experiment-design resubmission. Complete them in the frozen specification bundle and obtain the independent pre-seal conformance review before execution."
- **[L36]** "An actual-valid edit can therefore have two invalid global predictions without contradicting the global cancellation identity. Those predictions are coverage exclusions. Check their finite forecast equality where both predicted beliefs are valid, independently of whether the other class predictors pass the common mask."
- **[L38]** "Second, a numerical guard mismatch does not necessarily imply that the `1e-9` recovery tolerance was exceeded. A tiny perturbation can place two otherwise close beliefs on opposite sides of the `1e-6` guard."
- **[L40]** "For a predictor required to recover the actual chart, retain a stopping guard-consistency check. Report the actual and predicted minimum probabilities, chart difference and available recovery residual. Describe the event as a guard inconsistency, not as proof of a large prediction error. Do not relax the guard or tolerance after seeing it."
- **[L44]** "N1 correctly adds the D6 and SYS-NC1 global premises. Their diagnostic roles remain unchanged."
- **[L59]** "Keep the separate handling of a nonempty zero matrix and an empty design. An empty fitting set is unavailable; it is not a successfully fitted rank-zero matrix."
- **[L61]** "N3's exact normalization assertion is appropriate. Specify the denominator unambiguously:"
- **[L70]** "This avoids turning an independently accumulated floating-point sum into an unintended normalization adjustment. Freeze the floating-point summation order used for rho and c3. Failed exact normalization stops; nothing is rescaled."
- **[L72]** "Computing c2, c3 and normalization values during execution under frozen rules is allowed. They are derived quantities, not post-result choices. C9.5's blanket statement that "no value is set" after any output must be read and corrected accordingly."
- **[L74]** "One statement in the Research Lead summary also needs correction: not every readout is affine in z. SYS-NC1 and SYS-NC3 are nonlinear. SYS-PC and SYS-LIM have affine chart maps only within a fixed branch. The record's system-specific claims should govern."
- **[L92]** "The supplied exact midpoint also equals `(A + D)/2`."
- **[L96]** "First, the loss-cell count does not match C3.6(c). That clause retains class and evaluation-orbit resolution for both fit types, plus weighted and unweighted results."
- **[L112]** "Each record can contain all four quantities: `L_mu`, `L_full`, `S` and gain. This is a record count, not a scalar count."
- **[L114]** "The table's 5,040 count instead omits class resolution for global losses and does not count weighting modes. Preserve C3.6(c)'s richer diagnostics and correct the table. Global orbit-level aggregates can be derived from these records; if separately stored, enumerate them separately."
- **[L116]** "Second, the optional single-prefix fits are not included in the 541-SVD schedule. Disable them for this package. Their optional status must not permit an implementation-time expansion after the counts are frozen."
- **[L118]** "Third, skip reasons overlap unless precedence is specified. A voided prefix can also belong to a class with an unavailable map, and either can occur after a stop. Count each scheduled propagation exactly once. Whole-system inadmissibility also needs an explicit accounting category and execution policy."
- **[L120]** "Fourth, hard termination can prevent the last counters from being written. Do not manufacture exact attempted/unreached counts from an incomplete log. Report the last durable counters and any unknown interval, with the run marked incomplete."
- **[L122]** "The stated 21 files correctly count the enumerated core artifacts. They do not include the wrapper post-run index or any additional logs. The final schema must list those separately."
- **[L126]** "The P0 dependency problem is not confined to SYS-NC1. SYS-FK's product-chart L table is also needed before its P0 check, but system construction currently occurs later."
- **[L143]** "The NC1 coefficient refit is system construction. It is not one of the intervention-response-map fits that P0 must precede."
- **[L145]** "During S6, check guard consistency and finite identities when the required values become available. Accumulate maxima and counts. Do not wait until S7 to discover a stopping failure after completing all seven systems."
- **[L147]** "C7.3 also needs its eligibility gates restored explicitly. VALIDATION MET alone does not establish sufficient SYS-PC comparison coverage or a positive response denominator."
- **[L152]** "The declared count and law-mass coverage in every required fold/class at the reference size."
- **[L153]** "A positive scoreable denominator."
- **[L156]** "Store diagnostic values where permitted, but do not award HEADROOM MET after a coverage failure. An empty identity domain is not a passed identity."
- **[L158]** "There is a smaller wording conflict in C7.2: an applicable NC1 P0 check is mandatory, while the text says confound systems "never enter VALIDATION." The intended distinction should be that confound gains and descriptive expectations do not enter validation. Mandatory integrity checks remain mandatory."
- **[L162]** "They need not all be copied into the prose scope record. They must be fixed in a versioned, immutable implementation annex or manifest that is part of the frozen specification bundle."
- **[L166]** "The present ruling fixes the scientific design and execution rules."
- **[L167]** "Implementation supplies exact array provenance, hashes, schema, file paths and resource estimates."
- **[L168]** "An independent pre-seal review checks that those details conform."
- **[L169]** "The Research Lead completes the frozen bundle, standing-approval application and seal before S0."
- **[L171]** "Reusing the declared arrays does not authorize generating new arrays with different conventions. Seed values alone are insufficient: preserve the specified generator, dimensions, ordering, normalization and matrix-sign conventions, or use the authenticated existing arrays."
- **[L173]** "The memory estimate must cover Python objects, exact arithmetic, numerical-library workspace, aggregation records and serialization. The raw numeric-array size alone is not a process-memory estimate. No pilot execution is needed for this estimate."
- **[L175]** "No further Astra scope review is required solely to fill those bounded implementation details. A proposed change to the estimator, controls, masks, thresholds, directions, sizes, caps or claim ceiling would require a new ruling."
- **[L235]** "The claim ceiling remains E38-15, including no result about trained GRUs, no answer to any of the four Q-tags, no exclusion of general two-coordinate or lookup implementations, and no consciousness, C4/C5, autopoiesis or life claim. The explicit limitation concerning orbit-dependent codes also remains."
- **[L237]** "Proceed to implementation and independent pre-seal review under these fixed amendments. No additional synthetic pilot or checkpoint inspection is authorized by this ruling."

**#39 rank categories (verbatim, L48–57).**

```text
Resolved full column rank:
    every required singular-value ratio > 1e-6

Unresolved:
    at least one ratio in [1e-10, 1e-6]

Resolved lower rank:
    no ratio in that band, but fewer than all columns resolved
```

**#39 normalization (verbatim, L63–68).**

```text
P_sum_exact = sum_a P_a       # exact rational arithmetic
assert P_sum_exact == 1
P_sum_float = float(P_sum_exact)
c2 = rho_NC1 / sqrt(P_sum_float)
```

**#39 stage order (verbatim, L130–141).**

```text
S0  Preflight
S1  O1
S2  O2
S3  System construction, validity/admissibility, normalization,
    NC1 coefficient refit, c2/c3, midpoint, L/J/G tables and bounds
S4  Applicable P0 checks
S5  Response-map fits, rank reports, matrix identities and fit freeze
S6  Baselines and finite evaluation, with streaming identity checks
S7  Final aggregation and labels
S8  Reporting and post-run records
```

**#39 caps (verbatim, L225–233).**

```text
1 CPU
No GPU
RLIMIT_AS = 4,000,000,000 bytes
600 seconds cumulative from before imports
540-second operational stop
Hard termination no later than T0 + 595 seconds
No automatic retries
```

## 3. Design: classes, fits, stored terms, rank, pooling

**C3.1 Orbits, folds and class labels (inherited, unchanged).**
- **Orbits and folds.** These come from v1.1 oracle §2 L48–49 and `geometry.py:7–22`.
  - Orbits: A{0,5,10,15}, B{1,4,11,14}, C{2,7,8,13}, D{3,6,9,12}.
  - Six directed whole-orbit 2+2 folds (E38-1 "whole-orbit outer holdout"): AB→CD, CD→AB, AC→BD, BD→AC, AD→BC, BC→AD.
- **Representatives:** A→0, B→1, C→2, D→3.
- **Flip masks.** Defined at `stages.py:208` (O1 flip fixture, PASS in `stage_O1.json`).
  - Mask 5 = flip-X (μ_x→−μ_x, κ→−κ).
  - Mask 10 = flip-Y (μ_y→−μ_y, κ→−κ).
  - Mask 15 = flip-XY (κ unchanged).
- **Class label.** g(a) = a XOR rep(orbit(a)), read as one of I, X, Y, XY:

| Class | A | B | C | D |
|---|---|---|---|---|
| I (mask 0) | 0 | 1 | 2 | 3 |
| X (mask 5) | 5 | 4 | 7 | 6 |
| Y (mask 10) | 10 | 11 | 8 | 9 |
| XY (mask 15) | 15 | 14 | 13 | 12 |

- **Representative signs (RD arithmetic, `stage_O1.json` `stage4_chart_exact`).** All four representatives have μ_x > 0 and μ_y > 0, so here the class coincides with the sign quadrant. Write χ(g) = s_x·s_y (I +1, X −1, Y −1, XY +1). Then κ_a = χ(g(a))·κ_rep(orbit(a)).
- **Per fold:** 2 fitting prefixes and 2 evaluation prefixes per class (#37 L107).

**C3.2 Selected class-conditioned model (E38-1; #38 L140–156, verbatim).**

```text
For each system, fold f and class g:

Full:
    Delta theta_hat = B_(f,g) delta
    B_(f,g) is an unrestricted 3 x 8 matrix.

Fixed-kappa:
    Delta theta_hat = [A_(f,g) delta; 0]
    A_(f,g) is an unrestricted 2 x 8 matrix.
```

- **Objective.** E36-3 weighted least squares on all output components, with w(a,u) = P_h(a,u) over all 16 continuations, on fitting prefixes only:

  min Σ_{a∈fit(f)∩g} Σ_u w(a,u)‖L_a(u)X − J_a(u)‖²

  Here J_a(u) is the system's local response map and L_a(u) = ∂Φ/∂θ at the system's own baseline chart. The fixed-κ fit uses the first two columns of L_a(u).
- **Separate fitting.** Each class is fitted separately: 4 classes × 2 maps per fold.
- **Global comparator.** One pair (B_f, A_f) per fold, fitted on all 8 fitting prefixes (#38 L154).
- **Effective basis, stated explicitly (Q2d).**
  - Full map: the 24 free coefficients of B_(f,g), constant across the class's prefixes.
  - Fixed-κ map: the 16 free coefficients of A_(f,g), with κ row identically 0.
  - **No augmentation.** There are no μ_x, μ_y, polynomial or shared-e terms, no coupling across classes and no tied-bilinear form (#38 L156; Q2c).
- **Application.** A class map is applied unchanged to the class-g prefixes of the evaluation orbits (#37 L105). The same maps serve ALL, MARG and XOR reporting.

**C3.3 Solver, rank and rank premises.**
- **(a) Solver and rank bands (inherited, unchanged).**
  - One SVD of the √w-weighted design (`linalg_fit.py:21–75`).
  - σ_i/σ_1 > 10⁻⁶ is resolved. σ_i/σ_1 < 10⁻¹⁰ is resolved zero. The band [10⁻¹⁰, 10⁻⁶] is UNRESOLVED (E36-8). σ_1 = 0 means rank 0 and a zero fit.
  - Minimum-norm fit with rcond = 1e-10 (`pinned.py:17`).
  - B2: a resolved lower-rank design is fitted minimum-norm and scored. The inherited rank bands are retained per #38 L302.
- **(a′) Rank categories (NOTE_1 N2 adopted, E39-8; #39 L46–59).** For every nonempty design:
  - **Resolved full column rank:** every required σ_i/σ_1 > 1e-6.
  - **Unresolved:** at least one ratio in [1e-10, 1e-6]. The cell reads REFERENCE RANK UNRESOLVED and is handled by C3.9 and C7.1. It does **not** read EXPECTATION NOT APPLICABLE (RANK).
  - **Resolved lower rank:** no ratio in that band, but fewer than all columns resolved. EXPECTATION NOT APPLICABLE (RANK) applies only here.
  - **Nonempty zero matrix:** σ_1 = 0, giving rank 0 and a zero minimum-norm fit. This is a resolved lower rank, kept separate from the empty case.
  - **Empty design:** zero non-voided fitting prefixes. The design is **UNAVAILABLE**. It is not a successfully fitted rank-zero matrix (#39 L59, E39-8).
- **(b) Rank premises (E38-3).** A coefficient-recovery or held-out-prediction identity applies only when its design has **resolved full column rank** (3 for full maps, 2 for fixed-κ maps). A resolved lower-rank minimum-norm fit is still scored and reported, but no identity is asserted for it. It reads EXPECTATION NOT APPLICABLE (RANK), not an identity failure (#38 L71–73).

| Identity | System(s) | Required premise |
|---|---|---|
| B = DQᵀ, global and class; finite recovery | SYS-O6 | full design rank 3 in that cell |
| D1 global (B = [c_x;c_y;0], A = [c_x;c_y]) | SYS-PC | global full rank 3 and global μ design rank 2 (invertible normal matrices, #38 L31) |
| D2 class (B = S_gC); finite recovery | SYS-PC | class full rank 3 |
| D6 global (B = [c_x;c_y;λc_τ], A = [c_x;c_y]); diagnostic only (NOTE_1 N1) | SYS-LIM | global full rank 3 and μ design rank 2 |
| Global Pred_full ≡ Pred_μ; descriptive (NOTE_1 N1) | SYS-NC1 | global full rank 3 and μ design rank 2, plus zero voids (C4.4) |
| D4 (B = [C_μ;0], A = C_μ) | SYS-FK | full rank 3 for B; μ design rank 2 for A |
| D5 (full exact) | SYS-NC2 | full rank 3 |
| D7 (diagnostic only) | SYS-LIM | class full rank 3 in CD/BD/BC folds |

  - **Analytic support (#38 L75–83).** Each valid baseline's exact 3-column L has full rank. That supports the exact-rank premises but does not establish numerical rank under the thresholds. Numerical ranks are prospective and are not predicted here.

**C3.4 Global comparator.** For every system, the global pair per fold is fitted with the same solver. It is a fixed descriptive comparator (#37 L116), except for the identities of C4.

**C3.5 Freeze-before-scoring order.** For every system:
1. Compute every global and class fit from fitting prefixes only.
2. Write the fits with their stored terms to `outputs/fit_freeze_<system>.json` and fsync.
3. Only then propagate any evaluation edit. No fit is recomputed after evaluation begins. Fits are stage S5; evaluation is stage S6 (C8.1).

**C3.6 Stored outputs (E37-8).** Arrays are float64 C-contiguous little-endian, each with name, shape, `<f8` and raw-byte sha256 (closure note N-b).
- **(a) Matrices.** Every B and A, global and class, for every system and fold, stored in full.
- **(b) Rank reports.** For every fit design and every extended-B3 stack (C3.11): full σ list, σ_1, ratios, numerical rank, unresolved flag and n_inverted.
- **(c) Losses (E39-6).** One base loss record per (system, fit type, fold, class, evaluation orbit, group, ε_syn, weighting mode ∈ {weighted, unweighted}). Each record holds L_μ, L_full, S and gain, with the scoreable count and law mass behind them.
  - Per fit type and system: 6·4·2·3·4 = 576 logical cells.
  - Scheduled maximum: 7·2·2·576 = **16,128 mode-indexed base loss records** (#39 L100–112).
  - Global orbit-level aggregates are derivable from these records and are **not stored separately**. Every stored aggregate is enumerated in §8 (C8.3).
- **(d) Normal-equation terms.**
  - Per prefix: G_a (3×3) and r_a (3×8).
  - Per (fold, class) and per fold: ΣG and Σr.
  - Their μμ block (2×2) and μ rows (2×8).
- **(e) Cancellation diagnostics (#37 L35–62).**
  - Per (system, orbit): Σ G_a[κ,μ_x], Σ G_a[κ,μ_y] and Σ G_a[μ_x,μ_y].
  - For SYS-NC1–NC3: Σ G_a[κ,κ]·Dg(μ_a).
  - The P0 residuals of C4.0.
  - Tolerances per C5.5. These are reported diagnostics, except where C4 makes them identities.

**C3.7 Disclosure (E37-5; #37 L118–120).**
- The class label is supplied by the analyst from the prefix index.
- Class models have 4× the parameters of the global model (4×24 full, 4×16 fixed-κ, against 24 and 16).
- Success would not show that any neural system contains or consults the label.

**C3.8 Diagnostics only (E37-8).**
- κ-row norms of every map.
- **Single-prefix local fits are disabled for this package** (E39-6, #39 L116). They are not in the 541-SVD schedule, and their former optional status does not allow implementation-time expansion.
- Neither enters any outcome.

**C3.9 Voiding, unresolved cells and pooling suppression (E38-8; Q3).**
- **Voiding.** Systems whose baseline is not the true chart (SYS-FK, SYS-NC1–NC3) inherit N4(ii) per-prefix voiding. SYS-NC1–NC3 also inherit the ≥5-of-16 RESTRICTED COMPARATOR NOT ADMISSIBLE rule (v1_4_N L38–43).
- **Inadmissible systems (E39-7).** A system declared RESTRICTED COMPARATOR NOT ADMISSIBLE at stage S3 receives **no subsequent response-map fits, extended-B3 stacks or evaluation propagations**. Its skipped work is counted in its own accounting category (C8.4). Its applicable P0 check is not run, because P0 applies only to an admissible SYS-NC1 (E38-5).
- **Empty class.** A class with 0 non-voided fitting prefixes in a fold has an empty design. Its maps are **UNAVAILABLE** (C3.3(a′)).
- **Unavailable map.** In C7 and C8, a map is unavailable if its design is empty or rank-unresolved. Neither kind is formed or propagated (B1). Resolved lower-rank maps are fitted, scored and propagated.
- **B1 extension (confirmed, Q3).** Any unavailable or unresolved map required by a common-mask comparison prevents pooling of that comparison (REFERENCE RANK UNRESOLVED).
  - No missing map is replaced by a zero map.
  - No unresolved cell is silently dropped.
  - No pooled statistic is formed from a subset of resolved classes.
  - The cell-level losses that can be formed are still stored.

**C3.10 Pooling (E36-5, inherited).**
- Occurrences are pooled with their original w(a,u) and equal direction and sign weights, normalized once over the pooled scoreable occurrences.
- The class statistic pools over all 6 folds × 4 classes.
- H, S and their ratio use identical masks and weights.

**C3.11 Extended B3 rank-two guard (E38-6; #38 L330–336).**
- **(a) Justification.** For SYS-FK and SYS-NC1–NC3, J_a(u) = A_a(u)·C_μ with C_μ = D_μQ₂ᵀ, the same prefix-independent 2×8 right factor at every prefix. So any row stack of J matrices has rank ≤ 2.
- **(b) Stacking convention (frozen).**
  - For each such system, a stack is formed per fold, over the non-voided fitting prefixes.
  - Rows are ordered (prefix ascending, continuation u = 0..15, output component X, Y, XOR), giving (n_fit·48) × 8.
  - A further stack is formed per (fold, class) the same way.
  - The stack is unweighted: J itself, not √w·J. Rank of J is weight-independent when all w > 0, and every P_h(a,u) is positive (O1 exact rationals).
  - Count: 4 systems × (6 + 24) = **120 stacks** (maximum). Stacks are not formed for an inadmissible system or for an empty fitting set. Those skips are counted (C8.4).
  - Q-R5 accepted (#39 L19): unweighted fitting-prefix stacks, global and class-specific.
- **(c) Zero matrix.** If σ_1 = 0, the stack has rank 0. This is recorded, with no stop.
- **(d) Bands.**
  - σ₃/σ₁ > 10⁻⁶ is a resolved third direction: INTEGRITY STOP (exit 7), PIPELINE INVALID.
  - σ₃/σ₁ in [10⁻¹⁰, 10⁻⁶] is recorded as **UNRESOLVED-B3**, with no automatic stop (E39-8). It is never described as a passed guard. By itself it does not make a fitted response map unavailable.
  - σ₃/σ₁ < 10⁻¹⁰ passes.
- **(e) Scope.** The guard is not generalized to two-coordinate neural systems with prefix-dependent marginal-state Jacobians (C10.6).

**C3.12 Normalization and fixed rules (E38-11).**
- Every synthetic normalization (ψ̄, D_ψ for SYS-PC/SYS-LIM/SYS-O6; μ̄, D_μ for SYS-FK/SYS-NC1–NC3) is computed **once per system** at stage S3, over all 16 prefixes with exact-law P_a from O1 (`stages.py:149–154`), as in `_embed`, `stages.py:323–329`.
- Normalization is never recomputed per fold.
- Weights, draws (C5.2) and coefficient rules (C4.4.R) are fixed in the frozen file before execution.

## 4. Systems and derived expectations

**Notation.**
- θ = (μ_x, μ_y, κ) and Φ(θ,u) is the forecast.
- Output flip actions P_X = diag(−1,1,−1) and P_Y = diag(1,−1,−1) (RD arithmetic, `world.py:146–158`).
- R_X = diag(−1,1,−1), R_Y = diag(1,−1,−1), R_XY = diag(−1,−1,1).
- **Premise P0.** L_{g·a}(g·u) = P_g L_a(u) R_g and w(g·a,g·u) = w(a,u). Hence G_{g·a} = R_g G_a R_g. P0 alone does not give D1 or D6. It must be combined with the specified state map, weights, complete fitting orbits and rank conditions (Q11).

**C4.R Readout form, by system and domain (E39-11).** Affine claims are system- and domain-specific. Every exactness claim in C4 holds only where the readout is affine in z on the stated domain.

| System | Chart map z → θ | Domain of the affine claim |
|---|---|---|
| SYS-O6 | affine | all z |
| SYS-PC | affine **within a fixed sign branch** (sign(ψ₁), sign(ψ₂) unchanged) | declared non-crossing edits only |
| SYS-FK | affine (κ ≡ 0) | all z |
| SYS-NC1 | **nonlinear** (quadratic g) | none: no exact-recovery claim |
| SYS-NC2 | affine (g₂ linear in μ_x) | all z |
| SYS-NC3 | **nonlinear** (cubic g) | none: no exact-recovery claim |
| SYS-LIM | affine **within a fixed threshold branch** (sign of \|ψ₁\| − t unchanged) | declared non-crossing edits only |

v1.2 made no exactness claim for SYS-NC1 or SYS-NC3, and its SYS-PC and SYS-LIM exactness claims were already restricted to non-crossing edits. This table makes those domains explicit. The Research Lead summary's statement that every readout is affine in z (#39 L74) has no standing here.

**C4.0 P0 fixture (E38-5, E39-2, E39-10).**
- **When.** At stage S4, after system construction (stage S3) has built the required L, J and G tables, and before any intervention-response-map fit (stage S5). The SYS-NC1 coefficient refit is system construction, not a response-map fit (#39 L143).
- **Charts checked.**
  - The true chart (designs shared by SYS-O6, SYS-PC, SYS-LIM).
  - The SYS-FK product chart.
  - The SYS-NC1 chart **if SYS-NC1 is admissible** (C4.4).
  - Not SYS-NC2 or SYS-NC3, which break the symmetry by design.
- **Checks,** for every prefix a, flip g ∈ {X, Y, XY} and continuation u (g·u by reading masks 85/170, `stages.py:221`):
  - (i) L comparison: ‖L_{g·a}(g·u) − P_g L_a(u) R_g‖_max ≤ 1e-12 + 1e-10·max(‖·‖_max, ‖·‖_max) (#38 L284–286).
  - (ii) Probability invariance: P_h(g·a, g·u) = P_h(a,u) **as exact rationals from O1** (#38 L300). These are exact equalities, not byte equality of float sums.
  - (iii) G comparison: ‖G_{g·a} − R_g G_a R_g‖_max under the same formula as (i).
- **Applicability domain (E39-10).**
  - For a checked chart, comparisons (i) and (iii) for a pair (a, g) are applicable iff **both a and g·a are non-voided** on that chart. L and G are defined only at valid baselines.
  - Each omitted pair (chart, a, g, reason = VOID of a and/or g·a) is recorded.
  - Comparison (ii) is law-level and chart-independent. It covers all 16·3·16 = 768 (a, g, u) triples once.
  - The true chart has no voids by construction (O1 exact beliefs). The annex lists the domain per chart and the record format.
  - P0 on the SYS-NC1 chart is mandatory when SYS-NC1 is admissible (E39-5). It is not run when SYS-NC1 is inadmissible (E38-5 "admissible").
- **Failure.** A failed applicable P0 check stops the package: PIPELINE INVALID (P0), exit 7, no fit, no rerun. The report gives an operational failure diagnosis only, not a conclusive attribution to derivation or implementation (Q5).

**C4.1 SYS-O6: existing affine exact-filter control.**
- **Construction.** State, readout, embedding (Q, seed 35006) and edits exactly as in O6 (oracle v1.1 L83–91).
- **Inclusion (Q13).** Including it is allowed. It does not reopen, replace or retry the completed oracle package.
- **Identities (E38-3).**
  - Each global and class B equals DQᵀ within 1e-9 max abs, in every cell with resolved full rank 3.
  - In those cells, Pred_full matches actual within 1e-9 on actual-valid edits (C5.3(c)). The global and class full predictors are actual-recovery predictors, so the guard-consistency stop applies.
  - A cell without the premise reads EXPECTATION NOT APPLICABLE (RANK).
- **Comparator (descriptive).** A_(f,g) = C_μ + (ΣG_μμ)⁻¹(ΣG_μκ)c_κ over the class's fitting prefixes. The adjustment to C_μ is generally nonzero within a class, so the class comparator loss may differ from the O6 global value (UNVERIFIED).

**C4.2 SYS-PC: sign-dependent positive control.**
- **(a) State.** ψ = (μ_x, μ_y, τ) with τ = sign(μ_xμ_y)·κ. τ is flip-invariant, so it is constant within an orbit. z = Q·D_ψ⁻¹(ψ − ψ̄), with Q from seed 35006 (reused, Q10) and system-level normalization (C3.12).
- **(b) Readout (autonomous; Q8 confirmed).** ψ = D_ψQᵀz + ψ̄, then θ = (ψ₁, ψ₂, sign(ψ₁ψ₂)·ψ₃). The marginal coordinates carry the signs used by the readout. The baseline chart is the true θ_a, so L, the weights and the designs are identical to SYS-O6's.
- **(c) Local map (E38-2).** C = D_ψQᵀ with rows c_x, c_y, c_τ, and S_a = diag(1,1,χ_a).
  - On a non-crossing edit the **chart increment S_g C δ is exact**: θ' = θ_a + S_g C δ.
  - J_a δ = L_a S_g C δ is the **first-order** forecast response.
- **(d) D1, global fit (UNVERIFIED; #38 L13–38).**
  - With P0, Σ_g G_{g·r} = 4·diag(G_r[xx], G_r[yy], G_r[κκ]) and Σ_g G_{g·r}S_g = 4·diag(G_r[xx], G_r[yy], 0).
  - For fit sets that are unions of complete orbits, and given the C3.3(b) rank premise: **B_global = [c_x; c_y; 0]** and **A_global = [c_x; c_y]**.
  - The two predicted perturbed charts are equal, so their finite forecast predictions are equal wherever propagation is defined.
  - **Residual.** The exact finite discrepancy is Φ(θ_a + S_gCδ, u) − Φ(θ_a + B_global δ, u), computed by propagation (C5.6). L_a[:,κ]χ_a c_τ δ is only its first-order approximation (#38 L40–57).
- **(e) D2, class fit (UNVERIFIED; #38 L61–73).**
  - Within class g, J_a = L_a S_g C. If the stacked class full design has **resolved full column rank 3**, least squares uniquely recovers **B_(f,g) = S_g C**, and finite prediction is exact on valid non-crossing edits.
  - Otherwise the cell reads EXPECTATION NOT APPLICABLE (RANK), and for VALIDATION that is NOT MET (RANK) (C7.2).
  - **D3.** A_(f,g) = C_μ + χ_g(ΣG_μμ)⁻¹(ΣG_μκ)c_τ. **The adjustment to C_μ is generally nonzero** (#38 L96).
  - When the full predictor is exact on the evaluated edits, L_full = 0, so class gain = L_μ,class ≥ 0 (#38 L85–94). The non-negativity follows from exactness, not from nesting.
  - The magnitude of L_μ,class is not derived. No equality with O6's R follows.
- **(f) Sign boundaries and crossing rule.**
  - The boundaries are ψ₁ = 0 and ψ₂ = 0.
  - An edit crosses if sign(ψ'_i) ≠ sign(ψ_{a,i}) or ψ'_i = 0 for i ∈ {1,2}.
  - A crossing edit is not scoreable for any SYS-PC model. It enters the common mask, is counted and is never replaced.
  - **Bound (#38 L229–247 confirmed).** |Δψ_i| = ε_syn·sd_i·|q_iᵀv| ≤ ε_syn·sd_i.
    - With the displayed (rounded) sd_x = 0.36806 and sd_y = 0.61364, the bounds at ε_syn = 0.25 are 0.0920 and 0.1534.
    - The corresponding margins are min|μ_x| = 0.2501 and min|μ_y| = 0.4276 (`stage_O1.json`).
  - **Full precision governs (#38 L249).** The package computes D_ψ under C3.12 and the bound from it at stage S3, before any edit. The displayed numbers explain the bound and do not govern it.
  - An observed crossing under these premises is an integrity failure (exit 7), with no replacement edit (#38 L251).
- **(g) Global identity checks (E38-4).** In every fold, and where stated in every (group, ε_syn) cell:
  - (i) ‖B_global − [c_x;c_y;0]‖_max ≤ 1e-9.
  - (ii) ‖A_global − [c_x;c_y]‖_max ≤ 1e-9.
  - (iii) max|Pred_full − Pred_μ| ≤ 1e-9, checked on edits where **both global predicted beliefs are valid**, independently of the actual belief and of the class predictors' masks (E39-4; #39 L24–36). SYS-PC global does not require Pred_full = actual. Ordinary invalid global predictions are coverage exclusions, not identity failures, and the guard-consistency stop does not apply to them. The tested-edit count is reported.
  - (iv) |L_μ − L_full| ≤ 1e-18 + 1e-9·S per (fold, group, size) cell. This is reported as a consequence and is never the sole definition.
  - All four pass: GLOBAL CANCELLATION AS DERIVED.
- **(h) Class identity checks.** In every (fold, class) cell with the premise:
  - ‖B_(f,g) − S_gC‖_max ≤ 1e-9.
  - max|Pred_full − actual| ≤ 1e-9 on actual-valid non-crossing edits. The class full predictor is an actual-recovery predictor, so the guard-consistency stop of C5.3(c) applies.
  - All pass: CLASS RECOVERY AS DERIVED.

**C4.3 SYS-FK: globally zero-κ control on product-chart designs (E38-10).**
- **State.** z = Q₂·D_μ⁻¹(μ − μ̄), Q₂ from seed 35007 (reused, Q10).
- **Readout.** θ = (μ_x, μ_y, 0). The baseline chart is (μ_a, 0). Disagreement with the true reachable forecasts is reported separately.
- **Validity (RD arithmetic; UNVERIFIED).** The minimum baseline product-belief p is ≈ 0.0317, and ≥ 0.0074 under the edit bound at ε_syn = 0.25. Both are above 10⁻⁶. The package recomputes this.
- **D4 (UNVERIFIED; E38-3).** J_a = L_a[:,μ]·C_μ.
  - **If the design has resolved full column rank**, B = [C_μ; 0], and A = C_μ when the μ design has rank 2.
  - Pred_full = Pred_μ = actual, so L_full = L_μ = 0, gain 0 and S > 0.
  - v1.1's "for every resolved design" is withdrawn (#38 L73).
- **Checks (per cell with premise).**
  - B and A recovery ≤ 1e-9.
  - max|Pred_full − actual| and max|Pred_μ − actual| ≤ 1e-9 on actual-valid edits. All four SYS-FK predictors are actual-recovery predictors, so the guard-consistency stop applies.
  - Zero gain per required cell, using that cell's common-mask losses and S: |L_μ − L_full| ≤ 1e-18 + 1e-9·S.
    - Global: per fold/group/size.
    - Class: per **fold/class/group/size** (Q-R2 confirmed, #39 L16).
    - These checks are never replaced by a pooled check.
  - All pass: FIXED-κ IDENTITY AS DERIVED.
- **Scope statement (report verbatim):** "FK checks the κ row on the product-chart designs, not on the SYS-O6/SYS-PC designs." FK's design ranks are reported next to SYS-O6/SYS-PC's.
- **Alternatives (corrected per E38-10, #38 L206–227).**
  - A globally constant κ cannot reproduce true baselines that have different κ values.
  - But autonomous same-baseline controls with κ fixed under the declared interventions **can** exist. For example, a frozen register r initialized to κ_a and left unchanged by edits (#38 L214–221). That would be an intervention-fixed control.
  - A two-coordinate plateau construction is also not excluded (#38 L225).
  - Both are outside this package and **are not added**. No impossibility of same-baseline autonomous controls is claimed.

**C4.4 SYS-NC1–NC3: descriptive two-coordinate confounds (E37-7; #38 L160, L186). Not negative controls.**
- **Construction.** z = Q₂·D_μ⁻¹(μ − μ̄) with chart (μ_x, μ_y, g_k(μ)).
  - Derivatives and finite predictions are taken about the system's own baseline.
  - Validity is checked per prefix, with N4(ii) voiding.
  - No refit after inspection and no replacement.
  - Extended B3 per C3.11.
- **SYS-NC1 = O7 lookup: a varying-κ two-coordinate confound** (#38 L160). Its g is the O7 P-weighted quadratic fit recomputed in-package. Committed `stage_O7.json` `g_coefficients`: g ≈ 0.1404·μ_xμ_y.
  - **Global.** Pred_full ≡ Pred_μ is expected only if 0 prefixes are voided and the NOTE_1 N1 rank premise holds (C3.3(b)). It is reported with the zero-gain formula, as a descriptive identity, not a validation item. Otherwise it reads EXPECTATION NOT APPLICABLE (RANK), or not applicable (voids). SYS-NC1's mandatory P0 check is separate and does remain mandatory (E39-5).
  - **Class.** A gain of either sign is permitted and reported.
- **SYS-NC2.** g₂ = c₂μ_x, an affine symmetry-breaking confound.
  - **D5 (UNVERIFIED).** Dg₂ is constant, so the full model is exact **when the design has resolved full column rank** (E38-3). Gain = L_μ ≥ 0 under the exactness premise.
  - Reported. It is not evidence of a covariance register.
- **SYS-NC3.** g₃ = c₃μ_x³, a cubic confound (Q7 accepted). No gain expectation; reported.
- **Comparison caveat (#38 L186).** NC2 and NC3 differ in baselines and derivatives, so the pair is not a comparison in which only functional form changes. Equal gradient RMS does not imply equal forecast response, conditioning or transferability (E38-11).

**C4.4.R RMS-matching rule (Q7 accepted; E38-11).**
- **Rule.** ρ(g) = sqrt(Σ_a P_a‖Dg(μ_a)‖²), with **P_a the exact-law prefix probabilities from O1** (`stages.py:149–154`) and μ_a the exact stage-4 marginals.
  - ρ_NC1 is computed from SYS-NC1's g.
  - The in-package O7 refit must equal the committed `g_coefficients` within the C3.6(e)-type tolerance (#38 L284–286). Otherwise INTEGRITY STOP.
  - c₂ = ρ_NC1. c₃ = ρ_NC1 / (3·sqrt(Σ_a P_a μ_{x,a}⁴)). Both are unique and positive, because every |μ_x| ≥ 0.2501.
- **Values: c₂ = TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW; c₃ = TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW.**
  - They are computed at stage S3 before any response-map fit, recorded, and never changed (Q7: "No coefficient adjustment after inspection"). Values computed under these frozen rules are permitted execution outputs (E39-9; #39 L72).
  - My earlier values came from probabilities reconstructed from rounded SDs and are withdrawn (change log 8).
  - Neither I nor this record computes the exact-law values. `stage_O1.json` stores the exact stage-4 charts but not P_h or P_a: its keys are listed in §12, and `stages.py:285–291` builds P_a only in memory. So exact-law P_a needs the O1 filter run, which is excluded here.
  - **Frozen arithmetic (NOTE_1 N3 as clarified by #39 L61–70; E39-9).**
    1. P_a_exact = Σ_u P_h(a,u) in exact rationals (O1 history probabilities).
    2. P_sum_exact = Σ_a P_a_exact in exact rationals. **Assert P_sum_exact == 1.** On failure: PIPELINE INVALID (normalization), stop, nothing rescaled.
    3. P_sum_float = float(P_sum_exact), converted once.
    4. P_a_float = float(P_a_exact), converted once per prefix.
    5. **Frozen summation order.** ρ_NC1² and M4 = Σ_a P_a_float·μ_{x,a}⁴ are each accumulated in float64 as a sequential left-to-right sum over a = 0, 1, …, 15. Each term is formed as P_a_float × (term in float64), with no pairwise, compensated or library reduction. ‖Dg‖² = (∂g/∂μ_x)² + (∂g/∂μ_y)², evaluated from the refitted coefficients with the inherited `g_gradient`.
    6. c₂ = ρ_NC1 / sqrt(P_sum_float) (#39 L67). c₃ = ρ_NC1 / (3·sqrt(M4)), unchanged, because the scale cancels (NOTE_1 N3).
  - **SYS-NC1 refit input.** The in-package O7 refit reproduces the inherited construction exactly, including its float P_a accumulation (`stages.py:286–291`, `stages.py:745–751`), because it must equal the committed `g_coefficients`. The RMS rule uses P_a_float from step 4. The two P_a representations are intentional; see the CNA first-look list (§12.4).
- **Admissibility.** If any matched baseline is invalid (p < 10⁻⁶), the system is RESTRICTED COMPARATOR NOT ADMISSIBLE, with no rescaling. Admissibility is not predicted here.

**C4.5 SYS-LIM: orbit-indexed limit control, REPORTED ONLY (E38-9; Q14, Q15, Q17).**
- **Purpose.** It exposes a limitation of the selected constant-per-class maps (#38 L192).
- **Midpoint (exact law).** t = (|μ_x|_A + |μ_x|_D)/2 from the exact `stage4_chart_exact` rationals:
  - |μ_x|_A = 2640740184/4981285969 (≈ 0.530132);
  - |μ_x|_D = 867714984/3134384719 (≈ 0.276837);
  - **t = 6299716077234553896/15613266622202707711** (≈ 0.403484820292257; RD arithmetic, exact rational from committed data).
  - The package recomputes t from O1 and compares exactly.
  - s_A = +1, s_B = s_C = s_D = −1. The margin is ≈ 0.126647. No additional split (Q14).
- **State and readout.** ψ = (μ_x, μ_y, s(|μ_x|)·κ), z = Q·D_ψ⁻¹(ψ − ψ̄), system-level normalization. The readout reads the threshold from the state's own |ψ₁|, which is autonomous (Q17, #38 L204). The baseline is the true chart.
- **Crossing bound (#38 L239–245 confirmed).** ||ψ'₁| − |ψ₁|| ≤ |Δψ₁| ≤ ε_syn·sd_x. With the displayed sd_x = 0.36806:

  | ε_syn | ε·sd_x |
  |---|---|
  | 0.02 | 0.00736 |
  | 0.05 | 0.01840 |
  | 0.10 | 0.03681 |
  | 0.25 | 0.09201 |

  All are below the margin 0.126647. The full-precision bound is computed by the package (#38 L249). An observed crossing is an integrity failure.
- **D6 global (UNVERIFIED; uses P0; diagnostic only).** Premise per NOTE_1 N1 (C3.3(b)): global full rank 3 and μ design rank 2. Otherwise EXPECTATION NOT APPLICABLE (RANK). The result stays REPORTED ONLY.
  - λ = (s₁K₁ + s₂K₂)/(K₁ + K₂), where K_o = Σ_{a∈o} G_a[κκ]. B = [c_x; c_y; λc_τ] and A = [c_x; c_y].
  - **CD/BD/BC fitting folds.** λ = −1, so the held-out A gets the wrong sign. The **first-order** loss on A is L_full ≈ 4·E_A against L_μ ≈ E_A.
  - **A-containing folds.** λ = (K_A − K_X)/(K_A + K_X). The **first-order** ratio is L_full/L_μ ≈ (1+λ)², and (1+λ)² < 1 iff K_A < K_X.
  - **These loss-scaling statements are Jacobian-level only and are not asserted at finite ε_syn (E38-2, #38 L118–120).** Reported with no sign expectation.
- **D7 class (diagnostic).** In the CD, BD and BC fitting folds, full-rank recovery gives B_(f,g) = diag(1,1,−1)·C, the negative-sign chart map. It is wrong on held-out A whenever the edit has a nonzero relevant component (#38 L194).
  - D7 is reported as an analytic diagnostic.
  - A failure of an exact, applicable D7 identity is flagged **D7 INVESTIGATE** (#38 L198; Q-R1 accepted, #39 L15; E39-8).
    - It is non-stopping and changes neither VALIDATION nor HEADROOM.
    - It is retained prominently in the report.
    - It **accompanies any later decision about neural work**, which must address it. Unchanged labels do not resolve the discrepancy.
- **Limit exposed (E38-9).** The negative result concerns the specified global and flip-class map families. It does not establish impossibility for predictors given a different declared transport rule: a rule using the state's magnitude could represent this system (#38 L196).

## 5. Units, edits, masks, weights, groups, tolerances

- **C5.1 Units.** All systems are synthetic. An edit is δ = ε_syn·sign·v in the 8-D synthetic state, with field `eps_syn`.
- **C5.2 Edits and draws (Q10, Q12).**
  - **Directions.** The 16 unit directions of seed 35016 (the O6/O7 array), applied as +v then −v.
  - **Embeddings.** Q (35006) and Q₂ (35007) are reused with their generation conventions and hashes. The reuse is disclosed as development-informed.
  - **Provenance (E39-10; #39 L171).** The package loads the **authenticated existing arrays** from the committed `drawn_arrays.npz` and verifies each per-array raw-byte sha256 before use. It does not regenerate them. Hashes, generator, dimensions, ordering, normalization and sign conventions are in the implementation annex (§9, C9.6).
  - **Sizes.** ε_syn ∈ {0.02, 0.05, 0.1, 0.25}, with 0.1 the sole headroom reference (`pinned.py:28–29`).
  - **Per system:** 6 folds × 8 evaluation prefixes × 16 continuations × 32 signed directions × 4 sizes = 98,304 edits. Per fold per size that is 4,096 (`stages.py:48` `EDITS_PER_FOLD` = 8·16·16·2).
- **C5.3 Masks and identity domains (E38-7).**
  - **(a) Common mask (comparative losses).** An edit is scoreable for the comparison iff the actual perturbed belief and all four predicted perturbed beliefs (global full, global μ, class full, class μ) pass p ≥ 10⁻⁶.
    - For SYS-PC and SYS-LIM, the edit must also be non-crossing.
    - The same mask governs L_μ, L_full and S for both fit types.
    - Coverage is reported per fold, class and size.
  - **(b) Matrix identities** (C4.1, C4.2(g)(i)–(ii), C4.2(h), C4.3) are checked on the fitted matrices **before** any evaluation masking.
  - **(c) Finite recovery identities (E38-7, E39-3, E39-4).**
    - **Actual-recovery predictors.** Checked on **actual-valid, non-crossing** edits in cells where the exactness premise applies, and not restricted to the common mask. These predictors are:
      - SYS-O6 global and class Pred_full;
      - SYS-PC class Pred_full;
      - SYS-FK global and class Pred_full and Pred_μ.
    - **Guard consistency (actual-recovery predictors only).** If the actual perturbed belief passes the p ≥ 10⁻⁶ guard and such a predictor's belief fails it, that is a **stopping guard inconsistency** (PIPELINE INVALID, operational).
      - The report gives the actual and predicted minimum probabilities, the chart difference and the available recovery residual.
      - It describes the event as a guard inconsistency, not as proof that the 1e-9 tolerance was exceeded (#39 L38–40).
      - Neither the guard nor the tolerance is relaxed after it is seen.
    - **SYS-PC global** (Pred_full = Pred_μ) is **not** an actual-recovery identity. It is checked where both global predicted beliefs are valid (C4.2(g)(iii)). Its invalid predictions are coverage exclusions (E39-4).
    - **Streaming (E39-3).** Every finite identity and guard-consistency check runs during stage S6 as soon as its values exist. Maxima and tested-edit counts accumulate per identity cell. An applicable stopping failure stops further evaluation immediately.
    - **Tested-edit count.** Every identity report includes the number of tested edits. A cell with an empty test domain is **NOT EVALUATED**, not passed (E39-3, #39 L156).
  - **(d) Other predicted-belief guard failures** are coverage exclusions. All identity checks keep their fold and ε_syn resolution, and gain identities keep their group resolution (E38-4).
- **C5.4 Weights and groups.**
  - w(a,u) = P_h(a,u), with uniform direction, sign and size weights.
  - The groups ALL, MARG and XOR are reported separately. Outcomes use ALL and MARG at ε_syn = 0.1.
  - R-type ratios are worded per E37-3.
- **C5.5 Tolerances (Q9; #38 L278–302, verbatim).**

```text
Matrix/forecast recovery:
    max absolute error <= 1e-9

P0 L and G comparisons, and applicable C3.6(e) identities:
    ||A - B||_max
        <= 1e-12 + 1e-10 * max(||A||_max, ||B||_max)

Cancellation sums expected to equal zero:
    ||sum_i T_i||_max
        <= 1e-12 + 1e-10 * sum_i ||T_i||_max

Zero-gain identities:
    |L_mu - L_full| <= 1e-18 + 1e-9 * S
```

  - **Gain tolerance granularity (#38 L296).** It applies within each required fold/group/size cell, using that cell's common-mask losses and S. Pooled equality cannot override a failing cell. The absolute difference and its scale are reported.
    - For class fits, the required cell is fold/class/group/size. This is my proposal (Q-R2).
  - These are prospective acceptance conventions, not certified forward-error bounds. They are not loosened if a poorly conditioned fit fails (#38 L298).
  - **Exact probabilities.** Probability invariance uses O1's exact rationals (#38 L300).
  - **Inherited.** The rank bands and the headroom BOUNDARY convention (relative 10⁻⁶, v1_4_N L16) are retained (#38 L302).
  - **Exact-zero flags** are reported separately from tolerance checks (E37-2).
- **C5.6 Finite discrepancies (E38-2).** Every loss uses finite forecasts: the actual perturbed chart and each predicted perturbed chart are each propagated through Φ (5 propagations per edit, §8). No first-order surrogate enters any loss.

## 6. Confound treatment: descriptive-only (selected; E38-1; #38 L136–186)

- **Selection.** The descriptive-only treatment is selected (#38 L5, L138).
  - It applies to confound interpretation.
  - The implementation identities and the separate SYS-PC headroom assessment remain.
- **Confound systems.** SYS-NC1–NC3 are fitted with the same plain maps as every other system and reported descriptively, with no gain-must-vanish criterion and no floor.
  - A positive confound gain is "compatible with two-coordinate mediation" (E37-7). **This applies to SYS-NC1–NC3 only.** It is not used to classify SYS-LIM as a two-coordinate system (E39-11).
- **SYS-LIM** is also reported only, with no gain criterion, but it is **not** a two-coordinate confound. Its state is three-coordinate, with an orbit-indexed κ sign (C4.5).
  - It does not identify a register and does not exclude two-coordinate mediation or reachable-set lookup (E38-15).
- **What is not used.** No measured confound ratio is carried forward as a hurdle, floor or calibration for any neural study (#38 L158).
- **Withdrawn alternatives,** each with its source:
  - v1 Option B: Q2a, L164.
  - B-repaired / shared e / D2′: Q2b, L183. Astra accepts the D2′ algebra as conditional mathematics only.
  - Tied bilinear: Q2c.
  - Option A floor: L158.
  - Option C: L184.

## 7. Outcome labels and order

**C7.0 Flag storage (E38-8).** For every system, fit type, fold, class, group and size, the package stores:
- every admissibility, voiding, rank (with premise status) and coverage flag;
- the crossing counts;
- the identity residuals with their tolerances.

This holds even when a higher-priority display label applies.

**C7.1 Per-statistic labels.** Labels are formed per system, fit type and group (ALL, MARG) at ε_syn = 0.1. Other sizes are reported. Identity checks use every size. **First match wins:**
1. **PIPELINE INVALID (operational failure diagnosis; Q5).** Any of the following stops the package, with no rerun:
   - an O1 or O2 fixture failure;
   - an applicable P0 failure (C4.0);
   - an applicable control-identity failure: SYS-O6 (C4.1), SYS-PC global (C4.2(g)) or class (C4.2(h)), SYS-FK (C4.3), in a cell whose premise holds;
   - a resolved extended-B3 third direction (C3.11);
   - an observed SYS-PC or SYS-LIM crossing;
   - an SYS-NC1 refit mismatch;
   - a failed exact normalization assertion (C4.4.R step 2; E39-9);
   - a stopping guard inconsistency for an actual-recovery predictor (C5.3(c); E39-4);
   - an integrity condition of C8.6.

   Finite identity and guard checks are evaluated during stage S6 as their values become available, and they stop further evaluation at once (E39-3).

   The diagnosis names the failed check. It does not conclusively attribute the failure to derivation or implementation.
2. **CAP REACHED / CAP RESERVE REACHED (INCOMPLETE) / PROJECTION HALT** (C8.5). This is incomplete work, not a scientific negative.
3. **REFERENCE COVERAGE NOT MET.** Count coverage < 75% (4·n_s < 3·n_t) or law-mass coverage < 0.75·(1 − 10⁻⁶) in some fold, or for class statistics some fold×class.
4. **REFERENCE RANK UNRESOLVED.** A required map is unresolved or unavailable (C3.9). No pooled statistic is formed.
5. **RESTRICTED COMPARATOR NOT ADMISSIBLE** (SYS-NC1–NC3): ≥5 of 16 prefixes voided, or a matched baseline invalid.
6. **ZERO RESPONSE.** Pooled S = 0 exactly.
7. **Identity statistics** (SYS-O6; SYS-PC global and class; SYS-FK): IDENTITY AS DERIVED; EXPECTATION NOT APPLICABLE (RANK) per cell with a resolved lower rank (E38-3, N2); or **NOT EVALUATED** per cell with an empty test domain (E39-3). Each comes with its tested-edit count.
8. **Reported statistics** (SYS-NC1–NC3, SYS-LIM, and every global gain other than the SYS-PC/SYS-FK identities): REPORTED. Negative gains are kept (#38 L94). D7 INVESTIGATE flags, if any, are reported.

**C7.2 VALIDATION (E38-12, E39-5, E39-8).** **CLASS-FIT VALIDATION MET** iff:
- O1, O2 and every applicable P0 check passed. This includes the mandatory SYS-NC1 P0 check when SYS-NC1 is admissible (E39-5);
- every required control identity holds and has its rank premise (SYS-O6 global and class; SYS-PC global, all four checks of C4.2(g); SYS-PC class; SYS-FK both fit types);
- no required identity is NOT EVALUATED. An empty identity domain is not a passed identity (E39-3, #39 L156);
- no required cell is REFERENCE RANK UNRESOLVED or UNAVAILABLE.

Otherwise it reads **CLASS-FIT VALIDATION NOT MET (<first failing reason>)**.
- A required SYS-PC class cell with EXPECTATION NOT APPLICABLE (RANK) gives **NOT MET (RANK)** (E38-12, Q15).
- For SYS-O6 and SYS-FK, a required cell lacking its premise likewise prevents VALIDATION MET (Q-R3 confirmed, #39 L17; E39-8).
  - A resolved lower rank gives NOT MET (RANK).
  - An unresolved rank gives NOT MET (REFERENCE RANK UNRESOLVED).
  - The two are kept distinct (#39 L17).
- **Confound gains and descriptive expectations do not enter VALIDATION.** That covers the SYS-NC1–NC3 gains, the SYS-NC1 global descriptive identity, SYS-LIM, D6 and D7. **Mandatory applicable integrity checks, including P0, remain mandatory** (E39-5; #39 L158). VALIDATION does not depend on any gain magnitude.

**C7.3 SYS-PC HEADROOM (E38-12; Q4).**
- **Formation and eligibility (E39-5; #39 L147–156).** VALIDATION MET is necessary but not sufficient. A threshold label is issued only if all of the following hold:
  1. VALIDATION MET;
  2. the required SYS-PC maps are available and no required fit is unresolved;
  3. the declared count and law-mass coverage (C7.1 item 3 rule) hold in **every required fold/class at ε_syn = 0.1**;
  4. the scoreable denominator is positive;
  5. S > 0.

  Missing eligibility receives its applicable status: NOT FORMED (VALIDATION NOT MET), REFERENCE RANK UNRESOLVED, UNAVAILABLE, REFERENCE COVERAGE NOT MET or ZERO RESPONSE. It **cannot yield HEADROOM MET**. Diagnostic values are stored where permitted.
- **Statistic.** **H = L_μ,class** for SYS-PC at ε_syn = 0.1, with √H and R = H/S, for ALL and MARG.
- **Thresholds (synthetic reporting conventions only).** ALL √H ≥ 10⁻³ and R ≥ 0.05; MARG √H ≥ 10⁻⁴ and R ≥ 0.02 (`pinned.py:24–27`). Labels are HEADROOM NOT MET / BOUNDARY / MET under the inherited band rule (v1_4_N L15–16).
- **No prediction** is made that SYS-PC will meet them.
- They supply no neural response floor (#37 L164).

**C7.4 What the labels license.** VALIDATION MET with SYS-PC HEADROOM MET licenses only a decision on whether a neural specification is warranted. SYS-LIM and the confound results go with any such decision as stated limits. So does any D7 INVESTIGATE flag, which that decision must address (E39-8; #39 L15).

## 8. Execution specification and accounting (E38-13, E38-14, E39-2, E39-3, E39-6, E39-7)

The counts below are **scheduled maxima derived from the frozen design**. Each is a product of declared factors, with sources cited. None is measured. Outcome-dependent reductions are accounted for by C8.4 and never appear as unexplained mismatches. #39 checked the propagation, fit and SVD arithmetic (#39 L78–92). The workload, runtime and memory remain **UNVERIFIED**.

**C8.0 Label hygiene.** In this record, stage labels are always written "stage S0" … "stage S8". They mean only the execution stages of C8.1. Systems are always "SYS-…", so the two label sets cannot collide. The same tokens appear with other meanings in quoted raw text:
- E37-1 "S12 or S15" names other study items;
- E37-4 "S6" names an earlier prospective neural design;
- #38 L5 "S6/Q1" names a part of the #38 question packet.

v1.2's own stage numbering is superseded: v1.2's S3 (P0) and S4 (construction) are swapped here, per E39-2. Any citation of a v1.2 stage label must be translated.

**C8.1 Stage order (E39-2; #39 L128–143).**

| Stage | Content | Φ propagations (max) |
|---|---|---|
| S0 | Wrapper T0 before imports; preflight; manifest, annex and input hash checks; authenticated array check; runtime versions recorded as observations; RLIMIT_AS set by wrapper | 0 |
| S1 | O1 exact fixtures (inherited): 16 prefix filters + 256 terminal forecasts, exact; exact P_h retained | 272 exact (`pinned.py:11`; `results.json:70`) |
| S2 | O2 closed-form L vs finite-difference check (inherited) | 1,536 float (`results.json:4`) |
| S3 | System construction for all 7 systems: system-level normalization; SYS-NC1 coefficient refit and committed-coefficient check; exact normalization assertion; c₂, c₃; exact t; baseline validity, voiding and admissibility; L, J and G tables; full-precision crossing bounds | 0 |
| S4 | Applicable P0 checks on the true, SYS-FK and admissible SYS-NC1 charts, with domains and omitted pairs (C4.0) | 0 |
| S5 | Response-map fits for admissible systems (global and class, full and fixed-κ); rank reports; extended-B3 stacks; normal-equation terms; matrix identities (C5.3(b)); fit freeze: write and fsync `fit_freeze_<system>.json` | 0 |
| S6 | Baselines and finite evaluation, systems in the fixed order SYS-O6, SYS-PC, SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3, SYS-LIM. Per admissible system: 256 baseline propagations, then 5 propagations per edit, with **streaming** finite-identity and guard-consistency checks (E39-3). The first 1,000 stage-S6 propagations are the timing sample (`pinned.py:41`; E36-13 projection) | 3,442,432 |
| S7 | Final aggregation of stored residuals and losses; pooling; labels; flags (C7). No deferred finite-identity checking | 0 |
| S8 | Reporting and post-run records: report, results serialization, wrapper post-run index | 0 |

No intervention-response-map fit precedes the applicable P0 checks (E39-2). The event ordering inside each stage is fixed in the annex (A6).

**C8.2 Cache policy (Q-R6 accepted, #39 L20).**
- **L tables.** One closed-form table of 256 L_a(u) per **distinct baseline chart**, built at stage S3: true chart (shared by SYS-O6, SYS-PC, SYS-LIM and used by O2), SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3. That gives 5 tables, **1,280 L evaluations** at most. No L is evaluated at a voided baseline, and no table is built for an inadmissible system. P0 reads these tables and computes no new L.
- **Baseline forecasts.** Propagated **per system** (256 each, 1,792 total), with no cross-system sharing. For true-chart systems they are compared with O1's exact forecasts as a reported check.
- **Predictions.** No deduplication. Every scheduled actual and predicted propagation is attempted as scheduled, unless C8.4 skips it.
- **Fits.** Not cached across systems.

**C8.3 Accounting table (scheduled maxima).**

Notation: F = 6 folds; K = 4 classes; E = 8 evaluation prefixes per fold (2 per class); U = 16 continuations; V = 16 directions × 2 signs = 32; Z = 4 sizes; N_sys = 7.

| Item | Formula | Count | Source |
|---|---|---|---|
| Edits per (fold, size) | E·U·V | 4,096 | `stages.py:48` |
| Edits per (fold, class, size) | 2·U·V | 1,024 | C3.1 |
| Edits per system | F·E·U·V·Z | 98,304 | C5.2 |
| Edits, all systems | 7 × 98,304 | 688,128 | — |
| Propagations per edit | actual + global full + global μ + class full + class μ | 5 | C5.6 |
| Edit propagations per system | 98,304 × 5 | 491,520 | — |
| Baseline propagations per system | 16 prefixes × U | 256 | C8.2 |
| S6 propagations per system | 491,520 + 256 | 491,776 | — |
| **S6 propagations, all systems** | 7·(98,304·5 + 256) | **3,442,432** | #38 L369 |
| O2 float propagations | 16·16·3·2 | 1,536 | `results.json:4` |
| **Scheduled float propagations, package maximum** | 3,442,432 + 1,536 | **3,443,968** | — |
| Exact propagations (O1) | 16 + 256 | 272 | `pinned.py:11`; `results.json:70` |
| Additional diagnostic Φ propagations | none declared | 0 | C8.1 |
| Closed-form L evaluations | 5 charts × 256 | 1,280 | C8.2 |
| J evaluations | 7 × 256 | 1,792 | C3.2 |
| Validity-guard evaluations, edits | equal to edit propagations | 3,440,640 | C5.3 |
| Validity-guard evaluations, baselines | 7 × 16 | 112 | C3.9 |
| Weighting modes per loss | weighted, unweighted | 2 | C3.6(c) |
| Weighted LS fits per system | F·(2 global + 2K class) | 60 | C3.2 |
| Weighted LS fits, all systems | 7 × 60 | 420 | — |
| SYS-NC1 g refit | 1 | 1 | C4.4.R |
| Extended-B3 stacks (SVD) | 4 systems × (F + F·K) | 120 | C3.11 |
| **SVDs total** | 420 + 1 + 120 | **541** | — |
| Stored fitted matrices | 7 × 60 | 420 | C3.6(a) |
| Stored G_a / r_a | 7 × 16 each | 112 / 112 | C3.6(d) |
| Stored normal-equation sums | 7 × 30 cells × {ΣG, Σr, ΣG_μμ, Σr_μ} | 840 | C3.6(d) |
| Rank reports | = SVDs | 541 | C3.6(b) |
| Orbit cancellation sums | 7 × 4 orbits × 3 scalars, plus 3 × 4 Σ G[κκ]Dg vectors (NC1–NC3) | 84 scalars + 12 vectors | C3.6(e) |
| P0 L comparisons | ≤ 3 charts × 16 × 3 flips × U | ≤ 2,304 | C4.0 |
| P0 G comparisons | ≤ 3 × 16 × 3 | ≤ 144 | C4.0 |
| P0 exact probability comparisons | 16 × 3 × U (law-level, chart-independent) | 768 | C4.0 |
| Logical loss cells per (system, fit type) | F·K·2 orbits·3 groups·Z | 576 | C3.6(c); #39 L101 |
| **Mode-indexed base loss records, all systems** | 7 systems × 2 fit types × 2 modes × 576 | **16,128** | E39-6; #39 L108 |
| Quantities per base record | L_μ, L_full, S, gain (+ scoreable count, law mass) | 4 (+2) | E39-6 |
| Stored pooled aggregates | 7 × 2 fit types × 3 groups × Z × 2 modes | 336 | C3.10 |
| Global orbit-level aggregates | derivable from base records; not stored | 0 | E39-6 |
| Coverage records | 7 × (F·Z per fold + F·K·Z per fold×class) | 7 × (24 + 96) = 840 | C5.3 |
| Identity cells, SYS-O6 | matrices 6 + 24; recovery F·Z + F·K·Z | 30 + 120 | C4.1 |
| Identity cells, SYS-PC global | matrices 12; Pred equality F·Z; loss F·3·Z | 12 + 24 + 72 | C4.2(g) |
| Identity cells, SYS-PC class | matrices 24; recovery F·K·Z | 24 + 96 | C4.2(h) |
| Identity cells, SYS-FK | matrices 60; recovery 2 predictors × (F·Z + F·K·Z); zero gain F·3·Z + F·K·3·Z | 60 + 240 + 360 | C4.3 |
| SYS-NC1 global descriptive identity | F·3·Z | 72 | C4.4 |
| D7 diagnostic matrices (SYS-LIM) | 3 folds × K | 12 | C4.5 |
| D6 diagnostic matrices (SYS-LIM; NOTE_1 N1) | F | 6 | C4.5 |
| **Identity cell records, total** | 150 + 108 + 120 + 660 + 72 + 12 + 6 | **1,128** | C4, C5.3 |
| Guard-consistency records (actual-recovery cells) | SYS-O6 120 + SYS-PC class 96 + SYS-FK 240 | 456 | C5.3(c) |
| P0 omitted-pair records | ≤ 2 charts (SYS-FK, SYS-NC1) × 16 × 3 | ≤ 96 | C4.0 |
| Single-prefix local fits | disabled | 0 | E39-6 |
| Core stage files written | stages S0, S1, S2, S3, S4; 7 fit_freeze (S5); 7 evaluation (S6); results (S7); report (S8) | 21 | #39 L122 |
| Additional files, listed separately | wrapper post-run index; run log (durable counters); stop record | 3 | #39 L122; annex A5 |

**C8.4 Terminal accounting categories (E38-13, E39-7; #39 L118–120).** Every scheduled propagation, fit and B3 stack receives **exactly one** terminal category:
- **ATTEMPTED.** Any call that was started, whatever its outcome. Attempted propagations are sub-classified as valid-finite, guard-invalid (stored null, counted), ValueError or non-finite, following the inherited policy (`stages.py:95–121`). A scoreable-edit failure stops the package (`stages.py:103–116`).
- **For an unattempted call, the first applicable reason wins:**
  1. **SKIPPED: PRIOR STOP.** Any stop (integrity, P0, identity, guard inconsistency, normalization, cap, reserve, projection halt) that occurred before the call.
  2. **SKIPPED: SYSTEM INADMISSIBLE.** The system was declared RESTRICTED COMPARATOR NOT ADMISSIBLE at stage S3. It receives no response-map fits, B3 stacks, baselines or evaluation propagations. Per system that is up to 60 fits, 30 stacks and 491,776 propagations, counted in this separate category.
  3. **SKIPPED: PREFIX VOID.** The prefix is voided on that system's chart. Its 16 baseline propagations are skipped. On each fold where it is an evaluation prefix, its 2,048 edits × 5 = 10,240 propagations are skipped. Those edits stay in the coverage denominator.
  4. **SKIPPED: UNAVAILABLE MAP.** The map's design is empty or rank-unresolved (C3.3(a′), C3.9). Its prediction is skipped, one propagation per affected edit: 4,096 per (fold, class) map and 16,384 per global map. Resolved lower-rank maps are not skipped. UNRESOLVED-B3 alone does not make a map unavailable (E39-8).
- **Closure.** For every (system, stage): scheduled = attempted + Σ skipped. A **normally completed** run must close exactly. A mismatch, or attempted float propagations above 3,443,968, is INTEGRITY STOP (exit 7).
- **Forced termination (#39 L120; E39-7).** After a wrapper kill or other forced termination, the package reports the **last durable counters** (annex A5: run-log checkpoints) and marks every later interval as **UNKNOWN**. It does not manufacture attempted or unreached counts from an incomplete log. The run is marked INCOMPLETE, which is not a scientific result.

**C8.5 Caps (E38-14, verbatim in §2b; unchanged per #39 L223–233).**
- 1 CPU, no GPU, RLIMIT_AS 4,000,000,000 bytes (`pinned.py:37`).
- 600 s cumulative from before imports, including setup and reporting.
- Operational stop at 540 s (`pinned.py:39`), with the declared 60 s reserve (`pinned.py:40`). Hard termination at 595 s − (now − T0) (`pinned.py:38`; closure note L18).
- Projection halt if the projected remaining time exceeds 540 s − T_elapsed (closure note L19).
- No automatic retries, parameter substitutions or post-result tolerance changes.
- Cap-limited work is incomplete, not a scientific negative.

**C8.6 Integrity stops (exit 7).**
- A hash mismatch of code, inputs or the application against the sealed manifest, or a runtime-version mismatch.
- A float-propagation overrun or an accounting-closure failure (C8.4).
- An edit-count mismatch.
- An extended-B3 resolved third direction (C3.11).
- An observed SYS-PC or SYS-LIM crossing.
- An SYS-NC1 refit mismatch.
- A mismatch between the exact recomputed t and the frozen rational.
- A hash mismatch of a reused array against the annex (A1).

**C8.7 Workload estimate (UNVERIFIED feasibility estimate, not a guarantee).**
- **Reference run.** The sealed oracle run made 784,960 float propagations (`results.json:72`) in t_elapsed_s = 21.7287 (`results.json:26466`). That is ≈ 36,125 propagations/s overall, including its setup and reporting.
- **Linear scaling** to 3,443,968 gives ≈ **95.3 s**.
- **Not covered by the reference.** 541 SVDs on small designs (largest fit design 384 rows × 3, global; class designs 96 × 3; largest B3 stack 384 × 8) and serialization of the arrays above. On paper both are small against the 540 s stop. Neither has been measured.
- **Memory (#39 L173).** The analytic estimate is in the annex (A4). It covers Python objects, exact arithmetic, numerical-library workspace, aggregation records and serialization. It is UNVERIFIED and comes from no pilot or measurement.
- No pilot is run (#38 L372; #39 L173, L237).

## 9. Manifest, seal and approval

- **C9.1 One package.** It has its own scope, code, manifest and post-run index.
  - #39 approves the scientific design for freeze with the #39 amendments (E39-1).
  - The remaining implementation details go in the immutable, hash-referenced annex (C9.6) and are checked by an independent pre-seal conformance review.
  - The Research Lead completes the frozen bundle, the standing-approval application and the seal before stage S0 (#39 L160–169).
  - No further Astra scope review is required solely to fill bounded implementation details (#39 L175).
- **C9.2 Sequence (N2, v1_4_N L22–30).**
  1. Code and the draft manifest are complete.
  2. The annex is completed (C9.6) and passes the independent pre-seal conformance review.
  3. The standing-approval application is filed. It cites by sha256 this record, the annex, the #39, #38, #37 and #36 raw files, the governing set, every implementation file and every input.
  4. The application sha goes into the manifest.
  5. The manifest is sealed.
  6. Stage S0 begins.
- **C9.3 Preflight.**
  - It asserts sealed: true, all hashes, and the runtime versions, recording the observed versions as observations.
  - It asserts that no checkpoint or weight file is read. The allowed input set is enumerated.
- **C9.4 E37-2 hygiene.** No hard-coded phase or seal strings appear in outputs. Every elapsed-time or memory figure names its source file and field.
- **C9.5 Frozen in the manifest.**
  - C3.1–C3.12.
  - C4 including the rules of C4.4.R and the exact t.
  - C5 including the verbatim tolerances.
  - C6.
  - C7 including the thresholds.
  - C8 including stage order, cache policy, accounting table and caps.
  - The output schema and paths (annex A2–A3).

  **Corrected per E39-9 (#39 L72).** No discretionary rule, parameter or threshold is chosen or changed after outputs are inspected. Values computed during execution under frozen deterministic rules are permitted execution outputs, not post-result choices. These include normalizations, ρ_NC1, c₂, c₃, t, the full-precision bounds and fitted matrices. v1.2's blanket "no value is set" is read and corrected accordingly.
- **C9.6 Implementation annex and reference scheme (E39-1, E39-10).**
  - **Annex path:** `review/ckappa_classfit_implementation_annex_v1.md`.
  - **What it holds:**
    - A1: reused-array provenance and conventions;
    - A2: output schema;
    - A3: paths;
    - A4: memory and resource estimate;
    - A5: artifact inventory and durable counters;
    - A6: deterministic event ordering;
    - A7: P0 domains;
    - A8: open implementation fields.
  - **Reference direction (acyclic).**
    - This record names the annex **by path only** and does not contain the annex's sha256.
    - The annex cites this record **by full sha256**.
    - The annex's sha256 is recorded in the posted report and must be recorded in the sealed manifest and the standing-approval application.
    - The manifest is the root that binds both hashes.
    - Writing the annex's hash into this record would make each file's hash depend on the other, so it is deliberately omitted.
  - **Versioning.** The annex is immutable once hashed. Any change, including filling an open field, produces a new annex file (`…_annex_v2.md`, and so on) that cites this record's sha256 and supersedes the earlier version by name. This record does not change when the annex is versioned, unless a scope change is ruled.
- **C9.7 Fixed design (#39 L175).** A proposed change to the estimator, controls, masks, thresholds, directions, sizes, caps or claim ceiling requires a new Astra ruling. Neither the annex nor the implementation may make such a change.

## 10. Wording rules

- **C10.1 Negatives (E37-4).** "The declared [global/class-conditioned]-map intervention-prediction criterion was not met." Cap-limited work is "incomplete", never negative (E38-14).
- **C10.2 Ratios (E37-3).** "Comparator squared prediction error divided by actual response energy."
- **C10.3 Oracle labels (E37-1).** "Oracle-scale headroom only."
- **C10.4 Neural ceiling.** E37-10 and E38-15 verbatim, plus the #38 L202 sentence (C1).
- **C10.5 SYS-PC success.** "The class-conditioned fit recovered the declared sign-dependent synthetic map, which the global fit cancels as derived."
  - It does not show that a network uses κ, carries a class label or has a covariance register.
  - Headroom thresholds are synthetic conventions, never a neural floor.
- **C10.6 Extended B3.** It is never described as applicable to neural two-coordinate systems (E38-6).
- **C10.7 SYS-LIM.** It is described only with the exact failure statement of #38 L194. No "no predictor can" or impossibility wording (E38-9).
- **C10.8 Confounds.** RMS matching is never described as matching response, conditioning, transferability or GRU geometry (E38-11, #38 L158). The word "floor" is not used for any confound result. SYS-NC1 is described as a varying-κ two-coordinate confound (#38 L160).
- **C10.9 SYS-FK.** It is described as "globally zero-κ on product-chart designs". No impossibility of alternatives is stated (E38-10).
- **C10.10 Readouts (E39-11).** Affine claims are always stated with their system and domain (C4.R). SYS-NC1 and SYS-NC3 are never called affine. SYS-PC and SYS-LIM are called affine only "within their declared non-crossing branches". "Compatible with two-coordinate mediation" is never applied to SYS-LIM.
- **C10.11 Guard inconsistency (E39-4).** It is described as "a guard inconsistency", with margins and residuals. It is never described as proof that the recovery tolerance was exceeded.
- **C10.12 UNRESOLVED-B3 and NOT EVALUATED (E39-3, E39-8).** Never described as a passed guard or a passed identity.
- **C10.13 D7 INVESTIGATE (E39-8).** Retained prominently. Any later decision about neural work must address it, and unchanged labels do not resolve it.

## 11. Status of open questions; items still to fix

**Q1–Q17** were closed by #38 (v1.2 §11; unchanged).

**Q-R1 to Q-R6: all closed by #39 (L13–40).**

| Q | #39 ruling | Where applied |
|---|---|---|
| Q-R1 | D7 INVESTIGATE accepted; no stop; no effect on VALIDATION or HEADROOM; retained prominently; a later neural decision must address it | C4.5, C7.4, C10.13 |
| Q-R2 | fold/class/group/size confirmed for SYS-FK class losses; no pooled replacement | C4.3 |
| Q-R3 | confirmed; SYS-O6 and SYS-FK rank lapses prevent VALIDATION MET; resolved lower rank kept distinct from unresolved | C7.2 |
| Q-R4 | accepted for actual-recovery predictors, with two qualifications (SYS-PC global; guard mismatch is not proof of tolerance excess) | C4.2(g)(iii), C5.3(c) |
| Q-R5 | unweighted global and class stacks accepted; band result stays explicitly unresolved, with no automatic stop | C3.11 |
| Q-R6 | per-system baselines and no deduplication accepted; P0 dependency corrected; streaming stopping checks | C8.1, C8.2, C5.3(c) |

**Open questions for Astra: none.** #39 L175 says no further scope review is needed solely to fill bounded implementation details. The items below go to the independent pre-seal conformance review. If that review finds that any of them needs a change in a C9.7 category, a new ruling is required.

**Items for the conformance review (interpretations made in v1.3 or the annex).**
- **CR-1.** E39-4's guard consistency is implemented for the **actual-valid** direction: actual valid, actual-recovery predictor invalid, which stops. The reverse direction (actual invalid, predictor valid) is recorded and counted but does not stop, because E39-4 opens with "Actual-valid guard consistency". The review should confirm or correct this reading.
- **CR-2.** The SYS-NC1 refit uses the inherited float P_a accumulation, so that it reproduces the committed coefficients. The RMS rule uses exact-law P_a converted once (C4.4.R). The two representations are deliberate.
- **CR-3.** D6 diagnostic matrix residuals (6 cells) are counted and reported because NOTE_1 N1 gives D6 a premise. Its role stays diagnostic only.
- **CR-4.** The memory baseline for interpreter, libraries and inherited stages is not derivable from committed files (annex A4, A8).
- **CR-5.** Proposed output and wrapper paths avoid overwriting the sealed oracle artifacts (annex A3).

**Items TO BE FIXED BEFORE SEAL, or computed by the package under a frozen rule.**
1. c₂: TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW (C4.4.R). This is permitted as a frozen-rule execution output (E39-9).
2. c₃: TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW (C4.4.R). Permitted as above.
3. Full-precision normalizations and crossing bounds are computed at stage S3 under C3.12 (permitted, E39-9).
4. The annex's open fields (annex A8: code paths and hashes, runtime footprint baseline, manifest field names) are filled before seal in a new annex version or the sealed manifest, then conformance-reviewed (E39-1).
5. Implementation code, manifest and standing-approval application (C9.2). Not yet written.

## 12. Verification

**12.1 Checks run by me (read only; arithmetic and hashing on committed data).**
- **Raw #39.** sha256 = `e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482`, 237 lines. This matches the Specialist's prefix e6403b63…482.
- **Exact-substring checks.**
  - The 11 E39 quotes, the 37 body excerpts, the Q-R table and the four #39 code blocks were extracted programmatically and checked against the raw file.
  - The E38 quotes and excerpts were re-checked against #38 raw (`87fd77e0…ca2a5`), and the E37 quotes against #37 raw (`ce010fdb…63e2`).
- **Clause references.** Every Cn.m reference in this file resolves to a defined clause. The script result is in the posted report.
- **Reused arrays.** Per-array raw-byte sha256 recomputed from the committed `drawn_arrays.npz` (C-contiguous `<f8` bytes). They match `drawn_array_hashes.json` for Q, Q2, O6_directions, O7_directions and O4_directions (annex A1).
- **Accounting arithmetic.** 7·2·2·576 = 16,128. Identity cells: 150 + 108 + 120 + 660 + 72 + 12 + 6 = 1,128. Propagations as in v1.2, which #39 verified (L78–92).
- **Inherited order and policy** read from `stages.py:492–640` (O6 loop nesting, lazy baseline cache, propagate-every-edit policy) and `run_package.sh` (wrapper).

**12.2 UNVERIFIED (prospective, per E39-10).**
- D1–D7 and P0.
- All numerical ranks, headroom and fixture outcomes.
- Full-precision normalizations and bounds.
- c₂, c₃ and NC admissibility.
- SYS-FK validity bounds.
- Runtime and memory.

**12.3 Raw #39 versus the Specialist's summary (raw governs).**
- **Agrees:**
  - Q-R1 to Q-R6 accepted;
  - D7 non-stopping and addressed by any later neural decision;
  - SYS-FK per-cell zero gain;
  - SYS-O6/SYS-FK rank lapses block VALIDATION;
  - SYS-PC global needs only Pred_full = Pred_μ;
  - guard mismatch is not proof of tolerance excess;
  - unweighted B3 and UNRESOLVED-B3;
  - caching without deduplication;
  - the rank categories, with empty = UNAVAILABLE;
  - the 16,128 records;
  - single-prefix fits disabled;
  - the skip precedence;
  - forced-termination unknowns;
  - the stage order (matches L130–141);
  - the E39-5 gates;
  - E39-11 on NC1/NC3 and PC/LIM;
  - caps and ceiling unchanged;
  - the new-ruling sentence.
- **Differences or omissions, followed per raw:**
  1. **NOTE_1.** E39-8 adopts N1 and N2 by name. N3 is "appropriate", with a numerical clarification (L42, L61–70) given in E39-9. The summary's "N1 to N3 adopted" is acceptable only with that clarification.
  2. **Q-R3** also requires keeping resolved lower rank distinct from unresolved rank (L17).
  3. **Q-R4 extras.** SYS-PC global equality is checked "where both predictions are valid, independently of unrelated predictor masks" (E39-4). The guard report must give minimum probabilities, chart difference and recovery residual, and must not relax guard or tolerance (L40).
  4. **E39-8 extras.** UNRESOLVED-B3 is never described as a passed guard and does not by itself make a map unavailable. A resolved third direction keeps the integrity stop.
  5. **P0 dependency.** It covers **SYS-FK's** product-chart L table, not just SYS-NC1 (L126).
  6. **Nonempty zero matrix.** It is kept separate from the empty design (L59).
  7. **Summation order.** E39-9 freezes the summation for ρ and c₃ specifically. It asserts the exact ΣP = 1 and forbids rescaling. #39 also orders C9.5's "no value is set" to be corrected (L72).
  8. **Accounting extras.**
     - Global orbit-level aggregates are derivable, and enumerated separately if stored (L114).
     - Each record holds four quantities; it is a record count, not a scalar count (L112).
     - An already attempted call is counted as attempted.
     - An inadmissible system receives no subsequent fits or evaluation propagations, and its skipped work is counted separately (E39-7).
  9. **E39-3 extras.** Tested-edit counts are required, and an empty test domain is NOT EVALUATED.
  10. **E39-5 extras.** Missing eligibility gets its applicable status, diagnostics are stored where permitted, and C7.2's wording conflict about SYS-NC1 P0 is fixed (L158).
  11. **E39-11 target.** The correction targets "the Research Lead summary" (L74), and "the record's system-specific claims should govern". v1.2's exactness claims were already domain-restricted. The only v1.2 wording changed is SYS-LIM's grouping with two-coordinate mediation in C6 and in the E37-7 note (E39-11, last sentence).
  12. **E39-10 extras.** "Losses, identities and coverage are not silently evaluated on different undeclared domains", and outcomes remain prospective.
  13. **Array provenance (L171).** Seeds alone are insufficient. Either preserve generator, dimensions, ordering, normalization and sign conventions, or use the authenticated existing arrays. v1.3 chooses the latter.
  14. **Memory scope (L173).** The estimate must cover Python objects, exact arithmetic, library workspace, aggregation records and serialization.
  15. **No further Astra review (L175)** is needed solely to fill bounded implementation details.
  16. **Status wording.** #39 says "approved for freeze" (E39-1). The pre-seal review covers the bundle's implementation details, not only "annex conformance". See the status note.
  17. **Ceiling.** L235 also keeps "the explicit limitation concerning orbit-dependent codes".

**12.4 CNA first-look list.** CR-1 to CR-5 (§11), then annex A8.

**12.5 Not done.** No code was run and no memory was measured. The repo, v1.2 and NOTE_1 were not modified. Nothing was posted or sent.
