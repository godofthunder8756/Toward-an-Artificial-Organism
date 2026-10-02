# SUB-A0 engineering execution v1

2026-10-02. The user's "Execute and review it" authorizes this bounded
engineering implementation/run. No confirmatory seeds or finals are authorized.
Historical boundary, design and allocation registration remain byte-identical.
This additive engineering specification resolves implementation choices before
any fits/results; it is not a human-approved final protocol freeze.

## Candidate and information

One conventional recurrent local updater, not a claim of architectural novelty.
256 independent fair acquired bits form a 16-by-16 cue/output task table.
The task is deliberately reducible to acquired table storage plus ordinary coding.

Each of the 256 task coefficients and 42 updater coefficients has three live
traces, totaling T=768, R=126 and 894 learned stored scalars (298 independently
optimized developmental coefficients). The updater has 3 inputs, 4 recurrent
units and 2 outputs: proposed delta and allocation score. Its input is a target
trace and its two live peers, not true faults, labels, bank names or original
values. Shared connectivity is supplied; effective operator coefficients are
the arithmetic mean of their three currently damaged traces. No host mean or
median is computed as a correction target: the live learned updater computes
all candidate proposal values.

All 42 learned performing coefficients, including biases and recurrent and
output weights, are addressable by the same updater and damaged. Each of the
894 destinations has a 4-unit persistent recurrent state, also damaged.
There are no protected learned heads, teacher or runtime optimizer states.
Physical coefficient addresses are independently permuted per seed; ties use
lowest physical address. Peer wiring is uniformly applied to all triplets.

Task retrieval averages three live traces and thresholds at zero; it is a
declared redundant readout, not maintained cognitive machinery or a neural-
necessity result. All corrective candidate writes still depend on live R.

## Developmental objective and fixed budget

CPU, one PyTorch thread, float32. Engineering seeds 0 and 1 only; no grid.
For each seed:

1. Fit initially neutral task coefficients on that individual's random table:
   128 Adam updates, learning rate 0.1, binary cross entropy only.
2. Optimize updater initialization through 128 development trajectories,
   16 damaged/self-writing steps each, Adam learning rate 0.01. Each
   trajectory starts from the SAME acquired task and currently optimized
   updater initializer. Final table binary cross entropy is the ONLY loss.
   No coefficient-restoration, allocation, survival or homeostasis objective.
3. Discard optimizer state at assay entry. No outer parameter updates occur
   during maintenance.

Step 2 is explicitly externally supplied, task-supervised meta-development,
not autonomous within-lifetime acquisition of priorities. Short development
trajectory restarts are not continuing assay life resets. The learned
initializer is never reloaded inside an assay branch.

Scores choose at most B=256 physical scalar destinations per tick. Deltas are
`0.05*tanh(output_delta)`. Training uses hard top-k forward choices with a
sigmoid straight-through mask gradient; the surrogate is reported, not an
exact gradient of discrete routing. Deployed evaluation uses hard choices only.
This learning budget can fail; no optimizer/grid extension is permitted here.

## Fault law and ordering

Use the draft starting law without tuning:
per-coordinate shrinkage `0.0002 * hidden_region_multiplier`, additive Gaussian
drift standard deviation `0.002 * multiplier`; multipliers in {1,4,16},
switch probability 1/200 per region per tick, 8 physical regions. With
probability 1/2000 choose a region and erase 10% of its coefficients independently.
R/T have the same physical marginal fault law; absolute fault scale is common.
R and T amplitude distributions may differ and are reported as a confound.
Persistent recurrent state receives the corresponding shrinkage/drift and
erasure, with independently drawn state noise.

The evaluator produces complete fault streams; proposer receives live state
only. Query/evaluator score precedes fault application, proposal and write.
SHAM disables faults but retains the same queries/opportunities.
PRESSURE and all decaying controls share the exact same fault/query stream.
H=1024, no assay resets, external labels/feedback or parameter reloads.

## Arms, probes and endpoint

For each acquired seed evaluate candidate SHAM, PRESSURE and immortal
reference; no-write, R-write-interception, uniform allocation, fixed
round-robin allocation, and a disagreement-threshold allocation rule all
use the SAME live learned proposals with the same vulnerability.
An explicitly EXTERNAL median repetition-code arm supplies correction values
from live traces, not original answers, and is not endogenous performing repair.
It is a reduction/reference, not an information-parity learned controller.

Candidate itself is a conventional recurrent allocator. This pilot does NOT
exhaust the stronger task-value-sensitive controller training envelope; thus
no strongest-rival win or Phase A license can be issued from engineering.
Keep all arm/seed failures. Metric definition and thresholds remain those of
the original allocation registration; no 23/32 inference from two pilot seeds.
No-write still runs/charges candidate proposal compute but drops writes.
R interception charges attempted R writes; T proposals remain available.

At ticks 256, 512 and 768, fork evaluator snapshots without restoring parents.
Erase one task replica chosen prospectively by the probe stream, then allow
16 label-free live repair steps without further faults. Report accuracy before
the perturbation, immediately after it, and gain. Single-replica erasure may
leave sign recall intact; floor/ceiling failure is an explicit identifiability
STOP, never evidence of preserved repair capacity.
Complete-deletion control zeros all T/R/hidden state and receives no labels.

Record per-tick query, output, correct count, writes, magnitudes, opportunities,
repair-bank scale and task-bank scale; aggregate all planned ticks.
Counts from actual nonzero accepted changes exclude zero/duplicate writes.
Store transparent NumPy acquired coefficients and per-tick JSONL, not pickle.
Fresh-instance replay starts each branch once from its acquired initializer,
never rescues a continuing branch.

## Resources and prospective early STOP

At most two fits, 4096 total development ticks plus acquisition, one CPU
thread; no GPU. Whole command hard wall watchdog: 1200 seconds, owned process
only. Checks between operations also stop at the internal deadline.
Output creation refuses overwrite; source/boundary/config/dependency hashes
are recorded before fitting. Process peak working set and wall times are
reported; physical energy/bus traffic remain unmeasured.

Report computed dense linear forward MACs and development forward/backward
invocation counts separately. Backward nonlinear, optimizer and physical
traffic are NOT inferred from parameter counts or forward MACs.

After completing every arm for seed 0, STOP without seed 1 if:

- no-write pressure whole-horizon accuracy >=0.98 and candidate advantage over
  it <=0.02 (the regime has not made maintenance load-bearing); OR
- all three capacity probes have zero accuracy loss immediately after the
  perturbation in both candidate and interception branches (ceiling/unobservable
  repair-capacity contrast); OR
- a boundary/numerical/resource defect occurs.

Seed 1 remains NOT_RUN with the stopping reason, not silently dropped.
Do not intensify faults, change the task, repair probes, thresholds or optimizer
after observing this pilot. A stopped pilot supplies engineering negative or
invalid-design evidence, not a full-family impossibility certificate.
Before any final source freeze or final run, return this evidence for human
review; retain Phase III-B B and A6 UNRESOLVED.
