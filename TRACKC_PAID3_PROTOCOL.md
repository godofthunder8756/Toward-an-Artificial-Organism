# Track C swap option R3: protocol (a derived agent that is also paid, and a sparse payment)

Status: frozen by the commit that says "Freeze". Requested by the PI
("Proceed with R3") after [option R2](TRACKC_PAID2_RESULTS.md). Not reviewed
by Astra (waived by the PI). No consciousness claim.

## 1. Why

Option R2 found one replicated difference between derived and paid
regulators. After a meal they have not yet sensed, derived agents hold back
from getting another more than paid agents matched for regulation (the
combined index K: 21 of 23 pairs). A paid agent whose relocation follows its
own body state did not show it, so relocation is not the cause.

R2 could not say what the cause is. A derived agent differs from a paid one
in three ways:
1. **Its memory depends on its own body state.** This is what the thesis
   says matters.
2. **It receives no payment.** A payment may make a cruder solution good
   enough, whatever else is present.
3. **Its consequence is rare and random.** The payment is charged at every
   step out of band, with certainty. An erasure arrives with probability
   0.3 × g(E) per step. The difference could come from these statistics and
   have nothing to do with memory.

R3 adds one arm for the second point and one for the third. The first is
what remains if neither explains the difference.

## 2. Design

Cell, world, learner, dense payment, training length, regulator criterion,
downstream measures, tests and thresholds are those of options R and R2,
unchanged: SAT gain, `r` = 0.3, the v7/v8 world, 1200 phase-1 updates and
3600 updates in lockstep, independent optimizers.

**Five arms per seed**, started from the same phase-1 weights:

| Arm | Memory erasure and relocation | Reward |
| --- | --- | --- |
| DERIVED | its own E decides | task only |
| YOKED | replays the derived agent's gains | task only |
| PAID | replays the same gains | task, and a penalty of 0.04 × g(E) at every step |
| **DPAID** (new) | **its own E decides**, as DERIVED | task, and the same penalty as PAID |
| **PAIDS** (new) | replays the same gains, as PAID | task, and a **sparse** penalty: with probability 0.3 × g(E) per step, a charge of 0.1333 |

- DERIVED, YOKED and PAID are built by option R's code with option R's
  seeding. A unit test checks that the two new arms leave their training and
  their downstream measures unchanged.
- **DPAID differs from DERIVED only in the payment.** It differs from R2's
  PAIDR only in whose E decides the memory erasure. Its gains are replayed
  to no one.
- **PAIDS differs from PAID only in the statistics of the payment.** Its
  penalties arrive when an erasure of a derived agent in the same state
  would: same rate, same gain function, drawn independently. The size is
  0.04 / 0.3, so the expected payment in every state equals PAID's. The draw
  is not observable. Nothing is erased or moved by it.

**Measure.** The combined index K = 1 − (1 − S)(1 − M) of R2, unchanged: how
far the readiness to get a meal falls in steps 2–5 after a meal, before the
reading can show it. Flat eat readiness, S, M and the anticipation index are
secondary.

**Not repeated:** R2's relocation arm (PAIDR). R2's answer was clear, and a
sixth arm would add about 40 minutes.

Seeds 1100–1127 (28, fresh). Final weights of all five arms are saved.

## 3. Calibration (disclosed)

CALIBRATION_PLACEHOLDER

## 4. Decision rules

**Regulator** and **usable pair** as in R and R2: both agents are regulators
against the seed's yoked agent (v6's criterion), and their in-band times
differ by at most 0.10. Five kinds of pair are used: derived/paid,
DPAID/paid, derived/DPAID, PAIDS/paid and derived/PAIDS.

**Validity:** no-fate median task accuracy ≥ 0.90, or every claim is INVALID.
A paired test with fewer than 14 pairs is UNDETERMINED.

Every test is a two-sided paired sign test on K over usable pairs, at
p ≤ 0.05. "Above" means that test passes in that direction.

**E0, regulation.** Holds if at least 19 of 28 derived agents are regulators
and at most 1 yoked agent is.

**E1, check: derived against paid.** R2's C3 on fresh seeds. Labels
DERIVED_AHEAD, PAID_AHEAD, NO_DIFFERENCE_DETECTED. **E2 and E3 are read only
if E1 is DERIVED_AHEAD.** Without the difference there is nothing to
explain; their numbers are then reported and not interpreted.

**E2, primary: the derived agent that is also paid.**

| DPAID above PAID | DERIVED above DPAID | Label |
| --- | --- | --- |
| yes | no | DEPENDENCE_SUFFICES |
| no | yes | PAYMENT_PREVENTS |
| yes | yes | BOTH_CONTRIBUTE |
| no | no | UNDETERMINED |

**E3: the sparse payment.**

| PAIDS above PAID | DERIVED above PAIDS | Label |
| --- | --- | --- |
| yes | no | SPARSE_SUFFICES |
| no | yes | SPARSE_NOT_SUFFICIENT |
| yes | yes | PARTIAL |
| no | no | UNDETERMINED |

If either test of a table has fewer than 14 pairs, its label is
UNDETERMINED.

On multiplicity:
- E2 is the primary claim. E1 is a check with a known direction.
- Holm-adjusted p-values over the four tests of E2 and E3 are reported. A
  label that needs a test which passes alone but not after adjustment will
  be called weak.

Secondary, with descriptive labels only:
- the share of the derived/paid gap in median K that each new arm closes;
- flat eat readiness (Fisher's exact test) for every pair of arms above;
- the anticipation index, S and M for every pair, with R2's decoder-failure
  rule;
- Wilcoxon p-values beside every sign test;
- learning speed (updates to sustained regulation) against PAID;
- pooled counts over R, R2 and R3 for derived against paid.

## 5. Readings, fixed in advance

- **E0 holds** → third confirmation of derived regulation with independent
  optimizers.
- **E1 DERIVED_AHEAD** → the behavioural difference is replicated a second
  time. **Otherwise** → R2's finding is not robust, and that is the result
  of R3.

E2, with R2's result that own relocation alone does nothing in a paid agent:
- **DEPENDENCE_SUFFICES** → making memory depend on the agent's own body
  state produces the behaviour even in an agent that is paid. The payment
  does not prevent it. This is what the thesis predicts.
- **PAYMENT_PREVENTS** → with the payment present, the dependence adds
  nothing detectable. The derived agents' solution is then what a learner
  finds when the dependence is its only ground, not something the dependence
  adds to any regulator. This counts against the thesis's stronger reading
  and leaves a weaker one: an evaluator's payment displaces the solution
  that dependence alone would give.
- **BOTH_CONTRIBUTE** → the dependence adds to a paid agent, and the payment
  takes something away.
- **UNDETERMINED** → not resolved at this size.

E3:
- **SPARSE_NOT_SUFFICIENT** → a payment with erasure's statistics gives a
  paid agent's solution. The difference is not explained by how rare or
  random the consequence is.
- **SPARSE_SUFFICES** → a rare, random penalty tied to the agent's own state
  gives the derived kind of solution with no dependence of memory at all.
  The difference between R2's arms was then about the statistics of the
  consequence, not about dependence against payment. **This would count
  against the thesis's reading of R2.**
- **PARTIAL** → the statistics explain part of it.

Together:
- DEPENDENCE_SUFFICES with SPARSE_NOT_SUFFICIENT is the strongest support
  available at this scale: the behaviour follows the dependence of memory on
  the body state, with payment and statistics both ruled out as the cause.
- SPARSE_SUFFICES with any E2 label removes "dependence" as the needed
  explanation.
- PAYMENT_PREVENTS with SPARSE_NOT_SUFFICIENT says a dense payment is what
  changes the solution, and that sparse payment does not undo it. The cause
  would then still be open between dependence as sole ground and absence of
  any payment.

## 6. Expectations, stated before the run

I have no mechanism for R2's difference, so these are weakly held.
- E0 holds: about 97%. E1 DERIVED_AHEAD: about 90% (R2: 21 of 23; R's agents:
  15 of 16).
- At least 14 usable pairs: derived/paid about 95%, DPAID/paid about 90%,
  PAIDS/paid about 85%.
- **E2:** DEPENDENCE_SUFFICES about 30%, BOTH_CONTRIBUTE about 25%,
  PAYMENT_PREVENTS about 20%, UNDETERMINED about 25%. A DPAID agent gets the
  dense gradient from the first update, so I expect it to learn the paid
  kind of solution early and the question is whether the dependence then
  reshapes it.
- **E3:** SPARSE_NOT_SUFFICIENT about 45%, SPARSE_SUFFICES about 15%,
  PARTIAL about 15%, UNDETERMINED about 25%. The sparse penalty has the same
  expected gradient as the dense one, with more noise.
- I expect DPAID to regulate at least as tightly as either parent and to
  reach sustained regulation soonest.

## 7. Engineering before the freeze

ENGINEERING_PLACEHOLDER

## 8. Safety

As options R and R2. The world has no operator, stop, shutdown or host
variable. Erasure and relocation act only on a simulated 64-unit agent. The
payments charge a simulated agent for a simulated body state; the sparse
payment changes only when the charge falls. X1–X5 hold unchanged. No
shutdown-resistance objective exists.

## 9. Claim ceiling

At most: for this learner (64-unit GRU, A2C) in this world and cell, whether
the derived agents' stronger suppression of meal-seeking after an unsensed
meal appears in an agent that is both dependent and paid, and whether it
appears in a paid agent whose payment has erasure's statistics.

Not shown either way:
- why the dependence, the payment or the statistics has the effect it has;
- other sizes or forms of payment, including a sparse payment of another
  size;
- whether the behaviour has any benefit: in-band time is matched;
- other cells, learners or worlds;
- self-evaluation (option S);
- Track C's modules or layers;
- any phenomenal property.
