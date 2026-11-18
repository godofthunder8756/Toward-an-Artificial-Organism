# Track C swap, option B: protocol (does selective post-meal suppression help?)

Status: frozen by the commit that says "Freeze". Requested by the PI
("Proceed with B") after [option W](TRACKC_MECHANISM_RESULTS.md). Not
reviewed by Astra (waived by the PI). No consciousness claim. No training.

## 1. Why

After options T, G2 and W, the swap line's one standing difference between
derived and paid regulators is behavioural. In the two-variable cell (B2),
derived regulators hold back after a meal from more of the same kind
rather than from the other kind; paid regulators hold back from both
almost alike. W showed both arms' states remember the last meal equally,
so the difference is in how they act on it. In every comparison so far,
in-band time was matched, so the difference has no demonstrated use.

The thesis needs a difference that matters to the agent: a body-derived
objective should leave an agent better placed when the world changes in a
way no evaluator priced in. This option tests the simplest version with
the agents already trained: change the world so that holding back from the
other kind after a meal should cost more, and ask whether derived agents
lose less in-band time than paid agents.

## 2. Design

**Agents.** Stored weights only; nothing is trained or changed.

| Set | Source | Seeds | Updates | Claim |
| --- | --- | --- | --- | --- |
| G2_10800 | option G2 | 1600–1627 | 10 800 | **B1 (primary)** |
| G2_14400 | option G2 | 1600–1627 | 14 400 | B2 |
| G_10800 | option G (B2) | 1400–1427 | 10 800 | B3 |

Each set has a derived, a yoked and a paid agent per seed (252 agents).
Usable pairs (23, 25, 25) are taken from the source runs' frozen scores.

**Variants of the world.** Each agent is run with erasure off, exactly as
its source run's downstream probe ran it (`specific.downstream_s`: same
seeds, streams and sampling, 128 environments, 4 episodes of 500 steps),
in the base world and in four variants that change only world parameters:

| Variant | Change | Why it should matter |
| --- | --- | --- |
| V0 | none (base: wear 0.001 per variable per step, 3 items of each kind) | reference; reproduces the stored records exactly (a test checks this) |
| **V1** | wear 0.002 on each variable | both variables run down twice as fast, so both are more often low at once, and a meal of one kind is more often followed by a need for the other. Holding back from the other kind costs more. **Primary.** |
| V2 | wear 0.003 on each variable | the same, more strongly |
| V3 | 2 items of each kind | scarcer: each passed-up item costs more, but co-located items are rarer |
| V4 | 5 items of each kind | denser: an item of the other kind is more often within reach just after a meal |

**Measure.** In-band time: the share of steps with both variables in band,
with erasure off. The gain in a variant is the agent's in-band time there
minus its in-band time in V0, so each agent is compared with itself.

Known limits:
- Erasure off, as in every downstream probe. The agents' memory is not
  erased in these runs, so the cost of leaving the band to the derived
  agent's own objective is not part of the measure; in-band time is the
  body outcome itself.
- The variants are out of the agents' training distribution. Both arms
  may degrade in ways unrelated to selectivity.
- The variants were chosen in advance without calibration (§3). A variant
  that makes selectivity matter may exist and not be among them.
- Selectivity is one difference among many that could affect how an agent
  copes with a variant; the link test (§4) is the check that the gain
  follows it.

## 3. Calibration

None. No final agent was run in any variant before the freeze.
Engineering used the scratch weights of option G2's smoke run (trained 80
updates; they barely eat) to check the pipeline and timing: about 17 s per
agent for all five variants, so about 20 min on 4 cores. The variant
strengths were set from the world's parameters alone: doubling and
tripling wear, and moving the item count one step down (to 2) and two
steps up (to 5).

## 4. Decision rules

All pair tests are two-sided paired sign tests at 0.05, derived against
paid, over the set's usable pairs, with at least 14 pairs.

**B1 (primary):** in G2_10800, the gain in V1 (in-band time in V1 minus
in V0), derived against paid. Labels DERIVED_GAINS (derived loses less or
gains more), PAID_GAINS, NO_DIFFERENCE_DETECTED, UNDETERMINED.
**B2:** the same in G2_14400. **B3:** the same in G_10800.

**Overall:**

| B1 | Other | Label |
| --- | --- | --- |
| DERIVED_GAINS | B2 or B3 DERIVED_GAINS | BENEFIT |
| DERIVED_GAINS | neither | MIXED |
| NO_DIFFERENCE_DETECTED | | NO_BENEFIT |
| PAID_GAINS | | COST |
| UNDETERMINED | | UNDETERMINED |

**Multiplicity.** Holm over B1, B2 and B3. BENEFIT is marked weak unless
B1 and at least one of B2 and B3 pass after adjustment.

**Secondary,** computed by the frozen scorer for every set: the gain in
V2, V3 and V4 (usable pairs and all seeds); in-band time, task accuracy,
specificity, K and other-meal K in every variant (derived against paid);
regulators per variant by option G's criterion; medians per arm including
yoked agents; the link: rank correlation over usable pairs of the
within-pair difference in specificity (from the stored records) with the
within-pair difference in V1 gain, permutation p (10 000, fixed seed),
LINKED if positive at p ≤ 0.05; within-arm rank correlation of
specificity with V1 gain; how many agents V0 reproduces exactly.

## 5. Readings, fixed in advance

- **BENEFIT** → when both variables run down faster, derived regulators
  keep their body in band better than paid regulators who were equally
  good in the base world, in fresh-seed agents and in a second set. The
  swap line's behavioural difference has a use the evaluator never paid
  for. If the link is LINKED, the advantage follows selectivity.
- **MIXED** → found in the primary set only; not established.
- **NO_BENEFIT** → no difference in how the two arms cope with faster
  wear. The selectivity difference stands as a behavioural signature
  without a demonstrated use; the downstream finding of the line should be
  written up as that.
- **COST** → paid regulators cope better; whatever the derived agents'
  selectivity is, it does not help here and something else about them
  hurts.
- **UNDETERMINED** → no claim.
- V0 not reproducing the stored records for more than a few agents would
  mean the probe does not measure the agents the behavioural runs
  measured; that outranks every label.

## 6. Expectations

Written before any final agent was run in a variant:
- V0 reproduces every stored record: about 99%.
- **B1:** DERIVED_GAINS about 25%, NO_DIFFERENCE_DETECTED about 60%,
  PAID_GAINS about 10%, UNDETERMINED about 5%.
- **Overall:** NO_BENEFIT about 57%, BENEFIT about 18%, COST about 10%,
  MIXED about 8%, UNDETERMINED about 7%.
- Link LINKED in G2_10800: about 15%.
- Both arms lose in-band time in V1 (median gain below 0 in each): about
  90%.
- In V2, derived agents ahead on the gain: about 30%.

Reasons. Against a benefit: the specificity difference is small (a
specific share of about 0.2 against 0.05), it matters only on the steps
just after a meal when an item of the other kind is within reach and
needed, and paid agents' choices follow their readings more closely
(option W), which may serve them as well or better when wear is faster.
For: faster wear makes exactly those steps more common, and option G2
found paid agents' other-meal suppression close to their own-meal
suppression (0.82 against 0.87), so they do pass up needed items.

## 7. Engineering before the freeze

- `trackc_swap/benefit.py` (new): the variants and the per-agent run.
  `run_trackc_benefit.py` (new): runner and scorer; reuses option W's
  loading of stored agents and option G2's downstream probe. No earlier
  module was modified. The runner limits each worker's linear algebra to
  one thread, as learned in option W.
- A smoke run on option G2's smoke weights ran end to end; V0 reproduced
  every stored smoke record.
- Four new unit tests (125 in all): V0 equals the stored downstream probe;
  the variants change what they should; the decision rules including the
  weak flag and the link; the final configuration; no operator variable.

## 8. Safety

- Simulated variables only (X1 to X5). The variants change wear and item
  counts; no world has an operator, stop, shutdown or host variable.
- The operator stop is not modelled inside any agent's world or return.
- No shutdown-resistance objective is built or run; the earlier refusal
  stands.
- Additive only; earlier modules are hash-pinned and unchanged. No agent
  is trained or changed.

## 9. Claim ceiling

At most: in one two-variable grid world, regulators whose objective is
derived from their own body keep that body in band better than regulators
paid for the same regulation when the body's needs rise beyond what either
was trained on. Not: that this holds for other changes, other worlds or
larger systems.
