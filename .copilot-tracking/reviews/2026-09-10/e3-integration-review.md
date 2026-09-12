---
title: Independent E3 integration design acceptance
description: Final static review of the v0.11 integration, IFR1 catalogs, and IFR2 scientific boundary
ms.date: 2026-09-10
status: Complete - accept engineering-only design snapshot; current finals prohibited
---

## Decision

ACCEPT the integrated engineering-only design for its prospective design snapshot.
No concrete remaining design blocker was found in this integration scope.
IFR1 is closed by v0.11's additive catalogs; IFR2 is closed by its scientific
restriction, not by proving the stronger H2 premise. IFR3 remains a later
implementation-validation gate. Neither freeze nor any execution is certified.
Current confirmatory H2, the full final experiment and fresh final draws remain
NO-GO even if every script subsequently passes.

## Scope and evidence

Read E3_INTEGRATION_DECISION_v0_11.md, E3_CONFORMANCE_CONTRACT_v0_10.md,
E3_INTERFACE_CONTRACT_v0_9.md and E3_EVALUATION_CONTRACT_v0_8.md in full;
cross-checked IFR1/IFR2 and the complete arithmetic table in
.copilot-tracking/reviews/2026-09-10/e3-interface-review.md,
also read in full. Read control v0.6, CT review and the ordinary ROM closure;
consulted the service note's typed-ROM/disposition sections, B06 review through
the financial counterexample, protocol freeze rules, current plan, and original
mission statements in NEW_AGENT_GUIDE.md and RESEARCH_NOTEBOOK.md.

This is an independent static integration review, not a new instruction-by-instruction
audit of every unchanged witness or a rerun of B06 probability calculations.
Only this requested review is written. Other sources, historical reviews, root
documents and the plan are read-only here. No code, command, runtime, target/root
draw, generator, bootstrap, hash computation or freeze manifest was produced.
Earlier reviewers' hash checks are historical evidence, not newly verified hashes.

## IFR1 catalog and ledger closure

V0.11 has explicit precedence for this extension and stage eligibility. The old
v0.9/v0.10-only incompatibility remains correctly recorded in IFR1; it does not
persist when the new normative extension is included. All intervals below are
half-open and append after the original maximum without renumbering core keys.

| Catalog               | New interval          | Added  | Combined maximum |
|-----------------------|-----------------------|--------|------------------|
| Phase and summary     | [284592,285616)        | 1024   | 285616           |
| Canonical reset class | [29696,29952)          | 256    | 29952            |
| Tick                  | [129338400,129700128)  | 361728 | 129700128        |
| Response              | [111393280,111718400)  | 325120 | 111718400        |
| Maximum snapshot      | [3818368,3829888)      | 11520  | 3829888          |
| Source reset audit    | [225200,225712)        | 512    | 225712           |

The product is 2 codes x 8 individuals x 8 panels x 2 scripts x 2 budgets = 512
ecologies. Reset sharing removes budget only after 512 distinct actual-source
audits, leaving 256 script-G futures. Delta ticks = $512(512)+389(256)=361728$;
responses = $507(512)+256(256)=325120$; summaries = $512+2(256)=1024$.
Scheduled snapshots = $12(512)+13(256)+2(512)=10496$; add at most 1024
shutdowns for 11520. Unused shutdown slots are absent, not fabricated live states.

| Other logical quantity   | Core         | Delta      | Combined     |
|--------------------------|--------------|------------|--------------|
| Trunk roster             | 29696        | 0          | 29696        |
| Paid ISOLATE slots       | 254896       | 1024       | 255920       |
| Offered controllers      | 94633984     | 294912     | 94928896     |
| Planned outer services   | 3311370832   | 9303040    | 3320673872   |
| Ordinary fault slots     | 408696147840 | 1143060480 | 409839208320 |
| Primary/reset challenges | 5898240      | 20480      | 5918720      |
| With existing FLIP       | 5959680      | 20480      | 5980160      |
| Teaching rows            | 7602176      | 0          | 7602176      |
| BLOCK COMMIT slots       | 950272       | 0          | 950272       |
| Privileged templates     | 160          | 0          | 160          |

Controller delta = $512(512)+128(256)$. Service delta =
$12800(512)+507(512)+512+(3200+6520)(256)+1024=9303040$.
Fault delta = $3160(361728)$; challenge delta = $80(256)$.
ZERO-FAULT remains excluded from ordinary fault draws.
Both prepaid controller budgets remain 256 energy each: added ceiling 75497472
per C, 150994944 together; combined 24301797376 per C, 48603594752 together.
These follow from offered controllers, not an assertion of funded/realized work.
The inherited loose aggregate bound, updated for ticks/boundaries, is
$15597142635599251520<2^{64}$; checked uint64 aggregation remains mandatory.

### Complete dense byte ledger

| Component            | Core bytes | Added bytes | Combined bytes |
|----------------------|------------|-------------|----------------|
| Ticks, 48 each        | 6208243200 | 17362944    | 6225606144     |
| Responses, 8 each     | 891146240  | 2600960     | 893747200      |
| Snapshots, 308 each   | 1176057344 | 3548160     | 1179605504     |
| Reset audits, 64 each | 14412800   | 32768       | 14445568       |
| Summaries, 512 each   | 145711104  | 524288      | 146235392      |
| Lessons, 8 each       | 60817408   | 0           | 60817408       |
| COMMITs, 4 each       | 3801088    | 0           | 3801088        |
| Templates, 64 each    | 10240      | 0           | 10240          |
| Context              | 67108864   | 4194304     | 71303168       |
| Total                | 8567308288 | 28263424    | 8595571712     |

Record-only delta is 24069120. Extension context sums exactly:
2097152 ROM + 83968 schedules + 65536 descriptors + 49152 commitments + 8192
class maps + 512 G bytes + 1048576 metadata/directories + 841216 spare = 4194304.
These fund 64 schedules, 1024 descriptors/commitments/summaries, 256 class rows
and four G records. Total is 8.595571712 GB, not a strict 8.5-GB ceiling or measured
disk/runtime demand. No compression, death or favorable aliasing is needed.
Fixtures, expanded traces, replay copies and backups need separate budgets.

### Widths, dictionaries and identity boundaries

* Product SCRIPTED=13 and policies SCRIPT-U/ALL=5/6 fit inherited u8 fields. Family stays H2 (1). Schedule namespace/slot34 is external, never worker family34 or an added scalar/header field; workers still receive ecology phase4.
* G=$400+2\,code+script$ gives 400..403, within the existing 512-entry G catalog. Policies5/6, objective0 and public script specializations are explicit. No G identifies an individual, outcome or winner; no fourth live code selector exists.
* The 64 schedules use reserved slot34 within20480, not extra cells or targets; slots35..63 remain unused. Phase/class/snapshot limits supersede284592/29696/3818368, not trunk29696. The number512 is the summary byte width and G capacity, not an old 512-phase limit.
* Phase/reference/first-row u32 values fit combined row ranges; schedule/G u16 and namespace u8/u16 fit their IDs. All-ones absence stays invalid as a real reference. Directory first_row/count/offset/length and aggregate counters remain checked uint64; archive offsets cannot be stock-sized or u32. Canonical JSON uint64 values remain decimal strings.
* Original72-byte directories retain table IDs0..13, codecs0..2 and global ordinals across shards. Extension ID1 belongs to external versioned manifest/binding context, not the four reserved zero bytes or worker frames. New semantic keys/ranges are explicit; unknown enums/keys still reject.
* Retain v0.9 core caps: 1024 finalized shards, metadata925696 within1048576, dictionary65536 maps + 786432 operand bytes + 196608 recipes =1048576, at most65536 twelve-byte descriptors. Extension metadata has its separate1048576 allocation. Neither allowance enlarges descriptor widths, releases reserved bits, or permits per-history objects/hidden dictionaries.
* Capsule groups remain8+32+32+32+16+8=128 bits; summary $16+62(8)=512$ bytes, response8, snapshot32+276=308, audit64, original event192 and commitment48. New outcome fields belong to the external gate catalog, not these records. PASS/FAIL/UNEVALUABLE/TECHNICAL-FAILURE, original traces, core/extension planned and actual counts remain distinct; overflow/missing rows block COMPLETE.

## Static machine acceptance and unchanged precision

Accept the adopted complete symbolic machine at its reviewed abstract level:
CT repairs, ordinary service/ROM witnesses, v0.10 oracle and script amendments.
Fixed-slot MOV, METER128, SENSE16, ATTEMPT16, TICK PASSIVE and paid admission
dispatch remain selected primitives, not undocumented native-code algorithms.
No lowered host-microinstruction proof or positive run is claimed or needed now.
S terminates after clearing; W increment is 2^27; both C budgets are prepaid;
scratch stays32 bytes and persistent state276, with no helper bank or host PC.

Ordinary co-resident endpoint37536 gains TEMPLATE intervals [37536,38048) and
[38048,38560); highest reserved address38559 fits PC16. Oracle demand36254 fits.
SCRIPTSEL replaces E, not an appended override: 12 instructions plus STAGE and
270 paid kernel MOVs, with no leftover rank packets. Script demand5021 fits
[4800,14400), replacing fixed/DRIVE regions; whole-image bound31799 fits38560.
These are unchanged reviewed static witnesses, not emitted or executed images.

Final design n=32 and eight panels per individual are unchanged, although final
execution is prohibited. Scripts use existing engineering tables/trunks only.
Keep the primary H1-RL-developed erasure subset, equal panel/individual weighting,
planned denominators, undefined zero comparators and fixed paired bootstrap.
No script reset, repeated audit or alias adds a target or independent primary vote.
The combined roster reserves capacity, not permission for finals; engineering-stage
manifests declare their own planned subset without instantiating final secrets/rows.

## IFR2 scientific boundary

The statement actually supported is financial: fixed/frozen REP uses at most
28+5=33 material per busiest source, including full conditioning, and 33<=36.
Under the reviewed eligible-start funding induction this is a counterexample
to universal budget-forced abandonment. It proves neither accurate all-region
retention nor failure of every numerical H2 hypothesis. Unqualified "H2 refuted"
would overstate the evidence; v0.11 correctly says universal financial interpretation.

SCRIPT-U success/ALL failure cannot prove optimality or exclude conventional
all-region retention. V0.11 overrides any earlier apparent promotion route:
even a script pass cannot authorize current confirmatory H2 or final draws.
Keep all512 cases, invalid/dead parents, high-support/low-U failures, zero
comparators, inactivity-only ALL failure and both-scripts-retain outcomes.
Technical failure is not biological death; technically valid scientific failure
is COMPLETE with failed gates. No retuning g, weakening rivals or deleting failures.

The qualified 0.996306 assurance and clean-reference adaptive bound about0.0164
remain conditional reviewed mathematics, not observed passes or universal no-go
theorems. AN-001/AN-002 and POL-001..003 are explicitly retained. A positive
hypothesis result is not required before the first freeze of a falsifiable design.
Conformance precedes interpretation; future confirmatory scope requires separate
prospective independent review, not script success or a renamed negative result.

## Snapshot status and remaining work

This acceptance is not the design hash manifest. None was created here; the
inspected root and filename search show E1/E2 freezes only, not an E3 freeze.
The current plan still records historical20%/pending phases, so v0.11's claim
that it records current progress is not yet realized. This is a nonblocking
tracking synchronization item, not evidence of a completed snapshot or execution.

* [ ] Owner records acceptance in current tracking/root status and creates/verifies the new design-only hash manifest before implementation; preserve historical bytes.
* [ ] After that gate, implement under existing user authorization; no additional routine permission is required. This review itself authorizes no runtime action.
* [ ] Validate codecs/ROM/budgets/prefixes, malformed packets, actual process access, complete-state cancellation, paired resets and original-trace replay; measure bounded resources before full engineering allocation.
* [ ] Then run authorized engineering controls, retaining failures. Current finals remain prohibited; any revised final scope also needs the separate second freeze.

No additional original-scope research or factual user clarification is required.
The original aim remains organization-derived priorities and a continuing
artificial individual, not conventional ECC relabeled life or consciousness.
Neither success nor failure here resolves subjectivity, completes that goal,
or exhausts all possible research. No such promise is part of acceptance.