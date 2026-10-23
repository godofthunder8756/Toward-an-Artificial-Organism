# C-κ class-fit validation package: synthetic-only scope record v1.2 (consolidated, after Astra #38)

**Status: DRAFT. NOT FROZEN. NOTHING RUNS.** Research Delegate (Track A), 2026-10-23 (ET). This is a new file. v1.1 (`97165ac6cb90fbd9433fa3a8777c017319b7cefc88b6ed45d9f902f3aaca23aa`) and its additive note 1 (`00ec1902fcd16f2d722447c8f52d67123a5eb305bbe0c73c3657afb73b531aea`) are not edited. v1.2 is a complete replacement text that supersedes both for freeze purposes.

I executed nothing: no oracle, solver, fit, simulation or checkpoint. "RD arithmetic" means my own arithmetic on committed numbers in the PR #13 outputs at `14376f38`: the `stage_O1.json` exact rationals, the stored B matrices in `fit_freeze_O6.json` with Q from `drawn_arrays.npz`, and the `stage_O7.json` `g_coefficients`. Every derived expectation is **UNVERIFIED** until an approved, frozen run. Nothing in this file authorizes execution (E37-9, E38-16).

**Selected design (Astra #38, E38-1).**
- The confound treatment is descriptive-only.
- Each flip class gets plain, separately fitted maps: a full unrestricted 3×8 B and a fixed-κ [A; 0], where A is an unrestricted 2×8 matrix.
- The global comparator is one pair of maps per fold.
- All seven systems are included.
- There is no augmented basis, no shared e, no tied-bilinear fit and no empirical neural floor.

**System names** are kept from v1.1:

| Name | Role (relabelled per #38 L160) |
|---|---|
| SYS-O6 | Existing affine exact-filter control (implementation identity) |
| SYS-PC | Sign-dependent positive control (identities, plus the separate HEADROOM label) |
| SYS-FK | Genuinely fixed-κ control: globally zero κ on product-chart designs |
| SYS-NC1 | **Varying-κ two-coordinate confound** (O7 lookup). It is *not* a fixed-κ control and *not* a gain-negative control. |
| SYS-NC2 | Affine symmetry-breaking two-coordinate confound (descriptive) |
| SYS-NC3 | Cubic two-coordinate confound (descriptive) |
| SYS-LIM | Orbit-indexed limit control, REPORTED ONLY |

"NC" is kept only as a legacy label. None of SYS-NC1–NC3 is a negative control, and none has a gain-must-vanish criterion (E37-7, E38-15). The token "S6" occurs only in quoted raw text: E37-4, where it names the earlier prospective neural design, and #38 L5 ("S6/Q1"), where it names a section of the #38 question packet. Neither names a system here.

## Change log relative to v1.1 + note 1

Each entry cites its #38 source. "Withdrawn" means the text is removed and must not be reintroduced without a new ruling.

**Withdrawn**
1. **Option A, the empirical NC floor.** Withdrawn per E38-1 and #38 L158: "Calling the number a "floor" gives it a calibration role that has not been established."
2. **v1 Option B, the per-class matched basis.** Withdrawn per #38 L164 and Q2a.
3. **B-repaired (shared e) and derivation D2′.** Withdrawn per E38-1 and Q2b. Astra accepts the conditional algebra but does not approve the coupled class fitting. The dx/dy table goes with it.
4. **Option C, and the falsify-only text tied to it.** Withdrawn per E38-1 and #38 L184. No floor exists to be falsified.
5. **All matched-basis and effective-basis-span material.** This includes the v1.1 note that μ_x² lay inside the Option B effective basis. Withdrawn per E38-1 and #38 L156. The effective basis is now stated explicitly as plain, with no augmentation (C3.2, Q2d).
6. **Note 1 item 3** ("NC2 (c₂μ_x) and NC3 (c₃μ_x³) share a symmetry ... and differ only in being linear or nonlinear", together with its floor-transfer framing). Withdrawn per #38 L186: "their different baselines and derivatives mean this is not a comparison in which only functional form changes."
7. **SYS-LIM under B-repaired (v1.1 TBF item).** Withdrawn as not applicable (Q16).
8. **My inferred orbit masses and the c₂/c₃ values derived from them** (≈0.100448 and ≈0.199056). Withdrawn per Q7 and E38-11. The values are now TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW (C4.4.R).
9. **v1.1's DERIVATION PREMISE vs IMPLEMENTATION attribution labels.** Withdrawn per #38 Q5. A failed identity is "an operational failure diagnosis, not conclusive proof" of which one failed. The stop is kept.

**Corrected**
10. **D1 residual and SYS-PC local map (E38-2; #38 L40–57).**
    - The chart increment S_g C δ is exact.
    - L_a[:,κ]χ_a c_τ δ is only the first-order forecast discrepancy.
    - Exact finite discrepancies are computed by propagating both perturbed charts through Φ.
11. **Rank premises (E38-3; #38 L61–83).**
    - D2, D4 and D5, and the SYS-O6 class recovery, require **full column rank** (3).
    - v1.1's "for every resolved design" (D4) is withdrawn.
    - Missing rank is EXPECTATION NOT APPLICABLE (RANK).
12. **D3 wording (#38 L85–96).**
    - The non-negative class gain follows from exact full prediction (L_full = 0), not from nesting.
    - "Generally ≠ 0" now refers to the adjustment to C_μ, not to B_μ as a whole.
13. **SYS-PC global cancellation check (E38-4; #38 L122–134).** It is now matrix recovery, plus equality of finite predictions, plus per-cell loss equality. Loss equality alone no longer defines it.
14. **SYS-LIM (E38-2, E38-9; #38 L98–120, L188–204).**
    - The (1+λ)² ratio and the factor 4 are first-order statements.
    - The "no fit type can carry it" wording is replaced by Astra's exact failure statement.
    - No impossibility claim is made for predictors with a declared transport rule.
    - D7 is a reported diagnostic, not a VALIDATION item.
    - The midpoint is computed from exact-law A and D magnitudes.
15. **SYS-FK alternatives (E38-10; #38 L206–227).** v1.1's claim that no autonomous same-baseline alternative exists is wrong and is withdrawn. Astra's counterexample is a frozen register r = κ_a. Astra also rejects v1.1's dismissal of a two-coordinate plateau construction (L225). Neither control is added.
16. **P0 (E38-5).**
    - Probability invariance is checked on exact rationals from O1.
    - P0 is required on the true chart, SYS-FK and admissible SYS-NC1.
    - The #38 tolerances apply.
17. **Extended B3 (E38-6).** It is justified only by the common right factor D_μQ₂ᵀ. The stacking convention is frozen (C8.2). Zero matrices and rank bands are handled explicitly.
18. **Masks and identity domains (E38-7, E38-8).** C5.3 and C7.0 are new.
19. **Normalization (E38-11).** It is system-level, using exact-law weights, and is not recomputed per fold.

**Fixed (formerly TO BE FIXED or open)**
20. **Tolerances (Q9).** Taken verbatim from #38 L280–302 (C5.5).
21. **SYS-PC HEADROOM thresholds (Q4, E38-12).** Retained as synthetic reporting conventions, with H = L_μ,class and no prediction that SYS-PC meets them.
22. **Draw reuse (Q10).** Q, Q₂ and the directions are reused with their conventions and hashes, and the development-informed reuse is disclosed.
23. **Sizes (Q12).** All four ε_syn are kept; 0.1 is the sole headroom reference.
24. **SYS-O6 inclusion (Q13).** Allowed. It is not a rerun.
25. **SYS-LIM midpoint (Q14).** A versus BCD, with no extra split.
26. **Rank lapse (Q15, E38-12).** A rank-lapsed required SYS-PC class cell gives NOT MET (RANK).
27. **SYS-LIM autonomy (Q17).** Confirmed.
28. **B1 extension (Q3, E38-8).** Confirmed.
29. **Caps (E38-14).** Restated verbatim.

**Added**
30. **Execution-accounting table (E38-13).** New §8.
31. **Claim ceiling.** E38-15 and the #38 L202 neural-ceiling sentence are added verbatim (C1, C10).

## 0. Sources, hashes and precedence

| Source | sha256 | Role |
|---|---|---|
| `/workspace/astra_consult38_response.txt` (Astra #38 raw, 385 lines, E38-1..16) | `87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5` | **Governs over everything**, including this file and any summary of #38 |
| `/workspace/astra_consult37_response.txt` (Astra #37 raw) | `ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2` | Governs below #38 |
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
1. Astra #38 raw text.
2. Astra #37 raw text, where #38 does not revise it.
3. E36 raw text.
4. This record.
5. The oracle governing set. It supplies every inherited definition that this record does not replace.

A summary of #38 that departs from the raw text, including the Specialist's, has no standing; see §12.3.

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

## 2. Astra #37 items: verbatim text and compliance map (kept from v1.1)

The E37 quotes are carried over unchanged. Where #38 revises the mapped clause, the #38 rule governs, as shown in §2b.

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

*Binding here:* C4.4 and C6. SYS-NC1–NC3 and SYS-LIM have **no** gain-must-vanish criterion. Their gains are reported, not passed or failed. No floor and no augmented basis is used (E38-1). Exclusion of two-coordinate mediation would need the different test in #37 L142, which is out of scope.

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

## 2b. Astra #38 items: verbatim text and compliance map

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
- **(b) Rank premises (E38-3).** A coefficient-recovery or held-out-prediction identity applies only when its design has **resolved full column rank** (3 for full maps, 2 for fixed-κ maps). A resolved lower-rank minimum-norm fit is still scored and reported, but no identity is asserted for it. It reads EXPECTATION NOT APPLICABLE (RANK), not an identity failure (#38 L71–73).

| Identity | System(s) | Required premise |
|---|---|---|
| B = DQᵀ, global and class; finite recovery | SYS-O6 | full design rank 3 in that cell |
| D1 global (B = [c_x;c_y;0], A = [c_x;c_y]) | SYS-PC | global full rank 3 and global μ design rank 2 (invertible normal matrices, #38 L31) |
| D2 class (B = S_gC); finite recovery | SYS-PC | class full rank 3 |
| D4 (B = [C_μ;0], A = C_μ) | SYS-FK | full rank 3 for B; μ design rank 2 for A |
| D5 (full exact) | SYS-NC2 | full rank 3 |
| D7 (diagnostic only) | SYS-LIM | class full rank 3 in CD/BD/BC folds |

  - **Analytic support (#38 L75–83).** Each valid baseline's exact 3-column L has full rank. That supports the exact-rank premises but does not establish numerical rank under the thresholds. Numerical ranks are prospective and are not predicted here.

**C3.4 Global comparator.** For every system, the global pair per fold is fitted with the same solver. It is a fixed descriptive comparator (#37 L116), except for the identities of C4.

**C3.5 Freeze-before-scoring order.** For every system:
1. Compute every global and class fit from fitting prefixes only.
2. Write the fits with their stored terms to `outputs/fit_freeze_<system>.json` and fsync.
3. Only then propagate any evaluation edit. No fit is recomputed after evaluation begins (stage order C8.1).

**C3.6 Stored outputs (E37-8).** Arrays are float64 C-contiguous little-endian, each with name, shape, `<f8` and raw-byte sha256 (closure note N-b).
- **(a) Matrices.** Every B and A, global and class, for every system and fold, stored in full.
- **(b) Rank reports.** For every fit design and every extended-B3 stack (C3.11): full σ list, σ_1, ratios, numerical rank, unresolved flag and n_inverted.
- **(c) Losses.** L_μ, L_full, S and gain per (system, fit type, fold, class, evaluation orbit, group, ε_syn), weighted and unweighted, with scoreable counts and law mass.
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
- Optional single-prefix local fits, which abandon the held-out claim (#37 L113).
- Neither enters any outcome.

**C3.9 Voiding, unresolved cells and pooling suppression (E38-8; Q3).**
- **Voiding.** Systems whose baseline is not the true chart (SYS-FK, SYS-NC1–NC3) inherit N4(ii) per-prefix voiding. SYS-NC1–NC3 also inherit the ≥5-of-16 RESTRICTED COMPARATOR NOT ADMISSIBLE rule (v1_4_N L38–43).
- **Empty class.** A class with 0 non-voided fitting prefixes in a fold is a rank-UNRESOLVED class cell.
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
  - Count: 4 systems × (6 + 24) = **120 stacks**.
- **(c) Zero matrix.** If σ_1 = 0, the stack has rank 0. This is recorded, with no stop.
- **(d) Bands.**
  - σ₃/σ₁ > 10⁻⁶ is a resolved third direction: INTEGRITY STOP (exit 7), PIPELINE INVALID.
  - σ₃/σ₁ in [10⁻¹⁰, 10⁻⁶] is recorded as UNRESOLVED-B3, with no stop. This is not a resolved third direction under the inherited bands.
  - σ₃/σ₁ < 10⁻¹⁰ passes.
- **(e) Scope.** The guard is not generalized to two-coordinate neural systems with prefix-dependent marginal-state Jacobians (C10.6).

**C3.12 Normalization and fixed rules (E38-11).**
- Every synthetic normalization (ψ̄, D_ψ for SYS-PC/SYS-LIM/SYS-O6; μ̄, D_μ for SYS-FK/SYS-NC1–NC3) is computed **once per system** over all 16 prefixes with exact-law P_a from O1 (`stages.py:149–154`), as in `_embed`, `stages.py:323–329`.
- Normalization is never recomputed per fold.
- Weights, draws (C5.2) and coefficient rules (C4.4.R) are fixed in the frozen file before execution.

## 4. Systems and derived expectations

**Notation.**
- θ = (μ_x, μ_y, κ) and Φ(θ,u) is the forecast.
- Output flip actions P_X = diag(−1,1,−1) and P_Y = diag(1,−1,−1) (RD arithmetic, `world.py:146–158`).
- R_X = diag(−1,1,−1), R_Y = diag(1,−1,−1), R_XY = diag(−1,−1,1).
- **Premise P0.** L_{g·a}(g·u) = P_g L_a(u) R_g and w(g·a,g·u) = w(a,u). Hence G_{g·a} = R_g G_a R_g. P0 alone does not give D1 or D6. It must be combined with the specified state map, weights, complete fitting orbits and rank conditions (Q11).

**C4.0 P0 step-0 fixture (E38-5).**
- **When.** After O1 and O2, before any fit (C8.1 stage S3).
- **Charts checked.**
  - The true chart (designs shared by SYS-O6, SYS-PC, SYS-LIM).
  - The SYS-FK product chart.
  - The SYS-NC1 chart **if SYS-NC1 is admissible** (C4.4).
  - Not SYS-NC2 or SYS-NC3, which break the symmetry by design.
- **Checks,** for every prefix a, flip g ∈ {X, Y, XY} and continuation u (g·u by reading masks 85/170, `stages.py:221`):
  - (i) L comparison: ‖L_{g·a}(g·u) − P_g L_a(u) R_g‖_max ≤ 1e-12 + 1e-10·max(‖·‖_max, ‖·‖_max) (#38 L284–286).
  - (ii) Probability invariance: P_h(g·a, g·u) = P_h(a,u) **as exact rationals from O1** (#38 L300). These are exact equalities, not byte equality of float sums.
  - (iii) G comparison: ‖G_{g·a} − R_g G_a R_g‖_max under the same formula as (i).
- **Failure.** A failed applicable P0 check stops the package: PIPELINE INVALID (P0), exit 7, no fit, no rerun. The report gives an operational failure diagnosis only, not a conclusive attribution to derivation or implementation (Q5).

**C4.1 SYS-O6: existing affine exact-filter control.**
- **Construction.** State, readout, embedding (Q, seed 35006) and edits exactly as in O6 (oracle v1.1 L83–91).
- **Inclusion (Q13).** Including it is allowed. It does not reopen, replace or retry the completed oracle package.
- **Identities (E38-3).**
  - Each global and class B equals DQᵀ within 1e-9 max abs, in every cell with resolved full rank 3.
  - In those cells, Pred_full matches actual within 1e-9 on actual-valid edits (C5.3(c)).
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
  - **Full precision governs (#38 L249).** The package computes D_ψ under C3.12 and the bound from it at step S4, before any edit. The displayed numbers explain the bound and do not govern it.
  - An observed crossing under these premises is an integrity failure (exit 7), with no replacement edit (#38 L251).
- **(g) Global identity checks (E38-4).** In every fold, and where stated in every (group, ε_syn) cell:
  - (i) ‖B_global − [c_x;c_y;0]‖_max ≤ 1e-9.
  - (ii) ‖A_global − [c_x;c_y]‖_max ≤ 1e-9.
  - (iii) max|Pred_full − Pred_μ| ≤ 1e-9 on the required valid edits.
  - (iv) |L_μ − L_full| ≤ 1e-18 + 1e-9·S per (fold, group, size) cell. This is reported as a consequence and is never the sole definition.
  - All four pass: GLOBAL CANCELLATION AS DERIVED.
- **(h) Class identity checks.** In every (fold, class) cell with the premise:
  - ‖B_(f,g) − S_gC‖_max ≤ 1e-9.
  - max|Pred_full − actual| ≤ 1e-9 on actual-valid non-crossing edits.
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
  - max|Pred_full − actual| and max|Pred_μ − actual| ≤ 1e-9 on actual-valid edits.
  - Zero gain per (fold[, class], group, size) cell: |L_μ − L_full| ≤ 1e-18 + 1e-9·S.
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
  - **Global.** Pred_full ≡ Pred_μ is expected only if 0 prefixes are voided. Reported with the zero-gain formula, as a descriptive identity, not a validation item.
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
  - They are computed at stage S4 before any fit, recorded, and never changed (Q7: "No coefficient adjustment after inspection").
  - My earlier values came from probabilities reconstructed from rounded SDs and are withdrawn (change log 8).
  - Neither I nor this record computes the exact-law values. `stage_O1.json` stores the exact stage-4 charts but not P_h or P_a: its keys are listed in §12, and `stages.py:285–291` builds P_a only in memory. So exact-law P_a needs the O1 filter run, which is excluded here.
  - **Frozen arithmetic.** In the package, P_a = Σ_u P_h(a,u) is formed as an exact rational sum and converted once to float64. ρ, c₂ and c₃ are then computed in float64 and recorded at full precision.
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
- **D6 global (UNVERIFIED; uses P0).**
  - λ = (s₁K₁ + s₂K₂)/(K₁ + K₂), where K_o = Σ_{a∈o} G_a[κκ]. B = [c_x; c_y; λc_τ] and A = [c_x; c_y].
  - **CD/BD/BC fitting folds.** λ = −1, so the held-out A gets the wrong sign. The **first-order** loss on A is L_full ≈ 4·E_A against L_μ ≈ E_A.
  - **A-containing folds.** λ = (K_A − K_X)/(K_A + K_X). The **first-order** ratio is L_full/L_μ ≈ (1+λ)², and (1+λ)² < 1 iff K_A < K_X.
  - **These loss-scaling statements are Jacobian-level only and are not asserted at finite ε_syn (E38-2, #38 L118–120).** Reported with no sign expectation.
- **D7 class (diagnostic).** In the CD, BD and BC fitting folds, full-rank recovery gives B_(f,g) = diag(1,1,−1)·C, the negative-sign chart map. It is wrong on held-out A whenever the edit has a nonzero relevant component (#38 L194).
  - D7 is reported as an analytic diagnostic.
  - A failure of an exact, applicable D7 identity is flagged **D7 INVESTIGATE** (#38 L198). It is not a VALIDATION item and not a stop.
- **Limit exposed (E38-9).** The negative result concerns the specified global and flip-class map families. It does not establish impossibility for predictors given a different declared transport rule: a rule using the state's magnitude could represent this system (#38 L196).

## 5. Units, edits, masks, weights, groups, tolerances

- **C5.1 Units.** All systems are synthetic. An edit is δ = ε_syn·sign·v in the 8-D synthetic state, with field `eps_syn`.
- **C5.2 Edits and draws (Q10, Q12).**
  - **Directions.** The 16 unit directions of seed 35016 (the O6/O7 array), applied as +v then −v.
  - **Embeddings.** Q (35006) and Q₂ (35007) are reused with their generation conventions and hashes. The reuse is disclosed as development-informed.
  - **Sizes.** ε_syn ∈ {0.02, 0.05, 0.1, 0.25}, with 0.1 the sole headroom reference (`pinned.py:28–29`).
  - **Per system:** 6 folds × 8 evaluation prefixes × 16 continuations × 32 signed directions × 4 sizes = 98,304 edits. Per fold per size that is 4,096 (`stages.py:48` `EDITS_PER_FOLD` = 8·16·16·2).
- **C5.3 Masks and identity domains (E38-7).**
  - **(a) Common mask (comparative losses).** An edit is scoreable for the comparison iff the actual perturbed belief and all four predicted perturbed beliefs (global full, global μ, class full, class μ) pass p ≥ 10⁻⁶.
    - For SYS-PC and SYS-LIM, the edit must also be non-crossing.
    - The same mask governs L_μ, L_full and S for both fit types.
    - Coverage is reported per fold, class and size.
  - **(b) Matrix identities** (C4.1, C4.2(g)(i)–(ii), C4.2(h), C4.3) are checked on the fitted matrices **before** any evaluation masking.
  - **(c) Finite recovery identities** are checked on **actual-valid, non-crossing** edits in cells where the exactness premise applies. They are not restricted to the common mask: invalidity of a different predictor does not hide an applicable exact-control identity.
    - Applicable identities: SYS-O6 class/global Pred_full = actual; SYS-PC class Pred_full = actual; SYS-PC global Pred_full = Pred_μ; SYS-FK Pred_full = Pred_μ = actual.
    - If a predictor covered by an applicable exact-recovery identity fails the p ≥ 10⁻⁶ guard while the actual belief passes, that contradicts the identity. It is an identity failure, not a coverage exclusion.
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
- **Confound systems.** SYS-NC1–NC3 (and SYS-LIM) are fitted with the same plain maps as every other system and reported descriptively, with no gain-must-vanish criterion and no floor.
  - A positive confound gain is "compatible with two-coordinate mediation" (E37-7).
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
   - an integrity condition of C8.6.

   The diagnosis names the failed check. It does not conclusively attribute the failure to derivation or implementation.
2. **CAP REACHED / CAP RESERVE REACHED (INCOMPLETE) / PROJECTION HALT** (C8.5). This is incomplete work, not a scientific negative.
3. **REFERENCE COVERAGE NOT MET.** Count coverage < 75% (4·n_s < 3·n_t) or law-mass coverage < 0.75·(1 − 10⁻⁶) in some fold, or for class statistics some fold×class.
4. **REFERENCE RANK UNRESOLVED.** A required map is unresolved or unavailable (C3.9). No pooled statistic is formed.
5. **RESTRICTED COMPARATOR NOT ADMISSIBLE** (SYS-NC1–NC3): ≥5 of 16 prefixes voided, or a matched baseline invalid.
6. **ZERO RESPONSE.** Pooled S = 0 exactly.
7. **Identity statistics** (SYS-O6; SYS-PC global and class; SYS-FK): IDENTITY AS DERIVED, or EXPECTATION NOT APPLICABLE (RANK) per cell lacking its premise (E38-3).
8. **Reported statistics** (SYS-NC1–NC3, SYS-LIM, and every global gain other than the SYS-PC/SYS-FK identities): REPORTED. Negative gains are kept (#38 L94). D7 INVESTIGATE flags, if any, are reported.

**C7.2 VALIDATION (E38-12).** **CLASS-FIT VALIDATION MET** iff:
- O1, O2 and every applicable P0 check passed;
- every required control identity holds and has its rank premise (SYS-O6 global and class; SYS-PC global, all four checks of C4.2(g); SYS-PC class; SYS-FK both fit types);
- no required cell is REFERENCE RANK UNRESOLVED.

Otherwise it reads **CLASS-FIT VALIDATION NOT MET (<first failing reason>)**.
- A required SYS-PC class cell with EXPECTATION NOT APPLICABLE (RANK) gives **NOT MET (RANK)** (E38-12, Q15).
- For SYS-O6 and SYS-FK, a required cell lacking its premise likewise gives NOT MET (RANK). "every required control identity and its rank premise" (E38-12) applies to all controls.
- SYS-LIM, D7 and the confound systems never enter VALIDATION. VALIDATION does not depend on any gain magnitude.

**C7.3 SYS-PC HEADROOM (E38-12; Q4).**
- **Formation.** Formed only if VALIDATION is MET. Otherwise it reads NOT FORMED (VALIDATION NOT MET).
- **Statistic.** **H = L_μ,class** for SYS-PC at ε_syn = 0.1, with √H and R = H/S, for ALL and MARG.
- **Thresholds (synthetic reporting conventions only).** ALL √H ≥ 10⁻³ and R ≥ 0.05; MARG √H ≥ 10⁻⁴ and R ≥ 0.02 (`pinned.py:24–27`). Labels are HEADROOM NOT MET / BOUNDARY / MET under the inherited band rule (v1_4_N L15–16).
- **No prediction** is made that SYS-PC will meet them.
- They supply no neural response floor (#37 L164).

**C7.4 What the labels license.** VALIDATION MET with SYS-PC HEADROOM MET licenses only a decision on whether a neural specification is warranted. SYS-LIM and the confound results go with any such decision as stated limits.

## 8. Execution specification and accounting (E38-13, E38-14)

The counts below are **scheduled maxima derived from the frozen design**. Each is a product of declared factors, with sources cited. None is measured. Outcome-dependent reductions (voids, unresolved maps, stops) are accounted for by C8.4 and never appear as unexplained mismatches. The workload and runtime remain **UNVERIFIED** (#38 L372).

**C8.1 Stage order (frozen proposal).**

| Stage | Content | Φ propagations (max) |
|---|---|---|
| S0 | Wrapper T0 before imports; preflight; manifest hash checks; runtime versions recorded as observations; RLIMIT_AS set | 0 |
| S1 | O1 exact fixtures (inherited): 16 prefix filters + 256 terminal forecasts, exact | 272 exact (`pinned.py:11`; `results.json:70`) |
| S2 | O2 closed-form L vs finite-difference check (inherited) | 1,536 float (`results.json:4`) |
| S3 | P0 fixture on true chart, SYS-FK chart and SYS-NC1 chart (if admissible), using closed-form L only (C4.0) | 0 |
| S4 | System construction for all 7 systems: system-level normalization; SYS-NC1 g refit and committed-coefficient check; c₂, c₃ from exact law; t from exact law; baseline validity, voiding and admissibility; L and J tables; crossing bounds at full precision | 0 |
| S5 | Fits for all systems (global and class, full and fixed-κ); rank reports; extended-B3 stacks; normal-equation terms; matrix identities (C5.3(b)); write and fsync `fit_freeze_<system>.json` | 0 |
| S6 | Evaluation, systems in the fixed order SYS-O6, SYS-PC, SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3, SYS-LIM. Per system: 256 baseline propagations, then per edit 5 propagations. The first 1,000 S6 propagations are the timing sample (`pinned.py:41`; E36-13 projection) | 3,442,432 |
| S7 | Finite identity checks, pooling, labels, flags (C7) | 0 |
| S8 | Serialization of stage files and `results.json`; report; wrapper post-run index | 0 |

S3 precedes S4 even though P0 on the SYS-NC1 chart needs SYS-NC1's admissibility. That sub-check therefore runs at the start of S4, immediately after SYS-NC1's admissibility is known and before any fit. A failure stops the package (E38-5).

**C8.2 Cache policy (frozen proposal).**
- **L tables.** One closed-form table of 256 L_a(u) per **distinct baseline chart**: true chart (shared by SYS-O6, SYS-PC, SYS-LIM and used by O2), SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3. That gives 5 tables, **1,280 L evaluations**. P0 reads these tables and computes no new L.
- **Baseline forecasts.** Propagated **per system** (256 each, 1,792 total), with no cross-system sharing even where charts coincide. This matches E38's count (#38 L369). For true-chart systems, they are compared with O1's exact forecasts as a reported check.
- **Predictions.** No deduplication. Every scheduled actual and predicted propagation is attempted as scheduled, even where two predictions are expected to coincide (for example SYS-PC global full and μ). Deduplication would hide the very equality being checked.
- **Fits.** Not cached across systems. Each system's designs are formed from its own tables, even when identical to another system's (SYS-O6/SYS-PC/SYS-LIM), and stored.

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
| Loss cells per system | global F·2 orbits·3 groups·Z + class F·K·2·3·Z | 144 + 576 = 720 | C3.6(c) |
| Loss cells, all systems | 7 × 720 | 5,040 | — |
| Pooled statistics per system | 2 fit types × 3 groups × Z | 24 | C3.10 |
| Coverage records per system | F·Z (global) + F·K·Z (class) | 24 + 96 = 120 | C5.3 |
| Identity cells, SYS-O6 | matrices 6 + 24; recovery F·Z + F·K·Z | 30 + 120 | C4.1 |
| Identity cells, SYS-PC global | matrices 12; Pred equality F·Z; loss F·3·Z | 12 + 24 + 72 | C4.2(g) |
| Identity cells, SYS-PC class | matrices 24; recovery F·K·Z | 24 + 96 | C4.2(h) |
| Identity cells, SYS-FK | matrices 60; recovery 2 predictors × (F·Z + F·K·Z); zero gain F·3·Z + F·K·3·Z | 60 + 240 + 360 | C4.3 |
| SYS-NC1 global descriptive identity | F·3·Z | 72 | C4.4 |
| D7 diagnostic matrices (SYS-LIM) | 3 folds × K | 12 | C4.5 |
| Stage files written | S0, S1, S2, S3, S4, 7 fit_freeze, 7 evaluation, results, report | 21 | C8.1 |

**C8.4 Accounting for reduced or stopped work.** For every (system, stage), the package records:

> scheduled = attempted + not-propagated(VOID) + not-propagated(UNRESOLVED) + not-reached(STOP)

Attempted propagations are further split into valid-finite, guard-invalid (stored null, counted), ValueError and non-finite, following the inherited policy that every edit is propagated and guard failures are counted (`stages.py:95–121`).
- **VOID.** For each voided prefix (SYS-FK, SYS-NC1–NC3): its 16 baseline propagations are not made. If it is an evaluation prefix in a fold, that fold's edits on it are not propagated: 16·32·4 = 2,048 edits = 10,240 propagations per (fold, voided evaluation prefix). They stay in the coverage denominator.
- **UNRESOLVED or unavailable map.** That map's prediction is not propagated, which is one propagation per affected edit:
  - per unresolved (fold, class) map: 1,024·4 = 4,096 edits, so 4,096 propagations;
  - per unresolved global map: 4,096·4 = 16,384.

  The comparison is not pooled (C3.9).
- **INVALID.** A predicted or actual belief failing the guard is still attempted and counted (inherited). A scoreable-edit failure stops the package (`stages.py:103–116`).
- **STOP** (cap, reserve, projection halt or integrity). The unreached count is recorded per stage. Partial outputs are kept and labelled INCOMPLETE.
- **Closure check.** If the identity fails for any (system, stage), or attempted float propagations exceed 3,443,968, the result is INTEGRITY STOP (exit 7).

**C8.5 Caps (E38-14, verbatim in §2b).**
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

**C8.7 Workload estimate (UNVERIFIED feasibility estimate, not a guarantee).**
- **Reference run.** The sealed oracle run made 784,960 float propagations (`results.json:72`) in t_elapsed_s = 21.7287 (`results.json:26466`). That is ≈ 36,125 propagations/s overall, including its setup and reporting.
- **Linear scaling** to 3,443,968 gives ≈ **95.3 s**.
- **Not covered by the reference.** 541 SVDs on small designs (largest fit design 384 rows × 3, global; class designs 96 × 3; largest B3 stack 384 × 8) and serialization of the arrays above. On paper both are small against the 540 s stop. Neither has been measured.
- **Memory.** Not estimated. Per-edit forecasts are aggregated into loss cells, not stored per edit. A memory estimate is TO BE FIXED BEFORE FREEZE, in the application.
- No pilot is run (#38 L372).

## 9. Manifest, seal and approval

- **C9.1 One package.** It has its own scope, code, manifest and post-run index. Astra reviews this revised scope and the Research Lead freezes it before anything executes (E38-16; #37 L146).
- **C9.2 Sequence (N2, v1_4_N L22–30).**
  1. Code and the draft manifest are complete.
  2. The standing-approval application is filed. It cites by sha256 this record (as frozen), the #38, #37 and #36 raw files, the governing set, every implementation file and every input.
  3. The application sha goes into the manifest.
  4. The manifest is sealed.
  5. Stage S0 begins.
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
  - The output schema and paths.

  No value is set or changed after any output of this package is seen (E37-9, E38-11).

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

## 11. Status of Q1–Q17 and remaining open questions

**Q1–Q17: all closed by #38 (L253–276).**

| Q | #38 ruling | Where applied |
|---|---|---|
| Q1 | descriptive-only, plain 4-class, 7 systems, no floor | C3.2, C6 |
| Q2a | withdraw v1 Option B | change log 2 |
| Q2b | D2′ algebra accepted; B-repaired not included | change log 3 |
| Q2c | no tied bilinear | C3.2 |
| Q2d | effective basis stated, no augmentation | C3.2 |
| Q3 | B1 extension; no survivor pooling | C3.9 |
| Q4 | thresholds as synthetic conventions; H = L_μ,class; no prediction | C7.3 |
| Q5 | stop; operational diagnosis only | C4.0, C7.1 |
| Q6 | keep SYS-FK; correct impossibility claim | C4.3 |
| Q7 | cubic and RMS accepted; exact-law P_a; no adjustment | C4.4.R |
| Q8 | yes | C4.2(b) |
| Q9 | #38 tolerances | C5.5 |
| Q10 | reuse with hashes; disclose | C5.2, §0 |
| Q11 | P0 plus state map, weights, orbits, rank | C4 notation |
| Q12 | four sizes, 0.1 reference | C5.2 |
| Q13 | SYS-O6 allowed; not a rerun | C4.1 |
| Q14 | A-vs-BCD midpoint, no split | C4.5 |
| Q15 | SYS-LIM reported only; SYS-PC rank lapse gives NOT MET (RANK) | C7.2 |
| Q16 | not applicable | change log 7 |
| Q17 | yes | C4.5 |

**Items TO BE FIXED BEFORE FREEZE (or computed by the package under a frozen rule).**
1. c₂: TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW (C4.4.R).
2. c₃: TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW (C4.4.R).
3. Full-precision D_ψ, D_μ and the crossing bounds are computed by the package at S4 under C3.12. The rule is frozen; the displayed values do not govern.
4. Full sha256 of Q, Q₂ and the directions arrays, plus their generation conventions, recorded in the manifest (Q10). TO BE FIXED BEFORE FREEZE.
5. Memory estimate and substantiated workload in the application (C8.7). TO BE FIXED BEFORE FREEZE.
6. Output schema and file paths (C9.5). TO BE FIXED BEFORE FREEZE.
7. Rulings or acceptance on Q-R1 to Q-R6. TO BE FIXED BEFORE FREEZE.
8. Implementation code, manifest and standing-approval application (C9.2). Not yet written.

**Remaining open questions.** These are new execution specifications that v1.2 proposes. Each needs Astra review, not a ruling already given.
- **Q-R1 (D7 handling).** v1.2 flags a failed applicable D7 identity as D7 INVESTIGATE, with no stop and no effect on any label. Is that the intended reading of "warrants investigation" (#38 L198)?
- **Q-R2 (class zero-gain cells).** v1.2 applies the gain tolerance to SYS-FK class losses per fold/class/group/size cell, extending #38 L296's fold/group/size. Confirm.
- **Q-R3 (rank lapse in other controls).** v1.2 reads E38-12's "every required control identity and its rank premise" as making SYS-O6 and SYS-FK rank lapses also NOT MET (RANK). E38-12 names only SYS-PC explicitly.
- **Q-R4 (guard failure of an exact predictor).** Under C5.3(c), a guard failure of a predictor covered by an applicable exact-recovery identity, when the actual belief is valid, counts as an identity failure. Confirm that this is the E38-7 "contradict" case.
- **Q-R5 (extended B3).** Are the C3.11 stacking convention (unweighted J; per fold and per fold×class) and the band handling (UNRESOLVED-B3 recorded, no stop) acceptable?
- **Q-R6 (cache policy and stage order, C8.1–C8.2).** Specifically: per-system baseline propagation with no sharing; no prediction deduplication; the SYS-NC1 P0 sub-check at the start of S4.

## 12. Verification

**12.1 Checks run by me (read only; arithmetic on committed data).**
- Raw #38 sha256 = `87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5`, 385 lines. The 16 E38 quotes, the 43 body excerpts, the Q table, the model block and the tolerance block were extracted programmatically from the raw lines and checked as exact substrings.
- The E37 quotes were re-checked against #37 raw (`ce010fdb…63e2`).
- The exact rational t was computed from `stage_O1.json` `stage4_chart_exact` [0][0] and [3][0].
- `stage_O1.json` keys: `T_O1_s`, `continuation_strings_shared`, `failures`, `fold_spec`, `mismatch_count`, `mismatches`, `n_O1`, `orbits`, `split_table`, `stage4_chart_exact`, `stage`, `status`, `test_count`, `train_count`, `val_readout_rejection`. There is no P_h or P_a, so c₂ and c₃ cannot be computed exactly here.
- Accounting arithmetic: 7·(98,304·5 + 256) = 3,442,432 (matches #38 L369); + 1,536 = 3,443,968; 784,960/21.7287 ≈ 36,125/s; 3,443,968/36,125 ≈ 95.3 s.
- Line citations were checked: `pinned.py` (L10–11, L17, L21, L24–29, L37–41), `stages.py` (L48, L95–121, L149–154, L285–291, L323–329), `results.json` (L4, L70, L72, L26466).

**12.2 UNVERIFIED.**
- D1–D7 and P0.
- All numerical ranks.
- Full-precision normalizations and bounds.
- c₂ and c₃.
- NC admissibility.
- The validity bounds for SYS-FK.
- Workload, runtime and memory.

**12.3 Raw #38 versus the Specialist's summary (raw governs).**
- **Agrees:** descriptive-only treatment; plain per-class maps; 7 systems; no augmentation, shared e or floor; D1 first order; full column rank for D2/D4; matrix and prediction checks for cancellation; SYS-LIM reported with the A/BCD midpoint; D7 diagnostic; Q17; the L202 sentence; no impossibility claim; the SYS-FK counterexample r = κ_a; full-precision bound; exact-law c₂/c₃; B1 pooling suppression; SYS-PC NOT MET (RANK); SYS-O6 not a rerun; verbatim tolerances; E38-14 caps; E38-13 accounting.
- **Differences or omissions, followed per raw:**
  1. **Relabelling SYS-NC1.** The raw text corrects the description to a varying-κ two-coordinate confound (L160). It does not order a rename, so v1.2 keeps the name and relabels.
  2. **Plateau construction.** The raw text also rejects v1.1's dismissal of a two-coordinate plateau construction (L225). The summary mentions only the register example.
  3. **Diagnosis wording.** Q5 makes a failed identity "an operational failure diagnosis, not conclusive proof". v1.1's DERIVATION PREMISE / IMPLEMENTATION split is therefore withdrawn.
  4. **Rank premises cover SYS-O6 and SYS-NC2 too** (L73), not only D2 and D4.
  5. **Requirements the summary does not mention:**
     - E38-5: exact rationals, and the three charts with admissibility;
     - E38-6: the right-factor justification, frozen stacking, zero/band handling, no neural generalization;
     - E38-7: matrix identities before masking; an exact identity not hidden by another predictor's invalidity;
     - E38-8: flags stored under higher-priority labels; no zero-map substitution;
     - E38-11: system-level normalization, not per fold;
     - Q4: "No prediction that PC will meet them";
     - Q10: reuse with hashes, and disclosure;
     - Q12: four sizes;
     - Q11: P0 alone is insufficient;
     - L94: keep negative gains;
     - L186: NC2/NC3 are not a functional-form-only comparison, which withdraws note 1 item 3.
  6. **Tolerances.** Besides recovery and zero gain, the raw text adds the P0/C3.6(e) relative formula, the cancellation-sum formula, per-cell application with no pooled override, "not certified forward-error bounds", the exact-rational probability rule and retention of the rank bands and boundary convention (L280–302).
  7. **Q-ceiling.** E38-15 says the package "answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY". A phrase like "Q-CAUSE only" may be read only as "informs a possible later Q-CAUSE specification", never as a Q-CAUSE answer (C1.3).
  8. **Count.** #38 calls 3,442,432 "not yet the complete package count" (L372). The package maximum here is 3,443,968 float plus 272 exact.

**12.4 Not done.** No code was run. No oracle, solver, fit or simulation was executed. The repo was not modified, and v1.1 and note 1 were not edited. Nothing was posted or sent.
