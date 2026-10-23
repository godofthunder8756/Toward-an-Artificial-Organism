# C-κ oracle-only scope record v1.4: pre-seal resolutions N1–N4, n1–n5 (DRAFT for freeze. Not sealed, nothing run)

Constitutive agent, 2026-10-22 (ET). **Additive** under Astra #36 L162 ("If implementation reveals a substantive ambiguity or requires changing one of these rules, resolve it additively before execution."). Leaves unchanged: v1 (`1b450bcf…`), v1.1 (`e40c288f…`), v1.2 (`7e15e812…`), v1.3 (`f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5`), build script (`77d6cc49…`). Addresses the Delegate's delta check `ckappa_oracle_scope_record_v1_3_delta_check_RD.md` (`a70acb05…`), accepted in full.

## 0. Precedence
**v1.4 > v1.3 > v1.2 > v1.1**, except that the verbatim E36-1..14 text (v1.3 §1) governs over everything, including this file. A conflict with E36 found later is resolved additively before execution.

## N1. §5 outcome vocabulary and precedence (frozen)
Evaluated separately for ALL and for MARG at ε_syn = 0.1. **First match wins:**
1. **PIPELINE INVALID**: an O1, O2 or O6 fixture failure, or the O7 contradiction in N4(i). Stops the package.
2. **REFERENCE COVERAGE NOT MET**: in some fold, exact count coverage < 75% (integer test 4·n_scoreable < 3·n_total), or law-mass coverage clearly below 0.75 (below 0.75·(1 − 10⁻⁶)). This is not a mechanism or headroom statement.
3. **ZERO RESPONSE**: pooled S = 0 exactly (v1.3 §3).
4. **HEADROOM NOT MET**: any of √H\* or R\* clearly below its threshold t (x < t·(1 − 10⁻⁶)).
5. **BOUNDARY**: no clear failure, but at least one float statistic (√H\*, R\*, law-mass coverage) satisfies |x − t| ≤ 10⁻⁶·t.
6. **MET** (ALL) / **AVAILABLE** (MARG).

- The BOUNDARY band applies **only to float statistics**. Count coverage uses the exact integer test, so 96/128 is ≥ 75% and is not BOUNDARY.
- **Consequences:** for ALL, any outcome other than MET means no inference spec is drafted without a new ruling (v1.1 L123 extended). For MARG, anything other than AVAILABLE means MARG is descriptive only. Every label reports its reason and the underlying values.

## N2. Application before seal (replaces v1.3 §4 item 12 source line)
Sequence:
1. Code and the manifest draft are complete.
2. The Research Lead files the standing-approval application. It cites by sha256: v1.1, v1.2, v1.3, v1.4, the v1.3 build script, every implementation file, and the inputs (results.json at `5d9d8a7` and the protocol).
3. The application's path and sha256 are entered in the manifest.
4. The manifest is sealed (immutable, E36-14).
5. Step 0 may begin only once both the application and the sealed manifest exist.

The post-run index references the manifest sha. The application never references the manifest.

## N3. Solver cutoff consistent with the rank rule (amends v1.3 §3 "Solver")
- For every fit (O6 B and B_μ, O7, and the §6 commitment), the rank rule (v1.1 L68–73 plus E36-8) is applied to the singular values of the √w-weighted design **before** the fit.
- If any σ_i/σ_1 lies in the unresolved band [10⁻¹⁰, 10⁻⁶], equalities included, the cell is UNRESOLVED and **not scored**. It stays in the denominator.
- Otherwise the fit is `numpy.linalg.lstsq(A, y, rcond=1e-8)`. Because no ratio lies in [10⁻¹⁰, 10⁻⁶], every cutoff in that interval gives the same truncation: resolved directions are kept and resolved-zero directions are never inverted. σ_1 = 0 exactly means rank 0 and a zero fit (E36-8).

## N4. O7 rules (amends v1.3 §2 row 6)
- **(i)** A resolved third singular direction of O7's stacked Jacobian (σ₃/σ₁ > 10⁻⁶) is a demonstrated implementation contradiction (E36-7 and Astra's note). It means **STOP, PIPELINE INVALID**, an integrity diagnosis in the report, and no rerun. A ratio in the unresolved band reads UNRESOLVED and the package continues. Resolved lower rank is reported.
- **(ii) Granularity: whole fixture.** If the quadratic baseline (μ_x, μ_y, g(μ_x, μ_y)) is invalid (any p < 10⁻⁶) at **any** of the 16 prefixes, O7 as a whole reads **RESTRICTED COMPARATOR NOT ADMISSIBLE**. Its g coefficients and the list of invalid prefixes are reported. Its derivatives and predictions are not evaluated, and the package continues to O3. There is no refit, no replacement and no partial evaluation, because partial evaluation would change the frozen fold design.
- **(iii)** O7's derivatives, Pred_full and Pred_μ are all taken **about O7's own baseline chart (μ_x, μ_y, g(μ_x, μ_y))**. Disagreement with the true reachable oracle forecasts is reported separately (E36-6).

## n1, n2. Supersession map additions (to v1.3 §2)
| v1.1 text | Edit | Now reads |
| --- | --- | --- |
| L138 "(this is the κ-component accuracy floor, S-M4)" | E36-9 | **Withdrawn.** Floor (a) concerns total comparator prediction error only. |
| L142–147, the claim unit, quota and package labels | E36-11 | Replaced by E36-11's disjoint p/f/u/h counts. The claim unit stays the F-TRAINED seed, and the S-M6 marginal-wording rule stays, applied to E36-11 labels. |

**Owed by the later inference spec (E36-1):** the cell → seed status rules (rank or coverage UNRESOLVED cells, headroom-limited cells, how a seed's status is set across folds and both counted ε), the absolute response-magnitude floor, and the neural coverage rule. Nothing here settles them.

## n3. Overhead reserve (amends v1.2 D-2 as reordered by E36-13)
- Non-propagation overhead after step 0 is **omitted from T_rem** and covered by a fixed **60 s reserve** for serialization and report writing.
- **PROJECTION HALT** if T_rem > 600 s − 60 s − T_elapsed.
- **Soft deadline:** at T_elapsed = 540 s the package starts no new stage. It writes what it has and the report, then exits with the status CAP RESERVE REACHED (INCOMPLETE).
- **Hard cap:** independent of the projection, the wrapper (n4) kills the process at 600 s. That is reported as CAP REACHED.
- These three stop kinds are distinct in the outputs.

## n4. Wrapper and incremental outputs
- `run_package.sh` is a shell wrapper that is itself hashed in the manifest. It records T0 (`date +%s.%N`) before anything else and exports it as `CKAPPA_T0`. It then sets `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1` and runs:
  `prlimit --as=4000000000 -- taskset -c 0 timeout --signal=KILL <600 − (now − T0)>s python3 -m ckappa_oracle`
- The Python side measures T_elapsed against `CKAPPA_T0`, so interpreter startup and imports are inside the clock (E36-14).
- **Incremental outputs:** each completed stage (O1, O2, O6, O7, O3, O4, O5) writes its own `outputs/stage_<id>.json`, fsynced on completion. `results.json` collects them at the end. A kill loses at most the stage in progress. The post-run index is written by the wrapper after the process exits, whatever the exit status, and records the exit status and stop kind.

## n5. Memory
The cap is **4×10⁹ bytes** (`RLIMIT_AS`), matching Astra #35's "4 GB". The v1.3 §3 "4 GiB" reading is superseded.

## Other delta-check notes adopted
- **NumPy pinning.** The exact NumPy and Python versions are recorded in the manifest, and the run asserts them at startup; a mismatch stops before any work. The drawn Q, Q₂ and direction arrays are written to `outputs/drawn_arrays.npz`, and its sha256 goes in the post-run index.
- **"36000 + seed_id".** seed_id is the PR #7 seed number (100–109), so seeds are 36100–36109. This is prospective and applies to §6 only.
- **Field names.** Oracle edit sizes are the field `eps_syn`. The neural field `eps` does not occur in oracle outputs (Astra L7).
- **Output paths**, relative to the package root:
  - `outputs/stage_*.json`
  - `outputs/results.json`
  - `outputs/REPORT.md`
  - `outputs/run.log`
  - `outputs/drawn_arrays.npz`
  - `post_run_index.json`, outside `outputs/`

## Manifest checklist deltas (to v1.3 §4)
- **Item 1:** add sha256 of v1, v1.4 and the v1.3 build script.
- **Item 2:** name the W2 certificate, PR #4 `RESULTS.md`, and the results.json fields `certificate`, `freeze_commit` and `freeze_file_sha256`, all at `5d9d8a7`.
- **Item 6:** version pinning, and the drawn arrays as outputs.
- **Item 7:** add the N1 vocabulary and precedence, the `eps_syn` and `eps` fields, and the N3 rank-before-fit rule.
- **Item 8:** add the N4(i) O7 stop, the N4(ii) whole-fixture admissibility rule, and REFERENCE COVERAGE NOT MET.
- **Item 9:** add the n3 reserve, the soft deadline and the three stop kinds, plus the n4 wrapper.
- **Item 10:** 4×10⁹ bytes.
- **Item 11:** the paths above and incremental stage files.
- **Item 12:** the N2 sequence. The application sha is in the manifest, and the application is filed before the seal.

## Claim ceiling
Unchanged: oracle-only (v1.1 §8, Astra #36 L164). No checkpoint is opened. Nothing runs before the application is filed and the manifest is sealed.
