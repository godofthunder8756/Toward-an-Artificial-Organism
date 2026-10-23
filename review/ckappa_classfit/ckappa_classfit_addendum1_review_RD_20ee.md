# Read-only review of Application v1 Addendum 1 / RL-14 (Research Delegate)

**Status:** review record only. It establishes no result.

- **Reviewed at:** PR #14 HEAD `8ff3fb15445bcbbfdae86246663321d561d5a42d`, after a620317a (application), 992a30e6 (seal) and 8ff3fb15 (outputs). Written 2026-10-23, about 09:55 ET.
- **Addendum:** `/workspace/review/ckappa_classfit_application_v1_ADDENDUM_1.md`. sha256 is `5f7e06e084e8da400e6c98f95b9e2f093cafcc5ba1fe1cd686c263e603ff4131` ✓ (verified).
- **How I worked:** static reading only. I did not run the wrapper, any stage or preflight, and I pushed and posted nothing.

## Ruling: CONCUR WITH CONDITIONS

The administrative reading is sound. The plan works with **no code change**. There are four conditions, C1 to C4 in §6. C1 matters most: a leftover canonical path would make the wrapper refuse at exit 7, and that refusal would itself use up attempt 2.

## (a) Shas and the seal diff

- **Attempt-1 files at 8ff3fb15.** All match:

  | File | sha256 |
  |---|---|
  | `classfit_outputs/results.json` | `b61a3fac…` ✓ |
  | `classfit_outputs/REPORT.md` | `c624901c…` ✓ |
  | `classfit_post_run_index.json` | `f363162f…` ✓ |
  | `classfit_outputs/run.log` | `ff948daf…` |
  | `classfit_outputs/stop_kind.json` | `7693b8d3…` |

  The addendum does not list the last two (see C2).
- **Manifest and application.** The sealed manifest is `364b7dad…` ✓. The application `…application_v1_1f6d.md` is `c726f37f…` ✓.
- **Seal diff.** `review/ckappa_classfit/classfit_seal_diff.txt` is `83b2bc7d…`. No sha for it was stated to check against, so I record this value.
  - It is a diff against `64f03292…` (the bf320dd5 manifest). It lists 8 changed fields: sealed, seal_status, the application path and sha256, evidence, notes, review_records and seal_timestamp. `disallowed_count: 0`.
  - My own `git diff bf320dd5 8ff3fb15 -- classfit_manifest.json` shows the same 8 fields. `standing_approval_application.status` stayed `"PENDING"`. That is the cause of attempt 1.
  - Evidence `tests/test_phi_count.py` is `3e811cc0…` and matches its bytes ✓.
  - Code, oracle, wrapper, tests and annex v5 are unchanged from bf320dd5 to 8ff3fb15 ✓.
- **Note.** Application v1 permits only "sealed=true, seal_status, the application path and sha, and the evidence/notes fields". The first seal also added `review_records` and `seal_timestamp`. These are harmless, because no code reads them (grep), but the addendum's re-seal list should cover them explicitly. See C3.

## (b) Attempt 1 did no study work

The code path, in order:

1. **Wrapper** (`run_classfit_package.sh:4–35`). Sets T0, cds, sets thread env vars, runs the stdlib-only pre-check (`outputs_gate` lstat). Passed: the directory was absent.
2. **`__main__`.** Checks the thread env and imports the driver. Module bodies only define things.
3. **`driver.main` → `preflight`** (`preflight.py:389–401`), with these steps before `load_manifest`:
   - `check_outputs_directory` (lstat, no write);
   - threads, clock, affinity and RLIMIT reads;
   - `check_no_gpu`;
   - `check_versions`;
   - `check_schedule_constants`, which is arithmetic on constants.
4. **`load_manifest`** (`:398` → `:201–222`) refuses at `:219`.

So **none of the following ran: B0** (`check_b0_budget` is at `:401`), the application hash (`:399`), the sealed hashes (`:400`), the `Run` claim and `run.log` (`runstate.py:28–42` comes after preflight, `driver.py`), array or input loading, and every propagation, fit and SVD.

**Writes.** `_write_pair(None, …)` claimed the absent directory and wrote `results.json`, `REPORT.md`, `run.log` (`"0.000000 PREFLIGHT FAILED"`) and `stop_kind.json`. The wrapper post-run block then wrote `classfit_post_run_index.json`. `git ls-files classfit_outputs` shows exactly those 4 files, plus the index. Nothing else was written.

**Information that could bias attempt 2: none about the study.**
- `results.json` has every count, timing, projection, sample and label null or empty. Its detail field holds only the refusal reason.
- `REPORT.md` is the fixed template, with "VALIDATION label: None" and "HEADROOM ALL/MARG label: None" (L60–62).
- The index carries `t0`, `wrapper_kill_budget_s` 594.977 s (which reveals about 23 ms of shell startup), and the RL-5 oracle re-hash (all match). None of this is an outcome, a seed or a timing of study work.
- One weak inference: passing `check_versions` shows the pinned Python and NumPy were present. That is environmental, not an outcome.

## (c) What `load_manifest`, `preflight` and `check_application_hash` validate

**Status.** `preflight.py:219` reads `if application.get("status") in (None, "PENDING", "PLACEHOLDER_NOT_FILED"): _fail(...)`.
- This is a **deny-list**. Any other value passes, including `"FILED"`. The comparison is exact and case-sensitive.
- CNA's description is confirmed. `"FILED"` passes.

**Other checks in `load_manifest`:**
- manifest file present and parseable as JSON (`:203–210`);
- `sealed is True` (`:211–212`);
- application is a dict (`:213–215`);
- application `sha256` is 64 lowercase hex characters (`:216–218`);
- `frozen_runtime == FROZEN_RUNTIME` (`:220–221`).

**`check_application_hash`** (`:244–268`). The path must be a non-empty string and the sha must be 64 hex characters. The file must not be a symlink and must be a regular file. The sha256 of the file must equal the manifest sha. Application v1 is unchanged (`c726f37f…`), so this passes and no re-filing is needed.

**`check_sealed_hashes`** (`:313–388`) checks:
- the exact implementation file set, plus the 6 oracle modules, by sha;
- every `items.governing` entry by path and sha;
- the `REQUIRED_GOVERNING` set, including annex v5 being present;
- the loaded oracle modules;
- `items.inputs` against the pinned values.

The listed re-seal changes (status, seal_timestamp, review_records, notes) touch none of these.

**Things no code checks:**
- the application's pinned pre-seal manifest sha `64f03292…` (it is not compared against anything);
- `review_records`, `evidence`, `notes`, `seal_timestamp` and `seal_status` (grep finds no reader);
- any self-hash of the manifest (S0 and the index only *record* `manifest_sha256`).

So the addendum **does not need** to be in `items.governing`. No `REQUIRED_GOVERNING` or `pinned.py` constant changes, and no code changes. If the addendum is added to `items.governing` instead of `review_records`, it is simply hashed at S0, and that also passes.

**Conclusion.** A re-seal from `364b7dad` changing only status → `"FILED"`, seal_timestamp, review_records (adding the addendum by path and sha) and one appended note would pass every preflight check up to B0. This is a static conclusion and has not been executed.

## (d) git mv interactions

**The gates check only the two exact names.**
- `outputs_gate.py:13–14` defines `OUTPUT_DIR_NAME = "classfit_outputs"` and `POST_RUN_INDEX_NAME = "classfit_post_run_index.json"`.
- `outputs_refusal` (`:26–53`) and `index_refusal` (`:56–68`) call `os.lstat(root/NAME)`. They never look at sibling paths.
- `classfit_outputs_attempt1/` and `classfit_post_run_index_attempt1.json` do not collide with anything. CNA's description is confirmed.

**Globs.**
- `preflight.py:325`: `(root/"ckappa_classfit").glob("*.py")`. It is unaffected.
- CNA missed one: `run_classfit_package.sh:161`, `outputs.glob("*.tmp")`. It runs post-run and only inside the canonical `classfit_outputs/`, so it is unaffected.
- No other glob, scandir or listdir exists apart from `outputs_gate.py:50`, which scans only the canonical directory.

**Index.**
- An existing canonical index makes the wrapper pre-check refuse (`run_classfit_package.sh:11–35`, `index_refusal` "exists") with exit 7, before Python launches.
- The post-run block also refuses on an existing index (`:58–69`).
- If not refused, the index is written by `os.replace` to the canonical path (`:214–219`). It must therefore be moved, as the addendum says.

**Directory states.**
- *Absent:* the gate passes. `Run.__init__` claims and then does `mkdir(parents=True, exist_ok=True)` (`runstate.py:28–38`), and `_write_pair` does the same (`driver.py:76–82`). Both work.
- *Empty real directory:* passes.
- *Containing `.gitkeep` or any entry:* "nonempty", which is INTEGRITY STOP / exit 7. The wrapper pre-check refuses before launch and writes nothing.
- `git mv` of every tracked file out of `classfit_outputs/` (or `git mv classfit_outputs classfit_outputs_attempt1`) leaves the directory absent in the working tree. A fresh checkout never creates an empty directory. Either way it is absent, which passes.

**Hash entries.** No manifest entry or A8 row hashes any path under `classfit_outputs/` or either index name (grep of `classfit_manifest.json`).

**RL-5 oracle re-hash.** The post-run block hashes only the oracle's `manifest.json`, `post_run_index.json` and `outputs/*` (`pinned.py` constants). The move does not affect it.

**Paths inside the moved index.** The moved index's `output_sha256` keys still read `classfit_outputs/…`. These are pre-move paths, as the adopted attempt-1 note says ✓. I confirm the wording fix.

## (e) Single-attempt rules

**v1.3.**
- Quoting #39 (L357): "There are no automatic retries, parameter substitutions or post-result tolerance changes."
- C8.5 (L1245): "No automatic retries, parameter substitutions or post-result tolerance changes."
- The no-rerun clauses are tied to stops: "PIPELINE INVALID (P0), exit 7, no fit, no rerun" (L866), and the C7.1 item 1 conditions "stop the package, with no rerun" (L1088).
- v1.3 forbids outcome-dependent repetition and automatic retries. A PREFLIGHT FAILED refusal that happened before any study computation is none of the C7.1 item 1 stop conditions, produced no outcome, and is not an automatic retry.
- v1.3 also requires that no discretionary choice is made after outputs are inspected (C9.5, L211 and L554). Attempt 1 produced no output that could be inspected.

**Application v1** (`c726f37f`): "Exactly one attempt. No reruns, retries, pilots or partial reruns, whatever the outcome, including an INTEGRITY STOP or PIPELINE INVALID."
- Literally, attempt 1 *was* the one attempt. So attempt 2 needs the Lead's amendment, and RL-14 supplies it under the same standing approval.
- The reading is sound because:
  - no study quantity existed;
  - the refusal came from an administrative field that the Lead's own instruction left out;
  - the addendum caps the total at two, with no attempt 3 whatever the outcome.
- The application's header conditions include "Aidan is to be informed". Attempt 1 and RL-14 should be reported to him (C4).

## 6. Conditions

- **C1.** Before the attempt-2 launch, check read-only that there is no `classfit_outputs` at all (no directory, no `.gitkeep`, no symlink) and no `classfit_post_run_index.json`, for example `test ! -e … && test ! -L …`. Otherwise the wrapper refuses with exit 7. Under "no attempt 3", that refusal would end the experiment. The cleanest move is `git mv classfit_outputs classfit_outputs_attempt1`.
- **C2.** Re-verify the shas of all **five** attempt-1 files after the move. The addendum lists three; add `run.log` `ff948daf…` and `stop_kind.json` `7693b8d3…`.
- **C3.** The status value must be exactly `"FILED"`, and the seal diff should quote `preflight.py:219` as a deny-list. The addendum should also state that it amends application v1's allowed-field list (status, plus the `review_records` and `seal_timestamp` already used at the first seal) and its "Exactly one attempt" clause. Application v1 itself stays unchanged and still passes `check_application_hash`.
- **C4.** Tell Aidan about attempt 1 and RL-14, as the application's standing-approval conditions require. I can't send that; the parent or Lead should.
