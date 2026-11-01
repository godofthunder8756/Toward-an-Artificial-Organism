# Track B v3.6 freeze prep: CNA E50-1 / E50-3 file, ADDENDUM 1 — Lead rulings recorded (corr3 superseded; LIM IN; quota shortfall INCOMPLETE; quantile rank) (CNA v1)

**Author:** CNA. **Written:** 2026-11-01, about 12:16–12:20 PM ET.
**STATUS: PLANNING/AUDIT RECORD. DRAFT, NOT FROZEN.**
- Additive, by supersession only. It amends **review/trackB_scope_v3_6_CNA_E50_1_E50_3_v1.md** (whole-file sha256 b5a880ea35a77ae2de47dfd8d9bb2516d9e9b331f96c52ded8e123c780939f97, footer 1ebe8c5d4aec7027f97be89a01049fc7b9441d5dddeeea50aafa8b7fc4ba5a2f, 207 lines; "CE50 Ln").
- CE50 was already chmod 444 when the rulings arrived, so under the binding no-rewrite rule (E2 L6) they are recorded here and CE50 is not edited.
- Rulings were relayed by the Lead at 12:15 PM ET.
- Nothing was run or timed; the only computation was exact integer/rational arithmetic and SHA-256. X1–X5 and the claim ceiling are unchanged. No consciousness claim. Astra was not contacted.

## R1. E50-1 SUPERSEDES corr3 (review/trackB_freezeprep_v2_5_erratum2_corr3_Lead.md, 2f813ba4bb58507241ced0bea97354fdfc63990015786feaadeb4709e4630eec) — RULED by the Lead
C3 §1 ("NOT ASSESSED passes only when n1 = n2 = n3 = n4b = 0; otherwise the row FAILS") is **superseded** by CE50 §1.2–§1.4:
1. **NOT ASSESSED / insufficient support → UNRESOLVED, never PASS** (CE50 §1.4 step 4; A50 L47–L48, L56).
   - It is not FAIL on that ground alone.
   - FAIL is reserved for an assessed violation of the binding screen and for a licence without a valid computed label (A50 L50–L54).
2. **BOUNDARY / UNRESOLVED split:** row 4b is replaced by **4B (BOUNDARY, a computed non-licence)** and **4U (UNRESOLVED, an unavailable assessment)** (CE50 §1.2; A50 L27–L31).
3. **Binding conservative screen:** S_cons = (n5 + n4B + n4U)/(n4 + n4B + n4U + n5) must meet point ≤ 0.05 **and** one-sided 95% CP upper ≤ 0.08 (CE50 §1.3; A50 L35).
   - Its n_cons ≥ 36 sets assessment availability.
   - The 4b-share cap is withdrawn (A50 L39).
4. **Rows 1 and 3: the E5-only credit is renamed "plant realization"** (pr_i; PR = Σ pr_i/200 ≥ 188/200). It no longer reuses real_i·elig_i (CE50 §1.1; A50 L15–L17).
   - Row 2 (N) keeps pr_i = 0 (A49 L141).

**C3's anti-loophole intent stands.** Neither UNRESOLVED nor BOUNDARY is a licence, and neither can lead to PASS:
- BOUNDARY and UNRESOLVED are adverse events in the binding screen;
- insufficient support blocks PASS whatever its source (rows 1, 2, 3 or 4U).

Hedging to BOUNDARY/UNRESOLVED, or driving replicates into rows 1–3, therefore cannot produce a PASS. It can only produce FAIL (via the screen) or UNRESOLVED.

C3's recorded cost now reads: "a row whose all-undefined cells are frequent by design is UNRESOLVED on that alone". C3 §1's open narrowing question is closed by A50 L56–L58 (CE50 §1.5).

**CE50 §3 L-1 status: RULED (adopted).** L-2…L-8 remain recommendations pending Lead ruling.

## R2. IGN-LIM is IN calibration — RULED by the Lead (supersedes V25 R5 "LIM OUT, conditional" and CD0 §A4's OUT reading)
- LIM's 2 cells join C_cal: **|C_cal| = 15** (13 + LIM 2).
- Its limitation behavior is a required check that must not become "untested" (A50 L97). This answers E50-2's limitation-validation path for LIM by full calibration membership.
- The transition-location rule (A50 L90–L95) stays an E50-2 item.
- **C_conf is unchanged at 20 cells.** LIM's 2 confirmation cells were already counted; NC2r 1 + dose-0 4 + 15.
- **Arithmetic only (cost is the Lead's E50-5 item; for the Lead's recost).** T = 267,004,800·15 + (1,828,800·15 + 914,400·20)·n = **4,005,072,000 + 45,720,000·n** trials:
  - **7,068,312,000** at n = 67;
  - **4,416,552,000** at n = 9.
  - Previously: 3,471,062,400 + 42,062,400·n.

## R3. Quota shortfall → INCOMPLETE — RULED by the Lead
- A per-(seed, required bin) final-partition quota shortfall (fewer than 100 eligible of 127) makes **that replicate INCOMPLETE**. M L2009: "bin shortfall → that replicate is INCOMPLETE".
- It is not a trial-level exclusion and not a top-up; the replicate stays in the 200.
- **Mapping to the CE50 truth table:** an INCOMPLETE replicate is classed with row 0. Its pr_i = 0, and it enters no literal-FL or S_cons count.
  - A licence in it is a licence without a valid computed label → row **FAIL** (CE50 §1.4 step 1).
  - Its count is reported under its own reason code (quota shortfall), separate from other row-0 causes.
  - This mapping is a CNA reading of the ruling; the Lead may confirm.

## R4. Network tolerance rank — RULED by the Lead (E50-4 input; CNA records only)
- **k = ⌈0.99·(n_q + 1)⌉**, where n_q is the number of independent null runs used for threshold estimation. The threshold is the k-th ordered distance, with the fixed tie rule still to be pinned (E50-4).
- **Exact check at Astra's example n_q = 1,000 (exact rationals):**
  - k = ⌈990.99⌉ = **991**, one rank above Astra's 990th (A50 L125).
  - Conditional on the fixed centre and a continuous distance distribution, P(coverage < 0.97) = P[Bin(1000, 0.97) ≥ k]:
    - **5.660 × 10⁻⁶ at k = 991** (ruled rule);
    - 1.813 × 10⁻⁵ at k = 990 (A50 L130 reproduced).
  - The ruled rank is the more conservative of the two.
- It is a per-threshold statement, not simultaneous over the battery (A50 L132).
- **k ≤ n_q requires n_q ≥ 99.** Below that, the rule must be a construction failure. Proposed for E50-4 (owner per Lead).

## Status
| Item | Status |
|---|---|
| CE50 L-1 (corr3 superseded by E50-1) | **RULED** (R1) |
| LIM calibration membership | **RULED IN**; \|C_cal\| = 15 (R2) |
| Quota shortfall | **RULED INCOMPLETE** (M L2009); the row-0 mapping is a CNA reading (R3) |
| Network rank k | **RULED** ⌈0.99(n_q + 1)⌉; tie rule and n_q ≥ 99 guard pending E50-4 (R4) |
| CE50 L-2 … L-8 | Pending Lead ruling |

*DRAFT. Planning only. Nothing was run or timed. X1–X5 and the claim ceiling unchanged. No consciousness claim.*
---
sha256 of all content above this line: 36a2ad78a43cd553a5b843fd9a94f990d1c7f9bed0773532f3b9288cfc2f9bc7
