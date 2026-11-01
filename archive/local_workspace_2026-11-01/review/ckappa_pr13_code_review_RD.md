# Adversarial code review: PR #13, C-κ oracle package phase 1

Research Delegate, 2026-10-22 (ET). This is a new file. The review is read-only. No package code, stage, fixture or timing sample was run, and no checkpoint was loaded. The only checks were static: an `ast` parse of `ckappa_oracle/*.py`, `bash -n run_package.sh`, and sha256 checks. The PR was fetched into a scratch clone at `/workspace/scratch/pr13` (`git fetch origin pull/13/head`). `/workspace/repo` was not modified. Nothing was posted to GitHub.

- **PR:** https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/13
- **Branch and commit:** `cursor/ckappa-oracle-package-v1` at `e99f0d3979575c012b6c775f9d744eccb5f85984`
- **Governing set:** RL `6a5e0f24…` + RL ruling `6d75918f…`. Below those: closure `4ad1d217` > v1.4_N `3f0c5c12` > v1.3 `f6263fb8` > v1.2 `7e15e812` > v1.1 `e40c288f`. Astra's verbatim E36 text governs over all of these (RL L8, v1.4_N L8, closure L35).

## Overall verdict: **READY WITH NAMED FIXES**

- **1 BLOCKER and 5 MAJOR.** Every one is a small, named edit.
- **Oracle mathematics:** I found no contradiction of E36, B1, B2 or B3 in the code. That covers the chart, filter, folds, fits, masks, pooling, N1 order, the rank band, the O7 void ceiling and the σ stop.
- **The blocker is in the draft manifest.** Its precedence rule ranks E36 below the RL and closure records.
- **Q1–Q11:** 6 ACCEPT and 5 REPLACE. The REPLACE items are Q6, Q7, Q8 and Q10, plus Q3, which is accepted in substance and reworded.

## 1. Bundle and hashes (task 1)

- **`review/ckappa/SHA256SUMS`:** `sha256sum -c` gives OK on all 20 entries.
  - All 18 scope and check files are byte-identical (`cmp`) to `/workspace/review/<name>`.
  - Both Astra files are byte-identical to `/workspace/astra_consult3{5,6}_response.txt`.
  - Governing hashes as listed: `6a5e0f24…c15c63`, `6d75918f…563edd`, `4ad1d217…c45c9c`, `3f0c5c12…6ff359`, `f6263fb8…04e5`, `7e15e812…7d`, `e40c288f…0c`. E36 file: `c8342d5a…6002`.
- **`manifest_DRAFT.json`:** sha256 `b96a74e7fe2a8799b7f0e6e59b143ace966f909126ad4f3ddf78d594822873e5`.
  - `sealed: false`.
  - Application `{status: PLACEHOLDER_NOT_FILED, path: null, sha256: "PLACEHOLDER"}`.
  - Matches the Specialist's report.
- **`IMPLEMENTATION_QUESTIONS.md`:** sha256 `f67ba25d2022d3ad198a2f71a9771b6eee5d5dae5e53c21a05aae50af89d2c36`. Matches.
- **Implementation files:** all 16 `ckappa_oracle/*.py` files and `run_package.sh` hash to the values in manifest item 2.
- **Inputs:** checked statically with `git show 5d9d8a7:<path> | sha256sum`.
  - `results.json`: `bf2de92c…`
  - `RESULTS.md`: `8477e98c…`
  - protocol: `6ff31a0d…`
  - `certificate` = "two-stream world-admission analytic certificate v1"
  - `freeze_commit` = `c69deb44…`
  - `freeze_file_sha256` = `c654a121…`
  - `history_count` = 256
  - `bits` order is reading 1 first, which matches `inputs.py:76`.
  - Terminal forecasts come from the stage-8 posterior with no final transition (protocol L105–108), which matches `world.py`.

## 2. Q1–Q11 verdicts

| Q | Verdict | One-line wording (if REPLACE) and reason |
|---|---|---|
| Q1 float count | **ACCEPT** | I recomputed 1536 + 256 + 294,912 + 256 + 294,912 + 196,608 = **788,480**, and n_O1 = 16 + 256 = **272**. Both are under v1.2 D-6's ≈1×10⁶ and follow its pieces: O6/O7 ≈ 5.9×10⁵ matches 589,824 exactly. The projection also follows D-2 and E36-13 ("frozen scheduled upper counts with completed work subtracted"). Caps: one process, a few-kB working set, and ~0.8 M small 4×4 propagations, which should fit easily within 1 CPU / 4e9 B / 10 min. That is my estimate and is UNVERIFIED until step 0, as the scope intends. Condition: the overrun stop (`runstate.py:79–87`) is outside N1's PIPELINE INVALID list. It must be named by ruling; see M3. |
| Q2 O7 seed | **ACCEPT** | v1.1 O7 scores "the O6-protocol gain over B_μ", so the edits are shared. The `O7_directions` record (`draws.py:100–113`) carries seed 35016, shape, `<f8`, the raw-byte sha and `shared_with: O6_directions`, which satisfies closure §4 / N-b. I agree with CNA. |
| Q3 chart moments | **REPLACE (wording only; substance accepted)** | "P = P(a) = Σ_u P(h). The chart mean is P(a)-weighted. Each SD uses the population divisor Σw. D = diag(SD). g is fit with the same P(a) weights. O7 uses z = Q₂·D_μ⁻¹((μ_x, μ_y) − μ̄), centered with the same P(a)-weighted mean and the same μ block of D as O6." This agrees with CNA. The code already centers (`stages.py:887`), but Q3's text omits it. Centering does not change any O7 edit or derivative, because Q₂ᵀQ₂ = I and `mu_new = μ + D_μQ₂ᵀδ`. The construction must still be stated as matching O6's (v1.1 L83 vs L95). |
| Q4 O7 σ stack | **ACCEPT** | B3 says "stacked Jacobian over the non-voided prefixes per fold", and the per-fold stacked Jacobian is the fit-side stack. Each prefix is a fit prefix in 3 folds, so all non-voided prefixes are covered. The code matches B3 as ruled. The σ check runs **before** the admissibility branch, so it applies with 0, 1–4 or ≥5 voids (`stages.py:757–790`). σ₃/σ₁ > 1e-6 leads to an integrity diagnosis, STOP and PIPELINE INVALID. A ratio in the band is UNRESOLVED and the run continues. σ₁ = 0 means no ratios and no stop. See also N7. |
| Q5 g rank-unresolved | **ACCEPT** | N3 applies the rank rule to "every fit (… O7 …)". E36-7 says "Numerical ambiguity is reported as unresolved", and E36-6/E36-7 say O7 stops only on a demonstrated contradiction. With no g, there is no void test and no σ stack. Continuing to O3 is correct. Use one label string: see N6. |
| Q6 O5 mask | **REPLACE** | "O5 uses the O4 perturbations and the O4 validity rule (all four p ≥ 1e-6) on both inverse_chart(θ_a+Δ) and its κ-zeroed counterpart, checked before Φ. One common mask applies to the numerator and denominator of R_G. Masked, ValueError and non-finite cases are excluded from both means and reported by count and law mass per size and group. O5 stays descriptive." This is CNA's wording plus "checked before Φ" and the per-size reporting. Reason: v1.1 L108 (O4 validity, "never replaced"), Astra L12 ("Invalid edits cannot silently disappear from coverage accounting"), and E36-5's identical-mask principle. The current code (`stages.py:1066–1098`) averages forecasts of non-probability charts into H_G and drops only ValueError and non-finite cases. Masked O5 edits need not be propagated: O5 is outside the step-0 sample, and 196,608 stays an upper bound. |
| Q7 coverage with unresolved fold | **REPLACE (logic accepted + one addition)** | "Coverage is tested on the resolved O6 folds, and a coverage failure there takes precedence (N1 step 2) over REFERENCE RANK UNRESOLVED (step 3). Each rank-unresolved fold still gets a coverage row marked `not_propagated: rank UNRESOLVED` with its scheduled n_total = 4096 per ε_syn and no fraction." This is the only reading under which B1 (closure §2) is reachable: counting an unpropagated fold as 0/4096 would always fire step 2 first. E36-4 requires coverage "for every fold", and today the unresolved fold does not appear in the coverage table at all (`stages.py:591`). |
| Q8 all O6 folds unresolved | **REPLACE** | "If no O6 fold is resolved, results.json `section5` keeps the N1 labels from O6 (REFERENCE RANK UNRESOLVED, or REFERENCE COVERAGE NOT MET if applicable). The package then stops with stop kind STEP 0 SAMPLE SHORT, exit 6, which is distinct from PROJECTION HALT, CAP RESERVE REACHED and CAP REACHED. O7 and O3–O5 are not run." The stop is right: E36-13 requires the projection before further work, and no improvisation is allowed. But `driver.py:71–84` replaces the determinate §5 outcome with the stop-kind label. The label survives only under `stages.O6.section5_from_o6`. See N3. |
| Q9 t_sample | **ACCEPT** | v1.4_N n3 L54 says "Non-propagation overhead after step 0 is omitted from T_rem", and E36-13 calls the projection a heuristic that "omits or separately estimates non-propagation overhead". Summing `perf_counter` around the 1,000 Φ calls (`runstate.py:103–108`) is therefore the literal reading. T_rem excludes O2 and the baseline already done (`runstate.py:125–126`). The halt is T_rem > 540 − T_elapsed (`runstate.py:130`), which matches n3 L56. See N8 for the expected understatement. |
| Q10 guard-failing edits | **REPLACE** | "Every edit in the nest is propagated. The guard is evaluated on the three beliefs first. For a guard-failing edit, a ValueError or non-finite Φ is caught and counted by kind, never stops the package, and is stored as null in any retained record. The edit stays in the coverage denominator and is excluded from the losses and the 1e-9 identity. A ValueError or non-finite Φ on a scoreable edit is an O6 fixture failure (PIPELINE INVALID), or for O7 an integrity diagnosis." Reason: with p < 1e-6 (possibly negative), `observe_float` can raise or return non-finite values, and the O6/O7 loops do not catch this (`stages.py:519–536`, `908–925`). The result would be EXECUTION ERROR. A non-finite q in `retained_o6_sample` (`runstate.py:95`) also makes `json_ready` raise inside `_write_outputs`, including in the exception handler (`driver.py:124–127`). Then neither results.json nor stop_kind.json is written. See M2. |
| Q11 nest order | **ACCEPT** | `stages.py:495–536` and `884–925` match the listed nest. That includes v1.1's fold order (`geometry.py:15–22`), eps_syn order, actual → Pred_full → Pred_μ, and the cached baseline call on first use. Fits are frozen and hashed before any edit is scored (`stages.py:486`, `838`), as in v1.2 D-4. Row order does not change the minimum-norm solution. |

## 3. Findings

### BLOCKER

- **K1. The manifest's precedence rule demotes E36.**
  - **Where:** `manifest_DRAFT.json:46` ("Records ranked 1–4 are the adopted amendments to that text"), `:61` ("A higher rank wins"), `:65` ("Rank 5's E36 verbatim text governs inside v1.3 and over ranks 6 and 7"). The same ordering appears in `IMPLEMENTATION_QUESTIONS.md:5–13`.
  - **Conflict:** under this rule, ranks 1–4 (both RL records, the closure note and v1.4_N) override E36. The governing set says the opposite:
    - RL L8: "E36 verbatim text governs over all of these"
    - v1.4_N L8: "governs over everything, including this file"
    - closure L35
  - **Why it blocks:** Astra L149 requires "an unambiguous precedence rule", and the manifest is immutable after the seal (E36-14).
  - **Fix (one line in item 1 and top-level):** "E36-1..14 verbatim (v1.3 §1, from `c8342d5a…`) governs over every record below. Then: RL ruling `6d75918f` > RL `6a5e0f24` > closure `4ad1d217` > v1.4_N `3f0c5c12` > v1.3 §2–§3 > v1.2 > v1.1. Any conflict with E36 is resolved additively before execution."

### MAJOR

- **M1. The run does not check that it is executing the sealed code.**
  - **Where:** `preflight.py:76–99` checks only `sealed`, the format of the application sha and `frozen_runtime`. It does not re-hash the implementation files, `run_package.sh` or the `review/ckappa/` bundle against `manifest.json`. It does not check that the application file exists at its recorded path with that sha. The post-run index (`run_package.sh:50–97`) hashes outputs only.
  - **Effect:** nothing ties the executed bytes to the sealed manifest, against E36-14 and N2's cite-by-hash chain.
  - **Fix:** in preflight, verify the sha256 of every `implementation_files` entry and the application file against `manifest.json`, and stop with PREFLIGHT FAILED on any mismatch. Also record the executed-file hashes in `post_run_index.json`.
- **M2. Guard-failing Φ is unhandled, and output writing is not fail-safe.**
  - **Where:** `stages.py:519–536` and `908–925` propagate guard-failing edits with no ValueError or non-finite handling. `runstate.py:95` stores raw q in the retained sample. `io.py:18–30` rejects non-finite values. `driver.py:124–127` can then fail a second time inside the handler.
  - **Effect:** a theoretical but unexcluded path gives an unclassified stop with no results.json or stop_kind.json. That violates E36-14's "Preserve completed outputs on stopping", although the stage files are kept.
  - **Fix:** apply Q10 as worded above, and make `_write_outputs` fall back to a minimal results.json and stop_kind.json if serialization fails.
- **M3. The stop vocabulary goes beyond N1 and manifest item 8.**
  - **Where:** PIPELINE INVALID is raised for several things that are not O1/O2/O6 fixtures or N4(i):
    - input hash or certificate mismatch and `git show` failure (`inputs.py:31–83`)
    - schedule overrun (`runstate.py:79–87`)
    - QR or direction degeneracy (`draws.py:45–59`)
    - zero chart SD (`stages.py:266–267`)
    - coverage mass total 0 (`stages.py:407–408`)
    - O6 edit-count mismatch (`stages.py:580–589`)
    - O2 propagation count (`stages.py:318–319`)
    - an empty reduced O7 design (`stages.py:819–820`)
  - **Gap:** none of these is listed in manifest item 8 (`manifest_DRAFT.json:~296`). Astra L156 requires the manifest to say which outcomes stop execution.
  - **O7 case:** the O7 stop contradicts E36-6 and the E36-7 note ("should not stop … merely because …"). It is unreachable with ≤4 voids, because each fold keeps at least 4 of its 8 fit prefixes. Even so, it should read RESTRICTED COMPARATOR NOT ADMISSIBLE for that fold, not PIPELINE INVALID.
  - **Fix:** one RL line classifying the pre-O1 input and draw checks and the count checks as integrity failures (PIPELINE INVALID, O1-class), listed by name in item 8. Relabel the O7-empty case.
- **M4. The O5 mask (Q6) is a code change before the seal.**
  - **Where:** `stages.py:1046–1123` (`probability_guard_applied: false` at `:1122`).
  - **Fix:** implement Q6 as worded above, then re-hash.
- **M5. The application citation list predates the governing set.**
  - **Where:** `manifest_DRAFT.json:381` copies N2's list: v1.1, v1.2, v1.3, v1.4_N, the build script, the implementation files and the inputs.
  - **Missing:** closure `4ad1d217`, RL `6a5e0f24`, RL ruling `6d75918f`, the E36 file `c8342d5a`, `IMPLEMENTATION_QUESTIONS.md`, and the forthcoming Q1–Q11 RL ruling record.
  - **Fix:** the Specialist's application should cite the full governing set by sha. The manifest text should list it.

### NOTE

- **N1. Python and NumPy pins.** The pins are Python 3.12.3 and NumPy 1.26.4, asserted at `preflight.py:58–64`. This box has Python 3.13.5 and NumPy 2.5.4, so the run must use an environment that matches. A mismatch stops with PREFLIGHT FAILED, before any oracle work.
- **N2. The wrapper maps any SIGKILL (137) to CAP REACHED** (`run_package.sh:72–74`), including a kernel OOM kill. Record the wall time at exit in `post_run_index.json` so that a kill well before 595 s can be told apart. RLIMIT_AS overruns surface as MemoryError, which is reported as EXECUTION ERROR (exit 1), so they are already distinct.
- **N3. Package §5 after a non-PIPELINE-INVALID stop.**
  - `driver.py:71–84` replaces a complete O6 §5 result with the stop-kind label, for example CAP RESERVE REACHED at O5, or Q8.
  - Keep `section5` as the O6 N1 labels, marked "package incomplete; O7 integrity check not completed" when O7 did not finish. Carry the stop kind separately.
- **N4. `exact_reduction_to_cross_term`** (`stages.py:739`) tests float `== 0.0`. In float64, flip-symmetric data give c₀, c₁, c₂, c₃, c₅ around 1e-17, not exactly 0, so this will read False. Report max |c_i| / |c₄| for i ≠ 4, or rename the field "exact float zero", so it is not read as a symmetry finding (v1.1 L98: "reported, not assumed").
- **N5. A NOT ADMISSIBLE O7 payload says `derivatives_evaluated: False`** (`stages.py:799`). B3's σ stack does evaluate derivatives at the non-voided prefixes. Use "σ-stack derivatives only; no B fits or predictions".
- **N6. Label strings differ:** "G RANK UNRESOLVED" vs "g rank UNRESOLVED" (`stages.py:699–700`). Use one string.
- **N7. The σ stack is analytic.** It is computed as L(chart)·dθ/dz (`stages.py:750–771`), so rank ≤ 2 holds by construction and the N4(i) check mainly tests linear algebra, not the O7 readout path. This is consistent with B3 and E36-7 as written. It may be worth noting in the report that the check is structural.
- **N8. The projection omits the per-edit work outside Φ** (guard, `inverse_chart`, loss bookkeeping). That follows n3, but T_rem will understate the true remaining time by perhaps 1–2×. The 540 s soft stop and the 595 s kill remain the real bounds.
- **N9. The O6 baseline Φ calls go to the "O6" bucket** (`stages.py:501–506`), while the separate `true_baseline` bucket counts only O5 misses. The 1,000-call sample therefore includes 3 baseline calls. This is consistent with Q11's nest. Name it in the manifest.
- **N10. A resolved lower-rank O6 B design gets scored under B2,** then fails the frozen B = DQᵀ expectation (v1.1 L90) and gives PIPELINE INVALID as an O6 fixture failure. That is consistent. B_μ has no identity check and is scored normally. Say this in item 7.
- **N11. Manifest item 1 lists "the rank-2 record's addition"** (RL L11) as adopted (`manifest_DRAFT.json:65`). B3 states that it replaces L11. Reword to "RL L11 as replaced by B3".
- **N12. "consciousness" appears only in REPORT.md's claim-ceiling disclaimer** (`report.py:31`, a negation copied from v1.1 §8 and Astra L164). "autopoietic" and "alive" do not appear anywhere in the package, wrapper or manifest. Keep the disclaimer only if the house rule allows the negated term. Otherwise drop the word.
- **N13. `inputs.py` reads inputs with `git show 5d9d8a7:…`,** so the run directory must be a git checkout that contains that commit.

## 4. Checklist (task 3)

| Item | Status | Where |
|---|---|---|
| B2: only rank-UNRESOLVED is unscored; resolved lower rank and σ₁ = 0 are fit minimum-norm and scored, rank and σ₁ reported | OK | `linalg_fit.py:21–70`. σ₁ = 0 gives rank 0, no ratios, zero solution, scored. Band [1e-10, 1e-6] inclusive gives None. Otherwise invert σ > 1e-10·σ₁. The report carries σ, σ₁, ratios, rank and n_inverted. |
| B3: σ₃/σ₁ > 1e-6 at non-voided prefixes leads to integrity diagnosis, STOP, PIPELINE INVALID; otherwise descriptive | OK | `stages.py:639–674, 757–790`. Runs for any void count. `>` keeps an equality at 1e-6 in the band. |
| B1 and N1 order; band on floats only; 4·n_s ≥ 3·n_t | OK | `outcomes.py`: count test `:38`, clear/band `:17–22`, rank `:58`; coverage → rank → ZERO RESPONSE → HEADROOM NOT MET → BOUNDARY → MET/AVAILABLE. PIPELINE INVALID is step 1 via `driver.py:74–79`. Evaluated at ε_syn = 0.1 for ALL and MARG separately. |
| rcond 1e-10 from the same SVD | OK | `linalg_fit.py:16, 37, 63–67` (RL ruling item c). |
| O7: ≥5 of 16 gives NOT ADMISSIBLE; 1–4 voided labelled RESTRICTED COMPARATOR NOT ADMISSIBLE; g never refit; per-fold counts | OK | `stages.py:708–721, 806–837, 956–971`. |
| N4(iii): O7 derivatives and predictions about its own baseline chart; disagreement with the reachable oracle reported separately | OK | `stages.py:856–878, 885–902`. |
| ½ floor, E36-10 L_μ/S ≥ 0.02, E36-11 p/f/u/h | Correctly **absent** | §6 is prospective (E36-1). The code does no seed roll-up. Measured gain H − L_full is reported (E36-9). |
| E36-13 step-0 order O1 → O2 → first 1,000 O6, retained and not recomputed | OK | `driver.py:105–114`, `runstate.py:88–101`. Draws and inputs come before O1 and are not O6 work. |
| Projection halt T_rem > 540 − T_elapsed; 540 s soft stop; 595 s kill; 60 s reserve; distinct stop kinds | OK | `runstate.py:63–70, 118–145`; `run_package.sh:11–14`. Exit codes 3 / 4 / 137 (or 124), recorded distinctly. |
| Wrapper sets threads, affinity and 4e9 B before Python; T0 first | OK | `run_package.sh:3–14`. Rechecked in `__main__.py` and `preflight.py:25–55`. |
| Pinned versions asserted at startup | OK | `preflight.py:58–64` (see N1). |
| §6 seeds 36100–36109 | OK (prospective only, not drawn) | `pinned.py:57`. |
| Per-array raw-byte sha256, shape and `<f8` in results.json; hash file written at draw time; covers Q, Q₂, O4, O6 and O7 | OK | `draws.py:15–30, 65–113`; `driver.py:31`. The npz file hash is flagged as not a reproducibility check (`run_package.sh:95`). |
| Each stage writes its file on completion (atomic + fsync) | OK | `runstate.py:150–157`, `io.py:33–51`. |
| No retries | OK | There is no retry path anywhere. |
| ε_syn naming (E35-9) | OK | Fields use `eps_syn`. The neural field `eps` does not occur in the outputs. |
| Seal order (N2) | OK in the code and the item 12 sequence | `manifest_DRAFT.json:379–387`, `preflight.py:76–99`. The application does not reference the manifest. See K1, M1 and M5. |
| No checkpoint or neural inference | OK | No torch, pickle or weight loading anywhere. The only inputs are three git blobs at `5d9d8a7`. |
| Forbidden language | NOTE N12 | |

## 5. Next steps

1. The RL rules on Q1–Q11 (wording above) and on M3, additively.
2. The cloud agent applies K1, M1–M4 and the notes it chooses, re-hashes, and updates the manifest draft and the Q record.
3. I do a short delta check.
4. The Specialist files the application citing the full governing set (M5).
5. The application sha goes into the manifest, then the seal, then step 0.

Claim ceiling unchanged: oracle-only. Nothing executes before the application is filed and the manifest is sealed.
