import hashlib, sys
sys.path.insert(0,'/workspace/scratch/u1_audit/v1_1'); from common import *
SRC='/workspace/review/u1_substrate_audit_v1.md'; DST='/workspace/review/u1_substrate_audit_v1_1.md'
raw=open(SRC,'rb').read(); assert hashlib.sha256(raw).hexdigest()=='48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a'
s=raw.decode()
def rep(a,b,n=1):
    global s; c=s.count(a); assert c==n,(c,a[:70]); s=s.replace(a,b)
def between(a,b,new):
    global s; i=s.index(a); j=s.index(b,i); s=s[:i]+new+s[j:]

rep("# U1 substrate audit v1: applying the consult #25 substrate rule to the AC lineage code\n",
f"""# U1 substrate audit v1.1: applying the consult #25 substrate rule to the AC lineage code

**v1.1 (2026-10-21, about 12:11 PM–1 PM ET).** Built from v1 (`u1_substrate_audit_v1.md`, sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`, left unchanged) by `/workspace/scratch/u1_audit/v1_1/build_audit_v1_1.py`. It applies Astra consult #28 {C28}: edits E28-1 and E28-2 verbatim, the firmer closure sentence, the T1 qualification, and the rulings on Q-A1–Q-A3. Paper only, under Aidan's planning approval. Nothing was executed except read-only `git show`, `sha256sum`, `rg` and document checks. Changes are listed in §10.
""")

# §1: T1 qualification + E28-1
rep("""- **T1 Generic:** the operation implements generic transformation, transport, execution or integration. It contains no constant or control flow specific to this organization.""",
f"""- **T1 Generic:** the operation implements generic transformation, transport, execution or integration. It contains no constant or control flow specific to this organization.
  - **Qualified in v1.1 (Astra #28, verbatim):** {T1Q}
  - So a constant fails T1 only through its organizational role: what it selects, triggers, schedules or sequences. Examples are `DESC_TRIGGER` (I5) and `STREAK_N` (I13). Rule width, the replica count, the `_cap` coefficients and the decode format do not fail T1 merely by being constants.""")
rep("""- **EXTERNAL COORDINATION (violation):** an operation that fails T2. This means organization-specific sequencing, switching or repair held in supplied code.""",
f"""- **EXTERNAL COORDINATION (violation):** an operation that fails T2. This means organization-specific sequencing, switching, targeting or repair held in supplied code.

**Primitive versus policy (Astra #28 edit E28-1, verbatim):**
> {E1}

Applied in §3: each routine is split into its primitive (copy, compare, addressed write, erase) and the choices around it (source, destination, precondition, budget, schedule, next phase), and each part is classified separately.""")

# §3 table
between("## 3. Classification table","## 4. Per-item evidence",f"""## 3. Classification table

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
| I4e | **FIXED ORDER** IDLE→COPY→VERIFY→{{SWITCH, back to COPY}}→{{REMOVE, back to COPY}}→IDLE | `ac95.py:L89@a1b9759`, `ac95.py:L642@a1b9759`, `ac95.py:L663@a1b9759`, `ac95.py:L673-L676@a1b9759`, `ac95.py:L680-L681@a1b9759`, `ac95.py:L510@a1b9759`, `ac95.py:L720-L721@a1b9759` | **No.** No state content can express a different order | **EXTERNAL COORDINATION** |
| I4f | Phase value, pointer, ACTIVE bit (what I4e reads) | `ac95.py:L85-L88@a1b9759`; `ac95.py:L291-L296@a1b9759` | n/a (content) | **DECLARED-STATE** |
| I5 | Succession start/switching condition (`succ_trigger`, `rate_ok`) | `ac95.py:L735@a1b9759`; `ac95.py:L76-L80@a1b9759`; `ac95.py:L635@a1b9759`; `ac95.py:L638-L650@a1b9759` | **No.** The thresholds play an organizational (switching) role | **EXTERNAL COORDINATION** |
| I6 | Timer/RIP update rule (reset on start, +1 per `TIMER_K`, clear RIP at 0) | `ac95.py:L611-L623@a1b9759`; `ac95.py:L428-L473@a1b9759`; `ac95.py:L101-L103@a1b9759`; `ac95.py:L309-L327@a1b9759` | **No** for the rule | **EXTERNAL COORDINATION** (rule); the counter and RIP bits are **DECLARED-STATE** |
| I7 | `maintain()` schedule and its host injection before every action | `ac95.py:L729-L748@a1b9759`; `ac95.py:L836-L837@a1b9759`; `ac105.py:L177-L178@8f0218a`; `ac99.py:L267-L270@8e9ab4a` | **No.** No program content can omit, reorder or retime it | **EXTERNAL COORDINATION** |
| I8 | Majority-restore primitives (`reg_description_active`, `reg_pointer`, `reg_ctrl`) | `ac95.py:L536-L577@a1b9759` | **Yes.** Restores toward the *current* majority | **SUBSTRATE** (primitive only); which registers, when and with what budget are I7 |
| I9 | `reg_from_active` (rewrite program bits from the active description) | `ac95.py:L580-L594@a1b9759` | **Yes** for content | **SUBSTRATE** (primitive only); trigger, budget and excluded offsets are I10 |
| I10 | Regeneration trigger, persistent trigger, budget rule, exclusion list | `ac95.py:L734@a1b9759`; `ac104.py:L144-L157@343ba17`; `ac103.py:L98-L112@3c89857`; `ac104.py:L118-L123@343ba17`; `ac104.py:L87@343ba17`; `ac105.py:L166-L167@8f0218a` | **No** | **EXTERNAL COORDINATION** |
| I11 | W-catalysed affordability gate (`_cap`, atomic MODE gate, combined switch gate) | `ac95.py:L336-L338@a1b9759`; `ac95.py:L369-L408@a1b9759`; `ac95.py:L476-L532@a1b9759` | **Yes**: content-blind | **SUBSTRATE** (named change 2: does not internalize I4e/I5/I7) |
| I12-p | Action execution primitives (route contact, renewal, `birth` into an addressed bank, `ac4.react`) | `ac9.py:L85-L112@6c6323b`; `ac9.py:L42-L49@6c6323b` | **Yes** | **SUBSTRATE** |
| I12 | **Birth targeting**: action 6 births into bank 0 plus every memory bank with demand | `ac9.py:L108@6c6323b`; `ac9.py:L106-L111@6c6323b`; `ac9_memory.py:L26-L27@6c6323b` | **No.** The target list is fixed by the host; content cannot redirect it | **EXTERNAL COORDINATION (supplied targeting)**, per Astra #28 (§4.1). v1 had this as SUBSTRATE, contested |
| I13 | Relinquishment/allocation policy (`STREAK_N`, drop, reserve release) | `ac99_d2.py:L128-L159@8e9ab4a`; `ac12.py:L52@5b06281` | **No** | **EXTERNAL COORDINATION**; the Gray streak counter (`ac99_d2.py:L76-L116@8e9ab4a`) is **DECLARED-STATE** |
| I14 | Observation map, conservation balance | `ac9.py:L52@6c6323b`; `ac9.py:L113@6c6323b` | **Yes**: content-blind | **SUBSTRATE** |
| I15 | Program and description content (including the five fixed rule words) | `ac95.py:L71@a1b9759`; `ac5_program.py:L22-L30@6c6323b` | n/a (content) | **DECLARED-STATE** (inherited content is permitted per the verdict) |

**Counts (v1.1).**
- **SUBSTRATE: 12.** I1, I2, I3, I4a-p, I4b-p, I4c-p, I4d-p, I8, I9, I11, I12-p, I14. I8, I9 and I12-p are primitives only.
- **EXTERNAL COORDINATION: 11.** I4a-s, I4b-s, I4c-s, I4d-s, I4e, I5, I6 rule, I7, I10, I12 (supplied targeting), I13 policy. I4 as a whole is also EXTERNAL COORDINATION.
- **DECLARED-STATE: 2 whole items** (I4f, I15), plus the counter and RIP bits in I6 and the Gray streak in I13.
- **DISCLOSED EXPRESSIVITY RESTRICTION: 1** (I3r).

""")

# §4 edits
rep("""- Caveat on T1: bank rules are always encoded with `enabled=1`, so the format cannot express a disabled bank rule. That is a format restriction, not an organization-specific instruction.""",
"""- Caveat on T1 (revised in v1.1 as I3r): bank rules are always encoded with `enabled=1`, so the format cannot express a disabled bank rule. Astra #28 (verbatim): "However, forced enablement of designated bank rules must be disclosed as an expressivity restriction. It cannot be classified as harmless syntax solely because other fields remain mutable. The question is whether it hard-wires an organization-specific action that declared content cannot suppress or redirect."
  - From the code: masks and actions are read from the description (`read_masks`, `read_actions`), so content can redirect a bank rule's action but cannot disable the rule.
  - Whether that hard-wires an organization-specific action is left open (§8).""")
rep("**I4a COPY: SUBSTRATE.**","**I4a COPY: primitive SUBSTRATE (I4a-p); source, destination and budget EXTERNAL COORDINATION (I4a-s).**")
rep("- It copies whatever the source holds, valid or not and correct or not. It is generic transport.",
"- It copies whatever the source holds, valid or not and correct or not; the write primitive is generic transport.\n- v1.1 (E28-1): the destination `(source + 1) % SLOTS` (`ac95.py:L652@a1b9759`) and the budget are choices. Astra #28: \"Always selecting the next description slot is a targeting policy.\"")
rep("**I4b VERIFY: SUBSTRATE (as a test).**","**I4b VERIFY: compare primitives SUBSTRATE (I4b-p); outcome-authorizes-transaction EXTERNAL COORDINATION (I4b-s).**")
rep("- What happens *after* the test (go to SWITCH, or back to COPY) belongs to I4e.",
"- What happens *after* the test (go to SWITCH, or back to COPY) belongs to I4e. Astra #28: \"Making a successful comparison authorize this particular pointer/MODE transaction is organizational coordination unless represented in declared content.\"")
rep("**I4c SWITCH: SUBSTRATE (the write primitive).**","**I4c SWITCH: atomic write primitive SUBSTRATE (I4c-p); precondition, target and next phase EXTERNAL COORDINATION (I4c-s).**")
rep("**I4d REMOVE: SUBSTRATE.**","**I4d REMOVE: erase primitive SUBSTRATE (I4d-p); choice of slot and timing EXTERNAL COORDINATION (I4d-s).**")
rep("- It erases whatever is there, which is generic. Which slot to erase and when are I4e.",
"- It erases whatever is there, which is generic. Which slot to erase (`old_source = (source - 1) % SLOTS`) and when are choices. Astra #28: \"Automatically erasing the previous active slot is a policy.\"")
rep("**I8 Majority-restore primitives: SUBSTRATE.**","**I8 Majority-restore primitives: SUBSTRATE (primitive only).**")
rep("**I9 `reg_from_active`: SUBSTRATE (operation).**","**I9 `reg_from_active`: SUBSTRATE (primitive only).**")
between("**I12 Action semantics: SUBSTRATE, contested in one line.**","**I13 Relinquishment policy",f"""**I12 Action semantics: primitives SUBSTRATE (I12-p); birth targeting EXTERNAL COORDINATION (supplied targeting).**
- The step executes the program-chosen action: route contacts (0/1), renewals (3/4), action 6 births, and everything else through `ac4.react` (`ac9.py:L85-L112@6c6323b`). The primitives execute any chosen action, harmful ones included (I12-p).
- v1 had marked the bank-selection line `ac9.py:L108@6c6323b` as contested. Astra #28 rules (verbatim): "For `ac9.py:108`, "every bank with demand" is not necessarily a priority ordering. It is a supplied production-targeting rule. On the description provided, I would not clear it as generic chemistry yet."
- v1.1 therefore classifies I12 as **EXTERNAL COORDINATION (supplied targeting)**. The code-level explanation is in §4.1.

""")
rep("## 5. Revised closure sentence",f"""### 4.1 Birth targeting at `ac9.py:L108@6c6323b` (code-level explanation)

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
- From the code: demand reads occupancy (`life>0`) of the memory replicas. Occupancy is declared state, but the mapping from it to targets is not. Targeting changes only through occupancy, never through content that encodes the targeting itself. Competition is resolved by host list order.

**What would make it declared state (SKETCH ONLY, not a proposal).**
- Each bank would carry a declared, damageable demand marker or receptor that a generic birth reaction reads locally, with no host list.
- The service order and thresholds would sit in maintained content, or competition would be resolved by a generic law, for example proportional allocation.
- Altered markers, including harmful ones, would redirect births without host restoration.
- Bank 0's inclusion would itself be marker content.

Building or testing this needs separate, concrete approval (Astra #28).

## 5. Revised closure sentence""")

# §5 closure
between("**Triage v1.1 F1 (as written).**","**What would move each violating item into declared state.**",f"""**Closure sentence (v1.1, verbatim from Astra #28; replaces the v1 sentence, which is withdrawn).**

> {NEW}

**Astra #28 edit E28-2 (verbatim):**
> {E2}

**Scope notes (Astra #28, verbatim).**
- {NORECERT}
- Astra's reason for the firmer wording: "The revised closure sentence is directionally correct but still overstates the W/C/B clause while birth targeting remains contested. It also risks preserving the headline through "closure holds conditional on external coordination.""

**Directive (Astra #28, verbatim):** {STOP} {NORUN}

""")
rep("**What would move each violating item into declared state.** These are future protocols, not runs. Each requires its own approval, and none was designed or executed here.",
f"""**What would move each violating item into declared state: SUCCESSOR DESIGN, SKETCH ONLY, NOT A PROPOSAL.** Astra #28 (verbatim): {SKETCH2} {APPR} Its planning-only note: {NOAUTH}

Nothing below was designed in detail or executed. Astra #28 adds that {SKETCH1}, and that the successor must account for (verbatim):
{SUCC_REQ}

Sketch items:""")
rep("- **I12** (only if Astra rules it organization-specific): put the birth bank list in rule content.",
"- **I12 birth targeting** (ruled supplied targeting by Astra #28): declared, damageable demand markers read by a generic birth reaction (§4.1 sketch).\n- **I4a-s/I4c-s/I4d-s choices:** the source, destination and erase-target rules become table or marker content, under the same table sketch.")
rep('Dependency flag, carried from triage v1.1 U1: such a successor may be a new architecture family or need a protected controller. Both need explicit approval. Consult #25 also says "Do not automatically build a successor."',
'Dependency flag (updated per Astra #28): "This would be a material architectural change. Whether the project calls it a new "family" depends on its architecture taxonomy; that terminology should not determine authorization." A protected controller is not inherently necessary. Consult #25 also says "Do not automatically build a successor."')

# §6
rep("| Q-EXIST | Narrows the *statement* of the bounded production-closure claim (§5). No new evidence; a definitional reclassification only. |",
"| Q-EXIST | Replaces the closure statement with Astra #28's firmer sentence (§5). No new evidence; a definitional reclassification only. The birth-targeting rule qualifies the W/C/B production claim (E28-2). C1–C5 criteria are not re-certified here. |")
# §7
rep("- **Exception.** If a future protocol first moved the coordination into declared state (§5), a U3-style loop running through that declared table *would* bear on the closure sentence. That ordering follows consult #25: U1 first, then U3 only if it would change a named conclusion.",
f"""- **Exception.** If a future protocol first moved the coordination into declared state (§5, sketch only), a U3-style loop running through that declared table *would* bear on the closure sentence. That ordering follows consult #25: U1 first, then U3 only if it would change a named conclusion.
- **Astra #28 (verbatim):** {U3HOLD}""")
# §8
between("## 8. Open items for Astra (no run implied)","## 9. Integrity",f"""## 8. Astra items: rulings from consult #28, and what remains open

- **Q-A1 (step split): ruled too narrow.** Astra #28: "The primitive/policy distinction is right, but "the four steps are substrate, and only their order violates the rule" is too narrow." Applied as E28-1 (§1, §3).
- **Q-A2 (I12 birth targeting): ruled supplied targeting.** I12 is reclassified EXTERNAL COORDINATION (supplied targeting) (§3, §4.1). E28-2 keeps it as an explicit qualification on the W/C/B production claim.
- **Q-A3 (format): partly ruled.** Astra #28: "Fixed rule width, first-match interpretation and a fixed instruction vocabulary can be admissible syntax. A system need not have a universal programming language." Forced enablement is disclosed as an expressivity restriction (I3r).
- **Open (paper only).** Does the forced enablement in I3r hard-wire an organization-specific action that declared content cannot suppress or redirect? From the code, content can redirect the action field, but cannot disable the rule.

""")
# §9
between("## 9. Integrity","\0" if False else s[s.index("## 9. Integrity"):][:0]+"## 9. Integrity",'')
s=s[:s.index("## 9. Integrity")]+f"""## 9. Integrity

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
"""
open(DST,'w').write(s); print('ok',len(s))
