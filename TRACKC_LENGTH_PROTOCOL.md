# Track C swap, option T: protocol (training length in the base cell)

Status: frozen by the commit that says "Freeze". Requested by the PI
("Proceed with Option T") after [option G](TRACKC_GENERAL_RESULTS.md). Not
reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Why

Options R2 to R4 found, in one cell, that derived regulators hold back after
a meal they cannot yet sense far more than paid regulators matched for
regulation (K higher in 81 of 88 pairs over R to R4). Option G then found:
- with a 128-unit learner the difference is there but about half the size,
  because paid agents' K rose;
- with a two-variable body, trained three times as long, it is absent.

One hypothesis fits all three cells: the arms differ in how readily a
learner comes to hold back after a meal, not in whether it can, and more
training closes the gap. If that is right, the downstream claim of the swap
line is a claim about learning speed. Option G could not test it, because
its two-variable cell changed the body and the training length together.

This protocol tests it where the difference was found: the base cell,
unchanged, trained three times as long, with K measured along the way.

## 2. Design

One cell: the base cell of options R to R4 (64-unit recurrent core, one body
variable, the 7×7 world). World, learner, learning rate, batch, rate,
payment weight, regulator criterion, measure, tests and thresholds are
unchanged. Each agent has its own optimizer. 28 fresh seeds, 1500–1527.

**Three arms per seed**, started from the same phase-1 weights (1200 updates
with fate off), trained in lockstep:

| Arm | Memory erasure and relocation | Reward |
| --- | --- | --- |
| DERIVED | its own body state decides | task only |
| YOKED | replays the derived agent's gains | task only |
| PAID | replays the same gains | task, and a penalty of 0.04 × the gain of its own body state at every step |

**Three measurement points:** after 3600, 7200 and 10 800 phase-2 updates.
- 3600 is the training length of options R to R4. Up to and including the
  measurement at that point, a seed's job is the base-cell job of R2 to R4
  and G: same code path, seeds and random streams. A unit test checks that
  the records, weights and probe results are identical.
- 10 800 is the length option G gave its two-variable cell.
- At each point the three agents are evaluated as in every earlier run (two
  fresh episodes, no learning; followers replay the derived agent's gains),
  and their weights are copied. Training then continues from a fresh episode
  with the same agents, optimizers and streams.
- The downstream probes for all three points run on the copied weights
  after training has ended, so they cannot affect training.

**Measure.** K = 1 − (1 − S)(1 − M) of R2, on frozen weights with erasure
off. S is how far the readiness to eat falls in steps 2–5 after a meal,
before the reading can show it; M is the same for moving toward the nearest
visible item.

**Regulator** and **usable pair** are judged at each point from that point's
evaluation: both agents are regulators against the seed's yoked agent, and
their in-band times differ by at most 0.10.

Known limits of the design:
- It tests training length in the base cell only. It does not rerun the
  two-variable cell at a shorter length (that cell does not regulate at the
  base length), so it cannot show directly why option G's B2 showed no
  difference; it can show whether training length alone is enough to
  explain it.
- The same agents are measured three times, so the three points are not
  independent samples. The tests below are within-seed.
- The sets of usable pairs at different points can differ.
- No control arms (DPAID, PAID0, DNOISE) are rerun.
- Option G found that most of what K measures in a two-variable world is
  not specific to the fed variable. This cell has one kind of meal, so that
  question cannot be asked here; K is used as R2 defined it.
- If paid agents' K rises, the run does not say what makes it rise.

## 3. Calibration

None. Every setting is the base cell's, and the one new number, the length,
is taken from option G's two-variable cell. There is nothing to tune, and
nothing would be tuned if regulation drifted over the longer run: that
would be a result (T0).

One timing run was made at the final sizes on a calibration-range seed
(9700): phase 1 and then 100 and 300 phase-2 updates, training stage only.
Only the time was read: 198 s for phase 1 and 100 updates, with other work
sharing the machine. The 300-update reading was lost with the task's output
file and was not repeated. From this and the rates of R2 and G, a seed
should take about 55 minutes and the run about 6.5 hours on 4 cores.

## 4. Decision rules

**Validity:** no-fate median task accuracy ≥ 0.90, or every claim is
INVALID. A paired test with fewer than 14 pairs is UNDETERMINED.

**T0, regulation.** Holds if, at 3600 and at 10 800, at least two thirds of
the derived agents (19 of 28) are regulators and at most 1 yoked agent is.

**T1, the check at 3600.** A two-sided paired sign test on K, derived
against paid, over the pairs usable at 3600, at p ≤ 0.05. This is the test
of R2 to R4 on fresh seeds. Labels DERIVED_AHEAD, PAID_AHEAD,
NO_DIFFERENCE_DETECTED, UNDETERMINED.

**T2 (primary), the same test at 10 800,** over the pairs usable at 10 800.

**T3, the change.** For each seed usable at both 3600 and 10 800, the
within-pair difference D = K(derived) − K(paid) at each point. A two-sided
sign test on D at 10 800 against D at 3600, at p ≤ 0.05. Labels NARROWS,
WIDENS, NO_CHANGE_DETECTED, UNDETERMINED.

**Overall:**

| T1 at 3600 | T2 at 10 800 | T3 | Label |
| --- | --- | --- | --- |
| DERIVED_AHEAD | DERIVED_AHEAD | not NARROWS | PERSISTS |
| DERIVED_AHEAD | DERIVED_AHEAD | NARROWS | PERSISTS_SMALLER |
| DERIVED_AHEAD | NO_DIFFERENCE_DETECTED or PAID_AHEAD | NARROWS | CLOSES |
| DERIVED_AHEAD | NO_DIFFERENCE_DETECTED or PAID_AHEAD | not NARROWS | UNRESOLVED |
| NO_DIFFERENCE_DETECTED or PAID_AHEAD | not UNDETERMINED | any | NOT_REPLICATED |
| UNDETERMINED at either point | | | UNDETERMINED |

On multiplicity: T1 is a check. Holm-adjusted p-values over T2 and T3 are
reported. A label that needs a test which passes alone but not after
adjustment will be called weak (PERSISTS needs T2; PERSISTS_SMALLER needs
T2 and T3; CLOSES needs T3). "No difference detected" is not equivalence:
an exact interval for the median within-pair difference is reported at
each point.

Secondary, with descriptive labels only, all computed by the scorer:
- the same test at 7200;
- each arm's own K at 10 800 against 3600, over agents regulating at both
  (does paid agents' K rise; does derived agents' K move);
- median K per arm and the number of agents below 0.5 at each point;
- an exact order-statistic interval (at least 95%) for the median
  within-pair difference at each point, and the change in D on all seeds
  without the matching rule;
- at each point: K on all seeds, K on pairs within 0.05 in band, S and M
  separately, flat eat readiness, the in-band difference within usable
  pairs, the rank correlation of K with in-band time, regulation with
  erasure off;
- regulators at every point, and learning speed.

## 5. Readings, fixed in advance

- **T0 does not hold** → derived regulation does not last (or is not
  reached) over the longer run in this cell. That outranks T1 to T3.
- **NOT_REPLICATED** → the base-cell difference failed its fifth test at
  the base length. T2 and T3 are reported but the run cannot speak to
  training length.
- **PERSISTS** → three times the training does not shrink the difference
  in the cell where it was found. Training length alone does not explain
  its absence in option G's two-variable cell; something else about that
  cell does. The "stage of learning" hypothesis is not supported.
- **PERSISTS_SMALLER** → the difference is still there and is shrinking.
  Whether it would close with more training is open; the secondary
  interval and the 7200 point say how fast it moves.
- **CLOSES** → in the base cell the difference is a stage of learning.
  The downstream claim of R2 to R4 should then be stated as a difference
  in how soon the behaviour is learned, and option G's two-variable result
  is what that predicts.
- **UNRESOLVED** → not detected at the end, without a detectable change.
  Read from the intervals; no claim either way.
- **UNDETERMINED** → not resolved at this size.

Whatever the label, a paid arm whose own K rises between 3600 and 10 800
(secondary) is evidence that paid agents keep acquiring the behaviour after
they already regulate.

## 6. Expectations

Written before any code for this option was run:
- **T0** holds at both points: about 85%. Regulation past 3600 updates with
  independent optimizers has not been run in this cell.
- **T1** DERIVED_AHEAD: about 88%.
- **T2:** DERIVED_AHEAD about 60%, NO_DIFFERENCE_DETECTED about 25%,
  UNDETERMINED about 12%, PAID_AHEAD about 3%.
- **T3:** NARROWS about 35%, NO_CHANGE_DETECTED about 55%, WIDENS about 5%,
  UNDETERMINED about 5%.
- **Overall:** PERSISTS about 40%, PERSISTS_SMALLER about 20%, CLOSES about
  15%, UNRESOLVED about 12%, NOT_REPLICATED about 10%, UNDETERMINED about
  3%.
- **Paid agents' median K at 10 800:** about 0.6; I would be surprised
  below 0.45 or above 0.8. At least 0.10 above their median at 3600: about
  40%.
- **Derived agents' median K** changes by less than 0.05 between 3600 and
  10 800: about 75%.

Reasons. For persistence: paid agents in the base cell already regulate at
about 0.94 in band without holding back, so the pull toward doing so is
small; and in option G, agents that had regulated for longer did not have
clearly higher K (post hoc, weak). Against: 128-unit paid agents reached
0.79 with the base training, and two-variable paid agents 0.90 with three
times as much.

## 7. Engineering before the freeze

- **Smoke run:** two seeds, horizon 100, 10 phase-1 updates, points at 20,
  40 and 60 updates. It checked the arms, the three points, the probes,
  weight saving, report and rescoring.
- **Resume:** a smoke run with its outputs and one finished record removed
  continued from the kept record and produced the same records as the
  uninterrupted run. The final run is continued by repeating its command.
- **Tests:** five new unit tests (110 in total). They cover:
  - the per-seed record: that everything up to the first point equals the
    base-cell job of R2 to R4 and G (evaluation, weights, curves, probe
    results); that training continues past it; that followers replay the
    derived agent's gains at every point; that the probes do not change
    training;
  - the view of a run at one point, and the interval for a median;
  - the decision rules on synthetic data: T0, every T3 label, every overall
    label, the matching rule at both points, INVALID, and a training-only
    record;
  - the final configuration (fresh seeds, the three points, unchanged
    thresholds), and the absence of operator variables.
- No final seed has run, and no seed has been trained past 300 updates
  under this protocol.

## 8. Safety

As options R to R4 and G. The world has no operator, stop, shutdown or host
variable. Erasure and relocation act only on a simulated 64-unit agent.
The only change from the base cell is that training runs longer. X1–X5
hold unchanged. No shutdown-resistance objective exists.

## 9. Claim ceiling

At most: whether, in the one cell where it was found, the derived/paid
difference in post-meal suppression persists, shrinks or closes when
training is three times as long, for this learning rule (A2C with a GRU
core).

Not shown either way:
- why the difference arises, or what makes paid agents' K move if it does;
- what happens beyond 10 800 updates;
- why option G's two-variable cell showed no difference, except whether
  training length alone could account for it;
- larger learners, other learning rules, other architectures;
- whether the behaviour has any benefit: in-band time is matched;
- what K is specific to (option G, §5);
- Track C's modules or layers;
- any phenomenal property.
