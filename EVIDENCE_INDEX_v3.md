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

Reference architecture version: `add3bb5` — `S1_SYNTHESIS_v2.md`,
`C4_TASK_DESIGN_v1.md`, `AC109_ENGINEERING_v1.md`, `AC110_RESULTS_v1.md`,
`AC111_RESULTS_v1.md`, `P1_MANUSCRIPT_DRAFT_v1.md`.

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
  error rate: 0.7–0.8 → 0.748 correct, 0.9–1.0 → 1.000 correct) and **strictly
  dominates** every ordinary heuristic (raw counter, binary, binary+imm — the strongest,
  not a strawman) on the defer-vs-act tradeoff, dominance growing in the incomplete-
  evidence regime (min-mean regret q=0.7: 0.884 vs 0.995; q=0.9: 1.359 vs 1.744).
  Mechanism: likelihood-ratio weighting (decisive observations act immediately; weak
  occluded-unproductive evidence accumulates slowly, LR = log(4/3) ≈ 0.288). **This is
  a decision-theoretic demonstration of the observation process, not an organism's
  behaviour.** The first-order estimate is SUPPORTED-by-design; the organism-scale run
  is the authorized, still-unrun continuation (Item 5 / next step).
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
- **Full autopoiesis criterion (M&V clauses i + ii) — NOT ESTABLISHED (A2).** Clause (i)
  is supported; clause (ii) spatial unity is met only at the constituent-retention level
  and is limited by three modeling declarations, none an empirical gap: (a) the space is
  supplied; (b) the exchange interface is supplied and not boundary-mediated (B is a pure
  retention wall, not a semipermeable membrane); (c) the controller is non-spatial. The
  substitution fact is struck from the verdict (A2 correction: a rescue control that
  substitutes boundary supply *identifies* the function, it does not refute it). No child
  experiment moves the verdict — it requires changing the supplied physics.
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

The terminal synthesis (`S1_SYNTHESIS_v2.md`) is the reconciled account that these
post-N deliverables feed, and its verdict and next step are reproduced in the next two
sections. There is no work after the N-program that remains outside the reconciled
account: `add3bb5` is HEAD, and the untracked files in the working tree are engineering
scratch (underscore-prefixed probe scripts, `ac110/ac111` smoke dirs, run logs) — not
new claims and not frozen.

---

## The reconciled verdict (one paragraph)

Two tracks, one reconciled account. The **autonomy** track is **stable within the current model** (its
two verdicts do not change for any experiment inside the model — moving them requires a re-architecture,
not a run): production closure (M&V clause i) is SUPPORTED within the declared model and operating range
under the accepted substrate convention, and the full two-clause autopoiesis criterion is NOT
ESTABLISHED for a reason that is a modeling limitation (three concrete limits — supplied space, supplied
exchange interface, non-spatial controller — not "supplied space" alone), not an empirical gap. The
**cognition** track is characterized, not exhausted: a maintained one-bit cause-estimate is acquired from
the organism's own observations, discriminates two causes at ceiling accuracy (0/32 mistakes), and is
causally coupled to its maintenance (the paid acquisition/update write) in both directions — but its
persistence is inert where the current observation is decisive in the clean task (C1/AC109), its ongoing
repair is not load-bearing for correctness/use in the decision window (C3/AC110; repair is load-bearing
for post-window storage, G4), and its first-order uncertainty generalization is discriminating by design
but untested organism-scale (C4). The next bounded step is to write up the three paper-ready claims and
authorize one named continuation (among several open continuations on record): the graded-posterior
(first-order uncertainty) organism-scale study. Neither a breakthrough nor exhaustion is claimed.

Three paper-ready claims (P1): (1) level (a) production closure, SUPPORTED bounded with
the A2 boundary correction; (2) level (b) adaptive autonomy, ESTABLISHED (AC99–AC105);
(3) level (c) representational coupling — a maintained one-bit cause-estimate
discriminates two causes at ceiling accuracy and is causally coupled to its maintenance
machinery in both directions, with the survival caveat attached. Not supportable:
"autopoietic" unqualified, "alive", "self-sustaining", "conscious", "metacognitive",
any survival-advantage claim for the estimate, any reliability-monitoring claim.

---

## Evidence index (claim → tier → frozen study → verdict)

| Claim | Tier | Evidence | Verdict |
| --- | --- | --- | --- |
| Production closure (level a) | Substrate-conditional (Item 4) | K3 + A2 (B re-confirmed C1–C5) + A1 ledger | SUPPORTED, bounded |
| Full autopoiesis criterion (i + ii) | Substrate-conditional (Item 4) | A2 | NOT ESTABLISHED (i supported; ii modeling-limited) |
| Adaptive autonomy (level b) | Earlier/current autonomy (Item 3, AC96–105) | AC99–AC105 | ESTABLISHED |
| Diagnostic acquisition + discrimination | Organism (Item 1) | AC107 (0/32 mistakes) | SUPPORTED |
| Coupling, both directions | Organism (Item 1) | AC108 (7/7 gates) | SUPPORTED |
| Persistent history (clean world) | Harness/engineering (Item 2) | AC109 (48/48 equivalence) | FALSIFIED (storage inert) |
| Persistent history (gated world) | Harness (Item 2) | C2 identifiability | SUPPORTED-by-design |
| Ongoing repair dependence | Organism (Item 1) | AC110 (G4 8/16) | not load-bearing in the decision window; load-bearing for post-window storage |
| First-order uncertainty | Harness/mathematical (Item 2) | C4 probe | SUPPORTED-by-design |
| Reliability (second-order) | Untested | C4 §11; K8 (blocked → narrowed) | UNTESTED |
| Composition with autonomy | Organism (Item 1) | AC111 (G3/G5 12/16) | direct channels clean; full composition not established (gates retained) |
| Comparative performance / viability | Organism (Item 1) | AC107/108/109 | Partial (content load-bearing; survival seed-bounded) |

**Unsupported (the record does not earn these, and no downstream doc may inherit them):**
unqualified "autopoietic"/"alive"/"self-sustaining"; full two-clause autopoiesis; any
survival-advantage claim for the cause-estimate; any reliability/meta-monitoring claim;
"first demonstrated" beyond this project's lineage; "sustained representation-repair
coupling" (N1 point 3, C3).

---

## The next bounded step (chosen, with warranting evidence)

Write up the three paper-ready claims (P1 already drafted) and authorize one named
continuation (among several open continuations on record): the **graded-posterior (first-order
uncertainty) organism-scale study** — replace the binary cause-estimate with a graded log-odds
posterior held in the same vulnerable, paid-maintained state (the AC12/AC96 dead-rule free-bit pattern
extended to a low-bit-width log-odds register), updated per contact by the C4 likelihood structure,
consumed by a threshold relinquish/hold decision. **The discriminating
prediction (prespecified):** in the C2 occluded-gate world at high q (0.7–0.9), the
graded posterior is (G1) calibrated and (G2) strictly dominates the sharpest heuristic
(`binary+imm`) on expected regret at equal action speed — gated on calibration + decision
utility, explicitly not survival. If the graded posterior matches or is beaten by
`binary+imm` organism-scale, the hypothesis is falsified and recorded, not moved.

The reliability (second-order) tier is the named next-after, gated on that result. The
autonomy track's two verdicts are stable within the current model (moving them requires a
re-architecture, not a run) — a bounded disposition, not a claim of exhaustion; other open
continuations on record include the AC110 longer-horizon/second-cause world and the C3 ongoing-repair
isolation. The I1 named interference (the corrupted contact rule
re-scheduling reacquisition) is a subordinate robustness question, not a new storage or
spending design.

---

## Sources

`S1_SYNTHESIS_v2.md`, `P1_MANUSCRIPT_DRAFT_v1.md`, `C4_TASK_DESIGN_v1.md`,
`C2_TASK_DESIGN_v1.md`, `AC109_ENGINEERING_v1.md`, `AC110_RESULTS_v1.md`,
`AC111_RESULTS_v1.md`, `AC107_RESULTS_v1.md`, `AC108_RESULTS_v1.md`,
`N1_CORRECTIONS_v1.md`, `A1_REALIZATION_LEDGER_v1.md`, `A2_BOUNDARY_VERDICT_v1.md`,
`CLOSURE_VERDICT_v1.md` (K3), `DEFINITIONS_CHARTER_v2.md` (K2), `K9_SYNTHESIS_v1.md`,
`K8_DISPOSITION_v1.md`, `AC105_RESULTS_v1.md` / `AC105_PROTOCOL_v1.md`,
`EVIDENCE_INDEX_v2.md`, `BASELINE_v1.md`, `P3_CORRECTIONS_v1.md`. Frozen dirs: `ac105_results_v1` (160 rows),
`ac107_results_v1` (240 rows), `ac108_results_v1` (288 rows), `ac110_results_v1`
(96 rows), `ac111_results_v1` (144 rows). This index is derived and is not hashed into
any study's `pre_run_snapshot.json`.
