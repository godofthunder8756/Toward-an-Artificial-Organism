HEAD="""Consult #39 - PRE-FREEZE REVIEW of the C-kappa CLASS-FIT SYNTHETIC-ONLY SCOPE RECORD v1.2 + additive NOTE_1 (answers your #38 REVISE AND RESUBMIT, edits E38-1..16, raw sha 87fd77e0). Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

What is sent. The record under review is ckappa_classfit_synthetic_scope_record_v1_2.md (Research Delegate, sha256 79ea0eeb1658e7d265aae3a68d31c6fb385ceab23a91eb654fee61a4aa64561c), status DRAFT, NOT FROZEN, NOTHING RUNS, 94 KB. It is sent CONDENSED: sections 3-11 (every clause, label, SYS-* definition, derived expectation, outcome order, the full accounting table, the TO BE FIXED list and Q-R1..Q-R6) are sent essentially verbatim. Condensed [condensed]: the 31-entry change log (titles only), the source/hash table, the E37 and E38 compliance maps (the requirement->clause rows are kept, the verbatim E37/E38 quotes are dropped because they are your text, checked in-record as exact substrings of the raw), the 43 verbatim #38 body excerpts and the Q1-Q17 ruling table (your text; mapped in S11), and S12. NOTE_1 (sha 832d9bcf...) is sent in full. v1.1 (97165ac6) and v1.1 NOTE_1 (00ec1902) are unchanged and superseded. ASCII transliteration only (Greek spelled out, markdown dropped). Nothing has run; no checkpoint is opened.

=== RECORD v1.2 (condensed where marked) ===
"""
REC = R(1,26) + """
Change log relative to v1.1 + note 1 [condensed: 31 entries, titles only; each cites its #38 source]
Withdrawn: 1 Option A empirical NC floor (E38-1, L158). 2 v1 Option B per-class matched basis (L164, Q2a). 3 B-repaired (shared e), D2' and the dx/dy table (E38-1, Q2b). 4 Option C and its falsify-only text (L184). 5 all matched-basis / effective-basis-span material (L156; effective basis now stated as plain, C3.2). 6 v1.1 note 1 item 3 (NC2 vs NC3 functional-form framing; L186). 7 SYS-LIM under B-repaired (Q16). 8 inferred orbit masses and c2~0.100448 / c3~0.199056 (Q7, E38-11; now computed by package from exact law). 9 DERIVATION PREMISE vs IMPLEMENTATION attribution labels (Q5; stop kept).
Corrected: 10 D1 residual and SYS-PC local map (E38-2). 11 rank premises: full column rank for D2, D4, D5 and SYS-O6 class recovery; "for every resolved design" withdrawn; missing rank = EXPECTATION NOT APPLICABLE (RANK) (E38-3). 12 D3 wording (L85-96). 13 SYS-PC global cancellation = matrix recovery + finite prediction equality + per-cell loss equality (E38-4). 14 SYS-LIM: first-order qualifiers, exact failure statement, no impossibility, D7 diagnostic, exact-law midpoint (E38-2, E38-9). 15 SYS-FK alternatives: v1.1 impossibility claim withdrawn; register r = kappa_a and plateau construction acknowledged, neither added (E38-10). 16 P0 on exact rationals, on true chart, SYS-FK, admissible SYS-NC1 (E38-5). 17 extended B3 justified by D_mu Q2^T; stacking frozen (E38-6). 18 masks and identity domains C5.3, C7.0 (E38-7, E38-8). 19 system-level normalization (E38-11).
Fixed: 20 tolerances verbatim (Q9). 21 HEADROOM thresholds as synthetic conventions, H = L_mu,class (Q4, E38-12). 22 draw reuse with hashes, disclosed (Q10). 23 four sizes, 0.1 sole reference (Q12). 24 SYS-O6 inclusion, not a rerun (Q13). 25 A-vs-BCD midpoint (Q14). 26 SYS-PC rank lapse gives NOT MET (RANK) (Q15, E38-12). 27 SYS-LIM autonomy (Q17). 28 B1 extension (Q3, E38-8). 29 caps verbatim (E38-14).
Added: 30 execution-accounting table (E38-13), S8. 31 claim ceiling: E38-15 and the #38 L202 sentence verbatim (C1, C10).

0. Sources, hashes and precedence [condensed]
Governing raw files: #38 87fd77e0 (governs over everything, including this file and any summary of #38), #37 ce010fdb (below #38), #36 c8342d5a (inherited oracle definitions). Superseded: v1.1 97165ac6, v1.1 NOTE_1 00ec1902 (item 3 withdrawn). Inherited: governing set 6a5e0f24, B2/B3 ruling 6d75918f, v1_4_N closure note 4ad1d217 (B1, 595 s, N-b), v1_4_N 3f0c5c12, v1_3_E36 f6263fb8, oracle v1.1 e40c288f, results review 617e983d (M-1). PR #13 scratch @14376f38 read only (stages.py 936d3378, linalg_fit.py de6f4034, geometry.py 117e98e9, world.py 3d235fca, pinned.py 03c55323; outputs stage_O1.json 794746a7, stage_O7.json 994dda0a, results.json 6adb5de2, fit_freeze_O6.json b6f817c8, fit_freeze_O7.json 347bcd51).
"""+R(105,117)+R(118,119)+"""
[E38-15 verbatim here - your text.]
"""+R(124,132)+"""
2. Astra #37 items: compliance map (kept from v1.1) [condensed: E37 quotes dropped; checked as exact substrings of #37 raw]
"""+noquote(137,215)+"""
2b. Astra #38 items: compliance map [condensed: E38-1..16 quotes dropped (your text; exact substrings of raw sha 87fd77e0..ca2a5, re-checked in S12). Each requirement -> clause row is kept verbatim.]
"""+noquote(220,379)+"""
Other binding #38 body text [condensed]: the record quotes verbatim 43 excerpts of your raw text, at L5, 38, 46, 57, 69, 71, 73, 83, 94, 96, 118, 120, 124, 134, 138, 154, 156, 158, 160, 164, 183, 184, 186, 190, 192, 194, 196, 198, 204, 208, 210, 221, 223, 225, 227, 249, 251, 296, 298, 300, 302, 336, 372, and states "These lines carry rulings outside E38-1..16, and they bind as written." It also tabulates your Q1-Q17 rulings verbatim (L255-276); see S11 for where each is applied.

"""+R(451,1034)
TAIL="""
12. Verification [condensed]
12.1 Read-only checks by the Delegate: raw #38 sha and 385 lines; the 16 E38 quotes, 43 body excerpts, Q table, model block and tolerance block extracted programmatically and checked as exact substrings; E37 quotes re-checked against #37 raw; exact rational t computed from stage_O1.json stage4_chart_exact [0][0] and [3][0]; stage_O1.json has no P_h or P_a key, so c2 and c3 cannot be computed exactly here; accounting arithmetic 7*(98,304*5 + 256) = 3,442,432 (matches #38 L369), + 1,536 = 3,443,968; 784,960/21.7287 ~ 36,125/s; 3,443,968/36,125 ~ 95.3 s; line citations in pinned.py, stages.py, results.json checked.
12.2 UNVERIFIED: D1-D7 and P0; all numerical ranks; full-precision normalizations and bounds; c2 and c3; NC admissibility; SYS-FK validity bounds; workload, runtime and memory.
12.3 Raw #38 vs the Specialist's summary (raw governs). Agrees on the main rulings. Differences followed per raw: (1) SYS-NC1 relabelled as varying-kappa two-coordinate confound, not renamed (L160); (2) plateau construction rejection also corrected (L225); (3) Q5 operational-diagnosis wording, attribution split withdrawn; (4) rank premises also cover SYS-O6 and SYS-NC2 (L73); (5) requirements the summary omitted (E38-5, -6, -7, -8, -11; Q4, Q10, Q11, Q12; L94; L186); (6) the full tolerance block L280-302; (7) Q-ceiling: "answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY"; (8) count: package maximum is 3,443,968 float plus 272 exact, since #38 L372 calls 3,442,432 "not yet the complete package count".
12.4 Not done: no code run, no oracle/solver/fit/simulation; repo not modified; v1.1 and note 1 not edited; nothing posted.

=== ADDITIVE NOTE_1 to v1.2 (Research Delegate; full text, sha256 832d9bcfb5855ad20abf242888bfda0f372f3ad83e48f197005e3d37905033b9) ===
"""+open(NOTE).read()+"""
=== RESEARCH LEAD NOTES ===
- NOTE_1 records the CNA's read-only check of v1.2 against your #38 raw text (room, about 12:42 AM ET 2026-10-23), and the Research Lead has accepted it. The CNA found: E38-2 (first-order wording) correct - C4.2(c) treats the chart increment S_g*C*delta as exact and J_a*delta as first-order; C4.2(d)'s exact residual is Phi(theta_a + S_gC delta) - Phi(theta_a + B_global delta); C5.6 keeps losses finite; C4.5 marks D6's (1+lambda)^2 and factor 4 as Jacobian-level; the remaining exact claims are exact because each readout is affine in z. E38-3 correct where stated, but the C3.3(b) premise table was missing the D6 SYS-LIM global row and the SYS-NC1 global row (NOTE_1 N1), and "resolved full column rank" needed the sigma-ratio definition (NOTE_1 N2). E38-10 (SYS-FK) correct. Non-blocking: c2 = rho_NC1 holds only if sum_a P_a = 1; the Research Lead adopted both fixes (NOTE_1 N3: exact-rational assertion sum P_a = 1, and c2 = rho_NC1 / sqrt(sum P_a)).
- Delegate's room summary of v1.2: E38-1..16 quoted in full with compliance tables; 31-entry change log; accounting table (98,304 edits per system, 688,128 over 7; 3,442,432 evaluation propagations matching #38 L369; 1,536 O2 float; 3,443,968 float + 272 exact in total; 541 SVDs; 5,040 loss cells; closure identity; runtime ~95 s UNVERIFIED); places it followed the raw over the summary (S12.3); and the TO BE FIXED list. c2 and c3 are package-computed from exact law; t is an exact rational ~0.403485. Still open: hashes and generation rules for Q, Q2 and the directions; the memory estimate; the output schema; code, manifest and application.

=== QUESTIONS FOR CONSULT #39 ===
(1) Does v1.2, together with NOTE_1 (the accepted CNA points), satisfy E38-1 to E38-16? Name any edit that is not met, or that is over- or under-implemented.
(2) Rule on Q-R1 to Q-R6:
- Q-R1: a D7 failure reads INVESTIGATE, with no stop.
- Q-R2: the class zero-gain check is per cell (fold/class/group/size).
- Q-R3: a rank lapse in SYS-O6 or SYS-FK also reads NOT MET (RANK).
- Q-R4: an exact predictor that fails the validity guard (actual valid) is an identity failure.
- Q-R5: the rank-guard (extended B3) stacking convention and band handling.
- Q-R6: the cache policy and stage order.
(3) Rule on the CNA's rank-table additions (NOTE_1 N1) and the sigma-ratio definition (N2), and on N3.
(4) Is the C8.3 accounting table complete and correct for E38-13?
(5) Can the remaining TO BE FIXED items (Q/Q2/direction generation rules and hashes, memory estimate, output schema) be fixed at implementation time and checked by an independent pre-seal review? Or must they be in the scope record before freeze?
(6) Verdict: FREEZE (optionally with named edits, verbatim, numbered E39-1..), or REVISE AND RESUBMIT. Restate the caps (current: 1 CPU, no GPU, RLIMIT_AS 4,000,000,000 bytes, 600 s cumulative, 540 s operational stop, hard termination <= 595 s, no retries) and the claim-ceiling text if they change.
"""
