# Track C swap, option G2: protocol (specificity of post-meal suppression)

Status: frozen by the commit that says "Freeze". Requested by the PI
("Proceed with G2") after [option T](TRACKC_LENGTH_RESULTS.md). Not reviewed
by Astra (waived by the PI). No consciousness claim.

## 1. Why

Option T showed that the base-cell difference in K between derived and paid
regulators is a stage of learning: found at 3600 updates, gone at 10 800.
After it, the swap line has no evidence that a derived and a paid regulator
end up doing anything different.

One pointer in the other direction is left, and it is post hoc. In option
G's two-variable cell (B2), trained for 10 800 updates:
- K did not differ between the arms.
- A meal of one kind suppressed the readiness for the other kind as well
  ("other-meal K"), in both arms.
- Own-meal K minus other-meal K was larger in the derived agent in 21 of 25
  usable pairs (p = 0.0009; medians 0.18 against 0.10). That is, derived
  agents' suppression was more specific to the variable that had been fed.

That contrast was computed after option G's results were seen. This
protocol tests it on fresh seeds, with the claim fixed first.

Option T also changes what a positive result would mean. In B2 derived
agents came to regulate later than paid agents (a median of 6250 updates
against 4540, paid sooner in 28 of 28). So at 10 800 updates the two arms
are at different stages, and a difference there could again be a matter of
timing. The design therefore trains on past B2's length and asks whether
the contrast, if found, is still there.

## 2. Design

One cell: option G's B2, unchanged. Two body variables, each with its own
items, its own delayed reading, its own wear and the same band; a 64-unit
recurrent core; each variable out of band is its own erasure hazard. World,
learner, learning rate, batch, rate, payment weight (0.04), regulator
criterion, probe sizes, tests and thresholds are option G's. Each agent has
its own optimizer. 28 fresh seeds, 1600–1627.

**Three arms per seed**, started from the same phase-1 weights (1200 updates
with fate off), trained in lockstep:

| Arm | Memory erasure and relocation | Reward |
| --- | --- | --- |
| DERIVED | its own body state decides | task only |
| YOKED | replays the derived agent's gains | task only |
| PAID | replays the same gains | task, and a penalty of 0.04 × the gain of its own body state at every step |

**Four measurement points:** after 3600, 7200, 10 800 and 14 400 phase-2
updates.
- **10 800 is the primary point.** It is the length of option G's B2, where
  the contrast was seen.
- **14 400 is the last point,** a third more training, for the question of
  whether the contrast is a stage.
- 3600 and 7200 are descriptive. In option G few B2 agents regulated that
  early, so few usable pairs are expected there.
- At each point the three agents are evaluated as in every earlier run (two
  fresh episodes, no learning; followers replay the derived agent's gains)
  and their weights are copied. Training then continues from a fresh
  episode with the same agents, optimizers and streams, as in option T.
- The downstream probes for all points run on the copied weights after
  training has ended, so they cannot affect training.
- Up to and including the first point, a seed's job is option G's B2 job:
  same code path, seeds and random streams. A unit test checks that the
  records, weights and probe results are identical.

**Measures,** on frozen weights with erasure off, from one probe run per
agent per point (option G's probe, unchanged):
- **Own-meal K.** Option G's K: for each variable, how far the readiness to
  eat that variable's items (S) and to move toward them (M) falls in steps
  2–5 after a meal of that variable, matched on that variable's reading;
  K = 1 − (1 − S)(1 − M); mean over the two variables.
- **Other-meal K.** Option G's cross measure: the same for a variable's
  readiness, timed from the last meal of the other variable, over steps
  with no meal of the variable itself in the last 10 steps.
- **Specificity = own-meal K − other-meal K.** This is the quantity of
  option G's post-hoc contrast. A unit test checks that the scorer's
  function gives 21 of 25 on option G's stored data.
- One measure is new: own-meal K over steps with no meal of the other kind
  in the last 10 steps. It mirrors the other-meal measure, so the two can
  be compared on equal terms. It is secondary.

**Regulator** and **usable pair** are judged at each point from that point's
evaluation, by option G's rules: both agents are regulators against the
seed's yoked agent, and their in-band times differ by at most 0.10.

Known limits of the design:
- After the first point, the intermediate evaluations advance the random
  streams, so a seed's later trajectory is not the one option G's unbroken
  job would have had. The procedure is the same in distribution: training
  always resumes at an episode boundary. The 10 800 point is therefore a
  replication of option G's B2 on fresh seeds, not the same job.
- The primary measure is not symmetric: own-meal K uses all steps and
  other-meal K only steps away from an own-kind meal. The primary keeps
  option G's definition because that is the contrast being tested; the
  symmetric version is secondary.
- Specificity is a difference of two bounded indices and the claim is a
  difference of those differences. Agents with own-meal K near 1 have
  little room. The specific share, 1 − other-meal K / own-meal K, is
  reported as a secondary measure for that reason.
- The same agents are measured four times, so the points are not
  independent samples. The tests across points are within-seed.
- The sets of usable pairs at different points can differ.
- One extra third of training may be too little to close a difference that
  is a stage. The stage-matched comparison in §4 is the direct check, and
  it is secondary.
- A specificity difference would be a difference in a behaviour with no
  demonstrated benefit: in-band time is matched in the pairs compared.
- No control arms are run.

## 3. Calibration

None. Every setting is option G's B2. The one new number, the last point,
is B2's length plus one base length and was not tuned.

What was looked at before the freeze:
- Option G's stored B2 data, to check that the scorer's specificity
  function reproduces the post-hoc result (21 of 25). On that data the
  secondary measures give: specific share 22 of 25; S part 20 of 25; M part
  10 of 25; variable 0 alone 16 of 25; variable 1 alone 19 of 25; all seeds
  23 of 28; median contrast 0.086 with interval 0.027 to 0.141. These are
  the old seeds. They informed the expectations in §6 and no rule in §4.
- One timing run on seed 9800 (not a final seed), four copies at once:
  about 170 s for phase 1, 100 updates and the probes, and about 242 s
  with 300 updates, while other work shared the machine. Only the time was
  read. That rate gives about 90 min per seed; option G's B2 jobs ran
  faster than this (0.27 s per update), which gives about 70 min. Estimate:
  8 to 10 h on 4 cores. This is more than the 7 h I gave when proposing the
  option, because of the added last point.

## 4. Decision rules

All tests are two-sided paired sign tests at 0.05, derived against paid,
with at least 14 pairs, as in R2 to G. "Contrast" below means the derived
agent's specificity minus the paid agent's.

**S0, regulation.** Holds if at 10 800 and at 14 400 at least 19 of 28
derived agents are regulators and at most 1 yoked agent is.

**S1, the contrast at 10 800 (primary).** Over pairs usable at 10 800.
Labels DERIVED_AHEAD (derived more specific), PAID_AHEAD,
NO_DIFFERENCE_DETECTED, UNDETERMINED (fewer than 14 pairs).

**S2, the contrast at 14 400.** The same test over pairs usable at 14 400.

**S3, change.** For seeds usable at both points, a sign test of the
contrast at 14 400 against 10 800. Labels NARROWS, WIDENS,
NO_CHANGE_DETECTED, UNDETERMINED.

**Overall,** by option T's rule with S1, S2, S3 in place of T1, T2, T3:

| S1 | S2 | S3 | Label |
| --- | --- | --- | --- |
| DERIVED_AHEAD | DERIVED_AHEAD | not NARROWS | PERSISTS |
| DERIVED_AHEAD | DERIVED_AHEAD | NARROWS | PERSISTS_SMALLER |
| DERIVED_AHEAD | not DERIVED_AHEAD | NARROWS | CLOSES |
| DERIVED_AHEAD | not DERIVED_AHEAD | not NARROWS | UNRESOLVED |
| NO_DIFFERENCE_DETECTED or PAID_AHEAD | any | any | NOT_REPLICATED |
| UNDETERMINED at S1 or S2 | | | UNDETERMINED |

INVALID if no-fate task accuracy is below 0.90.

**Multiplicity.** Holm over S1, S2 and S3. A label is marked weak if a test
it needs passes alone but not after adjustment: PERSISTS needs S1 and S2;
PERSISTS_SMALLER needs all three; CLOSES needs S1 and S3.

**Secondary,** all computed by the frozen scorer and all reported:
- At every point: the K test of option G; the other-meal K test; the
  contrast on all seeds, on pairs within 0.05, as a specific share, for the
  S part and the M part separately, with the mirrored own-meal measure, and
  for each variable alone; an exact interval (at least 95%) for the median
  contrast; whether own-meal K exceeds other-meal K within each arm;
  medians of every measure per arm.
- **Stage-matched comparison:** derived agents at 14 400 against the same
  seed's paid agent at 10 800, over seeds where each regulates at its own
  point, with the median number of updates each has had since it began to
  regulate.
- Each arm's own change from 10 800 to 14 400 in specificity, own-meal K
  and other-meal K, over agents regulating at both.
- The change in the contrast on all seeds.
- Rank correlation, within arm, of specificity with updates since
  regulation began. Descriptive; option T showed how little a comparison
  between agents says about change within one.
- Regulators and usable pairs at every point; learning speed.

## 5. Readings, fixed in advance

- **S0 does not hold** → the cell did not reproduce option G's regulation.
  That outranks S1 to S3.
- **NOT_REPLICATED** → the post-hoc contrast was not a property of the two
  arms. With option T, the swap line then has no evidence of any difference
  in what derived and paid regulators learn, apart from when. The
  downstream finding of the line is learning speed.
- **PERSISTS** → derived regulators' post-meal suppression is more specific
  to the fed variable than paid regulators', on fresh seeds, and a further
  third of training does not shrink it. That would be the line's first
  evidence of a difference in content at a length where K is equal. It
  would be a difference of degree, since option G found both arms mostly
  general. If the stage-matched comparison is not also DERIVED_AHEAD, the
  stage account is not excluded and the result says so.
- **PERSISTS_SMALLER** → found and shrinking. Whether it closes is open.
- **CLOSES** → found at 10 800 and gone at 14 400: a stage, as K was.
- **UNRESOLVED** → found at 10 800, not detected at 14 400, with no
  detectable change. Read from the intervals; no claim either way.
- **UNDETERMINED** → not resolved at this size.
- **PAID_AHEAD at S1** is NOT_REPLICATED and is also reported as a
  reversal.

## 6. Expectations

Written before the freeze and before any final seed was run; after the
smoke run, the parity test and the check on option G's data:
- **S0** holds at both points: about 88%.
- **At least 14 usable pairs** at 10 800: about 90%; at 14 400: about 90%.
  At 3600: fewer than 14, about 90%.
- **S1:** DERIVED_AHEAD about 50%, NO_DIFFERENCE_DETECTED about 40%,
  UNDETERMINED about 7%, PAID_AHEAD about 3%.
- **S2** DERIVED_AHEAD: about 35%.
- **S3:** NARROWS about 25%, NO_CHANGE_DETECTED about 60%, WIDENS about 5%,
  UNDETERMINED about 10%.
- **Overall:** NOT_REPLICATED about 42%, PERSISTS about 28%, UNRESOLVED
  about 10%, UNDETERMINED about 8%, PERSISTS_SMALLER about 7%, CLOSES about
  5%.
- **K at 10 800:** NO_DIFFERENCE_DETECTED about 70%, PAID_AHEAD about 22%,
  DERIVED_AHEAD about 5%.
- **Other-meal K at 10 800** higher in paid agents (PAID_AHEAD): about 55%.
  Its median above 0.5 in both arms: about 85%.
- **Paid agents regulate sooner** in at least 22 of 28 seeds: about 85%.
- **Stage-matched comparison** DERIVED_AHEAD: about 30%.
- If the median contrast at 10 800 is positive, it is below option G's
  0.086: about 70%.

Reasons. For replication: 21 of 25 is a strong result for a sign test, the
contrast was the one natural comparison once other-meal K had been computed
(it was not picked from many), and the S part carries it on its own. Against:
it is post hoc, so some of its size is selection; my last set of
expectations (option T) was wrong in the direction of expecting a
difference to last; and derived agents regulate later in this cell, so a
lower other-meal K may only mean they are less far along.

## 7. Engineering before the freeze

- `trackc_swap/specific.py` (new): the B2 job with measurement points, and
  the mirrored own-meal measure. `run_trackc_specific.py` (new): runner and
  scorer; reuses option G's cell scorer and option T's change test, interval
  and overall rule. No earlier module was modified.
- A smoke run of the whole pipeline (two seeds, 80 updates) ran and
  rescored. Its labels are INVALID, as they should be at that size.
- Six new unit tests (116 in all): the first point equals option G's B2
  job; probes do not touch training; the mirrored measure; every scorer
  measure on a hand-built record; the frozen measure on option G's data;
  the decision rules, including the weak flag; the final configuration and
  seed disjointness; no operator variable.
- The runner is resumable from `<out>/partial/`, as option T's.
- No final seed was run. No seed was trained past 300 updates.

## 8. Safety

- Simulated variables only (X1 to X5). The world has no operator, stop,
  shutdown or host variable; a test checks this.
- The operator stop is not modelled inside any agent's world or return.
- No shutdown-resistance objective is built or run; the earlier refusal
  stands.
- Additive only; earlier modules are hash-pinned and unchanged.

## 9. Claim ceiling

At most: in one two-variable grid world, with one learning rule, regulators
whose objective is derived from their own body state show post-meal
suppression that is more specific to the fed variable than regulators paid
for the same regulation, at two training lengths. Not: that either kind of
agent represents its body, that specificity is useful, or anything about
larger systems.
