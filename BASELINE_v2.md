# Baseline v2 — the reconciled two-track state at HEAD `db0ef2f`

2026-09-22. Bookkeeping note, not a scientific claim. Nothing is re-run, re-frozen,
re-hashed, or edited here; this document only names what already exists so that downstream
planning stops silently inheriting claims demonstrated in an earlier architecture, and stops
conflating the autonomy track with the cognition track. Frozen artifacts (runners, protocols,
results dirs, hashes) are untouched. Supersedes `BASELINE_v1.md` (which covered the autonomy
track only, at `8f0218a`); the autonomy material is carried forward unchanged.

## Reference commit and architecture

- **Reference commit:** `db0ef2f` ("AC106 (C2): maintained-belief causal test — NEGATIVE").
  This is `7969b14` (the planning program: baseline, evidence index, charter, roadmap,
  dependency audit v2, autopoiesis assessment, X1 coupling, S1 synthesis) plus one commit,
  `daf421c` (AC105 errata) between them.
- **Two tracks exist and are recorded separately below.** The AUTONOMY track (the AC-line
  body, frozen through AC105) and the COGNITION track (C1→C2→C3→X1, terminating in the AC106
  engineering negative). They share the same organism and the same discipline but answer
  different questions and have different baselines; neither may stand in for the other.

---

## 1. AUTONOMY baseline (frozen through AC105)

**Architecture** (the AC105 body, inherited from AC99–AC104):
1. `gray_ctl` — a Gray-coded relinquishment failure-streak with **no reserve**
   (AC99/AC100: the Gray encoding, not the reserve, carries adaptation).
2. **Persistent reconstruction trigger** — `reg_from_active` fires while the decoded program
   still differs from the description-derived target, the completion test derived from
   maintained state (AC103).
3. **Allowance-42 material budget** — `budget = max(0, spendable_material − 42)`,
   `DECISION_ALLOWANCE = STREAK_N × 7 = 42`, applied throughout life with no challenge-time
   knowledge (AC104; operating range tested AC105).

The internal-state substrate (130-bit description in vulnerable slots + maintained
coordination state, AC85–AC89) is carried into the reference architecture unchanged.
Frozen reference study: **AC105** (seeds 5800–5807, 6/6 gates, corruption @8192 + route
moves under a declared condition grid).

**Verdict by claim level** (charter §2, from `S1_SYNTHESIS_v1.md`):
- **Level (b) adaptive autonomy — ESTABLISHED.** Gray streak + allowance-42 coordinate the
  paid reconstruction write with the paid decision write; the organism acquires and then
  relinquishes route content on its own viability conditions (AC99/AC100/AC104/AC105;
  two-way relinquish/restore AC15/AC18/AC75).
- **Level (a) organizational closure — UNRESOLVED** on one named modeling judgment, **J1**:
  whether `advance()` (succession transition logic) and `prog.choose` (interpreter) are
  acceptable substrate or undeclared coordinators. Established by A2 as not empirically
  settleable (infinite regress), not an empirical gap.
- **Level (c) representation — PARTIAL** (acquired route memory; interoceptive observation
  only; no content-bearing perceptual representation, J5).

**Accepted milestones** and their frozen studies are unchanged and enumerated in
`EVIDENCE_INDEX_v1.md` §2–§3. The dependency ledger (`DEPENDENCY_AUDIT_v2.md`) — components
C1–C9, the supplied-substrate classification, and the J1–J5 gaps — is carried forward
unchanged and is the autonomy-track graph.

---

## 2. COGNITION baseline (terminating in the AC106 engineering negative)

**Track arc:** C1 (task design) → C2 (AC106 implementation/measurement) → C3 (metacognition
gate) → X1 (coupling test). All four are complete; the track terminates in a measured
negative. No cognition study is frozen.

- **C1** — `MAINTAINED_BELIEF_TASK_v1.md`: a two-cause, partially-observed task (E_world =
  channel move / E_machinery = read cut, same immediate failure), with four prespecified
  predictions and six rivals. Design document, not a study.
- **C2** — `ac106.py` / `AC106_ENGINEERING_v1.md`: implements the task as a **one-bit
  maintained cause-estimate** e ∈ {E_world, E_machinery} with five matched rivals plus a
  scramble control. **Engineering result NEGATIVE** (seeds 0–7, 16 individuals): the
  estimate carries no cause information (reads E_machinery in *both* causes — the update
  rule is confounded by blind re-acquisition), its hold is partial and seed-dependent
  (14/16 vs r2's 8/16 in the cut, failing exactly on the fast-streak corner), and its
  proactive renewal (97–171 writes) is redundant with the frozen reactive renewal. **No
  protocol written, no final seeds, no freeze.**
- **C3** — `C3_DISPOSITION_v1.md`: CLOSED, not blocked — the metacognition activation
  condition (a first-order estimate whose accuracy varies) fails, so a reliability estimate
  has nothing to predict or control.
- **X1** — `X1_COUPLING_ASSESSMENT_v1.md`: coupling question answered NEGATIVE on existing
  evidence — maintaining the estimate does not change viability (survival identical to r2
  and scramble), and organizational maintenance sustains no cognitive function (the organism
  relies on the host-side first-order machinery).

**Verdict:** the level-(d) line (maintained belief → metacognition → HOT-2) is **FALSIFIED**
on measured, structural grounds for this candidate mechanism. Level-(e) (phenomenal
consciousness) remains NOT ASSESSABLE. This is a falsification of one specific candidate
under one operational definition — it is **not** a verdict on autopoiesis or consciousness
in general, and it does not touch the level-(b)/(c) autonomy machinery (whose maintenance
*is* load-bearing: AC67/AC71/AC75/AC91/AC92).

---

## 3. The AC106 configuration limitation (must be stated, not inherited past)

**AC106 did not run in AC105's combined-challenge architecture.** `ac106.py` declares its
world as *"the AC100 Gray-streak architecture, corrupt=False, TICKS=16384, DEV=512,
PORTS=4 (blind fallback 1/4), mapping over {0,1}."* Concretely:

- **AC100-derived, not AC105-derived.** AC106 inherits the AC100 single-challenge world
  (route move only). It has **no corruption challenge** (`corrupt=False`), therefore no
  persistent-trigger reconstruction, no allowance-42 spending rule, and no combined
  corruption+move schedule — the three defining features of the AC105 body (§1).
- **Consequence.** AC106 establishes a *task-level engineering negative* for the maintained
  belief under the earlier AC100 configuration. It did **not** establish — and did not test
  — cognitive integration in AC105's combined-challenge architecture. Any statement about
  whether a maintained belief is (or is not) integrated must be scoped to "AC100-derived,
  corrupt=False"; it cannot be quoted as a verdict on the AC105 body.

---

## 4. Corrections: what already exists, what is still required

**Already exist (published, non-frozen correction notes — no frozen artifact edited):**

| Note | What it corrects |
| --- | --- |
| `AC105_ERRATA_v1.md` | 160 arm-runs = **80 matched comparisons**; the 4 rescues = **1 seed × 2 shared-challenge schedules × 2 histories**; "never harms" scoped to survival/relinquishment (5603 reconstruction harm retained); allowance-42 is a spend constraint, not guaranteed funding; 5802 `move_first` is a shared failure, not an isolated causal diagnosis. |
| `AC104_ERRATA_v1.md` | generalization untested; fresh sample had no rescue; allowance is a spend constraint. |
| `AC103_ERRATA_v1.md` | recovery 5/6; defer uses CORRUPT_TICK; bounded conclusion. |
| `AC102_ERRATA_v1.md` | G3/G4 predicate reversed; screened-not-unseen seeds; narrowed headline. |
| `AC100_ERRATA_v1.md` | two successful alternatives; engineering 1/8; seed-7 failure downstream of the drop. |
| `AC79_ERRATA_v1.md` | (earlier) survivor-gated maintenance; reporting corrections. |

Also already correcting AC106 downstream: `X1_COUPLING_ASSESSMENT_v1.md` §4 already notes a
C2 reporting error — "every arm completes" is false (30 of 288 rows die) — and re-derives
arm-independent survival. This is a correction already in hand, not a pending one.

**Still required (open successors — the next cards):**

- **K1 (t_a26a6854) — correct AC106 and downstream interpretations.** Nine named
  overreach points to verify against code and saved artifacts and then publish as scoped
  errata: (1) `HOLD_N == STREAK_N`, so r4 did not implement the advertised longer-threshold
  comparison; (2) the estimator not distinguishing re-acquisition from retained access is an
  implementation defect, not proof of no representation; (3) identical terminal labels ≠
  zero cause information throughout the trajectory (report decision-time discrimination);
  (4) route-holding/relinquishment changes are behavioural effects even without a survival
  improvement; (5) the scramble arm overrides reads AND suppresses writes — not a selective
  expenditure-matched ablation; (6) AC106 is an engineering negative with no frozen
  confirmatory protocol — not a confirmatory rejection; (7) unchanged survival ≠ absent
  maintenance dependence; (8) similarity to an externally supported controller ≠ falsified
  internal integration; (9) a failed cause estimator ≠ falsified metacognition/consciousness
  mechanisms generally, or all cognition-maintenance coupling. Plus numerical and
  survival-reporting inconsistencies, and reopening/superseding
  `C3_DISPOSITION_v1.md`, `X1_COUPLING_ASSESSMENT_v1.md`, `S1_SYNTHESIS_v1.md` where they
  overgeneralized. No positive finding may be manufactured.
- **K2 (t_46494bfe) — resolve closure-criterion consistency.** The update/repair/produce
  distinction; whether pointer/timer/streak writes satisfy the production criterion C2
  (verify, not assert); the derived network criterion; boundary production vs boundary
  function; which evidence composes in the AC105 architecture vs earlier versions.
- **K3, K4** — downstream of K2 and K1 respectively.

---

## 5. Concise evidence index (two tracks)

**Autonomy track — accepted capabilities** (full list in `EVIDENCE_INDEX_v1.md`; abbreviated
here to the reference-architecture line and the milestone anchors):

| Capability / milestone | Frozen study | Status |
| --- | --- | --- |
| Internal-state milestone (description maintained, reconstructed, transferred) | AC85/86/87/88/89 | ACCEPTED |
| Gray encoding carries adaptation (not the reserve) | AC99, AC100 | ACCEPTED |
| Persistent reconstruction trigger | AC103 | ACCEPTED |
| Internal spending rule (allowance-42) | AC104, AC105 | ACCEPTED (one fresh rescue + no-harm, not universal) |
| Production-dependencies / machinery load-bearing (W/C/B) | AC91, AC92 | ACCEPTED |
| Composition (internal-state) | AC101 | PARTIAL (behavioural arm fails 3/4 unseen) |
| Controller turnover, description maintenance, succession | AC76, AC79–AC96 | ACCEPTED |

**Cognition track — outcomes** (none frozen):

| Item | Artifact | Status |
| --- | --- | --- |
| Maintained-belief task design | `MAINTAINED_BELIEF_TASK_v1.md` (C1) | Design only |
| Maintained cause-estimate causal test | `ac106.py`, `AC106_ENGINEERING_v1.md` (C2) | **NEGATIVE** (engineering; no freeze) |
| Metacognition gate | `C3_DISPOSITION_v1.md` (C3) | CLOSED (premise absent) |
| Cognition↔self-maintenance coupling | `X1_COUPLING_ASSESSMENT_v1.md` (X1) | **NEGATIVE** |

**Falsified / do-not-inherit records** (both tracks): AC11, AC13, AC14, AC16, AC17, AC97,
AC98 (autonomy, gate-shape/economics); AC106 (cognition, mechanism). Full list in
`EVIDENCE_INDEX_v1.md` §4, plus the AC106 entry added below.

---

## 6. Updated dependency graph (two tracks)

The **autonomy-track graph is unchanged** and lives in `DEPENDENCY_AUDIT_v2.md` §4 — the
C1–C9 component network (W/C/B/description/pointer/coordination/route-memory/
decision-memory/derived-program) with the supplied-substrate line (J1). The cognition track
adds one candidate edge that does **not** sit on that network:

```
AUTONOMY track (AC105 body, corrupt=True @8192):           COGNITION track (AC106, corrupt=False):
  C1..C9 component network (DEPENDENCY_AUDIT_v2 §4)          one-bit cause-estimate e ∈ {E_world, E_machinery}
  ├─ gray_ctl (C8 streak) ── relinquish/restore               ├─ stored in a dead-rule action bit (bank 0)
  ├─ persistent trigger + rebuild (C9 ← C4)                   ├─ damaged by the sticky program stream,
  └─ allowance-42 budget rule                                  │  repaired by paid bank-0 majority-restore
                                                              ├─ update: productive-after-failure → E_machinery
                                                              │          relinquishment            → E_world
                                                              ├─ consume: E_world → relinquish
                                                              │          E_machinery → hold + proactive renew
                                                              └─ VERDICT: carries no cause information
                                                                 (reads E_machinery in both causes);
                                                                 redundant with r2's Gray streak + reactive
                                                                 renewal → NEGATIVE (no freeze)
```

The cognition edge is **not a component of the AC105 architecture** (it was built on the
AC100-derived, corrupt=False world — §3). Its negative therefore does not add or remove
anything from the C1–C9 ledger; it is a separate-track result about a candidate
level-(d) mechanism.

---

## Stale directives carried forward from v1 (unchanged)

`RESUME_RESEARCH.md` (AC10-era) and `DEPENDENCY_AUDIT_v1.md` (pre-AC79) are stale;
`CLOSURE_BOUNDARY_v1.md` superseded by v2; the consciousness gate stays archived. See
`BASELINE_v1.md` §"Stale directives" and §"Unresolved claims". The v1 disposition holds:
no frozen study is restarted, re-hashed, or re-run because it is named here; this baseline
and the evidence index are derived documents and are **not** hashed into any study's
`pre_run_snapshot.json`.
