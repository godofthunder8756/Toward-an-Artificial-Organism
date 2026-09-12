---
title: E3 B02 independent full-document review
description: Critical review of operation prices, finite-state lifetimes, failure semantics, and necessary affordability bounds
date: 2026-09-10
---

## Status and scope

Review complete; B02 requires revision before claiming specification closure.
The fused controller, vulnerable query ring, paid retirement, and explicit
abstract-machine tariffs constitute substantive progress, not demonstrated
feasibility or automatic success.

Read completely, including frontmatter and final sections:

* E3_OPERATION_CONTRACT_v0_3.md, lines 1-495
* E3_STATE_CONTRACT_v0_2.md, lines 1-439
* .copilot-tracking/research/subagents/2026-09-10/e3-b02-operation-research.md,
  lines 1-513

Evidence below uses O, S, and R respectively, with 1-based line ranges. O is
the selected operation schedule; R supplies calculation provenance, not
competing normative rules. No external sources, simulations, implementation,
model validation, or empirical performance tests were used. Scalar arithmetic
was checked. Only this review artifact was authored; prior documents were not
edited and no additional research note was created.

High findings block B02 closure or materially affect gate interpretation.
Medium findings require explicit specification choices. Low denotes a wording
error. Unknown B03 routes/rent/yields and B04 objective constants are named
dependencies, not findings merely because their numerical values are pending.

## Review questions

* Are gate reservations, mandatory tails, scratch lifetimes, and shutdown rules
  consistent without hidden acquired state?
* Are accepted, rejected, partial, terminal, teaching, and query paths priceable,
  including reward finalization and source-specific material costs?
* Do the decoder and TD counts match their declared primitives and capacities?
* What necessary B03 supply bounds follow, and how do they constrain the
  original active/completion and functional gates without changing them?

## Findings

### OP-001 High: Mandatory RESPONSE work escapes the minimum-tail definition

Evidence: O 108-110, 179-207, 216-221, 314-334; R 199-210.

The tail enumeration omits reward-field finalization, although RESPONSE requires
it on every learning path. Generic rejection forbids body reads and CONTROL,
whereas RESPONSE requires a slot read even when invalid and may need a valid-bit
read, reward read, clamp, and rewrite. A rejection budget of METER, scratch clear,
and slot retirement cannot execute those requirements. The later instruction to
reserve finalization does not resolve the incompatible minimum-path definitions.

Exact correction: separate a mandatory RESPONSE base from an optional decode
body. Make the base's reads, finalization, control, and slot retirement part of
the public tail, including on decode rejection. Reserve the possible valid-record
case before any learning controller/action, without remembering controller
success in an external latch. After a paid valid check, an invalid record may
skip reward access; unused reservation stays in the physical reservoirs.

One concrete tariff consistent with that correction is one base METER, CONTROL,
and scratch clear; four slot READ2; one transition-valid-lane READ2; eight reward
READ2 and eight WRITE2 when valid; four clamp ALUs; and four slot-clear WRITE2.
Its learning worst-case base is 507 energy and 12 material before transport.
An emitted scalar adds one addition ALU; optional decode admission pays its own
METER and decoder/I/O costs. Explicitly adopt this decomposition or give an
equally complete alternative, rather than charging an ordinary rejection.

Use one read-add-clamp-write finalization, not an intermediate reward write
followed by an unpriced second rewrite. The 72-energy reward access price excludes
the separate valid read and arithmetic. This keeps the stated eight reward-write
lanes per tick defensible.

### OP-002 High: Exact-debit execution conflicts with absorbing zero energy

Evidence: O 103-104, 185-192, 223-234, 249-268, 328-334.

Affordability currently admits equality, while E=0 is physically absorbing.
Service/exit envelopes can be prepaid before their work executes. If a last
debit reaches zero, the text does not say whether prepaid output, cleanup,
deposit, or learning may still execute. Atomic fault protection is not permission
to continue a dead worker, and an unrecorded transaction-live flag would defeat
the selected physical-state rule. Not every such path necessarily revives, but
the boundary case is undefined.

Exact correction: require a one-energy survival residue at every live admission,
subgate, and minimum-tail check. Entry must cover the gate fee, minimum rejection
or retirement exit, future tail, and one energy. Pay the fee; only then compare
the remaining resources against the body bound, local mandatory exit, future
tail, and one energy. Do not give rejected bodies a free preliminary test.
Material comparisons may allow equality. Debit costs before deposits; no deposit
or output is permitted from
E=0. Apply caps when the deposit actually occurs. A failed minimum check sinks
remaining E, stops agent work, and leaves unpaid persistent retirement undone.
Alternatively version a different zero-energy rule explicitly; do not implement
boundary-only death while retaining the current absorbing-state claim.

### OP-003 High: The subgate liveness argument drops still-live values

Evidence: O 174-199, 272-304, 419-433; S 109-123, 179-189.

The assertion that only scan/decoded data survive per-write gates is incomplete.
The current observation must survive until record storage; the selected action
must survive or be reconstructible from the charged micro-PC. Any B04
prefix-dependent action return also needs an accounted accumulator or paid
recomputation. Gate comparison registers cannot silently overwrite these values.
TD-before-Q-load is a useful witness for that particular gate, not all gates.

Exact correction: document a bounded slot/liveness table for TD, selected-action,
per-code-write, RESPONSE, and teaching gates. Include observation, action,
current return if needed, scan, decoded payload, address, loop position, predicate,
quote component, and local exit obligation. A public tick/substep may select a
ROM tail; an acquired-dependent internal PC or address must occupy scratch.
No quote, successful-reservation flag, spent total, or unused-credit counter may
survive operation exit outside the declared fields.

State the no-escrow invariant explicitly: every optional debit preserves the
componentwise local mandatory remainder plus the public future tail, and the
positive energy residue from OP-002. Recompute immutable bounds or keep bounded
scratch intermediates; never subtract from a hidden reservation account. This
requests a specification witness, not a claim that a 256-bit fit is impossible.

### OP-004 High: Fixed CONTROL256 is not a complete service quote

Evidence: O 73-79, 94-121, 164-170, 185-207, 249-268, 435-437,
472-495; R 482-485; S 406-411.

A fixed 256-slot envelope is a legitimate declared abstract-machine assumption.
No finding asserts that it must be hardware-derived or that a future trace cannot
fit. O correctly disclaims implemented traces. However, an envelope does not
determine the number of envelopes/gates, mandatory rejection services, routed
I/O messages, or excluded kernel invocations. RESPONSE's initial and post-read
admissions, the tick METER's own exit, and the additional tick-end scratch clear
are not reconciled into a service ledger. Forage/collection lack an explicit
body/packet tariff interface. These prevent a unique symbolic operation price,
even if numerical G and B03 supplies were handed to an implementer.

Exact correction: add a per-service path table for tick entry, controller core,
TD subgate, each action, RESPONSE base/decode, ADMIT, lesson, COMMIT, TERMINAL,
and boundary clearing. Give counts of METER, CONTROL, scratch clears, lane
accesses, explicit ALUs, and inbound/outbound flits, including failed gates.
Say whether the tick-end clear is an additional eight energy or already one
named exit. Expose B03 service costs and B04 packet widths as named, bounded
inputs where appropriate, not unpriced helper calls. Then write each quote as
a function of those inputs. This does not require choosing their numerical values.

Until then replace "selected priceable service schedule" with "selected tariff
and partial service decomposition; B02 pricing/lifetime closure pending review."
Do not mark all opcode costs complete. Retain the separate later requirement for
static implementation traces within CONTROL256 and the 256-bit scratch budget.

### OP-005 Medium: Price regeneration for examined scrub cells, not only writes

Evidence: O 132-148, 289-295, 414-433; R 345-365.

The fixed block scan keeps the winning four-bit payload and observed symbols,
not a retained twenty-bit winning codeword. Determining whether a binary cell
disagrees therefore requires regenerating its expected bit even when no write
follows. "Extra generation for rewriting" does not identify whether the six
ALUs are charged only on WRITE2 or on each examined symbol. Billing only written
symbols gives clean comparisons free parity work.

Exact correction: for the stated fixed-order scrub, define V examined cells,
A funded needed-write gate attempts, and W completed writes, with W <= A <= V.
Charge block regeneration 6V, each attempted gate 128, and each completed WRITE2
6 before routes, plus comparison/control work under its specified envelope.
Count the first rejected gate when its METER was paid. Include corresponding
repetition extraction work under its declared rule. An explicit intact-scan
early exit or a retained generated word would be a separately specified path
with its own work/liveness accounting, not an invisible optimization.

### OP-006 Medium: Terminal success and death need explicit event precedence

Evidence: O 223-234, 249-268, 345-348; R 263-289.

The selected schedule already places TERMINAL before end-of-tick faults. Preserve
that choice; it is not an error to flush before a later fatal fault. The remaining
ambiguity is the interaction with OP-002 and what counts as completion if the
last fault kills the worker after a funded response/flush.

Exact correction: specify these cases separately:

* Gate/minimum failure before TERMINAL causes shutdown; no later flush runs.
* A rejected optional TD kernel still executes funded record retirement.
* A completed TERMINAL update/clear remains completed if the following fault
  reduces E to zero; no rollback or retroactive missed response occurs.
* Faults may alter just-cleared bytes, but those bytes do not become a protected
  pending callback or authorize posthumous learning. Nonlearning entry rules
  still apply, and ordinary support cannot reactivate the worker.

B05 must define active-tick and completion sampling relative to the final fault.
Preserve planned rows and distinguish service completion from boundary survival;
neither a corruptible flag nor an offline snapshot may decide eligibility.

### OP-007 Medium: Acquisition admission and ordering remain incomplete

Evidence: O 194-203, 247-268, 365-395; S 273-289; R 299-320.

The selected whole-block staging transfer correctly supersedes R's three-stage
validity protocol. Its 36-energy/four-material access count is correct; rejecting
it must leave the old block unchanged. A failed fourth lesson must not cancel
the scheduled COMMIT or replace stored-valid testing with an authenticated
success flag. The exact live-tick list, however, has no lesson/COMMIT positions,
and repetition's five attempts lack an explicit all-or-nothing versus
per-write-prefix admission rule. That distinction changes cost and failure paths.

Exact correction: add the acquisition-specific B02 ordering: tick support/minimum
check and living/dues, LESSON, scheduled fourth-lesson COMMIT, specified metadata
dues, then fault/boundary. State explicitly whether there is any RESPONSE service
on acquisition ticks; absence of admissions alone does not answer this. Choose
and price repetition prefix gates, including failed attempts, or explicitly
choose whole-lesson admission. For block COMMIT price the staging read, validity
test, generation, write gates, and exactly one full staging retirement. Reserve
that retirement already in the fourth lesson's tail. B05 may enumerate the
calendar later; these atomic paths must not be left to implementation inference.

### OP-008 High: Affordability conclusions must cover both codes and both gates

Evidence: O 439-466; S 232-237, 346-372, 425-428.

The published 2,068 material and decoder-only H1 totals are correct. The weaker
statement that block needs new power while repetition merely needs checking
misses a decisive bound already implied by the envelopes. Also, successful
admission/response coverage is not identical to living through the horizon.
Do not use the full-service material bound alone as a definition of completion.

Exact correction: add the necessary bounds below to B03/B06 acceptance criteria.
Reject the no-replenishment, single-inventory configuration for full H1 service
for either representation. Unknown routes/rent/hazards cannot rescue a lower
bound that already fails with all of them omitted. A prospectively declared
external subsidy may change feasibility, not establish that functional or
adaptive gates pass. Do not lower the original gates or select support after
observing a winner.

### OP-009 Low: Decoder scratch uses forty bits, not forty symbols

Evidence: O 414-417; S 117-123; R 367-373.

"40 symbols" contradicts the claimed 64-bit subtotal. Replace it with
"40 observed-code bits (twenty two-bit symbols)." Then
40 + 4 + 4 + 3 x 5 + 1 = 64 of the 96 decoder bits. This corrects the unit,
not the allocated capacity or an implemented liveness proof.

## Verified arithmetic and nonfindings

The following checks support the review; they are not model validation.

* The allocation is 2,464 total bits and 2,208 persistent bits, or 276 bytes.
  The reward field starts eight bits into the 32-bit transition, so its sixteen
  bits are aligned to eight two-bit lanes. No masked neighboring-bit write is
  needed for a complete reward rewrite.
* Repetition scan: 2 + 5 x 5 + 12 + 5 + 5 = 49. Block scan:
  64 + 16 x (2 + 20 x 11 + 6) + 7 + 20 + 20 = 3,759. The six parity steps can
  be AND, shift, XOR, shift, XOR, final AND. Empty/tied live abstention is
  consistent with the state contract. These are declared kernel counts,
  excluding transport/envelopes, not universal decoder lower bounds.
* Q read/rewrite prices are 25/48. Nonterminal TD is
  25 + 75 + 4 + 23 + 48 = 175; terminal TD is 25 + 1 + 23 + 48 = 97.
  The numerator extrema are -1,019,888 and 1,019,889, within signed 32 bits.
  The 24 selection slots and CONTROL256 are padded design assumptions, not
  independently executed opcode traces.
* O's READ2/WRITE2 prices include route lookup and insertion/extraction. R's
  earlier 32-energy Q rewrite and 64-energy record store exclude those bundled
  ALUs. They are provenance subtotals, not competing selected prices. Do not
  charge the bundled ALUs a second time.
* For source assignment s(l), material is
  $C_{P,j}=\sum_{w\in W}\mathbf{1}\{s(l_w)=j\}+U_j$.
  Count same-value writes, full erasures, staging, Q, and bookkeeping; rejected
  writes consume no write material. If upkeep's actual lane writes are already
  in W, $U_j$ contains only additional physical upkeep consumption. Gate fees
  consume energy, not an invented material charge. Sum-of-pools affordability
  does not replace the four separate inequalities.
* The 48/56 material bookkeeping totals are valid for their stated funded
  learning/admission paths, not universal tick minima. Nineteen 56-unit ticks
  require 1,064 material; maximum initial stock is 1,020. Final terminal writes,
  repair, ages, and status costs are additional.
* Full acquisition code writes are 1,280 for each representation. Selected block
  staging adds 256 x 4 = 1,024 lane writes; 64 retirements add 256. Thus block
  acquisition alone needs at least 2,560 material, versus 1,280 for repetition,
  before other services. Full stock deficits are at least 1,540 and 260,
  respectively. These are full-write-path bounds, not assertions that every
  permitted partial acquisition must finish all writes.
* Five-slot timing, H1 256 responses, H2 507 total/256 endpoint responses,
  H2's 128 U/128 O endpoint split, and development's 2,043 responses agree.
  ADMIT failure leaves a retired slot blank; an invalid/underfunded response
  emits no bit. A wrong acquired address is not repaired from the scorer.
  Later fault-created false validity is corruption, not permission for a hidden
  retry. Unfunded retirement means shutdown with unchanged bytes, not a free clear.

### Exact reward-prefix obligation for B04

O 336-343 and R 243-261 correctly leave numerical returns to B04. This dependency
is not an error. Make its acceptance condition mechanically checkable. For
attempted-action contribution a and same-tick response contribution b:

$$
-32768\le a\le32767,\qquad
-32768\le a+b\le32767,\qquad
r=\min(256,\max(-256,a+b)).
$$

These bounds apply to every permitted failed/partial action and response path;
use b=0 when no scalar contribution is produced. Compute exact integer sums
within the declared scratch/field widths. Do not first clamp a: a=300, b=-300
must finalize to zero, not -44. No tick-total cost accumulator is permitted.
Later consumption reclips a possibly corrupted stored reward. With no faults
between controller storage and RESPONSE, the new uncorrupted prefix can remain
exact until the single finalization write. No additional reward-bearing event
may be added after RESPONSE without revising ownership and tails.

## Necessary B03 bounds and original gate implications

For full H1 service, ignoring routes, rent, upkeep, sensing, faults, tick METERs,
additional subgates, and boundary costs, the existing schedule already requires:

$$
W=261(4)+256(4)=2068,
$$

$$
E_{\min}(K)=261(16+12+24)+256(24)
 +(261+256)(128+256+8)+256K.
$$

Here 12 is the four-lane slot read, 24 its clear/admission write price, and
K is 49 or 3,759. Each funded RESPONSE, including the five invalid warm-up slot
reads, and each successful ADMIT pays an admitted-operation envelope. Therefore:

* Repetition: $E_{\min}=234924$, requiring at least 169,389 accepted added energy
  beyond a full 65,535 initial reservoir
* Block: $E_{\min}=1184684$, requiring at least 1,119,149 accepted added energy
  beyond that reservoir
* Either code: at least 1,048 accepted added material beyond four full pools

These are conservative necessary lower bounds, not final quotes. OP-001's
optional decode gate, tick metering, positive live residue, and every omitted
physical cost can only increase the corresponding full-service requirement.
Even repetition cannot complete full H1 service from the single energy reserve.

For each source j and every execution prefix t, B03 must satisfy:

$$
P_j(0)+G^{\mathrm{accepted}}_j(\le t)
\ge W_j(\le t)+U_j(\le t)+L_j(\le t).
$$

For every prefix required to remain live under OP-002:

$$
E(0)+G^{\mathrm{accepted}}_E(\le t)
\ge C^{\mathrm{debits}}_E(\le t)+L_E(\le t)+1.
$$

At each gate, current resources must additionally cover its componentwise
mandatory reservation. The loss terms denote physical losses, not expenditure;
accepted grants exclude cap overflow. H1 has neither allocator
collection nor ecological yield, so those cannot supply its deficits. Total
grants arriving after a failed gate cannot satisfy a prefix constraint, and
ordinary grants after shutdown cannot revive a historical worker.

There is also a distinct survival bound even if every admission is rejected:
mandatory H1 slot clearing alone consumes 261 x 4 = 1,044 material. From 1,020,
at most 255 ticks can fund this retirement, before any other consumption.
Thus no-support cannot fund all 261 live ticks even after abandoning full query
service. Under an active-fraction definition counting fully funded live ticks,
the material-only upper bound is 255/261 = 0.97701149; energy and other costs
may tighten it. Do not confuse that upper bound with a predicted fraction or
automatically call it a failure of every possible active threshold.

The reviewed sources do not reproduce the original numerical active/completion
thresholds or their final-fault sampling convention. Carry those gates forward
unchanged and apply their exact definitions in B05/B06. Full-service infeasibility,
survival/completion, and missing-response penalties are separate checks. A
resource-feasible, subsidized configuration must still establish the original
H1 retention, adaptive-over-periodic, H2 allocation, and erasure-precision
conditions prospectively. None follows from the arithmetic here.

Disclose initial inventories, accepted/overflowed support, route/rent/upkeep
costs, physical losses, and boundary/activation interventions by phase and arm.
Use prospectively matched external opportunities, not winner-conditioned top-ups;
different consumption/cap overflow can legitimately produce different accepted
amounts. External power/material and ecological correctness returns are support
and teaching channels, not autonomous resource generation or a neuroscience
result. E3a remains conventional ECC plus ordinary allocation.

## Recommended next work

No additional source research is required to resolve these review findings.
The following work was not performed in this review:

* [ ] Round 1: reconcile mandatory RESPONSE/tails, zero-energy behavior, gate
  scratch ownership, terminal ordering, and acquisition prefix semantics.
* [ ] Round 2: supply the symbolic service ledger and scrub-generation counts;
  recheck all accepted/rejected/partial paths and the resulting lower bounds.
* [ ] Round 3: independently verify the revised full documents and disposition
  of OP-001 through OP-009. If blockers remain, retain an explicit blocked or
  conditional status rather than claiming B02 complete.
* [ ] B03: select physical routes, source assignments, rent/upkeep, hazards,
  capacities, and target-independent support satisfying prefix inequalities.
* [ ] B04-B06: bound signed reward prefixes, fix objective/policies/schedules,
  specify active/completion sampling, and assess original functional headroom
  and precision without adaptive gate changes.
* [ ] Later authorized implementation/B07: check bounded opcode/register traces,
  conservation, reset/noninterference, planned-row accounting, and no-replay
  behavior. No such tests have been claimed here.

## Clarifying questions

None needed to complete the bounded review.

## Independent revised-contract re-review on 2026-09-10

The original review above is retained unchanged. The closure assessment below
uses the revised operation contract, not the earlier 495-line version. Its
scope is symbolic B02 prices, paths, conservation constraints and slot accounting.
It does not establish implementation liveness, resource feasibility or performance.

### Re-review evidence and questions

Read the following documents in full, including frontmatter and final sections:

* E3_OPERATION_CONTRACT_v0_3.md, lines 1-941, abbreviated O2 below
* E3_STATE_CONTRACT_v0_2.md, lines 1-439, abbreviated S below
* .copilot-tracking/reviews/2026-09-10/e3-b02-review.md, original lines 1-411

SHA-256 identities at re-review entry:

* O2: F9AEB8595CC3AB0DFA47EA3F2C3F978F91C81EEB1F51F62AAE62E83B5856B019
* S: 0040C21E3B3A46E02000F0F9A201264A621A641686CA3658A6ED7FED3AE2E1BD
* Original review: CAB390131F44468FBE56A96028D879C2F1088282E9247BEEE6E889265A977D82

The independent checks cover OP-001 through OP-009, service arithmetic and
envelope ownership, paid discretionary gates, one-energy residue, unknown-address
bounds, mandatory learning RESPONSE paths, scalar occurrence limits, live reward
and prefix scratch, Q updates, frozen-entry retirement, examined-symbol generation,
acquisition, no-op charges, and accepted-supply prefix constraints. Numerical
B03-B07 choices are distinguished from contradictions in the selected B02 rules.
No simulator, training, experiment or repository program was run. Only this
existing review receives appended text.

### Bounded closure verdict

Re-review complete. OP-001 through OP-009 are resolved at the symbolic B02
specification level in the reviewed O2 version. No additional symbolic B02
contradiction was identified, so no OP-010 finding is assigned. This supersedes
the opening revision-required status only for this revised contract; the
original findings and their evidence remain historical review records.

Accept the revised symbolic service decomposition as a specification candidate,
not a runnable design freeze. The fixed tariffs and slot sums are coherent.
An implementation fitting CONTROL256, each scratch partition and all register
lifetimes has not been supplied or proved. Neither this verdict nor the resource
inequalities establish service feasibility, retention, adaptive benefit or any
other performance result.

### Disposition of original findings

* OP-001 resolved: O2 191-249, 354-394 and 628-658 make RESPONSE a mandatory
  base with an optional decode. Learning reserves the valid-record worst case
  before controller/action work. Invalid slots and rejected decoding still pay
  the valid-lane read and, if valid, exactly one reward read/add/clamp/rewrite,
  followed by slot retirement. Valid learning costs 636 energy/12 material;
  invalid-record learning costs 559/4, not the nonlearning 556/4. No external
  controller-success latch selects the reservation.
* OP-002 resolved: O2 183-254, 256-289 and 400-428 require the gate fee,
  mandatory local remainder, public future tail and one-energy residue.
  Material may meet equality; live energy must retain one. Gates precede
  optional body tests, actual debits precede outputs/action deposits, and
  minimum failure sinks remaining E without unpaid clearing or later ordinary
  reactivation. The preflight passive grant is an explicit external-support
  exception, not action income or continuation from E=0.
* OP-003 resolved as a slot witness: O2 191-239, 577-625 and 755-820 retain
  old reward through TD admission and current observation/action/return through
  action and write gates. Acquired loop/address state is scratch, not host
  history. Local and future obligations are recomputed without escrow. The
  92-bit action peak fits the 96-bit decoder partition; this does not prove an
  executable CONTROL/register trace.
* OP-004 resolved: O2 87-132 and 291-526 specify envelope multiplicities,
  mandatory and rejection paths, nested fees, explicit kernels, scalar widths,
  routes and accepted-material transport. TICK and each outer service have
  their own single exit clear; nested gates and the final boundary add none.
  Forage/collection have a 16-energy attempt body plus bounded I/O/transport.
  METADATA is a bounded, priced configuration template rather than an unnamed
  helper. Later numerical configuration is not an omitted B02 tariff.
* OP-005 resolved: O2 156-159 and 491-525 charge regeneration/extraction for
  every examined cell, including clean cells, plus each attempted write gate
  and completed write. The first rejected paid gate is included. Empty/tied
  scrub pays ACTION's gate but has no generation/write body; an intact unique
  decode has no free early exit. No winning 20-bit codeword is retained.
* OP-006 resolved: O2 527-575, 679-683 and 738-748 place terminal work before
  the final fault and define active/completion sampling after that fault.
  Completed responses/terminal updates are not rolled back by later death.
  Rejected optional terminal TD still retires the record; minimum failure
  performs no flush. Later corrupted bytes do not authorize posthumous work.
* OP-007 resolved: O2 354-440, 515-525, 570-575 and 701-748 give acquisition
  its own schedule, with no CONTROLLER, RESPONSE or ADMIT. Repetition is a
  costed prefix, block staging is a whole paid transfer, and the fourth lesson's
  rejection does not cancel scheduled COMMIT. COMMIT reserves and performs its
  one full staging retirement on every funded path, including invalid staging
  and rejected encoding.
* OP-008 resolved: O2 822-908 retains both-code full-service lower bounds,
  separates coverage from survival/completion, and adds accepted-supply
  source-specific prefix constraints. No-replenishment full H1 coverage fails
  for both codes; mandatory retirement also prevents all 261 live H1 ticks
  from one material inventory. Subsidies do not establish functional gates or
  permit changing thresholds after outcomes.
* OP-009 resolved: O2 755-762 now says forty observed-code bits, or twenty
  two-bit symbols. The original decoder subtotal is 64 bits, not forty symbols.

### Conservation, quote ownership and unknown admission

O2 104-130 and 183-254 define a nonrecursive priced gate. The scheduled METER
fee pays that gate's shape selection and sequential reservoir comparisons;
those comparisons do not introduce another METER call. An optional body is
tested only after its scheduled fee is paid. Minimum-path preflight is not a
free optional-body probe: inability to fund the fee, obligatory work and residue
causes the specified physical shutdown. Lost E is not reclassified as operation
expenditure, and unfunded agent work does not execute.

The local remainder excludes the debit currently being tested; the future tail
excludes the current service. Thus a gate preserves c + L + T + rho without
counting the current exit in both L and T. A newly admitted core adds its
specified remaining work to L. Executed work or a paid terminating/skipping
branch can reduce L; expected income cannot. Unused bounds were never debited,
so their release is not a refund. T remains public worst-case until its service
starts, even after a controller has cleared a record. These rules avoid both
double reservation of an exit and a hidden spent-credit/success account.

O2 39-46, 185-218, 313-322, 431-440 and 444-479 require pre-read maxima over
all possible acquired address encodings, separately for each material source.
This applies to the unreceived maintenance/admission/lesson cue, unknown
observation-dependent Q routes, response address and corruptible metadata
cursor. Later narrowing uses only paid scratch observations. Componentwise
maxima may conservatively combine bounds from different possible addresses;
they are not a claim that all maxima occur on one execution. Unknown address,
dirty count, Q value or scorer knowledge cannot select an unpaid cheaper quote.

Accepted material transport is reserved before an action yield, then charged
for accepted units. Energy yield has scalar transport but no per-unit energy
transport tariff. Caps apply to actual deposits. The TICK grant occurs before
its preflight by explicit exception and incurs its declared five scalar charges
and accepted-material transport on a funded service; a failed preflight yields
external support followed by shutdown loss, not free agent service. No grant
revives E=0 except a separately named canonical activation.

### Independent tariff and no-op audit

All numbers below exclude routes and scalar I/O unless explicitly stated.
Arithmetic was checked independently using constant-expression calculations,
not repository code or a simulator.

* F = 128 + 256 + 8 = 392. TICK = 152, plus five scalar encoding ALUs, their
  routes, accepted-material transport and declared rent/dues. Its S is its own
  exit, not another tick-end clear.
* CONTROLLER bases are 616/16 for learning and 520/0 for frozen operation.
  These include DECIDE's fee even when DECIDE rejects. An admitted learning
  core adds K + J + 416 and sixteen new-store material; frozen adds K + J + 144.
  The learning base already includes sixteen old-clear material. The core's
  TD and ACTION fees are included once each; no TD fee/record access occurs
  in a frozen controller. Old TD rejection skips its kernel, not its gate.
* Nonlearning RESPONSE is 556/4. Learning valid-record finalization adds
  3 + 72 + 1 + 4 = 80 energy/eight material, giving 636/12. An invalid record
  skips only the 77-energy/eight-material reward body, leaving 559/4.
  Invalid slot, rejected decode and no response contribution are not grounds
  for skipping mandatory valid-record finalization. A missing contribution
  uses b=0; it does not introduce another message or reward write.
* ADMIT and LESSON outer rejection cost 136 with no body access or lesson/cue
  delivery. Successful ADMIT is 416/4; block LESSON is 428/4. Same-value writes
  and erasures are still physical writes, not discounted no-ops.
* COMMIT base is 556/4, including its encoding fee on invalid/rejected paths.
  A full twenty-symbol prefix adds 120 + 2,560 + 120 = 2,800 energy and twenty
  material, for 3,356/24 including staging retirement. No second encoding gate
  or staging clear is added. A full repetition LESSON is
  392 + 5 + 640 + 30 = 1,067 energy/five material, plus lesson I/O and routes.
* TERMINAL base is 664/16, including full record reads/clear and one TD fee
  even when invalid, action=3 or rejected. Its admitted 97-energy/eight-material
  kernel gives 761/24, not another fee. The scheduled terminal uses m=0;
  ordinary old-record TD obeys the stored terminal bit and therefore uses
  97 or 175 as appropriate.
* Q read/rewrite remain 25/48. Nonterminal TD is
  25 + 75 + 4 + 23 + 48 = 175, with 32 Q-lane reads and eight writes.
  Terminal TD is 25 + 1 + 23 + 48 = 97, with eight Q-lane reads and eight writes.
  Record access/retirement is separate. Numerator extrema remain -1,019,888
  and 1,019,889. Selection rereads the current row after TD; its 99 includes
  three Q reads and 24 selection ALU slots, not an extra TD maximum.
* ISOLATE is 704/52: 392 + 6(20 + 16 + 16). Failure is a boundary prerequisite
  failure/shutdown, not ordinary reject-and-continue. METADATA is one F plus
  its declared bounded accesses, non-C arithmetic, I/O and physical dues.
* Scrub body is gV + 128A + 6W plus write/material routes, with
  W <= A <= V <= n. Loop admission reserves generation and possible gate fees;
  it does not debit every reserved fee. Clean examined cells pay g, a failed
  needed-write gate pays 128 but no write material, and the first such failure
  stops the loop. Empty/tied scrub still pays ACTION's scheduled 128.

READ2/WRITE2 bundled lookup/insertion/extraction work, scan captures, Q accesses,
TD arithmetic and selection slots are not added a second time to N_L or CONTROL.
The sensor kernel's sixteen energy includes its two encoding ALUs; only sensor
flit routes are added, not two additional I_G encoding ALUs. Explicit METER
ownership governs reservoir comparisons; CONTROL governs the separate bounded
decoding, packing, status and cell/loop predicates. The scrub paragraph's general
comparison wording introduces no second gate or envelope. Exact opcode allocation
and simultaneous register use still require the later static trace, rather than
being certified by these fixed-charge identities.

### Scalar completeness and live-state cross-check

O2 303-352 bounds every atomic service, including nested action traffic:

* TICK has five grant scalars: one 16-bit E and four eight-bit P quantities,
  including explicit zeros.
* CONTROLLER plus ACTION has at most eight: offer 5, sensors 16 and 8,
  random indices 1/2/4, request 6, and one yield 16 or 8. The widths are bits;
  the count is 1 + 2 + 3 + 1 + 1 = 8. Fixed policies omit unused randoms;
  scrub has no request/yield. No extra action-return scalar exists.
* RESPONSE has at most four: optional one-bit guess, one-bit output, 16-bit
  ecological E yield and 16-bit signed learner contribution. Frozen ecology
  omits the learner contribution; isolation/H1 omit both feedback packets;
  spurious unplanned output receives neither. There is no correctness packet.
* ADMIT has one scalar, LESSON two, COMMIT/TD/TERMINAL and ISOLATE none.
  Each METADATA instance must declare zero to eight bounded scalars before
  acquisition. Lane protocols are separately charged R/W traffic, not missing
  scalar occurrences. Any redelivery counts again and cannot exceed the cap.

The reviewed scratch sums are scan 69, full old-record load 85, old TD gate
78, selected-action/write peak 92, RESPONSE scan 74 and finalization 47 bits in
the 96-bit decoder partition. At old TD admission the sixteen reward bits are
still present; only afterward can they move into an arithmetic register. The
92-bit peak includes three five-bit V/A/W counters instead of the single loop
counter, the offered cue and expected symbol, in addition to observation,
action, signed return, raw snapshot, best payload and predicates. It leaves four
decoder bits unused, not another resource or reward ledger. Four arithmetic
registers and the 32-bit control partition remain separately allocated.

The complete storage budget remains 160 + 2,048 + 256 = 2,464 bits, with
276 persistent bytes. O2's frozen-entry rule agrees with S 179-189 and 291-299:
funded ISOLATE clears ring, staging and the old transition before nonlearning
entry. Frozen controllers and RESPONSE neither consume nor modify subsequent
fault-created transition validity. Terminal clearing before a later fault does
not replace this entry boundary or resurrect learning.

Exact a storage followed by one RESPONSE finalization preserves a=300, b=-300
as zero, rather than -44. Signed-16 bounds for every permitted a and a+b, the
bounded B04 return function and its CONTROL/slot fit remain explicit acceptance
conditions, not assumed numerical values. No live tick-total expense accumulator
or post-RESPONSE reward source was introduced.

### Accepted supply and remaining prerequisites

The revised conservative H1 totals check: 2,068 lane writes, 234,924 repetition
energy and 1,184,684 block energy before the explicitly omitted newer charges.
Beyond full initial stocks these imply at least 1,048 accepted material and
169,389 or 1,119,149 accepted energy, respectively, before additional costs and
residue. Mandatory retirement alone is 1,044 material; 1,020 funds at most
255 such ticks, giving the material-only upper bound 255/261 = 0.97701149.
Full acquisition is 1,280 code-write material for either representation and
2,560 total write material for block after staging/retirement. The associated
full-write deficits are 260 and 1,540. These are necessary bounds, not observed
rates or assertions that partial acquisition must finish all writes.

O2 873-903 correctly uses accepted, not offered, supplies at every execution
prefix and for each source. Overflow cannot pay a bill; late supply cannot cure
an earlier failed prefix. Total or average accepted rates alone do not prove
feasibility, and four-pool totals cannot replace source-specific gates. The
current c + L + T + rho requirement is stronger than cumulative conservation.
Physical losses remain distinct from expenditure and local remainder L.
Matched offered opportunities may produce unequal accepted amounts through
different consumption/cap overflow, without authorizing winner-conditioned
top-ups. No numerical accepted-rate sufficiency is claimed here.

No further research is needed to close the nine original symbolic findings.
Recommended next work, not completed in this re-review:

* [ ] B03: instantiate route/source maxima, domain/rent/upkeep/hazard rules,
  caps, accepted-yield bounds, support and bounded METADATA instances.
* [ ] B04: specify bounded reward-prefix functions, thresholds, fixed policies
  and grids within the declared scalar, CONTROL and scratch limits.
* [ ] B05: enumerate phase/arm/channel schedules and carry forward numerical
  active/completion and functional gates without outcome-dependent changes.
* [ ] B06: establish source-specific prefix feasibility and accepted-supply
  requirements, then assess H1/adaptive/H2 headroom and erasure precision.
* [ ] B07 and later authorized implementation: verify reset/interface
  noninterference and static CONTROL/register/slot traces, conservation,
  planned-row accounting, shutdown and no-replay behavior.

These are named remaining design or implementation prerequisites, not newly
discovered B02 contradictions. No clarifying question is required for this
bounded verdict.