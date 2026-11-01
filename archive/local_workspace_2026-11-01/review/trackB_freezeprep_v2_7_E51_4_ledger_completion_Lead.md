# Track B freeze preparation v2.7: E51-4 ledger completion (Lead) — K_dc bound, fit decomposition, dip procedure, network settling, revised maximum work; v2.7 carry-overs

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** A new, additive file; it edits no existing file. Under the binding rule, no chmod-444 file is rewritten in place; corrections go in new versioned files beside it. Nothing was run, timed, benchmarked or installed. The only computation was SHA-256 and exact integer arithmetic plus float64 products of stated per-unit costs in the system `python3` (scripts `scratch/lead_v27/ledger4.py`, `gen_v27.py`). **Every CPU-hour figure is arithmetic on stated, unmeasured per-unit costs and is UNVERIFIED; none is a bound** (A51 L175). Nothing was sent to Astra or anyone else.
- **Written:** 2026-11-01, 1:05 PM ET (from `date` when generated), by the Lead's executor, on the Lead's E51-4 task.
- **Scope:** Astra's E51-4 only (A51 L189: "E51-4. Finish the maximum-work ledger: K_dc bound, fit decomposition, dip procedure and network settling duration. Keep runtime figures conditional and unverified."), plus the v2.7 carry-overs from RD's light pass (RDLP2). E51-1, E51-2 and E51-3 are **not** answered here; where this file touches them (§1 failure outcome, §6.7 zero denominators) it says so.
- **Governance:** GA-1 and A-2026-10-24 remain approved by Aidan (2026-11-01 10:58 AM ET). Every rule below is a prospective, pre-data proposal under A-2026-10-24. **No freeze, execution, benchmark or timing run is requested or authorized** (A51 L191). Any such run needs its own protocol, Astra's review and Aidan's explicit yes.
- **Safety (unchanged):** X1–X5; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); claim ceiling (#41 L304); no consciousness claim is made or implied.
- **Labels:** **PROPOSED** = for the Lead to rule on; **CARRY-OVER** = an RDLP2 item or Lead instruction recorded for v2.7.

### Inputs (all verified: whole-file sha256 recomputed; footers recomputed where present)
| Abbrev. | File | sha256 | Footer |
|---|---|---|---|
| A51 | `astra_consult51_response.txt` | `f7f35ec21d37fc98478dc3597d43d4333a72edee606dd00ff5acb33086772463` | — (no footer) |
| V26 | `review/trackB_freezeprep_v2_6_consolidated_Lead.md` | `ff03eb81c158e1306df0aaf2127d6191c81f80e11838231345749dd88e0de4c6` | `85cc351656baddd047bc52597251d84fdd81d3a74114a1273f438526a1321dd6` ✔ |
| WL | `review/trackB_freezeprep_v2_6_E50_5_workload_ledger_Lead.md` | `83247be974ce3da79735c0eb28cbb8eb80d476d1d00a07ea43b270bb7e33e5fe` | `39371967c33a3c709e562490fe97cca7f4b3a9a71af3244393a3f8c3a2b1f269` ✔ |
| RDLP2 | `review/trackB_freezeprep_v2_6_consolidated_lightpass_RD_v2.md` | `77a889b36cde79f3e46e2e972c803422a5a4674ead9381aef7ccc5e1e16fb72a` | `5165b5c4c460a13446e2a31d4728b42db70465d94c63a2cb260aed2a9a87015c` ✔ |
| A50 | `astra_consult50_response.txt` | `59e93cfffa8f9755262cf4736c4e8158b45064acb8348fb3d813ebc1b4d314c3` | — (no footer) |
| V25 | `review/trackB_freezeprep_v2_5_consolidated_Lead.md` | `d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5` | `36dbcb5f48c7e21ab572af6da5cce63548f54f4b30403955f6d5fb9d8631e0c0` ✔ |
| E2C2 | `review/trackB_freezeprep_v2_5_erratum2_corr2_Lead.md` | `5100f4de826dacbd422be92e056f58578fc9a5c332353885ebb0f50f62cf8092` | `da5aec39632978c3f318caf1055b602a14560a69b02c7af914c88984b79e1ae0` ✔ |
| E2C3 | `review/trackB_freezeprep_v2_5_erratum2_corr3_Lead.md` | `2f813ba4bb58507241ced0bea97354fdfc63990015786feaadeb4709e4630eec` | `8d420ab1b9fbee4745cedf430b3e9cfc57feb3230617fb290faa40afa0122b2f` ✔ |
| CE50 | `review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1.md` | `b5a880ea35a77ae2de47dfd8d9bb2516d9e9b331f96c52ded8e123c780939f97` | `1ebe8c5d4aec7027f97be89a01049fc7b9441d5dddeeea50aafa8b7fc4ba5a2f` ✔ |
| CE50e1 | `review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1_erratum1.md` | `42bf6c6d75380579d6f99643b29b9c9723601867003a5b4d0d51d9cb4e4e1d77` | `fd5b764b5e2a728f6d86e10e1bf97a2640f8e918da827a0983410a1b2184e2e7` ✔ |
| RD26 | `review/trackB_freezeprep_v2_6_E50_2_E50_4_RD.md` | `8a36920898f8a2aece46189631f4c5592719f0c4e5a566cf5687ba1dbc28fc73` | `c29401c458a408ebd73a93f94c89a91f3a6da2f6464bbee84b1724a95fbc3520` ✔ |
| RD26c2 | `review/trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr2.md` | `e8bba1b248b3702bdc4f231581a28a0f333d1456420c6d89a53a8e55c3d9addf` | `7ee752014bcb89b3a4a3a85366d6c3fd86a232e68d7d5270ccf87abacb105fbf` ✔ |
| CE50a1 | `review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1_addendum1.md` | `fdba7c639e9e0deb0d20829ac6e8829d7a0429292d94aa68d6a3540014c6fc7c` | `36a2ad78a43cd553a5b843fd9a94f990d1c7f9bed0773532f3b9288cfc2f9bc7` ✔ |
| RDPP | `review/trackB_scope_v3_6_CNA_E50_params_and_erratum1_lightpass_RD_v1.md` | `12371a769217eec9322f36932bcd7b4002d59cb8636f2dcf734d1f175d0df19a` | `ae88a5c7914cf608ab05b133d4ed250f4d8c08b1da7ce5448c47cd90d740974e` ✔ |
| ER1 | `review/trackB_freezeprep_v2_5_erratum1_Lead.md` | `10860e98444d31c0f432b44f44427b1a522add744d42dd65ce38e20c5c349c2a` | `4d51b00cdb17a4bc86b2dc0863a8264113c7e38d9cdf1ae706382f8294249511` ✔ |
| M | `review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` | `bb074b332a3af3563823c4a5bc687bbb3b5db23dcc573991cbe04308a498b6d8` ✔ |
| MP | `review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` | — (no footer) |

"A51 Ln" = line n of Astra's raw #51 reply; "A50 Ln" likewise for #50; "V26 Ln", "WL Ln", "M Lnnnn", "MP Ln" = lines of those files.

## 0. Summary
| E51-4 item (A51 L165–L173) | Response | § |
|---|---|---|
| K_dc bound | **PROPOSED hard bound K_dc ≤ 5** candidate doses per dose-calibration cell, enforced by a frozen candidate list and counter assertion; no 6th candidate; unsuccessful calibration → construction failure of the cell (blocking). **B1 maximum 72,009,000 trials** | §1 |
| Fit decomposition | Per (replicate, c-level, seed): 12 model fits × 3 starts = **36 optimizer calls**; per (replicate, c-level): ≤ **18 pooled selection calls** for ŝ*; dose calibration and hysteresis counted. **Worst case at n = 67: 84,066,900 optimizer calls**, ≤ 1,262,684,838,000 value+gradient evaluations under the pin | §2 |
| Dip procedure | Hartigan & Hartigan dip; p-value from a **frozen exact-n Monte Carlo table** (uniform null, N_tab = 100,000 per n, n = 4…127, RNG role `ign-dip-null-table`), exact count lookup, **no interpolation, no per-test simulation, no fallback**. Worst case 7,931,800 observed dips + 12,400,000 one-off table dips | §3 |
| Network settling | **t_s,net = 20 network steps, a literal integer** (M L1127's network clause); readout t_r ∈ {3, 5, 8} steps; trial = 28 steps; null runs = 20 steps. Conversion: τ_net := 4 steps by definition, so 5τ_net = 20 steps | §4 |
| Revised maximum work | Op counts §5.1. CPU-h (UNVERIFIED) at 67: **≈ 931 (Low) to ≈ 87,404 (High = maximum-cost envelope)**; **pin-saturated ceiling ≈ 165,116**. At 9: ≈ 582 to ≈ 55,211, ceiling ≈ 103,829 | §5 |
| v2.7 carry-overs | Cost-drop attribution; v2.6 lock time; E2C2/E2C3; "for every negative g"; AM-12..AM-14; Fisher–Yates counter; zero-denominator rule; AM-2 rationale; "full-grid work is scheduled" | §6 |

## 1. K_dc: fixed upper bound, dose-calibration maximum, enforcement (PROPOSED; the Lead rules)
Astra (A51 L167): "K_dc = 5 is a placeholder, not a maximum. Either adopt five as a hard bound with a defined unsuccessful-calibration outcome, or leave the total explicitly conditional."
- **Proposed value: K_dc = 5 as a hard upper bound** (not a placeholder): at most five candidate doses per dose-calibration cell. Rationale: each dose-calibration cell is one required dose level (V26 §2 cell list: BOTT/0–1, RINIT/0–2, ARCH/0–1), and five candidates bracket its target with two on each side of the planning value. The choice uses no data. A smaller K_dc lowers B1 linearly (K_dc = 3: 43,205,400 trials).
- **Which cells:** only the **7 network C_cal cells** (BOTT/0, BOTT/1, RINIT/0, RINIT/1, RINIT/2, ARCH/0, ARCH/1). Scalar references are analytic and the NC2 rule (AM-3) removes the scalar cells (V26 §5). D0 cells never need dose calibration. The set is frozen as a list before dose calibration starts.
- **Maximum:** **B1 ≤ 7 cells × R_cal,dose 50 × 4,572 trials × n_dc 9 × K_dc 5 = 72,009,000 trials** (exact). It does not depend on n_seed*: dose calibration runs before sample-size calibration (WL B1). In seed-units: 7 × 50 × 9 × 5 = **15,750**. In network steps: 72,009,000 × 28 = 2,016,252,000.
- **Enforcement (all → construction failure, M L3421, no fallback):**
  1. the frozen candidate-dose list of each cell has **between 1 and 5 entries**, each a float64 hex literal, asserted at construction (len > 5 → construction failure);
  2. candidates are evaluated in the frozen list order; **maximum-cost accounting charges all five**, whether or not an earlier candidate qualifies;
  3. **no candidate may be added, replaced or refined** after dose calibration starts; there is no 6th candidate, no bisection between candidates and no re-run with new seeds;
  4. an integer **dose-calibration trial counter** per cell must end ≤ 50 × 4,572 × 9 × K_dc (≤ 10,287,000 per cell); exceeding it is an integrity failure;
  5. a per-ledger cap for B1 (P5) is set at 72,009,000 trial-equivalents; cap-limited work is "INCOMPLETE, never passed" (M L368).
- **Unsuccessful calibration (defined outcome):** if no listed candidate meets the frozen dose-selection criterion, the cell records **DOSE-CAL-FAIL**. That is a **construction failure of the cell** (a failure that invalidates the assessment, in Astra's E51-1 sense, A51 L30): it **blocks**. The rows that need that cell are **UNRESOLVED, never PASS**, and are not absorbed as an acceptable missing fraction. The redesign policy (M §5.8) applies: revise, re-freeze and a new Astra review, with the failure kept in the record. Revising K_dc or the list after dose calibration has started would be a post-calibration change and needs its own named amendment, disclosed as post-calibration.
- **Status:** PROPOSED for the Lead. The dose-selection criterion itself (what a candidate must achieve) is not changed here; it stays as frozen in CNA v3 §8.3 / M §5.9.

## 2. Fitting work: decomposition and worst case
Astra (A51 L169): "Decompose the upper fit count into main fits, pooled selection fits for s-hat*, dose calibration and any additional diagnostic fits. With three fixed restarts, the scheduled fit count should have a traceable derivation."
**Fitter pin** (V26 §5, PROVISIONAL library pin): L-BFGS-B, analytic gradients, mean per-trial NLL, ftol 1e-10, gtol 1e-8 (on the projected-gradient max-abs component; see §6.9), **maxiter 1,000, maxfun 15,000, maxcor 10, maxls 20**, three deterministic starts. Per call, the conservative ceiling on value+gradient evaluations is **maxfun + maxls = 15,020** (a line search in progress when maxfun is reached can add at most maxls evaluations; maxiter × maxls = 20,000 > maxfun, so maxfun binds). This reading of scipy's counting is UNVERIFIED for scipy 1.18.1 and is to be confirmed at freeze with the library pin.

| Fit family | Unit | Calls per unit | Data per call | Units at n = 67 (φ_c = 1 / 3) | Calls at 67 (φ_c = 1 / 3) |
|---|---|---|---|---|---|
| F1 main H0/H1 per seed (fitting partition) | (replicate, c-level, seed) = seed-unit × c-level | 2 models × 3 t_r × 2 readouts = 12 fits × 3 starts = **36** | 2,286 trials | 1,546,000 / 1,967,200 | 55,656,000 / 70,819,200 |
| F2 pooled selection H1 for ŝ* (RD26 L50) | (replicate, c-level) | ≤ 3 t_r × 2 readouts × 3 starts = **18** (3 if ŝ* is fitted only at the selected t_r and readout) | n × 1,143 trials | 37,000 / 47,000 | 666,000 / 846,000 |
| F3 hysteresis transition fits (REPORTED) | seed-unit × c-level | ≤ 2 directions × 3 starts = **6** (estimator PENDING) | ≤ 9·h points | 1,546,000 / 1,967,200 | 9,276,000 / 11,803,200 |
| F4 dose-calibration per-seed fits | dose-calibration seed-unit | **36** | 2,286 trials | 0 / 15,750 | 0 / 567,000 |
| F5 dose-calibration pooled fits | (cell, replicate, candidate dose) | **18** | 9 × 1,143 trials | 0 / 1,750 | 0 / 31,500 |
| **Total** | | | | | **65,598,000 / 84,066,900** |

- **Derivations.** Seed-units U = Σ over cells and replicates of n_seed = 1,546,000 at 67 (A51 L153 confirms 1,546,000). φ_c is the NC1 per-c-level factor (1–3): extra units U_NC1·(φ_c − 1), U_NC1 = 210,600 at 67, so U_eff = 1,967,200 at φ_c = 3. (Replicate, c-level) units: 15 C_cal cells × 2,200 replicates (200 × 9 grid points + 400 step-3a) + 20 C_conf cells × 200 = 37,000, plus (φ_c − 1) × (2 × 2,200 + 3 × 200) = 10,000 at φ_c = 3. "F = 36" in V26 and WL is F1 only.
- **No other fits:** ΔLL scoring on the final partition, Ashman D and the dip statistic use the F1 parameters without refitting; the bootstrap resamples seed statistics only, with no refit (WL C4); cross-validation is not run (AM-2). Diagnostic refits are not scheduled; any would need a named amendment and its own ledger line.
- **Worst-case evaluation count (n = 67, φ_c = 3, K_dc = 5):** 84,066,900 calls × 15,020 = **1,262,684,838,000 value+gradient evaluations**. Trial-weighted: (F1 + F4) × 2,286 + F2 × n × 1,143 + F5 × 9 × 1,143 + F3 × 9, times 15,020, times c_ev ops per trial per evaluation = **3.0655e+17 ops at c_ev = 100** (c_ev UNVERIFIED planning value for a two-component mixture with logistic π(s) and its gradient). At 9: 52,886,100 calls, 1.9178e+17 ops.
- **Cost model.** Envelope (as V26): t_fit = 0.03–0.3 s per F1-size call, F2/F5 scaled by data size (n × 1,143 / 2,286), F3 negligible. **Pin-saturated ceiling:** every call uses 15,020 evaluations at c_ev = 100 ops per trial and 10⁹ ops/s (both UNVERIFIED): ≈ 3.43 s per F1 call, 11.4× the High t_fit. This is the maximum the pin allows, not an expected cost.

## 3. Dip procedure (pinned; per-test simulation is not a procedure)
Astra (A51 L171): "Pin the dip p-value procedure and table. A table-based primary procedure and per-test simulated p-values are different algorithms. The latter can be a labelled cost scenario, but cannot remain an unspecified fallback after seeing results." MP L70: "Hartigan dip test on w at the two grid levels nearest the fitted transition s* (where π = 0.5), conditioned on c."
- **Test:** Hartigan & Hartigan (1985) dip statistic D_n (DOI 10.1214/aos/1176346577), computed by one pinned implementation of the Hartigan (1985) AS 217 algorithm (implementation and version PENDING with the library pins, P6). The same code computes observed and table dips.
- **Data:** w at the two grid levels nearest the fitted transition, per readout, per c-level, on the seed's **final-partition eligible trials** of that bin (≤ 127 per seed). **4 dips per (seed-unit, c-level)** (2 bins × 2 readouts at the selected t_r; WL C3), plus 4 per dose-calibration seed-unit if the dose-selection criterion uses the dip.
- **Minimum sample:** a bin with fewer than the frozen n_trial eligible points is UNAVAILABLE (MP L80), never tested. The table covers every n from 4 to 127, so it does not depend on how R22's per-bin minimum is finally scoped.
- **p-value:** for sample size n, p = (1 + #{D_null,n ≥ D_obs}) / (N_tab + 1), with N_tab = **100,000** null dips per n, **drawn from Uniform(0, 1)** (the least-favourable unimodal null of Hartigan & Hartigan). Ties count as ≥. The count is an exact lookup in the sorted table (binary search), **with no interpolation** in D or across n. The smallest attainable p is 1/100,001 ≈ 1.0 × 10⁻⁵. At α_IGN = 0.01 (MP L204) the Monte Carlo SE of p is √(0.01·0.99/10⁵) ≈ 3.1 × 10⁻⁴.
- **Table construction:** RNG role **`ign-dip-null-table`** (Philox, the project's KAT-checked generator), keyed by (n, draw index), separate from every other role and never reused. Size 124 sizes × 100,000 = **12,400,000 null dips**, generated once **before any calibration** (an S0 construction step; it is a run and needs the S0 authorization), stored with its sha256 in the freeze record, and never regenerated.
- **Not adopted:** per-test simulated p-values and any interpolated published table. Per-test simulation is shown in §5.3 only as a **labelled hypothetical cost scenario**; it is not a fallback and cannot be switched to after any result is seen (A51 L171).
- **Worst-case count (n = 67, φ_c = 3, K_dc = 5):** observed dips 4 × 1,967,200 + 4 × 15,750 = **7,931,800**; one-off table **12,400,000**; at about 10⁴ ops per dip (WL), 7.932e+10 + 1.240e+11 ops; table lookups ≤ 17 comparisons each. At 9: 4,962,200 observed dips.

## 4. Network settling duration
Astra (A51 L173): "Reconcile "networks only: 5 tau settling" with the ledger's 20-step null runs. Fix one operative duration or an explicit conversion."
- **Source:** M L1127 reads "t_s = 5τ in plants (residual e^−5 < 1%); 20 steps in networks", rationale "For networks, 20 steps exceeds 2·d_c for typical d_c ≤ 10"; M L1128: "t_r = 3τ in plants; 5 steps in networks". The 5τ clause is the **plant** clause; AM-4 replaces it by t_s = 0 for scalar plants. The **network clause is already a step count**.
- **Operative duration (PROPOSED for the Lead): t_s,net = 20 network steps**, a literal integer in the freeze record, with an integer step-counter assertion (like (vii-b) for scalar n_EM). It is fixed: no tolerance-driven extension or early exit.
- **Explicit conversion:** one network step is the network time unit. To state M L1127's "5τ" in network time units, **τ_net is defined as 4 steps**, so 5τ_net = 20 steps. τ_net is a naming convention only; no network time constant is estimated, and nothing depends on τ_net except this identity.
- **Correction of the v2.6/#51 wording:** V26 L57 ("M L1127's t_s = 5τ applies to **networks only** (20 steps)"), V26 L104 (AM-4: "5τ/20-step settling and the tolerance apply to networks only") and #51 R3 ("M L1127's 5 tau settling applies to networks only") wrongly attach "5τ" to networks. The v2.7 text is: "M L1127's network clause (20 steps) applies to networks; its plant clause (5τ) is replaced for scalar plants by t_s = 0 (AM-4)."
- **Consistency with the ledger:** network trial = 20 settling + t_r,max 8 = **28 steps** (t_r grid {3, 5, 8}, V25 L198; WL L36); centre and quantile null runs = **20 settling steps** each (WL B2a/B2b), no readout; hysteresis trial-equivalents include settling.
- **Cost of settling (network steps; already inside lines A-network, B1, B2, B3, not added again):** at 67: trials 3,278,124,000 × 20 + dose calibration 72,009,000 × 20 + null runs 789,417,000 × 20 + hysteresis 12,906,000 × 20 = **83,049,120,000 settling steps**; at 9: **52,681,944,000**. At 2·d_h²·κ_net flop per step and 10⁻⁹ s/flop (UNVERIFIED): **≈ 189.0 CPU-h** (d_h 64, κ 1), **≈ 3,023.7** (d_h 256), **≈ 48,379.6** (d_h 512, κ 4) at 67; ≈ 119.9 / 1,918.1 / 30,689.5 at 9. Settling is about 71% of network trial cost (20/28) and all of null-run cost.

## 5. Revised maximum work (every runtime figure conditional and UNVERIFIED)
### 5.1 Op counts (exact; n = 67, full GRID Σ = 292, 15 C_cal / 20 C_conf cells, φ_c = 3, K_dc = 5)
- Scheduled trials **7,068,312,000** (4,005,072,000 + 45,720,000·67); at 9: 4,416,552,000.
- Dose calibration **≤ 72,009,000** trials (§1).
- Null runs: centre 72,417,000 + quantile 717,000,000 = **789,417,000**, 20 steps each.
- Hysteresis **≤ 27,828,000** trial-equivalents.
- Fits **≤ 84,066,900 optimizer calls**, ≤ 1,262,684,838,000 evaluations (§2); 9: 52,886,100 calls.
- Dips **7,931,800** observed + **12,400,000** one-off table (§3).
- Bootstrap ≤ 1.86 × 10¹² ops (B = 10,000, no refit; WL C4). KATs and fixtures negligible.

### 5.2 CPU-h by line (UNVERIFIED; per-unit envelopes as WL §1.2 and V26 §6)
Columns: **Low** and **High** as V26 (High = **maximum-cost envelope**: d_h 512, κ_net 4, c_step 30 µs, t_fit 0.3 s, φ_c 3, dose calibration on 7 network cells, K_dc 5, h = 1, dips at 10⁷ ops/s); **d_h 256** = V25 illustrative network point; **Ceiling** = High with every fit call saturating the pin (§2).

| Line | Low, 67 | d_h 256, 67 | High, 67 | Ceiling, 67 | Low, 9 | High, 9 | Ceiling, 9 |
|---|---|---|---|---|---|---|---|
| A trials: scalar | 105.3 | 105.3 | 15,792.5 | 15,792.5 | 65.5 | 9,826.0 | 9,826.0 |
| A trials: network (20 of 28 steps per trial are settling, §4) | 208.9 | 3,341.9 | 53,470.1 | 53,470.1 | 131.1 | 33,573.5 | 33,573.5 |
| B1 dose calibration (K_dc ≤ 5, §1) | < 0.1 | < 0.1 | 1,174.6 | 1,174.6 | < 0.1 | 1,174.6 | 1,174.6 |
| B2a null-centre runs (n_c = 101; 20 settling steps) | 3.3 | 52.7 | 843.7 | 843.7 | 2.1 | 529.8 | 529.8 |
| B2b null-quantile runs (n_q = 1,000; 20 settling steps) | 32.6 | 522.1 | 8,353.7 | 8,353.7 | 20.5 | 5,245.2 | 5,245.2 |
| B3 hysteresis sweeps | 1.2 | 13.6 | 272.7 | 272.7 | 0.8 | 170.9 | 170.9 |
| C1 fits: main + pooled selection + dose calibration + hysteresis (§2) | 580.1 | 580.1 | 7,439.9 | 85,151.8 | 362.4 | 4,654.5 | 53,271.6 |
| C3 dip statistics, observed (§3) | < 0.1 | < 0.1 | 2.2 | 2.2 | < 0.1 | 1.4 | 1.4 |
| C3b dip null table, one-off (§3) | < 0.1 | < 0.1 | 3.4 | 3.4 | < 0.1 | 3.4 | 3.4 |
| C4 seed-level bootstrap | < 0.1 | < 0.1 | 51.5 | 51.5 | < 0.1 | 32.2 | 32.2 |
| D1–D2 KATs, fixtures, root solves | < 0.1 | < 0.1 | < 0.1 | < 0.1 | < 0.1 | < 0.1 | < 0.1 |
| **Total (UNVERIFIED)** | **≈ 931** | **≈ 4,616** | **≈ 87,404** | **≈ 165,116** | **≈ 582** | **≈ 55,211** | **≈ 103,829** |

### 5.3 Change from V26 §6 and labelled scenarios
- **Low** 815 → **931**: pooled selection fits F2 (+116.0) and hysteresis fits F3 are now counted.
- **High** 85,860 → **87,404**: C1 5,901.6 → 7,439.9 (F2 pooled, F4/F5 dose-calibration fits and φ_c in dips); observed dips 2.2 and the one-off table 3.4 were previously uncounted.
- **Maximum-cost envelope** 103,038 → **87,404** (= High): V26's "Max" was High plus per-test simulated dips. That is no longer a procedure (§3), so it leaves the envelope. For comparison only, the **hypothetical per-test-simulation scenario** (N_null = 10⁴ per test, 10⁷ ops/s) is ≈ 109,437 CPU-h (dip line ≈ 22,033).
- **Pin-saturated ceiling ≈ 165,116 at 67 (≈ 103,829 at 9)**: the largest figure the frozen counts and pins allow under these per-unit costs. Fits then dominate (≈ 85,152).
- Network lines still scale with d_h²·κ_net (d_h PENDING, P4); every figure is a hypothetical scenario, not a measured bound (A51 L175). Wall-time caps are separate operational limits and need not guarantee completion.

## 6. Carry-overs for v2.7
**6.1 Cost-drop attribution (RDLP2 L-1, CARRY-OVER).** Replaces the room summary's attribution. "Change from WL: High and Max fall because **n_dc 67 → 9 with dose calibration on network cells only** (B1 11,296.6 → 1,174.6; Max 13,849.3 → 1,174.6), **n_c capped at 101** instead of up to 1,001 (B2a 8,362.0 → 843.7), and **G 2 → 1 at the maximum** (no frozen g > 2; A-scalar Max 31,584.9 → 15,792.5). **Not dropping CV:** CV was never in WL's totals (WL L95), so its removal only drops the ×6 contingency (C1 Max ≈ 35,410 → ≈ 5,902). Low rises (505 → 815) from 3 restarts and scheduled hysteresis." §5.3 adds this file's further changes.

**6.2 v2.6 lock time (RDLP2 L-2, disclosure).** V26 L4 says "Written: 2026-11-01, about 12:36–12:50 PM ET". The file was locked (chmod 444, mtime) at **12:39:15 PM ET**; the range in its header runs past the lock. No content effect. V26 is not edited.

**6.3 Labels (RDLP2 L-3).** V26 L30's "C2 and C3 §1" means **E2C2 and E2C3 §1** (E2C2 = `5100f4de826dacbd422be92e056f58578fc9a5c332353885ebb0f50f62cf8092`, E2C3 = `2f813ba4bb58507241ced0bea97354fdfc63990015786feaadeb4709e4630eec`), the §10 abbreviations.

**6.4 Astra's wording (RDLP2 L-4).** V26 L49's "(which Astra found not guaranteed for every g, A50 L153)" is a paraphrase. Astra wrote: "direct fixed-point iteration is not guaranteed to converge **for every negative g**" (A50 L153). The v2.7 text uses that wording; AM-9 is unaffected.

**6.5 Named amendments AM-12..AM-14 (CNA's three items; recorded per the Lead's instruction, to be put to Astra).**
| # | Name | Supersedes / departs from | New rule (pre-data) | Source |
|---|---|---|---|---|
| AM-12 | **NOT ASSESSED → UNRESOLVED** | E2C3 §1 (and E2C2 §1) "otherwise the row FAILS"; V25 L56; ER1 E1; E2-3; E2-4 | E50-1's row outcome supersedes corr3: "NOT ASSESSED → UNRESOLVED: never PASS, and never FAIL on that ground alone" (CE50 L93). FAIL comes only from a row-0 licence or an assessable screen violation | CE50 §1.4; CE50a1 R1; V26 §1 |
| AM-13 | **Single σ_ref from IGN-P1** | any per-row noise scale (M L1126's ‖x_hi − x_lo‖ per plant) | One σ_ref = 0.05·Δ_ref for every scalar IGN row, Δ_ref = 2x* from bistable IGN-P1 at s = 0, frozen hex, never recomputed from a row's own attractors (A50 L142) | CE50 L-6; V26 §3 |
| AM-14 | **EM recursion as the validated object, S_max = 8** | the SDE reading of the plants | The discrete Euler–Maruyama recursion is the tested plant; the SDE is interpretation only (A50 L151); |u| ≤ S_max = 8 asserted over the full frozen input table and at every root call | CE50 L-8; CE50e1 E1-1; RDPP V-6; V26 §3 |

**6.6 Fisher–Yates counter (restated; RDLP2 §3).** k_FY is the Fisher–Yates loop index, k_FY = 507…1; Philox counter **(508 − k_FY, 0, 0, 0)**; **j = w0 mod (k_FY + 1)** (CE50e1 L49; RD26c2 L81). Positions per (seed, bin) of 508 after the shuffle: fitting a[0..253], selection a[254..380] (V25 L83; RD26 L50), final a[381..507]; per seed 2,286 / 1,143 / 1,143.

**6.7 Zero denominators (explicit rule; A51 L37).** No rate is evaluated on a zero denominator. A screen whose denominator is zero, or whose availability condition fails (S_cons and S_wc: n_cons = n4 + n4B + n4U + n5 ≥ 36), is **not evaluated**; the row is then **UNRESOLVED** (insufficient support) unless step 1 (row-0 licence) or an assessable screen at step 2 has already given FAIL. It is **never PASS**. PR is evaluated on its fixed denominator 200. Separate per-screen availability definitions are part of the E51-1 response, not this file.

**6.8 AM-2 rationale (Astra's correction, A51 L57).** v2.6 and #51 implied that 5-fold CV leaks. Corrected rationale: "five-fold cross-validation does not inherently leak outcomes. Properly nested cross-validation can be valid. The problem was its unresolved interaction with the separately declared final partition." ΔLL-HO is kept because it removes that ambiguity, not because CV inherently leaks.

**6.9 Fitter wording (A51 L139; for E51-3).** "absolute gtol 1e-8" is replaced by "gtol 1e-8 on the maximum absolute component of the projected gradient of the mean NLL; ftol is a separate stopping condition; the termination reason and the final projected-gradient residual are recorded for every call". Bounds, starts, label ordering and all-starts-failed behaviour are E51-3 items, not settled here.

**6.10 Full-grid wording (A51 L177).** V26 L96's "The full-grid cost is the expenditure" becomes "**full-grid work is scheduled**; integrity stops and cap-limited work can prevent completion, and such work remains INCOMPLETE". Early stopping stays NOT ADOPTED.

## 7. PENDING (unchanged unless stated)
| # | Item | Status |
|---|---|---|
| PD-2 | K_dc | **PROPOSED hard bound 5** (§1); Lead ruling pending |
| PD-1 | Network Var(w) floor | PENDING (CNA, P4) |
| PD-3 | Network width d_h, κ_net | PENDING (P4); network lines scale with d_h²·κ_net |
| PD-4 | Fitter library pin; maxfun counting under scipy 1.18.1 | PROVISIONAL, UNVERIFIED |
| PD-7 | Dip p-value method | **Closed by proposal** (§3); dip implementation pin PENDING (P6) |
| PD-new-1 | Hysteresis transition estimator (F3) | PENDING; counted at ≤ 6 calls per seed-unit |
| PD-new-2 | Whether ŝ* is fitted per t_r and readout (F2: 18 vs 3 calls) | PENDING; worst case 18 counted |
| PD-new-3 | Per-ledger caps (P5) incl. B1 at 72,009,000 | PENDING |
| — | E51-1, E51-2, E51-3 | Not answered here |

## 8. Discrepancies found
1. **Fits under-counted in V26/WL:** "fits 55,656,000–70,819,200" counted F1 only. Pooled selection fits (F2, ≤ 846,000 calls), hysteresis fits (F3, ≤ 11,803,200), and dose-calibration fits (F4/F5, ≤ 598,500) were missing. Total ≤ 84,066,900 calls.
2. **Dips under-counted:** V26's 6,184,000 = 4U ignores the NC1 c-level factor (4 × U_eff = 7,868,800 at φ_c = 3) and dose calibration (63,000). The cost of computing the observed dip statistics themselves was never costed (only simulated null dips were).
3. **Max envelope falls** (103,038 → 87,404) because per-test simulated dips leave the procedure; the new pin-saturated ceiling (165,116) is higher than any earlier figure.
4. **"5τ in networks" wording** in V26 L57/L104 and #51 R3 misreads M L1127 (§4). The ledger's 20-step runs were right.
5. **τ_net** is a definition introduced here (4 steps); M has no network time constant.
6. **A51 L75** says "At n_q = 198 the rank is 198; at 199 it is 198" — consistent with AM-10 (r_q at 199 = ⌈0.99·200⌉ = 198). No action.
7. The fitter's maxfun-overshoot reading (≤ maxfun + maxls) is not verified against scipy's source; it only affects the ceiling by 0.13%.
8. **"Astra L153"** in the task means A50 L153 (#50), not A51 L153 (A51 L153 is the seed-unit identity).
9. V26 was locked at 12:39:15 PM ET, before its header's stated end time (§6.2).

*DESIGN ONLY. Nothing was run, timed, benchmarked, installed, sent or posted, and no existing file was edited. X1–X5 and the claim ceiling unchanged. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: d1c09ef54dbb4d59cb54c147d25cde7bd7b8eae15a3fc0525112bced70d6dd51
