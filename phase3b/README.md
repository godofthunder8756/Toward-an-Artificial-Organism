---
description: Phase III-B H15 pretraining implementation scope and remaining STOP conditions
ms.date: 2026-09-28
---

# Phase III-B H15 pretraining implementation

This package is an **unscored, provisional H15 implementation**. Import,
unit tests, and `preflight()` do not train neural arms or create a results
directory. The old Phase III and organism artifacts are untouched.

The candidate and R1/R2/R3/R4/R8/R9 use independent learnable whole-arm
graphs. R4 sees only a public, history-independent route. Its planned
training round-robin exposes each source equally, and the route search uses
cached per-context losses from the training histories, with context 3
assigned by the predeclared fallback. R9 additionally has an exact candidate
clone subfamily, checked for all 256 sensory histories, eight local-bit
triples, and four decision contexts. That copied model is never scored as
an independent win. R5/R6/R7 are evaluator-only **EXTERNAL** controls.

`preflight()` checks the H3 map collision, exactly eight legal words, wiring
isolation, R9 clone, whole-arm parameter limits, and observed linear forward
MACs before a fit is allowed. The evaluation API and the independent raw
artifact auditor are present but are not invoked by tests. The primary gate
uses integer episode sums and all six independently trained comparators.
I1-I7 are diagnostic hooks; I2/I6 have out-of-band no-message readouts, and
I4/I5 are separately trainable frozen-encoder diagnostics, never intact wins.

## STOP before engineering or finals

* No execution freeze, recorded complete manifest, hashes, signed source
  snapshot, reserved fresh results directory or H16 authorization exists.
  `fit()` and engineering selection require an explicit matching engineering
  authorization; there is deliberately no final-training entry point.
* Linear MACs, trainable parameters and recurrent-state bytes are counted.
  An unscored synthetic CPU operator profile now reports forward/backward,
  loss, clipping and AdamW operator calls, sampled FLOPs, torch-reported
  allocation, optimizer state and OS process peak on a throwaway model.
  No scientific episode is scored. Torch allocation is not physical bus
  traffic, and the high-water process peak is not an isolated model peak.
  Full-run training compute, actual bandwidth, and run-specific parity
  remain unaudited. The resource-meter gate
  still hard-stops fitting even if a caller claims authorization.
* A preflight-only snapshot can pin the full Python source and design-chain
  hashes (including replay tests), model grids, versions,
  the H3 result and R9 clone count, and the raw auditor now demands its
  digest. The snapshot is exclusive-write and detects drift, but it is
  neither cryptographically signed nor an engineering or final approval.
  Engineering training accepts only declared seeds 0-3; final training has
  no entry point. Source and freeze review remain H16 obligations.
* The prescribed secondary 2,048/8,192-parameter and 1/4/4-times-compute
  Pareto sweeps and equal-capacity 2,048/4,096 transfer study are not
  implemented. H10 source-state decoding and information diagnostics, the
  I1 matched-history report, full I1-I7 scored comparison/negative-control
  report, and optional R10 certificate also remain open.
* H3's Bayes map is cross-checked against the implemented loss ledger for
  both local-bit values and every prespecified positive-support belief case.
  H3 is a scarcity statement, not proof of architectural superiority over
  R9 or full belief broadcast.
* The raw audit checks sources, costs, checkpoints, actions, words, component
  losses, seed family, and the exact sign gate. Independent kernel-level
  resource profiling, frozen configuration/hash attestation and a fresh
  results-directory policy still need independent H16 audit before finals.
* The R9 constructive clone has matched outputs, parameters and forward
  linear MACs. Independent R9 training and its optional port-partitioned
  unrestricted-code sweep have not run. Do not count cloning as a win.

No scored engineering fits, neural finals, protocol revisions, or claims of
an H15-complete execution freeze are made here.