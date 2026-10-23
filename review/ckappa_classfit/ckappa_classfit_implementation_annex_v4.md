# C-κ class-fit package: implementation annex v4

**Binds to:** `ckappa_classfit_synthetic_scope_record_v1_3.md`, sha256 `a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`.

**Supersedes:** `ckappa_classfit_implementation_annex_v3.md` by name. Annex v3 sha256 `435453e0917d1d4d3f2c50c4cc8dc469d6487147f8dd987fd53eb877ac5cb8bd`. The v3 file is retained byte-identical and is not edited. Annex v2 sha256 `5d6daf06fea3466ff2fc1eebf73414f12c47daeccfe06095ec7a3efb64907262` and annex v1 sha256 `8614bf114b127f4bdab516c0e933c23c84d1cd5f4d0ef34837d5cb0ad453d3a8` stay byte-identical.

**Status: IMPLEMENTATION ANNEX v4. NOT SEALED. NO STAGE S0–S8 WAS RUN.**

**Implementation commit:** `771a8f8339138b124db8cb3bc77e04d4cc30111a`. That commit contains the module bytes hashed in A8. This annex is added in a later commit that does not change those bytes. This file does not contain its own sha256. The unsealed draft manifest records it.

Lead rulings RL-6 through RL-12, file `review/ckappa_classfit/ckappa_classfit_rulings_RL6_RL12_7da7.md`, sha256 `fc402c3db3bf9657cf0a1bb30a49c3022667f9827f2af8dfdaff972331a7883f`. Those rulings settle the Delegate review `review/ckappa_classfit/ckappa_pr14_code_review_RD_5132.md`, sha256 `f67b52133fd840371b78adebcd8277edd5c86c2313b9430a567bc84cefc7d7d0`, and its annex v3 delta `review/ckappa_classfit/ckappa_classfit_annex_v3_delta_RD_a5a6.md`, sha256 `d674991741cb52ce6cbca0bc4aa426720d7b2669aaae607d8ecf2e97e1617125`. The three files are committed byte-identical. RL-1 through RL-5 remain as annex v3 recorded them, except where a ruling below replaces a named field.

**Governing text.** Astra #39 raw (`e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482`) > #38 (`87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5`) > #37 (`ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2`) > v1.3 (`a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`) > this annex.
- Where this annex and annex v3 conflict, this annex governs, because it supersedes v3 by name.
- Where this annex and v1.3 conflict, v1.3 governs.
- There is no fallback from this annex to annex v3 or v2. A missing annex v4 entry is INTEGRITY STOP.

**Claim ceiling.** E38-15, unchanged. This annex establishes no result.

**What was executed.** `py_compile` of the package modules with the bytecode written outside the tree, `bash -n` on `run_classfit_package.sh`, and unit tests on tiny synthetic inputs. Those tests called pure helpers. They did not call `driver.main`, the wrapper, `preflight`, any `stage_s0` through `stage_s8`, or `static_checks`. One import-only process remeasured B0. No declared data were fit or evaluated. No checkpoint or weight file was opened. `classfit_manifest.json` is not sealed. The standing-approval application is not filed.

---

## RL-12. Authorship correction

Recorded from `fc402c3db3bf9657cf0a1bb30a49c3022667f9827f2af8dfdaff972331a7883f`.

Annex v2 was written by cloud agent `bc-11c1f9eb`. Annex v3 was written by cloud agent `bc-77fb29a4`. Both were written under Lead direction. The Research Delegate authored v1.3 and annex v1 only.

The same ruling says `_guard_detail` builds its record only on a mismatch, and the annex v1 role string in the manifest is corrected. Both are in the mapping below.

---

## Per-item mapping

Implementation commit for every code row: `771a8f8339138b124db8cb3bc77e04d4cc30111a`.

| Item | Commit | File:line | CI item |
|---|---|---|---|
| B-1 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/construction.py:65`, `:156` | CI-NC-ONE-VOID, replaced by the RL-6 split |
| B-2 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/aggregate.py:459`, `:495` | CI-HEADROOM-MET-LABEL, replaced by the inherited-label test |
| B-3 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/p0.py:20`, `construction.py:231`, `evaluate.py:517`, `accounting.py:34`, `schedule.py:109`, `aggregate.py:342` | CI-EXIT-CODES |
| B-4 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/pinned.py:74`, `preflight.py:297`, `:304` | MANIFEST-ITEMS-SHAPE |
| B-5 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/preflight.py:244`, `:390` | APPLICATION-PENDING |
| B-6 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/outputs_gate.py:26`, `driver.py:70`, `runstate.py:30`, `__main__.py:9`, `run_classfit_package.sh:11` | CR-5 |
| M-1 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/preflight.py:225`, `driver.py:118` | MANIFEST-ITEMS-SHAPE |
| M-2 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/fits.py:175`, `evaluate.py:157` | E39-7 skip point |
| M-3 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/accounting.py:105`, `driver.py:185` | RL-9 attempted partition |
| M-4 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/aggregate.py:610` | CI-EXIT-CODES |
| M-5 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/aggregate.py:479`, `evaluate.py:697` | UNFORMED-VS-ZERO |
| M-6 | none | `ckappa_classfit/aggregate.py:160`, `:353` | CI-PARTIAL-MASK, left OPEN under RL-11 |
| M-7 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/evaluate.py:113` | ATTEMPTED-DETAIL |
| M-8 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/evaluate.py:197` | C7.0 partial eval |
| M-9 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/fits.py:373`, `:397` | descriptive D5 |
| M-10 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/p0.py:69` | E39-10 domains |
| M-11 | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/rankcats.py:55`, `static_checks.py:52` | CI-B3-SHORT-STACK |
| RL-12 guard record | `771a8f8339138b124db8cb3bc77e04d4cc30111a` | `ckappa_classfit/evaluate.py:499` | RL-12 |
| RL-12 annex v1 role | manifest commit that adds this annex | `classfit_manifest.json` governing role for annex v1 | RL-12 |

`static_checks.py` now expects INTEGRITY STOP, exit 7, for a formed short stack. That file was not executed.

---

## RL-6. NC admissibility (B-1)

**Ruling.** `fc402c3d…`. Admissibility follows v1.3 C7.1 item 5, split by system. SYS-NC1 is inadmissible only at `>= 5` voids (`o7_void_stop_count`). SYS-NC2 and SYS-NC3 are inadmissible only when a matched baseline is invalid. One void alone does not make SYS-NC1 inadmissible. RL-1, rho_NC1 over all 16 prefixes, is unchanged.

**Implemented reading.** The matched baseline for SYS-NC2 and SYS-NC3 is that system's RMS-matched chart. A void of that chart (`len(voids) > 0`, belief below the guard) is `matched_baseline_invalid`. The `>= 5` count is not applied to SYS-NC2 or SYS-NC3. The sentence "one void alone never makes a system inadmissible" is applied to SYS-NC1: one void does not fire the void-count clause. It is not applied as a second exception that would keep SYS-NC2 or SYS-NC3 admissible after their matched chart is voided. C4.4.R says a matched baseline with `p < 10^{-6}` makes that system RESTRICTED COMPARATOR NOT ADMISSIBLE, with no rescaling.

`nc_system_admissible` in `construction.py`:
- SYS-NC1: admissible when `len(voids) < 5`. Reason `void_count` otherwise.
- SYS-NC2 and SYS-NC3: inadmissible when `voids` is nonempty. Reason `matched_baseline_invalid`.
- Any other system: this function returns admissible. True-chart voids remain a separate INTEGRITY STOP.

The per-prefix void row label is `VOIDED`. It is not `RESTRICTED COMPARATOR NOT ADMISSIBLE`. The system label stays the C7.1 item 5 words when the system is inadmissible.

B-1 is not left open.

---

## RL-7. HEADROOM gates (B-2, M-5)

**Ruling.** `fc402c3d…`. Restore the inherited law-mass BOUNDARY band. HEADROOM and MARG use the inherited vocabulary. The word MET is retired as the MARG success word. CI-HEADROOM-MET-LABEL is replaced by a test of the inherited labels, including the BOUNDARY band. An unformed HEADROOM row is UNAVAILABLE, never ZERO RESPONSE.

**Implemented reading of MET.** The inherited `ckappa_oracle/outcomes.py` success word is `MET` for ALL and `AVAILABLE` for MARG. v1.3 C7.4 still says the success sentence prints when HEADROOM is MET. This annex keeps ALL's inherited word `MET` and restores MARG's inherited word `AVAILABLE`. MET is retired only as the MARG success word that annex v2 had substituted. A law-mass value inside the inherited boundary band (`|x - t| <= boundary_relative * t`, with coverage `0.75` and `boundary_relative` `1e-6`) returns `BOUNDARY` after the clear-failure tests. `BOUNDARY` is not MET and is not AVAILABLE.

The C7.4 success sentence in `report.py` is printed when all of these stored labels hold:
- SYS-PC class label `IDENTITY AS DERIVED`;
- VALIDATION `CLASS-FIT VALIDATION MET`;
- HEADROOM ALL `MET`;
- HEADROOM MARG `AVAILABLE`.

The template condition sentence states that rule. `PC_SUCCESS` and the scientific sentences stay verbatim. The template does not assert that the labels hold.

M-5. `_unformed_headroom_label` maps `not_formed_reason` to its own status. Unknown reasons and `NOT_FORMED` become `UNAVAILABLE`. A formed row with pooled `S == 0` remains `ZERO RESPONSE`. Base loss records in `evaluate._emit_losses` carry `formed` and `not_formed_reason`.

---

## RL-8. Exit codes and stop labels (B-3, M-4)

**Ruling.** `fc402c3d…`. INTEGRITY STOP is exit 7. PIPELINE INVALID is exit 2. P0 failure and normalization failure are INTEGRITY STOP. Guard failure is PIPELINE INVALID. Accounting and schedule errors are INTEGRITY STOP. S7 labels a stopped run with its real stop kind and does not pool after a stop.

| Failure | Kind | Exit | Diagnosis stored with the stop |
|---|---|---|---|
| P0 | INTEGRITY STOP | 7 | `PIPELINE INVALID (P0)` |
| normalization | INTEGRITY STOP | 7 | `PIPELINE INVALID (normalization)` |
| guard inconsistency | PIPELINE INVALID | 2 | `PIPELINE INVALID (guard inconsistency)` |
| accounting error | INTEGRITY STOP | 7 | the accounting reason |
| schedule error | INTEGRITY STOP | 7 | the schedule reason |
| B3 short stack | INTEGRITY STOP | 7 | `PIPELINE INVALID (B3 short stack)` |

`schedule._check` is not run at import. `check_schedule_arithmetic` runs at S0 and is INTEGRITY STOP.

S7. Caps keep `CAP REACHED`, `CAP RESERVE REACHED`, or `PROJECTION HALT`, and VALIDATION `CLASS-FIT VALIDATION NOT MET (INCOMPLETE)`. Every other stop uses the stop kind as the label. VALIDATION reads `CLASS-FIT VALIDATION NOT MET ({stop_kind})`. `first_failing_reason` is the diagnosis, reason, or check from the stop detail. A stop is never labelled `NOT EVALUATED`.

After a stop, pooling does not run. A system that was not constructed gets `not_formed_reason` `NOT_REACHED` and is not marked inadmissible. A system that was constructed gets `PRIOR STOP`.

---

## RL-9. Fail closed (B-4, B-5, B-6, M-1, M-3)

**Ruling.** `fc402c3d…`.

**Inherited oracle modules.** The six modules this package imports are listed by path and sha in `ORACLE_IMPORTED_SHA256` and in the manifest. S0 re-hashes them. S0 then asserts that `sys.modules` contains no other `ckappa_oracle` name. The allowed names are `ckappa_oracle`, `ckappa_oracle.geometry`, `ckappa_oracle.io`, `ckappa_oracle.linalg_fit`, `ckappa_oracle.pinned`, and `ckappa_oracle.world`. The file `ckappa_oracle/__init__.py` is hashed. Its module name in `sys.modules` is `ckappa_oracle`, not `ckappa_oracle.__init__`.

**Application.** `check_application_hash` hashes `application.path` and compares it with `application.sha256`. A missing path, a missing file, a non-hex sha, or a mismatch is INTEGRITY STOP. The draft keeps `path` null, `sha256` null, and `status` `PENDING`. `load_manifest` still requires `sealed` true and a filed sha before a real run, so the unsealed draft stops as PREFLIGHT FAILED and does not reach the hash. The hash check is on the S0 path after that gate, and it was unit-tested on a temporary file. The application is not filed by this annex.

**Governing files.** S0 checks every governing entry by path and by sha. The required set is `REQUIRED_GOVERNING` in `preflight.py`. Annex v4's path is required. Its sha is not hardcoded in the module, because that sha would include this annex. S0 requires the manifest entry, requires the file, and compares the manifest sha with the file bytes. There is no fallback to annex v3 or v2. The other required shas are hardcoded. Consult 36 is the `review/ckappa/astra_consult36_response.txt` path. Those bytes equal `review/astra_consult36_response.txt`. The B2/B3 ruling file is not in the governing-set document's GOVERNING list, so it is not in `REQUIRED_GOVERNING`.

**Output directory.** Before any write, `outputs_gate` uses `os.lstat` and does not follow a symlink. It refuses a symlink, a non-directory, a path that resolves outside the package root, a nonempty `classfit_outputs/`, and an existing or symlinked `classfit_post_run_index.json`. A refusal writes nothing, prints `INTEGRITY STOP: classfit_outputs refused: …` on stderr, and exits 7. The same check runs in the driver, in `Run` before it creates the directory, in `__main__._thread_stop` before NumPy is imported, and in the wrapper before Python is launched. The wrapper skips the post-run block when the pre-check fails.

The first successful claim is process-local. Later writes in that same process are allowed after the directory has received that run's own files. A refusal does not record a claim. The wrapper's post-run block runs in a second process. It allows a nonempty directory only because the pre-check already passed, and it still refuses a symlink, a non-directory, a path outside the root, and an existing index.

**M-3.** On the COMPLETED path, after the ledger closes, `attempted_totals` partitions ATTEMPTED: S1 propagation against `run.exact_count`, S2 plus S6 propagation against `run.float_count`, fit plus b3_stack against `run.svd_count`, and every other cell against 0. A mismatch is INTEGRITY STOP.

**Post-run index.** The wrapper also re-hashes `post_run_index.json` against `7825c536ea987978b76f84c37c6a388846136a89ba4dd43fb0c6fc527427faea`. `stops` stays false on a match and on a mismatch. A mismatch does not change the package exit status. RL-5's rule for the sealed manifest and `outputs/` is unchanged.

---

## RL-10. B3 short stack (M-11)

**Ruling.** `fc402c3d…`. A formed stack with fewer than three singular values is INTEGRITY STOP, never PASS.

`b3_status` returns `NOT_FORMED` when the stack is unformed. A formed empty or zero first singular value stays `ZERO`. A formed stack shorter than three singular values calls `integrity_stop` with diagnosis `PIPELINE INVALID (B3 short stack)`. A formed stack of the declared shape is `(48·n_fit)×8` and has eight singular values, so the short-stack stop is unreachable there. `static_checks.py` expects that stop. `static_checks` was not run.

---

## RL-11. M-2 and M-6 through M-10

**Ruling.** `fc402c3d…`. Fix each item as the Delegate review specifies. If an item conflicts with v1.3, do not choose: leave it open.

| Item | Disposition |
|---|---|
| M-2 | Fixed. `SKIPPED_SYSTEM_INADMISSIBLE` is assigned at that system's S5 and S6 point. If `run.stopped` is already set, the category is `SKIPPED_PRIOR_STOP`. It is not dumped for every system at the end of S3. |
| M-6 | **Left open.** No code change. See below. |
| M-7 | Fixed. When a stage-S6 belief fails `_valid`, the ledger detail is `guard_invalid`. The forecast is retained. Scoring already ignores an invalid belief through the scoreable test, so the forecast is not replaced with null. |
| M-8 | Fixed. A `PackageStop` during baselines or folds writes `eval_<system>.json` with `partial: true`, then re-raises. |
| M-9 | Fixed. SYS-NC2 gets a descriptive D5 record. Status is `REPORTED` when the rank is full and a residual exists; otherwise `UNAVAILABLE`, `REFERENCE_RANK_UNRESOLVED`, `NOT_APPLICABLE_RANK`, or `NOT_EVALUATED`. Tolerances are null. The record does not stop and does not enter VALIDATION. It is outside the 1,128 identity-cell count. `IDENTITY_CELLS` is unchanged. The expectation text is that Dg2 is constant and Gain = L_mu >= 0 when the rank premise holds. |
| M-10 | Fixed. `p0_domain_pairs` is written to `stage_S4_P0.json` with `domains_recorded_before_comparisons: true` before any L or G comparison. Failure rewrites keep the same domains. |

**M-6, open.** `_one_label` tests coverage before rank, which is the literal order of v1.3 C7.1 items 3 and 4. Coverage therefore counts cells whose maps are unavailable, and REFERENCE COVERAGE NOT MET can mask REFERENCE RANK UNRESOLVED. The inherited oracle classifies coverage on resolved folds only, so coverage does not mask rank there. Changing this package to that oracle rule would depart from the v1.3 order. RL-11 says not to choose. CI-PARTIAL-MASK stays ACCEPT. No code in `aggregate.py` was changed for M-6.

The Delegate's minor notes (vacuous dtype check, gradient product spelling, the B3 `rank_category` field name, XOR zero-gain rows outside VALIDATION, UNRESOLVED-B3 not surfaced in labels, and `CUDA_VISIBLE_DEVICES`) were not part of B-1..B-6 or M-1..M-11. They are unchanged.

---

## A8. Fields filled in v4

The standing-approval application is not filed. Its path and sha256 stay null. The Lead files the application.

### Module file list and per-file sha256

Bytes of implementation commit `771a8f8339138b124db8cb3bc77e04d4cc30111a`. The six `ckappa_oracle` rows are inherited sealed bytes. This commit does not change them.

| Path | sha256 |
|---|---|
| `ckappa_classfit/__init__.py` | `d62a51c78144ca1bcfaff7db4f148b245deea34f42858b1c0f198a6d01f87ea0` |
| `ckappa_classfit/__main__.py` | `7b1660a820b6ec7bbd7a98af3cb510f5d3e517caabb9f30de2b419cd37337b5a` |
| `ckappa_classfit/accounting.py` | `59dbc9601e0e44785c599b973b800850ab4309e26b48b65ccd97212642416052` |
| `ckappa_classfit/aggregate.py` | `c141ea445e6ddcbc1fd8d65a359bf1830144a8795594f7b68998a02d97cce9b8` |
| `ckappa_classfit/arrays.py` | `9af98b49ab048be0595b71a801e92b03d9b2f2ce5d75e75a450c6343f8e571a4` |
| `ckappa_classfit/classes.py` | `115df4f03c9e76e3213bc543190287e3ac140601a11efcab4eaed6467036d219` |
| `ckappa_classfit/construction.py` | `a7cd3606c3f15cc311928282f9563e1f5c91e1b9cd473acbcea4680554aa3155` |
| `ckappa_classfit/driver.py` | `566b119e439e3bf6a38e96065cc22520d1226bd5de06a222e5bb370bf73ab3fb` |
| `ckappa_classfit/evaluate.py` | `e7031c76e8d2f872e7bec730d5450969fce63746cf6ae8eb8da38fa0368119cf` |
| `ckappa_classfit/fits.py` | `bc22bd9d85f9c1ac9ad6790d12b7f318a0dc6f709187cd5bd0beed5131b870da` |
| `ckappa_classfit/gate.py` | `82f79eafffe96248282f5051fcae7b9c64e1e009681153e1063eb1caa1878e18` |
| `ckappa_classfit/inputs.py` | `2486b03257678cf4161d03d1fd0327498373d98ae9df636af92c2404b606c7dc` |
| `ckappa_classfit/o1o2.py` | `8db5e1e5f06b1cc61844768c44b0133510968f397584cdaae147e8d04c9f917f` |
| `ckappa_classfit/outputs_gate.py` | `89832c8b172132328329f378e0fe847cf725353575d4b74bcfe18272ccab6440` |
| `ckappa_classfit/p0.py` | `3f8416f1bb63d9c695a34b0871edca4bc61cc70facf5bdeb34a27a92e9d1934a` |
| `ckappa_classfit/pinned.py` | `ecbca5c9662d768fa372976df771a0a9345518b7692438e24407a0fc3836b8c5` |
| `ckappa_classfit/preflight.py` | `87bcd808e81c4af9b6abfeacafc215198d239cfbd1e53db530cfbb21d149fec2` |
| `ckappa_classfit/rankcats.py` | `6168fb042dfe9040efea3a8d94e362a0a7cc8e0364961df6ced592e4ffd5c7cb` |
| `ckappa_classfit/records.py` | `7e05faaf3cd7e1a8e74aab112ad90faa9af13896be1f56ab106118dbc79fe122` |
| `ckappa_classfit/report.py` | `96bf6aeda8239fc03d5f6590d60aeb36534e7e40739a6ae983890377151d0ff2` |
| `ckappa_classfit/runstate.py` | `d682f1bb475fa6edae710063ece642b5924cfab6a797533492a1a215c6ad1c60` |
| `ckappa_classfit/schedule.py` | `da698d438dc96daabc3fa14065a6fddc15977a3d2551b179dd90cbc34865cd34` |
| `ckappa_classfit/static_checks.py` | `c3b1208bf2e0c8f40f45dfd78f358cbe9f2ca618bff072775172dff7f396f477` |
| `run_classfit_package.sh` | `05eecb2c34596269ed08943b8416132ab16b448af0658402a87f99601c6fbe44` |
| `ckappa_oracle/__init__.py` | `45f848b1c56ba1fe4b5a8a663c706937402ee936a8e414100ea2d16e4b5db718` |
| `ckappa_oracle/geometry.py` | `117e98e959c8134cb0f124bf284488a9ee71bc319b07b21ac9fa489dac7e8ac9` |
| `ckappa_oracle/io.py` | `b1795bcc4f022228da1ef13703c8a0ede2dc96287af25e8e5e314d390fc17802` |
| `ckappa_oracle/linalg_fit.py` | `de6f4034260bbc0ba74c2b6d1bddfbc5fe0bfd3c637ef0b4168e188885fd936a` |
| `ckappa_oracle/pinned.py` | `03c55323d0eb0b14fc463510738109d24e76ee9dc4623ba0e8c396e712363a68` |
| `ckappa_oracle/world.py` | `3d235fca82741e1a2081c7f4eac993b04f59226a3720b6232d06e637803f5aac` |

`classfit_manifest.json` and this annex are not module files. Their hashes belong in the manifest. `ckappa_classfit/__main__.py` is in this list and was not imported during the B0 measurement, because its body calls `main()`.

### Implementation commit hash

`771a8f8339138b124db8cb3bc77e04d4cc30111a`

### B0 memory baseline

Imports changed, so B0 was remeasured. The annex v3 figure 59,170,816 B is not reused.

One import-only process. No input was read, no system was built, and no stage was executed. `classfit_outputs/` was absent before and after the process. `ckappa_classfit.__main__` was not imported. Every other package module was imported by name, including `ckappa_classfit.outputs_gate`. The loaded `ckappa_oracle` names were exactly the six allowed names.

Wrapper settings, checked inside the process: `prlimit --as=4000000000`, `taskset -c 0` (affinity `{0}`), `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`. The pinned interpreter and NumPy were present, so nothing was substituted.

| Observation | Value |
|---|---|
| `sys.version` | `3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0]` |
| `numpy.__version__` | `1.26.4` |
| VmPeak | `60024 kB` = **61,464,576 B** (`/proc/self/status`; kB = 1024 B) |
| VmHWM, peak resident set, context only | `36676 kB` = 37,556,224 B |
| `ru_maxrss`, context only | 36,492 KiB = 37,367,808 B |
| RLIMIT_AS soft, hard | 4,000,000,000, 4,000,000,000 |
| VmPeak + package budget | 61,464,576 + 316,737,056 = **378,201,632** |
| Against 4e9 B | 378,201,632 ≤ 4,000,000,000. The condition holds for this measurement. |

VmPeak is the only operand. The two RSS figures differ by 184 KiB. Neither enters the comparison. `PACKAGE_BUDGET_BYTES` remains 316,737,056. The annex v3 feasibility bound, VmPeak ≤ 3,683,262,944 B, is unchanged. S0 re-measures VmPeak and does not reuse 61,464,576 B.

### Package budget

Unchanged from annex v3. Incremental bytes 158,368,528. Package budget, with the factor-2 allowance, 316,737,056.

---

## CI disposition at this annex

| CI item | Disposition |
|---|---|
| CI-NC-ONE-VOID | Replaced by the RL-6 split. SYS-NC1 uses the `>= 5` void count. SYS-NC2 and SYS-NC3 use matched-baseline invalidity. |
| CI-HEADROOM-MET-LABEL | Replaced. The test is the inherited labels, including BOUNDARY. ALL success word `MET`. MARG success word `AVAILABLE`. |
| CI-EXIT-CODES | INTEGRITY STOP is exit 7. PIPELINE INVALID is exit 2. S7 uses the real stop kind. |
| CI-B3-SHORT-STACK | INTEGRITY STOP, exit 7. Never PASS. |
| CR-5 | The output directory and the existing post-run index are refused before any write. The oracle re-hash now includes `post_run_index.json`. `stops` stays false. |
| MANIFEST-ITEMS-SHAPE | Governing entries are checked by path and sha. Annex v4 is required. Inherited oracle modules are in the implementation list. |
| APPLICATION-PENDING | The path and sha stay null. The S0 hash check exists and is not reached on this unsealed draft. |
| ATTEMPTED-DETAIL | `guard_invalid` is populated. The forecast is retained. |
| UNFORMED-VS-ZERO | An unformed HEADROOM row is not ZERO RESPONSE. Loss records carry `formed` and `not_formed_reason`. |
| CI-PARTIAL-MASK | ACCEPT, and M-6 stays open under RL-11. |

---

## Open items

- **M-6** is open under RL-11. Coverage is still tested before rank. No code change.
- The manifest is **UNSEALED**. `sealed` is false. `seal_status` is `UNSEALED`.
- The standing-approval application is **PENDING**. `path` and `sha256` are null. It has not been filed.
- No stage S0–S8, no wrapper launch, no fit, and no `static_checks` run was performed. The short-stack expectation in `static_checks.py` is updated and unexecuted.
- The Delegate minor notes listed under RL-11 are unchanged.
- B-1 through B-6 and M-1 through M-5 and M-7 through M-11 are implemented as this annex states. They are not open.
