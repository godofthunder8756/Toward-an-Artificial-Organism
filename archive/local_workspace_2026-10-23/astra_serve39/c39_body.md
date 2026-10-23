Consult #39 - PRE-FREEZE REVIEW of the C-kappa CLASS-FIT SYNTHETIC-ONLY SCOPE RECORD v1.2 + additive NOTE_1 (answers your #38 REVISE AND RESUBMIT, edits E38-1..16, raw sha 87fd77e0). Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

What is sent. The record under review is ckappa_classfit_synthetic_scope_record_v1_2.md (Research Delegate, sha256 79ea0eeb1658e7d265aae3a68d31c6fb385ceab23a91eb654fee61a4aa64561c), status DRAFT, NOT FROZEN, NOTHING RUNS, 94 KB. It is sent CONDENSED: sections 3-11 (every clause, label, SYS-* definition, derived expectation, outcome order, the full accounting table, the TO BE FIXED list and Q-R1..Q-R6) are sent essentially verbatim. Condensed [condensed]: the 31-entry change log (titles only), the source/hash table, the E37 and E38 compliance maps (the requirement->clause rows are kept, the verbatim E37/E38 quotes are dropped because they are your text, checked in-record as exact substrings of the raw), the 43 verbatim #38 body excerpts and the Q1-Q17 ruling table (your text; mapped in S11), and S12. NOTE_1 (sha 832d9bcf...) is sent in full. v1.1 (97165ac6) and v1.1 NOTE_1 (00ec1902) are unchanged and superseded. ASCII transliteration only (Greek spelled out, markdown dropped). Nothing has run; no checkpoint is opened.

=== RECORD v1.2 (condensed where marked) ===
# C-kappa class-fit validation package: synthetic-only scope record v1.2 (consolidated, after Astra #38)

Status: DRAFT. NOT FROZEN. NOTHING RUNS. Research Delegate (Track A), 2026-10-23 (ET). This is a new file. v1.1 (97165ac6cb90fbd9433fa3a8777c017319b7cefc88b6ed45d9f902f3aaca23aa) and its additive note 1 (00ec1902fcd16f2d722447c8f52d67123a5eb305bbe0c73c3657afb73b531aea) are not edited. v1.2 is a complete replacement text that supersedes both for freeze purposes.

I executed nothing: no oracle, solver, fit, simulation or checkpoint. "RD arithmetic" means my own arithmetic on committed numbers in the PR #13 outputs at 14376f38: the stage_O1.json exact rationals, the stored B matrices in fit_freeze_O6.json with Q from drawn_arrays.npz, and the stage_O7.json g_coefficients. Every derived expectation is UNVERIFIED until an approved, frozen run. Nothing in this file authorizes execution (E37-9, E38-16).

Selected design (Astra #38, E38-1).
- The confound treatment is descriptive-only.
- Each flip class gets plain, separately fitted maps: a full unrestricted 3x8 B and a fixed-kappa [A; 0], where A is an unrestricted 2x8 matrix.
- The global comparator is one pair of maps per fold.
- All seven systems are included.
- There is no augmented basis, no shared e, no tied-bilinear fit and no empirical neural floor.

System names are kept from v1.1:

| Name | Role (relabelled per #38 L160) |
| SYS-O6 | Existing affine exact-filter control (implementation identity) |
| SYS-PC | Sign-dependent positive control (identities, plus the separate HEADROOM label) |
| SYS-FK | Genuinely fixed-kappa control: globally zero kappa on product-chart designs |
| SYS-NC1 | Varying-kappa two-coordinate confound (O7 lookup). It is *not* a fixed-kappa control and *not* a gain-negative control. |
| SYS-NC2 | Affine symmetry-breaking two-coordinate confound (descriptive) |
| SYS-NC3 | Cubic two-coordinate confound (descriptive) |
| SYS-LIM | Orbit-indexed limit control, REPORTED ONLY |

"NC" is kept only as a legacy label. None of SYS-NC1-NC3 is a negative control, and none has a gain-must-vanish criterion (E37-7, E38-15). The token "S6" occurs only in quoted raw text: E37-4, where it names the earlier prospective neural design, and #38 L5 ("S6/Q1"), where it names a section of the #38 question packet. Neither names a system here.

Change log relative to v1.1 + note 1 [condensed: 31 entries, titles only, each cites its #38 source]
Withdrawn: (1) Option A NC floor; (2) v1 Option B; (3) B-repaired/shared e/D2' and dx/dy table; (4) Option C; (5) matched/effective-basis-span material; (6) v1.1 note 1 item 3; (7) SYS-LIM under B-repaired; (8) inferred orbit masses and c2~0.100448/c3~0.199056 (now package-computed from exact law); (9) DERIVATION PREMISE vs IMPLEMENTATION labels (stop kept).
Corrected: (10) D1 residual/SYS-PC local map (E38-2); (11) full-column-rank premises, "for every resolved design" withdrawn (E38-3); (12) D3 wording; (13) SYS-PC global cancellation check (E38-4); (14) SYS-LIM first-order/exact failure/no impossibility/D7 diagnostic/exact midpoint; (15) SYS-FK alternatives (E38-10); (16) P0 (E38-5); (17) extended B3 (E38-6); (18) masks and identity domains C5.3, C7.0 (E38-7, -8); (19) system-level normalization (E38-11).
Fixed: (20) tolerances Q9; (21) HEADROOM thresholds Q4/E38-12; (22) draw reuse Q10; (23) sizes Q12; (24) SYS-O6 Q13; (25) midpoint Q14; (26) rank lapse Q15/E38-12; (27) autonomy Q17; (28) B1 extension Q3/E38-8; (29) caps E38-14. Added: (30) accounting table S8 (E38-13); (31) claim ceiling E38-15 + #38 L202 sentence (C1, C10).

0. Sources, hashes and precedence [condensed]
Governing raw files: #38 87fd77e0 (governs over everything, including this file and any summary of #38), #37 ce010fdb (below #38), #36 c8342d5a (inherited oracle definitions). Superseded: v1.1 97165ac6, v1.1 NOTE_1 00ec1902 (item 3 withdrawn). Inherited: governing set 6a5e0f24, B2/B3 ruling 6d75918f, v1_4_N closure note 4ad1d217 (B1, 595 s, N-b), v1_4_N 3f0c5c12, v1_3_E36 f6263fb8, oracle v1.1 e40c288f, results review 617e983d (M-1). PR #13 scratch @14376f38 read only.
Precedence (proposed for freeze).
1. Astra #38 raw text.
2. Astra #37 raw text, where #38 does not revise it.
3. E36 raw text.
4. This record.
5. The oracle governing set. It supplies every inherited definition that this record does not replace.

A summary of #38 that departs from the raw text, including the Specialist's, has no standing; see S12.3.

Development-informed disclosure.
- #37 L162: "This is development-informed work: O7 and its cancellation are already known. New freezing does not make them unseen."
- Q, Q2 and the directions are reused per #38 Q10, and that reuse is likewise development-informed.

## 1. Claim ceiling (C1)

[E38-15 verbatim here - your text.]
- C1.1 Synthetic-only. The package concerns declared synthetic systems only.
- C1.2 No checkpoint. No checkpoint or weight file is opened (E37-9, E38-16).
- C1.3 Q-tags. None of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY is answered, and the four stay separate. The package's only forward role is to inform whether a later, separately frozen Q-CAUSE measurement specification is warranted (#37 L164). That is a decision input, not a Q-CAUSE result.
- C1.4 Neural ceiling. E37-10 (S2) plus the #38 L202 sentence, which must be retained explicitly:

  > "Failure of the declared class-conditioned criterion does not exclude orbit-dependent covariance codes, including codes whose local coordinate relation differs on held-out orbits."

- C1.5 No consciousness, C4, C5, autopoiesis/"autopoietic", life/"alive" claim is made or implied.

2. Astra #37 items: compliance map (kept from v1.1) [condensed: E37 quotes dropped; checked as exact substrings of #37 raw]
E37-1..E37-10 requirement -> clause map is unchanged from v1.1 (which you reviewed in #38), with clause numbers updated: E37-1 -> C1.2, C10.3; E37-2 -> C9.4, C5.5; E37-3 -> C5.4, C10.2; E37-4 -> C10.1, C1.2; E37-5 -> C3.1, C3.2, C3.5, C3.7 (note: E38-1's plain separately fitted per-class maps satisfy E37-5 literally; v1.1's B-repaired departure withdrawn); E37-6 -> C4.2 (SYS-PC, D1-D3 UNVERIFIED, first-order per E38-2; class dependence from the system's own readout sign(psi1 psi2)), C4.3 (SYS-FK); E37-7 -> C4.4, C6 (no gain-must-vanish criterion for SYS-NC1-NC3 or SYS-LIM; no floor, no augmented basis); E37-8 -> C3.6(a)-(e), C3.8; E37-9 -> C9.1, C1.1, C9.2, C1.2, C9.3, S0, C9.5 (every TO BE FIXED BEFORE FREEZE item fixed in a frozen file before any execution); E37-10 -> C1, C10.4 (verbatim neural ceiling with the #38 L202 sentence).

2b. Astra #38 items: compliance map [condensed: E38-1..16 quotes dropped (your text; exact substrings of raw sha 87fd77e0..ca2a5, re-checked in S12). Each requirement -> clause row is kept verbatim.]
E38-1 [L308]: descriptive-only confound treatment -> C6; separately fitted plain full (3x8) and fixed-kappa ([A;0], A 2x8) maps in each of four flip classes -> C3.2 (with effective basis stated, Q2d); whole-orbit outer holdout -> C3.1 (six directed 2+2 folds, inherited); no augmented basis, shared-e, tied-bilinear fit or empirical neural floor -> C3.2, C6; change log 1-5; all seven systems included -> C4.1-C4.5; S8 accounting;
E38-2 [L312]: chart increment S_g C delta exact on non-crossing SYS-PC edits -> C4.2(c); J_a delta is the first-order forecast response -> C4.2(c), C4.2(d); exact finite discrepancies by propagating actual and predicted perturbed charts through Phi -> C4.2(d), C5.6, S8 (5 propagations per edit); SYS-LIM Jacobian loss-scaling formulas first-order only -> C4.5 D6/D7;
E38-3 [L316]: recovery / held-out identities require full-column-rank premises -> C3.3(b), C4.1, C4.2(e), C4.3, C4.4 (D5); resolved lower-rank min-norm fit does not inherit identities -> C3.3(b); applies to all systems -> C3.3(b) premise table; missing premise = EXPECTATION NOT APPLICABLE (RANK), not identity failure -> C7.1 item 7;
E38-4 [L320]: SYS-PC global checked via fitted full and reduced matrices -> C4.2(g)(i)-(ii); equality of resulting finite predictions -> C4.2(g)(iii); equality of losses (as consequence, per cell) -> C4.2(g)(iv), C5.5; fold and edit-size resolution retained for all identity checks -> C5.3(d), C7.0;
E38-5 [L324]: exact rational history probabilities for probability invariance -> C4.0(ii); #38 tolerances for L, G, cancellation -> C4.0, C5.5; P0 on true chart, SYS-FK and admissible SYS-NC1 -> C4.0 (charts); failed applicable P0 check stops the package -> C4.0, C7.1 item 1;
E38-6 [L328]: rank-two guard justified by common right factor D_muQ2^T -> C3.11; stacking convention frozen explicitly -> C3.11(b); not generalized to neural systems -> C3.11(e), C10.6; explicit handling of zero matrices and rank bands -> C3.11(c)-(d);
E38-7 [L340]: common masks govern comparative losses -> C5.3(a); exact-control identity not hidden by another predictor's invalidity -> C5.3(c); matrix identities checked before evaluation masking -> C5.3(b); finite recovery on actual-valid non-crossing edits where premise applies -> C5.3(c); predicted-belief guard failures are coverage exclusions unless contradicting an exact-recovery identity -> C5.3(c)-(d);
E38-8 [L344]: unavailable/unresolved required map prevents pooling of that comparison -> C3.9, C7.1 item 4; all admissibility, rank and coverage flags stored even under a higher-priority label -> C7.0; no zero-map substitution, no silent dropping, no subset pooling -> C3.9, C7.0;
E38-9 [L348]: SYS-LIM reported only -> C4.5, C7.1 item 8, C7.2; midpoint from exact-law A and D magnitudes -> C4.5 (exact rational t); no additional split -> C4.5; negative result limited to declared map families; no impossibility for transport-rule predictors -> C4.5 'Limit exposed', C10.7;
E38-10 [L352]: SYS-FK globally zero-kappa on product-chart designs -> C4.3; does not test true-chart designs -> C4.3 (report sentence); intervention-fixed autonomous controls possible but out of scope -> C4.3 'Alternatives'; no impossibility claim -> C4.3; change log 15;
E38-11 [L356]: normalization, weights, draws, coefficient rules fixed before execution -> C3.12, C4.4.R, C5.2, C9.5; system-level normalization, not per fold -> C3.12; c2, c3 from exact-law prefix probabilities via frozen RMS rule -> C4.4.R; equal gradient RMS != equal response, conditioning or transferability -> C4.4.R, C10.8;
E38-12 [L360]: VALIDATION requires every required control identity and its rank premise -> C7.2; rank-lapsed required SYS-PC class cell gives NOT MET (RANK) -> C7.2; headroom only after validation; H = L_mu,class -> C7.3; thresholds synthetic conventions; no neural floor -> C7.3, C10.5;
E38-13 [L364]: stage order -> C8.1; baseline-cache policy -> C8.2; identity-check domains -> C5.3, C8.3 (identity rows); exact scheduled edit counts; maximum propagation counts -> C8.3; accounting for voided, unresolved, invalid, prematurely stopped work -> C8.4; setup, diagnostics, serialization, reporting in workload/resource accounting -> C8.3, C8.5; outcome-dependent omissions not unexplained mismatches -> C8.4 (closure identity);
E38-14 [L376]: 1 CPU, no GPU, RLIMIT_AS 4,000,000,000 bytes -> C8.5; 600 s cumulative from before imports incl. setup/reporting -> C8.5; operational stop 540 s; declared reserve; hard termination <= 595 s -> C8.5; no retries, substitutions, post-result tolerance changes -> C8.5, C9.5; cap-limited work incomplete, not a scientific negative -> C7.1 (cap labels), C10.1;
E38-15 [L380]: ceiling text -> C1 (verbatim), C10.4;
E38-16 [L384]: revised scope before freeze; no new outputs inspected -> this file; S12; no checkpoint, no execution before review, application and seal -> C9.2, status line;

Other binding #38 body text [condensed]: the record quotes verbatim 43 excerpts of your raw text, at L5, 38, 46, 57, 69, 71, 73, 83, 94, 96, 118, 120, 124, 134, 138, 154, 156, 158, 160, 164, 183, 184, 186, 190, 192, 194, 196, 198, 204, 208, 210, 221, 223, 225, 227, 249, 251, 296, 298, 300, 302, 336, 372, and states "These lines carry rulings outside E38-1..16, and they bind as written." It also tabulates your Q1-Q17 rulings verbatim (L255-276); see S11 for where each is applied.

## 3. Design: classes, fits, stored terms, rank, pooling

C3.1 Orbits, folds and class labels (inherited, unchanged).
- Orbits and folds. These come from v1.1 oracle S2 L48-49 and geometry.py:7-22.
- Orbits: A{0,5,10,15}, B{1,4,11,14}, C{2,7,8,13}, D{3,6,9,12}.
- Six directed whole-orbit 2+2 folds (E38-1 "whole-orbit outer holdout"): AB->CD, CD->AB, AC->BD, BD->AC, AD->BC, BC->AD.
- Representatives: A->0, B->1, C->2, D->3.
- Flip masks. Defined at stages.py:208.
- Mask 5 = flip-X (mu_x->-mu_x, kappa->-kappa).
- Mask 10 = flip-Y (mu_y->-mu_y, kappa->-kappa).
- Mask 15 = flip-XY (kappa unchanged).
- Class label. g(a) = a XOR rep(orbit(a)), read as one of I, X, Y, XY:

| Class | A | B | C | D |
| I (mask 0) | 0 | 1 | 2 | 3 |
| X (mask 5) | 5 | 4 | 7 | 6 |
| Y (mask 10) | 10 | 11 | 8 | 9 |
| XY (mask 15) | 15 | 14 | 13 | 12 |

- Representative signs. All four representatives have mu_x > 0 and mu_y > 0, so here the class coincides with the sign quadrant. Write chi(g) = s_x*s_y (I +1, X -1, Y -1, XY +1). Then kappa_a = chi(g(a))*kappa_rep(orbit(a)).
- Per fold: 2 fitting prefixes and 2 evaluation prefixes per class (#37 L107).

C3.2 Selected class-conditioned model (E38-1; #38 L140-156, verbatim).

text
For each system, fold f and class g:

Full:
    Delta theta_hat = B_(f,g) delta
    B_(f,g) is an unrestricted 3 x 8 matrix.

Fixed-kappa:
    Delta theta_hat = [A_(f,g) delta; 0]
    A_(f,g) is an unrestricted 2 x 8 matrix.

- Objective. E36-3 weighted least squares on all output components, with w(a,u) = P_h(a,u) over all 16 continuations, on fitting prefixes only:

  min sum_{ainfit(f) intersect g} sum_u w(a,u)||L_a(u)X - J_a(u)||^2

  Here J_a(u) is the system's local response map and L_a(u) = dPhi/dtheta at the system's own baseline chart. The fixed-kappa fit uses the first two columns of L_a(u).
- Separate fitting. Each class is fitted separately: 4 classes x 2 maps per fold.
- Global comparator. One pair (B_f, A_f) per fold, fitted on all 8 fitting prefixes (#38 L154).
- Effective basis, stated explicitly (Q2d).
- Full map: the 24 free coefficients of B_(f,g), constant across the class's prefixes.
- Fixed-kappa map: the 16 free coefficients of A_(f,g), with kappa row identically 0.
- No augmentation. There are no mu_x, mu_y, polynomial or shared-e terms, no coupling across classes and no tied-bilinear form (#38 L156; Q2c).
- Application. A class map is applied unchanged to the class-g prefixes of the evaluation orbits (#37 L105). The same maps serve ALL, MARG and XOR reporting.

C3.3 Solver, rank and rank premises.
- (a) Solver and rank bands (inherited, unchanged).
- One SVD of the sqrtw-weighted design.
- sigma_i/sigma_1 > 10^-6 is resolved. sigma_i/sigma_1 < 10^-1^0 is resolved zero. The band [10^-1^0, 10^-6] is UNRESOLVED (E36-8). sigma_1 = 0 means rank 0 and a zero fit.
- Minimum-norm fit with rcond = 1e-10.
- B2: a resolved lower-rank design is fitted minimum-norm and scored. The inherited rank bands are retained per #38 L302.
- (b) Rank premises (E38-3). A coefficient-recovery or held-out-prediction identity applies only when its design has resolved full column rank (3 for full maps, 2 for fixed-kappa maps). A resolved lower-rank minimum-norm fit is still scored and reported, but no identity is asserted for it. It reads EXPECTATION NOT APPLICABLE (RANK), not an identity failure (#38 L71-73).

| Identity | System(s) | Required premise |
| B = DQ^T, global and class; finite recovery | SYS-O6 | full design rank 3 in that cell |
| D1 global (B = [c_x;c_y;0], A = [c_x;c_y]) | SYS-PC | global full rank 3 and global mu design rank 2 (invertible normal matrices, #38 L31) |
| D2 class (B = S_gC); finite recovery | SYS-PC | class full rank 3 |
| D4 (B = [C_mu;0], A = C_mu) | SYS-FK | full rank 3 for B; mu design rank 2 for A |
| D5 (full exact) | SYS-NC2 | full rank 3 |
| D7 (diagnostic only) | SYS-LIM | class full rank 3 in CD/BD/BC folds |

- Analytic support (#38 L75-83). Each valid baseline's exact 3-column L has full rank. That supports the exact-rank premises but does not establish numerical rank under the thresholds. Numerical ranks are prospective and are not predicted here.

C3.4 Global comparator. For every system, the global pair per fold is fitted with the same solver. It is a fixed descriptive comparator (#37 L116), except for the identities of C4.

C3.5 Freeze-before-scoring order. For every system:
1. Compute every global and class fit from fitting prefixes only.
2. Write the fits with their stored terms to outputs/fit_freeze_<system>.json and fsync.
3. Only then propagate any evaluation edit. No fit is recomputed after evaluation begins (stage order C8.1).

C3.6 Stored outputs (E37-8). Arrays are float64 C-contiguous little-endian, each with name, shape, <f8 and raw-byte sha256.
- (a) Matrices. Every B and A, global and class, for every system and fold, stored in full.
- (b) Rank reports. For every fit design and every extended-B3 stack (C3.11): full sigma list, sigma_1, ratios, numerical rank, unresolved flag and n_inverted.
- (c) Losses. L_mu, L_full, S and gain per (system, fit type, fold, class, evaluation orbit, group, eps_syn), weighted and unweighted, with scoreable counts and law mass.
- (d) Normal-equation terms.
- Per prefix: G_a (3x3) and r_a (3x8).
- Per (fold, class) and per fold: sumG and sumr.
- Their mumu block (2x2) and mu rows (2x8).
- (e) Cancellation diagnostics (#37 L35-62).
- Per (system, orbit): sum G_a[kappa,mu_x], sum G_a[kappa,mu_y] and sum G_a[mu_x,mu_y].
- For SYS-NC1-NC3: sum G_a[kappa,kappa]*Dg(mu_a).
- The P0 residuals of C4.0.
- Tolerances per C5.5. These are reported diagnostics, except where C4 makes them identities.

C3.7 Disclosure (E37-5; #37 L118-120).
- The class label is supplied by the analyst from the prefix index.
- Class models have 4x the parameters of the global model (4x24 full, 4x16 fixed-kappa, against 24 and 16).
- Success would not show that any neural system contains or consults the label.

C3.8 Diagnostics only (E37-8).
- kappa-row norms of every map.
- Optional single-prefix local fits, which abandon the held-out claim (#37 L113).
- Neither enters any outcome.

C3.9 Voiding, unresolved cells and pooling suppression (E38-8; Q3).
- Voiding. Systems whose baseline is not the true chart (SYS-FK, SYS-NC1-NC3) inherit N4(ii) per-prefix voiding. SYS-NC1-NC3 also inherit the >=5-of-16 RESTRICTED COMPARATOR NOT ADMISSIBLE rule.
- Empty class. A class with 0 non-voided fitting prefixes in a fold is a rank-UNRESOLVED class cell.
- B1 extension (confirmed, Q3). Any unavailable or unresolved map required by a common-mask comparison prevents pooling of that comparison (REFERENCE RANK UNRESOLVED).
- No missing map is replaced by a zero map.
- No unresolved cell is silently dropped.
- No pooled statistic is formed from a subset of resolved classes.
- The cell-level losses that can be formed are still stored.

C3.10 Pooling (E36-5, inherited).
- Occurrences are pooled with their original w(a,u) and equal direction and sign weights, normalized once over the pooled scoreable occurrences.
- The class statistic pools over all 6 folds x 4 classes.
- H, S and their ratio use identical masks and weights.

C3.11 Extended B3 rank-two guard (E38-6; #38 L330-336).
- (a) Justification. For SYS-FK and SYS-NC1-NC3, J_a(u) = A_a(u)*C_mu with C_mu = D_muQ2^T, the same prefix-independent 2x8 right factor at every prefix. So any row stack of J matrices has rank <= 2.
- (b) Stacking convention (frozen).
- For each such system, a stack is formed per fold, over the non-voided fitting prefixes.
- Rows are ordered (prefix ascending, continuation u = 0..15, output component X, Y, XOR), giving (n_fit*48) x 8.
- A further stack is formed per (fold, class) the same way.
- The stack is unweighted: J itself, not sqrtw*J. Rank of J is weight-independent when all w > 0, and every P_h(a,u) is positive (O1 exact rationals).
- Count: 4 systems x (6 + 24) = 120 stacks.
- (c) Zero matrix. If sigma_1 = 0, the stack has rank 0. This is recorded, with no stop.
- (d) Bands.
- sigma3/sigma1 > 10^-6 is a resolved third direction: INTEGRITY STOP (exit 7), PIPELINE INVALID.
- sigma3/sigma1 in [10^-1^0, 10^-6] is recorded as UNRESOLVED-B3, with no stop. This is not a resolved third direction under the inherited bands.
- sigma3/sigma1 < 10^-1^0 passes.
- (e) Scope. The guard is not generalized to two-coordinate neural systems with prefix-dependent marginal-state Jacobians (C10.6).

C3.12 Normalization and fixed rules (E38-11).
- Every synthetic normalization (psi_bar, D_psi for SYS-PC/SYS-LIM/SYS-O6; mu_bar, D_mu for SYS-FK/SYS-NC1-NC3) is computed once per system over all 16 prefixes with exact-law P_a from O1, as in _embed, stages.py:323-329.
- Normalization is never recomputed per fold.
- Weights, draws (C5.2) and coefficient rules (C4.4.R) are fixed in the frozen file before execution.

## 4. Systems and derived expectations

Notation.
- theta = (mu_x, mu_y, kappa) and Phi(theta,u) is the forecast.
- Output flip actions P_X = diag(-1,1,-1) and P_Y = diag(1,-1,-1).
- R_X = diag(-1,1,-1), R_Y = diag(1,-1,-1), R_XY = diag(-1,-1,1).
- Premise P0. L_{g*a}(g*u) = P_g L_a(u) R_g and w(g*a,g*u) = w(a,u). Hence G_{g*a} = R_g G_a R_g. P0 alone does not give D1 or D6. It must be combined with the specified state map, weights, complete fitting orbits and rank conditions (Q11).

C4.0 P0 step-0 fixture (E38-5).
- When. After O1 and O2, before any fit (C8.1 stage S3).
- Charts checked.
- The true chart (designs shared by SYS-O6, SYS-PC, SYS-LIM).
- The SYS-FK product chart.
- The SYS-NC1 chart if SYS-NC1 is admissible (C4.4).
- Not SYS-NC2 or SYS-NC3, which break the symmetry by design.
- Checks, for every prefix a, flip g in {X, Y, XY} and continuation u:
- (i) L comparison: ||L_{g*a}(g*u) - P_g L_a(u) R_g||_max <= 1e-12 + 1e-10*max(||*||_max, ||*||_max) (#38 L284-286).
- (ii) Probability invariance: P_h(g*a, g*u) = P_h(a,u) as exact rationals from O1 (#38 L300). These are exact equalities, not byte equality of float sums.
- (iii) G comparison: ||G_{g*a} - R_g G_a R_g||_max under the same formula as (i).
- Failure. A failed applicable P0 check stops the package: PIPELINE INVALID (P0), exit 7, no fit, no rerun. The report gives an operational failure diagnosis only, not a conclusive attribution to derivation or implementation (Q5).

C4.1 SYS-O6: existing affine exact-filter control.
- Construction. State, readout, embedding (Q, seed 35006) and edits exactly as in O6 (oracle v1.1 L83-91).
- Inclusion (Q13). Including it is allowed. It does not reopen, replace or retry the completed oracle package.
- Identities (E38-3).
- Each global and class B equals DQ^T within 1e-9 max abs, in every cell with resolved full rank 3.
- In those cells, Pred_full matches actual within 1e-9 on actual-valid edits (C5.3(c)).
- A cell without the premise reads EXPECTATION NOT APPLICABLE (RANK).
- Comparator (descriptive). A_(f,g) = C_mu + (sumG_mumu)^-1(sumG_mukappa)c_kappa over the class's fitting prefixes. The adjustment to C_mu is generally nonzero within a class, so the class comparator loss may differ from the O6 global value (UNVERIFIED).

C4.2 SYS-PC: sign-dependent positive control.
- (a) State. psi = (mu_x, mu_y, tau) with tau = sign(mu_xmu_y)*kappa. tau is flip-invariant, so it is constant within an orbit. z = Q*D_psi^-1(psi - psi_bar), with Q from seed 35006 (reused, Q10) and system-level normalization (C3.12).
- (b) Readout (autonomous; Q8 confirmed). psi = D_psiQ^Tz + psi_bar, then theta = (psi1, psi2, sign(psi1psi2)*psi3). The marginal coordinates carry the signs used by the readout. The baseline chart is the true theta_a, so L, the weights and the designs are identical to SYS-O6's.
- (c) Local map (E38-2). C = D_psiQ^T with rows c_x, c_y, c_tau, and S_a = diag(1,1,chi_a).
- On a non-crossing edit the chart increment S_g C delta is exact: theta' = theta_a + S_g C delta.
- J_a delta = L_a S_g C delta is the first-order forecast response.
- (d) D1, global fit (UNVERIFIED; #38 L13-38) [condensed]. With P0, sum_g G_{g.r} = 4 diag(G_r[xx], G_r[yy], G_r[kk]) and sum_g G_{g.r} S_g = 4 diag(G_r[xx], G_r[yy], 0). For fit sets that are unions of complete orbits, given the C3.3(b) rank premise: B_global = [c_x; c_y; 0] and A_global = [c_x; c_y]; the two predicted perturbed charts are equal, so their finite forecast predictions are equal wherever propagation is defined. Residual: the exact finite discrepancy is Phi(theta_a + S_gC delta, u) - Phi(theta_a + B_global delta, u), computed by propagation (C5.6); L_a[:,kappa] chi_a c_tau delta is only its first-order approximation (#38 L40-57).
- (e) D2, class fit (UNVERIFIED; #38 L61-73).
- Within class g, J_a = L_a S_g C. If the stacked class full design has resolved full column rank 3, least squares uniquely recovers B_(f,g) = S_g C, and finite prediction is exact on valid non-crossing edits.
- Otherwise the cell reads EXPECTATION NOT APPLICABLE (RANK), and for VALIDATION that is NOT MET (RANK) (C7.2).
- D3. A_(f,g) = C_mu + chi_g(sumG_mumu)^-1(sumG_mukappa)c_tau. The adjustment to C_mu is generally nonzero (#38 L96).
- When the full predictor is exact on the evaluated edits, L_full = 0, so class gain = L_mu,class >= 0 (#38 L85-94). The non-negativity follows from exactness, not from nesting.
- The magnitude of L_mu,class is not derived. No equality with O6's R follows.
- (f) Sign boundaries and crossing rule.
- The boundaries are psi1 = 0 and psi2 = 0.
- An edit crosses if sign(psi'_i) != sign(psi_{a,i}) or psi'_i = 0 for i in {1,2}.
- A crossing edit is not scoreable for any SYS-PC model. It enters the common mask, is counted and is never replaced.
- Bound (#38 L229-247 confirmed). |Deltapsi_i| = eps_syn*sd_i*|q_i^Tv| <= eps_syn*sd_i.
- With the displayed (rounded) sd_x = 0.36806 and sd_y = 0.61364, the bounds at eps_syn = 0.25 are 0.0920 and 0.1534.
- The corresponding margins are min|mu_x| = 0.2501 and min|mu_y| = 0.4276.
- Full precision governs (#38 L249). The package computes D_psi under C3.12 and the bound from it at step S4, before any edit. The displayed numbers explain the bound and do not govern it.
- An observed crossing under these premises is an integrity failure (exit 7), with no replacement edit (#38 L251).
- (g) Global identity checks (E38-4). In every fold, and where stated in every (group, eps_syn) cell:
- (i) ||B_global - [c_x;c_y;0]||_max <= 1e-9.
- (ii) ||A_global - [c_x;c_y]||_max <= 1e-9.
- (iii) max|Pred_full - Pred_mu| <= 1e-9 on the required valid edits.
- (iv) |L_mu - L_full| <= 1e-18 + 1e-9*S per (fold, group, size) cell. This is reported as a consequence and is never the sole definition.
- All four pass: GLOBAL CANCELLATION AS DERIVED.
- (h) Class identity checks. In every (fold, class) cell with the premise:
- ||B_(f,g) - S_gC||_max <= 1e-9.
- max|Pred_full - actual| <= 1e-9 on actual-valid non-crossing edits.
- All pass: CLASS RECOVERY AS DERIVED.

C4.3 SYS-FK: globally zero-kappa control on product-chart designs (E38-10).
- State. z = Q2*D_mu^-1(mu - mu_bar), Q2 from seed 35007 (reused, Q10).
- Readout. theta = (mu_x, mu_y, 0). The baseline chart is (mu_a, 0). Disagreement with the true reachable forecasts is reported separately.
- Validity (RD arithmetic; UNVERIFIED). The minimum baseline product-belief p is ~ 0.0317, and >= 0.0074 under the edit bound at eps_syn = 0.25. Both are above 10^-6. The package recomputes this.
- D4 (UNVERIFIED; E38-3). J_a = L_a[:,mu]*C_mu.
- If the design has resolved full column rank, B = [C_mu; 0], and A = C_mu when the mu design has rank 2.
- Pred_full = Pred_mu = actual, so L_full = L_mu = 0, gain 0 and S > 0.
- v1.1's "for every resolved design" is withdrawn (#38 L73).
- Checks (per cell with premise).
- B and A recovery <= 1e-9.
- max|Pred_full - actual| and max|Pred_mu - actual| <= 1e-9 on actual-valid edits.
- Zero gain per (fold[, class], group, size) cell: |L_mu - L_full| <= 1e-18 + 1e-9*S.
- All pass: FIXED-kappa IDENTITY AS DERIVED.
- Scope statement (report verbatim): "FK checks the kappa row on the product-chart designs, not on the SYS-O6/SYS-PC designs." FK's design ranks are reported next to SYS-O6/SYS-PC's.
- Alternatives (corrected per E38-10, #38 L206-227) [condensed]. A globally constant kappa cannot reproduce true baselines with different kappa values, but autonomous same-baseline controls with kappa fixed under the declared interventions can exist (e.g. a frozen register r initialized to kappa_a and unchanged by edits, #38 L214-221: an intervention-fixed control), and a two-coordinate plateau construction is not excluded (#38 L225). Both are outside this package and are not added. No impossibility of same-baseline autonomous controls is claimed.
C4.4 SYS-NC1-NC3: descriptive two-coordinate confounds (E37-7; #38 L160, L186). Not negative controls.
- Construction. z = Q2*D_mu^-1(mu - mu_bar) with chart (mu_x, mu_y, g_k(mu)).
- Derivatives and finite predictions are taken about the system's own baseline.
- Validity is checked per prefix, with N4(ii) voiding.
- No refit after inspection and no replacement.
- Extended B3 per C3.11.
- SYS-NC1 = O7 lookup: a varying-kappa two-coordinate confound (#38 L160). Its g is the O7 P-weighted quadratic fit recomputed in-package. Committed stage_O7.json g_coefficients: g ~ 0.1404*mu_xmu_y.
- Global. Pred_full == Pred_mu is expected only if 0 prefixes are voided. Reported with the zero-gain formula, as a descriptive identity, not a validation item.
- Class. A gain of either sign is permitted and reported.
- SYS-NC2. g2 = c2mu_x, an affine symmetry-breaking confound.
- D5 (UNVERIFIED). Dg2 is constant, so the full model is exact when the design has resolved full column rank (E38-3). Gain = L_mu >= 0 under the exactness premise.
- Reported. It is not evidence of a covariance register.
- SYS-NC3. g3 = c3mu_x^3, a cubic confound (Q7 accepted). No gain expectation; reported.
- Comparison caveat (#38 L186). NC2 and NC3 differ in baselines and derivatives, so the pair is not a comparison in which only functional form changes. Equal gradient RMS does not imply equal forecast response, conditioning or transferability (E38-11).

C4.4.R RMS-matching rule (Q7 accepted; E38-11).
- Rule. rho(g) = sqrt(sum_a P_a||Dg(mu_a)||^2), with P_a the exact-law prefix probabilities from O1 and mu_a the exact stage-4 marginals.
- rho_NC1 is computed from SYS-NC1's g.
- The in-package O7 refit must equal the committed g_coefficients within the C3.6(e)-type tolerance (#38 L284-286). Otherwise INTEGRITY STOP.
- c2 = rho_NC1. c3 = rho_NC1 / (3*sqrt(sum_a P_a mu_{x,a}^4)). Both are unique and positive, because every |mu_x| >= 0.2501.
- Values: c2 = TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW; c3 = TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW. [condensed] Computed at stage S4 before any fit, recorded, never changed (Q7). Earlier values from probabilities reconstructed from rounded SDs are withdrawn. The record does not compute exact-law values: stage_O1.json stores the exact stage-4 charts but not P_h or P_a, so exact-law P_a needs the O1 filter run, excluded here. Frozen arithmetic: P_a = sum_u P_h(a,u) as an exact rational sum, converted once to float64; rho, c2, c3 computed in float64 and recorded at full precision. (NOTE_1 N3 adds the sum P_a = 1 exact assertion and c2 = rho_NC1/sqrt(sum P_a).)
- Admissibility. If any matched baseline is invalid (p < 10^-6), the system is RESTRICTED COMPARATOR NOT ADMISSIBLE, with no rescaling. Admissibility is not predicted here.

C4.5 SYS-LIM: orbit-indexed limit control, REPORTED ONLY (E38-9; Q14, Q15, Q17).
- Purpose. It exposes a limitation of the selected constant-per-class maps (#38 L192).
- Midpoint (exact law). t = (|mu_x|_A + |mu_x|_D)/2 from the exact stage4_chart_exact rationals:
- |mu_x|_A = 2640740184/4981285969 (~ 0.530132);
- |mu_x|_D = 867714984/3134384719 (~ 0.276837);
- t = 6299716077234553896/15613266622202707711 (~ 0.403484820292257; RD arithmetic, exact rational from committed data).
- The package recomputes t from O1 and compares exactly.
- s_A = +1, s_B = s_C = s_D = -1. The margin is ~ 0.126647. No additional split (Q14).
- State and readout. psi = (mu_x, mu_y, s(|mu_x|)*kappa), z = Q*D_psi^-1(psi - psi_bar), system-level normalization. The readout reads the threshold from the state's own |psi1|, which is autonomous (Q17, #38 L204). The baseline is the true chart.
- Crossing bound (#38 L239-245 confirmed). ||psi'1| - |psi1|| <= |Delta psi1| <= eps_syn*sd_x. With the displayed sd_x = 0.36806: eps 0.02 -> 0.00736; 0.05 -> 0.01840; 0.10 -> 0.03681; 0.25 -> 0.09201. All are below the margin 0.126647. The full-precision bound is computed by the package (#38 L249). An observed crossing is an integrity failure.
- D6 global (UNVERIFIED; uses P0).
- lambda = (s1K1 + s2K2)/(K1 + K2), where K_o = sum_{aino} G_a[kappakappa]. B = [c_x; c_y; lambdac_tau] and A = [c_x; c_y].
- CD/BD/BC fitting folds. lambda = -1, so the held-out A gets the wrong sign. The first-order loss on A is L_full ~ 4*E_A against L_mu ~ E_A.
- A-containing folds. lambda = (K_A - K_X)/(K_A + K_X). The first-order ratio is L_full/L_mu ~ (1+lambda)^2, and (1+lambda)^2 < 1 iff K_A < K_X.
- These loss-scaling statements are Jacobian-level only and are not asserted at finite eps_syn (E38-2, #38 L118-120). Reported with no sign expectation.
- D7 class (diagnostic). In the CD, BD and BC fitting folds, full-rank recovery gives B_(f,g) = diag(1,1,-1)*C, the negative-sign chart map. It is wrong on held-out A whenever the edit has a nonzero relevant component (#38 L194).
- D7 is reported as an analytic diagnostic.
- A failure of an exact, applicable D7 identity is flagged D7 INVESTIGATE (#38 L198). It is not a VALIDATION item and not a stop.
- Limit exposed (E38-9). The negative result concerns the specified global and flip-class map families. It does not establish impossibility for predictors given a different declared transport rule: a rule using the state's magnitude could represent this system (#38 L196).

## 5. Units, edits, masks, weights, groups, tolerances

- C5.1 Units. All systems are synthetic. An edit is delta = eps_syn*sign*v in the 8-D synthetic state, with field eps_syn.
- C5.2 Edits and draws (Q10, Q12).
- Directions. The 16 unit directions of seed 35016 (the O6/O7 array), applied as +v then -v.
- Embeddings. Q (35006) and Q2 (35007) are reused with their generation conventions and hashes. The reuse is disclosed as development-informed.
- Sizes. eps_syn in {0.02, 0.05, 0.1, 0.25}, with 0.1 the sole headroom reference.
- Per system: 6 folds x 8 evaluation prefixes x 16 continuations x 32 signed directions x 4 sizes = 98,304 edits. Per fold per size that is 4,096.
- C5.3 Masks and identity domains (E38-7).
- (a) Common mask (comparative losses). An edit is scoreable for the comparison iff the actual perturbed belief and all four predicted perturbed beliefs (global full, global mu, class full, class mu) pass p >= 10^-6.
- For SYS-PC and SYS-LIM, the edit must also be non-crossing.
- The same mask governs L_mu, L_full and S for both fit types.
- Coverage is reported per fold, class and size.
- (b) Matrix identities (C4.1, C4.2(g)(i)-(ii), C4.2(h), C4.3) are checked on the fitted matrices before any evaluation masking.
- (c) Finite recovery identities are checked on actual-valid, non-crossing edits in cells where the exactness premise applies. They are not restricted to the common mask: invalidity of a different predictor does not hide an applicable exact-control identity.
- Applicable identities: SYS-O6 class/global Pred_full = actual; SYS-PC class Pred_full = actual; SYS-PC global Pred_full = Pred_mu; SYS-FK Pred_full = Pred_mu = actual.
- If a predictor covered by an applicable exact-recovery identity fails the p >= 10^-6 guard while the actual belief passes, that contradicts the identity. It is an identity failure, not a coverage exclusion.
- (d) Other predicted-belief guard failures are coverage exclusions. All identity checks keep their fold and eps_syn resolution, and gain identities keep their group resolution (E38-4).
- C5.4 Weights and groups.
- w(a,u) = P_h(a,u), with uniform direction, sign and size weights.
- The groups ALL, MARG and XOR are reported separately. Outcomes use ALL and MARG at eps_syn = 0.1.
- R-type ratios are worded per E37-3.
- C5.5 Tolerances (Q9; #38 L278-302, verbatim).

text
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

- Gain tolerance granularity (#38 L296). It applies within each required fold/group/size cell, using that cell's common-mask losses and S. Pooled equality cannot override a failing cell. The absolute difference and its scale are reported.
- For class fits, the required cell is fold/class/group/size. This is my proposal (Q-R2).
- These are prospective acceptance conventions, not certified forward-error bounds. They are not loosened if a poorly conditioned fit fails (#38 L298).
- Exact probabilities. Probability invariance uses O1's exact rationals (#38 L300).
- Inherited. The rank bands and the headroom BOUNDARY convention (relative 10^-6, v1_4_N L16) are retained (#38 L302).
- Exact-zero flags are reported separately from tolerance checks (E37-2).
- C5.6 Finite discrepancies (E38-2). Every loss uses finite forecasts: the actual perturbed chart and each predicted perturbed chart are each propagated through Phi (5 propagations per edit, S8). No first-order surrogate enters any loss.

## 6. Confound treatment: descriptive-only (selected; E38-1; #38 L136-186)

- Selection. The descriptive-only treatment is selected (#38 L5, L138).
- It applies to confound interpretation.
- The implementation identities and the separate SYS-PC headroom assessment remain.
- Confound systems. SYS-NC1-NC3 (and SYS-LIM) are fitted with the same plain maps as every other system and reported descriptively, with no gain-must-vanish criterion and no floor.
- A positive confound gain is "compatible with two-coordinate mediation" (E37-7).
- It does not identify a register and does not exclude two-coordinate mediation or reachable-set lookup (E38-15).
- What is not used. No measured confound ratio is carried forward as a hurdle, floor or calibration for any neural study (#38 L158).
- Withdrawn alternatives, each with its source:
- v1 Option B: Q2a, L164.
- B-repaired / shared e / D2': Q2b, L183. Astra accepts the D2' algebra as conditional mathematics only.
- Tied bilinear: Q2c.
- Option A floor: L158.
- Option C: L184.

## 7. Outcome labels and order

C7.0 Flag storage (E38-8). For every system, fit type, fold, class, group and size, the package stores:
- every admissibility, voiding, rank (with premise status) and coverage flag;
- the crossing counts;
- the identity residuals with their tolerances.

This holds even when a higher-priority display label applies.

C7.1 Per-statistic labels. Labels are formed per system, fit type and group (ALL, MARG) at eps_syn = 0.1. Other sizes are reported. Identity checks use every size. First match wins:
1. PIPELINE INVALID (operational failure diagnosis; Q5). Any of the following stops the package, with no rerun:
- an O1 or O2 fixture failure;
- an applicable P0 failure (C4.0);
- an applicable control-identity failure: SYS-O6 (C4.1), SYS-PC global (C4.2(g)) or class (C4.2(h)), SYS-FK (C4.3), in a cell whose premise holds;
- a resolved extended-B3 third direction (C3.11);
- an observed SYS-PC or SYS-LIM crossing;
- an SYS-NC1 refit mismatch;
- an integrity condition of C8.6.

   The diagnosis names the failed check. It does not conclusively attribute the failure to derivation or implementation.
2. CAP REACHED / CAP RESERVE REACHED (INCOMPLETE) / PROJECTION HALT (C8.5). This is incomplete work, not a scientific negative.
3. REFERENCE COVERAGE NOT MET. Count coverage < 75% (4*n_s < 3*n_t) or law-mass coverage < 0.75*(1 - 10^-6) in some fold, or for class statistics some foldxclass.
4. REFERENCE RANK UNRESOLVED. A required map is unresolved or unavailable (C3.9). No pooled statistic is formed.
5. RESTRICTED COMPARATOR NOT ADMISSIBLE (SYS-NC1-NC3): >=5 of 16 prefixes voided, or a matched baseline invalid.
6. ZERO RESPONSE. Pooled S = 0 exactly.
7. Identity statistics (SYS-O6; SYS-PC global and class; SYS-FK): IDENTITY AS DERIVED, or EXPECTATION NOT APPLICABLE (RANK) per cell lacking its premise (E38-3).
8. Reported statistics (SYS-NC1-NC3, SYS-LIM, and every global gain other than the SYS-PC/SYS-FK identities): REPORTED. Negative gains are kept (#38 L94). D7 INVESTIGATE flags, if any, are reported.

C7.2 VALIDATION (E38-12). CLASS-FIT VALIDATION MET iff:
- O1, O2 and every applicable P0 check passed;
- every required control identity holds and has its rank premise (SYS-O6 global and class; SYS-PC global, all four checks of C4.2(g); SYS-PC class; SYS-FK both fit types);
- no required cell is REFERENCE RANK UNRESOLVED.

Otherwise it reads CLASS-FIT VALIDATION NOT MET (<first failing reason>).
- A required SYS-PC class cell with EXPECTATION NOT APPLICABLE (RANK) gives NOT MET (RANK) (E38-12, Q15).
- For SYS-O6 and SYS-FK, a required cell lacking its premise likewise gives NOT MET (RANK). "every required control identity and its rank premise" (E38-12) applies to all controls.
- SYS-LIM, D7 and the confound systems never enter VALIDATION. VALIDATION does not depend on any gain magnitude.

C7.3 SYS-PC HEADROOM (E38-12; Q4).
- Formation. Formed only if VALIDATION is MET. Otherwise it reads NOT FORMED (VALIDATION NOT MET).
- Statistic. H = L_mu,class for SYS-PC at eps_syn = 0.1, with sqrtH and R = H/S, for ALL and MARG.
- Thresholds (synthetic reporting conventions only). ALL sqrtH >= 10^-3 and R >= 0.05; MARG sqrtH >= 10^-4 and R >= 0.02. Labels are HEADROOM NOT MET / BOUNDARY / MET under the inherited band rule.
- No prediction is made that SYS-PC will meet them.
- They supply no neural response floor (#37 L164).

C7.4 What the labels license. VALIDATION MET with SYS-PC HEADROOM MET licenses only a decision on whether a neural specification is warranted. SYS-LIM and the confound results go with any such decision as stated limits.

## 8. Execution specification and accounting (E38-13, E38-14)

The counts below are scheduled maxima derived from the frozen design. Each is a product of declared factors, with sources cited. None is measured. Outcome-dependent reductions (voids, unresolved maps, stops) are accounted for by C8.4 and never appear as unexplained mismatches. The workload and runtime remain UNVERIFIED (#38 L372).

C8.1 Stage order (frozen proposal).

| Stage | Content | Phi propagations (max) |
| S0 | Wrapper T0 before imports; preflight; manifest hash checks; runtime versions recorded as observations; RLIMIT_AS set | 0 |
| S1 | O1 exact fixtures (inherited): 16 prefix filters + 256 terminal forecasts, exact | 272 exact |
| S2 | O2 closed-form L vs finite-difference check (inherited) | 1,536 float |
| S3 | P0 fixture on true chart, SYS-FK chart and SYS-NC1 chart (if admissible), using closed-form L only (C4.0) | 0 |
| S4 | System construction for all 7 systems: system-level normalization; SYS-NC1 g refit and committed-coefficient check; c2, c3 from exact law; t from exact law; baseline validity, voiding and admissibility; L and J tables; crossing bounds at full precision | 0 |
| S5 | Fits for all systems (global and class, full and fixed-kappa); rank reports; extended-B3 stacks; normal-equation terms; matrix identities (C5.3(b)); write and fsync fit_freeze_<system>.json | 0 |
| S6 | Evaluation, systems in the fixed order SYS-O6, SYS-PC, SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3, SYS-LIM. Per system: 256 baseline propagations, then per edit 5 propagations. The first 1,000 S6 propagations are the timing sample | 3,442,432 |
| S7 | Finite identity checks, pooling, labels, flags (C7) | 0 |
| S8 | Serialization of stage files and results.json; report; wrapper post-run index | 0 |

S3 precedes S4 even though P0 on the SYS-NC1 chart needs SYS-NC1's admissibility. That sub-check therefore runs at the start of S4, immediately after SYS-NC1's admissibility is known and before any fit. A failure stops the package (E38-5).

C8.2 Cache policy (frozen proposal).
- L tables. One closed-form table of 256 L_a(u) per distinct baseline chart: true chart (shared by SYS-O6, SYS-PC, SYS-LIM and used by O2), SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3. That gives 5 tables, 1,280 L evaluations. P0 reads these tables and computes no new L.
- Baseline forecasts. Propagated per system (256 each, 1,792 total), with no cross-system sharing even where charts coincide. This matches E38's count (#38 L369). For true-chart systems, they are compared with O1's exact forecasts as a reported check.
- Predictions. No deduplication. Every scheduled actual and predicted propagation is attempted as scheduled, even where two predictions are expected to coincide (for example SYS-PC global full and mu). Deduplication would hide the very equality being checked.
- Fits. Not cached across systems. Each system's designs are formed from its own tables, even when identical to another system's (SYS-O6/SYS-PC/SYS-LIM), and stored.

C8.3 Accounting table (scheduled maxima).

Notation: F = 6 folds; K = 4 classes; E = 8 evaluation prefixes per fold (2 per class); U = 16 continuations; V = 16 directions x 2 signs = 32; Z = 4 sizes; N_sys = 7.

| Item | Formula | Count | Source |
| Edits per (fold, size) | E*U*V | 4,096 | stages.py:48 |
| Edits per (fold, class, size) | 2*U*V | 1,024 | C3.1 |
| Edits per system | F*E*U*V*Z | 98,304 | C5.2 |
| Edits, all systems | 7 x 98,304 | 688,128 | - |
| Propagations per edit | actual + global full + global mu + class full + class mu | 5 | C5.6 |
| Edit propagations per system | 98,304 x 5 | 491,520 | - |
| Baseline propagations per system | 16 prefixes x U | 256 | C8.2 |
| S6 propagations per system | 491,520 + 256 | 491,776 | - |
| S6 propagations, all systems | 7*(98,304*5 + 256) | 3,442,432 | #38 L369 |
| O2 float propagations | 16*16*3*2 | 1,536 | results.json:4 |
| Scheduled float propagations, package maximum | 3,442,432 + 1,536 | 3,443,968 | - |
| Exact propagations (O1) | 16 + 256 | 272 | pinned.py:11; results.json:70 |
| Additional diagnostic Phi propagations | none declared | 0 | C8.1 |
| Closed-form L evaluations | 5 charts x 256 | 1,280 | C8.2 |
| J evaluations | 7 x 256 | 1,792 | C3.2 |
| Validity-guard evaluations, edits | equal to edit propagations | 3,440,640 | C5.3 |
| Validity-guard evaluations, baselines | 7 x 16 | 112 | C3.9 |
| Weighted LS fits per system | F*(2 global + 2K class) | 60 | C3.2 |
| Weighted LS fits, all systems | 7 x 60 | 420 | - |
| SYS-NC1 g refit | 1 | 1 | C4.4.R |
| Extended-B3 stacks (SVD) | 4 systems x (F + F*K) | 120 | C3.11 |
| SVDs total | 420 + 1 + 120 | 541 | - |
| Stored fitted matrices | 7 x 60 | 420 | C3.6(a) |
| Stored G_a / r_a | 7 x 16 each | 112 / 112 | C3.6(d) |
| Stored normal-equation sums | 7 x 30 cells x {sumG, sumr, sumG_mumu, sumr_mu} | 840 | C3.6(d) |
| Rank reports | = SVDs | 541 | C3.6(b) |
| Orbit cancellation sums | 7 x 4 orbits x 3 scalars, plus 3 x 4 sum G[kappakappa]Dg vectors (NC1-NC3) | 84 scalars + 12 vectors | C3.6(e) |
| P0 L comparisons | <= 3 charts x 16 x 3 flips x U | <= 2,304 | C4.0 |
| P0 G comparisons | <= 3 x 16 x 3 | <= 144 | C4.0 |
| P0 exact probability comparisons | 16 x 3 x U (law-level, chart-independent) | 768 | C4.0 |
| Loss cells per system | global F*2 orbits*3 groups*Z + class F*K*2*3*Z | 144 + 576 = 720 | C3.6(c) |
| Loss cells, all systems | 7 x 720 | 5,040 | - |
| Pooled statistics per system | 2 fit types x 3 groups x Z | 24 | C3.10 |
| Coverage records per system | F*Z (global) + F*K*Z (class) | 24 + 96 = 120 | C5.3 |
| Identity cells, SYS-O6 | matrices 6 + 24; recovery F*Z + F*K*Z | 30 + 120 | C4.1 |
| Identity cells, SYS-PC global | matrices 12; Pred equality F*Z; loss F*3*Z | 12 + 24 + 72 | C4.2(g) |
| Identity cells, SYS-PC class | matrices 24; recovery F*K*Z | 24 + 96 | C4.2(h) |
| Identity cells, SYS-FK | matrices 60; recovery 2 predictors x (F*Z + F*K*Z); zero gain F*3*Z + F*K*3*Z | 60 + 240 + 360 | C4.3 |
| SYS-NC1 global descriptive identity | F*3*Z | 72 | C4.4 |
| D7 diagnostic matrices (SYS-LIM) | 3 folds x K | 12 | C4.5 |
| Stage files written | S0, S1, S2, S3, S4, 7 fit_freeze, 7 evaluation, results, report | 21 | C8.1 |

C8.4 Accounting for reduced or stopped work. For every (system, stage), the package records:

> scheduled = attempted + not-propagated(VOID) + not-propagated(UNRESOLVED) + not-reached(STOP)

Attempted propagations are further split into valid-finite, guard-invalid (stored null, counted), ValueError and non-finite, following the inherited policy that every edit is propagated and guard failures are counted.
- VOID. For each voided prefix (SYS-FK, SYS-NC1-NC3): its 16 baseline propagations are not made. If it is an evaluation prefix in a fold, that fold's edits on it are not propagated: 16*32*4 = 2,048 edits = 10,240 propagations per (fold, voided evaluation prefix). They stay in the coverage denominator.
- UNRESOLVED or unavailable map. That map's prediction is not propagated, which is one propagation per affected edit:
- per unresolved (fold, class) map: 1,024*4 = 4,096 edits, so 4,096 propagations;
- per unresolved global map: 4,096*4 = 16,384.

  The comparison is not pooled (C3.9).
- INVALID. A predicted or actual belief failing the guard is still attempted and counted (inherited). A scoreable-edit failure stops the package.
- STOP (cap, reserve, projection halt or integrity). The unreached count is recorded per stage. Partial outputs are kept and labelled INCOMPLETE.
- Closure check. If the identity fails for any (system, stage), or attempted float propagations exceed 3,443,968, the result is INTEGRITY STOP (exit 7).

C8.5 Caps (E38-14, verbatim in S2b).
- 1 CPU, no GPU, RLIMIT_AS 4,000,000,000 bytes.
- 600 s cumulative from before imports, including setup and reporting.
- Operational stop at 540 s, with the declared 60 s reserve. Hard termination at 595 s - (now - T0).
- Projection halt if the projected remaining time exceeds 540 s - T_elapsed.
- No automatic retries, parameter substitutions or post-result tolerance changes.
- Cap-limited work is incomplete, not a scientific negative.

C8.6 Integrity stops (exit 7).
- A hash mismatch of code, inputs or the application against the sealed manifest, or a runtime-version mismatch.
- A float-propagation overrun or an accounting-closure failure (C8.4).
- An edit-count mismatch.
- An extended-B3 resolved third direction (C3.11).
- An observed SYS-PC or SYS-LIM crossing.
- An SYS-NC1 refit mismatch.
- A mismatch between the exact recomputed t and the frozen rational.

C8.7 Workload estimate (UNVERIFIED feasibility estimate, not a guarantee) [condensed]. Reference: the sealed oracle run made 784,960 float propagations in t_elapsed_s = 21.7287, ~36,125/s including setup and reporting; linear scaling to 3,443,968 gives ~95.3 s. Not covered: 541 SVDs on small designs (largest fit design 384 x 3 global; class 96 x 3; largest B3 stack 384 x 8) and serialization; on paper small against the 540 s stop; not measured. Memory: not estimated; per-edit forecasts aggregated into loss cells, not stored per edit; a memory estimate is TO BE FIXED BEFORE FREEZE, in the application. No pilot is run (#38 L372).

## 9. Manifest, seal and approval

- C9.1 One package. It has its own scope, code, manifest and post-run index. Astra reviews this revised scope and the Research Lead freezes it before anything executes (E38-16; #37 L146).
- C9.2 Sequence (N2, v1_4_N L22-30).
  1. Code and the draft manifest are complete.
  2. The standing-approval application is filed. It cites by sha256 this record (as frozen), the #38, #37 and #36 raw files, the governing set, every implementation file and every input.
  3. The application sha goes into the manifest.
  4. The manifest is sealed.
  5. Stage S0 begins.
- C9.3 Preflight.
- It asserts sealed: true, all hashes, and the runtime versions, recording the observed versions as observations.
- It asserts that no checkpoint or weight file is read. The allowed input set is enumerated.
- C9.4 E37-2 hygiene. No hard-coded phase or seal strings appear in outputs. Every elapsed-time or memory figure names its source file and field.
- C9.5 Frozen in the manifest.
- C3.1-C3.12.
- C4 including the rules of C4.4.R and the exact t.
- C5 including the verbatim tolerances.
- C6.
- C7 including the thresholds.
- C8 including stage order, cache policy, accounting table and caps.
- The output schema and paths.

  No value is set or changed after any output of this package is seen (E37-9, E38-11).

10. Wording rules [condensed; all kept]. C10.1 Negatives (E37-4): "The declared [global/class-conditioned]-map intervention-prediction criterion was not met."; cap-limited work is "incomplete", never negative (E38-14). C10.2 Ratios (E37-3): "Comparator squared prediction error divided by actual response energy." C10.3 Oracle labels (E37-1): "Oracle-scale headroom only." C10.4 Neural ceiling: E37-10 and E38-15 verbatim plus the #38 L202 sentence. C10.5 SYS-PC success: "The class-conditioned fit recovered the declared sign-dependent synthetic map, which the global fit cancels as derived." - not that a network uses kappa, carries a class label or has a covariance register; thresholds never a neural floor. C10.6 Extended B3 never described as applicable to neural two-coordinate systems (E38-6). C10.7 SYS-LIM only with the exact failure statement of #38 L194; no impossibility wording (E38-9). C10.8 Confounds: RMS matching never described as matching response, conditioning, transferability or GRU geometry; "floor" not used for any confound result; SYS-NC1 described as varying-kappa two-coordinate confound. C10.9 SYS-FK "globally zero-kappa on product-chart designs"; no impossibility of alternatives (E38-10).

## 11. Status of Q1-Q17 and remaining open questions

Q1-Q17: all closed by #38 (L253-276) and applied as tabulated in the record [condensed]: Q1 C3.2, C6; Q2a-d change log 2-3, C3.2; Q3 C3.9; Q4 C7.3; Q5 C4.0, C7.1; Q6 C4.3; Q7 C4.4.R; Q8 C4.2(b); Q9 C5.5; Q10 C5.2, S0; Q11 C4 notation; Q12 C5.2; Q13 C4.1; Q14 C4.5; Q15 C7.2; Q16 change log 7; Q17 C4.5.
Items TO BE FIXED BEFORE FREEZE (or computed by the package under a frozen rule).
1. c2: TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW (C4.4.R).
2. c3: TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW (C4.4.R).
3. Full-precision D_psi, D_mu and the crossing bounds are computed by the package at S4 under C3.12. The rule is frozen; the displayed values do not govern.
4. Full sha256 of Q, Q2 and the directions arrays, plus their generation conventions, recorded in the manifest (Q10). TO BE FIXED BEFORE FREEZE.
5. Memory estimate and substantiated workload in the application (C8.7). TO BE FIXED BEFORE FREEZE.
6. Output schema and file paths (C9.5). TO BE FIXED BEFORE FREEZE.
7. Rulings or acceptance on Q-R1 to Q-R6. TO BE FIXED BEFORE FREEZE.
8. Implementation code, manifest and standing-approval application (C9.2). Not yet written.

Remaining open questions. These are new execution specifications that v1.2 proposes. Each needs Astra review, not a ruling already given.
- Q-R1 (D7 handling). v1.2 flags a failed applicable D7 identity as D7 INVESTIGATE, with no stop and no effect on any label. Is that the intended reading of "warrants investigation" (#38 L198)?
- Q-R2 (class zero-gain cells). v1.2 applies the gain tolerance to SYS-FK class losses per fold/class/group/size cell, extending #38 L296's fold/group/size. Confirm.
- Q-R3 (rank lapse in other controls). v1.2 reads E38-12's "every required control identity and its rank premise" as making SYS-O6 and SYS-FK rank lapses also NOT MET (RANK). E38-12 names only SYS-PC explicitly.
- Q-R4 (guard failure of an exact predictor). Under C5.3(c), a guard failure of a predictor covered by an applicable exact-recovery identity, when the actual belief is valid, counts as an identity failure. Confirm that this is the E38-7 "contradict" case.
- Q-R5 (extended B3). Are the C3.11 stacking convention (unweighted J; per fold and per foldxclass) and the band handling (UNRESOLVED-B3 recorded, no stop) acceptable?
- Q-R6 (cache policy and stage order, C8.1-C8.2). Specifically: per-system baseline propagation with no sharing; no prediction deduplication; the SYS-NC1 P0 sub-check at the start of S4.

12. Verification [condensed]
12.1 Read-only checks by the Delegate: raw #38 sha and 385 lines; the 16 E38 quotes, 43 body excerpts, Q table, model block and tolerance block extracted programmatically and checked as exact substrings; E37 quotes re-checked against #37 raw; exact rational t computed from stage_O1.json stage4_chart_exact [0][0] and [3][0]; stage_O1.json has no P_h or P_a key, so c2 and c3 cannot be computed exactly here; accounting arithmetic 7*(98,304*5 + 256) = 3,442,432 (matches #38 L369), + 1,536 = 3,443,968; 784,960/21.7287 ~ 36,125/s; 3,443,968/36,125 ~ 95.3 s; line citations in pinned.py, stages.py, results.json checked.
12.2 UNVERIFIED: D1-D7 and P0; all numerical ranks; full-precision normalizations and bounds; c2 and c3; NC admissibility; SYS-FK validity bounds; workload, runtime and memory.
12.3 Raw #38 vs the Specialist's summary (raw governs). Agrees on the main rulings. Differences followed per raw: (1) SYS-NC1 relabelled as varying-kappa two-coordinate confound, not renamed (L160); (2) plateau construction rejection also corrected (L225); (3) Q5 operational-diagnosis wording, attribution split withdrawn; (4) rank premises also cover SYS-O6 and SYS-NC2 (L73); (5) requirements the summary omitted (E38-5, -6, -7, -8, -11; Q4, Q10, Q11, Q12; L94; L186); (6) the full tolerance block L280-302; (7) Q-ceiling: "answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY"; (8) count: package maximum is 3,443,968 float plus 272 exact, since #38 L372 calls 3,442,432 "not yet the complete package count".
12.4 Not done: no code run, no oracle/solver/fit/simulation; repo not modified; v1.1 and note 1 not edited; nothing posted.

=== ADDITIVE NOTE_1 to v1.2 (Research Delegate; full text, sha256 832d9bcfb5855ad20abf242888bfda0f372f3ad83e48f197005e3d37905033b9) ===
# Additive note 1 to class-fit synthetic scope record v1.2 (Research Delegate)

Applies to: ckappa_classfit_synthetic_scope_record_v1_2.md (sha256 79ea0eeb1658e7d265aae3a68d31c6fb385ceab23a91eb654fee61a4aa64561c). v1.2 is not edited. Status: DRAFT, NOT FROZEN, NOTHING RUNS.
Source: CNA's read-only check of v1.2 against the #38 raw text (87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5), posted in the room on 2026-10-23 at about 12:42 AM ET. CNA found E38-2 and E38-10 correct, and E38-3 correct but with an incomplete table.

N1. Rows added to the C3.3(b) premise table, under E38-3: "applies consistently to all systems".
- D6, the SYS-LIM global fit. The derived expectation B = [c_x; c_y; lambda*c_tau] requires the global full design to be resolved at full column rank 3 and the mu design to be resolved at full column rank 2, the same premise as D1. If the premise fails, the cell reads EXPECTATION NOT APPLICABLE (RANK). The result stays REPORTED ONLY, and no label changes.
- SYS-NC1 global. The derived expectation Pred_full == Pred_mu requires the same premise, in addition to the zero-voids condition already stated in C4.4. If the premise fails, the cell reads EXPECTATION NOT APPLICABLE (RANK). The result stays REPORTED ONLY, and no label changes.

N2. A definition used wherever v1.2 says "resolved full column rank". It means every sigma_i/sigma_1 > 1e-6, the inherited upper band edge, with rcond = 1e-10 unchanged. A cell with any ratio inside the inherited band [1e-10, 1e-6] reads REFERENCE RANK UNRESOLVED, which the existing outcome order and the unresolved-class suppression rule then handle. It does not read EXPECTATION NOT APPLICABLE (RANK). That label is reserved for a resolved rank below full.

N3. Normalization for C4.4.R. Before c2 or c3 is computed, the package asserts in exact rationals that sum_a P_a = 1 over the prefixes the rule uses. If the assertion fails, that is PIPELINE INVALID, and nothing is rescaled. As a second guard, c2 is defined as rho_NC1 / sqrt(sum_a P_a), which equals rho_NC1 whenever the assertion holds. The c3 formula is unchanged, because the scale cancels.

There are no other changes. The open questions stay Q-R1 to Q-R6.

=== RESEARCH LEAD NOTES ===
- NOTE_1 records the CNA's read-only check of v1.2 against your #38 raw text (room, ~12:42 AM ET 2026-10-23), accepted by the Research Lead. CNA: E38-2 correct (C4.2(c) chart increment exact, J_a*delta first-order; C4.2(d) exact residual Phi(theta_a + S_gC delta) - Phi(theta_a + B_global delta); C5.6 finite losses; C4.5 marks D6's (1+lambda)^2 and factor 4 Jacobian-level; remaining exact claims exact because each readout is affine in z). E38-3 correct where stated but premise table incomplete (N1) and needs the sigma-ratio definition (N2). E38-10 correct. Non-blocking c2 normalization fix adopted (N3).
- Delegate's room summary of v1.2 matches the record (accounting totals 688,128 edits, 3,442,432 S6 + 1,536 O2 = 3,443,968 float + 272 exact propagations, 541 SVDs, 5,040 loss cells, ~95 s UNVERIFIED). Still open: Q/Q2/direction hashes and generation rules; memory estimate; output schema; code, manifest and application.

=== QUESTIONS FOR CONSULT #39 ===
(1) Does v1.2, together with NOTE_1 (the accepted CNA points), satisfy E38-1 to E38-16? Name any edit that is not met, or that is over- or under-implemented.
(2) Rule on Q-R1 to Q-R6:
- Q-R1: a D7 failure reads INVESTIGATE, with no stop.
- Q-R2: the class zero-gain check is per cell (fold/class/group/size).
- Q-R3: a rank lapse in SYS-O6 or SYS-FK also reads NOT MET (RANK).
- Q-R4: an exact predictor that fails the validity guard (actual valid) is an identity failure.
- Q-R5: the rank-guard (extended B3) stacking convention and band handling.
- Q-R6: the cache policy and stage order.
(3) Rule on the CNA's rank-table additions (NOTE_1 N1) and the sigma-ratio definition (N2), and on N3.
(4) Is the C8.3 accounting table complete and correct for E38-13?
(5) Can the remaining TO BE FIXED items (Q/Q2/direction generation rules and hashes, memory estimate, output schema) be fixed at implementation time and checked by an independent pre-seal review? Or must they be in the scope record before freeze?
(6) Verdict: FREEZE (optionally with named edits, verbatim, numbered E39-1..), or REVISE AND RESUBMIT. Restate the caps (current: 1 CPU, no GPU, RLIMIT_AS 4,000,000,000 bytes, 600 s cumulative, 540 s operational stop, hard termination <= 595 s, no retries) and the claim-ceiling text if they change.
