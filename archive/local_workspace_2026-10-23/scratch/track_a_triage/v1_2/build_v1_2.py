"""Build track_a_lineage_triage_v1_2.md from v1.1 by exact, asserted text edits. Writes only the v1.2 file."""
import hashlib, re
SRC='/workspace/review/track_a_lineage_triage_v1_1.md'
DST='/workspace/review/track_a_lineage_triage_v1_2.md'
raw=open(SRC,'rb').read()
assert hashlib.sha256(raw).hexdigest()=='d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef'
s=raw.decode('utf-8')
def rep(old,new,n=1):
    global s
    c=s.count(old); assert c==n,(c,old[:80]); s=s.replace(old,new)
def between(a,b,new):
    global s
    i=s.index(a); j=s.index(b,i); s=s[:i]+new+s[j:]

AUDIT='`/workspace/review/u1_substrate_audit_v1.md` (sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`)'
WREV='`/workspace/review/wrel_results_review_v1.md` (sha256 `60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace`)'
ATT='`/workspace/review/wrel_attainability_from_existing_outputs_v1.md`'
C25='`/workspace/astra_consult25_response.txt` (sha256 `31740a1e7129baf9ff9d3c047492fdbe1952970ad836d271742b5a6f14ff8791`)'
C26='`/workspace/astra_consult26_response.txt` (sha256 `e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12`)'
SENT=("Within the declared model and operating range, and with interpretation, decoding, copy, comparison, write, erase, majority-restore, the W-catalysed affordability gate, action execution, observation and conservation as substrate, the production of W, C and B by program-selected actions executes declared, inherited content and meets C1–C5. The replacement of the description (succession) and the reconstruction and repair of the program and the maintained registers do not meet the rule. They are sequenced, triggered and scheduled by supplied, organization-specific coordination: `maintain()`'s schedule and triggers; `advance()`'s fixed copy→verify→switch→remove order, start condition and timer coupling; the regeneration trigger, budget and exclusion policy; and the relinquishment policy. The organism's maintained state holds only the current phase, pointer, counter and streak values that this coordination reads. Production closure of the full network {W, C, B, description, derived program} therefore holds only conditional on that external coordination, and is not established under this rule.")
NC1='"Triage priority, retained functional evidence and mechanism novelty are separate fields. Reproduction by a conventional mechanism does not automatically erase a functional role or classify a result as redundant."'
NC7='"Rival reproduction may end development of a claimed novelty without negating retained causal or functional evidence. The claim being retired is named explicitly."'
NC8='"No additional lineage experiment is proposed unless its possible outcomes change a named scientific claim or program decision. Completing an experiment queue is not itself a research objective."'
NC2='"Track A\'s substrate rule is fixed before further runs. Organization-specific maintenance sequencing must be represented in declared system state; a supplied resource gate alone does not internalize the sequence it enables."'
RULE='"A supplied substrate operation may implement generic state transformation, transport, execution or numerical integration. Organization-specific instructions, maintenance sequences, switching conditions and repair policies must be represented in declared system state rather than hidden in the supplied operation. The substrate must execute alternative admissible instruction contents, including unsuccessful ones, without substituting the intended organization."'

# ---------- header + changelog ----------
between('# Track A lineage triage v1.1','## Changelog against v1 (`b4e1a772…7f0b`)', f"""# Track A lineage triage v1.2: Artificial Autonomy and Organizational Closure

| | |
| --- | --- |
| Owner | Research Delegate (Track A), for Aidan Ahern |
| Date | 2026-10-21. v1 about 10:30 AM ET; v1.1 about 10:45 AM ET; v1.2 built about 11:12 AM–noon ET |
| Supersedes | `track_a_lineage_triage_v1_1.md` (sha256 `d2cc9152…a5d3ef`), which supersedes `track_a_lineage_triage_v1.md` (sha256 `b4e1a772…7f0b`). Both left untouched. Built deterministically from v1.1 by `/workspace/scratch/track_a_triage/v1_2/build_v1_2.py` |
| Kind | Planning and assessment only (PAPER ONLY). Nothing was run, trained, committed or pushed |
| Repo | `godofthunder8756/Toward-an-Artificial-Organism`, master `32cfbe6` (2026-10-20 1:39 PM ET) |
| PRs read | #3–#10, all open drafts, fetched read-only (heads in §0.2). W-REL results: PR #11 (via the review below) |
| Astra | Consult #25: {C25}. Consult #26: {C26} |
| W-REL | Approved by Aidan at 8:58 AM ET today (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`). Executed in PR #11 and reviewed in {WREV}. Consult #26: formal A-SEP is **UNRESOLVED-COMPUTE** (ITEM-9 validation incomplete); per-setting labels are conditional classifications (U10) |
| U1 | Addressed by {AUDIT} |

**Standing rules applied.**
- Read-only on the repo and GitHub; scratch work only, outside the repo.
- No runs and no training.
- No consciousness claim, and no C4 or C5 claim. "C1–C5" and "S1–S4" in F1 are the Definitions Charter v2 component and maintained-state criteria, not C-axis levels.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.
- In the organism lineage, a result shown by ablation is labelled **within-model ablation dependence**. It is never relabelled Q-NECESSITY, which in this program means necessity of a learned component relative to a declared restricted class (PR #9 and #10 usage).

**Citation convention.**
- `path` @ `commit` names a file and the commit it is read from.
- For master files the commit is the last commit that touched the file.
- For PR files the commit is the PR head, and the PR link is given.
- Every `path @ commit` pair in this document was machine-checked to exist (§6).
- Box files (not in the repo) are cited by absolute path and sha256.
- Anything not verifiable from these sources is marked **UNVERIFIED**.

## Changelog v1.2 against v1.1 (`d2cc9152…a5d3ef`)

1. **Astra #25 named changes 1, 7 and 8 applied, quoted verbatim in §0.3.**
   - NC1: each REDUCED OR NO LONGER PRIORITY entry now carries separate fields for triage priority, retained functional evidence, mechanism novelty and future effort (§4).
   - NC7: each such entry names the claim being retired (§4).
   - NC8: every U entry has a "Named claim or decision its outcomes would change" field. No experiment is proposed in this triage.
2. **Category renamed.** REDUNDANT is now **REDUCED OR NO LONGER PRIORITY** everywhere: definitions, counts, §4 heading, S5, S13, R4, R5, U3 and U10. The old name survives only inside verbatim Astra quotes and this changelog.
3. **F1–F4 narrowed as Astra #25 §B.1 specifies, each quoted verbatim.**
   - F1 is foundational only to a *conditional* closure claim. It adopts the revised closure sentence of the U1 audit, cited by path and sha.
   - F2 no longer treats common-resource explanations as generally excluded.
   - F3 does not exclude an externally specified coordinator with a consequential resource gate.
   - F4 is renamed "endpoint agreement under the audited observer-discard procedure".
4. **U10 corrected and updated.**
   - Reproduction by a rival no longer creates a reduction entry (NC1, NC7).
   - W-REL results are added from the review and Astra #26: formal A-SEP is UNRESOLVED-COMPUTE; the conditional labels are UNRESOLVED-DESIGN at (1/50, 3/50) and REFERENCE CRITERIA NOT MET at (1/100, 1/10); MB-myopic is UNRESOLVED at the no-contrast settings; the A1–A4 dispositions are recorded.
   - The read-only attainability extraction is added.
   - B4 is updated from METHOD ONLY to RESULTS REVIEWED.
5. **Astra #25 allocation applied to the U items.**
   - U1: ADDRESSED by the audit, with open Astra items Q-A1–Q-A3.
   - U2: RETAINED AS A QUESTION.
   - U3: HELD, NOT PROPOSED. Per the audit, U3 does not change the closure sentence; it bears only on a separate Q-CAUSE (O3) claim.
   - U4–U7 and U9: DEFERRED.
   - U8 and U11: DROPPED from the active queue, with short dropped-with-reason notes.
   - U10: EXECUTED AND REVIEWED; FORMAL A-SEP UNRESOLVED-COMPUTE.
   - Astra's two stopping-rule corrections are applied to U2 and U3.
6. **Counts.** Category counts are unchanged (5 / 15 / 11 / 11 = 42). §1 adds allocation sub-counts for the 11 UNRESOLVED entries.
7. **Not applied (out of the requested scope).**
   - Astra #25's remarks on F5, S8, S10 and S12. They are consistent with the existing entries; S12's "read the existing comparison" remains open.
   - Its Track B items.
8. **Check script.** `/workspace/scratch/track_a_triage/v1_2/check_v1_2.py` (log `check_v1_2.log`) checks:
   - every Astra quote is verbatim;
   - every `path @ commit` pair exists;
   - the counts;
   - the rename;
   - forbidden phrases;
   - the audit sentence is byte-identical to the audit file;
   - v1 and v1.1 are unchanged.

## Changelog v1.1 against v1 (retained from v1.1)

""")
rep('## Changelog against v1 (`b4e1a772…7f0b`)\n\n','')
rep('No category assignment, count, rank or finding changed from v1.\n','No category assignment, count, rank or finding changed from v1 (v1.1 statement, retained).\n')

# ---------- sources ----------
rep("- `/workspace/review/c4_reliability_APPROVAL_RECORD.md`.\n\n### 0.3",
f"""- `/workspace/review/c4_reliability_APPROVAL_RECORD.md`;
- (v1.2) W-REL results review {WREV};
- (v1.2) read-only attainability extraction {ATT}.

**v1.2 sources (box).**
- Astra consult #25 {C25};
- Astra consult #26 {C26};
- U1 substrate audit {AUDIT}.

### 0.3""")

# ---------- categories ----------
rep("""- **REDUNDANT.** Adequately explained by a simpler established mechanism. The mechanism is named from control theory, RL, dynamical systems or ALife. "Redundant" is a statement about the claimed *extra* mechanism. It does not say the measurements were wrong.""",
"""- **REDUCED OR NO LONGER PRIORITY** (renamed in v1.2, per Astra #25: "I would rename REDUNDANT to "REDUCED OR NO LONGER PRIORITY," with separate fields for retained evidence and future effort. A mechanism can instantiate a real role while being conventional.").
  - This is a **triage-priority** category only. The claimed *extra* mechanism is adequately explained by a named simpler mechanism from control theory, RL, dynamical systems or ALife, so developing that claim further is not a priority.
  - It does not say the measurements were wrong. It does not erase any functional or causal role.
  - Each entry carries the separate fields of NC1 and names its retired claim (NC7). See §4.""")
rep("""Where this triage makes a judgment the repo does not itself record, the entry says **"triage judgment"**.""",
f"""- **UNRESOLVED allocation (v1.2).** Each UNRESOLVED entry also carries Astra #25's allocation: ADDRESSED, RETAINED AS A QUESTION, HELD (NOT PROPOSED), EXECUTED AND REVIEWED, DEFERRED, or DROPPED FROM THE ACTIVE QUEUE. It also names the claim or decision its outcomes would change (NC8).

**Astra #25 named changes applied in v1.2 (verbatim):**
- **NC1.** > {NC1}
- **NC7.** > {NC7}
- **NC8.** > {NC8}

How they are applied:
- **Category is triage priority only.** Retained functional evidence and mechanism novelty are recorded separately: in §4 for reduced entries, and in each F and S entry's evidence and "Simplest rival" lines.
- **No F or S entry claims mechanism novelty.** Several (F5, S6, S11, S12) keep a real functional role even though a conventional mechanism explains them.

Where this triage makes a judgment the repo does not itself record, the entry says **"triage judgment"**.""")

# ---------- counts ----------
between('## 1. Summary counts','---\n\n## 2. FOUNDATIONAL',"""## 1. Summary counts

| Category | Count | IDs |
| --- | --- | --- |
| FOUNDATIONAL | 5 | F1–F5 (F1 now foundational only to a conditional closure claim) |
| SUPPORTING | 15 | S1–S15 |
| REDUCED OR NO LONGER PRIORITY | 11 | R1–R11 |
| UNRESOLVED | 11 | U1–U11 |
| **Total** | **42** | |

**UNRESOLVED allocation (Astra #25 §B.2, applied in v1.2):**

| Allocation | Count | IDs |
| --- | --- | --- |
| ADDRESSED (audit done; Astra items open) | 1 | U1 |
| RETAINED AS A QUESTION (no experiment queue) | 1 | U2 |
| HELD, NOT PROPOSED | 1 | U3 |
| EXECUTED AND REVIEWED; formal A-SEP UNRESOLVED-COMPUTE | 1 | U10 |
| DEFERRED | 5 | U4, U5, U6, U7, U9 |
| DROPPED FROM THE ACTIVE QUEUE | 2 | U8, U11 |
| **Total** | **11** | |

**Top questions by consequence** (full entries in §5):
1. **U1 / J1, addressed.** Under the consult #25 substrate rule, the sequencing, triggers and policies are external coordination. Production closure of the full network is not established under the rule (F1). Astra items Q-A1–Q-A3 are open.
2. **U2.** Can the system adapt its own organization? This is retained as a question, with no experiment queue.
3. **U3.** Does a content intervention propagate to the enabling machinery and back (the O3 constitutive loop)? It does not change the closure sentence and bears only on a separate Q-CAUSE claim. Held, not proposed.

""")

# ---------- F1-F4 ----------
between('### F1. Production closure','### F5. Reconstruction', f"""### F1. Production closure (Maturana & Varela clause (i)): foundational only to a conditional claim

**Astra #25 narrowing (verbatim).** "F1 is foundational only to a conditional closure claim. A strongly connected dependency graph does not by itself demonstrate production closure: the edges must distinguish production, enabling conditions, resource dependence and supplied sequencing."

**Substrate rule applied (consult #25, verbatim).**
> {RULE}

**Finding (v1.2; adopted verbatim from the U1 audit §5, {AUDIT}).**
> {SENT}

**What the repo verdict records (kept as a record, not as this triage's finding).**
- K3 states that every necessary component {{W, C, B, description, derived program}} meets C1–C5, and that the maintained state {{pointer, coordination, route memory, decision state}} meets S1–S4.
- It states that the production-dependency network is one strongly connected component with no external root.
- Its scope is "within the declared model and operating range, under the accepted substrate convention".
- C1–C5 and S1–S4 are Definitions Charter v2 criteria. K3 itself excludes "autopoietic" unqualified and "alive"; this triage makes neither claim.

**What the strongly connected component does not show (Astra #25).** Whether the dependency audit's edges are typed as production, enabling condition, resource dependence or supplied sequencing was **not re-checked in this triage (UNVERIFIED)**. Until they are, the graph is read as a dependency graph, not as a demonstration of production closure. The dependency audit itself calls `advance()` "A fixed sequence machine" with a built-in verify gate (`DEPENDENCY_AUDIT_v2_CORRECTION.md` @ `4b85851`, "Supplied operations").

**Evidence:**
- `CLOSURE_VERDICT_v1.md` @ `4b85851` (K3 verdict, §1–§3);
- `DEFINITIONS_CHARTER_v2.md` @ `4b85851` (§8 criterion);
- `DEPENDENCY_AUDIT_v2_CORRECTION.md` @ `4b85851`;
- `AC105_RESULTS_v1.md` @ `daf421c` (seeds 5800–5807, 160 rows, six gates pass);
- ledger layers O1, O2 and C0 = SUPPORTED_BOUNDED in `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`;
- `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1 row 1 (HIGH);
- the code the audit classified: `ac95.py` @ `a1b9759` (`advance()`, `maintain()`), `ac5_program.py` @ `6c6323b` (`prog.choose`), `ac104.py` @ `343ba17`, `ac105.py` @ `8f0218a`, `ac99_d2.py` @ `8e9ab4a` (U1 audit §3–§4).

**Simplest rival.** *External coordination over an ALife production network*: a conventional artificial chemistry whose turnover is real, but whose organization is held together by a host-supplied scheduler. The belief ledger's O2 rival is "conventional production network under identical substrate".

**Excluded?** Only for the parts the rule classifies as substrate-executed content.
- **Production of W, C and B by program-selected actions:** this executes declared, inherited content through generic substrate operations (U1 audit I1–I3, I8, I9, I11, I12, I14 SUBSTRATE). I12, birth targeting at `ac9.py` @ `6c6323b`, is contested (Q-A2).
- **Every coordinator *write* is W-gated** through `_cap` (`AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §2). Per named change 2, this shows the gate matters. It does not internalize the sequence: > {NC2}
- **Not excluded for succession, reconstruction and repair.** The fixed copy→verify→switch→remove order, the start condition, the timer coupling, the `maintain()` schedule, the regeneration policy and the relinquishment policy are EXTERNAL COORDINATION under the rule (U1 audit I4e, I5, I6, I7, I10, I13).

**Why foundational (narrowed).** It is foundational only to the conditional closure claim. Every later autonomy verdict that inherits it by byte-identity composition (A0, A2, A4/I1, I5) inherits the same condition.

**Bound (load-bearing).** The J1 "substrate by convention" reading is replaced by the consult #25 rule (U1). Before K3, `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` had issued **UNRESOLVED** on this judgment. The audit's result is consistent with that.

**Evidence split (stated in K3 §1).** AC105 supplies the operating range. The ablation, turnover and verification facts are inherited from AC10–AC95 and were not re-tested by AC105.

### F2. Within-model ablation dependence of the production network, including functional interruption and rescue during function

**Astra #25 narrowing (verbatim).** "F2 supports within-model ablation dependence. The digest does not justify treating common-resource explanations as generally excluded."

**Finding.** Ablating W, C or B production breaks the organization. Blocking W birth depletes W at about t=63, and 8/8 individuals die with the description intact at death. Cutting W just before reconstruction makes reconstruction fail **during function, before death** (`window_reg_writes == 0`; AC92's "while alive" is an operational not-yet-dead label, not an "alive" claim), and a machinery-only restoration of W (labelled EXTERNAL) resumes and completes it.

**Evidence:**
- `AC10_RESULTS_v1.md` @ `10f6878` (nine prespecified gates);
- `AC91_RESULTS_v1.md` @ `1fc82f1` (seeds 4200–4203, seven gates pass);
- `AC92_RESULTS_v1.md` @ `125027b` (seeds 4300–4303, six gates pass);
- K3 §1 table.

**Simplest rival.** *Common resource starvation* (dynamical systems): any cut that drains energy or material kills a dissipative system, with no specific dependency structure. A weaker variant is a t=0 kill that shows only that the part is needed at startup.

**Excluded?** Only the t=0 variant. Common-resource explanations are **not generally excluded**.
- **The t=0 variant: excluded.** AC92 shows reconstruction failing during function (before death), with the content intact, and resuming under a machinery-only W restoration (`AC92_RESULTS_v1.md` @ `125027b`).
- **Content loss as the cause of death: excluded.** AC91 shows the description intact at death (`AC91_RESULTS_v1.md` @ `1fc82f1`).
- **Common resource starvation: not generally excluded.**
  - The AC2 clamped-information contrast and catalyst rescue are "bounded evidence" for AC2's setting only (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`, row "Dependence not explained solely by common resource starvation"; `AC2_RESULTS_v1.md` @ `6c6323b`).
  - AC92's rescue restores W, which is both the produced machinery and a common resource. So it is consistent with resource dependence.
- **Also not excluded:**
  - dependence outside the declared model and range;
  - W=0 being an absorbing state, a named cascade (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1).

**Why foundational.** This is Track A's "causal necessity through interventions" in the organism lineage, in the bounded sense of within-model ablation dependence. It uses interruption during function plus a content-free rescue, not a t=0 kill.

**Q-axis.** Within-model ablation dependence (Q-CAUSE-type evidence within the model). **This is not Q-NECESSITY.**

**Bound.** One model, one operating range. W=0 is an autocatalytic absorbing state, a named cascade (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1).

### F3. Coordination writes are W-gated by produced machinery; the succession is coherent and resumable (its sequence is supplied)

**Astra #25 narrowing (verbatim).** "F3 does not exclude an externally specified coordinator with a consequential resource gate. Refusal at W=0 establishes that the gate matters. It does not establish that the sequence of operations is internally constituted."

**Finding.**
- **AC93** makes the coordinator's MODE write W-gated: it refuses at W=0 and binds gradedly in W, and it is inert at the healthy fixed point W=3.
- **AC94** freezes a coherent resumable succession, with four per-individual requirements all holding:
  - source preservation;
  - verified activation, with the pointer switch atomic with the MODE commit (`split_events == 0`);
  - correct removal;
  - a W-funded rate limiter that freezes at W=0 and resumes on a machinery-only rescue.
- The `ungated` comparator reproduces frozen AC92 byte-for-byte (32/32).

**Evidence:**
- `AC93_RESULTS_v1.md` @ `1fe48df`;
- `AC94_RESULTS_v1.md` @ `6db1c47` (seeds 4404–4407, 120 rows);
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (historical next-action block).

**Simplest rivals.**
- (a) *External coordination with a cosmetic gate*: a host-supplied sequencer whose resource gate never binds.
- (b) *An externally specified coordinator with a consequential resource gate* (Astra #25).

**Excluded?**
- **(a) is excluded for the writes.**
  - The gate binds: it refuses at W=0 at the single-step level, and a mid-cycle W=0 stall is pinned to the pre-existing copy by the ungated rival arm (`AC93_RESULTS_v1.md` @ `1fe48df`).
  - Changes are attributable: the AC94 `ungated` comparator reproduces AC92 byte-for-byte, and the `split` rival differs only in the switch mechanism (`AC94_RESULTS_v1.md` @ `6db1c47`).
- **(b) is not excluded.**
  - The gate is consequential, but the sequence is supplied. Under the consult #25 rule, the fixed order, start condition and timer coupling are EXTERNAL COORDINATION (U1 audit I4e, I5, I6), and the gate itself is SUBSTRATE (I11).
  - The gate is also inert at the healthy fixed point W=3, so in normal operation it does not distinguish the organism from an ungated sequencer (AC93, "near-equivalence").

**Why foundational (narrowed).** It moves every paid write on the reconstruction and coordination path onto produced, finite-lived machinery. It shows that the gate matters, not that the sequence is internally constituted.

**Bound.** The transition *logic* in `advance()` is host-supplied coordination under the rule. The interpreter `prog.choose` is generic substrate under the rule (U1 audit I1), subject to Q-A3.

### F4. Endpoint agreement under the audited observer-discard procedure

**Astra #25 narrowing (verbatim).** "F4 should say "endpoint agreement under the audited observer-discard procedure." That is narrower than trajectory-level state sufficiency or absence of every host-side influence."

**Finding.**
- **AC95.** The reset-progress flag becomes a maintained RIP bit, and the observer is strictly observational. Discarding the observer record leaves the final `state_hash` identical 16/16, including under a mid-reset W cut followed by a machinery-only rescue.
- **AC96.** The host-side `alloc.streak` is internalized. Endpoint agreement under observer-discard holds 8/8 at a mid-streak discard point.

**Evidence:**
- `AC95_RESULTS_v1.md` @ `d7925cf` (seeds 4408–4411, 136 rows, four gates);
- `AC96_RESULTS_v1.md` @ `d7925cf` (seeds 4412–4415, 24 rows);
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (paragraphs AC95 and AC96).

**Simplest rival.** *Hidden host-side memory* (external coordination): host bookkeeping, such as an observer history or a Python dict, that silently steers the trajectory.

**Excluded?** Only at the endpoint, under the audited procedure.
- Observer-discard leaves the final `state_hash` identical: 16/16 in AC95, 8/8 in AC96.
- Source inspection closed the two named class-C leaks, the reset flag and `alloc.streak` (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`).

**Not excluded:**
- **Trajectory-level state sufficiency:** "per-tick trajectory not compared" (status file).
- **Absence of every host-side influence.** In particular, the supplied coordination the U1 audit classifies as EXTERNAL COORDINATION (I4e, I5, I6, I7, I10, I13) is a host-side influence by design. Observer-discard tests the observer's *record*, not the coordinator's *logic*.
- **Host functions outside the audited architecture.**

**Why foundational (narrowed).** It is the operational test that the observer record does not determine the endpoint. Track B can reuse it as T-OBS (Appendix B6), reported as endpoint agreement.

**Bound.**
- Endpoint agreement only.
- Source inspection covers the audited architecture only.

""")

# ---------- S-table renames ----------
rep("**The decision *rule* is classified REDUNDANT (R4)**","**The decision *rule* is classified REDUCED OR NO LONGER PRIORITY (R4)**")
rep("The matrix-specific negative is recorded, not redundant |","The matrix-specific negative is recorded; it is not a reduction entry |")
rep("| Superseded in strength by S15","| Superseded in strength by S15")
rep("Mechanism-level composition. The survival level is not confirmed (U8) |","Mechanism-level composition. The survival level is not confirmed (U8, dropped from the active queue) |")

# ---------- section 4 ----------
rep("## 4. REDUNDANT (named simpler mechanism)","## 4. REDUCED OR NO LONGER PRIORITY (named simpler mechanism)")
rep("| ID | Claimed extra mechanism | Reduces to (named mechanism, field) | Evidence (path @ commit) | What survives |",
    "| ID | Claimed extra mechanism | Reduces to (named mechanism, field) | Evidence (path @ commit) | Retained functional evidence |")
rep("**Triage judgment**: the repo labels level (b) ESTABLISHED and does not call the rule redundant |",
    "**Triage judgment**: the repo labels level (b) ESTABLISHED and does not reduce the rule |")
rep("Integration is not falsified (P8: observer-discard passes). Redundancy is a utility claim about the implementation as built (P2 defect) |",
    "Integration is not falsified (P8: observer-discard passes). The errata's \"redundant\" is a utility claim about the implementation as built (P2 defect) |")
rep("**Simplest rival per redundant entry.** For REDUNDANT entries the simplest rival *is* the reduction, and existing evidence supports it.",
    "**Simplest rival per reduced entry.** For REDUCED OR NO LONGER PRIORITY entries the simplest rival *is* the reduction, and existing evidence supports it.")
rep("""- **R11. Simplest rival:** a same-information reactive policy, or a 3-line sufficient-statistic threshold rule (control / RL).
""","""- **R11. Simplest rival:** a same-information reactive policy, or a 3-line sufficient-statistic threshold rule (control / RL).

**Separate fields per entry (NC1), with the retired claim named (NC7).** For every entry:
- **Triage priority** is REDUCED OR NO LONGER PRIORITY: no further development of the named claim.
- **Mechanism novelty** is none: the claimed extra mechanism reduces to the named mechanism in the table.
- **Retained functional evidence** is the table's last column. The measurements stand.

| ID | Claim retired (named, NC7) | Retained functional or causal evidence (not negated) | Future effort |
| --- | --- | --- | --- |
| R1 | "The AC67/AC71 loop is self-monitoring beyond a watchdog with a fixed corrective action" | AC67/AC71 measurements; the read/repair convention lesson | None |
| R2 | "AC11 acquires an adaptive allocate/relinquish switch" | AC11 measurements; the fixed-level sweep rule (B6 T-RIVAL) | None in this line. The construct is not retired (U2; Astra #25: "Failure of one adaptive implementation does not retire adaptation of organization as a construct.") |
| R3 | "Experience-dependent adjustment of the exploration rate is needed for AC6's behaviour" | Local relinquishment and reacquisition are viable (AC6) | None |
| R4 | "The decision rule's *adaptivity* is a mechanism beyond a counter threshold with a fixed budget" (triage judgment) | The internalization (S5) and the AC105 matched comparisons | None; economics deferred (U7) |
| R5 | "The AC106 second-order cause-belief adds utility over the first-order streak counter, as implemented" | Integration is not falsified (observer-discard passes); P1/P2 defects documented | None |
| R6 | "Persistent storage of the cause estimate is load-bearing in the clean two-cause world" | Content is load-bearing as a selector (S7) | None |
| R7 | "Continuous repair sustains the estimate's in-window correctness" | Repair matters post-window (G4 8/16); correctness and retention are separable | None |
| R8 | "The AC117 monitor is a second-order predictor" | CONTROL-yes (directional repair) | None here; the W-REL follow-up is U10 |
| R9 | "A graded or weighted posterior format yields a demonstrated advantage" | AC113 data; "format is not cognitive necessity" | None |
| R10 | "The organism self-produces new content" | Inherited content is permitted; reconstruction of inherited content (F5) | None |
| R11 | "An explicit maintained self-state V is needed in the tested task" | P_rb and rule 9_d results; the bridge task as a benchmark | None |
""")

# ---------- U section ----------
between('### U1 (rank 1).','### U2 (rank 2).', f"""### U1 (rank 1). J1: supplied coordinator and interpreter — substrate, or externally coordinated computation? **ADDRESSED by the U1 audit; Astra items open**

**Allocation (Astra #25, verbatim).** "Resolve now by specification and code audit. Stop after classifying each disputed operation and revising the claim. Do not automatically build a successor."

**Status: ADDRESSED** by {AUDIT}.
- The finite rule is consult #25's, quoted verbatim in F1.
- The audit classified every disputed operation of the AC105 code path, with file:line@commit citations machine-checked against master `32cfbe6` and `db0ef2f`:
  - **SUBSTRATE.** The interpreter `prog.choose`; decode; `build_program`; each of the COPY, VERIFY, SWITCH and REMOVE steps; majority-restore; `reg_from_active`; the `_cap` W gate; action execution; observation and conservation.
  - **DECLARED-STATE.** The phase, pointer and ACTIVE bits, the timer counter and RIP bit, the Gray streak, and program and description content.
  - **EXTERNAL COORDINATION (violations).** The **fixed copy→verify→switch→remove order** (I4e); the succession start condition (I5); the timer/RIP update rule (I6); the `maintain()` schedule (I7); the regeneration trigger, budget and exclusion policy (I10); the relinquishment policy (I13).
- Consequence: F1 is revised to the audit's closure sentence. Production closure of the full network is not established under the rule.

**Open Astra items (from the audit §8, no run implied):**
- **Q-A1.** Confirm the step-level split: the four steps are SUBSTRATE, and only their order is the violation. If the steps themselves were ruled coordination, the F1 conclusion would stand, with more items listed.
- **Q-A2.** Rule on birth targeting (`ac9.py` @ `6c6323b`, "every bank with demand"). If it is organization-specific, the W/C/B production clause of F1 also becomes conditional.
- **Q-A3.** Confirm that the fixed rule format (width, first-match order, bank rules always enabled) is generic syntax. If not, the interpreter also becomes coordination.

**What would move each violation into declared state** (future protocols, not proposed here; audit §5):
- a declared, damageable transition table executed by a generic table-driven step, tested with alternative and failing tables;
- thresholds held as maintained parameters;
- table operations on the counter and RIP bits;
- maintenance as program-selected actions;
- the regeneration and relinquishment policies held as declared content.

Then repeat the F3/F4 tests.

**Dependency flags (retained from v1.1):**
- Such a successor may be a new architecture family or need a protected controller. Both need explicit approval.
- Consult #25 says "Do not automatically build a successor."

**Named claim or decision its outcomes would change (NC8).**
- The audit already changed the F1 claim.
- The Astra rulings Q-A1–Q-A3 could change its list of conditions.
- A declared-state successor would change the F1 claim from "not established under this rule" to a tested claim. It is therefore eligible to be proposed, but no proposal is made here (it requires Aidan's decision).

**Simplest rival.** *External coordination*: a host-supplied sequencer and policies that carry the organization while the produced machinery funds their writes. Under the rule, this rival is **not excluded** for succession, reconstruction and repair.

**Evidence:**
- {AUDIT};
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §2;
- `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §3 and §7;
- `DEFINITIONS_CHARTER_v2.md` @ `4b85851` §9;
- `DEPENDENCY_AUDIT_v2_CORRECTION.md` @ `4b85851` ("Supplied operations");
- `ac95.py` @ `a1b9759`.

**Exact missing clarification (v1.1, now supplied).** v1.1 asked for "a substrate-admissibility rule that is stated in advance and independent of this organism". Consult #25 supplies it, and the audit applies it.

**Relevance: YES, high (realized).** The flagship Track A sentence changed (F1).

**Stopping criterion.** **Met** for the audit: each disputed operation is classified and the claim is revised. Remaining: Astra rulings Q-A1–Q-A3 (paper only). No successor is built.

""")

rep("""**Stopping criterion.** If the analytic check shows that no fixed-vs-adaptive gap exists in any admissible world of the declared family, stop and record "not well posed". Do not run organism finals.""",
"""**Stopping criterion.** If the analytic check shows that no fixed-vs-adaptive gap exists in any admissible world of the declared family, stop and record "not well posed **for that declared family**". Do not run organism finals.
- Astra #25 stopping-rule correction (verbatim): "Failure of one adaptive implementation does not retire adaptation of organization as a construct."

**Allocation (Astra #25, verbatim): RETAINED AS A QUESTION.** "Retain as a question, not a standing experimental queue. Require one explicit acquired organizational change and one discriminating prediction before proposing a run."

**Named claim or decision its outcomes would change (NC8).** The status row "New maintenance dependencies acquired autonomously" (NOT ESTABLISHED). No run is proposed until the two requirements above are written down.""")

# U3
rep("""**Exact missing causal test** (ledger `next_falsifier`, made operational).""","""**Exact missing causal test** (ledger `next_falsifier`, made operational; v1.2 adds Astra #25's design requirements after the list).""")
rep("""   - the inactive-queue reduction "production-versus-state-regrowth dependency audit" (`ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`, inactive_theory_queue).
""","""   - the inactive-queue reduction "production-versus-state-regrowth dependency audit" (`ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`, inactive_theory_queue).

**Astra #25 design requirements (verbatim).**
- "First establish that the machinery intervention isolates the proposed pathway without simply disabling computation or changing available resources."
- "For U3, use pathway interruption plus machinery-specific restoration, with resource and immediate-function controls. A single blocking arm is not a complete mediation argument."
""")
rep("""**Relevance: YES, high.** It decides whether closure extends from the material and production layer (O1/O2) to the informational and functional organization (O3), which is the "functional organization" in the Track A question.""",
"""**Relevance (v1.2, corrected per the U1 audit §7).**
- **For the closure sentence (F1): NO under the current code.** Every machinery-repair and regeneration path runs through supplied coordination (audit I7, I10). A positive U3 would change the amount or timing of repair delivered *through* fixed policies without moving any sequence or policy into declared state. A negative U3 removes nothing F1 relies on.
- **For a separate O3 / Q-CAUSE claim: YES.** It would decide ledger O3 (PARTIAL), the content→machinery→content loop.
- **Exception:** if the coordination were first moved into declared state (U1 future protocol), a U3-style loop through that declared table *would* bear on the closure sentence.""")
rep("""**Stopping criterion.** If the clamp arm shows that (b) occurs without (a), the loop reduces to ordinary state estimation; record it REDUNDANT and stop.""",
"""**Stopping criterion (corrected).** If (b) persists under the machinery clamp, the proposed mediation account is defeated. Record "mediation not supported" and stop.
- Astra #25 correction (verbatim): "Persistence of an effect under the U3 machinery clamp defeats the proposed mediation account; it does not prove reduction to ordinary estimation."
- Do not create a reduction entry from that outcome alone.

**Allocation: HELD, NOT PROPOSED.**
- Astra #25 calls it the "Highest-value possible Track A experiment after U1", and its next-step 2 says "Propose that experiment only if the answer is yes" (would U3 change the synthesis conclusion).
- For the closure conclusion the answer is no. For the separate Q-CAUSE claim it is yes.
- Whether to propose a protocol for that separate claim is Aidan's decision, and any protocol needs its own approval.

**Named claim or decision its outcomes would change (NC8).** Ledger layer O3 (PARTIAL), a Q-CAUSE claim. Not F1.""")

# U4-U7, U9 deferred
def defer(anchor_stop, uid, quote, nc8):
    rep(anchor_stop, anchor_stop+f"""

**Allocation (Astra #25, verbatim): DEFERRED.** "{quote}"

**Named claim or decision its outcomes would change (NC8).** {nc8}""")
defer("""**Stopping criterion.** Stop after one pre-registered extended search with no witness, unless a bound becomes feasible. Do not iterate searches (forking paths). Any training needs Aidan's approval.""","U4",
 "Defer. Another failed R-FIX search is unlikely to affect program strategy. Reopen only for a decision that a compensation witness would change.",
 "Only a verified R-FIX witness would change a claim (Q-NECESSITY stays NOT_ESTABLISHED otherwise). Reopen only if a named program decision depends on it.")
defer("""**Stopping criterion.** Stop if step 1 shows the strongly connected component is already minimal and every S-item has an existing ablation. Then record "minimal within the declared component list".""","U5",
 "Defer unless \"minimal\" remains in a publication claim. Remove that adjective otherwise. Graph connectivity and leave-one-out ablations do not establish minimality over compensating alternatives.",
 "Any publication sentence using \"minimal\". This triage makes no minimality claim, and none should be made from connectivity or leave-one-out ablations.")
defer("""**Stopping criterion.** Do not start without explicit authorization. If started, stop at the first prespecified falsification clause.""","U6",
 "Separate ALife successor project requiring an explicit PI decision. Not a prerequisite for Track B.",
 "The clause (ii) whole-organism unity verdict (NOT ESTABLISHED). It requires a PI decision.")
defer("""**Stopping criterion.** Stop at the analytic bound if it is decisive.""","U7",
 "Keep as a documented operating-range limitation. Do an affordability analysis only if the intended claim requires the missing range.",
 "Only a level-(b) robustness claim that needs the missing range. Otherwise it stays a documented operating-range limitation.")
defer("""**Stopping criterion.** Run only if a downstream claim relies on Q-CAUSE strength. Otherwise keep the qualifier.""","U9",
 "Keep the sampled-control qualifier. No new draw-count study without a downstream decision requiring it.",
 "The strength of the PR #9 Q-CAUSE entry (S15) only, if a downstream decision requires it. The sampled-control qualifier is kept.")

# U8 dropped
between('### U8. Survival-level composition','### U9.', """### U8. Survival-level composition (AC115 G4–G7; AC68 bimodality; AC39 transfer) — DROPPED FROM THE ACTIVE QUEUE

**Allocation (Astra #25, verbatim).** "Drop from the active queue."

**Dropped with reason.**
- The survival-bundled gate failures (`AC115_ERRATA_v1.md` @ `e2e2ac6`) stay recorded as failed. S4 keeps its mechanism-level result.
- Resolving them would not change F1 or S4; the mission audit calls it "a known wall". The simplest rival is seed-dependent W/C bistability.
- Reopen only if a closure claim comes to depend on survival (NC8).

""")
# U11 dropped
between('### U11. AC116 storage question','---\n\n## 6. Verification', """### U11. AC116 storage question (suspended at the resolution floor) — DROPPED FROM THE ACTIVE QUEUE

**Allocation (Astra #25, verbatim).** "Drop from the active queue; preserve the suspended result."

**Dropped with reason.**
- The suspended result is preserved as recorded: exact sign-flip p = 0.0625 at n = 8, the floor of the test; "Suspended — not closed, not demonstrated" (`AC116_ERRATA_v1.md` @ `e2e2ac6`; `AC116_RESULTS_v1.md` @ `3ebccdf`).
- S0 records it as "not a license for further storage-comparison runs". The mission audit says it "would not move the architecture".
- No named claim or decision depends on it (NC8).

""")

# U10 rewrite
between('### U10. W-REL exact check','### U11.', f"""### U10. W-REL exact check — EXECUTED AND REVIEWED; formal A-SEP UNRESOLVED-COMPUTE; labels conditional

**Allocation (Astra #25, verbatim).** "Finish the already approved bounded analysis and review it separately."
- Done: executed in PR #11 (https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/11) and reviewed separately in {WREV}.
- Astra #26 then ruled on the review's items: {C26}.

**Status.**
- **Approved** by Aidan at 8:58 AM ET, 2026-10-21 (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`).
- **Formal A-SEP: UNRESOLVED-COMPUTE.** Astra #26 (verbatim): "Under the stated overall gate, the formal A-SEP outcome remains UNRESOLVED-COMPUTE until the missing coverage is completed. This is an incomplete-computation outcome, not a cap-exceeded outcome."

**Conditional classifications** (Astra #26 table, "conditional on completion of required validation"):

| T_SEP | (c_R, c_S) | Classification |
| ---: | --- | --- |
| 3 | (1/50, 3/50) | UNRESOLVED-DESIGN; no donor contrast; C-REF and C-T2 also fail |
| 4 | (1/50, 3/50) | UNRESOLVED-DESIGN; same reasons |
| 3 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET; C-REF and C-SEL fail |
| 4 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET; C-REF fails |

**Review items A1–A4, as ruled by Astra #26.**
- **A1:** "Retain the frozen precedence." UNRESOLVED-DESIGN precedes REFERENCE CRITERIA NOT MET, with the C-REF and C-T2 failures reported. Astra corrects the review's reasoning: the precedence "follows the chosen protocol precedence, not a general rule of logic".
- **A2:** "The coverage qualifier alone is insufficient." This produces the formal UNRESOLVED-COMPUTE above.
- **A3:** "Identity swaps do not supply the missing intervention comparison." MB-myopic reproduction at the two no-contrast settings is **UNRESOLVED**, not YES. The YES comparisons at the two contrast settings "remain provisional comparison results, subject to the validation shortfall".
- **A4, attainability:** "Not immediately." The read-only extraction Astra asked for first is in {ATT}. It finds:
  - **10 of the 12 candidate settings are already ruled out for the reference's core conjunction** from emitted outputs. Six follow from the analytic RESAMPLE-dominance bound (47817/500000 < c_S = 1/10, any horizon). Four follow from the no-RECHECK trap at T ≤ 4.
  - **Only (T_SEP, c_R, c_S) = (3, 1/100, 3/50) and (4, 1/100, 3/50) remain possible.** C-REF passes there exactly, but C-SEL (ii) and rescue are NEEDS-APPROVED-RUN.
- **A5** (v2 only): "The checking ceiling remains FAIL."

**Corrected relevance (NC1, NC7; replaces v1.1's wording).**
- v1.1 said a PATTERN REPRODUCED BY NAMED CONTROL outcome "would add" a reduction entry. That contradicted the W-REL interpretation rules. Astra #25: "PATTERN REPRODUCED BY NAMED CONTROL does not automatically create a REDUNDANT entry."
- Under NC7, such an outcome could only retire, by name, the novelty claim "R-HAC-MB's assessment role is distinguished from the named analytic controls", without negating any retained component result.
- No setting received that label. The reference met its own core criteria in no tested setting, so no separation is supported or refuted, and no reduction entry follows. Astra #26: "These comparisons do not establish absence of an assessment role".

**Retained evidence (bounded facts about supplied analytic agents).** These come from Astra #26 and the review:
- ITEM-1 symmetry audit VERIFIED;
- the value calculations;
- at (4, 1/100, 1/10), the component intervention, C-FO and rescue results.

They do not establish acquired assessment or the complete admission conjunction.

**Q-tags.** Q-EXIST (world/identifiability): ITEM-1. Q-CAUSE: nothing established. Q-LEARN: not tested. Q-NECESSITY: not tested. No change to the C4 evidence or status row. No C4 or consciousness conclusion.

**Simplest rival.** *The battery's own named count-based and policy-only analytic agents* (counting / filtering): R-CONF-A, R-BLIND/R-CONF-S, R-CG counts, R-HAC-MF, the policy-minimized PM-ACT, and MB-myopic.

**Relevance.** Mainly Track B (C4 admission). LOW for Track A.

**Named claim or decision its outcomes would change (NC8).**
- The W-REL ledger row (Astra #26 §B.5 wording).
- The decision whether to prepare an A-SEP successor. A 2-setting reference-only check (NEEDS-APPROVED-RUN) would decide whether any grid setting can host the conjunction; if none can, retire "that finite reference/grid/horizon combination as a successful separation design".

**Stopping criterion.**
- (a) Complete mandatory ITEM-9 validation only under the separate approval Astra #26 §D proposes.
- (b) Make any attainability check a separate decision, limited to the two open settings.
- (c) Do not add costs or horizons after seeing failures.

""")

# ---------- §6 verification ----------
rep("""**v1.1.** `/workspace/scratch/track_a_triage/v1_1/check_v1_1.py`""","""**v1.2.** `/workspace/scratch/track_a_triage/v1_2/check_v1_2.py` (log `check_v1_2.log`) checks this file:
- every `path @ commit` pair exists (`git cat-file -e`, read-only);
- every Astra #25/#26 quotation is a byte-exact substring of the consult file;
- the F1 sentence is byte-identical to the U1 audit's;
- the §1 counts and allocation counts equal the entries;
- the old category name appears only in verbatim quotes and the changelogs;
- forbidden phrases are absent;
- v1 and v1.1 hashes are unchanged.

The dropped U8 and U11 notes intentionally omit the "Exact missing" fields.

**v1.1.** `/workspace/scratch/track_a_triage/v1_1/check_v1_1.py`""")

# ---------- B4 ----------
rep("### B4. W-REL named-rival battery (theory-stage) — METHOD ONLY, RESULTS PENDING","### B4. W-REL named-rival battery (theory-stage) — METHOD; RESULTS EXECUTED AND REVIEWED (formal A-SEP UNRESOLVED-COMPUTE)")
rep("""**METHOD ONLY, RESULTS PENDING.**
- W-REL was approved by Aidan at 8:58 AM ET (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6…7687`) and is currently running.
- This section states the frozen method only. No outcome, label or statistic from the run is reported or implied.""",
f"""**v1.2 status.**
- W-REL was approved by Aidan at 8:58 AM ET (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6…7687`), executed in PR #11, and reviewed in {WREV}.
- Results and their status are in U10. This section keeps the frozen method.""")
rep("""**Status: METHOD ONLY, RESULTS PENDING.** The check is running, and no result has been read by this triage.""",
"""**Status (v1.2).** Formal A-SEP is UNRESOLVED-COMPUTE (Astra #26). Conditional per-setting classifications are in U10.

**Portability lesson (Astra #26 E-W5/E-W6, verbatim).** "The chosen A-SEP settings were not checked prospectively for joint criterion attainability." A Track B study must check criterion attainability and action dominance for its reference *before* freezing its settings.""")
rep("""- **T-OBS: observer-discard.** Discard the host's observational record mid-function. The trajectory endpoint must be byte-identical (`state_hash`). State whether per-tick comparison was done. Source: `AC95_RESULTS_v1.md` @ `d7925cf`.""",
"""- **T-OBS: observer-discard.** Discard the host's observational record mid-function. The trajectory endpoint must be byte-identical (`state_hash`). State whether per-tick comparison was done, and report the result as "endpoint agreement under the audited observer-discard procedure" (F4, Astra #25). Source: `AC95_RESULTS_v1.md` @ `d7925cf`.""")

open(DST,'w',encoding='utf-8').write(s)
print('written',len(s))
