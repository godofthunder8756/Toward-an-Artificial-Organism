import hashlib, sys
sys.path.insert(0,'/workspace/scratch/u1_audit/v1_1'); from common import *
SRC='/workspace/review/track_a_lineage_triage_v1_2.md'; DST='/workspace/review/track_a_lineage_triage_v1_3.md'
raw=open(SRC,'rb').read(); assert hashlib.sha256(raw).hexdigest()=='84fa9614e022561b86cf2dddea0e3713d6f84585ee228d1016d95cea122fdb09'
s=raw.decode()
AUD='`/workspace/review/u1_substrate_audit_v1_1.md` (built from v1, sha256 `48c174f5…f13a`, which is retained unchanged)'
def rep(a,b,n=1):
    global s; c=s.count(a); assert c==n,(c,a[:80]); s=s.replace(a,b)
def between(a,b,new):
    global s; i=s.index(a); j=s.index(b,i+len(a)); s=s[:i]+new+s[j:]
rep("# Track A lineage triage v1.2: Artificial Autonomy and Organizational Closure","# Track A lineage triage v1.3: Artificial Autonomy and Organizational Closure")
rep("v1.2 built about 11:12 AM–noon ET |","v1.2 built about 11:12 AM–noon ET; v1.3 built about 12:11 PM–1 PM ET |")
rep("| Supersedes | `track_a_lineage_triage_v1_1.md`","| Supersedes | `track_a_lineage_triage_v1_2.md` (sha256 `84fa9614…fdb09`), left untouched; built from it by `/workspace/scratch/track_a_triage/v1_3/build_v1_3.py`. v1.2 superseded `track_a_lineage_triage_v1_1.md`")
rep("Consult #26: `/workspace/astra_consult26_response.txt` (sha256 `e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12`) |",
f"Consult #26: `/workspace/astra_consult26_response.txt` (sha256 `e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12`). Consult #28: {C28} |")
rep("| U1 | Addressed by `/workspace/review/u1_substrate_audit_v1.md` (sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`) |",
f"| U1 | Addressed by the U1 audit v1.1, {AUD}. Astra #28 rulings applied |")
rep("## Changelog v1.2 against v1.1",f"""## Changelog v1.3 against v1.2 (`84fa9614…fdb09`)

Paper only, under Aidan's planning approval. Source: Astra consult #28, with its named edits used verbatim. E28-3 to E28-10 are Track B items and are not applied here.
1. **E28-1 and E28-2 added verbatim** (F1, U1). The U1 audit v1.1 now splits primitives (SUBSTRATE) from source, destination, precondition, budget, scheduling and next-phase choices (EXTERNAL COORDINATION).
2. **Closure sentence replaced** everywhere by Astra #28's sentence. It is byte-identical to the audit v1.1 and synthesis v1.1. The v1.2 sentence is withdrawn, and C1–C5 for W/C/B are not re-certified.
3. **T1 qualified** (F1): constants are judged by organizational role. The substrate test T1 is distinct from the A0 tests T1–T5 cited in the U entries.
4. **I12 birth targeting** (`ac9.py` @ `6c6323b`) changes from contested to EXTERNAL COORDINATION (supplied targeting). F1's "Excluded?" text and U1 are updated, and Q-A1–Q-A3 are marked as ruled.
5. **Directives recorded** (F1, U1, U3): no further closure runs on the unchanged architecture; the successor transition-table design is SKETCH ONLY, not a proposal; U3 stays on hold. §6 records the v1.3 check script.

## Changelog v1.2 against v1.1""")
rep("- U1 substrate audit `/workspace/review/u1_substrate_audit_v1.md` (sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`).",
f"- U1 substrate audit `/workspace/review/u1_substrate_audit_v1.md` (sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`), and its v1.1 `/workspace/review/u1_substrate_audit_v1_1.md` (v1.3).\n- Astra consult #28 {C28} (v1.3).")
rep("Production closure of the full network is not established under the rule (F1). Astra items Q-A1–Q-A3 are open.",
"Production closure of the full declared network is not established under the rule (F1). Astra #28 ruled on Q-A1–Q-A3, and birth targeting is supplied targeting. No further closure runs on the unchanged architecture.")
rep("It does not change the closure sentence and bears only on a separate Q-CAUSE claim. Held, not proposed.",
"It does not change the closure sentence and bears only on a separate Q-CAUSE claim. Held, not proposed (on hold per Astra #28).")
# F1
rep("""without substituting the intended organization."

**Finding (v1.2; adopted verbatim""",f"""without substituting the intended organization."

**Substrate test T1, qualified (v1.3).** The U1 audit's test T1 ("Generic") is qualified by Astra #28 (verbatim):
> {T1Q}

**Primitive versus policy (Astra #28 edit E28-1, verbatim).**
> {E1}

**Finding (v1.2; adopted verbatim""")
between("**Finding (v1.2; adopted verbatim","**What the repo verdict records",f"""**Finding (v1.3; verbatim from Astra #28 and the U1 audit v1.1 §5; replaces the v1.2 finding, which is withdrawn).**
> {NEW}

**Astra #28 edit E28-2 (verbatim).**
> {E2}

**Scope (Astra #28, verbatim).** {NORECERT}

**Directive (Astra #28, verbatim).** {STOP} {NORUN}

""")
rep("""- **Production of W, C and B by program-selected actions:** this executes declared, inherited content through generic substrate operations (U1 audit I1–I3, I8, I9, I11, I12, I14 SUBSTRATE). I12, birth targeting at `ac9.py` @ `6c6323b`, is contested (Q-A2).""",
"""- **Production of W, C and B by program-selected actions:** the action primitives are substrate (U1 audit v1.1 I1–I3, I12-p, I14). However, birth targeting at `ac9.py` @ `6c6323b` (line 108, "every bank with demand") is **EXTERNAL COORDINATION (supplied targeting)** per Astra #28 (audit v1.1 I12 and §4.1). It remains an explicit qualification on the W/C/B production claim (E28-2). Forced enablement of the bank rules is a disclosed expressivity restriction (audit v1.1 I3r).""")
rep("- **Not excluded for succession, reconstruction and repair.** The fixed copy→verify→switch→remove order, the start condition, the timer coupling, the `maintain()` schedule, the regeneration policy and the relinquishment policy are EXTERNAL COORDINATION under the rule (U1 audit I4e, I5, I6, I7, I10, I13).",
"- **Not excluded for succession, reconstruction and repair.** Under the rule, these are EXTERNAL COORDINATION (U1 audit v1.1 I4a-s–I4d-s, I4e, I5, I6, I7, I10 and I13):\n  - the next-slot destination, the authorize-on-compare step and the erase-previous-slot choices;\n  - the fixed copy→verify→switch→remove order, the start condition and the timer coupling;\n  - the `maintain()` schedule, the regeneration policy and the relinquishment policy.")
rep("- the code the audit classified: `ac95.py` @ `a1b9759` (`advance()`, `maintain()`), `ac5_program.py` @ `6c6323b` (`prog.choose`),",
"- the code the audit classified: `ac9.py` @ `6c6323b` (birth targeting), `ac9_memory.py` @ `6c6323b` (`demand()`), `ac95.py` @ `a1b9759` (`advance()`, `maintain()`), `ac5_program.py` @ `6c6323b` (`prog.choose`),")
# U1
rep("**ADDRESSED by the U1 audit; Astra items open**","**ADDRESSED by the U1 audit v1.1; Astra #28 rulings applied**")
rep("**Status: ADDRESSED** by `/workspace/review/u1_substrate_audit_v1.md` (sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`).",
f"**Status: ADDRESSED** by {AUD.replace('`/workspace/review/u1_substrate_audit_v1_1.md`','`/workspace/review/u1_substrate_audit_v1_1.md`',1)}.\n- v1.3: Astra #28 (verbatim): \"Track A: ACCEPT THE MAIN AUDIT CONCLUSION, WITH NAMED CORRECTIONS. Under the adopted substrate rule, full production closure is not established. Further runs on the unchanged architecture will not resolve that structural limitation.\"")
rep("""  - **SUBSTRATE.** The interpreter `prog.choose`; decode; `build_program`; each of the COPY, VERIFY, SWITCH and REMOVE steps; majority-restore; `reg_from_active`; the `_cap` W gate; action execution; observation and conservation.""",
"""  - **SUBSTRATE (primitives only, per E28-1).** The interpreter `prog.choose`; decode; `build_program`; the copy, compare, atomic-write and erase primitives inside COPY, VERIFY, SWITCH and REMOVE; majority-restore; `reg_from_active`; the `_cap` W gate; the action primitives; observation and conservation.
  - **DISCLOSED EXPRESSIVITY RESTRICTION.** Forced enablement of bank rules (I3r).""")
rep("""  - **EXTERNAL COORDINATION (violations).** The **fixed copy→verify→switch→remove order** (I4e);""",
"""  - **EXTERNAL COORDINATION (violations).** The routines' source, destination, precondition, budget and next-phase choices (I4a-s–I4d-s); **birth targeting** at `ac9.py` @ `6c6323b` (I12, supplied targeting); the **fixed copy→verify→switch→remove order** (I4e);""")
rep("- Consequence: F1 is revised to the audit's closure sentence. Production closure of the full network is not established under the rule.",
"- Consequence: F1 is replaced by Astra #28's closure sentence (F1). Production closure of the full declared network is not established under the rule.")
between("**Open Astra items (from the audit §8, no run implied):**","**Dependency flags (retained from v1.1):**",f"""**Astra items: ruled by consult #28 (audit v1.1 §8).**
- **Q-A1: ruled too narrow.** "The primitive/policy distinction is right, but "the four steps are substrate, and only their order violates the rule" is too narrow." Applied as E28-1.
- **Q-A2: ruled supplied targeting.** "For `ac9.py:108`, "every bank with demand" is not necessarily a priority ordering. It is a supplied production-targeting rule. On the description provided, I would not clear it as generic chemistry yet." The audit v1.1 §4.1 gives the code-level explanation that Astra asked for, and no run is needed.
- **Q-A3: partly ruled.** Fixed width, first-match order and the instruction vocabulary can be admissible syntax. Forced enablement is disclosed as an expressivity restriction (I3r). Whether it hard-wires an organization-specific action remains open, on paper only.

**Directive (Astra #28, verbatim).** {STOP} {NORUN}

**What would move each violation into declared state: SUCCESSOR DESIGN, SKETCH ONLY, NOT A PROPOSAL** (audit v1.1 §5 and §4.1):
- a declared, damageable transition table executed by a generic table-driven step, tested with alternative and failing tables;
- thresholds held as maintained parameters;
- table operations on the counter and RIP bits;
- maintenance as program-selected actions;
- the regeneration and relinquishment policies held as declared content;
- declared demand markers read by a generic birth reaction, in place of the host bank list.

Astra #28 (verbatim): {SKETCH1} Requirements it lists (verbatim):
{SUCC_REQ}

Astra #28 (verbatim): {SKETCH2} {APPR} Aidan's planning-only approval: {NOAUTH}

""")
rep("""**Dependency flags (retained from v1.1):**
- Such a successor may be a new architecture family or need a protected controller. Both need explicit approval.""",
"""**Dependency flags (updated per Astra #28):**
- Architecture taxonomy does not determine authorization ("that terminology should not determine authorization"), and a protected controller is not inherently necessary. Implementation and testing need separate, concrete approval.""")
rep("""- The Astra rulings Q-A1–Q-A3 could change its list of conditions.
- A declared-state successor would change the F1 claim from "not established under this rule" to a tested claim. It is therefore eligible to be proposed, but no proposal is made here (it requires Aidan's decision).""",
"""- The Astra #28 rulings changed its list of conditions (v1.3: E28-1, I12).
- A declared-state successor could change the F1 claim from "not established under this rule" to a tested claim. Per Astra #28 it stays a SKETCH ONLY and is not proposed; any proposal requires Aidan's separate, concrete approval.""")
rep("Remaining: Astra rulings Q-A1–Q-A3 (paper only). No successor is built.",
"Astra rulings Q-A1–Q-A3 were received in consult #28 and applied in v1.3. Remaining: the open I3r question (paper only). No further closure runs on the unchanged architecture, and no successor is built.")
# U3
rep("- **Exception:** if the coordination were first moved into declared state (U1 future protocol), a U3-style loop through that declared table *would* bear on the closure sentence.",
f"- **Exception:** if the coordination were first moved into declared state (U1 successor sketch, not proposed), a U3-style loop through that declared table *would* bear on the closure sentence.\n- **Astra #28 (verbatim, v1.3):** {U3HOLD}")
# §6
rep("## 6. Verification of this document\n",
"""## 6. Verification of this document

**v1.3.** `/workspace/scratch/u1_audit/v1_1/check_v1_1.py` (log `check_v1_1.log`) checks this file together with the audit v1.1 and the synthesis v1.1. It checks that:
- every Astra #28 quotation is byte-exact;
- the closure sentence is byte-identical across the three files, and the v1.2 sentence is absent;
- every `` `path` @ `commit` `` pair exists;
- forbidden phrases are absent;
- prior versions are unchanged.
""")
rep("Fixed duty 1/2 gives 4/6 alive,","Fixed duty 1/2 gives 4/6 surviving,")
rep("Require failure while alive with content intact,","Require failure during function, before death, with content intact,")
rep("§6 records the v1.3 check script.","§6 records the v1.3 check script. Two survival-count wordings (R2, T-INTERRUPT) are reworded to avoid the word \"alive\" outside quotes.")
open(DST,'w').write(s); print('ok',len(s))
