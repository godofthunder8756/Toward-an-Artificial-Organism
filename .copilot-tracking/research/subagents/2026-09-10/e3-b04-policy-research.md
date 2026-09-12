---
title: E3 B04 policy research
description: Bounded design-only decisions and evidence for the conventional policy contract
ms.date: 2026-09-10
status: Complete - bounded research; B04 operational closure pending
---

## Scope and questions

Select exact action and same-tick ecological returns, signed arithmetic bounds,
paid observation bins, random ranks, conventional policy rules, tuning grids,
and refresh policy without simulation or code. Determine whether B04 can close
symbolically and identify the remaining B05-B07 dependencies. Write only this
note and the new policy contract; preserve all prior artifacts.

## Evidence read in full

* E3_OPERATION_CONTRACT_v0_3.md: single transition, eight scalar occurrences,
  paid common scan, exact action prefix, RESPONSE ownership, CONTROL256,
  scratch partitions, tariffs and ordering.
* E3_STATE_CONTRACT_v0_2.md: 32 observations, 96 signed-16 Q entries, fixed TD
  constants, finite metadata, canonical reset and target-independent inputs.
* E3_PHYSICAL_CONTRACT_v0_4.md: HS-AC and LL-EVAL13, automatic conditioning,
  current-age hazard law, no selected Q refresh, high-support H2 reference
  distinct from still-unselected scarce H2, and sourcewise funding bounds.
* E3_PROTOCOL_v0_1.md: ordinary ECC/RL reference, fair main-arm objective,
  diagnostic fixed drive, prospective H1/H2/erasure gates and engineering IDs.

## Initial findings

* Select accepted resource returns, not a bonus for choosing collection or
  avoiding obsolete storage. Charge completed corrective writes directly.
* Ecology is an explicit task-learning channel; isolation and H1 have neither
  physical task yield nor learner-feedback packets.
* Common paid scan is required even for no-write and periodic controllers.
* Frozen learning removes bookkeeping expenditure; equal opportunities cannot
  be reported as matched actual spend.
* Literal Q refresh cannot restore a damaged value and has no conditioning
  effect under B03. Select no Q refresh for primary policies.
* A public target-independent phase clock can implement a periodic ROM rule;
  it cannot reconstruct a learned individual-specific service schedule.

## Decisions and bounded proofs

Selected deliverable: E3_POLICY_CONTRACT_v0_5.md. It is a new design candidate,
not a freeze or an amendment to the four source contracts.

### Objective and information boundary

Select a=floor(F/4)+2C-W, where F is accepted forage energy in 0..64, C is
accepted local material in 0..8, and W is completed corrective code writes in
0..5 or 0..20. Only one action executes. Thus a is in [-20,16], not the looser
sum of mutually exclusive resource maxima. Failed gates, clean/empty/tied
scrubs and capped-away resource yield do not earn an attempt bonus.

The floor is necessary for a cap-truncated forage yield not divisible by four;
there is no hidden fractional residue. The cost coefficient is one return
unit per real code-write material unit. It deliberately omits direct rewards
for neutral support, upkeep, auxiliary traffic, gate attempts and energy
overhead, all of which remain physically charged and reported.

Select physical ecological offer 64vc and signed learner term b=64v(2c-1),
with scheduled-response usefulness v and correctness c. Useful correct gives
(64,+64), useful wrong (0,-64), obsolete (0,0). Physical cap overflow does not
change the assigned task term. No emitted/planned response means no feedback
packet and b=0. The two packets refer to one synchronous outcome. The signed
term distinguishes useful failure from obsolescence; with the emitted binary
bit it can disclose the target. This is explicitly task teaching, not evidence
of example-free repair.

Main-objective a+b is in [-84,80]. Exact a is stored; RESPONSE adds b and
clamps once, without an extra return packet or callback. Corrupted reward plus
b uses a signed-32 temporary in [-32832,32831]. TD clips again after faults.
The nominal discounted objective uses gamma=15/16, the common r/256 scale,
and the fixed learning-phase horizon. Its sum is offline evaluator accounting,
never an extra worker accumulator. Missing worker records are not recreated
from that accounting. Every main arm shares these weights and outcome law.

Rejected alternatives were attempted-resource income, true-damage reduction,
visible-health improvement, a bonus for avoiding obsolete storage, and reserve
potential shaping that would need further observations. The accepted-resource
formula contains no target input, but realized returns can depend on acquired
reserves/memory. Complete-reset independence still requires removing those
histories; function-level answer independence is not a statistical proof.

Evidence: E3_OPERATION_CONTRACT_v0_3.md, scalar inventory and RESPONSE ownership;
E3_STATE_CONTRACT_v0_2.md, temporal/erasure boundary; E3_PHYSICAL_CONTRACT_v0_4.md,
bounded opportunities; E3_PROTOCOL_v0_1.md, common objectives and ecology caveat.

### Observations, Q and ranks

Select default Ecut=32768 and Pcut=64, with equality high, from the single
paid E/local-P observation after the sixteen-energy sensor kernel and four
route energy, before TD/retirement/action. Use h=0 empty, h=1 nonempty tied,
h=2 fully observed agreeing unique decode, h=3 other unique decode.
Index s=16u+8e+4p+h. A wrong but agreeing word can be h=2.

Retain exactly 96 signed-16 Q parameters, 1,536 bits, 1/256 scale, alpha=1/8,
gamma=15/16, epsilon=1/16, the inherited roundEven/saturation update and one
transition. The TD numerator is in [-1019888,1019889] with clipped reward and
arbitrary damaged Q; terminal bounds are [-528368,528384]. Rounded increments
are at most 7968 in magnitude. No convergence or affordable-update guarantee
follows from ordinary Q learning with this observation aliasing and corruption.

Select independent indexed B in {0,1}, T in {0,1,2}, X in 0..15. Explore iff
X=0 using T. Otherwise rank maxima in ascending action order, using B for
two maxima and T for three. A three-valued primitive is not two bits modulo
three; invalid encoding 3 is a contract error, not a retry. Exact external
categorical provenance remains a later input-generation obligation. No target
seed, run ID, schedule key or action-count RNG cursor enters the worker.

Evidence: E3_STATE_CONTRACT_v0_2.md, observation/learner and finite state;
E3_OPERATION_CONTRACT_v0_3.md, selection kernels and controller lifetime.

### Fixed policies, write prohibitions and refresh

Select fixed resource priority: low energy forage, otherwise low local material
collect, otherwise the named trigger. Periodic triggers at t=1+kI with default
I=8 using the protected public phase clock. Threshold triggers exactly at h=3.
Neither uses target labels, online outcomes or a per-individual schedule.
Both pay the revised B02 common health scan. Periodic reuses the scan snapshot
for scrub rather than scanning twice. No failed action falls back or retries.

The available eight-bit periodic counter is not used. A power-of-two period
uses charged subtraction/mask/comparison in CONTROL, adds no metadata service,
and cannot encode an acquired cue schedule. The counter's unaligned starting
offset 1773 would need preservation/merge work if later used. No reserve,
visit-count or additional parameter storage is activated.

The paired H1 no-code-write arm retains its developed RL/Q inference and paid
scan; only corrective writes are disabled. A selected scrub pays its gate and
abstains. Recovery learning is frozen in both branches. H1 has no controller,
actions or ecological packets. Fixed/no-learning ecology does not receive
unused signed feedback or create a transition.

Frozen ecology removes 48 material on the ordinary valid-update/finalization
path, twelve per source, with path-dependent actual savings if work drops.
This is not matched actual expenditure. All resource opportunities, capacity,
physical losses and unused allocation remain disclosed.

Select no literal Q refresh. B03 conditioning consumes medium and resets only
the stored domain age, with h(a)=0.001(1+a), e(a)=0.0001a. It never rewrites Q
or restores its old sign. Reaffirming all 768 Q lanes would cost 18,432 access
energy and 768 material without fixing an unknown corrupted value or resetting
domain age. A repairable Q representation is a deferred new mechanism.

Select separate DRIVE diagnostic a_D=16 for a selected scrub, zero otherwise,
with b_D=b. It intentionally rewards a choice even when no repair succeeds.
Bounds are a_D in [0,16], a_D+b_D in [-64,80]. Its assigned objective is not
included in fair main-arm claims. An exact-template oracle remains privileged.

Evidence: E3_OPERATION_CONTRACT_v0_3.md, revised common-scan and frozen service
costs; E3_PHYSICAL_CONTRACT_v0_4.md, conditioning/no-refresh law and frozen
savings; E3_PROTOCOL_v0_1.md, main arms and diagnostic distinction.

### Finite tuning and concrete defaults

Defaults are cuts (32768,64), periodic I=8, threshold h=3, and no refresh.
The only future grid is Ecut in {24576,32768,40960}, Pcut in {32,64,96},
with nine RL/threshold cut pairs and 81 periodic candidates after crossing
I in {1,2,4,8,16,32,64,128,256}. DRIVE is a single configuration. Ablations
inherit parent parameters and have no independently tuned favorable variant.

Use future engineering IDs 1-8 only, eight panels each as repeated measures,
the same hidden label table per individual across candidates, and equal
256/2048 acquisition/development opportunities. No engineered table transfers
between candidates. These are not final individuals or final held-out panels.
No engineering may run before the design-only freeze and later authorization.

Preselect lexicographic ordering: feasibility flag, higher mean R for H1 or
higher minimum branch mean R_U for H2, lower corrective material, higher
completion, lower total paid material, then deterministic ascending grid order.
This is explicitly an offline multiobjective selection, not unspecified
online reward shaping. O-write reduction and the desired learner margin are
not tuning targets. Failed/dead individuals remain. No feasible candidate
means an infeasible diagnosis, not replacement individuals or a passing gate.

H1 and H2 have separately declared population-level selections, fixed across
individuals and paired branches, never per outcome. H2 tuning waits for the
scarce profile; the supported reference cannot substitute for it. B05 must
still finish the exact intact-prerequisite probe schedule and input manifest.

Evidence: E3_PROTOCOL_v0_1.md, engineering-only tuning, gates and denominators;
E3_STATE_CONTRACT_v0_2.md, no new acquired parameter capacity.

### What is and is not symbolically closed

All requested policy choices have explicit selections and bounded mathematical
definitions. The full controller still lacks CONTROL256 conformance. The
conservative non-kernel worksheet is 144+12n for learning RL (204 repetition,
384 block) and 104+12n for frozen fixed policies (164 repetition, 344 block).
These are approximate allocations, not implemented upper-bound proofs or
minimum requirements. Exceeding 256 in a conservative estimate is not an
impossibility proof, but cannot be presented as successful conformance.
Tighten actual bounded traces or version/reprice a changed service before
freeze. No extra control, scratch lifetime or scan padding is silently granted.

Scalar limits hold at the interface: full RL resource controller eight, RL
scrub six, fixed resource controller five, fixed scrub three; RESPONSE at most
four. Prefix counts and current return fit the inherited 92/96-bit action
scratch witness, conditional on a complete register/slot trace. No simulation,
static executable checker or microcode was used to establish more than that.

Under full supported entry/refill, the selected observation has local P=255
and E at least 60522 for block. All grid cuts are high there. Neutral support
can make forage unnecessary for survival while still paying its assigned
return; tuning cannot manufacture resource-bin sensitivity in that reference.
HS-H2-REFERENCE is not scarce H2, and LL-EVAL13 is an H1 diagnostic only.

The earlier candidate final sample (32 individuals/eight panels) remains
unfrozen. No H2 pass is a required procedural deliverable if the conventional
reference fails. Preserve rejection/unevaluable/inconclusive outcomes rather
than selecting favorable support or lowering five-point gates.

Evidence: E3_OPERATION_CONTRACT_v0_3.md, finite control and scratch obligations;
E3_PHYSICAL_CONTRACT_v0_4.md, support prefix arithmetic and incomplete H2;
E3_PROTOCOL_v0_1.md, rejection and precision rules.

## Review and validation

Read the new policy contract in full and checked it against the four fully
read source contracts. Self-review corrected an imprecise RESPONSE packet
count, made low-resource priority explicit inside both fixed-rule descriptions,
and distinguished literal target packets from reconstructible ecological task
information. It also added the explicit discounted objective and paired-label
engineering rule. This is self-review, not an independent validator approval.

Editor diagnostics reported no errors in the two new Markdown files before
final cleanup; final diagnostics are checked separately. No terminal command,
simulation, Python execution, data analysis, historical replay or final target
inspection occurred. Only the two authorized new documents were written.
No repository-wide preservation/hash audit or design freeze is claimed.

## Recommended next research

* [ ] B04/B03: complete non-kernel primitive and register traces, particularly
  block scrub, without exceeding CONTROL256 or existing kernels/scalar caps.
* [ ] B05: choose scarce H2 sourcewise support/opportunity calendar and complete
  branch/profile/channel, intact-probe, entry, stream and output-row manifests.
* [ ] B06: prove viable H2 scarcity/gains and positive reference denominators
  despite conditioning contention, dropped TD and the frozen subsidy.
* [ ] B06: establish H1 functional and adaptive-over-periodic headroom separately;
  select final sample/panels from prospective erasure-precision assurance.
* [ ] B07: complete ownership, operational review and production noninterference
  obligations before a design-only freeze and any later authorized execution.

## Clarifying questions

None require user input for this selection. The remaining issues are design
and verification blockers, not authorization to implement or simulate E3.