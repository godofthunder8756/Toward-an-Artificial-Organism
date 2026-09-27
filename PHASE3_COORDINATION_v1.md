# Phase-III coordination condition v1 — the cross-consumer coherence that sharing alone can guarantee

2026-09-27. Deliverable for the G6 card (t_5f843868): *what measurable coordination
condition requires the specialists to consider COMMON latent content, not just each be
correct independently?* Category B/F — **design / formalization; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It defines the coordination condition
and its endpoint that G10 folds into primary gate **H4** ("organizational value of
sharing … over strongest non-shared rivals"), and that G9's reduction question (4)
("is the coordination condition reducible to one monolithic policy?") reads. It does
**not** define the per-consumer causal facts (G5's I1–I5), the novel-consumer /
sample-efficiency measures (G7), or the z-leakage audit (G8); it defines only the
cross-consumer condition those cards leave to it.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; the coordination endpoint is a planned-denominator readout
reported per seed family, never a per-family guarantee (AC39/AC68). (3) "Coordination"
is forbidden to mean "all heads correct" — the card's explicit bar; §1 states the two
readings excluded and the one kept. (4) The G0 demotions bind: V is absent, the
maintenance rule A is fixed/reactive (verdict D), and this condition does **not** wire
S_reg's decision to π (G3 §8), does not re-open D, and does not reintroduce V.

---

## 0. The one-paragraph answer

The coordination condition is **joint-realizability**: at every tick, the three
specialists' outputs must be a point on the **shared-content manifold** — the strict
1-D curve of triples `(S_pol(w), S_plan(w), S_reg(w))` swept by one scalar w. Because
the three specialists occupy three distinct invariance classes (odd / sign-and-magnitude
/ even, G3 §4), *most* triples in the output product `{A,B} × {commit-A, commit-B,
postpone} × {preserve, release}` lie **off** that curve — and an off-curve triple is a
self-contradiction that no single belief can produce. The condition has two concrete
off-curve forms: a **sign contradiction** (S_pol says A while S_plan commits B — two
sign-trackers disagreeing) and a **magnitude contradiction** (S_plan commits, which
needs `|W| ≥ a`, while S_reg releases, which needs `|W| < θ`, under the design ordering
`θ ≤ a` that §2.3 fixes). The **architectural consequence of sharing** is that a single
W makes both contradictions **structurally impossible** — one value read by three
functions of it always lands on the manifold — whereas the unshared rival R1 (three
private learned encoders, each correct in expectation) produces off-manifold triples at
a measurable rate, because three independent inferences drift across each other's
thresholds. The endpoint is the **incoherence rate**: the planned-denominator fraction
of (seed, tick) pairs whose triple is off the manifold (and its per-episode form, the
fraction of episodes containing at least one contradiction). Candidate (and the shared
rival R4, and the equivalent-content rival R5) score 0 by construction; R1 scores > 0;
R2/R3 score an empirical, not structural, value — which is exactly the fact G9's
reduction question (4) needs.

---

## 1. What "coordination" is forbidden to mean, and what it means here

Three readings are possible and only one is kept. The card rules out the first two.

1. **FORBIDDEN — "all heads correct."** Each specialist independently achieves its own
   optimum against its own loss. This is what G5's I2 (W-cut, per consumer) already
   establishes as *CAUSAL*, and what R1 can also achieve (three private encoders, each
   converging on the sufficient statistic). "Coordination = correctness" adds nothing
   beyond G5 and fails the card's bar.
2. **FORBIDDEN — "the outputs co-vary" (correlation).** The three outputs all move when
   W moves. G5's I1 differential-scramble already establishes this as *DISTINCT*, and a
   flat co-varying response is the two-linear-heads rival G3 §1 must fail. A correlation
   is not a coordination; it is the thing coordination must *transcend*.
3. **KEPT — joint-realizability (a relational constraint that a single shared variable
   enforces for free and no independently-optimized rival gets for free).** The three
   outputs must be mutually consistent with **one** value of the latent content at
   **one** tick. This is a *cross-consumer* constraint — it constrains the tuple, not
   any single specialist — and it is satisfied **by construction** only when the three
   read the same variable. "Each correct independently" does not imply it: three
   private states can each be the right answer in expectation and still, at a given
   tick, straddle their thresholds in opposite directions, producing a triple no single
   belief could have generated. The coordination claim is the *relational* half of N2:
   the specialists are not merely three correct consumers of the same content; their
   outputs are *locked together* by it.

The formal object is §2's manifold; the tension that makes it a *coordination problem*
rather than a scoring convention is §3; the endpoint is §4.

---

## 2. The coordination condition (COORD): the shared-content manifold

### 2.1 The manifold — a strict curve, not a product

Each specialist is a fixed function of W with a distinct invariance class (G3 §4):

- `S_pol(w) = A iff w > 0` — **odd** (sign-equivariant).
- `S_plan(w) = commit-A iff w ≥ +a; commit-B iff w ≤ −b; else postpone` — **sign-and-
  magnitude dependent** (symmetric default a = b).
- `S_reg(w) = preserve iff |w| ≥ θ(E, d, s)` — **even** (sign-invariant).

The **shared-content manifold** M is the image of the map `w ↦ (S_pol(w), S_plan(w),
S_reg(w))`, a **1-D curve** inside the 3-D output product (12 triples in the symmetric
default). It is strict: the invariance classes make most of the product empty under the
map. The full curve (symmetric default, θ < a):

| w range | S_pol | S_plan | S_reg |
| --- | --- | --- | --- |
| w ≥ +a | A | commit-A | preserve |
| +θ ≤ w < +a | A | postpone | preserve |
| 0 < w < +θ | A | postpone | release |
| −θ < w ≤ 0 | B | postpone | release |
| −a < w ≤ −θ | B | postpone | preserve |
| w ≤ −a | B | commit-B | preserve |

The manifold has **six** realizable triples. The other six of the twelve are
**unreachable by any single w** — they are the incoherent triples.

**Definition (COORD).** A specialist system is **coordinated** on an episode iff, at
every tick t, the triple of the specialists' functions-of-W outputs lies on M (i.e.
there exists a scalar w consistent with all three outputs at that tick). The system is
coordinated **per seed** iff it is coordinated on that seed's episode; the **coherence
rate** is the fraction of seeds so coordinated.

### 2.2 The two contradiction types (the off-manifold triples)

Only two *kinds* of incoherence exist, and each names a specific rival's failure:

- **Sign contradiction (off-curve on the sign axis).** `(A, commit-B, ·)` and
  `(B, commit-A, ·)` — S_pol's direction and S_plan's committed direction disagree.
  Both specialists are sign-trackers, so a single shared w can never produce this (w
  has one sign). It arises only when S_pol and S_plan read **different** latent values
  whose signs disagree — the R1 failure (three private encoders near the sign boundary).
- **Magnitude contradiction (off-curve on the magnitude axis).** `(·, commit-*, release)`
  — S_plan commits (needs `|w| ≥ a`) while S_reg releases (needs `|w| < θ`), which is
  impossible iff `a ≥ θ` (§2.3). Both are magnitude-readers, so a single shared w obeys
  the ordering by construction. It arises only when S_plan and S_reg read **different**
  latent magnitudes that straddle the `[θ, a)` gap — again the R1 failure, now between
  the value gate and the commitment gate.

The **retention-vs-commitment** pair is the condition's "one action changes what
information remains useful to another" instance: S_reg's release is a decision that a
belief has stopped being worth holding, and S_plan's commitment is a decision that the
belief is now worth acting on; a shared magnitude makes the two jointly consistent by
ordering, private magnitudes do not.

### 2.3 The design constraint that makes coherence structural: θ ≤ a

For "commit ⇒ preserve" to be an invariant of the shared architecture, the two
thresholds must be ordered: **θ(E, d, s) ≤ a for every feasible (E, d, s)**. This is a
binding design constraint G6 adds to G3's parameters, and it is economically natural —
a belief you would stop paying to hold at confidence `θ` is a belief you would not act
on at the higher confidence `a`; between them (`θ ≤ |W| < a`) the organism keeps
paying to gather evidence it is not yet ready to act on. It is stated as a *swept*
parameter family `θ ∈ [θ_lo, a]` (never above a), so the ordering is a level family,
not a single hand-picked value (AC11 rule 2). With `θ ≤ a`, the shared architecture
**cannot** emit a magnitude contradiction; the value-of-information gate is always
below the commitment gate.

---

## 3. The situation that forces common content (why "each correct" is not enough)

The coordination condition is not a scoring convention bolted on top of G3; it is the
cross-consumer form of a genuine tension the three specialists already carry. Two
losses pull in opposite directions over the `[θ, a)` region:

- **S_reg's loss** (resource economy, G3 §2.3) rewards releasing **early** — the
  moment `|W|` drops below θ, continued retention is wasted budget, so S_reg is
  graded to release at exactly θ.
- **S_plan's loss** (speed-accuracy-cost, G3 §2.2) rewards committing **late** — it
  postpones until `|W|` clears a, so it is graded to keep gathering evidence up to a.

The two are in tension precisely on `θ ≤ |W| < a`: there, S_reg's objective says
"still worth holding," S_plan's says "not yet worth acting on," and the *jointly*
correct behaviour is to keep holding while postponing. A **shared** magnitude resolves
this for free — both read the same `|W|`, so S_reg releases at exactly the tick the
belief leaves the worth-holding region, never while S_plan is still inside it. Two
**private** magnitudes do not: S_reg's W_reg can dip below θ while S_plan's W_plan is
still below a (or vice versa), so S_reg releases while S_plan postpones — S_plan is now
gathering evidence in a belief that S_reg has already judged not worth holding, a
self-contradictory plan. This is the card's "they act at different times with different
losses; one action changes what information remains useful to another," realized
without re-opening verdict D (S_reg remains a readout, not a maintenance controller;
the tension lives in the two *objectives*, which is where G3 already put it).

The key fact that makes common content *necessary* rather than convenient: **the
manifold constraint is a relation over the tuple, and no amount of per-specialist
correctness enforces it.** Three encoders each trained to their own optimum can each be
correct and still produce off-manifold triples wherever independent training noise
straddles a threshold. Only a single variable whose value all three read makes the
constraint free.

---

## 4. The measurable endpoint

Reported per seed (planned denominator, never pooled), with disjoint engineering and
finals families (AC39):

- **Primary — incoherence rate.** `R_inc = #{ (seed, tick) : triple ∉ M } / #{ seed, tick }`,
  the planned-denominator fraction of off-manifold ticks, reported per seed family as a
  lower-bound-on-0 (the candidate's structural claim) with the per-seed distribution
  carried. Its per-episode form — `R_inc^ep = #{ seeds with ≥1 off-manifold tick } / N`
  — is the categorical companion: "does the system ever contradict itself."
- **Secondary — coherent-correct-plan rate.** The fraction of seeds whose triple is
  coherent **and** correct at the consequential ticks (S_plan's commitment tick τ and
  S_pol's decision tick H): S_plan commits to the right z, S_pol decides the right z,
  and S_reg preserved W through both. This separates "coordinated and right" from
  "coordinated but wrong," and is the endpoint H4's "coordination advantage" reads.
- **Chronological scalars** (the G-series analogue of the organism line's first-loss
  scalars): first incoherence tick, first sign-contradiction tick, first
  magnitude-contradiction tick — recorded where they carry the mechanism.

The tie at w = 0 is a fixed convention, not part of the claim (G5 §3 rule 4): the
manifold test at |w| < resolution folds w = 0 into the `release`/`postpone`/`B` cell
(S_pol's tie convention W ≤ 0 → B), held identically across every arm.

**Consequentialization (optional, G10's choice).** To make the endpoint a scored
quantity rather than a passive count, G10 may fold a contradiction penalty into the
joint plan score — an off-manifold triple earns the abstain payoff minus a fixed
`C_contradiction`, applied identically to every arm, so a self-contradictory plan is
penalized above and beyond being merely wrong. This is a G6-authorized extension to
the consequence structure (like S_plan was G3-authorized); it is **not** required for
the endpoint to be measurable, and it must not handicap any rival (R1's specialists
are scored against the same penalty).

---

## 5. Per-arm application (which arm can and cannot meet it)

| Arm | Incoherence rate | Why | What it shows |
| --- | --- | --- | --- |
| **CANDIDATE (SLW)** | **0 by construction** | one W, three functions of it; sign and magnitude cannot disagree; θ ≤ a forbids the magnitude contradiction | sharing makes coordination free |
| **R4 (suff-stat broadcast)** | **0 by construction** | one broadcast S_t, three functions of it — the same guarantee | R4 *also* coordinates; it differs only on the maintained/learned endpoints (G4 §4), never on this one |
| **R5 (separate copies)** | **0 by construction** | three bit-identical deterministic copies cannot disagree | coordination alone does **not** separate R5 — its separation is the single-write identity (G5 I1), the maintenance economy, and novel-consumer reuse (G7) |
| **R1 (private state)** | **> 0, measured** | three learned encoders converge on the same statistic but drift independently; near a boundary one W_i crosses while another does not | the load-bearing rival: three *correct* private inferences still contradict each other — the card's "cannot each optimize independently" |
| **R2 (monolithic RNN)** | **empirical, not structural** | one h_t is shared, but nothing forces the three heads to map h_t onto the manifold — sign(S_pol head) ≠ sign(S_plan head) is possible unless training aligns them | the modularity contrast: the candidate's coherence is guaranteed by its explicit W + function forms; R2's is only as coherent as its heads happen to be |
| **R3 (history access)** | **empirical, not structural** | each reader independently attends over the history; nothing ties their outputs to one latent | same as R2: coherence is a training outcome, not a structural fact |

**What the arm table licenses, and what it does not.** The coordination condition's
clean, load-bearing separation is **candidate (and the shared/free arms) = 0 by
construction vs R1 = measured > 0**. This is exactly the card's demand — the rival that
"each optimizes independently" is the one that fails the cross-consumer condition — and
it is what H4's "coordination" clause gates on. It does **not** separate candidate from
R4 or R5 (nor should it: those arms are shared or content-equivalent, and their
reductions live on other predicates). It does **not** by itself separate candidate from
R2/R3; what it establishes for those two is the *modularity* fact G9's reduction
question (4) needs: the candidate's coordination is **structural** (guaranteed by an
explicit maintained W and three fixed function forms), R2/R3's is **statistical**
(achieved only if the monolithic/reader heads happen to land on the manifold). That is
a genuine architectural consequence of the explicit shared latent, and it is reported
as such — not over-claimed as "R2/R3 must fail."

---

## 6. The architectural consequence of sharing (why coherence is free for the candidate)

The one-sentence version: **the shared-content manifold is enforced by identity, not by
optimization.** When all three specialists read the same W, the triple is
`(S_pol(W_t), S_plan(W_t), S_reg(W_t))` *by wiring*, and that triple is on M *by
definition of M* — no specialist ever needs to know anything about another to stay
coherent. When they read three private states, the triple is
`(S_pol(W_1), S_plan(W_2), S_reg(W_3))`, and staying on M would require the three
independent inferences to agree at every tick — a cross-specialist optimization problem
no single specialist's loss even sees. The three consequences of this:

1. **Coherence is a property of the organization, not of the training run.** The
   candidate's 0 incoherence rate holds for every seed, every horizon, every threshold
   sweep — it is a theorem about the wiring, not a statistic. R1's incoherence rate is a
   training-outcome statistic that must be measured and can only be driven down, never
   to 0, by more training.
2. **A single burden of consistency replaces three burdens of agreement.** R1 would
   need its three encoders to agree (near boundaries) — an agreement the architecture
   does not supply and the losses do not reward. The candidate spends that consistency
   for free, once, in the shared variable.
3. **The contradiction is impossible *inside* the candidate, so detecting one is a
   wiring bug, not a result.** The AC85 lesson applies in reverse: a silently wrong
   wiring (a specialist reading a private copy instead of W) *would* show up as an
   off-manifold triple in the candidate, so the manifold check doubles as a
   byte-level wiring audit — the candidate's incoherence rate must be exactly 0, and
   any nonzero value is a defect to find, not a finding to report.

---

## 7. Pre-declared gates (consistency checks G10 must assert)

Each gate is pre-declared and none may be amended after seeing results (AC16/17
discipline). Gate shape matches claim shape: categorical "coordinated" claims gate on
per-individual dominance / a threshold met by every seed, never a mean margin (AC16);
equivalence claims gate on exact equality, never "similar" (P7).

1. **Candidate coherence is structural (H4's coordination clause).** On the finals
   seed family, the candidate's incoherence rate is **exactly 0** at every tick — no
   sign contradiction, no magnitude contradiction. Any nonzero value is a wiring bug to
   fix, not a result (AC85, and §6.3). The threshold ordering `θ ≤ a` is verified in
   the same pass.
2. **R1 incoherence is real and measured (the rival must fail).** On the same finals
   family, R1's incoherence rate is **> 0 on at least one seed** (and its per-seed
   distribution is reported). A gate of "R1 = 0 too" would be a wiring bug (R1 secretly
   sharing); a gate of "R1 > 0 on every seed" would over-claim — the honest gate is
   per-individual dominance with the distribution reported, the AC16/17 shape. This is
   the load-bearing contrast: three private *correct* inferences still contradict.
3. **Shared arms are coherent, off-axis arms are empirical (the modularity fact).** R4
   and R5 have incoherence rate 0 (R4 by identity, R5 by determinism) — assert this, or
   the arm is not what G4 specified. R2 and R3 report their incoherence rate as a
   measured training outcome with **no structural guarantee**; assert that the *code
   path* for their heads/readers is genuinely unconstrained on the manifold (not that
   the rate is nonzero — whether monolithic training lands on the manifold is the
   empirical question G9 audits).
4. **Manifold geometry (the two contradiction types are the only ones).** Assert the
   realizable set M has exactly six triples (symmetric default, θ < a) and that the
   six off-curve triples decompose into the four sign-contradiction triples
   `(A, commit-B, preserve)/(A, commit-B, release)/(B, commit-A, preserve)/(B, commit-A,
   release)` and the two magnitude-contradiction triples `(A, commit-A, release)/
   (B, commit-B, release)`. A different geometry means the invariance classes (G3 §4)
   were not respected and the design is not the one this document specifies.
5. **Threshold ordering θ ≤ a holds across the sweep.** For every swept member of the
   θ and a families, assert `θ ≤ a` (so "commit ⇒ preserve" is invariant). A member
   with θ > a is excluded from the coordination claim and reported as such.
6. **Byte-identity at the intact boundary (P7).** The manifold/endpoint readouts are
   compared against the uninterrupted control run on the same seed; the only permitted
   difference is the arm's topology. This is the coordination endpoint's own version of
   G5's rule 7 and AC83's method.

---

## 8. Parameters (concrete defaults, swept as level families)

| Parameter | Symbol | Default | Swept / note |
| --- | --- | --- | --- |
| Specialists | n | 3 (S_pol, S_plan, S_reg) | minimal pair n = 2 (S_pol, S_reg) as a variant (G3 §7) |
| S_pol threshold | θ_pol | 0 (sign) | fixed (G2 §6) |
| S_plan thresholds | a, b | a = b (symmetric) | swept with the cost model (G3 §7); asymmetric under G3 §3.3 |
| S_reg threshold | θ(E, d, s) | fixed/reactive form | swept in `[θ_lo, a]`, **never above a** (§2.3) |
| Threshold ordering | θ vs a | θ ≤ a | binding design constraint (§2.3) |
| Contradiction penalty | C_contradiction | 0 (endpoint measured, not scored) | optional scoring layer, G10's choice (§4) |
| W quantization | b | 5 bits | swept; rival at same b (G2 §4.2) |
| Horizon / probe | H, K | 32, 8 | G2 §6 |
| Seeds | — | disjoint eng/finals families | AC39: per-family, never mixed |

The manifold M is computed from the *function forms* (G3 §2), not from trained weights:
it is the map `w ↦ (S_pol(w), S_plan(w), S_reg(w))` with the thresholds in place. The
numeric thresholds do not change the geometry (the six-triple curve), only which w maps
to which triple — the sweep verifies this, exactly as G3 §6 gate 1 verifies the
invariance classes.

---

## 9. Scope, claim ceiling, and what this does NOT claim

- **Claim ceiling.** A pass earns, at most: **"the candidate's three specialists are
  coordinated — their outputs are mutually consistent with one value of the shared
  maintained content at every tick, by construction — while the unshared rival that
  solves the same inference three times contradicts itself at a measurable rate, and the
  off-axis rivals achieve coherence only as a training outcome, not as a structural
  fact."** This is the *relational* half of N2 (the cross-consumer constraint), nothing
  stronger. No "global broadcast", no "workspace seat" (O3/GWT), no metacognition (N4),
  no autopoiesis, no consciousness claim.
- **S_reg is still a readout, not a maintenance controller.** The tension in §3 lives in
  the two *objectives*; S_reg's preserve/release does not gate π here (G3 §8), and the
  coordination condition does not re-open verdict D. A maintenance-allocation claim is
  T4's, not N2's.
- **Not claimed:** that R2/R3 *must* be incoherent (only that their coherence is not
  structural — G9's reduction question (4) settles whether a monolithic policy trivially
  lands on the manifold); that coordination separates candidate from R4/R5 (it does not,
  and is not expected to — G4 §9); any novel-consumer / sample-efficiency / transfer
  result (G7's); any z-leakage result (G8's). This is a level-(b)/(c) coordination
  design.
- **The endpoint is coordination, not correctness.** The primary endpoint (incoherence
  rate) is orthogonal to whether the specialists are right about z: a system can be
  perfectly coordinated and wrong (all three consistently wrong — G5's I5 coherent-error
  case), or correct on average and incoherent (R1 near a boundary). The secondary
  endpoint (coherent-correct-plan rate) is where correctness re-enters, and it is kept
  explicitly secondary so "coordination" cannot silently collapse back into "both
  correct."

---

## 10. Provenance

Defines the cross-consumer condition over the three specialists of
`PHASE3_SPECIALISTS_v1.md` (G3 — S_pol sign / S_plan SPRT / S_reg even-gate, §3.2
invariance classes, §4 the three-way non-collapse, §7 thresholds) and the six arms of
`PHASE3_ARCHITECTURES_v1.md` (G4 — candidate SLW + R1–R5, §8 comparability contract,
§9 the per-rival gate shapes, §10 "G6 = coordination condition + endpoint"). It takes
G5's `PHASE3_CAUSAL_PLAN_v1.md` as the per-consumer half and supplies the cross-consumer
half G5 §7 explicitly defers to it ("I4 supplies the per-consumer load-bearing fact, G6
supplies the cross-consumer condition"), reusing G5's surgical discipline (§3 rule 5,
byte-identity) and its I5 coherence check as the single-tick seed of the full-manifold
condition. The five-predicate vocabulary is `SHARED_CONTENT_DEFINITION_v1.md` (G1 §2,
the FUNCTIONALLY_DISTINCT "no collapse" condition §2.3, the single-write test §2.1-c);
the task and its probe/ceiling are `PHASE3_INFERENCE_TASK_v1.md` (G2 §1.3 probe, §2.1
scalar LLR, §6 parameters). The demotions (no V, fixed/reactive A, S_reg not gating π)
are `PHASE3_BASELINE_v1.md` (G0 §3) and the verdict `BRIDGE_PHASE2_VERDICT_v1.md`
(B+D). The gate-shape and rival-sweep discipline is `ACI_ARCHITECTURAL_PRINCIPLES_v1.md`
(P6, P7, D1–D8). Organism study references read from the skill's `references/` dir where
named (`ac11`/`ac16`/`ac17` — gate shape matched to claim shape; `ac39`/`ac68` —
seed/bimodality; `ac83` — byte-identity license; `ac85` — a silently wrong wiring is the
failure mode, exposed by the exact-match gate).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is
a coordination-condition design, not a result.
