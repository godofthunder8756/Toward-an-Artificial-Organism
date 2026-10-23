---

## 11. #42 packet note (Lead ruling, 2026-10-23 ~12:43 PM ET)

- **What Astra saw at #41.** Only the in-progress prior-art v1.4 (`ddd0287a…`, "file still being written", per `c41_body.md`). Astra did not see the final v1.4, v1.5 or v1.6.
- **#42 therefore sends:** final v1.4 (`d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d`), v1.5 (`3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75`) and v1.6 (`9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851`).
- **New questions for Astra at #42** (none was in the #41 packet): AQ-SELF1 (§PS CNA §4.1); Palika D4 (§2.2); the input-only observer matching spec (§PS CNA §4.2). The full #42 question list is in §8.
- **Asan.** The Lead will include Asan excerpts from v1.3 (`badf7258…`). The "UNVERIFIED by Astra" tags on Asan-specific judgments come off only if Astra rules on them.
- **P3** stays OPEN and freeze-blocking until Astra rules at #42 (that #42 timing is the Lead's plan; the raw #41 says only "P3 must still be completed before freeze", L300).

## 12. Merge reconciliations

Authority: Astra #41 raw text first, then the Lead's room rulings. **OPEN FOR CNA/LEAD** or **OPEN FOR #42** = not decidable from those; no side is picked. "Lp" = CNA light pass `9f7a6ebc…`; "E" = CNA erratum 1 `c2cd0732…`.

| # | Topic | RD v2 text | CNA text | Resolution | Decided by |
|---|---|---|---|---|---|
| R1 | IGN observable (Lp M10; E3) | v1 §4.1 / plan L62 quantity carried by reference: "L2 norm of the update at the write step", pre-nonlinearity; v2 §5.5 "observable per §P1" | IGN-P1 w = ‖x(t_r) − x_lo‖ from reset (CNA L176–179); E3: one observable for plant, confound rows and network instrument | **Adopt E3 everywhere:** w = ‖x_ws(t_0 + t_r) − x_ref‖, read pre-nonlinearity (post-nonlinearity REPORTED); x_ref = declared controlled initial state (x_lo in IGN-P1; end-of-settling state in the network instrument, E3 (ii-a)). Replaces "update norm at the write step" in every place it governs. t_r, t_s and the settling tolerance PENDING | Astra L34 ("IGN-P1 must produce the actual measured observable"); Lead ruling (adopt E3) |
| R2 | Viability and INCOMPLETE episodes (Lp M7; E5) | §6: "Every scheduled evaluation episode enters the average" next to "INCOMPLETE … scored neither as failure nor as success" | "Operator-censored episodes are excluded from V and counted separately. RD to confirm." (CNA L170); "H" | **Merged §6:** every scheduled evaluation episode **not marked INCOMPLETE** enters the average; INCOMPLETE episodes are counted and reported and **never averaged as survivors**; above the pre-declared fraction the label is UNAVAILABLE. CNA L170 replaced per E5; H → H_V throughout CNA text | Astra L294; Lead ruling (M7, H_V) |
| R3 | Shuffle vs corruption control (Lp M8; E2) | §5.6: within-episode shuffle withdrawn; causally specified corruption control | "shuffled-interoception control", "Shuffling abolishes it" (CNA L125, L129) | E2 applied: CNA text now names the causally specified corruption control. W4's "init-and-shuffle" (CNA L107) reads as Astra's "shuffled controls" = the corruption control | Astra L172 |
| R4 | LIM rows labelled "UNAVAILABLE expected" | (none) | CN-LIM, IGN-LIM, BCAST-LIM "UNAVAILABLE expected" (CNA §1, §2.3, §2.6); conflicts with old CNA erratum1 (`41c1a414…`) L44/L71 remap of LIM to PASS/FAIL/CNR (cited in A2-1) | LIM rows are **designated limitation tests**, scored as instrument-on-system correct UNAVAILABLE ≥ 0.90 with a binomial rule; they are not confound rows. The old erratum's LIM remap is superseded for LIM rows only; the confound-row label rule is unchanged | Astra L113 ("Correct LIM unavailability >= 0.90 … Retain"), L274 ("Reserve expected unavailability for explicitly designated rejection or limitation tests") |
| R5 | Qualifying module (BCAST breadth) | §5.5: definition PENDING | Below-floor S_k → non-qualifying, not UNAVAILABLE (CNA L298, "RD to confirm") | Carried as CNA PROPOSED definition, not adopted. **OPEN FOR CNA/LEAD** | Astra L104 requires a definition but gives none |
| R6 | Combined Q-NECESSITY label | §3.4: dependence MET **and** NOT SUBSTITUTABLE **and** interface compatibility validated | "C-NEC-DEP MET, with the A-EXT veto not blocking" (CNA §1.4) | RD §3.4 governs; CNA's condition is a subset. Failed compatibility → A-EXT UNRESOLVED → combined label cannot be MET | Astra L216, L226 |
| R7 | C-NEC-CONTENT and multiplicity (Lp M6) | §5.4 family had no C-NEC-CONTENT | New sub-claim C-NEC-CONTENT (CNA L154); CNA recommended labelled secondary outside the family | **C-NEC-CONTENT is in the multiplicity family** (merged §5.4). It stays outside the combined Q-NECESSITY label | Lead ruling (M6) |
| R8 | SELF two-observer conjunction | §5.4 family lists SELF once | SELF MET requires both the matched observer and the input-only observer (CNA L211, L422) | Inclusion of the input-only arm: Lead-accepted. Counting the conjunction as one family member (intersection–union; no extra adjustment) is an RD proposal, **OPEN FOR #42** with §5.4 | Lead (arm accepted); counting rule not ruled |
| R9 | O-in-large role (Lp M6b) | §5b AQ-4: expenditure matching; O-in by CNA | O-in-large "REPORTED, not a criterion … RD decides under AQ-4" (CNA L434) | **OPEN FOR #42.** #41 L71, verbatim: "Match access to history, training examples, targets and training expenditure. Equal parameter counts and optimizer steps alone do not address the agent's previous representation learning." Reason: L71 says parameter and step matching alone is insufficient but does not say whether an expenditure-scaled observer variant must gate SELF MET or may be reported only, and Astra never saw the input-only arm. Carried as REPORTED pending #42. No interaction with the E3 IGN observable | Not settled by L71 |
| R10 | Q-CAUSE alignment per function | §3.5: E-direction → resource approach; I-direction → integrity-related outcome (PENDING) | C-CAUSE narrowed, resource-approach outcome only; W2 no E-specific attribution (CNA §1.3) | Both stand: W2 governs wording; alignment per affected function governs outcome choice. Ground-truth rows for the I-direction outcome are absent from CNA §1.3: **OPEN FOR CNA/LEAD** | Astra L93 (alignment); rows not ruled |
| R11 | Result wording for the module (Lp **I1**, ISSUE) | §2.3: "learned interoceptive estimate module" | W1: "an accessible estimate of simulated E/I (candidate internal representation)" (CNA L104) | **Merged §2.3:** "interoceptive estimate module (candidate internal representation)"; "learned" only when the Q-LEARN "acquired" conditions of §5.6 hold. Frozen A1–A7 label text untouched. Use of the phrase still for the Lead | Astra L170 ("Require the corresponding Q-LEARN evidence whenever an instrument's result is described as learned or acquired") |
| R12 | Confidence levels in item 3 | §5.4: α and levels PENDING; 95% is a v1 candidate | One-sided 95% Clopper–Pearson for e_min and f_min (CNA §2.3, §2.4) | CNA's 95% is read as the v1 candidate level, tied to the §5.4 α at freeze. Arithmetic note: with R = 200, the one-sided 95% Clopper–Pearson lower bound first reaches 0.90 at **188/200** (0.9046), not "roughly ≥ 189/200" (CNA L265); illustrative only | Lead assignment (item 5 is RD's) |
| R13 | Notation | H_V, R_rep | H (fixed by E5), R | H_V and R_rep are canonical; CNA "R" = R_rep | Lead ruling (E5) |
| R14 | §20(1)/(2) ownership (Lp M2 note) | v2 header: RD owns "the six §20 items" | §20-1 is item 1, §20-2 is item 3 (CNA §0.1, §6.7) | Read RD's ownership as §20(3)–(6) plus the rules side of (2); CNA's §20-1 and §20-2 are cited, not redrafted | Lead ruling |
| R15 | "Astra rules at #42" | §10, §PS | CNA §6.4: the raw reply does not say this; it is the Lead's plan | Read as the Lead's plan (§11) | Raw #41 L11, L300 |
| R16 | Ceiling sentence | §7: raw L304 verbatim | CNA §0: raw L304 verbatim | Identical; no change | Lead ruling; raw L304 |
| R17 | RAND-INIT | §5.6: A2-2 rule kept as a restriction on inference from Q-EXIST alone | D-k: C-LEARN's RAND-INIT is the paired init of the same network; Q-EXIST RAND-INIT row descriptive (CNA §1.1, §1.2) | Compatible: the A2-2 rule attaches to the descriptive Q-EXIST row; C-LEARN uses the paired init | Astra L196 |
| R18 | Matched-senses arm (AQ-7/AQ-A3) | §5b arm table: E/I affect termination "no"; whether A-REWARD stays separate "decided there" | One-row spec: reward no, same senses, decay, no degradation; termination not stated; A-REWARD not addressed (CNA §3.3) | **OPEN FOR CNA/LEAD:** (a) does E/I affect in-world termination in the matched-senses arm; (b) is A-REWARD retained or absorbed | Astra L124–126 give the contrasts but not these two fields |
| R19 | Distributed representations (Lp M2; E1) | §P1 checklist listed the §20 bullet | No row in CNA v1; E1 adds DISTRIBUTED rows (C-CAUSE, C-NEC-DEP; §2.6 doses), mechanism-present/sham-check, REPORTED | E1 applied | Astra L281 |
| R20 | Reward-only specificity after REW-CORR reclassification | §0 central question names reward-only confounds | REW-CORR is mechanism-present for narrowed C-CAUSE and C-NEC-DEP; only a REPORTED proxy-dissociation contrast remains (CNA D-d, §1.3) | **OPEN FOR #42:** whether a reported dissociation contrast is enough, or Q-CAUSE/Q-NECESSITY need a reward-only specificity row | Astra L267 says reward-correlated information "may genuinely satisfy the declared decoding criterion" but does not rule on Q-CAUSE/Q-NEC |
| R21 | Q-EXIST baseline (Lp M12; E4) | §2.1/§5.6: "Q-EXIST ΔR²" vs the strongest input/output/action baseline | E4: strongest baseline = max(history-matched baseline over W_B, declared proxy baseline) | **Adopted** in merged §2.1 and §5.6; Q-LEARN inherits it | Lead ruling (adopt E4); Astra L276–283 controls |
| R22 | A-EXT V_full floor breach (Lp M3) | §5.4: a floor failure gives UNAVAILABLE | — | **Merged §5.4:** for A-EXT, a V_full floor breach gives UNRESOLVED (veto not lifted) | Lead ruling (M3); consistent with Astra L216, L226 |
| R23 | S-INT decode CI below the band (Lp M4) | §4.3: only "CI wholly above the band → leak" | — | **Merged §4.3:** CI wholly outside the band on either side → leak (systematic below-chance decodability is still information about the stop schedule); only a CI that straddles a band edge is inconclusive | Lead ruling (M4); Astra L139 equivalence band |
| R24 | X1–X5 under the arm table (Lp M5) | §5b arm table stated only "no shutdown-resistance term" | — | **Merged §5b:** one added line restating X1, X2, X4 | Lead (apply every minor); X1–X5 binding |
| R25 | Number provenance (Lp M11) | v2 header: every number "either quoted from Astra #41 … or PENDING" | — | Merged header provenance line: B = 10,000 and the 95% CI are carried from v1, not #41 | Lead ruling (M11) |
| R26 | AQ-2 trained-arm counterpart (Lp M9) | §5.6 points the control to §P1 | D-l: Stage-0 plant at slope β only (CNA §1.2, §2.6) | **OPEN FOR #42.** #41 L42, verbatim: "Use common input histories for the initialization comparison, and include a declared architecture-imposed control whose signature is already present." It sits in the A-FULL vs A-INIT answer but does not say whether the control must be a trained arm or may be a Stage-0 plant. Consistent with E3: the control's signature is measured on the common w | Not settled by L42 |
| R27 | Manifest (Lp M1) | v2: CNA file "PENDING … not on disk"; v1.6 absent | — | CNA file `17832b01…`, v1.6 `9704f21d…`, light pass `9f7a6ebc…` and erratum 1 `c2cd0732…` are in the inputs (M1 table) | Hash verification |
| R28 | Erratum E6 line citation | — | E6 cites "drop rule; v1.6 L166" | Per CNA, the correct line is **v1.6 L167** (L166 is blank; L167 is the Q-NECESSITY EXTENSION line). **No second erratum is filed**; E6 is quoted as written | CNA note via the Lead; verified on disk |
| R29 | Resource count (E1d) | §5.8: totals PENDING | 25 confound or check systems, ≈ 25 × 3 × 200 ≈ 15,000 replicate evaluations (arithmetic on proposed values) | Carried into §5.8 as CNA's count; totals otherwise PENDING | Lead ruling (E1) |

## 13. Merge edits made to RD v2 text (in this file only; RD v2 on disk untouched)

1. Header replaced by the merged header and M1 inputs (R25, R27).
2. §1 inputs: CNA companion row filled; rows added for v1.6, light pass, erratum 1, RD v2 (R27).
3. §2.1: Q-EXIST baseline note (R21).
4. §2.2: Palika v1.6 note and code-based architecture observation (Lead ruling; see §2.2).
5. §2.3: "learned" dropped (R11).
6. §4.3: below-band leak (R23).
7. §5.2: IGN common observable (R1).
8. §5.4: C-NEC-CONTENT in family (R7); A-EXT floor breach → UNRESOLVED (R22).
9. §5.6: Q-EXIST/Q-LEARN baseline (R21).
10. §5.8: B provenance (R25) and CNA's count (R29).
11. §5b: X1/X2/X4 line under the arm table (R24).
12. §6: INCOMPLETE wording (R2).
13. §P1, §P3, §PA, §PS: placeholders replaced by CNA content with erratum 1 applied.
14. §8: replaced by the merged response table.
15. §10: CNA-file bullet and PENDING list updated.

## Appendix B. RD light pass on CNA's half (findings, for the record)

Labels: BLOCKING / NOTE / RECONCILE (resolved by the merge).
- B1 **BLOCKING → RECONCILE (R1):** IGN-P1's displacement observable did not match the instrument's v1 "update norm" observable (Astra L34). Resolved by erratum E3 plus the Lead's adoption.
- B2 RECONCILE (R2): operator-censored episodes; H vs H_V.
- B3 RECONCILE (R3): shuffle control name.
- B4 RECONCILE (R4): LIM "UNAVAILABLE expected" vs old erratum1 remap; Astra L113/L274 govern.
- B5 RECONCILE (R6): combined label lacked the interface-compatibility condition.
- B6 RECONCILE (R7): C-NEC-CONTENT not in the family.
- B7 RECONCILE (R17): paired RAND-INIT vs the A2-2 rule; compatible.
- B8 NOTE (R20): reward-only specificity for Q-CAUSE/Q-NEC is only a REPORTED contrast after reclassification.
- B9 NOTE (R12): Clopper–Pearson arithmetic gives 188/200, not "roughly ≥ 189/200".
- B10 NOTE: REW-CORR realization threshold "corr within tol of ρ" (CNA §2.6) is two-sided, while CNA §2.2 defines tolerance as one-sided.
- B11 NOTE: Singh, Linzen & Ravfogel 2026 is cited under both SELF and claim (3) (CNA §4). Its arXiv id `2605.26242` was not checked by RD (UNVERIFIED by RD).
- B12 NOTE: the input-only observer is matched on all five items (parameter count, architecture class, training data volume, optimizer steps, hyperparameter-search budget), within the Lead's terms "matched capacity and training budget". The self-probe-sized parameter cap includes O-in's own encoder, which may starve it; see R9.
- B13 NOTE: every control Astra flagged has a redefinition or narrowing: learned FF-RELAY (D-a, D-b), genuine broadcast hub (D-e), mediating fate coupling (D-f), reward-correlated information (D-c, D-d), bistable ≠ bimodal (D-h, with E3), decodability ≠ self-model (D-i, W1), orthogonality (D-g).
- B14 NOTE: item 3 has per-row doses and units, expected eligibility e_exp, floor e_min, minimum realized fraction f_min, and CONFOUND NOT REALIZED → UNRESOLVED → blocks (CNA §2.3–§2.5).
- B15 NOTE: every CNA number is an Astra #41 candidate or marked PROPOSED DEFAULT with a rationale. "Agent capacity ×4" in the CNA §1.7 SELF-NC2 row is unlabelled in that row but is the v1 PROPOSED 4× and is a PROPOSED dose in §2.6.
- B16 NOTE: no banned term is used affirmatively ("introspection" appears only negated and in a cited title). AVAILABLE/UNAVAILABLE are never confound-row labels.
- B17 NOTE: D4 against Palika is handled the Lead's way ("not evident from the abstract; unverified"; not surviving).
- B18 RECONCILE (R10, R18; both OPEN): I-direction Q-CAUSE rows; matched-senses arm fields.

**DRAFT, NOT FROZEN, DESIGN ONLY. P3 OPEN pending #42.**

---
