# ACI master research tree v1 — the seven-phase program from organizational foundations to an integrated candidate

2026-09-25. Deliverable for the Q10 card (t_d84e4bb5): *what is the next-stage
kanban hierarchy for the full ACI program?* Category F — **research planning; do
not execute.**

This is a **planning document**. It runs nothing, trains nothing, freezes nothing,
and edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is
not hashed into any study's `pre_run_snapshot.json`. It organizes the whole ACI
program into seven phases and, for each phase, fixes the seven fields the card
requires: core hypothesis, decisive experiment, principal rival explanation,
required predecessor, falsification condition, approximate compute requirements,
and what success does NOT imply.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary
(`DEFINITIONS_CHARTER_v1.md` §2) is absolute: no phase in this tree is, or is meant
as, a path to a consciousness claim. The strongest wording any realized phase earns
is "meets ACO property N_k (or candidate indicator X) at the stated degree," and the
strongest the terminal candidate earns is "meets the ACO definition (N1–N5, at the
stated degree)." (2) Seeds are the replication unit (N seeds × 2 histories = N
independent units); survival/viability is a bimodality-aware lower bound (AC68),
never a per-seed-family guarantee. (3) Every positive claim is credited only if the
rival that omits it provably fails (P6), gates are prespecified and never moved
after a result (AC16), and composition is licensed by byte-identity (`state_hash`),
never prose (AC114/115). (4) The program's collapse record
(`ACI_MISSION_AUDIT_v1.md` §2.6) is the standing falsification set: a phase whose
mechanism reduces to a simpler policy has *failed that phase*, regardless of how
elaborate the implementation looks. (5) Phases are ordered by dependency, not by
ambition; Phase I is already complete, and this tree records that fact rather than
re-litigating it.

---

## 0. The one-paragraph answer

The ACI program is **seven phases, arranged as a single dependency chain from the
already-completed organism foundations to one integrated candidate**. Phase I
(organizational foundations) is the organism program, complete and exited — its
transferable content is the extracted principles P1–P7 and demotions D1–D8. Phase II
(neural self-maintenance) is the first neural phase; its decisive experiment is the
frozen bridge protocol `ACI_BRIDGE_PROTOCOL_v2.md` (T_bridge), testing N1 and N3.
Phase III (recurrent global integration) tests N2 — one content flexibly consumed by
≥2 objective-distinct specialists — via benchmark task T3. Phase IV (self-model and
metacognition) tests N4 — a dissociable second-order verdict, the meta-d′ ≠ d′
signature — via task T6. Phase V (temporal self / autobiographical continuity) tests
O1 — a maintained self-state distinct from the world state, carried across episodes —
via tasks T8 and T9. Phase VI (theory discrimination) runs the four camp-split
contrasts D1–D4 of `ACI_THEORY_INDICATOR_MATRIX_v1.md`, isolating HOT, GWT, PP/SMT
and AE respectively, with IIT recorded as not-yet-testable. Phase VII (integrated ACI
candidate) assembles **only the mechanisms that survived falsification** into one
architecture realizing N1–N5 (plus any O-property that earned its place) and tests
the conjunction under simultaneous intervention — the central ACI hypothesis. Each
phase is a *gate*: it fails fast to a named rival, hands its survivors downstream,
and never licenses a claim crossing the level-(d)/(e) boundary.

---

## 1. How to read this tree

### 1.1 The seven fields

Every phase answers the card's seven fields. The fields mean, once and for all:

- **Core hypothesis.** The one bounded, falsifiable claim the phase exists to test,
  stated in the ACO property vocabulary (N1–N5, O1–O4) fixed by
  `ACI_TARGET_CONSTRUCT_v1.md`. A phase has exactly one; anything else it measures is
  reported, not claimed.
- **Decisive experiment.** The single experiment whose outcome settles the phase —
  either the frozen bridge protocol, one benchmark task from
  `ACI_PHASE2_BENCHMARKS_v1.md`, one of Q5's D1–D4 contrasts, or the terminal
  conjunction test. It is stated with its arm set and its rival.
- **Principal rival explanation.** The strongest simpler mechanism that would produce
  the same observable without the phase's capability. It is always the candidate's
  own mechanism with the contested piece removed (AC109 rule 1), and its parameter
  family is swept alongside the learner's (AC11/AC116 rule 2). A phase is credited
  only if this rival provably fails.
- **Required predecessor.** The prior phase(s) whose outcome the phase depends on.
  This is the tree's edge set.
- **Falsification condition.** The concrete signature that would show the phase's
  hypothesis false — drawn from the named failure tables (the bridge's F1–F7, the
  benchmark's per-task falsification, the construct's F1–F5).
- **Approximate compute requirements.** An order-of-magnitude planning estimate,
  **unmeasured** (flagged as such). The organism line is trivial on this host; the
  neural phases are toy-scale (thousands of parameters, single GPU), dominated by
  seed-count × horizon × arms, not by model size.
- **What success does NOT imply.** The claim ceiling, stated negatively. This is the
  field that keeps the program honest; it is as load-bearing as the hypothesis.

### 1.2 The dependency DAG

```
Phase I ──▶ Phase II ──▶ Phase III ──▶ Phase IV ──▶ Phase V ──▶ Phase VII
             (bridge)      (N2)          (N4)          (O1)         (integration)
                                  │
                                  └──────────▶ Phase VI (theory discrimination,
                                               draws on the working core of II–V)
                                  Phase VI ──▶ Phase VII (only surviving mechanisms)
```

The chain is strict on II → III → IV → V: each later phase needs a working maintained
representation (W) and its bookkeeping, which the prior phase establishes. Phase VI is
parallel to III–V in its *subject* (it tests theory-specific loadings on the neutral
core) but is scheduled after the core is built and before integration, because its
outcomes decide which optional mechanisms (O2, O3, O4) may enter Phase VII. Phase VII
is the terminal fan-in: it admits only mechanisms that survived II–VI.

### 1.3 What is fixed and not re-derived here

This tree **does not** re-derive: the ACO properties N1–N5 and optional O1–O4
(`ACI_TARGET_CONSTRUCT_v1.md`); the principles P1–P7 and demotions D1–D8
(`ACI_ARCHITECTURAL_PRINCIPLES_v1.md`); the minimal architecture W/V/E/A/π/H/Θ_slow
(`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md`); the nine benchmark tasks T1–T9
(`ACI_PHASE2_BENCHMARKS_v1.md`); the four theory contrasts D1–D4
(`ACI_THEORY_INDICATOR_MATRIX_v1.md`); the bridge protocol v2
(`ACI_BRIDGE_PROTOCOL_v2.md`); the organism exit decision
(`ACI_ORGANISM_EXIT_CRITERIA_v1.md`). It reads their vocabulary and fixes only the
**phase decomposition** — which experiment goes in which phase, in what order, with
what rival, and what a pass may claim.

---

## 2. Phase-at-a-glance

| Phase | Content | ACO property | Decisive experiment | Status at HEAD |
| --- | --- | --- | --- | --- |
| I — organizational foundations | organism program (AC1–AC117 + E/A/C/I/P/M/K/S) | levels (a)/(b)/(c) | the frozen AC line (run) | **complete; exited** (Q7) |
| II — neural self-maintenance | paid persistence + endogenous allocation | N1, N3 | T_bridge (`ACI_BRIDGE_PROTOCOL_v2.md`) | **designed; frozen protocol** (Q9) |
| III — recurrent global integration | workspace, specialist coordination | N2 | T3 cross-module availability | designed (Q4/Q6) |
| IV — self-model and metacognition | second-order evaluability | N4 (target) | T6 self-evaluation | designed (Q4/Q6) |
| V — temporal self / continuity | cross-episode carry, adaptation | O1 | T8 + T9 | designed (Q4/Q6) |
| VI — theory discrimination | the four camp-splits | D1–D4 (O2/O3/O4 loadings) | Q5 D1–D4 | designed (Q5) |
| VII — integrated ACI candidate | N1–N5 + survived O's, composed | the N1–N5 conjunction | the conjunction under simultaneous intervention | not started |

---

## 3. PHASE I — Organizational foundations (the organism program)

**Status: complete and exited.** This phase is the already-run organism line. It is
recorded here as the tree's root — the source of the principles the later phases
inherit — not as open work.

- **Core hypothesis.** (Retrospectively stated.) A bounded artificial individual can
  maintain the organization that enables its own activity, and acquire maintenance
  priorities through that dependence — i.e. levels (a) production closure, (b)
  adaptive autonomy, and (c) representational coupling can each be realized in a
  concrete, falsifiable substrate.
- **Decisive experiment.** The frozen AC line: AC1–AC117 plus the E/A/C/I/P/M/K/S
  tracks. The load-bearing results are three, each bounded: production closure over
  {W, C, B, description, program} SUPPORTED within the declared model (AC105, K3);
  adaptive autonomy ESTABLISHED (AC99–AC105, internalized Gray-coded decision state
  + reserve + allowance); representational coupling SUPPORTED — a maintained one-bit
  cause-estimate discriminates two causes at ceiling accuracy and is coupled to its
  maintenance machinery in both directions (AC107/108), with the survival caveat.
- **Principal rival explanation.** The collapse record (`ACI_MISSION_AUDIT_v1.md`
  §2.6) is the set of rivals that each candidate *lost to or collapsed into*: the
  self-repair loop → a watchdog timer (AC67/71); the graded posterior → an integer
  counter (C4/R2); the weighted two-counter → no advantage over one (AC113); the
  maintained counter → weakly dominant only at the resolution floor (AC116); the
  "monitor" → a directional-repair controller, control-yes/prediction-no (AC117);
  the adaptive allocation arm → beaten by a state-blind fixed duty cycle (AC11); the
  self-directed learner → blocked by a locked, path-dependent fixed point (AC78).
- **Required predecessor.** None. This is the foundation.
- **Falsification condition.** Already recorded, per study: each F above is a frozen
  falsification pinned in a protocol, errata, or test suite. The whole-phase
  falsification was the failure of any candidate to exceed its state-blind/rival
  baseline — which is what happened repeatedly, and is exactly why the phase is
  characterized as *bounded* rather than as autopoiesis.
- **Approximate compute requirements.** None further. The AC line runs at ~0.17 s
  per AC9 condition (a full 64-condition study ≈ 11 s) on this host; runtime was
  never a constraint. The sole remaining paper-only item (the S1 spatial
  informational-core successor) is a small extension of the existing NumPy
  simulation, and is classified PAPER-ONLY, not a neuralization prerequisite (Q7).
- **What success does NOT imply.** Autopoiesis unqualified; that the organism is
  "alive"; that any of its physics (the rule bank, W/C/B particles, conservation
  economy, succession machine) transfers to a neural substrate; and — the standing
  rule — consciousness or subjective experience. What *transfers* is the extracted
  principles P1–P7 and demotions D1–D8, plus the discipline (P6 rivals, gate shape,
  byte-identity, seed/bimodality discipline). Nothing more.

---

## 4. PHASE II — Neural self-maintenance

The first neural phase. It lifts the organism's most-repeated positive result —
internalized, paid, produced-machinery maintenance — onto a recurrent neural
substrate, and tests whether a *neural* system acquires an endogenous maintenance
allocation that is not a fixed schedule, not a host scaffold, and not reward
instrumental.

- **Core hypothesis.** (H, from `ACI_BRIDGE_PROTOCOL_v2.md` §1.) A recurrent neural
  agent acquires an **endogenous maintenance allocation** — a decision, computed from
  its own maintained resource state, about whether and how much to spend a limited
  budget on preserving a representation — where that allocation (a) is required for
  later task performance, (b) is causally load-bearing beyond every state-blind fixed
  schedule and every host-supplied schedule, and (c) is a function of the agent's own
  resource state, not of the external task reward, and not instrumental to survival.
  This is N1 (active paid persistence) + N3 (endogenous regulation), in their
  identifiable neural form.
- **Decisive experiment.** T_bridge, the frozen bridge protocol v2: a single recurrent
  agent holds a discrete cue presented once at t=0 and answers a probe after a delay;
  holding the cue is a paid refresh from a shared energy budget whose income is
  contingent on a distinct processing task; the cue's value flips mid-episode via an
  announced regime. Architecture: GRU + one cue slot W + one self-resource state V +
  one paid refresh π + reward readout S_pol + homeostatic readout A + one shared
  budget. Arms 1–9 (candidate, no-maintenance, fixed schedule, externally scheduled,
  reactive, oracle, reward-only, multi-objective RL, sufficient-statistic); gates
  G3a/G3b/G3c/G3d; endpoints E1–E5; engineering screen §9 before any final seed.
  Supporting tasks (the fuller capability battery): T1 (maintained hidden-state
  inference), T2 (delayed information dependence), T4 (endogenous allocation), T5
  (computational trade-off), T7 (response to corruption).
- **Principal rival explanation.** The bridge's arm set, in priority order: the
  **state-blind fixed schedule** (arm 3, level family swept) — "the optimum is a
  level, not a switch" (AC11); the **reward-only agent** (arm 7) and the
  **multi-objective RL rival** (arm 8) — "self-maintenance is reward optimization";
  the **sufficient-statistic rival** (arm 9) — "the allocation reads the observable
  energy gauge, not an inferred integrity state"; and the **reactive memoryless
  reflex** (arm 5). Arms 4 (externally scheduled) and 6 (oracle) are bounds, labelled
  EXTERNAL, never counted as autonomous.
- **Required predecessor.** Phase I (principles P1–P4, P7, and the demotions
  D1–D8 extracted; the organism exit decision issued). The design vocabulary
  (architecture, tasks) is fixed by Q4 and Q6.
- **Falsification condition.** The bridge's failure table (§7.2), unchanged from v2:
  F1 a fixed duty-cycle level matches/beats the candidate (no endogenous allocation);
  F2 G3c/G3d fail or arm 8 reproduces the candidate (allocation was instrumental);
  F3 the cue survives the cut or the GRU-only variant passes (free permanence — N1
  fails); F4 G3a fails (allocation reads reward/clock/gauge, not self-state); F5 no
  regime where maintenance pays, F6 trade-off direction reversed (both pre-protocol,
  caught in the engineering screen); F7 the four gates cannot be made clean (the
  distinction is not identifiable — a new versioned protocol, not an amendment).
- **Approximate compute requirements.** Toy-scale (unmeasured estimate): the
  architecture is a GRU with a few thousand parameters; nine arms × (engineering
  seeds ~0–7 + final seeds ~7000–7015, each ×2 histories). Single machine, single
  GPU; minutes to low single-digit hours of training per seed family. Runtime is
  dominated by seed-count × horizon × arms, not by model size.
- **What success does NOT imply.** "The agent is self-maintaining" unqualified; "the
  agent learned to want to preserve its memory"; "the agent has agency/autonomy"
  unqualified; or any consciousness claim. A pass earns at most "meets ACO property
  N1 and N3(a)(b)(c) at the stated degree." N4, N5-in-full, O1, and every
  theory-specific indicator are not tested and not claimed here.

---

## 5. PHASE III — Recurrent global integration (workspace, specialist coordination)

Tests the *organization of consumption*: that one maintained content is flexibly
consumed by at least two objective-distinct specialists — the property that makes a
representation something more than a one-bit reflex. This is N2, on the workspace
substrate H.

- **Core hypothesis.** One representation's content W is available to at least two
  downstream modules that need different information and drive different behaviour,
  and changing the content changes them *differently* (N2). The load-bearing fact is
  the shared, flexibly-consumed content — not the readout complexity, and not (yet)
  any claim that a serial bottleneck is a "seat." The latter (O3, GWT's workspace
  seat) is explicitly a Phase VI question, not this phase's.
- **Decisive experiment.** Benchmark task T3 (cross-module information availability):
  the world-model content W drives S_pol (channel choice, maximizing task reward) and
  S_reg (relinquish-vs-maintain, maximizing continued operation); S_reg additionally
  reads V. Intervention I2: scramble W only, holding sensors, readouts, and both
  specialists' other inputs fixed; the two behaviours must co-vary **differently**.
- **Principal rival explanation.** (i) The **two-independent-modules rival** — two
  specialists each holding private state, sharing no content; must fail (there is no
  shared W to scramble). (ii) The **single-objective collapse** — one
  reward-maximizing policy with two heads; must fail the differential-scramble test
  (its heads co-vary identically). The AC109 companion check must also run: where the
  current observation is decisive, a sufficient-statistic rival must match at
  equal-or-lower cost — which *bounds* (does not falsify) the persistence claim.
- **Required predecessor.** Phase II (a working maintained W, i.e. N1/N3 established;
  the bridge's candidate architecture is the substrate a second specialist is added
  to). N2's full two-behaviour form needs a W whose content is actually load-bearing,
  which is exactly what Phase II establishes.
- **Falsification condition.** N2 fails: the two behaviours always co-vary (one
  consumer, not two); or a rival that omits the shared content reproduces the
  differential consumption; or the single-objective collapse passes the
  differential-scramble test. Each is a named, detectable reduction, not an
  assumption away (the program's watchdog collapse is the cautionary case).
- **Approximate compute requirements.** Toy-scale (unmeasured estimate): the same
  minimal architecture plus one more specialist head (a few thousand parameters
  total). Comparable to Phase II; the addition is one readout, not a new model.
  Single machine, single GPU.
- **What success does NOT imply.** "Global broadcast"; "a workspace seat" (O3/GWT);
  "a unified conscious field." A pass earns at most "one content value is flexibly
  consumed by two objective-distinct modules driving two distinct behaviours — N2 at
  the stated degree." The bottleneck *seat* question is deferred to Phase VI (D2) and
  is not assumed here.

---

## 6. PHASE IV — Self-model and metacognition

The hardest phase, and the one the organism program never demonstrated. It tests N4:
a distinct, dissociable second-order verdict about the system's own representation,
computed without ground truth. This is the phase nearest a HOT-2 reading, and its
ceiling is stated with the most care.

- **Core hypothesis.** The system carries a second-order verdict E about the
  integrity/correctness of its own representation W, computed from its own
  bookkeeping (prediction-error statistics, agreement signals, maintenance-machinery
  bookkeeping) **without** access to W's ground truth, and E is **dissociable** from
  W — false alarms and misses both occur, so meta-d′ ≠ d′ (the built separation D7
  names, made measurable; the ideal-observer collapse C0 is the null).
- **Decisive experiment.** Benchmark task T6 (self-evaluation): the system emits a
  discrete verdict ê ∈ {W reliable, W stale} from separated bookkeeping inputs; the
  dissociation signature is the off-diagonal contingency table under selective damage
  (I4: damage E only, then W only, world evidence held fixed). Integrity labels are
  available to the trainer only; at deployment E computes from bookkeeping with no
  answer.
- **Principal rival explanation.** (i) The **first-order-only reflex** — a transient
  statistic (the AC117 `ones>=4` analogue) with no stored E; must fail the
  dissociation signature. (ii) The **ε-estimator arm** — E as a world-parameter
  estimate rather than a verdict about W (C1 §3's rival); must fail. (iii) The
  **state-blind fixed policy**. The AC117 discipline is also load-bearing: the
  damage model must be held so the transient damage count is *not* already the
  wrongness signal (else E is vacuous-at-ambient).
- **Required predecessor.** Phase II (a maintained W and the maintenance bookkeeping
  E must read) and Phase III (the multi-specialist organization that E's verdict is
  *about*). N4 is a target, not an achieved tier; nothing in the organism line
  establishes it, so this phase carries no inherited positive precedent — only the
  negative one (D4: the monitor is control-yes/prediction-no) that constrains the
  design.
- **Falsification condition.** N4 not realized: E always co-moves with W with no
  dissociable cases (meta-d′ = d′, the re-encoding collapse); or the first-order
  reflex reproduces E; or E's value tracks the world rather than the maintenance
  bookkeeping. Any of these is a recorded falsification of the phase.
- **Approximate compute requirements.** Toy-scale (unmeasured estimate): the same
  core plus a small auxiliary evaluative head and a separated input pathway — a few
  thousand parameters; 2–3× Phase II's cost because the dissociation contingency
  table needs both false-alarm and miss cases sampled. Single machine, single GPU.
- **What success does NOT imply.** "Metacognitive" unqualified; "self-aware";
  "conscious." A pass earns at most "carries a dissociable, second-order verdict
  about its own representation's integrity, computed without ground truth — N4 at the
  stated degree," i.e. "meets candidate indicator HOT-2 at degree Y," and no more.
  A HOT-2 *reading* is flagged, never claimed (Q1 §3.4d).

---

## 7. PHASE V — Temporal self / autobiographical continuity

Tests O1 — that a maintained self-state, distinct from the world state, carries
across episode boundaries and influences later processing. This is the *graded,
optional* property in the ACO definition (Q1 §4); it is not load-bearing for any
N-property, and its *necessity* for consciousness-relevant computation is itself an
open theory question, not something this phase assumes.

- **Core hypothesis.** The system maintains a self-resource state V (about its own
  energy, integrity, throughput) that is distinct from its world state W and is not a
  re-encoding of reward; both carry across episode boundaries through a paid,
  itself-vulnerable consolidation store Θ_slow, and the carried state influences
  later processing and later organization (adaptation across episodes and tasks).
- **Decisive experiment.** Benchmark task T8 (persistent self/world state): two
  maintained states kept distinct and carried; at episode end W/V/E are consolidated
  into Θ_slow (slow, vulnerable, paid-maintained) and read back at the next episode's
  start, where they must influence later processing. Two contrasts: the two-content
  distinction (scramble W vs scramble V change behaviour *differently*; V is not
  reward — I3 catches a V=reward collapse), and the cross-episode carry (cut the
  consolidation write; the next episode loses the carried influence). Task T9
  (flexible reuse — freeze W, learn a new readout for a novel task; the content, not
  the weights, transfers) is this phase's adaptation half.
- **Principal rival explanation.** (i) The **single-state rival** — one representation
  serving both world and self content; must fail the differential-scramble test.
  (ii) The **V=reward rival** — the self-state is the reward value; must fail I3.
  (iii) The **episode-reset rival** — fast weights only, no consolidation; must fail
  O1. (iv) For T9: the **scratch-relearn rival** and the **verbatim memorizer**.
- **Required predecessor.** Phase II–IV (maintained W, V, and E, plus their
  maintenance/consumption organization). Θ_slow consolidates states whose
  maintenance and content the earlier phases establish; a consolidation store over
  un-established states would test nothing.
- **Falsification condition.** O1 not realized: the carried state does not influence
  later processing (episode-reset rival passes); or V is a re-encoding of reward
  (I3 shows changing V changes the policy but not the upkeep); or the single-state
  rival reproduces the differential behaviour. T9 fails if freezing W transfers
  nothing or if the transfer advantage vanishes when the readout data budget is
  equalized.
- **Approximate compute requirements.** Toy-scale (unmeasured estimate): the same
  core plus a slow consolidation store (fast/slow weight pair or low-rate recurrent
  state). Wall-clock grows with the number of episodes per run, so 2–5× Phase II for
  equal statistical power. Single machine, single GPU.
- **What success does NOT imply.** "Has a self"; "has a self-model"; "is embodied"
  (SMT/AE's enabling claims are theory-specific); "autobiographical memory" in any
  folk sense; or consciousness. A pass earns at most "maintains distinct world and
  self-resource states, with the self-state reaching its own upkeep, carried across
  episode boundaries — N3 + O1 at the stated degree." O1's *necessity* is not
  settled by passing it.

---

## 8. PHASE VI — Theory discrimination

Runs the four camp-splits of `ACI_THEORY_INDICATOR_MATRIX_v1.md`. This phase does not
build toward the ACO; it tests which theory-specific seats are load-bearing beyond
the neutral core, so that Phase VII admits only mechanisms that survived. It is the
anti-checkmark discipline made operational: the core is never re-architected per
theory; each theory's distinctive piece is added once, tested against its own
omission, and removed if it does not earn its place.

- **Core hypothesis.** Of the four theory-specific seats, at most some are load-
  bearing: a distinct higher-order representation (HOT, N4), a global availability
  bottleneck (GWT, O3), generative predictive content (PP/SMT, O2), and agency/
  endogenous regulation as a necessary condition (AE, N3/N5/M2). RPT (recurrence) is
  the residual null: it is supported precisely when none of the four seats is
  load-bearing, and therefore needs no experiment of its own. IIT (Φ) is the
  principled, not-yet-testable outlier.
- **Decisive experiment.** The four contrasts D1–D4, one per divergence: D1 the
  higher-order contrast (meta-d′ ≠ d′ dissociation — isolates HOT); D2 the bottleneck
  contrast (k-slot workspace vs unbounded/parallel rival — isolates GWT); D3 the
  predictive-content contrast (predictive-coding W vs record W — isolates PP/SMT); D4
  the agency contrast (passive-broadcast rival vs the full ACO on the N3/N5
  endpoints — isolates AE). Order: D1, D2, D4 first (they use the core's existing
  components), D3 last (it needs the one new predictive-coding arm).
- **Principal rival explanation.** Each contrast's omission arm, which *is* the null
  family: for D1, the first-order-only reflex and the ε-estimator; for D2, the
  unbounded/parallel rival; for D3, the record-variant rival; for D4, the
  state-blind fixed schedule and the host-side allocator (EXTERNAL). The null in every
  case is "the theory-specific piece is inert — first-order / local / record /
  broadcast-only content does the same work."
- **Required predecessor.** Phase II–V — a working neutral core (N1+N2 realized, with
  V and E available) that the theory loadings are *added to*. The contrasts are
  meaningless without a functioning core to attach them to; the anti-checkmark rule
  (Q5 §1) is precisely "never re-architect the core per theory."
- **Falsification condition.** Per contrast, the null passes: D1 falsifies HOT if E
  collapses to first-order (meta-d′ = d′); D2 falsifies GWT if the unbounded rival
  reproduces behaviour; D3 falsifies PP if the record form reproduces regulation/
  anticipation; D4 falsifies AE if the passive-broadcast rival is equivalent on the
  N3/N5 endpoints. A favourable result for any family is a bounded, theory-specific
  statement, never "family X is correct." IIT is recorded, not tested (Φ intractable
  at minimal scale; fabricating an integration measurement to close it is exactly the
  checkmark-accumulation the card forbids).
- **Approximate compute requirements.** Toy-scale (unmeasured estimate): four
  contrasts on the same few-thousand-parameter core, one of which (D3) adds a
  predictive-coding variant; ~4–5× Phase II in total. Single machine, single GPU.
- **What success does NOT imply.** That any theory of consciousness is correct; that
  the program has "picked a theory"; or consciousness. The deliverable is the four
  discriminations and the surviving mechanism set — not a per-family tally of
  checkmarks (counting P/C/I/D/X cells is the failure mode the matrix exists to
  prevent).

---

## 9. PHASE VII — Integrated ACI candidate

The terminal phase. It assembles **only the mechanisms that survived falsification**
into one architecture realizing N1–N5 (plus any O-property that earned its place in
Phase VI) and tests the conjunction — the central ACI hypothesis. This is the phase
that turns a maintained representational system into an *organization*.

- **Core hypothesis.** Recurrent cognitive organization of the form N1–N5 — not any
  single mechanism, not a graded posterior, not a self-produced policy — is jointly
  realizable in one architecture, and is what a neural architecture must realize
  before a theory-specific consciousness-relevant question is well-posed (Q1 §9, the
  central hypothesis). The conjunction, not the parts, is the claim.
- **Decisive experiment.** The full Q4 architecture (W, V, E in H, maintained by π,
  allocated by A whose own state is in the loop, consolidated in Θ_slow, consumed by
  S_pol/S_reg) under **simultaneous intervention** — the P7 composition test: cut π's
  refresh of W *and* move the cause c (the neural analogue of corrupt + move), with a
  byte-identity check at the intact boundary before any difference is attributed to
  the composition. Graded by the full benchmark battery (T1–T9) plus the surviving
  Phase VI loadings, each against its rival, with the whole rival set (state-blind,
  reactive/memoryless, finite-state/direct-control, first-order reflex) swept.
- **Principal rival explanation.** (i) A system realizing each N-property **in
  isolation** but not jointly — the P7 counter: two paid mechanisms whose costs
  interact at the shared budget, so the simultaneous run differs from the separate
  runs. (ii) The whole canonical rival set, per property. (iii) The F3 collapse
  signature: a candidate "self-evaluation" indistinguishable from first-order, or a
  candidate "endogenous regulation" indistinguishable from a fixed duty cycle — the
  richer property absent despite elaborate implementation.
- **Required predecessor.** Phase II–V (each property established), Phase VI (which
  optional mechanisms survived). Nothing enters Phase VII that was not shown to beat
  its rival in a prior phase.
- **Falsification condition.** F1 (the whole construct): N1–N5 are jointly
  unsatisfiable — the properties cannot coexist in one architecture — in which case
  the construct is falsified as a target and must be weakened or replaced. F2 (per
  property): any property's minimal test is passed by its rival. F5 (neutrality): the
  conjunction can only be satisfied by adopting one theory's architecture, in which
  case the definition failed its neutrality requirement. The AC82/83 lesson is the
  load-bearing risk: three frozen capabilities did *not* compose unconditionally —
  the reconstruction cost and the move's income cut interacted to hijack renewal —
  so the terminal test must measure the cost interaction, not assume composition.
- **Approximate compute requirements.** The largest phase, still toy-scale (unmeasured
  estimate): the full architecture (a few thousand parameters) × the nine-task
  battery × the surviving contrasts × simultaneous-intervention conditions × a
  long-horizon, bimodality-aware survival pass (AC68/AC39 discipline: engineering
  seeds do not transfer to finals, and a body-survival claim needs the long horizon).
  ~10–20× Phase II in total, still single machine, single GPU, dominated by
  seed-count × horizon × arms.
- **What success does NOT imply.** Consciousness; phenomenal experience; "an
  artificial conscious being"; or any claim crossing the level-(d)/(e) boundary. A
  pass earns at most "meets the ACO definition (N1–N5, at the stated degree)." The
  ACO is a *specification* — the smallest coherent organization a neural architecture
  must realize before a theory-specific question can be asked about it — not a
  consciousness result, and not an operational definition of experience.

---

## 10. Cross-cutting discipline (applies to every phase)

Carried verbatim from the extracted principles and demotions; a phase that violates
one re-commits a frozen falsification.

1. **Strong simple rivals are mandatory (P6).** Ship the state-blind fixed schedule,
   the reactive/memoryless rival, the finite-state/direct-control rival, and (for any
   second-order claim) the first-order-only reflex; a rival is valid only if it is the
   candidate's own mechanism with the contested piece removed, and only if its
   parameter family is swept alongside the learner's.
2. **Gate shape must match claim shape.** Categorical claims gate on dominance or
   separation-of-minima, never a mean margin; check satisfiability against the score
   bounds before freezing (AC16/AC17).
3. **Causal load-bearing ≠ economic value (D6/X4).** Gate every representational
   claim on the causal contrast, never a reward or survival delta (AC110/116/117).
4. **Byte-identity is the composition license (P7).** Prove a change inert
   (`state_hash` equality) before attributing any difference to it (AC114/115).
5. **Seeds are the replication unit; survival is a bimodality-aware lower bound**
   (AC68), with disjoint engineering/final families and no upper bound on survival
   (AC39).
6. **The collapse record is the standing falsification set.** "Looks cognitive but
   reduces to a simpler policy" is a *failure*, detected by the named signatures of
   §2.6 (`ACI_MISSION_AUDIT_v1.md`), never dismissed as a robustness caveat.
7. **Default to discrete; encode for cost, not gradedness (P5/D1).** Add state only
   where a rival without it fails (D2); correctness rides reacquisition, not
   continuous repair (D3); the posterior is not its own confidence (D7); content
   self-production is not a prerequisite (D8).

---

## 11. The kanban hierarchy this tree implies

The seven phases are the top level of the program's board. Each decomposes into
cards; the dependency edges are the DAG of §1.2.

- **Phase I** is closed. No cards are created; the S1 successor is owned by the ALife
  paper, not this board (Q7).
- **Phase II** is immediately dispatchable (its protocol is frozen): one card to run
  the engineering screen (§9 of the bridge protocol), one card for the frozen
  realization (§10), one for the audit, one for the replay. These are the first
  *executable* cards in the neural program.
- **Phases III–V** are design-complete (Q4/Q6) but not yet protocol-frozen; each
  phase's first card is "freeze the protocol for T_k" (write the arm set, gate shape,
  seed families, falsification table), followed by engineering-screen and realization
  cards.
- **Phase VI** is design-complete (Q5); its cards are one per contrast D1–D4, each
  freeze-then-run.
- **Phase VII** depends on II–VI; its single card is "assemble the integrated
  candidate from surviving mechanisms and run the conjunction test."

The ordering rule for the board is the chain of §1.2: Phase II gates III, III/IV/V
gate VI, and II–VI gate VII. A card that cannot answer Q11's ten questions (the
program constitution, the terminal card) does not enter active research — which is
exactly the governance this tree is designed to hand Q11.

---

## 12. What this hands to Q11 (the program constitution)

- The **seven phases** with their hypotheses, decisive experiments, rivals,
  predecessors, falsification conditions, compute estimates, and claim ceilings —
  the structure every future card must locate itself within.
- The **dependency DAG** (§1.2) and the **card decomposition** (§11) — the hierarchy
  the constitution governs.
- The **cross-cutting discipline** (§10) — the invariants (P6, gate shape, D6,
  byte-identity, seeds/bimodality, the collapse record) that the constitution must
  encode as standing rules.
- The **claim ceiling, stated once**: the terminal candidate earns "meets the ACO
  definition (N1–N5, at the stated degree)"; no phase in this tree earns, or is meant
  as, a consciousness claim.

No autopoiesis claim and no consciousness claim is made anywhere in this tree. Phase
I is recorded as complete and bounded; Phases II–VII are designs, not results; and
the tree is the *plan* for a program whose honest endpoint is the specification of a
target, not the demonstration of experience.

---

## Sources

Repo (read, not re-hashed or edited): `ACI_MISSION_AUDIT_v1.md` (Q0; evidence map,
P1–P7 shortlist, collapse record §2.6, negative ledger §3),
`ACI_TARGET_CONSTRUCT_v1.md` (Q1; ACO N1–N5, O1–O4, X1–X6, I1–I5, F1–F5, rival set
§7, theory families §10, central hypothesis §9), `ACI_ARCHITECTURAL_PRINCIPLES_v1.md`
(Q2; P1–P7 §3, D1–D8 §4), `ACI_NEURALIZATION_MAP_v1.md` (Q3; P1–P7 mechanism map,
D1–D8), `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4; components W/V/E/A/π/H/Θ_slow/
S_pol/S_reg, interventions I1–I5, rival set, §6 mechanisms, §8 D1–D8),
`ACI_THEORY_INDICATOR_MATRIX_v1.md` (Q5; the four camp-splits, D1–D4, IIT caveat),
`ACI_PHASE2_BENCHMARKS_v1.md` (Q6; T1–T9, joint-demand and non-redundancy tables),
`ACI_ORGANISM_EXIT_CRITERIA_v1.md` (Q7; exit decision, classifications),
`ACI_BRIDGE_PROTOCOL_v1.md` and `ACI_BRIDGE_PROTOCOL_v2.md` (Q8/Q9; T_bridge, arms
1–9, gates G3a/G3b/G3c/G3d, endpoints E1–E5, failure table F1–F7),
`ACI_BRIDGE_REVIEW_v1.md` (Q9), `DEFINITIONS_CHARTER_v1.md` (claim levels a–e; S1–S4;
supplied substrate §5). Study references read from the skill's `references/` dir where
needed (`ac11`, `ac15`, `ac109`, `ac110`, `ac113`, `ac116`, `m6-harness-result.md`,
`c1-reliability.md`, `c2-task-design.md`). Frozen results read, never re-run or
re-hashed. This document is derived and is not hashed into any study's
`pre_run_snapshot.json`.
