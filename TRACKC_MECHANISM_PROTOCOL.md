# Track C swap, option W: protocol (what the hidden state carries after a meal)

Status: frozen by the commit that says "Freeze". Requested by the PI
("Proceed with W") after [option G2](TRACKC_SPECIFIC_RESULTS.md). Not
reviewed by Astra (waived by the PI). No consciousness claim. No training.

## 1. Why

Options G and G2 found, in the two-variable cell (B2), that derived
regulators hold back after a meal more specifically to the variable that
was fed than paid regulators do (G2: 19 of 23 pairs at 10 800 updates, 21
of 25 at 14 400), while K itself is equal or slightly favours the paid arm.
That is a difference in behaviour. This option asks where it lives:
- in what the recurrent state carries (the derived agent's state says more
  about which kind of item it has just eaten), or
- in how the policy reads a state that carries the same thing in both arms.

## 2. Design

**Agents.** Stored weights only; nothing is trained.

| Set | Source | Seeds | Updates | Claim |
| --- | --- | --- | --- | --- |
| G2_10800 | option G2 | 1600–1627 | 10 800 | **W1 (primary)** |
| G2_14400 | option G2 | 1600–1627 | 14 400 | W2 |
| G_10800 | option G (B2) | 1400–1427 | 10 800 | W3 |
| G2_7200 | option G2 | 1600–1627 | 7200 | descriptive |

Each set has a derived, a yoked and a paid agent per seed (336 agents).
Which agents regulate and which pairs are usable are taken from the source
run's frozen scores (usable pairs: 23, 25, 25, 15).

**Probe.** Each agent is run exactly as the source run's downstream probe
ran it (`general.run_probe_g`): same world seed, streams and action
sampling, erasure off, 128 environments, 4 episodes of 500 steps. A unit
test checks that the trajectory is identical; the scorer also counts, for
every agent, whether the probe's episode statistics equal the stored ones.
At every step t (from step 9 of an episode) the state h_t that the policy
reads is recorded with:
- the observation o_t, without the zeroed echo (80 inputs);
- both interoceptive readings over the previous nine steps (18 inputs);
- the steps since the last meal of each variable.

**Samples.**
- *Kind:* steps 2–5 after a meal of variable k (as in every post-meal
  measure since option Q), where the other variable's last meal was at
  least 10 steps before that meal. Label k.
- *Meal:* the same post-meal steps (label 1) against steps with no meal of
  either variable in the last 10 steps (label 0), the latter subsampled
  with a fixed seed to the same number.

**Decoders.** L2-regularised logistic regression (penalty 1.0 on
standardised weights, as option P's ridge decoders), fitted by Newton's
method, two-fold cross-validated across environments (by parity, as option
P). Three decoders per sample set:
- B, the baseline: o_t and the reading history. It holds everything the
  agent sees now and has recently seen of its body, but not the meal: the
  eaten item has gone from the view, and the delayed readings do not show
  a meal until 6 steps after it.
- H: h_t alone.
- HB: h_t and the baseline together.

**Measure.** Kind bits = (cross-validated log-likelihood of HB − that of B)
/ number of samples, in bits: what the state adds about which variable was
just fed, beyond the agent's current inputs and reading history. This
conditions on the readings as the behavioural measures did by matching:
an agent tends to eat the variable that is low, so the readings alone
predict the kind to some degree, and a state that merely tracks the
readings would otherwise look as if it remembered the meal. A measure
needs at least 1000 samples of each class, or it is undefined.

Known limits:
- A linear decoder finds what is linearly available; the policy is linear
  in h, so this is the relevant kind of availability, but not all of it.
- The baseline does not include the item views of past steps, which would
  contain the meal itself. Information the state carries about the recent
  view history other than the meal (for example where items of each kind
  were) is credited to the state.
- The agents of G2 are the same agents at three points. G's agents are
  different seeds.
- The sets of usable pairs come from the behavioural runs and are not
  re-judged.

## 3. Calibration

None. No final agent was probed before the freeze. Engineering used a
randomly initialised agent and the scratch weights of option G2's smoke
run (trained 80 updates). One choice was made from them: a full-size probe
of a smoke agent gave 433 kind samples and a strongly negative baseline
log-likelihood (overfitting), so the minimum was raised from 200 to 1000
samples per class. The penalty was not tuned.

## 4. Decision rules

All pair tests are two-sided paired sign tests at 0.05, derived against
paid, over the set's usable pairs, with at least 14 pairs, as in R2 to G2.

**W1 (primary):** kind bits, derived against paid, in G2_10800. Labels
DERIVED_AHEAD, PAID_AHEAD, NO_DIFFERENCE_DETECTED, UNDETERMINED.
**W2:** the same in G2_14400. **W3:** the same in G_10800.

**Carries:** within each arm of G2_10800, over that arm's regulators, a
two-sided sign test of kind bits against 0. CARRIES, NOT_DETECTED,
UNDETERMINED (fewer than 14).

**Overall:**

| W1 | Other | Label |
| --- | --- | --- |
| DERIVED_AHEAD | W2 or W3 DERIVED_AHEAD | REPRESENTED |
| DERIVED_AHEAD | neither | MIXED |
| NO_DIFFERENCE_DETECTED | both arms CARRIES | READ_OUT |
| NO_DIFFERENCE_DETECTED | both arms NOT_DETECTED | NOT_IN_STATE |
| NO_DIFFERENCE_DETECTED | otherwise | UNRESOLVED |
| PAID_AHEAD | | REVERSED |
| UNDETERMINED | | UNDETERMINED |

**Multiplicity.** Holm over W1, W2 and W3. REPRESENTED is marked weak
unless W1 and at least one of W2 and W3 pass after adjustment.

**W4, link (pre-stated secondary with its own label).** In G2_10800, over
usable pairs, the rank correlation between the within-pair difference in
kind bits and the within-pair difference in behavioural specificity (from
G2's stored records), with a two-sided permutation p (10 000 permutations,
fixed seed). LINKED if positive with p ≤ 0.05; NOT_LINKED; UNDETERMINED
under 14 pairs.

**Secondary,** computed by the frozen scorer for every set: kind bits on
all seeds; meal bits (derived against paid); decoding accuracy from h
alone and from the baseline alone; the baseline's own bits; kind bits with
penalties 10 and 100; within-arm rank correlation of kind bits with
specificity; kind bits at each step 1–10 after the meal; medians per arm,
including yoked agents; the carries tests and W4 in every set; trajectory
matches.

## 5. Readings, fixed in advance

- **REPRESENTED** → the derived agents' state carries more about which
  variable was just fed, beyond their inputs, than the paid agents' state,
  in fresh-seed agents and again in a second set. The behavioural
  specificity has a representational counterpart. If W4 is LINKED, the
  pairs where the state differs most are the pairs where behaviour differs
  most.
- **MIXED** → found in the primary set only; not established.
- **READ_OUT** → both arms' states carry the kind of meal, to a similar
  degree. The behavioural difference lies in how the policy uses it. The
  content claim of G2 should then be stated as behavioural: the two arms
  hold the same information and act on it differently.
- **NOT_IN_STATE** → the state adds nothing detectable beyond the inputs
  in either arm. The specificity then comes from what the inputs show
  (for example the readings), not from a remembered meal.
- **REVERSED** → the paid agents' state carries more and they use it less.
- **UNRESOLVED / UNDETERMINED** → no claim.
- Trajectory mismatches in more than a few agents would mean the probe
  does not measure the agents the behavioural runs measured; that
  outranks every label.

## 6. Expectations

Written before any final agent was probed:
- Every trajectory matches: about 99%.
- Both arms CARRIES in G2_10800: about 85%.
- **W1:** DERIVED_AHEAD about 45%, NO_DIFFERENCE_DETECTED about 42%,
  PAID_AHEAD about 8%, UNDETERMINED about 5%.
- **Overall:** REPRESENTED about 38%, READ_OUT about 33%, REVERSED about
  8%, MIXED about 7%, UNRESOLVED about 5%, UNDETERMINED about 5%,
  NOT_IN_STATE about 4%.
- **W4** LINKED: about 30%.
- Baseline accuracy above 0.6 in both arms (the readings and view
  predict the kind): about 70%.
- Kind bits lower at step 10 than at step 2 in both arms: about 70%.
- Meal bits, derived against paid: NO_DIFFERENCE_DETECTED about 60%.

Reasons. For REPRESENTED: the specificity is in the readiness to eat an
item already underfoot, a function of the state; a policy difference of
this kind is most simply produced by a state difference. For READ_OUT: a
recurrent state tends to carry recent inputs whether or not they are used,
both arms see the same kind of meals, and within each arm own-meal K
exceeded other-meal K in almost every agent, so both arms hold some of it.

## 7. Engineering before the freeze

- `trackc_swap/mechanism.py` (new): the recording probe, sample sets and
  decoders. `run_trackc_mechanism.py` (new): runner and scorer; reads the
  stored weights and the source runs' records and scores, which are
  hash-pinned with the code. No earlier module was modified.
- A smoke run on option G2's smoke weights ran end to end (too few samples
  for any measure, as expected) and matched every trajectory.
- Five new unit tests (121 in all): the probe reproduces option G's
  downstream probe trajectory; the sample rules; the decoders on
  synthetic data (no gain from an uninformative state, a gain from an
  informative one); the decision rules including the weak flag and the
  link test; the final configuration (sets, usable counts, weight files);
  no operator variable.
- Estimated time: under an hour on 4 cores.

## 8. Safety

- Simulated variables only (X1 to X5). No world in this option has an
  operator, stop, shutdown or host variable; a test checks the module.
- The operator stop is not modelled inside any agent's world or return.
- No shutdown-resistance objective is built or run; the earlier refusal
  stands.
- Additive only; earlier modules are hash-pinned and unchanged. No agent
  is trained or modified.

## 9. Claim ceiling

At most: in one two-variable grid world, the recurrent state of regulators
whose objective is derived from their own body carries more linearly
decodable information about which variable was just fed, beyond their
current inputs, than that of regulators paid for the same regulation. Not:
that either kind of agent represents its body in any further sense, or
anything about larger systems.
