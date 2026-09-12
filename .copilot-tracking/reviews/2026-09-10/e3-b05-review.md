---
title: Independent B05 evaluation contract review
description: Static consistency, experimental-design, workload, and archive review of E3 evaluation v0.7
ms.date: 2026-09-10
status: Complete - changes required before B05 acceptance or design freeze
---

## Executive decision

Changes required. The numerical products in v0.7 are internally correct, but
that is not sufficient grounds to accept the selected experiment. Two major
B05 findings remain: an omitted protocol positive control described as optional,
and an unjustified prohibition on simplifying the experimental/archive product.
Neither finding authorizes automatic edits, experiments, or a freeze.

Preserve all 32 final individuals and eight primary panels, the primary 256-query
H1 endpoint, the 128-U/128-O H2 endpoint, and every existing numerical gate.
Do not impose an arbitrary one-million-row experiment limit. Instead distinguish
scientifically necessary observations from redundant trajectories, physical
copies, and an unnecessarily large candidate-by-control product.

The selected totals are 49,982,464 final and 320,444,928 engineering response
rows; 65,223,680 final and 418,568,704 engineering checkpoint rows. Together the
276-byte payloads alone occupy 133,526,697,984 uncompressed bytes, or 133.53 GB
(124.36 GiB). Engineering alone is 115.52 GB, before indices, responses, service
records, schedules, hashes, or metadata. No measured disk usage or runtime is
claimed. Lossless deduplication is already permitted, so these are logical
uncompressed sizes, not an unavoidable physical-storage lower bound.

## Scope and evidence

Read E3_EVALUATION_CONTRACT_v0_7.md in full against full reads of
E3_PROTOCOL_v0_1.md, E3_POLICY_CONTRACT_v0_5.md,
E3_PHYSICAL_CONTRACT_v0_4.md, and E3_CONTROL_CONTRACT_v0_6.md.
Also read E3_STATE_CONTRACT_v0_2.md, E3_OPERATION_CONTRACT_v0_3.md,
NEW_AGENT_GUIDE.md, the incorporated controller review, and the B05 research
record. Consulted relevant older physical research and current service/ROM
research only for authority and completion-status checks.

This is an independent static document review. Arithmetic used only published
integer constants. No E3 worker, target assignment, random generator, bootstrap,
Monte Carlo, historical result analysis, external model, training, replay, or
experiment ran. Only this review file was created or edited.

### Authority and conflicting paper profiles

* E3_CONTROL_CONTRACT_v0_6.md, lines 8-38 and 274-303: the selected controller
  has two prepaid 256-instruction execution budgets, 512 total CONTROL energy.
  It adds 256 energy per actually funded offered controller, not per acquisition
  or H1 tick. The contract takes precedence over incorporated CT repairs, then
  the trace, then inherited rules for unchanged matters. This does not mean
  two stored-ROM pages or 1,024 CONTROL energy.
* E3_PHYSICAL_CONTRACT_v0_4.md, selection and HS-AC sections: the selected
  22 upkeep services cost 12,944 energy and 25 material per source when all
  conditioning bodies execute. Earlier research using 1,432 upkeep energy,
  g=38/56/37/18, or lower energy grants is superseded evidence, not a competing
  executable profile. Current g values are acquisition 48, development 66,
  recovery 47, H1 28, with LL-EVAL13 a separate diagnostic.
* E3_POLICY_CONTRACT_v0_5.md: objective, grid, observation, vulnerable Q,
  fixed/DRIVE/frozen distinctions, and lexicographic selection remain selected.
  Its one-C worksheet and prior full-start E bound do not override v0.6.
* E3_STATE_CONTRACT_v0_2.md explicitly supersedes v0.1's ambiguous delay and
  live random block-tie interpretation. The later physical contract also
  supersedes the earlier suggestion that a same-value Q rewrite may lower
  hazard: under v0.4 only the specified conditioning process resets age.
* The hypotheses, gates, and required control purposes in
  E3_PROTOCOL_v0_1.md remain in force. Neither the B05 research note repeating
  an omission nor v0.7 calling that omission optional resolves EV-001.

Current service research reports proposed static witnesses, while ROM research
was in progress when read. Such status text is not an independently checked or
normatively incorporated freeze pass. Hash the selected final witnesses and
review their actual scope. Do not treat a stale research profile as a new tariff
or silently reopen already incorporated CT repairs.

## Concrete B05 findings

### EV-001 Major: disabled oracle contradicts preserved control purpose

Evidence: E3_EVALUATION_CONTRACT_v0_7.md, lines 155-176 and 915-917;
E3_PROTOCOL_v0_1.md, conventional-baseline table at line 179, partial-damage
control clause at lines 233-237, and required verification at lines 440-448;
E3_POLICY_CONTRACT_v0_5.md, fixed-drive and exact-next-design-work sections.

The protocol includes an exact-template oracle as a privileged repair positive
check and distinguishes it from externally funded ordinary correction. B05 was
to specify it, not declare its purpose nonexistent. V0.7 assigns it zero
branches and states, "This is not a missing mandatory control." That is not
supported by the retained protocol. Not being a fair-objective rival or a
numerical H1/H2 claim gate does not make a specified positive control optional.

The omission matters diagnostically: ordinary correction cannot replace a
positive check with explicitly restored information. A failed ordinary arm
cannot by itself distinguish a weak repair policy from a broken restoration,
decoder, query, or assay pathway. Conversely, an oracle success would not prove
example-free reconstruction, RL superiority, or autonomous maintenance.

Required disposition before accepting B05:

1. State accurately that the required privileged-positive-control purpose is
   unimplemented/unspecified, does not currently pass, and prevents claiming
   complete control coverage or first-freeze readiness.
2. In a new version, either specify a bounded engineering positive-control
   implementation, schedule, inputs, funding, expected validation, and counts,
   or explicitly amend the inherited protocol with a scientific rationale for
   excluding/replacing that purpose. Leaving historical files unchanged is
   appropriate; pretending the requirement never existed is not.
3. Do not automatically cross the oracle with every policy/candidate/panel.
   The protocol establishes a control purpose, not that maximal product.
   A prespecified engineering conformance check may suffice if the new version
   expressly defines its limited inference and coverage.

The suggested direct-template prefix prices are arithmetically consistent:
394+5(1+128+23)=1,154 for REP and
394+20(6+128+23)=3,534 for BLOCK. They do not supply a complete CONTROL trace,
tail, sourcewise quote, delivery contract, or instantiated oracle branch.
There is no basis to add an unpriced callback or a free direct WRITE2.

Keep a second positive-control obligation distinct: protocol section 8 requires
scripted H2 feasibility controls before final seeds. G-DIAG and HS-REFERENCE
running ordinary learned/fixed policies do not automatically constitute such
witnesses. B06 must specify the sourcewise candidate witness; authorized
implementation validation must test it before finals. This obligation remains
through protocol incorporation; it is not an additional claimed arithmetic bug.

### EV-002 Major: scope and archive expansion lack discriminating rationale

Evidence: E3_EVALUATION_CONTRACT_v0_7.md, lines 10-16, 182-204, 309-329,
383-420, 569-599, and 669-788; NEW_AGENT_GUIDE.md, lines 203-220 and 273-278.

The opening prohibition treats archive size as no reason to reconsider any
branches or raw observations. It then requires all tuning candidates to run
all controls, all-history negative continuations, four full H1 assays per
history, and every-tick logical checkpoints. This conflates preservation of
scientific precision with preservation of every newly invented cross-product.

The guide requires the smallest discriminating world, practical non-pickle
checkpoints, and exact selected replay without retraining. It does not demand
an arbitrary amount of duplicated development or hundreds of millions of
physical snapshots. The original protocol requires complete state whenever
checkpointed and all planned outcomes whenever run; neither condition proves
that this particular Cartesian product is necessary.

Specific drivers of the expansion:

* Every engineering candidate runs six H1 or six H2 branches, although selection
  uses H1 intact/A and H2 intact/D/C. Frozen children do not enter candidate
  selection. M/S/X/N and frozen controls have important final/diagnostic roles,
  but no supplied rationale makes all of them tuning measures for all 100
  candidates per representation/family.
* Every nonnegative phase generates a 389-tick reset continuation. These add
  33,741,824 final and 217,492,480 engineering checkpoint rows when their
  eight boundary rows are included: approximately 52% of each archive.
  The reset payload alone is 69.34 GB across cohorts. Equal canonical states
  under the same G/Z deliberately have equal futures; repeating those futures
  does not provide new target tables or inferential units.
* PRE is repeated six times from the same candidate's developed parent using
  the same PRE inputs. It has no branch intervention yet. These logically
  distinct records have an exact common origin, unlike different panel streams.
* The saturated HS development admits all declared cut pairs with the same
  high E/P bins. The known aliasing is acknowledged but not used to bound
  required host computation or explain why separate physical trace copies
  are valuable.
* Checkpoint deduplication only solves payload duplication. The current design
  still mandates 483,792,384 checkpoint index rows and 12,014,094,592 outer
  service slots. Per-service actual-path records can dominate the state archive.

Required disposition: before first freeze, provide a branch-purpose matrix and
an archive/execution plan that distinguishes logical outcomes, required physical
execution, and storage encoding. Either justify the full product quantitatively
or issue a smaller prospective version without changing the scientific question
or primary precision. Preserve v0.7 as historical design evidence.

This is not permission to sample rows out of a completed or still-selected run.
Nor is it a demand for a fixed disk limit. It is a request to stop treating
unreasoned replication of controls and snapshots as a scientific safeguard.

## Verified arithmetic and counting corrections

No published cohort-product arithmetic defect was found. The correction needed
is interpretation: 418,568,704 is the engineering checkpoint total, not a byte
count or a number of independent observations. The >100 GB concern is real for
the stated uncompressed engineering payload, not for final payload alone.

### Branch products and units

Per individual/panel cell:

* Final T=16: two codes x two families x four policies.
* Final H=48: two codes x four policies x six H1 branches.
* Final J=8: one H2 intact probe for each of two codes x four policies.
* Final K=52: 48 H2 core branches plus four FROZEN-D/C branches from RL only.
* Final A=16: two pulse branches x two codes x four policies.
* Engineering T=400: two codes x two families x (9+81+9+1) candidates.
* Engineering H=1,248: 1,200 core plus 48 H1 diagnostics.
* Engineering J=200: two codes x 100 H2 candidate parents.
* Engineering K=1,320: 1,200 core + 36 frozen + 48 grid + 12 HS + 24 mixed.
* Engineering A=424: 400 core pulses + 12 mixed pulses + 12 LL13 pulses.

The final multiplier is 32 x 8=256 cells; engineering is 8 x 8=64 cells.
These are not "256 controls versus 64 controls." Final has 100 H1/ecology
histories per cell, 25,600 overall. Of those 100, 76 are main-policy/frozen
histories and 24 are DRIVE. H2 frozen is only two branches per RL parent, not
another six-way product or an H1 product. Engineering has 2,436 core and 132
diagnostic histories per cell, 164,352 overall, excluding trunks and J probes.

### Cohort totals

Let E=2T+5H+J+K, L=2304T+1172H+261J+512K+389E, and
B=5T+17H+3J+4K+8E+A. T/H/J/K count histories, not individuals.

| Quantity                      | Final           | Engineering       |
|-------------------------------|-----------------|-------------------|
| T                             | 4,096           | 25,600            |
| H                             | 12,288          | 79,872            |
| J                             | 2,048           | 12,800            |
| K                             | 13,312          | 84,480            |
| A                             | 4,096           | 27,136            |
| E                             | 84,992          | 547,840           |
| Summary rows 3E               | 254,976         | 1,643,520         |
| Teaching rows 256T            | 1,048,576       | 6,553,600         |
| BLOCK COMMIT rows 64T_BLOCK   | 131,072         | 819,200           |
| Planned due responses         | 49,982,464      | 320,444,928       |
| Planned tick rows L           | 64,250,880      | 412,296,704       |
| Extra checkpoint boundaries B | 972,800         | 6,272,000         |
| Full checkpoint rows L+B      | 65,223,680      | 418,568,704       |
| State bytes 276(L+B)          | 18,001,735,680  | 115,524,962,304   |
| ISOLATE slots                 | 250,880         | 1,617,920         |
| Outer-service slots           | 1,620,049,920   | 10,394,044,672    |
| Offered controller slots      | 27,656,192      | 176,029,696       |
| Max added v0.6 energy         | 7,079,985,152   | 45,063,602,176    |
| Ordinary fault-scalar slots   | 203,032,780,800 | 1,302,857,584,640 |
| Primary/reset challenge slots | 7,782,400       | 50,216,960        |

Secondary FLIP adds 61,440 engineering challenge scalars, 80 x 768 histories.
No unused planned scalar needs to be materialized as a separate draw record.
The additional controller energy is an upper bound on funded execution, not
a debit charged to dead rows.

Responses decompose as follows; this independently checks the published sum
2043T+1024H+256J+507K+256E:

| Response source | Final      | Engineering |
|-----------------|------------|-------------|
| Development     | 8,368,128  | 52,300,800  |
| Four H1 assays  | 12,582,912 | 81,788,928  |
| H2 intact probe | 524,288    | 3,276,800   |
| Ecology         | 6,749,184  | 42,831,360  |
| Reset FINAL     | 21,757,952 | 140,247,040 |

Acquisition contributes no query responses; its 256 lessons and BLOCK's 64
COMMITs are different tables. Recovery contributes no planned query rows even
though RESPONSE service may emit an unscored spurious bit. H1 contributes four
256-query assays and 128 recovery ticks, not four 128-tick phases. H2 has 507
whole-phase responses, of which 256 are the prespecified endpoint.

The summary formula is also correct: E nonnegative phase rows plus two rows
for each of E negative children gives 3E. It is not a demand for a new summary
row for every tick, cue, response, metric, or replica. Reducing summary columns
or deriving a single stage summary from existing observations cannot eliminate
the charged probe experiment that v0.7 actually selects.

### Storage and host-work implications

Combined totals are 370,427,392 responses, 483,792,384 checkpoints,
12,014,094,592 outer-service slots, and 1,505,890,365,440 ordinary fault-scalar
slots. These are planned products, not all necessarily executed work after death.

The two uint64 offset/length values alone would occupy 7.74 GB if physically
stored once per checkpoint. A separate 32-byte digest for every checkpoint
would add 15.48 GB if that encoding is chosen. A merely illustrative 16-byte
record for every service slot would require 192.23 GB; the actual schema has
more fields and no fixed byte width yet. These are encoding illustrations,
not additional mandated byte totals or measured capacity estimates.

The optional 65,536S primitive expansion would have a combined upper bound of
787,355,703,181,312 slots. It is explicitly not required and is too loose to
serve as a practical archive plan. Prefer bounded compiled traces, actual-path
identifiers/counts, indexed external inputs, and deterministic validation hashes.
Do not confuse cheap simulated energy quanta with cheap host runtime.

## Minimum-preserving reductions for a new version

Order recommendations by scientific preservation and likely benefit. None was
applied. Current v0.7 logical outcomes remain mandatory unless superseded
prospectively; sharding at one million rows is not scientific subsampling.

### 1 Separate tuning measures from confirmation controls

Retain all 9 RL, 81 PERIODIC, 9 THRESHOLD, and one DRIVE candidate definitions
where currently selected. Preserve the v0.5 population ranking and full planned
development. Screen H1 candidates on intact I and correction-enabled A, and H2
candidates on its intact probe plus D/C, including all costs and feasibility
components used by that ranking. Record all candidates, ties, and infeasible
outcomes. Do not tune on desired RL-minus-periodic margins.

The screening product would be 400 H1 histories, 200 H2 intact probes, and
400 H2 ecologies per cell, rather than the current core 1,200/200/1,236.
Run the full control product for the selected family configurations and the
prespecified diagnostic defaults. Account for overlap without adding a second
vote or rerunning an identical already archived condition. This is a concrete
reduction of unused tuning crossings, not omission of primary final controls.

Exact revised totals depend on whether DRIVE screening is retained, how winner
and default overlap is encoded, and which diagnostics are selected. They must
be derived in the new version, not represented by the current RAWCOUNT formula
with deleted rows. Preserve H1 N/M/S/X and H2 N/M/S/X, frozen D/C, and DRIVE's
diagnostic purpose where the protocol requires their control function. Do not
remove a difficult conventional rival or abandon BLOCK reporting.

### 2 Represent identical development and probes once

At full-start HS sensing, v0.6 gives E>=60,266 and local P=255. All three E and
P cuts are high, not merely likely to be high. Conditional on the funding and
trace assumptions, paired streams and the same policy therefore make the nine
cut-pair development paths identical. PERIODIC intervals can still differ.

Per representation/family/panel/individual there are at most 12 distinct
development behaviors: one RL, nine periodic intervals, one threshold, and
one DRIVE, versus 100 candidate IDs. Across engineering this is 3,072 distinct
behavioral trajectories instead of 25,600, before any cross-family or panel
change. Avoiding the 22,528 duplicate 2,048-tick executions would save
46,137,344 host-simulated development ticks. Acquisition is even more widely
policy-independent, but REPRESENTATION and input-namespace differences remain.

There are two different permissions:

* V0.7 already allows lossless payload deduplication. Executing each candidate
  separately and storing identical bytes once is not a scientific redesign.
  Retain each candidate's independent logical lineage, planned outcomes,
  eligibility, simulated costs, and key checks.
* Executing one representative trajectory and declaring the others replay-
  equivalent requires an explicit shared-record rule in a new version because
  v0.5/v0.7 require each candidate's own canonical development and forbid Q
  transfer. Supply an exact transition/input equivalence argument, per-candidate
  conformance coverage, and distinct candidate configurations. This is not
  importing the best learned Q into an unrelated candidate or skipping training
  failures. Later H2 cuts may cease to alias and must then branch normally.

For the same H1 candidate, six PRE probes start with identical state and shared
PRE inputs before any branch intervention. Their payload/response traces can
be referenced once while retaining six logical stage rows and correct
all-experiment accounting. No assumption about independent PRE samples is lost.
Do not generalize equality from equal final scores: phase namespace, G, inputs,
all 276 bytes, charges, and event ordering must match for the portion shared.

In particular, do not merge M/S/resource branches merely because their scientific
contrast is saturated. Their external intervention flows differ; the first
post-refill accepted transport can also differ. Equal recall is not a
byte-identical trajectory or ledger proof.

### 3 Store snapshots at replay and fork boundaries

Use full 276-byte snapshots at canonical activation, acquisition completion,
development completion, every actual fork, injury/intervention boundary,
probe entry/exit, recovery end, final/ecology end, and death. Retain invalid
encodings, reserve, ages, reservoirs, and all external lifecycle metadata.
Choose any additional sparse restart anchors prospectively from replay cost,
not from favorable outcomes.

For intermediate ticks, retain the complete planned event/response key space,
actual path/debit/output data, external indexed input definition, and hash or
hash-chain evidence sufficient to verify replay from the nearest anchor.
Archive consumed scalar provenance and scorer outputs without granting worker
read access. Emit planned-dead rows or a lossless range representation with
exact deterministic expansion; never fabricate biological death for exceptions.

This permits branch replay from the developed snapshot without reacquiring or
retraining the individual. Hashes authenticate records but cannot reconstruct
state without an anchor, deterministic transition specification, and exact
input context. A hash alone is not a checkpoint. A saved parent is accessible
to the external branch/replay harness only, never as a live repair template.

V0.3's tick-order clause currently says to emit a full boundary snapshot, and
v0.7 expressly requires every planned tick payload and index row. Sparse
checkpointing therefore needs an explicit versioned override of those clauses;
it is not an already compliant way to skip their rows. In contrast, compression
of payloads with every existing logical index is already permitted. These
options preserve primary queries and precision but have different specification
and validation obligations.

### 4 Separate actual reset validation from identical reset futures

Keep reset transformation checks on every planned source history if that
coverage is retained: read the actual end state, construct a genuinely new
canonical state, cancel references/events, compare every field, and record
the mapping and eligibility. Do not start with a blank initializer and claim
the preceding acquisition-to-reset boundary was tested.

Once exact reset and transition noninterference have been established, a new
version can use one continued reset trajectory per distinct G and fixed future
Z, referencing it from all equivalent parent-reset records. Holding candidate
identity fixed gives a conservative upper count of 4,096 final and 25,600
engineering representative futures, rather than 84,992 and 547,840, before
any additional proven G-equivalence reduction. This count is not new statistical
n and does not authorize skipping actual reset checks on the other histories.

At 397 checkpoint rows per continuation including boundaries, those naive
representative products would avoid 32,115,712 and 207,329,280 duplicated
continuation rows respectively. New reset-audit/reference rows still have to
be counted, so these are gross continuation savings, not finalized archive
totals. If future equality is unproved or implementation tests require paired
executions, run those exact comparisons rather than memoizing away the test.

### 5 Treat shared development across panels as a scientific choice

Unlike the same-input candidate aliases, different panels currently have
different acquisition, development, wear, and exploration streams. They are
not byte-identical clones by definition. Sharing one development per
individual/representation/family/policy, followed by eight independent held-out
evaluation panels, is a plausible closer reading of the original guide/protocol,
but changes the estimand and covariance. It requires a new version and B06
assurance, not a storage-only optimization.

Without candidate aliasing, that alternative changes final T from 4,096 to
512 and engineering T from 25,600 to 3,200, while retaining 32 independent
final target tables and eight evaluations per primary endpoint. It cannot
reuse the existing all-history summary/reset formulas without revision.
Prefer proven candidate/trace deduplication and narrower tuning crossings
before changing panel development if the present multiple-development
estimand has a scientific justification.

Do not silently remove PRE/ACUTE/POST. Protocol section 6 explicitly proposes
those disposable probes. A new version may narrow diagnostic probe replication
with a reason, but must preserve the required stored-information demonstration
and the primary FINAL assay. A summary can aggregate a measured stage; it
cannot turn four selected paid probes into one uncharged host decode.

## Experimental unit, targets, pairing, and covariance

The acquisition-target rule is already unambiguous in v0.7, lines 35-41 and
442-455: draw one independent 16-bit table per individual, using its own private
32-byte request, then reuse its 16 labels across representations, policies,
candidate settings, families, panels, and counterfactual branches. Teaching
presents those same labels sixteen times per cue. Do not redraw at each panel,
reacquisition opportunity, representation, reset child, or failed branch.

There are 32 independent final tables, not 256. Engineering has eight tables,
not 64. The unused 240 bits of a 256-bit target draw do not enlarge target-table
entropy. Coincidentally identical independently drawn tables are retained;
enforcing uniqueness or label balance would change the law.

V0.7 explicitly chooses eight independently randomized developments nested
within a target-table individual. The inferential cluster is therefore the
target-table ID with all of its developments and counterfactuals, not literally
one physical developed body. This is statistically coherent with cluster-level
averaging, but differs from presenting eight panels only to one developed body.
The distinction should be stated in the methods and B06 model, rather than
counting branches or repeated cue responses as independent acquisitions.

For a contrast, let d_ip be its complete paired value for individual i and
panel p, and D_i=(1/8) sum_p d_ip. The reported estimate is
(1/32) sum_i D_i. With independent individuals under the ideal input law:

$$
\operatorname{Var}(\widehat\Delta)=\frac{\operatorname{Var}(D_i)}{32},
\qquad
\operatorname{Var}(D_i)=\frac{1}{64}
\sum_{p=1}^{8}\sum_{q=1}^{8}\operatorname{Cov}(d_{ip},d_{iq}).
$$

With conditional independence of panel-specific developments/evaluations given
Y_i and fixed G, this becomes

$$
\operatorname{Var}(D_i)=
\operatorname{Var}_{Y}\!\left(\mathbb E[d_{ip}\mid Y_i,G]\right)
+\frac{1}{8}\mathbb E_Y\!\left[\operatorname{Var}(d_{ip}\mid Y_i,G)\right].
$$

The first term does not disappear with eight panels. Shared-development panels
instead condition on both Y_i and the common developed state S_i; variation
in S_i joins the shared term rather than being reduced by eight independent
developments. This is why changing development reuse needs prospective assurance.

Within a panel, paired arms share their actual developed parent where specified
and common indexed exogenous streams. Their contrast variance contains the
covariance term, Var(A-B)=Var(A)+Var(B)-2Cov(A,B). Cross-policy and cross-code
development is not the same physical parent, even when labels/noise are paired.
The 10,000 bootstrap resamples must resample the whole 32-ID vectors once,
sharing indices across comparisons. V0.7 does this correctly; no tick-level or
response-level bootstrap is authorized. Finite HMAC streams implement the
ideal law computationally, not an information-theoretic independence proof.

Whole-block U/O is correctly chosen by a target-independent panel shuffle,
shared across policies/codes and across D/C. Each final H2 endpoint has exactly
128 U and 128 O responses, while C preserves that same U label for its recall
denominator. Balanced cue counts do not imply balanced target labels. H2
spending ticks 257-512 intentionally differ from endpoint admission ticks
252-507; all five drain controller offers remain included.

## Complete-erasure and physical-boundary assessment

The selected reset semantics are substantively correct at design level, not
proved by this review. Code becomes 10 at all 80 lanes; all 2,048 auxiliary
bits become zero, including Q, ring payload and reserved bits, staging,
transition, metadata, every age, resources, and inaccessible reserve. Activate
the new body identically with E=65,535 and all four Pj=255. A dead parent remains
dead; its new negative child is not a rescued historical body.

All twenty physical age words and their cross-domain storage dependencies must
be covered. There is no protected historical age or medium stock. Ordinary
faults use the simultaneous pre-fault stored ages; they cannot read an age
already altered by the same fault or preserve a clean vector into the next
worker transition. Resource injury and refill are typed sinks/deposits, not
bit flips that manufacture energy/material or restore code.

Reset must cancel scheduled messages, callbacks, pending feedback, old input
cursors, and references to original state, scorer, target, or checkpoint.
History IDs may select archive output locations but cannot choose future Z.
Fixed policy/cut constants G stay fixed during counterfactual tests; do not
retune them on each changed history or target table. Repeat tests across live,
dead, resource-skewed, corrupt, and deliberately populated states. Code-only
partial lesions do not establish all-state erasure.

Required target coverage is precise:

* All 16 four-bit tables in the reduced component test, through actual
  acquisition and reset, using paired future inputs
* Each of the 16 individual bit changes in the production target table,
  cross-block changes, and populated/corrupt body/queue/age/reserve cases
* A full production finite-state inventory and compositional argument for
  every history, not an assertion that the finite cases exhaust all histories

There are 65,536 full 16-bit target assignments. Exhausting them is an optional
stronger test under protocol section 7, not a mandatory 255-target or 256-target
enumeration. The value 255 is each material reservoir's cap. The canonical
snapshot is 276 bytes, not 255 or 256 bytes. No requirement to reset fewer
fields follows from reducing archive copies.

For the empty-code negative, sign flips do not populate erased symbols and
scrubbing abstains. This supports a fresh-readout-guess argument, but query
validity, missingness, funding, and availability remain part of the proof.
V0.7 correctly retains planned-denominator failures, separately reports emitted
forced-choice accuracy, marks any zero-emission panel undefined, and requires
coverage/activity >=0.95. Its containment interval applies to the fixed
H1-family RL-developed subset, separately for REP and BLOCK; duplicated
all-history children cannot narrow that primary interval.

Do not report empirical chance or 0.80 containment assurance from these
structural observations alone. B06 must evaluate the stated output law and
the selected individual-level procedure. Balanced guesses, artificial labels,
deleted missing panels, and evaluator-substituted answers are invalid shortcuts.

## Other full-review conclusions

### Controls and supported profiles

H1's six ordinary branches match the required partial/intact/no-code-write/
material/sham/external-support functions. No-write preserves Q inference,
epsilon, paid scans, query/age bookkeeping, and faults; it is not all-writes
prohibition or a fresh fixed table. FROZEN exists only in H2 from trained RL,
with inference and Q faults retained and learning/record costs honestly omitted.
DRIVE has a different assigned objective and cannot pass fair-arm gates.

H1 material/refill and extra-funding contrasts are explicitly saturated under
full entry and g=47. H1-M's net initial addition is thirteen per source after
ISOLATE; H1-X offers thirteen extra every recovery tick, not the same total
intervention dose or a reimbursement. V0.7 correctly discloses this. Equality
does not establish biologically meaningful resource restoration. Nor can a
negative result in such a null contrast establish material irrelevance.

The 128-tick recovery has no teaching, ADMIT, ecological income, signed return,
or outcome-conditioned timing. PRE/ACUTE/POST are separate disposable wearing
assays, not independent biological replicates; parent trajectories do not incur
their 783 ticks. FINAL is the challenged actual recovered branch. H2 does
receive outcome-dependent feedback and may relearn; it cannot be pooled with
H1 as no-example recovery. These distinctions are correctly maintained.

### g=36 and H1 headroom are legitimate B06 work

The g=36 material offer per source is a selected budget, not an empirical
scarcity result. Being below the 40 all-conditioned learning housekeeping
figure does not prove maintaining all regions impossible: TD/conditioning can
drop, collection is local, reservoirs start full, and fixed/frozen paths save
work. The protocol needs an actual sourcewise opportunity-cost and useful-
retention analysis, positive O-write denominators, and scripted feasibility
validation before finals. V0.7 already identifies those limits and requires
versioning rather than choosing the best diagnostic grid point after outcomes.

The g={28,32,36,40} default grid and g=66 reference are bounded diagnostics,
not a hidden optimization axis. Their deliberate duplicate g=36 namespace
does not create an extra independent individual or selection vote. Consider
exact shared-record reuse only if the namespace/input law is explicitly
changed prospectively; numerical equality of g alone is insufficient.

Financial support of 29,394+1 energy for a maximal BLOCK learning tick does
not establish recall or allocation. Isolated three/five-copy challenge gain
0.01944 and optimistic recovery-wear headroom about 0.08641 omit important
assay/Q/query effects. Keep both five-point H1 comparisons distinct. A
competent periodic rival defeating the adaptive gate is a valid result.

### Gates, death, and freezes

The numerical H1/H2 gates, individual weighting, ratio-of-means rule,
zero-comparator treatment, negative containment band, and separate BLOCK
reporting are retained. H1 prerequisite uses intact I FINAL; H2 uses its
developed intact probe. Acquisition and development activity are separately
required >=0.95. Do not add a final H1 completion threshold merely because
engineering feasibility uses one; v0.7 correctly distinguishes them.

Death keeps every planned failure and actual shutdown RAM. A valid emitted
response before a fatal fault is scored, but does not imply active tick or
completion. Ordinary support cannot resurrect it. A technical exception is
FAILED/PARTIAL, not a fabricated biological-death suffix or COMPLETE run.
Immutable start/end/shards, no overwrite, private roots, and one-way scorer
ownership are appropriate. Full replay context must include lifecycle and
pending externally scheduled events as well as the 276 worker bytes.

First freeze requires a complete selected design, honest control coverage,
static feasibility/headroom/precision work, and ownership/trace specifications.
It cannot require already-passed production tests before code is authorized.
Authorized implementation and validation then precede engineering; independent
final target tables and private roots follow the second source/config/test/
analysis freeze. Neither freeze has occurred. Research hypotheses are not
required to succeed to permit reporting a valid negative experiment.

## Verification record

Recomputed all published T/H/J/K/E, summary, teaching, COMMIT, response, tick,
boundary, checkpoint, byte, ISOLATE, service, controller, energy-increment, and
fault/challenge products using read-only scalar PowerShell arithmetic. No
published total needed numerical replacement. An evidence-gathering command
initially collided with a typed variable retained in the PowerShell session;
rerunning with fresh names succeeded. No experiment or file edit resulted.

The five source hashes below were unchanged on the final comparison. Editor
diagnostics reported no errors in this review. The document was read back in
full. No claim is made about concurrent edits by other agents or files outside
the five hashed contracts.

Reviewed SHA-256 values, recorded for source identification, not a freeze:

* E3_EVALUATION_CONTRACT_v0_7.md:
  ea3698bdb595b66eeebf8f50a75b6514166bdfdb7bbaaa16c6392e7ef6e0dae3
* E3_PROTOCOL_v0_1.md:
  5a551f004024ae59e60ae25b95ca60af61f2989fb33575c97aa774b81e804bef
* E3_POLICY_CONTRACT_v0_5.md:
  fe174d0bdb8d8d22583e426cf74ebb680d8d471a8c447f906a104819ded791cf
* E3_PHYSICAL_CONTRACT_v0_4.md:
  f0f05d57b5f98c171ff2956ca4bdfd00a59edfb3579d3fbe05fb74c8001e1dc8
* E3_CONTROL_CONTRACT_v0_6.md:
  198c96c610d0fd89f9990836ad8b6d68aca13580b9ecad80b55cb5be962af060

## Recommended next work and clarifications

* [ ] Resolve EV-001 in a new version: bounded privileged positive check or
  explicit prospective protocol amendment, with accurate coverage status.
* [ ] Resolve EV-002: justify or reduce tuning/control/reset crossings and
  specify logical versus physical archive/execution requirements.
* [ ] Prefer exact candidate/trace reuse, branchpoint snapshots, and narrower
  tuning products before changing 32-individual/eight-panel precision.
* [ ] Make the panel-development estimand explicit and supply its covariance
  model to B06; any shared-development alternative needs prospective assurance.
* [ ] Complete B06 H1 headroom, H2 sourcewise/scarcity and scripted-control
  design, and powered-erasure containment assurance without final-outcome tuning.
* [ ] Complete B07 ownership/reset and independent static/ROM review, then
  implementation validation only after design freeze and authorization.

No factual clarification requires user input to establish these findings.
Choosing among justified prospective redesigns is the next bounded design
decision, not permission to edit contracts or run experiments in this review.

## V0.8 acceptance closure scope

Acceptance review date: 2026-09-10. Status: Complete; decision follows below.
This appended section is the sole research and closure record for this request.
The initial v0.7 review above, including its historical status and recommendations,
is preserved rather than rewritten. No separate research artifact is created.

Review E3_EVALUATION_CONTRACT_v0_8.md against v0.7, EV-001/EV-002, the completed
B06 analysis/review, and the now-present B07 information review. Verify the
oracle's authority, prefixes, coverage and diagnostic physics; screening and
selected controls; all-history reset audits and primary future-input identity;
integer workload/archive bounds; unchanged statistical gates; and the distinction
between outstanding design decisions and later implementation evidence.

All investigation is static document review and read-only scalar arithmetic.
No E3 code, target/root draw, experiment, bootstrap, training or replay is run.
Only this existing review receives appended material. The initial 39,311 bytes
have SHA-256 9c0c33b3d735cc0dcef8a6d53566e91525f96b58fec738b628f8b7e9b9b5d2a0.
Original bytes are retained in terminal memory for the final prefix comparison.

## V0.8 acceptance closure decision

Review complete. QUALIFIED B05 DESIGN PASS: EV-001 and EV-002 are closed as
prospective design-remediation findings. The initial review remains the correct
assessment of v0.7, not the current disposition of those two findings. This
closure does not certify implemented controls, a validated archive codec,
unconditional B07 closure, either freeze, or scientific success.

No replacement is needed for the published v0.8 workload or byte arithmetic.
The primary experiment remains 32 independent final individuals, eight separately
developed panels per individual, both representations, every final ordinary
control, the original endpoints and all numerical scientific gates. No final
target, root, winning configuration, realized denominator or runtime is predicted.

| Identifier | Current acceptance disposition |
|------------|--------------------------------|
| EV-001 | CLOSED at B05 purpose/scope level: mandatory bounded privileged engineering restoration, exact-code checkpoint, separate zero-fault and live-wear probes |
| EV-002 | CLOSED at B05 product/architecture level: discriminating screening, full selected controls, complete planned raw outcomes, every-source reset checks and sparse exact replay |
| AN-003 / AN-006 | PASS for v0.8 compatibility: the reviewed canonical-empty assurance law and primary reset subset survive the revised product |
| AN-001 / AN-002 | Existing localized B06 corrections remain applicable to adoption of that analysis; neither is a v0.8 count error or a change to erasure assurance |
| IF009 | Its EV-001/EV-002 pending-revision dependency is resolved by this review; other B07 acceptance conditions are not automatically discharged |
| AC-01 through AC-04 below | Remaining bounded pre-freeze design closures, not newly discovered numerical defects or requests for empirical success before code |

### Closure evidence and limits

Read v0.8 and v0.7 in full, the initial B05 review, B05 revision evidence, the
complete B06 analysis and independent review, and the now-complete B07
information review. Read the state, operation, physical, policy, control and
protocol contracts and both completed service/ROM notes to check the inherited
rules and the new oracle's boundaries. No historical result data were analyzed.

Primary evidence locations:

* E3_EVALUATION_CONTRACT_v0_8.md, lines 8-35: explicit prospective supersession
* E3_EVALUATION_CONTRACT_v0_8.md, lines 37-95: units, screening, ranking and final catalog
* E3_EVALUATION_CONTRACT_v0_8.md, lines 176-262: mandatory oracle, packets, trace, probes and counts
* E3_EVALUATION_CONTRACT_v0_8.md, lines 264-336: every-history reset, canonical futures and randomness ownership
* E3_EVALUATION_CONTRACT_v0_8.md, lines 338-529: sparse checkpoints, raw encoding, counts and byte ceiling
* E3_EVALUATION_CONTRACT_v0_8.md, lines 531-592: unchanged estimands/gates and stage obligations
* .copilot-tracking/reviews/2026-09-10/e3-b06-review.md, AN-001 through AN-007
* .copilot-tracking/reviews/2026-09-10/e3-b07-information-review.md, IF001 through IF010 and proposed exact worker-frame closure

The B06 and B07 reviews originally had no completed v0.8 to inspect. Their
absence/pending-revision statements are historical, not evidence that v0.8 is
still missing. Conversely, their completed unchanged-service findings do not
automatically certify the newly added privileged interface or archive codec.

### EV-001 required oracle coverage and sourcewise payment

The selected product is exactly two codes times eight engineering individuals
times panel 1: sixteen conformance cases. It uses the actual H1 RL default
SCREEN A post-lesion boundary, even if damaged, dead or ineligible. A separately
declared diagnostic clone and replacement-power exception permit that test;
the original historical body stays unchanged and cannot be revived by it.
There are eight independent engineering tables, not sixteen independent tables.
The sixteen exhaustive four-bit acquisition/reset component cases are a separate
validation obligation, not this oracle product or extra final individuals.

For each case, full entry and paid ISOLATE clear query/staging/transition state.
Sixteen REP cue templates or four BLOCK payload templates unconditionally write
every one of eighty lanes, including already correct lanes. They read no old
clean code, perform no scan, and cannot restore Q, ages, metadata or reserve.
The code-equality assertion occurs immediately after restoration, BEFORE any
query probe or fault. Decode accuracy alone cannot satisfy that assertion.

Each admitted template receives exactly cue:4 and payload:4, once each at X;
REP payload is restricted to 0/1. The two encoding charges contribute two
energy, not an extra target callback. Ordinary body rejection is M+S=136 and
receives neither scalar. The admitted prefix is exactly

$$
E_{\rm prefix}=394+gV+128A+23W,\qquad V=A,\quad 0\le W\le A\le n.
$$

Here 394=128+256+8+2, code WRITE2 is 6+8(2)+1=23, and every completed code
write consumes one unit at the addressed block's source. Thus full REP is
1154 for five writes and full BLOCK is 3534 for twenty, with g=1/6 respectively.
The full-bank totals are 18464/14136. They do not include ISOLATE, query work
or external replacement/transport, which must remain separate ledger categories.

Before every template replace E/P with 65535/255 and separately log old/new
stocks plus the 1020 material-hop dispatch energy. No replenishment occurs
inside an operation. After M/C, E=65151; after both inputs it is 65149.
Full completion leaves E=64381/62001 and the addressed P=250/235. Across a
whole bank, exactly twenty writes address each source. Sourcewise affordability
is therefore not inferred from pooling four material stocks.

At zero-based cell i, retain (n-i)(g+128)+8 before generation. After generation,
retain its current gate plus the remaining cells and S; after paying that gate,
test WRITE2 against 23+(n-i-1)(g+128)+8+1 energy and one local material.
The largest such first-write requirements are 548/2578, far below the available
stock. The full positive margins dominate every successful prefix. A hypothetical
rejected gate exits immediately, keeps its completed prefix, and releases only
unvisited obligations. There is no refund, source transfer or borrowed yield.
Future ordinary services do not disappear: the off-clock harness explicitly
has T=0 outside the current template's reserved S/residue.

The normal-path CONTROL count reproduces. Entry/input retention contributes
five instructions; base preparation, including three REP adjustments or three
BLOCK padding slots, contributes nine; exit contributes two. Each cell uses
six: payload EX, expected MOV, base EX, address ADD, STAGE and rejection BR.
Generation, gates, WRITE2 and scalar encoding are separately charged. Therefore
16+6n=46/136, and the conservative 60+6(20)=180 remains below one C256.
The ordinary two-C controller price does NOT apply to this teaching-template
service. No W counter, fifth arithmetic register, acquired loop or return stack
is required. Saved cue/payload/base/expected survive arithmetic-clobbering gates.

For storage, the displayed normal paths require 21+(g+8)n typed sites,
66/301 respectively, not 256 stored sites per envelope. These counts include
outer M/C/S, two scalar sites and each generation/gate/write. Even storing both
shapes beyond the existing 27936-site reserved layout gives 28303 addresses
before separately specifying traps. This rules out an apparent capacity problem;
it does not silently add the new service to the old oracle-zero ROM manifest.
The remaining exact schema/link/trap adoption is AC-01/AC-02, not an instruction
budget failure or a need to implement a compiler before accepting this bound.

### Exact restoration is not a live-wear 100 percent gate

The protected off-clock restoration block is explicitly NEW DIAGNOSTIC PHYSICS:
no TICK, ordinary fault, leakage or upkeep intervenes between its templates.
The separate ZERO-FAULT query probe also disables RAM flips/erasures, while
retaining typed leakage, grants, all paid query/upkeep work and 261 real ticks.
It is not ordinary H1 physics and cannot pass an ordinary scientific gate.

After its own entry/ISOLATE, that probe has eighty exact symbols and cleared
query slots. Every cue's REP majority is correct; the BLOCK columns containing
1,2,4,8 make the encoded payload unique. Full support funds both codes' query
services and conditioners. With query validity/address faults disabled, all
256 admissions at ticks 1-256 emit their correct bits at ticks 6-261. Thus
256/256, activity, coverage and completion one are the conditional conformance
expectation, not an observed test result.

The independently keyed LIVE-WEAR clone starts from the same restored checkpoint
but retains ordinary v0.4 code, query and auxiliary faults for 261 ticks. It
has NO 100-percent recall gate. Realistic assay erosion can reduce its recall
despite correct restoration. Ordinary primary H1 additionally retains its own
challenge and wear, so no zero-fault oracle claim transfers to that endpoint.
Neither clone returns state, labels, outputs or test status to its parent.

Oracle totals reproduce: sixteen restoration histories, thirty-two probes,
8352 ticks, 8192 responses, 160 templates, 1280 code writes, 260800 template
energy, 48 ISOLATEs and 48 actual reset audits. Its resets reuse the already
selected H1-RL-default canonical class after revoking oracle permissions; they
add no new canonical continuation, target table or final oracle branch.

### EV-002 screening, probes and complete selected observations

All 100 candidates per code/family keep their own canonical 256-tick acquisition
and 2048-tick development. There is no selected development execution deduplication,
Q transfer, shortened training, omitted periodic setting or predicted winner.
Cut aliases can be reported without assuming identical G or skipping executions.

H1 SCREEN is TWO histories, I and A, for each of two codes and 100 candidates:
400 histories per engineering cell, not 200. H2 SCREEN is likewise 400 D/C
ecologies, plus 200 actual intact-prerequisite probes. H1 PRE is exactly 200
actual trunk probes, not one per downstream branch. PRE is diagnostic; intact
selection recall is I FINAL and ranking recall is A FINAL. H2 ranking still uses
min(mean D R_U, mean C R_U), equal D/C material averaging and all v0.5 costs.

After ranking, each selected code/family/policy receives its FULL control product
on every engineering individual/panel, using the winning developed trunk and
the distinct SELECTED-CONTROL namespace. This adds 48 H1 histories and 52 H2
ecologies per cell, including four RL frozen D/C ecologies. Their I/A and D/C
are deliberate distinct-input repeats, not duplicate selection votes. No
winner/default overlap is assumed in advance. Both executions remain archived.

Defaults add the fixed 48 H1 and 84 H2 diagnostics. Therefore engineering per
cell has H=400+48+48=496 and K=400+52+84=536. Selected RL A/N contributes six
stage probes per cell: two codes times one shared ACUTE and two separate POST.
ACUTE reuse requires exact same post-lesion bytes and inputs before permission
divergence. PRE/prerequisite references never create additional executions.

Finals keep T=16, H=48, P=8, J=8 and K=52 per individual/panel, with all six
H1 and six H2 branches for every policy/code plus the RL frozen children.
Every selected H1 has its actual 128 recovery and 261 FINAL; every ecology
has 512 ticks and all 507 planned responses, including its exact 128 U/128 O
endpoint. Raw dead/missing rows, spurious outputs and fatal-tick emitted answers
retain their specified meanings. Removing unselected candidate/control crossings
prospectively is not deletion of rows from a selected or completed experiment.

### All-history audits, canonical futures and primary precision

Every terminal nonnegative source phase is audited, including acquisition,
development, recovery, FINAL, actual probes, ecologies, diagnostics and dead
states. V0.8 resets all 276 bytes to code 10/all auxiliary zero, including Q,
invalid payloads, all twenty ages, stocks, metadata and reserve, then compares
the identically activated bytes. It cancels messages, cursors, queues and old
worker/scorer/target/archive references. A blank initializer alone does not
audit the actual source history.

Sharing follows those byte/reference checks, never replaces them. Canonical
continuation classes include cohort, individual, panel, code, family, complete
inherited G and reset-input definition. One representative per distinct class
runs 128 supported recovery plus 261 FINAL ticks. The fixed 400/16 trunk-slot
rosters are conservative logical bounds; exact unions are resolved in the
manifest, not inferred from expected future winning cuts or equal scores.
Required paired implementation trajectories must actually run before their
equivalence is trusted for reuse.

For SAME G and individual/panel future Z, different histories or target
counterfactuals must produce identical reset bytes, predictions, availability
and subsequent trajectories. Scores can differ against changed target labels.
For DIFFERENT G, equal initial canonical bytes and paired Z do not imply equal
trajectories; such equality is neither claimed nor required. Candidate/history/
outcome/diagnostic IDs cannot choose reset Z. Different G cannot merge merely
because outputs agree. FROZEN correctly maps to underlying RL with erased Q.

The primary erasure mapping remains exactly ONE H1-family RL-developed parent
per code/individual/panel: 256 panel mappings per code, 512 across both codes.
Each of the eight panels has distinct ideal indexed future draws; that panel's
draws are held fixed across counterfactual histories. Do not repeat one panel's
guess stream eight times, and do not generate new streams per source history.
Structural resets and shared suffix references add no new n or bootstrap votes.

B06's bound is preserved, conditional on canonical empty code, full g=47
recovery/g=28 assay support, the 128+261 schedule, conforming paid services,
simultaneous ages/faults and independent ideal indexed guesses. Empty code
cannot be populated by sign/erasure faults or legal empty-scan scrub; corrupt
Q cannot turn a readout guess into correction. Query validity sees five faults,
so s=(1+0.998^5)/2=0.995019960039984. For positive emitted count m,
C conditional on M=m is Binomial(m,1/2). Expected planned recall is s/2,
0.497509980019992, not exactly 0.5; emitted forced-choice accuracy is chance.

The independently recomputed sufficient event is at least 244 emissions in
each of 32 times eight primary panels. Its one-panel lower-tail probability
is 9.00860987833051e-10. Conditional independent correctness and equal-panel
weights give

$$
P(\text{containment and guards})\ge
1-256p_{\rm low}-64e^{-9.76}=0.996306033562934.
$$

Every individual mean inside the band makes every resample mean a convex
combination inside it, covering the actual 10000-resample order statistics
250/9750 without drawing bootstrap indices. This is a sufficient assurance
bound, not exact bootstrap coverage or a guarantee of the realized result.
The two-code union bound is 0.992612067125867 without cross-code independence.
All zero-emission, coverage/activity and equal-individual rules remain unchanged.

Generic noninterference does not establish this fresh-guess output law. The
fixed-per-cue sensitivity and optional n=256 hardening are different prospective
designs, not selected requirements. No larger n, response-level resampling,
balanced guesses or label filtering is justified by the current review.

### Target, root and archive ownership

V0.8 incorporates the exact v0.7 CNG/HMAC construction: one private independent
32-byte target request per individual, using sixteen low label bits; separate
private purpose roots and separate engineering/final cohorts; twelve-field
RFC 8785 tuples, HMAC-SHA-256, uint128 unbiased rejection and checked failure.
The public conformance key and public analysis key are different roles, never
live target or schedule keys. Distinct names on an exposed target seed would
not be a valid substitute.

SCREEN, SELECTED-CONTROL, final CORE, trunk probes and diagnostic purposes are
explicitly separated. Within prescribed paired products, code/policy/candidate
IDs do not split the shared draw keys. Reset removes history/product/branch
suffixes while retaining individual/panel and base family; oracle probes have
separate diagnostic purposes. Planned coordinates, not consumed-response or
successful-action counters, index future inputs.

Engineering-selected G can depend on engineering labels; therefore hold it
fixed in reset counterfactual tests. Freeze it with source/configuration/tests/
analysis/archive definitions before NEW independent final targets and roots.
One table is reused within an individual across codes, policies and panels;
neither independent requests that happen to match nor unequal label frequencies
are reasons to redraw. Final n remains 32.

The specified ordinary/reset worker has no labels, target keys, archive hashes,
scorer cue, old checkpoint, filesystem/network handle or callback channel.
Only the oracle's allowlisted template packets admit privileged engineering
labels; revoke that authority before its reset. Root/HMAC separation is a
computational implementation of the ideal law, not an information-theoretic
independence theorem or an executed no-leak audit. IF001/IF003/IF004 capability
and provenance validation remains required; this review found no newly allowed
ordinary answer channel, but cannot certify an unimplemented process.

### Exact counts and conditional packed archive envelope

All N/U/L/F/B/Bmax formulas, teaching/COMMIT counts, ISOLATEs, controller offers,
added controller-energy bounds, outer-service slots and fault/challenge products
reproduce using the declared roster. No response or snapshot total is an
independent-sample count.

| Quantity | Final | Engineering excluding oracle | Oracle | Combined |
|----------|-------|------------------------------|--------|----------|
| Planned due responses | 20360192 | 91024896 | 8192 | 111393280 |
| Planned ticks | 23695360 | 105634688 | 8352 | 129338400 |
| Maximum full snapshot rows | 760832 | 3056768 | 768 | 3818368 |
| Actual-source reset audits | 50176 | 174976 | 48 | 225200 |
| Phase summary roster | 58368 | 226176 | 48 | 284592 |
| ISOLATE slots | 54272 | 200576 | 48 | 254896 |
| Planned outer-service slots | 606543872 | 2704618112 | 208848 | 3311370832 |

Final/engineering controller offers are 17301504/77332480; extra v0.6 energy
is bounded by 24226299904 combined, charged only on funded controllers.
Ordinary fault scalars are 74877337600/333805614080, plus oracle 13196160
for LIVE-WEAR only. Primary/reset challenge slots are 1310720/4587520;
engineering FLIP adds 61440. The zero-fault oracle has no ordinary fault draws
and neither oracle assay adds a primary challenge.

Full 276-byte snapshots occur at named boundaries, every 64 ticks and phase
ends, with actual shutdown anchors. A 261-tick phase has five tick anchors,
not 261 full snapshots. The separate per-tick record is a raw 32-byte SHA-256
plus 16-byte capsule. Its specified groups sum to 8+32+32+32+24=128 capsule
bits; each four-byte group's field widths also reproduce. It is not a full
checkpoint and cannot reconstruct anything without exact anchors/G/inputs.

Replay starts from saved developed/fork states, not reacquisition or retraining.
Nearest anchors, indexed immutable inputs and linked deterministic transitions
must reproduce every intermediate byte/output/debit and match original-path
digests, not merely a digest generated by replay itself. Hashes are external
audit evidence, never clean state accessible to the live worker. Dead ranges
must expand every planned key exactly; technical interruptions stay PARTIAL.

The packed components sum to 8567308288 bytes: 8.567308288 decimal GB,
7.97892761230469 GiB. This is approximately 8.57 GB, NOT a strict 8.5 GB cap.
Snapshot payload alone is 1053869568 bytes; tick SHA-256 values alone are
4138828800 bytes. The conditional ceiling includes eight-byte responses,
308-byte indexed snapshots, 64-byte reset audits, 512-byte summaries, packed
teaching/COMMIT/template events and 64 MiB of shared context.

The ceiling uses bounded integers/raw bytes, not Python-object, per-history
JSON, hex-digest or expanded-table sizes. Capsule representability and the
64 MiB context layout still need explicit validation. Overflow blocks validation;
it never licenses dropped rows. Debug views, backups and separately budgeted
implementation fixtures are outside this envelope. There is no measured disk
or runtime guarantee, and 3.31 billion derivable service slots remain nontrivial
host work despite sparse storage.

Relative to v0.7, ticks are 27.1407%, responses 30.0716%, and maximum full
snapshots 0.7893%. These are different prospectively selected workloads,
not measured speedups or lossless removal of already executed experiments.

### B06 limitations and exact remaining pre-freeze design closures

B06's principal mathematics has been independently reviewed. Do not continue
listing all H1/H2 finance or 32-by-eight precision calculations as missing.
H1's clean-parent REP reference permits maintenance benefit but bounds the
expected adaptive advantage over I=1 near 0.0164, below five points in that
reference. It is not a no-go for every actual trained parent or realized cohort.
H2 g=36 establishes conditional liveness and real learner/conditioning costs,
not forced all-region code-maintenance scarcity: fixed REP can fund its maximal
33-per-source path. No positive realized O-write denominator is guaranteed.

Apply AN-001 when adopting B06: later conditioners reserve mandatory TERMINAL
clearing, not its optional two-material-per-source TD update. The 34-unit full
final envelope is not an ordering proof that optional TD survives conditioning;
the busiest-source mandatory-tail bound is 32. Apply AN-002's illustrative
PERIODIC planning probabilities 0.619/0.204 instead of 0.611/0.198. These
localized corrections do not alter primary gates, v0.8 counts or 0.996306.

The following bounded design items remain before an unconditional first freeze.
They are separated from unperformed implementation tests deliberately.

| ID | Remaining design closure | Existing evidence and exact exit condition |
|----|--------------------------|--------------------------------------------|
| AC-01 | Select normative authority and worker/privileged codecs | B07 IF001/IF003/IF004/IF007 supplies a proposed exact frame and completed ordinary-service witnesses. Adopt a fully enumerated capability/field schema and selected witness hashes, extending it for the new oracle. Its currently proposed ordinary tags cannot silently carry a four-bit privileged payload or protected diagnostic mode. |
| AC-02 | Close the oracle-specific static boundary | The price, sourcewise normal prefixes, CONTROL capacity, exact-code and zero-fault argument pass here. Finish/select exact scratch bindings, public entries, rejected/body-dispatch and bad-packet exits, and oracle-inclusive finite linking/quote construction required by v0.8. The old ROM note explicitly assigned zero oracle sites. No executable linker or observed 16-case pass is required at this stage. |
| AC-03 | Specify the bounded SCRIPTED H2 feasibility product and interpretation | Protocol section 8 and v0.8 explicitly require it, but the reviewed sources provide accounting/ordinary-policy diagnostics rather than an instantiated script. Fix its permissions, G, sourcewise path, input namespace, budget, finite cases, functional criteria and failure disposition before freeze; account for it separately from the selected core archive. Record the disclosed learner/conditioning opportunity interpretation rather than claiming g=36 excludes all-region fixed-REP maintenance. |
| AC-04 | Close finite archive-schema sufficiency | Fix actual field/status enumerations, trace IDs, compact boundary/audit/response/summary/context layouts and original-trace digest conventions. Establish representation for every selected corrupt/rejected/dead path and a bounded shared schedule/context inventory. The numerical envelope and bit-width sums pass; a header promising future validation is not a completed codec proof. Mechanical round trips and byte-layout checks follow implementation. |

These conditions do not reopen completed unchanged scan, RESPONSE, TERMINAL,
AGE, CONDITION, TICK, ADMIT, LESSON, COMMIT or ISOLATE paper witnesses. Those
notes now exist and B07 has reviewed their finite design. Selecting their exact
contents is distinct from demanding that a runnable implementation already exist.
For AC-02 similarly distinguish a static address/binding construction from a
later emitted-image checker. No source edit or new interface is adopted here.

V0.8 now requires H1 financial versus functional/headroom ANALYSIS and explicitly
allows scientific gates to fail. Read that alongside its preserved thresholds:
positive RL superiority, useful-retention success and future sample passes are
experimental outcomes, not additional pre-code proof demands. Record acceptance
of the qualified B06 findings and AN-001/AN-002 in the eventual design authority.
If retaining a stronger forced-scarcity/positive-headroom requirement instead,
it remains unresolved; neither B06 nor this review invents that theorem.

### Later evidence, not current design errors

After design freeze, implementation must validate the chosen service traces,
caps, exact prefixes, typed stocks/faults, packet provenance/reachability,
all-state resets, context cancellation, no parent/probe feedback and sparse
replay. It must exercise sixteen reduced acquisition/reset tables, sixteen
production bit changes, cross-block/populated/corrupt/dead histories and
rejected-prefix/invalid-packet cases. Chance accuracy cannot replace these tests.

Then complete the required sixteen-case engineering oracle, all engineering
screening/selected-control/diagnostic products and scripted H2 validation with
every failure retained. Fix configurations and the second source/configuration/
tests/analysis/archive freeze before any final target table or private root is
drawn. No final-data access, implementation pass, engineering pass or freeze
is implied by B05 acceptance.

No repeat user-permission prompt is needed for already authorized safe ongoing
work. This request itself remains static review only and authorizes no E3
execution. Technical stage gates, not repeated consent questions, are the
remaining conditions; final seeds must stay untouched until the second freeze.

### Closure verification record and next work

Read-only PowerShell recomputed all revised products, oracle/control/prefix
arithmetic, capsule bit widths, archive components and the finite binomial
assurance expression. No PRNG, bootstrap-index generator or E3 program ran.
The initial review prefix comparison after the scope append passed for all
39311 original bytes. Final readback, diagnostic and evidence-hash checks follow
this appended decision before the acceptance response.

Two arithmetic-command syntax issues were corrected without using failed
outputs: assign foreach results before piping; parenthesize each arithmetic
term inside comma-separated arrays. This lesson is recorded only here to
preserve the single-artifact constraint, not in a new memory or script file.

Reviewed evidence identities, not freeze hashes:

| Input | SHA-256 |
|-------|---------|
| E3_EVALUATION_CONTRACT_v0_8.md | 36580bcb074e2f7e12a1708353dc9b2cefd845d5dc6a1bdd1fbbca8d7ec876a3 |
| E3_EVALUATION_CONTRACT_v0_7.md | ea3698bdb595b66eeebf8f50a75b6514166bdfdb7bbaaa16c6392e7ef6e0dae3 |
| .copilot-tracking/research/subagents/2026-09-10/e3-b06-analysis.md | c7ecd3d39a227a73c1b433ea35318c84667626bcc416552ab6f66e0ec6396303 |
| .copilot-tracking/reviews/2026-09-10/e3-b06-review.md | 008b85b4deaf1a94a18cacbc2c2f8e66710a571b2f0950fcb107c434980473e9 |
| .copilot-tracking/reviews/2026-09-10/e3-b07-information-review.md | d31f38a22948859cbfae74ec8a41bcc0fcd8b1bff472d3434bad459c7e5bd69c |
| .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md | 9d3b53757de35077b4973b619ea61bade1dc7f7c1c10edcd03b17251610a1e1f |
| .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md | c4cb49fb838834f21a125829615a073b58cae8a972fdeb33b548a459e94e4816 |

* [x] Review v0.8 against v0.7 and the initial EV findings.
* [x] Verify oracle normal prefixes, one-C bound, exact-code versus wearing-probe interpretation and counts.
* [x] Verify screening/selected controls, complete-source resets, primary mappings and B06 assurance compatibility.
* [x] Recompute roster, raw-row, snapshot, service and packed-byte bounds.
* [ ] Complete AC-01 through AC-04 without changing primary precision or numerical scientific gates.
* [ ] At the proper later stages, validate implementation, execute engineering, then complete the second freeze before final draws.

No factual clarification or renewed routine permission is required. No new
research thread, sample redesign, cloud deployment or runtime estimate is
necessary to finish this acceptance review.

### Final preservation and diagnostic check

Full closure readback completed. The exact original 39311-byte prefix is
unchanged. All thirteen captured evidence hashes are unchanged; every recorded
closure hash matches its input. The appended content has no tabs or trailing
whitespace, and editor diagnostics report no errors. These are document checks,
not implementation tests, a recursive archive audit or either freeze. The sole
written artifact is this existing review. Final status remains QUALIFIED B05
DESIGN PASS, with AC-01 through AC-04 outstanding before unconditional first-freeze
acceptance and no user clarification required.