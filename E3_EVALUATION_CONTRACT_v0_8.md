---
title: E3a bounded evaluation and archive contract
description: Prospective B05 revision with mandatory engineering oracle, discriminating selection, complete reset audits, and sparse replay archives
ms.date: 2026-09-10
status: Selected prospective revision - independent review and B06/B07 closure pending
---

## Authority and explicit supersession

This version supersedes the workload, oracle exclusion, probe multiplicity,
all-history reset-continuation product, every-tick checkpoint requirement, and
RAWCOUNT schemas/formulas in [E3_EVALUATION_CONTRACT_v0_7.md](E3_EVALUATION_CONTRACT_v0_7.md).
It also overrides the full-snapshot-at-every-tick clause in the v0.3 tick order.
Historical files remain unchanged. No previously executed observations are removed:
this is a prospective design revision, not implementation, a freeze, or an experiment.

Apply [E3_CONTROL_CONTRACT_v0_6.md](E3_CONTROL_CONTRACT_v0_6.md), including its
incorporated CT repairs and traces, for all ordinary controllers. Otherwise retain
[E3_POLICY_CONTRACT_v0_5.md](E3_POLICY_CONTRACT_v0_5.md),
[E3_PHYSICAL_CONTRACT_v0_4.md](E3_PHYSICAL_CONTRACT_v0_4.md),
[E3_OPERATION_CONTRACT_v0_3.md](E3_OPERATION_CONTRACT_v0_3.md),
[E3_STATE_CONTRACT_v0_2.md](E3_STATE_CONTRACT_v0_2.md), and the hypotheses,
control purposes, and numerical gates in [E3_PROTOCOL_v0_1.md](E3_PROTOCOL_v0_1.md).
The specifically isolated oracle harness below is the only new physical-law exception.
Ordinary controllers still prepay two CONTROL256 budgets, 512 energy total;
other services retain one C where specified. Ordinary policy interfaces are unchanged;
only the separately allowlisted privileged template interface is added.

EV-001's required privileged positive-control purpose was incorrectly called optional
in v0.7. Select its bounded engineering conformance product below; it is mandatory,
unimplemented, and not a passed control. EV-002 is addressed by the smallest
discriminating product: selection measures for every candidate, full controls for
selected configurations, and complete outcomes only for those selected histories.
Storage convenience does not justify reducing independent individuals, primary
panels, difficult rivals, or raw observations within any selected history.

## Individuals, selection, and branch purposes

Retain eight engineering individuals 1-8 and 32 final individuals 300-331, each
with eight panels. One independent 16-label binary target table belongs to each
individual and is reused across codes, policies, families, candidates, and panels.
Each panel retains its own 256-tick acquisition and 2048-tick development, not a
shared development across panels. Thus final n is 32, not 256 developments or
the number of responses. Coincidentally identical independently drawn tables stay.
No targets, roots, or final winning configurations are drawn or predicted here.

For each code REP/BLOCK and family H1/H2 retain RL's nine cut pairs, PERIODIC's
81 cut/interval settings, THRESHOLD's nine pairs, and DRIVE's one default: 100.
Ecut={24576,32768,40960}, Pcut={32,64,96}, I={1,2,4,8,16,32,64,128,256};
h=3, default cuts 32768/64 and I=8. Each candidate starts from its own canonical
body. No development shortening, Q transfer, omitted alias, or retuning children.

| Product                    | Coverage per engineering individual/panel             | Purpose                                      |
|----------------------------|--------------------------------------------------------|----------------------------------------------|
| Candidate trunks           | 2 codes x 2 families x 100 = 400                       | Equal full experience for selection          |
| H1 SCREEN                  | 2 codes x 100 x I/A = 400 histories                    | Intact feasibility and partial-loss ranking   |
| H2 SCREEN                  | 2 codes x 100 x D/C = 400 ecologies                    | Both branches of feasibility/ranking          |
| H2 prerequisite            | 2 codes x 100 = 200 probes                             | One intact probe per H2 trunk                 |
| H1 PRE                     | 2 codes x 100 = 200 probes                             | One diagnostic PRE per H1 trunk               |
| SELECTED-CONTROL H1         | 2 codes x 4 selected policies x 6 = 48 histories       | Full engineering control coverage             |
| SELECTED-CONTROL H2         | 2 codes x 4 selected policies x 6 + 4 frozen = 52      | Full controls and trained-RL frozen D/C        |
| Selected RL stage probes   | 2 codes x (1 ACUTE + 2 POST) = 6 probes                | Paid partial-loss A/N stored-state diagnostics |
| Fixed H1 diagnostics        | 48 histories, defaults only                           | LL13, FLIP, HUB, RESOURCE                      |
| Fixed H2 diagnostics        | 84 ecologies, defaults only                           | G-DIAG, HS-REFERENCE, MIXED                    |

All rows above use all 8 x 8 engineering cells. SCREEN has no N/M/S/X or frozen
crossing. After ranking, require the full SELECTED-CONTROL product once per
selected code/family/policy on the existing winning developed trunks, before
final draws. This is a dedicated input namespace, including its own I/A and D/C,
not a second selection vote, a new development, or extra confirmatory individuals.
Retain both SCREEN and SELECTED-CONTROL data. Deliberate I/A and D/C repeats avoid
forecasting winner/default overlaps and yield fixed logical totals. PRE and H2
prerequisite remain references to their one actual trunk probe, with no repetition.
Engineering controls are validation/diagnosis, not final scientific gate evidence.

Use v0.5's exact population lexicographic ranking separately per code, policy,
and family: feasible first; recall higher; correction material lower; completion
higher; full-window paid material lower; ascending Ecut/Pcut/I. H1 intact recall
is H1-I FINAL, ranking recall/material/completion are H1-A, not PRE; H2 uses its
intact probe and min(mean D R_U, mean C R_U), with equal D/C material averaging.
Keep intact >=0.90, acquisition and development activity separately >=0.95,
assay activity/completion >=0.90 (both D/C in H2), and every v0.5 cost window.
Do not tune on RL margins, O-write reduction, or desired scientific success.
Retain exact rational ties and infeasible/dead candidates; no feasible candidate
means a labeled diagnostic selection, not a passing prerequisite. Structural
errors stop ranking. DRIVE's different assigned objective cannot pass fair gates.
Report ranking-window and all-experiment costs separately, including all tuning,
probes, controls, resets, oracle subsidies and external handling. Count a referenced
execution once in actual expenditure; disclose logical attribution without extra votes.

Finals have 16 trunks, 48 H1 histories, eight PRE, eight H2 prerequisite probes,
and 52 ecologies per individual/panel: all six H1 and all six H2 controls for
each of four policies and two codes, plus FROZEN-D/C from each H2 RL parent.
There are no final diagnostic grids, secondary injuries, ACUTE/POST clones,
or oracle branches. Selected H1 and H2 configurations remain separately fixed.

## Physical branches and paid phases

The complete H1-I/A/N/M/S/X and H2-D/C/N/M/S/X branch definitions, whole-block
U/O assignment, external dispatch conventions, and fixed diagnostics in v0.7
are incorporated unchanged except for the probe/execution products specified here.
For avoidance of ambiguity, the core interventions are:

| Family | Branch | Intervention and permission                                                    |
|--------|--------|--------------------------------------------------------------------------------|
| H1     | I      | Intact code, correction allowed during recovery                                |
| H1     | A      | Erase k=3,4, exactly 32 symbols; correction allowed                             |
| H1     | N      | Same lesion; corrective code writes prohibited, inference preserved             |
| H1     | M/S    | Same lesion/prohibition; P-only refill to 255 / matched sham at injury boundary |
| H1     | X      | Same lesion; ordinary correction; recovery g=60 rather than 47                  |
| H2     | D/C    | Two obsolete whole blocks / continued usefulness, ordinary correction, g=36    |
| H2     | N      | D with corrective code writes prohibited                                       |
| H2     | M/S    | D plus P-only refill / matched sham after tick 256, before tick 257             |
| H2     | X      | D with ordinary g=66                                                           |
| H2     | FROZEN | D/C from RL parent; Q inference/epsilon/faults retained, learning work omitted  |

No-write never means no query/age/auxiliary writes or zeroed Q. Frozen savings
are reported, not hidden with dummy work. Whole-block U/O is hidden, target-
independent, paired across policies/codes/D/C, and never an extra controller input.
H1 M/S dispatch 255 per source, 1020 material and 1020 external transport energy,
but only M changes worker stock. Their gross handling costs match, not accepted
stock. At supported H1 entry P=242 after ISOLATE: M adds thirteen net; ordinary
g=47 already refills caps. X offers thirteen extra per source on each recovery
tick, not a refund or the same dose as M. Disclose these saturated/null contrasts.

Acquisition: canonical activation E=65535/Pj=255; 256 LESSONs in sixteen grouped
passes, sixteen presentations per cue, g=48, no responses/controller/ADMIT.
BLOCK has 64 scheduled COMMITs, including after a rejected fourth lesson.
Development: live FULL-SOURCE-ENTRY, paid ISOLATE, 2048 ticks at g=66; 2043
admissions at 1-2043, responses at 6-2048, five independent current drain offers.
Learning trunks schedule TERMINAL once. All ordinary live ticks offer 30000 energy.
ISOLATE costs 1120 energy/thirteen material per source. No ordinary support
reactivates a dead historical body; downstream planned failures remain.

Each selected H1 history has an actual 128-tick recovery and actual 261-tick
FINAL, including I. Enter with live FULL-SOURCE-ENTRY, ISOLATE, lesion/no-op,
and control intervention/no-op. Recovery uses g=47 (X 60), frozen learning,
paid controller/RESPONSE, no ADMIT, examples, ecological yield, signed outcome,
or feedback-conditioned timing. Forage/collection opportunities remain 64/eight.
Then full entry, ISOLATE, independent code-only p=0.1 challenge, and FINAL g=28.
FINAL admits 1-256, responds 6-261, sixteen per cue, no controller/correction/Q
update/feedback. Every tick wears; primary R=correct/256, including missing/dead.

PRE is a disposable charged 261-tick no-challenge probe once per H1 trunk before
branch entry. All attached histories reference it; it is not multiplied by six.
The H2 prerequisite is the same probe once per H2 trunk. For SELECTED-CONTROL
RL partial A/N only, take one shared ACUTE from their identical post-lesion state
before the permission difference takes effect, and separate POST clones after
each 128-tick recovery. This prespecified diagnostic covers both codes/all 64
engineering cells. Each probe has its own full entry, paid ISOLATE, g=28, wear,
and 256 raw responses, never returned to its parent. ACUTE equality requires
matching all bytes and probe inputs; a mismatch is an implementation error.
Other branches have no ACUTE/POST obligation. This explicitly narrows protocol
section 6 replication without deleting its temporal diagnostic purpose. Every
FINAL still follows paid transient clearing, so final stored-information evidence
does not depend on an uncharged host decode or persistent inference scratch.

H2 retains 512 ticks, 507 admissions/responses, no lesion/challenge; endpoint
admissions 252-507 produce responses 257-512, exactly 128 U/128 O. O correction
writes use ticks 257-512, including all five drain controller offers. Full-phase
activity/completion and costs are separate from endpoint recall. Outcome-dependent
energy and signed learning packets remain present where v0.5 permits them;
H2 can relearn and is never evidence of example-free H1 recovery. Assigned g=36
is not a demonstrated scarcity theorem; g=36 failure requires version review.

Keep all v0.7 default-only diagnostics: LL13-RESTORE/SHAM, FLIP-A/N, HUB-A/N,
RESOURCE-A/N each contribute twelve H1 histories per cell; G-DIAG contributes
48 ecologies at g={28,32,36,40}, HS-REFERENCE twelve at g=66, MIXED 24 D/C/M/S.
Their lesion/pulse times, hidden hub schedule, mixed-cue assignment, and pairing
stay unchanged. They reference default PRE/prerequisite probes and add no trunks
or ACUTE/POST. LL13's actual FINAL uses g=13 and its tick-129 restore/sham;
other H1 diagnostics retain the standard later challenge. No diagnostic selects
g, a preferred injury, or a replacement final endpoint. These ordinary-policy
diagnostics do not discharge the separate scripted H2 feasibility obligation.

## Mandatory privileged engineering oracle

Select PRIVILEGED-EXACT-TEMPLATE as 2 codes x 8 engineering individuals x panel 1
= 16 conformance cases, not a candidate/family/policy/control Cartesian product.
Use the H1 RL default SCREEN A post-lesion boundary, regardless of damage or
eligibility. Each individual retains its same independent 16-label engineering
table; the two codes are not independent target tables. No final targets are used.
The harness explicitly grants a new diagnostic clone lifecycle and replacement
power even from a dead source; it does not revive or modify that historical parent.
It supplies privileged labels and protected restoration timing, not fair repair.

Begin from that actual arbitrary damaged snapshot; full entry and paid ISOLATE
clear ring/staging/transition. Do not canonicalize Q, metadata, ages, reserve, or
code. Execute sixteen REP templates (cue 0..15, payload its label) or four BLOCK
templates (cue 0,4,8,12, payload its four labels in little-endian order). Each
rewrites five/twenty symbols unconditionally, including already correct cells.
Collectively overwrite all 80 symbols. There is no scan, decoder, old-clean read,
Q/clock restoration, controller selection, or additional repair permission.

Before EACH atomic template, externally replace E/P with 65535/255 and log old
stocks, new stocks, and 1020 material-hop dispatch energy separately from agent
spending. These grants cannot occur within an operation. Templates are a finite
off-clock harness block, with no TICK, ordinary fault, leakage, or upkeep between
them; this protected restoration timing is an explicit diagnostic exception,
not a change to acquisition, recovery, ecology, or final physics. T=0 after
each template except its own S/residue; no future service is secretly omitted.

The new template follows B02's unconditional teaching-prefix convention: outer
M=128, one C=256, S=8, two scalars at X, cue:4 and payload:4 (REP range 0..1).
It receives each scalar once after body admission, with one energy encoding each;
no callback or target key is worker-readable. Body rejection costs M+S=136 and
receives neither scalar. An admitted prefix costs 394+gV+128A+23W energy,
W material entirely at the addressed hub, g=1 REP/6 BLOCK, V=A and W<=A<=n.
Every reached write pays its M gate; first failure stops, preserving the prefix.
After prepaid C, retain S plus remaining generation/gates in L; compare each
WRITE2 with c+L+T+rho at its actual source, rho_E=1. No refunds or borrowed yield.
Full prices are REP 1154 and BLOCK 3534; complete-bank totals are 18464 and
14136. Even without replenishment between templates these totals are below Emax,
and twenty code writes per source are below 255; per-operation grants make the
every-prefix positive proof independent of the source's old resource history.

The following static CONTROL expansion uses existing four arithmetic registers,
micro-PC/address/flags and decoder slots cue:4, payload:4, base:7, expected:2.
Narrow MOV preserves neighbors; gates may clobber arithmetic registers, not these
scratch slots. Code generation is separately charged, never hidden in CONTROL.

1. After M/C: MOV entry micro-PC; MOV flags zero; STAGE inputs; receive the two
   priced scalars into R0/R1; MOV cue from R0; MOV payload from R1.
2. SHR R0 by 2; SHL R2 from R0 by 4; SHL R3 from R0 by 2; ADD R2,R2,R3.
   REP: EX R0,cue; AND R0,3; ADD R2,R2,R0. BLOCK: three charged padding slots.
   MOV base,R2; STAGE first cell. These are fourteen CONTROL instructions total.
3. Unroll each cell: EX R0,payload; paid g generation; MOV expected,R0;
   EX R1,base; ADD lane-address,R1,literal-offset; STAGE write-gate; paid M;
   BR rejected-to-exit; otherwise paid WRITE2 then fall through. Exactly six
   CONTROL per visited cell, no loop counter, W increment, helper call, or retry.
4. Exit: STAGE S; BR S; pay S and clear all scratch, with no later micro-PC write.

REP offsets are 0,4,8,12,16; generation is AND R0,1. BLOCK offsets 0..19 use
columns 1..15,1,2,4,8,15 and the six-step AND/SHR/XOR/SHR/XOR/AND parity kernel.
The expected 00/01 symbol and eleven-bit address survive the gate. Administration
is sixteen instructions, bounded by a reserved sixty; hence 16+6n is 46/136,
and even 60+6(20)=180<=256. Source/shape and L derive from paid cue and unrolled
micro-PC; no acquired ledger/counter survives S. Literal linking, bad-packet traps,
rejected-prefix paths, and independent trace checking remain pre-freeze obligations,
not an implemented conformance pass. No second controller C is applied here.

Immediately after restoration, before any assay or fault, checkpoint and assert
exact code equality to the target encoding at ALL 80 lanes, not merely decoding
accuracy. Assert untouched Q/metadata/ages/reserve and only declared ISOLATE/resource
changes elsewhere. Fork two independent charged 261-tick no-challenge query probes:
one ZERO-FAULT control harness (RAM flips/erasures off, typed leakage/charges and
all query/upkeep services retained), one LIVE-WEAR with ordinary v0.4 faults.
Each receives its own full entry and ISOLATE, g=28, no controller/feedback. The
zero-fault proof predicts 256/256 correct, full coverage/activity/completion,
conditional on conforming services; the live-wear probe has NO 100% accuracy gate.
The latter distinguishes realistic assay erosion from exact restoration failure.
Neither probe supplies a main H1/H2 pass or proves reconstruction without labels.

Required counts: 16 restoration histories, 32 probes, 8352 ticks, 8192 responses,
160 templates, 1280 code writes, 260800 template energy, and 48 paid ISOLATEs.
Audit reset after restoration and after each probe: 48 actual source resets,
mapped to the already selected H1-RL-default canonical reset class below.
No additional continuation or target draw is needed. Oracle input permissions
are revoked before reset. Separately retain the mandatory exhaustive sixteen
four-bit acquisition/reset component cases; those are implementation validation,
not these 16 oracle cases or a new final sample. Final oracle product size is zero
because its required conformance purpose is tested in engineering, not waived.

## Complete reset of every history with canonical futures

For every planned terminal nonnegative phase, perform an actual reset audit on
its archived terminal state, including dead/ineligible states: acquisition and
development; each H1 recovery and FINAL; each actual PRE/prerequisite/ACUTE/POST;
each ecology; and all three oracle phases. Shared probes have one actual source
and explicit branch references. There is no reset after a nonexistent probe and
no recursive resetting of negative phases. This changes v0.7's history catalog,
not the obligation to erase every acquired field of every retained source.

Construct a genuinely new canonical 276-byte body from G: all 80 code symbols
10; all 2048 auxiliary bits zero, including Q, every invalid ring payload/reserved
bit, teaching/transition, metadata, ALL twenty ages, resources, and inaccessible
reserve. Cancel old queues, callbacks, input cursors, messages and reachable
history/scorer/target/checkpoint references. Assert byte equality to canonical
before activation and equality after identical E=65535/Pj=255 activation. Preserve
the original state hash, source lifecycle, reset event, field checks and reference
cancellation result. A blank-initializer-only test does not audit the old history.

Continue one representative per distinct (cohort, individual, panel, code, family,
complete inherited policy/configuration G, reset-input definition). Reset fixes
correction allowed and learning disabled, erases Q, normalizes injury/support
calendars, and maps FROZEN to its underlying RL G. Candidate ID/outcome, parent
history, diagnostic name and target do not select future Z. Different G never
merge merely because outputs agree. Each actual reset must pass byte/reference
checks before its continuation reference is valid. Archive class membership and
the compositional transition/input noninterference proof, not a score comparison.

The conservative fixed roster uses all 400 engineering or 16 final trunk G slots
per cell. If exact G slots coincide, keep logical references but resolve one
representative; actual continued count is the manifest union and at most this
roster. Do not assert fewer paths from saturated cuts: G differs. Required paired
implementation tests execute both trajectories before reuse is trusted. Reset
validation failures stop completion; a saved hash alone proves no independence.

Each representative runs paid ISOLATE, 128 frozen recovery ticks at g=47, full
entry/ISOLATE/challenge, then the actual 261-tick g=28 FINAL. No teaching or task
feedback. Each has 256 planned responses; all linked source histories retain
their own reset check but not another 389-tick continuation. Original dead bodies
remain dead; the new canonical body is explicitly powered, never posthumous repair.
Primary erasure statistics use only the H1-family RL-developed parent mapping,
one per code/individual/panel: final 2 x 32 x 8 = 512, engineering 128 diagnostic
maps. Other reset mappings cannot enlarge n or narrow this interval.

## Randomness, permissions, and exact replay

Incorporate v0.7's complete "Randomness and external input ownership" section:
independent checked CNG 32-byte requests, sixteen low target bits, private separate
purpose roots, RFC 8785 twelve-field tuples, HMAC-SHA-256, uint128 rejection
mapping with 1024-attempt abort, exact hazard thresholds, public conformance and
analysis keys, acquisition grouping, hidden balanced schedules, drain offers,
3160 indexed ordinary-fault scalars per planned tick, and fixed bootstrap tuples.
These are normative algorithms, not new public schedules or empirical independence.
Use version E3-EVAL-0.8. SCREEN, SELECTED-CONTROL, and final CORE are distinct
family namespace suffixes for branch-phase inputs; trunk PRE/prerequisite use
their single TRUNK suffix. Fixed diagnostics retain named namespaces and pairing.
Codes/policies/candidate IDs do not enter paired within-product draw keys.

Reset uses only base H1/H2 plus RESET-RECOVERY/RESET-FINAL, omitting product,
branch, history and outcome suffixes. Individual/panel inputs remain fixed under
counterfactual history/target tests. Oracle ZERO-FAULT/LIVE-WEAR have separate
diagnostic purposes and use engineering labels only through their allowlisted
template packets. Scorer labels never enter ordinary or reset workers. Archive
complete scheduled admissions/offers before execution and consumed-input indices;
unconsumed slots are algorithmically planned, not billions of materialized draws.

No execution deduplication of acquisition/development is selected. The full
400-candidate engineering experience is the baseline bound. Optional byte-identical
archive references require matching complete state, G, input context, lifecycle,
ordered traces, outputs and all charges, checked BEFORE reuse. Equal scores or
equal sensor bins are insufficient; absence of a proof means separate execution.
The selected PRE/reset sharing rules above have their own exact boundary proofs.
Replay uses saved developed/fork states without reacquisition or retraining.

## Sparse checkpoints and complete compact raw records

Replace every-tick full snapshots with full 276-byte snapshots at canonical and
activation boundaries, acquisition/development ends, every actual fork/entry/
ISOLATE/intervention, recovery/probe/FINAL/ecology ends, and actual shutdown.
Additionally anchor ticks 64,128,... and each phase's final tick. A 261-tick phase
has five tick anchors, recovery two, ecology eight, and a trunk 4+32. These are
fixed planned slots even after death: encode dead anchors by exact shutdown-state
references, not invented canonical payloads. Named coincident anchors may alias
bytes but keep their semantic keys. Scratch is zero; no suspended service resumes.

Every actual tick records SHA-256 of its actual full end state (32 raw bytes,
not a hex string or a truncated digest) plus a fixed 16-byte trace capsule. It
is NOT a full checkpoint. Nearest anchor plus immutable G, lifecycle, scheduled
external events, indexed inputs, and deterministic transition traces reconstruct
all intermediate bytes/outputs/debits exactly; verify every recorded digest.

Select this 48-byte tick encoding, with fixed little-endian bitfields:

* One byte: five-bit stop/last outer-service ordinal, two-bit lifecycle, one zero bit
* Four bytes: mode-specific prefix V/A/W (five bits each), action two, TD path two,
  terminal one, DECIDE one, eligibility one, old validity one, source two, new
  store one, offer-consumed one, five reserved zero bits
* Four bytes: due slot eight, decode path three, emitted status/bit two, record
  finalized one, ADMIT two, LESSON two, COMMIT two, TERMINAL two, decoded payload
  four, health two, E/P bins one each, two reserved zero bits
* Four bytes: twenty CONDITION admission bits, two completed AGE bits, ten zero bits
* Three bytes: executed controller C_A/C_B counts nine each, actual outer-service
  count five, one reserved zero bit; noncontroller phases store zero C_A/C_B

Each capsule is a typed union selected by immutable phase/trace ID: acquisition
uses V/A/W for its one code-writing LESSON or COMMIT, never both; query phases
use it for CONTROLLER. Service status codes distinguish absent, rejected,
completed and partial as applicable. The linked finite opcode trace maps these
fields and replayed paid state to each actual service path, primitive counts,
scalar consumption and five-source debit vectors. Record rejected services when
entered, not zero records for all unreachable services after shutdown. Raw scan/
TD internals are reconstructed and exactly checked against per-shard trace digests,
not stored as padded opcode rows. Generate those digests from ORIGINAL executed
service paths/debits/scalars, not from replay alone. Full ledger views expand exactly.
Capsule sufficiency for every corrupt/rejected path is a B07 proof/test obligation;
unrepresentable paths stop validation, never overflow, truncate, or silently omit work.

Raw due responses are complete within every selected history: eight bytes per
row for actual cue, emission/status, raw due slot, scoring flags, signed-return
int16, physical yield uint8, and presence/guess/survival flags. Planned cue/target,
tick, slot and service/ledger keys derive from immutable schedules, private target
table, and shard range, not worker access. Feedback absence differs from a zero
packet. Preserve all spurious emissions in their actual tick capsule with no score.
Teaching uses eight bytes per planned lesson and COMMIT four; all missed/dead
opportunities stay. Phase summaries up to 512 bytes preserve exact costs/status;
their projections never substitute for raw response or trace records.

Dead suffixes may use lossless run-length ranges with first/last planned key,
actual shutdown payload/hash, absence/failure statuses, counts and checksums.
Expansion must reproduce every planned tick, response, lesson, COMMIT and anchor,
including per-query scorer fields and reasons. Derive missing services from the
immutable tick order and stop ordinal, not an unexplained hole. The fatal tick
retains a response emitted before its last fault even if its activity is zero.
No technical exception may become biological death; PARTIAL records missing keys.

Use non-pickle packed binary shards and canonical-JSON context, with full worker/
scorer separation. Boundary indices use 32 bytes plus each 276-byte payload;
reset audit records use 64 bytes plus their two canonical/activation snapshots.
Context contains source/config/schema/trace hashes, all fixed maps/parameters,
life status, pending external events, lineage and namespace resolution, private
input provenance, schedules and encoding dictionaries. Hash each immutable shard.
Inherit v0.7's exclusive-new-directory STARTED/COMPLETE/FAILED/PARTIAL lifecycle,
unchanged start manifest, separate end manifest, restricted roots, exact replay,
and new destinations for reanalysis. Scientific failure is not technical failure.

## Exact logical counts and conservative physical bounds

Let T=trunks, H=two-phase H1 histories, P=PRE, J=H2 prerequisite, D=extra
ACUTE/POST probes, K=ecologies, R=canonical reset roster, A=mid-phase pulse
boundaries. Upper bounds do not depend on the identity of future winners.

$$
N=2T+2H+P+J+D+K,\quad U=N+2R,
$$
$$
L=2304T+389H+261(P+J+D)+512K+389R,
$$
$$
F=2043T+256(H+P+J+D+R)+507K.
$$

N is actual source-history reset checks; U is phase summary rows. F/L count
planned responses/ticks including dead suffix expansion and logical reset slots.
The full checkpoint scheduled-slot count is

$$
B=41T+15H+8(P+J+D)+12K+13R+2N+A,\quad B_{\max}=B+U.
$$

Coefficients include tick anchors plus named boundaries: trunk 36+5; H1 7+8;
probe 5+3; ecology 8+4; reset continuation 7+6. Each source audit separately
adds fresh canonical and activated snapshots (2N). The six reset-continuation
boundaries are activated start reference, recovery ISOLATE, recovered anchor,
FINAL full entry, ISOLATE, challenge. Allow one extra shutdown snapshot per
timed phase, at most U; coincident death/anchors need not duplicate payloads.
Thus B is an exact logical schedule, Bmax a fixed row maximum, not an observed
death count. Pre-dead phases keep scheduled anchor references but add no shutdown.

| Quantity                        | Final per cell | Engineering per cell | Final total | Engineering total |
|---------------------------------|----------------|----------------------|-------------|-------------------|
| T                               | 16             | 400                  | 4096        | 25600             |
| H                               | 48             | 400+48+48=496        | 12288       | 31744             |
| P / J                           | 8 / 8          | 200 / 200            | 2048 / 2048 | 12800 / 12800     |
| D                               | 0              | 6                    | 0           | 384               |
| K                               | 52             | 400+52+84=536        | 13312       | 34304             |
| R maximum roster                | 16             | 400                  | 4096        | 25600             |
| A                               | 16             | 16+12+12=40          | 4096        | 2560              |
| N reset audits                  |                |                      | 50176       | 174976            |
| U phase summaries               |                |                      | 58368       | 226176            |
| Teaching rows                   |                |                      | 1048576     | 6553600           |
| BLOCK COMMIT rows               |                |                      | 131072      | 819200            |
| F due responses                 |                |                      | 20360192    | 91024896          |
| L ticks                         |                |                      | 23695360    | 105634688         |
| B scheduled snapshot slots      |                |                      | 702464      | 2830592           |
| Extra shutdown maximum U        |                |                      | 58368       | 226176            |
| Bmax snapshot rows              |                |                      | 760832      | 3056768           |
| 276 Bmax payload bytes          |                |                      | 209989632   | 843667968         |

Multipliers are 256 final cells and 64 engineering cells. Add the oracle once,
not per cell: N/U +48/+48, L/F +8352/+8192. Its scheduled snapshots are 736,
plus at most 32 assay shutdowns =768: per case 26+2n scheduled (raw/entry/ISOLATE,
two per template, exact-code anchor, sixteen probe boundaries/anchors, six reset
snapshots), plus two shutdowns. n=16 REP/4 BLOCK. Oracle negative continuations
already reference R. Combined maxima: 129338400 ticks, 111393280 responses,
3818368 snapshot rows, 225200 reset audits, and 284592 phase summaries.

No unavailable winner map is assumed. At run start archive the prospective
candidate and selected-slot catalog; after selection append immutable bindings
and resolved reset equivalence classes. Logical roster totals above stay fixed.
Actual executed ticks/services depend on death, admitted paths, and proven shared
references; actual counts are sums over the resolved union, never forecasts of
winning G equality. No index rows for unselected candidate controls are invented.

For independent service-count checking, ISOLATE slots are
I=T+2H+P+J+D+K+2R: final 54272, engineering 200576, plus oracle 48.
Controller offers C=2048T+128(H+R)+512K: 17301504/77332480; total v0.6 extra
energy <=24226299904, charged only when funded. Learning trunks are 2048/2560
and learning ecologies 6144/5888. Outer-service planned slot formula is

$$
S=6144T+64T_{BLOCK}+51200T+2043T+T_L
+3200(H+R)+6520(H+P+J+D+R)+12800K+507K+K_L+I.
$$

S is 606543872 final and 2704618112 engineering; add oracle 208848, total
3311370832. These are derivable slots, NOT physical per-service log rows.
Ordinary scalar-slot maxima 3160L are 74877337600/333805614080 plus oracle
13196160 for its sixteen LIVE-WEAR probes; ZERO-FAULT has no random fault draws.
Primary/reset challenge slots are 1310720/4587520, plus 61440 engineering FLIP
slots. No oracle challenge. Unconsumed scalar slots need no separate storage.

### Archive byte envelope and reduction

Use fixed uncompressed record ceilings, no assumed favorable compression, death,
candidate aliasing, or exact-score deduplication. Selected core archive ceilings:

| Component                            | Bytes      |
|--------------------------------------|------------|
| 48 bytes x planned ticks              | 6208243200 |
| Eight bytes x raw responses           | 891146240  |
| 308 bytes x maximum snapshots         | 1176057344 |
| 64 bytes x reset audit records        | 14412800   |
| 512 bytes x phase summaries           | 145711104  |
| Eight bytes x teaching rows           | 60817408   |
| Four bytes x COMMIT rows              | 3801088    |
| 64 bytes x oracle template events     | 10240      |
| Shared contexts/dictionaries/manifests | 67108864   |
| Total selected packed archive ceiling| 8567308288 |

This is 8.567 GB (7.979 GiB), conditional on validated capsule/context schemas,
not measured disk usage or a universal storage limit. Count bounded packed schedules
once per shared input definition; text views expand rather than duplicate them.
The 64 MiB context allowance requires a pre-execution byte/layout check, not an
assumption that arbitrary JSON per history fits. Expanded debugging views,
replicated backups and later implementation conformance fixtures are separately
budgeted, not silently included. A schema overflow blocks validation; version the
encoding rather than remove observations. Raw SHA-256 values alone require
4138828800 bytes at this tick bound: claiming only hundreds of MB would be wrong.

Against v0.7's combined logical products, ticks are 27.1407%, responses 30.0716%,
and maximum full snapshots 0.7893%. Snapshot payload becomes 1053869568 bytes
versus 133526697984, a 99.2107% reduction. Final/engineering response counts are
40.7347%/28.4058% of their old counts. Logical service slots fall from 12014094592
to 3311370832, while no per-unexecuted-service records are stored. These ratios
compare different prospectively selected workloads, not observed speedups or
lossless removal of v0.7 experiments. The 32 individuals/eight primary panels remain.

## Statistical decisions and outstanding gates

Retain all v0.7 estimands/gates and complete per-individual vectors: mean of eight
panels, then equal mean of 32 individuals; 10000 paired individual bootstraps,
same indices across contrasts, order statistics 250/9750 without interpolation.
Use ratio of aggregate means for H2, retaining zero-reference individuals;
aggregate zero comparator makes the ratio undefined and gate unable to pass.
No survivor/complete-case filtering, response-level bootstrap, or engineering
selection data enters final confidence intervals. Report BLOCK separately regardless
of REP success; DRIVE/oracle cannot satisfy a fair-objective advantage gate.

| Gate                | Unchanged requirement                                                        |
|---------------------|------------------------------------------------------------------------------|
| INFO / STRUCT       | Exact interfaces, ledgers, all-state reset and compositional noninterference  |
| PREREQ              | Intact >=0.90; acquisition and development activity each >=0.95               |
| H1-MAINT            | REP RL A minus N >=0.05, paired lower CI >0; at least one reconstruction write|
| H1-FUNC             | REP RL A R>=0.80 and FINAL activity >=0.90                                    |
| H1-ADAPT            | REP RL A minus H1 tuned PERIODIC A >=0.05, paired lower CI >0                 |
| H2-SELECT           | REP RL D O writes >=50% below C, absolute reduction lower CI >0               |
| H2-PERIODIC         | REP RL D O writes >=10% below H2 tuned PERIODIC D, reduction lower CI >0      |
| H2-VIABLE           | REP RL D R_U>=0.80, whole-phase activity/completion each >=0.90               |
| H2-RETAIN           | Upper paired CI for C R_U minus D R_U <=0.05                                  |
| ERASURE-ACCURACY    | Primary forced-choice CI contained in [0.45,0.55]; coverage/activity >=0.95   |

H1 prerequisite is intact I FINAL; H2 prerequisite is its developed intact probe.
Do not invent a final H1 completion gate from engineering feasibility. Active
means funded TICK and E>0 after its fault, not successful decoding/controller.
Report reset planned-denominator R, emitted accuracy, coverage, activity and
completion. Each panel's forced-choice ratio is averaged within individual;
zero emission in any panel makes that individual's statistic undefined and the
containment decision inconclusive, not a reason to omit it. Primary reset mapping
is fixed before results; other reset histories provide structural coverage only.

Panel-specific development remains the estimand. With d_ip a paired contrast
and D_i=(sum_p d_ip)/8, Var(mean_i D_i)=Var(D_i)/32, where Var(D_i) includes all
64 panel covariance terms divided by 64. Shared target-table variability does
not vanish with eight panels. B06 must audit conditional independence assumptions,
paired noise, missingness, and the full output law; canonical erasure alone does
not imply independent repeated guesses or empirical chance accuracy.

Before the design-only freeze require independent review of this revision,
B06-H1 financial versus functional/headroom analysis for both five-point gates,
B06-H2 sourcewise every-prefix scarcity/opportunity costs and a bounded SCRIPTED
H2 feasibility witness (not ordinary G-DIAG/HS-REFERENCE), and B06-PRECISION for
32 x 8 including >=0.80 prospective erasure-containment assurance with its guard.
No B06 proof, precision calculation, or empirical test pass is claimed here.

B07 must verify all linked service/ROM traces, oracle trace/prefix/zero-fault
positive proof, protected-law labels, exact input permissions, all-byte resets
and event cancellation, sparse replay/capsule sufficiency, and count/byte ceilings.
Specify reduced exhaustive sixteen-table acquisition/reset tests, sixteen
production bit-change tests, cross-block/populated/corrupt/dead histories, ledger
and prefix failures, oracle exact-code and live-wear separation, and exact replay.
These tests are UNIMPLEMENTED; define them before first freeze, execute them only
after authorized implementation, then require their passes before engineering.

After engineering require the mandatory 16-case oracle and full selected-control
coverage, resolve/freeze configurations and manifests, and complete scripted H2
validation before final seeds. Freeze source/configuration/tests/analysis/archive
schemas before independently drawing final target tables or roots. Neither freeze
has occurred. A scientific gate may fail in a technically valid experiment;
no control success authorizes retuning or a claim of task completion.
