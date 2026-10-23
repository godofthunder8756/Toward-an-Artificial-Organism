import hashlib, sys
sys.path.insert(0,'/workspace/scratch/astra29'); from common29 import *
SRC='/workspace/review/track_a_lineage_triage_v1_3.md'; DST='/workspace/review/track_a_lineage_triage_v1_4.md'
raw=open(SRC,'rb').read(); assert hashlib.sha256(raw).hexdigest()=='167c7e67791bb24e2ec7667c4c669fd96fd5b9bf48f9e307fd7f5cb07e579b66'
s=raw.decode()
def rep(a,b,n=1):
    global s; c=s.count(a); assert c==n,(c,a[:90]); s=s.replace(a,b)
def between(a,b,new):
    global s; i=s.index(a); j=s.index(b,i+len(a)); s=s[:i]+new+s[j:]
PRREC=("PR #11 branch fetched read-only (`refs/pull/11/head` → `dddd63c`, 2026-10-21 12:32 PM ET). Records:\n"
"  - Addendum A1 verification result: `c4_reliability_exact_check_v1/RESULTS_v3.md` @ `0e17a05`, lines 9–17 and 25–36. The missing ITEM-8 replay AGREES with 0 mismatches, status COMPLETE. ITEM-9 now agrees on every replayed quantity, and the earlier incomplete-coverage status is lifted. The four original formal labels are unchanged.\n"
"  - Policy-coverage close-out: `c4_reliability_exact_check_v1/WREL_CLOSEOUT_E27_v1.md` @ `7b89c66`, lines 9–13. Condition (a) holds: the independently rebuilt reference policy was the object used in the required intervention and rescue replay. Condition (b), a stored action-table comparison, is not established.\n"
"  - Addendum A2 result: `c4_reliability_exact_check_v1/RESULTS_A2.md` @ `dddd63c`, lines 9, 30–44, 73–79, 92–106 and 135–141, with `c4_reliability_exact_check_v1/outputs/attainability_A2/SUMMARY.json` @ `dddd63c`. At T_SEP = 3 and 4:\n"
"    - reference conjunction ATTAINED; C-REF, C-T2, C-SEL, C-FO and rescue all PASS; status COMPLETE;\n"
"    - primary and replay agree, with 0 action disagreements (432 and 1552 rows);\n"
"    - the formal label is UNRESOLVED-DESIGN, from `decide_setting` called with an empty control list.\n"
"  - A2 approval: `c4_reliability_exact_check_v1/c4_reliability_APPROVAL_ADDENDUM_A2.md` @ `fb3e9b4`. Frozen spec, code and manifest: `c4_reliability_exact_check_v1/c4_reliability_exact_check_spec_ADDENDUM_A2.md` @ `8a4b393`.")
rep("# Track A lineage triage v1.3:","# Track A lineage triage v1.4:")
rep("v1.3 built about 12:11 PM–1 PM ET |","v1.3 built about 12:11 PM–1 PM ET; v1.4 built about 2:22–3 PM ET |")
rep("| Supersedes | `track_a_lineage_triage_v1_2.md` (sha256 `84fa9614…fdb09`), left untouched; built from it by `/workspace/scratch/track_a_triage/v1_3/build_v1_3.py`.",
"| Supersedes | `track_a_lineage_triage_v1_3.md` (sha256 `167c7e67…79b66`), left untouched; built from it by `/workspace/scratch/track_a_triage/v1_4/build_v1_4.py`. v1.3 superseded `track_a_lineage_triage_v1_2.md` (sha256 `84fa9614…fdb09`), built by `/workspace/scratch/track_a_triage/v1_3/build_v1_3.py`.")
rep("W-REL results: PR #11 (via the review below) |","W-REL results: PR #11 (via the review below; v1.4 also read the PR #11 branch head `dddd63c`, fetched read-only) |")
rep("Consult #26: formal A-SEP is **UNRESOLVED-COMPUTE** (ITEM-9 validation incomplete); per-setting labels are conditional classifications (U10) |",
f"v1.4 (Astra #29 {C29}, checked against the PR #11 record): the verification gap is closed (Addendum A1, `0e17a05`). Addendum A2 attained the reference conjunction at (1/100, 3/50), T_SEP = 3 and 4 (`dddd63c`). Named controls were not evaluated (U10) |")
rep("| U1 | Addressed by the U1 audit v1.1,","| U1 | Addressed by the U1 audit v1.1 and v1.2 (`/workspace/review/u1_substrate_audit_v1_2.md`; I12 PROVISIONAL),")
rep("- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.\n",f"- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.\n- {SEP}\n")
rep("## Changelog v1.3 against v1.2",f"""## Changelog v1.4 against v1.3 (`167c7e67…79b66`)

Paper only. Source: Astra consult #29 {C29}. Its W-REL statements were checked against the PR #11 branch (fetched read-only, head `dddd63c`) before being written; the record supports them (U10).
1. **E29-6 added verbatim** (Track A status; §0 and U10). The stale W-REL entries are replaced in the header, §1 counts, U10 and B4, using Astra #29's ledger wording and E29-1. The earlier formal status sentence and the proposed future two-setting check are dropped; v1.2's changelog keeps them as history.
2. **Birth targeting (I12) is PROVISIONAL** (F1, §1, U1). The code evidence is the U1 audit v1.2 §4.2, which states what the code shows and what it does not; Astra #28 is not cited as a code certification.
3. **Systems separation stated** (§0, §3): the AC lineage and the GRU-8 studies are separate systems and do not jointly establish one organism. Each "8/10" contribution now names PR #9 FO+ISO and its per-seed joint rule (S15, S15 rival, U9).
4. **"Resolved by" becomes "would be tested by"** in proposed tests. v1.3 had none outside quotes, so no text changed for this edit; the check confirms none remain.
5. **Other Track A items from #29 Q4** are recorded: Astra's acceptance of the revised closure statement (verdict line). The closure sentence, E28-1 and E28-2 are unchanged. E29-1 and Astra's ledger wording are used only for the W-REL status. E29-2 to E29-5 and E29-7 (W-REL detail, Track B, program boundary) are not applied as Track A edits, and the #29 §D approval question is not approved or proposed here.

## Changelog v1.3 against v1.2""")
rep("- (v1.2) read-only attainability extraction `/workspace/review/wrel_attainability_from_existing_outputs_v1.md`.",
"- (v1.2) read-only extraction from existing outputs `/workspace/review/wrel_attainability_from_existing_outputs_v1.md`. Its status lines are historical; the current status is in U10 (v1.4).\n- (v1.4) Astra consult #29 "+C29+".")
rep("| ADDRESSED (audit done; Astra items open) | 1 | U1 |","| ADDRESSED (audit done; Astra #28 rulings applied; I12 PROVISIONAL) | 1 | U1 |")
rep("| EXECUTED AND REVIEWED; formal A-SEP UNRESOLVED-COMPUTE | 1 | U10 |","| EXECUTED AND REVIEWED; verification gap closed; A2 reference conjunction attained; named controls not evaluated | 1 | U10 |")
rep("Astra #28 ruled on Q-A1–Q-A3, and birth targeting is supplied targeting.","Astra #28 ruled on Q-A1–Q-A3. Birth targeting is classified as supplied targeting, PROVISIONAL (audit v1.2 §4.2).")
# F1 excluded bullet
rep("However, birth targeting at `ac9.py` @ `6c6323b` (line 108, \"every bank with demand\") is **EXTERNAL COORDINATION (supplied targeting)** per Astra #28 (audit v1.1 I12 and §4.1).",
"However, birth targeting at `ac9.py` @ `6c6323b` (line 108, \"every bank with demand\") is classified **EXTERNAL COORDINATION (supplied targeting), PROVISIONAL**. Astra #28's judgment was provisional on the supplied description. The code evidence is the U1 audit v1.2 §4.2: a host-written bank list selects which functional W groups receive births. That reading does not show necessity for any W/C/B result.")
# U1
rep("**birth targeting** at `ac9.py` @ `6c6323b` (I12, supplied targeting);","**birth targeting** at `ac9.py` @ `6c6323b` (I12, supplied targeting, PROVISIONAL);")
rep("- **Q-A2: ruled supplied targeting.** \"For","- **Q-A2: provisional judgment (Astra #28), now PROVISIONAL in v1.4.** \"For")
rep("The audit v1.1 §4.1 gives the code-level explanation that Astra asked for, and no run is needed.",
f"The audit v1.1 §4.1 gives the code-level explanation. Astra #29 (verbatim): {PROV} The audit v1.2 §4.2 sets out what that code reading establishes and what it does not.")
# §3 separation
rep("## 3. SUPPORTING\n\n",f"## 3. SUPPORTING\n\n{SEP} S12–S15 are GRU-8 findings; the other rows here concern the AC lineage or evidence integrity.\n\n")
rep("REPLICATED at **exactly 8/10** (D_FO 10/10, D_ISO 8/10, M 10/10).",
"REPLICATED at **exactly 8/10** under its declared per-seed joint rule (D_FO and D_ISO in each seed, with materiality M): D_FO 10/10, D_ISO 8/10, D_FO and D_ISO 8/10, M 10/10, joint 8/10. GRU-8 system, separate from the AC lineage.")
rep("  - *Excluded at 8/10 for the sampled families:* D_FO 10/10, D_ISO 8/10 (`first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`).",
"  - *Excluded at 8/10 for the sampled families,* in PR #9 FO+ISO (GRU-8) under the per-seed joint rule D_FO and D_ISO (with M): D_FO 10/10, D_ISO 8/10, joint 8/10 (`first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`).")
rep("- The REPLICATED label is at exactly 8/10. Each failing seed lost to one isotropic draw.",
"- The PR #9 FO+ISO (GRU-8) REPLICATED label is at exactly 8/10, under the per-seed joint rule D_FO and D_ISO (with M). Each failing seed lost to one isotropic draw.")
# U10
rep("### U10. W-REL exact check — EXECUTED AND REVIEWED; formal A-SEP UNRESOLVED-COMPUTE; labels conditional",
"### U10. W-REL exact check — EXECUTED AND REVIEWED; verification gap closed; A2 reference conjunction attained; named controls not evaluated")
between("- **Formal A-SEP: UNRESOLVED-COMPUTE.**","**Review items A1–A4, as ruled by Astra #26.**",f"""- **v1.4 status (Astra #29; verified against the PR #11 record before writing).** Astra #29 says (verbatim): {STALE}
- {PRREC}
- **Ledger wording (Astra #29, verbatim):**
  > {LEDGER}
- **A2 scope (Astra #29 edit E29-1, verbatim):**
  > {E291}
- **On conditions (a) and (b) (Astra #29, verbatim):** {ORALT}
- **Track A status (Astra #29 edit E29-6, verbatim):**
  > {E296}

**Formal per-setting labels, original four settings** (unchanged; `c4_reliability_exact_check_v1/RESULTS_v3.md` @ `0e17a05`, lines 29–36):

| T_SEP | (c_R, c_S) | Formal label |
| ---: | --- | --- |
| 3 | (1/50, 3/50) | UNRESOLVED-DESIGN; no donor contrast; C-REF and C-T2 also fail |
| 4 | (1/50, 3/50) | UNRESOLVED-DESIGN; same reasons |
| 3 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET; C-REF and C-SEL fail |
| 4 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET; C-REF fails |

**Addendum A2 settings** (`c4_reliability_exact_check_v1/RESULTS_A2.md` @ `dddd63c`): at (1/100, 3/50), T_SEP = 3 and 4, the reference conjunction was ATTAINED. The formal label is UNRESOLVED-DESIGN from the empty-control invocation, reported with NAMED-CONTROL COMPARISON: NOT RUN (E29-1).

""")
rep("- **A2:** \"The coverage qualifier alone is insufficient.\" This produces the formal UNRESOLVED-COMPUTE above.",
"- **A2:** \"The coverage qualifier alone is insufficient.\" That ground was removed when Addendum A1 closed the verification gap (above).")
between("- **A4, attainability:**","- **A5** (v2 only)","""- **A4:** "Not immediately." The read-only extraction from existing outputs (`/workspace/review/wrel_attainability_from_existing_outputs_v1.md`) left (T_SEP, c_R, c_S) = (3, 1/100, 3/50) and (4, 1/100, 3/50) open. The separately approved Addendum A2 (`fb3e9b4`) then evaluated exactly those two and attained the reference conjunction at both (above). The extraction's status lines are historical.
""")
rep("- No setting received that label. The reference met its own core criteria in no tested setting, so no separation is supported or refuted, and no reduction entry follows.",
"- No setting received that label. In the four original settings the reference did not meet its core criteria. In the two A2 settings it attained them, but no named control was evaluated. So no separation is supported or refuted, and no reduction entry follows.")
rep("**Q-tags.** Q-EXIST (world/identifiability): ITEM-1. Q-CAUSE: nothing established.",
"**Q-tags.** Q-EXIST (world/identifiability): ITEM-1. Q-CAUSE: A2 component findings only, restricted per Astra #29 to \"the declared donor interventions and first-order probe battery\"; no separation is established.")
between("- The W-REL ledger row (Astra #26 §B.5 wording).","**Stopping criterion.**","""- The W-REL ledger row, now Astra #29's wording (above).
- The next W-REL decision: Astra #29 recommends one bounded named-control comparison at the two A2 settings. Its approval question (#29 §D) is for Aidan and is neither approved nor proposed here.

""")
between("- (a) Complete mandatory ITEM-9 validation only","- (c) Do not add costs or horizons after seeing failures.",f"""- (a) Met: the mandatory verification was completed under Addendum A1 (`0e17a05`).
- (b) Met: Addendum A2 evaluated only the two open settings (`dddd63c`).
""")
rep("- (c) Do not add costs or horizons after seeing failures.",f"- (c) Do not add costs or horizons after seeing failures. Astra #29 (verbatim): {NOEXT}")
# B4
rep("— METHOD; RESULTS EXECUTED AND REVIEWED (formal A-SEP UNRESOLVED-COMPUTE)","— METHOD; RESULTS EXECUTED AND REVIEWED (verification gap closed; A2 reference conjunction attained; named controls not evaluated)")
rep("1. UNRESOLVED-COMPUTE;\n","1. `UNRESOLVED-COMPUTE` (frozen label name in the spec's decision order);\n")
rep("**Status (v1.2).** Formal A-SEP is UNRESOLVED-COMPUTE (Astra #26). Conditional per-setting classifications are in U10.",
f"**Status (v1.4).** Astra #29 edit E29-6 (verbatim):\n> {E296}\n\nThe record, the labels and Astra's ledger wording are in U10.")
rep("A Track B study must check criterion attainability and action dominance for its reference *before* freezing its settings.",
"A Track B study must check criterion attainability and action dominance for its reference *before* freezing its settings. (W-REL itself later established attainment at the two A2 settings; see U10.)")
# §6
rep("## 6. Verification of this document\n","""## 6. Verification of this document

**v1.4.** `/workspace/scratch/astra29/check_e29.py` (log `check_e29.log`) checks this file together with the audit v1.2 and the synthesis v1.2. It checks that:
- Astra #29 quotations are verbatim;
- `` `path` @ `commit` `` pairs exist, including the PR #11 commits, and the PR #11 record supports the W-REL statements;
- no "resolved by" appears outside quotes;
- no earlier formal-status or attainability-check text appears outside the changelogs and quotes;
- the closure sentence is byte-identical across the three files;
- each "8/10" contribution names PR #9 FO+ISO and its joint rule;
- forbidden phrases are absent;
- earlier versions are unchanged.
""")
open(DST,'w').write(s); print('ok')
