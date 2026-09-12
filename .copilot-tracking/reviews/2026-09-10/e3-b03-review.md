---
title: Independent E3 B03 physical contract review
description: Full selected-contract review against B02 and the prior feasibility candidate
ms.date: 2026-09-10
status: Complete - selected B03 feasibility accepted within its stated partial scope
---

## Executive verdict

Independent review complete. No Critical, Major or Minor defect was identified
in the selected physical contract. Its service arithmetic, source-specific
HS-AC sufficient-prefix witness and LL-EVAL13 live-lapse construction are
consistent with the revised B02 operation contract. Accept those bounded
pre-code design results, not full B03 closure or a runnable freeze.

LL-EVAL13's tick-17 admitted set is exactly {0,1,5,7}. It does not require
favorable response validity, labels, decoding or age-bit faults. The exact
material trajectory is distinct from the variable energy expenditure and
stochastic stored-age trajectory. The guarantee is financial survival and
scheduled pre-fault lapse, not correct recall or uncorrupted post-fault ages.

OP-001 through OP-009 remain closed at the symbolic B02 specification level.
The proposed CONTROL budgets and scratch allocations are not implemented
instruction/register traces. Their later conformance checks remain required,
but their absence is not a newly discovered pricing defect or a reason to
claim the analytical feasibility calculation has not been supplied.

## Evidence and review limits

Read all selected text, including frontmatter, caveats and final blockers:

* P: E3_PHYSICAL_CONTRACT_v0_4.md, lines 1-606
* O: E3_OPERATION_CONTRACT_v0_3.md, lines 1-941
* R: .copilot-tracking/research/subagents/2026-09-10/e3-b03-feasibility.md,
  lines 1-587

Also read E3_STATE_CONTRACT_v0_2.md in full to verify offsets and corruptible
metadata, and .copilot-tracking/reviews/2026-09-10/e3-b02-review.md in full,
including its appended revised-contract closure assessment. The older opening
verdict in that review does not supersede the appended closure of all nine OPs.

Reviewed SHA-256 identities:

| Source | SHA-256 |
|--------|---------|
| P | F0F05D57B5F98C171FF2956CA4BDFD00A59EDFB3579D3FBE05FB74C8001E1DC8 |
| O | F9AEB8595CC3AB0DFA47EA3F2C3F978F91C81EEB1F51F62AAE62E83B5856B019 |
| R | 8D4873DDB831DB81E66C5EF9CC5D763FCF084056B93AC5B8B38631CA27127E4B |

P selects the current physical plan. R is calculation provenance, not an
alternative current upkeep tariff or supply schedule. Read-only constant
arithmetic checked the prices and totals below. No external lookup, project
program, simulation, experiment, target draw or implementation test was run.
Only this review file was written.

## Findings and exact-fix disposition

| Severity | Count | Disposition |
|----------|-------|-------------|
| Critical | 0 | No contradiction requiring rejection of the selected model |
| Major | 0 | No failing service price, funding prefix or live-lapse guarantee found |
| Minor | 0 | No corrective text change required for the reviewed claims |

PHY001 and subsequent identifiers are reserved for actionable findings; none
is assigned merely to restate an acknowledged downstream dependency. There is
no exact corrective patch to prescribe. In particular, do not revert to R's
1,432-energy service, add an unused cursor service, make conditioning mandatory,
or demand production traces as evidence already available before code exists.
The remaining checks below are verification evidence and bounded next work,
not undisclosed findings.

## Placement and source-age distribution

P 36-112 agrees with the finite inventory and O's route/source rules.

* The tree has $1+4+20=25$ vertices, $4+20=24$ edges and diameter four.
  Code-to-X distance is two; auxiliary-to-X distance is one. A code write
  additionally transports its material one link from its assigned hub.
* Persistent positions are $80+1024=1104$. Removing 24 typed resource
  positions leaves 1,080 RAM lanes: 948 accessible and 132 inaccessible.
  Persistent storage is 2,208 bits, or 276 bytes. Scratch remains 256 bits.
* Each hub has 20 code lanes and 217 accessible auxiliary lanes, plus 33
  reserve lanes: $20+217+33=270$. Accessible auxiliary lanes are
  $192+5+4+4+10+2=217$. No unused alignment gap creates extra memory.
* Q words assign two lanes to each source. Query slots and teaching blocks
  assign one to each; transitions assign four; reward fields assign two.
  Unknown Q addresses preserve these counts. Unknown code destinations require
  a twenty-write maximum in every source component until paid discovery,
  not an averaged five and not eighty actual code writes.
* Domain 5j contains code, the next three domains each contain 64 Q lanes,
  and domain 5j+4 contains the remaining 58 RAM lanes at that hub, including
  its 33 reserve lanes. Thus $20+3(64)+58=270$ lanes per hub. Typed P and E
  membership does not make them bit-flippable RAM.

Age d occupies lanes $924+2d$ and $925+2d$. Even d uses B0/B1, and odd d
uses B2/B3. Each ten-word age operation has five even and five odd indices,
so its ten age rewrites consume five material at every source. The whole
increment pass consumes ten per source. The complete conditioning reset pass
also consumes ten per source, and its five physical dues per hub add five.

All age words are physically stored in auxiliary domains 4, 9, 14 and 19,
not necessarily the domains they describe. This cross-domain dependency is
explicit and covered by the simultaneous pre-fault rule. It neither creates
a second age array nor supplies a free health observation to the allocator.

## Paid services and gate invariants

### Exact age-pass price

P 149-212 separates two mandatory age operations. Each has twenty READ2,
twenty WRITE2, eighty explicit kernel ALUs and one M/C/S envelope:

$$
392+20(10)+20(14)+80=952.
$$

Together they cost 1,904 energy and ten material per source. The eight
instructions per age explicitly assemble, compare, increment, select and mask
the value. The addition can represent sixteen; it does not wrap a saturated
four-bit fifteen to zero. Every input encoding is in 0..15 and every output
is in 1..15. The full read/rewrite is paid even at saturation.

The full word is aligned and shares neither lane with another age. No masked
neighbor-preservation read is missing. READ2 insertion and WRITE2 extraction
are not charged twice; the two explicit scratch-to-register extractions are
separate kernel work, as stated.

The proposed CONTROL allocation is $10(20)+32=232$ per half, versus
$20(20)+32=432$ for the rejected single-envelope design. Kernel ALUs and
bundled lane work are outside that CONTROL allocation. The streaming witness
retains four raw bits, a five-bit index, a predicate and four output bits in
decoder scratch, with four reusable arithmetic registers and the unchanged
32-bit control partition. These fit as design allocations; they are not an
executed instruction or simultaneous-register-use proof.

### Twenty conditioning services

P 214-259 correctly prices each fixed-domain operation:

$$
C_{\rm reject}=128+256+128+8=520,
\qquad C_{\rm admit}=520+4+2(14)=552.
$$

The nested METER is paid even on rejection. The 32-energy body consumes one
material for physical dues and two for age writes. Both writes set complete
dedicated lanes; no old age read or partial-lane preservation is needed.

Its source vector is not three units arbitrarily drawn from a pooled stock:

| Domains | Body vector at B0, B1, B2, B3 |
|---------|-------------------------------|
| 0, 2, 4 | (2,1,0,0) |
| 1, 3 | (1,0,1,1) |
| 5, 7, 9 | (0,1,1,1) |
| 6, 8 | (1,2,0,0) |
| 10, 12, 14 | (1,1,1,0) |
| 11, 13 | (0,0,2,1) |
| 15, 17, 19 | (0,0,1,2) |
| 16, 18 | (1,1,0,1) |

The sum is (15,15,15,15), including dues and resets. Consequently:

$$
C_{\rm upkeep}=2(952)+20(520)+32n=12304+32n.
$$

At n=20 this is 12,944 energy and 25 material per source. Independent envelope
reconstruction gives $42(128)+22(256)+22(8)=11184$; adding forty reads,
eighty writes, 160 kernel ALUs and eighty energy of physical dues yields
$11184+400+1120+160+80=12944$. At n=0 there are still forty writes and
12,304 energy of mandatory work. Rejection is not free clock service.

The claimed at-most-64 CONTROL slots per fixed-domain service are a design
budget within 256, not an unlisted arithmetic kernel or proved microtrace.

### Local remainders, loops and exits

O 183-254 and 400-440 remain intact. A CONDITION minimum reserves its outer
M, C, nested M, S, subsequent mandatory services and energy residue. After
paying the nested M, the body gate preserves its local exit, future mandatory
tail and residue componentwise. Later optional conditioning bodies are not
promoted into T. Otherwise LL-EVAL13 would incorrectly require all twenty
bodies before permitting any one of them.

Admitted conditioning reserves the entire physical-dues/two-write body, so
medium cannot be paid while an unaffordable age write is left pending. No
mid-body fault or later gain restarts it. A rejected body performs no age
write but still exits and advances to the next public service. A failed
mandatory minimum instead shuts down without unpaid work.

The existing scrub/teaching loop rules are unchanged: charge g per examined
cell, each reached 128-energy write gate, and each completed write; reserve
remaining generation/gate fees and local cleanup. The first rejected needed
write terminates that loop. Bounds are not debits or hidden escrow. The new
twenty-service schedule does not introduce a retry loop or a saved success
bitmap across operations.

## HS-AC sufficient-prefix audit

### Routed prices and complete tick envelopes

Auxiliary READ2/WRITE2 are 10/14. Code READ2/WRITE2 are 17/23, including the
write's material hop. The selected scan prices are $49+5(14)=119$ and
$3759+20(14)=4039$. Q read/rewrite are 81/112; selection is
$3(81)+24=267$; nonterminal TD is $81+3(81)+4+23+112=463$.

The other reused bounds check: frozen RESPONSE base 616, learning RESPONSE
base 823, ADMIT 449, block LESSON 490, full COMMIT
$616+20(6+128+23)=3756$, and repetition LESSON
$392+2+5(1+128+23)=1154$. Terminal TD is 217 routed energy, giving full
TERMINAL $392+160+224+128+217=1121$. ISOLATE is $392+52(14)=1120$.

Maximal scrub bodies are 3,140 and 760, excluding ACTION's already-listed
gate. Complete frozen controllers are 8,118 and 1,818; learning controllers
with TD are 9,317 and 3,017. Frozen/H1 RESPONSE maxima are 4,657 and 737;
learning RESPONSE maxima are 4,866 and 946. Invalid/spurious slot or record
paths cannot exceed these bounds.

TICK is at most $177+4g$, not a charge for material that overflowed. Sensor
encoding is already in its sixteen-energy kernel; local-P sensing adds four
flit hops. Collection's request/yield cost 4+5 and its body costs 25; forage's
body costs 18. These are smaller than maximal scrub, and their gains are not
needed for the funding proof. Declared scalar occurrences remain within eight.

| Window | Block energy | Repetition energy | Per-source material maximum including leakage |
|--------|--------------|-------------------|------------------------------------------------|
| Acquisition | 17,559 | 14,467 | 48 |
| Development | 29,138 | 18,918 | 66 |
| Recovery | 26,084 | 15,864 | 47 |
| H1 | 18,339 | 14,419 | 28 |
| High-support H2 reference | 29,138 | 18,918 | 66 |

For example, full learning is
$441+9317+4866+449+1121+12944=29138$ energy. Its worst source uses
$25+10+3+1+6+20+1=66$ material. Including admission and TERMINAL together
is conservative although the actual last tick is drain-only. The other source
bounds are $25+1+1+20+1=48$, $25+1+20+1=47$ and $25+1+1+1=28$.

The increase over R is 11,512 upkeep energy and ten material per source.
Ten more offered units per source add forty maximum transport energy, so
tick bounds increase by 11,552. The 30,000 grant, not R's old 20,000, sustains
the selected worst learning envelope. Unspecified B04 metadata/refresh work
is expressly outside these numbers.

### Capacity, entry and every-prefix survival

FULL-SOURCE-ENTRY supplies E=65,535 and Pj=255 only to an eligible still-live
historical body, logs removed and supplied resources, and preserves RAM. The
subsequent paid ISOLATE leaves E=64,415 and Pj=242 before the ordinary grant.
Every selected first grant restores those expenditures, including LL's g=13.
Acquisition instead starts full and its first grant overflows.

Starting full, worst end-of-tick stocks under HS-AC are bounded below by:

$$
E_{\rm end}\ge65535-29138-1=36396>0,
\qquad P_{j,\rm end}\ge255-66=189.
$$

The applicable next g covers the preceding sourcewise spend including leakage;
30,000 covers energy spending plus leakage. Hence the next ordinary deposit
refills caps. Entry intervention and paid isolation handle changes between
window-specific g values; a lower new g is not assumed to erase arbitrary
acquired stock history by itself.

Every local prefix and remaining public mandatory tail is bounded by the
complete componentwise envelope. Material maxima are below 255; energy cost
plus B02's one-energy residue and the additional final leakage fits 65,535.
This proves admission affordability, not merely positive final net balances.
The proof does not rely on an action yield or cross-source transfer. Reservoir
overflow is excluded from accepted supply, and zero material is allowed while
energy must remain positive after the final fault.

### Horizon arithmetic and coverage meaning

P 471-501's totals check:

* Block acquisition: $256(369+12944+490)+64(3756)=3773952$ energy
* Repetition acquisition: $256(369+12944+1154)=3703552$ energy
* Acquisition material: 29,184 for block and 27,904 for repetition
* Block recovery: $128(26084)=3338752$ energy
* Block H1: $261(289+4657+12944)+256(449)=4784234$ energy
* Repetition H1: $261(289+737+12944)+256(449)=3761114$ energy
* H1 material: $6525+517+261=7303$ per source, or 29,212 overall

Energy leakage and separately paid boundary services are additional to those
energy totals. All 261 query-phase RESPONSE operations are bounded, not only
the 256 planned responses. Fault-created valid warm-up slots can cause extra
scans but not extra planned rows. H1's 7,308 offered material per source is
not automatically accepted supply.

Financially funded decoding/admission and full-horizon survival do not mean
all planned responses are emitted or correct. Corrupted valid/cue fields can
still lose or misroute responses. Without ordinary support, mandatory age
increments and retirement alone require eleven material per source per tick;
$24(11)=264>255$ before leakage or admission. The unsupported control is not
equally viable merely because conditioning bodies may reject.

## LL-EVAL13 exact trajectory and fault qualifications

P 503-549's fixed material trajectory follows from mandatory retirement and
age writes plus financially admitted query writes, not from successful recall.

On each admission tick, retirement consumes one per source, admission one,
and increments ten. Those twelve fit the minimum thirteen available after
the grant. No optional decoding path adds material in frozen H1. The maximum
energy envelope is $18339-4(28-13)=18279$ before leakage. Even starting from
only the 30,000 energy grant leaves at least $30000-18279-1=11720>0$.
Energy therefore cannot make one of these otherwise affordable services fail.

Full conditioning consumes another fifteen per source. Tick one ends at
$255-12-15-1=227$. Each later full-conditioning admission tick adds thirteen
and spends twenty-eight including leakage, reducing end stock by fifteen.
Thus tick sixteen ends at $227-15(15)=2$, and tick seventeen starts at fifteen.
Retirement, admission and increments leave (3,3,3,3) before CONDITION-0.

| Tick-17 service | Body vector | Stocks after admitted body |
|-----------------|-------------|----------------------------|
| 0 admits | (2,1,0,0) | (1,2,3,3) |
| 1 admits | (1,0,1,1) | (0,2,2,2) |
| 2-4 reject | No material debit | (0,2,2,2) |
| 5 admits | (0,1,1,1) | (0,1,1,1) |
| 6 rejects | No material debit | (0,1,1,1) |
| 7 admits | (0,1,1,1) | (0,0,0,0) |
| 8-19 reject | No material debit | (0,0,0,0) |

The four bodies sum to (3,3,3,3). Upkeep is
$12304+4(32)=12432$ energy and $40+4(3)=52$ material, thirteen per source.
The full tick energy bound is $229+4657+449+12432=17767$ plus one energy
leakage. Material leakage is zero at zero stock, not an additional unfunded
unit. All twenty conditioning fees and exits remain paid.

Ticks 18-256 start at thirteen, leave (1,1,1,1) before conditioning, reject
domain 0 and admit only domain 1. That leaves (0,1,0,0); leakage returns all
sources to zero. Their upkeep energy is 12,336 and full tick bound 17,671
before energy leakage. This supports the selected sustained-lapse statement.

The last five drain ticks also fit, without extrapolating the admission-only
pattern past tick 256. Each starts at thirteen, spends eleven per source,
and reaches (2,2,2,2) before conditioning. Domains 0 and 5 admit, leaving
(0,0,1,1); all others reject and leakage returns stock to zero. Upkeep is
12,368 energy; the tick bound is $229+4657+12368=17254$ before energy leakage.
This is a scalar extension of the prefix argument, not a simulated trace.

### Optional responses and end-of-tick faults

The financial pattern is independent of the following functional variability:

* An invalid slot omits optional decoding, not its mandatory read, gate and
  one-per-source retirement. A spurious valid slot may add scan/output/guess
  energy already covered by the maximum. It adds no material or H1 feedback.
* H1 has no controller, collection, forage, ecological yield, reward update
  or TERMINAL. Fault-created transition validity or terminal bits do not turn
  frozen operation back into learning. In learning windows, the larger
  nonterminal TD bound already covers either stored-terminal-bit choice.
* Age corruption changes the input to the next fixed-cost increment, never
  the number of age reads/writes or the source of a reset. Conditioning tests
  typed resources, not a corruptible age, validity or prior-success flag.
* Resource serialization bits are not ordinary bit-flip targets. The selected
  final resource losses are exactly min(E,1) and min(Pj,1), not arbitrary
  XOR faults capable of changing this stock recurrence.

At tick seventeen the sixteen unconditioned ages are in 1..15 immediately
before the fault, even if their preceding stored values were corrupted.
The four admitted domains are zero at that instant. Therefore lapsed hazards
are in h=0.002..0.016 and e=0.0001..0.0015, while admitted domains have
h=0.001 and e=0. This is not a claim that all sixteen lapsed ages equal one.

An end-of-tick age-bit flip or lane erasure may subsequently turn a reset age
nonzero or a lapsed age zero. It changes later increments/hazards, not the
already-selected simultaneous fault probabilities or the paid body list.
P expressly takes hazards from the pre-fault state and qualifies its
at-least-one age statement as pre-fault. There is no guarantee of a monotone
post-fault age trajectory, and none is needed for the stated live-lapse result.
At ticks 18-256 all four code domains lapse; the sole conditioned domain 1
is a Q domain. The diagnostic is fixed-order conditioning, not learned
usefulness-directed selection.

## Invalid cursor and counter nonfinding

The persistent five-bit cursor, periodic counter and diagnostic flags remain
fault-exposed, but the selected B03 services do not read them. Their schedule
uses public fixed ranges and a protected, operation-local five-bit index.
Invalid persistent cursor values therefore cannot redirect or shut down this
particular service sequence. This is irrelevance by nonuse, not repair or an
assumption that metadata stays valid.

Likewise, the RL funding witness does not imply a cursor/counter-dependent
periodic policy has already been priced. B04 must declare paid reads, bounded
invalid branches and any writes if it later uses those fields. Such added
services need revised bounds. O's invalid-cursor rule applies to a cursor-using
operation; it does not require every operation to read an unused field.

## Physical claims and unresolved downstream work

P 114-147 selects sacrificial conditioning, not RAM reconstruction. It exposes
the pooled protection idealization and declares stored age the sole condition
coordinate. Corruption can make that modeled condition better or worse; no
clean physical timestamp, damage map or secret medium inventory repairs it.
Q-only literal refresh would additionally cost $768(10+14)=18432$ energy and
768 material before its control services, and cannot recover old Q values.

P 261-330 consistently applies one post-operation, pre-fault state to the
simultaneous channel. Code sign flips cannot populate erased/invalid symbols;
erasures have precedence. Auxiliary, reserve, age and inactive fields remain
exposed. Typed leakage is a separate sink. HS-AC's h=0.001 is a funded
constitutive-law consequence, not protection against every RAM fault.

The primary lesion removes 32 symbols, eight per block, with the same physical
positions for both representations. Recovery is 128 charged, wearing ticks;
the p=0.1 challenge is additional; a response at t=6..261 follows t-1 ordinary
evaluation faults. The selected document does not promote R's idealized
retention sensitivity calculations into proven functional headroom.

The secondary whole-substrate and global-resource injury maps are specified
as losses, not clean restoration. Their unresolved locations, timing, indexed
noise pairing and branch crossings remain B05 work. Unknown secondary panel
choices are not an unimplemented-proof defect in the named primary funding
window. Conversely, the primary proof must not be exported to those injuries.

For H2, full ordinary updated learning needs forty material per source before
code writes, dropped-TD learning 38, and frozen no-record operation 28.
The twelve-per-source frozen saving is 48 overall, exceeding a maximal
twenty-symbol block scrub. The conservative 512-tick no-code envelope is
$512(39)+507+6=20481$ per source, not a necessary spend for every legal policy.
No scarce H2 support calendar or positive obsolete-write denominator follows.

FULL-SOURCE-ENTRY, repeated H1 support, refill/sham saturation and externally
funded correction remain explicit experimental subsidies. B05 still owes
the full matched branch product; B06 still owes paid functional reconstruction,
the unchanged five-point contrasts, useful-retention/selective-spending
opportunity and erasure precision under dependent outputs. B07 still owes
interface/reset ownership review and later authorized production validation.
These are retained blockers, not implied achievements or new empirical claims.

## Complete selected-document coverage

| P lines | Section | Review disposition |
|---------|---------|--------------------|
| 1-35 | Frontmatter, selection and authority | Partial B03 and reference/diagnostic distinctions retained |
| 36-85 | Finite G and footprint | Exact positions, routes, lane counts and source maxima verified |
| 86-112 | Domains and visible age words | Full RAM coverage and cross-domain age storage verified |
| 114-147 | Material process and rent | Physical idealization explicit; no free data refresh |
| 149-212 | Schedule and two age services | Fees, ALUs, saturation, source distribution and bounded slots checked |
| 214-259 | Twenty CONDITION services | Nested gates, full-body vectors, rejection and totals verified |
| 261-302 | Tick order and simultaneous faults | Pre-fault hazards, typed sinks and post-fault survival distinguished |
| 304-330 | Injury maps and phase exposure | Primary exposure complete; secondary products explicitly open |
| 332-370 | Reservoirs, routes and opportunities | Caps, scalar traffic, yield bounds and sourcewise conservation checked |
| 372-414 | Named entry and support windows | Paid boundary, live eligibility and profile-specific refills checked |
| 416-469 | Service and prefix derivation | Both-code energy/material bounds and every-prefix sufficiency verified |
| 471-501 | Horizons and H1 subsidy | Totals, 261 service ticks, 256 planned responses and saturation checked |
| 503-549 | LL-EVAL13 | Exact tick-17 set, later admissions, drains and fault qualifications checked |
| 551-606 | H2, conservation and final blockers | Updated envelope, no false functional/full closure, future gates retained |

## Recommended next work not performed

No further research is needed to answer this review's questions. The following
existing design and later implementation work is not completed by this review:

* [ ] Carry the 22 named service plans into complete static instruction/register
  traces when that work is authorized. Check CONTROL/kernel separation, scratch
  liveness and simultaneous-fault interfaces; stop/version/reprice if a cap
  fails. A host implementation's temporary locals are not a conformance proof.
* [ ] Complete B04's signed a and a+b bounds, clipping, sensor thresholds,
  policy metadata/refresh plans and grids. Reprice any additional service.
* [ ] Complete B05's full branch/profile/channel products, scarce calendars,
  source-prefix entry conditions, saturation controls, noise indexing and rows.
* [ ] Complete B06's functional, comparative, H2 opportunity and dependent-output
  precision arguments without changing thresholds or selecting favorable noise
  after outcomes.
* [ ] Complete B07's design ownership/reset review, then later authorized
  implementation conformance and production tests before engineering/final use.

Static runtime traces and production tests have not passed here. They are
future requirements, not evidence implied by the pre-code feasibility verdict.
B03 remains partial; B04-B07 remain open; all nine symbolic B02 issues remain
closed. No clarifying question or additional user decision is needed to finish
this bounded review.