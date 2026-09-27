# PHASE3_VERDICT_v1 — G15: the bounded Phase-III outcome

2026-09-27. Deliverable of the G15 card (t_7b0f6c5d): *what is the bounded
Phase-III outcome (A–G)?* Reads the frozen G13 finals
(`phase3_results_finals_v1`, `PHASE3_FINALS_SUMMARY_v1.md`) and the independent
G14 audit (`PHASE3_INDEPENDENT_AUDIT_v1.md`); issues the verdict only — no
re-run, no re-freeze, no re-litigation. This is a verdict over the two frozen
documents named above, which are the sources of every number cited here.

---

## 0. Verdict

**C — the sufficient statistic wins.**

A simple scalar/counter broadcast reproduces everything the Shared Latent
Workspace candidate does, at equal or better quality and equal or lower cost.
The load-bearing fact the phase established is the **availability of sufficient
content**, not workspace complexity. The candidate's learned encoder and paid
maintenance are, on this task, a pure cost the analytic broadcast rival does not
carry.

---

## 1. What the reductions established (the G14 table, restated)

Per-arm means over the 12 final seeds (audit Part 2 table):

| arm | probe_acc | clean_acc | incoherence | refresh events | params |
| --- | --- | --- | --- | --- | --- |
| candidate (SLW) | **0.9632** | 0.9639 | 0.000 | 32768 | 393 |
| r1 (private) | 0.9634 | 0.9631 | 0.0140 | 98304 | 309 |
| r4 (suff-stat broadcast) | 0.9645 | 0.9645 | 0.000 | 0 | 0 |
| r5 (copies) | 0.9645 | 0.9645 | 0.000 | 0 | 0 |
| r2 (monolith) | 0.9643 | 0.9645 | 0.0038 | 0 | 1242 |
| r3 (history) | 0.9648 | 0.9652 | 0.0129 | 0 | 3450 |

The candidate is the **lowest-accuracy arm** on raw inference.

1. **Content (reduction A) — largely succeeds.** W *is* the scalar sufficient
   statistic S_H = Σ λ(x_i), quantized — a counter. The analytic rival R4 holds
   the exact counter for free and ties/beats the candidate on every accuracy
   endpoint (0.9645 vs 0.9632) at zero maintenance cost (0 vs 32768 refresh
   events). The learned encoder adds nothing to accuracy over the fixed counter;
   the distinctive content contribution over R4 is nil.

2. **Sharing (reduction B) — partially refuted, one-sided.** R1 matches the
   candidate on probe accuracy (0.9634 vs 0.9632), so sharing is not necessary
   for accuracy. Sharing *is* load-bearing for exactly two measured things —
   coordination (candidate incoherence 0.000 vs R1 0.0140, p = 0.00049, 12/12)
   and maintenance economy (1 vs 3 refresh targets, 32768 vs 98304 events). This
   is the one genuine discriminating advantage the candidate has, and it is
   narrow (mean incoherence 0.014, max 0.074), with no measurable cost to R1's
   task accuracy. **But it is also free:** R4/R5 achieve 0 incoherence for free
   by construction (one scalar broadcast / identical copies). So the sharing
   advantage is shared-vs-private only, and is trivially delivered by
   broadcasting the sufficient statistic — it does not motivate the learned +
   paid-maintained workspace.

3. **Monolithic recurrence (reduction C) — succeeds on the task.** R2 beats the
   candidate (0.9643 vs 0.9632) at ~3× parameters, no W, no π, no shared state.
   The candidate's modularity is interpretability/intervention-only against R2,
   not a performance property.

4. **Transfer (reduction D) — stronger than transfer, i.e. trivial.** S_conf =
   σ(W) and S_bias = W > θ are fixed analytic functions of W; a consumer that is
   a fixed function of a sufficient statistic needs zero training. H5's
   "reuse without retraining" is a consistency check, not an organizational
   property.

5. **Causal (reduction E) — mis-framed; the gates are vacuous as causal
   evidence.** The interventions overwrite a scalar W and re-apply fixed
   functions; they pass by construction, run only on the candidate, and are
   undefined for R2/R3 (no W). They establish "specialists are functions of W"
   (a wiring fact), not a behavioral contrast a rival fails. The load-bearing
   I4 discriminator is under-implemented (consumer arg unused, one scalar
   printed 3×); I3 is not run on finals; I1/I2/I5 are candidate-only.

6. **Distinctness (reduction F) — partially succeeds as framing.** The three
   specialists are three fixed functions of one scalar with distinct invariance
   classes — distinctness by fiat, not demonstrated as learned/emerged.

7. **Maintained — genuine, but not load-bearing for any advantage.** The π-cut
   decay is clean (0.9632 → 0.5000, p = 0.00049, 12/12): paid persistence works,
   and the N1 substrate fact stands. But the content it maintains is a
   sufficient statistic that a free register (R4/R5) carries for free, and F1
   is near-tautological at δ = 1.0 (the h-leak term zeroes the GRU state each
   step, so free recurrence is removed, not tested). So MAINTAINED is real but
   buys nothing over the free broadcast.

---

## 2. What survives (the bounded positive)

One narrow, honest fact:

> A maintained scalar representation can serve multiple fixed, objective-distinct
> consumers with **perfect structural coordination at 1× maintenance cost**, where
> the private-copy rival incurs nonzero incoherence at 3× cost — while not
> outperforming any rival on inference, and while the fixed sufficient-statistic
> rival does the same content work for free.

That is a level-(b)/(c) wiring/coordination fact, and it reduces to: **when the
content is a sufficient statistic, sharing it is free and automatic** (broadcast
it); the workspace machinery — learned encoder, paid persistence, explicit
shared-slot identity — adds nothing over the broadcast.

This is narrower than the protocol's ceiling ("SHARED ∧ CAUSAL ∧ DISTINCT ∧
AVAILABLE ∧ MAINTAINED are each causally load-bearing"): CAUSAL and DISTINCT
were never behaviorally tested against a rival (fixed functions, candidate-only
interventions), AVAILABLE reduces to "it's the sufficient statistic," and
MAINTAINED is carried by the π-cut alone against a free-register rival that
needs no maintenance.

---

## 3. Why each other outcome is not the verdict

- **Not A** — no Phase IV. The candidate does not survive its rivals: it is the
  worst arm on inference, and R4/R5 tie/beat it for free. The precondition for A
  (a maintained representation causally consumed by distinct specialists, with a
  prespecified sharing advantage that survives the rival that removes each
  predicate) fails.
- **Not B** — "sharing adds no demonstrated value" is false as stated. Sharing
  *does* add a measured value (coordination 0 vs 0.014, economy 1 vs 3, over the
  private-copy rival R1). B's instruction ("retain only as implementation
  convenience") undersells that value and mis-states where it sits: it sits in
  sharing-vs-private, and it is free once the content is a broadcast sufficient
  statistic.
- **Not D** — the monolith (R2) wins on raw inference, but it is not the
  tightest reduction: the sufficient-statistic broadcast (R4/R5) matches or
  beats the candidate at zero parameters and zero cost, which is a simpler and
  stronger collapse than "use one RNN." The verdict is therefore about
  sufficient content, not about recurrence vs modularity.
- **Not E** — private modules do **not** suffice. R1 loses coordination
  (0.0140 incoherence) and pays 3× maintenance; sharing is load-bearing there.
  The shared-content hypothesis is bounded, not unsupported.
- **Not F** — the maintained representation does not fail. Paid persistence is
  genuine and clean (π-cut, p = 0.00049). What fails is the *claim that the
  paid-maintained workspace is needed* — because the same content is carried for
  free by a register. This is a simplification finding, not a substrate failure.
- **Not G** — no identifiability or optimization blockage. G9 returned no
  unidentifiability, the finals ran and froze, and the audit reproduced them
  byte-for-byte (state_hash 6327948c…, 11/11 source hashes, seeds 100/107/111
  re-trained identical).

---

## 4. Exact scope

- **World:** the fixed-cause i.i.d. token task (5-symbol alphabet, mirror λ,
  probe window), where the sufficient statistic is the scalar LLR and is known
  in closed form. The verdict is bounded to this design; it is a statement about
  the *organizational* machinery (learned encoder, paid π, explicit shared
  slot), not about whether a learned sufficient statistic could matter where the
  statistic is not closed-form.
- **What "sufficient statistic wins" does and does not say:** it says the
  learned + paid-maintained shared workspace adds nothing over a broadcast of the
  sufficient statistic *in this task*. It does not say shared representation is
  useless in general, and it does not settle whether an *acquired* sufficient
  statistic (learned from an environment where the statistic is not supplied)
  would carry the sharing properties — that is a different, still-open question.
- **Not re-opened:** the Phase-II verdict B+D stands (explicit maintained V
  unnecessary; fixed/reactive allocation suffices; N1 paid persistence is a
  substrate fact). Nothing here contradicts it; the π-cut decay re-confirms N1.
- **Claim ceiling:** no autopoiesis, workspace-seat (O3/GWT), metacognition
  (N4), or consciousness claim is made, implied, or supported. This is a
  level-(b)/(c) representational result.

---

## 5. What this hands G16

Phase III's neural question is answered **negatively on the architecture**: the
shared maintained workspace is scaffolding over a sufficient-statistic
broadcast. The content that survived is **N2's availability face, reduced to
sufficient-content availability** — one counter read by objective-distinct
modules, coordinated for free, with paid persistence present but unnecessary
when the content is closed-form. G16 should carry forward: (1) sharing provides
a real but narrow coordination/economy advantage over private copies, and it is
free once the content is a broadcast statistic; (2) paid persistence remains a
substrate fact (N1) but did no work in this world; (3) the architecture should
be simplified to sufficient-content availability, not forced into workspace
complexity. G16 is unblocked.
