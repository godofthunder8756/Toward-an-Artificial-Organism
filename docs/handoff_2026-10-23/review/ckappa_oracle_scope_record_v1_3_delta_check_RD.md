# Delta check: C-κ oracle-only scope record v1.3 (E36) against Astra #36

Research Delegate, 2026-10-22 (ET). **Review only.**
- Nothing in the package was run. No filter was propagated and no checkpoint was loaded.
- I did **not** run the build script: it writes into `/workspace/review` and overwrites v1.3. My only computation was a separate text-matching script, kept under `/workspace/scratch/ckappa_v13/`.
- No existing file was edited.

## Files and hashes (all verified)

| File | sha256 |
|---|---|
| v1.3 `ckappa_oracle_scope_record_v1_3_E36.md` | `f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5`. Stable on disk; matches the posted hash. |
| Build script `…_v1_3_E36_build.py` | `77d6cc4982295cb885ab3ee199e5eef161ab6645a60ab85ef50c51308a9a7b80` |
| Astra #36 raw text | `c8342d5aa27c659dda5657e1e9ad70006a5e30759cc43eb25101d5546e756002` (read in full) |
| v1.1 | `e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c`, **unchanged** |
| v1.2 | `7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d`, **unchanged** |
| v1 | `1b450bcf231324c6fc3c686cc2daa819ed5f09cd5725c7c3283a1b3e2c39c5bf`, **unchanged** |

My Step 1 checklist was extracted independently from the raw text:
- `scratch/ckappa_v13/e36_items.json`, `585ba62d…`, holds E36-1..14.
- `scratch/ckappa_v13/manifest_items.json`, `08d62d24…`, holds the 12 manifest items.

## Our error, recorded

**Correction of my delta check `ff7b434a…`, part (b).** There I decomposed L_μ = E_s + K and L_full = E_s + e. From that I read floor (a) as leaving "at most ≈50% of the κ-part squared error (≈71% RMS)". **That decomposition was not established, and the reading is withdrawn.**

Astra #36, verbatim: "The claimed decomposition into shared error E_s and separate kappa errors K and e has not been established. With separately fitted maps and nonlinear finite predictions, residual components can have cross terms." The exact identity is "L_mu - L_full = 2*<r_mu,d> - ||d||^2", and "the half-loss rule means halving the named comparator's total prediction error. It does not mean that at most 71% of a separately identified kappa-component RMS error remains."

The error originated with me. CNA carried it into v1.2 Q1, and v1.3 §2 records the withdrawal correctly.

## Verdict

**PASS WITH NOTES. Four MAJOR notes must be fixed additively before the seal.** Each is a one-paragraph fix.

The core is correct. All 14 E36 items and all 6 of Astra's unquoted notes are present byte-for-byte. The precedence rule is unambiguous. The supersession map covers almost every conflicting v1.1/v1.2 line. The manifest checklist mirrors Astra's 12 items exactly.

The MAJOR notes, N1–N4 below, close gaps where execution would otherwise require improvisation. Astra L115, verbatim: "Do not improvise a tolerance after seeing a value."

## (a) E36 items: verbatim check and integration

The verbatim check was run independently against the raw text. For every n, `> "<text>"` is a substring of the raw file and of v1.3, in the block format `**E36-n.**\n\n> "…"\n`. All 14 are **True**. All six Astra notes that follow edits (after E36-4, 5, 7, 8, 11 and 13) are present verbatim, and no other notes exist in the raw text. The build script's own assertions (L23, L101–L102) say the same, but I did not rely on them.

| Item | Status | Integration with v1.1/v1.2 |
|---|---|---|
| E36-1 | RESOLVED | §0 L6 and §5 L144. §6 is non-executable. |
| E36-2 | RESOLVED | §2 rows 1–2 replace v1.1 L44 and withdraw the O5 "≈ H·sin²θ" reading (v1.1 L111). |
| E36-3 | RESOLVED | §2 row 3 removes the rank constraints (v1.1 L84, v1.2 D-4). §3 L110 freezes the solver. See **N3** on rcond versus the rank bands. |
| E36-4 | RESOLVED, **NEW-ISSUE N1** | §2 row 4 replaces v1.1 §5's "≥75% of O6 edits valid" with the per-fold count-and-mass rule. The §5 label for a coverage failure is undefined (N1). |
| E36-5 | RESOLVED | §2 row 5 replaces v1.1 L92 and L141. |
| E36-6 | PARTIAL (**N4**) | §2 row 6 and §3 L111 give the basis, normalization (raw), min-norm and the per-prefix validity check. Undefined: whether NOT ADMISSIBLE applies per prefix or to the whole fixture. Also "about its own baseline chart" is not restated for O7's Pred definitions; §0 precedence makes §1 govern. |
| E36-7 | PARTIAL (**N4**) | §2 row 6 says rank ≤ 2 and gives the integrity diagnosis. It does not say whether a resolved third direction *stops* the run. Astra's note: "A demonstrated implementation contradiction should still stop it." |
| E36-8 | RESOLVED, **NEW-ISSUE N1** | §2 row 7 extends the rank bands to equality cases and adds σ₁. §3 L108 declares the BOUNDARY band and L109 the zero-response rule. N1 covers applying the band to exact counts. |
| E36-9 | RESOLVED, with one map gap (n1) | §2 rows 8–9 replace v1.2 D-1 and withdraw the 71% reading. v1.1 L138's label "(this is the κ-component accuracy floor, S-M4)" is not listed. §1 governs it, but list it. |
| E36-10 | RESOLVED | §2 row 10. The 10⁻¹² band is kept only as a marker. |
| E36-11 | RESOLVED, prospective gap (n2) | §2 row 11 replaces v1.2 D-3(ii) "in full". That also removes v1.2's *seed-level* cell→seed status rules, and E36-11 defines only package-level labels from seed counts. That is acceptable for the oracle freeze (E36-1: the inference spec must settle "complete … outcome-accounting rules"), but record it as owed. The v1.1 L142–L147 quota labels should also be listed as superseded. |
| E36-12 | RESOLVED | §2 row 12 replaces v1.1 L130's "linear-regime references". |
| E36-13 | RESOLVED, minor (n3) | §2 row 13: O1→O2→1,000 O6, retained, PROJECTION HALT distinct from CAP REACHED. "Overhead estimated separately" names no method (n3). |
| E36-14 | RESOLVED, minor (n4) | §2 row 14. The mechanism for starting the clock before interpreter imports is not stated (n4). |

**Old text still contradicting E36.** Each case below is covered by §0 precedence, but the supersession map should be explicit:
- the v1.1 L138 κ-component label (n1);
- the v1.1 L143–L147 package labels (n2).

I found no surviving 71% reading, old step-0 order, ε-nonlinearity claim or O7 "PIPELINE INVALID on rank ≠ 2" in a governing position.

## (b) MANIFEST CONTENTS checklist against Astra L147–L160

The checklist has **12 of 12** items, verbatim, in order. Nothing is missing and nothing is extra. Notes on the "Source" lines:

| # | Status | Note |
|---|---|---|
| 1 | Add | Also hash v1 and the build script `77d6cc49…`, since §1 was generated by it. |
| 2 | Specify | Name "certificate" concretely: PR #4 `twostream_results_v1/RESULTS.md` plus results.json `certificate`, `freeze_commit` and `freeze_file_sha256` @ `5d9d8a7`. |
| 3 | OK | |
| 4 | OK | |
| 5 | OK | Plus N4's O7 granularity. |
| 6 | OK, add | NumPy `Generator` streams are not guaranteed stable across NumPy versions. Pin the version (item 10) and write the drawn Q, Q₂ and direction arrays, or their hashes, to the outputs. Define "seed_id" in "36000+seed_id": PR #7 seed 100–109, or index 0–9. That is prospective, §6 only. |
| 7 | Add | The §5 outcome vocabulary and precedence (N1), and output field naming `eps_syn` versus `eps` (Astra L7: "Keep that distinction throughout the manifest, output fields and report."). |
| 8 | Fix | Add the O7 resolved-third-direction rule (N4) and the §5 coverage-failure label (N1). |
| 9 | Add | A declared overhead reserve (n3), and the wrapper mechanism for the hard cap (n4). |
| 10 | Fix | "`RLIMIT_AS` = 4 GiB" is 4.29 GB. The cap is "4 GB address space" (Astra #35 L192). Use 4×10⁹ bytes, or record that GiB is the declared interpretation (n5). |
| 11 | Specify | The output paths, outside the repo or on a named branch, and that writes are incremental so a kill keeps completed outputs. |
| 12 | **Conflict (N2)** | "Filed by the Specialist after sealing; references the manifest sha" contradicts Astra's list, which puts the application *in* the immutable manifest. |

## (c) Unchanged

v1, v1.1 and v1.2 are byte-identical to their recorded hashes. ✔

## (d) Declared values (§3), checked against Astra #36

| Value | Required by Astra? | Assessment |
|---|---|---|
| BOUNDARY band \|x − t\| ≤ 10⁻⁶·t, distinct from NOT MET, not a pass | Yes. L115: "Use a declared numerical boundary band for S5 comparisons" | Sound and declared in advance. It is generous relative to float64 error, which is conservative. **But** see N1: applied to *exact count* coverage, an exact 75% hit (for example 96/128) would read BOUNDARY rather than ≥75%. |
| Zero response: S = 0 makes ratios UNDEFINED; oracle reads ZERO RESPONSE; neural counts as h with its reason | Yes. E36-8 and L71: "a low-sensitivity outcome, not a pass…" | Consistent with E36-11's note ("An absolute low-response outcome can be included within h, with its reason retained separately"). It counts in h, not u, which matches that note. Near-zero but nonzero S is left to the absolute response floor that E36-1 requires; fine for the oracle package. |
| `lstsq(rcond=None)`, min-norm on the √w system; B_μ on a 2-column design | Yes. E36-3: "minimum-norm solution convention and numerical solver are frozen" | Sound, with one interaction (**N3**). rcond=None truncates below ≈ machine-ε·max(M,N)·σ_max, roughly 10⁻¹³ relative. The rank rule calls σᵢ/σ₁ < 10⁻¹⁰ "resolved zero". Directions between 10⁻¹³ and 10⁻¹⁰ would be called zero yet still be inverted by the solver, which amplifies noise. **Fix:** set `rcond=1e-10`, or say that the rank rule is applied to the stacked design before fitting and that cells with σ ratios in [10⁻¹⁰, 10⁻⁶] are UNRESOLVED and not scored. For O7, min-norm does not create rank: the forecast Jacobian with respect to z is L·[I₂; Dg]·(scaled Q₂ᵀ), which has rank ≤ 2 structurally whatever the solver. |
| O7 raw monomial quadratic {1, μx, μy, μx², μxμy, μy²} | Yes. E36-6: "Specify the polynomial basis, coefficient normalization and minimum-norm fitting convention" | Acceptable. Raw monomials *are* a declared normalization. If the 16-point design has full rank 6, min-norm and scaling do not affect the solution. The 16 points form 4 flip orbits with 4 distinct (μx², μy²) pairs, so full rank is plausible, but it is **UNVERIFIED** without computation. Conditioning should be modest, since \|μ\| < 1 and the odd and even columns are orthogonal on symmetric data. Report the design's singular values under the rank rule. |
| PCG64; one `standard_normal` draw, row-major; reduced QR with diag(R) > 0; row-normalized directions; +v then −v | Yes. L154: "Seeds alone are insufficient" | Sound and complete, apart from the version pinning in item 6. diag(R) = 0 has probability zero. |
| One process; OMP/MKL/OPENBLAS = 1; pinned affinity; RLIMIT_AS 4 GiB | Yes. L158 | Sound, but the environment variables, affinity (taskset) and rlimit (prlimit) must be set by the **wrapper before interpreter start**, consistent with E36-14 (n4). GiB versus GB is n5. |

None of these values depends on outcomes. All are declared before any computation. ✔

## Notes

**MAJOR: fix additively before the seal.**
- **N1. The §5 outcome vocabulary and precedence are incomplete.** The oracle reference can now end in any of these:
  - met;
  - HEADROOM NOT MET;
  - BOUNDARY (§3);
  - ZERO RESPONSE (§3);
  - a coverage failure below 75% by count or mass in some fold (E36-4: "The oracle reference requires at least 75% coverage…"), which has **no label**.

  There is no precedence when statistics disagree, for example √H\* at BOUNDARY while R\* clearly fails. **Fix:** declare a coverage-failure label (for example "REFERENCE COVERAGE NOT MET", not a mechanism statement) and a precedence. Suggested order:
  1. PIPELINE INVALID;
  2. coverage not met;
  3. ZERO RESPONSE;
  4. any clear failure, giving HEADROOM NOT MET;
  5. any BOUNDARY, giving BOUNDARY;
  6. otherwise met.

  Also state that the BOUNDARY band applies only to float statistics (√H\*, R\*, law-mass coverage). Exact count coverage uses exact ≥.
- **N2. The application timing conflicts with Astra's manifest list.** Astra L160 includes "The Research Lead's application of the standing approval to this exact oracle-only scope" *in* the freeze manifest. E36-14 makes the manifest immutable. Checklist item 12 has the application filed *after* sealing and referencing the manifest sha, which is circular. **Fix:** the application cites the hashes of the scope files (v1.1, v1.2, v1.3), the code and the inputs. It is filed before the seal. Its sha256 goes into the manifest, which is then sealed. Execution may begin only after both exist.
- **N3. rcond versus the rank bands.** Set `rcond=1e-10`, or freeze the "rank rule on the design before the fit; unresolved cells are not scored" convention, so that a direction the rank rule declares zero is never inverted.
- **N4. O7 stop and admissibility granularity.**
  - **(i)** Declare that a *resolved* third singular direction (σ₃/σ₁ > 10⁻⁶) is a demonstrated implementation contradiction, so STOP, PIPELINE INVALID, an integrity diagnosis and no rerun. E36-7 ("contradicts the fixture's structural construction") and Astra's note ("A demonstrated implementation contradiction should still stop it") support this. An unresolved band reads unresolved.
  - **(ii)** Declare whether an invalid quadratic baseline at *some* prefixes makes the whole fixture RESTRICTED COMPARATOR NOT ADMISSIBLE, or only those prefixes, with the rest evaluated and coverage reported. Either is acceptable if declared. Without refitting or replacement (E36-6).
  - **(iii)** Restate that O7's Pred_full and Pred_μ are taken about its own baseline chart (μx, μy, g(μx, μy)) (E36-6).

**MINOR: fix at seal.**
- **n1.** Add v1.1 L138's "κ-component accuracy floor" label to the §2 map as withdrawn (E36-9).
- **n2.** Add v1.1 L142–L147 to the §2 map. Record that the seed-level cell→seed status rules are owed by the inference spec (E36-1, E36-10, E36-11).
- **n3.** E36-13 overhead: freeze "omit" plus a fixed reserve for serialization and report writing (for example 60 s subtracted from the remaining cap), or freeze another explicit estimate.
- **n4.** E36-14 clock: name the external wrapper. For example, a shell wrapper records the start time and sets the environment, taskset and prlimit, then runs `timeout` with the remaining-cap kill. Outputs are written incrementally so a kill keeps them.
- **n5.** 4 GiB versus 4 GB (item 10 above).
- **n6.** Manifest items 1, 2, 6 and 11: the source refinements above.

## Wording and scope

- The claim ceiling is oracle-only (§5, Astra L164).
- There is no neural, acquisition, S12, S15, C4 or consciousness statement.
- No checkpoint is opened.
- Nothing runs before the seal and the application.
- Astra L162, verbatim: "No pre-freeze dry run is authorized."
