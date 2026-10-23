# C-kappa oracle scope: Research Lead ruling on B2/B3 (additive to CKAPPA_SCOPE_GOVERNING_SET_RL.md 6a5e0f24)
Date: 2026-10-22 ~2:16 AM ET. Responds to the Delegate check db6012e9. Both fixes are adopted verbatim.

B2 (N3): "In N3, 'rank-deficient' means rank-UNRESOLVED only. A resolved lower-rank design (including sigma_1=0) is fitted minimum-norm and scored, and its rank and sigma_1 are reported."

B3 (replaces the addition at RL L11): "The sigma report uses the stacked Jacobian over the non-voided prefixes per fold. sigma_3/sigma_1 > 1e-6 there is handled as N4(i): integrity diagnosis, STOP, PIPELINE INVALID. Otherwise it is descriptive."

Non-blocking items, also adopted:
(a) Voided prefixes are labelled with E36-6's "RESTRICTED COMPARATOR NOT ADMISSIBLE" wording.
(b) The per-array hash file is written at draw time.
(c) The fit is computed from the same SVD that the rank check uses.

Governing set = 6a5e0f24 + this ruling. The SCOPE IS FROZEN. No further scope files.
