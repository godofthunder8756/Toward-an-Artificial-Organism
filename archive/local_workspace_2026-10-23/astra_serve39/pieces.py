def compact(a,b):
    out=[];cur=None
    for l in L[a-1:b]:
        m=re.match(r'^\*\*(E3[78]-\d+)\*\* \[(L\d+)\]',l)
        if m:
            if cur: out.append(cur)
            cur=m.group(1)+' ['+m.group(2)+']:';continue
        if cur is None: continue
        if l.startswith('|') and not re.match(r'^\|[-| ]+\|$',l) and 'Requirement | Clause' not in l:
            c=[x.strip() for x in l.strip('|').split('|')]
            cur+=' '+c[0]+' -> '+c[1]+';'
        elif l.startswith('*Binding here:*') or l.startswith('*Note (#38):*'):
            cur+=' '+l.replace('*','')
    if cur: out.append(cur)
    return '\n'.join(out)+'\n'
HEAD="""Consult #39 - PRE-FREEZE REVIEW of the C-kappa CLASS-FIT SYNTHETIC-ONLY SCOPE RECORD v1.2 + additive NOTE_1 (answers your #38 REVISE AND RESUBMIT, edits E38-1..16, raw sha 87fd77e0). Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

What is sent. The record under review is ckappa_classfit_synthetic_scope_record_v1_2.md (Research Delegate, sha256 79ea0eeb1658e7d265aae3a68d31c6fb385ceab23a91eb654fee61a4aa64561c), status DRAFT, NOT FROZEN, NOTHING RUNS, 94 KB. It is sent CONDENSED: sections 3-11 (every clause, label, SYS-* definition, derived expectation, outcome order, the full accounting table, the TO BE FIXED list and Q-R1..Q-R6) are sent essentially verbatim. Condensed [condensed]: the 31-entry change log (titles only), the source/hash table, the E37 and E38 compliance maps (the requirement->clause rows are kept, the verbatim E37/E38 quotes are dropped because they are your text, checked in-record as exact substrings of the raw), the 43 verbatim #38 body excerpts and the Q1-Q17 ruling table (your text; mapped in S11), and S12. NOTE_1 (sha 832d9bcf...) is sent in full. v1.1 (97165ac6) and v1.1 NOTE_1 (00ec1902) are unchanged and superseded. ASCII transliteration only (Greek spelled out, markdown dropped). Nothing has run; no checkpoint is opened.

=== RECORD v1.2 (condensed where marked) ===
"""
REC = R(1,26) + """
Change log relative to v1.1 + note 1 [condensed: 31 entries, titles only, each cites its #38 source]
Withdrawn: (1) Option A NC floor; (2) v1 Option B; (3) B-repaired/shared e/D2' and dx/dy table; (4) Option C; (5) matched/effective-basis-span material; (6) v1.1 note 1 item 3; (7) SYS-LIM under B-repaired; (8) inferred orbit masses and c2~0.100448/c3~0.199056 (now package-computed from exact law); (9) DERIVATION PREMISE vs IMPLEMENTATION labels (stop kept).
Corrected: (10) D1 residual/SYS-PC local map (E38-2); (11) full-column-rank premises, "for every resolved design" withdrawn (E38-3); (12) D3 wording; (13) SYS-PC global cancellation check (E38-4); (14) SYS-LIM first-order/exact failure/no impossibility/D7 diagnostic/exact midpoint; (15) SYS-FK alternatives (E38-10); (16) P0 (E38-5); (17) extended B3 (E38-6); (18) masks and identity domains C5.3, C7.0 (E38-7, -8); (19) system-level normalization (E38-11).
Fixed: (20) tolerances Q9; (21) HEADROOM thresholds Q4/E38-12; (22) draw reuse Q10; (23) sizes Q12; (24) SYS-O6 Q13; (25) midpoint Q14; (26) rank lapse Q15/E38-12; (27) autonomy Q17; (28) B1 extension Q3/E38-8; (29) caps E38-14. Added: (30) accounting table S8 (E38-13); (31) claim ceiling E38-15 + #38 L202 sentence (C1, C10).

0. Sources, hashes and precedence [condensed]
Governing raw files: #38 87fd77e0 (governs over everything, including this file and any summary of #38), #37 ce010fdb (below #38), #36 c8342d5a (inherited oracle definitions). Superseded: v1.1 97165ac6, v1.1 NOTE_1 00ec1902 (item 3 withdrawn). Inherited: governing set 6a5e0f24, B2/B3 ruling 6d75918f, v1_4_N closure note 4ad1d217 (B1, 595 s, N-b), v1_4_N 3f0c5c12, v1_3_E36 f6263fb8, oracle v1.1 e40c288f, results review 617e983d (M-1). PR #13 scratch @14376f38 read only (stages.py 936d3378, linalg_fit.py de6f4034, geometry.py 117e98e9, world.py 3d235fca, pinned.py 03c55323; outputs stage_O1.json 794746a7, stage_O7.json 994dda0a, results.json 6adb5de2, fit_freeze_O6.json b6f817c8, fit_freeze_O7.json 347bcd51).
"""+R(105,117)+R(118,119)+"""
[E38-15 verbatim here - your text.]
"""+R(124,132)+"""
2. Astra #37 items: compliance map (kept from v1.1) [condensed: E37 quotes dropped; checked as exact substrings of #37 raw]
E37-1..E37-10 requirement -> clause map is unchanged from v1.1 (which you reviewed in #38), with clause numbers updated: E37-1 -> C1.2, C10.3; E37-2 -> C9.4, C5.5; E37-3 -> C5.4, C10.2; E37-4 -> C10.1, C1.2; E37-5 -> C3.1, C3.2, C3.5, C3.7 (note: E38-1's plain separately fitted per-class maps satisfy E37-5 literally; v1.1's B-repaired departure withdrawn); E37-6 -> C4.2 (SYS-PC, D1-D3 UNVERIFIED, first-order per E38-2; class dependence from the system's own readout sign(psi1 psi2)), C4.3 (SYS-FK); E37-7 -> C4.4, C6 (no gain-must-vanish criterion for SYS-NC1-NC3 or SYS-LIM; no floor, no augmented basis); E37-8 -> C3.6(a)-(e), C3.8; E37-9 -> C9.1, C1.1, C9.2, C1.2, C9.3, S0, C9.5 (every TO BE FIXED BEFORE FREEZE item fixed in a frozen file before any execution); E37-10 -> C1, C10.4 (verbatim neural ceiling with the #38 L202 sentence).

2b. Astra #38 items: compliance map [condensed: E38-1..16 quotes dropped (your text; exact substrings of raw sha 87fd77e0..ca2a5, re-checked in S12). Each requirement -> clause row is kept verbatim.]
"""+compact(220,379)+"""
Other binding #38 body text [condensed]: the record quotes verbatim 43 excerpts of your raw text, at L5, 38, 46, 57, 69, 71, 73, 83, 94, 96, 118, 120, 124, 134, 138, 154, 156, 158, 160, 164, 183, 184, 186, 190, 192, 194, 196, 198, 204, 208, 210, 221, 223, 225, 227, 249, 251, 296, 298, 300, 302, 336, 372, and states "These lines carry rulings outside E38-1..16, and they bind as written." It also tabulates your Q1-Q17 rulings verbatim (L255-276); see S11 for where each is applied.

"""+R(451,620)+"""- (d) D1, global fit (UNVERIFIED; #38 L13-38) [condensed]. With P0, sum_g G_{g.r} = 4 diag(G_r[xx], G_r[yy], G_r[kk]) and sum_g G_{g.r} S_g = 4 diag(G_r[xx], G_r[yy], 0). For fit sets that are unions of complete orbits, given the C3.3(b) rank premise: B_global = [c_x; c_y; 0] and A_global = [c_x; c_y]; the two predicted perturbed charts are equal, so their finite forecast predictions are equal wherever propagation is defined. Residual: the exact finite discrepancy is Phi(theta_a + S_gC delta, u) - Phi(theta_a + B_global delta, u), computed by propagation (C5.6); L_a[:,kappa] chi_a c_tau delta is only its first-order approximation (#38 L40-57).
"""+R(626,665)+"""- Alternatives (corrected per E38-10, #38 L206-227) [condensed]. A globally constant kappa cannot reproduce true baselines with different kappa values, but autonomous same-baseline controls with kappa fixed under the declared interventions can exist (e.g. a frozen register r initialized to kappa_a and unchanged by edits, #38 L214-221: an intervention-fixed control), and a two-coordinate plateau construction is not excluded (#38 L225). Both are outside this package and are not added. No impossibility of same-baseline autonomous controls is claimed.
"""+R(672,691)+"""- Values: c2 = TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW; c3 = TO BE COMPUTED BY THE PACKAGE FROM EXACT LAW. [condensed] Computed at stage S4 before any fit, recorded, never changed (Q7). Earlier values from probabilities reconstructed from rounded SDs are withdrawn. The record does not compute exact-law values: stage_O1.json stores the exact stage-4 charts but not P_h or P_a (stages.py:285-291 builds P_a only in memory), so exact-law P_a needs the O1 filter run, excluded here. Frozen arithmetic: P_a = sum_u P_h(a,u) as an exact rational sum, converted once to float64; rho, c2, c3 computed in float64 and recorded at full precision. (NOTE_1 N3 adds the sum P_a = 1 exact assertion and c2 = rho_NC1/sqrt(sum P_a).)
"""+R(697,707)+"""- Crossing bound (#38 L239-245 confirmed). ||psi'1| - |psi1|| <= |Delta psi1| <= eps_syn*sd_x. With the displayed sd_x = 0.36806: eps 0.02 -> 0.00736; 0.05 -> 0.01840; 0.10 -> 0.03681; 0.25 -> 0.09201. All are below the margin 0.126647. The full-precision bound is computed by the package (#38 L249). An observed crossing is an integrity failure.
"""+R(718,944)+"""C8.7 Workload estimate (UNVERIFIED feasibility estimate, not a guarantee) [condensed]. Reference: the sealed oracle run made 784,960 float propagations (results.json:72) in t_elapsed_s = 21.7287 (results.json:26466), ~36,125/s including setup and reporting; linear scaling to 3,443,968 gives ~95.3 s. Not covered: 541 SVDs on small designs (largest fit design 384 x 3 global; class 96 x 3; largest B3 stack 384 x 8) and serialization; on paper small against the 540 s stop; not measured. Memory: not estimated; per-edit forecasts aggregated into loss cells, not stored per edit; a memory estimate is TO BE FIXED BEFORE FREEZE, in the application. No pilot is run (#38 L372).

"""+R(952,975)+"""10. Wording rules [condensed; all kept]. C10.1 Negatives (E37-4): "The declared [global/class-conditioned]-map intervention-prediction criterion was not met."; cap-limited work is "incomplete", never negative (E38-14). C10.2 Ratios (E37-3): "Comparator squared prediction error divided by actual response energy." C10.3 Oracle labels (E37-1): "Oracle-scale headroom only." C10.4 Neural ceiling: E37-10 and E38-15 verbatim plus the #38 L202 sentence. C10.5 SYS-PC success: "The class-conditioned fit recovered the declared sign-dependent synthetic map, which the global fit cancels as derived." - not that a network uses kappa, carries a class label or has a covariance register; thresholds never a neural floor. C10.6 Extended B3 never described as applicable to neural two-coordinate systems (E38-6). C10.7 SYS-LIM only with the exact failure statement of #38 L194; no impossibility wording (E38-9). C10.8 Confounds: RMS matching never described as matching response, conditioning, transferability or GRU geometry; "floor" not used for any confound result; SYS-NC1 described as varying-kappa two-coordinate confound. C10.9 SYS-FK "globally zero-kappa on product-chart designs"; no impossibility of alternatives (E38-10).

"""+R(990,991)+"Q1-Q17: all closed by #38 (L253-276) and applied as tabulated in the record [condensed]: Q1 C3.2, C6; Q2a-d change log 2-3, C3.2; Q3 C3.9; Q4 C7.3; Q5 C4.0, C7.1; Q6 C4.3; Q7 C4.4.R; Q8 C4.2(b); Q9 C5.5; Q10 C5.2, S0; Q11 C4 notation; Q12 C5.2; Q13 C4.1; Q14 C4.5; Q15 C7.2; Q16 change log 7; Q17 C4.5.\n"+R(1017,1034)
TAIL="""
12. Verification [condensed]
12.1 Read-only checks by the Delegate: raw #38 sha and 385 lines; the 16 E38 quotes, 43 body excerpts, Q table, model block and tolerance block extracted programmatically and checked as exact substrings; E37 quotes re-checked against #37 raw; exact rational t computed from stage_O1.json stage4_chart_exact [0][0] and [3][0]; stage_O1.json has no P_h or P_a key, so c2 and c3 cannot be computed exactly here; accounting arithmetic 7*(98,304*5 + 256) = 3,442,432 (matches #38 L369), + 1,536 = 3,443,968; 784,960/21.7287 ~ 36,125/s; 3,443,968/36,125 ~ 95.3 s; line citations in pinned.py, stages.py, results.json checked.
12.2 UNVERIFIED: D1-D7 and P0; all numerical ranks; full-precision normalizations and bounds; c2 and c3; NC admissibility; SYS-FK validity bounds; workload, runtime and memory.
12.3 Raw #38 vs the Specialist's summary (raw governs). Agrees on the main rulings. Differences followed per raw: (1) SYS-NC1 relabelled as varying-kappa two-coordinate confound, not renamed (L160); (2) plateau construction rejection also corrected (L225); (3) Q5 operational-diagnosis wording, attribution split withdrawn; (4) rank premises also cover SYS-O6 and SYS-NC2 (L73); (5) requirements the summary omitted (E38-5, -6, -7, -8, -11; Q4, Q10, Q11, Q12; L94; L186); (6) the full tolerance block L280-302; (7) Q-ceiling: "answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY"; (8) count: package maximum is 3,443,968 float plus 272 exact, since #38 L372 calls 3,442,432 "not yet the complete package count".
12.4 Not done: no code run, no oracle/solver/fit/simulation; repo not modified; v1.1 and note 1 not edited; nothing posted.

=== ADDITIVE NOTE_1 to v1.2 (Research Delegate; full text, sha256 832d9bcfb5855ad20abf242888bfda0f372f3ad83e48f197005e3d37905033b9) ===
"""+open(NOTE).read()+"""
=== RESEARCH LEAD NOTES ===
- NOTE_1 records the CNA's read-only check of v1.2 against your #38 raw text (room, ~12:42 AM ET 2026-10-23), accepted by the Research Lead. CNA: E38-2 correct (C4.2(c) chart increment exact, J_a*delta first-order; C4.2(d) exact residual Phi(theta_a + S_gC delta) - Phi(theta_a + B_global delta); C5.6 finite losses; C4.5 marks D6's (1+lambda)^2 and factor 4 Jacobian-level; remaining exact claims exact because each readout is affine in z). E38-3 correct where stated but premise table incomplete (N1) and needs the sigma-ratio definition (N2). E38-10 correct. Non-blocking c2 normalization fix adopted (N3).
- Delegate's room summary of v1.2 matches the record (accounting totals 688,128 edits, 3,442,432 S6 + 1,536 O2 = 3,443,968 float + 272 exact propagations, 541 SVDs, 5,040 loss cells, ~95 s UNVERIFIED). Still open: Q/Q2/direction hashes and generation rules; memory estimate; output schema; code, manifest and application.

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
