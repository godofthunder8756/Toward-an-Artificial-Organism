# PR #14 fix delta check, 11efb513 → 515725d7 (Research Delegate)

**Status: DRAFT REVIEW RECORD. NOTHING RUNS.** This record establishes no result. The claim ceiling is E38-15.

- **Range.** HEAD `515725d7fc39a2129dacbda37737efcdd884b903`.
  - Code commit: `771a8f8339138b124db8cb3bc77e04d4cc30111a`.
  - Record commit (annex v4, manifest, three copied reviews): `515725d7`.
- **Clone.** Fresh fetch into `/workspace/scratch/pr14`. `/workspace/repo` was not touched.
- **Read-only.** No push and no comment. No earlier file was edited. This file is new.
- **Written.** 2026-10-23, about 09:30 ET.
- **Governing set.**
  - v1.3 `a17e133d…`
  - Astra #39 raw `e6403b63…` (box file verified)
  - Specialist rulings `/workspace/review/ckappa_classfit_rulings_RL6_RL12.md`, sha256 `fc402c3db3bf9657cf0a1bb30a49c3022667f9827f2af8dfdaff972331a7883f` (verified)
  - My review `ckappa_pr14_code_review_RD.md`, `f67b5213…`
- **What I executed.**
  - `py_compile`, with bytecode to `/tmp`, on all `ckappa_classfit/*.py`.
  - `bash -n` on the wrapper.
  - One isolated import of `ckappa_classfit.driver` and `ckappa_classfit.static_checks`, to list the loaded `ckappa_oracle` modules. Module bodies are definitions only, and no `__main__` was imported.
  - No stage, wrapper, driver `main`, `static_checks` run, fit or simulation.
- **Housekeeping.** Before this pass I removed two stale, gitignored `__pycache__` directories in the scratch clone. My earlier import-only check had left them there. They were untracked and are irrelevant to the reviewed bytes.

## 0. Verdict: BLOCKERS (one, small and fix-before-seal)

- B-1..B-6 and M-1, M-2, M-4, M-5, M-7..M-11 are FIXED. M-6 is OPEN by design under RL-11. The P_a_float minor is FIXED.
- **NEW NB-1 (blocker): the ATTEMPTED-vs-counter check can INTEGRITY-STOP a clean run.** It is the same finding as CNA's N-1, and I agree with it; see §5. The trigger is very unlikely, but it cannot be excluded statically. The run is single-shot with no retries, and the fix is three lines. So I hold it as fix-before-seal.
- Everything else new is a note.

## 1. Identity checks

| Item | Result |
|---|---|
| Annex v4 sha256 | `84620dc7e8b84df65ecb81db9689f0170dbb354b183ecd955d7a5b139284b984` ✓ |
| Annex v4 supersedes v3 by name; no fallback | Header: "Supersedes: `…annex_v3.md` by name … There is no fallback from this annex to annex v3 or v2. A missing annex v4 entry is INTEGRITY STOP." ✓ Code: `preflight.py:225` `REQUIRED_GOVERNING` and the `ANNEX_V4_PATH` check; `driver.py:122–138` stops if the v4 entry is absent or its sha mismatches. The v3→v2 fallback is removed ✓ |
| Manifest sha256 | `24f2e547be0ce33c1a4c9056bbceea925fbb07b45898bb18c432601adf943c31` ✓. `sealed: false`, `seal_status: UNSEALED`, application `{path: null, sha256: null, status: PENDING}` ✓ |
| Oracle modules in the manifest | Six, all matching the bytes: `__init__` `45f848b1…`, `geometry` `117e98e9…`, `io` `b1795bcc…`, `linalg_fit` `de6f4034…`, `pinned` `03c55323…`, `world` `3d235fca…`. They equal `pinned.ORACLE_IMPORTED_SHA256` ✓ |
| Full imported set | AST scan of `ckappa_classfit/*.py` plus the six modules, and an isolated import of `driver` and `static_checks`. Loaded set = {`ckappa_oracle`, `.geometry`, `.io`, `.linalg_fit`, `.pinned`, `.world`}. That is exactly the listed six ✓. Only `linalg_fit` imports another oracle module (`pinned`). `outcomes`, `stages`, `runstate` and the rest are not loaded ✓ |
| Copied review files | `review/ckappa_classfit/ckappa_pr14_code_review_RD_5132.md` = `f67b5213…`, `…annex_v3_delta_RD_a5a6.md` = `d6749917…`, `…rulings_RL6_RL12_7da7.md` = `fc402c3d…`. All byte-identical to the `/workspace/review` originals ✓ |
| Unchanged files | v1.3 `a17e133d…`, annex v1 `8614bf11…`, v2 `5d6daf06…`, v3 `435453e0…`, #39 `e6403b63…`, #38 `87fd77e0…`, #37 `ce010fdb…`. All unchanged (no diff 11efb513..515725d7) ✓ |
| Sealed oracle artifacts | `manifest.json` `4179b71a…`, `post_run_index.json` `7825c536…`, 15 `outputs/*` files. All equal the pinned values. `ckappa_oracle/` has no diff ✓ |
| A8 table | All 30 rows (23 classfit + `outputs_gate.py` + 6 oracle modules; the wrapper is counted among the 23 classfit rows) match the bytes at HEAD, and match the manifest `implementation_files` ✓. No code differs between 771a8f83 and 515725d7 ✓ |
| Other governing shas | `REQUIRED_GOVERNING` hardcodes #36 `c8342d5a…` and the oracle governing set (`CKAPPA_SCOPE_GOVERNING_SET_RL.md` `6a5e0f24…`, v1_4_N closure note `4ad1d217…`, v1_4_N `3f0c5c12…`, v1_3_E36 `f6263fb8…`, v1_2 `7e15e812…`, v1_1 `e40c288f…`). All match the bytes ✓ |
| py_compile / bash -n | OK ✓ |

## 2. Per-item status at 515725d7

| ID | Status | Evidence (file:line) |
|---|---|---|
| B-1 | **FIXED** | `construction.py:65–85` `nc_system_admissible`: NC1 is inadmissible only at ≥ `o7_void_stop_count` (5) voids; NC2/NC3 on `matched_baseline_invalid`. Per-prefix label is `VOIDED` (`:156`). Reading ruled in §4(a). |
| B-2 | **FIXED** | `aggregate.py:459–476` `_law_mass_boundary` (reference ε, class rows); `:542–551` appends `law_mass` to the band, giving BOUNDARY. `:22–23` ALL `MET`, MARG `AVAILABLE`. `report.py:142–143` success needs ALL `MET` and MARG `AVAILABLE`. |
| B-3 | **FIXED** | P0 `p0.py:22` and normalization `construction.py:231–235` raise `integrity_stop` (7), with diagnosis "PIPELINE INVALID (…)". Guard `evaluate.py:517` is `_pipeline(…, 2)`. Accounting `accounting.py:35–52` and schedule `schedule.py:109–113, 124` raise `integrity_stop`. Schedule check moved to S0 (`preflight.py:195`). S7 uses the real kind (`aggregate.py:345–347`, `:390–400`). No PIPELINE INVALID/7 pair remains (grep). See note N-6 for the one remaining `ValueError`. |
| B-4 | **FIXED** | `pinned.py` `ORACLE_IMPORTED_SHA256` / `ORACLE_IMPORTED_MODULES`. `preflight.py` `check_sealed_hashes` requires the oracle set to equal the pinned set by path and sha, re-hashes it, and calls `assert_oracle_modules_loaded` (`:297–301`). |
| B-5 | **FIXED** | `preflight.py:244–268` `check_application_hash`: a missing path or sha, a symlink, a missing file or a mismatch is INTEGRITY STOP. It is called at `preflight.py` before `check_sealed_hashes`. Today the unsealed manifest stops earlier, at PREFLIGHT FAILED. |
| B-6 | **FIXED** (notes N-3, N-5) | Full write-path trace in §3. |
| M-1 | **FIXED** | Exact path and sha for the required governing set, the v4 entry required (`preflight.py:225–243, 363–375`; `driver.py:122–138`). `items.inputs` is cross-checked against the pinned constants (`check_input_rows`). #36 and the oracle governing set are included. |
| M-2 | **FIXED** | The eager S3 skip was removed (`construction.py:299–300`). Skips are assigned at S5 (`fits.py:176–180`) and S6 (`evaluate.py:157–167`), with SKIPPED_PRIOR_STOP if the run has stopped. |
| M-3 | **PARTIAL → NEW NB-1** | `accounting.py:105–122` `attempted_totals`; `driver.py:185–197` compares it with the run counters. The comparison mixes two definitions; see §5. |
| M-4 | **FIXED** | `aggregate.py:596–625`: after a stop, nothing is pooled. Rows read NOT_REACHED (system not built) or PRIOR STOP, and admissibility is never set false for unreached systems. The 336-row count is preserved (7 × 2 × 3 groups × 4 ε × 2 modes). |
| M-5 | **FIXED** | `aggregate.py:479–493` maps `not_formed_reason`, with unknown or NOT_FORMED → UNAVAILABLE. `:505–514`: an unformed row is never ZERO RESPONSE. Base loss records carry `formed` / `not_formed_reason` (`evaluate.py:676, 697–698, 723–724, 730–744`). |
| M-6 | **OPEN (by RL-11)** | Annex v4 L161 lists it for a Lead ruling. No code change. Correctly handled under RL-11's "do not choose". |
| M-7 | **FIXED** | `evaluate.py:113–117`: a guard-invalid belief is ATTEMPTED/`guard_invalid`. Callers only special-case `value_error` / `non_finite`, so behaviour is unchanged. |
| M-8 | **FIXED** | `evaluate.py:194–203`: on PackageStop, writes `eval_<system>.json` with `partial: true`, then re-raises. This happens after the Run claim, so B-6 is safe. |
| M-9 | **FIXED** | `fits.py:372–374, 397–444` `_d5`: descriptive, null tolerances, premise statuses, no stop. Not in VALIDATION (NC2 is not in `IDENTITY_SYSTEMS`). The target is `slope[0]`; NC2's block is prefix-constant (`construction.py:397–408`, affine gradient). |
| M-10 | **FIXED, with NEW note N-2** | `p0.py:65–92`: domains are serialized to `stage_S4_P0.json` before any L/G comparison, and to every FAIL/PASS write. N-2: the pre-comparison write carries `status: "PASS"`. |
| M-11 | **FIXED** (note N-4) | `rankcats.py:68–74`: a short stack is INTEGRITY STOP. |
| Minor: S3 `rms` lacks `P_a_float` | **FIXED** | `construction.py:547`. |
| RL-12 guard record | **FIXED** | `evaluate.py:509–511, 522–524`: built only on the mismatch or the first reverse event. |
| RL-12 authorship | **FIXED** | Annex v4 L28: "Annex v2 was written by cloud agent `bc-11c1f9eb`. Annex v3 was written by cloud agent `bc-77fb29a4` … The Research Delegate authored v1.3 and annex v1 only." |
| RL-12 manifest v1 role string | **FIXED** | The precedence entry reads "superseded by name and retained". |

## 3. B-6 write-path trace

The gate is `outputs_gate.py`. It is stdlib only.
- `outputs_refusal` (`:26–53`) uses `os.lstat` and refuses on symlink, non-directory or non-empty. It does not follow a symlink, and a dangling symlink is also caught by `lstat`.
- `index_refusal` (`:56–68`) refuses if `classfit_post_run_index.json` exists or is a symlink.
- `claim_output_dir` (`:71–87`) remembers only a success and creates nothing.

| Writer | Gate before first write | On refusal |
|---|---|---|
| Wrapper pre-launch (`run_classfit_package.sh:11–35`) | `outputs_refusal` + `index_refusal` in a stdlib child. If the child itself fails, that is also exit 7. | stderr + `exit 7`. Python is not launched, and the post-run block is not reached. Nothing is written. ✓ |
| `__main__._thread_stop` (`__main__.py:16–20`) | `claim_output_dir` before `mkdir` | stderr + `SystemExit(7)` ✓ |
| `preflight.check_outputs_directory` (start of `preflight`) | lstat-based state + index | Raises INTEGRITY STOP. Writes nothing itself. |
| `driver._write_pair` (`driver.py:70–79`) for every stop/complete path (`:236–239, 258–260, 280–283, 292–295`) | `claim_output_dir(ROOT)` before `mkdir` or any write | stderr, returns 7, and `main` returns 7. No write ✓ |
| `Run.__init__` (`runstate.py:28–42`), which owns the `mkdir` and opens `run.log` with `"w"` | `claim_output_dir` first | Raises INTEGRITY STOP (run stays None). `_write_pair(None…)` is then also refused. No write ✓ |
| `run.write_json` / `write_text` / `write_stop` / `run.log` / checkpoints / the partial eval write (M-8) / the P0 writes | Only reachable after a successful claim in `Run.__init__` | n/a ✓ |
| Logging handler | None exists (no `logging` module). `run.log` is the file handle opened after the claim ✓ | |
| Wrapper post-run block (`run_classfit_package.sh:58–70`) | Refuses on symlink, not-a-directory or an existing index. **Non-empty is allowed** (`:61`), because the package legitimately wrote there. | stderr + `SystemExit(7)`, then the wrapper exits 7 (`:226–229`) ✓ |

**Result.** On refusal no writer writes, follows a symlink or creates the directory. The fallback write in `_write_pair`'s `except` runs only after a successful claim.

**Note N-3 (TOCTOU, not a blocker).**
- The wrapper pre-check and the package's claim are separate moments. If foreign files appear in `classfit_outputs/` between the pre-check and the in-process claim, the package refuses with exit 7 and writes nothing. The post-run block then accepts "nonempty" and may add `stop_kind.json` (write-if-missing) and the index.
- A symlink swapped in after a claim would be followed by the later `mkdir` and atomic writes.
- Both need concurrent tampering. Suggested hardening: the package writes a run-nonce marker at claim time, the post-run block requires it, and paths are opened with `O_NOFOLLOW`.

## 4. RL-6..RL-12 against the code and the two readings

The code checks for RL-6..RL-12 are in §2.

### (a) RL-6 reading: a void in the NC2/NC3 RMS chart = `matched_baseline_invalid`; the one-void sentence applies to NC1 only. **CONFIRM (with a note to the Lead).**

The v1.3 text, quoted:
- C7.1 item 5 (L1105): "RESTRICTED COMPARATOR NOT ADMISSIBLE (SYS-NC1–NC3): ≥5 of 16 prefixes voided, **or a matched baseline invalid**."
- C4.4.R (L969): "**Admissibility.** If **any** matched baseline is invalid (p < 10⁻⁶), the system is RESTRICTED COMPARATOR NOT ADMISSIBLE, with no rescaling."
- C3.9 (L791): "Systems whose baseline is not the true chart (SYS-FK, SYS-NC1–NC3) inherit N4(ii) per-prefix voiding. SYS-NC1–NC3 also inherit the ≥5-of-16 RESTRICTED COMPARATOR NOT ADMISSIBLE rule (v1_4_N L38–43)."
- Inherited N4(ii) (`review/ckappa/ckappa_oracle_scope_record_v1_4_N.md:39–43`): "A prefix whose quadratic baseline … is invalid (any p < 10⁻⁶) is **voided** … If more than 25% of the 16 prefixes are voided (5 or more), O7 as a whole reads RESTRICTED COMPARATOR NOT ADMISSIBLE."

Reasoning:
- In v1.3 a "matched baseline" is the baseline of an RMS-matched system (C4.4.R, which governs NC2 and NC3).
- A prefix baseline of that chart with p < 10⁻⁶ is exactly what N4(ii) calls a void. "Any matched baseline invalid" therefore fires on one NC2/NC3 void.
- L791 is not contradicted. Per-prefix voiding still happens and is listed. For NC2/NC3 the ≥5 clause is subsumed (≥5 voids implies at least one invalid), so it is redundant, not inconsistent.
- For NC1 only the ≥5 clause applies, because NC1 is the source of ρ, not a matched system.
- The reading also follows the rulings' default "revert to v1.3 … Fail closed".

Note: RL-6's sentence "One void alone never makes a system inadmissible" literally conflicts with this for NC2/NC3. Annex v4 L68 scopes it to NC1 and the void-count clause. I recommend the Lead acknowledge that scoping in the next ruling. It is not a blocker, because v1.3 outranks the ruling's paraphrase and the annex records the reading.

### (b) RL-7 reading: ALL keeps MET, MARG uses AVAILABLE. **CONFIRM. ALL is MET, so there is no blocker.**

Inherited source at `14376f38` (`git show 14376f38:ckappa_oracle/outcomes.py`, sha `897728e4…`, byte-identical to HEAD):
- `outcomes.py:12`: `"ALL": {"sqrt_H": fnum("all_sqrt_H"), "R": fnum("all_R"), "met_label": "MET"},`
- `outcomes.py:13`: `"MARG": {"sqrt_H": fnum("marg_sqrt_H"), "R": fnum("marg_R"), "met_label": "AVAILABLE"},`
- `outcomes.py:9`: `REL = fnum("boundary_relative")`. `ckappa_oracle/pinned.py:22`: `"boundary_relative": "1e-6"`.
- `outcomes.py:21–22`: `def _in_band(value, threshold): return abs(value - threshold) <= REL * threshold`. So the band is |x − t| ≤ 1e-6·t, confirming CNA's citation.
- The law-mass band joins the BOUNDARY list (`outcomes.py:44–45`, `:91`).

Sealed oracle outputs:
- `outputs/REPORT.md:9`: "ALL: MET. count coverage, law-mass coverage, sqrt(H*), and R* are all clearly met"
- `outputs/REPORT.md:18`: "MARG: AVAILABLE. count coverage, …"
- `outputs/results.json`: `section5.ALL.label = "MET"`, `section5.MARG.label = "AVAILABLE"` (also under `o6_section5` and `stages.O6.section5_from_o6`).

Code at HEAD matches this: `aggregate.py:22–23`, `report.py:142–143`.

The rulings text "the word MET is retired" is correctly implemented as retiring MARG's v2 substitution only. Retiring ALL's MET would contradict the inherited source and v1.3 C7.4. The band test reuses the same `_in_band` form and `REL` (aggregate imports `boundary_relative`).

## 5. NB-1 (CNA N-1): the ATTEMPTED partition vs `float_count`

**Agree. I hold it as a BLOCKER (fix-before-seal).**

The mechanism:
- `runstate.py:153–155` calls `phi_float(...)` and only then does `self.float_count += 1`.
- Inherited `world.observe_float` (`ckappa_oracle/world.py:185–189`) raises `ValueError("observation has predictive probability 0")` when `float(unnorm.sum()) == 0.0`. A ValueError therefore leaves `float_count` unchanged.
- S6 `_propagate` (`evaluate.py:107–109`) books that call as ATTEMPTED/`value_error` and returns. On a **non-scoreable** edit the run continues (`evaluate.py:403–405` stops only on scoreable edits; baselines stop at `:221–224`).
- At completion, `driver.py:185–197` compares `attempted_totals()["float"]` (which includes the value_error) with `float_count` (which excludes it), and raises INTEGRITY STOP.
- S2 value_errors stop anyway (`o1o2.py:254–256`), so S6 non-scoreable edits are the only path.

Reachability:
- The trigger needs an exact float zero predictive at one of four observation steps for a guard-invalid, non-scoreable edit. Its components can be negative, so exact cancellation is possible in principle.
- It cannot be ruled in or out statically without propagating the frozen 688,128 edits × predictors, which is not allowed here.
- The sealed oracle recorded 0 value errors (all 11 `value_error` counts in `outputs/results.json` are 0) over 784,960 float propagations. So the likelihood is very low. **UNVERIFIED / NEEDS-APPROVED-RUN.**

Why it is still a blocker: a false INTEGRITY STOP would void the single approved run, and v1.3 allows no retry.

The correct fix under v1.3's accounting identity:
- v1.3 C8.4 (L1231): "ATTEMPTED. Any call that was started, whatever its outcome. Attempted propagations are sub-classified as valid-finite, guard-invalid …, ValueError or non-finite."
- L1237: "attempted float propagations above 3,443,968 is INTEGRITY STOP".
- So the ledger is right and the counter is wrong. Count the call when it starts.
- In `runstate.phi`, keep the soft-deadline check first. Then wrap `phi_float` in `try/except ValueError:` that does `self.float_count += 1`, runs the overrun check and re-raises. An equivalent alternative is to increment before the call. Timing-sample accounting should stay success-only.
- Do **not** exclude `value_error` from the partition (`attempted_totals`). That would contradict C8.4.
- Add a unit test: a ValueError on a non-scoreable S6 edit must leave the partition equal to the counters.

## 6. Notes, including CNA's two notes

- **N-2 (fix before seal, minor).** `p0.py:89–92` writes `stage_S4_P0.json` with `status: "PASS"` **before any L/G comparison**. A SIGKILL before the final write (`:158–162`) leaves a premature PASS on disk. Fix: use `status: "DOMAINS_RECORDED"` (or `PENDING`) for the pre-comparison write.
- **N-3 (note).** The TOCTOU described in §3.
- **N-4 (CNA note 1: agree, note).** `rankcats.py:65–66` returns `ZERO` (σ₁ = 0, or an empty σ list) before the short-stack test at `:68`. That is a wording gap against RL-10. It is unreachable: a formed stack has ≥48 rows × 8 columns (`fits.py:557–565`, with an empty `usable` giving NOT_FORMED at `:540–556`), so NumPy returns 8 singular values. Optional fix: test `len(sigma) != 8` first.
- **N-5 (CNA note 2: agree, note).** `outputs_gate.py:41–50` compares `path.resolve()` with `root.resolve()/NAME`. Because the lstat check has already rejected a symlink at `path`, and `root` is resolved on both sides, the comparison and `relative_to` always pass. It is vacuous but harmless. The lstat check is the real guard.
- **N-6 (note).** `rankcats.py:32–33` still raises `ValueError("nonempty design missing sigma_1")`, which becomes EXECUTION ERROR, exit 1, not INTEGRITY STOP. It is unreachable, because `fit_from_svd` returns σ₁ for a nonempty design. For RL-8 consistency, make it `integrity_stop`.
- **N-7 (note).** The RL-6..RL-12 rulings copy (`_7da7.md`, `fc402c3d…`) is cited by sha in annex v4 but is not in the manifest's `items.governing` or `REQUIRED_GOVERNING`. Consider adding it at seal.
- **N-8 (note).** RL-8 labels a stopped run with its real kind, for example "CLASS-FIT VALIDATION NOT MET (INTEGRITY STOP)". v1.3 C7.1(1) names these conditions under PIPELINE INVALID. The diagnosis "PIPELINE INVALID (P0 / normalization / B3 short stack)" is carried in the reason, so both are visible. This is acceptable under the Lead ruling.
- **N-9 (note).** Annex v4's sha is not pinned in code. That is correct, because pinning it would be circular. It is bound only by the manifest, which the filed application must pin.

## 7. B0 (RL-4)

- **Arithmetic.** 61,464,576 = 60,024 kB × 1024 ✓. 61,464,576 + 316,737,056 = **378,201,632** < 4,000,000,000 ✓. The feasibility bound VmPeak ≤ 3,683,262,944 is unchanged ✓.
- **Budget constant unchanged.** The `pinned.py` diff 11efb513..515725d7 adds only shas and oracle constants. `PACKAGE_BUDGET_BYTES` is derived from the same unchanged integers (`pinned.py:125–141`), which I recomputed as 316,737,056 at 11efb513.
- **S0 rule** (live VmPeak + budget > 4e9 ⇒ INTEGRITY STOP; RSS is not an operand) is unchanged.
- **B0 itself is UNVERIFIED.** The box has Python 3.13.5 / NumPy 2.5.4 and cannot reproduce the pinned 3.12.3 / 1.26.4 measurement. S0 re-measures VmPeak live, so the annex figure is context only.

## 8. Summary for the parent

- **Verdict:** BLOCKERS (1: NB-1). After NB-1 is fixed, and given the N-2 status-word fix, I expect CLEAR WITH NOTES.
- **CNA comparison.** CNA rated the package CONFORMS with one fix-before-seal item. I agree on that item (NB-1) and rate it a blocker under my scale. I agree with both CNA notes at note level. I add N-2, which CNA did not raise, and the N-3 TOCTOU.
