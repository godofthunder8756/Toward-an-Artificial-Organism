# S0 — Continuation decision v1: feasibility outcome and the single strongest next step

2026-09-25. Terminal decision deliverable for the S0 card (t_fc7605c6): *what is the
feasibility outcome, and what is the strongest justified next step?* Predecessors: M6
disposition (t_4e030ff7, `AC117_RESULTS_v1.md`), A0 (t_29785c9c,
`A0_AUTONOMY_VERDICT_v1.md`), W0 (t_af25584a, doc reconciliation). It runs nothing,
re-hashes nothing, freezes nothing, and edits no frozen artifact (no runner, protocol,
results dir, hash, or ledger). It issues the continuation decision and names the next
step; it does not declare the research exhausted or achieved.

---

## 0. The decision, stated first

**Feasibility outcome: (c) — control effects present, but the reliability
interpretation unsupported.**

The estimator-monitoring feasibility question that the M-track reopened (C1 §3, "does the
organism maintain a second-order state that monitors its own estimate's reliability?") has
now been defined (M3), audited for identifiability (M4), designed as a frozen harness (M5),
and run (M6/AC117). The answer is split, and it is split in the direction that does NOT
reopen the reliability tier as a *monitoring/prediction* capability:

- **CONTROL — SUPPORTED.** The monitor's retained write-value (direction knowledge) is a
  genuine, causally effective, load-bearing maintenance state. Directional repair keeps the
  first-order estimate `e` correct in **32/32 individuals**, where the obs-bit-2 reflex, a
  transient `direct` policy, a history predictor, and a spend-matched `fixed_duty` all fail
  (C-G1 clean control 64/64, C-G2 utility dominance, C-G3 content inertness, C-G4 causal
  role via `scramble_m`/`scramble_e` all pass). The direction knowledge earns its keep as a
  *control* parameter — it knows which way to repair.
- **PREDICTION / RELIABILITY — UNSUPPORTED.** Under sticky-SET (0→1) damage the directioned
  count `ones>=4` *is* the wrongness signal, so a transient state-blind `direct` policy is a
  perfect predictor (AUC 1.0, Brier 0.0) and the monitor fails P-G5 (calibration) and P-G6
  (discrimination) against it. The retained write-value adds nothing to the *readout*; it
  adds the *repair direction*. And at the frozen ambient 1e-4 rate the harness is vacuous —
  action 2 already maintains `e` via unrelated program corruption, so the monitor == reflex
  (base rate 0/8096).

The "second-order predictor" / HOT-2 metacognitive-monitoring interpretation therefore does
not survive this test. What survives is a narrower, real result: the organism can maintain a
second-order state that drives **directional** repair of a first-order estimate, in a damage
regime the shared whole-bank reflex cannot handle. That is a control finding, not a
reliability-monitoring finding.

---

## 1. Why (c), not (a), (b), or (d)

- **Not (a)** — (a) requires prediction AND control both supported; P-G5/P-G6 fail, so no
  organism-scale reliability-monitor protocol is licensed. M6's own disposition is
  (c)-shaped: "the result does NOT license an organism-scale reliability-monitor protocol."
- **Not (b)** — (b) asserts *prediction* supported with control unresolved; the inverse
  holds (control supported, prediction unresolved-as-failing).
- **Not (d)** — (d) requires feasibility blocked by a named limitation with no positive
  result; there is a genuine, load-bearing control result (C-G1–C-G4), so the mechanism is
  not blocked, it is bounded.
- **Is (c)** — control effects are present and causally isolated; the *reliability*
  (prediction/monitoring) interpretation of the monitor is unsupported in the tested regime.

---

## 2. What this bounds, and what it does not

**Bounded (recorded, not erased).** The reliability tier, at the harness level, is
CONTROL-yes / PREDICTION-no / vacuous-at-ambient. The monitor is not a reliability grader;
it is a directional-repair controller whose value is representational, not economic
(route-1 retention 1.00 in every arm; income +3%). This is consistent with, and carries
forward, the AC116 storage lesson: a genuine mechanism can be causally load-bearing while
economically marginal.

**Not licensed.** No organism-scale reliability-monitor protocol (S0 option a); no entry of
AC117 into the integrated organism's evidence ledger (harness-level only, per W0); no claim
that the reliability tier is "closed" — it is *bounded at the harness level* in the tested
(sticky-SET, damage-component) regime, and the roadmap's K9 gate stands: it is re-openable
only by a mechanism change introducing a non-zero, non-trivial error rate where the damage
count is *not* already the wrongness signal (e.g. bidirectional damage with an acquired
value that can be 1). That re-open is a possible future route, not this cycle's next step.

---

## 3. The single strongest justified next step

**Design the finite clause-(ii) successor: the spatial realization of the informational
core (A0 R1–R4, tested by T1–T5).**

The A0 verdict named the *sole* remaining genuine clause-(ii) limitation — the non-spatial
informational core (program, description, pointer, coordination, route memory) living in
fixed arrays never positioned and never passed to `tr.move`, "inside" only by declaration —
and converted it from a modeling fact into a **finite causal requirement**:

- **R1 (realization-by-production):** the informational substrate is a produced component
  class (or an extension of W's role) with positions, finite lifetimes, and observed
  turnover — C1/C2 hold for it as for W/C/B.
- **R2 (local access):** reads and paid writes are position-mediated through produced
  machinery; no host dereference; a read fails where the local reader is absent.
- **R3 (retention vulnerability):** the informational substrate is in the transport and
  damage streams; a puncture degrades it; its renewal is paid and W-gated.
- **R4 (mutual constraint):** the informational substrate lies on the production-dependency
  cycle with W/C/B — production maintains it and it constrains production.

Candidate tests are prespecified (T1 localized read, T2 retention vulnerability, T3
production dependency, T4 mutual-constraint directionality, T5 no-hidden-backup
observer-discard) with a prespecified falsification (a hidden host array reproducing the
trajectory under T5; a removed reader leaving action selection unchanged under T1; a
transport-exempt core behaving identically under T2).

**Why this, against the named alternatives.**

- **It is the sole remaining genuine clause-(ii) limitation.** Clause (i) production closure
  is SUPPORTED (inherited by composition, AC115 G1 byte-identity); composition is SUPPORTED
  at the mechanism level (survival-level NOT confirmed, G4–G7 retained as failed); the
  exchange interface is now resolved (SR-1 → AC114/AC115). Every other front is either
  stable in-model or bounded by a recorded negative (storage suspended at the resolution
  floor; graded generalization negative; the monitor now bounded control-yes/prediction-no).
  The non-spatial core is what stands between the present verdict and a stronger (still
  bounded) clause-(ii) claim.
- **The reliability tier is no longer the "reopened" next question.** It was the single
  strongest next question last cycle (S0-v2 item 7); the M-track has now answered it at the
  harness level with CONTROL-yes/PREDICTION-no. Re-testing prediction under a different
  damage model is a robustness re-test, not a new ceiling, and is subordinate to the
  architectural question that still gates the central autopoiesis claim.
- **A re-architecture, not a run.** This successor is a change to the supplied physics (a
  new component class plus a localized read/write reaction), exactly as SR-1 was — it is
  out of the frozen AC9 model's scope, and it is finite (four checkable properties), not an
  infinite regress. Supplied substrate (geometry, laws, reaction forms, interpreter, initial
  content) stays supplied; only the informational core's *realization* moves from declared
  to produced.

**The monitor's direction-knowledge finding is a carried input to this design, not its
subject.** AC117 established that a second-order maintenance state (retained write-value)
can be genuinely load-bearing for directional repair. The successor's local read/write
machinery (R2) will need exactly such a state, so the M-track's positive control result
composes forward into the R1–R4 architecture as an available primitive — without importing
the reliability-monitoring interpretation that failed.

---

## 4. The follow-up card commissioned

One dependency-linked card is created (see §Sources for the id): a **design/specification
task** — turn R1–R4/T1–T5 into a concrete successor specification (the informational-core
realization architecture, with its prespecified gates and falsification), in the same form
`A0_SUCCESSOR_SPEC_v1.md` gave SR-1, with the resulting frozen proposed protocol marked
AWAITING separate execution authorization. It is design-only: **do not run it in this
program**, do not build `acN.py`, and do not freeze seeds. The build is a further card the
spec commission may authorize.

---

## 5. Disposition

- The continuation decision is (c); the monitor tier is bounded (control-yes,
  prediction-no); no organism-scale reliability-monitor protocol is prepared.
- The strongest justified next step is the finite clause-(ii) successor (R1–R4/T1–T5),
  carried forward as a commissioned design task.
- Neither autopoiesis nor consciousness is claimed; the research is neither exhausted nor
  achieved. The level-(d)/(e) boundary is untouched.

## Sources

`AC117_RESULTS_v1.md`, `AC117_PROTOCOL_v1.md`, `M5_MONITOR_HARNESS_DESIGN_v1.md`,
`M4_MONITOR_INPUT_AUDIT_v1.md`, `M3_MONITOR_TARGET_v1.md`, `A0_AUTONOMY_VERDICT_v1.md`
(§4–§6), `A0_SUCCESSOR_SPEC_v1.md` (the SR-1 precedent for the spec form),
`CONSCIOUSNESS_ROADMAP_v1.md` (§13), `S0_SYNTHESIS_v3.md` (item 7), `I5_INTEGRATED_
ORGANIZATIONAL_VERDICT_v1.md`. Frozen results read, never re-run or re-hashed:
`ac117_results_v1/` (480 rows). This document is derived and is not hashed into any study's
`pre_run_snapshot.json`. Follow-up card: t_5380f752 (S1 — Spec the spatial informational-core successor).
