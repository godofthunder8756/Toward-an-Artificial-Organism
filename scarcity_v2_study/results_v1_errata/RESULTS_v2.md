# scarcity_v2 results, v2 correction

Additive correction of the v1 labels. Freeze commit `16e974a55348f801e1117b3ee2dae41967a609a2`. Results commit `5fa6571023941af97fa95638d187e04c191aaaad`. The protocol, the freeze note, and every file under `scarcity_v2_study/results/` stay byte-identical. No optimization was rerun. Labels below were recomputed from those outputs plus the E2 certificate (`recompute_v2.py`). Cell values that this file does not restate are the v1 values.

The recomputation agrees with errata E1, E2, and E3. Nothing in it assigns a different family label from those rulings. Notes that are easy to misread as disagreements are at the end.

## Corrected labels

| Quantity | Corrected label |
| --- | --- |
| SEL | ADMIT, certified on unpaid cells |
| ACC | REJECT-SIG primary; REJECT-NARROW also established and retained |
| UPK | ADMIT, ample storage, scarce upkeep |
| UPK_cue | ADMIT, ample storage, scarce upkeep |
| UPK_ev | Descriptive |
| ROUTE | ADMIT, the channel formulation of the corresponding SEL problem |
| ADAPT | VALUE-ONLY |

v1 recorded ACC as REJECT-NARROW and recorded UPK and UPK_cue as ADMIT without tagging the unresolved K = 1 controls. E1 and E2 are the corrections. SEL, ROUTE, and ADAPT keep the same family words, with the scope notes below.

## Claim ceiling

In W2′, exact optimization and analytic certificates establish value pressure and representability for cue-dependent selection under unpaid storage constraints, its equivalent channel-limited routing formulation, and cue-dependent durability allocation under a scarce upkeep budget at ample storage. Qualifying optimal policies exist in each declared admission bin. Acquisition, causal use in a developed system, and necessity beyond the declared rival classes remain unestablished.

The certificate establishes existence inside the specified mathematical policy classes. It does not establish those roles in a learned model or a developed system. Computed intervention effects characterize the specified policies.

## SEL

ADMIT(SEL). Controls pass, and each storage bin has a CERT-POS cell with a ROBUST optimum. The witnesses are unpaid cells. Paid small-K SEL was not searched (`OMISSION_MANIFEST.md`). That omission does not empty a bin.

## ACC

Primary verdict REJECT-SIG(ACC), under the §7.2 order REJECT-ABSENT, then REJECT-SIG, then REJECT-NARROW. All five positive clean decision cells are SIG-UNDEFINED, with complete optimum lists. REJECT-NARROW is also established: bin (0, 1/4] contains no positive cell, and later bins do. Neither finding rejects the ACC role or C3. Detail, including the five gaps, is `ERRATUM_E1_ACC.md`.

`verdicts.py` still returns REJECT-NARROW(ACC) on these records, because the v1 implementation treated the §7.3 sentence as an override. That function is unchanged. The corrected primary label is the standard rule, reported here.

## UPK and UPK_cue

ADMIT(UPK) and ADMIT(UPK_cue), for ample storage and scarce upkeep.

Before E2, tagging the §5.5 K = 1 control makes both verdicts UNRESOLVED: 8 decision-bearing UPK cells and 4 decision-bearing UPK_cue cells (v = 3/4) are unresolved. The positive ample cells are not the problem. E2 certifies every K = 1 upkeep record, primary and secondary, all three quantities, 96 records, as DEGENERATE with gap 0. After that certificate, rule 4 holds and both admissions return. The qualifying counts stay 14 in B_up = 1 and 20 in B_up = 2.

The cited clean primary values, δ = 1/2, v = 3/4, are 5/96 at B_up = 1, K ≥ 26, and 5/192 at B_up = 2, K ≥ 16, both ROBUST. At r = 5/8 the same cells are 5/64 and 5/128, also ROBUST. UPK_cue equals UPK on these 34 cells. They reproduce the analytic predictions. They are upkeep-budget pressure at capacities where the displayed policies fit, not a storage-scarcity interaction. Detail is `ERRATUM_E2_K1.md` and `ERRATUM_E3_EXECUTION.md`.

## UPK_ev

Descriptive, not an admission role. On the 34 ample clean primary cells above, UPK_ev = 0. The graded §5.4 report is positive: UPK_ev = 33/4096, with UPK = 33/4096 and UPK_cue = 0. Elsewhere, cells that the closed forms do not cover stay UNRESOLVED and NOT-RUN, except K = 1, which E2 sets to 0. No clean upkeep cell in the frozen outputs has a positive UPK_ev.

## ROUTE

ADMIT(ROUTE). Bins L = 2 and L = 3 each have qualifying cells, and the controls pass.

A decoder’s L messages define L action vectors; selecting a message is selecting a codeword. With separate consumer channels and symmetric tasks, the objectives separate. Report ROUTE as the channel formulation of the same selection result, not independent evidence for multi-consumer coordination.

On the frozen outputs that check is exact: all 54 route cells have an unpaid SEL cell at K = L with the same evidence law, and all 54 gaps are equal. The match includes the graded cells and a = 5/6. Equality of the numbers is the check. The claim of equivalence is the identity of the two selection problems, so ROUTE is not a second, independent admission.

## ADAPT

VALUE-ONLY. There is no response property and no admission bin. Controls that were run are certified zero. This is not a positive adaptation finding.

Both unresolved experimental intervals are reported:

| Condition | K | result | execution | Interval | T_const | T2 |
| --- | --- | --- | --- | --- | --- | --- |
| SWITCHING | 64 and 125 | UNRESOLVED | RUN | [0, 105/3968] | 119/128 | 3739/3968 |
| UNKNOWN-FIXED | 64 and 125 | UNRESOLVED | RUN | [0, 5/384] | 119/128 | 367/384 |

T2 and T3 are adaptive trackers. T3 was not run, because H = 3 was not swept. The lower end 0 follows from class inclusion: the tracker is a feasible member of `full_B`, so the gap cannot be negative once that policy is available. A lower bound of zero does not itself show that adaptation failed. The restricted search found no improvement over the specified trackers. Wrong-bit and dash signalling encoders were not enumerated, so the upper end stays open. The other unresolved ADAPT cells were not searched (`execution = NOT-RUN`).

## Execution and self-tests

Every record’s `result` and `execution` are in `records_v2.json`. Unsearched cells are UNRESOLVED and NOT-RUN. No timeout is asserted for them. The accounting is `ERRATUM_E3_EXECUTION.md`. The omissions are `OMISSION_MANIFEST.md`.

46 of 46 executed self-tests passed, and none failed. That sentence does not show that every required control was covered. The §5.5 K = 1 upkeep control was not among the 46. E2 covers it.

## Agreement with the errata

The recomputed labels are the table at the top. In particular:

- The standard precedence rule returns REJECT-SIG(ACC), and the first-bin test still establishes REJECT-NARROW.
- After E2, `control_failures` is empty for UPK and UPK_cue, and both verdicts are ADMIT. Before E2 they are UNRESOLVED.
- No frozen K = 1 upkeep record contains a nonzero gap, so the certificate does not overwrite a certified positive.
- Route and SEL gaps match on all 54 paired cells.
- The longest recorded search is 8532 ms, under the 4-minute full-class limit.

Two implementation facts are not label disagreements. `verdicts.py` still emits REJECT-NARROW(ACC) if called; the corrected primary label is this folder’s recomputation, not a silent edit of that file. The B_up = 0 experimental pin in the implementation is K ≥ 27, while the executed ADAPT grid does not contain K = 27; the neighbouring executed cells are K = 26 (NOT-RUN) and K = 48 (CERT-ZERO).
