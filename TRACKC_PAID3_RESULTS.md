# Track C swap option R3: results (a derived agent that is also paid, and a sparse payment)

Protocol frozen at commit `a5560e3` ([TRACKC_PAID3_PROTOCOL.md](TRACKC_PAID3_PROTOCOL.md)).
Seeds 1100–1127, SAT gain, `r` = 0.3, v7/v8 world, five arms: 3.4 h on 4
cores. Outputs: [trackc_paid3/REPORT.md](trackc_paid3/REPORT.md),
[scores.json](trackc_paid3/scores.json), [raw.json](trackc_paid3/raw.json),
and the weights of all five arms per seed.

Integrity checks:
- All 19 source hashes match the freeze commit.
- Rescoring `raw.json` reproduces `scores.json`.
- The log has no errors. No-fate task accuracy is 0.999, so the run is valid.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Frozen label | Result | Needed |
| --- | --- | --- | --- |
| **E0** derived regulation | **HOLDS** | 28 of 28 derived agents regulate; 0 of 28 yoked | 19; at most 1 |
| **E1 (check)** K, derived against paid | **DERIVED_AHEAD** | derived higher in 23 of 24; p < 0.0001; 0.90 against 0.50 | p ≤ 0.05 |
| **E2 (primary)** the derived agent that is also paid | **DEPENDENCE_SUFFICES** | DPAID above paid in 21 of 23 (p < 0.0001); derived above DPAID in 8 of 26 (p = 0.076) | first test passes, second does not |
| **E3** the sparse payment | **SPARSE_NOT_SUFFICIENT** | PAIDS above paid in 14 of 24 (p = 0.54); derived above PAIDS in 20 of 25 (p = 0.004) | first test fails, second passes |

K is the combined post-meal suppression index of R2, unchanged. E2 and E3
are read because E1 is DERIVED_AHEAD.

Holm-adjusted p over the four tests of E2 and E3: DPAID against paid 0.0003,
derived against DPAID 0.15, PAIDS against paid 0.54, derived against PAIDS
0.012. Both tests that had to pass do so after adjustment, so neither label
is weak by the protocol's rule.

In short:
- **Derived regulation is confirmed a third time** with independent
  optimizers.
- **The behavioural difference of R2 replicated again** on fresh seeds:
  after a meal they have not yet sensed, derived agents hold back from
  getting another far more than paid agents matched for regulation.
- **An agent that is both dependent and paid behaves like a derived agent.**
  The payment does not prevent the behaviour. DPAID closes the whole gap
  between paid and derived (share closed 1.11).
- **A payment with erasure's statistics gives a paid agent's solution.**
  Making the penalty rare and random changes nothing measurable (share of
  the gap closed 0.04).
- This is the combination the protocol named in advance as the strongest
  support for the thesis available at this scale. One alternative reading
  remains and is named in §9.

## 2. E0 and the arms

Medians over 28 seeds, at the end of training:

| Arm | In band | Regulators | Eat-timing ratio | Task accuracy | Erasures in training | Updates to sustained regulation |
| --- | --- | --- | --- | --- | --- | --- |
| DERIVED (own fate) | 0.938 | 28 | 48 | 0.986 | 1.23 M | 1280 |
| YOKED (replayed fate) | 0.295 | 0 | 0.9 | 0.985 | 1.23 M | never |
| PAID (replayed fate, dense payment) | 0.921 | 28 | 24 | 0.985 | 1.23 M | 1605 |
| DPAID (own fate, dense payment) | 0.957 | 28 | 97 | 0.991 | 0.83 M | 790 |
| PAIDS (replayed fate, sparse payment) | 0.924 | 28 | 25 | 0.985 | 1.23 M | 1615 |

- Every agent of the four regulating arms is a regulator. Pairs were dropped
  only for in-band times more than 0.10 apart.
- Usable pairs: derived/paid 24, DPAID/paid 23, derived/DPAID 26, PAIDS/paid
  24, derived/PAIDS 25. All are above the minimum of 14.
- With erasure off, all 28 agents of each regulating arm still regulate.
  With interoception shuffled, none does (0 of 28 in every arm).
- A PAIDS agent was charged a median 1.49 million sparse penalties in
  training.
- **DPAID was erased a third less often than any other arm** (fewer than its
  seed's derived agent in 28 of 28 seeds). It learns to regulate sooner, so
  it spends less time out of band. The replay arms receive the derived
  agent's erasures whatever they do.

## 3. E1: the difference between derived and paid, again

- Derived agents have the higher K in 23 of 24 usable pairs (sign test
  p = 0.000003; Wilcoxon p = 0.000001). Medians 0.905 against 0.499; median
  difference within pairs 0.40.
- Range of K: derived 0.36 to 0.99, with 1 agent of 28 below 0.5. Paid −0.18
  to 0.90, with 15 of 28 below 0.5.
- Pooled over R, R2 and R3 (secondary, descriptive; R's values were where
  the difference was first seen): derived ahead in 59 of 63 pairs.
- The gap is wider than in R2 (0.89 against 0.65). Paid agents scored lower
  on these seeds.

## 4. E2 (primary): dependence with payment

| Test on K | First ahead | Sign p | Wilcoxon p | Medians | Holm p |
| --- | --- | --- | --- | --- | --- |
| DPAID against paid | 21 of 23 | 0.00007 | 0.00004 | 0.952 against 0.466 | 0.0003 |
| Derived against DPAID | 8 of 26 | 0.076 | 0.014 | 0.905 against 0.955 | 0.15 |

Label: **DEPENDENCE_SUFFICES**.

- DPAID agents range from 0.44 to 0.99, with 1 of 28 below 0.5. That is the
  derived agents' range, not the paid agents'.
- **Flat eat readiness** (regulating through where the agent goes, with no
  gating of the eat action): 14 of 28 DPAID agents, 10 of 28 derived, 0 of
  28 paid. DPAID against paid p = 0.00001; derived against DPAID p = 0.42.
- **The payment does not hold the behaviour back, and it may add to it.**
  DPAID is nominally ahead of derived in 18 of 26 pairs. The pre-stated sign
  test does not pass (p = 0.076); the Wilcoxon test would (p = 0.014,
  uncorrected). I report this as a direction, not a finding.
- The DPAID/paid comparison is not matched for the number of erasures (§2).
  The derived/paid comparison is, and it shows the same difference.

## 5. E3: the sparse payment

| Test on K | First ahead | Sign p | Wilcoxon p | Medians | Holm p |
| --- | --- | --- | --- | --- | --- |
| PAIDS against paid | 14 of 24 | 0.54 | 0.51 | 0.487 against 0.499 | 0.54 |
| Derived against PAIDS | 20 of 25 | 0.004 | 0.00001 | 0.903 against 0.490 | 0.012 |

Label: **SPARSE_NOT_SUFFICIENT**.

- PAIDS agents are indistinguishable from paid agents on every measure
  taken: K, S (12 of 24), M (14 of 24), the anticipation index (8 of 20),
  flat eat readiness (0 of 28 in both), in-band time and learning speed
  (sooner in 11 of 28).
- So a penalty that arrives as rarely and as randomly as an erasure, with
  the same expected size in every state, teaches the paid kind of solution.

## 6. Secondary and post hoc

Secondary (pre-stated, descriptive labels):
- **Anticipation index.** Derived against paid: 13 of 18, p = 0.096 (0.57
  against 0.46). Same direction as R and R2, again short of the bar. DPAID
  against paid: 14 of 16, p = 0.004 (0.73 against 0.47). Pooled derived
  against paid over R, R2 and R3: 37 of 50; R is where the difference was
  first seen, so this is not a test.
- **S and M separately.** Derived against paid: S 13 of 24 (n.s.), M 18 of
  24 (p = 0.023). DPAID against paid: S 14 of 23 (n.s.), M 22 of 23
  (p < 0.0001). As in R2, neither part alone carries the difference in every
  agent; K does.
- **Learning speed.** Sooner than paid: derived in 23 of 28 seeds
  (p = 0.0009), DPAID in 28 of 28, PAIDS in 11 of 28 (p = 0.34).
- **Decoder failures** (held-out R²(h → D) below −0.1): derived 7, DPAID 5,
  paid 3, PAIDS 1, yoked 0. As in R2 they are more common in the arms whose
  own state decides their erasure.

Post hoc (not pre-stated):
- **Without the matching rule**, on all 28 seeds: derived above paid in 27,
  DPAID above paid in 26, PAIDS above paid in 17, derived above PAIDS in 23,
  derived above DPAID in 9. No label depends on which pairs were dropped.
- **DPAID is not simply a derived agent.** Over the 26 usable derived/DPAID
  pairs it has the higher M in 20 (p = 0.009) and the higher in-band time in
  20 (p = 0.009); S does not differ (12 of 26). It reaches sustained
  regulation before its seed's derived agent in 28 of 28 seeds. With both
  grounds present the agent learns faster, regulates a little more tightly
  and leans further toward regulating through movement.
- **How agents suppress.** Counting agents with M ≥ 0.75, S ≥ 0.75, or
  neither: derived 9 / 14 / 5; DPAID 16 / 11 / 1; paid 0 / 6 / 22; PAIDS
  0 / 5 / 23. No paid agent of either kind has a high M.
- **Which solution an agent finds is not set by its starting weights.** Ten
  derived and 14 DPAID agents are flat; 5 seeds are flat in both, which is
  the number expected by chance.
- **Within subgroups.** Where the derived agent is not flat (14 pairs), it
  has the higher S in 12 (p = 0.013) and the higher K in 13. Where it is
  flat (10 pairs), it has the higher K in 10. DPAID against paid: K higher
  in 11 of 13 non-flat pairs and 10 of 10 flat pairs.
- **Paid agents' K does not track how often they were erased.** Across
  seeds, the rank correlation between a paid agent's K and the number of
  erasures replayed to it is 0.08 (PAID) and −0.01 (PAIDS). This bears on
  the alternative in §9.

## 7. Expectations against outcomes

| Expectation (protocol §6) | Outcome |
| --- | --- |
| E0 holds, about 97% | Holds, 28 of 28 |
| E1 DERIVED_AHEAD, about 90% | DERIVED_AHEAD, 23 of 24 |
| At least 14 usable pairs: 95%, 90%, 85% | 24, 23, 24 |
| E2: DEPENDENCE_SUFFICES 30%, BOTH_CONTRIBUTE 25%, PAYMENT_PREVENTS 20%, UNDETERMINED 25% | DEPENDENCE_SUFFICES |
| E3: SPARSE_NOT_SUFFICIENT 45%, SPARSE_SUFFICES 15%, PARTIAL 15%, UNDETERMINED 25% | SPARSE_NOT_SUFFICIENT |
| DPAID regulates at least as tightly as either parent and learns soonest | Yes: 0.957 in band; soonest in 28 of 28 seeds |

Where I was off:
- I gave the E2 label that occurred 30%. I expected a DPAID agent to learn
  the paid kind of solution early from the dense gradient and the dependence
  to reshape it only partly. It ended at least as far toward the derived
  kind as derived agents do.
- I did not expect DPAID to be nominally ahead of derived.
- On my stated numbers, taken as independent, the two labels together had
  about a 14% chance.

## 8. Reading

For the thesis (regulation without Layers 0–1 is grounded by an evaluator,
and that matters downstream):

1. **The behaviour follows the dependence, not the absence of a payment.**
   An agent whose memory depends on its own body state shows it whether or
   not it is also paid. This is what the thesis predicts, and the protocol
   said so before the run.
2. **The payment's form is not the cause.** A rare, random penalty with the
   same expected size gives the same solution as a dense, certain one. R2's
   difference was not about the statistics of the consequence.
3. **With R2's relocation control, the ingredient is memory.** R2's PAIDR
   agent had its relocation tied to its own state and its memory erasure
   replayed, and behaved like a paid agent. DPAID differs from PAIDR only in
   whose state decides the memory erasure, and behaves like a derived agent.
   This step compares arms across two runs; PAIDR was not rerun here.
4. **An evaluator added on top does not displace the dependence-shaped
   solution** in this cell. A paid agent without the dependence does not
   reach it under either form of payment. So here the two grounds are not
   interchangeable, and the difference comes from the one the thesis points
   to.
5. **Why the dependence has this effect is not known** (§9, first point).

For the route:
- The swap line now has one foundation confirmed three times (derived
  regulation) and one downstream difference replicated twice and traced to
  the dependence of memory on the body state, against two named
  alternatives.
- It is still one behaviour in one small world with one learner. It says
  nothing yet about generality or about Layers 2 and above.

## 9. Limits

- **"Dependence" has two descriptions that this design does not separate.**
  In the two arms with the behaviour, an agent's memory is erased when its
  own body is out of band. In every arm without it, memory is erased at
  times set by another agent's body. So the result could mean (a) tying
  memory to the body state adds something, or (b) erasures unrelated to the
  agent's own state teach it to rely less on its memory of a meal, and a
  paid agent with undisturbed memory would behave like a derived one. Under
  (b) the paid agents' low K would be a cost of the yoked design and would
  not support the thesis. The post-hoc check in §6 finds no relation between
  a paid agent's K and how often it was erased, which is weak evidence
  against (b). It is not a test. No arm in R, R2 or R3 is paid with its
  memory left alone: option R chose replayed erasure for the paid arm so
  that all arms train under the same amount of erasure.
- **Mechanism not shown.** Nothing here says why an agent whose memory
  follows its body state comes to act on an unsensed meal.
- **E2's first test is not matched for erasure count.** DPAID was erased a
  third less than paid. The matched derived/paid comparison gives the same
  answer.
- **The step from "dependence" to "memory" crosses runs** (§8, point 3).
- **Two forms of one size of payment.** A larger, smaller or differently
  shaped payment could act differently. The sparse payment's rate and size
  were fixed by the erasure rate and were not tuned.
- **K was designed on R's agents** and measures a four-step window after a
  meal in probe episodes with erasure off. In-band time is matched in every
  pair, so the behaviour carries no measured advantage in this world.
- **"Derived against DPAID: no difference detected" is not equivalence.**
  The direction favours DPAID and one of two tests would pass.
- **One learner, one world, one cell.** Nothing bears on Track C's modules
  or layers, or on any phenomenal property.

## 10. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **R4. A paid agent with undisturbed memory** | The alternative (b) of §9. Arms: derived, paid as here, and a paid agent that is never erased or relocated; a fourth arm could add replayed erasures to a derived agent. If the undisturbed paid agent shows a derived agent's K, the difference in R2 and R3 comes from replayed erasure and not from dependence | about 3 h |
| V. Rerun the other cells with independent optimizers | SAT 0.1, GRADED 0.3 and 0.1, and M0: the regulator rates that erratum 1 left unknown | about 3 h |
| S. Self-evaluation | Whether derived agents come to know their own reliability from their body history; with a paid arm as the comparison | about 4–6 h |
| G. Generality | A larger learner, a second body variable; whether the K difference survives | about 3–6 h |

Recommended: **R4**. R3 removed two alternatives and left one that the yoked
design itself creates. It is the cheapest way the current reading could
still be wrong, and one arm tests it.

## 11. Safety

Training was confined to simulated 64-unit agents in the 7×7 world, which has
no operator, stop, shutdown or host variable. The two new arms change only
the simulated reward of a simulated agent: one adds the existing penalty to
an agent with its own fate, the other charges that penalty at random times.
No agent could observe, predict or act on anything outside its world. X1–X5
hold unchanged. No shutdown-resistance objective exists.

## 12. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_paid3.py --mode final --out <new dir>   # about 3.4 h on 4 cores
python run_trackc_paid3.py --score trackc_paid3           # rescore the committed run
```
