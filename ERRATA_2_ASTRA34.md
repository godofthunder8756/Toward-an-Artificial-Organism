# Errata E34-1 through E34-6

Source: Astra consult #34, response sha256 prefix bf724ca2. Date: 2026-10-21.

E34-1 supersedes the draft feasibility note in the results review by reference. That results review file is not edited.

## E34-1

> "Post-run feasibility interpretation, without relabelling: For 70 TRAINED checkpoints forming seven (PR, arm) units -- PR #7-#9 cand_final and f_trained, and PR #10 CAND -- pooled L(base) is below the frozen absolute floor in both C1 and C2. Since L(full) is nonnegative, their meets-floor outcome was arithmetically unattainable. Their below-floor classifications therefore do not discriminate hidden-state accessibility once this bound is known. Their measured losses and gains remain informative descriptions of the tested procedure. For the other 16 units, comprising 160 checkpoints, the elementary bound permits a pass in both comparisons, but does not establish decoder attainability. None met the C2 floor. This feasibility partition is a post-run interpretation; it changes no label, denominator, count or quota outcome. A different floor would belong to a separately specified, development-informed analysis."

## E34-2

> "For 89 TRAINED checkpoints, adding STATE to B_conf reduced held-out oracle-probability loss by the prespecified margin. No TRAINED checkpoint met the C2 margin. These findings concern the declared feature-and-regularization procedure. They establish neither information discarded by the output nor absence of information in hidden state. Shrinkage, extrapolation and representation geometry remain possible contributors, not identified explanations."

## E34-3

> "The later 112/112 consistency-check rerun resolves the missing-dependency obstacle to re-executing that check in the recorded environment. It does not make the stopped check contemporaneously complete at the original run. The original deviation, later dependency additions and resolution remain separate additive records. No numerical audit was rerun."

## E34-4

> "The recorded commit, runner-session and checkpoint-copy timestamps support the reported ordering of the documented run. A checkpoint-copy modification time is not a checkpoint-load timestamp, and these records alone do not independently establish that no earlier checkpoint inference occurred. The no-earlier-inference statement is retained as an execution attestation."

## E34-5

> "The reported 26.416-second wall time is an internal audit-clock measurement, not an all-inclusive launch-to-completion measurement. The clock starts after module imports and manifest checks, and the stored runtime is sampled before final output serialization and report writing. The 27.224-second CPU value is cumulative process-and-child usage and has a different measurement interval. Their difference is not explained by interpreter overhead on an identical interval. Any all-inclusive cap-accounting statement must separately identify available launch, completion and setup records, and disclose unmeasured portions."

## E34-6

> "Future improvement-based protocols distinguish a scientific effect floor from the available improvement headroom. They specify the relevant upper bound, its assessment stage and the interpretation of an unattainable floor before outcome evaluation. An outcome-dependent headroom check is not described as outcome-blind, and feasibility does not imply attainability."
