# SUB-A0 engineering execution and review v1

2026-10-02. **ENGINEERING STOP: maintenance was not load-bearing.**
No confirmatory A0 verdict, Phase A license or final run.

## 1. What was executed

The user's "Execute and review it" was implemented as bounded CPU engineering
under the [additive execution specification](SUB_A0_ENGINEERING_PROTOCOL_v1.md),
not an automatic human approval of a final source freeze.
One fixed candidate/development configuration, engineering seed 0, nine arms,
1,024 ticks/arm. Planned engineering seed 1 was NOT_RUN because the prospectively
specified early-stop rule fired after all seed-0 arms completed.
No seed was discarded or restarted, no fault/endpoint was retuned, and no
confirmatory seed 1000-1031 was used.

The [implementation](sub_a0_v1/model.py) is a small ordinary recurrent local
allocator with 894 live learned scalars: 768 task traces and 126 performing
repair traces. Its 42 unique performing coefficients all compute proposals
and are writable by the same live updater. All 3,576 persistent recurrent
state scalars also receive faults. The task is a 256-bit acquired random table,
with conventional redundant retrieval. It is not a neural-necessity assay.

Externally supervised development used task binary cross entropy only:
128 acquisition updates and 128 16-step meta-development trajectories. External
optimizer state was absent from the continuing assay. This is declared
task-trained instrumental machinery, not spontaneous priorities.

Source/config/dependency provenance was captured before fits in the
[manifest](sub_a0_engineering_v1/manifest.json). This is an engineering
provenance snapshot, not an externally preregistered confirmatory freeze.

## 2. All arms, all executed seeds

Results below are for the ONE executed engineering seed, not independent
replications across ticks.

| Arm | Whole-horizon accuracy | Last-quarter accuracy | Allocation A |
| --- | ---: | ---: | ---: |
| Candidate SHAM | 1.000000 | 1.000000 | 0.062524 |
| Candidate PRESSURE | 1.000000 | 1.000000 | 0.063515 |
| No writes, same damage/proposal compute | 1.000000 | 1.000000 | 0, NO_ALLOCATION |
| Intercept R writes, charge attempts | 0.996521 | 0.986084 | -1.000000 |
| Uniform allocation, live proposals | 1.000000 | 1.000000 | 0.004170 |
| Fixed round-robin allocation, live proposals | 1.000000 | 1.000000 | 0.000119 |
| Disagreement threshold, live proposals | 0.781189 | 0.726318 | -0.306617 |
| EXTERNAL live median repetition code | 1.000000 | 1.000000 | 0.005219 |
| Immortal reference | 1.000000 | 1.000000 | 0.062524 |

The [full results](sub_a0_engineering_v1/results.json), acquired numeric
checkpoint, development losses, arm records and 9,216 raw per-tick JSONL rows
are preserved in the [engineering archive](sub_a0_engineering_v1/).
The EXTERNAL arm is a supplied decoder, not evidence for endogenous
performing repair. Uniform/fixed/threshold controls reuse the live updater;
the threshold's failure is not a strongest-rival win.

### Registered allocation signature

- `A_PRESSURE = 0.06351509703873362`, below strict 0.10.
- `A_SHAM = 0.06252427309955892`.
- `D = 0.0009908239391746981`, below strict 0.10.
- Engineering allocation signature: **fails for seed 0**.
- The prospective 23/32 gate was **NOT evaluated**. No p-value or replicated
  hypothesis rejection is claimed from this one seed.

There is modest R enrichment even in sham, and almost no damage-induced
increase. Extra R writes cannot be interpreted as the hypothesized contingent
priority. Initial task/repair absolute coefficient means were 4.44918 and
0.27797: the common absolute noise scale implies unequal fractional stress.
This scale confound is disclosed, not credited as an endogenous effect.

## 3. Functional tests and decisive STOP

Candidate pressure minus no-write accuracy is exactly **0**.
The no-write arm already retains every scored answer across all planned ticks.
The fault law damages stored numeric values but does not make preservation
of their task-relevant signs depend on repair in this pilot.

The engineering STOP `NO_WRITE_TRIVIALLY_RETAINS_SKILL` therefore fired.
Continuing training or running seed 1 under the same regime would not repair
this interpretation. Increasing fault dose after observing it is not permitted
as a covert extension of this run.

R-write interception lowers last-quarter accuracy by **0.013916**, below the
proposed 0.05 causal margin. Since completely disabling writes performs
perfectly, even this small difference does not establish task-preserving
repair. A live updater becoming harmful when its R writes are blocked is a
remaining ordinary explanation, not evidence of constitutive maintenance.

All six capacity probes (three candidate, three interception) have:

`before = immediate = after = 1.0; gain = 0`.

Deleting one of three sign-consistent task replicas did not create an observable
accuracy deficit. The capacity contrast is **ceiling-limited/unidentifiable**,
not evidence that repair capacity survived. This independently meets the
specified probe STOP, although the primary no-write STOP was logged first.
Complete deletion of all T/R/hidden state remains zero and cannot reconstruct
the arbitrary table without a content source.

## 4. Implementation and evidence review

### Boundary

The [frozen boundary](SUB_A0_SUBSTRATE_BOUNDARY_v1.md),
[design](SUB_A0_DESIGN_v1.md), [prior art](SUB_A0_PRIOR_ART_v1.md) and
[allocation registration](SUB_A0_ALLOCATION_REGISTRATION_v1.json) remain
byte-identical to their recorded hashes. No learned performing parameter is
kept in a protected runtime model: proposals read current damaged R traces.
All performing coefficients can be self-written. Labels appear in development
and evaluator scoring, not in the proposal API.

Generic arithmetic, peer wiring, coefficient addressing, recurrent execution,
redundant retrieval and uniform write physics remain supplied. This execution
does not establish unqualified production closure or autonomous organization.

### Review and discovered artifact defect

A separate read-only code review reported no significant logic issues in
the initial execution source. The independent raw-file audit then found the
Windows LF/CRLF hash-definition defect. It was flagged BEFORE accepting the
raw audit. See the additive [erratum](SUB_A0_ENGINEERING_ERRATA_v1.md).

The recorded `trace_sha256` hashes LF-normalized content, not physical CRLF
bytes. Both are now verified and separately recorded; no original trace,
manifest, source or checkpoint was changed. This does not alter observations.
The review is not external laboratory replication.

### Validation

- **56 distinct tests passed**: 22 engineering, 9 independent-audit and 25
  earlier substrate fixture regressions.
- [Fresh-instance replay](sub_a0_engineering_v1/replay.json) passed all nine
  arms without retraining, reproducing metrics and canonical trace hashes.
- [Independent raw/source audit](sub_a0_engineering_v1/independent_audit_v1.json)
  reconstructed all 9,216 clocks, queries, predictions, correct counts,
  accepted-write totals, opportunity denominators and enrichment values.
  It verifies physical file hashes separately from normalized trace hashes.
- Original execution source hashes and existing tracked scientific record
  remain unchanged. The Phase III-B B verdict and A6 UNRESOLVED are untouched.

## 5. Resources and exclusions

CPU-only PyTorch 2.7.0, NumPy 2.2.6, Python 3.13.3, one configured PyTorch
intra-op thread. No GPU and no scale-up.

| Quantity | Observed/accounted value |
| --- | ---: |
| Owned-worker launch-to-exit wall | 27.478 s |
| Internal run wall, excluding Python startup | 21.085 s |
| Development wall | 9.166 s |
| Worker process lifetime peak working set | 276,295,680 bytes = 263.50 MiB |
| Development updater linear forward MACs | 65,912,832 |
| Nine assays plus capacity probes, updater linear forward MACs | 299,697,408 |
| Complete-deletion control, updater linear forward MACs | 514,944 |
| Fresh replay of nine assays plus probes, linear forward MACs | 299,697,408 |
| Development backward invocations | 256: 128 acquisition + 128 meta-development |

Linear MACs are computed from the executed fixed dense graph and actual call
counts, not measured hardware operations. Exclude nonlinearities, optimizer,
fault generator, sorting, writes, task reductions, tests and audit overhead.
Backward MACs, physical memory traffic and hardware energy are **unmeasured**;
backward invocation count is not a substitute. Peak working set is the worker
process lifetime, not isolated per-arm or whole-machine usage.

The [owned-process watchdog](sub_a0_engineering_v1/watchdog.json) enforced a
1,200-second launch wall cap; exit code 0, no timeout. No process outside the
owned worker was terminated. Original discovery/final budgets were not reused.

## 6. Bounded verdict and next decision

**ENGINEERING_STOP / REGIME_DOES_NOT_REQUIRE_MAINTENANCE**, with an additional
**CAPACITY_PROBE_UNIDENTIFIABLE** finding.

This ends execution of the specified task/fault/probe/development combination.
It does not prove learned repair impossible, nor reject the population A0
hypothesis by a confirmatory sample. No Phase A license is earned.
No finals should be frozen or run for this configuration.

The shortest justified next action is human review of these negatives.
If this line is reconsidered, the proposal must establish task-relevant damage
and an observable repair-capacity deficit BEFORE further training, explicitly
justify any revised fault/task/readout model, preserve the present failure,
and use a new version and new approval. That is a changed question/configuration,
not an automatic A0.1 gate or permission to keep optimizing this result.

No homeostasis, survival, metacognition, self-model or consciousness evidence
was obtained. Ordinary acquired table storage was sufficient in the tested
regime. The weakest explanation is not rescued because a threshold control
performed badly.

## Replay commands

```powershell
python -m pytest sub_a0_v1\test_engineering.py sub_a0_v1\test_audit.py sub_a_v1\test_skeleton.py -q
```

The original run/replay/audit entry points refuse to overwrite result records.
Their replay and audit records already exist. For a new review, inspect those
saved records or call the read-only auditor without writing another record:

```powershell
python -c "from pathlib import Path; from sub_a0_v1.audit import audit; print(audit(Path('sub_a0_engineering_v1'))['passed'])"
```

Do not rerun training into a renamed folder to evade the consumed pilot budget.
