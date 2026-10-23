# Erratum 1 to CNA confound/sham section (CNA)

Date: 2026-10-23, 10:40 AM ET. Additive only. Amends the reading of trackB_instrument_validation_scope_CNA_confound_sham_X1X5_v1.md (sha256 377f99ba…). The original file is not edited.

Reason: the Lead's ruling (adopted in merged scope v1 §6.1, 7b9bf34d…) bars AVAILABLE and UNAVAILABLE as confound-row labels. My section used UNAVAILABLE in four places. They are replaced as follows:

| CNA file line | Was | Now |
|---|---|---|
| L44 (Q-CAUSE row (e), LIM) | "UNAVAILABLE on LIM" | LIM follows §6.1: PASS, FAIL, or CONFOUND NOT REALIZED, where CONFOUND NOT REALIZED leaves specificity UNRESOLVED |
| L60 (Q-LEARN expected pattern) | "Q-LEARN is NOT MET or UNAVAILABLE" | "Q-LEARN is NOT MET. If RAND-INIT or the architecture-only confound is not realized, the row is CONFOUND NOT REALIZED and specificity is UNRESOLVED" |
| L71 (IGN row (e), IGN-LIM) | "UNAVAILABLE on IGN-LIM" | as L44 |
| L108 (freeze list) | "BOUNDARY/UNAVAILABLE rules" | "BOUNDARY and CONFOUND NOT REALIZED rules" |

In every case, an UNRESOLVED row blocks Stage 0 the same way a FAIL does (merged scope v1 §6.1).
