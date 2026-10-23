# ERRATUM E2 — K = 1 upkeep certificate

Additive correction. No upkeep search was rerun. The certificate is the class inclusion below, applied to the frozen cell list.

## Ruling

At K=1, the sole reachable I-phase configuration fixes all answer fields and durability marks independently of evidence and cue. Every admissible full policy therefore also belongs to fixed_upkeep and cue_blind_upkeep. The three optima coincide, so UPK=UPK_cue=UPK_ev=0. All applicable K=1 upkeep records are corrected to DEGENERATE with certified zero gaps and included in control accounting. These certificates restore ADMIT(UPK) and ADMIT(UPK_cue).

## Certificate

An S-DIRECT policy sends each evidence-and-cue pair to an I-phase configuration. At K = 1 that budget admits one configuration, so the image cannot depend on the input. `fixed_upkeep` and `cue_blind_upkeep` are the constant-policy subclasses of `full`. At K = 1 every full policy is constant, so the three feasible sets are equal and the three optimal values are equal. The gaps are structural zeros. The status is DEGENERATE, which §7.2 counts as zero. `k1_certificate()` in `recompute_v2.py` is this argument; it does not enumerate policies.

The certificate covers every K = 1 upkeep record: primary and secondary, B_up ∈ {0, 1, 2, 3}, and all three quantities. That is 32 cells × 3 quantities = 96 records. It is not limited to the eight decision-bearing UPK cells.

## What v1 had already certified

No frozen K = 1 upkeep gap is a nonzero rational. Rows that v1 left UNRESOLVED had gap null. Rows that v1 had already proved were gap 0. The certificate does not contradict any existing number. It replaces the unresolved rows and relabels the existing zeros as DEGENERATE, because at K = 1 the classes coincide.

| Quantity | v1 status | Decision-bearing | Count |
| --- | --- | --- | --- |
| UPK | UNRESOLVED | yes (δ = 1/2, B_up ∈ {1, 2}) | 8 |
| UPK | UNRESOLVED | no (δ = 1/4, B_up ∈ {1, 2}) | 8 |
| UPK | CERT-ZERO | no (B_up ∈ {0, 3}) | 16 |
| UPK_cue | UNRESOLVED | yes (v = 3/4) | 4 |
| UPK_cue | CERT-ZERO | yes (v = 1/3, UPK-C0) | 4 |
| UPK_cue | UNRESOLVED | no (δ = 1/4, v = 3/4) | 4 |
| UPK_cue | CERT-ZERO | no | 20 |
| UPK_ev | UNRESOLVED | yes | 8 |
| UPK_ev | UNRESOLVED | no (δ = 1/4) | 8 |
| UPK_ev | CERT-ZERO | no (B_up ∈ {0, 3}) | 16 |

After the correction, all 96 records are `result = DEGENERATE`, `gap = 0`, `execution = PROVED`, `control = K=1`. The per-record list is `k1_corrections.json`.

## Control accounting, rule 4

§7.2 requirement 4: no control is UNRESOLVED. §5.5 lists K = 1 as DEGENERATE for all roles. v1 did not tag the unresolved K = 1 upkeep cells, so the recorded `ADMIT(UPK)` and `ADMIT(UPK_cue)` were not control-complete. The positive witnesses are untouched.

Tagging the decision-bearing K = 1 rows and rerunning the same control check, before the certificate:

| Role | Failures | Verdict |
| --- | --- | --- |
| UPK | 8 UNRESOLVED | UNRESOLVED |
| UPK_cue | 4 UNRESOLVED | UNRESOLVED |

Tagging every K = 1 row, including report-only δ = 1/4, gives 16 UPK failures and 8 UPK_cue failures, and the same UNRESOLVED verdicts. The protocol freezes δ = 1/4 as report-only, so those rows cannot change a label. They are still certified and counted. The decision-bearing rows alone are enough to block admission before the certificate.

After the certificate, both failure lists are empty. The bins are unchanged in their qualifying cells: B_up = 1 has 14 CERT-POS ROBUST cells, B_up = 2 has 20. Unresolved non-control cells remain below K_suff (32 in bin 1, 22 in bin 2) and do not remove a bin that already qualifies.

Recomputed verdicts: `ADMIT(UPK)` and `ADMIT(UPK_cue)`. Rule 4 holds. The restoration agrees with the ruling.
