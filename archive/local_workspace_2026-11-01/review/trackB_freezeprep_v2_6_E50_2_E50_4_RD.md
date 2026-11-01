# Track B freeze preparation v2.6: E50-2 and E50-4 proposed freeze text (RD)

- **Author:** Research Delegate (RD)
- **Date/time:** 2026-11-01 12:11 EST (America/New_York, from `date`)
- **Status:** DESIGN/TEXT ONLY. No runs, simulations or timing. Arithmetic is exact (Python integers/`fractions`) plus sha256 only. Additive file; edits no other file. If an error is found after locking, it will go in a separate `_corr` file, never a rewrite.
- **Governing text:** Astra #50, `astra_consult50_response.txt`, sha256 `59e93cfffa8f9755262cf4736c4e8158b45064acb8348fb3d813ebc1b4d314c3` (16,768 B). Quoted verbatim as "A50 Lnn".
- **Inputs verified this session (whole-file sha256; footer recomputed OK where present):** v2.5 consolidated `d101438d…` (footer OK); Lead erratum1 `10860e98…` (OK); erratum2 `81bdfcf2…` (OK); corr1 `c2c83921…` (OK); corr2 `5100f4de…` (OK, superseded); corr3 `2f813ba4…` (OK); RD E49-2 `ae80cc12…` (OK); RD E49-2 erratum1 `c1bc0f0d…` (OK); CNA E49 `d620918f…` (OK); CNA addendum1 `55030ebd…` (OK); CNA dose0/xref `647a72d2…` (OK); M = merged v3.6 `ab80afa5…` (OK); MP = `trackB_measurement_plan_v1_RD.md` `1d5458e3…` (no footer); packet v4 manifest `57c0915d…` (footer `d4f70d62…` OK).
- **Abbreviations:** V25 = v2.5 consolidated; C3 = erratum2 corr3; CD0 = CNA dose0/xref; CNA2 = scope v2 CNA items file; MP and M as above.
- **Labels:** PROPOSED = RD text for the Lead to adopt or amend. PENDING (owner) = value or decision not yet set. Nothing here is frozen. A50 L250: "no freeze, execution or timing run is authorized."

---

## 0. Summary

| Item | One-line result |
|---|---|
| E50-2 (i) s* rule | PROPOSED: ŝ* = −θ₀/θ₁ from the frozen H1 logistic π(s) fitted on the selection partition, per replicate and per c-level, pooled across seeds. Fixed bound [s_1, s_9] set before data. Near-transition pair = bracketing pair, with a lower-index tie rule. Non-locatable or outside → UNAVAILABLE (IGN-UA-SSTAR). Grid values are PENDING CNA. |
| E50-2 (ii) aggregate gates | PROPOSED: G-i per (replicate, c-level) on selection data. G-ii is the per-(seed, bin) quota itself; a shortfall is INCOMPLETE, not a separate UNAVAILABLE. G-iii is per (replicate, near-transition bin) on final data, with the floor PENDING CNA. A precedence order is given. |
| E50-2 (iii) LIM path | PROPOSED: (A) a deterministic gate fixture validates the analytic boundary predicate, and (B) end-to-end validation of the estimated-ŝ* path in the 2 LIM confirmation cells, with gate ≥ 0.90 correct UNAVAILABLE. Outcome labels are given. **CONFLICT:** V25 sets LIM OUT only under a non-fitted rule, but the gate here is fitted. The Lead must choose OUT (confirmation-only required check) or IN (+2 C_cal cells, figures in §1.4). |
| E50-2 (iv) cell list | 13 calibration cells and 20 confirmation cells enumerated by ID, row and dose index. DOSE0 = 2^64−1. The RAND-INIT dose-0 drop and NC2r's withdrawn role are worded as named prospective scope changes. Totals recheck exactly: 3,471,062,400 + 42,062,400·n_seed. |
| E50-4 centre | PROPOSED: coordinatewise median of x_ref over n_c centre runs (n_c odd recommended), per (replicate, seed, cell). n_c is PENDING Lead/CNA. |
| E50-4 quantile | PROPOSED: T = X_(k) with k = ⌈0.99·n_q⌉, no interpolation. Under Astra's illustrative n_q = 1000, k = 990. n_q is PENDING Lead/CNA. |
| E50-4 allocations | PROPOSED: new roles `ign-null-centre` and `ign-null-quantile` with partition field "fitting" and suffix = run ordinal. Evaluation stays on `ign-trial`. Runs are never reused. |
| E50-4 tie rule | PROPOSED: eligible iff d ≤ T (ties count as inside). Justification: this is the only rule under which the certified exclusion bound 1 − k/(n_q+1) still holds when ties occur. |
| E50-4 coverage claim | P(D_new ≤ X_(k)) = k/(n_q+1), exactly under continuity and ≥ with ties, per threshold. At n_q = 1000 (not frozen) this is 990/1001 = 90/91 = 0.98901…, and P[Bin(1000, 0.97) ≥ 990] = 1.8129913468e-05, which confirms A50 L130. |
| E50-3 dependencies | PENDING CNA: the analytic s* of the scalar plants, the scalar domain, the root rule, the monostable noise reference, and recursion vs SDE (§3). |
| corr3 advisory (for CNA, E50-1) | Same direction as Astra (no free pass from missing assessments; rows 1/2/3/4b all covered). It conflicts on the label (FAIL vs UNRESOLVED) and keeps a PASS branch for NOT ASSESSED. It also needs the BOUNDARY/UNRESOLVED split and the "plant realization" renaming (§4). |

---

## 1. E50-2

A50 L242: "E50-2. Freeze the IGN transition-location rule, aggregate gates and limitation-validation path. Enumerate calibration and confirmation cells, including the prospective dose-zero and NC2r scope changes."
A50 L8 (E49-2): "Allocation is resolved. The transition-location rule, aggregate gates and revised settling rule need complete definitions."

### 1.1 (i) IGN transition-location rule s*

Sources:
- MP L66: "Ignition H1: w | s ~ π(s)·N(μ_hi, σ_hi²) + (1 − π(s))·N(μ_lo, σ_lo²), with π(s) logistic and μ_hi, μ_lo shared across s. H1 is fitted with the same covariate conditioning as H0."
- MP L70: "Hartigan dip test on w at the two grid levels nearest the fitted transition s* (where π = 0.5), conditioned on c."
- MP L79: UNAVAILABLE if "the transition s* lies outside the probed grid".
- A50 L88: "Every grid has fixed boundaries. That does not determine whether the response transition lies inside them."
- A50 L93: "A transition location estimated from selection data."
- A50 L155: "Selection among them must use selection data; final outcomes cannot choose the winning time."

**PROPOSED freeze text (IGN-S\*):**

> **Grid.** For each IGN cell, the strength grid is S = (s_1 < s_2 < … < s_9). It has K_s = 9 levels, all of them required bins (B_req = K_s = 9). Its values are frozen per plant/network setting before any calibration data exist. Grid values are PENDING CNA (plant parameters; E50-3 cross-reference §3). The **grid bound** is the closed interval [s_1, s_9]. It is fixed with the grid and is never fitted or widened after data.
>
> **Estimator.** Within each replicate, using **selection-partition trials only** (Fisher–Yates positions 254–380 of each (seed, bin); M L376), pooled across all seeds of the replicate, fit the frozen H1 of MP L66 by maximum likelihood with π(s) = 1/(1 + exp(−(θ₀ + θ₁·s))). If c is present, fit separately per c-level, as MP L65–L66 require. The H1 fitter is identical to the one used for ΔLL: same optimizer, initialisation and restart set. These settings are PENDING RD; the best-likelihood restart is kept, and ties go to the lowest restart index. For each c-level, **ŝ\*_c = −θ₀/θ₁**, defined only when the fit converged, every value is finite, and θ₁ > 0.
>
> **Boundary decision (gate G-i).** ŝ\*_c is *inside* iff s_1 ≤ ŝ\*_c ≤ s_9 (closed interval; equality counts as inside). If, for any c-level, the fit fails, θ₁ ≤ 0, any value is non-finite, or ŝ\*_c is outside the bound, the replicate's IGN label is **UNAVAILABLE** with reason code IGN-UA-SSTAR. The cause is recorded: FIT-FAIL, NONINCREASING or OUTSIDE-LOW/HIGH.
>
> **Near-transition bins.** For an inside ŝ\*_c, the near-transition pair is (s_i, s_{i+1}), with i the unique index in 1…8 such that s_i ≤ ŝ\*_c < s_{i+1}. If ŝ\*_c = s_9 the pair is (s_8, s_9). On an equally spaced grid this bracketing pair equals "the two grid levels nearest" (MP L70). On an unequal grid, the bracketing pair governs, by this text.
>
> **No final-data choice.** The pair is fixed from selection data before any final-partition statistic is computed. Final outcomes never choose or move it (A50 L155, applied by analogy).

Notes:
- (a) The pooled-across-seeds unit follows V25 §2.4 G-i, which says "per replicate, selection partition, pooled across seeds". A per-seed ŝ\* would need a per-seed G-i, which is not proposed.
- (b) **Interaction to check, PENDING calibration:** graded rows (N1, NC1/NC2 confounds) could produce θ₁ ≤ 0 or an outside ŝ\*. That would turn an expected NOT MET into UNAVAILABLE. These rows are all in C_cal, so this rate is measured, not assumed. The G-i rate per row is reported.
- (c) The exact "θ₁ > 0" orientation assumes π increases in s. The orientation is PENDING RD: the convention that larger s means more ignition.

### 1.2 (ii) The three aggregate gates (MP L78–L81)

Sources:
- MP L78–L81, verbatim: "**UNAVAILABLE** if: / the transition s* lies outside the probed grid; / fewer than n_trial trials fall per near-transition bin; / Var(w) is below a floor (workspace collapse, §3)."
- M L1130 coverage: "At **every** required strength bin and each near-transition bin, the one-sided Clopper–Pearson lower bound of the eligible fraction is ≥ 0.90. Otherwise IGN is **UNRESOLVED**".

**PROPOSED freeze text (IGN-GATES):**

| Gate | Evaluation unit | Data | Rule | Outcome |
|---|---|---|---|---|
| G-i (MP L79) | (replicate, c-level), pooled across seeds | Selection partition | IGN-S\* §1.1 | UNAVAILABLE (IGN-UA-SSTAR) |
| G-ii (MP L80) | (seed, required bin), for all 9 bins, so it includes both near-transition bins | Final partition (127 slots) | **This is the quota, not a separate test.** n_trial := 100 eligible of the 127 final slots (V25 §2.4). Missing, crashed or non-finite slots count as ineligible and are never replaced (CNA E48 F-6) | Shortfall makes the replicate **INCOMPLETE**, counted (M L2009). Reported once, under one reason code |
| Coverage (M L1130) | (replicate, bin) for every required bin and each near-transition bin | Final partition, eligibility | One-sided CP lower bound ≥ 0.90 | UNRESOLVED |
| G-iii (MP L81) | (replicate, near-transition bin, c-level), pooled across seeds | Final partition, eligible trials only | Var(w) ≥ floor (pre-nonlinearity w, MP L62). Floor value PENDING CNA | UNAVAILABLE (IGN-UA-COLLAPSE) |

> **Relation to the quota.** G-ii and the per-(seed, bin) quota are one test, counted once. MP L80's label "UNAVAILABLE" is **superseded** for this case by INCOMPLETE (M L2009). A quota shortfall is an execution incompleteness, not a property of the instrument's answer.
>
> **Precedence** (every gate is computed and recorded whatever the label):
> 1. construction failure or quota shortfall → INCOMPLETE;
> 2. G-i → UNAVAILABLE;
> 3. coverage → UNRESOLVED;
> 4. G-iii → UNAVAILABLE;
> 5. otherwise MET / NOT MET / BOUNDARY per MP L75–L77.
>
> G-i comes before coverage because the near-transition bins that coverage needs do not exist without an inside ŝ\*.

Conflict to note: MP L80 says "UNAVAILABLE" and V25 §2.4 says "reported once". Using INCOMPLETE is an RD proposal and needs the Lead's adoption.

### 1.3 (iii) LIM limitation-validation path

Sources:
- A50 L86: "Q3. The proposed LIM exclusion is not justified by a fixed grid boundary alone."
- A50 L92: "A known-answer plant with analytically specified transition location, checked by a deterministic boundary predicate."
- A50 L95: "The first can be validated through a separately costed deterministic gate fixture without repeating the full sample-size sweep. The second needs end-to-end validation of its estimator, uncertainty and UNAVAILABLE decision."
- A50 L97: "In both cases, the limitation behavior remains a required check. "Outside calibration" must not become "untested.""
- MP L88: "IGN-LIM: a bistable unit with s* outside the probed grid. **Must be UNAVAILABLE**, never NOT MET."
- MP L199: "Correct UNAVAILABLE on LIM | ≥ 0.90".
- V25 L174: "LIM OUT only if the MP L79 "s* outside grid" decision is a **fixed, pre-registered grid bound** (n_seed-independent, not fitted from pooled data). If the frozen rule estimates s* from data, LIM goes IN (CD0 L42)."

**Finding.** The instrument's G-i in §1.1 has to *estimate* s\*. Networks have no analytic s\*, and the gate cannot read plant ground truth. LIM is therefore in A50 L93's second case for the instrument decision, even though LIM is also a known-answer plant (first case) for its construction. Under V25's own L174 condition, the fitted rule puts LIM **IN**, which contradicts the 13/20 set. **CONFLICT: decision for the Lead.**

**PROPOSED freeze text (IGN-LIM-VAL), written so that it holds under either Lead choice:**

> **(A) Deterministic gate fixture** (first case, A50 L92/L95). For each LIM dose index (2 levels; offsets in grid steps, PENDING CNA), the analytic transition location s\*_LIM of the noise-free plant is computed by the frozen analytic rule (PENDING CNA, E50-3 §3). The frozen predicate "inside iff s_1 ≤ s\* ≤ s_9" is applied to it. It must return OUTSIDE. The same predicate code is also run on a frozen fixture list of points: s_1, s_9, one inside point, and one point outside on each side, each with its expected verdict. The fixture involves no sampling. It is costed separately as a fixed computation, recorded under E50-5 and owned by the Lead. Outcomes:
> - FIXTURE-PASS (all verdicts match);
> - FIXTURE-FAIL (any mismatch). This is a construction failure. LIM is NOT VALID and the IGN limitation claim is FAIL.
>
> **(B) End-to-end validation** (second case, A50 L95). Each of the 2 LIM cells runs the full instrument (estimator §1.1, gates §1.2) at R = 200 replicates. Per cell, the outcome is the fraction of replicates labelled UNAVAILABLE with reason IGN-UA-SSTAR. The required check: the one-sided 95% CP lower bound of that fraction is ≥ 0.90 (MP L199; M L345). Any replicate labelled NOT MET or MET is reported individually; MP L88 says "never NOT MET". The check's labels:
> - **PASS:** the bound is ≥ 0.90 in both cells and FIXTURE-PASS holds.
> - **FAIL:** the bound is < 0.90 in either cell (an assessed criterion violated, A50 L50–L51).
> - **UNRESOLVED:** INCOMPLETE replicates leave too few assessed replicates for the bound to be computed. This blocks PASS (A50 L47–L48).
>
> **When.**
> - (A) runs before any calibration data.
> - (B), Lead option **OUT**: (B) runs only in confirmation at the inherited n_seed (2 cells, as in V25). It is a required check, so a FAIL there blocks the IGN limitation claim. The report discloses that n_seed selection did not protect it (CD0 L38/L42 risk accepted by name).
> - (B), Lead option **IN**: the 2 LIM cells join C_cal and the check also enters the n_seed selection.

### 1.4 (iv) Calibration and confirmation cell list

Sources:
- A50 L111: "The 20-cell confirmation count needs an explicit cell-ID list. The condensed description does not uniquely reconstruct that membership."
- A50 L203: "These totals are correct conditional on the 13/20 sets and stated step-3a workload. They do not verify that those sets contain every required cell."
- Membership follows V25 §5 (table L159–L169) and C_cal/C_conf at L171.

Dose index = the u64 "dose index" field of address v2, numbered 0, 1, 2 in the listed order of each row's required doses. DOSE0 = 2^64 − 1 = 0xFFFFFFFFFFFFFFFF, unsigned (Lead E2-8).

| Cell ID | Row | Type | Dose index | Dose (value) | Role | C_cal | C_conf |
|---|---|---|---|---|---|---|---|
| IGN-P1/0 | IGN-P1 | scalar | 0 | nominal g, PENDING CNA | required (P) | ✔ | ✔ |
| IGN-N1/0 | IGN-N1 | scalar | 0 | g < 1, PENDING CNA | required (N) | ✔ | ✔ |
| IGN-NC1/0 | IGN-NC1 | scalar | 0 | Δs = 2 grid steps | required (confound) | ✔ | ✔ |
| IGN-NC1/1 | IGN-NC1 | scalar | 1 | Δs = 4 grid steps | required (confound) | ✔ | ✔ |
| IGN-NC2/0 | IGN-NC2 | scalar | 0 | clip quantile 0.8 | required (confound) | ✔ | ✔ |
| IGN-NC2/1 | IGN-NC2 | scalar | 1 | clip quantile 0.6 | required (confound) | ✔ | ✔ |
| BOTT/0 | BOTTLENECK-ONLY | network | 0 | g_b level 1, PENDING | required (confound) | ✔ | ✔ |
| BOTT/1 | BOTTLENECK-ONLY | network | 1 | g_b level 2, PENDING | required (confound) | ✔ | ✔ |
| RINIT/0 | RAND-INIT (IGN part) | network | 0 | g_0 = 0.9× default | required (confound) | ✔ | ✔ |
| RINIT/1 | RAND-INIT (IGN part) | network | 1 | g_0 = 1.0× default | required (confound) | ✔ | ✔ |
| RINIT/2 | RAND-INIT (IGN part) | network | 2 | g_0 = 1.1× default | required (confound) | ✔ | ✔ |
| ARCH/0 | Architecture-imposed | network | 0 | β level 1, PENDING RD/CNA | required (confound) | ✔ | ✔ |
| ARCH/1 | Architecture-imposed | network | 1 | β level 2, PENDING RD/CNA | required (confound) | ✔ | ✔ |
| IGN-NC2r/0 | IGN-NC2r | scalar | 0 | single construction, no dose declared (CNA) | REPORTED, descriptive | — | ✔ |
| IGN-LIM/0 | IGN-LIM | scalar | 0 | s\* offset level 1, PENDING CNA | required check (§1.3) | — (Lead option) | ✔ |
| IGN-LIM/1 | IGN-LIM | scalar | 1 | s\* offset level 2, PENDING CNA | required check (§1.3) | — (Lead option) | ✔ |
| IGN-NC1/D0 | IGN-NC1 | scalar | DOSE0 | Δs = 0 | REPORTED dose-0 sanity | — | ✔ |
| IGN-NC2/D0 | IGN-NC2 | scalar | DOSE0 | no clipping | REPORTED dose-0 sanity | — | ✔ |
| BOTT/D0 | BOTTLENECK-ONLY | network | DOSE0 | linear gate | REPORTED dose-0 sanity | — | ✔ |
| ARCH/D0 | Architecture-imposed | network | DOSE0 | linear gate | REPORTED dose-0 sanity | — | ✔ |

**Counts.**
- C_cal = 13: 6 scalar (P1, N1, NC1×2, NC2×2) and 7 network (BOTT×2, RINIT×3, ARCH×2).
- C_conf = 20: 13 + NC2r 1 + LIM 2 + DOSE0 4. That is 11 scalar (6 + 1 + 2 + 2) and 9 network (7 + 2).
- These match V25 L171.

**Dose-0 wording.** A50 L105: "They need not produce NOT MET: other mechanisms may remain. Keeping them REPORTED and confirmation-only is appropriate." Proposed text:
> The four dose-0 cells are REPORTED, confirmation-only, and never block or pass a row. They are never in calibration or step 3a, and no arm is reused.

**Named prospective scope change SC-1 (RAND-INIT dose 0).**
- A50 L107: "Dropping the proposed RAND-INIT zero dose is acceptable as a named prospective scope change if it creates degeneration rather than a meaningful confound-off condition. Retain the required nonzero doses."
- Proposed text:
> Deviation from CNA2 L242 ("a dose-0 sanity level that is REPORTED only"): RAND-INIT has no dose-0 cell. The candidate off value g_0 → 0 makes W_rec's init spectral radius 0, a degenerate network, not a confound-off condition (Lead E2-7). The required doses g_0 ∈ {0.9, 1.0, 1.1}× (RINIT/0–2) are retained.

**Named prospective scope change SC-2 (NC2r).**
- A50 L109: "NC2r can be confirmation-only and descriptive if its required validation role is explicitly withdrawn. "Already covered" is not demonstrated equivalence. The report must not claim calibrated performance on recurrent-clipping mechanisms from another row's success."
- Proposed text:
> IGN-NC2r's required validation role is **withdrawn**. IGN-NC2r/0 is confirmation-only, descriptive and REPORTED. The report claims no calibrated performance on recurrent-clipping mechanisms, including from Architecture-imposed's success. NC2r is excluded from C_cal and from every acceptance criterion.
- The brief's phrase "NC2r is out" means OUT of C_cal. NC2r keeps its 1 confirmation cell, per V25 L168.

**Totals recheck** (exact integers; per-cell figures from V25 L218 and L225):
- Calibration sweep per C_cal cell: 267,004,800. Then 13 × 267,004,800 = **3,471,062,400** ✔.
- Per-n_seed coefficient: 13 × 1,828,800 (step 3a) + 20 × 914,400 (confirmation) = 23,774,400 + 18,288,000 = **42,062,400** ✔.
- At n_seed = 67: 6,289,243,200. At n_seed = 9: 3,849,624,000. Both match A50 L189–L201.
- Under Lead option LIM IN: C_cal = 15 adds 2 × 267,004,800 = 534,009,600 and 2 × 1,828,800 = 3,657,600·n_seed. The total becomes 4,005,072,000 + 45,720,000·n_seed, which is 7,068,312,000 at 67 and 4,416,552,000 at 9. These are conditional figures only, not adopted.
- Per A50 L203, these totals do not themselves prove membership. The table above is the membership list for Astra to check.

---

## 2. E50-4: network reference centre and quantile tolerance

A50 L246: "E50-4. Freeze the network reference-center and quantile procedure, independent sample allocations, rank/tie convention and precise coverage claim. Retain independent final eligibility checks."
A50 L119: "The proposed network quantile gate is defensible, with a finite-sample specification. An empirical 0.99 quantile does not guarantee exactly 1% exclusion on new runs."
A50 L121–L126: "A concrete prospective choice is: / - Fit and freeze the center using a separate portion of fitting data. / - Generate 1,000 independent null runs per applicable seed/network setting for threshold estimation. / - Use the 990th ordered distance as the threshold, with a fixed tie rule. / - Do not use these runs again as final eligibility observations."

Scope: networks only (M L1129 "Network instruments only."). Scalar plants keep t_s = 0 and x_ref = x_lo (M L1127).

### 2.1 Reference centre

> **PROPOSED (NET-CENTRE).** For each (replicate, seed) of each network cell (BOTT/·, RINIT/·, ARCH/·, including D0 cells), run n_c **centre runs**. Each is a null-input settling run of t_s = 20 steps (M L1127), from the declared initial-state law, under frozen weights. The run's x_ref ∈ ℝ^d is the end-of-settling state.
>
> The centre is c = the **coordinatewise median** of the n_c x_ref vectors. Per coordinate: the ((n_c+1)/2)-th order statistic if n_c is odd; the arithmetic mean of the (n_c/2)-th and (n_c/2+1)-th if n_c is even. **n_c odd is recommended**, so that c is an observed coordinate value with no averaging.
>
> c is computed from the centre runs only and frozen before any quantile run's distance is computed.
>
> **n_c: PENDING (Lead/CNA, costed under E50-5).** A50 L134: "The number of center-fitting runs must also be declared and costed."

The distance is d = ‖x_ref − c‖₂ (Euclidean), the same norm as V25 §6.2.

### 2.2 0.99-quantile procedure

> **PROPOSED (NET-QUANT).** For each (replicate, seed, cell), run n_q **quantile runs**, independent of the centre runs and drawn identically. Compute d_1 … d_{n_q} and sort ascending, keeping duplicates. The tolerance is T = d_(k), the k-th order statistic, with **k = ⌈0.99·n_q⌉** (ceiling, computed in exact rational arithmetic). There is **no interpolation**. Require n_q ≥ 100, so that 1 ≤ k < n_q, i.e. so that k ≤ n_q − 1.
>
> At Astra's illustrative n_q = 1000 this gives k = ⌈990⌉ = **990**, the "990th ordered distance" of A50 L125.
>
> **n_q: PENDING (Lead/CNA).** A50 L124's 1,000 is a "concrete prospective choice", not yet frozen.

Note: the alternative k = ⌈0.99·(n_q+1)⌉ would give 991 at 1000, with expected coverage 991/1001 ≥ 0.99. The ⌈0.99·n_q⌉ form is proposed because it reproduces A50 L125 exactly. The claim in §2.5 is stated for whichever k is frozen.

### 2.3 Independent sample allocations (address v2)

> **PROPOSED (NET-ROLES).** Two new roles are added to the address-v2 role registry. The existing field order and length-prefix encoding are unchanged.
>
> | Role | Partition field | Bin | Suffix (u64, BE) | Counter (t, s, 0, 0) | Use |
> |---|---|---|---|---|---|
> | `ign-null-centre` | "fitting" | not applicable (null input) | run ordinal r = 0…n_c−1 | t = absolute settling step 0…19; s = frozen ordinal in the IGN variable list (PENDING CNA, V25 O10) | centre c only |
> | `ign-null-quantile` | "fitting" | not applicable | run ordinal r = 0…n_q−1 | as above | threshold T only |
> | `ign-trial` (existing) | "final" | bin | slot j (0…507) | (step, 0) as frozen | final eligibility (d_trial ≤ T) and statistics |
>
> The other address fields (replicate set, generator ID, row ID, dose index (DOSE0 for D0 cells), n_grid, replicate, seed) are those of the cell, so every (replicate, seed, cell) has its own keys.
>
> **No reuse.** Distinct role tags give distinct keys. Centre runs never enter T. Quantile runs never enter c. Neither is ever a final eligibility observation (A50 L126) or a probe trial. Each final trial's settling uses its own `ign-trial` stream; that is the "independent final eligibility check" of A50 L246.
>
> The banned counter inputs are unchanged.
>
> **Sentinel conformance (A50 L181):** these roles' membership is fixed by role tag and not by a generated partition, so the fixed string "fitting" is not circular.

Byte-level KAT vectors for the two new roles are PENDING. A KAT needs a frozen master seed, generator and row IDs. RD will supply them when those IDs are frozen; none are invented here.

### 2.4 Rank/tie convention

> **PROPOSED (NET-TIE).**
> - **Ties in the order statistic:** T is a value. Duplicate distances occupy consecutive ranks, and d_(k) is well defined whatever the ties.
> - **Ties at the gate:** a final trial is **eligible iff d_trial ≤ T** (a tie counts as inside).
> - Every tie (d_trial = T exactly) is counted and reported per cell.
>
> **Justification (conservative choice).** The finite-sample guarantee this gate certifies is an upper bound on spurious exclusion of a settled trial: P(d_new > X_(k)) ≤ 1 − k/(n_q+1). By exchangeability, that bound holds **with or without ties** when the gate is "≤". With "<", ties could raise exclusion above the bound.
>
> Over-inclusion at an exact tie has probability 0 under continuity. It is also no rescue for a bad workspace, because the G-iii collapse gate and coverage stay operative. A50 L134: "The final eligibility gates remain operative; a broad tolerance cannot rescue a collapsed workspace or an absent response."

### 2.5 Exact coverage claim

> **PROPOSED (NET-COVER).** Conditions:
> - (C1) the n_q quantile-run distances and a new null distance are exchangeable. This holds if they are i.i.d. given the frozen network, seed, cell, centre and settling protocol, and the final trial's settling procedure is identical in law to a quantile run's.
> - (C2) the centre c is fixed independently of the quantile runs and the new run (separate centre runs, §2.3).
> - (C3) the distance distribution is continuous.
>
> Under (C1)–(C3): **P(D_new ≤ X_(k)) = k/(n_q + 1)** exactly, marginally over the quantile sample. Under (C1)–(C2) alone: ≥ k/(n_q+1).
>
> The conditional coverage C = F(X_(k)) ~ Beta(k, n_q − k + 1), so **P(C < p) = P[Bin(n_q, p) ≥ k]**.
>
> This is a **per-threshold** statement. It is not a simultaneous guarantee over seeds, cells or the battery (A50 L132). It describes null-run exclusion only, not the coverage gate M L1130.

Evaluated at Astra's illustrative n_q = 1000 and k = 990 (**not frozen**; exact fractions):
- k/(n_q+1) = 990/1001 = **90/91 = 0.989010989…**
- Expected exclusion is 1/91 = 0.010989…, which is **not** exactly 1% (A50 L119).
- P[Bin(1000, 0.97) ≥ 990] = **1.8129913468 × 10⁻⁵**, from an exact rational sum. This **confirms** A50 L130's "approximately 0.00001813".

---

## 3. Items that depend on E50-3 (PENDING CNA)

A50 L244: "E50-3. Define a nonzero noise reference for monostable and other conditions lacking two attractors; pin the scalar parameter domain, root computation and failure rule. State whether the numerical recursion or the continuous-time SDE is the validated object."

| Item here | Depends on | Status |
|---|---|---|
| §1.1 grid values s_1…s_9 per scalar plant | scalar parameter domain (A50 L153), root rule | PENDING CNA |
| §1.3 (A) analytic s\*_LIM and the LIM offsets | root computation and failure rule (A50 L153) | PENDING CNA |
| G-iii Var(w) floor (§1.2) | noise reference: σ = 0.05·\|x_hi − x_lo\| is undefined for monostable N1 (A50 L138–L142) | PENDING CNA |
| Whether ŝ\* refers to the discrete generator or the SDE | A50 L151: "Either define the discrete generator as the tested plant, or separately justify any claim about its continuous-time counterpart." | PENDING CNA |
| §2 network centre and quantile | none from E50-3 (networks are discrete by construction) | not dependent |

---

## 4. Advisory for CNA (owner of E50-1): corr3 vs A50 Q1/E50-1

Texts compared:
- C3 L13: **"NOT ASSESSED passes only when n1 = n2 = n3 = n4b = 0; otherwise the row FAILS."**
- A50 L240: "Insufficient support for a required assessment is UNRESOLVED, never PASS."

| Point | Astra | corr3 | Verdict |
|---|---|---|---|
| Missing assessments cannot pass via rows 1/2/3/4b | L56: "Apply the insufficient-support rule regardless of whether the missing assessments arise from rows 1, 2, 3 or 4b" | Covers n1, n2, n3, n4b | **Consistent** in scope and direction |
| Any NOT ASSESSED → PASS route | L43: "still allows no assessment at all to pass". L240: "never PASS" | Keeps PASS when n1 = n2 = n3 = n4b = 0. That case is reachable: with R = 200 and rows 0/4/5 only, if n4+n5 < 36 the denominator is short because of row-0 replicates | **Conflict.** Delete the PASS branch: NOT ASSESSED is always UNRESOLVED |
| Label for insufficient support | L47–L48: "UNRESOLVED, blocking that check's PASS." FAIL is reserved for a violated assessed criterion (L50–L51) or a licence without a valid computed label (L53–L54) | "the row FAILS" | **Conflict, needs relabelling.** It is stricter in effect but uses the wrong label. FAIL asserts a measured violation that did not occur |
| BOUNDARY vs UNRESOLVED | L27–L31: BOUNDARY is a computed non-licence in the denominator; UNRESOLVED is reported separately | One count, n4b, for "BOUNDARY/UNRESOLVED" | **Needs a split:** n4b-B and n4b-U, with literal FL = n5/(n4 + n4b-B + n5), the conservative screen and the diagnostic n5/(n4+n5) defined separately (L33, L37) |
| Conservative denominator and ≥36 | L41: "the conservative denominator is n4+n4b+n5. The >=36 rule concerns that assessment's denominator" | E2-3: ≥36 on n4+n4b+n5 | **Consistent**; after the split, state which n4b the screen counts |
| Binding conservative screen | L35: point ≤ 0.05 and CP upper ≤ 0.08; L37: "combined specificity/informativeness screen"; L39: "A separate arbitrary cap is unnecessary." | Not addressed | **Gap:** make FL_wc binding under that name. Add no row-4b cap |
| Realization naming | L17: "Call this quantity plant realization; do not silently reuse the earlier meaning of real_i times instrument eligibility." L19–L25: three separate conditions | Uses rows 1/3 credit without renaming | **Needs renaming:** "plant realization" (E5) for rows 1 and 3, kept separate from "assessment availability" and "false-licence performance"; Σ real_i·elig_i is not reused |
| Row 0 | L41: "Row-0 licences remain immediate failures." | Row 0 = construction failure | **Consistent** |
| Pre-execution inapplicability | L58: needs "an applicable construction-level proof. Population rho_E = 0 is not a proof…" | C3 L32 lists narrowing as an open question | **Consistent**; any narrowing needs a construction-level proof |

Suggested replacement wording, for CNA to adopt or amend:
> "If a required operating-characteristic check has insufficient support (assessable denominator n4 + n4b-B + n5 < 36, for any mix of rows 1, 2, 3 or 4b-U), the check is UNRESOLVED and cannot PASS. FAIL is reserved for an assessed criterion violated or a licence without a valid computed label."

---

## 5. Conflicts and errors raised

1. **LIM OUT vs fitted G-i** (§1.3). V25 L174's own condition puts LIM IN under any estimated s\*. Lead decision: OUT as a confirmation-only required check, or IN at 15/20 (figures in §1.4).
2. **MP L80 label** (§1.2): UNAVAILABLE vs INCOMPLETE for a quota shortfall. RD proposes INCOMPLETE.
3. **corr3** (§4): the PASS branch, the FAIL vs UNRESOLVED label, the BOUNDARY split and the realization renaming.
4. **k convention** (§2.2): ⌈0.99·n_q⌉ (Astra's 990) gives expected coverage 90/91 < 0.99. ⌈0.99·(n_q+1)⌉ gives ≥ 0.99. Lead to confirm.
5. **Still open, not invented here:** n_c, n_q, the s grids, the LIM offsets, the Var floor and the new-role KATs.

No errors found in the verified inputs' hashes or footers. Astra's A50 L130 figure and the 13/20 totals reproduce exactly.

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: c29401c458a408ebd73a93f94c89a91f3a6da2f6464bbee84b1724a95fbc3520
