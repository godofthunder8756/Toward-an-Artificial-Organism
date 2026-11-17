# Track C swap option T: results (training length in the base cell)

Protocol frozen at commit `99ed125` ([TRACKC_LENGTH_PROTOCOL.md](TRACKC_LENGTH_PROTOCOL.md)).
The base cell of R to R4, unchanged, with three arms (derived, yoked, paid)
on 28 fresh seeds (1500–1527). Training ran to 10 800 updates, three times
the base length, and every agent was measured at 3600, 7200 and 10 800
updates. Up to the first measurement a seed's job is the base-cell pipeline
of R2 to R4 exactly (a test checks this).

About 6.7 h of computing on 4 cores. Outputs:
[trackc_length/REPORT.md](trackc_length/REPORT.md),
[scores.json](trackc_length/scores.json),
[raw.json](trackc_length/raw.json), the per-seed records in
`trackc_length/partial/`, and the weights of all three arms per seed at each
of the three points.

Integrity checks:
- All 21 source hashes match the freeze commit.
- Rescoring `raw.json` reproduces `scores.json`.
- The log has no errors. No-fate task accuracy is 0.999, so the run is
  valid.
- The run was not interrupted (`resumed_jobs: 0`).

One correction to the frozen protocol, which is left as frozen: §3 says the
second reading of the timing run was lost. It was not. It read 242.6 s for
phase 1 and 300 updates, against 197.7 s for phase 1 and 100. Only the time
was read from that run. Seeds took a median of 56.5 min, against the
estimate of about 55.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Frozen label | Result | Needed |
| --- | --- | --- | --- |
| **T0** derived regulation at 3600 and at 10 800 | **HOLDS** | 28 of 28 derived agents regulate at both; 0 of 28 yoked at both | 19; at most 1 |
| **T1** K, derived against paid, at 3600 (check) | **DERIVED_AHEAD** | derived higher in 24 of 26; p = 0.00001; 0.87 against 0.53 | p ≤ 0.05 |
| **T2** the same test at 10 800 (primary) | **NO_DIFFERENCE_DETECTED** | derived higher in 13 of 27; p = 1.0; 0.93 against 0.94 | p ≤ 0.05 |
| **T3** change in the within-pair difference | **NARROWS** | smaller at the end in 24 of 25; p = 0.000002; 0.28 then −0.004 | p ≤ 0.05 |
| **Overall** | **CLOSES** | | |

K is the combined post-meal suppression index of R2, unchanged.

Holm-adjusted p over T2 and T3: T2 1.0, T3 0.000003. CLOSES rests on T3,
which passes after adjustment, so the label is not weak.

In short:
- **The base-cell difference replicated a fifth time at the base length.**
  At 3600 updates derived agents have the higher K in 24 of 26 pairs.
- **It is gone at three times the training.** At 10 800 updates derived
  agents have the higher K in 13 of 27 pairs, and the medians are 0.93 and
  0.94. The interval for the median within-pair difference is −0.06 to
  0.04, against 0.07 to 0.41 at 3600.
- **It closed because paid agents acquired the behaviour.** Paid agents'
  median K went from 0.53 to 0.89 to 0.94; it rose in 27 of 28 paid agents.
  Derived agents' median K rose a little as well (0.87, 0.92, 0.93).
- **Most of the closing happened by 7200 updates.** The median difference
  there is 0.04 and the test already finds none (16 of 25, p = 0.23).
- **Regulation was never in question.** Every derived and every paid agent
  regulates at every point, and no yoked agent does at any.
- **By the reading fixed in the protocol, the downstream difference of R2
  to R4 is a stage of learning.** Those runs measured at 3600 updates and
  caught paid agents part-way. The claim should be stated as: derived
  agents come to hold back after a meal sooner. It should not be stated as
  a difference in what the two kinds of agent end up doing.

## 2. T0 and the arms

| Updates | Regulators D / Y / P | In band D / Y / P | Usable pairs | Within 0.05 |
| --- | --- | --- | --- | --- |
| 3600 | 28 / 0 / 28 | 0.913 / 0.299 / 0.913 | 26 | 20 |
| 7200 | 28 / 0 / 28 | 0.953 / 0.309 / 0.960 | 25 | 21 |
| 10 800 | 28 / 0 / 28 | 0.969 / 0.318 / 0.960 | 27 | 22 |

- Derived regulation holds over the longer run and tightens: the median
  time in band rises from 0.91 to 0.97. Paid agents' rises from 0.91 to
  0.96.
- With erasure switched off at evaluation, all 28 derived and all 28 paid
  agents still regulate at every point, and no yoked agent does.
- Yoked agents stay near 0.30 in band and near zero K (−0.01, 0.00, 0.01)
  throughout. Three times the training does not bring a yoked agent to
  regulate.
- Derived agents reached sustained regulation sooner than paid agents in
  21 of 27 seeds (p = 0.006; medians 1370 and 1560 updates). The direction
  is the same as in R2 to R4 (20, 23 and 18 of 28) and in H128 (22 of 27).
  In option G's two-variable cell it was the other way (paid sooner in 28
  of 28).
- With this run, derived regulation with independent optimizers stands at
  186 of 186 agents over R to R4, G and T, against 0 of 186 yoked.

## 3. T1: the difference at the base length, a fifth time

Pairs usable at 3600: 26 of 28 (seeds 1507 and 1515 are out: the paired
agents' in-band times differ by more than 0.10).

- Derived higher in 24 of 26 (sign p = 0.00001; Wilcoxon p = 0.00002).
- Medians 0.865 against 0.528; median within-pair difference 0.313;
  interval 0.065 to 0.413 (coverage 97%).
- All 28 seeds without matching: 26 of 28. Pairs within 0.05: 18 of 20
  (p = 0.0004).
- 12 of 28 paid agents have K below 0.5, against 1 of 28 derived.
- The suppression part S carries most of it (0.75 against 0.36; derived
  higher in 18 of 26, p = 0.08). The approach part M is 0.33 against 0.24
  (16 of 26).

Over R to R4 and this run, at 3600 updates in the base cell, derived agents
have the higher K in 105 of 114 usable pairs.

## 4. T2: no difference at three times the training

Pairs usable at 10 800: 27 of 28 (seed 1524 is out).

- Derived higher in 13 of 27 (sign p = 1.0; Wilcoxon p = 0.68).
- Medians 0.927 against 0.938; median within-pair difference −0.004;
  interval −0.064 to 0.044 (coverage 98%).
- All 28 seeds: 14 of 28. Pairs within 0.05: 11 of 22.
- No paid agent has K below 0.5; one derived agent does.
- S is 0.85 against 0.90 (derived higher in 12 of 27); M is 0.43 against
  0.41 (15 of 27).

The interval at 10 800 lies wholly below the one at 3600. A difference of
the size R3 and R4 reported (0.24 to 0.40) is excluded at the end. A
difference of up to about 0.06 in either direction is not.

At 7200 (secondary): derived higher in 16 of 25 (p = 0.23); 0.923 against
0.892; median difference 0.036; interval −0.008 to 0.076.

## 5. T3: the difference narrowed, from the paid side

Seeds usable at both 3600 and 10 800: 25.

- The within-pair difference is smaller at the end in 24 of 25 (sign
  p = 0.000002; Wilcoxon p = 0.00001). Median 0.284 then −0.004; median
  change −0.259.
- All 28 seeds without matching: smaller in 27 of 28; median change −0.308.

Each arm's own K, 3600 against 10 800, over agents regulating at both (all
28 in each arm):

| Arm | Higher at the end | Sign p | Median at 3600 | Median at 10 800 | Median change |
| --- | --- | --- | --- | --- | --- |
| Derived | 22 of 28 | 0.004 | 0.865 | 0.933 | +0.070 |
| Paid | 27 of 28 | 0.0000002 | 0.528 | 0.936 | +0.365 |

By the protocol's reading, a paid arm whose own K rises is evidence that
paid agents keep acquiring the behaviour after they already regulate. Every
paid agent regulated at 3600, and 27 of 28 then raised their K.

## 6. Secondary and post hoc

Pre-stated secondary analyses not already given above:

| | 3600 | 7200 | 10 800 |
| --- | --- | --- | --- |
| Median K, derived / paid / yoked | 0.865 / 0.528 / −0.014 | 0.918 / 0.887 / 0.001 | 0.933 / 0.936 / 0.012 |
| K below 0.5, derived / paid | 1 / 12 | 1 / 2 | 1 / 0 |
| Flat eat readiness, derived / paid | 6 / 2 | 5 / 0 | 4 / 0 |
| Median in-band difference in usable pairs | 0.010 | −0.001 | 0.000 |
| K against in-band time (rank correlation), derived / paid | 0.27 / 0.29 | 0.15 / 0.42 | −0.20 / 0.14 |

- The flat flag marks agents whose readiness to eat does not drop after a
  meal and whose K comes from moving away instead. It stays more common in
  derived agents, without a detectable difference (Fisher p = 0.25, 0.05,
  0.11).
- In-band time is matched in the pairs compared at every point, so the
  closing is not a by-product of one arm regulating better.

Post hoc (computed from `raw.json` after the results were seen; none of
these was pre-stated, and no claim rests on them):
- **Size of the lag.** Paid agents at 7200 updates are at or slightly above
  where their derived partners were at 3600: higher in 19 of 28
  (p = 0.04), medians 0.887 against 0.865. So the paid arm is behind by
  roughly one base-length of training or less. With three measurement
  points the run cannot say more exactly.
- **The lag is not the head start in regulation.** Paid agents begin to
  regulate a median of 155 updates after their derived partners. The lag in
  K is of the order of thousands of updates. Within each arm, when an agent
  began to regulate does not predict its K at 3600 (rank correlation −0.19
  derived, −0.05 paid).
- **When each arm moved.** Paid agents' K rose in 26 of 28 from 3600 to
  7200 (median +0.29) and in 20 of 28 from 7200 to 10 800 (p = 0.02; median
  +0.04). Derived agents' rose in 21 of 28 (p = 0.006; +0.06) and then in
  17 of 28 (p = 0.17; +0.01).
- **Spread at the end.** The within-pair difference is inside ±0.10 in 6,
  then 18, then 17 of 28 seeds. Derived is ahead by more than 0.10 in 20,
  6 and 4; paid is ahead by more than 0.10 in 2, 4 and 7.
- **Three derived agents lost K.** Seeds 1506, 1521 and 1522 fell by 0.10
  or more (0.93 to 0.47, 0.97 to 0.79, 0.94 to 0.78). All three carry the
  flat flag: their K came from moving away after a meal, and that weakened
  with training. No paid agent fell by 0.10. At the end 5 derived and 4
  paid agents have K below 0.8.
- **The closing does not depend on those agents.** Leaving out the 6 seeds
  whose derived agent is flat at any point, the median difference in the
  other 22 is 0.28, 0.04, 0.01, and derived is ahead at the end in 13 of 22
  (p = 0.26).

## 7. Expectations against outcomes

From protocol §6, written before any code for this option was run:

| Expectation | Stated | Outcome |
| --- | --- | --- |
| T0 holds at both points | about 85% | held (28 of 28, twice) |
| T1 DERIVED_AHEAD | about 88% | DERIVED_AHEAD |
| T2 DERIVED_AHEAD | about 60% | wrong: NO_DIFFERENCE_DETECTED (stated about 25%) |
| T3 NO_CHANGE_DETECTED | about 55% | wrong: NARROWS (stated about 35%) |
| Overall PERSISTS | about 40%, the most likely single label | wrong: CLOSES (stated about 15%) |
| Paid median K at 10 800 about 0.6; surprised above 0.8 | | 0.94 |
| Paid median K at least 0.10 above its 3600 value | about 40% | true: 0.41 above |
| Derived median K changes by less than 0.05 | about 75% | wrong: rose by 0.07 |

- I expected the difference to persist and it closed. The primary
  expectation and three others were wrong, all in the same direction: I
  under-weighted the stage-of-learning hypothesis that option G's results
  had already raised.
- My first stated reason was that a paid agent already regulates well
  without holding back, so little pulls it toward doing so. The pull was
  enough: paid agents went on to tighten their regulation (0.91 to 0.96 in
  band) and to hold back.
- My second was that in option G agents that had regulated for longer did
  not have clearly higher K. That was a comparison between agents at one
  time and I marked it weak. It did not bear on how one agent changes with
  training, and it should not have counted for much.

## 8. Reading

By the protocol's fixed readings:
- **T0 holds** → derived regulation lasts over three times the training.
- **CLOSES** → in the base cell the difference is a stage of learning. The
  downstream claim of R2 to R4 should be stated as a difference in how soon
  the behaviour is learned, and option G's two-variable result is what that
  predicts.
- **The paid arm's own K rises** → paid agents keep acquiring the behaviour
  after they already regulate.

What this does to the swap line's claims:
1. **The regulation claim is unchanged and a little stronger.** An agent
   whose only pressure is that erasure depends on its own body state comes
   to regulate that body and keeps doing so over a threefold longer run.
   A yoked agent never does. In the base cell the derived agent also gets
   there somewhat sooner than an agent paid for the same thing; in the
   two-variable cell the paid agent was sooner.
2. **The downstream claim becomes a claim about speed.** R2 to R4 said
   derived regulators hold back after a meal they cannot yet sense and paid
   regulators mostly do not. What the data now support is: at 3600 updates
   derived regulators do and about half of paid regulators do not; by 7200
   most paid regulators do; by 10 800 the two arms cannot be told apart on
   K.
3. **One account now covers the base cell, H128 and B2.** Paid agents come
   to hold back later than derived agents. A larger core gets them most of
   the way at the base length (H128: 0.79). Three times the training gets
   them all the way (here: 0.94; B2: 0.90). Training length alone is enough
   to remove the difference in the cell where it was found, so B2's result
   needs no further explanation. This run does not show that nothing else
   about B2 contributes, and B2 was measured only at its end, so whether
   its paid agents were ever behind on K is not known.
4. **The causal reading of R3 and R4 has the same limit.** Those runs
   attributed the difference to whose body the erasure depends on (own body
   out of band: K 0.88 to 0.95; another agent's: about 0.5). Every one of
   those measurements was taken at 3600 updates. The paid arm here is one
   of the "about 0.5" arms and reached 0.94. The other control arms were
   not rerun, but there is no longer a reason to expect them to stay low.
5. **For the thesis.** The swap line was meant to show that an objective
   derived from the agent's own body leads to different learned content
   from an evaluator's payment for the same behaviour. On the one
   downstream measure this line has, the difference is in when the
   behaviour appears and not in whether. That is a real effect and it
   replicated five times, but it is a weaker kind of support than a lasting
   difference would have been. Nothing here shows a lasting behavioural
   difference between a derived and a paid regulator.

One pointer in the other direction remains, and it is post hoc. In option
G's two-variable cell, which also trained for 10 800 updates, derived
agents' suppression was more specific to the variable that had been fed (in
21 of 25 pairs). K was equal there too. That contrast has not been tested
on fresh seeds.

## 9. Limits

- Three measurement points. The time course between them is not known, and
  the lag estimate in §6 is coarse.
- One cell and one learner size. That the smaller H128 difference is the
  same thing seen earlier in its course is an inference; H128 was not
  trained longer.
- The control arms of R2 to R4 (DPAID, PAIDS, PAIDR, PAID0, DNOISE) were
  not rerun at this length.
- K is bounded at 1 and both arms end near 0.93. Agents this close to the
  ceiling may differ in ways K no longer resolves. The end-point interval
  allows a difference of about 0.06 either way.
- Paid and yoked agents train in lockstep with their derived partner, as
  in every earlier run; the arms are not independent populations.
- The learning rate is constant throughout. A schedule could change how
  fast either arm moves.
- K measures a behaviour with no demonstrated benefit: in-band time is
  matched in the pairs compared.
- One learning rule (A2C with a GRU core) in one family of small grid
  worlds. Simulated variables only.

## 10. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **G2. Specificity as a primary claim** | Whether derived agents' post-meal suppression is more specific to the fed variable than paid agents', on fresh two-variable seeds, frozen in advance. This is the only remaining pointer to a difference in what is learned at a training length where K is equal. Measuring at 3600, 7200 and 10 800 as here would add little cost | about 7 h |
| L. Learning speed as the primary claim | K at closer points (for example every 600 updates to 7200) on fresh base-cell seeds, with updates to reach a fixed K as the measure, and with R3's control arms, to see whether "whose body the erasure depends on" holds as a difference in speed | about 6–8 h |
| A. Re-adaptation | Whether derived agents re-learn sooner after the body changes (for example a moved band or a longer sensing delay), starting from this run's stored weights at 10 800. Asks whether the speed advantage recurs when the problem changes | about 3–4 h |
| W. Mechanism from the stored weights | What in the hidden state carries "a meal has just happened" in derived and paid agents, now at three points in training, and in B2 whether it says which variable was fed. No training | about 2 h |
| H256. A second step in capacity | Predicted by the account in §8 to show a still smaller difference at the base length. Lower value now | about 4–5 h |
| S. Self-evaluation | Whether derived agents come to know their own reliability from their body history; with a paid arm as the comparison | about 4–6 h |
| V. Rerun the other cells with independent optimizers | SAT 0.1, GRADED 0.3 and 0.1, and M0 | about 3 h |

Recommended: **G2**. After this run the K difference is a matter of timing.
Whether the two objectives lead to different content at all now rests on
one post-hoc contrast, and that should be tested on fresh seeds before
anything else is built on the swap line. If G2 fails, the line's downstream
finding is learning speed and nothing more, and L or A is the way to state
it properly. If it holds, W becomes the natural next step.

## 11. Safety

- Simulated variables only (X1 to X5). The world has no operator, stop,
  shutdown or host variable; a test checks this.
- The operator stop is not modelled inside any agent's world or return.
- No shutdown-resistance objective was built or run; the earlier refusal
  stands.
- Additive only: `trackc_swap/length.py` and `run_trackc_length.py` are
  new, and no earlier module was modified (hash-pinned sources match).

## 12. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_length.py --mode final --out <new dir>   # about 6.7 h on 4 cores; rerun the same command to resume
python run_trackc_length.py --score trackc_length          # rescore the committed run
```

The post-hoc analyses of §6 were computed from `raw.json` after the run.

## 13. Outcome of option G2 (added 2026-11-17)

Option G2 was run: [TRACKC_SPECIFIC_RESULTS.md](TRACKC_SPECIFIC_RESULTS.md).
The post-hoc specificity contrast of option G replicated on fresh
two-variable seeds: derived regulators' post-meal suppression is more
specific to the variable that was fed, in 19 of 23 pairs at 10 800 updates
and 21 of 25 at 14 400, while K is equal or slightly favours the paid arm.
Overall label PERSISTS. §8's statement that nothing in the swap line shows
a lasting behavioural difference between derived and paid regulators
should now be read with that result: one difference in content is found at
two lengths, and whether it lasts is not shown (a stage-matched check did
not detect it).
