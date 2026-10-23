# ACI program briefing: "Toward an Artificial Organism"

Prepared 2026-10-20 (America/New_York) from `/workspace/repo` at HEAD `32cfbe6`
(merge of PR #2, the Copilot repository-cleanup PR, 2026-10-20 13:39 EDT). Read-only:
nothing in the repo was modified. (The clone was shallow, so I ran `git fetch --unshallow`
to get the 209-commit history. That changes only `.git` metadata, not tracked files.)
Every claim below cites the file it comes from.

---

## 1. Core thesis and governing rules

### Thesis
- Original goal: build "a bounded artificial individual whose activity maintains the
  organization that makes that activity possible, and whose development creates particular
  dependencies and priorities during its lifetime". Its causal chain is: experience ->
  acquired organization -> dependence -> learned allocation -> continued functioning
  (`PROJECT_UNDERSTANDING_2026-09-14.md` §1; `NEW_AGENT_GUIDE.md` §1).
- The program keeps three questions apart: functional motivation, organismal autonomy and
  subjectivity. Functional success does not establish experience (`NEW_AGENT_GUIDE.md` §2;
  `PROJECT_UNDERSTANDING_2026-09-14.md` §1).
- In the current ACI framing (`ACI_RESEARCH_CONSTITUTION_v3.md`), two axes are investigated
  separately:
  - **O-axis** (organization): supplied organization, internal maintenance,
    production/reconstruction closure, cognitive organizational closure, constituted unity.
  - **C-axis** (cognition): self-maintaining organization, regulation, representation,
    integration, internal evaluation, temporal self/world organization, theory convergence,
    and a separate phenomenal/philosophical boundary (C7).
  - The O/C intersection is the hypothesis that cognitive processes may help maintain and
    reorganize their own enabling organization. "Every arrow needs a causal test." Ordinary
    sufficient statistics plus control and memory remain the principal alternative.
- ACO v1 (`ACI_TARGET_CONSTRUCT_v1.md`) is a falsifiable working target, not doctrine.
  Changes need a human-approved successor, and old results must not be retrofitted
  (constitution v3).
- The README says the repo is "a scaffolded research benchmark, not an artificial living
  or conscious system" (`README.md`).

### What the constitution (v3) requires and forbids
- **No consciousness score.** Autopoiesis, intelligence, representation, metacognition,
  a workspace, a self-model, or their conjunction does not establish phenomenal
  consciousness. Layer numbers are dependencies, not a meter. C7 is philosophical: never
  "manufacture a final empirical criterion" or equate C0–C6 success with phenomenal
  consciousness. "No authorization licenses an unsupported empirical consciousness claim."
- **Four questions per node:** Q-EXIST, Q-LEARN, Q-CAUSE, Q-NECESSITY/VALUE. Causal role,
  property-relative necessity and engineering advantage are kept separate. A lesion shows
  use, not necessity.
- **Strongest-rival reduction.** A principle gets credit only if it survives the strongest
  plausible reduction. The rival must be matched on information, experience, substrate,
  vulnerabilities and resources. No protected copy, oracle or supplied answer may enter an
  endogenous claim.
- **Thirteen admission questions (Q1–Q13).** Every future card must answer all of them:
  "No answer, no active experiment." Cards are classed as analytic, engineering,
  confirmatory or synthesis. Engineering work cannot be promoted to confirmatory evidence.
  Analytic construction proves existence, not acquisition.
- **Evidence statuses:** SUPPLIED, SUPPORTED_BOUNDED, PARTIAL, REDUCED, NOT_ESTABLISHED,
  UNRESOLVED, PHILOSOPHICAL_BOUNDARY. Seed-level replication, prospective gates,
  independent replay, frozen final protocols and strong rivals remain binding. Costs are
  reported separately, and unmeasured quantities stay labeled unmeasured.
- **Substrate discipline.** Fixed primitive substrate is allowed if explicit. A contested
  mechanism must not be redeclared as substrate after it fails.
- **Human authorization required for:** fundamentally new architecture families,
  scale-ups, organism re-entry, first C4/C5/C6 studies, ACO-definition changes, gate
  relaxation, and phenomenal/philosophical inference.
- **A6 rules:** PASS needs actual legal finite weights, rigorous margins and graph replay.
  FAIL needs full-family impossibility. Otherwise the result is UNRESOLVED. "Neither solver
  luck nor timeout is certification." No neural training is authorized by the A6 effort.
- **Current blanket status:** "no neural training is authorized" (`README.md`;
  `ACI_MASTER_RESEARCH_TREE_v5.md` "Live-work policy"). "No organism restart, new
  architecture construction or consciousness claim is authorized" (`README.md`).
- **After each major cycle**, record the surviving explanation, surprises, use versus
  necessity, all reductions and nulls, and whether another run would change an
  architectural decision. Keep a small inactive theory-only queue, not a build backlog
  (constitution v3; queue in `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json`).

---

## 2. Experiment lineage (question -> outcome)

### Organism era
- **E0 pilot** (`pilot.py`, `results/`). Six evolved recurrent controllers in an
  energy/maintenance world, asking whether resource-dependent control shows organismal
  maintenance. A handwritten reflex also reached the 600-tick ceiling, so the world was
  too easy. Kept as a negative control (`PROJECT_UNDERSTANDING_2026-09-14.md` §3).
- **E1a** (`E1_PROTOCOL.md`, `e1_results/RESULTS.md`). Can an instrumental maintenance
  priority be acquired? The neural Q controller's precursor use went 0% -> 26.7% after
  withdrawal, and recall recovered to 99.8%. **Ordinary tabular Q learning reproduced the
  pattern.** The priority is real but explained by ordinary learning. E1a is the
  ordinary-learning baseline (`README.md`; `PROJECT_UNDERSTANDING_2026-09-14.md` §3).
- **E2** (`E2_PROTOCOL.md`, `e2_results/RESULTS.md`). One 12-neuron maintained recurrent
  network with local biomass growth. History effects on preference and dependence passed.
  Activity-guided growth was worse than a fixed structural target (−16.4 pts). Maintaining
  conductance is not maintaining acquired information, because host-held weights were
  re-exposed (`README.md`; `PROJECT_UNDERSTANDING…` §3).
- **E3** (`E3_DESIGN.md`, contracts v0.1–v0.11, `E3_INTEGRATION_DECISION_v0_11.md`).
  Maintaining finite damageable acquired information without a protected copy. The main
  experiment was ruled **NO-GO** before running: about 1.64 pts of adaptive headroom
  against a 5-pt gate, and a 33 < 36 budget refutation. The obsolescence side branch
  (OB1/OB2) is toy scaffolding (`PROJECT_UNDERSTANDING…` §4–5; `E3_REVISED_HYPOTHESIS_v1.md`).
- **AC series, AC1–AC117** (`AC<n>_*`). This is the organism autonomy and cognition track.
  Summary from `EVIDENCE_INDEX_v3.md` Item 3 and `ACI_MISSION_AUDIT_v1.md`:
  - **AC1–AC10, foundational body.** The controller pays for its own repair, produces W/C/B
    components and transport, and passes constituent ablations (AC10, 9/9).
  - **AC15–AC75, acquisition/adaptation.** Graded access law; relinquish/restore (AC18);
    majority-read register (AC71); erase-on-relinquishment (AC75). Negatives: AC11
    (state-blind duty cycle beats the adaptive arm), AC13/14, AC16/17.
  - **AC76–AC95, internal state/turnover/production.** Controller turnover, reconstruction
    recipe, succession, W production load-bearing (AC91/92).
  - **AC96–AC105, adaptive autonomy ESTABLISHED.** Gray-coded streak, allowance-42.
    Negatives: AC97/98 and AC102/103.
  - **AC107/AC108, representational coupling.** A one-bit cause estimate scored 0/32
    mistakes (AC107). Causal coupling ran both ways in AC108 (7/7 gates).
  - **AC109–AC117.** Storage inert (AC109). Graded estimate equals an integer counter
    (R2). Two-counter shows no advantage (AC113, corrected by R1). AC114/115 cover
    boundary exchange and composition: supported at mechanism level, not at survival
    level (AC115 errata). AC116 shows no significant storage advantage (errata). AC117's
    monitor is CONTROL-yes, PREDICTION-no.
- **Organism verdicts.** Production closure is SUPPORTED, bounded (`CLOSURE_VERDICT_v1.md`,
  K3). The integrated verdict (`I5_…`) supports clause (i) by composition. Clause (ii)
  spatial unity is limited by the non-spatial core (`A0_AUTONOMY_VERDICT_v1.md`). The
  mission audit concluded "more organism work? NO" and the organism line was stopped
  (`ACI_MISSION_AUDIT_v1.md` §4; `ACI_ORGANISM_EXIT_CRITERIA_v1.md` per commit fcd35d2).
- **Organism-era A-series** (separate from A6 and SUB_A0):
  - A1: realization ledger and exchange spec.
  - A2: boundary verdict, `A2_BOUNDARY_VERDICT_v1.md`.
  - A3: AC114 SR-2 confirmation.
  - A4: exchange verdict, `A4_EXCHANGE_VERDICT_v1.md`. Clause (i) supported and extended.
  - A0: corrected autonomy verdict plus a finite spatial-successor spec (S1, design-only),
    `A0_AUTONOMY_VERDICT_v1.md`.

### Neural (ACI) era
- **Q0–Q11.** Mission audit, target construct, principles, neuralization map, minimal
  architecture, bridge protocols and constitution v1 (git log, 2026-09-25;
  `ACI_MISSION_AUDIT_v1.md`).
- **Phase II neural bridge** (N-series; `BRIDGE_PHASE2_VERDICT_v1.md`). Is an explicit
  maintained integrity self-state V load-bearing? **Verdict B+D:**
  - A same-information policy matches it (p = 0.64), so explicit V is unnecessary.
  - A 3-line threshold rule beats the learned allocation.
  - The only positive, N1 paid persistence, is a substrate fact.
- **Phase III** (G-series; `PHASE3_VERDICT_v1.md`). Is a learned, paid Shared Latent
  Workspace needed? **Verdict C:** a sufficient-statistic broadcast reproduces it at zero
  parameters. Sharing matters only against private copies (0 vs 0.014 incoherence).
- **Phase III-B** (`ACI_PHASE3B_PROTOCOL_v1.md`, `PHASE3B_VERDICT_v1.md`). Does a
  competitive candidate-exclusive workspace beat the best of six rivals? **Verdict B,
  bounded negative:** 1/16 seeds passed against 14 required. Unrestricted eight-symbol R9
  won on mean loss.
- **R10** (`PHASE3B_R10_CERTIFICATION_v1.md`). Exact optimal eight-symbol coding has joint
  loss `5101889/29296875` ≈ 0.1741, against learned R9 at 0.3338. Most of the gap is
  non-capacity.
- **R10A / R9 class** (`R10A_DECISION_v1.md`, `R9_FUNCTION_CLASS_v1.md`). The context-3
  R9-class optimum is 0.1761, with a finite witness. Excess splits into 11.4% capacity,
  1.09% class restriction and 87.5% within-class shortfall. That last share is not a clean
  optimizer-failure attribution (`ACI_RESEARCH_SYNTHESIS_v1.md`).
- **Shared4 Stage A** (`SHARED4_STAGE_A_STATUS_v1.md`). For one shared R9 across four
  contexts, the bracket is 0.17610 ≤ L ≤ 0.22011 and the gate is 0.18414. UNRESOLVED.
- **A6 bounded existence effort** (`A6_GATE_DECISION_v1.md`, `a6_decision_v1/`).
  **UNRESOLVED and closed.** Six MILP/LP slots produced no witness and no impossibility
  certificate. A resource erratum is preserved.
- **A6 gate reduction** (`A6_GATE_REDUCTION_v1.md`). Exact results:
  - The full R9 gate is equivalent to the joint threshold alone.
  - The S3 floor is 182/625 in either orientation.
  - Unrestricted eight-symbol capacity suffices for the full gate.
  - Deployed R9 existence remains open.
- **Synthesis, governance and decision package** (2026-10-01): `ACI_RESEARCH_SYNTHESIS_v1.md`,
  constitution v3, tree v5, evidence index v5, `ACI_PRIOR_ART_AND_REDUCTION_v1.md`,
  `ACI_NEXT_EXPERIMENT_DECISION_v1.md`.

### Post-decision-package work (newest commits; not reflected in README, tree or board)
- **SUB_A** (2026-10-01; `SUB_A_ORIENTATION_v1.md`, `SUB_A_ANALYTIC_CHECK_v1.md`,
  `SUB_A_SESSION_REPORT_v1.md`). L0/L1 substrate: can live-trace consolidation repair beat
  matched simpler maintenance? **ADMISSION_STOP.** By induction, every-tick self-repair
  equals an external every-tick schedule and ordinary consensus code. A host-supplied
  median fails the machinery-vulnerability requirement. Human decision requested: narrow
  Phase A, or redesign the repair mechanism.
- **SUB_A0 design** (2026-10-01/02; `SUB_A0_DESIGN_v1.md`, `SUB_A0_DESIGN_HANDOFF_v1.md`,
  `SUB_A0_SUBSTRATE_BOUNDARY_v1.md`, `SUB_A0_ALLOCATION_REGISTRATION_v1.json`). Under damage,
  does a task-trained repairer allocate writes to its own vulnerable repair machinery
  without being rewarded for it? Endpoint: A > 0.10 and D > 0.10 in ≥ 23/32 seeds.
- **SUB_A0 engineering** (`SUB_A0_ENGINEERING_REVIEW_v1.md`, errata v1/v2). Reclassified
  **INVALID: failed positive control.**
  - No-write kept 1.000 accuracy, so the regime applied no maintenance pressure.
  - The probe was ceiling-limited by construction.
  - The IMMORTAL arm was identical to SHAM.
  - The EXTERNAL arm used unmatched write physics.
  - D = 0.00099 is uninterpretable.
- **SUB_A0 calibration v1** (2026-10-05; `SUB_A0_CAL_RESULTS_v1.md`).
  - Stage 1 PASSED: λ = (2, 1, 1), H = 2048, NO_MAINT 0.668, EXT_BISTABLE 1.000.
  - Stage 2 STOPPED as `PROBE_UNIDENTIFIABLE`. The lesion was too shallow, so drift
    reversed it.
- **SUB_A0 probe v2** (`SUB_A0_CAL_PROBE_v2.md`, `SUB_A0_CAL_RESULTS_v2.md`). STOPPED as
  `NO_ADMISSIBLE_DEPTH`. Nearest miss: k = −6, W = 256, NO_MAINT 0.104 against a 0.10 bound.
  Holdout untouched.
- **SUB_A0 R-repairability check** (`SUB_A0_R_REPAIRABILITY_CHECK_v1.md`). Analytic result:
  real-valued weight magnitude cannot be identified from live state under common-mode
  shrinkage. A re-test is predicted to end NEGATIVE for substrate reasons. "QUALIFIED PASS"
  for a re-test only with that prediction pre-stated.

---

## 3. Current open questions and the pending human decisions

### 3a. The formal "next human decision package" (`ACI_NEXT_EXPERIMENT_DECISION_v1.md`)
It is DESIGN ONLY and authorizes nothing. Its decision logic depends on the certified A6
outcome:

| A6 outcome | Next human decision |
| --- | --- |
| PASS | Consider a prospective all-context Q-LEARN protocol. Freeze everything before any fit. |
| FAIL | Inspect the minimal obstruction and propose a minimally changed structural kind. Re-establish Q-EXIST first. |
| **UNRESOLVED (actual outcome)** | Leave R9 optimization. Choose an identifiable first-order world/state question whose interpretation does not depend on the R9 decision. |

**The decision it asks Aidan to make:** whether to approve its recommended next node, an
**analytic world-admission discriminator**.
- **Question:** does a two-stream temporal world require keeping joint first-order
  predictive information beyond a factorized estimate, and is a small ordinary joint
  statistic enough?
- **World:** hidden binary (X, Y) with a common flip C~Bern(1/5), private flips 1/50 and
  1/40, and 8 alternating BSC(1/5) observations. All 256 histories are enumerated with
  exact rational filtering.
- **Rivals:** full joint Bayes (oracle); factorized marginals; marginals plus one
  covariance; current-observation-only; direct-history table.
- **Pre-frozen signatures:**
  - history excess > 0;
  - XOR Brier excess ≥ 1/1000;
  - zero-covariance substitution shifts the XOR forecast ≥ 1/20 on ≥ 1/4 of probability
    mass while X/Y forecasts stay unchanged;
  - strong reduction: marginals plus covariance match the joint filter. This counts as
    success, not a defect.
- **Budget:** one solver-free enumeration plus one independent replay. No sweep, no
  learner, no gradient fitting.

**The three routes it ranks** (readiness, not consciousness potential):
1. Predictive-state / ordinary estimator: **recommended first discriminator** after
   UNRESOLVED.
2. Energy / recurrent constraint restoration: held as an alternative; needs a human gate.
3. Locally reconstructed process/graph: held until the O3 arrow is identifiable; needs a
   human gate.

Even if the world is admitted, any neural execution needs a separate approved protocol.
The board card `aci-world-admission-human-gate` (`.vscode/aci-research-cards-v1.json`) has
`requires_human_approval: true` and `execution_authorized: false`. I found no protocol or
results file for this node, so it appears **not yet approved or executed**.

### 3b. Other pending decisions on the newest work
- **SUB_A** (`SUB_A_SESSION_REPORT_v1.md`): either narrow Phase A to "can ordinary redundant
  information sustain acquired function through internally executed vulnerable repair"
  (no superiority claim), or propose a mechanism whose performing circuit is vulnerable
  and that an ordinary code or schedule cannot reproduce.
- **SUB_A0 calibration** (`SUB_A0_CAL_RESULTS_v2.md`, "Decision needed"):
  - **Option 1, weakened §8.5:** drop the capacity probe and judge the cascade by
    R-interception harm. Run the stage-3 holdout for the regime only, then propose a
    re-test with the NEGATIVE prediction pre-stated.
  - **Option 2, substrate revision (recommended by the doc):** sign-coded or bistable
    performing weights with physics-set magnitude, declared before results, plus
    control-arm recalibration. Needs explicit approval and has not been started.
  - **Option 3, park:** record pressure plus repairability, an unidentifiable probe, and
    R unrepairable in principle.
  - None of the options licenses candidate training. A re-test follows the go/no-go table
    in `SUB_A0_RETEST_PROPOSAL_v1.md` (rows 0–6).

### Underlying open scientific questions
- **Shared R9 existence (A6):** is there a legal shared R9 with joint loss ≤ 21579431/117187500?
  The question is parked (`A6_GATE_DECISION_v1.md`).
- **O3 arrows "content -> future cognitive machinery" and "future machinery -> future
  content":** not established (synthesis, O3 arrow audit).
- **C4/C5/C6:** unadmitted. **C7** is a philosophical boundary (`ACI_MASTER_RESEARCH_TREE_v5.md`).

---

## 4. Naming conventions and workflow

### File prefixes (`docs/REPOSITORY_MAP.md`, plus what I observed)
- Entry points: `README.md`, `ACI_*`, `EVIDENCE_INDEX_v*`, `NEW_AGENT_GUIDE.md`.
- `E1_*`/`e1/`, `E2_*`/`e2/`, `E3_*`/`e3/`: organism-era E experiments. E3 contracts are
  versioned v0_1–v0_11.
- `AC<n>_*.md`: numbered experiments. Suffixes include `_ENGINEERING`, `_PROTOCOL`,
  `_RESULTS`, `_ERRATA`, `_DESIGN`, `_FINDING`, plus `_D1/_D2/_D3` diagnostic sub-studies.
- `ac<n>.py`: runners. `audit_*`, `replay_*`, `verify_*`, `diagnose_*`, `explore_*`, `test_*`
  are scripts and tests.
- `*_results_v*/`, `*_engineering_v*/`: frozen outputs (`rows.jsonl`, `results.json`,
  `pre_run_snapshot.json`).
- Card-letter series from git log and docs:
  - Q: ACI planning
  - N: Phase II bridge
  - G: Phase III
  - K: closure
  - M: monitor/errata
  - P, I, C, W, S: phases, integration, reliability, manuscript, synthesis
  - R1/R2: corrections
  - R9/R10/R10A: neural rival classes and certificates
- "A" is overloaded:
  - organism-era `A0_AUTONOMY…`, `A1_…`, `A2_…`, `A4_…`;
  - neural `A6_*`, plus "A8" referenced in `A6_GATE_DECISION_v1.md`;
  - `SUB_A*`. The `SUB_A0_` prefix was chosen deliberately to avoid colliding with
    `A0_AUTONOMY_*` (`SUB_A0_CAL_ORIENTATION_v1.md`).
- Versioning: every successor is a new `_vN` file. Old versions stay (e.g. constitution
  v1–v3, tree v1–v5, index v1–v5).

### Protocol -> errata -> results workflow (as practiced; e.g. AC115, SUB_A0)
1. **Design / engineering** (`*_ENGINEERING_v1.md`, engineering seeds disjoint from finals).
   This is never a freeze or a confirmatory claim (`AC115_ENGINEERING_v1.md`).
2. **Protocol** (`*_PROTOCOL_v1.md`): frozen gates, hashed into `pre_run_snapshot.json` or a
   `*_FREEZE_*.json` **before** final seeds run (`AC115_PROTOCOL_v1.md`;
   `SUB_A0_CAL_FREEZE_v1.json`).
3. **Results** (`*_RESULTS_v1.md` plus a results directory created with
   `mkdir(exist_ok=False)`). Gates are not moved after viewing outcomes. Then an `audit_*.py`
   re-derives the gates and `replay_*.py` reruns sampled seeds exactly
   (`ACI_MISSION_AUDIT_v1.md` reading discipline).
4. **Errata** (`*_ERRATA_vN.md`): additive corrections. Frozen source, rows and hashes are
   never edited (`AC115_ERRATA_v1.md`, `SUB_A0_ENGINEERING_ERRATA_v2.md`; `CONTRIBUTING.md`).
5. **Verdict / synthesis / evidence-index** successor files reconcile the record.

Rules from `CONTRIBUTING.md`: don't edit or move frozen artifacts; run from the repo root
because imports are flat; run the relevant `test_*` before submitting; don't start
experiments the constitution doesn't authorize; keep cleanup separate from research.

---

## 5. Gaps, inconsistencies and stale docs I noticed

1. **README is internally inconsistent.** The top correctly points to constitution v3,
   tree v5, A6 UNRESOLVED and the decision package. Lower down it still says "The current
   frontier is `E3_DESIGN.md`", and the heading says "v0.3" (`README.md`).
2. **The governance docs don't mention the newest work.** README, tree v5, evidence index
   v5 and the board (`.vscode/aci-research-cards-v1.json`, 6 cards ending at
   `aci-world-admission-human-gate`) were all written 2026-10-01 (commit a72136c). None
   mention SUB_A or SUB_A0 (commits 415e3b1 → b7e7cae, 2026-10-01 to 10-06). No evidence
   index v6 or tree v6 records SUB_A0 as a line.
3. **Unclear priority between two tracks.** The world-admission discriminator (the formally
   recommended next node) appears never to have been approved or run. Instead the
   SUB_A/SUB_A0 maintenance line went ahead. No document I found reconciles the two.
4. **Authorization tension.** Tree v5/README say "no neural training is currently
   authorized". SUB_A0 calibration fit task tables with PyTorch. The doc flags this itself
   and argues it is control-arm-only (`SUB_A0_CAL_ORIENTATION_v1.md`, "Discrepancies").
   The calibration freeze approval was **inferred from "Continue"**, and the protocol
   header still says DRAFT (`SUB_A0_CAL_RESULTS_v1.md`, "Provenance"). Worth confirming
   with Aidan.
5. **Probe-v1 protocol §9** was flagged by its own author as overreaching
   (`SUB_A0_CAL_RESULTS_v1.md`).
6. **`docs/REPOSITORY_MAP.md` gloss "AC = assignment/check" is unsupported.** None of the
   docs I read define "AC". The map was added by the 2026-10-20 cleanup PR. It also lumps
   R1/R2 corrections with R9/R10A under `R*`, and doesn't list N/G/K/M/P/I/C/Q/S/W/SUB_A*
   prefixes.
7. **`requirements.txt` is incomplete.**
   - It omits `scipy` (imported by `a6_decision_v1/`) and `pytest` (used by the documented
     `python -m pytest` commands).
   - It says torch is "only" for phase3*/bridge, but `sub_a0_v1/` and `sub_a0_cal_v1/v2`
     import torch too.
   - Versions are unpinned.
8. **Windows-specific commands.** A6/SUB_A docs give PowerShell commands with `\` paths
   (`A6_GATE_DECISION_v1.md`, `SUB_A_SESSION_REPORT_v1.md`). SUB_A0 errata v1 documents a
   CRLF hash-semantics defect.
9. **Frozen result directories were deleted.** Commit d0ee2bb (2026-10-02, "Remove large
   result files…") deleted 78 files from frozen dirs (e.g. `ac17_results_single_v1/`,
   `ac67_results_v1/`, `ac76_results_v1/`, `ac79_results_v1/`, `ac80_results_v1/`). This
   conflicts with `CONTRIBUTING.md` ("do not edit or move"). Audits and replays that
   reference those dirs probably can't run from HEAD. I have not verified this.
10. **Committed noise.** `__pycache__/` (5 tracked files) despite `.gitignore`. The repo
    also includes `.copilot-tracking/`, `.claude/`, `.agents/` and `.mcp.json`.
11. **Stale guides.** `NEW_AGENT_GUIDE.md` (v1.0, 2026-09-09) is E3-era; the README says
    so. `RESUME_RESEARCH.md` and `AUTONOMY_RESEARCH_STATUS.md` describe older "current"
    states (AC20–AC28; K-series, 2026-09-23/24). Read them as history only.
12. **Shallow history at clone time.** The local clone showed only one commit until
    unshallowed, so ordering by git date needs the full history.
