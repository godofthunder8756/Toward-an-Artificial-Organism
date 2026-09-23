# K8 — reliability monitoring: BLOCKED (prerequisite absent — the first-order estimate is ceiling-accurate)

2026-09-22. Disposition note, not a study. No experiment run, no seeds, no protocol.
This card was conditional on K6's feasibility decision; that decision is explicit in K6's
handoff and is verified here against the frozen record. The branch is blocked, with
reopening conditions below.

## 1. The question and its prerequisite

K8 asks: does a **distinct reliability estimate** — a second-order state about the
reliability of the first-order cause-estimate — **predict errors** and **regulate
information gathering or action**, beyond simple uncertainty heuristics (the fixed
failure-streak, the raw counter)?

The card's stated prerequisite (K6's feasibility decision) is that K6 establish
"a functioning estimate with MEANINGFUL VARIATION in accuracy." That variation is what
gives a reliability state something to do: it must be able to predict *when the estimate
is wrong* (so there must be wrong instances) and to regulate *differently* between
reliable and unreliable regimes (so accuracy must actually vary across the task). A
reliability estimate over an estimate that is never wrong is a constant, and a constant
is trivially matched by a simple heuristic — the test would be vacuous.

## 2. The measured fact (K6, frozen)

The maintained cause-estimate is **ceiling-accurate**:

- `cut` (E_machinery): reads E_machinery at the window end in **16/16** individuals.
- `move` (E_world): reads E_world at the first drop in **16/16** individuals.
- post-intervention mistakes: **0** across all 32 individuals
  (`AC107_RESULTS_v1.md` §1). Engineering (K5, seeds 0-7) measured the same: 0 mistakes.

The estimate is never wrong. This is not a partial or noisy success — it is a
*perfect* discriminator, because the two causes produce disjoint action-observation
histories once the estimate reads the organism's own `(bound, used_held, productive)`
triple (K4's identifiability result, K5's implementation).

The only residual variance in the estimate's behaviour is **not** accuracy variance:

- **Latency** — the estimate reaches the correct value 13-46 ticks after the
  intervention, dominated by when the program happens to contact channel 1, not by any
  discrimination delay. It is never wrong en route.
- **Seed-bounded survival** — the candidate dies on 6002 in `move`, but that individual
  still *reads the correct cause* (E_world, drops at 8235); it dies because the
  frozen streak threshold (6) drops too slowly for that seed's economy, not because the
  estimate misattributed. This is an economic/viability variance, not an accuracy one.

There is therefore **no error variance** for a reliability state to predict, and **no
reliable-vs-unreliable regime** for it to regulate. K8's support condition ("reliability
predicts errors and causally regulates behavior") cannot be met in this world.

## 3. How this differs from C3 (and why it matters)

This is the **mirror image** of the earlier C3 disposition (`C3_DISPOSITION_v1.md`,
later superseded in part by `AC106_ERRATA_v1.md`):

- **C3 closed** because the first-order estimate carried **no cause information** — it
  could not distinguish the two causes at all, so a reliability estimate had nothing to
  predict.
- **K8 blocks** because the first-order estimate now carries **perfect cause
  information** — it distinguishes the causes with zero error, so a reliability estimate
  again has nothing to predict.

Both are the same failure of the *premise* ("meaningful variation in accuracy"), reached
from opposite directions. The K4/K5/K6 work removed C3's confound and produced a
ceiling-accurate estimator; in doing so it did **not** produce the error variance K8
needs — it eliminated the error that a reliability state would exist to predict.

## 4. Disposition

**K8 is BLOCKED**, not closed and not falsified. The first-order estimate is a positive
result (perfect discrimination, causally coupled to maintenance per K7); the
second-order reliability question is *untestable as specified* in this world because its
premise — an estimate that is sometimes wrong — does not hold.

**Reopening conditions (explicit).** Re-open K8 when a mechanism or world change
introduces a **non-zero, non-trivial error rate** in the first-order cause-estimate,
such that a reliability state could (a) predict the errors from the organism's own
observations and (b) regulate information gathering or action differently from a simple
uncertainty heuristic. Concrete routes, each a named mechanism/information change with a
new discriminating prediction (per K6's successor-authorization rule):

1. **Relax the perfect identifiability** K4 established — a partially-observed task in
   which the two causes produce *overlapping* action-observation histories, so the
   update rule sometimes misattributes.
2. **Degrade the observation interface** — noise on the `(bound, used_held, productive)`
   triple or on the observation bits, so a correct rule occasionally misfires.
3. **Add a third cause or an ambiguous case** that the current discriminator
   structurally misattributes.

In every route the error must be (i) *predictable in principle* from the organism's own
observations (otherwise reliability is trivially vacuous) and (ii) *behaviourally
consequential* (the error changes an action or a survival outcome, otherwise reliability
has nothing worth regulating). A route that merely re-runs the unchanged AC107 design
must not be authorized — the design is ceiling-accurate by construction.

## 5. Non-falsification boundary (constraint honored)

This block does **not** falsify reliability monitoring, metacognition, or the broader
consciousness / HOT-2 direction. The first-order estimator *succeeded* — it discriminates
perfectly and is causally coupled to its maintenance (K6 Q1/Q3, K7). The reason K8 cannot
run is that the estimator is *too* good to exhibit error variance, which is a property of
the current task design (perfect identifiability), not a failure of the reliability
hypothesis. Reliability monitoring remains an **untested hypothesis**, not a refuted one.

## 6. What this hands to K9

- Reliability monitoring is **untested (blocked, not falsified)**; the reason is the
  first-order estimate's ceiling accuracy, which follows from the task's perfect
  identifiability (K4).
- The HOT-2 metacognitive-monitoring mapping is therefore open at the **reliability
  tier**: discrimination (K6) and coupling (K7) are established, but the
  "monitor grades its own representation's reliability" tier has no testable instance
  until an error-variance mechanism exists.
- The next bounded step toward that tier is the reopening route in §4, to be weighed by
  K9 against the rest of the evidence — not authorized here, where the prerequisite is
  absent.
