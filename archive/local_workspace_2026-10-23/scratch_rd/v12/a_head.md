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

"NC" is kept only as a legacy label. None of SYS-NC1–NC3 is a negative control, and none has a gain-must-vanish criterion (E37-7, E38-15). The bare token "S6" appears only inside the E37-4 quote, where it names the earlier prospective neural design.

## Change log relative to v1.1 + note 1

Each entry cites its #38 source. "Withdrawn" means the text is removed and must not be reintroduced without a new ruling.

**Withdrawn**
1. **Option A, the empirical NC floor.** Withdrawn per E38-1 and #38 L158: "Calling the number a 'floor' gives it a calibration role that has not been established."
2. **v1 Option B, the per-class matched basis.** Withdrawn per #38 L164 and Q2a.
3. **B-repaired (shared e) and derivation D2′.** Withdrawn per E38-1 and Q2b. Astra accepts the conditional algebra but does not approve the coupled class fitting. The dx/dy table goes with it.
4. **Option C, and the falsify-only text tied to it.** Withdrawn per E38-1 and #38 L184. No floor exists to be falsified.
5. **All matched-basis and effective-basis-span material.** This includes the v1.1 note that μ_x² lay "inside the span". Withdrawn per E38-1 and #38 L156. The effective basis is now stated explicitly as plain, with no augmentation (C3.2, Q2d).
6. **Note 1 §3** ("NC2 and NC3 ... differ only in being linear or nonlinear"). Withdrawn per #38 L186: "their different baselines and derivatives mean this is not a comparison in which only functional form changes."
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

