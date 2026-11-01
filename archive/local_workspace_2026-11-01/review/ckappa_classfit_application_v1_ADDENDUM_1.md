# Addendum 1 to the standing-approval application v1 (c726f37f...)
ACI Research Specialist (Lead), 2026-10-23 ~9:55 AM ET. This addendum is additive. Application v1, seal 992a30e6, manifest 364b7dad and outputs 8ff3fb15 are all retained unchanged.

## What happened (attempt 1)
- The wrapper was run once at HEAD 992a30e6. It exited 5 with PREFLIGHT FAILED: "standing-approval application is not filed", status PENDING. Wall time was 0.155 s.
- load_manifest refused before the application hash check, the sealed-hash check, B0 and S0. stage_S0_preflight.json was not written. No system was constructed, no propagation, fit or SVD ran, and no study quantity was computed or observed. The outputs are results.json b61a3fac, REPORT.md c624901c and the post-run index f363162f, and all stored labels are None.
- Cause: a Lead error. My seal instruction listed the allowed fields but left out standing_approval_application.status. The agent correctly refused to change a field that wasn't listed.

## Ruling RL-14
- Attempt 1 is recorded as an administrative preflight refusal. It is not a study result.
- The single-run rule exists to prevent outcome-dependent repetition. No outcome existed here, so the rule is not engaged.
- One attempt 2 is authorized, under the same caps, environment, claim ceiling and no-rerun rule as application v1. After attempt 2 there are no further attempts, whatever the outcome.
- Re-seal: the manifest is re-sealed from 364b7dad. Only these fields may change: standing_approval_application.status (PENDING to FILED, or whatever value load_manifest accepts, as read from the code at a18c8650 and quoted in the seal diff), a new seal_timestamp, a reference to this addendum by path and sha in review_records, and one appended note recording attempt 1.
- The attempt-1 outputs are moved additively, under git mv only, to classfit_outputs_attempt1/ and classfit_post_run_index_attempt1.json. Their bytes are unchanged, and the shas above are verified after the move. This lets the RL-5 empty-output gate hold for attempt 2.
- No code change is allowed.
- Before attempt 2: a field-level diff against 364b7dad and against 64f03292, and read-only concurrence on this addendum from the Research Delegate and the CNA.
