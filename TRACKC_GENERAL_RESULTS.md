# Track C swap option G: results (generality: a larger learner and a two-variable body)

Protocol frozen at commit `2a22e1c` ([TRACKC_GENERAL_PROTOCOL.md](TRACKC_GENERAL_PROTOCOL.md)).
Two cells, three arms each (derived, yoked, paid), 28 fresh seeds per cell:
- **H128:** the base world with a 128-unit core, seeds 1300–1327.
- **B2:** two body variables with a 64-unit core and three times the
  training, seeds 1400–1427.

About 9 h of computing on 4 cores. Outputs:
[trackc_general/REPORT.md](trackc_general/REPORT.md),
[scores.json](trackc_general/scores.json),
[raw.json](trackc_general/raw.json), the per-job records in
`trackc_general/partial/`, and the weights of all three arms per seed.

Integrity checks:
- All 19 source hashes match the freeze commit.
- Rescoring `raw.json` reproduces `scores.json`.
- The log has no errors. No-fate task accuracy is 0.9997 (H128) and 0.999
  (B2), so both cells are valid.
- **The run was interrupted once and resumed.** The machine restarted after
  32 of 56 jobs. The four B2 jobs then in progress were lost and rerun from
  the start; the 32 finished records were kept. Each job is seeded on its
  own and the code was unchanged, so the resumed jobs are the computations
  they would have been. `raw.json` records `resumed_jobs: 32`.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Frozen label | Result | Needed |
| --- | --- | --- | --- |
| **G0, H128** derived regulation | **HOLDS** | 28 of 28 derived agents regulate; 0 of 28 yoked | 19; at most 1 |
| **G0, B2** derived regulation | **HOLDS** | 28 of 28 derived agents regulate; 0 of 28 yoked | 19; at most 1 |
| **G1, H128** K, derived against paid | **DERIVED_AHEAD** | derived higher in 19 of 25; p = 0.015; 0.91 against 0.77 | p ≤ 0.05 |
| **G1, B2** K, derived against paid | **NO_DIFFERENCE_DETECTED** | derived higher in 8 of 25; p = 0.11; 0.85 against 0.88 | p ≤ 0.05 |
| **Overall** | **HOLDS_IN_H128_ONLY** | | |

K is the combined post-meal suppression index of R2, unchanged; in B2 it is
the mean of the two variables' K.

Holm-adjusted p over the two G1 tests: H128 0.029, B2 0.11. The H128 test
passes after adjustment, so the label is not weak.

In short:
- **Derived regulation extends to both new cells.** Every derived agent
  regulates and no yoked agent does, with independent optimizers.
- **The behavioural difference is found with the larger learner, at about
  half the base cell's size or less.** The median within-pair difference in
  K is 0.12, against 0.40 (R3) and 0.24 (R4). It shrank because paid agents'
  K rose (0.79, against 0.47 to 0.64 in the base cell); derived agents' K is
  where it was (0.91).
- **It is not found with a two-variable body, and the direction there is
  the other way.** Paid agents have the higher K in 17 of 25 pairs. The
  interval for the median difference (−0.08 to 0.005; post hoc) excludes
  the difference seen in H128 and in the base cell. So this is not a
  smaller version of the same effect: at this size there is none, or a
  small reversed one.
- **In B2, most of what K measures is not specific to the variable that was
  fed.** A meal of one kind suppresses readiness to eat the other kind
  almost as much (derived 0.65 against 0.84; paid 0.79 against 0.90). The
  protocol said this should be near zero if what an agent carries after a
  meal is about the variable the meal raised. It is not near zero in either
  arm.
- **The downstream claim of the swap line is therefore narrower than R2 to
  R4 suggested.** Paid agents can acquire the behaviour. How far they do
  depends on the cell.

## 2. G0 and the arms

Medians over 28 seeds, at the end of training:

| Cell | Arm | Regulators | In band | Eats when low ÷ when high | Task accuracy | First sustained regulation (updates) |
| --- | --- | --- | --- | --- | --- | --- |
| H128 | derived | 28 | 0.947 | 63 | 0.990 | 885 |
| H128 | paid | 28 | 0.944 | 60 | 0.989 | 1005 |
| H128 | yoked | 0 | 0.283 | 0.97 | 0.989 | never |
| B2 | derived | 28 | 0.866 | 39 | 0.970 | 6250 |
| B2 | paid | 28 | 0.867 | 41 | 0.969 | 4540 |
| B2 | yoked | 0 | 0.176 | 0.98 | 0.971 | never |

- In B2 "in band" means both variables in band together. Each variable
  alone is in band 0.93 of the time in derived and paid agents, and 0.31 in
  yoked agents.
- With erasure off (the probe run), all 56 derived and all 56 paid agents
  still regulate. In-band medians: H128 0.950 and 0.943; B2 0.838 and
  0.870.
- Usable pairs (both regulators, in band within 0.10): 25 of 28 in each
  cell. Within 0.05: 20 in H128, 22 in B2. The median in-band difference
  within usable pairs is −0.003 in H128 and +0.003 in B2, so the K
  comparison is between equally good regulators.
- Over R to R4 and this run, 158 of 158 derived agents trained with
  independent optimizers regulate, and 0 of 158 yoked agents.

## 3. G1 in H128: the difference is found, smaller

| Measure, usable pairs (25) | Derived | Paid | Derived higher | Sign p | Wilcoxon p | Median difference |
| --- | --- | --- | --- | --- | --- | --- |
| **K (primary)** | 0.909 | 0.773 | 19 | 0.015 | 0.0009 | 0.125 |
| S (eat readiness) | 0.878 | 0.678 | 18 | 0.043 | 0.16 | 0.087 |
| M (approach) | 0.287 | 0.166 | 17 | 0.11 | 0.014 | 0.092 |

- K on all 28 seeds: derived higher in 22 (p = 0.004). On the 20 pairs
  within 0.05 in band: 15 (p = 0.041).
- K ranges: derived 0.59 to 0.98; paid 0.01 to 0.96, with one paid agent
  below 0.5 (seed 1316). In the base cell the paid agents' median K was
  itself near 0.5 (0.47 to 0.64).
- Four derived agents (seeds 1301, 1308, 1319, 1327) and no paid agent have
  flat eat readiness (Fisher p = 0.11). They hold back after a meal by not
  approaching food (M 0.80 to 0.94) while their readiness to eat does not
  change (S near 0).
- K rises with in-band time within each arm (rank correlation 0.39 derived,
  0.28 paid), as R4 found.
- Derived agents reached sustained regulation sooner in 22 of 27 seeds
  (p = 0.0015). The four calibration seeds had suggested the opposite.
- Post hoc: dropping any one pair leaves the sign test at p ≤ 0.023. An
  exact interval for the median difference is 0.06 to 0.20 (95.7%), which
  lies below both base-cell medians.

## 4. G1 in B2: the difference is not found

| Measure, usable pairs (25) | Derived | Paid | Derived higher | Sign p | Wilcoxon p | Median difference |
| --- | --- | --- | --- | --- | --- | --- |
| **K (primary)** | 0.853 | 0.883 | 8 | 0.11 | 0.15 | −0.030 |
| K, variable 0 | 0.862 | 0.883 | 8 | 0.11 | 0.18 | −0.026 |
| K, variable 1 | 0.870 | 0.901 | 9 | 0.23 | 0.09 | −0.035 |
| S (eat readiness) | 0.788 | 0.820 | 11 | 0.69 | 0.34 | −0.056 |
| M (approach) | 0.320 | 0.291 | 13 | 1.0 | 0.75 | 0.012 |
| K from the other variable's meals | 0.665 | 0.788 | 5 | 0.004 | 0.003 | −0.131 |

- K on all 28 seeds: derived higher in 8, paid in 20 (p = 0.036). The
  scorer's descriptive label for that secondary test is PAID_AHEAD. It is
  one of several secondary tests, uncorrected, and the primary test does
  not reach it. On the 22 pairs within 0.05: derived higher in 7
  (p = 0.13).
- K ranges: derived 0.67 to 0.93; paid 0.69 to 0.96. No agent of either arm
  is below 0.5 and none has flat eat readiness.
- K rises with in-band time within each arm here too (0.37 derived, 0.36
  paid).
- Paid agents reached sustained regulation sooner in 28 of 28 seeds
  (medians 4540 against 6250 updates, of 10 800).
- Post hoc: an exact interval for the median difference is −0.08 to 0.005
  (95.7%). "No difference detected" is not equivalence, but this interval
  excludes H128's 0.125 and the base cell's 0.24 and 0.40.

## 5. Secondary and post hoc

Pre-stated, computed by the scorer (reported in §2 to §4): K on all seeds
and on tight pairs, the in-band difference, the rank correlation of K with
in-band time, effect size beside the base cell's, S and M, flat readiness,
learning speed, regulation with erasure off, K for each variable, and
specificity.

**Specificity in B2 (pre-stated).** For each variable, K was recomputed
with "after a meal" timed from the last meal of the other variable, over
steps with no meal of its own in the last 10, matched on its own reading.

| Arm (28 seeds) | K from own meals | K from the other variable's meals | Other ÷ own |
| --- | --- | --- | --- |
| Derived | 0.844 | 0.652 | 0.79 |
| Paid | 0.896 | 0.792 | 0.89 |
| Yoked | 0.00 | 0.00 | |

- Own-meal K is above other-meal K in every derived agent (28 of 28) and in
  27 of 28 paid agents, so some of the suppression is specific. Most of it
  is not.
- Paid agents have the higher other-meal K in 20 of 25 usable pairs
  (p = 0.004).

**Post hoc (not in the protocol; hypotheses, not findings).**
- *Specificity as a difference.* Own-meal K minus other-meal K is larger in
  the derived agent in 21 of 25 usable pairs (p = 0.0009; medians 0.18
  against 0.10), and in 23 of 28 seeds. I computed this after seeing that
  the primary test in B2 had gone the other way, so it is exactly the kind
  of contrast that needs a fresh run before it carries weight.
- *Across cells.* Paid agents' median K is 0.47 to 0.64 in the base cell
  (R2 to R4), 0.79 in H128 and 0.90 in B2. Derived agents' is 0.88 to 0.90,
  0.91 and 0.84. The cells used different seeds and are not paired, so this
  is a description.
- *K against when regulation was reached.* Within each arm of each cell the
  rank correlation of K with the update of first sustained regulation is
  small (−0.23 to 0.10). Agents that regulated earlier, and so trained
  longer as regulators, do not have clearly higher K at the end.
- *Intervals and leave-one-out* in §3 and §4.

## 6. Expectations against outcomes

From protocol §6, written before any result of either cell:

| Expectation | Stated | Outcome |
| --- | --- | --- |
| H128: G0 holds | about 90% | held (28 of 28) |
| H128: at least 14 usable pairs | about 85% | 25 |
| H128: G1 DERIVED_AHEAD | about 65% | DERIVED_AHEAD |
| B2: G0 holds (after calibration) | about 80% | held (28 of 28) |
| B2: at least 14 usable pairs | about 75% | 25 |
| B2: G1 DERIVED_AHEAD | about 45% | not found; NO_DIFFERENCE_DETECTED (stated about 25%) |
| Overall: HOLDS_IN_H128_ONLY | about 35%, the most likely single label | this label |
| Median difference below the base cell's range in each cell | about 60% | true in both |
| B2: other-meal K well below own-meal K in derived agents | about 65% | wrong: 0.65 against 0.84 |

- The overall label is the one I thought most likely, and my stated reason
  for the lower H128 number (a larger core gives a paid agent more room to
  carry the memory of a meal as well) matches how the difference shrank.
- I gave a reversed label in B2 about 2%. The primary test did not reach
  it, but the direction is reversed and one secondary test carries that
  label. I under-weighted a reversal.
- I expected the suppression to be mostly specific to the fed variable. It
  is mostly general.
- The learning-speed pattern seen in calibration held in B2 (paid sooner in
  28 of 28) and did not hold in H128 (derived sooner in 22 of 27).

## 7. Reading

By the protocol's fixed readings:
- **G0 holds in both cells** → derived regulation extends to a 128-unit
  learner and to a two-variable body.
- **G1 DERIVED_AHEAD in H128** → the downstream difference is found with
  the larger learner.
- **G1 NO_DIFFERENCE_DETECTED in B2** → not found there at this size. The
  secondary effect size says it is absent or slightly reversed, not merely
  smaller.
- **HOLDS_IN_H128_ONLY** → the difference survives a larger learner. With a
  two-variable body it is not shown, and the protocol lists what else
  changed there: twice the items, a larger observation, a different rule
  for combining two hazards, and three times the training.

What this does to the swap line's claims:
1. **The regulation claim is stronger.** An agent whose only pressure is
   that erasure depends on its own body state comes to regulate that body
   in every cell tried, including one where it has to keep two variables in
   band at once.
2. **The downstream claim is weaker.** R2 to R4 found that derived agents
   hold back after a meal they cannot yet sense and that paid agents mostly
   do not. That is not a general property of the two arms. Paid agents
   acquire the behaviour to a large degree with a larger core, and fully in
   the two-variable cell.
3. **The trend runs against the thesis's use of the result.** The thesis is
   about large systems. Doubling the core roughly halved the difference,
   from the paid side. The protocol named a difference that capacity
   removes as the most damaging outcome; capacity has not removed it here,
   but it has moved it in that direction.
4. **K is less specific than its name suggested.** In the only cell where
   it can be checked, most of the post-meal suppression follows any meal,
   in both arms. In the base cell there is one kind of meal, so R2 to R4
   could not tell "this meal will raise this variable" from "I have just
   eaten". Their K differences stand as measured; what they are differences
   in is less clear.

A hypothesis that fits all three cells, stated after the fact: the two arms
differ in how readily a learner comes to hold back after a meal, not in
whether it can. In the base cell a paid agent can regulate well without
doing so, and many stop there. More capacity, more training or a harder
regulation problem brings paid agents to it. This run cannot tell those
three apart.

The post-hoc specificity contrast (§5) points the other way from the B2
primary result, toward derived agents carrying more variable-specific
content. It is untested and I do not rest anything on it.

## 8. Limits

- B2 differs from the base cell in several linked ways, and no cell here
  changes only one of them. In particular this run cannot say whether
  three times the training would by itself remove the difference in the
  base cell.
- H128 is one step in capacity. Whether the difference keeps shrinking
  with size is not shown.
- No control arms were rerun (DPAID, PAID0, DNOISE), so nothing here says
  whether the H128 difference has the cause R3 and R4 pointed to in the
  base cell.
- B2's design was settled in calibration (the hazard rule and the training
  length), on regulation alone. Four calibration seeds were seen under more
  than one setting. No final seed was.
- The specificity measure conditions on no own-kind meal in the last 10
  steps. Steps soon after one kind of meal in which the agent has not
  eaten the other kind for a while may differ from other steps in ways the
  matching on the reading does not remove.
- K measures a behaviour with no demonstrated benefit: in-band time is
  matched in the pairs compared.
- One learning rule (A2C with a GRU core) in one family of small grid
  worlds. Simulated variables only.

## 9. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **T. Training length in the base cell** | Whether the base-cell difference is a stage of learning. Derived, yoked and paid agents in the base cell for 10 800 updates, with K measured at 3600, 7200 and 10 800. Separates "more training" from the other changes in B2, and would show whether paid agents' K rises once they already regulate | about 6 h |
| W. Mechanism from the stored weights | What in the hidden state carries "a meal has just happened", in derived and paid agents of the base cell, H128 and B2, and in B2 whether it says which variable was fed. Would test the post-hoc specificity contrast on existing agents, though not on fresh seeds. No training | about 2 h |
| G2. Specificity as a primary claim | The post-hoc contrast of §5 on fresh B2 seeds, frozen in advance | about 6.5 h |
| H256. A second step in capacity | Whether the H128 difference keeps shrinking | about 4–5 h |
| S. Self-evaluation | Whether derived agents come to know their own reliability from their body history; with a paid arm as the comparison | about 4–6 h |
| V. Rerun the other cells with independent optimizers | SAT 0.1, GRADED 0.3 and 0.1, and M0 | about 3 h |

Recommended: **T**. It is the most direct test of the unfavourable
hypothesis in §7. If paid agents' K climbs to the derived level with
training alone, the downstream claim reduces to a difference in learning
speed and should be stated that way. If it does not, the two-variable body
itself is what removed the difference, and G2 or W becomes the next
question.

## 10. Safety

- Simulated variables only (X1 to X5). The two-variable world has no
  operator, stop, shutdown or host variable; a test checks this.
- The operator stop is not modelled inside any agent's world or return.
- No shutdown-resistance objective was built or run; the earlier refusal
  stands.
- Additive only: `trackc_swap/general.py` and `run_trackc_general.py` are
  new, and no earlier module was modified (hash-pinned sources match).

## 11. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_general.py --mode final --out <new dir>   # about 9 h on 4 cores; rerun the same command to resume
python run_trackc_general.py --score trackc_general         # rescore the committed run
```

The post-hoc analyses (intervals, leave-one-out, the specificity
difference, K against the time regulation was reached, and the cross-run
medians) were computed from `raw.json` and the earlier runs' `scores.json`
after the run.
