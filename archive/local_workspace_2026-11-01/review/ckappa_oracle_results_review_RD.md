# Adversarial review: results of the sealed C-κ oracle package run (PR #13 @ 14376f38)

Research Delegate, 2026-10-22, ~3:45 AM ET. New file. Read-only. No rerun; no package code executed or imported. Scratch clone `/workspace/scratch/pr13`, branch `pr13run` = `14376f38fe09157eef85bfac1cc4a4433d49bebc`. `/workspace/repo` untouched; nothing posted to GitHub. Checks marked **YOURS** are my own small numpy/hashlib recomputations from committed output files only. The CNA spot-check (relayed by the parent) was verified independently against `stage_O7.json` / `fit_freeze_O7.json`, not adopted.

## Verdict: **CONFIRMED WITH NOTES**

Every reported figure that has a committed source is confirmed, with three wording corrections (σ₁ attribution, "observed" versions, wall/VmHWM provenance). All hashes verify. No stop or guard should have fired and did not. No contradiction with E36 or the RL records in the run outputs.

There are **no blockers** for the oracle result. There is **one MAJOR finding, about the prospective neural design (§6), not about this run**: O7's zero gain is a symmetry identity. The O6/§6 gain statistic (one global linear B per fold, fit on unions of flip orbits) cancels any κ-sensitivity whose sign alternates across the W2 flip orbits. So a neural NOT SHOWN under the current §6 design could not be read as "κ not used" (M-1). One MINOR: stale "unsealed" labels inside the sealed run (m-1).

Question separation: this run answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY. O6 is a feasibility precondition for a later neural test. M-1 constrains what that later test's negative outcome could mean. Nothing here is evidence for or against any of the four questions.

## 0. Integrity and run accounting

| Claim | Status | Evidence |
|---|---|---|
| manifest.json 4179b71a | ✓ | sha256 `4179b71a…6831`. Sealed copy equals `manifest_DRAFT.json` except `sealed: true` (sorted JSON diff, one line). Seal commit 804df04 at 03:21:48 ET; t0 = 1792653725.91 = 03:22:05 ET; outputs commit at 03:25:19 ET. |
| application 4df62ccd FILED | ✓ | `review/ckappa/CKAPPA_STANDING_APPROVAL_APPLICATION_RL.md` and `/workspace/review/…` both `4df62ccd…5042`. Both manifest path fields identical. Citations include ADDENDUM_RL1, my delta check (7a890376) and the Astra raw file (c8342d5a; `/workspace/astra_consult36_response.txt` matches). |
| Code bytes = sealed manifest | ✓ (YOURS) | All 17 `items.2.implementation_files` re-hash equal at HEAD. The file set equals `ckappa_oracle/*.py` + `run_package.sh`. No code change since 697200e8 (`git diff --stat 697200e8..HEAD -- ckappa_oracle run_package.sh` empty). Inputs at 5d9d8a7 re-hash equal via `git show`. |
| 5d9d8a7 present | ✓ | Commit object present and an ancestor of HEAD. Runtime `git show` of the three inputs must have succeeded, otherwise INTEGRITY STOP exit 7. |
| Python 3.12.3 / NumPy 1.26.4 "observed" | ✓ by gate; wording | `check_versions` (`preflight.py:60–66`) compares the actual versions and fails otherwise. But `results.json` `versions` is the pinned constant (`driver.py:45`), not a recorded observation. Say "asserted at preflight". |
| 21.8 s wall | ≈ | Package elapsed `t_elapsed_s` 21.729 (results), last log line 21.75 s (`run.log:11`), both from the wrapper T0. The wrapper's own end time is not recorded in `post_run_index.json`. |
| VmHWM 41 MB | **UNVERIFIED** | Appears in no committed file. |
| 784,960 float + 272 exact | ✓ (YOURS) | `results.json:72`. Buckets sum exactly: O2 1536 + O6 295168 + O7 294912 + O7_baseline 256 + O5 193088. Against the schedule, 788480 − 784960 = 3520 = 2 × 1760: both O5 charts are skipped for each invalid s=0.5 occurrence. The 256 true baselines are charged to the `O6` bucket (`true_baseline: 0`), a labeling nit. Bound respected; no overrun stop due. |
| post_run_index 7825c536; results.json 6adb5de2 | ✓ | All 15 output hashes in the index match the files. `drawn_arrays.npz`: each array's raw-byte sha256, shape and dtype matches `results.json` (YOURS). |
| Scope bundle | ✓ | `review/ckappa/SHA256SUMS` verifies (20 entries). |

## (1) `phase: "unsealed-implementation"` on a sealed run

**Stale hard-coded constant, not a draft-manifest load. Severity MINOR.**

- **Source of the label.** It is a literal in `driver.py:39` (`_results_body`), also at `driver.py:78/95/119`, `__main__.py:19`, `run_package.sh:83`, and `__init__.py:6` (`__version__ = "phase1-unsealed"`). Nothing reads it from a manifest.
- **Which manifest was loaded.** `load_manifest` opens only `root/"manifest.json"` (`preflight.py:79–80`) and fails unless `sealed is True` (`:90–91`). The draft has `sealed: false`, so loading it would have been exit 5. The log line "preflight passed; sealed manifest loaded" (`run.log:1`) is written only after `preflight()` returns. The wrapper recorded `manifest_path: manifest.json`, sha `4179b71a`, `manifest_sealed_file_present: true`.
- **M1.** `check_sealed_hashes` (`preflight.py:127–180`, called at `:191` before any draw) re-hashed the 17 code files, the inputs and the application at `standing_approval_application.path`. Any mismatch would have been exit 7. The run completed (exit 0), so the application matched 4df62ccd and the executed bytes matched the sealed list at run time. This is self-attesting (the check lives in the checked code), and my YOURS re-hash of the committed bytes agrees.
- **More stale labels in the sealed manifest itself.** `manifest.json:2` `"document": "…manifest DRAFT"`, `:4` `"seal_status": "UNSEALED"`, and `:11` draft_note ("application sha256 remains PLACEHOLDER… This draft is not sealed"). These contradict `sealed: true` and the filed application in the same file. No gate reads them: preflight keys only on `sealed`, the application sha/status and `frozen_runtime`.
- **Severity: MINOR.** No computation, gate or label depends on these fields. Audit readability suffers, though. E36-14 makes the manifest immutable, so do not edit it. Record an additive erratum stating that `phase`, `__version__`, `document`, `seal_status` and `draft_note` are stale implementation labels, and that the sealed state is established by `sealed: true`, sha 4179b71a in the post-run index, and the M1 pass.

## (2) No p/f/u/h roll-up

**Correct.**

- E36-11 (`astra_consult36_response.txt:127`) defines "disjoint **seed** counts p, f, u and h" with POSITIVE at p ≥ 8, i.e. the 8/10 neural seed quota (E36 Q3, L57).
- The oracle has no seeds. It is one deterministic W2 oracle with folds over prefixes, and E36 Q3 says folds "are not independent replications".
- E36-1 (L79): §6 "does not constitute an executable inference protocol". The §6 seeds 36100–36109 remain prospective.
- So the absence of a roll-up is required, not an omission. The oracle reports N1 §5 labels per group at ε_syn = 0.1, which is what it did.

## (3) What O6 MET / AVAILABLE licenses

**Confirmed values and inequalities.**

- **Figures.** ALL: √H 1.5406e-3 vs 1e-3, R 0.07988 vs 0.05, S 2.9714e-5, L_full 1.93e-33, measured_gain = H. MARG: √H 8.017e-4 vs 1e-4, R 0.07865 vs 0.02. Coverage 4096/4096 and law-mass 1.0 in all 6 folds at all four ε_syn. `law_mass_in_boundary_band: []`. Pred_full max error 4.44e-16 ≤ 1e-9, and B max error ≤ 4.2e-16 in every fold.
- **YOURS arithmetic.** √(2.3735e-6) = 1.5406e-3, R = H/S, and denominator 96 = 3 × total history mass (1) × 32 edits, which matches E36-5.
- **Inequalities.** `outcomes.py`: a value is HEADROOM NOT MET only if < thr·(1−1e-6), BOUNDARY if |v−thr| ≤ 1e-6·thr, and MET/AVAILABLE otherwise. This is ≥ with the declared boundary band (E36-8). The coverage count test is the integer `4·n_s < 3·n_t`, checked before rank and headroom per N1. Applied correctly; no value is near a band.

**What is licensed.**

- Under the frozen synthetic embedding (Q seed 35006, the 8-D z with κ as one fixed linear direction, O6 directions seed 35016, ε_syn = 0.1, fixed-κ comparator), W2 at stage k = 4 has enough κ-attributable forecast response for the oracle thresholds.
- Per N1 that means ALL may proceed to an inference specification, which still needs its own freeze and review (E36-1), and MARG is usable rather than descriptive-only.
- It says **nothing about the GRU** (E36-9; Astra Q1 L11: "Oracle H* does not certify neural feasibility"). Astra Q2 L28: the thresholds "are not intrinsic thresholds of W2, neural sensitivity guarantees, or evidence that a later study will pass".
- L_full ≈ 0 is by construction (θ is linear in z, so B recovers the map exactly). "MET" is therefore ideal headroom (E36-9), not a demonstration of recoverability.

**Limits.**

- **ALL vs MARG.** The κ-attributable share is about the same: R_MARG 0.0787 vs R_ALL 0.0799 (CNA's "about the same" ✓). The margins differ because MARG's thresholds are lower. ALL: √H at 1.54× and R at 1.6× threshold; **ALL √H is the tightest margin in the run**. MARG: √H 8.0× and R 3.9×.
- **CNA's "~92%".** 1 − R = 0.920 (ALL), 0.921 (MARG) ✓ as 1 − L_μ/S. Better wording: "the fixed-κ comparator leaves 8% of the response energy as error". "Absorbs 92%" implies an orthogonal decomposition, which held-out L_μ/S does not guarantee (E36 Q3 cross-term identity, L48).
- **S = 2.97e-5.** The weighted mean squared forecast response at ε_syn = 0.1, so RMS response ≈ 5.45e-3 forecast-probability units summed over the ALL components, under this embedding. It is a scale reference, not an absolute response floor. Astra Q4 L69 forbids borrowing oracle quantities "as though it already supplied that neural floor". E36-1 and E36-10 still require an absolute floor before inference.
- **E36-10 (L_μ/S ≥ 0.02).** The oracle analogue R = 0.080 / 0.079 is about 4× that convention. That is a property of the synthetic κ direction only. For a checkpoint, L_μ/S is computed on the network's own responses and cannot be carried over from O6. Astra Q4 L67: the numerical match to R*_MARG "supplies no theorem".

## (4) O7 under E36-6/7 and E35-2

**Framing correction (CNA is right; I adopt it after checking).**

- Calling g(μ) "the lookup rival" is wrong.
  - v1.1 L102: O7 "is *one* explicit smooth two-coordinate system. It is not the reachable-set lookup… It cannot test or exclude the lookup rival, and no exclusion follows from any of its outcomes (E35-2)".
  - E35-2: "The reachable-set lookup non-claim remains unchanged".
  - E36-6: O7 is "an exploratory restricted-comparator fixture, not a required behavioral negative control".
- The dispatch's "g has ≈0 gain over the full predictor" is also inverted. Inside the O7 system, the full (κ-row) predictor has ≈0 gain over the fixed-κ predictor: Pred_full ≡ Pred_μ.
- **Correction to my own earlier record.** `ckappa_oracle_scope_record_v1_adversarial_review_RD.md:164` said O7 "shows concretely that a rank-2 system can produce a κ-row gain". This run shows it did not, and why (below). The O7 null must not be cited as "μ-only systems produce no gain". E35-2's point that a smooth lookup contributes L_κ·Dg still stands.

**Confirmed O7 values (`stage_O7.json`).**

- Status EVALUATED, admissible, 0 voids.
- g rank 6/6 with **σ₁ = 1.0789**. Note: that is the g-fit design's σ₁. The O7 stacked-Jacobian σ₁ is 1.5095 (AB→CD), with third ratio 2.6e-16 to 7.2e-16 in all 6 folds. That is resolved rank 2, below the [1e-10, 1e-6] band, so no B3 stop was due (`stage_O7.json:795`).
- **CNA's g claim ✓.** `g_coefficients` (`:508`) = [3.7e-17, 8.1e-18, 1.6e-17, 1.2e-17, **0.14038**, −8.2e-17], i.e. g ≈ 0.1404·μ_x·μ_y.
- **`exact_reduction_to_cross_term: false` (`:253`).** This is a float-rounding artifact of the frozen definition, not a code bug. The code uses exact `== 0.0` with no tolerance (`stages.py:796`), which is what `manifest.json:243` freezes ("exactly 0"). The reduction holds to 1e-16 and is forced by symmetry. YOURS: refitting the six monomials to the committed stage-4 charts gives zero non-cross terms for uniform weights and for random orbit-invariant weights.
- **CNA's L_full = L_μ ✓ (YOURS).** (H − L_full)/H = 5e-16 to 3.5e-15 for every group and size. measured_gain/H is identical, so the gain is numerically zero. Pooled measured_gain is 4e-24 to 2e-21, scaling with H.
- **CNA's flat R ✓.** ALL 0.004377 / 0.004376 / 0.004376 / 0.004370 at ε_syn 0.02 / 0.05 / 0.1 / 0.25; MARG ≈0.00449; XOR ≈0.00433. "0.0044" is right to two figures.
  - Flatness means H and S both scale as ε². H is the first-order omission of the local term L_κ∇g·dμ, not curvature (curvature would make R grow with ε).

**Is R ≈ 0.004 the right figure, and how does it relate to O6's 0.08?** Yes, as O7's own H/S. It is the fraction of O7's response energy carried by g's local κ-variation that **neither** global linear predictor captures (L_full = L_μ = H). It is not a headroom figure and not comparable to O6's 0.08. O6's κ is an independent fixed state direction, which the full model recovers exactly. O7's κ is slaved to μ, and no global model recovers it. The S values are similar (O7 3.16e-5, O6 2.97e-5 at 0.1), so the gap is in H.

**Is the zero gain zero by construction? Yes. CNA's mechanism is confirmed in structure.**

The O6/O7 fit is B = argmin Σ_p w_p ‖L_p(B − M_p·dmu)‖², with M_p = [I₂; ∇g(μ_p)]. In O6, M is a constant I₃.

- (a) **Exact flip orbits (YOURS, from `stage_O1.json` exact charts).** Each orbit A {0,5,10,15}, B {1,4,11,14}, C {2,7,8,13}, D {3,6,9,12} is {(±μ_x, ±μ_y)} with κ → sign-flip under each single flip (the Klein four-group). Every fit set is a union of two orbits (`fold_spec`).
- (b) **∇g = 0.1404·(μ_y, μ_x)** sums to exactly 0 over each orbit (YOURS). Each component is odd under one of the flips.
- (c) **Block orthogonality, measured in every fold of both O6 and O7 (YOURS from `fit_freeze_O7.json` / `stage_O6.json`).** The √w-weighted 3-column design's singular values are exactly the 2-column (B_μ) singular values plus one extra (e.g. O7 AB→CD: {0.2814, **0.18722, 0.15352**} vs {0.18722, 0.15352}). So Σ_p w_p L_μᵀL_κ = 0 over every fit set, and the κ column decouples.
- Given (c), B's μ rows equal B_μ's exactly, and B's κ row = (ΣG_κκ)⁻¹·Σ_p G_κκ,p·∇g_p·dmu. That is zero when G_κκ,p is equal within each orbit, which follows from the world's flip symmetry with (b). Then B ≡ B_μ, Pred_full ≡ Pred_μ, and gain = 0 up to rounding. This is what (e) shows.
- **UNVERIFIED pieces.**
  - The fitted B matrices are not committed (only `B_sha256`), so "κ row = 0" is inferred from (c), (e) and the identity, not read.
  - The within-orbit equality of G_κκ,p and of the history weights needs L, which needs package code I did not run.
  - Both are implied by the world symmetry, and the observed 1e-15 relative gain is the expected footprint.
- **Generality.** Any g respecting the world's (odd, odd) symmetry has an orbit-cancelling gradient. So O7's null would hold for every symmetric smooth μ-lookup, not just this quadratic.

**Implication for a neural test (MAJOR, M-1). Flag plainly.**

- **What the statistic detects.** It detects κ-sensitivity of the edited coordinates only when it is **coherent across flip orbits**: a fixed global linear κ readout direction, as in O6, where gain = H. κ-sensitivity whose sign or direction alternates across an orbit cancels in the κ row and lands in the shared residual (L_full = L_μ). That gives a non-POSITIVE outcome, because L_full ≤ L_μ/2 fails.
- **Does the same cancellation null a state that carries κ linearly?**
  - If "linearly" means a fixed readout direction: no. O6 is exactly that case.
  - If "linearly" means linear in κ along a hidden direction whose effective sign depends on the orbit: yes. Examples: a recurrent code roughly equivariant under the world flips, where the κ-carrying direction is mapped to itself while κ changes sign; κ stored jointly with sign(μ_x·μ_y); a gated or region-dependent κ code. These use κ for prediction, but the global-B gain cancels by the same identity.
  - Nothing in the frozen records excludes such codes for a GRU trained on this symmetric world.
- **The reverse limit.** A μ-only map that breaks the symmetry has a non-cancelling average gradient. It can produce a positive κ-row gain (E35-2). So neither outcome separates κ-aligned use from a smooth μ-lookup.
- **Consequence.** Under the current §6 commitments, a neural NOT SHOWN would mean only "no orbit-coherent, globally linear κ direction found in the edited coordinates". It could not mean "κ not used", and it would say nothing about the lookup rival.
  - This is a **design flaw for the neural test, not only a wording issue**, because a plausible κ-using encoding is structurally invisible to it.
  - It is not a defect of this oracle run. §6 is not executable (E36-1), and the inference specification "must be reviewed and frozen before checkpoint inspection".
- **Recommendation (for the RL/Astra; not adopted here).** Before any neural inference specification, address orbit coherence. Options:
  - orbit-resolved or sign-aligned fits;
  - per-prefix local Jacobian comparisons;
  - reporting the fitted κ-row norm and orbit-resolved gains;
  - a positive-control fixture in which κ is carried linearly with orbit-dependent sign. The global statistic should fail on it, which would demonstrate the blind spot.

  Any of these is a new ruling under the standing approval, with Astra review.

## (5) s = 0.5 exclusions

**Descriptive only; internally consistent; the units are not normalized. NOTE.**

- **Descriptive only.** O3–O5 are "Descriptive only" (v1.3_E36 item 8 source line; `stage_O5.json` `descriptive_only: true`). They use the O4 directions and chart edits, not the O6/O7 edits. §5 is determined by O6 at ε_syn = 0.1 alone. Nothing non-descriptive depends on them.
- **Consistency (YOURS).**
  - O4 at s = 0.5: 1947/2048 valid (`stage_O4.json:183`). 101 invalid (prefix, direction, sign) triples, perturbed chart only.
  - O5 validity does not depend on the continuation, so its count must be a multiple of 16: 1760 = 16 × 110. The 9 extra triples come from O5 also requiring the κ-zeroed chart to be valid (`stages.py:1155–1162`).
- **Units.** O5 `law_mass` is Σ P_h(prefix, continuation) over excluded occurrences. P_h sums to 1 and each history carries 64 directions × 2 signs, so the total is 128 (denominator 127.99999… at s = 0.1 and 0.25).
  - Check: 128 − 8.39463 = 119.60537, exactly the s = 0.5 denominator (`stage_O5.json:152–156`).
  - So 8.39 is 6.56% of law mass (count share 5.37%), not a mass above 1.
  - Recommend reporting the normalized fraction next to the raw number in future reports.
- Invalid edits concentrate in orbit A (O4: 22/20/21/20 for prefixes 0/5/10/15, the largest |μ|), as expected near the simplex boundary.

## Other checks

- **Stops and guards.** Every gate is satisfied, so no stop or guard was due:
  - O1 PASS, 272/272, mismatch 0;
  - O2 max |Δ| 2.026e-10 ≤ 1e-8;
  - O6 identity 4.4e-16 ≤ 1e-9;
  - O7 third ratio ≤ 7.2e-16, not in the band, no σ stop;
  - void ceiling not approached (0 of 5);
  - coverage 1.0 everywhere;
  - `guard_failing_phi` all 0 in O6/O7;
  - O5 value_error / non_finite 0;
  - projection T_rem 12.26 s ≤ 539.71 s limit;
  - float count ≤ 788,480;
  - stop COMPLETED, exit 0 in both `stop_kind.json` and the index.
- `val_readout_rejection: "UNVERIFIED"` in O1 is the declared frozen value (`manifest.json:228`).
- O7 edits reuse the O6 directions as frozen (`manifest.json:245`, `draws.py:100–106`); not a deviation.
- **E36 / RL.**
  - No contradiction found. Order O1→O2→O6→O7→O3→O4→O5 (`run.log`, E36-13).
  - Retained sample 1000. Measured gain reported separately (E36-9). O7 about its own chart, with reachable disagreement reported (E36-6).
  - No checkpoint loaded; the only subprocess is `git show`.
  - REPORT.md stays within the claim ceiling. Its only forbidden-list term is inside the negated claim-ceiling sentence.

## Findings

- **Blockers.** None.
- **MAJOR M-1 (prospective neural design, §6).** The global-B gain cancels any orbit-odd κ-sensitivity by the W2 flip symmetry (`stages.py` O6/O7 fits via `_fit_blocks`, `stages.py:381–395`; fit sets are orbit unions, `stage_O1.json` `fold_spec`/`orbits`; evidence `stage_O7.json:626ff`, `fit_freeze_O7.json` singular values). A neural NOT SHOWN under §6 as frozen would not mean "κ not used". Resolve before any inference specification.
- **MINOR m-1.** Stale labels: `driver.py:39` (`phase`), `__init__.py:6`, `manifest.json:2,4,11`. Handle with an additive erratum; do not edit the immutable manifest.
- **NOTES.**
  - n-1: versions in results are pinned constants (`driver.py:45`), not observations.
  - n-2: VmHWM and wrapper wall time are not in any committed file.
  - n-3: the reported "σ₁ 1.079" is the g-fit σ₁, not the Jacobian σ₁.
  - n-4: `exact_reduction_to_cross_term` uses an exact-zero definition (`stages.py:796`, `manifest.json:243`) that rounding defeats.
  - n-5: O5 `law_mass` is unnormalized (total 128).
  - n-6: true baselines are counted in the O6 bucket.
  - n-7: the dispatch's "lookup rival" and "g gain over the full predictor" framings are corrected in (4), as is my earlier review's L164.

No interpretation beyond the oracle claim ceiling is made here.
