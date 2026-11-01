# PR #14 final delta check, 515725d7 → bf320dd5 (Research Delegate)

**Status: DRAFT REVIEW RECORD. NOTHING RUNS.** This record establishes no result. The claim ceiling is E38-15.

- **Scope.** HEAD `bf320dd560daec8b49f881793f13ee380d8f919b`.
  - Code, test and copied files: `a18c8650524a70a57ed500ee92ba0393ad9b9bfa`.
  - Annex v5 and manifest: `bf320dd5`.
  - No code, test, oracle or wrapper bytes differ between a18c8650 and bf320dd5.
- **Read-only.** Nothing pushed or commented. No earlier file edited. This is a new file, written 2026-10-23 at about 09:45 ET.
- **What I executed.**
  - `py_compile` on all `ckappa_classfit/*.py` and the test file.
  - `bash -n` on the wrapper.
  - `tests/test_phi_count.py`, once. I read its imports first: `runstate`, `rankcats`, `accounting`, `schedule`, `outputs_gate`, `pinned`, `ckappa_oracle.io` and `.world`. All are definitions and constants only, and none runs a stage. The test builds `Run` on `tempfile.mkdtemp()` directories outside the repo and substitutes `phi_float`. It printed "phi-count checks passed", exit 0. The box has Python 3.13.5 and NumPy 2.5.4, so it is not authoritative.
  - No stage, wrapper, driver, static_checks, fit or simulation.
- **Housekeeping.** The `py_compile` loop left gitignored `__pycache__/` in `ckappa_classfit/` and `tests/` of the scratch clone. I deleted them, and `git status --ignored` is now clean.

## Verdict: CLEAR WITH NOTES

## 1. Identity

| Check | Result |
|---|---|
| Annex v5 sha256 | `7eb1c7ad9ed212a37bf063d34259a78fbdff4236390d5bafabc77f3ad19c67fd` ✓ |
| Supersedes v4 by name | Header: "Supersedes: `…annex_v4.md` by name … There is no fallback from this annex to annex v4 or any earlier annex. A missing annex v5 entry is INTEGRITY STOP." ✓ |
| Code enforces no fallback | `preflight.py:228, 237` require `ANNEX_V5_PATH`, and `:382–383` stops if it is absent. `driver.py:122–141` stops if the v5 entry is absent or its sha mismatches. v4 is now pinned by sha (`pinned.py` `ANNEX_V4_SHA256` = `84620dc7…`, `REQUIRED_GOVERNING`) ✓ |
| RL-13 recorded | Annex v5 L54: "'One void alone never makes a system inadmissible' applies to SYS-NC1 only. For SYS-NC2 and SYS-NC3, a prefix void is an invalid matched baseline and the system is RESTRICTED COMPARATOR NOT ADMISSIBLE." ✓ L56: "M-6 is **ACCEPT**." ✓ L58: RL-7 confirmed, citing `outcomes.py` lines 12–13 (ALL `MET`, MARG `AVAILABLE`) ✓ |
| Manifest sha256 | `64f03292bca2ddd9bae5bb6b4d55fd98e36fcee6f60074e80a33a0d60e8a267c` ✓. `sealed: false`, `UNSEALED`, application `{path: null, sha256: null, status: PENDING}` ✓. Implementation commit `a18c8650…` ✓ |
| Manifest governing list | Includes `ckappa_classfit_rulings_RL6_RL12.md` `fc402c3d…` and `ckappa_pr14_fix_delta_RD_5f85.md` `0303e3b1…`. All 18 governing entries match their bytes ✓. Both are also hardcoded in `REQUIRED_GOVERNING` (`pinned.py` `RL6_RL12_SHA256`, `FIX_DELTA_SHA256`) ✓ |
| Copied files | `ckappa_classfit_rulings_RL6_RL12.md` = `fc402c3d…`, which equals the `/workspace/review` original and the earlier `_7da7` copy. `ckappa_pr14_fix_delta_RD_5f85.md` = `0303e3b1…`, which equals `/workspace/review/ckappa_pr14_fix_delta_RD.md` ✓ |
| A8 | 30 rows. All match the module bytes and the manifest `implementation_files` ✓. `tests/test_phi_count.py` is not listed; annex v5 L89 says it is not an implementation module (note T-2) |
| Oracle modules | All six unchanged: `45f848b1`, `b1795bcc`, `03c55323`, `3d235fca`, `117e98e9`, `de6f4034` ✓ |
| Import set | No new import statement in any package module; the diff adds only ckappa_classfit symbols to existing import lines. No module was added under `ckappa_classfit/`. So the import set is unchanged and B0 = 61,464,576 B stands; I did not re-measure it ✓ |
| Unchanged files | v1.3 `a17e133d`, annexes v1 `8614bf11`, v2 `5d6daf06`, v3 `435453e0` and v4 `84620dc7`, Astra raws #37–#39, `manifest.json` `4179b71a`, `post_run_index.json` `7825c536`, `outputs/*` and `ckappa_oracle/` have no diff 515725d7..bf320dd5 ✓ |

## 2. NB-1 (FIXED)

**Order in `Run.phi`** (`runstate.py:140–163`):
1. Soft-deadline check (`:140`), CAP RESERVE REACHED.
2. Overrun check `if self.float_count >= SCHEDULED_FLOAT` (`:155`), INTEGRITY STOP 7.
3. `self.float_count += 1` (`:161`).
4. `phi_float(...)` (`:163`).

The timing sample is taken only on success ✓. The overrun bound is unchanged in effect. At most 3,443,968 calls start. The call that would be the 3,443,969th now stops before it runs, where before it ran and was counted first. That is stricter, not looser.

**Ledger booking** (`evaluate.py:101–119`, `_propagate`):
- **ValueError path.** The call is counted (step 3). `except ValueError` books `ATTEMPTED/value_error` (`:107–109`). The S6 float ATTEMPTED total and `float_count` both include it ✓.
- **Overrun stop path.** `float_count` is not incremented, so `except PackageStop: if run.float_count > before` (`:103–106`) books nothing. Nothing is counted or booked ✓. The soft-deadline stop behaves the same way ✓.
- **Stop after counting.** The only PackageStop raised after the count is the projection inside `phi`. It is counted and booked `valid_finite`, so the totals stay equal. This behaviour is unchanged from before.
- **S2** (`o1o2.py:252–261`). A ValueError is counted, booked `value_error`, then stops at PIPELINE INVALID 2. The overrun or deadline paths book nothing ✓.

**Partition.**
- `accounting.py:105–135` `attempted_totals` adds `value_error` as its own subtotal, read from `attempted_detail`. That key exists for every grid cell (`:25–30`).
- The subtotal is not removed from `exact` or `float` ✓.
- `driver.py:189–197` compares only `exact`, `float`, `svd` and `other` with the counters. `value_error` is reported but is not a fifth counter ✓.
- This matches v1.3 C8.4 (L1231): "Any call that was started, whatever its outcome … ValueError".

**Test coverage (`tests/test_phi_count.py`).**
- `test_raising_phi_counts` (`:28–62`) and `test_overrun_stops_before_increment` (`:65–91`) do exercise `Run.phi`'s order on both paths:
  - count +1 and no timing sample on ValueError;
  - INTEGRITY STOP 7, no increment and no `phi_float` call on overrun.
  - They also check that the partition equals the counters, with `value_error == 1`.
- **Gap (note T-1).** The ValueError test books the ledger row by hand (`:53`). It does not go through `evaluate._propagate`, so the S6 booking (`:103–109`) is verified by my reading, not by the test. A test that calls `_propagate` with a stubbed `phi` on both paths would close this.
- `test_short_stack_before_zero` and `test_missing_sigma_stops` cover items 4 and 5.

## 3. N-2 (FIXED)

`p0.py:89–92`: the pre-comparison write is `status: "DOMAINS_RECORDED"`, with domains and `domains_recorded_before_comparisons: true`.
- FAIL is written only at the failing comparison (`p0.py:98–107, 128–135, 150–157`).
- PASS is written only after all comparisons (`:159–163`) ✓.

## 4. Short stack (FIXED)

`rankcats.py:66–77`, after NOT_FORMED:
- `len(sigma) < 3` raises INTEGRITY STOP (`:69–75`) **before** the σ₁ = 0 ZERO return (`:76–77`) ✓.
- An empty σ list now also stops instead of returning ZERO. That is correct: a formed stack always has 8 values.
- The `static_checks.py:51` fixture changed from `[0.0, 0.0]` to `[0.0, 0.0, 0.0]` to match. That is the only static_checks change.

## 5. N-6 (FIXED)

`rankcats.py:32–36`: a missing σ₁ is `integrity_stop("nonempty design missing sigma_1", diagnosis="PIPELINE INVALID (rank)")`. That is the inherited INTEGRITY STOP, exit 7; `integrity_stop` was already imported at `rankcats.py:8` ✓.

## 6. Diff scan (code: 8 package files plus the new test)

| File | Change | Assessment |
|---|---|---|
| `accounting.py` | `value_error` subtotal | OK. It removed `del system`; `system` is now used to index `attempted_detail` |
| `driver.py` | v5 required; partition compared without `value_error` | OK. The S0 payload adds the v5 fields and keeps the v4/v3/v2 shas as context only |
| `p0.py` | DOMAINS_RECORDED | OK |
| `pinned.py` | three shas | OK. No budget or FROZEN_RUNTIME change |
| `preflight.py` | v5 path; v4, rulings and fix-delta pinned | OK |
| `rankcats.py` | short stack first; missing σ₁ stops | OK |
| `runstate.py` | phi order | OK |
| `static_checks.py` | one fixture | OK |

There are no regressions and no unrelated changes. The wrapper, `outputs_gate`, aggregate, evaluate, fits and construction are byte-unchanged.

## 7. Notes (none blocking)

- **T-1.** The test does not exercise `evaluate._propagate`'s booking. See §2.
- **T-2.** `tests/test_phi_count.py` is not hashed in the manifest. That is fine because the package never executes it. Pin it at seal if it is to count as evidence.
- **N-3 / N-5** remain notes, as annex v5 L135 records: the TOCTOU between the wrapper pre-check and the in-process claim, and the redundant resolve comparison.
- **B0.** 61,464,576 + 316,737,056 = 378,201,632 < 4,000,000,000, from the annex v4 measurement. It is not re-measured and remains UNVERIFIED on the box. S0 re-measures it live.
