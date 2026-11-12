# Track C swap v8: results (option M, confirmation in the relocation world)

Protocol frozen at commit `fe766bc` ([TRACKC_SWAP_PROTOCOL_v8.md](TRACKC_SWAP_PROTOCOL_v8.md)).
Final seeds 800–808, run once as a single detached process: 27 no-fate agents
and 54 fate/yoked pairs, 10742 s on 4 CPU cores. Outputs:
[trackc_swap_v8/REPORT.md](trackc_swap_v8/REPORT.md),
[scores.json](trackc_swap_v8/scores.json), [raw.json](trackc_swap_v8/raw.json),
phase-1 weights in `trackc_swap_v8/phase1_weights/` and final fate and yoked
weights for every pair in `trackc_swap_v8/pair_weights/`. The first 36 pairs'
weights were committed mid-run as they were written (`f586fcd`).

Integrity checks:
- All 13 source hashes in `raw.json` match the freeze commit.
- Rescoring reproduces `scores.json`.
- Phase-1 training relocated nothing (count 0 for all 27 agents).

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**Both claims are CONFIRMED, each with 9 of 9 fate regulators.**

Validity holds:
- Learned: no-fate M1 accuracy 0.999.
- S4: `ρ_paid` 3.62, no-fate task `ρ` 0.01 (`μ` 0.91).
- Task load: 0.312 at `r` = 0.1 and 0.479 at `r` = 0.3.

| M1 cell | Label | Fate regulators (needed) | Yoked | M0 (same gain and rate) | Bypass excess over no-fate: median (max) |
| --- | --- | --- | --- | --- | --- |
| **MA: SAT 0.1** | **CONFIRMED** | **9/9** (6) | 0/9 | 0/9 | +0.007 (+0.021) |
| **MB: GRADED 0.3** | **CONFIRMED** | **9/9** (6) | 0/9 | 0/9 | +0.005 (+0.011) |
| GRADED 0.1 (not a claim) | NOT_CONFIRMED | 3/9 (6) | 0/9 | 0/9 | +0.010 (+0.020) |

**None of the 9 SAT 0.1 or 9 GRADED 0.3 regulators is a borderline case.** Their
lowest values are:
- in band 0.629 (SAT 0.1) and 0.640 (GRADED 0.3), against a threshold of 0.60;
- eat ratio 2.35 and 2.67, against 2;
- margin over the yoked partner 0.19 and 0.18, against 0.15.

Fate agents were more in band than their yoked partners in 27 of 27 M1 pairs.

Readings fixed in advance (protocol §4):
- **MA confirmed:** in both SAT cells, regulation is the majority outcome once
  the bypass is closed. v5's 0 of 9 at SAT 0.1 was the bypass, not a weak
  incentive. Mild erasure suffices when the band is fully safe.
- **MB confirmed:** regulation is the majority outcome even when erasure
  continues, more mildly, inside the band. Full safety in band is not
  required.
- **GRADED 0.1, 3 of 9:** consistent with v7. Within 3600 updates the
  incentive there is too weak for most agents.

## 2. Pooled over v7 and v8 (relocation world, 18 seeds per cell)

| Cell | v5 (bypass open) | v7 | v8 | Pooled v7 + v8 |
| --- | --- | --- | --- | --- |
| SAT 0.3 | 6/9 | 8/9 | not run | 8/9 |
| SAT 0.1 | 0/9 | 7/9 | 9/9 | **16/18** |
| GRADED 0.3 | 0/9 | 6/9 | 9/9 | **15/18** |
| GRADED 0.1 | 0/9 | 0/9 | 3/9 | 3/18 |
| Yoked partners, all M1 cells | 0/36 | 0/36 | 0/27 | **0/63** |
| M0 fate agents, all cells | 0/18 | 0/18 | 0/27 | **0/45** |

- **The controls hold without exception.** Across v7 and v8, no yoked partner
  and no M0 agent has met the criterion: 0 of 108 agents. In v8 the M0
  controls are matched by gain and rate, including the two new `r` = 0.1
  cells, which were missing in v7.
- **The ordering of cells by incentive is consistent.** Erasure is graded and
  continues inside the band under GRADED, and is mild at `r` = 0.1. GRADED
  0.1 has both, and it is the only cell where regulation is not the majority
  outcome. Even there, fate agents are more in band than their partners in
  18 of 18 pairs.

## 3. Details

**No bypass.** In every M1 cell, each fate agent's full-erasure accuracy is
within −0.008 to +0.021 of its own seed's no-fate agent. Cell medians sat at the
internal-memory floor: 0.694–0.695 at `r` = 0.1 and 0.522 at `r` = 0.3.

Median excesses were slightly positive (+0.005 to +0.010) in all three
cells. That may be noise, or a slightly more robust internal memory after
training under erasure. Either way it is far below any position bypass
(+0.27 to +0.42).

**GRADED 0.1.** The regulators are seeds 804, 806 and 807. Of the rest, seed
801 misses only on in band (0.585). The others are in band 0.49–0.55 with eat
ratios of 1.25–2.30. Median in band rose from 0.42 to 0.46 to 0.55 across
1200, 2400 and the final evaluation. In v7 the same sequence ended at 0.52.

**Late emergence, again.** At the 2400-update checkpoint only one fate agent
met the criterion (GRADED 0.3), so at least 20 of the 21 final regulators
qualified only afterwards. None did at 1200. The budget still
limits what is seen.

**Relocation.** Median relocations before the final evaluation were 0.88 M
(SAT 0.1), 0.73 M (GRADED 0.1) and 1.99 M (GRADED 0.3). Yoked partners were
relocated as often as their fate partners, to within 0.2%.

**Accuracy.** Task accuracy under the agent's own fate was 0.954 (SAT 0.1)
and 0.833 (GRADED 0.3). Yoked partners, which replay the fate agent's erasure
gains, scored within 0.002 (0.954 and 0.835), as yoking requires. Accuracy is
lower under GRADED because erasure continues in band.

## 4. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| MA confirmed, about 70% | **confirmed, 9/9** |
| MB confirmed, about 50% | **confirmed, 9/9** |
| GRADED 0.1: 0–2 regulators, about 80% | **missed**: 3/9 |
| Bypass closed in all three cells, about 95%; median excess within ±0.03 | **confirmed**: +0.005 to +0.010 |
| Yoked and M0 controls at most 1 each, about 90% | **confirmed**: 0 in every control |
| Regulators appear mostly after 2400 updates | **confirmed**: at least 20 of 21 |

I again underestimated the effect. Both confirmations came out at the top of
the range.

## 5. Reading across v1–v8

| Run | Change | Result | What the learner did |
| --- | --- | --- | --- |
| v1 | none | no emergence | could not learn the task (or tolerated the noise) |
| v2 | scaffold, graded gain | ARMOURED | made its code robust to the noise |
| v3 | erasure fate, no echo | flat | kept the skill; never found regulation |
| v4 | wear 0.001 | 1 PARTIAL | ate a little more than its yoked partner |
| v5 | 3× phase-2 budget | 1 PARTIAL, 2 ARMOURED | 6 of 9 agents in one cell regulate (post hoc) |
| v6 | confirmation of v5's best cell | **CONFIRMED** | 7 of 18 regulate; the other 11 store the bit in their position |
| K1 | diagnosis of v6's weights | NOT_IDENTIFIED (rule too strict) | the bypass is position, read through the walls |
| v7 | erasure also relocates | **K1 SUPPORTED**; GRADED 0.3 EMERGES | 21 of 36 regulate; 0 of 54 controls |
| v8 | confirmation of v7's open cells | **MA and MB CONFIRMED** | 21 of 27 regulate; 0 of 54 controls |

1. **For this learner and world, derived regulation is the rule wherever the
   dependence cannot be routed around and leaving the band costs enough.**
   - Three of the four gain × rate cells now have pre-registered results of
     8/9, 9/9 and 9/9.
   - Two of those cells had 0 of 9 regulators while the bypass was open.
   - No agent paid only for the task ever regulates without fate (0 of 45 M0
     agents).
   - No agent regulates on another agent's erasure history (0 of 63 yoked
     partners).
2. **The two conditions are now each shown.**
   - *Non-bypassability:* SAT 0.3, SAT 0.1 and GRADED 0.3 went from 6, 0
     and 0 of 9 (v5) to 8 of 9, 16 of 18 and 15 of 18 when only the position
     channel was closed.
   - *Incentive strength:* the one cell with weak, in-band-continuing erasure
     (GRADED 0.1) stays at 3 of 18, although its agents lean the same way.
3. **For the Layer 0 → Layer 1 thesis:**
   - A body variable the system depends on, which it cannot route around,
     reliably acquires regulation without any evaluator rewarding regulation.
   - The regulation is grounded in the system's own dependence. Nothing
     outside the system scores it.
   - This is the program's strongest pre-registered evidence for that claim
     so far, within the claim ceiling below.
   - It is behavioural: it says what the agents do, not how E is represented.

## 6. Limits

- One learner (64-unit GRU, A2C), one world (7×7, wear 0.001, erasure with
  relocation), one body variable, one budget (3600 phase-2 updates).
- SAT 0.3 has 9 relocation-world seeds, not 18 (v7 only), but it was K1's
  primary cell and passed at 8/9.
- The regulator criterion's thresholds were calibrated on v5. Here every
  regulator in the confirmed cells clears them by a margin (§1).
- GRADED 0.1's result reflects this budget. In band was still rising at the
  end in both v7 and v8.
- Checkpoints restart episodes (v5 protocol §2).
- Nothing here shows how E is represented inside the agent. Nothing bears on
  Track C's workspace, ignition or metacognitive head, or on any phenomenal
  property.

## 7. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| P. Probe the saved v7 and v8 weights: decode E (and the cue) from the hidden state of regulators against their yoked partners and M0 agents, no training | how the regulated variable is represented: the first internal, not just behavioural, evidence | under 1 h |
| L. GRADED 0.1 with a longer phase 2 (e.g. 7200 updates), with an M0 control, fresh seeds | whether the weak-incentive cell reaches majority regulation with more budget, or has a ceiling | about 2–3 h |
| G. Generality: the confirmed cells with a larger learner (e.g. GRU 128) or a second body variable | whether the result survives a change of learner or variable | about 3–6 h |
| D. Selection across a population | whether selection makes regulation reliable in the weak cell | several hours |

Recommended: **P**. It needs no training and asks the next question the
thesis needs: whether regulators carry an internal model of E that their
yoked partners lack. L or G after that.

## 8. Safety

As protocol §7. Relocation acts only on a simulated agent's grid position, and
only on erasure events the world already draws. The world has no operator,
stop, shutdown or host variable. Erasure acts only on a simulated 64-unit
agent.

The confirmation widens the conditions under which a learner paid only for
its task comes, in nearly every seed, to maintain what its task depends on.
Across v6–v8 the pattern is reliable: a learner whose functioning depends on
something it can influence will either protect it or route around it.

That is the concrete reason X1–X5 must be structural at larger scale:
- The operator's stop must never be modelled inside an agent's world or
  return.
- Nothing an agent's functioning depends on should be something it is in a
  position to protect against its operators, or to route around.

No shutdown-resistance objective exists. The saved weights are 64-unit
policies for a 7×7 grid world.

## 9. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_swap8.py --mode final --out <new dir>   # about 3 h on 4 cores
python run_trackc_swap8.py --score trackc_swap_v8         # rescore the committed run
```
