# Track B freeze preparation v2.5: ERRATUM 2 (Lead) — Lead rulings E2-1..E2-9 on the v2.5 light passes

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** A new, additive file. It amends `review/trackB_freezeprep_v2_5_consolidated_Lead.md` ("V25 Ln"; `d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5`) and `review/trackB_freezeprep_v2_5_erratum1_Lead.md` ("ER1 Ln"; `10860e98444d31c0f432b44f44427b1a522add744d42dd65ce38e20c5c349c2a`) by supersession only; neither is edited. Nothing was run or timed; the only computation was SHA-256 and exact integer arithmetic (system `python3`).
- **Written:** 2026-11-01, about 11:54 AM–12:00 PM ET, by the Lead's executor. Lead rulings given in the "ACI Research" room, about 11:52–11:55 AM ET; E2-4 as amended by the Lead before filing.
- **Sources:** CNA light pass of V25/ER1/#50 v3 ("CLP"), RD erratum 1 to E49-2 ("RDE"), RD light pass of V25/ER1 ("RLP"); hashes in §4.
- **Binding file rule (Lead, from 11:53 AM ET):** once a file is chmod 444 it is **never rewritten in place**, even a draft; corrections go in a new versioned file beside it.

## 1. Lead rulings

**E2-1 Fisher–Yates bias figure (supersedes V25 L82's "exact maximum … 1.3878 × 10⁻¹⁷" and LP2 `6c02198c…` (a) on that figure).** The exact maximum relative deviation |m·P(idx = i) − 1| over all 507 swaps (m = 2…508) is **2.6455 × 10⁻¹⁷, at m = 504** (= 488/2^64; CLP L52). 1.3878 × 10⁻¹⁷ holds only at m = 508. The ruled bound **508/2^64 = 2.7539 × 10⁻¹⁷ stands**. Absolute deviation: the ruling records **5.42 × 10⁻²⁰** (CLP L53). *Executor recomputation (exact integers, this pass):* the maximum of max(r, m − r)/(m·2^64), r = 2^64 mod m, is **5.4210e-20 at m = 256**; 5.42 × 10⁻²⁰ equals 2^−64 (= 5.4210 × 10⁻²⁰), which is the strict upper bound rather than the attained maximum. Both are < 2^−64; no conclusion changes. Flagged for CNA to confirm which figure the frozen text carries.

**E2-2 IGN-N1 x_lo (supersedes ER1 L24's "x\* = tanh(g·x\* + b)").** The symbol "b" is **WITHDRAWN**. It is replaced by the row's null-input s: x\* is the **unique stable fixed point of f(x) = −x + tanh(g·x + s) at null input** (x\* = 0 at s = 0), computed by the same rule (fixed-point iteration from x = 0 until |Δx| < 1e-12 in float64 under the pinned libm, frozen as a constant per dose). For g < 1 the map is a contraction, so the fixed point is unique and the iteration converges. Rows with g > 1 keep the existing lower-branch definition. **g = 1 is EXCLUDED from every dose grid.** (RLP V-6.)

**E2-3 Worst-case FL rate assessability (adds to ER1 E1 (i)).** FL_wc = (n_5 + n_4b)/(n_4 + n_4b + n_5). Its ≥ 36 assessability check counts **n_4 + n_4b + n_5**. Row-0 licences are **not** part of FL_wc; they remain a separate row-level FAIL (V25 L56). (CLP 2.3; RLP V-4.) Whether FL_wc must meet the 0.08 CP criterion stays asked in #50 Q1.

**E2-4 Row-4b loophole and other non-counting replicates (supersedes V25 L56 for these cases; PROVISIONAL, #50 Q1).** CNA's wording, adopted: **"If the false-licence check is NOT ASSESSED and n4b > 0, the row FAILS. NOT ASSESSED passes only when n4b = 0."** Reason (RLP item 10): under V25 L56, pushing replicates into 4b until the FL denominator falls below 36 was a route **to** PASS.
- **Provisional extension (Lead):** the same rule applies to **all-undefined (all-D) replicates and too-few-qualified-seed (Q-insufficient) replicates** — rows **1 and 3** of the V25 §1.1 table — **unless CNA shows they are fully plant-determined** (independent of the system-under-test's outputs). That is: **NOT ASSESSED passes only when no system-influenceable non-counting replicate exists.**
- **Scope PENDING CNA:** whether rows 1 and 3 are fully plant-determined (if so, they are exempt). *Label note:* the Lead's relayed text named all-undefined as "row 2"; in the V25 table all-D is **row 1** and row 2 is **N** (real_i = 0, ND cells exist, neither route holds). This erratum applies the rule by name (all-D, Q-insufficient). Whether N replicates are also system-influenceable non-counting replicates for this purpose is included in the PENDING CNA scope question.
- To Astra: #50 Q1.

**E2-5 Noise scale "per τ".** σ = 0.05·‖x_hi − x_lo‖ is the noise scale **per τ**; M L1126's "per unit time" is to be read, and merged, as **"per τ"**. (RLP V-1.)

**E2-6 Δt (supersedes the uncapped form in ER1 / V25 §0.2 item 3, §6.3).** **Δt = τ / (100·⌈max(1, g − 1)⌉).** This guarantees integer t_r/Δt for the plant t_r grid {2τ, 3τ, 5τ} for every g. CNA's admissibility bound Δt ≤ τ/(20·max(1, g − 1)) is still satisfied (⌈·⌉ ≥ its argument). Plant steps per trial = 5τ/Δt = **500·⌈max(1, g − 1)⌉** (500 for g ≤ 2; no V25 §8 figure changes). (RLP V-2.)

**E2-7 RAND-INIT dose 0 is a named DEVIATION.** Dropping RAND-INIT's dose-0 arm (R5; V25 §5) is a **prospective deviation from CNA2 L242** ("Each specificity row has … a dose-0 sanity level"). Reason: g_0 → 0 gives a **degenerate network** (no recurrence at init), not "confound off". Named as such in #50 Q3. (RLP V-3.)

**E2-8 DOSE0 encoding (adds to ER1 E3 item 2).** DOSE0 = 2^64 − 1 is packed as an **unsigned** 64-bit integer in the **same byte order as the other address fields** (big-endian, `>Q`): length prefix 00000008, bytes ff ff ff ff ff ff ff ff. Signed int64 packing (where 2^64 − 1 is −1) is banned. **A DOSE0 address KAT is required at freeze.** (RLP V-5.)

**E2-9 Wording (V25 L179).** Read: "With process noise, the end-of-settling state is Gaussian to first order, so its **distance from the median** is half-normal (1-D)". The **distance**, not the state, is half-normal. No figure changes. (RLP §5.)

## 2. Records
1. **ER1 E3 item 6 CLOSED.** RD's E49-2 erratum 1 (RDE, `c1bc0f0d9bdb22b976b3e56fd6862ffe7bc5f96ef981eb6674490f752b2186e5`) rescopes V2.5-RD L54 (independence: scalar plants have no settling period or tolerance; networks add the M L1129 tolerance) and L60 (trial-level eligibility), and adopts slot j = 0…507 (L76). It closes V25 §12 item 6 / ER1 E3 item 6.
2. **Disclosed pre-post rewrites.** The Delegate and CNA disclosed that the following files were rewritten in place before being posted: **d5ee9a1b…** (RD cost light pass), **a44ff0d6…** (RD light pass of CE49), and the Lead executor's own **7cc789a8…** (ER1 draft, replaced by `10860e98…` before any send; copy at scratch/lead_v25/erratum1_draft_7cc789a8_superseded.md). The posted hashes are the governing ones; under the binding rule above, no 444 file will be rewritten in place again.
3. **Non-blocking notes.** (a) Several file headers state write times later than the files' mtimes (CD0, CE49a1 per LP2; also noted in CLP/RLP); not corrected in place. (b) In the #50 packet the R-items were listed out of numeric order (R1, R2, R5, R6, R7, R4); v4 lists them in order.

## 3. Status updates
| Item | Status |
|---|---|
| V25 §12 item 6 / ER1 E3 item 6 | CLOSED by RDE |
| ER1 E3 item 7 (IGN-N1 x_lo) | RESOLVED as amended by E2-2 |
| ER1 E3 item 2 (DOSE0) | RESOLVED as amended by E2-8; DOSE0 KAT required at freeze (new pre-freeze item) |
| E2-4 rows 1/3 (and N) scope | **PENDING CNA**; rule PROVISIONAL pending #50 Q1 |
| Row-4b maximum share value | PENDING (ER1 E1 (ii)) |
| E2-1 absolute-deviation figure (5.42e-20 vs 5.40e-20) | CNA to confirm |

## 4. Inputs (whole-file sha256 and footer recomputed this pass; all MATCH)
| Abbrev | Path | Whole-file sha256 | Footer |
|---|---|---|---|
| V25 | `review/trackB_freezeprep_v2_5_consolidated_Lead.md` | `d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5` | `36dbcb5f…` ✔ |
| ERR1 | `review/trackB_freezeprep_v2_5_erratum1_Lead.md` | `10860e98444d31c0f432b44f44427b1a522add744d42dd65ce38e20c5c349c2a` | `4d51b00c…` ✔ |
| CLP | `review/trackB_freezeprep_v2_5_CNA_lightpass_v1.md` | `59eb019bfa777d4f598a2cd67e9803a67f36b6593cb2f2813584451eaa8aefc8` | `3d98f1af…` ✔ |
| RDE | `review/trackB_freezeprep_v2_5_E49_2_erratum1_RD.md` | `c1bc0f0d9bdb22b976b3e56fd6862ffe7bc5f96ef981eb6674490f752b2186e5` | `5eabfcec…` ✔ |
| RLP | `review/trackB_freezeprep_v2_5_consolidated_lightpass_RD_v1.md` | `70a0bfff934ab46907a9224d27eee3a313b8849ca292bbd704d4ef98c3413c02` | `9645b1be…` ✔ |
| LP2 | `review/trackB_scope_v3_6_CNA_dose0_xref_and_E49_addendum1_lightpass_RD_v1.md` | `6c02198c2fe6b612272a7a5d0731ffa55ae4deff699fa8353853c00063bd25cc` | `f7d751d2…` ✔ |

*DESIGN ONLY. Draft, not frozen. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No host coupling. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: c62a3bbf8419a1c205be268380fd6e0cc7ce6aa92060d7efbbded2439dccae79
