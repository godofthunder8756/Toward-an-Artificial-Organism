# ACI next-phase disposition v1 — the G17 terminal decision (revise the architecture before metacognition)

2026-09-27. Deliverable of the G17 card (t_69645f9f): *what is the next phase, given
the Phase-III result?* This is the **terminal** decision of the ACI program. The
disposition is a **documented architecture revision** — the card's branch-B deliverable —
prepared but **not executed**: it runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It closes the program.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary
(`DEFINITIONS_CHARTER_v1.md` §2) is absolute: no phase in, or revision of, this program
is, or is meant as, a path to a consciousness claim. (2) Seeds are the replication unit;
survival is a bimodality-aware lower bound (AC68), never a per-seed-family guarantee.
(3) Every positive claim is credited only if the rival that omits it provably fails
(P6); gates are prespecified and never moved after a result (AC16). (4) Composition is
licensed by byte-identity (`state_hash`), never prose. (5) The program's collapse record
is the standing falsification set, now extended by the two neural demotions D11/D12.
(6) This document reads frozen verdicts; it does not re-litigate them.

---

## 0. The one-paragraph answer

Phase III collapsed to a **simple sufficient-statistic broadcast** (OUTCOME C: the
Shared Latent Workspace candidate is the lowest-accuracy of six arms, and the analytic
broadcast rivals R4/R5 tie-or-beat it at zero parameters and zero cost, with the
monolith R2 beating it at ~3× parameters). Per G17's own branch instruction, that
collapse selects the **revise-the-architecture** branch, not the prepare-Phase-IV
branch: the integration mechanism — the learned encoder + paid-maintained shared
workspace — did **not** survive, so the program does **not** add higher-order machinery
(metacognition, N4) on top of it. The revision reduces the architecture to its
surviving load-bearing object — **sufficient-content availability**, carried for free
by a broadcast, with **N1 paid persistence** retained only as a necessary-condition
substrate fact — and re-specifies the single open forward question as the
**acquired-statistic question**: whether a sufficient statistic *learned* from an
environment where it is not supplied in closed form makes the workspace/sharing
machinery load-bearing. That is a revision of the integration layer's test, **not** a
metacognitive build. It is prepared here as a direction; it is not executed, not
frozen, and — this card being terminal — it is not scheduled as a further card.

---

## 1. The decision (G17's branch, applied to the frozen verdict)

G17 offers two branches and names the condition that selects between them:

- **Branch A** (Phase III produced real shared-content with organizational value) →
  prepare the Phase-IV protocol around competition-for-limited-workspace / recurrent
  amplification / selective broadcast / self-evaluation of shared content.
- **Branch B** (Phase III collapsed to simple broadcast or monolithic recurrence) →
  revise the architecture before metacognition; do **not** add higher-order machinery
  onto an integration mechanism that has not survived.

The frozen verdict (`PHASE3_VERDICT_v1.md`) is OUTCOME C, which is a collapse of
exactly the kind Branch B names: the candidate is the worst arm on raw inference, and
the *analytic* sufficient-statistic broadcast (R4) and identical copies (R5) reproduce
its content for free, while the monolith (R2) beats it. The verdict's own scope note
(§4) is explicit that the collapse is bounded to the closed-form-statistic task and
that the acquired-statistic question is a *different, still-open* question.

**Decision: Branch B.** The next phase is an architecture revision, not a Phase-IV
protocol and not a metacognition build. The program ends here with a specification —
the revised architecture plus the prepared-but-not-executed forward question — not a
result.

---

## 2. What Phase III established (restated from the frozen verdict; read, not re-run)

Per-arm probe accuracy over the 12 final seeds (from `PHASE3_VERDICT_v1.md`, the G14
table):

| arm | probe_acc | clean_acc | incoherence | refresh events | params |
| --- | --- | --- | --- | --- | --- |
| candidate (SLW) | 0.9632 | 0.9639 | 0.000 | 32768 | 393 |
| r1 (private copies) | 0.9634 | 0.9631 | 0.0140 | 98304 | 309 |
| r2 (monolith RNN) | 0.9643 | 0.9645 | 0.0038 | 0 | 1242 |
| r4 (suff-stat broadcast) | 0.9645 | 0.9645 | 0.000 | 0 | 0 |
| r5 (identical copies) | 0.9645 | 0.9645 | 0.000 | 0 | 0 |
| r3 (raw history) | 0.9648 | 0.9652 | 0.0129 | 0 | 3450 |

Three facts, each read at its exact width:

1. **Content survives; machinery does not.** The candidate's learned encoder adds
   nothing over the fixed scalar counter R4 (0.9632 vs 0.9645 at zero cost). The
   content *is* the scalar sufficient statistic; the encoder + paid persistence +
   shared-slot identity are pure cost.
2. **The monolith is a valid (better) realization.** R2 — one RNN, no W, no π, no
   shared state — beats the candidate at ~3× parameters. Modularity is an
   interpretability/intervention affordance, not a performance property.
3. **Sharing is load-bearing narrowly, and free once content is sufficient.** Sharing
   genuinely buys coordination (0 vs 0.014 incoherence, p = 0.00049) and maintenance
   economy (1 vs 3 refresh targets) over the private-copy rival R1 — but a broadcast
   delivers it for free. The *content* is shared; the *machinery* is not needed.

These are the neural restatement of the organism program's signature collapse
(D2/D5/AC109), and they enter the demotion set as **D11** (shared maintained workspace
unnecessary) and **D12** (modular specialists add no value) — already absorbed into
`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` §8 and `ACI_MASTER_RESEARCH_TREE_v3.md` §5.3.

---

## 3. The architecture revision (the core deliverable)

### 3.1 What is removed

The minimal neural architecture (`ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md`, Q4)
specified eight components. Phase III measured two of them and found them scaffolding;
the revision removes them as *performance* components:

1. **The limited recurrent workspace H, as a learned encoder + paid-maintained shared
   slot — removed (D11).** The workspace machinery (learned encoder, paid persistence
   π as an inference advantage, explicit shared-slot identity) adds nothing over a
   broadcast of sufficient content. It survives only in its degenerate form: a free
   register/broadcast carrying sufficient content. The k-slot bottleneck claim (GWT's
   O3) was never adopted by the neutral core (Q4 §5.4), and now the machinery that
   would occupy that bottleneck is measured to be scaffolding on closed-form content.
2. **Modular specialists, as a performance property — removed (D12).** The three
   specialists are three fixed functions of one scalar with distinct invariance
   classes; the monolith beats them. Specialists survive only as intervention and
   interpretation affordances (a scramble-able slot, a separable persistence term),
   never as a claim that modularity buys accuracy.

### 3.2 What survives (the revised load-bearing object)

Three things survive the two neural verdicts jointly, and they are the whole revised
architecture:

1. **Sufficient-content availability** — the load-bearing fact. When the content is a
   sufficient statistic, carrying it to the consumers is free and automatic (broadcast
   it). The design target is the *content's sufficiency*, not the machinery around it.
2. **N1 active paid persistence — as a necessary-condition substrate fact, not an
   advantage.** The π-cut decay is clean (0.9632 → 0.5000, p = 0.00049), but the
   content it maintains is carried for free by a register. Paid persistence is
   *required* for any non-free-permanent representation; it buys no inference
   advantage over the free broadcast.
3. **Sharing as a free broadcast — the narrow coordination/economy fact.** Sharing is
   load-bearing over private copies (coordination, economy) and is delivered for free
   once the content is a sufficient statistic.

### 3.3 The revised minimal architecture (what Q4 becomes, in one paragraph)

The architecture reduces to: a recurrent network that computes **sufficient content**
(a statistic that summarizes the relevant history), held under **paid persistence**
(the N1 substrate — the one necessary condition, since nothing persists for free), and
**broadcast for free** to any number of objective-distinct consumers. The workspace,
the encoder, the paid-maintained shared slot, and the modular specialists are *not*
components to build; they are properties the content realizes for free when it is
sufficient, and scaffolding otherwise. The maintenance controller A and the
self-evaluative pathway E are **not** revised away by Phase III — but they are also
**not** the next thing to build, because they sit at the N4/metacognition tier that
this card's branch instruction parks (§4).

### 3.4 The revised theory matrix (D2 re-framed)

The theory-indicator matrix (`ACI_THEORY_INDICATOR_MATRIX_v1.md` §8) already records
the Phase-III consequence: D2 (the GWT bottleneck contrast) must be re-framed around
**acquired** content — as written it asks whether a k-slot bottleneck beats local
recurrence on closed-form content, which Phase III shows is near-vacuous (the
bottleneck machinery is scaffolding there). The load-bearing form of D2 is the
acquired-statistic question. This disposition adopts that re-framing as the program's
forward direction (§5), and it extends the same re-framing to the whole of the
integration layer, not only D2.

---

## 4. What is explicitly NOT done (the negative half of the disposition)

The card's branch instruction is a *prohibition* as much as a direction. The following
are decided against, and the decision is recorded so a later reader does not re-commit
them:

1. **No Phase IV (N4 / metacognition) build.** The self-evaluative pathway E, the
   higher-order contrast D1, and the metacognitive-monitoring target are not built on
   top of an integration mechanism (the shared workspace) that did not survive. Adding
   higher-order machinery now would repeat the program's signature error — elaborate
   machinery over a collapse — at the metacognition tier.
2. **No Phase-IV protocol around competition / recurrent amplification / selective
   broadcast / self-evaluation.** That is Branch A's deliverable, and Branch A is moot:
   Phase III did not produce shared-content with organizational value; it collapsed to
   a free broadcast.
3. **No re-tuning of the SLW candidate.** The workspace candidate is the worst of six
   arms and is not to be improved (`ACI_MASTER_RESEARCH_TREE_v3.md` §11).
4. **No re-opening of Phase II or Phase III.** Both are closed with their recorded
   verdicts (B+D; C).
5. **No re-opening of the organism line.** Phase I is closed (Q7's exit); the neural
   verdicts confirm, not invalidate, its transferred principles.
6. **No consciousness or autopoiesis claim.** The claim ceiling (§7) is unchanged.

---

## 5. The prepared-but-not-executed forward question: the acquired statistic

The one open forward question the Phase-III verdict's own scope note names (§4 of
`PHASE3_VERDICT_v1.md`), carried by G16 into the tree (§5.4) and the roadmap (§4.2), is
this: **does a sufficient statistic that is *learned* from an environment where the
statistic is not supplied in closed form carry the sharing/workspace properties?**
This disposition makes it the program's endpoint, specified — not executed.

### 5.1 Why this is a revision of the integration layer, not a metacognition build

The collapse of Phase III is a property of *closed-form* content: when the relevant
history compresses to a known scalar, the analytic broadcast rival R4 is available for
free and beats the workspace machinery. The acquired-statistic question removes exactly
that rival's free availability: if the content must be *learned* (the sufficient
statistic is not supplied in closed form), there is no R4 to broadcast, and the
question becomes whether the maintained learned representation — the workspace's
content-bearing object — is load-bearing where the free rival cannot go. That is a
**re-specification of the integration mechanism's test**, not a higher-order build. It
honours the card's prohibition precisely: instead of adding machinery above the failed
workspace, it re-tests the same workspace under content the free broadcast cannot
supply.

### 5.2 Design direction (prepared, not executed)

The direction is a *new task design*, not a re-run of Phase III's closed-form world
(`ACI_MASTER_RESEARCH_TREE_v3.md` §11). Stated at design level, not protocol level:

- **Content.** The environment's sufficient statistic is **not closed-form** — the
  relevant history does not compress to a known analytic scalar, so the representation
  must be *acquired* by a learner from observations alone. The content is still a
  maintained representation consumed by objective-distinct specialists (N2, the same
  property), but no free analytic broadcast rival exists for it.
- **Rivals (unchanged P6 set, re-applied).** The state-blind fixed policy; the
  reactive/memoryless rival; the finite-state/direct-control rival; the monolith
  (R2's form); the private-copies rival (R1's form); and the raw-history rival (R3's
  form). The one rival that *cannot* be supplied is the closed-form analytic broadcast
  (R4) — and its absence is the point of the design.
- **The discriminating question.** Does the maintained *learned* statistic beat the
  monolith and the private copies where no free broadcast exists? If the monolith or
  a fixed mapping still wins with acquired content, the workspace is scaffolding
  **unconditionally**, and the program ends with a strong negative (the collapse is
  not closed-form-specific). If the maintained shared statistic becomes load-bearing
  only when content is acquired, the integration layer survives in its acquired form,
  and — only then — metacognition (N4) becomes a legitimate next step.
- **Gates would be categorical** (per-individual dominance, or a threshold met by
  every seed), never a mean margin (AC16/17); the rival families would be swept
  alongside the learner's own (AC11); and the equivalence/byte-identity checks would
  stay mandatory. **None of this is frozen** — no seeds, no gate constants, no
  protocol — because this card is terminal and the direction is a specification, not a
  scheduled experiment.

### 5.3 What a positive answer would and would not earn

A positive answer to the acquired-statistic question would earn, at most, "a learned
maintained statistic's content is available to objective-distinct modules — N2 at the
stated degree, with the content acquired." It would **not** earn metacognition,
workspace-seat (O3/GWT), or any level-(d)/(e) claim. It is a revision of the
integration layer, and its ceiling is level (b)/(c) representational.

---

## 6. What this hands the program (the terminal hand-off)

- **The decision:** Phase III collapsed to a sufficient-statistic broadcast; the next
  phase is an architecture revision, not metacognition (Branch B).
- **The revision:** the architecture reduces to sufficient-content availability via
  free broadcast + N1 paid persistence as a necessary-condition substrate fact; the
  workspace machinery (D11) and modular specialists (D12) are demoted; the matrix's D2
  is re-framed around acquired content.
- **The forward question:** the acquired statistic, prepared as a design direction,
  not executed, not frozen, not scheduled — the program's endpoint is the
  specification of this target, not the demonstration of anything beyond the two
  measured verdicts (B+D; C).
- **The standing falsification set** is now D1–D12 plus the organism negatives of the
  mission audit; the collapse record has three sites (organism, neural
  self-maintenance, neural workspace) and one shape.

---

## 7. Claim ceiling (stated once, unchanged)

No autopoiesis claim, no "alive"/"self-sustaining" claim, no subjectivity claim, and no
consciousness claim is made or implied anywhere in this disposition. The strongest
wording the program earns across its two measured neural phases is: N1 active paid
persistence as a necessary-condition substrate fact (Phase II), and sharing as a free
broadcast over sufficient content (Phase III) — both level (b)/(c) representational.
Phases IV–VII remain designs, re-scoped by the revision and gated by the
acquired-statistic question; none is a result. The level-(d)/(e) boundary is absolute.

---

## Sources

Read, not re-run, re-hashed, or edited: `PHASE3_VERDICT_v1.md` (G15),
`ACI_PHASE3_PROTOCOL_v1.md` (G10), `PHASE3_FINALS_SUMMARY_v1.md` (G13),
`PHASE3_INDEPENDENT_AUDIT_v1.md` (G14), `ACI_MASTER_RESEARCH_TREE_v3.md` (G16),
`ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2 + G16 §8), `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md`
(Q4), `ACI_THEORY_INDICATOR_MATRIX_v1.md` (Q5 + G16 §8), `ACI_TARGET_CONSTRUCT_v1.md`
(Q1), `CONSCIOUSNESS_ROADMAP_v1.md`, `MANUSCRIPT_ROADMAP_v1.md`,
`ACI_MISSION_AUDIT_v1.md` (Q0), `DEFINITIONS_CHARTER_v1.md` (claim levels). Frozen
results read, never re-run or re-hashed. This document is derived and is not hashed
into any study's `pre_run_snapshot.json`.
