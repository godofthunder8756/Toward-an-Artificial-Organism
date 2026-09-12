---
title: E3a conventional objective and policy contract
description: Selected bounded returns, paid observations, policy rules and prospective engineering selection with explicit closure limits
ms.date: 2026-09-10
status: Selected design candidate - B04 partial
---

## Decision and authority

Select accepted-resource income minus completed corrective-code-write cost as
the conventional action objective, and a separate same-tick ecological task
contribution. Select no learned-Q refresh, paid common health sensing, fixed
integer Q learning, and the policy rules below. These are decisions, not an
invitation to choose unspecified reward terms inside a later implementation.

Retain the state, operations and physical laws in
[E3_STATE_CONTRACT_v0_2.md](E3_STATE_CONTRACT_v0_2.md),
[E3_OPERATION_CONTRACT_v0_3.md](E3_OPERATION_CONTRACT_v0_3.md), and
[E3_PHYSICAL_CONTRACT_v0_4.md](E3_PHYSICAL_CONTRACT_v0_4.md).
Retain all hypotheses and numerical gates in
[E3_PROTOCOL_v0_1.md](E3_PROTOCOL_v0_1.md). Only B04's previously open policy
choices are supplied here; none of those four files is amended. The
[research note](.copilot-tracking/research/subagents/2026-09-10/e3-b04-policy-research.md)
records the design reasoning and remaining work.

B04's objective, observation, randomness, policy and tuning semantics can be
specified symbolically. Full B04 closure cannot yet be claimed: the complete
non-kernel CONTROL256 trace, especially for the twenty-cell scrub path, is
unverified and the conservative worksheet below exceeds that envelope. This
is not a runnable freeze or a resource-feasibility proof for every new policy.
No code, simulation, engineering execution, final target draw, or empirical
result is supplied. The final configuration, sample and panels remain unfrozen.

## Selected common objective

### Action return and exact units

Actions are encoded as forage 0, collect local material 1, and scrub 2.
Encoding 3 remains invalid. It never becomes an alternative resource action.

Let F be energy actually accepted from this action's forage attempt, C be
material actually accepted from its collection attempt, and W be completed
corrective code-symbol writes in its scrub prefix. They refer to this atomic
controller only. They are not cumulative tick costs or another stored record.
Unselected resource actions have zero accepted yield. Select

$$
a=\left\lfloor\frac{F}{4}\right\rfloor+2C-W,
\qquad 0\le F\le64,\quad0\le C\le8,\quad0\le W\le n,
\qquad n\in\{5,20\}.
$$

Use the integer floor, including for cap-truncated F not divisible by four.
There is no hidden quarter-unit residue. The learner stores these integers in
the existing signed reward word; one stored return unit represents 1/256 in
the Q fixed-point convention. Thus accepted forage contributes one return unit
per complete four energy, accepted collection contributes two per material,
and each completed code write costs one return unit per material it actually
consumes. These weights are assigned exchange values, not derived preferences
or measured physical equivalences.

Select a raw forage opportunity of 64 energy on each offered controller tick
in the named B03 supported windows. Select a raw collection opportunity of
eight material at the currently offered source in those windows. A resource
body rejected by its gate receives no request/yield packet and has F=C=0.
An admitted zero-yield or fully overflowed attempt has zero income but still
pays its physical attempt, I/O and gate charges. In a later scarce profile,
B05 may specify target-independent availability of these opportunities;
the return function already covers every integer yield from zero to its bound.
No scarce availability calendar is chosen here.

Use B02's single incoming yield packet and existing METER cap/deposit operation.
METER determines the accepted amount from the current reservoir after paying
the admitted body's charges; that bounded amount is consumed by return mapping
in the same operation. It is not another delivered scalar, resource sensor,
reusable callback, accepted-yield history or hidden copy surviving a gate.
Forage/collection cannot borrow their yield to pay their own admission.

For scrub, W advances only after a completed WRITE2. A rejected needed-write
gate increases the paid-attempt count, not W. Empty/tied decode, rejected loop
entry, code-write prohibition and a clean unique snapshot all have W=0.
Actual completed writes are charged even if their decoded sign is wrong.
No action-return term uses true correctness, reduction of true damage, health
improvement, number of agreeing cells gained, or an evaluator-approved
maintenance pattern. The separate ecological task term below is explicitly
correctness-dependent and is forbidden in isolation/H1.

Do not select an attempted-resource bonus, potential-based reserve shaping,
an obsolete-avoidance bonus, or a tick-total net-energy/material objective.
An attempt bonus would pay for capped-away supply; reserve-potential shaping
would require further paid observations and a different state/lifetime audit.
The selected function needs neither. It is an assigned resource-return
objective with a real but deliberately partial write-material cost term.

Living, rent, scans, Q/record/query writes, upkeep clocks, conditioning medium,
neutral helper support, and failed write gates remain physically paid but have
no direct reward term. In particular, the one-unit write coefficient does not
claim to price all agent expenditure. Report those omitted direct-reward costs
separately. Their consequences can affect later opportunities and survival.

The action-return function contains no target argument, but its realized value
need not be statistically independent of previously acquired history: accepted
supply depends on current reserves and W on surviving memory. In isolated
recovery these are permitted surviving state, not a fresh answer channel.
Complete erasure must also reset these dependencies, as required by B01/B07.

### Same-tick ecological task contribution

For an emitted response to a planned due query, let v be the scheduled query's
usefulness at response time, and let c indicate agreement of the emitted bit
with that query's true binary target. Only the external scorer knows c and
the original due cue. The controller's current offer and a corrupt stored
address do not replace the scorer's scheduled cue.

Select the physical ecological energy offer and learner contribution as

$$
Y_E=64vc,\qquad b=64v(2c-1),\qquad v,c\in\{0,1\}.
$$

A useful correct response therefore offers 64 energy and contributes +64;
a useful incorrect response offers zero and contributes -64; any emitted
obsolete response offers zero and contributes zero. Penalizing incorrect
useful task responses is explicitly assigned task learning. It is not
autonomous motivation or a health reward. Usefulness of a due response can
differ from usefulness of the simultaneous maintenance offer.

The physical offer is capped at deposit; overflow is discarded. The task
contribution remains the stated b even if a correct response's physical energy
cannot all be accepted. This differs deliberately from accepted action income.
Both packets encode the same declared task outcome (v,c), not independent
feedback or a second event. Neither packet literally transmits the target bit,
but for a useful binary response, its emitted bit plus the signed outcome
can reveal that target. This is a teaching channel. The physical quantity alone is not
an injective encoding: zero can mean obsolete or useful-incorrect. The signed
packet explicitly distinguishes those cases. Do not disguise that information
as label-free resource feedback or infer that the two packets carry identical
numbers of bits of outcome information.

Learning RESPONSE receives the existing physical-yield:16 and signed-return:16
packets once and consumes them synchronously. It sends no further correctness
flag. Missing, invalid, unaffordable or unplanned responses have b=0 and no
feedback packet; a valid record is still finalized through the mandatory path.
Spurious outputs earn neither physical gain nor a scored response.

Frozen ecology receives only the physical-yield packet. Its common task
objective can be evaluated offline from the same scheduled outcome, but no
signed-return packet, transition access or learning is added. Fixed policies
likewise have no learner to receive that packet. This is the same objective
and outcome law, not identical unused I/O expenditure.

Isolation/recovery and H1 have no ecological physical-yield or learner-return
packets, including zero-valued packets or outcome-dependent timing. Recovery
allows only the declared resource opportunities with frozen learning. H1 has
no controller offers, actions or learning; its answer scoring is offline and
does not change resources or operation timing.

### Signed bounds and single-record ownership

The action cases are mutually exclusive:

* Forage has a in 0..16.
* Collect has a in 0..16.
* Repetition scrub has a in -5..0.
* Block scrub has a in -20..0.
* Rejected/abstaining scrub has a=0; a partially written prefix has a=-W.

Thus every valid action prefix satisfies -20 <= a <= 16. Every ecological
contribution is in {-64,0,64}, so -84 <= a+b <= 80. Both bounds are strictly
inside signed sixteen bits, for every failed/partial/successful path and any
combination of current offer and due-query usefulness. In isolation b=0.
No fault occurs between the action prefix and its same-tick finalization.

Store exact a, not a preclipped approximation. RESPONSE alone adds b and
finalizes once as r=min(256,max(-256,a+b)). The clamp is inactive for an
uncorrupted selected main-objective record, but remains mandatory. A corrupt
preexisting signed reward plus b fits a signed-32 temporary in
[-32832,32831] before clamping; do not add in sixteen-bit arithmetic. Later TD
again clips the stored reward because a boundary fault may have changed it.

Follow B02's lifetime without another tuple: consume/update or drop the old
record, retire it, select the current action, execute its bounded prefix,
store the observation/action/exact a, and finalize inside that tick's RESPONSE.
The due response normally belongs to an admission five ticks earlier. Its b
belongs to the current action's one-step return, not an action selected by
looking up that old admission. No five-step credit callback is introduced.
Death can lose an unprocessed record. TERMINAL uses zero bootstrap and clears
the record without a fabricated successor tick or posthumous update.

No record is invented if DECIDE rejected or a stored validity bit is zero.
Fault-created validity/action/terminal bits receive B02's stored-state treatment,
not correction by a hidden controller-success or true-history flag.

The assigned conventional objective for each learning phase of H planned ticks
is the expected discounted return

$$
J(\pi)=\mathbb{E}_{\pi}\left[\sum_{t=1}^{H}
\left(\frac{15}{16}\right)^{t-1}\frac{r_t}{256}\right],
\qquad H\in\{2048,512\}.
$$

For offline objective accounting use a=0 if no current action was selected,
and b=0 when no ecological contribution occurred; dead ticks contribute zero.
This defines a common outcome objective even on a tick whose learner record
is absent. Such an offline return must never create a missing worker record
or retroactive update. The actual learner consumes only the permitted stored
transitions, which can be dropped or corrupted; it is not guaranteed to
optimize this objective. The sum is evaluator accounting, not a new live
accumulator. Nominal main-objective |r_t| <= 84 implies |J| < 5.25; even the
full learner clamp gives the conventional discounted scale bound 16.

Every main representation, fixed policy, write-prohibition and frozen-learning
arm has these same exchange weights, task outcomes and offline objective.
Learning/nonlearning I/O follows B02 rather than sending unused packets.
Only the separately labeled DRIVE and privileged oracle are exceptions to
objective/information matching. Their results cannot satisfy a fair main-arm
advantage claim.

## Paid observation and finite learner

### Exact sensor cuts and health indices

Select Ecut=32768 and Pcut=64 for the untuned reference instantiation.
Define e=1 exactly when observed E >= Ecut, and p=1 exactly when observed
local P >= Pcut; equality is high. Otherwise the corresponding bin is zero.
The finite engineering grid below is the only permitted later tuning of cuts.
There is no hysteresis, normalization history or extra observation bit.

Receive the current offer, pay the full code scan, pay the sixteen-energy
sensor kernel and both sensor routes, then sample the current pair once.
Under B03 the routes add four energy: E is at X and local P at its hub.
The sampled E is after all twenty sensing energy and earlier executed charges,
but before old-record TD/retirement, Q selection, ACTION and the current store.
Reserved obligations are not subtracted as if spent. No later deposit or debit
recomputes the observation. Consume the two readings to form their bits and
release the raw readings before action/write gates.

Set h, in this priority order, using only the paid current scan:

1. h=0: no observed binary symbols; erased and invalid count as unobserved.
2. h=1: at least one observation but no unique minimizer, including a tied
   repetition vote. The empty rule has priority over an all-candidate tie.
3. h=2: a unique decode, every symbol binary and every symbol agreeing with
   that decoded codeword. A wholly wrong but self-consistent codeword is h=2.
4. h=3: a unique decode with at least one erased/invalid/disagreeing symbol.

Use s=16u+8e+4p+h in 0..31, with u the current offer's advertised usefulness.
No damage-to-answer distance, age vector, inferred cue history, missing query
counter, visit count or target-specific health statistic is available. All
main controllers pay the same representation-specific scan K on admitted
DECIDE paths, including periodic and code-write-disabled policies. They pay
for decode/RESPONSE separately as B02 requires.

### Q arithmetic and update timing

Keep 32 rows, three actions, and signed sixteen-bit Q values, initially zero
only at canonical initialization. There are 96 learned scalar parameters,
1,536 bits. Keep alpha=1/8, gamma=15/16, epsilon=1/16 and 1/256 Q units.
Use the current damaged table, never a clean row or shadow policy.

For a valid admitted update, read the stored old q and the current successor
row maximum m, with m=0 when the stored terminal bit is set. Reclip stored
reward to [-256,256]. Use exactly

$$
N=16r+15m-16q,\qquad
q'=\operatorname{sat}_{16}\bigl(q+\operatorname{roundEven}(N/128)\bigr).
$$

Both q and m may be any signed-sixteen-bit value after faults. Thus
-1019888 <= N <= 1019889; terminal N is in [-528368,528384]. Rounded
nonterminal increments lie within [-7968,7968]. Even the loose sum bound
[-40736,40735] fits signed 32 bits before mandatory saturation. No sixteen-bit
intermediate, host float, fractional residue or optimizer state is allowed.

For an unambiguous signed roundEven definition, divide |N| by 128 into an
integer quotient k and remainder d in 0..127. Increment k when d>64 or when
d=64 and k is odd; then restore N's sign. This defines the result, not a
license to exceed B02's 23-ALU TD tariff. A conforming signed quotient/remainder
trace must realize this rule within the inherited kernel budget. For example,
N=64,-64 both round to zero; N=192 rounds to 2 and N=-192 to -2.
With q=m=0 these examples correspond to r=4,-4,12,-12 respectively.

Read the selection row again after TD; an update may have changed that row.
Every invalid/dropped update still pays the specified TD gate. Recovery,
H1 and frozen ecology never update Q. Freezing learning does not freeze Q
faults and does not remove epsilon exploration from offered controller ticks.

The ideal nonquantized discounted-return bound 4096 is a scale check, not
a convergence or precision guarantee. Observation aliasing, fixed alpha,
quantization stalls, finite development, Q corruption, mortality and skipped
updates invalidate any automatic appeal to tabular Q-learning convergence.

### Independent random ranks with no rejection sampling

Each admitted RL selection consumes three separately priced indexed scalars:
B uniform on {0,1} with width 1, T uniform on {0,1,2} with width 2, and
X uniform on {0,...,15} with width 4. All three are supplied on every admitted
RL selection, even if a particular rank is unused. Draws at a rejected DECIDE
are not consumed and cannot shift any future indexed draw.

Explore exactly when X=0, choosing action T. Otherwise construct the maximizing
action mask from the freshly read row. For a singleton choose it; for two maxima
choose the B-th element in ascending action order; for three choose T. For
example the two-action set {0,2} maps B=0 to 0 and B=1 to 2. Conditional on
exploitation, every maximum has probability 1/k. Exploration is uniform over
all three actions and is independent of the row. For k maxima, a maximizing
action's probability is (15/16)/k+1/48 and a nonmaximum's is 1/48.

T is a three-valued primitive input, not two random bits modulo three. The
unused two-bit encoding 3 is a packet-contract error, not a fourth action or
a reason for a worker retry. The external input law is categorical uniform;
finite host random-generation provenance and its distribution tests remain
B05/B07 obligations. No worker rejection loop, local PRNG state or shared
action-count cursor exists. Keep B02's separately charged 24 selection ALUs.

Index each allowed draw by public phase, planned tick, purpose, physical
location/slot where applicable, and externally selected panel. Pair purposes
across arms under B05, without adding the action taken to the random key.
Keep target assignment, opportunity, fault, exploration, readout-guess and
analysis streams separate. The worker receives only the current scalar, not
any seed, run/individual ID, future schedule, target-generation state or
reconstructible key. Independence requires independent generator provenance,
not merely different labels applied to the same exposed target seed.

Empty/tied forced readout gets a separate independent fair bit indexed by
response slot and planned tick. It never supplies a repair sign. Reset cancels
old events and selects target-independent future input indexing; complete
erasure cannot retain an answer-dependent input namespace.

## Selected conventional policies

### Main policy rules

Ordinary RL selects exactly by the preceding Q/rank rule; it has no hidden
low-resource override. Its ACTION gate can reject its selection normally.
The fixed policies use the following resource-priority rule from the same
paid observation: if e=0 choose forage; otherwise if p=0 choose collection;
otherwise evaluate the named maintenance trigger. A false trigger selects
forage. Energy wins when both bins are low. A rejected action does not retry
or fall back. Source selection always follows the current offered cue.

Select these fixed rules:

* Periodic: after the resource-priority branches, scrub on the due ticks of
  interval I; otherwise forage. It ignores u and h for scheduling, but still
  pays the common scan. The shared scrub body reuses that snapshot, abstains
  on empty/tied decoding, and examines/regenerates every clean unique snapshot
  cell without making same-value writes. It does not pay a second scan.
* Threshold: after the resource-priority branches, scrub exactly when h=3;
  otherwise forage. This tests visible disagreement/erasure, not true
  correctness or a desired damage pattern. h=0/1 never authorizes a guess-based
  repair; h=2 does not trigger. No extra health threshold/count or label-specific
  table is used.
* No-maintenance fixed comparator, when included by B05: apply the same
  resource-priority rule and otherwise forage, never scrub. It is not a
  substitute for the paired code-write-disabled RL contrast below.

The threshold predicate is selected exactly, not another health grid. Only
resource cuts and periodic interval are subject to the finite grid below.
All fixed policies ignore u; the utility-conditioned learner can use it.
There is no main-arm reward for obeying u or not scrubbing obsolete cells.

### No-code-write permission and frozen learning

For the primary H1 no-write comparison, use the paired developed RL state
and retain its Q-based inference and all permitted resource actions. Disable
only corrective code writes during the isolated recovery. A selected scrub
pays ACTION's gate and abstains with V=A=W=0; it does not run a hidden repair
or replace the selected action with collection. All common scans, Q selection,
queries, readout, conditioning, rent, routing and physical faults remain.
Both paired recovery policies already have learning frozen. H1 itself has
no controller and disables corrective code writes/Q updates for every arm.

This comparison preserves inference; it does not zero Q, remove paid decoding,
turn all responses into guesses, or exempt non-code RAM from cost/damage.
Calling this arm "no writes" never means stopping required ring, age or other
bookkeeping writes. Offline probes use disposable clones, not live repair
templates. Other paired write prohibitions in B05 must apply this same rule.

Frozen allocator ecology begins from its own paired trained checkpoint using
the funded entry/ISOLATE rule. It retains Q-dependent selection and epsilon,
but performs no transition read/clear/store/finalization or TD gate/update.
Fault-created transition validity is ignored. It receives physical ecology
yield but not b. It is not a fresh pristine fixed table.

On an ordinary learning tick with admitted TD and valid-record finalization,
freezing removes 16 retirement + 16 store + 8 reward + 8 Q-write material,
48 overall or twelve per source. That excludes the once-per-phase TERMINAL
saving. If TD drops, the analogous saving is 40 overall; absent finalization
or other rejected work changes actual savings again. Report the actual
ledger, not a constant refund. Even the ordinary 48 exceeds a maximal
twenty-symbol block scrub. Identical opportunities and 2,464 allocated bits
therefore do not mean matched actual spend or equivalent maintenance scarcity.
Do not add wasteful dummy writes to hide the difference in the primary arm.

### Public periodic clock instead of a new service counter

Select I=8 as the untuned periodic instantiation. Periodic due ticks obey
(t-1) modulo I = 0, starting at tick one of each offered phase, with t the
protected public planned phase tick. For I a power of two, evaluate this as
((t-1) AND (I-1)) = 0 using charged CONTROL work. Tick counting does not pause
when a controller or action rejects. No service is made up on a later tick.
H1 has no controller even if its tick satisfies the arithmetic predicate.

Select this global-clock implementation, not the available eight-bit acquired
periodic counter. It adds no metadata service, lane access, source write or
persistent age/visit table. The existing counter/cursor/flags remain allocated,
fault-exposed and unused by these policies; they are not secretly reset or
read from an audit log. No extra lane storage is activated in the reserve.

The interval is one immutable population-level hyperparameter selected only
from the finite engineering procedure, shared across individuals and paired
branches in its declared comparison family. The phase origin is fixed at one,
not optimized per cue or outcome. This is an inherited target-independent
schedule, not a free acquired schedule. No offline table of per-individual
optimal times, future useful cues, damage, outputs, or learned Q values may
be loaded into clock ROM. The public clock cannot regenerate a historical
due cue or bypass the damaged query ring.

A counter-based alternative would require paid reads and, because the counter
starts at auxiliary bit 1773 and shares boundary lanes, preservation/merge
and rewrite work with ordinary counter faults. It is not selected or priced
as a free alternative here. The selected fixed algorithm/clock is protected;
RL's acquired Q is not. That conventional-rival advantage is disclosed rather
than "matched" by adding an unrequested failure mechanism to the fixed rule.

### Fixed-drive diagnostic with a different objective

Select a separate DRIVE diagnostic using the same Q architecture, constants,
packets and action set but its own explicit action objective

$$
a_D=16\,\mathbf{1}\{\text{selected action is scrub}\},\qquad b_D=b.
$$

An admitted DECIDE selecting scrub earns the assigned drive return even if its
ACTION body rejects, finds no unique value, finds a clean value or completes
no write. A rejected DECIDE creates no current record. Forage and collection
have zero direct DRIVE return irrespective of accepted yield. This objective
is intentionally not a health-improvement measure. It demonstrates externally
assigned maintenance preference, not intrinsic motivation or a fair main-arm
comparison. Do not include DRIVE in any claim of adaptive improvement under
matched reward. Its objective ID must be reported separately.

Bounds are 0 <= a_D <= 16 and -64 <= a_D+b_D <= 80. It uses the same exact
prefix-store and final-clamp rule without another callback. Select the
untuned cuts 32768/64 for DRIVE and no objective-weight search. Learning remains
frozen in recovery, with no b there, and there are no actions or feedback in H1.
An exact-template oracle is also privileged, not a main objective-matched arm;
its operation and branch details remain B05, not an implicit agent capability.

## Conditioning and no Q refresh

Select no literal Q read/rewrite refresh service and no allocator-chosen body
upkeep action in the primary design. Keep the B03 automatic AGE-LOW, AGE-HIGH
and twenty CONDITION services, including their paid rejection paths. A funded
conditioner consumes the declared four energy/one hub material plus its two
age-lane writes. It resets only that domain's existing four-bit age to zero.

The physical law is exactly h(a)=0.001(1+a), e(a)=0.0001a for a in 0..15,
from the simultaneous pre-fault, post-operation stored ages. All covered RAM,
including Q and the ages themselves, remains fault-exposed. An unfunded body
leaves the paid incremented age and can increase future hazard. There is no
second true age, free clean-health channel, protected medium inventory or
Q restoration hidden inside conditioning. Code/Q writes do not reset ages.

Literal same-value Q refresh can copy only the currently read corrupt value.
It cannot determine that a sign or magnitude is wrong without additional
surviving information. Under this selected law it does not even reset domain
age. Reading/reaffirming all 768 Q lanes would cost 768 material and 18,432
access energy before control, with no selected restorative mechanism. Do not
invoke an earlier generic suggestion that refresh reduces hazard to override
this later explicit constitutive law.

Repairable Q would require a separately budgeted redundant representation,
trusted teaching/re-estimation scheme, or different physical mechanism and
new gates. Defer it. No shadow Q, checkpoint restoration, CRC recovery,
per-word upkeep history or new visit counts are permitted. Retain 160 code
bits, 2,048 auxiliary bits including the existing unused reserve, and 256
scratch bits. Fixed policies use no learned scalar parameters; their at most
three immutable cut/interval constants are disclosed ROM, not storage for
acquired policies. All allocated unused capacity still pays its physical rent.

## I/O, scratch and finite control obligations

### Eight scalar occurrences and ephemeral values

On a full RL forage/collection controller path the scalar count is exactly
eight: packed offer 1, E/local-P sensor outputs 2, random ranks 3, request 1,
yield 1. Scrub uses six. A fixed resource policy uses five, a fixed scrub
uses three. Rejected paths consume only their admitted packets. No action
return, accepted-amount notification, success flag, threshold value, time
message or cost-total packet is added. Time and fixed cuts are inherited ROM
inputs whose calculation still occupies CONTROL slots.

The separate RESPONSE has at most four scalars on a learning guessed response:
guess, emitted bit, physical yield and signed return. A unique learning
response has three, a frozen guessed ecological response three, and a guessed
isolated/H1 response two. The
controller and RESPONSE are separate cleared operations, not an eight-packet
allowance that can be pooled across a tick.

Reuse the inherited scratch witness. During scrub retain raw snapshot 40,
best payload 4, observation 5, action 2, signed a 16, predicates 4, and three
five-bit V/A/W counts: 86 bits; cue 4 and expected symbol 2 give 92 of the
96 decoder bits. These counts replace the one five-bit loop slot, not add a
second retained loop index. V supplies traversal position; W counts only
completed writes. Alternatively a=-W can be accumulated directly in the same
return slot, without a second tick ledger. Do not use both alternatives as
extra state. Select the W-count form and form a=-W after the prefix ends.

For resource actions, stream the accepted yield through an arithmetic register,
map it to a, then discard it before the full current transition is packed.
Sensors and randoms die before the write-gate row. The arithmetic four-register
budget and control micro-PC:16/address:11/flags:5 remain unchanged. No entire
forty-bit snapshot is one 32-bit operand. Packed subfields are extracted using
charged instructions. Old-record and RESPONSE scratch stages remain B02's
85-bit and 47-bit witnesses, with no concurrent second transition.

### Non-kernel CONTROL256 worksheet

Every outer controller still pays exactly one 256-energy CONTROL envelope.
This is not permission for unlimited policy logic. The following are
conservative approximate primitive allocations to guide a static paper trace,
not measured counts or proof that an implementation fits:

* Common entry, public branch/stage/exit administration: at most 32 slots.
* Offer unpack, validity, two comparisons, health-result index and observation
  packing after the paid scan: at most 24 slots. The scan's already charged
  empty/tie/agreement logic is not recomputed or counted again here.
* Learning record extraction, validity/action checks, retirement/store packing
  and terminal-bit handling: at most 32 slots; omitted on frozen paths.
* Q row/address and TD admission/selection handoff administration: at most
  16 slots when used; lane work, TD arithmetic and selection kernel excluded.
* Fixed resource-priority/trigger rule, including the three-operation periodic
  predicate and action packing: at most 16 slots. RL needs at most eight
  handoff/packing slots beyond its separately charged selection kernel.
* Resource-yield mapping or W-to-return mapping and action branch exits:
  at most 16 slots, with no extra sensor/callback or running expense total.
* Scrub prefix setup and exit administration: at most 16 slots.
* Each examined scrub cell: allow up to twelve non-kernel slots for snapshot
  extraction, current/expected comparison, needed-write dispatch, V/A/W
  transfers, next-address preparation and loop termination. Generation g is
  separately charged, as are READ2/WRITE2 and the METER fee/comparisons.

A conservative learning-RL scrub worksheet is therefore
32+24+32+16+8+16+16+12n = 144+12n: 204 for repetition, 384 for block.
A frozen fixed scrub worksheet is 32+24+16+16+16+12n = 104+12n: 164 or 344.
Resource-only paths omit loop setup/cell work. A smaller actual trace may fit;
these loose estimates are not a lower-bound impossibility proof. However,
384 or 344 cannot be called CONTROL256 conformance, or hidden under scan/
selection padding. No block-policy execution or design freeze is authorized
on this worksheet. Tighten the actual bounded instruction/slot trace, or
version and price a genuinely different service decomposition before freezing.
Do not increase CONTROL, truncate useful work or split a fused operation with
unbudgeted surviving scratch after observing results.

RESPONSE control budgets must separately enumerate slot/valid unpack and
dispatch (up to 32), decode/emit handling (up to 24), feedback/record packing
(up to 24), and common stage/exit work (up to 32). Its explicit five add/clamp
ALUs, lane accesses and scalar encodings are already charged outside CONTROL.
The external two-packet outcome map is scorer work, not a worker correctness
computation. This 112-slot planning allowance also requires a trace rather
than a claim of completed verification.

B03's 22 upkeep services and B02's remaining services retain their own trace
obligations. Fixed ROM thresholds or return weights are not an exemption from
instruction counting. A realized trace exceeding any cap is a contract failure.
No executable microtrace, instruction-count test or liveness test was run here.

## Finite future engineering selection

### Exact grids and scope

Select the untuned reference as cuts (32768,64), periodic I=8, and threshold
trigger h=3. Fix the objective weights, TD constants, random law, phase origin,
health definition and no-refresh decision; they are not tuning dimensions.

Prospectively permit only these finite grids:

* Ecut in {24576,32768,40960}; Pcut in {32,64,96}.
* Ordinary RL: nine cut pairs, with all Q-learning constants fixed.
* Periodic: those nine pairs crossed with I in {1,2,4,8,16,32,64,128,256},
  for exactly 81 candidates per representation and endpoint family.
* Threshold: nine cut pairs and the single fixed h=3 predicate.
* No-maintenance fixed comparator: nine cut pairs if it is instantiated.
* No-code-write and frozen-allocator ablations inherit the matched selected
  parent policy/cuts; they receive no independent favorable retuning.
* DRIVE has the single selected cuts/objective and is not in the main grid.

These constants use the already selected capacity. No grid adds visit counts,
replay, per-cue periods, learned thresholds, phase offsets or hidden timers.
The grid and ranking rule are selected now. Its future winning element is
not claimed to be known. Defaults are concrete reference values, not reported
as tuned optima or frozen final parameters.

Use only future engineering individuals with IDs 1-8, all retained including
acquisition failures and deaths. Use eight planned engineering panels per
individual, averaged within individual and then equally across the eight
individuals. IDs never seed a reconstructible target packet. B05 must fix the
actual independent engineering input manifest before any execution. These
panels are not the final held-out panels and cannot count as independent
individuals or as confirmatory evidence.

Each candidate gets the same 256 acquisition and 2,048 development ticks and
matched public opportunities/noise. Reuse the same hidden label table for each
engineering individual across representations/candidates, while keeping the
eight individuals' tables independent. A Q-learning candidate starts from its
own canonical state and receives at most the planned online update opportunities;
no trained table is transferred between candidates. Fixed policies run those
same phases under their own rules and do not pay unused learner work. Report
their lower actual spending, all 81 periodic trials and all other trials.
Offline hyperparameter search has a different objective from online reward;
disclose both rather than representing it as lifetime autonomous learning.

### Preselected offline lexicographic ranking

Select separate population-level configurations for the H1 family and H2
family, not per individual, injury, panel or devalued/continued branch. A
family's chosen policy is fixed before its final individuals are acquired.
There is no runtime family/outcome oracle or per-individual schedule table.
Report both selections; do not carry whichever looks better into the other
family after inspecting final results.

For each representation/policy family, rank candidates by this exact tuple:

1. Feasible flag, higher first. Require engineering mean intact recall >=0.90,
   acquisition/development mean active fraction >=0.95, and assay mean active
   fraction and completion each >=0.90. H2 must meet the latter two thresholds
   in both the devalued and continued-use branches. Structural/ledger failures
   are not low scores: stop and fix/version before any such ranking.
2. Recall, higher first. H1 uses mean planned-denominator post-challenge R for
   the partial-damage, correction-enabled HS-AC branch. H2 uses the smaller
   of mean R_U in its scarce devalued and continued-use branches, with the
   same fixed U set and 128 planned U responses in each.
3. Material, lower first. H1 uses mean total corrective-code material during
   its 128 recovery ticks. H2 uses mean total corrective-code material over
   the final 256 ticks, averaged equally across its two branches. Do not use
   only O writes, O-write reduction, or the desired RL advantage as a tuning
   target. Required non-code material and total energy are still reported.
4. Completion, higher first, using H1's full charged assay completion mean or
   the smaller H2 branch mean. This orders candidates even when both already
   meet the coarse feasibility flag.
5. Total paid material across the corresponding full comparison windows,
   lower first, including auxiliary/conditioning work and excluding physical
   losses, overflow and intervention removals. Those remain separate reports.
6. Deterministic grid order, ascending Ecut, then Pcut, then I when present.
   The first tuple wins an exact remaining tie; no seed-dependent tie break.

Here H1 assay active fraction uses all 261 evaluation ticks and completion
requires survival to its final fault, with prior recovery deaths retained as
failures. H2 uses all 512 ticks. Step five counts paid work over recovery plus
H1 for the H1 family, or the full H2 phase averaged over the two H2 branches,
including their paid entry ISOLATE services and any TERMINAL. Experimental
stock replacements and ordinary support are not agent expenditure. B05 must
fix the intact-prerequisite assay's full schedule and paid probe/clone plan
before execution; it cannot redefine its mean based on engineering outcomes.

All means include planned dead/missing failures and use the prescribed paired
panels without active-only filtering. Compare exact rational counts/means
where defined, not an outcome-chosen tolerance. This is a lexicographic
multiobjective selection, not an unspecified trade-off to choose after data.
Also report the common objective return and actual expenditure of every
candidate. Do not select a periodic rival to maximize the learner's margin.

If no candidate is feasible, nominate only the highest-ranked infeasible
candidate for transparent diagnosis; label selection infeasible and do not
claim the prerequisite passes. A development or acquisition failure is not
permission to replace individuals, enlarge the grid or change objective weights.
An out-of-grid redesign needs a new version and newly separated confirmatory
individuals. No engineering execution is permitted until the design-only freeze
and later implementation validation/authorization; final execution additionally
requires the source/configuration/tests/analysis freeze.

H2 selection cannot run until B05/B06 specify and justify the scarce profile.
The HS-H2-REFERENCE is not a surrogate on which to tune a "scarce" optimum.
LL-EVAL13 is an H1 live-lapse diagnostic, not that missing H2 condition.

## High support, failure gates and remaining closure

### Reference support does not establish adaptive opportunity

No new metadata or refresh service is selected, so B03's numerical upper
quotes are not increased by a new service charge, conditional on CONTROL and
kernel conformance. Under a fully refilled supported tick, local P is still
255 at the selected sensor instant: no optional action or learning record
write has yet occurred. A conservative block E reading is at least
65535-441-512-1-4039-20 = 60522. The terms are maximal TICK, executed outer
controller/DECIDE fees, offer encoding, scan and sensing respectively.

Consequently all three E cuts and all three P cuts are high at those admitted
HS sensor points. The nine cut pairs alias there; search cannot create
resource sensitivity out of identical bins. Forage may still earn its assigned
income even though neutral grants finance viability. Collection can overflow,
especially with frozen no-record controllers. Report accepted resources, not
claimed need, offered supply or a supposed internally discovered maintenance
drive. Outside the full-start supported windows, use actual paid sensor values;
do not assume these bounds after whole-substrate or resource injuries.

HS-AC/HS-H2-REFERENCE test a conventional supported reference with ordinary
wear. They do not select the scarce material calendar, guarantee useful/obsolete
opportunity cost, guarantee intact recall, or imply that learned Q will survive.
No primary H2 success is required as a procedural condition if the conventional
reference fails. Record failed prerequisites, unsupported H1/adaptive claims,
or an unevaluable/failed H2 honestly. Do not tune support until a main claim
passes. A later redesigned attempt is a new version, not a repair of a result.

### Preserve the protocol decisions

Keep H1 RL-minus-no-code-write R >=0.05 with paired lower CI >0, H1 RL R
>=0.80 and active fraction >=0.90, and the separate RL-minus-tuned-periodic
R >=0.05 with paired lower CI >0. Require at least one paid reconstruction
write. A positive health change alone does not meet any of these gates.

Keep H2 O-write reductions >=50% against continued usefulness and >=10%
against tuned periodic in devalued ecology, with the specified positive paired
reduction lower intervals. Keep R_U >=0.80, whole-ecology active fraction and
completion >=0.90, and the upper paired interval for continued-minus-devalued
R_U <=0.05. Freeze U/O before branching, use the same 128 U response rows,
and retain zero-reference individuals. Ratios use aggregate individual means;
a zero aggregate comparator denominator is undefined and H2 cannot pass.

Keep mean intact recall >=0.90 and mean active fraction >=0.95 prerequisite
gates, exact information/ledger tests, and complete-erasure noninterference
plus powered accuracy interval contained in [0.45,0.55]. Keep individual-level
panel averaging and the proposed 10,000 paired bootstrap draws with a later
frozen analysis RNG. Insufficient erasure precision is inconclusive, not proof
of a leak or evidence of successful deletion. These are preserved prospective
gates, not a claim that the original candidate sample is adequate.

### Exact next design work

* B04/B03 operational closure: replace the approximate CONTROL worksheet with
  a complete bounded instruction/register trace for each candidate service,
  preserving B02 prices and scalar/slot limits or versioning a changed service.
  Verify kernel/control separation, all threshold equality and fault cases,
  accepted-yield ownership, roundEven and prefix/saturation edge cases on paper
  before design freeze. Implemented tests remain later work, not a pass here.
* B05: select the scarce H2 per-source support and availability/pulse calendar
  without outcome-conditioned gains; complete the representation/policy/profile/
  phase/arm/channel product, learned/frozen pairing, entry funding, sham/refill/
  external-funding saturation contrasts and privileged oracle. Select secondary
  injury locations/times and mixed-block status; expose no intervention names
  to the policy. Fix independent input manifests, faults/ranks/guess pairing,
  acquisition/checkpoint/output formats and exact planned rows, including
  recovery's no admissions, 261 H1 ticks with 256 responses, and 512 H2 ticks
  with 507 responses and the final 128 U/128 O rows. No hidden restart or retry.
* B06: prove sourcewise prefixes and viable scarce H2 gains/opportunity costs
  under collection, optional conditioning, dropped TD and the frozen savings;
  establish positive comparator O-write denominators without guaranteed policy
  behavior. Check H1 reconstruction and wearing-query sufficiency separately
  from five-point adaptive-over-periodic headroom. Select final individual/
  panel counts and prospective erasure-containment assurance under dependent
  outputs. The old 32 individuals/eight panels are still candidates, not a
  justified final sample or outcome-dependent stopping rule.
* B07: complete worker/scorer/physics ownership and information-interface review,
  all-276-byte reset and noninterference obligations, protected clock/ROM and
  conditioning caveats, full operational review and required production tests.
  Only then archive a design-only manifest; authorized implementation and
  engineering precede a separate source/configuration/test/analysis freeze.

No additional user choice is required for this bounded selection. The remaining
blockers are explicit design/verification work. Ordinary ECC plus conventional
allocation may explain any future success, and ordinary failure is an allowed
outcome. No new metaphysical or originality claim follows from these choices.