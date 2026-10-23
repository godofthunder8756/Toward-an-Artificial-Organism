# C-κ class-fit package: implementation annex v5

**Binds to:** `ckappa_classfit_synthetic_scope_record_v1_3.md`, sha256 `a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`.

**Supersedes:** `ckappa_classfit_implementation_annex_v4.md` by name. Annex v4 sha256 `84620dc7e8b84df65ecb81db9689f0170dbb354b183ecd955d7a5b139284b984`. The v4 file is retained byte-identical and is not edited. Annex v3 sha256 `435453e0917d1d4d3f2c50c4cc8dc469d6487147f8dd987fd53eb877ac5cb8bd`, annex v2 sha256 `5d6daf06fea3466ff2fc1eebf73414f12c47daeccfe06095ec7a3efb64907262`, and annex v1 sha256 `8614bf114b127f4bdab516c0e933c23c84d1cd5f4d0ef34837d5cb0ad453d3a8` stay byte-identical.

**Status: IMPLEMENTATION ANNEX v5. NOT SEALED. NO STAGE S0–S8 WAS RUN.**

**Implementation commit:** `a18c8650524a70a57ed500ee92ba0393ad9b9bfa`. That commit contains the module bytes hashed in A8. This annex is added in a later commit that does not change those bytes. This file does not contain its own sha256. The unsealed draft manifest records it.

**RL-13.** Lead rulings on the Delegate fix delta `review/ckappa_classfit/ckappa_pr14_fix_delta_RD_5f85.md`, sha256 `0303e3b159b92b570ccf21715bd2963a2f0a7bcffa50456fc5197b213f9e3d0d`. That file is committed byte-identical. RL-6 through RL-12 remain the file `review/ckappa_classfit/ckappa_classfit_rulings_RL6_RL12.md`, sha256 `fc402c3db3bf9657cf0a1bb30a49c3022667f9827f2af8dfdaff972331a7883f`, which is the same bytes as `ckappa_classfit_rulings_RL6_RL12_7da7.md`.

**Governing text.** Astra #39 raw (`e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482`) > #38 (`87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5`) > #37 (`ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2`) > v1.3 (`a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318`) > this annex.
- Where this annex and annex v4 conflict, this annex governs, because it supersedes v4 by name.
- Where this annex and v1.3 conflict, v1.3 governs.
- There is no fallback from this annex to annex v4 or any earlier annex. A missing annex v5 entry is INTEGRITY STOP.

**Claim ceiling.** E38-15, unchanged. This annex establishes no result.

**What was executed.** `py_compile` of the package modules with bytecode written outside the tree, `bash -n` on `run_classfit_package.sh`, and `tests/test_phi_count.py`. That test calls `Run.phi` with a substituted `phi_float`, plus `b3_status` and `rank_category_from_ratios`, on temporary directories. It does not call `driver.main`, the wrapper, `preflight`, any `stage_s0` through `stage_s8`, or `static_checks`. The import set did not change, so B0 was not remeasured. No declared data were fit or evaluated. `classfit_manifest.json` is not sealed.

---

## RL-13

### 1. NB-1, the same finding as CNA N-1

v1.3 C8.4 counts a float propagation when it starts. In `Run.phi` the order is exactly:

1. the overrun check (`float_count >= SCHEDULED_FLOAT`);
2. `float_count += 1`;
3. `phi_float`.

The soft-deadline check stays before those three steps. If the overrun check stops the run, `float_count` is not incremented and `phi_float` is not called. If `phi_float` then raises `ValueError`, the increment from step 2 remains. The timing sample is still recorded only after a successful return.

`attempted_totals` keeps `value_error` as its own subtotal. That subtotal is not removed from the exact or float ATTEMPTED sums, and it is not a fifth run counter. The four sums `exact`, `float`, `svd`, and `other` must equal `run.exact_count`, `run.float_count`, `run.svd_count`, and 0. A started call that raises `ValueError` is therefore in both the counter and the ATTEMPTED total.

`tests/test_phi_count.py` covers both paths. A substituted `phi_float` that raises `ValueError("observation has predictive probability 0")` leaves `float_count` one higher, records no timing sample, and after the `value_error` ledger row the ATTEMPTED total equals the counters. A call made when `float_count` is already `SCHEDULED_FLOAT` raises INTEGRITY STOP, exit 7, does not change `float_count`, and does not call `phi_float`.

### 2. N-2

The pre-comparison write of `stage_S4_P0.json` uses status `DOMAINS_RECORDED`. That write is not a verdict. `PASS` and `FAIL` are written only after a comparison.

### 3. CNA note 1

In `b3_status`, a formed stack with fewer than three singular values is INTEGRITY STOP, exit 7, and that test runs before the `ZERO` return. A formed stack of at least three singular values whose first value is 0 still returns `ZERO`. An unformed stack stays `NOT_FORMED`.

### 4. N-6

`rank_category_from_ratios` no longer raises `ValueError` when a nonempty design has no `sigma_1`. That case is INTEGRITY STOP, exit 7, diagnosis `PIPELINE INVALID (rank)`.

### 5. RL-6 scoping, M-6, and the RL-7 reading

RL-6's sentence "One void alone never makes a system inadmissible" applies to SYS-NC1 only. For SYS-NC2 and SYS-NC3, a prefix void is an invalid matched baseline and the system is RESTRICTED COMPARATOR NOT ADMISSIBLE. That is v1.3 C4.4.R (a matched baseline with `p < 10^{-6}`) and C7.1 item 5 (matched baseline invalid). The code in `nc_system_admissible` already follows this split. This annex states the scoping as the Lead ruling.

M-6 is **ACCEPT**. Coverage remains before rank, which is the literal v1.3 C7.1 order. No code change.

The RL-7 reading is confirmed against the inherited oracle: `ckappa_oracle/outcomes.py` lines 12–13 give ALL `met_label` `MET` and MARG `met_label` `AVAILABLE`. ALL keeps `MET`. MARG uses `AVAILABLE`.

### 6. N-7

`review/ckappa_classfit/ckappa_classfit_rulings_RL6_RL12.md` (`fc402c3d…`) and `review/ckappa_classfit/ckappa_pr14_fix_delta_RD_5f85.md` (`0303e3b1…`) are in the manifest governing list and in `REQUIRED_GOVERNING`. Annex v5 is required. Its sha is not hardcoded. S0 requires the path, requires the file, and compares the manifest sha with the file bytes. There is no fallback to annex v4.

---

## Per-item mapping

Implementation commit for every code row: `a18c8650524a70a57ed500ee92ba0393ad9b9bfa`.

| Item | Commit | File:line | What changed |
|---|---|---|---|
| NB-1 order | `a18c8650524a70a57ed500ee92ba0393ad9b9bfa` | `ckappa_classfit/runstate.py:152` | overrun check, then `float_count += 1`, then `phi_float` |
| NB-1 value_error partition | `a18c8650524a70a57ed500ee92ba0393ad9b9bfa` | `ckappa_classfit/accounting.py:105`, `driver.py:185` | `value_error` stays inside the ATTEMPTED sums |
| NB-1 tests | `a18c8650524a70a57ed500ee92ba0393ad9b9bfa` | `tests/test_phi_count.py:29`, `:64` | raising `phi_float`, and overrun before the increment |
| N-2 | `a18c8650524a70a57ed500ee92ba0393ad9b9bfa` | `ckappa_classfit/p0.py:89` | status `DOMAINS_RECORDED` before any verdict |
| CNA note 1 | `a18c8650524a70a57ed500ee92ba0393ad9b9bfa` | `ckappa_classfit/rankcats.py:68` | short stack before `ZERO`; INTEGRITY STOP exit 7 |
| N-6 | `a18c8650524a70a57ed500ee92ba0393ad9b9bfa` | `ckappa_classfit/rankcats.py:32` | missing `sigma_1` is INTEGRITY STOP exit 7 |
| RL-6 scoping | this annex | RL-13 item 5 | SYS-NC1 only; NC2/NC3 one void is not admissible |
| M-6 ACCEPT | this annex | RL-13 item 5 | no code change |
| RL-7 confirmation | this annex | RL-13 item 5 | `outcomes.py:12–13` |
| N-7 | `a18c8650524a70a57ed500ee92ba0393ad9b9bfa` and the manifest commit | `ckappa_classfit/preflight.py:226`, `driver.py:122` | annex v5 required; rulings and delta are governing files |

`static_checks.py` now expects `ZERO` from a formed stack of three zeros, so a two-value stack is not described as `ZERO`. That file was not executed.

---

## A8. Module file list and per-file sha256

Bytes of implementation commit `a18c8650524a70a57ed500ee92ba0393ad9b9bfa`. The six `ckappa_oracle` rows are inherited sealed bytes. This commit does not change them. `tests/test_phi_count.py` is not an implementation module.

| Path | sha256 |
|---|---|
| `ckappa_classfit/__init__.py` | `d62a51c78144ca1bcfaff7db4f148b245deea34f42858b1c0f198a6d01f87ea0` |
| `ckappa_classfit/__main__.py` | `7b1660a820b6ec7bbd7a98af3cb510f5d3e517caabb9f30de2b419cd37337b5a` |
| `ckappa_classfit/accounting.py` | `1fdecdd11a5f2053c3fca53e7e24d343cb94ed6d43e6a9a6189e0c058eb2fc7a` |
| `ckappa_classfit/aggregate.py` | `c141ea445e6ddcbc1fd8d65a359bf1830144a8795594f7b68998a02d97cce9b8` |
| `ckappa_classfit/arrays.py` | `9af98b49ab048be0595b71a801e92b03d9b2f2ce5d75e75a450c6343f8e571a4` |
| `ckappa_classfit/classes.py` | `115df4f03c9e76e3213bc543190287e3ac140601a11efcab4eaed6467036d219` |
| `ckappa_classfit/construction.py` | `a7cd3606c3f15cc311928282f9563e1f5c91e1b9cd473acbcea4680554aa3155` |
| `ckappa_classfit/driver.py` | `f467f5f3aa2a0bc1d77cfd27c590d5e50cbd73dc48142444cc8fcec0f6fcacfd` |
| `ckappa_classfit/evaluate.py` | `e7031c76e8d2f872e7bec730d5450969fce63746cf6ae8eb8da38fa0368119cf` |
| `ckappa_classfit/fits.py` | `bc22bd9d85f9c1ac9ad6790d12b7f318a0dc6f709187cd5bd0beed5131b870da` |
| `ckappa_classfit/gate.py` | `82f79eafffe96248282f5051fcae7b9c64e1e009681153e1063eb1caa1878e18` |
| `ckappa_classfit/inputs.py` | `2486b03257678cf4161d03d1fd0327498373d98ae9df636af92c2404b606c7dc` |
| `ckappa_classfit/o1o2.py` | `8db5e1e5f06b1cc61844768c44b0133510968f397584cdaae147e8d04c9f917f` |
| `ckappa_classfit/outputs_gate.py` | `89832c8b172132328329f378e0fe847cf725353575d4b74bcfe18272ccab6440` |
| `ckappa_classfit/p0.py` | `d6d56e667dfeb91b9e1d5614a882796548455200a065e00ccfaa05a4a1d93c43` |
| `ckappa_classfit/pinned.py` | `91752b443e2278df1e7ea3deb91d2244c4c3381be180f6cd10cc27e32b819de6` |
| `ckappa_classfit/preflight.py` | `de8f532ea67ad0de1f158bd273d1f7e532d4100833ebfb8604c0291e5eaeed31` |
| `ckappa_classfit/rankcats.py` | `90802f23c1438553adb7225963d64487a8aee96d028f4588c92c17370360af2c` |
| `ckappa_classfit/records.py` | `7e05faaf3cd7e1a8e74aab112ad90faa9af13896be1f56ab106118dbc79fe122` |
| `ckappa_classfit/report.py` | `96bf6aeda8239fc03d5f6590d60aeb36534e7e40739a6ae983890377151d0ff2` |
| `ckappa_classfit/runstate.py` | `2432bda7af70a8336f827be35af6ee0263ba7ba693a7f36ff4c8bfa750378e1b` |
| `ckappa_classfit/schedule.py` | `da698d438dc96daabc3fa14065a6fddc15977a3d2551b179dd90cbc34865cd34` |
| `ckappa_classfit/static_checks.py` | `7e70c788b5a986d47dee535666732e24d3427feb92949052200101b1e7c2bae0` |
| `run_classfit_package.sh` | `05eecb2c34596269ed08943b8416132ab16b448af0658402a87f99601c6fbe44` |
| `ckappa_oracle/__init__.py` | `45f848b1c56ba1fe4b5a8a663c706937402ee936a8e414100ea2d16e4b5db718` |
| `ckappa_oracle/geometry.py` | `117e98e959c8134cb0f124bf284488a9ee71bc319b07b21ac9fa489dac7e8ac9` |
| `ckappa_oracle/io.py` | `b1795bcc4f022228da1ef13703c8a0ede2dc96287af25e8e5e314d390fc17802` |
| `ckappa_oracle/linalg_fit.py` | `de6f4034260bbc0ba74c2b6d1bddfbc5fe0bfd3c637ef0b4168e188885fd936a` |
| `ckappa_oracle/pinned.py` | `03c55323d0eb0b14fc463510738109d24e76ee9dc4623ba0e8c396e712363a68` |
| `ckappa_oracle/world.py` | `3d235fca82741e1a2081c7f4eac993b04f59226a3720b6232d06e637803f5aac` |

### B0

The import set is unchanged. No new `ckappa_oracle` module is imported, and no new module was added under `ckappa_classfit/`. B0 was not remeasured. The annex v4 figure stands: VmPeak **60,024 kB = 61,464,576 B**. Plus the package budget 316,737,056 B is **378,201,632 B**, which is within 4,000,000,000 B. VmPeak is the only operand. S0 still remeasures VmPeak and does not reuse 61,464,576 B.

---

## Open items

- The manifest is **UNSEALED**. The standing-approval application is **PENDING**. `path` and `sha256` stay null.
- M-6 is ACCEPT. It is not open.
- NB-1, N-2, CNA note 1, N-6, and N-7 are implemented. They are not open.
- Delegate notes N-3 (TOCTOU between the wrapper pre-check and the in-process claim) and N-5 (the resolve comparison is redundant after the lstat symlink check) were not given a code change by RL-13. They remain notes.
- N-8 stays as RL-8 left it: the label uses the real stop kind, and the diagnosis carries `PIPELINE INVALID (...)`.
- N-9 stays: this annex's sha is not hardcoded. The manifest binds it.
- The earlier Delegate minor notes outside these items are unchanged.
- `static_checks` was not run. No stage was run.
