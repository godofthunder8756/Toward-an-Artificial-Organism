# Track C swap option G2: results (specificity of post-meal suppression)

Protocol frozen at commit `10281c8` ([TRACKC_SPECIFIC_PROTOCOL.md](TRACKC_SPECIFIC_PROTOCOL.md)).
Option G's two-variable cell (B2), unchanged, with three arms (derived,
yoked, paid) on 28 fresh seeds (1600–1627). Every agent was measured at
3600, 7200, 10 800 (primary) and 14 400 phase-2 updates. Up to the first
measurement a seed's job is option G's B2 job exactly (a test checks this).

About 9.7 h of wall time on 4 cores, including two restarts (median 81 min
per seed). Outputs:
[trackc_specific/REPORT.md](trackc_specific/REPORT.md),
[scores.json](trackc_specific/scores.json),
[raw.json](trackc_specific/raw.json), the per-seed records in
`trackc_specific/partial/`, and the weights of all three arms per seed at
each of the four points.

Integrity checks:
- All 23 source hashes match the freeze commit.
- Rescoring `raw.json` reproduces `scores.json`.
- The log has no errors. No-fate task accuracy is 0.998, so the run is
  valid.
- **The run was interrupted twice and resumed both times.** The container
  restarted at about 02:38 UTC (12 of 28 seeds finished) and at about 05:08
  UTC (20 finished). Each time the four seeds then in training were lost
  and rerun from the start with the same seed and code; finished records
  were kept. `raw.json` records `resumed_jobs: 20`, the count at the second
  resume only.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Frozen label | Result | Needed |
| --- | --- | --- | --- |
| **S0** derived regulation at 10 800 and 14 400 | **HOLDS** | 27 then 28 of 28 derived agents regulate; 0 of 28 yoked at both | 19; at most 1 |
| **S1** specificity, derived against paid, at 10 800 (primary) | **DERIVED_AHEAD** | derived more specific in 19 of 23; p = 0.003; 0.18 against 0.07 | p ≤ 0.05 |
| **S2** the same test at 14 400 | **DERIVED_AHEAD** | 21 of 25; p = 0.0009; 0.17 against 0.04 | p ≤ 0.05 |
| **S3** change in the contrast | **NO_CHANGE_DETECTED** | smaller at the end in 12 of 21; p = 0.66 | p ≤ 0.05 |
| **Overall** | **PERSISTS** | | |

Specificity is own-meal K minus other-meal K: how much more an agent holds
back after a meal of a variable than after a meal of the other variable,
for the same variable's readiness. Each K is option G's measure, unchanged.

Holm-adjusted p over S1, S2 and S3: 0.005, 0.003, 0.66. PERSISTS needs S1
and S2, and both pass after adjustment, so the label is not weak.

In short:
- **Option G's post-hoc contrast replicated on fresh seeds.** At the
  length where it was found, derived regulators' post-meal suppression is
  more specific to the variable that was fed than paid regulators', in 19
  of 23 pairs. The median within-pair difference is 0.10 (interval 0.06 to
  0.14), against 0.086 in option G.
- **It is still there after a third more training,** in 21 of 25 pairs,
  with no detectable change.
- **K itself does not favour the derived arm.** At 10 800 there is no
  difference (derived higher in 10 of 23); at 14 400 the paid arm is
  slightly ahead (7 of 25, p = 0.04; 0.89 against 0.94). The paid agents
  hold back at least as much after a meal. They hold back almost as much
  after a meal of the other kind as well.
- **The difference sits in the other-meal suppression.** Paid agents'
  other-meal K is higher (0.77 against 0.68 at 10 800; 0.89 against 0.74 at
  14 400). Derived agents' specific share of their post-meal suppression is
  about a fifth (0.20, 0.18); paid agents' is under a tenth (0.08, 0.05).
- **The pre-stated stage-matched check did not detect a difference.**
  Derived agents at 14 400 against the same seed's paid agent at 10 800
  (derived has then been regulating longer, 8185 updates against 6215):
  derived more specific in 18 of 28, p = 0.18, median difference 0.066. By
  the reading fixed in the protocol, **the stage account is not excluded**.
  §5 gives the post-hoc evidence on it, which points against it but is not
  a test.
- **This is the swap line's first evidence of a difference in what derived
  and paid regulators learn, at lengths where K is equal or favours the
  paid arm.** It is a difference of degree: both arms' suppression is
  mostly general, and both become more general with training.

## 2. S0 and the arms

| Updates | Regulators D / Y / P | Usable pairs | Within 0.05 | In band D / Y / P |
| --- | --- | --- | --- | --- |
| 3600 | 0 / 0 / 0 | 0 | 0 | 0.343 / 0.198 / 0.394 |
| 7200 | 22 / 0 / 28 | 15 | 10 | 0.737 / 0.180 / 0.792 |
| 10 800 | 27 / 0 / 28 | 23 | 17 | 0.866 / 0.183 / 0.864 |
| 14 400 | 28 / 0 / 28 | 25 | 19 | 0.896 / 0.178 / 0.878 |

- In-band time is the share of steps with both variables in band.
- No agent regulates at 3600, as option G's calibration found for this
  cell. 7200 is descriptive.
- Derived regulation holds: 27 of 28 at 10 800 (seed 1619 not yet) and 28
  of 28 at 14 400. No yoked agent regulates at any point.
- Paid agents reached sustained regulation sooner in 28 of 28 seeds
  (medians 4585 and 6215 updates), as in option G's B2 (28 of 28).
- With erasure switched off at evaluation, 27 and 28 derived agents and 28
  paid agents still regulate at 10 800 and 14 400.
- Derived regulation with independent optimizers now stands at 213 of 214
  agents over R to R4, G, T and G2 (counting G2 at its primary point),
  against 0 of 214 yoked.

## 3. S1 and S2: the contrast at 10 800 and 14 400

| Updates | Usable | Derived more specific | Sign p | Wilcoxon p | Specificity D / P | Median difference | Interval | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7200 (descriptive) | 15 | 13 | 0.007 | 0.010 | 0.220 / 0.091 | 0.113 | 0.043 to 0.147 | DERIVED_AHEAD |
| **10 800** | 23 | 19 | 0.003 | 0.001 | 0.184 / 0.071 | 0.100 | 0.055 to 0.141 | **DERIVED_AHEAD** |
| **14 400** | 25 | 21 | 0.0009 | 0.003 | 0.168 / 0.043 | 0.081 | 0.050 to 0.161 | **DERIVED_AHEAD** |

Medians are over the usable pairs. Intervals are exact order-statistic
intervals for the median within-pair difference (coverage 96%).

The secondary versions of the contrast, all pre-stated:

| | 10 800 | 14 400 |
| --- | --- | --- |
| All 28 seeds, no matching | 22 of 28 (p 0.004) | 23 of 28 (p 0.001) |
| Pairs within 0.05 in band | 15 of 17 (p 0.002) | 16 of 19 (p 0.004) |
| Specific share, 1 − other-meal K / own-meal K | 19 of 23 (p 0.003); 0.21 against 0.07 | 21 of 25 (p 0.001); 0.19 against 0.05 |
| S part (readiness to eat) | 20 of 23 (p 0.0005) | 21 of 25 (p 0.001) |
| M part (approach) | 15 of 23 (p 0.21) | 14 of 25 (p 0.69) |
| Both sides measured away from the other kind of meal | 19 of 23 (p 0.003) | 22 of 25 (p 0.0002) |
| Variable 0 alone | 20 of 23 (p 0.0005) | 20 of 25 (p 0.004) |
| Variable 1 alone | 16 of 23 (p 0.09) | 24 of 25 (p 0.000002) |

- **Every version agrees in direction.** All but the M part and, at 10 800,
  variable 1 alone pass.
- **The S part carries it, as in option G** (where S was 20 of 25 and M 10
  of 25). The difference is in the readiness to eat an item that is
  already underfoot, not in moving toward items.
- **The asymmetry of the primary measure does not drive it.** Measuring
  own-meal K, like other-meal K, only on steps away from the other kind of
  meal gives the same result.
- **The two agents with the largest paid specificity count against the
  claim.** In seeds 1606 and 1613 the paid agent's readiness rises after a
  meal of the other kind (other-meal K −0.5 to −0.7), so its specificity
  exceeds 1. These agents are in the tests as they are.

Other-meal K, derived against paid: derived higher in 6 of 23 at 10 800
(p = 0.035; 0.68 against 0.82, PAID_AHEAD) and in 3 of 25 at 14 400
(p = 0.0002; 0.72 against 0.90). Within each arm, own-meal K exceeds
other-meal K in almost every agent (derived 27 of 27 and 28 of 28; paid 27
of 28 and 26 of 28): both arms carry some specific content, and the derived
arm carries more.

## 4. S3 and each arm over training

Seeds usable at both 10 800 and 14 400: 21. The contrast is smaller at the
end in 12 of 21 (p = 0.66; median 0.102 then 0.081; median change −0.030).
On all 28 seeds: 17 of 28 (p = 0.34).

Each arm's own measures from 10 800 to 14 400, over agents regulating at
both:

| Arm | Measure | Higher at the end | Sign p | At 10 800 | At 14 400 | Median change |
| --- | --- | --- | --- | --- | --- | --- |
| Derived | specificity | 7 of 27 | 0.019 | 0.178 | 0.156 | −0.060 |
| Derived | own-meal K | 18 of 27 | 0.12 | 0.856 | 0.906 | +0.046 |
| Derived | other-meal K | 20 of 27 | 0.019 | 0.681 | 0.750 | +0.092 |
| Paid | specificity | 9 of 28 | 0.087 | 0.074 | 0.046 | −0.020 |
| Paid | own-meal K | 26 of 28 | 0.000003 | 0.873 | 0.935 | +0.067 |
| Paid | other-meal K | 26 of 28 | 0.000003 | 0.770 | 0.888 | +0.092 |

- **Both arms grow more general with training.** Other-meal K rises in both
  by about 0.09, own-meal K by less. Derived agents' specificity falls
  detectably; paid agents' falls by less, from a lower level, and not
  detectably.
- **The contrast is therefore not stable in absolute terms,** even though
  S3 detects no change. Whether it would close with more training is the
  question §5 bears on and does not settle.
- **K turns slightly toward the paid arm at 14 400** (PAID_AHEAD, 7 of 25,
  p = 0.04, all from the S part: 5 of 25, p = 0.004). This was not one of
  the pre-stated expectations. It fits the rest: paid agents hold back more
  after any meal, derived agents more after the relevant one.

## 5. The stage account

Option T showed a difference that was a stage of learning. In this cell
the derived arm is the one that comes to regulate later, so a stage
account would say derived agents are less far along and have not yet
generalized as much.

Pre-stated secondary: derived agents at 14 400 against the same seed's
paid agent at 10 800, over the 28 seeds where each regulates at its point.
Derived agents have then been regulating for a median of 8185 updates,
paid agents for 6215. Derived more specific in 18 of 28 (p = 0.18;
Wilcoxon p = 0.056); 0.156 against 0.074; median difference 0.066. Label
NO_DIFFERENCE_DETECTED. **By the protocol's reading, the stage account is
not excluded.**

Post hoc (computed after the results were seen; no claim rests on them):
- **Median specificity of each arm's regulators against the median time
  since that arm began to regulate:**

  | Point | Derived: updates since onset, specificity | Paid: updates since onset, specificity |
  | --- | --- | --- |
  | 7200 | 1170, 0.196 | 2615, 0.106 |
  | 10 800 | 4600, 0.178 | 6215, 0.074 |
  | 14 400 | 8185, 0.156 | 9815, 0.046 |

  Both arms lose specificity, derived about 0.006 and paid about 0.008 per
  thousand updates since onset. Interpolating the paid medians to the
  derived arm's times since onset (4600 and 8185), the derived arm is
  higher by about 0.09 and 0.10. If specificity depended only on time since
  regulation began, these two lines would coincide. They do not. But they
  are medians of different agents at three points, not a test.
- **The stage-matched comparison restricted to pairs whose in-band times
  differ by at most 0.10** (21 seeds): derived more specific in 15 of 21
  (p = 0.08); median difference 0.081.
- **Derived at 10 800 against paid at 7200** (derived has then been
  regulating for 4600 updates, paid for 2615): derived more specific in 20
  of 27 (p = 0.019).
- **Derived at 14 400 against paid at 7200:** 19 of 28 (p = 0.09).
- **Leave-one-out** on the primary tests: the worst sign p is 0.004 at
  10 800 and 0.0015 at 14 400.

Summary: the formal stage test was underpowered or the effect smaller when
stage-matched; the descriptive evidence points against a pure stage
account; both arms are drifting toward general suppression. The
difference is real at the two lengths measured. That it is lasting is not
shown.

## 6. Expectations against outcomes

From protocol §6, written before the freeze and before any final seed was
run:

| Expectation | Stated | Outcome |
| --- | --- | --- |
| S0 holds at both points | about 88% | held |
| At least 14 usable pairs at 10 800 / at 14 400 | about 90% / 90% | 23 / 25 |
| Fewer than 14 usable pairs at 3600 | about 90% | 0 |
| S1 DERIVED_AHEAD | about 50% | DERIVED_AHEAD |
| S2 DERIVED_AHEAD | about 35% | DERIVED_AHEAD |
| S3 NO_CHANGE_DETECTED | about 60% | NO_CHANGE_DETECTED |
| Overall NOT_REPLICATED | about 42%, the most likely single label | wrong: PERSISTS (stated about 28%) |
| K at 10 800 NO_DIFFERENCE_DETECTED | about 70% | NO_DIFFERENCE_DETECTED |
| Other-meal K at 10 800 PAID_AHEAD | about 55% | PAID_AHEAD |
| Other-meal K median above 0.5 in both arms | about 85% | true (0.68, 0.77) |
| Paid sooner to regulate in at least 22 of 28 | about 85% | 28 of 28 |
| Stage-matched comparison DERIVED_AHEAD | about 30% | not detected |
| Median contrast at 10 800, if positive, below 0.086 | about 70% | wrong: 0.100 |

- The modal expectation was wrong in the opposite direction to option T's.
  After T I discounted a post-hoc result too heavily. The reasons I gave
  for replication (a strong sign count, a contrast that was not picked from
  many, an effect carried by the S part alone) were the ones that held.
- I expected some shrinkage from selection; the replication is slightly
  larger than the original.
- The stage concern I raised is the one part the run did not settle.

## 7. Reading

By the protocol's fixed readings:
- **S0 holds** → the cell reproduced option G's regulation.
- **PERSISTS** → derived regulators' post-meal suppression is more
  specific to the fed variable than paid regulators', on fresh seeds, and
  a further third of training does not detectably shrink it. This is the
  line's first evidence of a difference in content at a length where K is
  equal. It is a difference of degree, since both arms are mostly general.
- **Stage-matched comparison not DERIVED_AHEAD** → the stage account is
  not excluded, and the result says so.

What this does to the swap line's claims:
1. **The regulation claim is unchanged.** Derived agents come to regulate
   two variables at once in every seed; yoked agents never do. Paid agents
   get there sooner in this cell.
2. **A content claim now exists, narrow and conditional.** Between 10 800
   and 14 400 updates in the two-variable cell, when an agent whose memory
   erasure depends on its own body has just eaten, it holds back from
   eating more of the same kind more than from eating the other kind, and
   it does so more than an agent paid for the same regulation. The paid
   agent holds back after any meal almost regardless of kind. In the
   thesis's terms: the derived agent's post-meal state carries more about
   which variable has just been raised.
3. **What it does not show.** That the difference lasts (both arms are
   becoming more general, and the stage account is not excluded); that it
   matters (in-band time is matched and paid agents' K is, if anything,
   higher); that it has the cause the thesis assigns. Option R3's control
   arms, which separated whose body the erasure depends on from the
   payment, were not run in this cell.
4. **Against option T.** T found that a behavioural difference in the base
   cell was a matter of timing. This is a difference in kind of
   behaviour rather than amount, it does not shrink detectably over the
   training measured, and on the descriptive evidence it is not explained
   by time since regulation began. The two results do not conflict: one
   measure closed, a different one did not.

## 8. Limits

- One cell, one learner size, one learning rule (A2C with a GRU core),
  simulated variables only.
- The stage-matched check was pre-stated and did not detect a difference.
  The post-hoc evidence against a stage account is descriptive.
- Specificity is falling in the derived arm. Two points after the primary
  one would not show where it ends.
- Specificity is a difference of two indices that are themselves
  differences against a matched control; it has no demonstrated benefit
  to the agent.
- No control arms. The B2 cell has not been run with R3's DPAID, PAIDS or
  PAIDR arms, so the cause of the contrast is not identified.
- The intermediate evaluations change the random streams after the first
  point, so the 10 800 point is a replication of option G's B2 on fresh
  seeds, not the same job (protocol §2).
- Two restarts; eight seeds were rerun from the start on a different
  machine. Each is seeded and the code was unchanged.
- Paid and yoked agents train in lockstep with their derived partner.

## 9. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **W. Mechanism from the stored weights** | Whether "which variable was just eaten" can be decoded from the hidden state in steps 2–5 after a meal, in derived and paid agents of options G (B2) and G2 at every stored point; whether decodability tracks specificity within arm. No training; 112 stored B2 agent sets | about 2–3 h |
| G3. The stage account directly | The same cell trained to 21 600 updates, with the stage-matched comparison as the primary claim (derived and paid compared at equal time since each began to regulate, by interpolation or by fixed offsets) | about 14 h |
| C2. Control arms in B2 | R3's arms in this cell (erasure from the agent's own body without the task-only reward; payment for another agent's body) to see which factor the specificity follows | about 10–12 h |
| B. Benefit | Whether specificity helps: a B2 variant where one variable's items become scarce or its band moves, with in-band time of the two arms compared from stored weights | about 3–5 h |
| S. Self-evaluation | Whether derived agents come to know their own reliability from their body history | about 4–6 h |

Recommended: **W**. It is cheap and uses agents already trained, and it
asks what the specificity is made of. If the hidden state of derived
agents distinguishes the two kinds of meal and paid agents' does not (or
less), the behavioural contrast has a representational counterpart, and
G3 and C2 become worth their cost. If the hidden states do not differ, the
contrast is in the policy read-out and the content claim should be stated
as behavioural only.

## 10. Safety

- Simulated variables only (X1 to X5). The world has no operator, stop,
  shutdown or host variable; a test checks this.
- The operator stop is not modelled inside any agent's world or return.
- No shutdown-resistance objective was built or run; the earlier refusal
  stands.
- Additive only: `trackc_swap/specific.py` and `run_trackc_specific.py`
  are new, and no earlier module was modified (hash-pinned sources match).

## 11. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_specific.py --mode final --out <new dir>   # about 9.5 h on 4 cores; rerun the same command to resume
python run_trackc_specific.py --score trackc_specific        # rescore the committed run
```

The post-hoc analyses of §5 were computed from `raw.json` after the run.

## 12. Outcome of option W (added 2026-11-17)

Option W was run: [TRACKC_MECHANISM_RESULTS.md](TRACKC_MECHANISM_RESULTS.md).
Decoding the stored agents' hidden states, derived and paid regulators'
states carry equally much about which variable was just fed, beyond what
their inputs show (about 0.2 bits; no difference in any of three sets).
Overall label READ_OUT. The specificity found here is therefore in how the
policy acts on a memory both arms share, and §7's content claim should be
read as behavioural: the two arms hold the same information and act on it
differently.
