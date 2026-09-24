# S1 synthesis v2 — the reconciled account across both tracks, and the next bounded step

2026-09-23. Terminal synthesis of the N/A/C/I/P planning phase (S1 card, t_03024c7c). It
reconciles the two reference architectures — the **autonomy** track (AC105 body, K3/A2) and the
**cognition** track (AC107/108 binary cause-estimate, K6/K7 → C1–C4/I1) — into one account, reports
the eight required items separately with supported / falsified / untested / unsupported labels, and
chooses the next bounded step. Derived document: it runs nothing, re-hashes nothing, freezes nothing.
It supersedes `S1_SYNTHESIS_v1.md` (the assessment-track synthesis) as the current terminal account;
that file is preserved unchanged as the record. No frozen artifact is edited.

The predecessor deliverables it reads: A2 (`A2_BOUNDARY_VERDICT_v1.md`), C1 (`AC109_ENGINEERING_v1.md`),
C2 (`C2_TASK_DESIGN_v1.md`), C3 (`AC110_RESULTS_v1.md`), C4 (`C4_TASK_DESIGN_v1.md`),
I1 (`AC111_RESULTS_v1.md`), P1 (`P1_MANUSCRIPT_DRAFT_v1.md`), plus N1 (`N1_CORRECTIONS_v1.md`),
A1 (`A1_REALIZATION_LEDGER_v1.md`), the K-series terminal (`K9_SYNTHESIS_v1.md`), the criterion
(`DEFINITIONS_CHARTER_v2.md`, `CLOSURE_VERDICT_v1.md`), and the evidence index (`EVIDENCE_INDEX_v2.md`).

---

## Verdict (one paragraph)

Two tracks, one reconciled account. The **autonomy** track is **stable within the current model** (its two verdicts do not change for any
experiment inside the model — moving them requires a re-architecture, not a run): production closure
(Maturana & Varela clause i) is SUPPORTED within the declared model and operating range under the
accepted substrate convention, and the full two-clause autopoiesis criterion is NOT ESTABLISHED for a
reason that is a **modeling limitation, not an empirical gap**. The
**cognition** track is **characterized, not exhausted**: a maintained one-bit cause-estimate is
acquired from the organism's own observations, discriminates two causes at ceiling accuracy, and is
causally coupled to its maintenance (the paid acquisition/update write) in both directions — but its
*persistence* is inert where the current observation is decisive in the clean task (C1), its *ongoing
repair* is not load-bearing for correctness/use in the decision window (correctness rides reacquisition,
C3; repair *is* load-bearing for post-window storage, AC110 G4), and its *first-order uncertainty*
generalization is discriminating by design but untested organism-scale (C4). The next bounded step is
therefore **write up the three paper-ready claims (P1 drafted them) and authorize one named continuation**
(among several open continuations on record, §"The next bounded step"): the graded-posterior
(first-order uncertainty) organism-scale study, with its discriminating prediction stated. The
reliability (second-order) tier is the named next-after, gated on that result. Neither a breakthrough
nor exhaustion is claimed.

---

## The eight items, reported separately

### 1. Production closure (level a) — SUPPORTED, bounded

Components {W, C, B, description, derived program} meet C1–C5 (charter v2: C5/C6/C7/C8 are
maintained state S1–S4, not produced components) and form one strongly-connected
production-dependency network with no external root (K3). A2 re-confirmed the boundary component B on
C1–C5 (produced, turns over ~10×, W-anchored, on the W→B→W cycle). A1's realization ledger accounts
for the four operational-state items (pointer, coordination, route memory, decision state) as
**explicit substrate provision for their storage medium + maintained state (S1–S4) for their value** —
no unaccounted dependency, no produced-component gap. This is the charter's own ceiling for level (a):
"meets the finite closure criterion within the declared model and operating range, under the accepted
substrate convention (J1 = substrate)." Not "autopoietic" unqualified; not "alive."

### 2. The full adopted autopoiesis criterion (M&V clauses i + ii) — NOT ESTABLISHED (clause i supported; clause ii modeling-limited)

The adopted criterion is Maturana & Varela's two-clause definition, operationalized via Montevil &
Mossio closure of constraints. **Clause (i), production closure, is SUPPORTED (bounded)** (item 1).
**Clause (ii), spatial unity, is NOT ESTABLISHED** — it is met only at the constituent-retention level
(the organism produces a finite-lived perimeter that retains W/C inside a bounded interior), and is
limited by three modeling declarations, none of them an empirical gap: (a) the space/geometry is
supplied; (b) the exchange interface is supplied and not boundary-mediated (the boundary is a pure
retention wall, not a semipermeable membrane); (c) the controller is non-spatial (program/description/
memory/pointer/decision state are fixed arrays never passed to transport). A2's correction: the earlier
record cited "retention is substitutable by substrate" as the reason clause (ii) is unresolved — that
is a category error (a rescue control that substitutes boundary supply *identifies* the function; it
does not refute it), and it is struck from the verdict. The complete two-clause criterion is **not met
and not presented as completion**. Because the residual is a modeling limitation, **no child experiment
was created** — the one discriminating question (does the boundary mediate exchange) requires changing
the supplied physics.

### 3. Diagnostic-state acquisition and behavioural causality — SUPPORTED

The one-bit cause-estimate is **acquired** from the organism's own observations (the update rule reads
the `(bound, used_held, productive)` triple and gates every conclusion on the organism's own memory —
no externally supplied diagnosis) and held in vulnerable, paid-maintained state. Its content is
**behaviourally causal** by single-flag intervention: `force_machinery` reverses the move-side
adaptation 16/16 (holds the stale route where the candidate relinquishes 16/16) and collapses
production/viability 16/16; `scramble` and `no_write` cause mis-relinquishment of a still-valid route
on 4/8 seeds where the candidate holds. Discrimination is ceiling-accurate (0/32 mistakes on fresh
cohorts, AC107). This is the strongest positive of the cognition track. **Caveat (not hidden):** the
survival advantage is seed-bounded and the cut-side bite is priority-corner-specific — behavioural
causality and storage maintenance are established independent of the failed survival gates (N1 point 5).

### 4. Contribution of persistent history — FALSIFIED in the clean world; SUPPORTED-by-design in the gated world

Split, and the split is the point. **(a) In the AC107/108 two-cause world, persistent history
contributes nothing:** C1 (`AC109_ENGINEERING_v1.md`) measured a direct-diagnostic rival that reads the
same triple transiently and matches the stored estimate on **48/48 behavioural endpoints** (survival,
relinquishments, routes, drop/reacquire timing, streak), while the stored estimate costs *more* (a
7-replica write plus 72–141 redundant proactive renewals). The discriminator is a pure function of the
current observation, so there is nothing for a stored bit to remember — "storage adds benefit" is
falsified; the estimate's *content* (as a selector) is what is load-bearing. **(b) A task where
history IS load-bearing exists:** C2 showed, by design and before any run, that one declared interface
change — occluding the `used_held` observation on a Bernoulli(q) fraction of contacts — makes the two
causes produce an **identical current observation** (`bound=1, used_held=occluded, productive=0`) while
their histories differ, so a maintained accumulator of the last open-gate conclusion is load-bearing
where the transient discriminator is wrong for one cause. Identifiability is demonstrated
(`_c2_identifiability.py`), not assumed.

### 5. Ongoing representation-repair dependence — not load-bearing in the decision window; load-bearing for post-window storage (G4)

C3 (`AC110_RESULTS_v1.md`, frozen finals 6200–6207) cut the estimate's **only** repair path
(`no_repair` excludes the estimate bit from action 2's bank-0 majority-restore, reacquisition intact)
and found correctness/use **unchanged** (G1 32/32 clean control, G2 accuracy 16/16, G3 use 16/16,
G5 viability 48/48). Correctness rides **reacquisition** (`bel_write` at open contacts), not repair;
the repair path is **unreachable in the decision window under the frozen ambient 1e-4 damage** — a
single bit contributes at most 3 minority replicas and can never trigger the whole-bank obs-bit-2
trigger on its own (which needs ≥4 over 126 bits), and ambient program damage accumulates too slowly
within 96 ticks (action 2 fires 0 times in the window). This is conditional, not absolute: damage
*elsewhere* in the program at an elevated rate would fire action 2, which also restores the estimate
bit (it is part of bank 0) — exactly what the post-window drift measures. The repair cut's only effect
is that seed-dependent, decision-irrelevant post-window **storage** drift (G4 recorded 8/16, the
Binomial(7,~0.55) coin flip, not moved): repair *is* load-bearing for post-window storage protection
(maintained holds the estimate at 0 in 16/16; no_repair drifts to majority-1 in 8/16), but not for
correctness/use in the window. This confirms N1 point 3: the maintenance that *is* load-bearing is the
paid **acquisition/update** write (one atomic flip at cause-onset), not an ongoing repair loop.
"Sustained representation-repair coupling" is **not** established.

### 6. Uncertainty / reliability mechanisms — first-order SUPPORTED-by-design; reliability UNTESTED

**First-order uncertainty is SUPPORTED (design + decision-theoretic probe, no organism-scale run).**
C4 showed a graded Bayesian posterior over the cause is **calibrated** (binned confidence tracks the
empirical error rate: conf 0.7–0.8 → 0.748 correct, 0.9–1.0 → 1.000 correct) and **strictly dominates**
every ordinary heuristic (raw counter, binary estimate, binary+imm — the strongest, not a strawman) on
the defer-vs-act tradeoff, with the dominance growing in the incomplete-evidence regime (min-mean
regret q=0.7: 0.884 vs 0.995; q=0.9: 1.359 vs 1.744). The mechanism is likelihood-ratio weighting:
decisive observations act immediately, weak occluded-unproductive evidence accumulates slowly
(LR = log(4/3) ≈ 0.288), which no uniform counter can express. **The reliability (second-order) tier
is UNTESTED** — its entry condition is named (C4 §11): make the evidence channel's diagnostic value
`P_YIELD` vary across distinguishable conditions and ask whether an *estimated* `P_YIELD` restores the
discriminating weighting a *frozen* `P_YIELD` supplies. K8's "reliability blocked" is thereby narrowed:
the block was a property of the perfect-identifiability task (N1 point 6), and C4 is the first place
the error variance actually exists.

### 7. Composition with the autonomy architecture — direct channels clean; full composition retains two failed gates (named interference)

I1 (`AC111_RESULTS_v1.md`, frozen finals 6300–6307, 144 rows) composed the cognitive mechanism with
AC105's reconstruction + spending. The two **direct channels are clean**: reconstruction never
overwrites the estimate bit (the `bel_off` exclusion from `reg_from_active` is load-bearing and now
verified under a *live* reconstruction), and the allowance-42 budget never starves reacquisition (it
defers only `reg_from_active`; `bel_write` is W-gated). This is a property of the spending *policy* —
the allowance reserves reconstruction's own spend, and `bel_write` is W-gated not allowance-gated; it
does not mean the decision write and reconstruction do not compete for the shared material/energy/W
pools (the policy resolves that competition, it does not remove it — AC104 rule 2). G2
reconstruction-completes 48/48, G4 move discrimination 16/16, G6 no-harm survival 48/48 — these
establish that the two *direct* channels compose. The **full composition is not established**: two
prespecified gates fail and are retained (G3 cut-holds 12/16, G5 `bel_writes==7` 12/16), as a named
**seed-dependent behavioural interference**, not a storage/spending interaction: corruption flips the
contact rule (mask 1→126), changing *when* the organism contacts and therefore *when* `bel_write`
fires. On 6306 the cut never bites (estimate stays E_world, consequence-free, route held); on 6307 a
spurious relinquishment at t=8198 is recovered by t=8203 (re-binds, estimate corrected, route held).
Both modes are survival-neutral, absent from engineering seeds (AC39 unfavourable), and recorded as
gate failures (G3 12/16, G5 12/16), not moved.

### 8. Comparative performance and viability — partial: content load-bearing, survival seed-bounded

**Comparative.** The estimate's content is ceiling-accurate (0/32 mistakes) and behaviourally causal
(item 3), but its rivals are genuinely competitive: the direct diagnostic matches it behaviourally
(C1), the raw counter `r4` separates "any history" from "attributed history" (its 6/16 move survival
vs the candidate's 12/16 shows the attribution carries a partial survival edge but not a categorical
one), and the graded posterior dominates all of them decision-theoretically (C4). **Viability.** The
survival advantage is **seed-bounded and does not transfer**: AC107 Q4 (cut-side vacuous — r2 survives
16/16; move-side candidate 14/16 vs r4 10/16) and AC108 (adaptation reversal 16/16, survival reversal
**12/16** — candidate survives 12/16 where force_machinery dies 16/16, dying on 6100/6107). The
candidate's own move deaths are the **re-acquisition boundary** (AC83/AC74 starved re-bind), not a
coupling failure. Viability is a bimodality-aware lower bound throughout (AC68); no survival claim is
made for the representation.

---

## Reconciled evidence state (one table)

| Item | Verdict | Named evidence |
| --- | --- | --- |
| Production closure (level a) | SUPPORTED, bounded | K3 + A2 (B re-confirmed C1–C5); A1 ledger |
| Full autopoiesis criterion (i + ii) | NOT ESTABLISHED (i supported; ii modeling-limited) | A2 |
| Diagnostic acquisition + behavioural causality | SUPPORTED | AC107/108 (0/32 mistakes; both directions) |
| Persistent history | FALSIFIED (clean world) / SUPPORTED-by-design (gated world) | AC109 / C2 |
| Ongoing representation-repair dependence | not load-bearing in the decision window; load-bearing for post-window storage (G4) | AC110 |
| First-order uncertainty | SUPPORTED-by-design | C4 |
| Reliability (second-order) | UNTESTED | C4 §11; K8 (blocked→narrowed) |
| Composition with autonomy architecture | direct channels clean; full composition not established (G3/G5 12/16 retained) | AC111 |
| Comparative performance / viability | Partial (content load-bearing; survival seed-bounded) | AC107/108/109 |

**Unsupported (the record does not earn these, and no downstream doc may inherit them):** unqualified
"autopoietic"/"alive"/"self-sustaining"; full two-clause autopoiesis; any survival-advantage claim for
the cause-estimate; any reliability/meta-monitoring claim; "first demonstrated" beyond this project's
lineage (N1 point 8); "sustained representation-repair coupling" (N1 point 3, C3).

---

## The next bounded step (chosen, with warranting evidence)

**Decision: write up (three paper-ready claims, P1 already drafted), and authorize one named
continuation (among several open continuations on record) — the graded-posterior (first-order
uncertainty) organism-scale study. Do not re-open the autonomy track; do not jump straight to the
reliability tier.**

**Why the autonomy track is stable within the current model.** Production closure is SUPPORTED
bounded, and the full autopoiesis criterion is NOT ESTABLISHED for a modeling limitation (supplied
space/exchange/non-spatial controller — three concrete limits, not "supplied space" alone). A2
established that the one discriminating question (does the boundary mediate exchange) requires
changing the supplied physics — a re-architecture, not a run. No experiment moves either verdict;
the correct action is to write the bounded claim with its exact scope (P1 §2–§4). This is a bounded
disposition, not a claim that the research is exhausted: the cognition track has several open
continuations (below and on record).

**The named changed mechanism (the authorized successor).** Replace the binary cause-estimate
`e ∈ {E_world, E_machinery}` with a **graded log-odds posterior** `L = log P(move | history)` held in
the same vulnerable, paid-maintained state (the AC12/AC96 dead-rule free-bit pattern extended to a
low-bit-width log-odds register, majority-read, W-gated write, excluded from `reg_from_active`),
updated per contact by the C4 likelihood structure and consumed by a threshold relinquish/hold
decision.

**The discriminating prediction (the gate, prespecified).** In the C2 occluded-gate world at high q
(q = 0.7–0.9, the regime C4 showed discriminates), the graded posterior is (G1) **calibrated** — binned
confidence tracks the empirical error rate across the population of decisions — and (G2) **strictly
dominates the sharpest heuristic** (the `binary+imm` rival: AC107 binary estimate + immediate
relinquish-on-open-held, minimized over its own threshold) on expected regret at equal action speed.
Gated on calibration + decision utility, explicitly **not** survival. If the graded posterior matches
or is beaten by `binary+imm` organism-scale, the hypothesis is **falsified** and recorded, not moved.

**Warrant.** C4 demonstrated the dominance at the decision-theoretic level (probe, monotone in q,
already ~0.13 regret at q=0.7). AC107/108/110/111 established that the binary estimate's *content* is
load-bearing while its *storage is inert in the clean task and its repair is not load-bearing in the
decision window* (C1/C3) — so the remaining increment on this line is
content *granularity* (bit → graded), not storage or repair. This is
one continuation that carries a named mechanism change and a discriminating prediction; it continues
this line rather than re-measuring a known wall.

**Falsification risk, stated honestly (this is what makes the gate discriminating).** AC110's result —
correctness rides reacquisition (`bel_write` at open contacts), and at occluded contacts the binary
estimate's stored last-open conclusion is already correct — raises a real doubt that the graded
posterior's advantage (weighting weak occluded evidence) manifests organism-scale. That risk is the
point: the gate is a genuine falsifiable prediction, not a guaranteed positive, and a falsification
would be a recorded outcome, not a project failure.

**Named, not authorized now.** (1) The **reliability tier** (second-order estimated `P_YIELD`) — gated
on the graded-posterior result; its entry condition (make `P_YIELD` vary across distinguishable
conditions) is a further task re-design on record (C4 §11). (2) The **I1 named interference** (the
corrupted contact rule re-scheduling reacquisition) — a bounded robustness question about whether the
estimate's decision should tolerate a re-scheduled reacquisition, subordinate to the graded-posterior
step and explicitly *not* a new storage or spending design.

**Neither a breakthrough nor exhaustion.** The graded-posterior study is a bounded falsifiable test of
one named mechanism change; its falsification is a recorded outcome. The autonomy track's stable-
within-the-current-model state is a bounded SUPPORT plus a modeling-limited NOT-ESTABLISHED — it is
not a claim that the research goal is exhausted, and it is not a promise that the cognition line
reaches any level beyond level (c).

---

## Sources

`A2_BOUNDARY_VERDICT_v1.md`, `AC109_ENGINEERING_v1.md`, `C2_TASK_DESIGN_v1.md`, `AC110_RESULTS_v1.md`,
`C4_TASK_DESIGN_v1.md`, `AC111_RESULTS_v1.md`, `P1_MANUSCRIPT_DRAFT_v1.md`, `N1_CORRECTIONS_v1.md`,
`A1_REALIZATION_LEDGER_v1.md`, `K9_SYNTHESIS_v1.md`, `CLOSURE_VERDICT_v1.md`,
`DEFINITIONS_CHARTER_v2.md`, `EVIDENCE_INDEX_v2.md`, `AUTONOMY_RESEARCH_STATUS.md`,
`CONSCIOUSNESS_ROADMAP_v1.md`, `AC107_RESULTS_v1.md`, `AC108_RESULTS_v1.md`,
`P3_CORRECTIONS_v1.md`. This document is derived
and is not hashed into any study's `pre_run_snapshot.json`.
