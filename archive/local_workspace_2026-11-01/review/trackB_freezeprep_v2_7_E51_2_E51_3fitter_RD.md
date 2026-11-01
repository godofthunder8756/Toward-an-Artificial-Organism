# Track B freeze preparation v2.7: E51-2 (LIM fixture vs stochastic transition; non-locatable selection fits) and E51-3 fitter half (bounds, restarts, termination, failure handling) (RD)

- **Author:** Research Delegate (RD). **Written:** 2026-11-01, 13:13 EST (America/New_York, from `date`: "Sun Nov  1 13:13:16 EST 2026"); locked at the time shown by `ls -l` on this file.
- **Status:** DESIGN/TEXT ONLY. DRAFT, NOT FROZEN. Additive file; edits no other file. Errors found after locking go in a separate `_corr` file, never a rewrite. A51 L191: "no freeze, execution or timing run is authorized."
- **Lane:** RD owns E51-2 in full and the fitter half of E51-3 (Lead assignment, room 2026-11-01). CNA owns E51-1 and the plant half of E51-3 (CE51). The Lead owns E51-4 (LDG).
- **Computation (no simulation, no RNG, no fitting run, no timing):** exact rationals (`fractions`), mpmath 1.4.1 at 50 digits (closed forms, root-finding on formulas, a certified-bracket fixed point, and evaluation of the **noise-free (σ = 0)** recursion, the same class of deterministic evaluation as RDPP §2.2 and CE51 §8), float64 evaluation of the same noise-free recursion under the box libm (UNVERIFIED for P6), and a float64-vs-50-digit gradient comparison on a synthetic input built by formula. Scripts: `/workspace/scratch/rd_e51_2/lim.py`, `fx.py`, `grad.py` (scratch venv of `/workspace/scratch/rd_e50_params_lp/venv`; system python untouched). scipy 1.18.1 source was **read only** (`scipy/optimize/_lbfgsb_py.py`, sha256 `61b69554f33a210284d4ae3de7da282152f9302b428eeb16984498b54e381d57`); the optimizer was not run.
- X1–X5 and the claim ceiling unchanged. No consciousness claim. Astra not contacted. Nothing posted or sent.
- **Labels:** PROPOSED = RD text for the Lead (or CNA, where marked) to adopt or amend. PENDING = not settled, owner named. UNVERIFIED = depends on the run environment or pinned libm (P6).
- **Abbreviations:** A51 Ln = `astra_consult51_response.txt` (cat -n). A50 Ln = Astra's **#50** reply `astra_consult50_response.txt`. V26 = v2.6 consolidated; C51 = #51 body; PP = CNA pending params; CE50 / CE50e1 = CNA E50-1/E50-3 file / erratum1; CE51 / CE51c1 = CNA E51-1/E51-3-plant file / corr1; RDPP = my params light pass; RD26 / RD26c2 = my v2.6 E50-2/E50-4 file / corr2; RDLP2 = my v2.6 consolidated light pass v2; LDG = Lead's v2.7 E51-4 ledger; WL = Lead's E50-5 ledger; M = merged v3.6; MP = measurement plan v1; δ = s_c/4 (grid step); NL = non-locatable.

## 0. Hash verification (recomputed 12:59–13:13 EST; all MATCH)

| Tag | File (review/ unless noted) | Whole-file sha256 | Footer check |
|---|---|---|---|
| A51 | astra_consult51_response.txt (13,893 B) | `f7f35ec21d37fc98478dc3597d43d4333a72edee606dd00ff5acb33086772463` | no footer; size 13,893 B MATCH |
| V26 | trackB_freezeprep_v2_6_consolidated_Lead.md | `ff03eb81c158e1306df0aaf2127d6191c81f80e11838231345749dd88e0de4c6` | 85cc3516… (as filed) |
| C51 | /workspace/astra_serve51/c51_body.md | `4ea8d7cc64223e7c28ce07c509d6e9eae5bab7fdc772e153da117acda8903415` | — |
| PP | trackB_scope_v3_6_CNA_E50_pending_params_v1.md | `a1dc190a0583c3e336f10cd1ce4c8449a990a6677c3ca0b42d87f26a8683bdf8` | 0f8d89c0… |
| CE50e1 | trackB_scope_v3_6_CNA_E50_1_E50_3_v1_erratum1.md | `42bf6c6d75380579d6f99643b29b9c9723601867003a5b4d0d51d9cb4e4e1d77` | fd5b764b… |
| CE50 | trackB_scope_v3_6_CNA_E50_1_E50_3_v1.md | `b5a880ea35a77ae2de47dfd8d9bb2516d9e9b331f96c52ded8e123c780939f97` | 1ebe8c5d… recomputed MATCH |
| RDPP | trackB_scope_v3_6_CNA_E50_params_and_erratum1_lightpass_RD_v1.md | `12371a769217eec9322f36932bcd7b4002d59cb8636f2dcf734d1f175d0df19a` | ae88a5c7… |
| RD26 | trackB_freezeprep_v2_6_E50_2_E50_4_RD.md | `8a36920898f8a2aece46189631f4c5592719f0c4e5a566cf5687ba1dbc28fc73` | c29401c4… recomputed MATCH |
| RD26c1 | trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr1.md | `ebe3a08ceab597d06b9239271ff06ae70804ded9a037bb29a1a023878998d708` | — |
| RD26c2 | trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr2.md | `e8bba1b248b3702bdc4f231581a28a0f333d1456420c6d89a53a8e55c3d9addf` | 7ee75201… recomputed MATCH |
| RDLP2 | trackB_freezeprep_v2_6_consolidated_lightpass_RD_v2.md | `77a889b36cde79f3e46e2e972c803422a5a4674ead9381aef7ccc5e1e16fb72a` | 5165b5c4… recomputed MATCH |
| CE51 | trackB_scope_v3_6_CNA_E51_1_E51_3plant_v1.md (198 lines) | `bc27d6959e904a07b1dc441f2ddca46617c1a2a5d5e6e2db6c3a2fde4e708ea5` | `3444c7bfe9bbcfc4c5eeab25a9e9715102c15ee214ba76244ab11933d4f917dd` recomputed MATCH |
| CE51c1 | trackB_scope_v3_6_CNA_E51_1_E51_3plant_v1_corr1.md (13 lines) | `b83b9e04f0aaa7aaa584c5ad56ebd4b0248372cf8246641fee5b572df538f0ff` | `bc3a7f1d9da334d22cec4d98bee2a7d5bf4c35b111e42b878f849abfa7f92ed0` recomputed MATCH |
| LDG | trackB_freezeprep_v2_7_E51_4_ledger_completion_Lead.md (183 lines) | `ccdcda05181f9445040ff37d642e67f09bfacd844d35ddac0eeadda6bcb8699b` | `d1c09ef54dbb4d59cb54c147d25cde7bd7b8eae15a3fc0525112bced70d6dd51` recomputed MATCH |
| WL | trackB_freezeprep_v2_6_E50_5_workload_ledger_Lead.md | `83247be974ce3da79735c0eb28cbb8eb80d476d1d00a07ea43b270bb7e33e5fe` | — |
| M | trackB_instrument_validation_scope_v3_6_merged_RD.md | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` | — |
| MP | trackB_measurement_plan_v1_RD.md | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` | no footer |

Footer convention as in my earlier files: the footer hash covers every byte through the newline that ends the convention line.

## 1. Summary

| # | Item | Result |
|---|---|---|
| S-1 | **Finding (blocks the current LIM claim):** with the frozen offset +7, the **noise-free** finite-time transition of LIM/1 lies **inside** the LIM/1 grid at t_r = 2 | s_nf(2) = 1.0600926655859691 = 7.958δ; LIM/1 s_1 = 7δ. Margin −0.958δ (inside). t_r = 3: +0.416δ; t_r = 5: +1.568δ. "3 steps outside" holds only for the t → ∞ fold s_c (§2.3) |
| S-2 | Noise-free LIM gate fixture FX-LIM defined on the recursion, hex-pinned (§2.2, §2.4) | LIM/0 passes at every t_r with a proven margin ≥ 3δ = 0.39963 (actual finite-time margins 4.43–6.96δ). LIM/1 at +7 **fails** at t_r = 2. **PROPOSED (CNA owns plant parameters): LIM/1 offset +11** → margins 3.042δ / 4.416δ / 5.568δ; max \|u\| = 2.531 ≤ S_max = 8; no count changes |
| S-3 | Stochastic claim: **choice (b)**, with (a) as optional evidence | A rigorous EM-recursion bound exists for LIM/0 only: P(trial ever leaves the low basin within n_EM) ≤ 2.04e−4 / 3.23e−4 / 8.12e−4 at the top LIM/0 point (t_r = 2/3/5), ≤ 4.2e−6 at every other LIM/0 point. For LIM/1 the elementary bounds are uninformative (0.42–1.00). Neither bound speaks to the fitted ŝ\* (§3) |
| S-4 | Non-locatable selection fit (PI-SSTAR-NL) defined: 7 causes NL-1…NL-7 (§4.1) | Row outcomes mapped; never PASS; FAIL only via row-0 licence or screen violation; counted **once per replicate**; LIM carve-out keyed by frozen row ID; reverse hedge closed (§4.2–§4.5) |
| S-5 | ŝ\* per (t_r, readout): the governing text is silent; PROPOSED default **one fit per (t_r, readout, c-config)**, every-fit rule (§4.6) | F2 = **666,000 calls** (φ_c = 1) / **846,000** (φ_c = 3), independent of n_seed; reproduces LDG F2's worst case |
| S-6 | Fitter pin completed (§5): bounds in hex, restarts by exact formula, termination from scipy 1.18.1 source, failure mapping, gradient fixture, KAT | Gradient fixture prototype: worst relative error 8.0e−16 (float64 analytic vs 50-digit central difference) |
| S-7 | L-E2 (GA-1 accrual through M L2819–L2820) | **NOT CONFIRMED** as the text stands; mapping text PROPOSED (§6.1) |
| S-8 | CNA decision table vs fitter mapping | Consistent after three edits; two conflicts flagged (§5.6) |
| S-9 | **Second finding (CNA/Lead):** IGN-P1's own grid S puts the noise-free t_r = 2 transition at 7.958δ, **0.042δ below s_9** | Under the EDGE cause and the every-fit rule, P1 power at t_r = 2 is at risk. Must be resolved before calibration (§4.7) |

---

# Part A. E51-2

## 2. Requirement and the deterministic gate fixture

### 2.1 What Astra requires (verbatim)
- A51 L6: "| E50-2 | NOT CLOSED | LIM is correctly restored to validation, but its asserted transition location is not established by shifting the grid away from zero. |"
- A51 L112–L123: "The LIM offset requires more than a grid-index argument. / If the nine centered nodes are m = -4,...,4, shifting by +7 gives: / [0.75*s_c, 2.75*s_c] = approximately [0.39963, 1.46531]. / That interval contains the positive spinodal s_c = 0.53284. A low-attractor reset breaks the symmetry that might otherwise suggest a transition centered at zero. The finite-time, noisy mixture transition estimated by H1 need not be zero or equal to the spinodal. / Therefore, "three steps outside" establishes that zero is outside the shifted grid. It does not establish that the relevant fitted transition is outside. / The deterministic fixture can test what the gate does when supplied an outside location. It cannot establish that the stochastic LIM plant generates that location. Supply the corresponding construction argument, or revise the existing LIM parameters and claims before calibration."
- A51 L141: "The selection-partition H1 used for s-hat* also needs explicit handling of theta1 = 0, component non-identifiability and unsuccessful fits. Those cases are non-locatable; they are not finite outside-grid estimates."
- A51 L185: "E51-2. Separate the LIM gate fixture from the stochastic plant's transition claim. Establish or revise the asserted outside-grid construction, and define non-locatable selection fits explicitly."

**Reading note (grid geometry).** The frozen rule (PP L61, L81–L82; V26 L58–L59) is s_{i,o} = fl(s_c·m)/4, m = i − 1 + o, i = 1…9: the unshifted grid runs 0…8δ, not centred at zero. So LIM/1 = S + 7δ = [7δ, 15δ] = [1.75·s_c, 3.75·s_c] = [0.93247, 1.99815], and LIM/0 = [−7δ, δ]. Astra's interval [0.75·s_c, 2.75·s_c] comes from a centred-node reading. Under the frozen rule the analytic fold s_c = 4δ is **not** inside LIM/1. **Astra's conclusion still stands, for a different reason (S-1):** at finite t_r the noise-free transition moves above s_c, and at t_r = 2 it enters LIM/1.

### 2.2 FX-LIM: the gate fixture on the noise-free recursion (PROPOSED; replaces RD26 L106's "(A)" analytic-only fixture)
> **Object.** The frozen EM recursion with σ = 0: x_{k+1} = x_k + h·(−x_k + tanh(g·x_k + s)), g = 2, h = 1/100, x_0 = x_lo = −x\* (CE51 §6; A51 L98–L100), n_EM ∈ {200, 300, 500} literal integers for t_r ∈ {2, 3, 5} (V26 L53 (vii)). Float64 under the pinned libm, one implementation order (CE51 §8 formula order).
> **Noise-free class.** For each LIM dose d ∈ {LIM/0, LIM/1}, each t_r and each of its 9 grid points: class = HI iff x_nf(s, t_r) ≥ 0, else LO. The threshold 0 is the unstable middle root of the reset map at u = 0 (CE51 L126), i.e. w = |x − x_lo| = x\* = Δ_ref/2, the midpoint between the two reset-input attractors.
> **Expected.** LIM/0: LO at all 27 (point, t_r) pairs. LIM/1: HI at all 27. The (A) predicate checks of RD26 L106 (s_1, s_9, one inside point, one point outside each side, plus the analytic s_c) are kept.
> **Outcome.** All 54 classes and all predicate checks match → FIXTURE-PASS. Any mismatch → FIXTURE-FAIL = construction failure **B-BUILD** (CE51 L40): the LIM row is not built, so it is UNRESOLVED (NOT BUILT), never PASS (CE51 §5 step 2).
> **Robustness assertion.** min |x_nf| over the 54 evaluations must exceed 10⁻⁶ (PROPOSED), so that a last-bit libm difference cannot flip a class; otherwise B-BUILD.
> **Cost.** 2 × 9 × (200 + 300 + 500) = **18,000** noise-free steps, once, off-total. No RNG.

### 2.3 Proof and margins
**Facts used (exact, from the closed form and monotonicity).**
1. The map T_s(x) = x + h·f_s(x), with f_s(x) = −x + tanh(g·x + s), has T_s′(x) = 1 − h + h·g·sech²(g·x + s) ≥ 1 − h > 0. So T_s is strictly increasing in x, and also in s. Hence x_nf(s, t_r) is non-decreasing in s for every n_EM (induction), and **the noise-free finite-time transition s_nf(t_r) := inf{s : x_nf(s, t_r) ≥ 0} is well-defined and unique**.
2. For s < s_c(2), f_s has a lower stable root x_L(s) < 0 (the fold formula, RDPP §3.1). A monotone 1-D map started on one side of a fixed point never crosses it. If x_lo ≤ x_L(s) (0 < s < s_c), the orbit rises to x_L(s) and stays ≤ x_L(s) < 0. If x_lo > x_L(s) (s ≤ 0), then f_s < 0 on (x_L, x_M) with x_M > 0, or on (x_L, ∞) when s < −s_c, so the orbit falls and stays ≤ x_lo < 0. At s = s_c the lower root is x_c = −√(1/2) < 0, with the same argument. **So x_nf(s, ·) < 0 for every s ≤ s_c and every n_EM: s_nf(t_r) > s_c for every t_r.**

**LIM/0 (offset −7).** Its top point is δ = s_c − 3δ. By fact 2 every LIM/0 point is LO at every t_r, and the guaranteed margin is **s_c − δ = 3δ = 0.399629981515164** (absolute) for all t_r. The actual finite-time margins s_nf(t_r) − δ are below. The upper-branch fold −s_c = −4δ lies inside LIM/0, but under a low reset the orbit never visits the upper branch (fact 2), so it has no noise-free effect. Under noise see §3.

**LIM/1 (offset +7, as frozen).** For s > s_c there is no root below the upper one, so the orbit rises. Fact 1 gives a unique s_nf(t_r). It was computed by bisection on s (170 halvings, 50 digits) on the noise-free recursion, using fact 1:

| t_r (n_EM) | s_nf(t_r) (50-digit, 17 sig.) | (s_nf − s_c)/δ | LIM/0 margin s_nf − δ | LIM/1 (+7) margin 7δ − s_nf | LIM/1 (+11, PROPOSED) margin 11δ − s_nf |
|---|---|---|---|---|---|
| 2 (200) | 1.0600926655859691 | 3.958 | 6.958δ = 0.92688 | **−0.958δ = −0.12762 (INSIDE)** | 3.042δ = 0.40523 |
| 3 (300) | 0.87701826570546710 | 2.584 | 5.584δ = 0.74381 | 0.416δ = 0.05545 | 4.416δ = 0.58826 |
| 5 (500) | 0.72357136067554556 | 1.432 | 4.432δ = 0.59036 | 1.568δ = 0.20890 | 5.568δ = 0.74170 |

- Cross-check (float64, box libm): FX-LIM classes are LO×9 at every t_r for LIM/0. For LIM/1 at +7, **t_r = 2 gives "LHHHHHHHH"** (x_nf(7δ) = −0.40254, so FIXTURE-FAIL) and t_r = 3 and 5 give all HI (min |x_nf| 0.2700 and 0.8861). At +11, all HI at every t_r (min |x_nf| 0.5525 / 0.8325 / 0.9754). These agree with the 50-digit values.
- **Consequence.** PP L81–L82's "the transition lies 3 steps below the grid" is true only of the t → ∞ fold. For the recursion actually run (CE50 L166; V26 L56), the noise-free transition is inside LIM/1 at t_r = 2 and 0.42δ outside at t_r = 3.
- **PROPOSED revision (CNA owns the LIM parameters; Lead rules):** LIM/1 offset **+11** (grid 11δ…19δ), so that s_1 ≥ max_t_r s_nf(t_r) + 3δ. The smallest integer start index meeting "+3δ" is 11 at t_r = 2 (10 at t_r = 3, 9 at t_r = 5). LIM/0 stays −7. The new grid max is 19δ = 2.5309898829293718 ≤ S_max = 8 (CE50e1 (i′) sweep still passes). No cell, replicate or trial count changes. The asymmetry (−7 vs +11) is justified by the finite-time drift, which delays ignition only. The alternative, keeping +7 and dropping t_r = 2 for LIM only, would need a per-row t_r grid, which no text provides. I do not recommend it.

### 2.4 FX-LIM hex pins (float64; box libm; **UNVERIFIED for P6**; recomputed at freeze)
- g = `4000000000000000`; h = 1/100 = `3f847ae147ae147b`; s_c = `3fe10d066b84a372`; x_lo = `bfeea3df7aa66894`; σ = 0 for the fixture only.
- LIM/0 grid (m = −7…1): `bfedd6cb3c281e08` `bfe99389a146f52b` `bfe550480665cc4e` `bfe10d066b84a372` `bfd99389a146f52b` `bfd10d066b84a372` `bfc10d066b84a372` `0000000000000000` `3fc10d066b84a372`.
- LIM/1 grid at +7 (m = 7…15; as frozen): `3fedd6cb3c281e08` `3ff10d066b84a372` `3ff32ea738f537e0` `3ff550480665cc4e` `3ff771e8d3d660bd` `3ff99389a146f52b` `3ffbb52a6eb78999` `3ffdd6cb3c281e08` `3ffff86c0998b276`.
- LIM/1 grid at +11 (m = 11…19; PROPOSED): `3ff771e8d3d660bd` `3ff99389a146f52b` `3ffbb52a6eb78999` `3ffdd6cb3c281e08` `3ffff86c0998b276` `40010d066b84a372` `40021dd6d23ceda9` `40032ea738f537e0` `40043f779fad8217`.
- The 54 x_nf readouts are frozen as hex at freeze, as KATs alongside CE51 §8's 27 NC2 readouts. A second, independent implementation must agree bitwise (as CE51 L180).

## 3. The stochastic transition claim

### 3.1 Why shifting the grid cannot establish the noisy location
- With σ = σ_ref > 0 the EM increments are Gaussian with unbounded support. **Every grid point has a nonzero per-trial probability of either outcome** at every t_r. There is no "location" in the deterministic sense, only a mixing curve π(s) that H1 fits (MP L66).
- Its π = 0.5 point depends on t_r (S-1 shows that even the noise-free crossing moves by 2.5δ between t_r = 2 and 5) and on σ: noise-assisted escape lowers it and critical slowing near the fold raises it (PP L84–L86).
- The fitted ŝ\* is then a statistic of finite data on the selection partition (RD26 L50), with its own sampling spread.
- Hence no grid-index argument (A51 L112) and no noise-free fixture (A51 L123) establishes where the **fitted** transition falls. At most, an analytic bound can show that the per-trial switching probability is negligible across a whole grid.

### 3.2 Option (a): rigorous bound for the discrete recursion
**Object** (CE50 L166; V26 L56): x_{k+1} = x_k + h·f_s(x_k) + σ·√h·ξ_k, ξ_k i.i.d. N(0, 1), x_0 = x_lo, σ = σ_ref = 0.09575040240772688, h = 1/100, g = 2, k = 0…n_EM − 1.

**Theorem (LIM/0 escape bound).** Fix s with s < s_c and a level b with x_L(s) < b ≤ b_inf(s) := (−atanh(√(1 − 1/g)) − s)/g and f_s(b) < 0. Let κ := −f_s(b)/(b − x_L), α := κ(2 − hκ)/(2σ²), and τ := min{k : x_k > b}. If x_lo ≤ b then
  P(τ ≤ n) ≤ exp(α·[(x_lo − x_L)² − (b − x_L)²]) · (1 − hκ)^(−n).

*Proof.*
- (i) Write r(x) := −f_s(x)/(x − x_L) = 1 − g·(chord mean of sech²(g·y + s) over [x_L, x]).
  - For y ≤ b_inf, g·y + s ≤ −atanh(√(1/2)) < 0, so sech² increases in y. On (x_L, b] r therefore decreases, with minimum r(b) = κ. On (−∞, x_L), r ≥ 1 − g·sech²(g·x_L + s) = λ_L ≥ κ.
  - Also r ≤ 1 < 1/h. Then T(x) − x_L = (x − x_L)(1 − h·r(x)), so |T(x) − x_L| ≤ (1 − hκ)·|x − x_L| for all x ≤ b.
- (ii) Let W(x) = exp(α(x − x_L)²), m = T(x) − x_L, v = σ²h. The exact Gaussian identity gives E[W(x_{k+1}) | x_k = x] = (1 − 2αv)^(−1/2)·exp(α·m²/(1 − 2αv)). By the choice of α, 1 − 2αv = (1 − hκ)². With (i), this is ≤ (1 − hκ)^(−1)·W(x) for every x ≤ b.
- (iii) So M_k = W(x_{k∧τ})·(1 − hκ)^(k∧τ) is a non-negative supermartingale and E[M_n] ≤ W(x_lo). On {τ ≤ n}, x_τ > b > x_L gives M_n ≥ exp(α(b − x_L)²)·(1 − hκ)^n. Markov's inequality gives the bound. ∎

Any admissible b gives a valid bound. b was scanned over 400 points of (x_L, b_inf], and the best was at b = b_inf. x_L(s) was found by root-finding and certified by a strict sign change of f_s at x_L ± 10⁻⁴⁰. The asserted 0 < κ ≤ λ_L held at every point.

| LIM/0 point s | x_L(s) | b | κ | Bound, t_r = 2 | t_r = 3 | t_r = 5 |
|---|---|---|---|---|---|---|
| +1δ (s_9) | −0.9413079 | −0.5072918 | 0.46039 | **2.04e−4** | **3.23e−4** | **8.12e−4** |
| 0 | −0.9575040 | −0.4406868 | 0.51550 | 8.78e−7 | 1.48e−6 | 4.14e−6 |
| −1δ | −0.9686898 | −0.3740818 | 0.56007 | 1.38e−9 | 2.41e−9 | 7.40e−9 |
| −2δ | −0.9766723 | −0.3074768 | 0.59718 | 7.95e−13 | 1.45e−12 | 4.80e−12 |
| −3δ … −7δ | −0.98249 … −0.99421 | −0.24087 … +0.02555 | 0.62867 … 0.71846 | ≤ 1.74e−16 | ≤ 3.26e−16 | ≤ 1.15e−15 |

(Bounds are rounded up at the last digit shown.)

**Assumptions (every one is needed):**
- (A1) the ξ_k are exactly i.i.d. standard normal (the pinned Gaussian transform of the `ign-trial` stream is modelled as exact; finite-precision and PRNG effects are outside the bound);
- (A2) real-arithmetic recursion (float64 rounding not modelled);
- (A3) x_0 = x_lo exactly, σ = σ_ref, h = 1/100, n = n_EM literal;
- (A4) the event bounded is "the state exceeds b at some update ≤ n_EM", which contains "the readout is above b" and therefore any switch into the upper basin.

**LIM/1 (non-ignition).** On A = {x_k ≤ y for all k ≤ n}, x_n ≥ x_lo + n·h·m_y + Σ η_k with m_y = min_{z ≤ y} f_s(z) > 0, so P(A) ≤ Φ((y − x_lo − t·m_y)/(σ√t)). At s = 7δ and y = 0, m_y = (s − s_c)/g = 3δ/2 = 0.19981. The bound is **0.99998 / 0.98458 / 0.42303** at t_r = 2/3/5: **uninformative**. The only drift lower bound available to an elementary argument is the bottleneck value, which ignores the faster passage elsewhere. I could not obtain a rigorous informative LIM/1 bound for the discrete recursion, and I do not claim one.

**What (a) does not give, even for LIM/0.** The theorem bounds per-trial switching. It does not determine the fitted ŝ\*: with π ≈ 0 across the whole grid, the H1 fit is expected to be OUTSIDE-HIGH or component-degenerate (NL-3/NL-5/NL-6, §4.1), but that is a property of the estimator on finite data, so it is measured, not proven.

### 3.3 Choice: **(b)**, with (a) as optional evidence
(a) is rigorous only for LIM/0's switching probability and silent on the fitted location. For LIM/1 it is not available. So (a) cannot carry the LIM claim.

**PROPOSED revised claim text (replaces PP L81–L87 and V26 L40/L59 wording):**
> "IGN-LIM's **noise-free** transition of the frozen recursion lies outside each LIM grid at every t_r ∈ {2, 3, 5}. This is checked by FX-LIM (§2.2) with the margins of §2.3, which needs LIM/1 at offset +11. The **stochastic** transition location, and the location the selection-partition H1 fit estimates, are **measured quantities, reported and not asserted**. For LIM/0 the per-trial probability of leaving the low basin within n_EM updates is analytically bounded by ≤ 8.12 × 10⁻⁴ at every grid point and t_r (§3.2, assumptions A1–A4). No such bound is claimed for LIM/1."

**What the selection procedure does with it.**
- (1) Nothing in the instrument reads s_nf, s_c, the margins or the bound. They are construction facts only (no ground-truth leak into G-i; RD26 L102).
- (2) The fitted ŝ\* per (t_r, readout) and the NL cause codes are **recorded and reported** for every LIM replicate, alongside s_nf(t_r).
- (3) The LIM row is validated **only** by RD26 §1.3 (B), the CP lower bound of the correct-UNAVAILABLE fraction ≥ 0.90 (MP L199), scored by §4.4, plus FX-LIM.
- (4) "LIM's transition is outside the grid" never appears as a premise of any other row.

---

## 4. Non-locatable selection fits (PI-SSTAR-NL)

### 4.1 Definition (PROPOSED; extends RD26 L52's IGN-UA-SSTAR causes)
A **selection fit** is one H1 fit of the frozen fitter (§5) on the selection partition of one replicate, pooled across its seeds (RD26 L50), for one (t_r, readout, c-config) (§4.6). It is **non-locatable** if any of the following holds. Every cause that applies is recorded, in this order:

| Code | Condition (all evaluated at the selected restart, §5.5) |
|---|---|
| NL-1 FIT-FAIL | no restart accepted (§5.4). A51 L141 "unsuccessful fits" |
| NL-2 RESTART-DISAGREE | two accepted restarts within τ_f = 10⁻⁹ in mean NLL of the best (PROPOSED) give ŝ\* differing by > δ/2, or different §4.1 classes. This is a flat or ridged likelihood, so the location is not identified |
| NL-3 NONINCREASING | θ₁ ≤ 0, including θ₁ = 0 (A51 L141), so ŝ\* is undefined or of the wrong orientation (RD26 L61(c)) |
| NL-4 θ₁ AT NEGATIVE BOUND | θ₁ within 10⁻⁹ relative of −B_θ (subsumed by NL-3; recorded separately) |
| NL-5 BOUND-ACTIVE (component non-identifiability) | any of μ_lo, η, ℓ_lo, ℓ_hi or θ₀ within 10⁻⁹·max(1, \|bound\|) of either bound (§5.2). This covers a collapsed or merged component (A51 L141 "component non-identifiability") |
| NL-6 OUTSIDE-LOW / OUTSIDE-HIGH | ŝ\* = −θ₀/θ₁ < s_1 or > s_9 (grid convex hull) |
| NL-7 EDGE | s_1 ≤ ŝ\* < s_1 + δ/2 or s_9 − δ/2 < ŝ\* ≤ s_9 (within half a step of an end). This supersedes RD26 L54's "If ŝ\*_c = s_9 the pair is (s_8, s_9)" |

- A fit is **locatable** iff none of NL-1…NL-7 holds, i.e. ŝ\* ∈ [s_1 + δ/2, s_9 − δ/2] with θ₁ > 0, at most θ₁ at **+B_θ** (flag SEPARATED, REPORTED; the bracketing pair is still identified, so it stays locatable) and no other bound active.
- Non-finite values are **not** an NL cause. They are a construction failure (§5.4 T-4).
- δ is the grid step of the row's own grid (networks: (s_9 − s_1)/8, PP L107).

**Replicate rule (with §4.6).** A replicate is **G-i-locatable** iff **every** one of its selection fits locates. Otherwise its IGN label is UNAVAILABLE, reason **IGN-UA-SSTAR = PI-SSTAR-NL** (CE51 L44), with all per-fit causes recorded. The near-transition pair for the label comes from the fit at the selected t_r and the primary (pre-nonlinearity) readout (M L314), by RD26 L54's bracketing rule.

### 4.2 Row outcomes (consistent with CE51 §5 as adopted by the Lead, and with M L3422 where AM-15 does not apply)
- Non-locatable gives UNAVAILABLE for the replicate, **never PASS**, and is counted **once per replicate**, whatever the number of NL fits.
- FAIL only from a row-0 licence (CE51 §5 step 3) or an available-screen violation (step 4a/4b).

| Row | Role of a PI-SSTAR-NL replicate | Can it buy a pass? |
|---|---|---|
| IGN-P1 (power, MP L196) | non-MET (non-success) in the power fraction | No: it lowers power |
| IGN-N1, IGN-NC1/0–1, IGN-NC2/0–1 (false MET ≤ 0.05, CP upper ≤ 0.08; MP L198) | **PROPOSED (needs a Lead ruling, R-1): adverse in a worst-case false-MET screen** FM_wc = (n_MET + n_NL)/(n_assessed + n_NL), same thresholds; the literal false-MET rate REPORTED. Without R-1 the replicate is a non-MET, which is **favourable**: converting 12 of 20 false METs out of 200 (CP upper 0.1420, FAIL) into NL gives 8/200 (CP upper 0.0710, PASS). **Open hedge.** | Not under R-1: (a + x)/(b + x) ≥ a/b |
| Network rows BOTT/·, RINIT/·, ARCH/· (confound specificity) | as N/NC (R-1) | as above |
| GA-1 and any row using S_cons/S_wc (AM-15 scope, Lead ruling) | **PI: pr_i = 0, stays in the 200, adverse in both numerator and denominator of S_wc** (CE51 L44, L58) | No |
| IGN-NC2r/0, D0 cells (REPORTED) | counted and reported; enters no label | n/a |
| **IGN-LIM/0, IGN-LIM/1** | **carve-out §4.4: expected outcome, not adverse** | Reverse hedge closed in §4.4 |

- **AM-15 scope consistency.** The Lead ruled ROW0-FL v2 (AM-15) applies to GA-1 and any row that uses S_cons/S_wc, not battery-wide. IGN rows use MP §2.2's operating characteristics, not S_cons/S_wc. So PI-SSTAR-NL is S_wc-adverse **only** in AM-15-scope rows. The N/NC/network confound rows get adverse treatment only if the Lead adopts R-1, which would make them "rows that use an S_wc-type screen" by the Lead's own scope definition, so the scope rule remains consistent. If R-1 is declined, the hedge in the table stays open and must be disclosed to Astra.

### 4.3 Hedge checks
- **H-1 (lowering an adverse rate).** In AM-15 rows and, under R-1, the IGN specificity rows, NL is adverse in numerator and denominator, so the screen can only rise. At P1 it is a non-success. **No path lowers an adverse rate** under R-1.
- **H-2 (once per replicate).** The unit in every denominator is the replicate. NL fits cannot inflate or dilute counts.
- **H-3 (t_r / readout cherry-picking).** Under the every-fit rule a replicate cannot be labelled from the one (t_r, readout) that locates while another is NL.
- **H-4 (no licence through NL).** An NL replicate's label is UNAVAILABLE, so it issues no MET/NOT MET and cannot carry a licence. CE51 §5 step 3 therefore cannot be reached through NL.

### 4.4 IGN-LIM carve-out (L-E3, adopted by the Lead) and the reverse hedge
- **MP L88, verbatim:** "- **IGN-LIM:** a bistable unit with s* outside the probed grid. **Must be UNAVAILABLE**, never NOT MET." MP L199: "| Correct UNAVAILABLE on LIM | ≥ 0.90 | LIM must never be read as a negative. |"
- **Keying.** The carve-out applies only to cells whose **frozen row ID** is IGN-LIM (cell IDs IGN-LIM/0, IGN-LIM/1; V26 L41). The row ID comes from a frozen table hashed into the freeze record. No runtime quantity (ŝ\*, an NL cause, fit status, data, t_r choice) can set, clear or read the key. An assertion at scoring checks that the LIM key table hash equals the frozen value; a mismatch is B-INTEG.
- **Correct LIM replicate (PROPOSED).** Every selection fit of the replicate is NL **with an acceptable cause**: NL-6 in the **expected direction** (OUTSIDE-HIGH for LIM/0, OUTSIDE-LOW for LIM/1), NL-3/NL-4, or NL-5.
- **Incorrect LIM replicate (reverse hedge closed).** Any fit that is:
  - **locatable** (inside the core);
  - **EDGE** (NL-7);
  - **OUTSIDE in the wrong direction**;
  - **FIT-FAIL** (NL-1); or
  - **RESTART-DISAGREE** (NL-2).

  FIT-FAIL is incorrect because a failure is never a pass: a broken fitter must not validate LIM. A label of MET/NOT MET/BOUNDARY at LIM is incorrect and reported individually (RD26 L110: "never NOT MET").
- **Scoring.** The incorrect replicate counts as a non-success in the RD26 §1.3 (B) fraction. That is the existing LIM gate rule; it is not FIXTURE-FAIL, which is reserved for the deterministic FX-LIM. The row outcome stays as RD26 L111–L113 (PASS iff CP lower ≥ 0.90 in both cells and FIXTURE-PASS; FAIL if the bound is < 0.90; UNRESOLVED if INCOMPLETE leaves the bound uncomputable).
- **Cross-row protection.** A fitter that always reports OUTSIDE-HIGH passes LIM/0, fails LIM/1 and fails P1 power. A fitter that always fails fits fails both LIM cells (FIT-FAIL is incorrect) and P1.

### 4.5 Flag for CNA (E51-1 owner)
- CE51 L44 lists PI-SSTAR-NL causes as "FIT-FAIL / NONINCREASING / OUTSIDE-LOW/HIGH". Please extend the list to **NL-1…NL-7** (adds RESTART-DISAGREE, BOUND-ACTIVE and EDGE).
- Please state "once per replicate" and the AM-15 scope (S_wc-adverse only in AM-15 rows; IGN specificity rows per R-1).
- Please replace "it scores as a correct outcome there" (L44) with §4.4's acceptable-cause list, so that FIT-FAIL, RESTART-DISAGREE and EDGE are **not** correct at LIM.

### 4.6 Is ŝ\* fitted per t_r and per readout? (Lead's PD-new-2; LDG L164)
**What the text says (verbatim).**
- RD26 L50: "Within each replicate, using **selection-partition trials only** … pooled across all seeds of the replicate, fit the frozen H1 of MP L66 … If c is present, fit separately per c-level". It is silent on t_r and readout.
- M L313: "Hyperparameters, IGN transition bins, comparator candidates, probe orientation and the optimized BCAST comparator … are chosen on the selection partition."
- M L376: "**Design selection** (probe hyperparameters, IGN bins, t_r, comparator candidates) happens **inside** each replicate on its selection partition (§5.2), and is part of the frozen procedure, not a calibration role."
- M L314: "w = ‖x_ws(t_0 + t_r) − x_ref‖, read pre-nonlinearity (primary; post-nonlinearity REPORTED)".
- V25 L198: "All candidates read from one trajectory per trial on the selection partition".
- MP L70: "Hartigan dip test on w at the two grid levels nearest the fitted transition s* (where π = 0.5), conditioned on c."

**Verdict.** No governing text fixes whether ŝ\* is fitted per t_r or per readout. The t_r **selection statistic** itself is also unspecified anywhere I could find. It is a Lead item (R-4).

**PROPOSED rule (the Lead's default):**
- One selection fit per **(t_r ∈ grid, readout ∈ {pre, post}, c-config)**, with no pooling across them.
- The every-fit rule of §4.1: a replicate is locatable, and therefore PASS-eligible, only if every fit locates.
- Any PI-SSTAR-NL in a non-LIM row counts **once per replicate**.
- The ledger counts the worst case.

**Two conflicts to flag (R-5):**
- (i) The post-nonlinearity readout is "REPORTED" (M L314), yet under this rule its fit gates the label. For NC2 this is deliberate pressure (the clipped readout is the confound), but it makes a REPORTED readout binding. The alternative is that the every-fit rule binds over t_r for the primary readout only, with post-readout NL REPORTED.
- (ii) The S-9 interaction with P1 (§4.7).

### 4.7 Flag for CNA/Lead: P1 at t_r = 2 (S-9)
- The unshifted grid S (0…8δ) contains s_nf(2) = 7.958δ, which is **0.042δ below s_9** and inside the NL-7 EDGE zone (> 7.5δ). s_nf(3) = 6.584δ and s_nf(5) = 5.432δ are inside the core.
- These are noise-free facts. The noisy, fitted location at t_r = 2 is unknown (§3.1) and is measured in calibration (P1 is in C_cal).
- Under the every-fit rule, a P1 replicate whose t_r = 2 fit is EDGE or OUTSIDE-HIGH is non-locatable, so P1 power could be structurally capped.
- **Options for the Lead/CNA, before calibration:**
  - (a) rescale the P1-matched grid so that every s_nf(t_r) lies ≥ 1δ inside the core (CNA owns the grid; the analytic s_nf table above is the input);
  - (b) restrict the every-fit rule to the selected t_r. This weakens H-3 and needs a frozen t_r selection statistic (R-4);
  - (c) drop EDGE (NL-7) for non-LIM rows, keeping it as an incorrect cause at LIM only.

  I recommend (a). No option changes any count.

---

# Part B. E51-3, fitter half

## 5. Fitter pin (PROPOSED; supersedes RDPP §4 where it differs; library PROVISIONAL, UNVERIFIED for the run environment)

### 5.1 What Astra asked (verbatim)
- A51 L129–L135: "For the fitter, accept held-out scoring, analytic gradients and three deterministic restarts. Complete the specification with: / - Exact restart values or generation rules. / - Parameter bounds and positive scale floors. / - Component-label ordering or another fixed identifiability convention. / - Restart acceptance, tie-breaking and all-restarts-failed behavior. / - maxfun and maxls, in addition to maxiter."
- A51 L137: "For mixture models, unconstrained collapsing scales can make likelihood fitting ill-posed. These bounds are scientific implementation choices, not merely library pins."
- A51 L139: "Also correct "absolute gtol": SciPy's L-BFGS-B applies gtol to the maximum absolute component of the projected gradient. ftol is a separate stopping condition. A successful status does not necessarily mean the gradient threshold was reached. Record the termination reason and residual rather than equating every successful status with that condition."
- A51 L187: "E51-3. … Pin NC2 dose quantiles and the fitter's bounds, restarts, termination and failure handling."

### 5.2 Parameterisation, identifiability and bounds
**Data scale constants** (per fit, from the **partition being fitted only**; anti-leak pin V26 L71 (2)): N = number of fitted trials; w_(1) and w_(N) = min and max (type-1 order statistics); R := max(w_(N) − w_(1), σ_min). Grid constants: s_1, s_9, δ, S_abs := max(|s_1|, |s_9|). Frozen constants:
- σ_min = 0.01·Δ_ref = 0.019150080481545376 = `3f939c14258938b1` (scalar rows; V26 L60). log σ_min = −3.9554483606726487 = `c00fa4c21c30d8c2`.
- Networks: σ_min = 0.01·m₀, **PENDING** with the network floor (PD-1).
- B_θ := 20/δ = 150.13888540723337 = `4062c471bfcf3eb0` at the P1 grid (PP L107). Networks: δ = (s_9 − s_1)/8.

**H1** (MP L66). Parameter vector p = (θ₀, θ₁, μ_lo, η, ℓ_lo, ℓ_hi), in this frozen order. π(s) = 1/(1 + e^(−(θ₀ + θ₁s))); μ_hi = μ_lo + e^η; σ_lo = e^(ℓ_lo); σ_hi = e^(ℓ_hi).
- **Label ordering (identifiability convention, A51 L134):** μ_hi > μ_lo strictly, by construction (e^η > 0). π is the weight of the **higher-mean** component, and locatability requires θ₁ > 0 (§4.1), i.e. the hi component grows with s (RD26 L61(c)). Label switching is impossible.

| Parameter | Lower | Upper |
|---|---|---|
| θ₁ | −B_θ | +B_θ |
| θ₀ | −B_θ·(S_abs + 8δ) | +B_θ·(S_abs + 8δ) |
| μ_lo | w_(1) − R | w_(N) + R |
| η | log σ_min | log(3R) |
| ℓ_lo, ℓ_hi | log σ_min | log(3R) |

- Every bound is finite, so on the box the objective is finite: log-space densities, with `logaddexp` both for the mixture and for the softplus terms log π and log(1 − π). A non-finite value is therefore a defect, not a data event (§5.4 T-4).
- The θ₀ range represents every ŝ\* within 8δ of the hull at any |θ₁| ≤ B_θ.
- **Bound arithmetic.** Bounds are computed once per fit in float64 from the pinned constants and the two order statistics, in the order written. They are recorded per fit with their hex.

**H0** (MP L65: "w | s ~ F(μ(s), σ(s), γ(s)). Here μ is a monotone 4-parameter logistic, σ(s) is log-linear in s, and γ is a skew-normal shape").
- p₀ = (A, B, k, c₀, ℓ₁, ℓ₉, γ).
- μ(s) = A + (B − A)/(1 + e^(−k(s − c₀))).
- log σ(s) = ℓ₁ + (ℓ₉ − ℓ₁)(s − s_1)/(s_9 − s_1) (RDPP L179), so σ ≥ σ_min on the whole grid from box bounds alone.
- γ is a **constant skew-normal shape per c-level**. This is my reading of "γ(s)": MP gives no s-dependence, so **CNA please confirm**.
- Bounds: A, B ∈ [w_(1) − R, w_(N) + R]; k ∈ [−B_θ, +B_θ]; c₀ ∈ [s_1 − 8δ, s_9 + 8δ]; ℓ₁, ℓ₉ ∈ [log σ_min, log(3R)]; **γ ∈ [−10, 10]** (PROPOSED; skewness at |γ| = 10 is 0.9556 of the family's 0.9953 maximum, so the bound costs little shape. It replaces RDPP L179's "unbounded").
- H0-FLOOR is REPORTED when ℓ₁ or ℓ₉ is bound-active. H0 has no locatability role.
- **Same optimizer, restarts and acceptance as H1** (RD26 L50).

### 5.3 Restart start points (deterministic, no RNG)
Type-1 order statistic of the **fitted partition's** w (all N trials of the fit, across all grid levels): q(p) := w_(⌈p·N⌉), with p an exact rational and the index computed in integers as (p_num·N + p_den − 1) div p_den.

| Restart | (p_lo, p_hi) | ŝ₀ |
|---|---|---|
| r0 | (1/10, 9/10) | s_5 |
| r1 | (1/4, 3/4) | s_3 |
| r2 | (1/20, 19/20) | s_7 |

- **H1 start:**
  - θ₁ = 4/(s_9 − s_1); θ₀ = −θ₁·ŝ₀;
  - μ_lo = q(p_lo); η = log(max(q(p_hi) − q(p_lo), σ_min));
  - ℓ_lo = ℓ_hi = log(max((q(p_hi) − q(p_lo))/4, σ_min)).
- **H0 start:** A = q(p_lo), B = q(p_hi), k = 4/(s_9 − s_1), c₀ = ŝ₀, γ = 0. ℓ₁ and ℓ₉ = log(max(1.482602218505602·MAD_i, σ_min)) at levels i = 1 and 9, where MAD_i = the type-1 lower median of |w − w_med,i| over level i's trials, and w_med,i is the type-1 lower median w_(⌈N_i/2⌉). The constant 1.482602218505602 = 1/Φ⁻¹(3/4).
- Each start is projected onto the box explicitly: clip, recorded. scipy also clips x0 (`_lbfgsb_py.py` L359: `x0 = np.clip(x0, bounds[0], bounds[1])`), but the pin does not rely on it.
- Example (gradient-fixture data of §5.7): the r0 start is (θ₀, θ₁, μ_lo, η, ℓ_lo, ℓ_hi) = (`c000000000000000`, `400e071c6618644d`, `3fd129242a038cee`, `3fcbc6365c7e9003`, `bff2b57c336a67ef`, `bff2b57c336a67ef`). θ₀ = −2 exactly, because θ₁·s_5 = 4·4δ/8δ.

### 5.4 Termination (scipy 1.18.1 `_lbfgsb_py.py`, read-only; line numbers of that file)
- **Call:** `minimize(fun, x0, jac=True, method='L-BFGS-B', bounds=B, options={'maxiter': 1000, 'maxfun': 15000, 'ftol': 1e-10, 'gtol': 1e-8, 'maxcor': 10, 'maxls': 20})`, objective = mean per-trial NLL (V26 L72).
- **Mapping in source:**
  - L335–L336 `pgtol = gtol`, `factr = ftol / np.finfo(float).eps` (= 450,359.96…);
  - **L438–L443:** `if task[0] == 4: warnflag = 0` / `elif sf.nfev > maxfun or n_iterations >= maxiter: warnflag = 1` / `else: warnflag = 2`;
  - `status = warnflag`, `success = (warnflag == 0)` (L460–L461);
  - task codes (L50–L91): 4 = CONVERGENCE with 401 "NORM OF PROJECTED GRADIENT <= PGTOL" or 402 "RELATIVE REDUCTION OF F <= FACTR*EPSMCH"; 6 = WARNING (601–604, e.g. "ROUNDING ERRORS PREVENT PROGRESS"); 7 = ERROR (701–713); **8 = ABNORMAL**.
  - In 1.18.1 the message is `status_messages[task[0]] + ": " + task_messages[task[1]]` (L456). The pre-1.15 text "ABNORMAL_TERMINATION_IN_LNSRCH" **does not occur**; an abnormal line-search exit reads "ABNORMAL: …" and gets status 2, unless a limit was also crossed (then status 1).
  - The limit checks run **only at a new iteration** (`task[0] == 1`, L421–L434, with a strict `sf.nfev > maxfun`). The source comment reads "interruptions due to maxfun are postponed until the completion of the current minimization iteration".
- **Per-restart classification (keyed on integers; message text recorded verbatim, never parsed for decisions):**

| Code | Condition | Restart result |
|---|---|---|
| T-0 ACCEPT | status 0; x, fun, jac finite; recomputing the objective and gradient at res.x reproduces res.fun **bitwise**; projected-gradient residual ρ := max_i \|clip(x_i − g_i, l_i, u_i) − x_i\| ≤ **G_acc = 10⁻⁵** (PROPOSED, 10³·gtol) | accepted. ρ, nit, nfev and the message (401 vs 402) are recorded (A51 L139) |
| T-1 STALLED | status 0 but ρ > G_acc (ftol-type convergence far from stationarity) | discarded |
| T-2 LIMIT | status 1 (maxiter or maxfun) | discarded |
| T-3 ABNORMAL/WARNING/ERROR | status 2 | discarded |
| T-4 NON-FINITE | any objective or gradient evaluation non-finite. The wrapper raises a frozen exception at once; scipy does not check finiteness | **construction failure** (M L3421); no retry, no other restart run |
| T-5 NON-REPRODUCIBLE | the bitwise recomputation differs | **integrity failure** (B-INTEG, CE51 L42) |

- **Evaluation ceiling (UNVERIFIED).** The wrapper bounds nfev only by maxfun + (evaluations within one iteration). One line search uses ≤ maxls evaluations. L-BFGS-B, after a failed line search with non-empty memory, resets memory and retries within the same iteration, so I use **maxfun + 2·maxls = 15,040** as the conservative ceiling (LDG L59 uses 15,020). This reading of the compiled routine (`_lbfgsb.cpython-313-x86_64-linux-gnu.so`, sha256 `b1969757…`, no C source shipped) is UNVERIFIED. It changes LDG's ceiling by 0.13% (its §8 item 7).

### 5.5 Restart selection and failure handling (fit level)
- **Selection:** among accepted restarts, the lowest **recomputed** mean NLL (float64 comparison), with exact ties to the lowest index r0 < r1 < r2 (RDPP L181).
- **One or two restarts fail** (T-1/T-2/T-3): the fit stands on the accepted ones. Failures are recorded and REPORTED, with no label effect.
- **All three fail:** **FIT-FAIL**.
  - Selection fit: NL-1 → PI-SSTAR-NL (§4.2).
  - Main per-seed fit F1 (ΔLL/D): new code **PI-FIT-NC** (PROPOSED, Lead R-2). The replicate is INCOMPLETE and its IGN label is not computed. It is a non-success in IGN rows (M L3422), and PI (adverse in S_wc) in AM-15-scope rows. CE51 L53's default ("unlisted cause → BLOCKING") applies until the Lead lists it.
- **Restarts disagree:** for selection fits only, NL-2 (§4.1, τ_f = 10⁻⁹, Δŝ\* > δ/2). For F1 fits the selected minimum stands, and the spread of accepted NLLs is REPORTED.
- **Flags at the selected restart:**
  - SEPARATED (θ₁ at +B_θ): REPORTED; the fit is locatable if otherwise inside the core.
  - θ₁ at −B_θ: NL-3/NL-4.
  - Any other bound active: NL-5 for selection fits. For F1 fits it is REPORTED and the fit stands: the floors bound the likelihood, which is their purpose (A51 L137), and ΔLL and D use the bounded fit.
- **T-4 / T-5** are never absorbed at the fit level (next section).

### 5.6 Mapping to row outcomes, checked against CNA's decision table (CE51 §5, adopted by the Lead with n_wc ≥ 36)

| Fitter event | Class | CE51 §5 step (AM-15 rows) | IGN rows (M L3422 / MP §2.2) | Never PASS? |
|---|---|---|---|---|
| Thread-pool assertion fails; T-5 non-reproducible; any fit reading final-partition data | B-INTEG (CE51 L42) | 1 BLOCKED | stage blocked | yes |
| Gradient fixture §5.7, version/KAT mismatch at freeze, FX-LIM fail | B-BUILD (CE51 L40) | 2 NOT BUILT | row not built | yes |
| T-4 non-finite | B-RUN construction failure (M L3421) | 5 UNRESOLVED (blocked) | replicate INCOMPLETE, non-success; row UNRESOLVED if it cannot meet its rule (M L3422) | yes |
| Selection FIT-FAIL / NL-2…NL-7 | PI-SSTAR-NL (CE51 L44) | PI, adverse in S_wc (step 4b) | §4.2 (R-1 for specificity rows) | yes |
| F1 FIT-FAIL | PI-FIT-NC (new, R-2) | PI, adverse in S_wc | INCOMPLETE non-success | yes |
| 1–2 restarts fail; SEPARATED; F1 bound-active | none (REPORTED) | — | — | n/a |

**Consistency verdict.** Consistent with CE51 §5's order (integrity → not built → licence in row 0 → available screen violated → runtime construction failure → confound not realized → insufficient support → PASS): every fitter failure lands on a non-PASS step, and none produces FAIL except through a screen evaluated on counts that include it adversely. Three conflicts:
1. **C-1 (BLOCKING vs PI default).** CE51 L53 makes unlisted causes BLOCKING. Until the Lead lists **PI-FIT-NC** and the extended NL causes (§4.5) as PI, they default to BLOCKING, which is stricter. It is safe but would block a whole row on one non-converged seed fit. Lead ruling R-2.
2. **C-2 (T-4 scope).** CE51 step 5 (B-RUN blocks the row) is stricter than M L3422 and applies only in AM-15 scope. IGN rows keep M L3422. A non-finite fitter value is therefore row-blocking in AM-15 rows but a non-success in IGN rows. This is consistent with the Lead's scope ruling, and I note it so nobody reads the stricter rule into IGN.
3. **C-3 (LIM).** At IGN-LIM, FIT-FAIL is **incorrect** (§4.4), whereas CE51 L44 says PI-SSTAR-NL "scores as a correct outcome there". §4.4's acceptable-cause list should govern; CNA please align (§4.5).

### 5.7 Analytic-gradient verification fixture (PROPOSED; B-BUILD on failure)
- **Input, by formula (no RNG).**
  - Levels s_i = fl(s_c·m)/4, m = 0…8 (P1 grid hex, CE51 L151–L161), with J = 12 trials per level, so N = 108.
  - z_j = Φ⁻¹((j − ½)/12), j = 1…12, computed at 50 digits and rounded to float64 (z_1 = `bffbb4e5b9cfe1d2`, z_2 = `bff267d4c07b0567`, z_3 = `bfe9fdb02fd57a07`, …).
  - k_m = ⌊12·m/8⌋ = (0, 1, 3, 4, 6, 7, 9, 10, 12) hi trials at level m.
  - w_{m,j} = 0.3 + 1.2·[j ≤ k_m] + 0.1·z_j.
  - Data KAT: sha256 of the big-endian float64 (s, w) arrays = `ee1707137c2bbc5c9c246f7410a460e1c5f057b35c74ab17a646008ca61d9ba4` (box; UNVERIFIED for P6).
- **Points:** the three §5.3 starts r0/r1/r2 computed from this input, so the fixture also checks the start formula. Their hex is frozen.
- **Check:** for each point and component, the float64 analytic gradient g_an vs a reference g_ref = the 50-digit central difference (step 10⁻²⁰) of the 50-digit objective. Pass iff |g_an − g_ref| ≤ **10⁻⁹·max(1, |g_ref|)** (PROPOSED) and |f_float − f_50| ≤ 10⁻¹² for all 18 components and 3 objectives. A float64 central-difference check (step 2⁻²⁰·max(1, |p_j|), tolerance 10⁻⁶ relative) runs in the run environment as a second, mpmath-free check.
- **Prototype result (box; H1):** worst relative gradient error **8.04e−16**; objective errors 9.2e−19, 8.5e−17, 7.8e−17. The fixture is constructible and passes with margin.
- **H0 fixture:** same construction once CNA confirms the γ form (§5.2). PENDING CNA.

### 5.8 Reproducibility, environment and freeze KAT
- **Pins (PROVISIONAL, UNVERIFIED for the run environment):**
  - Python 3.13.5, numpy 2.5.4, scipy 1.18.1, threadpoolctl 3.7.0;
  - record `numpy.show_config()`, scipy's bundled OpenBLAS version, the libm build and the sha256 of `scipy/optimize/_lbfgsb_py.py` (box: `61b69554…`) and of the `_lbfgsb` extension (box: `b1969757…`).
- **Threads:** before importing numpy, set `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `BLIS_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`. Then assert with `threadpoolctl.threadpool_info()` that every pool has `num_threads == 1`; otherwise B-INTEG. One fit per process.
- **Freeze-time KAT (required):**
  - (i) the §5.7 fixture passes;
  - (ii) a frozen **reference fit**: the full fitter on the §5.7 input, from the three frozen starts, under the pinned environment. Record each restart's status, message, nit, nfev, ρ and the selected x as hex. At construction, rerun it and require a **bitwise** match, else B-BUILD. This is a deterministic construction KAT on synthetic formula data, not instrument data, and is run only at freeze by whoever is authorized then; **not run here**;
  - (iii) the version and hash records above match;
  - (iv) the thread assertion holds.
- **Any change** of version, BLAS or libm is a re-freeze.

---

# Part C. Cross-lane items

## 6. Items requested by the parent / Lead

### 6.1 L-E2: does GA-1's shortfall use the M L2819–L2820 usable-allocation accrual? (RD owns E-ATTR)
- GA-1 is "REW-CORR option B" (amendment record L16). Its rows are REW-CORR-E/-I (M L1627: "| REW-CORR-E | E-ATTR (state z = r̄ + ε, ε ~ N(0, (0.1·SD(r̄))²); policy reads the state) | not MET | specificity row, PASS / FAIL / CONFOUND NOT REALIZED |").
- **M L2819 (verbatim, excerpt):** "**Usable allocations (replaces the DISSOC stopping rule of PZ5 §5.4).** Accrual counts **usable allocations**, not cell occupancy: a usable allocation is a recipient with a full four-continuation unit … Accrual stops at the first batch boundary at which the declared quota of usable allocations per seed (50 recipients, with their donors) is met; no matching tolerance, reuse limit or eligibility rule is relaxed as the cap approaches (#44 L120)."
- **M L2820 (verbatim):** "**Attribution incompleteness (replaces "enters D20 worst-case completion" in the PZ5 §5.4 DISSOC row).** For attribution and every other non-V paired comparison, an INCOMPLETE unit or seed takes **D20's no-label rule**: any incomplete required pair → no confirmatory label. Worst-case completion bounds apply only to V-based comparisons (V, G, d_EXT) and **cannot manufacture an attribution result** (#44 L122)."
- **M L2763 (verbatim, excerpt):** "| **End-to-end fitted-probe rows** | Probes fitted on the DISSOC fitting partition; the full frozen pipeline | RCAL-ADV-E/-I, NLN-E/-I, MIXED-CODE-E/-I, REW-CORR-E/-I, ATTR-P1-E/-I …".
- **Verdict: NOT CONFIRMED.**
  - (1) L2819 sits in §4.3 "caps, consequences and accrual", written for DISSOC screening episodes and the caps "DISSOC 4,300 screening episodes per seed". Its "per seed" is the trained-agent seed.
  - (2) L2763 puts REW-CORR-E/-I through "the full frozen pipeline", which **supports** the accrual applying to Stage-0 GA-1 replicates, but no text maps L2819's per-seed 50-recipient quota onto a GA-1 Stage-0 replicate seed or says what a Stage-0 shortfall is called.
  - (3) GA-1's approved wording ("Pooled per outer replicate") says nothing about accrual.
  - (4) L2820's no-label rule is stated for attribution, which does cover E-ATTR, but again without a Stage-0 mapping.
  - A51 L35 requires "an explicit scope mapping", and none exists.
- **PROPOSED mapping text (RD, E-ATTR owner; Lead to adopt):** "For the GA-1 rows REW-CORR-E/-I, each Stage-0 replicate seed runs the frozen E-ATTR/I-ATTR pipeline under M L2819's usable-allocation accrual, with the same quota (50 recipients with their donors per seed), the same matching, caliper, support, donor-reuse and partition-separation rules, and the same cap. A seed that does not reach the quota at the cap is INCOMPLETE and takes M L2820's D20 no-label rule. The replicate is then **PI-ATTR-ACCRUAL** (CE51 L45): pr_i = 0, adverse in S_wc, any licence → FAIL. The IGN per-(seed, bin) quota does not apply to GA-1." With this text adopted, L-E2 becomes CONFIRMED.

### 6.2 Fit-count input for the Lead's ledger (E51-4; exact integers from frozen counts)
**Units (from WL L17, V25 L209, L218):**
- Replicates per C_cal cell = |GRID|·200 + step-3a 2·200 = 1,800 + 400 = 2,200. Over 15 cells: 33,000. C_conf: 20 × 200 = 4,000. **R = 37,000 replicates**, independent of n_seed.
- NC1 replicates: 2 × 2,200 + 3 × 200 (NC1/0, NC1/1, NC1/D0) = **5,000**. c-configs: φ_c ∈ {1, 3}. My reading of φ_c = 3 is 2 c-levels + 1 no-c REPORTED run, from MP L86 ("Run also without c").
- Replicate-configs R_c = 37,000 + 5,000·(φ_c − 1) = **37,000 / 47,000**.
- Seed-units U = 15·(58,400 + 400n) + 20·200n; U_NC1 = 2·(58,400 + 400n) + 3·200n; U_c = U + U_NC1·(φ_c − 1).

| Family | Partition | Unit | Fits/unit | Restart calls/unit | n = 67, φ_c = 1 | n = 67, φ_c = 3 | n = 9, φ_c = 1 | n = 9, φ_c = 3 |
|---|---|---|---|---|---|---|---|---|
| F1 main H0+H1 (ΔLL, D) | fitting, per seed (2,286 trials) | U_c | 2 × 3 t_r × 2 readouts = 12 | 36 | 18,552,000 fits / **55,656,000** calls | 23,606,400 / **70,819,200** | 11,592,000 / **34,776,000** | 14,697,600 / **44,092,800** |
| F2 ŝ\* selection H1 (§4.6 default) | selection, pooled over the replicate's n seeds (n × 1,143 trials) | R_c | 3 t_r × 2 readouts = 6 | 18 | 222,000 / **666,000** | 282,000 / **846,000** | same as 67 | same as 67 |
| F2 if fitted only at the selected (t_r, readout) | selection | R_c | 1 | 3 | 37,000 / 111,000 | 47,000 / 141,000 | same | same |
| FX-LIM (noise-free, no fit) | — | once | — | — | 18,000 recursion steps | same | same | same |
| Gradient fixture + reference fit KAT | synthetic | once | 1 | 3 | negligible | | | |

- These reproduce LDG L63–L64 exactly (F1 55,656,000 / 70,819,200; F2 666,000 / 846,000), confirming LDG's PD-new-2 worst case.
- Per-call evaluation ceiling: 15,040 (§5.4; UNVERIFIED) vs LDG's 15,020. The worst-case F2 evaluations are 846,000 × 15,040 = 12,723,840,000 (LDG basis: 12,706,920,000).
- F3–F5 (hysteresis, dose calibration) are LDG's and not re-derived here.
- No stop or schedule quantity enters any count; all counts follow from frozen cell lists, GRID, R = 200 and the t_r and readout grids.

### 6.3 Wording notes
- **Network settling** is **20 steps** (M L1127: "t_s = 5τ in plants (residual e^−5 < 1%); 20 steps in networks"). Scalar plants use t_s = 0 under AM-4. Nothing in this file uses "5τ" for networks.
- The AM-9 rationale quote "direct fixed-point iteration is not guaranteed to converge for every negative g" is **A50 L153** (Astra's **#50** reply), not #51.
- The x0 key that CE51 §7 supersedes is at **V26 L52** (CE51c1 item 1).

## 7. Rulings needed

| # | For | Decision | RD proposal |
|---|---|---|---|
| R-1 | Lead | IGN specificity rows (N1, NC1, NC2, BOTT, RINIT, ARCH): count PI-SSTAR-NL (and PI-FIT-NC) adversely in a worst-case false-MET screen FM_wc, same thresholds, literal rate REPORTED. This brings them inside AM-15's "rows using S_wc-type screens" | Adopt. Otherwise disclose the open hedge (§4.2) to Astra |
| R-2 | Lead | List PI-FIT-NC and NL-1…NL-7 as PI (not BLOCKING by default, CE51 L53) | Adopt |
| R-3 | CNA → Lead | LIM/1 offset +7 → **+11**; FX-LIM replaces RD26 (A); the claim text of §3.3 | Adopt before calibration |
| R-4 | Lead | Frozen t_r selection statistic (no text found) | PENDING; needed for §4.1's near-transition pair |
| R-5 | Lead | ŝ\* per (t_r, readout) with the every-fit rule (§4.6) vs primary-readout-only binding | Default adopted here; note the REPORTED-readout conflict |
| R-6 | CNA/Lead | P1 at t_r = 2 sits at the grid edge (§4.7): grid rescale (a), selected-t_r-only (b), or EDGE dropped for non-LIM rows (c) | (a) |
| R-7 | Lead | Fitter constants: G_acc = 10⁻⁵, τ_f = 10⁻⁹, Δŝ\* > δ/2, \|γ\| ≤ 10, fixture tolerance 10⁻⁹, FX-LIM \|x_nf\| > 10⁻⁶ | Adopt as PROPOSED |
| R-8 | Lead | L-E2 mapping text (§6.1) | Adopt; then L-E2 CONFIRMED |
| R-9 | CNA | Extend CE51 L44 per §4.5; confirm the H0 γ form (§5.2) | — |

*DESIGN ONLY. Draft, not frozen. Nothing was simulated, fitted, trained or timed. X1–X5 and the claim ceiling unchanged. No consciousness claim. Nothing was posted or sent.*
---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 1d99454ad1165544fe8d8a371b1c4ff1a7a1fbdad1cb20db714f5db6858276df
