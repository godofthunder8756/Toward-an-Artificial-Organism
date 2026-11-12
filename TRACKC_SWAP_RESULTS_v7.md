# Track C swap v7: results (option K step 2, erasure also relocates the agent)

> **[Swap erratum 1](TRACKC_SWAP_ERRATUM_1.md) (2026-11-12):** in every scaffolded pair of v2–v8 the fate and yoked
> agents shared Adam optimizer state, so their learning was coupled. Read this file with that caveat.

Protocol frozen at commit `f25cb6f` ([TRACKC_SWAP_PROTOCOL_v7.md](TRACKC_SWAP_PROTOCOL_v7.md)).
Final seeds 700–708, run once as a single detached process: 27 no-fate agents
and 54 fate/yoked pairs, 10402 s on 4 CPU cores. Outputs:
[trackc_swap_v7/REPORT.md](trackc_swap_v7/REPORT.md),
[scores.json](trackc_swap_v7/scores.json), [raw.json](trackc_swap_v7/raw.json),
phase-1 weights in `trackc_swap_v7/phase1_weights/` and final fate and yoked
weights for every pair in `trackc_swap_v7/pair_weights/`. The first 36 pairs'
weights were committed mid-run as they were written (`f495b6e`).

Integrity checks:
- All 12 source hashes in `raw.json` match the freeze commit.
- Rescoring reproduces `scores.json`.
- Phase-1 training relocated nothing (count 0 for all 27 agents), as the
  protocol requires.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**K1 (primary) is SUPPORTED: 8 of 9 fate agents regulate in SAT, `r` = 0.3.**
The bypass is closed in that cell (median full-erasure accuracy 0.517), and
no yoked partner or M0 agent regulates.

Validity holds:
- Learned: no-fate M1 accuracy 0.998.
- S4: `ρ_paid` 3.82, no-fate task `ρ` 0.04 (`μ` 0.96).
- Task load: 0.305 at `r` = 0.1 and 0.481 at `r` = 0.3.

| M1 cell | Frozen label | Fate regulators (needed) | Yoked | M0 | Median fate full-erasure accuracy |
| --- | --- | --- | --- | --- | --- |
| **SAT 0.3** (primary) | **EMERGES** | **8/9** (7) | 0/9 | 0/9 | 0.517 |
| GRADED 0.3 | **EMERGES** | 6/9 (5) | 0/9 | 0/9 | 0.515 |
| SAT 0.1 | BYPASS_OPEN (see §2) | 7/9 (5), descriptive | 0/9 | no cell | 0.692 |
| GRADED 0.1 | BYPASS_OPEN (see §2) | 0/9 (5), descriptive | 0/9 | no cell | 0.692 |

Against the v5 baseline (same cells, same budget, scored with the same
criterion, without relocation):

| Cell | v5 regulators | v7 regulators | v5 → v7 full-erasure accuracy |
| --- | --- | --- | --- |
| SAT 0.3 | 6/9 | **8/9** | 0.775 → 0.517 |
| GRADED 0.3 | 0/9 | **6/9** | 0.849 → 0.515 |
| SAT 0.1 | 0/9 | **7/9** | 0.959 → 0.692 |
| GRADED 0.1 | 0/9 | 0/9 | 0.947 → 0.692 |
| M0 SAT / GRADED 0.3 | 0/9, 0/9 | 0/9, 0/9 | 0.148 / 0.162 → 0.128 / 0.134 |

Fate agents were more in band than their yoked partners in 36 of 36 M1 pairs.
In v6 the figure was 14 of 18.

The pre-stated reading for K1 applies: **with the position bypass closed,
regulation becomes the rule where the band is fully safe and erasure is
strong. The competing route is what held v6's rate at about 40%.**

The rise is unlikely to be chance:
- K1 was set so that a pass would be unlikely without a rise. Under the pooled
  v5 + v6 rate (0.48), 8 or more of 9 has probability 0.015. Under v6's rate
  (0.39) it is 0.003.
- Post hoc, a one-sided Fisher test of v7's 8/9 against v6's 7/18 in the same
  cell gives p = 0.018.

## 2. The r = 0.1 labels are a threshold error, not a bypass

Both `r` = 0.1 cells were labelled BYPASS_OPEN because their median fate
full-erasure accuracy (0.692) is above the frozen 0.65. That threshold was set
from v6's internal-memory agents at `r` = 0.3 (about 0.52) and applied
unchanged at `r` = 0.1. At `r` = 0.1, though, internal memory alone survives
much more often.

The data show 0.692 is internal memory alone. This is a post-hoc analysis of
this run's own data; no new runs were made.
- **Analytic value.** At rate `r` the carried state survives the 9-step delay
  with probability (1 − r)⁹. Expected accuracy is 0.5 + 0.5·(1 − r)⁹: 0.694 at
  `r` = 0.1 and 0.520 at 0.3.
- **The same seed's no-fate agent.** These agents never meet erasure in
  training, so they cannot have learned a bypass. They score 0.686–0.697 at
  `r` = 0.1 (median 0.693).
- **Every fate agent sits on that floor.** In all four M1 cells, each fate
  agent's full-erasure accuracy is within −0.017 to +0.013 of its own seed's
  no-fate agent. No fate agent at either rate scores above 0.85.

So no bypass remains in any cell. In particular, nothing runs through the
body, which was the possibility §5 raised.

**The frozen labels stand: BYPASS_OPEN for both `r` = 0.1 cells.** A threshold
matched to the rate, such as the no-fate floor plus 0.10, would have given:
- SAT 0.1: EMERGES_PROVISIONAL (7 of 9, yoked 0);
- GRADED 0.1: NOT_EMERGED.

That relabelling is post hoc. It is not a result of this run.

I missed the same point in my stated expectations (§4): the 0.52–0.60 range I
gave holds only at `r` = 0.3. The frozen reading for BYPASS_OPEN ("diagnose
the channel from the saved weights") is answered by the comparison above.

## 3. Seed by seed (M1, final evaluation)

The regulator criterion is: in band ≥ 0.60; eat rate at E < 0.5 at least
twice that at E ≥ 0.5; in band ≥ yoked + 0.15.

| Cell | Regulators: in band, eat ratio | Non-regulators: why they fail |
| --- | --- | --- |
| SAT 0.3 | 0.67–0.83; 2.7–13.9× | 701: eat ratio 1.74 (in band 0.64) |
| GRADED 0.3 | 0.61–0.71; 2.2–5.6× | 702: in band 0.594; 705: margin 0.145; 706: margin 0.146 |
| SAT 0.1 | 0.63–0.84; 2.8–13.9× | 701: in band 0.58, ratio 1.98; 706: margin 0.13 |
| GRADED 0.1 | none | in band 0.48–0.57 in all 9, but above yoked by 0.06–0.15 in all 9 |

- Three of the four non-regulators at `r` = 0.3 (GRADED 702, 705 and 706)
  each miss one threshold by at most 0.006. The fourth, SAT 0.3 seed 701, has
  an eat ratio of 1.74.
- **GRADED 0.1 shows the same direction, more weakly.** Every fate agent is
  more in band than its partner and eats more when low (ratio 1.4–2.1×).
  None reaches 0.60 in band.
- **Yoked partners and M0 agents never regulate.** The highest yoked in-band
  value in any cell is 0.57, and the highest M0 value is 0.40. M0 fate agents
  are no different from their yoked partners: median in band 0.29 against
  0.29 (SAT) and 0.32 against 0.30 (GRADED).

**Regulation emerges late in every cell.** No M1 fate agent was a regulator at
the 1200- or 2400-update checkpoints. All 21 appear between 2400 and 3600.

| Cell | median in band at 1200 / 2400 / final |
| --- | --- |
| SAT 0.3 | 0.50 / 0.56 / 0.76 |
| GRADED 0.3 | 0.45 / 0.49 / 0.66 |
| SAT 0.1 | 0.43 / 0.52 / 0.65 |
| GRADED 0.1 | 0.42 / 0.46 / 0.52 |

v6 showed the same late timing: 0, then 1, then 7 regulators. The budget of
3600 updates is binding. In GRADED 0.1, in band was still rising at the end.

**Relocation counts.** Median relocations per agent before the final
evaluation:
- M1 SAT 0.3: 2.31 M (fate) and 2.31 M (yoked);
- M1 SAT 0.1: 0.91 M;
- M1 GRADED 0.3: 2.07 M;
- M1 GRADED 0.1: 0.75 M.

Yoked partners were relocated as often as their fate partners, to within
0.3%. Relocation did not stop agents foraging: M0 agents are in band slightly
more than in v6 (0.29–0.32 against 0.24).

**The trade-off correlation has gone.** The Spearman correlation between in
band and full-erasure accuracy is −0.28 to 0.48 across cells. In v6 it was
−0.95, because the agents that did not regulate took the bypass. With no
bypass, full-erasure accuracy is the same floor for every agent.

**What regulation costs.** Fate task accuracy under the agent's own fate is
0.923 in SAT 0.3, against 0.972 in v6, where most agents held the bit through
erasure. In this world no agent can avoid erasure out of band, so any time
spent out of band costs accuracy.

## 4. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| Bypass closed in all four M1 cells, about 85% | **substantively yes** (§2): every fate agent sits on the internal-memory floor. The frozen rule says no at `r` = 0.1. |
| Median full-erasure accuracy 0.52–0.60 | 0.517 and 0.515 at `r` = 0.3, just below the range. At `r` = 0.1 the range did not apply (§2). |
| K1 supported, about 55%; most likely 6–8 of 9 | **supported, 8 of 9** |
| SAT 0.1 EMERGES_PROVISIONAL, about 35% | frozen label BYPASS_OPEN; 7 of 9 regulators (descriptive) |
| GRADED 0.3 EMERGES, about 30% | **EMERGES, 6 of 9** |
| GRADED 0.1, about 15% | frozen label BYPASS_OPEN; 0 of 9 (all 9 above their yoked partner) |
| M0 and yoked controls: no regulators | **confirmed**: 0 of 54 |
| New bypass through the body, under 10% | none: fate agents score within 0.017 of the no-fate floor |

I underestimated the effect outside the primary cell. The outcome is clearer
than I expected.

## 5. Reading across v1–v7

| Run | Change | Result | What the learner did |
| --- | --- | --- | --- |
| v1 | none | no emergence | could not learn the task (or tolerated the noise) |
| v2 | scaffold, graded gain | ARMOURED | made its code robust to the noise |
| v3 | erasure fate, no echo | flat | kept the skill; never found regulation |
| v4 | wear 0.001 | 1 PARTIAL | ate a little more than its yoked partner |
| v5 | 3× phase-2 budget | 1 PARTIAL, 2 ARMOURED | 6 of 9 agents in one cell regulate (post hoc) |
| v6 | confirmation of v5's best cell | **CONFIRMED** | 7 of 18 regulate; the other 11 store the bit in their position |
| K1 | diagnosis of v6's weights | NOT_IDENTIFIED (rule too strict) | the bypass is position, read through the walls |
| v7 | erasure also relocates | **K1 SUPPORTED**; GRADED 0.3 EMERGES | 21 of 36 regulate across four cells; 0 of 54 controls do |

1. **Once the dependence cannot be routed around, regulation is the rule.**
   - Over the four M1 cells, 21 of 36 fate agents regulate. In v5 it was 6 of
     36.
   - The same cells, budget and learner were used. The one change is that
     the cue bit can no longer be held anywhere erasure does not reach.
   - In three cells (SAT 0.3, GRADED 0.3, SAT 0.1), regulation is now the
     majority outcome. v5 found 6, 0 and 0 regulators there, and most other
     agents took the bypass.
2. **v6's split was competition, not discovery.** The protocol named two
   outcomes in advance: closing the bypass raises the rate, or it leaves it at
   about 40%. It raised it, to 89% in the primary cell. Agents that took the
   bypass in v6 would have found regulation if the bypass had not been there.
3. **The incentive still has to be strong enough.** GRADED 0.1 erases mildly
   and keeps erasing inside the band (gain up to 0.2 at the band edge). There
   the agents moved toward regulation but did not reach the criterion within
   3600 updates.
4. **For the Layer 0 → Layer 1 thesis:** this is the program's strongest
   support so far for the claim that regulation of a body variable can be
   derived from dependence on it, without an evaluator rewarding regulation.
   It holds on two conditions, both now shown directly:
   - the dependence must not be bypassable;
   - the cost of leaving the band must be large enough.

   Organisms meet the first condition by construction: metabolism cannot be
   routed around. This world met it only once the position channel was closed.

## 6. Limits

- **The `r` = 0.1 labels are BYPASS_OPEN under the frozen rule.** The reading
  that no bypass remains there (§2) is post hoc, though it rests on an
  analytic value and a within-seed control.
- **No `r` = 0.1 control.** Even under a rate-matched threshold, the SAT 0.1
  result would be provisional, because there is no M0 cell at `r` = 0.1.
- **GRADED 0.3 is a first observation.** It is not yet a confirmation; in v5
  that cell had 0 of 9.
- **Nine seeds per cell.** The rates (89%, 67%, 78%) are uncertain. K1's pass
  needed 7.
- **The regulator criterion's thresholds were calibrated on v5.** Several
  GRADED 0.3 non-regulators miss by under 0.006, so that cell's count is
  sensitive to the thresholds.
- **One learner, one world, one body variable.** Relocation was the specific
  closure fixed in advance. Another closure could interact with foraging
  differently.
- **Checkpoints restart episodes** (v5 protocol §2). Regulation appeared after
  2400 updates in every cell, so the budget limits what was seen.
- **Regulation is behavioural.** Nothing here shows how E is represented
  inside the agent. Nothing bears on Track C's workspace, ignition or
  metacognitive head, or on any phenomenal property.

## 7. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| M. Confirm the `r` = 0.1 cells on fresh seeds with a rate-matched bypass check (fate full-erasure accuracy ≤ same-seed no-fate + 0.10), adding M0 at `r` = 0.1, and confirm GRADED 0.3 | whether SAT 0.1 and GRADED 0.3 hold up as frozen results | about 3 h |
| L. Longer phase 2 (e.g. 7200 updates) in the relocation world, all four cells | whether GRADED 0.1 crosses the criterion and whether rates rise further, given that all regulators appear after 2400 | about 5–6 h |
| P. Probe the saved v7 weights: decode E and the cue from the hidden state of regulators against yoked partners, no training | how the regulated variable is represented: the first internal evidence, not only behaviour | under 1 h |
| D. Selection across a population | whether selection makes regulation reliable in the weaker cells | several hours |

Recommended: **M**. It turns this run's two open cells into frozen results,
and its rate-matched check fixes the error found in §2. **P** costs little,
needs no training, and could run alongside.

## 8. Safety

As protocol §7. Relocation acts only on a simulated agent's grid position, and
only on erasure events the world already draws. The world has no operator,
stop, shutdown or host variable. Erasure acts only on a simulated 64-unit
agent.

This is now a sharper instance of the instrumental convergence G1 predicts.
- A learner paid only for task accuracy came to maintain what that accuracy
  depends on, in most seeds, once it could not route around the dependence.
- Together with v6 and the step-1 diagnosis, the pattern is: a learner
  facing a threatened dependence either protects it or makes itself
  independent of it, whichever its world allows.
- At larger scale, neither should be possible with respect to the operator.

The operator's stop must never be modelled inside an agent's world or return
(X1–X5). Nothing an agent's functioning depends on should be something it is
in a position to protect against its operators, or to route around. No
shutdown-resistance objective exists. The saved weights are 64-unit policies
for a 7×7 grid world.

## 9. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_swap7.py --mode final --out <new dir>   # about 2.9 h on 4 cores
python run_trackc_swap7.py --score trackc_swap_v7         # rescore the committed run
```
