# Short delta check: C-κ oracle scope record v1.4, against the delta check a70acb05… and the Research Lead's rulings

Research Delegate, 2026-10-22, about 02:12 ET.
- Read-only: nothing was run or propagated, and no checkpoint was touched. This is a new file; no existing file was edited.
- Scope is limited to N1–N4, n1–n5 and manifest items 1, 2, 6, 7, 8, 9, 10, 11 and 12, plus precedence and the immutability of earlier files.
- Line references are to v1.4 unless stated otherwise.

## Hashes (verified)
- **v1.4** `ckappa_oracle_scope_record_v1_4.md`: `160ddfd5825dc36e230b06334d874deee080001dca6de4bff4e49d5b105ba7fb`. This matches the posted sha. The file name is `v1_4.md`, not `v1_4_N.md`.
- **Unchanged:**
  - v1: `1b450bcf231324c6fc3c686cc2daa819ed5f09cd5725c7c3283a1b3e2c39c5bf`
  - v1.1: `e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c`
  - v1.2: `7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d`
  - v1.3: `f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5`

**Precedence (L6): OK.** The order is v1.4 > v1.3 > v1.2 > v1.1, and the verbatim E36-1..14 text governs over everything, including v1.4. I found no v1.4 line that contradicts the E36 verbatim text. N4(ii) was checked against E36-6 in particular; see below.

## Verdict: **PASS WITH NOTES**

There is one gap that should be closed additively before sealing: **B1**, a one-line addition. Everything else is resolved, or is a note that does not block.

## Rulings that now govern (the Research Lead accepted both deviations)

**(a) N3, rcond = 1e-8 instead of 1e-10: CONFIRMED, not material.**
- The bands come from v1.1 L68–71 with E36-8 (v1.3 L51, L96):
  - resolved if σᵢ/σ₁ > 10⁻⁶;
  - zero if σᵢ/σ₁ < 10⁻¹⁰;
  - unresolved in [10⁻¹⁰, 10⁻⁶], endpoints included.
- 10⁻⁸ lies strictly inside that band.
- `numpy.linalg.lstsq` treats a singular value as zero when s < rcond·s_max, where s_max is the largest singular value of the same A. That is exactly the rank rule's σᵢ/σ₁ ratio, so the two definitions match.
- N3 (L31–33) applies the rule to the same √w-weighted design A **before** the fit, and does not score any cell with a ratio in the band. In every fitted cell, therefore, each ratio is either > 10⁻⁶, and kept because it is > 10⁻⁸, or < 10⁻¹⁰, and zeroed because it is < 10⁻⁸.
- Any cutoff in [10⁻¹⁰, 10⁻⁶] truncates identically, so 1e-8 and 1e-10 give the same fit.
- LAPACK's singular values in lstsq (gelsd) and a separate SVD can differ by about ε·σ₁. That cannot matter: a ratio near 10⁻⁸ would already have made the cell unresolved.
- The ruling's "unscored as u" is implemented as UNRESOLVED, not scored, kept in the denominator (L32). That is consistent.

**(b) N4(ii), whole-fixture NOT ADMISSIBLE instead of the 25% rule: stricter, CONFIRMED. "Changes nothing else": REFUTED in one narrow respect, which does not block sealing.**
- *Stricter:* every invalid-baseline pattern that the 25% rule called NOT ADMISSIBLE is also NOT ADMISSIBLE under v1.4. The cases with 1–4 invalid prefixes out of 16 are now NOT ADMISSIBLE too, so the set of admissible outcomes shrinks.
- *Consistent with E36-6:* "Failure of the quadratic to define a valid baseline is reported as RESTRICTED COMPARATOR NOT ADMISSIBLE, not automatically as PIPELINE INVALID. It does not trigger refitting or replacement." That holds here: there is no refit or replacement, and the package continues to O3 (L37).
- *Unaffected:*
  - §5, which is decided by O6 alone (v1.3 manifest item 8);
  - the §6 roll-up (E36-11), which O7 does not enter;
  - package continuation in the case where the baseline is invalid.
- *What does change:* when O7 is voided, its stacked Jacobian is never evaluated, so the integrity stop in N4(i) (a resolved σ₃/σ₁ > 10⁻⁶ means STOP, PIPELINE INVALID) cannot fire.
  - Under the 25% rule, with 1–4 invalid prefixes, the valid prefixes would have been evaluated, and an implementation bug could still have triggered a STOP.
  - Under v1.4 the package continues in that case.
  - So v1.4 is stricter about admissibility but slightly *less* sensitive as an integrity check.
- *Why this does not block:* O7 is exploratory (E36-6), and an implementation contradiction is only required to stop the run when it is "demonstrated" (Astra's note after E36-7). The required integrity fixtures are O1, O2 and O6.
- *Optional, non-blocking:* report σ₁…σ₃ of the Jacobian at the valid prefixes even when O7 is voided. This would be descriptive, with no stop.

## Per-item status
| Item | Status | Note |
|---|---|---|
| N1 vocabulary and precedence | RESOLVED, with **B1** | L9–18: first match wins, in the order PIPELINE INVALID > COVERAGE NOT MET > ZERO RESPONSE > HEADROOM NOT MET > BOUNDARY > MET/AVAILABLE. The integer test 4·n_s < 3·n_t is exactly n_s/n_t < 0.75: 96/128 gives 384 vs 384, so not below, so it passes and is not BOUNDARY (L17). Law mass uses the float band, and the gap between 0.75(1 − 10⁻⁶) and 0.75 falls into BOUNDARY, so the order is consistent with E36-4. **B1:** an O6 fold whose design is rank-UNRESOLVED (N3, L32) has no §5 label. |
| N2 application before seal | RESOLVED | L20–28 conform exactly to the ruling: the application cites the scope, code and input hashes, its sha goes into the manifest, then the seal. Nothing is circular (L28). |
| N3 rank before fit and rcond | RESOLVED; deviation accepted | See (a). |
| N4(i) σ₃ stop | RESOLVED | L36 conforms: > 10⁻⁶ means STOP, PIPELINE INVALID, no rerun. A ratio in the band reads UNRESOLVED and the package continues. |
| N4(ii) granularity | RESOLVED; deviation accepted | See (b). |
| N4(iii) own baseline | RESOLVED | L38 matches E36-6. |
| n1 L138 label | RESOLVED | L43 |
| n2 L142–147 labels, owed rules | RESOLVED | L44–46 |
| n3 reserve | RESOLVED | L48–53: HALT if T_rem > 540 − T_elapsed; soft stop at 540 s; hard kill at 600 s. The three stop kinds are distinct. Note N-a below. |
| n4 wrapper | RESOLVED | L55–59: T0 is recorded by the wrapper before Python starts, and the environment, prlimit, taskset and timeout are set outside Python, satisfying E36-14. Stage files are fsynced as they complete. Note N-a below. |
| n5 memory | RESOLVED | L62 and L57 `--as=4000000000` |
| NumPy pin and array hashes | PARTIAL (N-b) | L65: the version is asserted at startup. The ruling said hashes of Q, Q₂ and the directions go to the outputs. v1.4 instead hashes the `.npz` archive in the post-run index. |
| seed_id | RESOLVED, not material | L66: 36000 + 100…109 = 36100–36109. This is how I read the ruling's "seed id itself (100–109)": the seed_id is the PR #7 seed number, so the generator seeds are 36100–36109. It is §6 only, so it does not touch the oracle seal. |
| Field names, paths | RESOLVED | L67–74 |
| Manifest item 1 | RESOLVED | L77 |
| Item 2 | RESOLVED | L78 |
| Item 6 | PARTIAL | See N-b. |
| Item 7 | RESOLVED | L80; once B1 is fixed, its label belongs here too. |
| Item 8 | RESOLVED | L81 |
| Item 9 | RESOLVED | L82, plus N-a. |
| Item 10 | RESOLVED | L83 |
| Item 11 | RESOLVED | L84 |
| Item 12 | RESOLVED | L85 |

## Issues
- **B1 (fix before seal: one additive line).** N3 makes an O6 cell UNRESOLVED and unscored if its design's σ ratio lies in the unresolved band. N1 has no outcome for that case, and "pooled H\*" is undefined over a partly unscored set of folds.
  - Proposed fix: insert into N1, between steps 2 and 3, **"REFERENCE RANK UNRESOLVED: any fold's O6 B or B_μ design is rank-UNRESOLVED; no pooled §5 statistic is formed."**
  - This is unlikely to occur, because the oracle's L is structurally full rank, but it is otherwise an unhandled §5 path that would invite improvisation (Astra L115).
- **N-a (note).** The post-run index is written by the wrapper after a SIGKILL at 600 s, so strictly it falls outside the 10-minute interval that E36-14 says "includes final serialization and report writing". Suggestion: set the timeout to 595 s minus the elapsed time, leaving a 5 s margin for the index. The work involved is milliseconds; it does not block.
- **N-b (note).** `np.savez` writes zip members with the current timestamp: NumPy 2.5.4 `_npyio_impl.py` L785 calls `zipf.open(fname,'w')`. The `.npz` sha256 therefore certifies the file but is not reproducible from the array contents. To match the ruling as stated, also write sha256 over each array's C-order float64 bytes, with its shape and dtype, into `results.json`. Not blocking.

## Claim ceiling
Unchanged: oracle-only (L88). Nothing runs until the application is filed and the manifest is sealed.
