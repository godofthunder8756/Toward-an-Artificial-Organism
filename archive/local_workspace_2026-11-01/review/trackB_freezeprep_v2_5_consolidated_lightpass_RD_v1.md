# Track B freeze prep v2.5: RD light pass of the Lead's consolidated v2.5 and Lead erratum 1 (RD v1)

**Author:** Research Delegate (RD). **Written:** 2026-11-01 11:51 ET (box `date`: 2026-11-01 11:51 EST). **STATUS: DESIGN/TEXT ONLY. DRAFT, NOT FROZEN.** Additive; no other file is edited. Nothing run or timed. Computation: exact integer/rational arithmetic (`fractions`), SHA-256, and the integer Philox checks already filed in RDL/LP2, all in pure Python on the system `python3`. X1–X5 and the claim ceiling unchanged. No consciousness claim.
**Lane:** code paths, RNG, counters, stop/exit (close); the rest light. "V25 Ln" = review/trackB_freezeprep_v2_5_consolidated_Lead.md; "ER1 Ln" = review/trackB_freezeprep_v2_5_erratum1_Lead.md; "CE49", "CE49a1", "RDL", "LP2" as in V25 L6.
**Footer convention:** as in the project files: the footer is the sha256 of every byte of this file above the footer line, from the first byte through the newline ending the "Footer convention:" line just above it.

## 0. Hashes (recomputed)
- V25: whole-file `d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5` MATCH; footer `36dbcb5f48c7e21ab572af6da5cce63548f54f4b30403955f6d5fb9d8631e0c0` MATCH (its own stated convention, which includes its "Footer convention:" line).
- ER1: whole-file `10860e98444d31c0f432b44f44427b1a522add744d42dd65ce38e20c5c349c2a` MATCH; footer `4d51b00cdb17a4bc86b2dc0863a8264113c7e38d9cdf1ae706382f8294249511` MATCH.
- **Header times (minor):** V25 L5 "about 11:37 AM–12:10 PM ET" and ER1 L4 "about 11:50–11:58 AM ET" extend past the files' mtimes (11:43 and 11:48 ET). Same class as LP2 item 6.

## Verdicts
| # | Item | Verdict |
|---|---|---|
| 1 | Fisher–Yates pin and slot mapping (V25 §2.2, §3.1, §3.3) | CONFORMS |
| 2 | Address v2 fields; counter (t, s, 0, 0) and ban list (V25 §3.1–§3.2, §2.6) | CONFORMS |
| 3 | Noise convention and Euler–Maruyama step (V25 §0.2, §6.3) | CONFORMS WITH EDITS |
| 4 | Δt = τ/(100·max(1, g − 1)), τ/20 admissibility (V25 §6.3, §6.4) | CONFORMS WITH EDITS |
| 5 | IGN-P1 t_s = 0, x_ref = x_lo; M L1129 networks only (V25 §6.1, §2.3) | CONFORMS (RD's E49-2 erratum filed) |
| 6 | 0.99-quantile network tolerance, provisional (V25 §6.2) | CONFORMS |
| 7 | Dose 0: four rows, RAND-INIT dropped, confirmation-only (V25 §5) | CONFORMS WITH EDITS |
| 8 | NC2r OUT; LIM OUT with a fixed grid bound (V25 §5) | CONFORMS |
| 9 | Full grid, early stop only as #50 Q2 (V25 §4) | CONFORMS |
| 10 | Row 4b and hedging (V25 §1; V25 L67–L68 superseded by ER1 E1) | CONFORMS WITH EDITS |
| 11 | M L1966 strike; Philox 7/10-round labels; CNA2 L258; MP gate units | CONFORMS |
| 12 | No stop/truncation/schedule quantity in any input; X1–X5 intact | CONFORMS |
| 13 | Recost (exact) and CPU-h arithmetic (UNVERIFIED) (V25 §8) | CONFORMS |
| 14 | ER1: FL_wc formula, DOSE0, IGN-N1 x_lo, Hoeffding, E2 | CONFORMS WITH EDITS |

## 1. Fisher–Yates: CONFORMS
V25 L81: k = 507…1, one block under `ign-partition` at (508 − k, 0, 0, 0), idx = w0 mod (k + 1) unsigned 64-bit, w1–w3 discarded, exactly 507 draws, no rejection/retry. L82: relative bound |m·P − 1| < 508/2^64 = 2.7539 × 10⁻¹⁷, exact max 1.3878 × 10⁻¹⁷, absolute ≤ 2.73 × 10⁻²⁰ (matches LP2 (a)). L84 and D54/D55: float form, contiguous ranges, any rejection sampler banned. L81/L83: positions 0–253 fitting, 254–380 selection, 381–507 final; value a[p] is slot j. Registry row L124: c0 = 508 − k ∈ {1…507}, s = 0, w0 only. KAT L134 equals the one RD reproduced in LP2 (fa85f551…) ✓.

## 2. Address and counter: CONFORMS
V25 L129 field order (domain; master seed; replicate set; generator; row; dose index; n_grid; replicate; partition; seed; role; suffix), 4-byte big-endian length prefixes, SHA-256, k0/k1 little-endian: identical to CE49 §4.2 ✓. L105 carries A49 L77/L143 fields plus generator, replicate set, n_grid ✓. L115: (t, s, 0, 0), nonzero c2/c3 and out-of-range s are construction failures; t = absolute root-episode step inherited by continuations; A49 L118 ban verbatim ✓; L105 imports the full V2.5-RD L80 ban list (branch/donor/call-order/draw-count/continuation-relative counters, wall clock, process/thread/worker/completion order) ✓. Registry L120–L124 consistent with CE49a1 (rewcorr-eta one η_k per (t, k) block, w2/w3 discarded) ✓.

## 3. Noise convention: CONFORMS WITH EDITS
τ·dx = f·dt + σ√τ·dW gives dx = (f/τ)dt + (σ/√τ)dW, so one Euler–Maruyama step is Δx = (Δt/τ)·f + σ·√(Δt/τ)·ξ ✓ (V25 L191). Noise variance accumulated over one τ is σ², so σ is the per-τ scale ✓. One normal per step from `ign-trial` at (t, 0, 0, 0), w0/w1 Box–Muller ✓ (L123). MP L84 placement superseded (D60, #50 Q4) ✓.
- **Edit V-1:** M L1126 says "N(0, (0.05·‖x_hi − x_lo‖)²) per unit **time**"; V25 L190 reads σ as "per-unit-τ". These agree only if the time unit is τ. The merge text for M L1126 should say "per τ" explicitly.

## 4. Δt: CONFORMS WITH EDITS
Δt = τ/(100·max(1, g − 1)) satisfies Δt ≤ τ/(20·max(1, g − 1)) by exactly 5× for every g ✓. N = 5τ/Δt = 500·max(1, g − 1) ✓.
- **Edit V-2 (code path):** V25 L193 says every t_r is an integer multiple of Δt "(true for the grid below)". t_r/Δt = 100·max(1, g − 1)·{2, 3, 5}. That is an integer for g ≤ 2, but **not for general g > 2** (exact: g = 2.5 gives 300, 450, 750, fine; g = 2.337 gives 267.4, 401.1, 668.5; g = 3.0001 gives 400.02, …). Pin either "g − 1 is a multiple of 0.01 when g > 2", or Δt = τ/(100·⌈max(1, g − 1)⌉) (still admissible), so N_steps and the readout step are integers.

## 5. IGN-P1 settling: CONFORMS
V25 L180–L182 (M L1127 replacement with the CNA2 L258 cite; M L1129 "Network instruments only."; M L314 unchanged) and L88 match R6. **RD's E49-2 erratum is filed:** review/trackB_freezeprep_v2_5_E49_2_erratum1_RD.md (rescopes V2.5-RD L54 independence and L60 eligibility; adopts slot j = 0…507). That closes ER1 E3 item 6 / V25 §12 item 6.
- Wording slip (no verdict impact): V25 L179 "the end-of-settling state is half-normal about its median" should read "the end-of-settling state is Gaussian, so its distance from the median is half-normal".

## 6. Network tolerance: CONFORMS
0.99 quantile of ‖x_ref − median x_ref‖ on fitting-partition null-input runs, chosen without w, provisional, #50 Q4; Reading I/II tables match LP2 (f) ✓; null-run count ABSENT (O9) ✓.

## 7. Dose 0: CONFORMS WITH EDITS
Four rows (NC1, NC2, BOTTLENECK-ONLY, Architecture-imposed); confirmation-only at R_rep = 200 and the frozen n_seed, 914,400·n_seed each; never calibration or 3a; never blocks/passes ✓ (V25 L172). Cell counts check: C_cal = 6 scalar + 7 network = 13; C_conf = 13 + 1 + 2 + 4 = 20 (11 scalar, 9 network) ✓.
- **Edit V-3:** CNA2 L242 attaches a dose-0 level to "**Each** specificity row", and RAND-INIT is one (CNA2 L189). Dropping it is a prospective deviation from that text, not just a parameter choice; name it as such in #50 Q3 (currently Q3 asks only about dose-0 values and LIM).

## 8. NC2r / LIM: CONFORMS
NC2r OUT, REPORTED, cannot become required without re-entering C_cal (L173). LIM OUT only under a fixed, pre-registered, n_seed-independent s* grid bound; otherwise IN (L174) ✓.

## 9. Full grid: CONFORMS
M L2784 quote verbatim; A44 L108 quote verbatim; 267,004,800 per calibration cell; early stop not adopted (D56); #50 Q2 includes CNA's three conditions and the diagnostic point with a pre-stated false-fail rate ✓.

## 10. Row 4b and hedging: CONFORMS WITH EDITS
Table L45–L51 matches CE49 + CE49a1 (rows 0–5 with 4b; 4b real_i from E5 only, outside FL denominator and the 36 count) ✓; 188/200 and the 36/58/77/95/112/129 figures ✓. **Confirmed: V25 L67–L68 are wrong on the hedging safeguards.** L67 (b) treats exclusion from the ≥ 36 count as a safeguard, but under L56 "NOT ASSESSED" leads to PASS, so pushing replicates into 4b until the denominator falls below 36 is a route **to** PASS, not a guard. L68 "no position is taken" is superseded by ER1 E1. See item 14.

## 11. Housekeeping: CONFORMS
M L1966 struck, M L1963 tagged (L154, D57) ✓. KV L38–L40 = 7 rounds, L41–L43 = 10 rounds (L132) ✓. CNA2 L258 used (L179–L180, §12 3a) ✓. MP gate units G-i/G-ii/G-iii (L95–L97) = CE49a1 E-RD-7 ✓. False-MET cite M L1965 ✓.

## 12. Stop/exit and safety: CONFORMS
No key field, counter word or input carries a stop, truncation, horizon-end, cap or schedule quantity; the kernel freeze text (L141) carries the M L280 clause; B/B_I uses in-world termination only and "No evaluation episode carries a scheduled stop" (L144); a registered `stop` role may feed only the scheduler (L126). The Fisher–Yates draw reads only schedule fields and k. X1–X5, claim ceiling and #42 L223 stated intact (L7, L354) ✓. Runs/benchmarks need Aidan's explicit yes (L14) ✓.

## 13. Recost: CONFORMS (all recomputed exactly)
- 13 × 267,004,800 = **3,471,062,400** ✓. n-term 13 × 1,828,800 + 16 × 914,400 + 4 × 914,400 = 23,774,400 + 14,630,400 + 3,657,600 = **42,062,400** ✓ (= 20 × 914,400 confirmation + 13 × 1,828,800 step 3a).
- Totals: n = 67 → **6,289,243,200**; n = 9 → **3,849,624,000** ✓. Scalar/network split 3,011,119,200 + 3,278,124,000 and 1,791,309,600 + 2,058,314,400 sum to the totals ✓ (both n-coefficients are 21,031,200 ✓).
- Calibration/confirmation ledgers: 5,063,947,200 / 1,225,296,000 (67); 3,685,032,000 / 164,592,000 (9) ✓. Whole-procedure share 0.80518 → **80.5%**, 0.95724 → **95.7%** ✓. Per-C_cal-cell 450,799,200 / 291,693,600, shares 86.4% / 97.2% ✓.
- Seed-units U = 1,375,600 / 842,000; dip tests 5,502,400 / 3,368,000 ✓.
- **CPU-h (UNVERIFIED; arithmetic only):** scalar trials 83.6 / 12,546.3 (67) and 49.8 / 7,463.8 (9) ✓; fits 137.6 / 4,126.8 and 84.2 / 2,526.0 ✓; network at d_h = 256 (3.670016 ms/trial) 3,341.9 (67) ✓ and 2,098.35 (9; V25 prints 2,098.4, RD gets 2,098.346, a rounding difference); d_h = 64/512: 208.9/13,367.5 ✓ and 131.15/8,393.4 (V25 131.2; exact 131.147, rounds to 131.1). Totals ≈ 3,563 / 20,015 / 2,232 / 12,088 ✓. The two last-digit roundings are immaterial; the figures stay UNVERIFIED, as V25 says.

## 14. Lead erratum 1: CONFORMS WITH EDITS
**FL_wc (ER1 L9).** Row numbering per CE49 §1 (L42–L43) and CE49a1 §2 (L36, L41): **row 4 = Q-labelled, label NOT MET; row 4b = Q-labelled, BOUNDARY or UNRESOLVED; row 5 = Q-labelled, label MET.** In the GA-1 control every MET is a false licence, so n_5 is the would-be-false-licence count. FL_wc = (n_5 + n_4b)/(n_4 + n_4b + n_5): the numerator is every MET plus every 4b ✓; the denominator is the primary FL denominator (n_4 + n_5, CE49 L42–L43 "denominator +1" for rows 4 and 5) plus n_4b ✓. FL_wc ≥ primary FL whenever n_5 ≤ n_4 + n_5 (always), so it bounds the hedge from above ✓. Safeguard (ii)'s share uses the same base (rows 4 + 4b + 5) ✓.
- **Edit V-4:** if #50 makes FL_wc gate on the 0.08 CP criterion, state its assessability rule (does ≥ 36 apply to n_4 + n_4b + n_5?) and its value when n_4 + n_5 = 0 but n_4b > 0 (FL_wc = 1, primary undefined).
**DOSE0 = 2^64 − 1 (ER1 L25).** The dose field is a u64, length-prefixed 8 bytes (CE49 §4.2), so 18446744073709551615 encodes as 00000008 ff ff ff ff ff ff ff ff ✓ (checked). Real dose ordinals are 0-based and at most 2 (3 doses), so there is no collision; the encoding stays injective ✓. Dose index 0 = first required dose ✓.
- **Edit V-5 (code path):** require an **unsigned** 64-bit pack (e.g. `>Q`); in signed int64 (numpy int64, Java long) 2^64 − 1 is −1 and may be rejected or mis-encoded. Add a DOSE0 address KAT at freeze.
**IGN-N1 x_lo (ER1 L24).** For g < 1, tanh(g·x + b) is a contraction (slope ≤ g < 1), so the fixed point is unique and the iteration converges ✓.
- **Edit V-6:** "b" is undefined; the plant drift uses s (V25 L190). Write x* = tanh(g·x* + s_null) and name s_null. "g ≥ 1 keep the lower-branch definition" leaves g = 1 (no separate lower branch) unspecified; use g > 1 for bistable plants and g ≤ 1 for the fixed-point rule, or state g = 1 is excluded.
**Hoeffding 27(3), p. 718 UNVERIFIED (ER1 L26)** ✓ (agrees with CE49 L84). **E2** 3/8–5/8 ✓.

## Edits summary
V-1 M L1126 "per τ"; V-2 Δt integrality for g > 2; V-3 RAND-INIT dose-0 drop named as a deviation in #50 Q3; V-4 FL_wc assessability and the n_4 + n_5 = 0 case; V-5 DOSE0 unsigned pack + KAT; V-6 x_lo symbol and g = 1 boundary; plus header times and the L179 wording slip. No DOES NOT CONFORM item; no hash mismatch.

*DRAFT. Design/text only. No freeze or execution is authorized (A49 L147).*
---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 9645b1becb2941a298af4da37caf8b12ba7acdd9f20898619ca01d77c1e68f9f
