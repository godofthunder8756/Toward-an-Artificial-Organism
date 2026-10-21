# ERRATA v1

Documentation only. This file quotes consult 26, section C, and records E-W4. E-W numbering is the numbering in the independent review `wrel_results_review_v1`. `RESULTS_v1.md` and every frozen file and output JSON are unchanged. No solver, planner, item, or replay was run to produce this errata.

The quotations below are consult 26, section C, verbatim.

## E-W1

> "Core intervention components unavailable because of NO INTERVENTION CONTRAST are masked consistently for the reference and all controls. Identity-swap values remain descriptive only. MB-myopic reproduction at the two no-contrast settings is UNRESOLVED, not YES."

## E-W2/E-W3

> "ITEM-9 did not deliver all mandated Sec.5.4 coverage. Agreement on performed checks is retained, but COMPLETE/AGREE does not certify omitted checks. The original post-failure ITEM-8-dependent replay portion was NOT-RUN. Mandatory validation remains incomplete; conditional downstream classifications are not final A-SEP certification."

## E-W4

The omitted ITEM-5 `n_R_S` counts are **missing**.

Retained-artifact inspection, with no recomputation: `outputs/ITEM-5.json` has 468 rows. All 288 H0 rows store `n_R_S` as null. The 180 H1 rows do not contain `n_R_S`. No other file under `outputs/` holds those dropped R-CG recheck counts. They are not recovered.

ITEM-6 `n_R` values are R-HAC-MF counts. They are not the omitted R-CG counts and are not used as a substitute.

## E-W5/E-W6

> "The chosen A-SEP settings were not checked prospectively for joint criterion attainability. At c_S=1/10, the resampling conjunct is unattainable by the reference. At (1/50,3/50) and T_SEP in {3,4}, the reference generates no rechecks or donor contrast and also fails C-REF and C-T2. These are limitations of the tested design, not implementation bugs or evidence that assessment is absent."

## E-W7

> "C-FO for F0-based controls follows analytically from the predictor's independence from manipulated controller content. These flags were assigned by construction, not obtained through independent intervention replay. Analytic justification and executed verification are reported separately."

## E-W8

> "D1 repairs a missing report-field connection and enables a previously failed calculation; it does not alter the specified scientific formulas. Frozen outputs and D1 outputs are preserved separately. Rebuilt ITEM-1 through ITEM-7 scientific equivalence was inferred, not independently observed. The D1 wrapper did not invoke the original manifest guard. Total reported computation including the rebuild was approximately 48 minutes; per-item cap compliance is supported by the stated conservative bounds."

## Advisory-run disclosure

> "At approximately 10:59 AM ET, the reviewer executed a seven-second independent reference-planner calculation outside the frozen analysis specification. It preceded the subsequent scope-tightening message. Its artifacts are preserved as ADVISORY and do not satisfy mandatory replay coverage or support confirmatory labels. The scope deviation has been reported to Aidan."

**Timing correction (reviewer, 2026-10-21):**

> "The reviewer later reported that the advisory script and output files were last modified at 11:00:20 and 11:00:27 AM ET, not about 10:59 AM ET. The reviewer's scope-tightening message was issued during its 11:00 AM ET turn. Whether the computation preceded that message cannot be confirmed, so the word 'preceded' in the quoted disclosure is unverified. Artifact hashes: script 0e634895..., output 1f99c5ed.... The run remains an out-of-spec ADVISORY computation and does not support any label."

This errata records that disclosure. It does not add the advisory script or its output, and it does not treat that run as frozen validation.
