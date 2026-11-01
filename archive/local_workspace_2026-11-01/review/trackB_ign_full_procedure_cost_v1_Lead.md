# Track B IGN instrument: full-procedure cost estimate v1 (Lead)

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** This is a new, additive file. It edits no existing file. No IGN, plant, harness or instrument code was written or run. No training, simulation, Monte Carlo, Stage 0, calibration, pilot or checkpoint inspection took place. **No runtime was measured for this estimate.** Every per-trial or per-fit time below is a non-running estimate built from design operation counts and generic published hardware throughput, and each one is labelled **UNVERIFIED**. The only computation was exact integer and binomial arithmetic (Python) and SHA-256.

- **Written:** 2026-11-01, about 11:05–11:30 AM ET, by the Lead's executor.
- **Governing ruling:** Astra #49 Q2 and E49-2 (raw `/workspace/astra_consult49_response.txt`, sha256 `6b66bbba1b800aa3dc8aacd024a827a82acb3346216cad8f19397cde66934468`; "A49 Ln" = line n).
- **Shorthand:** "V2.3" = freeze-prep v2.3 addendum; "V2.5-RD" = RD's E49-2 section for v2.5 (`trackB_freezeprep_v2_5_E49_2_IGN_wording_RD.md`, `ae80cc12…`); "M Ln" = merged scope v3.6; "S2.1 Ln" = merged scope v2.1 (carried by reference into v3.6, M L2349); "CNA2 Ln" = CNA v2 half (`17832b01…`); "MP Ln" = measurement plan v1.
- **Safety (binding, unchanged):** X1–X5 are unchanged. There is no host coupling. The standard string "no additional stop-associated reward, penalty or terminal return" (#42 L223) applies. The claim ceiling (#41 L304) is unchanged. No consciousness, awareness or sentience claim is made or implied.

---

## 0. Headline

| Quantity (all partitions, 254/127/127) | Per IGN generator × dose cell | Over the 16 declared cells (§2) |
|---|---|---|
| Sample-size calibration over GRID (Σ = 292) | **267,004,800** | **4,272,076,800** |
| PZ5 §4.2 step 3a envelope reporting, 2 × 914,400·n_seed* | 1,828,800·n_seed* (122,529,600 at 67) | 29,260,800·n_seed* (1,960,473,600 at 67) |
| Confirmation, **914,400·n_seed*** (V2.5-RD L88) | 914,400·n_seed* (61,264,800 at 67) | 14,630,400·n_seed* (980,236,800 at 67) |
| **Total scheduled trials** | 267,004,800 + 2,743,200·n_seed* | **4,272,076,800 + 43,891,200·n_seed*** |
| at n_seed* = 67 (R26 budget only) | 450,799,200 | **7,212,787,200 (≈ 7.21 × 10⁹)** |
| at n_seed* = 9 (GRID floor) | 291,693,600 | **4,667,097,600 (≈ 4.67 × 10⁹)** |

The **range is about 70 to 37,000 CPU-hours (UNVERIFIED)** at n_seed* = 67, from the formula in §4. That is trials plus model fits. The width comes from two things the design leaves ABSENT: the integration step Δt, and how the code is implemented. **No figure in this file is a measurement.** R25 (M L2390) requires the per-unit cost u to be measured in the S0 preflight on code-audit plants, and that requires its own authorization.

Four conditional items are not included in the totals (§3): IGN dose calibration, settling-tolerance null runs, hysteresis sweeps, and simulated dip p-values.

---

## 1. Trial counts under 254/127/127 (task 1)

**Does V2.3 already assume 254/127/127?** Yes. Astra froze fitting 254, selection 127 and final 127 per (seed, required bin) (A49 L64–L69). That is 508 = 4 × 127, exactly the D27 50/25/25 shares (M L616). So V2.3 §5's "All partitions (×4, D27)" column is the frozen allocation: 306,324 per replicate at 67; 61,264,800 confirmation; 267,004,800 calibration. V2.3 had flagged that column as "open" because the partition counts were not yet fixed. A49 closes that, and V2.5-RD (1) carries the closure. **No recomputation was needed.** Every figure was re-derived here and matches.

Astra's arithmetic was re-checked as well (exact): P(Bin(127, 0.9) ≥ 100) = 0.9999503753, 603rd power = 0.9705188816, n = 126 → 0.9349005775 (A49 L53–L58).

**Deterministic slot assignment.** IGN trials are assigned to partitions by a deterministic, outcome-free rule from the frozen schedule, which gives exactly 254/127/127 in every (replicate, seed, bin) (V2.5-RD (1a), rule PENDING CNA). The counts below are therefore exact scheduled counts, not expectations. A D27 environment-seed hash split would give these shares only in expectation. Missing or invalid slots stay in the denominator and are never topped up (V2.5-RD (3a)), so scheduled count = cost count.

| Partition | Per (seed, bin) | Per seed (K_s = 9) | Per replicate at 67 | Confirmation (200 reps, 67) | Sample-size calibration (200 × Σ292) |
|---|---|---|---|---|---|
| Fitting | 254 | 2,286 | 153,162 | 30,632,400 | 133,502,400 |
| Selection | 127 | 1,143 | 76,581 | 15,316,200 | 66,751,200 |
| Final | 127 | 1,143 | 76,581 | 15,316,200 | 66,751,200 |
| **All** | **508** | **4,572** | **306,324** | **61,264,800** | **267,004,800** |

In general, confirmation = 200 × 4,572 × n_seed* = **914,400·n_seed*** per generator and dose (V2.5-RD L88). Calibration = 200 × 4,572 × 292 = 267,004,800, fixed by the GRID {9, 12, 16, 20, 24, 32, 48, 64, 67} (M L377).

**Calibration lines V2.3 left out.** The L-CAL ledger (M L2161) includes "sample-size calibration (§4; R_cal,n = 200 over GRID; **3a envelope points**)". PZ5 §4.2 step 3a (M ~L1963) reports the same OCs at σ_s/margin = 0.25 and 0.5 at the selected n_seed: "Cost ≤ 2 × 200 × 67 = 26,800 seed-units per generator × dose". In trials that is 2 × 914,400·n_seed* = 1,828,800·n_seed*, or 122,529,600 at 67. Neither V2.3 §5 nor the V2.5-RD L88 formula includes it. It is included here as a calibration line. Dose calibration (R_cal,dose = 50) is conditional and is covered in §3.

## 2. IGN generators and doses the scope declares

V2.3 §5 and V2.5-RD L88 leave the generator × dose count PENDING. Merged v3.6 carries the IGN rows by reference from v2.1 §P1/§P3 (M L2349). M L3187 says "their required rows as declared in merged v3.4 (unchanged)". The rows below are read from S2.1 L248–L255 and CNA2 §2.6. This is a reading, not a freeze.

| Row | Role | Dose parameter, declared levels | Cells | Source |
|---|---|---|---|---|
| IGN-P1 | P | nominal positive at 1.5× margin (D26); no separate IGN dose grid found | 1 (ASSUMED) | S2.1 L248; M L615 |
| IGN-N1 | N | g < 1; no grid found | 1 (ASSUMED) | S2.1 L249 |
| IGN-NC1 | confound | Δs ∈ {2, 4} grid steps | 2 | CNA2 L296 |
| IGN-NC2 | confound | clip quantile {0.8, 0.6} | 2 | CNA2 L297 |
| IGN-NC2r | mechanism-present | ABSENT | 1 (ASSUMED) | S2.1 L252 |
| BOTTLENECK-ONLY | mechanism-present | g_b, 2 levels | 2 | CNA2 L298 |
| RAND-INIT (IGN part) | mechanism-present / C-LEARN | g_0 ∈ {0.9, 1.0, 1.1}× default | 3 | CNA2 L283 |
| Architecture-imposed | C-LEARN control | β, 2 levels | 2 | CNA2 L284 |
| IGN-LIM | designated limitation | s* offset, 2 levels | 2 | CNA2 L309 |
| **Total** | | | **16** | |

**Sensitivity.** CNA2 L328 mentions "plus dose 0" for confound rows. If NC1 and NC2 each carry a dose-0 cell, there are 18 cells, and every total scales by 18/16 (8,114,385,600 at 67). The calibration loop covers "every labelled row: positives, negatives, confound rows" (M ~L1950). LIM and mechanism-present rows are included in the 16 here, which is the conservative choice. If calibration covered only P, N and confound rows (P1, N1, NC1 × 2, NC2 × 2 = 6 cells), calibration lines would scale by 6/16.

Three generator types run on networks rather than scalar plants: RAND-INIT, Architecture-imposed and BOTTLENECK-ONLY (untrained nets or gated modules). Their per-trial cost depends on architecture sizes that are still open (P4, M L3231). §4 gives them a separate formula.

## 3. What is a trial, a fit, or a selection step (task 3)

| Cost class | Unit | Count per cell at n_seed* = 67 (all roles) | Source |
|---|---|---|---|
| **Trials** (scheduled) | one reset-to-x_ref probe at strength s_j: settle, apply input, read w = ‖x_ws(t_0 + t_r) − x_ref‖, pre- and post-nonlinearity (two reads of one trajectory) | 450,799,200 | §1; M L314; A49 L64–L69 |
| **Model fits** (fitting partition) | per seed-unit: graded null H0 (4-parameter logistic μ, log-linear σ, skew-normal γ) and mixture H1 (logistic π, shared μ_hi/μ_lo, σ_hi/σ_lo) fitted to that seed's 2,286 fitting trials across all 9 bins. They are fitted **per seed, not per (seed, bin)**: each model is one function of s across bins. They are fitted per level of c where c exists (NC1), and NC1 is also fitted without c (REPORTED) | 98,600 seed-units (13,400 conf + 58,400 cal + 26,800 3a) × F fits | MP L65–L66, L86; M L313 |
| **Selection** (selection partition) | choosing t_r from the frozen t_r grid, the near-transition bins and the fit choices, by scoring candidate fitted models on 1,143 selection trials. Each t_r candidate needs its own H0/H1 fit, so the fit count F scales with \|t_r grid\| (ABSENT) | included in F | M L313, L376–L377 |
| **Final evaluation** | held-out ΔLL on 1,143 final trials (likelihood evaluation, no fit); Hartigan dip at the 2 near-transition bins (127 points each) per readout; Ashman D from the H1 parameters | 98,600 × (2 bins × 2 readouts) ≈ 394,400 dip tests | MP L69–L75 |
| **Aggregation** | seed-level bootstrap, B = 10,000 resamples of seed statistics (no refit assumed), label at level 1 − α/m | 2,400 replicate-evaluations per cell (200 conf + 9 × 200 cal + 400 3a) | M ~L1957; D15 M L604 |
| Conditional, **not in totals** | (a) IGN dose calibration R_cal,dose = 50, only if the P1 imitation reference is not analytic: 50 × 306,324 = 15,316,200 trials if a dose-calibration replicate is one 67-seed replicate (size ABSENT). (b) Settling-tolerance null-input runs on the fitting partition (count ABSENT; M L1129). (c) Hysteresis sweeps, separate and unscheduled (V2.5-RD (2); count ABSENT). (d) Dip p-values by simulation rather than tables (method ABSENT; if simulated with N_null draws, ≈ 394,400·N_null extra dip computations per cell) | — | M L373, L1140; CNA2 L241 |

## 4. Per-trial and per-fit cost model (task 2)

**Measured timings.** No IGN plant, harness or comparable plant exists in `/workspace` or `/workspace/repo` (V2.3 §5 search; rechecked by grepping for dip/Ashman/bistable code, and none was found). The only recorded timings found are `wall_seconds` fields in `/workspace/repo/sub_a0_cal_results_v1/stage2/*.json` (for example job_2000_e1.json: 37.62 s). Those are trained-torch-agent calibration jobs from another study, not a scalar SDE probe, so **they are not used**. **There are no measured timings for this design.**

**Scalar-plant trial (IGN-P1, N1, NC1, NC2, NC2r, LIM).** The plant is τ·dx/dt = −x + tanh(g·x + s + ξ), with ξ ~ N(0, (0.05‖x_hi − x_lo‖)²) per unit time (M L1126). Settling is t_s = 5τ and readout t_r = 3τ (M L1127–L1128). The trial is simulated to t_s + max(t_r grid) ≥ 8τ.

- Steps per trial: N_st = (t_s + t_r,max)/Δt. **Δt is ABSENT.** Illustration: Δt = τ/20 gives 160 steps; τ/100 gives 800 steps.
- Operations per step, from the design (UNVERIFIED counts): one Philox4x64-10 block (10 rounds × 2 64×64→128 multiplies plus about 6 xor/add ops, about 80–100 integer ops; M E48-4 RNG), one Box–Muller normal (log, sqrt, cos; cos only, A49 L116), and one Euler update (tanh plus a few multiply-adds). That is about 200–300 scalar op-equivalents per step.
- Throughput, generic published orders of magnitude (UNVERIFIED): a compiled or vectorised scalar loop on one modern core at about 10⁹ simple ops/s gives about 0.1 µs/step. An interpreted CPython loop at about 10⁷–10⁸ bytecode ops/s gives about 5–20 µs/step.
- **Per-trial CPU time c_trial (UNVERIFIED):** compiled 16 µs (160 steps) to 80 µs (800 steps); interpreted about 0.8 ms (160 steps) to about 16 ms (800 steps). Batching trials across slots (independent by construction, V2.5-RD (2)) would sit at or below the compiled figures.

**Network-type trial (RAND-INIT, Architecture-imposed, BOTTLENECK-ONLY).** Settling is t_s = 20 steps and t_r = 5 steps, so 25 network steps (M L611 D22). c_trial,net ≈ 25 × 2·d_h² × c_flop, where d_h is the recurrent width (ABSENT, P4) and c_flop is the effective seconds per flop (UNVERIFIED; about 10⁻⁹ s unbatched on one core). Illustration only: at d_h = 256, that is 3.3 × 10⁶ flop per trial, about 3 ms. These 7 cells are about 7/16 of the trials, so the network formula can dominate if d_h is large.

**Fit (UNVERIFIED).** One H1 or H0 log-likelihood evaluation on N = 2,286 points is about 1–2 × 10⁵ flops. With gradients (about 3×) and 100–500 quasi-Newton iterations, that is about 4 × 10⁷ to 2 × 10⁸ flops per fit, so t_fit ≈ 0.02–0.2 s. Fits per seed-unit: F = 2 models × \|t_r grid\| × 2 readouts × restarts × c-factor. This gives F ≈ 4 (one t_r, no restarts) to 60 (5 t_r × 3 restarts); every factor is ABSENT except models and readouts.

**Formula (complete procedure):**

> CPU = Σ_cells [ T_cell · c_trial(cell) ] + U · F · t_fit + (bootstrap + dip + conditional items),
> T_cell = 267,004,800 + 2,743,200·n_seed*, U = Σ_cells (58,400 + 600·n_seed*) seed-units, the bootstrap is 2,400 replicate-evaluations × 10⁴ × n_seed sums per cell (≈ 2.6 × 10¹⁰ ops in total at 67, under an hour even interpreted; UNVERIFIED).

**Range at n_seed* = 67, all 16 cells treated as scalar plants (UNVERIFIED):**

| Component | Low | High |
|---|---|---|
| Trials, 7.2128 × 10⁹ × c_trial | 32 CPU-h (16 µs) | 32,057 CPU-h (16 ms) |
| (mid points) | 160 CPU-h (80 µs) | 1,603 CPU-h (0.8 ms) |
| Fits, 1,577,600 seed-units × F × t_fit | 35 CPU-h (F = 4, 0.02 s) | 5,259 CPU-h (F = 60, 0.2 s) |
| Bootstrap, final-partition dip (table p) | < 1 CPU-h | ≈ 1 CPU-h |
| **Total** | **≈ 70 CPU-h** | **≈ 37,300 CPU-h** |

At n_seed* = 9, trials fall to 4.667 × 10⁹, which is 0.647× the trial line. Calibration dominates either way: it is 59% of trials at 67 and 92% at 9. Wall-clock time = CPU-h / parallel cores used, because trials and seed-units are embarrassingly parallel. That figure is a feasibility number, not a validity one (§5 L5).

## 5. Levers L1–L5: what each would change (task 4; no lever is chosen)

Astra's rule is that the allocation is retained and the complete procedure is costed. "If that is unaffordable, make an explicit prospective reduction before running; do not weaken the rules during execution." (A49 L87). Under A49 L47, "before running" means before any calibration, pilot, feasibility or diagnostic output exists. A reduction is a prospective gate or control change under Amendment A-2026-10-24 (record `2f29a07a…`). The Lead can approve it after addressing Astra's review conditions, with Aidan informed. Changes to X1–X5, the claim ceiling, or anything after data collection starts need Aidan's explicit approval.

| Lever | Astra (verbatim) | What it would change in the cost | What it would change in the design |
|---|---|---|---|
| L1, 100-trial per-seed quota | "The number 100 is a prospective convention … Reducing it requires revising and validating the instrument, not reinterpreting its denominator." (A49 L81) | All trial lines scale with n_s. 508 = 4 × n_s under 50/25/25 | The R22 precision rationale (SE 0.05 = one m_IGN margin unit at p = 0.5, M L2387) no longer holds. The instrument must be revised and re-validated. V2.3 D47 forbids n_s < 127 under the current instrument |
| L2, fewer bins K_s | "possible prospectively, but changes the declared input-strength coverage and IGN procedure. It is not a clerical saving." (A49 L82) | Trials scale linearly with K_s. n_s might drop slightly, because the joint quota spans K_s·n_seed cells | Changes the declared ≥ 9-level coverage (MP L61), B_req = K_s, the per-bin coverage rule, and the fitted s-curve support |
| L3, fewer replicates or doses | "changes the precision or tested domain. It cannot retain the existing operating-characteristic claims without recalculation." (A49 L83) | Calibration and confirmation scale with R and with the number of cells (16) | The CP bounds at R = 200 (coverage SE 0.0154, the 0.08 false-MET bound) need recalculation. Dropping a required dose conflicts with the §8.3 blocking rule (M ~L2172) and needs an explicit amendment |
| L4, lower n_seed by calibration | "already legitimate. Cost alone cannot override that selection." (A49 L84) | Confirmation and 3a scale with n_seed*: 2,743,200·n_seed* per cell. Calibration (267.0M per cell) does not change unless the GRID changes | None. n_seed* is whatever the frozen rule selects (M §5.7 step 3) |
| L5, more hardware (e.g. Aidan's DGX Spark) | "changes feasibility, not validity. Trial counts alone do not justify a hardware choice." (A49 L85) | No change to trial or fit counts. Wall-clock ≈ CPU-h / usable parallel cores; the network cells could use an accelerator | None. R25 caps need u measured in the S0 preflight on the hardware actually used (M L2390). No hardware decision is made here |

## 6. Inconsistencies and gaps found in the inputs

1. **3a envelope cost omitted.** V2.3 §5 and V2.5-RD L88 cost calibration as 200 × 4,572 × 292 only. L-CAL (M L2161) and PZ5 §4.2 step 3a add 2 × 200 × n_seed* seed-units per cell: +122,529,600 trials per cell at 67, or +37% on the V2.3 per-cell total of 328,269,600.
2. **Generator × dose count never totalled.** V2.3 and V2.5-RD leave it PENDING. The scope implies 16 cells (§2), but IGN-P1, N1 and NC2r have no numeric dose grid, and CNA2 L328's "plus dose 0" is ambiguous (16 vs 18).
3. **V2.3 formula shape.** "G × Dose × …" assumes the same number of doses for every generator. The declared rows have 1–3, so the total must be Σ over (g, k) cells.
4. **Is the calibration GRID run in full?** The PZ5 §4.2 loop runs "for n in GRID (ascending)" and picks n* = the smallest passing n. It does not say whether larger n must still be run. Σ292 (V2.3, V2.5-RD) assumes all nine are run. If the loop stopped at the first pass, calibration would be as low as 200 × 4,572 × 9 = 8,229,600 per cell. This needs an explicit prospective statement either way. It is not a cost lever to pick during execution.
5. **R25 workload line** (M L2390) gives "sample-size calibration 200 × Σ(generator × dose)" with no ×|GRID| factor. That conflicts with the §4.2 loop. R25 is tagged as superseded by PZ5 §8.2, but the line is still in the file.
6. **Settling in plants.** IGN-P1 resets analytically to x_lo (x_ref = x_lo, S2.1 L242), yet M L1127 sets t_s = 5τ "in plants". Whether plant trials include settling changes steps per trial by 8/3. Δt and the t_r grid are ABSENT.
7. **D27 vs exact counts.** D27's hash split cannot give exactly 254/127/127 (V2.5-RD §9 item 1). This estimate assumes the deterministic slot rule (rule PENDING CNA).
8. **Footer conventions differ in wording.** This brief said "hash of all bytes above the '---' line". Project files (v2.4, amendment record, V2.5-RD) hash every byte above the `sha256 of all content above this line:` line, which includes the `---` line. This file follows the project files.

## 7. Inputs (sha256 recomputed this pass)

| Path | sha256 |
|---|---|
| `/workspace/astra_consult49_response.txt` | `6b66bbba1b800aa3dc8aacd024a827a82acb3346216cad8f19397cde66934468` |
| `/workspace/review/trackB_freezeprep_v2_5_E49_2_IGN_wording_RD.md` | `ae80cc122a284b16d96f4a02144c6a9a57a104fe1c5402551ca34cada5dede72` |
| `/workspace/review/trackB_freezeprep_v2_3_addendum_RD.md` | `48f75cfb37f56e8a076a18bfe671b6910fdca8da9bbf844b4795d5dea46a70d8` (footer `34a2555d…` verified) |
| `/workspace/review/trackB_freezeprep_v2_4_governance_addendum_RD.md` | `cf56c653dae28f9acee5be28d4f7a67568ce3aedfab933db308408f714e1cd9d` |
| `/workspace/review/trackB_freezeprep_v2_2_addendum_RD.md` | `9c10cbe0d1beb4e20c86c1252114390f63a658f5c6785bd613e239aab955dafe` |
| `/workspace/review/trackB_freezeprep_v2_1_addendum_RD.md` | `7b1a17d766d341865bf5b6465794168a06c648be7d28c4da25e0c2fcab7fe3ba` |
| `/workspace/review/trackB_freezeprep_v2_consolidated_RD.md` | `b41f0e1068fee9fec0dc2a6ece4879cebec510c0729f6eed2e45e3ca26bff55c` |
| `/workspace/review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` |
| `/workspace/review/trackB_instrument_validation_scope_v2_1_merged_RD.md` | `8ea6abc50b3929a39688aa54b1a1d66fe34c8ef17b3c5dfae98cc8efa79862de` |
| `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` |
| `/workspace/review/trackB_scope_v3_6_CNA_E48_response_v1.md` | `90fcb1fb762a22db91cde5bd4fd68a683d28d6a78c8efe9ca21a13e1e103f1ce` |
| `/workspace/review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` |
| `/workspace/review/constitution_amendment_A-2026-10-24_record.md` | `2f29a07a617464e1b0a30ad77ce7c67367f31208e749f6bcbff938fa8f7c2dd6` |

*DESIGN ONLY. Draft, not frozen. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No host coupling. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: c7d396f525169b869d37d34a2b96e537b972cdcee9b253514ae297ce9b6e4783
