# C-κ class-fit package: implementation annex v3

**Binds to:** `ckappa_classfit_synthetic_scope_record_v1_3.md`, sha256 `a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`.

**Supersedes:** `ckappa_classfit_implementation_annex_v2.md` by name. Annex v2 sha256 `5d6daf06fea3466ff2fc1eebf73414f12c47daeccfe06095ec7a3efb64907262`. The v2 file is retained byte-identical and is not edited. Annex v1 sha256 `8614bf114b127f4bdab516c0e933c23c84d1cd5f4d0ef34837d5cb0ad453d3a8` stays byte-identical.

**Status: IMPLEMENTATION ANNEX v3. NOT SEALED. NO STAGE S0–S8 WAS RUN.**

**Implementation commit:** `12b816ef0b72409d5baf0875d5acab00f9c78676`. That commit contains the module bytes hashed in A8. This annex is added in a later commit that does not change those bytes. This file does not contain its own sha256. The unsealed draft manifest records it.

Research Lead implementation rulings RL-1 through RL-5, 2026-10-23. These rulings came out of the pre-seal review. Annex v2 was written before they were applied. No new Astra ruling is required. This annex may not change the estimator, controls, masks, thresholds, directions, sizes, caps, or claim ceiling.

**Governing text.** Astra #39 raw (`e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482`) > #38 (`87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5`) > #37 (`ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2`) > v1.3 (`a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`) > this annex.
- Annex v2 remains the carried A1–A7 text except where an RL ruling below replaces a named field.
- Where this annex and annex v2 conflict, this annex governs, because it supersedes v2 by name.
- Where this annex and v1.3 conflict, v1.3 governs.

**Claim ceiling.** E38-15, unchanged. This annex establishes no result.

**What was executed.** `python -m py_compile` on the package modules, `python -m ckappa_classfit.static_checks` on hand-made fixtures, and one import-only `python3 -c` for B0. No declared data were fit or evaluated. No checkpoint or weight file was opened. `classfit_manifest.json` is not sealed.

---

## RL-1. rho_NC1 determinism (completes E39-9)

**Ruling.** rho_NC1 is computed from the refitted g over all 16 exact-law prefixes, regardless of SYS-NC1's prefix voiding or admissibility. It is a coefficient rule, not a map fit, so E39-7's skip rule does not apply.

**Implementation.** `rho_nc1_exact_law` in `ckappa_classfit/construction.py`.
- Arguments are the refitted coefficient vector, the exact-law μ_x and μ_y, and the exact-law P_a. There is no void set, admissibility flag, run object, or ledger argument.
- The length of each sequence must be 16. A shorter list is INTEGRITY STOP. The sum is the sequential left-to-right sum over a = 0, 1, …, 15 from C4.4.R.
- P_a are the exact-law prefix probabilities, each converted once with `float`. P_sum_exact must equal 1 before the coefficients are formed. A failure is the existing normalization PIPELINE INVALID and is not repaired by rescaling.
- ‖Dg‖² uses the inherited `g_gradient` on the refitted coefficients.
- The call sits in stage S3 after the SYS-NC1 coefficient refit and before SYS-NC1's chart, void report, or admissibility exist. A later void or an inadmissible SYS-NC1 does not recompute or drop a prefix.
- The function does not call the E39-7 ledger. It is not one of the scheduled map fits.
- `stage_S3_construction.json` field `rms` records `rho_NC1`, `M4`, `P_sum_float`, `c2`, `c3`, `summation_order` (`sequential a=0..15`), `n_prefixes` (16), `prefix_domain` (`exact-law a=0..15`), `independent_of_sys_nc1_voids` (true), `independent_of_sys_nc1_admissibility` (true), `e39_7_skip_applied` (false), and `unit` (`coefficient_rule`).

The SYS-NC1 refit itself is unchanged. It still uses the inherited float P_a accumulation so that it can match the committed coefficients (annex v2 CR-2). That refit is a scheduled construction fit. rho_NC1 is not.

Hand-made static fixtures put all of the probability mass on prefix 0 and, separately, on prefix 15. Both return rho_NC1 = 2 for g = 2 μ_x. A 1-prefix list stops.

## RL-2. Reverse guard record (CR-1)

**Ruling.** The reverse guard direction (actual invalid, predictor valid) is recorded and does not stop. It has its own record, separate from `first_mismatch`, with the same fields: the minimum p on each side, the chart difference, and the residual.

**Implementation.** In `ckappa_classfit/evaluate.py`, each guard cell keeps two records.
- `first_mismatch` is the first actual-valid, predictor-invalid event. That direction still stops, as PIPELINE INVALID, and is still described as a guard inconsistency rather than as proof that the recovery tolerance was exceeded.
- `first_reverse_mismatch` is the first actual-invalid, predictor-valid event. It increments `n_reverse_mismatch_recorded` and does not stop. A later event in the same cell does not replace it. A later stopping mismatch does not replace it.
- Both records, when present, have `edit`, `min_p_actual`, `min_p_predicted`, `chart_diff_max_abs`, and `recovery_residual_max_abs`. A missing belief, chart, or forecast leaves the corresponding field null.
- The guard-consistency row in `eval_<system>.json` always has both keys. An empty direction is null.

The forward direction is unchanged. The FULL-rank premise of the guard check is unchanged.

## RL-3. D6 cells (CR-3)

**Ruling.** D6 cells are reported as residual plus premise status only, with no PASS or FAIL in `identity_status` or anywhere else. INVESTIGATE belongs to D7 only.

**Implementation.** `ckappa_classfit/fits.py` function `_d6` no longer calls the pass/fail identity check.
- The residual is the maximum of the B residual and the A residual, when those residuals exist. It is stored as `max_abs_residual`.
- `premise_rank_category` is the joint rank premise of the full map and the μ map.
- `status` is the identity_status field. It is only a premise status:

| Premise | `status` |
|---|---|
| `UNAVAILABLE_EMPTY` | `UNAVAILABLE` |
| `UNRESOLVED` | `REFERENCE_RANK_UNRESOLVED` |
| `LOWER` or `ZERO_NONEMPTY` | `NOT_APPLICABLE_RANK` |
| not full, or no residual | `NOT_EVALUATED` |
| full rank premise and a residual is stored | `REPORTED` |

- `REPORTED` means the rank premise holds and the residual is stored. v1.3 C4.5 keeps that result REPORTED ONLY. It is not a pass and not a failure. A residual above 1e-9 stays `REPORTED`.
- `tolerance_abs` and `tolerance_rel` are null. A stored tolerance would be a verdict threshold.
- Before the record is appended, a walk rejects any string value or key equal to `PASS`, `FAIL`, or `INVESTIGATE`. That rejection is INTEGRITY STOP.
- D6 does not stop on the residual.
- D6 rows are not copied into label `identity_status`. They stay outside VALIDATION and HEADROOM, as in annex v2.
- D7 still uses `INVESTIGATE` when an applicable full-rank identity fails. That flag is non-stopping and is the only `INVESTIGATE` status.

`n_tested` is 1 when a residual is stored and 0 otherwise. It counts whether a residual was formed. It is not a verdict.

## RL-4. Memory budget and measured B0 (CR-4)

**Ruling.** Add the 420 fitted-matrix records, the 1,064 normal-equation records, the label records, and serialization overhead to the memory estimate. Measure B0 import-only under the pinned run environment and the real wrapper settings. The RLIMIT_AS comparison is VmPeak plus the package budget against 4e9 B. Peak RSS is context only. S0 re-measures B0 and raises INTEGRITY STOP if VmPeak + package budget > 4e9 B.

### Updated design budget

Annex v2 rows 1–5 and row 8 are unchanged. Row 6 gains the records below. Row 7 is the annex v2 serialization rule applied to those records: a JSON-ready copy and the indented JSON text, each budgeted at 2,048 B, so 4,096 B per record. The factor of 2 remains the arena allowance. These are design allocations, not measured object sizes.

| Added records | Count | Basis |
|---|---|---|
| Fitted matrices | 420 | annex v2 A2, one B or A matrix per scheduled fit |
| Normal-equation records | 1,064 | 112 prefix G + 112 prefix r + 840 fold terms |
| Label rows | 28 | 7 systems × 2 fit types × 2 groups |
| VALIDATION | 1 | one record |
| HEADROOM | 1 | one record; the ALL and MARG gates sit inside it |
| **Added records** | **1,514** | |
| Added row-6 bytes | 3,100,672 | 1,514 × 2,048 |
| Added row-7 serialization | 6,201,344 | 1,514 × 4,096 |

| # | Component | Bytes |
|---|---|---|
| 1–5, 8 | Unchanged from annex v2 | 7,594,768 |
| 6 | Aggregation and stored records, 24,540 × 2,048 | 50,257,920 |
| 7 | Serialization of row 6, 24,540 × 4,096 | 100,515,840 |
| **I** | Incremental total | **158,368,528** |
| **I×2** | Package budget, with the factor-2 allowance | **316,737,056** |

The annex v2 incremental total was 149,066,512. Adding 3,100,672 + 6,201,344 gives 158,368,528. Twice that is 316,737,056. `ckappa_classfit.pinned.PACKAGE_BUDGET_BYTES` is this integer. It is not a key of `FROZEN_RUNTIME`.

**Feasibility condition.** VmPeak + 316,737,056 ≤ 4,000,000,000, that is **VmPeak ≤ 3,683,262,944 B**. RSS is not an operand. RLIMIT_AS limits virtual address space.

### Measured B0

Option (b), authorized by this Research Lead ruling. One import-only process. No input was read, no system was built, and no stage was executed. `classfit_outputs/` was absent after the process. `ckappa_classfit.__main__` was not imported: that module's body calls `main()` and would execute stages S0–S8. Its bytes are still in the A8 file list. Every other package module was imported by name.

Wrapper settings, checked inside the process: `prlimit --as=4000000000`, `taskset -c 0` (affinity `{0}`), `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`.

| Observation | Value |
|---|---|
| `sys.version` | `3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0]` |
| `numpy.__version__` | `1.26.4` |
| VmPeak | `57784 kB` = **59,170,816 B** (`/proc/self/status`; kB = 1024 B) |
| VmHWM, peak resident set, context only | `33856 kB` = 34,668,544 B |
| `ru_maxrss`, context only | 33,760 KiB = 34,570,240 B (`resource.getrusage(RUSAGE_SELF).ru_maxrss`; Linux reports KiB) |
| RLIMIT_AS soft, hard | 4,000,000,000, 4,000,000,000 |
| VmPeak + package budget | 59,170,816 + 316,737,056 = **375,907,872** |
| Against 4e9 B | 375,907,872 ≤ 4,000,000,000. The condition holds for this measurement. |

The two RSS figures differ by 96 KiB. Neither enters the comparison.

**Static argument, retained as a cross-check.** File sizes of the interpreter, NumPy, and OpenBLAS are not virtual address space. The sealed oracle run used the same Python, NumPy, thread settings, and RLIMIT_AS, and its log records completion under that cap. That shows one process which imported those libraries and the inherited O1/O2 paths stayed under 4,000,000,000 B. It does not separate B0 from the rest of that process. The measured VmPeak above is the byte count this ruling asked for. The static argument does not replace it.

### S0 re-measurement

`check_b0_budget` in `ckappa_classfit/preflight.py` reads VmPeak at the end of preflight, before any class-fit quantity is computed. It adds `PACKAGE_BUDGET_BYTES` and raises INTEGRITY STOP when the sum is greater than `FROZEN_RUNTIME["memory_bytes"]` (4,000,000,000). If VmPeak cannot be read, that is also INTEGRITY STOP. The observation stored for stage S0 includes VmPeak, the sum, and the RSS fields. The RSS fields are labeled context only. The annex's 59,170,816 B figure is not reused as a substitute for the live VmPeak.

This S0 check was not executed. The manifest is unsealed, so preflight would stop on `sealed is not true` before the budget check on a real run. The predicate `address_space_exceeds` was checked on hand-made integers only.

## RL-5. Output directory and sealed-oracle rehash (CR-5)

**Ruling.** S0 asserts that `classfit_outputs/` is absent or empty, or INTEGRITY STOP. The post-run index re-hashes the sealed oracle artifacts from PR #13 (`manifest.json` sha `4179b71a…` and the `outputs/` files) and records whether they match. It does not stop.

**S0.** `check_outputs_directory` runs at the start of `preflight`, before `Run` creates the directory. Absent and empty are accepted. A non-directory or any directory entry is INTEGRITY STOP. Hand-made temporary directories covered absent, empty, and nonempty. The nonempty case raised INTEGRITY STOP. The repository's `classfit_outputs/` was absent during this work.

**Post-run index.** `run_classfit_package.sh`, after the package process has exited, hashes `manifest.json` and each path in `ORACLE_SEALED_OUTPUT_SHA256`. Each row is `{sha256, expected_sha256, match, stops}`. `stops` is false on a match and on a mismatch. A missing file is a mismatch and does not change the process exit status. An import or hash error is stored in `oracle_rehash_error` and still does not change the exit status. The index fields are `oracle_artifact_rehash`, `oracle_rehash_error`, and `oracle_rehash_stops` (false).

Expected manifest sha256: `4179b71a0110903472d6506686b2f7e0ab2188d9050c9c3f40c31a2fb6b46831`.

Expected `outputs/` sha256 values, copied from the sealed `post_run_index.json` and not recomputed by opening those files in this change:

| Path | sha256 |
|---|---|
| `outputs/REPORT.md` | `6c6d42ccefa224ec2e94a77f9f9c6169c318abee1db89decb4d0335a987e0785` |
| `outputs/drawn_array_hashes.json` | `ce286f281d7ee2989657e59c2d474d122ecaf21537270999f63f299279aac2ce` |
| `outputs/drawn_arrays.npz` | `1e7a599229cff0a1a61391b791139f30eff4f3a007007ba8de6a2e9177a0dea4` |
| `outputs/fit_freeze_O6.json` | `b6f817c8b3e70ae78e405f57e27226b08d1daec8fdbce7b2a1348a4c119e454a` |
| `outputs/fit_freeze_O7.json` | `347bcd511fe94648751473d182ed5118b2e57e04207ee5b3e4f1385e8c16bd05` |
| `outputs/results.json` | `6adb5de2650f5017b3f4195c84cf4b6955abb94186a01c92795efe0717dd0023` |
| `outputs/run.log` | `64f9af66c9b4154b314e08b10663f8e479fd323de6fb0af9812e35921b0a8977` |
| `outputs/stage_O1.json` | `794746a728caf4ff6211e6612ce007ae6f670084f2f4df898bc7ea3af692c3ec` |
| `outputs/stage_O2.json` | `4220a4df77511f48745a95f46064293ebff4d22b1368b435fbb102bb9c4818f1` |
| `outputs/stage_O3.json` | `2e30e9ad027fa4c5718a2e2b81a482429c3520b39ac215121ab26b96134a6539` |
| `outputs/stage_O4.json` | `7213d1709d8409dd7f49874f5fcb1a97e32dc58a8396316743d66f27cc918b3d` |
| `outputs/stage_O5.json` | `c61f6639a348542928fecdb82823b35928f56820626114973800c28f000c03ad` |
| `outputs/stage_O6.json` | `1a894f14501a19f783f50d13f4718f0ea45f32b77f9a810ada7da5147a9705b8` |
| `outputs/stage_O7.json` | `994dda0a1e9f4194726abab2420033c8ae266c8802bcf962f7a38ce7c2350116` |
| `outputs/stop_kind.json` | `2d5e1da5d451ba9addbafd9815b93163427c618d25732038531e07e49b6eb19a` |

The wrapper was not executed. The comparison function was checked on hand-made digests. A mismatch returned `stops: false`.

---

## A8. Fields filled in v3

The standing-approval application is not filed. Its path and sha256 stay null. The Research Lead files the application.

### Module file list and per-file sha256

Bytes of implementation commit `12b816ef0b72409d5baf0875d5acab00f9c78676`.

| Path | sha256 |
|---|---|
| `ckappa_classfit/__init__.py` | `d62a51c78144ca1bcfaff7db4f148b245deea34f42858b1c0f198a6d01f87ea0` |
| `ckappa_classfit/__main__.py` | `f03238fbb9a311f1afc7476308e4cba80a44d56b60ecfc8446f450a9a05b51c2` |
| `ckappa_classfit/accounting.py` | `91f22bdba716d57827cdb7580488c8544f46c88ad650dd9c5398e06a835f257f` |
| `ckappa_classfit/aggregate.py` | `2deae2886b62285c6a4ec934f42ad69319f221a3a26b590e1b4ab49e8bdac2f6` |
| `ckappa_classfit/arrays.py` | `9af98b49ab048be0595b71a801e92b03d9b2f2ce5d75e75a450c6343f8e571a4` |
| `ckappa_classfit/classes.py` | `115df4f03c9e76e3213bc543190287e3ac140601a11efcab4eaed6467036d219` |
| `ckappa_classfit/construction.py` | `6f7bdd150a12b465860ca12306f3c0d8d9284bc24cd8c36b9042c9ea14fc774e` |
| `ckappa_classfit/driver.py` | `70c6761577e8bb96ae50a394ddadadde19c39c887b23dde3cd4c343a76b4694f` |
| `ckappa_classfit/evaluate.py` | `2a0776faef5abb411b283230392b4c7bedd022d4a31d6a146e499173c08ff710` |
| `ckappa_classfit/fits.py` | `8524f4b4ef4ffa6af6a3c95fa677b33b87e63e122a7ece654cd2a8b5ef8c6382` |
| `ckappa_classfit/gate.py` | `82f79eafffe96248282f5051fcae7b9c64e1e009681153e1063eb1caa1878e18` |
| `ckappa_classfit/inputs.py` | `2486b03257678cf4161d03d1fd0327498373d98ae9df636af92c2404b606c7dc` |
| `ckappa_classfit/o1o2.py` | `8db5e1e5f06b1cc61844768c44b0133510968f397584cdaae147e8d04c9f917f` |
| `ckappa_classfit/p0.py` | `02a04cc8345e8252cea1400b78a8e2bbc117d62bbb05b65cedabaeba8d4090e4` |
| `ckappa_classfit/pinned.py` | `6f43b6ec86a72acfbdcbc7656cffc38e89524b42c228c5a46bd28997fa09f694` |
| `ckappa_classfit/preflight.py` | `811d4b5436989af1eb323d2a4ffc851e273b6cc68e2a9287d6285f1a49de52ca` |
| `ckappa_classfit/rankcats.py` | `c7062b4647fa663262a4679ea6eab57399b09ba9990ab0a6d529969f0fcae870` |
| `ckappa_classfit/records.py` | `7e05faaf3cd7e1a8e74aab112ad90faa9af13896be1f56ab106118dbc79fe122` |
| `ckappa_classfit/report.py` | `cca04d79b06cabd1c410c5ccb0e2040764946d7ebeb956c4e169b29a4fd0e984` |
| `ckappa_classfit/runstate.py` | `9b1bcc8e4b40b36fadf8c3e5bfa2c6cf9c6e789c7196c7975a74fd675e8e29cc` |
| `ckappa_classfit/schedule.py` | `778304aca18b59b95f62a32e8131786998ec082a4ee341c85a64f064a8269b49` |
| `ckappa_classfit/static_checks.py` | `f819a4dc5c6ff7061415d6b31a5224fbaadc84ecc88767fff416e44800b950a2` |
| `run_classfit_package.sh` | `3558780fe5c2c9ac1a69a1e4df3c7ce51542d501783ec7b1318e6505d77b4c82` |

`classfit_manifest.json` and this annex are not module files. Their hashes belong in the manifest.

### Implementation commit hash

`12b816ef0b72409d5baf0875d5acab00f9c78676`

### B0 memory baseline

Measured VmPeak **59,170,816 B** under Python 3.12.3 and NumPy 1.26.4, as in the RL-4 table. Peak RSS is context only (VmHWM 34,668,544 B; `ru_maxrss` 34,570,240 B). The package budget compared with that VmPeak is 316,737,056 B. The static argument in RL-4 is a cross-check and is not the byte count.

### `REPORT.md` template text

The stage S8 template is the following text. Stored labels are appended after it. It states no new claim. It does not hard-code a draft or bundle status word. Two sentences were added for RL-2 and RL-3: the reverse guard does not stop, and D6 reports residual plus premise status with no PASS or FAIL.

```
# C-kappa class-conditioned synthetic package

Claim ceiling, E38-15, verbatim:
This package tests implementation identities, synthetic response headroom and limitations of declared intervention-prediction models on specified synthetic systems. It establishes no result about trained GRUs and answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY. Confound gains do not identify an independent covariance register or exclude two-coordinate mediation or reachable-set lookup implementations. Failure of a class-conditioned criterion does not exclude nonlinear, prefix-dependent or orbit-dependent covariance codes. No result establishes acquisition, recurrent-transition-specific use, necessity, irreducible joint state, C4, C5, consciousness, autopoiesis or life.

E37-10, verbatim:
Any subsequent neural result is limited to prediction of intervention-induced forecasts by the declared prefix-conditioned oracle response models. It does not identify the reachable-history algorithm, establish acquisition, isolate the recurrent transition from the readout, exclude general lookup implementations, or establish irreducible joint state, C4 or consciousness.

Retained #38 L202 sentence, verbatim:
Failure of the declared class-conditioned criterion does not exclude orbit-dependent covariance codes, including codes whose local coordinate relation differs on held-out orbits.

E37-3, verbatim:
O7's zero gain follows from its symmetry-preserving global least-squares construction: complete flip-orbit fits, invariant continuation weights, a constant marginal-state map, and the declared odd-in-each-marginal lookup. It is not evidence that two-coordinate systems generally lack kappa-row gain. Comparator loss divided by response energy is not described as an orthogonal allocation of that energy.

E37-4, verbatim:
Failure of the global-map intervention criterion means that the declared criterion was not met. It does not establish absence of covariance sensitivity, absence of a global direction, or absence of a nonlinear or prefix-dependent coordinate relation. The prospective S6 design does not proceed to checkpoint inference unchanged.

Ratio wording: Comparator squared prediction error divided by actual response energy.
Oracle labels, when quoted from the earlier oracle package: Oracle-scale headroom only.
Cap-limited work is incomplete.
When a stored label says a declared criterion failed, the wording is one of these two sentences:
The declared global-map intervention-prediction criterion was not met.
The declared class-conditioned-map intervention-prediction criterion was not met.

Permitted SYS-PC success sentence. It is printed again below only when the stored class label is IDENTITY AS DERIVED and both stored VALIDATION and HEADROOM labels are MET. This template does not assert that those labels hold:
The class-conditioned fit recovered the declared sign-dependent synthetic map, which the global fit cancels as derived.
That sentence does not show that a network uses κ, carries a class label, or has a covariance register.
Headroom thresholds are synthetic conventions.

FK checks the κ row on the product-chart designs, not on the SYS-O6/SYS-PC designs.
No impossibility of alternatives is stated.

SYS-LIM is described only with this failure statement: in the CD, BD and BC fitting folds, full-rank recovery produces the negative-sign chart map, which is wrong on held-out A whenever the edit has a nonzero relevant component.
A declared transport rule using the state's magnitude could represent this system; the selected maps do not contain that rule.
SYS-LIM is not a two-coordinate system.
Compatible with two-coordinate mediation is not applied to SYS-LIM.

SYS-NC1 is described as a varying-κ two-coordinate confound.
RMS matching is never described as matching response, conditioning, transferability or GRU geometry.
SYS-NC1 and SYS-NC3 are not called affine.
SYS-PC and SYS-LIM are called affine only within their declared non-crossing branches.
Affine claims stay with their system and domain.

A guard inconsistency is reported with margins and residuals. It is not described as proof that the recovery tolerance was exceeded.
The reverse guard direction is recorded on its own and does not stop.
UNRESOLVED-B3 is not described as a passed guard. NOT EVALUATED is not described as a passed identity.

D6 cells report the residual and the premise status only. They do not carry PASS or FAIL. INVESTIGATE belongs to D7 only.
D7 INVESTIGATE is retained prominently. Any later decision about neural work must address it. Unchanged labels do not resolve it. D7 INVESTIGATE is non-stopping and stays outside VALIDATION and HEADROOM.

The class label is supplied by the analyst from the prefix index. Class models have 4 times the parameters of the global model. The extended B3 guard is not described as applicable to neural two-coordinate systems.

Elapsed time, when a figure is printed below, is results.json field t_elapsed_s. Its source is time.time() minus CKAPPA_CLASSFIT_T0.
Memory, when a figure is printed below, is the run.log observation ru_maxrss_kb from resource.getrusage(RUSAGE_SELF).ru_maxrss, and VmPeak from /proc/self/status.
No new claim is stated.
```

### Manifest field names

Draft file: `classfit_manifest.json`. `sealed` is false. The application is pending. This annex does not seal the file.

| Field | Draft value |
|---|---|
| `document` | C-kappa class-conditioned synthetic package manifest DRAFT |
| `sealed` | false |
| `seal_status` | UNSEALED |
| `standing_approval_application.status` | PENDING |
| `standing_approval_application.path` | null |
| `standing_approval_application.sha256` | null |
| `draft_note` | states that stage S0 requires sealed true and a filed application, and that annex v3 records RL-1 through RL-5 |
| `precedence_rule` | #39 raw > #38 > #37 > v1.3 > annex v3; annex v3 supersedes annex v2 by name; annex v1 superseded by name and retained |
| `precedence` | rank, name, path, sha256 |
| `items.governing` | path, role, sha256, including this annex once the draft manifest is updated |
| `items.inputs` | path_at_commit, commit, sha256, opened_by_package |
| `items.implementation.implementation_commit` | `12b816ef0b72409d5baf0875d5acab00f9c78676` |
| `items.implementation.implementation_files` | path, sha256, equal to the module list above |
| `frozen_runtime` | the object below; preflight requires exact equality with `ckappa_classfit.pinned.FROZEN_RUNTIME` |

The application path and sha256 are null because the Research Lead files the application.

`items` uses these names rather than the oracle draft's numeric item ids, because preflight reads `items.implementation.implementation_files` and `items.governing`.

No `phase` key is present.

### Frozen-runtime constants

`FROZEN_RUNTIME` is unchanged from annex v2. The RL-4 budget integers are module constants beside it, not keys of this object. Inherited `scheduled_float_propagations` stays 788480. `classfit_scheduled_float_propagations` stays 3443968.

```json
{
  "all_R": "0.05",
  "all_sqrt_H": "1e-3",
  "array_commit": "14376f38fe09157eef85bfac1cc4a4433d49bebc",
  "base_loss_record_maximum": 16128,
  "boundary_relative": "1e-6",
  "cancellation_abs": "1e-12",
  "cancellation_rel": "1e-10",
  "certificate": "two-stream world-admission analytic certificate v1",
  "classfit_declared_n_o1": 272,
  "classfit_scheduled_exact_remaining": 0,
  "classfit_scheduled_float_propagations": 3443968,
  "comparison_abs": "1e-12",
  "comparison_rel": "1e-10",
  "coverage_fraction": "0.75",
  "declared_n_o1": 272,
  "drawn_arrays_file_sha256": "1e7a599229cff0a1a61391b791139f30eff4f3a007007ba8de6a2e9177a0dea4",
  "edit_maximum": 688128,
  "eps_syn": [
    "0.02",
    "0.05",
    "0.1",
    "0.25"
  ],
  "exact_t": "6299716077234553896/15613266622202707711",
  "fd_step": "1e-6",
  "freeze_commit": "c69deb44b3c9ad06f176dae76fdaf311b992a665",
  "freeze_file_sha256": "c654a12176aebe0ab5ea4ee3c3b1e6a3c6167bd2b0df34b997fcaf28802dd280",
  "guard": "1e-6",
  "hard_kill_seconds": 595,
  "input_commit": "5d9d8a7d1274d58e27e9a18380d1a33faaab57cc",
  "marg_R": "0.02",
  "marg_sqrt_H": "1e-4",
  "matrix_forecast_recovery_max_abs": "1e-9",
  "memory_bytes": 4000000000,
  "numpy": "1.26.4",
  "o2_tolerance": "1e-8",
  "o4_direction_count": 64,
  "o4_sizes": [
    "0.1",
    "0.25",
    "0.5"
  ],
  "o6_direction_count": 16,
  "o6_tolerance": "1e-9",
  "o7_sigma3_stop_above": "1e-6",
  "o7_void_stop_count": 5,
  "prefix_count": 16,
  "protocol_sha256": "6ff31a0dcecf123c7796fb2ba6fa4735c4efb7f968dbbcad19e46e4ff0151098",
  "python": "3.12.3",
  "rank_resolved_above": "1e-6",
  "rank_resolved_zero_below": "1e-10",
  "rcond": "1e-10",
  "reference_eps_syn": "0.1",
  "reserve_seconds": 60,
  "results_json_sha256": "bf2de92c9cd09809ad85145827922e9a70d6e742d30f8828d6c4973e92b51fed",
  "results_md_sha256": "8477e98c77860c61e997580a73d35d160711806d00b6789df55fe597b5b37a3c",
  "sample_propagations": 1000,
  "scheduled_exact_remaining": 0,
  "scheduled_float_propagations": 788480,
  "section6_seeds_prospective": [
    36100,
    36101,
    36102,
    36103,
    36104,
    36105,
    36106,
    36107,
    36108,
    36109
  ],
  "seed_O4_directions": 35004,
  "seed_O6_directions": 35016,
  "seed_Q": 35006,
  "seed_Q2": 35007,
  "single_prefix_fits": 0,
  "soft_deadline_seconds": 540,
  "stage_o7_file_sha256": "994dda0a1e9f4194726abab2420033c8ae266c8802bcf962f7a38ce7c2350116",
  "summation_order_rho_c3": "sequential a=0..15",
  "svd_maximum": 541,
  "system_order": [
    "SYS-O6",
    "SYS-PC",
    "SYS-FK",
    "SYS-NC1",
    "SYS-NC2",
    "SYS-NC3",
    "SYS-LIM"
  ],
  "zero_gain_abs": "1e-18",
  "zero_gain_rel": "1e-9"
}
```

RL-4 constants, outside `FROZEN_RUNTIME`:

| Name | Value |
|---|---|
| `PACKAGE_BUDGET_BYTES` | 316737056 |
| `INCREMENTAL_BYTES` | 158368528 |
| `FITTED_MATRIX_RECORDS` | 420 |
| `NORMAL_EQUATION_RECORDS` | 1064 |
| `LABEL_RECORDS` | 30 |
| `ORACLE_SEALED_MANIFEST_SHA256` | `4179b71a0110903472d6506686b2f7e0ab2188d9050c9c3f40c31a2fb6b46831` |

## Disposition of annex v2 conformance items

- **CR-1** is RL-2. The reverse direction has its own record and does not stop.
- **CR-2** is unchanged. The refit still uses the inherited float P_a accumulation. The RMS rule still uses exact-law P_a converted once.
- **CR-3** is RL-3. D6 is residual plus premise status. INVESTIGATE is D7 only.
- **CR-4** is RL-4. The numeric B0 byte count is the measured VmPeak, 59,170,816 B. The comparison uses VmPeak, not RSS.
- **CR-5** is RL-5. S0 requires `classfit_outputs/` absent or empty. The post-run index re-hashes the sealed oracle artifacts and does not stop.

Nothing in this annex was produced by running stage S0–S8, and the manifest is not sealed.
