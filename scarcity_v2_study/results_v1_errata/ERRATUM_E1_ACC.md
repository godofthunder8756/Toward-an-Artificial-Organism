# ERRATUM E1 — ACC label

Additive correction to the scarcity_v2 v1 results. The frozen protocol, freeze commit `16e974a55348f801e1117b3ee2dae41967a609a2`, and `scarcity_v2_study/results/` are unchanged. No search was rerun. The recomputation is `recompute_v2.py`.

## Ruling

ACC’s primary verdict is REJECT-SIG under §7.2 precedence. Every positive decision cell has a certified complete optimum set and is SIG-UNDEFINED. The independently established §7.3 REJECT-NARROW finding remains valid: the first storage bin contains no positive cell. Neither finding rejects the ACC role or C3.

These are two downstream findings, not a choice between them. The signature needs redesign for identification, and the declared breadth criterion separately fails. The sentence that the §7.3 record is preserved does not erase the precedence rule (REJECT-ABSENT, then REJECT-SIG, then REJECT-NARROW). Repairing the signature would not repair the failed breadth criterion.

The v1 file `results/verdicts.json` records `REJECT-NARROW(ACC)`, and `verdicts.py` still forces that label when the first bin is clear and a later bin is positive. That code is part of the frozen implementation and is not edited. The corrected primary label is the §7.2 standard rule applied to the same records.

## Recomputation

Storage-attributed ACC uses the clean unpaid decision cells. All three bins are fully resolved.

| Bin (K / 8) | Cells | CERT-POS | Qualifying | UNRESOLVED |
| --- | --- | --- | --- | --- |
| (0, 1/4] | 8 | 0 | 0 | 0 |
| (1/4, 1/2] | 8 | 3 | 0 | 0 |
| (1/2, 1) | 4 | 2 | 0 | 0 |

The five positive decision cells, each with a complete optimum list (`truncated` false):

| Cell | Gap | Signature | Optima |
| --- | --- | --- | --- |
| clean, v = 1/3, r = 5/8, K = 3 | 1/48 | SIG-UNDEFINED | 12 |
| clean, v = 1/3, r = 3/4, K = 3 | 1/24 | SIG-UNDEFINED | 12 |
| clean, v = r = 3/4, K = 3 | 1/192 | SIG-UNDEFINED | 12 |
| clean, v = 1/3, r = 5/8, K = 6 | 1/48 | SIG-UNDEFINED | 42 |
| clean, v = 1/3, r = 3/4, K = 6 | 1/24 | SIG-UNDEFINED | 42 |

`_standard("ACC")` returns `REJECT-SIG(ACC)`: every CERT-POS decision cell is SIG-UNDEFINED, every decision value is resolved, and the controls pass. The separate breadth test also holds, so REJECT-NARROW remains established: bin (0, 1/4] has no positive cell, and a later bin does.

SIG-UNDEFINED here is operator unavailability on the certified positive optima, not an observed null response to an applicable intervention. It is not a claim about every codebook with K ≤ 6, and it is not a claim about every possible ACC intervention.

Corrected labels: primary `REJECT-SIG(ACC)`; retained `REJECT-NARROW(ACC)`.
