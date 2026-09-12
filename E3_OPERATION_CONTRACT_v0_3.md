---
title: E3a costed operations and event schedule
description: Selected B02 service tariffs, bounded transactions, event lifetimes, and affordability constraints
ms.date: 2026-09-10
---

## Decision and scope

Select the transaction and tariff rules below as the next design candidate.
They supplement [E3_STATE_CONTRACT_v0_2.md](E3_STATE_CONTRACT_v0_2.md), which
remains unchanged. No simulation, experiment, design freeze, final target draw
or empirical E3 result is supplied by this contract.

All execution state is managed through the .copilot-tracking folder files;
the [B02 plan](.copilot-tracking/plans/2026-09-10/e3-b02-plan.md) is current.
The [independent operation research](.copilot-tracking/research/subagents/2026-09-10/e3-b02-operation-research.md)
is supporting analysis, not a second competing normative schedule.

This version chooses a priced abstract machine, not measured processor energy.
Reads, physical writes, transport, declared arithmetic kernels, and fixed padded
control services are charged. Fixed control prices replace the earlier suggestion
of deriving every simulator branch from hardware-level costs. A faster host
implementation cannot silently lower the simulated price. Report padding and
actual primitive use separately. B03 must instantiate routes, rent, hazards and
supplies; B04 supplies objective/threshold/policy constants; B05 supplies schedules.
The OP-001 through OP-009 revisions below close the symbolic B02 service
decomposition as a specification candidate. B03-B07 decisions and later bounded
implementation traces remain conditions of a runnable freeze, not omitted B02
tariffs. No hardware-derived price or implemented microtrace is claimed.

## State and input constraints

Keep exactly 160 code bits, 2,048 auxiliary bits and 256 scratch bits. There is
one persistent transition, five persistent addresses, four teaching blocks,
and no hidden event queue, alive bit, balance mirror, reward total, escrow,
visited-cell map or per-word upkeep history. Use the existing 276-byte boundary
snapshot. Every operation clears scratch before returning; a fused operation
may contain internal substeps without clearing, but cannot suspend across ticks.

Inherited configuration G supplies fixed lane locations, routes, maximum route
length D, material-source assignments, domain membership, capacities and public
phase rules. Emax is at most 65,535; each of four Pmax values at most 255.
Reject a configuration before acquisition if any route/cost bound is invalid
or exceeds signed 32-bit arithmetic. Route/shape tables are target-independent
ROM, not a history-dependent pricing cache. Unknown addresses use maxima over
all possible encodings until the address is acquired by a paid read.

Only current input packets are exposed. Responses use the stored due address;
neither a scheduled due-cue field nor a historical/future schedule lookup is
available. Current exogenous offer/random flits may be reread inside a tick
only within the service's declared packet budget and for another charge. They
cannot retain chosen actions, decoded answers or computed feedback between
operations. Action yields and the synchronous ecological return are consumed
once by their owning operation, never reread through a reusable callback.

## Primitive and service prices

Divide the 2,208 persistent bits into 1,104 aligned two-bit lanes. Eleven bits
address a lane; six two-bit flits suffice for its address. Invalid lane addresses
are prohibited by the executor, not redirected to a clean backup.

* READ2 costs one energy, plus one ROM-route lookup and one scratch insertion:
  three energy before transport. A width-w field touches every intersecting lane.
* WRITE2 costs four energy and one material unit, plus one route lookup and
  one two-bit extraction: six energy before transport. Same-value and erasure
  writes cost the same. Material is consumed, not recovered by clearing.
* A masked single-bit change reads its lane, performs one Boolean merge, then
  writes it. No uncharged preservation of the neighboring bit is available.
* Each at-most-32-bit ALU/register instruction costs one energy. Shifts, AND,
  XOR, equality/comparison, addition/subtraction, select and extraction are
  separate instructions. No variable-length popcount, decoder or table search
  is a single ALU instruction. Scratch register access belongs to the instruction.
* A two-bit flit costs one energy per link. Symmetric read routing costs 7d
  (six request flits plus reply); write routing costs 8d (address, value, ack).
  Transporting one material unit a distance m costs m additional energy.
* Physical E/P are typed reservoir quantities, not ordinary RAM write targets.
  Their exact debit/deposit/cap changes use METER, not recursive WRITE2 calls.
  A resource observation costs sixteen energy for a current E/local-P pair,
  including encoding, plus the two sensors' routed flits under G.
* Clearing eight 32-bit scratch words costs eight energy and no material.
  This is a stated volatile-register exception, not free clearing of persistent
  teaching, query, Q or transition fields.
* Living costs sixteen energy per live tick. B03 allocated-domain rent and
  upkeep dues are additional, not implicit in any kernel price below.

For a trace with lane distances d and material routes m:

$$
C_E=3N_R+6N_W+N_L+7\sum_R d+8\sum_W d+\sum_W m
+C_{\rm services}+16I_{\rm living}+C_{\rm rent},
\qquad C_{P,j}=N_{W,j}+C_{{\rm upkeep},j}.
$$

N_L excludes route/insertion/extraction instructions already bundled into
READ2/WRITE2. Kernel totals explicitly include their bundled lane accesses;
never charge the same access again when assembling the transaction. The service
term includes separately enumerated scalar I/O, accepted-material deposit
transport and fixed envelopes; do not lose those non-lane costs. For each source
j, N_W,j counts writes assigned to j, not an interchangeable sum of all pools.
Upkeep adds only physical consumption not already counted among lane writes.

### Fixed control services

METER costs 128 energy per operation admission or discretionary subgate.
It covers shape-quote selection, sequential resource comparisons, cap/overflow
arithmetic, physical debit/deposit and one-way audit emission. Reservoir transport
is priced separately by G. It owns no persistent escrow or history. Its internal
physical updates do not recursively invoke METER. This fixed simulator charge
is a modeling choice, not a measured instruction count or ATP claim.

A body-admitted ordinary operation pays another 256 energy for a CONTROL
envelope and eight for final scratch clearing. Mandatory-base services below
pay CONTROL even when their optional body rejects. CONTROL covers input decoding,
field extraction, legal-address checks, status decisions, fixed loop control,
public substep management, and internal field packing not enumerated in a kernel.
It does not include persistent reads/writes, routed I/O, scans, Q arithmetic,
code generation, explicit scalar I/O encoding, or resource sensing. Ordinary
ADMIT/LESSON rejection pays METER plus eight for clearing scratch, with no body
read or CONTROL. CONTROLLER, RESPONSE, COMMIT and TERMINAL instead have the
mandatory bases explicitly priced below; they are not ordinary rejection paths.

Each CONTROL envelope permits at most 256 bounded ALU instructions, charged
as 256 even when fewer are used. Unused slots are padding, not usable work
later. An implementation must produce a static instruction/liveness trace
within this cap for each service. Exceeding the cap is an implementation-contract
failure: stop and version the design, not truncate an agent's calculation or
raise the cap after final outcomes. Such traces have not yet been implemented.

This finite cap closes the price definition, not a proof that every eventual
implementation fits. The cap and tariff are common to competing codes/controllers.
Separate protected simulator physics/evaluator work from agent work: physics
does not supply free health bins, decoded bits, past cues or cost histories.

### Priced computational kernels

The repetition scan reads five symbols and always runs the same vote/health
logic. Two counter initializations, five per-symbol steps, twelve final steps,
five route lookups and five physical reads total 49 energy before transport.
The five per-symbol steps include scratch insertion, two equalities and two
adds; thus do not add another READ2 insertion to this total. Empty overrides
tie, then intact/degraded unique decoding. All five symbols are read.

The block scan reads twenty symbols and compares all sixteen generic codewords.
Generator columns, in this logical order, are 1 through 15 followed by 1,2,4,8,15.
Each output bit is the parity of a four-bit candidate AND its fixed column.
Sixty-four initialization/capture steps, 228 steps per candidate, seven final
health steps, twenty route lookups and twenty reads give 3,759 energy before
transport. The 228 steps comprise two initializations, twenty eleven-step cell
comparisons, and six minimum/tie updates. Six of the eleven cell steps implement
AND plus shift/XOR parity; the rest extract a symbol, test observation/mismatch,
mask and accumulate. Strictly smaller distance clears the tie flag; equal
distance sets it. Empty or multiple minimizers forbid live corrective writes.

This is the cost of a specific deliberately simple kernel, not a lower bound
on all possible ECC. A more efficient decoder is a future priced baseline,
not a free optimization. Regeneration costs six ALU steps per examined block
symbol, including clean symbols that need no write; repetition extraction costs
one per examined symbol. Candidate addressing/loop administration is covered
by CONTROL, not parity arithmetic.

An aligned signed Q read costs 25 energy: eight READ2 accesses and one signed
extraction. A Q rewrite costs 48 energy plus eight material. A maximum of three
Q values uses two compare/select pairs, four additional ALU steps. Reread the
selection row after updating Q; the old row can be stale.

TD arithmetic costs 23 ALU steps: four reward clamps, six numerator steps,
two quotient/remainder steps, five ties-to-even predicate steps, two adds,
four saturation steps. Nonterminal TD costs 175 energy before transport:
old Q read 25, successor reads 75, max 4, arithmetic 23, Q rewrite 48.
Terminal TD costs 97: old Q read 25, zero-bootstrap assignment 1, arithmetic
23, rewrite 48. Record access/retirement, meters and CONTROL are additional.

Three-action epsilon-greedy selection costs 24 ALU slots plus three Q reads
(75 energy), and routed indexed random inputs. The slots cover epsilon test,
two compare/select maxima, tie-mask construction, ranked selection and result
assignment; unused slots are charged padding. Supply fixed independent random
indices uniform in {0,1}, {0,1,2} and {0,...,15}; select by actual tie count
without an unbounded rejection sampler. Receiving each index is charged I/O.
Fixed/periodic policies do not pay for Q reads they do not perform, but their
rule consumes CONTROL slots and any needed metadata reads. Threshold policies
must pay their memory-health scan. Precise rules and grids remain B04.

## Transaction admission and mandatory tails

An operation quote is determined by G, public substep, representation, packet
shape and fixed maximum body length, not dirty-cell count, validity or Q value.
Compare energy and each of four material quantities separately. Reserving enough
total material but not enough at the assigned source is a failed reservation.

The public future tail T sums the mandatory paths of all later scheduled services
through this tick, including their gate fees, CONTROL where specified, scratch
clears, accesses, worst allowed routes, finalization and source-specific material.
It is a pure function of public substep and phase, not a counter or escrow field.
The executor recomputes it from ROM. L is the current operation's still-mandatory
local remainder, determined by its bounded scratch micro-PC/loop position and
already-paid observations. T excludes the current service; L excludes a debit
already being tested. Never count an exit twice or omit it from both.
Reject G if any symbolic worst-case quote overflows or exceeds a declared cap;
resource shortage within valid G is a normal physical failure, not data deletion.

Preflight may inspect physical reservoirs through METER, but no acquired RAM.
Every live minimum check requires its gate fee, minimum local rejection or
retirement path, T, and a one-energy survival residue. Material may meet equality;
energy must cover costs plus one. Pay the gate fee before testing the optional
body against L + T + that residue. A failed minimum check is physical shutdown,
not a free preliminary body test. A rejected optional body makes no optional
accesses but still completes all mandatory-base work in the ledger below.

For every optional debit vector c, require componentwise R >= c + L + T + rho,
where rho has energy component one and four zero material components. This
invariant also holds while paying fixed envelopes and all subsequent accesses.
Quotes include all transport and exits; before paid address discovery use maxima
over every possible encoding, separately for each material source. Do not read
an acquired value merely to select a cheaper quote without paying that read.
Later gates may narrow bounds using the already-paid scratch snapshot only.

Debit costs before deposits and before outputs. No output, deposit or prepaid
cleanup may execute at E=0. Cap each actual deposit when it occurs. Reserve
maximum permitted yield-transport cost before any action or response yield;
yield cannot finance its own admission. Pay actual executed accesses/kernels
and the specified fixed envelopes/attempted gates. Unspent bounds remain in
physical reservoirs: they are not debits, refunds, loans or escrow objects.

Within an admitted fused controller or teaching commit, discretionary subgates
pay METER but do not clear operation scratch. Their bounds reserve local record
store/retirement, atomic exit and the rest of the tick. Conditional body selection
may use already-paid scratch observations. Stop on the first failed needed write;
there is no search for a cheaper cell or retry loop. Required tail services have
priority over optional repair, Q updates, collection or foraging.

Admitting an optional body promotes its quoted fixed-core obligations into L
only after the paid gate covers them along with the existing obligations.
Within that admitted body, obligations decrease only when the specified work
executes or a paid branch terminates/skips it. Recompute from ROM and scratch;
never track spent totals, unused credit or a successful-reservation flag. Gains
cannot enlarge an admitted loop, restart a failed gate, retroactively fund work,
or reduce L or T. They may fund later publicly scheduled gates under the same
monotonic remainder rule. T remains public worst-case until its service starts,
even if a prior controller appeared to leave an invalid record.

At tick entry reserve CONTROLLER's base when offered, the complete RESPONSE
worst-case base on query-phase ticks, ADMIT rejection when scheduled, fourth-block
COMMIT's base on acquisition ticks, TERMINAL when scheduled, and B03 metadata,
upkeep and rent dues. Learning RESPONSE includes its possible valid-record
read-add-clamp-write, even if the controller will reject. LESSON rejection is
also in the acquisition tail. Full decode, new admission, new transition storage,
TD and code writes are optional. An action may leave optional decoding
unaffordable, not consume reserved response finalization. Missing responses
remain failures; funded retirement does not imply functional sufficiency.

No faults occur between quote and operation cleanup. B03 faults occur after
tick operations, so they cannot remove reserved resources midway through a
transaction. A different fault window requires a different contract. This is
protected atomic execution, not a claim that the executor repairs itself.

### Retirement paths and status

An eight-bit query slot or teaching block clear costs four WRITE2 operations
(24 energy, four material, plus routes). A 32-bit transition clear/store costs
sixteen WRITE2 (96 energy, sixteen material, plus routes). An aligned 16-bit
reward update costs eight READ2 plus eight WRITE2 (72 energy, eight material,
plus routes). Its separate valid-lane read costs three and its single addition
and four clamps cost five ALUs. Field extraction is CONTROL work. Clear all
bits, including unused payload/reserved bits.

No routine clear is free. If minimum retirement cannot be funded with the
one-energy residue, enter physical shutdown with unchanged uncleared bytes;
do not claim that retirement ran. Resource loss is recorded separately from
operation expenditure.
No future ordinary refill may reactivate those stale records in the same phase.

E=0 is physically absorbing within a phase. If the minimum tail cannot be funded,
the environmental shutdown transition sinks remaining E and stops live execution.
P and memory need not disappear. This declared physical sink is not a paid agent
write or additional alive bit. The scorer emits every remaining planned failure.
Ordinary passive support is ignored after shutdown. A named experimental
activation may power a new canonical reset state, not revive arbitrary old
pending responses or grant posthumous learning.

The existing corruptible dead/failed flags are diagnostic only. They do not
control survival, row retention, clean restoration or branch eligibility.
Status writes occur only in an explicitly scheduled, priced METADATA service,
not in ad hoc failure handlers. A single masked flag change costs READ2 + one
merge ALU + WRITE2 = ten energy/one material plus routes, within that service.
After shutdown no flag update runs. Scheduled status rules may inspect paid
current fields/public events only, not an unrecorded previous operation result.
Cursor/periodic fields are read before use; invalid values take the scheduled
bounded failure branch, not an out-of-range access or clean restoration.
One-way audit labels are not a hidden second worker copy of those fields.

## Symbolic service ledger

Use M=128, C=256, S=8 and F=M+C+S=392. For an actual bounded lane-access
multiset X, write R(X)=3|X|+7 sum(d_X) and
W(X)=6|X|+8 sum(d_X)+sum(m_X). W consumes one material at the assigned
source per lane. In the rows below, numerical subtotals omit routes; add those
R/W route terms exactly once. For code scan K, use 49 or 3,759 plus its five
or twenty read routes. Selection is 99 plus its 24 Q-lane read routes.
Nonterminal TD is 175 plus 32 read and eight write routes; terminal TD is 97
plus eight read and eight write routes. Those totals already include accesses
and ALUs from the kernel definitions. All material quotes are four-vectors.

For scalar x of declared width w and route d, I_G(x)=1+ceil(w/2)d: one
encoding/receiving ALU and the two-bit flits, with no extra implicit handshake.
Every scalar is at most 32 bits and every atomic operation has at most eight
scalar occurrences on any path. Repeated delivery is another occurrence and
another charge; lane protocols are already in R/W, not scalar packets. Inputs
must fit their declared width/range; G rejects incompatible packet definitions
before acquisition. CONTROL handles bounded validity tests, not unpaid I/O.
The 16-energy sensor kernel already includes its two encoding ALUs; add only
their flit routes, not I_G's two ALUs a second time.

G specifies directional scalar routes and finite accepted-yield bounds. Let
H_G(y)=sum_j(y_j m_j) be transport of accepted material deposits to their
assigned pools. Reservoir command/cap/deposit arithmetic is in the already
named METER, not a callback with its own unlisted cost. Energy deposits have
no per-unit transport tariff in this abstract machine: their scalar packet
transport and METER are charged. Only material units incur the extra hop term.
Quotes reserve maximum H_G over allowed yields before any gain. No paid
memory peek chooses this bound. The passive public grant is the sole support
exception allowed before TICK preflight; it is external support, not action
income, and still incurs the TICK I/O/transport charges below.

### Scalar packet inventory

| Service               | Maximum scalar occurrences and widths                                                 |
|-----------------------|---------------------------------------------------------------------------------------|
| TICK                  | Five inbound grant quantities: E:16 and four P:8; explicit zeros are charged          |
| CONTROLLER/DECIDE     | Offer cue/usefulness packed:5; sensors E:16, local-P:8; independent randoms:1,2,4     |
| ACTION inside core    | Forage/collect request action/cue:6 outbound; yield E:16 or local-P:8 inbound         |
| RESPONSE/DECODE       | Guess:1 inbound if needed; bit:1 outbound; ecology yield:16 and learner return:16     |
| ADMIT                 | Current cue:4 inbound on successful body admission                                    |
| LESSON                | Current cue:4 and label:1 inbound on successful body admission                        |
| COMMIT/TD/TERMINAL    | None; use only paid persistent reads and current scratch                              |
| ISOLATE               | None; public fixed clearing plan                                                      |
| METADATA              | G declares a list of at most eight scalars, each width 1-32, or an empty list         |

CONTROLLER and its nested ACTION share a maximum of eight scalars: one offer,
two sensors, three randoms, one request, one yield. Fixed policies omit unused
randoms. Scrub has no resource request/yield packet. No separate action-return
packet exists: B04's bounded integer function of the paid attempt/prefix and
accepted yield uses CONTROL slots and the declared 16-bit return scratch.
Sensor routing is included as described above. Other listed scalar encoding
ALUs are additional to C. There is no reusable host callback or implicit
additional sensor, success bit, cost history, or reward-total message.

RESPONSE's ecological physical yield is a nonnegative E quantity of at most
16 bits. Its signed learner contribution uses 16 bits and is present only on
learning ecology paths. Frozen ecology may receive physical yield, but never
creates/updates a transition. Both feedback packets are absent in isolation/H1.
A spurious unplanned output receives no feedback packets or gain. Guess input
is present only for readout-only empty/tied decoding, never live correction.

### Outer services and mandatory paths

| Service/path                | M,C,S counts | Lane/explicit arithmetic or nested fees               | Energy before routes/I/O      | Write material |
|-----------------------------|--------------|-------------------------------------------------------|-------------------------------|----------------|
| TICK funded                 | 1,0,1        | Living 16; G rent/dues outside this subtotal          | 152                           | 0              |
| CONTROLLER learning base    | 1,1,1        | Old clear 16W; DECIDE gate M even on rejection        | 616                           | 16             |
| CONTROLLER frozen base      | 1,1,1        | DECIDE gate M even on rejection; no record access     | 520                           | 0              |
| RESPONSE nonlearning base   | 1,1,1        | Slot 4R+4W; DECODE gate M even when invalid           | 556                           | 4              |
| RESPONSE learning worst     | 1,1,1        | Above + valid 1R + reward 8R+8W + add 1 + clamps 4    | 636                           | 12             |
| ADMIT rejection             | 1,0,1        | No body reads/writes or cue delivery                  | 136                           | 0              |
| ADMIT success               | 1,1,1        | Slot 4W; cue I/O                                      | 416                           | 4              |
| Block LESSON rejection      | 1,0,1        | No staging read/write or lesson delivery              | 136                           | 0              |
| Block LESSON success        | 1,1,1        | Staging 4R+4W; cue/label I/O                          | 428                           | 4              |
| Repetition LESSON rejection | 1,0,1        | No lesson delivery or cell work                       | 136                           | 0              |
| Repetition LESSON admitted  | 1,1,1        | Lesson I/O + V + 128A + 6W, n=5                       | 392 + V + 128A + 6W           | W              |
| COMMIT mandatory base       | 1,1,1        | Staging 4R+4W; encoding gate M even when invalid      | 556                           | 4              |
| COMMIT admitted prefix      | 0,0,0        | Additional generation 6V + per-write gates 128A + 6W  | 6V + 128A + 6W                | W              |
| TERMINAL mandatory base     | 1,1,1        | Record 16R+16W; TD gate M even invalid/rejected       | 664                           | 16             |
| TERMINAL admitted TD        | 0,0,0        | Additional terminal kernel                            | 97                            | 8              |
| ISOLATE funded              | 1,1,1        | Ring 20W + staging 16W + transition 16W               | 704                           | 52             |
| METADATA scheduled          | 1,1,1        | G-bounded R/W plan, explicit ALUs, I/O, physical dues | 392 + 3N_R + 6N_W + N_L + U_E | N_W + U_P      |

TICK is 128+8+16=152. Add its five scalar encodings/routes,
accepted passive-material transport H_G, and declared rent. It has no
CONTROL or tick-exit S: TICK clears its own scratch after grant accounting and
living/rent. Every subsequent outer service clears once on its own exit.
Nested gates have no C or S. The final boundary checks already-zero scratch;
it is not another charged clear. No active tick can skip the TICK charge.

CONTROLLER's ungated learning subtotal is F+96=488; its DECIDE fee makes 616.
Nonlearning is F+128=520. The learning minimum always reserves old-record
clear even if DECIDE fails; no old-record read is required on that failure.
RESPONSE's ungated subtotal is F+12+24=428; its every-tick DECODE fee makes
556. Learning adds 3+72+1+4=80. After its paid valid read, an invalid record
skips exactly 77 energy and eight material (and their routes), so that path
costs 559 plus routes, not 556. Reserve 636/12 before discovery. A rejected
decode still reads/clears the slot and finalizes any valid learning record.

COMMIT's encoding gate is included once in 556; its twenty possible per-write
gates are additional. Invalid staging or rejected encoding performs no generation
or code writes but still pays the encoding fee, staging reads and one clear.
TERMINAL's optional 97 does not add a second TD fee. Its full update is 761
energy/24 material before routes. ISOLATE has no ordinary reject-and-continue
path: inability to fund its complete clear plus residue fails the boundary.

The local execution order removes any ambiguity about prepaid envelopes:

* TICK: public passive deposit, minimum check, M, five scalar I/O charges and
   accepted-material transport, living/rent, S. A grant followed by a failed
   minimum check is external support followed by shutdown loss, not free agent
   service. Its unpaid work does not execute or earn an active tick.
* CONTROLLER: M, C, DECIDE M, body test; if rejected, learning record clear
   then S. If admitted, follow the controller stages below, ending in S. The
   old clear is reserved, not performed before its admitted TD read/update.
* RESPONSE: M, C, four slot reads, the learning valid-lane read if enabled,
   DECODE M, optional decode/emit/feedback, valid-record finalization, four slot
   writes to clear, S. Rejecting decode does not skip the later mandatory work.
* COMMIT: M, C, four staging reads, encoding M, optional prefix body, four
   staging writes to clear, S. Stored validity is tested with CONTROL slots.
* TERMINAL: M, C, sixteen record reads, TD M, optional 97 kernel, sixteen
   record writes to clear, S. Only valid/action 0-2 permits TD; force m=0
   regardless of the stored terminal bit. Invalid/action=3 or rejection skips
   only the 97 kernel, not its fee/reads/clear.
* ADMIT and LESSON: M, body test, then C/I/O/body/S if admitted or only S if
   rejected. LESSON uses the representation-specific body above.
* ISOLATE: minimum check, M, C, ring clear, staging clear, record clear, S.
   METADATA: minimum check, M, C, declared bounded read/compute/write plan and
   physical dues, S; no extra failure-handler operation is implicit.

Every step still obeys the positive-energy and source-specific remainder
invariant. Reserve C/S in advance where required, but debit C when entered and
S only at exit. Unexecuted accesses/retirement remain reservations, not debits;
sensors observe charges actually paid in this order. All ordinary gate fees
are paid before their optional body comparison. An unfunded
minimum stops without executing any remaining agent work or unpaid clearing.

G/B03 must instantiate each scheduled METADATA service with a public bounded
access plan (each R/W list length at most 1,104), named scalar widths/routes,
explicit non-C kernels and U dues. Accesses chosen by corruptible cursor values
use pre-read source/route maxima. Invalid values take the declared bounded
no-body branch after the paid read and C; no implicit correction or retry.
Reserve the worst mandatory path in T. If minimum dues cannot be paid, shut
down; do not silently skip rent or forge status. N_L excludes C slots and
bundled R/W ALUs. U includes only additional physical dues not already charged
as lane writes. This is a priced service template, not permission for unspecified
helpers; a configuration with missing counts, widths or bounded branches fails
before acquisition. The CONTROL256 trace obligation applies to each instance.

### Controller, decode and action bodies

An admitted DECIDE adds K, the 16-energy sensor kernel, its scalar I/O routes,
the non-sensor scalar encoding ALUs, and selection J. J=99 plus Q-read routes
for RL; other policies use their CONTROL slots and separately declared R/W
metadata accesses. All policies
pay the selected common scan K; no health-free threshold policy is permitted.
DECIDE also reserves ACTION's M=128 on every admitted path, including abstention.
Learning DECIDE adds old-record 16R=48, current full store 16W=96, and the
TD gate M=128 whether the old record is invalid, action=3, or TD rejects.
These fees are not in the outer 616/520 minimum when DECIDE itself rejects.

Thus, excluding routes, scalar I/O and optional TD/action bodies:

$$
D_{\rm learn}=K+16+J+48+96+128+128=K+J+416,
\qquad D_{\rm frozen}=K+16+J+128=K+J+144.
$$

DECIDE reserves this whole core, new-store material, local cleanup and T before
scanning or receiving the offer. Old-record clearing is already in its outer
base; do not add it again. Additional paid metadata used by a selected policy
is a declared G/B04 term, never an implicit read. Optional TD may be admitted
only while preserving the remaining selection, ACTION gate, new store, exit
and T. Its 175 nonterminal or 97 terminal body consumes eight material plus
routes. Invalid/action=3 records and dropped updates have body zero but still
pay the 128 TD fee. Frozen controllers do not read, clear, store or consume a
record, do not pay a TD gate, and cannot act on later fault-created validity.
Their nonlearning entry uses the funded ISOLATE service before the first tick.

An admitted RESPONSE decode adds K for its stored address and scalar I/O,
including bounded guess/output/feedback. Its E yield has no material hop cost.
The base already paid its single DECODE gate. Slot invalidity or a rejected
quote adds zero
decode-body cost and emits no bit; it does not cancel the base. For unknown
addresses the pre-slot-read minimum uses G maxima. After that paid read the
decode gate can select the corresponding immutable route quote, never the
scorer's address. CONTROL packs the selected bit; I_G charges transmission.

ACTION's one scheduled gate costs 128 whether the action body admits or not.
After selection, pay that fee before testing the body. Forage and collection
each add attempt kernel 16, request/yield I/O and H_G(accepted yield).
The 16 slots are a fixed physical-attempt tariff, padded on zero yield, not
free harvesting logic. Debit attempt/transport costs before deposit; reserve
maximum transport before accepting the yield. Collection deposits only into
G's selected source pool. No rejected action receives a yield, chooses a
fallback forage, or manufactures material to fund its own gate. Return mapping
for failed/partial attempts uses B04 CONTROL slots, not another packet.

For scrub let n=5 (repetition) or 20 (block), g=1 or 6 respectively. The
already-paid scan supplies the snapshot and unique decoded payload. Empty/tied
scrub abstains after ACTION's fee with V=A=W=0. Otherwise, after that fee,
reserve gn+128n energy plus local cleanup/store, T and residue before examining
any cell. This is a loop-entry bound, not another gate charge. Then visit the
fixed logical order. Each examined cell pays g even if clean. Each needed-write
attempt pays a distinct 128 gate before testing its WRITE2 body plus remaining
local obligations. A rejected needed write ends the loop immediately.

For V examined cells, A paid needed-write gates and W completed writes:

$$
0\le W\le A\le V\le n,\qquad
C_{\rm scrub,body}=gV+128A+6W+8\sum_W d+\sum_W m.
$$

The first rejected paid gate counts in A; a rejected write uses no material.
Preserve g and 128 for every not-yet-examined cell until it is examined or the
loop terminates; a clean cell releases its unused gate bound without a refund.
This ensures that generation and every possible failed gate remain payable
before testing write material. Quote/write comparisons reuse arithmetic
registers; compare/loop/needed-cell predicates belong to CONTROL256. Do not
retain a generated 20-bit codeword or silently take an intact early exit.
Fixed-policy scrubs use the same rule and prices. The scan is not charged twice.

Repetition LESSON uses the same prefix mechanism with n=5,g=1, but every cell
needs a write, even if its current value would agree; there is no code read.
Its outer body admission reserves C+S, lesson I/O and all five generation/gate
bounds (5+640) before receiving the label. Pay gates only when reached, not all
up front; reserving all five fees is not prepaying them. No full-write material
reservation is required: the first material/energy failure preserves the paid
prefix, with V=A and W<=A. Block COMMIT likewise has n=20,g=6, every cell needs
a write, no code reads, and its already-paid encoding gate checks the 120+2,560
loop bound plus staging retirement, exit and T. Invalid stored validity skips
that loop, not the encoding fee. Rejected loop admission has V=A=W=0.

## Exact live tick order

All phase clocks count planned ticks, not successful operations. This schedule
overrides alternative orderings in the research note. No teaching occurs in
development, H2, isolation or H1 evaluation.

The query-phase order (development, H2, isolated recovery and H1) is:

1. At E>0 apply the public target-independent passive grant in TICK, cap actual
   deposits and pay its M, scalar I/O/transport, living, fixed rent and S.
   Its minimum check covers the complete current-tick mandatory path plus one
   energy after the grant; failure causes shutdown. This is declared external
   support, never reward from a future action. At E=0 only named canonical
   activation, not an ordinary grant, can start a phase.
2. Run the fused CONTROLLER if there is a current maintenance offer. H1 has
   none. The controller's scheduled DECIDE gate runs even if its body rejects.
3. Run RESPONSE, including synchronous ecological yield/return if enabled,
   its mandatory slot read, DECODE gate, possible reward finalization and slot
   clear on every funded path, including invalid/rejected decode. No feedback
   exists in isolation/H1. Complete this before admission into that position.
4. Run ADMIT for the optional current cue. If unaffordable, leave the already
   cleared slot blank and report the future planned response missing normally.
5. Run scheduled priced B03/B04 upkeep and METADATA services. They cannot keep
   hidden per-word ages or infer old Q. Same-value refresh pays to read/rewrite
   the current value and preserves any corruption already present.
6. At the publicly known last learning tick run TERMINAL: optional m=0 update,
   mandatory record retirement. No new observation, dummy action or extra tick.
7. With scratch already cleared by the last service, apply the prespecified
   B03 physical fault, then emit the full persistent boundary snapshot/log.
   Do not charge or perform another tick-end S. No output, callback or delayed
   reward survives in host state. A fault reducing E to zero ends survival now.

An active tick requires funded TICK and E>0 after this final fault. Completion
requires remaining live through the planned horizon, including E>0 after its
last fault. Preserve all inherited numerical active/completion gates; these
definitions fix sampling, not thresholds. Fully served query coverage and recall
are separate measures. A successful response before a fatal fault is still
scored. A completed TERMINAL update/clear stays completed if that fault kills
the worker: no rollback or retroactive missed response. A rejected optional
terminal TD still clears the record; minimum failure before TERMINAL shuts down
without a flush. Faults may alter freshly cleared bytes, but create no protected
callback or right to posthumous learning. Nonlearning entry rules still apply.

Acquisition has a separate order: TICK (grant/minimum check, living/rent, S),
LESSON, COMMIT after every fourth block-coded lesson, scheduled upkeep/METADATA
dues, then fault/boundary. There is no CONTROLLER, RESPONSE or ADMIT, including
no query-slot retirement service on acquisition ticks. A failed fourth LESSON
never cancels that scheduled COMMIT; only physical shutdown stops later work.
The COMMIT mandatory base is already in that fourth tick's earlier tails.

### CONTROLLER internal lifetime

The controller is one atomic operation; its internal stages do not clear scratch.
At most 40 observed-code bits and one four-bit best payload remain while its
four 32-bit arithmetic registers are reused for old/new Q calculations. No saved
second transition, clean Q table or complete list of block candidates is needed.

1. Fund the mandatory base; pay DECIDE before testing its core quote. If rejected,
   clear the old record on learning ticks and exit without observation/action.
   If admitted, receive the offer, scan its code, pay E/local-P sensing, and
   form the observation bin in CONTROL. Thresholds use the actual sensor point
   after paying the 16-energy sensing kernel and both sensor routes, not a
   saved earlier balance. Sample that current E/local-P pair once; no uncharged
   callback recalculates the bin after later debits or deposits.
2. On learning-enabled ticks, pay to read the old transition. If invalid or
   action=3, drop it without inventing a valid action; still pay the TD gate.
   Otherwise pay that gate, test the appropriate body, and, if admitted, update
   using the paid current observation and stored reward. A corrupted terminal
   bit is obeyed: use 97 for terminal or 175 for nonterminal, not clean history.
   Unaffordable update is dropped, not queued. Clear all 32 record bits before
   any current transition is stored. Controller rejection also clears the old
   record via its funded base. Nonlearning entry retired it through ISOLATE;
   frozen controllers ignore even fault-created valid bits and never reread it.
3. Reread the current Q row for ordinary RL action selection after TD. Fixed
   policies execute only their declared priced rule. Choose exactly one action.
4. Perform the action before any due-query response. Fund a forage/collection
   attempt before accepting its capped current yield; no failed action is
   silently replaced by forage. For scrubbing reuse the paid scan in scratch.
   Empty/tied decode abstains. Unique decode visits cells in fixed logical order;
   regenerate every examined symbol, compare against the snapshot, attempt only
   erased/invalid/disagreeing symbols, and pay each attempted gate/write as in
   the ledger. At first unaffordable needed write stop. Preserve
   its paid prefix but no unfinished mask or retry state. Wrong unique decodes
   may miscorrect; truth only enters offline analysis.
5. For learning ticks, store current observation/action/exact action return a,
   terminal if this is the public last learning tick, and valid=1, with reserved
   bits zero. That full store must be reserved before starting the
   observation/decision body.
   Otherwise the operation rejects without choosing an action; it cannot use
   an uncounted action latch to gather resources while claiming to learn.
6. Pay the single outer S and clear scratch. The one record is now the only
   surviving transition. In frozen ecology/recovery no new transition is
   created; observations/actions still occur entirely within the charged
   atomic controller.

The maximum material allowance for the learning controller core is sixteen for
old-record retirement plus sixteen for the new store. A TD update, if admitted,
uses eight more. Scrub writes and status/metadata service are additional. Quotes
for code writes after scanning may be conditional on scratch, but scans never
receive their own health/dirty count for free.

### RESPONSE and reward ownership

Every query-phase tick consumes slot (t-1) modulo five; acquisition does not.
Pay to read it even if invalid. Pay the 128 DECODE gate
on every such tick, even if invalid; only then admit optional decode at the
stored address, bounded over unknown addresses before the read. A funded decode
emits one bit: its unique decoded answer or a fresh readout-only fair guess on
empty/tied memory. Invalid/unaffordable response
emits no bit. Do not decode the scorer's original address or repair the latch.

On ecology ticks with a planned due query the scorer compares the emitted bit
with the originally scheduled cue and returns one bounded scalar physical yield
inside this operation, plus one bounded integer learner return when learning
is enabled. There is no separate correctness flag, target or gradient.
The two encodings represent the same declared task outcome under B04 and are an
acknowledged teaching channel. Spurious outputs without a planned due query earn
nothing. In isolation/H1 both feedback channels are absent, not zero-valued
messages whose timing could reveal correctness.

Reserve the worst valid-record finalization in every learning RESPONSE base
before emission, without relying on a controller-success latch. Pay one
transition-valid-lane read even when no bit is emitted. If valid, read the
16-bit reward once, add b (zero if no contribution), apply four clamp ALUs,
and rewrite the reward once. Do not write an intermediate sum and then rewrite
it a second time. This costs 72 access energy + five ALUs/eight material beyond
the valid read. It runs even on invalid-slot/rejected-decode paths. An invalid
record skips those 77 energy/eight material, with no invented transition;
physical yield may still arrive on an emitted ecological response. Frozen paths
perform no record-valid or reward read/write. Retire all eight due-slot bits on
every funded path. A spurious but valid learning record is treated as stored
state, not repaired using an external controller-success history.

The controller's attempted-action return and RESPONSE return are the only reward
contributions in this selected schedule. ADMIT, living, upkeep and retirement
have physical costs but no additional scalar reward; physical reserves can
affect subsequent opportunities. This restriction prevents a hidden tick-total
cost accumulator. For every permitted failed/partial/successful action and
response path, B04 must supply constants/functions satisfying:

$$
-32768\le a\le32767,\qquad -32768\le a+b\le32767,\qquad
r=\min(256,\max(-256,a+b)).
$$

Use b=0 when no scalar contribution is produced. Compute exact integer a and
a+b; do not clamp a before storage. For example a=300,b=-300 finalizes to zero,
not -44. Only RESPONSE finalizes the uncorrupted reward. With no intervening
fault, the stored prefix remains exact. Later TD consumption clips possibly
corrupted stored rewards again. B04 must use the same objective for competitors
and fit return computation within declared CONTROL slots; no later reward-bearing
event or unpriced accumulation may be added without revising this contract.

At a known learning-phase end, TERMINAL reads the current record, optionally
updates with m=0, then clears it whether update ran or not. Unexpected death loses
an unprocessed transition. Neither a later refill nor experimenter checkpoint
can supply a missing successor or retroactively finish an update.

### Query counts and admission

ADMIT writes a full eight-bit slot with valid=1, current four-bit cue and zero
reserved bits. No lesson label or guessed bit enters it. The slot was retired
first, so failure never retains an overdue address or adds a sixth outstanding
query. No attempt to clear/insert twice is made after a failure.

Keep H1 admissions 1-256 and responses 6-261, with 261 charged live ticks.
Keep H2 admissions 1-507 and responses 6-512. Its scored responses 257-512
correspond to admissions 252-507, with exactly 128 U and 128 O. The five final
drain ticks have maintenance offers independent of the due cue. Development
admits 1-2043 and responds 6-2048. Missing slots do not shrink planned counts.
H1 lacks allocator action and therefore requires explicitly declared B03 support
for its entire response/upkeep-only phase: the capped initial reserves alone
cannot satisfy the necessary bounds below.

## Acquisition, prefix writes and isolation boundaries

Acquisition has 256 lesson ticks: sixteen passes through four consecutive
four-cue blocks. Tick METER/living/rent and end-of-tick faults still apply.
No learned allocation, query admission or ecological correctness feedback occurs
in acquisition; the explicit teacher is the information source. Scheduled teaching
traffic and support are paid/declared, not earned motivation.

Repetition attempts five code writes per lesson in fixed order, including
same-value writes, using the reserved-five-gate prefix rule in the ledger.
Its failed outer admission costs 136 and receives no lesson; its first failed
paid write gate terminates the admitted prefix, not the next scheduled lesson.
Block teaching reads and rewrites the full eight-bit staging block atomically
for the current lesson, preserving other currently stored bits,
setting the current label and its stored valid bit. This replaces the research
note's three-stage validity=0/label/validity=1 transfer: a lesson either funds its
whole staging transfer or leaves the old block unchanged. Whole-block staging
uses four reads and four writes, 36 energy/four material before routes and
operation envelopes. There is no independently authenticated success bitmap.

After the fourth lesson of each block, even if that lesson rejected, run its
single COMMIT opportunity before dues and tick faults. Read all eight staging
bits and pay the encoding gate; only four stored valid ones enable
encoding-body admission. False-valid and wrong-label faults remain possible.
Reserve all twenty generation/write-gate fees before starting that body, then
attempt twenty code writes in fixed logical order; stop on the first
unaffordable write, retaining the paid prefix. Always retire the eight staging
bits on the funded exit path, including no valid payload or no affordable code
writes. Reserve
that retirement before admitting the opportunity. If even minimum retirement
fails, physical shutdown preserves uncleared bytes without future retries.

Full acquisition attempts 1,280 code writes for either code, but block teaching
adds 1,024 staging lane writes and 256 staging-retirement lane writes. These
are real auxiliary material costs, not parity-free information. Partial lessons,
commits, false acceptance and lost teaching opportunities must be reported.
Do not reacquire successful-looking individuals or drop acquisition failures.

Normal isolation/nonlearning entry is the publicly scheduled ISOLATE service
clearing query ring (20 lanes), teaching (16 lanes), transition (16 lanes),
and scratch.
It preserves only the surviving declared code/Q/body/metadata; no old callback
or computed scalar remains reachable. Inability to pay is a failed prerequisite,
not a free restart. A separately named experimenter boundary intervention can
fund these 52 lane writes with identical declared grants across branches, if
selected prospectively in B03/B05. Never conflate that intervention with agent
maintenance. It supplies clearing/resources, not a clean acquired template.

Complete-information erasure is a distinct experimenter intervention: construct
the canonical state from inherited constants, cancel every old reachable event,
and apply identical target-independent activation/support. Record physical
removals/refills as intervention flows, not paid autonomous reconstruction.
The structural proof and production tests remain B07 and later implementation.

## Scratch-liveness obligations

During scan, decoder scratch holds 40 observed-code bits (twenty two-bit
symbols), four candidate bits, four best bits, three five-bit counters and one
tie bit: 40+4+4+15+1=64 of 96 bits, leaving 32 for bounded local state. Never
manipulate the entire 40-bit snapshot as one 32-bit ALU operand; use fixed
subfields/words. Five repetition symbols need only ten raw bits but receive
the same capacity allowance, not extra persistent storage.

The addressing/control partition is micro-PC:16 + lane address:11 + flags:5
=32 bits. Acquired-dependent internal stage/address choices occupy this scratch,
not a protected host PC. Public phase/tick selects immutable ROM; it cannot
replace an acquired loop counter. The four 32-bit arithmetic registers are
reusable operands, not an extra persistent return or resource ledger.

| Stage/gate                  | Live contents in 96-bit decoder partition                                           | Bits              | Arithmetic/control use                                           |
|-----------------------------|-------------------------------------------------------------------------------------|-------------------|------------------------------------------------------------------|
| Scan                        | Raw 40, candidate 4, best 4, counters 15, tie 1; offer cue/usefulness up to 5       | 69                | Kernel arithmetic; 32-bit micro-PC/address/flags                 |
| Old-record load             | Raw 40, best 4, observation 5, full old record 32, offered cue 4                    | 85                | Stream 16 paid lanes; no hidden record copy                      |
| Old TD admission            | Raw 40, best 4, observation 5, old metadata 9, old reward 16, offered cue 4         | 78                | Four registers free for sequential quote comparisons             |
| TD kernel                   | Core raw 40, best 4, observation 5, old metadata 9; offered cue 4                   | 58 core; 62 total | q,r,m,numerator; later quotient/remainder/tie reuse              |
| Selection/action/write gate | Raw 40, best 4, observation 5, action 2, return 16, loop 5, predicates 4            | 76 core; 92 peak  | Extra cue/symbol/counters below; control partition 32            |
| RESPONSE decode gate/scan   | Slot 8, valid lane 2, scan working set up to 64                                     | 74                | Gate before scan; decode arithmetic afterwards                   |
| RESPONSE finalization       | Slot 8, valid lane 2, emitted bit 1, reward 16, b 16, predicates 4                  | 47                | Scan is dead; yield, add and clamp use arithmetic registers      |
| Repetition teaching gates   | Cue 4, label 1, expected symbol 2, loop 5, predicates 4                             | 16                | Quote comparisons; no code snapshot or Q                         |
| COMMIT encoding/write gates | Staging 8, expected symbol 2, loop 5, predicates 4                                  | 19                | Quote comparisons/parity share arithmetic registers              |
| TERMINAL TD gate            | Full old record 32, predicates 4                                                    | 36                | Quote comparisons before q/r/m load; then record/TD reuse        |

Before old TD, the 58-bit core fits, but the already-paid old reward must not
vanish: keep its 16 bits in decoder scratch until the gate finishes, giving
74, plus four for the offered cue =78. The transient full-record load is
81+4=85 before extraction/drop of unused reserved bits. Then move reward into
r using CONTROL; no free reread from RAM or host copy is assumed. Old Q and
successor Q load only after TD
admission. Clear the old record after TD/drop and before the new store.

During selected-action and per-write gates, preserve the full 76-bit row,
including observation, action and current signed return. Keep the four-bit
offered cue in spare decoder bits so Q accesses and gate/write routing may
reuse the control address slot without losing the maintenance unit. Loop
position is five bits. For prefix returns, preserve the four predicate bits
and use spare decoder capacity for at most V,A,W as three five-bit counts.
Replacing the one five-bit loop count by those counts increases the core to
86 bits; adding offered cue 4 and expected symbol 2 gives a 92-bit peak. No
32-bit tick-total expense accumulator is permitted. B04 must implement its
bounded return function with these slots or charged recomputation.

Gates compare one source at a time, reusing four arithmetic registers for
immutable quote component, local remainder component, future-tail component
and sum/comparison temporary. Expected symbol is recomputable from the raw/best
row or occupies two of the spare decoder bits; parity is never regenerated
without its g charge. A needed-cell predicate survives the gate in decoder
predicates. Recompute L from micro-PC/loop and ROM, not a reservation counter.
All scheduled outer S clears the full 256 bits. No quote, partial lesson,
chosen action, return or successful-reservation flag survives exit.

Sensor readings and indexed random inputs are consumed sequentially before
the action stage; they do not coexist with the full write-gate row. RESPONSE
discards the scan before receiving feedback and finalizing reward. TERMINAL
needs no decoder snapshot. This is a bounded slot witness, not implemented
microcode; any actual overlap exceeding a partition or 256 total bits fails
conformance even if ordinary host memory would hold it.

Every future service needs a static slot/register trace checked against CONTROL
and scratch caps. No source-level claim that "locals are temporary" substitutes
for that trace. This requirement is independent of empirical success.

## Immediate affordability consequences

For each ordinary learning/admission tick with funded controller and current
record finalization, mandatory planned bookkeeping uses 48 material units:
16 old-record clear + 16 store + 8 reward write + 4 slot clear + 4 admission.
A successful Q update raises this to 56, before code repair, status or upkeep.
Across four eight-bit material reservoirs the maximum inventory is 1,020 units.
Without replenishment that cannot fund nineteen such 56-unit ticks: 1,064
would be needed. Nor can an experiment assume that thousands of Q updates
are affordable merely because its code bank is only 160 bits.

H1 response/upkeep-only evaluation needs at least 2,068 lane writes: 261 x 4
for slot retirement plus 256 x 4 for admissions. This exceeds all four full
reservoirs by 1,048 units before upkeep. For the selected successful-service
path, no material replenishment prevents full query-service coverage; this
is not the definition of survival/completion. A powered warm-up/drain is not
free. This is a necessary inventory bound, not a simulated observation or
proof that externally supplied support
cannot make the assay feasible. Expose the support as an experimental subsidy.

Kernel-only H1 scans, with all planned valid responses, cost 12,544 energy for
repetition or 962,304 for the fixed block decoder. Including the old service
envelopes, reads, clears, admissions and living already gives the conservative
full-service lower bound:

$$
E_{\min}(K)=261(16+12+24)+256(24)
 +(261+256)(128+256+8)+256K.
$$

This equals 234,924 for repetition and 1,184,684 for block. It deliberately
excludes the newly explicit TICK M/S, all 261 DECODE fees, I/O, routes, rent,
upkeep, hazards, boundary costs and survival residue; it is not a final quote.
Even with all omitted costs zero, either code exceeds a single 65,535 energy
inventory. Accepted additional energy must be at least 169,389 or 1,119,149,
respectively, before those further costs/residue. No-replenishment full H1
coverage is therefore ruled out for both representations, not just block.

There is a separate survival bound with every admission rejected: mandatory
H1 slot clearing alone costs 261 x 4 = 1,044 material, exceeding 1,020. At most
255 ticks can pay that retirement from a full initial stock. Thus no-support
cannot keep the worker live for all 261 ticks even after abandoning recall.
The material-only active-fraction upper bound is 255/261 = 0.97701149;
energy, routing and the final fault can only reduce it. This is an upper bound,
not a prediction or a claim that every inherited active threshold must fail.

Full acquisition's code writes need 1,280 material for either code; block adds
1,024 staging writes and 256 retirement writes, giving 2,560 material. The
full-write deficits beyond stock are at least 260 and 1,540 respectively.
Permitted partial acquisition need not complete all those writes, but its
failures remain in the cohort and cannot be repaired with free reacquisition.

For each source j and every execution prefix t, B03/B06 must establish:

$$
P_j(0)+G_j^{\rm accepted}(\le t)
\ge W_j(\le t)+U_j(\le t)+L_j(\le t),
$$

$$
E(0)+G_E^{\rm accepted}(\le t)
\ge C_E^{\rm debits}(\le t)+L_E(\le t)+1
\quad\text{for every prefix required to remain live}.
$$

Here G means accepted supply, not the inherited configuration symbol; losses
L_j,L_E in these two equations are physical losses, not the gate's local
remainder L. U excludes upkeep lane writes already in W. Accepted grants
exclude cap overflow. At gates these cumulative necessities do not replace
the stronger current componentwise c+L+T+rho reservation. Supply arriving
after a failed prefix cannot rescue it. H1 has no collection or ecological
yield, and ordinary support after shutdown cannot revive a historical worker.

Disclose initial stocks, offered/accepted/overflowed support, routes, rent,
upkeep, losses and boundary/activation interventions by phase and arm. Use
prospectively matched external opportunities, not winner-conditioned top-ups;
different consumption/cap overflow may yield different accepted amounts.
Full query coverage, boundary survival/completion and recall over all planned
rows remain distinct. Feasible subsidized service implies none of the original
retention, adaptive-over-periodic, H2 allocation or erasure-precision gates.
Do not change those gates or choose support after observing a winning code.

These consequences advance B03/B06: exact external support and opportunity
costs are scientifically important, not implementation details. They do not
justify exempting auxiliary writes or lowering the five-point gates after data.
The baseline remains conventional ECC plus ordinary allocation; no subjective
or organismal claim follows even if every future functional gate passes.

## Completion gates and next work

B02 supplies the revised symbolic service decomposition, mandatory/optional
failure paths, gate accounting, scratch witness and event precedence. OP-001
through OP-009 are addressed as specification choices; there is no deliberately
deferred B02 price multiplicity or lifetime decision. It does not supply
executed primitive traces, a resource-feasible G or production noninterference.
CONTROL256 and the padded attempt/selection kernels remain stated modeling
assumptions. Their later static traces must fit without increasing these prices.

Before a design freeze, in order:

1. Independently review this revised B02 ledger, bounded slot witness and
   OP-001 through OP-009 disposition before accepting specification closure.
2. B03: instantiate lane placement, four material routes, twenty domain/age
   rules, rent, finite caps, hazards, neutral support and physical losses.
   Instantiate METADATA plans/packet widths and satisfy source-specific prefix
   bounds, including both H1 full coverage and survival requirements.
3. B04: specify return contributions/prefix bounds, sensor thresholds, fixed
   policies, refresh timing and tuning grids under this objective/lifetime rule,
   with signed-16 a and a+b bounds for every permitted action/response prefix.
4. B05: enumerate full phase/arm/branch/channel schedules and output row counts;
   no missing planned responses, hidden reactivation or adaptive schedule access.
5. B06: prove resource feasibility, useful/obsolete scarcity, H1 and adaptive
   headroom separately, and chance-interval precision prospectively.
6. B07: full information-interface/ownership and operational review. Missing
   production code tests cannot be performed before code exists; specify them
   now and require them before engineering/final interpretations.
7. Archive the design-only freeze only after those decisions pass; then implement
   and validate bounded service traces, full-state reset and ledgers before
   engineering-only runs. Freeze source/configuration/tests/analysis separately
   before untouched final individuals. Failed gates remain failed outcomes.
