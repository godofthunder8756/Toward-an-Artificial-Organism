# RESULTS v2

Corrected classification for the W-REL bounded exact check. `RESULTS_v1.md` is unchanged and remains the record of what the runner emitted, including the exact rationals. This file is a documentation correction. It does not replace `outputs/`. No solver, planner, item, or replay was run to produce it.

No ledger file is edited. The ledger sentence below is the wording to record. It includes the statement that the C4 evidence row and status row are unchanged, and it states no consciousness conclusion.

## Formal A-SEP certification

**UNRESOLVED-COMPUTE**, pending completion of the missing ITEM-9 coverage required by spec §5.4.

This is an incomplete-computation outcome. It is not a cap-exceeded outcome. Agreement on the checks that were performed is retained. COMPLETE or AGREE on those checks does not certify the omitted checks. The original post-failure ITEM-8-dependent replay portion was NOT-RUN.

The four rows below are conditional downstream classifications. They are not the formal A-SEP certification.

## Classification conditional on completion of required validation

| T | Costs | Classification conditional on completion of required validation |
| --- | --- | --- |
| 3 | (1/50, 3/50) | UNRESOLVED-DESIGN; no donor contrast; C-REF and C-T2 also fail |
| 4 | (1/50, 3/50) | UNRESOLVED-DESIGN; same reasons |
| 3 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET; C-REF and C-SEL fail |
| 4 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET; C-REF fails |

Reasons, one setting at a time:

- T = 3, costs (1/50, 3/50). UNRESOLVED-DESIGN because there is no donor contrast. C-REF and C-T2 also fail.
- T = 4, costs (1/50, 3/50). UNRESOLVED-DESIGN for the same reasons: no donor contrast, and C-REF and C-T2 also fail.
- T = 3, costs (1/100, 1/10). REFERENCE CRITERIA NOT MET because C-REF fails and C-SEL fails.
- T = 4, costs (1/100, 1/10). REFERENCE CRITERIA NOT MET because C-REF fails.

T = 4 was outside some replay coverage by the frozen ITEM-9 scope. That does not make the required ITEM-9 work complete. These rows are setting-specific findings. The study-level validation gate is the UNRESOLVED-COMPUTE certification above.

## Reproduction masking

Core intervention components that are unavailable because of NO INTERVENTION CONTRAST are masked consistently. Identity-swap values remain descriptive only.

MB-myopic reproduction at the two no-contrast settings is **UNRESOLVED**, not YES.

| T | Costs | MB-myopic reproduction in this correction |
| --- | --- | --- |
| 3 | (1/50, 3/50) | UNRESOLVED |
| 4 | (1/50, 3/50) | UNRESOLVED |
| 3 | (1/100, 1/10) | YES, provisional, subject to the validation shortfall |
| 4 | (1/100, 1/10) | YES, provisional, subject to the validation shortfall |

`RESULTS_v1.md` reports YES for MB-myopic at all four settings. That emitted column is what the runner wrote. The two no-contrast YES entries are masked here. The YES comparisons at the two contrast settings remain provisional comparison results, subject to the validation shortfall. PM-ACT reproduction YES at T = 4 and (1/100, 1/10), as emitted, is in the same provisional class.

## Compute

The corrected total is **about 48 minutes**, including the D1 rebuild. The figure that counted only the freeze-run process left the rebuild out.

The two recorded process clocks, copied from the existing JSON and not recomputed, are:

- Freeze-run `outputs/SUMMARY.json` `total_wall_seconds_float`: 1408.710860391 seconds.
- D1 `outputs/deviation_1/ITEM-9.json` `total_wall_seconds_float`: 1420.8845916250002 seconds.

Their sum is 2829.595452016 seconds, which is 47.2 minutes and is the consult's "approximately 48 minutes." Both processes stayed under the 4-hour cap. Per-item cap compliance is the statement in E-W8: it is supported by the stated conservative bounds. The longest freeze-run item clock is ITEM-2 at 1045.629281903 seconds. Charging the entire D1 process clock, 1420.8845916250002 seconds, on top of that item gives 2466.513873528 seconds, under the 3600-second item cap. That sum is arithmetic on recorded clocks. It is not a new run, and the D1 wrapper did not record a separate per-item rebuild time.

## Ledger wording

Consult 26, section B.5, verbatim:

> "W-REL: theory-stage C4 candidate; bounded exact check executed, with mandatory validation incomplete. Execution was approved by Aidan on 2026-10-21 at 8:58 AM ET. The reported computation, including the D1 rebuild, remained within the declared caps.
>
> Q-EXIST/world: the implementation audit verified the declared non-recheck symmetry on its audited domain; the factorization argument supplies the general history-level claim. Rechecks can provide source information, without guaranteeing finite-horizon identification.
>
> ORIGIN: the analytic mechanisms, predictors and update rules are supplied. Q-LEARN was not tested.
>
> ROLE/Q-CAUSE: no tested setting established the complete prespecified admission conjunction. At costs (1/50,3/50), the reference never rechecked at T=3 or 4, so the donor contrast was absent; C-REF and C-T2 also failed. At (1/100,1/10), C-REF's resampling requirement was unattainable for the reference; T=3 additionally failed the directional checking criterion. Reported component intervention and rescue results are retained as bounded facts about the supplied analytic agents.
>
> REDUCTION: after correcting unavailable-component masking, MB-myopic reportedly reproduces the reference pattern in the two settings with donor contrast; PM-ACT reportedly reproduces it at T=4 and (1/100,1/10). These comparisons do not establish absence of an assessment role and remain subject to the validation shortfall.
>
> Formal A-SEP certification is UNRESOLVED-COMPUTE pending completion of mandatory ITEM-9 coverage. Conditional downstream classifications are recorded separately. Q-NECESSITY was not tested. No change to the C4 evidence or status row, and no consciousness conclusion."

## Scope of this correction

Emitted labels, flags, and exact rationals stay in `RESULTS_v1.md` and in `outputs/`. C-FO flags for F0-based controls were assigned by construction; that separation is E-W7 in `ERRATA_v1.md`. The omitted ITEM-5 `n_R_S` counts stay missing. Formal certification waits on the missing ITEM-9 coverage. That completion has not been approved and was not run.
