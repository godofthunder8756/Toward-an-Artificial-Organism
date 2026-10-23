# U1 substrate audit v1: applying the consult #25 substrate rule to the AC lineage code

Paper-only audit. No repo code, harness or planner was executed. I used only read-only `git show`/`git grep`, `sha256sum` and `rg`. The repo was not modified, and no earlier review file was changed.

Scope: this audit classifies supplied operations against a declared, finite substrate rule and restates the bounded production-closure sentence (Maturana & Varela clause (i)) under that rule. It makes no C4, C5 or consciousness claim, and it does not call the system autopoietic or alive.

Q-tags are kept separate. Everything below is a **definitional/code-reading** judgement about what the existing **Q-EXIST** closure claim may say. No Q-CAUSE, Q-LEARN or Q-NECESSITY claim is made or changed (§6).

**Citation format.** `path:Lstart-Lend@commit`. Each commit is the file's last-touching commit on `master` (`32cfbe6`). Every cited code blob is also byte-identical at `db0ef2f`, the commit `CLOSURE_VERDICT_v1.md` evaluated (checked with `git rev-parse`; see the check script). The source file for the rule is `/workspace/astra_consult25_response.txt` (sha256 `31740a1e7129baf9ff9d3c047492fdbe1952970ad836d271742b5a6f14ff8791`).

## 1. The frozen rule (verbatim)

Astra consult #25, §B.1 (`/workspace/astra_consult25_response.txt` line 27):

> "A supplied substrate operation may implement generic state transformation, transport, execution or numerical integration. Organization-specific instructions, maintenance sequences, switching conditions and repair policies must be represented in declared system state rather than hidden in the supplied operation. The substrate must execute alternative admissible instruction contents, including unsuccessful ones, without substituting the intended organization."

Consult #25's own application of the rule (line 29, verbatim):

> Under that rule, a hard-coded copy->verify->switch->remove routine is supplied organizational coordination unless that sequence is represented in maintained state. A generic interpreter can qualify as substrate; calling a function an interpreter is insufficient.

Named change 2 (line 167, verbatim):

> "Track A's substrate rule is fixed before further runs. Organization-specific maintenance sequencing must be represented in declared system state; a supplied resource gate alone does not internalize the sequence it enables."

**Operational tests derived from the rule** (applied to code text only):
- **T1 Generic:** the operation implements generic transformation, transport, execution or integration. It contains no constant or control flow specific to this organization.
- **T2 No hidden organization:** no organization-specific instruction, maintenance sequence, switching condition or repair policy lives in the operation's code or module constants instead of in declared state.
- **T3 Executes alternatives, failing ones included:** given any other *admissible* content (syntactically valid for the declared format), the operation executes it, including content that harms the organism. It does not consult or substitute the intended organization (e.g. `succ.encoded`).

**Classes.**
- **SUBSTRATE:** passes T1–T3.
- **DECLARED-STATE:** the item is content held in the organism's damageable, paid-maintained state (`traces` banks 0/1), not an operation.
- **EXTERNAL COORDINATION (violation):** an operation that fails T2. This means organization-specific sequencing, switching or repair held in supplied code.

**Declared system state** here means the maintained state named by the closure verdict: pointer, coordination (MODE, timer, RIP), route memory and decision state (`CLOSURE_VERDICT_v1.md:L38-L46@4b85851`). It also includes the component contents (description slots, program bits).

## 2. Which code the closure verdict rests on

- `CLOSURE_VERDICT_v1.md` evaluates the AC105 reference architecture at `db0ef2f`.
- AC105 builds its step from `ac95.build` with the `gated` arm configuration (`ac105.py:L171-L177@8f0218a`; `ac95.py:L168-L170@a1b9759`). It then replaces the injected maintenance function with the AC104 persistent/budget builder (`ac105.py:L177-L178@8f0218a`).
- That builder is source surgery on `ac95.maintain`, executed in `ac95`'s namespace. So the operative `advance()` is `ac95.advance` (`ac104.py:L144-L157@343ba17`). `ac99.maintain` wraps `ac95.maintain` (`ac99.py:L267-L270@8e9ab4a`).
- The verdict names both disputed operations as supplied substrate: `CLOSURE_VERDICT_v1.md:L59-L70@4b85851` (J1) and `CLOSURE_VERDICT_v1.md:L96-L99@4b85851` (scope item 2).
- The verdict's description row cites "succession copy→verify→switch→remove (turnover)" as the description's production/replacement route (`CLOSURE_VERDICT_v1.md:L35@4b85851`). Its W row cites "action 6 birth" (`CLOSURE_VERDICT_v1.md:L32@4b85851`).

## 3. Classification table

| # | Item | Citation | Executes alternative/failing admissible content? (from code) | Class |
| --- | --- | --- | --- | --- |
| I1 | `prog.choose` rule interpreter | `ac5_program.py:L33-L41@6c6323b`; call site `ac9.py:L84@6c6323b` | **Yes** | **SUBSTRATE** |
| I2 | Majority-replica decode (`ac1.decode`, `read_slot`) | `ac1.py:L67-L68@6c6323b`; `ac95.py:L261-L263@a1b9759` | **Yes** | **SUBSTRATE** |
| I3 | `build_program` generic description→program decode | `ac95.py:L243-L253@a1b9759` | **Yes** for admissible content; inadmissible permutation → `None` | **SUBSTRATE** |
| I4 | `advance()` as a whole | `ac95.py:L607-L725@a1b9759` | Executes alternative *contents*; cannot execute any alternative *sequence* | **EXTERNAL COORDINATION** (via I4e, I5, I6) |
| I4a | COPY step | `ac95.py:L659-L664@a1b9759`; `ac95.py:L341-L352@a1b9759` | **Yes** | **SUBSTRATE** |
| I4b | VERIFY step | `ac95.py:L665-L676@a1b9759` | **Yes** for admissible content | **SUBSTRATE** |
| I4c | SWITCH step (atomic pointer + MODE commit) | `ac95.py:L677-L692@a1b9759`; `ac95.py:L476-L532@a1b9759` | **Yes** | **SUBSTRATE** (write primitive); the next-phase constant at `ac95.py:L510@a1b9759` belongs to I4e |
| I4d | REMOVE step | `ac95.py:L717-L725@a1b9759` | **Yes** | **SUBSTRATE** |
| I4e | **FIXED ORDER** IDLE→COPY→VERIFY→{SWITCH, back to COPY}→{REMOVE, back to COPY}→IDLE | `ac95.py:L89@a1b9759`, `ac95.py:L642@a1b9759`, `ac95.py:L663@a1b9759`, `ac95.py:L673-L676@a1b9759`, `ac95.py:L680-L681@a1b9759`, `ac95.py:L510@a1b9759`, `ac95.py:L720-L721@a1b9759` | **No.** No state content can express a different order | **EXTERNAL COORDINATION** |
| I4f | Phase value, pointer, ACTIVE bit (what I4e reads) | `ac95.py:L85-L88@a1b9759`; `ac95.py:L291-L296@a1b9759` | n/a (content) | **DECLARED-STATE** |
| I5 | Succession start/switching condition (`succ_trigger`, `rate_ok`) | `ac95.py:L735@a1b9759`; `ac95.py:L76-L80@a1b9759`; `ac95.py:L635@a1b9759`; `ac95.py:L638-L650@a1b9759` | **No.** Thresholds are module constants | **EXTERNAL COORDINATION** |
| I6 | Timer/RIP update rule (reset on start, +1 per `TIMER_K`, clear RIP at 0) | `ac95.py:L611-L623@a1b9759`; `ac95.py:L428-L473@a1b9759`; `ac95.py:L101-L103@a1b9759`; `ac95.py:L309-L327@a1b9759` | **No** for the rule | **EXTERNAL COORDINATION** (rule); counter and RIP bits are **DECLARED-STATE** |
| I7 | `maintain()` schedule and its host injection before every action | `ac95.py:L729-L748@a1b9759`; `ac95.py:L836-L837@a1b9759`; `ac105.py:L177-L178@8f0218a`; `ac99.py:L267-L270@8e9ab4a` | **No.** No program content can omit, reorder or retime it | **EXTERNAL COORDINATION** |
| I8 | Majority-restore repair primitives (`reg_description_active`, `reg_pointer`, `reg_ctrl`) | `ac95.py:L536-L577@a1b9759` | **Yes.** Restores toward the *current* majority, so damaged-majority content is kept | **SUBSTRATE** |
| I9 | `reg_from_active` (rewrite program bits from the active description) | `ac95.py:L580-L594@a1b9759` | **Yes** for content; its excluded offsets are host-resolved (I10) | **SUBSTRATE** (operation) |
| I10 | Regeneration trigger, persistent trigger, budget rule, exclusion list | `ac95.py:L734@a1b9759`; `ac104.py:L144-L157@343ba17`; `ac103.py:L98-L112@3c89857`; `ac104.py:L118-L123@343ba17`; `ac104.py:L87@343ba17`; `ac105.py:L166-L167@8f0218a` | **No.** Thresholds and allowance are supplied constants | **EXTERNAL COORDINATION** |
| I11 | W-catalysed affordability gate (`_cap`, atomic MODE gate, combined switch gate) | `ac95.py:L336-L338@a1b9759`; `ac95.py:L369-L408@a1b9759`; `ac95.py:L476-L532@a1b9759` | **Yes**: content-blind | **SUBSTRATE** (named change 2: does not internalize I4e/I5/I7) |
| I12 | Action semantics in the step (births for 6/7/8 and others) | `ac9.py:L85-L112@6c6323b`; bank list `ac9.py:L108@6c6323b` | **Yes** | **SUBSTRATE (contested at `ac9.py:L108@6c6323b`, see §4)** |
| I13 | Relinquishment/allocation policy (`STREAK_N`, drop, reserve release) | `ac99_d2.py:L128-L159@8e9ab4a`; `ac12.py:L52@5b06281` | **No.** Threshold and branch structure are supplied | **EXTERNAL COORDINATION**; the Gray streak counter (`ac99_d2.py:L76-L116@8e9ab4a`) is **DECLARED-STATE** |
| I14 | Observation map, conservation balance | `ac9.py:L52@6c6323b`; `ac9.py:L113@6c6323b` | **Yes**: content-blind | **SUBSTRATE** |
| I15 | Program content and description content (incl. the five fixed rule words) | `ac95.py:L71@a1b9759`; `ac5_program.py:L22-L30@6c6323b` | n/a (content) | **DECLARED-STATE** (inherited content is permitted per the verdict) |

Counts: SUBSTRATE 11 (I1, I2, I3, I4a–I4d, I8, I9, I11, I14), plus I12 marked contested. DECLARED-STATE 2 as whole items (I4f, I15), plus the counter/RIP bits in I6 and the Gray streak in I13. EXTERNAL COORDINATION 6 (I4e, I5, I6 rule, I7, I10, I13 policy). I4 (the whole of `advance()`) is EXTERNAL COORDINATION because it contains I4e, I5 and I6.

## 4. Per-item evidence

**I1 `prog.choose`: SUBSTRATE.**
- What it does: majority-decodes the 126 program bits in `traces[0]`, splits them into nine 14-bit rules, and returns the action of the first enabled rule whose mask is contained in the observation. Otherwise it returns 9 (`ac5_program.py:L33-L41@6c6323b`).
- Alternatives and failing content: it executes whatever bits are present. A disabled, mis-masked or harmful rule is executed or skipped by the same generic first-match semantics. There is no reference to an intended program. The module docstring declares "Interpreter and format are supplied laws." (`ac5_program.py:L1-L5@6c6323b`).
- T1 and T2: the fixed format (rule count, width, first-match order, fallthrough 9) is generic syntax, not a sequence specific to this organization.

**I2 Majority decode: SUBSTRATE.**
- `decode` returns `sum > 3` per 7-replica site (`ac1.py:L67-L68@6c6323b`), and `read_slot` does the same for bank 1 (`ac95.py:L261-L263@a1b9759`).
- It is a generic, content-blind read that executes whatever the majority holds.

**I3 `build_program`: SUBSTRATE.**
- It rebuilds the program from the description's five words, permutation, masks and actions, and returns `None` only when the permutation is not a permutation of 0–3 (`ac95.py:L243-L253@a1b9759`).
- Any admissible description, including one encoding a harmful priority or masks, is decoded and later installed. Inadmissible syntax is refused rather than replaced, and no intended content is consulted.
- Caveat on T1: bank rules are always encoded with `enabled=1`, so the format cannot express a disabled bank rule. That is a format restriction, not an organization-specific instruction.

**I4 `advance()`: EXTERNAL COORDINATION (as a whole).**
- It is not a generic interpreter. It is a hand-coded state machine whose branch structure is the succession procedure (`ac95.py:L607-L725@a1b9759`).
- In consult #25's words, "calling a function an interpreter is insufficient". Each step's *operation* is classified separately below. The violation sits in the fixed order (I4e), the start condition (I5) and the timer coupling (I6).

**I4a COPY: SUBSTRATE.**
- It reads the source slot's majority and writes it toward the target slot under `SUCC_BUDGET` and `_cap` (`ac95.py:L659-L664@a1b9759`; `ac95.py:L341-L352@a1b9759`).
- It copies whatever the source holds, valid or not and correct or not. It is generic transport.

**I4b VERIFY: SUBSTRATE (as a test).**
- It computes `valid = build_program(tgt_maj) is not None` and `correct = tgt_maj == src_maj` (`ac95.py:L665-L676@a1b9759`).
- Both tests are generic: syntactic admissibility (I3) and copy fidelity against the organism's *own* source.
- An admissible but harmful description passes and proceeds. `succ.encoded` (the intended description) is written only into observer fields (`target_correct`) and never branches the organism (`ac95.py:L645-L658@a1b9759` shows the only reads of `succ._entry`; in the `gated`/`timer_maintained` arm they only create log entries).
- What happens *after* the test (go to SWITCH, or back to COPY) belongs to I4e.

**I4c SWITCH: SUBSTRATE (the write primitive).**
- It re-checks equality and admissibility, then `commit_switch` writes the pointer to `target` and the MODE word atomically under one W-cap affordability test (`ac95.py:L677-L692@a1b9759`; `ac95.py:L476-L532@a1b9759`).
- It would switch to any admissible copy, harmful ones included. The atomic multi-field write is a generic transaction primitive.
- Not generic: the hard-coded next phase `encode_ctrl(1, PHASE_REMOVE, last)` (`ac95.py:L510@a1b9759`) and the target rule `(source + 1) % SLOTS`. Both are assigned to I4e.

**I4d REMOVE: SUBSTRATE.**
- It writes zeros toward the slot before the current pointer, then sets IDLE once that slot is empty (`ac95.py:L717-L725@a1b9759`).
- It erases whatever is there, which is generic. Which slot to erase and when are I4e.

**I4e FIXED ORDER: EXTERNAL COORDINATION.**
- The legal transitions are written as Python control flow and constants:
  - IDLE→COPY (`ac95.py:L642@a1b9759`)
  - COPY→VERIFY (`ac95.py:L663@a1b9759`)
  - VERIFY→SWITCH or COPY (`ac95.py:L673-L676@a1b9759`)
  - SWITCH→COPY on re-check failure (`ac95.py:L680-L681@a1b9759`)
  - SWITCH→REMOVE (`ac95.py:L510@a1b9759`)
  - REMOVE→IDLE (`ac95.py:L720-L721@a1b9759`)
  - phase codes (`ac95.py:L89@a1b9759`)
- The organism's state holds only the *current* phase (I4f). No bit pattern in any declared register can make the substrate run a different order: verify-first, skip-verify, remove-before-switch, or a different target rule.
- Damage that writes an undefined phase code (5–7) matches no branch, so `advance()` does nothing until `reg_ctrl` restores the majority. That is evidence that the order is not content the substrate executes.
- This is the case consult #25 names: "a hard-coded copy->verify->switch->remove routine is supplied organizational coordination unless that sequence is represented in maintained state." The Specialist's point holds: even with I4a–I4d generic, their fixed sequence is organization-specific sequencing.

**I4f Phase, pointer, ACTIVE: DECLARED-STATE.**
- They live in bank-1 CTRL and pointer replicas (`ac95.py:L85-L88@a1b9759`) and are read by majority (`ac95.py:L291-L296@a1b9759`).
- They are damaged by the ambient stream and paid-repaired. The verdict already lists them as maintained state (S1–S4).

**I5 Succession start condition: EXTERNAL COORDINATION.**
- A succession starts when `succ_trigger` (`dm >= DESC_TRIGGER`, with `DESC_TRIGGER = 2`) and `rate_ok` (`timer_value(o) >= TIMER_MAX`) both hold (`ac95.py:L735@a1b9759`; `ac95.py:L76-L80@a1b9759`; `ac95.py:L635@a1b9759`; `ac95.py:L638-L650@a1b9759`).
- The thresholds and the conjunction are supplied constants and control flow. They are a "switching condition" in the rule's sense and are not represented in declared state.

**I6 Timer/RIP update rule: EXTERNAL COORDINATION (rule); DECLARED-STATE (counter, RIP bit).**
- The counter bits and the RIP bit are maintained, damaged and repaired state. AC95-D2 deliberately moved the RIP flag out of a host dict (`ac95.py:L309-L327@a1b9759`).
- The rule coupling them to succession is fixed code (`ac95.py:L611-L623@a1b9759`; `ac95.py:L428-L473@a1b9759`; `ac95.py:L101-L103@a1b9759`): reset while RIP and active, clear RIP when the counter reads 0, increment one bit every `TIMER_K = 200` ticks. That is organization-specific scheduling.
- The W gate makes every timer write *machinery-dependent*, which F3 showed. Under named change 2, that does not internalize the schedule.

**I7 `maintain()` schedule and injection: EXTERNAL COORDINATION.**
- The host splices `maintain(o,e,succ,reg_offs,cfg,now)` before the action line of every step (`ac95.py:L836-L837@a1b9759`), and AC105 rebinds it to the persistent/budget builder (`ac105.py:L177-L178@8f0218a`).
- `maintain()` then runs a fixed maintenance sequence: description repair, pointer repair, CTRL repair, `advance()`, regeneration. Each step has its own trigger constant (`ac95.py:L729-L748@a1b9759`; `ac99.py:L267-L270@8e9ab4a`).
- Maintenance is not an action the organism's program selects. No program content can suppress, reorder or retime it. It is a "maintenance sequence" and set of "repair policies" held in supplied code.

**I8 Majority-restore primitives: SUBSTRATE.**
- They write replicas toward their current majority under `_cap` (`ac95.py:L536-L577@a1b9759`).
- They are content-blind. A damaged-majority (failing) value is preserved, not corrected to an intended value, so T3 holds.
- *When* they fire is I7.

**I9 `reg_from_active`: SUBSTRATE (operation).**
- It writes program bits toward `build_program(read_slot(active))`, skipping host-supplied offsets (`ac95.py:L580-L594@a1b9759`).
- It is generic decode plus write, and it would install a harmful but admissible description's program.
- Its trigger, budget and exclusion list are I10.

**I10 Regeneration policy: EXTERNAL COORDINATION.**
- The parts:
  - the regeneration trigger (`ac95.py:L734@a1b9759`);
  - the persistent trigger `program_incomplete` (`ac103.py:L98-L112@3c89857`), spliced in by source surgery (`ac104.py:L144-L157@343ba17`);
  - the budget rule `max(0, material - allowance)` with `DECISION_ALLOWANCE = STREAK_N * 7` (`ac104.py:L118-L123@343ba17`; `ac104.py:L87@343ba17`);
  - the exclusion list `reg_offs + streak_offs`, resolved by the host at acquisition (`ac105.py:L166-L167@8f0218a`).
- These are repair policy and resource-priority policy in supplied code and constants.

**I11 W-catalysed gate: SUBSTRATE.**
- `_cap = min(32, 8·W, energy, material)`, the all-or-nothing MODE write, and the combined switch gate (`ac95.py:L336-L338@a1b9759`; `ac95.py:L369-L408@a1b9759`; `ac95.py:L476-L532@a1b9759`) are content-blind resource laws.
- Named change 2 applies: the gate makes the sequence *depend on* produced machinery. It does not place the sequence in declared state.

**I12 Action semantics: SUBSTRATE, contested in one line.**
- The step executes the program-chosen action: route contacts (0/1), renewals (3/4), action 6 births, and everything else through `ac4.react` (`ac9.py:L85-L112@6c6323b`). It executes any chosen action, harmful ones included.
- Contested point: action 6 births in bank 0 *plus every bank with memory demand* (`ac9.py:L108@6c6323b`). That bank-selection rule is a fixed law, but it also amounts to a supplied production priority.
- I classify it SUBSTRATE, as world chemistry analogous to a reaction rule, and flag it for Astra (Q-A2 in §8). If Astra rules otherwise, it joins the violations and §5 adds "W/C/B birth targeting".

**I13 Relinquishment policy: EXTERNAL COORDINATION (policy); DECLARED-STATE (Gray streak).**
- The streak counter lives in maintained bits (`ac99_d2.py:L76-L116@8e9ab4a`).
- The policy is a host-class method with supplied threshold and branch structure (`ac99_d2.py:L128-L159@8e9ab4a`; `ac12.py:L52@5b06281`): reset on productive contact, increment otherwise, drop at `STREAK_N = 6`, reserve-release conditions.
- This bears on the verdict's "decision state" maintained-state row. It does not bear on any C1–C5 production edge.

**I14 Observation and conservation: SUBSTRATE.**
- The observation map (`ac9.py:L52@6c6323b`) and the inventory balance (`ac9.py:L113@6c6323b`) are content-blind, supplied world laws. The verdict lists observation and conservation as supplied (`CLOSURE_VERDICT_v1.md:L96-L99@4b85851`).

**I15 Program and description content: DECLARED-STATE.**
- The five fixed rule words (including W/C/B births via actions 6/7/8) are *content* (`ac95.py:L71@a1b9759`; `ac5_program.py:L22-L30@6c6323b`). They sit in damageable description and program bits and are executed by I1/I3.
- That content is inherited, which the verdict permits (§3 item 5).

## 5. Revised closure sentence

**Triage v1.1 F1 (as written).** "Every necessary component {W, C, B, description, derived program} meets C1–C5." … "Scope: 'within the declared model and operating range, under the accepted substrate convention'."

**Revised sentence (under the consult #25 rule):**

> Within the declared model and operating range, and with interpretation, decoding, copy, comparison, write, erase, majority-restore, the W-catalysed affordability gate, action execution, observation and conservation as substrate, the production of W, C and B by program-selected actions executes declared, inherited content and meets C1–C5. The replacement of the description (succession) and the reconstruction and repair of the program and the maintained registers do not meet the rule. They are sequenced, triggered and scheduled by supplied, organization-specific coordination: `maintain()`'s schedule and triggers; `advance()`'s fixed copy→verify→switch→remove order, start condition and timer coupling; the regeneration trigger, budget and exclusion policy; and the relinquishment policy. The organism's maintained state holds only the current phase, pointer, counter and streak values that this coordination reads. Production closure of the full network {W, C, B, description, derived program} therefore holds only conditional on that external coordination, and is not established under this rule.

**What would move each violating item into declared state.** These are future protocols, not runs. Each requires its own approval, and none was designed or executed here.
- **I4e fixed order.** Represent the phase-transition table as content in a maintained, damageable, paid-repaired register: for example (current phase, test outcome) → (next phase, operation code). A generic table-driven step executes whatever table is present.
  - Admissibility check: the step must execute alternative tables (skip-verify, reversed switch/remove, a different target rule) and let them fail, without falling back to the intended order.
  - Repeat interruption, machinery-only rescue and observer-discard (F3/F4) on that version.
- **I5 start condition.** Hold `DESC_TRIGGER` and the "timer full" requirement as maintained parameters (or table entries), read by a generic comparator. Damage to them must be able to change when succession fires.
- **I6 timer/RIP rule.** Express reset-on-start and increment-per-period as table operations on the existing counter and RIP bits. Keep the W gate (it remains substrate).
- **I7 maintenance schedule.** Remove the unconditional host call. Either make the maintenance operations actions that program rules select from observation bits exposing minority counts (executed by I1), or drive them from the I4e-style declared table. Program content must be able to omit or reorder maintenance and suffer the consequence.
- **I10 regeneration policy.** Hold the trigger, the budget allowance and the protected-offset list as declared content. The host must not resolve the protected offsets once at acquisition.
- **I13 relinquishment policy.** Hold `STREAK_N` and the drop/reserve conditions as declared content executed by a generic counter-compare-act step (the streak counter already is declared state).
- **I12** (only if Astra rules it organization-specific): put the birth bank list in rule content.

Dependency flag, carried from triage v1.1 U1: such a successor may be a new architecture family or need a protected controller. Both need explicit approval. Consult #25 also says "Do not automatically build a successor."

## 6. Q-tag separation

| Tag | Effect of this audit |
| --- | --- |
| Q-EXIST | Narrows the *statement* of the bounded production-closure claim (§5). No new evidence; a definitional reclassification only. |
| Q-CAUSE | Unchanged. Ablation dependence (AC10/91/92), W-gating (F3) and observer-discard (F4) results stand as measured. Their interpretation changes, as consult #25 says for F3: refusal at W=0 shows the gate matters, not that the sequence is internally constituted. |
| Q-LEARN | Not addressed. No acquisition claim is made. |
| Q-NECESSITY | Not addressed. No minimality claim is made. |

## 7. Does U3 (content-to-machinery loop) change the revised sentence?

**No, not under the current code.**
- U3 asks whether a content intervention changes the production or repair of enabling machinery, which then changes regenerated content (triage v1.1 U3).
- In the audited code, every machinery-repair and regeneration path runs through I7 and I10, which are supplied coordination. A positive U3 would show that content changes the *amount or timing* of repair delivered *through* those fixed policies. It would not place any sequence, switching condition or repair policy in declared state. A negative U3 removes nothing the revised sentence relies on.
- So U3 bears on a separate O3 claim (informational/functional organization, Q-CAUSE), not on the I4e/I5/I6/I7/I10/I13 violations that limit the closure sentence.
- **Exception.** If a future protocol first moved the coordination into declared state (§5), a U3-style loop running through that declared table *would* bear on the closure sentence. That ordering follows consult #25: U1 first, then U3 only if it would change a named conclusion.

## 8. Open items for Astra (no run implied)

- **Q-A1.** Confirm the step-level split: the operations of COPY, VERIFY, SWITCH and REMOVE are SUBSTRATE, and their order (I4e) is the violation.
- **Q-A2.** Rule on I12 (`ac9.py:L108@6c6323b`): is "birth into every demanded bank" generic chemistry or a supplied production priority?
- **Q-A3.** Confirm that format restrictions (fixed rule width, first-match semantics, bank rules forced `enabled=1`) count as generic syntax under T1.

## 9. Integrity

- Check script: `/workspace/scratch/u1_audit/check_u1_audit.py`. It confirms:
  - the three rule quotations are byte-exact substrings of the consult file;
  - every `path:L…@commit` citation exists at that commit, its line range is in bounds, and its lines contain a declared anchor string;
  - every cited code blob is identical at `master` and `db0ef2f`;
  - forbidden claim phrases are absent;
  - the earlier review files' hashes are unchanged.
- Earlier files (unchanged):
  - `track_a_lineage_triage_v1.md` `b4e1a772…`
  - `track_a_lineage_triage_v1_1.md` `d2cc9152…`
  - `track_a_lineage_triage_v1_1_astra_digest.md` `d4034423…`
  - `wrel_results_review_v1.md` `60c3f5a9…`
