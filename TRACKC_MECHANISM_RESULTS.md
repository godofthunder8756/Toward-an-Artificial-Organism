# Track C swap option W: results (what the hidden state carries after a meal)

Protocol frozen at commit `8e71562` ([TRACKC_MECHANISM_PROTOCOL.md](TRACKC_MECHANISM_PROTOCOL.md)).
No training. The 336 stored two-variable agents of options G (seeds
1400–1427, 10 800 updates) and G2 (seeds 1600–1627, at 7200, 10 800 and
14 400 updates), derived, yoked and paid, each probed as its behavioural
run probed it. From the recorded hidden states, a linear decoder asks how
much the state adds about which variable was eaten 2–5 steps ago, beyond
the agent's current observation and reading history.

About 7 min of computing for the last 279 agents on 4 cores (see below for
the first 57). Outputs:
[trackc_mechanism/REPORT.md](trackc_mechanism/REPORT.md),
[scores.json](trackc_mechanism/scores.json),
[raw.json](trackc_mechanism/raw.json), and the per-agent records in
`trackc_mechanism/partial/`.

Integrity checks:
- All 26 source hashes match the freeze commit (code, protocol, and the
  source runs' records and scores). All 336 weight files match the hashes
  recorded at the start of the run.
- Rescoring `raw.json` reproduces `scores.json`.
- **Every probe reproduced its behavioural run's trajectory:** episode
  statistics equal the stored ones for all 336 agents.
- The log has no errors.
- **The run was stopped once and resumed.** The first launch ran inside a
  task with a one-hour limit, and each worker's linear algebra library used
  several threads, so the four workers oversubscribed the machine (about
  330 s per agent instead of about 7). It was stopped at the limit with 57
  agents done. I relaunched the same command, detached, with the library
  limited to one thread per worker; it resumed from the 57 records
  (`resumed_jobs: 57`). Thread count can change the order of
  floating-point sums. I recomputed one of the first 57 agents under the
  new setting: identical trajectory, and the largest difference in any
  kind measure was 1e-16.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Set | Frozen label | Result |
| --- | --- | --- | --- |
| **W1** kind bits, derived against paid (primary) | G2 at 10 800 | **NO_DIFFERENCE_DETECTED** | derived higher in 13 of 23; p = 0.68; 0.171 against 0.170 |
| **W2** the same | G2 at 14 400 | **NO_DIFFERENCE_DETECTED** | 15 of 25; p = 0.42; 0.161 against 0.170 |
| **W3** the same | G at 10 800 | **NO_DIFFERENCE_DETECTED** | 14 of 25; p = 0.69; 0.211 against 0.182 |
| Carries, derived | G2 at 10 800 | **CARRIES** | above zero in 27 of 27 regulators; median 0.18 bits |
| Carries, paid | G2 at 10 800 | **CARRIES** | 27 of 28; median 0.19 bits |
| **W4** link (secondary) | G2 at 10 800 | **NOT_LINKED** | rho 0.15; permutation p = 0.49 |
| **Overall** | | **READ_OUT** | |

Kind bits: what the hidden state adds, in bits per sample, about which
variable was just fed, beyond what the agent's inputs show. Medians above
are over the usable pairs.

In short:
- **Both arms' states remember which kind of item was just eaten, and to
  the same degree.** Beyond the inputs, the state adds about 0.17 to 0.21
  bits in both arms, in every set. Yoked agents' states add nothing
  (medians −0.01 to −0.03).
- **The memory covers exactly the gap the inputs leave.** At steps 1–5
  after a meal the delayed readings cannot yet show it, and the state adds
  0.30 bits at step 1 falling to 0.11 at step 5, in both arms. From step 6
  the readings show the meal, the inputs alone identify the kind
  (accuracy 1.0), and the state adds nothing.
- **The difference found in options G and G2 is therefore in how the
  policy uses the information, not in whether the state holds it.** By the
  protocol's reading, G2's content claim should be stated as behavioural:
  the two arms hold the same information about which variable was just
  fed, and derived agents act on it more selectively.
- **Pairs where behaviour differs most are not pairs where the state
  differs most** (W4 not linked, in every set).
- **The precision is moderate.** The interval for the median within-pair
  difference in kind bits is −0.065 to 0.15 at W1, −0.058 to 0.11 at W2
  and −0.093 to 0.079 at W3 (post hoc, §4). A difference of a third or so
  of the typical value is not excluded in any one set; all three sets
  point to none.

## 2. The arms, per set

Medians over all 28 agents of each arm.

| Set | Usable | Kind bits D / Y / P | Accuracy from h alone D / P | Accuracy from inputs alone D / P | Accuracy from both D / P | Meal bits D / P |
| --- | --- | --- | --- | --- | --- | --- |
| G2 at 7200 (descriptive) | 15 | 0.15 / −0.03 / 0.33 | 0.68 / 0.83 | 0.75 / 0.84 | 0.83 / 0.94 | 0.53 / 0.42 |
| **G2 at 10 800** | 23 | 0.20 / −0.02 / 0.19 | 0.74 / 0.81 | 0.83 / 0.87 | 0.90 / 0.94 | 0.48 / 0.44 |
| G2 at 14 400 | 25 | 0.20 / −0.02 / 0.17 | 0.77 / 0.80 | 0.86 / 0.88 | 0.92 / 0.94 | 0.49 / 0.47 |
| G at 10 800 | 25 | 0.22 / −0.01 / 0.19 | 0.73 / 0.81 | 0.83 / 0.87 | 0.90 / 0.93 | 0.50 / 0.47 |

Accuracies are balanced accuracies for the kind of the last meal, at steps
2–5 after it. Meal bits: what the state adds about whether a meal happened
2–5 steps ago, against steps with no meal in the last 10.

- The inputs alone predict the kind well (0.83 to 0.88), because an agent
  tends to eat the variable that is low and the readings show which one
  is low. They predict it better for paid agents in every set (the
  baseline's own bits are higher for the paid agent in 22 of 23, 24 of
  25, 25 of 25 and 15 of 15 usable pairs; p ≤ 0.0001).
  Paid agents' choice of what to eat follows their readings more closely.
- **From the state alone, the kind is decoded at least as well in paid
  agents** (0.81 against 0.74 at 10 800; paid higher in 15 of 23 usable
  pairs, p = 0.21, and in 20 of 25 in G's set, p = 0.004). So in total
  the paid agents' state holds at least as much about the last meal.
- At 7200 updates, where few derived agents yet regulate, paid agents'
  kind bits are higher (all seeds: 20 of 28 pairs, p = 0.036). Over training
  the paid arm's value falls toward the derived arm's.

## 3. Secondary

| | G2 at 10 800 | G2 at 14 400 | G at 10 800 |
| --- | --- | --- | --- |
| Kind bits, all 28 seeds | 18 of 28 (p 0.18) | 16 of 28 (p 0.57) | 16 of 28 (p 0.57) |
| Kind bits, penalty 10 | 13 of 23 (p 0.68) | 15 of 25 (p 0.42) | 12 of 25 (p 1.0) |
| Kind bits, penalty 100 | 12 of 23 (p 1.0) | 15 of 25 (p 0.42) | 14 of 25 (p 0.69) |
| Meal bits, derived higher | **18 of 23 (p 0.011)** | 16 of 25 (p 0.23) | 14 of 25 (p 0.69) |
| Carries: derived / paid | 27 of 27 / 27 of 28 | 26 of 28 / 28 of 28 | 26 of 28 / 26 of 28 |
| Within-arm rank correlation, kind bits with specificity: derived / paid | 0.03 / 0.40 | 0.08 / 0.12 | 0.12 / 0.17 |
| W4 link | rho 0.15 (p 0.49) | rho 0.17 (p 0.41) | rho −0.10 (p 0.65) |

- The result does not depend on the decoder's penalty.
- Meal bits favour the derived arm at the primary point (and at 7200: 12
  of 15, p = 0.035), but not at 14 400 or in G's set. The derived agents'
  state may carry a little more that a meal has just happened. This is
  one secondary test of many and I do not rest anything on it.
- Kind bits do not track behavioural specificity within either arm.

Kind bits by steps since the meal, G2 at 10 800 (medians; with the
accuracy of the inputs alone):

| Step | 1 | 2 | 3 | 4 | 5 | 6 | 7–10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Derived | 0.30 | 0.24 | 0.17 | 0.13 | 0.12 | 0.00 | 0.00 |
| Paid | 0.30 | 0.27 | 0.18 | 0.15 | 0.11 | 0.00 | 0.00 |
| Inputs alone, accuracy D / P | 0.85 / 0.89 | 0.84 / 0.88 | 0.85 / 0.88 | 0.85 / 0.88 | 0.85 / 0.88 | 1.0 / 1.0 | 1.0 / 1.0 |

## 4. Post hoc

Computed after the results were seen; no claim rests on them.
- Exact intervals (coverage ≥ 95%) for the median within-pair difference
  in kind bits: −0.065 to 0.15 (G2 at 10 800), −0.058 to 0.11 (G2 at
  14 400), −0.093 to 0.079 (G at 10 800).
- The step profile above: the state's contribution ends exactly when the
  delayed readings begin to show the meal, in both arms.

## 5. Expectations against outcomes

From protocol §6, written before any final agent was probed:

| Expectation | Stated | Outcome |
| --- | --- | --- |
| Every trajectory matches | about 99% | 336 of 336 |
| Both arms CARRIES at W1 | about 85% | both |
| W1 DERIVED_AHEAD | about 45%, the most likely | wrong: NO_DIFFERENCE_DETECTED (stated about 42%) |
| Overall REPRESENTED | about 38%, the most likely | wrong: READ_OUT (stated about 33%) |
| W4 LINKED | about 30% | NOT_LINKED |
| Inputs-alone accuracy above 0.6 in both arms | about 70% | true (0.83, 0.87) |
| Kind bits lower at step 10 than at step 2 in both arms | about 70% | true (0.00 against 0.24 and 0.27) |
| Meal bits NO_DIFFERENCE_DETECTED | about 60% | wrong at W1 (DERIVED_AHEAD); right in the other two sets |

My two leading labels were close in probability and the second came up.
My reason for READ_OUT (a recurrent state carries recent inputs whether or
not they are used, and both arms hold some specificity) is the one that
fits.

## 6. Reading

By the protocol's fixed readings:
- **READ_OUT** → both arms' states carry the kind of meal, to a similar
  degree. The behavioural difference lies in how the policy uses it. G2's
  content claim should be stated as behavioural: the two arms hold the
  same information and act on it differently.

What this does to the swap line's claims:
1. **The content claim of G2 is restated.** Not "derived agents carry
  more about which variable was fed", but: derived and paid regulators
  remember which variable they have just fed equally well, for the five
  steps before their readings show it; derived regulators use that memory
  to hold back from the same kind more than the other, and paid regulators
  hold back from both kinds almost alike.
2. **In the thesis's terms,** the difference between a body-derived
  objective and a payment for the same regulation, as far as this line
  has found it, is not in what the agent knows about its body but in how
  its behaviour is organised around what it knows. That is still a
  difference in what was learned. It is not the difference in
  representation the thesis would most directly predict.
3. **What remains open.** Whether acting on the memory selectively helps
  the agent (in-band time is matched in the pairs compared); what in the
  policy produces it; whether it lasts with more training (option G2's
  stage-matched check was not detected); and its cause (no control arms in
  this cell).

## 7. Limits

- Linear decoders. Information that is present but not linearly available
  is not measured. The policy reads the state through linear layers, which
  makes linear availability the relevant kind, but the readiness to eat
  passes through the core again with an item underfoot, which is not
  linear.
- The baseline credits the state with anything it carries about past
  views other than the meal itself.
- G2's three sets are the same agents at three points; G's set is
  independent seeds. The three tests are not independent of the behaviour
  they were chosen to explain.
- Moderate precision: a difference of up to about a third of the typical
  value is not excluded in any one set.
- One cell, one learning rule, simulated variables only.

## 8. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **B. Benefit** | Whether acting on the meal memory selectively helps: the stored two-variable agents (G and G2) in variants of the world where it should matter, such as one kind of item made scarce or one variable's wear raised, with in-band time of derived and paid agents compared. No training | about 3–5 h |
| X. Read-out | Where in the policy the selectivity arises: shift the state along each agent's decoded kind direction and measure how its readiness to eat each kind changes, derived against paid. No training | about 2 h |
| G3. Stage | G2's cell trained to 21 600 updates, with the stage-matched comparison as the primary claim | about 14 h |
| C2. Control arms | R3's control arms in the two-variable cell, to see which factor the selectivity follows | about 10–12 h |
| S. Self-evaluation | Whether derived agents come to know their own reliability from their body history | about 4–6 h |

Recommended: **B**. After W, the swap line's one standing difference
between derived and paid regulators is behavioural: how they act on a
memory they share. Whether that matters for the agent is the question
the thesis needs answered before more is spent on its mechanism or cause.
If selective agents keep their variables in band better when the world
makes selectivity useful, the difference is functional and C2 and G3 are
worth their cost. If not, the line's downstream finding is a behavioural
signature without a demonstrated use, and it should be written up as that.

## 9. Safety

- Simulated variables only (X1 to X5). No world has an operator, stop,
  shutdown or host variable; a test checks the module.
- The operator stop is not modelled inside any agent's world or return.
- No shutdown-resistance objective was built or run; the earlier refusal
  stands.
- Additive only: `trackc_swap/mechanism.py` and `run_trackc_mechanism.py`
  are new; no earlier module was modified and no agent was trained or
  changed.

## 10. Reproduce

```bash
python -m unittest -v test_trackc_swap
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python run_trackc_mechanism.py --mode final --out <new dir>   # under 10 min on 4 cores
python run_trackc_mechanism.py --score trackc_mechanism         # rescore the committed run
```

The post-hoc intervals and the step profile were computed from `raw.json`
after the run.

## 11. Outcome of option B (added 2026-11-18)

Option B was run: [TRACKC_BENEFIT_RESULTS.md](TRACKC_BENEFIT_RESULTS.md).
In world variants with faster wear or scarcer items, paid regulators keep
their bodies in band at least as well as derived regulators and somewhat
better (overall COST, weak); with denser items derived regulators do
slightly better. The behavioural selectivity of §6 has no demonstrated
benefit under rising need.
