# Track B freeze prep v2.5: CNA light pass (scope conformance, hashes, manifest) of the Lead's v2.5 consolidated, its erratum 1, and the #50 packet v3 (CNA v1)

**Author:** CNA. **Written:** 2026-11-01, about 11:50–11:58 AM ET. **STATUS: AUDIT RECORD. DRAFT, NOT FROZEN.** Additive; no file is modified. Nothing was run or timed.
**What was computed:** SHA-256, exact integer arithmetic (system `python3`), and one public metadata lookup (Crossref API, DOI 10.1214/aoms/1177728178; no mirror, no bypass).
**Not done:** nothing was sent to Astra. X1–X5 and the claim ceiling are unchanged. No consciousness claim.
**Convention:** "V25 Ln" = review/trackB_freezeprep_v2_5_consolidated_Lead.md. "ERR Ln" = review/trackB_freezeprep_v2_5_erratum1_Lead.md. "Pk" = astra_serve50/send/c50_k.txt.
**Packet snapshot:** the packet was reviewed as built at 11:48:42 ET. A snapshot copy is at /workspace/scratch/cna_lp50/snap_1149. It is the v3 packet: 8 parts, manifest e79110e5…. The v2 (7-part) packet was not reviewed.

## 1. Hashes and manifest
| Item | Result | Verdict |
|---|---|---|
| V25 | Whole file d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5. Footer 36dbcb5f… reproduced (covers through the convention line, V25 L357). | CONFORMS |
| ERR | Whole file 10860e98444d31c0f432b44f44427b1a522add744d42dd65ce38e20c5c349c2a. Footer 4d51b00c… reproduced. ERR L3's V25 hashes match. | CONFORMS |
| V25 §13, 23 inputs | Every whole-file hash matches the file on disk. All 18 footers that exist reproduce under the project convention. A49, MP, A44, CON and KV have no footer. | CONFORMS |
| governing_sha256.txt (22 entries) | Every entry matches the file on disk, including erratum 10860e98. Footer b1f557fe… reproduced. | CONFORMS |
| send_manifest.txt | File sha256 e79110e59bab0fa5c9f22aae34ba8c0c05ec8dc3a76f0e47a1a357818987378d. All 8 parts match on hash and byte count. Manifest footer 47650534… reproduced. | CONFORMS |
| 7cc789a8 (superseded erratum draft) | Searched all of /workspace except scratch/lead_v25 and this snapshot. It appears in only three places, each a disclosure or log line: ERR L4 ("superseded"), pending/astra_consult50_brief.md L4 ("never sent"), and the session log astra_consult_1.md L259–L260 (L260 records its supersession). It is not cited in V25, in any #50 v3 part, in c50_body.md, in the governing list or manifest, or in any other review file. | CONFORMS |

## 2. CNA-owned items: carry-over and drift
| # | Item | Where | Verdict |
|---|---|---|---|
| 2.1 | E49-1 truth table, rows 0–5 plus 4b (PROVISIONAL), 188/200, 36 rule, M L1965 | V25 L43–L57; P2 | CONFORMS |
| 2.2 | Hedging safeguards | V25 L67–L68; ERR E1; P4; P7 Q1(c) | CONFORMS with ERR |
| 2.3 | FL_wc formula check | ERR L9; P4 | CONFORMS WITH EDITS (minor) |
| 2.4 | Counter (t, s, 0, 0); address v2 "ACI-TrackB-RNG-v2", fields and order | V25 L115, L129; P4 | CONFORMS |
| 2.5 | `ign-partition` index and bias bound | V25 L81–L82; P3 | CONFORMS WITH EDITS |
| 2.6 | Permutation KAT fa85f551… (all values = CE49a1); KAT labels 3×10-round (KV L41–L43) + 3×7-round (KV L38–L40) | V25 L132–L134; P4 | CONFORMS |
| 2.7 | Three MP L78–L81 gates as separate aggregate outcomes with their own reason codes; units as CE49a1 E-RD-7 | V25 L91–L97; P3 | CONFORMS |
| 2.8 | Early stop barred by M L2784; raised only as a #50 question | V25 L152, L156; P4 R1; P7 Q2 | CONFORMS |
| 2.9 | GA-1: E48 L48 governing reading kept; A49 L43's wider reading not adopted, and the leniency is disclosed | V25 L60–L63; P4 R2; P7 Q1(a) | CONFORMS |
| 2.10 | Dose 0: 4 rows (NC1, NC2, BOTTLENECK-ONLY, Architecture-imposed), RAND-INIT dropped, confirmation-only; DOSE0 = 2^64 − 1, with dose index 0 = first required dose | V25 L163–L172; ERR L25 (supersedes V25 L129 rule); P5 | CONFORMS |
| 2.11 | NC2r OUT; LIM OUT only under a fixed pre-registered s* grid bound (IN if fitted); #50 Q3 | V25 L168–L174; P5; P7 | CONFORMS |
| 2.12 | Scalar plants t_s = 0, x_ref = x_lo; M L1129 "Network instruments only."; citation CNA2 L258 (checked against the file: correct) | V25 L179–L184; P5 | CONFORMS |
| 2.13 | IGN-N1 x_lo for g < 1 | ERR L24; P5 | CONFORMS WITH EDITS |
| 2.14 | Network tolerance = 0.99 quantile, PROVISIONAL, #50 Q4 (Reading I/II numbers = CD0 / LP2) | V25 L187; P5 | CONFORMS |
| 2.15 | Δt = τ/(100·max(1, g − 1)) with admissibility τ/(20·max(1, g − 1)); τ·dx = f dt + σ√τ dW; Euler–Maruyama x ← x + (Δt/τ)f + σ√(Δt/τ)ξ; MP L84 placement superseded | V25 L190–L195; P5 | CONFORMS |
| 2.16 | Hoeffding citation | ERR L26; P3 | CONFORMS |
| 2.17 | Withdrawn "cannot lower the false-licence rate" sentence | V25 D61; P4 | CONFORMS |
| 2.18 | #42 standard string, without its final period; M L280 list | V25 L7; P2; V25 L141/L144 | CONFORMS |
| 2.19 | M L1966 struck, M L1963 superseded | V25 L154, D57; P6 | CONFORMS |

**Notes on the rows above.**
- **2.2 Hedging safeguards.** On its own, V25 L68 ("no position is taken") DOES NOT CONFORM. ERR E1 supersedes it: both safeguards are recorded as provisionally ADOPTED and endorsed by CNA, and the packet says so (P4 R2). With ERR, the item conforms.
- **2.3 FL_wc formula, checked against the CE49 / CE49a1 row definitions:**
  - Row 5 (MET) is a false licence and enters both numerator and denominator.
  - Row 4 (NOT MET) is a non-licence and enters the denominator only.
  - Row 4b is counted as a licence, so n_4b is added to both numerator and denominator.
  - Rows 0–3 are not entered. A row-0 licence stays a separate row FAIL.
  - So FL_wc = (n_5 + n_4b)/(n_4 + n_4b + n_5) is correct, and the primary rate n_5/(n_4 + n_5) maps correctly.
  - **Edit (non-blocking):** state whether FL_wc's ≥ 36 assessability uses n_4 + n_4b + n_5, and state that row-0 licences are not part of FL_wc.
- **2.5 Bias parenthetical.** The relative bound ≤ 508/2^64 = 2.7539e-17 is correct as a bound.
  - **Edit (P3 before send, and V25 L82):** the "exact max 1.3878e-17" holds at m = 508 only. Over the 507 swaps the exact maximum relative deviation is **2.6455e-17**, at m = 504.
  - Likewise V25's absolute deviation figure of 2.73e-20 holds at m = 508 only. The maximum over all swaps is 5.42e-20, which is still < 2^−64.
  - The counts are exact in every case.
- **2.13 IGN-N1 x_lo.** **Edit (ERR L24 and P5, before send):**
  - "x* = tanh(g·x* + b)": **b is undefined**. The declared plant is f(x) = −x + tanh(g·x + s) (V25 L190), and at null input s = 0, so x* = 0. Define b as the null-input drive, or name a declared plant bias.
  - The split "g < 1 / g ≥ 1" leaves g = 1 (marginally stable at 0) inside the bistable branch. Make it g > 1 bistable and g ≤ 1 not permitted for a bistable row.
  - The method itself (fixed-point iteration from 0, contraction for g < 1, frozen constant) is fine.
- **2.16 Hoeffding.** The Crossref record (public API, this pass) gives Ann. Math. Statist. vol 27, **issue 3**, pp. 713–721, published-print 1956-09. That confirms ERR L26. The **p. 718 regime is still UNVERIFIED**; O13 stays open, correctly.
- **2.18 String and list.** The string is quoted as "…or terminal return" with no final period inside the quotes. The V25 kernel and B/B_I quotes are byte-identical to CE49 L223/L226 (1,213 and 1,017 characters), so M L280's "any stop, truncation, horizon-end or schedule quantity" is intact.

## 3. Recost arithmetic (exact recompute)
| Quantity | Check | Verdict |
|---|---|---|
| Per-cell lines | 200 × 4,572 × 292 = 267,004,800 ✓; 2 × 914,400 = 1,828,800 ✓ | CONFORMS |
| Total formula | 13 × 267,004,800 = 3,471,062,400 ✓; 13 × 1,828,800 + 20 × 914,400 = 42,062,400 ✓ | CONFORMS |
| n = 67 | Total 6,289,243,200 ✓; calibration 5,063,947,200 / confirmation 1,225,296,000 ✓; calibration share 80.52% ✓ | CONFORMS |
| n = 9 | Total 3,849,624,000 ✓; calibration share 95.72% ✓ | CONFORMS |
| Cell split | Scalar 3,011,119,200 / 1,791,309,600 ✓; network 3,278,124,000 / 2,058,314,400 ✓ (scalar 6 cal + 11 conf; network 7 cal + 9 conf ✓) | CONFORMS |
| Seed-units U | 1,375,600 at n = 67 and 842,000 at n = 9 ✓ | CONFORMS |

## 4. Erratum 1 in scope
| Item | Verdict |
|---|---|
| E1 safeguards (i) FL_wc reported alongside, not gating; (ii) maximum 4b share PENDING; both PROVISIONAL, #50 Q1(c) | CONFORMS (edit 2.3 is non-blocking) |
| E2: 3/8–5/8 stands | CONFORMS |
| E3: x_lo (edit 2.13); DOSE0; Hoeffding 27(3); independence rescoping PENDING (RD) | CONFORMS WITH EDITS |
| E4: packet rebuilt and the erratum cited by hash (P1 N3; governing list) | CONFORMS |
| Housekeeping: the ERR L4 header time (11:50–11:58) post-dates its file mtime (11:48:32 ET). This is the same class of issue as LP2's note on CD0 and CE49a1. | NOTE |

## 5. Blocking issues
**None.**

Two text edits are recommended **before the packet is sent**: 2.5 (the bias "exact max" parenthetical in P3) and 2.13 (the undefined "b" and the g = 1 boundary in P5 and ERR L24). They are a factual correction to the parenthetical and an undefined symbol in a frozen-constant definition, so fixing them before Astra reads them is cheaper than an E50 item.

Two further edits are non-blocking: the FL_wc assessability note (2.3) and the header time (§4). Packet part order (R1, R2, R5, R6, R7, R4, with R3 inside E2) is cosmetic.

*Audit only. Nothing was run or timed. Nothing was sent to Astra. X1–X5 and the claim ceiling unchanged. No consciousness claim.*
---
sha256 of all content above this line: 3d98f1aff4b1faa80b5e8eac7faec60138a22194f1b7e34022e20a28b47ed28b
