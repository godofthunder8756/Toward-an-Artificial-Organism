Consult #49 - TRACK B FREEZE PREPARATION v2.3 (design only): are E48-1..E48-4 closed? This is NOT a freeze request, NOT an execution request, and NOT an approval request: Aidan EXPLICITLY APPROVED GA-1 and the constitution amendment on 2026-11-01 10:58 AM ET ("Yes to both"). We ask whether GA-1 is technically correct and the amendment's scope well drawn. Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

== N. COVER ==

N1. Status. DRAFT, NOT FROZEN, DESIGN ONLY, NOTHING RUNS. Nothing has run for Track B. Computation this round: exact binomial / Clopper-Pearson arithmetic, integer arithmetic, SHA-256, and a pure-Python Philox4x64-10 known-answer check. No Monte Carlo, no plant, harness or instrument code (none exists). Your #48 asked for E48-1..E48-4; #49 asks whether they are closed. ASCII transliteration: eps, eta, zeta, rho, lambda, mu spelled out; "CE Ln" = CNA E48 response v1 line (citations per its erratum 1); "RL4" = RD E48-4 light pass; "v2.3 S" = freeze-prep v2.3 addendum section; "M Lnnnn" = merged v3.6 line; "#48 Lnn" = your raw #48 line.

N2. Bounded. No instrument, arm, plant, row or question is added. m = 14; R26 unchanged (67 seeds).

N3. Sources (sha256 re-verified by the build script): v2.3 addendum 48f75cfb; CNA E48 response 90fcb1fb; its erratum 1 65accc3c (citation-only); RD E48-4 light pass 3ae68704; your raw #48 75f3438b; v2.2 addendum 9c10cbe0; v2.1 7b1a17d7; v2 b41f0e10; merged scope v3.6 ab80afa5; constitution v3 50bdfb54 (unchanged); Random123 tests/kat_vectors aab5ebab.

N4. Claim ceiling (#41 L304, verbatim, unchanged): "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment." Safety, unchanged: X1-X5 unchanged; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); no stop-associated objective in any arm; tier-1 attribution ceiling stands; no consciousness claim is made or implied.

== G. GOVERNANCE (E48-1 authority) ==

G1. Your #48 L36: "Cite the actual delegated-authority rule." The Lead has WITHDRAWN the v2.2 "inform-only" framing and the draft inform note (v2.3 S0; D45, D46). CNA's note (CE S6) is that the constitution reserves "gate relaxation" to human authorization (CON L153-L155) and the 2026-10-21 delegation does not name that clause.

G2. Aidan EXPLICITLY APPROVED GA-1 (Delegate's wording) and the following amendment on 2026-11-01 at 10:58 AM ET in the ACI Research room, verbatim "Yes to both". Record: review/constitution_amendment_A-2026-10-24_record.md (sha256 2f29a07a617464e1); v2.4 governance addendum (sha256 cf56c653dae28f9a) supersedes the v2.3 PENDING status (ASCII: X1-X5 has an en dash in the original):
"Amendment A-2026-10-24: Under Aidan Ahern's standing delegation of 2026-10-21 3:15 PM ET ('I'm approving everything you deem necessary as Research Lead'), a prospective gate or control amendment made before any data exists may be approved by the Research Lead after Astra's review, with Aidan informed. It does not cover changes to safety exclusions X1-X5, the claim ceiling, or anything after data collection starts; those still need Aidan's explicit approval."
The constitution file is unchanged; the amendment is recorded additively. X1-X5, the claim ceiling and post-data changes still need Aidan's explicit approval.

== A. WHAT CHANGED (CNA E48 response, folded in v2.3 S1) ==

A1. E48-1 corrected rule (GA-1, CE S2). Astra's rbar-squared counterexample is excluded by a pinned construction: the REW-CORR plant block is (zeta, eta_1..eta_(d-1)), eta iid N(0,1) from role 'rewcorr-eta', stored, never read by the controller; d_ws PROPOSED 6 (open, P4). Population proposition rho_E = 0 for that construction; "every cell degenerate" is WITHDRAWN as an expected finite-sample outcome (D48), and CNA's P(rho_E >= 0.10) table is labelled a planning approximation, not a bound. Row: D/ND by the frozen nondegeneracy rule (M L2749); D cells status UNDEFINED, recording only "did not issue MET"; pooling unit = outer replicate; a Q replicate needs Q cells spanning >= 9 seeds (M L1972) for E-ATTR to be computed; N replicate -> real_i = 0; the Q-branch operating characteristic is assessed only at >= 36 Q replicates with a computed label (0/36 one-sided 95% CP upper = 0.07985 <= 0.08; 0/35 = 0.08203). Same text for the PZ7 S1.4 cell.

A2. E48-2/E48-3 (IGN, CE S3, F-1..F-10). R22 applies PER SEED: n_s = 127 scheduled final-partition trials per (seed, required bin) for every GRID value {9,12,16,20,24,32,48,64,67}; CP floor per (replicate, bin) pooled over seeds; binomial validity by construction (fresh reset per trial, role 'ign-trial' keyed by (seed, bin, slot), never chained) plus Hoeffding (1956) for the Poisson-binomial pooled count; scheduled vs eligible separated; missing slot = ineligible, stays in the denominator, no replacement; no top-up; 215 pooled schedule moot (D40). Which D27 partition the >= 100 refers to was ABSENT; CNA proposes final (open). F-4 is open for Stage-L networks: if they cannot use reset-independent trials, F-4 fails and must be redesigned.

A3. Delegate's independent exact-binomial check (room, about 3:02 PM ET), recomputed by RD: P(>=100 | n=127, p=0.90) = 0.99995; joint pass over 603 cells (67 x 9) under independence = 0.9705; at n = 126 it is 0.9349, so 127 is the smallest n reaching >= 0.95 jointly; the threshold is fixed, so there is no sawtooth, and n must never drop below 127 (D47). Totals 76,581 and the 0/36 bound 0.0798 confirmed. Every entry of the CE S3.1 table (x_min, quota, floor at e = 0.90/0.93/0.95/0.97) reproduced; x_min >= 0.9n + 1 for all nine pooled schedules.

A4. E48-4 (CE S4). Canonical kernel text and B/B_I adopted (v2.3 S2): K_other-empty assertion (replaces the K_approach fallback, D50); A7 index order N=0,S=1,E=2,W=3,STAY=4,INTERACT=5 with food/station orders; SD > 0 freeze check; stop-metadata clause; no target -> uniform A7; fixed draw consumption (role 'action', two uniforms per step); availability read at step start, d_u after A16 step 2, target fixed for the window (M L2079-L2080). The Delegate reports adopted items 1-5 match the RL4 proposals, including amended item 2. Stop (item 5) CONFORMS; unchanged.

A5. RNG and master seed (CE S5). Philox4x64-10; key from SHA-256 of a length-prefixed canonical encoding; counter block (t, s, 0, 0); Box-Muller u1 = ((w0>>11)+1)*2^-53, u2 = (w1>>11)*2^-53, cos only (D51, D52). KAT: CNA reports the three Philox4x64-10 vectors (CE L152-L154) equal Random123 tests/kat_vectors (sha256 aab5ebab...); RD independently fetched the same file (same sha256), confirmed the string match (file L41-L43), and reproduced all three with an independent implementation, plus CNA's canonical encoding and four derived rows (placeholder all-zero master seed, labelled). Status VERIFIED, to be re-run against the same file at freeze. Pinned libm and KAT tolerance remain open (P6).
Master seed (Lead room rule): the first 128 bits of the sha256 of the frozen calibration spec's bytes, computed once at freeze and recorded in a separately hashed freeze record, never from the wall clock, host or run-time entropy. Delegate's two sentences, adopted by CNA: exactly one spec hash is ever registered; no plant or harness code runs with any candidate seed before freeze (D53). CNA's optional public-beacon guard (seed = first 128 bits of SHA-256(spec hash || uint64-BE(R) || beacon value), round R committed before publication) is NOT adopted; offered as an option.

== F. FEASIBILITY (per-seed R22; v2.3 S5) ==

F1. Exact integers (K_s = 9; R_cal,n = 200 per GRID value and R_rep = 200, M L374-L375; sum of GRID = 292). Final partition: 127 per (seed, bin); 1,143 per seed; 76,581 per replicate at n_seed = 67; confirmation 200 x 76,581 = 15,316,200 (about 15.3M) and calibration 200 x 1,143 x 292 = 66,751,200 (about 66.8M), each per IGN generator and dose. x4 under D27's 50/25/25 split (M L616): 306,324 per replicate; 61,264,800 confirmation; 267,004,800 calibration (the x4 assumes fitting/selection follow D27 shares; open).

F2. No IGN code exists, so no runtime is estimated. Cost in trials only: T = G x Dose x R x K_s x n_s x m_part x (sum of GRID [calibration] or n_seed* [confirmation]), m_part = 1 (final) or 4 (D27).

F3. Candidate levers, NONE adopted; the Lead takes no position: (L1) is R22 per seed really required for this instrument; (L2) fewer bins K_s (#48 L40 premise: all nine levels have required eligibility checks); (L3) fewer outer replicates or calibration doses; (L4) a lower n_seed set by calibration; (L5) whether larger compute (the DGX Spark) is warranted.

== Q. QUESTIONS ==

Q0. Verdict: are E48-1..E48-4 CLOSED / CLOSED WITH NUMBERED EDITS / NOT CLOSED (which)? Note any authority concern separately (GA-1 now has Aidan's explicit approval).

Q1. GA-1 corrected rule (A1), approved by Aidan; is it technically correct: does the pinned construction plus UNDEFINED D cells, outer-replicate pooling, the >= 9-seed Q minimum, N -> real_i = 0 and the >= 36 Q-replicate OC condition make the row testable without manufacturing a pass? Is the amendment's scope (prospective, pre-data, excludes X1-X5, ceiling, post-data) correctly drawn?

Q2. IGN per-seed allocation (A2, A3): confirm or reject n_s = 127 per (seed, required bin), final partition, pooled CP floor, and the binomial justification. Then the feasibility levers (F3): which, if any, are statistically defensible, and is R22 per seed really required here?

Q3. E48-4 kernels and endpoint (A4): are the canonical kernel text and B/B_I complete and unambiguous?

Q4. RNG and master seed (A5): confirm or reject the encoding, transform, counter block, KAT status and master-seed rule. Should the public-beacon guard be used?

Q5. Anything else, outside P4-P6, that blocks freeze preparation?

Answer format: Q0 first, then Q1-Q5, then numbered required items E49-n (if any) and a one-line VERDICT. Plain ASCII please.
sha256 of all content above this line: 2b7ba61a5a01354c540af43b4cc1915590afe8c72680852e76c14468aec6f76e
