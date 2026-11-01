# Track B IGN cost v1: RD light pass and items 2–4 (with item 1 settled)

Author: Research Delegate (RD). Written Sun Nov 1 2026, 11:23 AM ET (box `date`).
**STATUS: DESIGN/TEXT ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** This is a new, additive file that edits no existing file. Nothing was trained, simulated, executed, benchmarked or timed. No Monte Carlo was run. The only computation was exact integer/rational arithmetic (Python `fractions`) and SHA-256. Every CPU-hour figure below is arithmetic on the cost file's stated, **UNVERIFIED** operation counts and throughputs. None is a measurement. Astra's raw text governs; "A4x Ln" = line n of `/workspace/astra_consult4x_response.txt`. "LC Ln" = the Lead's cost file; "M Ln" = merged v3.6; "S2.1 Ln" = merged v2.1; "CNA2 Ln" = CNA v2 half; "MP Ln" = measurement plan v1; "CE49 Ln" = CNA's E49-1/E49-3 file; "V2.5-RD" = RD's E49-2 section.

## 0. Inputs (sha256 recomputed this pass; footers recomputed where present)

| Path | Whole-file sha256 | Footer (stated = recomputed) |
|---|---|---|
| `review/trackB_ign_full_procedure_cost_v1_Lead.md` | `7d4cbbad73d246425db425a6bf8231253d33c4cde07d4426f346650c16b9345d` (prefix 7d4cbbad ✔) | `c7d396f525169b869d37d34a2b96e537b972cdcee9b253514ae297ce9b6e4783` ✔ (c7d396f5) |
| `review/trackB_scope_v3_6_CNA_E49_1_E49_3_v1.md` | `d620918f9cb463639ca97b6b303c476b9f7eba60e831165b7ec4e18ee55e4bfa` (d620918f ✔) | `fbb1e975…` ✔ |
| `review/trackB_freezeprep_v2_5_E49_2_IGN_wording_RD.md` | `ae80cc122a284b16d96f4a02144c6a9a57a104fe1c5402551ca34cada5dede72` | `d0736ba8…` ✔ |
| `review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` | `bb074b33…` ✔ |
| `review/trackB_instrument_validation_scope_v2_1_merged_RD.md` | `8ea6abc50b3929a39688aa54b1a1d66fe34c8ef17b3c5dfae98cc8efa79862de` | — |
| `review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` | — (errata 1 `c2cd0732…`, 2 `5ddde854…` checked: no IGN dose change) |
| `review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` | — |
| `review/trackB_freezeprep_v2_3_addendum_RD.md` | `48f75cfb37f56e8a076a18bfe671b6910fdca8da9bbf844b4795d5dea46a70d8` | `34a2555d…` ✔ |
| `astra_consult49_response.txt` | `6b66bbba1b800aa3dc8aacd024a827a82acb3346216cad8f19397cde66934468` | — |
| `astra_consult44_response.txt` | `49afbb5d1ca63f0db692f3123e85c7ccf1c2870dbd45b48d639d39c30bc22060` | — |
| `astra_consult43_response.txt` | `9a46cb81cf50b988a0ece75d444e90921f14b0751de13b0d7b6c3fe207f79cf4` | — |
| `astra_consult42_response.txt` | `e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847` | — |

Every hash in this table was recomputed this pass. The four hashes the brief supplied (cost file 7d4cbbad / footer c7d396f5, CNA E49 file d620918f, V2.5-RD ae80cc12) match. No mismatch was found.

## 1. Correction to V2.5-RD §7 (acknowledged)

The V2.5-RD §7 confirmation line, **200 × 4,572 × n_seed\* = 914,400·n_seed\* trials per generator × dose cell**, is correct and **is not superseded**. My omission was the **PZ5 §4.2 step 3a calibration-side lines**. M L1967, verbatim: "**3a [v3.3 E43-4].** At the selected n_seed only, the same OCs are REPORTED at the other two envelope points, σ_s/margin = 0.25 and 0.5. Nothing is selected on them. Cost ≤ 2 × 200 × 67 = 26,800 seed-units per generator × dose (calibration ledger, §8)." M L2161 (L-CAL) includes "3a envelope points". In trials, step 3a is 2 × 914,400·n_seed\* = **1,828,800·n_seed\*** per cell, on the calibration ledger. The corrected per-cell total is:

> calibration ledger: 267,004,800 + 1,828,800·n_seed\*; confirmation ledger: 914,400·n_seed\*; together **267,004,800 + 2,743,200·n_seed\***.

V2.5-RD §7 (ii)'s list of procedure components should also have named "step 3a envelope points". This file records the correction additively; V2.5-RD itself is unchanged.

## 2. Light pass of LC (every exact figure recomputed)

| LC figure (line) | Recomputed | Verdict |
|---|---|---|
| Calibration 200 × 4,572 × 292 = **267,004,800** per cell (L16, L44) | 267,004,800 | **CONFORMS**. The full GRID runs (§3) |
| 16 cells: 4,272,076,800 (L16) | 16 × 267,004,800 = 4,272,076,800 | CONFORMS (arithmetic); the cell count is item 2 (§4) |
| Step 3a 1,828,800·n; 122,529,600 at 67 (L17, L46) | 2 × 914,400 = 1,828,800; × 67 = 122,529,600 | CONFORMS. Citation edit: "M ~L1963" → **M L1967** |
| Confirmation 914,400·n; 61,264,800 at 67 (L18, L44) | 200 × 4,572 = 914,400; × 67 = 61,264,800 | CONFORMS |
| Per cell **267,004,800 + 2,743,200·n** (L19, L98) | 914,400 × 3 = 2,743,200 | **CONFORMS** |
| Per cell 450,799,200 at 67; 291,693,600 at 9 (L20–L21) | 267,004,800 + 183,794,400; + 24,688,800 | CONFORMS |
| **≈ 7.21B at 67** (7,212,787,200), **≈ 4.67B at 9** (4,667,097,600), 16 cells (L20–L21) | 4,272,076,800 + 43,891,200 × 67 = 7,212,787,200; × 9 → 4,667,097,600 | **CONFORMS WITH EDITS**. Arithmetic is exact; the 16-cell count is an upper reading for calibration (§4: calibration set 13–16 cells; dose 0 is confirmation-side only) |
| §1 partition table: 2,286 / 1,143; 153,162 / 76,581; 30,632,400 / 15,316,200; 133,502,400 / 66,751,200; totals 4,572 / 306,324 / 61,264,800 / 267,004,800 (L37–L42) | all reproduced | CONFORMS |
| "**Calibration** … 59% of trials at 67 and 92% at 9" (L110) | 267,004,800 / 450,799,200 = 0.5923; / 291,693,600 = 0.9154 | **CONFORMS WITH EDITS**. These shares count only the GRID sweep. LC itself files step 3a as calibration (L46; M L2161). The calibration-ledger share including 3a is 389,534,400 / 450,799,200 = **0.8641 (86%) at 67** and 283,464,000 / 291,693,600 = **0.9718 (97%) at 9**. Relabel 59% / 92% as "GRID-sweep share" or replace them |
| "0.647× the trial line" at 9 vs 67 (L110) | 4,667,097,600 / 7,212,787,200 = 11/17 = 0.64706 | CONFORMS |
| 18-cell sensitivity, every total × 18/16 = 8,114,385,600 (L65) | arithmetic correct | **DOES NOT CONFORM** as a reading. Dose 0 is "a dose-0 sanity level that is REPORTED only. … Only required doses enter the label." (CNA2 L242 = S2.1 L339). The calibration loop runs over "required dose k" (M L1951), and 3a is per required (g, k). So dose 0 never enters calibration or 3a; at most it adds confirmation-side 914,400·n per dose-0 cell (§4.3) |
| "only P, N and confound rows … 6/16" (L65) | 6 cells | **DOES NOT CONFORM** with M L2785, which lists "positives, negatives, specificity and confound rows". The lower bound is 13 (§4.2) |
| **8.2M** early-stop minimum, 200 × 4,572 × 9 = 8,229,600 (L129) | 8,229,600 | Arithmetic CONFORMS. **As a design figure DOES NOT CONFORM**: M L2784 forbids early stop (§3) |
| **37%**: 122,529,600 / 328,269,600 (L126) | 328,269,600 = 267,004,800 + 61,264,800; ratio 0.37326 | CONFORMS |
| Conditional dose calibration 50 × 306,324 = 15,316,200 (L78) | 15,316,200 | CONFORMS (arithmetic; the replicate size is ABSENT, as LC says) |
| Seed-units 98,600 per cell at 67 (13,400 + 58,400 + 26,800) (L74); U = 1,577,600 (L106) | 200·67 + 200·292 + 2·200·67 = 98,600; × 16 | CONFORMS |
| 2,400 replicate-evaluations per cell (L77) | 200 + 9 × 200 + 400 | CONFORMS |
| Bootstrap ≈ 2.6 × 10¹⁰ ops at 67 (L98) | LC's form 2,400 × 10⁴ × 67 × 16 = 2.5728 × 10¹⁰ applies n = 67 to calibration evaluations as well. Using each evaluation's own n: 10⁴ × 98,600 × 16 = **1.5776 × 10¹⁰** | CONFORMS WITH EDITS (an over-count in the conservative direction; UNVERIFIED either way) |
| Dip tests 98,600 × 4 = 394,400 (L76) | 394,400 | CONFORMS |
| Steps per trial 160 (Δt = τ/20) and 800 (τ/100) over 8τ (L86) | 8 × 20, 8 × 100 | CONFORMS given 8τ. Whether plants settle is item 4 (§6) |
| Compiled "about 0.1 µs/step" from "about 200–300 scalar op-equivalents per step" at "about 10⁹ simple ops/s" (L87–L89) | 200–300 / 10⁹ = **0.2–0.3 µs/step** | **CONFORMS WITH EDITS**. The stated inputs give 32–48 µs (160 steps) to 160–240 µs (800 steps), not 16–80 µs |
| Interpreted "about 5–20 µs/step" from 10⁷–10⁸ ops/s (L88–L89) | 200–300 ops at 10⁷–10⁸ ops/s = **2–30 µs/step** | CONFORMS WITH EDITS. LC's range is narrower than its own inputs give; at the high end 800 × 30 µs = 24 ms per trial |
| Fit flops "about 4 × 10⁷ to 2 × 10⁸", t_fit 0.02–0.2 s (L93) | (1–2 × 10⁵) × 3 × (100–500) = **3 × 10⁷ to 3 × 10⁸**, so 0.03–0.3 s at 10⁹ flop/s | CONFORMS WITH EDITS |
| F = 4 (2 × 1 × 2 × 1) and 60 (2 × 5 × 2 × 3) (L93) | 4; 60 | CONFORMS (the t_r grid and restarts are ABSENT) |
| Network trial 25 × 2 × 256² = 3.3 × 10⁶ flop, ≈ 3 ms; 7/16 cells (L91) | 3,276,800; 3.28 ms at 10⁻⁹ s/flop; RAND-INIT 3 + Arch 2 + BOTTLENECK 2 = 7 | CONFORMS (d_h is ABSENT, P4) |
| CPU table: trials 32 / 160 / 1,603 / 32,057 CPU-h; fits 35 / 5,259 CPU-h; totals ≈ 70 / ≈ 37,300 (L104–L108) | 7,212,787,200 × {16 µs, 80 µs, 0.8 ms, 16 ms} = 32.06 / 160.28 / 1,602.84 / 32,056.83 h; 1,577,600 × 4 × 0.02 s = 35.06 h; × 60 × 0.2 s = 5,258.67 h | Arithmetic **CONFORMS** to LC's per-unit values. The range stays **UNVERIFIED**. If the per-unit values are re-derived from LC's own stated op counts (rows above), the same arithmetic gives trials 64.11 h (32 µs) to 48,085.25 h (24 ms) and fits 52.59 h (0.03 s) to 7,888 h (0.3 s): **≈ 117 to ≈ 55,974 CPU-h**. That is arithmetic only, not an estimate RD endorses; R25 / #43 L134 require the S0 preflight |
| §2 citations "CNA2 L283", "CNA2 L284", "CNA2 L309" | RAND-INIT is CNA2 **L289**, Architecture-imposed **L290**, LIM **L308** (matching S2.1 L243 / CNA2 erratum 1 L77) | CONFORMS WITH EDITS |
| Other approximate cites: "M ~L1950", "M ~L1957", "M ~L2172" | L1951, L1958, L2170 | CONFORMS WITH EDITS |
| LC §6 item 4: the loop "does not say whether larger n must still be run" (L129) | M L2784 says it | **DOES NOT CONFORM**; settled (§3) |

## 3. Item 1 (CNA owns it): settled

M L2784, verbatim: "**2 (last line) [v3.4 E44-3].** `pass(g,k,n) = TRUE iff every target below is met at n`. Record pass(g,k,n) for **every** n in GRID; do not stop at the first passing n." Its source is A44 L108, verbatim: "Fresh confirmation then evaluates that selected common n. Retain the full grid results; do not impose monotonicity by replacing failed results." The selection rule (A44 L104–L106): "Select the smallest n in GRID at which every required row and dose / passes the complete calibration requirements. / If there is no such n, confirmation is BLOCKED."

**Settled as written: the full GRID runs, at 267,004,800 trials per cell.** Early stop would change frozen text and needs a Lead ruling plus Astra review under A-2026-10-24, before any calibration output (A49 L47). It is not a cost lever (CE49 L135–L136). A diagnostic extra grid point is needed only if early stop is adopted.

RD's check of the loop text, for CNA's record. RD found no smoothing, no cross-grid monotonicity fit and no pooled cross-n statistic in M L1949–L1967 or L2784–L2785; each pass(g, k, n) is computed from point n's own replicates. One dependence exists: R37 (M L2407) keys the spawn tree by "(role, generator, dose, replicate, purpose …)" with **no grid value**. Replicate r at different n therefore reuses the same streams, an implicit nested-seed design. That shares draws but creates no computational dependence. CE49 L129–L131 identified this and adds an `n_grid` field (CE49 L166). That field also closes a gap in V2.5-RD §6, whose field list lacked a grid-value field (and the replicate set, which CE49 also adds). The selected n_seed is a minimum by construction (M L2785). It stays the minimum common passing point only if every R_core (g, k) is evaluated at each n until that point (CE49 L127).

## 4. Item 2: generator × dose cells

### 4.1 Every IGN generator row and its dose grid

| Row | Role (S2.1) | Dose parameter and required doses | Source | Cells |
|---|---|---|---|---|
| IGN-P1 | P (S2.1 L248) | g > 1 (S2.1 L239, MP L84). Positive at "nominal dose" (S2.1 L244), with the nominal positive dose "1.5× margin" (M L615, D26). **No numeric g or IGN dose grid** | S2.1 L239–L244, L248; M L615 | 1 (ASSUMED) |
| IGN-N1 | N (S2.1 L249) | "g < 1" (S2.1 L249, MP L85). **No numeric grid** | S2.1 L249; MP L85 | 1 (ASSUMED) |
| IGN-NC1 | Confound, specificity (S2.1 L250) | Δs ∈ {2, 4} grid steps | CNA2 L296 = S2.1 L393 | 2 |
| IGN-NC2 | Confound, specificity (S2.1 L251) | clip quantile {0.8, 0.6} | CNA2 L297 = S2.1 L394 | 2 |
| IGN-NC2r | Mechanism-present (S2.1 L252) | **No dose parameter or grid** in CNA2 §2.6 or S2.1 | S2.1 L252 | 1 (ASSUMED) |
| BOTTLENECK-ONLY | Mechanism-present for C-IGN; specificity for joint IGN∧BCAST (S2.1 L253) | g_b, "2 levels giving D ≥ 2" (no values) | CNA2 L298 = S2.1 L395 | 2 |
| RAND-INIT (IGN part) | Mechanism-present for C-IGN; specificity for C-LEARN-on-IGN (S2.1 L254) | g_0 ∈ {0.9, 1.0, 1.1}× the declared default | CNA2 L289 = S2.1 L386 | 3 |
| Architecture-imposed | C-LEARN (CNA2 L290: "**RD/AQ-2**"); covered by S2.1 L254 "by-construction" | β "at 2 levels" (no values) | CNA2 L290 = S2.1 L387 | 2 |
| IGN-LIM | Designated limitation (S2.1 L255) | s* offset in grid steps, "2 levels each" | CNA2 L308 = S2.1 L406 | 2 |
| **Total required cells** | | | | **16** (LC agrees) |

Merged v3.6 carries these rows by reference (M L2349, M L3187). The v2, v2.2 and v2.3 freeze-prep files and CNA's E48 response name no IGN generator or dose grid; they cost "per IGN generator and dose" (V2.3 L129–L133; CE F-8, CE L72). No later CNA file changes an IGN dose (CNA2 errata 1 and 2 checked).

### 4.2 Which cells enter sample-size calibration (bound, 13–16)

M L2785 requires "every required calibration row (positives, negatives, specificity and confound rows …) and every required dose". That covers P1 (1), N1 (1), NC1 (2), NC2 (2), and the three rows that are specificity rows for some reading: BOTTLENECK-ONLY (2), RAND-INIT (3) and Architecture-imposed (2), for **13 cells**. Two rows are not clearly calibration rows: NC2r is mechanism-present only, and IGN-LIM is a designated limitation scored as correct UNAVAILABLE (CNA2 L257). Including both gives **16 cells**. M L3174 (R_core = "every calibration row and dose required for any family-member label at its licensed level") does not settle it. **PENDING: Lead ruling** (sample-size calibration is RD's role, M L374, with CNA, who owns row roles).

### 4.3 "Plus dose 0": resolved as confirmation-side only and bounded

CNA2 L328 ("about 2–3 required doses each plus dose 0, each at R prespecified replicates") is resolved by CNA2 L242 (S2.1 L339): dose 0 is "REPORTED only. … Only required doses enter the label". It is therefore **not** a calibration or 3a cell (M L1951, "required dose k"). If it is run at R = 200 in confirmation, each dose-0 cell adds 914,400·n_seed\* trials. CNA2 L242 attaches dose 0 to "each specificity row", which here means NC1 and NC2 (2) and at most also BOTTLENECK-ONLY, RAND-INIT and Architecture-imposed (5). The bound is therefore **d0 ∈ {0, …, 5}**, not LC's 18/16 scaling of every line: at 67 that adds 0 to 306,324,000 trials (16-cell upper total 7,519,111,200), and at 9 it adds 0 to 41,148,000 (4,708,245,600). **PENDING CNA** (author of L242): whether dose 0 runs the full IGN procedure at R = 200, and on which rows.

### 4.4 Proposed cost formula (RD PROPOSED; replaces V2.3 §5 "G × Dose × …")

> T_total = Σ_{c ∈ C_cal} [ 200 · 4,572 · ΣGRID + 2 · 200 · 4,572 · n_seed\* ] + Σ_{c ∈ C_conf} 200 · 4,572 · n_seed\*
> = 267,004,800·|C_cal| + 1,828,800·n_seed\*·|C_cal| + 914,400·n_seed\*·|C_conf|, and
> CPU = Σ_c T_c · c_trial(type(c)) + fits + aggregation, with c_trial differing for scalar-plant and network cells.

A cell c is a (generator row, required dose) pair, with 1–3 doses per row (§4.1). C_cal is 13–16 cells (§4.2); C_conf is C_cal plus any confirmation-only rows (NC2r and LIM if they are not in C_cal) plus d0 dose-0 cells (§4.3). This replaces the uniform "G × Dose" product, which assumes the same dose count for every generator. Bounds (exact): **5,860,389,600 (13 cells) to 7,519,111,200 (16 cells + 5 dose-0) at n_seed\* = 67; 3,792,016,800 to 4,708,245,600 at 9.**

**Unresolved grids and owners.** CNA owns the plants and doses (V2.2 L7): IGN-P1's g and nominal dose, IGN-N1's g, the IGN-NC2r dose parameter, the BOTTLENECK g_b values, and the IGN-LIM s* offsets are PENDING CNA. The Architecture-imposed β values are PENDING **RD with CNA** (CNA2 L290: "RD/AQ-2"). Calibration membership of NC2r and LIM is PENDING the **Lead** (§4.2). The dose-0 run policy is PENDING **CNA** (§4.3). M L377 requires every dose grid to be frozen "before calibration starts".

## 5. Item 3: R25 workload line (M L2390)

Verbatim (M L2390, R25, excerpt): "Workload, arithmetic on proposed values: confirmation 200 × Σ(generator × dose); sample-size calibration 200 × Σ(generator × dose); dose calibration ≤ 50 × (plants with fitted references or κ_f). At about 25 confound systems × 3 doses (merge R29, v2.1) that is about 15,000 + 15,000 + ≤ 3,750 replicate evaluations, plus 2 × 3 × 200 = 1,200 per role for MIXED-CODE-E/I and the DISSOC draws of R14."

**Conflict.** The calibration loop (M L1951–L1953) runs "for n in GRID" and "for r in 1..R_cal,n (= 200)" inside each (g, k), and M L2784 requires every n. Sample-size calibration is therefore 200 × |GRID| = 200 × 9 = **1,800** replicate evaluations per cell (200 × ΣGRID = 58,400 seed-units), not 200, plus step 3a at 2 × 200 = 400 per cell (M L1967). R25 omits both, which understates calibration ×9 in replicate evaluations and ×(292/n_seed\*) in seed-units. R25 carries the tag "[v3.3 E43-8: superseded or amended by §PZ5 §8.2]" (M L2390), and PZ5 §8.2 (M L2161) states "R_cal,n = 200 over GRID; 3a envelope points" correctly, so the stale line is in a superseded row. CE49 L246 makes the same point.

**Proposed replacement wording (a new-file proposal for the next merge's stale-text list; M is not edited):**
> "Workload, arithmetic on proposed values, per required generator × dose cell c: confirmation 200 replicate evaluations at n_seed\*; sample-size calibration 200 × |GRID| = 1,800 replicate evaluations (200 × ΣGRID = 58,400 seed-units; every n in GRID is run, PZ6 §3.2), plus PZ5 §4.2 step 3a 2 × 200 = 400 replicate evaluations at n_seed\*; dose calibration ≤ 50 × (plants with fitted references or κ_f). At R25's illustrative 25 × 3 = 75 cells: 15,000 + 135,000 + 30,000 + ≤ 3,750 replicate evaluations. Superseded for budgeting by PZ5 §8.2 (L-CAL / L-CONF)."

(75 × 200 = 15,000; 75 × 1,800 = 135,000; 75 × 400 = 30,000; 50 × 75 = 3,750. These are R25's own illustrative values; no number is new.)

## 6. Item 4: IGN-P1 analytic reset vs §8.1 plant settling

**Text A, analytic reset.** S2.1 L240: "(i) Each trial starts from a **reset to the low attractor x_lo**, a controlled initial condition (L36)." S2.1 L242: "In IGN-P1, x_ref = x_lo, so plant and instrument share one definition." M L314 (merge R1): "x_ref is the declared controlled initial state (x_lo in IGN-P1; end-of-settling state under null input in the network instrument …)".
**Text B, plant settling.** M L1127 (CNA v3 §8.1): "| IGN settling (E3 (ii-a); #42 L221) | Settling length | t_s = 5τ in plants (residual e^−5 < 1%); 20 steps in networks |". M L1128: "| | Readout delay | t_r = 3τ in plants; 5 steps in networks |". M L1129: settling tolerance "2 × the median absolute deviation of ‖x_ref − median x_ref‖ in null-input runs on the fitting partition". M L2349 maps "IGN settling parameters → CNA v3 §8.1". Astra (A42 L221): "IGN settling exclusions need coverage checks at every required strength and transition bin. Aggregate eligibility can hide exclusion of the informative region. The claim is about the declared settled-state response protocol."

**Where 8/3 comes from.** Under Text B, a plant trial runs t_s + t_r = 5τ + 3τ = 8τ. Under Text A, it runs t_r = 3τ. The ratio is 8τ / 3τ = **8/3**, holding only at a single t_r = 3τ. M L376–L377 make t_r a selection-partition choice from "the IGN t_r grid", which is ABSENT. LC simulates to t_s + max(t_r grid), so the general factor is (5τ + t_r,max) / t_r,max. Steps per trial = (t_s + t_r,max) / Δt, and **Δt is ABSENT** everywhere checked (M, S2.1, CNA2, MP). LC also assumes every t_r candidate is read from one trajectory per trial; that assumption is PENDING CNA.

**Analysis.** The two texts conflict on x_ref. Text B's rationale ("residual e^−5 < 1%") presumes a transient to decay, which an exact reset to x_lo does not have. Under Text A, though, every trial has x_ref = x_lo exactly, so the M L1129 settling tolerance is degenerate: the MAD is 0 and no trial can fail it. Stage 0 would then not exercise the settling-exclusion path that A42 L221 asks to be coverage-checked. Calibration must run "the COMPLETE confirmation procedure unchanged … support/eligibility checks (counted, never dropped)" (M L1956–L1957; A43 L183: "The sample-size procedure calibrates the actual complete decision rule.").

**RD PROPOSED:** §8.1 (Text B) governs for IGN-P1 and the other scalar plants. Each trial resets to x_lo, then settles for t_s = 5τ under null input with process noise ξ, and x_ref = the end-of-settling state. M L314's parenthesis "(x_lo in IGN-P1; …)" then becomes "(end-of-settling state after reset to x_lo in IGN-P1; …)". Cost: the 8/3 factor at t_r = 3τ applies. **Decision needed:** which text governs IGN-P1 trial initialization. **Owner: CNA** (plants and IGN protocol are CNA-owned, V2.2 L7), with the **Lead** ruling in consolidation. Also PENDING CNA, to be frozen before calibration (M L377): Δt and the t_r grid.

## 7. New conflicts and cross-references (for the Lead)

1. **Dose 0 in LC's 18-cell sensitivity** scales calibration and 3a, but dose 0 is REPORTED only (CNA2 L242). It is confirmation-side at most (§4.3).
2. **LC's 6/16 lower bound** conflicts with M L2785's explicit inclusion of specificity rows (§4.2).
3. **LC's per-step and per-fit times** are 2–3× below what LC's own stated op counts imply (§2). This is UNVERIFIED either way.
4. **LC's calibration share (59% / 92%)** excludes the 3a lines that LC files as calibration (§2).
5. **R37 (M L2407) has no grid-value field**, which gives an implicit nested-seed design across GRID. CE49 L166's `n_grid` field resolves it, and V2.5-RD §6's field list should be read with CE49 §4.2 (§3).
6. **Text A vs Text B on x_ref for IGN-P1** (M L314 vs M L1127–L1129), and the degenerate settling tolerance under Text A (§6).
7. **Cross-reference, V2.5-RD 3b(iii) PENDING.** CE49 L108–L112 answers it with the three bin-wide gates of MP L78–L81 (s* outside the grid; fewer than n_trial trials per near-transition bin; Var(w) below a floor). CE49 L112 calls the Var(w) floor Astra's "bin-wide variance test" (A49 L73). RD concurs that these are aggregate outcomes under V2.5-RD (3b)(iii).
8. **Cross-reference, R25.** CE49 L246 independently flags M L2390's missing ×|GRID| factor, consistent with §5.

*DESIGN/TEXT ONLY. Draft, not frozen. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No host coupling. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 3032e59fc6ab68582d5b86e4734bfe0790c52165684bda5b2ce870c7ece3073c
