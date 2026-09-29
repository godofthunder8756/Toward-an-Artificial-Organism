---
description: Phase III-B audited secondary frozen-core transfer results
ms.date: 2026-09-29
---

# Phase III-B frozen-core transfer v1

This is the [protocol](ACI_PHASE3B_PROTOCOL_v1.md)'s **secondary**
access-matched transfer study, not a primary result or a zero-shot
success claim. It began only after the [independent final audit](phase3b_results_v1/phase3b_final_audit_v1.json).
All seven final learned arms and 16 untouched final model seeds contributed
one frozen source representation. Their original head/state digests were
identical before and after each transfer fit. Every new readout had 780
trainable parameters, 2,048 separate training episodes (64 updates), one
new private factor-four sensor, and 4,096 disjoint evaluation episodes
per seed. R3 used its **predeclared specialist 0** only.

The final manifest SHA-256 is
`5ba90ee9e6f2d734b0ab2eadf9906edea30b52c66e24cf093dd802cd0b4091a9`.
The 112 per-seed records and their hashes are in the
[transfer index](phase3b_results_v1/transfer/transfer_index.json),
SHA-256 `a302b7f5fe2c0f23a7ad32863d1d74fff2de351ab1fe42e09468fe3dee4270af`.
An independent record validation checked every source tensor digest,
original-head byte identity, seed/stream, sample allowance, risk-curve
denominator, and intact consumer read bandwidth.

| Frozen source | Mean error at 0 new samples | Mean error at 2,048 samples | Intact read bits, excluding new sensor |
| --- | ---: | ---: | ---: |
| Candidate | 0.482056 | **0.254761** | 3 |
| R1 unlimited learned broadcast | 0.509903 | **0.193329** | 3,456 |
| R2 monolithic recurrence | 0.490677 | 0.308411 | 1,824 |
| R3 private specialist 0 | 0.488953 | 0.313309 | 1,024 |
| R4 fixed-selector workspace | 0.502045 | 0.246536 | 3 |
| R8 shared learned vector | 0.475403 | 0.397339 | 1,152 |
| Independently trained R9 eight-symbol code | 0.532837 | 0.251328 | 3 |

At 2,048 samples, R1 has lower risk than the candidate but reads much
more information per episode; it is not a three-bit bandwidth-matched
transfer win. R4 and R9 also match or modestly improve the candidate
with the same three-bit transfer interface. These descriptive results
provide **no candidate-exclusive representation-reuse advantage**.
The 0-sample row uses an untrained new random readout, not a zero-shot
deployment of a trained transfer classifier. The new head is trained;
the old representation and old heads are frozen. The risk curves are
secondary observations over the same 16 model seeds, not 4,096
independent replicates.

The extra 780 parameters, read bits, training-core and new-head MACs,
optimizer state, and evaluation work are disclosed separately in each
record. Logical tensor counts and process high-water memory are not
physical traffic, energy, or isolated per-model peak.
