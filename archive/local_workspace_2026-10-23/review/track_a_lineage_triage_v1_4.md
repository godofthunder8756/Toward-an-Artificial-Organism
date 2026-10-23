# Track A lineage triage v1.4: Artificial Autonomy and Organizational Closure

| | |
| --- | --- |
| Owner | Research Delegate (Track A), for Aidan Ahern |
| Date | 2026-10-21. v1 about 10:30 AM ET; v1.1 about 10:45 AM ET; v1.2 built about 11:12 AM–noon ET; v1.3 built about 12:11 PM–1 PM ET; v1.4 built about 2:22–3 PM ET |
| Supersedes | `track_a_lineage_triage_v1_3.md` (sha256 `167c7e67…79b66`), left untouched; built from it by `/workspace/scratch/track_a_triage/v1_4/build_v1_4.py`. v1.3 superseded `track_a_lineage_triage_v1_2.md` (sha256 `84fa9614…fdb09`), built by `/workspace/scratch/track_a_triage/v1_3/build_v1_3.py`. v1.2 superseded `track_a_lineage_triage_v1_1.md` (sha256 `d2cc9152…a5d3ef`), which supersedes `track_a_lineage_triage_v1.md` (sha256 `b4e1a772…7f0b`). Both left untouched. Built deterministically from v1.1 by `/workspace/scratch/track_a_triage/v1_2/build_v1_2.py` |
| Kind | Planning and assessment only (PAPER ONLY). Nothing was run, trained, committed or pushed |
| Repo | `godofthunder8756/Toward-an-Artificial-Organism`, master `32cfbe6` (2026-10-20 1:39 PM ET) |
| PRs read | #3–#10, all open drafts, fetched read-only (heads in §0.2). W-REL results: PR #11 (via the review below; v1.4 also read the PR #11 branch head `dddd63c`, fetched read-only) |
| Astra | Consult #25: `/workspace/astra_consult25_response.txt` (sha256 `31740a1e7129baf9ff9d3c047492fdbe1952970ad836d271742b5a6f14ff8791`). Consult #26: `/workspace/astra_consult26_response.txt` (sha256 `e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12`). Consult #28: `/workspace/astra_consult28_response.txt` (sha256 `1df2fba3189a8217067dd4e13e0c3f5d4b22a25dc7aedabec85d7ee8bd8b96ed`) |
| W-REL | Approved by Aidan at 8:58 AM ET today (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`). Executed in PR #11 and reviewed in `/workspace/review/wrel_results_review_v1.md` (sha256 `60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace`). v1.4 (Astra #29 `/workspace/astra_consult29_response.txt` (sha256 `38056d5597fa3f8b077b7ed5b89c4cd64ea58ec1d6632b7d3d10c8936b352ce8`), checked against the PR #11 record): the verification gap is closed (Addendum A1, `0e17a05`). Addendum A2 attained the reference conjunction at (1/100, 3/50), T_SEP = 3 and 4 (`dddd63c`). Named controls were not evaluated (U10) |
| U1 | Addressed by the U1 audit v1.1 and v1.2 (`/workspace/review/u1_substrate_audit_v1_2.md`; I12 PROVISIONAL), `/workspace/review/u1_substrate_audit_v1_1.md` (built from v1, sha256 `48c174f5…f13a`, which is retained unchanged). Astra #28 rulings applied |

**Standing rules applied.**
- Read-only on the repo and GitHub; scratch work only, outside the repo.
- No runs and no training.
- No consciousness claim, and no C4 or C5 claim. "C1–C5" and "S1–S4" in F1 are the Definitions Charter v2 component and maintained-state criteria, not C-axis levels.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.
- **Systems separation (v1.2/v1.4, per Astra #29).** The maintained-component (AC) lineage (AC1–AC105: closure, repair, succession; F1–F5, U1, U3) and the GRU-8 studies are separate systems. The GRU-8 studies are PRs #8–#10, together with the GRU-8 acquisition and transfer studies in PRs #5 and #7. Their findings do not jointly establish one organism, and no finding from one system is evidence about the other. Astra #29 (verbatim): "Keep findings from different systems separate. The maintained-component lineage and the GRU studies do not jointly establish a single integrated organism. "Bounded neural causal contribution at 8/10" should identify the separate GRU experiment and its declared conjunction."
- In the organism lineage, a result shown by ablation is labelled **within-model ablation dependence**. It is never relabelled Q-NECESSITY, which in this program means necessity of a learned component relative to a declared restricted class (PR #9 and #10 usage).

**Citation convention.**
- `path` @ `commit` names a file and the commit it is read from.
- For master files the commit is the last commit that touched the file.
- For PR files the commit is the PR head, and the PR link is given.
- Every `path @ commit` pair in this document was machine-checked to exist (§6).
- Box files (not in the repo) are cited by absolute path and sha256.
- Anything not verifiable from these sources is marked **UNVERIFIED**.

## Changelog v1.4 against v1.3 (`167c7e67…79b66`)

Paper only. Source: Astra consult #29 `/workspace/astra_consult29_response.txt` (sha256 `38056d5597fa3f8b077b7ed5b89c4cd64ea58ec1d6632b7d3d10c8936b352ce8`). Its W-REL statements were checked against the PR #11 branch (fetched read-only, head `dddd63c`) before being written; the record supports them (U10).
1. **E29-6 added verbatim** (Track A status; §0 and U10). The stale W-REL entries are replaced in the header, §1 counts, U10 and B4, using Astra #29's ledger wording and E29-1. The earlier formal status sentence and the proposed future two-setting check are dropped; v1.2's changelog keeps them as history.
2. **Birth targeting (I12) is PROVISIONAL** (F1, §1, U1). The code evidence is the U1 audit v1.2 §4.2, which states what the code shows and what it does not; Astra #28 is not cited as a code certification.
3. **Systems separation stated** (§0, §3): the AC lineage and the GRU-8 studies are separate systems and do not jointly establish one organism. Each "8/10" contribution now names PR #9 FO+ISO and its per-seed joint rule (S15, S15 rival, U9).
4. **"Resolved by" becomes "would be tested by"** in proposed tests. v1.3 had none outside quotes, so no text changed for this edit; the check confirms none remain.
5. **Other Track A items from #29 Q4** are recorded: Astra's acceptance of the revised closure statement (verdict line). The closure sentence, E28-1 and E28-2 are unchanged. E29-1 and Astra's ledger wording are used only for the W-REL status. E29-2 to E29-5 and E29-7 (W-REL detail, Track B, program boundary) are not applied as Track A edits, and the #29 §D approval question is not approved or proposed here.

## Changelog v1.3 against v1.2 (`84fa9614…fdb09`)

Paper only, under Aidan's planning approval. Source: Astra consult #28, with its named edits used verbatim. E28-3 to E28-10 are Track B items and are not applied here.
1. **E28-1 and E28-2 added verbatim** (F1, U1). The U1 audit v1.1 now splits primitives (SUBSTRATE) from source, destination, precondition, budget, scheduling and next-phase choices (EXTERNAL COORDINATION).
2. **Closure sentence replaced** everywhere by Astra #28's sentence. It is byte-identical to the audit v1.1 and synthesis v1.1. The v1.2 sentence is withdrawn, and C1–C5 for W/C/B are not re-certified.
3. **T1 qualified** (F1): constants are judged by organizational role. The substrate test T1 is distinct from the A0 tests T1–T5 cited in the U entries.
4. **I12 birth targeting** (`ac9.py` @ `6c6323b`) changes from contested to EXTERNAL COORDINATION (supplied targeting). F1's "Excluded?" text and U1 are updated, and Q-A1–Q-A3 are marked as ruled.
5. **Directives recorded** (F1, U1, U3): no further closure runs on the unchanged architecture; the successor transition-table design is SKETCH ONLY, not a proposal; U3 stays on hold. §6 records the v1.3 check script. Two survival-count wordings (R2, T-INTERRUPT) are reworded to avoid the word "alive" outside quotes.

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

1. **Simplest rival, every entry.** All 42 entries (F1–F5, S1–S15, R1–R11, U1–U11) now carry a "Simplest rival" line. It names the simplest established mechanism that could explain the finding, from control theory, RL, dynamical systems, ALife, counting/filtering or external coordination. For F and S entries the line also says whether existing evidence excludes that rival, with citations. F and U entries have it inside their subsection. S and R entries have it in a per-ID list directly under their table.
2. **W-REL.** B4 is labelled **METHOD ONLY, RESULTS PENDING**. U10's status cites the approval record (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6…7687`) and says the check is currently running. The header row is updated to match. No W-REL file or run was touched.
3. **Defaults, not universal rules.** The 8/10 replication bar and the "more than two invalid seeds = UNRESOLVED" rule are restated in B5 as **defaults that each Track B study must freeze in its own protocol**. The PR #8, #9 and #10 wordings are kept as the frozen instances they are. U9's wording follows. B1 and B3 point to B5.
4. **B3 verbatim.** B3 is rebuilt from verbatim excerpts of `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818` (sha256 `eca2121c…ea40`), sliced byte-exactly by the build script. The excerpts cover §1 arms, §3 target and §3.1 dual-evaluator rule, §4 harness and freezing checks, §6 validity, §7 labels, the §8.1 "Not reached" wording and the §8.3 claim ceiling. v1 had condensed the dual-evaluator block onto fewer lines.
5. **Check script.** `/workspace/scratch/track_a_triage/v1_1/check_v1_1.py` (with `.log`) extends the v1 checks with:
   - a Simplest-rival line per ID, and an exclusion statement plus a citation for each F and S entry;
   - byte-exact B3 excerpts;
   - the B4 label;
   - the U10 approval citation and approval-record sha;
   - the defaults wording;
   - v1 unchanged;
   - a reproducible rebuild.

No category assignment, count, rank or finding changed from v1 (v1.1 statement, retained).

---

## 0. Scope, sources and how the categories are used

### 0.1 Track A question (PI directive, as relayed)

Track A asks whether a system can maintain, reconstruct and adapt its own functional organization. Doing so requires five things:
- separating organizational closure from externally coordinated computation;
- establishing causal necessity through interventions;
- identifying minimal organization;
- producing reusable falsification tests for Track B;
- making sure any new experiment resolves a meaningful uncertainty.

### 0.2 Sources

**Authoritative state on master (32cfbe6):**
- Status: `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`.
- Belief ledger: `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`, with its layer assessments O0–O4 and C0–C7, its collapse ledger and its inactive theory queue.
- Mission audit: `ACI_MISSION_AUDIT_v1.md` @ `a50ae55`.
- Prior-art and reduction audit: `ACI_PRIOR_ART_AND_REDUCTION_v1.md` @ `a72136c`.
- **The belief ledger predates PRs #4–#10.** Their ledger entries live inside each PR (cited per entry) and are not merged.

**Draft PRs.** Each was fetched with `git fetch origin pull/N/head` only. Heads:

| PR | Branch | Head | Base | Link |
| --- | --- | --- | --- | --- |
| #3 | restore-d0ee2bb-frozen-results | `efceef3` | master | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/3 |
| #4 | twostream-admission-certificate | `5d9d8a7` | master | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/4 |
| #5 | twostream-acquisition-study | `88b500a` | master | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/5 |
| #6 | scarcity-v2-c3-certificate | `5f65315` | master | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/6 |
| #7 | recurrent-core-transfer | `379bb01` | PR #5 | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/7 |
| #8 | graded-joint-reversion | `a5225eb` | PR #7 | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/8 |
| #9 | first-order-iso-controls | `4f6fc4c` | master (stacked on #8) | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/9 |
| #10 | frozen-recurrent-compensation | `0329818` | master (stacked on #9) | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/10 |

**Earlier independent reviews (box, not in the repo).** These were used for recomputed numbers. Each states that it was recomputed from committed artifacts only:
- `/workspace/review/graded_reversion_results_review_v1.md` (PR #8);
- `/workspace/review/fo_control_results_review_v1.md` (PR #9);
- `/workspace/review/frozen_comp_results_review_v1.md` (PR #10, reviewed at `5f6446f`, before the errata commit `0329818`).

**W-REL documents (box).** These are not in the repo:
- `/workspace/review/c4_reliability_exact_check_spec_FINAL.md`, sha256 `ae626b65…adef`;
- `/workspace/review/c4_reliability_assessment_admission_v3_2.md`, sha256 `f35b6f9d…4207`;
- `/workspace/review/c4_reliability_APPROVAL_RECORD.md`;
- (v1.2) W-REL results review `/workspace/review/wrel_results_review_v1.md` (sha256 `60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace`);
- (v1.2) read-only extraction from existing outputs `/workspace/review/wrel_attainability_from_existing_outputs_v1.md`. Its status lines are historical; the current status is in U10 (v1.4).
- (v1.4) Astra consult #29 `/workspace/astra_consult29_response.txt` (sha256 `38056d5597fa3f8b077b7ed5b89c4cd64ea58ec1d6632b7d3d10c8936b352ce8`).

**v1.2 sources (box).**
- Astra consult #25 `/workspace/astra_consult25_response.txt` (sha256 `31740a1e7129baf9ff9d3c047492fdbe1952970ad836d271742b5a6f14ff8791`);
- Astra consult #26 `/workspace/astra_consult26_response.txt` (sha256 `e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12`);
- U1 substrate audit `/workspace/review/u1_substrate_audit_v1.md` (sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`), and its v1.1 `/workspace/review/u1_substrate_audit_v1_1.md` (v1.3).
- Astra consult #28 `/workspace/astra_consult28_response.txt` (sha256 `1df2fba3189a8217067dd4e13e0c3f5d4b22a25dc7aedabec85d7ee8bd8b96ed`) (v1.3).

### 0.3 Categories (as instructed)

- **FOUNDATIONAL.** Load-bearing for the Track A answer. It survived an intervention or ablation plus at least one named rival or integrity check, and later findings rest on it.
- **SUPPORTING.** Real and correctly bounded, but it carries an auxiliary, infrastructure, prerequisite or context role. It can also be a foundational result's weaker or partly failed sibling.
- **REDUCED OR NO LONGER PRIORITY** (renamed in v1.2, per Astra #25: "I would rename REDUNDANT to "REDUCED OR NO LONGER PRIORITY," with separate fields for retained evidence and future effort. A mechanism can instantiate a real role while being conventional.").
  - This is a **triage-priority** category only. The claimed *extra* mechanism is adequately explained by a named simpler mechanism from control theory, RL, dynamical systems or ALife, so developing that claim further is not a priority.
  - It does not say the measurements were wrong. It does not erase any functional or causal role.
  - Each entry carries the separate fields of NC1 and names its retired claim (NC7). See §4.
- **UNRESOLVED.** The exact missing causal test or formal clarification is stated. Each entry also gives its **relevance**: would resolving it change a scientific conclusion? Each also gives its **stopping criterion**.

- **UNRESOLVED allocation (v1.2).** Each UNRESOLVED entry also carries Astra #25's allocation: ADDRESSED, RETAINED AS A QUESTION, HELD (NOT PROPOSED), EXECUTED AND REVIEWED, DEFERRED, or DROPPED FROM THE ACTIVE QUEUE. It also names the claim or decision its outcomes would change (NC8).

**Astra #25 named changes applied in v1.2 (verbatim):**
- **NC1.** > "Triage priority, retained functional evidence and mechanism novelty are separate fields. Reproduction by a conventional mechanism does not automatically erase a functional role or classify a result as redundant."
- **NC7.** > "Rival reproduction may end development of a claimed novelty without negating retained causal or functional evidence. The claim being retired is named explicitly."
- **NC8.** > "No additional lineage experiment is proposed unless its possible outcomes change a named scientific claim or program decision. Completing an experiment queue is not itself a research objective."

How they are applied:
- **Category is triage priority only.** Retained functional evidence and mechanism novelty are recorded separately: in §4 for reduced entries, and in each F and S entry's evidence and "Simplest rival" lines.
- **No F or S entry claims mechanism novelty.** Several (F5, S6, S11, S12) keep a real functional role even though a conventional mechanism explains them.

Where this triage makes a judgment the repo does not itself record, the entry says **"triage judgment"**.

### 0.4 Repo-integrity note (affects verification, not conclusions)

**Working-tree state.** `git status` in `/workspace/repo` shows 15 tracked `__pycache__/*.pyc` files deleted in the working tree (`__pycache__/` and `e3/__pycache__/`). This triage did not cause it and did not repair it (no repo changes). It does not affect any document cited here.

**Missing frozen rows on master.** Commit `d0ee2bb` (2026-10-02 11:38 PM ET) deleted the frozen rows of 26 result directories from master, including:
- AC67 and AC68;
- AC71 and AC75;
- AC76;
- AC79 (including its seeds-4000 deviation directory) and AC80.

**What PR #3 does.** PR #3 restores them. I compared all 78 deleted paths: the blobs at `efceef3` are identical to `d0ee2bb^` (0 mismatches). Until PR #3 merges, the AC75 and AC79/AC80 row-level evidence cited by K3 cannot be re-audited from master alone.

---

## 1. Summary counts

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
| ADDRESSED (audit done; Astra #28 rulings applied; I12 PROVISIONAL) | 1 | U1 |
| RETAINED AS A QUESTION (no experiment queue) | 1 | U2 |
| HELD, NOT PROPOSED | 1 | U3 |
| EXECUTED AND REVIEWED; verification gap closed; A2 reference conjunction attained; named controls not evaluated | 1 | U10 |
| DEFERRED | 5 | U4, U5, U6, U7, U9 |
| DROPPED FROM THE ACTIVE QUEUE | 2 | U8, U11 |
| **Total** | **11** | |

**Top questions by consequence** (full entries in §5):
1. **U1 / J1, addressed.** Under the consult #25 substrate rule, the sequencing, triggers and policies are external coordination. Production closure of the full declared network is not established under the rule (F1). Astra #28 ruled on Q-A1–Q-A3. Birth targeting is classified as supplied targeting, PROVISIONAL (audit v1.2 §4.2). No further closure runs on the unchanged architecture.
2. **U2.** Can the system adapt its own organization? This is retained as a question, with no experiment queue.
3. **U3.** Does a content intervention propagate to the enabling machinery and back (the O3 constitutive loop)? It does not change the closure sentence and bears only on a separate Q-CAUSE claim. Held, not proposed (on hold per Astra #28).

---

## 2. FOUNDATIONAL

### F1. Production closure (Maturana & Varela clause (i)): foundational only to a conditional claim

**Astra #25 narrowing (verbatim).** "F1 is foundational only to a conditional closure claim. A strongly connected dependency graph does not by itself demonstrate production closure: the edges must distinguish production, enabling conditions, resource dependence and supplied sequencing."

**Substrate rule applied (consult #25, verbatim).**
> "A supplied substrate operation may implement generic state transformation, transport, execution or numerical integration. Organization-specific instructions, maintenance sequences, switching conditions and repair policies must be represented in declared system state rather than hidden in the supplied operation. The substrate must execute alternative admissible instruction contents, including unsuccessful ones, without substituting the intended organization."

**Substrate test T1, qualified (v1.3).** The U1 audit's test T1 ("Generic") is qualified by Astra #28 (verbatim):
> "Also qualify T1: constants are not inherently forbidden. Fixed reaction rates, instruction widths and numerical integration rules can be substrate. Their organizational role, not their being constants, decides the classification."

**Primitive versus policy (Astra #28 edit E28-1, verbatim).**
> "SUBSTRATE classifications apply to generic copy, compare, addressed write and erase primitives. They do not automatically cover the cited routines' source selection, destination selection, preconditions, budgets, scheduling or next-phase assignments. Each such choice is classified separately."

**Finding (v1.3; verbatim from Astra #28 and the U1 audit v1.1 §5; replaces the v1.2 finding, which is withdrawn).**
> The audited system exhibits the reported component-production, repair and reconstruction behavior under supplied organizational coordination. Under the adopted substrate rule, production closure of the full declared network is not established.

**Astra #28 edit E28-2 (verbatim).**
> "The audited system exhibits the reported component-production, repair and reconstruction behavior under supplied organizational coordination. Under the adopted substrate rule, production closure of the full declared network is not established. The birth-targeting rule remains an explicit qualification on the W/C/B production claim."

**Scope (Astra #28, verbatim).** "Retain the individual empirical findings with their original scope. Do not automatically re-certify all C1-C5 criteria for W/C/B through this code-reading exercise."

**Directive (Astra #28, verbatim).** "Stop further closure experiments on that unchanged architecture." "Further runs on the unchanged architecture will not resolve that structural limitation."

**What the repo verdict records (kept as a record, not as this triage's finding).**
- K3 states that every necessary component {W, C, B, description, derived program} meets C1–C5, and that the maintained state {pointer, coordination, route memory, decision state} meets S1–S4.
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
- the code the audit classified: `ac9.py` @ `6c6323b` (birth targeting), `ac9_memory.py` @ `6c6323b` (`demand()`), `ac95.py` @ `a1b9759` (`advance()`, `maintain()`), `ac5_program.py` @ `6c6323b` (`prog.choose`), `ac104.py` @ `343ba17`, `ac105.py` @ `8f0218a`, `ac99_d2.py` @ `8e9ab4a` (U1 audit §3–§4).

**Simplest rival.** *External coordination over an ALife production network*: a conventional artificial chemistry whose turnover is real, but whose organization is held together by a host-supplied scheduler. The belief ledger's O2 rival is "conventional production network under identical substrate".

**Excluded?** Only for the parts the rule classifies as substrate-executed content.
- **Production of W, C and B by program-selected actions:** the action primitives are substrate (U1 audit v1.1 I1–I3, I12-p, I14). However, birth targeting at `ac9.py` @ `6c6323b` (line 108, "every bank with demand") is classified **EXTERNAL COORDINATION (supplied targeting), PROVISIONAL**. Astra #28's judgment was provisional on the supplied description. The code evidence is the U1 audit v1.2 §4.2: a host-written bank list selects which functional W groups receive births. That reading does not show necessity for any W/C/B result. It remains an explicit qualification on the W/C/B production claim (E28-2). Forced enablement of the bank rules is a disclosed expressivity restriction (audit v1.1 I3r).
- **Every coordinator *write* is W-gated** through `_cap` (`AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §2). Per named change 2, this shows the gate matters. It does not internalize the sequence: > "Track A's substrate rule is fixed before further runs. Organization-specific maintenance sequencing must be represented in declared system state; a supplied resource gate alone does not internalize the sequence it enables."
- **Not excluded for succession, reconstruction and repair.** Under the rule, these are EXTERNAL COORDINATION (U1 audit v1.1 I4a-s–I4d-s, I4e, I5, I6, I7, I10 and I13):
  - the next-slot destination, the authorize-on-compare step and the erase-previous-slot choices;
  - the fixed copy→verify→switch→remove order, the start condition and the timer coupling;
  - the `maintain()` schedule, the regeneration policy and the relinquishment policy.

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

### F5. Reconstruction of the working program from the maintained description

**Finding.**
- AC79→AC80: a generic decode replaces the external recipe, with `rebuild == prog.program` bit-for-bit.
- AC85: masks and actions are stored.
- AC87: an order-preserving decode reproduces the acquired layout.
- The derived program (C9) is a necessary component in K3, and the description with its repair is necessary (K3 §5).

**Evidence:**
- `AC79_RESULTS_v1.md` @ `9245cef`;
- `AC80_RESULTS_v1.md` @ `6a1f4fb`;
- `AC87_RESULTS_v1.md` @ `dc3e428` (seeds 4028–4031, 320 rows, nine gates pass);
- K3 table rows "description" and "program" in `CLOSURE_VERDICT_v1.md` @ `4b85851`.

**Simplest rival.** Either of two mechanisms:
- *An external recipe*: the host re-supplies the program (external coordination).
- *Template copying*: ALife self-replication by copying inherited content, with no reconstruction from the organism's own description.

**Excluded?**
- **The external recipe: yes.** The generic decode replaces `prog.program`, and the rebuild equals it bit-for-bit (`AC80_RESULTS_v1.md` @ `6a1f4fb`; K3 table in `CLOSURE_VERDICT_v1.md` @ `4b85851`).
- **Template copying: not excluded, and not claimed.** Reconstruction decodes inherited, maintained content. The decode format is supplied substrate (`CLOSURE_VERDICT_v1.md` @ `4b85851` §3 item 2), and content invention is blocked (R10).

**Why foundational.** It is the "reconstruct" leg of the Track A question.

**Verification caveat.**
- On master, `ac79_results_v1/`, `ac79_engineering_v1/`, `ac79_deviation_seeds4000_v1/` and `ac80_results_v1/` are absent (deleted in `d0ee2bb`).
- They are restored blob-identical by PR #3 (`ac80_results_v1/rows.jsonl` @ `efceef3`).
- Row-level re-audit from master is therefore **UNVERIFIED** until PR #3 merges.
- Content inherited at development is permitted (charter C4). Content *self-production* is a separate question (R10).

---

## 3. SUPPORTING

**Systems separation (v1.2/v1.4, per Astra #29).** The maintained-component (AC) lineage (AC1–AC105: closure, repair, succession; F1–F5, U1, U3) and the GRU-8 studies are separate systems. The GRU-8 studies are PRs #8–#10, together with the GRU-8 acquisition and transfer studies in PRs #5 and #7. Their findings do not jointly establish one organism, and no finding from one system is evidence about the other. Astra #29 (verbatim): "Keep findings from different systems separate. The maintained-component lineage and the GRU studies do not jointly establish a single integrated organism. "Bounded neural causal contribution at 8/10" should identify the separate GRU experiment and its declared conjunction." S12–S15 are GRU-8 findings; the other rows here concern the AC lineage or evidence integrity.

| ID | Finding (bounded) | Evidence (path @ commit; PR) | Role / why not foundational |
| --- | --- | --- | --- |
| S1 | AC1–AC4 building blocks confirmed on fresh seeds 5100–5507: paid maintenance of acquired controller information, produced and decaying repair constituents, produced energy-conversion machinery, and a produced boundary with transport effects. AC1, AC2 and AC4 confirm at every declared rate; AC3 confirms at 2/3 rates, with one death recorded (7/8) | `AC1_4_CONFIRMATION_RESULTS_v1.md` @ `9245cef`; `AC1_RESULTS_AND_NEXT_STEP.md` @ `6c6323b`; `AC2_RESULTS_v1.md` @ `6c6323b`; `AC3_RESULTS_v1.md` @ `6c6323b`; `AC4_RESULTS_v1.md` @ `6c6323b` | Components that F1 composes. Same-author confirmation; external peer review is still open (status table row "Independent review") |
| S2 | Description *succession* (copy→verify→switch→remove). The description holds 130/130 bits under succession; without maintenance it degrades by 23–46 bits and the individual dies | `AC80_RESULTS_v1.md` @ `6a1f4fb`; `AC86_RESULTS_v1.md` @ `ae3504a`; `AC87_RESULTS_v1.md` @ `dc3e428`; K3 §5 in `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` | **Capability, not the survival load-bearer**: "in-place repair alone also survives" (A3 §5, verbatim sense). Supports "reconstruct", but replacement is not shown necessary at the 16,384-tick horizon |
| S3 | Boundary-mediated exchange at the material layer (SR-2 site gate). D1 (site vs count), D2 (local) and D3 (semipermeability) each 16/16, on seeds 6500–6507 | `AC114_RESULTS_v1.md` @ `56ea176`; `A4_EXCHANGE_VERDICT_v1.md` @ `508ea30`; `I1_BOUNDARY_CORRECTION_v1.md` @ `508ea30` | The I1 correction limits AC114's closure to {W, C, B}; the five-component verdict does not transfer to AC114. Material layer only |
| S4 | Exchange composes with the five-mechanism closure. G1, G2, G3 and G8 are 16/16 (mechanism level). The survival gates fail on a minority of finals and are retained as failed: G4/G5 2/16, G6 4/16, G7 6/16 | `AC115_RESULTS_v1.md` @ `dfa19ed`; `AC115_ERRATA_v1.md` @ `e2e2ac6`; `I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` @ `eb79ecb`; `A0_AUTONOMY_VERDICT_v1.md` @ `eb79ecb` | Mechanism-level composition. The survival level is not confirmed (U8, dropped from the active queue) |
| S5 | Level (b) "adaptive autonomy": internalized decision state (Gray streak + allowance-42) held in maintained, damageable, W-gated state. AC105: no survival reversal or relinquishment harm on 80 matched comparisons; it rescues one marginal priority (5804) | `AC96_RESULTS_v1.md` @ `d7925cf`; `AC99_RESULTS_v1.md` @ `4813cf1`; `AC100_RESULTS_v1.md` @ `58094fb`; `AC104_RESULTS_v1.md` @ `98828b5`; `AC105_RESULTS_v1.md` @ `daf421c`; `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1 row 2 | **Supporting for closure** (the S1–S4 decision-state item). **The decision *rule* is classified REDUCED OR NO LONGER PRIORITY (R4)**, and its economics are UNRESOLVED (U7). The repo calls level (b) "ESTABLISHED" (K3 §7); this triage keeps the internalization and separates out the adaptivity claim |
| S6 | Route memory (C7) acquired from the organism's own contact outcomes. AC7: 8/8 correct routes, with targeted erasure causing failure in 6/6 changed-mapping cases. AC8: 8/8 reacquire after remapping, against 0/8 frozen. AC75: erase-on-relinquishment passes all eight gates, and the no-erase rival dies 8/8 under change | `AC7_RESULTS_v1.md` @ `6c6323b`; `AC8_RESULTS_v1.md` @ `6c6323b`; `AC75_RESULTS_v1.md` @ `86aa64d`; `ac75_results_v1/rows.jsonl` @ `efceef3` (PR #3) | Necessary income path in K3. The acquisition mechanism is ordinary trial-and-error association (AC7 itself notes "random ports also viable"). AC75 rows are absent on master (PR #3) |
| S7 | Content↔maintenance coupling for a maintained one-bit cause estimate, after the AC106 correction. AC107: discrimination 0/32 mistakes; storage maintenance confirmed; content-causal (Q2) not established on finals. AC108: both directions, with all seven gates passing. Maintenance→accuracy/use is 16/16. Content→adaptation/production is 16/16 in the move direction. The survival reversal is 12/16 | `AC107_RESULTS_v1.md` @ `ad53ff1`; `AC108_RESULTS_v1.md` @ `5c0b2f1`; ledger O3 = PARTIAL | This is the program's best "maintenance ↔ content" coupling, but ledger O3 marks the constitutive loop PARTIAL (U3). The causal role is behavioural, not survival-level |
| S8 | AC106 corrective work: errata K1 (nine overreach points). It establishes that the AC106 negative is "falsified in engineering" only and that its scope is the candidate *as implemented*. The update rule dropped the `bound` flag (P2), and r4 was never a longer-threshold counter (P1: `HOLD_N == STREAK_N`) | `AC106_ERRATA_v1.md` @ `d8fd25b`; `AC106_ENGINEERING_v1.md` @ `db0ef2f` | Method and scope correction. It prevented a structural-falsification overclaim and fed the AC107 fix |
| S9 | Composition of the estimate with the autonomy architecture. Direct channels are clean (G2, G4, G6 pass). G3/G5 are 12/16 and retained: the corrupted contact rule reschedules reacquisition on 6306 and 6307 | `AC111_RESULTS_v1.md` @ `6b5f163` | Partial composition. The failure is a named interference, not a closure gap |
| S10 | PR #3: frozen result files deleted in `d0ee2bb` are restored blob-identically. I verified 78/78 paths (0 mismatches against `d0ee2bb^`) | `RECOVERY_MANIFEST_d0ee2bb_v1.md` @ `efceef3`; PR #3 | Evidence-integrity prerequisite for F5, S6 and R1 row-level audits. Merge is pending |
| S11 | PR #4: two-stream world-admission certificate **ADMIT**. Exact enumeration over 256 histories, gates (i)–(iv). Per its claim ceiling, "the ordinary three-number chart is the joint posterior in different coordinates" | `twostream_results_v1/RESULTS.md` @ `5d9d8a7`; `TWOSTREAM_PROTOCOL_v1.md` @ `5d9d8a7`; PR #4 | Benchmark infrastructure for W2. Its claim ceiling excludes C2/C3 promotion and organism claims |
| S12 | PR #5: two-stream acquisition. E1 (predictive acquisition) SHOWN. E2 RECURRENT ADAPTATION SUPPORTED. E3 NOT LOCALIZED BY THIS INTERVENTION. The K-FR E3 label is UNRESOLVED, and K-EXACT is NOT CONFIRMED | `acquisition_results_v1/RESULTS.md` @ `88b500a`; `acquisition_results_v1_errata/ERRATUM_v1_claim_ceiling.md` @ `88b500a`; PR #5 | **Q-LEARN** prerequisite for PR #7–#10. Not a Track A closure result |
| S13 | PR #7: recurrent-core transfer. TRANSFER SHOWN 10/10 and E1 REPLICATED 10/10. Matrix-specific reversion is not demonstrated: SPECIFIC(r) 1/10, (z) 3/10, (n) 3/10 | `results_v1_errata/RESULTS_v2.md` @ `379bb01`; `RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md` @ `379bb01`; PR #7 | **Q-LEARN** (transfer) only; it is the prerequisite for PR #8–#10. The matrix-specific negative is recorded; it is not a reduction entry |
| S14 | PR #8: graded joint recurrent reversion. **Q-CAUSE, organization level: SUPPORTED, BOUNDED.** 9/10 fresh seeds (200–209) exceed every one of 32 block-norm-matched isotropic paths and meet materiality. The secondary single blocks are r 0/10, z 0/10 and n 5/10. Four passing seeds have a margin under 10% | `graded_reversion_results_v1/PHASE_B_RESULTS_v3.md` @ `a5225eb`; `graded_reversion_results_v1/results_v1_errata/ERRATA_v3.md` @ `a5225eb`; `GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb`; PR #8 | Superseded in strength by S15, which adds the first-order-matched family. **Q-CAUSE only; Q-NECESSITY not tested** |
| S15 | PR #9: graded joint reversion exceeds **both** first-order-matched and isotropic controls. REPLICATED at **exactly 8/10** under its declared per-seed joint rule (D_FO and D_ISO in each seed, with materiality M): D_FO 10/10, D_ISO 8/10, D_FO and D_ISO 8/10, M 10/10, joint 8/10. GRU-8 system, separate from the AC lineage. Seeds 300 and 301 each lose to a single isotropic draw. Three seed–family margins are under 10% | `first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`; `first_order_control_results_v1/results_v1_errata/ERRATA_v1.md` @ `4f6fc4c`; `first_order_control_protocol_FINAL.md` @ `4f6fc4c`; PR #9 | The strongest neural **Q-CAUSE** result: a bounded causal contribution of trained weight_hh to prefix-dependent prediction, with the surrounding computation fixed. It is **at the boundary** (U9). It is causal contribution, not necessity, and therefore not foundational for Track A's necessity, closure or minimality aims |

**Simplest rival per supporting entry (with exclusion status).**

- **S1. Simplest rival:** *common resource starvation in a generic dissipative chemistry* (dynamical systems / ALife).
  - *Partly excluded:* the AC2 clamped-information contrast and catalyst rescue ("bounded evidence", `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`), plus fresh-seed confirmation (`AC1_4_CONFIRMATION_RESULTS_v1.md` @ `9245cef`).
  - *Not excluded* at AC3's third rate, which had one death (7/8).
- **S2. Simplest rival:** *in-place repair by redundancy and majority restore* (error-correcting storage).
  - *Not excluded:* "in-place repair alone also survives" (`AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §5). That is why succession is a capability, not the load-bearer.
- **S3. Simplest rival:** *an aggregate count-based intake gate, or a supplied exchange law* (control theory / external coordination).
  - *The count gate is excluded:* D1 site-vs-count is 16/16 (`AC114_RESULTS_v1.md` @ `56ea176`).
  - *The supplied law is not excluded:* the "Exchange *law* (gated react actions) still supplied" (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1 row 3).
- **S4. Simplest rival:** *externally coordinated, non-interacting modules* (external coordination; ledger O4 rival "externally coordinated modules").
  - *Excluded at mechanism level:* G1 byte-identity to AC105 and the G2/G3 discriminations, with all six functions exercised in the same organisms 16/16 (`AC115_RESULTS_v1.md` @ `dfa19ed`).
  - *Not excluded for whole-organism unity:* O4 NOT_ESTABLISHED (`I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` @ `eb79ecb`).
  - *Not excluded at survival level:* G4–G7 retained as failed (`AC115_ERRATA_v1.md` @ `e2e2ac6`).
- **S5. Simplest rival:** for the internalization, *a host-side counter* (external coordination); for the rule, *a fixed failure-count threshold with a fixed budget* (control theory; R4).
  - *The host counter is excluded* as the steering memory: observer-discard 8/8, with the streak held in maintained, W-gated state (`AC96_RESULTS_v1.md` @ `d7925cf`).
  - *The fixed-threshold rival is not excluded* (R4).
  - *Note:* the host control *outperforms* the internalized streak economically, 8/8 vs 2/8 relinquish (same file; U7).
- **S6. Simplest rival:** *blind random-port search, or tabular associative (bandit) learning* (RL).
  - *Blind search is excluded* as the explanation of use: targeted erasure causes failure in 6/6 changed-mapping cases (`AC7_RESULTS_v1.md` @ `6c6323b`); remapped reacquisition is 8/8 vs 0/8 frozen (`AC8_RESULTS_v1.md` @ `6c6323b`); no-erase dies 8/8 (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.4 item 3).
  - *Blind search is not excluded for viability:* "random ports also viable" (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`).
  - *Associative learning is not excluded* and is not claimed to be.
- **S7. Simplest rival:** *a same-information direct (reactive) diagnostic, or the first-order streak counter* (counting / filtering).
  - *Not excluded for storage:* the direct diagnostic matches 48/48 in the clean world (`AC109_ENGINEERING_v1.md` @ `d7e24fa`).
  - *Excluded for maintenance→content:* cutting the paid write leaves the estimate inaccurate 16/16 (`AC108_RESULTS_v1.md` @ `5c0b2f1`).
  - *Content→adaptation* (force_machinery 16/16) shows that the content is used. It does not distinguish maintained content from the same content read directly.
- **S8. Simplest rival:** *implementation defect*, not structural absence. The update rule dropped `bound`, and r4 duplicated r2.
  - *Adopted rather than excluded:* the errata endorses this reading (`AC106_ERRATA_v1.md` @ `d8fd25b` P1, P2).
- **S9. Simplest rival:** *independent superposition* (two mechanisms that do not interact).
  - *Excluded for the direct channels:* G2, G4 and G6 pass (`AC111_RESULTS_v1.md` @ `6b5f163`).
  - *Refuted as the full account:* the interference on 6306 and 6307 (G3/G5 12/16) shows a real interaction.
- **S10. Simplest rival:** *regenerated or altered files substituted for the originals.*
  - *Excluded:* all 78 restored blobs equal `d0ee2bb^` (this triage, `git rev-parse` comparison; `RECOVERY_MANIFEST_d0ee2bb_v1.md` @ `efceef3`).
- **S11. Simplest rival:** *an ordinary Bayesian joint filter* (counting / filtering).
  - *Not excluded, by design.* The certificate states that the chart *is* the joint posterior in different coordinates. Its claim ceiling forbids reading more into it (`twostream_results_v1/RESULTS.md` @ `5d9d8a7`). The mean-field arm was "not run" (same file).
- **S12. Simplest rival:** *a product-of-marginals (mean-field) filter, or readout-only learning on a fixed core* (counting / filtering; reservoir computing).
  - The labels are E1 SHOWN, E2 RECURRENT ADAPTATION SUPPORTED and E3 NOT LOCALIZED (`acquisition_results_v1/RESULTS.md` @ `88b500a`).
  - Which comparison E2 uses to exclude the readout-only rival is **UNVERIFIED in this triage** (not re-read).
  - Localization is not established.
- **S13. Simplest rival:** *readout and gain tuning on a fixed recurrent core* (reservoir computing / echo-state networks).
  - *Excluded within the declared grid:* "ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED (10/10), within the declared grid", and F-INIT A-FIT 0/10 (`results_v1_errata/RESULTS_v2.md` @ `379bb01`).
  - *Not excluded outside the grid:* selection hit the grid edge, g=2 in 10/10 seeds (same file).
- **S14. Simplest rival:** *generic loss-aligned displacement*: any equal-norm perturbation with a large first-order loss projection (first-order sensitivity).
  - *Not excluded by PR #8*, which used isotropic controls only (`GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb` §4).
  - PR #9 addresses it (S15).
- **S15. Simplest rival:** *first-order (tangent-matched) displacement, and isotropic equal-norm displacement.*
  - *Excluded at 8/10 for the sampled families,* in PR #9 FO+ISO (GRU-8) under the per-seed joint rule D_FO and D_ISO (with M): D_FO 10/10, D_ISO 8/10, joint 8/10 (`first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`).
  - *Not excluded for:*
    - unsampled perturbation families;
    - single extreme draws (each failing seed lost to one ISO path);
    - readout-compatibility disruption ("does not eliminate differential disruption of compatibility among recurrent matrices, input weights, biases and the readout", `GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb` §4).

**Context-only PR (listed for completeness, not a Track A finding).** PR #6, the scarcity_v2 C3 pressure-and-representability certificate:
- Corrected labels: SEL ADMIT, ACC REJECT-SIG, UPK and UPK_cue ADMIT, ROUTE ADMIT, ADAPT VALUE-ONLY.
- Sources: `scarcity_v2_study/results_v1_errata/RESULTS_v2.md` @ `5f65315` and `scarcity_v2_study/SCARCITY_V2_PROTOCOL_FINAL.md` @ `5f65315`.
- It certifies existence inside specified mathematical policy classes. It is a Track B (C3) input and is not counted in §1.

---

## 4. REDUCED OR NO LONGER PRIORITY (named simpler mechanism)

| ID | Claimed extra mechanism | Reduces to (named mechanism, field) | Evidence (path @ commit) | Retained functional evidence |
| --- | --- | --- | --- | --- |
| R1 | Self-monitoring and self-repair loop (AC67/AC71): "pays to repair its own corruption" | **Fault detection with a fixed corrective action**: a watchdog or threshold-triggered homeostatic regulator (control theory). One bit drives one fixed action, read from host-side observation each tick; nothing is stored, maintained or produced | `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.6 item 1; collapse ledger "watchdog self-monitor" in `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`; `AC71_RESULTS_v1.md` @ `a7f417d` (rows in PR #3) | The read/repair *convention* lesson (AC67→AC71): align the read threshold with the repair trigger. That is engineering, not cognition |
| R2 | Adaptive maintenance allocation / "acquire the need to allocate or relinquish" (AC11) | **State-blind open-loop duty cycle at a fixed level** (control theory). Fixed duty 1/2 gives 4/6 surviving, and the adaptive family matches it or is beaten by it; the learner's own threshold is irrelevant. "The optimum can be a level, not a switch" | `AC11_DESIGN_CONTROLS_v2.md` @ `c348a67`; `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.6 item 6 | The rule "sweep the fixed-level family before claiming a switch" (Appendix B6). The question was "not well posed here" (U2) |
| R3 | Experience-dependent exploration adjustment (AC6) | **Constant-rate exploration** (RL: fixed-ε exploration). Fixed rates 1/1024 and 1/2048 pass all original AC6 behavioural criteria on eight new seeds, with no net material saving | `AC6_FIXEDRATE_RESULTS_v1.md` @ `6c6323b` | Local relinquishment and reacquisition are viable; adaptivity of the rate is not needed |
| R4 | *Adaptivity* of the internalized decision rule (Gray streak threshold + allowance-42), as distinct from its internalization (S5) | **Failure-count threshold with a fixed budget** (control theory: counter/integrator threshold with saturation; a sequential-test stopping rule). Gray coding is "a cost lever, not a semantic change"; the reserve designs AC97/98 starve the decision they fund; AC102/103 find no universal spending policy. **Triage judgment**: the repo labels level (b) ESTABLISHED and does not reduce the rule | `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1 row 2 and §2.1 item 3; `AC106_ENGINEERING_v1.md` @ `db0ef2f` (r2 = "the frozen Gray streak (STREAK_N=6, the history-based rival)") | The internalization (S5) |
| R5 | AC106 maintained cause-belief (second-order "E_world vs E_machinery" estimate) | **The frozen first-order failure-streak counter** (r2); in control terms, counter-based change detection. Errata P8: "the estimate is redundant with the frozen first-order machinery" | `AC106_ERRATA_v1.md` @ `d8fd25b` P8; `AC106_ENGINEERING_v1.md` @ `db0ef2f` (engineering seeds 0–7, 288 rows) | Integration is not falsified (P8: observer-discard passes). The errata's "redundant" is a utility claim about the implementation as built (P2 defect) |
| R6 | Persistent storage of the cause estimate (AC109, clean two-cause world) | **Reactive policy on a sufficient current observation**: a direct diagnostic read at decision time (RL/control: Markov reactive controller). It matches the stored estimate on 48/48 cells at lower cost | `AC109_ENGINEERING_v1.md` @ `d7e24fa` | Content is load-bearing as a selector (S7); storage is not, where the observation is decisive. History load-bearing by design is C2 (`C2_TASK_DESIGN_v1.md` @ `6875f38`) |
| R7 | "Continuous repair sustains the estimate's correctness" (AC110) | **Re-estimation from fresh evidence** (filtering: state re-derived at open in-window contacts; reacquisition). G2/G3 16/16 independent of repair; repair matters only post-window (G4 8/16) | `AC110_RESULTS_v1.md` @ `928b938` | Correctness and retention are temporally separable (Appendix B7) |
| R8 | Reliability "monitor" as a second-order predictor (AC117 harness) | **Directional-repair control** (control theory). Prediction is matched by the transient damage count `ones>=4`, and the harness is vacuous at ambient damage | `AC117_RESULTS_v1.md` @ `bd26525` (seeds 6800–6815) | CONTROL-yes, PREDICTION-no. The W-REL exact check is the program's current theory-stage follow-up (U10) |
| R9 | Graded / weighted posterior (C4 probe, P2/R2, AC113) | **Integer counting statistic with a threshold** (sequential probability-ratio rule, `N = ceil(logit θ/LR)`). AC113: no demonstrated advantage (sign-flip p ≈ 0.71 / 0.63, n=8) | `R1_AC113_REANALYSIS_v1.md` @ `38a19ae`; `AC113_RESULTS_v1.md` @ `aebb753`; `R2_P2_PROOF_CORRECTION_v1.md` @ `38a19ae` | Cognition-track cross-reference. "Format is not cognitive necessity" |
| R10 | Self-directed content production (AC72/73/77/78) | **Convergence to a path-dependent, seed-specific fixed point** (dynamical systems; N_eff ≈ 1 per life). Content self-production is blocked structurally, not by a weak learner | `AC78_ENGINEERING_v1.md` @ `9245cef`; `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.6 item 8 | Inherited content is permitted (charter). Organization regeneration and content invention are separate problems |
| R11 | Explicit maintained self-state V for allocation (neural bridge, Phase II) | **Same-information reactive policy and a 3-line sufficient-statistic threshold rule** on raw observables (control/RL). P_rb matches the candidate (op 0.823 vs 0.895, sign-flip p = 0.64); rule 9_d attains the oracle (op 1.000) | `BRIDGE_PHASE2_VERDICT_v1.md` @ `40528f8`; ledger O1/C1 counterevidence | "Explicit V is unnecessary in the tested task" |

**Simplest rival per reduced entry.** For REDUCED OR NO LONGER PRIORITY entries the simplest rival *is* the reduction, and existing evidence supports it.

- **R1. Simplest rival:** watchdog fault detection with a fixed corrective action (control theory).
- **R2. Simplest rival:** state-blind open-loop duty cycle at a fixed level (control theory).
- **R3. Simplest rival:** constant-rate (fixed-ε) exploration (RL).
- **R4. Simplest rival:** failure-count threshold with a saturating counter and a fixed budget (control theory; sequential stopping rule). This remains a triage judgment.
- **R5. Simplest rival:** the frozen first-order failure-streak counter, used as counter-based change detection (counting / filtering).
- **R6. Simplest rival:** a reactive (Markov) policy on the decisive current observation (RL / control).
- **R7. Simplest rival:** re-estimation from fresh in-window evidence, i.e. filtering refresh or reacquisition (counting / filtering).
- **R8. Simplest rival:** directional-repair control plus a transient damage count `ones>=4` (control theory / counting).
- **R9. Simplest rival:** an integer counting statistic with a threshold, as in a sequential probability-ratio rule (counting / filtering).
- **R10. Simplest rival:** convergence to a path-dependent, seed-specific fixed point (dynamical systems).
- **R11. Simplest rival:** a same-information reactive policy, or a 3-line sufficient-statistic threshold rule (control / RL).

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

---

## 5. UNRESOLVED (exact missing test or clarification, relevance, stopping criterion)

Ranked by consequence for a Track A conclusion. **Relevance** asks: would resolving this change a scientific conclusion on record?

### U1 (rank 1). J1: supplied coordinator and interpreter — substrate, or externally coordinated computation? **ADDRESSED by the U1 audit v1.1; Astra #28 rulings applied**

**Allocation (Astra #25, verbatim).** "Resolve now by specification and code audit. Stop after classifying each disputed operation and revising the claim. Do not automatically build a successor."

**Status: ADDRESSED** by `/workspace/review/u1_substrate_audit_v1_1.md` (built from v1, sha256 `48c174f5…f13a`, which is retained unchanged).
- v1.3: Astra #28 (verbatim): "Track A: ACCEPT THE MAIN AUDIT CONCLUSION, WITH NAMED CORRECTIONS. Under the adopted substrate rule, full production closure is not established. Further runs on the unchanged architecture will not resolve that structural limitation."
- The finite rule is consult #25's, quoted verbatim in F1.
- The audit classified every disputed operation of the AC105 code path, with file:line@commit citations machine-checked against master `32cfbe6` and `db0ef2f`:
  - **SUBSTRATE (primitives only, per E28-1).** The interpreter `prog.choose`; decode; `build_program`; the copy, compare, atomic-write and erase primitives inside COPY, VERIFY, SWITCH and REMOVE; majority-restore; `reg_from_active`; the `_cap` W gate; the action primitives; observation and conservation.
  - **DISCLOSED EXPRESSIVITY RESTRICTION.** Forced enablement of bank rules (I3r).
  - **DECLARED-STATE.** The phase, pointer and ACTIVE bits, the timer counter and RIP bit, the Gray streak, and program and description content.
  - **EXTERNAL COORDINATION (violations).** The routines' source, destination, precondition, budget and next-phase choices (I4a-s–I4d-s); **birth targeting** at `ac9.py` @ `6c6323b` (I12, supplied targeting, PROVISIONAL); the **fixed copy→verify→switch→remove order** (I4e); the succession start condition (I5); the timer/RIP update rule (I6); the `maintain()` schedule (I7); the regeneration trigger, budget and exclusion policy (I10); the relinquishment policy (I13).
- Consequence: F1 is replaced by Astra #28's closure sentence (F1). Production closure of the full declared network is not established under the rule.

**Astra items: ruled by consult #28 (audit v1.1 §8).**
- **Q-A1: ruled too narrow.** "The primitive/policy distinction is right, but "the four steps are substrate, and only their order violates the rule" is too narrow." Applied as E28-1.
- **Q-A2: provisional judgment (Astra #28), now PROVISIONAL in v1.4.** "For `ac9.py:108`, "every bank with demand" is not necessarily a priority ordering. It is a supplied production-targeting rule. On the description provided, I would not clear it as generic chemistry yet." The audit v1.1 §4.1 gives the code-level explanation. Astra #29 (verbatim): "My #28 birth-targeting judgment was provisional on the supplied description. If audit v1.1 now establishes that the implementation performs semantic host targeting, cite that new evidence. Do not describe #28 alone as an unconditional code certification. I cannot certify the unavailable audit's new details from this synthesis." The audit v1.2 §4.2 sets out what that code reading establishes and what it does not.
- **Q-A3: partly ruled.** Fixed width, first-match order and the instruction vocabulary can be admissible syntax. Forced enablement is disclosed as an expressivity restriction (I3r). Whether it hard-wires an organization-specific action remains open, on paper only.

**Directive (Astra #28, verbatim).** "Stop further closure experiments on that unchanged architecture." "Further runs on the unchanged architecture will not resolve that structural limitation."

**What would move each violation into declared state: SUCCESSOR DESIGN, SKETCH ONLY, NOT A PROPOSAL** (audit v1.1 §5 and §4.1):
- a declared, damageable transition table executed by a generic table-driven step, tested with alternative and failing tables;
- thresholds held as maintained parameters;
- table operations on the counter and RIP bits;
- maintenance as program-selected actions;
- the regeneration and relinquishment policies held as declared content;
- declared demand markers read by a generic birth reaction, in place of the host bank list.

Astra #28 (verbatim): "A damageable transition table is a plausible successor design, but moving Python branches into an array is insufficient." Requirements it lists (verbatim):
- "Production, copying, repair and replacement of the table itself."
- "Its triggers, addressing rules, budgets and exclusions."
- "The mechanism that schedules its execution."
- "Bootstrapping and inherited initial content."
- "Whether corrupted but admissible tables execute without host restoration of the intended policy."
- "Any protected interpreter state or hidden backup."
- "An inherited initial table is compatible with the declared convention. An indefinitely protected host copy that reinstalls it would preserve the problem."

Astra #28 (verbatim): "My recommendation is to close the present Track A claim and retain a short successor design sketch. Do not build the successor automatically." "Implementation and testing require a separate, concrete approval. A protected controller is not inherently necessary." Aidan's planning-only approval: "It does not authorize a hand-built simulation, online adaptation, an HRL comparison run or a Track A architectural successor."

**Dependency flags (updated per Astra #28):**
- Architecture taxonomy does not determine authorization ("that terminology should not determine authorization"), and a protected controller is not inherently necessary. Implementation and testing need separate, concrete approval.
- Consult #25 says "Do not automatically build a successor."

**Named claim or decision its outcomes would change (NC8).**
- The audit already changed the F1 claim.
- The Astra #28 rulings changed its list of conditions (v1.3: E28-1, I12).
- A declared-state successor could change the F1 claim from "not established under this rule" to a tested claim. Per Astra #28 it stays a SKETCH ONLY and is not proposed; any proposal requires Aidan's separate, concrete approval.

**Simplest rival.** *External coordination*: a host-supplied sequencer and policies that carry the organization while the produced machinery funds their writes. Under the rule, this rival is **not excluded** for succession, reconstruction and repair.

**Evidence:**
- `/workspace/review/u1_substrate_audit_v1.md` (sha256 `48c174f5780f8bdaff8ed6b55ee06d32ca97e781920d9d78adc361299e69f13a`);
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §2;
- `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §3 and §7;
- `DEFINITIONS_CHARTER_v2.md` @ `4b85851` §9;
- `DEPENDENCY_AUDIT_v2_CORRECTION.md` @ `4b85851` ("Supplied operations");
- `ac95.py` @ `a1b9759`.

**Exact missing clarification (v1.1, now supplied).** v1.1 asked for "a substrate-admissibility rule that is stated in advance and independent of this organism". Consult #25 supplies it, and the audit applies it.

**Relevance: YES, high (realized).** The flagship Track A sentence changed (F1).

**Stopping criterion.** **Met** for the audit: each disputed operation is classified and the claim is revised. Astra rulings Q-A1–Q-A3 were received in consult #28 and applied in v1.3. Remaining: the open I3r question (paper only). No further closure runs on the unchanged architecture, and no successor is built.

### U2 (rank 2). Adaptation of the system's own functional organization

**What is open.**
- The status file row "New maintenance dependencies acquired autonomously" is **NOT ESTABLISHED**.
- AC11 was falsified by its own controls (R2).
- AC6 adaptivity is unnecessary (R3).
- Content self-production is blocked (R10).
- The decision rule reduces to a fixed threshold and budget (R4).
- Bridge allocation reduces to a reactive rule (R11).
- So the "adapt" leg of the Track A question has no positive result. "Maintain" (F1–F4) and "reconstruct" (F5) do.

**Evidence:**
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (row "New maintenance dependencies acquired autonomously");
- `AC11_DESIGN_CONTROLS_v2.md` @ `c348a67`;
- `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.5 items 5 and 6. In the frozen economy, maintenance was priced at about 25× its payoff, so a cost/benefit trade-off was absent.

**Exact missing causal test.**
- A world whose economy is checked analytically, *before* any run, to contain a genuine maintenance trade-off. The best *fixed level* must be strictly worse than the oracle state-dependent policy, by a declared margin.
- An organism-internal adaptation of its maintenance allocation that beats the **entire swept fixed-level family** and a same-information reactive rule. These are Appendix B6 rivals.
- An intervention that reverses the adaptation when the acquired state is scrambled, with matched expenditure (AC106 P5 lesson).

**Simplest rival.** *A fixed-level duty cycle, or a same-information reactive threshold rule* (control theory). These already reproduce every adaptive candidate on record (R2, R3, R11).

**Relevance: YES, high.**
- A positive result would add the first established "adapt own organization" claim.
- A clean negative with the analytic trade-off certified would retire it.
- Today nothing is concluded.

**Stopping criterion.** If the analytic check shows that no fixed-vs-adaptive gap exists in any admissible world of the declared family, stop and record "not well posed **for that declared family**". Do not run organism finals.
- Astra #25 stopping-rule correction (verbatim): "Failure of one adaptive implementation does not retire adaptation of organization as a construct."

**Allocation (Astra #25, verbatim): RETAINED AS A QUESTION.** "Retain as a question, not a standing experimental queue. Require one explicit acquired organizational change and one discriminating prediction before proposing a run."

**Named claim or decision its outcomes would change (NC8).** The status row "New maintenance dependencies acquired autonomously" (NOT ESTABLISHED). No run is proposed until the two requirements above are written down.

### U3 (rank 3). O3 constitutive loop: does a content intervention alter the enabling machinery and then future content?

**What is open.** Ledger O3 = PARTIAL: "maintenance affects content and content affects adaptation; full constitutive loop unestablished".
- AC108 shows content → adaptation/production (force_machinery) and maintenance → content.
- It does not show a closed loop in which content changes the machinery that later regenerates content.

**Evidence:**
- `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c` (layer O3);
- `AC108_RESULTS_v1.md` @ `5c0b2f1`;
- `ACI_PRIOR_ART_AND_REDUCTION_v1.md` @ `a72136c` ("Cross-route discriminator": "what is restored, and whether it restores the conditions enabling restoration").

**Exact missing causal test** (ledger `next_falsifier`, made operational; v1.2 adds Astra #25's design requirements after the list).
1. Apply a matched-current-observation content intervention at t0.
2. Measure (a) a change in the *production or repair* of the enabling machinery during t0..t1 (for example W-gated repair writes or the description repair schedule).
3. Measure (b) a change in *content regenerated* after t1 that is mediated by (a). Mediation is shown by a second arm that clamps the machinery change while leaving the content intervention intact, so (b) must vanish.
4. Rivals:
   - a world-state-only controller;
   - the inactive-queue reduction "production-versus-state-regrowth dependency audit" (`ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`, inactive_theory_queue).

**Astra #25 design requirements (verbatim).**
- "First establish that the machinery intervention isolates the proposed pathway without simply disabling computation or changing available resources."
- "For U3, use pathway interruption plus machinery-specific restoration, with resource and immediate-function controls. A single blocking arm is not a complete mediation argument."

**Simplest rival.** *Ordinary state estimation with intact, supplied machinery* (counting / filtering): a world-state-only controller whose content changes behaviour but never the machinery that regenerates content.

**Relevance (v1.2, corrected per the U1 audit §7).**
- **For the closure sentence (F1): NO under the current code.** Every machinery-repair and regeneration path runs through supplied coordination (audit I7, I10). A positive U3 would change the amount or timing of repair delivered *through* fixed policies without moving any sequence or policy into declared state. A negative U3 removes nothing F1 relies on.
- **For a separate O3 / Q-CAUSE claim: YES.** It would decide ledger O3 (PARTIAL), the content→machinery→content loop.
- **Exception:** if the coordination were first moved into declared state (U1 successor sketch, not proposed), a U3-style loop through that declared table *would* bear on the closure sentence.
- **Astra #28 (verbatim, v1.3):** "Keep U3 on hold unless its separate content-to-machinery causal claim is independently worth pursuing. U3 cannot internalize a schedule by demonstrating stronger dependence on it."

**Stopping criterion (corrected).** If (b) persists under the machinery clamp, the proposed mediation account is defeated. Record "mediation not supported" and stop.
- Astra #25 correction (verbatim): "Persistence of an effect under the U3 machinery clamp defeats the proposed mediation account; it does not prove reduction to ordinary estimation."
- Do not create a reduction entry from that outcome alone.

**Allocation: HELD, NOT PROPOSED.**
- Astra #25 calls it the "Highest-value possible Track A experiment after U1", and its next-step 2 says "Propose that experiment only if the answer is yes" (would U3 change the synthesis conclusion).
- For the closure conclusion the answer is no. For the separate Q-CAUSE claim it is yes.
- Whether to propose a protocol for that separate claim is Aidan's decision, and any protocol needs its own approval.

**Named claim or decision its outcomes would change (NC8).** Ledger layer O3 (PARTIAL), a Q-CAUSE claim. Not F1.

### U4 (rank 4). Q-NECESSITY of recurrent-matrix learning (PR #10)

**What is open.**
- R-FIX-32 and R-FIX-48 both return **TARGET NOT REACHED WITHIN DECLARED SEARCH**, with 0/10 final verified passes, 0 init witnesses, 0 invalid and 0 boundary.
- CAND, the unrestricted comparator, reaches target 10/10.
- Q-NECESSITY = **NOT_ESTABLISHED**. "Failure means only 'not reached within declared search.' This is not a necessity certificate."

**Evidence:**
- `frozen_recurrent_compensation_results_v1/stage2/RESULTS.md` @ `0329818`;
- `frozen_recurrent_compensation_results_v1/results_v1_errata/RESULTS_v2.md` @ `0329818` (the ledger, per `results_v1_errata/ERRATA_v1.md` @ `0329818`);
- `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818`;
- PR #10.

**Exact missing test.**
- *Either* a pre-registered extended R-FIX search (protocol Appendix D) with a fixed grid of LR, steps and restarts, a held-out selection subset, a CAND comparator under the same search, and training-loss curve logging;
- *or* a finite-class bound: inf T > 1 over a declared parameter domain. The review judged a bound infeasible at 651–843 continuous parameters except for a narrow quantized subclass.

**Simplest rival.** *Reservoir computing*: train the input weights, biases and readout on a fixed random recurrent matrix. This is exactly the R-FIX arm, so it is a rival not yet excluded or confirmed beyond the declared search.

**Relevance: asymmetric.**
- **One verified R-FIX witness would change a conclusion.** It would refute, within GRU-8 at that W0 and head width, that weight_hh learning is needed for the target.
- Another failure would **not** change the conclusion: it stays NOT_ESTABLISHED.
- Necessity can only come from a bound.

**Stopping criterion.** Stop after one pre-registered extended search with no witness, unless a bound becomes feasible. Do not iterate searches (forking paths). Any training needs Aidan's approval.

**Allocation (Astra #25, verbatim): DEFERRED.** "Defer. Another failed R-FIX search is unlikely to affect program strategy. Reopen only for a decision that a compensation witness would change."

**Named claim or decision its outcomes would change (NC8).** Only a verified R-FIX witness would change a claim (Q-NECESSITY stays NOT_ESTABLISHED otherwise). Reopen only if a named program decision depends on it.

### U5 (rank 5). Minimal organization

**What is open.**
- K3 §5 and A3 §5 classify components as necessary or optional by ablation (AC10/91/92).
- No document shows that the set is *minimal*, meaning that no proper subset meets C1–C5 and S1–S4 and forms a closed strongly connected component.
- Pointer, coordination and decision state are established as maintained state (S1–S4), but not each individually as ablation-necessary at the AC105 body.
- Coordination maintenance is a "state-cleanliness contrast" only (AC87 G6).

**Evidence:**
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §1;
- `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §5;
- `AC87_RESULTS_v1.md` @ `dc3e428`.

**Exact missing test** (mostly analytic, then a small causal table):
1. An exhaustive check over the declared production graph that no proper subset is a closed strongly connected component with no external root. This is graph work, no simulation.
2. A leave-one-out ablation per maintained-state item at the AC105 body, with a declared functional endpoint (reconstruction completion or income) rather than survival alone.

**Simplest rival.** *A smaller autocatalytic sub-network* (ALife: a minimal autocatalytic set). For example, the W/C/B production loop with the description treated as passive storage.

**Relevance: MEDIUM.** It delivers Track A's "minimal organization" item and could demote an item from necessary to optional. The closure verdict is unaffected unless a necessary component turns out to be removable.

**Stopping criterion.** Stop if step 1 shows the strongly connected component is already minimal and every S-item has an existing ablation. Then record "minimal within the declared component list".

**Allocation (Astra #25, verbatim): DEFERRED.** "Defer unless "minimal" remains in a publication claim. Remove that adjective otherwise. Graph connectivity and leave-one-out ablations do not establish minimality over compensating alternatives."

**Named claim or decision its outcomes would change (NC8).** Any publication sentence using "minimal". This triage makes no minimality claim, and none should be made from connectivity or leave-one-out ablations.

### U6. Clause (ii): whole-organism unity (non-spatial informational core)

**What is open.**
- Clause (ii) is NOT ESTABLISHED: met only at the material layer.
- The "sole remaining genuine limitation" is the non-spatial informational core.
- The finite successor requirements R1–R4 and tests T1–T5 are specified. The S1 spec and its protocol are "AWAITING separate execution authorization".

**Evidence:**
- `A0_AUTONOMY_VERDICT_v1.md` @ `eb79ecb` §4–§6;
- `S1_SPATIAL_SUCCESSOR_SPEC_v1.md` @ `eb79ecb`;
- `I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` @ `eb79ecb` (c);
- ledger O4 = NOT_ESTABLISHED.

**Exact missing test.** A0 T1–T5:
- T1: localized-read ablation and endogenous restoration;
- T2: retention vulnerability, with a transport-exempt contrast arm;
- T3: mid-function production block plus machinery-only rescue;
- T4: two directed cuts with separable effects;
- T5: observer-discard with exactly one copy.

The falsification clauses are A0 §6 (i)–(iii).

**Dependency flag.** It needs a new component class. The status file calls it "a re-architecture of the supplied physics", so it requires approval under the "no new architecture family" rule.

**Simplest rival.** *External coordination through a declared non-spatial host array*: the informational core is ordinary host memory that space and boundary never touch.

**Relevance.** YES for the full two-clause autopoiesis verdict, which would move from NOT ESTABLISHED for the informational core. NO for any neural or Track B architecture: the mission audit says "NO — defer to the ALife paper".

**Stopping criterion.** Do not start without explicit authorization. If started, stop at the first prespecified falsification clause.

**Allocation (Astra #25, verbatim): DEFERRED.** "Separate ALife successor project requiring an explicit PI decision. Not a prerequisite for Track B."

**Named claim or decision its outcomes would change (NC8).** The clause (ii) whole-organism unity verdict (NOT ESTABLISHED). It requires a PI decision.

### U7. Economic viability of the internalized decision state

**What is open.**
- AC96: the internalized streak is paid, and in the move world it is starved by the income collapse it exists to pre-empt. The maintained arm relinquishes 2/8 against the host's 8/8, and 6/8 die. The status file calls it "the new open item".
- AC104/AC105 show the allowance economics are seed-dependent: allowance 33 vs 42, the 5804 rescue and the 5603 harm.

**Evidence:**
- `AC96_RESULTS_v1.md` @ `d7925cf`;
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`;
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §5.

**Exact missing test.** An analytic affordability bound: the expected cost of maintaining the decision state against the income it protects, across the declared challenge grid. Then one frozen run only if the bound is not decisive.

**Simplest rival.** *A host-side counter* (external coordination). It is economically better on record: the host relinquishes 8/8 against the maintained arm's 2/8 (`AC96_RESULTS_v1.md` @ `d7925cf`).

**Relevance: LOW for closure** (K3 §5: "Robustness limits are NOT redesign requirements"). Medium for the level-(b) robustness claim.

**Stopping criterion.** Stop at the analytic bound if it is decisive.

**Allocation (Astra #25, verbatim): DEFERRED.** "Keep as a documented operating-range limitation. Do an affordability analysis only if the intended claim requires the missing range."

**Named claim or decision its outcomes would change (NC8).** Only a level-(b) robustness claim that needs the missing range. Otherwise it stays a documented operating-range limitation.

### U8. Survival-level composition (AC115 G4–G7; AC68 bimodality; AC39 transfer) — DROPPED FROM THE ACTIVE QUEUE

**Allocation (Astra #25, verbatim).** "Drop from the active queue."

**Dropped with reason.**
- The survival-bundled gate failures (`AC115_ERRATA_v1.md` @ `e2e2ac6`) stay recorded as failed. S4 keeps its mechanism-level result.
- Resolving them would not change F1 or S4; the mission audit calls it "a known wall". The simplest rival is seed-dependent W/C bistability.
- Reopen only if a closure claim comes to depend on survival (NC8).

### U9. Robustness of PR #9's Q-CAUSE label to additional control draws

**What is open.**
- The PR #9 FO+ISO (GRU-8) REPLICATED label is at exactly 8/10, under the per-seed joint rule D_FO and D_ISO (with M). Each failing seed lost to one isotropic draw.
- Protocol-mandated sentence: "robustness to additional draws is untested".

**Evidence:**
- `first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`;
- `first_order_control_protocol_FINAL.md` @ `4f6fc4c` §6.1.

**Exact missing test.** A new pre-registered confirmatory study on fresh seeds with more draws per family (for example 128), the same joint rule, and the B5 default bar (8/10, with UNRESOLVED above two invalid seeds) frozen in its own protocol. Not a reanalysis.

**Simplest rival.** *Order-statistic variability* of the maximum over a finite set of random control draws (sampling). The label could move with more draws, without any change in mechanism.

**Relevance: MEDIUM.** It could weaken the bounded Q-CAUSE entry. It cannot touch Q-NECESSITY or closure.

**Stopping criterion.** Run only if a downstream claim relies on Q-CAUSE strength. Otherwise keep the qualifier.

**Allocation (Astra #25, verbatim): DEFERRED.** "Keep the sampled-control qualifier. No new draw-count study without a downstream decision requiring it."

**Named claim or decision its outcomes would change (NC8).** The strength of the PR #9 Q-CAUSE entry (S15) only, if a downstream decision requires it. The sampled-control qualifier is kept.

### U10. W-REL exact check — EXECUTED AND REVIEWED; verification gap closed; A2 reference conjunction attained; named controls not evaluated

**Allocation (Astra #25, verbatim).** "Finish the already approved bounded analysis and review it separately."
- Done: executed in PR #11 (https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/11) and reviewed separately in `/workspace/review/wrel_results_review_v1.md` (sha256 `60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace`).
- Astra #26 then ruled on the review's items: `/workspace/astra_consult26_response.txt` (sha256 `e7b64e40fe430455be97435a349cc0f8428f9da86ba68af8577e767ab999ab12`).

**Status.**
- **Approved** by Aidan at 8:58 AM ET, 2026-10-21 (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`).
- **v1.4 status (Astra #29; verified against the PR #11 record before writing).** Astra #29 says (verbatim): "The W-REL entries are stale. Mandatory verification has been completed, and A2 attainability has been demonstrated. Replace both the UNRESOLVED-COMPUTE sentence and the proposed future attainability check."
- PR #11 branch fetched read-only (`refs/pull/11/head` → `dddd63c`, 2026-10-21 12:32 PM ET). Records:
  - Addendum A1 verification result: `c4_reliability_exact_check_v1/RESULTS_v3.md` @ `0e17a05`, lines 9–17 and 25–36. The missing ITEM-8 replay AGREES with 0 mismatches, status COMPLETE. ITEM-9 now agrees on every replayed quantity, and the earlier incomplete-coverage status is lifted. The four original formal labels are unchanged.
  - Policy-coverage close-out: `c4_reliability_exact_check_v1/WREL_CLOSEOUT_E27_v1.md` @ `7b89c66`, lines 9–13. Condition (a) holds: the independently rebuilt reference policy was the object used in the required intervention and rescue replay. Condition (b), a stored action-table comparison, is not established.
  - Addendum A2 result: `c4_reliability_exact_check_v1/RESULTS_A2.md` @ `dddd63c`, lines 9, 30–44, 73–79, 92–106 and 135–141, with `c4_reliability_exact_check_v1/outputs/attainability_A2/SUMMARY.json` @ `dddd63c`. At T_SEP = 3 and 4:
    - reference conjunction ATTAINED; C-REF, C-T2, C-SEL, C-FO and rescue all PASS; status COMPLETE;
    - primary and replay agree, with 0 action disagreements (432 and 1552 rows);
    - the formal label is UNRESOLVED-DESIGN, from `decide_setting` called with an empty control list.
  - A2 approval: `c4_reliability_exact_check_v1/c4_reliability_APPROVAL_ADDENDUM_A2.md` @ `fb3e9b4`. Frozen spec, code and manifest: `c4_reliability_exact_check_v1/c4_reliability_exact_check_spec_ADDENDUM_A2.md` @ `8a4b393`.
- **Ledger wording (Astra #29, verbatim):**
  > "W-REL PR #11: the mandatory verification gap was closed by the approved verification addendum, with the independently reconstructed policy used in the required reference intervention and rescue replay. The original four setting labels remain unchanged. Exploratory Addendum A2 subsequently attained the frozen reference core conjunction under H0 at (c_R,c_S)=(1/100,3/50), T_SEP=3 and 4. Primary and independent replay statistics agree, and the compared action-table domains and actions agree. Named controls and PM-ACT were outside A2 and were not evaluated. The frozen decision function returned UNRESOLVED-DESIGN for the empty-control invocation; this is not a completed named-control comparison. C-T2 is an exact-Bayes calibration result, and causal findings are restricted to the declared donor interventions and first-order probe battery. Q-LEARN and Q-NECESSITY remain untested. No change is made to the C4 evidence or status row, and no consciousness conclusion is drawn."
- **A2 scope (Astra #29 edit E29-1, verbatim):**
  > "Addendum A2 demonstrates attainment of the frozen reference core conjunction at the two declared settings. It does not evaluate named-control reproduction or separation. The UNRESOLVED-DESIGN return from the empty-control invocation is preserved as software output and reported alongside NAMED-CONTROL COMPARISON: NOT RUN."
- **On conditions (a) and (b) (Astra #29, verbatim):** "Condition (a), independently rebuilding the policy and using it in the required replay, was an alternative to condition (b). Both were not required."
- **Track A status (Astra #29 edit E29-6, verbatim):**
  > "The original W-REL verification gap has been closed. Exploratory A2 attained the reference conjunction at (1/100,3/50), T_SEP=3 and 4. Named controls at these settings remain unevaluated. This update changes neither Track A's closure verdict nor any C4 evidence or status row."

**Formal per-setting labels, original four settings** (unchanged; `c4_reliability_exact_check_v1/RESULTS_v3.md` @ `0e17a05`, lines 29–36):

| T_SEP | (c_R, c_S) | Formal label |
| ---: | --- | --- |
| 3 | (1/50, 3/50) | UNRESOLVED-DESIGN; no donor contrast; C-REF and C-T2 also fail |
| 4 | (1/50, 3/50) | UNRESOLVED-DESIGN; same reasons |
| 3 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET; C-REF and C-SEL fail |
| 4 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET; C-REF fails |

**Addendum A2 settings** (`c4_reliability_exact_check_v1/RESULTS_A2.md` @ `dddd63c`): at (1/100, 3/50), T_SEP = 3 and 4, the reference conjunction was ATTAINED. The formal label is UNRESOLVED-DESIGN from the empty-control invocation, reported with NAMED-CONTROL COMPARISON: NOT RUN (E29-1).

**Review items A1–A4, as ruled by Astra #26.**
- **A1:** "Retain the frozen precedence." UNRESOLVED-DESIGN precedes REFERENCE CRITERIA NOT MET, with the C-REF and C-T2 failures reported. Astra corrects the review's reasoning: the precedence "follows the chosen protocol precedence, not a general rule of logic".
- **A2:** "The coverage qualifier alone is insufficient." That ground was removed when Addendum A1 closed the verification gap (above).
- **A3:** "Identity swaps do not supply the missing intervention comparison." MB-myopic reproduction at the two no-contrast settings is **UNRESOLVED**, not YES. The YES comparisons at the two contrast settings "remain provisional comparison results, subject to the validation shortfall".
- **A4:** "Not immediately." The read-only extraction from existing outputs (`/workspace/review/wrel_attainability_from_existing_outputs_v1.md`) left (T_SEP, c_R, c_S) = (3, 1/100, 3/50) and (4, 1/100, 3/50) open. The separately approved Addendum A2 (`fb3e9b4`) then evaluated exactly those two and attained the reference conjunction at both (above). The extraction's status lines are historical.
- **A5** (v2 only): "The checking ceiling remains FAIL."

**Corrected relevance (NC1, NC7; replaces v1.1's wording).**
- v1.1 said a PATTERN REPRODUCED BY NAMED CONTROL outcome "would add" a reduction entry. That contradicted the W-REL interpretation rules. Astra #25: "PATTERN REPRODUCED BY NAMED CONTROL does not automatically create a REDUNDANT entry."
- Under NC7, such an outcome could only retire, by name, the novelty claim "R-HAC-MB's assessment role is distinguished from the named analytic controls", without negating any retained component result.
- No setting received that label. In the four original settings the reference did not meet its core criteria. In the two A2 settings it attained them, but no named control was evaluated. So no separation is supported or refuted, and no reduction entry follows. Astra #26: "These comparisons do not establish absence of an assessment role".

**Retained evidence (bounded facts about supplied analytic agents).** These come from Astra #26 and the review:
- ITEM-1 symmetry audit VERIFIED;
- the value calculations;
- at (4, 1/100, 1/10), the component intervention, C-FO and rescue results.

They do not establish acquired assessment or the complete admission conjunction.

**Q-tags.** Q-EXIST (world/identifiability): ITEM-1. Q-CAUSE: A2 component findings only, restricted per Astra #29 to "the declared donor interventions and first-order probe battery"; no separation is established. Q-LEARN: not tested. Q-NECESSITY: not tested. No change to the C4 evidence or status row. No C4 or consciousness conclusion.

**Simplest rival.** *The battery's own named count-based and policy-only analytic agents* (counting / filtering): R-CONF-A, R-BLIND/R-CONF-S, R-CG counts, R-HAC-MF, the policy-minimized PM-ACT, and MB-myopic.

**Relevance.** Mainly Track B (C4 admission). LOW for Track A.

**Named claim or decision its outcomes would change (NC8).**
- The W-REL ledger row, now Astra #29's wording (above).
- The next W-REL decision: Astra #29 recommends one bounded named-control comparison at the two A2 settings. Its approval question (#29 §D) is for Aidan and is neither approved nor proposed here.

**Stopping criterion.**
- (a) Met: the mandatory verification was completed under Addendum A1 (`0e17a05`).
- (b) Met: Addendum A2 evaluated only the two open settings (`dddd63c`).
- (c) Do not add costs or horizons after seeing failures. Astra #29 (verbatim): "Do not extend horizons, add controls or change thresholds after seeing results."

### U11. AC116 storage question (suspended at the resolution floor) — DROPPED FROM THE ACTIVE QUEUE

**Allocation (Astra #25, verbatim).** "Drop from the active queue; preserve the suspended result."

**Dropped with reason.**
- The suspended result is preserved as recorded: exact sign-flip p = 0.0625 at n = 8, the floor of the test; "Suspended — not closed, not demonstrated" (`AC116_ERRATA_v1.md` @ `e2e2ac6`; `AC116_RESULTS_v1.md` @ `3ebccdf`).
- S0 records it as "not a license for further storage-comparison runs". The mission audit says it "would not move the architecture".
- No named claim or decision depends on it (NC8).

---

## 6. Verification of this document

**v1.4.** `/workspace/scratch/astra29/check_e29.py` (log `check_e29.log`) checks this file together with the audit v1.2 and the synthesis v1.2. It checks that:
- Astra #29 quotations are verbatim;
- `` `path` @ `commit` `` pairs exist, including the PR #11 commits, and the PR #11 record supports the W-REL statements;
- no "resolved by" appears outside quotes;
- no earlier formal-status or attainability-check text appears outside the changelogs and quotes;
- the closure sentence is byte-identical across the three files;
- each "8/10" contribution names PR #9 FO+ISO and its joint rule;
- forbidden phrases are absent;
- earlier versions are unchanged.

**v1.3.** `/workspace/scratch/u1_audit/v1_1/check_v1_1.py` (log `check_v1_1.log`) checks this file together with the audit v1.1 and the synthesis v1.1. It checks that:
- every Astra #28 quotation is byte-exact;
- the closure sentence is byte-identical across the three files, and the v1.2 sentence is absent;
- every `` `path` @ `commit` `` pair exists;
- forbidden phrases are absent;
- prior versions are unchanged.

**v1.2.** `/workspace/scratch/track_a_triage/v1_2/check_v1_2.py` (log `check_v1_2.log`) checks this file:
- every `path @ commit` pair exists (`git cat-file -e`, read-only);
- every Astra #25/#26 quotation is a byte-exact substring of the consult file;
- the F1 sentence is byte-identical to the U1 audit's;
- the §1 counts and allocation counts equal the entries;
- the old category name appears only in verbatim quotes and the changelogs;
- forbidden phrases are absent;
- v1 and v1.1 hashes are unchanged.

The dropped U8 and U11 notes intentionally omit the "Exact missing" fields.

**v1.1.** `/workspace/scratch/track_a_triage/v1_1/check_v1_1.py` (log `check_v1_1.log`) runs all v1 checks on this file and the additional v1.1 checks listed in the changelog. The v1 description below is retained.

`/workspace/scratch/track_a_triage/check_citations.py` (with `.log`) extracts every `` `path` @ `commit` `` pair in this file and runs `git cat-file -e commit:path` in `/workspace/repo`. This is read-only, and the result is in the log.

It also checks that:
- the §1 counts equal the entry counts;
- each UNRESOLVED entry has the fields "Exact missing", "Relevance" and "Stopping criterion".

**Figures not re-derived (UNVERIFIED).**
- Numbers quoted from repo documents (gate counts, seeds, p-values) were read from those documents, not re-derived from rows. They are UNVERIFIED at row level except PR #8, #9 and #10, which the earlier independent reviews recomputed.
- The mission audit's "≈25×" economy figure is quoted from `ACI_MISSION_AUDIT_v1.md`. Its primary computation (AC11/AC15 economy check) was not re-traced here.

---

## Appendix. Portable Track B falsification test pack

Each test is stated as a frozen rule with its source. They are portable as *procedures*. Thresholds, seed bars and invalid-seed rules are **defaults that each study must re-freeze in its own protocol** before any outcome exists (B5). Nothing here authorizes a run.

### B1. Graded-reversion AUC directional rule (PR #8)

**Source:** `GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb` §4, §6 and §7.

**Intervention.** Interpolate the learned component toward its initialization, W(α) = W_T + α·(W_0 − W_T), during the declared steps. Hold the other trained parameters and a fresh readout fixed.

**Controls.**
- 32 random directions per seed, matched per block in Frobenius norm to the displacement, reused across every dose and target.
- Generator `torch.Generator` with seed 40000 + 100·s.
- Zero-displacement blocks get a zero perturbation.

**Curve.** Delta_c(α) = L(c, α) − L(intact). The doses and weights are:

```text
alpha:   0     1/8    1/4    1/2    3/4    1
weight:  1/16  1/8    3/16   1/4    1/4    1/8
```

AUC_c = Σ w_α·Delta_c(α). Negative excesses are retained and nothing is clipped. "It is not a certified integral of the network's continuous dose response."

**Per-seed rules.**
- **(D) Directional:** "D passes iff AUC_REV − max_j AUC_rand,j > eps0."
- **(M) Materiality:** AUC_REV > eps0 **and** AUC_REV ≥ B_prefix/4.

**Eligibility.** A failure is a non-pass, not invalid. The seed must be valid, pass transfer, have B_prefix > eps0, have C_prefix > eps0, and have displacement > eps0.

**Seed bar.** The B5 defaults (8/10, and UNRESOLVED above two invalid seeds) were the frozen PR #8 instance. A new study must freeze its own.

**Integrity.** These have no evidential role, and any failure makes the seed invalid:
- SHAM equals intact within eps0;
- RESTORE reproduces intact within IDENTITY_TOL;
- checkpoint sha256 values match;
- outputs are finite and in (0, 1).

**The comparison is empirical and directional, not a calibrated p-value.** Reversion toward initialization is not exchangeable with isotropic directions.

### B2. Conjunctive FO + ISO matched controls (PR #9)

**Source:** `first_order_control_protocol_FINAL.md` @ `4f6fc4c` §4, §6, §6.1 and §7.

**Families.** FO paths are matched to REV's first-order (gradient-projection) effect per block. ISO paths are B1's isotropic norm-matched directions. Both have 32 paths.

**Rule** (verbatim):

```text
D_FO  = (AUC_REV - max_j AUC_FO,j > eps0)
D_ISO = (AUC_REV - max_j AUC_ISO,j > eps0)
D     = D_FO and D_ISO

Joint pass = valid and eligible and D_FO and D_ISO and M
```

**Count rule.** "Separate eight-seed successes against each family are insufficient."

**Thin-margin rule** (reporting only). A joint-passing seed is *thin for family F* if max_j AUC_F,j > eps0 and margin_F < 0.10·max_j AUC_F,j. If the label is REPLICATED but fewer than eight joint passes are non-thin for both families, print verbatim:

> "The REPLICATED label depends on at least one seed whose directional margin against at least one family is below 10% of that family's most damaging sampled path; robustness to additional draws is untested."

**Diagnostic.** AUC − FO_AUC is a "residual after subtracting the initial tangent contribution", **not a curvature estimate**.

### B3. R-FIX freeze and compensation test (PR #10): verbatim rules

Track B considers this the most important test, so every rule below is quoted verbatim, not paraphrased.

**Source.** `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818`, PR #10 (https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/10). Protocol sha256 `eca2121c5972138580ebd8ababb1cd40879a4c20404e925e129becd7e778ea40`. It is byte-identical to `/workspace/review/frozen_recurrent_compensation_protocol_FINAL.md`.

**How the excerpts were made.** Each fenced excerpt is sliced byte-exactly from that file by `build_v1_1.py`, and `check_v1_1.py` re-verifies each one as an exact substring. Section numbers inside the excerpts are the protocol's own.

**Excerpt 1. §1 arms table and parameter-matching statement**

````text
| arm | head H | frozen | trainable | # trainable | # stored total |
| --- | --- | --- | --- | --- | --- |
| **CAND** | 32 | nothing | everything | **843** (456 + 387) | 843 |
| **R-FIX-32** | 32 | `weight_hh_l0` = W0 (192) | W_ih, b_ih, b_hh, readout | **651** (216 + 48 + 387) | 843 |
| **R-FIX-48** | 48 | `weight_hh_l0` = W0 (192) | W_ih, b_ih, b_hh, readout | **843** (216 + 48 + 579) | 1035 |
| (R-FIX-70, not run) | 70 | `weight_hh_l0` | as above | 1107 (264 + 843) | 1299 |

> "R-FIX-32 tests compensation with the original architecture. R-FIX-48 additionally tests compensation with an equal total trainable-parameter count allocated differently. These comparisons do not isolate parameter count from readout width, parameter allocation or optimization effects."
````

**Excerpt 2. §3 target definition**

````text
T(θ) = max( L_prefix(θ) / (τ·PD(q*)), E_total_TEST(θ) / thr_total_TEST, E_XOR_TEST(θ) / thr_XOR_TEST ).

τ = 0.25. The target is L_prefix ≤ 0.25·PD(q*) AND both TEST A-FIT inequalities (consult #18 §7). Numerical decisions follow the dual-evaluator rule of §3.1.
````

**Excerpt 3. §3.1 numerical decision rule (dual evaluator), complete**

````text
### 3.1 Numerical decision rule (consult #19, Edit 2; applies identically to CAND, R-FIX-32 and R-FIX-48, at init and final)

The two evaluators are:
- (E1) the frozen evaluator: `evaluate_arm`, `l_prefix` and `component_excess`;
- (E2) an independent float64 NumPy forward pass and metric implementation.

Each evaluator computes the three normalized components and T independently. Verbatim:

```text
t = 1e-9

VERIFIED TARGET PASS:
    both evaluators give T < 1 - t

VERIFIED TARGET FAIL:
    both evaluators give T > 1 + t

BOUNDARY / NUMERICALLY UNRESOLVED:
    neither condition holds

Evaluator disagreement beyond the agreement tolerance:
    integrity failure
```

Agreement, for each normalized component `x, y`, verbatim:

```text
abs(x-y) <= 1e-12 + 1e-9*max(abs(x), abs(y))
```

Consult #19 verbatim: "Both evaluators must independently pass the target rule; agreement alone is insufficient. Call these **numerically verified witnesses under the declared float64 evaluation**, not formal real-arithmetic certificates."

Float32 (native) evaluation may be reported descriptively. It does not gate any claim (§14 ruling 5). Consult #19 verbatim: "Dual evaluation is a numerical cross-check, not a validated error bound for real arithmetic."
````

**Excerpt 4. §4 harness additions and freezing checks, complete**

````text
## 4. Harness additions (written and frozen with the protocol; engineering only)

1. **`train_arm_rfix(model, episode_seed)`.** PR #7 `train_arm` with exactly one difference: `rnn.weight_hh_l0.requires_grad_(False)`, and every other tensor `True`.
   - The Adam parameter list and `clip_grad_norm_` cover exactly that arm's trainable tensors.
   - §14 ruling 3, verbatim: "clip each arm's actual trainable parameter set. Do not compute artificial gradients through frozen parameters to imitate CAND's clipping."
   - Everything else is identical to `train_arm`: the generator, `sample_batch`, the loss, the LR schedule and the failure checks.
2. **Freezing checks (consult #19, Edit 4, verbatim):**

   > "For every R-FIX run, assert before optimization that weight_hh is the only frozen parameter tensor, is absent from the optimizer parameter list, and has requires_grad=False. Check after backward that its gradient remains None. Check W0 byte equality after training and after checkpoint reload."

   - The "after backward" gradient check runs at every step, or at minimum the first and last step. This is an implementation choice to be fixed at freeze; see ambiguity A4.
   - Byte equality uses sha256 of the tensor bytes, compared with the Stage-0 W0 hash.
   - Any failure makes the run invalid.
3. **Synthetic-fixture test of the freezing implementation (Edit 4).** Verbatim: "A `.grad is None` check before backward is vacuous. Test the freezing implementation on a synthetic fixture; do not consume an additional fresh-seed training run."
   - The fixture is a model built from a non-study seed, on synthetic inputs, run for a handful of optimizer steps.
   - It exercises `train_arm_rfix`'s checks, including a deliberately mis-frozen negative case that must be caught.
   - It is not a study run, has no evidential role, and uses none of seeds 400–409 or streams 1400–1409.
   - It is run as part of implementation freezing, not by this drafting task.
4. **No evaluation of trained models in Stage 1.** Stage 1 logs training loss only. Init checkpoints are evaluated only in Stage 2, together with the finals, so that no outcome information exists before the Stage-1 seal.
````

**Excerpt 5. §6 validity and eligibility, complete**

````text
## 6. Validity (per arm and seed)

A run is **invalid** on any of the following:
- a training integrity failure (non-finite loss, gradients or weights, as in PR #7);
- a checkpoint round-trip mismatch;
- `outputs_valid` false;
- identity checks failing at IDENTITY_TOL;
- any §4 freezing check failing (R-FIX);
- a Stage-0 pairing assertion failing;
- an episode digest mismatch;
- a Stage-2 checkpoint sha not matching the sealed manifest;
- **evaluator disagreement beyond the §3.1 agreement tolerance.**

Invalid checkpoints supply no witness.

**Eligibility: consult #19, Edit 1, verbatim replacement of the initialization eligibility rule:**

> "T(init) is descriptive and does not determine eligibility for an existence witness. A valid initialization or final checkpoint that passes the numerical verification rule supplies a witness for its specified frozen W0 and head width. Report initialization witnesses separately. Acquisition of target attainment requires a verified above-target initialization followed by a verified below-target final checkpoint."

"Retain all ten seeds and all 30 scheduled runs regardless of initialization results. Do not replace seeds."

"For the acquisition annotation, use both evaluators to establish `T(init) > 1 + T_BOUNDARY_TOL`. An initialization near the boundary cannot establish the initially-failing condition."

The acquisition annotation for a run therefore requires both of the following under §3.1:
- init classified VERIFIED TARGET FAIL;
- final classified VERIFIED TARGET PASS.
````

**Excerpt 6. §7 labels, complete**

````text
## 7. Labels (per arm; decided only in Stage 2)

**Witnesses.** A **numerically verified witness under the declared float64 evaluation** is a valid checkpoint, initialization or final, classified VERIFIED TARGET PASS under §3.1.

- R-FIX final witnesses need W0 byte-equal after training and after reload.
- An init checkpoint has `weight_hh` = W0 by construction, so a verified-pass initialization is an existence witness for its W0 and head width.
- Because the CAND and R-FIX-32 inits of a seed are identical, one such init witness is a single witness. It is reported once, under H = 32, with CAND noted. See ambiguity A1.

**Label rules (consult #19, Edit 3, verbatim):**

> "Per arm, report final verified target passes out of ten, initialization witnesses, invalid runs and boundary runs separately. One verified checkpoint supplies an existence witness. At least eight final verified passes earns TARGET REACHED REPRODUCIBLY. If more than two runs are invalid or numerically unresolved, the reproducibility label is UNRESOLVED; otherwise fewer than eight passes gives REPRODUCIBILITY CRITERION NOT MET."

When zero witnesses are found (verbatim):
- "If all ten final evaluations resolve above target, use `TARGET NOT REACHED WITHIN DECLARED SEARCH`."
- "Otherwise use `NO VERIFIED WITNESS FOUND`, with unresolved and invalid counts."

"CAND follows the same numerical and evaluability rules. CAND failure still does not invalidate an R-FIX witness."

**Per-arm report block (mandatory, all three arms):**
- final verified passes: n/10;
- initialization witnesses: count;
- acquisition annotations: count;
- invalid runs: count, with reasons;
- boundary or numerically unresolved runs: count;
- existence label: WITNESS FOUND, `TARGET NOT REACHED WITHIN DECLARED SEARCH`, or `NO VERIFIED WITNESS FOUND`;
- reproducibility label: TARGET REACHED REPRODUCIBLY, REPRODUCIBILITY CRITERION NOT MET, or UNRESOLVED.

**CAND** is the unrestricted comparator. Its labels are reported with the same rules. If CAND does not reach TARGET REACHED REPRODUCIBLY, the R-FIX-vs-CAND comparison is reported as UNRESOLVED (comparator not reproduced). R-FIX witnesses still stand (§13 ruling 10).

There is no pooled R-FIX label and no comparison test between arms. R-FIX-32 vs R-FIX-48 differences are descriptive.

There is no multiplicity correction for existence statements: they are verified-instance claims, not statistical inferences. The search size must be disclosed: 20 final R-FIX checkpoints plus their 20 inits.
````

**Excerpt 7. §8.1 'Not reached' wording and §8.3 claim ceiling**

````text
**Not reached:** "R-FIX-H: TARGET NOT REACHED WITHIN DECLARED SEARCH (one run per seed, 4000 steps, PR #7 recipe, no restarts). Failure means only 'not reached within declared search.' This is not a necessity certificate and does not establish that departing from W0 is necessary."

### 8.3 Claim ceiling (consult #18, verbatim)

> "A certificate must establish `inf T(theta) > 1` throughout the restricted domain, alongside an unrestricted witness with `T <= 1`. The domain must specify the frozen matrix, remaining weight ranges or precision, readout size and supplied timing information."

> "That would establish necessity of **departing from that specified frozen matrix within that domain**. It would not establish universal necessity of recurrent training. A simple prefix-separation argument should not be presumed available: trainable input weights, gates and readout may retain substantial representational flexibility."

The ceiling of this study is one of the following, never a certificate:
- numerically verified existence (or reproducibility) of a witness for the reported W0 and H, under the declared float64 evaluation;
- "not reached within declared search";
- "no verified witness found".
````

**Portability notes (this triage's, not protocol text).**
- τ, the target components, the head widths, the budget and the seed and stream ranges are study-specific. A Track B study must freeze its own.
- The thresholds t = 1e-9 and the agreement formula are PR #10's frozen values. They are a reasonable default for float64 dual evaluation, but they must be re-frozen per study.
- The "at least eight final verified passes" and "more than two runs … UNRESOLVED" clauses are PR #10's frozen instance of the B5 defaults.
- Two-stage seal: Stage 1 trains and seals checkpoint hashes with no target evaluation, then Stage 2 scores. Future practice (PR #10 errata E-D1, `results_v1_errata/ERRATA_v1.md` @ `0329818`) is an immutable Stage 0 manifest plus a dated addendum.

### B4. W-REL named-rival battery (theory-stage) — METHOD; RESULTS EXECUTED AND REVIEWED (verification gap closed; A2 reference conjunction attained; named controls not evaluated)

**v1.2 status.**
- W-REL was approved by Aidan at 8:58 AM ET (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6…7687`), executed in PR #11, and reviewed in `/workspace/review/wrel_results_review_v1.md` (sha256 `60c3f5a9a333e092ad625955696a0533e23ab667b3e332c3e0f6a7fa9cae8ace`).
- Results and their status are in U10. This section keeps the frozen method.

**Source:** `/workspace/review/c4_reliability_exact_check_spec_FINAL.md` §3, §4.4–§4.6 (box; not in the repo).

**Rivals:**
- R-HAC-MB (reference) and R-HAC-MB-myopic;
- the oracle;
- R-BLIND/R-CONF-S (one control);
- R-CONF-A;
- R-HAC-MF (eligible only at T_SEP = 3);
- R-CG;
- PM-ACT (policy-minimized).

All share the supplied first-order predictor F0 and are exact analytic agents.

**Core criteria:**
- **C-REF.** Δ_R ≥ 1/100 and Δ_M ≥ 1/100.
- **C-T2.** Relative reduction of squared error against the prior-marginal baseline ≥ 1/2. A zero baseline is "not demonstrated", never a pass.
- **C-SEL.** Under I-SWAP, the signed assessment error moves in the predicted direction (≥ 1/100) and the checking probability follows (≥ 1/100), in both directions.
- **C-FO.** Exact equality of pre-check probabilities and binary decisions under every intervention.
- **Rescue.** Signed reversals ≥ 1/100 plus L_A − L_B ≥ 1/100, for I-SWAP-S **and** I-SWAP-E.

**Reproduction rule** (verbatim): "Reproduction is YES only when every required component is available and within tolerance. It is NO when at least one available component demonstrably exceeds tolerance or disagrees on an exact equality flag. Otherwise it is UNRESOLVED, with the unavailable components listed. Missing components are never imputed."

Tolerance: 1/1000 per component.

**Decision order per setting:**
1. `UNRESOLVED-COMPUTE` (frozen label name in the spec's decision order);
2. UNRESOLVED-DESIGN (reference undefined);
3. REFERENCE CRITERIA NOT MET;
4. PATTERN REPRODUCED BY NAMED CONTROL;
5. CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED;
6. UNRESOLVED-DESIGN (an essential comparison is unavailable, or a reproduction is UNRESOLVED);
7. DISTINGUISHES NAMED CONTROLS.

**Claim lock.** "Policy minimization alone does not establish absence of an assessment role." No outcome is a C4 or consciousness claim.

**Status (v1.4).** Astra #29 edit E29-6 (verbatim):
> "The original W-REL verification gap has been closed. Exploratory A2 attained the reference conjunction at (1/100,3/50), T_SEP=3 and 4. Named controls at these settings remain unevaluated. This update changes neither Track A's closure verdict nor any C4 evidence or status row."

The record, the labels and Astra's ledger wording are in U10.

**Portability lesson (Astra #26 E-W5/E-W6, verbatim).** "The chosen A-SEP settings were not checked prospectively for joint criterion attainability." A Track B study must check criterion attainability and action dominance for its reference *before* freezing its settings. (W-REL itself later established attainment at the two A2 settings; see U10.)

### B5. Seed bar and invalid-seed rule: DEFAULTS each Track B study must freeze

**These are defaults, not universal rules.** Each Track B study must state and freeze its own replication bar and invalid-seed rule in its own protocol, before any confirmatory outcome exists. It may adopt the defaults below or justify different values. A study that does not freeze them has no bar.

**Default 1: replication bar 8/10.**
- At least eight of ten prespecified confirmatory seeds must jointly satisfy validity, eligibility and every per-seed criterion.
- The denominator stays ten, and seeds are not removed from it.
- There is no intermediate band.

**Default 2: more than two invalid seeds = UNRESOLVED.**
- Apply after any prerequisite check, and before the count rule.
- Other eligibility failures remain scientific non-passes. They are not invalidity.

**Default precedence:**
1. Prerequisite not replicated → UNRESOLVED (prerequisite).
2. Default 2.
3. Default 1.

**Frozen instances on record.** These are verbatim and binding only within their own studies:
- **PR #8** (`GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb` §7): "At least eight of the ten prespecified phase-B seeds jointly satisfy validity, eligibility, D and M. The denominator remains ten; seeds are not removed from it." The precedence is "E1 not replicated" first, then "More than two invalid seeds" gives "UNRESOLVED".
- **PR #9** (`first_order_control_protocol_FINAL.md` @ `4f6fc4c` §7, consult #17 edit 8): "After the E1 prerequisite, if more than two distinct seeds are invalid or have a collapsed control family for the target, report UNRESOLVED (insufficient evaluable seeds). Otherwise retain the denominator of ten."
- **PR #10** (`frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818` §7; see B3 Excerpt 6): "At least eight final verified passes earns TARGET REACHED REPRODUCIBLY. If more than two runs are invalid or numerically unresolved, the reproducibility label is UNRESOLVED; otherwise fewer than eight passes gives REPRODUCIBILITY CRITERION NOT MET."
  - This instance counts *runs* per arm and includes numerically unresolved runs. That shows the default must be adapted and frozen per design.

**Why defaults, not rules.** The bar's power and false-pass rate depend on the per-seed criterion, the number of control draws (U9) and the seed count. A study with a different seed count or criterion must recompute and freeze its own bar.

**Exploratory phase (default).** Use separate seeds. The headline is only "EXPLORATORY (… ; NOT CONFIRMATORY)", with no aggregate verdict.

**Wording (default).** Write "below the declared materiality threshold", never "immaterial".

### B6. Organism-lineage portable tests (Track A → Track B)

These come from the AC record. Each names the failure it catches.

- **T-RIVAL: sweep the fixed-level and reactive family first.** Before claiming an adaptive switch, sweep the state-blind fixed level and the same-information reactive rule (AC11, BRIDGE 9_d). A rival matching the best learner = no acquired decision demonstrated. Sources: `AC11_DESIGN_CONTROLS_v2.md` @ `c348a67` and `BRIDGE_PHASE2_VERDICT_v1.md` @ `40528f8`.
- **T-INTERRUPT: functional interruption plus content-free rescue.** Cut the enabling production *during* the function, not at t=0. Require failure during function, before death, with content intact, and resumption under a machinery-only rescue labelled EXTERNAL. Sources: `AC92_RESULTS_v1.md` @ `125027b`; A0 T3.
- **T-OBS: observer-discard.** Discard the host's observational record mid-function. The trajectory endpoint must be byte-identical (`state_hash`). State whether per-tick comparison was done, and report the result as "endpoint agreement under the audited observer-discard procedure" (F4, Astra #25). Source: `AC95_RESULTS_v1.md` @ `d7925cf`.
- **T-INERT: byte-identity composition license.** Before attributing a difference to a new mechanism, show the change is byte-inert at the intact boundary (G1). Sources: `AC114_RESULTS_v1.md` @ `56ea176` and `AC115_RESULTS_v1.md` @ `dfa19ed`.
- **T-SCRAMBLE: selective, expenditure-matched content ablation.** A scramble must override reads only (writes intact), with matched expenditure. Otherwise it confounds content with cost. Sources: AC106 errata P5 in `AC106_ERRATA_v1.md` @ `d8fd25b`; `AC116_ERRATA_v1.md` @ `e2e2ac6` §2.
- **T-DIRECT: same-information direct rival.** For any stored or maintained state, include a rival that reads the same information at decision time without storage (AC109). Storage must beat it to be load-bearing. Source: `AC109_ENGINEERING_v1.md` @ `d7e24fa`.
- **T-REACQ: correctness versus retention split.** Cut repair while leaving reacquisition intact. Require separate in-window correctness and post-window retention gates (AC110). Source: `AC110_RESULTS_v1.md` @ `928b938`.
- **T-RESTORE: cross-route discriminator.** Ask "what is restored, and whether it restores the conditions enabling restoration". Classify a result as (1) maintained sufficient state, (2) restored activity under intact constraints, or (3) restoration of enabling organization. Source: `ACI_PRIOR_ART_AND_REDUCTION_v1.md` @ `a72136c`.
- **Reporting rules:**
  - seeds, not histories, are the replication unit;
  - survival is a bimodality-aware lower bound;
  - nonsignificance is not equivalence (R1);
  - gate shape must match claim shape (AC16/AC17).

  Sources: `R1_AC113_REANALYSIS_v1.md` @ `38a19ae`; `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.3.

**B7. Q-separation lock (for every Track B report).**
- Q-EXIST: an exact or supplied solution exists.
- Q-LEARN: acquisition or transfer.
- Q-CAUSE: intervention-based causal contribution.
- Q-NECESSITY: requires a bound or complete search within a declared restricted class.

None upgrades another. No C-level, C4, C5, consciousness or organism conclusion follows from any of them.
