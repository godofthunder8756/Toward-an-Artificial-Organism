# Track B scope v3.6: CNA disposition v1 (light pass on PZ5–PZ8, KR-ID premises, B_req, e_PD, cross-references)

Author: CNA (adversarial reviewer, Track B: plants, confounds, observers, donor laws, hashes, manifest). Filed Sat Oct 24 2026, 12:3x PM EDT.
Status: PLANNING/AUDIT RECORD. Additive; no existing file modified. Nothing in this file authorizes execution.
This is the CNA light pass named in §PZ5 §11 (merged L2203) and §PZ5/§PZ2 header notes (merged L650, L1557). RD PROPOSED replacements of CNA-owned text govern only as dispositioned below.
Convention: "M Lnnnn" = merged v3.6 line; "CNA Ln" = CNA v3 half (5dec96f5); "E1 Ln" = CNA erratum 1 (da613127); "#47 Ln" = astra_consult47_response.txt; "PRQ Ln" = RD prerequisites; "CON Ln" = RD consolidated. All proposals are marked **PROPOSED, CNA**. Where a specification does not exist it is marked **ABSENT**.

## 0. Safety position (restated, unchanged)

- X1–X5 unchanged. No host coupling. No execution authorized (no training, simulation, Stage 0 or checkpoint inspection); this pass ran only pure arithmetic (§8).
- No stop-associated objective, reward or penalty: "no additional stop-associated reward, penalty or terminal return" (#42 L223, verbatim). The ordinary truncated return with its bootstrap term is not prohibited (#42 L223).
- Claim ceiling unchanged (#41 L304). No consciousness claims. Attribution wording ceiling stays at tier 1 (#47 L136) until P1 is filed and ruled; see §4 for an additional, independent tier-2 blocker.

## 1. Inputs (sha256 recomputed this pass; all match the hashes given by the Lead/RD; no mismatch)

| Input | sha256 (whole file) | Footer |
|---|---|---|
| trackB_instrument_validation_scope_v3_6_merged_RD.md | ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b | match |
| v3.6 addendum | 9bbde57e215343b518639a240af35c72efccfd49cf2dd82f869bbebec4809834 | match |
| astra_consult47_response.txt | 51d9f30d06344e851e2ae6b045e22dde312f4ba686489a338a218e36fe69be90 | n/a |
| RD consolidated | a043df3dbe43799d5a7903ae41d3d05e63d94c688349b24eb9439465ea6bbf30 | match |
| RD prerequisites | 69f884d59323c40312691f75afd18661cc6d4649429f39140eaba713ea550701 | match |
| CNA v3 half (plants) | 5dec96f59255cb2e9da29447cd102637c91a1736899f28653a606e2de8193321 | 7d93990c… match |
| CNA erratum 1 | da613127b981a365151bda7a0239fa62d2254ec54e1946f467f97e00a33be623 | 952a789e… match |
| env/integrity defaults (= §PY) | d5523c7152ec683b52a8ca2c16aed6036bd6f9ec6b93fe54b2d7a5655f43322e | match |
| CNA seams light pass | 9c55aae1b7d2d667c7cfe11db0569adc1ad998a4c4988dc66aa23182130d21c5 | match |
| LEAD_addendum1_rulings_2026-10-23.md | e90d49295f4b3d295dd846a18048fef8adc840a63149559e9b124717296c30e8 | n/a |

No CNA file is newer than Oct 23 15:14 EDT; no CNA text since then is superseded by anything here except where stated.

## 2. P1 dispositions by section

### 2.1 PZ5

| Section (M lines) | Disposition | Reason / exact edit |
|---|---|---|
| §2.3 clamp, coordinates, readouts (M L1855–1871) | CONFORMS WITH EDITS | Clamp x_PL(d) = x_d + v̂_E v̂_Eᵀ(x_i − x_d) and Δ_ATTR = Δ_E − Δ_PL conform to CNA §4.2 intent (CNA L146–151). N_ATTR,E is as governed by PZ6 §1.5 (M L2728–2730). The fallback "if ‖v_E‖ = 0 … x_PL(d) = x_d" (M L1869) **DOES NOT CONFORM** (it yields Δ_ATTR ≡ 0, a free null); it is already withdrawn by PZ6 §2.2 (M L2746–2752: degenerate cell ineligible). No further edit. |
| §2.3 statistics and label (M L1873–1878) | CONFORMS | m = 14, one-sided 0.996429 = 1 − 0.05/14 (I4); intersection–union for conjunctions (Lead rulings L7; PZ6 §5.5 M L2864). |
| §2.3 "Why residuals are bounded" (M L1880) | CONFORMS WITH EDITS | "Δ_ATTR = 0 exactly" holds only for known readouts (KR-ID, PZ6 §2.4 M L2758–2765), not for fitted probes. Append: "**For a null row's tier-2 use, the zero-E-use premise is established only by Route I or Route B of PZ8 §1.3; the KR-ID result does not establish it for fitted probes.** (PROPOSED, CNA)" |
| §2.3 "What Δ_ATTR measures" / wording | CONFORMS | As governed by PZ6 §1.2 (tiers, M L2695–2704) and PZ7 §1.4 (M L3038–3051). |
| §2.4 RCAL-ADV-E/-I (M L1886–1898) | CONFORMS WITH EDITS | Pure plant per R2 (E1 L12; CNA L186). Recipient restriction |controller argument| ≤ 0.25 is pre-intervention. Arithmetic verified: minimum Δ_E = σ(0.55) − σ(−0.05) = 0.146633 ≥ 0.1466 (§8). Edit to realization condition (4): replace "§1.3 inactivity" wording with "**Route I or Route B of PZ8 §1.3, evaluated per replicate and entering real_i of CNA §5 (L220)**". |
| §2.4 MIXED-CODE-E/-I | CONFORMS WITH EDITS | E1 L12 + S-I1 (Lead rulings L2; PZ5 §9 M L2185): C-NEC-DEP + checks 3a/3b at every ρ; E-ATTR NOT MET (E1 L38). Same edit for condition (4) as RCAL-ADV. |
| §2.4 REW-CORR-E/-I | DOES NOT CONFORM (as specified) | Action law and ε persistence ABSENT (E5 L67 "policy reads the state"; CNA v2 L148); G3 can fail (§3.3). Replacement law PROPOSED in §3.4. Separately, expected degenerate by construction (§4): Lead ruling required. |
| §2.4 ATTR-P1 | CONFORMS | |
| §1.4 relabels carried into §PY (§PY M L1361, L5 M L1383, X-6 M L1413, X-9 M L1416, D-RD14 M L1429) | CONFORMS WITH EDITS | The quoted no-op value 0.198 is S, not V (E43-1). Exact replacements (§PY text owned by CNA): §5.2 bullet: "no-op policy: V_no-op = 0.04 (E[V] = 0.036972), S_no-op = 0.198 (E[S] = 0.184116)". L5 cell, X-6, X-9, D-RD14: replace every "no-op V ≈ 0.198" with "no-op S ≈ 0.198 (V ≈ 0.04)". Values recomputed (§8). |
| §6.4 event order (M L2054–2074) | CONFORMS WITH EDITS | Step-3 outcome clip [0, 200] conforms to A4/A5 (M L1273–1274) min(1, ·) and LP-22 (M L2609). Step 0 replacement: "0  if a scheduled stop is due at t and the episode is at risk: STOP before anything below; **no additional stop-associated reward, penalty or terminal return (#42 L223)**; the ordinary truncated return with its learner-side bootstrap term only." |
| §6.5 approach rule (M L2076–2085) | CONFORMS WITH EDITS | B6 (M L1324) counts INTERACT on an available station; §6.5 dropped it. Shortest-path = Manhattan under A1 (M L1270, no internal walls), so the distance part conforms. Replacement count rule: "u counts as approach iff the agent's shortest-path distance to the target fixed at t_d strictly decreases at u, **or the agent is on that target while it is available and its action at u is INTERACT**." Restoration of CNA B6, outcome-blind; freeze before calibration. |
| §6.6 (M L2087–2089) | CONFORMS | |
| §6.7 (M L2091–2093) | CONFORMS | Astra β/4 arithmetic verified: 0.3×0.079 = 0.0237, 0.3×0.169 = 0.0507 (§8). |
| §7.2 ellipsoid wording (M L2133–2142, last row) | CONFORMS WITH EDITS | Adopt. Exact replacements: CNA §7.0 L341: "Conditional compatibility: draws must lie inside the declared high-probability ellipsoid (radius χ_d(0.99))."; L342: "Draws outside that ellipsoid are rejected and redrawn." E6 DL-PATCH (E1 L82): "{1.25, 1.5} × the χ_d(0.99) ellipsoid radius, i.e. outside the declared high-probability ellipsoid for any d." Also, Q-LEARN bullet (M L2138) drops R39: append "'Acquired' or 'learned' only when all three §5.6 conditions hold (#41 L168); otherwise 'increased through training' (Lead rulings L6)." |

### 2.2 PZ6

| Section (M lines) | Disposition | Reason / exact edit |
|---|---|---|
| §1.3 fidelity (M L2706–2711) | CONFORMS WITH EDITS | Citation "same bootstrap as §5.4" is unresolved (§6). Replace with "the seed-level bootstrap of PZ5 §4.2 step 2 (M L1958; B = 10,000; seed as unit), one-sided 95%". tol_fid = 0.05; FID-DET protective; D_PR over all replicates: conform. |
| §1.4 NLN (M L2713–2726) | CONFORMS WITH EDITS | As superseded by PZ7 §1.2/§6.1 (M L3014–3032, L3204–3208). Update law after t_d is ABSENT; u₁ is re-read from E, so a clamped φ must persist. PROPOSED, CNA: "Stored coordinate φ: φ_{t+1} = λφ_t + (1 − λ)·r_std,t, λ = 1 − 1/τ_r; u₁ = 1 + (E − 0.5) recomputed each step from E; u₂ := φ/u₁ is derived, not stored; the controller reads φ only." |
| §1.5 N sets (M L2728–2730) | CONFORMS | |
| §4.3 accrual (M L2815–2820) | CONFORMS WITH EDITS | "quota of usable allocations per seed (50 recipients, with their donors)" conflicts with CNA §4.1 (CNA L124; M L735): A_cells = 50 per cell per seed. Replace with "**50 usable allocations in each of the four E × r̄ cells per seed (200 per seed) (CNA §4.1)**; every screened recipient that reaches t_d enters the E2 eligibility denominator." |
| §5.3 L8 (M L2845–2854) | CONFORMS WITH EDITS | "No stop-associated reward, penalty or terminal return" is not the ruled sentence. Replace with the verbatim #42 L223 sentence (§0). L8 Q/S independence and ≤ 40,000 conform. |
| §5.4 aggregation (M L2856–2860) | CONFORMS WITH EDITS | Per-seed mean over eligible trials; B as fraction of 10 steps conform. Carry the §6.5 INTERACT edit. |

### 2.3 PZ7

| Section (M lines) | Disposition | Reason / exact edit |
|---|---|---|
| §1.2 (M L3014–3032) | CONFORMS | As amended by PZ8 §1.2. |
| §1.3 (M L3034–3036) | Withdrawn (PZ8 §1.3) | Noted only. Its g = β·z_R is superseded by g = z_R/SD(z_R) (E1 L12; PZ8 §2.2(d)). |
| §1.4 table (M L3038–3051) | CONFORMS WITH EDITS | Except the REW-CORR expected cell: replace with "**CONFOUND NOT REALIZED pending Lead ruling on CNA disposition v1 §4**". |
| §4.3 (M L3137–3143) | CONFORMS | As amended by PZ8 §3.2–§3.3. |
| §5.4 (M L3177–3194) | CONFORMS WITH EDITS | Replace "RCAL-ADV with §1.3 inactivity" with "**RCAL-ADV, MIXED-CODE and REW-CORR each PASS with Route I or Route B (PZ8 §1.3)**". |

### 2.4 PZ8

| Section (M lines) | Disposition | Reason / exact edit |
|---|---|---|
| §1.2 (M L3347–3356) | CONFORMS WITH EDITS | M L3349 "same bootstrap as PZ5 §5.4" is wrong (§6). Replace with "PZ5 §4.2 step 2 (B = 10,000; seed as unit), one-sided 95%". |
| §1.3 Routes I/B (M L3358–3370) | CONFORMS WITH EDITS | (i) Setting citations (M L3362) per §6. (ii) Premises for MIXED-CODE/RCAL-ADV hold only with §3.2 pinning text. (iii) U_A conditioning sentence (§3.1 e). (iv) Add: "**Route I/B is assessed per replicate and enters real_i of the row's f_ok rule (CNA §5 L220).**" (v) REW-CORR per-row text (M L3369) replaced by §3.4; row remains blocked by §4. Gate kept unrounded: C_H·U_A < 0.05 ⇔ U_A < 1/33 = 0.030303 at C_H = 1.65 (#47 L57–61). |
| §1.4 (M L3372–3375) | CONFORMS | |
| §2.2 row (b) (M L3405) | CONFORMS | |
| §2.2 row (c) (M L3406) | CONFORMS | |
| §2.2 row (d) (M L3407) | CONFORMS WITH EDITS | SD(z_R) (REW-CORR: SD(z)) is a frozen fitting-partition constant; for REW-CORR a_d,i uses ζ (§3.4). |
| §3.2–§3.3 (M L3442–3461) | CONFORMS | Arithmetic verified (§8). |

### 2.5 Rulings consistency

R2 pure plant preserved (E1 L12; PZ7 §6.1 M L3208). S-I1 preserved (M L2185). Intersection–union, not Holm (M L2864). I4 m = 14, 0.996429. R39 needs the M L2138 carry edit (§2.1).

## 3. KR-ID premise checks (P1 a–e; #47 L47–53, L57–61, L130–131)

### 3.1 MIXED-CODE-E/-I and RCAL-ADV-E/-I (same pure plant; M L1890)

| Check | Verdict | Basis |
|---|---|---|
| a. Action law | HOLDS GIVEN §3.2 TEXT | P(approach) = σ(a − β·z_R/SD(z_R)), β = 1.2 (E1 L12) ⇒ c_π = β/4 = 0.3, C_H = 1.65 (κ_j = 1). The approach/non-approach action kernels are ABSENT (CNA L187 "monotone function"). Without §3.2 text: NOT ESTABLISHED. |
| b. G3 (update) | HOLDS (pathwise) GIVEN §3.2 TEXT | z_R = r̄ (CNA L80, L95, L185): deterministic EMA of the reward history ⇒ under identical history Δg_j = λ^{j−1}Δg_1, κ_j ≤ 1. Exact recursion and read timing ABSENT → pinned in §3.2. C_H = 1.65 with κ_j = 1 is conservative (1.5549 with κ_j = λ^{j−1}, REPORTED only). |
| c. G1, G2, G4 | G1, G2 HOLD; G4 HOLDS GIVEN §3.2 | G1: pre-drawn streams A11–A13, A18 (M L1290–1300); CRN (E2 L48); scoring reads positions only (PZ6 §5.4). G2: E1 L12 + kernels. G4: z_E weight exactly 0 (E1 L12); decoys are separate blocks; other block coordinates (d_ws ≥ 6) ABSENT → §3.2. Fate noise in plants ABSENT → §3.2 (off). |
| d. Persistence of noise | N/A | No noise in controller input. |
| e. U_A conditioning | CONFORMS WITH EDITS | PZ8 L3368 does not tie U_A to Δ_ATTR's units. Add: "**U_A is computed over exactly the recipients and four-continuation units entering the row's Δ_ATTR (same usable cells, eligibility and exclusions), A_i equally weighted within seed and seeds equally weighted, conditional on the same frozen recipient states, donors and fitted probes. By linearity |E mean Δ_ATTR| ≤ C_H·mean A_i per seed.**" Level one-sided 95% (realization level, E7 L97), not 0.996429. |

### 3.2 PROPOSED, CNA: pinning text for MIXED-CODE / RCAL-ADV (insert in §PC1 after CNA L187)

"Reward coordinate: z_R,t = λ·z_R,t−1 + (1 − λ)·r_t, λ = 1 − 1/τ_r, τ_r = 50, z_R,0 = 0; updated at end of step t after r_t is known (A16); the controller at step t reads z_R,t−1; no other input. SD(z_R) is a frozen constant from the fitting partition. Action kernels: with probability p_t = σ(a − β·z_R,t−1/SD(z_R)), β = 1.2, draw from K_approach = one move along a shortest path (static walls) to the nearest available target (food item for -E/-I food rows; repair station for -I), ties to lowest index, or INTERACT if on an available target; otherwise draw uniformly from K_other = the remaining A7 actions that do not strictly decrease that distance. Both kernels are functions of world state only; all draws use the action-sampling CRN role. Every block coordinate other than z_R is written only from world quantities or a dedicated CRN role and is read only by frozen probes; d_ws is declared by the generator. No fate noise." Then K_approach and K_other have disjoint supports, TV(π_x, π_x′) = |Δp| ≤ 0.3·|Δg|, case (ii) holds.

### 3.3 REW-CORR-E/-I (as currently specified)

| Check | Verdict | Basis |
|---|---|---|
| a | ABSENT | E5 L67 "policy reads the state"; CNA v2 L148 "reads r̄". No law. |
| b | ABSENT; CAN FAIL | ε persistence and z update unstated. Counterexample if ε is stored in the block and persists: Δζ = 1, Δε = −1 ⇒ Δg_1 = 0 but Δg_j = λ^{j−1} − 1 ≠ 0 (−0.02, −0.0396, … at λ = 0.98); no κ_j bounds this by Δg_1. |
| c | G1 HOLDS; G2, G4 ABSENT | |
| d | PROPOSED §3.4 | ε per-step, CRN-shared, not stored. |
| e | As §3.1 e | |

### 3.4 PROPOSED, CNA: REW-CORR law (replaces CNA §8.1 L431 "State law" for REW-CORR and E5 L67 parenthesis)

"Block stores ζ_t, updated exactly as z_R in §3.2 (τ_r = 50), plus write-only coordinates as §3.2. Controller input z_t = ζ_t−1 + ε_t, ε_t ~ N(0, (0.1·SD(ζ))²) drawn i.i.d. every step from a dedicated 'rewcorr-eps' RNG role, shared by all four continuations (CRN), never stored in the block and never transplanted by swap or clamp. Action law and kernels identical to §3.2 with g_t = z_t/SD(z), SD(z) frozen (= SD(ζ)·√1.01). Route B: a_d,i := |ζ(x_PL(d)) − ζ(x_d)|/SD(z)." Then ε cancels within a recipient, Δg_j = λ^{j−1}Δζ/SD(z), c_π = 0.3, C_H = 1.65. C-EXIST/C-CAUSE/C-NEC-DEP REW-CORR rows unaffected (J contains r̄: ΔR² ≈ 0; realization R²(ζ → E) = ρ²).

## 4. CNA finding F-RC: REW-CORR-E/-I is expected to be degenerate (Lead ruling required)

Analytic expectation, not a run. REW-CORR carries E information only through r̄ (CNA v2 L118; CNA L431), and r̄ ∈ N_ATTR (PZ6 §1.5 M L2730). The fitted E probe therefore lies essentially in span(W_N): ρ_E ≈ 0 < ρ_min = 0.10 (PZ6 §2.2 M L2749–2750) ⇒ degenerate ⇒ ineligible ⇒ E2 eligibility floor fails ⇒ CONFOUND NOT REALIZED under CNA §5 f_ok (L220) ⇒ tier 2 blocked (M L3360) regardless of P1(d). Contrast: MIXED-CODE is non-degenerate (by hand, ρ_E ≈ 0.90 at ρ = 0.9). No existing file addresses this (rg over merged REW-CORR mentions).

| Option | CNA view |
|---|---|
| A. Status quo | Tier 2 expected permanently blocked. Safe but uninformative. |
| B. Pre-data re-specification (CNA preferred) | PROPOSED, CNA: "For REW-CORR-E/-I only, real_i = 1 iff E5 checks 1–2 (corr, R²) hold and either every cell is degenerate (the declared known answer: no nuisance-orthogonal E coordinate exists) or Route I/B holds on the non-degenerate cells. Degenerate cells are non-MET, not ineligible, for this row. PASS iff f_ok CP ≥ 0.90 and the all-replicate false-MET criterion holds; degeneracy rate REPORTED." Needs Lead ruling + Astra confirmation (#48). Not gate relaxation in CNA's view (no frozen gate exists; pre-data; makes the row testable), but the Lead should decide whether Aidan must see it (PRQ §4). |
| C. Drop the row | Not recommended: removes a required control. |
| D. Redesign as MIXED-CODE-like | Duplicative of MIXED-CODE. |

Until ruled: REW-CORR is CONFOUND NOT REALIZED; tier-1 ceiling stands.

## 5. B_req (P2) and e_PD (P3)

| Item | Disposition | Detail |
|---|---|---|
| B_req as a number | ABSENT | Not in any CNA/RD/merged file. Only #44 L171, #47 L131, RD files (PRQ L50–58) reference it. M L2009 "At B_req = 6 that is 120" is RD illustration. |
| B_req = 6 | DOES NOT CONFORM | Non-conservative: near-transition bins are chosen within each replicate on the selection partition (M L313, L376), so they cannot be pre-designated; every grid level must be schedulable. Only stated grid size is ≥ 9 levels (scope v1 L71). At n = 120, B = 9: all-bin attainment 0.929 (Bonferroni bound) / 0.931 (independent) < 0.95. |
| B_req recommendation | PROPOSED, CNA | B_req := K_s, the size of the frozen IGN strength grid; every level is a required bin (CNA §8.1 L440 "every required strength bin and each near-transition bin": the near-transition bins are members of the grid, not extra bins). K_s itself is ABSENT in v3.6: PROPOSED K_s = 9 (scope v1 L71 minimum). Then B_req = 9 ⇒ n_sched = 121 at e_PD = 0.90. |
| e_PD | CONFORMS (adopt 0.90) | Conservative and outcome-blind. n_sched table (§8). |
| Binding constraint (note) | CNA §8.1 L440 per-bin CP floor | Floor requires ≥ 115/121 eligible; P(pass per bin) = 0.036 at true e = 0.90, 0.598 at 0.95, 0.927 at 0.97. The floor, not the 100-trial quota, binds. Floor unchanged; no rescue. The unit of the floor (per seed vs per replicate pooled over seeds) is ABSENT in CNA §8.1; CNA-owned clarification PROPOSED, CNA: "per (replicate, required bin), pooled over that replicate's seeds". Lead to confirm before freeze; if the Lead treats this as a gate change, route to Astra. |

## 6. Cross-references

| Citation (location) | Finding | Exact replacement |
|---|---|---|
| "PC1 §5" (PZ8 §1.3 Setting, M L3362) | Redundant but valid: §PC1 (M L648) is CNA v3 §5 verbatim; z_R = r̄_t (CNA L185), reads only z_R (L186). But the logistic law is in E1 L12, not §5 (L187 "monotone function"). | "§PC1 (CNA v3 §5, L185–187) and §PZ2 erratum E1 (L12)" |
| "PC §8.1 + erratum E5" (M L3362) | No "§PC" section. CNA v3 §8.1 is in §PX (REW-CORR row M L1121; CNA L431: z = p + ε, p = r̄). E5 L67 correct but adds only "policy reads the state". Neither gives action law nor ε persistence. | "CNA v3 §8.1 (L431; carried in §PX, M L1121) and §PZ2 erratum E5 (L67); law per CNA disposition v1 §3.4" |
| "erratum E1" | Correct (E1 L12: reads only z_R, z_E weight 0, β = 1.2). | none |
| "PZ5 §5.4" bootstrap (PZ8 §1.2 M L3349) | Wrong: PZ5 §5.4 is accrual rules (M L2003). B = 10,000 is at PZ5 §4.2 step 2 (M L1958). Sidedness per merged §5.4 (M L326). RD consolidated F2 (CON L145) "could not locate B" is therefore incorrect. Resampling type for the seed-level bootstrap is ABSENT (D7 M L596 percentile covers the episode-cluster bootstrap only). | "PZ5 §4.2 step 2 (M L1958; B = 10,000; seed as unit), one-sided 95%". PROPOSED, CNA (RD-owned): "percentile seed-level bootstrap, as D7". Same fix for PZ6 §1.3 M L2708. |

## 7. Open items for the Lead

1. Rule on F-RC (§4): option A or B. If B, route to Astra #48.
2. Adopt or reject §3.2 and §3.4 texts (P1 a, b, d premises).
3. Freeze K_s and B_req (§5); confirm CP-floor unit.
4. Apply the edits in §2 and §6 in the next RD merge; the §6.5 INTERACT restoration and the L223 sentence are carry-forward corrections, not new rules.
5. Nothing here needs Aidan, unless the Lead judges option B a gate change.

## 8. Arithmetic (pure Python, /workspace/scratch/cna_disp/arith.py; exact binomial; no simulation)

- c_π = 1.2/4 = 0.3; C_H = 0.3×(1/10)×ΣΣκ_j = 1.65 (κ_j = 1); 1.5548513 (κ_j = λ^{j−1}, λ = 0.98). Gate U_A < 0.05/1.65 = 0.030303.
- σ(0.3) − σ(−0.3) = 0.148885; σ(0.55) − σ(−0.05) = 0.146633.
- 0.3×0.079 = 0.0237; 0.3×0.169 = 0.0507; 0.3×0.05 = 0.015.
- No-op: E[V] = 0.036972, E[S] = 0.184116.
- n_sched = min n with P(Bin(n, e) ≥ 100) ≥ 1 − 0.05/B:

| e \ B | 1 | 2 | 4 | 6 | 8 | 9 | 10 | 12 | 18 |
|---|---|---|---|---|---|---|---|---|---|
| 0.85 | 125 | 127 | 129 | 130 | 130 | 130 | 131 | 131 | 132 |
| 0.90 | 117 | 119 | 120 | 120 | 121 | 121 | 121 | 122 | 122 |
| 0.92 | 114 | 115 | 116 | 117 | 117 | 117 | 118 | 118 | 118 |
| 0.95 | 109 | 110 | 111 | 112 | 112 | 112 | 112 | 112 | 113 |

- All-bin attainment at n = 120, e = 0.90 (independent / Bonferroni): B=2 0.984/0.984; B=6 0.953/0.952; B=9 0.931/0.929; B=12 0.909/0.905.
- Per-bin CP floor (one-sided 95% lower bound ≥ 0.90): n = 120 needs x ≥ 114 (P pass 0.038 / 0.606 / 0.930 at e = 0.90 / 0.95 / 0.97); n = 121 needs x ≥ 115 (0.036 / 0.598 / 0.927).

sha256 of all content above this line: ab95954c9306bd9cc4582470dfb72cdb09cf9e35a0f30b76ef13a224247e9fc7
