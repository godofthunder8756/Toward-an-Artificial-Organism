# ACI frontier audit v1 (read-only)

Date: 2026-10-20, about 14:30 EDT. Auditor: ACI Research Specialist (Grok Bot) for Aidan Ahern.
Scope: read-only. I ran nothing scientific (no enumeration, solver, training or experiment)
and changed no tracked file. My only git actions were `git pull`,
`git fetch --unshallow` and a fetch of remote branch refs. These update `.git` metadata
only; `git status` is clean.

I checked the claims in `/workspace/aci_handoff.md`, a condensed copy of Aidan's handoff,
against the repository.

---

## 1. HEAD, branch, worktree, newer commits, kanban

| Check | Result |
| --- | --- |
| HEAD | `32cfbe6034fe1568eba360397c987c53b7404ccc`. **Matches the handoff.** |
| Branch | `master`, tracking `origin/master`. `git pull` reports "Already up to date". |
| Worktree | Clean: no modified or untracked tracked-path changes. |
| Newer commits on master | **None.** HEAD is the merge of PR #2 (copilot-swe-agent, 2026-10-20 13:39 EDT). PR #2 added only `.gitignore`, `CONTRIBUTING.md`, `docs/REPOSITORY_MAP.md`, `requirements.txt` and 22 README lines. The last research commit is `b7e7cae` (2026-10-06, SUB_A0 probe-v2 results). |
| Other remote branches | **`origin/elminster/loving-ptolemy-ityj4l`** has one commit not on master: `33fa803`, 2026-10-01 15:22 EDT, "SCARCITY_GAP_v1", co-authored by a Claude session. It adds `SCARCITY_GAP_v1.md` and `scarcity_v1/` (certificate, tests). It is **unmerged and unreviewed**, and it directly criticizes the pending two-stream package (§4 below). `origin/learned-vs-reactive` has one marker commit from 2026-09-16 pointing to a sibling repo, "earned-state". `origin/e3-obsolescence-side-branch` is fully merged (PR #1). |
| Kanban `.vscode/kanban-agent.json` | **38 cards: 35 done, 3 todo. Matches the handoff.** The three todo cards are #29 "A6 PARKED UNRESOLVED…", #31 "A8 PARKED: unresolved A6 leaves shared-code learning unauthorized…", and #38 "HUMAN APPROVAL REQUIRED: analytic first-order temporal-world admission; no learning". The board uses `task-…` ids and titles, not the `r10a-a6`/`r10a-a8` ids in the handoff; the content matches. |
| Admission board `.vscode/aci-research-cards-v1.json` | 6 cards. `aci-world-admission-human-gate` has `requires_human_approval: true` and `execution_authorized: false`. **Neither board has any SUB_A, SUB_A0 or SCARCITY card.** |
| Authorizations in force | Nothing is authorized to execute. README and tree v5 say "no neural training is authorized". The decision package is "DESIGN ONLY". The SUB_A0 options "need your explicit approval" (`SUB_A0_CAL_RESULTS_v2.md`). |

---

## 2. Canonical files read

All handoff Section-2 sources were read: README, REPOSITORY_MAP, constitution v3, tree v5,
evidence index v5 and v3 (structure plus Items 3–5), synthesis v1, belief ledger, A6
decision and reduction, next-experiment package and CONTRIBUTING. The frozen verdicts were
also read, with their audits and errata:
- `CLOSURE_VERDICT_v1.md` (K3)
- `I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md`, with `AC115_ERRATA_v1.md`
- `BRIDGE_PHASE2_VERDICT_v1.md`, with `BRIDGE_FINALS_AUDIT_v1.md`
- `PHASE3_VERDICT_v1.md`, with `PHASE3_INDEPENDENT_AUDIT_v1.md`
- `PHASE3B_VERDICT_v1.md`, with its audit `phase3b_results_v1/phase3b_final_audit_v1.json`, cited by hash
- `R10A_DECISION_v1.md`, with `r10a_v1/independent_audit.json`
- `AC116_ERRATA_v1.md`, `C1_RELIABILITY_DISPOSITION_v1.md`

Small defect found: the ledger's C4 evidence cites `N5_Evidence_Hierarchy_v1.md`, but the
file is `N5_EVIDENCE_HIERARCHY_v1.md`. That path breaks on case-sensitive filesystems. It is
the only missing ledger reference.

---

## 3. O0–O4 / C0–C7 frontier

Statuses come from `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` and `ACI_RESEARCH_SYNTHESIS_v1.md`.
The constitution (v3) says these are scope-specific synthesis assessments, **not a
consciousness ladder**.

### O-axis

| Layer | Status | Establishes (bounded) | Does NOT establish | Sources |
| --- | --- | --- | --- | --- |
| **O0** supplied organization | SUPPLIED | Current R9 weights, interpreter and functional machinery are host-guaranteed. The organism's primitive interpreter (`prog.choose`) and `advance()` are declared substrate (K3 resolved J1 as "substrate"; `advance()` is the larger concession). | That anything in R9 maintains itself. | Ledger O0; `R9_FUNCTION_CLASS_v1.md`; `CLOSURE_VERDICT_v1.md` §2 |
| **O1** internal maintenance | SUPPORTED_BOUNDED (organism only) | Paid, vulnerable, internal maintenance with ablation dependence. Neural N1 paid persistence: 0.978 vs 0.000, p=0.00049, 12/12. | Constitutive neural machinery maintenance. N1 is a substrate fact shared by fixed schedules ("must not later be cited as evidence that the learned allocator is load-bearing"). | Ledger O1; `BRIDGE_PHASE2_VERDICT_v1.md` §1; `ACI_MISSION_AUDIT_v1.md` |
| **O2** production/reconstruction | SUPPORTED_BOUNDED | Production closure: {W, C, B, description, program} meet C1–C5, and maintained state meets S1–S4. They form one strongly connected network with no external root, within the model and under the substrate convention. Inherited by I5 via G1 byte identity. | "Autopoietic" unqualified, "alive", invention of new content, neural closure. AC105 alone is the wrong study for the production claims; the composition with AC10–AC95 is what is cited. | `CLOSURE_VERDICT_v1.md` §0–1; `I5_…` §0(a); `AC115_ERRATA_v1.md` |
| **O3** cognitive organizational closure | PARTIAL | AC108: maintenance → accurate content (no-write contrast), and content → adaptation (16/16 reversal; survival 12/16 vs 0/16). | The arrows content → *future cognitive machinery* → future content. These are often reproducible by direct control (AC109/AC116), and AC117 repairs an estimate, not machinery. | Synthesis "O3 arrow audit"; ledger O3 |
| **O4** constituted unity | NOT_ESTABLISHED | A material-layer produced, semipermeable perimeter (AC114/A4). I5 (b): six functions compose at mechanism level. | Whole-organism unity (non-spatial informational core). Survival-level composition: G4–G7 retained as failed. Functional cognitive unity. | `I5_…` §0(b–c); `A0_AUTONOMY_VERDICT_v1.md`; `A2_BOUNDARY_VERDICT_v1.md` |

### C-axis

| Layer | Status | Establishes (bounded) | Does NOT establish | Sources |
| --- | --- | --- | --- | --- |
| **C0** self-maintaining organization | SUPPORTED_BOUNDED (organism) | Modeled organizational self-maintenance under explicit substrate. | Consciousness. Neural constitutive self-maintenance does not follow from cue retention. | Ledger C0; `CLOSURE_VERDICT_v1.md` |
| **C1** endogenous regulation | PARTIAL | Internal state affects regulation. | A unique learned allocator. A 3-line threshold rule reached the oracle (1.000 vs 0.895); AC11's state-blind duty cycle won; Phase II verdict D. | Ledger C1; `BRIDGE_PHASE2_VERDICT_v1.md` §0 |
| **C2** representation | PARTIAL | AC107: one-bit cause estimate, 0/32 mistakes. AC108 content interventions. III-B causal read wiring; a probe decodes 72.89% vs a 34.04% baseline. | Competent acquired multi-specialist latent cognition. III-B: 0/1,024 matched-history address switches; S2 always abstained; S3 near chance. Probes are not semantic use. | Ledger C2; `PHASE3B_VERDICT_v1.md`; `PHASE3B_H10_DIAGNOSTICS_v1.md` |
| **C3** integration/availability | PARTIAL | Shared-content coordination: 0.000 vs 0.0140 incoherence against private copies (p=0.00049). | Workspace necessity. A free scalar broadcast (R4) matches at 0 parameters and 0 refreshes, and the candidate is the lowest-accuracy arm (Phase III verdict C). III-B shows no candidate-exclusive integration (verdict B, 1/16 vs 14/16). Scope note: Phase III is "not about whether a learned sufficient statistic could matter where the statistic is not closed-form". | `PHASE3_VERDICT_v1.md` §1, §4; `PHASE3_INDEPENDENT_AUDIT_v1.md`; `PHASE3B_VERDICT_v1.md` |
| **C4** internal evaluation | NOT_ESTABLISHED | AC117 at harness level: CONTROL-yes, PREDICTION-no. C1 disposition: the C0 collapse holds **only** under the ideal-observer assumption, so monitoring is identifiable in principle for the actual damaged estimator. | A dissociable second-order evaluator. Human C4 gate required. | Ledger C4; `C1_RELIABILITY_DISPOSITION_v1.md` l.12; `AC117_RESULTS_v1.md` |
| **C5** temporal self/world | NOT_ESTABLISHED | Elementary internal/world-cause precursors only. | A persistent self/world model governing counterfactuals or commitments. N5 maintenance closure is not C5. Human gate required. | Ledger C5; constitution v3 |
| **C6** theory convergence | NOT_ESTABLISHED | Nothing. | Any convergence result. Human gate required. | Ledger C6 |
| **C7** phenomenal | PHILOSOPHICAL_BOUNDARY | A boundary rule only. | Any empirical phenomenal verdict, ever, by construction. | Ledger C7; constitution v3 |

### Neural existence and learning boundary (A6)
- **Shared R9:** 5159249/29296875 ≤ L ≤ 1031759/4687500, against a joint gate of
  21579431/117187500. **UNRESOLVED**; six slots consumed (`A6_GATE_DECISION_v1.md`).
- **Gate reduction:** joint competence implies every specialist gate. Unrestricted
  eight-symbol R10 (5101889/29296875) passes the full gate (`A6_GATE_REDUCTION_v1.md`).
- **Single-context R9 shortfall:** 87.5% is within-class; held-out non-identifiability is
  at least 8/75 (`R10A_DECISION_v1.md`).
- **Status:** do not train; A6 and A8 are parked.

**The handoff's "claimed frontier" (its §Layers) matches the repo evidence.** I found no
discrepancy in layer statuses.

### The three open forks
1. **A6 is parked.** Its mathematical node stays open. No search extension, gate relaxation
   or training (tree v5).
2. **The two-stream world-admission analysis is awaiting human approval** (kanban #38).
3. **SUB_A0 needs a decision** (`SUB_A0_CAL_RESULTS_v2.md`):
   - option 1: drop the probe;
   - option 2: sign-coded or bistable substrate (the author's recommendation);
   - option 3: park.
   SUB_A's own Phase A narrowing question (`SUB_A_SESSION_REPORT_v1.md`) is also unanswered.

A fourth, unofficial input is SCARCITY_GAP_v1 on the unmerged branch (§4).

---

## 4. Has the two-stream analytic world been executed or modified?

**No.**
- `ACI_NEXT_EXPERIMENT_DECISION_v1.md` has exactly one commit, `a72136c` (2026-10-01), and
  is unchanged since.
- `git grep` across master, PR #2, `elminster/loving-ptolemy-ityj4l` and
  `learned-vs-reactive` finds the design only in:
  - `ACI_NEXT_EXPERIMENT_DECISION_v1.md`, `ACI_MASTER_RESEARCH_TREE_v5.md` and
    `A6_GATE_DECISION_v1.md` (references);
  - the two `.vscode` boards (todo, `execution_authorized: false`);
  - `a6_decision_v1/test_program.py:54`, which asserts the card status is `todo`.
- There is no protocol, manifest, freeze, enumeration script, certificate or result for it
  on any branch. The `1/50` match in `phase3b/freeze.py` is an unrelated III-B gate margin.

**One newer document modifies its interpretation without executing it.**
`SCARCITY_GAP_v1.md` (unmerged branch, §1 table and §7) argues:
- The two-stream world "sits in the sufficiency regime".
- Its strong-reduction signature "is built to succeed". It recommends adding a capacity axis
  below ρ = log K / H(S) = 1.

My own check (algebra only, no enumeration run) supports the second point:
- A distribution over two binary variables has 3 degrees of freedom.
- (pX, pY, cov) is a bijective reparameterization of it:
  p11 = pXpY + cov, p10 = pX − p11, p01 = pY − p11, p00 = 1 − pX − pY + p11.
- The Bayes update of the joint is a function of the joint.
- So signature (iv), "marginals + covariance match the joint filter's forecasts and update
  law", is a **mathematical identity, guaranteed to pass**. It is a correctness check, not
  evidence.

I verified two of SCARCITY_GAP's citations against master:
- `PHASE3_VERDICT_v1.md` §4 says the verdict is "not about … where the statistic is not
  closed-form".
- `C1_RELIABILITY_DISPOSITION_v1.md` l.12 says "C0's collapse is correct only under the
  ideal-observer assumption".

I did not run or replay its certificate (not authorized).

---

## 5. The 2026-10-02 deletion of frozen result files

| Field | Finding |
| --- | --- |
| Commit | `d0ee2bb46e3a6ec3d80be2b9ec6f53d9a1e7a89e` |
| Author / date | **Aidan Ahern** <ahernaidan1@gmail.com>, Fri 2026-10-02 23:38:35 EDT (−0400) |
| Message | "Remove large result files and snapshots from multiple versions" (no body) |
| Change | 78 deletions (status D), no additions or modifications. Exactly 3 files per folder: `rows.jsonl`, `results.json`, `pre_run_snapshot.json`. |
| Folders (26) | `ac17_results_single_v1`, `ac18_results_v1`, `ac32_results_v1`, `ac33_results_v1`, `ac36_results_v1`, `ac43_results_v1`, `ac45_results_v1`, `ac46_results_v1`, `ac50_results_v1`, `ac54_results_v1`, `ac55_results_v1`, `ac57_results_v1`, `ac58_results_v1`, `ac60_results_v1`, `ac67_engineering_v1`, `ac67_results_v1`, `ac68_engineering_v1`, `ac68_results_v1`, `ac71_results_v1`, `ac75_results_v1`, `ac76_engineering_v1`, `ac76_results_v1`, `ac79_deviation_seeds4000_v1`, `ac79_engineering_v1`, `ac79_results_v1`, `ac80_results_v1`. Each folder is now absent from the tree. |
| Size | 2,085,169 bytes in total (about 2.0 MiB). The largest are AC17/AC18 at about 0.5 MB each; most are 5–100 KB. For comparison, commit `b7e7cae` four days later added about 5.6 M lines. "Large" is a weak rationale. |
| Duplicates? | **No.** None of the 78 blobs exists elsewhere in the parent tree. |
| Gitignored? | **No.** `.gitignore` at the parent ignored only venvs, `__pycache__`, `*.pyc` and `bridge/runs/`. The 2026-10-20 cleanup PR's ignore rules don't cover these paths either. |
| Errata or record? | **None.** No errata, README note, board card or evidence-index entry mentions the removal. |
| Dependents broken | `audit_ac*.py`/`replay_ac*.py` for AC17, 18, 32, 33, 36, 43, 45, 46, 50, 54, 55, 57, 58, 60, 67, 68, 71, 75, 76, 79 and 80 read these folders (e.g. `audit_ac67.py:11`, `replay_ac67.py:14`, `ROOT = …/'ac67_results_v1'`). So do the matching runners and tests. About 31 results, protocol and status docs cite them as evidence (e.g. `AC67_RESULTS_v1.md:64`). These are the inherited AC15–AC80 "acquisition/adaptation" and "internal-state milestone" evidence (`EVIDENCE_INDEX_v3.md` Item 3), which `CLOSURE_VERDICT_v1.md` cites by composition. |
| Preservation inventory | **All 78 files are in `a6_decision_v1/baseline_hashes.json`** (7,326 protected files, head `370685b`). I recomputed SHA-256 in Python without running the repo script. At HEAD, 78 protected files are missing and 1 differs (`.gitignore`, from PR #2). Another 4,791 differ only by CRLF/LF checkout (Windows-created inventory). So the A6 `preservation --check` documented in `A6_GATE_DECISION_v1.md` would fail at HEAD. |
| Recoverable? | **Yes, exactly.** The bytes at `d0ee2bb^` match all 78 inventory hashes after LF→CRLF normalization. Nothing is lost from git history. |

**Assessment.** This was not a sanctioned cleanup of duplicates or ignored artifacts. It is
the repo owner's own commit, so it was presumably intentional, perhaps to reduce repo size.
But it violates the program's immutability rules:
- **Constitution v1 §6 (Standing rule III), item 3, "Frozen-version discipline":** "an old freeze, hash, ledger, or
  result is never edited". Deleting the result is the stronger act.
- **Constitution v3:** independent replay is "binding".
- **The A6 preservation inventory**, which this commit silently invalidates.

`CONTRIBUTING.md` ("Do not edit or move [frozen artifacts]") was only written on
2026-10-20, so it did not exist at the time. The commit nonetheless contradicts it now.

**Recommended remedy (needs Aidan's approval; not done):** restore additively with
`git checkout d0ee2bb^ -- <26 dirs>`, or write a versioned errata/provenance note recording
the removal and the recovery commit. If size was the concern, use Git LFS or an archive
manifest with hashes.

---

## Other observations carried from the first briefing (`/workspace/aci_briefing.md` §5)
- **README is stale.** It still says "the current frontier is `E3_DESIGN.md`".
- **`requirements.txt` is incomplete.** It omits `scipy` (used by `a6_decision_v1`) and
  `pytest`, and says torch is "only" for phase3/bridge, but SUB_A0 uses torch too.
- **`docs/REPOSITORY_MAP.md` defines "AC = assignment/check" without support** in any
  research document.
- **Approval was inferred, not given.** The SUB_A0 calibration freeze approval was inferred
  from Aidan replying "Continue" (`SUB_A0_CAL_RESULTS_v1.md`, "Provenance").
- **Governance docs are behind.** Tree, index and boards don't record SUB_A or SUB_A0.
