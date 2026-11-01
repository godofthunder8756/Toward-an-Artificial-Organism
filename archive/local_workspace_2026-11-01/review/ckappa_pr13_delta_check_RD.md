# Delta check: PR #13, e99f0d39..697200e8, against the RL Q1–Q11 ruling and my review 5e1cb7ac

Research Delegate, 2026-10-22, about 3:30 AM ET. This is a new file. The check was read-only and static: an `ast` parse of `ckappa_oracle/*.py`, `bash -n run_package.sh` and sha256 checks only. No package code, stage, fixture or timing sample was run, and no checkpoint was loaded. I fetched the new head into the scratch clone at `/workspace/scratch/pr13`. `/workspace/repo` was not touched, and nothing was posted to GitHub.

## Verdict: **CLEAR WITH NOTES**

There are no blockers. K1 and M1–M5 are applied, and so are the Q3, Q6, Q7, Q8 and Q10 rulings. The regression scan found nothing that undoes an earlier pass and no new contradiction with E36. The notes below are recommendations for the application text or optional hygiene. None of them needs a code change before the seal.

## Hashes
| Item | Claimed | Verified |
|---|---|---|
| RL ruling `/workspace/review/CKAPPA_PR13_RL_RULING_Q1_Q11.md` | 9a2ea59b… | `9a2ea59bc6a1063eed108b66d23a8c8e7edcec6f683393be2be0dc51ab1d0c1d`. The branch copy `review/CKAPPA_PR13_RL_RULING_Q1_Q11.md` is byte-identical. |
| Head / review-record commit | 697200e8 / b8fd7cef | `697200e860a5f53486ca59245e1df1251fbecb4b`, parent `b8fd7ce`. The branch copy of my review is byte-identical to 5e1cb7ac. |
| manifest_DRAFT.json | 936524a6 | `936524a6b469364f18184c744f0b5cceb3eb363a8687b19fadb31eff92331389`. `sealed: false`, application `PLACEHOLDER` / `PLACEHOLDER_NOT_FILED`. |
| IMPLEMENTATION_QUESTIONS.md | fc1931f6 | `fc1931f62adbb7e11847fcadde939c25aca6b28dfcbdcf2eb054c0c2bd10b834`. Matches manifest L14. |
| IMPLEMENTATION_QUESTIONS_ADDENDUM_RL1.md | e06d784e | `e06d784ed8700b821fbd4db4707ad35fd9500e2f64220a146d82e501bd36e3a4` |
| Code delta | 10 changed, 7 unchanged | Confirmed. Changed: `__main__`, draws, driver, inputs, io, preflight, report, runstate, stages, `run_package.sh`. Unchanged: `__init__`, geometry, linalg_fit, outcomes, pinned, schedule, world. All 17 hashes match manifest item 2 and the item 12 copy. |
| `review/ckappa/` bundle | unchanged | No diff in the range, and `SHA256SUMS` still verifies. |

## Items (one line each)
| Item | Status | Evidence |
|---|---|---|
| K1 precedence | PASS | E36 verbatim is rank 1 in `manifest_DRAFT.json:16–24`, the top-level rule (`:82`) and the item 1 rule (`:86`). It is also first in `IMPLEMENTATION_QUESTIONS.md:7–9`. "A higher rank wins" is gone. The RL records are marked subordinate to E36. See D-n1. |
| Q3 wording | PASS | `IMPLEMENTATION_QUESTIONS.md:39` and manifest item 5 have the centered form. Code is unchanged at `stages.py:960`. |
| Q6 / M4 O5 mask | PASS | `stages.py:1155–1162`: O4 validity is checked on both inverse_chart(θ+Δ) and its κ-zeroed counterpart **before** Φ. The one common mask covers H and the response energy. Invalid, ValueError and non-finite cases are excluded and recorded by count and law mass per size and group (`:1116–1121`, `:1208–1232`). `probability_guard_applied: true` and `descriptive_only: true` are set. |
| Q7 not-propagated rows | PASS | `stages.py:124–141`. Each unresolved fold gets a row at every ε_syn (`:645–647` for O6, `:1040` for O7). `_section5` (`:483–489`) still classifies on the resolved folds only, so the null rows never reach `classify_group`, and coverage is still checked before REFERENCE RANK UNRESOLVED. |
| Q8 exit 6 keeps the O6 label | PASS | `driver.py:22–33`: for any stop other than PIPELINE INVALID or INTEGRITY STOP, `section5` is the O6 label. `o6_section5` is also written on its own (`:59`), and the stop kind is recorded separately. `report.py:38–45` prints both. |
| Q10 guard-failing Φ | PASS (see D-n2) | `stages.py:95–122`. The guard is computed before propagation (`:578`, `:976–980`). For a guard-failing edit, ValueError and non-finite results are counted in `guard_failing_phi` and held as None. For a scoreable edit, the same failure calls `_fail`, giving PIPELINE INVALID (exit 2). A non-finite q in the retained sample is stored as null (`runstate.py:87–92`). |
| M1 runtime re-hash | PASS (see D-n4) | `preflight.py:126–180`, called at `:191` before draws or any computation. It checks that the file set equals the 17 listed files, re-hashes each one including `run_package.sh`, re-hashes the three inputs via `git show`, and re-hashes the application at its path. Any mismatch is INTEGRITY STOP, exit 7, `section5: None`. |
| M2 safe writer | PASS | `io.py:31–58`: non-finite values become null, and NumPy scalars and arrays are handled. Python exit paths have fallbacks in `driver.py:64–146`, including a text-only fallback. A bad thread setting writes both files in `__main__.py:9–44`. The wrapper writes both files when they are missing, including after a kill or a non-start (`run_package.sh:63–92`). |
| M3 stop vocabulary | PASS | The only remaining `PIPELINE INVALID` sites are: O1 fixture (`stages.py:313`), O2 derivative and fixture (`:343`, `:354`, `:376`), O6 B and Pred identity (`:548`, `:621`), the Q10 scoreable failure (`:104`, `:116`), and the B3 σ stop (`:847`). Everything else is `integrity_stop` with exit 7, `classification: non-N1` and no label: inputs, draws, the overrun, zero SD, O2 count, coverage mass 0, O6 edit count, and the M1 checks. Manifest item 8 lists both kinds. |
| M5 citation list | PASS (see D-n3) | Item 12 `citation_list`, `manifest_DRAFT.json:397–492`: v1.3_E36 (holds E36), closure, v1_4_N, v1.2, v1.1, RL 6a5e0f24, RL 6d75918f, RL Q-ruling 9a2ea59b, IMPLEMENTATION_QUESTIONS fc1931f6, my review 5e1cb7ac, the build script, the inputs and all 17 code hashes. This matches RL M5 as worded. |
| (a) overrun is INTEGRITY STOP | PASS in code and manifest; stale line noted | Code: `runstate.py:78–83`. Manifest item 9 schedule note says "INTEGRITY STOP (non-N1), with no outcome label". `IMPLEMENTATION_QUESTIONS.md:25` still says PIPELINE INVALID. That supersession is recorded only in ADDENDUM_RL1 L53, which is mentioned in the manifest's draft note but neither hashed nor in the citation list. See D-n3. |
| (b) exit 7 | PASS | `io.py:20–28`. Exits in use: 0 COMPLETED, 1 EXECUTION ERROR, 2 PIPELINE INVALID, 3 PROJECTION HALT, 4 CAP RESERVE REACHED, 5 PREFLIGHT FAILED, 6 STEP 0 SAMPLE SHORT, 7 INTEGRITY STOP, and 124/137 CAP REACHED from the wrapper. All are distinct. The wrapper reads exit 7 through `stop_kind.json`. |
| (c) empty O7 design | PASS (see D-n5) | `stages.py:876–892`: the stage file with `status`/`label: UNRESOLVED`, `derivatives_evaluated: false` and `predictions_evaluated: false` is written **before** the `assert`. `fit_from_svd` for that fold comes after it at `:893`, so that fold is never fitted. It is unreachable: with at most 4 voids, every fold keeps at least 4 of its 8 fit prefixes. |

## Regression scan
- **B1, B2 and `rcond`:** `outcomes.py` and `linalg_fit.py` are unchanged, so B1/N1 order, the count test, floats-only band, B2 (only UNRESOLVED is unscored; σ₁ = 0 scored with rank 0) and the same-SVD fit with `rcond=1e-10` all still hold.
- **B3 and the O7 rules:** the σ stop still runs before the admissibility branch for any number of voids (`stages.py:814–847`, logic unchanged). It is still PIPELINE INVALID. The void ceiling is still at least 5 (`pinned.py` unchanged), and g is never refit.
- **Timing:** unchanged in `runstate.py` (`check_deadline`, `project`; limit 540 − T_elapsed). The wrapper head (`run_package.sh:1–19`) is unchanged: T0 first, threads, `prlimit --as=4000000000`, `taskset -c 0`, kill at 595 − elapsed. Only the post-run section changed.
- **Pins and seeds:** `pinned.py` is unchanged. Pins are 3.12.3 / 1.26.4, seeds 35004/35006/35007/35016, and §6 seeds 36100–36109 remain prospective only.
- **Per-array hashes:** the record format and write-at-draw are unchanged; only the stop labels changed (`draws.py:18/46/55`).
- **Other checks:**
  - No checkpoint, weight or pickle loading was added; the only new subprocess is `git show` of the three inputs in preflight.
  - `eps_syn` naming is unchanged.
  - The forbidden-term check (consciousness, autopoietic, alive) gives the same result as before: "consciousness" appears only in REPORT.md's negated claim-ceiling line. The RL record also carries a negated line at L36.
- **E36:** I found no new contradiction.

## Notes (non-blocking)
- **D-n1. Wording of the precedence ranks.** The manifest puts the RL records at numeric ranks 7–9, below v1.1, as the RL ruled.
  - The only live clash between an RL record and a scope file is B2 against v1_4_N L35 ("rank-deficient"). E36-3 and E36-8, which sit at rank 1, decide that clash in B2's favour, so there is no substantive conflict.
  - Recommend one line in the application: "RL rulings are the operative readings of ranks 2–6 where those texts are silent or ambiguous. B2 is the operative reading of v1_4_N L35."
- **D-n2. A ValueError skips the counters.** When `phi_float` raises, `run.phi` raises before `_note_float` runs (`runstate.py:103–108`). So a guard-failing ValueError call is not counted in `float_count`, the sample or `retained_o6_sample`. Only a non-finite result leaves a null record.
  - This is harmless: 788,480 is an upper bound, and the counts are in `guard_failing_phi`.
  - It does mean "stored as null" holds only in the in-memory triple for ValueError cases. State this in the application, or count the call before re-raising.
- **D-n3. The addendum is not citable as it stands.** ADDENDUM_RL1 (e06d784e) carries the only record that `IMPLEMENTATION_QUESTIONS.md:25` is superseded and that exit 7 was assigned, but it is neither hashed in the manifest nor in the citation list.
  - Recommend the application cite ADDENDUM_RL1 e06d784e and this delta check, and state: "IMPLEMENTATION_QUESTIONS.md:25 ('PIPELINE INVALID' for a float overrun) is superseded by RL M3 and the room ruling: INTEGRITY STOP, exit 7."
  - Optionally also cite the raw Astra file `astra_consult36_response.txt` c8342d5a. It is hashed in manifest item 1 as a reference but is not in the citation list. RL M5 accepted v1.3_E36 as the E36 citation.
- **D-n4. What M1 does and does not cover.**
  - M1 does not re-hash the `review/ckappa/` scope bundle, `IMPLEMENTATION_QUESTIONS.md` or the addendum. The RL scoped M1 to code, wrapper, inputs and application, so this is optional.
  - The application path is resolved relative to the package root unless it is absolute (`preflight.py:171–180`). The filed application must therefore exist at that path on the run machine. Keep `standing_approval_application.path` and item 12 `path` identical.
- **D-n5. The empty-O7 assertion stops the package.** With assertions on, which is the default, the empty-O7 `assert` raises AssertionError. The driver turns that into EXECUTION ERROR, exit 1, and O3–O5 do not run.
  - That differs from the E36-7 note in letter, but the path is unreachable. Manifest item 8 says "not PIPELINE INVALID" without naming the resulting exit.
  - Add "(would surface as EXECUTION ERROR, exit 1)" in the application. Earlier folds' fits computed in that loop are in memory only and are never frozen or scored.
- **D-n6. Wrapper edge cases (not regressions).**
  - A kill landing after `results.json` is written but before the process exits gives a `results.json` that says COMPLETED alongside an index that says CAP REACHED. That window is very small.
  - A corrupt `stop_kind.json` would make `json.loads` raise in the wrapper (`run_package.sh:55–57`) before `post_run_index.json` is written.
  - Both are optional hardening.
- **D-n7. Carried from 5e1cb7ac and not applied.** The RL did not require any of these.
  - N3: an incomplete run reports the O6 label as `section5` without an "O7 integrity check not completed" caveat.
  - N4: `exact_reduction_to_cross_term` uses float `==`.
  - N5: `derivatives_evaluated: False` on a NOT ADMISSIBLE O7.
  - N6: two different spellings of the G RANK UNRESOLVED string.
  - N11: "the rank-2 record's addition" wording in manifest item 1.
- **D-n8. Run environment.** RL "Run environment" applies: Python 3.12.3 and NumPy 1.26.4 in a checkout that contains `5d9d8a7`. This box (3.13.5 / 2.5.4) is not that environment.

## Next
1. The RL files the application. It should cite the full governing set per M5, plus ADDENDUM_RL1 and this check (D-n3), and carry the D-n1, D-n2 and D-n5 lines.
2. The application's path and sha go into the manifest. The two `path` fields must match (D-n4).
3. Copy to `manifest.json`, seal, then step 0.

Nothing executes before the seal. Claim ceiling unchanged: oracle-only.
