# C-κ class-fit package: implementation annex v1

**Binds to:** `review/ckappa_classfit_synthetic_scope_record_v1_3.md`, sha256 `a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`.

**Status: IMPLEMENTATION ANNEX v1 (E39-1, E39-10). NOT COMPLETE FOR SEAL (open fields in A8). NOT SEALED. NOTHING RUNS.**

Research Delegate (Track A), 2026-10-23 (ET). This file is immutable once hashed.
- Any change, including filling an A8 field, produces a new file (`ckappa_classfit_implementation_annex_v2.md`, and so on). The new file cites the same v1.3 sha256 and supersedes v1 by name.
- The annex's own sha256 is not written into v1.3, because that would create a circular reference. It is recorded in the posted report and must be recorded in the sealed manifest and the standing-approval application (v1.3 C9.6).
- The manifest is the root that binds both hashes.

**Governing text.** Astra #39 raw (`e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482`) > #38 > #37 > v1.3 > this annex.
- This annex supplies implementation details only.
- **It may not change the estimator, controls, masks, thresholds, directions, sizes, caps or claim ceiling. Any such change requires a new Astra ruling** (#39 L175; v1.3 C9.7).
- Where this annex and v1.3 appear to conflict, v1.3 governs, and the conflict goes to the pre-seal conformance review.

**Claim ceiling.** E38-15, unchanged (v1.3 C1; #39 L235). This annex establishes no result.

**Whether #39 allows open fields.**
- #39 L160–169: "Remaining implementation details may be completed before sealing … They must be fixed in a versioned, immutable implementation annex or manifest that is part of the frozen specification bundle … Implementation supplies exact array provenance, hashes, schema, file paths and resource estimates. … An independent pre-seal review checks that those details conform."
- So open fields are permitted **in this draft only**. Each must be filled, either in a later annex version or in the sealed manifest, and conformance-reviewed **before the seal** (E39-1: "The complete frozen bundle, standing-approval application and seal are required before S0").
- No field may be filled by inspecting an experimental outcome (E39-1).

I executed nothing beyond reading committed files and hashing their bytes. Every value below either cites its committed source or is marked **TO BE FILLED BY IMPLEMENTATION**, with the rule that fixes it.

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
| B0 | Interpreter, NumPy 1.26.4 and single-thread OpenBLAS address space, package imports, and the inherited O1/O2 code paths | Not derivable from committed files | **TO BE FILLED BY IMPLEMENTATION** |

- **Feasibility condition.** B0 + 298,133,024 ≤ 4,000,000,000, that is **B0 ≤ 3,701,866,976 B**.
- **Committed evidence about B0.** The sealed oracle run used the same Python, NumPy, thread settings and RLIMIT_AS (`run_package.sh`: `prlimit --as=4000000000`, `OPENBLAS_NUM_THREADS=1`). It completed (`outputs/run.log`: "stop COMPLETED exit 0"). So its whole-process address-space peak was below 4e9 B. That bounds B0 only loosely and does not establish the condition.
- **RLIMIT_AS limits virtual address space,** not RSS. Library reservations count toward it, which is why B0 cannot be inferred from object sizes.
- **Rule for B0 (A8).** B0 is filled before seal by one of:
  - (a) a static argument the conformance review accepts; or
  - (b) if the Research Lead rules it admissible, an import-only footprint observation that reads no input and runs no stage.

  Option (b) is not a synthetic pilot in #39 L237's sense, but #39 neither authorizes nor forbids it explicitly, so it needs the Research Lead's decision.
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

## A8. Open fields: TO BE FILLED BY IMPLEMENTATION before seal

#39 permits these to be completed before sealing, in an annex version or the manifest, subject to the independent pre-seal review (#39 L160–169; E39-1). None may depend on an experimental outcome.

| Field | Rule that fixes it | Destination |
|---|---|---|
| Module file list and per-file sha256 | the files as committed for review; hashes are of exact bytes | sealed manifest |
| Implementation commit hash | the commit containing the reviewed code | sealed manifest |
| B0 memory baseline | A4 rule (static argument, or an RL-admitted import-only observation) | annex v2 |
| `REPORT.md` template text | must follow v1.3 C10 and E37-3/E37-4 wording; no new claim | annex v2 |
| Manifest field names, and the application path and sha | follow the oracle manifest pattern (`manifest.json` keys: sealed, seal_status, standing_approval_application, precedence, items, frozen_runtime) | sealed manifest |
| Frozen-runtime constants for the new package | carry over the inherited values (`pinned.py:6–45`) wherever v1.3 uses them unchanged; add the new constants: SCHEDULED_FLOAT = 3,443,968; DECLARED_N_O1 = 272; the #38 tolerances; the system order | annex v2 or manifest |

Everything else in A1–A7 is complete as written, subject to conformance review.
