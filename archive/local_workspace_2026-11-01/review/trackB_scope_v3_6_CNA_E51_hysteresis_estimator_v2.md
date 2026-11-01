# Track B v3.6 freeze prep: CNA pin of the IGN hysteresis estimator (MP L72; REPORTED only) (CNA v2)

- **Author:** CNA. **Written:** 2026-11-01 13:09:23 EST (America/New_York, from `date` at write time). This is an additive file; no read-only file is rewritten. **Supersedes `trackB_scope_v3_6_CNA_E51_hysteresis_estimator_v1.md` (8673a421…), which ran to 124 lines against the 120-line limit.** The content is the same, condensed, and one citation is corrected (WL L17 only; v1's "L27 L17" was unverified).
- **Status:** PLANNING ONLY. Nothing was run as an experiment, simulation or timing run.
  - The computations were SHA-256, exact binomial sums, and a deterministic **noise-free** (σ = 0) float64 evaluation of the frozen recursion (`/workspace/scratch/cna_e51/hyst.py`, system `python3`, no RNG).
  - Float values are **UNVERIFIED for the pinned libm (P6)**.
- X1–X5 unchanged. Astra not contacted. No consciousness claims.
- **Inputs (sha256 recomputed, MATCH):** L27 = v2.7 E51-4 ledger (ccdcda05181f…); V26 = v2.6 consolidated (ff03eb81c158…); CE51 = my E51 plant file (bc27d6959e90…); A50 (59e93cfffa8f…); A51 (f7f35ec21d37…); M (ab80afa56ac1…); MP (1d5458e3319b…).

## 1. Governing text (verbatim)
- **MP L72:** "4. Secondary (REPORTED): hysteresis. Ascending and descending s sweeps, and the difference in transition points."
- **MP L84:** "IGN-P1: a bistable unit, τ·dx/dt = −x + tanh(g·x + s + ξ) with g > 1 and ξ white noise. Write w = x at a fixed readout time. Bimodal near s*, with hysteresis. **Must be MET.**"
- **M L1127:** "t_s = 5τ in plants (residual e^−5 < 1%); 20 steps in networks". The plant clause is replaced by t_s = 0 (AM-4). **Network settling is 20 steps** (L27 §4).
- **V26 L43:** "Hysteresis (MP L72): scheduled as REPORTED only (one ascending and one descending sweep per seed-unit; ≤ 27,828,000 trial-equivalents at n = 67). It enters no label."
- **A50 L214:** "The acknowledged exclusions matter: dose calibration, null-reference runs, hysteresis and dip-test calibration."
- **A51 L48:** AM-4 accepted: "This defines a reset experiment; do not describe it as stationary sampling."
- **A51 L104:** "Solving a new equilibrium at every probed input would change the reset experiment."

## 2. Protocol (scalar rows; PROPOSED)
**Departure from reset, named.** A sweep must carry state across levels; otherwise there is no direction and no hysteresis. This departs from the CE50/CE51 reset design (CE51 §6).
- **Named scoped exception AM-HYST (A-2026-10-24, for Lead ruling):** state is carried only inside the hysteresis sweeps defined here.
- Every main-protocol trial stays a reset trial: x_0 = x_lo, t_s = 0, x_ref = x_lo, and x_lo is never re-solved (A51 L104).
- Sweeps are a separate sample. They use none of the 508 Fisher–Yates slots and enter no fit, selection or label.
- They are a quasi-static protocol, **not stationary sampling** (A51 L48).

**Sweep grid H (separate from the 9-level probe grid).**
- The probe grid S = [0, 2s_c] (CE51 §8) cannot show the descending transition: for g = 2 the upper-branch fold lies at −s_c < s_1 = 0.
- Hysteresis therefore uses **H = { fl(s_c·m′)/4 : m′ = 2m + o, m = −4…4 }**, under the same single-rounding rule as V26 L58.
  - o = 0 gives [−2s_c, 2s_c] with spacing 2δ = s_c/2. Both folds ±s_c (m′ = ±4) are grid points.
  - **LIM:** o ∈ {−7, +7}, matching its probe offsets.
  - Nine levels per direction keeps the cost at the scheduled amount (§6).
  - max |u| = fl(s_c·15)/4 = 1.99815 ≤ S_max = 8, so assertion (i′) applies through the construction sweep.

**Sweep (one per direction per seed-unit; d = 0 ascending, d = 1 descending).**
- **Start state:**
  - Ascending: x = x_lo (CE51 §6; −x\* for bistable rows, the frozen x_lo for graded rows and subunits).
  - Descending: x = x_hi. That is +x\* for bistable rows; for graded rows it is the mirror −x_lo, which is 0 for N1/NC2/NC2r.
  - Both are frozen constants, so nothing is re-solved.
- **Hold:** at each level, apply exactly **n_hold = 500·G integer EM steps** (5τ; one scalar trial-equivalent, WL L17). The level is applied in order; the descending sweep uses the reverse order.
  - The hold is fixed and independent of the selected t_r, so hysteresis never depends on selection.
  - Integer step-counter assertion as in (vii-b) (V26 L53).
- **Branch indicator** at the end of each hold: **b_k = 1{x > 0}**, on the pre-nonlinearity state (M L314).
  - 0 is the unstable middle root at s = 0.
  - Noise-free stable states lie at |x| ≥ √(1 − 1/g) = 0.7071 at g = 2. That is ≥ 7.4·σ_ref from the threshold.
- **NC1:** the subunit for each (seed, direction) is fixed by seed index mod 2 (PROPOSED), so the sweep count is unchanged.

**Network rows:** the same shape (two directions, nine levels, branch indicator, carried state).
- One **20-step null settling** (M L1127) precedes each sweep, at the sweep's first level.
- The network grid, the indicator threshold on w = ‖x_ws − x_ref‖ and the hold length are **PENDING P4** (network width and normalisation ABSENT).
- **Budget constraint:** ≤ 18 network trial-equivalents = 18 × 28 = 504 steps per seed-unit, including both settlings. Example: a 24-step hold gives 2 × (20 + 9 × 24) = 472.

## 3. Statistic and estimator (fit-free; PROPOSED)
- **Switch points** (first passage, no fit). These are **not** the H1 ŝ\*. RD's per-readout ŝ\* granularity is not decided or used here.
  - Ascending: k↑ = the first level with b = 1, and ŝ↑ = (h_{k↑−1} + h_{k↑})/2.
  - Descending: k↓ = the first level, in sweep order, with b = 0, and ŝ↓ = the midpoint with its predecessor.
- **Censoring:**
  - No switch in the sweep → ŝ↑ = +∞ (right-censored) or ŝ↓ = −∞.
  - A switch at the very first level → ŝ = h_1 boundary-censored (level-1 switch).
  - Re-crossings after the first passage are counted and REPORTED.
- **Per-seed width** W_j = ŝ↑ − ŝ↓. This is MP L72's "difference in transition points". Loop area is not adopted (MP names the difference).
- **Per (replicate, cell, c-level):** **median of W_j over the n seeds**, with +∞ ranked last.
- **CI:** **exact distribution-free order-statistic interval** [W_(k), W_(n+1−k)], with k the largest rank such that 1 − 2·P[Bin(n, ½) ≤ k − 1] ≥ 0.95.
  - n = 9: ranks (2, 8), coverage 0.9609375.
  - n = 67: ranks (26, 42), coverage 0.95020.
  - It is computed by integer `comb`, assuming independent seeds. **Data-only analysis: no resampling, no RNG, no simulated null or reference table.** This complies with the room's constraint; a percentile bootstrap is not needed.
- **Cell summary (REPORTED):** quantiles (0.1, 0.5, 0.9) of the 200 replicate medians, plus the count of replicates whose CI lower bound is > one H spacing (2δ). That spacing is the estimator's resolution floor (§5).
- **Undefined / failure handling:**
  - median = +∞ (≥ half the seeds censored) → **NOT LOCATABLE (censored)**, REPORTED;
  - CI upper = +∞ → "unbounded above";
  - a NaN/±∞ in a sweep → that sweep's computation **stops and is recorded as a construction failure** (M L3421).
  - Because hysteresis gates nothing, whether such a failure also flags the plant code for the main rows is **L-H4**.

## 4. RNG role (new; no reuse)
- **New role `ign-hyst-sweep`.** Address under ACI-TrackB-RNG-v2: role, replicate-set, cell, replicate, seed, plus the direction d.
- **Counter (t, d, 0, 0)**, with t = global step 1…9·n_hold within the sweep. One standard normal per step, drawn by Box–Muller as for `ign-trial` (V25 L117–L124).
- It is distinct from `ign-trial`, `ign-partition`, `ign-null-centre` and `ign-null-quantile` (M L372 "never reused across roles").
- **KAT:** the first 4 normals under the zero placeholder key for the role address, computed at freeze under the pinned implementation. The hash is fixed in the freeze record. **PENDING P6.**
- The sweeps are in-protocol runs at execution time, not prep. No null table is built.

## 5. Noise-free example (g = 2, h = 1/100, n_hold = 500; UNVERIFIED for P6)
- Analytic folds are at ±s_c = ±0.532839975353552 (3fe10d066b84a372), so the analytic loop width is 2s_c = 1.065679950707104.
- **P1 ascending** end-of-hold x at m′ = −8…8: −0.9953, −0.9924, −0.9868, −0.9768, −0.9578, −0.9178, **−0.7954 (m′ = 4, at the fold)**, **+0.8792 (m′ = 6)**, +0.9947.
  - ŝ↑ = 5δ = 1.25·s_c = 0.66605. The descending sweep mirrors it exactly: ŝ↓ = −0.66605.
  - **W = 1.3320999383838799 = 2.5·s_c.** The 0.5·s_c excess over 2s_c is grid quantisation: a fold at a grid point switches at the next level.
- **N1 (graded, g = 0.5; no hysteresis analytically):** ŝ↑ = +δ and ŝ↓ = −δ, so **W = 0.266419987676776 = one H spacing**. This comes from the finite-hold lag: x = −0.038 at s = 0 on the way up.
- **Resolution floor:** W ≤ 2δ (one spacing) does not indicate hysteresis. These are deterministic references, not simulated nulls.

## 6. Cost check against L27 (≤ 27,828,000 trial-equivalents)
- Per seed-unit: 2 directions × 9 levels × 1 trial-equivalent = 18. 1,546,000 seed-units (A51 L153) × 18 = **27,828,000**, matching L27 L99.
  - Scalar: 829,000 × 18 = 14,922,000.
  - Network: 717,000 × 18 = 12,906,000, matching L27 L92.
  - Network steps stay ≤ 504 per seed-unit (§2).
- **Fits: F3 falls to 0.** The estimator is fit-free. L27 L65 counted ≤ 9,276,000 / 11,803,200 calls, so the fit totals fall to **56,322,000 / 72,263,700** (from 65,598,000 / 84,066,900). **This is a cost DECREASE, flagged.**
- The CI costs integer arithmetic only.
- The scheduled total **4,005,072,000 + 45,720,000·n is unchanged**.

## 7. REPORTED only; never gates
- Hysteresis enters no label, gate, eligibility, realization, calibration or selection (V26 L43; MP L72 "Secondary (REPORTED)").
- MP L84's "with hysteresis" is a plant description, not a gate. It is not tested as one.
- AQ1 (MP L303) proposed hysteresis as primary; it is **not adopted**.

## 8. Needs the Lead's ruling
| # | Item |
|---|---|
| L-H1 | AM-HYST: carried state inside the sweeps only, as a named reset exception |
| L-H2 | The H grid (m′ = 2m + o, nine levels over [−2s_c, 2s_c]) and the ±x start states |
| L-H3 | The fit-free switch-point estimator, the exact order-statistic CI and the resolution-floor reporting; F3 → 0 calls |
| L-H4 | A NaN in a sweep: hysteresis-only failure, or also a flag on the main rows' plant code |
| L-H5 | New RNG role `ign-hyst-sweep` with counter (t, d, 0, 0); KAT PENDING P6 |
| L-H6 | NC1 subunit by seed mod 2; the network grid, threshold and hold PENDING P4, within ≤ 504 steps |

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: a3440ea94d4b125450ccceb74b5410b56fb8eae567637461d435adddb0c56353
