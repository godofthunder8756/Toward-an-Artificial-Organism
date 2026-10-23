src="/workspace/review/c4_reliability_assessment_admission_v3.md"
dst="/workspace/review/c4_reliability_assessment_admission_v3_1.md"
t=open(src).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:70],t.count(a)); t=t.replace(a,b)
# header
s=t.index("**Admission status, recorded exactly"); 
t='''# Learned assessment of internal processing reliability with costly rechecking: C4 admission and identifiability (v3.1, theory only; synchronization revision of v3 after Astra consult #23)

**Status.** v3.1, written 2026-10-21, about 5:10–5:40 AM ET, by the Research Delegate executor for the ACI Research Specialist, for Aidan Ahern.

**Why v3.1 exists.** Consult #23 named edits 1 and 7 require changes to the admission document:
- edit 1 replaces the §7 F-ID automatic-revision rule;
- edit 7 synchronizes the binary tie rule and removes the `sign(p − 1/2) = X` definition.

Consult #23 Q2 (limitation) and Q10 (ledger line) are also recorded. Every other v3 text is carried forward unchanged except for spec references, which now point to spec v3. v3.1 changes are marked **[v3.1]**.

**[v3.1] Card status (consult #23, part A).** "Admission v3 retains **ADMIT AS THEORY-STAGE C4 CANDIDATE** as a card status." This is a card status only, not a C4 claim.

**[v3.1] Ledger line (consult #23, Q10, verbatim):**

> "W-REL: admitted as a theory-stage C4 candidate. Exact-check specification under revision; execution pending Aidan's approval. No change to the C4 evidence or status row, and no system-level C4 conclusion."

'''+t[s:]
rep('''- This is an **additive** revision. Both earlier files are left untouched:

  | file | sha256 |
  | --- | --- |
  | `c4_reliability_assessment_admission_DRAFT.md` | dd463a2dfae6f93c07736d708ecc92b251d57481f72a63e893241703dc05523c |
  | `c4_reliability_assessment_admission_v2.md` | ef401a4b33c93bf787419da10f339b646f20ccb6267172d0d0a51ec9e1f52162 |''',
'''- This is an **additive** revision. All earlier files are left untouched:

  | file | sha256 |
  | --- | --- |
  | `c4_reliability_assessment_admission_DRAFT.md` | dd463a2dfae6f93c07736d708ecc92b251d57481f72a63e893241703dc05523c |
  | `c4_reliability_assessment_admission_v2.md` | ef401a4b33c93bf787419da10f339b646f20ccb6267172d0d0a51ec9e1f52162 |
  | `c4_reliability_assessment_admission_v3.md` | f122b47fbdd281a444f862021428dd3fa4e2569627f9aa745fa016fb9bde677a |''')
rep("- Change logs: §13 (DRAFT → v2) and §14 (v2 → v3).","- Change logs: §13 (DRAFT → v2), §14 (v2 → v3) and §15 (v3 → v3.1).")
rep('''**Work done for v3.**
- No training, no repo changes.
- No computation of any result. No exact-fraction re-check was run, and no number changed.
- Only a document consistency script was run (`/workspace/scratch/c4_reliability/v3_check/`). It checks text and hashes only.
- The bounded exact check is specified, **not run**, in the companion `c4_reliability_exact_check_spec_v2.md` (spec v2). It is PENDING Aidan's approval (§11).''',
'''**Work done for v3 and v3.1.**
- No training, no repo changes.
- No computation of any result. No number changed.
- Only document consistency scripts were run (`/workspace/scratch/c4_reliability/v3_check/` and `v3_1_check/`). They check text and hashes only.
- **[v3.1]** The bounded exact check is specified, **not run**, in the companion `c4_reliability_exact_check_spec_v3.md` (spec v3). It is PENDING Aidan's approval (§11).''')
t=t.replace("spec v2 §4.5","spec v3 §4.4").replace("spec v2","spec v3")
# edit 7 tie rule sync
rep("- **Correctness criterion:** K_t(a) = 1[sign(p̂ᵃ_t − 1/2) = X_t], the learner's own post-action correctness. A log-loss variant is reported separately.",
"- **Correctness criterion [v3.1, synchronized with spec v3 §0.2]:** K_t(a) = 1[d_t(a) = X_t], the learner's own post-action correctness.\n  - The binary decision is d_t(a) = 1 iff p̂ᵃ_t > 1/2, otherwise 0. This is the frozen tie rule.\n  - In the exact check, probabilistic quality is reported by expected Brier score. Log scores are not used: consult #23 edit 6, \"Expected Brier scores remain rational; log scores generally do not.\"")
rep('''- **Second-order false alarms and misses.**''','''- **Second-order false alarms and misses** (construct-level; [v3.1] terminology note).
  - In the exact check, signed C-SEL errors are named "overestimation" and "underestimation of own correctness" (consult #23 edit 3).
  - Consult #23: "Overestimating correctness is not automatically a false alarm about unreliability; those labels require a separately defined alarm convention."
  - The definitions below remain construct-level intentions for a later study. They are not exact-check outputs.''')
rep('''- **[v3]** The A-SEP analysis (spec v3 §4) reports one of five labels: DISTINGUISHES NAMED CONTROLS, PATTERN REPRODUCED BY NAMED CONTROL, REFERENCE CRITERIA NOT MET, UNRESOLVED-DESIGN or UNRESOLVED-COMPUTE.''',
'''- **[v3.1]** The A-SEP analysis (spec v3 §4.5) reports, per setting, one of six labels:
  - DISTINGUISHES NAMED CONTROLS;
  - PATTERN REPRODUCED BY NAMED CONTROL;
  - CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED;
  - REFERENCE CRITERIA NOT MET;
  - UNRESOLVED-DESIGN;
  - UNRESOLVED-COMPUTE.

  Per-control reproduction and criterion-attainment columns are reported separately.''')
rep("separate outcome-level false-alarm and miss frequencies: spec v3 §4.4.","separate outcome-level overestimation and underestimation frequencies: spec v3 §4.4.")
# edit 1 F-ID
rep('''- **F-ID [new; revised in v3].** A-SEP (spec v3 §4) returns PATTERN REPRODUCED BY NAMED CONTROL or REFERENCE CRITERIA NOT MET.
  - The prespecified core criteria (C-REF, C-T2, C-SEL, C-FO and the specified rescue) then do not distinguish the reference from that named control. Alternatively, the reference itself fails them.
  - Any empirical study must first revise the criteria under a new version.
  - This does not establish that the reproducing control lacks the role, or that the reference has it. That interpretation "additionally requires a justified account of whether the reproducing control implements the role" (consult #22).''',
'''- **F-ID [new; revised in v3.1 per consult #23 edit 1].** A-SEP (spec v3 §4.5) returns REFERENCE CRITERIA NOT MET, PATTERN REPRODUCED BY NAMED CONTROL, or CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED.
  - **Rule (verbatim):** "Reproduction triggers examination of what the reproducing implementation does. Revision is required when the procedure fails to identify the proposed role, not merely because another implementation reproduces it."
  - REFERENCE CRITERIA NOT MET means the procedure did not identify the proposed role in the reference. Revision is then required before any empirical study.
  - Reproduction or shared core criteria lead to examination of the reproducing implementation. Revision is required only if that examination shows that the procedure fails to identify the role.
  - Neither outcome establishes that a control lacks the role or that the reference has it. That interpretation "additionally requires a justified account of whether the reproducing control implements the role" (consult #22).''')
rep("   - F-ID: revise the criteria under a new version.","   - F-ID [v3.1]: examine what the reproducing implementation does. Revise the criteria under a new version only when the procedure fails to identify the proposed role.")
# A11 limitation
rep('''  - The edit-3 distinction between own and oracle correctness is therefore not exercised by these analytic agents at these rates. It would matter for a learned predictor, other rates, or a scoring-rule reward. Flagged for Astra (§10.3).''',
'''  - The edit-3 distinction between own and oracle correctness is therefore not exercised by these analytic agents at these rates.
  - **[v3.1] Limitation (consult #23, Q2, verbatim):** "These analytic predictors share the oracle's binary decisions on the tested observation domain. The analysis therefore does not test whether assessment tracks predictor-specific departures from oracle correctness."
  - Binary K remains primary. No scoring-rule reward variant is added: "A scoring-rule reward would change optimal checking and warrants a separate version."''')
# 10.3 interpretive questions
rep('''**For consult #23:** see spec v3 §9. Interpretive questions carried here:
1. A11: given that analytic agents' binary own-correctness coincides with Bayes correctness at these rates, should the theory-stage C-T2 be scored on probabilities or proper scores (log or Brier)? Or should a scoring-rule reward variant be added so that edit 3's own-versus-oracle distinction is exercised?
2. Is the "theory-stage C4 candidate" admission status to be recorded in the program ledger as a card status only, with no change to the C4 row? This document assumes so.''',
'''**[v3.1] Consult #23 answered the two interpretive questions carried in v3:**

| v3 question | Consult #23 answer, as applied |
| --- | --- |
| A11: scoring of C-T2 | Binary K stays primary; limitation recorded verbatim (§10.2 A11); Brier loss descriptive; no scoring-rule variant. |
| Ledger status | Card status only; ledger line recorded verbatim (header). |

No interpretive question remains open in this admission document.''')
# approval
rep('''- Analysis specification and compute limit: **[v3]** `c4_reliability_exact_check_spec_v2.md`. This is the revision for consult #23 review; it is not yet the final frozen identifier.''',
'''- Analysis specification and compute limit: **[v3.1]** `c4_reliability_exact_check_spec_v3.md`. It is not yet the final frozen identifier. Its §8 carries consult #23's scope attachment verbatim and the approval-record template.
- Consult #23: "The existing question still matches this bounded theory-only scope. No replacement question is needed." "The currently submitted spec hash 04992f86 is not the final executable identifier after these edits."''')
# change log
rep("## Appendix A. Exact values (unchanged from DRAFT Appendix A)",'''## 15. Change log v3 → v3.1 [v3.1]

| Change | Source (consult #23) |
| --- | --- |
| Card status retained; ledger line verbatim | Part A, Q10 |
| F-ID automatic-revision rule replaced with edit 1 wording; Q7 failure branch synchronized | edit 1 |
| Six A-SEP labels, including CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED | Q1 |
| K_t(a) uses the frozen binary tie rule; `sign(...)` definition removed; log-loss variant replaced by Brier (exact check) | edit 7, edit 6 |
| Over/underestimation terminology note | edit 3 |
| A11 limitation verbatim | Q2 |
| Spec references → spec v3 | — |
| **Numbers:** none changed; nothing computed | — |

---

## Appendix A. Exact values (unchanged from DRAFT Appendix A)''')
open(dst,"w").write(t); print(len(t))
