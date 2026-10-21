# RESULTS A3 errata E30

Documentary errata for Astra consult #30. This file is additive. It quotes the reviewer's section D close-out wording and errata E30-1 through E30-7. Deliverables 1 and 2 of the E30 close-out do not contradict those quotations, so none is corrected. The diagnosis and the coverage table are in `WREL_CLOSEOUT_E30_v1.md`.

No frozen file is edited. No criterion or label is changed. No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated.

## Corrections

None. The rescue-support classification is case (ii), a repaired PM state with zero intact decoder occupancy, which is what E30-3 says the record identifies. The D2 coverage table records every mandatory comparison and records `cfo_detail` as having no primary counterpart, which is what E30-4 requires. The stored reproduction columns match E30-2.

## Section D close-out wording

Verbatim:

> "W-REL PR #11 records a bounded analytic study of source-dependent checking and the proposed assessment criteria. The original mandatory verification gap was completed additively. Under H0, the original settings (c_R,c_S)=(1/50,3/50), T_SEP=3 and 4, retain UNRESOLVED-DESIGN; the original settings (1/100,1/10), T_SEP=3 and 4, retain REFERENCE CRITERIA NOT MET.
>
> "Exploratory Addendum A2 attained the frozen reference core conjunction at (1/100,3/50), T_SEP=3 and 4. Addendum A3 evaluated the frozen eligible named controls at those settings. Following the documented D1 and D2 verification repairs, the reported formal outcome is UNRESOLVED-DESIGN at both settings: PM-ACT fails no evaluable core criterion, while its required rescue comparison is not evaluable.
>
> "All eligible non-PM implementations fail C-REF and C-T2. PM-ACT full-pattern reproduction is NO at T_SEP=3 and UNRESOLVED at T_SEP=4; its core conjunction is unresolved at both. These findings do not establish separation from all conventional controllers, absence of assessment in PM-ACT, or a fundamental impossibility of identifying the proposed role.
>
> "The reference is a supplied analytic mechanism. Its zero C-T2 error is principally a calibration and implementation result. Intervention findings are bounded by the frozen donor choices, probe battery, horizon and cost settings. The analytic predictors share the oracle's binary decisions on the tested domain, so the study does not establish assessment of learner-specific departures from oracle correctness. R-HAC-MF was evaluated only at T_SEP=3.
>
> "Q-LEARN and Q-NECESSITY remain untested. No C4 evidence or status row changes, and no consciousness or sentience conclusion follows. The analytic tournament is closed. Further work requires a separately frozen study addressing an identified scientific question."

## E30-1 through E30-7

Verbatim from section F of the review:

E30-1. Scope of separation:

> "The reference meets the frozen conjunction, while every eligible non-PM implementation fails C-REF and C-T2. This is a comparison with the named implementations, not separation from ordinary control mechanisms generally."

E30-2. PM-ACT outcome:

> "PM-ACT full-pattern reproduction is NO at T_SEP=3, owing to the reported e_A_S discrepancy, and UNRESOLVED at T_SEP=4. Its core conjunction is unresolved at both settings because rescue is not evaluable. Criterion attainment and full-pattern reproduction remain separate."

E30-3. Rescue support:

> "The record identifies the exact conditioning event, distribution and zero denominator responsible for PM-ACT's unavailable rescue statistic. A zero-probability decoder-conditioning event is distinguished from an impossible recipient-world trajectory. No fundamental identifiability conclusion is inferred from this unavailable comparison."

E30-4. D2 verification:

> "D2 was specified after observing the D1 discrepancy. It restores the frozen required comparison contract without changing primary results or scientific criteria. Every mandatory quantity is accounted for explicitly; a required field absent from the primary is a coverage failure, not an automatically excluded comparison. The replay-only cfo_detail diagnostic is reported separately."

E30-5. Stop history:

> "The primary verification stopped on a representation-handling exception. D1 stopped on the reported comparison discrepancy. D2 completed the declared verification comparisons. No resource cap was reached. Original artifacts and all repair records remain preserved."

E30-6. Roster:

> "The eligible roster contains 20 controls at T_SEP=3 and 18 at T_SEP=4, including PM-ACT. Including the reference gives 21 and 19 configurations. R-HAC-MF is absent from the T_SEP=4 comparison."

E30-7. Close-out boundary:

> "The W-REL analytic tournament ends with the reported unresolved named-control comparison. The next proposed study concerns acquisition and causal use of learner-specific correctness information. It does not require a faithful compiled implementation to lack or fail the proposed functional role."

## Authority and repair scope

D1 and D2 were authorized by the Research Lead under Aidan Ahern's standing approval given at 3:15 PM ET on 2026-10-21. The approval files quote that message as "I'm approving everything you deem necessary as Research Lead". The D1 approval is `c4_reliability_APPROVAL_ADDENDUM_A3_D1.md`, recorded 2026-10-21 at 3:16 PM ET, sha256 `47fd381e1fdf98b40914b117e5bf24412316a7aba56240fcce273b78e872bd62`. The D2 approval is `c4_reliability_APPROVAL_ADDENDUM_A3_D2.md`, recorded 2026-10-21 at 3:29 PM ET, sha256 `1f7158133243a2a506076bedba3a1ee5147f0004a6b772e6c92f077e6f8b82df`. This close-out does not request a further approval of those repairs.

D1 authorized scope: a plumbing-only repair of the verification-block representation crash, then the one independent replay per configuration that Addendum A3 already permitted and that had not run. The primary evaluation is not rerun. Criteria, thresholds, donor rules, interventions, rescue, decision order, roster, costs, and horizons stay unchanged.

D1 repair that executed: the blind joint walks each regime and stores content `None`, so the frozen one-regime unpack is not called on two horizons. Commit `0c5b308` then stopped during the `T_SEP = 3` reference comparison. The only stored failure is `cfo_detail`. No formal label was issued. Primary files at `7e153d1` were left unchanged.

D2 authorized scope: replay agreement is assessed on the frozen replay-comparison keys. `cfo_detail` is reported and does not gate. One verification pass covers the reference and every roster control at `T_SEP = 3` and `T_SEP = 4`, including PM-ACT and the `T_SEP = 4` machine rebuild. The primary evaluation is not rerun. Criteria, roster, costs, and horizons stay unchanged.

D2 repair that executed: gating uses the frozen `_compare_cases` tuple plus the `_mb_replay_failures` additions, restricted to fields the stored primary emits, with roster per-action errors recorded when the columns do not store them. `cfo_detail` is a non-gating difference. Commit `1f2a6c9` completed that pass. All 21 configurations at `T_SEP = 3` and all 19 at `T_SEP = 4` agreed on the gating keys. The formal label is UNRESOLVED-DESIGN, clause 7, at both settings. The coverage table in `WREL_CLOSEOUT_E30_v1.md` is the record that this restriction did not drop a mandatory comparison.
