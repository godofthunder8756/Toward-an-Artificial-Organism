# Track B freeze preparation v2.6: Lead response to Astra #50 E50-5 — complete IGN workload ledger, maximum-cost accounting, early-stop status

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** A new, additive file; it edits no existing file. Nothing was run, timed or benchmarked. The only computation was exact integer/rational arithmetic on design operation counts (system `python3`; scripts `scratch/lead_v26/ledger.py`, `ledger2.py`, `gen.py`) and SHA-256. **Every CPU-hour figure is arithmetic on stated, UNVERIFIED per-unit costs; none is a measurement, a feasibility interval or a reliable upper bound** (A50 L212). Binding caps need u measured in an authorized S0 preflight (R25, M L2390; P5), which needs its own protocol, Astra's review and Aidan's explicit yes; none is planned.
- **Written:** 2026-11-01, about 12:10–12:25 PM ET, by the Lead's executor. "A50 Ln" = line n of Astra's raw #50 reply; "RD26" = the Delegate's E50-2/E50-4 file, "RD26c1" its correction 1; other shorthands as V25. All inputs with full hashes in §6.
- **Edit addressed (A50 L248, verbatim):** "E50-5. Complete the workload ledger, including omitted calibration and inference work. If early stopping is adopted, supersede the full-grid requirement explicitly, retain maximum-cost accounting, and report later points as NOT RUN BY DESIGN."
- **Lead rulings applied here (room, about 12:14 PM ET):** (a) **IGN-LIM is IN calibration**: |C_cal| = 15 (RD26 §1.3 option (B) IN; V25 L174's own condition). The Delegate's totals **4,005,072,000 + 45,720,000·n_seed*** are adopted (RD26 §1.4) and were rechecked here exactly. (b) The network **null-centre runs (n_c)** and **null-quantile runs (n_q)** are counted as **separate, non-reused samples** (RD26 §2.1–§2.3 roles `ign-null-centre`, `ign-null-quantile`); both counts are symbolic and **PENDING CNA**. (c) Quantile index **k = ⌈0.99·(n_q + 1)⌉** (see §4 item 9).
- **Scope:** the IGN instrument workload (the object of V25 §8 and #50 Q6). Other Track B instruments' ledgers are outside this file (O-W14).
- **Safety (unchanged):** X1–X5; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); claim ceiling (#41 L304); no consciousness claim is made or implied.

## 0. Headline
- **Scheduled trials (exact; full GRID; |C_cal| = 15, |C_conf| = 20):** 15 × 267,004,800 + (15 × 1,828,800 + 20 × 914,400)·n = **4,005,072,000 + 45,720,000·n_seed*** → **7,068,312,000 (≈ 7.07 × 10⁹) at n_seed* = 67** and **4,416,552,000 (≈ 4.42 × 10⁹) at 9**. Matches RD26 §1.4 exactly. Supersedes V25 §8.2's 13-cell 6,289,243,200 / 3,849,624,000 (the +2 LIM cells add 2 × 389,534,400 = 779,068,800 at 67).
- **Newly ledgered (op counts, n = 67):** null-centre runs **72,417,000–717,717,000** (n_c = 101–1,001) and null-quantile runs **717,000,000** (n_q = 1,000), 20 steps each; dose calibration 0 to **1,148,715,000** trials; hysteresis 0 to **27,828,000** trial-equivalents; fits **18,552,000–70,819,200**; dip tests **6,184,000**; bootstrap 3.09e+10–1.86e+12 ops; KATs and fixtures negligible.
- **CPU-h, complete ledger (UNVERIFIED):** **≈ 505 to ≈ 103,501 at n_seed* = 67** (≈ 4,177 at V25's illustrative network point d_h = 256, κ_net = 1, low settings otherwise); **≈ 316 to ≈ 69,069 at 9**. **Maximum-cost envelope ≈ 139,086 CPU-h** (§2). V25's ≈ 221–20,015 (n = 67) is superseded: it had 13 calibration cells, omitted the B/C lines below, and priced networks at 2·d_h² flop/step only.
- **Early stopping: NOT ADOPTED. The full grid governs (R1).** §3.

## 1. Complete workload ledger (E50-5)
Notation: n = n_seed*; G = ⌈max(1, g − 1)⌉ (E2-6; plant steps per trial = 500·G); d_h = network width (P4, ABSENT); κ_net ≥ 1 = network overhead factor for modules, gates, heads, random generation and memory traffic beyond 2·d_h² flop/step (A50 L210); seed-units U = 15·(58,400 + 400n) + 20·200n (1,546,000 at 67, 966,000 at 9); network seed-units U_net = 7·(58,400 + 400n) + 9·200n (717,000 at 67, 450,200 at 9; LIM is scalar, so U_net is unchanged by ruling (a)).

### 1.0 Cell-ID list (A50 L111; IDs and membership as RD26 §1.4, with Lead ruling (a))
| Cells (RD26 IDs) | Type | C_cal | C_conf |
|---|---|---|---|
| IGN-P1/0, IGN-N1/0, IGN-NC1/0, IGN-NC1/1, IGN-NC2/0, IGN-NC2/1 | scalar | IN (6) | IN (6) |
| **IGN-LIM/0, IGN-LIM/1** | scalar | **IN (2), Lead ruling (a)** | IN (2) |
| BOTT/0, BOTT/1, RINIT/0, RINIT/1, RINIT/2, ARCH/0, ARCH/1 | network | IN (7) | IN (7) |
| IGN-NC2r/0 (validation role withdrawn, RD26 SC-2; A50 L109) | scalar | — | IN (1) |
| IGN-NC1/D0, IGN-NC2/D0 (DOSE0) | scalar | — | IN (2) |
| BOTT/D0, ARCH/D0 (DOSE0; RAND-INIT dose 0 dropped, RD26 SC-1) | network | — | IN (2) |
| **Totals** | | **15 (8 scalar, 7 network)** | **20 (11 scalar, 9 network)** |

### 1.1 Ledger lines
| Line | Component | Operation count (exact formula) | At n = 67 | Inputs |
|---|---|---|---|---|
| A1 | GRID sweep, calibration | 200·4,572·292 = 267,004,800 per C_cal cell × 15 | 4,005,072,000 trials | exact |
| A2 | Step 3a envelope points (M L1967) | 1,828,800·n × 15 = 27,432,000·n | 1,837,944,000 trials | exact |
| A3 | Confirmation incl. DOSE0, NC2r | 914,400·n × 20 = 18,288,000·n | 1,225,296,000 trials | exact |
| A-cost | per trial | scalar 500·G steps × c_step; network 28 steps × 2·d_h²·κ_net flop × c_flop. One trajectory serves all t_r candidates and both readouts (A50 L214) | scalar 3,790,188,000, network 3,278,124,000 | G, d_h, κ_net PENDING |
| B1 | **Dose calibration** (M L373, R_cal,dose = 50) | 50 × 4,572 × n_dc × K_dc per cell needing a fitted reference or κ_f (≤ 8 scalar, ≤ 7 network required-dose cells) | 0 (all references analytic) to 1,148,715,000 trials (n_dc = 67, K_dc = 5, 15 cells) | which cells need fitting, n_dc (seeds per dose-calibration replicate; it runs **before** sample-size calibration, so n_seed* cannot set it), K_dc (candidate doses per cell): ABSENT |
| B2a | **Network null-centre runs** (RD26 §2.1; A50 L122, L134) | U_net × n_c runs of 20 null-input settling steps; separate, never reused | n_c = 101: 72,417,000; n_c = 1,001: 717,717,000 runs | **n_c symbolic, PENDING CNA** (odd recommended, RD26) |
| B2b | **Network null-quantile runs** (RD26 §2.2; A50 L124) | U_net × n_q runs of 20 steps; separate from B2a and from all trials, never reused | n_q = 1,000: 717,000,000 runs | **n_q symbolic, PENDING CNA**; threshold = k-th order statistic, k = ⌈0.99·(n_q + 1)⌉ (= 991 at n_q = 1,000) |
| B3 | **Hysteresis sweeps** (MP L72, REPORTED secondary) | h sweeps per seed-unit × 2 directions × 9 bins ≤ 18·h trial-equivalents per seed-unit | 0 (unscheduled) to 27,828,000 (h = 1) | schedule, h, hold length ABSENT |
| B4 | **LIM validation path** (RD26 §1.3; A50 L92–L97) | (A) deterministic gate fixture: 2 LIM doses × N_fix predicate evaluations (negligible); (B) end-to-end: the 2 LIM cells, now inside A1–A3 | in A1–A3 | N_fix, s* offsets PENDING CNA |
| B5 | Noise reference (E50-3); IGN-N1 bracketed root solve with iteration cap and failure status (A50 L153) | one solve per (plant, dose); < 10⁶ ops in total | negligible | E50-3 |
| C1 | **Model fits incl. mixture fitting** (H0 logistic/skew-normal; H1 two-component mixture; one per t_r candidate on selection data) | (U + U_NC1·(φ_c − 1)) × F; F = 2 models × 3 t_r × 2 readouts × restarts 1–3 = 12–36; φ_c = NC1 per-c-level factor 1–3; U_NC1 = 2·(58,400 + 400n) + 3·200n | 18,552,000–70,819,200 fits | restarts, φ_c ABSENT; t_fit 0.03–0.3 s UNVERIFIED |
| C2 | Selection scoring, held-out ΔLL, Ashman D | likelihood evaluations on 1,143 selection / 1,143 final trials per seed-unit per candidate | inside C1 | — |
| C3 | **Dip tests and dip-test calibration** | 4 per seed-unit (2 near-transition bins × 2 readouts). p-values from a frozen table (a one-off N_null dips per sample size; negligible) or simulated per test (4U × N_null) | 6,184,000 tests; per-test simulation would add 6.18e+10 null dips at N_null = 10⁴ | method ABSENT |
| C4 | **Seed-level bootstrap, B = 10,000** (M L1958, D15) | 10⁴ × U × S_b × c_b ops; resamples **seed statistics only, no refit** (frozen assumption: a refit bootstrap would multiply C1 by 10⁴ and is excluded) | 3.09e+10–1.86e+12 ops (S_b 1–12 statistics, c_b 2–10 ops) | S_b ABSENT |
| C5 | Aggregation, CP bounds, labels, OC tables | closed form per replicate-evaluation | negligible | — |
| D1 | **KATs** | integer Philox4x64 (6 vectors, KV L38–L43); address/key rows R1–R10; permutation KAT (507 draws); **DOSE0 address KAT** (E2-8; A50 L175); partition-key sentinel KAT (A50 L181); KATs for the new roles `ign-null-centre` / `ign-null-quantile` (RD26 §2.3); floating-transform checks (CE49 R1, R2, R7, R9) | < 10⁷ ops in total | run at freeze; tolerance P6 |
| D2 | **Replays** (determinism / audit re-execution) | fraction ρ_rep of any line above, re-run bit-exactly | 0 (no replay is required by the governing text) | ABSENT; if frozen, adds ρ_rep × that line |
| D3 | S0 preflight (u measurement, R25) and code audits with planted violations (M §5.8 stage S0) | ABSENT | not counted | own protocol, Astra's review and Aidan's explicit yes |

### 1.2 Per-unit costs (UNVERIFIED; op counts only)
- **Scalar plant step:** 1 Philox4x64-10 block + 1 log + 1 sqrt + 1 cos (Box–Muller) + 1 tanh + about 6 flops. These operations do not have interchangeable costs (A50 L212). c_step is carried as **0.2 µs (compiled) to 30 µs (interpreted)** (V25 §8.2): an envelope, not a bound.
- **Network step:** 2·d_h²·κ_net flop at c_flop = 10⁻⁹ s (V25's illustrative value). Envelope d_h ∈ [64, 512], κ_net ∈ [1, 4], illustrative only; if the frozen architecture falls outside, the formula governs. Null runs cost 20/28 of a network trial.
- **Fit:** t_fit 0.03–0.3 s (LCL L59). **Dip:** about 10⁴ ops. **Bootstrap/dip throughput:** 10⁷ (interpreted) to 10⁹ (compiled) ops/s.
- **Scenarios.**
  - **Low:** d_h 64, κ_net 1, G 1, F 12 at 0.03 s, φ_c 1, c_step 0.2 µs, n_c 101, n_q 1,000, no dose calibration, no hysteresis, tabulated dips, S_b·c_b = 2 at 10⁹.
  - **V25 point:** as Low, but d_h 256.
  - **High:** d_h 512, κ_net 4, G 1, F 36 at 0.3 s, φ_c 3, c_step 30 µs, n_c 1,001, n_q 1,000, dose calibration on all 15 required-dose cells (n_dc 67, K_dc 5), h = 1, tabulated dips, S_b·c_b = 120 at 10⁷.
  - **Max:** as High, plus G = 2 (any frozen g in (2, 3]) and per-test simulated dips (N_null = 10⁴).

### 1.3 CPU-hours by line (UNVERIFIED)
| Line | Low, n=67 | V25 point, n=67 | High, n=67 | **Max** (§2) | Low, n=9 | High, n=9 |
|---|---|---|---|---|---|---|
| A trials: scalar | 105.3 | 105.3 | 15,792.5 | 31,584.9 | 65.5 | 9,826.0 |
| A trials: network | 208.9 | 3,341.9 | 53,470.1 | 53,470.1 | 131.1 | 33,573.5 |
| B1 dose calibration | < 0.1 | < 0.1 | 11,296.6 | 13,849.3 | < 0.1 | 11,296.6 |
| B2a null-centre runs (n_c) | 3.3 | 52.7 | 8,362.0 | 8,362.0 | 2.1 | 5,250.5 |
| B2b null-quantile runs (n_q) | 32.6 | 522.1 | 8,353.7 | 8,353.7 | 20.5 | 5,245.2 |
| B3 hysteresis sweeps | < 0.1 | < 0.1 | 272.7 | 334.9 | < 0.1 | 170.9 |
| C1 fits incl. mixture fitting | 154.6 | 154.6 | 5,901.6 | 5,901.6 | 96.6 | 3,674.4 |
| C3 dip p-values | < 0.1 | < 0.1 | < 0.1 | 17,177.8 | < 0.1 | < 0.1 |
| C4 seed-level bootstrap | < 0.1 | < 0.1 | 51.5 | 51.5 | < 0.1 | 32.2 |
| D1-D2 KATs, fixtures, root solves | < 0.1 | < 0.1 | < 0.1 | < 0.1 | < 0.1 | < 0.1 |
| **Total (UNVERIFIED)** | **≈ 505** | **≈ 4,177** | **≈ 103,501** | **≈ 139,086** | **≈ 316** | **≈ 69,069** |

The network lines (A, B2a, B2b) dominate at large d_h·κ_net. Dose calibration and the null runs are the largest previously uncounted lines. Bootstrap and KATs are negligible on every setting in the envelope.

## 2. Maximum-cost accounting
**Rule (Lead, PROPOSED for the freeze text):** budgets and per-ledger caps (P5) are set against the **scheduled maximum**, never an expected figure. Cap-limited work is "INCOMPLETE, never passed" (M L368).
- **Schedule maxima (exact):**
  - n_seed* = 67 (GRID maximum).
  - Full GRID, Σ = 292, always (R1).
  - |C_cal| = 15 (ruling (a)) and |C_conf| = 20.
  - DOSE0: 4 cells. The RAND-INIT drop was accepted by Astra as a named scope change (A50 L107).
- **Maximum scheduled trials:** **7,068,312,000** (scalar 3,790,188,000, network 3,278,124,000).
- **Conditional addition:** if the NC2r withdrawal (RD26 SC-2) were not adopted and NC2r entered calibration, |C_cal| = 16 would add 389,534,400 trials, giving 7,457,846,400. This is not counted in the maximum.
- **Plus, at the envelope tops:**
  - dose calibration: 1,148,715,000 trials;
  - null-centre runs: 717,717,000; null-quantile runs: 717,000,000;
  - hysteresis: 27,828,000 trial-equivalents;
  - fits: 70,819,200;
  - dips: 6,184,000 (+ 6.18e+10 null dips if simulated per test).
- **Max CPU-h envelope ≈ 139,086 (UNVERIFIED).** It scales linearly in G for the scalar lines, in d_h²·κ_net for the network lines, and linearly in n_c and n_q for B2. It is not a bound, because those parameters are ABSENT.
- **Conditional addition outside the envelope (5-fold CV):** MP L69 specifies ΔLL "from 5-fold cross-validation over trials within a seed", while V25 and LC read ΔLL as held-out on the frozen final partition, with no CV. If 5-fold CV were also retained, fits would rise up to ×6 (5 folds plus the full fit): line C1 at Max would be ≈ 35,410 CPU-h instead of ≈ 5,902 (O-W6).
- **Redesign:** a FAIL or UNRESOLVED leads to revise, re-freeze and a new review (M §5.8). A later run is ledgered as a new run, never folded into this one.

## 3. Early stopping
- **Status: NOT ADOPTED.** Per Lead ruling R1 (V25 §4.1, D56), the **full GRID governs**: "Record pass(g,k,n) for **every** n in GRID; do not stop at the first passing n." (M L2784; A44 L108). Every n in GRID is run for every required (g, k), so the full-grid cost is the expenditure: "Under the currently retained full-grid rule, the cost remains the full-grid cost. Under an adopted early-stop rule, that cost becomes the scheduled maximum, not the guaranteed expenditure." (A50 L84). §1–§2 cost the full grid.
- **Astra's position, recorded (A50 L64–L84):** the three equivalence conditions preserve the selected n*. "Retain the full grid results" meant computed results at every point: "My earlier "retain the full grid results" did mean computed results at every point. A formally adopted prospective amendment can replace that requirement. The resulting report must mark later points NOT RUN BY DESIGN, and must relinquish claims about performance across those unexecuted points." (A50 L70).
- **Conditions under which a LATER amendment could adopt early stopping (stated here; NOT adopted now):**
  1. **Explicit supersession.** A prospective amendment under A-2026-10-24 must name and supersede the full-grid rule (M L2784's "every n" clause, V25 §4.1, D56). It must be adopted before any calibration, pilot, feasibility or diagnostic output exists (A49 L47, L87), with Astra's review.
  2. **Maximum-cost accounting retained.** Budgets and caps stay at the full-grid (Σ = 292) maximum of §2. Early stopping gives a scheduled maximum, not a guaranteed saving (A50 L84).
  3. **NOT RUN BY DESIGN.** Every unvisited GRID point is reported "NOT RUN BY DESIGN", and claims about performance across unexecuted points are relinquished (A50 L70).
  4. **Astra's further requirements (A50 L74–L82):**
     - n* = the first n at which every required row and dose passes, each pass computed from that point's own data, with n_grid-keyed streams and no pooling (append-only);
     - every required row and dose completed at each visited n;
     - failed points and all their flags retained;
     - confirmation fresh and independent;
     - if no point passes, the grid is exhausted and confirmation blocked;
     - integrity-stop rules preserved;
     - any diagnostic point optional, with its location and treatment frozen (including when n* is already the maximum);
     - no "a single failure is expected noise" wording, and exact-identity and implementation-integrity failures never absorbed by a statistical allowance.
- **Size of the saving forgone (arithmetic only; not a lever now):** the GRID sweep would fall from 267,004,800 per C_cal cell to 200 × 4,572 × Σ(visited n). At the earliest possible stop (n* = 9) that is 8,229,600 per cell, or 123,444,000 over 15 cells, against 4,005,072,000 now.

## 4. Discrepancies and corrections found this pass
1. **V25 §8.2 totals (13 cells)** are superseded by ruling (a): 15 cells, 4,005,072,000 + 45,720,000·n. Astra's A50 L189–L201 figures re-verify for the 13-cell basis only.
2. **V25 §8.2 "Plant steps scale ×(g − 1) for any frozen g > 2"** is superseded by E2-6: steps scale ×⌈max(1, g − 1)⌉ (G).
3. **V25 §8.2's per-unit network cost of 2·d_h² flop/step** is incomplete (A50 L210). It is carried here with κ_net.
4. **V25 §8.2's bootstrap ops "10⁴·U"** omit the statistics count and the per-resample ops, and leave the no-refit assumption implicit. All three are now explicit (C4).
5. **V25 §8.2's "Not in totals" list** (dose calibration, null runs, hysteresis, simulated dip p-values) is now ledgered (B1–B3, C3). A50 L214 also asked for the bootstrap and the mixture fitting (C4, C1).
6. **Dose-calibration replicate size.** LC §3 sized a dose-calibration replicate as one 67-seed replicate. Dose calibration runs before sample-size calibration (M L372–L375), so n_seed* cannot size it; n_dc must be frozen separately.
7. **ΔLL method.** MP L69's "5-fold cross-validation" differs from the 254/127/127 held-out-final reading (LC §3, V25). The fit count differs by up to ×6 (§2).
8. **Hysteresis.** V25 L255 calls it "unscheduled", but MP L72 lists it as a REPORTED secondary statistic. It needs a schedule or an explicit withdrawal.
9. **Quantile index.** The Lead ruling k = ⌈0.99·(n_q + 1)⌉ gives **k = 991** at n_q = 1,000. Astra's concrete choice is "the 990th ordered distance" (A50 L125), and RD26 §2.2 proposes k = ⌈0.99·n_q⌉ = 990 to reproduce it. The ruled k is one order statistic more conservative. The coverage tail changes from P[Bin(1000, 0.97) ≥ 990] = 1.8130e-05 (A50 L130, reproduced) to P[Bin(1000, 0.97) ≥ 991] = 5.6601e-06. The workload is unaffected, since cost depends on n_q, not k. RD26 §2.5's coverage text must use the ruled k, and #51 should state the change to Astra.
10. **RD26 corr1 (K-1)** is a citation-precision correction only. It notes that frozen M L1127 still reads "t_s = 5τ in plants" until V25 §6.1's replacement is adopted. This ledger costs scalar plants at t_s = 0 (V25 §6.1, R6), so it depends on that adoption.
11. **Astra's arithmetic re-checked (exact):** 3,849,624,000 / 6,289,243,200; calibration 3,685,032,000 / 5,063,947,200 (A50 L198–L201); 3,341.88 h (A50 L207–L208); 1.8130 × 10⁻⁵ (A50 L130). All match. RD26's 15-cell totals match.
12. No input hash or footer failed to verify (§6).

## 5. Open items (workload)
| # | Item | Owner | Effect on ledger |
|---|---|---|---|
| O-W1 | Plant gains g (P1, N1, NC1, NC2, NC2r, LIM base) → G | CNA | scalar lines × G |
| O-W2 | d_h and the full network architecture → κ_net | P4 | network lines ∝ d_h²·κ_net |
| O-W3 | Which cells need dose calibration; n_dc; K_dc | CNA (M §8.3), RD | B1: 0 to ≈ 1.15 × 10⁹ trials |
| O-W4 | **n_c** (null-centre runs) and **n_q** (null-quantile runs) | **CNA** (RD26 §2.1–§2.2) | B2a ∝ n_c, B2b ∝ n_q |
| O-W5 | Hysteresis schedule (h, hold length) or its withdrawal | CNA/RD | B3 |
| O-W6 | ΔLL method: 5-fold CV (MP L69) or held-out final partition | RD/CNA, Lead | C1 up to ×6 |
| O-W7 | Fit restarts; NC1 per-c-level factor φ_c | RD | C1 |
| O-W8 | Dip p-value method (frozen table vs per-test simulation, N_null) | RD | C3 |
| O-W9 | Bootstrap statistics per seed S_b; no-refit assumption confirmed | RD | C4 |
| O-W10 | LIM offsets, analytic s*_LIM and fixture size N_fix (RD26 §1.3 (A)) | CNA | B4 |
| O-W11 | NC2r withdrawal (RD26 SC-2) formally adopted | Lead | §2 conditional +1 cell |
| O-W12 | Replay policy ρ_rep | Lead | D2 |
| O-W13 | Per-unit costs u (S0 preflight; Aidan's explicit yes) and per-ledger caps | P5, Aidan | turns CPU-h into budgets |
| O-W14 | Workload ledgers for the non-IGN Track B instruments (M §5.8 count formula) | RD | outside this file |
| O-W15 | E50-1, E50-3 and the remaining E50-2/E50-4 items (RD26 §3–§5) | Lead, CNA, Astra | may change cells or lines |
| O-W16 | Quantile index k: ruled form vs A50 L125's 990th (§4 item 9), to be stated to Astra | Lead → Astra | none on cost |

## 6. Inputs (whole-file sha256 and footer recomputed this pass; all MATCH)
| Abbrev | Path | Whole-file sha256 | Footer |
|---|---|---|---|
| A50 | `astra_consult50_response.txt` | `59e93cfffa8f9755262cf4736c4e8158b45064acb8348fb3d813ebc1b4d314c3` | — (no footer) |
| LC | `review/trackB_ign_full_procedure_cost_v1_Lead.md` | `7d4cbbad73d246425db425a6bf8231253d33c4cde07d4426f346650c16b9345d` | `c7d396f5…` ✔ |
| LCL | `review/trackB_ign_cost_v1_lightpass_items2to4_RD.md` | `d5ee9a1b3790aa71a6585ee77ef46bccff552e938e79d849d7cb9a78e430bdc1` | `3032e59f…` ✔ |
| V25 | `review/trackB_freezeprep_v2_5_consolidated_Lead.md` | `d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5` | `36dbcb5f…` ✔ |
| ER1 | `review/trackB_freezeprep_v2_5_erratum1_Lead.md` | `10860e98444d31c0f432b44f44427b1a522add744d42dd65ce38e20c5c349c2a` | `4d51b00c…` ✔ |
| E2 | `review/trackB_freezeprep_v2_5_erratum2_Lead.md` | `81bdfcf29ad81ac20b4effbdb8434664d82b67e0f96f3f0345504950079f4569` | `c62a3bbf…` ✔ |
| E2C1 | `review/trackB_freezeprep_v2_5_erratum2_corr1_Lead.md` | `c2c839210580f1b037580fd977421fa0cd2faaedb6a3d781ee80741f12cce212` | `62364a21…` ✔ |
| E2C2 | `review/trackB_freezeprep_v2_5_erratum2_corr2_Lead.md` | `5100f4de826dacbd422be92e056f58578fc9a5c332353885ebb0f50f62cf8092` | `da5aec39…` ✔ |
| E2C3 | `review/trackB_freezeprep_v2_5_erratum2_corr3_Lead.md` | `2f813ba4bb58507241ced0bea97354fdfc63990015786feaadeb4709e4630eec` | `8d420ab1…` ✔ |
| RD26 | `review/trackB_freezeprep_v2_6_E50_2_E50_4_RD.md` | `8a36920898f8a2aece46189631f4c5592719f0c4e5a566cf5687ba1dbc28fc73` | `c29401c4…` ✔ |
| RD26C1 | `review/trackB_freezeprep_v2_6_E50_2_E50_4_RD_corr1.md` | `ebe3a08ceab597d06b9239271ff06ae70804ded9a037bb29a1a023878998d708` | `a43bae64…` ✔ |
| M | `review/trackB_instrument_validation_scope_v3_6_merged_RD.md` | `ab80afa56ac1d5717392e278a237468e41e79c3119c2a133d14f7aa2d5a86e3b` | `bb074b33…` ✔ |
| MP | `review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` | — (no footer) |
| V2.5-RD | `review/trackB_freezeprep_v2_5_E49_2_IGN_wording_RD.md` | `ae80cc122a284b16d96f4a02144c6a9a57a104fe1c5402551ca34cada5dede72` | `d0736ba8…` ✔ |
| A49 | `astra_consult49_response.txt` | `6b66bbba1b800aa3dc8aacd024a827a82acb3346216cad8f19397cde66934468` | — (no footer) |
| A44 | `astra_consult44_response.txt` | `49afbb5d1ca63f0db692f3123e85c7ccf1c2870dbd45b48d639d39c30bc22060` | — (no footer) |
| AMD | `review/constitution_amendment_A-2026-10-24_record.md` | `2f29a07a617464e1b0a30ad77ce7c67367f31208e749f6bcbff938fa8f7c2dd6` | `222648af…` ✔ |

*DESIGN ONLY. Draft, not frozen. No freeze, execution, benchmark or timing run is authorized (A50 L250). X1–X5 and the claim ceiling unchanged. No host coupling. No consciousness claim is made or implied. Nothing was sent to Astra or anyone else.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 39371967c33a3c709e562490fe97cca7f4b3a9a71af3244393a3f8c3a2b1f269
