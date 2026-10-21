# Deviations and implementation choices

Status: written before Stage 0, before any study training, and before any target evaluation of seeds 400–409.

No consciousness claim.

## Deviations

The study design is the FINAL protocol. Two optimizer uses happened before this freeze and are not among the 30 study runs:

1. A 20-step call to the unchanged PR #7 `train_arm` on seed 7, batch 256, episode stream 1007, was used only to time a step. The weights were discarded. The run was not scored against the target.
2. A 2-step `train_cand` and a 2-step `train_arm_rfix` on seed 11, batch 256, episode stream 1011, checked that both trainers hash the same accepted batches as `episode_stream_digest`. The digests matched. The weights were discarded. The runs were not scored against the target.

Neither use touched seeds 400–409 or streams 1400–1409. They are not replacement seeds, restarts, or a search. They are recorded because the approval names the synthetic fixture as the implementation-testing training.

No other deviation is known at freeze.

### Post-freeze correction, before any study training

The first invocation of Stage 1, on commit `0fed34ebad4bee2b794ce1324ec286ae0a2c68ab`, printed `stage1 seed 400 CAND starting` and then raised `NameError: name 'load_snapshot' is not defined` at `frozen_recurrent_compensation_study.py`, in `_train_one`, on the call that loads the sealed init into `CoreGRU`. That call is before `train_cand` and before `train_arm_rfix`. The process exited. It wrote no `progress.jsonl` line and no Stage 1 checkpoint. No optimizer step ran on seeds 400–409. No target was evaluated.

The correction, applied before any study training and before any score, is the import of the existing `load_snapshot` from `recurrent_core_transfer_models`. No training equation, seed, step count, freeze rule, evaluator, or label rule changes.

The Stage 0 runner refuses to train or score when `code_tree_sha256()` differs from the hash stored in `manifest_stage0.json`. Leaving the broken import in place makes the sealed procedure impossible to execute. Rewriting inits or episode digests is not part of the correction. After this import and this section were added, only `code_tree_sha256` and `code_files_sha256` in `manifest_stage0.json` were replaced so they name the corrected tree. Init checkpoint shas, W0 shas, episode-stream digests, pairing flags, and the synthetic-fixture record are the Stage 0 bytes. The freeze commit retains the pre-correction code-tree hash `1349a6786e92d81ba194d866d48dd88304961b5acda900fc5cadc3c52998f7f9`. The corrected code-tree hash is stored only in `manifest_stage0.json`, which is outside the code-tree hash, and is not copied back into this file.

## Choices fixed here

### A1–A6

Confirmed as the FINAL protocol states them. In particular: gradient-None is checked after every backward (A4's default); init evaluation is only in Stage 2 (A2); the synthetic fixture is implementation testing (A3); reproducibility's unresolved count is final BOUNDARY runs, and invalid runs are counted separately (A6).

### Episode digest

sha256 over steps in order. Each step contributes the C-order little-endian float32 bytes of the accepted bit array, shape `(batch, 8)`, then the accepted label array, shape `(batch, 3)`, as returned by `recurrent_core_transfer_train.sample_batch`. Study runs use batch 256 and 4000 steps. The generator seed is `1000 + s`. TEST histories are rejected. VAL histories are not rejected.

Digest equality is required when the arm consumed the full 4000-batch stream and did not already fail a freezing check. An early stop is not also labeled a digest mismatch. A partial stream stores `episode_digest_matches_stage0: null`.

### CAND batches

`train_arm` is called unchanged. For the duration of that call, `recurrent_core_transfer_train.sample_batch` is wrapped so the batches actually consumed are hashed. The wrapper returns the original tensors. The PR #7 source file is not modified.

### Draw and train order

Seeds 400 through 409. Within a seed: CAND, then R-FIX-32, then R-FIX-48. Each init is `build_initialized(s, H)`.

### W0 bytes

sha256 of the contiguous float32 tensor bytes of `rnn.weight_hh_l0`. The hash is checked after every optimizer step, after training, and after checkpoint reload. Edit 4 requires the last two. The per-step check is additional. A mismatch invalidates the run.

### Synthetic fixture

Seed 7, readout width 32, 4 Adam steps, batch 8, synthetic bits and labels from generator seed 17. Negative cases, all caught by `train_arm_rfix`'s checks: an extra frozen tensor, `weight_hh` left trainable, a backward pass that produces a `weight_hh` gradient, and an optimizer that includes `weight_hh`. `freeze_mode` other than `"rfix"` is only the negative fixture. It is not a study arm. The unit test runs the fixture, and Stage 0 runs it again to record the result. Neither execution is a study run.

### Code-tree sha

sha256 of `name + NUL + sha256(file bytes) + newline` over `CODE_FILES` in sorted order. Stage manifests, checkpoints and results are not part of the hash.

### Validity partition

Final statuses are a partition of the ten runs: VERIFIED TARGET PASS, VERIFIED TARGET FAIL, BOUNDARY / NUMERICALLY UNRESOLVED, INVALID. Invalid-run count is the size of the INVALID cell. Boundary count is the size of the BOUNDARY cell. Reproducibility is UNRESOLVED when invalid runs plus boundary runs is greater than 2; otherwise eight or more final passes is TARGET REACHED REPRODUCIBLY and fewer is REPRODUCIBILITY CRITERION NOT MET.

An initialization witness is an init checkpoint with status VERIFIED TARGET PASS. It is counted even when the final checkpoint is invalid. Init invalidity is reported on its own line and does not, by itself, move a clean final out of the final partition. Acquisition requires init status VERIFIED TARGET FAIL and final status VERIFIED TARGET PASS.

A final checkpoint is evaluated when Stage 1 recorded 4000 steps, the checkpoint round-trip succeeded, the file sha matches, and the weights are finite. Stage-1 invalid reasons still apply, so a digest or freeze failure is not a verified pass. A shorter run is not given a final T.

### Shared H=32 init

If the CAND and R-FIX-32 init shas differ, or their statuses differ, or their E1 normalized components disagree under the §3.1 tolerance, both inits are INVALID for that seed (`pairing` or `shared_init_classification_mismatch`). One verified H=32 init is one witness, noted under both arms.

### Binding, best, median, paired difference

Displayed binding is the argmax of the three E1 normalized components, in the order prefix, total, xor. Exact ties are co-binding and count in each component. E2's argmax is stored. An argmax difference is not itself an integrity failure. Binding frequencies use classified checkpoints as the denominator, separately for init and final.

Best T is the minimum E1 final T. The smallest seed breaks ties. Median is the middle value, or the mean of the two central values when the count is even. Invalid finals are omitted.

Paired difference is E1 final T(R-FIX) − T(CAND) when both finals are classified. Otherwise it is null.

### Other reporting

`C_prefix` and `G_prefix` are reported for E1 and E2 whenever both endpoints were evaluated. `G_prefix` is within-run prefix-loss improvement. Neither gates the target.

Former VAL errors are the probability-weighted squared error renormalized on the VAL histories (the inherited `probability_excess` definition). Descriptive only.

Float32 evaluation runs the module's native sequence forward and does not gate.

In the fixed sentences, `R-FIX-H` is written as the arm name, and `u` and `i` are the boundary count and the invalid-run count. The Edit 6 witness sentence is emitted only for an R-FIX arm that has a witness. CAND uses the same labels and does not receive that sentence, because the sentence says `weight_hh` stayed at W0.

### Runtime

`torch.set_num_threads(1)` and `torch.use_deterministic_algorithms(True)` are set by this runner before initialization and training, as in the PR #7 study runner. `train_arm` itself sets the thread count and not the deterministic flag. That split is unchanged.

### Crash guard

Stage 1 appends a progress line only after that arm's one training call returns and its checkpoint has been written. An arm with a progress line is not trained again. A checkpoint file without a progress line stops the runner instead of training that arm again. An incomplete call that never returned is not a saved run. This is not a restart, a second attempt, or a replacement seed.
