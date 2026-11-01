# CNA light pass on merged v3.1 seams + RD v3.2 addendum, v1 (SHORT, usage-limit wrap-up)

CNA, 2026-10-23, about 3:00–3:16 PM ET. **DESIGN/AUDIT ONLY. NOTHING RUNS.** New additive file; edits nothing. Inputs (sha256 verified on the box; footers reproduced): merged v3.1 `9817c33b92ab776ab1703f3de4789ec8417bc2fb0a4d0cc9173295e18b02dcb0` (footer `84a5449b…`); RD v3.2 addendum `d724e453246786ce07652b51c1d5fda1a008704d3df5360f0fd7e3128c31600a` (footer `b7985f08…`); raw #42 `e438e329…`; CNA v3 half `5dec96f5…` (footer `7d93990c…`); CNA env/integrity `d5523c71…` (footer `e0d16350…`); CNA light pass `c47d8d47…` (footer `86bbc308…`); RD v3 half `0892ccac…` (footer `451c130a…`). Companion: CNA erratum 1 `trackB_scope_v3_CNA_plants_confounds_observer_v1_erratum1.md`.

## Verdict: CONFORMS WITH ISSUES (4 ISSUE), all fixable at the v3.2 merge; one needs a Lead ruling (S-I1). R39: OBJECT (narrow, one line).

## Checks done
- **Verbatim carriage:** script, stronger than the merge's set check: every CNA block is byte-identical after heading re-level only, as a contiguous run: CNA v3 L110–175 → v3.1 L576; L178–231 → L515; L234–328 → L649; L331–421 → L751; L1–107 → L849; L422–512 → L957; env file L1–216 → L1065. 401/401 and 174/174 non-blank lines confirmed; own footers fenced.
- **m = 14 propagation:** no unstruck "m = 13", 0.99615 or 2.665 remains; my text never states 13 (it says "§5.4 level"; D36 maps it to m = 14). Recomputed: 1 − 0.05/14 = 0.996429, z = 2.6901; noncentral-t n = 8/20/67 at m = 14 (66 at m = 13); floor 9 holds.
- **Light-pass I1–I4, M1–M12:** applied as R27–R42 (I1 struck in place; I2 R28 + §5.9; I3 R29; I4 m = 14 throughout). Residue: R29 (D18 L470), R33/R51 (D1 L453, D30 L482 still say "exactly 0.2"), R34 (D8 L460) are recorded in §17 but not struck in place. Strike at merge.
- **Safety:** "no additional stop-associated reward, penalty or terminal return" verbatim 14× in v3.1 and 1× in the addendum; X1–X5 list (§5b L292–299) and #41 ceiling (L440) verbatim.
- **R62** (H_V end = learner-side truncation with bootstrap): PASS; consistent with my A15, where in-world termination stays a true terminal (R47). **R63** (post-death steps = non-approach): PASS. **R65**, **L7**: PASS.
- **Seam cross-refs** §PC1–4, §PX, §PY, §17.3: resolve. Stale text (not ISSUE): §17.1 lead-in L1449 "Neither proposal had arrived"; §10 L1394; R20 L1455 "16-vs-63".
- **n_seed in my text:** only CNA L453 (v3.1 L988), consistent with R26(a).

## R26 budget checks (addendum §1.1)
- 200 × 67 = **13,400** ✓; Σgrid 292, × 200 = 58,400 ✓; 452 stops are not n_seed-dependent ✓.
- Observers: 96 = 2 required observers × 16 configurations × 3 init seeds; × 67 = **6,432** ✓. **9,648** (= 144 × 67) is moot under erratum E3: action-ignoring candidates reuse O-IN-P's trainings. **Missing:** the diagnostic plateau sweep (27 points × 3 seeds, on 3 designated seeds per arm per erratum E6), O-HEAD and O-SIG.
- DISSOC **73,700** = 67 × 1,100, where 1,100 = 200 recipients (2×2 × 50, my §4.1) + 800 donors (4×, my §4.3; R6) + 100 selection (RD). **Mismatch:** this counts retained episodes, not the screening needed to fill balanced cells. Off-diagonal cell probability is 0.167 / 0.127 / 0.072 at agent corr(E, r̄) 0.5 / 0.7 / 0.9, so filling 50 recipients per cell takes ≈ 300 / 395 / 697 screened episodes (run to t_d), and donors ≈ 1,200 / 1,580 / 2,787. Budget up to ≈ 3,830 per seed (≈ 257,000 per arm at 67) or state the bound.
- Addendum quote "in this declared system, intervention and task family" is v1 §4.4 text (v1_RD L102), not Astra: attribute it.

## R39 (§2.3 wording, addendum §2): OBJECT, narrowly
- Quotes verified verbatim: #41 L19, L168, L304 (L304 sits inside quotation marks in the raw text), #42 L55, L223. The name "interoceptive estimate module (candidate internal representation of simulated E/I)" is consistent with my rows (CNA L63). No licence implies "self-model".
- **Objection:** "Q-LEARN MET licenses only: the measured accessibility was acquired through training" overclaims. Under #41 L160–168 and §5.6, "acquired" needs all three conditions; a training contrast alone gives "increased through training". **Fix:** "Q-LEARN MET licenses only 'increased through training' within the tested comparisons; 'acquired' or 'learned' only when all three §5.6 conditions hold (#41 L168)." Optional: add "nor SELF or SIG-ATTR" to the never-licenses-self-model sentence. With that fix: NO OBJECTION.

## ISSUES
- **S-I1 (Lead ruling).** Adopted R2(a) requires C-CAUSE MET at each ρ on MIXED-CODE (v3.1 L1430; addendum L81). That is unreachable by construction: the optimized comparator reaches z_R (erratum E1 arithmetic). **Fix:** restrict it to C-NEC-DEP plus block/direction checks 3a/3b (erratum E1).
- **S-I2 (RD; Astra).** D23 (v3.1 L475) doesn't exclude the target direction from the optimized comparator's search. If the search contains u, "beat the strongest comparator" is unreachable on every plant, CN-P1 included. **Fix:** search the orthogonal complement of the target subspace (or other blocks only), and state it.
- **S-I3 (CNA; fixed in erratum E2).** DL-ATTR exact c-matching is infeasible at R6 pool sizes: P(both donors) ≈ 0.32 < 0.90. Coarsened c_ATTR is in the erratum.
- **S-I4 (RD).** The R26 resource plan omits DISSOC screening load and the diagnostic observer costs (above).

## NOT CHECKED
Line-by-line conformance of the RD body outside the seams; Appendix L/L2 beyond the LP items cited; R21–R25 values; v2.1 by-reference content.

---
sha256 of all content above this line: f5e67976be907506612d202481e8bf07e58034807d14fc451f3d76df241e6aa0
