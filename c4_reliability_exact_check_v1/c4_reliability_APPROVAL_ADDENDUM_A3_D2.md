# W-REL Addendum A3 Deviation D2 authorization: replay-agreement key set

Recorded: 2026-10-21, 3:29 PM ET (America/New_York)
Authority: Aidan Ahern (PI), chat message t38u at 3:15 PM ET: "I'm approving everything you deem necessary as Research Lead". The Research Lead judges this deviation necessary.

Context: The D1 verification (approval 66b9439, freeze 8010eb5, results 0c5b308) stopped on R-HAC-MB at T_SEP=3. The only mismatch was the non-deciding diagnostic field cfo_detail, which is null in the stored primary because evaluate_mb_family never emits it. The runner had compared every A2 primary key, not the frozen replay-comparison key set. Every deciding field matched, including flags with C-FO, and the 432-row intervention/repair table agreed.

Authorized: replay agreement is assessed on the frozen replay-comparison key set (deciding statistics, as defined in the frozen spec and the D1 agreement list). Non-deciding diagnostic fields such as cfo_detail are reported as differences but are not gating. The fix is frozen before execution. One complete independent-verification pass runs over every configuration (the reference and all roster controls at T_SEP=3 and 4, plus PM-ACT, including the T_SEP=4 machine rebuild). Formal labels are issued only if that replay agrees. Primary results are not rerun or replaced. Criteria, roster, costs and horizons stay unchanged. The A3 caps apply cumulatively. Everything is recorded additively as Deviation D2. No C4 or consciousness claim.
