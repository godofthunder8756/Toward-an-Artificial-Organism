# Errata v1

Additive reporting and provenance corrections for draft PR #10. Consult #20 is the authoritative wording. No existing result file is rewritten. No training was run for this errata. No label changes.

The ledger is `frozen_recurrent_compensation_results_v1/results_v1_errata/RESULTS_v2.md`. The path `results_v1_errata/RESULTS_v2.md` already holds the recurrent-core presentation v2, so that file is not replaced.

## E-D1

> "Stage 0 was originally sealed at 0fed34e with code tree 1349a678.... Before Stage 1 optimization, fd720ee added the missing load_snapshot import and recorded corrected code tree d00ff89b.... The sealed manifest was edited in place to update code hashes, contrary to the intended immutable-manifest practice. Initial checkpoints, W0 hashes, episode digests and pairing records were unchanged. Stage 1 and Stage 2 used the corrected implementation. The original and corrected manifests are preserved as separate immutable provenance artifacts."

## E-D2

Consult #20 adopts E-D1 and E-D2 with one wording. The same sentence is the E-D2 record:

> "Stage 0 was originally sealed at 0fed34e with code tree 1349a678.... Before Stage 1 optimization, fd720ee added the missing load_snapshot import and recorded corrected code tree d00ff89b.... The sealed manifest was edited in place to update code hashes, contrary to the intended immutable-manifest practice. Initial checkpoints, W0 hashes, episode digests and pairing records were unchanged. Stage 1 and Stage 2 used the corrected implementation. The original and corrected manifests are preserved as separate immutable provenance artifacts."

The copies are `STAGE0_MANIFEST_original_0fed34e` and `STAGE0_MANIFEST_corrected_fd720ee`, with `MANIFEST_ADDENDUM.md`.

## E-D3

> "The quoted t28s1 question is the approval request actually presented, as relayed by the Specialist. Its exclusion sentence paraphrases consult #19 without expanding the authorized scope."

The question, the answer, and the consult #19 sentence labelled proposed wording are in `APPROVAL_PROVENANCE.md`.

## E-D4

> "Three pre-freeze implementation tests performed 24 optimizer steps on real W2 streams using non-study seeds 7 and 11. They were outside the documented synthetic-fixture exception and were not covered explicitly by the 30-run approval. Their weights were discarded and no target evaluation was performed. No contamination of the study cohort was identified. Their timing relative to approval is after Aidan's approval at 3:06 AM ET on 2026-10-21. This authorization deviation is recorded separately from the validity of the study results."

Timing basis. The placeholder is filled as after the approval.

- Aidan's approval is recorded at 3:06 AM ET on 2026-10-21.
- The cloud-agent run that contains the calls, `bc-8340cf4a-0af8-5058-94b9-feee87e5eb07`, was created at 2026-10-21 07:07:06.955 UTC, which is 3:07:06 AM ET.
- That run's transcript starts with the implementation request, which already quotes the approval. The seed 7 twenty-step `train_arm` call and the seed 11 two-step `train_cand` and `train_arm_rfix` calls appear later in the same transcript. The transcript has no per-command clock.
- Freeze commit `0fed34ebad4bee2b794ce1324ec286ae0a2c68ab` already contains the deviation note for those calls. Its author and committer dates are 2026-10-21 07:33:32 UTC, which is 3:33:32 AM ET.

The calls therefore sit after 3:06 AM ET and before the freeze commit.

## E-D5

This replaces the assertion that the final minibatch losses establish operation at the noise floor.

> "No training-loss curve or intermediate checkpoint was recorded. The final loss is one stochastic minibatch measurement. Comparing it with the distribution-averaged Bayes risk, 0.58395, does not establish convergence, a plateau or attainment of the noise floor."

## E-D6

> "CAND is the unrestricted comparator: target reached in 10/10 seeds. Its witnesses are not R-FIX restricted-class witnesses."

## E-D7

> "The missing import escaped testing because the exact Stage 1 entry path was not exercised. Future freezes must test that entry path using an authorized fixture, including checkpoint loading, optimizer construction and manifest output."
