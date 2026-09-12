<!-- markdownlint-disable-file -->
# Existing evidence audit

Date: 2026-09-09

Status: Complete, with integrity failures and numerical replay limitations recorded

## Scope and preservation requirements

Research-only audit of E0/E1/E2 frozen evidence, source and run hashes, selected replay integrity, raw evaluation Cartesian coverage, seed-level point estimates, metadata, protected acquired state, and historical package-manifest drift. No experiment, training, original-file edits, validation-output replacement, or E3 implementation is permitted.

Only this research document and a bytecode-disabled audit script in this directory were created. Verifier writes were intercepted in memory for known validation destinations only. Original files were hashed before and after execution.

## Questions

* Do the E0 source hash and mechanism checks agree with saved evidence without training?
* Do E1/E2 freeze hashes, run source snapshots, manifests, evaluation key coverage, and selected replays agree?
* Can reported developed and paired history point estimates be recomputed from seed-level raw data?
* Which acquired E2 state remains protected, including replay, target network, and Adam state?
* Does PACKAGE_MANIFEST.json version 0.2 still describe the current tree?

## Evidence and commands

Executed from the workspace root:

```powershell
python -B .copilot-tracking/research/subagents/2026-09-09/audit_existing_evidence.py
```

The script independently completed source, data, mechanism and selected replay checks. Its final strict preservation assertion returned exit code 1 because one pre-existing type-checker cache file's metadata changed while the audit ran. All original file contents had identical before/after hashes; details below. This exit must not be reported as a clean overall pass.

The script calls the original verify_e1.verify and verify_e2.verify functions under `unittest.mock.patch.object(Path, 'write_text', capture)`. The replacement accepts only e1_results/VALIDATION.json and e2_results/VALIDATION.json and stores their JSON in memory. A process audit hook rejects filesystem writes/mutations; training methods and Adam.step are patched to reject calls. No analyzer entry point, experiment runner, optimizer step, retraining, diagnostic rerun, or E3 implementation was executed.

A second, read-only PowerShell command extracted JSON fields from the first command's terminal log, using Get-Content, ConvertFrom-Json and Select-Object. It displayed E1_SELECTED_REPLAYS, E2_SELECTED_REPLAYS and E2_ESTIMATES without rerunning or changing evidence.

The parent reports `python -B -m unittest -v test_e1 test_e2`: all 24 tests pass on Python 3.13.3. This audit did not independently repeat that test suite. Editor diagnostics reported no errors in either new research artifact before execution.

### Runtime provenance

| Runtime | Python | NumPy | Other information |
| --- | --- | --- | --- |
| Fresh audit | 3.13.3 | 2.2.6 | Windows x86-64; Python313 interpreter; scipy-openblas/OpenBLAS 0.3.29, 64-bit integer build; bytecode disabled |
| Saved E0 | 3.12.14 | 2.3.5 | Recorded wall time 47.50932717323303 seconds |
| Saved E1 | 3.12.14 | 2.3.5 | Recorded wall time 235.18303203582764 seconds |
| Saved E2 | 3.12.14 | 2.3.5 | Recorded wall time 324.2709765434265 seconds |

Both Python and NumPy differ. Tiny replay differences are compatible with numerical-stack differences, but the audit does not isolate their exact cause or establish same-stack replay.

## Source-inspection findings

* NEW_AGENT_GUIDE.md read in full. E0 is exploratory; E1/E2 are local freezes, not external preregistrations. Verification is evidence integrity, not evidence of life or consciousness.
* verify_e1.py writes only e1_results/VALIDATION.json after all assertions; verify_e2.py writes e2_results/VALIDATION.json before raising SystemExit on any false check. Both functions must be called under a destination-restricted in-memory Path.write_text patch. Their command-line entry points will not be run.
* E1_FREEZE.json includes ENGINEERING_LOG.md. The current log includes later E2 entries; the resulting hash mismatch was verified and retained as an integrity finding, not repaired.
* E2_FREEZE.json contains seven entries, including its protocol but not analyze_e2.py, verify_e2.py, or diagnose_e2.py. ENGINEERING_LOG.md discloses that E2 analysis/audit scripts were written during the final run, after the protocol gates were frozen.
* E1 run.json records initial and final source hashes and completed status; E2 run.json has one source-hash set and elapsed seconds, but no explicit completion status, timestamps, final source-hash set, or config hash. Completion therefore needs data-coverage evidence, not an invented metadata field.
* Data Viewer is closed. Independently retrieved schemas: E0 episodes 7,104 x 12, E1 evaluation 4,480 x 19, E2 evaluation 9,216 x 20. Samples: E0 first active_steps=600, E1 first stage=pre, E2 first recall=0.041666666666666664.
* e2/model.py retains learned p arrays separately from biomass. Network.load reconstructs target from p, resets Adam and replay, and restores updates. Saved checkpoints support evaluation, not exact mid-training resumption. e2/experiment.py clones the full in-memory network for branches, retaining target, Adam and replay during the original training.

## Preservation results

Before and after inventory: 5,260 original files, 681,989,069 bytes before execution. Exclusions were .copilot-tracking/ and .git/; pre-existing .mypy_cache/ was deliberately included. No files were added or removed in this inventory. The SHA-256 of the sorted path-to-content-hash inventory was identical before and after:

`d48aa41e381cb372e7c121c7d78a2caddc1fe3c4de434888a2a8f43c04a57569`

The strict `(size, mtime_ns, SHA-256)` comparison flagged only .mypy_cache/3.13/@plugins_snapshot.json. Its contents were unchanged, as were all experiment sources, raw data, manifests, checkpoints and saved validation reports. The script itself rejected filesystem mutations; a concurrent cache writer outside that Python process is plausible but not proven. No timestamp was restored and no cache was removed. The failure is retained, not hidden by excluding the file after the result.

| Original validation file | Identical before/after SHA-256 |
| --- | --- |
| e1_results/VALIDATION.json | `0d220c27858bf2aac005e7164b8d837f17f0f8fd48109ed86bb23b5a728a7857` |
| e2_results/VALIDATION.json | `a9e03e02ec5514f76f786a3a295404bb17e194c834041701f2f856488764e982` |

## Freeze, source and run-manifest integrity

### E0

E0 has exploratory run provenance in results/run.json, not an E1/E2-style pre-run freeze. pilot.py SHA-256 equals the saved source hash:

`b5485d28534d7aa18dd85d5784711cfd44754872a60867ea6c64c1996596b358`

pilot.check_mechanisms() returned all five saved checks without training: quality changes neural dynamics; gain disconnection isolates that link; paired rollouts are deterministic; action accounting matches active ticks; repair restores quality while sham consumes the same resources without restoration. The returned list exactly matches the manifest.

### E1

10 of 11 E1_FREEZE.json entries match. The sole mismatch is ENGINEERING_LOG.md:

* Frozen SHA-256: `0e5b072359b3893459ee26028f020fb9676a72a006d1095561d835a66460637a`
* Current SHA-256: `a575168dd92fa05ced72539091656b729d983fb433d706eeec0f31e50c452a27`
* Historical manifest size 1,933 bytes; current size 3,898 bytes
* The current file includes an E2 engineering section after the E1 material. This documents later log growth; the audit has not reconstructed the frozen file or proved that its original byte prefix is identical.

All six E1 module hashes agree with the run's initial and final source hash sets, which also agree with each other. The frozen protocol, analysis, tests and configuration pass their hashes. Configuration values equal e1/frozen_config.json. The run's canonical sorted-JSON config hash recomputes as `1c2f13e75787e71a9927705cfb7e913510a973ed0719e9e6525ca99dc9762a5e`.

E1 run status is completed; engineering_feasibility and external_preregistration are false. The freeze timestamp and run started_utc both say 2026-09-09T19:29:48Z, so this metadata has only same-second ordering resolution. The current log drift invalidates a present-tense claim that every E1-frozen file is unchanged; it does not show that the numerical model changed.

### E2

All seven E2_FREEZE.json entries match: e2/__init__.py, e2/experiment.py, e2/model.py, e1/circuits.py, E2_PROTOCOL.md, test_e2.py and e2/frozen_config.json. All four module hashes in e2_results/run.json match current files. Configuration values equal the frozen configuration; variants are plastic, static and shuffled; exploratory is false.

The E2 model hash is `9885e5bb58e65614e33155e562422f926d1e014e9781679694009e29ce6822a9`; runner hash is `837fa5a0e68b879aee8e694ca4447be37bcfe46249655108e8e5d8d0fbc60823`. The shared circuit hash is `d8ddf0b61194793d8e380f1c4d23824d362eab747eddacfa15a8407e0dd7a850`. E1 runner hash is `3c52790fcb8c1d4c56e0a89f5ec5277a57b9225272a7d3228e726ca965395228`.

Neither final result directory contains a separate source/ snapshot directory. Their matching source manifests refer to the shared workspace files. E2 lacks run start/end timestamps, explicit status, final source hashes, and a config checksum. Its freeze JSON also lacks a timestamp. Current hash equality and complete output coverage are verified; historical timing is documented by project records, not independently timestamp-authenticated. Post-freeze analysis/audit/diagnostic scripts are not members of its seven-file freeze.

## Full raw-table key coverage and accounting

Expected keys were constructed from the protocol's specific levels, not inferred from whatever levels happened to be present in the CSV.

| Table | Expected key set | Result |
| --- | --- | --- |
| E0 episodes | 3 scenarios x 6 neural conditions x 6 seeds x 64 episodes, plus 3 scenarios x reflex seed 0 x 64 episodes | 7,104 rows and unique keys; zero missing, unexpected or duplicate keys |
| E1 evaluation | seeds 100-119 x 4 named variants x 7 named stages x worlds 0-7 | 4,480 rows and unique keys; zero missing, unexpected or duplicate keys |
| E2 evaluation | seeds 200-215 x plastic/static/shuffled x histories 0/1 x 16 named stages x worlds 0-5 | 9,216 rows and unique keys; zero missing, unexpected or duplicate keys |
| E1 budgets | seeds 100-119 x 4 variants x pre/acquisition/dependency/rescue/sham/lost_usefulness | 480 complete unique keys |
| E1 assays | seeds 100-119 | 20 complete unique keys |
| E2 saved diagnostics | seeds 200-215 x 3 variants x histories 0/1 | 96 complete unique keys |

E1 stages: pre, acute, acquired, dependency, rescue, sham, lost_usefulness. E2 stages: initial, developed, lesion_all, lesion_0, lesion_1, acute_normal, normal, acute_rescue, rescue, acute_sham, sham, acute_lost, lost, acute_swap, swap, frozen_weights.

Top-level E1 and E2 evaluation tables equal the multisets of all corresponding per-seed tables. E1 top-level budgets likewise equal their per-seed tables. E1 world_seed/mode checks produced zero errors. E1 active/planned trial and collection/recall denominator identities produced zero errors; every planned evaluation horizon is 128. E2 unconditional-versus-active collection identities and recall <= active_fraction <= 1 produced zero errors.

E1 planned maintenance slots sum to 675,840, actual slots to 617,761. These are recomputed from raw budgets, not a rerun of maintenance learning. E2's original verifier counted 1,420,800 training rows, equal to 16 x 3 x 2 x (4,000 + 6 x 1,800). Maximum E2 training ledger error and maximum evaluation ledger error were both `1.1102230246251565e-16`, below its `1e-12` threshold. The training-row check is a total-count check, not a new full Cartesian training-log proof.

All three raw E1 file hashes equal the saved validation values:

* evaluation.csv: `7706e3a3fe59956459399e29c20bc09689c474a67195f40a9b72dd2bef1a17a8`
* assays.csv: `b7dbdfae4e7da36fbbe577193d2f439401e8853b0a1c650eb1a71d2f7afd5315`
* budgets.csv: `b5de14beefc87e723a0b6e38f9da1a0993f1ee59f6f59d075084115e74b731c6`

E2's saved validation report does not provide comparable raw CSV/checkpoint hashes. Current internal consistency and audit-time non-mutation are not retrospective authentication of every E2 output byte.

## Seed-level recomputation of reported estimates

The audit independently aggregated raw rows using the exact formulas in analyze_e1.py and analyze_e2.py without calling their writing functions. E1 worlds were averaged within developmental seed; E2 architecture estimates average both histories and worlds within initial seed. Histories are paired counterfactuals, not additional independent agents.

### E0 recomputation

All 21 scenario/condition mean lifetimes and saved seed vectors match exactly. Normal-condition means: evolved 600; telemetry-clamped 66.26041666666667; reset-hidden 421.5625; gain-disconnected 600; sham-repair 94.734375; untrained 69.63020833333333; reflex 600. The reflex ceiling remains a simpler explanation for ordinary survival performance. No evolution or selection was rerun.

### E1 recomputation

All 224 saved condition/metric means and their seed vectors match exactly. All 20 within-variant primary contrast means and seed vectors also match exactly; maximum difference was 0.0. Examples for neural_q, as fractions:

| Stage | Active precursor rate | Recall per planned trial | Completion |
| --- | ---: | ---: | ---: |
| pre | 0.000000000000 | 1.000000000000 | 1.00000 |
| acute | 0.066650390625 | 0.453710937500 | 0.83125 |
| acquired | 0.266943359375 | 0.998339843750 | 1.00000 |
| dependency | 0.241943359375 | 0.988769531250 | 1.00000 |
| rescue | 0.000000000000 | 1.000000000000 | 1.00000 |
| lost_usefulness | 0.037837040450 | 0.318847656250 | 0.90000 |

Primary neural contrast means: acquired minus pre precursor 0.266943359375; acquired minus acute function 0.54462890625; dependency minus rescue precursor 0.241943359375; dependency minus sham precursor 0.1713604939616015; dependency minus lost-usefulness precursor 0.2041063189252729.

Recomputed memory assay means: naive 0.259521484375; intact 1; lesion 0.2501953125; restored 1; degraded 0.25517578125. Every seed meets intact >= 0.85 and lesion <= 0.35. These are summaries of saved assay measurements, not newly executed recall assays.

### E2 developed estimates and paired histories

All 240 saved stage/metric means and seed vectors match exactly, as do all 24 within-variant contrasts and both architecture contrasts. Maximum mean and seed-vector difference was 0.0.

| Variant | Developed recall/planned | Active fraction | Completion |
| --- | ---: | ---: | ---: |
| plastic | 0.7092447916666667 | 0.8392144097222223 | 0.4166666666666667 |
| static | 0.8734375 | 0.9636935763888889 | 0.8958333333333333 |
| shuffled | 0.6523003472222222 | 0.7940755208333333 | 0.328125 |

| Contrast | Recomputed mean, fraction |
| --- | ---: |
| plastic minus static developed recall | -0.16419270833333333 |
| plastic minus shuffled developed recall | 0.05694444444444445 |
| plastic development minus initial recall | 0.5755208333333333 |
| plastic paired history priority D | 0.052821180555555555 |
| plastic paired history dependence L | 0.15342881944444442 |
| static D | -0.0495225694444444 |
| static L | 0.0721571180555556 |
| shuffled D | 0.0109375 |
| shuffled L | 0.172634548611111 |
| plastic swap recovery | 0.021462673611111073 |
| plastic normal minus lost collection | 0.09001736111111111 |
| plastic lost collection | 0 |
| plastic normal minus rescue collection | -0.04769965277777777 |
| plastic normal minus frozen recall | 0.0230685763888889 |

For each seed, D = ((A_rate - B_rate)_history0 - (A_rate - B_rate)_history1)/2 at developed stage. L = ((recall_lesion1 - recall_lesion0)_history0 - (recall_lesion1 - recall_lesion0)_history1)/2. Each history-level term averages six worlds; the final point estimate averages 16 seed differences. Matching the saved seed vectors checks the pairing itself rather than only the final means.

The original gate pattern is retained: functional development FAIL, selective value of growth FAIL, history priority PASS, history dependence PASS, viable relinquishment PASS, chemistry swap recovery FAIL. Bootstrap intervals and gates requiring those intervals were read from saved outputs, not independently bootstrapped here. No thresholds changed.

The 96 saved exploratory diagnostic rows recompute DIAGNOSTICS.json exactly. Every variant's snapshot, restored, and paired-history-biomass recall mean is 1.0. Depleted snapshot means are plastic 0.49969482421875, static 0.5032958984375, shuffled 0.501953125. Shuffled-weight recall means are respectively 0.61761474609375, 0.540771484375 and 0.56488037109375. These post-freeze assays were not rerun and are not additional confirmatory gates.

## Original verifier outcomes and bounded replay differences

| Check | Actual outcome |
| --- | --- |
| verify_e1.verify | AssertionError: Frozen protocol/code changed; zero replay calls before exit; no validation write attempted |
| verify_e2.verify | Source, evaluation, seed, training and ledger checks true; saved_checkpoint_replays false; SystemExit: Validation failed |
| Intercepted validation writes | Exactly one: E2's failing validation JSON captured in memory; neither original validation file written |

E1's failure was not bypassed by changing its freeze or verifier. A separately labelled replay supplement evaluated the original 28 seed-100/world-0 variant-stage combinations. E2's verifier executed its original 42 seed-200/world-0 variant-history-stage combinations. No original comparison was made tolerant.

| Selected replay | Cases exactly equal | Rows | Differing numeric cells | Largest absolute difference | Discrete mismatches | Length mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E0 evolved, saved seed-0/episode-0 trace | 1 / 1 | 600 | 0 | 0 | 0 | 0 |
| E1, all 4 variants x 7 stages | 0 / 28 | 3,433 | 370 | 1.1102230246251565e-16 | 0 | 0 |
| E2, all 3 variants x 2 histories x 7 checkpoint stages | 12 / 42 | 10,080 | 4,044 | 7.105427357601002e-15 | 0 | 0 |

E2 checkpoint stages were developed, normal, rescue, sham, lost, swap and frozen_weights. No other seed or world replay is implied. The E0 trace was generated by a saved-controller rollout with the original evaluation conditions, not training.

For a separate diagnostic bound, every compared numeric cell satisfied `abs(replay - saved) <= 1e-12 + 1e-12 * abs(saved)`. This is an audit-only descriptive bound, not a replacement frozen acceptance criterion. Discrete action, correctness, trial, active/dead and other relevant event fields were required to remain exact. Stored energy levels were also exactly equal for these samples (E1 energy_before/energy_after and E2 energy); net_energy and other continuous activity/material/ledger fields did have small differences.

E1 differing fields and counts: neural_activity 258; external_repair 32; q_before/q_used/q_after 21 each; precursor_used 9; net_energy 8. Example, neural_q/pre at zero-based trial 1: saved neural_activity 0.6999667495350334 versus replay 0.6999667495350332.

E2 differing fields: balance_error, consumed, demand_a, demand_b, external, mass_a, mass_added, mass_b, mass_lost, net_energy, store_a and store_b. Example, plastic/history0/developed at trial 0: saved demand_a 0.09009825386832525 versus replay 0.09009825386832523. At trial 3, mass_b was 18.537787551329654 versus 18.53778755132965.

The saved reports claim 28 and 42 exact replays in their original context. That historical claim is not reproduced exactly under this audit's different numerical stack. Behavioral event agreement and bounded floating-point differences are supported for the selected samples; universal cross-platform bitwise reproducibility is not.

## E2 protected acquired-state inventory

Sources: e2/model.py Network.__init__, Network.forward, Network.add_learn, Network.save/load and Body.update; e2/experiment.py rollout, evaluate and run_one; e1/circuits.py Adam; diagnose_e2.py.

| State or mechanism | Role and protection | Persistence/checkpoint behavior |
| --- | --- | --- |
| p['u'], p['w'], p['b'], p['v'] | Acquired input/recurrent/bias/readout parameters; actual computation is biomass-gated, but the signed values are not erased by material loss | Protected host arrays survive depletion; saved as p_u/p_w/p_b/p_v |
| target | Protected individual-specific copy of all p arrays, updated every 30 learning updates; bootstraps resource Q targets | Cloned into original branches; not serialized; load replaces it with a fresh copy of saved p |
| Adam m, v, t | Protected gradient-history moments and update count; optimizer is externally implemented, not reconstructed by biomass | Cloned in original branches; not serialized; load creates zero moments and t=0 |
| Replay buf | Up to 512 individual-specific transitions; contains cue-bearing x, prior mass z, action/reward, next inputs/mass, terminal flag, attempted gate, success and propensity | Retained through development and cloned into branches; not serialized; empty after load |
| cursor and updates | Replay insertion/scheduling and target-update timing | cursor resets to 0 on load; updates is serialized and restored |
| mass, store, energy | Vulnerable continuous material/body state; mass gates recurrence and node activation | Saved; evaluation retains mass but standardizes store and energy |
| mask, umask, types | Protected inherited topology, sensor routing and chemical-bank membership, not acquired information in this experiment | Saved unchanged; no produced boundary or learned replacement of the masks |
| Hidden activations | Transient computation, not persistent lifelong memory | Reset to zero by forward for each trial |
| Learning and environment machinery | Global optimizer, objective laws, masks, random streams, reward calculation, direct material delivery and training energy top-ups remain outside the maintained organization | Full branch cloning and evaluation resets are host operations; checkpoints/traces are external records |

Replay records are particularly important for future information-loss claims: successful binary attempts plus recorded cue inputs retain association information outside biomass-gated parameter arrays. Target and Adam provide additional acquired state. They are not consulted during no-learning evaluation, but can influence continued learning in the original process. Their absence from E2 checkpoints does not mean they were absent from E2 training.

The inspected seed-200/plastic/history0/developed checkpoint has 11 arrays: p_u (8 x 12), p_w (12 x 12), p_b (12), p_v (12 x 5), mask (12 x 12), umask (8 x 12), types (12), mass (12 x 12), store (12), scalar energy and updates. There are 312 dense parameter slots and 70 permitted recurrent edges for this seed. Loaded p arrays are finite; target equals p; Adam moments are zero and t=0; replay length and cursor are 0; restored updates=993. There are 672 final E2 checkpoint files (16 x 3 x 2 x 7). Full contents of all 672 checkpoints were not semantically audited, although their original bytes were included in preservation hashing.

Network.forward applies p_w * mass and biomass-derived node gains. Body.update grows/decays mass and charges stores; it does not destroy or locally reconstruct p, target, replay or Adam information. Complete lesions remove differentiated outputs but leave the host's learned parameters intact. Restoring original biomass can expose those parameters again. diagnose_e2.py explicitly preserves original weights for mass loss/restoration and uses copies for weight perturbation. This is conductance-dependent access to protected information, not autonomous recovery of deleted acquired information.

## Historical package-manifest drift

PACKAGE_MANIFEST.json remains version 0.2. Of its 756 entries, 753 match current size and SHA-256, none are missing, and three drift:

| Path | Recorded bytes | Current bytes | Current SHA-256 |
| --- | ---: | ---: | --- |
| ENGINEERING_LOG.md | 1,933 | 3,898 | `a575168dd92fa05ced72539091656b729d983fb433d706eeec0f31e50c452a27` |
| README.md | 4,205 | 4,727 | `13490931ee5d1d4bf67807b5b0c67ef0c18e9b397c2fa054d0b209e48d9f065c` |
| RESEARCH_NOTEBOOK.md | 33,874 | 36,320 | `4d6436ac4062e3ec4c12656d0a9c547d11fa5faf564835c2b8ab97e555820248` |

The inventory has 4,504 unlisted files, including 579 type-checker cache files, 2,985 files under e2_results/, E2 engineering outputs, the E2 sources/protocol/freeze/audit scripts, E3_DESIGN.md and NEW_AGENT_GUIDE.md. The count includes the manifest itself and excludes research-tracking files, so it must not be described as 4,504 missing scientific artifacts. The current README labels the project v0.3. This v0.2 manifest is historical, not a complete valid manifest of the current tree. It was not repaired, regenerated or relabelled.

## References read

NEW_AGENT_GUIDE.md (full); RESEARCH_NOTEBOOK.md (E0/E1 evidence and opening E2 context); README.md; E1_PROTOCOL.md; E2_PROTOCOL.md; E2_DIAGNOSTIC_PROTOCOL.md; ENGINEERING_LOG.md; E1_FREEZE.json; E2_FREEZE.json; PACKAGE_MANIFEST.json; pilot.py; e1/circuits.py; e1/control.py; e1/environment.py; e1/experiment.py; e2/model.py; e2/experiment.py; analyze_e1.py; analyze_e2.py; diagnose_e2.py; replay_e1.py; replay_e2.py; verify_e1.py; verify_e2.py; results/run.json and summary/raw tables; e1_results/run.json, RESULTS.md, summary.json, VALIDATION.json and raw tables; e2_results/run.json, RESULTS.md, summary.json, VALIDATION.json, DIAGNOSTICS.json and raw tables. No external research was necessary.

## Recommended next checks not completed

* [ ] If bitwise replay is required, use a separately provisioned environment matching the saved Python 3.12.14/NumPy 2.3.5 stack and investigate numerical-library/hardware provenance. Do not replace saved outputs or reinterpret tolerance agreement as exact equality.
* [ ] If strict filesystem metadata immutability is required, repeat in an isolated read-only copy with editor/type-checker background writers disabled. Preserve this run's cache-metadata failure as a finding.
* [ ] If a current distribution is needed, create a separately versioned manifest or erratum identifying the historical E1 log drift, rather than changing the existing v0.2 manifest or E1 freeze. This requires a separate authorized task.

No clarifying question is needed for this completed audit. No experiments, retraining, threshold revisions, original-file repair, or E3 implementation is recommended as part of it.