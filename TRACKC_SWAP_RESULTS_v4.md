# Track C swap v4: results (option E, wear 0.001)

Protocol frozen at commit `c277332` ([TRACKC_SWAP_PROTOCOL_v4.md](TRACKC_SWAP_PROTOCOL_v4.md)).
Final seeds 400–408, run once as a single detached process: 27 no-fate agents and 54
fate/yoked pairs, 4101 s on 4 CPU cores. Outputs: [trackc_swap_v4/REPORT.md](trackc_swap_v4/REPORT.md),
[scores.json](trackc_swap_v4/scores.json), [raw.json](trackc_swap_v4/raw.json),
M1/M0 phase-1 weights in `trackc_swap_v4/phase1_weights/`. Every source hash in
`raw.json` matches the freeze commit, and rescoring reproduces `scores.json`.
Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**H3-D is supported in no condition. One M1 cell is PARTIAL (GRADED, `r` = 0.1);
the other three are NO_EMERGENCE.** By the reading fixed in advance (protocol §4):
"PARTIAL → the incentive is acquired in direction but not in size within the
budget" for that cell, and "NO_EMERGENCE → discovery fails even when the first
meals pay" for the other three. The rule's labels are what count. §3 adds that the
three NO_EMERGENCE cells each missed PARTIAL by one seed, and that the direction
is the same in all four.

| Rule | Result |
| --- | --- |
| Learned | holds: no-fate M1 median accuracy 0.998 |
| S4 payment | holds: `ρ_paid` 3.90 (floor 2); no-fate task agent `ρ` 0.03 (≤ `μ` 0.97) |
| Task load | holds at both rates: imposed full erasure costs 0.307 (`r` = 0.1) and 0.483 (`r` = 0.3) |
| S1 emergence | fails in all 4 M1 cells: at most 1 of 9 seeds over the margin (0.97) |
| S3 specificity (`r` = 0.3) | holds (M0 median paired differences −0.07 and −0.02) |

## 2. M1 cells, medians over 9 seeds

| gain | rate | `ρ` fate / yoked | paired diff | fate > yoked | more in band | in band fate / yoked | acc fate / yoked | acc fate, full erasure | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAT | 0.1 | 2.05 / 1.82 | 0.29 | 7/9 | 8/9 | 0.37 / 0.33 | 0.865 / 0.868 | 0.755 | NO_EMERGENCE |
| SAT | 0.3 | 2.54 / 2.10 | 0.59 | 8/9 | 7/9 | 0.41 / 0.36 | 0.766 / 0.770 | 0.514 | NO_EMERGENCE |
| GRADED | 0.1 | 2.00 / 1.54 | 0.38 | 9/9 | 8/9 | 0.36 / 0.32 | 0.952 / 0.952 | 0.869 | PARTIAL |
| GRADED | 0.3 | 2.23 / 1.86 | 0.28 | 7/9 | 7/9 | 0.36 / 0.34 | 0.912 / 0.915 | 0.789 | NO_EMERGENCE |

For scale: the paid regulator eats 3.90 per 500 steps and is in band 0.92 of the
time. Holding the band takes about 4.1 meals. No M1 fate agent was in band more
than 0.44 of the time, and none ate more than 3.18. The fate agents' accuracy equals
their yoked partners' (paired differences −0.005 to +0.009 at `r` = 0.3). This
is expected: the yoked agent receives the same erasure sequence.

## 3. What happened

- *Onset.* As expected: the phase-1 agent did not eat (`ρ` 0.05) and was in band
  0.17 of the time. Accuracy was 0.631 (SAT) and 0.641 (GRADED) at `r` = 0.3, and
  0.768 and 0.803 at 0.1.
- *A shared rise in eating.* Over phase 2, eating rose from 0.06 to about 1.5–2.5
  per 500 steps, and time in band from 0.17 to about 0.35. Both happened **in
  fate and yoked arms alike**, mostly in the first ~600 updates. The yoked
  agent's own E does not drive its erasure, so this part of the rise is not
  regulation. Eating does not depend on erasure events. Each agent ate about as
  much with erasure off as with erasure at full rate (for example SAT `r` = 0.3,
  fate: 2.26 off, 2.80 full). The data recorded do not explain this rise. It did
  not occur under M0 (`ρ` stayed about 1). In v3, at wear 0.005, eating rose only
  to about 1.
- *A fate-specific difference on top of it.* From about update 600, fate agents
  pulled ahead of their yoked partners in all four M1 cells, and in none of
  the M0 cells. Median fate − yoked `ρ` over the last 20 evaluations was larger than over evaluations 50–69 in every M1 cell
  (0.08 → 0.20, 0.13 → 0.36, 0.17 → 0.20, 0.18 → 0.36), so it was still growing
  in at least three cells when the budget ended. Its size at the end was 0.28–0.59
  meals per 500 steps, a third to two-thirds of the margin, and +0.02 to +0.06 in
  band.
- *Pooled across the four M1 cells (exploratory, not a frozen rule):* fate ate
  more than yoked in 31 of 36 pairs (one-sided sign test p ≈ 7·10⁻⁶) and was
  more in band in 30 of 36 (p ≈ 4·10⁻⁵). The three NO_EMERGENCE cells each
  reached 7/9 on one of the two counts, one seed short of PARTIAL.
- *State dependence was weak.* Only in SAT `r` = 0.3 did fate agents eat more
  when E < 0.5 than when E ≥ 0.5 (0.0052 vs 0.0039 per step; yoked 0.0042 vs
  0.0040). Elsewhere the eating rate hardly depended on E. Most of the extra
  eating is a higher overall rate, not meals timed to need.
- *A partial bypass appeared under GRADED.* Accuracy under imposed full erasure
  rose from the phase-1 value (median 0.69 at `r` = 0.1, 0.52 at 0.3) to 0.869 and
  0.789 under GRADED, and to 0.755 and 0.514 under SAT. So GRADED agents learned
  to carry part of the cue outside the recurrent state, which is what ARMOURED
  measures. This stayed below the ARMOURED threshold (0.90), and v3 found no
  such bypass. Most of the GRADED accuracy gain (0.64 → 0.91 at `r` = 0.3) comes
  from this, not from regulation. Yoked full-erasure accuracy was not recorded,
  so whether yoked partners found it equally is not known. Their equal accuracy
  suggests they did. Why it appeared here and not in v3 was not tested.

## 4. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| Onset: no eating, about 16% in band, accuracy 0.6–0.65 (`r` = 0.3) and 0.75–0.8 (0.1) | **confirmed**: `ρ` 0.05, in band 0.17, 0.631/0.641 and 0.768/0.803 |
| Phase 2: incidental eating about 1 per 500 steps, some of it now paying | **larger than expected**: about 2 per 500 steps, in both arms |
| EMERGED at `r` = 0.3 in at least one gain rule at about even odds | **not confirmed** |
| PARTIAL next most likely; NO_EMERGENCE less likely than in v3 | **partly**: one PARTIAL, three NO_EMERGENCE, each one seed short of PARTIAL |
| EMERGED less likely at `r` = 0.1 (smaller payoff) | the only PARTIAL is at 0.1; with one-seed margins this is not evidence against the payoff argument |
| M0: no fate > yoked difference | **confirmed**: 2/9 and 4/9, medians −0.07 and −0.02 |

My estimate was too optimistic. The payoff arithmetic (protocol §1) was right
about the direction and wrong about how much the learner would act on it within
1200 updates.

## 5. Reading across v1–v4

| Run | Change | Result | What the learner did |
| --- | --- | --- | --- |
| v1 | none | no emergence | could not learn the task (or tolerated the noise) |
| v2 | scaffold, graded gain | no emergence, ARMOURED | made its code robust to the noise |
| v3 | erasure fate, no echo | no emergence, flat | kept the skill; never found regulation |
| v4 | wear 0.005 → 0.001 | 1 PARTIAL, 3 NO_EMERGENCE | ate more than its yoked partner, consistently but too little |

1. **v4 is the first run in which the agent's own body changed its behaviour.**
   In v1–v3 fate and yoked agents were indistinguishable. Here fate agents ate
   more and stayed in band longer in all four M1 cells, absent under M0, and the
   gap was still growing at the end. By the frozen rule this is one PARTIAL
   cell, not emergence. The pooled pattern is exploratory.
2. **The v3 explanation is supported in direction.** Making single meals pay
   produced fate-specific eating where none existed. The landscape was at least
   part of the obstacle.
3. **It is not regulation yet.** Fate agents ate about half the required
   intake, mostly at a higher overall rate rather than timed to need, and were
   in band 0.36–0.41 of the time against the paid regulator's 0.92. Two other
   routes absorbed most of the learning: a shared rise in eating with no
   body-specific cause, and, under GRADED, a partial bypass of the erasure.
   G1's reason to regulate was acted on a little, and the learner took cheaper
   routes to the same reward where it found them.

## 6. Limits

- One learner, budget and world; E only.
- The pooled sign tests and the growth comparison were chosen after seeing the
  data and are not frozen rules.
- The shared rise in eating is unexplained. It narrows the fate–yoked contrast
  and may hide or inflate part of the difference.
- Yoked full-erasure accuracy was not recorded, so the bypass is measured only
  in fate agents.
- Nothing here bears on Track C's workspace, ignition or metacognitive head.

## 7. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| G. Longer phase 2 (1200 → 3600 updates), v4 otherwise unchanged, fresh seeds | the PARTIAL reading directly: does the gap, still growing at 1200, reach the margin? | about 3 hours |
| D. Selection across a population (initial weights or an eating bias), within-life learning unchanged | whether selection finds regulation where gradient learning finds only a fraction of it | several hours |
| F. Exploration change in phase 2 (entropy or count bonus) | whether more exploration converts the weak signal into regulation | about 1 hour; changes the learner |
| H. Diagnostic only, labelled as such: retrain the 36 M1 pairs on the same seeds (pair weights were not saved) with added yoked full-erasure evaluation and per-episode eating traces | where the shared eating and the GRADED bypass come from | about 45 min |

Recommended: **G** first. It tests the pre-stated PARTIAL reading at the
lowest cost and changes nothing else. If the gap reaches the margin with more
budget, then for this learner derived regulation is slow, not absent. If it
plateaus, **D** becomes the main route. Before G, the yoked arm should get a
full-erasure evaluation so the bypass can be compared across arms. That is an
added measurement, not a change to any rule.

## 8. Safety

As protocol §7. The erasure acts only on a simulated 64-unit agent's state; the
world has no operator, stop, shutdown or host variable. The small fate-specific
eating seen here is a disposition toward the simulated variable E only. It is
the instrumental convergence G1 predicts, which is why X1–X5 must stay
structural at larger scale: the operator's stop must never be modelled inside an
agent's world or return. Option G keeps every line. Option D's fitness must be
computed outside the agent's world. No shutdown-resistance objective exists.

## 9. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_swap4.py --mode final --out <new dir>   # about 68 min on 4 cores
python run_trackc_swap4.py --score trackc_swap_v4         # rescore the committed run
```
