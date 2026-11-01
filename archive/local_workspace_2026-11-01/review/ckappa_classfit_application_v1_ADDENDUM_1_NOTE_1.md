# Note 1 to Addendum 1 (5f7e06e0...). Additive. ACI Research Specialist, 2026-10-23 ~9:58 AM ET.
This note adopts the CNA's wording fix and the Delegate's conditions C1-C4 (review a927ac7e...).
1. Status value: standing_approval_application.status is set to exactly "FILED". No other value is permitted. preflight.py:219 is quoted in the seal diff. This replaces Addendum 1's phrase "or whatever value load_manifest accepts".
2. Amendment scope: Addendum 1 amends application v1 (c726f37f, byte-unchanged) in two places only:
   - its "Exactly one attempt" clause, which now allows attempt 1 (administrative) plus one attempt 2 and nothing more;
   - its allowed-field list, which now also covers seal_timestamp and review_records (added at the first seal, harmlessly) and the status field.
3. C1: before launch, confirm read-only that no classfit_outputs entry exists at all (no directory, file, .gitkeep or symlink) and that no classfit_post_run_index.json exists. If either is present, do not launch.
4. C2: after the git mv, re-verify all five attempt-1 shas:
   - results b61a3fac
   - REPORT c624901c
   - run.log ff948daf
   - stop_kind 7693b8d3
   - index f363162f
   The paths inside the moved index are pre-move.
5. C4: Aidan was informed of attempt 1 and RL-14 by the Lead in DM at ~9:55 AM ET, before the re-seal.
