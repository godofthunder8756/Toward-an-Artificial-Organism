# C-κ class-fit validation package: synthetic-only scope record v1 (Research Delegate draft)

**Status: DRAFT. NOT FROZEN. NOTHING RUNS.** Research Delegate (Track A), 2026-10-22 (ET). This is a new file, and no existing file was edited. I executed nothing: no training, no solver runs, no simulation, no checkpoint, no oracle code. The arithmetic marked "RD arithmetic" is my own hand or calculator work on committed numbers. Every expectation derived below is **UNVERIFIED** until an approved, frozen run. Nothing in this file authorizes execution (E37-9).

## 0. Sources, hashes and precedence

| Source | sha256 | Role |
|---|---|---|
| `/workspace/astra_consult37_response.txt` (Astra #37 raw) | `ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2` | **Governs over everything**, including this file |
| `/workspace/astra_consult36_response.txt` (Astra #36 raw, E36-1..14) | `c8342d5aa27c659dda5657e1e9ad70006a5e30759cc43eb25101d5546e756002` | Governs the inherited oracle definitions, below #37 |
| `/workspace/astra_serve37/c37_body.md` (#37 question packet) | `a97fc9400ec6311b70afac17a93f8c3c09e717d42348782e2024e31c2ada75ba` | Context only |
| `review/CKAPPA_ORACLE_CLOSEOUT_E37.md` | `4751e88c54c839df81df325ae9365607e7264314fe035b452295065b4b324fb9` | Close-out. It cites the raw file at `review/astra_consult37_response.txt`. Its sha matches, but the file actually sits at `/workspace/astra_consult37_response.txt` (path nit). |
| `review/CKAPPA_SCOPE_GOVERNING_SET_RL.md` | `6a5e0f24995a1349664349713e1ee0a550267ac06ab0e4b462b121d931c15c63` | Oracle governing set |
| `review/CKAPPA_SCOPE_RL_RULING_B2_B3.md` | `6d75918f7cc2ae06386d80400645345539d7e6f0d893f105bbb7fa0b2c563edd` | B2/B3 |
| `review/ckappa_oracle_scope_v1_4_N_closure_note.md` | `4ad1d217aaab0bd45d2be6fd3e24872a4b22407d0c8abc2fa36a5a1ac7c45c9c` | B1, 595 s, N-b |
| `review/ckappa_oracle_scope_record_v1_4_N.md` | `3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359` | N1–N4, n1–n5 |
| `review/ckappa_oracle_scope_record_v1_3_E36.md` | `f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5` | E36 verbatim, §3 values |
| `review/ckappa_oracle_scope_record_v1_1.md` | `e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c` | World, folds, O6/O7 definitions |
| `review/ckappa_oracle_results_review_RD.md` | `617e983d96c0487f7345fdaae83fe972cf9d5ffe5102f84a4b37e94ad73f64ba` | M-1 |
| PR #13 scratch clone `/workspace/scratch/pr13` @ `14376f38fe09157eef85bfac1cc4a4433d49bebc` | files: `stages.py` 936d3378, `linalg_fit.py` de6f4034, `geometry.py` 117e98e9, `world.py` 3d235fca, `pinned.py` 03c55323; outputs: `stage_O1.json` 794746a7, `stage_O7.json` 994dda0a, `results.json` 6adb5de2, `fit_freeze_O6.json` b6f817c8, `fit_freeze_O7.json` 347bcd51; `manifest.json` 4179b71a | Read only. Code hashes match the application `4df62ccd`. |

**Precedence (proposed for freeze).**
1. Astra #37 raw text.
2. E36 raw text.
3. This record.
4. The oracle governing set (RL `6a5e0f24` + B2/B3 `6d75918f` > closure note > v1_4_N > v1.3 > v1.2 > v1.1). It supplies every inherited definition that this record does not replace.

A conflict with #37 or E36 that is found later is resolved additively before execution.

**Development-informed disclosure (Astra #37 L162).** "This is development-informed work: O7 and its cancellation are already known. New freezing does not make them unseen."

## 1. Claim ceiling

- The package is **synthetic-only**. It measures what the class-conditioned fit can and cannot detect on declared synthetic systems.
- It **supports nothing about trained GRUs**. No checkpoint is opened (E37-9), so no neural sensitivity, recoverability, acquisition or causal finding can follow.
- **Q-tags.** It answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY. Its only role is to calibrate a measurement that a later, separately frozen **Q-CAUSE** study might use. Q-EXIST, Q-LEARN and Q-NECESSITY are untouched and stay separate.
- **No consciousness, C4, C5, "autopoietic" or "alive" claim** is made or implied.
- The ceiling for any later neural result is E37-10, quoted in §2.

## 2. Astra #37 items: verbatim text and compliance map

Each E37 item is quoted as an exact substring of the raw file, with the raw-file line in brackets.

**E37-1** [L170]
> "The completed oracle package is closed with ALL = MET and MARG = AVAILABLE under its frozen synthetic embedding, edits, weights, comparator and thresholds. These labels establish oracle-scale headroom only. They establish no result about GRU computation, acquisition, causal use, necessity, S12 or S15."

*Binding here:* C1.2 and C10.3. No oracle label is used as neural evidence or as a neural floor.

**E37-2** [L174]
> "The sealed manifest, code and outputs remain unchanged. Stale phase, version and sealing-description strings are documented additively. Runtime versions are described as asserted at preflight; elapsed-time and memory claims identify their recorded sources. The frozen exact-zero flag is retained and distinguished from the analytic symmetry statement."

*Binding here:* C9.4. The new package records observed runtime versions as observations, not pinned constants. It does not hard-code phase or seal strings, and it names the source of every timing or memory figure. Exact-zero flags are kept separate from tolerance checks (C4.6).

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

**E37-6** [L190]
> "The synthetic validation includes an explicitly defined sign-dependent positive control and a genuinely fixed-kappa control. Positive-control expectations are derived before execution. Class-dependent response generation is implemented by the synthetic system's declared state and readout, not supplied only to the analysis."

| Requirement | Clause |
|---|---|
| explicitly defined sign-dependent positive control | C4.2 (system S2, "PC±") |
| genuinely fixed-κ control | C4.3 (system S3, "FK") |
| PC expectations derived before execution | C4.2 derivation D1–D3 (written here; UNVERIFIED) |
| class-dependence generated by the system's own state and readout | C4.2: the readout computes sign(ψ₁ψ₂) from the state itself; the analyst's class label does not enter response generation |

**E37-7** [L194]
> "Smooth two-coordinate lookup systems are confound controls, not required gain-negative controls. A kappa-row gain in such a system is compatible with two-coordinate mediation. Neither the global nor the class-conditioned gain statistic identifies an independent covariance register or excludes the reachable-set lookup rival."

*Binding here:* C4.4 and C6. S4–S6 have **no** gain-must-vanish criterion, and their gain is reported, not passed or failed. A floor (Option A) or a matched basis (Option B) calibrates or removes one *known* confound only. Neither licenses exclusion of two-coordinate mediation or of the reachable-set lookup rival. Exclusion would need the different test in #37 L142, which is out of scope here.

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

*Binding here:* C10.4. It is carried forward verbatim as the ceiling for any neural spec this package might lead to.

**Other binding #37 body text (unnumbered, quoted).**
- **[L146]** "this response does not authorize an unspecified implementation to execute."
- **[L148–158]** The scope must fix:
  - canonical representatives, class labels, fold assignments and exact class-conditioned model (C3);
  - full and fixed-κ objectives, rank handling and freeze-before-scoring order (C3.2–C3.5);
  - each synthetic state encoding, readout, baseline chart, validity domain and analytic expectation (C4);
  - the PC's sign-switch boundaries and a prospective finite-edit rule (C4.2(f));
  - native versus synthetic units, directions, magnitudes, masks, coverage, weights and output groups (C5);
  - absolute and relative tolerances, expected identities versus substantive gain criteria (C5.5, C7);
  - global and class-conditioned outputs including matrices and normal-equation terms (C3.6);
  - failure, unresolved, headroom and cap outcomes without fixture replacement or parameter search (C7, C8);
  - a complete implementation and input manifest and the standing-approval application (C9).
- **[L160]** "Use one CPU, no GPU, 4 GB and ten cumulative wall-clock minutes including setup and reporting, with no automatic retries, subject to a substantiated workload estimate." Covered by C8.
- **[L116]** "Use the original global model as a fixed descriptive comparator. Report the actual matrices, their ranks and norms, and class/orbit-resolved losses. A kappa-row norm alone is not an outcome". Covered by C3.4 and C3.8.
- **[L118]** "The analyst supplies the class label. Success would not show that the neural system contains or consults that label." Covered by C3.7.

## 3. Design: classes, fits, stored terms, rank and pooling

**C3.1 Orbits, folds and class labels.** Orbits and folds are inherited unchanged: v1.1 §2 L48–49 and `geometry.py:7–22`. The orbits are A{0,5,10,15}, B{1,4,11,14}, C{2,7,8,13} and D{3,6,9,12}. The six directed 2+2 folds are AB→CD, CD→AB, AC→BD, BD→AC, AD→BC and BC→AD.

- **Representative.** The representative of each orbit is its smallest prefix: A→0, B→1, C→2, D→3.
- **Flip masks.** These come from `stages.py:208` (O1 flip fixture, PASS in `stage_O1.json`). Mask 5 is flip-X (μ_x→−μ_x, κ→−κ), mask 10 is flip-Y (μ_y→−μ_y, κ→−κ), and mask 15 is flip-X-and-Y (κ unchanged).
- **Class label.** g(a) = a XOR rep(orbit(a)), read as one of {I, X, Y, XY}:

| Class | A | B | C | D |
|---|---|---|---|---|
| I (mask 0) | 0 | 1 | 2 | 3 |
| X (mask 5) | 5 | 4 | 7 | 6 |
| Y (mask 10) | 10 | 11 | 8 | 9 |
| XY (mask 15) | 15 | 14 | 13 | 12 |

- **Signs (RD arithmetic, from the `stage_O1.json` `stage4_chart_exact` rationals, read only).**
  - All four representatives have μ_x > 0 and μ_y > 0, so at these 16 prefixes Astra's group-element class coincides with the sign quadrant (sign μ_x, sign μ_y): I=(+,+), X=(−,+), Y=(+,−), XY=(−,−). CNA's (s_x, s_y) partition is therefore the same partition here. E37-5's definition governs if they ever differ.
  - Write χ(g) = s_x·s_y (I:+1, X:−1, Y:−1, XY:+1). Then κ_a = χ(g(a))·κ_rep(orbit(a)).
  - κ does **not** have one sign within a class. For example, class I has κ = +0.1114 (A), −0.0120 (B), −0.1951 (C) and +0.0171 (D).
- **Per-fold counts.** Each fold's fitting set holds 2 prefixes per class, and so does its evaluation set (#37 L107). That is an identifiable grouping, not evidence of sufficient support.

**C3.2 Class-conditioned model.** For each system S, fold f and class g:
- **B_{f,g}** is the full 3×8 map, fitted on the class-g fitting prefixes of fold f.
- **B_μ,{f,g}** is the fixed-κ map: its κ row is fixed to 0 and its μ rows are fitted on the reduced 2-column design (E36-3; v1.3 §3).
- **Objective.** The objective is the E36-3 weighted least squares on ALL output components, with law weights w(a,u) = P_h(a,u) and all 16 continuations: min Σ_{a∈fit(f)∩g} Σ_u w(a,u)‖L_a(u)·X − J_a(u)‖². Here J_a(u) is system S's local response map (forecast change per unit synthetic-state change) and L_a(u) = ∂Φ/∂θ at S's own baseline chart.
- **Reporting.** The same maps are used for ALL, MARG and XOR reporting.
- **Evaluation.** A class map is applied unchanged to the class-g prefixes of the evaluation orbits (#37 L105).

**C3.3 Solver and rank (inherited, unchanged).**
- The rank check uses one SVD of the √w-weighted design, per B2/B3 non-blocking item (c) and `linalg_fit.py:21–75`.
  - σ_i/σ_1 > 10⁻⁶ is resolved. σ_i/σ_1 < 10⁻¹⁰ is resolved zero. The band [10⁻¹⁰, 10⁻⁶], endpoints included, is UNRESOLVED (E36-8).
  - σ_1 = 0 exactly means rank 0 and a zero fit.
- The fit is minimum-norm, inverting only σ_i > rcond·σ_1 with rcond = 1e-10 (N3, `pinned.py:17`).
- **B2.** A resolved lower-rank design is fitted minimum-norm and **scored**, with its rank and σ_1 reported. Only rank-UNRESOLVED cells go unscored, and they stay in the denominator.
- The check is applied separately to every (system, fold, class) design and to every global design.

**C3.4 Global comparator.** The original global B and B_μ per fold (O6/v1.1 L84, E36-3) are fitted for every system with the same solver. They are reported as a **fixed descriptive comparator** (#37 L116). No global statistic determines a package outcome, except the expected identities in C4.

**C3.5 Freeze-before-scoring order.** For each system:
1. Compute every global and class design and fit from fitting prefixes only.
2. Write them, with their stored terms (C3.6), to `outputs/fit_freeze_<system>.json` and fsync.
3. Only then propagate any evaluation-prefix edit.

No fit is recomputed after evaluation begins.

**C3.6 Stored outputs (E37-8).** Arrays are float64 C-contiguous little-endian. Each records name, shape, dtype `<f8` and the raw-byte sha256 (closure note N-b, L22–24).
- **(a) Matrices.** Every fitted B and B_μ, global and per class, for every system and fold, stored in full, not only as hashes. Under Option B, the augmented maps too (C6).
- **(b) Rank reports.** σ (full list), σ_1, ratios, numerical rank, the unresolved flag and n_inverted, for every design.
- **(c) Losses.** L_μ, L_full, S and measured gain L_μ − L_full, per (system, fit type ∈ {global, class}, fold, class, evaluation orbit, group, ε_syn). Weighted and unweighted values are both given, along with the scoreable counts and law mass behind each.
- **(d) Normal-equation terms.**
  - Per prefix a: G_a = Σ_u w(a,u) L_a(u)ᵀL_a(u) (3×3) and r_a = Σ_u w(a,u) L_a(u)ᵀJ_a(u) (3×8).
  - Per (fold, class), the sums ΣG and Σr that define B_{f,g}. Per fold, the global sums.
  - The 2×2 μμ block and the μ rows of Σr that define B_μ.
- **(e) Cancellation diagnostics (#37 L35–62).**
  - Per (system, orbit): Σ_{a∈orbit} G_a[κ,μ_x], Σ G_a[κ,μ_y] and Σ G_a[μ_x,μ_y].
  - For two-coordinate systems: Σ_{a∈orbit} G_a[κ,κ]·Dg(μ_a).
  - Per (prefix, flip): max|G_{g·a} − R_g G_a R_g|, where R_X = diag(−1,1,−1), R_Y = diag(1,−1,−1) and R_XY = diag(−1,−1,1).
  - These are descriptive identity checks with tolerances set in C5.5. They are not outcome criteria.

**C3.7 Disclosure (E37-5, #37 L118–120).**
- The class label is **supplied by the analyst** from the prefix index.
- Each class-conditioned model has 4× the parameters of the global model: 4×24 for full and 4×16 for fixed-κ, against 24 and 16.
- Success would not show that any neural system contains or consults the label. Four class maps address only the declared flip-class form of variation, not arbitrary nonlinear encodings.

**C3.8 Diagnostics only (E37-8).**
- **κ-row norm.** ‖row_κ(B)‖₂ for every global and class map, in chart-κ units per unit synthetic state. Its scale depends on the fitted coordinates (#37 L116).
- **Per-prefix local fits.** An optional single-prefix B_a, 48×3 design. These use evaluation-prefix Jacobians and so abandon the held-out claim (#37 L113).
- Neither enters any outcome.

**C3.9 Voiding and unresolved classes.**
- **Voiding.** Systems whose baseline chart is not the true chart (S4–S6) inherit the N4(ii) per-prefix voiding and the ≥5-of-16 RESTRICTED COMPARATOR NOT ADMISSIBLE ceiling (v1_4_N L38–43; B2/B3 item (a)).
- **Empty classes.** A class with 0 non-voided fitting prefixes in a fold is a rank-UNRESOLVED class cell: not scored, and kept in the denominator.
- **Proposed rule (B1 extended).** If any (fold, class) design of a system is UNRESOLVED, that system's pooled class-conditioned statistic is **not formed** (REFERENCE RANK UNRESOLVED), mirroring closure note B1 (L15). CNA's alternative, voiding the class cell and pooling the rest, is OPEN QUESTION Q3.

**C3.10 Pooling (E36-5, inherited).** Occurrences are pooled with their original w(a,u), equal direction and sign weights, normalized once over the pooled scoreable occurrences. Fold-normalized losses are never averaged. The class-conditioned statistic pools over all 6 folds × 4 classes of evaluation occurrences. H, S and their ratio use identical masks and weights.

## 4. Systems and derived expectations

**Notation.**
- θ = (μ_x, μ_y, κ) is the chart and Φ(p,u) the forecast (E36-2).
- Forecasts are q_X = m_x, q_Y = m_y and q_XOR = m_x + m_y − 2(m_x m_y + c) (`world.py:146–150`).
- **Output flip action.** Under flip-X, (q_X, q_Y, q_XOR) → (1−q_X, q_Y, 1−q_XOR) (RD arithmetic from `world.py:146–158`). So dΦ changes by P_X = diag(−1,1,−1), and P_Y is the analogue.
- **Premise P0.** Together with the O1 terminal-flip and probability-invariance fixtures (`stages.py:221–231`), P0 gives L_{g·a}(g·u) = P_g L_a(u) R_g, w(g·a, g·u) = w(a,u), and hence **G_{g·a} = R_g G_a R_g**. P0 is UNVERIFIED numerically and is checked by C3.6(e).
- **Systems.** S1–S3 are implementation and positive controls with **expected identities**. S4–S6 are **confound controls** under E37-7, with gain reported, not passed or failed.

**C4.1 S1: existing affine exact-filter control (O6; retains its positive implementation role, #37 L124).**
- State, readout, embedding (Q, seed 35006) and edits are exactly as in O6 (v1.1 L83–91; v1.3 §3).
- **Expected:**
  - global B = D·Qᵀ to ≤ 10⁻⁹ (v1.1 L90), and Pred_full error ≤ 10⁻⁹ on every scoreable edit (v1.1 L91);
  - every **class** B_{f,g} = D·Qᵀ to ≤ 10⁻⁹ whenever its design is resolved rank 3. The target is J = L·DQᵀ, which a resolved design reproduces exactly.
- B_μ,{f,g} = C_μ + (ΣG_μμ)⁻¹(ΣG_μκ)c_κ over the class's two fitting prefixes. That sum is generally non-zero within a class, because the cross term cancels only over whole orbits. So the class comparator loss **may differ from the O6 global value** (UNVERIFIED).
- This is a new package containing the O6 system as a control. It is not a rerun of the sealed package (see Q13).

**C4.2 S2: sign-dependent positive control "PC±" (E37-6; #37 L125). This is CNA's PC+, made concrete.**
- **(a) State.** ψ = (μ_x, μ_y, τ) with τ = sign(μ_x μ_y)·κ. By C3.1, τ_a = κ_rep(orbit(a)): it is flip-invariant and so the same within an orbit. The state is z = Q·D_ψ⁻¹(ψ − ψ̄), with Q the 8×3 matrix of seed 35006 (reused; TO BE FIXED BEFORE FREEZE whether to reuse). ψ̄ and D_ψ are the P-weighted mean and SD of ψ over the 16 prefixes, computed in-package as in `stages.py:323–330`.
- **(b) Readout (autonomous).** Recover ψ = D_ψ Qᵀ z + ψ̄. Then set θ = (ψ₁, ψ₂, sign(ψ₁ψ₂)·ψ₃) and forecast with Φ.
  - The class/sign information is carried by the state (the signs of ψ₁ and ψ₂) and used by the readout. The analyst's label is never used in generating responses.
  - At each prefix the baseline chart equals the true θ_a, because sign² = 1. So L_a(u), the weights and the global and class **designs are identical to O6's**, and the global designs are known resolved: every O6 fold scored in `fit_freeze_O6.json`. The class designs are new and their rank is UNVERIFIED.
- **(c) Local map.** With C = D_ψQᵀ (rows c_x, c_y, c_τ) and S_a = diag(1, 1, χ_a), the response is J_a(u) = L_a(u)·S_a·C. It is exact for finite edits that do not cross a sign boundary, because the readout is then linear: θ' = θ_a + S_a C δ.
- **(d) Derivation D1, global fit (UNVERIFIED).** Take prefix a = g·r in a complete orbit with representative r, and write R_g = diag(r_x, r_y, χ_g).
  - By P0, G_a S_a = R_g G_r R_g S_g = R_g G_r diag(r_x, r_y, 1).
  - Summing over the Klein group, Σ_orbit G_a S_a = 4·diag(G_r[xx], G_r[yy], 0). Every off-diagonal coefficient and the κκ coefficient sums to zero, because each carries a factor r_x, r_y or r_x r_y.
  - Likewise Σ_orbit G_a = 4·diag(G_r[xx], G_r[yy], G_r[κκ]).
  - For any fit set that is a union of complete orbits (all six folds), the normal equations ΣG·B = ΣG S C give **B = [c_x; c_y; 0]** whenever ΣG's diagonal is positive.
  - The fixed-κ fit gives **B_μ = [c_x; c_y]**, the same μ rows.
  - Hence global Pred_full ≡ Pred_μ for finite predictions too, so **global measured gain = 0** up to rounding, and global L_full = L_μ > 0. The unpredicted part is L_a[:,κ]·χ_a·c_τ·δ.
  - Conditions: complete orbits, invariant weights, no exclusions. These hold for S2 because its baseline is the true chart and so is never voided.
  - This is the blind spot M-1 describes, now exhibited by an explicit state code.
- **(e) Derivation D2, class fit (UNVERIFIED).** Within class g, S_a = S_g is constant. So Σ_{r∈fit} G_{g·r}·B = Σ G_{g·r} S_g C gives **B_{f,g} = S_g·C** exactly when the class design is resolved rank 3. Then Pred_full is exact on every non-crossing scoreable edit, to the O6 tolerance of 10⁻⁹.
  - **D3.** B_μ,{f,g} = C_μ + χ_g(ΣG_μμ)⁻¹(ΣG_μκ)c_τ, with ΣG_μκ taken over the two fitting prefixes, which is generally ≠ 0. So class measured gain = L_μ,class − L_full,class = L_μ,class ≥ 0, and > 0 unless the comparator reproduces the κ response exactly.
  - **Not derived:** the *magnitude* of L_μ,class, and CNA's statement that "per-class R [is] near the O6 value". D3 shows the class comparator absorbs a class-dependent part of the κ response through its μ rows, so no equality with O6's R (0.07988, #37 L11) follows. The magnitude is a measured quantity, judged against thresholds fixed before freeze (C7, Q4).
  - If a class design is resolved lower rank (B2), D2 does not hold. That cell is scored min-norm and the identity expectation lapses, so the package reports EXPECTATION NOT APPLICABLE (RANK) and does not count it as an identity failure.
- **(f) Sign-switch boundaries and finite-edit rule (#37 L153).**
  - **Boundaries.** The boundaries are ψ₁ = 0 and ψ₂ = 0.
  - **Rule (prospective).** An edit is *crossing* if sign(ψ'_i) ≠ sign(ψ_{a,i}) or ψ'_i = 0 for i ∈ {1, 2}, where ψ' is the actually perturbed state. A crossing edit is **not scoreable** for every model of S2. It enters the common mask (C5.3), counts in the coverage denominator, is never replaced and is never assigned zero error (E36-4 analogue). Crossing counts are reported per class and ε_syn.
  - **Derived expectation: 0 crossings (RD arithmetic; UNVERIFIED).**
    - Bound. |Δψ_i| = ε·|(D_ψQᵀv)_i| ≤ ε·sd_i, since Q has orthonormal columns and ‖v‖ = 1. Also sd_i ≤ max_a|ψ_{a,i}|.
    - Data (`stage_O1.json` `stage4_chart_exact`). min|μ_x| = 0.2501 and max|μ_x| = 0.5301; min|μ_y| = 0.4276 and max|μ_y| = 0.7303.
    - Result. At the largest declared ε_syn = 0.25, |Δμ_x| ≤ 0.1325 < 0.2501 and |Δμ_y| ≤ 0.1826 < 0.4276. So no crossing is possible at any declared size.
    - Any crossing observed is therefore an integrity diagnosis (C8.2), not a mere coverage loss.
- **(g) Expected outcome labels (§5 of this record).**
  - S2-global: GLOBAL CANCELLATION AS DERIVED, if |L_μ − L_full| ≤ tol_gain (C5.5) in every group and size.
  - S2-class: CLASS RECOVERY AS DERIVED, if the Pred_full identity holds to 10⁻⁹ and every class B_{f,g} = S_g C to 10⁻⁹. Class headroom is then judged by C7.

**C4.3 S3: genuinely fixed-κ control "FK" (E37-6; #37 L126).**
- **State.** z = Q₂·D_μ⁻¹(μ − μ̄), with Q₂ the 8×2 matrix of seed 35007 (reused, as in O7; TO BE FIXED BEFORE FREEZE).
- **Readout.** θ = (μ_x, μ_y, 0), the product belief. κ is fixed at 0 by construction for every state, so no edit can move it. The baseline chart is (μ_a, 0), which is not the reachable chart. Derivatives are taken about this baseline, and disagreement with the true reachable forecasts is reported separately (E36-6 convention).
- **Validity (RD arithmetic; UNVERIFIED).**
  - Product-belief p ≥ ((1−|μ_x|)/2)·((1−|μ_y|)/2).
  - At baseline the minimum is 0.2350 × 0.1349 ≈ 0.0317 (orbit A).
  - With the C4.2(f) edit bound at ε_syn = 0.25 it is ≥ 0.1687 × 0.0436 ≈ 0.0074.
  - Both exceed the 10⁻⁶ guard. So no FK baseline is voided, and no actual or exactly predicted edit is invalid at any declared size.
- **Derivation D4 (UNVERIFIED).** J_a = L_a[:,μ]·D_μQ₂ᵀ, so the marginal-only model is exact.
  - The full normal equations ΣG·B = ΣG·[C_μ; 0] give **B = [C_μ; 0]**, and B_μ = C_μ, for every resolved design, global or class.
  - Hence Pred_full ≡ Pred_μ ≡ actual (readout linear in z). So L_full = L_μ = 0 to rounding, gain = 0, and S > 0.
  - **Expected label: FIXED-κ IDENTITY AS DERIVED**, if max|Pred_full − actual| and max|Pred_μ − actual| ≤ 10⁻⁹ and |gain| ≤ tol_gain, for both fit types.
  - This is the check that "adding the kappa row does not create substantive gain when the specified marginal-only model already predicts the responses exactly" (#37 L126).
- An alternative FK, a piecewise-constant κ lookup at the true κ_a, is listed as Q6.

**C4.4 S4–S6: smooth two-coordinate confound controls (E37-7; #37 L127–138). These are not gain-negative controls.** Each system is z = Q₂·D_μ⁻¹(μ − μ̄) with chart (μ_x, μ_y, g_k(μ)). Derivatives and finite predictions are taken about its own baseline chart. Validity is checked per prefix before derivatives, and N4(ii) voiding applies. g is never refitted and no prefix is replaced (E36-6). The B3 stop is extended to every two-coordinate system (C8.2).
- **S4 = O7 (NC-1, symmetric).** The g basis, coefficients and normalization are exactly O7's: v1.3 §3 L111, the quadratic P-weighted fit recomputed in-package. Committed `stage_O7.json` `g_coefficients` ≈ [3.7e-17, 8.1e-18, 1.6e-17, 1.2e-17, 0.14038, −8.2e-17], i.e. g ≈ 0.1404·μ_xμ_y.
  - Global expectation: Pred_full ≡ Pred_μ, gain 0 (#37 L56–62). This applies **only if 0 prefixes are voided**, since voids break orbit completeness (#37 L64). It is a descriptive identity check.
  - Class fit: within a class, Dg(μ_a) = 0.1404·(μ_y, μ_x) varies across the two fitting prefixes, so the κ row need not cancel. **A class gain of either sign is permitted and reported.** A positive gain is "compatible with two-coordinate mediation" (E37-7).
- **S5 = NC-2, prespecified symmetry-breaking affine example (#37 L127, L138).** Proposed g₂(μ) = c₂·μ_x (affine and odd in x only, so it breaks the odd-odd symmetry).
  - Derivation D5 (UNVERIFIED): Dg₂ = (c₂, 0) is constant, so the true local map M·C₂ is constant. Both the global and the class full models are then exact for resolved designs (finite predictions exact, because the readout is linear in z), and **gain = L_μ > 0 generically under both fit types**.
  - This is Astra's explicit example: "For an affine g, the full local chart map can be exact" (#37 L138). The gain is expected and is not evidence of a covariance register.
  - c₂: TO BE FIXED BEFORE FREEZE by a rule declared in the frozen file, not by search. The rule must give a valid baseline at all 16 prefixes and must not be chosen on the basis of any gain value.
- **S6 = NC-3, nonlinear law outside the Option B basis (CNA's transfer test).** Required under Option C, optional under Option A, and excluded under Option B unless Astra asks for it.
  - Proposed g₃(μ) = c₃·μ_x². It is even-even, so it breaks the world's odd-odd symmetry, and it lies outside the basis {μ_xμ_y}.
  - c₃: TO BE FIXED BEFORE FREEZE by the same kind of declared rule. Whether this form is acceptable is Q7.
  - No gain expectation. It is reported.

## 5. Units, edits, masks, weights, groups and tolerances

- **C5.1 Units.** All systems are synthetic. Edits are δ = ε_syn·sign·v in the 8-D synthetic state, with no native units. The field name is `eps_syn` (v1_4_N L73).
- **C5.2 Edits (proposed reuse; TO BE FIXED BEFORE FREEZE).**
  - The 16 unit directions of seed 35016, the same array as O6/O7 (`results.json` drawn_arrays, sha 5ed4bc8b…), applied +v then −v.
  - ε_syn ∈ {0.02, 0.05, 0.1, 0.25}, with reference size 0.1 (`pinned.py:28–29`).
  - Edits are applied on evaluation prefixes × 16 continuations, giving 4096 per fold per size (`stages.py:48`).
- **C5.3 Common mask.** Per system, an edit is scoreable iff:
  - the actual perturbed belief and all four predicted perturbed beliefs (global full, global μ, class full, class μ; plus the augmented maps under Option B) pass p ≥ 10⁻⁶; and
  - for S2, the edit is non-crossing (C4.2(f)).

  The same mask applies to L_μ, L_full and S for both fit types (E36-4 extended). Count and law-mass coverage are reported per fold, class and size.
- **C5.4 Weights and groups.**
  - w(a,u) = P_h(a,u), with uniform direction, sign and size weights (v1.1 L62).
  - Groups are ALL, MARG and XOR, reported separately. Section-5-type outcomes use ALL and MARG at ε_syn = 0.1 (`geometry.py:30`).
  - Ratios are worded per E37-3.
- **C5.5 Tolerances.**
  - The identity tolerance on predicted responses and maps is 10⁻⁹ maximum absolute (v1.1 L90–91; `pinned.py:21`).
  - The BOUNDARY band is relative 10⁻⁶ (v1_4_N L16).
  - **TO BE FIXED BEFORE FREEZE:**
    - tol_gain, the absolute and relative tolerance for "gain = 0" identities (S2-global, S3, S4-global). It must be stated relative to S and as an absolute floor, before execution.
    - The tolerance for the C3.6(e) normal-equation identity checks.
  - Exact-zero flags, if any, are reported as such and distinguished from tolerance checks (E37-2).

## 6. Handling the smooth-lookup confound: declared options for Astra (choice left open)

E37-7 governs all three options. None turns a smooth-lookup system into a required gain-negative control, and none licenses exclusion of two-coordinate mediation or of the reachable-set lookup rival.

**Option A: empirical NC floor (measured on this design).**
- **Floor F_A.** F_A is the pooled class-conditioned measured-gain ratio (L_μ − L_full)/S for S4 (O7), per counted size and group. It is declared as the reference that a *later* neural spec's class gain would have to exceed before the spec could word a result as more than the O7-type confound would produce.
- **Limits.**
  - F_A is measured on **one κ law**. A trained GRU's μ-only nonlinearity need not match it, so F_A may not transfer.
  - Clearing F_A says only that the gain exceeds what that one declared confound produced. It does not exclude two-coordinate mediation (E37-7).
  - F_A is not an outcome for S4. S4 neither passes nor fails.

**Option B: matched declared basis in both models (the Delegate's proposal).**
- **Construction.** Give B_μ and B, in each class, the same pre-declared μ basis Φ_b. The minimum is {μ_xμ_y}; the full basis is TO BE FIXED BEFORE FREEZE.
  - The predicted κ-change row becomes μ_{y,a}·e₁ + μ_{x,a}·e₂ (the derivative of μ_xμ_y at the baseline), with free 1×8 rows e₁ and e₂. This is linear in parameters, so the frozen solver applies.
  - The full model adds its free κ row b_κ.
- **Intended effect.** Under κ ≡ g(μ) ∝ μ_xμ_y, the augmented fixed-κ model is exact. The full model's κ column should then be redundant, giving REFERENCE RANK UNRESOLVED or zero gain.
- **Honest limits, including a correction to my earlier room statement (derived here; UNVERIFIED).**
  - **(i) Structural rank deficiency.** Each class has only 2 fitting prefixes (#37 L107). The full model's κ part then has three functions (1, μ_y, μ_x) evaluated at two base points, so its design is rank-deficient **in every class, for every system, not only under the NC**.
    - Under the frozen rule, exact deficiency gives a ratio far below 10⁻¹⁰, i.e. resolved lower rank, so **B2 fits it minimum-norm and scores it**. Ratios landing in the band by rounding would read UNRESOLVED instead, which makes the outcome rounding-dependent.
    - Under min-norm, the split between b_κ and e₁, e₂ is set by the null direction (a function vanishing on the line through the two fitting μ's). Evaluated at the held-out prefixes' different μ, the full model's predictions can deviate while the augmented fixed-κ model stays exact. So under S4 the expected held-out class gain is **≤ 0, not = 0**.
    - My earlier statement that the frozen rank rule would return RANK UNRESOLVED or zero gain "by construction" therefore does not hold as stated for 2-prefix classes.
    - Possible repairs:
      - sharing the basis rows e across classes within a fold, which departs from E37-5's "separately fitted within each class";
      - a tied bilinear form κ-row = γ·Dφ(μ_a)·B_μ, which needs a non-frozen nonlinear solver.

      Both go to Q2.
  - **(ii)** The basis removes only leaks **inside** it. A μ-only nonlinearity outside Φ_b (for example S5 or S6) still leaks through the κ column.
  - **(iii)** It raises both models' flexibility further, which must be disclosed (E37-5).
  - **(iv)** Under E37-7 a zero NC gain was never required, so Option B's value is interpretive (removing a known confound), not a pass criterion.

**Option C: both (CNA's view).** Use the Option B basis, plus an Option A floor measured on that augmented design (S4), plus S6, a second NC whose μ-only law lies outside the basis. S6 tests directly whether the floor transfers. Option C inherits the limits of both A and B, including B(i).

**Choice.** This record leaves the choice to Astra: A, B, C, or "none; report confounds descriptively only". The C8 workload estimate covers the largest case (C).

## 7. Outcome labels and order (N1 extended consistently)

Labels are evaluated per system, per fit type and per group (ALL, MARG) at ε_syn = 0.1. Other sizes are reported and never replace the reference (v1.3 §2 last row). **First match wins:**

1. **PIPELINE INVALID.** Any of:
   - an O1 or O2 fixture failure;
   - an S1 identity failure;
   - an S2 D1/D2 or S3 D4 identity failure on a resolved design;
   - a B3-type resolved third direction in any two-coordinate system (C8.2);
   - a failed scoreable edit.

   The package stops and is not rerun under this record. Whether a derived-expectation failure stops the package or only labels it is Q5.
2. **REFERENCE COVERAGE NOT MET.** In some fold (and, for class statistics, some fold×class), count coverage < 75% (the integer test 4·n_s < 3·n_t) or law-mass coverage < 0.75·(1 − 10⁻⁶) (v1_4_N L13).
3. **REFERENCE RANK UNRESOLVED.** Any required design for that statistic is rank-UNRESOLVED (closure note B1 L15, extended per C3.9). No pooled statistic is formed.
4. **RESTRICTED COMPARATOR NOT ADMISSIBLE.** S4–S6 only: 5 or more of 16 prefixes voided (v1_4_N L41).
5. **ZERO RESPONSE.** Pooled S = 0 exactly (v1.3 §3 L109).
6. **S2-class only: HEADROOM NOT MET / BOUNDARY / MET.**
   - The class-conditioned √H and R = L_μ,class/S are compared with thresholds **TO BE FIXED BEFORE FREEZE**. The proposal is to reuse the v1.1 §5 declared conventions: ALL √H ≥ 10⁻³ and R ≥ 0.05; MARG √H ≥ 10⁻⁴ and R ≥ 0.02 (v1.1 L115–121; `pinned.py:24–27`). Q4 asks Astra to confirm.
   - The comparison uses the band rule of v1_4_N L15–16.
7. **Identity systems (S1, S2-global, S3):** IDENTITY AS DERIVED, or EXPECTATION NOT APPLICABLE (RANK) where B2 lower rank voids a derivation premise.
8. **Confound systems (S4–S6):** REPORTED. Gain, losses, matrices and κ-row norms are descriptive. There is no pass or fail (E37-7).

**Package summary label.**
- **CLASS-FIT VALIDATION MET** iff:
  - S1 is IDENTITY AS DERIVED;
  - S2-global is IDENTITY AS DERIVED (the cancellation is demonstrated);
  - S2-class is IDENTITY AS DERIVED and MET for ALL;
  - S3 is IDENTITY AS DERIVED, for both fit types.
- Anything else reads **CLASS-FIT VALIDATION NOT MET (<first failing reason>)**.
- Per #37 L164, MET licenses only a *decision* on whether a neural specification is warranted. It is not a neural spec, a neural floor or a neural result. The later neural absolute-response floor "remains unresolved; O6 does not supply it" (#37 L164).

## 8. Resources, integrity stops and timing

- **C8.1 Caps (#37 L160; inherited n3/n4/N-a).**
  - 1 CPU, no GPU, 4×10⁹ bytes (RLIMIT_AS; v1_4_N L68), 10 cumulative wall-clock minutes from before imports, including setup and reporting (E36-14). No automatic retries.
  - Wrapper kill at 595 s − (now − T0) (closure note L18). 60 s reserve, soft stop at 540 s, projection halt if T_rem > 540 s − T_elapsed (closure note L19).
  - CAP REACHED, CAP RESERVE REACHED (INCOMPLETE) and PROJECTION HALT are kept distinct.
  - Incremental, fsynced stage files (v1_4_N L65).
- **C8.2 Integrity stops (inherited, exit 7).**
  - Any hash mismatch of code, inputs or the application against the sealed manifest. Runtime-version mismatch.
  - A float-propagation overrun above the frozen scheduled count (application `4df62ccd` L22).
  - An edit-count mismatch (`stages.py:638–645` analogue).
  - **Extended B3.** In S3–S6 the stacked Jacobian J = [L_a M_a]·C₂ has rank ≤ 2 for every fold and class subset, because C₂ is a constant 2-row map. So σ₃/σ₁ > 10⁻⁶ in any such stack is an integrity diagnosis: STOP, PIPELINE INVALID (B2/B3 ruling L6; E36-7).
  - Any S2 sign crossing, since C4.2(f) derives that none is possible.
- **C8.3 Workload estimate (paper; UNVERIFIED; TO BE SUBSTANTIATED BEFORE FREEZE).**
  - Per system: 6 folds × 8 evaluation prefixes × 16 continuations × 16 directions × 2 signs × 4 sizes = 98,304 edits. Each edit needs 5 forecast propagations (actual, global full, global μ, class full, class μ), giving 491,520 + 256 baselines.
  - Totals: 6 systems (S1–S6) ≈ 2.95×10⁶. Under Option B or C, add 2 augmented predictions per edit: 7 per edit, ≈ 4.13×10⁶.
  - Reference: the sealed oracle run did 784,960 float propagations (`results.json:72`) in t_elapsed_s = 21.73 (`results.json:26466`, wrapper-T0 based, per E37-2). Linear scaling suggests roughly 80–115 s plus fits.
  - That is an extrapolation, not a bound. Step 0 timing and projection are inherited (E36-13).
  - The exact scheduled counts per stage are TO BE FIXED BEFORE FREEZE.

## 9. Manifest, seal and approval

- **C9.1 One package.** It gets its own scope, code, manifest and post-run index. Astra reviews it and the Research Lead freezes it before anything executes (E37-9; #37 L146).
- **C9.2 Sequence (N2, v1_4_N L22–30).**
  1. Code and the draft manifest are complete.
  2. The Research Lead files the standing-approval application, citing by sha256 this record (as frozen), the #37 and #36 raw files, the inherited governing set, every implementation file and the inputs at `5d9d8a7d1274d58e27e9a18380d1a33faaab57cc`.
  3. The application sha goes into the manifest.
  4. The manifest is sealed and immutable.
  5. Step 0 begins.
- **C9.3 Preflight.**
  - It asserts sealed: true, all hashes, and the runtime versions. It records the observed versions as observations (E37-2).
  - It asserts that the package reads no checkpoint or weight file. The allowed input set is enumerated in the manifest.
- **C9.4 E37-2 hygiene.** No hard-coded phase or seal strings in outputs. Every elapsed-time or memory figure names its source file and field.
- **C9.5 Frozen in the manifest (mirrors #37 L148–158).**
  - Representatives, class table and folds (C3.1).
  - Class and global objectives and the solver (C3.2–C3.4).
  - Freeze order (C3.5).
  - Each system's state, readout, baseline chart, validity domain and derivation (C4).
  - The PC boundary rule (C4.2(f)).
  - Units, directions, sizes, mask, coverage, weights and groups (C5).
  - Tolerances, including tol_gain (C5.5).
  - The chosen Option and its basis (C6).
  - Labels and order, with thresholds (C7).
  - Stops and caps (C8).
  - Stored-output schema and paths (C3.6; v1_4_N L74–81 pattern).
  - Every TO BE FIXED BEFORE FREEZE value. **None may be set or changed after any output of this package is seen.**

## 10. Wording rules

- **C10.1 Negatives (E37-4).** "The declared [global/class-conditioned]-map intervention-prediction criterion was not met." For a resolved negative, add: "This does not exclude prefix-dependent or nonlinear coordinate relations" (#37 L84–88).
- **C10.2 Ratios (E37-3).** "Comparator squared prediction error divided by actual response energy." Never "fraction carried by" or "absorbs".
- **C10.3 Oracle labels (E37-1).** "Oracle-scale headroom only."
- **C10.4 Later neural ceiling.** E37-10 verbatim.
- **C10.5 S2 success.** "The class-conditioned fit recovered the declared sign-dependent synthetic map, which the global fit cancels as derived." It does not show that a network uses κ, carries a class label, or has a covariance register.

## 11. Open questions for Astra

1. **Q1 (Option).** A, B, C, or descriptive-only (§6)?
2. **Q2 (Option B structure).** With 2 fitting prefixes per class, the augmented full model is rank-deficient in every class (§6 B(i)). Should it be:
   - scored minimum-norm under B2, accepting a possibly negative held-out NC gain;
   - repaired by sharing the basis rows across classes within a fold (a departure from E37-5's "separately fitted"); or
   - given a tied bilinear form, which needs a new solver convention?
3. **Q3 (unresolved class cells).** Should one rank-UNRESOLVED (fold, class) design suppress the system's pooled class statistic (B1 extension, C3.9), or be voided with the rest pooled (CNA)?
4. **Q4 (S2-class thresholds).** Reuse the v1.1 §5 conventions (√H 10⁻³ / R 0.05 ALL; 10⁻⁴ / 0.02 MARG), or other declared values? CNA's "R near the O6 value" is not derivable (C4.2 D3).
5. **Q5 (control-expectation failure).** Should an S2 or S3 derived-identity failure stop the package as PIPELINE INVALID, as with an O6 fixture failure, or only label it, leaving a separate diagnosis of derivation error versus implementation error?
6. **Q6 (FK form).** Is the product-chart κ ≡ 0 system (C4.3) "genuinely fixed-kappa"? The alternative is a piecewise-constant κ_a lookup on the true chart, which needs its own cell-boundary rule.
7. **Q7 (NC-2 and NC-3).** Are g₂ = c₂μ_x (affine, symmetry-breaking) and g₃ = c₃μ_x² (outside basis) acceptable? What declared rule should fix c₂ and c₃ without search?
8. **Q8 (PC± adequacy).** τ = sign(μ_xμ_y)·κ makes the stored quantity orbit-invariant, and the sign comes from the state's μ components. Does this satisfy E37-6's "explicitly encodes the sign/class information in its synthetic state"? Or is a second positive control wanted, with a separate explicit sign coordinate?
9. **Q9 (tol_gain).** What absolute and relative tolerance for "gain = 0" identities (S2-global, S3, S4-global)?
10. **Q10 (reuse of draws).** May Q (35006), Q₂ (35007) and the O6 directions (35016) be reused? Does E37-9 prefer fresh, declared seeds?
11. **Q11 (premise P0).** Is checking G_{g·a} = R_g G_a R_g numerically (C3.6(e)) sufficient support for D1's use of the output flip action?
12. **Q12 (sizes).** Keep all four ε_syn with 0.1 as reference, as in the oracle? Or declare counted sizes {0.1, 0.25} to match the prospective neural commitments?
13. **Q13 (S1 inclusion).** Confirm that recomputing the O6 system inside this new package is not a "rerun of the completed package" (#37 L29).

## 12. Verification notes

- **Checked by me (read only):**
  - E37-1..10 quoted text against the raw file (script substring check);
  - class table and κ signs from `stage_O1.json`;
  - flip masks from `stages.py:208`;
  - forecast formulas from `world.py:146`;
  - solver and rank code from `linalg_fit.py`;
  - O6 B matrices stored in `fit_freeze_O6.json`, but only hashes stored for O7 (`stages.py:908–925`);
  - float count and elapsed time from `results.json`.
- **UNVERIFIED:** derivations D1–D5, P0, the zero-crossing bound and FK validity bound (RD arithmetic), all class-design ranks, and the workload estimate.
- **Not done:** no code was run, no numbers were computed by package code, and nothing was posted.
