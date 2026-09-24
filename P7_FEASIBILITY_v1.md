# P7 — integration and reliability prerequisites: feasibility decision

2026-09-24. P7's deliverable (task `t_4aefbe19`): assess (1) whether the tested cognitive
mechanism composes with the maintained organizational architecture, and (2) whether there is
a distinct, identifiable reliability question beyond the first-order posterior. This is a
feasibility assessment, not a study — no organism-scale run, no seeds, no freeze. Every claim
below is read from the frozen/engineering record and the runner code; no frozen artifact is
edited, re-run, or re-hashed.

The mechanism under assessment is the maintained cause-estimate, in its two current forms: the
one-bit estimate (AC107/108, K6/K7) and its generalization to a maintained integer counter
with supplied likelihood weights (the AC112/AC113 two-counter and its single-counter rival).
The operative result from P6 (`AC113_RESULTS_v1.md`, frozen 6400–6407) is F1 equivalence:
heterogeneous (two-dimensional, non-integer) weighting is NOT load-bearing at organism scale —
a maintained single integer counter matches the two-counter at both regimes' optima. The P2
conclusion (a maintained integer counter suffices) survives the heterogeneous likelihood
ratio. The estimate remains informative and causally effective (V2), but its graded/weighted
form buys nothing over the integer form.

---

## 1. Integration: does the mechanism compose with the maintained architecture?

Two questions, kept separate as the card requires.

### (1) Does organizational maintenance sustain the mechanism's useful operation?

**Yes — through the paid acquisition/update write, not through in-window repair.** The
load-bearing maintenance is `bel_write` (the atomic 7-replica write at open in-window
contacts), which AC108 (both directions, 7/7 gates) and AC110 (G2 accuracy 16/16, G3 use 16/16)
established. AC110 cut the estimate's only repair path and correctness/use were unchanged —
correctness rides reacquisition, and the repair path is unreachable in the 96-tick window under
the frozen ambient 1e-4 damage (a single bit contributes ≤3 minority replicas, below the
whole-bank ≥4 trigger). Repair IS load-bearing for post-window storage protection (AC110 G4:
maintained 16/16 vs no_repair 8/16). The counter forms generalize the estimate and use the
identical storage pattern: dead-rule free bits, majority-read, W-gated writes (`counter_write`
refuses beyond `ac95._cap`), observer-discard clean (AC113 V3 16/16 per-tick byte-identity).
So the operation is sustained by maintenance in the only sense the evidence licenses: the paid
acquisition/update write, plus repair for post-window storage — not an exercised ongoing-repair
loop inside the window (P3 point 6, N1 point 3).

### (2) Does that operation affect organizational behaviour or viability?

**Behaviour — yes, causally. Viability — no, seed-bounded, and not required.** AC108
`force_machinery` reverses the move-side adaptation 16/16 and collapses production/viability
16/16; AC113 V2 shows the counter's accumulated content drives a false-relinquishment under cut
that the read-forced scramble cannot (4/16 vs 0/16). The estimate's content is behaviourally
causal by single-flag intervention. The survival advantage is seed-bounded (AC107 Q4; AC108
12/16; AC113's collapse tail is a death on 2/16 finals, and post-cause income shows no graded
advantage). The card names survival advantage as one possible outcome, not a prerequisite, so
this is a finding, not a defect of the mechanism.

### Composition verdict

**The mechanism composes; the direct channels are clean.** AC111 (I1, frozen 6300–6307)
verified both direct channels under a live reconstruction: the estimate bit is excluded from
`reg_from_active` (the `bel_off` exclusion is load-bearing and exercised, not merely declared),
and the allowance-42 budget never starves reacquisition (it defers only reconstruction;
`bel_write`/`counter_write` are W-gated). G2/G4/G6 pass. The full composition retains the one
named residual: the corrupted contact rule re-schedules reacquisition, producing a
seed-dependent, survival-neutral behavioural interference (G3/G5 12/16 — the 6306 never-biting
cut and 6307 spurious-then-recovered relinquishment). That residual is a contact-schedule
perturbation, not a storage/spending interaction, and is already on record as a robustness
question, not a composition failure.

**No new integration test is authorized.** The counter bits live in the AC96 streak free-bits
(`streak_offs`), which AC96/AC99–AC105 already composed with corruption + reconstruction; the
estimate bit's exclusion was exercised live by AC111; and the counter bits are in the same
exclude set (`exclude_offs = reg_offs + streak_offs + [bel_off]`, ac112.py:490). The one
unexercised detail — that the counter's own bits survive a *live* reconstruction (AC113 ran
`corrupt=False`, so no reconstruction fired) — is closable by a single unit-level assertion
(reconstruction target at the counter offsets equals what `reg_from_active` would write,
AC111 rule 1), not by a study. Nothing here warrants spending a frozen experiment on the
storage channel.

---

## 2. Reliability: is there a distinct question beyond the first-order posterior?

**Yes — distinct and identifiable.** The first-order posterior is `P(cause | history)`, now
shown equivalent to an integer counter (P2) with its heterogeneous weighting non-load-bearing
(AC113 F1). The reliability tier is a state about a *different* object: the evidence channel's
own diagnostic value — the residual yield ε (equivalently `P_YIELD`), which sets how much
weight each observation deserves. It is a property of the estimator's inputs, not of the cause.
This is C4 §11's named content/reliability separation, K8's reopening condition 2 ("degrade
the observation interface"), and P4 §9's named next-after. Its load-bearing claim is: when the
diagnostic value *varies across distinguishable conditions*, a maintained estimate of it
restores/selects the discriminating weighting that a frozen (supplied) value provides.

**What AC113 does and does not say about it.** AC113 falsified the *first-order* heterogeneous
weighting — with ε frozen. It did not touch the reliability tier. Per the card, this failure is
not a global verdict on the reliability direction. But AC113 did record a specific wall that
the reliability tier's own premise must clear: a decision-theoretic weighting advantage does
not transfer to organism scale when the per-action economics differ (rule 1 — a false
relinquish refreshes the entry rather than costing R=4, and holding has an ongoing entry-expiry
cost). The reliability tier's premise — "an estimated weight restores a discriminating
weighting a frozen weight supplies" — is a decision-theoretic claim of exactly the kind AC113
just showed fails to transfer at organism scale.

### Feasibility decision on reliability

**Distinct and identifiable: yes. Currently runnable as an organism-scale metacognition study:
no — not without first clearing AC113's wall at the harness level.** The reliability question
is not blocked on ceiling accuracy anymore (K8's wall is crossed: the occluded world has real
error variance — AC110 G4 drift, AC113's 2/16 collapse and cut false-relinquishments). It is
deferred on a different, specific basis: the premise that a graded/weighted magnitude becomes
load-bearing at organism scale has now been falsified twice from the first-order side (P2
homogeneous, AC113 heterogeneous), and the reliability tier inherits the same per-action-
economics transfer risk. Authorizing the organism-scale study now would violate the card's own
constraint ("do NOT automatically launch a metacognition study").

### Candidate discriminating test (warranted, at harness level only)

The warranted next step is a **decision-theoretic probe with the corrected organism-scale
economics**, in the C2/C4/P4 pre-implementation discipline, not an organism-scale run:

1. Model the two causes with ε **varying across two distinguishable conditions** (e.g. ε high vs
   low, signalled by an observation the organism already receives, no hidden label).
2. Use the **corrected per-action economics** AC113 measured: a false relinquish refreshes the
   entry (no R=4 penalty), holding a stale route costs ongoing lost income with entry-expiry
   churn. Do not import C4's abstract `R=4` model.
3. Ask: does a policy that **estimates ε** (a second-order state) beat the strongest policy
   with a **frozen ε**, on decision utility — in a regime where the frozen value is wrong for
   one condition?

**Falsification (both meaningful):** if the frozen-ε policy matches the estimated-ε policy
(the second-order state buys nothing), the reliability tier is **deferred with a named wall**
— the organism's per-action economics, not its information, already fix the decision, exactly
as AC113 found for the weighting. If the estimated-ε policy wins, the reliability tier is
**authorized** for a bounded organism-scale study (a maintained ε-estimate in the free-bit
pattern vs a frozen-ε rival, gated on decision utility not survival).

This probe is cheap (no runner, no seeds), respects "no automatic metacognition study," and
does not treat AC113's failure as a verdict on the direction — it makes the direction's
premise earn its keep before any organism-scale spend.

---

## 3. What this hands to S0

- **Composition:** established to the level the evidence licenses — maintenance sustains the
  mechanism via the paid acquisition/update write (repair for post-window storage only); the
  operation is behaviourally causal but not viability-advantageous (seed-bounded, not required).
  No new integration study.
- **Reliability:** a distinct, identifiable question (the estimator's own diagnostic value),
  deferred not on ceiling accuracy but on the AC113 per-action-economics wall; the next step is
  a harness-level probe (corrected economics, varying ε, estimated-vs-frozen weight), whose
  outcome decides whether the reliability tier is authorized or deferred with a named wall.
- **Neither verdict is a global one:** AC113's F1 and K8's block both bound the first-order
  tier; the second-order reliability direction remains open, gated on a single cheap probe.

## Sources

`AC113_RESULTS_v1.md`, `AC113_PROTOCOL_v1.md`, `AC112_ENGINEERING_v1.md`, `ac112.py`,
`AC111_RESULTS_v1.md`, `AC110_RESULTS_v1.md`, `AC107_RESULTS_v1.md`, `AC108_RESULTS_v1.md`,
`C2_TASK_DESIGN_v1.md`, `C4_TASK_DESIGN_v1.md`, `C4_P2_EQUIVALENCE_v1.md`,
`P4_COGNITION_CONTINUATION_v1.md`, `P3_CORRECTIONS_v1.md`, `K8_DISPOSITION_v1.md`,
`S1_SYNTHESIS_v2.md`, `CONSCIOUSNESS_ROADMAP_v1.md`. This document is derived and is not hashed
into any study's `pre_run_snapshot.json`.
