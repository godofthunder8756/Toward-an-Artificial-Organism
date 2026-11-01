# Track B v3.6: RD light pass of CNA E50 pending parameters (PP) and CNA E50-1/E50-3 erratum 1 (CE50e1)

- **Author:** Research Delegate (RD). **Written:** 2026-11-01, about 12:27–12:40 PM EST (America/New_York, from `date`).
- **Status:** REVIEW RECORD. DRAFT, NOT FROZEN. Additive; edits no other file. Errors found after locking go in a separate `_corr` file, never a rewrite.
- **Split:** RD closely reviews code paths, RNG, counters, root rule, stop/exit and numerics. RD lightly reviews scope and citations, which CNA owns.
- **Computation:** exact rational arithmetic (Python `fractions`, integer `comb`), mpmath 1.4.1 at 50 digits, SHA-256, and deterministic float64 evaluation of closed forms and of the noise-free recursion under the box's system libm. No RNG, simulation, Monte Carlo, training, calibration or timing run. Scripts: /workspace/scratch/rd_e50_params_lp/chk.py and nc2.py (mpmath/scipy in a scratch venv there; the system python is untouched). System libm is not the pinned libm (P6), so every float value is UNVERIFIED for freeze.
- **Lead rulings taken into account (relayed 12:27 PM EST, all subject to this pass):** (1) ΔLL-HO adopted, CV not run; (2) NC2 clip ceiling on the noise-free recursion adopted provisionally; (3) ROW0-FL confirmed for both counts; (4) network floor, K_dc and fitter library remain PENDING.
- X1–X5 and the claim ceiling are unchanged. No consciousness claim. Astra was not contacted. Nothing was posted or sent.
- **Abbreviations:** PP = CNA pending-params file; CE50e1 = CNA erratum 1; CE50 = CNA E50-1/E50-3 main file; CE50a1 = its addendum 1; A50 Ln = astra_consult50_response.txt (cat -n); M = merged v3.6; MP = measurement plan v1; V25 = v2.5 consolidated; RD26 = my v2.6 E50-2/E50-4 file; WL = Lead's E50-5 ledger; CNA2 = trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md (`17832b01…`).

## 0. Hash verification (recomputed 12:27–12:29 PM EST)

| File | Claimed | Recomputed full sha256 | Footer (bytes above footer line) | Lines | Result |
|---|---|---|---|---|---|
| PP `trackB_scope_v3_6_CNA_E50_pending_params_v1.md` | a1dc190a…, footer 0f8d89c0…, 166 | a1dc190a0583c3e336f10cd1ce4c8449a990a6677c3ca0b42d87f26a8683bdf8 | 0f8d89c0d82a6388776a6d33314749eed2034bbb4e398464d35c7bcf771f37a6 | 166 | **MATCH** |
| CE50e1 `trackB_scope_v3_6_CNA_E50_1_E50_3_v1_erratum1.md` | 42bf6c6d…, footer fd5b764b…, 100 | 42bf6c6d75380579d6f99643b29b9c9723601867003a5b4d0d51d9cb4e4e1d77 | fd5b764b5e2a728f6d86e10e1bf97a2640f8e918da827a0983410a1b2184e2e7 | 100 | **MATCH** |

- Both files are mode `-r--r--r--`. Footer convention checked as in my earlier passes: the footer hash covers every byte through the newline ending the convention line.
- **Timestamps (noted only):** PP's header says "about 12:30 PM EST" and CE50e1's "about 12:35 PM EST". `ls -l --full-time` gives **12:25:29.697847157 EST for both files** (identical to the nanosecond). This matches CNA's disclosure that both were written at 12:25. No content consequence.
- **References (recomputed, all MATCH):** CE50 b5a880ea35a7…; CE50a1 fdba7c639e9e…; my light pass 2b403bcb162b… (236 lines, as CE50e1 L6 states); RD26 8a36920898f8…; RD26 corr1 ebe3a08ceab5…; RD26 corr2 e8bba1b248b3…; WL 83247be974ce…; V25 d101438d75ae…; A50 59e93cfffa8f…; M (`trackB_instrument_validation_scope_v3_6_merged_RD.md`) ab80afa56ac1…; MP (`trackB_measurement_plan_v1_RD.md`) 1d5458e3319b…; CNA2 17832b01de2b….

## 1. Summary of verdicts (EDIT and FAIL first)

**No FAIL.** Eight EDITs, none of which changes a scheduled total.

| # | Item | Verdict | One line |
|---|---|---|---|
| V-1 | NC2 clip ceiling on the noise-free recursion (Lead ruling 2) | **EDIT** | NC2's role is intact and it does not pass trivially *because of* this change, but the ceiling's population, quantile type and t_r dependence must be pinned, and the redefinition of CNA2 L297's dose must be named |
| V-2 | Dose-calibration arithmetic and attribution | **EDIT** | All products exact. The drop 1,148,715,000 → 154,305,000 comes from n_dc 67 → 9 (factor 9/67 exactly), not from the NC2 rule. Under the adopted NC2 rule the tight B1 maximum is 72,009,000 (≤ 7 network cells); 154,305,000 stays valid as the 15-cell envelope |
| V-3 | ΔLL-HO leak checks | **EDIT** | Matches M L312–L313. Three pins needed: fits are per seed; every data-derived start/scale comes from the partition being fitted; Ashman D comes from the fitting-partition fit |
| V-4 | G-iii floor ratio claim | **EDIT** | Floor 3.6673e−4 is exact. "5.4–8.7×" holds only at t_r = 3, and P1 uses the stationary V_c instead of the reset transient. Over t_r ∈ {2, 3, 5}: 5.28–9.05× |
| V-5 | Grid float evaluation order | **EDIT** | Two natural evaluation orders differ in the last ulp at 8 of 27 grid points. Pin one formula with a single rounding; freeze hex KATs |
| V-6 | Erratum (i′) S_max placement | **EDIT** | S_max = 8 is sound, but the check must run over the whole frozen input table at construction, not only where a root is solved |
| V-7 | Erratum (vii) completeness | **EDIT** | As written it can be tautological. Freeze n_EM as literal integers, and add a readout-counter assertion |
| V-8 | Fitter convergence mapping | **EDIT** | CNA's gtol scaled by max(1, \|NLL\|) is not a native L-BFGS-B criterion. Use the mean per-trial NLL as the objective and an absolute gtol. Full pin in §4 (PROPOSED) |
| V-9 | Fold formula s_c(g) | OK | Saddle-node condition and sign verified at 50 digits; values and hex reproduce |
| V-10 | Grid definition | OK | 9 points, step s_c/4, bound [0, 1.065679950707104] |
| V-11 | LIM ∓7δ offsets | OK | Internally consistent: transition exactly 3 steps outside each grid. Max \|u\| 1.99815 ≤ 8 |
| V-12 | n_c = 101, n_q = 1,000, r_q = 991 | OK | Exact |
| V-13 | Erratum root rule (b) x0 key, (c) integer n_EM, (viii) | OK | Correct; one robustness note |
| V-14 | ROW0-FL vs M L3422 and A50 L41 | OK | Consistent as a named, conservative override |
| V-15 | Gains, domains, σ_ref | OK | All inside their domains |
| V-16 | Stop/exit and RNG roles | OK | No stop/schedule quantity enters any input; no role overlap; the fitter and NC2 ceiling use no RNG |
| V-17 | ΔLL CV fold rule | MOOT | One line: CV is not run (Lead ruling 1), so the fold rule is moot. Its arithmetic (51/51/51/51/50) was correct |

## 2. Dedicated item: NC2 under a noise-free clip ceiling (V-1, EDIT)

### 2.1 What NC2 is meant to test (verbatim, with line numbers)
- **MP L87:** "**IGN-NC2 (saturation confound):** a graded unit whose output is clipped at a ceiling, producing a point mass. **Must be NOT MET** on the pre-nonlinearity readout."
- **MP L62:** "w_j is the workspace write magnitude: the L2 norm of the workspace update at the write step, measured on the **pre-nonlinearity** value as well as the post-nonlinearity value, so that output saturation can't create bimodality."
- **M L314:** "w = ‖x_ws(t_0 + t_r) − x_ref‖, read pre-nonlinearity (primary; post-nonlinearity REPORTED), common to IGN-P1, every IGN confound row and the network instrument."
- **CNA2 L186:** "| IGN-NC2 (saturation, feedforward) | Confound, specificity | Clipping after the readout point | Pre-nonlinearity bimodality | Not MET on the pre-nonlinearity readout |"
- **CNA2 L297 (dose and realization):** "| IGN-NC2 (feedforward) | Clip ceiling as a quantile of the unclipped output distribution | {0.8, 0.6} quantile | Point mass at the ceiling: post-nonlinearity dip and D | Post-nonlinearity D ≥ 2 | Var(w) floor: the pre-nonlinearity w keeps variance by construction |"
- **V25 L164:** "| IGN-NC2 | scalar plant | clip quantile {0.8, 0.6} (2) | IN | 2 | **yes** (no clip, PROPOSED) |"
- **M L373** (why a fitted dose needs calibration): "**Dose calibration (CNA v3 §8.3):** R_cal,dose = 50 replicates per plant that needs a fitted reference or κ_f." **M L1139:** "Every analytic imitation reference stays analytic."

**Reading.** NC2 is a specificity row. Its confound is real (a point mass at the ceiling makes the *post*-nonlinearity readout look bimodal: realization target "post-nonlinearity D ≥ 2"). Its known answer is NOT MET on the *pre*-nonlinearity readout, because the clip sits after the readout point (feedforward). What NC2 actually certifies is that the instrument reads w before the clip and does not mistake saturation for ignition.

### 2.2 Does a noise-free ceiling change what NC2 detects, or let it pass trivially?
- **Pre-nonlinearity readout: unchanged by any ceiling.** In a feedforward clip the state trajectory x does not depend on the ceiling c, so the pre-nonlinearity w is the same random variable for every c (including dose 0, "no clip"). This was already true under the noisy-quantile definition. NC2's NOT MET therefore never depended on how c is computed, and the noise-free definition does not make it easier. The "trivial" aspect is inherent in MP L87's design: NC2 tests the readout path, not the mixture statistics. The noise-free change adds no new triviality.
- **Post-nonlinearity realization: this is where the definition matters.** "Post-nonlinearity D ≥ 2" (CNA2 L297) is what makes the confound real. It is evaluated per replicate on realized data and stays binding (CE50 §1, E5 realization). A dose that fails it is insufficient support → UNRESOLVED, never PASS (A50 L47–L48). So no ceiling definition can make NC2 PASS without the confound being present.
- **What changes is the meaning of the dose label.** CNA2 L297 defines the ceiling as "a quantile of the unclipped output distribution", which is a property of the noisy plant (hence a fitted reference under M L373). A noise-free ceiling is a deterministic function of the frozen constants (no RNG, no calibration replicates), which is why scalar cells leave B1. But "quantile 0.8" then no longer means "20% of unclipped trials are clipped".
  - Example (float64, system libm, g = 0.5, h = 1/100, x_0 = 0, grid S of PP §3; EXAMPLE ONLY): the noise-free readouts x(t_r) at s_1…s_9 are, at t_r = 3, (0, 0.20245, 0.38026, 0.52243, 0.63049, 0.71097, 0.77064, 0.81499, 0.84810). The type-1 quantiles of these 9 equally weighted values are x(s_8) = 0.81499 (p = 0.8, index ⌈0.8·9⌉ = 8) and x(s_6) = 0.71097 (p = 0.6, index 6).
  - The top-level gaps are 0.033–0.080, smaller than the per-trial noise SD at N1 (√V ≈ 0.093 at t_r = 3, §3.4). So the realized clipped fraction will differ from 0.2 / 0.4. I do not estimate it here (that would need simulation).
  - The ceiling depends on t_r: x(s_8) = 0.72368, 0.81499, 0.86831 at t_r = 2, 3, 5. t_r is chosen on the selection partition (M L313, M L376), so the ceiling must be frozen per t_r.

### 2.3 Required edits (V-1)
1. **Population and quantile type.** Freeze: c_p(t_r) = the type-1 (inverse-ECDF, no interpolation) p-quantile of the 9 equally weighted noise-free readouts x_nf(s_i, t_r) of the frozen recursion (same h, n_EM, x_0 = x_lo, σ = 0), with index ⌈p·9⌉ computed in exact rationals. Any other population (for example, weighted by eligible trials) must be named instead.
2. **Per t_r.** Freeze c_p(t_r) for every t_r ∈ {2, 3, 5} and dose p ∈ {0.8, 0.6} as float64 hex under the pinned libm (P6 KAT list). The selected t_r picks the frozen value; nothing is computed from data.
3. **Clip is post-readout only.** The clip is applied to the reported post-nonlinearity output and never re-enters x (that would be NC2r, CNA2 L187).
4. **Code-path fixture (PROPOSED).** Under one placeholder key, run the NC2 plant with and without the clip and assert the pre-nonlinearity w sequences are **bitwise identical**. Any difference → construction failure. This turns "clipping after the readout point" into a checked property.
5. **Name the change.** CNA2 L297's "quantile of the unclipped output distribution" → "type-1 quantile of the noise-free grid readouts". This is a pre-data dose redefinition. I recommend recording it under A-2026-10-24 and naming it in #51 with ΔLL-HO and ROW0-FL.
6. **Keep realization binding.** State explicitly that the post-nonlinearity D ≥ 2 realization check stays per replicate and binding, and that its rate is measured in calibration (C_cal includes NC2/0 and NC2/1).

With 1–6, NC2's role is intact. **Verdict: EDIT.**

## 3. Close checks

### 3.1 Fold formula (V-9, OK)
- For x = tanh(g·x + s), a saddle-node needs F = x − tanh(g·x + s) = 0 and F′ = 1 − g·sech²(g·x + s) = 0. Then tanh²(g·x + s) = 1 − 1/g, and with x = tanh(·), x_c² = 1 − 1/g. The lower stable branch folds at **x_c = −√(1 − 1/g)**, s = atanh(x_c) − g·x_c, i.e. **s_c(g) = g·√(1 − 1/g) − atanh(√(1 − 1/g))**, for g > 1.
- **Sign:** s_c > 0 for g > 1, and increasing s pushes toward x_hi. Root count at g = 2 (mpmath): 2 negative roots at s_c − 10⁻⁶ and 0 at s_c + 10⁻⁶, so the lower branch vanishes at **+s_c**, as PP L50 says. The upper branch folds at −s_c, which is irrelevant for resets at x_lo.
- **Values (50 digits; float64 hex):** s_c(1.25) = 0.077805169315343976605 (3fb3eb0a21ab4d18); **s_c(2) = 0.53283997535355202357** (3fe10d066b84a372); s_c(4) = 2.1471437182129378784 (40012d59af8c4a90). All three hex values match PP L55–L57. Residuals of f and f′ at the fold are ≤ 6e−51.
- **Bound:** s_9 = 2·s_c = **1.065679950707104**, so [0, 1.06568] is confirmed.

### 3.2 Grid (V-10, OK) and evaluation order (V-5, EDIT)
- s_i = s_c·(i − 1)/4 for i = 1…9 gives **9 points**, step **δ = s_c/4 = 0.133209993838388**, s_1 = 0, s_5 = s_c, s_9 = 2s_c. That meets MP L61's "≥ 9 levels". K_s = 9 = B_req (RD26 L48).
- **V-5 (EDIT):** in float64, computing grid points as fl(s_c·m)/4 versus fl(s_c·(i−1))/4 + o·fl(s_c/4) gives different last bits at 8 of the 27 points over offsets o ∈ {−7, 0, +7}: (i, o) = (2,−7), (3,−7), (5,−7), (6,−7), (7,−7), (9,−7), (4,+7), (7,+7).
  - Pin: **s_{i,o} = fl(s_c·m)/4 with integer m = i − 1 + o** (division by 4 is exact, so there is one rounding). Apply the same rule to NC1: θ = δ·m_θ with m_θ ∈ {3, 5} (Δs = 2) and {2, 6} (Δs = 4), and to u = s − θ as fl(s_c·(m − m_θ))/4.
  - Freeze every grid value as hex. Fixture outcomes are unaffected (3δ margins), but bit-identity across implementations is not otherwise guaranteed.

### 3.3 s*_LIM and the LIM offsets (V-11, OK)
- LIM/0 = S − 7δ = (−7δ … +δ) = (−0.93247 … 0.13321). s_9 = δ = s_c − 3δ, so the transition s_c = 4δ is **exactly 3 steps above** the grid.
- LIM/1 = S + 7δ = (7δ … 15δ) = (0.93247 … 1.99815). s_1 = 7δ = s_c + 3δ, so the transition is **exactly 3 steps below** the grid.
- Consistency with the grid length: the unshifted grid spans 0…8δ with the transition at 4δ, so a 7-step shift puts the nearer grid end at 8δ − 7δ = δ (LIM/0) or 0 + 7δ = 7δ (LIM/1), i.e. 4δ ∓ 3δ. Each grid still has 9 points and one fixture point outside on each side is available (RD26 L106). In float64 both strict inequalities (LIM/0 s_9 < s_c; LIM/1 s_1 > s_c) hold.
- Fixture (A) returns OUTSIDE-HIGH / OUTSIDE-LOW exactly for the analytic s*_LIM. The noisy finite-t_r location is a validation outcome (PP L84–L87; RD26 L111). That is correctly stated, not a pre-data guarantee.
- **S_max:** max |u| over S, LIM/0, LIM/1 and NC1 (θ ∈ {2δ, 3δ, 5δ, 6δ} plus θ = 0) is **1.99815** (LIM/1 s_9). NC1 alone peaks at 1.06568. Everything is ≤ S_max = 8 with a margin of 4.0037×. The NC1 max |θ| = 6δ = 0.79926 ≤ 1 (CE50 L131).

### 3.4 G-iii Var(w) floor (V-4, EDIT)
- **Δ_ref = 2x\*** with x\* the positive root of x = tanh(2x): x\* = 0.95750402407726874, **Δ_ref = 1.9150080481545375** (CE50 L179). σ_ref = Δ_ref/20 = 0.095750402407726874. Floor (0.01·Δ_ref)² = **3.6672558 × 10⁻⁴**, so 3.6673e−4 is confirmed. SD floor/σ_ref = 0.2 exactly, as PP L91 says.
- **Variance algebra.** Linearised EM from the exact reset y_0 = 0: V(n_EM) = σ²h(1 − a^(2·n_EM))/(1 − a²), with a = 1 − hλ and h = 1/100 (G = 1). With mean-zero Gaussian y, w = |y| has Var(w) = (1 − 2/π)·V (half-normal). λ_N1 = 0.5 at s = 0; λ_P1 = 1 − 2(1 − x\*²) = 0.8336279122483257.

| t_r | N1 V(n_EM) | N1 Var(w)/floor | P1 V(n_EM) | P1 Var(w)/floor |
|---|---|---|---|---|
| 2 | 0.0079534595 | 7.8809 | 0.0053279288 | **5.2793** |
| 3 | 0.0087369491 | **8.6572** | 0.0054855858 | 5.4355 |
| 5 | 0.0091299599 | **9.0467** | 0.0055206782 | 5.4703 |

- PP's N1 figure (V(300) = 0.0087369, 8.66×) reproduces exactly. PP's P1 figure uses V ≈ 0.0054989, which is the SDE stationary V_c = σ²/(2λ), not the EM reset transient. That gives 5.4488×, not the t_r-matched value.
- **Edit:** restate as "linearised, pure noise sits **5.28–9.05×** above the floor over t_r ∈ {2, 3, 5} (P1 at t_r = 2 is the minimum)", and use V(n_EM) for both rows. The conclusion (floor well below pure-noise spread) is unchanged. These are first-order figures (A50 L117), not guarantees for the nonlinear plant.
- Network floor (0.01·m₀)²: PENDING P4 (Lead ruling 4). Not reviewed further.

### 3.5 ΔLL-HO (V-3, EDIT) and the CV fold rule (V-17, MOOT)
- **V-17:** CV is not run (Lead ruling 1), so the fold rule is moot. Its arithmetic (254 = 4·51 + 50 → 51/51/51/51/50; selection and final slots in no fold) was correct.
- **Governing text, verbatim:**
  - **M L312:** "**5.2 Nested fitting (no fitting on final-test data).** Every instrument uses three frozen, disjoint partitions at the level of **independent episodes/trajectories** … "Fitting probes, subspaces and donor rules. Selecting optimization settings and comparator candidates. Final evaluation on untouched episodes and donor pairs.""
  - **M L313:** "Probes and decoders (Q-EXIST, SELF observers, S-INT audit, BCAST subspaces, IGN mixture/graded fits) are fit on the fitting partition. Hyperparameters, IGN transition bins, comparator candidates, probe orientation and the optimized BCAST comparator … are chosen on the selection partition. Labels use the final partition only. "Bootstrap the paired final comparisons; do not optimize inside the final test set.""
  - **MP L69:** "1. ΔLL: held-out log-likelihood per trial, H1 minus H0, from 5-fold cross-validation over trials within a seed. Cross-validation is used rather than BIC, to avoid parameter-count arguments."
- **Match.** Fitting H0/H1 on positions 0–253 and scoring per-trial log-likelihood on positions 381–507 is exactly M L313's "fit on the fitting partition … Labels use the final partition only". MP L69's purpose (no parameter count) is kept. MP's 5-fold CV over all trials within a seed would fit on final trials, which M L312's heading forbids. PP's citation (M L143 lists MP as an input) is correct. The amendment is properly named.
- **Partition counts:** 254 + 127 + 127 = 508 per (seed, bin). There are 9 × 127 = **1,143** final trials per seed and 2,286 fitting trials per seed.
- **Leak check (code path).** Nothing in PP's text puts final data into a fit, but three things are not yet pinned:
  1. **Unit of fit.** PP L130 says "Fit H0/H1 on fitting slots (positions 0–253 of each (seed, bin))" and "mean … over the final trials of the seed". It should say explicitly that H0 and H1 are fitted **per seed** on that seed's 2,286 fitting trials. MP L69 is "within a seed", and the seed is the inferential unit (M L310). Pooled fits would couple seeds.
  2. **Data-derived starts and scales.** The restart starts in PP §6 (q10/q90, q25/q75, q5/q95 of w; per-level medians and MAD for H0) must be computed from **the partition being fitted only**: fitting slots for the ΔLL fits, selection slots for the G-i ŝ\* fit (RD26 L50). If they were computed over all trials, final-partition values would enter the fit through x0. σ_min = 0.01·Δ_ref is a frozen constant, so that is fine.
  3. **Ashman D.** MP L71's D = √2·|μ_hi − μ_lo|/√(σ_hi² + σ_lo²) must be computed from the per-seed **fitting-partition** H1 parameters. A refit on the final partition would be "fitting on final-test data" (M L312). The dip test (MP L70) is a test on final-partition w, not a fit, so it is fine.
- The H1 fit for ŝ\* on selection slots (RD26 L50) and the ΔLL fits on fitting slots are different fits on disjoint partitions. Both use the same frozen fitter (§4), and neither touches final data. **Verdict: EDIT (pins 1–3).** CV cost ×6 no longer applies; C1 is unchanged.

### 3.6 Erratum 1 root rule (V-6, V-7 EDIT; V-13 OK)
- **(a) S_max = 8 (value OK).** The largest bracket argument is |u| + g ≤ 8.8. 1 − tanh(8.8) = 4.54409 × 10⁻⁸ ≈ 2.046 × 10⁸ × 2⁻⁵², against the box saturation point 19.061547465398498 (box float64: tanh(19.061547465398498) == 1.0 and tanh(prev float) ≠ 1.0, reproduced). The margins 4.0037× and 9.54× reproduce. 2⁻³⁰ = 9.31 × 10⁻¹⁰ < 4.54 × 10⁻⁸, so the P6 check tanh(8.8) < 1 − 2⁻³⁰ is a sound KAT. F(∓1) signs at u = ±8, g = 0.8 are as stated.
- **V-6 (EDIT, placement):** (i′) is written as a replacement for assertion (i)'s s-clause in the root rule, but CE50e1 L29 says bistable rows solve roots only at u = 0, and probe inputs never go through a root solve. As placed, |u| > S_max on a probe input would never be checked. Make (i′) a **construction-time sweep over the full frozen table** {(row, dose, grid value, θ)}, plus a check at every root call.
- **(b) x0 key (V-13, OK).** "x0 := 0 iff u = s − θ = 0 exactly" is correct by oddness and uniqueness for graded g. For NC1 at the null input, u = −θ ≠ 0, so x_lo is bisected. With V-5's integer-index rule, u = 0 iff m = m_θ, so the float equality is exact and implementation-independent.
- **(c) Integer n_EM (V-13, OK).** G by float comparisons (G = 1 if g ≤ 2; 2 if 2 < g ≤ 3; 3 if 3 < g ≤ 4) equals ⌈max(1, g − 1)⌉ on the domain. n_EM = t_r·100·G ∈ {200G, 300G, 500G}. The hazard is real: box float64 3/(1/300) = 899.9999999999999 → int 899.
- **V-7 (EDIT):** (vii) "n_EM, computed in integers, equals the frozen table value" is tautological if the table is produced by the same expression. Pin: (vii-a) the table entries are **literal integers in the freeze record**, written independently of the code; (vii-b) **new: at readout, the integer step counter equals n_EM**, and the readout is taken after exactly n_EM updates (no off-by-one between "after step n" and "at step n"). Otherwise, construction failure.
- **(viii) (OK).** 0 < hλ < 2 at every frozen x0 holds: h ≤ 1/100 and λ ∈ (0, 1] for g ≥ 0 (graded λ ∈ [1 − g, 1]; P1 λ = 0.8336 at x_lo). Asserting it is cheap and correct.
- **Completeness otherwise:** (ii)–(vi) of CE50 L149–L153 are unchanged and still apply. With (i′) swept per V-6 and (vii-b) added, I find no remaining unchecked code path in the root and step-count logic.

### 3.7 Dose calibration (V-2, EDIT)
- Exact: 50 × 4,572 × 9 × 5 = **10,287,000** per cell; × 7 = **72,009,000**; × 15 = **154,305,000**. WL's high value 50 × 4,572 × 67 × 5 × 15 = **1,148,715,000** reproduces, and 1,148,715,000 × 9/67 = 154,305,000 exactly.
- **Attribution edit.** The fall from 1,148,715,000 to 154,305,000 is caused entirely by n_dc 67 → 9. The NC2 rule does not enter it: 154,305,000 still assumes all 15 required-dose cells. Under the adopted NC2 rule, and with every other scalar reference analytic (M L1139), the scalar cells need no dose calibration. So the **tight B1 maximum is 72,009,000 (≤ 7 network cells, WL L37)**. 154,305,000 stays a valid (looser) 15-cell envelope. Both figures assume WL's placeholder K_dc = 5, which stays PENDING (Lead ruling 4).
- **Lead's question:** "the dose-calibration maximum is 154,305,000" is **verified as the 15-cell envelope** at n_dc = 9, K_dc = 5. Under the adopted NC2 rule the reachable maximum is 72,009,000.
- **Scheduled totals.** B1 is off-total (WL L37), so **4,005,072,000 + 45,720,000·n** is unchanged. That is 7,068,312,000 at n = 67, reproduced.
- **RNG addressing (OK, note).** No new role is needed. Dose-calibration replicates are separated by the address field "replicate set" (V25 L129) under existing roles. M L372 requires a dedicated stream per role set ("never reused across roles"). PP should state the replicate-set tag and seed indices 0…8 for n_dc = 9.
- **n_dc = 9 rationale:** "a dose that meets its realization criterion at n = 9 is expected to meet it at every larger GRID n" is labelled as design rationale, not proof (PP L120). Realization stays binding at confirmation. OK as worded.

### 3.8 n_c and n_q (V-12, OK)
- n_c = 101 is odd, so each coordinate's median is the single order statistic X_(51) of that coordinate. Note that the median *vector* generally mixes runs across coordinates, which is fine for a coordinatewise centre. P[Bin(101, ½) ≤ 40] = 0.023022 per tail, so [X_(41), X_(61)] covers the population median with probability 0.953956, as PP L34 states. U_net = 72,417,000/101 = 717,000 exactly.
- r_q = ⌈0.99·1001⌉ = ⌈990.99⌉ = **991**. 1,000 ≥ 199 and r_q = n_q − 9. E[C] = 991/1001 = 0.990010.
- P[Bin(1000, 0.97) ≥ 991] = **5.660070 × 10⁻⁶**; at rank 990 it is 1.812991 × 10⁻⁵ (A50 L130: "approximately 0.00001813"); P[Bin(1000, 0.99) ≥ 991] = 0.457301. All reproduce. The event wording "coverage < 0.97" matches A50 L128 ("covers less than 97% of that same null distribution").
- Validity independent of n_c: correct, given the centre runs (`ign-null-centre`) and quantile runs (`ign-null-quantile`) are distinct roles (RD26 L23), so the centre is independent of the quantile sample.

### 3.9 ROW0-FL (V-14, OK)
- **M L3422** (verbatim): "Stage-0 rows: the affected replicate is INCOMPLETE; it stays in every denominator as a non-success (non-MET for power, non-event for FID-DET, ineligible for eligibility floors); if the row cannot meet its rule as a result it is UNRESOLVED".
- **A50 L41** (verbatim): "(d) Yes: the conservative denominator is n4+n4b+n5. The >=36 rule concerns that assessment's denominator; 36 permits acceptance only with a sufficiently small adverse count. Row-0 licences remain immediate failures."
- **Ruled reading:** a shortfall counts 0 in the realization tally and stays in the 200; it is out of S_cons; it counts as adverse in both the numerator and denominator of S_wc; any licence in it → row FAIL.
  - Realization: "non-success" in the 200 is exactly M L3422. **Consistent.**
  - S_cons: literal A50 L41 denominator (n4 + n4B + n4U + n5, with 4b split into 4B/4U). Exclusion departs from M L3422's "every denominator", which is why it is named. **Consistent as named override.**
  - S_wc: counting the replicate as adverse, rather than as M L3422's "non-event", is the conservative direction. A50 L35 supports a binding worst-case screen at the same thresholds ("require it to satisfy the frozen point <= 0.05 and CP upper <= 0.08 conditions"). **Consistent.**
  - Licence → FAIL matches A50 L41's last sentence and CE50 §1.4 step 1. **Consistent.**
- **Exact re-check:** CP one-sided 95% upper bounds: 8/188 → 0.07547 (point 0.0426, PASS); 9/200 → 0.07721 (PASS); 10/200 → 0.08334 (FAIL); 20/200 → 0.14199 (FAIL). So "largest passing count at 200 is 9" (CE50e1 L68) reproduces, and S_wc maps the 8/188 example back to 20/200 → FAIL. S_wc ≥ S_cons holds because (a + x)/(b + x) ≥ a/b whenever a ≤ b.
- The C-AV n ≥ 36 rule on S_cons's denominator is unchanged. That is fine, because S_wc's denominator is never smaller. #51 must disclose the departure from A50 L41, as CE50e1 L80 says.

### 3.10 Gains, domains, σ_ref (V-15, OK)
- g_P1 = g_LIM = 2.0 ∈ [1.25, 4]; graded g = 0.5 ∈ [0, 0.8] (CE50 L129–L130). G = 1, h = 1/100.
- σ_ref = 0.05·2x\* over the bistable domain ranges from 0.0710412 (g = 1.25) to 0.0999326 (g = 4). σ_ref(2) = 0.0957504 lies in **[0.0710, 0.0999]**.

### 3.11 Stop/exit and RNG (V-16, OK)
- Early stopping is not adopted (WL). n_c, n_q, n_dc, the grids, the floor, the fitter settings and the NC2 ceilings are frozen constants. None is computed from a stop count, executed-stop log, schedule position or n_seed\*. No stop or schedule quantity enters any policy, value or selection input in either file.
- Roles: `ign-trial`, `ign-partition`, `ign-null-centre`, `ign-null-quantile` are distinct (V25 L117–L124; RD26 L23). The fitter uses no RNG (PP L112). The NC2 noise-free ceiling uses none. CV folds would have used none, and are now moot. Dose calibration reuses roles under a distinct replicate-set address field (§3.7 note). **No role overlap.**

## 4. Fitter pin (PROPOSED; library left PENDING with RD by PP L113)

Everything in this section is **PROPOSED**. Versions are **UNVERIFIED for the run environment** (P6). The fitter applies identically to the G-i ŝ\* fit (selection partition) and the ΔLL fits (fitting partition, per seed), for both H0 and H1 (RD26 L50).

| Setting | PROPOSED value |
|---|---|
| Software | Python 3.13.5 (box), **numpy == 2.5.4** (box system install, `pip show numpy`), **scipy == 1.18.1**. **scipy is not installed in the box's system python** (`pip show scipy`: "Package(s) not found"). 1.18.1 is what pip resolved today into a scratch venv alongside numpy 2.5.4; threadpoolctl 3.7.0 likewise. Record `numpy.show_config()`, the scipy wheel's bundled OpenBLAS version and the libm at freeze. Any version change is a re-freeze |
| Call | `scipy.optimize.minimize(fun, x0, jac=True, method='L-BFGS-B', bounds=B, options={'maxiter': 1000, 'maxfun': 15000, 'ftol': 1e-10, 'gtol': 1e-8, 'maxcor': 10, 'maxls': 20})`. `fun` returns (objective, analytic gradient) in float64. No `eps` (no finite differences), no callback, `workers` not set |
| Objective | **Mean per-trial NLL** over the fitted trials (NLL/N). This makes scipy's absolute gtol correspond to CNA's scale-relative intent (V-8): L-BFGS-B's ftol test is (f_k − f_{k+1})/max(\|f_k\|, \|f_{k+1}\|, 1) ≤ ftol, and its gtol test is max_i \|proj g_i\| ≤ gtol. Computed in log space (log-sum-exp for the mixture; log-densities directly), so it is finite on the bounded domain. A non-finite objective or gradient is a construction failure (M L3421), never retried |
| Converged | `res.status == 0` and every value finite. Status 1 (iteration/evaluation limit) or 2 (abnormal line-search termination) → restart discarded. Key on the integer status, not `res.message` text. No converged restart → FIT-FAIL (RD26 L52) |
| H1 parameters and bounds | Order frozen: (θ₀, θ₁, μ_lo, η, log σ_lo, log σ_hi), μ_hi = μ_lo + e^η (PP L106). θ₁ ∈ [−20/δ, +20/δ] (PP L107; symmetric so G-i's θ₁ ≤ 0 → NONINCREASING can still fire). θ₀, μ_lo: unbounded. **η ≥ log σ_min** (components at least σ_min apart). log σ_lo, log σ_hi ≥ log σ_min, upper unbounded. σ_min = 0.01·Δ_ref (scalar); networks PENDING with the floor |
| H0 parameters and bounds | 4PL (lower, upper, slope, centre) with \|slope\|·δ ≤ 20. σ(s) is log-linear, **parametrised by its endpoint values ℓ_1 = log σ(s_1) and ℓ_9 = log σ(s_9)**, each ≥ log σ_min. This makes σ(s) ≥ σ_min on the whole grid with box bounds only. Skew shape as frozen by CNA (MP L66), unbounded; a runaway ends as status 1/2 and is discarded |
| Restarts (deterministic, no RNG) | CNA's r0/r1/r2 (PP L110) adopted, with: every quantile is a **type-1 order statistic** w_(⌈p·N⌉) of the **partition being fitted**, with the index computed in integers (no library interpolation). σ start = max((q_hi − q_lo)/4, σ_min); η start = log(max(q_hi − q_lo, σ_min)). Starts are projected onto the bounds explicitly (scipy 1.18.1 also clips x0, but this does not rely on it). H0 starts as PP L110, also from the fitted partition only |
| Tie-break | Recompute the objective once at each converged restart's returned x with the frozen objective. Keep the **lowest mean NLL** (float64 comparison); on exact equality, the **lowest restart index** (r0 < r1 < r2) |
| Threads | Before importing numpy: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `BLIS_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`. At start, assert with `threadpoolctl.threadpool_info()` that every reported pool has `num_threads == 1`; otherwise construction failure. On this box the default is 8 threads per OpenBLAS pool, and with the variables set it reports 1. Fits run one per process; no parallelism inside a fit |
| SEPARATED | At the selected optimum, θ₁ is **bound-active**: \|θ₁ − b\| ≤ 1e−9·max(1, \|b\|) for b = ±20/δ. REPORTED. ŝ\* = −θ₀/θ₁ stays defined, and G-i applies as written (PP L111) |
| DEGENERATE-COMPONENT | At the selected optimum, any of log σ_lo, log σ_hi or η is bound-active at its lower bound (same tolerance). REPORTED; the fit stands (PP L111). For H0, ℓ_1 or ℓ_9 bound-active → H0-FLOOR (REPORTED) |

- Restart count 3 sits inside WL C1's "restarts 1–3", so there is no cost change. maxiter 1,000 is PP's. ftol 1e−10 is PP's. gtol 1e−8 is PP's on the mean-NLL scale. maxcor 10 and maxls 20 are the scipy defaults, frozen explicitly so that a default change cannot move them.

## 5. Items for the Lead / CNA

1. **CNA (V-1):** pin the NC2 ceiling (type-1, 9 equally weighted noise-free readouts, per t_r, hex KAT), add the bitwise pre-nonlinearity fixture, and name the CNA2 L297 dose redefinition under A-2026-10-24 and in #51.
2. **CNA/Lead (V-2):** reword the B1 attribution. The drop is from n_dc; the tight maximum under the adopted NC2 rule is 72,009,000; 154,305,000 is the 15-cell envelope. K_dc stays PENDING.
3. **CNA (V-3):** per-seed fits; starts from the fitted partition only; D from the fitting-partition fit.
4. **CNA (V-4):** restate the floor ratio as 5.28–9.05× (linearised, t_r ∈ {2, 3, 5}, V(n_EM) for both rows).
5. **CNA (V-5):** single-rounding grid formula with integer index; hex KATs.
6. **CNA (V-6, V-7):** sweep (i′) over the full frozen table; literal-integer n_EM table and the readout-counter assertion (vii-b).
7. **Lead (V-8, §4):** adopt or amend the PROPOSED fitter pin; library stays PENDING until then.
8. **RD (own file):** RD26 §2.5 coverage text and L202 were already superseded by my corr2 (`e8bba1b2…`). Nothing new is owed from this pass.

*REVIEW RECORD. Nothing was run or timed beyond deterministic formula and noise-free recursion evaluation. X1–X5 and the claim ceiling unchanged. No consciousness claim.*
---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: ae88a5c7914cf608ab05b133d4ed250f4d8c08b1da7ce5448c47cd90d740974e
