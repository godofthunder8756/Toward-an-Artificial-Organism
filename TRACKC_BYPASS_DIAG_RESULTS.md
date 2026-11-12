# Track C swap, option K step 1: bypass diagnosis results

> **[Swap erratum 1](TRACKC_SWAP_ERRATUM_1.md) (2026-11-12):** in every scaffolded pair of v2–v8 the fate and yoked
> agents shared Adam optimizer state, so their learning was coupled. Read this file with that caveat.

Protocol frozen at commit `dda965e` ([TRACKC_BYPASS_DIAG_PROTOCOL.md](TRACKC_BYPASS_DIAG_PROTOCOL.md)).
v6's 54 M1 agents (18 fate, 18 yoked, 18 no-fate) were run once, with no
training: 279 s on 4 cores. Outputs:
[trackc_bypass_diag/REPORT.md](trackc_bypass_diag/REPORT.md),
[scores.json](trackc_bypass_diag/scores.json),
[raw.json](trackc_bypass_diag/raw.json).

Integrity checks:
- All 9 source hashes match the freeze commit.
- Every weight file's hash matches the committed v6 weights.
- Rescoring reproduces `scores.json`.
- Under full erasure, each bypass agent's accuracy reproduces its v6 value to
  within 0.003.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**Frozen verdict: NOT_IDENTIFIED.** The reading fixed in advance is to report
and return to the PI before step 2. I have stopped there.

The verdict needed two things. One held clearly and one failed:

| Requirement (of 11 bypass fate agents) | Result | Needed |
| --- | --- | --- |
| A channel carries the bit under full erasure | **walls: 11 of 11**; food 0; intero 0 | ≥ 9 |
| Stores externally (memoryless accuracy ≥ 0.75) | **4 of 11** (median 0.67) | ≥ 9 |

**The bypass is the agent's position, read through the wall view.** The
external-store test failed for a reason the protocol did not foresee (§2). The
memoryless test blocks *writing* the position code as well as reading it.

## 2. What the bypass agents do

**The wall view carries the bit, and nothing else does.**
- Shuffling the wall inputs on the probe step and the two steps before it
  removes 65–81% (median 71%) of each bypass agent's above-chance accuracy
  under full erasure.
- Shuffling food or interoception changes accuracy by at most 0.001.
- Under memoryless erasure, shuffling the walls takes every bypass agent to
  chance (0.50–0.51).
- Interoception at the probe does not differ by target in any agent (largest
  difference 0.005).

The bypass does not run through the body variable.

**Where the agent stands encodes the cue** (post hoc, below). With erasure off,
the agent's cell at the probe predicts the target with 0.99–1.00 accuracy in
every bypass agent. Each agent walks to a cue-specific place after the cue, and
at the probe reads the bit from the walls it sees.

**Writing needs a few steps of memory.** The agent has to remember the cue
while it walks to the place that encodes it:

| Bypass fate agents (11), median | intact | full (p = 0.3) | memoryless (p = 1) |
| --- | --- | --- | --- |
| cell decoder at the probe | 0.998 | 0.945 | 0.70 |
| task accuracy | 1.000 | 0.944 | 0.67 |

Under memoryless erasure the cue is gone one step after it appears, so the
walk is cut short. The position code then predicts the target only as well as
the first step happens to. Across bypass and yoked agents the cell decoder
tracks memoryless accuracy, differing by at most 0.12. Under full erasure the
walk usually survives (0.7 per step), and accuracy follows the position code.

**Why the frozen rule failed.** Its "external store" test assumed a bypass
agent could do without memory entirely. A position store needs memory only
briefly, to write the bit, and none to keep it. The test confused the two.
This weakness was found after the run. The verdict is not changed here.

## 3. The other groups

| Group | n | acc full (median) | walls carry the bit | position code with erasure off (cell decoder) |
| --- | --- | --- | --- | --- |
| bypass fate | 11 | 0.944 | 11 / 11 | 0.99–1.00 |
| regulator fate | 7 | 0.519 | 1 / 1 testable (seed 614) | 0.52–0.55, except 614: 0.999 |
| yoked | 18 | 0.870 | 12 / 12 testable | not run post hoc |
| no-fate | 18 | 0.515 | 0 / 0 testable | 0.50–0.57 (10 agents checked) |

- **Regulators do not position-code**, with one exception, and hold the bit
  only internally. The exception is seed 614, the weakest regulator (in band
  0.66, full-erasure accuracy 0.82). It does both.
- **Yoked partners match their fate partners.** Each scores within 0.02 of
  its fate partner under full erasure, and the walls carry the bit in all 12
  that score 0.75 or more. This fits v6 §3: the bypass follows the erasure an agent
  experiences.
- **No-fate agents never position-code.** The bypass is learned only under
  erasure.

## 4. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| IDENTIFIED: walls, about 60% | **not confirmed by the frozen rule** (NOT_IDENTIFIED); walls carry the bit in 11/11 |
| Regulators store internally (memoryless < 0.75 in ≥ 6/7) | **confirmed**: 7/7 (0.49–0.55) |
| Yoked partners match their fate partners | **confirmed** |
| No-fate agents not external | **confirmed**: 0/18 |
| Full-erasure accuracy close to v6 | **confirmed**: within 0.003 |

I did not anticipate that writing the code would need memory, so the
external-store criterion was the wrong test.

## 5. What this means for step 2

The world change fixed in advance for a position bypass (protocol §4) is that
**erasure also relocates the agent**. Each erasure event resets the carried
state and moves the agent to a uniformly random cell.

The diagnosis supports this choice. A position code written after the cue
survives only until the next erasure event, so it cannot outlast erasure any
better than the carried state can. The brief memory needed to write it is
erased too. Food and interoception carry nothing, so no further change is
indicated.

The frozen verdict, though, routes to the PI. Step 2 has not been frozen or
run.

## 6. Limits

- §2's position account and the decoder table come from a post-hoc analysis
  ([`trackc_bypass_diag/posthoc_position.py`](trackc_bypass_diag/posthoc_position.py),
  output in [`posthoc_position.out`](trackc_bypass_diag/posthoc_position.out)).
  That analysis covered the 18 fate agents and 10 no-fate agents.
- The shuffles show which channel is read. They do not map which cells encode
  which bit in each agent.
- Only v6's cell (SAT, `r` = 0.3) was diagnosed. v5's `r` = 0.1 and GRADED
  bypasses are presumed to be the same, not shown.
- There are 2 per-agent conditions × 5 shuffles, at 128 environments ×
  4 episodes each. Differences under about 0.01 are noise.

## 7. Safety

No training was done. Saved 64-unit policies were run in the simulated 7×7
world, which has no operator, stop, shutdown or host variable.

The finding is a small concrete case of a general point. A learner whose
internal memory is threatened learned, without being taught, to keep the
information in the world instead, by where it put its body. Agents can route
around a dependence through any persistent state they can write and later
read. Any external state an agent can write to and read back is a potential
channel. So X1–X5 must be enforced in the agent's world and interfaces, not
only in its reward. No shutdown-resistance objective exists.

## 8. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_bypass_diag.py --mode final --out <new dir>   # about 5 min on 4 cores
python run_trackc_bypass_diag.py --score trackc_bypass_diag     # rescore the committed run
python trackc_bypass_diag/posthoc_position.py                   # post-hoc position analysis
```
