# C-kappa oracle package (PR #13): Research Lead ruling on Q1-Q11, K1, M1-M5
Date: 2026-10-22 ~3:00 AM ET. Additive record. It changes no frozen scope file.
Inputs: Delegate code review /workspace/review/ckappa_pr13_code_review_RD.md (sha 5e1cb7ac...6180), CNA spot-check (Q2, Q3, Q6), PR #13 commit e99f0d39, IMPLEMENTATION_QUESTIONS.md f67ba25d, manifest_DRAFT.json b96a74e7.

## Precedence (K1, blocker)
1. The E36 verbatim text (Astra #36, in v1.3_E36 f6263fb8) governs over everything else.
2. Then: closure note 4ad1d217 > v1_4_N 3f0c5c12 > rest of v1.3_E36 f6263fb8 > v1.2 7e15e812 > v1.1 e40c288f.
3. RL records (CKAPPA_SCOPE_GOVERNING_SET_RL.md 6a5e0f24, CKAPPA_SCOPE_RL_RULING_B2_B3.md 6d75918f, this record) are implementation rulings. They are subordinate to E36 and cannot override it.
Fix: manifest_DRAFT.json lines 46, 61, 65 and IMPLEMENTATION_QUESTIONS.md lines 5-13 get this order, with E36 first.

## Q rulings
- Q1 ACCEPT (788,480 floats, n_O1 = 272).
- Q2 ACCEPT: O7 reuses the O6 draw (seed 35016); the O7_directions hash is marked shared with O6.
- Q3 REPLACE (wording only): "O7 z = Q2 * D_mu^-1 ((mu_x, mu_y) - mu_bar) is centered with the same P(a)-weighted mean and the same mu block of D as O6." Code at stages.py:887 already does this; no code change.
- Q4 ACCEPT: the sigma_3/sigma_1 stop runs before the admissibility branch, for any number of voids (B3).
- Q5 ACCEPT: rank-unresolved g gives O7 UNRESOLVED; the package continues to O3; no refit.
- Q6 REPLACE: "O5 uses the O4 perturbations and the O4 validity rule (all four p >= 1e-6), checked before Phi is evaluated, on both Phi(b_a + Delta) and its kappa-zeroed counterpart. One common mask applies to the numerator and the denominator of R_G. Invalid, ValueError and non-finite cases are left out of both means and reported by count and law mass, per size and per group. O5 stays descriptive." (Code change: M4.)
- Q7 REPLACE: keep the logic (coverage on resolved folds, coverage failure checked first). Every unresolved fold still gets a coverage row marked "not propagated" (E36-4 requires every fold).
- Q8 REPLACE: exit code 6 stays. driver.py:71-84 must not overwrite O6's outcome label with the stop kind; both are recorded separately.
- Q9 ACCEPT: the projection is optimistic; the 540 s and 595 s stops are the real bounds.
- Q10 REPLACE: propagate every edit. On guard-failing edits, catch ValueError and non-finite results, count them, store them as null. The same failure on a scoreable edit is PIPELINE INVALID.
- Q11 ACCEPT.

## Majors
- M1: at runtime, before any computation, preflight re-hashes every code file, run_package.sh, the inputs and the filed application against the sealed manifest. Any mismatch is an INTEGRITY STOP with no outcome label.
- M2: the Q10 handling is implemented; the writer serializes non-finite values as null; results.json and stop_kind.json are written on every exit path, including stops.
- M3: PIPELINE INVALID is reserved for N1, manifest item 8, the B3 sigma stop and the Q10 scoreable-edit failure. The other fail-closed checks stay but are relabelled INTEGRITY STOP (non-N1): they halt with no outcome label and are reported separately. The empty-O7-design case is labelled UNRESOLVED per E36-6/7 and guarded by an assertion; it is not expected to be reachable.
- M4: implement the Q6 mask (stages.py:1046-1123) before the seal.
- M5: the application's citation list (manifest_DRAFT.json:381) covers E36 / v1.3_E36 f6263fb8, closure note 4ad1d217, v1_4_N 3f0c5c12, v1.2, v1.1, both RL records (6a5e0f24, 6d75918f), this record, IMPLEMENTATION_QUESTIONS.md, the Delegate review 5e1cb7ac, and all code and input hashes.

## Run environment
The run uses the pinned Python 3.12.3 and NumPy 1.26.4 in a checkout that contains 5d9d8a7, on the cloud agent's machine, not this box. If the pins can't be installed exactly, STOP and report; no substitution.

## Order from here
Cloud agent applies K1, M1-M4 and the Q wording, re-hashes, runs nothing beyond py_compile and bash -n. Delegate delta check. RL files the application (M5). Its sha goes into the manifest, the manifest is sealed, then step 0 and the run.
No consciousness claim is made or implied.
