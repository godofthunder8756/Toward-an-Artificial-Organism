# Phase-III architecture alternatives v1 — the candidate (Shared Latent Workspace) and five reduction rivals

2026-09-27. Deliverable for the G4 card (t_6a2431ec): *what is the candidate (Shared
Latent Workspace) and the five strongest reduction rivals, defined BEFORE training?*
Category B/F — **design / formalization; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It specifies the six architecture
alternatives that G10 will build and train on the G2 inference task and the G3
specialists; G5 (causal plan), G6 (coordination), G7 (novel-consumer) and G8 (leakage
audit) each read the same six arms and define their own endpoints on top of them. It
does **not** define those endpoints (that is their cards), and it does **not** fix the
training/evaluation protocol (that is G10's).

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; every comparison is a planned-denominator readout reported per
seed family, never a per-family guarantee (AC39/AC68). (3) Each rival is the
candidate's own mechanism with exactly one organizational property removed or changed
(P6, AC109 rule 1), and its parameter family is swept alongside the learner's (AC11/
AC116 rule 2). (4) No rival is handicapped by information access or by capacity; the
candidate earns its keep on *organization*, not on having more information or more
state (D2). (5) The G0 demotions bind: V is absent from all six arms, and the
maintenance rule A is fixed/reactive everywhere (verdict D), never a learned allocator.

---

## 0. The one-paragraph answer

The **candidate** is the **Shared Latent Workspace (SLW)**: one learned inference
network (a recurrent encoder) turns the observation stream into a single maintained
latent **W** (the b-bit scalar log-likelihood ratio of G2 §4.2), whose persistence
between acquisition writes is **paid** through the refresh π (the N1 substrate, driven
by the fixed/reactive rule A per verdict D), and which is consumed by **n = 3**
objective-distinct specialists **S_pol / S_plan / S_reg** (G3), each reading the same W
plus its own specialist-specific context — no specialist receives the latent cause z,
no private pristine copy of W exists, and V is not added. The **five rivals** each
remove exactly one organizational property, forming a 2×2 reduction lattice plus two
off-axis arms: **R1** (private-state specialists) removes SHARING, keeping learned
content and paid persistence — three private W_i, one per specialist; **R4**
(sufficient-statistic broadcast) removes *learned content* and *paid persistence*,
keeping sharing — the fixed analytic scalar in one free register, broadcast; **R5**
(separate copies) removes *both* the sharing mechanism and the learned/paid status —
three free copies of the same analytic scalar; **R2** (monolithic recurrent policy)
removes *modularity* — one RNN, all outputs jointly, no explicit W and no separate
specialists; **R3** (direct history-access specialists) removes the *compressed
maintained W* — each specialist reads the full bounded history directly, no W. The N2
claim survives only if each rival loses on the predicate it removes, on endpoints G5–G8
define; the comparability contract (§8) fixes capacity and information access so that a
loss is attributable to the removed property, never to an unfairness.

---

## 1. The six alternatives at a glance

| Arm | Topology in one line | Removes (the reduction) | Keeps | The claim it isolates |
| --- | --- | --- | --- | --- |
| **CANDIDATE (SLW)** | encoder → maintained W (paid π) → 3 specialists read W | — (the full conjunction) | — | SHARED ∧ CAUSAL ∧ DISTINCT ∧ AVAILABLE ∧ MAINTAINED, with learned content |
| **R1 private-state** | 3 encoders → 3 private W_i (paid π_i) → specialist i reads W_i | SHARING | modularity, learned content, paid persistence | does sharing beat solving the same inference three times? |
| **R4 suff-stat broadcast** | fixed scalar S_t (free register, broadcast) → 3 specialists read S_t | learned content + paid persistence | modularity, sharing | is the principle "shared sufficient content", not learned neural inference? |
| **R5 separate copies** | fixed scalar S_t, 3 free copies → specialist i reads copy i | sharing mechanism (+ learned/paid) | modularity, equivalent content | does the sharing *mechanism* matter, or only equivalent content? |
| **R2 monolithic RNN** | one RNN h_t → 3 heads read h_t jointly | modularity (+ explicit W, + paid π) | learned recurrence | is modularity necessary, or just interpretable? |
| **R3 history-access** | full history x_1..x_t → 3 specialists read it directly | the compressed maintained W | modularity | does W provide a compression advantage over raw history? |

The reduction is a **2×2 lattice** over two axes — *shared* (one variable) vs *unshared*
(n copies), and *learned content + paid persistence* vs *fixed content + free register*
— plus two off-axis arms (R2 monolithic, R3 history). The candidate is the
(shared, learned+paid) corner; R4 is (shared, fixed+free); R1 is (unshared, learned+paid);
R5 is (unshared, fixed+free). R2 and R3 leave the lattice by removing modularity and the
compressed representation respectively.

---

## 2. The candidate — Shared Latent Workspace (SLW)

```
x_t ──▶ [ encoder f_enc (learned, recurrent) ] ──▶ W_t  (b-bit maintained latent)
                                                  │
                     paid refresh π ◀── A (fixed/reactive rule on (s, E, d))
                     (supplied primitive;          └─ W decays at rate δ unless refreshed)
                      re-energizes W)
                                                  │  shared content: the SAME W
                 ┌────────────────┬───────────────┴───────────────┐
                 ▼                ▼                               ▼
           S_pol(W, x_t)     S_plan(W, cost)               S_reg(W, E, d, s)
              → ẑ ∈{A,B}     → {commit-A,commit-B,postpone} → {preserve, release}
```

**Components (learned vs supplied), per the G0 §4 contract.**

- **Encoder f_enc (learned).** The inference network receiving observations. A recurrent
  net (GRU per G0 §3.7) that maps `(W_{t-1}, x_t) → W_t`: the acquisition/update write
  that integrates the token stream into the belief. Correctness rides this write, not the
  refresh (D3, AC110). It never receives z as input; z is available only to the trainer as
  a disclosed scaffold (G2 §1.1).
- **W (the maintained latent).** The shared content: the scalar log-likelihood ratio S_t
  quantized to b bits (default b = 5; G2 §4.2). One storage location, one write point, one
  refresh target. This is the variable the three specialists read.
- **π (supplied).** The paid refresh that re-energizes W against decay rate δ at cost c per
  slot per step, drawn from the shared budget (the N1 substrate; G0 §3.6, G1 §2.5). The
  F1 discipline binds: the persistence must be paid, not free recurrence — the
  no-maintenance control runs the encoder's recurrence *with W decayed/zeroed*, not a
  no-recurrence policy (G0 §3.7).
- **A (supplied, fixed/reactive).** The maintenance rule that decides the refresh vector
  from the raw bookkeeping `(s, E, d)` — a threshold rule, NOT a learned allocator (verdict
  D, G0 §3.3). It is allowed, not assumed-learned, and it does not reintroduce V.
- **Specialists (learned).** S_pol (reads W, x_t; odd/sign-equivariant), S_plan (reads W,
  cost; sign-and-magnitude dependent), S_reg (reads W, E, d, s; even/sign-invariant). The
  three invariance classes of G3 §4 guarantee non-collapse. Each reads the same W plus its
  own specialist context u_i; none reads the raw history (AVAILABLE, G1 §2.4) and none reads
  z.

**What it does NOT contain (binding).** No V (G0 §3.2, verdict B — none of the six arms
requires it); no specialist receives z; no private pristine copy of W (the reference copy,
if any were needed, would itself be vulnerable and paid-maintained — here none exists);
no learned maintenance allocator (verdict D).

---

## 3. R1 — private-state specialists (removes SHARING)

```
x_t ──▶ [ enc_1 ] ──▶ W_1 (paid π_1) ──▶ S_pol(W_1, x_t)
x_t ──▶ [ enc_2 ] ──▶ W_2 (paid π_2) ──▶ S_plan(W_2, cost)
x_t ──▶ [ enc_3 ] ──▶ W_3 (paid π_3) ──▶ S_reg(W_3, E, d, s)
```

- **What it is.** Each specialist maintains its *own* private representation W_i, produced
  by its own encoder enc_i and held by its own paid refresh π_i. There is no shared W; no
  single write reaches all three consumers.
- **Removes / keeps.** Removes **SHARED** (G1 §2.1 — the two-independent-modules rival,
  generalized to three). Keeps: modularity (three specialists), **learned content** (each
  W_i is learned), and **paid persistence** (each W_i is maintained). This is the axis
  "shared → unshared" at the *learned+paid* level.
- **The claim.** "Does sharing beat solving the same inference three times?" The three
  private encoders all solve the *same* inference (all three W_i converge on the same
  sufficient statistic, differing only by training noise); the candidate solves it once
  and shares. R1 loses if the candidate's amortized inference is cheaper or more consistent
  — visible on the sample-efficiency / coordination / novel-consumer endpoints (G6/G7) —
  while matching R1 on inference accuracy.
- **Capacity.** Primary: R1's three encoders split the shared budget P three ways, so each
  private encoder has ≈ |f_enc|/3 while the candidate's shared encoder has the full |f_enc|
  (the amortization is the point). Robustness variant (§8): also run R1 with each encoder at
  full |f_enc| (R1 total = 3|f_enc|) to show the advantage is not a capacity artifact.
- **Information access.** Identical token stream to every arm; each enc_i sees x_1..x_t.
  No z to any specialist. Not handicapped.
- **Correctness checks.** (i) Each π_i is an independent paid refresh (three refresh
  budgets, not one). (ii) A single write to W_i reaches only specialist i (fails the
  single-write test, G1 §2.1-c). (iii) The three W_i are content-equivalent to the
  candidate's W up to training noise — assert their disagreement is at the noise floor, or
  the arm is not "the same inference solved thrice".

---

## 4. R4 — sufficient-statistic broadcast (removes learned content + paid persistence)

```
S_t = S_{t-1} + λ(x_t)     [fixed algorithmic update; free register]
        │
        ▼  (one broadcast register, b bits)
   ┌────┼───────────┐
S_pol(S_t,x_t)  S_plan(S_t,cost)  S_reg(S_t,E,d,s)
```

- **What it is.** The analytic scalar accumulator of G2 §2/§4.1: the *fixed* update
  `S ← S + λ(x_t)` with the λ's supplied as constants (the generative model's log-likelihood
  ratios, G2 §1.2 table), held in one ordinary free register at b bits, broadcast to the
  three specialists (which are the *same* learned readouts as the candidate's).
- **Removes / keeps.** Removes **learned content** (the update is fixed, not learned) and
  **paid persistence** (the register is free, no π, no decay). Keeps: modularity (three
  specialists) and **sharing** (one broadcast scalar). This is the axis "learned+paid →
  fixed+free" at the *shared* level.
- **The claim.** "If R4 matches, the principle is shared *sufficient content*, not learned
  neural inference." R4 holds the *exact* Bayes-optimal content at full precision; the
  candidate differs from it only in the learned update and the paid-maintained substrate,
  never in capacity or information (G2 §4.1). The candidate must (a) match R4 on inference
  accuracy — R4 is the ceiling, not the thing to beat — and (b) do organizational work R4
  cannot, because R4 has no π to cut and no maintained variable to share: the I1 decay
  signature and the maintained/shared-organizational endpoints (G5–G7). If R4 matches on
  every endpoint, learned+paid inference was unnecessary.
- **Capacity.** R4 has no learned inference, so its budget goes entirely to the three
  heads (identical to the candidate's heads). Its "free" inference is not a handicap — it
  is the defining property of the analytic rival (the optimal content supplied, D8).
- **Information access.** R4 receives the λ lookup (5 supplied constants) — its defining
  advantage, disclosed, not hidden. The candidate does not receive λ (it must learn the
  same mapping). This asymmetry *is* the learned-vs-fixed contrast.
- **Correctness checks.** (i) b bits, same as the candidate's W (G2 §4.2 — never a
  precision advantage). (ii) The update is exactly Eq. (1) of G2 §2.1, unlearned. (iii) A
  single scramble of S_t changes all three specialists (passes the single-write test — this
  is the *shared* rival, and it must pass SHARED to be a clean reduction of the other two
  properties).

---

## 5. R5 — separate copies of the sufficient statistic (removes the sharing mechanism)

```
S_t^1 = S_{t-1}^1 + λ(x_t)  ──▶ S_pol(S_t^1, x_t)
S_t^2 = S_{t-1}^2 + λ(x_t)  ──▶ S_plan(S_t^2, cost)
S_t^3 = S_{t-1}^3 + λ(x_t)  ──▶ S_reg(S_t^3, E, d, s)
```

- **What it is.** The same fixed analytic scalar, but computed into **three separate free
  registers** — specialist i reads copy i. No broadcast, no shared variable; the three
  copies carry *identical* content (the same deterministic update, the same λ's).
- **Removes / keeps.** Removes **the sharing mechanism** (SHARED's identity criterion, G1
  §2.1-b: same content ≠ shared content) *and* the learned+paid status (same as R4). Keeps:
  modularity and **equivalent content**. This is the (unshared, fixed+free) corner of the
  lattice — R4 with the sharing removed.
- **The claim.** "Does the sharing *mechanism* matter, or only equivalent content?" If R5
  matches the candidate, then having three specialists hold equal-valued content is as good
  as having them read one maintained variable — the organizational claim (one burden of
  persistence, one point of update) would be inert. The candidate wins only on endpoints
  that distinguish *identity* from *value*: the single-write test, the paid-maintenance
  economy (one refresh target vs three), and the novel-consumer reuse (G7).
- **Capacity.** Identical to R4: no learned inference; three heads at the candidate's head
  budget. Three free registers (no learned parameters).
- **Information access.** Identical to R4 (λ supplied). Not handicapped.
- **Correctness checks.** (i) The three copies are bit-identical by construction
  (deterministic update) — assert this, or the arm is not "equivalent content". (ii) A
  single write to copy i reaches only specialist i (fails the single-write test). (iii)
  The difference between R4 and R5 is *only* one-vs-three registers — nothing else, or the
  R4/R5 contrast is confounded.

---

## 6. R2 — monolithic recurrent policy (removes modularity)

```
x_t ──▶ [ one RNN: h_t = RNN(h_{t-1}, x_t) ]
                 │
        ┌────────┼──────────┐
   S_pol(h_t, x_t)   S_plan(h_t, cost)   S_reg(h_t, E, d, s)
```

- **What it is.** One recurrent network integrates the observation stream into a single
  hidden state h_t; three heads read h_t jointly and produce the three outputs. There is
  no explicit W slot, no paid refresh π, and no separate specialist modules — the heads are
  jointly parameterized readouts of one RNN.
- **Removes / keeps.** Removes **modularity** (the explicit W + separate specialists), and
  with it the explicit maintained W and the paid π (the recurrence *is* the persistence,
  unpaid). Keeps: learned recurrence over the full history.
- **The claim.** "Is modularity necessary, or just interpretable?" R2 is *richer* (h_t is a
  full vector ≥ b bits) and *cheaper* (no paid persistence) than the candidate — a strong
  rival by construction (not handicapped). If R2 matches the candidate on the intervention
  signatures and the organizational endpoints, then the explicit maintained W and the
  specialist separation are interpretive scaffolding. The candidate wins only if its
  modular structure does work R2 cannot: the differential-scramble signatures (G3 §5 —
  scrambling W produces three distinct predictable effects, which R2 has no W to scramble),
  the paid-decay signature (cut π → decay; R2 has no π), and the coordination/novel-consumer
  endpoints (G6/G7).
- **Capacity.** One RNN at the full budget P. The three heads read (h_t, context) — each
  head keeps its specialist-specific context (x_t / cost / E,d,s) so R2 is not handicapped
  on information; the hidden-state dimension is swept (comfortably ≥ b bits, so R2 is never
  capacity-limited relative to a b-bit W).
- **Information access.** Full history through the recurrence; no z to any head. Not
  handicapped.
- **Correctness checks.** (i) The three heads are jointly computed from one h_t (no separate
  modules). (ii) There is no W variable to scramble and no π to cut — assert this, or R2 is
  secretly the candidate. (iii) The heads keep their distinct objectives and distinct
  context inputs, so R2 fails FUNCTIONALLY DISTINCT (if at all) by *architecture*, not by
  construction of the heads.

---

## 7. R3 — direct history-access specialists (removes the compressed maintained W)

```
x_1..x_t (full bounded history, window M ≥ H) ──▶ [ reader_1 ] ──▶ S_pol(reader_1, x_t)
                                                ──▶ [ reader_2 ] ──▶ S_plan(reader_2, cost)
                                                ──▶ [ reader_3 ] ──▶ S_reg(reader_3, E, d, s)
```

- **What it is.** Each specialist reads the *full bounded history* x_1..x_t directly
  (through its own learned read, e.g. attention over the window), with no maintained W, no
  encoder, no π. The raw token window is the only memory.
- **Removes / keeps.** Removes **the compressed maintained W** (AVAILABLE + MAINTAINED, G1
  §2.4/§2.5 — no sufficient summary, no paid persistence). Keeps: modularity (three
  specialists).
- **The claim.** "Does W provide a compression advantage?" R3 has *more* information (the
  full history, including the informative accumulation-phase tokens, so R3 is **not** at
  chance in the probe — unlike the memoryless rival of G2 §3.1, which sees only x_t) and it
  has no maintenance cost. The candidate must show its b-bit paid-maintained summary
  matches R3 on inference accuracy while winning on the economy and the organizational
  endpoints: b bits + refresh cost vs an M-token buffer, sample efficiency (a new specialist
  reads W rather than learning to attend over M tokens), and single-write-reaches-all.
- **Capacity.** Three readers at the shared budget (each ≈ the candidate's encoder budget
  split three ways, or swept). The window length M is swept (M ≥ H = 32 default, so the
  full episode is available — R3 is never denied history).
- **Information access.** Full history (more than the candidate's W-only read). Not
  handicapped; in fact this is the information-ceiling rival.
- **Correctness checks.** (i) No W, no π — the readers take raw x_1..x_t, not a latent.
  (ii) Each specialist reads the history through its own read (no shared encoder whose
  output would secretly be a shared W). (iii) Assert R3 reaches ≥ the candidate's inference
  accuracy (it should — it has the history) so that any candidate win is an organizational/
  economic win, not an information win.

---

## 8. The comparability contract (how the six arms are made fair)

These five rules are fixed here and inherited by G10's implementation; they are what makes
"the candidate beats a rival" attributable to the removed property rather than to an
unfairness.

1. **Same task, same token stream, same seeds.** Every arm runs the G2 inference task
   (identical generative model, identical probe window, identical reward) on the identical
   seed families. No arm sees a different task.
2. **No specialist receives z, in any arm.** z is a training-only scaffold for the encoder
   (candidate/R1/R2) or absent entirely (R4/R5 fixed update); it is never a forward input to
   any specialist, in any arm, and never present at evaluation (G2 §1.1).
3. **Capacity matched by total trainable-parameter budget P, swept as a level family.** Each
   arm is swept over P ∈ {small, mid, large}. Arms that replicate inference (R1, R5) split P
   across their copies, so the candidate's single shared inference gets the full P while each
   private copy gets P/n — the amortization is stated, not implicit. R4/R5 have no learned
   inference (their "inference" is the supplied analytic update), so their budget goes to the
   identical heads; this is their defining property, disclosed, not a hidden saving.
   **Robustness variant:** R1 (and R5) additionally run with each copy at full P (total
   n·P), reported alongside the primary matched-P comparison, so a sharing win is shown not
   to be a capacity artifact (AC11 rule 2).
4. **Information never withheld; asymmetric information always in the rival's favor, and
   disclosed.** R4/R5 receive the λ lookup (the optimal content supplied — the ceiling); R3
   and R2 receive the full history; the candidate receives neither λ nor the raw history at
   read time (it retains only W). Every asymmetry gives the *rival* the advantage, so the
   candidate's burden is the organizational claim alone. No arm is ever given *less* than
   the candidate.
5. **No V, no pristine copy, in any arm.** V is absent everywhere (verdict B; no arm
   requires it). No arm contains a hidden copy of its representation that the decay/damage
   stream never reaches (G1 §2.5); where a rival has no maintained state at all (R2, R3,
   R4, R5), that is its defining property, not a pristine backup.

---

## 9. The reduction ladder — what each rival falsifies, and the gate shape

The N2 conjunction H_share (G1 §3) is the candidate's claim. Each rival removes one
predicate, and the experiment is a conjunction test: the claim survives only if every
rival loses on *its own* predicate. The gate for each arm is stated here in shape (the
numeric thresholds are G5–G8's, defined on these arms):

| Rival | Predicate removed | The candidate must show (gate shape) | What a rival win means |
| --- | --- | --- | --- |
| R1 | SHARED | single shared inference matches three private inferences on accuracy, and beats them on sample-efficiency / consistency / novel-consumer reuse (G6/G7) | sharing is inert; three private copies suffice |
| R4 | learned + paid (MAINTAINED) | match R4's ceiling accuracy; differ only on the π-dependent (I1 decay) and organizational endpoints | the principle is shared *sufficient content*, not learned/paid inference |
| R5 | the sharing *mechanism* | beat R5 on single-write identity, maintenance economy (one refresh vs three), novel-consumer reuse | equivalent content suffices; the shared variable is inert |
| R2 | modularity (+ explicit W, π) | the three distinct intervention signatures (G3 §5) and the organizational endpoints, which R2 cannot produce | modularity is interpretive; one RNN suffices |
| R3 | compressed maintained W | match R3's history-ceiling accuracy at b bits + paid cost, and win on the economy/compression endpoints | W is pure cost; raw history suffices |

**Gate-shape discipline (AC16/17, carried).** Categorical claims gate on per-individual
dominance or a threshold met by every individual, not a mean margin; "the candidate is
richer/better-informed" is excluded by §8 rules 3–4; and where a rival can reach the
ceiling (R4's accuracy), the gate is *equivalence on the ceiling plus separation on the
organizational endpoint*, never a strict `>` on the ceiling. Each rival's parameter family
is swept alongside the candidate's own hyperparameters; selecting the candidate's best
member while leaving a rival at one setting is AC11's fatal error and is prohibited.

---

## 10. What is NOT settled here (deferred to the named cards)

This document fixes the *architectures*; the following are deliberately left to the cards
that consume them, and each reads these six arms as its substrate:

- **G5 (causal plan, PHASE3_CAUSAL_PLAN_v1.md).** The frozen interventions I1–I5 and their
  per-consumer predictions. Note the arm-level consequence already fixed here: only the
  candidate (and R1) has a π to cut (I1) and a W to scramble (I2); R2/R3/R4/R5 have neither,
  so their "intervention" arms are the degenerate cases that expose what they lack.
- **G6 (coordination).** The measurable coordination condition and endpoint — which arm can
  and cannot meet it is the architectural consequence of sharing.
- **G7 (novel-consumer).** The frozen-W reuse test and the sample-efficiency / interference
  measures — the primary place R1, R4, R5 and R3 are expected to lose.
- **G8 (leakage audit).** The decoding-of-z audit across every pathway, per arm.
- **G10 (synthesis/training).** The training objectives, the frozen protocol, seeds, and the
  audit/replay split; the six arms here are its treatment column.

---

## 11. Parameters (concrete defaults, swept as level families)

| Parameter | Symbol | Default | Swept / note |
| --- | --- | --- | --- |
| Number of specialists | n | 3 (S_pol, S_plan, S_reg) | minimal pair n = 2 (S_pol, S_reg) as a variant (G3 §7) |
| W quantization | b | 5 bits | swept; R4/R5 at the same b (G2 §4.2) |
| Latent / task constants | H, K, λ, θ | G2 §6 | fixed by the task; not re-tuned per arm |
| Total parameter budget | P | swept {small, mid, large} | equal across arms (§8.3); R1/R5 split P per copy |
| Encoder capacity | \|f_enc\| | = P − n·\|S\| | the candidate's single shared inference budget |
| R2 hidden dim | d_h | swept, ≥ b bits | R2 is never capacity-limited vs a b-bit W |
| R3 window | M | H = 32 | swept M ≥ H (full episode available) |
| Refresh cost / decay | c, δ | computed at impl. | supplied (G0 §3.6 / G3 §7); candidate + R1 only |
| Maintenance rule | A | fixed/reactive on (s, E, d) | supplied, verdict D; candidate + R1 only |
| Seeds | — | disjoint eng/finals families | AC39: per-family, never mixed |

---

## 12. Claim ceiling and what this does NOT claim

- **What a pass earns, at most.** That the candidate's organizational properties — one
  maintained, paid-persistent, shared representation consumed by objective-distinct
  modules — are each causally load-bearing against a rival that removes exactly that
  property (N2 at the stated degree). Nothing stronger.
- **Not claimed here.** Any coordination, transfer, or leakage result (G5–G8's claims); any
  trained outcome (this is a design, run by G10); any "global broadcast" or "workspace
  seat" (O3/GWT); metacognition (N4); autopoiesis; any claim crossing the level-(d)/(e)
  boundary. This is a level-(b)/(c) architecture design.
- **The rivals are co-equal, not strawmen.** R4 and R3 are *advantaged* on information
  (optimal content / full history), R2 is *advantaged* on capacity and cost, R1/R5 are
  exact content-equivalent counterparts. The candidate is not "richer" than any rival; it
  differs only in the organizational properties under test.

---

## 13. Provenance

Reads the vocabulary and constraints of: `PHASE3_BASELINE_v1.md` (G0 — W/π/S_pol/S_reg
RETAIN, V REMOVE, A SIMPLIFY, the supplied-vs-learned contract), `SHARED_CONTENT_DEFINITION_v1.md`
(G1 — the five-predicate conjunction and the per-criterion rival/falsifier), `PHASE3_INFERENCE_TASK_v1.md`
(G2 — the scalar-LRR sufficient statistic, b-bit quantization, the R4 scalar accumulator,
the probe and Bayes/memoryless ceilings), `PHASE3_SPECIALISTS_v1.md` (G3 — S_pol/S_plan/S_reg
and the three invariance classes), `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4 — component
symbols, the intervention map, the pristine-backup and no-recurrence controls), and
`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2 — P5/P6 and D1/D2/D8 as the negative constraints).
Organism study references read from the skill's `references/` dir where named (`ac11`,
`ac16`, `ac17`, `ac39`, `ac68`, `ac109`, `ac110`, `ac116`).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is an
architecture design, not a result.
