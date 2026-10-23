# Implementation questions addendum RL1

Additive record for `review/CKAPPA_PR13_RL_RULING_Q1_Q11.md` (`9a2ea59bc6a1063eed108b66d23a8c8e7edcec6f683393be2be0dc51ab1d0c1d`). It does not replace `IMPLEMENTATION_QUESTIONS.md`. Earlier text was changed in place only at the lines named below. The manifest stays unsealed. `standing_approval_application.sha256` stays `PLACEHOLDER`.

Line numbers are the lines after this addendum's companion commit. The centering statement at `ckappa_oracle/stages.py:960` (`z_prefix = q2 @ ((mu - mean2) / sd2)`) was not edited. The ruling said that statement, then at line 887, already matches Q3.

## Rulings

| Ruling | What was applied | File and lines |
| --- | --- | --- |
| K1 | E36 verbatim text first, then closure note > v1_4_N > rest of v1.3_E36 > v1.2 > v1.1. The three RL records are implementation rulings, subordinate to E36. | `IMPLEMENTATION_QUESTIONS.md:5-9`. `manifest_DRAFT.json:16-81` (precedence array; the old line 46 text is now the rank-1 field at `23`). `manifest_DRAFT.json:82` (old line 61). `manifest_DRAFT.json:86` (old line 65). |
| Q1 | Accepted counts only. No question-text edit. The overrun stop in code follows M3. | Question text left at `IMPLEMENTATION_QUESTIONS.md:25`. Code: `ckappa_oracle/runstate.py:78-83`. Manifest: `manifest_DRAFT.json:348`. |
| Q2 | Accepted. No text edit. | `IMPLEMENTATION_QUESTIONS.md:27-29` left as filed. |
| Q3 | Wording only. No edit to the centering statement. | `IMPLEMENTATION_QUESTIONS.md:39`. `manifest_DRAFT.json:245`. Code unchanged at `ckappa_oracle/stages.py:960`. |
| Q4 | Accepted. No text edit and no code edit. | `IMPLEMENTATION_QUESTIONS.md:41-43` left as filed. |
| Q5 | Accepted. The existing status strings were left in place. | `IMPLEMENTATION_QUESTIONS.md:45-47` left as filed. `ckappa_oracle/stages.py:756-757` still says `G RANK UNRESOLVED` and `g rank UNRESOLVED`. The package still continues to O3 and does not refit. |
| Q6 | Wording, and the mask in code (M4). | `IMPLEMENTATION_QUESTIONS.md:51`. `ckappa_oracle/stages.py:1116-1242`. |
| Q7 | Coverage stays on resolved folds and is checked first. Every unresolved fold gets a row marked `not propagated`. | `IMPLEMENTATION_QUESTIONS.md:55-60`. `ckappa_oracle/stages.py:124-141`, `645-647`, `1011-1041`. `manifest_DRAFT.json:233`. |
| Q8 | Exit 6 stays. The stop kind does not replace the O6 outcome label. | `IMPLEMENTATION_QUESTIONS.md:64`. `ckappa_oracle/driver.py:22-34` (this replaces the old `driver.py:71-84`). `ckappa_oracle/driver.py:148-207`. `ckappa_oracle/report.py:38-45`. `manifest_DRAFT.json:319-328`. |
| Q9 | Accepted. No text edit and no code edit. | `IMPLEMENTATION_QUESTIONS.md:66-68` left as filed. |
| Q10 | Every edit is propagated. Guard-failing ValueError and non-finite results are counted and stored as null. The same failure on a scoreable edit is `PIPELINE INVALID`. | `IMPLEMENTATION_QUESTIONS.md:72`. `ckappa_oracle/stages.py:95-122`, `579-591`, `981-993`. `ckappa_oracle/runstate.py:87-92`. `ckappa_oracle/io.py:31-58`. `manifest_DRAFT.json:351` and `389`. |
| Q11 | Accepted. No text edit and no code edit. | `IMPLEMENTATION_QUESTIONS.md:74-88` left as filed. |
| M1 | Before any oracle computation, preflight re-hashes every `ckappa_oracle/*.py` file, `run_package.sh`, the three inputs, and the filed application against the sealed manifest. A mismatch is `INTEGRITY STOP` with no outcome label. | `ckappa_oracle/preflight.py:104-191`. |
| M2 | Non-finite values serialize as null. `results.json` and `stop_kind.json` are written on the Python exit paths, with a text fallback if the full writer fails. The wrapper writes the same two files if they are missing after the process exits, including a kill before the interpreter starts. | `ckappa_oracle/io.py:31-58`. `ckappa_oracle/driver.py:64-146`. `ckappa_oracle/__main__.py:9-44`. `run_package.sh:50-92`. `manifest_DRAFT.json:389`. |
| M3 | `PIPELINE INVALID` remains for N1 fixture failures, manifest item 8, the B3 sigma stop, and a Q10 scoreable-edit failure. The other fail-closed checks are `INTEGRITY STOP` with classification `non-N1` and no outcome label. An empty reduced O7 design is labelled `UNRESOLVED` and then guarded by an assertion. | `ckappa_oracle/io.py:19-28`. `ckappa_oracle/inputs.py:38-86`. `ckappa_oracle/draws.py:18`, `46`, `55`. `ckappa_oracle/runstate.py:78-83`. `ckappa_oracle/stages.py:326`, `378`, `467`, `639-644`, `841-847` (B3 sigma stop stays `PIPELINE INVALID`), `876-892`. `ckappa_oracle/driver.py:22-26`. `manifest_DRAFT.json:314-328` and `348`. |
| M4 | The Q6 mask is in `stage_o5` before any seal. | `ckappa_oracle/stages.py:1116-1242`. |
| M5 | The application citation list names E36 / v1.3_E36, the closure note, v1_4_N, v1.2, v1.1, both earlier RL records, this Q1-Q11 record, `IMPLEMENTATION_QUESTIONS.md`, the Delegate review, and the code and input hashes. The application sha stays `PLACEHOLDER`. The v1.3 build script was already in the old citation sentence and is still listed. | `manifest_DRAFT.json:397-492`. |

## In-place changes of earlier text

1. `IMPLEMENTATION_QUESTIONS.md:5-9` replaced the old lines 5-13 precedence list. Q1, Q2, Q4, Q5, Q9, and Q11 were not rewritten.
2. `IMPLEMENTATION_QUESTIONS.md:39` replaced the O7 standardization bullet with the Q3 sentence.
3. `IMPLEMENTATION_QUESTIONS.md:51` replaced the Q6 provisional reading.
4. `IMPLEMENTATION_QUESTIONS.md:55-60` replaced the Q7 provisional bullets. The coverage-first logic and the `REFERENCE RANK UNRESOLVED` / `REFERENCE COVERAGE NOT MET` split were kept.
5. `IMPLEMENTATION_QUESTIONS.md:64` replaced the Q8 provisional reading. Exit code 6 and the stop kind name were kept, and the non-overwrite rule was added. The cross-reference in that paragraph now says "ruling on question 7" where it had said "provisional reading of question 7".
6. `IMPLEMENTATION_QUESTIONS.md:72` replaced the Q10 provisional reading.
7. `manifest_DRAFT.json:11` draft note now points at this addendum. `sealed` is still false.
8. `manifest_DRAFT.json:12-15` question-file hash regenerated.
9. `manifest_DRAFT.json:16-82` precedence array and top-level precedence rule.
10. `manifest_DRAFT.json:86` item 1 precedence rule. The adopted-amendment sentences were kept and are now explicitly unable to override E36. The phrase "the rank-2 record's addition" was left as it stood.
11. `manifest_DRAFT.json:170-187` code hash list regenerated.
12. `manifest_DRAFT.json:233` coverage sentence for Q7.
13. `manifest_DRAFT.json:245` O7 z sentence for Q3.
14. `manifest_DRAFT.json:314-328` item 8 stop vocabulary, including the empty-O7 sentence.
15. `manifest_DRAFT.json:348` schedule overrun stop.
16. `manifest_DRAFT.json:351` nest sentence for Q10 and the accepted Q11 nest.
17. `manifest_DRAFT.json:389` JSON rule: non-finite values are null, and both result files are written on every exit path.
18. `manifest_DRAFT.json:391` `results.json` field list adds `o6_section5`.
19. `manifest_DRAFT.json:397-492` item 12 citation list and the copied code and input hashes. Application `sha256` at lines 9 and 401 is `PLACEHOLDER`.

## Not applied as a second wording

`IMPLEMENTATION_QUESTIONS.md:25` still says a float count above 788480 is `PIPELINE INVALID`. Q1 was accepted for the counts 788480 and n_O1 = 272, and the ruling did not name that line. M3 relabels that same overrun `INTEGRITY STOP` (non-N1). The code and manifest item 9 follow M3. The question sentence was not rewritten.

`INTEGRITY STOP` uses exit code 7. The ruling names the stop kind and "no outcome label" and does not number the exit. Exits 0 through 6 were already bound, so 7 keeps this stop separate from them.

Under the default interpreter, a reached empty O7 design writes the stage file with label `UNRESOLVED` and then the assertion fires, so the process does not continue into that fold's fit. With assertions disabled, the assertion is absent and `stage_o7` returns after the `UNRESOLVED` write.
