# Manuscript roadmap v1 — what the papers claim now, and what closes next

2026-09-26. Deliverable of the N14 card (t_8b4303fa): the manuscript roadmap,
updated for the Phase-II verdict. **Updated 2026-09-27 by G16 (t_a299aaef) for the
Phase-III verdict (OUTCOME C).** It is a **planning document**: it authorizes no
experiment, freezes nothing, and edits no frozen artifact. It states which claims
are paper-ready today, which claims the Phase-II and Phase-III verdicts removed or
weakened, and what each not-yet-run phase would add. This is manuscript development, not
authorization to submit or publish externally.

---

## 0. One-paragraph status

Two papers are in scope and are now clearly separated by their claim ceiling. The
**organism paper** (`P1_MANUSCRIPT_DRAFT_v1.md`) carries three bounded,
already-established claims — level (a) production closure (SUPPORTED, bounded),
level (b) adaptive autonomy (ESTABLISHED), level (c) representational coupling
(SUPPORTED, with the survival caveat) — and is unaffected by either neural verdict.
The **neural line** has now run **two** experiments to verdict. Phase II (the bridge)
returned OUTCOME B + D: its only paper-ready claim is **N1 active paid persistence as a
necessary-condition/substrate fact**, and the two headline ambitions it was built to test
— an explicit maintained self-state, and an endogenous adaptive allocation — are **not
supported** and must be written as negatives. Phase III (the workspace) returned OUTCOME
**C — the sufficient statistic wins**: the shared maintained workspace (learned encoder +
paid π + shared slot) is the worst of six arms on inference, and the analytic
sufficient-statistic broadcast rival matches/beats it for free; the two headline ambitions
it was built to test — a load-bearing shared maintained workspace, and load-bearing modular
specialists — are **not supported** and must be written as negatives, with the one narrow
positive (sharing buys coordination + economy over private copies, for free via broadcast)
carried as a bounded coordination fact. The joint teaching is stated in §2.3. No
consciousness claim enters either paper.

---

## 1. What is paper-ready now (established, with exact evidence)

### 1.1 The organism paper (unchanged by Phase II)

The three bounded claims of `P1_MANUSCRIPT_DRAFT_v1.md` stand, each carrying its
frozen evidence and its attached caveats:

1. **Level (a) production closure** — SUPPORTED within the declared model and
   operating range, under the accepted substrate convention; boundary-mediated
   exchange established at the material layer (AC114/A4), composed with the
   five-mechanism closure at the mechanism level (AC115/I5); survival-level
   composition not confirmed.
2. **Level (b) adaptive autonomy** — ESTABLISHED (AC99–AC105).
3. **Level (c) representational coupling** — a maintained one-bit cause-estimate
   discriminates two causes at ceiling accuracy and is causally coupled to its
   maintenance in both directions, with the survival caveat; its graded/weighted
   generalization is **not** a paper-ready claim (AC113, R1).

### 1.2 The neural-bridge line — exactly one claim, narrow

**N1 — active paid persistence (necessary condition).** Future-task information
depends on a representation whose retention is paid per tick out of a limited
budget, and is unrecoverable without it. Candidate stable slot survival 0.978 vs
no_maintenance / free_memory 0.000; exact sign-flip p = 2/2^12 = 0.00049 (floor);
12/12 seeds; force-hold → probe 1.0, force-drop → chance.

This is the **only** claim the bridge earns, and it must be written with three
bounding clauses, or the paper over-claims:

1. **Necessary-condition, not uniqueness.** State-blind fixed schedules and the
   reward-only arm also hold the cue through paid refresh (N12 finding F2). N1
   establishes that paid maintenance is *required*; it does **not** establish that
   the candidate's *learned allocator* is causal or distinctive.
2. **Substrate + architecture, not learned behaviour.** The free-permanence fact
   rests on the S4 architecture (S_pol reads only (W, x_t), x_t c-independent), a
   structural fact, not something the `free_memory` arm measured (N12 finding F1).
3. **Observed-integrity world only.** The scaffold's integrity `I_t = f(d_t)` is a
   readable age counter, not an inferred latent; the inferred-integrity question is
   a documented STOP (N6/N6b) and is not touched by this claim.

---

## 2. What the Phase-II verdict removed or weakened (must be written as negatives)

OUTCOME B + D (`BRIDGE_PHASE2_VERDICT_v1.md`) removes two headline claims and
weakens a third. These are findings, not omissions; they are as much the paper's
content as the positive claim in §1.2.

1. **"An explicit maintained self-state V is causally load-bearing" — NOT
   SUPPORTED (B).** The strongest same-information rival (P_rb, no V slot) matches
   the candidate (op 0.823 vs 0.895, p = 0.64). V's integrity bit is a learned
   re-encoding of the observable age `d_t`. Write: "explicit maintained V was
   unnecessary in this task," never a relabeling of the rival as part of the
   candidate.
2. **"Endogenous adaptive allocation (N3)" — NOT SUPPORTED (D).** A 3-line
   reactive threshold rule on (s, E, d) attains the oracle (op 1.000) in every
   seed, above the candidate (0.895). The learned allocator is reproduced by a
   hand-coded rule. Write as: "the optimum is a level/threshold, not a learned
   switch" — the neural restatement of organism demotion D5 (AC11).
3. **Weakened:** the candidate's allocation is regime-dependent beyond every
   state-blind schedule in 10/12 seeds (op 0.895 vs 0.500), but **not** strictly
   dominant — 2/12 final seeds collapsed to over-refresh and died (bimodality,
   AC39/AC68). Report as a bimodality-aware result, never as "better in every
   seed."

**Not claimed anywhere:** A (allocation distinctive), C (recurrence defeats paid
persistence), E (N1 is an objective reduction), or any consciousness claim. The
bridge's ceiling is level (b)/(c) representational, bounded to the observed-
integrity world.

### 2.4 What the Phase-III verdict removed (must be written as negatives)

OUTCOME C (`PHASE3_VERDICT_v1.md`) removes two headline claims and carries one bounded
positive. Per-arm probe accuracy over 12 final seeds: candidate 0.9632 (lowest), R1
0.9634, R2 0.9643, R4 0.9645, R5 0.9645, R3 0.9648.

1. **"A learned encoder + paid-maintained shared workspace is necessary for flexible
   cross-module content" — NOT SUPPORTED (C).** The analytic sufficient-statistic
   broadcast (R4) and identical copies (R5) match or beat the candidate on every accuracy
   endpoint at zero parameters, zero refresh, zero incoherence. The workspace machinery is
   a pure cost the broadcast rival does not carry. Write: "the shared maintained workspace
   was scaffolding over a sufficient-statistic broadcast in this task," never a relabeling
   of R4/R5 as part of the candidate.
2. **"Modular specialists add value over a monolithic or broadcast architecture" — NOT
   SUPPORTED (C).** The monolith (R2, one RNN, ~3× params, no W/π/shared state) beats the
   candidate; the three specialists are three fixed functions of one scalar with distinct
   invariance classes — distinctness by fiat. Modularity survives only as an
   interpretability/intervention affordance, not a performance property.
3. **Bounded positive carried forward.** Sharing is load-bearing for coordination (0 vs
   R1's 0.014 incoherence, p = 0.00049) and maintenance economy (1 vs 3 refresh targets),
   and it is free once the content is a broadcast statistic. Write it exactly at that
   width — a coordination/economy fact over private copies — never as a workspace claim.
4. **Mis-framed, not claimed:** the causal interventions (I1/I2/I5) pass by construction
   (fixed functions of a scalar, candidate-only, undefined for R2/R3); they establish
   "specialists are functions of W," not a behavioral contrast a rival fails. Do not
   present them as architectural evidence.

### 2.5 The joint Phase-II + Phase-III teaching (the paper's framing)

Across two neural levels the load-bearing object was the **availability of sufficient
content**, not the machinery around it: Phase II stripped the explicit maintained
self-state; Phase III stripped the shared maintained workspace. Answering the standing
question — expensive persistence / shared representation / explicit workspace / modular
specialists / sufficient-statistic availability / none — the record now supports **only
sufficient-statistic availability as load-bearing**, with paid persistence as a
necessary-condition substrate fact (N1) and sharing as a free broadcast. This is the
program's signature collapse ("paid/learned/maintained X adds nothing over a
sufficient-statistic or reactive rival") at three sites (organism D2/D5/AC109; neural
D9/D10; workspace D11/D12), and it must be written as the paper's through-line, not as
three unrelated negatives. It is bounded to closed-form-statistic tasks; the open forward
question (an *acquired* statistic carrying the sharing properties) is §4.2.

---

## 3. The evidence ledger entry the roadmap points to

The bridge evidence is recorded in `EVIDENCE_INDEX_v3.md` under the new
"Neural bridge (Phase II)" section, and in the architecture matrix
(`ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`) under the new bridge-lineage section. The
roadmap does not duplicate those tables; it states the *claims* they support and
the order in which they enter a manuscript.

---

## 4. What closes next, in order

### 4.1 Done: the revised principles absorbed (G16)

The architectural principles have now absorbed the two Phase-II demotions (D9 "explicit
maintained self-state unnecessary"; D10 "learned adaptive allocation demoted") **and** the
two Phase-III demotions (D11 "shared maintained workspace unnecessary"; D12 "modular
specialists add no value") — see `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` §8. This
documentation step is complete; the principles are the gate that has now passed.

### 4.2 Executed: Phase III (N2) returned OUTCOME C — the forward direction is the acquired statistic

Phase III (N2 — recurrent cross-module availability of a maintained representation) has
**executed** and returned OUTCOME C: the shared maintained workspace is scaffolding over a
sufficient-statistic broadcast, the candidate is the worst of six arms, and the analytic
broadcast rival matches/beats it for free. The claim ceiling Phase III would have earned
("one content value flexibly consumed by two modules — N2 at the stated degree") is **not
earned**; what is earned is the narrower bounded fact in §2.4.3 (sharing buys coordination
+ economy over private copies, for free via broadcast). The next manuscript section is
**not** a re-run of Phase III's closed-form world; it is the **acquired-statistic
question** (§5.4 of `ACI_MASTER_RESEARCH_TREE_v3.md`): whether a sufficient statistic
*learned* from an environment where the statistic is not supplied in closed form carries
the sharing properties. That is a new task design (G17), not a re-tune of the SLW
candidate.

### 4.3 Not in scope now: inferred integrity (STOP)

The bridge's central ambition — a maintained *inferred* integrity estimate doing
causal work — is a documented, unsettled STOP (N6/N6b). Nothing in this roadmap
resurrects it, and nothing here is evidence against it. It would require a new
scaffold where integrity is not a deterministic function of a readable observable.

---

## 5. Claim ceiling (stated once, for both papers)

No autopoiesis claim, no "alive"/"self-sustaining" claim, no subjectivity claim,
and no consciousness claim enters either paper. The strongest wording the organism
paper earns is "meets the ACO property at the stated degree" for levels (a)/(b)/(c);
the strongest the bridge earns is "meets N1 at the stated degree (necessary
condition)"; the strongest the workspace line earns is the bounded coordination fact
(sharing buys coordination + economy over private copies, for free once content is a
broadcast sufficient statistic) — it does **not** earn N2 at any degree, because the
shared-workspace architecture was the scaffolding the verdict stripped. The
level-(d)/(e) boundary is absolute.

---

## Sources

`BRIDGE_PHASE2_VERDICT_v1.md` (N13), `BRIDGE_FINALS_RESULTS_v1.md` (N11),
`BRIDGE_FINALS_AUDIT_v1.md` (N12), `ACI_MASTER_RESEARCH_TREE_v2.md` (N14, this
revision's tree), `P1_MANUSCRIPT_DRAFT_v1.md`, `EVIDENCE_INDEX_v3.md`,
`ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`, `ACI_ARCHITECTURAL_PRINCIPLES_v1.md`.
Frozen results read, never re-run or re-hashed. Derived document; not hashed into
any study's `pre_run_snapshot.json`.

**G16 extension sources:** `PHASE3_VERDICT_v1.md` (G15), `PHASE3_FINALS_SUMMARY_v1.md`
(G13), `PHASE3_INDEPENDENT_AUDIT_v1.md` (G14), `PHASE3_REDUCTION_AUDIT_v1.md` (G9),
`ACI_MASTER_RESEARCH_TREE_v3.md` (G16's tree).
