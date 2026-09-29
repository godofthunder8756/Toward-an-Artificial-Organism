---
description: Phase III-B implementation, audited results, and limitations
ms.date: 2026-09-29
---

# Phase III-B implementation

Import, unit tests, and `preflight()` do not train neural arms or create a
results directory. The separately authorized engineering and final runs
are complete; see the [completed status](../PHASE3B_STATUS_v2.md) and
[bounded verdict](../PHASE3B_VERDICT_v1.md). The old Phase III and organism
artifacts are untouched. See the
[resource contract](../PHASE3B_RESOURCE_CONTRACT_v1.md) for the binding
whole-arm caps, measured costs, and quantities that cannot be inferred from
allocator counts.

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
The separately hashed [post-final supplement](../PHASE3B_INTERVENTIONS_v1.md)
repaired the helper's engineering-only seed guard without changing this
frozen primary source.

## Execution and outstanding boundaries

* The execution-freeze and phase-specific engineering/final approval paths
  require signed, source-bound provenance. Both phases were separately
  approved and executed; `fit()` still rejects missing or invalid
  provenance. The final entry point does not run on import.
* Linear MACs, trainable parameters and recurrent-state bytes are counted.
  An unscored synthetic CPU operator profile now reports forward/backward,
  loss, clipping and AdamW operator calls, sampled FLOPs, torch-reported
  allocation, optimizer state and OS process peak on a throwaway model.
  No scientific episode is scored. Torch allocation is not physical bus
  traffic, and the high-water process peak is not an isolated model peak.
  Actual-run linear MACs, optimizer state and wall time are in the final
  manifest. Exact physical traffic and isolated per-arm OS peak remain
  unmeasured, not fictitious eligibility gates.
* A preflight-only snapshot pins Python source and design-chain hashes
  (including replay tests and the resource contract), grids, versions,
  the H3 result and R9 clone count. An additional exclusive execution
  freeze pins dependencies, endpoint, statistic and reviewer public key;
  signed engineering/final approvals must bind the same freeze. The
  preflight snapshot is not an approval. Engineering seeds are 0-3 and
  final seeds are 1000-1015; independent H16 review and H18 raw audit
  passed. A failed primary gate is a valid scientific negative.
* The prescribed secondary 2,048/8,192-parameter and 1/4/4-times-compute
  Pareto sweeps were not run. The 2,048/4,096 secondary transfer study
  completed for every final arm; see its [report](../PHASE3B_TRANSFER_v1.md).
  The separately versioned I1-I7 supplement scored all seven intervention
  families with negative controls. The H10 source-state, information,
  and H3 matched-history analyses are in their separate
  [post-final report](../PHASE3B_H10_DIAGNOSTICS_v1.md). The optional
  R10 certificate remains open as a **secondary limitation**, not a
  reason to exclude a primary rival or claim workspace value.
* H3's Bayes map is cross-checked against the implemented loss ledger for
  both local-bit values and every prespecified positive-support belief case.
  H3 is a scarcity statement, not proof of architectural superiority over
  R9 or full belief broadcast.
* The raw audit checks sources, selected configurations and engineering
  scores, checkpoint state and file hashes, costs, actions, words, component
  losses, seed family, and the exact sign gate. The fresh results-directory
  and signed freeze policy were independently reviewed before execution.
* The R9 constructive clone has matched outputs, parameters and forward
  linear MACs. Independently trained R9 ran on all final seeds; the optional
  port-partitioned unrestricted-code sweep did not. Do not count cloning
  as a win.

No Phase IV neural experiment or consciousness inference is authorized.