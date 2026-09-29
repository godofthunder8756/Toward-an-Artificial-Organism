# Architecture-by-claim matrix (I0, extended by W0 through I1/C1/I5/C3)

2026-09-24. Audit deliverable for the I0 card (t_3eba13c2): *which architecture actually
contains which mechanisms, and which evidence has been transferred across architectures
without a demonstrated composition argument?* Grounded in the code at e5f6050, not in
any study's prose. Extended by W0 (t_f741e226) to carry the I1 boundary correction, the
C1 reliability correction, the I5 integrated-organizational verdict (AC115), and the C3
storage comparison (AC116). Extended again by A0 (t_29785c9c) to carry the M1 outcome-
classification errata (AC115 export 14/16; G6 RETENTION+DEATH; G7 DEATH-only; t=347
early collapse, not long-horizon) and to name the finite causal relationship a future
spatial successor must demonstrate (the R1–R4 requirement and T1–T5 tests,
`A0_AUTONOMY_VERDICT_v1.md`). Extended a fourth time by N14 (t_8b4303fa) to add the
**neural-bridge lineage** (T_bridge, the Phase-II experiment) and its claim status
after the OUTCOME B + D verdict — §8. Extended a fifth time by G0 (t_e408b2f6) to
record the **Phase-III baseline** — the revised neural architecture and its
per-component classification after the B + D verdict — §9. Extended a sixth time by G16
(t_a299aaef) to record the **Phase-III result** — OUTCOME C, the sufficient statistic
wins, the Shared Latent Workspace candidate and its five reduction rivals R1–R5, with the
joint Phase-II + Phase-III teaching — §10.

One sentence up front: **there are two architecture lineages in scope, and the largest
pre-integration study number (AC114) is NOT the integrated one.** AC114 is a minimal
AC9-derived branch that contains none of the five internalization mechanisms; the
integrated architecture was the AC105-113 line, whose shared root is `ac95.py`. A4/S0
transferred the AC80-99 closure evidence into the AC114 verdict without a composition
argument; that is exactly the error I1 corrects. **AC115 is now the realized
integration** (I2–I5): AC114's SR-2 admission gate composed with the AC105 five-mechanism
closure in one organism, byte-identical at the intact boundary (G1). AC116 (C3) tests the cognitive
storage line and returns F1 (weak dominance at the sign-flip resolution floor — the storage question is
suspended, not closed). §7 organizes the
whole account by architecture, using the six W0 categories.

---

## 1. The two lineages (transitive source dependencies, from the import graph)

**Lineage B — minimal AC9-derived exchange successor (AC114, frozen seeds 6500-6507).**

```
ac114.py
  ac9_priority_v2.py -> ac9.py
  ac9.py   -> ac4.py, ac5.py, ac5_program.py, ac9_memory.py, ac4_transport.py, ac1.py
  ac4.py, ac4_transport.py, ac1.py   (surgery targets)
```

Full transitive closure: `{ac9, ac5, ac5_program, ac9_memory, ac4, ac4_transport, ac1}`.
The organism is `ac9_priority_v2.acquire(seed)`, i.e. `ac9.acquire` with the AC9-v2 rule
reorder. `ac9.acquire` zeroes `traces[0,126:]` and `traces[1:]` — there is **no bank-1
description store** (ac9.py:24 `b.traces[1:]=0`).

**Lineage A — integrated cognitive successor (AC105-113), shared root `ac95.py`.**

```
ac105.py -> ac104 -> ac103 -> ac102 -> ac101 -> ac100 -> {ac99, ac99_d2 -> ac99}
                -> ac96 -> ac95 -> {ac76 -> ac71 -> ac12 -> {ac9, ac9_priority_v2, ac4,
                                   ac5_program, ac12_memory}, ac9, ac4, ac5_program}
ac107.py -> {ac99_d2, ac96, ac95, ac12, ac4, ac71, ac9}
ac110.py -> {ac107, ac106, ac12, ac95, ac96, ac100, ac4, ac9, ac71, ac99_d2, ac5_program}
ac111.py -> {ac110, ac107, ac106, ac104, ac103, ac12, ac95, ac96, ac100, ac4, ac9,
             ac71, ac76, ac99_d2, ac5_program}
ac112.py -> {ac110, ac107, ac106, ac99_d2, ac96, ac95, ac12, ac4, ac71, ac9, ac100,
             ac5_program}
ac113.py -> {ac112, ac12, ac4, ac95, ac96, ac100, ac106, ac107}
```

`ac95.py` carries the whole internalization layer (130-bit description, `SLOTS=4`,
`Succession`, `build_program`/`reg_from_active`, `_cap`); `ac12.py` carries the
streak/register primitive (`STREAK_N=6`, `Alloc`, `bit_value`, `_drop`/`_restore`) on top
of the same `ac9` base. Every runner from `ac96` upward imports `ac95`; AC114 imports none
of them.

---

## 2. The five mechanisms, defined once, with their code locus

| Mechanism | Definition | Code locus (root) | Introduced |
| --- | --- | --- | --- |
| **Description turnover** | The 130-bit recipe is stored in interchangeable slots and re-made from itself (copy → verify → switch → remove) | `ac95.Succession`, `SLOTS=4`, `slot_offset`/`read_slot`/`read_pointer` | AC86, AC87 |
| **Succession coordination** | The succession controller's working state (active/phase/last-start) lives in the maintained substrate, written atomically | `ac95` controller-state layout + `Succession` (MODE/LAST split) | AC87, AC88 |
| **Reconstruction** | The 126-bit program is rebuilt from the 130-bit description on the damage signal | `ac95.build_program`, `ac95.reg_from_active` | AC80, AC85, AC87 |
| **Internalized operational memory** | The decision state (3-bit streak + reserve bit) in the dead rule's free bits, Gray-coded, majority-read, W-gated paid writes | `ac96.streak_*`, `ac99.reserve_*`, `ac99_d2.gray_*` | AC95/96/99 |
| **Decision allowance** | The spending budget that reserves material for the decision state's writes (`material - 42`) | `ac104.DECISION_ALLOWANCE = STREAK_N*7 = 42`, `budget_rule`; `ac99.reserve` | AC97/98/104 |

---

## 3. Architecture-by-claim matrix

"Present" = the runner's transitive closure actually contains the code path, and a frozen
run exercised it. "Inherited (justified)" = reproduced byte-for-byte from a prior study
(`state_hash` equality). "Transferred (no composition)" = cited in prose but absent from
the architecture.

| Architecture (runner) | Deps (root) | Developmental scaffold | Operational scaffold | Demonstrated (frozen) | Inherited, justified | Transferred w/o composition |
| --- | --- | --- | --- | --- | --- | --- |
| AC9 (ac9.py) | ac4, ac5, ac5_program, ac9_memory, ac4_transport, ac1 | grow `t<512`, activation `t<512`, deposit | program bank (126×7), route memory, W/C/B, B(20), repair (action 2), renewal (3/4), birth (6), B-birth (8) | developmental routing, retention, production (AC9 controls v3) | — (base) | — |
| AC114 (ac114.py) | ac9 + ac9_priority_v2 + ac4 surgery + ac4_transport + ac1 | same AC9 schedule | **AC9 body only** (no description store, no succession, no reconstruction, no streak/reserve, no allowance) + **SR-2 admission gate** | boundary-mediated exchange (G1-G6), retention continuity (G2) | AC10 retention + production (field-for-field, G2) | description turnover, succession, reconstruction, operational memory, decision allowance (all absent) |
| AC95 (ac95.py) | ac76, ac71, ac12, ac9, ac4, ac5_program | corruption@8192, move@8192 | 130-bit desc (SLOTS=4), Succession, reg_from_active, streak (host) | description maintenance + succession + reconstruction | AC87/AC89 succession, AC85 desc, AC80 recipe | — |
| AC99/99_d2 (ac99.py, ac99_d2.py) | ac96, ac95, ac12 | corruption+move | reserve bit + Gray streak in dead-rule free bits | internalized operational memory (streak+reserve) | ac95 (byte-identity), ac96 streak | — |
| AC100 (ac100.py) | ac99, ac99_d2, ac96, ac95, ac12 | two-move schedule | Gray vs binary streak; reserve | Gray encoding carries the success (2×2) | ac99 (byte-identity) | — |
| AC104 (ac104.py) | ac100, ac99_d2, ac99, ac96, ac95, ac12, ac9 | corruption+move | reg_from_active + allowance-42 budget | reconstruction + decision allowance | ac101-103 (byte-identity at baseline) | — |
| AC105 (ac105.py) | ac104 + full stack | corruption tick + move schedule as run params | **all five mechanisms in one run** | operating range of persistent-trigger + allowance-42 (6/6 gates) | ac104 (byte-identity at baseline) | — |
| AC107 (ac107.py) | ac99_d2, ac96, ac95, ac12, ac4, ac71, ac9 | move vs read-cut | one-bit cause estimate in dead-rule action bit | cause discriminator (frozen partial) | ac106 world | — |
| AC108 (ac108.py) | ac107, ac106, ac12 | move/cut/no_cause | no_write / force / scramble arms | coupling both directions (7/7) | ac107 (byte-identity) | — |
| AC109 (ac109.py) | ac107, ac99_d2, ac12, ac4, ac9 | move/cut | direct diagnostic rival | storage inert (equivalence) | ac107 (byte-identity) | — |
| AC110 (ac110.py) | ac107, ac106, ac12, ac95, ac96, ac100, ac4, ac9, ac71, ac99_d2 | C2 gated world | maintained vs no_repair | repair not load-bearing in-window (G4 8/16) | ac107 (byte-identity) | — |
| AC111 (ac111.py) | ac110, ac107, ac106, ac104, ac103, ac12, ac95, ac96, ac100, ac4, ac9, ac71, ac76, ac99_d2 | corruption + move | est × reconstruction × allowance | composes w/ contact-schedule interference (G3/G5 12/16) | ac110 (byte-identity), ac105 allowance | — |
| AC112 (ac112.py) | ac110, ac107, ac106, ac99_d2, ac96, ac95, ac12, ac4, ac71, ac9, ac100 | occlusion q + residual eps | two-counter accumulator | (engineering) | ac107/ac110 world | — |
| AC113 (ac113.py) | ac112, ac12, ac4, ac95, ac96, ac100, ac106, ac107 | high occlusion q=0.9 | two-counter vs single-counter | F1 no demonstrated advantage (frozen, R1) | ac112 (byte-identity) | — |
| AC115 (ac115.py) | ac105 stack (ac104→ac103→ac102→ac101→ac100→ac99→ac95→ac76→ac71→ac12→ac9) + ac114 admission-gate surgery | corruption@8192, move@8192+12288, puncture | **SR-2 link-specific admission gate composed with the five-mechanism closure** | mechanism-level composition (G1/G2/G3/G8 16/16); survival-level NOT confirmed (G4–G7 retained, seed-dependent) | ac105 (byte-identity via G1); ac114 SR-2 D1/D2 discriminations | — (this *is* the composition I0/I1 required) |
| AC116 (ac116.py) | ac110, ac107, ac106, ac99_d2, ac96, ac95, ac12, ac4, ac71, ac9 | C2 occluded-gate world (ε=0, q=0.9) | maintained integer counter vs tuned-memoryless / estimate / no_write / scramble | F1 no demonstrated income advantage (frozen) | ac110 (byte-identity at q=0.5, G1) | — |

---

## 4. AC114 mechanism inventory — verified per item, from code (NOT from prose)

Grounded in `ac114.py` (read in full), `ac9.py`, `ac9_priority_v2.py`, and a zero-hit grep
of `ac114.py` for every mechanism marker.

1. **Description turnover — ABSENT.** `ac114.py` imports no `Succession`, `SLOTS`,
   `pointer`, or `read_slot`. Its organism is `ac9_priority_v2.acquire`, and
   `ac9.acquire` sets `b.traces[1:]=0` (ac9.py:24), so there is no bank-1 description
   store to turn over. The 126-bit program lives only in `traces[0,:126]` and is repaired,
   never re-made from a description.
2. **Succession coordination — ABSENT.** No succession controller, no pointer, no
   active/phase/last-start state. AC114's only "transition" is the ONSET switch from the
   normal step to the punctured step, which is a run-loop flag (`pre`/`post`), not
   maintained state.
3. **Reconstruction — ABSENT.** AC114 runs the frozen `ac9.step` (or a `react`-shimmed
   variant); action selection is `prog.choose` directly. There is no `build_program`, no
   `reg_from_active`, no `rebuild`. The corruption stream `core_flips` is XOR-ed in and
   answered by action-2 majority repair only, as in base AC9.
4. **Internalized operational memory — ABSENT.** No `streak`, no `reserve`, no counter in
   the dead rule's free bits. AC114 uses `ac9_priority_v2.acquire`, whose dead-rule mask
   bits are the frozen all-zero program content — not repurposed as decision state (the
   AC12 `Alloc`/register layer is never imported). The only "memory" is `ac9_memory`
   (route key→port entries), which is developmental route memory, not operational memory.
5. **Decision allowance — ABSENT.** No `DECISION_ALLOWANCE`, no `budget_rule`, no
   `reserve`. `ac114.py` has no `allowance`/`reserve` token at all (grep = 0).

**What AC114 DOES contain (its valid bounded finding):** the AC9 developmental body —
126-bit program bank (9 rules × 14 bits × 7 replicas) with majority repair, route memory
with renewal/deposit, W/C/B components, the 20-link B boundary with B-birth, and
fuel/material intake — plus the SR-2 admission gate (`ac4.react` actions 0/1 gated on
`GATE_LINKS[c]` live-state). Its licensed ceiling (A1 §5) is one step above retention,
one below clause (ii): *the produced boundary's live links admit the intake that funds
production, the same links that retain the constituents.* That claim rests on AC10's
retention + production evidence (inherited field-for-field, G2) and AC114's own admission
gates. It does **not** rest on, and is not evidence for, any of the five mechanisms above.

---

## 5. The single authoritative integrated baseline — AC105, NOT AC114

**Selection: AC105** (the frozen persistent-trigger + allowance-42 architecture,
seeds 5800-5807), with **AC111** as the cognitive composition point (AC105 + the AC107/110
cause estimate) and AC110/AC113 as the cognitive sub-studies C1/C2 anchor on.

Justification, from code and evidence, not the study number:

1. **AC105 is the one runner that composes all five mechanisms in a single frozen run.**
   Its transitive closure reaches `ac95` (description turnover + succession +
   reconstruction), `ac96`/`ac99_d2` (internalized operational memory), and
   `ac104.DECISION_ALLOWANCE=42` (decision allowance). The K2 closure verdict states it
   directly: "AC105 composes turnover/persistence/decision-operating-range in ONE run."
2. **Its inherited evidence is licensed by construction, not assertion.** At the baseline
   condition it reproduces `ac104` byte-for-byte (`state_hash`), and `ac104`→`ac103`→`ac102`
   →`ac101`→`ac100`→`ac99`→`ac95` each reproduce their predecessor the same way. So the
   AC80-99 evidence that AC105 inherits is carried by a demonstrated reproduction chain,
   which is the composition argument the matrix asks for.
3. **AC114 is the trap the task warns about.** It is the largest study number but a
   *minimal* branch: it shares only the AC9 base with AC105-113 and contains none of the
   five mechanisms (§4). Selecting it as "the integrated baseline" would re-commit exactly
   the error A4/S0 made — transferring later closure evidence into an architecture that
   does not contain the mechanisms producing it.
4. **Per-child anchoring.** I1's "new work" is the correction of AC114 itself (its
   baseline *is* AC114, and the correction is that AC114 is NOT the integrated
   architecture). C1/C2's "new work" (reliability disposition, storage comparison) lives
   on AC109-113, whose shared integrated root is AC105 via AC104/AC100. AC105 is therefore
   the single architecture the integration and cognitive work should be described against,
   with AC111 named as the point where the cognitive mechanism was added.

**What is out of scope for AC105 as baseline:** it does not contain the boundary-exchange
admission gate (that is AC114's addition, on the other lineage), and it does not contain
the AC112/113 two-counter accumulator (that is a later cognitive narrowing). Neither is
needed for the five-mechanism inventory; both are line-specific extensions.

---

## 6. Where the transferred-without-composition error sits (for I1)

A4 (`A4_EXCHANGE_VERDICT_v1.md`) and S0 (`S0_SYNTHESIS_v2.md`) reuse the K2 production-closure
verdict ("clause i SUPPORTED") in the context of the AC114 boundary-exchange successor.
Clause (i) is earned by the five-mechanism architecture (AC80-99, composed in AC105); AC114
contains none of those mechanisms, so the production-closure evidence was carried across
lineages **without a composition argument**. The one piece AC114 legitimately inherits is
AC10's retention + production (G2 field-for-field). The integration-dependency list I1 must
produce is: description turnover, succession coordination, reconstruction, internalized
operational memory, and decision allowance — all present in AC105, all absent in AC114.

---

## 7. The paper, organized by architecture (the six W0 categories)

The manuscript's claims are now organized by *which architecture contains the mechanism*,
not by finding. Six categories, each a distinct evidentiary status that must not be
collapsed into another. This section is the reconciliation target the manuscript (P1),
status, evidence index, and roadmap are built against.

### 7.1 Findings demonstrated TOGETHER in one organism

One frozen architecture holds each of these *in the same individual*; none is a
cross-study assembly.

- **AC115 (the integrated successor, finals 6600–6607, 208 rows).** All six integrated
  functions — exchange admission, retention, boundary renewal, reconstruction,
  succession, paid updates — are present AND exercised in the SAME organisms (the `keep`
  arm, 16/16): reconstruction fw 8→0, 6 successions desc 130/130, 2 relinquishments,
  paid reg/succ/ctrl writes, B_births 1674–1679. The admission gate is byte-inert at the
  intact boundary (G1 == AC105) and the discriminations hold through active reconstruction
  and succession. *Licensed wording:* one organism renews its produced exchange boundary
  while admission is link-specific (G2) and local (G3) and the five internalization
  mechanisms are preserved byte-for-byte (G1). **Mechanism-level composition is SUPPORTED.**
- **AC105 (finals 5800–5807).** The five internalization mechanisms (description turnover,
  succession coordination, reconstruction, operational memory, decision allowance) compose
  in one run; this is the architecture on which K3 issued the five-component closure verdict.
- **AC99–AC104.** Each composes its own mechanisms in one organism (Gray streak, 2×2 reserve
  factorial, persistent trigger, allowance-42) — the level-(b) adaptive-autonomy chain.

### 7.2 Findings demonstrated in SEPARATE experimental models

These are real but live on distinct architectures; citing them together requires a
composition argument (which AC115 now supplies for the exchange+closure pair, and which
AC111/AC116 supply only partially or not at all for the cognition pairs).

- **AC114** (minimal SR-2 body) established boundary-mediated exchange over {W, C, B} **on
  its own lineage**, containing none of the five mechanisms. It inherits AC10's {W, C, B}
  retention + production field-for-field (G2), nothing more.
- **AC107/AC108** (cognitive discrimination + coupling) live in the **clean two-cause world**
  (`corrupt=False`), not the AC105 combined-challenge body. Their composition with the
  autonomy architecture is AC111's question, answered only partially (direct channels clean;
  G3/G5 12/16 retained).
- **AC110** (repair dependence) and **AC113/AC116** (weighted / counter storage) are cognitive
  sub-studies on the AC107/110 world, separate from the AC105 closure line.
- **K3's five-component closure verdict belongs to AC105, not AC114** — the I1 composition
  correction, now superseded by AC115's demonstrated composition (the exchange role rides the
  produced B the five-mechanism organism already maintains).

### 7.3 Supplied model structure

Declared by the simulator and never produced by the organism; permitted substrate, not
counted against the verdict (I1 spatial correction). Inventory (charter v2 §5, A1):

- `prog.choose` (14-bit rule interpreter), `advance()` (succession transition logic), the
  decode format, the observation function, the conservation laws, the damage model, the tick
  clock, world constants, and the storage arrays (`traces (4,1024,7)`, `mem.Memory (2,2,3,7)`,
  `boundary[20]`).
- The **admission reaction form** (gated `react` actions 0/1), `GATE_LINKS`, yields — the
  exchange *function* is boundary-mediated; its *law* is supplied (A4/I1).
- **Supplied coordinates and physical laws are PERMITTED substrate**, not a clause-(ii)
  limitation (I1 correction: "the space is supplied" is struck from the limitation list).
- Content (rule words, priority permutation, `GATE_LINKS` association) is inherited/supplied
  (charter §6); content self-production is not required and remains AC78-blocked.

### 7.4 Causal intervention results (ablation/rescue, per-mechanism)

- **AC10** (9/9 gates): no-W / no-C / no-B / retention-rescue / external-B — every
  constituent dependency isolated. `external_B`/`B_rescue` labelled EXTERNAL.
- **AC114** (6/6): D1 site-vs-count, D2 local admission, D3 semipermeability, retention
  continuity — established by puncture ablation, not assertion.
- **AC115** (G1–G8): single-change license (byte-identity), link-specific + local admission
  discrimination, plus the four survival-bundled gates (G4–G7) retained as failures.
  Per M1 errata: G4/G5 DEATH (6602, t=347 early W/C collapse under B suppression, not
  horizon); G6 RETENTION (6606, single-particle leak, completes) + DEATH (6602); G7
  DEATH-only (description intact at death in every failing individual).
- **AC91/92**: W production load-bearing for viability (block → 8/8 die, content intact);
  functional interruption-and-rescue while underway.
- **AC107/108**: `no_write`/`force_machinery`/`scramble` single-flag interventions — both
  coupling directions.
- **AC110**: repair cut → correctness rides reacquisition in-window; repair load-bearing
  post-window (G4 8/16).
- **AC116**: `no_write` acquisition cut dies 4/16 under move (schedule perturbation, not
  clean read-content); `scramble` (read forced 0) survives 14/16.

### 7.5 Comparative performance (the candidate beats / ties / loses to a rival)

- **AC113** (R1): two-counter vs single-counter — **no demonstrated advantage** (seed-level
  sign-flip p ≈ 0.71/0.63, n = 8).
- **AC116** (C3): maintained integer counter vs strongest **tuned memoryless** rival —
  **F1 no demonstrated income advantage** (mean +200/seed, sign-flip p = 0.0625; weakly
  dominant, never worse; real but income-invisible cut-safety edge 4/16 vs 16/16).
- **AC109** (C1): stored estimate vs transient direct-diagnostic — **storage inert, content
  load-bearing** (48/48 match, lower cost).
- **AC99/AC100**: Gray encoding vs binary (the Gray encoding, not the reserve, carries the
  success — 2×2 factorial).
- **AC105**: allowance-42 budget vs no-spending-rule control — 6/6 gates, rescue on one
  unseen marginal priority (5804), no survival/relinquishment harm.

### 7.6 Unresolved theoretical interpretation (the genuine open questions)

- **Clause (ii) whole-organism unity — NOT ESTABLISHED.** Met only at the material
  (constituent) layer. The **sole** remaining genuine modeling limitation is the
  **non-spatial informational core** (program/description/pointer/coordination/route
  memory in fixed arrays never passed to `tr.move`). Supplied space is permitted substrate
  (I1). This is a finite successor question — not a permanently untestable fact — and it is
  **not** discharged by assigning coordinates to `traces` or passing arrays through
  transport: the successor must demonstrate the **causal** relationship (realization-by-
  production, local access through produced machinery, retention vulnerability, mutual
  constraint with W/C/B) named as R1–R4 with candidate tests T1–T5 in
  `A0_AUTONOMY_VERDICT_v1.md`.
- **Survival-level composition — NOT CONFIRMED.** AC115's G4–G7 fail on a minority of finals
  and are retained as failed gates (M1 errata: G4/G5/G6-6602 are an early W/C collapse under
  B suppression, not long-horizon; only G7's deaths t=9589–16336 are the AC68 W/C bimodality;
  G6-6606 is a single-particle retention leak; no failure is a description-integrity
  failure — AC39 transfer). Production closure and mechanism-level composition are
  unaffected.
- **Reliability tier — corrected disposition (C1).** C0's "not identifiable / closed" holds
  only under the ideal-observer assumption; the AC architecture violates it by construction,
  so the tier is **identifiable in principle as a question about monitoring the actual
  (damaged, maintained, sometimes-wrong) estimator** — a named discriminating candidate
  question, NOT yet demonstrated, NOT authorized. Estimating ε alone still does not establish
  metacognition.
- **Storage question suspended at the resolution floor (C3/AC116, M2-corrected).** Retained history does
  not demonstrate a *significant* graded income advantage over the strongest tuned memoryless policy (weak
  dominance at the sign-flip resolution floor — not "closed"); this bounds usefulness without erasing
  AC107's content-role, AC108's acquisition-necessity, AC110's repair-dependence, or AC113's single-counter
  sufficiency. Ongoing repair was deliberately not tested here.
- **Estimator-monitoring feasibility (M6/AC117, harness-level — not an architecture in scope).** The M5
  harness on the AC110/AC116 world: the monitor's retained write-value is load-bearing for CONTROL
  (directional repair keeps `e` correct 32/32) but NOT for PREDICTION (the transient `ones>=4` policy
  predicts wrongness perfectly), and vacuous at ambient damage. A harness result; it is not entered into the
  integrated organism's evidence ledger and adds no architecture to the matrix.

---

## 8. The neural-bridge lineage (Phase II, T_bridge) — added by N14

The bridge is a **third lineage**, distinct from both organism lineages: it is a
neural (GRU) architecture, not an AC runner, and its claim status is a matter of
the Phase-II verdict (OUTCOME B + D), not of the organism evidence. It is included
here so the architecture-by-claim matrix is complete across the whole program.

| Item | Bridge architecture (T_bridge, `bridge/final_arms.py` + frozen harness) |
| --- | --- |
| **Components** | GRU body; one cue slot W (paid refresh π, decay δ); one self-resource state V (integrity bit + energy code); allocator A (homeostatic, reads (V, s)); readouts S_pol (probe) and S_reg; shared energy budget |
| **Deps / provenance** | Not an AC runner; trained arms (candidate, P_rb arm 10, reward arm 7, multi-objective arm 8) from the frozen harness; mechanical arms (fixed family, arm 9, oracle) are hand-coded rules |
| **What it was built to test** | N1 (active paid persistence) + N3 (endogenous allocation from a maintained, *inferred* integrity estimate) |
| **What it earned (frozen, `N11`/`N12`/`N13`)** | **N1 — CONFIRMED (necessary condition only):** candidate slot survival 0.978 vs no_maintenance / free_memory 0.000, p = 2/2^12 = 0.00049, 12/12 seeds. **Not unique to the candidate** (fixed schedules + reward-only arm also hold the cue — N12 F2) |
| **What it did NOT earn** | **N3a/b/c NOT SUPPORTED.** Explicit V unnecessary: P_rb (no V slot) matches (0.823 vs 0.895, p = 0.64); arm 9_d (s,E,d threshold rule) attains the oracle (1.000) above the candidate; V's integrity bit is a re-encoding of the observable age `d_t`. Not strictly dominant over the fixed family (2/12 collapse) |
| **Transferred w/o composition** | None — the bridge is self-contained; its one claim is bounded to the δ-decay **observed-integrity** world (inferred-integrity = documented STOP N6/N6b, unsettled) |
| **Claim ceiling** | Level (b)/(c) representational; no autopoiesis / subjectivity / consciousness claim |

**Implication for the two organism lineages:** the bridge verdict does **not**
touch the organism architecture matrix (§3–§7). It *confirms* two organism-derived
lessons at the neural level — D5 (the optimum is a level, not a switch) and the
AC109 rule (same information, mechanism must do causal work) — and adds two neural
demotions (D9 explicit-self-state unnecessary; D10 learned-adaptive-allocation
demoted) that Phase III must absorb before it is designed
(`ACI_MASTER_RESEARCH_TREE_v2.md` §4.3). The organism program is not reopened.

---

## 9. The Phase-III baseline (revised neural architecture after B + D) — added by G0

Phase III (N2 — recurrent cross-module availability of a maintained representation)
adopts the revised baseline recorded in `PHASE3_BASELINE_v1.md`. It is the bridge
architecture *after* the B + D verdict has stripped what failed: paid W persistence
remains (N1, the substrate), the explicit integrity state V is removed, the learned
allocator A is simplified to a fixed/reactive rule, and the two specialists are
retained as the two objective-distinct consumers N2 requires. The per-component
classification (the card's RETAIN / SIMPLIFY / REMOVE / DEFER / THEORY-SPECIFIC):

| Component | Classification | Reason (the rival that must fail if omitted) |
| --- | --- | --- |
| W — maintained representation | **RETAIN** | the N1 substrate; the shared content N2 is about (memoryless / pristine-backup rival) |
| V — self-resource / integrity state | **REMOVE** | B: P_rb (no V slot) matches; V re-encodes the readable age `d_t`; raw `(s,E,d)` suffices |
| A — maintenance controller | **SIMPLIFY** | D: a `(s,E,d)` threshold rule attains the oracle above the candidate; fixed/reactive is ALLOWED |
| S_pol — policy specialist | **RETAIN** | consumer 1 of W (finite-state / direct-control rival) |
| S_reg — regulation specialist | **RETAIN** (input simplified) | consumer 2 of W; reads W + `(s,E,d)`, not W + V (single-objective-collapse rival) |
| π — paid refresh | **RETAIN** | N1's mechanism; the paid write that holds W (pristine-backup rival) |
| GRU — recurrence | **RETAIN** | the substrate N1/N2 run on; free-permanence control runs it with W zeroed (F1) |
| Θ_slow — temporal continuity | **DEFER** | O1, Phase V; not part of the N2 baseline |

None of the eight is **THEORY-SPECIFIC** — attention (→O3/GWT), predictive coding
(→O2/PP), and differentiable memory (→O1) remain outside the core, as Q5's rows.
No component is retained for legacy: each RETAIN above is justified by the N2 claim
it serves and the named rival that must fail if it is omitted.

**Cross-lineage status.** This revised baseline is a *neural* lineage (like §8), not
an AC runner, and it does not touch the organism matrix (§3–§7). It inherits the
bridge's one surviving claim (N1, a substrate fact, shared by state-blind schedules)
and applies the two neural demotions (D9/D10) as negative design constraints. The
The organism program remains closed; no frozen organism number is re-read here.

---

## 10. The Phase-III result (Shared Latent Workspace + reduction rivals) — added by G16

The Phase-III lineage (§9's baseline) has now been **executed** and adjudicated OUTCOME C
(`PHASE3_VERDICT_v1.md`). It is the same *neural* lineage as §8/§9, distinct from both
organism lineages; its claim status is a matter of the Phase-III verdict, not of organism
evidence.

| Item | Phase-III workspace architecture (SLW + R1–R5, `phase3/` + frozen harness) |
| --- | --- |
| **Components** | candidate: GRU encoder → b-bit scalar W (quantized LLR) maintained by paid π, read by three objective-distinct specialists (S_pol/S_plan/S_reg), 393 params |
| **Rivals (one predicate removed each)** | R1 private copies (removes SHARED, 309 params); R2 monolith RNN (removes modularity, 1242); R3 raw history (removes compressed W, 3450); R4 sufficient-statistic broadcast (removes learned content + paid persistence, 0); R5 identical copies (removes the sharing mechanism, 0) |
| **What it was built to test** | N2 — one maintained, shared, b-bit content variable consumed by objective-distinct modules, with SHARED ∧ CAUSAL ∧ DISTINCT ∧ AVAILABLE ∧ MAINTAINED each load-bearing |
| **What it earned (frozen, G13/G14/G15)** | Per-arm probe acc over 12 seeds: candidate 0.9632 (worst), R1 0.9634, R2 0.9643, R4 0.9645, R5 0.9645, R3 0.9648. Candidate is **lowest on inference**. Sharing IS load-bearing for coordination (0 vs R1 0.014 incoherence, p=0.00049) and economy (1 vs 3 refresh targets, 32768 vs 98304 events) — but free via broadcast (R4/R5: 0 incoherence, 0 cost). Monolith beats at ~3× params (modularity = interpretability only). π-cut decay clean (0.9632→0.5000) but content carried free by a register. |
| **What it did NOT earn** | No workspace/encoder/shared-slot advantage; no modular-specialist advantage; no causal-intervention evidence (vacuous by construction — fixed functions of a scalar, candidate-only); no distinctness beyond fiat. |
| **Transferred w/o composition** | None — self-contained; the verdict is bounded to the fixed-cause i.i.d. token task where the sufficient statistic (scalar LLR) is closed-form. The acquired-statistic question is open. |
| **Claim ceiling** | Level (b)/(c) representational; no autopoiesis / workspace-seat / metacognition / consciousness claim. |

**The joint Phase-II + Phase-III teaching (for the whole matrix).** Two neural levels, one
verdict shape: the load-bearing object is the **availability of sufficient content**, not
the machinery around it. Phase II (B + D) stripped the explicit maintained self-state; Phase
III (C) stripped the shared maintained workspace. What survives both is N1 (paid persistence
as a necessary-condition substrate fact) plus the fact that a closed-form sufficient
statistic is carried for free by a broadcast/register. Answering the card's question —
expensive persistence / shared representation / explicit workspace / modular specialists /
sufficient-statistic availability / none — **only sufficient-statistic availability
survives as load-bearing in the tested low-dimensional tasks**; the rest is scaffolding
there (R2 monolith and R4/R5 broadcast match/beat the candidate). This confirms, at the neural level, the organism lessons D2
(more state not better), D5 (level not switch), AC109 (same info → mechanism must do causal
work), and P5 (encoding secondary). It does **not** touch the organism matrix (§3–§7); the
organism program remains closed.

## 11. Phase III-B transition (new question, not transferred evidence)

| Item | Status at H0 |
| --- | --- |
| Organism and Phase II/III lineages | Frozen; no Phase III-B result may be back-propagated into those studies |
| Falsified in Phase III | Learned maintained single-content slot adds no value over closed-form scalar broadcast; fixed consumer functions and candidate-only edits do not show exclusive causal organization |
| Surviving constraint | Suitable content can be made available to multiple consumers; paid persistence is a substrate fact only in the tested decay world |
| Open, not inherited | Acquired multi-factor state; binding information capacity; state-dependent occupancy; architectural value against fixed, private, unlimited and monolithic rivals |
| Claim ceiling | A bounded N2 organizational test; no consciousness or autopoiesis inference |

The G17 acquired-statistic question is a *forward question*, not a result.
`PHASE3B_TRANSITION_v1.md` narrows its proposed test to competing contents and
an actual bandwidth limit. A scalar sufficient statistic in the original
single-cause task must not be universalized to all learned latent worlds;
similarly, a trivial single-statistic broadcast must not be generalized into
"shared availability is never useful." H3 must show that the new limit really
forces a choice before any neural training is licensed.




