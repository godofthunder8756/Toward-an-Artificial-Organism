# ERRATUM E3 — execution scope

Additive correction of status wording. No search was rerun.

## Ruling

Unsearched cells retain scientific status UNRESOLVED and receive execution status NOT-RUN. No timeout is asserted for them. Nontrivial positive UPK certificates were obtained at ample capacity: K≥26 for B_up=1 and K≥16 for B_up=2 in the cited clean examples. These certify upkeep-budget pressure, not a storage-scarcity interaction. The qualifying values reproduce the protocol’s analytic predictions. Other cells resolved by separate zero proofs remain certified.

## Two fields

Every result record in `records_v2.json` has `result` and `execution`. There are 2266 records: the frozen unpaid, upkeep, route, and adapt cells, the three upkeep quantities on each upkeep cell, and the three-quantity graded upkeep report.

| execution | Meaning |
| --- | --- |
| RUN | A class search executed. An unresolved interval from that search stays UNRESOLVED. |
| PROVED | An analytic certificate, including E2 and the closed forms. Process time is not a search budget. |
| NOT-RUN | No class search was run, and v1 did not close the cell by a proof. |

`TIMEOUT` is not a status. The largest recorded process time in the frozen outputs is 8532 ms, on `route/graded/a=3/4/r=5/8/v=1/3/L=3`. The per-cell limits were 4 CPU-minutes for the full class and 6 for the rivals. No executed search reached either limit.

v1 `RESULTS.md` says that every search returned before its limit, and its unresolved-cell lines say the residual search was not exhausted inside the cell budget. The first sentence is true of searches that ran. The second sentence is withdrawn for cells that were never searched: they are `result = UNRESOLVED`, `execution = NOT-RUN`. The original results file is left byte-identical; this file is the correction.

## Counts

| Records | result | execution |
| --- | --- | --- |
| unpaid SEL, 238 | DEGENERATE 14, CERT-ZERO 176, CERT-POS 48 | RUN 238 |
| unpaid ACC, 238 | DEGENERATE 14, CERT-ZERO 98, CERT-POS 126 | RUN 238 |
| upkeep UPK, 544 | DEGENERATE 32, CERT-ZERO 336, CERT-POS 68, UNRESOLVED 108 | PROVED 436, NOT-RUN 108 |
| upkeep UPK_cue, 544 | DEGENERATE 32, CERT-ZERO 384, CERT-POS 68, UNRESOLVED 60 | PROVED 484, NOT-RUN 60 |
| upkeep UPK_ev, 544 | DEGENERATE 32, CERT-ZERO 404, UNRESOLVED 108 | PROVED 436, NOT-RUN 108 |
| ROUTE, 54 | CERT-ZERO 42, CERT-POS 12 | RUN 36, PROVED 18 |
| ADAPT, 101 | CERT-ZERO 71, DEGENERATE 8, UNRESOLVED 22 | PROVED 79, RUN 4, NOT-RUN 18 |
| graded upkeep report, 3 | UPK 33/4096, UPK_cue 0, UPK_ev 33/4096 | PROVED 3 |

The 18 ROUTE rows marked PROVED are the constructive zeros at L ≥ K_dec,base. The other route cells were enumerated.

The four ADAPT rows marked RUN are the subclass searches that returned an interval: SWITCHING at K = 64 and K = 125, interval [0, 105/3968], and UNKNOWN-FIXED at the same capacities, interval [0, 5/384]. K = 125 records process time 0 because that subclass evaluation is reused from K = 64; the interval is present, so the execution status is RUN. The other 18 unresolved ADAPT rows are NOT-RUN. One of them, SWITCHING at B_up = 1, K = 26, records 1 ms. That time is a tracker feasibility check. The equivariant search was not run, and no timeout is asserted.

## UPK scope

The admitted UPK and UPK_cue cells are ample-storage, upkeep-scarce. On the clean primary grid, v = 3/4, δ = 1/2:

| B_up | K | r = 3/4 | r = 5/8 | Cells | Signature |
| --- | --- | --- | --- | --- | --- |
| 1 | ≥ 26 | 5/96 | 5/64 | 7 + 7 | ROBUST |
| 2 | ≥ 16 | 5/192 | 5/128 | 10 + 10 | ROBUST |

UPK_cue equals UPK on all 34 cells, and UPK_ev is 0. These are the protocol’s closed forms (the r = 3/4 gaps 5/96 and 5/192, and the same algebra at r = 5/8). They certify pressure from the upkeep budget at capacities where the displayed policies fit. They do not certify an interaction between upkeep and scarce storage. Cells below K_suff that v1 left open stay UNRESOLVED and NOT-RUN, except the K = 1 rows closed by E2.

Existential admission can survive unresolved non-control cells once every bin already qualifies. It cannot survive an unresolved required control. E2 is what removes the K = 1 controls from that second case. The remaining NOT-RUN upkeep rows are not controls, and both bins already have qualifying optima, so they do not remove `ADMIT(UPK)` or `ADMIT(UPK_cue)`.
