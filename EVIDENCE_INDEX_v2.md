# Evidence index v2 — reconciled evidence state at HEAD 77ace95 (N0)

2026-09-23. Derived bookkeeping deliverable for the N0 card (t_69bd4615). Supersedes
`EVIDENCE_INDEX_v1.md` only by adding the K-series outcome and the cognition-track
positive; the autonomy material and the negative/falsified ledger are carried forward
unchanged. No frozen artifact is edited, re-run, or re-hashed. Seeds are the replication
unit (N seeds × 2 histories = N independent units). Survival is a bimodality-aware lower
bound (AC68), never a per-seed-family guarantee. "Frozen" = hashed protocol + results dir
under `mkdir(exist_ok=False)` + audit (re-derives gates without simulating) + replay
(sampled exact reruns).

## The reconciled verdict (one paragraph)

At HEAD 77ace95 there are two reference architectures. The **autonomy** architecture is the
AC105 body (`gray_ctl` Gray-coded relinquishment streak + persistent reconstruction trigger +
allowance-42 material budget, `corrupt=True` operating-range grid), on which K3 issued a
bounded **SUPPORTED** production-closure verdict (level (a): components {W, C, B,
description, program} meet C1–C5 and maintained state {pointer, coordination, route memory,
decision state} meets S1–S4, under the substrate convention; J4 spatial unity unresolved).
The **cognition** architecture is AC107/108 (the AC100-derived `corrupt=False` two-cause
world), on which K6/K7 established a maintained one-bit cause-estimate that discriminates
two causes at ceiling accuracy (0/32 mistakes on fresh cohorts) and is causally coupled to
its maintenance in **both directions** by single-flag interventions — the first level-(c)
representation shown causally coupled to level-(a/b) machinery **in this project's lineage**
(not a field-level first; see `N1_CORRECTIONS_v1.md`), not merely co-present. The
survival advantage of the representation is seed-bounded and its ongoing-repair loop is not
exercised (single paid write at cause-onset; the AC13 wall). The reliability tier (K8) is
BLOCKED, not falsified. Three bounded claims are paper-ready (level b; level a with exact
scope; level-c coupling with its survival caveat); one follow-on (three-cause integration)
is gated, not authorized.

---

## Item 1 — Autonomy reference architecture (AC105 body)

**What it is.** The frozen AC105 architecture composes three accepted mechanisms, all
operating `corrupt=True` across a predeclared grid of challenge timings, priorities and
repeated route moves:

| Mechanism | Component | Established by |
| --- | --- | --- |
| `gray_ctl` — Gray-coded relinquishment streak (3-bit reflected Gray, 1-bit transitions), no reserve | decision state (C8) | AC99 (5/5), AC100 (2×2 factorial isolates Gray, not reserve — 6/6) |
| Persistent reconstruction trigger (fire while the decoded program ≠ description-derived target) | program (C9) reconstruction | AC103 (persistent vs current — the persistent trigger is the accepted recovery mechanism) |
| Allowance-42 budget `max(0, material − 42)`, `DECISION_ALLOWANCE = STREAK_N × 7`, applied throughout life with no challenge-time knowledge | decision-spending coordinator | AC104 (6/6, 5700–5707), AC105 (6/6, 5800–5807) |

**Frozen evidence.** AC105 seeds 5800–5807 (untouched), 2 histories, 2 arms
(`persistent` / `persistent_budget`), 5 conditions (`simult`, `simult3`, `corrupt_first`,
`move_first`, `late`), 160 rows = 80 matched comparisons, 16,384 ticks. All six gates pass:
G1 control identity (byte-identical to AC104 at `simult`), G2 candidate reconstructs
`fw→0` 80/80, G3 no-harm survival, G4 no-harm relinquishment, G5 observer-discard per-tick
16/16, G6 completeness + determinism. The rescue (candidate survives where control dies)
is 4/80 matched comparisons = **one fresh seed** (5804, priority `(0,3,2,1)`) × two
shared-challenge schedules (`simult`/`simult3`) × two histories. One `move_first` boundary
(5802) kills both arms via the re-acquisition path (not the budget); a retained diagnostic
reconstruction-level harm (5603 under `late`) trades reconstruction completeness for a
reserve it cannot use. Corrected reporting in `AC105_ERRATA_v1.md`.

**The closure component ledger (charter v2 §7, applied by K3 at db0ef2f = AC105 body).**
Components (produced/replaced, C2): W (`life[:16]`, action 6 birth, autocatalytic),
C (`life[16:20]`, action 7 birth), B (`boundary`, action 8 birth), description
(130-bit, bank-1 slots, succession copy→verify→switch→remove), derived program
(`traces[0,:126]`, reconstruction via generic decode). Maintained state (S1–S4,
internalized not produced): pointer (2-bit), coordination (MODE + W-funded timer + RIP),
route memory, decision state (allocation register + Gray streak). Supplied substrate:
`prog.choose` (interpreter), `advance()` (succession transition logic), decode format,
observation, conservation laws, damage model, world constants.

**Verdict status.** Level (a) production closure **SUPPORTED (bounded)** — "meets the
finite closure criterion within the declared model and operating range, under the accepted
substrate convention" (K3 `CLOSURE_VERDICT_v1.md`). J1 = substrate (resolved); J4 spatial
unity (M&V clause ii) UNRESOLVED and outside the criterion's scope (B retention is
load-bearing per AC10, but substitutable by substrate). Not "autopoietic" unqualified.

---

## Item 2 — Cognition reference architecture (AC107/108)

**What it is.** The AC100-derived, `corrupt=False` two-cause world, carrying a maintained
one-bit cause-estimate `e ∈ {E_world=1, E_machinery=0}` plus an explicit diagnostic
interface.

**Mechanism.** The estimate bit lives in the dead-rule action bit
(`14·dead_rule_index + 10`, acquired value 1 = E_world, the AC12 inverted-semantics
pattern): damaged by the sticky program damage stream, read by majority, written by the
paid W-gated `bel_write`, excluded from `reg_from_active`. The update rule reads the
organism's own `(bound, used_held, productive)` triple and gates every conclusion on its
own memory (K1's confound closed):
`bound & not used_held → E_machinery`; `used_held & not productive → E_world`;
`not bound & productive → E_world`. Consumption: E_world → frozen Gray-streak
relinquishment (STREAK_N=6); E_machinery → withhold relinquishment + proactive renewal.

**Diagnostic interface (K4's identifiability).** `bound` is the organism's own unshimmed
introspection read (`o.memory.read(1) is not None`); `used_held` is the shimmed retrieval
result (`selected is not None`), forwarded to the allocator (an interface change, not a new
sensor). `productive` is the frozen yield. The two causes produce disjoint tuples: E_world
gives F1 (held-entry failure `(1,1,0)`, one-sided); E_machinery gives F2
(resumption-via-bound `(1,·,1)`, two-sided). Separability is a task property demonstrated
by a hold-and-observe harness (K4), not assumed.

**World.** AC100 Gray-streak architecture, corrupt=False, TICKS=16384, DEV=512, PORTS=4
(blind fallback 1/4), mapping over {0,1}; `move` flips channel-1 mapping at t=8192; `cut`
suppresses the channel-1 read for [8192, 8192+96). **Absent from this world:** the AC105
corruption challenge and the allowance-42/persistent-trigger decision-spending refinements
(orthogonal to the coupling question; a corruption at the cut/move tick would be a THIRD
cause).

**Arms.** candidate (maintained estimate); r2 (frozen Gray streak, threshold 6); r4 (raw
per-key counter, HOLD_N=24); r1 (reactive, threshold 1); scramble (read forced E_world,
write intact); AC108 adds no_write (write disabled, read honest) and force_machinery (read
forced E_machinery, write intact).

**Integration decision.** The K6 mechanism runs on the K3-assessed autonomy baseline's
machinery — `ac95.maintain` (succession, reconstruction, description/pointer/ctrl repair)
and the W-gated paid writes are inherited UNCHANGED by `ac107.py`, re-verified by G6
byte-identity (the extension is inert for the frozen arms). This is stated, and its limits
are item 6.

---

## Item 3 — Confirmed on FRESH cohorts

**AC107 (K6, finals 6000–6007, 240 rows, protocol hashed pre-run, audit+replay).** Partial
confirmation; four questions answered separately:

- **Q1 discrimination — CONFIRMED.** `cut` reads E_machinery at window end 16/16; `move`
  reads E_world at first drop 16/16; **0 post-intervention mistakes across 32 individuals**.
  Transfers to the untouched family unchanged.
- **Q3 storage maintenance — CONFIRMED (content sense).** Observer-discard per-tick
  byte-identity 16/16 (value read from vulnerable maintained state, not host state);
  no-cause identity 16/16 (estimate inert absent a cause); vulnerable-storage audit (bit in
  the sticky damage stream, paid W-gated write, excluded from `reg_from_active`).
- **Q2 content causal — NOT transferred.** `scramble` is behaviourally causal (relinquishes
  in `cut` where the candidate holds, seeds 6001/6006), but the survival consequence is
  vacuous on the fresh family (no final seed carries the priority-corner `[3,0,2,1]`; a
  mid-cut relinquishment is recoverable). G2 FAILS (recorded, not moved).
- **Q4 comparative advantage — NOT transferred (seed-bounded).** Move-side candidate
  14/16 vs r4 10/16 (both die on 6002); cut-side no advantage (r2 survives 16/16). G5
  FAILS (recorded).

**AC108 (K7, finals 6100–6107, 288 rows, 7/7 gates, protocol hashed pre-run,
audit+replay).** Both coupling directions confirmed, each by a selective intervention:

- **Direction 1 (maintenance → accuracy/use) — CONFIRMED.** `no_write` reads E_world at
  cut end 16/16 (inaccurate) vs candidate E_machinery 16/16 (accurate); the write is
  actually cut (`bel_writes == 0`, `bel_attempts == 0`); mis-use is behavioural
  (relinquishes a still-valid route on 6100/6101/6104/6105 where the candidate holds).
  Load-bearing for accuracy 16/16 and use (behavioural, 4/8); NOT load-bearing for
  survival in this world.
- **Direction 2 (content → adaptation/production/viability) — CONFIRMED.** `force_machinery`
  reverses the move-side adaptation (holds the stale route 0/16 relinquishments, where the
  candidate relinquishes 16/16) and collapses production/viability 16/16 (all die); the
  candidate re-acquires and survives 12/16. `scramble` is cut-side behavioural (relinquishes
  a valid route on 6101/6103/6104/6105 where the candidate holds). Content is causal for
  adaptation (both directions) and production/viability (move side 16/16).

**Key scoping (carried, not hidden).** Survival is reported NOT gated (bimodality-aware
lower bound); the candidate's own move deaths (6100, 6107) are the re-acquisition boundary
(the AC83/AC74 path), not a coupling failure; the cut's death bite is priority-corner-
specific and no final seed in 6000–6007 or 6100–6107 carries it.

---

## Item 4 — ENGINEERING-only (not frozen claims)

| Item | Evidence class | Notes |
| --- | --- | --- |
| AC106 maintained-belief causal test | Engineering negative (seeds 0-7, no protocol, no freeze) | K1 corrected it: an **implementation defect** (update rule read `productive` and dropped `bound`; r4 had HOLD_N==STREAK_N; scramble was a 3-way confound), NOT a capacity absence. Valid negative preserved: the estimate *as implemented* was not causally load-bearing |
| AC107 mechanism feasibility (K5) | Engineering (seeds 0-7) | Discrimination 16/16 + survival-relevant in both directions; proactive-renewal redundancy measured inert. Unblocked K6 on feasibility only |
| K4 task identifiability | Analysis + diagnostic harness (no study) | Separability of the two causes via `(bound, used_held, productive)` is demonstrated, not a frozen claim |
| K8 reliability monitoring | **BLOCKED, not falsified** | The first-order estimate is ceiling-accurate (0 mistakes) → no error variance for a second-order state to predict. Reopening requires a non-zero non-trivial error rate (3 named routes) |
| Three-cause integration (corruption + move + cut) | Untested | Gated follow-on; only if the survival/composition question is judged load-bearing |
| Re-acquisition boundary (candidate move deaths) | Untested as a mechanism | Operating-range question, not a coupling gap |
| AC105 engineering-screen rescues + 5603 reconstruction harm | Disclosed engineering (not persisted in rows.jsonl) | Seeds 1/6/7/5603 rescues; 5603 `late` reconstruction-level harm (fw 2 vs 0) retained as a finding |

---

## Item 5 — Inherited from earlier architectures (AC10–AC95 ablations/turnover)

The necessity-by-ablation, replacement-verification, and turnover record is carried forward
from earlier frozen studies and **is not re-tested by AC105/AC107/AC108** (K3 §1 states
this explicitly). The accepted capability ledger (unchanged from `EVIDENCE_INDEX_v1.md` §3):

- **Foundational body (AC1–AC10):** AC1 controller pays for its own repair (+ confirmatory
  AC1–AC4, fresh seeds 5100–5507); AC2 produced W catalysts; AC3 produced C converters
  (2/3 rates in confirmatory); AC4 produced B boundary + measured transport; AC4_FOLLOWUP
  integrated repair sustains activity; AC9 controls v3 (developmental allocation + broad
  controls); AC10 every constituent dependency isolated (no-W/no-C/no-B/retention-rescue/
  external-B, 9/9 gates).
- **Acquisition/adaptation (AC15–AC75):** AC15 graded access law; AC18 two-way
  relinquish/restore; AC67 repair load-bearing under sticky damage; AC71 majority-read
  register closes the closure triplet; AC75 erase-on-relinquishment makes the closure
  world-accommodating.
- **Internal-state milestone (AC76–AC89):** AC76 controller turnover from a
  corruption-immune description; AC79 description maintenance; AC80 internalized
  reconstruction recipe; AC81 component replacement (turnover accounting); AC84
  unconditional turnover floor; AC85 stored bank-rule convention; AC86 recipe storage
  succession; AC87/88/89 integrated successor (succession controller state in maintained
  substrate, order-preserving decode, simultaneous + adversarial challenge).
- **Production dependencies (AC91–AC95):** AC91 W production load-bearing for viability +
  maintenance capacity; AC92 functional interruption-and-rescue (W cut mid-reconstruction);
  AC93 coordinator transition write W-gated; AC94 coherent resumable succession; AC95 state
  sufficiency (observer-discard endpoint equivalence).
- **Decision-state economics (AC96–AC105):** AC96 internalized relinquishment streak (state
  sufficiency complete; economic viability flagged); AC97/98 reserve falsified (withholds
  the decision it funds / W-denominated shortfall); AC99 Gray encoding resolves the
  maintenance/adaptation conflict; AC100 factorial isolates Gray not reserve; AC101
  composition (internal-state 8/8, behavioural partial); AC102/103 premature-termination vs
  resource-shortage separation; AC104/105 allowance-42 budget (item 1).

**Negative / falsified ledger (do not inherit as capabilities):** AC11 (state-blind duty
cycle beats adaptive arm), AC13, AC14 (self-reversing damage), AC16/17 (gate-shape), AC97/98
(reserve), AC102/103 (partial: the *distinction* stands, no universal spending policy),
AC106 (engineering negative, superseded in scope by K1–K9).

---

## Item 6 — Direct single-flag interventions vs source-inspected dependencies

The claimed dependencies at 77ace95 fall into two classes by how they are evidenced.

### 6a. Direct single-flag interventions (causal; one flag changed, effect isolated)

| Dependency claimed | Intervention | Result |
| --- | --- | --- |
| Maintenance → representation accuracy/use (direction 1) | `no_write` — disable the estimate's paid W-gated write, read stays honest | Inaccurate 16/16; write actually cut; behavioural mis-use 4/8 |
| Representation content → adaptation/production/viability (direction 2, move) | `force_machinery` — force read = E_machinery, write intact | Adaptation reversed 16/16; production/viability collapse 16/16 |
| Representation content → adaptation (direction 2, cut) | `scramble` — force read = E_world, write intact (read-only control) | Behavioural relinquishment 4/8 where candidate holds |
| State sufficiency (value lives in maintained state, not host) | observer-discard (per-tick byte-identity) | 16/16 (AC107/108); AC95/96 endpoint equivalence 8/8–16/16 |
| Estimate inertness absent a cause | no-cause identity (candidate == r2 state_hash) | 16/16 |

These five are the only coupling/state-sufficiency dependencies established by a **single
flag** at 77ace95. (The autonomy track has its own single-flag ablations — AC10 no-W/C/B,
AC91 W-birth block, AC92 W-cut + machinery-only rescue, AC93 W-gated MODE, AC95-D3 direct W
cut, AC96 single-step damage+repair — but those are **inherited from earlier frozen
architectures**, not re-run at this HEAD.)

### 6b. Source-inspected only (code-traced, NOT causally isolated by a single flag here)

| Dependency claimed | How it is evidenced | The gap |
| --- | --- | --- |
| The estimate bit is *vulnerable and paid-maintained* (in the sticky damage stream, written by paid W-gated `bel_write`, excluded from `reg_from_active`) | Source audit (`ac107.py` §"the estimate bit"; `AC107_RESULTS_v1.md` §3 vulnerable-storage audit; `AC107_ENGINEERING_v1.md` §7 host-field audit) | The **ongoing repair loop is NOT exercised** — maintenance is a single paid write at cause-onset (the AC13 wall: 96-tick window vs 1e-4/replica/tick). "Sustained representation-repair coupling" is NOT demonstrated; N1's point 3 |
| The K6/K7 mechanism "runs on the K3-assessed machinery" (ac95.maintain succession/reconstruction/desc/pointer/ctrl repair + W-gated paid writes inherited unchanged) | Source inheritance + G6 byte-identity (the extension is inert for frozen arms) | Byte-identity confirms the extension didn't *change* the frozen arms; it does NOT re-establish the W-gating/reconstruction causal links, which are inherited from AC91–AC95 |
| The closure-verdict C1–C5 / S1–S4 per-component dependencies | Code-traced matrix (`DEPENDENCY_AUDIT_v2_CORRECTION.md`, `CLOSURE_CRITERION_CONSISTENCY_v1.md` §3), each component's named evidence from AC10–AC95 | These are direct interventions *in their own studies*, but at 77ace95 they are **inherited, not re-tested** by AC105/AC107/AC108 (K3 §1 states this) |
| K4 identifiability (F1/F2 separation) | Diagnostic hold-and-observe harness on frozen modules (source inspection + small simulation) | A task-property demonstration, not a single-flag causal intervention on the organism |

**Bottom line for item 6.** The two coupling directions and the state-sufficiency/no-cause
properties are the only dependencies at this HEAD with clean single-flag causal
interventions (`no_write` / `force_machinery` / `scramble` + observer-discard). The
estimate's *vulnerable storage realization*, its *ongoing repair*, and the *inheritance of
the AC91–AC95 maintenance machinery* are source-inspected (or inherited by byte-identity),
not fresh single-flag causal demonstrations. This is exactly the boundary N1 must correct
and A1 must account for.

---

## The acyclic board graph (kanban dependency DAG, planning phase)

The N0 card is the root of the new planning phase. Edges are parent→child (a child stays
`todo` until all parents complete). S1 is the sole sink. The graph is acyclic (no card
appears as its own ancestor).

Nodes (id, status, priority):
- N0 t_69bd4615 running 90 — Baseline and evidence reconciliation
- N1 t_cb679061 todo 85 — Correct acquisition/coupling/scope claims
- A1 t_293cdb2c todo 84 — Account for the physical realization of operational state
- A2 t_3d75b49d todo 80 — Resolve the boundary criterion as far as the model permits
- C1 t_9e21dcbb todo 79 — Compare against a direct diagnostic controller
- C2 t_a5ef427b todo 78 — Establish a task where history has a testable role
- C3 t_2874c547 todo 76 — Isolate ongoing repair after successful acquisition
- C4 t_d06a5e21 todo 75 — Investigate uncertainty as a separate research question
- I1 t_188163c5 todo 74 — Evaluate composition without conflating it with uncertainty
- P1 t_2aff2675 todo 77 — Draft the evidence-backed paper account
- S1 t_03024c7c todo 70 — Integrate results and choose the next bounded step

Edges (parent → child), from the board's task_links table:
```
N0 → N1 ; N0 → A1
N1 → C1 ; N1 → C4 ; N1 → P1
A1 → A2
C1 → C2 ; C1 → S1
C2 → C3 ; C2 → C4 ; C2 → S1
C3 → I1 ; C3 → S1
C4 → S1
A2 → I1 ; A2 → P1 ; A2 → S1
I1 → S1
P1 → S1
```

Layered view (topological order):
```
          N0
        /     \
      N1       A1
     / | \       \
    C1 C4 P1      A2
    |       \    / | \
    C2       +--+  |  \
   /  \         |  |   \
  C3  C4        |  P1   \
   |             \        \
  I1 <-------------+        \
   |                  I1     |
   +--------------------> S1 <--- (C1, C2, C3, C4, A2, I1, P1 all feed S1)
```

Every path terminates at S1; there is no cycle. N0 completing releases N1 and A1; A1
completing releases A2; N1 completing releases C1, C4 and P1.

Predecessor (completed) K-series DAG, for context — its terminal synthesis K9 is the input
to this planning phase:

```
K0 → {K1, K2}
K1 → K4 → K5 → K6 → {K7, K8, K9}
K2 → K3 ──────────┴────────→ {K7, K9}
K8 → K9 ; K7 → K9 ; K9 (terminal)
```

---

## What this hands to N1 and A1

- **N1 (correct the claims)** gets the exact scope boundaries it must enforce: `no_write`
  cuts acquisition/update, not ongoing repair (item 6b row 1); the diagnostic interface is
  an explicit `bound`/`used_held` split (item 2); the survival reversal in AC108 is 12/16
  (candidate survives 12/16 while force_machinery dies 16/16), distinct from the 16/16
  *adaptation* reversal; partial results (behavioural causality, storage maintenance) must
  be reported independent of the failed survival gates (item 3); ceiling accuracy is a
  property of THIS task, not a universal wall (item 4); three-cause integration is ONE
  continuation, not the only one.
- **A1 (account for physical realization)** gets the realization ledger it must resolve:
  the four maintained-state items {pointer, coordination, route memory, decision state}
  live in `traces[0]`/`traces[1]`/`mem.Memory` (S1), are damage-reachable (S2), paid-
  maintained (S3), correctness-neutral (S4) — but their *realization* is an
  update/repair-in-place process, not a produced component (charter v2 §7b), and whether
  that realization is covered by a produced component, an explicit substrate provision, or
  an unaccounted dependency is exactly the open question (item 1 component ledger + item 6).

---

## Item 7 — S1 reconciliation (terminal; the N/A/C/I/P track closes the two open hands)

This index's "hands to N1 and A1" are now answered, and the reconciled state is recorded in
`S1_SYNTHESIS_v2.md` (the terminal synthesis). In brief, per the eight required items:

- **Production closure (level a):** SUPPORTED, bounded (K3), with A2 re-confirming B on C1–C5 and A1
  accounting the four operational-state items as substrate storage + maintained state (no unaccounted
  dependency).
- **Full autopoiesis criterion (i + ii):** NOT ESTABLISHED — clause (i) supported, clause (ii) spatial
  unity met only at constituent-retention level and limited by supplied space/exchange/non-spatial
  controller; the substitution fact is struck (function-identification, not refutation). Modeling
  limitation, no child experiment.
- **Diagnostic acquisition + behavioural causality:** SUPPORTED (AC107/108; 0/32 mistakes; both
  coupling directions by single-flag intervention).
- **Persistent history:** FALSIFIED in the clean world (C1/AC109, storage inert, 48/48 equivalence);
  SUPPORTED-by-design that a history-load-bearing task exists (C2, occluded-`used_held` gate).
- **Ongoing repair dependence:** FALSIFIED (C3/AC110, frozen 6200–6207; correctness rides reacquisition;
  G4 8/16 recorded).
- **Uncertainty/reliability:** first-order graded posterior SUPPORTED-by-design (C4); reliability
  (second-order) tier UNTESTED, entry condition named (vary `P_YIELD`).
- **Composition with autonomy:** SUPPORTED with a named interference (I1/AC111, frozen 6300–6307;
  direct channels clean; corrupted contact rule re-schedules reacquisition on 6306/6307).
- **Comparative performance/viability:** content load-bearing, survival seed-bounded (adaptation
  reversal 16/16, survival reversal 12/16).

**Next bounded step:** write up the three paper-ready claims (P1 drafted) and authorize exactly one
named continuation — the graded-posterior (first-order uncertainty) organism-scale study, with its
discriminating prediction (calibration + strict regret-dominance over `binary+imm` in the high-q
occluded-gate regime, gated on calibration/utility not survival). The reliability tier is gated after;
the autonomy track is terminal.

## Sources

`K9_SYNTHESIS_v1.md`, `K8_DISPOSITION_v1.md`, `CLOSURE_VERDICT_v1.md` (K3),
`DEFINITIONS_CHARTER_v2.md` (K2), `TASK_IDENTIFIABILITY_v1.md` (K4),
`AC107_RESULTS_v1.md` / `AC107_PROTOCOL_v1.md` / `AC107_ENGINEERING_v1.md`,
`AC108_RESULTS_v1.md` / `AC108_PROTOCOL_v1.md`, `AC105_RESULTS_v1.md` /
`AC105_PROTOCOL_v1.md` / `AC105_ERRATA_v1.md`, `AC106_ERRATA_v1.md` (K1),
`AUTONOMY_RESEARCH_STATUS.md`, `EVIDENCE_INDEX_v1.md`, `ac107.py`, `ac108.py`,
frozen dirs `ac105_results_v1` (160 rows) / `ac107_results_v1` (240 rows) /
`ac108_results_v1` (288 rows). This index is derived and is not hashed into any snapshot.
