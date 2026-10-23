src="/workspace/review/c4_reliability_assessment_admission_v2.md"
dst="/workspace/review/c4_reliability_assessment_admission_v3.md"
t=open(src).read()
def rep(a,b):
    global t
    assert t.count(a)==1, ("not unique/absent", a[:80], t.count(a))
    t=t.replace(a,b)

# --- header ---
head_old=t[:t.index("**Approvals.**")]
head_new='''# Learned assessment of internal processing reliability with costly rechecking: C4 admission and identifiability (v3, theory only; additive revision of v2 after Astra consult #22)

**Status.** v3, written 2026-10-21, about 4:40–5:10 AM ET, by the Research Delegate executor for the ACI Research Specialist, for Aidan Ahern.

**Admission status, recorded exactly as Astra worded it (consult #22, part A):**

> "**A: ADMIT AS THEORY-STAGE C4 CANDIDATE, with the interpretive edits below.** This admits the question for analytic investigation, not the proposed separation test or any C4 conclusion."

**What "theory-stage C4 candidate" is and is not.**
- It is an **admission status**: the question is admitted for analytic investigation.
- It is **not a C4 claim**. No C4 status, no C4 evidence row, and no C5 or consciousness claim is made or implied.
- The admission does not extend to the proposed separation test: consult #22 part B, "REVISE the exact-check spec before freezing".
- Nothing here is evidence of any C-level for any system.

**Card class.** ANALYTIC / admission-criteria (constitution v3). It authorizes no experiment.

**Relation to earlier versions.**
- This is an **additive** revision. Both earlier files are left untouched:

  | file | sha256 |
  | --- | --- |
  | `c4_reliability_assessment_admission_DRAFT.md` | dd463a2dfae6f93c07736d708ecc92b251d57481f72a63e893241703dc05523c |
  | `c4_reliability_assessment_admission_v2.md` | ef401a4b33c93bf787419da10f339b646f20ccb6267172d0d0a51ec9e1f52162 |

- v2 text is carried forward except where marked **[v3]**.
- Section markers **[replaces DRAFT §x]** and **[new]** refer to the DRAFT, as in v2.
- Change logs: §13 (DRAFT → v2) and §14 (v2 → v3).

**Astra edit 8 of consult #21 (verbatim, retained).** This is **theory about C4 admission**, not evidence that the work is "below C4 throughout." It authorizes no empirical study and establishes no C4 status.

**What this document asserts.** It makes no C4, C5 or consciousness claim. Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate and labelled at every use.

**Work done for v3.**
- No training, no repo changes.
- No computation of any result. No exact-fraction re-check was run, and no number changed.
- Only a document consistency script was run (`/workspace/scratch/c4_reliability/v3_check/`). It checks text and hashes only.
- The bounded exact check is specified, **not run**, in the companion `c4_reliability_exact_check_spec_v2.md` (spec v2). It is PENDING Aidan's approval (§11).

'''
t=head_new+t[len(head_old):]

# --- §1 assumptions and primary law ---
rep('''  - In both, P(Z_0 = S) = 1/2.
''','''  - In both, P(Z_0 = S) = 1/2.
  - **[v3]** Consult #22, Q1: "**H0 primary: acceptable.**" "A static but unknown regime is a legitimate persistent latent variable. It isolates information acquisition from tracking a changing source. H1 is a useful secondary condition; switching need not be primary."
- **[v3] Independence and exogeneity assumptions.** Consult #22, Q1 (verbatim): "State explicitly that X values, costs and policy randomization are independent of Z, and that Z evolves exogenously. Under those assumptions, the L1 factorization argument is sound."
  - (i) X_t is uniform and independent of Z.
  - (ii) Costs, and any cost-switch schedule, are set independently of Z.
  - (iii) Any policy randomization is independent of Z, given observables.
  - (iv) Z evolves exogenously: actions, predictions and outcomes do not affect the transition law.
- **[v3] Event order and cost information:** as frozen in spec v2 §0. Only current costs are visible.
''')

# --- L1 status ---
rep('''**Status.** This is an analytic proof. Its exact verification (spec §1, A-SYM) is **pending approval and not run**. The single-trial statement in DRAFT D1, "no learner can distinguish…", is **not** carried into the persistent setting except through L1 (Astra edit 5).''',
'''**[v3] Assumptions.** L1 holds under the §1 independence and exogeneity assumptions (i)–(iv).

**[v3] L1 conclusion (consult #22, Q1, verbatim wording):**

> "Without recheck observations, the observation history supplies no information about Z beyond its propagated prior. Recheck observations can be informative. This does not imply perfect identification of the realized regime within a finite horizon."

**[v3] Status.** The factorization proof is the support for the claim at every horizon. The exact A-SYM item in spec v2 (pending approval, **not run**) does not replace it. Consult #22 (verbatim): "The T <= 3 audit checks the implementation. The factorization proof, not that finite audit alone, supports the general horizon claim."

The single-trial statement in DRAFT D1, "no learner can distinguish…", is **not** carried into the persistent setting except through L1 (Astra edit 5 of consult #21).''')

# --- §3 counterfactual target ---
rep('''  - For non-taken actions, K_t(a) is obtained in analysis only, by world-side replay of the same trial with a fixed noise seed. This is analysis apparatus, not an agent register.''',
'''  - **[v3]** For non-taken actions the target is an expectation, not a single replay. Consult #22, Q3 (verbatim): "A fixed replay produces one counterfactual outcome. It does not produce `E[K(a) | information]`." The exact analysis uses:

    ```text
    m_a(H) = sum_omega P(omega | H) *
             1[agent_prediction(H, do(a), omega) = X(omega)]
    ```

    Here H is the declared observable information at the decision, and ω includes the remaining latent variables and observation noise.
  - **[v3]** The full-history target m_a(H) and the state-conditioned target m_a(s_agent) are reported separately wherever they differ: for PM, count-based and Q-based agents (spec v2 §4.3).
  - **[v3]** Interventions retain the recipient's world distribution and change only the specified agent content.
  - **[v3]** Common random numbers are permissible only for later numerical estimation, with correct action-specific marginals and disclosed coupling. They do not replace the expectation.
  - This is analysis apparatus, not an agent register.''')

# --- R-CG wording ---
rep('''- **R-CG, the cost-general controller [new; the decisive conventional rival].**''',
'''- **R-CG, cost-general controller baselines [new; wording revised in v3].** Consult #22, Q5 wording, adopted verbatim:

  > "A prespecified family of cost-general conventional baselines; conclusions are restricted to these implementations."

  - **[v3]** The six R-CG variants are "useful named baselines, not a decisive conventional class". Non-myopic Bayes is kept "as the stronger model-based reference".
  - **[v3]** Count-per-(action, read class) variants "may also adapt poorly to regime changes. That is a limitation of these variants, not of conventional correctness estimation generally."
  - **[v3]** Complete update, prediction, bonus, initial-count and tie rules: spec v2 §3.''')

# --- §4.4 last bullet ---
rep('''- Whether the §5 criteria distinguish an **assessment** variable from a **policy-minimal** machine that reproduces the checking policy without cost-general correctness content is an open identification question. It is computed for the analytic agents in spec §4 (pending).''',
'''- **[v3]** The A-SEP analysis (spec v2 §4) reports one of five labels: DISTINGUISHES NAMED CONTROLS, PATTERN REPRODUCED BY NAMED CONTROL, REFERENCE CRITERIA NOT MET, UNRESOLVED-DESIGN or UNRESOLVED-COMPUTE.
  - Consult #22 (verbatim): "Neither of the first two labels automatically establishes assessment-versus-policy separation. That interpretation additionally requires a justified account of whether the reproducing control implements the role."
  - The policy-minimized comparator is **not** a known role-absent control. Consult #22: "absence of an explicit correctness register does not prove absence of assessment content."''')

# --- §5.2 margins ---
rep('''Margins are to be derived later, from the decision sensitivity of each named rival to tolerated p̂ changes (open question 4).''',
'''Margins are to be derived later, from the decision sensitivity of each named rival to tolerated p̂ changes.

**[v3] Consult #22, Q4:** "decision-flip probability alone is insufficient." The analysis reports four things for every intervention:
- probability-vector changes;
- calibration and proper-score changes;
- action changes;
- value consequences.

Consult #22 (verbatim): "D5 already demonstrates why unchanged binary decisions can conceal changed inference."

The decision-flip bound adopted as a supplement, verbatim:

```text
If every estimated action correctness changes by at most epsilon,
an action-value gap greater than 2*epsilon cannot change sign.
```

"For non-myopic control, apply the bound to complete action values, including continuation value, rather than immediate correctness alone." "No analogous bound follows solely from `abs(Delta p0) <= 0.02`: the action system may depend on additional state. A decision-flip bound can supplement category-2 reporting, but cannot replace it."''')

# --- §7 F-ID ---
rep('''- **F-ID [new].** The causal criteria do not separate an assessment variable from a policy-minimal machine (spec §4, DOES-NOT-SEPARATE). The criteria are then insufficient as stated, and must be revised under a new version before any empirical study.''',
'''- **F-ID [new; revised in v3].** A-SEP (spec v2 §4) returns PATTERN REPRODUCED BY NAMED CONTROL or REFERENCE CRITERIA NOT MET.
  - The prespecified core criteria (C-REF, C-T2, C-SEL, C-FO and the specified rescue) then do not distinguish the reference from that named control. Alternatively, the reference itself fails them.
  - Any empirical study must first revise the criteria under a new version.
  - This does not establish that the reproducing control lacks the role, or that the reference has it. That interpretation "additionally requires a justified account of whether the reproducing control implements the role" (consult #22).''')

rep('''   - If it reproduces the observations **without** the role (for example, a policy-minimal machine), the tests have not identified the role (F-ID).''',
'''   - If it reproduces the observations **without** the role, the tests have not identified the role (F-ID).
   - **[v3]** A policy-minimized machine is not assumed to lack the role. Consult #22: "PM_k is therefore not automatically a known "role-absent" control."''')

# --- §9 answers ---
rep('''   - What is the finite-horizon VOI?
   - Do the §5 criteria separate an assessment variable from a policy-minimal checking machine, for the named analytic rivals?''',
'''   - **[v3]** What are planning_advantage_T, adaptive_information_advantage_T and oracle_gap_T (spec v2 §2)?
   - **[v3]** Which prespecified response patterns distinguish the named analytic implementations (spec v2 §4)?''')
rep('''6. **Q6. On success** (at theory stage: L1 verified, positive VOI, SEPARATES).''',
'''6. **Q6. On success** [v3] (theory stage: A-SYM verifies the implementation of L1; the A-SEP label is DISTINGUISHES NAMED CONTROLS, interpreted only within edit 8 below).''')
rep('''   - F-ID: revise the criteria under a new version.''','''   - F-ID: revise the criteria under a new version.
   - [v3] Cap reached: completed exact results are preserved; dependent unexecuted work is NOT-RUN; no overall label is issued.''')
rep('''    - **NOT established:** assessment of the learner's own representation; history-level identifiability (until A-SYM); acquired evaluation; any C4 status.''',
'''    - **[v3] Theory-stage ceiling (consult #22, edit 8, verbatim):** "The analysis reports which prespecified response patterns distinguish the named analytic implementations. Policy minimization alone does not establish absence of an assessment role. Any stronger construct-identification claim requires additional justification."
    - [v3] Consult #22 (verbatim): "The analytic agents have supplied mechanisms and update rules. Their results cannot establish acquisition, even if a controller updates its counts online."
    - **NOT established:** assessment of the learner's own representation; perfect identification of the realized regime; acquired evaluation; any C4 status. "Theory-stage C4 candidate" is an admission status only.''')
rep('''    - Theory success: "the W-REL-B criteria can separate an own-correctness assessment from a policy-minimal machine for named analytic agents".
    - F-ID: "the criteria as stated do not separate assessment from checking policy".''',
'''    - [v3] Theory outcome: "The analysis reports which prespecified response patterns distinguish the named analytic implementations. Policy minimization alone does not establish absence of an assessment role. Any stronger construct-identification claim requires additional justification."
    - F-ID: "the prespecified core criteria do not distinguish the reference from [named control]". No inference is drawn about whether either implements the role.''')

# --- §10.1 F6 note, §10.2 ambiguities ---
rep('''- **A10 [new].** K_t(a) for non-taken actions is defined by world-side counterfactual replay with a fixed noise seed.''',
'''- **A10 [revised in v3].** The counterfactual correctness target is the expectation m_a(H) over ω (§3), not a single replay. Full-history and state-conditioned targets are reported separately.
- **A11 [v3, new; analytic observation, interpretive].** At the illustrative rates, D5 says the S-model and E-model Bayes decisions agree on all 64 post-recheck observations.
  - Decisions also agree trivially for default and resample observations.
  - For a belief mixture, p(b) − 1/2 has the sign of a function linear in b. So, provided D5's equality holds under the frozen tie rule, every belief-weighted or prior-marginal predictor makes the **same binary decisions**. Spec v2 ITEM-1(d) re-verifies this; it is not run.
  - Consequence: for the analytic agents, the binary own-correctness K_t(a) does not differ from Bayes-oracle correctness. Only probabilities and proper scores differ.
  - The edit-3 distinction between own and oracle correctness is therefore not exercised by these analytic agents at these rates. It would matter for a learned predictor, other rates, or a scoring-rule reward. Flagged for Astra (§10.3).
- **A12 [v3, new].** Only current costs are visible to every agent.
  - Planning agents use the declared certainty-equivalent assumption that current costs persist.
  - The switch schedule is unknown to all agents (spec v2 §0.3).''')

# --- §10.3 open questions ---
oq_start=t.index("### 10.3 Open questions for Astra (consult #22)")
oq_end=t.index("## 11. Approval: PENDING [new]")
t=t[:oq_start]+'''### 10.3 Open questions [revised in v3]

**Consult #22 answered the v2 questions:**

| v2 question | Consult #22 answer, as applied |
| --- | --- |
| 1. H0 primary | Acceptable. Assumptions (i)–(iv) and the L1 conclusion wording added (§1, §1.2). |
| 2. PM test / SEPARATES | Not acceptable as written. Five labels; core criteria C-REF, C-T2, C-SEL, C-FO plus rescue; I-COST descriptive (spec v2 §4). |
| 3. World-side replay | Acceptable, but a single fixed seed is insufficient. m_a(H) expectation adopted (§3). |
| 4. Margins | Decision-flip probability alone insufficient. Four-way reporting plus the 2ε bound (§5.2). |
| 5. R-CG | Named baselines, not a decisive class. Rules completed in spec v2 §3. |
| 6. Hard cap | Acceptable. Accounting includes replay and restarts; item order frozen (spec v2 §5). |

**For consult #23:** see spec v2 §9. Interpretive questions carried here:
1. A11: given that analytic agents' binary own-correctness coincides with Bayes correctness at these rates, should the theory-stage C-T2 be scored on probabilities or proper scores (log or Brier)? Or should a scoring-rule reward variant be added so that edit 3's own-versus-oracle distinction is exercised?
2. Is the "theory-stage C4 candidate" admission status to be recorded in the program ledger as a card status only, with no change to the C4 row? This document assumes so.

---

'''+t[oq_end:]

# --- §11 approval ---
rep('''- Analysis specification and compute limit: `c4_reliability_exact_check_spec_draft_v1.md`.
- Prior approvals do not carry over.''',
'''- Analysis specification and compute limit: **[v3]** `c4_reliability_exact_check_spec_v2.md`. This is the revision for consult #23 review; it is not yet the final frozen identifier.
- **[v3] Approval-record additions (consult #22):** "Add the final spec identifier and the four-hour/one-hour/eight-GB limits to the approval record. Do not ask Aidan to approve the same scope again if he approves that question with this specification attached."
  - Limits: ≤ 4 hours total; ≤ 1 hour per named item; ≤ 8 GB; one CPU process.
- Consult #22: "The existing question still matches this revised analytic scope. Constructing and minimizing a named finite comparator is not an exhaustive all-controller certificate."
- Consult #22: "There is no answer yet, so execution remains pending."
- Prior approvals do not carry over.''')
rep('''- The only computation done since consult #21 is a sizing count (`plan_counts.py`).''',
'''- The only computation done since consult #21 is a sizing count (`plan_counts.py`). Since consult #22, only a document consistency script has run.''')

# --- §12/13 references ---
rep('''- A change log is in §12.''','') if '- A change log is in §12.' in t else None
rep('''| Analytic step that needs approval (solver-like) | **Addressed.** Companion spec, PENDING (§11). |''','''| Analytic step that needs approval (solver-like) | **Addressed.** Companion spec (v2), PENDING (§11). |''') if '| Analytic step that needs approval (solver-like) | **Addressed.** Companion spec, PENDING (§11). |' in t else None
rep('''| R-CG added (decisive); costs visible and continuous for all; no cost bins | Q6 |''','''| R-CG added; costs visible and continuous for all; no cost bins | Q6 |''')

# --- §14 change log ---
rep('''## Appendix A. Exact values (unchanged from DRAFT Appendix A)''','''## 14. Change log v2 → v3 [v3]

| Change | Source (consult #22) |
| --- | --- |
| Admission status recorded verbatim; admission status distinguished from a C4 claim | Part A |
| H0 primary accepted; H1 secondary | Q1 |
| Independence and exogeneity assumptions (i)–(iv) | Q1 |
| L1 conclusion wording verbatim; audit versus proof roles separated | Q1 |
| Counterfactual target m_a(H) as an expectation over ω; full-history versus state-conditioned; recipient world retained; CRN disclosure | Q3 |
| Four-way margin reporting; 2ε decision-flip bound as a supplement only | Q4 |
| R-CG described as "A prespecified family of cost-general conventional baselines; conclusions are restricted to these implementations." | Q5 |
| Five A-SEP labels replace the v2 binary label; PM not a known role-absent control; F-ID revised | Q2, edit 5 |
| Theory outcome narrowed to edit 8 wording | edit 8 |
| Acquisition cannot be established by analytic agents | edit 8 |
| Approval record: spec identifier + 4 h / 1 h / 8 GB; no re-approval of the same scope | Approval scope |
| A11 (analytic agents' binary own-correctness equals Bayes correctness at these rates), A12 (cost information) | new, flagged |
| **Numbers:** none changed; nothing computed | — |

---

## Appendix A. Exact values (unchanged from DRAFT Appendix A)''')
open(dst,"w").write(t)
print("written", len(t))
