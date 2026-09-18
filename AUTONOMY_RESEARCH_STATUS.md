# Active autonomy research status

Updated 2026-09-18 after AC92. The internal-state milestone
(AC86-89) is ACCEPTED: internally stored controller information is maintained, reconstructed, and
repeatedly transferred to successor storage, with vulnerable coordination state, through the tested
environmental challenge. Full autopoiesis remains UNESTABLISHED — `CLOSURE_BOUNDARY_v2.md`'s
declaration that the succession mechanism is "substrate" is a modeling choice, not a settled finding
(the review left it unresolved). AC91 established that W production is necessary for continued organism viability and sustained
W-dependent maintenance capacity; early release of the production block permits endogenous recovery,
late release after W extinction does not. AC92 closed the functional-interruption gap: on a MATURE
organism, cutting W production so W depletes to 0 just before the reconstruction challenge
(first_W_empty 8176–8178) makes the
reconstruction fail WHILE ALIVE (program stays corrupted, `window_reg_writes == 0`), and a
machinery-only restoration of W (labeled EXTERNAL) makes it resume and complete — with the
W-dependent content writes shown to stop and resume with W while the coordinator transition write
(`write_ctrl`) is not gated by W.

## Current evidence and open requirements

| Requirement | Authoritative evidence/status |
| --- | --- |
| Acquired controller information drives and receives paid maintenance | AC1_RESULTS_AND_NEXT_STEP.md; original and 32-new-seed follow-up; AC1_AUDIT_v1.json |
| Produced, decaying repair constituents enable controller repair | AC2_RESULTS_v1.md; positive at two rates, third rate fails robustness; AC2_AUDIT_v1.json |
| Dependence not explained solely by common resource starvation | AC2 clamped-information contrast and catalyst rescue; bounded evidence |
| Complete-state erasure removes history-dependent recovery | AC1–AC4 tests at their exact declared state boundaries; not a proof for future added state |
| Produced energy-conversion machinery | AC3_RESULTS_v1.md; all three engineering configurations pass; AC3_AUDIT_v1.json |
| Internally produced spatial boundary with measured transport effects | AC4_RESULTS_v1.md: paid B production, W/C transport loss under ablation, B and retention rescues; bounded engineering evidence |
| Controller repair enables sustained activity in integrated architecture | AC4_FOLLOWUP_RESULTS_v1.md: all self complete8192 ticks, all no-policy-write terminate, eight new seeds at two rates |
| Every constituent dependency isolated in the integrated architecture | AC10_RESULTS_V1.md: W, C and B production ablations plus retention and both rescue substitutions in the AC9 body; all nine prespecified gates pass; enclosure retention substitutes for enclosure matter |
| New maintenance dependencies acquired autonomously | NOT ESTABLISHED in AC1–AC4; their policies are demonstrated. AC11 attempted it and was falsified by its own pre-run controls (AC11_DESIGN_CONTROLS_v2.md): a state-blind fixed duty cycle matches or beats every adaptive configuration, and relinquishment is not viable in that regime |
| Developmental allocation creates a local functional-maintenance requirement | AC9_PRIORITY_RESULTS_v2.md:8/8 retain42 allocated sites; occupied-region interruption loses entries, unoccupied interruption preserves them; broader controls missing |
| Unknown resource access acquired without route demonstrations | AC7_RESULTS_v1.md:8/8 correct acquired routes, targeted erasure causes failure in6/6 changed-mapping cases; random ports also viable |
| Reacquisition without a new route teacher | AC8_RESULTS_v1.md:8/8 remap_live reacquire by ticks4104–4157 and complete; frozen0/8 |
| Maintenance of acquired selector fields isolated from inherited action types | AC8_PARTITION_RESULTS_v1.md: keep8/8 versus selector-repair-block2/8,26.01pp activity contrast; narrow representation-dependent result |
| Viable relinquishment in the same maintained architecture | AC6 fixed rates1/1024 and1/2048 pass local revision/reacquisition gates; no net material saving; whole-boundary AC5 fails; AC6_FIXEDRATE_RESULTS_v1.md |
| Rich individual development and general learned organization | NOT ESTABLISHED; demonstrated policy family has only24 permutations |
| Independent review and new confirmatory protocol | DONE for AC1–AC4 (confirmatory v1, fresh seeds 5100–5507): AC1, AC2, AC4 transport and AC4 long-horizon repair dependence confirm at every declared rate; AC3 confirms at 2/3 rates with one self death at the highest rate (7/8) recorded, not amended — `AC1_4_CONFIRMATION_RESULTS_v1.md`. External peer review remains open |
| Full organismal autonomy/autopoiesis or subjectivity | NOT ESTABLISHED |

## Next action

AC92 closed the functional-interruption gap AC91 left open: on a MATURE organism, cutting W production
so W depletes to 0 just before the reconstruction challenge (first_W_empty 8176–8178; t=8192) makes the reconstruction fail WHILE ALIVE
(`window_reg_writes == 0`, `fw == 7-8` at t=8239, content intact at death), and a machinery-only
restoration of W (life re-seed, labeled EXTERNAL) makes it resume (`fw == 0`) and the organism survive.
The W-dependent content writes stop and resume with W; the coordinator transition write `write_ctrl` is
not gated by W (pinned at the single-step level). `AC92_RESULTS_v1.md`; seeds 4300-4303, all six gates.

Two scope notes remain, stated plainly: (1) the SUCCESSION function was not observed mid-cycle — no
succession overlapped the 48-tick window, so the "copying stops while the coordinator keeps changing
phase" split is established by unit tests (content writes stop with W == 0, `write_ctrl` does not), not
as a live mid-copy stall; (2) the coordinator mechanism (`advance()`) remains supplied format-level
machinery, and whether it is "reactions enacted by produced components" or an "always-available
coordinator needing only payable resources" is still the unresolved modeling judgment, not a measurement
this line settles. The production-dependencies phase (AC91 + AC92) is now closed: W production is
necessary for viability and W-dependent maintenance capacity (AC91), and the loss/recovery of the
reconstruction function is isolated and observed while alive (AC92).

Frozen experiments prohibit retroactively changing the old experiment, not changing the next
architecture. Do not resume the stopped E3 v0.11 final experiment.

## Recent turn classification

**AC92 FROZE and its claim PASSES — all six gates** (`AC92_PROTOCOL_v1.md` hashed before the run;
`AC92_RESULTS_v1.md`; seeds 4300-4303 × 2 histories, 96 rows, 16,384 ticks, no route move). The
question: AC91 left open the functional-interruption gap — it blocked W from t=0, so the blocked
organisms died at 248-254 BEFORE succession or the reconstruction challenge, and their `fw=8` was
post-mortem, not an observed failure while alive. AC92 interrupts W availability while the
reconstruction function is UNDERWAY, on a MATURE organism. The interruption is the same W-birth
production gate, but timed: block from `BLOCK_TICK = CORRUPT_TICK − 63` (t=8129), so W depletes
naturally to 0 at 8176–8178, just before the 8-bit corruption (t=8192). Three matched conditions (same content and
resources, identical trajectories until t=8129): `intact` (baseline, byte-identical to AC91
`succession`), `W_block` (cut forever), `W_rescue` (cut, then at t=8240 a MACHINERY-ONLY rescue —
life[:4] re-seeded to the frozen endowment, labeled EXTERNAL, no description/program/pointer/
coordinator state touched). **Result: `intact` reconstructs 8/8 (initial repair fw 8→2→0 in ~2 ticks;
seed 4303's two histories re-corrupt to fw=2 at t=8239 under ongoing damage, then re-repair to 0 — three
phases, final recovery 8/8, not "correct thereafter"); `W_block`
stalls while alive — alive at t=8192 AND t=8239 with `fw == 7-8` and `window_reg_writes == 0` (the
reconstruction never ran), then dies 8410-8414 with the content INTACT (desc 130/130 at death); `W_rescue`
was stalled (`W_pre == 0`, `fw == 7-8`) then resumes after the rescue (`fw == 0`) and survives 8/8. The
W-dependent / W-independent split is shown two ways: at the organism level (content writes = 0 in the
window, reconstruction stalls/resumes with W) and at the single-step level (unit tests: with W == 0,
`write_toward_slot`/`write_pointer`/`reg_from_active`/`reg_description_active`/`reg_pointer`/`reg_ctrl`
all write 0, while `write_ctrl` writes its mode transition on energy+material alone — NOT gated by W).**
Nuance reported, not gated: `fw_pre_rescue` is 7-8 rather than a uniform 8, because the two corrupted
bits of rule 0 whose acquired value is 1 self-repair under the sticky `|=` damage stream (AC67/AC71);
the load-bearing pair is `window_reg_writes == 0` AND `fw_pre_rescue > 0`, not `fw_pre_rescue == 8`. The
death in `W_block` is the same AC13 attention-hijack relocated to the mature organism (fuel 20-27 at
death, not full — the mature economy differs from AC91's t=0 block). Verification: audit passes (96 rows,
14 hashes no drift, arm invariants, W-dependence contrast, generic-decode link, gates recomputed without
simulating), replay **6/6 exact**, 16 AC92 tests (gate no-op for `intact`, blocks bank-0 from block_tick,
writes no content; restore_W touches only life/pos; W-dependence of content writes vs W-independence of
`write_ctrl`; categorical gate shapes; recorded freeze), full 174-test suite green (56 core + 118 AC79-92).
Equivalence: **64/64 rows byte-identical to frozen AC91** (`intact` ≡ `succession`, `W_block(block_tick=0)`
≡ `no_W`). **Boundary unchanged:** full autopoiesis is still not claimed — `advance()` and `prog.choose`
remain supplied format-level machinery, the rescue is EXTERNAL (AC91 established endogenous production
separately), and the succession function was not observed mid-cycle (no succession overlapped the window;
the split is pinned by unit tests). No content self-production (AC78).

**AC91 FROZE and its claim PASSES — all seven gates** (`AC91_PROTOCOL_v1.md` hashed before the run;
`AC91_RESULTS_v1.md`; seeds 4200-4203 × 2 histories, 224 rows, 16,384 ticks, no route move). The
question: can the organization replace the finite-lived components enabling reconstruction and
coordination, while their loss removes those functions and their endogenous replacement restores
them? The produced, finite-lived component is the **W repair catalyst** (4 slots, lifetime 64,
autocatalytic), whose per-action write cap `min(32, 8·W)` gates the W-catalyzed content writes (NOT the
coordinator transition write `write_ctrl`, which runs on energy+material alone). The intervention is a W-birth gate (bank 0 only, content
never touched). **Result: `no_W` blocks W production → W depletes at t=63, reconstruction/maintenance
writes stop (7-10 vs 2276-2474), and all 8 die at 248-254 with the controller information INTACT
(desc 130/130 at death) — the loss removes the machinery and the functions, not the content;
`W_restore` (block [0,50] then un-block) drops W to 1, recovers endogenously, and all 8 reconstruct
(fw=0) and survive with desc 130/130 — restoration supplies no content by construction;
`W_restore_late` (un-block at t=100, after W died at 63) is byte-identical to `no_W` — W-birth needs
a live parent, so the replacement must occur before autocatalytic death; ordinary operation produces
766 W birth events ≈ 192 four-slot complements while desc 130/130 and fw=0 persist. The death in `no_W` is the
AC13 attention-hijack (obs bit 6 stuck → blocked W-birth preempts C-birth → C dies → energy drains,
fuel still full at death). `repair` (succession off) survives 8/8 — replacement is a capability, not
a necessity. Controls: `unmaintained` and `no_repair` die 8/8.** Verification: audit passes (224
rows, 14 hashes no drift, W-birth-gate no-op + content-vs-machinery contrast, gates recomputed
without simulating), replay **6/6 exact**, 15 AC91 tests (gate blocks exactly bank 0 and writes no
content; W-birth autocatalytic; categorical gate shapes; recorded freeze), full 158-test suite green.
Equivalence: **256/256 rows byte-identical to frozen AC89** on the four shared arms. **Boundary
unchanged:** full autopoiesis is still not claimed — `advance()` and `prog.choose` remain supplied
format-level machinery; what is now shown produced-and-replaced is the W catalyst that executes the
supplied machine's writes. No content self-production (AC78). **Timing caveat:** the blocked organisms
die at 248-254, before succession (t=2400) or reconstruction (t=8192), so their fw=8 is post-mortem —
AC91 does not isolate loss/recovery of coordination itself; that is AC92's task.

**AC90 proposed a closure boundary (`CLOSURE_BOUNDARY_v2.md`), a writing/analysis card, not a new
experiment; the "substrate" boundary is a modeling choice the review left unresolved, not a settled
finding.** It declares (1) the generic substrate — the `advance()` transition logic
(copy -> verify -> switch -> remove), the tick clock, the decode format (14-bit word =
`enabled|mask<<1|action<<10`, majority read, paid write), the write-primitive format, the
interpreter fallthrough, the conservation laws, the observation function, the damage model and the
world constants — as supplied format-level machinery, versus the organism-specific
produced/replaced components (the 130-bit description and the coordinator's working state), and
states plainly that AC87 internalizes the coordinator's *state*, not its *mechanism*, and that
demanding the mechanism self-rewrite is an infinite regress, not a scientific target; and (2) the
necessary maintenance (description maintenance + reconstruction, recipe replacement) from the
optional capability (coordinator-state maintenance, G6) — the goal claim rests on the necessary
dependencies. It folds in AC89's positive result (the adversarial priority and the simultaneous
challenge both hold 8/8), records the unchanged limit set (no catastrophic recovery,
four-bank-rule format, no content self-production), and writes the accepted-milestone statement.
The AC67/AC68-era `CLOSURE_BOUNDARY_v1.md` is preserved unchanged (AC71 cites it by name). The
"goal active" framing above is revised accordingly: the goal is to verify and bound this milestone,
not to internalize the next thing.

**AC87 FROZE and its claim PASSES — all nine gates** (`AC87_PROTOCOL_v1.md` hashed before the run;
`AC87_RESULTS_v1.md`; seeds 4028-4031 × 2 histories, 320 rows, 16,384 ticks). The integrated
successor: the full 130-bit description (words + permutation + bank-rule masks/actions) lives in four
interchangeable slots, the succession coordinator's working state (active / phase / last-start) lives
in the same vulnerable damage-streamed paid-maintained substrate, both source and successor are
exposed to damage behind a real verify gate (switch only after the successor decodes syntactically
valid AND matches the source), the decode is generic over syntax (a non-convention mask/action decodes
faithfully, no `m==(4<<b)` correctness rule) and order-preserving, and the AC82/AC83 composition
(corrupt rule 0 at t=8192 + channel-1 move at t=12288) is re-run with the corrected decoder. **Result:
`succession` survives 8/8 with 6-7 cycles and desc 130/130 (controller state ends idle, minority 0-1);
the composition holds both routes 8/8; `unmaintained` and `no_repair` die 8/8; the no-damage control
is byte-identical `succession`==`repair`.** This closes the review's three residuals — the succession
controller's state is now under maintenance (G6), the verify is a real gate, and AC85/AC86 are one
architecture. **Two caveats, stated plainly:** (a) the finals' priorities `[3,2,1,0]`,
`[1,2,3,0]`, `[1,2,0,3]`, `[3,0,1,2]` do not include AC83's adversarial `[3,0,2,1]` (renewal rule
last), so the seed-dependent renewal-contention limit is not exercised on these finals — route-holding
is a lower bound; (b) G6 is a state-cleanliness contrast (the succession is robust to its own state's
degradation), not a survival claim. Verification: audit passes (320 rows, 14 hashes no drift,
decode==acquired), replay **6/6 exact**, 14 AC87 tests + full AC1-87 line (136 tests) green.
**Boundary unchanged:** no catastrophic-recovery claim (AC61), four bank rules still four bank rules
(format), no content self-production (AC78). This is the replacement machinery's own coordination
moved inside the organization — not full autopoiesis.

**AC85 FROZE and its claim PASSES — all six gates** (`AC85_PROTOCOL_v1.md` hashed before the run;
`AC85_RESULTS_v1.md`; seeds 4024-4027 × 2 histories, 64 rows, 16,384 ticks). The question: AC80
internalized the reconstruction recipe but its generic decode still DERIVED the four bank rules from
the permutation by the architectural convention bank b → (enabled=1, mask=4<<b, action=2+b) — the
last supplied machinery on the reconstruction path. AC85 stores the bank rules' masks and actions as
vulnerable, damage-streamed, paid-maintained state alongside the words and permutation (a 130-bit
description: 5 words + 8-bit permutation + 4×9-bit masks + 4×4-bit actions), and `rebuild` READS
them instead of deriving them — no function on the reconstruction path computes a mask or action
from a bank index, and a degraded description decodes to None (invalid permutation, or a stored
mask/action inconsistent with the permutation) rather than a silently wrong controller. The decode
is order-preserving (AC86's correction carried forward): it reproduces the ACQUIRED program, not
`prog.program` order. **Result: `internalized` survives 8/8 and recovers every corrupt individual
(fw=0, description 130/130 — words 70/70, permutation 8/8, bank-rule masks+actions 52/52);
`unmaintained` dies with the description degraded (word 17-20/70, bank 10-12/52 — the convention
itself now degrades); `no_repair` dies 8/8; the no-corruption control is clean (fw=0,
description_same=1).** The bank-rule content is now inside the maintained state, so the G2 contrast
measures the convention's own degradation, not just the words. Verification: audit passes (64 rows,
14 hashes no drift, arm invariants, decode==acquired, gates recomputed without simulating), replay
**6/6 exact**, 12 AC85 tests, AC core suite + AC71-86 line green. **Boundary restated:** no content
self-production (AC78); the four bank rules are still the four bank rules — what moved into the
vulnerable state is their mask/action content, not the fact that four bank rules exist (format).
This closes AC80's recorded residual (4).

**AC84 FROZE and its claim PASSES — all six gates** (`AC84_PROTOCOL_v1.md` hashed before the run;
`AC84_RESULTS_v1.md`; seeds 4020-4023 × 2 histories, 24 rows, 4096 ticks). Milestone 2 (replacement
across generations) re-established **without the survivor-conditioning weakness AC81 carried**: AC81
gated its turnover claim on `completed` (2/8 survivors), so AC84 scores turnover and use on **every
individual, dead or alive** — no `completed` filter — and drops the t=8192 kill intervention (the
components turn over continuously with no intervention). **Result: every internalized individual,
including seed 4021 (both histories) which dies at t=3464 of the AC68 W/C collapse with the recipe
intact (78/78), fully replaces each component class — W 293-361 births vs 16 slots, C 50-64 vs 4,
B 337-418 vs 20 — and uses them (writes 1611-3030, converted 930-1125, both routes bound). The two
collapse deaths (seed 4021, both histories) are the fragility finding, not a licence to gate: that
individual's turnover (293/50/337) far exceeds the floors, so the collapse never prevented turnover
from being observable.** The causal contrast is categorical at the
turnover level: `no_repair` (loop cut) dies 8/8 with **B_birth=0 in every individual**, and
`unmaintained` degrades the recipe (65-72/78) and dies 8/8. The unconditional floor is "births >= the
slot complement" (16/4/20) — NOT 2x, because a broad 256-individual scan found an earliest collapse
at t=603 (W=30, C=5, B=37) below the 2x floors, so "multiple turnover cycles" is reported per
individual (healthy ~18-23x) rather than gated. Horizon 4096 sits inside the pre-collapse window
(8/64 collapse vs 24/64 at 16384). Verification: audit passes (24 rows, 15 hashes no drift,
unconditional-turnover floor recomputed without simulating), replay **6/6 exact**, 8 AC84 tests
(including a test pinning G1 to the full cohort), full 571-test suite green. Boundary restated: no
content self-production (AC78), the description is the terminal non-regenerable reference, the bank
rules are still synthesized by convention — this is replacement of the physical components, not
discovery of a better recipe.

**AC86 FROZE and its claim PASSES — all seven gates** (`AC86_PROTOCOL_v1.md` rev 1.1 hashed before
the run; `AC86_RESULTS_v1.md`; seeds 4016-4019 × 2 histories, 48 rows, 16,384 ticks). The question:
is the recipe-bearing storage itself — the physical substrate carrying the 78-bit description — a
replaceable component? AC81 (milestone 2) showed W/C/B components turn over but never the recipe
storage, which sits at a fixed location and is repaired in place. AC86 puts the recipe in `SLOTS=4`
interchangeable storage slots in bank 1, with a 2-bit generation pointer (also bank 1, offset
312-313) selecting the active slot; on the recipe's own degradation signal the organism constructs a
paid, W-catalyzed successor copy, verifies it decodes to a valid program and matches the source,
switches the pointer, and only then clears the old slot. **Result: `succession` survives 8/8 with 7
complete replacement cycles each (all four slots cycled, every cycle `verified_valid` and
`target_correct`), description 78/78; `repair` (in-place repair only) survives 8/8 with 0
successions and 78/78; `unmaintained` loses the recipe (23-46/78) and dies 8/8 (1754-2273). The
no-damage control is byte-identical across arms (0 successions, 78/78, state_hash equality).**
Two engineering findings drove the final design: (1) AC80's `build_program` reorders the acquired
program (prog.program order vs `ac9_priority_v2`'s reorder), so AC80's re-instantiation moves the
dead rule on every fire — harmless for AC80's always-zero register but fatal for any decision state
resolved against the acquired layout; `rebuild_active` is order-preserving (unit-tested bit-for-bit
against the acquired program). (2) A pointer stored in the program bank's dead rule is damaged by
the *program* stream (on even in the no-damage control) but repaired only by action 2's whole-bank
majority-restore (obs bit 2), too slow for a 2-bit pointer — a 4/7 flip cements; the pointer lives
in bank 1 (recipe stream) with its own minority-count trigger, which is what makes the no-damage
control clean. Verification: audit passes (48 rows, 15 hashes no drift, gates recomputed without
simulating), replay **6/6 exact**, 14 AC86 tests, full AC1-AC81 suite green. **Boundary
restated:** no recovery from catastrophic recipe-content corruption (a successor copies the active
slot's majority), the bank rules are still synthesized by the architectural convention (AC80's
residual 4, supplied machinery), and no content self-production (AC78 still blocked) — this is
turnover of the recipe substrate, not discovery of a better recipe.

**AC80/AC81/AC82 froze the "internalize the reconstruction recipe" arc (commit 6a1f4fb), with a
corrected reading in `AC79_ERRATA_v1.md`.**

AC80 (milestone 1, seeds 4008-4011, 6 gates) internalizes the reconstruction recipe: the five rule
words (70 bits) + the 8-bit permutation now live in vulnerable paid-maintained state, and a generic
decode `rebuild` (bit-identical to `prog.program`, unit-tested) replaces the external `prog.program`
on the reconstruction path. The AC79 "rides obs bit 2" trigger is insufficient at 78 bits, so the
description carries its own minority-count trigger (DESC_TRIGGER=2). 8/8 internalized individuals
recovered the corrupted bits; 6/8 survived. **Residual limitations:** reconstruction still has an
automatic host-side trigger (fixed DESC_TRIGGER=2 fires before action selection — calling it
"format-level" does not settle whether it is generic machinery or a host-supplied controller), and
the four bank rules are still synthesized by a fixed convention (bank b → mask 4<<b, action 2+b) —
supplied machinery, not stored state.

AC81 (milestone 2, seeds 4012-4015, 8 gates) shows surviving organisms repeatedly replace W/C/B
components using the internally stored production rules (W ~95x, C ~64x, B ~84x their complements).
But only 2/8 survive (both histories of seed 4015), and the deaths are part of the mechanism's
performance, not "known collapse" to dismiss: seed 4013 dies at 9083 with partial loss vs 11704
without; seed 4014 survives without loss but dies at 15229 with it, recipe intact — preserving the
recipe does not guarantee preserving the organization. It does not demonstrate successive replacement
of the recipe-bearing storage itself.

AC82 (milestone 3, engineering only, no frozen claim) combines reconstruction + description
maintenance + route-move adaptation and answers NO to unconditional composition: reconstruction and
description maintenance are unconditional (16/16), but route re-acquisition is not (10/16), because
the reconstruction cost + the move's income cut set obs bit 1 and the frozen priority's material
contact preempts the renewal (the AC74 attention-hijack pattern).

**Corrected reporting (`AC79_ERRATA_v1.md`):** AC79's frozen cohort is 2/8-2/8-0/8, not "12/12"; G1/G5
were outcome-informed survivor-filter revisions, not prospective gates; AC78's "fails everywhere"
over-reaches its six-position-world scope; consciousness §7 was a scheduling decision. All status
summaries must use these corrected numbers.

**AC79 FROZE and its claim PASSES — all six gates** (`AC79_PROTOCOL_v1.md` hashed before the run;
`AC79_RESULTS_v1.md`; seeds 4004–4007 × 2 histories, 64 rows, 16,384 ticks). The question: does
AC76's compressed-description turnover rely on a *hidden pristine backup* (the 8-bit priority
description stored in dead bank 1, where the damage stream never reaches it and no action repairs
it)? AC79 puts the description IN the sticky 1e-4 damage stream (an independent stream) and maintains
it with a paid majority-restore folded into the corruption-triggered re-instantiation. **`maintained`
recovers the program and keeps the description intact exactly where `pristine` recovers
(per-individual fw equality 2==2, 0==0), while `unmaintained` degrades (descValid=0) and dies 4/4
(8287–8325, the AC76 baseline signature) and `no_repair` dies 8/8 (449–704) — maintenance is both
sufficient and necessary.** Survival is bimodal and reported as a lower bound only (2/8 on this
collapse-heavy final family vs 12/16 engineering — AC39's transfer failure in the unfavourable
direction); the clean endpoints (recovery, description integrity) gate on **survivors** because the
paid maintenance stops at death (a gate-shape correction recorded in the protocol, two deviating runs
disclosed at `ac79_deviation_seeds4000_v1/`). Verification: audit passes (64 rows, 14 hashes, arm
invariants, gates recomputed without simulating), replay **6/6 exact**, 6 AC79 tests (including
description-repair-is-paid and register-exclusion unit tests), 533-test full suite green. **Boundary
restated:** the description is the terminal non-regenerable reference — its own past-majority
corruption is cemented (AC61 one level down), the "catastrophic destruction" analog, not a hidden
backup. **Not content self-production** (AC78 still blocked): this establishes only that the
description's storage + maintenance is endogenous.

**AC1–AC4 confirmatory v1 FROZE and the foundational claims CONFIRM on fresh seeds**
(`AC1_4_CONFIRMATION_PROTOCOL_v1.md` hashed before the run; `AC1_4_CONFIRMATION_RESULTS_v1.md`;
`ac1_4_confirm_results_v1/`, 568 rows, seeds 5100–5507). This closes status item 28: the four
foundational constituents were engineering-evidence-only, and every later AC study was frozen on
fresh disjoint seeds while AC1–AC4 were not. The confirmatory study re-runs each claim's decisive
contrast and validity controls on new families, reusing the frozen physics unmodified. **AC1
(vulnerable controller paying for its own repair) confirms 8/8 at both rates, including the
free-ablation contrast (+0.627/+0.850); AC2 (produced W catalysts) confirms 16/16 at both rates,
synthesis contrast +0.380/+0.658 and clamp-info contrast +0.732/+0.856; AC4 transport confirms 8/8
(B contrast +0.817/+0.829, every no_B exports W/C); AC4 long-horizon repair dependence confirms 8/8
(no_policy_write 0/8 at both rates, contrast +0.379/+0.563).** **One gate fails and is recorded,
not amended: AC3 G1 at the highest rate (0.0004) — self completes 7/8, one death (activity 0.751,
policy accuracy 0.9844, the policy-corruption-then-death pattern), while AC3's causal gates (C
dependence +0.914, W-under-clamp +0.915, turnover) all pass.** So the engineering claim "all 24 AC3
self runs complete" does not fully transfer at the highest rate (AC39's lesson in the strong
direction), but the produced-converter mechanism is confirmed. Verification: audit passes (568
rows, gates re-derived without simulating, source hashes un-drifted), replay **59/59 exact**, 10
tests including seed-family disjointness and a falsifiability test. Nothing about autopoiesis; the
controller remains externally supplied (`DEPENDENCY_AUDIT_v1.md`).

**AC76 FROZE and its claim PASSES — all five gates** (`AC76_PROTOCOL_v1.md` hashed before the run;
`AC76_RESULTS_v1.md`; seeds 3000–3003 × 2 histories, 48 rows, 16,384 ticks). The question: is the
controller-bearing component *regenerated* (§3), not merely repaired? The organism stores its 8-bit
priority description in the dead legacy bank and re-instantiates the 126-bit program from it through its
own paid, vulnerable machinery (excluding the 4 register bits). Under bounded corruption (majority of the
first 8 program bits flipped — the fuel-acquisition rule), **`regen` recovers the corrupted bits (0/8
wrong, 8/8 survive, program 125–126/126), `baseline` (single-bank majority-restore) cements them (8/8
wrong) and starves to death 8/8 (8400–8422), and `no_repair` dies 8/8 (393–758) — so regeneration is
load-bearing and crosses the AC61 boundary (repair freezes a corrupted majority).** Secondary result: in
the control the baseline's program silently *drifts* to 102–106/126 over the horizon (sticky-SET +
majority-restore cementing the drift) while re-instantiation holds 125–126 — regeneration also *prevents*
drift, not only recovers corruption. A dead-rule-index bug (`5+priority.index(3)` → `4+…`, the
`ac9_priority_v2` rule reorder) was caught by the register-exclusion unit test and fixed before
finalizing. Verification: audit passes (48 rows, 12 hashes, gates recomputed without simulating), replay
6/6 exact, 4 AC76 tests, 310-test full suite green. **Not established, plainly:** content
*self-production* (the priority is still externally supplied — this is turnover of an inherited
description, not production of it), recovery from catastrophic corruption (≥16 bits is economically
unrecoverable; consistent with the goal's "not recovery from complete destruction"), and the description's
own maintenance. The §3 milestone (endogenous component replacement of the controller) is now **frozen**
for bounded/gradual turnover, not claimed as full autopoiesis.

**AC75 FROZE and its claim PASSES — all eight gates** (`AC75_PROTOCOL_v1.md` hashed before the run;
`AC75_RESULTS_v1.md`; seeds 2900–2903 × 2 histories, 96 rows, 16,384 ticks). The question: is the AC71
reconciled closure (majority read + load-bearing repair) *world-accommodating*, or only fixed-world? AC74
found a route move is fatal (material→W→re-acquisition cascade via a stale-route persistence window). AC75
joins AC16's re-acquisition machinery (deposit open + restore rule) to the AC71 closure and adds the one
declared change that closes the cascade: **erase-on-relinquish** (the drop also clears the entry, booked as
memory expiry, not a paid write). **Result: `erase` survives 8/8, re-acquires the moved route and holds
both routes (`demand=[42,0]`) with register intact, under a permanent move AND a temporary outage (two
transitions) — while the no-erase rival `restore` dies 8/8 under change (8439–8449) and `erase_no_repair`
dies 8/8 (403–792), so the repair loop stays load-bearing. The unchanged-world control is exact
(`erase` ≡ `restore`, zero relinquishments).** The mechanism is legitimate (the organism's own
relinquishment, its own vulnerable bank, no privileged info or external rescue) and generalizes across the
transition family. Verification: audit passes (96 rows, 12 hashes, gates recomputed without simulating),
replay 6/6 exact, 306 tests green. This is the first result where the closure survives *change* at the
long horizon. **It does not close the structural gap** (`DEPENDENCY_AUDIT_v1.md`): the controller is still
externally supplied and only maintained, not produced — this is a body/function/decision-state closure,
not autopoiesis.

**AC71 FROZE and its claim PASSES — all five gates** (`AC71_PROTOCOL_v1.md` hashed before the run;
`AC71_RESULTS_v1.md`; seeds 2800–2803 × 2 histories, 16 rows, 16,384 ticks). The single declared change
from AC67: read the decision-state register by **majority (4)** instead of single-replica (1). This is the
reconciled configuration AC69/AC70 diagnosed: the three closure gaps of `CLOSURE_BOUNDARY_v1.md` had one
root cause — a read/repair threshold mismatch — and majority read closes all three at once. **Gates:
G1 closed survives 8/8; G2 routes held 8/8 (`demand=[42,0]`); G3 body stable 8/8 (W=3, C=2, energy
118–125, no bimodality); G4 register intact 8/8; G5 no_repair dies 8/8 (deaths 402–860, observation
hijack).** So the acquired function is now self-maintaining, the body is de-bimodalized, the register no
longer degrades, and the repair loop stays load-bearing — but the load-bearing constraint has *shifted*
from the decision register (AC67) to the self-monitoring observation (the program's own corruption
signal). The reconciled architecture: a **robust decision state** (majority read) plus a **load-bearing
self-monitoring loop** (paid repair of its own corruption signal). Verification: audit passes (five gates
recomputed without simulating), replay **5/5 exact**, 6 tests. Nothing about autopoiesis (the controller
is still acquired, not self-produced) or consciousness.

**AC68 froze: repair is necessary but not sufficient — body bimodal, function open, register intact only
in survivors** (`AC68_PROTOCOL_v1.md` hashed before the run; `AC68_RESULTS_v1.md`; seeds 2700–2703 × 2
histories, 8 rows, 16,384 ticks = 4× standard). Long-horizon follow-up to AC67 on the same closed arm.
**Gates: G3 PASS (routes lapse in 8/8), G1/G2 FAIL (body survives/maintained only 4/8)** — the claim
"body self-sustaining, function lapses" is falsified on the body half. The measured pattern: 4/8 reach a
steady state (energy ~120, W=2, C=2, B=20) and survive; 4/8 collapse at ~7,400–7,800 via a W/C decay
cascade (the AC47 stable-vs-collapse limit re-entering through the long horizon). Three gaps located for
full organismal autonomy: (1) the acquired function (routes) lapses in all 8 via scheduling neglect —
region 1 renewed zero times, the program spends its actions on W/C birth (8,792) and idle (4,357) not
renewal (132); (2) the body's self-production is bimodal/fragile, not robust; (3) the register is intact
in survivors but degraded in the dying via the organism's own `_drop` relinquishment (the
majority-directed repair cannot undo it) — a refinement of AC67: repair maintains the decision state
against *damage*, not against self-relinquishment. Engineering seeds 0–2 all survived, finals split 4/4
(AC39's transfer lesson again). Verification: audit passes (gates recomputed without simulating), replay
**4/4 exact**, 6 tests including tests asserting the recorded G1/G2 failure and the register bimodality.
Nothing about autopoiesis or consciousness.

**AC67 froze: the repair loop is load-bearing — and AC14's "inert loop" was an artifact**
(`AC67_PROTOCOL_v1.md` hashed before the run; `AC67_RESULTS_v1.md`; seeds 2600–2603 × 2 histories,
32 rows, 4096 ticks). The one declared change from the frozen physics is the damage model AC14's
option 2 asked for: program-bank damage is a sticky SET (`|=`) not a toggle (`^=`), so a damaged
replica stays damaged until the paid bank-0 repair rewrites it; register read is single-replica.
**Result: 8/8 survive with the repair link intact, 8/8 die with it cut** — the loop is load-bearing,
not inert. This corrects AC14: its `arm_parts` matched `'_no_repair' in arm` but the arm is named
`'no_repair'` (no underscore), so the substring never matched and its `no_repair` arm ran with repair
*enabled* — identical to `closed` by construction, which is the whole of the "no observable
consequence" finding. **Gates: G2/G3/G4 pass (survival separation 8/8 vs 8/8, closed register intact,
closed survives); G1/G5 FAIL and are recorded as such** — the death has *two* paths, decision-state
degradation (6/8: register flips to "relinquished", the entry lapses, death) and observation hijack
(2/8: sticky damage sets the bank-0 corruption bit permanently, the program loops on repair+birth,
never acquires routes, drains energy to death). The register-only claim is falsified; the broader
claim — the program bank (rules *and* decision register) is a maintained constraint whose repair is
causally necessary — survives complete separation. The protected arms are confounded (the observation
is read from the live damaged bank, not the shadow) and are not used. **Verification:** audit passes
(gates recomputed from the table without simulating, 12 source hashes), replay **5/5 exact**, 7 tests
including tests that assert the *recorded* G1/G5 failure. Nothing about autopoiesis or consciousness;
the mechanism is measured, not assumed (`first_register_flip < first_death` in every register-path
individual).

**AC18 froze and its claim PASSES — all eight predeclared gates** (`AC18_PROTOCOL_v1.md`
hashed before the run; `AC18_RESULTS_v1.md`; seeds 2500-2503 × 2 histories, 88 rows, 4096
ticks). The gate is the claim's own shape — a **separation of worst cases**, which is what
"a one-way rule cannot hold" means: **G1 PASS** (learner's worst individual **1.000**, i.e.
1.000 in all 8), **G2 PASS** (one-way's worst **0.429**), G3 PASS (keeping arms exactly 0.000
with no re-binding tick, every individual), G4 PASS (kept channel 1.000), G5 PASS (three
consistency equalities exact on `state_hash`), G6 PASS (`restore_only` barred — structural),
G7 PASS (no blind rival or swept configuration reaches 0.90), G8 PASS (all declared arms
complete). **The learner is invariant at 1.000 while one-way ranges 0.429-0.800 and the crude
always-relinquish arm 0.444-0.714** — both rivals re-bind but neither can hold, their values
varying with re-binding luck; the learner's constancy is the mechanism's signature. Note what
the passing gate does *not* require: unlike AC17's unsatisfiable demand, the learner need not
beat one-way on every individual, only that one-way cannot *guarantee* holding. **Necessity
confirmed on three seed families:** drop-only binds but cannot hold (0.429-0.800 / 0.462-1.000
/ 0.636-0.889), restore-only is exactly 0.000 with no re-binding (it never frees the key, so
the frozen deposit gate bars it), and both directions together hold in every individual — so
the two-way rule is **necessary and sufficient within this machinery**. **This closes the
project's open item** (a controller that acquires the need to allocate or relinquish under a
post-development intervention, no protected copy, no externally fixed correct state) modulo the
stated scope: behavioural and economic, not survival-level (every declared arm completes);
**not** generalized to worlds where both channels move (measured and excluded in AC17's
engineering, where the crude arm already reaches 0.93); no optimality claim; nothing about
consciousness/experience/autopoiesis. **Verification:** audit passes (coverage, invariants, 18
hashes with no drift, three equalities, all eight gates recomputed without simulating); replay
**8/8 exact**; 15 AC18 tests including a satisfiability test on the gate and a seed-disjointness
test; **149 tests pass** in the full suite; every tool hashed up front with no post-freeze edit.
**Process lesson:** three consecutive versions were affected by gate shape — AC16's mean margin
(falsified by 0.006 while dominating 8/8 individuals), AC17's strict dominance (unsatisfiable at
the ceiling), AC18's separation of minima (passes, and could have failed). **Classify the claim
first: "cannot hold" is a worst-case statement → separation of minima; "worse on average" → a
justified margin; "better everywhere" → dominance exempting the ceiling.** Both falsifications
stand permanently and neither is re-run with better-chosen gates.

**AC17 v1 froze; the mechanism holds in every individual, and the claim is falsified only by
an unsatisfiable gate — my design error** (`AC17_PROTOCOL_v1.md` hashed before the run;
`AC17_RESULTS_v1.md`; seeds 2300-2303 × 2 histories, 88 rows, 4096 ticks, single-channel
move). Gates: **G1 PASS** (learner holds ≥0.90 on the moved channel in **8/8 individuals**,
value 1.000 each), **G2 FAIL**, **G3 PASS** (every keeping arm exactly 0.000 with no
re-binding tick, every individual), **G4 PASS** (kept channel 1.000), **G5 PASS** (three
consistency equalities exact on `state_hash`), **G6 PASS**, **G7 PASS** (blind rivals and the
whole swept family 0.000), **G8 PASS** (all declared arms complete). **G2 asked for strict
per-individual dominance over one-way and is UNSATISFIABLE BY CONSTRUCTION**: on 2 of 8
individuals one-way *also* reached 1.000, so strict `>` cannot hold regardless of the
mechanism. That is a defect in my gate, not a result, and it should have been caught when the
protocol was written. **The claim's true categorical shape is a separation of worst cases:**
learner minimum **1.000** (holds every time) against one-way minimum **0.462** (fails to hold
somewhere) — one-way is not merely lower on average, it cannot *guarantee* holding, and when
it does hold (seed 2301) that is luck of re-binding timing, which is why its value is
seed-dependent 0.462-1.000 while the learner's is invariant. That gate was **not** declared in
advance, so it is not this study's result. **AC17's genuine new knowledge is G6/Claim A, and
it is structural rather than empirical:** `restore_only` (restore rule, no drop rule) scores
exactly 0.000 with no re-binding tick in all 8 individuals, predicted from the frozen code
before the run because `mem.deposit` requires `selected is None` — so with AC16's drop-only
result (binds but cannot hold), **both directions are necessary and each is insufficient
alone**. **A third claim was killed before the protocol** (`AC17_ENGINEERING_v1.md`): in the
both-channels-move world the crude always-relinquish arm reaches 0.93 mean against the
learner's 0.75 (an arm that never renews is always free to re-bind), so that world is excluded
rather than reframed. **Verification:** audit passes (coverage, invariants, hashes, three
equalities, all eight gates recomputed without simulating, reporting G2 FAIL correctly);
replay **8/8 exact**; 15 tests, with the G2 test asserting the recorded unsatisfiable-gate
result plus the minima separation and the ceiling tie count; protocol, runner, audit, replay
and test file all hashed up front (AC16's post-dated test gap is not repeated). **Two
consecutive falsifications by gate shape** (AC16's mean margin, AC17's unsatisfiable
dominance) → rule for AC18: derive the gate from the claim's logic — "a one-way rule cannot
hold" is a worst-case statement, so test a **separation of minima**, declared on fresh seeds.

**AC16 v1 froze and its claim as specified is FALSIFIED — by 0.006** (`AC16_PROTOCOL_v1.md`
hashed before the run; `AC16_RESULTS_v1.md`; seeds 2100-2103 × 2 histories, 80 rows, 4096
ticks). The question AC15 left open was answered mechanically first: AC15's learner never
bound a correct route after the move because the frozen deposit path is gated on `grow` and
the frozen runner stops growth at t=512, before AC15's t=1024 intervention — **AC15's world
had re-acquisition switched off**. AC16 opens that window (the single declared change) and
adds one primitive: a **restore** rule symmetric with the drop (relinquish on a streak of
failures, restore maintenance on a productive contact — sound because the frozen gate can
only be passed by a match, and the deposit binds exactly the port that matched; both writes
paid per replica into the same vulnerable bank). **Gate outcomes: G1 PASS (learner holds a
correct route at 1.000 in all 8 individuals), G2 FAIL (+0.2437 against a predeclared +0.25),
G3 PASS (keeping arms exactly 0.000 and never a re-binding tick), G4 PASS (kept channel
1.000), G5 PASS (all three consistency equalities exact on `state_hash`, including
`restore_disabled` == one-way `allocate`), G6 FAIL (`relinquish` dies 4/8; not in the
falsification list), G7 PASS (blind rivals 0.000).** The protocol says G1-G5 or G7 failing
falsifies the claim, so **AC16 v1 is falsified and I did not amend the protocol or move the
threshold.** What the data shows is a clean three-way categorical separation: keeping arms
**cannot re-bind at all** (the frozen gate requires `selected is None`, so holding a stale
entry bars binding — a structural control supplied by frozen code, not a scaffold), one-way
relinquishment **binds but cannot hold** (re-binds at ticks 1139-1309, lapses within its
64-tick life, scores 0.636-0.889), and the two-way rule **holds at 1.000 in all eight
individuals** while never sacrificing the valid channel. The learner strictly dominates
one-way in **8/8 individuals** (+0.111 to +0.364); only the *mean* margin fell short.
**Why G2 was the wrong test:** the claim is categorical, and a mean margin over a rival that
partially succeeds by re-binding repeatedly measures how often one-way gets lucky, which is
seed-dependent and irrelevant to whether holding is possible. **That diagnosis is not
licence to re-run AC16 with a better threshold** — the next version (AC17) declares
dominance and categorical gates in advance on fresh seeds: learner ≥0.90 in *every*
individual, every keeping arm exactly 0.000 with no re-binding tick, strict per-individual
dominance over one-way, plus the three consistency equalities. **Verification:** audit
passes (coverage against the declared seeds, invariants, hashes, all three equalities, all
seven gates recomputed without simulating); replay **7/7 exact**; 17 tests pass, two of
which are regression tests asserting the *recorded* failures so a code change cannot
silently absorb them; the frozen conservation identity holds exactly with the restore
booked. **Disclosed gap:** `test_ac16.py` postdates the frozen snapshot (authored after the
run started, cannot affect it), reported as a warning by the audit every run.

**First gated positive result in the allocation line: AC15 frozen, all five prespecified
gates PASS** (`AC15_PROTOCOL_v1.md` hashed before the run; `AC15_RESULTS_v1.md`; seeds
1900-1903 × 2 histories, 64 rows). The claim: under the graded access law — where a wrong
stored port costs a declared quarter of the yield instead of everything, the fix for the
AC11→AC13 wall in which a stale entry earned exactly zero and starvation made the decision
for the organism — after an unannounced post-development move of **one** channel, an
organism whose per-slot maintenance decision is driven by its own realized contact outcomes
relinquishes the stale route and keeps the still-valid one. Measured: learner mean late
per-channel productivity **0.699** (kept channel 1.000, moved 0.398) versus `preserve`
0.500, `relinquish` 0.439, and *every* state-blind rival at exactly 0.5000 (fixed duties
1,2,3,4,8; random p 0.25,0.5,0.75). All 8 learner individuals relinquish exactly one slot,
keep the valid route at 1.000, and end at demand [21,0]; 64/64 arms complete the horizon,
so the result is behavioural and economic, **not survival-level**. The design is two-sided
and both ways to fail it are measured failing: `preserve` keeps what it should not (moved
0.000) and `relinquish` loses what it should keep (kept 0.343). **The intervention had to be
asymmetric to discriminate** — moving both channels makes "drop everything" optimal
(`relinquish` 0.560 > learner 0.294 in the first grid), which is why the protocol declares
`MOVE_ACTIONS=(1,)`. **G3 holds exactly**: duty 1/1 (`fixed_period_1`) and an unreachable
streak (`streak_never`) each reproduce `preserve` including the state hash — the same
consistency check that falsified AC11. **Verification:** `audit_ac15.py` passes (coverage,
per-row invariants, no hash drift, protocol hashed, all gates recomputed without
simulating); `replay_ac15.py` **6/6 exact** (first attempt reported 0/6 purely because JSON
round-trips int keys to strings in `chan_late`/`chan_productivity`; the comparison now
normalises rather than excuses); `test_ac15.py` 13 tests pass; `GRADE=0` equivalence with
the unmodified AC12 harness 6/6 identical state hashes. **Two limits stated plainly:** no
blind rival ever lets the stale entry lapse (those arms choose whether to *renew*, and
renewal stays frequent enough that the entry's 64-tick life never expires — so they score
exactly `preserve` and G2 is real but weak), and the learner's own threshold makes no
difference (0.6989 for streaks 2/4/6/8 — the learner beats every rival at every setting, so
no selection was needed to obtain the result). **Not established: re-acquisition.** The
learner relinquishes the stale route; it does not learn a correct new one (moved 0.398 ≈
blind search's ~1/2, not above it), and every keeping arm showed productivity 0.000 after
the move. **Deviation disclosed:** the first final run used seeds 1800-1803 (the runner
still held a placeholder seed family); the protocol was **not** amended, the deviating run
is preserved at `ac15_deviation_seeds1800_v1/`, and the corrected run is the final sample.
Both seed families give the same verdict (G1 +0.200/+0.282 on 1800-1803 vs +0.199/+0.260 on
1900-1903), which is a robustness check the protocol did not require.

**Positive primitive result, the first in this line since AC10.** AC15 builds the
graded access law the AC11→AC13 wall required: on a miss (wrong port) the contact
takes a declared quarter of the yield instead of nothing — material full 64/miss 16,
fuel 32/8 — with **no conservation law touched**, because `ac4.balance` already
carries intake as a variable (`b.material == M + in_m - overflow_m - spent_m`). The
surgery replaces the frozen gate block and the productivity line, and productivity is
deliberately owned by the contact and defined by the **match** rather than by intake:
in a frozen world the two are equivalent, but deriving it from intake in a graded
world would make every stale route count as productive every tick, so the
relinquishment rule could never fire. **Verification: `GRADE=0` reproduces the
unmodified AC12 harness byte for byte, 6/6 state hashes** (e.g. 70baa91c7da7 both,
inventory 125/109/9 both). That test caught two real harness bugs: the contact called
the `ac4` module directly instead of the world's shimmed react (reinstating the frozen
yields — a 31-unit material divergence), and a forced-action builder hardcoded
`GRADE=1`, which made the first economics table show the graded column twice.
**Economics, measured per contact with the action forced and the entry inside its
64-tick life:** correct 64, stale-kept 16, blind 36 (material); 32 / 8 / 18 (fuel).
The blind fallback is a **single coin**, `port=int(coin)`, matching ~1/2 — not a
uniform draw over a port space, which the first draft of the docstring got wrong. So
dropping a stale route improves yield **2.25×** and keeping it is **survivable**,
where the frozen law offered 0 versus 26.7: a decision with a consequence in which
neither option is fatal, which is exactly what the AC11→AC13 line never had.
**Full-organism engineering grid (36 rows, 2048 ticks, port move at t=1024):** the
frozen wall reproduces — `allocate`, `preserve`, `no_learning` all **0/6 dead with
late income exactly 0**, `relinquish` 6/6, `random` 3/6, `fixed_schedule` 2/6 — and
under the graded law **all six arms survive 6/6** and differ in retained entries and
productivity (`allocate` ends at demand [0,0] with 0.294 productivity; `preserve`,
`random`, `fixed_schedule`, `no_learning` keep [42,0] with productivity exactly
0.000). **Not claimed:** that the dropping arm earns more — aggregate income is
*higher* for the keeping arms (`preserve` 1632 vs `allocate` 725), and that comparison
is confounded because a stored entry changes the observation and therefore which
actions the program chooses; only the per-contact table is valid economic evidence.
Also unclaimed and untested: **re-acquiring** a correct port rather than merely
dropping a stale one — every keeping arm never re-learns. Next step: `AC15_PROTOCOL_v1.md`
written and hashed before the first final seed, rivals swept first per AC11's lesson.

Negative closure result, with a quantified reason: AC14 cut the loop's repair link
(the program bank that carries the allocation register is repaired only by the paid
bank-0 action, whose capacity is core W, which the program itself produces) using a
frozen mechanism (`ac4.react`'s existing `no_policy_write` guard, which zeroes repair
capacity for banks 0-1; bank 1 holds only zeroed payload here). Cutting it has **no
observable consequence** in the live-register organism over 4096 ticks: identical
completion, identical activity, identical per-seed action histograms. Reason,
measured: with repair blocked for the whole run the program bank accumulates only
**3 differing replicas out of 882** (126 bits x 7), because flips are XOR and net
differing replicas is small at 1e-4 per replica per tick; the register is read by
majority of seven, so its decoded value changes only when 4 of 7 replicas differ —
no register bit flipped in 24 register-bits x 2 regimes. The loop is structurally
present but **arithmetically inert**: the decision state is nominally vulnerable yet
protected by its own redundancy, so the constraint is never at risk and closure
cannot be shown or refuted at this damage rate. Quantified requirement for a
meaningful test: raise the program-bank damage rate to order 1e-3-1e-2 (10-100x), or
store the register with less redundancy (one bit, or three replicas so a flip needs
2 of 3 — the more faithful option, since a constraint that cannot be perturbed cannot
be shown to be maintained), or use a much longer horizon. Two designs were discarded
first: blocking core-W births hijacks behaviour (obs bit 6 never clears, the W rule
fires every tick, death at 251 with activity 0.123, numerically identical to AC10's
`no_W`), so that measures attention hijack rather than the loop. One anomaly is
flagged **unexplained, not reported as a result**: `protected_no_repair` dies 0/6
(deaths 554-1381) with action 6 chosen 3403-3826 times of 4096, while `no_repair` is
unaffected, and no drops are recorded in any arm; the next diagnostic is a
first-divergence trace between the two from identical initial states. Nothing frozen
touched.

Negative design result (third in the allocation line) with a structural conclusion:
AC13's design was posed and calibrated, then falsified by a replication check
before any final seed. The calibration reported a 41% phase-2 renewal saving on 6
individuals (393 vs 662 writes, `AC13_CALIBRATION_v1.md`); on 12 fresh engineering
individuals the mean saving is **−9.3%** (range −311% to +99.8%) and `preserve`
matches the learner on phase-1 productivity and phase-2 writes in 10 of 12, so the
protocol's own falsification clause fires. Cause, measured: phase-2 renewal counts
are dominated by the slot the policy keeps; `renew` writes nothing on an
undecodable slot, so when material income is thin the material slot lapses by
starvation in *both* arms (writes 0/21/18 in both), and when the entry stays
decodable both arms keep renewing it for a handful of replicas (<5%). The 41% came
from the two individuals where the kernel lined up — six individuals were too few
to see that. What replicates: the drop is triggered by the organism's own realized
outcomes, fires at tick 1050–1098, is paid per replica, lands in the vulnerable
program bank, leaves the other slot intact, and the usefulness-blind static dies
while the route is valid (0–1/4 alive, phase-1 productivity 0.23–0.28 against
1.000). **Structural limit, now supported by three independent measurements
(AC11 region granularity, AC12 per-slot granularity, AC13 unreliable port with a
wider sample):** with a single-bit resource port whose blind fallback is uniform
over the same candidate set, the value of a stored route is either decisive
*because fatal* (a wrong stored value zeroes income) or negligible (a stored value
earns exactly what blind search earns). The maintenance decision therefore has no
consequence between "forced by starvation" and "irrelevant", so no learner can
demonstrate a need under those conditions. Two supplied-law additions would change
that, each needing its own primitive and protocol: a **graded access law** (being
wrong costs a fraction of the yield, not all of it) and a **wider access channel
with non-uniform fallback** (a stored value carries more usable information than a
blind attempt can reach). Nothing frozen touched; 12 new test methods pass; AC10,
AC9 and AC12's primitive and register are unaffected and remain the foundation.

Progress (first positive signal in the allocation line): the AC11/AC12 wall was
removed by changing the intervention rather than the learner. Those designs failed
because the intervention zeroed the organism's income, so starvation lapsed the
entry whether or not the policy chose to relinquish it. AC13's intervention makes
the affected port **unreliable** (the channel is drawn per contact, so a stored
value earns exactly what blind search earns) and drops the material yield at the
same moment, so worthless information costs without deciding lifetime.
Calibrated world (ports 4, yields 64 before and 12 after the intervention at tick
1024, 6 engineering individuals per arm): `allocate` completes **6/6** with
phase-1 productivity 1.000 and phase-2 renewal writes **393**, against `preserve`
5/6 with 662 writes (41% more), `no_learning` 6/6 with 463, `fixed_schedule` 6/6
with 491, `random` 4/6, and `relinquish` **0/6** with phase-1 productivity 0.277.
So the route is maintained while it is worth 4x blind search, stopped 46 ticks
after it becomes worthless in 6/6 individuals, and the sham-write control shows the
write to the vulnerable register is what produces the saving. Calibration also
fixed the world: the never-maintain arm must fail while the route is valid (Y1=64;
at 48/32 it survives 2-4/6), and Y2 must not put the drop's own 7-unit payment on a
knife edge (at Y2=8 `allocate` falls to 3/6 while a scripted switch is 6/6).
Stated limitation: `preserve` survives 5/6, so this is **not a survival-level
need** -- the claim is behavioural and economic (spending tracks usefulness with
viability preserved, and the usefulness-blind static dies). Engineering outputs in
`ac13_calibration_v1/`; no protocol, tests, audit or final seeds yet; nothing
frozen touched.

Negative design result (second in the same line): AC12 built the per-slot renewal
primitive AC11 identified as missing and re-asked the allocation question with it.
The primitive works and is verified: `renew_alloc` shares the frozen per-action
capacity (a first version wrongly gave each slot its own 32-write budget — 42
writes where the frozen law writes 32 — and was discarded), and `renew_region`
reproduces the frozen `ac9_memory.renew` exactly in 6/6 stressed cases. The
allocation register lives in the four free mask bits of the frozen program's
permanently dead rule (mask 32; verified never matchable — 0 of 12 observed
observations set bit 5), inside `traces[0,:126]`, so it is flipped by the same
damage stream and repaired only by the same paid bank-0 repair; with the register
all-maintained AC12 reproduces the frozen AC9 v2 rows exactly (4/4, including
state digests), proving the change is inert. Measured outcome (6 engineering
individuals per arm): `allocate` is **indistinguishable from `preserve`** (identical
phase-1 and phase-2 productivity, same death window) and a state-blind fixed duty
cycle survives 4/6 where the learner survives 1/6. Diagnosis, measured: after the
relabelling an organism with a readable stale entry has material income exactly
zero, so renewal writes collapse to 0-3 replicas in most individuals and the entry
lapses by starvation whether or not the policy chose to relinquish it; the one
surviving `preserve` individual is the one whose key-1 entry had never been
deposited, so no stale route existed. Allocation is therefore downstream of an
economics that has already fixed the outcome. Not the break-even hypothesis I first
suspected — measured against the frozen economy the route is worth several times
its maintenance cost. Next requirement: an intervention that does not zero income
(damage a route rather than invalidate it, or move a port to a resource obtainable
another way), so that both "keep paying" and "stop paying" remain affordable with
different consequences. Engineering outputs retained in `ac12_engineering_v2/`; no
final seeds, no live process, nothing frozen touched.

Negative design result: AC11 (acquired allocation of preservation spending under
an unannounced post-development port relabelling) was falsified by its own
pre-run engineering controls before any final seed. A state-blind fixed duty
cycle reaches 4/6 viability where every configuration of the adaptive arm reaches
3/6 (thresholds N=2,4,8,16 all identical; N=32 degenerates to `preserve` at 1/6),
and fixed duty 1/1 and random p=1.0 reproduce `preserve` exactly, confirming the
harness. With both ports relabelled nothing survives the horizon and
`relinquish` scores best only by starving in the earlier phase (deaths 472–986),
so no "need to relinquish" exists there either. Diagnosis, all measured: renewal
is region-granular while the usefulness boundary is per-key, making the optimal
maintenance level intermediate and constant; and blind access at 1/4 success
cannot fund even a reduced metabolism (energy starvation with stores non-empty
and zero converters). The two requirements are in tension across regimes — the
frozen economy makes relinquishment viable but preservation unnecessary, the AC11
regime makes preservation necessary but relinquishment unsurvivable. The
requirement therefore remains NOT ESTABLISHED and now has a named prerequisite: a
per-entry renewal primitive, an aligned usefulness boundary, and a measured
economy where blind access funds the reduced metabolism (five requirements listed
in AC11_DESIGN_CONTROLS_v2.md). Side-finding carried forward: the lineage's
optimum level of memory maintenance is intermediate rather than all-or-nothing,
which explains AC6's earlier "no net material saving" and sharpens why the AC9
v1→v2 stored rule-order change mattered. AC10's constituent ablations are
unaffected (they removed whole constituents, not maintenance levels). Engineering
outputs retained in ac11_feasibility_v1/, ac11_feasibility_v2/,
ac11_design_controls_v1/ and ac11_design_controls_v2/; no final seeds, no live
process, nothing frozen touched.

Progress: implemented and ran the integrated constituent ablations (AC10, seeds
1300–1303, two histories, nine arms, 72 rows) that the earlier status table
recorded as missing. All nine prespecified gates pass. W production abolished
leaves no entry ever allocated (0/8) and kills 8/8 at 248–252; C production
abolished confines conversion to the endowment (zero assay conversion) and kills
8/8 at 200–232; B production abolished exports constituents in 8/8 and loses
both routes at 195–279 while activity persists to 0.355 through random fallback;
forced retention with zero enclosure matter, and external B supply, both retain
8/8 routes, 8/8 completion and zero export, so the enclosure's causal
contribution is retention rather than mass. Late-onset W and B suppression still
destroys the acquired routes (599–609 and 647–857), making this a continuous
maintenance requirement rather than a one-time acquisition. policy accuracy was
1.000 in all 72 rows, so the acquired program bank is not the discriminating
endpoint at this horizon. 21 test methods, the table audit and 11/11 exact
sampled replays pass; the eight inherited sources hash-match the AC9 v3 freeze.
No autonomous need acquisition, full autopoiesis or rich development claim. Run
steps are terminal; no live process remains.

Progress: exact decision replay identifies memory starvation behind higher-
priority boundary work. New stored-priority version runs40 conditions and passes
all first-stage gates:8/8 entry retention versus0/8 original controls on new seeds;
occupied-region blockage loses entries, unoccupied blockage preserves them.
All balances/hashes and ten exact reruns verified. Priority bodies retain20 B
and have zero W/C exports. AC9_PRIORITY_RESULTS_v2.md records claims and limits.
Run68553 and audit terminal exit0. No broader developmental/autopoiesis proof yet.

Progress: integrated AC9, ran32 conditions, verified all resource ledgers/source
hashes, eight sampled reruns and four integrated test methods. Eight additional
keep-history chronology replays match exactly.7/8 keep bodies complete activity,
but only1/8 retains both learned entries. Initial synchronized-W-extinction
hypothesis is contradicted by the chronology. No live process remains.

Progress this turn: implemented expiring physically allocated memory with no
external key/value cache and five passing mechanism tests. A reference AC7
contact-timing probe identifies a regional-W bootstrap constraint (one observed
first contact at tick32, when an unrenewed endowment would have only2 W).
This is not an integrated AC9 prediction. AC9_MEMORY_PRIMITIVE_v0_1.md records
state, costs, scope and required integration. No AC9 organism result exists yet.
No live process remains from these tests/probe.

Progress this turn: executed developmental scope audit against hashed AC7/AC8
results: four acquired routing classes (two unknown bits), six changed guesses,
two initially correct, no within-mapping route diversity. This does not refute
autonomy; it limits the present developmental claim. Re-read E2's protected
learning/scaffolding and primary organization literature. Selected paid physical
allocation for the next design and recorded discriminating controls. This design
is not an implemented result or completed autonomy claim.

Progress: AC8 completes48 conditions with six exact sampled replays and three
test methods; both reacquisition/route-maintenance gates pass. Additional32-row
partition separates selector bits from inherited action types: selector repair
block completes2/8 versus keep8/8. All balances/hashes and mask selectivity pass,
four exact reruns plus full default equivalence verified. AC8_RESULTS_v1.md and
AC8_PARTITION_RESULTS_v1.md contain claims and limits. Original runs74372/40338
and both audits are terminal with exit0. No developmental new-need claim yet.
No live process or external blocker remains. Do not restart completed runs.
All source/results are in the shared worktree; inspect them before relying on
this summary. New files are uncommitted, and earlier AC1/AC2 artifacts are also
untracked; do not discard them as disposable temporary files.
