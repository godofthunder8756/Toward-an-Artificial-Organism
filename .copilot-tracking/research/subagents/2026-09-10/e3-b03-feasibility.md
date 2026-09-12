---
title: E3 B03 physical and resource feasibility research
description: Analytical candidate placement, upkeep, supply bounds, and unresolved feasibility constraints without implementation
ms.date: 2026-09-10
status: Complete
---

## Scope

Research B03 under the revised E3_OPERATION_CONTRACT_v0_3.md and
E3_STATE_CONTRACT_v0_2.md, with E3_PROTOCOL_v0_1.md supplying the hypotheses.
No implementation, simulation, target draws, final freeze, or historical edits.
Only this research file is authorized to change.

## Questions

* Which finite placements and routes admit bounded operation quotes?
* Which domain-age, rent, upkeep, and fault laws cover every acquired field
  without free resource creation or hidden timestamps?
* Which fixed, target-independent supply schedules satisfy source-specific
  necessary bounds or explicit sufficient-prefix witnesses?
* Can material support sustain bookkeeping without removing H2 scarcity?
* Which B02 issues and B04/B05/B06 blockers remain?

## Decision

Bounded research is complete; B03 is not closed or frozen. The tree below gives
a concrete resource-feasible, externally supported service envelope. It does
not prove accurate recall, learned selective maintenance, or autonomy.

Retain the B02 tariffs. Learning consumes 48 material per ordinary successful
admission tick, or 56 with TD, before upkeep and code writes. H1 retirement alone
needs 1,044 material, exceeding the maximum stock of 1,020. No-support H1 is
impossible even after abandoning admissions. Source-local and upkeep constraints
make this problem more severe, not less.

Main result: high support can fund bounded service, while plausible low support
mainly makes learning bookkeeping scarce. With matched opportunities, freezing
the learner saves more material per tick than even maximal block correction
can consume. There is no demonstrated support level at which ordinary RL must
select obsolete code rather than drop updates, collect more material, or fail.
That is a scientific blocker, not permission to change costs or objectives.

## Evidence and authority

* E3_OPERATION_CONTRACT_v0_3.md was read completely, including its revised
  ledger, scalar inventory, prefix gates, fault timing, and affordability bounds.
* E3_STATE_CONTRACT_v0_2.md was read completely. Its exact field inventory,
  isolation boundary, query timing, and frozen-learning rules are retained.
* E3_PROTOCOL_v0_1.md supplies H1/H2, controls, channels, and original gates;
  relevant hypothesis, resource, intervention, and endpoint sections were read.
* .copilot-tracking/research/subagents/2026-09-10/e3-b02-revision.md and
  .copilot-tracking/research/subagents/2026-09-10/e3-b02-operation-research.md
  provide supporting history, not alternative tariffs or precedence.
* E3_LITERATURE_REVIEW_v0_1.md supplies only previously documented source limits.
  The Yoon/Erez flexible-ECC and Patel/Hsiao adaptive-ECC full-text gaps remain.
  No algorithm from either inaccessible text is imported or attributed here.

All numerical results below are ledger arithmetic or closed-form channel
calculations. Read-only scalar arithmetic checked them; no E3 worker, simulation,
random draws, target tables, or historical outputs were used.

## Candidate G and finite placement

Use a tree, with central executor X, four block hubs B0-B3, and five separate
storage leaves L(j,0)-L(j,4) attached to each Bj. Edges X-Bj and Bj-L(j,k) have
unit length. No other links exist. Executor-to-code distance is two, to ordinary
auxiliary RAM one. Maximum physical shortest path is four; no logical direct
cross-cell copy avoids X or its tariffs.

Set Emax=65,535 at X and Pmax,j=255 at Bj. Each pool supplies only its assigned
writes; no action transfers material between pools. Unused capacity elsewhere
does not rescue a deficient source. Collection replenishes the currently offered
block's pool only. The 48 resource bits serialize these five typed quantities;
they are not RAM lanes on which XOR, WRITE2, or generic refresh can create stock.

For block j, physical code position i=4k+r, with k=0..4 and r=0..3, lies at
L(j,k). Repetition cue 4j+r uses its five positions r,4+r,...,16+r. Block coding
uses columns 1..15,1,2,4,8,15 in increasing physical i order. The same two-layer
lesion removes k=3,4 for both codes: eight symbols per block, 32 in total.
It leaves the first twelve block columns, not a separately selected favorable
puncturing. No distance claim about that puncturing is needed for this budget.

Stripe auxiliary RAM lanes by global lane index modulo four across B0-B3.
Global code lanes are 0..79; auxiliary offset u begins at lane 80+floor(u/2).
Exclude typed resource positions from RAM access. Preserve all existing field
offsets, including the 264 inaccessible reserve bits. This striping places an
eight-lane Q word two lanes at each source, a four-lane query/staging block one
at each, and a sixteen-lane transition four at each. The aligned reward field
also has two lanes at each source. Reads still travel to X and writes back.

| Quantity per source                         | Two-bit RAM lanes |
|---------------------------------------------|-------------------|
| Code                                        | 20                |
| Q                                           | 192               |
| Query ring / staging / transition / metadata | 5 / 4 / 4 / 2     |
| Ages                                        | 10                |
| Inaccessible reserve                        | 33                |
| Accessible code plus auxiliary RAM          | 237               |
| All RAM, including inaccessible reserve     | 270               |

There are 948 accessible RAM lanes, 132 inaccessible RAM lanes, and 24 typed
resource lane positions: 1,104 positions, 2,208 persistent bits, 276 bytes.
Within auxiliary capacity, Q=1,536 bits, typed resources=48, ages=80,
metadata=16, query/staging/transition=104, and inaccessible reserve=264.
No reserve bit is used as a mask, timestamp, refreshed-word list, or balance.
Scratch remains 96+128+32=256 bits, cleared at each operation boundary.

### Domain membership and static prices

Assign five upkeep domains to each block hub, twenty total:

* Domain 5j contains all twenty code cells below Bj, including all five leaves.
* Domains 5j+1, 5j+2, 5j+3 partition that hub's Q lanes into three consecutive
  groups of 64, in increasing global-lane order.
* Domain 5j+4 contains its remaining auxiliary RAM, including age/metadata and
  inaccessible reserve lanes, plus physical Pj. E belongs to domain 4, at X.

Stored age d occupies the original four-bit age field d. Its two lanes follow
the striping rule; an age need not reside in the domain it describes. This is
explicit cross-domain dependence, not an additional copy of the age.

Rent is one energy per allocated domain per live tick: twenty total, even for
empty code or unused reserve. One mandatory METADATA service per live tick,
after admissions, performs the following fixed plan:

* Read the forty age lanes; two paid READ2 operations per domain age.
* Pay physical conditioning dues of four energy and one material per domain,
  from that domain's hub source. These are additional U dues, not RAM writes.
  Conditioning is an abstract hub-local service, with no additional routed
  agent packet or material moved to individual leaves; it does not refresh data.
* Rewrite each complete four-bit age as zero, two paid WRITE2 operations.
  There are no metadata/status writes or scalar packets in this service.

The service is M+C+S, forty reads, forty writes, U_E=80 and U_P,j=5:

$$
C_{\rm upkeep}=392+40(10)+40(14)+80=1432,
\qquad P_{{\rm upkeep},j}=10+5=15.
$$

This candidate buys physical domain conditioning, not restoration or same-value
refresh of Q/code RAM. It is a declared abstract physical process. Claiming that
these dues perform 768 Q-lane rewrites would be a real B02 violation. If that
physical distinction is rejected, use the refresh cost analysis below instead;
do not silently redefine the service. Its CONTROL256 trace is still unverified.

The sixteen controller-metadata bits remain vulnerable RAM but are not used by
this RL-service witness. B04 must price any cursor/counter/flag use by another
policy. One whole-field read/rewrite service would add 584 energy and two
material per source; it is not included by implication.

### Wear, lapse, injuries, and resource conservation

Define age-dependent physical probabilities h(a)=0.001(1+a) and
e(a)=0.0001a, for four-bit a in 0..15. Conditioned age zero gives exactly
0.001 sign flips per occupied code symbol per tick and zero lapse erasure.
Code erasure writes the physical symbol 10; sign flips swap 00/01 and never
populate 10/11. Ordinary auxiliary and reserve bits XOR independently with
probability h; an independent lane-erasure event of probability e sets its
two bits to 00. Neither operation supplies a clean value.

Evaluate the simultaneous storage channel from the post-operation ages, then
apply its resulting bit changes, including changes to the age bits themselves.
There is no historical age snapshot available to a later operation. All normal
funded ticks have just reset all ages, so h=0.001 during acquisition, development,
128-tick recovery, H2, and all 261 H1 evaluation ticks. Challenge is an additional
independent p=0.1 occupied-code sign flip immediately before H1 evaluation.

This all-domain conditioning candidate has a limitation: mandatory unpaid dues
cause shutdown, not a live aging branch. A stored/corrupted age has no lasting
hazard effect if the next conditioning service succeeds. It is a fully serviced
affordability witness, not a nontrivial demonstration of selective upkeep lapse.
It does not satisfy a stronger requirement that living agents experience
graded lapse and selectively allocate domain conditioning; that remains open.
A live lapse candidate requires a different explicit B03 service plan: paid
saturating age increments, paid domain resets, and a nonmandatory conditioning
rule. No one-word Q write may reset its domain while claiming to refresh all
64 Q lanes; either price the full refresh or disclose pooled conditioning.

At every normal tick's final fault step also lose min(E,1) energy and
min(Pj,1) from each pool. These deterministic physical leakage losses are logged
separately from spending, with no RAM operation or extra mutable counter.
Reserve a conservative extra one energy after B02's survival residue when
proving post-fault survival. Leakage can only decrease stock.

Primary H1 lesion and challenge are explicitly code-bank-only; ordinary Q,
ring, transition, metadata, and age wear is not disabled. A distinct secondary
whole-substrate channel can erase all RAM at a selected hub and its leaves,
sink that hub's entire P, and sink floor(E/2), with locations fixed independently
of values. A separate global injury can halve all five reservoirs. These are
finite proposed loss maps, not selected panel frequencies. Do not pool them
with primary H1 or claim that their affordability follows from the primary.
Any injury reaching E=0 is absorbing until a named canonical activation.

Every resource prefix obeys initial stock plus accepted deposits minus paid
debits minus physical losses. Accepted deposits equal offered deposits minus
cap overflow. Faults never reinterpret the serialized high bits as new resources.
After complete erasure, all RAM and resources are canonicalized as contracted;
subsequent activation is independent of every prior history.

For each execution prefix p and source j, require
$P_j(0)+A_j(p)-W_j(p)-U_j(p)-\ell_j(p)\ge0$ and
$E(0)+A_E(p)-C_E(p)-\ell_E(p)\ge1$ while live. At each gate, the stronger
current-reservoir test is componentwise $R\ge c+L+T+\rho$.
Here A denotes accepted supply and ell physical loss, not acquired accumulators.

## Routes, packets, and full-service energy envelopes

Auxiliary READ2/WRITE2 prices are 10/14 energy. Code prices are 17/23, because
code writes add one material hop from Bj to its leaf. Repetition scan is
49+5(14)=119; block scan is 3,759+20(14)=4,039. Q read/rewrite is 81/112;
RL selection is 267; nonterminal TD is 463. Existing fees are unchanged.

Deliver teaching, offers, query admissions, random indices, response bits,
guesses, and ecological scalars at X, distance zero: each still pays its scalar
encoding ALU. E sensing is at X; the selected local-P sensor adds four flit hops.
The non-sensor controller scalar encodings and sensor routes add eight energy
on a complete RL path. All declared packet counts remain within eight.

Supply passive material from an external depot at X, one hop to its designated
pool; TICK charges transport on accepted units only. For uniform offer g to
each source, TICK is at most 157+20+4g=177+4g. Its five scalar encodings are
included, including zeros. Do not charge transport for overflow.
Each public tick supplies a fresh packet of at most 4g material total; no
unbounded depot inventory is reachable by the worker. Energy is likewise a
bounded scalar offer, not an agent-controlled unlimited withdrawal.

Provide a nonbankable local collection opportunity of at most eight material
at each Bj per tick. Only the current offered source can be collected, once;
uncollected supply expires. Request and yield scalars travel one link, costing
4+5 energy. The physical source and destination pool coincide, so accepted
collection material has zero deposit distance: ACTION body costs 16+9=25.
Forage and ecological energy yields are each bounded by 64, with packets at X.
Forage body costs 18. B04 still owes their signed learner-return mapping.
All opportunities are target-independent except the explicitly labeled
correctness-dependent ecological yield, which is absent in isolation/H1.
Collection cannot bootstrap its own learning-core admission. Before accepting
any collection yield, each source must support at least 26 material for old
clear/new store, RESPONSE's worst finalization, and upkeep, excluding optional
TD/admission and final-tick TERMINAL. An admitted TD raises that path to 28.
Another source with ample stock cannot satisfy a deficient component.

| Service upper envelope                         | Energy | Material by source                  |
|------------------------------------------------|--------|-------------------------------------|
| Frozen RESPONSE base                           | 616    | 1                                   |
| Learning RESPONSE worst base                   | 823    | 3                                   |
| ADMIT successful                               | 449    | 1                                   |
| Block LESSON successful                        | 490    | 1                                   |
| Block COMMIT, all twenty writes                 | 3756   | 1, plus 20 at code source            |
| Repetition LESSON, all five writes              | 1154   | 5 at code source                    |
| Full block scrub body, excluding ACTION gate    | 3140   | 20 at code source                   |
| Full repetition scrub body, excluding gate      | 760    | 5 at code source                    |
| Frozen block controller, maximal scrub          | 8118   | 20 at code source                   |
| Learning block controller, TD and maximal scrub | 9317   | 10, plus 20 at code source           |
| TERMINAL with TD                               | 1121   | 6                                   |
| ISOLATE                                        | 1120   | 13                                  |

The learning controller maximum is
744+4039+267+416+112+128+8+463+3140=9317.
Its 744 includes routed old-record clearing; 112/128 are old-record read/new
store transport. The full learning RESPONSE with block decode, guess, output,
and both feedback packets is 823+4039+4=4866. H1's maximum is 616+4039+2=4657.
Unused guess/feedback packets are not charged as actual traffic. These maxima
bound spurious valid slots and records without treating them as known invalid.

Unknown Q addresses still require exactly two write lanes per source. Unknown
code addresses can require twenty at any source, so an early quote must use
twenty in each component, not five after averaging over pools. Later paid cue
discovery narrows the code source. This does not debit eighty actual writes.

### Explicit sufficient-prefix witness

For the envelope only, use a named activation at E=65,535 and Pj=255, then
offer 20,000 energy every tick. Offer the following fixed material amounts to
every source, identically across matched arms, regardless of use or damage:

| Phase / material offer per source | Maximum charged energy per tick | Maximum consumption plus leakage at one source |
|----------------------------------|---------------------------------|-----------------------------------------------|
| Acquisition, g=38                | 6007                            | 38                                            |
| Frozen recovery, g=37            | 14532                           | 37                                            |
| H1 response-only, g=18           | 6787                            | 18                                            |
| Learning, g=56                   | 17586                           | 56                                            |

The last row conservatively includes admission and full TERMINAL together,
although the final learning tick is drain-only. Each row includes TICK, all
appropriate service fees, full optional kernels, maximal code writes, upkeep,
and worst scalar/route costs; energy leakage adds one separately. Repetition
costs less. Collection/forage bodies are smaller than the maximal scrub body.

Induction: if the preceding tick began full, its actual per-source use including
leakage is at most g, and energy use plus leakage is below 20,000. The next
fixed offer therefore restores each reservoir to its cap before preflight.
Within a tick, every possible prefix, remaining fixed loop fee, local cleanup,
and public tail is bounded by the complete envelope. That envelope plus residue
and energy leakage is below Emax and each 255 cap. B02's componentwise gate
invariant consequently admits every financially optional service in this
envelope, not merely the final net balance. No same-tick gain is needed.

This is a sufficient funding witness conditional on the declared injury-free
resource window, service plans, and eventual CONTROL/scratch conformance.
It does not make corrupted validity true, force a scrub action, make tied memory
correctable, or cause a correct answer. Extra B04 services are not covered.
It is not an unconditional full-state implementation proof.
All candidate envelope sums and routed products above are below 65,535,
apart from accumulated horizon totals, which remain below signed 32-bit limits.
Actual G validation still must reject any unlisted or overflowing quote.

Fund ISOLATE separately with the same fixed boundary offer to both arms before
an injury: it consumes thirteen per source and 1,120 energy. Boundary support
does not revive a dead historical worker. The prefix induction requires the
stated initial stock; branches beginning with acquired unequal reservoirs must
instead use their actual stock bounds. Replacing all reservoirs with the same
full stock is an additional named intervention, not an ordinary grant and not
part of ISOLATE. B05 must choose whether the primary preserves body reserves
or uses this explicitly equalized, externally funded condition.

### Finite horizon totals and overflow disclosure

Using the above per-tick transport bounds, full block acquisition costs at most
816,640 energy; repetition costs 746,240. Block acquisition needs 2,560 teaching
material plus 256(64) upkeep/leakage=18,944 total; repetition needs 17,664.
These are bounds for all teaching services, not acquisition accuracy.

Recovery's maximal block energy is 128(14,532)=1,860,096. H1 is at most
261(249+616+1432+4041)+256(449)=1,769,162 energy for block, or 746,042 for
repetition. The H1 maximum scans every tick, including fault-created spurious
valid slots; exactly 256 scheduled responses remain the recall denominator.
Energy leakage and boundary services are additional.

H1 with successful admissions consumes 2,068 routing writes, 15,660 upkeep
material, and 1,044 leakage: 18,772 total, exactly 4,693 per source. Upkeep
dominates routing; code-write disablement does not make evaluation inexpensive.
Even retirement-only live ticks require at least sixteen material per source
before leakage, so full stock cannot fund sixteen such ticks without support.
This is stronger than B02's otherwise valid 255-tick material upper bound.

Fixed g=18 H1 offers 18,792 material over 261 ticks, plus initial stock. First
offers overflow completely under the full-stock witness; later admissions,
drain ticks, action choices, and prior injuries change accepted amounts. Record
offered, accepted, overflowed, spent, lost, and remaining quantities separately.
No accepted-amount equality across arms is assumed or manufactured.

## Why whole-RAM refresh is not a free alternative

The conditioning candidate rewrites only forty age lanes, not Q or all RAM.
Q-only same-value refresh needs another 768 reads and 768 writes each tick:
18,432 access energy and 768 material, before any additional service envelope.
It preserves current corrupt values, not learned pre-fault values.

With TD, admissions, age service, domain dues, and leakage, Q-only refresh
requires 222 material per source on an ordinary learning tick. Add up to twenty
at one source for code scrub and six per source for TERMINAL. These capacities
can fit, but need nearly full replenishment each tick. At g=222 the block energy
envelope is already 35,561 before extra refresh control services. The 20,000
energy support witness does not sustain it. CONTROL256 and scratch traces must
also be shown; lane counts alone are not a service implementation.

An additional fixed full-RAM refresh pass over every accessible lane, including
code but excluding typed resources and inaccessible reserve, needs 237 writes
per source. Merge its age writes with upkeep, counting them only once, but
perform this pass in addition to ordinary learning writes. Add learning's
fourteen per source and five
physical domain dues: 256 per source before leakage, 257 with leakage.
This exceeds both 255 locally and 1,020 globally before additional code scrub.
Only one local collection action is allowed; at least three other sources
still exceed capacity, with no intervening passive material deposit. Arbitrarily
large tick-start offers overflow rather than solve this contradiction.
This rules out that explicit additional-pass workload, not every conceivable
refresh scheme. Counting ordinary writes as refresh for selected fields changes
the access plan and can lower it. Such deduplication requires a declared static
plan or paid observations, never a hidden per-word visited/freshness bitmap.

If a requirement means full auxiliary-RAM refresh but not code, its distinct
bound is 217+14+5+1=237 per source; that is not the same contradiction. It still
requires large flows and paid control traces. Refreshing the inaccessible reserve
through agent operations is prohibited, not another optimization candidate.

At per-bit h=0.001, a frozen unrefreshed sixteen-bit Q word initially at a given
value returns to that exact value after 128 ticks with probability
((1+0.998^128)/2)^16=0.146743. This is an exact-word retention calculation,
not the probability its policy is useless. Same-value refresh would not recover
the original word. Vulnerable policy retention therefore remains substantive.

## H2 material support versus genuine scarcity

Consider 512 full learning ticks with one ordinary Q update each tick, all 507
admissions, full final TERMINAL, no code writes, and the stated upkeep/leakage.
A conservative per-source envelope is

$$
B_j=512(29)+507+6=15361.
$$

The 29 comprises drain-tick bookkeeping, TD, upkeep, and leakage; an admission
adds one. This slightly overbounds initial invalid/terminal TD cases, so it is
a full-service budget envelope, not a necessary spend on every legal trajectory.
If nonterminal TD is valid each tick except the initial update and terminal
choice, the maximum saving is only a few units, not hundreds per source.

With full initial stock, the first grant overflows. No-collection supply over
the remaining 511 ticks is at most 255+511g at each source. Let
S_j=255+511g-15361. The table compares this envelope with candidate g levels.
Negative entries are maintenance deficits before any corrective write; positive
entries are residuals relative to this conservative spending envelope, not
guaranteed accessible code budgets or upper bounds on every actual trajectory.
Skipped work can increase actual residuals; overflow and timing can reduce them.

| g per source | S_j   | Aggregate margin | Collections to cover envelope deficit, at yield 8 |
|--------------|-------|------------------|--------------------------------------------------|
| 27           | -1309 | -5236            | 656                                              |
| 28           | -798  | -3192            | 400                                              |
| 29           | -287  | -1148            | 144                                              |
| 30           | 224   | 896              | 0                                                |
| 31           | 735   | 2940             | 0                                                |
| 32           | 1246  | 4984             | 0                                                |
| 34           | 2268  | 9072             | 0                                                |
| 35           | 2779  | 11116            | 0                                                |
| 50           | 10444 | 41776            | 0                                                |
| 56           | 13510 | 54040            | 0                                                |

At g=27, even 512 collection actions cannot cover the envelope's 5,236 deficit:
their global maximum is 4,096. Initial/terminal TD savings cannot close that
gap. Thus the stipulated update-every-tick workload is impossible, not every
legal agent trajectory. At g=28/29, the table requires source-local opportunities
for at least 100/36 collection actions per source respectively. B05 has not
supplied their prefix timing. Whole-horizon totals cannot exclude an early local
shutdown. Collecting leaves at most 112/368 other actions before code costs.

At g=30 a no-code-spending full-service path is prefix-affordable from full
stock: ordinary ticks consume at most thirty per source including leakage, so
each next grant refills it. Final drain/TERMINAL leaves at least 220 per source.
This proves an auxiliary-service path, not a learned policy or maintenance
advantage. The remaining inventory alone is large compared with the expected
40.96 independent code sign flips over 512 fully conditioned, fully occupied
ticks. Actual corrective writes can differ through repeated visits,
miscorrection, omissions, injuries, and partial repair.

At g=35, aggregate inflow covers even twenty code writes per tick, but locality
does not: fifty can be needed at one source while it receives thirty-five.
A long run of offers to one block can exhaust that source despite surplus
elsewhere. At g=50, ordinary maximal code workloads are covered sourcewise;
the full initial stock also covers the single terminal excess. g=56 supplies
the simpler all-tick envelope witness. Neither is a scarce-code regime.

### Unavoidable subsidy trade-off under this service plan

Without ordinary TD, successful learning bookkeeping falls from 56 to 48.
At g=28 a full admission path with dropped Q updates is feasible before code
costs; scarce material need not express itself as selective obsolete repair.
The kernel update is optional under B02. It cannot be forced merely to make
the scarcity table look favorable.

Frozen no-record operation instead consumes only eighteen per source on
ordinary admission ticks, including upkeep/leakage. It saves twelve per source,
forty-eight total, versus updated RL. That is greater than the maximum twenty
code writes in a block scrub. For example, g=29 gives frozen operation forty-four
surplus units per tick across sources before overflow, even while updated RL
must collect to maintain its bookkeeping. g=18 supports the frozen auxiliary
path but does not support the full learned path. Identical nominal supplies
are scientifically fair opportunities, not identical remaining code budgets.

Changing g by one changes maximum whole-horizon support by 2,044 material,
far larger than the expected baseline code-flip burden. Initial 1,020 stock
also cushions scarcity. A fractional-average public pulse schedule or smaller
initial stock could resolve supply more finely, but needs an exact B05 calendar
and a new prefix proof. Do not introduce branch-winner-dependent top-ups,
outcome-triggered collection yields, or extra reservoirs.

All-domain dues alone consume 30,720 material in H2, plus 2,048 leakage.
Adding updated-learning bookkeeping gives about 61,444 before code, under the
conservative envelope. The generous g=56 offers 114,688 material plus initial
stock. This funds the agent from outside; it does not establish resource autonomy.
H1 may deliberately be externally powered and materially supported, while H2
uses a separately named lower material condition, identical within matched arms.
Neither label removes the bookkeeping subsidy.

H2 may retain neutral energy at 17,000 per tick: for g=30 the maximal ordinary
block tick is 16,361, and its conservative terminal tick is 17,482, payable from
the full stock maintained before that final tick. A grant of 12,000 is not an
equivalent feasible choice for the stipulated full learning workload. With
valid TD, full unique block response, admission, and forage, even dropping all
passive-material transport gives a lower debit bound of
177+6195+4865+449+1432=13,118. Forage plus ecology supply at most 128 additional
energy; 12,128 income cannot sustain that workload. Rejecting scans or updates
is a different path, not a proof of full service. Neutral energy removes starvation
from this candidate; abundant energy cannot demonstrate autonomous foraging.

## Functional headroom is a separate question

Recovery has 128 paid, wearing ticks. Challenge p=0.1 follows. H1 has no
controller, no offers, no actions, no learning, and no ecological return over
all 261 evaluation ticks. Ring admission/retirement, upkeep, and faults continue.
Primary repair and code-write-disabled arms receive identical exogenous recovery
offers, support packets, and indexed physical noise; neither gets an outcome-
dependent refill. Their different expenditures and cap overflow remain visible.

For a useful sensitivity check only, assume correct uncorrupted routing, no
erasures, independent sign flips, and perfectly restored five-copy code just
before challenge. Response at tick t=6..261 precedes that tick's fault, so
there are t-1=5..260 evaluation wear events before it. Put
x_t=0.8(0.998)^(t-1). Mean ideal five-copy accuracy is the average of
1/2+(15x_t-10x_t^3+3x_t^5)/16: 0.943681.

Three unrepaired copies also carry 128 recovery ticks of wear. Substitute
y_t=x_t(0.998)^128 into 1/2+(3y_t-y_t^3)/4: mean 0.830590. Their difference,
0.113092, is optimistic headroom under those assumptions, not an H1 forecast.
The cue/valid payload has 25 exposed bit-ticks during its five-tick residence;
the probability none flips is 0.999^25=0.975298. Routing damage, policy damage,
wrong unique decodes, recovery scheduling, and resource constraints remain.

Even a prefix-funded maximal scrub is not guaranteed reconstruction. H1 must
show at least one paid corrective write and retained functional gain without
answer access. The separate five-point advantage over a tuned periodic rival
has no witness here. H2 obsolete-region spending depends on ordinary RL's
unspecified B04 scalar feedback, not on a protected usefulness-to-scrub rule.

## B02 findings and downstream blockers

No new arithmetic contradiction was found in the revised 48/56, 1,044,
gate, or retirement tariffs. The full-RAM-refresh contradiction is a proposed
physical requirement failing those tariffs, not grounds to change them.
Two genuine contract boundaries must remain visible: domain conditioning cannot
be advertised as unpaid RAM refresh, and an eventual service exceeding CONTROL256
or scratch caps must stop/version B02 rather than quietly raise its allowance.
No completed opcode/liveness trace is claimed.

### Exact next B04 work

* Define bounded signed contributions a and b for attempted forage, collection,
  tied abstention, failed/partial scrub, and ecological outputs. Prove signed-16
  a and a+b bounds and final clipping under B02, without a hidden tick-cost sum.
* Fix paid E/P thresholds at the specified sensor instant, health bins, random
  mappings, and reward scales. Neutral power can collapse the energy bin; do
  not imply that forage still has necessary physical value under this subsidy.
* Specify whether useful/obsolete spending should emerge despite optional TD
  dropping and frozen-policy savings. Do not reward an experimenter-desired
  abandonment pattern or give the allocator true correctness/damage.
* Price periodic/threshold metadata and any Q refresh with exact bounded plans,
  preserving common information and tuning opportunity. Check whether additional
  policy bookkeeping invalidates the g=28..30 prefix budgets.

### Exact next B05 work

* Select initial-reservoir handling, paid isolation support, full arm/branch
  product, and explicit code-only versus whole-substrate injury maps. Keep
  developed failures rather than replacing them with successfully powered clones.
* Freeze finite per-source offers, any coarse/fine pulse calendar, collection
  bounds, caps, leakage, and accepted/overflow logs identically within matched
  arms. Prove prefixes for each actual starting-stock condition.
* Supply current recovery/H2 offers independent of due cues, and all acquisition,
  development, 128-recovery, 261-H1, and 512-H2 calendars. H2 has 507 admissions,
  128 U scored responses, 128 O, and no missing final drain ticks.
* Specify fault and random-purpose/location indexing, boundary injury timing,
  final post-fault active/completion status, negative-control activation, and
  expected row counts. No final individuals or seeds are drawn in this work.

### Exact next B06 work

* Establish source-prefix affordability for the chosen scarce condition with
  B04 policies and actual B05 calendars, including threshold and periodic rivals.
  A total-stock inequality or CONTROL capacity witness is insufficient.
* Find a meaningful useful-retention/selective-code-spending opportunity under
  the housekeeping subsidy, or record infeasibility. Demonstrate positive
  comparator O-write denominators rather than assuming damaging enough storage.
* Assess H1 functional sufficiency and adaptive-over-periodic headroom separately,
  including wearing Q/routing and miscorrection. Retain all inherited gates.
* Establish complete-erasure interval precision under actual dependent output
  and panel structure, alongside structural noninterference. No outcome-dependent
  sample growth, favorable channel substitution, or survivor-only denominators.

## Remaining research and clarifications

* [x] Read the required contracts and checked revised B02 quantities.
* [x] Supplied finite placement, route prices, domain coverage, fault/resource
  typing, static upkeep, and conditional sufficient-prefix funding witnesses.
* [x] Compared low/intermediate/high material conditions and recorded local-cap,
  whole-refresh, bookkeeping-subsidy, and functional-headroom limitations.
* [ ] Resolve whether physical domain conditioning is acceptable or literal
  data refresh/nontrivial live lapse is required; both must remain explicit.
* [ ] Complete the B04/B05/B06 blockers above before any design-only freeze.
* [ ] B07 and later authorized implementation must verify CONTROL/scratch traces,
  exact conservation, production reset, no hidden timestamps, and noninterference.

No user clarification is needed to continue bounded research. Selecting the
conditioning law, starting-stock intervention, and scarce-support calendar is
a prospective design decision, not something these calculations silently freeze.