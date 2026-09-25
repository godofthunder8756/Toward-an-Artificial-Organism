# Evidence index v3 — authoritative baseline at HEAD add3bb5 (P0)

2026-09-24. Derived bookkeeping deliverable for the P0 card (t_84a11ca1): the
reconciled evidence state at HEAD `add3bb5` (P1/S1 manuscript + terminal synthesis),
separated into the five required items. Supersedes `EVIDENCE_INDEX_v2.md` (the N0
baseline at `77ace95`) and `BASELINE_v1.md` (the AC105-era baseline at `8f0218a`) as
the authoritative baseline; both are preserved unchanged as the record. No frozen
artifact (runner, protocol, results dir, hash, ledger) is edited, re-run, or re-hashed.
Seeds are the replication unit (N seeds × 2 histories = N independent units). Survival
is a bimodality-aware lower bound (AC68), never a per-seed-family guarantee. "Frozen" =
hashed protocol + results dir under `mkdir(exist_ok=False)` + audit (re-derives gates
without simulating) + replay (sampled exact reruns).

Reference architecture version: `57ca900` (+ working tree) — `S1_SYNTHESIS_v2.md`,
`C4_TASK_DESIGN_v1.md`, `AC109_ENGINEERING_v1.md`, `AC110_RESULTS_v1.md`,
`AC111_RESULTS_v1.md`, `P1_MANUSCRIPT_DRAFT_v1.md`, `AC113_RESULTS_v1.md` (P6),
`AC114_RESULTS_v1.md` (A3), `R1_AC113_REANALYSIS_v1.md`, `R2_P2_PROOF_CORRECTION_v1.md`,
`A4_EXCHANGE_VERDICT_v1.md`, `C0_FEASIBILITY_v1.md`.

**W0 reconciliation (2026-09-24, this revision).** This index is updated in place by W0
to carry the four R1/R2/A4/C0 results, and re-reconciled by W0 (t_f741e226) to carry the
I1/C1/I5/C3 corrections and results. In one sentence each: **R1** corrects AC113's
frozen F1 label from "equivalence" to **no demonstrated advantage** (the two histories
within a seed are byte-identical duplicates, so the seed-level sign-flip p is ≈ 0.71 /
0.63, n = 8, not the frozen n = 16); **R2** corrects the P2 proof's "irrationality"
reasoning while making the central result *stronger* (`N = ceil(logit θ/LR)` exact for
every θ under the matching `>=` convention) and discloses the AC112/113 scaffolding as
supplied limitations; **A4** resolves the A2 "supplied exchange interface" limitation at
the material layer — AC114 establishes boundary-mediated exchange plus reciprocal
production support, so the full two-clause criterion is limited by **one** modeling
declaration (the non-spatial controller), not three (I1: "supplied space" is permitted
substrate, struck from the limitation list); **C0** scopes the "reliability continuation"
as a second-order cognition track — under a label-free criterion "monitoring the
reliability of one's own estimate" is not identifiable separately from learning ε (a
first-order world parameter) or the first-order cause posterior **under the ideal-observer
assumption** — and **C1** corrects that scope (the AC architecture violates the assumption
by construction, so the tier is identifiable in principle as monitoring the *actual*
estimator; a named candidate question, not yet demonstrated); **I1** corrects the boundary
assessment (composition scoped to {W, C, B} in AC114; temporal window post-mortem; supplied
space is permitted substrate); **I5** issues the integrated organizational verdict (AC115:
six functions compose at the mechanism level, survival-level not confirmed); **C3** runs
the storage comparison (AC116: F1 no demonstrated income advantage over the tuned
memoryless rival; the storage line closes at the organism scale).

---

## The five items, recorded separately

### Item 1 — Organism-level evidence (frozen organism-scale studies)

These are the claims that rest on **frozen** organism-scale runs (hashed protocol,
`mkdir(exist_ok=False)` results dir, audit + replay). Four studies in the AC107–111
range are frozen; **AC109 is engineering-only** (no protocol, no freeze, no finals) and
is recorded in Item 2, not here — the task's parenthetical "(AC107–111 frozen studies)"
is corrected on this one point.

| Study | Card | Finals | Rows | Verdict | Gates |
| --- | --- | --- | --- | --- | --- |
| **AC107** | K6 | 6000–6007 | 240 | Partial confirmation: discrimination + storage maintenance confirm; content-causal and survival-advantage do NOT transfer | G1/G3/G4/G6/G7 pass; G2/G5 fail (recorded) |
| **AC108** | K7 | 6100–6107 | 288 | Both coupling directions confirmed, each by single-flag intervention | 7/7 pass |
| **AC110** | C3 | 6200–6207 | 96 | FALSIFICATION: ongoing repair NOT load-bearing for correctness/use in the decision window (correctness rides reacquisition); repair IS load-bearing for post-window storage (G4) | G1/G2/G3/G5 pass; G4 8/16 (recorded) |
| **AC111** | I1 | 6300–6307 | 144 | Composition: direct channels clean (reconstruction overwrite absent, spending starvation absent); full composition retains two failed gates (G3/G5 12/16) as a named behavioural interference | G1/G2/G4/G6 pass; G3/G5 12/16 (recorded) |
| **AC113** | P6 | 6400–6407 | 736/regime | **No demonstrated advantage (R1-corrected).** The maintained two-counter weighted estimate does not beat the single counter on post-cause income at the fixed engineering-selected parameters; the frozen F1 "equivalence" label is withdrawn (nonsignificance ≠ equivalence) | F1 recorded, now read as "no demonstrated advantage" (R1) |
| **AC114** | A3/A4 | 6500–6507 | 176 | **Boundary-mediated exchange, material layer.** Intake admitted at the local live-state of a produced gate link; the produced perimeter retains constituents and admits intake (`B → retention + exchange → production → B`); production closure over {W, C, B} only (I1 — the five-component K3 verdict does not transfer) | 6/6 (G1 inertness, G3/G4/G5 exchange, G6) |
| **AC115** | I3/I4 | 6600–6607 | 208 | **Integrated successor: exchange composes with the five-mechanism closure.** SR-2 admission gate on the AC105 architecture; six functions exercised in one organism; mechanism-level composition 16/16 (G1/G2/G3/G8); survival-level NOT confirmed (G4–G7 retained, seed-dependent) | G1/G2/G3/G8 16/16; G4 2/16, G5 2/16, G6 4/16, G7 6/16 (retained) |
| **AC116** | C3 | 6600–6607 | 240 | **F1 no demonstrated income advantage.** Maintained integer counter vs strongest tuned memoryless rival in the pure occluded-gate world (ε=0, q=0.9); counter weakly dominant (+200/seed, p=0.0625), real but income-invisible cut-safety edge; the storage line closes at organism scale | G1/G2/G3 pass; G4=F1 (recorded) |

The organism-level claims they establish, at the strongest wording the evidence earns:

- **AC107 — discrimination (0/32 mistakes).** The maintained one-bit cause-estimate
  reads E_machinery at the cut-window end 16/16 and E_world at the first drop 16/16,
  with **0 post-intervention mistakes across 32 final individuals**, transferring to the
  untouched family unchanged. Plus storage-maintenance in the content sense:
  observer-discard per-tick byte-identity 16/16 (value read from vulnerable maintained
  state, not host state) and no-cause identity 16/16 (estimate inert absent a cause).
- **AC108 — coupling, both directions.** Direction 1 (maintenance → accuracy/use):
  `no_write` leaves the estimate inaccurate 16/16 and mis-used (relinquishes a
  still-valid route on 4/8 seeds where the candidate holds), with the write actually
  cut. Direction 2 (content → adaptation/production/viability): `force_machinery`
  reverses the adaptation 16/16 (holds the stale route where the candidate relinquishes
  16/16) and collapses production/viability 16/16; `scramble` relinquishes a valid
  route on 4/8 seeds in the cut. Each effect is isolated by a single-flag intervention
  against the maintained candidate and fixed-threshold rivals (r2, r4).
- **AC110 — repair not load-bearing in the decision window; load-bearing for post-window storage.**
  Cutting the estimate's only repair path leaves correctness/use unchanged in the decision window
  (G2 16/16, G3 16/16, G5 48/48); correctness rides reacquisition (`bel_write` at open contacts), not
  repair. The repair path is unreachable in the window *under the frozen ambient 1e-4 damage* (one bit
  contributes ≤3 minority replicas and can never trigger the whole-bank obs-bit-2 trigger on its own,
  which needs ≥4 over 126 bits, and ambient program damage accumulates too slowly within 96 ticks —
  action 2 fires 0 times in the window). This is conditional, not absolute: damage *elsewhere* in the
  program at an elevated rate would fire action 2, which also restores the estimate bit (it is part of
  bank 0). The repair cut's only effect is a seed-dependent, decision-irrelevant post-window storage
  drift (G4 8/16, the Binomial(7,~0.55) coin flip): repair *is* load-bearing for post-window storage
  protection (maintained holds 16/16; no_repair drifts to majority-1 in 8/16).
- **AC111 — composition, direct channels clean; full composition retains two failed gates.** The
  cognitive mechanism composes with AC105's reconstruction + spending on its two *direct* channels:
  reconstruction never overwrites the estimate bit (the `bel_off` exclusion from `reg_from_active` is
  load-bearing and verified under a live reconstruction), and the allowance-42 budget never starves
  reacquisition — a property of the spending *policy* (the allowance defers only `reg_from_active`;
  `bel_write` is W-gated not allowance-gated), not evidence that the decision write and reconstruction
  do not compete for the shared material/energy/W pools. The full composition is not established: two
  prespecified gates fail and are retained (G3 12/16, G5 12/16) as a named seed-dependent behavioural
  interference (the corrupted contact rule re-schedules reacquisition on 6306/6307), survival-neutral
  and absent from engineering seeds.
- **AC113 — weighted (heterogeneous) generalization: no demonstrated advantage (R1-corrected).**
  At the fixed engineering-selected parameters the maintained two-counter is statistically
  indistinguishable from the single counter on post-cause income (seed-level sign-flip p ≈ 0.71 /
  0.63, n = 8, median difference 0, the negative mean driven by one collapse seed), and the candidate
  is worse on survival (a candidate-only collapse seed), expenditure (~2× `counter_writes`), and cut
  false-relinquish. The frozen F1 "equivalence" label is withdrawn (nonsignificance ⇒ equivalence is the
  fallacy R1 corrects); the result is "no demonstrated advantage," not equivalence and not capability
  falsification. The load-bearing object remains decisive-observation handling plus a counter threshold,
  not a graded register.
- **AC114 — boundary-mediated exchange at the material layer (A4, I1-corrected).** Intake is admitted at the *local*
  live-state of a produced gate link (site gate, not aggregate count), and the same produced links that
  retain the constituents admit the intake that funds production — a `B → retention + exchange →
  production → B` cycle established by ablation, not assertion. This resolves the A2 "supplied exchange
  interface" limitation at the material layer; the full two-clause criterion remains NOT ESTABLISHED for
  the whole organization, limited by **one** modeling declaration (the non-spatial controller — I1:
  supplied space is permitted substrate, not a limitation). Production closure in AC114 is over {W, C, B}
  only; the five-component K3 verdict does not transfer (I1 composition correction).
- **AC115 — integrated successor (I5): exchange composes with the five-mechanism closure at the
  mechanism level.** The SR-2 admission gate is composed with the AC105 five-mechanism architecture in one
  organism (finals 6600–6607, 208 rows): G1 byte-identity to AC105 at the intact boundary, G2 link-specific
  and G3 local admission, and all six functions (exchange admission, retention, renewal, reconstruction,
  succession, paid updates) exercised in the same individuals (keep arm 16/16). **Mechanism-level composition
  SUPPORTED; survival-level NOT confirmed** (G4–G7 fail on a minority of finals and are retained — seed-dependent
  AC68/AC39). Production closure (clause i, five-component) stands SUPPORTED and unchanged; clause (ii) remains
  NOT ESTABLISHED, limited solely by the non-spatial informational core.
- **AC116 — storage comparison (C3): F1 no demonstrated income advantage.** In the pure occluded-gate world
  (ε=0, q=0.9) the maintained integer counter does not demonstrate a significant post-cause income advantage
  over the strongest tuned memoryless rival (mean +200/seed, exact sign-flip p=0.0625; weakly dominant, never
  worse). Its accumulation is causally effective (G3) and its open-blind latch buys a real but income-invisible
  cut-safety edge (4/16 vs 16/16 false relinquishments). The storage line **closes at the organism scale**
  without erasing AC107's content-role, AC108's acquisition-necessity, AC110's repair-dependence, or AC113's
  single-counter sufficiency.

**Survival caveat, attached to every organism-level claim (not a footnote).** No
survival-advantage claim for the estimate is earned: AC107 Q4 is seed-bounded (move
14/16 vs r4 10/16, both die on 6002; no cut-side edge), and AC108's survival reversal is
**12/16** (candidate survives 12/16 where `force_machinery` dies 16/16), distinct from
the 16/16 *adaptation* reversal. The candidate's own move deaths are the re-acquisition
boundary (AC83/AC74), an operating-range limit, not a coupling failure. Survival is
reported as a bimodality-aware lower bound throughout; no survival claim is made for the
representation.

### Item 2 — Mathematical / harness-level proposals (design + decision-theoretic, no frozen organism-scale run)

These are the claims that are **not** organism-scale frozen results. They are
demonstrated at the harness/decision-theoretic/engineering level, and none may be cited
as "the organism does X."

- **C4 — graded-posterior (first-order uncertainty) probe** (`C4_TASK_DESIGN_v1.md`,
  `_c4_uncertainty_probe.py` / `_c4_uncertainty_pareto.py`, run). The graded Bayesian
  posterior over the cause is **calibrated** (binned confidence tracks the empirical
  error rate: 0.7–0.8 → 0.748 correct, 0.9–1.0 → 1.000 correct). Its advertised "strict
  dominance" over heuristics was a **rival defect, not a property of gradedness** (P2):
  fixing the one omitted decisive observation in the strongest rival makes it bit-for-bit
  the graded policy, and the graded posterior is computationally equivalent to an integer
  ambiguous-failure counter (`N = ceil(logit θ/LR)`, exact for every θ under the matching
  `>=` convention — R2). Mechanism: likelihood-ratio weighting with constant
  LR = log(4/3) ≈ 0.288. **This is a decision-theoretic demonstration of the observation
  process, not an organism's behaviour.** The organism-scale continuation (AC113, P6) ran
  and — corrected by R1 — showed **no demonstrated advantage** for the
  heterogeneous-weighting generalization (see Item 1); a maintained integer counter
  suffices.
- **C2 — task design + identifiability demonstration** (`C2_TASK_DESIGN_v1.md`,
  `_c2_identifiability.py`, run). Occluding the `used_held` observation on a Bernoulli(q)
  fraction of contacts makes the two causes produce an identical current observation
  `(bound=1, used_held=occluded, productive=0)` while their histories differ, so a
  maintained accumulator of the last open-gate conclusion is load-bearing. Identifiability
  is demonstrated by a hold-and-observe harness against the frozen modules, not assumed.
- **K4 — task identifiability** (analysis + diagnostic harness, no study). The two causes
  produce disjoint action-observation histories on the organism's own `(bound, used_held,
  productive)` triple (F1 held-fail one-sided ⇒ E_world; F2 resumption two-sided ⇒
  E_machinery). A task-property demonstration, not a single-flag causal intervention.
- **AC109 — direct-diagnostic rival (C1)** (`AC109_ENGINEERING_v1.md`, engineering seeds
  0–7, no freeze). The direct diagnostic (reads the triple transiently, no stored
  estimate) matches the stored-estimate candidate on 48/48 behavioural cells, while the
  stored estimate costs more (a 7-replica write plus ~100 redundant proactive renewals).
  Verdict: **storage inert, content load-bearing** — the estimate's causal role is as a
  content *selector*, not a memory. Engineering-only; a run, but not frozen.
- **C0 — reliability-identifiability verdict** (`C0_FEASIBILITY_v1.md`,
  `_c0_reliability_identifiability.py`, run). The "reliability continuation" is **not
  identifiable** as a second-order cognition mechanism **under the ideal-observer
  assumption**: under a label-free criterion,
  "monitoring the reliability of one's own estimate" collapses to (a) learning the
  channel parameter ε (a first-order world parameter) or (b) a function of the sufficient
  statistic (n_u, n_p) (the first-order cause posterior); the third self-referential
  reading is the already-answered substrate question (AC110). No probe run (none
  authorized). The residue is a first-order parameter-learning question — acquire and
  maintain a graded estimate of ε and beat a stale/supplied weight — framed as parameter
  learning, never as reliability monitoring.
- **C1 — reliability disposition correction** (`C1_RELIABILITY_DISPOSITION_v1.md`,
  reanalysis, no run). C0's collapse is **valid only under the ideal-observer assumption**,
  which the AC architecture violates by construction (damaged, resource-constrained,
  sometimes-wrong estimate, spatially/temporally separated from its maintenance machinery —
  the conditions the metacognition literature identifies for a distinct second-order
  computation). The corrected disposition is **"identifiable in principle as a question
  about monitoring the actual estimator"**, delivered as a discriminating candidate
  question (content = maintenance bookkeeping; dissociable from the estimate by selective
  damage; causal role on the maintenance direction). **Not yet demonstrated, not
  authorized.** Retained: estimating ε alone does not establish metacognition.

The common status: these are **proposals/measurements of the task and the decision
problem**, each demonstrated at the harness level before (or instead of) any organism-
scale question. Their headline discipline is the C4 §13 boundary — at q → 0 the estimate
is unnecessary and heuristics match (the correct non-vacuous control, not a weakness).

### Item 3 — Earlier-architecture evidence (the AC10–AC95 ablation/turnover record)

This is the autonomy track's accumulated record, **inherited by the current account and
not re-tested by AC105/AC107/AC108/AC110/AC111** (K3 §1 states this explicitly). The
accepted capability ledger:

- **Foundational body (AC1–AC10).** AC1 controller pays for its own repair (+
  confirmatory AC1–AC4, fresh seeds 5100–5507); AC2 produced W catalysts; AC3 produced C
  converters (2/3 rates in confirmatory); AC4 produced B boundary + measured transport;
  AC9 controls v3 (developmental allocation + broad controls); AC10 every constituent
  dependency isolated (no-W/no-C/no-B/retention-rescue/external-B, 9/9 gates).
- **Acquisition/adaptation (AC15–AC75).** AC15 graded access law; AC18 two-way
  relinquish/restore; AC67 repair load-bearing under sticky damage; AC71 majority-read
  register closes the closure triplet; AC75 erase-on-relinquishment makes the closure
  world-accommodating.
- **Internal-state milestone (AC76–AC89).** AC76 controller turnover from a
  corruption-immune description; AC79 description maintenance; AC80 internalized
  reconstruction recipe; AC81 component replacement (turnover accounting); AC84
  unconditional turnover floor; AC85 stored bank-rule convention; AC86 recipe-storage
  succession; AC87/88/89 integrated successor (succession controller state in maintained
  substrate, order-preserving decode, simultaneous + adversarial challenge).
- **Production dependencies (AC91–AC95).** AC91 W production load-bearing for viability
  + maintenance capacity; AC92 functional interruption-and-rescue; AC93 coordinator
  transition write W-gated; AC94 coherent resumable succession; AC95 state sufficiency
  (observer-discard endpoint equivalence).

**Boundary note (carried, not hidden).** AC96–AC105 is **not** an "earlier architecture"
in the ablation sense — it is the *current* autonomy architecture. AC96 (internalized
streak), AC99 (Gray encoding), AC100 (2×2 factorial isolates Gray, not reserve), AC103
(persistent reconstruction trigger), AC104/AC105 (allowance-42 budget) establish **level
(b) adaptive autonomy — ESTABLISHED**, one of the three paper-ready claims, and AC105 is
the reference body on which K3 issued the level-(a) closure verdict (Item 4). The
task's "(AC10–95 ablations)" range is honoured exactly: AC10–AC95 is the inherited
ablation/turnover/production record; AC96–AC105 is the current autonomy line.

**Negative / falsified ledger (do not inherit as capabilities):** AC11 (state-blind duty
cycle beats adaptive arm), AC13/AC14 (self-reversing damage), AC16/17 (gate-shape),
AC97/98 (reserve withholds/starves the decision it funds), AC102/103 (the *distinction*
stands, no universal spending policy), AC106 (engineering negative, superseded in scope
by K1–K9).

### Item 4 — Conclusions conditional on the supplied substrate

The following are **not** substrate-free results; each carries the "conditional on the
supplied substrate" classification and must be quoted with it.

- **Level (a) production closure — SUPPORTED, bounded (K3 `CLOSURE_VERDICT_v1.md`).**
  Every necessary component {W, C, B, description, derived program} satisfies C1–C5 and
  the maintained state {pointer, coordination, route memory, decision state} satisfies
  S1–S4, forming a single strongly-connected production-dependency network with no
  external root — *within the declared model and operating range, under the accepted
  substrate convention*. **J1 = substrate (resolved)**: `prog.choose` (interpretation)
  and `advance()` (succession semantics) are supplied substrate, a modeling choice, not
  a measurement. Not "autopoietic" unqualified; not "alive."
- **Full autopoiesis criterion (M&V clauses i + ii) — NOT ESTABLISHED (A2 + A4 + I5).** Clause
  (i) is supported; clause (ii) spatial unity is met only at the **material (constituent)
  layer** and is limited by **one** modeling declaration, not an empirical gap: the
  controller is non-spatial (I1 correction — "the space is supplied" is **permitted
  substrate**, struck from the limitation list; every formalization bottoms out in supplied
  laws). The former third limitation — the
  exchange interface supplied and not boundary-mediated (B a pure retention wall) — is
  **resolved at the material layer** by AC114 (A4): intake is admitted at the local
  live-state of a produced gate link, so the produced perimeter retains constituents
  *and* mediates the intake that funds production. What remains supplied is the admission
  reaction form (the gated `react` actions 0/1) and the gate associations; the exchange
  *function* is boundary-mediated, its *law* is supplied. The substitution fact is struck
  from the verdict (A2 correction: a rescue control that substitutes boundary supply
  *identifies* the function, it does not refute it). **AC115 (I5) then shows the exchange
  role composes with the five-mechanism closure in one organism at the mechanism level**
  (G1 byte-identity, G2/G3 admission discrimination, all six functions exercised 16/16);
  the four survival-bundled gates (G4–G7) are retained as failures (seed-dependent). Moving
  clause (ii) further — a spatial realization of the informational core — requires a
  re-architecture, not an in-model run.
- **A1 realization ledger.** The four operational-state items {pointer, coordination,
  route memory, decision state} are each **(b) explicit substrate provision** for their
  *storage medium* (the development-allocated `traces`/`mem.Memory` arrays) plus
  **maintained state (S1–S4)** for their *value*. None is a produced component; none is an
  unaccounted dependency. The storage arrays themselves are supplied substrate (§5's
  definitional amendment), never re-allocated during life.
- **The substrate inventory, named** (charter v2 §5 + A1): `prog.choose` (14-bit rule
  interpreter), `advance()` (succession transition logic), the decode format, the
  observation function, the conservation laws, the damage model, the tick clock, the
  world constants, and the storage arrays (`traces (4,1024,7)`, `mem.Memory (2,2,3,7)`,
  `boundary[20]`) allocated at development by `acquire()`.

**Rule for downstream docs:** any level-(a) or closure citation must carry "within the
declared model and operating range, under the accepted substrate convention," and no
downstream doc may cite the full two-clause criterion as satisfied or "spatial unity
unresolved because substitutable" (that phrase is now wrong — A2).

### Item 5 — Work completed after the reported N-program

The "reported N-program" is the planning-phase baseline reported at `b97388e`
("N0/N1/A1/A2: baseline + scope corrections + autopoiesis accounting"; the N0 evidence
index at HEAD `77ace95` plus the N1/A1/A2 corrections). The work completed **after** it,
in commit order, is now folded into this baseline and leaves **no unincorporated work**:

| Commit | Deliverable | Card | Status in this baseline |
| --- | --- | --- | --- |
| `d7e24fa` | `AC109_ENGINEERING_v1.md` | C1 | Item 2 (engineering, direct-diagnostic equivalence) |
| `6875f38` | `C2_TASK_DESIGN_v1.md`, `C4_TASK_DESIGN_v1.md` | C2, C4 | Item 2 (harness-level designs + probes) |
| `928b938` | `AC110_RESULTS_v1.md` (frozen 6200–6207) | C3 | Item 1 (repair falsified) |
| `6b5f163` | `AC111_RESULTS_v1.md` (frozen 6300–6307) | I1 | Item 1 (composition supported, named interference) |
| `add3bb5` | `P1_MANUSCRIPT_DRAFT_v1.md`, `S1_SYNTHESIS_v2.md` | P1, S1 | The terminal synthesis (below) |
| `57ca900` | `AC113_RESULTS_v1.md` (frozen 6400–6407) + `A0_SUCCESSOR_SPEC_v1.md` (SR-1) | P6, A0 | Item 1 (AC113, R1-corrected); the A-track successor spec (SR-1, superseded by SR-2) |
| (working tree) | `R1_AC113_REANALYSIS_v1.md`, `R2_P2_PROOF_CORRECTION_v1.md` | R1, R2 | Corrections folded into Items 1/2 (AC113 F1 → no demonstrated advantage; P2 proof reasoning corrected) |
| (working tree) | `A1_EXCHANGE_SPEC_v1.md` (SR-2), `ac114.py`, `AC114_RESULTS_v1.md` (frozen 6500–6507), `A4_EXCHANGE_VERDICT_v1.md` | A1–A4 | Items 1/4 (boundary-mediated exchange at the material layer) |
| (working tree) | `C0_FEASIBILITY_v1.md` | C0 | Item 2 (reliability tier not identifiable under the ideal-observer assumption) |
| (working tree) | `I1_BOUNDARY_CORRECTION_v1.md` | I1 (boundary) | Items 1/4 (composition scoped to {W,C,B}; supplied space permitted substrate; temporal window post-mortem) |
| (working tree) | `C1_RELIABILITY_DISPOSITION_v1.md` | C1 (reliability) | Item 2 (C0 collapse valid only under the ideal-observer assumption; tier re-opened to a named candidate question, not authorized) |
| (working tree) | `I2_INTEGRATED_EXCHANGE_DESIGN_v1.md`, `ac115.py`, `AC115_RESULTS_v1.md` (frozen 6600–6607), `I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` | I2–I5 | Items 1/4 (exchange composes with the five-mechanism closure at the mechanism level; survival-level not confirmed) |
| (working tree) | `C2_STORAGE_COMPARISON_v1.md`, `ac116.py`, `AC116_RESULTS_v1.md` (frozen 6600–6607) | C2 (storage), C3 (storage) | Item 1 (F1 no demonstrated income advantage; storage line closes at organism scale) |

The terminal synthesis (`S1_SYNTHESIS_v2.md`) is the reconciled account that the
`d7e24fa`–`add3bb5` post-N deliverables feed. The later work (`57ca900` and the
working-tree R1/R2/A1–A4/C0 deliverables) is reconciled by this W0 revision, which folds
them into Items 1/2/4 above; the next terminal synthesis (S0) is the child of this task
and has not yet run. Nothing outside the reconciled account remains: the working-tree
underscore-prefixed probe scripts (`_r1_*`, `_r2_*`, `_c0_*`, `_a1_*`…`_a3_*`) are
supporting engineering scratch, not new claims and not frozen.

---

## The reconciled verdict (one paragraph)

Two tracks, one reconciled account. The **autonomy** track is **stable within the current model** (its
verdicts do not change for any experiment inside the model — moving them requires a re-architecture,
not a run): production closure (M&V clause i) is SUPPORTED within the declared model and operating range
under the accepted substrate convention, and the full two-clause autopoiesis criterion is NOT
ESTABLISHED for a reason that is a modeling limitation — now **one** concrete limit (the non-spatial
controller; supplied space is permitted substrate, I1), with the third (supplied exchange interface)
resolved at the material layer by AC114 (A4) and the exchange role shown to compose with the
five-mechanism closure at the mechanism level by AC115 (I5; survival-level composition not confirmed) —
not an empirical gap. The **cognition** track is characterized, not exhausted: a maintained
one-bit cause-estimate is acquired from the organism's own observations, discriminates two causes at
ceiling accuracy (0/32 mistakes), and is causally coupled to its maintenance (the paid acquisition/update
write) in both directions — but its persistence is inert where the current observation is decisive in the
clean task (C1/AC109), its ongoing repair is not load-bearing for correctness/use in the decision window
(C3/AC110; repair is load-bearing for post-window storage, G4), and its weighted (heterogeneous)
generalization shows **no demonstrated advantage** over a single counter at organism scale (AC113; R1),
and its maintained-storage half shows **no demonstrated income advantage** over the strongest tuned
memoryless rival (AC116; C3, F1) — the storage line closes at the organism scale without erasing the
content-role/acquisition-necessity/repair-dependence/single-counter results.
The reliability (second-order) tier is **not identifiable as a separable mechanism under the
ideal-observer assumption** (C0); C1 corrects that scope — the AC architecture violates the assumption
by construction, so the tier is **identifiable in principle as a question about monitoring the actual
estimator** (a named candidate question, not yet demonstrated). Neither a breakthrough nor exhaustion
is claimed.

Three paper-ready claims (P1): (1) level (a) production closure, SUPPORTED bounded with
the A2 boundary correction and the A4 exchange extension (boundary-mediated exchange at
the material layer; scoped by I1 to {W, C, B} in AC114, five-component verdict with AC105,
and composed with the exchange role by AC115/I5 at the mechanism level); (2) level (b)
adaptive autonomy, ESTABLISHED (AC99–AC105); (3) level
(c) representational coupling — a maintained one-bit cause-estimate discriminates two
causes at ceiling accuracy and is causally coupled to its maintenance machinery in both
directions, with the survival caveat attached. Its generalization to graded/weighted
form is NOT a paper-ready claim (AC113: no demonstrated advantage), and its maintained
storage is NOT a paper-ready advantage (AC116/C3: F1 no demonstrated income advantage).
Not supportable:
"autopoietic" unqualified, "alive", "self-sustaining", "conscious", "metacognitive",
any survival-advantage claim for the estimate, any reliability-monitoring claim as a
*distinct* mechanism (C0's scoped non-identifiability survives; C1 re-opens the tier to a
named, untested candidate question).

---

## Evidence index (claim → tier → frozen study → verdict)

| Claim | Tier | Evidence | Verdict |
| --- | --- | --- | --- |
| Production closure (level a) | Substrate-conditional (Item 4) | K3 + A2 (B re-confirmed C1–C5) + A1 ledger + A4 (exchange mediated at the material layer) + I5 (AC115 composition) | SUPPORTED, bounded |
| Full autopoiesis criterion (i + ii) | Substrate-conditional (Item 4) | A2 + A4 + I5 | NOT ESTABLISHED (i supported; ii met at the material layer only — the non-spatial controller; supplied space is permitted substrate, I1) |
| Boundary-mediated exchange | Organism (Item 1) | AC114 (A4, site gate, 16/16) | ESTABLISHED at the material layer (retention + exchange on the one produced structure) |
| Exchange composes with closure | Organism (Item 1) | AC115 (I5, G1/G2/G3/G8 16/16) | SUPPORTED at the mechanism level; survival-level NOT confirmed (G4–G7 retained) |
| Adaptive autonomy (level b) | Earlier/current autonomy (Item 3, AC96–105) | AC99–AC105 | ESTABLISHED |
| Diagnostic acquisition + discrimination | Organism (Item 1) | AC107 (0/32 mistakes) | SUPPORTED |
| Coupling, both directions | Organism (Item 1) | AC108 (7/7 gates) | SUPPORTED |
| Persistent history (clean world) | Harness/engineering (Item 2) | AC109 (48/48 equivalence) | FALSIFIED (storage inert) |
| Persistent history (gated world) | Harness (Item 2) | C2 identifiability | SUPPORTED-by-design |
| Maintained storage (gated world) | Organism (Item 1) | AC116 (C3, F1) | no demonstrated income advantage over tuned memoryless rival (storage line closes at organism scale) |
| Ongoing repair dependence | Organism (Item 1) | AC110 (G4 8/16) | not load-bearing in the decision window; load-bearing for post-window storage |
| First-order uncertainty | Harness/mathematical (Item 2) | C4 probe + P2/R2 + AC113 (R1) | graded posterior == integer counter (P2/R2); heterogeneous weighting: no demonstrated advantage at organism scale (AC113/R1) |
| Reliability (second-order) | Harness (Item 2) | C0 + C1 | NOT IDENTIFIABLE under the ideal-observer assumption (C0); identifiable in principle as monitoring the actual estimator (C1) — a named candidate question, not yet demonstrated |
| Composition with autonomy | Organism (Item 1) | AC111 (G3/G5 12/16) | direct channels clean; full composition not established (gates retained) |
| Comparative performance / viability | Organism (Item 1) | AC107/108/109/113 | Partial (content load-bearing; survival seed-bounded; weighted form no advantage) |

**Unsupported (the record does not earn these, and no downstream doc may inherit them):**
unqualified "autopoietic"/"alive"/"self-sustaining"; full two-clause autopoiesis; any
survival-advantage claim for the cause-estimate; any reliability/meta-monitoring claim as
a *demonstrated* distinct mechanism; "first demonstrated" beyond this project's lineage;
"sustained representation-repair coupling" (N1 point 3, C3).

---

## Disposition after R1/R2/A4/C0 (the next question is S0's to choose)

The previously chosen next step — the graded-posterior (first-order uncertainty)
organism-scale study — has now **run** (AC113, P6) and its outcome, corrected by R1, is
**no demonstrated advantage**: at the fixed engineering-selected parameters the maintained
two-counter is statistically indistinguishable from the single counter on post-cause income
(seed-level sign-flip p ≈ 0.71 / 0.63, n = 8), and the candidate is worse on survival,
expenditure, and cut false-relinquish. The frozen F1 "equivalence" label is withdrawn; the
result is "no demonstrated advantage," not equivalence and not capability falsification.

The named next-after — the reliability (second-order `P_YIELD`) tier — is **scoped, not closed**
(C0), and **C1 corrects the scope**: under a label-free criterion *and the ideal-observer
assumption* it is not identifiable separately from learning ε (a first-order world parameter)
or the first-order cause posterior; but the AC architecture violates that assumption by
construction, so the tier is **identifiable in principle as a question about monitoring the
actual estimator** — delivered as a discriminating candidate question (C1 §3), **not yet
demonstrated and not authorized**. Estimating ε alone still does not establish metacognition.

The autonomy track moved: the SR-1/SR-2 boundary-exchange successor was built and frozen
(AC114, A1–A4), establishing boundary-mediated exchange at the material layer, and the
**integrated successor** (AC115, I3–I5) showed the exchange role composes with the five-mechanism
closure in one organism at the **mechanism level** (survival-level not confirmed, G4–G7 retained).
The full two-clause criterion is now limited by **one** modeling declaration (the non-spatial
controller; supplied space is permitted substrate — I1), not three.

The storage comparison (AC116, C3) ran the C2-named contrast and returned **F1 no demonstrated
income advantage** over the strongest tuned memoryless rival — the storage line closes at the
organism scale without erasing AC107/108/110/113.

The strongest justified next question, its cost, and its falsification risk are S0's
deliverable (the child of this task). Open continuations on record, any of which S0 may
choose: (1) the C1 candidate question (monitoring the actual estimator — a stored, maintained,
flexibly-consumed second-order state dissociable from the estimate), gated on an estimate that
is sometimes wrong for implementation reasons; (2) three-cause integration (corruption as a third
cause) and the re-acquisition boundary; (3) the AC110 longer-horizon/second-cause world and the
ongoing-repair isolation (kept out of AC116's scope). The autonomy track's verdicts are stable
within the current model — moving clause (ii) further requires a re-architecture (a spatial
realization of the informational core), not an in-model run. Neither breakthrough nor exhaustion
is claimed.

---

## Sources

`S1_SYNTHESIS_v2.md`, `P1_MANUSCRIPT_DRAFT_v1.md`, `C4_TASK_DESIGN_v1.md`,
`C2_TASK_DESIGN_v1.md`, `AC109_ENGINEERING_v1.md`, `AC110_RESULTS_v1.md`,
`AC111_RESULTS_v1.md`, `AC107_RESULTS_v1.md`, `AC108_RESULTS_v1.md`,
`N1_CORRECTIONS_v1.md`, `A1_REALIZATION_LEDGER_v1.md`, `A2_BOUNDARY_VERDICT_v1.md`,
`CLOSURE_VERDICT_v1.md` (K3), `DEFINITIONS_CHARTER_v2.md` (K2), `K9_SYNTHESIS_v1.md`,
`K8_DISPOSITION_v1.md`, `AC105_RESULTS_v1.md` / `AC105_PROTOCOL_v1.md`,
`AC113_RESULTS_v1.md` / `AC113_PROTOCOL_v1.md` (P6), `R1_AC113_REANALYSIS_v1.md`,
`R2_P2_PROOF_CORRECTION_v1.md`, `AC114_RESULTS_v1.md` / `AC114_PROTOCOL_v1.md` (A3),
`A4_EXCHANGE_VERDICT_v1.md`, `A1_EXCHANGE_SPEC_v1.md` (SR-2), `C0_FEASIBILITY_v1.md`,
`I1_BOUNDARY_CORRECTION_v1.md`, `C1_RELIABILITY_DISPOSITION_v1.md`,
`I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md`, `I2_INTEGRATED_EXCHANGE_DESIGN_v1.md`,
`AC115_RESULTS_v1.md` / `AC115_PROTOCOL_v1.md` (I3/I4),
`AC116_RESULTS_v1.md` / `AC116_PROTOCOL_v1.md` (C3), `C2_STORAGE_COMPARISON_v1.md`,
`ARCHITECTURE_BY_CLAIM_MATRIX_v1.md` (I0),
`EVIDENCE_INDEX_v2.md`, `BASELINE_v1.md`, `P3_CORRECTIONS_v1.md`. Frozen dirs: `ac105_results_v1` (160 rows),
`ac107_results_v1` (240 rows), `ac108_results_v1` (288 rows), `ac110_results_v1`
(96 rows), `ac111_results_v1` (144 rows), `ac113_results_v1` /
`ac113_results_v1_eps002` (736 rows each), `ac114_results_v1` (176 rows),
`ac115_results_v1` (208 rows), `ac116_results_v1` (240 rows). This index is
derived and is not hashed into any study's `pre_run_snapshot.json`.
