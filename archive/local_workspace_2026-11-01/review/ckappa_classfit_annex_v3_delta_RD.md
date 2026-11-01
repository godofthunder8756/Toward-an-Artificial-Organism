# Delta check: C-κ class-fit implementation annex v3 (Research Delegate)

**Status: DRAFT REVIEW RECORD. NOTHING RUNS.** It establishes no result. The claim ceiling is E38-15.

- **File:** `review/ckappa_classfit/ckappa_classfit_implementation_annex_v3.md` at PR #14 HEAD `11efb513`. It was added in commit `11efb51`.
- **Method:** static reading only. I imported `ckappa_classfit.pinned` alone to read its constants. No stage, wrapper, fit or simulation was run. Nothing was posted.
- **Date:** 2026-10-23, about 09:00 ET.
- **Companion review:** `/workspace/review/ckappa_pr14_code_review_RD.md`.

## Verdict: CLEAR WITH NOTES

The annex is correctly identified, cited and superseding. Its RL-1 to RL-4 text matches the code. Its RL-5 text states the ruling correctly, but the code only partly meets it (code review B-6). That is a code defect, not an annex-text defect. The annex makes no change to the estimator, controls, masks, thresholds, directions, sizes, caps or claim ceiling beyond what the RL rulings order.

## 1. Identity and citations

| Check | Result |
|---|---|
| sha256 of annex v3 | `435453e0917d1d4d3f2c50c4cc8dc469d6487147f8dd987fd53eb877ac5cb8bd` ✓ (equals the expected value and the manifest entry) |
| Cites v1.3 | "Binds to: … v1_3.md, sha256 `a17e133d…e318`" ✓ |
| Cites annex v2 | "Annex v2 sha256 `5d6daf06…7262`" ✓ |
| Supersedes v2 by name | "Supersedes: `ckappa_classfit_implementation_annex_v2.md` by name … retained byte-identical" ✓ |
| Cites annex v1 | `8614bf11…` stays byte-identical ✓ |
| Precedence | #39 `e6403b63…` > #38 `87fd77e0…` > #37 `ce010fdb…` > v1.3 > annex v3. "Where this annex and v1.3 conflict, v1.3 governs" ✓ |
| Own sha omitted | Yes. It is recorded in the draft manifest ✓ |
| Implementation commit | `12b816ef…`. The commit adding the annex (`11efb51`) changes no module bytes ✓ (`git diff 12b816ef 11efb513` touches only the manifest and annex v3) |
| A8 table | 23 rows. All equal the bytes at HEAD and the manifest `implementation_files` ✓ |

**Byte-unchanged files at 11efb513 (vs b4c03502 and the box copies).**
- v1.3 `a17e133d…`
- annex v1 `8614bf11…`
- annex v2 `5d6daf06…`
- #39 `e6403b63…`
- #38 `87fd77e0…`
- #37 `ce010fdb…`

All are unchanged ✓. The only file added under `review/` is annex v3.

## 2. RL sections against the code

**RL-1. Matches the code.**
- `rho_nc1_exact_law` has no void, admissibility or ledger argument and requires length 16.
- It asserts the exact Σ = 1, converts P_a to float once, and sums sequentially over a = 0..15.
- It is called after `_refit_nc1` and before NC1 voids or admissibility exist.
- **Note A1.** The S3 `rms` record does not include `P_a_float`. The annex's list of fields does not claim it, so this is consistent, but the earlier checklist asked for it.

**RL-2. Matches.** `first_reverse_mismatch` is written once, never overwritten, does not stop, and carries the L40 fields with nulls where data are missing.

**RL-3. Matches.** D6 status is a premise status only (the annex table equals `_d6_premise_status`). The tolerances are null. The PASS/FAIL/INVESTIGATE walk ends in INTEGRITY STOP. D6 stays outside the labels. INVESTIGATE is used only by D7.

**RL-4. Arithmetic verified.**
- Added records: 420 + 1,064 (112 + 112 + 840) + 30 = 1,514.
- 1,514 × 2,048 = 3,100,672 and 1,514 × 4,096 = 6,201,344.
- Rows 1–5 and 8: 7,594,768. Check: 7,594,768 + 23,026 × 6,144 = 149,066,512, which is v2's I.
- Row 6 is 24,540 × 2,048 = 50,257,920. Row 7 is 24,540 × 4,096 = 100,515,840.
- I = 158,368,528 and I × 2 = **316,737,056**. This equals `pinned.PACKAGE_BUDGET_BYTES`. It also equals the 298,133,024 analytic base plus 18,604,032.
- Feasibility condition: VmPeak ≤ 3,683,262,944 ✓.
- B0 is VmPeak 59,170,816 B (57,784 kB × 1024). 59,170,816 + 316,737,056 = 375,907,872 ✓.
- S0 compares `vmpeak + budget > 4e9` and gives INTEGRITY STOP. RSS is context only ✓.
- The `__main__` exclusion is justified: its body runs `main()`. It is hashed in A8 (`f03238fb…`) ✓.
- **Note A2.** I cannot reproduce B0 on the box (Python 3.13.5 / NumPy 2.5.4). It is UNVERIFIED by me. The build string "3.12.3 (main, Aug 31 2026, GCC 13.3.0)" should be checked against the run host when the approved run is made. B0 is recorded as context, and S0 re-measures it live, so a mismatch here cannot weaken the gate.
- **Note A3.** The label-record count of 30 treats HEADROOM as one record containing both gates, as the code does. Counting 31 changes I×2 by 12,288 B, which is immaterial.

**RL-5. Text correct; code partial.**
- The annex correctly states the ruling, and that `check_outputs_directory` runs "before `Run` creates the directory".
- It does not mention that the PackageStop handler then writes `results.json`, `REPORT.md`, `run.log` and `stop_kind.json` into that same non-empty directory (`driver.py:188–190` → `_write_pair`).
- The wrapper's post-run block also writes. Symlinks are followed.
- So the stated property ("absent or empty, or INTEGRITY STOP") holds for computation but not for writes. This is code review **B-6**. Annex v4 should record the fixed behaviour.
- The re-hash table (manifest `4179b71a…` + 15 `outputs/*`) matches the committed bytes. Each row has `stops: false` ✓.
- **Note A4.** The oracle `post_run_index.json` (`7825c536…`) is not re-hashed. That is optional under the ruling text.

**CR-2. Unchanged ✓.** The NC1 refit still uses the inherited float P_a accumulation (`_refit_nc1` is untouched by the delta). The RMS rule uses exact-law P_a converted once.

## 3. Other notes

- **A5. Attribution.** Annex v3 attributes the rulings to the Research Lead and does not name its own author. Annex v2's retained header still says "Research Delegate (Track A) … carried forward", but the RD did not write annex v2. Annex v2's bytes must not be edited. Annex v4, or the seal record, should state who wrote v2 and v3.
- **A6. Carried annex v2 design readings are not re-ruled.** Annex v3 carries annex v2's A9 literal readings unchanged. These include CI-NC-ONE-VOID, the HEADROOM MARG word and missing band, the CI-EXIT-CODES pairing and CI-B3-SHORT-STACK = PASS. Code review B-1 to B-3 and M-11 still apply. Annex v3's statement that it "may not change the estimator, controls, …" is true of v3 itself. The v2 readings remain unratified (L175) and need revert or ruling before seal.
- **A7. Stale manifest string (CNA note 2, agree).** The annex v1 `items.governing` role reads "superseded by annex v2 once that file exists". Fix it at seal. A8 is unaffected.
- **A8. Fallback (CNA note 1, agree; major).** `driver.py:110–113` falls back from annex v3 to v2 silently. The annex's A8 "Manifest field names" table should require the annex v3 entry, and S0 should integrity-stop if it is absent.
- **A9. `_guard_detail` cost (CNA note 3, agree).** The annex does not mention the extra per-event work. There is no change in results. Timing is NEEDS-APPROVED-RUN.
- **A10. "What was executed."** The annex discloses `py_compile`, `static_checks` on hand-made fixtures, and one import-only B0 process authorized by RL-4 option (b). This is consistent with E39-1 and with "no stage S0–S8".

## 4. Summary

| Item | Ruling |
|---|---|
| Identity, citations, supersession | CLEAR |
| RL-1 to RL-4 text vs code | CLEAR (notes A1–A3) |
| RL-5 text vs code | NOTE: code is partial (code review B-6) |
| Design changes made by v3 itself | None found |
| Carried v2 readings | NOT ratified (A6). They are blockers in the code review, not in this delta |
