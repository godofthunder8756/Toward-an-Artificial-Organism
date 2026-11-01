# Track B freeze preparation v2.6: CONSOLIDATED (Lead) — E50-1..E50-5 responses, Lead rulings, named pre-data amendments, recost

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** A new, additive file; it edits no existing file. Under the binding rule, no chmod-444 file is rewritten in place; corrections go in new versioned files beside it. Nothing was run, timed, benchmarked or installed. The only computation was SHA-256 and exact integer/rational arithmetic in the system `python3` (scripts `scratch/lead_v26/ledger.py`, `ledger2.py`, `ledger3.py`, `gen_v26.py`); no scipy was used or installed. **Every CPU-hour figure is arithmetic on stated per-unit costs and is UNVERIFIED** (A50 L212).
- **Written:** 2026-11-01, about 12:36–12:50 PM ET, by the Lead's executor. Lead rulings given in the "ACI Research" room, about 12:14–12:36 PM ET.
- **Shorthands:** "A50 Ln" = line n of Astra's raw #50 reply; the other abbreviations are those of §10 (governing file list, full hashes).
- **Governance:** GA-1 and A-2026-10-24 remain approved by Aidan (2026-11-01 10:58 AM ET). Every change below is a **prospective, pre-data** change under A-2026-10-24, adopted before any calibration, pilot, feasibility or diagnostic output exists (A49 L47, L87). **No freeze, execution, benchmark or timing run is requested or authorized** (A50 L250). Any such run needs its own protocol, Astra's review **and** Aidan's explicit yes; none is planned.
- **Safety (unchanged):** X1–X5; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); claim ceiling (#41 L304); no consciousness claim is made or implied.

## 0. Status of Astra's #50 edits (A50 L240–L250; for Astra to confirm in #51 Q0)
| Edit | Response | Where |
|---|---|---|
| E50-1 GA-1 outcome structure | CE50 §1 truth table v3 (rows 0, 1, 2, 3, 4, **4B**, **4U**, 5); plant realization PR separate from availability (n_cons ≥ 36) and from the binding screens S_cons and S_wc; NOT ASSESSED → UNRESOLVED, never PASS; ROW0-FL for quota shortfall | §1 |
| E50-2 transition rule, gates, LIM path, cell list | RD26 §1.1–§1.4 (ŝ* from the frozen H1 logistic on selection data; gates G-i/G-ii/G-iii with precedence; LIM fixture (A) plus end-to-end (B)); **LIM IN calibration**; cell-ID list of 15 / 20 | §2 |
| E50-3 noise reference, domain, root rule, validated object | CE50 §2 + CE50e1 E1-1 (σ_ref from the IGN-P1 reference; domains; 100-iteration bisection with assertions; S_max = 8; integer n_EM); validated object = the discrete recursion | §3 |
| E50-4 network centre and quantile | RD26 §2 + corr2: n_c = 101 centre runs, n_q = 1,000 quantile runs (separate roles, never reused), r_q = ⌈0.99(n_q + 1)⌉ = 991, tie rule d ≤ T, n_q ≥ 199 | §4 |
| E50-5 workload ledger | WL, recosted here with P-1…P-9 and the RD params EDITs; maximum-cost accounting; early stopping NOT adopted | §6 |

## 1. E50-1: GA-1 (CE50 §1 as amended by CE50a1 R1, R3 and CE50e1 E1-3…E1-5)
- **Truth table v3** (CE50 §1.2, adopted): 0 construction failure / INCOMPLETE; 1 all-D; 2 N (pr_i = 0); 3 Q-insufficient; 4 NOT MET; **4B BOUNDARY** (a computed non-licence); **4U UNRESOLVED** (an unavailable assessment); 5 MET. Row 4b (ER1, E2-3, #50 E1) is split into 4B and 4U (A50 L27–L31).
- **Plant realization** (L-3): pr_i = 1 iff E5 checks 1–2 pass and the replicate is not row 0; PR = Σ pr_i/200 must reach ≥ 188/200 (CP lower ≥ 0.90). This replaces f_ok (M L698) for GA-1 rows. N keeps pr_i = 0. A50 L56, verbatim (quote corrected per CE50e1 E1-3; CE50 L40's "remain[s]" is replaced): "Their causes and realization treatment remain different; their absence cannot demonstrate an unmeasured operating characteristic."
- **Assessment availability:** n_cons = n4 + n4B + n4U + n5 ≥ 36 (A50 L41).
- **Literal false-licence rate** (REPORTED): FL_lit = n5/(n4 + n4B + n5). **Decisive-only** n5/(n4 + n5) is REPORTED as "conditional on a decisive result; not the overall false-licence rate" (A50 L33).
- **Binding screen S_cons** (L-2; A50 L35–L41): S_cons = (n5 + n4B + n4U)/(n4 + n4B + n4U + n5), i.e. Astra's literal A50 L41 denominator n4 + n4b + n5 with 4b = 4B + 4U. It is a combined specificity/informativeness screen (A50 L37), not the observed false-licence rate. **Thresholds: point ≤ 0.05 and one-sided 95% Clopper–Pearson upper ≤ 0.08** (the M L1965 conditions; **amendment AM-8**). The separate 4b-share cap is withdrawn (A50 L39).
- **ROW0-FL (Lead ruling; amendment AM-1, a named override of M L3422).** A per-(seed, required bin) final-partition quota shortfall makes the replicate **INCOMPLETE** (M L2009: "bin shortfall → that replicate is INCOMPLETE"). It goes to row 0 under reason code QUOTA-SHORTFALL, with:
  - realization pr_i = 0, and it stays in the 200;
  - it is **outside S_cons**, which keeps Astra's literal A50 L41 denominator;
  - it is **adverse in both the numerator and the denominator of the binding S_wc** = (n5 + n4B + n4U + n0Q)/(n4 + n4B + n4U + n5 + n0Q), with the **same thresholds as S_cons** (point ≤ 0.05, CP upper ≤ 0.08; AM-8);
  - **any licence in it makes the row FAIL** (A50 L41: "Row-0 licences remain immediate failures").
  - M L3422 says an INCOMPLETE replicate "stays in every denominator as a non-success". Counting it as a non-event in the false-licence screens would lower them, which is anti-conservative (RDLP V-1). Hence the named override. Exact example (RDLP V-1; RDPP V-14, reproduced here): 20 adverse of 200 FAILs (CP upper 0.142); converting 12 of them to shortfalls gives S_cons = 8/188 (CP upper 0.0755, PASS), but S_wc = 20/200 → FAIL. The largest passing adverse count at 200 is 9 (9/200 → 0.0772; 10/200 → 0.0833). S_wc ≥ S_cons always.
- **Row outcome** (CE50 §1.4 with L-4 precedence; supersedes V25 L56, ER1 E1, E2-3, E2-4, C2 and C3 §1, per CE50a1 R1):
  1. a licence in row 0 (no valid computed label, including a QUOTA-SHORTFALL replicate) → **FAIL**;
  2. availability holds and S_cons or S_wc violates its thresholds → **FAIL**;
  3. PR CP lower < 0.90 → CONFOUND NOT REALIZED → **UNRESOLVED**;
  4. n_cons < 36 → **UNRESOLVED (insufficient support)**, blocking PASS, whatever row removed the support (A50 L47–L48, L56);
  5. otherwise **PASS**.
- **Narrowing of rows 1/2/3/4b stays closed** (L-5; CE50e1 E1-4): "no exemption from the insufficient-support rule for rows 1, 2, 3 or 4b unless an applicable construction-level proof, made before execution, is filed (A50 L56–L58)". No such proof exists in the governing text (#51 Q6 asks Astra to confirm this reading).

## 2. E50-2: transition rule, gates, LIM, cells (RD26 §1, as amended)
- **ŝ*** = −θ₀/θ₁ from the frozen H1 logistic π(s), fitted on the selection partition per replicate and c-level, pooled across seeds; fixed bound [s_1, s_9]; non-locatable or outside → UNAVAILABLE (IGN-UA-SSTAR) (RD26 §1.1). Gates G-i/G-ii/G-iii with precedence (RD26 §1.2). G-ii is the quota itself; a shortfall is INCOMPLETE (ROW0-FL above), not a separate UNAVAILABLE.
- **IGN-LIM IN calibration (Lead ruling; amendment AM-7).** LIM's limitation behaviour is a required check that must not become "untested" (A50 L97). Validation by (A) a deterministic gate fixture on the analytic s*_LIM (predicate returns OUTSIDE-HIGH for LIM/0, OUTSIDE-LOW for LIM/1) and (B) full calibration and confirmation of the estimated-ŝ* path. |C_cal| = 15, |C_conf| = 20.
- **Cell-ID list** (RD26 §1.4; A50 L111): C_cal = IGN-P1/0, IGN-N1/0, IGN-NC1/0, IGN-NC1/1, IGN-NC2/0, IGN-NC2/1, IGN-LIM/0, IGN-LIM/1 (8 scalar); BOTT/0, BOTT/1, RINIT/0, RINIT/1, RINIT/2, ARCH/0, ARCH/1 (7 network). C_conf = those 15 plus IGN-NC2r/0, IGN-NC1/D0, IGN-NC2/D0 (scalar) and BOTT/D0, ARCH/D0 (network): 11 scalar, 9 network. DOSE0 = 2^64 − 1, unsigned big-endian (E2-8).
- **RAND-INIT dose 0 dropped** (amendment AM-5; deviation from CNA2 L242; A50 L107 accepts it as a named scope change). **NC2r demoted to descriptive** (amendment AM-6; A50 L109): its required validation role is withdrawn; IGN-NC2r/0 is confirmation-only, descriptive and REPORTED, and no calibrated performance on recurrent-clipping mechanisms is claimed from any other row.
- **Hysteresis** (MP L72): scheduled as **REPORTED** only (one ascending and one descending sweep per seed-unit; ≤ 27,828,000 trial-equivalents at n = 67). It enters no label.

## 3. E50-3: scalar plants (CE50 §2 + CE50e1 E1-1, PP §1/§3–§5, RDPP EDITs)
- **Noise reference (L-6):** one σ_ref for every scalar IGN row, from the declared bistable reference IGN-P1 at g_ref = g_P1, s = 0, noise-free: σ_ref = 0.05·Δ_ref, Δ_ref = 2x*, frozen as float64 hex. It is never recomputed from a row's own attractors (A50 L142). At g_P1 = 2.0 (example values, system libm, UNVERIFIED for freeze): x* = 0.9575040240772688, σ_ref = 0.09575040240772688.
- **Domains (L-7):** τ = 1; graded g ∈ [0, 0.8]; bistable g ∈ [1.25, 4]; g = 1 excluded; null input s = 0; Δt = τ/(100·G), G = ⌈max(1, g − 1)⌉.
- **Gains (P-1):** g_P1 = g_LIM = 2.0 (G = 1); graded g = 0.5 for N1 and the NC1/NC2/NC2r subunits.
- **Root rule (L-7 + CE50e1 E1-1; amendment AM-9):** float64 **bisection, exactly 100 iterations, no early exit**, under the pinned libm, replacing E2-2's fixed-point iteration (which Astra found not guaranteed for every g, A50 L153). Graded bracket [−1, 1]; bistable bracket [10⁻³, 1] at s = 0, x_lo = −x*. Assertions (i′)–(viii) → construction failure (M L3421), no fallback:
  - (i′) effective input u = s − θ non-finite or |u| > **S_max = 8**, checked by a **construction-time sweep over the full frozen input table** and at every root call (RDPP V-6);
  - (ii) no strict sign change; (iii) |F| > 10⁻¹² after 100 iterations; (iv) stability margin λ ≤ 0; (v) bistable x* < 0.6 or Δ_ref non-finite; (vi) any non-finite value;
  - x0 := 0 exactly **iff u = 0 exactly** (the **x0 key**); otherwise bisection;
  - (vii) **integer n_EM** = t_r × 100 × G, frozen as **literal integers** in the freeze record, plus (vii-b) at readout the integer step counter equals n_EM (RDPP V-7); never t_r/Δt in floating point;
  - (viii) 0 < h·λ < 2 at every frozen x0;
  - P6 KAT: tanh(8.8) < 1 − 2⁻³⁰ under the pinned libm.
- **Validated object (L-8):** the discrete Euler–Maruyama recursion, not the SDE (A50 L151). The SDE is interpretation only. The Gaussian-approximation caveat applies to the 2×MAD exclusion figures (CE50 §2.7; A50 L117).
- **Scalar settling (amendment AM-4):** V25 §6.1 wording adopted: scalar plants use **t_s = 0** (analytic reset x(t_0) = x_lo, x_ref = x_lo); M L1127's t_s = 5τ applies to **networks only** (20 steps), and the M L1129 tolerance is "Network instruments only".
- **Strength grids (P-4, RDPP V-5):** s_c(g) = g·√(1 − 1/g) − atanh(√(1 − 1/g)); s_c(2) = 0.532839975353552 (hex 3fe10d066b84a372). Fold-based grid **s = fl(s_c·m)/4** with integer m = i − 1 + o (one rounding), i = 1…9, frozen as hex. NC1 θ = δ·m_θ with m_θ ∈ {3, 5} (Δs = 2) and {2, 6} (Δs = 4).
- **LIM (P-5):** s*_LIM = s_c(g_LIM); LIM/0 grid = S − 7δ, LIM/1 grid = S + 7δ (transition 3 steps outside each grid). Max |u| = 1.99815 ≤ S_max.
- **G-iii Var(w) floor (P-6, RDPP V-4):** scalar floor **(0.01·Δ_ref)² = 3.6673 × 10⁻⁴**. Linearised pure noise sits **5.28–9.05×** above it over t_r ∈ {2, 3, 5}, using V(n_EM) for both rows (first-order figures, A50 L117). **Network floor: PENDING** (rule (0.01·m₀)² proposed; P4).
- **NC2 ceiling (RDPP V-1; amendment AM-3, redefining CNA2 L297):** c_p(t_r) = the **type-1 (inverse-ECDF) p-quantile of the 9 equally weighted noise-free grid readouts** x_nf(s_i, t_r) of the frozen recursion (σ = 0), index ⌈p·9⌉ in exact rationals, frozen in hex **per t_r ∈ {2, 3, 5}** and p ∈ {0.8, 0.6}. The clip is post-readout only. A **bitwise fixture** asserts that the pre-nonlinearity w sequences with and without the clip are identical (otherwise construction failure). The post-nonlinearity D ≥ 2 realization check stays per replicate and binding.

## 4. E50-4: network centre and quantile (RD26 §2 + corr1 + corr2; PP §2)
- **Centre:** coordinatewise median over **n_c = 101** null-centre runs (P-2) per (replicate, seed, cell), role `ign-null-centre`.
- **Quantile:** **n_q = 1,000** null-quantile runs (P-3), role `ign-null-quantile`, separate from the centre runs and never reused; T = X_(r_q), no interpolation; eligible iff d ≤ T.
- **Rank (Lead ruling; amendment AM-11):** **r_q = ⌈0.99·(n_q + 1)⌉ = 991** at n_q = 1,000. This **departs from Astra's "990th ordered distance" (A50 L125)** by one order statistic, in the conservative direction. **Event wording:** "coverage < 0.97" = P[Bin(n_q, 0.97) ≥ r_q] = **5.6601e-06** at r_q = 991 (vs 1.8130e-05 at 990, A50 L130). This is a per-threshold statement, not simultaneous over the battery (A50 L132). Nominal coverage 991/1001.
- **Construction requirement (amendment AM-10):** **n_q ≥ 199**; n_q < 199 is a construction failure, asserted before any null draw (for 99 ≤ n_q ≤ 198, r_q = n_q and T would be the sample maximum; checked exactly).
- **Symbols (CE50e1 E1-2):** k_FY (Fisher–Yates index), n_EM (EM step count), r_q (quantile rank).

## 5. Fitter and ΔLL
- **ΔLL-HO (amendment AM-2, from MP L69):** ΔLL is **held-out on the final partition** (fit H0/H1 per seed on that seed's 2,286 fitting trials; score on its 1,143 final trials). **Cross-validation is NOT run at all.** Anti-leak pins (RDPP V-3): (1) fits are per seed; (2) every data-derived start or scale comes only from the partition being fitted; (3) Ashman D comes from the fitting-partition H1 fit. M L312–L313 govern ("no fitting on final-test data").
- **Fitter (P-7 with RDPP §4; PROVISIONAL pin):** L-BFGS-B via `scipy.optimize.minimize`, analytic gradients, objective = **mean per-trial NLL**, ftol 1e-10, **absolute gtol 1e-8** on the mean NLL (RDPP V-8), maxiter 1,000, maxfun 15,000, maxcor 10, maxls 20; three deterministic restarts from type-1 order statistics of the fitted partition; converged iff integer status 0 and all values finite; lowest mean NLL, ties to the lowest restart index; single-threaded BLAS asserted. **Library pin PROVISIONAL: scipy 1.18.1 / numpy 2.5.4, UNVERIFIED for the run environment; confirmed at freeze.** scipy is not installed in the box's system python and was not installed for this file.
- **Dose calibration (P-8, RDPP V-2):** **n_dc = 9** seeds per dose-calibration replicate, R_cal,dose = 50. Under the NC2 rule (AM-3) and analytic scalar references, only network cells can need it: **B1 maximum 72,009,000 trials** (≤ 7 network cells × 50 × 4,572 × 9 × K_dc, K_dc = 5 placeholder). 154,305,000 is the looser 15-cell envelope. The fall from WL's 1,148,715,000 comes from n_dc 67 → 9; the NC2 rule removes the scalar cells. **K_dc PENDING.**

## 6. Cost (E50-5; WL superseded where stated)
The ledger (WL) supersedes V25 §8.2's stale terms (13 cells, ×(g − 1) scaling, 2·d_h²-only network cost, unspecified bootstrap, uncounted lines). This section updates WL with the rulings above: G = 1 (g ≤ 2), n_c = 101, n_q = 1,000, restarts = 3 (F = 36), CV not run, hysteresis scheduled (h = 1), n_dc = 9 with B1 ≤ 72,009,000.
- **Scheduled trials (exact):** **4,005,072,000 + 45,720,000·n_seed*** → **7,068,312,000 at 67**, **4,416,552,000 at 9** (15 / 20 cells; RD26 §1.4 and CE50a1 R2 reproduce).
- **Off-total lines at n = 67:** null-centre runs 72,417,000 and null-quantile runs 717,000,000 (20 steps each); dose calibration 0 to 72,009,000; hysteresis 27,828,000 trial-equivalents; fits 55,656,000 (φ_c = 1) to 70,819,200 (φ_c = 3); dip tests 6,184,000 (frozen-table p-values); bootstrap 3.09e+10–1.86e+12 ops; KATs and fixtures negligible.
- **CPU-h (UNVERIFIED):** **≈ 815 to ≈ 85,860 at n_seed* = 67** (≈ 4,499 at the V25 illustrative network point d_h = 256, κ_net = 1); **≈ 510 to ≈ 54,227 at 9**. **Maximum-cost envelope ≈ 103,038 CPU-h** (adds per-test simulated dip p-values). The network lines dominate and scale with d_h²·κ_net (d_h PENDING, P4).

| Line (per-unit envelopes as WL §1.2) | Low, 67 | d_h 256, 67 | High, 67 | Max | Low, 9 | High, 9 |
|---|---|---|---|---|---|---|
| A trials: scalar | 105.3 | 105.3 | 15,792.5 | 15,792.5 | 65.5 | 9,826.0 |
| A trials: network | 208.9 | 3,341.9 | 53,470.1 | 53,470.1 | 131.1 | 33,573.5 |
| B1 dose calibration | < 0.1 | < 0.1 | 1,174.6 | 1,174.6 | < 0.1 | 1,174.6 |
| B2a null-centre runs (n_c) | 3.3 | 52.7 | 843.7 | 843.7 | 2.1 | 529.8 |
| B2b null-quantile runs (n_q) | 32.6 | 522.1 | 8,353.7 | 8,353.7 | 20.5 | 5,245.2 |
| B3 hysteresis sweeps | 1.2 | 13.6 | 272.7 | 272.7 | 0.8 | 170.9 |
| C1 fits incl. mixture fitting | 463.8 | 463.8 | 5,901.6 | 5,901.6 | 289.8 | 3,674.4 |
| C3 dip p-values | < 0.1 | < 0.1 | < 0.1 | 17,177.8 | < 0.1 | < 0.1 |
| C4 seed-level bootstrap | < 0.1 | < 0.1 | 51.5 | 51.5 | < 0.1 | 32.2 |
| D1-D2 KATs, fixtures, root solves | < 0.1 | < 0.1 | < 0.1 | < 0.1 | < 0.1 | < 0.1 |
| **Total (UNVERIFIED)** | **≈ 815** | **≈ 4,499** | **≈ 85,860** | **≈ 103,038** | **≈ 510** | **≈ 54,227** |

- **Maximum-cost accounting:** budgets and per-ledger caps (P5) are set against the scheduled maximum (n_seed* = 67, full GRID Σ = 292, 15 calibration cells); cap-limited work is "INCOMPLETE, never passed" (M L368). These CPU-h figures are not bounds; caps need u from an authorized S0 preflight.
- **Early stopping: NOT ADOPTED. The full grid governs** (R1; M L2784; A44 L108; D56). The full-grid cost is the expenditure (A50 L84). A later amendment could adopt it only by explicitly superseding the full-grid rule, keeping maximum-cost accounting, and reporting later points as NOT RUN BY DESIGN, together with Astra's A50 L74–L82 requirements (WL §3). It is not adopted now.

## 7. Named pre-data amendments under A-2026-10-24
| # | Name | Supersedes / departs from | New rule (pre-data) | Source |
|---|---|---|---|---|
| AM-1 | **ROW0-FL** | M L3422 ("stays in every denominator as a non-success") for the GA-1 false-licence screens | Quota-shortfall INCOMPLETE (M L2009) → row 0: pr_i = 0, kept in the 200; outside S_cons; adverse in numerator and denominator of the binding S_wc; any licence → row FAIL | §1; CE50e1 E1-5; RDPP V-14 |
| AM-2 | **ΔLL-HO** | MP L69 ("from 5-fold cross-validation over trials within a seed") | ΔLL held-out on the final partition after per-seed fitting on the fitting partition; CV not run; three anti-leak pins | §5; PP §8; RDPP V-3 |
| AM-3 | **NC2 ceiling redefinition** | CNA2 L297 ("Clip ceiling as a quantile of the unclipped output distribution") | Type-1 p-quantile of the 9 noise-free grid readouts, per t_r, frozen in hex; bitwise pre-nonlinearity fixture | §3; RDPP V-1 |
| AM-4 | **Scalar-plant t_s = 0** | M L1127 ("t_s = 5τ in plants") and the plant clause of M L1129 | Scalar plants reset analytically, t_s = 0, x_ref = x_lo; 5τ/20-step settling and the tolerance apply to networks only | §3; V25 §6.1 |
| AM-5 | **RAND-INIT dose-0 drop** | CNA2 L242 (a dose-0 sanity level for each specificity row) | No RAND-INIT dose-0 cell (g_0 → 0 is degenerate, not confound-off); required doses kept | §2; E2-7; RD26 SC-1 |
| AM-6 | **NC2r demoted to descriptive** | NC2r as a required validation row (CNA2 L187; V25 R5) | Validation role withdrawn; confirmation-only, descriptive, REPORTED; no claim from other rows | §2; RD26 SC-2 |
| AM-7 | **LIM in calibration** | V25 R5 / L174 ("LIM OUT, conditional") | IGN-LIM/0, /1 join C_cal (15 cells) with fixture (A) and end-to-end validation (B) | §2; CE50a1 R2 |
| AM-8 | **S_cons and S_wc thresholds** | ER1 E1 / E2-3 (reported worst-case rate; 4b-share cap) | New pre-data binding thresholds for both screens: point ≤ 0.05 **and** one-sided 95% CP upper ≤ 0.08 (the M L1965 conditions); cap withdrawn | §1; A50 L35–L41 |
| AM-9 | **100-iteration float64 bisection** | E2-2's fixed-point iteration from x = 0 | Bisection, exactly 100 iterations, no early exit, with assertions (i′)–(viii) and S_max = 8 | §3; CE50 §2.3; CE50e1 E1-1 |
| AM-10 | **n_q ≥ 199 construction requirement** | RD26 L202 (n_q ≥ 100) and CE50a1 R4 (n_q ≥ 99) | n_q < 199 → construction failure | §4; CE50e1 E1-6; RD26c2 §3 |
| AM-11 | **r_q = 991** | A50 L125 ("Use the 990th ordered distance"); RD26 L22 (⌈0.99·n_q⌉) | r_q = ⌈0.99·(n_q + 1)⌉ = 991 at n_q = 1,000; event "coverage < 0.97" = 5.6601e-06 | §4; RD26c2 §2–§4 |

Each is put to Astra in #51 Q2 for accept/reject. AM-8 is also in Q1, AM-9 in Q4, AM-10 and AM-11 in Q3.

## 8. PENDING / open items
| # | Item | Owner | Blocks |
|---|---|---|---|
| PD-1 | **Network Var(w) floor** (proposed (0.01·m₀)²) | CNA, P4 | G-iii for networks |
| PD-2 | **K_dc** (candidate doses per dose-calibration cell; 5 is a placeholder) | CNA/RD, P4 | B1 count |
| PD-3 | **Network width d_h** and the overhead factor κ_net | P4 | network cost lines |
| PD-4 | Fitter library versions (scipy 1.18.1 / numpy 2.5.4, PROVISIONAL, UNVERIFIED for the run environment) | RD, at freeze | fitter pin |
| PD-5 | Pinned libm, float tolerances and hex KATs (σ_ref, x_lo, grids, NC2 ceilings, tanh(8.8)); DOSE0 and null-role KATs | P6, at freeze | KATs |
| PD-6 | BOTTLENECK g_b and Architecture-imposed β values; network dose targets | CNA; RD with CNA (P4) | network cells, B1 |
| PD-7 | Dip p-value method (frozen table assumed) | RD | C3 |
| PD-8 | Per-ledger caps; u from an authorized S0 preflight (Aidan's explicit yes) | P5, Aidan | budgets |
| PD-9 | Astra #51 on Q0–Q6 | Lead → Astra | adoption of every PROVISIONAL item |
| PD-10 | Clean consolidated freeze text | P6(a) | freeze |

## 9. Discrepancies noted this pass
1. **CE50 L40 quote** altered A50 L56 with "remain[s]"; corrected to the verbatim "remain" (CE50e1 E1-3).
2. **CE50e1 and PP header times** (12:35 / 12:30 PM) post-date their file times (both 12:25:29 PM ET, RDPP §0); no content effect.
3. **PP §5 floor multiples** (5.45×, 8.66×) are superseded by RDPP V-4's 5.28–9.05×.
4. **PP §7 B1 attribution**: the fall to 154,305,000 comes from n_dc, not the NC2 rule; the tight maximum is 72,009,000 (RDPP V-2).
5. **WL §1–§2** priced B1 at n_dc = 67 (up to 1,148,715,000), the CV option at ×6, hysteresis as optional and n_c up to 1,001; all are superseded here by P-2, P-8, AM-2 and the hysteresis schedule.
6. **r_q vs A50 L125:** the ruled 991 departs from Astra's 990th (AM-11); disclosed in #51 Q3.
7. **ROW0-FL vs A50 L41 / M L3422:** S_cons keeps the literal L41 denominator; the shortfall enters only S_wc, as adverse; disclosed in #51 Q1–Q2.
8. **RDPP's fitter versions** come from a scratch venv (scipy is not in the box's system python); hence PROVISIONAL.
9. The box restart around 12:11 PM ET voided CNA's earlier CE50 write (hash b195df02…, CE50 L4). All the hashes below verify on disk now.
10. No hash or footer failed to verify.

## 10. Governing file list (whole-file sha256 and footer recomputed this pass; all MATCH)
| Abbrev | Role | Path | Whole-file sha256 | Footer |
|---|---|---|---|---|
| A50 | Astra #50 raw reply | `astra_consult50_response.txt` | `59e93cfffa8f9755262cf4736c4e8158b45064acb8348fb3d813ebc1b4d314c3` | — (no footer) |
| V25 | v2.5 consolidated | `review/trackB_freezeprep_v2_5_consolidated_Lead.md` | `d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5` | `36dbcb5f48c7e21ab572af6da5cce63548f54f4b30403955f6d5fb9d8631e0c0` |
| ER1 | v2.5 erratum 1 | `review/trackB_freezeprep_v2_5_erratum1_Lead.md` | `10860e98444d31c0f432b44f44427b1a522add744d42dd65ce38e20c5c349c2a` | `4d51b00cdb17a4bc86b2dc0863a8264113c7e38d9cdf1ae706382f8294249511` |
| E2 | v2.5 erratum 2 | `review/trackB_freezeprep_v2_5_erratum2_Lead.md` | `81bdfcf29ad81ac20b4effbdb8434664d82b67e0f96f3f0345504950079f4569` | `c62a3bbf8419a1c205be268380fd6e0cc7ce6aa92060d7efbbded2439dccae79` |
| E2C1 | erratum 2 corr1 | `review/trackB_freezeprep_v2_5_erratum2_corr1_Lead.md` | `c2c839210580f1b037580fd977421fa0cd2faaedb6a3d781ee80741f12cce212` | `62364a219985a9bb3adcb4da5833852d269d1b6bd90587a17215f8b9ac07d9b6` |
| E2C2 | erratum 2 corr2 (superseded by corr3) | `review/trackB_freezeprep_v2_5_erratum2_corr2_Lead.md` | `5100f4de826dacbd422be92e056f58578fc9a5c332353885ebb0f50f62cf8092` | `da5aec39632978c3f318caf1055b602a14560a69b02c7af914c88984b79e1ae0` |
| E2C3 | erratum 2 corr3 (superseded by CE50a1 R1) | `review/trackB_freezeprep_v2_5_erratum2_corr3_Lead.md` | `2f813ba4bb58507241ced0bea97354fdfc63990015786feaadeb4709e4630eec` | `8d420ab1b9fbee4745cedf430b3e9cfc57feb3230617fb290faa40afa0122b2f` |
| WL | Lead E50-5 workload ledger | `review/trackB_freezeprep_v2_6_E50_5_workload_ledger_Lead.md` | `83247be974ce3da79735c0eb28cbb8eb80d476d1d00a07ea43b270bb7e33e5fe` | `39371967c33a3c709e562490fe97cca7f4b3a9a71af3244393a3f8c3a2b1f269` |
| RD26 | RD E50-2/E50-4 | `review/trackB_freezeprep_v2_6_E50_2_E50_4_RD.md` | `8a36920898f8a2aece46189631f4c5592719f0c4e5a566cf5687ba1dbc28fc73` | `c29401c458a408ebd73a93f94c89a91f3a6da2f6464bbee84b1724a95fbc3520` |
| RD26c1 | RD26 corr1 | `review/trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr1.md` | `ebe3a08ceab597d06b9239271ff06ae70804ded9a037bb29a1a023878998d708` | `a43bae6449f461b90062469947ea5511092954524ec7ec768a58d097c5f274e2` |
| RD26c2 | RD26 corr2 | `review/trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr2.md` | `e8bba1b248b3702bdc4f231581a28a0f333d1456420c6d89a53a8e55c3d9addf` | `7ee752014bcb89b3a4a3a85366d6c3fd86a232e68d7d5270ccf87abacb105fbf` |
| RDLP | RD light pass of CE50/CE50a1 | `review/trackB_scope_v3_6_CNA_E50_1_E50_3_lightpass_RD_v1.md` | `2b403bcb162b0c1f9da7776ee47e44b692f83bd4f228000aaaeb73c02a1f5aad` | `80314aa7ed42e55feac20067c5853d1d565e095b1d7bf5b6269e59b7e94d8365` |
| CE50 | CNA E50-1/E50-3 | `review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1.md` | `b5a880ea35a77ae2de47dfd8d9bb2516d9e9b331f96c52ded8e123c780939f97` | `1ebe8c5d4aec7027f97be89a01049fc7b9441d5dddeeea50aafa8b7fc4ba5a2f` |
| CE50a1 | CE50 addendum 1 | `review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1_addendum1.md` | `fdba7c639e9e0deb0d20829ac6e8829d7a0429292d94aa68d6a3540014c6fc7c` | `36a2ad78a43cd553a5b843fd9a94f990d1c7f9bed0773532f3b9288cfc2f9bc7` |
| CE50e1 | CE50 erratum 1 | `review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1_erratum1.md` | `42bf6c6d75380579d6f99643b29b9c9723601867003a5b4d0d51d9cb4e4e1d77` | `fd5b764b5e2a728f6d86e10e1bf97a2640f8e918da827a0983410a1b2184e2e7` |
| PP | CNA pending params | `review/trackB_scope_v3_6_CNA_E50_pending_params_v1.md` | `a1dc190a0583c3e336f10cd1ce4c8449a990a6677c3ca0b42d87f26a8683bdf8` | `0f8d89c0d82a6388776a6d33314749eed2034bbb4e398464d35c7bcf771f37a6` |
| RDPP | RD light pass of PP and CE50e1 | `review/trackB_scope_v3_6_CNA_E50_params_and_erratum1_lightpass_RD_v1.md` | `12371a769217eec9322f36932bcd7b4002d59cb8636f2dcf734d1f175d0df19a` | `ae88a5c7914cf608ab05b133d4ed250f4d8c08b1da7ce5448c47cd90d740974e` |
| M | merged scope v3.6 (unchanged) | `review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` | `bb074b332a3af3563823c4a5bc687bbb3b5db23dcc573991cbe04308a498b6d8` |
| MP | measurement plan v1 (unchanged) | `review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` | — (no footer) |
| CNA2 | CNA v2 half (unchanged) | `review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` | `b666b1d76abe8e526cdc20a404c7cf047ac46823e121a2104636c9d165c68dd1` |
| AMD | amendment record (unchanged) | `review/constitution_amendment_A-2026-10-24_record.md` | `2f29a07a617464e1b0a30ad77ce7c67367f31208e749f6bcbff938fa8f7c2dd6` | `222648af594bd926f28cecb6d6fce9eab8e57c42fa8695371b9992edd3c43e92` |

*DESIGN ONLY. Draft, not frozen. No freeze, execution, benchmark or timing run is requested or authorized. X1–X5 and the claim ceiling unchanged. No host coupling. No consciousness claim is made or implied. Nothing was sent to Astra or anyone else.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 85cc351656baddd047bc52597251d84fdd81d3a74114a1273f438526a1321dd6
