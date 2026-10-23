# C-κ class-fit package: implementation annex v2

**Binds to:** `ckappa_classfit_synthetic_scope_record_v1_3.md`, sha256 `a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`.

**Supersedes:** `ckappa_classfit_implementation_annex_v1.md` by name. The v1 file is retained byte-identical and is not edited.

**Status: IMPLEMENTATION ANNEX v2. A8 fields are filled below, except where a field is marked CONFORMANCE ITEM. NOT SEALED. NOTHING RUNS.**

**Implementation commit:** `315d9da9f7de10120374ea7b11c912e1b9f9c8a0`. That commit contains the module bytes hashed in A8. This annex is added in a later commit that does not change those bytes. This file does not contain its own sha256.

Research Delegate (Track A), 2026-10-23 (ET), carried forward. This file is immutable once hashed.
- Any further change produces a new annex file that cites the same v1.3 sha256 and supersedes v2 by name.
- The annex's own sha256 is not written into v1.3. It is recorded in the draft manifest. The manifest is the root that binds both hashes.
- v1.3 names the annex by the review-root path. The byte-identical copy, and this v2 file, live under `review/ckappa_classfit/`. That path difference is CI-GOVERNING-PATH. The v1.3 bytes were not edited to rename the path.

**Governing text.** Astra #39 raw (`e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482`) > #38 (`87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5`) > #37 (`ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2`) > v1.3 (`a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`) > this annex.
- This annex supplies implementation details only.
- **It may not change the estimator, controls, masks, thresholds, directions, sizes, caps or claim ceiling. Any such change requires a new Astra ruling** (#39 L175; v1.3 C9.7).
- Where this annex and v1.3 appear to conflict, v1.3 governs, and the conflict goes to the pre-seal conformance review.

**Claim ceiling.** E38-15, unchanged (v1.3 C1; #39 L235). This annex establishes no result.

A1–A7 below are the v1 text, carried unchanged, except the A4 B0 cell and the static argument that fills that open field. No stage S0–S8 was run. No import footprint was measured. Hashes below are of committed bytes.

---

## A1. Reused arrays: provenance and conventions (E39-10; #39 L171; v1.3 C5.2)

**Rule.** The package uses the **authenticated existing arrays** and does **not** regenerate them (#39 L171: "preserve the specified generator, dimensions, ordering, normalization and matrix-sign conventions, or use the authenticated existing arrays").

**Source (committed, read only).**

| Item | Value |
|---|---|
| Repository commit | `14376f38fe09157eef85bfac1cc4a4433d49bebc` (PR #13 head) |
| Array file | `outputs/drawn_arrays.npz`, file sha256 `1e7a599229cff0a1a61391b791139f30eff4f3a007007ba8de6a2e9177a0dea4` |
| Hash record | `outputs/drawn_array_hashes.json`, file sha256 `ce286f281d7ee2989657e59c2d474d122ecaf21537270999f63f299279aac2ce` |
| Generator code | `ckappa_oracle/draws.py`, sha256 `ce73d9496ac73e6ab86fddb0dbc96a74251b32a0b31e78da16e9d24670988457` |
| Frozen seeds | `ckappa_oracle/pinned.py:33–35` (`seed_Q` 35006, `seed_Q2` 35007, `seed_O6_directions` 35016); pinned.py sha256 `03c55323d0eb0b14fc463510738109d24e76ee9dc4623ba0e8c396e712363a68` |
| Runtime that generated them | Python 3.12.3, NumPy 1.26.4 (`pinned.py:6–7`) |

**Arrays used.**

| npz key | Used by | Shape | dtype / order | Seed | Generation procedure (verbatim from the hash record) | Raw-byte sha256 |
|---|---|---|---|---|---|---|
| `Q` | SYS-O6, SYS-PC, SYS-LIM | (8, 3) | `<f8`, C-contiguous | 35006 | "standard_normal((8, 3)); reduced QR; columns signed so diag(R) > 0" | `01cdf2abcdefb52570c59c4ed227404d085704ab755df17e0ed25d729dfef919` |
| `Q2` | SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3 | (8, 2) | `<f8`, C-contiguous | 35007 | "standard_normal((8, 2)); reduced QR; columns signed so diag(R) > 0" | `86159ba687c89cd445164398e748464174b651acca27ecd111aa9599569b6937` |
| `O6_directions` | all seven systems | (16, 8) | `<f8`, C-contiguous | 35016 | "standard_normal((16, 8)); each row divided by its Euclidean norm; signs applied later as +v then -v" | `5ed4bc8ba08bd9700bd9ad90c153301cf2fc7cc5c9a9b8f4477fb52ba0657c1d` |

- **Not used:**
  - `O7_directions`: the same bytes as `O6_directions`, shared with no second draw.
  - `O4_directions`: shape (64, 3), seed 35004, sha256 `6127c17d…3e58`.

  Neither is loaded for computation. Both may be hash-checked.
- **Generator** (`draws.py:33–57`): `numpy.random.Generator(numpy.random.PCG64(seed))`.
  - Q and Q₂ come from `standard_normal((8, k))` followed by `numpy.linalg.qr(mode="reduced")`. Each column is negated where diag(R) < 0, and a zero diagonal is an integrity stop.
  - Directions come from `standard_normal((16, 8))`, with each row divided by its Euclidean norm.
- **Ordering conventions.**
  - Direction index = row index 0–15. Signs are applied +v, then −v (v1.3 C5.2).
  - Q and Q₂ columns are in the order returned by QR. The embedding is z = Q·D⁻¹(ψ − ψ̄) (v1.3 C4).
- **Raw-byte sha256 convention** (`draws.py:15–19`): `hashlib.sha256(numpy.ascontiguousarray(a, dtype="<f8").tobytes()).hexdigest()`. This hashes row-major (C-order) little-endian IEEE-754 float64 bytes, with no header, shape or dtype bytes. The npz **file** hash authenticates the input bytes, but it is not the reproducibility check. The reproducibility check is the per-array raw-byte hash plus shape plus dtype. This is the inherited convention: `post_run_index.json` sets `drawn_arrays_npz_file_hash_is_reproducibility_check: false`.
- **Load rule (stage S0).**
  1. Read the file bytes with `git show 14376f38fe09157eef85bfac1cc4a4433d49bebc:outputs/drawn_arrays.npz`, following the inherited `inputs.py` git-object pattern. Verify the file sha256.
  2. Open with `numpy.load(..., allow_pickle=False)`.
  3. For each used key, verify the shape, `dtype.str == "<f8"`, C-contiguity and the raw-byte sha256 against the table above.
  4. Any mismatch is INTEGRITY STOP (exit 7).

  The arrays are never written back. Their hashes are restated in `stage_S0_preflight.json`.
- **I verified** (2026-10-23, by hashing the committed bytes, with no generation) that all five npz arrays match the hash record.

**Other committed inputs read by the package.**

| Input | Path at commit | sha256 | Use |
|---|---|---|---|
| Committed O7 coefficients | `14376f38…:outputs/stage_O7.json` | `994dda0a1e9f4194726abab2420033c8ae266c8802bcf962f7a38ce7c2350116` | SYS-NC1 refit equality check (v1.3 C4.4.R) |
| W2 world inputs (inherited) | `5d9d8a7d1274d58e27e9a18380d1a33faaab57cc`: `twostream_results_v1/results.json`, `twostream_results_v1/RESULTS.md`, `TWOSTREAM_PROTOCOL_v1.md` | `bf2de92c…1fed`, `8477e98c…7a3c`, `6ff31a0d…1098` (`pinned.py:51–53`) | World definition, as in the oracle |

No checkpoint or weight file is in the input set (v1.3 C1.2, C9.3).

## A2. Output schema (E39-10; v1.3 C3.6, C7.0, C8.3)

**Encoding (inherited, `io.py`).**
- UTF-8 JSON with `indent=2`, `sort_keys=True`, `allow_nan=False`. Non-finite floats are serialized as null (`io.py:30–55`).
- Every file is written atomically: write to `<name>.tmp`, flush, fsync, `os.replace`, then fsync the directory (`io.py:58–76`).
- Floats are written by Python's `json`, which gives shortest round-trip repr. Matrices are row-major nested lists, each also given a raw-byte sha256 (A1 convention).
- `eps_syn` values are the strings "0.02", "0.05", "0.1" and "0.25" (`pinned.py:29`).

**Enumerations.**

| Field | Values |
|---|---|
| system | `SYS-O6`, `SYS-PC`, `SYS-FK`, `SYS-NC1`, `SYS-NC2`, `SYS-NC3`, `SYS-LIM` |
| fold | `AB->CD`, `CD->AB`, `AC->BD`, `BD->AC`, `AD->BC`, `BC->AD` (`geometry.py:15–22`) |
| class | `I`, `X`, `Y`, `XY` |
| eval_orbit | `A`, `B`, `C`, `D` |
| group | `ALL`, `MARG`, `XOR` (`geometry.py:24–29`) |
| fit_type | `global`, `class` |
| mode | `weighted`, `unweighted` |
| predictor | `actual`, `global_full`, `global_mu`, `class_full`, `class_mu` |
| rank_category | `FULL`, `LOWER`, `ZERO_NONEMPTY`, `UNRESOLVED`, `UNAVAILABLE_EMPTY` (v1.3 C3.3(a′)) |
| identity_status | `PASS`, `FAIL`, `NOT_EVALUATED`, `NOT_APPLICABLE_RANK`, `REFERENCE_RANK_UNRESOLVED`, `UNAVAILABLE`, `NOT_APPLICABLE_VOIDS`, `INVESTIGATE` (D7 only) |
| b3_status | `PASS`, `UNRESOLVED-B3`, `ZERO`, `RESOLVED_THIRD_DIRECTION` (the last one stops), `NOT_FORMED` |
| accounting_category | `ATTEMPTED`, `SKIPPED_PRIOR_STOP`, `SKIPPED_SYSTEM_INADMISSIBLE`, `SKIPPED_PREFIX_VOID`, `SKIPPED_UNAVAILABLE_MAP`, `UNKNOWN_AFTER_LAST_DURABLE` |

**Record types.** Counts are scheduled maxima from v1.3 C8.3.

| Record | Keys | Max count | Location |
|---|---|---|---|
| Base loss record (E39-6) | system, fit_type, fold, class, eval_orbit, group, eps_syn, mode, L_mu, L_full, S, gain, n_scoreable, n_total, law_mass_scoreable, law_mass_total | 16,128 | `eval_<system>.json` → `loss_records` |
| Pooled aggregate | system, fit_type, group, eps_syn, mode, L_mu, L_full, S, gain, R, sqrt_H, n_scoreable, law_mass, formed (bool), not_formed_reason | 336 | `results.json` → `pooled` |
| Coverage record | system, fold, class (null for the per-fold row), eps_syn, n_total, n_scoreable, law_mass_total, law_mass_scoreable, count_rule_pass, mass_rule_pass, crossings | 840 | `eval_<system>.json` → `coverage` |
| Identity record (E39-3) | system, identity_id, kind ∈ {matrix, finite_recovery, finite_equality, zero_gain, diagnostic}, fit_type, fold, class, group, eps_syn, premise_rank_category, status, max_abs_residual, tolerance_abs, tolerance_rel, scale, n_tested, worst_edit | 1,128 | matrix kind: `fit_freeze_<system>.json`; others: `eval_<system>.json` → `identities` |
| Guard-consistency record (E39-4) | system, predictor, fit_type, fold, class, eps_syn, n_actual_valid_tested, n_stop_mismatch (actual valid, predictor invalid), n_reverse_mismatch_recorded (actual invalid, predictor valid; non-stopping), first_mismatch {edit, min_p_actual, min_p_predicted, chart_diff_max_abs, recovery_residual_max_abs or null} | 456 | `eval_<system>.json` → `guard_consistency` |
| Rank report | system, fit_type, fold, class, map ∈ {full, mu, b3_stack, nc1_g}, n_rows, n_cols, sigma (full list), sigma_1, ratios, rank_category, n_inverted, b3_status (stacks only) | 541 | `fit_freeze_<system>.json`; `nc1_g` in `stage_S3_construction.json` |
| Fitted matrix | system, fit_type, fold, class, map ∈ {B, A}, values (row-major), sha256 | 420 | `fit_freeze_<system>.json` |
| Normal-equation term | system, scope (prefix / fold / fold×class), id, name ∈ {G, r, sumG, sumr, sumG_mumu, sumr_mu}, values, sha256 | 112 + 112 + 840 | `fit_freeze_<system>.json` |
| Cancellation diagnostic | system, orbit, name, value, tolerance, scale | 84 scalars + 12 vectors | `fit_freeze_<system>.json` |
| P0 comparison | chart ∈ {true, SYS-FK, SYS-NC1}, kind ∈ {L, G, P_exact}, a, g, u (null for G), residual_max_abs, tolerance, pass | ≤ 2,304 + 144 + 768 | `stage_S4_P0.json` |
| P0 omitted pair (E39-10) | chart, a, g, reason ∈ {VOID_a, VOID_ga, VOID_both} | ≤ 96 | `stage_S4_P0.json` |
| Accounting record (E39-7) | system, stage, unit ∈ {propagation, fit, b3_stack}, scheduled, per-category counts, closed (bool) | 7 × 9 × 3 = 189 | `results.json` → `accounting` |
| Label record | system, fit_type, group, label, first_failing_reason, flags (all stored per E38-8) | 7 × 2 × 2 at reference size, plus VALIDATION and HEADROOM | `results.json` → `labels` |

**Per-file top-level keys.**
- `stage_S0_preflight.json`: stage, sealed, manifest_sha256, annex_sha256, scope_sha256, application_sha256, input_hashes, reused_arrays (A1 table, recomputed), runtime_observed {python, numpy}, rlimit_as_observed, cpu_affinity_observed, t_elapsed_s.
- `stage_S1_O1.json`: the inherited O1 payload keys (`stages.py:292–309`), plus `P_sum_exact` (rational string) and `P_a_exact` (16 rational strings). Exact rationals are stored as `"p/q"` strings, following the inherited `fraction_text`.
- `stage_S2_O2.json`: the inherited O2 payload.
- `stage_S3_construction.json`: per system: normalization (mean, sd, raw-byte sha256), admissibility, voided prefixes with min_p, and L/J/G table hashes. Also: nc1_g {coefficients, committed_coefficients, max_abs_diff, tolerance, rank report}; rms {rho_NC1, M4, P_sum_float, c2, c3, summation_order: "sequential a=0..15"}; t_exact (rational string, must equal v1.3 C4.5); crossing bounds at full precision.
- `stage_S4_P0.json`: P0 comparisons, omitted pairs and status per chart.
- `fit_freeze_<system>.json` (×7): fitted matrices, rank reports, B3 stacks, normal-equation terms, matrix identity records, cancellation diagnostics, `frozen_before_evaluation: true`.
- `eval_<system>.json` (×7): loss records, coverage, identity records (finite), guard-consistency records, crossing counts, D6/D7 diagnostics (SYS-LIM), accounting for that system.
- `results.json`: pooled aggregates, labels, VALIDATION, HEADROOM, accounting, timing sample (first 1,000 stage-S6 propagations: key and q, as inherited `runstate.py:84–97`), projection, stop_kind, exit_code, float_propagations, exact_propagations, t_elapsed_s (with source named, E37-2).
- `REPORT.md`: human-readable report under v1.3 C10. Template: TO BE FILLED BY IMPLEMENTATION (A8).

## A3. Paths (E39-10)

Proposed fixed paths. They are chosen so that **no sealed oracle artifact can be overwritten**: the oracle uses `outputs/`, `manifest.json` and `post_run_index.json` at the repo root.

| Artifact | Path (repo-relative) |
|---|---|
| Package module | `ckappa_classfit/` |
| Wrapper | `run_classfit_package.sh` |
| Manifest | `classfit_manifest.json` |
| Output directory | `classfit_outputs/` |
| Wrapper post-run index | `classfit_post_run_index.json` |
| Scope, annex | `review/ckappa_classfit_synthetic_scope_record_v1_3.md`; `review/ckappa_classfit_implementation_annex_v<N>.md` |

The module's file list and sha256s are TO BE FILLED BY IMPLEMENTATION (A8).

## A4. Memory and resource estimate (E39-10; #39 L173; RLIMIT_AS = 4,000,000,000 B)

**Status: analytic, UNVERIFIED, no pilot and no measurement** (#39 L173: "No pilot execution is needed for this estimate"). The per-object budgets below are **design allocations** that the implementation must respect. They are not measured sizes.

| # | Component (#39 L173 category) | Basis | Bytes |
|---|---|---|---|
| 1 | Numeric arrays (library data) | L tables 5·256·9·8 = 92,160; J tables 7·256·24·8 = 344,064; G_a and r_a 7·16·33·8 = 29,568; fitted matrices 7·30·40·8 = 67,200; normal-equation sums 7·30·53·8 = 89,040; reused arrays 168·8 = 1,344 | 623,376 (exact arithmetic) |
| 2 | Numerical-library workspace | Largest design 384×3 (9,216 B) with 384×8 target (24,576 B); largest B3 stack 384×8 (24,576 B); SVD workspace for at most 384×8. Budget | ≤ 1,048,576 |
| 3 | Python objects: baseline cache | 7 × 256 entries; budget 1,024 B per entry (key tuple, q and belief arrays) | 1,835,008 |
| 4 | Python objects: timing sample | 1,000 retained entries (inherited `runstate.py:84–97`); budget 1,024 B each | 1,024,000 |
| 5 | Exact arithmetic | Inherited O1 rationals: ≤ 2,928 Fractions (beliefs 64, terminals 1,024, history probabilities 256, forecasts 768, charts 816), plus P_a, P_sum and t; budget 1,024 B per Fraction | ≤ 2,998,272 |
| 6 | Aggregation records | ≤ 23,026 records (loss 16,128; aggregates 336; coverage 840; identity 1,128; guard 456; rank 541; P0 3,312; accounting 189; cancellation 96); budget 2,048 B per record as a Python dict | 47,157,248 |
| 7 | Serialization | JSON-ready copy of row 6 (`io.py:json_ready`) plus indented JSON text, each budgeted at 2,048 B per record | 94,314,496 |
| 8 | Per-edit transient | 5 charts, 5 beliefs, 5 forecasts and residuals; budget | ≤ 65,536 |
| **I** | **Incremental total** (rows 1–8) | | **149,066,512** |
| **I×2** | With a factor-2 allowance for allocator fragmentation and arena overhead | | **298,133,024** (7.45% of RLIMIT_AS) |
| B0 | Interpreter, NumPy 1.26.4 and single-thread OpenBLAS address space, package imports, and the inherited O1/O2 code paths | Not derivable from committed files | **NOT ESTABLISHED (CR-4).** No byte count is stated. The static argument is below. |

- **Feasibility condition.** B0 + 298,133,024 ≤ 4,000,000,000, that is **B0 ≤ 3,701,866,976 B**.
- **Committed evidence about B0.** The sealed oracle run used the same Python, NumPy, thread settings and RLIMIT_AS (`run_package.sh`: `prlimit --as=4000000000`, `OPENBLAS_NUM_THREADS=1`). It completed (`outputs/run.log`: "stop COMPLETED exit 0"). So its whole-process address-space peak was below 4e9 B. That bounds B0 only loosely and does not establish the condition.
- **RLIMIT_AS limits virtual address space,** not RSS. Library reservations count toward it, which is why B0 cannot be inferred from object sizes.
- **Rule for B0 (A8).** B0 is filled before seal by one of:
  - (a) a static argument the conformance review accepts; or
  - (b) if the Research Lead rules it admissible, an import-only footprint observation that reads no input and runs no stage.

  Option (b) is not a synthetic pilot in #39 L237's sense, but #39 neither authorizes nor forbids it explicitly, so it needs the Research Lead's decision.

**B0 static argument (option (a) only; no import measurement; no pilot).**
- File sizes of the interpreter, NumPy, and OpenBLAS are not virtual address space. RLIMIT_AS counts mappings and reservations (the A4 note above).
- The sealed oracle run used the same Python, NumPy, thread settings, and RLIMIT_AS, and its log records completion under that cap. That shows one process which imported those libraries and the inherited O1/O2 paths stayed under 4,000,000,000 B. It does not separate B0 from the rest of that process, and it does not show B0 ≤ 3,701,866,976.
- No import-only footprint was taken. Option (b) was not used.
- **CONFORMANCE ITEM CR-4.** The numeric B0 byte count stays unfilled. The feasibility condition is not established by this annex.

- **In-run observations** (no behavior change). At each stage end the package logs `resource.getrusage(RUSAGE_SELF).ru_maxrss` and `/proc/self/status` VmPeak to `run.log` as observations, naming the source (E37-2). A `MemoryError` under the cap ends the run as incomplete (v1.3 C8.5), not as a scientific result.
- **CPU and time.** One CPU via `taskset -c 0` with BLAS threads set to 1 (inherited wrapper). The runtime estimate is ≈ 95.3 s (v1.3 C8.7), UNVERIFIED.
- **Disk.** Not capped. Record sizes are budgeted at ≤ 2,048 B of JSON text each, so all outputs together come to ≈ 47 MB at most (row 6 count × 2,048 B). UNVERIFIED.

## A5. Artifact inventory and durable counters (E39-7, E39-10; #39 L120–122)

**Core files (21; v1.3 C8.3), all in `classfit_outputs/`.**

| # | File | Written at | Writer |
|---|---|---|---|
| 1 | `stage_S0_preflight.json` | end of stage S0 | package |
| 2 | `stage_S1_O1.json` | end of stage S1 | package |
| 3 | `stage_S2_O2.json` | end of stage S2 | package |
| 4 | `stage_S3_construction.json` | end of stage S3 | package |
| 5 | `stage_S4_P0.json` | end of stage S4 | package |
| 6–12 | `fit_freeze_SYS-O6.json`, `fit_freeze_SYS-PC.json`, `fit_freeze_SYS-FK.json`, `fit_freeze_SYS-NC1.json`, `fit_freeze_SYS-NC2.json`, `fit_freeze_SYS-NC3.json`, `fit_freeze_SYS-LIM.json` | stage S5, per system, before any stage-S6 propagation | package |
| 13–19 | `eval_SYS-O6.json` … `eval_SYS-LIM.json` (same order) | stage S6, at each system's end | package |
| 20 | `results.json` | stage S7 (on a stop: at the stop) | package; on forced termination, a minimal file by the wrapper if absent, with `"writer": "wrapper"` (inherited `run_package.sh`) |
| 21 | `REPORT.md` | stage S8 | package |

- An inadmissible system still gets its `fit_freeze_` and `eval_` files. They contain `system_inadmissible: true`, no fits and no propagations, plus the skipped-work accounting (E39-7). The count of 21 is therefore unconditional.
- After a stop, files for unreached stages are absent. Their absence is recorded in the post-run index (null hash).

**Additional files, listed separately (#39 L122).**

| File | Purpose | Writer |
|---|---|---|
| `classfit_outputs/run.log` | Append-only log: stage events, memory observations (A4) and **durable counter checkpoints** | package |
| `classfit_outputs/stop_kind.json` | `{exit_code, stop_kind}` | package; wrapper if absent (inherited) |
| `classfit_post_run_index.json` | t0, kill budget, exit status, stop kind and source, manifest path and sha, sha256 of every core and additional file (null if absent) | wrapper, after the process ends (inherited pattern) |
| `*.tmp` | Transient atomic-write files | Removed by `os.replace`. A leftover `.tmp` after a forced kill is listed in the post-run index as an incomplete write. |

**Durable counters (E39-7; #39 L120).**
- Checkpoints are written as `COUNTERS <json>` lines in `run.log`. Each line is flushed and fsynced.
- They are written at the end of each stage, after each system's baselines, after each (system, fold) in stage S6, and at every package-detected stop. That is ≤ 5 + 7 + 7 + 42 + 2 = 63 lines for a complete run.
- Each line holds the full category counts per system and unit (A2 accounting record), the float and exact totals and t_elapsed.
- After forced termination, the report reconstructs counts only up to the last complete `COUNTERS` line. Every later interval is reported as `UNKNOWN_AFTER_LAST_DURABLE`, and the run is marked INCOMPLETE.

**Exit codes (inherited).** 0 completed; 2 PIPELINE INVALID (`stages.py:51–54`); 3 PROJECTION HALT; 4 CAP RESERVE REACHED; 6 STEP 0 SAMPLE SHORT (`runstate.py`); 7 INTEGRITY STOP (`io.py:20–21`); 124/137 CAP REACHED (wrapper).

## A6. Deterministic event ordering (E39-2, E39-3, E39-10)

Within a stage, nothing depends on timing, hashing order or set iteration. Every loop below iterates in the stated order.

- **Stage S0.** Clock T0 in the wrapper before the interpreter starts. Then: manifest load and seal assertion; hash checks of scope, annex, application, code and inputs; A1 array checks; runtime observation.
- **Stage S1.** The inherited O1 order (`stages.py:144–311`). Exact P_a and P_sum are formed here and stored. The assertion runs at stage S3.
- **Stage S2.** The inherited O2 order.
- **Stage S3.** Systems in the order SYS-O6, SYS-PC, SYS-FK, SYS-NC1, SYS-NC2, SYS-NC3, SYS-LIM. For each:
  1. System-level normalization.
  2. For SYS-NC1 only: coefficient refit (inherited `stages.py:740–751`), then the committed-coefficient check.
  3. For SYS-NC2 and SYS-NC3: exact ΣP assertion, then ρ_NC1, then c₂ and c₃ (v1.3 C4.4.R). This requires SYS-NC1 first, which the order guarantees.
  4. For SYS-LIM: exact t and its comparison with the frozen rational.
  5. Baseline validity, voiding and admissibility.
  6. L table if the chart is new, then the J and G tables (prefix 0–15, u 0–15).
  7. Full-precision crossing bounds (SYS-PC, SYS-LIM).
- **Stage S4.**
  1. The law-level P_exact comparisons, in (a 0–15, g X→Y→XY, u 0–15) order.
  2. Then for each chart (true, SYS-FK, SYS-NC1 if admissible), in the same order: L comparisons for each applicable (a, g), then G comparisons, recording omitted pairs.
  3. Any failure stops.
- **Stage S5.** Admissible systems in system order. For each, folds in `FOLD_SPEC` order:
  1. global full, then global μ;
  2. classes I, X, Y, XY, each full then μ;
  3. B3 stacks for that fold: global, then classes I to XY (SYS-FK and SYS-NC1–NC3 only).

  Each matrix identity check runs immediately after its fit. Each system's `fit_freeze` file is written and fsynced before the next system.
- **Stage S6.** Admissible systems in system order. For each system:
  1. **Baselines:** prefix 0–15 ascending, u 0–15. Voided prefixes are skipped.
  2. **Edits:** fold (`FOLD_SPEC` order) → evaluation prefix (ascending) → u (0–15) → direction index (0–15) → sign (+1, −1) → ε_syn (0.02, 0.05, 0.1, 0.25). This is the inherited nesting (`stages.py:546–553`).
  3. **Within an edit:**
     1. actual chart; crossing test (SYS-PC, SYS-LIM: a crossing is an integrity stop);
     2. predicted charts (global full, global μ, class full, class μ);
     3. guard evaluations;
     4. propagations in the order actual, global full, global μ, class full, class μ, each skipped only per v1.3 C8.4 precedence;
     5. **streaming checks:** guard consistency, finite recovery and finite equality, each with tested-edit counts. A failure stops at once (E39-3);
     6. common-mask loss accumulation into the base records for both modes;
     7. counters.
  4. A `COUNTERS` checkpoint after each fold. The `eval_` file is written after each system.

  The timing sample is the first 1,000 stage-S6 propagations: SYS-O6's 256 baselines, then 744 edit propagations. The projection follows the inherited formula (`runstate.py:114–141`), with N_float_remaining = 3,443,968 − completed.
- **Stage S7.** Pooling, labels, VALIDATION, then the HEADROOM gates (v1.3 C7), all from stored records. No finite identity is first evaluated here.
- **Stage S8.** `REPORT.md`; final `results.json` and `stop_kind.json`; process exit. Then the wrapper writes `classfit_post_run_index.json`.

## A7. P0 applicability domains (E39-10; v1.3 C4.0)

| Chart | Comparison | Domain | Max count | Omitted pairs recorded |
|---|---|---|---|---|
| (law) | P_h(g·a, g·u) = P_h(a, u), exact rationals | all a 0–15, g ∈ {X, Y, XY}, u 0–15 | 768 | none (law-level) |
| true | L, G | all (a, g). True-chart baselines are exact O1 beliefs and are never voided. | 768 L + 48 G | none expected; any omission would be an integrity stop |
| SYS-FK | L, G | (a, g) with a and g·a both non-voided on the SYS-FK chart | ≤ 768 L + 48 G | yes: (a, g, VOID_a / VOID_ga / VOID_both) |
| SYS-NC1 | L, G | only if SYS-NC1 is admissible; (a, g) with a and g·a both non-voided | ≤ 768 L + 48 G | yes, as above |
| SYS-NC2, SYS-NC3 | — | not applicable (symmetry broken by design) | 0 | n/a |

- An L comparison covers the 3×3 matrix at one (a, g, u). A G comparison covers the 3×3 matrix at one (a, g). Tolerances are per v1.3 C5.5.
- The domain sets are written to `stage_S4_P0.json` before the comparisons. Losses, identities and coverage use only the domains declared in v1.3 C5.3 and A2. No other domain is used (E39-10).


## A8. Fields filled in v2

#39 permits these to be completed before sealing. None depends on an experimental outcome. The standing-approval application is not filed, so its path and sha256 stay null in the draft manifest.

### Module file list and per-file sha256

Bytes of implementation commit `315d9da9f7de10120374ea7b11c912e1b9f9c8a0`.

| Path | sha256 |
|---|---|
| `ckappa_classfit/__init__.py` | `d62a51c78144ca1bcfaff7db4f148b245deea34f42858b1c0f198a6d01f87ea0` |
| `ckappa_classfit/__main__.py` | `f03238fbb9a311f1afc7476308e4cba80a44d56b60ecfc8446f450a9a05b51c2` |
| `ckappa_classfit/accounting.py` | `91f22bdba716d57827cdb7580488c8544f46c88ad650dd9c5398e06a835f257f` |
| `ckappa_classfit/aggregate.py` | `90b5fd26019f80d200ff94a1a73313d69fe7214693b24dd94dd8dc2759adbc29` |
| `ckappa_classfit/arrays.py` | `9af98b49ab048be0595b71a801e92b03d9b2f2ce5d75e75a450c6343f8e571a4` |
| `ckappa_classfit/classes.py` | `115df4f03c9e76e3213bc543190287e3ac140601a11efcab4eaed6467036d219` |
| `ckappa_classfit/construction.py` | `133ab38e29d16dcc0238082b4763224fb6c1bc46ec5e16a23e8ac0384d3f32b7` |
| `ckappa_classfit/driver.py` | `35160ec67a3e5d9db6b5d9c00ad7a51249ed4b9916fb5edcf6b838113d848025` |
| `ckappa_classfit/evaluate.py` | `f87684fc58d8cfe05cf7e33bd6f6497e624b32e102902454ff1f68580f0eb57a` |
| `ckappa_classfit/fits.py` | `39096fe4528b21d7a2b2320b1bb32f561b7f5eee8ef6cac613a2438cd4a82b34` |
| `ckappa_classfit/gate.py` | `82f79eafffe96248282f5051fcae7b9c64e1e009681153e1063eb1caa1878e18` |
| `ckappa_classfit/inputs.py` | `2486b03257678cf4161d03d1fd0327498373d98ae9df636af92c2404b606c7dc` |
| `ckappa_classfit/o1o2.py` | `8db5e1e5f06b1cc61844768c44b0133510968f397584cdaae147e8d04c9f917f` |
| `ckappa_classfit/p0.py` | `02a04cc8345e8252cea1400b78a8e2bbc117d62bbb05b65cedabaeba8d4090e4` |
| `ckappa_classfit/pinned.py` | `f36a4c472758d73e92750816d9184ad7c27092005577daa13089dc89f304c80b` |
| `ckappa_classfit/preflight.py` | `74fa96eca38915a45ec388722ca523454ee54a252edc5f29211ece2a92590d86` |
| `ckappa_classfit/rankcats.py` | `c7062b4647fa663262a4679ea6eab57399b09ba9990ab0a6d529969f0fcae870` |
| `ckappa_classfit/records.py` | `7e05faaf3cd7e1a8e74aab112ad90faa9af13896be1f56ab106118dbc79fe122` |
| `ckappa_classfit/report.py` | `417e926f33caa3da67afd39f924d0f55e6391dca77a4f07f8798c8d2d5d09d72` |
| `ckappa_classfit/runstate.py` | `9b1bcc8e4b40b36fadf8c3e5bfa2c6cf9c6e789c7196c7975a74fd675e8e29cc` |
| `ckappa_classfit/schedule.py` | `778304aca18b59b95f62a32e8131786998ec082a4ee341c85a64f064a8269b49` |
| `ckappa_classfit/static_checks.py` | `04cb4ddad60400e9bbc3b85233085f0b76d293ca780e7c646782a6a6d54e6cc7` |
| `run_classfit_package.sh` | `d14b84c151f257fd3162a682fee66b36fc115dcb635db24db694f83f40575a4d` |

`classfit_manifest.json` and this annex are not module files. Their hashes belong in the manifest, and this annex does not contain its own hash.

### Implementation commit hash

`315d9da9f7de10120374ea7b11c912e1b9f9c8a0`

### B0 memory baseline

Option (a), static argument only, in A4 above. **CONFORMANCE ITEM CR-4:** no numeric byte count is stated. Option (b) was not performed.

### `REPORT.md` template text

The stage S8 template is the following text. Stored labels are appended after it. It states no new claim. It does not hard-code a draft or bundle status word.

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
UNRESOLVED-B3 is not described as a passed guard. NOT EVALUATED is not described as a passed identity.

D7 INVESTIGATE is retained prominently. Any later decision about neural work must address it. Unchanged labels do not resolve it. D7 INVESTIGATE is non-stopping and stays outside VALIDATION and HEADROOM.

The class label is supplied by the analyst from the prefix index. Class models have 4 times the parameters of the global model. The extended B3 guard is not described as applicable to neural two-coordinate systems.

Elapsed time, when a figure is printed below, is results.json field t_elapsed_s. Its source is time.time() minus CKAPPA_CLASSFIT_T0.
Memory, when a figure is printed below, is the run.log observation ru_maxrss_kb from resource.getrusage(RUSAGE_SELF).ru_maxrss, and VmPeak from /proc/self/status.
No new claim is stated.
```

### Manifest field names

Draft file: `classfit_manifest.json`. `sealed` is false. The application is pending.

| Field | Draft value |
|---|---|
| `document` | C-kappa class-conditioned synthetic package manifest DRAFT |
| `sealed` | false |
| `seal_status` | UNSEALED |
| `standing_approval_application.status` | PENDING |
| `standing_approval_application.path` | null |
| `standing_approval_application.sha256` | null |
| `draft_note` | states that stage S0 requires sealed true and a filed application |
| `precedence_rule` | #39 raw > #38 > #37 > v1.3 > annex v2; annex v1 superseded by name |
| `precedence` | rank, name, path, sha256 |
| `items.governing` | path, role, sha256 |
| `items.inputs` | path_at_commit, commit, sha256, opened_by_package |
| `items.implementation.implementation_commit` | `315d9da9f7de10120374ea7b11c912e1b9f9c8a0` |
| `items.implementation.implementation_files` | path, sha256, equal to the module list above plus nothing else |
| `frozen_runtime` | the object below; preflight requires exact equality with `ckappa_classfit.pinned.FROZEN_RUNTIME` |

The application path and sha256 are null because no application has been filed. Inventing a path would not fill the field. **CONFORMANCE ITEM CI-APPLICATION-PENDING.**

`items` uses these names rather than the oracle draft's numeric item ids, because preflight reads `items.implementation.implementation_files` and `items.governing`. **CONFORMANCE ITEM CI-MANIFEST-ITEMS-SHAPE.**

No `phase` key is present. **CONFORMANCE ITEM CI-MANIFEST-PHASE.**

### Frozen-runtime constants

Inherited `ckappa_oracle/pinned.py` values are copied by value. The inherited key `scheduled_float_propagations` stays 788480. The class-fit maximum is the new key `classfit_scheduled_float_propagations` = 3443968. **CONFORMANCE ITEM CI-SCHEDULE-KEY.**

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

## A9. Open conformance items

v1.3 CR-1 through CR-5 stay open for the pre-seal review.

- **CR-1.** Guard consistency stops only in the actual-valid direction. The reverse is recorded and does not stop.
- **CR-2.** The SYS-NC1 refit uses the inherited float P_a accumulation. The RMS rule uses exact-law P_a converted once.
- **CR-3.** D6 diagnostic matrix residuals are six cells, one per fold, with the residual equal to the max of the B and A residuals. Diagnostic only.
- **CR-4.** The numeric B0 byte count is not established. Static argument only. No import measurement.
- **CR-5.** Paths are `classfit_outputs/`, `classfit_manifest.json`, `classfit_post_run_index.json`, and `run_classfit_package.sh`.

Further items, each a literal reading rather than a new design:

- **CI-ACCOUNTING-ATTRIBUTION.** The 272 exact calls and the 1,536 O2 float calls are attributed to SYS-O6 in the 7×9×3 grid, because those totals are not divisible by 7. The sum across systems recovers the package maxima.
- **CI-B3-SHORT-STACK.** A formed stack with fewer than three singular values has no third ratio. `b3_status` is PASS. The enum has no other non-stop value.
- **CI-NC-ONE-VOID.** C4.4.R (any matched baseline invalid) and C7.1 (≥5 voids) are both applied. Any void makes the NC system inadmissible, so the ≥5 clause does not add a further case.
- **CI-LIM-SIGNS.** Declared signs are stored as `sign_matches_declared`. A mismatch is not an extra C8.6 stop. The readout uses the state's own |ψ₁|−t.
- **CI-LIM-BASELINE-BOUNDARY.** If a baseline |μ_x| equals t, the branch sign is 0. That case is recorded by the sign function and is not a separate stop.
- **CI-JOINT-PREMISE-TIMING.** The SYS-PC global B and A identities share the joint rank premise and are checked after both fits of that fold.
- **CI-EMPTY-FIT-CATEGORY.** An empty fit design is SKIPPED_UNAVAILABLE_MAP. SKIPPED_PREFIX_VOID is reserved for per-prefix propagations.
- **CI-LOWER-RESIDUAL.** A lower-rank fit may store a matrix residual with n_tested 0 and status NOT_APPLICABLE_RANK. It does not stop.
- **CI-PARTIAL-MASK.** If any of the four maps is empty or unresolved, neither fit type's comparative losses for that cell are formed.
- **CI-BASELINE-TOLERANCE.** The true-chart baseline versus the O1 exact forecast stores max abs and has no pass/fail threshold, because none is declared.
- **CI-EXIT-CODES.** P0, the normalization assertion, and a guard inconsistency are PIPELINE INVALID with exit 7. O1/O2 failures and control-identity failures (matrix, finite recovery, zero-gain) are PIPELINE INVALID with exit 2. B3 third direction, crossing, NC1 refit mismatch, t mismatch, hash, accounting, array, and version mismatches are INTEGRITY STOP exit 7. An unsealed manifest is PREFLIGHT FAILED exit 5.
- **CI-SCHEDULE-KEY.** See the frozen-runtime section.
- **CI-T0-ENV.** The wrapper clock variable is CKAPPA_CLASSFIT_T0.
- **CI-MANIFEST-PHASE.** No phase key. `seal_status` is present because the manifest pattern requires that key.
- **CI-HEADROOM-MET-LABEL.** The met label is MET for both ALL and MARG.
- **CI-NC1-FINITE-EQ-CELLS.** SYS-NC1 has 72 descriptive zero-gain cells and no separate finite Pred_full−Pred_μ cell. Descriptive, non-stopping.
- **CI-D6-A-INSIDE-ONE-CELL.** See CR-3.
- **CI-UNFORMED-VS-ZERO.** A base loss record has no separate formed flag. `n_scoreable` null means the comparison was not formed. `n_scoreable` 0 with null losses means the cell was formed and the denominator was zero.
- **CI-LAW-MASS-BOTH-MODES.** Both modes store the law mass of the cell. The unweighted loss denominator is the occurrence count.
- **CI-GOVERNING-PATH.** See the preamble.
- **CI-ATTEMPTED-DETAIL.** `attempted_detail` adds valid_finite, guard_invalid, value_error, and non_finite under ATTEMPTED. The six terminal categories remain the closure categories.
- **CI-REPRESENTATIVE-MU.** `representative_mu_positive` is stored. A false value is not an extra stop.
- **CI-LABEL-INADMISSIBLE.** An inadmissible NC system has no coverage rows, so C7.1 item 3 does not fire. The label is RESTRICTED COMPARATOR NOT ADMISSIBLE.
- **CI-RESULTS-WRITE-STAGE.** A5 names results.json at stage S7. A6 names the final results.json at stage S8. The driver serializes it once, after S7 returns, during S8.
- **CI-APPLICATION-PENDING.** Application path and sha256 are null until a filing exists.
- **CI-MANIFEST-ITEMS-SHAPE.** See the manifest section.
- **CI-GLOBAL-AGGREGATES.** Orbit-level global aggregates are not stored. The 336 pooled aggregates are stored.
- **CI-SINGLE-PREFIX.** Single-prefix fits are absent. The scheduled count is 0.
- **CI-CANCELLATION-DIAGNOSTIC.** Orbit cancellation sums are diagnostic and do not stop.
- **CI-MU-RECOVERY-PREMISE.** A fixed-κ recovery check uses that map's μ rank category. A full-map recovery check uses the full rank category.

Nothing in this annex was produced by running stage S0–S8, and the manifest is not sealed.
