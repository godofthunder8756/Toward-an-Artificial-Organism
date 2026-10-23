<!-- CURSOR_AGENT_PR_BODY_BEGIN -->
## Status

Phase 1 only. The package is implemented and the manifest is a draft. **Nothing was executed or sealed.** No stage S0–S8 was run, no pilot or smoke run was run, no fit was run on the declared data, and no checkpoint or weight file was opened. Allowed checks were `python -m py_compile`, import of the modules, hashing, and `python -m ckappa_classfit.static_checks` on hand-made fixtures that are not the declared systems and not the drawn arrays.

`classfit_manifest.json` has `sealed: false`, `seal_status: UNSEALED`, and `standing_approval_application.status: PENDING` with path and sha256 null. Preflight refuses to continue unless `sealed` is true and an application sha256 is filed.

## Starting point

- Starting SHA: `c5786583d25191157bd74f6d085caacb6f224110` on `cursor/ckappa-oracle-package-v1`
- Branch: `cursor/ckappa-classfit-synthetic-v1-4df8`
- Base: `cursor/ckappa-oracle-package-v1`
- Implementation commit (module bytes): `315d9da9f7de10120374ea7b11c912e1b9f9c8a0`
- Annex commit: `b4c035025f039f16efb3a2493a0fa40531cfe45d`
- Head: `b4c035025f039f16efb3a2493a0fa40531cfe45d`

The diff against the base is additive. No sealed oracle artifact, including PR #13 outputs and code, was modified.

## Governing files

All five were absent from the repo. They were committed byte-identical under `review/ckappa_classfit/` and re-hashed after commit.

| File | sha256 | Match |
|---|---|---|
| `review/ckappa_classfit/ckappa_classfit_synthetic_scope_record_v1_3.md` | `a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318` | yes |
| `review/ckappa_classfit/ckappa_classfit_implementation_annex_v1.md` | `8614bf114b127f4bdab516c0e933c23c84d1cd5f4d0ef34837d5cb0ad453d3a8` | yes |
| `review/ckappa_classfit/astra_consult39_response.txt` | `e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482` | yes |
| `review/ckappa_classfit/astra_consult38_response.txt` | `87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5` | yes |
| `review/ckappa_classfit/astra_consult37_response.txt` | `ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2` | yes |

Precedence recorded in the manifest: #39 raw > #38 > #37 > v1.3 > annex v2. Annex v2 supersedes annex v1 by name. Annex v1 is retained byte-identical.

v1.3 names the annex at the review root. The copies live under `review/ckappa_classfit/`. The v1.3 bytes were not edited. See CI-GOVERNING-PATH.

## What was added

- `ckappa_classfit/`: stages S0–S8 for all seven systems, plain separately fitted four-class full (3×8) and fixed-κ maps, accounting, rank bands, and the #38 tolerances.
- `run_classfit_package.sh`: 1 CPU, no GPU, `RLIMIT_AS` 4,000,000,000 B, hard kill at most 595 s from `CKAPPA_CLASSFIT_T0`, writing only `classfit_outputs/` and `classfit_post_run_index.json`.
- `classfit_manifest.json`: draft, unsealed.
- `review/ckappa_classfit/ckappa_classfit_implementation_annex_v2.md`: cites v1.3 by the full sha256 above, supersedes annex v1 by name, and fills the A8 fields. The numeric B0 byte count is **not** established (CR-4). B0 is a static argument only. No import was measured.

Reused arrays are loaded at runtime from the committed `outputs/drawn_arrays.npz` through a read allow-list, with per-array raw-byte sha256 checks. They are not regenerated. This draft did not open that file.

Caps in code: `SCHEDULED_FLOAT` 3,443,968; `DECLARED_N_O1` 272; at most 541 SVDs; 688,128 edits; 16,128 mode-indexed loss records. Skip precedence: prior stop, then whole-system inadmissibility, then prefix void, then unavailable map. Cap-limited work is incomplete. No retries. No hard-coded phase string in outputs.

## sha256 of every new file

```
d62a51c78144ca1bcfaff7db4f148b245deea34f42858b1c0f198a6d01f87ea0  ckappa_classfit/__init__.py
f03238fbb9a311f1afc7476308e4cba80a44d56b60ecfc8446f450a9a05b51c2  ckappa_classfit/__main__.py
91f22bdba716d57827cdb7580488c8544f46c88ad650dd9c5398e06a835f257f  ckappa_classfit/accounting.py
90b5fd26019f80d200ff94a1a73313d69fe7214693b24dd94dd8dc2759adbc29  ckappa_classfit/aggregate.py
9af98b49ab048be0595b71a801e92b03d9b2f2ce5d75e75a450c6343f8e571a4  ckappa_classfit/arrays.py
115df4f03c9e76e3213bc543190287e3ac140601a11efcab4eaed6467036d219  ckappa_classfit/classes.py
133ab38e29d16dcc0238082b4763224fb6c1bc46ec5e16a23e8ac0384d3f32b7  ckappa_classfit/construction.py
35160ec67a3e5d9db6b5d9c00ad7a51249ed4b9916fb5edcf6b838113d848025  ckappa_classfit/driver.py
f87684fc58d8cfe05cf7e33bd6f6497e624b32e102902454ff1f68580f0eb57a  ckappa_classfit/evaluate.py
39096fe4528b21d7a2b2320b1bb32f561b7f5eee8ef6cac613a2438cd4a82b34  ckappa_classfit/fits.py
82f79eafffe96248282f5051fcae7b9c64e1e009681153e1063eb1caa1878e18  ckappa_classfit/gate.py
2486b03257678cf4161d03d1fd0327498373d98ae9df636af92c2404b606c7dc  ckappa_classfit/inputs.py
8db5e1e5f06b1cc61844768c44b0133510968f397584cdaae147e8d04c9f917f  ckappa_classfit/o1o2.py
02a04cc8345e8252cea1400b78a8e2bbc117d62bbb05b65cedabaeba8d4090e4  ckappa_classfit/p0.py
f36a4c472758d73e92750816d9184ad7c27092005577daa13089dc89f304c80b  ckappa_classfit/pinned.py
74fa96eca38915a45ec388722ca523454ee54a252edc5f29211ece2a92590d86  ckappa_classfit/preflight.py
c7062b4647fa663262a4679ea6eab57399b09ba9990ab0a6d529969f0fcae870  ckappa_classfit/rankcats.py
7e05faaf3cd7e1a8e74aab112ad90faa9af13896be1f56ab106118dbc79fe122  ckappa_classfit/records.py
417e926f33caa3da67afd39f924d0f55e6391dca77a4f07f8798c8d2d5d09d72  ckappa_classfit/report.py
9b1bcc8e4b40b36fadf8c3e5bfa2c6cf9c6e789c7196c7975a74fd675e8e29cc  ckappa_classfit/runstate.py
778304aca18b59b95f62a32e8131786998ec082a4ee341c85a64f064a8269b49  ckappa_classfit/schedule.py
04cb4ddad60400e9bbc3b85233085f0b76d293ca780e7c646782a6a6d54e6cc7  ckappa_classfit/static_checks.py
535931b7981ec7611dcb6688e72134ed6433fb3de1523e73d2fd781029f7b71c  classfit_manifest.json
ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2  review/ckappa_classfit/astra_consult37_response.txt
87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5  review/ckappa_classfit/astra_consult38_response.txt
e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482  review/ckappa_classfit/astra_consult39_response.txt
8614bf114b127f4bdab516c0e933c23c84d1cd5f4d0ef34837d5cb0ad453d3a8  review/ckappa_classfit/ckappa_classfit_implementation_annex_v1.md
5d6daf06fea3466ff2fc1eebf73414f12c47daeccfe06095ec7a3efb64907262  review/ckappa_classfit/ckappa_classfit_implementation_annex_v2.md
a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318  review/ckappa_classfit/ckappa_classfit_synthetic_scope_record_v1_3.md
d14b84c151f257fd3162a682fee66b36fc115dcb635db24db694f83f40575a4d  run_classfit_package.sh
```

## Open conformance items

v1.3 CR-1..CR-5 remain open:

- **CR-1.** Guard consistency stops only when the actual belief is valid and an actual-recovery predictor is invalid. The reverse is recorded and does not stop.
- **CR-2.** The SYS-NC1 refit uses the inherited float `P_a` accumulation. The RMS rule uses exact-law `P_a` converted once.
- **CR-3.** D6 diagnostic matrix residuals are 6 cells, one per fold. The residual is the max of the B and A residuals. Diagnostic only.
- **CR-4.** The numeric B0 byte count is not established. Annex v2 gives a static argument only and does not measure an import. The feasibility condition is not established.
- **CR-5.** Output paths avoid the sealed oracle artifacts.

Literal readings recorded rather than resolved by a design choice:

- **CI-ACCOUNTING-ATTRIBUTION.** The 272 exact calls and 1,536 O2 float calls are attributed to SYS-O6 because they are not divisible by 7.
- **CI-B3-SHORT-STACK.** A formed stack with fewer than three singular values is `PASS`.
- **CI-NC-ONE-VOID.** Any matched invalid baseline makes an NC system inadmissible, so the ≥5-void clause adds no further case.
- **CI-LIM-SIGNS.** Declared signs are stored. A mismatch is not an extra integrity stop.
- **CI-LIM-BASELINE-BOUNDARY.** A baseline with `|μ_x| = t` gets branch sign 0 and is not a separate stop.
- **CI-JOINT-PREMISE-TIMING.** SYS-PC global B and A identities share the joint rank premise and are checked after both fits of the fold.
- **CI-EMPTY-FIT-CATEGORY.** An empty fit design is `SKIPPED_UNAVAILABLE_MAP`.
- **CI-LOWER-RESIDUAL.** Lower rank stores a residual with `n_tested` 0 and does not stop.
- **CI-PARTIAL-MASK.** If any of the four maps is empty or unresolved, neither fit type's comparison is formed.
- **CI-BASELINE-TOLERANCE.** True-chart baseline versus the O1 forecast stores max abs and has no declared pass/fail threshold.
- **CI-EXIT-CODES.** P0, normalization, and a guard inconsistency use exit 7 with kind PIPELINE INVALID. O1/O2 and the other control-identity failures use exit 2. Integrity conditions use exit 7. An unsealed manifest is exit 5.
- **CI-SCHEDULE-KEY.** Inherited `scheduled_float_propagations` stays 788480. The package maximum is `classfit_scheduled_float_propagations` 3443968.
- **CI-T0-ENV.** Clock variable is `CKAPPA_CLASSFIT_T0`.
- **CI-MANIFEST-PHASE.** No `phase` key. `seal_status` is present.
- **CI-HEADROOM-MET-LABEL.** The met label is MET for both ALL and MARG.
- **CI-NC1-FINITE-EQ-CELLS.** SYS-NC1 has 72 descriptive zero-gain cells and no separate finite equality cell.
- **CI-D6-A-INSIDE-ONE-CELL.** Same as CR-3.
- **CI-UNFORMED-VS-ZERO.** `n_scoreable` null means unformed. `n_scoreable` 0 with null losses means a zero denominator.
- **CI-LAW-MASS-BOTH-MODES.** Both modes store the cell's law mass. The unweighted denominator is the occurrence count.
- **CI-GOVERNING-PATH.** Copies live under `review/ckappa_classfit/`.
- **CI-ATTEMPTED-DETAIL.** Attempted calls also store valid-finite, guard-invalid, ValueError, and non-finite subcounts.
- **CI-REPRESENTATIVE-MU.** Representative `μ > 0` is stored and is not an extra stop.
- **CI-LABEL-INADMISSIBLE.** An inadmissible system has no coverage rows, so the coverage label does not fire.
- **CI-RESULTS-WRITE-STAGE.** A5 places `results.json` at S7 and A6 places the final file at S8. It is written once, after S7, during S8.
- **CI-APPLICATION-PENDING.** Application path and sha256 are null.
- **CI-MANIFEST-ITEMS-SHAPE.** `items` uses names `governing`, `inputs`, and `implementation` rather than numeric item ids.
- **CI-GLOBAL-AGGREGATES.** Orbit-level aggregates are not stored. The 336 pooled rows are.
- **CI-SINGLE-PREFIX.** Single-prefix fits are absent.
- **CI-CANCELLATION-DIAGNOSTIC.** Orbit cancellation sums do not stop.
- **CI-MU-RECOVERY-PREMISE.** Fixed-κ recovery uses the μ rank category.

## Explicit statement

No stage was executed. The manifest was not sealed. This pull request stays a draft.

<!-- CURSOR_AGENT_PR_BODY_END -->

<div><a href="https://cursor.com/agents/bc-11c1f9eb-41a4-5882-b6d5-af1e9b0c4df8?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-11c1f9eb-41a4-5882-b6d5-af1e9b0c4df8&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

