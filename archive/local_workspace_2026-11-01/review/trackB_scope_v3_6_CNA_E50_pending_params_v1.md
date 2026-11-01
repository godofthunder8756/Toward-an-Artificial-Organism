# Track B v3.6 freeze prep: CNA proposals for the E50-2/E50-4 items marked PENDING CNA (n_c, n_q, scalar s grids, s*_LIM, G-iii Var(w) floor, H1 fitter, n_dc, ΔLL method) (CNA v1)

- **Author:** CNA (scope-conformance owner). **Date/time:** 2026-11-01, about 12:30 PM EST (America/New_York, from `date`).
- **Status:** PLANNING/ASSESSMENT ONLY. Nothing run as an experiment, simulation or timing run. Only exact arithmetic, closed forms and SHA-256 (script `/workspace/scratch/cna_e50_13/pp.py`, system `python3`, no random numbers). Additive file; no read-only file is rewritten. X1–X5 unchanged. Astra not contacted. No consciousness claims.
- **Label key:** PROPOSED = CNA proposal for Lead ruling; PENDING = not justifiable before data or owned elsewhere, with what settles it.

## 0. Inputs (sha256 recomputed on disk at 12:21 PM EST)
| Tag | File | sha256 (prefix) | ✔ |
|---|---|---|---|
| RD26 | review/trackB_freezeprep_v2_6_E50_2_E50_4_RD.md | 8a36920898f8… | ✔ |
| RD26c1 | review/trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr1.md | ebe3a08ceab5… | ✔ |
| WL | review/trackB_freezeprep_v2_6_E50_5_workload_ledger_Lead.md | 83247be974ce… | ✔ |
| A50 | astra_consult50_response.txt | 59e93cfffa8f… | ✔ |
| V25 | review/trackB_freezeprep_v2_5_consolidated_Lead.md | d101438d75ae… | ✔ |
| CE50 | review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1.md | b5a880ea35a7… | ✔ |
| CE50a1 | review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1_addendum1.md | fdba7c639e9e… | ✔ |
| M | review/trackB_instrument_validation_scope_v3_6_merged_RD.md | ab80afa56ac1… | ✔ |
| MP | review/trackB_measurement_plan_v1_RD.md (M L143) | 1d5458e3319b… | ✔ |
| CE49a1 | review/trackB_scope_v3_6_CNA_E49_1_E49_3_v1_addendum1.md | 55030ebd7bb7… | ✔ |
Cost baseline (WL L6, L11): scheduled trials **4,005,072,000 + 45,720,000·n_seed*** (|C_cal| = 15, |C_conf| = 20). **No proposal below changes that total.** Changes to off-total lines (B1, C1) are flagged where they occur.
- **Lead rulings reflected (12:23 PM EST):** symbols k_FY (Fisher–Yates index), n_EM (EM step count) and r_q (quantile rank); n_q ≥ 199 is a construction requirement (§2.2). R3 option (b), the binding worst-case screen S_wc, is RULED and recorded in CE50 erratum1 E1-5. It sets no parameter here.

## 1. Scalar plant gains (prerequisite for §3–§4; PROPOSED)
- RD26 L131–L132 leave "nominal g" (P1) and "g < 1" (N1) PENDING CNA. Inside the CE50 L129–L130 domain:
  - **g_P1 = g_LIM = 2.0** (bistable; G = ⌈max(1, g − 1)⌉ = 1; h = 1/100; plant steps per trial 500·G, WL L17; EM step counts n_EM = t_r·100·G in integers, CE50 erratum1 E1-1).
  - **g = 0.5** for N1 and for the graded subunits of NC1, NC2 and NC2r.
- Why: g = 2.0 is the CE50 reference point (CE50 L179: x* = 0.9575040240772688, σ_ref = 0.09575040240772688). It keeps every derived offset inside |θ| ≤ 1 (CE50 L131; §3). g = 0.5 is mid-range in [0, 0.8] (contraction modulus 0.5).
- **Cost:** G = 1 is the WL Low and High assumption (WL L57, L59). No change.

## 2. Network null centre and quantile (E50-4; RD26 L21–L22, L216; WL B2a/B2b L38–L39)
### 2.1 n_c (role `ign-null-centre`): **PROPOSED n_c = 101**
- Odd, so the coordinatewise median is the single order statistic X_(51). No tie or averaging rule is needed (RD26 L21: "n_c odd recommended").
- Validity does not depend on n_c. A50's coverage statement is "Conditional on the fixed center" (A50 L128). The 0.99 coverage of §2.2 therefore holds for any frozen centre, and n_c affects only efficiency (how tight the gate is), not error control.
- Precision (exact, distribution-free, per coordinate): with 101 runs, [X_(41), X_(61)] covers the population median with probability 0.95396 (P[Bin(101, ½) ≤ 40] = 0.02302 per tail).
- **Cost:** WL L38 Low value: U_net × 101 = **72,417,000 runs** of 20 steps. Off-total (B2a). It sits at the ledger's low end; no change.
### 2.2 n_q (role `ign-null-quantile`): **PROPOSED n_q = 1,000**
- A50 L124 names it: "Generate 1,000 independent null runs per applicable seed/network setting".
- Ruled rank (CE50a1 R4; WL L6(c)), symbol **r_q** (Lead ruling; formerly "k"): **r_q = ⌈0.99·(n_q + 1)⌉ = ⌈990.99⌉ = 991**. T = X_(991), with no interpolation. Ties do not matter, because the order-statistic value is unique.
- **Construction requirement (Lead ruling): n_q ≥ 199**, so that r_q ≤ n_q − 1 and T is never the sample maximum (n_q = 199 → r_q = 198; n_q = 198 → r_q = 198 = n_q). n_q < 199 → construction failure. **n_q = 1,000 is well above it** (r_q = 991 = n_q − 9).
- **Coverage** C = F(T) ~ Beta(r_q, n_q + 1 − r_q) = Beta(991, 10), given a continuous distance distribution and a fixed centre (A50 L128):
  - E[C] = 991/1001 = **0.990010** (exact fraction 991/1001).
  - **Event "coverage < 0.97": P(C < 0.97) = P[Bin(n_q, 0.97) ≥ r_q] = P[Bin(1000, 0.97) ≥ 991] = 5.6601 × 10⁻⁶** (exact sum; WL L125 and RD light pass V-5 agree). It is not P(X_(r_q) < 0.99 quantile), which is ≈ 0.457. Astra's rank 990 gives 1.8130 × 10⁻⁵ (A50 L130).
- RD26 L22 (⌈0.99·n_q⌉ = 990) and RD26 L202 (n_q ≥ 100) are superseded by the rulings. RD26 §2.5's coverage text must use r_q = 991, and #51 must tell Astra (WL L125).
- **Cost:** WL L39: **717,000,000 runs** (B2b, off-total). No change.

## 3. Scalar strength grids s_1…s_9 (RD26 L48, L267; MP L62; PROPOSED)
**Analytic anchor (noise-free fold of the bistable plant, τ = 1, f(x) = −x + tanh(g·x + s)).** The lower branch (reset x_lo, CE50 L113–L116) disappears where f = 0 and f′ = 0:
- g·sech²(g·x + s) = 1 ⇒ x_c = −√(1 − 1/g), and s = atanh(x_c) − g·x_c, so
- **s_c(g) = g·√(1 − 1/g) − atanh(√(1 − 1/g))**, for g > 1.
- Larger s ⇒ more ignition, which fixes RD26 L61(c)'s orientation (θ₁ > 0).
- Values (float64, illustrative; the freeze KAT is the hex under the pinned libm, CE50 L154 and L187):

| g | x_c | s_c | hex(s_c) |
|---|---|---|---|
| 1.25 | −0.4472136 | 0.07780516931534398 | 3fb3eb0a21ab4d18 |
| **2.0** | −0.7071068 | **0.532839975353552** | 3fe10d066b84a372 |
| 4.0 | −0.8660254 | 2.147143718212938 | 40012d59af8c4a90 |

- At g = 2 the fold check gives residuals |f| = 1.1e−16 and |f′| = 4.4e−16. Roots, if computed at freeze, use the CE50 §2.3 bisection.

**Grid rule (P1 and all matched scalar rows): s_i = s_c(g_P1)·(i − 1)/4, for i = 1…9.**
- s_1 = 0 is the null input. That is the floor: the noise-free trial stays at x_lo.
- s_5 = s_c is the centre. s_9 = 2·s_c is saturation, at twice the fold.
- Spacing δ = s_c/4. This satisfies MP L62 "≥ 9 levels spanning floor to saturation".
- At g_P1 = 2: δ = 0.133209993838388. **S = (0, 0.13321, 0.26642, 0.39963, 0.53284, 0.66605, 0.79926, 0.93247, 1.06568).** The bound [s_1, s_9] = [0, 1.065679950707104] is fixed with the grid (RD26 L48).

| Row | Grid | Note |
|---|---|---|
| IGN-P1 | S | Noisy finite-t_r transition is near s_c, not exactly at it (§4 caveat) |
| IGN-N1 (g = 0.5) | S (matched) | No transition expected. Graded response over the same inputs |
| IGN-NC1 | S | Subunit thresholds θ = s_c ∓ (Δs/2)·δ for Δs ∈ {2, 4} grid steps. Max \|θ\| = s_c + 2δ = 0.79926 ≤ 1 (CE50 L131) |
| IGN-NC2, IGN-NC2r | S | Clip dose as frozen in the IGN row table; grid shared |
| IGN-LIM | shifted S (§4) | Offset acts on the probe grid, not the null input (CE50 L131) |

- Domain check: the gains of §1 keep every s finite. The CE50 L148 assertions apply unchanged.
- **Cost:** the grid values change no counts (K_s = 9 is already in WL). No change.

## 4. s*_LIM and the LIM offsets (RD26 L106, L145–L146, L268; A50 L92, L95; PROPOSED)
- **s*_LIM := s_c(g_LIM)**, the analytic noise-free fold (§3). At g_LIM = 2.0: **s*_LIM = 0.532839975353552** (hex 3fe10d066b84a372).
- **Dose levels (offsets in grid steps; one on each side, matching RD26 L106 "one point outside on each side"):**
  - **LIM/0:** grid = S − 7δ, so s_9 = s_c − 3δ. The transition lies 3 steps above the grid. Grid (−0.93247 … 0.13321).
  - **LIM/1:** grid = S + 7δ, so s_1 = s_c + 3δ. The transition lies 3 steps below the grid. Grid (0.93247 … 1.99815).
- **Fixture (A):** the predicate "inside iff s_1 ≤ s* ≤ s_9" must return OUTSIDE-HIGH for LIM/0 and OUTSIDE-LOW for LIM/1. Both are exact for the analytic s*_LIM.
- **Caveat (why the margin is 3 steps = 0.39963 in s).** The recursion is the validated object (CE50 L166). Its finite-t_r, noisy π = 0.5 location is not analytic:
  - noise-assisted escape moves it below s_c;
  - critical slowing near the fold moves it above (A50 L117: a nonlinear noisy system "does not generally have an exactly Gaussian stationary distribution").
  - Whether the fitted ŝ* stays outside is exactly what check (B) tests (RD26 L111). It is a validation outcome, not a pre-data guarantee.
- **Cost:** the LIM cells are in calibration (CE50a1 R2), so they are already in the 4,005,072,000 + 45,720,000·n totals. The fixture is a fixed computation (RD26 L106). No change.

## 5. G-iii Var(w) floor (RD26 L76, L269; MP L81, L236 D1)
- **Scalar rows: PROPOSED floor Var(w) ≥ (0.01·Δ_ref)² = 3.6673 × 10⁻⁴** (Δ_ref = 1.9150080481545375, CE50 L179). In SD terms that is 0.0191, one fifth of σ_ref per τ.
- Rationale:
  - D1 (MP L236) means "no write", i.e. collapse. The floor must sit below the pure-noise spread of w, or a working graded negative would read UNAVAILABLE instead of NOT MET.
  - Linearised check, using exact CE50 L179–L181 values for w = |x − x_lo| (half-normal variance (1 − 2/π)·V):
    - N1 at s = 0: V(300) = 0.0087369, so Var(w) = 0.0031748 = **8.66 × floor**.
    - P1 at x_lo: V ≈ 0.0054989, so Var(w) = 0.0019982 = **5.45 × floor**.
  - Near-transition bins have larger Var(w), so only a broken or noise-free write falls below the floor.
  - The same σ_ref holds for every scalar row (CE50 L117), so one floor serves all of them.
- **Networks: PENDING.** The w scale needs the network width and normalisation (P4, d_h ABSENT, WL L17). Proposed rule for ruling: floor = (0.01·m₀)², where m₀ = median of the n_q null-quantile distances of that (seed, setting). It reuses frozen B2b data and adds no runs. Settled by P4.
- **Cost:** none (no runs).

## 6. H1 (and H0) fitter settings (RD26 L50: "PENDING RD"; MP L65–L66; CNA proposes for RD/Lead adoption)
| Setting | PROPOSED |
|---|---|
| Method | Maximum likelihood by bounded quasi-Newton (L-BFGS-B), with analytic gradients. The same optimizer for H0 and H1 (RD26 L50: "identical … same optimizer, initialisation and restart set") |
| H1 parameters | θ₀, θ₁; μ_lo; μ_hi = μ_lo + e^η (prevents label switching); log σ_lo, log σ_hi. Per c-level where MP L65–L66 require it |
| Bounds | \|θ₁\|·δ ≤ 20 (δ = grid step; networks: (s_9 − s_1)/8). σ_lo, σ_hi ≥ σ_min = 0.01·Δ_ref (scalar; networks 0.01·m₀, PENDING with §5) |
| Convergence | Relative NLL change ≤ 1e−10 over an iteration, or projected-gradient ∞-norm ≤ 1e−8·max(1, \|NLL\|) |
| Max iterations | 1,000 per restart. A restart that has not converged is discarded. If none converges → FIT-FAIL (RD26 L52) |
| Restarts (deterministic) | r0: μ_lo, μ_hi = q10, q90 of w; σ = (q90 − q10)/4; ŝ₀ = s_5. r1: q25/q75, ŝ₀ = s_3. r2: q5/q95, ŝ₀ = s_7. In each, θ₁ = 4/(s_9 − s_1) and θ₀ = −θ₁·ŝ₀. H0: 4PL from per-level medians, log-linear σ from per-level MAD, γ = 0, same three slope/centre variants. Best NLL kept; ties go to the lowest index (RD26 L50) |
| Separation | If the θ₁ bound is active at the optimum, flag **SEPARATED** (reported). ŝ* = −θ₀/θ₁ stays defined, so G-i applies as written. A σ bound active → flag **DEGENERATE-COMPONENT** (reported); the fit stands |
| Randomness | **None.** No RNG role. If one were ever needed, it would be a new named role, not reuse of any existing one (CE49a1) |
| Library/version | PENDING RD (software pin) |
- Restart count 3 sits inside WL C1's "restarts 1–3" (WL L43). **Cost:** at the WL C1 upper value; no change.

## 7. Dose-calibration replicate size n_dc (Lead addition A; M L372–L373; WL L37, L122, O-W3)
- **PROPOSED n_dc = 9 seeds per dose-calibration replicate** (the GRID minimum, WL L11 "at 9"), with R_cal,dose = 50 (M L373).
- Why not n_seed*: dose calibration runs first (M L372–L375), so n_seed* is unknown (WL L122).
- Why the minimum: realization criteria are per-replicate medians across seeds. Those are noisiest at the smallest admissible n. A dose that meets its realization criterion at n = 9 is expected to meet it at every larger GRID n.
  - This is a design rationale, not a proof (no distributional guarantee).
  - The binding protection stays the per-replicate realization check at confirmation (CE50 §1, E5).
- **Which cells:** cells whose dose has a fitted target (network BOTT/ARCH levels "giving" a D target; RD26 L142–L143 PENDING RD/CNA). Scalar cells need none **if** the NC2 clip ceiling is defined on the noise-free recursion. That definition is PROPOSED here; otherwise NC2 joins B1. **K_dc stays PENDING** (candidate set per cell is P4-dependent; WL uses 5).
- **Cost (B1, off-total):** 50 × 4,572 × 9 × K_dc per cell.
  - At K_dc = 5: **10,287,000 trials per cell**.
  - ≤ 7 network cells (WL L37): 72,009,000.
  - All 15 cells: 154,305,000.
  - WL's high end is 1,148,715,000 (n_dc = 67). **This LOWERS the B1 maximum; flagged.**

## 8. ΔLL method (Lead addition B; MP L69; WL L95, L123, O-W6)
- **Recommendation: held-out on the final partition. Fit H0/H1 on fitting slots (positions 0–253 of each (seed, bin)); score per-trial log-likelihood on final positions 381–507.** ΔLL = mean of (ℓ_H1 − ℓ_H0) over the final trials of the seed.
- **Cited reason for departing from MP L69's CV:**
  - M L312 is headed "Nested fitting (no fitting on final-test data)".
  - M L313: "Probes and decoders (… IGN mixture/graded fits) are fit on the fitting partition … Labels use the final partition only."
  - MP L69's 5-fold CV "over trials within a seed" would fit on final trials.
  - M is the later frozen text and lists MP as an input (M L143).
- MP L69's stated purpose ("rather than BIC, to avoid parameter-count arguments") is fully kept, because a held-out likelihood needs no parameter count.
- **Record as A-2026-10-24 pre-data amendment "ΔLL-HO":** MP L69 "from 5-fold cross-validation over trials within a seed" → "held-out on the final partition after fitting on the fitting partition (M L312–L313)". **Cost: C1 unchanged (no ×6).**
- **If the Lead keeps CV (RD's fold pin; fold assignment frozen before any data):**
  - Slots: **fitting positions 0–253 only.** Selection 254–380 (chooses bins/t_r, M L313) and **final 381–507 are in no fold**, so the final read stays clean.
  - Assignment: **deterministic by position, fold(p) = p mod 5**, applied within each (seed, bin). No new RNG role is needed. The keyed Fisher–Yates permutation (index k_FY = 507…1, CE49a1) already makes position independent of slot identity, and existing roles are not reused.
  - Exact sizes per (seed, bin): 254 = 4·51 + 50 → folds 0–3 have **51**, fold 4 has **50**. Per seed (9 bins): **459, 459, 459, 459, 450** (Σ 2,286). Bins are stratified by construction.
  - Statistic: each fitting trial is scored once, by the fit trained on the other four folds. ΔLL_CV is the mean over 2,286 trials and is **REPORTED** (M L313 bars it as a label). The label ΔLL stays the final-partition value. Fits: 5 + 1 = ×6 (WL L95: C1 Max ≈ 35,410 CPU-h vs 5,902), which the Lead places inside the envelope.
  - **Example fold map** (placeholder zero seed, permutation KAT fa85f551…, CE49a1 L24; position p → slot a[p] → fold):

| p | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | … | 253 | 254–507 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| slot a[p] | 79 | 468 | 482 | 332 | 173 | 222 | 63 | 342 | … | a[253] | — |
| fold | 0 | 1 | 2 | 3 | 4 | 0 | 1 | 2 | … | 3 | none |

## 9. Decisions needing the Lead's ruling
| # | Decision | CNA proposal | Cost effect |
|---|---|---|---|
| P-1 | g_P1 = g_LIM = 2.0; graded g = 0.5 | Adopt | none (G = 1) |
| P-2 | n_c = 101 | Adopt | B2a 72,417,000 runs (WL low end) |
| P-3 | n_q = 1,000 (≥ 199 ruled); r_q = 991; P[Bin(1000, 0.97) ≥ 991] = 5.6601e−6 (coverage < 0.97); RD26 L22/L202 updated; #51 note | Adopt | B2b 717,000,000 (no change) |
| P-4 | Scalar grid s_i = s_c·(i − 1)/4; matched across P1/N1/NC1/NC2/NC2r; NC1 θ = s_c ∓ (Δs/2)δ | Adopt | none |
| P-5 | s*_LIM = s_c(g_LIM); LIM offsets ∓7δ (transition 3 steps outside, one level each side) | Adopt | none |
| P-6 | Var(w) floor (0.01·Δ_ref)² scalar; network rule (0.01·m₀)² PENDING P4 | Adopt scalar; rule for network | none |
| P-7 | H1/H0 fitter settings (§6) | Adopt; RD to confirm and pin library | none (restarts = 3) |
| P-8 | n_dc = 9; NC2 ceiling on the noise-free recursion; K_dc PENDING | Adopt | **B1 max falls** to 154,305,000 (K_dc 5, 15 cells) |
| P-9 | ΔLL held-out final (A-2026-10-24 "ΔLL-HO"); CV only as REPORTED with the §8 fold pin, if retained | Adopt held-out | none; CV option ×6 on C1 |
Scheduled-trial totals stay at **4,005,072,000 + 45,720,000·n_seed*** under every proposal.

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 0f8d89c0d82a6388776a6d33314749eed2034bbb4e398464d35c7bcf771f37a6
