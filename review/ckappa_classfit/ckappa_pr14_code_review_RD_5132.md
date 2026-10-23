# C-κ class-fit PR #14: adversarial code review (Research Delegate)

**Status: DRAFT, NOT FROZEN, NOTHING RUNS.** This is a review record. It establishes no result. The claim ceiling is E38-15.

- **PR:** https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/14 (draft, open). Branch `cursor/ckappa-classfit-synthetic-v1-4df8`.
- **Reviewed HEAD:** `11efb513faa2a9ec825583744ffc195b15ec60e1`. Implementation commit `12b816ef0b72409d5baf0875d5acab00f9c78676`.
- **Earlier pass:** HEAD `b4c03502` (implementation commit `315d9da9`). Every finding below is re-stated at `11efb513` and marked **FIXED**, **STILL OPEN** or **NEW**.
- **Clone:** `/workspace/scratch/pr14`, a fresh scratch clone. `/workspace/repo` was not touched. Nothing was posted on GitHub and nothing was pushed. No committed file was edited.
- **Date:** 2026-10-23, written about 09:00 ET.

**Governing precedence (raw text governs).** #39 raw `e6403b63…` > #38 raw `87fd77e0…` > #37 raw `ce010fdb…` > v1.3 `a17e133d…` > annex v3 `435453e0…` (which supersedes annex v2 `5d6daf06…` by name) > annex v1 `8614bf11…`. RL-1 to RL-5 are implementation rulings recorded in annex v3.

## 0. Verdict

**BLOCKERS. On the earlier READY scale this is NOT READY.**
- RL-1 to RL-4 are implemented as ruled. RL-5 is only partly implemented: the S0 check exists, but it does not protect the directory (NEW B-6).
- Earlier blockers B-1 to B-5 are **STILL OPEN**. The delta does not touch the code they concern.

| ID | Finding | Status at 11efb513 |
|---|---|---|
| B-1 | NC1/NC2/NC3 admissibility: one void makes the system inadmissible | STILL OPEN |
| B-2 | HEADROOM drops the inherited law-mass BOUNDARY band; the MARG word | STILL OPEN |
| B-3 | Exit-code and stop-kind pairing; INTEGRITY STOP is labelled NOT EVALUATED | STILL OPEN |
| B-4 | Inherited `ckappa_oracle` code is not in the manifest and is not re-hashed | STILL OPEN |
| B-5 | The application file is not hashed (C8.6) | STILL OPEN |
| B-6 | RL-5: a non-empty or symlinked `classfit_outputs/` still gets overwritten by the stop path | **NEW** |
| M-1 | Governing set is not required by sha; annex detection is hard-coded and falls back silently | STILL OPEN (it now falls back from v3 to v2) |
| M-2 | Inadmissibility skips are assigned eagerly at S3 | STILL OPEN |
| M-3 | No Σ ATTEMPTED cross-check against run counters | STILL OPEN |
| M-4 | S7 pooling runs after a stop; unreached systems are labelled NOT ADMISSIBLE | STILL OPEN |
| M-5 | HEADROOM labels any unformed row ZERO RESPONSE | STILL OPEN |
| M-6 | Coverage masks rank (needs an RL note) | STILL OPEN (RL note) |
| M-7 | `guard_invalid` subcount is never populated | STILL OPEN |
| M-8 | A streaming stop loses the partial `eval_<system>.json` | STILL OPEN |
| M-9 | No SYS-NC2 D5 descriptive record | STILL OPEN |
| M-10 | The P0 domain sets are not serialized, although the flag says they are | STILL OPEN |
| M-11 | B3 short stack returns PASS (unreachable) | STILL OPEN |
| CR-1 / RL-2 | Reverse guard record | **FIXED** |
| CR-3 / RL-3 | D6 PASS/FAIL | **FIXED** |
| CR-4 / RL-4 | B0 and memory budget | **FIXED** (B0 value UNVERIFIED by me) |
| CR-5 / RL-5 | Output directory and oracle re-hash | **PARTLY FIXED**; see B-6 |
| RL-1 | ρ_NC1 domain | **FIXED** (it was already effectively satisfied; it is now explicit and recorded) |
| N-1 | `_guard_detail` builds its record on every call (runtime cost) | **NEW**, note |
| N-2 | Stale annex v1 role string in `items.governing` | **NEW**, note |

## 1. Identity and delta

**Committed governing copies at 11efb513 are byte-identical to the box files and to b4c03502.**

| File | sha256 |
|---|---|
| v1.3 | `a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318` |
| annex v1 | `8614bf114b127f4bdab516c0e933c23c84d1cd5f4d0ef34837d5cb0ad453d3a8` |
| annex v2 | `5d6daf06fea3466ff2fc1eebf73414f12c47daeccfe06095ec7a3efb64907262` |
| annex v3 (new) | `435453e0917d1d4d3f2c50c4cc8dc469d6487147f8dd987fd53eb877ac5cb8bd` |
| #39 raw | `e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482` |
| #38 raw | `87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5` |
| #37 raw | `ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2` |

**Sealed oracle artifacts are unchanged.**
- `manifest.json` is `4179b71a…`.
- `post_run_index.json` is `7825c536…`.
- All 15 `outputs/*` files equal `pinned.ORACLE_SEALED_OUTPUT_SHA256`, which I recomputed from the bytes.
- `ckappa_oracle/` has no diff from b4c03502 to 11efb513.

**Delta b4c03502..11efb513.**
- There are two commits. `12b816e` applies RL-1 to RL-5. `11efb51` records annex v3.
- The delta changes the following package files: `aggregate.py` (comment only), `construction.py`, `driver.py`, `evaluate.py`, `fits.py`, `pinned.py`, `preflight.py`, `report.py`, `static_checks.py` and `run_classfit_package.sh`. It also changes `classfit_manifest.json` and adds annex v3.
- **12b816ef..11efb513** touches only `classfit_manifest.json` and annex v3. `git diff --quiet` over `ckappa_classfit/`, the wrapper and `ckappa_oracle/` is empty.
- All 23 manifest implementation shas match the bytes at HEAD. The 23 A8 rows in annex v3 match the same bytes. Every manifest governing sha, including annex v3, matches.

## 2. Static-checks decision

- Allowed this round: static reading and import-only checks.
- I ran `py_compile` with the cfile in `/tmp` on all `ckappa_classfit/*.py`, and `bash -n` on the wrapper. Both passed.
- I imported `ckappa_classfit.pinned` alone (constants only) to read the RL-4 integers: `LABEL_RECORDS` 30, added records 1,514, `INCREMENTAL_BYTES` 158,368,528, `PACKAGE_BUDGET_BYTES` 316,737,056.
- I did **not** re-run `static_checks` at this HEAD. The new version calls package functions (`rho_nc1_exact_law`, `_d6`) on toy fixtures and creates temporary directories. That is beyond import-only. Its result at b4c03502 was "static checks passed", on the box's non-pinned Python 3.13.5 / NumPy 2.5.4.
- No stage S0–S8, wrapper, fit, solve, propagation or simulation was run.

## 3. Blockers (fix before seal)

### B-1. NC admissibility (CI-NC-ONE-VOID). STILL OPEN

**Where.** `construction.py:260–265`. Any single void makes SYS-NC1, SYS-NC2 or SYS-NC3 inadmissible.

**Why it is wrong.** v1.3 C7.1 item 5 reads "≥5 of 16 prefixes voided, **or** a matched baseline invalid". C3.9 and the inherited ≥5 rule are the void criterion.

**Fix.**
- SYS-NC1: `admissible = len(voids) < 5`.
- SYS-NC2 and SYS-NC3: inadmissible iff a matched baseline is invalid (C4.4.R).
- At `construction.py:~145`, the per-prefix void row label should read `VOIDED`, not `RESTRICTED COMPARATOR NOT ADMISSIBLE`.

**Practical effect.** The committed oracle `stage_O7.json` has voided_count 0, so the effect is probably nil. That is UNVERIFIED.

### B-2. HEADROOM gates (CI-HEADROOM-MET-LABEL). STILL OPEN

**Where.** `aggregate.py:437–484` (`_headroom_one`). The inherited law-mass BOUNDARY band (`ckappa_oracle/outcomes.py`, mass_band → BOUNDARY) is missing, so MET can be awarded where the inherited rule gives BOUNDARY.

**Fix.** Add the reference-size fold/class law-mass in-band test, returning BOUNDARY.

**NEEDS RL RULING.** `aggregate.py:20–21` uses "MET" for MARG, where the inherited word is "AVAILABLE". RL must also say which group licenses the C7.4 success sentence (`report.py` success logic).

### B-3. Exit codes and labels (CI-EXIT-CODES). STILL OPEN

**Where the pairing breaks.** These raise kind `PIPELINE INVALID` with exit 7:
- `p0.py:23`
- `construction.py:220` (normalization)
- `evaluate.py:467` (guard)

**Where the label breaks.** `aggregate.py:324–329` and `373–378` label INTEGRITY STOP as "NOT EVALUATED". C7.1 item 1 puts C8.6 integrity conditions, P0, B3, crossing, NC1 refit, normalization and guard inconsistency under PIPELINE INVALID.

**Uncaught errors.** `accounting.py:35–42` (Ledger) and `schedule.py:96–114` raise `ValueError`, `KeyError` or `RuntimeError`, which become EXECUTION ERROR, exit 1.

**Fix.**
- Pair kind with exit exactly as inherited: INTEGRITY STOP ⇔ 7 (`io.py`) and PIPELINE INVALID ⇔ 2 (`stages._fail`).
- P0 (v1.3 C4.0 says exit 7) must use `integrity_stop` with detail label `PIPELINE INVALID (P0)`.
- Normalization: use `integrity_stop` (inherited analogue `stages.py:326`) with label `PIPELINE INVALID (normalization)`.
- Guard inconsistency: use (PIPELINE INVALID, 2). It is operational and not in C8.6. RL may choose 7 instead, but then the kind must be INTEGRITY STOP.
- S7 maps both kinds to label `PIPELINE INVALID` and VALIDATION `NOT MET (PIPELINE INVALID)`, with the check named.
- Ledger and schedule errors become `integrity_stop` (C8.4/C8.6). Move `schedule._check` into S0.

### B-4. Inherited code is not hashed. STILL OPEN

**Where.** `preflight.py:196–235` re-hashes only `ckappa_classfit/*.py` and the wrapper.

**Fix.**
- Add `ckappa_oracle/{__init__,io,pinned,world,geometry,linalg_fit}.py` to `items.implementation` with their shas: `45f848b1…`, `b1795bcc…`, `03c55323…`, `3d235fca…`, `117e98e9…`, `de6f4034…`.
- Re-hash them at S0.
- Assert that no other `ckappa_oracle.*` module is in `sys.modules`.

### B-5. Application not hashed. STILL OPEN

**Where.** `preflight.py:183–190` checks the format and status only. C8.6 says a hash mismatch of "the application against the sealed manifest" is INTEGRITY STOP.

**Fix.** Hash `application.path` and compare it to `application.sha256`. A mismatch or missing file is INTEGRITY STOP.

### B-6. RL-5 does not protect the output directory. NEW

**What the check does.** `preflight.check_outputs_directory` (`preflight.py:61–79`) runs first in `preflight` and correctly integrity-stops on a non-empty directory.

**What happens next.** `driver.main` (`driver.py:188–190`) catches that stop and calls `_write_pair(None, …)` (`driver.py:68–92`). That call writes `results.json`, `REPORT.md`, `run.log` and `stop_kind.json` **into the non-empty `classfit_outputs/`**, overwriting a prior run's files.

**Other write paths.**
- The wrapper's post-run block (`run_classfit_package.sh:32–33` and later) `mkdir`s the directory and unconditionally replaces `classfit_post_run_index.json`.
- `__main__._thread_stop` (`__main__.py:9–36`) writes before preflight.

**Symlinks.** `exists()` and `is_dir()` follow symlinks, so a symlink to an empty directory reads as `empty` and the run writes through it. A dangling symlink reads as `absent`.

**Effect.** The ruling's purpose (no mixing or overwriting of earlier outputs) is not achieved.

**Fix.**
1. Before any write in `__main__`, `driver` and the wrapper, refuse if `classfit_outputs` is a symlink (`is_symlink()`), resolves outside ROOT, is not a real directory, or is non-empty. Use `os.lstat`.
2. On that refusal, write nothing to `classfit_outputs/`. Print the stop to stderr and exit 7.
3. The wrapper must also check before launch and skip its post-run writes when the pre-check failed.
4. Apply the same rule to an existing `classfit_post_run_index.json`.

## 4. Majors

| ID | Where | Fix |
|---|---|---|
| M-1 | `driver.py:95–113`, `preflight.py:223–235` | Assert that the governing list contains the required set by **exact path and sha**: #39, #38, #37, v1.3, annex v3, v2 and v1, plus #36 raw and the oracle governing set needed by C9.2. A missing annex v3 entry must be INTEGRITY STOP, not a silent fall back to v2 (see CNA note 1). Cross-check `items.inputs` against the pinned constants. |
| M-2 | `construction.py:71–74` | Assign SKIPPED_SYSTEM_INADMISSIBLE at that system's S5/S6 point, so that a preceding stop takes priority (E39-7). |
| M-3 | completion path | Assert Σ ATTEMPTED equals `run.float_count`, `exact_count` and `svd_count`. A mismatch is INTEGRITY STOP. |
| M-4 | `driver.py:213–232`, `aggregate.py:86–95` | After a stop, mark pooled rows unformed with reason PRIOR STOP / NOT_REACHED. Do not set `admissible=False` for systems that were never constructed. |
| M-5 | `aggregate.py:452, 458` | Map `not_formed_reason` to its own status instead of ZERO RESPONSE. |
| M-6 | `aggregate.py:158–182, 334–338` | Coverage counts cells whose maps are unavailable, so REFERENCE COVERAGE NOT MET masks REFERENCE RANK UNRESOLVED. The inherited oracle uses resolved folds only. v1.3 C7.1 order is literal (CI-PARTIAL-MASK ACCEPT). This is an RL note, not a code defect. |
| M-7 | `evaluate.py` / `accounting.py:27` | Populate the `guard_invalid` subcount (C8.4). |
| M-8 | evaluate stop path | Write the partial `eval_<system>.json` before re-raising (C7.0). |
| M-9 | `fits.py` (NC2) | Add the descriptive D5 records for SYS-NC2 (v1.3 premise table, C4.4). |
| M-10 | `p0.py:131–134` | Serialize `p0_domain_pairs` to `stage_S4_P0.json` before the comparisons, or drop the `domains_recorded_before_comparisons: True` flag (E39-10). |
| M-11 | `rankcats.py:66–67`, `static_checks.py:52` | A short stack must be INTEGRITY STOP on the shape invariant, never PASS. The stack is (48·n_fit)×8, so this is unreachable. |

**Minors (unchanged from the earlier pass).**
- `arrays.py:315–317`: the dtype/order check is vacuous.
- `gradient @ gradient` should be written explicitly as `gx*gx+gy*gy`; it now lives in `rho_nc1_exact_law`.
- The B3 `rank_category` field is confusing.
- XOR zero-gain rows are excluded from VALIDATION.
- UNRESOLVED-B3 is not surfaced in the labels.
- The wrapper does not set `CUDA_VISIBLE_DEVICES`.
- The wrapper's UNKNOWN marker applies only for exit 124/137.
- Zero-gain checks use weighted mode only.
- `requirements.txt` is unpinned, and the BLAS build is not recorded at S0.

**FIXED minor.** The S3 `rms` payload dropped `P_a_float`. `rho_nc1_exact_law` still returns `P_a_float`, but the S3 `rms` key list at `construction.py:~520` still omits it. That makes this **STILL OPEN** (minor): add `"P_a_float"` to the list.

## 5. CI / CR verdicts at 11efb513

Unchanged from the earlier pass unless marked.

**ACCEPT:**
- CR-2 (re-verified, unchanged)
- ACCOUNTING-ATTRIBUTION
- JOINT-PREMISE-TIMING
- EMPTY-FIT-CATEGORY
- LOWER-RESIDUAL
- PARTIAL-MASK (see M-6)
- BASELINE-TOLERANCE
- SCHEDULE-KEY
- T0-ENV
- MANIFEST-PHASE
- NC1-FINITE-EQ-CELLS
- LAW-MASS-BOTH-MODES
- GOVERNING-PATH
- LABEL-INADMISSIBLE
- RESULTS-WRITE-STAGE
- APPLICATION-PENDING (+B-5)
- MANIFEST-ITEMS-SHAPE (+B-4, M-1)
- GLOBAL-AGGREGATES
- SINGLE-PREFIX
- CANCELLATION-DIAGNOSTIC
- MU-RECOVERY-PREMISE

Moved to ACCEPT at this HEAD (now FIXED): CR-1 (RL-2), CR-3 and D6-A-INSIDE-ONE-CELL (RL-3), CR-4 (RL-4).

**REPLACE:**
- CR-5 (RL-5): B-6.
- ATTEMPTED-DETAIL: M-7.
- UNFORMED-VS-ZERO: add explicit `formed` and `not_formed_reason` to base loss records.

**The hard four, in full:**
- **CI-B3-SHORT-STACK. REPLACE.** `rankcats.py:66–67` returns PASS when fewer than 3 σ exist. Required: INTEGRITY STOP on the shape invariant. If RL prefers not to stop, use UNRESOLVED-B3. It is never PASS. Update `static_checks.py:52`. Unreachable for a formed stack. STILL OPEN.
- **CI-NC-ONE-VOID. REPLACE.** As B-1. This changes a control/admissibility rule without an Astra or RL ruling, so it must be reverted to the C7.1 item 5 text. STILL OPEN.
- **CI-EXIT-CODES. REPLACE.** As B-3. INTEGRITY STOP must be exit 7, PIPELINE INVALID keeps exit 2, and the PIPELINE INVALID label scope (C7.1 item 1) is inherited and covers integrity stops. STILL OPEN.
- **CI-HEADROOM-MET-LABEL. REPLACE (gates) + NEEDS RL RULING (MARG word).** As B-2. STILL OPEN.

**NEEDS RL RULING:**
- HEADROOM MARG word.
- LIM-SIGNS and LIM-BASELINE-BOUNDARY. Recommendation: compute the signs with exact rationals; a mismatch or sign 0 is INTEGRITY STOP.
- REPRESENTATIVE-MU. Recommendation: INTEGRITY STOP if false.

## 6. RL-1 to RL-5 against the code

### RL-1. ρ_NC1. CONFORMS

`construction.py:201–253` `rho_nc1_exact_law(coef, mu_x, mu_y, p_a_exact)` takes no void, admissibility, run or ledger argument.
- It requires length 16, otherwise INTEGRITY STOP.
- It asserts the exact Σ = 1 before any float conversion. Failure is the normalization stop; see B-3 for its kind and exit.
- It converts P_a once to float, uses a sequential sum over a = 0..15, and uses the inherited `g_gradient` on the refit coefficients.
- It is called at `stage_s3` (~line 376) right after `_refit_nc1` and before SYS-NC1's chart, voids and admissibility.
- The S3 record carries `n_prefixes`, `prefix_domain`, the independence flags, `e39_7_skip_applied` false and `unit`. `P_a_float` is omitted (minor above).

### RL-2. Reverse guard record. CONFORMS

`evaluate.py:425–472`.
- `first_reverse_mismatch` is set once, on the first actual-invalid, predictor-valid event, and is never overwritten.
- It carries `edit`, `min_p_actual`, `min_p_predicted`, `chart_diff_max_abs` and `recovery_residual_max_abs`, each null when missing.
- It does not stop. It is emitted beside `first_mismatch` in the guard rows (`evaluate.py:~799`).
- The forward stop is unchanged. Its kind and exit are under B-3.
- See N-1 for the runtime cost.

### RL-3. D6. CONFORMS

`fits.py:386–454`.
- Status is one of UNAVAILABLE, REFERENCE_RANK_UNRESOLVED, NOT_APPLICABLE_RANK, NOT_EVALUATED or REPORTED.
- `tolerance_abs` and `tolerance_rel` are set to null after `_identity` (which would otherwise set `RECOVERY`).
- A recursive walk integrity-stops on any PASS, FAIL or INVESTIGATE value or key. I checked that no field `_identity` produces for D6 can hold those strings, so this walk cannot false-fire.
- D6 is excluded from label `identity_status` (`aggregate.py:199–201`). D7 alone keeps INVESTIGATE.
- `n_tested` is 1 or 0. No PASS or FAIL for D6 remains anywhere in the non-test code.

### RL-4. Memory. CONFORMS (B0 value UNVERIFIED)

**My recomputation of the budget.**
- Added records: 420 + 1,064 (112 + 112 + 840) + 30 (28 label rows + 1 VALIDATION + 1 HEADROOM record holding both gates) = 1,514.
- Added row 6: 1,514 × 2,048 = 3,100,672. Added row 7: 1,514 × 4,096 = 6,201,344.
- Rows 1–5 and 8: 7,594,768. Check: 7,594,768 + 23,026 × 6,144 = 149,066,512, which is annex v2's I.
- New I = 7,594,768 + 24,540 × 6,144 = 158,368,528. I × 2 = **316,737,056**. This equals `pinned.PACKAGE_BUDGET_BYTES` (import-only).
- The analytic base is 2 × 149,066,512 = 298,133,024 (the "~298 MB"). The additions are 2 × 9,302,016 = 18,604,032. The sum is 316,737,056 ✓.
- My earlier count of 31 label records assumed separate ALL and MARG HEADROOM records. The code and annex use one HEADROOM record. That difference is 12,288 B and immaterial. I accept 30.

**B0.** VmPeak 57,784 kB = 59,170,816 B. 59,170,816 + 316,737,056 = 375,907,872 ≤ 4e9, a margin of about 3.62e9.
- Measured import-only on Python 3.12.3 / NumPy 1.26.4 with the wrapper settings, as stated in annex v3.
- **UNVERIFIED by me:** the box has 3.13.5 / 2.5.4. The recorded `sys.version` build string ("Aug 31 2026, GCC 13.3.0") is unverifiable here.

**S0 code.** `preflight.py:~84–140`.
- `read_address_space` parses `VmPeak` as `<n> kB` × 1024. A malformed value gives None, which is INTEGRITY STOP.
- `address_space_exceeds(vmpeak, budget, cap)` returns `vmpeak + budget > cap`, with cap = `FROZEN_RUNTIME["memory_bytes"]` = 4e9. True gives INTEGRITY STOP.
- **RSS (VmHWM, VmRSS, ru_maxrss) is recorded as context only and is not an operand** ✓.
- It runs after all package imports, at the end of preflight and before any class-fit computation ✓. The annex constant is not reused in place of the live VmPeak ✓.

**`__main__` exclusion: justified.** `__main__.py` ends with `from ckappa_classfit.driver import main; raise SystemExit(main())`, so importing it would execute S0–S8. Its only other imports (os, sys) and `driver`'s transitive imports are covered by the other modules. It is hashed in A8 and in the manifest (`f03238fb…`, bytes unchanged since 315d9da9) ✓.

### RL-5. Output directory and oracle re-hash. PARTLY CONFORMS

- **S0 assertion:** present, but undermined by B-6.
- **Post-run re-hash:** present and matches the ruling.
  - The wrapper hashes `manifest.json` (expected `4179b71a…`) and the 15 `outputs/*` files against `pinned.ORACLE_SEALED_*`. I recomputed all 16 expected values from the committed bytes: all match.
  - Each row is `{sha256, expected_sha256, match, stops: false}`.
  - Errors are recorded and do not stop.
- Note: the oracle's `post_run_index.json` (`7825c536…`) is not in the re-hash list. I suggest adding it, though the ruling names only the manifest and `outputs/`.

## 7. Clause trace

These are unchanged from the earlier pass and still OK at this HEAD:
- E39-2 order.
- E39-3 streaming, `n_tested` and NOT EVALUATED.
- E39-4 one-directional stop, now with a reverse record.
- E39-6: 16,128 base loss records and no single-prefix fits.
- E39-7 precedence (except M-2).
- E39-8 categories.
- E39-9: exact P_sum, a single float conversion, sequential sums.
- E39-10 array provenance (except M-10).
- E39-11 wording.
- Caps: prlimit 4e9, `taskset -c 0`, KILL at 595 − elapsed, 540 s soft deadline, projection, no retries.
- E38-15 strings verbatim.
- Accounting closure by construction.
- Distinct output paths.

The new REPORT sentences (RL-2, RL-3) add no claim.

## 8. Pins and environment

- Preflight enforces Python 3.12.3 and NumPy 1.26.4 (INTEGRITY STOP), one thread, affinity {0}, RLIMIT_AS soft = hard = 4e9, and the absence of GPU modules. It now also enforces VmPeak + budget ≤ 4e9.
- The wrapper uses `python3` from PATH, so the version check is the only guard.
- The box (3.13.5 / 2.5.4) is not the run environment. Preflight would integrity-stop there, which is the correct fail-closed behaviour.

## 9. Independent ruling on the CNA notes

I finished my own checks before comparing with CNA.

1. **`_stage_s0` falls back from annex v3 to v2 (`driver.py:110–113`). AGREE, and raise it to a major (part of M-1); not a blocker.**
   - With no v3 entry, S0 records annex v2 and preflight passes, because `check_sealed_hashes` only verifies the entries that are listed.
   - If v3 is listed but altered, the governing re-hash catches it.
   - So the manifest is fail-closed only if it is the right manifest. Nothing outside the manifest pins its sha, because the application is not hashed (B-5).
   - This is not a blocker because the committed manifest lists v3 with the right sha. It must be fail-closed before seal: require the annex v3 path and sha, otherwise INTEGRITY STOP, and drop the fallback.
2. **Stale annex v1 role string. AGREE (note N-2).**
   - `items.governing` annex v1 role reads "superseded by annex v2 once that file exists; bytes retained".
   - The `precedence` list correctly reads "superseded by name and retained", rank 7.
   - The manifest is not an A8 module file and is not hashed in A8, so this can be fixed at seal without touching A8 or annex v3. That is true as long as the manifest's own sha is recorded only after the edit.
3. **`_guard_detail` runs on every FULL guard event. AGREE (note N-1), with an added timing caveat.**
   - Results are unchanged: the record is stored only on the first mismatch in each direction, and it uses only `.get` and None guards, so it adds no new failure modes.
   - The cost is about two extra `max|Δ|` reductions and two `min p` calls per guard event. That is the same order as the existing recovery check.
   - Projected wall time stays UNVERIFIED against the 540 s soft deadline. The risk is a PROJECTION HALT (incomplete), not wrong results. That is NEEDS-APPROVED-RUN.
   - Recommendation: build the record lazily, only on the stop branch or the first reverse event.

**CNA's delta claim. CONFIRMED.** 12b816ef..11efb513 changes only `classfit_manifest.json` and adds annex v3. All 23 module and wrapper files are byte-identical between the two commits, and they match A8.

**Where I differ from CNA's CONFORMS WITH NOTES.**
- CNA missed B-6: the RL-5 stop path overwrites the directory it just refused.
- Blockers B-1 to B-5 from the earlier pass remain open in code the delta did not touch.
