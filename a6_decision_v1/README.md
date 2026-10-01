# Bounded A6 gate-decision package

Analytic/MILP discovery only. No gradients, training, organism simulation or
new architecture family. [Protocol](PROTOCOL.md) and [contract](contract.json)
are frozen before discovery. Historical Phase III-B verdict B is unchanged.

The question is existence of ONE legal shared width-56 R9 satisfying the
complete [joint-and-specialist gate](../SHARED4_STAGE_A_GATE_v1.md), not the exact
global optimum. The [older bracket](../SHARED4_STAGE_A_STATUS_v1.md) remains valid
until a separately certified result changes it.

## Files and meanings

- `baseline_hashes.json`: all 7,326 protected tracked inputs. Only the landing
  README and prospective board metadata may change.
- `lemmas.json`: independent integer replay of conditional S1 slope exclusion,
  strict risk lattice and relaxed-S2 component-wise dominance.
- `*_start.json`: immutable consumption of one of the six approved jobs.
- `*_result.json`: parent resource/watchdog disposition, not a mathematical proof.
- `*_root.json`: exact dual proposals and numerical diagnostics. The exact
  arithmetic checker determines which bounds are valid.
- `*_worker.json`: solver diagnostics/cuts; solver success or infeasibility alone
  never certifies PASS or FAIL.
- `*_candidate.json`, when present: actual finite parameters and certification
  attempts. Lookup mappings are never inputs to the runtime graph.
- `decision.json`: final bounded-effort outcome; absent means not yet finalized.
- `independent_replay.json`: separate solver-free replay and preservation audit.

F1 uses continuous count-level mixtures, because equal-count ordered histories
can produce different messages and different specialist tradeoffs. Before F2
ran, the [exact gate reduction](../A6_GATE_REDUCTION_v1.md) proved the full gate
equivalent to its joint threshold, permitting scalar count-dominance and a
compact factorized master. These are impossibility-search relaxations, not legal
recurrent witnesses. F3 is a fixed-head/bounded-quadratic discovery template,
never a whole-family lower bound.

**Final outcome: UNRESOLVED.** See [the bounded report](../A6_GATE_DECISION_v1.md).
The effort is closed; mathematical existence remains open and training blocked.
Five slots completed and one audited interruption consumed the sixth. Preserve
the [resource erratum](continuation_v2/RESOURCE_ERRATA.md); unknown node use is not
zero. The successor resource/compact sources were separately frozen before their
four jobs.

For an affine binary head with nonpositive local-bit slope, the permitted
policies are `00`, `10`, `11`, with conditional risks `q`, `4/5`, `1-q`.
The best two-common-reading risk is `1/5`; thus S1 strict competence requires
positive slope. This statement uses the mathematical affine semantics of the
[frozen class definition](../R9_FUNCTION_CLASS_v1.md), not floating-point
parameter-bit-pattern enumeration. Constructive certification additionally
requires rigorously positive float32 decision margins and real graph agreement.

Component numerators have denominator `6250000000`. S1/S3 numerators are
multiples of 50, S2 is integer; exact strict maxima are respectively
`1249999950`, `1124999999`, `3124999950`. The joint numerator maximum is
`3452708960` on denominator `18750000000`. Solver tolerances are not these
strict thresholds; every proposed candidate is evaluated exactly.

## Read-only replay

From the repository root:

```powershell
python -B -m pytest a6_decision_v1 shared4_v1 r10a_v1 phase3b_r10_v1 -q
python -B -m a6_decision_v1.verify
python -B -m a6_decision_v1.independent_replay
python -B -m a6_decision_v1.preservation a6_decision_v1\baseline_hashes.json --check
```

Independent replay verifies frozen source/input bytes and actual evidence; it
does not require the old commit to remain HEAD and never authorizes execution.
The supervisor retains its strict execution HEAD/interpreter/dependency lock.
Do not bypass that lock or rerun consumed jobs after a later commit.
The frozen predecessor [runner](runner.py) and [disposition helper](decision.py) are historical implementations,
not the current continuation/publisher. The canonical decision was published by
[continuation publisher](continuation_v2/finalize.py); independent replay dispatches to each actual frozen
formulation. Never regenerate a successor result using the predecessor model.

The approved search is at most three formulations/six serial CPU jobs,
100,000 integer nodes each, 900-second worker watchdog, 4 GiB committed-memory
job limit and one solver thread. These are cutoff values, not completion
estimates. Windows Job Objects terminate only this supervisor's assigned worker
tree. Unreported node counts remain unknown, not zero. Committed memory is not
a measurement of physical memory traffic, energy or architectural efficiency.

Closing an exhausted effort as UNRESOLVED does not close the mathematical
question or permit Stage B. PASS would only release consideration of a separate
prospective training protocol. FAIL needs full-family proof coverage.
