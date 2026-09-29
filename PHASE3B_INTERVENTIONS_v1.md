---
description: Phase III-B post-final secondary I1-I7 diagnostic results
ms.date: 2026-09-29
---

# Phase III-B intervention diagnostics v1

The intact primary result and [independent audit](phase3b_results_v1/phase3b_final_audit_v1.json)
were frozen **before** these diagnostics. This is not a new primary gate or
an independently trained rival comparison. The candidate's intact mean
held-out joint loss was **0.369509** over 16 final seeds and 4,096
episodes per seed. The final manifest SHA-256 is
`5ba90ee9e6f2d734b0ab2eadf9906edea30b52c66e24cf093dd802cd0b4091a9`.

The [separate post-final runner](phase3b_results_v1/phase3b_interventions_runner_v1.py)
has SHA-256 `f8b5672caf57a1860f8ee81115a9d0ccf6e1ab1bf1a55e4257c5fecd2711191e`.
Its [result summary](phase3b_results_v1/interventions/summary.json)
has SHA-256 `0e616b50a8c1a44e5a17d40d2bef34ea798cb869e175743e9dfb2a95fae0b0e0`.
The frozen pretraining helper only admitted engineering seeds for
diagnostic-head fitting. Rather than change the frozen primary code after
scoring, the separately hashed secondary runner applied its stated
optimizer, baseline, clipping and 8,192-episode allowance to each final
seed's **original training histories**. This implementation repair is
post-final and cannot validate a primary advantage. I7 used separately
generated paired histories at stream `40000 + seed`; that stream was set
in the secondary runner, not in the original frozen protocol.

| Diagnostic | Mean joint loss | Difference from intact |
| --- | ---: | ---: |
| I1: substitute address at read, best constant address 0 | 0.355373 | -0.014136 |
| I1: other addresses 1 / 2 / 3 | 0.360117 / 0.358520 / 0.362821 | -0.009392 / -0.010989 / -0.006688 |
| I2: trained out-of-band no-message readout | 0.355565 | -0.013944 |
| I3: force source upstream, addresses 0 / 1 / 2 / 3 | 0.364329 / 0.377793 / 0.357074 / 0.355835 | -0.005180 / +0.008284 / -0.012435 / -0.013675 |
| I4: four / eight / sixteen-bit expanded word | 0.364825 / 0.360975 / 0.346453 | -0.004684 / -0.008535 / -0.023056 |
| I5: newly trained unlimited frozen-state readout | 0.389915 | +0.020406 |
| I6: cut only S1 / S2 / S3 to trained blank readout | 0.350090 / 0.376963 / 0.367531 | -0.019419 / +0.007454 / -0.001979 |
| I7: replace port 0 / 1 / 2 / 3 state | 0.369443 / 0.369550 / 0.369509 / 0.369509 | -0.000066 / +0.000041 / 0 / 0 |

Lower loss is better. The "best" I1 row is **descriptive selection from
four interventions**, not a selected model, primary comparator, or new
confirmatory win. I4 and I5 use new trainable heads and altered read
bandwidth; I2/I6 use an out-of-band no-message readout, not a ninth legal
intact word. I5 worsening under a new readout does not imply information
itself is harmful. The R6 evaluator-only selector over fixed learned
contents reached mean loss **0.283744**; this is selection headroom, not
an autonomous rival. See the [external controls](phase3b_results_v1/phase3b_external_controls_v1.json).

Every one of the 352 variant/seed raw files retains per-episode component
losses, actions, word traces when applicable, both possible private-bit
action maps, and first divergence tick. An independent read-only
recalculation checked every stored loss against truth/actions, every
response map against observed actions, the no-op byte identity, unaffected
I6 heads, and identical actions wherever I7 left the word unchanged.
All checks passed. The intact/no-op replay was exact for every seed.

The changed words and consumer responses establish that the trained
candidate has a causal on-wire read path. They do **not** show a beneficial
competitive selector: several cuts and constant-address substitutions
improved intact loss, and port-2/3 replacements had no aggregate held-out
loss effect. The primary rival envelope remains decisive. Physical memory
traffic and isolated per-model peak were not measured; reported allocator
and process metrics must not be recast as those quantities.
