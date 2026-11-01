# U1 substrate audit v1.2: applying the consult #25 substrate rule to the AC lineage code

**v1.2 (2026-10-21, about 2:22–3 PM ET).** Built from v1.1 (`u1_substrate_audit_v1_1.md`, sha256 `3d9bbde3644e15d81f2489c15cd6b68c07c93590097c95ef959b79758cd96373`, left unchanged) by `/workspace/scratch/u1_audit/v1_2/build_audit_v1_2.py`. It applies Astra consult #29 `/workspace/astra_consult29_response.txt` (sha256 `38056d5597fa3f8b077b7ed5b89c4cd64ea58ec1d6632b7d3d10c8936b352ce8`). Paper only. Nothing was executed except read-only `git fetch`/`git show`, `sha256sum`, `grep` and document checks, including one read-only parse of stored output rows (§4.2). Changes are listed in §11.

**Track A status (Astra #29 edit E29-6, verbatim):**
> "The original W-REL verification gap has been closed. Exploratory A2 attained the reference conjunction at (1/100,3/50), T_SEP=3 and 4. Named controls at these settings remain unevaluated. This update changes neither Track A's closure verdict nor any C4 evidence or status row."

Astra #29's verdict on Track A (verbatim): "Track A: ACCEPT THE REVISED CLOSURE STATEMENT. Correct the stale W-REL status and distinguish the prior provisional birth-targeting judgment from any newly established code finding."

**Systems separation (v1.2/v1.4, per Astra #29).** The maintained-component (AC) lineage (AC1–AC105: closure, repair, succession; F1–F5, U1, U3) and the GRU-8 studies are separate systems. The GRU-8 studies are PRs #8–#10, together with the GRU-8 acquisition and transfer studies in PRs #5 and #7. Their findings do not jointly establish one organism, and no finding from one system is evidence about the other. Astra #29 (verbatim): "Keep findings from different systems separate. The maintained-component lineage and the GRU studies do not jointly establish a single integrated organism. "Bounded neural causal contribution at 8/10" should identify the separate GRU experiment and its declared conjunction." This audit concerns the AC lineage only.

**v1.1 (2026-10-21, about 12:11 PM–1 PM ET).** Built from v1 (`u1_substrate_audit_v1.md`, sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`, left unchanged) by `/workspace/scratch/u1_audit/v1_1/build_audit_v1_1.py`. It applies Astra consult #28 `/workspace/astra_consult28_response.txt` (sha256 `1df2fba3189a8217067dd4e13e0c3f5d4b22a25dc7aedabec85d7ee8bd8b96ed`): edits E28-1 and E28-2 verbatim, the firmer closure sentence, the T1 qualification, and the rulings on Q-A1–Q-A3. Paper only, under Aidan's planning approval. Nothing was executed except read-only `git show`, `sha256sum`, `rg` and document checks. Changes are listed in §10.

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
  - **Qualified in v1.1 (Astra #28, verbatim):** "Also qualify T1: constants are not inherently forbidden. Fixed reaction rates, instruction widths and numerical integration rules can be substrate. Their organizational role, not their being constants, decides the classification."
  - So a constant fails T1 only through its organizational role: what it selects, triggers, schedules or sequences. Examples are `DESC_TRIGGER` (I5) and `STREAK_N` (I13). Rule width, the replica count, the `_cap` coefficients and the decode format do not fail T1 merely by being constants.
- **T2 No hidden organization:** no organization-specific instruction, maintenance sequence, switching condition or repair policy lives in the operation's code or module constants instead of in declared state.
- **T3 Executes alternatives, failing ones included:** given any other *admissible* content (syntactically valid for the declared format), the operation executes it, including content that harms the organism. It does not consult or substitute the intended organization (e.g. `succ.encoded`).

**Classes.**
- **SUBSTRATE:** passes T1–T3.
- **DECLARED-STATE:** the item is content held in the organism's damageable, paid-maintained state (`traces` banks 0/1), not an operation.
- **EXTERNAL COORDINATION (violation):** an operation that fails T2. This means organization-specific sequencing, switching, targeting or repair held in supplied code.

**Primitive versus policy (Astra #28 edit E28-1, verbatim):**
> "SUBSTRATE classifications apply to generic copy, compare, addressed write and erase primitives. They do not automatically cover the cited routines' source selection, destination selection, preconditions, budgets, scheduling or next-phase assignments. Each such choice is classified separately."

Applied in §3: each routine is split into its primitive (copy, compare, addressed write, erase) and the choices around it (source, destination, precondition, budget, schedule, next phase), and each part is classified separately.

**Declared system state** here means the maintained state named by the closure verdict: pointer, coordination (MODE, timer, RIP), route memory and decision state (`CLOSURE_VERDICT_v1.md:L38-L46@4b85851`). It also includes the component contents (description slots, program bits).

## 2. Which code the closure verdict rests on

- `CLOSURE_VERDICT_v1.md` evaluates the AC105 reference architecture at `db0ef2f`.
- AC105 builds its step from `ac95.build` with the `gated` arm configuration (`ac105.py:L171-L177@8f0218a`; `ac95.py:L168-L170@a1b9759`). It then replaces the injected maintenance function with the AC104 persistent/budget builder (`ac105.py:L177-L178@8f0218a`).
- That builder is source surgery on `ac95.maintain`, executed in `ac95`'s namespace. So the operative `advance()` is `ac95.advance` (`ac104.py:L144-L157@343ba17`). `ac99.maintain` wraps `ac95.maintain` (`ac99.py:L267-L270@8e9ab4a`).
- The verdict names both disputed operations as supplied substrate: `CLOSURE_VERDICT_v1.md:L59-L70@4b85851` (J1) and `CLOSURE_VERDICT_v1.md:L96-L99@4b85851` (scope item 2).
- The verdict's description row cites "succession copy→verify→switch→remove (turnover)" as the description's production/replacement route (`CLOSURE_VERDICT_v1.md:L35@4b85851`). Its W row cites "action 6 birth" (`CLOSURE_VERDICT_v1.md:L32@4b85851`).

## 3. Classification table

v1.1 applies E28-1: the rows for I4a–I4d, I8, I9 and I12 now classify primitives and choices separately. "Primitive" means only the generic operation on an addressed target.

| # | Item | Citation | Executes alternative/failing admissible content? (from code) | Class |
| --- | --- | --- | --- | --- |
| I1 | `prog.choose` rule interpreter (generic first-match execution) | `ac5_program.py:L33-L41@6c6323b`; call site `ac9.py:L84@6c6323b` | **Yes** | **SUBSTRATE** |
| I2 | Majority-replica decode (`ac1.decode`, `read_slot`) | `ac1.py:L67-L68@6c6323b`; `ac95.py:L261-L263@a1b9759` | **Yes** | **SUBSTRATE** |
| I3 | `build_program` generic description→program decode | `ac95.py:L243-L253@a1b9759` | **Yes** for admissible content; inadmissible permutation → `None` | **SUBSTRATE** (decode) |
| I3r | Forced enablement of the bank rules (`encode_rule(1, m, a)`) | `ac95.py:L243-L253@a1b9759` | Content can change a bank rule's mask and action but cannot disable it | **DISCLOSED EXPRESSIVITY RESTRICTION** (Astra #28); whether it hard-wires an organization-specific action is open (§8) |
| I4 | `advance()` as a whole | `ac95.py:L607-L725@a1b9759` | Executes alternative *contents*; cannot execute any alternative *sequence* or targeting | **EXTERNAL COORDINATION** (via I4a-s–I4d-s, I4e, I5, I6) |
| I4a-p | COPY primitive: write a slot toward a given bit vector | `ac95.py:L341-L352@a1b9759` | **Yes** | **SUBSTRATE** |
| I4a-s | COPY choices: source = active slot, destination = `(source + 1) % SLOTS`, budget `SUCC_BUDGET` | `ac95.py:L652@a1b9759`; `ac95.py:L659-L664@a1b9759`; `ac95.py:L77@a1b9759` | **No.** Always selects the next slot | **EXTERNAL COORDINATION** (targeting policy) |
| I4b-p | Compare primitives: admissibility test and equality test | `ac95.py:L665-L676@a1b9759` | **Yes** for admissible content | **SUBSTRATE** |
| I4b-s | Comparison outcome authorizing the pointer/MODE transaction | `ac95.py:L673-L676@a1b9759` | **No** | **EXTERNAL COORDINATION** (part of I4e) |
| I4c-p | Atomic multi-field write (pointer + MODE) under one affordability test | `ac95.py:L476-L532@a1b9759` | **Yes** | **SUBSTRATE** |
| I4c-s | SWITCH choices: re-check precondition, target rule, next phase `PHASE_REMOVE` | `ac95.py:L677-L692@a1b9759`; `ac95.py:L510@a1b9759` | **No** | **EXTERNAL COORDINATION** |
| I4d-p | Erase primitive: write zeros toward an addressed slot | `ac95.py:L341-L352@a1b9759` | **Yes** | **SUBSTRATE** |
| I4d-s | REMOVE choices: always erase the previous active slot `(source - 1) % SLOTS`, then IDLE | `ac95.py:L717-L725@a1b9759` | **No** | **EXTERNAL COORDINATION** (policy) |
| I4e | **FIXED ORDER** IDLE→COPY→VERIFY→{SWITCH, back to COPY}→{REMOVE, back to COPY}→IDLE | `ac95.py:L89@a1b9759`, `ac95.py:L642@a1b9759`, `ac95.py:L663@a1b9759`, `ac95.py:L673-L676@a1b9759`, `ac95.py:L680-L681@a1b9759`, `ac95.py:L510@a1b9759`, `ac95.py:L720-L721@a1b9759` | **No.** No state content can express a different order | **EXTERNAL COORDINATION** |
| I4f | Phase value, pointer, ACTIVE bit (what I4e reads) | `ac95.py:L85-L88@a1b9759`; `ac95.py:L291-L296@a1b9759` | n/a (content) | **DECLARED-STATE** |
| I5 | Succession start/switching condition (`succ_trigger`, `rate_ok`) | `ac95.py:L735@a1b9759`; `ac95.py:L76-L80@a1b9759`; `ac95.py:L635@a1b9759`; `ac95.py:L638-L650@a1b9759` | **No.** The thresholds play an organizational (switching) role | **EXTERNAL COORDINATION** |
| I6 | Timer/RIP update rule (reset on start, +1 per `TIMER_K`, clear RIP at 0) | `ac95.py:L611-L623@a1b9759`; `ac95.py:L428-L473@a1b9759`; `ac95.py:L101-L103@a1b9759`; `ac95.py:L309-L327@a1b9759` | **No** for the rule | **EXTERNAL COORDINATION** (rule); the counter and RIP bits are **DECLARED-STATE** |
| I7 | `maintain()` schedule and its host injection before every action | `ac95.py:L729-L748@a1b9759`; `ac95.py:L836-L837@a1b9759`; `ac105.py:L177-L178@8f0218a`; `ac99.py:L267-L270@8e9ab4a` | **No.** No program content can omit, reorder or retime it | **EXTERNAL COORDINATION** |
| I8 | Majority-restore primitives (`reg_description_active`, `reg_pointer`, `reg_ctrl`) | `ac95.py:L536-L577@a1b9759` | **Yes.** Restores toward the *current* majority | **SUBSTRATE** (primitive only); which registers, when and with what budget are I7 |
| I9 | `reg_from_active` (rewrite program bits from the active description) | `ac95.py:L580-L594@a1b9759` | **Yes** for content | **SUBSTRATE** (primitive only); trigger, budget and excluded offsets are I10 |
| I10 | Regeneration trigger, persistent trigger, budget rule, exclusion list | `ac95.py:L734@a1b9759`; `ac104.py:L144-L157@343ba17`; `ac103.py:L98-L112@3c89857`; `ac104.py:L118-L123@343ba17`; `ac104.py:L87@343ba17`; `ac105.py:L166-L167@8f0218a` | **No** | **EXTERNAL COORDINATION** |
| I11 | W-catalysed affordability gate (`_cap`, atomic MODE gate, combined switch gate) | `ac95.py:L336-L338@a1b9759`; `ac95.py:L369-L408@a1b9759`; `ac95.py:L476-L532@a1b9759` | **Yes**: content-blind | **SUBSTRATE** (named change 2: does not internalize I4e/I5/I7) |
| I12-p | Action execution primitives (route contact, renewal, `birth` into an addressed bank, `ac4.react`) | `ac9.py:L85-L112@6c6323b`; `ac9.py:L42-L49@6c6323b` | **Yes** | **SUBSTRATE** |
| I12 | **Birth targeting**: action 6 births into bank 0 plus every memory bank with demand | `ac9.py:L108@6c6323b`; `ac9.py:L106-L111@6c6323b`; `ac9_memory.py:L26-L27@6c6323b` | **No.** The target list is fixed by the host; content cannot redirect it | **EXTERNAL COORDINATION (supplied targeting), PROVISIONAL** (v1.2). This was Astra #28's provisional judgment on the supplied description. The code evidence is this audit's own, in §4.2; it is not an Astra code certification. v1 had this as SUBSTRATE, contested |
| I13 | Relinquishment/allocation policy (`STREAK_N`, drop, reserve release) | `ac99_d2.py:L128-L159@8e9ab4a`; `ac12.py:L52@5b06281` | **No** | **EXTERNAL COORDINATION**; the Gray streak counter (`ac99_d2.py:L76-L116@8e9ab4a`) is **DECLARED-STATE** |
| I14 | Observation map, conservation balance | `ac9.py:L52@6c6323b`; `ac9.py:L113@6c6323b` | **Yes**: content-blind | **SUBSTRATE** |
| I15 | Program and description content (including the five fixed rule words) | `ac95.py:L71@a1b9759`; `ac5_program.py:L22-L30@6c6323b` | n/a (content) | **DECLARED-STATE** (inherited content is permitted per the verdict) |

**Counts (v1.1).**
- **SUBSTRATE: 12.** I1, I2, I3, I4a-p, I4b-p, I4c-p, I4d-p, I8, I9, I11, I12-p, I14. I8, I9 and I12-p are primitives only.
- **EXTERNAL COORDINATION: 11.** I4a-s, I4b-s, I4c-s, I4d-s, I4e, I5, I6 rule, I7, I10, I12 (supplied targeting, PROVISIONAL), I13 policy. I4 as a whole is also EXTERNAL COORDINATION.
- **DECLARED-STATE: 2 whole items** (I4f, I15), plus the counter and RIP bits in I6 and the Gray streak in I13.
- **DISCLOSED EXPRESSIVITY RESTRICTION: 1** (I3r).

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
- Caveat on T1 (revised in v1.1 as I3r): bank rules are always encoded with `enabled=1`, so the format cannot express a disabled bank rule. Astra #28 (verbatim): "However, forced enablement of designated bank rules must be disclosed as an expressivity restriction. It cannot be classified as harmless syntax solely because other fields remain mutable. The question is whether it hard-wires an organization-specific action that declared content cannot suppress or redirect."
  - From the code: masks and actions are read from the description (`read_masks`, `read_actions`), so content can redirect a bank rule's action but cannot disable the rule.
  - Whether that hard-wires an organization-specific action is left open (§8).

**I4 `advance()`: EXTERNAL COORDINATION (as a whole).**
- It is not a generic interpreter. It is a hand-coded state machine whose branch structure is the succession procedure (`ac95.py:L607-L725@a1b9759`).
- In consult #25's words, "calling a function an interpreter is insufficient". Each step's *operation* is classified separately below. The violation sits in the fixed order (I4e), the start condition (I5) and the timer coupling (I6).

**I4a COPY: primitive SUBSTRATE (I4a-p); source, destination and budget EXTERNAL COORDINATION (I4a-s).**
- It reads the source slot's majority and writes it toward the target slot under `SUCC_BUDGET` and `_cap` (`ac95.py:L659-L664@a1b9759`; `ac95.py:L341-L352@a1b9759`).
- It copies whatever the source holds, valid or not and correct or not; the write primitive is generic transport.
- v1.1 (E28-1): the destination `(source + 1) % SLOTS` (`ac95.py:L652@a1b9759`) and the budget are choices. Astra #28: "Always selecting the next description slot is a targeting policy."

**I4b VERIFY: compare primitives SUBSTRATE (I4b-p); outcome-authorizes-transaction EXTERNAL COORDINATION (I4b-s).**
- It computes `valid = build_program(tgt_maj) is not None` and `correct = tgt_maj == src_maj` (`ac95.py:L665-L676@a1b9759`).
- Both tests are generic: syntactic admissibility (I3) and copy fidelity against the organism's *own* source.
- An admissible but harmful description passes and proceeds. `succ.encoded` (the intended description) is written only into observer fields (`target_correct`) and never branches the organism (`ac95.py:L645-L658@a1b9759` shows the only reads of `succ._entry`; in the `gated`/`timer_maintained` arm they only create log entries).
- What happens *after* the test (go to SWITCH, or back to COPY) belongs to I4e. Astra #28: "Making a successful comparison authorize this particular pointer/MODE transaction is organizational coordination unless represented in declared content."

**I4c SWITCH: atomic write primitive SUBSTRATE (I4c-p); precondition, target and next phase EXTERNAL COORDINATION (I4c-s).**
- It re-checks equality and admissibility, then `commit_switch` writes the pointer to `target` and the MODE word atomically under one W-cap affordability test (`ac95.py:L677-L692@a1b9759`; `ac95.py:L476-L532@a1b9759`).
- It would switch to any admissible copy, harmful ones included. The atomic multi-field write is a generic transaction primitive.
- Not generic: the hard-coded next phase `encode_ctrl(1, PHASE_REMOVE, last)` (`ac95.py:L510@a1b9759`) and the target rule `(source + 1) % SLOTS`. Both are assigned to I4e.

**I4d REMOVE: erase primitive SUBSTRATE (I4d-p); choice of slot and timing EXTERNAL COORDINATION (I4d-s).**
- It writes zeros toward the slot before the current pointer, then sets IDLE once that slot is empty (`ac95.py:L717-L725@a1b9759`).
- It erases whatever is there, which is generic. Which slot to erase (`old_source = (source - 1) % SLOTS`) and when are choices. Astra #28: "Automatically erasing the previous active slot is a policy."

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

**I8 Majority-restore primitives: SUBSTRATE (primitive only).**
- They write replicas toward their current majority under `_cap` (`ac95.py:L536-L577@a1b9759`).
- They are content-blind. A damaged-majority (failing) value is preserved, not corrected to an intended value, so T3 holds.
- *When* they fire is I7.

**I9 `reg_from_active`: SUBSTRATE (primitive only).**
- It writes program bits toward `build_program(read_slot(active))`, skipping host-supplied offsets (`ac95.py:L580-L594@a1b9759`).
- It is generic decode plus write, and it would install a harmful but admissible description's program.
- Its trigger, budget and exclusion list are I10.

**I10 Regeneration policy: EXTERNAL COORDINATION.**
- The parts:
  - the regeneration trigger (`ac95.py:L734@a1b9759`);
  - the persistent trigger `program_incomplete` (`ac103.py:L98-L112@3c89857`), spliced in by source surgery (`ac104.py:L144-L157@343ba17`);
  - the budget rule `max(0, material - allowance)` with `DECISION_ALLOWANCE = STREAK_N * 7` (`ac104.py:L118-L123@343ba17`; `ac104.py:L87@343ba17`);
  - the exclusion list `reg_offs + streak_offs`, computed by the host at acquisition (`ac105.py:L166-L167@8f0218a`).
- These are repair policy and resource-priority policy in supplied code and constants.

**I11 W-catalysed gate: SUBSTRATE.**
- `_cap = min(32, 8·W, energy, material)`, the all-or-nothing MODE write, and the combined switch gate (`ac95.py:L336-L338@a1b9759`; `ac95.py:L369-L408@a1b9759`; `ac95.py:L476-L532@a1b9759`) are content-blind resource laws.
- Named change 2 applies: the gate makes the sequence *depend on* produced machinery. It does not place the sequence in declared state.

**I12 Action semantics: primitives SUBSTRATE (I12-p); birth targeting EXTERNAL COORDINATION (supplied targeting), PROVISIONAL (v1.2, §4.2).**
- The step executes the program-chosen action: route contacts (0/1), renewals (3/4), action 6 births, and everything else through `ac4.react` (`ac9.py:L85-L112@6c6323b`). The primitives execute any chosen action, harmful ones included (I12-p).
- v1 had marked the bank-selection line `ac9.py:L108@6c6323b` as contested. Astra #28 rules (verbatim): "For `ac9.py:108`, "every bank with demand" is not necessarily a priority ordering. It is a supplied production-targeting rule. On the description provided, I would not clear it as generic chemistry yet."
- v1.1 therefore classified I12 as **EXTERNAL COORDINATION (supplied targeting)**. The code-level explanation is in §4.1.
- v1.2: the classification is **PROVISIONAL**. Astra #29 says its #28 judgment rested on the supplied description. §4.2 states exactly what this audit's own code reading shows and does not show.

**I13 Relinquishment policy: EXTERNAL COORDINATION (policy); DECLARED-STATE (Gray streak).**
- The streak counter lives in maintained bits (`ac99_d2.py:L76-L116@8e9ab4a`).
- The policy is a host-class method with supplied threshold and branch structure (`ac99_d2.py:L128-L159@8e9ab4a`; `ac12.py:L52@5b06281`): reset on productive contact, increment otherwise, drop at `STREAK_N = 6`, reserve-release conditions.
- This bears on the verdict's "decision state" maintained-state row. It does not bear on any C1–C5 production edge.

**I14 Observation and conservation: SUBSTRATE.**
- The observation map (`ac9.py:L52@6c6323b`) and the inventory balance (`ac9.py:L113@6c6323b`) are content-blind, supplied world laws. The verdict lists observation and conservation as supplied (`CLOSURE_VERDICT_v1.md:L96-L99@4b85851`).

**I15 Program and description content: DECLARED-STATE.**
- The five fixed rule words (including W/C/B births via actions 6/7/8) are *content* (`ac95.py:L71@a1b9759`; `ac5_program.py:L22-L30@6c6323b`). They sit in damageable description and program bits and are executed by I1/I3.
- That content is inherited, which the verdict permits (§3 item 5).

### 4.1 Birth targeting at `ac9.py:L108@6c6323b` (code-level explanation)

**What the code does.** Action 6 is the W-birth action (`ac9.py:L106-L111@6c6323b`):

```python
elif action==6:
    b.energy-=1; e['active']=1; e['spent_e']+=1
    banks=[0]+[r+1 for r,n in enumerate(o.memory.demand()) if n>0]
    for bank in banks:
        parents=np.flatnonzero(a[bank*4:bank*4+4])
        if len(parents): birth(b,bank,bank*4+int(parents[0]),e)
```

`demand()` is `self.occupied().sum(axis=(1,2,3)).astype(int)` (`ac9_memory.py:L26-L27@6c6323b`). It counts the live replica sites in each of the two memory regions. `birth` (`ac9.py:L42-L49@6c6323b`) finds the first empty constituent slot among the four in the addressed bank (`b.life[bank*4:bank*4+4]==0`) and pays 4 energy and 2 material through `ac4.pay(b,e,4,2)`. It then gives the new constituent lifetime 64 at its parent's position.

**Which banks receive births, and why.**
- Bank 0 is always in the list.
- Bank r+1 is added for each memory region r that has at least one occupied site, "every bank with demand".
- A bank receives a birth only if it still has a living parent constituent (`parents`) and the payment succeeds.
- Banks are served in list order (0, then 1, then 2). When energy or material runs short, the earlier banks are paid first, so the list also acts as an implicit priority under scarcity.
- The "why" lives in the host, not in the organism: the code decides that bank 0 always needs W and that a region with any stored entry needs it too.

**Why Astra classifies it as supplied targeting.**
- The program chooses only *whether* to fire action 6. *Where* the births go is computed by the host from a semantic designation (bank 0 as privileged; memory regions as demand-bearing) and from a host-side count of the memory array.
- Astra #28 (verbatim): "A host operation identifying the program bank and every semantically designated memory bank, then distributing births to them, supplies organizational targeting."
- Astra #28 contrasts this with "A generic reaction acting on declared local substrates, receptors or demand markers can be substrate."
- No declared content can remove bank 0, add a different bank, change the threshold `n>0`, or reorder the service order, and Astra asks for exactly these to be shown: "Show what "demand" reads, where it is represented, how targeting changes when that content changes, and how resource competition is resolved."
- From the code: demand reads occupancy (`life>0`) of the memory replicas. Occupancy is declared state, but the mapping from it to targets is not. Targeting changes only through occupancy, never through content that encodes the targeting itself. Competition is settled by host list order.

**What would make it declared state (SKETCH ONLY, not a proposal).**
- Each bank would carry a declared, damageable demand marker or receptor that a generic birth reaction reads locally, with no host list.
- The service order and thresholds would sit in maintained content, or competition would be handled by a generic law, for example proportional allocation.
- Altered markers, including harmful ones, would redirect births without host restoration.
- Bank 0's inclusion would itself be marker content.

Building or testing this needs separate, concrete approval (Astra #28).

### 4.2 Status of the I12 judgment (v1.2): PROVISIONAL

**Astra #29 (verbatim):** "My #28 birth-targeting judgment was provisional on the supplied description. If audit v1.1 now establishes that the implementation performs semantic host targeting, cite that new evidence. Do not describe #28 alone as an unconditional code certification. I cannot certify the unavailable audit's new details from this synthesis."

So I12 is **PROVISIONAL**, and Astra #28 is not cited here as a code certification. The evidence below is this audit's own read-only reading of the code at the cited commits, plus one parse of stored output rows. Astra has not reviewed it.

**What the code shows.**
1. **The AC105 step runs `ac9.step`'s source with this line unchanged.**
   - `STEP_SRC=inspect.getsource(ac9.step)` (`ac12.py:L64@5b06281`). `ac95.build` compiles that source (`ac95.py:L817-L840@a1b9759`), and AC105 uses it (`ac105.py:L177-L178@8f0218a`).
   - `build` replaces exactly five named strings: the renewal block, the outcome line, the damage line, the action line and the balance line. None is the bank-list line, so `ac9.py:L108@6c6323b` runs unchanged on the AC105 path.
2. **The step intercepts action 6 before the generic reaction** (`ac9.py:L85-L112@6c6323b`, with the `ac4.react` fallback at line 112).
   - The generic `ac4.react` action-6 branch treats every group alike: `groups=range(4) if action==6 else [4]` (`ac4.py:L97-L98@6c6323b`).
   - `ac9` replaces that uniform rule with a host list: bank 0 always, bank r+1 only when memory region r has an occupied site, and bank 3 never.
3. **Other host code ties bank indices to functional roles.**
   - W group `4*bank`…`4*bank+3` catalyses repair of `traces[bank]` (`ac4.py:L89-L92@6c6323b`).
   - W group r+1 catalyses renewal of memory region r, through `a[4*(r+1):4*(r+2)]` (`ac12.py:L67-L69@5b06281`).
   - `traces[0,:126]` holds the program (`ac12.py:L80@5b06281`). In AC105, `traces[1]` holds the description (`ac105.py:L169@8f0218a`).
4. **`demand()` on the AC105 path is the `ac9_memory` method** (`ac9_memory.py:L26-L27@6c6323b`). The AC105 organism comes from `ac12.acquire` (`ac105.py:L161@8f0218a`), which calls `ac9_priority_v2.acquire` (`ac12.py:L94-L107@5b06281`). That calls `ac9.acquire` (`ac9_priority_v2.py:L11-L15@6c6323b`), which builds `mem.Memory.empty()` (`ac9.py:L23-L26@6c6323b`), with `mem` = `ac9_memory` (`ac9.py:L9@6c6323b`).

**What this establishes.** The bank list is written in host code, not in declared content. It decides which functional W groups receive births: the program-repair group always, and the memory-renewal groups when memory is occupied. In that limited, code-level sense the implementation performs semantic host targeting.

**What the code does not show.**
- **Necessity.** It does not show that this targeting is necessary for any reported W/C/B result. That is a Q-NECESSITY question; only a run could settle it (NEEDS-APPROVED-RUN). No run is proposed, because Astra #28 directs no further closure runs on the unchanged architecture.
- **Intent.** It does not document the designers' intent. "Semantic" here means the functional roles that other code assigns to each bank index.
- **A role mismatch, noted but not assessed.** In AC105, the bank-1 W group also catalyses repair of the description trace (`traces[1]`). Yet bank-1 births are triggered by memory-region-0 occupancy, not by any description state.
- **Where bank-1 parents come from.** `ac9.acquire` zeroes `life[4:16]`, and every birth needs a living parent in the same bank. The path that later populates bank 1 was not traced.
- **The per-bank split in AC105.** Stored AC95 rows (`ac95_results_v1/rows.jsonl` @ `a1b9759`, 136 rows) record 174978 W births: 87394 in bank 0, 87584 in bank 1 (region 0) and 0 in bank 2 (region 1). AC105 rows (`ac105_results_v1/rows.jsonl` @ `8f0218a`) do not store per-bank birth counts, so the AC105 split is UNVERIFIED.

## 5. Revised closure sentence

**Closure sentence (v1.1, verbatim from Astra #28; replaces the v1 sentence, which is withdrawn).**

> The audited system exhibits the reported component-production, repair and reconstruction behavior under supplied organizational coordination. Under the adopted substrate rule, production closure of the full declared network is not established.

**Astra #28 edit E28-2 (verbatim):**
> "The audited system exhibits the reported component-production, repair and reconstruction behavior under supplied organizational coordination. Under the adopted substrate rule, production closure of the full declared network is not established. The birth-targeting rule remains an explicit qualification on the W/C/B production claim."

**Scope notes (Astra #28, verbatim).**
- "Retain the individual empirical findings with their original scope. Do not automatically re-certify all C1-C5 criteria for W/C/B through this code-reading exercise."
- Astra's reason for the firmer wording: "The revised closure sentence is directionally correct but still overstates the W/C/B clause while birth targeting remains contested. It also risks preserving the headline through "closure holds conditional on external coordination.""

**Directive (Astra #28, verbatim):** "Stop further closure experiments on that unchanged architecture." "Further runs on the unchanged architecture will not resolve that structural limitation."

**What would move each violating item into declared state: SUCCESSOR DESIGN, SKETCH ONLY, NOT A PROPOSAL.** Astra #28 (verbatim): "My recommendation is to close the present Track A claim and retain a short successor design sketch. Do not build the successor automatically." "Implementation and testing require a separate, concrete approval. A protected controller is not inherently necessary." Its planning-only note: "It does not authorize a hand-built simulation, online adaptation, an HRL comparison run or a Track A architectural successor."

Nothing below was designed in detail or executed. Astra #28 adds that "A damageable transition table is a plausible successor design, but moving Python branches into an array is insufficient.", and that the successor must account for (verbatim):
- "Production, copying, repair and replacement of the table itself."
- "Its triggers, addressing rules, budgets and exclusions."
- "The mechanism that schedules its execution."
- "Bootstrapping and inherited initial content."
- "Whether corrupted but admissible tables execute without host restoration of the intended policy."
- "Any protected interpreter state or hidden backup."
- "An inherited initial table is compatible with the declared convention. An indefinitely protected host copy that reinstalls it would preserve the problem."

Sketch items:
- **I4e fixed order.** Represent the phase-transition table as content in a maintained, damageable, paid-repaired register: for example (current phase, test outcome) → (next phase, operation code). A generic table-driven step executes whatever table is present.
  - Admissibility check: the step must execute alternative tables (skip-verify, reversed switch/remove, a different target rule) and let them fail, without falling back to the intended order.
  - Repeat interruption, machinery-only rescue and observer-discard (F3/F4) on that version.
- **I5 start condition.** Hold `DESC_TRIGGER` and the "timer full" requirement as maintained parameters (or table entries), read by a generic comparator. Damage to them must be able to change when succession fires.
- **I6 timer/RIP rule.** Express reset-on-start and increment-per-period as table operations on the existing counter and RIP bits. Keep the W gate (it remains substrate).
- **I7 maintenance schedule.** Remove the unconditional host call. Either make the maintenance operations actions that program rules select from observation bits exposing minority counts (executed by I1), or drive them from the I4e-style declared table. Program content must be able to omit or reorder maintenance and suffer the consequence.
- **I10 regeneration policy.** Hold the trigger, the budget allowance and the protected-offset list as declared content. The host must not resolve the protected offsets once at acquisition.
- **I13 relinquishment policy.** Hold `STREAK_N` and the drop/reserve conditions as declared content executed by a generic counter-compare-act step (the streak counter already is declared state).
- **I12 birth targeting** (classified supplied targeting, PROVISIONAL; §4.2): declared, damageable demand markers read by a generic birth reaction (§4.1 sketch).
- **I4a-s/I4c-s/I4d-s choices:** the source, destination and erase-target rules become table or marker content, under the same table sketch.

Dependency flag (updated per Astra #28): "This would be a material architectural change. Whether the project calls it a new "family" depends on its architecture taxonomy; that terminology should not determine authorization." A protected controller is not inherently necessary. Consult #25 also says "Do not automatically build a successor."

## 6. Q-tag separation

| Tag | Effect of this audit |
| --- | --- |
| Q-EXIST | Replaces the closure statement with Astra #28's firmer sentence (§5). No new evidence; a definitional reclassification only. The birth-targeting rule qualifies the W/C/B production claim (E28-2). C1–C5 criteria are not re-certified here. |
| Q-CAUSE | Unchanged. Ablation dependence (AC10/91/92), W-gating (F3) and observer-discard (F4) results stand as measured. Their interpretation changes, as consult #25 says for F3: refusal at W=0 shows the gate matters, not that the sequence is internally constituted. |
| Q-LEARN | Not addressed. No acquisition claim is made. |
| Q-NECESSITY | Not addressed. No minimality claim is made. |

## 7. Does U3 (content-to-machinery loop) change the revised sentence?

**No, not under the current code.**
- U3 asks whether a content intervention changes the production or repair of enabling machinery, which then changes regenerated content (triage v1.1 U3).
- In the audited code, every machinery-repair and regeneration path runs through I7 and I10, which are supplied coordination. A positive U3 would show that content changes the *amount or timing* of repair delivered *through* those fixed policies. It would not place any sequence, switching condition or repair policy in declared state. A negative U3 removes nothing the revised sentence relies on.
- So U3 bears on a separate O3 claim (informational/functional organization, Q-CAUSE), not on the I4e/I5/I6/I7/I10/I13 violations that limit the closure sentence.
- **Exception.** If a future protocol first moved the coordination into declared state (§5, sketch only), a U3-style loop running through that declared table *would* bear on the closure sentence. That ordering follows consult #25: U1 first, then U3 only if it would change a named conclusion.
- **Astra #28 (verbatim):** "Keep U3 on hold unless its separate content-to-machinery causal claim is independently worth pursuing. U3 cannot internalize a schedule by demonstrating stronger dependence on it."

## 8. Astra items: rulings from consult #28, and what remains open

- **Q-A1 (step split): ruled too narrow.** Astra #28: "The primitive/policy distinction is right, but "the four steps are substrate, and only their order violates the rule" is too narrow." Applied as E28-1 (§1, §3).
- **Q-A2 (I12 birth targeting): provisional judgment (Astra #28, on the supplied description).** I12 is classified EXTERNAL COORDINATION (supplied targeting), PROVISIONAL (§3, §4.1, §4.2). Astra #29: "Do not describe #28 alone as an unconditional code certification." E28-2 keeps it as an explicit qualification on the W/C/B production claim.
- **Q-A3 (format): partly ruled.** Astra #28: "Fixed rule width, first-match interpretation and a fixed instruction vocabulary can be admissible syntax. A system need not have a universal programming language." Forced enablement is disclosed as an expressivity restriction (I3r).
- **Open (paper only).** Does the forced enablement in I3r hard-wire an organization-specific action that declared content cannot suppress or redirect? From the code, content can redirect the action field, but cannot disable the rule.

## 9. Integrity

- v1.2 check script: `/workspace/scratch/astra29/check_e29.py` (log `check_e29.log`). It covers this file, triage v1.4 and synthesis v1.2. §11 lists what it checks.
- The v1.1 description below is retained.

- Check script: `/workspace/scratch/u1_audit/v1_1/check_v1_1.py`, which covers all three v1.1/v1.3 files. It checks:
  - every Astra #25/#28 quotation is a byte-exact substring of its consult file;
  - the closure sentence is byte-identical across the three files, and the v1 sentence is absent;
  - every `path:L…@commit` citation exists, is in range and contains a declared anchor;
  - every cited code blob is identical at master and `db0ef2f`;
  - forbidden phrases are absent;
  - prior versions are unchanged.
- Prior files (unchanged):
  - `u1_substrate_audit_v1.md` `48c174f5…`
  - `track_a_lineage_triage_v1.md` `b4e1a772…`
  - `track_a_lineage_triage_v1_1.md` `d2cc9152…`
  - `track_a_lineage_triage_v1_2.md` `84fa9614…`
  - `track_a_claim_synthesis_v1.md` `95888230…`
  - `wrel_results_review_v1.md` `60c3f5a9…`

## 10. Changes in v1.1

1. E28-1 and E28-2 are added verbatim. The table splits primitives from choices, so SUBSTRATE now covers primitives only.
2. The closure sentence is replaced by Astra #28's sentence. The v1 sentence is withdrawn, and C1–C5 criteria for W/C/B are not re-certified here.
3. T1 is qualified per Astra #28: constants are judged by their organizational role.
4. I12 changes from contested to EXTERNAL COORDINATION (supplied targeting), with a code-level explanation in §4.1. Forced bank-rule enablement is disclosed as I3r.
5. The directives are recorded: no further closure runs on the unchanged architecture; the successor table design is SKETCH ONLY, not a proposal; U3 stays on hold.

## 11. Changes in v1.2 (Astra #29)

1. **E29-6 added verbatim,** with Astra #29's Track A verdict. This audit has no W-REL entries to replace.
2. **I12 marked PROVISIONAL** (§3, §4, §8). The new §4.2 sets out what the code itself shows and does not show, and Astra #28 is not cited as a code certification.
3. **Systems separation stated:** the AC lineage and the GRU-8 studies are separate systems and do not jointly establish one organism.
4. **Wording.** The three non-test uses of "resolved by" now read "computed by" (I10 exclusion list), "settled by" (§4.1, resource competition) and "handled by" (§4.1 sketch). This file has no proposed tests that used "resolved by".
5. **Unchanged:** the closure sentence, E28-1 and E28-2.

The check script `/workspace/scratch/astra29/check_e29.py` confirms:
- verbatim Astra #29 quotes;
- citations;
- no "resolved by" outside quotes;
- no UNRESOLVED-COMPUTE or attainability-check text outside the changelog and quotes;
- the closure sentence is byte-identical across the three files;
- forbidden phrases are absent;
- earlier versions are unchanged.
