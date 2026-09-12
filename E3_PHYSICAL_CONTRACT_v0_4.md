---
title: E3a physical placement and conditioning contract
description: Selected finite physical design, paid domain clocks, supported and live-lapse profiles, and unresolved closure gates
ms.date: 2026-09-10
status: Selected design candidate - B03 partial
---

## Selection and authority

Select the finite placement and physical process below. Retain the state layout
in [E3_STATE_CONTRACT_v0_2.md](E3_STATE_CONTRACT_v0_2.md) and every primitive
tariff in [E3_OPERATION_CONTRACT_v0_3.md](E3_OPERATION_CONTRACT_v0_3.md).
This version instantiates B03 services; it does not edit those contracts or
the hypotheses and gates in [E3_PROTOCOL_v0_1.md](E3_PROTOCOL_v0_1.md).
The earlier [feasibility candidate](.copilot-tracking/research/subagents/2026-09-10/e3-b03-feasibility.md)
is evidence, not the selected upkeep plan or current supply arithmetic.

Select two named profiles, with the same placement, prices and automatic
conditioning process for repetition and block coding:

* HS-AC is the primary always-conditioned, externally supported reference.
  Its specified funding window pays every conditioning body. This is an
  explicit environmental-service simplification, not a demonstration of live
  lapse, selective upkeep, resource autonomy or autonomous foraging.
* LL-EVAL13 is the secondary selective-conditioning/live-lapse diagnostic.
  It uses the same supported acquisition, development and recovery, but reduces
  H1 material offers to thirteen per source. Mandatory paid clocks and query
  service remain affordable while individual conditioning bodies lapse.
  This is not the H2 scarce-material condition and does not replace primary H1.

B03 remains partial: the physical choices and analytical funding bounds are
selected, but complete static CONTROL/register traces and the full B05 branch
product are not supplied. B04-B07 remain open. No program, simulation, target
draw, empirical test pass, implemented runtime trace or design freeze is claimed.

## Finite G and exact physical footprint

G is target-independent ROM: one executor X, four hubs B0-B3, and twenty leaves
L(j,k), where j=0..3 and k=0..4. Edges X-Bj and Bj-L(j,k) have unit length.
There are no other links. The tree has 25 vertices, 24 edges and diameter four.
Code-to-X distance is two; auxiliary-RAM-to-X distance is one. All logical
reads and writes route through X; there is no unpriced cross-cell copy.

Keep exactly 1,104 persistent two-bit positions, 2,208 bits or 276 bytes.
Twenty-four positions serialize typed reservoirs, rather than writable RAM.
The other 1,080 positions are RAM, of which 948 are agent-accessible through
permitted paid operations and 132 are inaccessible reserve. The additional
256 scratch bits do not survive any operation boundary.

For code block j, physical position i=4k+r, with r=0..3, occupies global lane
20j+i at L(j,k). Cue 4j+r has repetition symbols at positions r,4+r,...,16+r.
The block code uses columns 1..15,1,2,4,8,15 in this same physical order.
All twenty code writes for block j consume Pj; a code write's material travels
one link from Bj to its leaf.

For auxiliary bit offset u, the global lane is 80+floor(u/2). Every ordinary
auxiliary lane n is at B(n modulo 4), consuming that hub's P on a write.
Typed resource offsets are exceptions: E is physically at X, Pj at Bj.
Their serialization positions never authorize READ2/WRITE2 stock manipulation.
Resource sensing and exact stock changes use B02's sensor/METER interfaces.

Preserve these inclusive auxiliary offsets without padding:

* Q is 0-1535: 768 lanes, 192 at each hub.
* Query ring is 1536-1575: twenty lanes, five at each hub.
* Teaching staging is 1576-1607: sixteen lanes, four at each hub.
* Previous transition is 1608-1639: sixteen lanes, four at each hub.
* E is 1640-1655; four P quantities are 1656-1687: 48 typed bits.
* Twenty ages are 1688-1767: forty RAM lanes, ten at each hub.
* Metadata is 1768-1783: eight lanes, two at each hub.
* Inaccessible reserve is 1784-2047: 132 lanes, 33 at each hub.

Thus each source has twenty code lanes and 217 accessible auxiliary lanes,
237 accessible RAM lanes total. Its additional 33 reserve lanes give 270 RAM
lanes. Each Q word has two lanes at every source; a slot or teaching block has
one at every source; a transition has four at every source. The aligned reward
field has two at each source. Unknown addresses use these sourcewise maxima,
not an average over pools.

The reserve remains physically present and fault-exposed but cannot be read,
written, refreshed or used as a hidden condition map by the agent. Serialization
and experimenter reset do not grant it an agent interface. Every acquired RAM
field, including all Q, ring payload/reserved bits, staging, transition,
metadata and ages, is exposed to ordinary wear in every live phase.

### Twenty domains and twenty visible state words

There are five domains per hub:

* Domain 5j covers its twenty code cells across all five leaves.
* Domains 5j+1, 5j+2 and 5j+3 cover three successive groups of 64 of that
  hub's Q lanes, ordered by increasing global lane index.
* Domain 5j+4 covers all remaining auxiliary RAM at Bj, including that hub's
  age lanes, metadata and inaccessible reserve, and physical Pj.
  Physical E additionally belongs to domain 4.

All RAM belongs to exactly one domain. Reservoir losses use the separate typed
law below; domain membership never turns a reservoir into flippable RAM.

Age d is the existing four-bit word at auxiliary offsets 1688+4d through
1691+4d. Its lanes are 924+2d and 925+2d. Even d stores one lane at each of
B0 and B1; odd d stores one at each of B2 and B3. These are the only twenty
age words, not hidden timestamps, copies or an extra maintenance table.
An age's storage domain need not be the domain it describes. Its own faults
therefore depend on its physical storage domain's current age.

Ages are declared RAM, accessed by the paid services below. They are not an
undeclared physics-only history. The allocator still has B01's 32 observation
bins; the executor does not give it a free age vector or a new observation.
Only the specified increment and conditioning services intentionally write
these words. Generic WRITE2 is a primitive inside permitted service plans,
not a fourth action allowing the policy to bypass conditioning dues.

## Selected material process

Select abstract sacrificial environmental conditioning: a hub-local supply of
generic protective medium is renewed and dissipatively services a whole domain.
It represents renewing a stabilizing environment around storage, not sensing,
copying or reconstructing its symbols. The service consumes four energy and
one material from the domain's hub, in addition to its explicit age writes.
No target-dependent reagent, pristine answer, clean Q copy or hidden measure
of true damage is involved.

The pooled hub-local process has no additional leaf-directed packet or
material route. Its shared physical protection is an explicit idealization,
not an omitted whole-domain RAM access bill or a second stock of medium.

The inherited physical constitutive law uses the declared four-bit age as the
domain's sole condition coordinate. Replacing the medium plus the paid reset
sets that coordinate to zero and lowers subsequent hazard. The model has no
second protected true age or uncharged medium inventory. Age corruption can
make the modeled condition better or worse; this is an exposed coarse physical
model, not a validated claim about a particular chemical or memory technology.
Material deposited into P alone has no immediate effect on age or RAM.

Conditioning never changes a Q, code, query or other non-age RAM value. In
particular, it cannot restore previous information or perform 768 free Q-lane
rewrites. Ordinary code correction, Q updating and same-value RAM writes do
not reset any domain age. Literal RAM refresh, if later added, must separately
pay all reads/writes and preserve current corruption; it gains no domain-age
reset under this selected law. Q-only refresh would
add 768 reads, 768 writes, 18,432 access energy and 768 material before its
control services; it is not selected here.

Rent is one energy per allocated domain per live tick, twenty total, including
unused code and reserve capacity. Rent is independent of occupancy and whether
conditioning succeeds. B02's sixteen living energy remains additional.

## Paid age and conditioning services

After the tick's ordinary admissions or teaching, first run AGE-LOW for domains
0-9, then AGE-HIGH for 10-19. Only after both complete, run CONDITION-d once
for each d=0..19 in that order. These are scheduled METADATA operations,
not allocator actions. They use no scalar packets and no persistent cursor,
serviced bitmap, successful-gate latch or deferred retry. All competitors use
the same order. Its source/domain bias is disclosed, not selected by usefulness.

All service minimums and later mandatory tails are reserved from public ROM
under B02. A failed minimum shuts the body down; it does not provide a free
clock increment or silently omit a required service. A rejected conditioning
body, in contrast, leaves a live, aged domain and continues to the next service.

### AGE-LOW and AGE-HIGH

Each operation pays M+C+S=392, twenty READ2, twenty WRITE2, and eighty explicit
ALUs. For each four-bit age, read both dedicated lanes, assemble its current
word, saturate its increment at fifteen, mask to four bits and rewrite both
lanes. Always pay the full read/rewrite, including when already at fifteen.
The aligned word shares neither lane with a neighboring age, so no unpaid
preservation of adjacent fields or additional masked single-bit merge is used.

The eight explicit at-most-32-bit kernel instructions per word are:

1. Extract the low two-bit field from the paid read buffer into a register.
2. Extract the high two-bit field into another register.
3. Shift the high field left by two.
4. XOR with the low field to assemble a in 0..15.
5. Compare a with fifteen.
6. Add one to a in a register wide enough for sixteen.
7. Select fifteen if the comparison was true, otherwise the sum.
8. AND with fifteen before the two WRITE2 extractions.

READ2 insertion and WRITE2 extraction are already bundled in their tariffs;
the first two kernel instructions are separate scratch-field-to-register work.
No old age array is saved after this operation. Across the full increment pass,
there are forty reads, forty writes and twenty saturation comparisons inside
160 explicit ALUs. All twenty words are updated even if later conditioning
will reset them; no fusion cancels these paid physical clock writes.

Each operation costs 392+20(10)+20(14)+80=952 energy and five material per
source. Together they cost 1,904 energy and ten material per source.

Use two envelopes rather than claiming one CONTROL256 fits the full pass.
The proposed conservative control allocation is twenty slots per word plus
32 service-scaffolding slots: 20(20)+32=432 exceeds 256, whereas each selected
ten-word service has 10(20)+32=232. The per-word allocation has five slots
for index/address preparation, four for access-stage sequencing, four for
local-remainder selection, three for loop advance/test/dispatch, two for
result/predicate transfers into scratch and two padding slots. This excludes
the eight paid kernel ALUs and bundled lane work.
The fixed 32 covers entry, public range selection and exit administration,
not the separately charged scratch clear. Actual instruction allocation still
requires a static trace; these are design budgets, not executed microcode.

Stream one word at a time. Use a five-bit domain index, not a four-bit index
that addresses only sixteen domains. A candidate scratch allocation retains
two raw lanes (four bits), the five-bit index, a comparison predicate and a
four-bit output in decoder scratch. Four 32-bit arithmetic registers serve
address/kernel/quote calculations sequentially; the 32-bit control partition
remains micro-PC:16, lane address:11 and flags:5. A whole twenty-age vector
would require eighty bits and is not packed into a fictitious 32-bit register.
No stage needs to retain all twenty words. Boundary scratch is cleared in full.

### CONDITION-d and affordability-dependent lapse

Each public fixed-domain service pays its outer M, C, a separate discretionary
M gate, and S even when its body rejects: 128+256+128+8=520 energy.
This explicitly prices a nested B02 subgate; it is not an invented zero-cost
optional branch of the old mandatory METADATA plan. No acquired RAM is read
to decide whether to condition. METER compares the current typed reservoirs.

At its paid subgate, admit the complete body only if it covers local exit,
the remaining mandatory services, any scheduled TERMINAL and survival residue.
The body costs four energy and one material at B(floor(d/5)) for the protective
medium, plus two auxiliary WRITE2 to set the complete age word to zero.
Its additional energy is 4+2(14)=32. Its material vector has one at the domain
hub and one at each of the two age-lane hubs, adding when these coincide.
The admitted service costs 552 energy and three material in total.

Writing v_j for one material debit at source j, that body vector is

$$
b(d)=v_{\lfloor d/5\rfloor}+v_{(924+2d)\bmod4}+v_{(925+2d)\bmod4}.
$$

Pay the physical dues before the two writes. The subgate reserves the whole
body, so there is no paid-medium/unwritten-age partial success, no extra
per-lane gate and no mid-body fault. Rejection executes neither body dues nor
age writes; pay the scheduled exit and continue. No current or later gain
restarts this service. Previous conditioning success has no effect on the
public mandatory tail of later services. Their optional bodies are not reserved
as mandatory, so funding one domain never presumes all twenty can be funded.

The per-domain plan has no scan or arithmetic kernel outside CONTROL, and no
scalar I/O. Budget at most 64 of its 256 control slots for fixed address/stage
selection, gate-branch handling and constant packing, with the rest padding;
METER comparisons are separately paid. Only fixed-domain addresses and a
bounded internal branch survive while this operation runs. This slot budget
also awaits a complete static trace and cannot excuse later unlisted work.

For n admitted bodies and rejection of the other 20-n, the exact scheduled
upkeep energy is 12,304+32n. Its material is ten per source for age increments,
plus the sum of the admitted bodies' specified vectors. At n=20 it is
12,944 energy and 25 material per source: forty reads, eighty writes, 160
explicit ALUs, twenty physical dues and all 22 outer/20 nested envelopes.
At n=0 it is 12,304 energy and ten material per source. This mandatory minimum
is deliberately not cheap; subsequent design must not reuse the old 1,432
energy/15-per-source witness or hide this overhead as padding elsewhere.
Here n is an offline sum of executed bodies, not a stored worker counter.

## Tick order and simultaneous physical faults

Retain B02's TICK, CONTROLLER when offered, RESPONSE, ADMIT order. Acquisition
instead runs LESSON and scheduled COMMIT. Then run both age increments and
all twenty CONDITION services. A last learning tick next runs TERMINAL, then
the physical fault. There is no fault between an operation's quote and exit,
nor between increment and conditioning. No extra action, query or tick is added.

Immediately before the final fault, let a_d be the CURRENT stored age d after
all conditioning operations and other scheduled writes. Select:

$$
h(a)=0.001(1+a),\qquad e(a)=0.0001a,\qquad a\in\{0,\ldots,15\}.
$$

Evaluate every fault probability from this one pre-fault, post-operation state;
then apply all resulting RAM changes simultaneously. Do not process domains
sequentially using an age already damaged by this same fault. In particular,
there is no before-increment or historical-age snapshot determining hazard.
The protected physics can evaluate the current state, but no snapshot or clean
age vector persists as worker state or becomes accessible to a later operation.

For occupied code, independently sample a sign flip with probability h(a_d),
swapping 00/01 only. Every code lane independently has erasure probability
e(a_d), setting 10 with precedence over a flip. Sign flips never populate
10/11; erasure can canonicalize 11 to 10. For all auxiliary and reserve RAM,
independent bit flips have probability h(a_d); an independent lane erasure
has probability e(a_d) and sets both bits to 00, taking precedence. Flips and
erasures use different indexed purposes. Fields are not exempt when inactive,
invalid, recently cleared, or labeled frozen. No clean value is consulted.

Age lanes themselves use their storage domains' pre-fault ages. Their changed
bits influence later increments and later faults, not another lane in this
same simultaneous fault. A successful conditioning pass therefore gives
h=0.001 and e=0 at this tick's fault even if that fault changes an age word.
The next funded service reads that damaged current word, never a clean copy.

At the same final physical step, lose min(E,1) energy and min(Pj,1) from each
reservoir. These typed leakage sinks cannot create stock. Reserve one additional
energy beyond B02's pre-fault survival residue in sufficient post-fault bounds.
After minimum failure, sink remaining E and stop; no unpaid age operation or
flag write runs. Ordinary support cannot revive E=0. Dead planned rows remain.

### Selected injury maps and phase exposure

Primary H1 erases k=3,4 at all four blocks: exactly 32 code symbols, eight per
block. It leaves the same first twelve block columns and three repetition
layers. No favorable separate puncturing or survivor-selected location is used.
This lesion is explicitly code-bank-only, not whole-substrate injury.

Recovery has 128 real, charged, wearing ticks. Under HS-AC its occupied-code
flip hazard is 0.001, not an underpaid or zero-wear interval. After recovery
and the declared pre-H1 boundary services, apply an independent code-only
sign-flip challenge p=0.1 before H1 tick one. It is not a replacement for
ordinary tick wear. H1 then has all 261 wearing ticks, including warm-up and
drain. The same ordinary auxiliary/age/metadata channel continues throughout
acquisition, development, recovery, H1 and any instantiated H2 profile.

H1 disables corrective code writes and Q updates, not paid query/age writes.
It has no allocator offers/actions, collection, forage or ecological feedback.
A response at H1 tick t=6..261 precedes that tick's fault and follows t-1
evaluation wear events. LL-EVAL13 uses the same baseline/challenge but higher
hazard at lapsed domains; it never assumes fully paid h=0.001 there.

Secondary whole-substrate loss at a selected hub sets its code to 10, its RAM
including reserve to 00, sinks its whole P and floor(E/2). A distinct global
resource injury sinks floor(E/2) and floor(Pj/2) at every source, without RAM
restoration. B05 must select target-independent panel locations, occurrence
times and branch crossings; these maps have no inherited funding guarantee
after the injury and must not be pooled with primary code-only results.

## Reservoirs, routes and bounded external opportunities

Set Emax=65,535 at X and Pmax,j=255 at each Bj, with no source transfers or
additional banks. The 48 serialized bits encode precisely those five physical
quantities. Overflow is discarded, not held for a later tick. Resource faults
are typed sinks, never XOR of high bits that manufactures stock.

Auxiliary READ2/WRITE2 cost 10/14 energy; code READ2/WRITE2 cost 17/23.
Repetition scan costs 119; block scan 4,039. Routed Q read/rewrite cost 81/112,
RL selection 267 and nonterminal TD 463. These are unchanged B02 prices.

Teaching, offer, query, random, response, guess and ecological scalars terminate
at X: every occurrence still pays its encoding ALU. E sensing is local;
local-P sensing adds four flit hops. A complete RL controller adds eight energy
for its non-sensor scalar encodings and sensor routes, already included below.
Retain B02's maximum eight scalar occurrences per atomic operation.

Each ordinary live tick offers 30,000 energy and a fixed material g per source.
The energy scalar fits sixteen bits and each selected g fits eight. The external
depot at X supplies a fresh bounded packet, not an agent-reachable stockpile.
Accepted material travels one hop to its hub; no transport is charged on
overflow. TICK costs at most 157+20+4g=177+4g, including living, M/S, five
scalar encodings, rent and accepted-material transport. Deposits before TICK
preflight are the explicit B02 passive-support exception, not action income.

Only the currently offered source has a collectable nonbankable opportunity
of at most eight material on a controller tick. It is at the destination hub,
so deposit distance is zero. Request/yield packets cost four plus five energy;
the body costs 16+9=25 beyond the controller's ACTION gate. Uncollected supply
expires. Forage at X costs eighteen body energy and returns at most 64 energy.
Ecological yield is at most 64 energy and absent in isolation/H1; mappings
remain B04. Yields cannot fund their own admission or bypass mandatory tails.

Every source and every live prefix obey initial stock plus accepted deposits
minus paid debits minus physical losses. Offered totals cannot replace accepted
supply. Apply B02's stronger current componentwise c+L+T+rho gate too. Unknown
code addresses require twenty-write bounds at each possible source until paid
discovery narrows them; that is not eighty actual writes. No cross-source
surplus can fund an understocked source.

## HS-AC named support and prefix bounds

Canonical acquisition activation supplies E=65,535 and Pj=255 to the blank
reset body. These are external initial resources, not agent production. For
each later named reference window, select FULL-SOURCE-ENTRY on a still-live
body: experimentally remove/log its current stocks and supply new E=65,535
and Pj=255 reservoirs at their declared locations. Preserve all RAM at this
step. This explicitly replaces acquired resource history and supplies material
and power; it is not a free agent operation, earned gain or ordinary TICK.
Record both removed stocks and full supplied stocks as intervention flows.

After that intervention, run paid ISOLATE before the first tick of each later
named window. It clears the ring, staging and transition through 52 writes,
costing 1,120 energy and thirteen material per source, plus required residue.
This fixed boundary also applies at entry to development and the high-support
H2 reference; it does not inspect stored validity to waive or add a clear.
At recovery entry it precedes the lesion. At H1 entry it follows recovery's
last fault and precedes the independent challenge. The first ordinary grant
then restores those expenditures before TICK, for both selected profiles.
Acquisition's first ordinary grant instead overflows its full initial stocks.

FULL-SOURCE-ENTRY never applies to a dead historical worker. Determine that
eligibility before replacing resources; deaths retain planned failure rows.
Do not replace failed individuals with successful clones. Complete-information
erasure is a distinct canonical-new-state intervention followed by identical
target-independent activation, not resurrection of old pending records.
Whole-substrate injury after entry does not inherit the full-stock guarantee.

Select the following offers. Energy use is an upper per-tick debit excluding
one additional final leakage and the separately accounted boundary services.
Material offers and maxima are per source. Repetition and block receive the
same 30,000 energy and g, not representation-specific compensation.

| Named window    | Ticks | g  | Block energy | Repetition energy | Material max with leakage |
|-----------------|-------|----|--------------|-------------------|---------------------------|
| HS-ACQUIRE      | 256   | 48 | 17559        | 14467             | 48                        |
| HS-DEVELOP      | 2048  | 66 | 29138        | 18918             | 66                        |
| HS-RECOVER      | 128   | 47 | 26084        | 15864             | 47                        |
| HS-H1           | 261   | 28 | 18339        | 14419             | 28                        |
| HS-H2-REFERENCE | 512   | 66 | 29138        | 18918             | 66                        |

HS-H2-REFERENCE is a high-support comparator, not the scarce H2 condition.
No H2 scarce g, pulse calendar or favorable low-stock tuning is selected.

### Derivation using new service prices

Full upkeep is 12,944, not 1,432. Unchanged routed bounds are frozen RESPONSE
base 616, learning RESPONSE worst base 823, successful ADMIT 449, block LESSON
490, full block COMMIT 3,756, repetition LESSON 1,154, frozen block controller
with maximal scrub 8,118, learning block controller with TD/maximal scrub 9,317,
and TERMINAL with TD 1,121. Full block RESPONSE is 4,657 in H1/recovery or
4,866 on learning ticks, including maximal scan and permitted scalar traffic.

The block tick calculations are:

* Acquisition: 369+490+3756+12944=17559.
* Frozen recovery: 365+8118+4657+12944=26084.
* H1 admission tick: 289+4657+449+12944=18339.
* Learning: 441+9317+4866+449+1121+12944=29138.

Learning conservatively includes admission and final TERMINAL together, although
the actual last tick is drain-only. Select no query admissions during recovery;
it still has maintenance offers and paid RESPONSE every tick, including any
fault-created valid slots. Repetition saves 3,920 per scan and 2,380 in maximal
scrub body, giving controller maxima 1,818 frozen or 3,017 learning, and RESPONSE
maxima 737 or 946. Both codes keep the same offered funding.

Material at the most burdened source is:

* Acquisition: 25 upkeep + 1 LESSON + 1 COMMIT retirement + 20 code + 1 leak = 48.
* Recovery: 25 upkeep + 1 RESPONSE retirement + 20 code + 1 leak = 47.
* H1: 25 upkeep + 1 RESPONSE retirement + 1 admission + 1 leak = 28.
* Learning: 25 upkeep + 10 controller/TD + 3 RESPONSE + 1 admission + 6 TERMINAL
  + 20 code + 1 leak = 66.

These include age resets and physical dues at their actual sources; a block's
code writes are not divided over pools. No bound includes unspecified B04
metadata/refresh services. Whole boundary flags are not updated by implication.

Compared with the previous candidate, upkeep adds 11,512 energy and ten
material per source. Raising each g by ten adds another forty maximum TICK
transport energy. The old tick bounds therefore increase by 11,552. The old
20,000 energy offer cannot sustain this full learning envelope; select 30,000
prospectively, still within sixteen bits. Prior low-g tables are not transferable.

For an eligible full-start window, 29,138+1 is below 30,000 and 65,535;
every sourcewise material bound is at most 66, below 255. Inductively the next
fixed grant refills caps after the preceding tick's bounded spending/leakage.
The complete bounds dominate every local/future mandatory remainder and optional
body, including all twenty conditioners. They consequently fund all specified
financial gates without relying on collection or ecology. FULL-SOURCE-ENTRY
and the first post-ISOLATE grant handle phase changes in g explicitly.

This is a sufficient analytical prefix bound conditional on the service plans
and eventual trace conformance, not successful decoding, learning, survival of
arbitrary earlier injuries or affordability of later additional B04 services.
Branches preserving developed reserves instead require their actual entry
prefixes, rather than pretending that a normal grant overwrote their history.

### Horizon checks and ordinary H1 support

Full-block acquisition energy is at most
256(369+12944+490)+64(3756)=3,773,952; repetition is
256(369+12944+1154)=3,703,552. Material including upkeep/leakage is 29,184
for block and 27,904 for repetition. Recovery's maximal block bound is
128(26084)=3,338,752 energy. These do not establish accurate acquisition/repair.

H1 block energy is at most 261(289+4657+12944)+256(449)=4,784,234;
repetition is 261(289+737+12944)+256(449)=3,761,114. Add 261 energy leakage
and boundary services separately. Only 256 queries are admitted; all 261 ticks
may require a scan because validity is corruptible. Listed horizon aggregates
fit signed 32-bit arithmetic but are not stocks. Future quote components and
products must still be rejected before acquisition if invalid or overflowing.

Fully conditioned successful H1 spends 6,525 upkeep material, 517 routing
material and 261 leakage per source: 7,303 per source, 29,212 overall.
Its g=28 offers 7,308 per source over 261 ticks before overflow, plus initial
stock; actual accepted amounts vary. Without support, even rejected conditioning
bodies leave eleven material per source per tick for mandatory age increments
and retirement. A 255-unit source cannot fund 24 such ticks, before leakage
or admissions. Live lapse does not make clocks or retirement free.

Ordinary H1 support introduces repeated global resource refill, although each
source remains local. FULL-SOURCE-ENTRY also eliminates initial reservoir
differences. Material-only refill/sham arms can be saturated and externally
funded correction can overlap primary funding. B05 must explicitly enumerate
those controls and their contrasts or prospectively revise the branch design.
Neither conceal saturation nor label identical opportunities an independent
intervention. Removing H1 support changes feasibility; it does not provide an
equally viable unsupported control. The full branch product remains unresolved.

## LL-EVAL13 live-lapse prefix

Keep FULL-SOURCE-ENTRY, paid ISOLATE, energy 30,000, the same challenge and
all H1 rules. Set only H1 g=13. The first post-ISOLATE grant restores thirteen
spent per source to full; subsequent ticks have at least thirteen available
before spending, even when their preceding end stock was zero.

Age increments cost ten per source, RESPONSE retirement one, and an admitted
query one. Every admission tick can fund these twelve per source; conditioning
cannot overdraw stock or consume a remaining mandatory tail. Leakage is
min(Pj,1), not a requirement to retain one P. Drain ticks cost one less.
The full energy bound is 18339-4(28-13)=18,279 plus one leakage, below 30,000.
Decode and admission are financially affordable before conditioning, although
valid routing and correct recall are not guaranteed. The same minimum-funding
induction keeps the body live throughout the selected code-only H1 window.

The first sixteen admission ticks condition all domains. Tick one ends with
227 per source; subsequent full-condition ticks each reduce the preceding end
stock by fifteen. Tick sixteen ends at two. Tick seventeen starts at fifteen
after its grant; retirement, admission and both age operations leave three at
each source before CONDITION-0. Fixed-order admitted domains are 0,1,5,7:

* Domain 0 consumes (2,1,0,0), leaving (1,2,3,3).
* Domain 1 consumes (1,0,1,1), leaving (0,2,2,2).
* Domains 2-4 reject; all service minimums, gates and exits are still paid.
* Domain 5 consumes (0,1,1,1), leaving (0,1,1,1).
* Domain 6 rejects; domain 7 consumes (0,1,1,1), leaving zero everywhere.
* Domains 8-19 reject; the body remains live after the fault.

All twenty increments were already paid. Four age words reset; sixteen retain
their incremented current values. An unconditioned age is at least one before
the fault, even if its prior stored value was corrupted. A previously zero age
now has h=0.002 and e=0.0001, rather than 0.001 and zero. Continued lapse can
reach 0.016 and 0.0015 at fifteen, subject to ordinary age corruption.

At tick seventeen n=4 gives upkeep 12,432 energy and 52 total material, thirteen
at each source. Its full tick bound is 229+4657+449+12432=17,767 energy plus
one leakage. Later admission ticks start at thirteen per source, spend twelve
before conditioning and can condition domain 1 only; leakage leaves zero
again. Thus lapse is sustained, not merely an unfunded last live tick. This
resource arithmetic needs no favorable label, decode or age-fault realization.

This is a financial prefix calculation, not an executed runtime trace or
functional outcome. It establishes the selected design's live domain-selective
lapse without extra actions/state. Its fixed-order source contention favors
particular domains, not learned usefulness. It cannot demonstrate the H2
selective-code-spending hypothesis. B05 still owes its matched panels/controls.

## H2, conservation and final blockers

All-conditioned ordinary learning with TD/admission needs forty material per
source including leakage before code writes. Dropping TD needs 38; frozen
no-record operation needs 28. The frozen saving remains twelve per source,
48 overall, more than a maximal twenty-symbol block scrub. Additional common
upkeep has not solved the housekeeping subsidy problem. For 512 learning ticks,
507 admissions, full TERMINAL and no code writes, the conservative envelope is
512(39)+507+6=20,481 per source, not the previous 15,361. With lapsed bodies,
spending is state-dependent; this envelope is not a necessary spend for every
legal policy. No favorable H2 g is chosen to force a desired spending pattern.

Record offered, accepted, overflowed, spent, physically lost and remaining
resources by source, with intervention removals/refills separate. Distinguish
clock writes, conditioning dues/resets, code correction and other RAM writes.
Audit totals and admitted-domain lists never return to the worker. Complete
erasure still sets code to 10, all auxiliary bits including ages/resources/
reserve to zero, and cancels old events/references before canonical activation.
No old reservoir, age snapshot, evaluator cue or checkpoint becomes a repair source.

Remaining gates are explicit:

* B03 is partial. Validate the 22 service instruction/register traces, quote
  maxima, kernel/control separation, five-bit domain indexing, cross-domain
  age dependencies and simultaneous fault interface. If a service exceeds
  CONTROL256 or scratch, stop/version and reprice rather than increase its
  allowance. Host locals or a merely parametric trace do not close this gate.
* B04 must fix signed action/response contributions and prove a and a+b fit
  signed sixteen bits, with exact final clipping, paid sensor thresholds,
  policy/metadata/refresh plans and engineering tuning grids. Neutral power
  can collapse energy bins and the functional need to forage. Added services
  require new prefix bounds, not silent inclusion in HS-AC.
* B05 must complete phase/profile/arm/channel products, entry interventions,
  refill/sham/external-funding saturation controls, resource-injury strata,
  source opportunity calendars, indexed random-purpose/location pairing and
  exact rows. Preserve 128 recovery ticks, 261 H1 ticks/256 planned responses,
  and 512 H2 ticks/507 admissions with 128 U and 128 O final responses, plus
  dead/missing rows and final drains. These selected references supply neither
  the scarce H2 calendar nor a completed experimental branch product.
* B06 must establish genuine H2 useful-retention/selective-code-spending
  opportunity and positive comparator O-write denominators despite optional
  dropped TD, source-local collection, conditioner competition and frozen-policy
  savings. Separately establish H1 paid reconstruction, functional sufficiency,
  five-point no-write and adaptive-over-periodic headroom with wearing Q/routing
  and miscorrection, and erasure interval precision under dependent outputs.
  Funding alone proves none of those gates. Do not relax thresholds, choose a
  favorable channel or grow the sample after outcomes.
* B07 must finish information-interface/ownership and operational review,
  including protected executor/physics assumptions, exact ledgers, all 276
  persistent bytes and reset noninterference. Production tests and implemented
  traces require later authorization and cannot have passed here. A design-only
  freeze can follow only after design gates pass; source/configuration/test
  freezes remain separate prerequisites before untouched final individuals.

No further user decision is required for this selection. Remaining work is
design closure and evidence, not permission to implement or simulate E3.