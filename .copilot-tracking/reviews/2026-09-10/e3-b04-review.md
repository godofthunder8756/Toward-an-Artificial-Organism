---
title: Independent E3 B04 policy contract review
description: Cross-contract review of policy mathematics, information boundaries, fairness, and unresolved operational closure
ms.date: 2026-09-10
status: Complete - policy consistency reviewed; B04 operational closure pending
---

## Scope and review status

Review E3_POLICY_CONTRACT_v0_5.md in full against E3_STATE_CONTRACT_v0_2.md,
the complete revised E3_OPERATION_CONTRACT_v0_3.md, E3_PHYSICAL_CONTRACT_v0_4.md,
and the preserved E3_PROTOCOL_v0_1.md gates. This is an independent paper review,
not an E3 implementation, engineering run, design freeze, or empirical result.

Only .copilot-tracking/reviews/2026-09-10/e3-b04-review.md may be written.
All source contracts and code remain outside the write scope.

Review complete. No new Critical or High mathematical, state-lifetime, packet,
or tariff contradiction was found in the selected policy rules. POL-001 and
POL-002 identify Medium scientific interpretation limitations; POL-003 is a
Low methods clarification. They are not evidence of a bad TD formula, a leaked
target, or an observed failing policy. Exact proposed additions appear below;
none has been applied to the source contracts.

B04 remains partial and operational closure is pending, not passed. The
unverified CONTROL256/register traces and remaining B03-B07 requirements
continue to block design freeze and execution. Their explicit disclosure is
correct; an unfinished trace is not a newly discovered defect merely because
this review did not complete it. The review is complete even though those
larger design obligations are not.

## Questions under review

* Verify reward bounds, fixed-point units, TD extrema and ties-to-even arithmetic.
* Verify the 32 observation states, sensor timing, common scans, fixed policies,
  no-code-write contrast, frozen learning, and absence of H1 feedback.
* Check tuning grids, feasibility ranking, matched opportunities and objectives,
  engineering-only target reuse, and complete-reset noninterference.
* Distinguish signed incorrect-response penalties from missing-response incentives
  and assess discount-horizon and retention claim limitations.
* Reconcile the complete revised B02 gate, prefix, record, packet and scratch rules.
* Separate new defects from explicitly unresolved static CONTROL and B03-B07 gates.
* Preserve mandatory gates without adding repeated routine permission requests.

## Evidence and verification boundaries

The following normative documents were read completely, including frontmatter,
failure branches, caveats, and final closure requirements. Citations below use
these abbreviations and 1-based source line ranges, not an earlier excerpt.

* P: E3_POLICY_CONTRACT_v0_5.md, lines 1-767
* S: E3_STATE_CONTRACT_v0_2.md, lines 1-439
* O: E3_OPERATION_CONTRACT_v0_3.md, lines 1-941, the complete revised B02
* F: E3_PHYSICAL_CONTRACT_v0_4.md, lines 1-606
* H: E3_PROTOCOL_v0_1.md, lines 1-457

Additional provenance read: the full B04 policy research note, the B03 review,
and the B02 review including its appended revised-contract re-review. The older
opening B02 verdict does not supersede its later OP-001 through OP-009 closure.
Research notes and prior reviews do not override the selected contracts.

Reviewed source SHA-256 identities, unchanged at the subsequent identity check:

* P: FE174D0BDB8D8D22583E426CF74EBB680D8D471A8C447F906A104819DED791CF
* S: 0040C21E3B3A46E02000F0F9A201264A621A641686CA3658A6ED7FED3AE2E1BD
* O: F9AEB8595CC3AB0DFA47EA3F2C3F978F91C81EEB1F51F62AAE62E83B5856B019
* F: F0F05D57B5F98C171FF2956CA4BDFD00A59EDFB3579D3FBE05FB74C8001E1DC8
* H: 5A551F004024AE59E60AE25B95CA60AF61F2989FB33575C97AA774B81E804BEF

Read-only PowerShell expressions checked integer extrema, finite action-return
ranges, all 32 indices, and all 96 equally likely rank triples for each of seven
nonempty maximum-action sets. Floating-point constant calculations were used
only for illustrative discount decay, not worker arithmetic. These checks used
no target draw, RNG sampling, repository program, simulation, or E3 test runner.
No executable service or production reset test was run.

An attempted Git status query reported that the folder is not a Git repository.
No Git-diff preservation claim follows; the five source identities above were
checked directly. Only the authorized review file was authored. Editor and
format checks of that artifact are distinct from E3 operational validation.

## POL findings and exact proposed corrections

Severity here measures interpretation or methods risk, not proof of a runtime
failure. Medium warrants an explicit scientific limitation before interpreting
results; Low requests a precise methodological guardrail. No finding below
changes a selected coefficient, hypothesis, or numerical gate.

### POL-001 Medium: Missing responses escape the useful-error penalty

Evidence: P 107-156, 194-218, 334-342; O 242-249, 628-681; H 366-403.

The formula correctly assigns -64 to an emitted useful incorrect response.
P also correctly sets b=0 when a response is missing, invalid, unaffordable, or
unplanned. Therefore the task component ranks a missing useful response above a
known incorrect useful response. It does not penalize every planned recall
failure equally. The nominal clamp is inactive, so it does not remove this
difference when the action prefix is held fixed.

For a useful emitted response with correctness probability p, the expected
task contribution is $64(2p-1)$. The missing-response contribution is zero.
Thus below-chance responses have lower expected task return than silence;
independent fair guesses tie silence in this component. This comparison does
not include physical energy benefits, action return, gate costs, or subsequent
survival and therefore is not a proof that suppressing responses is optimal.

There is no direct silence action: the action set is forage, collect, scrub,
and financially admitted RESPONSE emits its decoded bit or readout-only guess.
However, O expressly allows prior action spending to leave optional decoding
unaffordable. Query corruption, lost admissions and death also produce missing
rows. Whether a policy can learn to exploit an indirect avoidance path remains
unestablished, especially under the financially sufficient HS reference.

P does not currently claim a proved no-avoidance property. The issue is the
missing claim limitation, not an incorrect signed formula. High return must not
be described as evidence that the agent avoids all errors, values answering, or
retains information. Planned-denominator recall and viability gates remain
separate and must still pass.

Exact proposed addition after P's missing-response rule:

> The signed task term penalizes emitted useful incorrect responses, not every
> planned-response failure. Missing responses receive zero, so this term alone
> can favor avoiding a likely incorrect response. There is no explicit silence
> action, and this does not establish that avoidance is feasible, learned, or
> optimal under the full physical process. Report missing and rejected responses
> separately from emitted errors, retain all planned failures in recall, and
> apply the original recall, active-fraction and completion gates independently
> of objective return.

Do not silently change missing-response b to -64. That would require supplying
scheduled usefulness/outcome information on currently packet-free paths and
revisiting B02 ownership, I/O and the objective in a prospective new version.
No-feedback recovery/H1 must never acquire such a penalty channel.

### POL-002 Medium: The discount weakly values distant retention benefits

Evidence: P 194-213, 255-293, 618-679; S 158-189; H 26-48, 350-403.

The inherited gamma=15/16 is 0.9375. It is represented correctly in
N=16r+15m-16q and the 1/128 update denominator. Its conventional geometric
discount scale is $1/(1-\gamma)=16$ steps; the half-life is about 10.7401 ticks.
Illustrative relative weights are:

* Five ticks ahead: $\gamma^5=0.7241964340$
* Sixty-four ticks ahead: $\gamma^{64}=0.01607539635$
* One hundred twenty-eight ticks ahead: $\gamma^{128}=0.0002584183678$
* Two hundred fifty-six ticks ahead: $\gamma^{256}=6.678005284\times10^{-8}$

There is no hard sixteen-tick cutoff. The five-tick address delay is not
discounted away, and near-term preservation can still benefit task return.
Nevertheless, immediate code-write costs and resource-action income can dominate
benefits that arrive much later. In the phase-start objective, the H2 final
window begins with weight gamma^256; later local TD updates are not themselves
multiplied by that absolute-time weight. Distinguish these two facts rather
than claiming that all late-phase learning is disabled.

Primary H1 recovery freezes learning and H1 evaluation supplies no learner task
return at all. H1 retention is selected and tested offline, not optimized by
direct post-challenge reward. H2 tuning also ranks useful recall before material,
not J. P already disclaims guaranteed optimization and convergence; the specific
short-horizon retention mismatch deserves its own limitation. It is a scientific
design sensitivity, not a formula error or evidence that maintenance must fail.

Exact proposed addition after the discounted-objective definition:

> With gamma=15/16, the discount scale is sixteen ticks and the half-life is
> approximately 10.74 ticks. Distant retention benefits can therefore be weak
> relative to immediate resource income and write costs. This objective is not
> a guarantee of optimizing the 128-tick recovery or final-window recall
> endpoints. Recovery learning remains frozen and H1 provides no task feedback;
> offline engineering selection and the unchanged retention gates assess those
> outcomes separately. A later discount change would be a prospective new
> design, not an arithmetic repair or outcome-conditioned retuning.

No alpha, gamma, reward, horizon, or gate change is recommended in this review.

### POL-003 Low: Make engineering pairing and reset conditioning explicit

Evidence: P 101-105, 318-330, 598-626, 668-679; S 296-338;
H 50-68, 239-286, 350-365.

Reusing one hidden target table per engineering individual across representations
and candidates is appropriate pairing. It is explicitly restricted to future
engineering IDs 1-8, with independent tables across individuals. It is not an
accidental variable that persists through worker reset and is not a reason to
draw different labels for competing arms. P forbids a transferred trained Q
table, reconstructible target key, or final-outcome-based selection.

The tuned population constants can depend on engineering outcomes. Therefore
engineering-target independence must not be claimed by treating those fitted
constants as if they had been selected without those data. Final targets must
be independent of the selected configuration. Likewise a counterfactual reset
test compares histories under the same inherited G and future Z; reselecting
hyperparameters or the input namespace separately for each target would change
the tested contract. A worker's blank bytes alone cannot repair such a change.

No actual target leak or reset defect is evidenced here. This is a clarification
of the engineering exception and the conditional noninterference argument.

Exact proposed addition after the paired engineering target-table paragraph:

> Reuse across hyperparameter-search candidates is confined to engineering and
> supplies no worker input outside declared teaching/ecological interfaces. After population
> configurations are selected, freeze them before drawing independent final
> target tables; use each final individual's table consistently across its
> prespecified comparisons. Engineering outcomes may inform those constants but
> do not constitute confirmatory evidence. Reset counterfactuals hold G and
> future target-independent inputs fixed while varying acquired history; they
> do not retune constants or preserve an answer-dependent input namespace.

This does not require a new target draw now. No target was drawn in this review.

## Verified mathematics and reward ownership

### Prefix bounds and units

P 36-105 and 158-192 satisfy O 628-681's complete revised B02 rule.

* A forage action has a=floor(F/4) in 0..16 for accepted integer F in 0..64.
  Nonmultiples of four are floored; no fractional carry survives.
* Collection has a=2C in 0..16 for accepted C in 0..8.
* Scrub has a=-W in -5..0 or -20..0. W counts completed writes only.
  Failed needed-write gates affect A, not W; clean/empty/tied/prohibited or
  rejected-entry scrubs have zero action income/cost term.
* Mutual exclusivity gives -20 <= a <= 16, not an artificial sum of both
  resource maxima. With b in {-64,0,64}, -84 <= a+b <= 80.
* One return integer means 1/256 Q units. The exchange weights are assigned,
  not an accounting identity converting all physical energy/material costs.
* The main-objective clamp is inactive for uncorrupted prefixes. Corrupted
  signed reward plus b ranges from -32832 to 32831 before clamping and must
  use signed-32 arithmetic. These corrupted states are not counterexamples to
  the nominal signed-16 prefix proof.

Store exact a, then add b and clamp once inside that tick's RESPONSE. TD reclips
the possibly damaged stored word later. Do not preclip a or retain a hidden
tick-total expense accumulator. The general B02 example a=300,b=-300 must still
give zero rather than -44, even though that example is outside this selected
main objective's narrower range.

The action METER consumes its single incoming yield, calculates accepted supply
after paid admission/body charges and caps, and permits same-operation mapping.
No second accepted-amount notification, history sensor, or reusable callback is
introduced. Rejected actions receive no yield packet. Failed writes still pay
their gates; those energy costs and all auxiliary/upkeep costs remain on the
physical ledger even though they are omitted from the direct reward.

The ecological outcome map also checks: a useful correct emission has physical
offer 64 and b=+64; useful incorrect has zero and -64; obsolete has zero and
zero. Use the originally scheduled due cue's usefulness and target externally,
not the current maintenance offer or the damaged address. Physical overflow
reduces accepted energy but not b. A signed outcome together with the emitted
binary answer can disclose the target. Both packets describe the same task
event, but are not equally informative encodings: physical zero alone does not
distinguish obsolete from useful incorrect. This is declared teaching, not
label-free feedback, and neither packet is present in recovery/H1.

### TD extrema and rounding

P 255-293 agrees with S 158-176 and O 161-180.

For arbitrary signed-16 q and m and clipped r in [-256,256]:

$$
N_{\min}=16(-256)+15(-32768)-16(32767)=-1019888,
$$

$$
N_{\max}=16(256)+15(32767)-16(-32768)=1019889.
$$

With terminal m=0, the exact extrema are:

$$
N_{\min}^{\rm terminal}=16(-256)-16(32767)=-528368,
\qquad
N_{\max}^{\rm terminal}=16(256)-16(-32768)=528384.
$$

In particular, q=32767 and r=-256 give -528368. There is no off-by-sixteen
error to correct. Terminal bounds need not be symmetric because signed-16
q ranges from -32768 to 32767.

The rounded increment lies in [-7968,7968]; the stated loose pre-saturation
sum interval [-40736,40735] fits signed 32 bits. It need not be a tight joint
bound to establish safe intermediate width. Saturation remains mandatory.
Ties-to-even examples check: N=64 and -64 produce zero, while 192 and -192
produce 2 and -2. The mathematical absolute-value definition does not mandate
extra unpriced instructions if an equivalent signed quotient/remainder trace
implements it. The separate 23-ALU conformance obligation remains open.

Nominal |r|<=84 yields |J|<5.25 for either finite learning horizon. The full
clamp scale is at most 16; the ideal Q scale is 4096 stored units. These are
discounted scale checks, not convergence, fault immunity, or retention proofs.

### One record and terminal precedence

P 173-218 preserves O 577-683:

1. Read/update or drop the old record using its current stored validity/action
   and terminal bit. Pay TD's fee on every admitted learning DECIDE, even if
   the old record is invalid, action=3, or its update body is rejected.
2. Retire the old record before current selection/storage. Reread the selection
   Q row after TD, since the updated old entry may be in that row.
3. Select one action, execute its funded prefix, then store observation,
   action and exact a. A rejected DECIDE does not acquire a free action latch.
4. RESPONSE finalizes a currently valid record once, even on invalid-slot,
   no-output, or rejected-decode paths, using b=0 when absent. It does not
   invent a record when validity is zero or consult a clean success flag.
5. Scheduled TERMINAL forces m=0 and retires the record without another tick.
   Unexpected death can lose an unprocessed record. A completed pre-fault
   terminal update is not rolled back by the later fatal fault.

The response normally belongs to an admission five ticks earlier; its b belongs
to the current one-step record. No five-record credit queue or historical action
lookup is introduced. Offline objective accounting can include a task outcome
when the learner record is absent, but cannot reconstruct that record or perform
a retroactive update. Frozen paths ignore fault-created record validity entirely.

## Observations, randomness and conventional policies

### Thirty-two indices and support-induced degeneracy

P 222-253 matches S 126-156 and O 444-469, 581-589. The mapping
s=16u+8e+4p+h is a bijection from 2x2x2x4 combinations to integers 0..31.
There are exactly 96 signed-16 Q scalars, or 1536 bits. No extra missing-cue,
query-count, age, or target-distance state is introduced.

The health priority is exhaustive and exclusive: empty first, nonempty ambiguous
second, complete agreement with a unique decode third, otherwise a degraded
unique decode. A wrong but internally agreeing codeword is h=2. Empty/all-tied
memory cannot acquire a repair value from forced readout guessing.

The paid sensor point follows the offer, full code scan, sixteen sensing energy
and four routing energy; it precedes old TD/retirement, selection, action and
current storage. Equality with a cut is high. Reserved obligations are not
already-spent resources, and later debits/deposits do not resample the bins.

Under the named fully refilled supported windows, local P is still 255 at this
point and the conservative block bound is:

$$
E\ge65535-441-512-1-4039-20=60522.
$$

Thus all grid cuts, not only defaults, give e=p=1. The nominal 32-state table
uses at most indices 12..15 and 28..31 there. The nine resource-cut pairs alias;
periodic intervals can still differ. With paired inputs the duplicate-cut
candidates cannot acquire resource sensitivity merely through search. Retain
their reported trials and deterministic tie rule rather than claim nine
independent behavioral alternatives. This already disclosed degeneracy is not
an indexing bug or a reason to enlarge the grid after outcomes.

The bound does not cover an unresolved scarce H2 profile or arbitrary stock
injury after entry. LL-EVAL13 has no H1 controller and cannot supply a missing
H2 resource-sensitive policy test. Forage can earn accepted-income reward while
neutral support supplies viability; that is not autonomous resource necessity.

### Exact random selection and input independence

P 295-330 retains O's three charged inputs, not a hidden PRNG or rejection loop.
Enumeration of all 2x3x16 triples gives these counts out of 96:

* One maximizing action: 92 for it, 2 for each nonmaximum
* Two maximizing actions: 47 for each, 2 for the nonmaximum
* Three maximizing actions: 32 for each

These equal (15/16)/k+1/48 for maxima and 1/48 otherwise. All three draws are
delivered on an admitted RL selection, including unused ranks. Invalid T=3 is
a packet-contract failure, not an action or retry. Rejected DECIDE consumes no
draw and cannot shift future indexed inputs. The categorical external generator
and its independence remain B05/B07 validation obligations.

Fault, target, opportunity, exploration, guess and analysis purposes remain
separate. No seed, individual ID, action-count cursor, future schedule, or
answer-reconstructible namespace reaches the worker. Counterfactual reset must
remove resource/history dependencies as well as code bits, as POL-003 explains.

### Periodic, threshold and no-code-write rules

P 334-427 conforms to the complete revised B02 common-scan rule, not an older
health-free periodic interpretation. Every admitted fixed or write-disabled
DECIDE pays K and sensing. Periodic scrubbing reuses that snapshot; RESPONSE
is a different cleared operation and pays for its own decode. No second scrub
scan is required and no due response is inferred from the public clock.

Both fixed policies first choose forage for low E, otherwise collection for low
local P, otherwise their named trigger. False triggers choose forage. Periodic
uses t=1+kI, does not pause or make up rejected services, and ignores u/h for
scheduling only. Threshold scrubs exactly at h=3. Empty/tied memory never
authorizes guessed correction. An admitted unique clean periodic scrub still
examines all n cells and pays generation/extraction without same-value writes;
there is no unpriced intact early exit or fallback action.

The selected protected public clock costs CONTROL work but no acquired counter
reads/writes. The unused counter starts at auxiliary bit 1773; its unaligned
boundaries would require paid preservation if a future design used it. Leaving
it fault-exposed but unused is not an invalid-counter error or extra storage.
Protected fixed ROM versus vulnerable learned Q is a disclosed rival advantage,
not matched fault tolerance or permission to hide a learned schedule in ROM.

The primary no-code-write comparison retains the same developed RL inference,
paid scan, Q faults, resource actions and epsilon. During recovery a scrub
selection pays ACTION and abstains with V=A=W=0. It does not perform all clean
loop work, replace scrub by collection, zero Q, or stop ring/age writes. Both
paired recovery branches already freeze learning. H1 then disables controllers,
corrective writes and Q updates for every arm. This is the correct inference-
preserving reconstruction contrast, not a separate no-maintenance fixed policy.

### Frozen ecology and no refresh

P 380-396 and 454-484 preserve F's conditioning and ledger laws. Frozen ecology
retains trained Q-dependent selection and exploration after funded entry/ISOLATE,
but has no transition access, store/finalization, TD gate or update. Q faults
continue. It receives only physical ecological yield, not signed learner b.

Ordinary admitted-update/finalization savings are 16+16+8+8=48 material,
twelve per source; dropped-TD paths save 40 instead. Other missing work changes
the actual difference, and terminal savings are separate. This is not a constant
refund or matched expenditure. Forty-eight exceeds a twenty-symbol block scrub,
so frozen savings remain an H2 scarcity confound for B05/B06, not a solved issue.

Automatic paid AGE-LOW, AGE-HIGH and twenty CONDITION services remain. Conditioning
resets only the declared age coordinate. It changes future hazard but restores
neither a Q value nor code. All faults use simultaneous pre-fault stored ages;
no second true age survives. Literal Q refresh would cost 768 material and
768(10+14)=18432 access energy, preserve existing corruption, and not reset age.
Selecting no refresh adds no new service or protected Q copy.

DRIVE's a_D=16 for selected scrub, including ineffective/rejected scrub, is an
explicitly different objective with combined bounds [-64,80]. It is not a fair
main-arm objective comparison. The exact-template oracle is likewise privileged
and remains a B05 branch specification, not an implied worker capability.

## Phase separation, tuning and matching

P 107-218, 365-396 and 573-679 respect these distinct phases:

* Acquisition has 256 explicit teaching ticks and no controller, query response
  or ecological task return. Fixed and RL candidates pay their own teaching work.
* Development has 2048 offered learning-phase ticks and 2043 planned responses.
  RL may receive signed ecology feedback; fixed policies use their own rules
  without unused Q/transition work. Development teaching is explicit ecology,
  not evidence of answer-free repair.
* Recovery has 128 wearing ticks, offers/resource actions, no admissions, frozen
  learning, and neither ecological feedback packet. Surviving acquired Q/code
  may affect behavior; no new answer channel is allowed.
* H1 has 261 paid response/upkeep-only ticks, 256 planned responses, no controller,
  no corrective writes/Q updates and no feedback. Scoring is offline.
* H2 has 512 ticks and 507 planned responses. Final spending/response ticks
  257-512 contain 128 U and 128 O responses, admitted at 252-507. Learning ecology
  has both outcome packets; frozen ecology has only physical yield. Both use the
  original scheduled cue externally, not the corrupted worker address.

All main arms share the action exchange weights and scheduled ecological outcome
law. Fixed/frozen arms may evaluate that objective offline without receiving an
unused signed packet. Equal permitted capacity, planned phases and opportunities
do not mean equal realized spend, feedback traffic, accepted yield or learning.
P discloses these differences; they must not be rebranded as an identical-I/O or
equal-budget-consumption comparison.

The grids are exact: nine RL cut pairs, nine threshold pairs, and nine cut pairs
times nine periodic intervals = 81 periodic candidates per representation and
endpoint family. No-maintenance has nine only if instantiated; DRIVE has one.
Paired no-code-write/frozen ablations inherit their parent's cuts and policy,
without favorable independent tuning. All trials, failures and deaths remain.

Eight engineering individuals with eight panels each are eight independent
individual units, not 64 independent individuals. Each candidate starts its own
canonical learned state, uses the same 256/2048 opportunities and paired hidden
labels/inputs, and receives no trained Q transfer. The larger periodic search is
disclosed. Select once per endpoint family, representation and policy, then keep
that configuration fixed across individuals and paired continued/devalued branches.
No per-individual, injury, panel, or branch-specific winning configuration is
loaded at runtime.

The offline lexicographic ranking is specified, not an undefined scalar reward:

1. Feasibility: intact recall >=0.90; acquisition/development active >=0.95;
   assay active and completion >=0.90, in both H2 branches when applicable.
   Structural/ledger failures stop work instead of receiving a low score.
2. Recall: H1 correction-enabled HS-AC planned-denominator R; H2 the smaller
   branch mean R_U on the same U set and 128 planned U responses.
3. Corrective material: H1's 128 recovery ticks; H2's final 256 ticks averaged
   equally over both branches, not O-only savings or the learner's margin.
4. Completion: full charged H1 assay or the smaller H2 branch mean.
5. Total paid material: full recovery plus H1 or whole H2, including stated
   entry/terminal work and excluding intervention/loss/overflow flows.
6. Ascending Ecut, Pcut and I for exact remaining ties.

The ranking uses planned failures, individual-first panel averaging and exact
means where defined. No feasible candidate means an infeasible diagnostic
nomination, not a passed prerequisite or replacement cohort. Offline recall-
oriented selection intentionally differs from J, which must also be reported.
The original H1/H2 confirmatory thresholds are not replaced by the engineering
feasible flag. The intact-probe schedule remains explicitly B05 work.

H2 cannot be tuned before its scarce calendar and feasible sourcewise opportunity
costs are selected. HS-H2-REFERENCE and LL-EVAL13 do not fill that gap. Entry
resource replacement, repeated support and possible sham/refill saturation are
already disclosed; B05 still owes the actual control products. There is no
requirement to force a positive H2 result or tune periodic to lose.

## Full revised B02 and physical compatibility

P preserves O's paid gate-before-body order and the componentwise
c+L+T+rho invariant. Material may meet equality; live energy keeps its residue.
No yield funds its own admission. Mandatory RESPONSE finalization and retirement
remain reserved even after apparent controller failure; a minimum failure shuts
down without unpaid clearing or later ordinary revival.

The complete original OP dispositions remain intact at the symbolic level:

* OP-001/OP-004: learning RESPONSE reserves its full valid-record worst case,
  including the paid valid read and one read/add/clamp/rewrite. Valid learning
  base is 636/12 before routes; invalid record is 559/4, not nonlearning 556/4.
  No missing envelope, repeated reward write or free failure path is reintroduced.
* OP-002: positive-energy admission, executed debits rather than escrow, typed
  caps, physical shutdown and one-way losses remain. Passive pre-TICK support
  is the declared exception, not current action income.
* OP-003/OP-009: old reward survives TD admission; current observation/action/a
  survive write gates in the declared scratch. Forty snapshot bits mean twenty
  two-bit symbols, not forty symbols or one fictitious 32-bit operand.
* OP-005: scrub charges gV+128A+6W plus routes, W<=A<=V<=n. Every examined clean
  cell pays g, every reached failed needed-write gate counts in A, and the first
  such rejection ends the prefix. Empty/tied/prohibited scrub pays ACTION but
  has no loop; a clean unique admitted periodic scrub has no free early exit.
* OP-006: terminal work precedes the last fault, with no rollback or posthumous
  update. Active/completion sampling still includes that fault.
* OP-007: acquisition's teaching, staging and COMMIT schedule is unchanged.
  Equal 1280 possible code writes do not erase block staging overhead. Failed
  fourth lessons do not cancel funded mandatory COMMIT retirement.
* OP-008: accepted, source-specific supplies must fund every prefix and tail.
  Financial coverage and survival do not prove recall, H1 advantage, adaptive
  headroom or H2 opportunity cost. No historical gate is weakened.

All-controller scalar counts check: RL resource eight, RL scrub six, fixed
resource five, fixed scrub three. Separate RESPONSE maxima are four for guessed
learning ecology, three for unique learning or guessed frozen ecology, and two
for guessed isolation/H1. Absent planned outputs can lower actual counts.
Sensor encoding ALUs are already in the sixteen-energy kernel; only routes are
added. Lane protocols are not extra scalar packets. No received return, time,
threshold, success, or accepted-amount scalar beyond O's inventory is introduced.

The action/write-gate decoder peak is 40+4+5+2+16+4+15+4+2=92 of 96 bits.
V/A/W replace the single loop counter; V supplies position and a is formed from
W after the prefix. Raw sensors and random ranks are dead before these gates.
Old-record load peaks at 85 and RESPONSE finalization at 47. Four 32-bit
arithmetic registers and micro-PC:16/address:11/flags:5 are retained separately.
These sums are valid slot witnesses, not proofs of all simultaneous lifetimes.

No new selected refresh/metadata tariff invalidates F's numerical HS upper
quotes, conditional on actual kernel/control conformance. Different physical
loss profiles, extra services or source calendars cannot inherit those bounds
without new prefix checks. All 276 persistent bytes, typed reservoirs, reserve,
age dependencies and scratch clearing remain within the original reset scope.

## Existing operational blockers and scientific gates

P 522-571 and 733-767 correctly withhold full B04 closure. The worksheets are:

* Learning RL scrub: 144+12n = 204 for repetition, 384 for block
* Frozen fixed scrub: 104+12n = 164 for repetition, 344 for block
* RESPONSE planning allowance: 112 CONTROL slots

The block worksheets exceed 256, but they are conservative approximate
allocations, not proved minimum instruction counts. A tighter actual trace may
fit. Conversely, neither these worksheets nor the sub-256 repetition/RESPONSE
sums certify conformance. The actual trace must separate CONTROL from bundled
lane work, decoder kernels, TD/selection, scalar encoding and METER comparisons;
it must verify each register lifetime and rejected/terminal/fault-state path.

This is an existing mandatory closure blocker, not a new POL error assigned for
unfinished work. It is not permissible to mark operational closure passed,
borrow unused scan/selection padding, enlarge CONTROL, or split an atomic
operation while retaining unbudgeted scratch. A genuinely changed service needs
prospective versioning and pricing. F's 22 upkeep services and O's other services
have their own still-required trace obligations.

The retained scientific gates also remain independent:

* H1 RL-minus-no-code-write R >=0.05 with positive paired lower interval;
  RL R >=0.80, active >=0.90, and at least one paid reconstruction write
* Separate RL-minus-tuned-periodic R >=0.05 with positive paired lower interval
* H2 O-write reduction >=50% versus continued usefulness and >=10% versus
  periodic, with the specified positive paired reduction intervals
* H2 R_U >=0.80, active/completion >=0.90, and upper paired interval for
  continued-minus-devalued R_U <=0.05
* Intact recall >=0.90, active >=0.95, exact ledger/information tests, and
  production reset noninterference plus powered accuracy interval in [0.45,0.55]

H2 ratios retain zero-reference individuals and use aggregate individual means;
zero aggregate denominators are undefined and cannot pass. Panels are repeated
measures within individuals. The proposed 10000 paired bootstrap draws require
a later frozen analysis RNG; the candidate 32-individual/eight-panel final design
is not justified or frozen here. Imprecision is inconclusive, not evidence of
erasure or automatic evidence of leakage. Conventional failure is an allowed
research outcome and does not authorize outcome-conditioned support or gates.

## Complete policy-document coverage

* P 1-33: selected partial status and unchanged contract authority checked
* P 34-106: action units, accepted-yield ownership, prefix costs and omissions checked
* P 107-157: signed/physical ecological outcomes and isolation separation checked;
  POL-001 records the missing-response limitation
* P 158-219: exact bounds, record ownership and discounted objective checked;
  POL-002 records the retention-horizon limitation
* P 220-294: all health/observation indices, paid sensor point and Q arithmetic checked
* P 295-331: complete rank distribution, streams and reset namespace checked
* P 332-453: fixed policies, no-write/frozen contrasts, clock and DRIVE checked
* P 454-485: conditioning, no refresh, RAM capacity and protected-ROM caveat checked
* P 486-572: packet counts and slot witnesses checked; static CONTROL remains open
* P 573-680: exact grids, engineering pairing, feasibility and objective ranking
  checked; POL-003 clarifies the engineering/final/reset distinction
* P 681-732: support degeneracy, preserved numerical gates and failure outcomes checked
* P 733-767: remaining B04-B07 work and absence of claimed execution checked

## Recommended next work not completed in this review

No additional literature search is needed to answer this review's questions.
The following bounded design and later validation work remains:

* [ ] Incorporate the exact POL-001/POL-002 limitation text and POL-003 methods
  clarification through a separately scoped authorized contract update.
* [ ] B04/B03: complete static instruction/register traces for all selected
  services, including the block scrub, signed TD rounding, sensor/threshold
  boundaries, record corruption, forbidden writes and mandatory failure tails.
* [ ] B05: finalize scarce H2 support/opportunities, paired branch/profile/channel
  products, intact-probe/clone funding, entry/refill/sham/oracle controls, target
  and input manifests, and planned output rows before executing those choices.
* [ ] B06: establish sourcewise feasibility and viable H2 opportunity cost despite
  frozen savings; assess H1 reconstruction and adaptive-over-periodic headroom
  separately; justify dependent-output erasure precision and final sample size.
* [ ] B07: finish worker/scorer/physics ownership and the all-276-byte reset proof
  obligations, then archive the design-only manifest only after design gates pass.
* [ ] After the design gate, perform implementation and validation, engineering-only
  runs, and a separate source/configuration/test/analysis freeze before untouched
  final targets and confirmatory execution. Preserve failures and inconclusive
  outcomes instead of extending the search until a positive result appears.

The user has authorized autonomous continuation of the finite research workflow.
Routine research, review and verification phases do not require fresh permission
at each step; technical freeze and validation gates remain mandatory. References
to later authorization are not a reason to ask the same routine question again.
For this delegated review, the explicit sole-file write boundary still applies:
no source-contract edit, artifact outside this report, implementation or experiment
was undertaken.

## Clarifying questions

None. The original review questions are answered. Remaining blockers require
design work and evidence, not a user preference or renewed routine consent.
