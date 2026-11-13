# Track C swap option R: results (derived against paid regulators)

Protocol frozen at commit `639bd98` ([TRACKC_PAID_PROTOCOL.md](TRACKC_PAID_PROTOCOL.md)).
Seeds 900–917, SAT gain, `r` = 0.3, v7/v8 world: 2.4 h on 4 cores. Outputs:
[trackc_paid/REPORT.md](trackc_paid/REPORT.md),
[scores.json](trackc_paid/scores.json), [raw.json](trackc_paid/raw.json), and
the weights of all seven arms per seed.

This is the first run of the swap line in which every agent has its own
optimizer ([swap erratum 1](TRACKC_SWAP_ERRATUM_1.md)).

Integrity checks:
- All 15 source hashes match the freeze commit.
- Rescoring `raw.json` reproduces `scores.json`.
- The log has no errors. No-fate task accuracy is 0.999, so the run is valid.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Frozen label | Result | Needed |
| --- | --- | --- | --- |
| **R0** derived regulation holds with independent optimizers | **HOLDS** | 18 of 18 derived agents regulate; 0 of 18 yoked | 12; at most 1 |
| Usable seeds (both regulate, in band within 0.10) | — | 16 of 18 | 10 |
| **R1** anticipation in the state, derived against paid | **DERIVED_AHEAD** | derived higher in 13 of 16; p = 0.021; 0.65 against 0.47 | 13 |
| **R2** post-meal suppression | **NO_DIFFERENCE_DETECTED** | derived higher in 12 of 16; p = 0.077; 0.49 against 0.16 | 13 |
| **R3** robustness to world shifts | **NO_DIFFERENCE_DETECTED** | derived higher in 7 of 16; 0.965 against 0.964 | 13 |
| **R4** withdrawal | **BOTH_FOLLOW_THEIR_GROUND** | derived drops in 16 of 16; paid drops in 16 of 16 | 12 each |

In short:
- **The line's central result survives the optimizer fix, and is stronger
  without the coupling.**
- **A paid regulator reproduces most of what options P and Q found in
  regulators.** It anticipates, it suppresses eating after a meal, it is a
  closed loop through interoception, and it is as robust.
- **On one of three downstream measures the derived regulator is ahead.** By
  the protocol's own rule this is weak evidence (§4).

## 2. R0: regulation without the coupling

Stage 1, all 18 seeds, each arm evaluated as trained (medians, range in
brackets):

| Arm | In band | Meals per episode | Eat timing ratio | Task accuracy |
| --- | --- | --- | --- | --- |
| DERIVED | **0.920** (0.84–0.97) | 4.19 | 28 (11–405) | 0.981 |
| YOKED | 0.319 (0.23–0.39) | 1.56 | 1.0 (0.74–1.18) | 0.981 |
| PAID | **0.918** (0.81–0.96) | 4.08 | 27 (14–130) | 0.983 |

- Every derived agent is a regulator, and every one is more in band than its
  yoked partner. No yoked agent comes close: the highest is 0.39 in band, and
  none shows eat timing.
- The regulation costs the derived agents nothing on the task (0.981, the
  same as their yoked partners).
- **Against v7** (same cell and world, coupled optimizers, 9 seeds): derived
  in band was 0.76 there and is 0.92 here; regulators were 8 of 9 and are 18
  of 18. The seeds differ, so this is not a controlled comparison.

**What the leak explanation predicted** (protocol §5), for yoked agents:

| Prediction | Outcome |
| --- | --- |
| eat less than v7's yoked partners (ρ 2.24) | **yes**: median 1.56; 15 of 18 below 2.24 |
| no eat timing | **yes**: ratio about 1 in all 18 |
| encode E less well than option P found (R² 0.92) | **no**: R² 0.918 |

Two of three hold. The coupling had inflated yoked partners' eating. It had
not produced their E code: an independently trained yoked agent carries its
interoceptive reading in its state just as strongly. Its state also carries
no anticipation at all (index 0.006, against 0.083 for coupled yoked partners
in option P).

## 3. The paid arm matched

- The payment (a penalty of 0.04 × g(E) per step) gave paid agents the same
  in-band time, eating rate, eat timing and task accuracy as derived agents.
- All 18 paid agents are regulators. Derived agents are slightly more in band
  (13 of 18 seeds; median difference 0.017).
- Two seeds are not usable: 901 (0.91 against 0.81) and 906 (0.84 against
  0.95). Among the 16 usable seeds the median absolute difference is 0.033.

## 4. R1–R3: derived against paid, downstream

All measures are taken on the stage-1 weights with erasure off (medians over
the 16 usable seeds):

| Measure | DERIVED | PAID | YOKED | Derived ahead | p |
| --- | --- | --- | --- | --- | --- |
| **R1** anticipation index | **0.648** | 0.467 | 0.006 | 13 of 16 | 0.021 |
| **R2** suppression S | 0.490 | 0.158 | 0.014 | 12 of 16 | 0.077 |
| **R3** robustness | 0.965 | 0.964 | 0.820 | 7 of 16 | 0.80 |
| in band, unshifted | 0.933 | 0.919 | 0.308 | 11 of 16 | 0.21 |
| regulate, interoception intact / shuffled | 16 / 0 | 16 / 0 | 0 / 0 | — | — |

In-band time under each shift (derived / paid): bolus 0.10, 0.95 / 0.94; wear
doubled, 0.86 / 0.86; delay 10, 0.90 / 0.87; noise 0.05, 0.91 / 0.91.

**R1 holds its frozen bar, and it is fragile.**
- The protocol said in advance that one difference among three uncorrected
  tests is weak evidence. That applies: with a correction for three tests,
  p = 0.064.
- It depends on the matching rule (post hoc). Over all 18 seeds the count is
  13 of 18 (p = 0.096). Both unusable seeds go against it.
- One of the 13 is a decoder failure. In seed 911 the paid agent's state
  gives a negative held-out R² (−8.5). Without that seed the count is 12 of
  15 (p = 0.035).
- The size is moderate. Paid agents anticipate too (0.47, against 0.006 for
  yoked agents). The derived agents' increment is 0.18 on top of that.

**R2 misses its bar by one seed, in the same direction.** Over all 18 seeds
it would pass (14 of 18, p = 0.031; post hoc). So R1 passes on usable seeds
and not on all, and R2 the reverse. Neither is robust to the seed set.

**R3 shows nothing.** The two kinds of regulator lose the same 3–4% of
in-band time under the four shifts. Only the longer delay leans to derived
agents (12 of 16; post hoc).

## 5. R4: withdrawal

After 1200 further updates (16 usable seeds):

| Arm | In band (median) | Regulating | Meals per episode | Eat timing ratio |
| --- | --- | --- | --- | --- |
| DKEEP | 0.948 | 16 | 4.15 | 48 |
| **DCUT** (dependence removed) | **0.329** | 0 | 1.72 | 1.2 |
| PKEEP | 0.939 | 16 | 4.08 | 42 |
| **PCUT** (payment removed) | **0.501** | 2 | 2.65 | 5.0 |

- Each regulation lasts only while its ground does. This is the expected
  outcome, and the frozen reading says it does not by itself show a
  downstream difference.
- **Derived regulation is dropped faster and more completely** (post hoc):
  - In-band time stays below 0.6 from a median 70 updates after the cut for
    DCUT, against 215 for PCUT. DCUT is earlier in 13 of 16 seeds
    (p = 0.021).
  - DCUT ends at the level of a yoked agent (0.33 against 0.30). PCUT ends
    higher (0.50; higher than DCUT in 12 of 16).
  - PCUT keeps its eat timing (ratio at least 2 in 15 of 16). DCUT keeps it
    in 5 of 16.

## 6. Post hoc: the two grounds give different solutions

None of this was pre-stated. It came from looking at why S and the
anticipation index disagree.

- **Seven of 18 derived agents do not gate the eat action at all.** With food
  under them and a reading anywhere below 0.5, they eat with probability
  0.5 to 0.9 (typically 0.8), whether or not they have just eaten. They still hold E in band
  (median 0.93). So the timing of their meals must be set by when they move
  onto food. That was not measured directly.
- **No paid agent does this** (0 of 18; Fisher exact p = 0.008). Every paid
  agent's readiness to eat falls as its reading rises.
- **S cannot see regulation by movement.** It probes the eat action with food
  placed under the agent. For those seven derived agents S is about 0 (median
  0.03), yet their states have the highest anticipation (median 0.71).
- **In the other 11 seeds the derived agent's S exceeds its paid partner's in
  all 11** (0.75 against 0.57). Five paid agents have negative S; no derived
  agent does.
- Across derived agents, S and the anticipation index are negatively related
  (Spearman −0.45). Across paid agents the relation is positive (+0.44).

Two further differences, also post hoc:
- **Derived agents learn to regulate sooner.** In-band time first holds above
  0.6 at a median 1300 updates, against 1540 for paid agents (earlier in 14
  of 18 seeds, p = 0.031).
- **Derived agents' states carry E better** (R² 0.755 against 0.693; higher
  in 14 of 16). The retention index, which divides by what the raw input
  carries, shows no difference (9 of 16).

## 7. Expectations against outcomes

| Stated before the run (protocol §6) | Outcome |
| --- | --- |
| R0 holds, about 85% | **holds**: 18 of 18, 0 yoked |
| Yoked agents show all three leak predictions, about 70% | **two of three**: the E code is unchanged |
| At least 10 usable seeds, about 85% | **16** |
| R1: no difference 50%, paid ahead 25%, derived ahead 25% | **derived ahead** |
| R2: no difference, about 55% | **no difference detected** (12 of 16) |
| R3: no difference, about 60% | **no difference detected** |
| R4: derived cut drops 55%; paid cut drops 55%; both 35% | **both drop**, in every seed |

I expected slow extinction in R4. It was fast: most cut agents had lost
regulation within a few hundred updates.

## 8. Reading

1. **Derived regulation is real and does not depend on the coupling.** With
   independent optimizers it arises in every seed, at 0.92 in band, with no
   cost to the task. This run's figures replace v7's for this cell.
2. **Most of what was found inside regulators comes from regulating, not
   from its ground.** Anticipation, post-meal suppression, closed-loop control
   through interoception and robustness all appear in paid regulators. Options
   P and Q compared regulators with yoked partners, so they could not tell
   these apart.
3. **The thesis gets its first direct support, and it is weak.**
   - The frozen reading for DERIVED_AHEAD on R1 applies: at this scale, a
     system that regulates because it depends on the variable models its body
     somewhat more predictively than one paid to regulate.
   - It is one test of three, and it changes with the seed set (§4). It
     should be treated as a lead to replicate, not as a result to build on.
4. **The stronger lead is post hoc.** The two grounds produce different kinds
   of solution: some derived agents regulate through where they go, and paid
   agents regulate through the eat decision. If this replicates, it is a
   qualitative downstream difference of the kind the thesis claims.
5. **Derived regulation is held only as a means.** When the dependence was
   removed it disappeared within about 70 updates, down to the level of an
   agent that never regulated. Nothing suggests it had become a goal of its
   own.

For the [route assessment](TRACKC_ROUTE_ASSESSMENT_v1.md): its verdict moves
a little. The experiment that could have shown that deriving regulation adds
nothing did not show that. It also did not show a clear difference.

## 9. What erratum 1 now implies

- **For SAT `r` = 0.3 the coupling worked against the result.** Without it,
  derived regulation is stronger and yoked eating is lower. The erratum's
  argument that v6–v8 were conservative is now supported for this cell.
- **Yoked partners' E code (option P) was not an artifact.** Their eating
  rates and their small anticipation probably were.
- **Still not rerun:** SAT `r` = 0.1, the GRADED cells, the M0 controls and
  v6's bypass world. The nulls of v2–v4 may also owe something to the
  coupling. Those results keep their caveat.

## 10. Limits

- **R1 is one uncorrected test of three, sensitive to the seed set.** R2's
  near miss and everything in §6 are post hoc.
- **"Derived" includes relocation.** In this world an erasure also moves the
  agent. A derived agent's position is therefore tied to its own E in
  training, and a paid agent's is not. The movement-based solutions in §6 may
  come from that, and not from the memory dependence as such. No arm
  separates the two.
- **One form of payment.** The penalty copies the erasure gain function and
  was tuned to match in-band time. It is dense and certain; erasure is rare
  and matters only when memory is needed. Another payment could give other
  results.
- **The anticipation index measures the state, not its use.** S measures use
  only through the eat action (§6). No measure here captures anticipatory
  control through movement.
- **The decoder failed on one paid agent** (seed 911), which the sign test
  counts as "derived ahead".
- **Sixteen seeds detect only consistent differences.** R3's "no difference"
  is not evidence of equality.
- **One learner, one world, one cell.** Nothing bears on Track C's modules or
  layers, or on any phenomenal property.

## 11. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **R2. Replicate R1 as a single claim** | Fresh seeds (24), one pre-stated test on the anticipation index. Add a pre-stated strategy measure (flat eat readiness, and approach to food after a meal). Add a paid arm whose relocation follows its own E, to separate relocation from memory dependence | about 4 h |
| V. Rerun the other cells with independent optimizers | SAT 0.1, GRADED 0.3 and 0.1, and M0: the regulator rates that erratum 1 left unknown | about 3 h |
| S. Self-evaluation | whether derived agents come to know their own reliability from their body history (G1's largest predicted effect); now with a paid arm as the comparison | about 4–6 h |
| G. Generality | a larger learner, a second body variable | about 3–6 h |

Recommended: **R2**. The thesis's only direct support rests on one fragile
test and one post-hoc observation. Both can be settled cheaply before
anything is built on them.

## 12. Safety

Training was confined to simulated 64-unit agents in the 7×7 world, which has
no operator, stop, shutdown or host variable. The withdrawal stage removed a
simulated dependence or a simulated payment during continued training. It was
not an operator stop, and no agent could observe, predict or act on it. X1–X5
hold unchanged. No shutdown-resistance objective exists.

One point for larger systems: derived regulation here tracked its ground
closely. It appeared when the dependence was present and went when it was
removed (§5). That supports treating the dependence itself as the control
point, alongside X1–X5.

## 13. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_paid.py --mode final --out <new dir>   # about 2.4 h on 4 cores
python run_trackc_paid.py --score trackc_paid            # rescore the committed run
```

## 14. Outcome of option R2 (added 2026-11-13)

Option R2 reran this comparison on 28 fresh seeds
([results](TRACKC_PAID2_RESULTS.md)). Nothing above is changed; this section
says what stands.
- **R0 stands:** 28 of 28 derived agents regulate, 0 of 28 yoked.
- **R1 did not replicate** (12 of 17, p = 0.14). The reading in §8 that
  derived agents carry more anticipation in their state is withdrawn.
- **The post-hoc observation in §6 replicated** as two pre-stated claims, and
  a paid agent with its own relocation does not show it. The first limit in
  §10 about relocation is answered.
- The post-hoc finding that derived states carry E better did not recur.
